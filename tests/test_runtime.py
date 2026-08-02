"""End-to-end tests for the OAA runtime: real task chain, resume, DAG parallelism,
path isolation, ground-truth protection, and receipt chaining."""

import json
import os
import shutil
import tempfile
import threading
import time
import unittest

from oaa.runtime import Runtime
from oaa.memory import GroundTruthStore, GroundTruthWriteDenied
from oaa.dag import DAG, DAGNode, DAGExecutor
from oaa.receipt import ReceiptBuilder
from oaa.security import PathPolicy, PathViolation
from oaa.tools import ToolRuntime, FilesystemTool
from oaa.observability import Tracer


def seed_workspace(directory):
    with open(os.path.join(directory, "README.md"), "w", encoding="utf-8") as fh:
        fh.write("# Test Project\n\nA tiny architecture project used by tests.\n")
    with open(os.path.join(directory, "pyproject.toml"), "w", encoding="utf-8") as fh:
        fh.write("[project]\nname = 'oaa-test'\nversion = '1.0.0'\n")


class RuntimeChainTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="oaa_test_")
        seed_workspace(self.dir)

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def test_full_chain_real_task(self):
        runtime = Runtime(workspace=self.dir, approval_mode="auto")
        result = runtime.run(
            "Read README.md and pyproject.toml, analyze the project architecture, and write analysis.md"
        )
        self.assertEqual(result["state"], "PASSED")
        analysis_path = os.path.join(self.dir, "analysis.md")
        self.assertTrue(os.path.exists(analysis_path))
        with open(analysis_path, "r", encoding="utf-8") as fh:
            self.assertIn("Source: README.md", fh.read())

        receipt = runtime.get_receipt(result["task_id"])
        self.assertIsNotNone(receipt)
        for field in ("task_input_hash", "intent", "plan", "tool_calls",
                      "state_transitions", "artifacts", "verification", "environment",
                      "receipt_hash"):
            self.assertIn(field, receipt)
        self.assertTrue(receipt["plan"]["nodes"])
        self.assertTrue(receipt["tool_calls"])
        self.assertTrue(receipt["verification"]["passed"])
        state_values = [v for t in receipt["state_transitions"] for v in (t["from"], t["to"])]
        self.assertIn("RUNNING", state_values)
        self.assertIn("VERIFYING", state_values)
        self.assertIn("PASSED", state_values)

    def test_resume_after_process_restart(self):
        runtime = Runtime(workspace=self.dir, approval_mode="auto")
        task_id = runtime.control.create_task(
            "Read README.md and pyproject.toml, analyze the project architecture, and write analysis.md"
        )
        runtime.control.plan_task(task_id)

        # simulate a crash after the read wave: persist partial state + results
        harness = runtime.control.harness
        session = harness.load_session(task_id)
        session["state"] = "RUNNING"
        session["completed_nodes"] = ["read_readme", "read_pyproject"]
        session["node_results"] = {
            "read_readme": {"path": "README.md", "content": "# Test Project", "bytes": 15},
            "read_pyproject": {"path": "pyproject.toml", "content": "[project]", "bytes": 10},
        }
        harness.save_session(task_id, session)

        # new Runtime instance == process restart
        runtime2 = Runtime(workspace=self.dir, approval_mode="auto")
        state = runtime2.resume(task_id)
        self.assertEqual(state["state"], "PASSED")
        self.assertTrue(os.path.exists(os.path.join(self.dir, "analysis.md")))

    def test_dag_parallel_fanout_fanin(self):
        lock = threading.Lock()
        active = []
        peak = [0]

        def make(name):
            def func(context, results):
                with lock:
                    active.append(name)
                    peak[0] = max(peak[0], len(active))
                time.sleep(0.05)
                with lock:
                    active.remove(name)
                return name
            return func

        dag = DAG("parallel")
        a = dag.add_node(DAGNode("a", func=make("a")))
        b = dag.add_node(DAGNode("b", func=make("b")))
        c = dag.add_node(DAGNode("c", func=make("c")))
        join = dag.add_node(DAGNode("join", deps=("a", "b", "c"), func=lambda ctx, res: sorted(res[k] for k in ("a", "b", "c"))))
        results = DAGExecutor(max_workers=4, tracer=Tracer()).execute(dag, {})
        self.assertEqual(results["join"], ["a", "b", "c"])
        self.assertGreaterEqual(peak[0], 2)

    def test_path_isolation(self):
        tracer = Tracer()
        policy = PathPolicy(self.dir)
        runtime = ToolRuntime(tracer=tracer)
        runtime.register(FilesystemTool())
        ctx = {"policy": policy, "approval": None, "masker": None}
        runtime.bind(ctx)
        with self.assertRaises(PathViolation):
            runtime.call("filesystem", {"op": "read", "path": "../outside.txt"})

    def test_ground_truth_protection(self):
        store = GroundTruthStore(os.path.join(self.dir, "vault"))
        with self.assertRaises(GroundTruthWriteDenied):
            store.write_note("decision", "agent text", author="agent")
        store.write_note("decision", "human confirmed", author="human")
        self.assertIn("human confirmed", store.read_note("decision"))

    def test_receipt_chain(self):
        first = ReceiptBuilder("task_1")
        first.add_input("hello")
        r1 = first.build()
        second = ReceiptBuilder("task_1", parent_receipt_id=r1["receipt_id"])
        second.add_input("hello")
        second.set_parent_hash(r1["receipt_hash"])
        r2 = second.build()
        self.assertEqual(r2["parent_receipt_id"], r1["receipt_id"])
        self.assertEqual(r2["parent_receipt_hash"], r1["receipt_hash"])
        self.assertNotEqual(r1["receipt_hash"], r2["receipt_hash"])


if __name__ == "__main__":
    unittest.main()