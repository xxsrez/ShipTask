from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FAST = ROOT / "strategic-explainer-fast"
DOCS = ROOT / "docs" / "skills" / "strategic-explainer-fast"
SHARED_CASES = ROOT / "tests" / "strategic-explainer" / "cases"


class StrategicExplainerFastTest(unittest.TestCase):
    def test_runtime_is_complete_and_contains_no_subagent_invocation(self) -> None:
        skill = (FAST / "SKILL.md").read_text(encoding="utf-8")
        provider = (FAST / "references" / "in-context-contract.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("name: strategic-explainer-fast", skill)
        self.assertIn("Не создавай subagent", skill)
        self.assertIn("references/in-context-contract.md", skill)
        self.assertNotIn("fork_turns", skill + provider)
        self.assertNotIn("spawn_agent", skill + provider)

    def test_independent_source_package_has_all_requirements(self) -> None:
        requirements = (DOCS / "requirements.md").read_text(encoding="utf-8")
        architecture = (DOCS / "architecture.md").read_text(encoding="utf-8")

        for number in range(1, 17):
            self.assertIn(f"`SEF-{number:02d}`", requirements)
        self.assertIn("один publication unit", requirements)
        self.assertIn("не создаёт subagent", requirements)
        self.assertIn("Трассировка требований", architecture)

    def test_fast_reuses_exact_shared_portfolio(self) -> None:
        cases = [path for path in SHARED_CASES.iterdir() if path.is_dir()]
        self.assertEqual(len(cases), 20)
        for case in cases:
            with self.subTest(case=case.name):
                self.assertTrue((case / "facts.md").is_file())
                self.assertTrue((case / "rubric.md").is_file())

        protocol = (
            ROOT / "tests" / "strategic-explainer-fast" / "README.md"
        ).read_text(encoding="utf-8")
        self.assertIn("independent evaluator", protocol)
        self.assertIn("не создаёт subagent", protocol)
        self.assertIn("feasibility trial", protocol)


if __name__ == "__main__":
    unittest.main()

