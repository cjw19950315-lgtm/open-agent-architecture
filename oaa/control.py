"""Control Plane: task lifecycle, risk assessment, approvals, orchestration, verification."""

import json
import os
import time
import uuid

from oaa.state import TaskState, StateMachine, InvalidTransition
from oaa.intent import Intent, IntentCompiler
from oaa.security import CredentialMasker, PathPolicy, ApprovalGate
from oaa.observability import Tracer, Metrics
from oaa.tools import Tool, ToolRuntime, FilesystemTool
from oaa.skills import SkillRegistry, register_builtin_skills
from oaa.dag import DAG, DAGNode, DAGExecutor, DAGExecutionError
from oaa.agents import AgentLoop, DeterministicProvider
from oaa.harness import SessionHarness
from oaa.memory import IngestionStore, GroundTruthStore, EvidenceStore
from oaa.verification import VerificationGate
from oaa.receipt import ReceiptBuilder, digest_file


class _SkillTool(Tool):
    def __init__(self, skill):
        super().__init__(skill.name, skill.description)
        self._skill = skill

    def call(self, ctx, params):
        return self._skill.execute(ctx, params)


class ControlPlane:
    def __init__(self, workspace, approval_mode="auto", approval_callback=None,
                 model_provider=None, base_dir=".oaa", max_workers=4, tracer=None):
        self.workspace = os.path.abspath(workspace)
        os.makedirs(self.workspace, exist_ok=True)
        self.base_dir = os.path.join(self.workspace, base_dir)
        os.makedirs(self.base_dir, exist_ok=True)
        self.tracer = tracer or Tracer(log_path=os.path.join(self.base_dir, "logs", "runtime.log"))
        self.metrics = Metrics()
        self.masker = CredentialMasker()
        self.policy = PathPolicy(self.workspace)
        self.approval = ApprovalGate(mode=approval_mode, callback=approval_callback)
        self.registry = register_builtin_skills(SkillRegistry())
        self.tool_runtime = ToolRuntime(tracer=self.tracer, masker=self.masker)
        self.tool_runtime.register(FilesystemTool())
        for _skill in self.registry._skills.values():
            self.tool_runtime.register(_SkillTool(_skill))
        self.harness = SessionHarness(os.path.join(self.base_dir, "sessions"))
        self.ingestion = IngestionStore(os.path.join(self.base_dir, "ingestion"))
        self.ground_truth = GroundTruthStore(os.path.join(self.workspace, "vault"))
        self.evidence = EvidenceStore(os.path.join(self.base_dir, "evidence"))
        self.verification = VerificationGate(masker=self.masker, approval=self.approval, tracer=self.tracer)
        self.provider = model_provider or DeterministicProvider()
        self.compiler = IntentCompiler()
        self.max_workers = max_workers
        self._dags = {}

    def _build_context(self, task_id, prompt):
        ctx = {
            "task": task_id,
            "prompt": prompt,
            "policy": self.policy,
            "masker": self.masker,
            "approval": self.approval,
            "verification": self.verification,
            "tracer": self.tracer,
        }
        ctx["tools"] = self.tool_runtime.bind(ctx)
        return ctx

    def create_task(self, prompt, task_id=None):
        task_id = task_id or ("task_" + uuid.uuid4().hex[:12])
        session = self.harness.create_session(task_id, prompt)
        self.metrics.inc("tasks_created")
        self.tracer.event("task_created", task_id=task_id)
        return task_id

    def plan_task(self, task_id):
        session = self.harness.load_session(task_id)
        machine = StateMachine(session["state"])
        if machine.state == TaskState.CREATED:
            machine.transition(TaskState.PLANNING)
            machine.transition(TaskState.READY)
        session["state"] = machine.state.value
        self.harness.save_session(task_id, session)

        intent = self.compiler.compile(session["input_text"])
        primary, auxiliary = self.registry.select_skills(intent)

        dag = DAG("plan_" + task_id)
        dag.add_node(DAGNode("read_readme", func=self._read_node("README.md"), name="read_readme"))
        dag.add_node(DAGNode("read_pyproject", func=self._read_node("pyproject.toml"), name="read_pyproject"))
        dag.add_node(DAGNode("reason", deps=("read_readme", "read_pyproject"), func=self._reason_node(),
                             name="reason", timeout=90))
        dag.add_node(DAGNode("write_report", deps=("reason",), func=self._write_node(),
                             name="write_report", writes=True))
        dag.add_node(DAGNode("verify", deps=("write_report",), func=self._verify_node(),
                             name="verify", timeout=60))

        session["plan"] = dag.snapshot()
        session["intent"] = intent.to_dict()
        session["selected_skills"] = [s.name for s in primary + auxiliary]
        session["state"] = TaskState.READY.value
        self.harness.save_session(task_id, session)
        self._dags[task_id] = dag
        return dag

    def _read_node(self, path):
        def node(context, results):
            return self._run_skill(context, "read_file", {"path": path})
        return node

    def _reason_node(self):
        def node(context, results):
            session = self.harness.load_session(context["task"])
            seeds = [
                {"role": "tool", "name": "filesystem", "content": json.dumps(results.get("read_readme", {}))},
                {"role": "tool", "name": "filesystem", "content": json.dumps(results.get("read_pyproject", {}))},
            ]
            loop = AgentLoop(self.provider, context["tools"], tracer=self.tracer, max_steps=6)
            system = ("You are the OAA reason node. Analyze the provided project sources "
                      "and return the analysis text as your final answer. WRITE_DISABLED")
            tool_spec = {
                "type": "function",
                "function": {
                    "name": "analyze_markdown",
                    "description": "Analyze markdown sources and produce a structured summary.",
                    "parameters": {
                        "type": "object",
                        "properties": {"sources": {"type": "array", "items": {"type": "string"}}},
                        "required": ["sources"],
                    },
                },
            }
            result = loop.run(system, session["input_text"], tool_specs=[tool_spec], seed_tool_results=seeds)
            return result.to_dict()
        return node

    def _write_node(self):
        def node(context, results):
            content = (results.get("reason") or {}).get("content", "")
            return self._run_skill(context, "write_file", {"path": "analysis.md", "content": content})
        return node

    def _verify_node(self):
        def node(context, results):
            report = self._run_skill(context, "verify_artifact", {"path": "analysis.md"})
            if not report.get("passed"):
                raise ValueError("verification failed: " + json.dumps(report, ensure_ascii=False))
            return report
        return node

    def _run_skill(self, context, name, args):
        skill = self.registry._skills[name]
        with self.tracer.span("skill:" + name):
            return skill.execute(context, args)

    def run_task(self, task_id, resume=False):
        session = self.harness.load_session(task_id)
        machine = StateMachine(session["state"])
        if session.get("plan") is None:
            self.plan_task(task_id)
            session = self.harness.load_session(task_id)
            machine = StateMachine(session["state"])
        if machine.state == TaskState.READY or machine.state == TaskState.CREATED:
            try:
                machine.transition(TaskState.RUNNING)
            except InvalidTransition as exc:
                session["error"] = str(exc)
                self.harness.save_session(task_id, session)
                return self.get_state(task_id)

        session["state"] = machine.state.value
        session["error"] = None
        self.harness.save_session(task_id, session)

        dag = self._dags.get(task_id)
        if dag is None:
            dag = self.plan_task(task_id)
            session = self.harness.load_session(task_id)

        completed = set(session.get("completed_nodes", []))
        initial = session.get("node_results", {})

        def on_wave(done, results):
            self.harness.checkpoint(task_id, TaskState.RUNNING.value, len(done), done,
                                    extra={"node_results": results})

        context = self._build_context(task_id, session["input_text"])
        executor = DAGExecutor(max_workers=self.max_workers, tracer=self.tracer)
        try:
            results = executor.execute(dag, context, completed=completed,
                                       initial_results=initial, on_wave_complete=on_wave)
        except Exception as exc:
            session = self.harness.load_session(task_id)
            machine = StateMachine(session["state"])
            try:
                machine.transition(TaskState.FAILED)
            except InvalidTransition:
                machine = StateMachine(TaskState.RUNNING)
                machine.transition(TaskState.FAILED)
            session["state"] = machine.state.value
            session["error"] = str(exc)
            self.harness.save_session(task_id, session)
            self.metrics.inc("tasks_failed")
            self.tracer.event("task_failed", task_id=task_id, error=str(exc))
            return self.get_state(task_id)

        session = self.harness.load_session(task_id)
        machine = StateMachine(session["state"])
        machine.transition(TaskState.VERIFYING)
        session["state"] = machine.state.value
        self.harness.save_session(task_id, session)

        report = results.get("verify", {})
        if not report.get("passed"):
            machine.transition(TaskState.FAILED)
            session["state"] = machine.state.value
            session["error"] = "verification gate rejected artifact"
            self.harness.save_session(task_id, session)
            self.metrics.inc("tasks_failed")
            return self.get_state(task_id)

        machine.transition(TaskState.PASSED)
        receipt = self._build_receipt(task_id, results, report, machine)
        receipt_path = self.evidence.save_receipt(receipt)
        session["state"] = machine.state.value
        session["artifact"] = "analysis.md"
        session["receipt_ids"] = session.get("receipt_ids", []) + [receipt["receipt_id"]]
        session["last_receipt_hash"] = receipt["receipt_hash"]
        session["completed_nodes"] = sorted(results.keys())
        session["node_results"] = results
        self.harness.save_session(task_id, session)
        self.metrics.inc("tasks_passed")
        self.tracer.event("task_passed", task_id=task_id, receipt=receipt["receipt_id"], evidence=receipt_path)
        return self.get_state(task_id)

    def _build_receipt(self, task_id, results, report, machine):
        session = self.harness.load_session(task_id)
        intent_dict = session.get("intent") or {}
        intent = Intent(prompt=session["input_text"], **intent_dict)
        builder = ReceiptBuilder(
            task_id=task_id,
            parent_receipt_id=session.get("last_receipt_hash"),
            model_name=self.provider.name,
            model_config=self.provider.config,
        )
        builder.add_input(session["input_text"])
        builder.add_intent(intent)
        builder.add_plan(session.get("plan"))
        for call in self.tool_runtime.calls:
            builder.add_tool_call(call["tool"], call.get("params", {}), call.get("result", {}))
        history = machine.history
        for index in range(len(history) - 1):
            builder.add_state_transition(history[index], history[index + 1])
        artifact_path = os.path.join(self.workspace, "analysis.md")
        builder.add_artifact("analysis.md", digest_file(artifact_path))
        builder.add_verification(report)
        builder.add_environment()
        if session.get("last_receipt_hash"):
            builder.set_parent_hash(session["last_receipt_hash"])
        return builder.build()

    def approve(self, task_id, approved=True):
        session = self.harness.load_session(task_id)
        machine = StateMachine(session["state"])
        if machine.state == TaskState.WAITING_APPROVAL and approved:
            machine.transition(TaskState.RUNNING)
            session["state"] = machine.state.value
            session["approval"] = {"approved": True, "ts": time.time()}
            self.harness.save_session(task_id, session)
        return self.get_state(task_id)

    def cancel(self, task_id):
        session = self.harness.load_session(task_id)
        machine = StateMachine(session["state"])
        try:
            machine.transition(TaskState.CANCELLED)
        except InvalidTransition:
            pass
        session["state"] = machine.state.value
        session["cancelled_at"] = time.time()
        self.harness.save_session(task_id, session)
        self.metrics.inc("tasks_cancelled")
        return self.get_state(task_id)

    def retry(self, task_id):
        session = self.harness.load_session(task_id)
        machine = StateMachine(session["state"])
        if machine.state != TaskState.FAILED:
            return self.get_state(task_id)
        machine.transition(TaskState.RUNNING)
        session["state"] = machine.state.value
        session["completed_nodes"] = []
        session["node_results"] = {}
        session["error"] = None
        self.harness.save_session(task_id, session)
        return self.run_task(task_id)

    def resume(self, task_id):
        session = self.harness.load_session(task_id)
        if session["state"] in (TaskState.PASSED.value,):
            return self.get_state(task_id)
        if session["state"] in (TaskState.RUNNING.value, TaskState.READY.value):
            return self.run_task(task_id, resume=True)
        return self.get_state(task_id)

    def get_state(self, task_id):
        session = self.harness.load_session(task_id)
        return {
            "task_id": task_id,
            "state": session["state"],
            "artifact": session.get("artifact"),
            "error": session.get("error"),
            "receipt_ids": session.get("receipt_ids", []),
            "completed_nodes": session.get("completed_nodes", []),
            "checkpoints": len(session.get("checkpoints", [])),
            "updated_at": session.get("updated_at"),
        }

    def get_receipt(self, task_id):
        session = self.harness.load_session(task_id)
        ids = session.get("receipt_ids", [])
        if not ids:
            return None
        return self.evidence.load_receipt(ids[-1])