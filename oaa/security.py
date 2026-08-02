"""Zero-trust security primitives: path isolation, credential masking, command policy, approvals."""

import os
import re


_SECRET_PATTERNS = [
    re.compile(r"(sk-[A-Za-z0-9]{16,})"),
    re.compile(r"(api[_-]?key\s*[=:]\s*['\"]?[A-Za-z0-9_\-]{8,})", re.IGNORECASE),
    re.compile(r"(Bearer\s+[A-Za-z0-9\-._~+/]+=*)", re.IGNORECASE),
]


class CredentialMasker:
    @staticmethod
    def mask(text):
        for pattern in _SECRET_PATTERNS:
            text = pattern.sub("[REDACTED]", text)
        return text

    @staticmethod
    def contains_secret(text):
        return any(pattern.search(text) for pattern in _SECRET_PATTERNS)


class PathViolation(Exception):
    pass


class PathPolicy:
    def __init__(self, workspace):
        self.workspace = os.path.abspath(workspace)

    def resolve(self, relative):
        candidate = os.path.abspath(os.path.join(self.workspace, relative))
        if candidate != self.workspace and not candidate.startswith(self.workspace + os.sep):
            raise PathViolation("path escapes workspace: %s" % relative)
        return candidate

    def within(self, absolute):
        absolute = os.path.abspath(absolute)
        return absolute == self.workspace or absolute.startswith(self.workspace + os.sep)


class CommandViolation(Exception):
    pass


class CommandPolicy:
    ALLOWED = {"echo", "dir", "ls", "type", "cat", "python"}

    def check(self, command):
        parts = command.strip().split()
        if not parts or parts[0] not in self.ALLOWED:
            raise CommandViolation("command not allowed: %r" % command)
        return True


class ApprovalGate:
    def __init__(self, mode="auto", callback=None):
        self.mode = mode
        self.callback = callback

    def request(self, action):
        if self.mode == "auto":
            return {"approved": True, "mode": "auto", "action": action}
        if self.callback is not None:
            decision = self.callback(action)
            return {"approved": bool(decision.get("approved")), "mode": "callback", "action": action, **decision}
        return {"approved": False, "mode": "manual", "action": action, "reason": "awaiting human approval"}