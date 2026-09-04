"""Deterministic oracle for the mechanical Issue Grinder mode decisions.

The oracle covers the parts of IG-MODE-02, IG-MODE-04..07,
IG-MODE-10, IG-MODE-11 and IG-MA-19 that can be decided from structured state. It
deliberately does not parse natural language, orchestrate agents or stand in for
a model-forward run of the skill.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum


LUNA_MODEL = "gpt-5.6-luna"
LUNA_MAX_EFFORT = "max"
LUNA_HIGH_EFFORT = "high"
ACTIVE_TASK_STATUSES = frozenset({"In Progress", "In Review"})
FORBIDDEN_UNCHANGED_COORDINATION = frozenset(
    {
        "guard_discovery",
        "guard_help",
        "status_poll",
        "status_list",
        "empty_nudge",
    }
)


class ExecutionMode(str, Enum):
    SOLO = "solo"
    CLASSIC = "classic"
    BALANCE = "balance"
    SWARM = "swarm"
    ECONOMICAL = "economical"


class ModeOrigin(str, Enum):
    EXPLICIT = "explicit"
    AUTOMATIC = "automatic"


@dataclass(frozen=True)
class Profile:
    model: str
    effort: str | None

    def __post_init__(self) -> None:
        if not self.model.strip():
            raise ValueError("profile model must not be blank")
        if self.effort is not None and not self.effort.strip():
            raise ValueError("profile effort must not be blank")

    @property
    def is_luna(self) -> bool:
        return self.model.strip().casefold() == LUNA_MODEL


LUNA_MAX = Profile(LUNA_MODEL, LUNA_MAX_EFFORT)
LUNA_HIGH = Profile(LUNA_MODEL, LUNA_HIGH_EFFORT)


@dataclass(frozen=True)
class RoleProfiles:
    controller: Profile
    worker: Profile


@dataclass(frozen=True)
class ModeRecord:
    canonical_mode: ExecutionMode
    mode_origin: ModeOrigin
    initial_main_profile: Profile
    role_profiles: RoleProfiles


@dataclass(frozen=True)
class ModeDispatchPolicy:
    issue_grinder_execution_subagents_allowed: bool
    max_active_execution_lanes: int | None
    max_active_execution_subagents: int | None
    execution_profile: Profile | None
    service_provider_agents_allowed: bool


def mode_dispatch_policy(
    record: ModeRecord,
    *,
    current_main_profile: Profile,
) -> ModeDispatchPolicy:
    """Return the mechanical topology constraints of the selected mode."""

    if record.canonical_mode is ExecutionMode.SOLO:
        return ModeDispatchPolicy(
            issue_grinder_execution_subagents_allowed=False,
            max_active_execution_lanes=1,
            max_active_execution_subagents=0,
            execution_profile=current_main_profile,
            service_provider_agents_allowed=True,
        )
    if record.canonical_mode is ExecutionMode.BALANCE:
        return ModeDispatchPolicy(
            issue_grinder_execution_subagents_allowed=True,
            max_active_execution_lanes=4,
            max_active_execution_subagents=3,
            execution_profile=record.role_profiles.worker,
            service_provider_agents_allowed=True,
        )
    return ModeDispatchPolicy(
        issue_grinder_execution_subagents_allowed=True,
        max_active_execution_lanes=None,
        max_active_execution_subagents=None,
        execution_profile=None,
        service_provider_agents_allowed=True,
    )


def normalize_profiles(
    main_profile: Profile,
    *,
    mode: ExecutionMode = ExecutionMode.CLASSIC,
    controller_override: Profile | None = None,
    worker_override: Profile | None = None,
) -> RoleProfiles:
    """Apply the selected mode's worker baseline without guessing ordering."""

    default_controller = LUNA_MAX if main_profile.is_luna else main_profile
    default_worker = LUNA_HIGH if mode is ExecutionMode.BALANCE else LUNA_MAX
    if mode is ExecutionMode.BALANCE:
        default_controller = main_profile
    return RoleProfiles(
        controller=controller_override or default_controller,
        worker=worker_override or default_worker,
    )


