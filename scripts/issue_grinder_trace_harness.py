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
    checkpoint: str = ""
    unverified_work: str = ""
    impact: str = ""
    user_action: str = ""
    resume_condition: str = ""

    def missing_fields(self) -> tuple[str, ...]:
        return tuple(
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


def decide_blocker(
    context: BlockerContext,
    report: BlockerReport,
    *,
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

    events.append("publish_blocker_report")
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


def decide_environment_effect(*, explicit_run: bool, target: str | None) -> str:
    if not explicit_run:
        return "ordinary_authority_only"
    if target is None:
        return "resolve_uat_before_effect"
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


def _nonterminal(action: str, events: list[str], defect: str) -> BlockerDecision:
    return BlockerDecision(
        action=action,
        events=tuple(events),
        may_publish=False,
        may_stop=False,
        may_update_goal_blocked=False,
        defects=(defect,),
    )
