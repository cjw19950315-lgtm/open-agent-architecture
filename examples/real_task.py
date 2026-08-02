"""Real end-to-end task: read sources, analyze, write report, verify, receipt.

Run:
  python examples/real_task.py [workspace]
"""

import json
import os
import sys

from oaa.runtime import Runtime


def main():
    workspace = sys.argv[1] if len(sys.argv) > 1 else "."
    runtime = Runtime(workspace=workspace, approval_mode="auto")
    result = runtime.run(
        "Read README.md and pyproject.toml, analyze the project architecture, and write analysis.md"
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    receipt = runtime.get_receipt(result["task_id"])
    if receipt:
        print("\nReceipt:", receipt["receipt_id"])
        print("Task input hash:", receipt["task_input_hash"])
        print("Tool calls:", len(receipt["tool_calls"]))
        print("State transitions:", [t["to"] for t in receipt["state_transitions"]])
        print("Verification passed:", receipt["verification"]["passed"])
        print("Artifact:", receipt["artifacts"])
    return 0 if result["state"] == "PASSED" else 1


if __name__ == "__main__":
    sys.exit(main())