def resolve_mode(
    main_profile: Profile,
    *,
    explicit_mode: ExecutionMode | None = None,
    saved_record: ModeRecord | None = None,
    continuity_proven: bool = False,
    controller_override: Profile | None = None,
    worker_override: Profile | None = None,
) -> ModeRecord:
    """Resolve a new run or restore a proven continuation without mode drift."""

    if continuity_proven:
        if saved_record is None:
            raise ValueError("proven continuity requires a saved mode record")
        if explicit_mode is not None:
            raise ValueError("an explicit mode switch must pass the switch barrier")
        return saved_record

    canonical_mode = explicit_mode or ExecutionMode.SOLO
    origin = (
        ModeOrigin.EXPLICIT
        if explicit_mode is not None
        else ModeOrigin.AUTOMATIC
    )
    return ModeRecord(
        canonical_mode=canonical_mode,
        mode_origin=origin,
        initial_main_profile=main_profile,
        role_profiles=normalize_profiles(
            main_profile,
            mode=canonical_mode,
            controller_override=controller_override,
            worker_override=worker_override,
        ),
    )


@dataclass(frozen=True)
class ReviewWaveObservation:
    mode: ExecutionMode
    scope_is_simple: bool
    direct_owner_id: str
    parent_visible_child_ids: tuple[str, ...]
    candidate_author_id: str
    reviewer_id: str
    routing_guard_count: int
    owner_dispatch_count: int
    event_wait_count: int
    review_complete: bool
    finding_ledger_returned: bool
    terminal_acceptance_requested: bool = True
    deadline_reached: bool = False
    partial_ledger_returned: bool = False
    checkpoint_requested: bool = False
    unchanged_state_actions: tuple[str, ...] = ()
    material_rework: bool = False
    resumed_owner_id: str = ""
    resumed_reviewer_id: str = ""
    continuation_wait_count: int = 0
    replacement_reviewer_created: bool = False


@dataclass(frozen=True)
class ReviewWaveDecision:
    action: str
    may_accept_terminal: bool
    may_checkpoint: bool
    defects: tuple[str, ...] = ()


@dataclass(frozen=True)
class BalanceWaveObservation:
    """Observed main-owned Balance wave and its integration gates."""

    mode: ExecutionMode
    packet_ids: tuple[str, ...]
    owner_ids: tuple[str, ...]
    dependency_ready: tuple[bool, ...]
    self_contained: tuple[bool, ...]
    isolated_candidates: tuple[bool, ...]
    stable_interfaces: tuple[bool, ...]
    local_oracles: tuple[bool, ...]
    owned_surfaces: tuple[tuple[str, ...], ...]
    routing_valid: tuple[bool, ...]
    worker_models: tuple[str, ...]
    worker_efforts: tuple[str, ...]
    nested_delegation_counts: tuple[int, ...]
    dispatch_window_count: int
    active_wave_count: int
    total_execution_wave_count: int
    admission_completed_before_first_source_change: bool
    tool_wait_in_benefit_assessment: bool
    peak_luna_workers: int
    main_useful_work: bool
    main_repeated_worker_work: bool
    collective_wait_count: int
    polling_actions: tuple[str, ...]
    handoff_candidate_ids: tuple[str, ...]
    handoff_checks_present: tuple[bool, ...]
    common_exact_base: bool
    fan_in_complete: bool
    ownership_verified: bool
    integration_patch_rendered_in_context: bool = False
    parallel_tool_gate_count: int = 0
    integrated_checks_passed: bool = False
    main_exact_diff_reviewed: bool = False
    main_final_acceptance: bool = False
    separate_reviewer_count: int = 0


@dataclass(frozen=True)
class BalanceWaveDecision:
    action: str
    may_accept_terminal: bool
    defects: tuple[str, ...] = ()


