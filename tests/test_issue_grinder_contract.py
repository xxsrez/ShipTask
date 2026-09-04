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
ROUTING_GUARD = SKILL_ROOT / "scripts" / "model_routing_guard.py"


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
            "для каждой причины дай отдельный ответ",
            "почему она блокирует обязательный результат активного issue",
            "почему Issue Grinder не может устранить её сам",
            "зачем этот шаг нужен issue contract",
            "post-explanation reflection",
            "update_goal(status=blocked)",
            "одного совпадения selector-а для continuity недостаточно",
            "не сам report",
            "будущих run",
            "Одинаковая попытка без нового evidence",
            "Issue Grinder ·",
            "не более одного раза без",
            "Meaningful title",
            "To Do → In Progress",
            "comment committed / status failed",
            "Blind retry",
            "Production запрещён",
            "публичный UAT",
            "Да всегда",
            "собственные feature branch и Git worktree",
            "Writer admission — hard gate",
            "admission-only",
            "integration checkout read-only",
            "assert-unchanged",
            "Luna retry loop",
            "$strategic-explainer:strategic-explainer",
            "только пользователю в чате",
            "Strategic Outcome — постоянный ориентир исполнения",
            "empty active scope остаётся достаточным",
            "не превращай в источник новых Requirements",
            "применимые Human Requirements и отличимый Agent Plan",
        ):
            self.assertIn(invariant, runtime)

    def test_every_level_one_id_has_one_evaluation_row(self) -> None:
        requirements = REQUIREMENTS.read_text(encoding="utf-8")
        evaluation = EVALUATION.read_text(encoding="utf-8")
        requirement_ids = set(re.findall(r"`(IG-[A-Z]+-\d{2})`", requirements))
        rows = re.findall(r"^\| `(IG-[A-Z]+-\d{2})` \|", evaluation, re.MULTILINE)

        self.assertEqual(len(rows), len(set(rows)), "duplicate coverage rows")
        self.assertEqual(set(rows), requirement_ids)
        self.assertEqual(len(requirement_ids), 60)

    def test_architecture_runtime_layout_exists(self) -> None:
        architecture = ARCHITECTURE.read_text(encoding="utf-8")
        for relative in (
            "SKILL.md",
            "agents/openai.yaml",
            "references/task-manager-flow.md",
            "references/thread-title.md",
            "references/autonomy-and-environments.md",
            "references/mode-help.md",
            "references/run-and-goal.md",
            "references/execution-modes.md",
            "references/modes/solo.md",
            "references/modes/classic.md",
            "references/modes/balance.md",
            "references/modes/swarm.md",
            "references/modes/economical.md",
            "references/multi-agent-execution.md",
            "references/strategic-explainer.md",
            "scripts/model_routing_guard.py",
            "scripts/writer_worktree_guard.py",
        ):
            self.assertTrue((SKILL_ROOT / relative).is_file(), relative)
            self.assertIn(Path(relative).name, architecture)

    def test_execution_mode_runtime_and_evaluation_surfaces_are_wired(self) -> None:
        execution_modes = (
            SKILL_ROOT / "references" / "execution-modes.md"
        ).read_text(encoding="utf-8")
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        architecture = ARCHITECTURE.read_text(encoding="utf-8")
        evaluation = EVALUATION.read_text(encoding="utf-8")

        mode_files = {
            "Соло": "solo.md",
            "Классический": "classic.md",
            "Баланс": "balance.md",
            "Менеджер": "swarm.md",
            "Экономичный": "economical.md",
        }
        self.assertEqual(
            re.findall(
                r"^## (Соло|Классический|Баланс|Менеджер|Экономичный)$",
                execution_modes,
                re.MULTILINE,
            ),
            [],
        )
        for mode, filename in mode_files.items():
            mode_runtime = (
                SKILL_ROOT / "references" / "modes" / filename
            ).read_text(encoding="utf-8")
            self.assertEqual(
                re.findall(
                    r"^# (Соло|Классический|Баланс|Менеджер|Экономичный)$",
                    mode_runtime,
                    re.MULTILINE,
                ),
                [mode],
            )
            self.assertIn(f"modes/{filename}", execution_modes)
            self.assertIn(filename, architecture)
            self.assertIn(filename, evaluation)
        self.assertIn(
            "Число Issue Grinder execution-subagents и одновременных\n"
            "   содержательных execution lanes всегда равно `0` и `1`",
            (SKILL_ROOT / "references" / "modes" / "solo.md").read_text(
                encoding="utf-8"
            ),
        )
        self.assertIn(
            "Это правило одинаково для всех пяти execution modes",
            (SKILL_ROOT / "references" / "strategic-explainer.md").read_text(
                encoding="utf-8"
            ),
        )
        self.assertIn("[Execution modes](references/execution-modes.md)", skill)
        self.assertIn("ровно один связанный там файл", skill)
        self.assertIn("scripts/issue_grinder_mode_harness.py", architecture)
        self.assertIn("scripts/issue_grinder_mode_harness.py", evaluation)
        self.assertIn(
            "scripts/issue_grinder_mode_loading_smoke.py", architecture
        )
        self.assertIn(
            "scripts/issue_grinder_mode_loading_smoke.py", evaluation
        )
        self.assertIn(
            "scripts/issue_grinder_solo_topology_smoke.py", architecture
        )
        self.assertIn(
            "scripts/issue_grinder_solo_topology_smoke.py", evaluation
        )

    def test_mode_help_is_a_delivery_free_progressive_disclosure_path(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        mode_help = (SKILL_ROOT / "references" / "mode-help.md").read_text(
            encoding="utf-8"
        )
        architecture = ARCHITECTURE.read_text(encoding="utf-8")

        self.assertIn("[краткую справку](references/mode-help.md)", skill)
        self.assertIn("[Run, scope и Goal](references/run-and-goal.md)", skill)
        self.assertLess(len(skill.splitlines()), 190)
        for mode in ("Соло", "Классический", "Баланс", "Менеджер", "Экономичный"):
            self.assertIn(f"`{mode}`", mode_help)
        for forbidden_effect in (
            "не разрешает Task Manager scope",
            "не создаёт Goal",
            "не обращается к Task Manager",
            "не вызывает subagents",
        ):
            self.assertIn(forbidden_effect, mode_help)
        self.assertIn("`По умолчанию` — не шестой режим", mode_help)
        self.assertIn("## Главное различие Классического и Баланса", mode_help)
        self.assertIn("основной исполнитель делает почти всё", mode_help)
        self.assertIn(
            "до\nтрёх готовых независимых write-пакетов Luna High",
            mode_help,
        )
        self.assertIn("заканчивает сама", mode_help)
        self.assertIn("observable negative-effects\ncontract `IG-HELP-01`", architecture)

    def test_writer_guard_is_fail_closed_and_part_of_runtime(self) -> None:
        guard = WRITER_GUARD.read_text(encoding="utf-8")
        for invariant in (
            'WRITER_SCHEMA = "issue-grinder/writer-worktree/v1"',
            'GUARD_SCHEMA = "issue-grinder/integration-guard/v1"',
            'commands.add_parser("prepare")',
            'commands.add_parser("resume")',
            'commands.add_parser("admit")',
            'commands.add_parser("snapshot")',
            'commands.add_parser("assert-unchanged")',
            '"worktree",\n        "add",\n        "--lock"',
            'return 2',
        ):
            self.assertIn(invariant, guard)
        self.assertNotIn('"--force"', guard)

    def test_model_routing_guard_is_fail_closed_and_part_of_runtime(self) -> None:
        guard = ROUTING_GUARD.read_text(encoding="utf-8")
        execution_modes = (
            SKILL_ROOT / "references" / "execution-modes.md"
        ).read_text(encoding="utf-8")
        multi_agent = (
            SKILL_ROOT / "references" / "multi-agent-execution.md"
        ).read_text(encoding="utf-8")

        for marker in (
            "issue-grinder/model-routing/v2",
            "gpt-5.6-luna",
            "dispatch_fingerprint",
            "actual_luna_model_mismatch",
        ):
            self.assertIn(marker, guard)
        self.assertNotIn("FORCED_PROFILE_AGENT_TYPES", guard)
        self.assertNotIn("platform_agent_type_bypasses_mode_profile", guard)
        self.assertIn("Model routing — hard gate", execution_modes)
        self.assertIn("Model routing admission — hard gate", multi_agent)

    def test_balance_compiles_luna_execution_plane_and_final_control(self) -> None:
        balance = (
            SKILL_ROOT / "references" / "modes" / "balance.md"
        ).read_text(encoding="utf-8")
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        requirements = REQUIREMENTS.read_text(encoding="utf-8")
        architecture = ARCHITECTURE.read_text(encoding="utf-8")
        evaluation = EVALUATION.read_text(encoding="utf-8")

        for marker in (
            "не больше\n   трёх Luna workers",
            '`model="gpt-5.6-luna"`,',
            '`reasoning_effort="high"`',
            "одним collective event-driven wait",
            "механически переносит task-owned commits/bytes",
            "одним parallel tool batch",
            "independent reviewer не является штатной ролью",
            "final acceptance main profile",
        ):
            self.assertIn(marker, balance)

        self.assertIn("до трёх independent Luna", skill)
        self.assertIn("ограниченной параллельной помощью Luna", requirements)
        self.assertIn("Balance: ускоренный main-owned workflow", architecture)
        self.assertIn("balance-main-final-acceptance", evaluation)

    def test_non_solo_capability_aware_stage_contract_is_compiled(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        execution_modes = (
            SKILL_ROOT / "references" / "execution-modes.md"
        ).read_text(encoding="utf-8")
        multi_agent = (
            SKILL_ROOT / "references" / "multi-agent-execution.md"
        ).read_text(encoding="utf-8")
        requirements = REQUIREMENTS.read_text(encoding="utf-8")
        architecture = ARCHITECTURE.read_text(encoding="utf-8")
        evaluation = EVALUATION.read_text(encoding="utf-8")

        combined = "\n".join((architecture, skill, execution_modes, multi_agent))
        self.assertIn("nested delegation", combined.casefold())
        self.assertIn("direct luna", combined.casefold())
        self.assertTrue("event" in combined.casefold() or "событийн" in combined.casefold())
        for mode in ("classic", "balance", "swarm", "economical"):
            mode_runtime = (
                SKILL_ROOT / "references" / "modes" / f"{mode}.md"
            ).read_text(encoding="utf-8")
            self.assertIn("event-driven wait", mode_runtime)
        self.assertIn("IG-MA-19", requirements)
        self.assertIn("capability-aware-direct-stages", evaluation)
        self.assertIn("pre-dispatch guard ×1 → spawn owner ×1 → event wait ×1", architecture)
        self.assertIn("Для каждого нового direct owner-а", multi_agent)
        self.assertIn("multi-target/event mechanism", multi_agent)

    def test_model_forward_tuning_uses_one_hour_and_holdout(self) -> None:
        evaluation = EVALUATION.read_text(encoding="utf-8")

        self.assertIn("потолок `3 600` секунд", evaluation)
        self.assertIn("одного поля manifest", evaluation)
        self.assertIn("десятиминутного checkpoint", evaluation)
        self.assertIn("holdout", evaluation)
        self.assertIn("не участвовавший в правках", evaluation)

    def test_balance_wave_and_manager_loop_are_compiled(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        modes_root = SKILL_ROOT / "references" / "modes"
        balance = (modes_root / "balance.md").read_text(encoding="utf-8")
        swarm = (modes_root / "swarm.md").read_text(encoding="utf-8")
        multi_agent = (
            SKILL_ROOT / "references" / "multi-agent-execution.md"
        ).read_text(encoding="utf-8")

        self.assertIn("local model-forward evaluation", skill)
        self.assertIn("не объединяй\nв обрезаемый", skill)
        self.assertIn("до трёх independent Luna", skill)
        for marker in (
            "не больше\n   трёх Luna workers",
            "одну active wave",
            "collective event-driven wait",
            "parallel tool batch",
            "Отдельный independent reviewer не является штатной ролью",
        ):
            self.assertIn(marker, balance)
        self.assertIn("Open-ended fuzzing", swarm)
        self.assertIn("shadow tree", balance)
        self.assertIn("shadow tree", swarm)
        self.assertIn("shadow tree", multi_agent)
        normalized_swarm = " ".join(swarm.split())
        for marker in (
            "Manager Loop",
            "постоянную manager session",
            "постоянную implementer session",
            "ровно одна phase/rework wave",
            "Best-of-N",
            "не делегирует descendants",
            "sibling messaging не является",
        ):
            self.assertIn(marker, normalized_swarm)
        self.assertIn("постоянные direct Luna manager и implementer", multi_agent)
        self.assertIn("одним\nмеханическим действием", multi_agent)
        self.assertIn("не ищет tool\ncatalog и parent messaging", multi_agent)
        self.assertIn("технически вернул\ntimeout", multi_agent)

    def test_publication_unit_stays_with_coordinator(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        multi_agent = (
            SKILL_ROOT / "references" / "multi-agent-execution.md"
        ).read_text(encoding="utf-8")
        explainer = (
            SKILL_ROOT / "references" / "strategic-explainer.md"
        ).read_text(encoding="utf-8")
        architecture = ARCHITECTURE.read_text(encoding="utf-8")

        for text in (skill, multi_agent, explainer, architecture):
            self.assertIn("facts", text)
            self.assertIn("evidence", text)
            self.assertIn("anchors", text)
        self.assertIn("всей publication unit", skill)
        self.assertIn("не поручай им формулировать comment", skill)
        self.assertIn("не вызывает Strategic Explainer", multi_agent)
        self.assertIn("`create_thread`", multi_agent)
        self.assertIn("provider наблюдается\nкак его прямой built-in child", architecture)
        self.assertIn("не получает пакет «сформулировать комментарий»", architecture)
        self.assertIn("provider-child как reusable channel", architecture)
        self.assertIn("`followup_task` или\n`send_message`", architecture)
        self.assertIn("Каждый завершившийся facade call закрыт навсегда", explainer)
        self.assertIn("вообще не вызывает facade", explainer)

    def test_automatic_blocker_audit_does_not_repeat_human_wait_work(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        run_goal = (
            SKILL_ROOT / "references" / "run-and-goal.md"
        ).read_text(encoding="utf-8")
        explainer = (
            SKILL_ROOT / "references" / "strategic-explainer.md"
        ).read_text(encoding="utf-8")
        architecture = ARCHITECTURE.read_text(encoding="utf-8")
        evaluation = EVALUATION.read_text(encoding="utf-8")

        normalized_skill = " ".join(skill.split())
        self.assertIn("переиспользуй blocker fingerprint", normalized_skill)
        self.assertIn(
            "не повторяй проверку, facade, handoff или user request",
            normalized_skill,
        )
        for text in (run_goal, architecture):
            self.assertIn("browser/profile", text)
            self.assertIn("update_goal", text)
            self.assertIn("resume signal", text)
        self.assertIn("новой unit не создаёт", explainer)
        self.assertIn("двух следующих автоматических Goal\n  turns", evaluation)


if __name__ == "__main__":
    unittest.main()
