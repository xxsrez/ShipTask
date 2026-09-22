from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "issue_grinder_solo_topology_smoke.py"
SPEC = importlib.util.spec_from_file_location(
    "issue_grinder_solo_topology_smoke", SCRIPT
)
assert SPEC is not None and SPEC.loader is not None
SMOKE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = SMOKE
SPEC.loader.exec_module(SMOKE)


def event(event_type: str, **values: object) -> str:
    return json.dumps({"type": event_type, **values}, ensure_ascii=False)


def successful_output() -> str:
    root = "/cache/skills/issue-grinder"
    return "\n".join(
        (
            event("thread.started", thread_id="solo-thread"),
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
                            "result_file": "result.json",
                            "verification": "passed",
                        }
                    ),
                },
            ),
            event("turn.completed", usage={"input_tokens": 100}),
        )
    )


class IssueGrinderSoloTopologySmokeTest(unittest.TestCase):
    def test_clean_root_only_execution_passes(self) -> None:
        observation = SMOKE.observe_case(
            output=successful_output(),
            trace_events=[{"type": "turn_context", "payload": {}}],
            trace_path=Path("/tmp/solo-thread.jsonl"),
            result_payload=dict(SMOKE.EXPECTED_RESULT),
            exit_code=0,
        )

        self.assertTrue(observation.passed)
        self.assertEqual(observation.loaded_mode_files, ("solo.md",))
        self.assertEqual(observation.delegation_events, ())
        self.assertEqual(observation.defects, ())

    def test_spawn_agent_in_root_trace_fails(self) -> None:
        observation = SMOKE.observe_case(
            output=successful_output(),
            trace_events=[
                {
                    "type": "response_item",
                    "payload": {
                        "type": "function_call",
                        "namespace": "collaboration",
                        "name": "spawn_agent",
                    },
                }
            ],
            trace_path=Path("/tmp/solo-thread.jsonl"),
            result_payload=dict(SMOKE.EXPECTED_RESULT),
            exit_code=0,
        )

        self.assertFalse(observation.passed)
        self.assertEqual(observation.delegation_events, ("spawn_agent",))
        self.assertIn("execution_delegation:spawn_agent", observation.defects)

    def test_app_thread_dispatch_in_root_trace_fails(self) -> None:
        for tool in ("create_thread", "fork_thread"):
            with self.subTest(tool=tool):
                observation = SMOKE.observe_case(
                    output=successful_output(),
                    trace_events=[
                        {
                            "type": "event_msg",
                            "payload": {
                                "type": "item_completed",
                                "item": {
                                    "type": "McpToolCall",
                                    "server": "codex_app",
                                    "tool": tool,
                                },
                            },
                        }
                    ],
                    trace_path=Path("/tmp/solo-thread.jsonl"),
                    result_payload=dict(SMOKE.EXPECTED_RESULT),
                    exit_code=0,
                )

                self.assertFalse(observation.passed)
                self.assertIn(tool, observation.delegation_events)

    def test_service_provider_is_allowed_by_mode_policy(self) -> None:
        mode_harness_path = ROOT / "scripts" / "issue_grinder_mode_harness.py"
        spec = importlib.util.spec_from_file_location(
            "issue_grinder_mode_harness_for_solo_smoke",
            mode_harness_path,
        )
        assert spec is not None and spec.loader is not None
        harness = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = harness
        spec.loader.exec_module(harness)

        current = harness.Profile("gpt-6-sol", "xhigh")
        record = harness.resolve_mode(
            current,
            explicit_mode=harness.ExecutionMode.SOLO,
        )
        policy = harness.mode_dispatch_policy(
            record,
            current_main_profile=current,
        )

        self.assertFalse(policy.issue_grinder_execution_subagents_allowed)
        self.assertTrue(policy.service_provider_agents_allowed)

    def test_wrong_result_or_other_mode_file_fails(self) -> None:
        output = successful_output().replace(
            "references/modes/solo.md",
            "references/modes/classic.md",
        )
        observation = SMOKE.observe_case(
            output=output,
            trace_events=[],
            trace_path=Path("/tmp/solo-thread.jsonl"),
            result_payload={"total": 21},
            exit_code=0,
        )

        self.assertFalse(observation.passed)
        self.assertIn("mode_files_loaded:classic.md", observation.defects)
        self.assertIn("wrong_result_payload", observation.defects)

    def test_prompt_does_not_tell_model_to_avoid_execution_subagents(self) -> None:
        prompt = SMOKE.build_prompt()

        self.assertIn("режим «Соло»", prompt)
        self.assertIn("анализ", prompt)
        self.assertIn("self-review", prompt)
        self.assertNotIn("spawn_agent", prompt)
        self.assertNotIn("не создавай subagents", prompt)


if __name__ == "__main__":
    unittest.main()
