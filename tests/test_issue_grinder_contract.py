from __future__ import annotations

import re
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "issue-grinder"
REQUIREMENTS = ROOT / "docs" / "skills" / "issue-grinder" / "requirements.md"
ARCHITECTURE = ROOT / "docs" / "skills" / "issue-grinder" / "architecture.md"
EVALUATION = ROOT / "docs" / "skills" / "issue-grinder" / "evaluation.md"
WRITER_GUARD = SKILL_ROOT / "scripts" / "writer_worktree_guard.py"


class IssueGrinderContractTest(unittest.TestCase):
    def test_runtime_has_no_placeholders_and_declares_exact_routing(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        metadata = (SKILL_ROOT / "agents" / "openai.yaml").read_text(
            encoding="utf-8"
        )
        runtime = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted(SKILL_ROOT.rglob("*.md"))
        )
        runtime = re.sub(r"\s+", " ", runtime)

        self.assertIn("name: issue-grinder", skill)
        self.assertNotIn("[TODO", runtime)
        self.assertIn("$issue-grinder", skill.split("---", 2)[1])
        self.assertIn("Не использовать для Backlog", skill.split("---", 2)[1])
        self.assertIn('display_name: "Issue Grinder"', metadata)
        self.assertIn('value: "task-manager"', metadata)
        self.assertIn("allow_implicit_invocation: true", metadata)

    def test_hard_invariants_are_compiled_into_runtime(self) -> None:
        runtime = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted(SKILL_ROOT.rglob("*.md"))
        )
        runtime = re.sub(r"\s+", " ", runtime)
        for invariant in (
            "candidate blocker → причинное объяснение → reflection",
            "post-explanation reflection",
            "update_goal(status=blocked)",
            "одного совпадения selector-а недостаточно",
            "report не задерживается",
            "будущих run",
            "одинаковая попытка с тем же результатом",
            "Issue Grinder ·",
            "не более одного раза без",
            "Meaningful title",
            "To Do → In Progress",
            "comment committed / status failed",
            "Blind retry",
            "Production запрещён",
            "публичного UAT",
            "Да всегда",
            "собственные feature branch и Git worktree",
            "Writer admission — hard gate",
            "admission-only",
            "integration checkout read-only",
            "assert-unchanged",
            "Luna retry loop",
            "$strategic-explainer:strategic-explainer",
            "только пользователю в чате",
        ):
            self.assertIn(invariant, runtime)

    def test_every_level_one_id_has_one_evaluation_row(self) -> None:
        requirements = REQUIREMENTS.read_text(encoding="utf-8")
        evaluation = EVALUATION.read_text(encoding="utf-8")
        requirement_ids = set(re.findall(r"`(IG-[A-Z]+-\d{2})`", requirements))
        rows = re.findall(r"^\| `(IG-[A-Z]+-\d{2})` \|", evaluation, re.MULTILINE)

        self.assertEqual(len(rows), len(set(rows)), "duplicate coverage rows")
        self.assertEqual(set(rows), requirement_ids)
        self.assertEqual(len(requirement_ids), 39)

    def test_architecture_runtime_layout_exists(self) -> None:
        architecture = ARCHITECTURE.read_text(encoding="utf-8")
        for relative in (
            "SKILL.md",
            "agents/openai.yaml",
            "references/task-manager-flow.md",
            "references/thread-title.md",
            "references/autonomy-and-environments.md",
            "references/multi-agent-execution.md",
            "references/strategic-explainer.md",
            "scripts/writer_worktree_guard.py",
        ):
            self.assertTrue((SKILL_ROOT / relative).is_file(), relative)
            self.assertIn(Path(relative).name, architecture)

    def test_writer_guard_is_fail_closed_and_part_of_runtime(self) -> None:
        guard = WRITER_GUARD.read_text(encoding="utf-8")
        for invariant in (
            'WRITER_SCHEMA = "issue-grinder/writer-worktree/v1"',
            'GUARD_SCHEMA = "issue-grinder/integration-guard/v1"',
            'commands.add_parser("prepare")',
            'commands.add_parser("admit")',
            'commands.add_parser("snapshot")',
            'commands.add_parser("assert-unchanged")',
            '"worktree",\n        "add",\n        "--lock"',
            'return 2',
        ):
            self.assertIn(invariant, guard)
        self.assertNotIn('"--force"', guard)


if __name__ == "__main__":
    unittest.main()
