#!/usr/bin/env python3
"""Collect deterministic, content-free evidence from a local Git repository."""

from __future__ import annotations

import argparse
from datetime import date, datetime, time, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import subprocess
import sys
import tempfile
from typing import Any, Sequence


SCHEMA_VERSION = "1.0"
MAX_TEXT_BYTES = 1_048_576
SKIPPED_DIRECTORIES = frozenset(
    {
        ".git",
        "node_modules",
        "vendor",
        ".venv",
        "venv",
        "Pods",
        "DerivedData",
        "dist",
        "build",
        "target",
        "out",
        ".next",
        ".nuxt",
        ".gradle",
        ".idea",
        ".cache",
        "__pycache__",
    }
)
GENERATED_NAMES = frozenset(
    {"package-lock.json", "yarn.lock", "pnpm-lock.yaml", "Podfile.lock", "Cargo.lock"}
)
GENERATED_SUFFIXES = (".min.js", ".min.css", ".map")
COAUTHOR_RE = re.compile(
    r"(?im)^Co-authored-by:\s*(?P<name>[^\r\n<]+?)\s*<(?P<email>[^>\r\n]+)>\s*$"
)
INTERNAL_DOMAIN_MARKERS = frozenset({"corp", "internal", "intranet", "local", "lan"})
EMAIL_RE = re.compile(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9.-]+")
DOMAIN_RE = re.compile(r"(?i)(?:[A-Za-z0-9-]+\.)+[A-Za-z0-9-]+")
SECRET_PATTERNS = (
    (
        "private-key",
        re.compile(r"-----BEGIN(?: [A-Z0-9]+)* PRIVATE KEY-----.*", re.IGNORECASE),
    ),
    (
        "credential",
        re.compile(r"(?i)\b[A-Za-z0-9_.-]*credential[A-Za-z0-9_.-]*\s*[:=]\s*(?:['\"][^'\"]*['\"]|\S+)"),
    ),
    (
        "password",
        re.compile(r"(?i)\b[A-Za-z0-9_.-]*password[A-Za-z0-9_.-]*\s*[:=]\s*(?:['\"][^'\"]*['\"]|\S+)"),
    ),
    (
        "secret",
        re.compile(r"(?i)\b[A-Za-z0-9_.-]*secret[A-Za-z0-9_.-]*\s*[:=]\s*(?:['\"][^'\"]*['\"]|\S+)"),
    ),
    (
        "token",
        re.compile(r"(?i)\b[A-Za-z0-9_.-]*token[A-Za-z0-9_.-]*\s*[:=]\s*(?:['\"][^'\"]*['\"]|\S+)"),
    ),
    (
        "cloud-token",
        re.compile(r"\b(?:AKIA[0-9A-Z]{16}|ASIA[0-9A-Z]{16})\b"),
    ),
    (
        "code-host-token",
        re.compile(
            r"\b(?:gh[pousr]_[A-Za-z0-9]{20,255}|github_pat_[A-Za-z0-9_]{20,255}|glpat-[A-Za-z0-9_-]{20,255})\b"
        ),
    ),
    (
        "service-token",
        re.compile(r"\b(?:xox[baprs]-[A-Za-z0-9-]{10,255}|AIza[0-9A-Za-z_-]{30,})\b"),
    ),
)


class CollectorError(Exception):
    """A controlled collector failure with a documented exit code."""

    def __init__(self, message: str, exit_code: int) -> None:
        super().__init__(message)
        self.exit_code = exit_code


