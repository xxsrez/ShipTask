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
    def luna_route(self, mode: str, role: str = "implementation"):
        return validate_route(
            packet_id=f"packet-{mode}-{role}",
            mode=mode,
            semantic_role=role,
            agent_type="worker",
            model="gpt-5.6-luna",
            effort="max",
            fork_turns="none",
        )

    def test_three_economical_modes_admit_explicit_luna_max_work(self) -> None:
        for mode in ("balance", "swarm", "economical"):
            with self.subTest(mode=mode):
                receipt = self.luna_route(mode)
                self.assertTrue(receipt.allowed, receipt.defects)
                self.assertTrue(receipt.luna_required)
                self.assertEqual(receipt.telemetry_status, "telemetry_pending")

    def test_substantive_inherited_sol_is_rejected_in_all_three_modes(self) -> None:
        for mode in ("balance", "swarm", "economical"):
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
                self.assertIn("luna_max_effort_required", receipt.defects)
                self.assertIn("unbounded_or_missing_fork_turns", receipt.defects)

    def test_agent_type_label_does_not_override_explicit_profile(self) -> None:
        for agent_type in ("default", "worker", "explorer", "custom-quality"):
            with self.subTest(agent_type=agent_type):
                receipt = validate_route(
                    packet_id=f"packet-swarm-{agent_type}",
                    mode="swarm",
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

    def test_balance_keeps_material_judgment_on_controller_profile(self) -> None:
        receipt = validate_route(
            packet_id="packet-balance-material-judgment",
            mode="balance",
            semantic_role="material_judgment",
            agent_type="default",
            model="gpt-5.6-sol",
            effort="xhigh",
            fork_turns="none",
            actual_model="gpt-5.6-sol",
            actual_effort="xhigh",
        )
        self.assertTrue(receipt.allowed, receipt.defects)
        self.assertFalse(receipt.luna_required)
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
            packet_id="packet-balance-test-author",
            mode="balance",
            semantic_role="test_author",
            agent_type="default",
            model="gpt-5.6-luna",
            effort="max",
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

    def test_balance_routine_packet_loop_requires_luna(self) -> None:
        for role in (
            "packet_lead",
            "research",
            "implementation",
            "test_author",
            "test_runner",
            "verifier",
            "critic",
            "reducer",
            "rework",
        ):
            with self.subTest(role=role):
                receipt = self.luna_route("balance", role)
                self.assertTrue(receipt.allowed, receipt.defects)
                self.assertTrue(receipt.luna_required)

    def test_receipt_is_bound_to_packet_and_exact_dispatch_args(self) -> None:
        first = self.luna_route("balance", "implementation")
        same = self.luna_route("balance", "implementation")
        other_packet = validate_route(
            packet_id="packet-balance-implementation-other",
            mode="balance",
            semantic_role="implementation",
            agent_type="worker",
            model="gpt-5.6-luna",
            effort="max",
            fork_turns="none",
        )
        other_role = validate_route(
            packet_id=first.packet_id,
            mode="balance",
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
            mode="balance",
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
