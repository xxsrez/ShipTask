from __future__ import annotations

import json
from pathlib import Path
import unittest

from scripts.issue_grinder_trace_harness import (
    BlockerContext,
    BlockerReport,
    SafeAction,
    decide_blocker,
    decide_environment_effect,
    decide_finalization,
    decide_goal_creation,
    decide_transition,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "issue-grinder" / "scenarios.json"


def action(raw: dict) -> SafeAction:
    return SafeAction(**raw)


class IssueGrinderTraceHarnessTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.report = BlockerReport(**cls.fixture["completeReport"])

    def test_explanation_reveals_safe_action_and_forces_auto_continue(self) -> None:
        decision = decide_blocker(
            BlockerContext(
                explanation_actions=(action(self.fixture["explanationUnlock"]),),
                goal_active=True,
            ),
            self.report,
        )

        self.assertEqual(decision.action, "continue_work")
        self.assertIn("post_explanation_reflection", decision.events)
        self.assertIn("continue:create_synthetic_fixture", decision.events)
        self.assertFalse(decision.may_publish)
        self.assertFalse(decision.may_stop)
        self.assertFalse(decision.may_update_goal_blocked)
        self.assertNotIn("publish_blocker_report", decision.events)
        self.assertNotIn("update_goal:blocked", decision.events)

    def test_public_uat_is_not_a_permission_blocker(self) -> None:
        decision = decide_blocker(
            BlockerContext(
                preflight_actions=(action(self.fixture["publicUatUnlock"]),),
                goal_active=True,
            ),
            self.report,
        )

        self.assertEqual(decision.action, "continue_work")
        self.assertEqual(decision.events[-1], "continue:deploy_public_uat")
        self.assertEqual(
            decide_environment_effect(explicit_run=True, target="public-uat"),
            "perform_nonproduction_effect",
        )

    def test_unverified_alternative_is_checked_before_any_handoff(self) -> None:
        decision = decide_blocker(
            BlockerContext(
                explanation_actions=(action(self.fixture["unverifiedAlternative"]),),
                goal_active=True,
            ),
            self.report,
        )

        self.assertEqual(decision.action, "verify_safe_action")
        self.assertEqual(decision.events[-1], "verify:try_alternate_ingress")
        self.assertFalse(decision.may_publish)
        self.assertFalse(decision.may_stop)

    def test_incomplete_report_repairs_without_stop_or_goal_write(self) -> None:
        decision = decide_blocker(
            BlockerContext(goal_active=True),
            BlockerReport(primary_cause="First tool failed"),
        )

        self.assertEqual(decision.action, "repair_explainer_report")
        self.assertFalse(decision.may_publish)
        self.assertFalse(decision.may_stop)
        self.assertFalse(decision.may_update_goal_blocked)
        self.assertTrue(
            any(item == "missing_report_field:resume_condition" for item in decision.defects)
        )

    def test_caller_error_is_repaired_instead_of_becoming_a_blocker(self) -> None:
        decision = decide_blocker(
            BlockerContext(goal_active=True),
            self.report,
            explainer_outcome="caller_error",
        )

        self.assertEqual(decision.action, "repair_explainer_call")
        self.assertEqual(decision.events[-1], "repair_explainer_call")
        self.assertFalse(decision.may_stop)

    def test_technical_explainer_failure_uses_native_reflection(self) -> None:
        decision = decide_blocker(
            BlockerContext(
                explanation_actions=(action(self.fixture["explanationUnlock"]),),
                goal_active=True,
            ),
            self.report,
            explainer_outcome="technical_error",
        )

        self.assertEqual(decision.action, "continue_work")
        self.assertIn("explainer_technical_error", decision.events)
        self.assertIn("communication:native", decision.events)
        self.assertFalse(decision.may_stop)

    def test_terminal_blocker_requires_report_before_goal_and_stop(self) -> None:
        decision = decide_blocker(
            BlockerContext(goal_active=True, platform_blocker_audit_passed=True),
            self.report,
        )

        self.assertEqual(decision.action, "terminal_blocker")
        self.assertTrue(decision.may_publish)
        self.assertTrue(decision.may_stop)
        self.assertTrue(decision.may_update_goal_blocked)
        self.assertLess(
            decision.events.index("publish_blocker_report"),
            decision.events.index("update_goal:blocked"),
        )
        self.assertLess(
            decision.events.index("update_goal:blocked"),
            decision.events.index("stop"),
        )

    def test_platform_blocker_audit_cannot_be_skipped(self) -> None:
        decision = decide_blocker(
            BlockerContext(goal_active=True, platform_blocker_audit_passed=False),
            self.report,
        )

        self.assertEqual(decision.action, "continue_platform_blocker_audit")
        self.assertFalse(decision.may_publish)
        self.assertFalse(decision.may_stop)
        self.assertFalse(decision.may_update_goal_blocked)

    def test_optional_improvement_does_not_create_bureaucratic_loop(self) -> None:
        decision = decide_blocker(
            BlockerContext(
                explanation_actions=(action(self.fixture["optionalImprovement"]),)
            ),
            self.report,
        )

        self.assertEqual(decision.action, "terminal_blocker")
        self.assertTrue(decision.may_stop)
        self.assertNotIn("continue:polish_optional_copy", decision.events)

    def test_goal_creation_and_finalization_gates(self) -> None:
        self.assertEqual(
            decide_goal_creation(
                explicit_run=True,
                active_issue_count=2,
                compatible_goal_exists=False,
            ),
            "create_goal",
        )
        self.assertEqual(
            decide_goal_creation(
                explicit_run=False,
                active_issue_count=3,
                compatible_goal_exists=False,
            ),
            "no_goal",
        )
        self.assertEqual(
            decide_finalization(active_issue_count=0, material_action_available=False),
            "complete",
        )
        self.assertEqual(
            decide_finalization(active_issue_count=0, material_action_available=True),
            "continue_work",
        )

    def test_comment_transaction_and_backlog_boundary(self) -> None:
        self.assertEqual(
            decide_transition(source_status="To Do", target_status="In Progress"),
            "transition_status",
        )
        self.assertEqual(
            decide_transition(source_status="In Review", target_status="Done"),
            "publish_comment",
        )
        self.assertEqual(
            decide_transition(
                source_status="In Review",
                target_status="Done",
                comment_committed=True,
            ),
            "read_back_comment",
        )
        self.assertEqual(
            decide_transition(
                source_status="In Review",
                target_status="Done",
                comment_committed=True,
                comment_read_back=True,
                observed_status=None,
            ),
            "reconcile_status",
        )
        self.assertEqual(
            decide_transition(source_status="Backlog", target_status="In Progress"),
            "reject_backlog_mutation",
        )

    def test_production_is_rejected_and_unknown_uat_resolved(self) -> None:
        self.assertEqual(
            decide_environment_effect(explicit_run=True, target="production"),
            "reject_production",
        )
        self.assertEqual(
            decide_environment_effect(explicit_run=True, target=None),
            "resolve_uat_before_effect",
        )


if __name__ == "__main__":
    unittest.main()