class GitRunner:
    def __init__(self, repository: Path) -> None:
        self.repository = repository

    def _command(self, *arguments: str) -> list[str]:
        # A unique, never-created path disables repository hooks without mutating either workspace.
        disabled_hooks = Path(tempfile.gettempdir()) / f".internship-work-summary-disabled-hooks-{os.getpid()}-{id(self)}"
        return [
            "git",
            "--no-pager",
            "--no-optional-locks",
            "-c",
            "core.fsmonitor=false",
            "-c",
            f"core.hooksPath={disabled_hooks}",
            "-c",
            "core.untrackedCache=false",
            "-c",
            "diff.external=",
            "-c",
            "diff.trustExitCode=false",
            "-c",
            "log.showSignature=false",
            "-c",
            "color.ui=false",
            "-C",
            str(self.repository),
            *arguments,
        ]

    @staticmethod
    def _environment() -> dict[str, str]:
        environment = os.environ.copy()
        for name in tuple(environment):
            if name.startswith("GIT_CONFIG_KEY_") or name.startswith("GIT_CONFIG_VALUE_"):
                environment.pop(name, None)
        for name in (
            "GIT_CONFIG_COUNT",
            "GIT_CONFIG_SYSTEM",
            "GIT_CONFIG_GLOBAL",
            "GIT_DIR",
            "GIT_WORK_TREE",
            "GIT_INDEX_FILE",
            "GIT_OBJECT_DIRECTORY",
            "GIT_ALTERNATE_OBJECT_DIRECTORIES",
            "GIT_COMMON_DIR",
            "GIT_EXTERNAL_DIFF",
            "GIT_DIFF_OPTS",
            "GIT_PAGER",
        ):
            environment.pop(name, None)
        environment.update(
            {
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": os.devnull,
                "GIT_OPTIONAL_LOCKS": "0",
                "GIT_TERMINAL_PROMPT": "0",
                "GIT_PAGER": "cat",
                "PAGER": "cat",
            }
        )
        return environment

    def run(self, *arguments: str, allow_failure: bool = False) -> subprocess.CompletedProcess[str]:
        try:
            completed = subprocess.run(
                self._command(*arguments),
                capture_output=True,
                encoding="utf-8",
                errors="strict",
                env=self._environment(),
                check=False,
            )
        except FileNotFoundError as error:
            raise CollectorError("Git is unavailable", 3) from error
        except (OSError, UnicodeError) as error:
            raise CollectorError(f"Git output could not be read: {error}", 5) from error
        if completed.returncode != 0 and not allow_failure:
            diagnostic = completed.stderr.strip() or "Git query failed"
            raise CollectorError(diagnostic, 4)
        return completed

    def read_prefix(self, limit: int, *arguments: str) -> bytes:
        try:
            process = subprocess.Popen(
                self._command(*arguments),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=self._environment(),
            )
        except FileNotFoundError as error:
            raise CollectorError("Git is unavailable", 3) from error
        except OSError as error:
            raise CollectorError(f"Git output could not be read: {error}", 5) from error
        assert process.stdout is not None
        assert process.stderr is not None
        prefix = process.stdout.read(limit)
        if len(prefix) < limit:
            return_code = process.wait()
            diagnostic = process.stderr.read()
            if return_code != 0:
                message = diagnostic.decode("utf-8", errors="replace").strip() or "Git query failed"
                raise CollectorError(message, 4)
            return prefix
        process.stdout.close()
        process.terminate()
        process.wait()
        return prefix


def _positive_integer(value: str) -> int:
    try:
        number = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("max commits must be a positive integer") from error
    if number <= 0:
        raise argparse.ArgumentTypeError("max commits must be positive")
    return number


def _parse_date(value: str) -> datetime:
    try:
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            return datetime.combine(date.fromisoformat(value), time.min, tzinfo=timezone.utc)
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise argparse.ArgumentTypeError(f"invalid ISO-8601 date: {value}") from error
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise argparse.ArgumentTypeError("date-time values must include a timezone")
    return parsed.astimezone(timezone.utc)


