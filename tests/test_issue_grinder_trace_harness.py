from __future__ import annotations

import json
from pathlib import Path
import unittest

from scripts.issue_grinder_trace_harness import (
    AcceptedBlockerState,
    BlockerContinuationContext,
    BlockerContext,
    BlockerReasonAnswer,
    BlockerReport,
    ExistingWorkArtifact,
    SafeAction,
    WriterPacket,
    decide_blocker,
    decide_blocker_continuation,
    decide_environment_effect,
    decide_finalization,
    decide_goal_creation,
    decide_recovery,
    decide_stored_permission,
    decide_startup_recovery,
    decide_transition,
    decide_writer_wave,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "issue-grinder" / "scenarios.json"


def action(raw: dict) -> SafeAction:
    return SafeAction(**raw)


class IssueGrinderTraceHarnessTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        report = dict(cls.fixture["completeReport"])
        report["blocking_reasons"] = tuple(report["blocking_reasons"])
        cls.report = BlockerReport(**report)
        cls.reason_answers = tuple(
            BlockerReasonAnswer(**item) for item in cls.fixture["reasonAnswers"]
        )

    def test_explanation_reveals_safe_action_and_forces_auto_continue(self) -> None:
        decision = decide_blocker(
            BlockerContext(
                explanation_actions=(action(self.fixture["explanationUnlock"]),),
                goal_active=True,
            ),
            self.report,
            reason_answers=self.reason_answers,
        )

        self.assertEqual(decision.action, "continue_work")
        self.assertIn("post_explanation_reflection", decision.events)
        self.assertIn("continue:create_synthetic_fixture", decision.events)
        self.assertFalse(decision.may_publish)
        self.assertFalse(decision.may_stop)
        self.assertFalse(decision.may_update_goal_blocked)
        self.assertNotIn("publish_blocker_report", decision.events)
        self.assertNotIn("update_goal:blocked", decision.events)

    def test_writer_wave_dispatches_only_after_all_admissions(self) -> None:
        decision = decide_writer_wave(
            (
                WriterPacket("packet-one", prepared=True, admission_receipt_valid=True),
                WriterPacket("packet-two", prepared=True, admission_receipt_valid=True),
            ),
            integration_snapshot_valid=True,
            integration_unchanged=True,
        )

        self.assertEqual(decision.action, "dispatch_implementation")
        self.assertTrue(decision.may_dispatch_implementation)
        self.assertFalse(decision.may_fan_in)
        self.assertFalse(decision.may_write_lifecycle)
        self.assertLess(
            decision.events.index("all_admissions_valid"),
            decision.events.index("authorize_implementation_dispatch"),
        )

    def test_startup_inventory_precedes_fresh_work(self) -> None:
        decision = decide_startup_recovery((), inventory_completed=False)

        self.assertEqual(decision.action, "inspect_existing_work")
        self.assertFalse(decision.may_prepare_fresh)
        self.assertFalse(decision.may_resume)

    def test_quiescent_checkpoint_is_resumed_instead_of_replaced(self) -> None:
        decision = decide_startup_recovery(
            (
                ExistingWorkArtifact(
                    "branch:codex/issue-grinder/md-331",
                    scope_relation="exact",
                    owner_state="quiescent",
                ),
            ),
            inventory_completed=True,
        )

        self.assertEqual(decision.action, "resume_checkpoint")
        self.assertTrue(decision.may_resume)
        self.assertFalse(decision.may_prepare_fresh)

    def test_active_or_ambiguous_artifact_blocks_parallel_replacement(self) -> None:
        active = decide_startup_recovery(
            (
                ExistingWorkArtifact(
                    "worktree:md-331",
                    scope_relation="exact",
                    owner_state="active",
                ),
            ),
            inventory_completed=True,
        )
        ambiguous = decide_startup_recovery(
            (
                ExistingWorkArtifact(
                    "diff:unknown",
                    scope_relation="ambiguous",
                    owner_state="unknown",
                ),
            ),
            inventory_completed=True,
        )

        self.assertEqual(active.action, "continue_via_active_owner")
        self.assertEqual(ambiguous.action, "resolve_artifact_scope")
        self.assertFalse(active.may_prepare_fresh)
        self.assertFalse(ambiguous.may_prepare_fresh)

    def test_only_unrelated_artifacts_allow_fresh_work(self) -> None:
        unrelated = decide_startup_recovery(
            (
                ExistingWorkArtifact(
                    "worktree:user-experiment",
                    scope_relation="unrelated",
                    owner_state="unknown",
                ),
            ),
            inventory_completed=True,
        )
        integrated = decide_startup_recovery(
            (
                ExistingWorkArtifact(
                    "commit:finished",
                    scope_relation="exact",
                    owner_state="quiescent",
                    integrated=True,
                ),
            ),
            inventory_completed=True,
        )

        self.assertEqual(unrelated.action, "prepare_fresh")
        self.assertTrue(unrelated.may_prepare_fresh)
        self.assertEqual(integrated.action, "reuse_integrated_result")
        self.assertFalse(integrated.may_prepare_fresh)

    def test_writer_wave_missing_admission_blocks_all_effects(self) -> None:
        decision = decide_writer_wave(
            (WriterPacket("packet-one", prepared=True, admission_receipt_valid=False),),
            integration_snapshot_valid=True,
            integration_unchanged=True,
        )

        self.assertEqual(decision.action, "await_admission")
        self.assertFalse(decision.may_dispatch_implementation)
        self.assertFalse(decision.may_fan_in)
        self.assertFalse(decision.may_write_lifecycle)

    def test_writer_wave_rejects_dispatch_without_admission(self) -> None:
        decision = decide_writer_wave(
            (
                WriterPacket(
                    "packet-one",
                    prepared=True,
                    admission_receipt_valid=False,
                    implementation_dispatched=True,
                ),
            ),
            integration_snapshot_valid=True,
            integration_unchanged=True,
        )

        self.assertEqual(decision.action, "reconcile_writer_wave")
        self.assertIn("dispatch_without_admission", decision.defects)
        self.assertFalse(decision.may_dispatch_implementation)
        self.assertFalse(decision.may_fan_in)
        self.assertFalse(decision.may_write_lifecycle)

    def test_writer_wave_integration_change_blocks_fan_in(self) -> None:
        decision = decide_writer_wave(
            (
                WriterPacket(
                    "packet-one",
                    prepared=True,
                    admission_receipt_valid=True,
                    implementation_dispatched=True,
                    task_owned_commit=True,
                ),
            ),
            integration_snapshot_valid=True,
            integration_unchanged=False,
        )

        self.assertEqual(decision.action, "reconcile_writer_wave")
        self.assertIn("integration_checkout_changed", decision.defects)
        self.assertFalse(decision.may_fan_in)
        self.assertFalse(decision.may_write_lifecycle)

    def test_writer_wave_fan_in_requires_task_owned_commits(self) -> None:
        packet = WriterPacket(
            "packet-one",
            prepared=True,
            admission_receipt_valid=True,
            implementation_dispatched=True,
        )
        waiting = decide_writer_wave(
            (packet,),
            integration_snapshot_valid=True,
            integration_unchanged=True,
        )
        ready = decide_writer_wave(
            (
                WriterPacket(
                    "packet-one",
                    prepared=True,
                    admission_receipt_valid=True,
                    implementation_dispatched=True,
                    task_owned_commit=True,
                ),
            ),
            integration_snapshot_valid=True,
            integration_unchanged=True,
        )

        self.assertEqual(waiting.action, "await_task_owned_commits")
        self.assertFalse(waiting.may_fan_in)
        self.assertEqual(ready.action, "fan_in")
        self.assertTrue(ready.may_fan_in)
        self.assertFalse(ready.may_write_lifecycle)

    def test_public_uat_is_not_a_permission_blocker(self) -> None:
        decision = decide_blocker(
            BlockerContext(
                preflight_actions=(action(self.fixture["publicUatUnlock"]),),
                goal_active=True,
            ),
            self.report,
            reason_answers=self.reason_answers,
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
            reason_answers=self.reason_answers,
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

    def test_each_blocking_reason_requires_a_separate_answer(self) -> None:
        decision = decide_blocker(
            BlockerContext(goal_active=True),
            self.report,
            reason_answers=self.reason_answers[:-1],
        )

        self.assertEqual(decision.action, "repair_explainer_reason_answers")
        self.assertFalse(decision.may_publish)
        self.assertFalse(decision.may_stop)
        self.assertFalse(decision.may_update_goal_blocked)
        self.assertTrue(
            any(item.startswith("missing_reason_answer:") for item in decision.defects)
        )
        self.assertNotIn("publish_blocker_report", decision.events)

    def test_reason_answer_requires_all_three_explanatory_lenses(self) -> None:
        incomplete = BlockerReasonAnswer(
            reason=self.reason_answers[0].reason,
            blocks_goal_because=self.reason_answers[0].blocks_goal_because,
            agent_cannot_resolve_because=self.reason_answers[0].agent_cannot_resolve_because,
        )
        decision = decide_blocker(
            BlockerContext(goal_active=True),
            self.report,
            reason_answers=(incomplete, self.reason_answers[1]),
        )

        self.assertEqual(decision.action, "repair_explainer_reason_answers")
        self.assertIn(
            f"missing_reason_answer_field:{incomplete.reason}:goal_value",
            decision.defects,
        )
        self.assertFalse(decision.may_publish)
        self.assertFalse(decision.may_stop)

    def test_caller_error_is_repaired_instead_of_becoming_a_blocker(self) -> None:
        decision = decide_blocker(
            BlockerContext(goal_active=True),
            self.report,
            reason_answers=self.reason_answers,
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
            reason_answers=self.reason_answers,
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
            reason_answers=self.reason_answers,
        )

        self.assertEqual(decision.action, "terminal_blocker")
        self.assertTrue(decision.may_publish)
        self.assertTrue(decision.may_stop)
        self.assertTrue(decision.may_update_goal_blocked)
        reason_events = tuple(
            event
            for event in decision.events
            if event.startswith("publish_blocker_reason:")
        )
        self.assertEqual(len(reason_events), len(self.report.blocking_reasons))
        self.assertLess(
            decision.events.index("publish_blocker_report"),
            decision.events.index(reason_events[0]),
        )
        self.assertLess(
            decision.events.index(reason_events[-1]),
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
            reason_answers=self.reason_answers,
        )

        self.assertEqual(decision.action, "terminal_blocker")
        self.assertTrue(decision.may_publish)
        self.assertTrue(decision.may_stop)
        self.assertFalse(decision.may_update_goal_blocked)
        self.assertIn("publish_blocker_report", decision.events)
        self.assertIn("goal_block_pending_audit", decision.events)
        self.assertNotIn("update_goal:blocked", decision.events)

    def test_automatic_goal_continuation_reuses_handoff_without_retry(self) -> None:
        decision = decide_blocker_continuation(
            BlockerContinuationContext(
                goal_active=True,
                current_fingerprint="md-393:independent-principal",
                accepted=AcceptedBlockerState(
                    fingerprint="md-393:independent-principal",
                    handoff_published=True,
                    consecutive_goal_turns=2,
                ),
            )
        )

        self.assertEqual(decision.action, "await_platform_blocker_audit")
        self.assertFalse(decision.may_repeat_blocker_check)
        self.assertFalse(decision.may_invoke_explainer)
        self.assertFalse(decision.may_publish)
        self.assertFalse(decision.may_request_user)
        self.assertFalse(decision.may_update_goal_blocked)
        self.assertTrue(decision.may_stop)
        self.assertIn("suppress_duplicate_blocker_check", decision.events)
        self.assertIn("suppress_duplicate_user_request", decision.events)

    def test_platform_threshold_adds_only_missing_goal_effect(self) -> None:
        decision = decide_blocker_continuation(
            BlockerContinuationContext(
                goal_active=True,
                current_fingerprint="md-393:independent-principal",
                accepted=AcceptedBlockerState(
                    fingerprint="md-393:independent-principal",
                    handoff_published=True,
                    consecutive_goal_turns=3,
                ),
            )
        )

        self.assertEqual(decision.action, "finalize_goal_blocked")
        self.assertFalse(decision.may_repeat_blocker_check)
        self.assertFalse(decision.may_invoke_explainer)
        self.assertFalse(decision.may_publish)
        self.assertFalse(decision.may_request_user)
        self.assertTrue(decision.may_update_goal_blocked)
        self.assertEqual(decision.events[-2:], ("update_goal:blocked", "stop"))

    def test_new_relevant_signal_invalidates_accepted_blocker(self) -> None:
        decision = decide_blocker_continuation(
            BlockerContinuationContext(
                goal_active=True,
                current_fingerprint="md-393:independent-principal",
                accepted=AcceptedBlockerState(
                    fingerprint="md-393:independent-principal",
                    handoff_published=True,
                    consecutive_goal_turns=2,
                ),
                relevant_user_signal=True,
            )
        )

        self.assertEqual(decision.action, "resume_delivery")
        self.assertTrue(decision.may_repeat_blocker_check)
        self.assertFalse(decision.may_invoke_explainer)
        self.assertFalse(decision.may_publish)
        self.assertFalse(decision.may_stop)
        self.assertIn("invalidate_blocker_checkpoint", decision.events)

    def test_optional_improvement_does_not_create_bureaucratic_loop(self) -> None:
        decision = decide_blocker(
            BlockerContext(
                explanation_actions=(action(self.fixture["optionalImprovement"]),)
            ),
            self.report,
            reason_answers=self.reason_answers,
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

    def test_goal_reuse_requires_same_run_continuity(self) -> None:
        self.assertEqual(
            decide_goal_creation(
                explicit_run=True,
                active_issue_count=2,
                compatible_goal_exists=True,
                same_run_continuity=True,
            ),
            "reuse_goal",
        )
        self.assertEqual(
            decide_goal_creation(
                explicit_run=True,
                active_issue_count=2,
                compatible_goal_exists=True,
                same_run_continuity=False,
            ),
            "goal_continuity_required",
        )
        self.assertEqual(
            decide_goal_creation(
                explicit_run=False,
                active_issue_count=3,
                compatible_goal_exists=True,
                same_run_continuity=False,
            ),
            "no_goal",
        )

    def test_recovery_requires_changed_input_or_uses_bounded_exit(self) -> None:
        self.assertEqual(
            decide_recovery(
                previous_progress_fingerprint="scope-v1:error-timeout",
                current_progress_fingerprint="scope-v2:error-timeout",
                fallback_available=False,
            ),
            "continue_with_changed_input",
        )
        self.assertEqual(
            decide_recovery(
                previous_progress_fingerprint="scope-v1:error-timeout",
                current_progress_fingerprint="scope-v1:error-timeout",
                fallback_available=True,
            ),
            "use_fallback",
        )
        self.assertEqual(
            decide_recovery(
                previous_progress_fingerprint="scope-v1:error-timeout",
                current_progress_fingerprint="scope-v1:error-timeout",
                fallback_available=False,
            ),
            "candidate_blocker",
        )

    def test_stored_always_permission_is_narrow_and_cross_run(self) -> None:
        self.assertEqual(
            decide_stored_permission(
                persisted=True,
                same_project=True,
                same_category=True,
                target_production=False,
            ),
            "authorize_exact_category",
        )
        self.assertEqual(
            decide_stored_permission(
                persisted=True,
                same_project=True,
                same_category=False,
                target_production=False,
            ),
            "request_permission",
        )
        self.assertEqual(
            decide_stored_permission(
                persisted=True,
                same_project=True,
                same_category=True,
                target_production=True,
            ),
            "reject_production",
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

    def test_provider_production_label_does_not_reclassify_project_uat(self) -> None:
        self.assertEqual(
            decide_environment_effect(
                explicit_run=True,
                target="uat",
                provider_operation_label="This deploys the site to production",
            ),
            "perform_nonproduction_effect",
        )
        self.assertEqual(
            decide_environment_effect(
                explicit_run=True,
                target="production",
                provider_operation_label="Deploy preview",
            ),
            "reject_production",
        )


if __name__ == "__main__":
    unittest.main()