def assess_balance_wave(
    observation: BalanceWaveObservation,
) -> BalanceWaveDecision:
    """Validate the accelerated Solo-like Balance topology."""

    if observation.mode is not ExecutionMode.BALANCE:
        raise ValueError("balance wave applies only to Balance")

    defects: list[str] = []
    packet_count = len(observation.packet_ids)
    parallel_fields = (
        observation.owner_ids,
        observation.dependency_ready,
        observation.self_contained,
        observation.isolated_candidates,
        observation.stable_interfaces,
        observation.local_oracles,
        observation.owned_surfaces,
        observation.routing_valid,
        observation.worker_models,
        observation.worker_efforts,
        observation.nested_delegation_counts,
        observation.handoff_candidate_ids,
        observation.handoff_checks_present,
    )
    if packet_count < 2:
        defects.append("balance_parallel_wave_requires_two_packets")
    if packet_count > 3:
        defects.append("balance_worker_ceiling_exceeded")
    if any(len(values) != packet_count for values in parallel_fields):
        defects.append("balance_packet_evidence_length_mismatch")
        return BalanceWaveDecision("repair_balance_wave", False, tuple(defects))
    if any(not value.strip() for value in observation.packet_ids):
        defects.append("blank_packet_id")
    if len(set(observation.packet_ids)) != packet_count:
        defects.append("duplicate_packet_id")
    if any(not value.strip() for value in observation.owner_ids):
        defects.append("blank_owner_id")
    if len(set(observation.owner_ids)) != packet_count:
        defects.append("owners_not_independent")
    if not all(observation.dependency_ready):
        defects.append("packet_dependency_not_ready")
    if not all(observation.self_contained):
        defects.append("packet_not_self_contained")
    if not all(observation.isolated_candidates):
        defects.append("candidate_not_isolated")
    if not all(observation.stable_interfaces):
        defects.append("packet_interface_not_stable")
    if not all(observation.local_oracles):
        defects.append("packet_local_oracle_missing")
    normalized_surfaces = [set(values) for values in observation.owned_surfaces]
    for index, surfaces in enumerate(normalized_surfaces):
        if not surfaces or any(not value.strip() for value in surfaces):
            defects.append(f"packet_{index}:owned_surfaces_missing")
        for later in normalized_surfaces[index + 1 :]:
            if surfaces & later:
                defects.append("balance_write_surfaces_overlap")
    if not all(observation.routing_valid):
        defects.append("routing_invalid")
    if any(model.strip().casefold() != LUNA_MODEL for model in observation.worker_models):
        defects.append("balance_luna_model_required")
    if any(effort.strip().casefold() != LUNA_HIGH_EFFORT for effort in observation.worker_efforts):
        defects.append("balance_luna_high_effort_required")
    if any(count != 0 for count in observation.nested_delegation_counts):
        defects.append("balance_nested_delegation_forbidden")
    if observation.dispatch_window_count != 1:
        defects.append("balance_dispatch_not_one_window")
    if observation.active_wave_count != 1:
        defects.append("balance_active_wave_count_not_one")
    if observation.total_execution_wave_count != 1:
        defects.append("balance_total_execution_wave_count_not_one")
    if not observation.admission_completed_before_first_source_change:
        defects.append("balance_source_change_before_admission_dispatch")
    if not observation.tool_wait_in_benefit_assessment:
        defects.append("balance_tool_wait_ignored_in_admission")
    if observation.peak_luna_workers != packet_count:
        defects.append("balance_peak_workers_mismatch")
    if not observation.main_useful_work:
        defects.append("balance_main_useful_overlap_missing")
    if observation.main_repeated_worker_work:
        defects.append("balance_main_repeated_worker_work")
    if observation.collective_wait_count != 1:
        defects.append("balance_collective_wait_count_not_one")
    for action in observation.polling_actions:
        normalized = action.strip().casefold()
        if normalized in FORBIDDEN_UNCHANGED_COORDINATION:
            defects.append(f"unchanged_state_coordination:{normalized}")
    if any(not value.strip() for value in observation.handoff_candidate_ids):
        defects.append("balance_candidate_identity_missing")
    if not all(observation.handoff_checks_present):
        defects.append("balance_packet_check_missing")
    if not observation.common_exact_base:
        defects.append("candidate_base_mismatch")
    if not observation.fan_in_complete:
        defects.append("balance_fan_in_incomplete")
    if not observation.ownership_verified:
        defects.append("balance_ownership_not_verified")
    if observation.integration_patch_rendered_in_context:
        defects.append("integration_patch_rendered_in_context")
    if observation.parallel_tool_gate_count < 2:
        defects.append("balance_parallel_tool_gates_missing")
    if not observation.integrated_checks_passed:
        defects.append("balance_integrated_checks_failed")
    if not observation.main_exact_diff_reviewed:
        defects.append("balance_main_exact_diff_review_missing")
    if not observation.main_final_acceptance:
        defects.append("balance_main_final_acceptance_missing")
    if observation.separate_reviewer_count:
        defects.append("balance_unexpected_separate_reviewer")

    may_accept = not defects
    return BalanceWaveDecision(
        "ready_for_terminal_acceptance" if may_accept else "repair_balance_wave",
        may_accept,
        tuple(defects),
    )


