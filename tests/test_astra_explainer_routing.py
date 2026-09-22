from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AstraExplainerRoutingTest(unittest.TestCase):
    def test_automatic_publication_surfaces_have_astra_native_guard(self) -> None:
        surfaces = (
            ROOT / "issue-grinder" / "SKILL.md",
            ROOT / "issue-grinder" / "references" / "strategic-explainer.md",
            ROOT / "task-composer" / "SKILL.md",
            ROOT / "scope-reviewer" / "SKILL.md",
        )
        for path in surfaces:
            text = re.sub(r"\s+", " ", path.read_text(encoding="utf-8"))
            with self.subTest(path=path):
                self.assertIn("gpt-6-astra", text)
                self.assertIn("native", text)
                self.assertRegex(text, r"Astra[^.]{0,180}(?:не вызывает|не вызывай|без вызова)")

    def test_generic_skill_keeps_explicit_direct_request_exception(self) -> None:
        skill = (ROOT / "strategic-explainer" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        compact = re.sub(r"\s+", " ", skill)
        self.assertIn("автоматической или delegated publication unit", compact)
        self.assertIn("Явный прямой пользовательский запрос", compact)
        self.assertIn("$strategic-explainer:strategic-explainer", compact)


if __name__ == "__main__":
    unittest.main()
