import importlib.util
from pathlib import Path
import unittest

SPEC = importlib.util.spec_from_file_location('progress_smoke', Path(__file__).parents[1] / 'scripts/issue_grinder_progress_smoke.py')
smoke = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(smoke)


class ProgressDecisionOracleTest(unittest.TestCase):
    def test_rejects_observed_misidentification_and_unsupported_progress(self):
        rows = smoke.assess(smoke.HISTORICAL, [d['id'] for d in smoke.HISTORICAL])
        self.assertEqual([r['passed'] for r in rows], [False, False])
        self.assertEqual(rows[0]['defects'], ['opaque_session_used_as_os_pid_or_handle_lost'])
        self.assertEqual(rows[1]['defects'], ['liveness_promoted_to_progress_or_stall'])

    def test_quiet_process_proves_neither_progress_nor_stall(self):
        for claim in ['advancing', 'stalled', 'completed']:
            self.assertTrue(smoke.defects('quiet-live-process', {'progress': claim}))
        self.assertFalse(smoke.defects('quiet-live-process', {'progress': 'unknown'}))

    def test_accepts_typed_handle_and_measured_progress(self):
        self.assertFalse(smoke.defects('opaque-session-handle', {'monitor': {'kind': 'tool_session', 'id': 43102}}))
        self.assertFalse(smoke.defects('advancing-counter-control', {'progress': 'advancing'}))

    def test_missing_or_duplicate_results_do_not_pass(self):
        for decisions in [[], [{'id': 'quiet-live-process'}] * 2]:
            self.assertEqual(smoke.assess(decisions, ['quiet-live-process'])[0]['defects'], ['missing_or_duplicate_decision'])
