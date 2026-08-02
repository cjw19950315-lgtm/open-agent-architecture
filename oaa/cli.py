"""Command-line interface for the OAA runtime.

Usage:
  python -m oaa run "PROMPT" --workspace DIR [--approval auto|manual]
  python -m oaa state TASK_ID --workspace DIR
  python -m oaa resume TASK_ID --workspace DIR
  python -m oaa cancel TASK_ID --workspace DIR
  python -m oaa approve TASK_ID --workspace DIR
  python -m oaa retry TASK_ID --workspace DIR
  python -m oaa receipt TASK_ID --workspace DIR
"""

import argparse
import json
import sys

from oaa.runtime import Runtime


def _runtime(args):
    workspace = getattr(args, "workspace", None) or "."
    approval = getattr(args, "approval", None) or "auto"
    return Runtime(workspace=workspace, approval_mode=approval)


def _add_common(subparser):
    subparser.add_argument("--workspace", default=None, help="workspace directory (sandbox root)")
    subparser.add_argument("--approval", default=None, choices=("auto", "manual"), help="approval mode")


def cmd_run(args):
    runtime = _runtime(args)
    result = runtime.run(args.prompt)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_state(args):
    runtime = _runtime(args)
    print(json.dumps(runtime.get_state(args.task_id), ensure_ascii=False, indent=2))


def cmd_resume(args):
    runtime = _runtime(args)
    print(json.dumps(runtime.resume(args.task_id), ensure_ascii=False, indent=2))


def cmd_cancel(args):
    runtime = _runtime(args)
    print(json.dumps(runtime.cancel(args.task_id), ensure_ascii=False, indent=2))


def cmd_approve(args):
    runtime = _runtime(args)
    print(json.dumps(runtime.approve(args.task_id, approved=args.yes), ensure_ascii=False, indent=2))


def cmd_retry(args):
    runtime = _runtime(args)
    print(json.dumps(runtime.retry(args.task_id), ensure_ascii=False, indent=2))


def cmd_receipt(args):
    runtime = _runtime(args)
    receipt = runtime.get_receipt(args.task_id)
    if receipt is None:
        print(json.dumps({"error": "no receipt for task"}, ensure_ascii=False, indent=2))
        sys.exit(1)
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


def build_parser():
    parser = argparse.ArgumentParser(prog="oaa", description="Open Agent Architecture runtime")
    sub = parser.add_subparsers(dest="command", required=True)

    p_run = sub.add_parser("run", help="run a new task")
    p_run.add_argument("prompt", help="task prompt")
    _add_common(p_run)
    p_run.set_defaults(func=cmd_run)

    for name, fn, arg_name in (
        ("state", cmd_state, "task_id"),
        ("resume", cmd_resume, "task_id"),
        ("cancel", cmd_cancel, "task_id"),
        ("retry", cmd_retry, "task_id"),
        ("receipt", cmd_receipt, "task_id"),
    ):
        p = sub.add_parser(name, help=name + " a task")
        p.add_argument(arg_name, help="task id")
        _add_common(p)
        p.set_defaults(func=fn)

    p_approve = sub.add_parser("approve", help="approve a task")
    p_approve.add_argument("task_id")
    p_approve.add_argument("--yes", action="store_true", default=True, help="approve (default yes)")
    _add_common(p_approve)
    p_approve.set_defaults(func=cmd_approve)
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()