def _format_time(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _repo_path(value: str) -> str:
    posix = PurePosixPath(value)
    windows = PureWindowsPath(value)
    if (
        not value
        or "\\" in value
        or posix.is_absolute()
        or windows.is_absolute()
        or windows.drive
        or ".." in posix.parts
        or value == "."
    ):
        raise argparse.ArgumentTypeError(f"path must be repository-relative POSIX syntax: {value!r}")
    return posix.as_posix().rstrip("/")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    def common(subparser: argparse.ArgumentParser) -> None:
        subparser.add_argument("--repo", required=True, type=Path)
        subparser.add_argument("--since", type=_parse_date)
        subparser.add_argument("--until", type=_parse_date)
        subparser.add_argument("--max-commits", type=_positive_integer, default=500)
        subparser.add_argument("--output", default="-")
        subparser.add_argument("--pretty", action="store_true")

    contributors = subparsers.add_parser("contributors", help="list observed contributor identities")
    common(contributors)

    collect = subparsers.add_parser("collect", help="collect commit and file evidence")
    common(collect)
    collect.add_argument("--author", action="append", default=[])
    collect.add_argument("--path", action="append", default=[], type=_repo_path)
    collect.add_argument("--include-merges", action="store_true")
    collect.add_argument("--sensitivity", choices=("internal", "public"), default="internal")
    return parser


def _normalize_email(value: str) -> str:
    return value.strip().lower()


def _redact_text(value: str) -> tuple[str, list[str]]:
    redacted = value
    categories: list[str] = []
    for category, pattern in SECRET_PATTERNS:
        redacted, count = pattern.subn(f"[REDACTED:{category}]", redacted)
        if count:
            categories.append(category)
    return redacted, sorted(set(categories))


def _is_internal_domain(domain: str) -> bool:
    labels = {label.casefold() for label in domain.split(".")}
    return bool(labels & INTERNAL_DOMAIN_MARKERS) or domain.casefold().endswith((".internal", ".local"))


def _public_email(value: str) -> str:
    if "@" not in value:
        return "[REDACTED:email-local]"
    _, domain = value.rsplit("@", 1)
    visible_domain = "[REDACTED:internal-domain]" if _is_internal_domain(domain) else domain.lower()
    return f"[REDACTED:email-local]@{visible_domain}"


def _public_identity_label(email: str) -> str:
    digest = hashlib.sha256(_normalize_email(email).encode("utf-8")).hexdigest()[:12]
    return f"contributor-{digest}"


def _public_author_filter(value: str) -> str:
    normalized = value.strip().casefold()
    if EMAIL_RE.fullmatch(normalized):
        return _public_identity_label(normalized)
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:12]
    return f"author-filter-{digest}"


def _public_text(value: str) -> str:
    masked_emails = EMAIL_RE.sub(lambda match: _public_email(match.group(0)), value)
    return DOMAIN_RE.sub(
        lambda match: "[REDACTED:internal-domain]" if _is_internal_domain(match.group(0)) else match.group(0),
        masked_emails,
    )


def _sanitize_output(value: Any, sensitivity: str) -> tuple[Any, set[str]]:
    categories: set[str] = set()

    def sanitize(item: Any) -> Any:
        if isinstance(item, str):
            redacted, found = _redact_text(item)
            categories.update(found)
            return _public_text(redacted) if sensitivity == "public" else redacted
        if isinstance(item, list):
            return [sanitize(child) for child in item]
        if isinstance(item, dict):
            return {key: sanitize(child) for key, child in item.items()}
        return item

    return sanitize(value), categories


def _display_identity(name: str, email: str, sensitivity: str) -> dict[str, str]:
    return {
        "name": _public_identity_label(email) if sensitivity == "public" else name,
        "email": _public_email(email) if sensitivity == "public" else email,
    }


def _tool_version() -> str:
    version_path = Path(__file__).resolve().parents[1] / "VERSION"
    try:
        value = version_path.read_text(encoding="utf-8").strip()
    except (OSError, UnicodeError) as error:
        raise CollectorError(f"tool version could not be read: {error}", 5) from error
    if not value:
        raise CollectorError("tool version is empty", 5)
    return value


def _open_repository(candidate: Path) -> tuple[Path, GitRunner]:
    try:
        resolved = candidate.expanduser().resolve(strict=True)
    except (OSError, RuntimeError) as error:
        raise CollectorError(f"repository is unavailable: {error}", 3) from error
    runner = GitRunner(resolved)
    probe = runner.run("rev-parse", "--show-toplevel", allow_failure=True)
    if probe.returncode != 0:
        raise CollectorError("target is not a Git repository", 3)
    try:
        root = Path(probe.stdout.strip()).resolve(strict=True)
    except (OSError, RuntimeError) as error:
        raise CollectorError(f"repository root is unavailable: {error}", 3) from error
    return root, GitRunner(root)


def _has_head(git: GitRunner) -> bool:
    return git.run("rev-parse", "--verify", "HEAD", allow_failure=True).returncode == 0


