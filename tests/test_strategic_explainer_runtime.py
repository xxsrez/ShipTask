from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "strategic-explainer" / "SKILL.md"
ENTRYPOINT = ROOT / "strategic-explainer" / "references" / "provider-entrypoint.md"
CONTRACT = ROOT / "strategic-explainer" / "references" / "provider-contract.md"
REQUIREMENTS = ROOT / "docs" / "skills" / "strategic-explainer" / "requirements.md"
ARCHITECTURE = ROOT / "docs" / "skills" / "strategic-explainer" / "architecture.md"
EVALUATION = ROOT / "docs" / "reference" / "strategic-explainer-evaluation.md"
HARNESS = ROOT / "tests" / "strategic-explainer" / "README.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split()).lower()


def section(path: Path, start: str, end: str) -> str:
    text = path.read_text(encoding="utf-8")
    return text[text.index(start) : text.index(end)]


class StrategicExplainerRuntimeTest(unittest.TestCase):
    def test_completion_gate_rejects_audit_dump_and_unchanged_repetition(self) -> None:
        text = normalized(CONTRACT)
        for marker in (
            "сырой командный блок",
            "абсолютный путь",
            "список тестовых файлов",
            "неизменившиеся доказательства",
            "предыдущим пользовательским сообщением",
            "не проходит completion gate",
        ):
            self.assertIn(marker, text)

    def test_incomplete_result_cannot_hide_causality_in_source_basis(self) -> None:
        text = normalized(CONTRACT)
        for marker in (
            "какой результат или условие не достигнуты",
            "какова основная причина",
            "какое минимальное действие нужно",
            "наблюдаемому признаку",
            "полный source basis не исправляет пропуск",
            "доступное безопасное исправление",
            "не заявляй, что продолжение исчерпано",
        ):
            self.assertIn(marker, text)

    def test_incomplete_result_keeps_only_useful_navigation_names(self) -> None:
        text = normalized(CONTRACT)
        for marker in (
            "точное имя объекта или критерия",
            "оставь имя в публикации как навигацию",
            "существенно отличающейся группы",
            "различающиеся результаты, причины, зависимости, действия",
        ):
            self.assertIn(marker, text)

    def test_terminal_role_is_resolved_before_facade_protocol(self) -> None:
        text = SKILL.read_text()
        self.assertLess(
            text.index("## Сначала разреши роль"),
            text.index("## Публичный semantic contract"),
        )
        provider_branch = text[
            text.index("## Сначала разреши роль") : text.index("## Публичный semantic contract")
        ]
        self.assertIn("STRATEGIC_EXPLAINER_PROVIDER_V1", provider_branch)
        self.assertIn("это терминальный provider", provider_branch)
        self.assertIn("Не исполняй\n  facade protocol", provider_branch)
        self.assertIn("references/provider-entrypoint.md", provider_branch)
        self.assertIn("никогда не переклассифицирует себя в caller", provider_branch)

    def test_provider_entrypoint_rejects_off_role_work(self) -> None:
        text = ENTRYPOINT.read_text()
        for marker in (
            "provider-only admission contract",
            "Ты не caller, не router, не\ncoordinator и не evaluator",
            "Никогда не вызывай Strategic Explainer",
            "не создавай и не продолжай agents",
            "Planning, decomposition, implementation, mutation",
            "lifecycle/status/authority",
            "STRATEGIC_EXPLAINER_INVOCATION_ERROR",
            "точный defect",
            "не исправляй собственный вызов",
            "не запускай замену",
        ):
            self.assertIn(marker, text)

    def test_provider_runtime_has_no_agent_orchestration(self) -> None:
        contract = CONTRACT.read_text()
        self.assertNotIn("spawn_agent", contract)
        self.assertNotIn("fork_turns", contract)
        self.assertIn("не вызывай Strategic Explainer", contract)
        self.assertIn("не\n  создавай и не продолжай agents", contract)
        self.assertIn("comprehension check без другого агента", contract)
        self.assertIn("внешним model-forward\nevaluation harness", contract)

    def test_facade_owns_invocation_but_not_provider_expertise(self) -> None:
        text = SKILL.read_text()
        public = text[
            text.index("## Публичный semantic contract") :
            text.index("## Внутреннее исполнение facade")
        ]
        internal = text[text.index("## Внутреннее исполнение facade") :]
        self.assertIn("одна реальная user-facing formulation", public)
        self.assertIn("resolvable read-only source anchors", public)
        self.assertIn("Не требуй от внешнего workflow", public)
        self.assertIn("нового built-in `default` subagent", internal)
        self.assertIn('model="gpt-5.6-luna"', internal)
        self.assertIn('reasoning_effort="max"', internal)
        self.assertIn("Не передавай inherited turns", internal)
        self.assertIn("facade исправляет", internal)
        self.assertIn("обе части provider result", internal)
        self.assertIn("не сокращай и не реконструируй basis", internal)
        self.assertIn("source basis — вторая opaque-часть provider result", public.lower())
        self.assertIn("не строят собственный basis", public)
        for provider_recipe in (
            "одну главную причинную мысль",
            "первый смысловой слой",
            "scenario coverage map",
            "audit-redaction pass",
            "языковой очистки",
            "comprehension check",
        ):
            self.assertNotIn(provider_recipe, text)

    def test_facade_never_substitutes_user_visible_task_for_subagent(self) -> None:
        runtime = SKILL.read_text()
        internal = runtime[runtime.index("## Внутреннее исполнение facade") :]
        for marker in (
            "top-level tool call\n   `collaboration.spawn_agent`",
            "`ALL_TOOLS`",
            "`functions.exec`",
            "Никогда не подменяй его\n   `create_thread`",
            "новой пользовательской session",
            "верни provider unavailability без app-level замены",
            "Не пытайся\n   связаться с parent через app tools",
        ):
            self.assertIn(marker, internal)

        architecture = " ".join(ARCHITECTURE.read_text().split())
        evaluation = " ".join(EVALUATION.read_text().split())
        harness = " ".join(HARNESS.read_text().split())
        for text in (architecture, evaluation, harness):
            self.assertIn("parent link", text)
            self.assertIn("create_thread", text)
            self.assertIn("operational unavailability", text)
        self.assertIn("`Built-in subagent`", architecture)
        self.assertIn("child/subagent", architecture)
        self.assertIn("`collaboration.spawn_agent`", architecture)
        self.assertIn("не иметь права создавать grandchild", architecture)
        for text in (evaluation, harness):
            self.assertIn("built-in child/subagent", text)
            self.assertIn("facts/evidence/anchors", text)

    def test_metadata_exposes_semantics_not_invocation_recipe(self) -> None:
        metadata = (ROOT / "strategic-explainer" / "agents" / "openai.yaml").read_text()
        self.assertIn("понятный пользовательский текст", metadata)
        self.assertIn("source basis", metadata)
        for marker in (
            "STRATEGIC_EXPLAINER_PROVIDER_V1",
            "fork_turns",
            "gpt-5.6-luna",
            "reasoning_effort",
        ):
            self.assertNotIn(marker, metadata)

    def test_clean_call_recipe_uses_luna_max(self) -> None:
        text = SKILL.read_text()
        self.assertIn('fork_turns="none"', text)
        self.assertIn('model="gpt-5.6-luna"', text)
        self.assertIn('reasoning_effort="max"', text)

        entrypoint = ENTRYPOINT.read_text()
        self.assertNotIn('fork_turns="none"', entrypoint)
        self.assertNotIn('model="gpt-5.6-luna"', entrypoint)
        self.assertNotIn('reasoning_effort="max"', entrypoint)
        self.assertIn("Facade\nсам владеет clean-call recipe", entrypoint)

    def test_provider_contract_enforces_generic_human_output(self) -> None:
        text = normalized(CONTRACT)
        for marker in (
            "дай прямой ответ, а не заполняй отчётный шаблон",
            "структура и длина следуют содержанию",
            "не превращай процесс подготовки объяснения в предмет публикации",
            "каждую material limitation, exception или uncertainty ставь рядом",
            "сохрани в basis доступные точные значения и их смысл либо дай точный разрешимый anchor",
            "не заменяй их общей фразой о том, что технические детали исключены",
        ):
            self.assertIn(marker, text)

    def test_explanatory_bridge_is_outcome_driven_and_not_evidence(self) -> None:
        requirements = normalized(REQUIREMENTS)
        architecture = normalized(ARCHITECTURE)
        contract = normalized(CONTRACT)
        evaluation = normalized(EVALUATION)

        for text in (requirements, architecture, contract, evaluation):
            self.assertIn("незнакомого механизма", text)
            self.assertIn("величины", text)
            self.assertIn("визуального", text)
            self.assertIn("причин", text)
            self.assertIn("масштаб", text)
            self.assertIn("границ", text)

        self.assertIn("не превращай эти приёмы в порядок или шаблон", contract)
        self.assertIn("простой или точный экспертный ответ не расширяй", contract)
        self.assertIn("недоступный график", contract)
        self.assertIn("не восстанавливай догадкой", contract)
        self.assertIn("не являются его доказательством", requirements)

    def test_editing_reuses_the_common_publication_filter(self) -> None:
        text = normalized(CONTRACT)
        editing = " ".join(
            section(CONTRACT, "## Редакторская реконструкция", "## Completion gate").split()
        ).lower()
        for marker in (
            "сохранение исходника относится ко всему двухчастному result contract",
            "audit-only identifiers, внутренний процесс подготовки",
            "такой перенос не является потерей содержания",
            "само присутствие детали в target text не доказывает её пользовательскую релевантность",
            "не маскируй утечку переводом",
            "обезличенный внутренний процесс остаётся внутренним процессом",
        ):
            self.assertIn(marker, text)
        self.assertIn("заново примени весь фильтр публикации", editing)
        self.assertIn(
            "обезличенное сообщение о создании отчёта или ответа тоже удаляется",
            editing,
        )
        self.assertIn("для каждого точного факта", editing)
        self.assertIn("само значение либо разрешимый anchor", editing)
        self.assertNotIn("run/deployment/request ids", editing)


if __name__ == "__main__":
    unittest.main()
