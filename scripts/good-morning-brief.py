#!/usr/bin/env python3
"""
good-morning-brief.py
Daily startup brief with optional sync checks and good-night handoff wiring.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from write_style_bridge import build_write_bridge


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


def _session_options(mode: str, personality_bridge: Dict[str, str]) -> List[Dict[str, str]]:
    base = [
        {"label": "Deep Work", "reason": "Focus on one difficult task end-to-end."},
        {"label": "Analyst Mode", "reason": "Review signals and synthesize next actions."},
    ]
    if mode != "minimal":
        base.append({"label": "Light Review + Capture", "reason": "Close loops and stage signals safely."})
    if personality_bridge.get("pacePreference") == "short_bursts":
        base = [
            {"label": "Light Review + Capture", "reason": "Use short loops and frequent closure."},
            {"label": "Deep Work", "reason": "Do one short, scoped push only."},
            {"label": "Analyst Mode", "reason": "Clarify next action when energy is limited."},
        ]
    elif personality_bridge.get("workStyle") == "analytical":
        base = [
            {"label": "Analyst Mode", "reason": "Start with a clear frame and decision path."},
            {"label": "Deep Work", "reason": "Execute the highest-leverage action after framing."},
            {"label": "Light Review + Capture", "reason": "Close loops and keep evidence current."},
        ]
    return base


def _format_gate_suggestion_entry(entry: Any) -> str:
    if isinstance(entry, dict):
        parts = [str(entry.get("item", "")), str(entry.get("reason", ""))]
        return " — ".join(p for p in parts if p)
    return str(entry)


def _build_snapshot(
    night_handoff: Dict[str, Any],
    evidence_tail: List[str],
    curiosity_tail: List[str],
) -> List[str]:
    snapshot: List[str] = []
    if night_handoff:
        if night_handoff.get("quietRun"):
            snapshot.append(
                "Last night was a quiet dream closeout — keep today's scope small unless something urgent surfaced."
            )
        action = night_handoff.get("tomorrowTopAction", "")
        reason = night_handoff.get("topActionReason", "")
        signal = night_handoff.get("oneSignal", "")
        if action:
            snapshot.append(f"Carry-forward action from last night: {action}")
        if reason:
            snapshot.append(f"Why that action: {reason}")
        if signal:
            snapshot.append(f"Last-night signal: {signal}")
        wt_state = night_handoff.get("worktreeState")
        wt_adv = night_handoff.get("worktreeAdvice")
        if wt_state:
            snapshot.append(f"Worktree ({wt_state}): {wt_adv}")
        ignore = night_handoff.get("ignoreTomorrow", "")
        if ignore:
            snapshot.append(f"Ignore tomorrow: {ignore}")
        lane = night_handoff.get("activeLaneHint")
        if lane and str(lane).upper() != "NONE":
            snapshot.append(f"Lane hint: foreground {lane} after the top action.")
        ledger = night_handoff.get("residueLedger") or {}
        if isinstance(ledger, dict):
            non_empty = {k: v for k, v in ledger.items() if v}
            if non_empty:
                parts = [f"{k}: {str(v)[:80]}" for k, v in list(non_empty.items())[:4]]
                snapshot.append("Residue (capped): " + "; ".join(parts))
        gs = night_handoff.get("gateSuggestions") or []
        if gs:
            snapshot.append(f"Gate hint: {_format_gate_suggestion_entry(gs[0])[:220]}")
    if evidence_tail:
        snapshot.append(f"Recent evidence: {evidence_tail[-1][:180]}")
    if curiosity_tail:
        snapshot.append(f"Curiosity spark: {curiosity_tail[-1][:180]}")
    if not snapshot:
        snapshot.append("No recent context found; start with one small, high-confidence action.")
    return snapshot[:8]


def _git_quick_context(repo_root: Path) -> Dict[str, Any]:
    """Single-pass git snapshot for coffee orientation (read-only)."""
    st = subprocess.run(
        ["git", "status", "-sb"],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
        check=False,
    )
    br = subprocess.run(
        ["git", "branch", "-vv"],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
        check=False,
    )
    hd = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
        check=False,
    )
    status_out = (st.stdout or "").strip()
    branch_out = br.stdout or ""
    head = (hd.stdout or "").strip() or "unknown"
    body = [ln for ln in status_out.splitlines() if ln.strip() and not ln.startswith("## ")]
    dirty = len(body) > 0
    non_main = [
        line.strip()
        for line in branch_out.splitlines()
        if line.strip()
        and not line.strip().startswith("* main")
        and not line.strip().startswith("main ")
    ]
    return {
        "gitHeadShort": head,
        "worktreeDirty": dirty,
        "nonMainBranchCount": len(non_main),
        "statusLine": status_out.splitlines()[0] if status_out else "",
    }


def _read_coffee_runner_context(path: Path | None) -> Dict[str, Any]:
    if path is None or not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _coffee_orientation_hints(
    *,
    handoff: Dict[str, Any],
    gate_text: str,
    check_sync: bool,
    git_ctx: Dict[str, Any],
    runner_ctx: Dict[str, Any],
    top_execution_action: str,
) -> Dict[str, str]:
    """Bounded orientation block for coffee (not dream/bridge)."""
    gtl = gate_text.lower()
    has_candidates = "candidate" in gtl or "## candidates" in gtl
    non_main = int(git_ctx.get("nonMainBranchCount") or 0)
    dirty = bool(git_ctx.get("worktreeDirty"))
    branch_class = str(
        runner_ctx.get("branchHygieneClass") or git_ctx.get("branchHygieneClass") or ""
    ).strip()
    if not branch_class:
        if non_main > 4 or (dirty and len(str(git_ctx.get("statusLine", ""))) > 120):
            branch_class = "risky"
        elif non_main > 0 or dirty:
            branch_class = "watch"
        else:
            branch_class = "clean"

    strong_handoff = bool(
        handoff.get("tomorrowTopAction")
        and handoff.get("topActionReason")
        and not handoff.get("quietRun")
    )
    has_handoff = bool(handoff.get("tomorrowTopAction") or handoff.get("oneSignal"))

    if has_handoff and handoff.get("tomorrowTopAction"):
        diagnosis = "handoff_pickup"
    elif has_candidates:
        diagnosis = "gate_uncertainty"
    elif branch_class == "risky" or non_main > 2:
        diagnosis = "branch_drift"
    elif dirty:
        diagnosis = "execution_restart"
    else:
        diagnosis = "routine_sip"

    best = (top_execution_action or "").strip()
    if len(best) > 220:
        best = best[:217] + "…"

    friction_parts: List[str] = []
    wt = str(handoff.get("worktreeState") or "").lower()
    if "risky" in wt:
        friction_parts.append("risky worktree residue from dream")
    if has_candidates:
        friction_parts.append("unresolved gate surface")
    if non_main > 3:
        friction_parts.append("many open branches")
    if strong_handoff:
        friction_parts.append("strong carry-forward — ambiguity if you skip it")
    if check_sync and not friction_parts:
        friction_parts.append("sync checks ran — watch template drift if you pull")
    likely_friction = (
        "; ".join(friction_parts)
        if friction_parts
        else "low if you hold one lane until the top action is done"
    )[:240]

    do_not: List[str] = [
        "Do not stage or merge from this brief — gate stays companion-controlled.",
    ]
    if strong_handoff:
        do_not.append("Do not open a second lane before addressing last night's carry-forward.")
    if has_candidates:
        do_not.append("Do not add new gate candidates during orientation unless the signal is clearly identity-relevant.")
    if not has_handoff and has_candidates:
        do_not.append("Do not start deep execution before scanning pending candidates.")
    do_not_s = " ".join(do_not)[:320]

    return {
        "sipDiagnosis": diagnosis,
        "bestNextMove": best or "Pick one small execution step from your self-work plan.",
        "likelyFriction": likely_friction,
        "doNotStartWith": do_not_s,
        "branchHygieneClass": branch_class,
    }


def _apply_residue_session_options(
    options: List[Dict[str, str]],
    handoff: Dict[str, Any],
    mode: str,
) -> List[Dict[str, str]]:
    """When carry-forward is strong, de-emphasize light review (template default)."""
    if mode == "minimal":
        return options
    strong = bool(
        handoff.get("tomorrowTopAction")
        and handoff.get("topActionReason")
        and not handoff.get("quietRun")
    )
    if not strong:
        return options
    out: List[Dict[str, str]] = []
    rest: List[Dict[str, str]] = []
    for opt in options:
        label = opt.get("label", "")
        if label == "Light Review + Capture":
            rest.append(opt)
        else:
            out.append(opt)
    return out + rest


def _apply_coffee_lane(
    options: List[Dict[str, str]],
    lane: str,
) -> List[Dict[str, str]]:
    lane_l = (lane or "").strip().lower()
    if not lane_l or lane_l in ("none", "default"):
        return options
    priority = {
        "write": ("Deep Work", "WRITE"),
        "gate": ("Analyst Mode", "GATE"),
        "build": ("Deep Work", "BUILD"),
        "research": ("Analyst Mode", "RESEARCH"),
    }
    if lane_l not in priority:
        return options
    prefer_label, tag = priority[lane_l]
    front = [o for o in options if o.get("label") == prefer_label]
    others = [o for o in options if o.get("label") != prefer_label]
    tagged = list(front + others)
    if tagged:
        tagged[0] = {
            **tagged[0],
            "reason": f"{tagged[0].get('reason', '')} (lane={tag})".strip(),
        }
    return tagged


def _write_morning_checkback(
    handoff_dir: Path,
    *,
    morning_date: str,
    handoff_date: str,
    helpful: str,
    outcome: str,
) -> Path:
    handoff_dir.mkdir(parents=True, exist_ok=True)
    path = handoff_dir / f"morning-checkback-{morning_date}.json"
    payload = {
        "morningDate": morning_date,
        "referencesHandoffDate": handoff_date,
        "handoffWasHelpful": helpful,
        "yesterdayTopActionOutcome": outcome or "unknown",
        "generated_by": "good-morning-brief.py",
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def _extract_objective_id(text: str) -> str:
    match = re.search(r"\b(?:LO-\d{2}|[A-Z]{2,}-\d{2,})\b", text)
    return match.group(0) if match else ""


def _extract_knowledge_edge(knowledge_text: str) -> Dict[str, str]:
    lines = [ln.strip() for ln in knowledge_text.splitlines()]
    if not lines:
        return {"knowledgeEdge": "", "knowledgeObjectiveId": "", "parseConfidence": "none"}

    preferred_sections = ("topics / understanding", "facts entering awareness", "open", "next", "edge")
    section_idx = -1
    for idx, line in enumerate(lines):
        low = line.lower()
        if low.startswith("## ") and any(tag in low for tag in preferred_sections):
            section_idx = idx
            break

    candidates: List[str] = []
    confidence = "low"
    if section_idx >= 0:
        confidence = "high"
        for line in lines[section_idx + 1 :]:
            if line.startswith("## "):
                break
            if line.startswith("- "):
                cleaned = line[2:].strip()
                if cleaned.startswith("•"):
                    cleaned = cleaned[1:].strip()
                if cleaned and not cleaned.startswith("(e.g.") and cleaned != "•":
                    candidates.append(cleaned)
    else:
        for line in lines:
            if line.startswith("- "):
                cleaned = line[2:].strip()
                if cleaned.startswith("•"):
                    cleaned = cleaned[1:].strip()
                if cleaned and not cleaned.startswith("(e.g.") and cleaned != "•":
                    candidates.append(cleaned)

    edge = "; ".join(candidates[-2:])[:220] if candidates else ""
    objective_id = _extract_objective_id(edge) or _extract_objective_id(knowledge_text)
    if edge and confidence != "high":
        confidence = "medium"

    return {
        "knowledgeEdge": edge,
        "knowledgeObjectiveId": objective_id,
        "parseConfidence": confidence if edge else "none",
    }


def _extract_personality_bridge(personality_text: str) -> Dict[str, str]:
    text = personality_text.lower()
    if not text.strip():
        return {
            "workStyle": "neutral",
            "pacePreference": "standard",
            "tonePreference": "direct",
            "parseConfidence": "none",
        }

    work_style = "neutral"
    if any(token in text for token in ("analytical", "systematic", "structured")):
        work_style = "analytical"
    elif any(token in text for token in ("playful", "creative", "story")):
        work_style = "playful"

    pace = "standard"
    if any(token in text for token in ("short answers", "short", "quick", "brief")):
        pace = "short_bursts"
    elif any(token in text for token in ("deep", "long", "extended")):
        pace = "deep_focus"

    tone = "direct"
    if any(token in text for token in ("calm", "gentle", "kind")):
        tone = "calm"
    elif any(token in text for token in ("playful", "fun")):
        tone = "playful"

    confidence = "medium"
    if any(line.strip().startswith("- •") for line in personality_text.splitlines()):
        confidence = "high"

    return {
        "workStyle": work_style,
        "pacePreference": pace,
        "tonePreference": tone,
        "parseConfidence": confidence,
    }


def _extract_curiosity_bridge(curiosity_text: str) -> Dict[str, str]:
    lines = [ln.strip() for ln in curiosity_text.splitlines()]
    if not lines:
        return {"curiosityEdge": "", "curiosityObjectiveId": "", "parseConfidence": "none"}

    preferred_sections = ("questions / open curiosity", "interests", "open", "curiosity")
    section_idx = -1
    for idx, line in enumerate(lines):
        low = line.lower()
        if low.startswith("## ") and any(tag in low for tag in preferred_sections):
            section_idx = idx
            break

    candidates: List[str] = []
    confidence = "low"
    scan_lines = lines[section_idx + 1 :] if section_idx >= 0 else lines
    if section_idx >= 0:
        confidence = "high"
    for line in scan_lines:
        if line.startswith("## "):
            break
        if line.startswith("- "):
            cleaned = line[2:].strip()
            if cleaned.startswith("•"):
                cleaned = cleaned[1:].strip()
            if cleaned and not cleaned.startswith("(e.g.") and cleaned != "•":
                candidates.append(cleaned)

    edge = "; ".join(candidates[-2:])[:220] if candidates else ""
    objective_id = _extract_objective_id(edge) or _extract_objective_id(curiosity_text)
    if edge and confidence != "high":
        confidence = "medium"
    return {
        "curiosityEdge": edge,
        "curiosityObjectiveId": objective_id,
        "parseConfidence": confidence if edge else "none",
    }


def _extract_library_bridge(library_text: str) -> Dict[str, str]:
    if not library_text.strip():
        return {
            "activeShelfTopic": "",
            "staleReferenceAlert": "self-library missing or empty.",
            "suggestedLookupAction": "Add one approved library entry before relying on lookup-first references.",
            "parseConfidence": "none",
        }

    lines = [ln.strip() for ln in library_text.splitlines()]
    yaml_lines: List[str] = []
    in_yaml = False
    for line in lines:
        if line.startswith("```yaml"):
            in_yaml = True
            continue
        if in_yaml and line.startswith("```"):
            break
        if in_yaml:
            yaml_lines.append(line)

    joined = "\n".join(yaml_lines) if yaml_lines else "\n".join(lines)
    has_entries = "entries:" in joined
    empty_entries = "entries: []" in joined

    topic = ""
    patterns = [
        r"title:\s*([^\n]+)",
        r"topic:\s*([^\n]+)",
        r"domain:\s*([^\n]+)",
    ]
    for pattern in patterns:
        matches = re.findall(pattern, joined, flags=re.IGNORECASE)
        if matches:
            topic = matches[-1].strip().strip("'\"")
            break

    if has_entries and not empty_entries and topic:
        return {
            "activeShelfTopic": topic,
            "staleReferenceAlert": "",
            "suggestedLookupAction": f"Use SELF-LIBRARY topic '{topic}' as today's lookup anchor.",
            "parseConfidence": "high",
        }
    if has_entries and empty_entries:
        return {
            "activeShelfTopic": "",
            "staleReferenceAlert": "SELF-LIBRARY has no entries yet.",
            "suggestedLookupAction": "Queue one lookup-first source candidate if today's work depends on external references.",
            "parseConfidence": "medium",
        }
    return {
        "activeShelfTopic": "",
        "staleReferenceAlert": "SELF-LIBRARY format not recognized for entry extraction.",
        "suggestedLookupAction": "Keep library advisory off until a valid entries block is present.",
        "parseConfidence": "low",
    }


def _infer_skill_focus(self_work_text: str, think_text: str, write_text: str, work_text: str) -> Dict[str, str]:
    upper = self_work_text.upper()
    focus = ""
    if "THINK" in upper:
        focus = "THINK"
    elif "WRITE" in upper:
        focus = "WRITE"
    elif "WORK" in upper:
        focus = "WORK"
    else:
        # Fallback heuristic: default toward WORK when a lane plan exists.
        focus = "WORK" if work_text.strip() else "THINK"

    source_map = {
        "THINK": think_text,
        "WRITE": write_text,
        "WORK": work_text,
    }
    source = source_map.get(focus, "")
    objective_id = _extract_objective_id(self_work_text) or _extract_objective_id(source)
    next_evidence_target = f"Capture one {focus} evidence line linked to today's top action."
    if not self_work_text.strip():
        next_evidence_target = (
            f"No self-work plan found; set top skill focus to {focus} and capture one evidence line."
        )

    return {
        "topSkillFocus": focus,
        "skillObjectiveId": objective_id,
        "nextEvidenceTarget": next_evidence_target,
    }


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
    ap.add_argument(
        "--write-checkback",
        action="store_true",
        help="Write morning-checkback-<today>.json (requires --checkback-helpful).",
    )
    ap.add_argument(
        "--checkback-helpful",
        choices=["yes", "no", "partial"],
        default=None,
        help="Whether last night's handoff was helpful (used with --write-checkback).",
    )
    ap.add_argument(
        "--checkback-outcome",
        default="",
        help="One line: outcome of yesterday's top action (optional).",
    )
    ap.add_argument(
        "--coffee-context-file",
        default="",
        help="JSON from cadence-coffee: deltaLines, branchHygieneClass, suggestedCoffeeMode, etc.",
    )
    ap.add_argument(
        "--coffee-lane",
        default="",
        help="Optional lane focus: write|gate|build|research|none",
    )
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
    knowledge_text = _read_text(user_dir / "self-knowledge.md")
    library_text = _read_text(user_dir / "self-library.md")
    self_work_text = _read_text(user_dir / "self-work.md")
    think_text = _read_text(user_dir / "self-skill-think.md")
    write_text = _read_text(user_dir / "self-skill-write.md")
    work_text = _read_text(user_dir / "self-skill-work.md")
    gate_text = _read_text(user_dir / "recursion-gate.md")
    handoff = _read_json(user_dir / "daily-handoff" / "night-handoff.json")
    coffee_ctx_path = (
        Path(args.coffee_context_file).expanduser()
        if (args.coffee_context_file or "").strip()
        else None
    )
    runner_ctx = _read_coffee_runner_context(coffee_ctx_path)
    git_ctx = _git_quick_context(repo_root)
    if runner_ctx.get("branchHygieneClass"):
        git_ctx["branchHygieneClass"] = runner_ctx["branchHygieneClass"]
    if runner_ctx.get("nonMainBranchCount") is not None:
        try:
            git_ctx["nonMainBranchCount"] = int(runner_ctx["nonMainBranchCount"])
        except (TypeError, ValueError):
            pass
    if runner_ctx.get("worktreeDirty") is not None:
        git_ctx["worktreeDirty"] = bool(runner_ctx["worktreeDirty"])

    if args.write_checkback and not args.checkback_helpful:
        print(
            "--write-checkback requires --checkback-helpful yes|no|partial",
            file=sys.stderr,
        )
        return 1

    # Boundary guard: self-memory is ephemeral continuity only.
    # Do not derive identity truth or write Record updates from memory content.
    warm_greeting = _greeting(personality_text)
    context_snapshot = _build_snapshot(handoff, _tail_lines(evidence_text, 12), _tail_lines(curiosity_text, 12))
    intention_prompt = "What is one thing you want to understand or create better today?"
    self_work_bridge = _infer_skill_focus(self_work_text, think_text, write_text, work_text)
    knowledge_edge = _extract_knowledge_edge(knowledge_text)
    personality_bridge = _extract_personality_bridge(personality_text)
    curiosity_bridge = _extract_curiosity_bridge(curiosity_text)
    library_bridge = _extract_library_bridge(library_text)
    write_bridge = build_write_bridge(knowledge_edge, curiosity_bridge, personality_bridge, write_text)

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
    top_action_reason = handoff.get("topActionReason", "") if handoff else ""
    top_execution_action = handoff.get(
        "tomorrowTopAction",
        f"Execute one scoped {self_work_bridge['topSkillFocus']} action from self-work plan.",
    )
    if not handoff and knowledge_edge["parseConfidence"] == "high" and knowledge_edge["knowledgeEdge"]:
        top_execution_action = (
            f"Advance knowledge edge: {knowledge_edge['knowledgeEdge']}"
        )
    if (
        not handoff
        and curiosity_bridge["parseConfidence"] == "high"
        and curiosity_bridge["curiosityEdge"]
        and "Advance knowledge edge:" not in top_execution_action
    ):
        top_execution_action = f"Explore curiosity edge: {curiosity_bridge['curiosityEdge']}"
    if personality_bridge["pacePreference"] == "short_bursts":
        top_execution_action = f"{top_execution_action} Keep scope to one short burst."
    if personality_bridge["tonePreference"] == "calm":
        top_execution_action = f"{top_execution_action} Use calm pacing."
    if library_bridge["parseConfidence"] == "high" and library_bridge["activeShelfTopic"]:
        top_sync_action = (
            f"{top_sync_action} Reference shelf anchor: {library_bridge['activeShelfTopic']}."
        )
    pre_write_execution = top_execution_action
    write_bridge_overrode = False
    if self_work_bridge["topSkillFocus"] == "WRITE" and write_bridge["parseConfidence"] in {"medium", "high"}:
        write_bridge_overrode = True
        top_execution_action = write_bridge["suggestedWriteAction"]

    context_snapshot = list(context_snapshot)
    if write_bridge_overrode and handoff.get("tomorrowTopAction"):
        context_snapshot.append(
            "Note: WRITE bridge replaced last night's carry-forward action; "
            "the handoff reason above still reflects dream's judgment."
        )
    context_snapshot = context_snapshot[:9]

    delta_lines = runner_ctx.get("deltaLines")
    if isinstance(delta_lines, list) and delta_lines:
        prefixed = [f"Since last coffee: {str(x)[:200]}" for x in delta_lines[:4]]
        context_snapshot = prefixed + list(context_snapshot)
        context_snapshot = context_snapshot[:12]

    coffee_hints = _coffee_orientation_hints(
        handoff=handoff,
        gate_text=gate_text,
        check_sync=bool(args.check_sync),
        git_ctx=git_ctx,
        runner_ctx=runner_ctx,
        top_execution_action=top_execution_action,
    )
    if runner_ctx.get("branchHygieneClass"):
        coffee_hints["branchHygieneClass"] = str(runner_ctx["branchHygieneClass"])
    if runner_ctx.get("recommendedBranchAction"):
        coffee_hints["recommendedBranchAction"] = str(runner_ctx["recommendedBranchAction"])
    brc = coffee_hints.get("branchHygieneClass", "")
    if brc and brc != "clean":
        coffee_hints["likelyFriction"] = (
            f"{coffee_hints['likelyFriction']} (branch hygiene: {brc})"
        )[:260]

    session_opts = _session_options(args.mode, personality_bridge)
    session_opts = _apply_residue_session_options(session_opts, handoff, args.mode)
    session_opts = _apply_coffee_lane(session_opts, args.coffee_lane)

    top_gate_action = "Review recursion-gate candidates before adding new identity-relevant claims." if "candidate" in gate_text.lower() else "Stage only if identity-relevant signal appears."

    payload: Dict[str, Any] = {
        "user": args.user,
        "date": date.today().isoformat(),
        "mode": args.mode,
        "warmGreeting": warm_greeting,
        "contextSnapshot": context_snapshot,
        "intentionPrompt": {"enabled": args.mode != "minimal", "prompt": intention_prompt},
        "syncSummary": sync_summary,
        "sessionOptions": session_opts,
        "selfWorkBridge": self_work_bridge,
        "knowledgeBridge": {
            "knowledgeEdge": knowledge_edge["knowledgeEdge"],
            "knowledgeObjectiveId": knowledge_edge["knowledgeObjectiveId"],
            "parseConfidence": knowledge_edge["parseConfidence"],
        },
        "curiosityBridge": {
            "curiosityEdge": curiosity_bridge["curiosityEdge"],
            "curiosityObjectiveId": curiosity_bridge["curiosityObjectiveId"],
            "parseConfidence": curiosity_bridge["parseConfidence"],
        },
        "personalityBridge": personality_bridge,
        "libraryBridge": library_bridge,
        "writeBridge": write_bridge,
        "dailyOpsHandoff": {
            "topSyncAction": top_sync_action,
            "topExecutionAction": top_execution_action,
            "topGateAction": top_gate_action,
            "topActionReasonFromHandoff": top_action_reason,
            "writeBridgeOverrodeHandoff": write_bridge_overrode,
            "handoffExecutionBeforeWriteBridge": pre_write_execution if write_bridge_overrode else None,
        },
        "coffeeOrientationHints": coffee_hints,
        "coffeeRunnerMeta": {
            k: runner_ctx[k]
            for k in (
                "suggestedCoffeeMode",
                "recommendedBranchAction",
                "branchHygieneClass",
                "deltaLines",
            )
            if runner_ctx.get(k) is not None
        },
        "warnings": [],
    }

    capture_gap_result: Dict[str, Any] = {}
    try:
        _scripts = str(Path(__file__).resolve().parent)
        if _scripts not in sys.path:
            sys.path.insert(0, _scripts)
        from detect_capture_gap import detect_gap, format_gap_one_liner
        capture_gap_result = detect_gap(args.user)
    except Exception:
        pass
    if capture_gap_result:
        payload["capture_gap"] = capture_gap_result

    session_load_result: Dict[str, Any] = {}
    try:
        from assess_session_load import assess_load, format_load_one_liner
        session_load_result = assess_load(args.user)
    except Exception:
        pass
    if session_load_result:
        payload["session_load"] = session_load_result

    if not memory_text:
        payload["warnings"].append("self-memory.md missing or empty.")
    else:
        payload["warnings"].append("self-memory used as ephemeral context only (no identity merge).")
    if not evidence_text:
        payload["warnings"].append("self-evidence.md missing or empty.")
    if not self_work_text:
        payload["warnings"].append("self-work.md missing or empty; used fallback skill-focus heuristic.")
    if knowledge_text and knowledge_edge["parseConfidence"] in {"none", "low"}:
        payload["warnings"].append("Knowledge wiring skipped due to low-confidence parse.")
    if curiosity_text and curiosity_bridge["parseConfidence"] in {"none", "low"}:
        payload["warnings"].append("Curiosity wiring skipped due to low-confidence parse.")
    if personality_text and personality_bridge["parseConfidence"] == "none":
        payload["warnings"].append("Personality wiring skipped due to low-confidence parse.")
    if library_bridge["staleReferenceAlert"]:
        payload["warnings"].append(library_bridge["staleReferenceAlert"])
    if write_bridge["parseConfidence"] == "low":
        payload["warnings"].append("WRITE synthesis has low confidence; using generic write suggestion.")
    if handoff:
        payload["warnings"].append("Good-night handoff detected and incorporated.")

    if args.write_intention:
        _write_intention(
            user_dir / "daily-intentions" / f"{date.today().isoformat()}.md",
            args.user,
            intention_prompt,
        )
        payload["warnings"].append("Daily intention note written (generated_by: good-morning-brief.py).")

    if args.write_checkback and args.checkback_helpful:
        hdate = str(handoff.get("date", "")) if handoff else ""
        ck_path = _write_morning_checkback(
            user_dir / "daily-handoff",
            morning_date=date.today().isoformat(),
            handoff_date=hdate or "unknown",
            helpful=args.checkback_helpful,
            outcome=args.checkback_outcome.strip(),
        )
        payload["warnings"].append(f"Morning checkback written: {ck_path.name} (not Record; operational telemetry).")

    if args.emit_json:
        print(json.dumps(payload, indent=2))
        return 0

    lines: List[str] = []
    lines.append("### Good morning brief")
    lines.append(f"- Greeting: {warm_greeting}")
    if runner_ctx.get("suggestedCoffeeMode"):
        lines.append(
            f"- Suggested next mode (optional): {runner_ctx['suggestedCoffeeMode']} — you chose {args.mode}."
        )
    lines.append("### Coffee orientation (capped)")
    lines.append(f"- Why this sip: {coffee_hints['sipDiagnosis']}")
    lines.append(f"- Best next move now: {coffee_hints['bestNextMove']}")
    lines.append(f"- Likely friction: {coffee_hints['likelyFriction']}")
    lines.append(f"- Do not start with: {coffee_hints['doNotStartWith']}")
    for item in context_snapshot:
        lines.append(f"- Context: {item}")
    if args.mode != "minimal":
        lines.append(f"- Intention prompt: {intention_prompt}")
    if args.check_sync:
        ta = sync_summary["templateAlignment"]
        lines.append(f"- Template alignment: {ta['status']} ({ta['upstreamRepo']} @ {ta['upstreamRef']})")
        lines.append(f"- work-dev sync: {sync_summary['workDev']['status']}")
        lines.append(f"- work-business sync: {sync_summary['workBusiness']['status']}")
    lines.append(f"- Top skill focus: {self_work_bridge['topSkillFocus']}")
    if self_work_bridge["skillObjectiveId"]:
        lines.append(f"- Skill objective id: {self_work_bridge['skillObjectiveId']}")
    lines.append(f"- Next evidence target: {self_work_bridge['nextEvidenceTarget']}")
    if knowledge_edge["knowledgeEdge"]:
        lines.append(f"- Knowledge edge: {knowledge_edge['knowledgeEdge']}")
    lines.append(f"- Knowledge parse confidence: {knowledge_edge['parseConfidence']}")
    if curiosity_bridge["curiosityEdge"]:
        lines.append(f"- Curiosity edge: {curiosity_bridge['curiosityEdge']}")
    lines.append(f"- Curiosity parse confidence: {curiosity_bridge['parseConfidence']}")
    lines.append(
        f"- Personality bridge: style={personality_bridge['workStyle']}, pace={personality_bridge['pacePreference']}, tone={personality_bridge['tonePreference']}"
    )
    if library_bridge["activeShelfTopic"]:
        lines.append(f"- Library shelf topic: {library_bridge['activeShelfTopic']}")
    lines.append(f"- Library parse confidence: {library_bridge['parseConfidence']}")
    lines.append(f"- Library lookup action: {library_bridge['suggestedLookupAction']}")
    lines.append(f"- Write bridge style: {write_bridge['voiceStyle']}")
    lines.append(f"- Write suggestion: {write_bridge['suggestedWriteAction']}")
    lines.append(f"- Top sync action: {top_sync_action}")
    if top_action_reason:
        lines.append(f"- Handoff top-action reason: {top_action_reason}")
    if write_bridge_overrode:
        lines.append(
            f"- WRITE bridge overrode handoff action (was: {pre_write_execution[:160]}{'…' if len(pre_write_execution) > 160 else ''})"
        )
    lines.append(f"- Top execution action: {top_execution_action}")
    lines.append(f"- Top gate action: {top_gate_action}")
    if capture_gap_result and capture_gap_result.get("level", "ok") not in ("ok", "unknown"):
        lines.append(f"- Capture gap: {format_gap_one_liner(capture_gap_result)}")
    if session_load_result:
        lines.append(f"- Session load: {format_load_one_liner(session_load_result)}")
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