def _parse_history(
    git: GitRunner,
    *,
    since: datetime | None,
    until: datetime | None,
    max_commits: int,
    include_merges: bool,
    paths: list[str],
) -> tuple[list[dict[str, Any]], bool]:
    if not _has_head(git):
        return [], False
    fields = "%H%x1f%P%x1f%an%x1f%ae%x1f%cn%x1f%ce%x1f%aI%x1f%cI%x1f%B%x1e"
    arguments = ["log", "--no-ext-diff", "--no-textconv", f"--format={fields}"]
    if since is not None:
        arguments.append(f"--since={_format_time(since)}")
    if until is not None:
        arguments.append(f"--before={_format_time(until)}")
    if not include_merges:
        arguments.append("--no-merges")
    arguments.extend((f"--max-count={max_commits + 1}", "HEAD"))
    if paths:
        arguments.extend(("--", *paths))
    output = git.run(*arguments).stdout
    commits: list[dict[str, Any]] = []
    for raw_record in output.split("\x1e"):
        record = raw_record.strip("\r\n")
        if not record:
            continue
        values = record.split("\x1f", 8)
        if len(values) != 9:
            raise CollectorError("Git returned an unexpected commit record", 4)
        sha, parents, author_name, author_email, committer_name, committer_email, authored_at, committed_at, message = values
        commits.append(
            {
                "sha": sha,
                "parents": parents.split() if parents else [],
                "author_name": author_name,
                "author_email": author_email,
                "committer_name": committer_name,
                "committer_email": committer_email,
                "authored_at": authored_at,
                "committed_at": committed_at,
                "message": message.rstrip("\r\n"),
            }
        )
    reached_limit = len(commits) > max_commits
    return commits[:max_commits], reached_limit


def _matches_date(commit: dict[str, Any], since: datetime | None, until: datetime | None) -> bool:
    observed = datetime.fromisoformat(commit["authored_at"].replace("Z", "+00:00")).astimezone(timezone.utc)
    return (since is None or observed >= since) and (until is None or observed < until)


def _matches_author(commit: dict[str, Any], authors: list[str]) -> bool:
    if not authors:
        return True
    requested = {" ".join(value.split()).casefold() for value in authors}
    observed = {
        " ".join(commit["author_name"].split()).casefold(),
        _normalize_email(commit["author_email"]),
    }
    for match in COAUTHOR_RE.finditer(commit["message"]):
        observed.add(" ".join(match.group("name").split()).casefold())
        observed.add(_normalize_email(match.group("email")))
    return bool(requested & observed)


def _parse_name_status(output: str) -> list[dict[str, Any]]:
    tokens = output.split("\0")
    changes: list[dict[str, Any]] = []
    index = 0
    while index < len(tokens) and tokens[index]:
        status_token = tokens[index]
        index += 1
        status_code = status_token[0]
        if status_code in {"R", "C"}:
            if index + 1 >= len(tokens):
                raise CollectorError("Git returned an incomplete rename record", 4)
            old_path, path = tokens[index], tokens[index + 1]
            index += 2
        else:
            if index >= len(tokens):
                raise CollectorError("Git returned an incomplete path record", 4)
            old_path, path = None, tokens[index]
            index += 1
        status = {
            "A": "added",
            "M": "modified",
            "D": "deleted",
            "R": "renamed",
            "C": "copied",
            "T": "type-changed",
            "U": "unmerged",
        }.get(status_code, "modified")
        changes.append({"path": PurePosixPath(path).as_posix(), "old_path": old_path, "status": status})
    return changes


def _parse_numstat(output: str) -> dict[tuple[str | None, str], tuple[int | None, int | None]]:
    tokens = output.split("\0")
    result: dict[tuple[str | None, str], tuple[int | None, int | None]] = {}
    index = 0
    while index < len(tokens) and tokens[index]:
        header = tokens[index]
        index += 1
        parts = header.split("\t", 2)
        if len(parts) != 3:
            raise CollectorError("Git returned an unexpected numstat record", 4)
        added_text, deleted_text, path = parts
        old_path: str | None = None
        if not path:
            if index + 1 >= len(tokens):
                raise CollectorError("Git returned an incomplete numstat rename", 4)
            old_path, path = tokens[index], tokens[index + 1]
            index += 2
        added = None if added_text == "-" else int(added_text)
        deleted = None if deleted_text == "-" else int(deleted_text)
        result[(old_path, PurePosixPath(path).as_posix())] = (added, deleted)
        result[(None, PurePosixPath(path).as_posix())] = (added, deleted)
    return result


