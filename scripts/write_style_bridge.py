#!/usr/bin/env python3
"""Reusable WRITE style bridge for work modules."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def extract_edge_bullets(text: str) -> Dict[str, str]:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    bullets = []
    for line in lines:
        if line.startswith("- "):
            cleaned = line[2:].strip()
            if cleaned.startswith("•"):
                cleaned = cleaned[1:].strip()
            if cleaned and not cleaned.startswith("(e.g.") and cleaned != "•":
                bullets.append(cleaned)
    edge = "; ".join(bullets[-2:])[:220] if bullets else ""
    return {"edge": edge, "parseConfidence": "high" if edge else "none"}


def extract_personality_bridge(personality_text: str) -> Dict[str, str]:
    text = personality_text.lower()
    return {
        "workStyle": "analytical" if "analytical" in text else "playful" if "playful" in text else "neutral",
        "tonePreference": "calm" if "calm" in text else "playful" if "playful" in text else "direct",
        "pacePreference": "short_bursts" if "short" in text else "deep_focus" if "deep" in text else "standard",
        "parseConfidence": "high" if text.strip() else "none",
    }


def extract_style_profile(self_skill_write_text: str, personality_bridge: Dict[str, str]) -> Dict[str, str]:
    text = self_skill_write_text.lower()
    style = personality_bridge.get("workStyle", "neutral")
    tone = personality_bridge.get("tonePreference", "direct")
    pace = personality_bridge.get("pacePreference", "standard")
    sentence_length = "medium"
    structure = "simple_paragraph"
    dos = "Use concrete details."
    donts = "Avoid overlong output."

    if "short" in text or "simple" in text or pace == "short_bursts":
        sentence_length = "short"
    elif "complex" in text or "extended" in text or pace == "deep_focus":
        sentence_length = "long"

    if style == "analytical":
        structure = "point_reason_example"
        dos = "Lead with claim, then reason, then example."
        donts = "Avoid vague emotional phrasing without evidence."
    elif style == "playful":
        structure = "narrative_with_hook"
        dos = "Use one vivid image or playful line."
        donts = "Avoid flat corporate phrasing."

    confidence = "medium" if self_skill_write_text.strip() else "low"
    return {
        "style": style,
        "tone": tone,
        "pace": pace,
        "sentenceLength": sentence_length,
        "structure": structure,
        "dos": dos,
        "donts": donts,
        "parseConfidence": confidence,
    }


def build_write_bridge(
    knowledge_bridge: Dict[str, str],
    curiosity_bridge: Dict[str, str],
    personality_bridge: Dict[str, str],
    self_skill_write_text: str,
) -> Dict[str, str]:
    knowledge_seed = knowledge_bridge.get("knowledgeEdge", "")
    curiosity_seed = curiosity_bridge.get("curiosityEdge", "")
    profile = extract_style_profile(self_skill_write_text, personality_bridge)

    high_count = 0
    for bridge in (knowledge_bridge, curiosity_bridge, personality_bridge):
        if bridge.get("parseConfidence") == "high":
            high_count += 1
    parse_confidence = "high" if high_count >= 2 else "medium" if high_count == 1 else "low"

    if not (knowledge_seed or curiosity_seed):
        suggested = "Write 3-5 lines about today's top action in your own words."
        parse_confidence = "none"
    else:
        topic = curiosity_seed or knowledge_seed
        anchor = knowledge_seed if knowledge_seed else topic
        suggested = (
            f"Write a short note about '{topic}' using {profile['tone']} tone and {profile['pace'].replace('_', ' ')} pacing; "
            f"include one concrete fact from '{anchor}'."
        )
    if profile["style"] == "playful":
        suggested += " Keep one playful phrase."
    elif profile["style"] == "analytical":
        suggested += " Keep structure: point, reason, example."

    return {
        "knowledgeSeed": knowledge_seed,
        "curiositySeed": curiosity_seed,
        "voiceStyle": f"{profile['style']}/{profile['tone']}/{profile['pace']}",
        "styleProfile": profile,
        "suggestedWriteAction": suggested,
        "parseConfidence": parse_confidence,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Emit write-style profile for work modules.")
    ap.add_argument("--user-dir", required=True, help="Path to users/<id> directory")
    ap.add_argument("--emit-json", action="store_true")
    args = ap.parse_args()

    user_dir = Path(args.user_dir)
    write_text = _read_text(user_dir / "self-skill-write.md")
    personality_text = _read_text(user_dir / "self-personality.md")
    personality_bridge = extract_personality_bridge(personality_text)
    payload = extract_style_profile(write_text, personality_bridge)
    if args.emit_json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"style={payload['style']} tone={payload['tone']} pace={payload['pace']} structure={payload['structure']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

