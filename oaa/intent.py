"""Intent compilation: compress a user request into routing dimensions."""

import hashlib
import json


class Intent:
    def __init__(self, prompt, final_artifact, input_source, primary_action, business_domain, risk_level):
        self.prompt = prompt
        self.final_artifact = final_artifact
        self.input_source = input_source
        self.primary_action = primary_action
        self.business_domain = business_domain
        self.risk_level = risk_level

    def to_dict(self):
        return {
            "final_artifact": self.final_artifact,
            "input_source": self.input_source,
            "primary_action": self.primary_action,
            "business_domain": self.business_domain,
            "risk_level": self.risk_level,
        }

    def fingerprint(self):
        canonical = json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


class IntentCompiler:
    def compile(self, prompt):
        lowered = prompt.lower()
        if any(k in lowered for k in ("analy", "review", "audit", "summar")):
            action = "analyze"
        elif any(k in lowered for k in ("write", "create", "generate", "produce", "save")):
            action = "write"
        elif "read" in lowered:
            action = "read"
        else:
            action = "orchestrate"

        if any(k in lowered for k in ("readme", "doc", "architecture", "spec")):
            domain = "documentation"
        elif any(k in lowered for k in ("code", "python", "source", "test")):
            domain = "code"
        else:
            domain = "general"

        if any(k in lowered for k in ("delete", "remove ", "network", "http", "shell")):
            risk = "high"
        else:
            risk = "low"

        artifact = "report" if action == "analyze" else "file" if action == "write" else "data"
        return Intent(prompt=prompt, final_artifact=artifact, input_source=prompt[:80], primary_action=action, business_domain=domain, risk_level=risk)