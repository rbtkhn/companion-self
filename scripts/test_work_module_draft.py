#!/usr/bin/env python3
"""Tests for work_module_draft helper."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest


def _load_module():
    script_path = Path(__file__).with_name("work_module_draft.py")
    spec = importlib.util.spec_from_file_location("work_module_draft", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load work_module_draft.py for testing.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class WorkModuleDraftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load_module()

    def test_build_draft_uses_style_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            user_dir = Path(tmp)
            (user_dir / "self-knowledge.md").write_text("- • dragons are reptiles\n", encoding="utf-8")
            (user_dir / "self-curiosity.md").write_text("- • why dragons feel magical\n", encoding="utf-8")
            (user_dir / "self-personality.md").write_text("- • playful, likes short answers\n", encoding="utf-8")
            (user_dir / "self-skill-write.md").write_text("short expressive style", encoding="utf-8")

            result = self.mod.build_work_module_draft(user_dir, "work-business", "Draft a client update")
            self.assertIn("work-business", result["draft"])
            self.assertIn("Suggestion:", result["draft"])
            self.assertIn("playful", result["voiceStyle"])

    def test_build_draft_handles_missing_inputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            user_dir = Path(tmp)
            result = self.mod.build_work_module_draft(user_dir, "work-dev", "Draft release note")
            self.assertIn("work-dev", result["draft"])
            self.assertIn("3-5 lines", result["draft"])


if __name__ == "__main__":
    unittest.main()

