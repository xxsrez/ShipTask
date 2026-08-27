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
STRATEGIC_PROVIDER = (
    ROOT / "strategic-explainer" / "references" / "provider-contract.md"
)
STRATEGIC_ENTRYPOINT = (
    ROOT / "strategic-explainer" / "references" / "provider-entrypoint.md"
)
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
TERMINAL_ROUTING_REPORT = (
    ROOT / "docs" / "reports" / "2026-08-27-terminal-provider-routing-evaluation.md"
)
ADAPTER = ROOT / "docs" / "reference" / "task-manager-adapter.md"
VISION = SKILL_SOURCES / "strategic-explainer" / "product-vision.md"
REPORT = ROOT / "ship-tasks" / "references" / "delivery-report.md"
RUN_REPORT = ROOT / "ship-tasks" / "references" / "run-report.md"
AUTONOMY = ROOT / "ship-tasks" / "references" / "autonomy-and-release.md"
MEMORY = ROOT / "ship-tasks" / "references" / "project-memory.md"
HANDOFF = ROOT / "ship-tasks" / "references" / "strategic-explainer.md"
THREAD_TITLE = ROOT / "ship-tasks" / "references" / "thread-title.md"
CRITICAL_REVIEW = ROOT / "ship-tasks" / "references" / "critical-codebase-review.md"

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
        (
            "0026",
            "0026-periodic-uat-batch-releases.md",
        ),
        (
            "0027",
            "0027-critical-codebase-acceptance.md",
        ),
        (
            "0028",
            "0028-integrated-implementation-satisfies-blocked-by.md",
        ),
        (
            "0029",
            "0029-fresh-strategic-explainer-and-blocker-reflection.md",
        ),
        (
            "0030",
            "0030-opaque-strategic-explainer-provider-boundary.md",
        ),
        (
            "0031",
            "0031-standalone-strategic-explainer-plugin.md",
        ),
        (
            "0033",
            "0033-terminal-provider-and-optional-shiptask-routing.md",
        ),
        (
            "0034",
            "0034-luna-max-for-ordinary-strategic-explainer.md",
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
    STRATEGIC_ENTRYPOINT,
    STRATEGIC_PROVIDER,
    TERMINAL_ROUTING_REPORT,
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
    CRITICAL_REVIEW,
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
    ADR["0026"],
    ADR["0027"],
    ADR["0028"],
    ADR["0029"],
    ADR["0031"],
    ADAPTER,
    CRITICAL_REVIEW,
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
    validate_frontmatter(errors, SHIP_SKILL, "ship-tasks", 300)
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
        "per-Task gate",
        "периодический review-batch",
        "exact UAT release",
        "critical-codebase fallback",
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
        "current parent chain до ближайшего relevant Epic целиком",
        "передай bounded context любому implementation/review packet",
        "Epic задаёт смысл и планку качества, но не расширяет selector/scope",
        "TASK CONTEXT ALARM",
        "Доказательство важнее выбранного способа",
        "Сбой одного выбранного способа",
        "не делает его обязательным",
        "Не снижай current acceptance ради удобства",
        "как обеспечить это, решает агент",
        "task-contract-conflict",
        "verified-success",
        "verified-failure",
        "verification-blocked",
        "critical-codebase-accepted",
        "fork_turns=\"none\"",
        "In Review → In Progress",
        "продолжай rework в этом же run",
        "гарантированная часть current Task Manager adapter",
        "Не скрывай приёмочный инцидент",
        "немедленно сообщи в Codex chat",
        "каждые 10 минут",
        "краткий перечень существенных инцидентов",
        "Материальные `blocked by` gates отчитай отдельно",
        "$strategic-explainer:strategic-explainer",
        "Canonical `Backlog` не входит в delivery inventory",
        "closed selectors",
        "live selectors",
        "audit snapshot",
        "не требует approval",
        "Browser/controller/session switch — диагностика, не repair",
        "browser logistics не stop condition",
        "fresh full inventory",
        "`blocked by` открывает dependent implementation по readiness gate",
        "fan-in нужного blocking Task contract",
        "`Done` не требуется",
        "dependent Task уже runnable",
        "не инвалидируй независимые Tasks/evidence",
        "сам release новый Goal не создаёт",
        "Release-only run Goal не создаёт",
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
        "Role-scoped rule меняет\nтолько названную роль",
        "только genuinely simple packet запускай на `gpt-5.6-luna`/`max`",
        "Ordinary Strategic Explainer использует отдельный exact Luna Max contract",
        'model="gpt-5.6-luna"',
        'reasoning_effort="max"',
        "не наследуй current\nprofile",
        "без скрытой подмены Sol",
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
        "В начале run выбери communication mode",
        "ordinary `$strategic-explainer:strategic-explainer`",
        "иначе native",
        "не делай второй editorial\nrewrite",
        "не имитируй внутренний\nметод provider",
        "Обычный `To Do → In Progress` не запускает publication unit",
        "Финальный ответ — новая scope-level unit",
        "Каждый Task Manager comment, отдельный\nTask/scope report, blocker explanation и final",
        "одной compact user-facing task, exact scope, resolvable read-only\nanchors",
        "Invalid ordinary invocation исправь одним новым clean subagent",
        "provider explanation/source basis как\nreflection input",
        "Достаточный путь отменяет\nstale blocker",
        "Периодический UAT batch release",
        "лёгкий targeted gate",
        "разумный exact integrated batch",
        "один exact candidate в verified UAT",
        "Не деплой UAT после каждой bug/Task",
        "UAT — разрешённый non-production effect",
        "UAT read-back/smoke",
        "`blocked by` открывает dependent implementation",
        "[title contract](references/thread-title.md)",
        "доказанный catalog placeholder",
        "best-effort",
        "не блокируют",
    )

    require(
        errors,
        THREAD_TITLE,
        "Best-effort название Codex task",
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
        "все remaining In Review verification-blocked",
        "substantial human verifier, не bounded unlocker",
        "Ровно один read-only critic",
        "fork_turns=none",
        "per-Task verdict",
        "stale/inconclusive остаётся In Review",
        "SHIPTASK RUN REPORT",
        "Периодический UAT batch release",
        "один exact candidate в verified UAT",
        "UAT — разрешённый non-production effect",
        "UAT read-back/smoke",
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
        "$strategic-explainer:strategic-explainer",
        "не создавай Epic; single Task",
        "secret store",
        "live active catalog",
        "relation graph",
        "attachment mapping",
        "формат сам по себе не создаёт презумпцию уместности",
        "native attachment самой конкретной создаваемой Task",
        "Не начинай create,\nесли native transport заведомо недоступен",
        "attachment disposition",
        "искусственный umbrella Epic",
        "Не превращай шаги исходного плана в Tasks механически",
        "самодостаточную проекцию",
        "Epic context не расширяет scope child",
        "Title кратко называет ожидаемый результат",
        "Type/classification выражай native Label",
        "Legacy-prefixed и clean outcome title считай одним duplicate candidate",
        "Не строй последовательную цепочку по умолчанию",
        "Unknown write outcome",
        "остановился частично",
        "planning projection",
        "fork_turns=\"none\"",
        "model=\"gpt-5.6-luna\"",
        "reasoning_effort=\"max\"",
        "Не наследуй current model/effort",
        "не подменяй недоступную Luna на\nSol",
        "одна compact task",
        "новому clean subagent",
        "Не читай provider-internal contract",
        "текст самостоятельно не улучшай",
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
        "Статус: current Level 2 contract, 2026-08-27",
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
        "outcome graph",
        "Стратегическая преемственность",
        "одной ссылки недостаточно",
        "не разрешает выполнять\nсоседние подзадачи",
        "Attachments из bug report",
        "одно и то же рассуждение по содержанию, связи с Task и практической\nпользе",
        "не создают презумпцию уместности",
        "самой конкретной\nсоздаваемой Task",
        "native Task attachment",
        "attachment disposition",
        "$strategic-explainer:strategic-explainer",
        "создание Epic не начинается; single Task",
        "не secret value",
        "Создание нового Label не разрешено",
        "Direction каждого `blocks`",
        "Unknown write outcome",
        "Task Manager read-back доказывает только planning projection",
        "fork_turns=\"none\"",
        "одну compact task",
        "новый clean subagent",
    )
    require(
        errors,
        COMPOSER_EVALUATION,
        "observable planning result",
        "write происходит только по явному planning intent",
        "Epic problem-first",
        "независимые outcomes не сливаются",
        "activity Tasks",
        "самодостаточную\n  проекцию применимых strategic requirements",
        "не расширяет exact scope",
        "Strategic Explainer",
        "блокирует только Epic create",
        "каждый уместный attachment из bug report",
        "содержанием, связью с Task и пользой исполнителю",
        "тип файла не создаёт презумпцию уместности",
        "attachment binding и metadata",
        "Native transport обязательного attachment заведомо недоступен",
        "Task создана, но attachment bind завершился с ошибкой",
        "Release назначен только при однозначном current",
        "отсутствующий подходящий Label",
        "classification хранится в Label/hierarchy",
        "Есть live `Bug` Label",
        "Legacy `BUG: Исправить X` уже существует",
        "exact title `BUG: X` verbatim",
        "duplicate search предшествует create",
        "read-back подтверждает",
        "Ошибка после создания части Epic",
        "Первый Epic Explainer отклонил inherited/многословный context",
        "новый clean subagent",
        "opaque client protocol",
        "не читает provider-internal\n  contract",
    )
    for path in (
        COMPOSER_REQUIREMENTS,
        COMPOSER_SPEC,
        COMPOSER_SKILL,
        COMPOSER_EVALUATION,
    ):
        forbid(
            errors,
            path,
            "считается осмысленным по умолчанию",
            "считай осмысленным по умолчанию",
        )
    require(
        errors,
        ADR["0023"],
        "Task Composer как planning sibling-skill",
        "ship-tasks@srez-marketplace",
        "planning-only",
        "current или explicit Release",
        "Task Manager plugin остаётся adapter-only",
    )


