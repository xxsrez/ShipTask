from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS = ROOT / "docs" / "skills" / "task-composer" / "requirements.md"
ARCHITECTURE = ROOT / "docs" / "skills" / "task-composer" / "architecture.md"
SKILL = ROOT / "task-composer" / "SKILL.md"
EVALUATION = ROOT / "docs" / "skills" / "task-composer" / "evaluation.md"


class TaskComposerStrategyContractTest(unittest.TestCase):
    def test_three_roles_are_compiled_without_hidden_obligations(self) -> None:
        combined = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (REQUIREMENTS, ARCHITECTURE, SKILL, EVALUATION)
        )
        compact = " ".join(combined.split())
        for marker in (
            "Strategic Outcome",
            "Human Requirements",
            "Agent Plan",
            "не создаёт новое Human Requirement",
            "не создаёт новую задолженность",
            "не выданы за Human Requirement",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, compact)

    def test_strategy_and_formal_obligation_have_separate_trace(self) -> None:
        architecture = ARCHITECTURE.read_text(encoding="utf-8")
        self.assertIn("Strategic Outcome → вклад Tasks и направление решений", architecture)
        self.assertIn(
            "Human Requirement → Task/plan element → acceptance → expected evidence",
            architecture,
        )


if __name__ == "__main__":
    unittest.main()
