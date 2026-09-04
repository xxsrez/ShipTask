from dataclasses import replace
import unittest

from scripts.issue_grinder_mode_harness import (
    ExecutionMode, Profile, resolve_mode, mode_dispatch_policy, decide_mode_switch,
)


class ThreeModesTest(unittest.TestCase):
    def test_only_three_modes_exist(self):
        self.assertEqual({m.value for m in ExecutionMode}, {"solo", "classic", "economical"})

    def test_default_matrix(self):
        for model in ("gpt-5.6-luna", "gpt-5.6-sol", "gpt-6-astra", "unknown-model"):
            for effort in ("low", "high", "max", "xhigh"):
                for count in (0, 1, 2, 20):
                    with self.subTest(model=model, effort=effort, count=count):
                        record = resolve_mode(Profile(model, effort), scope_task_count=count)
                        expected = "classic" if model != "gpt-5.6-luna" and count > 1 else "solo"
                        self.assertEqual(record.canonical_mode.value, expected)
                        self.assertEqual(record.initial_scope_task_count, count)

    def test_explicit_choice_overrides_default(self):
        for model in ("gpt-5.6-luna", "gpt-5.6-sol"):
            for count in (1, 4):
                for mode in ExecutionMode:
                    self.assertEqual(
                        resolve_mode(Profile(model, "high"), scope_task_count=count,
                                     explicit_mode=mode).canonical_mode, mode)

    def test_continuation_never_recalculates_default(self):
        for model, count in (("gpt-5.6-sol", 4), ("gpt-5.6-luna", 4),
                             ("gpt-5.6-sol", 1)):
            original = resolve_mode(Profile(model, "high"), scope_task_count=count)
            for next_model, next_count in (("gpt-5.6-luna", 1), ("gpt-5.6-sol", 9)):
                restored = resolve_mode(
                    Profile(next_model, "max"), scope_task_count=next_count,
                    saved_record=original, continuity_proven=True)
                self.assertIs(restored, original)

    def test_retired_and_unknown_records_and_requests_fail_closed(self):
        profile = Profile("gpt-5.6-sol", "high")
        for mode in ("balance", "swarm", "manager", "roy", "roi", "Баланс", "Рой", "typo"):
            with self.subTest(mode=mode):
                with self.assertRaises(ValueError):
                    resolve_mode(profile, explicit_mode=mode)
                with self.assertRaises(ValueError):
                    decide_mode_switch(resolve_mode(profile), mode, explicit_request=True)
                with self.assertRaises(ValueError):
                    resolve_mode(profile, saved_record=replace(
                        resolve_mode(profile), canonical_mode=mode), continuity_proven=True)

    def test_explicit_switch_from_retired_record_preserves_checkpoint_barrier(self):
        original = replace(resolve_mode(Profile("gpt-5.6-sol", "high")),
                           canonical_mode="balance")
        waiting = decide_mode_switch(original, ExecutionMode.SOLO,
                                     explicit_request=True, active_writer_count=1)
        self.assertFalse(waiting.may_apply_next_wave)
        self.assertIs(waiting.mode_record, original)
        ready = decide_mode_switch(original, ExecutionMode.SOLO, explicit_request=True)
        self.assertTrue(ready.may_apply_next_wave)
        self.assertEqual(ready.mode_record.canonical_mode, ExecutionMode.SOLO)

    def test_unresolved_task_count_is_not_guessed(self):
        for count in (None, -1, True, "2"):
            with self.assertRaises(ValueError):
                resolve_mode(Profile("gpt-5.6-sol", "high"), scope_task_count=count)

    def test_solo_has_no_execution_children(self):
        profile = Profile("gpt-5.6-luna", "high")
        policy = mode_dispatch_policy(resolve_mode(profile, scope_task_count=10),
                                      current_main_profile=profile)
        self.assertFalse(policy.issue_grinder_execution_subagents_allowed)
        self.assertEqual(policy.max_active_execution_lanes, 1)
        self.assertEqual(policy.execution_profile, profile)


if __name__ == "__main__":
    unittest.main()
