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

    def resume(
        self,
        name: str,
        *,
        branch: str,
        allow_dirty: bool = False,
    ) -> tuple[Path, subprocess.CompletedProcess[str]]:
        worktree = self.root / name
        arguments = [
            "resume",
            "--repo",
            str(self.repository),
            "--worktree",
            str(worktree),
            "--branch",
            branch,
            "--expect-head",
            self.git("rev-parse", branch).stdout.strip(),
            "--owner",
            name,
        ]
        if allow_dirty:
            arguments.append("--allow-dirty")
        return worktree, self.guard(*arguments)

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

        existing_path = self.root / "existing-path"
        existing_path.mkdir()
        reused_path = self.guard(
            "prepare",
            "--repo",
            str(self.repository),
            "--worktree",
            str(existing_path),
            "--branch",
            "codex/issue-grinder/another-packet",
            "--base",
            self.base,
            "--owner",
            "another-packet",
            check=False,
        )
        self.assertEqual(reused_path.returncode, 2)
        self.assertIn("writer worktree path already exists", reused_path.stderr)

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

    def test_resume_restores_existing_branch_without_a_worktree(self) -> None:
        branch = "codex/issue-grinder/interrupted-packet"
        self.git("branch", branch, self.base)

        worktree, result = self.resume("interrupted-packet", branch=branch)
        receipt = json.loads(result.stdout)

        self.assertEqual(receipt["operation"], "resume")
        self.assertEqual(receipt["branch"], f"refs/heads/{branch}")
        self.assertEqual(receipt["head"], self.base)
        self.assertEqual(Path(str(receipt["worktree"])).resolve(), worktree.resolve())
        self.assertTrue(receipt["linked"])
        self.assertTrue(receipt["locked"])
        self.assertTrue(receipt["clean"])

    def test_resume_reuses_dirty_existing_worktree_only_when_allowed(self) -> None:
        worktree, receipt = self.prepare("interrupted-packet")
        self.git("worktree", "unlock", str(worktree))
        (worktree / "source.txt").write_text("partial implementation\n", encoding="utf-8")
        common_arguments = (
            "resume",
            "--repo",
            str(self.repository),
            "--worktree",
            str(worktree),
            "--branch",
            "codex/issue-grinder/interrupted-packet",
            "--expect-head",
            self.base,
            "--owner",
            "interrupted-packet",
        )

        rejected = self.guard(*common_arguments, check=False)
        after_rejection = self.git("worktree", "list", "--porcelain").stdout
        resumed = self.guard(*common_arguments, "--allow-dirty")
        resumed_receipt = json.loads(resumed.stdout)

        self.assertEqual(rejected.returncode, 2)
        self.assertIn("dirty without --allow-dirty", rejected.stderr)
        checkpoint_record = after_rejection.split(
            f"worktree {worktree.resolve()}\n", 1
        )[1]
        self.assertNotIn("\nlocked", checkpoint_record.split("\n\n", 1)[0])
        self.assertEqual(
            Path(str(resumed_receipt["worktree"])).resolve(), worktree.resolve()
        )
        self.assertFalse(resumed_receipt["clean"])
        self.assertTrue(resumed_receipt["locked"])
        self.assertEqual((worktree / "source.txt").read_text(), "partial implementation\n")

    def test_resume_refuses_parallel_replacement_for_checked_out_branch(self) -> None:
        existing_worktree, _ = self.prepare("interrupted-packet")
        replacement = self.guard(
            "resume",
            "--repo",
            str(self.repository),
            "--worktree",
            str(self.root / "replacement"),
            "--branch",
            "codex/issue-grinder/interrupted-packet",
            "--expect-head",
            self.base,
            "--owner",
            "replacement",
            check=False,
        )

        self.assertEqual(replacement.returncode, 2)
        self.assertIn(str(existing_worktree), replacement.stderr)
        self.assertIn("resume that exact worktree", replacement.stderr)


if __name__ == "__main__":
    unittest.main()
