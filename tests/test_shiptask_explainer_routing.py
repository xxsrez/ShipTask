from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "ship-tasks" / "SKILL.md"
PROTOCOL = ROOT / "ship-tasks" / "references" / "strategic-explainer.md"
DELIVERY = ROOT / "ship-tasks" / "references" / "delivery-report.md"
RUN_REPORT = ROOT / "ship-tasks" / "references" / "run-report.md"
REQUIREMENTS = ROOT / "docs" / "skills" / "ship-tasks" / "requirements.md"
ARCHITECTURE = ROOT / "docs" / "skills" / "ship-tasks" / "architecture.md"
COMPOSER = ROOT / "task-composer" / "SKILL.md"
COMPOSER_REQUIREMENTS = ROOT / "docs" / "skills" / "task-composer" / "requirements.md"
COMPOSER_ARCHITECTURE = ROOT / "docs" / "skills" / "task-composer" / "architecture.md"


def between(text: str, start: str, end: str) -> str:
    return text[text.index(start) : text.index(end)]


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
            "Operational unavailability или другой финальный failure facade переводит communication mode в native",
            " ".join(REQUIREMENTS.read_text().split()),
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

    def test_callers_use_only_semantic_facade(self) -> None:
        surfaces = {
            "ship runtime": between(
                SKILL.read_text(),
                "## 5. Обеспечь человеческое объяснение",
                "## 6. Продолжай автономно и финализируй",
            ),
            "ship protocol": PROTOCOL.read_text(),
            "ship requirements": between(
                REQUIREMENTS.read_text(),
                "### `ST-07`",
                "### `ST-08`",
            ),
            "ship architecture": between(
                ARCHITECTURE.read_text(),
                "## 6. Человеческое объяснение",
                "## 7. Реализация и проверка",
            ),
            "composer runtime": COMPOSER.read_text(),
            "composer requirements": between(
                COMPOSER_REQUIREMENTS.read_text(),
                "### `TC-09`",
                "### `TC-10`",
            ),
            "composer architecture": between(
                COMPOSER_ARCHITECTURE.read_text(),
                "## 5. Strategic Explainer",
                "## 6. Labels, hierarchy и relations",
            ),
        }
        semantic_markers = (
            "$strategic-explainer:strategic-explainer",
            "вопрос",
            "scope",
            "язык",
            "material constraints",
            "anchors",
        )
        implementation_markers = (
            "STRATEGIC_EXPLAINER_PROVIDER_V1",
            'fork_turns="none"',
            'model="gpt-5.6-luna"',
            'reasoning_effort="max"',
            "provider-entrypoint",
            "provider-contract.md",
            "built-in `default`",
        )
        method_markers = (
            "одну главную причинную мысль",
            "первый смысловой слой",
            "scenario coverage map",
            "audit-redaction pass",
        )
        for name, surface in surfaces.items():
            with self.subTest(surface=name):
                surface = " ".join(surface.split())
                for marker in semantic_markers:
                    self.assertIn(marker, surface)
                for marker in implementation_markers + method_markers:
                    self.assertNotIn(marker, surface)


if __name__ == "__main__":
    unittest.main()
