"""Session Harness: durable checkpoints, resume after restart, receipt linkage."""

import json
import os
import time


class SessionHarness:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def _path(self, task_id):
        return os.path.join(self.base_dir, task_id + ".json")

    def create_session(self, task_id, input_text):
        session = {
            "task_id": task_id,
            "input_text": input_text,
            "state": "CREATED",
            "step": 0,
            "completed_nodes": [],
            "checkpoints": [],
            "receipt_ids": [],
            "last_receipt_hash": None,
            "created_at": time.time(),
            "updated_at": time.time(),
        }
        self.save_session(task_id, session)
        return session

    def checkpoint(self, task_id, state, step, completed_nodes, extra=None):
        session = self.load_session(task_id)
        session["state"] = state
        session["step"] = step
        session["completed_nodes"] = sorted(completed_nodes)
        session["updated_at"] = time.time()
        checkpoint = {
            "ts": time.time(),
            "state": state,
            "step": step,
            "completed_nodes": sorted(completed_nodes),
        }
        if extra:
            checkpoint.update(extra)
        session["checkpoints"].append(checkpoint)
        self.save_session(task_id, session)
        return checkpoint

    def save_session(self, task_id, session):
        with open(self._path(task_id), "w", encoding="utf-8") as fh:
            json.dump(session, fh, ensure_ascii=False, indent=2)

    def load_session(self, task_id):
        path = self._path(task_id)
        if not os.path.exists(path):
            raise KeyError("session not found: %s" % task_id)
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)

    def list_sessions(self):
        return sorted(f[:-5] for f in os.listdir(self.base_dir) if f.endswith(".json"))