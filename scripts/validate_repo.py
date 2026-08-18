#!/usr/bin/env python3
"""Validate the portable ShipTask repository without third-party packages."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENTS_FILE = ROOT / "AGENTS.md"
SKILL_DIR = ROOT / "ship-tasks"
SKILL_FILE = SKILL_DIR / "SKILL.md"
OPENAI_FILE = SKILL_DIR / "agents" / "openai.yaml"
REPORT_REFERENCE = SKILL_DIR / "references" / "delivery-report.md"
RUN_REPORT_REFERENCE = SKILL_DIR / "references" / "run-report.md"
AUTONOMY_REFERENCE = SKILL_DIR / "references" / "autonomy-and-release.md"
MEMORY_REFERENCE = SKILL_DIR / "references" / "project-memory.md"
DOCS_INDEX = ROOT / "docs" / "README.md"
SPEC_FILE = ROOT / "docs" / "specs" / "ship-tasks.md"
ADAPTER_FILE = ROOT / "docs" / "reference" / "task-manager-adapter.md"
DECISION_FILE = ROOT / "docs" / "decisions" / "0001-task-manager-only.md"
REPORT_DECISION_FILE = (
    ROOT / "docs" / "decisions" / "0002-managed-delivery-report-in-task.md"
)
COMMENT_REPORT_DECISION_FILE = (
    ROOT / "docs" / "decisions" / "0003-delivery-reports-as-task-comments.md"
)
AUTONOMY_DECISION_FILE = (
    ROOT / "docs" / "decisions" / "0004-autonomous-continuation-and-release-authority.md"
)
AUTO_ACCEPTANCE_DECISION_FILE = (
    ROOT / "docs" / "decisions" / "0005-automatic-terminal-acceptance.md"
)
POLICY_MEMORY_DECISION_FILE = (
    ROOT / "docs" / "decisions" / "0007-delivery-policy-and-project-memory.md"
)
PLUGIN_DISTRIBUTION_DECISION_FILE = (
    ROOT / "docs" / "decisions" / "0008-plugin-only-runtime-distribution.md"
)
TERMINAL_CAPABILITY_DECISION_FILE = (
    ROOT / "docs" / "decisions" / "0009-terminal-report-capability-preflight.md"
)
BLOCKER_REPORT_DECISION_FILE = (
    ROOT / "docs" / "decisions" / "0010-blocker-analysis-and-human-run-report.md"
)

REQUIRED_FILES = (
    ROOT / "README.md",
    AGENTS_FILE,
    ROOT / ".gitignore",
    ROOT / ".gitattributes",
    SKILL_FILE,
    OPENAI_FILE,
    REPORT_REFERENCE,
    RUN_REPORT_REFERENCE,
    AUTONOMY_REFERENCE,
    MEMORY_REFERENCE,
    DOCS_INDEX,
    SPEC_FILE,
    ADAPTER_FILE,
    DECISION_FILE,
    REPORT_DECISION_FILE,
    COMMENT_REPORT_DECISION_FILE,
    AUTONOMY_DECISION_FILE,
    AUTO_ACCEPTANCE_DECISION_FILE,
    POLICY_MEMORY_DECISION_FILE,
    PLUGIN_DISTRIBUTION_DECISION_FILE,
    TERMINAL_CAPABILITY_DECISION_FILE,
    BLOCKER_REPORT_DECISION_FILE,
)

FORBIDDEN_SKILL_PATTERNS = {
    "ExampleNotes": re.compile(r"mind\s*diary", re.IGNORECASE),
    "Sites": re.compile(r"\bsites\b", re.IGNORECASE),
    "legacy skill name": re.compile(
        r"ship-(?:lin" r"ear|work)-release", re.IGNORECASE
    ),
}

RETIRED_PROVIDER_RE = re.compile("lin" + "ear", re.IGNORECASE)
SKILL_GENERATION_RE = re.compile(
    r"(?:ship[- ]?tasks|shiptask)\s*-?\s*v\d+", re.IGNORECASE
)

LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_frontmatter(errors: list[str], text: str) -> None:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        fail(errors, "ship-tasks/SKILL.md must start with YAML frontmatter")
        return
    try:
        closing = lines.index("---", 1)
    except ValueError:
        fail(errors, "ship-tasks/SKILL.md frontmatter is not closed")
        return

    keys: list[str] = []
    for line in lines[1:closing]:
        match = re.match(r"^([a-z_][a-z0-9_-]*):(?:\s|$)", line)
        if match:
            keys.append(match.group(1))
    if keys != ["name", "description"]:
        fail(
            errors,
            "SKILL.md frontmatter must contain only name and description, in order",
        )
    if "name: ship-tasks" not in "\n".join(lines[1:closing]):
        fail(errors, "SKILL.md name must be ship-tasks")
    if len(lines) > 500:
        fail(errors, f"SKILL.md is too long for runtime context: {len(lines)} lines")


def validate_skill(errors: list[str]) -> None:
    text = SKILL_FILE.read_text(encoding="utf-8")
    validate_frontmatter(errors, text)

    frontmatter = text.split("---", 2)[1] if text.count("---") >= 2 else ""
    for fragment in (
        "$ship-tasks",
        "по естественным просьбам выполнить, исправить или довести",
        "текущий Project/Release/scope",
        "создать одну Task и сразу начать",
        "single create-and-deliver, а не backlog capture",
        "project memory",
        "Bare $ship-tasks запускает batch",
        "exact Task — single без Goal",
        "Не использовать для чтения",
        "backlog capture",
    ):
        if fragment not in frontmatter:
            fail(errors, f"SKILL.md description is missing trigger contract {fragment!r}")

    if "[TODO" in text or "TODO:" in text:
        fail(errors, "SKILL.md contains a template TODO")
    if "Task Manager" not in text:
        fail(errors, "SKILL.md must use Task Manager as its only task source")
    for label, pattern in FORBIDDEN_SKILL_PATTERNS.items():
        match = pattern.search(text)
        if match:
            line = text.count("\n", 0, match.start()) + 1
            fail(errors, f"SKILL.md contains {label} residue at line {line}")

    metadata = OPENAI_FILE.read_text(encoding="utf-8")
    required_fragments = (
        'display_name: "Ship Tasks"',
        'short_description: "Доставить Task Manager scope по project context"',
        "$ship-tasks",
        'value: "task-manager"',
        "allow_implicit_invocation: true",
    )
    for fragment in required_fragments:
        if fragment not in metadata:
            fail(errors, f"agents/openai.yaml is missing {fragment!r}")


def validate_workflow_contract(errors: list[str]) -> None:
    agents_text = AGENTS_FILE.read_text(encoding="utf-8")
    for fragment in (
        "## Definition of done для изменения skill",
        "Exact repository scope закоммичен",
        "local `HEAD` совпадает с",
        "все три критерия",
        "Srez Marketplace/plugins/task-manager/skills/ship-tasks",
        "task-manager@srez-marketplace",
        "installed cache",
        "installed/enabled",
        "Standalone user-level каталог `~/.codex/skills/ship-tasks` должен",
        "fresh `skills/list` не должен возвращать отдельный user skill",
        "не удаляются вручную",
    ):
        if fragment not in agents_text:
            fail(errors, f"AGENTS.md is missing delivery DoD contract {fragment!r}")

    required_skill_fragments = (
        "Классифицировать intent до mutations",
        "Bare `$ship-tasks`",
        "`single` требует ровно одну canonical",
        "`single create-and-deliver`",
        "не завершать flow после одного `create_task`",
        "exact Task, только что",
        "перевести её в `In Progress`",
        "`memory-maintenance`",
        "project-memory reference",
        "Exact selector в текущем prompt выше memory default",
        "Task Manager adapter",
        "Создать Goal только для batch",
        "В `single`, `memory-maintenance` и `non-delivery` не вызывать Goal tools",
        "Любая `In Review` Task означает `completion-remains`",
        "per-Task targeted gate",
        "review-batch gate",
        "status-reconciliation",
        "active write target равен `1`",
        "Не начинать новую Task, если занятые lanes",
        "run-report reference",
        "finalization pass",
        "Blocker остаётся blocker до устранения",
        "SHIPTASK RUN REPORT",
        "delivery-report reference",
        "published/read-back `COMPLETED`",
        "Никогда не писать",
        "autonomy and release reference",
        "Не задавать пользователю вопрос",
        "`deferred`",
        "`runnable_count > 0`",
        "## Никогда не требовать ручную приёмку",
        "автоматически принять exact",
        "superseded historical evidence",
        "Никогда не переводить Goal в `blocked` по этой причине",
        "verified non-production target",
        "Никогда не выполнять production release",
        "Осмыслить и завершить по mode",
    )
    required_spec_fragments = (
        "### 1.1 Слои ответственности",
        "### 1.2 Классификация intent и execution mode",
        "Bare `$ship-tasks`",
        "`single` (`create-and-deliver`)",
        "не является backlog",
        "только что созданная самим workflow",
        "только затем начинать",
        "`memory-maintenance`",
        "приоритет над memory default",
        "Обязательный Goal только для batch",
        "`single`, `memory-maintenance` и `non-delivery` не вызывают",
        "### 5.3 Terminal invariant и automatic acceptance",
        "### 6.1 Двухуровневая verification",
        "`active_write_target` и `batch_target` — разные величины",
        "status-reconciliation barrier",
        "начинать следующую `To Do` запрещено",
        "### 9.3 Осмысленная финализация и terminal interaction report",
        "Finalization pass обязан",
        "Blocker считается существующим до фактического устранения",
        "SHIPTASK RUN REPORT",
        "Не запускать полный дорогой project gate для каждой Task",
        "Failed batch gate сначала локализовать",
        "final review batch прошёл gate",
        "### 9.1 Delivery report как Task comment",
        "обязательный completion report",
        "Никогда не записывать report в `description`",
        "### 5.4 Autonomous continuation и task-local defer",
        "### 5.5 Environment и release authority",
        "`production-approval-required`",
        "одну consolidated decision queue",
        "blocking input запрещён",
        "non-blocking final finding",
        "не блокировать batch Goal ожиданием",
        "Automatic terminal policy не настраивается Project",
        "superseded historical evidence",
        "не переводить Goal в `blocked` по этой причине",
        "Reopen исходной Task",
    )

    for path, fragments in (
        (SKILL_FILE, required_skill_fragments),
        (SPEC_FILE, required_spec_fragments),
    ):
        text = path.read_text(encoding="utf-8")
        for fragment in fragments:
            if fragment not in text:
                fail(
                    errors,
                    f"{path.relative_to(ROOT)} is missing workflow contract {fragment!r}",
                )

    report_text = REPORT_REFERENCE.read_text(encoding="utf-8")
    for fragment in (
        "Delivery report как Task comment",
        "native comment-create operation",
        "Не менять `description`",
        "Report key: shiptask/",
        "`not-available`",
        "`write-outcome-unknown`",
        "блокирует `Done` affected",
        "COMPLETED",
        "Не публиковать `ACCEPTANCE READY`",
        "REWORK REQUIRED",
        "Confidence: CONFIRMED | PROBABLE | UNKNOWN",
    ):
        if fragment not in report_text:
            fail(errors, f"delivery-report reference is missing {fragment!r}")

    run_report_text = RUN_REPORT_REFERENCE.read_text(encoding="utf-8")
    for fragment in (
        "Осмысленная финализация и ShipTask run report",
        "Не выбирать terminal outcome по последнему tool result",
        "Blocker — фактическое условие",
        "meaningful progress был возможен",
        "Глубокий компактный отчёт",
        "SHIPTASK RUN REPORT",
        "Итог и статус",
        "Почему так",
        "Подтверждение",
        "Осталось / следующий шаг",
        "После status write финальный ответ должен отражать фактический Goal status",
    ):
        if fragment not in run_report_text:
            fail(errors, f"run-report reference is missing {fragment!r}")

    autonomy_text = AUTONOMY_REFERENCE.read_text(encoding="utf-8")
    for fragment in (
        "Decision ladder",
        "Не задавать пользователю вопрос посреди runnable queue",
        "runnable_count = actionable To Do",
        "blocking input",
        "Automatic acceptance",
        "Stale acceptance context",
        "superseded historical evidence",
        "не может переопределить",
        "current skill",
        "Reason `acceptance-required` запрещён",
        "Deferred Task",
        "обязательно опубликовать",
        "Non-production release",
        "Production release требует explicit user approval",
        "production-approval-required",
        "Deferred-only handoff",
        "Finalization analysis and self-recovery",
        "Terminal run report",
        "SHIPTASK RUN REPORT",
        "Blocker остаётся blocker до устранения",
        "meaningful progress ещё возможен",
    ):
        if fragment not in autonomy_text:
            fail(errors, f"autonomy reference is missing {fragment!r}")

    memory_text = MEMORY_REFERENCE.read_text(encoding="utf-8")
    for fragment in (
        "Project memory contract",
        "Граница ответственности",
        "Поиск и приоритет источников",
        "Логическая схема",
        "Bootstrap и update",
        "Проверка перед delivery",
        "TASK CONTEXT ALARM",
        "Ограничения переносимости",
        "current_scope",
        "Task status, `version`",
        "только по явной просьбе",
        "не обещает cross-surface visibility",
    ):
        if fragment not in memory_text:
            fail(errors, f"project-memory reference is missing {fragment!r}")

    for path in (SKILL_FILE, SPEC_FILE, REPORT_REFERENCE):
        text = path.read_text(encoding="utf-8")
        for forbidden in (
            "SHIPTASK DELIVERY REPORT: START",
            "SHIPTASK DELIVERY REPORT: END",
            "managed delivery-report block",
        ):
            if forbidden in text:
                fail(
                    errors,
                    f"{path.relative_to(ROOT)} contains retired description-report contract {forbidden!r}",
                )

    for path in (SKILL_FILE, SPEC_FILE, REPORT_REFERENCE, AUTONOMY_REFERENCE):
        text = path.read_text(encoding="utf-8")
        for forbidden in (
            "По умолчанию acceptance — явное решение пользователя",
            "По умолчанию acceptance является явным решением пользователя",
            "После authorized acceptance",
            "zero unaccepted review-ready candidates",
            "Публиковать `ACCEPTANCE READY` только",
            "acceptance-ready report",
        ):
            if forbidden in text:
                fail(
                    errors,
                    f"{path.relative_to(ROOT)} contains retired human-acceptance contract {forbidden!r}",
                )

    decision_text = AUTO_ACCEPTANCE_DECISION_FILE.read_text(encoding="utf-8")
    for fragment in (
        "более старую memory-запись",
        "cached project context superseded historical",
        "не создаёт current authority, blocker или decision queue",
        "заблокированного только ручной приёмкой",
    ):
        if fragment not in decision_text:
            fail(errors, f"ADR-0005 is missing stale-context guard {fragment!r}")

    adapter_text = ADAPTER_FILE.read_text(encoding="utf-8")
    for fragment in (
        "только техническую границу",
        "Adapter responsibility",
        "не выбирает business scope",
        "Minimal read contract",
        "Identity and capability invariants",
        "Write and concurrency invariants",
        "current Task `version`",
        "Не повторять `create_task`",
        "Task Manager state доказывает только собственную projection",
    ):
        if fragment not in adapter_text:
            fail(errors, f"Task Manager adapter is missing compatibility contract {fragment!r}")

    decision_text = POLICY_MEMORY_DECISION_FILE.read_text(encoding="utf-8")
    for fragment in (
        "Task Manager skill  -> технический adapter",
        "ShipTask skill      -> intent routing и business delivery policy",
        "Project Memories    -> current scope и project-specific profile",
        "`single` — ровно одна",
        "`create-and-deliver` intent",
        "`batch` — Project, Release",
        "пишет memory только по явной просьбе пользователя",
    ):
        if fragment not in decision_text:
            fail(errors, f"ADR-0007 is missing architecture contract {fragment!r}")

    decision_text = PLUGIN_DISTRIBUTION_DECISION_FILE.read_text(encoding="utf-8")
    for fragment in (
        "Единственная runtime installation",
        "task-manager@srez-marketplace",
        "~/.codex/skills/ship-tasks",
        "не должен существовать",
        "task-manager:ship-tasks",
        "Marketplace snapshot и installed cache",
        "не удаляются вручную",
        "fresh Codex session",
    ):
        if fragment not in decision_text:
            fail(errors, f"ADR-0008 is missing plugin-only distribution contract {fragment!r}")

    decision_text = TERMINAL_CAPABILITY_DECISION_FILE.read_text(encoding="utf-8")
    for fragment in (
        "Статус: superseded",
        "отменено",
        "не является текущим runtime contract",
    ):
        if fragment not in decision_text:
            fail(errors, f"ADR-0009 is missing superseded marker {fragment!r}")

    decision_text = BLOCKER_REPORT_DECISION_FILE.read_text(encoding="utf-8")
    for fragment in (
        "comment lifecycle из",
        "Перед любым terminal outcome выполнить finalization pass",
        "Blocker остаётся blocker до фактического устранения",
        "глубоким, но компактным",
        "process diary",
    ):
        if fragment not in decision_text:
            fail(errors, f"ADR-0010 is missing blocker-analysis contract {fragment!r}")

    for path in (
        SKILL_FILE,
        SPEC_FILE,
        RUN_REPORT_REFERENCE,
        AUTONOMY_REFERENCE,
        BLOCKER_REPORT_DECISION_FILE,
        ROOT / "docs" / "overview.md",
    ):
        text = path.read_text(encoding="utf-8")
        if "`blocked` запрещён" in text:
            fail(
                errors,
                f"{path.relative_to(ROOT)} conflates a blocker with terminal Goal blocked",
            )

    retired_terminal_channel_fragments = {
        SKILL_FILE: (
            "terminal-report-channel-unavailable",
            "Production approval этого не исправляет",
            "scope-wide blocker ledger",
        ),
        REPORT_REFERENCE: (
            "Это scope-wide blocker",
            "остановить новый dispatch",
        ),
        ROOT / "docs" / "guides" / "development.md": (
            "terminal-report-channel-unavailable",
            "zero Task starts, code/Git/deploy",
        ),
        SPEC_FILE: (
            "### 3.4 Mandatory terminal-report capability gate",
            "scope-wide blocker ledger",
        ),
        AUTONOMY_REFERENCE: (
            "## Shared terminal channel loss",
            "Production approval не заменяет эту capability",
        ),
    }
    for path, fragments in retired_terminal_channel_fragments.items():
        text = path.read_text(encoding="utf-8")
        for fragment in fragments:
            if fragment in text:
                fail(
                    errors,
                    f"{path.relative_to(ROOT)} contains retired terminal-channel contract {fragment!r}",
                )

    retired_create_delivery_fragments = {
        SKILL_FILE: (
            "`single` требует ровно одну canonical существующую Task",
        ),
        SPEC_FILE: (
            "Skill должен довести выбранный scope уже созданных Task Manager Tasks",
            "Обычный запуск работает с уже созданным scope",
        ),
    }
    for path, fragments in retired_create_delivery_fragments.items():
        text = path.read_text(encoding="utf-8")
        for fragment in fragments:
            if fragment in text:
                fail(
                    errors,
                    f"{path.relative_to(ROOT)} contains retired create-and-deliver contract {fragment!r}",
                )


def repository_text_files() -> list[Path]:
    paths = [ROOT / "README.md", ROOT / "AGENTS.md", OPENAI_FILE]
    paths.extend(sorted(SKILL_DIR.rglob("*.md")))
    paths.extend(sorted((ROOT / "docs").rglob("*.md")))
    paths.extend(sorted((ROOT / "scripts").rglob("*.py")))
    return paths


def validate_single_task_manager_contract(errors: list[str]) -> None:
    for path in repository_text_files():
        text = path.read_text(encoding="utf-8")
        for label, pattern in (
            ("retired task provider", RETIRED_PROVIDER_RE),
            ("numbered ShipTask generation", SKILL_GENERATION_RE),
        ):
            match = pattern.search(text)
            if match:
                line = text.count("\n", 0, match.start()) + 1
                fail(
                    errors,
                    f"{path.relative_to(ROOT)} contains {label} at line {line}",
                )


def markdown_files() -> list[Path]:
    roots = [ROOT / "README.md", ROOT / "AGENTS.md"]
    roots.extend(sorted(SKILL_DIR.rglob("*.md")))
    roots.extend(sorted((ROOT / "docs").rglob("*.md")))
    return roots


def validate_links(errors: list[str]) -> None:
    for source in markdown_files():
        text = source.read_text(encoding="utf-8")
        for raw_target in LINK_RE.findall(text):
            target = raw_target.strip().strip("<>").split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            resolved = (source.parent / target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                fail(errors, f"{source.relative_to(ROOT)} links outside repository: {target}")
                continue
            if not resolved.exists():
                fail(errors, f"{source.relative_to(ROOT)} has broken link: {target}")

    index_text = DOCS_INDEX.read_text(encoding="utf-8")
    direct_targets = {
        (DOCS_INDEX.parent / raw.strip().strip("<>").split("#", 1)[0]).resolve()
        for raw in LINK_RE.findall(index_text)
        if raw and "://" not in raw
    }
    for document in sorted((ROOT / "docs").rglob("*.md")):
        if document == DOCS_INDEX:
            continue
        if document.resolve() not in direct_targets:
            fail(errors, f"docs/README.md does not link {document.relative_to(ROOT)}")


def validate_artifacts(errors: list[str]) -> None:
    for path in ROOT.rglob("*"):
        if ".git" in path.parts:
            continue
        if path.name == "__pycache__" or path.suffix == ".pyc":
            fail(errors, f"generated Python artifact present: {path.relative_to(ROOT)}")


def main() -> int:
    errors: list[str] = []
    for path in REQUIRED_FILES:
        if not path.is_file():
            fail(errors, f"missing required file: {path.relative_to(ROOT)}")

    if not errors:
        validate_skill(errors)
        validate_workflow_contract(errors)
        validate_single_task_manager_contract(errors)
        validate_links(errors)
        validate_artifacts(errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    doc_count = len(list((ROOT / "docs").rglob("*.md")))
    print(f"OK: ShipTask repository is valid ({doc_count} documentation files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
