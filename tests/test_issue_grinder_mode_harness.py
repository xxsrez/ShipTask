from __future__ import annotations

from dataclasses import replace
import unittest

from scripts.issue_grinder_mode_harness import (
    BalanceWaveObservation,
    EconomicalCheckpoint,
    ExecutionMode,
    LUNA_HIGH,
    LUNA_MAX,
    ManagerLoopObservation,
    ModeOrigin,
    Profile,
    ReviewWaveObservation,
    assess_balance_wave,
    assess_manager_loop,
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

    def complete_balance_wave(self, **overrides: object) -> BalanceWaveObservation:
        values: dict[str, object] = {
            "mode": ExecutionMode.BALANCE,
            "packet_ids": ("parser", "waves", "critical"),
            "owner_ids": ("luna-parser", "luna-waves", "luna-critical"),
            "dependency_ready": (True, True, True),
            "self_contained": (True, True, True),
            "isolated_candidates": (True, True, True),
            "stable_interfaces": (True, True, True),
            "local_oracles": (True, True, True),
            "owned_surfaces": (
                ("microflow/parser.py",),
                ("microflow/waves.py",),
                ("microflow/critical.py",),
            ),
            "routing_valid": (True, True, True),
            "worker_models": ("gpt-5.6-luna",) * 3,
            "worker_efforts": ("high",) * 3,
            "nested_delegation_counts": (0, 0, 0),
            "dispatch_window_count": 1,
            "active_wave_count": 1,
            "total_execution_wave_count": 1,
            "admission_completed_before_first_source_change": True,
            "tool_wait_in_benefit_assessment": True,
            "peak_luna_workers": 3,
            "main_useful_work": True,
            "main_repeated_worker_work": False,
            "collective_wait_count": 1,
            "polling_actions": (),
            "handoff_candidate_ids": ("commit:a", "commit:b", "commit:c"),
            "handoff_checks_present": (True, True, True),
            "common_exact_base": True,
            "fan_in_complete": True,
            "ownership_verified": True,
            "parallel_tool_gate_count": 3,
            "integrated_checks_passed": True,
            "main_exact_diff_reviewed": True,
            "main_final_acceptance": True,
        }
        values.update(overrides)
        return BalanceWaveObservation(**values)

    def complete_manager_loop(self, **overrides: object) -> ManagerLoopObservation:
        observation = ManagerLoopObservation(
            control_brief_complete=True,
            manager_id="luna-manager",
            implementer_id="luna-implementer",
            reviewer_id="luna-reviewer",
            routing_guard_owner_ids=(
                "luna-manager",
                "luna-implementer",
                "luna-reviewer",
            ),
            dispatched_owner_ids=(
                "luna-manager",
                "luna-implementer",
                "luna-reviewer",
            ),
            manager_persistent=True,
            implementer_persistent=True,
            reviewer_persistent=True,
            manager_source_access=False,
            manager_work_tool_calls=0,
            manager_implementation=False,
            phase_ids=("contract", "core", "integration", "acceptance"),
            accepted_phase_ids=("contract", "core", "integration", "acceptance"),
            implementer_session_ids=("luna-implementer",) * 4,
            candidate_ids=("candidate-1",) * 4,
            max_concurrent_phases=1,
            manager_complete=True,
            review_started_after_manager_complete=True,
            reviewer_delegation_count=0,
            review_complete=True,
            finding_ledger_returned=True,
            controller_final_review_started_after_review=True,
        )
        return replace(observation, **overrides)

    def test_review_modes_keep_independent_review_on_simple_scope(self) -> None:
        for mode in (
            ExecutionMode.CLASSIC,
            ExecutionMode.SWARM,
            ExecutionMode.ECONOMICAL,
        ):
            with self.subTest(mode=mode):
                decision = assess_review_wave(self.complete_review_wave(mode))
                self.assertTrue(decision.may_accept_terminal)
                self.assertEqual(decision.defects, ())

    def test_solo_and_balance_do_not_use_default_review_wave(self) -> None:
        for mode in (ExecutionMode.SOLO, ExecutionMode.BALANCE):
            with self.subTest(mode=mode):
                with self.assertRaisesRegex(ValueError, "not a default"):
                    assess_review_wave(self.complete_review_wave(mode))

    def test_review_wave_rejects_polling_and_repeated_guard(self) -> None:
        decision = assess_review_wave(
            self.complete_review_wave(
                ExecutionMode.SWARM,
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

    def test_balance_happy_path_matches_accelerated_solo_topology(self) -> None:
        decision = assess_balance_wave(self.complete_balance_wave())
        self.assertTrue(decision.may_accept_terminal)
        self.assertEqual(decision.action, "ready_for_terminal_acceptance")
        self.assertEqual(decision.defects, ())

    def test_balance_rejects_overwide_or_serialized_wave(self) -> None:
        overwide = self.complete_balance_wave(
            packet_ids=("a", "b", "c", "d"),
            owner_ids=("oa", "ob", "oc", "od"),
            dependency_ready=(True,) * 4,
            self_contained=(True,) * 4,
            isolated_candidates=(True,) * 4,
            stable_interfaces=(True,) * 4,
            local_oracles=(True,) * 4,
            owned_surfaces=(("a",), ("b",), ("c",), ("d",)),
            routing_valid=(True,) * 4,
            worker_models=("gpt-5.6-luna",) * 4,
            worker_efforts=("high",) * 4,
            nested_delegation_counts=(0,) * 4,
            handoff_candidate_ids=("ca", "cb", "cc", "cd"),
            handoff_checks_present=(True,) * 4,
            peak_luna_workers=4,
            dispatch_window_count=4,
        )
        decision = assess_balance_wave(overwide)
        self.assertIn("balance_worker_ceiling_exceeded", decision.defects)
        self.assertIn("balance_dispatch_not_one_window", decision.defects)

    def test_balance_rejects_bad_admission_overlap_and_wrong_profile(self) -> None:
        decision = assess_balance_wave(
            self.complete_balance_wave(
                dependency_ready=(True, False, True),
                owned_surfaces=(("shared.py",), ("shared.py",), ("third.py",)),
                worker_efforts=("max", "high", "high"),
                nested_delegation_counts=(0, 1, 0),
            )
        )
        self.assertIn("packet_dependency_not_ready", decision.defects)
        self.assertIn("balance_write_surfaces_overlap", decision.defects)
        self.assertIn("balance_luna_high_effort_required", decision.defects)
        self.assertIn("balance_nested_delegation_forbidden", decision.defects)

    def test_balance_dispatches_before_work_and_counts_tool_wait(self) -> None:
        decision = assess_balance_wave(
            self.complete_balance_wave(
                total_execution_wave_count=2,
                admission_completed_before_first_source_change=False,
                tool_wait_in_benefit_assessment=False,
            )
        )
        self.assertIn("balance_total_execution_wave_count_not_one", decision.defects)
        self.assertIn("balance_source_change_before_admission_dispatch", decision.defects)
        self.assertIn("balance_tool_wait_ignored_in_admission", decision.defects)

    def test_balance_requires_useful_overlap_collective_wait_and_main_acceptance(self) -> None:
        decision = assess_balance_wave(
            self.complete_balance_wave(
                main_useful_work=False,
                main_repeated_worker_work=True,
                collective_wait_count=3,
                polling_actions=("status_poll",),
                fan_in_complete=False,
                parallel_tool_gate_count=1,
                integrated_checks_passed=False,
                main_exact_diff_reviewed=False,
                main_final_acceptance=False,
                separate_reviewer_count=1,
            )
        )
        for defect in (
            "balance_main_useful_overlap_missing",
            "balance_main_repeated_worker_work",
            "balance_collective_wait_count_not_one",
            "unchanged_state_coordination:status_poll",
            "balance_fan_in_incomplete",
            "balance_parallel_tool_gates_missing",
            "balance_integrated_checks_failed",
            "balance_main_exact_diff_review_missing",
            "balance_main_final_acceptance_missing",
            "balance_unexpected_separate_reviewer",
        ):
            self.assertIn(defect, decision.defects)

    def test_manager_loop_keeps_sessions_candidate_and_phase_order(self) -> None:
        decision = assess_manager_loop(self.complete_manager_loop())
        self.assertTrue(decision.may_enter_controller_final_review)
        self.assertEqual(decision.defects, ())

    def test_manager_loop_rejects_parallel_phases_and_early_review(self) -> None:
        decision = assess_manager_loop(
            self.complete_manager_loop(
                manager_source_access=True,
                max_concurrent_phases=2,
                manager_complete=False,
                review_started_after_manager_complete=False,
                review_complete=False,
            )
        )
        self.assertIn("manager_source_access", decision.defects)
        self.assertIn("manager_parallel_phases", decision.defects)
        self.assertIn("manager_incomplete", decision.defects)
        self.assertIn("manager_review_started_early", decision.defects)

    def test_every_explicit_mode_wins(self) -> None:
        for main_profile in (Profile("gpt-5.6-luna", "low"), SOL):
            for mode in ExecutionMode:
                with self.subTest(main=main_profile, mode=mode):
                    record = resolve_mode(main_profile, explicit_mode=mode)
                    self.assertEqual(record.canonical_mode, mode)
                    self.assertEqual(record.mode_origin, ModeOrigin.EXPLICIT)

    def test_default_is_always_solo_for_every_main_profile(self) -> None:
        for effort in LUNA_EFFORTS:
            with self.subTest(effort=effort):
                record = resolve_mode(Profile("gpt-5.6-luna", effort))
                self.assertEqual(record.canonical_mode, ExecutionMode.SOLO)
                self.assertEqual(record.mode_origin, ModeOrigin.AUTOMATIC)
        self.assertEqual(resolve_mode(SOL).canonical_mode, ExecutionMode.SOLO)

    def test_balance_normalizes_only_workers_to_luna_high(self) -> None:
        profiles = normalize_profiles(SOL, mode=ExecutionMode.BALANCE)
        self.assertEqual(profiles.controller, SOL)
        self.assertEqual(profiles.worker, LUNA_HIGH)

    def test_other_modes_keep_luna_max_worker_baseline(self) -> None:
        for mode in (
            ExecutionMode.CLASSIC,
            ExecutionMode.SWARM,
            ExecutionMode.ECONOMICAL,
        ):
            with self.subTest(mode=mode):
                self.assertEqual(normalize_profiles(SOL, mode=mode).worker, LUNA_MAX)

    def test_role_overrides_win(self) -> None:
        controller = Profile("gpt-5.6-terra", "high")
        worker = Profile("gpt-5.6-luna", "medium")
        profiles = normalize_profiles(
            SOL,
            mode=ExecutionMode.BALANCE,
            controller_override=controller,
            worker_override=worker,
        )
        self.assertEqual(profiles.controller, controller)
        self.assertEqual(profiles.worker, worker)

    def test_solo_and_balance_dispatch_policies_are_distinct(self) -> None:
        solo = mode_dispatch_policy(resolve_mode(SOL), current_main_profile=SOL)
        balance_record = resolve_mode(SOL, explicit_mode=ExecutionMode.BALANCE)
        balance = mode_dispatch_policy(balance_record, current_main_profile=SOL)
        self.assertFalse(solo.issue_grinder_execution_subagents_allowed)
        self.assertEqual(solo.max_active_execution_subagents, 0)
        self.assertEqual(solo.execution_profile, SOL)
        self.assertTrue(balance.issue_grinder_execution_subagents_allowed)
        self.assertEqual(balance.max_active_execution_subagents, 3)
        self.assertEqual(balance.max_active_execution_lanes, 4)
        self.assertEqual(balance.execution_profile, LUNA_HIGH)

    def test_proven_continuation_preserves_mode_after_model_change(self) -> None:
        original = resolve_mode(SOL, explicit_mode=ExecutionMode.SWARM)
        resumed = resolve_mode(
            Profile("gpt-5.6-luna", "none"),
            saved_record=original,
            continuity_proven=True,
        )
        self.assertIs(resumed, original)

    def test_unproven_continuity_returns_to_solo_default(self) -> None:
        old = resolve_mode(SOL, explicit_mode=ExecutionMode.BALANCE)
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
                explicit_mode=ExecutionMode.BALANCE,
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
            ExecutionMode.BALANCE,
            ExecutionMode.SWARM,
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
            ExecutionMode.BALANCE,
            active_scope_count=1,
            terminal_acceptance_proven=True,
        )
        accepted = decide_run_exit(
            ExecutionMode.BALANCE,
            active_scope_count=0,
            terminal_acceptance_proven=True,
        )
        self.assertIn("active_scope_prevents_completion", rejected.defects)
        self.assertTrue(accepted.may_complete)

    def test_mode_switch_requires_explicit_safe_barrier(self) -> None:
        current = resolve_mode(SOL)
        automatic = decide_mode_switch(
            current,
            ExecutionMode.BALANCE,
            explicit_request=False,
        )
        unsafe = decide_mode_switch(
            current,
            ExecutionMode.BALANCE,
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
        current = resolve_mode(SOL)
        decision = decide_mode_switch(
            current,
            ExecutionMode.SWARM,
            explicit_request=True,
            active_writer_count=1,
            active_writers_checkpointed=True,
        )
        self.assertTrue(decision.may_apply_next_wave)
        self.assertEqual(decision.mode_record.canonical_mode, ExecutionMode.SWARM)
        self.assertEqual(decision.mode_record.mode_origin, ModeOrigin.EXPLICIT)


if __name__ == "__main__":
    unittest.main()
