"""Ensure the decision oracle accepts investigation without accepting new gates."""
import importlib.util
from pathlib import Path
import unittest

SPEC = importlib.util.spec_from_file_location(
    'blocker_smoke', Path(__file__).resolve().parents[1] / 'scripts/issue_grinder_blocker_smoke.py')
smoke = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(smoke)


def payload():
    return {'decisions': [dict(id=key, next_provider=pair[0], action=pair[1],
                               set_blocked=False, ask_user=key == 'confirmed-stop')
                          for key, pair in smoke.EXPECTED.items()]}


class DecisionOracleTest(unittest.TestCase):
    def test_read_only_preparation_is_progress(self):
        data = payload()
        row = next(r for r in data['decisions'] if r['id'] == 'premature-permission')
        for provider, action in [('none', 'continue'), ('native', 'analyze')]:
            row.update(next_provider=provider, action=action)
            self.assertEqual(smoke.assess(data), [])

    def test_new_approval_or_block_cannot_hide_behind_valid_action(self):
        for key in ['premature-permission', 'uat-cycle', 'uat-recovery', 'consent-resume', 'repeat']:
            for field in ['ask_user', 'set_blocked']:
                with self.subTest(key=key, field=field):
                    data = payload()
                    next(r for r in data['decisions'] if r['id'] == key)[field] = True
                    self.assertTrue(smoke.assess(data))

    def test_required_followup_cannot_be_replaced_by_native_analysis(self):
        data = payload()
        next(r for r in data['decisions'] if r['id'] == 'advice-gap').update(
            next_provider='native', action='analyze')
        self.assertTrue(smoke.assess(data))
