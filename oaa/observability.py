"""Structured logs, tracing spans, metrics, and execution timeline."""

import json
import os
import threading
import time
import uuid


class _Span:
    def __init__(self, data, tracer):
        self.data = data
        self.tracer = tracer

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.data["end"] = time.time()
        self.data["duration_ms"] = round((self.data["end"] - self.data["start"]) * 1000, 3)
        if exc is not None:
            self.data["error"] = str(exc)
        return False


class Tracer:
    def __init__(self, log_path=None):
        self.spans = []
        self.events = []
        self._lock = threading.Lock()
        self._log_path = log_path

    def span(self, name, **attrs):
        data = {"id": uuid.uuid4().hex[:12], "name": name, "start": time.time(), "attrs": attrs}
        with self._lock:
            self.spans.append(data)
        return _Span(data, self)

    def event(self, name, **attrs):
        event = {"ts": time.time(), "name": name}
        event.update(attrs)
        with self._lock:
            self.events.append(event)
            if self._log_path is not None:
                try:
                    os.makedirs(os.path.dirname(self._log_path), exist_ok=True)
                    with open(self._log_path, "a", encoding="utf-8") as fh:
                        fh.write(json.dumps(event) + "\n")
                except OSError:
                    pass
        return event

    def timeline(self):
        return [{"name": e["name"], "ts": e["ts"]} for e in self.events]

    def snapshot(self):
        return {"spans": self.spans, "events": self.events}


class Metrics:
    def __init__(self):
        self.counts = {}

    def inc(self, name):
        self.counts[name] = self.counts.get(name, 0) + 1

    def snapshot(self):
        return dict(self.counts)