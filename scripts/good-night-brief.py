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
from typing import Any, Dict, List, Tuple, Union

HANDOFF_SCHEMA_VERSION = 2

GateSuggestionEntry = Union[str, Dict[str, str]]


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


def _top_action_and_reason(gate_text: str) -> Tuple[str, str]:
    lower = gate_text.lower()
    if "candidate" in lower or "## candidates" in lower:
        return (
            "Review pending gate candidates first.",
            "Gate surface shows pending candidates; address or defer before opening new execution lanes.",
        )
    return (
        "Start with one high-confidence execution action.",
        "No urgent gate signal; default to one scoped execution step.",
    )


def _build_stop_condition(day_status: str, energy_fit: str) -> str:
    if day_status == "blocked":
        base = "Stop after one unblock attempt; escalate instead of looping."
    else:
        base = "Stop after top action is complete; avoid adding new maintenance tasks."
    if energy_fit == "low":
        return f"{base} (low energy: do not open a second lane tomorrow.)"
    if energy_fit == "high":
        return f"{base} (higher energy: after top action, allow one bounded follow-up.)"
    return base


def _tomorrow_energy_fit(mode: str) -> str:
    if mode == "minimal":
        return "low"
    if mode == "reflective":
        return "high"
    return "normal"


def _build_reset_cue(mode: str) -> str:
    if mode == "minimal":
        return "Close today; resume in your first focus window tomorrow."
    if mode == "reflective":
        return "Let go of unresolved details; keep only one clear next step."
    return "Release unfinished loops; begin with the top action tomorrow."


def _quiet_run(
    one_signal: str,
    skill_work_tail: List[str],
    evidence_tail: List[str],
    day_status: str,
) -> bool:
    if one_signal.startswith("No strong signal"):
        return True
    if not skill_work_tail and not evidence_tail and day_status == "partial":
        return True
    return False


def _active_lane_hint(
    skill_work_tail: List[str],
    evidence_tail: List[str],
    gate_text: str,
) -> str:
    lower = gate_text.lower()
    if "candidate" in lower or "## candidates" in lower:
        return "GATE"
    if skill_work_tail:
        return "WORK"
    if evidence_tail:
        return "SEED"
    return "NONE"


def _ignore_tomorrow(gate_text: str, day_status: str) -> str:
    lower = gate_text.lower()
    if "candidate" in lower:
        return "Ignore scope expansion until gate candidates are reviewed or consciously deferred."
    if day_status == "blocked":
        return "Ignore secondary polish until the main block is named and one step is chosen."
    return ""


def _build_residue_ledger(
    day_status: str,
    gate_text: str,
    skill_work_tail: List[str],
    evidence_tail: List[str],
) -> Dict[str, str]:
    """At most one short string per bucket (bounded)."""
    out: Dict[str, str] = {
        "must_resume": "",
        "safe_to_drop": "",
        "blocked": "",
        "watch_later": "",
    }
    lower = gate_text.lower()
    if day_status == "blocked":
        out["blocked"] = "Day marked blocked — start tomorrow with one unblock attempt."
    if skill_work_tail and day_status != "blocked":
        out["must_resume"] = skill_work_tail[-1][:120]
    if evidence_tail and day_status == "finished_well":
        out["safe_to_drop"] = "Polish and low-stretch items can wait if top action matters more."
    if "candidate" in lower:
        out["watch_later"] = "Ideas that compete with gate work — park until gate is clear."
    return out


def _gate_suggestions_structured(suggest: bool) -> List[GateSuggestionEntry]:
    if not suggest:
        return []
    return [
        {
            "item": "Review identity-relevant signals for recursion-gate.md",
            "reason": "End-of-day hint only; dream does not stage or merge.",
            "urgency": "normal",
        }
    ]


def _build_weekly_reflection(
    *,
    user: str,
    day_iso: str,
    one_signal: str,
    day_status: str,
    stop_condition: str,
    mode: str,
) -> Dict[str, Any]:
    return {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "user": user,
        "weekAnchorDate": day_iso,
        "mode": mode,
        "strongestRecurringSignal": one_signal[:240],
        "repeatedBlocker": day_status if day_status == "blocked" else "",
        "recurringStopConditionFailure": "",
        "themeWorthReviewing": one_signal[:120] if mode == "reflective" else "",
        "candidateCadenceAdjustment": "If blocked days repeat, consider shorter dream mode or earlier gate triage.",
    }


