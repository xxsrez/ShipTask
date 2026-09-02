from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scope-reviewer" / "scripts" / "lens_routing_guard.py"
SPEC = importlib.util.spec_from_file_location("scope_reviewer_lens_guard", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)
validate_route = MODULE.validate_route


class ScopeReviewerLensRoutingGuardTest(unittest.TestCase):
    def valid(self, **overrides):
        values = {
            "optic": "requirements-integrity",
            "snapshot_id": "project:p1@versions:t1=3,t2=8",
            "agent_type": "default",
            "model": "gpt-5.6-luna",
            "effort": "max",
            "fork_turns": "none",
        }
        values.update(overrides)
        return validate_route(**values)

    def test_exact_fresh_luna_max_route_is_admitted(self) -> None:
        receipt = self.valid(
            actual_model="gpt-5.6-luna",
            actual_effort="max",
        )
        self.assertTrue(receipt.allowed, receipt.defects)
        self.assertEqual(receipt.telemetry_status, "observed")
        self.assertEqual(receipt.snapshot_id, "project:p1@versions:t1=3,t2=8")

    def test_every_fixed_route_dimension_fails_closed(self) -> None:
        cases = {
            "agent_type": ("worker", "default_agent_required"),
            "model": ("gpt-5.6-sol", "luna_model_required"),
            "effort": ("xhigh", "luna_max_effort_required"),
            "fork_turns": ("all", "fresh_fork_required"),
            "optic": ("  ", "blank_optic"),
            "snapshot_id": ("", "blank_snapshot_id"),
        }
        for field, (value, defect) in cases.items():
            with self.subTest(field=field):
                receipt = self.valid(**{field: value})
                self.assertFalse(receipt.allowed)
                self.assertIn(defect, receipt.defects)

    def test_observed_profile_mismatch_is_rejected(self) -> None:
        receipt = self.valid(
            actual_model="gpt-5.4",
            actual_effort="high",
        )
        self.assertFalse(receipt.allowed)
        self.assertIn("actual_luna_model_mismatch", receipt.defects)
        self.assertIn("actual_luna_effort_mismatch", receipt.defects)

    def test_cli_returns_nonzero_for_invalid_route(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--optic",
                "release-risk",
                "--snapshot-id",
                "release:r1@v7",
                "--model",
                "gpt-5.6-sol",
                "--effort",
                "max",
                "--fork-turns",
                "none",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 2)
        self.assertIn('"allowed": false', completed.stdout)


if __name__ == "__main__":
    unittest.main()