@dataclass(frozen=True)
class ManagerLoopObservation:
    """Observed persistent Manager Loop for canonical_mode=swarm."""

    control_brief_complete: bool
    manager_id: str
    implementer_id: str
    reviewer_id: str
    routing_guard_owner_ids: tuple[str, ...]
    dispatched_owner_ids: tuple[str, ...]
    manager_persistent: bool
    implementer_persistent: bool
    reviewer_persistent: bool
    manager_source_access: bool
    manager_work_tool_calls: int
    manager_implementation: bool
    phase_ids: tuple[str, ...]
    accepted_phase_ids: tuple[str, ...]
    implementer_session_ids: tuple[str, ...]
    candidate_ids: tuple[str, ...]
    max_concurrent_phases: int
    manager_complete: bool
    review_started_after_manager_complete: bool
    reviewer_delegation_count: int
    review_complete: bool
    finding_ledger_returned: bool
    controller_final_review_started_after_review: bool
    material_rework: bool = False
    rework_implementer_id: str = ""
    recheck_reviewer_id: str = ""
    unchanged_state_actions: tuple[str, ...] = ()


@dataclass(frozen=True)
class ManagerLoopDecision:
    action: str
    may_enter_controller_final_review: bool
    defects: tuple[str, ...] = ()


def assess_manager_loop(
    observation: ManagerLoopObservation,
) -> ManagerLoopDecision:
    """Validate stable sessions, sequential phases and final independent review."""

    defects: list[str] = []
    owners = (
        observation.manager_id,
        observation.implementer_id,
        observation.reviewer_id,
    )
    if any(not owner.strip() for owner in owners):
        defects.append("manager_blank_owner")
    if len(set(owners)) != len(owners):
        defects.append("manager_roles_not_independent")
    if tuple(observation.routing_guard_owner_ids) != owners:
        defects.append("manager_routing_guards_do_not_match_roles")
    if tuple(observation.dispatched_owner_ids) != owners:
        defects.append("manager_dispatches_do_not_match_roles")
    if not observation.control_brief_complete:
        defects.append("manager_control_brief_missing")
    if not observation.manager_persistent:
        defects.append("manager_session_not_persistent")
    if not observation.implementer_persistent:
        defects.append("manager_implementer_not_persistent")
    if not observation.reviewer_persistent:
        defects.append("manager_reviewer_not_persistent")
    if observation.manager_source_access:
        defects.append("manager_source_access")
    if observation.manager_work_tool_calls:
        defects.append("manager_work_tool_use")
    if observation.manager_implementation:
        defects.append("manager_implemented")

    phases = tuple(phase.strip() for phase in observation.phase_ids)
    if not phases or any(not phase for phase in phases):
        defects.append("manager_phase_plan_missing")
    elif len(set(phases)) != len(phases):
        defects.append("manager_phase_ids_not_stable")
    if tuple(observation.accepted_phase_ids) != phases:
        defects.append("manager_phases_not_accepted_in_order")
    if len(observation.implementer_session_ids) != len(phases) or any(
        session_id != observation.implementer_id
        for session_id in observation.implementer_session_ids
    ):
        defects.append("manager_implementer_session_replaced")
    if len(observation.candidate_ids) != len(phases):
        defects.append("manager_candidate_trace_incomplete")
    elif observation.candidate_ids and len(set(observation.candidate_ids)) != 1:
        defects.append("manager_candidate_replaced")
    if observation.max_concurrent_phases != 1:
        defects.append("manager_parallel_phases")
    if not observation.manager_complete:
        defects.append("manager_incomplete")
    if not observation.review_started_after_manager_complete:
        defects.append("manager_review_started_early")
    if observation.reviewer_delegation_count:
        defects.append("manager_reviewer_delegated")
    if not observation.review_complete:
        defects.append("manager_independent_review_incomplete")
    if not observation.finding_ledger_returned:
        defects.append("manager_finding_ledger_missing")
    if not observation.controller_final_review_started_after_review:
        defects.append("manager_controller_final_review_started_early")
    if observation.material_rework:
        if observation.rework_implementer_id != observation.implementer_id:
            defects.append("manager_rework_implementer_replaced")
        if observation.recheck_reviewer_id != observation.reviewer_id:
            defects.append("manager_recheck_reviewer_replaced")

    for action in observation.unchanged_state_actions:
        normalized = action.strip().casefold()
        if normalized in FORBIDDEN_UNCHANGED_COORDINATION:
            defects.append(f"unchanged_state_coordination:{normalized}")

    may_enter = not defects
    return ManagerLoopDecision(
        "ready_for_controller_final_review" if may_enter else "repair_manager_loop",
        may_enter,
        tuple(defects),
    )