def _append_or_write_memory(memory_path: Path, block: str) -> None:
    marker = "## Good night closeout (generated)"
    existing = _read_text(memory_path)
    if marker in existing:
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
    tomorrow_top_action, top_action_reason = _top_action_and_reason(gate)
    energy_fit = _tomorrow_energy_fit(args.mode)
    stop_condition = _build_stop_condition(day_status, energy_fit)
    reset_cue = _build_reset_cue(args.mode)
    quiet_run = _quiet_run(one_signal, skill_work_tail, evidence_tail, day_status)
    active_lane = _active_lane_hint(skill_work_tail, evidence_tail, gate)
    ignore_tomorrow = _ignore_tomorrow(gate, day_status)
    residue_ledger = _build_residue_ledger(day_status, gate, skill_work_tail, evidence_tail)
    gate_suggestions = _gate_suggestions_structured(args.suggest_gate)

    payload: Dict[str, Any] = {
        "handoffSchemaVersion": HANDOFF_SCHEMA_VERSION,
        "user": args.user,
        "date": date.today().isoformat(),
        "mode": args.mode,
        "dayStatus": day_status,
        "oneSignal": one_signal,
        "tomorrowTopAction": tomorrow_top_action,
        "topActionReason": top_action_reason,
        "stopCondition": stop_condition,
        "optionalResetCue": reset_cue,
        "tomorrowEnergyFit": energy_fit,
        "quietRun": quiet_run,
        "activeLaneHint": active_lane,
        "ignoreTomorrow": ignore_tomorrow,
        "residueLedger": residue_ledger,
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
            f"- handoffSchemaVersion: {HANDOFF_SCHEMA_VERSION}\n"
            f"- day_status: {day_status}\n"
            f"- one_signal: {one_signal}\n"
            f"- tomorrow_top_action: {tomorrow_top_action}\n"
            f"- top_action_reason: {top_action_reason}\n"
            f"- stop_condition: {stop_condition}\n"
            f"- optional_reset_cue: {reset_cue}\n"
            f"- quiet_run: {quiet_run}\n"
        )
        _append_or_write_memory(memory_path, generated)
        handoff_dir.mkdir(parents=True, exist_ok=True)
        handoff_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

        if args.mode == "reflective":
            weekly_path = handoff_dir / "weekly-reflection.json"
            weekly_path.write_text(
                json.dumps(
                    _build_weekly_reflection(
                        user=args.user,
                        day_iso=payload["date"],
                        one_signal=one_signal,
                        day_status=day_status,
                        stop_condition=stop_condition,
                        mode=args.mode,
                    ),
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

    if args.emit_json:
        print(json.dumps(payload, indent=2))
        return 0

    lines = [
        "### Good night closeout",
        f"- Day status: {day_status}",
        f"- One signal: {one_signal}",
        f"- Tomorrow top action: {tomorrow_top_action}",
        f"- Why this action: {top_action_reason}",
        f"- Stop condition: {stop_condition}",
        f"- Optional reset cue: {reset_cue}",
        f"- Energy fit (tomorrow): {energy_fit}",
        f"- Quiet run: {quiet_run}",
        f"- Lane hint: {active_lane}",
    ]
    if ignore_tomorrow:
        lines.append(f"- Ignore tomorrow: {ignore_tomorrow}")
    if any(residue_ledger.values()):
        lines.append(f"- Residue ledger: { {k: v for k, v in residue_ledger.items() if v} }")
    if gate_suggestions:
        g0 = gate_suggestions[0]
        if isinstance(g0, dict):
            lines.append(f"- Gate suggestion: {g0.get('item', '')} ({g0.get('urgency', '')})")
        else:
            lines.append(f"- Gate suggestion: {g0}")
    if args.write_closeout:
        lines.append(f"- Handoff written: {handoff_path}")
        if args.mode == "reflective":
            lines.append(f"- Weekly reflection written: {handoff_dir / 'weekly-reflection.json'}")
    if payload["warnings"]:
        for warning in payload["warnings"]:
            lines.append(f"- Warning: {warning}")

    print("\n".join(lines[: max(args.max_lines, 1)]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
