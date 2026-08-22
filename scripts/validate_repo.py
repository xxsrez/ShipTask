#!/usr/bin/env python3
"""Validate ShipTask structure and current behavioral invariants."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHIP_SKILL = ROOT / "ship-tasks" / "SKILL.md"
SHIP_METADATA = ROOT / "ship-tasks" / "agents" / "openai.yaml"
COMPOSER_SKILL = ROOT / "task-composer" / "SKILL.md"
COMPOSER_METADATA = ROOT / "task-composer" / "agents" / "openai.yaml"
STRATEGIC_SKILL = ROOT / "strategic-explainer" / "SKILL.md"
STRATEGIC_METADATA = ROOT / "strategic-explainer" / "agents" / "openai.yaml"
SKILL_SOURCES = ROOT / "docs" / "skills"
SOURCE_INDEX = SKILL_SOURCES / "README.md"
SHIP_REQUIREMENTS = SKILL_SOURCES / "ship-tasks" / "requirements.md"
SPEC = SKILL_SOURCES / "ship-tasks" / "architecture.md"
COMPOSER_REQUIREMENTS = SKILL_SOURCES / "task-composer" / "requirements.md"
COMPOSER_SPEC = SKILL_SOURCES / "task-composer" / "architecture.md"
STRATEGIC_REQUIREMENTS = (
    SKILL_SOURCES / "strategic-explainer" / "requirements.md"
)
STRATEGIC_SPEC = SKILL_SOURCES / "strategic-explainer" / "architecture.md"
OVERVIEW = ROOT / "docs" / "overview.md"
DOCS_INDEX = ROOT / "docs" / "README.md"
DEVELOPMENT = ROOT / "docs" / "guides" / "development.md"
REVIEW_MATRIX = (
    ROOT / "docs" / "reference" / "shiptask-review-disposition-evaluation.md"
)
STRATEGIC_EVALUATION = (
    ROOT / "docs" / "reference" / "strategic-explainer-evaluation.md"
)
COMPOSER_EVALUATION = ROOT / "docs" / "reference" / "task-composer-evaluation.md"
ADAPTER = ROOT / "docs" / "reference" / "task-manager-adapter.md"
VISION = SKILL_SOURCES / "strategic-explainer" / "product-vision.md"
REPORT = ROOT / "ship-tasks" / "references" / "delivery-report.md"
RUN_REPORT = ROOT / "ship-tasks" / "references" / "run-report.md"
AUTONOMY = ROOT / "ship-tasks" / "references" / "autonomy-and-release.md"
MEMORY = ROOT / "ship-tasks" / "references" / "project-memory.md"
HANDOFF = ROOT / "ship-tasks" / "references" / "strategic-explainer.md"
THREAD_TITLE = ROOT / "ship-tasks" / "references" / "thread-title.md"

ADR = {
    number: ROOT / "docs" / "decisions" / name
    for number, name in (
        ("0001", "0001-task-manager-only.md"),
        ("0002", "0002-managed-delivery-report-in-task.md"),
        ("0003", "0003-delivery-reports-as-task-comments.md"),
        ("0004", "0004-autonomous-continuation-and-release-authority.md"),
        ("0005", "0005-automatic-terminal-acceptance.md"),
        ("0006", "0006-delivery-comment-as-terminal-effect.md"),
        ("0007", "0007-delivery-policy-and-project-memory.md"),
        ("0008", "0008-plugin-only-runtime-distribution.md"),
        ("0009", "0009-terminal-report-capability-preflight.md"),
        ("0010", "0010-blocker-analysis-and-human-run-report.md"),
        ("0011", "0011-separate-shiptask-plugin-distribution.md"),
        ("0012", "0012-strategic-explainer-as-portable-subagent-role.md"),
        ("0013", "0013-strategic-explainer-for-shiptask-report-narratives.md"),
        ("0014", "0014-problem-first-bounded-strategic-discovery.md"),
        ("0015", "0015-single-pass-review-disposition.md"),
        ("0016", "0016-current-lifecycle-and-reporting-contract.md"),
        ("0017", "0017-constitution-first-runtime-contract.md"),
        ("0018", "0018-outcomes-not-tool-choreography.md"),
        ("0019", "0019-goal-only-for-multi-task-implementation.md"),
        (
            "0020",
            "0020-visible-acceptance-incidents-and-required-comments.md",
        ),
        (
            "0021",
            "0021-requirements-as-agent-constitution.md",
        ),
        (
            "0022",
            "0022-mandatory-independent-strategic-explainer-for-comments.md",
        ),
        (
            "0023",
            "0023-task-composer-as-planning-sibling.md",
        ),
        (
            "0024",
            "0024-adaptive-multi-agent-execution-by-default.md",
        ),
        (
            "0025",
            "0025-cost-aware-subagent-profiles.md",
        ),
    )
}

CORE_FILES = (
    ROOT / "README.md",
    ROOT / "AGENTS.md",
    ROOT / ".gitignore",
    ROOT / ".gitattributes",
    SHIP_SKILL,
    SHIP_METADATA,
    COMPOSER_SKILL,
    COMPOSER_METADATA,
    STRATEGIC_SKILL,
    STRATEGIC_METADATA,
    SPEC,
    COMPOSER_SPEC,
    STRATEGIC_SPEC,
    SOURCE_INDEX,
    SHIP_REQUIREMENTS,
    COMPOSER_REQUIREMENTS,
    STRATEGIC_REQUIREMENTS,
    OVERVIEW,
    DOCS_INDEX,
    DEVELOPMENT,
    REVIEW_MATRIX,
    COMPOSER_EVALUATION,
    STRATEGIC_EVALUATION,
    ADAPTER,
    VISION,
    REPORT,
    RUN_REPORT,
    AUTONOMY,
    MEMORY,
    HANDOFF,
    THREAD_TITLE,
    *ADR.values(),
)

# These files describe current behavior. Historical reports and superseded ADRs
# may retain old wording, but cannot act as fallback policy.
CURRENT_CONTRACT_FILES = (
    ROOT / "README.md",
    ROOT / "AGENTS.md",
    SHIP_SKILL,
    SHIP_METADATA,
    COMPOSER_SKILL,
    COMPOSER_METADATA,
    STRATEGIC_SKILL,
    STRATEGIC_METADATA,
    SPEC,
    COMPOSER_SPEC,
    STRATEGIC_SPEC,
    SOURCE_INDEX,
    SHIP_REQUIREMENTS,
    COMPOSER_REQUIREMENTS,
    STRATEGIC_REQUIREMENTS,
    OVERVIEW,
    DOCS_INDEX,
    DEVELOPMENT,
    REVIEW_MATRIX,
    COMPOSER_EVALUATION,
    STRATEGIC_EVALUATION,
    VISION,
    REPORT,
    RUN_REPORT,
    AUTONOMY,
    MEMORY,
    HANDOFF,
    THREAD_TITLE,
    ADR["0018"],
    ADR["0019"],
    ADR["0020"],
    ADR["0021"],
    ADR["0022"],
    ADR["0023"],
    ADR["0024"],
    ADR["0025"],
    ADAPTER,
)

LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def require(errors: list[str], path: Path, *terms: str) -> None:
    text = read(path)
    normalized_text = normalize(text)
    for term in terms:
        if term not in text and normalize(term) not in normalized_text:
            fail(errors, f"{relative(path)} is missing required concept {term!r}")


def forbid(errors: list[str], path: Path, *terms: str) -> None:
    text = read(path)
    for term in terms:
        if term in text:
            fail(errors, f"{relative(path)} contains retired contract {term!r}")


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def section(text: str, heading: str) -> str | None:
    """Return a Markdown section beginning at an exact heading."""
    lines = text.splitlines()
    try:
        start = lines.index(heading)
    except ValueError:
        return None
    level = len(heading) - len(heading.lstrip("#"))
    end = len(lines)
    for index in range(start + 1, len(lines)):
        match = re.match(r"^(#+)\s", lines[index])
        if match and len(match.group(1)) <= level:
            end = index
            break
    return "\n".join(lines[start:end])


def table_rows(text: str, heading: str) -> list[list[str]]:
    body = section(text, heading)
    if body is None:
        return []
    rows: list[list[str]] = []
    for line in body.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells or all(re.fullmatch(r":?-+:?", cell) for cell in cells):
            continue
        rows.append(cells)
    return rows


def validate_frontmatter(
    errors: list[str], path: Path, expected_name: str, max_lines: int
) -> None:
    text = read(path)
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        fail(errors, f"{relative(path)} must start with YAML frontmatter")
        return
    try:
        closing = lines.index("---", 1)
    except ValueError:
        fail(errors, f"{relative(path)} frontmatter is not closed")
        return

    keys = []
    for line in lines[1:closing]:
        match = re.match(r"^([a-z_][a-z0-9_-]*):(?:\s|$)", line)
        if match:
            keys.append(match.group(1))
    if keys != ["name", "description"]:
        fail(errors, f"{relative(path)} frontmatter must contain name and description")
    if f"name: {expected_name}" not in "\n".join(lines[1:closing]):
        fail(errors, f"{relative(path)} name must be {expected_name}")
    if len(lines) > max_lines:
        fail(errors, f"{relative(path)} is too long: {len(lines)} > {max_lines}")
    if "[TODO" in text or "TODO:" in text:
        fail(errors, f"{relative(path)} contains an unfinished placeholder")


def validate_ship_skill(errors: list[str]) -> None:
    validate_frontmatter(errors, SHIP_SKILL, "ship-tasks", 250)
    text = read(SHIP_SKILL)
    description = text.split("---", 2)[1] if text.count("---") >= 2 else ""

    for term in (
        "$ship-tasks",
        "Task Manager scope",
        "неявно только",
        "TM-123",
        "одного delivery-глагола недостаточно",
        "Create-and-deliver",
        "Bare invocation определяет mode по live inventory",
        "Goal нужен только для implementation/rework минимум двух Tasks",
        "backlog capture",
    ):
        if term not in description:
            fail(errors, f"ship-tasks description is missing routing concept {term!r}")

    required_sections = (
        "## 1. Выбери mode и exact scope",
        "## 2. Соблюдай обязательные требования",
        "## 3. Выполни и проверь result",
        "## 4. Разбери приёмку по текущим фактам",
        "## 5. Обеспечь человеческое объяснение",
        "## 6. Продолжай автономно и финализируй",
    )
    for heading in required_sections:
        if section(text, heading) is None:
            fail(errors, f"ship-tasks/SKILL.md is missing section {heading!r}")

    require(
        errors,
        SHIP_SKILL,
        "полный exact scope",
        "принадлежит Task Composer",
        "TASK CONTEXT ALARM",
        "Доказательство важнее выбранного способа",
        "Сбой одного выбранного способа",
        "не делает его обязательным",
        "Нельзя снижать current acceptance",
        "как обеспечить это, решает агент",
        "task-contract-conflict",
        "verified-success",
        "verified-failure",
        "verification-blocked",
        "In Review → In Progress",
        "продолжай rework в этом же run",
        "гарантированная часть current Task Manager adapter",
        "Не скрывай приёмочный инцидент",
        "немедленно сообщи в Codex chat",
        "каждые 10 минут",
        "incident ledger",
        "$ship-tasks:strategic-explainer",
        "Canonical `Backlog` не входит в delivery inventory",
        "closed selectors",
        "live selectors",
        "audit snapshot",
        "не требует approval",
        "Browser/controller/session switch — диагностика, не repair",
        "browser logistics не stop condition",
        "fresh full inventory",
        "`Duplicate` отдельно не\nисполняй",
        "После смены session и до новой implementation surface найди task-owned Git state",
        "unfinished worktree/branch существует",
        "прежний writer остановлен",
        "прими тот же artifact и продолжай",
        "active/unknown ownership не перехватывай",
        "Исполняй topology rule пользователя, иначе выбирай автоматически",
        "effective topology rule",
        "exact/relative число",
        "Root не входит в явно\nназванное число субагентов",
        "Только без применимого rule сам решай",
        "rule не подменяй молча",
        "role-scoped rule меняет только названную роль",
        "только genuinely simple packet запускай на `gpt-5.6-luna`/`max`",
        "Strategic Explainer наследуют current model/effort",
        "Luna прекращает packet без\ncorrective mutations",
        "integration\nowner на current profile без повторного cheap Luna loop",
        "`luna-escalation=not-available` без скрытой подмены Sol",
        "явный unavailable user profile не подменяй",
        "единственный integration owner",
        "владелец Goal, Task Manager\ncomments/status/version writes",
        "собственную feature branch и собственный Git worktree",
        "Один writable worktree принадлежит одному writer",
        "Только integration owner делает fan-in",
        "Общий no-subagent rule означает ноль субагентов во всём run",
        "внутренняя target/width accounting не требуется",
        "сохраняй unrelated пользовательские изменения",
        "не используй blind rollback или destructive cleanup",
        "Пока effective rule сохраняет Explainer, каждый Task Manager comment проходит отдельного",
        "Если effective rule\nотключает Explainer, сам примени тот же problem-first",
        "не переписывай текст самостоятельно",
        "Обычный `To Do → In Progress` не запускает Explainer",
        "SHIPTASK RUN REPORT",
        "[title contract](references/thread-title.md)",
        "доказанный catalog placeholder",
    )

    require(
        errors,
        THREAD_TITLE,
        "Название первой Codex task",
        "codex_app__list_threads",
        "codex_app__read_thread",
        "codex_app__set_thread_title",
        "ровно одного кандидата calling task",
        "Не\n   выбирай просто самый свежий task",
        "history не paginated",
        "Meaningful title",
        "до первой Task Manager mutation",
        "create-and-deliver ждёт create/read-back exact\nTask",
        "без `threadId`",
        "не передавай discovery candidate id",
        "task-title=renamed",
        "task-title=preserved",
        "task-title=not-available",
    )

    require(
        errors,
        SHIP_METADATA,
        'display_name: "Ship Tasks"',
        'short_description: "Доставить выбранный Task Manager scope"',
        "$ship-tasks",
        'value: "task-manager"',
        "allow_implicit_invocation: true",
        "live scope",
        "task-owned worktree/branch",
        "natural-language правила пользователя",
        "без такого правила выбери полезную delegation автоматически",
        "отдельным feature branches и Git worktrees",
        "Не ослабляй acceptance",
        "SHIPTASK RUN REPORT",
    )
    metadata = read(SHIP_METADATA)
    prompt_match = re.search(r'^\s*default_prompt:\s*"(.*)"\s*$', metadata, re.MULTILINE)
    if prompt_match is None:
        fail(errors, f"{relative(SHIP_METADATA)} is missing one-line default_prompt")
    elif len(prompt_match.group(1)) > 1024:
        fail(
            errors,
            f"{relative(SHIP_METADATA)} default_prompt exceeds App Server limit of 1024 characters",
        )


def validate_composer_skill(errors: list[str]) -> None:
    validate_frontmatter(errors, COMPOSER_SKILL, "task-composer", 180)
    require(
        errors,
        COMPOSER_SKILL,
        "$ship-tasks:task-composer",
        "planning mutations",
        "ShipTask create-and-deliver contract",
        "canonical status `Backlog`",
        "current unreleased Release",
        "bounded duplicate search",
        "Не создавай Epic с одной формальной подзадачей",
        "$ship-tasks:strategic-explainer",
        "не создавай Epic; single Task",
        "secret store",
        "live active catalog",
        "relation graph",
        "искусственный umbrella Epic",
        "Title кратко называет ожидаемый результат",
        "Type/classification выражай native Label",
        "Legacy-prefixed и clean outcome title считай одним duplicate candidate",
        "Не строй последовательную цепочку по умолчанию",
        "Unknown write outcome",
        "остановился частично",
        "planning projection",
    )
    require(
        errors,
        COMPOSER_METADATA,
        'display_name: "Task Composer"',
        'short_description: "Сформулировать и связать Task Manager задачи"',
        "$ship-tasks:task-composer",
        'value: "task-manager"',
        "live Labels",
        "реальные relations",
        "allow_implicit_invocation: true",
    )
    require(
        errors,
        COMPOSER_SPEC,
        "Статус: current Level 2 contract, 2026-08-22",
        "`TC-*` в локальных",
        "[требованиях пользователя](requirements.md)",
        "planning mutations",
        "Проверяемая trigger matrix",
        "не управляет delivery lifecycle",
        "Все новые Tasks создаются в canonical status `Backlog`",
        "текущий unreleased Release",
        "Exact duplicate не создаётся",
        "искусственный umbrella Epic",
        "Title кратко называет ожидаемый результат",
        "Task type и другая classification metadata",
        "textual prefix не является fallback",
        "legacy classification prefixes",
        "canonical classification metadata",
        "отсутствие classification prefix/suffix",
        "самую мелкую полезную иерархию",
        "$ship-tasks:strategic-explainer",
        "создание Epic не начинается; single Task",
        "не secret value",
        "Создание нового Label не разрешено",
        "Direction каждого `blocks`",
        "Unknown write outcome",
        "Task Manager read-back доказывает только planning projection",
    )
    require(
        errors,
        COMPOSER_EVALUATION,
        "observable planning result",
        "write происходит только по явному planning intent",
        "Epic problem-first",
        "независимые outcomes не сливаются",
        "Strategic Explainer",
        "блокирует только Epic create",
        "Release назначен только при однозначном current",
        "отсутствующий подходящий Label",
        "classification хранится в Label/hierarchy",
        "Есть live `Bug` Label",
        "Legacy `BUG: Исправить X` уже существует",
        "exact title `BUG: X` verbatim",
        "duplicate search предшествует create",
        "read-back подтверждает",
        "Ошибка после создания части Epic",
    )
    require(
        errors,
        ADR["0023"],
        "Task Composer как planning sibling-skill",
        "ship-tasks@srez-marketplace",
        "planning-only",
        "$ship-tasks:strategic-explainer",
        "current или explicit Release",
        "Task Manager plugin остаётся adapter-only",
    )


def validate_strategic_skill(errors: list[str]) -> None:
    validate_frontmatter(errors, STRATEGIC_SKILL, "strategic-explainer", 240)
    require(
        errors,
        STRATEGIC_SKILL,
        "problem-first модель",
        "bounded read-only sources",
        "Форма context свободна",
        "material основания отсутствуют",
        "current/accepted",
        "proposed",
        "historical",
        "source basis",
        "не придумывай варианты ради квоты",
        "decision-relevant факт не потерян",
        "готовый пользовательский текст",
        "Пиши на языке пользователя",
        "пригодный для публикации",
        "Не выполняй writes",
    )
    text = read(STRATEGIC_SKILL)
    for coupling in ("ShipTask", "Task Manager", "$ship-tasks", "TM-123"):
        if coupling in text:
            fail(errors, f"Strategic Explainer runtime is coupled to {coupling!r}")
    require(
        errors,
        STRATEGIC_METADATA,
        'display_name: "Strategic Explainer"',
        'short_description: "Связать проблему, стратегию и текущий результат"',
        "$strategic-explainer",
        "готовое объяснение на языке пользователя",
        "не превращай текст в смесь русского",
        "allow_implicit_invocation: true",
    )


TRIGGER_CASES = {
    "$ship-tasks": (
        "да",
        "mode по live inventory; Goal только для `batch-implementation`",
    ),
    "Выполни TM-123": ("да", "`single` для exact существующей Task"),
    "Доведи выбранный Task Manager Project Alpha": (
        "да",
        "mode по фактической работе; selector не создаёт Goal",
    ),
    "Выпусти выбранный Task Manager Release 0.2 на production": (
        "да",
        "`release` без Goal; production authority дана exact запросом",
    ),
    "Имплементируй все незавершённые Tasks выбранного Release 0.2": (
        "да",
        "`batch-implementation` с Goal и `subagents=auto` после live inventory",
    ),
    "Имплементируй все незавершённые Tasks выбранного Release 0.2, но без субагентов": (
        "да",
        "`batch-implementation` с Goal и `subagents=off`",
    ),
    "Доведи текущий Task Manager scope": (
        "да",
        "mode по фактической работе; Goal только при имплементации 2+ Tasks",
    ),
    "Создай ровно одну Task в Task Manager: исправить импорт, и сразу начни выполнять её": (
        "да",
        "`single create-and-deliver`",
    ),
    "Почини X сейчас": ("нет", "обычная реализация без Task Manager scope"),
    "Исправь баг в plugin": ("нет", "обычная реализация без Task Manager scope"),
    "Реализуй это изменение в коде": ("нет", "обычная реализация без Task Manager scope"),
    "Покажи статус TM-123": ("нет", "read-only Task Manager adapter"),
    "Проведи аудит TM-123": ("нет", "read-only Task Manager adapter"),
    "Создай Task в Task Manager": ("нет", "Task Composer planning write, без delivery flow"),
    "Просто добавь это в backlog": ("нет", "Task Composer backlog capture, без delivery flow"),
}


def validate_trigger_matrix(errors: list[str]) -> None:
    rows = table_rows(read(SPEC), "### 1.2 Проверяемая trigger matrix")
    data = {cells[0].strip("`"): cells[1:] for cells in rows[1:] if len(cells) == 3}
    if set(data) != set(TRIGGER_CASES):
        missing = sorted(set(TRIGGER_CASES) - set(data))
        extra = sorted(set(data) - set(TRIGGER_CASES))
        fail(errors, f"trigger matrix mismatch; missing={missing}, extra={extra}")
        return
    for prompt, expected in TRIGGER_CASES.items():
        actual = tuple(data[prompt])
        if actual != expected:
            fail(errors, f"trigger case {prompt!r} is {actual}, expected {expected}")


COMPOSER_TRIGGER_CASES = {
    "$ship-tasks:task-composer": (
        "да",
        "сформировать planning model; writes только при явном intent",
    ),
    "Сформулируй Task Manager задачу, пока не создавай": (
        "да",
        "read-only draft",
    ),
    "Создай Task в Task Manager": (
        "да",
        "одна Task либо Epic с подзадачами по реальному scope",
    ),
    "Разбей это на Epic и подзадачи в Task Manager": (
        "да",
        "Epic и достаточные подзадачи",
    ),
    "Просто добавь это в backlog": (
        "да",
        "planning-only capture без implementation",
    ),
    "Спланируй это в текущем Task Manager Project": (
        "да",
        "compose и create при однозначном Project context",
    ),
    "Выполни TM-123": ("нет", "ShipTask delivery"),
    "Создай одну Task и сразу выполни её": (
        "нет",
        "ShipTask create-and-deliver",
    ),
    "Покажи статус TM-123": ("нет", "read-only Task Manager adapter"),
    "Проведи аудит TM-123": ("нет", "read-only Task Manager adapter"),
    "Исправь код": (
        "нет",
        "обычная implementation без Task Manager planning anchor",
    ),
}


def validate_composer_trigger_matrix(errors: list[str]) -> None:
    rows = table_rows(read(COMPOSER_SPEC), "### 1.1 Проверяемая trigger matrix")
    data = {cells[0].strip("`"): cells[1:] for cells in rows[1:] if len(cells) == 3}
    if set(data) != set(COMPOSER_TRIGGER_CASES):
        missing = sorted(set(COMPOSER_TRIGGER_CASES) - set(data))
        extra = sorted(set(data) - set(COMPOSER_TRIGGER_CASES))
        fail(errors, f"composer trigger matrix mismatch; missing={missing}, extra={extra}")
        return
    for prompt, expected in COMPOSER_TRIGGER_CASES.items():
        actual = tuple(data[prompt])
        if actual != expected:
            fail(
                errors,
                f"composer trigger case {prompt!r} is {actual}, expected {expected}",
            )


REVIEW_CASES = {
    "Обычный старт `To Do`": (
        "не создаётся",
        "Explainer не запускается",
        "In Progress",
    ),
    "Первый ShipTask-вызов в новой Codex task с catalog placeholder": (
        "unique app metadata",
        "один раз задать exact `ShipTask · ...` title",
        "до первой Task Manager mutation",
        "соседней task",
    ),
    "Повторный ShipTask-вызов, meaningful title или неоднозначный current candidate": (
        "title сохраняется без изменений",
        "`task-title=not-available`",
        "перезаписывать пользовательский title",
        "retry setter",
    ),
    "Candidate готов к review": ("read-back до transition", "In Review"),
    "Current acceptance противоречит самому себе": (
        "task-contract-conflict",
        "In Review",
    ),
    "Exact candidate воспроизводимо нарушает критерий": (
        "verified-failure",
        "immediate chat alarm",
        "до repair",
        "In Progress",
        "продолжить rework в том же run",
    ),
    "Defect найден и исправлен в одном run": (
        "found and resolved",
        "resolution",
        "final ledger",
        "стереть историю",
    ),
    "Incident unresolved во время долгого active run": (
        "каждые 10 минут",
        "спамить одинаковыми Task comments",
    ),
    "Новый run возобновляет Task с unresolved incident": (
        "первом содержательном chat update",
        "material change",
    ),
    "Новая Codex-сессия видит unfinished exact Task worktree/feature branch остановленного writer": (
        "нового exclusive owner",
        "продолжить candidate в том же task-owned worktree",
        "parallel replacement worktree",
        "потерять existing changes",
    ),
    "Для unfinished exact Task сохранилась feature branch, но usable worktree отсутствует": (
        "связь с Task доказана",
        "восстановить checkout этой же branch",
        "повторять готовую работу",
    ),
    "Existing task worktree имеет active либо unknown writer ownership": (
        "takeover не выполнен",
        "artifact сохранён без mutations/cleanup",
        "два concurrent writers",
        "reset/cleanup",
    ),
    "Первый выбранный способ проверки не сработал": (
        "агент сам выбирает",
        "считать первый инструмент обязательным",
    ),
    "После стартового inventory live Release появилась новая matching Task в `To Do`": (
        "автоматически расширила delivery inventory",
        "Goal остаётся active",
        "без повторного approval",
        "стартовый список/count замороженным",
    ),
    "Matching Task live Release переведена `Backlog → To Do` во время run": (
        "автоматически стала in-scope",
        "реализовать и проверить в том же run",
        "требовать второй approval",
    ),
    "Новая matching Task live Release остаётся в `Backlog`": (
        "исключена из delivery",
        "`Backlog` сохраняется",
        "не начинать implementation",
    ),
    "Exact candidate/server path уже доказал authenticated product hang, а другой browser/controller просит новый login или MFA": (
        "verified-failure",
        "browser gap вторичен",
        "repair и retest продукта",
        "выдавать Chrome/login за repair",
    ),
    "В current scope нет достаточного способа доказать success/failure": (
        "verification-blocked",
        "In Review",
        "strongest feasible путь",
        "только при material выборе",
    ),
    "Batch gate упал, виновная Task не установлена": (
        "In Review",
        "separating evidence",
    ),
    "Release verification нашла defect в terminal Task": (
        "verified-failure",
        "до reopen",
        "exact Task",
    ),
    "Полный evidence доказывает критерии": (
        "verified-success",
        "Done",
    ),
    "Reopen terminal Task": ("причину reopen", "working status"),
    "Новый `Canceled` или `Duplicate`": (
        "terminal reason",
        "terminal status",
    ),
    "Обязательный comment write/read-back дал ошибку": (
        "transition не завершён",
        "не выполнять существенный transition",
        "fallback в description",
        "skip обязательного comment",
    ),
    "Отдельный Strategic Explainer недоступен или отклонил текст, когда effective rule его сохраняет": (
        "не публиковать непроверенный черновик",
        "не выполнять зависящий переход",
        "основной агент сам одобряет",
    ),
    "Массовая имплементация минимум двух Tasks": (
        "batch-implementation",
        "создать/продолжить Goal",
    ),
    "Scope без user topology rule содержит несколько действительно независимых полезных packets": (
        "автоматически",
        "основной integration owner",
        "без fake fan-out",
        "scheduler-настройку",
    ),
    "Несколько implementation subagents пишут одновременно": (
        "unique feature branch",
        "unique Git worktree",
        "до первой mutation",
        "integration owner",
        "fan-in",
        "общий writable checkout",
    ),
    "Genuinely simple bounded packet без отдельного profile override": (
        "gpt-5.6-luna`/`max",
        "primary selection сам по себе не отключает cheap lane",
        "понизить Luna effort",
        "user-selected subagent profile",
    ),
    "Короткий packet требует creative/architectural judgment или несёт material risk": (
        "current model/effort",
        "малого diff",
    ),
    "Luna встретила ambiguity, surprising environment/tool state или proof gap": (
        "bounded read-only read-back точно устанавливает partial effects",
        "прекращает corrective mutations",
        "продолжает packet current profile",
        "повторный cheap Luna loop",
        "silent rollback",
    ),
    "Пользователь явно задал profile всем или named subagents": (
        "приоритет над auto-classification",
        "exact выбранный profile",
        "`<profile>=not-available`",
        "уменьшить role capacity",
        "incompatible context",
    ),
        "Current primary profile сама Luna": (
        "user choice сохраняется",
        "возвращается integration owner",
        "скрыто заменить Sol",
        "replacement Luna retry loop",
    ),
    "Большой batch с одной safe write lane": (
        "одним writer",
        "read-only scouts/reviewers",
        "конфликтующие writers",
        "fake fan-out",
    ),
    "Общий prompt `не используй субагентов`": (
        "ноль subagents",
        "напрямую применяет quality contract",
        "comment subagent",
    ),
    "Prompt `используй ровно три субагента`": (
        "ровно 3 subagents сверх root",
        "обязательное число",
        "молча запустить другое число",
    ),
    "Prompt `используй побольше субагентов`": (
        "выше automatic baseline",
        "больше полезной delegation",
        "фиктивные packets",
    ),
    "Prompt `используй субагентов, только если работа займёт больше получаса`": (
        "ожидаемой длительности",
        "не больше 30 минут",
        "подменить длительность",
    ),
    "Prompt отключает только implementation subagents, но сохраняет reviewer/Explainer": (
        "implementation workers не запускаются",
        "role-scoped rule буквально",
        "global off",
    ),
    "Обязательное topology rule конфликтует с authority, isolation, useful ownership или capacity": (
        "exact conflict",
        "фактическая topology",
        "скрытое уменьшение exact count",
    ),
    "Worker capability недоступна без exact user topology rule": (
        "technical limitation не является user opt-out",
        "coordinator-only",
        "effective rule его сохраняет",
    ),
    "Comment Explainer capability недоступна, но effective rule его сохраняет": (
        "capability gap",
        "comment-dependent transition не выполняется",
        "implementation workers могут продолжать",
    ),
    "Release готового candidate по Project/Release selector": (
        "release",
        "без нового Goal",
    ),
    "Task-local blocker в `batch-implementation`": (
        "правдивый non-terminal status",
        "продолжить независимые Tasks",
    ),
}


def validate_review_matrix(errors: list[str]) -> None:
    rows = table_rows(read(REVIEW_MATRIX), "## Обязательная матрица")
    data = {cells[0]: " | ".join(cells[1:]) for cells in rows[1:] if len(cells) == 6}
    for case, terms in REVIEW_CASES.items():
        row = data.get(case)
        if row is None:
            fail(errors, f"review matrix is missing case {case!r}")
            continue
        for term in terms:
            if term not in row:
                fail(errors, f"review case {case!r} is missing {term!r}")


def validate_source_layers(errors: list[str]) -> None:
    packages = (
        (SHIP_REQUIREMENTS, "ST", 22),
        (COMPOSER_REQUIREMENTS, "TC", 10),
        (STRATEGIC_REQUIREMENTS, "SE", 12),
    )
    for requirements, prefix, count in packages:
        requirement_ids = re.findall(
            r"^### `([A-Z]+-\d{2})`", read(requirements), re.MULTILINE
        )
        expected_ids = [f"{prefix}-{number:02d}" for number in range(1, count + 1)]
        if requirement_ids != expected_ids:
            fail(
                errors,
                f"{relative(requirements)} requirement IDs are missing, duplicated, "
                f"or out of order: {requirement_ids}",
            )
        require(
            errors,
            requirements,
            "Статус: current Level 1, 2026-08-22",
            "полный пользовательский исходный код только для",
            "не могут ослабить, заменить или\nмолча удалить",
            "Изменение смысла Level 1 требует явного решения пользователя",
            "`architecture.md` хранит agent-owned current способ достижения",
            "примерно\nэквивалентен",
        )

    require(
        errors,
        SHIP_REQUIREMENTS,
        "Backlog вне delivery",
        "явно перечисленные Task refs задают закрытый selector",
        "Project,\nRelease и resolved current scope задают live selector",
        "не требует повторного approval",
        "browser login\nили MFA не становится stop condition",
        "свежего сопоставления с selector",
        "Goal хранит identity/predicate selector",
        "product failure сообщается раньше\nлогистики browser/controller/OAuth/MFA",
        "свободным языком изменить эту topology",
        "запретить всех субагентов\nили только comment Explainer",
        "Пользователь может свободным языком задать обязательное правило delegation",
        "точное или относительное количество",
        "`ровно три`, `побольше`",
        "`используй субагентов, только если\nработа займёт больше получаса`",
        "root agent не\nвходит в число явно названных субагентов",
        "не\nподменяется молча",
        "Отчёт не обязан показывать внутренний расчёт target/width",
        "Изоляция concurrent writers",
        "implementation subagent работает в собственном Git\nworktree и собственной feature branch",
        "принадлежит ровно одному implementation writer и не разделяется между\nсубагентами",
        "TASK CONTEXT ALARM",
        "Lifecycle priority и duplicate context",
        "Bounded scope и сохранность чужого состояния",
        "Resume-first и подхватывание начатой работы",
        "После ошибки, остановки агента, прерывания run",
        "принимает эксклюзивное владение этим же\nworktree",
        "branch без доступного worktree",
        "двум writers одновременно менять один worktree",
        "Независимая plugin distribution",
        "должны быть byte-identical",
    )
    forbid(
        errors,
        SHIP_REQUIREMENTS,
        "ready independent width",
        "фактическую peak width",
        "Единственный пользовательский topology override",
        "Узкие role-specific opt-outs не являются отдельным публичным",
        "пользователь не обязан и не должен вручную\nзадавать число",
    )
    require(
        errors,
        COMPOSER_REQUIREMENTS,
        "Planning-only boundary",
        "Strategic Explainer для каждого Epic",
        "Независимая planning distribution",
        "искусственный umbrella Epic",
        "Unknown outcome не\nповторяется вслепую",
        "должны быть byte-identical",
    )
    require(
        errors,
        STRATEGIC_REQUIREMENTS,
        "Никакой скрытой управляющей роли",
        "отсутствие проверки не называется\ndefect",
        "контекстный документ не является completion evidence",
        "Publication-ready и пропорциональный result",
        "Общий переносимый communication skill",
        "остаются byte-identical",
    )
    forbid(
        errors,
        STRATEGIC_REQUIREMENTS,
        "отсутствие проверки — defect",
        "контекстный документ — completion evidence",
    )
    require(
        errors,
        SOURCE_INDEX,
        "Единица\nисходного кода — отдельный skill",
        "требования и\nархитектура разных skills не объединяются",
        "Компилятор здесь стохастический",
        "примерно тот\nже contract",
        "Каждый source package должен быть понятен и пригоден для пересборки",
        "Plugin — общий distribution artifact",
    )
    for architecture, prefix in (
        (SPEC, "ST-*"),
        (COMPOSER_SPEC, "TC-*"),
        (STRATEGIC_SPEC, "SE-*"),
    ):
        require(
            errors,
            architecture,
            "Статус: current Level 2 contract, 2026-08-22",
            f"`{prefix}` в локальных",
            "[требованиях пользователя](requirements.md)",
            "## 0. Compilation contract",
            "производная смысловая компиляция",
            "примерно\nэквивалентными",
        )

    for obsolete in (
        ROOT / "docs" / "requirements.md",
        ROOT / "docs" / "architecture.md",
        ROOT / "docs" / "specs" / "ship-tasks.md",
        ROOT / "docs" / "specs" / "task-composer.md",
        ROOT / "docs" / "specs" / "strategic-explainer.md",
    ):
        if obsolete.exists():
            fail(errors, f"competing monolithic/legacy source exists: {relative(obsolete)}")

    require(
        errors,
        ROOT / "AGENTS.md",
        "Документация как исходный код",
        "Единица source —\nотдельный skill",
        "`docs/skills/<skill>/requirements.md`",
        "`docs/skills/<skill>/architecture.md`",
        "Level 1 — требования пользователя",
        "Level 2 — архитектура достижения",
        "Level 3 — runtime skills",
        "При конфликте всегда побеждает Level 1",
        "Level 1 requirement → Level 2 design → runtime skill → observable evaluation",
        "Компиляция стохастическая",
        "не объединяют Requirements или Architecture разных skills",
    )
    require(
        errors,
        ROOT / "README.md",
        "[`docs/skills/<skill>/`](docs/skills/README.md)",
        "требования\nтрёх skills не объединяются",
        "Project, Release и\ncurrent scope остаются live selectors",
        "без повторного approval",
        "Browser switch допустим как диагностика",
        "не как repair",
    )
    require(
        errors,
        DOCS_INDEX,
        "[Source model](skills/README.md)",
        "[Requirements](skills/ship-tasks/requirements.md)",
        "[Architecture](skills/ship-tasks/architecture.md)",
    )
    require(
        errors,
        VISION,
        "Статус: current Level 2 strategic design, 2026-08-22",
        "[требованиях пользователя](requirements.md)",
    )


def validate_current_contract(errors: list[str]) -> None:
    require(
        errors,
        SPEC,
        "Статус: current Level 2 contract, 2026-08-22",
        "`ST-*` в локальных",
        "[требованиях пользователя](requirements.md)",
        "ADR-0018",
        "ADR-0019",
        "ADR-0020",
        "ADR-0021",
        "ADR-0022",
        "ADR-0024",
        "ADR-0025",
        "### 1.3 Название первой Codex task",
        "обязан один раз заменить\ncatalog placeholder",
        "ровно одного current candidate",
        "без `threadId` не более одного раза",
        "task-title=not-available",
        "## 2. Конституция",
        "### 7.1 Resume-first",
        "task-owned feature branch и worktree содержат незавершённый candidate",
        "создавать параллельный replacement worktree",
        "предыдущий writer всё ещё активен",
        "Остановка writer или Codex-сессии не превращает task-owned worktree в мусор",
        "После доказанной quiescence ownership может",
        "effective topology policy",
        "точное или относительное число",
        "Root/coordinator не входит",
        "Только если применимого user rule нет",
        "comment",
        "до записи статуса",
        "всегда создаёт и перечитывает обязательный comment",
        "effective topology rule не отключает comment Explainer",
        "`To Do → In Progress` комментария не создаёт",
        "Приёмочный инцидент виден сразу",
        "примерно каждые 10 минут",
        "compact ledger всех material incidents",
        "current acceptance не ослаблен",
        "не найден достаточный безопасный способ продолжить",
        "Нет фиксированного числа попыток",
        "продолжает исправление в том же run",
        "Goal создаётся только для `batch-implementation`",
        "production release уже подготовленного candidate",
        "Release-only run не создаёт",
        "Delivery inventory исключает canonical status `Backlog`",
        "Selector и inventory — разные сущности",
        "Project, Release и resolved current scope\nявляются live selectors",
        "не замораживает count, диапазон\nrefs или список Tasks",
        "повторное approval не требуется",
        "Browser/controller/session switch — один из диагностических способов",
        "browser logistics сообщаются после установленного product\noutcome",
        "Goal active и не требует его retarget или approval",
        "### 0.1 Current compilation status",
        "`Backlog` исключён из\ndelivery",
        "natural-language правила о числе, ролях и условиях delegation",
        "собственные branch/worktree",
        "Exact count\nозначает обязательное число subagents",
        "Conditional rule проверяется по указанному\nпользователем условию",
        "Только genuinely simple packet запускается на\n`gpt-5.6-luna` с `max`",
        "Strategic Explainer по умолчанию наследует current profile",
        "повторно отправлять ту же неразрешённую проблему cheap Luna lane\nнельзя",
        "его собственный выбор несовместимой формы context не делает profile\nunavailable",
        "`<profile>=not-available` уменьшает\ncapacity соответствующей роли",
        "Luna-to-current handoff",
        "единственный integration owner",
        "владелец Goal, Task Manager\ncomments/status/version writes",
        "собственную feature branch и собственный Git worktree",
        "Read-only scouts, reviewers и\ncomment Explainer отдельного worktree не требуют",
        "Только integration\nowner выполняет fan-in",
        "Role-scoped rule меняет только названную роль",
        "effective смысл и\nподтверждают соблюдение либо material deviation",
        "сохраняет отсутствие независимой\nпроверки",
    )
    require(
        errors,
        OVERVIEW,
        "Constitution-first подход",
        "comment read-back",
        "агент сам выбирает и меняет инструменты",
        "не обязывает чинить именно его",
        "не называется verified",
        "ADR-0018",
        "ADR-0019",
        "ADR-0020",
        "ADR-0021",
        "ADR-0022",
        "ADR-0024",
        "ADR-0025",
        "гарантированной adapter capability",
        "каждый создаваемый ShipTask-комментарий",
        "durable Task history",
        "Goal используется только для прогресса массовой имплементации",
        "production release",
        "несколько независимых safe lanes",
        "genuinely\n  simple packets получают Luna Max",
        "без повторного Luna loop",
        "exact/relative count",
        "root\n  agent не считается названным субагентом",
        "condition",
        "собственной feature branch\n  и собственном Git worktree",
        "interrupted task-owned worktree/branch",
        "подхватывается следующей сессией",
        "доказанная первая Codex task с catalog placeholder",
        "последующие turns не переименовываются",
        "Project, Release и\nresolved current scope — live selectors",
        "без повторного approval",
        "Browser/controller/session switch — диагностический путь",
        "product outcome идёт раньше browser/OAuth logistics",
        "identity/predicate, не стартовый список или count",
        "Task type хранится в Label/hierarchy",
        "не дублируется\nпрефиксом `BUG:`/`EPIC:`",
    )
    require(
        errors,
        REPORT,
        "Инвариант effects",
        "До связанного существенного status transition",
        "transition не завершён",
        "всегда создаёт и перечитывает обязательный comment",
        "Пока effective topology rule не отключает comment Explainer",
        "Когда user rule отключает Explainer",
        "Обычный старт `To Do → In Progress` комментария не создаёт",
        "До repair немедленно сообщить incident",
        "resolution/completion comment",
        "Приёмка заблокирована",
        "рекомендуемый feasible способ",
        "каждые 10 минут",
        "ответ в Codex не являются durable Task comment",
    )
    require(
        errors,
        RUN_REPORT,
        "acceptance incident openings",
        "compact ledger всех material acceptance incidents run",
        "found and resolved",
        "Luna-to-current handoff",
        "effective topology rule пользователя",
        "соблюдения либо material\n  deviation",
        "подхваченный existing checkpoint",
        "невозможность безопасного takeover",
        "не совместим с clean success",
        "fresh full inventory, включая Tasks",
        "Browser/controller/OAuth/MFA logistics идут после этого",
        "identity/predicate, не стартовый список/count",
    )
    require(
        errors,
        AUTONOMY,
        "Свобода способа и качество evidence",
        "не создаёт обязанности чинить именно его",
        "итоговый evidence",
        "выбор технического пути",
        "Task-local blocker",
        "Project, Release и resolved\ncurrent scope — live selectors",
        "не замораживает membership",
        "не является\nrepair продукта",
        "browser login либо MFA не отменяет incident",
        "`gpt-5.6-luna`/`max` получает только genuinely simple packet",
        "Luna не выполняет corrective recovery mutations",
        "Повторный cheap Luna loop запрещён",
        "выбранная\ncoordinator форма context не создаёт unavailability",
        "Явный unavailable user profile не\nподменяется",
        "exact или relative число субагентов",
        "Role-scoped rule меняет только названную роль",
        "После ошибки, interrupted run, смены агента/сессии",
        "прими exclusive ownership этого же\nworktree",
        "Не делай takeover при живом writer",
        "Production workflow требует явного approval",
    )
    require(
        errors,
        MEMORY,
        "Exact Task и явный список `task_selectors` задают closed selector",
        "`kind: project|release`\nи resolved current scope задают live selector",
        "не становится\nзамороженным списком",
        "не требует нового approval",
        "перед новой frontier, ожиданием, blocker/Goal status",
        "не является alarm либо scope expansion",
    )
    require(
        errors,
        HANDOFF,
        "Пока effective topology rule не отключает comment Explainer",
        "Если rule отключает Explainer",
        "отдельного субагента",
        "не переписывает текст обратно",
        "user-facing judgment packet наследует current model/effort",
    )
    require(
        errors,
        ADR["0018"],
        "Конституция управляет результатом, а не инструментами",
        "не выбирает за агента инструменты",
        "Сбой одного способа сам по себе не доказывает",
        "не нашёл достаточного безопасного способа",
        "не задаёт invocation или tool flow",
        "Фиксированного числа попыток",
    )
    require(
        errors,
        ADR["0019"],
        "Goal только для массовой имплементации Tasks",
        "минимум две concrete Tasks",
        "не определяют mode и не разрешают Goal",
        "Release-only не создаёт",
        "Production отличается дополнительной authority boundary",
        "Сам release новый Goal не создаёт",
    )
    require(
        errors,
        ADR["0020"],
        "Приёмочные инциденты видимы во всём run",
        "Comments — гарантированный adapter contract",
        "Немедленный outcome-first update",
        "примерно в 10 минут",
        "Final success не стирает найденный defect",
        "рекомендует самый сильный feasible",
    )
    require(
        errors,
        ADR["0021"],
        "Требования являются конституцией для агентов",
        "какой пользовательский или системный результат обязателен",
        "Агент самостоятельно выбирает план",
        "Когда допустима точность механизма",
        "Strategic Explainer определяется результатом",
        "Evals проверяют наблюдаемое поведение",
        "ADR-0024",
        "ADR-0025",
    )
    require(
        errors,
        ADR["0022"],
        "Каждый комментарий ShipTask проходит независимый Strategic Explainer",
        "Обычный переход `To Do → In Progress` не создаёт комментарий",
        "каждый комментарий в Task\n  Manager",
        "отдельный независимый субагент",
        "не переписывает одобренный текст",
        "не публикует комментарий",
        "самостоятельно выполненная основным агентом",
        "ADR-0024",
    )
    require(
        errors,
        ADR["0024"],
        "Automatic delegation и natural-language topology rules",
        "Default без user rule",
        "User topology rule",
        "Root/coordinator не входит",
        "Exact count является обязательным count",
        "role scope",
        "condition",
        "Task Manager comments/status/version writes",
        "Writer isolation",
        "собственную feature branch и собственный Git worktree",
        "Writable worktree принадлежит одному writer",
        "общий opt-out",
        "role-scoped rule",
        "Наблюдаемость без scheduler-бухгалтерии",
        "material deviation",
        "ADR-0025",
    )
    require(
        errors,
        ADR["0025"],
        "Cost-aware профили субагентов с эскалацией на current model",
        "`gpt-5.6-luna` с `max`",
        "Текущие model/effort основного агента образуют default profile",
        "Явное указание пользователя",
        "все условия",
        "Strategic Explainer по умолчанию наследует current profile",
        "Luna прекращает packet",
        "без Luna retry loop",
        "повторно\nотправить cheap Luna lane",
        "собственный выбор incompatible context не делает profile unavailable",
        "`<profile>=not-available`",
        "`luna-escalation=not-available`",
        "Sol Extra High или Sol Ultra как универсальный default",
    )
    for path in (
        ROOT / "AGENTS.md",
        ROOT / "README.md",
        SHIP_SKILL,
        SHIP_METADATA,
        SPEC,
        OVERVIEW,
        DEVELOPMENT,
        REVIEW_MATRIX,
        REPORT,
        RUN_REPORT,
        AUTONOMY,
        HANDOFF,
    ):
        forbid(
            errors,
            path,
            "active target равен",
            "весь target bounded workers",
            "ready independent lanes",
            "фактическую peak width",
            "peak width 0",
        )
    require(
        errors,
        ADAPTER,
        "повторно сверен 2026-08-22",
        "Native comment create/list/read являются гарантированной частью adapter",
        "reconciles через native reads до retry или status transition",
    )

    contradiction_patterns = {
        "comment deferred after status": re.compile(
            r"status\s+write.{0,100}(?:вс[её]\s+равно|после|затем).{0,100}(?:communication remainder|комментари)",
            re.I | re.S,
        ),
        "unclear batch reopened into rework": re.compile(
            r"неясн\w*\s+attribution.{0,120}(?:весь|все).{0,80}In Progress",
            re.I | re.S,
        ),
        "review status asserted as verified": re.compile(
            r"In Review.{0,30}(?:targeted-verified|machine-verified)", re.I | re.S
        ),
        "mandatory diagram by complexity": re.compile(
            r"non-trivial.{0,60}(?:получает|требует).{0,30}diagram", re.I | re.S
        ),
        "orchestration failure stops reporting": re.compile(
            r"повторн\w*\s+отказ.{0,80}останавливает\s+report", re.I | re.S
        ),
        "stale adapter cutover": re.compile(
            r"Task Manager skill пока содержит.{0,80}старого delivery", re.I | re.S
        ),
    }
    for path in CURRENT_CONTRACT_FILES:
        text = read(path)
        for label, pattern in contradiction_patterns.items():
            match = pattern.search(text)
            if match:
                line = text.count("\n", 0, match.start()) + 1
                fail(errors, f"{relative(path)} has {label} at line {line}")

    for path in CURRENT_CONTRACT_FILES:
        forbid(
            errors,
            path,
            "acceptance-required state",
            "ACCEPTANCE READY report",
            "reopen получает весь связанный batch",
            "Tasks с недействительным evidence в `In Progress`",
            "self-recovery",
            "Technical Brief",
            "communication remainder",
            "batch — с Goal",
            "Project/Release/bare scope — batch с Goal",
        )

    for path in CURRENT_CONTRACT_FILES:
        if path == ADR["0018"]:
            continue
        forbid(
            errors,
            path,
            "Необходимый инструмент сначала",
            "сначала восстанови нужные инструменты",
            "после material repair повтори",
            "только затем оцени равноценную альтернативу",
            "сначала пытается его восстановить",
        )

    for path in (
        SHIP_SKILL,
        SPEC,
        OVERVIEW,
        REPORT,
        RUN_REPORT,
        AUTONOMY,
        HANDOFF,
        ADAPTER,
    ):
        forbid(
            errors,
            path,
            "2–4 способа приёмки",
            "2–4 различных способа",
            "comment-delivery-unavailable",
            "terminal-report-channel-unavailable",
            "comment channel недоступен",
            "comment channel не работает",
        )

    for path in (
        ROOT / "README.md",
        SHIP_SKILL,
        STRATEGIC_SKILL,
        SPEC,
        STRATEGIC_SPEC,
        OVERVIEW,
        DEVELOPMENT,
        REVIEW_MATRIX,
        STRATEGIC_EVALUATION,
        VISION,
        REPORT,
        RUN_REPORT,
        HANDOFF,
    ):
        forbid(
            errors,
            path,
            'fork_turns="none"',
            "CONTEXT_INTEGRITY_ERROR",
            "PROBLEM_CONTEXT_ERROR",
            "2–4 реально различающихся варианта",
            "2–4 реально различающихся способа",
        )


def validate_strategic_contract(errors: list[str]) -> None:
    require(
        errors,
        STRATEGIC_SPEC,
        "Статус: current Level 2 contract, 2026-08-22",
        "`SE-*` в локальных",
        "[требованиях пользователя](requirements.md)",
        "общего skill `$strategic-explainer`",
        "Конституционный принцип",
        "не задаёт внутреннюю архитектуру агента",
        "Достаточный вход",
        "Bounded strategic discovery",
        "Exact envelope не требуется",
        "не придумывает alternatives ради количества",
        "Completion criteria",
        "Текст пишется на языке пользователя",
        "готовый пользовательский текст",
        "пригоден для публикации",
    )
    require(
        errors,
        VISION,
        "Продуктовое обещание",
        "Требования как конституция",
        "Никакой скрытой управляющей роли",
        "Визуализация служит пониманию",
        "Lossless by relevance",
        "Проверяемый source basis",
    )
    require(
        errors,
        STRATEGIC_EVALUATION,
        "Problem legitimacy",
        "Factual grounding и coverage",
        "Source state и relevance",
        "Read-only и authority boundary",
        "Human comprehension",
        "гибридную фразу с английским смысловым ядром",
        "пригоден для публикации",
        "Read-only boundary",
        "Реальный выбор способа проверки",
        "не оценивает agent topology",
    )

    numbered = []
    for line in read(VISION).splitlines():
        match = re.match(r"^### (\d+)\. ", line)
        if match:
            numbered.append(int(match.group(1)))
    if numbered != list(range(1, len(numbered) + 1)):
        fail(errors, f"strategic vision numbered requirements are not sequential: {numbered}")


def validate_supersession(errors: list[str]) -> None:
    required_markers = {
        "0002": ("superseded", "ADR-0003"),
        "0008": ("superseded ADR-0011",),
        "0003": ("ADR-0006", "ADR-0020"),
        "0009": ("superseded", "ADR-0010", "ADR-0017", "ADR-0020"),
        "0005": ("ADR-0016", "ADR-0017"),
        "0006": ("ADR-0016", "ADR-0017", "ADR-0020"),
        "0010": ("ADR-0016", "ADR-0017"),
        "0012": (
            "partially superseded",
            "ADR-0014",
            "ADR-0021",
            "ADR-0022",
            "no-tools",
        ),
        "0013": (
            "partially superseded",
            "ADR-0014",
            "ADR-0016",
            "ADR-0017",
            "ADR-0021",
            "ADR-0022",
        ),
        "0014": ("partially superseded", "ADR-0021"),
        "0015": ("partially superseded", "ADR-0017", "ADR-0020"),
        "0016": ("partially superseded", "ADR-0017", "ADR-0020"),
        "0007": ("ADR-0019",),
        "0017": (
            "partially superseded",
            "ADR-0018",
            "ADR-0019",
            "ADR-0020",
            "ADR-0021",
            "ADR-0022",
        ),
        "0021": ("partially superseded", "ADR-0022", "ADR-0024", "ADR-0025"),
        "0022": ("partially superseded", "ADR-0024"),
    }
    for number, terms in required_markers.items():
        header = "\n".join(read(ADR[number]).splitlines()[:18])
        for term in terms:
            if term not in header:
                fail(errors, f"ADR-{number} header is missing supersession marker {term!r}")


def validate_adapter_and_distribution(errors: list[str]) -> None:
    require(
        errors,
        ADAPTER,
        "current compatibility contract",
        "adapter skill `task-manager`",
        "не содержит\n`ship-tasks`/`task-composer`/`strategic-explainer`",
        "Adapter не выбирает business scope",
        "current Task `version`",
        "native Label catalogs/assignment",
        "relation create получает стабильный idempotency key",
        "Task Manager state доказывает только собственную projection",
        "Native comment create/list/read являются гарантированной частью adapter",
    )
    require(
        errors,
        ADR["0011"],
        "ship-tasks@srez-marketplace",
        "task-manager@srez-marketplace",
        "adapter skill `task-manager`",
        "skills/task-composer",
        "skills/strategic-explainer",
        "fresh Codex session",
    )
    require(
        errors,
        ROOT / "AGENTS.md",
        "Definition of done для изменения skill",
        "origin/main",
        "byte-identical",
        "installed cache",
        "installed/enabled",
        "Standalone user-level каталоги",
        "~/.codex/skills/task-composer",
        "task-manager@srez-marketplace` остаётся adapter-only",
        "каждый комментарий проходит\n  отдельного независимого Strategic Explainer",
        "`To Do → In Progress` комментария не создаёт",
        "правило пользователя свободным языком — exact/relative count",
        "root agent не входит в явно названное число",
        "duration/complexity condition",
        "собственные feature branch и Git worktree",
        "не разделяемые с\n  другим writer",
        "unfinished worktree/branch подхватывается",
        "exclusive writer после проверки quiescence",
        "`gpt-5.6-luna`/`max`",
        "Luna retry loop",
        "catalog placeholder после live scope resolution",
        "ambiguous candidate не\n  переименовываются",
    )
    require(
        errors,
        DEVELOPMENT,
        "read_marketplace_name.py",
        "update_plugin_cachebuster.py",
        "не меняйте\n   numeric version",
        "fresh App Server catalog",
        "ship-tasks:task-composer",
        "existing-only Labels",
        "отдельного Strategic Explainer при разрешённой роли",
        "`To Do → In Progress` не создаёт комментарий",
        "automatic default",
        "отдельный worktree каждого implementation writer",
        "natural-language exact/relative/role/conditional rules",
        "подхватывает\n  существующий unfinished task-owned worktree/branch",
        "active\n  или ambiguous ownership не захватывается",
        "ноль subagents",
        "Luna Max routing",
        "current-profile escalation",
        "Project/Release/current scope сохраняют live membership",
        "initial inventory не\n  превращается в Goal count/list cap",
        "authenticated product hang остаётся product incident",
        "browser/OAuth/MFA logistics",
        "Auto-title является отдельным явным требованием",
        "адресация только calling task",
        "Type Labels не должны дублироваться в title",
        "legacy-prefixed title участвует в\nduplicate search",
    )


def current_task_source_files() -> tuple[Path, ...]:
    return (
        SHIP_SKILL,
        SHIP_METADATA,
        COMPOSER_SKILL,
        COMPOSER_METADATA,
        SPEC,
        COMPOSER_SPEC,
        COMPOSER_EVALUATION,
        OVERVIEW,
        REPORT,
        RUN_REPORT,
        AUTONOMY,
        MEMORY,
        HANDOFF,
        THREAD_TITLE,
        ADR["0018"],
        ADR["0019"],
        ADR["0020"],
        ADR["0022"],
        ADR["0023"],
        ADR["0024"],
        ADR["0025"],
    )


def validate_task_source_boundary(errors: list[str]) -> None:
    retired_provider = re.compile(r"\blinear\b", re.I)
    generation = re.compile(r"(?:ship[- ]?tasks|shiptask)\s*-?\s*v\d+", re.I)
    for path in current_task_source_files():
        text = read(path)
        for label, pattern in (
            ("retired task provider", retired_provider),
            ("numbered ShipTask generation", generation),
        ):
            match = pattern.search(text)
            if match:
                line = text.count("\n", 0, match.start()) + 1
                fail(errors, f"{relative(path)} contains {label} at line {line}")


def markdown_files() -> list[Path]:
    files = [ROOT / "README.md", ROOT / "AGENTS.md"]
    files.extend(sorted((ROOT / "ship-tasks").rglob("*.md")))
    files.extend(sorted((ROOT / "task-composer").rglob("*.md")))
    files.extend(sorted((ROOT / "strategic-explainer").rglob("*.md")))
    files.extend(sorted((ROOT / "docs").rglob("*.md")))
    return files


def validate_links_and_navigation(errors: list[str]) -> None:
    for source in markdown_files():
        for raw in LINK_RE.findall(read(source)):
            target = raw.strip().strip("<>").split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            resolved = (source.parent / target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                fail(errors, f"{relative(source)} links outside repository: {target}")
                continue
            if not resolved.exists():
                fail(errors, f"{relative(source)} has broken link: {target}")

    direct_targets = {
        (DOCS_INDEX.parent / raw.strip().strip("<>").split("#", 1)[0]).resolve()
        for raw in LINK_RE.findall(read(DOCS_INDEX))
        if raw and "://" not in raw
    }
    for document in sorted((ROOT / "docs").rglob("*.md")):
        if document == DOCS_INDEX:
            continue
        if document.resolve() not in direct_targets:
            fail(errors, f"docs/README.md does not link {relative(document)}")


def validate_artifacts(errors: list[str]) -> None:
    for path in ROOT.rglob("*"):
        if ".git" in path.parts:
            continue
        if path.name == "__pycache__" or path.suffix == ".pyc":
            fail(errors, f"generated Python artifact present: {relative(path)}")


def main() -> int:
    errors: list[str] = []
    for path in CORE_FILES:
        if not path.is_file():
            fail(errors, f"missing required file: {relative(path)}")

    if not errors:
        validate_ship_skill(errors)
        validate_composer_skill(errors)
        validate_strategic_skill(errors)
        validate_trigger_matrix(errors)
        validate_composer_trigger_matrix(errors)
        validate_review_matrix(errors)
        validate_source_layers(errors)
        validate_current_contract(errors)
        validate_strategic_contract(errors)
        validate_supersession(errors)
        validate_adapter_and_distribution(errors)
        validate_task_source_boundary(errors)
        validate_links_and_navigation(errors)
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
