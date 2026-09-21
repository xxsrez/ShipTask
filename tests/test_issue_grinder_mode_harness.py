from __future__ import annotations

from dataclasses import replace
import unittest

from scripts.issue_grinder_mode_harness import (
    EconomicalCheckpoint,
    ExecutionMode,
    LUNA_MAX,
    ModeOrigin,
    Profile,
    ReviewWaveObservation,
    assess_review_wave,
    decide_mode_switch,
    decide_run_exit,
    mode_dispatch_policy,
    normalize_profiles,
    resolve_mode,
)


LUNA_EFFORTS = (None, "none", "minimal", "low", "medium", "high", "xhigh", "max")
SOL = Profile("gpt-5.6-sol", "xhigh")


def complete_checkpoint() -> EconomicalCheckpoint:
    return EconomicalCheckpoint(
        exact_candidate="commit:abc123",
        saved_change_identity="branch:codex/ig-mode",
        task_ownership_evidence="packet:IG-42",
        base_identity="commit:base123",
        branch_or_worktree_identity="worktree:/tmp/ig-mode",
        integration_identity="commit:integration123",
        checks=("unit", "static"),
        raw_results=("unit: 12 passed", "static: passed"),
        known_defects=(),
        unknowns=("expensive reviewer not run",),
        deferred_gates=("controller final review",),
        next_step="review commit abc123",
        resume_condition="controller capacity available",
        task_manager_status="In Review",
        goal_active=True,
    )


