"""Chained cryptographic execution receipts (not just artifact checksums)."""

import hashlib
import json
import platform
import sys
import time
import uuid


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def canonical_json(payload):
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)


class ReceiptBuilder:
    def __init__(self, task_id, parent_receipt_id=None, model_name=None, model_config=None):
        self.task_id = task_id
        self.parent_receipt_id = parent_receipt_id
        self.model_name = model_name or "unknown"
        self.model_config = model_config or {}
        self.parts = {
            "schema": "oaa.receipt.v1",
            "task_id": task_id,
            "task_input": None,
            "task_input_hash": None,
            "intent": None,
            "plan": None,
            "tool_calls": [],
            "state_transitions": [],
            "artifacts": [],
            "verification": None,
            "environment": None,
            "parent_receipt_id": parent_receipt_id,
            "parent_receipt_hash": None,
            "timestamp": time.time(),
        }

    def add_input(self, text):
        self.parts["task_input"] = text[:2000]
        self.parts["task_input_hash"] = sha256_bytes(text.encode("utf-8"))

    def add_intent(self, intent):
        self.parts["intent"] = intent.to_dict()

    def add_plan(self, dag_snapshot):
        self.parts["plan"] = dag_snapshot

    def add_tool_call(self, name, params, result):
        self.parts["tool_calls"].append({
            "name": name,
            "params_hash": sha256_bytes(canonical_json(params).encode("utf-8")),
            "result_hash": sha256_bytes(canonical_json(result).encode("utf-8")),
        })

    def add_state_transition(self, source, target):
        self.parts["state_transitions"].append({"from": source, "to": target})

    def add_artifact(self, path, digest):
        self.parts["artifacts"].append({"path": path, "sha256": digest})

    def add_verification(self, report):
        self.parts["verification"] = {"passed": report.get("passed"), "checks": report.get("checks")}

    def add_environment(self):
        self.parts["environment"] = {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "provider": self.model_name,
            "model_config": self.model_config,
        }

    def set_parent_hash(self, parent_hash):
        self.parts["parent_receipt_hash"] = parent_hash

    def build(self):
        payload = dict(self.parts)
        receipt_hash = sha256_bytes(canonical_json(payload).encode("utf-8"))
        payload["receipt_id"] = "rcpt_" + receipt_hash[:16]
        payload["receipt_hash"] = receipt_hash
        return payload


def digest_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()