#!/usr/bin/env python3
"""
good-night-brief.py
Low-cognitive-load end-of-day closeout for companion-self instances.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _tail_lines(text: str, n: int = 8) -> List[str]:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    return lines[-n:]


def _guess_day_status(evidence_text: str) -> str:
    t = evidence_text.lower()
    if "blocked" in t:
        return "blocked"
    if "done" in t or "completed" in t or "finished" in t:
        return "finished_well"
    return "partial"


def _build_one_signal(skill_work_tail: List[str], evidence_tail: List[str]) -> str:
    if skill_work_tail:
        return f"WORK signal: {skill_work_tail[-1][:160]}"
    if evidence_tail:
        return f"Evidence signal: {evidence_tail[-1][:160]}"
    return "No strong signal captured; default to one small, shippable action tomorrow."


def _build_top_action(gate_text: str) -> str:
    lower = gate_text.lower()
    if "candidate" in lower or "## candidates" in lower:
        return "Review pending gate candidates first."
    return "Start with one high-confidence execution action."


def _build_stop_condition(day_status: str) -> str:
    if day_status == "blocked":
        return "Stop after one unblock attempt; escalate instead of looping."
    return "Stop after top action is complete; avoid adding new maintenance tasks."


def _build_reset_cue(mode: str) -> str:
    if mode == "minimal":
        return "Close today; resume in your first focus window tomorrow."
    if mode == "reflective":
        return "Let go of unresolved details; keep only one clear next step."
    return "Release unfinished loops; begin with the top action tomorrow."


def _append_or_write_memory(memory_path: Path, block: str) -> None:
    marker = "## Good night closeout (generated)"
    existing = _read_text(memory_path)
    if marker in existing:
        # Replace latest generated section by truncating from marker.
        prefix = existing.split(marker)[0].rstrip()
        payload = f"{prefix}\n\n{block}\n"
    else:
        payload = existing.rstrip() + ("\n\n" if existing.strip() else "") + block + "\n"
    memory_path.write_text(payload, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate a short good-night closeout.")
    ap.add_argument("--user", required=True, help="Instance user id (users/<id>/)")
    ap.add_argument("--mode", default="standard", choices=["minimal", "standard", "reflective"])
    ap.add_argument("--emit-json", action="store_true")
    ap.add_argument("--write-closeout", action="store_true")
    ap.add_argument("--suggest-gate", action="store_true")
    ap.add_argument("--max-lines", type=int, default=120)
    args = ap.parse_args()

    repo_root = Path.cwd()
    user_dir = repo_root / "users" / args.user
    if not user_dir.exists():
        print(f"Missing instance path: {user_dir}", file=sys.stderr)
        return 2

    evidence_path = user_dir / "self-evidence.md"
    memory_path = user_dir / "self-memory.md"
    gate_path = user_dir / "recursion-gate.md"
    skill_work_path = user_dir / "self-skill-work.md"
    handoff_dir = user_dir / "daily-handoff"
    handoff_path = handoff_dir / "night-handoff.json"

    evidence = _read_text(evidence_path)
    memory = _read_text(memory_path)
    gate = _read_text(gate_path)
    skill_work = _read_text(skill_work_path)

    evidence_tail = _tail_lines(evidence, 12)
    skill_work_tail = _tail_lines(skill_work, 12)
    day_status = _guess_day_status(evidence)
    one_signal = _build_one_signal(skill_work_tail, evidence_tail)
    tomorrow_top_action = _build_top_action(gate)
    stop_condition = _build_stop_condition(day_status)
    reset_cue = _build_reset_cue(args.mode)

    gate_suggestions: List[str] = []
    if args.suggest_gate:
        gate_suggestions.append("If today's signal is identity-relevant, stage a candidate in recursion-gate.md.")

    payload: Dict[str, Any] = {
        "user": args.user,
        "date": date.today().isoformat(),
        "mode": args.mode,
        "dayStatus": day_status,
        "oneSignal": one_signal,
        "tomorrowTopAction": tomorrow_top_action,
        "stopCondition": stop_condition,
        "optionalResetCue": reset_cue,
        "gateSuggestions": gate_suggestions,
        "warnings": [],
    }

    if not evidence:
        payload["warnings"].append("self-evidence.md missing or empty; used fallback status heuristics.")
    if not memory:
        payload["warnings"].append("self-memory.md missing or empty; writing closeout will create/refresh it.")

    if args.write_closeout:
        generated = (
            "## Good night closeout (generated)\n\n"
            f"- generated_by: good-night-brief.py\n"
            f"- generated_at: {datetime.utcnow().isoformat()}Z\n"
            f"- day_status: {day_status}\n"
            f"- one_signal: {one_signal}\n"
            f"- tomorrow_top_action: {tomorrow_top_action}\n"
            f"- stop_condition: {stop_condition}\n"
            f"- optional_reset_cue: {reset_cue}\n"
        )
        _append_or_write_memory(memory_path, generated)
        handoff_dir.mkdir(parents=True, exist_ok=True)
        handoff_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    if args.emit_json:
        print(json.dumps(payload, indent=2))
        return 0

    lines = [
        "### Good night closeout",
        f"- Day status: {day_status}",
        f"- One signal: {one_signal}",
        f"- Tomorrow top action: {tomorrow_top_action}",
        f"- Stop condition: {stop_condition}",
        f"- Optional reset cue: {reset_cue}",
    ]
    if gate_suggestions:
        lines.append(f"- Gate suggestion: {gate_suggestions[0]}")
    if args.write_closeout:
        lines.append(f"- Handoff written: {handoff_path}")
    if payload["warnings"]:
        for warning in payload["warnings"]:
            lines.append(f"- Warning: {warning}")

    print("\n".join(lines[: max(args.max_lines, 1)]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

