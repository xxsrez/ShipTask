"""Observable reference model for Issue Grinder hard invariants.

The harness models external decisions and ordered effects only. It is not a
runtime orchestration engine and does not inspect Strategic Explainer internals.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SafeAction:
    action_id: str
    material: bool = True
    in_scope: bool = True
    authorized: bool = True
    primary_source_verified: bool = True

    @property
    def runnable(self) -> bool:
        return (
            self.material
            and self.in_scope
            and self.authorized
            and self.primary_source_verified
        )

    @property
    def needs_verification(self) -> bool:
        return (
            self.material
            and self.in_scope
            and self.authorized
            and not self.primary_source_verified
        )


@dataclass(frozen=True)
class BlockerReport:
    stopped_work: str = ""
    primary_cause: str = ""
    blocking_reasons: tuple[str, ...] = ()
    checkpoint: str = ""
    unverified_work: str = ""
    impact: str = ""
    user_action: str = ""
    resume_condition: str = ""

    def missing_fields(self) -> tuple[str, ...]:
        missing = tuple(
            name
            for name in (
                "stopped_work",
                "primary_cause",
                "checkpoint",
                "unverified_work",
                "impact",
                "user_action",
                "resume_condition",
            )
            if not getattr(self, name).strip()
        )
        if not self.blocking_reasons or any(
            not reason.strip() for reason in self.blocking_reasons
        ):
            return (*missing, "blocking_reasons")
        return missing


@dataclass(frozen=True)
class BlockerReasonAnswer:
    reason: str = ""
    blocks_goal_because: str = ""
    agent_cannot_resolve_because: str = ""
    goal_value: str = ""

    def missing_fields(self) -> tuple[str, ...]:
        return tuple(
            name
            for name in (
                "reason",
                "blocks_goal_because",
                "agent_cannot_resolve_because",
                "goal_value",
            )
            if not getattr(self, name).strip()
        )


@dataclass(frozen=True)
class BlockerContext:
    preflight_actions: tuple[SafeAction, ...] = ()
    explanation_actions: tuple[SafeAction, ...] = ()
    goal_active: bool = False
    platform_blocker_audit_passed: bool = True


@dataclass(frozen=True)
class BlockerDecision:
    action: str
    events: tuple[str, ...]
    may_publish: bool
    may_stop: bool
    may_update_goal_blocked: bool
    defects: tuple[str, ...] = ()


@dataclass(frozen=True)
class WriterPacket:
    owner: str
    prepared: bool
    admission_receipt_valid: bool
    implementation_dispatched: bool = False
    task_owned_commit: bool = False


@dataclass(frozen=True)
class WriterWaveDecision:
    action: str
    events: tuple[str, ...]
    may_dispatch_implementation: bool
    may_fan_in: bool
    may_write_lifecycle: bool
    defects: tuple[str, ...] = ()


@dataclass(frozen=True)
class ExistingWorkArtifact:
    artifact_id: str
    scope_relation: str
    owner_state: str
    integrated: bool = False


@dataclass(frozen=True)
class StartupRecoveryDecision:
    action: str
    artifact_ids: tuple[str, ...]
    may_prepare_fresh: bool
    may_resume: bool


def decide_startup_recovery(
    artifacts: tuple[ExistingWorkArtifact, ...],
    *,
    inventory_completed: bool,
) -> StartupRecoveryDecision:
    """Choose packet-level recovery before any fresh implementation setup."""

    if not inventory_completed:
        return StartupRecoveryDecision(
            action="inspect_existing_work",
            artifact_ids=(),
            may_prepare_fresh=False,
            may_resume=False,
        )

    for artifact in artifacts:
        if artifact.scope_relation not in {"exact", "ambiguous", "unrelated"}:
            raise ValueError(
                f"unsupported artifact scope relation: {artifact.scope_relation}"
            )
        if artifact.owner_state not in {"active", "quiescent", "unknown"}:
            raise ValueError(f"unsupported artifact owner state: {artifact.owner_state}")

    exact = tuple(item for item in artifacts if item.scope_relation == "exact")
    unfinished = tuple(item for item in exact if not item.integrated)
    if len(unfinished) > 1:
        return StartupRecoveryDecision(
            action="reconcile_existing_work",
            artifact_ids=tuple(item.artifact_id for item in unfinished),
            may_prepare_fresh=False,
            may_resume=False,
        )
    if unfinished:
        artifact = unfinished[0]
        if artifact.owner_state == "active":
            action = "continue_via_active_owner"
            may_resume = False
        elif artifact.owner_state == "quiescent":
            action = "resume_checkpoint"
            may_resume = True
        else:
            action = "resolve_ownership"
            may_resume = False
        return StartupRecoveryDecision(
            action=action,
            artifact_ids=(artifact.artifact_id,),
            may_prepare_fresh=False,
            may_resume=may_resume,
        )
    if exact:
        return StartupRecoveryDecision(
            action="reuse_integrated_result",
            artifact_ids=tuple(item.artifact_id for item in exact),
            may_prepare_fresh=False,
            may_resume=False,
        )

    ambiguous = tuple(
        item for item in artifacts if item.scope_relation == "ambiguous"
    )
    if ambiguous:
        return StartupRecoveryDecision(
            action="resolve_artifact_scope",
            artifact_ids=tuple(item.artifact_id for item in ambiguous),
            may_prepare_fresh=False,
            may_resume=False,
        )
    return StartupRecoveryDecision(
        action="prepare_fresh",
        artifact_ids=(),
        may_prepare_fresh=True,
        may_resume=False,
    )


def decide_writer_wave(
    packets: tuple[WriterPacket, ...],
    *,
    integration_snapshot_valid: bool,
    integration_unchanged: bool,
) -> WriterWaveDecision:
    """Apply the two-phase writer barrier before dispatch and fan-in."""

    events = ["writer_wave"]
    if not packets:
        return _writer_wave_stop("no_writer_packets", events)
    if not integration_snapshot_valid:
        return _writer_wave_stop("invalid_integration_snapshot", events)
    events.append("integration_snapshot_valid")

    invalid_dispatch = tuple(
        packet.owner
        for packet in packets
        if packet.implementation_dispatched
        and (not packet.prepared or not packet.admission_receipt_valid)
    )
    if invalid_dispatch:
        return _writer_wave_stop(
            "dispatch_without_admission",
            events,
            *(f"owner:{owner}" for owner in invalid_dispatch),
        )

    missing_prepare = tuple(packet.owner for packet in packets if not packet.prepared)
    if missing_prepare:
        return _writer_wave_stop(
            "writer_not_prepared",
            events,
            *(f"owner:{owner}" for owner in missing_prepare),
        )
    events.append("all_writers_prepared")

    missing_admission = tuple(
        packet.owner for packet in packets if not packet.admission_receipt_valid
    )
    if missing_admission:
        return WriterWaveDecision(
            action="await_admission",
            events=tuple((*events, "admission_pending")),
            may_dispatch_implementation=False,
            may_fan_in=False,
            may_write_lifecycle=False,
            defects=tuple(f"owner:{owner}" for owner in missing_admission),
        )
    events.append("all_admissions_valid")

    if not all(packet.implementation_dispatched for packet in packets):
        events.append("authorize_implementation_dispatch")
        return WriterWaveDecision(
            action="dispatch_implementation",
            events=tuple(events),
            may_dispatch_implementation=True,
            may_fan_in=False,
            may_write_lifecycle=False,
        )
    events.append("implementation_dispatched")

    if not integration_unchanged:
        return _writer_wave_stop("integration_checkout_changed", events)
    events.append("integration_checkout_unchanged")

    missing_commit = tuple(
        packet.owner for packet in packets if not packet.task_owned_commit
    )
    if missing_commit:
        return WriterWaveDecision(
            action="await_task_owned_commits",
            events=tuple((*events, "commit_pending")),
            may_dispatch_implementation=False,
            may_fan_in=False,
            may_write_lifecycle=False,
            defects=tuple(f"owner:{owner}" for owner in missing_commit),
        )

    events.append("fan_in_ready")
    return WriterWaveDecision(
        action="fan_in",
        events=tuple(events),
        may_dispatch_implementation=False,
        may_fan_in=True,
        may_write_lifecycle=False,
    )


def decide_blocker(
    context: BlockerContext,
    report: BlockerReport,
    *,
    reason_answers: tuple[BlockerReasonAnswer, ...] = (),
    communication_mode: str = "ordinary",
    explainer_outcome: str = "ready",
) -> BlockerDecision:
    """Run candidate blocker through explanation and reflection gates."""

    if communication_mode not in {"ordinary", "native"}:
        raise ValueError(f"unsupported communication mode: {communication_mode}")
    if explainer_outcome not in {"ready", "caller_error", "technical_error"}:
        raise ValueError(f"unsupported explainer outcome: {explainer_outcome}")

    events = ["candidate_blocker", "preflight_reflection"]
    runnable = _first(context.preflight_actions, "runnable")
    if runnable:
        events.append(f"continue:{runnable.action_id}")
        return _nonterminal("continue_work", events, "preflight_runnable_work")

    unverified = _first(context.preflight_actions, "needs_verification")
    if unverified:
        events.append(f"verify:{unverified.action_id}")
        return _nonterminal("verify_safe_action", events, "unverified_safe_action")

    if communication_mode == "ordinary" and explainer_outcome == "caller_error":
        events.append("repair_explainer_call")
        return _nonterminal("repair_explainer_call", events, "explainer_caller_error")

    if communication_mode == "ordinary" and explainer_outcome == "technical_error":
        events.extend(("explainer_technical_error", "communication:native"))
        effective_mode = "native"
    else:
        effective_mode = communication_mode
        events.append(f"communication:{effective_mode}")

    events.extend(("explanation_ready", "post_explanation_reflection"))

    runnable = _first(context.explanation_actions, "runnable")
    if runnable:
        events.append(f"continue:{runnable.action_id}")
        return _nonterminal(
            "continue_work", events, "explanation_revealed_runnable_work"
        )

    unverified = _first(context.explanation_actions, "needs_verification")
    if unverified:
        events.append(f"verify:{unverified.action_id}")
        return _nonterminal("verify_safe_action", events, "unverified_safe_action")

    missing = report.missing_fields()
    if missing:
        action = "repair_explainer_report" if effective_mode == "ordinary" else "repair_native_report"
        events.append(action)
        return BlockerDecision(
            action=action,
            events=tuple(events),
            may_publish=False,
            may_stop=False,
            may_update_goal_blocked=False,
            defects=tuple(f"missing_report_field:{name}" for name in missing),
        )

    reason_defects = _reason_answer_defects(report, reason_answers)
    if reason_defects:
        action = (
            "repair_explainer_reason_answers"
            if effective_mode == "ordinary"
            else "repair_native_reason_answers"
        )
        events.append(action)
        return BlockerDecision(
            action=action,
            events=tuple(events),
            may_publish=False,
            may_stop=False,
            may_update_goal_blocked=False,
            defects=reason_defects,
        )

    events.append("blocker_reason_answers_ready")
    events.append("publish_blocker_report")
    events.extend(
        f"publish_blocker_reason:{index}"
        for index, _ in enumerate(report.blocking_reasons, start=1)
    )
    if context.goal_active and not context.platform_blocker_audit_passed:
        events.extend(("goal_block_pending_audit", "stop"))
        return BlockerDecision(
            action="terminal_blocker",
            events=tuple(events),
            may_publish=True,
            may_stop=True,
            may_update_goal_blocked=False,
            defects=("platform_blocker_audit_pending",),
        )

    if context.goal_active:
        events.append("update_goal:blocked")
    events.append("stop")
    return BlockerDecision(
        action="terminal_blocker",
        events=tuple(events),
        may_publish=True,
        may_stop=True,
        may_update_goal_blocked=context.goal_active,
    )


def decide_goal_creation(
    *,
    explicit_run: bool,
    active_issue_count: int,
    compatible_goal_exists: bool,
    same_run_continuity: bool = False,
) -> str:
    if active_issue_count < 0:
        raise ValueError("active_issue_count must be non-negative")
    if compatible_goal_exists:
        if same_run_continuity:
            return "reuse_goal"
        if explicit_run and active_issue_count > 1:
            return "goal_continuity_required"
        return "no_goal"
    if explicit_run and active_issue_count > 1:
        return "create_goal"
    return "no_goal"


def decide_finalization(
    *, active_issue_count: int, material_action_available: bool
) -> str:
    if active_issue_count < 0:
        raise ValueError("active_issue_count must be non-negative")
    if active_issue_count:
        return "continue_scope"
    if material_action_available:
        return "continue_work"
    return "complete"


def decide_transition(
    *,
    source_status: str,
    target_status: str,
    comment_committed: bool = False,
    comment_read_back: bool = False,
    observed_status: str | None = None,
) -> str:
    if source_status == "Backlog" or target_status == "Backlog":
        return "reject_backlog_mutation"
    if source_status == "To Do" and target_status == "In Progress":
        return "transition_status" if observed_status != target_status else "transition_complete"
    if (source_status, target_status) not in {
        ("In Progress", "In Review"),
        ("In Review", "In Progress"),
        ("In Review", "Done"),
    }:
        return "reject_transition"
    if not comment_committed:
        return "publish_comment"
    if not comment_read_back:
        return "read_back_comment"
    if observed_status == target_status:
        return "transition_complete"
    if observed_status is None:
        return "reconcile_status"
    return "transition_status"


def decide_environment_effect(
    *,
    explicit_run: bool,
    target: str | None,
    provider_operation_label: str | None = None,
) -> str:
    if not explicit_run:
        return "ordinary_authority_only"
    if target is None:
        return "resolve_uat_before_effect"
    # Provider labels describe the generic hosted operation, not the project's
    # environment identity. In particular, a provider may call every public
    # deployment "production" while the exact project target is proven UAT.
    _ = provider_operation_label
    normalized = target.casefold().replace("-", " ").strip()
    if "prod" in normalized or "production" in normalized:
        return "reject_production"
    if normalized in {"uat", "public uat", "staging", "stage", "test"}:
        return "perform_nonproduction_effect"
    return "resolve_environment_before_effect"


def decide_recovery(
    *,
    previous_progress_fingerprint: str | None,
    current_progress_fingerprint: str,
    fallback_available: bool,
) -> str:
    if previous_progress_fingerprint != current_progress_fingerprint:
        return "continue_with_changed_input"
    if fallback_available:
        return "use_fallback"
    return "candidate_blocker"


def decide_stored_permission(
    *,
    persisted: bool,
    same_project: bool,
    same_category: bool,
    target_production: bool,
) -> str:
    if target_production:
        return "reject_production"
    if persisted and same_project and same_category:
        return "authorize_exact_category"
    return "request_permission"


def _first(actions: tuple[SafeAction, ...], attribute: str) -> SafeAction | None:
    return next((action for action in actions if getattr(action, attribute)), None)


def _reason_answer_defects(
    report: BlockerReport,
    reason_answers: tuple[BlockerReasonAnswer, ...],
) -> tuple[str, ...]:
    reasons = tuple(report.blocking_reasons)
    defects: list[str] = []
    if len(set(reasons)) != len(reasons):
        defects.append("duplicate_blocking_reason")

    answers_by_reason: dict[str, list[BlockerReasonAnswer]] = {}
    for answer in reason_answers:
        answers_by_reason.setdefault(answer.reason, []).append(answer)

    for reason in reasons:
        matches = answers_by_reason.get(reason, [])
        if not matches:
            defects.append(f"missing_reason_answer:{reason}")
            continue
        if len(matches) > 1:
            defects.append(f"duplicate_reason_answer:{reason}")
            continue
        defects.extend(
            f"missing_reason_answer_field:{reason}:{field}"
            for field in matches[0].missing_fields()
        )

    for reason in answers_by_reason:
        if reason not in reasons:
            defects.append(f"unexpected_reason_answer:{reason}")
    return tuple(defects)


def _nonterminal(action: str, events: list[str], defect: str) -> BlockerDecision:
    return BlockerDecision(
        action=action,
        events=tuple(events),
        may_publish=False,
        may_stop=False,
        may_update_goal_blocked=False,
        defects=(defect,),
    )


def _writer_wave_stop(
    defect: str,
    events: list[str],
    *details: str,
) -> WriterWaveDecision:
    return WriterWaveDecision(
        action="reconcile_writer_wave",
        events=tuple((*events, "writer_wave_stopped")),
        may_dispatch_implementation=False,
        may_fan_in=False,
        may_write_lifecycle=False,
        defects=(defect, *details),
    )
