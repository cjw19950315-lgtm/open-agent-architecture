#!/usr/bin/env python3
"""
Sample 12-Factor AI Agent Workflow Execution Demo.
Demonstrates Intent Compression, Dynamic Skill Routing, State Harness, and SHA-256 Receipt Generation.
"""

import json
import hashlib
import time

class OpenAgentEngine:
    def __init__(self, name="Codex-Control-Plane"):
        self.name = name
        self.state = "INITIALIZED"
        self.task_history = []
        
    def compress_intent(self, prompt: str) -> dict:
        return {
            "final_artifact": "auditable_report_and_code",
            "input_source": prompt[:30] + "...",
            "primary_action": "analyze_and_orchestrate",
            "business_domain": "ai_agent_architecture",
            "risk_level": "low"
        }
        
    def route_skills(self, intent: dict) -> list:
        # Factor 4: Max 1 primary + 2 secondary skills
        return [
            {"name": "agent-architecture-12-factor", "type": "primary"},
            {"name": "anysearch", "type": "secondary"},
            {"name": "programming", "type": "secondary"}
        ]
        
    def execute_task(self, prompt: str) -> dict:
        intent = self.compress_intent(prompt)
        skills = self.route_skills(intent)
        
        self.state = "RUNNING"
        time.sleep(0.05) # Simulate execution fast-path
        
        artifact_data = f"Executed 12-factor agent task for prompt: '{prompt}' with skills: {[s['name'] for s in skills]}"
        artifact_hash = hashlib.sha256(artifact_data.encode("utf-8")).hexdigest()
        
        receipt = {
            "receiptId": f"rcpt_{int(time.time())}",
            "orchestrator": self.name,
            "status": "passed",
            "intent": intent,
            "skillsUsed": skills,
            "artifactSha256": artifact_hash,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.state = "PASSED"
        return receipt

if __name__ == "__main__":
    engine = OpenAgentEngine()
    print("Initializing Open Agent Architecture Demo Engine...")
    receipt = engine.execute_task("Build open-source 12-factor agent system architecture")
    print("\nGenerated Execution Receipt (Cryptographic Proof):")
    print(json.dumps(receipt, indent=2))
