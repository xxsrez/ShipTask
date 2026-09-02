from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "scope-reviewer" / "SKILL.md"
METADATA = ROOT / "scope-reviewer" / "agents" / "openai.yaml"
SCOPE = ROOT / "scope-reviewer" / "references" / "scope-and-review.md"
REPAIR = ROOT / "scope-reviewer" / "references" / "plan-improvement.md"
REPORTING = ROOT / "scope-reviewer" / "references" / "reporting.md"
REQUIREMENTS = ROOT / "docs" / "skills" / "scope-reviewer" / "requirements.md"
EVALUATION = ROOT / "docs" / "skills" / "scope-reviewer" / "evaluation.md"


def normalized(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


class ScopeReviewerContractTest(unittest.TestCase):
    def test_all_requirements_have_runtime_and_evaluation_trace(self) -> None:
        requirement_ids = re.findall(
            r"^### `((?:SR)-\d{2})`", REQUIREMENTS.read_text(encoding="utf-8"), re.M
        )
        self.assertEqual(requirement_ids, [f"SR-{number:02d}" for number in range(1, 13)])
        evaluation = EVALUATION.read_text(encoding="utf-8")
        for requirement_id in requirement_ids:
            with self.subTest(requirement_id=requirement_id):
                self.assertEqual(evaluation.count(f"| `{requirement_id}` |"), 1)

    def test_runtime_routes_progressively_and_preserves_authority(self) -> None:
        skill = SKILL.read_text(encoding="utf-8")
        self.assertIn("references/scope-and-review.md", skill)
        self.assertIn("references/plan-improvement.md", skill)
        self.assertIn("references/reporting.md", skill)
        self.assertIn("требует однозначного intent", skill)
        compact = normalized(skill)
        self.assertIn("Human Requirements не изменяй ни при каких обстоятельствах", compact)
        self.assertIn("**Release review** — всегда read-only", compact)
        self.assertIn("не меняет `Backlog`/рабочие статусы", skill)
        self.assertIn("Strategic Outcome", skill)
        self.assertIn("Стратегический gap не создаёт скрытую задолженность", skill)

    def test_each_optic_has_exact_luna_max_profile_and_clean_context(self) -> None:
        skill = SKILL.read_text(encoding="utf-8")
        scope = SCOPE.read_text(encoding="utf-8")
        for marker in (
            'fork_turns="none"',
            'model="gpt-5.6-luna"',
            'reasoning_effort="max"',
            "built-in `default` subagent",
            "SCOPE_REVIEWER_LENS_V1",
            "conversation history",
            "coverage gap",
        ):
            self.assertIn(marker, skill + scope)

    def test_plan_repair_fails_closed_on_requirements_boundary(self) -> None:
        repair = REPAIR.read_text(encoding="utf-8")
        compact = normalized(repair)
        for marker in (
            "byte-identical",
            "representation blocker",
            "optimistic concurrency",
            "Unknown outcome",
            "requirements-integrity failure",
            "Partial repair",
            "Readiness — оценка плана",
            "не превращён в Requirement, blocker или скрытую Task",
        ):
            self.assertIn(marker, compact)

    def test_reporting_is_one_composition_with_release_truth_boundaries(self) -> None:
        reporting = REPORTING.read_text(encoding="utf-8")
        compact = normalized(reporting)
        for marker in (
            "одна связная композиция",
            "$strategic-explainer:strategic-explainer",
            "explicit editing task",
            "не выбирает findings, repair, readiness, lifecycle",
            "фактически доказанный product/release outcome",
            "Worker narrative без primary evidence",
            "не пишет comments, не меняет status/Goal",
            "достаточен для формального завершения Goal",
            "не создаёт новую Task, blocker или delivery loop",
        ):
            self.assertIn(marker, compact)

    def test_metadata_is_discoverable_and_task_manager_only(self) -> None:
        metadata = METADATA.read_text(encoding="utf-8")
        self.assertIn('display_name: "Scope Reviewer"', metadata)
        self.assertIn("$issue-grinder:scope-reviewer", metadata)
        self.assertIn('value: "task-manager"', metadata)
        self.assertIn("allow_implicit_invocation: true", metadata)


if __name__ == "__main__":
    unittest.main()
