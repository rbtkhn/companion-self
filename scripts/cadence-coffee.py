#!/usr/bin/env python3
"""
cadence-coffee.py — consolidated coffee runner for companion-self instances.

Single entry point for all morning startup modes.  Assembles the right
combination of good-morning-brief.py options (and optional git snapshot)
depending on the chosen mode.

Modes
-----
  standard   Full coffee: good-morning-brief (standard) + branch snapshot
  light      Lighter sip: good-morning-brief (minimal) + compact branch line
  deep       Deep coffee: good-morning-brief (deep, --check-sync) + branch snapshot
  closeout   Night closeout: good-night-brief (--write-closeout --suggest-gate)

Usage
-----
    python3 scripts/cadence-coffee.py --user demo
    python3 scripts/cadence-coffee.py --user demo --mode light
    python3 scripts/cadence-coffee.py --user demo --mode deep
    python3 scripts/cadence-coffee.py --user demo --mode closeout
    python3 scripts/cadence-coffee.py --user demo --write-intention
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
MODES = ("standard", "light", "deep", "closeout")


def _run(argv: list[str], *, label: str | None = None) -> int:
    display = label or " ".join(argv)
    print(f"\n{'=' * 60}\n$ {display}\n{'=' * 60}\n", flush=True)
    r = subprocess.run(argv, cwd=str(_REPO))
    return r.returncode


def _branch_snapshot(*, compact: bool = False) -> str:
    """Git branch hygiene status."""
    status = subprocess.run(
        ["git", "status", "-sb"], cwd=str(_REPO),
        capture_output=True, text=True,
    )
    status_out = status.stdout.strip()

    if compact:
        return f"Branch: {status_out}"

    branches = subprocess.run(
        ["git", "branch", "-vv"], cwd=str(_REPO),
        capture_output=True, text=True,
    )
    branch_out = branches.stdout.strip()
    non_main = [
        line.strip() for line in branch_out.splitlines()
        if line.strip()
        and not line.strip().startswith("* main")
        and not line.strip().startswith("main")
    ]
    if not non_main:
        return "Branch hygiene: clean (main only)."
    return (
        f"Branch snapshot:\n{status_out}\n\n"
        f"Branches:\n{branch_out}\n\n"
        f"Non-main branches: {len(non_main)} — review before next merge."
    )


def main() -> int:
    p = argparse.ArgumentParser(
        description="Coffee — consolidated morning cadence runner for companion-self instances."
    )
    p.add_argument(
        "--user", required=True,
        help="Instance user id (users/<id>/)",
    )
    p.add_argument(
        "--mode", "-m",
        choices=MODES,
        default="standard",
        help="Coffee mode (default: standard)",
    )
    p.add_argument(
        "--write-intention",
        action="store_true",
        help="Write daily intention note via good-morning-brief.py",
    )
    p.add_argument(
        "--check-sync",
        action="store_true",
        help="Force sync checks even outside deep mode",
    )
    args = p.parse_args()
    user = args.user
    py = sys.executable

    morning = [py, "scripts/good-morning-brief.py", "--user", user]
    night = [py, "scripts/good-night-brief.py", "--user", user]

    steps: list[list[str]] = []

    if args.mode == "standard":
        cmd = morning + ["--mode", "standard"]
        if args.check_sync:
            cmd.append("--check-sync")
        if args.write_intention:
            cmd.append("--write-intention")
        steps.append(cmd)

    elif args.mode == "light":
        cmd = morning + ["--mode", "minimal"]
        if args.check_sync:
            cmd.append("--check-sync")
        if args.write_intention:
            cmd.append("--write-intention")
        steps.append(cmd)

    elif args.mode == "deep":
        cmd = morning + ["--mode", "deep", "--check-sync"]
        if args.write_intention:
            cmd.append("--write-intention")
        steps.append(cmd)

    elif args.mode == "closeout":
        steps.append(night + ["--write-closeout", "--suggest-gate"])

    for argv in steps:
        code = _run(argv)
        if code != 0:
            return code

    if args.mode != "closeout":
        compact = args.mode == "light"
        print(f"\n{'=' * 60}\n$ git branch snapshot\n{'=' * 60}\n", flush=True)
        print(_branch_snapshot(compact=compact))

    return 0


if __name__ == "__main__":
    sys.exit(main())
