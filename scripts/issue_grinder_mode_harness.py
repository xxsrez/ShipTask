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
    ECONOMICAL = "economical"


class ModeOrigin(str, Enum):
    EXPLICIT = "explicit"
    AUTOMATIC = "automatic"


class ScopeSize(str, Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    UNCERTAIN = "uncertain"


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
SOL_XHIGH = Profile("gpt-5.6-sol", "xhigh")
BALANCE_VERSION = "luna-coordinator-v1"

def require_main_profile(mode: ExecutionMode, profile: Profile) -> None:
    if mode in (ExecutionMode.BALANCE, ExecutionMode.ECONOMICAL) and profile != LUNA_MAX:
        raise ValueError("main_profile_required: gpt-5.6-luna/max")



@dataclass(frozen=True)
class RoleProfiles:
    controller: Profile
    worker: Profile
    specialist: Profile | None = None


@dataclass(frozen=True)
class ModeRecord:
    canonical_mode: ExecutionMode
    mode_origin: ModeOrigin
    initial_main_profile: Profile
    role_profiles: RoleProfiles
    initial_scope_task_count: int = 1
    mode_contract_version: str | None = None
    initial_scope_size: ScopeSize = ScopeSize.UNCERTAIN
    mode_selection_reason: str = ""


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

    ExecutionMode(record.canonical_mode)
    require_main_profile(record.canonical_mode, current_main_profile)
    if record.canonical_mode is ExecutionMode.SOLO:
        return ModeDispatchPolicy(
            issue_grinder_execution_subagents_allowed=False,
            max_active_execution_lanes=1,
            max_active_execution_subagents=0,
            execution_profile=current_main_profile,
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

    require_main_profile(mode, main_profile)
    if mode in (ExecutionMode.BALANCE, ExecutionMode.ECONOMICAL) and controller_override not in (None, LUNA_MAX):
        raise ValueError("main_profile_required: controller override cannot replace root")
    default_controller = LUNA_MAX if main_profile.is_luna else main_profile
    default_worker = LUNA_MAX
    return RoleProfiles(
        controller=controller_override or default_controller,
        worker=worker_override or default_worker,
        specialist=SOL_XHIGH if mode is ExecutionMode.BALANCE else None,
    )


def resolve_mode(
    main_profile: Profile,
    *,
    scope_task_count: int = 1,
    scope_size: ScopeSize = ScopeSize.UNCERTAIN,
    scope_assessment_reason: str = "",
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
        ExecutionMode(saved_record.canonical_mode)  # retired records fail closed
        require_main_profile(saved_record.canonical_mode, main_profile)
        if saved_record.canonical_mode is ExecutionMode.BALANCE and saved_record.mode_contract_version != BALANCE_VERSION:
            raise ValueError("legacy_balance_requires_explicit_switch")
        return saved_record

    if not isinstance(scope_task_count, int) or isinstance(scope_task_count, bool) or scope_task_count < 0:
        raise ValueError("scope_task_count must be a nonnegative resolved task count")
    # The agent supplies the semantic assessment; this oracle does not infer
    # size from task count, profile or keywords in a justification.
    assessed_size = ScopeSize(scope_size)
    if explicit_mode is None and assessed_size is ScopeSize.LARGE and not scope_assessment_reason.strip():
        raise ValueError("large scope requires a concrete assessment reason")
    canonical_mode = (
        ExecutionMode(explicit_mode) if explicit_mode is not None else
        ExecutionMode.CLASSIC if assessed_size is ScopeSize.LARGE else
        ExecutionMode.SOLO
    )
    origin = (
        ModeOrigin.EXPLICIT
        if explicit_mode is not None
        else ModeOrigin.AUTOMATIC
    )
    return ModeRecord(
        canonical_mode=canonical_mode,
        mode_origin=origin,
        mode_contract_version=BALANCE_VERSION if canonical_mode is ExecutionMode.BALANCE else None,
        initial_scope_task_count=scope_task_count,
        initial_scope_size=assessed_size,
        mode_selection_reason=(
            "explicit mode choice" if explicit_mode is not None else
            scope_assessment_reason or "large scope is not established"
        ),
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


def assess_review_wave(observation: ReviewWaveObservation) -> ReviewWaveDecision:
    """Check an independent-review envelope for modes that require it."""

    if observation.mode is ExecutionMode.SOLO:
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
    current_main_profile: Profile | None = None,
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
    target_mode = ExecutionMode(target_mode)
    if target_mode in (ExecutionMode.BALANCE, ExecutionMode.ECONOMICAL):
        if current_main_profile is None:
            raise ValueError("current_main_profile_required")
        require_main_profile(target_mode, current_main_profile)
    if target_mode is current_record.canonical_mode and not (target_mode is ExecutionMode.BALANCE and current_record.mode_contract_version != BALANCE_VERSION):
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
        mode_contract_version=BALANCE_VERSION if target_mode is ExecutionMode.BALANCE else None,
        role_profiles=normalize_profiles(current_main_profile or current_record.initial_main_profile, mode=target_mode),
    )
    return ModeSwitchDecision("switch_next_wave", switched_record, True)
