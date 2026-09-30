"""Modes work without any observable or selectable main-session profile."""
from dataclasses import replace
from pathlib import Path
import os
from unittest.mock import patch
import unittest

from scripts.issue_grinder_mode_harness import (
    ExecutionMode, ModeOrigin, LUNA_MAX, SOL_XHIGH,
    resolve_mode, mode_dispatch_policy, decide_mode_switch,
)

ROOT = Path(__file__).resolve().parents[1]


class FourModesTest(unittest.TestCase):
    def test_launch_button_defaults_only_when_no_explicit_choice(self):
        prompt = (ROOT / "issue-grinder/agents/openai.yaml").read_text()
        self.assertIn("если я не указал другой режим явно, используй Соло", prompt)

    def test_default_and_all_explicit_modes_need_no_host_profile(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(
            Path, "open", side_effect=AssertionError("must not read host state")
        ):
            default = resolve_mode()
            self.assertEqual(default.canonical_mode, ExecutionMode.SOLO)
            self.assertEqual(default.mode_origin, ModeOrigin.AUTOMATIC)
            for mode in ExecutionMode:
                with self.subTest(mode=mode):
                    record = resolve_mode(explicit_mode=mode)
                    self.assertEqual(record.canonical_mode, mode)
                    self.assertEqual(record.mode_origin, ModeOrigin.EXPLICIT)
                    self.assertEqual(
                        mode_dispatch_policy(record).issue_grinder_execution_subagents_allowed,
                        mode is not ExecutionMode.SOLO,
                    )

    def test_saved_mode_wins_over_default_for_every_supported_mode(self):
        for mode in ExecutionMode:
            record = resolve_mode(explicit_mode=mode)
            self.assertIs(
                resolve_mode(saved_record=record, continuity_proven=True), record
            )
            self.assertEqual(
                resolve_mode(saved_record=record).canonical_mode, ExecutionMode.SOLO
            )

    def test_explicit_switch_needs_only_safe_work_checkpoint(self):
        for source in ExecutionMode:
            record = resolve_mode(explicit_mode=source)
            for target in ExecutionMode:
                if source is target:
                    continue
                waiting = decide_mode_switch(
                    record, target, explicit_request=True, active_writer_count=1
                )
                self.assertFalse(waiting.may_apply_next_wave)
                switched = decide_mode_switch(record, target, explicit_request=True)
                self.assertTrue(switched.may_apply_next_wave)
                self.assertEqual(switched.mode_record.canonical_mode, target)

    def test_retired_modes_are_not_silently_replaced(self):
        for name in ("swarm", "manager", "roy", "roi", "typo"):
            with self.assertRaises(ValueError):
                resolve_mode(explicit_mode=name)
            old = replace(resolve_mode(), canonical_mode=name)
            with self.assertRaises(ValueError):
                resolve_mode(saved_record=old, continuity_proven=True)

    def test_child_profiles_survive_without_main_profile(self):
        for mode in (ExecutionMode.CLASSIC, ExecutionMode.BALANCE, ExecutionMode.ECONOMICAL):
            profiles = resolve_mode(explicit_mode=mode).role_profiles
            self.assertEqual(profiles.worker, LUNA_MAX)
            self.assertEqual(profiles.reviewer, SOL_XHIGH if mode is ExecutionMode.BALANCE else LUNA_MAX)
        self.assertIsNone(resolve_mode().role_profiles)

    def test_removed_profile_probe_cannot_be_loaded_by_runtime(self):
        runtime = ROOT / "issue-grinder"
        self.assertFalse((runtime / "scripts/main_profile.py").exists())
        for path in runtime.rglob("*"):
            if path.is_file() and path.suffix in (".md", ".py", ".yaml"):
                text = path.read_text()
                for forbidden in (
                    "main_profile.py", "CODEX_THREAD_ID", "latest_turn_context",
                    "initial_main_model:", "initial_main_effort:",
                    "current-root admission", "luna-coordinator-v1",
                ):
                    with self.subTest(path=path, forbidden=forbidden):
                        self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
