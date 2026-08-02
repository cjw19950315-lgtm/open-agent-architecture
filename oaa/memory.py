"""Three-layer memory: ingestion, ground truth (Obsidian vault), session/evidence."""

import json
import os
import time


class MemoryStore:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def _path(self, name):
        safe = name.replace("..", "_").replace("/", "_").replace("\\", "_")
        return os.path.join(self.base_dir, safe)


class IngestionStore(MemoryStore):
    """Raw sources, always marked unconfirmed until a human reviews them."""

    def save_source(self, name, text, source_url=None):
        path = self._path(name + ".md")
        frontmatter = "---\nid: %s\ntype: source\nstatus: unconfirmed\nsource: %s\ncreated_at: %s\n---\n\n"
        content = frontmatter % (name, source_url or "", time.time()) + text
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        return path

    def list_sources(self):
        return sorted(os.listdir(self.base_dir))


class GroundTruthWriteDenied(Exception):
    pass


class GroundTruthStore(MemoryStore):
    """Obsidian-style vault. Only human authors may write; agents cannot overwrite ground truth."""

    def __init__(self, base_dir):
        super().__init__(base_dir)
        self.history_dir = os.path.join(base_dir, ".history")
        os.makedirs(self.history_dir, exist_ok=True)

    def write_note(self, name, content, author):
        if author != "human":
            raise GroundTruthWriteDenied("agent write to ground truth denied (author=%r)" % author)
        path = self._path(name + ".md")
        if os.path.exists(path):
            version = str(int(time.time()))
            history_path = os.path.join(self.history_dir, "%s.v%s.md" % (name, version))
            os.replace(path, history_path)
        frontmatter = "---\nid: %s\ntype: note\nstatus: confirmed\nsource: human\nupdated_at: %s\n---\n\n"
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(frontmatter % (name, time.time()) + content)
        return path

    def read_note(self, name):
        path = self._path(name + ".md")
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()

    def list_notes(self):
        return sorted(os.listdir(self.base_dir))


class SessionStore(MemoryStore):
    def save_session(self, task_id, session):
        path = os.path.join(self.base_dir, task_id + ".json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(session, fh, ensure_ascii=False, indent=2)

    def load_session(self, task_id):
        path = os.path.join(self.base_dir, task_id + ".json")
        if not os.path.exists(path):
            raise KeyError("session not found: %s" % task_id)
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)

    def list_sessions(self):
        return sorted(f[:-5] for f in os.listdir(self.base_dir) if f.endswith(".json"))


class EvidenceStore(MemoryStore):
    def save_receipt(self, receipt):
        path = os.path.join(self.base_dir, receipt["receipt_id"] + ".json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(receipt, fh, ensure_ascii=False, indent=2)
        return path

    def load_receipt(self, receipt_id):
        path = os.path.join(self.base_dir, receipt_id + ".json")
        if not os.path.exists(path):
            raise KeyError("receipt not found: %s" % receipt_id)
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)

    def list_receipts(self):
        return sorted(f[:-5] for f in os.listdir(self.base_dir) if f.endswith(".json"))