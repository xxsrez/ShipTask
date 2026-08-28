from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
GUARD = ROOT / "issue-grinder" / "scripts" / "writer_worktree_guard.py"


class WriterWorktreeGuardTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.repository = self.root / "repository"
        self.repository.mkdir()
        self.git("init")
        self.git("symbolic-ref", "HEAD", "refs/heads/main")
        self.git("config", "user.name", "Issue Grinder Test")
        self.git("config", "user.email", "issue-grinder@example.invalid")
        (self.repository / "source.txt").write_text("base\n", encoding="utf-8")
        self.git("add", "source.txt")
        self.git("commit", "-m", "initial")
        self.base = self.git("rev-parse", "HEAD").stdout.strip()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def git(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(self.repository), *arguments],
            check=True,
            capture_output=True,
            text=True,
        )

    def guard(
        self,
        *arguments: str,
        cwd: Path | None = None,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(GUARD), *arguments],
            cwd=cwd or self.repository,
            check=check,
            capture_output=True,
            text=True,
        )

    def prepare(self, name: str) -> tuple[Path, dict[str, object]]:
        worktree = self.root / name
        result = self.guard(
            "prepare",
            "--repo",
            str(self.repository),
            "--worktree",
            str(worktree),
            "--branch",
            f"codex/issue-grinder/{name}",
            "--base",
            self.base,
            "--owner",
            name,
        )
        return worktree, json.loads(result.stdout)

    def test_prepare_creates_distinct_locked_writer_worktrees(self) -> None:
        first, first_receipt = self.prepare("packet-one")
        second, second_receipt = self.prepare("packet-two")

        self.assertEqual(first_receipt["schema"], "issue-grinder/writer-worktree/v1")
        self.assertEqual(first_receipt["head"], self.base)
        self.assertEqual(first_receipt["branch"], "refs/heads/codex/issue-grinder/packet-one")
        self.assertTrue(first_receipt["clean"])
        self.assertTrue(first_receipt["linked"])
        self.assertTrue(first_receipt["locked"])
        self.assertNotEqual(first_receipt["worktree"], second_receipt["worktree"])
        self.assertNotEqual(first_receipt["git_dir"], second_receipt["git_dir"])
        self.assertEqual(first_receipt["common_dir"], second_receipt["common_dir"])

        admitted = self.guard(
            "admit",
            "--expect-worktree",
            str(first),
            "--expect-branch",
            "codex/issue-grinder/packet-one",
            "--expect-head",
            self.base,
            "--expect-common-dir",
            str(first_receipt["common_dir"]),
            "--owner",
            "packet-one",
            cwd=first,
        )
        self.assertEqual(json.loads(admitted.stdout)["operation"], "admit")

    def test_admission_rejects_shared_main_checkout(self) -> None:
        worktree, receipt = self.prepare("packet-one")
        rejected = self.guard(
            "admit",
            "--expect-worktree",
            str(worktree),
            "--expect-branch",
            "codex/issue-grinder/packet-one",
            "--expect-head",
            self.base,
            "--expect-common-dir",
            str(receipt["common_dir"]),
            "--owner",
            "packet-one",
            cwd=self.repository,
            check=False,
        )
        self.assertEqual(rejected.returncode, 2)
        self.assertIn("current working directory", rejected.stderr)
        self.assertIn("not admitted writer worktree", rejected.stderr)

    def test_admission_rejects_wrong_expected_state(self) -> None:
        worktree, receipt = self.prepare("packet-one")
        rejected = self.guard(
            "admit",
            "--expect-worktree",
            str(worktree),
            "--expect-branch",
            "codex/issue-grinder/packet-one",
            "--expect-head",
            "0" * 40,
            "--expect-common-dir",
            str(receipt["common_dir"]),
            "--owner",
            "packet-one",
            cwd=worktree,
            check=False,
        )
        self.assertEqual(rejected.returncode, 2)
        self.assertIn("HEAD mismatch", rejected.stderr)

    def test_integration_guard_detects_any_shared_checkout_write(self) -> None:
        snapshot_path = self.root / "integration-guard.json"
        snapshot = self.guard(
            "snapshot",
            "--worktree",
            str(self.repository),
            "--output",
            str(snapshot_path),
        )
        self.assertEqual(json.loads(snapshot.stdout)["operation"], "snapshot")

        (self.repository / "source.txt").write_text("stray writer change\n", encoding="utf-8")
        rejected = self.guard(
            "assert-unchanged",
            "--snapshot",
            str(snapshot_path),
            check=False,
        )
        self.assertEqual(rejected.returncode, 2)
        self.assertIn("integration worktree changed during writer wave", rejected.stderr)
        self.assertIn("status_sha256", rejected.stderr)

    def test_prepare_does_not_reuse_existing_branch_or_path(self) -> None:
        self.prepare("packet-one")
        reused_branch = self.guard(
            "prepare",
            "--repo",
            str(self.repository),
            "--worktree",
            str(self.root / "another-path"),
            "--branch",
            "codex/issue-grinder/packet-one",
            "--base",
            self.base,
            "--owner",
            "another-packet",
            check=False,
        )
        self.assertEqual(reused_branch.returncode, 2)
        self.assertIn("writer branch already exists", reused_branch.stderr)

    def test_receipt_cannot_dirty_a_git_worktree(self) -> None:
        receipt_path = self.repository / "guard-receipt.json"
        rejected = self.guard(
            "snapshot",
            "--worktree",
            str(self.repository),
            "--output",
            str(receipt_path),
            check=False,
        )
        self.assertEqual(rejected.returncode, 2)
        self.assertIn("receipt must be outside every Git worktree", rejected.stderr)
        self.assertFalse(receipt_path.exists())

    def test_snapshot_rejects_dirty_integration_checkout(self) -> None:
        (self.repository / "untracked.txt").write_text("dirty\n", encoding="utf-8")
        rejected = self.guard(
            "snapshot",
            "--worktree",
            str(self.repository),
            check=False,
        )
        self.assertEqual(rejected.returncode, 2)
        self.assertIn("must be clean before a parallel writer wave", rejected.stderr)

    def test_dirty_resume_requires_explicit_allow_dirty(self) -> None:
        worktree, receipt = self.prepare("packet-one")
        (worktree / "source.txt").write_text("unfinished checkpoint\n", encoding="utf-8")
        common_arguments = (
            "admit",
            "--expect-worktree",
            str(worktree),
            "--expect-branch",
            "codex/issue-grinder/packet-one",
            "--expect-head",
            self.base,
            "--expect-common-dir",
            str(receipt["common_dir"]),
            "--owner",
            "packet-one",
        )

        rejected = self.guard(*common_arguments, cwd=worktree, check=False)
        admitted = self.guard(
            *common_arguments,
            "--allow-dirty",
            cwd=worktree,
        )

        self.assertEqual(rejected.returncode, 2)
        self.assertIn("dirty before admission", rejected.stderr)
        self.assertFalse(json.loads(admitted.stdout)["clean"])


if __name__ == "__main__":
    unittest.main()
