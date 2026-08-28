"""Executable reference model for ShipTask terminal handoff evaluations.

The harness intentionally models only observable orchestration effects.  It is
not a writing template and it does not inspect Strategic Explainer internals.
"""

from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class BlockerClaim:
    task_refs: tuple[str, ...]
    required_publication_facts: tuple[tuple[str, ...], ...]


@dataclass(frozen=True)
class HandoffContext:
    blockers: tuple[BlockerClaim, ...]
    runnable_work: tuple[str, ...] = ()
    goal_active: bool = False


@dataclass(frozen=True)
class CandidateReport:
    text: str
    factual_conflict: bool = False


@dataclass(frozen=True)
class HandoffDecision:
    action: str
    may_publish: bool
    may_stop: bool
    may_update_goal_blocked: bool
    defects: tuple[str, ...] = ()


def decide_terminal_handoff(
    context: HandoffContext,
    report: CandidateReport,
    *,
    communication_mode: str = "ordinary",
    repair_attempt: int = 0,
) -> HandoffDecision:
    """Evaluate whether ShipTask may publish and stop an unfinished selector.

    This is an observable evaluation model, not a runtime writing recipe.  A
    caller supplies the already-established blocker ledger and candidate body;
    the gate never introspects Strategic Explainer's method or source basis.
    """

    if report.factual_conflict:
        return HandoffDecision(
            action="refresh_sources",
            may_publish=False,
            may_stop=False,
            may_update_goal_blocked=False,
            defects=("factual_conflict",),
        )

    if context.runnable_work:
        return HandoffDecision(
            action="continue_work",
            may_publish=False,
            may_stop=False,
            may_update_goal_blocked=False,
            defects=("runnable_work_remains",),
        )

    if not context.blockers:
        return HandoffDecision(
            action="rebuild_blocker_ledger",
            may_publish=False,
            may_stop=False,
            may_update_goal_blocked=False,
            defects=("missing_blocker_ledger",),
        )

    report_tokens = _tokens(report.text)
    defects: list[str] = []
    for blocker in context.blockers:
        blocker_name = "+".join(blocker.task_refs)
        for index, alternatives in enumerate(blocker.required_publication_facts):
            if not any(_tokens(alternative) <= report_tokens for alternative in alternatives):
                defects.append(f"missing_blocker_fact:{blocker_name}:{index}")

    if defects:
        if communication_mode == "ordinary" and repair_attempt == 0:
            action = "request_fresh_explainer"
        elif communication_mode == "ordinary":
            action = "switch_to_native"
        else:
            action = "repair_native_report"
        return HandoffDecision(
            action=action,
            may_publish=False,
            may_stop=False,
            may_update_goal_blocked=False,
            defects=tuple(defects),
        )

    return HandoffDecision(
        action="terminal_handoff",
        may_publish=True,
        may_stop=True,
        may_update_goal_blocked=context.goal_active,
    )


def _tokens(value: str) -> frozenset[str]:
    normalized = value.casefold().replace("ё", "е")
    return frozenset(re.findall(r"[a-zа-я0-9-]+", normalized))
