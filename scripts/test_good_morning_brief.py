#!/usr/bin/env python3
"""Unit tests for good-morning wiring helpers."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


def _load_module():
    script_path = Path(__file__).with_name("good-morning-brief.py")
    spec = importlib.util.spec_from_file_location("good_morning_brief", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load good-morning-brief.py for testing.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_write_style_module():
    script_path = Path(__file__).with_name("write_style_bridge.py")
    spec = importlib.util.spec_from_file_location("write_style_bridge", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load write_style_bridge.py for testing.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class KnowledgeEdgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load_module()

    def test_extract_high_confidence_from_topics_section(self):
        text = """# self-knowledge

## Topics / Understanding
- • dragons — seed

## Facts Entering Awareness
- • sky is blue — ACT-0001
"""
        result = self.mod._extract_knowledge_edge(text)  # pylint: disable=protected-access
        self.assertEqual(result["parseConfidence"], "high")
        self.assertIn("dragons", result["knowledgeEdge"])

    def test_filters_placeholder_bullets(self):
        text = """# self-knowledge

## Topics / Understanding
- •
- • (e.g. topic or concept — evidence id or source)
- • systems thinking — ACT-0009
"""
        result = self.mod._extract_knowledge_edge(text)  # pylint: disable=protected-access
        self.assertEqual(result["knowledgeEdge"], "systems thinking — ACT-0009")
        self.assertEqual(result["parseConfidence"], "high")

    def test_no_bullets_returns_none_confidence(self):
        text = """# self-knowledge

## Topics / Understanding
(Empty. Populated from approved activity.)
"""
        result = self.mod._extract_knowledge_edge(text)  # pylint: disable=protected-access
        self.assertEqual(result["knowledgeEdge"], "")
        self.assertEqual(result["parseConfidence"], "none")


class PersonalityBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load_module()

    def test_extracts_playful_short_preferences(self):
        text = """# self-personality

## Observed Voice / Expression
- • playful, likes short answers — seed
"""
        result = self.mod._extract_personality_bridge(text)  # pylint: disable=protected-access
        self.assertEqual(result["workStyle"], "playful")
        self.assertEqual(result["pacePreference"], "short_bursts")
        self.assertEqual(result["parseConfidence"], "high")

    def test_extracts_analytical_calm_preferences(self):
        text = """# self-personality

## Values / Preferences (Observed)
- • analytical and structured; calm tone
"""
        result = self.mod._extract_personality_bridge(text)  # pylint: disable=protected-access
        self.assertEqual(result["workStyle"], "analytical")
        self.assertEqual(result["tonePreference"], "calm")

    def test_empty_personality_returns_none_confidence(self):
        result = self.mod._extract_personality_bridge("")  # pylint: disable=protected-access
        self.assertEqual(result["parseConfidence"], "none")
        self.assertEqual(result["pacePreference"], "standard")


class CuriosityBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load_module()

    def test_extracts_high_confidence_curiosity_edge(self):
        text = """# self-curiosity

## Questions / Open Curiosity
- • Why do stories feel memorable?
- • I want to learn about dragons
"""
        result = self.mod._extract_curiosity_bridge(text)  # pylint: disable=protected-access
        self.assertEqual(result["parseConfidence"], "high")
        self.assertIn("dragons", result["curiosityEdge"])

    def test_curiosity_filters_placeholder_bullets(self):
        text = """# self-curiosity

## Interests
- •
- • (e.g. interest or theme)
- • drawing and stories — seed
"""
        result = self.mod._extract_curiosity_bridge(text)  # pylint: disable=protected-access
        self.assertEqual(result["curiosityEdge"], "drawing and stories — seed")
        self.assertEqual(result["parseConfidence"], "high")

    def test_empty_curiosity_returns_none_confidence(self):
        result = self.mod._extract_curiosity_bridge("")  # pylint: disable=protected-access
        self.assertEqual(result["parseConfidence"], "none")
        self.assertEqual(result["curiosityEdge"], "")


class LibraryBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load_module()

    def test_extracts_high_confidence_library_topic(self):
        text = """# SELF-LIBRARY

## Entries

```yaml
entries:
  - title: KY-4 polling notes
    domain: work-politics
```
"""
        result = self.mod._extract_library_bridge(text)  # pylint: disable=protected-access
        self.assertEqual(result["parseConfidence"], "high")
        self.assertIn("KY-4", result["activeShelfTopic"])

    def test_empty_entries_returns_medium_with_alert(self):
        text = """# SELF-LIBRARY

## Entries

```yaml
entries: []
```
"""
        result = self.mod._extract_library_bridge(text)  # pylint: disable=protected-access
        self.assertEqual(result["parseConfidence"], "medium")
        self.assertIn("no entries", result["staleReferenceAlert"].lower())

    def test_missing_library_returns_none(self):
        result = self.mod._extract_library_bridge("")  # pylint: disable=protected-access
        self.assertEqual(result["parseConfidence"], "none")
        self.assertTrue(result["suggestedLookupAction"])


class WriteBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load_write_style_module()

    def test_build_write_bridge_composes_three_inputs(self):
        knowledge = {"knowledgeEdge": "dragons are reptiles", "parseConfidence": "high"}
        curiosity = {"curiosityEdge": "why dragons feel magical", "parseConfidence": "high"}
        personality = {
            "workStyle": "playful",
            "tonePreference": "playful",
            "pacePreference": "short_bursts",
            "parseConfidence": "high",
        }
        result = self.mod.build_write_bridge(knowledge, curiosity, personality, "short expressive voice")
        self.assertEqual(result["parseConfidence"], "high")
        self.assertIn("why dragons feel magical", result["suggestedWriteAction"])
        self.assertIn("playful", result["voiceStyle"])
        self.assertIn("styleProfile", result)

    def test_build_write_bridge_fallback_when_no_seeds(self):
        knowledge = {"knowledgeEdge": "", "parseConfidence": "none"}
        curiosity = {"curiosityEdge": "", "parseConfidence": "none"}
        personality = {
            "workStyle": "neutral",
            "tonePreference": "direct",
            "pacePreference": "standard",
            "parseConfidence": "none",
        }
        result = self.mod.build_write_bridge(knowledge, curiosity, personality, "")
        self.assertEqual(result["parseConfidence"], "none")
        self.assertIn("3-5 lines", result["suggestedWriteAction"])


if __name__ == "__main__":
    unittest.main()