def assess_review_wave(observation: ReviewWaveObservation) -> ReviewWaveDecision:
    """Check an independent-review envelope for modes that require it."""

    if observation.mode in {ExecutionMode.SOLO, ExecutionMode.BALANCE}:
        raise ValueError("independent review wave is not a default for this mode")

    defects: list[str] = []
    if not observation.direct_owner_id.strip():
        defects.append("blank_direct_owner")
    if observation.parent_visible_child_ids != (observation.direct_owner_id,):
        defects.append("parent_visible_children_not_one_owner")
    if observation.routing_guard_count != 1:
        defects.append("direct_owner_guard_count_not_one")
    if observation.owner_dispatch_count != 1:
        defects.append("direct_owner_dispatch_count_not_one")
    if observation.event_wait_count != 1:
        defects.append("direct_owner_event_wait_count_not_one")
    if not observation.candidate_author_id.strip():
        defects.append("blank_candidate_author")
    if not observation.reviewer_id.strip():
        defects.append("blank_reviewer")
    elif observation.reviewer_id == observation.candidate_author_id:
        defects.append("reviewer_not_independent")
    if not observation.review_complete:
        defects.append("independent_review_incomplete")
    if not observation.finding_ledger_returned:
        defects.append("finding_ledger_missing")

    for action in observation.unchanged_state_actions:
        normalized = action.strip().casefold()
        if normalized in FORBIDDEN_UNCHANGED_COORDINATION:
            defects.append(f"unchanged_state_coordination:{normalized}")

    if observation.deadline_reached and not (
        observation.finding_ledger_returned or observation.partial_ledger_returned
    ):
        defects.append("deadline_handoff_missing")

    if observation.material_rework:
        if observation.resumed_owner_id != observation.direct_owner_id:
            defects.append("rework_owner_replaced")
        if observation.resumed_reviewer_id != observation.reviewer_id:
            defects.append("rework_reviewer_replaced")
        if observation.continuation_wait_count != 1:
            defects.append("rework_event_wait_count_not_one")
        if observation.replacement_reviewer_created:
            defects.append("replacement_reviewer_without_reason")

    may_checkpoint = (
        observation.mode is ExecutionMode.ECONOMICAL
        and observation.checkpoint_requested
        and (observation.finding_ledger_returned or observation.partial_ledger_returned)
    )
    may_accept_terminal = (
        observation.terminal_acceptance_requested
        and observation.review_complete
        and observation.finding_ledger_returned
        and not defects
    )
    if may_accept_terminal:
        action = "ready_for_terminal_acceptance"
    elif may_checkpoint:
        action = "economical_review_checkpoint"
    else:
        action = "repair_review_wave"
    return ReviewWaveDecision(action, may_accept_terminal, may_checkpoint, tuple(defects))


