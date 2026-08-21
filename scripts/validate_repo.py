#!/usr/bin/env python3
"""Validate ShipTask structure and current behavioral invariants."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHIP_SKILL = ROOT / "ship-tasks" / "SKILL.md"
SHIP_METADATA = ROOT / "ship-tasks" / "agents" / "openai.yaml"
STRATEGIC_SKILL = ROOT / "strategic-explainer" / "SKILL.md"
STRATEGIC_METADATA = ROOT / "strategic-explainer" / "agents" / "openai.yaml"
SPEC = ROOT / "docs" / "specs" / "ship-tasks.md"
STRATEGIC_SPEC = ROOT / "docs" / "specs" / "strategic-explainer.md"
OVERVIEW = ROOT / "docs" / "overview.md"
DOCS_INDEX = ROOT / "docs" / "README.md"
DEVELOPMENT = ROOT / "docs" / "guides" / "development.md"
REVIEW_MATRIX = (
    ROOT / "docs" / "reference" / "shiptask-review-disposition-evaluation.md"
)
STRATEGIC_EVALUATION = (
    ROOT / "docs" / "reference" / "strategic-explainer-evaluation.md"
)
ADAPTER = ROOT / "docs" / "reference" / "task-manager-adapter.md"
VISION = ROOT / "docs" / "strategic-explainer.md"
REPORT = ROOT / "ship-tasks" / "references" / "delivery-report.md"
RUN_REPORT = ROOT / "ship-tasks" / "references" / "run-report.md"
AUTONOMY = ROOT / "ship-tasks" / "references" / "autonomy-and-release.md"
MEMORY = ROOT / "ship-tasks" / "references" / "project-memory.md"
HANDOFF = ROOT / "ship-tasks" / "references" / "strategic-explainer.md"

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
    )
}

CORE_FILES = (
    ROOT / "README.md",
    ROOT / "AGENTS.md",
    ROOT / ".gitignore",
    ROOT / ".gitattributes",
    SHIP_SKILL,
    SHIP_METADATA,
    STRATEGIC_SKILL,
    STRATEGIC_METADATA,
    SPEC,
    STRATEGIC_SPEC,
    OVERVIEW,
    DOCS_INDEX,
    DEVELOPMENT,
    REVIEW_MATRIX,
    STRATEGIC_EVALUATION,
    ADAPTER,
    VISION,
    REPORT,
    RUN_REPORT,
    AUTONOMY,
    MEMORY,
    HANDOFF,
    *ADR.values(),
)

# These files describe current behavior. Historical reports and superseded ADRs
# may retain old wording, but cannot act as fallback policy.
CURRENT_CONTRACT_FILES = (
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
    MEMORY,
    HANDOFF,
    ADR["0018"],
    ADR["0019"],
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
    validate_frontmatter(errors, SHIP_SKILL, "ship-tasks", 220)
    text = read(SHIP_SKILL)
    description = text.split("---", 2)[1] if text.count("---") >= 2 else ""

    for term in (
        "$ship-tasks",
        "Task Manager scope",
        "implicit invocation",
        "TM-123",
        "Одного delivery-глагола недостаточно",
        "Create-and-deliver",
        "Bare $ship-tasks разрешает mode по live inventory",
        "Single и release работают без Goal",
        "Goal нужен только для batch-implementation минимум двух Tasks",
        "backlog capture",
    ):
        if term not in description:
            fail(errors, f"ship-tasks description is missing routing concept {term!r}")

    required_sections = (
        "## 1. Выбери mode и exact scope",
        "## 2. Соблюдай обязательные требования",
        "## 3. Выполни и проверь result",
        "## 4. Разбери `In Review` по текущим фактам",
        "## 5. Используй Strategic Explainer для человеческих объяснений",
        "## 6. Продолжай автономно и финализируй",
    )
    for heading in required_sections:
        if section(text, heading) is None:
            fail(errors, f"ship-tasks/SKILL.md is missing section {heading!r}")

    require(
        errors,
        SHIP_SKILL,
        "полный exact scope",
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
        "2–4 способа",
        "продолжай rework в этом же run",
        "$ship-tasks:strategic-explainer",
        "способ выполнения этого требования выбирает агент",
        "SHIPTASK RUN REPORT",
    )

    require(
        errors,
        SHIP_METADATA,
        'display_name: "Ship Tasks"',
        'short_description: "Доставить выбранный Task Manager scope"',
        "$ship-tasks",
        'value: "task-manager"',
        "allow_implicit_invocation: true",
        "In Review",
        "Goal создавай только для реальной implementation/rework минимум двух Tasks",
        "release-only, включая production, работают без нового Goal",
    )


def validate_strategic_skill(errors: list[str]) -> None:
    validate_frontmatter(errors, STRATEGIC_SKILL, "strategic-explainer", 240)
    require(
        errors,
        STRATEGIC_SKILL,
        "Problem to solve",
        "Current-State Brief",
        "CONTEXT_INTEGRITY_ERROR",
        "PROBLEM_CONTEXT_ERROR",
        "fork_turns=\"none\"",
        "bounded read-only tools",
        "current/accepted",
        "proposed",
        "historical",
        "Decision support request",
        "2–4",
        "Forward trace",
        "Reverse coverage",
        "source basis",
        "не готовый comment payload",
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
        "`batch-implementation` с Goal после live inventory",
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
    "Создай Task в Task Manager": ("нет", "planning/write через adapter, без delivery flow"),
    "Просто добавь это в backlog": ("нет", "backlog capture, без delivery flow"),
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


REVIEW_CASES = {
    "Обычный старт `To Do`": ("не требуется", "In Progress"),
    "Candidate готов к review": ("read-back до transition", "In Review"),
    "Current acceptance противоречит самому себе": (
        "task-contract-conflict",
        "In Review",
    ),
    "Exact candidate воспроизводимо нарушает критерий": (
        "verified-failure",
        "In Progress",
        "продолжить rework в том же run",
    ),
    "Первый выбранный способ проверки не сработал": (
        "агент сам выбирает",
        "считать первый инструмент обязательным",
    ),
    "В current scope нет достаточного способа доказать success/failure": (
        "verification-blocked",
        "In Review",
        "2–4 способа",
    ),
    "Batch gate упал, виновная Task не установлена": (
        "In Review",
        "separating evidence",
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
    "Обязательный comment фактически не создан или не перечитан": (
        "transition не завершён",
        "не выполнять существенный transition",
        "fallback в description",
    ),
    "Массовая имплементация минимум двух Tasks": (
        "batch-implementation",
        "создать/продолжить Goal",
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


def validate_current_contract(errors: list[str]) -> None:
    require(
        errors,
        SPEC,
        "Статус: current contract, 2026-08-21",
        "ADR-0018",
        "ADR-0019",
        "## 2. Конституция",
        "comment",
        "до status write",
        "не является обязательным",
        "current acceptance не ослаблен",
        "не найден достаточный безопасный способ продолжить",
        "Нет фиксированного числа попыток",
        "продолжает исправление в том же run",
        "Goal создаётся только для `batch-implementation`",
        "production release уже подготовленного candidate",
        "Release-only run не создаёт",
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
        "Goal используется только для прогресса массовой имплементации",
        "production release",
    )
    require(
        errors,
        REPORT,
        "Только затем",
        "transition не завершён",
        "не предписывает, какой tool выбрать",
        "Приёмка заблокирована",
        "2–4 различных способа",
        "Ответ в Codex не является durable Task comment",
    )
    require(
        errors,
        AUTONOMY,
        "Свобода способа и качество evidence",
        "не создаёт обязанности чинить именно его",
        "итоговый evidence",
        "выбор технического пути",
        "Task-local blocker",
        "Production workflow требует явного approval",
    )
    require(
        errors,
        HANDOFF,
        "Конституция не задаёт конкретный invocation или recovery flow",
        "Обязательный результат",
    )
    require(
        errors,
        ADR["0018"],
        "Конституция управляет результатом, а не инструментами",
        "не выбирает за агента инструменты",
        "Сбой одного способа сам по себе не доказывает",
        "не нашёл достаточного безопасного способа",
        "не задаёт tool flow",
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

    contradiction_patterns = {
        "comment deferred after status": re.compile(
            r"status.{0,100}(?:вс[её]\s+равно|сначала).{0,100}(?:communication remainder|комментари)",
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


def validate_strategic_contract(errors: list[str]) -> None:
    require(
        errors,
        STRATEGIC_SPEC,
        "Статус: current contract, 2026-08-21",
        "общий skill `$strategic-explainer`",
        "Problem to solve",
        "Current-State Brief",
        "Strategic discovery anchors",
        "PROBLEM_CONTEXT_ERROR",
        "CONTEXT_INTEGRITY_ERROR",
        "Decision support request",
        "2–4 реально различающихся варианта",
        "forward trace",
        "reverse coverage",
        "source note",
    )
    require(
        errors,
        VISION,
        "Продуктовое обещание",
        "bounded read-only discovery",
        "Никакой скрытой управляющей роли",
        "Визуализация служит пониманию",
        "Lossless by relevance",
        "Проверяемый source basis",
    )
    require(
        errors,
        STRATEGIC_EVALUATION,
        "Problem gate",
        "Discovery discipline",
        "Source-state и provenance",
        "Factual fidelity",
        "Authority boundary",
        "Read-only boundary",
        "Несколько способов провести проверку",
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
        "0009": ("superseded", "ADR-0010", "ADR-0017"),
        "0005": ("ADR-0016", "ADR-0017"),
        "0006": ("ADR-0016", "ADR-0017"),
        "0010": ("ADR-0016", "ADR-0017"),
        "0012": ("ADR-0014", "no-tools"),
        "0013": ("ADR-0014", "ADR-0016", "ADR-0017"),
        "0015": ("partially superseded", "ADR-0017"),
        "0016": ("partially superseded", "ADR-0017"),
        "0007": ("ADR-0019",),
        "0017": ("partially superseded", "ADR-0018", "ADR-0019"),
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
        "не содержит\n`ship-tasks`/`strategic-explainer`",
        "Adapter не выбирает business scope",
        "current Task `version`",
        "Task Manager state доказывает только собственную projection",
    )
    require(
        errors,
        ADR["0011"],
        "ship-tasks@srez-marketplace",
        "task-manager@srez-marketplace",
        "adapter skill `task-manager`",
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
        "task-manager@srez-marketplace` остаётся adapter-only",
    )
    require(
        errors,
        DEVELOPMENT,
        "read_marketplace_name.py",
        "update_plugin_cachebuster.py",
        "не меняйте\n   numeric version",
        "fresh App Server catalog",
    )


def current_task_source_files() -> tuple[Path, ...]:
    return (
        SHIP_SKILL,
        SHIP_METADATA,
        SPEC,
        OVERVIEW,
        REPORT,
        RUN_REPORT,
        AUTONOMY,
        MEMORY,
        HANDOFF,
        ADR["0018"],
        ADR["0019"],
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
        validate_strategic_skill(errors)
        validate_trigger_matrix(errors)
        validate_review_matrix(errors)
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
