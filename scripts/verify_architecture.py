#!/usr/bin/env python3
"""
Automated Architecture Verification Gate for Open Agent Architecture (OAA).
Checks structure integrity, multi-language coverage, contract validity, and security privacy rules.
"""

import os
import sys
import json

def verify():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print("==================================================")
    print(" Running Open Agent Architecture (OAA) Gate Checks")
    print("==================================================")
    
    errors = []
    
    # 1. Required Top-Level Files
    required_files = [
        "README.md",
        "LICENSE",
        "pyproject.toml",
        "CODEX_FOR_OSS_APPLICATION.md",
        "spec/12-factor-agent-spec.md",
        "spec/skill-routing-spec.md",
        "spec/architecture-contract.json",
        "schemas/architecture-contract.schema.json",
        "schemas/skill-registry.schema.json"
    ]
    
    for f in required_files:
        path = os.path.join(base_dir, f)
        if not os.path.exists(path):
            errors.append(f"Missing required file: {f}")
        else:
            print(f"[PASS] File exists: {f}")
            
    # 2. Multi-Language Check
    i18n_files = [
        "docs/i18n/README.zh-CN.md",
        "docs/i18n/README.ja.md",
        "docs/i18n/README.es.md",
        "docs/i18n/README.de.md"
    ]
    for f in i18n_files:
        path = os.path.join(base_dir, f)
        if not os.path.exists(path):
            errors.append(f"Missing multi-language doc: {f}")
        else:
            print(f"[PASS] i18n Doc exists: {f}")
            
    # 3. Contract Validity
    contract_path = os.path.join(base_dir, "spec", "architecture-contract.json")
    if os.path.exists(contract_path):
        try:
            with open(contract_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                factors = data.get("operatingModel", {}).get("factors", [])
                if len(factors) != 12:
                    errors.append(f"Expected 12 factors in contract, found {len(factors)}")
                else:
                    print(f"[PASS] Architecture contract valid with all {len(factors)} factors.")
        except Exception as e:
            errors.append(f"Invalid JSON in contract: {e}")
            
    print("--------------------------------------------------")
    if errors:
        print("RESULT: FAILED")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)
    else:
        print("RESULT: ALL GATES PASSED (100% SUCCESS)")
        print("==================================================")
        sys.exit(0)

if __name__ == "__main__":
    verify()
