"""Verification gate: schema validation, policy checks, security scan, tests, and approval."""

import time


class VerificationReport:
    def __init__(self, passed, checks, artifact_sha256=None, duration_ms=0.0):
        self.passed = passed
        self.checks = checks
        self.artifact_sha256 = artifact_sha256
        self.duration_ms = duration_ms

    def to_dict(self):
        return {
            "passed": self.passed,
            "checks": self.checks,
            "artifact_sha256": self.artifact_sha256,
            "duration_ms": self.duration_ms,
        }


class VerificationGate:
    def __init__(self, masker=None, approval=None, tracer=None):
        self.masker = masker
        self.approval = approval
        self.tracer = tracer

    def verify(self, task=None, artifact_path=None, artifact_text=None, schema=None, policy=None, tests=None):
        from oaa.receipt import sha256_bytes
        start = time.time()
        checks = []

        if artifact_text is None and artifact_path is not None:
            with open(artifact_path, "r", encoding="utf-8") as fh:
                artifact_text = fh.read()

        if artifact_text is not None:
            digest = sha256_bytes(artifact_text.encode("utf-8"))
            checks.append({"name": "artifact_hash", "ok": True, "detail": digest})
        else:
            digest = None
            checks.append({"name": "artifact_hash", "ok": False, "detail": "no artifact"})

        if schema is not None:
            try:
                import json
                payload = json.loads(artifact_text) if artifact_text else {}
                missing = [k for k in schema.get("required", []) if k not in payload]
                checks.append({"name": "schema_validation", "ok": not missing, "detail": missing or "ok"})
            except Exception as exc:
                checks.append({"name": "schema_validation", "ok": False, "detail": str(exc)})

        if policy is not None:
            try:
                issues = policy(artifact_text) if artifact_text else []
                checks.append({"name": "policy_validation", "ok": not issues, "detail": issues or "ok"})
            except Exception as exc:
                checks.append({"name": "policy_validation", "ok": False, "detail": str(exc)})

        if self.masker is not None and artifact_text is not None:
            has_secret = self.masker.contains_secret(artifact_text)
            checks.append({"name": "secret_scan", "ok": not has_secret, "detail": "secret-like pattern found" if has_secret else "clean"})

        if tests is not None:
            try:
                ok, detail = tests()
                checks.append({"name": "tests", "ok": ok, "detail": detail})
            except Exception as exc:
                checks.append({"name": "tests", "ok": False, "detail": str(exc)})

        approval_decision = None
        if self.approval is not None:
            approval_decision = self.approval.request({"action": "commit_artifact", "task": task})
            checks.append({"name": "approval", "ok": bool(approval_decision.get("approved")), "detail": approval_decision})

        passed = all(c["ok"] for c in checks)
        duration_ms = round((time.time() - start) * 1000, 3)
        return VerificationReport(passed=passed, checks=checks, artifact_sha256=digest, duration_ms=duration_ms)