@dataclass(frozen=True)
class EconomicalCheckpoint:
    exact_candidate: str = ""
    saved_change_identity: str = ""
    task_ownership_evidence: str = ""
    base_identity: str = ""
    branch_or_worktree_identity: str = ""
    integration_identity: str = ""
    checks: tuple[str, ...] = ()
    raw_results: tuple[str, ...] = ()
    known_defects: tuple[str, ...] | None = None
    unknowns: tuple[str, ...] | None = None
    deferred_gates: tuple[str, ...] | None = None
    next_step: str = ""
    resume_condition: str = ""
    task_manager_status: str = ""
    goal_active: bool = False

    def missing_fields(self) -> tuple[str, ...]:
        missing = [
            field_name
            for field_name in (
                "exact_candidate",
                "saved_change_identity",
                "task_ownership_evidence",
                "base_identity",
                "branch_or_worktree_identity",
                "integration_identity",
                "next_step",
                "resume_condition",
                "task_manager_status",
            )
            if not getattr(self, field_name).strip()
        ]
        for field_name in ("checks", "raw_results"):
            values = getattr(self, field_name)
            if not values or any(not value.strip() for value in values):
                missing.append(field_name)
        for field_name in ("known_defects", "unknowns", "deferred_gates"):
            values = getattr(self, field_name)
            if values is None or any(not value.strip() for value in values):
                missing.append(field_name)
        if (
            self.task_manager_status
            and self.task_manager_status not in ACTIVE_TASK_STATUSES
        ):
            missing.append("active_task_manager_status")
        if not self.goal_active:
            missing.append("goal_active")
        return tuple(missing)


@dataclass(frozen=True)
class RunExitDecision:
    action: str
    may_complete: bool
    may_block: bool
    may_checkpoint: bool
    defects: tuple[str, ...] = ()


def decide_run_exit(
    mode: ExecutionMode,
    *,
    active_scope_count: int,
    terminal_acceptance_proven: bool = False,
    terminal_blocker_accepted: bool = False,
    checkpoint: EconomicalCheckpoint | None = None,
) -> RunExitDecision:
    """Separate terminal completion/blocking from an economical checkpoint."""

    if active_scope_count < 0:
        raise ValueError("active_scope_count must not be negative")
    if terminal_acceptance_proven and terminal_blocker_accepted:
        raise ValueError("a run cannot be both accepted and blocked")
    if terminal_acceptance_proven and active_scope_count == 0:
        return RunExitDecision("complete", True, False, False)
    if terminal_blocker_accepted:
        return RunExitDecision("blocked", False, True, False)

    defects: tuple[str, ...] = ()
    if terminal_acceptance_proven:
        defects = ("active_scope_prevents_completion",)
    if mode is ExecutionMode.ECONOMICAL and checkpoint is not None:
        missing = checkpoint.missing_fields()
        if not missing:
            return RunExitDecision("checkpoint", False, False, True, defects)
        defects = (*defects, *(f"checkpoint_missing:{field}" for field in missing))
    return RunExitDecision("continue", False, False, False, defects)


@dataclass(frozen=True)
class ModeSwitchDecision:
    action: str
    mode_record: ModeRecord
    may_apply_next_wave: bool
    defects: tuple[str, ...] = ()


def decide_mode_switch(
    current_record: ModeRecord,
    target_mode: ExecutionMode,
    *,
    explicit_request: bool,
    active_writer_count: int = 0,
    active_writers_checkpointed: bool = False,
    integration_unchanged: bool = True,
    ownership_reconciled: bool = True,
    evidence_preserved: bool = True,
) -> ModeSwitchDecision:
    """Apply an explicit mode change only after the dispatch-wave barrier."""

    if active_writer_count < 0:
        raise ValueError("active_writer_count must not be negative")
    if not explicit_request:
        return ModeSwitchDecision("keep_mode", current_record, False)
    if target_mode is current_record.canonical_mode:
        return ModeSwitchDecision("already_selected", current_record, False)

    defects = []
    if active_writer_count and not active_writers_checkpointed:
        defects.append("active_writers_not_checkpointed")
    if not integration_unchanged:
        defects.append("integration_checkout_changed")
    if not ownership_reconciled:
        defects.append("ownership_not_reconciled")
    if not evidence_preserved:
        defects.append("candidate_evidence_not_preserved")
    if defects:
        return ModeSwitchDecision(
            "await_switch_barrier", current_record, False, tuple(defects)
        )

    switched_record = replace(
        current_record,
        canonical_mode=target_mode,
        mode_origin=ModeOrigin.EXPLICIT,
    )
    return ModeSwitchDecision("switch_next_wave", switched_record, True)
