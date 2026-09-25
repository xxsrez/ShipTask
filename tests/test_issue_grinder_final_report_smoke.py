"""Regression tests for lifecycle oracle, not report-quality keyword checks."""
import importlib.util
import json
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts/issue_grinder_final_report_smoke.py"
SPEC = importlib.util.spec_from_file_location("final_report_smoke", MODULE_PATH)
SMOKE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SMOKE)


class FinalReportSmokeTests(unittest.TestCase):
    def test_last_actual_message_is_reviewed(self):
        events = [
            {"type": "item.completed", "item": {"type": "agent_message", "text": "draft"}},
            {"type": "item.completed", "item": {"type": "agent_message", "text":
                json.dumps({"report": "outgoing", "effect": "publish"})}},
        ]
        self.assertEqual(SMOKE.extract("\n".join(map(json.dumps, events)))["report"], "outgoing")

    def test_repeated_short_report_is_rejected(self):
        result = {"effect": "blocked", "report": "Всё ещё нужен пользователь",
                  "new_user_request": False}
        self.assertTrue(SMOKE.assess_effect("repeat-3", result))

    def test_audit_cannot_block_early(self):
        result = {"effect": "blocked", "report": "", "new_user_request": False}
        self.assertTrue(SMOKE.assess_effect("repeat-2", result))
        self.assertEqual(SMOKE.assess_effect("repeat-3", result), [])

    def test_checkpoint_cannot_claim_completion(self):
        result = {"effect": "complete", "report": "Candidate проверен частично",
                  "new_user_request": False}
        self.assertTrue(SMOKE.assess_effect("checkpoint", result))

    def test_mechanical_pass_does_not_judge_semantics(self):
        self.assertEqual(SMOKE.assess_effect("complete", {
            "effect": "complete", "report": "Непроверенный произвольный текст",
            "new_user_request": False}), [])


if __name__ == "__main__":
    unittest.main()
