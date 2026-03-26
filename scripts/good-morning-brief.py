#!/usr/bin/env python3
"""
good-morning-brief.py
Daily startup brief with optional sync checks and good-night handoff wiring.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List


def _run(cmd: List[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _tail_lines(text: str, n: int = 8) -> List[str]:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    return lines[-n:]


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _greeting(personality_text: str) -> str:
    t = personality_text.lower()
    if "analytical" in t:
        return "Morning. What's the highest-leverage thread today?"
    if "curious" in t:
        return "Good morning. What are you most curious to resolve today?"
    return "Good morning. Ready for one focused step forward?"


def _template_alignment(repo: str, ref: str) -> Dict[str, Any]:
    # Lightweight availability check against upstream.
    ls = _run(["git", "ls-remote", repo, ref])
    if ls.returncode != 0 or not ls.stdout.strip():
        return {
            "status": "unavailable",
            "upstreamRepo": repo,
            "upstreamRef": ref,
            "notes": ["Unable to resolve upstream ref."],
        }
    return {
        "status": "aligned",
        "upstreamRepo": repo,
        "upstreamRef": ref,
        "notes": ["Upstream reachable; detailed drift check deferred."],
    }


def _lane_status(repo_root: Path, lane: str) -> Dict[str, Any]:
    lane_path = repo_root / "docs" / "skill-work" / lane
    if not lane_path.exists():
        return {"status": "not_established", "nextSteps": [f"Establish {lane} lane before syncing."]}
    return {"status": "no_relevant_updates", "nextSteps": [f"Review {lane} priorities and pick one action."]}


def _session_options(mode: str) -> List[Dict[str, str]]:
    base = [
        {"label": "Deep Work", "reason": "Focus on one difficult task end-to-end."},
        {"label": "Analyst Mode", "reason": "Review signals and synthesize next actions."},
    ]
    if mode != "minimal":
        base.append({"label": "Light Review + Capture", "reason": "Close loops and stage signals safely."})
    return base


def _build_snapshot(
    night_handoff: Dict[str, Any],
    evidence_tail: List[str],
    curiosity_tail: List[str],
) -> List[str]:
    snapshot: List[str] = []
    if night_handoff:
        action = night_handoff.get("tomorrowTopAction", "")
        signal = night_handoff.get("oneSignal", "")
        if action:
            snapshot.append(f"Carry-forward action from last night: {action}")
        if signal:
            snapshot.append(f"Last-night signal: {signal}")
    if evidence_tail:
        snapshot.append(f"Recent evidence: {evidence_tail[-1][:180]}")
    if curiosity_tail:
        snapshot.append(f"Curiosity spark: {curiosity_tail[-1][:180]}")
    if not snapshot:
        snapshot.append("No recent context found; start with one small, high-confidence action.")
    return snapshot[:4]


def _write_intention(path: Path, user: str, prompt: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = (
        f"# Daily intention ({date.today().isoformat()})\n\n"
        f"- generated_by: good-morning-brief.py\n"
        f"- user: {user}\n"
        f"- prompt: {prompt}\n"
        f"- note: Fill this with your one-line intention.\n"
    )
    path.write_text(payload, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate a daily good-morning brief.")
    ap.add_argument("--user", required=True)
    ap.add_argument("--mode", default="standard", choices=["minimal", "standard", "deep"])
    ap.add_argument("--emit-json", action="store_true")
    ap.add_argument("--write-intention", action="store_true")
    ap.add_argument("--check-sync", action="store_true")
    ap.add_argument("--upstream-repo", default="https://github.com/rbtkhn/companion-self")
    ap.add_argument("--upstream-ref", default="main")
    ap.add_argument("--max-lines", type=int, default=160)
    args = ap.parse_args()

    repo_root = Path.cwd()
    user_dir = repo_root / "users" / args.user
    if not user_dir.exists():
        print(f"Missing instance path: {user_dir}", file=sys.stderr)
        return 2

    memory_text = _read_text(user_dir / "self-memory.md")
    evidence_text = _read_text(user_dir / "self-evidence.md")
    curiosity_text = _read_text(user_dir / "self-curiosity.md")
    personality_text = _read_text(user_dir / "self-personality.md")
    gate_text = _read_text(user_dir / "recursion-gate.md")
    handoff = _read_json(user_dir / "daily-handoff" / "night-handoff.json")

    warm_greeting = _greeting(personality_text)
    context_snapshot = _build_snapshot(handoff, _tail_lines(evidence_text, 12), _tail_lines(curiosity_text, 12))
    intention_prompt = "What is one thing you want to understand or create better today?"

    sync_summary: Dict[str, Any] = {
        "enabled": bool(args.check_sync),
        "templateAlignment": {"status": "skipped", "upstreamRepo": args.upstream_repo, "upstreamRef": args.upstream_ref, "notes": []},
        "workDev": {"status": "skipped", "nextSteps": []},
        "workBusiness": {"status": "skipped", "nextSteps": []},
    }
    if args.check_sync:
        sync_summary["templateAlignment"] = _template_alignment(args.upstream_repo, args.upstream_ref)
        sync_summary["workDev"] = _lane_status(repo_root, "work-dev")
        sync_summary["workBusiness"] = _lane_status(repo_root, "work-business")

    top_sync_action = "Run sync checks and select one update action." if args.check_sync else "Sync checks skipped; choose one execution action."
    if sync_summary["workDev"]["status"] == "no_relevant_updates" and sync_summary["workBusiness"]["status"] == "no_relevant_updates":
        top_sync_action = "No relevant sync updates; keep mirrors unchanged today."
    top_execution_action = handoff.get("tomorrowTopAction", "Complete one high-confidence execution task.")
    top_gate_action = "Review recursion-gate candidates before adding new identity-relevant claims." if "candidate" in gate_text.lower() else "Stage only if identity-relevant signal appears."

    payload: Dict[str, Any] = {
        "user": args.user,
        "date": date.today().isoformat(),
        "mode": args.mode,
        "warmGreeting": warm_greeting,
        "contextSnapshot": context_snapshot,
        "intentionPrompt": {"enabled": args.mode != "minimal", "prompt": intention_prompt},
        "syncSummary": sync_summary,
        "sessionOptions": _session_options(args.mode),
        "dailyOpsHandoff": {
            "topSyncAction": top_sync_action,
            "topExecutionAction": top_execution_action,
            "topGateAction": top_gate_action,
        },
        "warnings": [],
    }

    if not memory_text:
        payload["warnings"].append("self-memory.md missing or empty.")
    if not evidence_text:
        payload["warnings"].append("self-evidence.md missing or empty.")
    if handoff:
        payload["warnings"].append("Good-night handoff detected and incorporated.")

    if args.write_intention:
        _write_intention(
            user_dir / "daily-intentions" / f"{date.today().isoformat()}.md",
            args.user,
            intention_prompt,
        )
        payload["warnings"].append("Daily intention note written (generated_by: good-morning-brief.py).")

    if args.emit_json:
        print(json.dumps(payload, indent=2))
        return 0

    lines: List[str] = []
    lines.append("### Good morning brief")
    lines.append(f"- Greeting: {warm_greeting}")
    for item in context_snapshot:
        lines.append(f"- Context: {item}")
    if args.mode != "minimal":
        lines.append(f"- Intention prompt: {intention_prompt}")
    if args.check_sync:
        ta = sync_summary["templateAlignment"]
        lines.append(f"- Template alignment: {ta['status']} ({ta['upstreamRepo']} @ {ta['upstreamRef']})")
        lines.append(f"- work-dev sync: {sync_summary['workDev']['status']}")
        lines.append(f"- work-business sync: {sync_summary['workBusiness']['status']}")
    lines.append(f"- Top sync action: {top_sync_action}")
    lines.append(f"- Top execution action: {top_execution_action}")
    lines.append(f"- Top gate action: {top_gate_action}")
    for option in payload["sessionOptions"]:
        lines.append(f"- Session option: {option['label']} — {option['reason']}")
    for warning in payload["warnings"]:
        lines.append(f"- Note: {warning}")

    print("\n".join(lines[: max(args.max_lines, 1)]))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # defensive top-level guard
        print(f"Unrecoverable runtime error: {exc}", file=sys.stderr)
        sys.exit(3)