def _diff_arguments(commit: dict[str, Any], *arguments: str) -> tuple[str, ...]:
    if len(commit["parents"]) > 1:
        return (*arguments, commit["parents"][0], commit["sha"])
    return (arguments[0], "--root", *arguments[1:], commit["sha"])


def _skip_reason(path: str, binary: bool, size: int | None) -> str | None:
    parts = PurePosixPath(path).parts
    if any(part in SKIPPED_DIRECTORIES for part in parts[:-1]):
        return "excluded-directory"
    name = parts[-1] if parts else path
    if name in GENERATED_NAMES or name.endswith(GENERATED_SUFFIXES):
        return "generated"
    if binary:
        return "binary"
    if size is not None and size > MAX_TEXT_BYTES:
        return "oversized"
    return None


def _blob_size(git: GitRunner, commit: dict[str, Any], change: dict[str, Any]) -> int | None:
    revision, path = _blob_location(commit, change)
    if revision is None:
        return None
    completed = git.run("cat-file", "-s", f"{revision}:{path}", allow_failure=True)
    if completed.returncode != 0:
        return None
    try:
        return int(completed.stdout.strip())
    except ValueError as error:
        raise CollectorError("Git returned an invalid blob size", 4) from error


def _blob_location(commit: dict[str, Any], change: dict[str, Any]) -> tuple[str | None, str]:
    if change["status"] == "deleted":
        if not commit["parents"]:
            return None, change["path"]
        return commit["parents"][0], change["path"]
    return commit["sha"], change["path"]


def _has_nul_prefix(git: GitRunner, commit: dict[str, Any], change: dict[str, Any]) -> bool:
    revision, path = _blob_location(commit, change)
    if revision is None:
        return False
    return b"\0" in git.read_prefix(8192, "cat-file", "blob", f"{revision}:{path}")


def _commit_files(git: GitRunner, commit: dict[str, Any]) -> list[dict[str, Any]]:
    safe_diff = ("--no-ext-diff", "--no-textconv")
    name_status = git.run(*_diff_arguments(commit, "diff-tree", *safe_diff, "--no-commit-id", "-r", "-M", "--name-status", "-z")).stdout
    numstat_output = git.run(*_diff_arguments(commit, "diff-tree", *safe_diff, "--no-commit-id", "-r", "-M", "--numstat", "-z")).stdout
    numstat = _parse_numstat(numstat_output)
    files: list[dict[str, Any]] = []
    for change in _parse_name_status(name_status):
        additions, deletions = numstat.get((change["old_path"], change["path"]), numstat.get((None, change["path"]), (0, 0)))
        binary = additions is None or deletions is None
        preliminary_skip = _skip_reason(change["path"], binary, None)
        size = None if preliminary_skip is not None else _blob_size(git, commit, change)
        if preliminary_skip is None and size is not None and _has_nul_prefix(git, commit, change):
            binary = True
            preliminary_skip = "binary"
        files.append(
            {
                "path": change["path"],
                "old_path": change["old_path"],
                "status": change["status"],
                "additions": additions,
                "deletions": deletions,
                "binary": binary,
                "size_bytes": size,
                "skipped_reason": preliminary_skip or _skip_reason(change["path"], binary, size),
            }
        )
    return sorted(files, key=lambda item: (item["path"], item["old_path"] or "", item["status"]))


def _path_matches(path: str, query: str) -> bool:
    return path == query or path.startswith(f"{query}/")


def _matches_paths(files: list[dict[str, Any]], paths: list[str]) -> bool:
    if not paths:
        return True
    return any(
        _path_matches(change["path"], query)
        or (change["old_path"] is not None and _path_matches(change["old_path"], query))
        for change in files
        for query in paths
    )


def _coauthors(message: str, sensitivity: str) -> list[dict[str, str]]:
    values = {
        (match.group("name").strip(), match.group("email").strip())
        for match in COAUTHOR_RE.finditer(message)
    }
    return [
        _display_identity(name, email, sensitivity)
        for name, email in sorted(values, key=lambda value: (value[0].casefold(), value[1].casefold()))
    ]