def validate_strategic_skill(errors: list[str]) -> None:
    # These markers prove that the constitutional/source-separation wiring is
    # present. Readability itself requires the model-forward evaluation contract.
    validate_frontmatter(errors, STRATEGIC_SKILL, "strategic-explainer", 240)
    require(
        errors,
        STRATEGIC_SKILL,
        "routing skill к изолированному provider-subagent",
        "Сначала разреши роль",
        "STRATEGIC_EXPLAINER_PROVIDER_V1",
        "это терминальный provider",
        "Не исполняй\n  caller protocol",
        "references/provider-entrypoint.md",
        "никогда не переклассифицирует себя в caller",
        "Opaque client protocol",
        "Не готовь explanation candidate",
        "нового built-in `default` subagent",
        "fork_turns=\"none\"",
        "model=\"gpt-5.6-luna\"",
        "reasoning_effort=\"max\"",
        "Не наследуй current model/effort",
        "не подменяй недоступную Luna на SOL",
        "одна реальная user-facing formulation",
        "strategic summary",
        "publication-ready text",
        "STRATEGIC_EXPLAINER_INVOCATION_ERROR",
        "Публикуй только текст",
        "Routine chat",
    )
    require(
        errors,
        STRATEGIC_ENTRYPOINT,
        "provider-only admission contract",
        "STRATEGIC_EXPLAINER_PROVIDER_V1",
        "одну\nтерминальную роль",
        "Ты не caller, не router, не\ncoordinator и не evaluator",
        "Никогда не вызывай Strategic Explainer",
        "не создавай и не продолжай agents",
        "Admission до discovery",
        "Planning, decomposition, implementation, mutation",
        "STRATEGIC_EXPLAINER_INVOCATION_ERROR",
        "точный defect",
        "model=\"gpt-5.6-luna\"",
        "reasoning_effort=\"max\"",
        "Не исправляй собственный\nвызов и не запускай замену",
        "provider-contract.md",
    )
    require(
        errors,
        STRATEGIC_PROVIDER,
        "Внутренний контракт Strategic Explainer",
        "читает только terminal provider",
        "provider-entrypoint.md",
        "не вызывай Strategic Explainer",
        "не\n  создавай и не продолжай agents",
        "Глубоко разберись, но объясни только главное",
        "Твой продукт — понимание читателя",
        "Граница роли",
        "Установи исходный вопрос и факты",
        "Наблюдаемое ограничение не называй",
        "Одно наблюдение не обобщай",
        "source basis их не заменяет",
        "Собери strategic context снизу вверх",
        "current/accepted от proposed и historical",
        "Первый смысловой\nслой выделяет одну главную причинную мысль",
        "Строй публикацию из reader model",
        "Английские слова не должны нести основную мысль",
        "Действие формулируй через наблюдаемую операцию человека",
        "переводи внутренние компоненты в\nописании результата или границы",
        "Проверь понимание",
        "своими словами назвать",
        "внутренний\ncomprehension check без другого агента",
        "внешним model-forward\nevaluation harness",
        "Редакторская реконструкция",
        "неизменяемое ядро",
        "Сопоставь новую версию с исходником в обе стороны",
        "не добавляй решение или authority",
        "Completion gate",
        "Не смешивай source basis с publication text",
    )
    text = read(STRATEGIC_SKILL)
    for coupling in ("Task Manager", "TM-123"):
        if coupling in text:
            fail(errors, f"Strategic Explainer runtime is coupled to {coupling!r}")
    forbid(
        errors,
        STRATEGIC_SKILL,
        "одну главную причинную мысль",
        "первый смысловой слой",
        "неизменяемое смысловое ядро",
        "самостоятельно поднимись через применимые relations",
    )
    require(
        errors,
        STRATEGIC_METADATA,
        'display_name: "Strategic Explainer"',
        'short_description: "Передать объяснение отдельному чистому субагенту"',
        "$strategic-explainer:strategic-explainer",
        "router",
        "fork_turns=none",
        "gpt-5.6-luna",
        "reasoning_effort=max",
        "STRATEGIC_EXPLAINER_PROVIDER_V1",
        "одну короткую user-facing задачу",
        "resolvable read-only anchors",
        "allow_implicit_invocation: true",
    )
    forbid(
        errors,
        STRATEGIC_METADATA,
        "одну главную причинную мысль",
        "strategic meaning",
        "перестрой target text",
    )


