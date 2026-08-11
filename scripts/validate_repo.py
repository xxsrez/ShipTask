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
DOCS_INDEX = ROOT / "docs" / "README.md"

REQUIRED_FILES = (
    ROOT / "README.md",
    ROOT / "AGENTS.md",
    ROOT / ".gitignore",
    ROOT / ".gitattributes",
    SKILL_FILE,
    OPENAI_FILE,
    DOCS_INDEX,
)

FORBIDDEN_SKILL_PATTERNS = {
    "ExampleNotes": re.compile(r"mind\s*diary", re.IGNORECASE),
    "Linear": re.compile(r"\blinear\b", re.IGNORECASE),
    "Sites": re.compile(r"\bsites\b", re.IGNORECASE),
    "UAT": re.compile(r"\buat\b", re.IGNORECASE),
    "legacy skill name": re.compile(
        r"ship-(?:linear|work)-release", re.IGNORECASE
    ),
    "release-specific wording": re.compile(r"\brelease\b", re.IGNORECASE),
}

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
    for label, pattern in FORBIDDEN_SKILL_PATTERNS.items():
        match = pattern.search(text)
        if match:
            line = text.count("\n", 0, match.start()) + 1
            fail(errors, f"SKILL.md contains {label} residue at line {line}")

    metadata = OPENAI_FILE.read_text(encoding="utf-8")
    required_fragments = (
        'display_name: "Ship Tasks"',
        'short_description: "Довести известный task scope до результата"',
        "$ship-tasks",
        "allow_implicit_invocation: false",
    )
    for fragment in required_fragments:
        if fragment not in metadata:
            fail(errors, f"agents/openai.yaml is missing {fragment!r}")


def markdown_files() -> list[Path]:
    roots = [ROOT / "README.md", ROOT / "AGENTS.md", SKILL_FILE]
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
