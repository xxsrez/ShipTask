from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUITE = ROOT / "tests" / "strategic-explainer"
CASES = SUITE / "cases"
COMMON_RUBRIC = SUITE / "common-rubric.md"

EXPECTED_CASES = {
    "automatic-capture-safe-boundary",
    "blocked-goal-causal-report",
    "bulk-cross-project-rollback",
    "comment-idempotency-and-stale-edit",
    "completion-comment-command-dump",
    "concurrent-edit-no-hidden-merge",
    "green-local-failed-uat",
    "hierarchy-cycle-and-stale-guard",
    "historical-content-current-access",
    "idempotent-retry-with-authorization",
    "invitation-reissue-single-pending",
    "large-file-boundary",
    "manager-role-ceiling",
    "mixed-preview-boundary",
    "ownership-transfer-one-owner",
    "project-shadow-restore",
    "redeploy-persistence-failure",
    "review-completion-duplicate-evidence",
    "release-delete-membership-boundary",
    "release-open-tasks-confirmation",
    "saved-view-base-temporary-separation",
    "viewer-comment-permissions",
    "write-rebind-fences-prepared-commit",
}

EXPECTED_SOURCE_PORTFOLIO = {
    "ExampleNotes": 12,
    "Task Manager": 11,
}

FACT_SECTIONS = (
    "## Publication unit",
    "## User-visible acceptance",
    "## Knowledge and authority boundary",
    "## Audit-only evidence",
    "## Accepted product source",
)

RUBRIC_SECTIONS = (
    "## What exactly was checked",
    "## Factual coverage",
    "## Human comprehension",
    "## Relevance and compression",
    "## Forbidden leakage",
    "## Verdict",
)


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


class StrategicExplainerCasesTest(unittest.TestCase):
    def test_suite_has_expected_cases(self) -> None:
        actual = {path.name for path in CASES.iterdir() if path.is_dir()}
        self.assertEqual(actual, EXPECTED_CASES)

    def test_each_case_separates_raw_facts_from_rubric(self) -> None:
        for name in sorted(EXPECTED_CASES):
            with self.subTest(case=name):
                case = CASES / name
                facts = (case / "facts.md").read_text(encoding="utf-8")
                rubric = (case / "rubric.md").read_text(encoding="utf-8")

                self.assertTrue(facts.startswith(f"# Raw facts: {name}\n"))
                self.assertTrue(rubric.startswith(f"# Evaluation rubric: {name}\n"))
                for heading in FACT_SECTIONS:
                    self.assertIn(heading, facts)
                for heading in RUBRIC_SECTIONS:
                    self.assertIn(heading, rubric)

                self.assertGreaterEqual(
                    len(re.findall(r"^### Scenario ", facts, flags=re.MULTILINE)),
                    2,
                )
                normalized_facts = normalized(facts)
                self.assertIn("полностью синтетический сценарий", normalized_facts)
                self.assertIn("не описывает текущую Task", normalized_facts)
                self.assertRegex(
                    facts,
                    r"(?m)^Source project: (?:ExampleNotes|Task Manager)$",
                )

                # Generator sees facts.md only. Keep evaluator language and the
                # desired-answer channel out of that fixture.
                for leaked_instruction in (
                    "Evaluation rubric",
                    "intended wording",
                    "expected answer",
                    "Вернуть `PASS`",
                    "comprehension gap",
                ):
                    self.assertNotIn(leaked_instruction, facts)

    def test_suite_covers_expected_product_sources(self) -> None:
        actual = {project: 0 for project in EXPECTED_SOURCE_PORTFOLIO}
        for name in EXPECTED_CASES:
            facts = (CASES / name / "facts.md").read_text(encoding="utf-8")
            match = re.search(
                r"(?m)^Source project: (ExampleNotes|Task Manager)$",
                facts,
            )
            self.assertIsNotNone(match, name)
            actual[match.group(1)] += 1

        self.assertEqual(actual, EXPECTED_SOURCE_PORTFOLIO)

    def test_rubrics_grade_semantics_not_wording(self) -> None:
        for name in sorted(EXPECTED_CASES):
            with self.subTest(case=name):
                rubric = (CASES / name / "rubric.md").read_text(encoding="utf-8")
                self.assertIn("оценивает смысл", rubric)
                self.assertNotRegex(rubric, r"(?i)ровно \d+ (?:слов|предложен|пункт)")
                self.assertNotIn("обязательный заголовок", rubric.lower())

    def test_suite_protocol_preserves_blind_generation(self) -> None:
        protocol = normalized((SUITE / "README.md").read_text(encoding="utf-8"))
        for concept in (
            'fork_turns="none"',
            'model="gpt-5.6-luna"',
            'reasoning_effort="max"',
            "facts.md",
            "rubric.md",
            "publication text",
            "source basis",
            "common-rubric.md",
            "blind generation trial",
        ):
            self.assertIn(concept, protocol)

    def test_common_gate_rejects_empty_and_hybrid_reports(self) -> None:
        rubric = normalized(COMMON_RUBRIC.read_text(encoding="utf-8"))
        for concept in (
            "что именно человек сделал",
            "всё работает",
            "считаются водой",
            "смысловой каркас собран из английских слов",
            "synthetic private UAT",
            "MD-EVAL-*",
            "TM-EVAL-*",
            "номера внутренних ревизий",
            "SHA",
            "source basis",
            "командные строки",
            "абсолютные пути",
            "неизменившийся доказательный след",
        ):
            self.assertIn(concept, rubric)


if __name__ == "__main__":
    unittest.main()