def _contributors(commits: list[dict[str, Any]], sensitivity: str) -> list[dict[str, Any]]:
    observations: dict[tuple[str, str], set[str]] = {}
    shared_emails: dict[str, set[tuple[str, str]]] = {}
    shared_names: dict[str, set[tuple[str, str]]] = {}

    def observe(name: str, email: str, commit_sha: str) -> None:
        clean_name = name.strip()
        clean_email = email.strip()
        key = (clean_name, clean_email)
        observations.setdefault(key, set()).add(commit_sha)
        shared_emails.setdefault(_normalize_email(clean_email), set()).add(key)
        shared_names.setdefault(clean_name.casefold(), set()).add(key)

    for commit in commits:
        observe(commit["author_name"], commit["author_email"], commit["sha"])
        observe(commit["committer_name"], commit["committer_email"], commit["sha"])
        for match in COAUTHOR_RE.finditer(commit["message"]):
            observe(match.group("name").strip(), match.group("email").strip(), commit["sha"])

    contributors: list[dict[str, Any]] = []
    for key in sorted(observations, key=lambda value: (value[0].casefold(), value[1].casefold())):
        name, email = key
        aliases: list[dict[str, str]] = []
        candidates = (shared_emails[_normalize_email(email)] - {key}, "shared_email")
        name_candidates = (shared_names[name.casefold()] - {key}, "shared_name")
        for identities, basis in (candidates, name_candidates):
            for alias_name, alias_email in sorted(identities, key=lambda item: (item[0].casefold(), item[1].casefold())):
                alias = {
                    "name": _public_identity_label(alias_email) if sensitivity == "public" else alias_name,
                    "email": _public_email(alias_email) if sensitivity == "public" else alias_email,
                    "basis": basis,
                }
                if alias not in aliases:
                    aliases.append(alias)
        visible_email = _public_email(email) if sensitivity == "public" else email
        contributors.append(
            {
                "name": _public_identity_label(email) if sensitivity == "public" else name,
                "email": visible_email,
                "commit_count": len(observations[key]),
                "aliases": aliases,
            }
        )
    return contributors


