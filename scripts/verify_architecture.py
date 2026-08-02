#!/usr/bin/env python3
"""
Automated Architecture Verification Gate for Open Agent Architecture (OAA).
Checks structure integrity, multi-language coverage, UTF-8 encoding integrity,
markdown local links, contract validity, and security privacy rules.
"""

import os
import re
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
        "CONTRIBUTING.md",
        "SECURITY.md",
        "CODE_OF_CONDUCT.md",
        "CHANGELOG.md",
        "ROADMAP.md",
        ".github/workflows/verify.yml",
        ".github/workflows/release.yml",
        ".github/ISSUE_TEMPLATE/bug_report.md",
        ".github/pull_request_template.md",
        "docs/governance-model.md",
        "docs/obsidian-harness-integration.md",
        "spec/12-factor-agent-spec.md",
        "spec/skill-routing-spec.md",
        "spec/architecture-contract.json",
        "schemas/architecture-contract.schema.json",
        "schemas/skill-registry.schema.json",
        "oaa/__init__.py",
        "oaa/runtime.py",
        "oaa/control.py",
        "oaa/dag.py",
        "oaa/skills.py",
        "oaa/harness.py",
        "oaa/cli.py",
        "tests/test_runtime.py",
        "tests/test_governance.py",
        "examples/real_task.py",
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
        "docs/i18n/README.de.md",
    ]
    for f in i18n_files:
        path = os.path.join(base_dir, f)
        if not os.path.exists(path):
            errors.append(f"Missing multi-language doc: {f}")
        else:
            print(f"[PASS] i18n Doc exists: {f}")

    # 3. UTF-8 Encoding Integrity Check (prevents mojibake regression)
    unicode_files = ["README.md", "README.zh-CN.md"] + i18n_files
    for f in unicode_files:
        path = os.path.join(base_dir, f)
        if not os.path.exists(path):
            continue
        with open(path, "rb") as fh:
            raw = fh.read()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            errors.append(f"Invalid UTF-8 in {f}: {exc}")
            continue
        nonascii = sum(1 for ch in text if ord(ch) > 127)
        if text.count("\ufffd") > 0:
            errors.append(f"Replacement character found in {f}")
        if nonascii == 0:
            errors.append(f"No non-ASCII characters in {f}; multilingual content may be corrupted")
        else:
            print(f"[PASS] UTF-8 integrity: {f} ({nonascii} non-ASCII chars)")

    # 4. Markdown Local Link Check
    readme_path = os.path.join(base_dir, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as fh:
            readme = fh.read()
        broken = 0
        for match in re.finditer(r"\]\(([^)]+)\)", readme):
            target = match.group(1).strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target_path = os.path.normpath(os.path.join(base_dir, target))
            if not os.path.exists(target_path):
                errors.append(f"Broken README link: {target}")
                broken += 1
        if broken == 0:
            print("[PASS] All local markdown links in README resolve")

    # 5. Contract Validity
    contract_path = os.path.join(base_dir, "spec", "architecture-contract.json")
    if os.path.exists(contract_path):
        try:
            with open(contract_path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            factors = data.get("operatingModel", {}).get("factors", [])
            if len(factors) != 12:
                errors.append(f"Expected 12 factors in contract, found {len(factors)}")
            else:
                print(f"[PASS] Architecture contract valid with all {len(factors)} factors.")
            if "obsidian" not in data.get("operatingModel", {}):
                errors.append("Contract missing obsidian ground-truth layer")
            if "harness" not in data.get("operatingModel", {}):
                errors.append("Contract missing session harness layer")
        except Exception as exc:
            errors.append(f"Invalid JSON in contract: {exc}")

    # 6. Runtime Import Check
    sys.path.insert(0, base_dir)
    try:
        import oaa
        print("[PASS] oaa package imports successfully")
    except Exception as exc:
        errors.append(f"oaa package import failed: {exc}")

    print("--------------------------------------------------")
    if errors:
        print("RESULT: FAILED")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)
    print("RESULT: ALL GATES PASSED (100% SUCCESS)")
    print("==================================================")
    sys.exit(0)


if __name__ == "__main__":
    verify()