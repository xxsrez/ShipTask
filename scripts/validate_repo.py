#!/usr/bin/env python3
"""Validate the portable ShipTask repository without third-party packages."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "ship-tasks"
SKILL_FILE = SKILL_DIR / "SKILL.md"
OPENAI_FILE = SKILL_DIR / "agents" / "openai.yaml"
REPORT_REFERENCE = SKILL_DIR / "references" / "delivery-report.md"
AUTONOMY_REFERENCE = SKILL_DIR / "references" / "autonomy-and-release.md"
DOCS_INDEX = ROOT / "docs" / "README.md"
SPEC_FILE = ROOT / "docs" / "specs" / "ship-tasks.md"
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

REQUIRED_FILES = (
    ROOT / "README.md",
    ROOT / "AGENTS.md",
    ROOT / ".gitignore",
    ROOT / ".gitattributes",
    SKILL_FILE,
    OPENAI_FILE,
    REPORT_REFERENCE,
    AUTONOMY_REFERENCE,
    DOCS_INDEX,
    SPEC_FILE,
    DECISION_FILE,
    REPORT_DECISION_FILE,
    COMMENT_REPORT_DECISION_FILE,
    AUTONOMY_DECISION_FILE,
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
        'short_description: "Доставить Task Manager scope до результата"',
        "$ship-tasks",
        'value: "task-manager"',
        "allow_implicit_invocation: false",
    )
    for fragment in required_fragments:
        if fragment not in metadata:
            fail(errors, f"agents/openai.yaml is missing {fragment!r}")


def validate_workflow_contract(errors: list[str]) -> None:
    required_skill_fragments = (
        "Вызвать `get_goal`",
        "Любая `In Review` Task означает `completion-remains`",
        "per-Task targeted gate",
        "review-batch gate",
        "passing exact batch gate",
        "final review batch прошёл gate",
        "delivery-report reference",
        "native comment-create",
        "`not-available`",
        "Никогда не писать",
        "autonomy and release reference",
        "Не задавать пользователю вопрос",
        "`deferred`",
        "`runnable_count = 0`",
        "Review precedence",
        "verified non-production target",
        "Никогда не выполнять production release",
    )
    required_spec_fragments = (
        "### 5.3 Terminal invariant и acceptance authority",
        "### 6.1 Двухуровневая verification",
        "Не запускать полный дорогой project gate для каждой Task",
        "Failed batch gate сначала локализовать",
        "final review batch прошёл gate",
        "### 9.1 Delivery report как Task comment",
        "не блокирует `Done`",
        "Никогда не записывать report в `description`",
        "### 5.4 Autonomous continuation и task-local defer",
        "### 5.5 Environment и release authority",
        "`production-approval-required`",
        "одну consolidated decision queue",
        "blocking input запрещён",
        "non-blocking final finding",
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
        "COMPLETED",
        "ACCEPTANCE READY",
        "REWORK REQUIRED",
        "Confidence: CONFIRMED | PROBABLE | UNKNOWN",
    ):
        if fragment not in report_text:
            fail(errors, f"delivery-report reference is missing {fragment!r}")

    autonomy_text = AUTONOMY_REFERENCE.read_text(encoding="utf-8")
    for fragment in (
        "Decision ladder",
        "Не задавать пользователю вопрос посреди runnable queue",
        "runnable_count = actionable To Do",
        "blocking input",
        "Deferred Task",
        "обязательно опубликовать",
        "Non-production release",
        "Production release требует explicit user approval",
        "production-approval-required",
        "Deferred-only handoff",
    ):
        if fragment not in autonomy_text:
            fail(errors, f"autonomy reference is missing {fragment!r}")

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