def _repository_metadata(root: Path, git: GitRunner, sensitivity: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    warnings: list[dict[str, Any]] = []
    branch_result = git.run("branch", "--show-current")
    head_result = git.run("rev-parse", "--verify", "HEAD", allow_failure=True)
    remote_result = git.run("config", "--get", "remote.origin.url", allow_failure=True)
    remote_url = remote_result.stdout.strip() if remote_result.returncode == 0 else None
    if remote_url:
        remote_url, categories = _redact_text(remote_url)
        warnings.extend(
            {"code": "secret_redacted", "evidence_ids": [], "message": f"repository metadata: {category}"}
            for category in categories
        )
    metadata = {
        "root": None if sensitivity == "public" else root.as_posix(),
        "remote_url": None if sensitivity == "public" else remote_url,
        "name": root.name,
        "branch": branch_result.stdout.strip() or None,
        "head": head_result.stdout.strip() if head_result.returncode == 0 else None,
        "is_dirty": bool(git.run("status", "--porcelain=v1", "-z").stdout),
        "is_shallow": git.run("rev-parse", "--is-shallow-repository").stdout.strip() == "true",
    }
    if metadata["is_dirty"]:
        warnings.append({"code": "dirty_worktree", "evidence_ids": [], "message": "working tree has local changes"})
    if metadata["is_shallow"]:
        warnings.append({"code": "shallow_repository", "evidence_ids": [], "message": "history may be incomplete"})
    return metadata, warnings


def _scope(arguments: argparse.Namespace) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    warnings: list[dict[str, Any]] = []

    def redacted_value(value: str) -> str:
        redacted, categories = _redact_text(value)
        warnings.extend(
            {"code": "secret_redacted", "evidence_ids": [], "message": f"scope value: {category}"}
            for category in categories
        )
        return redacted

    def safe_value(value: str) -> str:
        redacted = redacted_value(value)
        return _public_text(redacted) if getattr(arguments, "sensitivity", "internal") == "public" else redacted

    def safe_author(value: str) -> str:
        redacted = redacted_value(value)
        if getattr(arguments, "sensitivity", "internal") == "public":
            return _public_author_filter(redacted)
        return redacted

    scope: dict[str, Any] = {
        "mode": arguments.command,
        "since": _format_time(arguments.since),
        "until": _format_time(arguments.until),
        "authors": [],
        "paths": [],
        "max_commits": arguments.max_commits,
        "include_merges": False,
        "sensitivity": "internal",
    }
    if arguments.command == "collect":
        scope.update(
            {
                "authors": sorted({safe_author(value) for value in arguments.author}, key=str.casefold),
                "paths": sorted({safe_value(value) for value in arguments.path}, key=str.casefold),
                "max_commits": arguments.max_commits,
                "include_merges": arguments.include_merges,
                "sensitivity": arguments.sensitivity,
            }
        )
    else:
        scope["sensitivity"] = "internal"
    return scope, warnings


def _collect(arguments: argparse.Namespace) -> dict[str, Any]:
    if arguments.since and arguments.until and arguments.since >= arguments.until:
        raise CollectorError("--since must be earlier than --until", 2)
    root, git = _open_repository(arguments.repo)
    sensitivity = getattr(arguments, "sensitivity", "internal")
    repository, warnings = _repository_metadata(root, git, sensitivity)
    history, reached_limit = _parse_history(
        git,
        since=arguments.since,
        until=arguments.until,
        max_commits=arguments.max_commits,
        include_merges=getattr(arguments, "include_merges", True),
        paths=getattr(arguments, "path", []),
    )
    if reached_limit:
        warnings.append(
            {
                "category": "commit_limit_reached",
                "source_id": "scope",
                "detail": (
                    f"history scan limited to {arguments.max_commits} candidate commits; "
                    "narrow the date/path scope or raise --max-commits"
                ),
            }
        )

    if arguments.command == "contributors":
        contributors = _contributors(history, sensitivity)
        selected: list[dict[str, Any]] = []
    else:
        authors = sorted(set(arguments.author), key=str.casefold)
        paths = sorted(set(arguments.path), key=str.casefold)
        selected = []
        for commit in history:
            if not arguments.include_merges and len(commit["parents"]) > 1:
                continue
            if not _matches_author(commit, authors):
                continue
            files = _commit_files(git, commit)
            if not _matches_paths(files, paths):
                continue
            commit["files"] = files
            selected.append(commit)
        contributors = _contributors(selected, sensitivity)

    selected.sort(key=lambda item: (_format_time(datetime.fromisoformat(item["authored_at"].replace("Z", "+00:00"))), item["sha"]))
    commit_documents: list[dict[str, Any]] = []
    file_changes: list[dict[str, Any]] = []
    pending_evidence: list[dict[str, Any]] = []
    for commit in selected:
        title = commit["message"].splitlines()[0] if commit["message"].splitlines() else ""
        title, redactions = _redact_text(title)
        for category in redactions:
            warnings.append({"code": "secret_redacted", "evidence_ids": [], "message": f"commit title: {category}"})
        author = _display_identity(commit["author_name"], commit["author_email"], sensitivity)
        committer = _display_identity(commit["committer_name"], commit["committer_email"], sensitivity)
        coauthors = _coauthors(commit["message"], sensitivity)
        suspected_proxy = (
            commit["author_name"].casefold() != commit["committer_name"].casefold()
            or _normalize_email(commit["author_email"]) != _normalize_email(commit["committer_email"])
        )
        file_change_ids: list[str] = []
        for change in commit["files"]:
            file_change_id = f"FC-{len(file_changes) + 1:06d}"
            file_change_ids.append(file_change_id)
            file_changes.append(
                {
                    "file_change_id": file_change_id,
                    "commit_id": commit["sha"],
                    "path": change["path"],
                    "old_path": change["old_path"],
                    "status": change["status"],
                    "additions": change["additions"],
                    "deletions": change["deletions"],
                    "binary": change["binary"],
                    "generated": change["skipped_reason"] == "generated",
                    "size_bytes": change["size_bytes"],
                    "skipped_reason": change["skipped_reason"].replace("-", "_") if change["skipped_reason"] else None,
                }
            )
        commit_documents.append(
            {
                "commit_id": commit["sha"],
                "parents": commit["parents"],
                "author": author,
                "committer": committer,
                "authored_at_utc": _format_time(datetime.fromisoformat(commit["authored_at"].replace("Z", "+00:00"))),
                "title": title,
                "is_merge": len(commit["parents"]) > 1,
                "coauthors": coauthors,
                "suspected_proxy": suspected_proxy,
                "squash_clue": bool(re.search(r"(?i)\b(?:squash(?:ed)?|fixup!)\b", title)),
                "file_change_ids": file_change_ids,
            }
        )
        pending_evidence.append(
            {
                "kind": "commit",
                "repository": repository["name"],
                "path": None,
                "symbol": None,
                "line_start": None,
                "line_end": None,
                "commit": commit["sha"],
                "authors": [author, *coauthors],
                "observed_fact": f"Commit changed {len(commit['files'])} tracked file(s).",
                "supports": ["implementation", "ownership"],
                "confidence": "high",
                "attribution_basis": "git",
                "sensitivity": sensitivity,
            }
        )

    pending_evidence.sort(
        key=lambda item: (
            item["kind"], item["commit"] or "", item["path"] or "",
            item["line_start"] if item["line_start"] is not None else -1, item["observed_fact"],
        )
    )
    evidence = [dict(item, evidence_id=f"E-{index:06d}") for index, item in enumerate(pending_evidence, 1)]
    scope, scope_warnings = _scope(arguments)
    warnings.extend(scope_warnings)
    normalized_warnings: list[dict[str, Any]] = []
    for warning in warnings:
        if "code" in warning:
            normalized_warnings.append(warning)
        else:
            normalized_warnings.append(
                {"code": warning["category"], "evidence_ids": [], "message": warning["detail"]}
            )
    document = {
        "artifact_type": "evidence_report",
        "schema_version": SCHEMA_VERSION,
        "generated_at": _format_time(datetime.now(timezone.utc)),
        "tool": {"name": "collect_git_evidence", "version": _tool_version()},
        "repository": repository,
        "scope": scope,
        "contributors": contributors,
        "commits": commit_documents,
        "file_changes": file_changes,
        "evidence": evidence,
        "chains": [],
        "work_items": [],
        "conflicts": [],
        "questions": [],
        "warnings": normalized_warnings,
        "search_terms": [],
    }
    sanitized, output_redactions = _sanitize_output(document, sensitivity)
    sanitized["warnings"].extend(
        {"code": "secret_redacted", "evidence_ids": [], "message": f"report value: {category}"}
        for category in output_redactions
        if not any(
            warning["code"] == "secret_redacted" and warning["message"].endswith(category)
            for warning in sanitized["warnings"]
        )
    )
    sanitized["warnings"].sort(
        key=lambda item: (item["code"], item["evidence_ids"][0] if item["evidence_ids"] else "", item["message"])
    )
    return sanitized


def _serialize(document: dict[str, Any], pretty: bool) -> str:
    if pretty:
        return json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    return json.dumps(document, ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n"


def _write_output(value: str, destination: str) -> None:
    if destination == "-":
        try:
            sys.stdout.write(value)
            sys.stdout.flush()
        except (OSError, UnicodeError) as error:
            raise CollectorError(f"output could not be written: {error}", 5) from error
        return
    target = Path(destination).expanduser().resolve()
    if not target.parent.is_dir():
        raise CollectorError("output parent directory does not exist", 5)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=target.parent,
            prefix=f".{target.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary.write(value)
            temporary.flush()
            os.fsync(temporary.fileno())
            temporary_path = Path(temporary.name)
        os.replace(temporary_path, target)
    except (OSError, UnicodeError) as error:
        if temporary_path is not None:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError:
                pass
        raise CollectorError(f"output could not be written: {error}", 5) from error


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    try:
        arguments = parser.parse_args(argv)
        document = _collect(arguments)
        _write_output(_serialize(document, arguments.pretty), arguments.output)
        return 0
    except CollectorError as error:
        print(f"error: {error}", file=sys.stderr)
        return error.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
