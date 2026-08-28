from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "strategic-explainer" / "SKILL.md"
ENTRYPOINT = ROOT / "strategic-explainer" / "references" / "provider-entrypoint.md"
CONTRACT = ROOT / "strategic-explainer" / "references" / "provider-contract.md"


class StrategicExplainerRuntimeTest(unittest.TestCase):
    def test_completion_gate_rejects_audit_dump_and_unchanged_repetition(self) -> None:
        text = " ".join(CONTRACT.read_text().split()).lower()
        for marker in (
            "сырой командный блок",
            "абсолютный путь",
            "список тестовых файлов",
            "неизменившиеся доказательства из предыдущего пользовательского сообщения",
            "не проходит completion gate",
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
            "Не исправляй собственный\nвызов и не запускай замену",
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
        for provider_recipe in (
            "одну главную причинную мысль",
            "первый смысловой слой",
            "scenario coverage map",
            "audit-redaction pass",
            "языковой очистки",
            "comprehension check",
        ):
            self.assertNotIn(provider_recipe, text)

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
        for path in (SKILL, ENTRYPOINT):
            with self.subTest(path=path.name):
                text = path.read_text()
                self.assertIn('fork_turns="none"', text)
                self.assertIn('model="gpt-5.6-luna"', text)
                self.assertIn('reasoning_effort="max"', text)


if __name__ == "__main__":
    unittest.main()
