"""Governance and release-engineering tests: state machine, verification gate,
manual approval failure path, ground-truth versioning, CLI smoke, receipt fields."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from oaa.state import StateMachine, TaskState, InvalidTransition
from oaa.security import CredentialMasker
from oaa.verification import VerificationGate
from oaa.memory import GroundTruthStore
from oaa.runtime import Runtime


class StateMachineTest(unittest.TestCase):
    def test_invalid_transition_raises(self):
        machine = StateMachine(TaskState.CREATED)
        with self.assertRaises(InvalidTransition):
            machine.transition(TaskState.READY)

    def test_valid_lifecycle(self):
        machine = StateMachine(TaskState.CREATED)
        machine.transition(TaskState.PLANNING)
        machine.transition(TaskState.READY)
        machine.transition(TaskState.RUNNING)
        machine.transition(TaskState.VERIFYING)
        machine.transition(TaskState.PASSED)
        self.assertEqual(machine.state, TaskState.PASSED)


class VerificationGateTest(unittest.TestCase):
    def test_secret_scan_rejects_artifact(self):
        gate = VerificationGate(masker=CredentialMasker())
        report = gate.verify(artifact_text="sk-abcdef1234567890abcdef")
        self.assertFalse(report.passed)
        names = [c["name"] for c in report.checks]
        self.assertIn("secret_scan", names)


class ApprovalFailurePathTest(unittest.TestCase):
    def test_manual_approval_without_callback_fails_task(self):
        directory = tempfile.mkdtemp(prefix="oaa_approval_")
        try:
            with open(os.path.join(directory, "README.md"), "w", encoding="utf-8") as fh:
                fh.write("# T\n")
            with open(os.path.join(directory, "pyproject.toml"), "w", encoding="utf-8") as fh:
                fh.write("[project]\n")
            runtime = Runtime(workspace=directory, approval_mode="manual")
            result = runtime.run("Read README.md and pyproject.toml, analyze, and write analysis.md")
            self.assertEqual(result["state"], "FAILED")
            self.assertFalse(os.path.exists(os.path.join(directory, "analysis.md")))
        finally:
            shutil.rmtree(directory, ignore_errors=True)


class GroundTruthVersioningTest(unittest.TestCase):
    def test_human_write_creates_history_version(self):
        directory = tempfile.mkdtemp(prefix="oaa_vault_")
        try:
            store = GroundTruthStore(os.path.join(directory, "vault"))
            store.write_note("decision", "v1", author="human")
            store.write_note("decision", "v2", author="human")
            self.assertIn("v2", store.read_note("decision"))
            history = os.listdir(os.path.join(directory, "vault", ".history"))
            self.assertTrue(any("decision.v" in name for name in history))
        finally:
            shutil.rmtree(directory, ignore_errors=True)


class CliSmokeTest(unittest.TestCase):
    def test_cli_run_passes(self):
        repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        directory = tempfile.mkdtemp(prefix="oaa_cli_")
        try:
            with open(os.path.join(directory, "README.md"), "w", encoding="utf-8") as fh:
                fh.write("# CLI Test\n")
            with open(os.path.join(directory, "pyproject.toml"), "w", encoding="utf-8") as fh:
                fh.write("[project]\nname='cli'\n")
            proc = subprocess.run(
                [sys.executable, "-m", "oaa", "run",
                 "Read README.md and pyproject.toml, analyze, and write analysis.md",
                 "--workspace", directory, "--approval", "auto"],
                capture_output=True, text=True, timeout=120, cwd=repo,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn('"state": "PASSED"', proc.stdout)
        finally:
            shutil.rmtree(directory, ignore_errors=True)


class ReceiptFieldTest(unittest.TestCase):
    def test_receipt_contains_all_core_fields(self):
        directory = tempfile.mkdtemp(prefix="oaa_receipt_")
        try:
            with open(os.path.join(directory, "README.md"), "w", encoding="utf-8") as fh:
                fh.write("# R\n")
            with open(os.path.join(directory, "pyproject.toml"), "w", encoding="utf-8") as fh:
                fh.write("[project]\n")
            runtime = Runtime(workspace=directory, approval_mode="auto")
            result = runtime.run("Read README.md and pyproject.toml, analyze, and write analysis.md")
            receipt = runtime.get_receipt(result["task_id"])
            for field in ("task_input_hash", "intent", "plan", "tool_calls", "state_transitions",
                          "artifacts", "verification", "environment", "parent_receipt_id",
                          "parent_receipt_hash", "receipt_hash", "timestamp"):
                self.assertIn(field, receipt)
            self.assertIn("provider", receipt["environment"])
        finally:
            shutil.rmtree(directory, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()