def validate_strategic_provider_encapsulation(errors: list[str]) -> None:
    caller_files = (
        SHIP_SKILL,
        COMPOSER_SKILL,
        HANDOFF,
        REPORT,
        RUN_REPORT,
        AUTONOMY,
        CRITICAL_REVIEW,
        SHIP_REQUIREMENTS,
        SPEC,
        COMPOSER_REQUIREMENTS,
        COMPOSER_SPEC,
        REVIEW_MATRIX,
        COMPOSER_EVALUATION,
    )
    provider_markers = (
        "одну главную причинную мысль",
        "первый смысловой слой",
        "второй смысловой слой",
        "тот же quality contract",
        "применяет quality contract напрямую",
        "самостоятельно поднимись через",
        "Проверь понимание",
        "Редакторская реконструкция",
        "неизменяемое смысловое ядро",
        "английские слова не должны нести",
        "своими словами назвать",
        "Не придумывай варианты ради количества",
    )
    for path in caller_files:
        forbid(
            errors,
            path,
            *provider_markers,
            "strategic-explainer/references/provider-contract.md",
            "../strategic-explainer/references/provider-contract.md",
        )

    if len(read(HANDOFF).splitlines()) > 130:
        fail(errors, "ship-tasks Strategic Explainer client reference is not compact")

    require(
        errors,
        SHIP_SKILL,
        "ordinary `$strategic-explainer:strategic-explainer`",
        "иначе native",
        "ошибка выбранного provider-а\nпереводит mode в native",
        "не имитируй внутренний\nметод provider",
    )
    require(
        errors,
        COMPOSER_SKILL,
        'model="gpt-5.6-luna"',
        'reasoning_effort="max"',
        "Не наследуй current model/effort",
        "Не читай provider-internal contract",
        "не составляй explanation draft",
        "текст самостоятельно не улучшай",
    )
    require(
        errors,
        STRATEGIC_EVALUATION,
        "Provider encapsulation",
        "Terminal provider role",
        "Caller видит только router",
        "Provider contract загружается после admission",
        "Provider не вызывает себя и не оркестрирует agents",
        "Opt-out и недоступность не создают self-fallback",
    )
    require(
        errors,
        ADR["0030"],
        "Opaque provider boundary для Strategic Explainer",
        "двухслойным",
        "Только fresh subagent после успешного admission",
        "не включают self-fallback",
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
        "first-turn identity",
        "best-effort",
        "не более одной best-effort попытки",
        "отсутствие/deferred/failure не блокируют delivery",
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
    "Acceptance требует стандартный PDF/ZIP/PNG/изображение/Markdown, который агент может безопасно создать": (
        "synthetic fixture",
        "не считается blocker",
        "self-service",
    ),
    "Первый ingress для synthetic fixture не сработал": (
        "ingress failure",
        "другой безопасный supported path",
        "объявить product defect без attribution",
    ),
    "Acceptance требует второй principal, независимую сессию или provider-side evidence": (
        "authority blocker",
        "synthetic/ephemeral substitute",
        "blocker decision report",
        "менять ACL без authority",
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
    "Выбранная child Task принадлежит Epic": (
        "current Epic прочитан целиком",
        "применимые requirements/constraints/non-goals",
        "bounded Epic context implementation/reviewer",
        "только child scope",
        "игнорировать Epic",
    ),
    "Новая matching Task live Release остаётся в `Backlog`": (
        "исключена из delivery",
        "`Backlog` сохраняется",
        "не начинать implementation",
    ),
    "Blocking Task реализована и влита в exact integration candidate, но её functional verification пока недоступна": (
        "implementation gate открыт",
        "relation и attribution сохранены",
        "blocking Task остаётся правдиво non-terminal",
        "включить dependent Task в runnable frontier",
        "ждать `Done` blocking Task",
    ),
    "Изменение blocking Task существует только в writer branch/worktree или подтверждено лишь comment/status": (
        "dependency gate остаётся закрытым",
        "fan-in и общий contract не доказаны",
        "подтвердить exact integration candidate",
        "считать status/comment/isolated code достаточной",
    ),
    "После открытия dependency gate свежий attributed defect blocking Task нарушил contract dependent Task": (
        "только доказанно затронутые gates",
        "affected Tasks получают rework по evidence",
        "перепроверить affected downstream candidates",
        "массово инвалидировать batch",
    ),
    "Exact candidate/server path уже доказал authenticated product hang, а другой browser/controller просит новый login или MFA": (
        "verified-failure",
        "browser gap вторичен",
        "repair и retest продукта",
        "выдавать Chrome/login за repair",
    ),
    "Candidate blocker explanation обнаружило ранее пропущенный safe in-scope path": (
        "blocker decision остаётся provisional",
        "stale blocker candidate не публикуется",
        "primary sources/acceptance",
        "следующий user-facing result получает новый Explainer",
        "продолжать старый Explainer",
    ),
    "В current scope нет достаточного способа доказать success/failure после self-service frontier": (
        "verification-blocked",
        "In Review",
        "blocker decision report",
        "resume condition",
        "только при material выборе",
    ),
    "Fresh inventory ещё содержит matching `To Do` или `In Progress`, либо хотя бы одна `In Review` Task имеет доступный обычный test path": (
        "critical fallback не eligible",
        "обычную реализацию и честную functional verification",
        "закрывать доступную проверку code review-ом",
    ),
    "Все active Tasks находятся в `In Review`, обычная frontier исчерпана и каждая требует существенного human verifier": (
        "`To Do == 0`, `In Progress == 0`, `In Review > 0`",
        "ровно одного read-only `critic`",
        "`fork_turns=\"none\"`",
        "producer rationale",
        "bounded access unlock",
    ),
    "Critical reviewer доказал проблему в одной или нескольких Tasks": (
        "task-level `verified-failure`",
        "отдельный Strategic Explainer",
        "affected Tasks: `In Progress`",
        "точной attribution",
    ),
    "Critical reviewer grounded-одобрил exact candidate по коду, самостоятельно повторённым tests и связям": (
        "`critical-codebase-accepted`",
        "непроведённую functional check",
        "critic verdict",
        "residual risk",
        "`Done`",
        "называть outcome `verified-success`",
    ),
    "Critical reviewer не дал grounded approval или defect attribution": (
        "отсутствие findings не является approval",
        "оставить `In Review`",
        "симулировать независимый verdict",
    ),
    "Candidate, Task contract или active inventory изменился после critical review": (
        "disposition stale",
        "full eligibility gate",
        "status не меняется по stale verdict",
    ),
    "Effective user topology rule запрещает critic-субагента": (
        "critical fallback недоступен",
        "оставить affected Tasks в `In Review`",
        "изображать fresh independent review",
    ),
    "В batch scope накопились несколько совместимых ready candidates": (
        "лёгкий targeted gate",
        "периодический thorough review-batch gate",
        "один exact integrated candidate в UAT",
        "деплоить UAT после каждой bug/Task",
    ),
    "Достигнут UAT batch trigger (`batch_target`, review WIP, wave/frontier, общий effect, acceptance/Done, checkpoint или final flush)": (
        "UAT receipt/read-back",
        "один exact integrated candidate",
        "без отдельного approval",
        "назвать deploy verified без receipt",
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
    "Strategic Explainer отсутствует или завершился failure": (
        "переключён в native",
        "разрешённый transition выполняется",
        "блокировать comment/status",
    ),
    "Финальный ответ по однозначному результату": (
        "исходный вопрос и anchors всего run",
        "provider text без rewrite либо native grounded text",
        "склеить комментарии",
        "process diary",
    ),
    "Финальный ответ содержит сложный сбой, несколько инцидентов или сводный batch-результат": (
        "новая scope-level unit",
        "provider mode использует выбранный provider",
        "native mode пишет по ShipTask report contract",
        "продолжить прежний subagent",
    ),
    "Ordinary Explainer недоступен, но ответ пользователю уже должен быть дан": (
        "native mode сообщает установленные facts",
        "без служебного capability warning",
        "разрешённые transitions выполняются",
        "оставить пользователя без ответа",
        "эквивалентное provider quality",
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
        "ordinary исключён",
        "используется native",
        "имитировать provider method",
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
        "communication mode выбирается независимо",
    ),
    "Comment Explainer недоступен": (
        "mode native",
        "grounded comment публикуется",
        "comment-dependent transition выполняется",
        "без capability warning",
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
    require(
        errors,
        REVIEW_MATRIX,
        "## Матрица communication mode",
        "| установлен и разрешён | ordinary |",
        "| отсутствует или отключён | native |",
        "Failure выбранного provider-а переводит mode в native",
        "один corrected fresh retry",
    )
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
        (SHIP_REQUIREMENTS, "ST", 28),
        (COMPOSER_REQUIREMENTS, "TC", 12),
        (STRATEGIC_REQUIREMENTS, "SE", 17),
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
        if requirements == SHIP_REQUIREMENTS:
            require(
                errors,
                requirements,
                "Статус: действующий Level 1.",
                "полный набор действующих пользовательских требований только к",
                "не вправе ослаблять, заменять или молча удалять требования",
                "Смысл Level 1 меняется только по явному решению пользователя",
                "`architecture.md` описывает текущий инженерный способ",
                "семантически эквивалентным всем требованиям `ST-*`",
            )
        else:
            level_one_status = (
                "Статус: current Level 1, 2026-08-27"
                if requirements in (COMPOSER_REQUIREMENTS, STRATEGIC_REQUIREMENTS)
                else "Статус: current Level 1, 2026-08-26"
            )
            require(
                errors,
                requirements,
                level_one_status,
                "полный пользовательский исходный код только для",
                "не могут ослабить, заменить или\nмолча удалить",
                "Изменение смысла Level 1 требует явного решения пользователя",
                "`architecture.md` хранит agent-owned current способ достижения",
                "примерно\nэквивалентен",
            )

    require(
        errors,
        SHIP_REQUIREMENTS,
        "Backlog не входит в работу ShipTask",
        "явно перечисленные ссылки на Tasks образуют закрытое\nправило отбора",
        "Project, Release и однозначно определённый текущий\nобъём работ "
        "образуют динамический `selector`",
        "не считается\nрасширением объёма работ и не требует нового "
        "подтверждения",
        "отсутствие входа в другой браузер или MFA не\nостанавливает работу",
        "только\nпосле свежей проверки `selector`",
        "Goal хранит его идентичность и правило отбора",
        "Доказанный сбой продукта описывается раньше проблем с браузером",
        "Пользователь может обычным языком отключить ordinary Explainer полностью",
        "Общий запрет создавать subagents также\nисключает ordinary",
        "другой provider failure переводит communication mode в native",
        "Пользователь может обычным языком задать обязательное правило "
        "делегации",
        "точное или относительное число субагентов",
        "«ровно три» или\n  «используй побольше»",
        "«используй субагентов, только если работа\n  займёт больше получаса»",
        "Root agent не входит в явно указанное число\nсубагентов",
        "не\nподменяется молча",
        "Раскрывать внутренний расчёт\nчисла потоков необязательно",
        "Изоляция параллельных авторов изменений",
        "отдельном Git worktree и отдельной `feature branch`",
        "worktree с правом записи принадлежит ровно одному автору "
        "изменений и не\nиспользуется совместно с другими субагентами",
        "TASK CONTEXT ALARM",
        "Приоритет состояний и контекст дубликатов",
        "Ограниченный объём работ и сохранность чужого состояния",
        "Продолжение уже начатой работы",
        "После ошибки, остановки агента, прерывания запуска",
        "принимает эксклюзивное владение этим worktree",
        "ветка без доступного\nworktree",
        "двум авторам одновременно менять один worktree",
        "Независимое распространение plugin",
        "должны быть побайтно идентичны",
        "Периодические пакетные выпуски в UAT",
        "лёгкая целевая\nпроверка",
        "совместимые готовые версии объединяются в разумный и точно\n"
        "определённый пакет",
        "одну точно определённую интегрированную\nверсию",
        "без отдельного подтверждения",
        "развёртывание в UAT, повторную проверку опубликованного состояния,\n"
        "`smoke test`",
        "Критическая приёмка по кодовой базе при исчерпанном frontier",
        "`To Do` или `In Progress`",
        "человек должен сам стать содержательным проверяющим",
        "ровно одного специального read-only\nсубагента в роли `critic`",
        "`fork_turns=\"none\"`",
        "`critical-codebase-accepted`",
        "Task закрывается по критической проверке кодовой базы",
        "`blocked by` ограничивает доступность реализации, а не приёмку",
        "не требует, чтобы блокирующая Task перешла в\n`Done`",
        "влито в точный общий интеграционный candidate",
        "зависимая Task автоматически входит в runnable frontier",
        "может оставаться в `In Progress` или `In Review`",
        "не закрывают уже открытый dependency gate",
        "возвращает в rework только доказанно затронутые Tasks",
        "Epic задаёт смысл, но не расширяет Task",
        "перечитывает её\nтекущий parent chain до ближайшего применимого Epic",
        "получает любой исполнитель или reviewer",
        "не разрешает автоматически\nвыполнять sibling Tasks",
        "Strategic reflection до окончательной блокировки",
        "не публикует terminal blocker claim",
        "publication-ready explanation и\nего source basis",
        "stale candidate\nне публикуется",
        "один reflection pass",
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
        "Стратегическая преемственность от Epic к Task",
        "Уместные attachments из bug report",
        "Тип или формат attachment, включая screenshot, сам\nпо себе не делает материал ни уместным, ни неуместным",
        "native attachment той создаваемой\nTask",
        "Создание считается полным только когда read-back подтверждает\nкаждый обязательный attachment",
        "компактную самодостаточную проекцию",
        "Шаги исходного плана не превращаются в Tasks механически",
        "не\nрасширяет exact scope",
        "искусственный umbrella Epic",
        "Unknown outcome не\nповторяется вслепую",
        "должны быть byte-identical",
        "fork_turns=\"none\"",
        "model=\"gpt-5.6-luna\"",
        "reasoning_effort=\"max\"",
        "Current model/effort не\nнаследуются",
        "не подменяется Sol",
        "короткую задачу, exact planning scope и разрешимые source\nanchors",
        "автоматически вызывает новый экземпляр",
    )
    require(
        errors,
        STRATEGIC_REQUIREMENTS,
        "## Конституционное ядро",
        "Продукт Strategic Explainer —\nпонимание читателя",
        "Доказательства\nподтверждают сообщение, но не заменяют его",
        "если читатель не может\nпонять суть",
        "Никакой скрытой управляющей роли",
        "отсутствие проверки не называется\ndefect",
        "контекстный документ не является completion evidence",
        "Publication-ready и пропорциональный result",
        "Общий переносимый communication skill",
        "остаются byte-identical",
        "Редакторская реконструкция без потери смысла",
        "естественную профессиональную версию",
        "Редактура не меняет содержание",
        "Неясность или противоречие нельзя\nскрыть уверенной формулировкой",
        "не выдаёт редакторское решение за\nпользовательское требование",
        "переносятся\nдословно, включая написание и регистр",
        "Единый stateless API и чистый вызов",
        "fork_turns=\"none\"",
        "одна короткая, ёмкая, однозначная задача",
        "сам собирает current facts",
        "одну главную причинную мысль",
        "Один пользовательский результат на fresh invocation",
        "Изоляция provider expertise от caller",
        "opaque client protocol",
        "не получает, не читает и не применяет внутренние правила",
        "Единственная и терминальная provider-роль",
        "никогда не становится caller, router, coordinator или evaluator",
        "Provider не вызывает Strategic Explainer",
        "однозначный provider role lock",
        "STRATEGIC_EXPLAINER_INVOCATION_ERROR",
        "не запускает замену самостоятельно",
        "Publication text и source basis\nсемантически разделены",
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
    for architecture, prefix, status_marker in (
        (SPEC, "ST-*", "Статус: current Level 2 contract, 2026-08-27"),
        (COMPOSER_SPEC, "TC-*", "Статус: current Level 2 contract, 2026-08-27"),
        (STRATEGIC_SPEC, "SE-*", "Статус: current Level 2 contract, 2026-08-27"),
    ):
        require(
            errors,
            architecture,
            status_marker,
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
        "`blocked by` управляет доступностью реализации",
        "поздний defect\nинвалидирует только доказанно затронутые downstream results",
        "сохраняя применимый strategic\ncontext в каждой child Task",
        "ShipTask перечитывает current Epic",
        "не расширяет exact child scope",
        "новый Explainer result как\nreflection input",
    )
    require(
        errors,
        DOCS_INDEX,
        "[Source model](skills/README.md)",
        "[Requirements](skills/ship-tasks/requirements.md)",
        "[Architecture](skills/ship-tasks/architecture.md)",
        "[0028: Интегрированная реализация удовлетворяет `blocked by`]",
        "[0029: Fresh Strategic Explainer и reflection до blocker]",
        "[0031: Strategic Explainer как самостоятельный plugin]",
        "[0033: Terminal ordinary provider и optional routing ShipTask]",
        "[0034: Luna Max для ordinary Strategic Explainer]",
        "[Terminal Strategic Explainer и ShipTask routing: evaluation]",
    )
    require(
        errors,
        VISION,
        "Статус: current Level 2 strategic design, 2026-08-26",
        "[требованиях пользователя](requirements.md)",
    )


def validate_current_contract(errors: list[str]) -> None:
    require(
        errors,
        SPEC,
        "Статус: current Level 2 contract, 2026-08-27",
        "`ST-*` в локальных",
        "[требованиях пользователя](requirements.md)",
        "ADR-0018",
        "ADR-0019",
        "ADR-0020",
        "ADR-0021",
        "ADR-0022",
        "ADR-0024",
        "ADR-0025",
        "ADR-0026",
        "ADR-0027",
        "ADR-0028",
        "ADR-0029",
        "ADR-0031",
        "ADR-0033",
        "### 1.4 Dependency-ready frontier",
        "`Done` blocking Task в этот gate не входит",
        "Relation не удаляется",
        "не возвращает независимые Tasks в rework",
        "Dependency readiness управляет scheduling, но не release truth",
        "### 1.5 Epic context gate",
        "читает полный Epic",
        "self-contained implementation и review packet",
        "не добавляет sibling Tasks в selector",
        "task-contract-conflict` до\nзатронутой mutation",
        "другая independent runnable work\nпродолжается",
        "### 7.2 Per-Task gates и периодический UAT batch",
        "один deploy того же exact candidate в verified UAT",
        "standing authority периодического release",
        "не нужно спрашивать approval после каждой Task",
        "### 1.3 Best-effort название текущей Codex task",
        "best-effort попытки\nзаменить placeholder",
        "ровно одного current candidate",
        "не более одной попытки `codex_app__set_thread_title` без `threadId`",
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
        "ordinary `$strategic-explainer:strategic-explainer`, если он доступен и",
        "иначе native",
        "переводит mode в native",
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
        "Ordinary Strategic Explainer не относится к этой классификации",
        "exact Luna Max profile",
        "без profile escalation",
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
        "не читает и не имитирует provider method",
        "### 5.5 Критическая приёмка по кодовой базе",
        "every remaining blocker needs a human verifier, not an unlocker",
        "ровно одного read-only subagent role `critic`",
        "`fork_turns=\"none\"`",
        "`critical-codebase-accepted`",
        "не полноценной\nфункциональной приёмкой",
        "candidate report и перечитывает explanation/source basis",
        "candidate blocker не\nпубликуется",
        "один\nreflection pass",
    )
    require(
        errors,
        OVERVIEW,
        "Constitution-first подход",
        "comment read-back",
        "агент сам выбирает и меняет инструменты",
        "не обязывает чинить именно его",
        "непроведённая\n  functional check остаётся честно видна",
        "ADR-0018",
        "ADR-0019",
        "ADR-0020",
        "ADR-0021",
        "ADR-0022",
        "ADR-0024",
        "ADR-0025",
        "ADR-0026",
        "ADR-0027",
        "ADR-0028",
        "`blocked by` открывает dependent implementation",
        "late attributed defect инвалидирует",
        "гарантированной adapter capability",
        "каждый создаваемый ShipTask-комментарий",
        "durable Task history",
        "Goal используется только для прогресса массовой имплементации",
        "production release",
        "несколько независимых safe lanes",
        "genuinely simple\n  implementation/research packets получают Luna Max",
        "ordinary Strategic Explainer всегда\n  запускается на exact Luna Max",
        "без повторного Luna loop",
        "exact/relative count",
        "root\n  agent не считается названным субагентом",
        "condition",
        "собственной feature branch\n  и собственном Git worktree",
        "interrupted task-owned worktree/branch",
        "подхватывается следующей сессией",
        "best-effort",
        "последующие turns не переименовываются",
        "Project, Release и\nresolved current scope — live selectors",
        "без повторного approval",
        "Browser/controller/session switch — диагностический путь",
        "product outcome идёт раньше browser/OAuth logistics",
        "identity/predicate, не стартовый список или count",
        "лёгкий targeted gate",
        "один exact UAT deploy",
        "UAT — обычный разрешённый non-production effect",
        "`critical-codebase-accepted`",
        "`fork_turns=\"none\"`",
        "Task type хранится в Label/hierarchy",
        "не дублируется\nпрефиксом `BUG:`/`EPIC:`",
        "stateless API независимого объяснения",
        "fresh explanation как reflection",
    )
    require(
        errors,
        REPORT,
        "Инвариант effects",
        "До связанного существенного status transition",
        "transition не завершён",
        "всегда создаёт и перечитывает обязательный comment",
        "ordinary, если он доступен и\nразрешён, иначе native",
        "availability protocol",
        "native mode основной\nагент сообщает обязательные lifecycle facts",
        "Если provider отсутствует, отключён или завершился failure",
        "Обычный старт `To Do → In Progress` комментария не создаёт",
        "До repair немедленно сообщить incident",
        "resolution/completion comment",
        "Приёмка заблокирована",
        "рекомендуемый feasible способ",
        "каждые 10 минут",
        "ответ в Codex не являются durable Task comment",
        "непроведённую функциональную проверку",
        "критической проверке кодовой базы",
    )
    require(
        errors,
        RUN_REPORT,
        "authoritative source anchors и factual inventory",
        "В ordinary mode\nprovider получает одну короткую задачу",
        "проверяется только на material factual conflict",
        "не делает второй editorial rewrite",
        "без имитации provider",
        "краткий перечень существенных инцидентов, включая уже исправленные",
        "передача задачи с Luna на текущий профиль",
        "подхваченная незавершённая работа или невозможность безопасно продолжить её",
        "не совместим с формулировкой полного успеха",
        "заново перечитать полный список, включая Tasks",
        "Логистика браузера, OAuth или MFA идёт после этого",
        "Goal хранит правило принадлежности, а не стартовый список или\nсчётчик",
        "точка выпуска накопленного пакета",
        "подтверждение\nразвёртывания с повторным чтением",
        "пробелом доказательств, а не проверенным выпуском",
        "Tasks, закрытые через `critical-codebase-accepted`",
        "blocking/dependent Task refs",
        "Открытый implementation gate не выдаётся за upstream acceptance",
        "materially открытые или повторно закрытые dependency gates",
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
        "Периодический UAT batch",
        "не деплоит каждую bug/Task по умолчанию",
        "один thorough review-batch",
        "UAT deployment после проверки target",
        "отсутствие receipt не считается verified",
        "critical-codebase acceptance",
        "fresh full inventory без `To Do`/`In Progress`",
        "ровно один fresh-context\ncritic",
        "residual risk остаются видимыми",
        "Dependency-ready работа",
        "`blocked by` — structural relation и provenance",
        "Pending verification/effect сохраняет blocking Task",
        "Non-terminal upstream status",
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
        "Client protocol выбора Strategic Explainer",
        "$strategic-explainer:strategic-explainer",
        "Availability fallback",
        "Матрица выбора",
        "ordinary",
        "native",
        "Ordinary path",
        "нового built-in `default` read-only subagent",
        'model="gpt-5.6-luna"',
        'reasoning_effort="max"',
        "Не наследуй current model/effort",
        "не заменяй его скрыто на Sol",
        "STRATEGIC_EXPLAINER_PROVIDER_V1",
        "одну короткую user-facing formulation task",
        "Не\nчитай ordinary provider-only entrypoint",
        "готовый text и отдельно обозначенный source basis",
        "переводит\nrun в native mode",
        "Общий запрет создавать subagents также исключает ordinary",
        "Native path",
        "Обязательный comment всё равно публикуется и перечитывается",
        "Reflection до blocker",
    )
    require(
        errors,
        CRITICAL_REVIEW,
        "Eligibility gate",
        "`To Do == 0`, `In Progress == 0`, `In Review > 0`",
        "bounded unlocker",
        "ровно одного read-only subagent role `critic`",
        "`fork_turns=\"none\"`",
        "`critical-codebase-accepted`",
        "Mere absence of findings",
        "availability-selected Strategic Explainer",
        "residual knowledge boundary и риск",
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
    require(
        errors,
        ADR["0026"],
        "Периодические UAT releases разумными batch-группами",
        "per-Task targeted gate",
        "review-batch gate",
        "один deploy exact candidate в UAT",
        "standing delivery authority",
        "не превращает каждую Task в singleton",
        "UAT receipt/read-back",
        "Production release и его authority",
    )
    require(
        errors,
        ADR["0027"],
        "Критическая приёмка по кодовой базе при исчерпанном frontier",
        "`To Do == 0`, `In Progress == 0`",
        "содержательным verifier",
        "ровно один независимый read-only `critic`",
        "`fork_turns=\"none\"`",
        "`critical-codebase-accepted`",
        "отсутствие findings не равно approval",
        "отдельный Strategic Explainer",
        "более слабый, но явно маркированный terminal\noutcome",
        "не создаёт external effect",
    )
    require(
        errors,
        ADR["0028"],
        "Интегрированная реализация удовлетворяет `blocked by`",
        "Разделить structural relation, implementation readiness и terminal",
        "fan-in в integration target",
        "Не требовать terminal status blocking Task",
        "Dependent Task может достичь `Done`",
        "status == Done",
        "contract attribution",
    )
    require(
        errors,
        ADR["0029"],
        "Fresh Strategic Explainer и reflection до blocker",
        "Один stateless API",
        "fork_turns=\"none\"",
        "Caller передаёт одну короткую однозначную задачу",
        "Самостоятельное исследование и короткий result",
        "одну главную причинную мысль",
        "Blocker reflection",
        "не является evidence",
        "blocker не публикуется и работа продолжается",
        "один reflection pass",
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
            "CONTEXT_INTEGRITY_ERROR",
            "PROBLEM_CONTEXT_ERROR",
            "2–4 реально различающихся варианта",
            "2–4 реально различающихся способа",
        )
def validate_strategic_contract(errors: list[str]) -> None:
    require(
        errors,
        STRATEGIC_SPEC,
        "Статус: current Level 2 contract, 2026-08-27",
        "`SE-*` в локальных",
        "[требованиях пользователя](requirements.md)",
        "общего skill `$strategic-explainer`",
        "Конституционный принцип",
        "Продукт — понимание читателя",
        "publication text остаётся только то",
        "fresh stateless invocation",
        "Fresh API admission",
        "fork_turns=\"none\"",
        "model=\"gpt-5.6-luna\"",
        "reasoning_effort=\"max\"",
        "не наследует current\nmodel/effort",
        "compact selector",
        "Bounded strategic discovery",
        "независимо собрать current facts",
        "один самостоятельный user-facing result",
        "не придумывает alternatives ради количества",
        "Completion criteria",
        "Текст пишется на языке пользователя",
        "publication-ready result contract",
        "private evidence map",
        "reader model",
        "публикует только text",
        "пригоден для публикации",
        "Проверка понимания",
        "первый смысловой слой именно на исходный вопрос",
        "внешний model-forward\nevaluation harness",
        "единственным агентом своей publication unit",
        "Редакторская реконструкция",
        "неизменяемое смысловое ядро",
        "обратная проверка покрытия",
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
        "Уровень исходного вопроса",
        "обратным пересказом",
        "Publication text и source basis — разные продукты",
        "Редакторская реконструкция без потери смысла",
        "Свобода формы не означает свободу содержания",
        "Stateless invocation и publication unit",
        "fork_turns=\"none\"",
        "одна главная причинная мысль",
    )
    require(
        errors,
        STRATEGIC_EVALUATION,
        "Problem legitimacy",
        "Factual grounding и coverage",
        "Source state и relevance",
        "Read-only и authority boundary",
        "Human comprehension",
        "реальный model-forward\ngate",
        "exact `gpt-5.6-luna`",
        "reasoning_effort=\"max\"",
        "не заменяет Luna gate",
        "Один self-review генерирующего агента этого не\nдоказывает",
        "гибридную фразу с английским смысловым ядром",
        "первый смысловой слой прямо отвечает на исходный вопрос",
        "после удаления идентификаторов",
        "отдельный evaluator",
        "Простой вопрос, перегруженный техническим следом",
        "Production regression: завершение MD-325",
        "Task пока в `In Review`",
        "Исходный вопрос потерян внутри частной причины",
        "Сводный отчёт после нескольких технических инцидентов",
        "Независимый читатель не понял причинность",
        "пригоден для публикации",
        "Read-only boundary",
        "Реальный выбор способа проверки",
        "Редакторская целостность",
        "обратное сопоставление результата с исходником",
        "сохранены дословно, включая написание и\n  регистр",
        "Плотный документ требований",
        "Ясная структура с локальными языковыми дефектами",
        "Противоречие внутри редактируемого текста",
        "Fresh invocation admission",
        "Загрязнённый invocation",
        "Compact selector требует самостоятельного discovery",
        "Новый publication unit не продолжает старый candidate",
    )
    require(
        errors,
        TERMINAL_ROUTING_REPORT,
        "Terminal Strategic Explainer и ShipTask routing: evaluation",
        "STRATEGIC_EXPLAINER_INVOCATION_ERROR",
        "Provider children",
        "всех\n  provider trials было ноль дочерних agents",
        "все 20 model-forward cases получили финальный `PASS`",
        "Всего выполнено 22\ngeneration trials",
        "PASS after fresh retry",
        "ordinary → native",
        "переход provider failure в native",
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
            "ADR-0029",
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
        "0014": ("partially superseded", "ADR-0021", "ADR-0029"),
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
        "0021": (
            "partially superseded",
            "ADR-0022",
            "ADR-0024",
            "ADR-0025",
            "ADR-0029",
        ),
        "0022": ("partially superseded", "ADR-0024", "ADR-0029", "ADR-0033"),
        "0030": ("частично заменено ADR-0033",),
        "0031": ("частично заменено ADR-0033",),
        "0025": ("частично заменено ADR-0034",),
        "0033": ("частично заменено", "ADR-0034"),
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
        "не выводит из status\n  blocking Task business-решение о runnable frontier",
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
        "fresh Codex session",
    )
    require(
        errors,
        ADR["0031"],
        "Strategic Explainer как самостоятельный plugin",
        "Изменяет distribution-часть",
        "strategic-explainer@srez-marketplace",
        "$strategic-explainer:strategic-explainer",
        "ship-tasks@srez-marketplace` содержит только `ship-tasks` и\n  `task-composer`",
        "provider contract в этот package не копируется",
        "logical runtime\n  dependency",
        "не поддерживает\nplugin-to-plugin dependency",
        "fail-closed",
        "repository validator запрещает `skills/strategic-explainer` внутри\n  `plugins/ship-tasks`",
        "fresh Codex session видит `$strategic-explainer:strategic-explainer`",
        "не\n  видит прежний `$ship-tasks:strategic-explainer`",
    )
    require(
        errors,
        ADR["0033"],
        "Terminal ordinary provider и optional routing ShipTask",
        "STRATEGIC_EXPLAINER_PROVIDER_V1",
        "не становится caller",
        "не создаёт и не продолжает agents",
        "STRATEGIC_EXPLAINER_INVOCATION_ERROR",
        "ordinary Strategic Explainer",
        "native ShipTask writing",
        "не более одного provider",
        "не создают capability warning",
        "не блокируют разрешённый status\ntransition",
        "Task Composer не наследует новый routing автоматически",
    )
    require(
        errors,
        ADR["0034"],
        "Luna Max для ordinary Strategic Explainer",
        'fork_turns="none"',
        'model="gpt-5.6-luna"',
        'reasoning_effort="max"',
        "Current caller model/effort не наследуются",
        "без plugin-а основной агент пишет сам",
        "без secondary\n  provider retry",
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
        "Два Marketplace package",
        "Srez Marketplace/plugins/strategic-explainer/skills/strategic-explainer",
        "Srez Marketplace/plugins/ship-tasks/skills/strategic-explainer` отсутствует",
        "strategic-explainer@srez-marketplace",
        "ShipTask использует\n  `$strategic-explainer:strategic-explainer`",
        "task-manager@srez-marketplace` остаётся adapter-only",
        "в начале run ShipTask\n  выбирает ordinary",
        "выбирает ordinary при его наличии и разрешении, иначе native",
        "failure provider-а переводит run прямо в native",
        "exact terminal provider role lock",
        "не блокирует comment/status",
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
        "catalog placeholder при доступной host title capability",
        "best-effort попытку `ShipTask · ...`",
        "ambiguous candidate не\n  переименовываются",
    )
    require(
        errors,
        ROOT / "README.md",
        "Runtime публикуется двумя независимыми plugin",
        "ship-tasks@srez-marketplace`\nсодержит ShipTask и Task Composer",
        "strategic-explainer@srez-marketplace` — только ordinary Strategic Explainer",
        "Codex manifest не умеет автоматически\nустанавливать plugin dependency",
        "$strategic-explainer:strategic-explainer",
        "Каждый repository source\nсверяется со своим Marketplace package и installed plugin cache",
    )
    require(
        errors,
        DEVELOPMENT,
        "два независимых plugin",
        "ship-tasks@srez-marketplace",
        "strategic-explainer@srez-marketplace",
        "$strategic-explainer:strategic-explainer",
        "plugin-to-plugin dependency",
        "availability-based optional routing",
        "plugins/ship-tasks/skills/strategic-explainer",
        "отсутствует",
    )
    require(
        errors,
        SHIP_REQUIREMENTS,
        "strategic-explainer@srez-marketplace",
        "$strategic-explainer:strategic-explainer",
        "ShipTask не содержит его копии",
        "не поддерживает нативную plugin-to-plugin dependency",
        "optional communication enhancement",
        "его отсутствие выбирает native mode",
    )
    require(
        errors,
        SPEC,
        "ShipTask package не содержит runtime Explainer",
        "$strategic-explainer:strategic-explainer",
        "нормальным native mode",
        "встроенной копией",
    )
    require(
        errors,
        COMPOSER_REQUIREMENTS,
        "$strategic-explainer:strategic-explainer",
        "копия provider-а в ShipTask package\nне встраивается",
        "plugin-qualified skill проверяется в fresh Codex\nsession",
    )
    require(
        errors,
        COMPOSER_SPEC,
        "ADR-0031",
        "$strategic-explainer:strategic-explainer",
        "отдельно установленного",
        'model="gpt-5.6-luna"',
        'reasoning_effort="max"',
        "Current caller profile не наследуется",
        "не\nподменяет недоступную Luna на Sol",
    )
    require(
        errors,
        STRATEGIC_REQUIREMENTS,
        "самостоятельный plugin\n`strategic-explainer@srez-marketplace`",
        "$strategic-explainer:strategic-explainer",
        "model=\"gpt-5.6-luna\"",
        "reasoning_effort=\"max\"",
        "не разрешает скрытую подмену SOL",
        "не встраивается в\n`ship-tasks@srez-marketplace`",
    )
    require(
        errors,
        STRATEGIC_SPEC,
        "ADR-0031",
        "strategic-explainer@srez-marketplace` содержит только source\n`strategic-explainer/`",
        "strategic-explainer:strategic-explainer",
        "не получают provider reference в собственный plugin",
    )

    current_distribution_files = (
        ROOT / "AGENTS.md",
        ROOT / "README.md",
        DEVELOPMENT,
        SHIP_SKILL,
        SHIP_METADATA,
        COMPOSER_SKILL,
        COMPOSER_METADATA,
        STRATEGIC_SKILL,
        STRATEGIC_METADATA,
        SHIP_REQUIREMENTS,
        SPEC,
        COMPOSER_REQUIREMENTS,
        COMPOSER_SPEC,
        STRATEGIC_REQUIREMENTS,
        STRATEGIC_SPEC,
        OVERVIEW,
        STRATEGIC_EVALUATION,
        COMPOSER_EVALUATION,
        REVIEW_MATRIX,
        REPORT,
        RUN_REPORT,
        AUTONOMY,
        MEMORY,
        HANDOFF,
        CRITICAL_REVIEW,
    )
    for path in current_distribution_files:
        forbid(errors, path, "$ship-tasks:strategic-explainer")

    forbid(
        errors,
        DEVELOPMENT,
        "Единственная runtime-distribution — sibling skills в plugin\n`ship-tasks@srez-marketplace`",
        "Синхронизируйте все три marketplace skill directory",
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
        "один Strategic Explainer при разрешённой роли",
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
        "Auto-title является отдельным best-effort UI convenience",
        "адресация только calling task",
        "Type Labels не должны дублироваться в title",
        "legacy-prefixed title участвует в\nduplicate search",
        "Не вычисляйте dependency-ready frontier по `status == Done`",
        "blocking Task с влитым в exact integration candidate нужным contract",
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
        ADR["0026"],
        ADR["0030"],
        ADR["0031"],
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
        validate_strategic_provider_encapsulation(errors)
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
