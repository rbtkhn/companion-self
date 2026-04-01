#!/usr/bin/env python3
"""
cadence-dream.py — consolidated dream runner for companion-self instances.

End-of-day consolidation in one command.  Runs good-night-brief.py with
appropriate flags, then reports git status so the operator sees uncommitted
work before closing the day.

The night brief writes daily-handoff/night-handoff.json — the artifact
that cadence-coffee.py (via good-morning-brief.py) picks up tomorrow.

Usage
-----
    python3 scripts/cadence-dream.py --user demo
    python3 scripts/cadence-dream.py --user demo --mode reflective
    python3 scripts/cadence-dream.py --user demo --dry-run
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent


def _run(argv: list[str]) -> int:
    print(f"\n{'=' * 60}\n$ {' '.join(argv)}\n{'=' * 60}\n", flush=True)
    r = subprocess.run(argv, cwd=str(_REPO))
    return r.returncode


def _git_summary() -> str:
    """Uncommitted-work snapshot for end-of-day awareness."""
    status = subprocess.run(
        ["git", "status", "-sb"], cwd=str(_REPO),
        capture_output=True, text=True,
    )
    diff_stat = subprocess.run(
        ["git", "diff", "--stat"], cwd=str(_REPO),
        capture_output=True, text=True,
    )
    out = status.stdout.strip()
    if diff_stat.stdout.strip():
        out += "\n\nUnstaged changes:\n" + diff_stat.stdout.strip()
    return out


def main() -> int:
    p = argparse.ArgumentParser(
        description="Dream — consolidated night cadence runner for companion-self instances."
    )
    p.add_argument(
        "--user", required=True,
        help="Instance user id (users/<id>/)",
    )
    p.add_argument(
        "--mode", "-m",
        choices=("minimal", "standard", "reflective"),
        default="standard",
        help="Dream mode (default: standard)",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Run night brief without writing closeout or handoff",
    )
    p.add_argument(
        "--suggest-gate",
        action="store_true",
        help="Include gated candidate suggestions in the night brief",
    )
    args = p.parse_args()
    user = args.user
    py = sys.executable

    night_cmd = [py, "scripts/good-night-brief.py", "--user", user, "--mode", args.mode]
    if not args.dry_run:
        night_cmd.append("--write-closeout")
    if args.suggest_gate:
        night_cmd.append("--suggest-gate")

    code = _run(night_cmd)
    if code != 0:
        return code

    print(f"\n{'=' * 60}\n$ git status (end-of-day)\n{'=' * 60}\n", flush=True)
    print(_git_summary())

    return 0


if __name__ == "__main__":
    sys.exit(main())
