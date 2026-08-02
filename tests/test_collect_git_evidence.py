"""Focused standard-library integration tests for the Git evidence collector."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
COLLECTOR = ROOT / "skills" / "summarizing-internship-work" / "scripts" / "collect_git_evidence.py"
SPEC = importlib.util.spec_from_file_location("collect_git_evidence", COLLECTOR)
assert SPEC is not None and SPEC.loader is not None
collector = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(collector)


def run_git(repository: Path, *arguments: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repository), *arguments],
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )


class CollectGitEvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name)
        self.repository = self.root / "repository"
        self.repository.mkdir()
        run_git(self.repository, "init", "--initial-branch", "main")
        self.ada_commit = self._commit(
            "Ada Lovelace",
            "ada@corp.example",
            "Add service\n\nCo-authored-by: Grace Hopper <grace@corp.example>",
            "src/service.py",
            "def run():\n    return 'ok'\n",
            committer=("Release Bot", "release-bot@corp.example"),
        )
        self.ada_alias_commit = self._commit(
            "Ada Lovelace",
            "ada+alias@corp.example",
            "Document service",
            "docs/service.md",
            "# Service\n",
        )
        run_git(self.repository, "remote", "add", "origin", "https://example.invalid/team/repository.git")

    def _commit(
        self,
        name: str,
        email: str,
        message: str,
        relative_path: str,
        content: str,
        committer: tuple[str, str] | None = None,
    ) -> str:
        target = self.repository / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        run_git(self.repository, "add", "--all")
        committer_name, committer_email = committer or (name, email)
        environment = os.environ.copy()
        environment.update(
            {
                "GIT_AUTHOR_NAME": name,
                "GIT_AUTHOR_EMAIL": email,
                "GIT_COMMITTER_NAME": committer_name,
                "GIT_COMMITTER_EMAIL": committer_email,
                "GIT_AUTHOR_DATE": "2024-01-01T12:00:00+00:00",
                "GIT_COMMITTER_DATE": "2024-01-01T12:00:00+00:00",
            }
        )
        run_git(self.repository, "commit", "--no-gpg-sign", "--message", message, env=environment)
        return run_git(self.repository, "rev-parse", "HEAD").stdout.strip()

    def run_collector(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(COLLECTOR), *arguments],
            capture_output=True,
            text=True,
            cwd=ROOT,
            check=False,
        )

    def document(self, *arguments: str) -> dict[str, object]:
        completed = self.run_collector(*arguments)
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertEqual("", completed.stderr)
        return json.loads(completed.stdout)

    def test_contributors_discovers_authors_and_coauthors(self) -> None:
        document = self.document("contributors", "--repo", str(self.repository))
        contributors = {(entry["name"], entry["email"]): entry for entry in document["contributors"]}
        self.assertIn(("Ada Lovelace", "ada@corp.example"), contributors)
        self.assertIn(("Grace Hopper", "grace@corp.example"), contributors)
        self.assertEqual(1, contributors[("Ada Lovelace", "ada@corp.example")]["commit_count"])

    def test_collect_filters_commits_to_the_requested_author(self) -> None:
        document = self.document(
            "collect",
            "--repo",
            str(self.repository),
            "--author",
            "ada@corp.example",
        )
        self.assertEqual([self.ada_commit], [commit["commit_id"] for commit in document["commits"]])
        self.assertEqual(["ada@corp.example"], document["scope"]["authors"])

    def test_collect_requires_a_complete_author_name_or_email(self) -> None:
        document = self.document(
            "collect",
            "--repo",
            str(self.repository),
            "--author",
            "a",
        )
        self.assertEqual([], document["commits"])

    def test_collect_includes_commits_where_identity_is_a_coauthor(self) -> None:
        document = self.document(
            "collect",
            "--repo",
            str(self.repository),
            "--author",
            "  GRACE@CORP.EXAMPLE  ",
        )
        self.assertEqual([self.ada_commit], [commit["commit_id"] for commit in document["commits"]])

    def test_collect_enforces_the_commit_limit_and_reports_the_boundary(self) -> None:
        document = self.document(
            "collect",
            "--repo",
            str(self.repository),
            "--author",
            "Ada Lovelace",
            "--max-commits",
            "1",
        )
        self.assertEqual(1, len(document["commits"]))
        self.assertIn(
            "commit_limit_reached",
            [warning["code"] for warning in document["warnings"]],
        )

    def test_contributors_accepts_the_same_bounded_history_limit(self) -> None:
        document = self.document(
            "contributors",
            "--repo",
            str(self.repository),
            "--max-commits",
            "1",
        )
        self.assertEqual(1, document["scope"]["max_commits"])
        self.assertIn(
            "commit_limit_reached",
            [warning["code"] for warning in document["warnings"]],
        )

    def test_history_query_pushes_filters_to_git_and_caps_scanned_records(self) -> None:
        fields = (
            "{sha}\x1f\x1fAda Lovelace\x1fada@corp.example\x1f"
            "Ada Lovelace\x1fada@corp.example\x1f2024-01-01T12:00:00+00:00\x1f"
            "2024-01-01T12:00:00+00:00\x1fCommit {index}\x1e"
        )

        class RecordingGit:
            def __init__(self) -> None:
                self.log_arguments: tuple[str, ...] | None = None

            def run(self, *arguments: str, allow_failure: bool = False) -> subprocess.CompletedProcess[str]:
                if arguments[:2] == ("rev-parse", "--verify"):
                    return subprocess.CompletedProcess(arguments, 0, "head\n", "")
                self.log_arguments = arguments
                output = "".join(
                    fields.format(sha=str(index) * 40, index=index)
                    for index in range(1, 4)
                )
                return subprocess.CompletedProcess(arguments, 0, output, "")

        git = RecordingGit()
        commits, reached_limit = collector._parse_history(
            git,
            since=collector._parse_date("2024-01-01"),
            until=collector._parse_date("2024-02-01"),
            max_commits=2,
            include_merges=False,
            paths=["src"],
        )

        self.assertEqual(2, len(commits))
        self.assertTrue(reached_limit)
        assert git.log_arguments is not None
        self.assertIn("--since=2024-01-01T00:00:00Z", git.log_arguments)
        self.assertIn("--before=2024-02-01T00:00:00Z", git.log_arguments)
        self.assertIn("--max-count=3", git.log_arguments)
        self.assertIn("--no-merges", git.log_arguments)
        self.assertEqual(("--", "src"), git.log_arguments[-2:])

    def test_collect_includes_changed_file_evidence(self) -> None:
        document = self.document(
            "collect",
            "--repo",
            str(self.repository),
            "--author",
            "Ada Lovelace",
            "--path",
            "src/service.py",
        )
        change = next(item for item in document["file_changes"] if item["path"] == "src/service.py")
        self.assertEqual(self.ada_commit, change["commit_id"])
        self.assertEqual("added", change["status"])
        self.assertFalse(change["binary"])
        self.assertEqual(1, len(document["evidence"]))
        self.assertEqual(self.ada_commit, document["evidence"][0]["commit"])

    def test_public_collection_redacts_repository_and_personal_identifiers(self) -> None:
        document = self.document(
            "collect",
            "--repo",
            str(self.repository),
            "--author",
            "Ada Lovelace",
            "--sensitivity",
            "public",
        )
        serialized = json.dumps(document)
        self.assertIsNone(document["repository"]["root"])
        self.assertIsNone(document["repository"]["remote_url"])
        for name in ("Ada", "Grace", "Release Bot"):
            self.assertNotIn(name, serialized)
        for email in (
            "ada@corp.example",
            "ada+alias@corp.example",
            "grace@corp.example",
            "release-bot@corp.example",
        ):
            label = f"contributor-{hashlib.sha256(email.encode('utf-8')).hexdigest()[:12]}"
            self.assertIn(label, serialized)
        self.assertNotIn("Ada Lovelace", document["scope"]["authors"])
        self.assertIn("[REDACTED:email-local]@[REDACTED:internal-domain]", serialized)

    def test_invalid_repository_returns_a_controlled_error(self) -> None:
        invalid_repository = self.root / "not-a-repository"
        invalid_repository.mkdir()
        completed = self.run_collector("collect", "--repo", str(invalid_repository))
        self.assertEqual(3, completed.returncode)
        self.assertEqual("", completed.stdout)
        self.assertIn("target is not a Git repository", completed.stderr)

    def test_date_filters_use_inclusive_since_and_exclusive_until(self) -> None:
        observed = {"authored_at": "2024-01-01T12:00:00+00:00"}
        self.assertTrue(
            collector._matches_date(
                observed,
                collector._parse_date("2024-01-01"),
                collector._parse_date("2024-01-02"),
            )
        )
        self.assertFalse(
            collector._matches_date(
                observed,
                None,
                collector._parse_date("2024-01-01T12:00:00Z"),
            )
        )

    def test_merge_limit_and_rename_selection_helpers_preserve_expected_boundaries(self) -> None:
        self.assertEqual(
            [{"path": "new.py", "old_path": "old.py", "status": "renamed"}],
            collector._parse_name_status("R100\0old.py\0new.py\0"),
        )
        self.assertEqual(
            ("diff-tree", "--root", "--name-status", "root"),
            collector._diff_arguments({"parents": [], "sha": "root"}, "diff-tree", "--name-status"),
        )
        self.assertEqual(
            ("diff-tree", "--name-status", "parent", "merge"),
            collector._diff_arguments(
                {"parents": ["parent", "other"], "sha": "merge"}, "diff-tree", "--name-status"
            ),
        )

    def test_skip_classification_covers_generated_binary_and_oversized_paths(self) -> None:
        self.assertEqual("generated", collector._skip_reason("assets/app.min.js", False, 5))
        self.assertEqual("binary", collector._skip_reason("assets/image.png", True, 5))
        self.assertEqual("oversized", collector._skip_reason("src/large.py", False, collector.MAX_TEXT_BYTES + 1))
        self.assertEqual("excluded-directory", collector._skip_reason("node_modules/pkg/index.js", False, 5))

    def test_git_runner_removes_hostile_environment_and_uses_an_external_nonexistent_hooks_path(self) -> None:
        hostile = {
            "GIT_DIR": "unsafe",
            "GIT_WORK_TREE": "unsafe",
            "GIT_CONFIG_COUNT": "1",
            "GIT_CONFIG_KEY_0": "alias.x",
            "GIT_CONFIG_VALUE_0": "unsafe",
            "GIT_PAGER": "unsafe",
        }
        with mock.patch.dict(os.environ, hostile, clear=True):
            environment = collector.GitRunner._environment()
        for name in hostile:
            if name != "GIT_PAGER":
                self.assertNotIn(name, environment)
        self.assertEqual("cat", environment["GIT_PAGER"])
        runner = collector.GitRunner(self.repository)
        command = runner._command("status")
        hooks_value = next(value for index, value in enumerate(command) if command[index - 1] == "-c" and value.startswith("core.hooksPath="))
        hooks_path = Path(hooks_value.split("=", 1)[1])
        self.assertFalse(hooks_path.exists())
        self.assertNotEqual(self.repository.resolve(), hooks_path)
        self.assertNotIn(self.repository.resolve(), hooks_path.parents)
        self.assertNotIn(ROOT.resolve(), hooks_path.parents)

    def test_broad_secret_redaction_and_atomic_output_writing(self) -> None:
        redacted, categories = collector._redact_text(
            "password=one credential=two secret=three token=four "
            "-----BEGIN PRIVATE KEY-----private"
        )
        self.assertEqual({"password", "credential", "secret", "token", "private-key"}, set(categories))
        self.assertNotIn("one", redacted)
        destination = self.root / "output.json"
        collector._write_output("{\"ok\":true}\n", str(destination))
        self.assertEqual("{\"ok\":true}\n", destination.read_text(encoding="utf-8"))

    def test_malformed_arguments_missing_git_and_query_failure_are_controlled(self) -> None:
        malformed = self.run_collector("collect", "--repo", str(self.repository), "--path", "../escape")
        self.assertEqual(2, malformed.returncode)
        self.assertIn("repository-relative POSIX", malformed.stderr)
        runner = collector.GitRunner(self.repository)
        with mock.patch.object(collector.subprocess, "run", side_effect=FileNotFoundError):
            with self.assertRaisesRegex(collector.CollectorError, "Git is unavailable") as missing_git:
                runner.run("status")
        self.assertEqual(3, missing_git.exception.exit_code)
        failed = subprocess.CompletedProcess(["git"], 1, "", "query failed")
        with mock.patch.object(collector.subprocess, "run", return_value=failed):
            with self.assertRaisesRegex(collector.CollectorError, "query failed") as failed_query:
                runner.run("status")
        self.assertEqual(4, failed_query.exception.exit_code)


if __name__ == "__main__":
    unittest.main()
