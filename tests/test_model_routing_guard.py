from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "issue-grinder" / "scripts" / "model_routing_guard.py"
SPEC = importlib.util.spec_from_file_location("model_routing_guard", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)
validate_route = MODULE.validate_route


class ModelRoutingGuardTest(unittest.TestCase):
    def test_retired_routes_are_rejected_even_with_profile_override(self) -> None:
        for mode in ("balance", "swarm", "manager", "roy", "roi"):
            for override in (False, True):
                receipt = validate_route(
                    packet_id="retired-route", mode=mode, semantic_role="implementation",
                    agent_type="worker", model="gpt-5.6-luna", effort="max",
                    fork_turns="none", user_profile_override=override)
                self.assertFalse(receipt.allowed)
                self.assertIn("unknown_mode", receipt.defects)

    def luna_route(self, mode: str, role: str = "implementation"):
        effort = "max"
        return validate_route(
            packet_id=f"packet-{mode}-{role}",
            mode=mode,
            semantic_role=role,
            agent_type="worker",
            model="gpt-5.6-luna",
            effort=effort,
            fork_turns="none",
        )

    def test_luna_modes_admit_their_explicit_worker_profiles(self) -> None:
        for mode in ("economical",):
            with self.subTest(mode=mode):
                receipt = self.luna_route(mode)
                self.assertTrue(receipt.allowed, receipt.defects)
                self.assertTrue(receipt.luna_required)
                self.assertEqual(receipt.telemetry_status, "telemetry_pending")

    def test_substantive_inherited_sol_is_rejected_in_economical_mode(self) -> None:
        for mode in ("economical",):
            with self.subTest(mode=mode):
                receipt = validate_route(
                    packet_id=f"packet-{mode}-research",
                    mode=mode,
                    semantic_role="research",
                    agent_type="explorer",
                    model="gpt-5.6-sol",
                    effort="xhigh",
                    fork_turns="all",
                )
                self.assertFalse(receipt.allowed)
                self.assertIn("luna_model_required", receipt.defects)
                expected = "luna_max_effort_required"
                self.assertIn(expected, receipt.defects)
                self.assertIn("unbounded_or_missing_fork_turns", receipt.defects)

    def test_agent_type_label_does_not_override_explicit_profile(self) -> None:
        for agent_type in ("default", "worker", "explorer", "custom-quality"):
            with self.subTest(agent_type=agent_type):
                receipt = validate_route(
                    packet_id=f"packet-economical-{agent_type}",
                    mode="economical",
                    semantic_role="quality_check",
                    agent_type=agent_type,
                    model="gpt-5.6-luna",
                    effort="max",
                    fork_turns="none",
                    actual_model="gpt-5.6-luna",
                    actual_effort="max",
                )
                self.assertTrue(receipt.allowed, receipt.defects)
                self.assertEqual(receipt.agent_type, agent_type)

        guard = SCRIPT.read_text(encoding="utf-8")
        self.assertNotIn("FORCED_PROFILE_AGENT_TYPES", guard)
        self.assertNotIn("platform_agent_type_bypasses_mode_profile", guard)

    def test_economical_does_not_admit_a_sol_execution_child(self) -> None:
        receipt = validate_route(
            packet_id="packet-economical-material-judgment",
            mode="economical",
            semantic_role="material_judgment",
            agent_type="default",
            model="gpt-5.6-sol",
            effort="xhigh",
            fork_turns="none",
            actual_model="gpt-5.6-sol",
            actual_effort="xhigh",
        )
        self.assertFalse(receipt.allowed)
        self.assertTrue(receipt.luna_required)
        self.assertIn("luna_model_required", receipt.defects)
        self.assertEqual(receipt.telemetry_status, "observed")

    def test_economical_requires_luna_even_for_review(self) -> None:
        receipt = validate_route(
            packet_id="packet-economical-final-review",
            mode="economical",
            semantic_role="final_review",
            agent_type="default",
            model="gpt-5.6-sol",
            effort="xhigh",
            fork_turns="none",
        )
        self.assertFalse(receipt.allowed)
        self.assertTrue(receipt.luna_required)

    def test_observed_profile_mismatch_fails_closed(self) -> None:
        receipt = validate_route(
            packet_id="packet-economical-test-author",
            mode="economical",
            semantic_role="test_author",
            agent_type="default",
            model="gpt-5.6-luna",
            effort="high",
            fork_turns="1",
            actual_model="gpt-5.4",
            actual_effort="high",
        )
        self.assertFalse(receipt.allowed)
        self.assertIn("actual_luna_model_mismatch", receipt.defects)
        self.assertIn("actual_luna_effort_mismatch", receipt.defects)

    def test_explicit_user_profile_override_is_preserved_and_observed(self) -> None:
        receipt = validate_route(
            packet_id="packet-economical-user-override",
            mode="economical",
            semantic_role="implementation",
            agent_type="worker",
            model="gpt-5.6-terra",
            effort="high",
            fork_turns="none",
            user_profile_override=True,
            actual_model="gpt-5.6-terra",
            actual_effort="high",
        )
        self.assertTrue(receipt.allowed, receipt.defects)
        self.assertFalse(receipt.luna_required)

    def test_receipt_is_bound_to_packet_and_exact_dispatch_args(self) -> None:
        first = self.luna_route("economical", "implementation")
        same = self.luna_route("economical", "implementation")
        other_packet = validate_route(
            packet_id="packet-economical-implementation-other",
            mode="economical",
            semantic_role="implementation",
            agent_type="worker",
            model="gpt-5.6-luna",
            effort="high",
            fork_turns="none",
        )
        other_role = validate_route(
            packet_id=first.packet_id,
            mode="economical",
            semantic_role="verifier",
            agent_type="worker",
            model="gpt-5.6-luna",
            effort="max",
            fork_turns="none",
        )

        self.assertEqual(first.dispatch_fingerprint, same.dispatch_fingerprint)
        self.assertNotEqual(
            first.dispatch_fingerprint, other_packet.dispatch_fingerprint
        )
        self.assertNotEqual(
            first.dispatch_fingerprint, other_role.dispatch_fingerprint
        )

    def test_blank_packet_identity_is_rejected(self) -> None:
        receipt = validate_route(
            packet_id=" ",
            mode="economical",
            semantic_role="implementation",
            agent_type="worker",
            model="gpt-5.6-luna",
            effort="max",
            fork_turns="none",
        )

        self.assertFalse(receipt.allowed)
        self.assertIn("blank_packet_id", receipt.defects)

    def test_cli_returns_nonzero_for_invalid_route(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--packet-id",
                "packet-economical-implementation",
                "--mode",
                "economical",
                "--semantic-role",
                "implementation",
                "--agent-type",
                "worker",
                "--model",
                "gpt-5.6-sol",
                "--effort",
                "xhigh",
                "--fork-turns",
                "all",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 2)
        self.assertIn('"allowed": false', completed.stdout)


if __name__ == "__main__":
    unittest.main()