class IssueGrinderModeHarnessTest(unittest.TestCase):
    def complete_review_wave(
        self, mode: ExecutionMode, **overrides: object
    ) -> ReviewWaveObservation:
        values: dict[str, object] = {
            "mode": mode,
            "scope_is_simple": True,
            "direct_owner_id": "review-wave-owner",
            "parent_visible_child_ids": ("review-wave-owner",),
            "candidate_author_id": "candidate-author",
            "reviewer_id": "independent-reviewer",
            "routing_guard_count": 1,
            "owner_dispatch_count": 1,
            "event_wait_count": 1,
            "review_complete": True,
            "finding_ledger_returned": True,
        }
        values.update(overrides)
        return ReviewWaveObservation(**values)

    def test_review_modes_keep_independent_review_on_simple_scope(self) -> None:
        for mode in (
            ExecutionMode.CLASSIC,
            ExecutionMode.CLASSIC,
            ExecutionMode.ECONOMICAL,
        ):
            with self.subTest(mode=mode):
                decision = assess_review_wave(self.complete_review_wave(mode))
                self.assertTrue(decision.may_accept_terminal)
                self.assertEqual(decision.defects, ())

    def test_review_wave_rejects_polling_and_repeated_guard(self) -> None:
        decision = assess_review_wave(
            self.complete_review_wave(
                ExecutionMode.CLASSIC,
                routing_guard_count=3,
                owner_dispatch_count=2,
                event_wait_count=4,
                unchanged_state_actions=("status_poll", "empty_nudge"),
            )
        )
        self.assertFalse(decision.may_accept_terminal)
        self.assertIn("direct_owner_guard_count_not_one", decision.defects)
        self.assertIn("unchanged_state_coordination:status_poll", decision.defects)

    def test_only_economical_may_checkpoint_partial_review(self) -> None:
        economical = assess_review_wave(
            self.complete_review_wave(
                ExecutionMode.ECONOMICAL,
                review_complete=False,
                finding_ledger_returned=False,
                terminal_acceptance_requested=False,
                deadline_reached=True,
                partial_ledger_returned=True,
                checkpoint_requested=True,
            )
        )
        classic = assess_review_wave(
            self.complete_review_wave(
                ExecutionMode.CLASSIC,
                review_complete=False,
                finding_ledger_returned=False,
                terminal_acceptance_requested=False,
                deadline_reached=True,
                partial_ledger_returned=True,
                checkpoint_requested=True,
            )
        )
        self.assertTrue(economical.may_checkpoint)
        self.assertFalse(classic.may_checkpoint)

    def test_every_explicit_mode_wins(self) -> None:
        for main_profile in (LUNA_MAX,):
            for mode in ExecutionMode:
                with self.subTest(main=main_profile, mode=mode):
                    record = resolve_mode(main_profile, explicit_mode=mode)
                    self.assertEqual(record.canonical_mode, mode)
                    self.assertEqual(record.mode_origin, ModeOrigin.EXPLICIT)

    def test_single_task_default_is_solo_except_luna_max(self) -> None:
        for effort in LUNA_EFFORTS:
            with self.subTest(effort=effort):
                record = resolve_mode(Profile("gpt-5.6-luna", effort))
                self.assertEqual(record.canonical_mode, ExecutionMode.BALANCE if effort == "max" else ExecutionMode.SOLO)
                self.assertEqual(record.mode_origin, ModeOrigin.AUTOMATIC)
        self.assertEqual(resolve_mode(SOL).canonical_mode, ExecutionMode.SOLO)

    def test_other_modes_keep_luna_max_worker_baseline(self) -> None:
        for mode in (
            ExecutionMode.CLASSIC,
            ExecutionMode.CLASSIC,
            ExecutionMode.ECONOMICAL,
        ):
            with self.subTest(mode=mode):
                self.assertEqual(normalize_profiles(LUNA_MAX, mode=mode).worker, LUNA_MAX)

    def test_role_overrides_win(self) -> None:
        controller = Profile("gpt-5.6-terra", "high")
        worker = Profile("gpt-5.6-luna", "medium")
        profiles = normalize_profiles(
            SOL,
            mode=ExecutionMode.CLASSIC,
            controller_override=controller,
            worker_override=worker,
        )
        self.assertEqual(profiles.controller, controller)
        self.assertEqual(profiles.worker, worker)

    def test_proven_continuation_preserves_mode_after_model_change(self) -> None:
        original = resolve_mode(SOL, explicit_mode=ExecutionMode.CLASSIC)
        resumed = resolve_mode(
            Profile("gpt-5.6-luna", "none"),
            saved_record=original,
            continuity_proven=True,
        )
        self.assertIs(resumed, original)

    def test_unproven_continuity_returns_to_solo_default(self) -> None:
        old = resolve_mode(SOL, explicit_mode=ExecutionMode.CLASSIC)
        new = resolve_mode(
            Profile("gpt-5.6-luna", "high"),
            saved_record=old,
            continuity_proven=False,
        )
        self.assertEqual(new.canonical_mode, ExecutionMode.SOLO)

    def test_proven_continuity_requires_record_and_switch_barrier(self) -> None:
        with self.assertRaisesRegex(ValueError, "saved mode record"):
            resolve_mode(SOL, continuity_proven=True)
        with self.assertRaisesRegex(ValueError, "switch barrier"):
            resolve_mode(
                SOL,
                saved_record=resolve_mode(SOL),
                continuity_proven=True,
                explicit_mode=ExecutionMode.CLASSIC,
            )

    def test_only_economical_has_nonterminal_checkpoint(self) -> None:
        accepted = decide_run_exit(
            ExecutionMode.ECONOMICAL,
            active_scope_count=2,
            checkpoint=complete_checkpoint(),
        )
        self.assertTrue(accepted.may_checkpoint)
        for mode in (
            ExecutionMode.SOLO,
            ExecutionMode.CLASSIC,
            ExecutionMode.CLASSIC,
            ExecutionMode.CLASSIC,
        ):
            with self.subTest(mode=mode):
                decision = decide_run_exit(
                    mode,
                    active_scope_count=1,
                    checkpoint=complete_checkpoint(),
                )
                self.assertFalse(decision.may_checkpoint)

    def test_terminal_completion_requires_empty_active_scope(self) -> None:
        rejected = decide_run_exit(
            ExecutionMode.CLASSIC,
            active_scope_count=1,
            terminal_acceptance_proven=True,
        )
        accepted = decide_run_exit(
            ExecutionMode.CLASSIC,
            active_scope_count=0,
            terminal_acceptance_proven=True,
        )
        self.assertIn("active_scope_prevents_completion", rejected.defects)
        self.assertTrue(accepted.may_complete)

    def test_mode_switch_requires_explicit_safe_barrier(self) -> None:
        current = resolve_mode(SOL, explicit_mode=ExecutionMode.SOLO)
        automatic = decide_mode_switch(
            current,
            ExecutionMode.CLASSIC,
            explicit_request=False,
        )
        unsafe = decide_mode_switch(
            current,
            ExecutionMode.CLASSIC,
            explicit_request=True,
            active_writer_count=2,
            active_writers_checkpointed=False,
            integration_unchanged=False,
            ownership_reconciled=False,
            evidence_preserved=False,
        )
        self.assertEqual(automatic.action, "keep_mode")
        self.assertEqual(unsafe.action, "await_switch_barrier")
        self.assertEqual(len(unsafe.defects), 4)

    def test_safe_mode_switch_changes_only_mode_and_origin(self) -> None:
        current = resolve_mode(SOL, explicit_mode=ExecutionMode.SOLO)
        decision = decide_mode_switch(
            current,
            ExecutionMode.CLASSIC,
            explicit_request=True,
            active_writer_count=1,
            active_writers_checkpointed=True,
        )
        self.assertTrue(decision.may_apply_next_wave)
        self.assertEqual(decision.mode_record.canonical_mode, ExecutionMode.CLASSIC)
        self.assertEqual(decision.mode_record.mode_origin, ModeOrigin.EXPLICIT)


if __name__ == "__main__":
    unittest.main()
