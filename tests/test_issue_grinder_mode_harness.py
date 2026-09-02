from __future__ import annotations

from dataclasses import replace
import unittest

from scripts.issue_grinder_mode_harness import (
    BalanceFinding,
    EconomicalCheckpoint,
    ExecutionMode,
    LUNA_MAX,
    ModeOrigin,
    Profile,
    assess_balance_packet,
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
    def test_complete_balance_packet_can_enter_final_review(self) -> None:
        decision = assess_balance_packet(
            packet_id="TM-42-implementation-1",
            exact_candidate="commit:abc123",
            checks=("unit: passed", "integration: passed"),
            materially_changed=True,
            independent_verification_possible=True,
            independent_verification_performed=True,
            findings=(
                BalanceFinding(
                    finding="boundary case covered",
                    evidence="test_boundary_case: passed",
                    material=True,
                    disposition="fixed",
                ),
            ),
            expensive_work_roles=(
                "material_judgment",
                "integration_decision",
                "final_review",
            ),
        )

        self.assertEqual(decision.action, "ready_for_final_review")
        self.assertTrue(decision.may_enter_final_review)
        self.assertEqual(decision.defects, ())

    def test_balance_packet_requires_independent_verification_when_possible(
        self,
    ) -> None:
        decision = assess_balance_packet(
            packet_id="TM-42-implementation-1",
            exact_candidate="commit:abc123",
            checks=("unit: passed",),
            materially_changed=True,
            independent_verification_possible=True,
            independent_verification_performed=False,
            findings=(),
        )

        self.assertFalse(decision.may_enter_final_review)
        self.assertIn("independent_verification_missing", decision.defects)

    def test_balance_material_finding_is_not_outvoted(self) -> None:
        decision = assess_balance_packet(
            packet_id="TM-42-implementation-1",
            exact_candidate="commit:abc123",
            checks=("unit: passed",),
            materially_changed=True,
            independent_verification_possible=True,
            independent_verification_performed=True,
            findings=(
                BalanceFinding("looks good", "review:a", False, "fixed"),
                BalanceFinding("looks good", "review:b", False, "fixed"),
                BalanceFinding(
                    "data race remains",
                    "stress_test: reproduces",
                    True,
                    "escalate",
                ),
            ),
            escalation_questions=("Which consistency contract is required?",),
        )

        self.assertFalse(decision.may_enter_final_review)
        self.assertIn("escalation_pending", decision.defects)
        self.assertIn("finding_2:material_escalation_pending", decision.defects)

    def test_balance_rejects_broad_escalation_and_ordinary_expensive_work(
        self,
    ) -> None:
        decision = assess_balance_packet(
            packet_id="TM-42-implementation-1",
            exact_candidate="commit:abc123",
            checks=("unit: passed",),
            materially_changed=False,
            independent_verification_possible=False,
            independent_verification_performed=False,
            findings=(),
            escalation_questions=("Choose storage", "Implement the feature"),
            routing_valid=False,
            expensive_work_roles=("research", "implementation"),
        )

        self.assertFalse(decision.may_enter_final_review)
        self.assertIn("routing_invalid", decision.defects)
        self.assertIn("escalation_not_narrow", decision.defects)
        self.assertIn("ordinary_expensive_work:research", decision.defects)
        self.assertIn("ordinary_expensive_work:implementation", decision.defects)

    def test_every_explicit_mode_wins_for_luna_and_non_luna(self) -> None:
        for main_profile in (Profile("gpt-5.6-luna", "low"), SOL):
            for mode in ExecutionMode:
                with self.subTest(main=main_profile, mode=mode):
                    record = resolve_mode(main_profile, explicit_mode=mode)
                    self.assertEqual(record.canonical_mode, mode)
                    self.assertEqual(record.mode_origin, ModeOrigin.EXPLICIT)

    def test_all_luna_efforts_choose_economical_and_collapse_roles(self) -> None:
        for effort in LUNA_EFFORTS:
            with self.subTest(effort=effort):
                record = resolve_mode(Profile("gpt-5.6-luna", effort))
                self.assertEqual(record.canonical_mode, ExecutionMode.ECONOMICAL)
                self.assertEqual(record.mode_origin, ModeOrigin.AUTOMATIC)
                self.assertEqual(record.role_profiles.controller, LUNA_MAX)
                self.assertEqual(record.role_profiles.worker, LUNA_MAX)

    def test_solo_uses_current_profile_one_lane_without_execution_delegation(self) -> None:
        for main_profile in (Profile("gpt-5.6-luna", "low"), SOL):
            with self.subTest(main=main_profile):
                record = resolve_mode(
                    main_profile,
                    explicit_mode=ExecutionMode.SOLO,
                )
                policy = mode_dispatch_policy(
                    record,
                    current_main_profile=main_profile,
                )

                self.assertEqual(record.canonical_mode, ExecutionMode.SOLO)
                self.assertEqual(policy.execution_profile, main_profile)
                self.assertFalse(
                    policy.issue_grinder_execution_subagents_allowed
                )
                self.assertEqual(policy.max_active_execution_lanes, 1)
                self.assertTrue(policy.service_provider_agents_allowed)

    def test_other_modes_do_not_inherit_solo_topology(self) -> None:
        for mode in (
            ExecutionMode.CLASSIC,
            ExecutionMode.BALANCE,
            ExecutionMode.SWARM,
            ExecutionMode.ECONOMICAL,
        ):
            with self.subTest(mode=mode):
                policy = mode_dispatch_policy(
                    resolve_mode(SOL, explicit_mode=mode),
                    current_main_profile=SOL,
                )
                self.assertTrue(
                    policy.issue_grinder_execution_subagents_allowed
                )
                self.assertIsNone(policy.max_active_execution_lanes)
                self.assertIsNone(policy.execution_profile)
                self.assertTrue(policy.service_provider_agents_allowed)

    def test_automatic_luna_match_is_exact_not_fuzzy(self) -> None:
        for model in ("gpt-5.6-sol", "gpt-5.6-terra", "gpt-5.6-luna-preview"):
            with self.subTest(model=model):
                record = resolve_mode(Profile(model, "high"))
                self.assertEqual(record.canonical_mode, ExecutionMode.CLASSIC)

    def test_non_luna_keeps_controller_and_uses_luna_worker(self) -> None:
        profiles = normalize_profiles(SOL)

        self.assertEqual(profiles.controller, SOL)
        self.assertEqual(profiles.worker, LUNA_MAX)

    def test_role_overrides_win_independently(self) -> None:
        controller = Profile("gpt-5.6-terra", "high")
        worker = Profile("gpt-5.6-luna", "medium")
        profiles = normalize_profiles(
            Profile("gpt-5.6-luna", "low"),
            controller_override=controller,
            worker_override=worker,
        )

        self.assertEqual(profiles.controller, controller)
        self.assertEqual(profiles.worker, worker)

    def test_proven_continuation_preserves_mode_after_model_change(self) -> None:
        original = resolve_mode(
            SOL,
            explicit_mode=ExecutionMode.SWARM,
        )
        resumed = resolve_mode(
            Profile("gpt-5.6-luna", "none"),
            saved_record=original,
            continuity_proven=True,
        )

        self.assertIs(resumed, original)
        self.assertEqual(resumed.canonical_mode, ExecutionMode.SWARM)
        self.assertEqual(resumed.initial_main_profile, SOL)

    def test_unproven_continuity_does_not_leak_an_old_mode(self) -> None:
        old_record = resolve_mode(SOL, explicit_mode=ExecutionMode.BALANCE)
        new_record = resolve_mode(
            Profile("gpt-5.6-luna", "high"),
            saved_record=old_record,
            continuity_proven=False,
        )

        self.assertEqual(new_record.canonical_mode, ExecutionMode.ECONOMICAL)
        self.assertEqual(new_record.mode_origin, ModeOrigin.AUTOMATIC)

    def test_solo_continuation_uses_new_current_profile_without_mode_drift(self) -> None:
        original = resolve_mode(SOL, explicit_mode=ExecutionMode.SOLO)
        new_current = Profile("gpt-5.6-luna", "low")
        resumed = resolve_mode(
            new_current,
            saved_record=original,
            continuity_proven=True,
        )
        policy = mode_dispatch_policy(
            resumed,
            current_main_profile=new_current,
        )

        self.assertIs(resumed, original)
        self.assertEqual(resumed.canonical_mode, ExecutionMode.SOLO)
        self.assertEqual(policy.execution_profile, new_current)
        self.assertFalse(policy.issue_grinder_execution_subagents_allowed)
        self.assertTrue(policy.service_provider_agents_allowed)

    def test_proven_continuity_requires_a_record_and_switch_barrier(self) -> None:
        with self.assertRaisesRegex(ValueError, "saved mode record"):
            resolve_mode(SOL, continuity_proven=True)
        with self.assertRaisesRegex(ValueError, "switch barrier"):
            resolve_mode(
                SOL,
                saved_record=resolve_mode(SOL),
                continuity_proven=True,
                explicit_mode=ExecutionMode.BALANCE,
            )

    def test_complete_economical_checkpoint_is_nonterminal(self) -> None:
        decision = decide_run_exit(
            ExecutionMode.ECONOMICAL,
            active_scope_count=2,
            checkpoint=complete_checkpoint(),
        )

        self.assertEqual(decision.action, "checkpoint")
        self.assertTrue(decision.may_checkpoint)
        self.assertFalse(decision.may_complete)
        self.assertFalse(decision.may_block)

    def test_checkpoint_requires_every_observable_field(self) -> None:
        checkpoint = complete_checkpoint()
        blank_cases = {
            "exact_candidate": "",
            "saved_change_identity": "",
            "task_ownership_evidence": "",
            "base_identity": "",
            "branch_or_worktree_identity": "",
            "integration_identity": "",
            "checks": (),
            "raw_results": (),
            "known_defects": None,
            "unknowns": None,
            "deferred_gates": None,
            "next_step": "",
            "resume_condition": "",
            "task_manager_status": "",
            "goal_active": False,
        }

        for field_name, value in blank_cases.items():
            with self.subTest(field=field_name):
                decision = decide_run_exit(
                    ExecutionMode.ECONOMICAL,
                    active_scope_count=1,
                    checkpoint=replace(checkpoint, **{field_name: value}),
                )
                self.assertEqual(decision.action, "continue")
                self.assertFalse(decision.may_checkpoint)
                self.assertTrue(
                    any(field_name in defect for defect in decision.defects),
                    decision.defects,
                )

    def test_checkpoint_requires_an_active_task_status(self) -> None:
        decision = decide_run_exit(
            ExecutionMode.ECONOMICAL,
            active_scope_count=1,
            checkpoint=replace(complete_checkpoint(), task_manager_status="Done"),
        )

        self.assertEqual(decision.action, "continue")
        self.assertIn(
            "checkpoint_missing:active_task_manager_status", decision.defects
        )

    def test_other_modes_cannot_exit_through_checkpoint(self) -> None:
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
                self.assertEqual(decision.action, "continue")
                self.assertFalse(decision.may_checkpoint)

    def test_terminal_completion_requires_empty_active_scope(self) -> None:
        rejected = decide_run_exit(
            ExecutionMode.CLASSIC,
            active_scope_count=1,
            terminal_acceptance_proven=True,
        )
        accepted = decide_run_exit(
            ExecutionMode.ECONOMICAL,
            active_scope_count=0,
            terminal_acceptance_proven=True,
        )

        self.assertEqual(rejected.action, "continue")
        self.assertIn("active_scope_prevents_completion", rejected.defects)
        self.assertEqual(accepted.action, "complete")
        self.assertTrue(accepted.may_complete)

    def test_mode_switch_requires_explicit_request_and_safe_barrier(self) -> None:
        current = resolve_mode(SOL)
        automatic = decide_mode_switch(
            current,
            ExecutionMode.ECONOMICAL,
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
        self.assertEqual(automatic.mode_record, current)
        self.assertEqual(unsafe.action, "await_switch_barrier")
        self.assertEqual(len(unsafe.defects), 4)
        self.assertFalse(unsafe.may_apply_next_wave)

    def test_safe_mode_switch_changes_only_mode_and_origin(self) -> None:
        current = resolve_mode(SOL)
        decision = decide_mode_switch(
            current,
            ExecutionMode.SWARM,
            explicit_request=True,
            active_writer_count=1,
            active_writers_checkpointed=True,
        )

        self.assertEqual(decision.action, "switch_next_wave")
        self.assertTrue(decision.may_apply_next_wave)
        self.assertEqual(decision.mode_record.canonical_mode, ExecutionMode.SWARM)
        self.assertEqual(decision.mode_record.mode_origin, ModeOrigin.EXPLICIT)
        self.assertEqual(
            decision.mode_record.initial_main_profile,
            current.initial_main_profile,
        )
        self.assertEqual(decision.mode_record.role_profiles, current.role_profiles)


if __name__ == "__main__":
    unittest.main()
