from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "issue_grinder_mode_loading_smoke.py"
SPEC = importlib.util.spec_from_file_location(
    "issue_grinder_mode_loading_smoke", SCRIPT
)
assert SPEC is not None and SPEC.loader is not None
SMOKE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = SMOKE
SPEC.loader.exec_module(SMOKE)


def event(event_type: str, **values: object) -> str:
    return json.dumps({"type": event_type, **values}, ensure_ascii=False)


class IssueGrinderModeLoadingSmokeTest(unittest.TestCase):
    def test_selected_mode_is_the_only_observed_mode_file(self) -> None:
        root = "/cache/skills/issue-grinder"
        output = "\n".join(
            (
                event("thread.started", thread_id="thread-classic"),
                event(
                    "item.completed",
                    item={
                        "type": "command_execution",
                        "command": f"sed -n '1,240p' {root}/SKILL.md",
                    },
                ),
                event(
                    "item.completed",
                    item={
                        "type": "command_execution",
                        "command": f"sed -n '1,260p' {root}/references/execution-modes.md",
                    },
                ),
                event(
                    "item.completed",
                    item={
                        "type": "command_execution",
                        "command": f"sed -n '1,260p' {root}/references/modes/classic.md",
                    },
                ),
                event(
                    "item.completed",
                    item={
                        "type": "agent_message",
                        "text": json.dumps(
                            {
                                "canonical_mode": "classic",
                                "loaded_mode_file": "references/modes/classic.md",
                                "other_mode_files_loaded": [],
                            }
                        ),
                    },
                ),
                event("turn.completed", usage={"input_tokens": 100}),
            )
        )

        observation = SMOKE.observe_case("classic", output=output, exit_code=0)

        self.assertTrue(observation.passed)
        self.assertEqual(observation.loaded_mode_files, ("classic.md",))
        self.assertEqual(observation.defects, ())

    def test_reading_an_unselected_mode_fails_closed(self) -> None:
        root = "/cache/skills/issue-grinder"
        output = "\n".join(
            (
                event(
                    "item.completed",
                    item={
                        "type": "command_execution",
                        "command": f"sed -n '1,240p' {root}/SKILL.md",
                    },
                ),
                event(
                    "item.completed",
                    item={
                        "type": "command_execution",
                        "command": f"sed -n '1,260p' {root}/references/execution-modes.md",
                    },
                ),
                event(
                    "item.completed",
                    item={
                        "type": "command_execution",
                        "command": (
                            f"cat {root}/references/modes/classic.md "
                            f"{root}/references/modes/economical.md"
                        ),
                    },
                ),
            )
        )

        observation = SMOKE.observe_case("classic", output=output, exit_code=0)

        self.assertFalse(observation.passed)
        self.assertEqual(
            observation.loaded_mode_files,
            ("classic.md", "economical.md"),
        )
        self.assertIn("mode_files_loaded:classic.md,economical.md", observation.defects)

    def test_boolean_false_is_an_accepted_empty_self_report(self) -> None:
        root = "/cache/skills/issue-grinder"
        output = "\n".join(
            (
                event(
                    "item.completed",
                    item={
                        "type": "command_execution",
                        "command": (
                            f"cat {root}/SKILL.md "
                            f"{root}/references/execution-modes.md "
                            f"{root}/references/modes/solo.md"
                        ),
                    },
                ),
                event(
                    "item.completed",
                    item={
                        "type": "agent_message",
                        "text": json.dumps(
                            {
                                "canonical_mode": "solo",
                                "loaded_mode_file": "references/modes/solo.md",
                                "other_mode_files_loaded": False,
                            }
                        ),
                    },
                ),
            )
        )

        observation = SMOKE.observe_case("solo", output=output, exit_code=0)

        self.assertTrue(observation.passed)

    def test_broad_mode_directory_access_fails_closed(self) -> None:
        root = "/cache/skills/issue-grinder"
        output = event(
            "item.completed",
            item={
                "type": "command_execution",
                "command": f"find {root}/references/modes -type f -maxdepth 1",
            },
        )

        observation = SMOKE.observe_case("solo", output=output, exit_code=0)

        self.assertFalse(observation.passed)
        self.assertIn("broad_mode_directory_access", observation.defects)

    def test_broad_mode_directory_at_command_end_fails_closed(self) -> None:
        output = event(
            "item.completed",
            item={
                "type": "command_execution",
                "command": "ls references/modes",
            },
        )

        observation = SMOKE.observe_case("solo", output=output, exit_code=0)

        self.assertIn("broad_mode_directory_access", observation.defects)

    def test_prompt_names_one_contract_and_forbids_catalog_listing(self) -> None:
        prompt = SMOKE.build_prompt("economical")

        self.assertIn("references/modes/economical.md", prompt)
        self.assertIn("остальные два mode-файла", prompt)
        self.assertIn("не перечисляй каталог", prompt)
        for filename in ("solo.md", "classic.md"):
            self.assertNotIn(filename, prompt)


if __name__ == "__main__":
    unittest.main()
