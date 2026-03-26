#!/usr/bin/env python3
"""Generate style-shaped drafts for work modules."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Dict

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from write_style_bridge import build_write_bridge, extract_edge_bullets, extract_personality_bridge


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def build_work_module_draft(user_dir: Path, module_name: str, task: str) -> Dict[str, str]:
    knowledge_text = _read_text(user_dir / "self-knowledge.md")
    curiosity_text = _read_text(user_dir / "self-curiosity.md")
    personality_text = _read_text(user_dir / "self-personality.md")
    write_text = _read_text(user_dir / "self-skill-write.md")

    knowledge = extract_edge_bullets(knowledge_text)
    curiosity = extract_edge_bullets(curiosity_text)
    personality = extract_personality_bridge(personality_text)
    write_bridge = build_write_bridge(
        {"knowledgeEdge": knowledge["edge"], "parseConfidence": knowledge["parseConfidence"]},
        {"curiosityEdge": curiosity["edge"], "parseConfidence": curiosity["parseConfidence"]},
        personality,
        write_text,
    )

    draft = (
        f"[{module_name}] {task}\n"
        f"Style: {write_bridge['styleProfile']['structure']} / {write_bridge['styleProfile']['sentenceLength']} sentences.\n"
        f"Suggestion: {write_bridge['suggestedWriteAction']}\n"
    )
    return {
        "module": module_name,
        "task": task,
        "voiceStyle": write_bridge["voiceStyle"],
        "styleProfile": write_bridge["styleProfile"],
        "draft": draft,
        "parseConfidence": write_bridge["parseConfidence"],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate style-shaped work module draft text.")
    ap.add_argument("--user", required=True, help="User id under users/<id>")
    ap.add_argument("--module", required=True, help="Work module name (e.g. work-business)")
    ap.add_argument("--task", required=True, help="Draft purpose/task")
    ap.add_argument("--emit-json", action="store_true")
    args = ap.parse_args()

    repo_root = Path.cwd()
    user_dir = repo_root / "users" / args.user
    if not user_dir.exists():
        print(f"Missing instance path: {user_dir}", file=sys.stderr)
        return 2

    payload = build_work_module_draft(user_dir, args.module, args.task)
    if args.emit_json:
        print(json.dumps(payload, indent=2))
    else:
        print(payload["draft"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

