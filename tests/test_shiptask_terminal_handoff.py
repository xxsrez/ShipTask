from __future__ import annotations

import json
from pathlib import Path
import unittest

from scripts.terminal_handoff_harness import (
    BlockerClaim,
    CandidateReport,
    HandoffContext,
    decide_terminal_handoff,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = (
    ROOT
    / "tests"
    / "shiptask-terminal-handoff"
    / "latest-minddiary-vague.json"
)


def load_context(raw: dict) -> HandoffContext:
    return HandoffContext(
        blockers=tuple(
            BlockerClaim(
                task_refs=tuple(item["taskRefs"]),
                required_publication_facts=tuple(
                    tuple(alternatives)
                    for alternatives in item["requiredPublicationFacts"]
                ),
            )
            for item in raw["blockers"]
        ),
        runnable_work=tuple(raw["runnableWork"]),
        goal_active=raw["goalActive"],
    )


class ShipTaskTerminalHandoffTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_runnable_rework_cancels_terminal_handoff(self) -> None:
        decision = decide_terminal_handoff(
            load_context(self.fixture["runnableContext"]),
            CandidateReport(self.fixture["vagueReport"]),
        )

        self.assertEqual(decision.action, "continue_work")
        self.assertFalse(decision.may_publish)
        self.assertFalse(decision.may_stop)
        self.assertFalse(decision.may_update_goal_blocked)
        self.assertIn("runnable_work_remains", decision.defects)

    def test_vague_blocker_report_is_repaired_before_goal_write_or_stop(self) -> None:
        decision = decide_terminal_handoff(
            load_context(self.fixture["blockedContext"]),
            CandidateReport(self.fixture["vagueReport"]),
            communication_mode="ordinary",
            repair_attempt=0,
        )

        self.assertEqual(decision.action, "request_fresh_explainer")
        self.assertFalse(decision.may_publish)
        self.assertFalse(decision.may_stop)
        self.assertFalse(decision.may_update_goal_blocked)
        self.assertTrue(
            any(defect.startswith("missing_blocker_fact:") for defect in decision.defects)
        )

    def test_grounded_actionable_report_unlocks_terminal_effect(self) -> None:
        decision = decide_terminal_handoff(
            load_context(self.fixture["blockedContext"]),
            CandidateReport(self.fixture["acceptedReport"]),
        )

        self.assertEqual(decision.action, "terminal_handoff")
        self.assertTrue(decision.may_publish)
        self.assertTrue(decision.may_stop)
        self.assertTrue(decision.may_update_goal_blocked)
        self.assertEqual(decision.defects, ())

    def test_second_bad_ordinary_report_switches_to_native_without_stopping(self) -> None:
        decision = decide_terminal_handoff(
            load_context(self.fixture["blockedContext"]),
            CandidateReport(self.fixture["vagueReport"]),
            communication_mode="ordinary",
            repair_attempt=1,
        )

        self.assertEqual(decision.action, "switch_to_native")
        self.assertFalse(decision.may_publish)
        self.assertFalse(decision.may_stop)
        self.assertFalse(decision.may_update_goal_blocked)

    def test_bad_native_report_is_repaired_without_stopping(self) -> None:
        decision = decide_terminal_handoff(
            load_context(self.fixture["blockedContext"]),
            CandidateReport(self.fixture["vagueReport"]),
            communication_mode="native",
        )

        self.assertEqual(decision.action, "repair_native_report")
        self.assertFalse(decision.may_publish)
        self.assertFalse(decision.may_stop)
        self.assertFalse(decision.may_update_goal_blocked)


if __name__ == "__main__":
    unittest.main()
