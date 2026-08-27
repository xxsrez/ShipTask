from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "ship-tasks" / "SKILL.md"
PROTOCOL = ROOT / "ship-tasks" / "references" / "strategic-explainer.md"
DELIVERY = ROOT / "ship-tasks" / "references" / "delivery-report.md"
RUN_REPORT = ROOT / "ship-tasks" / "references" / "run-report.md"
REQUIREMENTS = ROOT / "docs" / "skills" / "ship-tasks" / "requirements.md"
ARCHITECTURE = ROOT / "docs" / "skills" / "ship-tasks" / "architecture.md"


class ShipTaskExplainerRoutingTest(unittest.TestCase):
    def test_two_install_combinations_are_explicit(self) -> None:
        text = PROTOCOL.read_text()
        for row in (
            "| доступен и разрешён | ordinary |",
            "| отсутствует или отключён | native |",
        ):
            self.assertIn(row, text)

    def test_priority_is_ordinary_then_native(self) -> None:
        text = PROTOCOL.read_text()
        routing = text[text.index("## Матрица выбора") : text.index("## Ordinary path")]
        self.assertLess(
            routing.index("ordinary `$strategic-explainer:strategic-explainer`"),
            routing.index("native ShipTask writing"),
        )

    def test_provider_failure_goes_native(self) -> None:
        text = PROTOCOL.read_text()
        self.assertIn("Ошибка уже выбранного ordinary переводит\nrun в native mode", text)
        self.assertIn(
            "Invalid invocation получает один\nавтоматически исправленный новый clean subagent",
            REQUIREMENTS.read_text(),
        )

    def test_native_mode_does_not_block_comment_or_status(self) -> None:
        combined = "\n".join(
            path.read_text()
            for path in (SKILL, PROTOCOL, DELIVERY, RUN_REPORT, REQUIREMENTS, ARCHITECTURE)
        )
        for marker in (
            "не блокирует comment",
            "Обязательный comment всё равно публикуется и перечитывается",
            "не мешает связанному существенному transition",
            "без служебного сообщения об отсутствии\nprovider",
        ):
            self.assertIn(marker, combined)
        self.assertNotIn("не публикуй comment", combined)
        self.assertNotIn("обязательный Strategic Explainer недоступен", combined)

    def test_topology_and_opt_out_route_to_native(self) -> None:
        text = PROTOCOL.read_text()
        self.assertIn("Общий запрет создавать subagents также исключает ordinary", text)
        self.assertIn("выбирает native", text)

    def test_ordinary_invocation_contains_terminal_role_lock(self) -> None:
        text = PROTOCOL.read_text()
        ordinary = text[text.index("## Ordinary path") : text.index("## Native path")]
        self.assertIn("STRATEGIC_EXPLAINER_PROVIDER_V1", ordinary)
        self.assertIn("fork_turns=\"none\"", ordinary)
        self.assertIn("одну короткую user-facing formulation task", ordinary)
        self.assertIn("Не\nчитай ordinary provider-only entrypoint", ordinary)


if __name__ == "__main__":
    unittest.main()
