#!/usr/bin/env python3
"""Audit retained historical evidence and classify evidence-loss cases.

The audit verifies relative evidence copies against both their recorded SHA-256
and the named Git commit. A disposed record is structural evidence only: this
tool does not authenticate its author or accept a lifecycle disposition.
"""

from __future__ import annotations

import argparse
import contextlib
import copy
import hashlib
import io
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

AUDIT_SCHEMA = "mori-evidence-loss-audit-v1"
CLASSIFICATION_SCHEMA = "mori-evidence-loss-classification-v1"
SELFTEST_SCHEMA = "mori-evidence-loss-selftest-v1"
REQUIRED_SCHEMA = "mori-required-observations-v1"
ACCOUNTING_SCHEMA = "mori-loss-accounting-v1"
RULE_SCHEMA = "mori-evidence-loss-rule-v1"
CASES_SCHEMA = "mori-evidence-loss-cases-v1"
ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")
REVISION_RE = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
ALLOWED_CLASSES = {"census-regression", "live-state"}
ALLOWED_DISPOSITIONS = {"settlement", "cleanup-accounted"}
NOFOLLOW = getattr(os, "O_NOFOLLOW", 0)
CLOEXEC = getattr(os, "O_CLOEXEC", 0)
DIRECTORY = getattr(os, "O_DIRECTORY", 0)
NONBLOCK = getattr(os, "O_NONBLOCK", 0)


class SetupError(Exception):
    """An invalid CLI input or unavailable audit prerequisite."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


class PathProblem(Exception):
    """A safe path could not be opened without following symlinks."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def _emit(value: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n")


def _reject_constant(_value: str) -> None:
    raise ValueError("non-json-number")


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate-json-key")
        result[key] = value
    return result


def _open_directory_absolute(path: str) -> int:
    if type(path) is not str or not path or "\0" in path:
        raise PathProblem("unsafe_path")
    absolute = path if os.path.isabs(path) else os.path.join(os.getcwd(), path)
    components = absolute.split(os.sep)
    if NOFOLLOW == 0 or DIRECTORY == 0:
        raise PathProblem("safe_open_unavailable")
    fd = os.open(os.sep, os.O_RDONLY | DIRECTORY | CLOEXEC)
    try:
        for component in components:
            if component in ("", "."):
                continue
            if component == "..":
                raise PathProblem("unsafe_path")
            next_fd = os.open(component, os.O_RDONLY | DIRECTORY | NOFOLLOW | CLOEXEC, dir_fd=fd)
            os.close(fd)
            fd = next_fd
        if not stat.S_ISDIR(os.fstat(fd).st_mode):
            raise PathProblem("unsafe_path")
        return fd
    except BaseException:
        os.close(fd)
        raise


def _open_absolute_regular(path: str) -> int:
    if type(path) is not str or not path or "\0" in path:
        raise PathProblem("unsafe_path")
    absolute = path if os.path.isabs(path) else os.path.join(os.getcwd(), path)
    components = absolute.split(os.sep)
    if len(components) < 2 or components[-1] in ("", ".", ".."):
        raise PathProblem("unsafe_path")
    if NOFOLLOW == 0 or DIRECTORY == 0:
        raise PathProblem("safe_open_unavailable")
    fd = os.open(os.sep, os.O_RDONLY | DIRECTORY | CLOEXEC)
    file_fd: int | None = None
    try:
        for component in components[1:-1]:
            if component in ("", "."):
                continue
            if component == "..":
                raise PathProblem("unsafe_path")
            next_fd = os.open(component, os.O_RDONLY | DIRECTORY | NOFOLLOW | CLOEXEC, dir_fd=fd)
            os.close(fd)
            fd = next_fd
        final_name = components[-1]
        before = os.stat(final_name, dir_fd=fd, follow_symlinks=False)
        if not stat.S_ISREG(before.st_mode):
            raise PathProblem("unsafe_path")
        file_fd = os.open(final_name, os.O_RDONLY | NOFOLLOW | CLOEXEC | NONBLOCK, dir_fd=fd)
        after = os.fstat(file_fd)
        if not stat.S_ISREG(after.st_mode) or (before.st_dev, before.st_ino) != (after.st_dev, after.st_ino):
            raise PathProblem("unsafe_path")
        os.close(fd)
        fd = -1
        return file_fd
    except BaseException:
        if file_fd is not None:
            os.close(file_fd)
        if fd >= 0:
            os.close(fd)
        raise


def _read_fd(fd: int) -> bytes:
    chunks: list[bytes] = []
    while True:
        block = os.read(fd, 131072)
        if not block:
            return b"".join(chunks)
        chunks.append(block)


def _read_cli_json(path: str) -> Any:
    try:
        fd = _open_absolute_regular(path)
    except FileNotFoundError:
        raise SetupError("input_missing") from None
    except PathProblem as exc:
        raise SetupError(exc.code) from None
    except OSError as exc:
        raise SetupError("input_missing" if exc.errno == 2 else "unsafe_input_path") from None
    try:
        raw = _read_fd(fd)
    except OSError:
        raise SetupError("input_read_failed") from None
    finally:
        os.close(fd)
    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object, parse_constant=_reject_constant)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
        raise SetupError("invalid_json") from None


def _safe_relative_parts(value: Any) -> tuple[str, ...] | None:
    if type(value) is not str or not value or "\0" in value or "\\" in value or value.startswith("/"):
        return None
    if any(ord(char) < 32 or ord(char) == 127 for char in value):
        return None
    parts = tuple(value.split("/"))
    if any(part in ("", ".", "..") for part in parts):
        return None
    return parts


def _read_root_relative(root_fd: int, parts: tuple[str, ...], include_bytes: bool = False) -> tuple[str, bytes | None]:
    if NOFOLLOW == 0 or DIRECTORY == 0:
        raise PathProblem("safe_open_unavailable")
    parent_fd = os.dup(root_fd)
    try:
        for component in parts[:-1]:
            info = os.stat(component, dir_fd=parent_fd, follow_symlinks=False)
            if stat.S_ISLNK(info.st_mode):
                raise PathProblem("unsafe_symlink")
            if not stat.S_ISDIR(info.st_mode):
                raise PathProblem("unsafe_path")
            next_fd = os.open(component, os.O_RDONLY | DIRECTORY | NOFOLLOW | CLOEXEC, dir_fd=parent_fd)
            os.close(parent_fd)
            parent_fd = next_fd
        final_name = parts[-1]
        before = os.stat(final_name, dir_fd=parent_fd, follow_symlinks=False)
        if stat.S_ISLNK(before.st_mode):
            raise PathProblem("unsafe_symlink")
        if not stat.S_ISREG(before.st_mode):
            raise PathProblem("unsafe_path")
        file_fd = os.open(final_name, os.O_RDONLY | NOFOLLOW | CLOEXEC | NONBLOCK, dir_fd=parent_fd)
        try:
            after = os.fstat(file_fd)
            if not stat.S_ISREG(after.st_mode) or (before.st_dev, before.st_ino) != (after.st_dev, after.st_ino):
                raise PathProblem("unsafe_path")
            digest = hashlib.sha256()
            data_chunks: list[bytes] | None = [] if include_bytes else None
            while True:
                block = os.read(file_fd, 131072)
                if not block:
                    break
                digest.update(block)
                if data_chunks is not None:
                    data_chunks.append(block)
            final = os.fstat(file_fd)
            if (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns) != (
                final.st_dev, final.st_ino, final.st_size, final.st_mtime_ns, final.st_ctime_ns
            ):
                raise PathProblem("evidence_changed")
            data = b"".join(data_chunks) if data_chunks is not None else None
            return digest.hexdigest(), data
        finally:
            os.close(file_fd)
    finally:
        os.close(parent_fd)


def _git(root: str, args: list[str], input_bytes: bytes | None = None) -> bytes:
    env = {
        "PATH": os.defpath,
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_NO_REPLACE_OBJECTS": "1",
        "GIT_PAGER": "cat",
        "LANG": "C",
    }
    try:
        result = subprocess.run(
            ["git", "-C", root, *args],
            input=input_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=30,
            env=env,
        )
    except FileNotFoundError:
        raise SetupError("git_unavailable") from None
    except subprocess.TimeoutExpired:
        raise SetupError("git_timeout") from None
    except OSError:
        raise SetupError("git_unavailable") from None
    if result.returncode != 0:
        raise SetupError("git_read_failed")
    return result.stdout


class GitEvidence:
    """Read-only lookup of evidence blobs in named committed revisions."""

    def __init__(self, root: str):
        self.root = root
        try:
            prefix_raw = _git(root, ["rev-parse", "--show-prefix"])
            self.prefix = prefix_raw.decode("utf-8").strip("\n")
        except UnicodeDecodeError:
            raise SetupError("git_root_invalid") from None
        if self.prefix and _safe_relative_parts(self.prefix.rstrip("/")) is None:
            raise SetupError("git_root_invalid")
        self.commits: dict[str, bool] = {}
        self.trees: dict[str, dict[bytes, tuple[bytes, bytes, bytes]]] = {}

    def _load_tree(self, revision: str) -> dict[bytes, tuple[bytes, bytes, bytes]] | None:
        if revision in self.trees:
            return self.trees[revision]
        if revision not in self.commits:
            try:
                kind = _git(self.root, ["cat-file", "-t", revision]).strip()
            except SetupError:
                self.commits[revision] = False
            else:
                self.commits[revision] = kind == b"commit"
        if not self.commits[revision]:
            return None
        try:
            raw = _git(self.root, ["ls-tree", "-r", "-z", "--full-tree", revision])
        except SetupError:
            self.commits[revision] = False
            return None
        tree: dict[bytes, tuple[bytes, bytes, bytes]] = {}
        try:
            for entry in raw.split(b"\0"):
                if not entry:
                    continue
                metadata, path_bytes = entry.split(b"\t", 1)
                mode, kind, object_id = metadata.split()
                tree[path_bytes] = (mode, kind, object_id)
        except ValueError:
            self.commits[revision] = False
            return None
        self.trees[revision] = tree
        return tree

    def verify(self, revision: str, path_parts: tuple[str, ...], expected_sha256: str) -> str | None:
        tree = self._load_tree(revision)
        if tree is None:
            return "revision_unavailable"
        repo_path = "/".join(part for part in (self.prefix.rstrip("/"), "/".join(path_parts)) if part)
        try:
            path_bytes = repo_path.encode("utf-8")
        except UnicodeEncodeError:
            return "revision_path_missing"
        entry = tree.get(path_bytes)
        if entry is None:
            return "revision_path_missing"
        mode, kind, object_id = entry
        if kind != b"blob" or mode not in (b"100644", b"100755"):
            return "revision_path_not_regular"
        try:
            blob = _git(self.root, ["cat-file", "blob", object_id.decode("ascii")])
        except (SetupError, UnicodeDecodeError):
            return "revision_blob_unavailable"
        if hashlib.sha256(blob).hexdigest() != expected_sha256:
            return "revision_hash_mismatch"
        return None


def _valid_id(value: Any) -> bool:
    return type(value) is str and ID_RE.fullmatch(value) is not None


def _require_keys(value: Any, required: set[str], allowed: set[str] | None = None) -> dict[str, Any]:
    if type(value) is not dict:
        raise SetupError("invalid_schema")
    keys = set(value)
    if not required.issubset(keys) or (allowed is not None and not keys.issubset(allowed)):
        raise SetupError("invalid_schema")
    return value


def _load_required(path: str) -> list[dict[str, Any]]:
    doc = _require_keys(_read_cli_json(path), {"schema", "observations"}, {"schema", "observations"})
    if doc["schema"] != REQUIRED_SCHEMA or type(doc["observations"]) is not list or not doc["observations"]:
        raise SetupError("invalid_required_schema")
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in doc["observations"]:
        item = _require_keys(row, {"id", "baseline", "evidence"}, {"id", "baseline", "evidence"})
        if not _valid_id(item["id"]):
            raise SetupError("invalid_observation_id")
        if item["id"] in seen:
            raise SetupError("duplicate_observation_id")
        if type(item["evidence"]) is not str or not item["evidence"].strip():
            raise SetupError("invalid_required_evidence")
        cite_path, separator, line = item["evidence"].rpartition(":")
        if not separator or not line.isdigit() or not line or int(line) < 1 or _safe_relative_parts(cite_path) is None:
            raise SetupError("invalid_required_evidence")
        seen.add(item["id"])
        rows.append(item)
    return rows


def _load_accounting(path: str) -> list[dict[str, Any]]:
    doc = _require_keys(_read_cli_json(path), {"schema", "observations"}, {"schema", "observations"})
    if doc["schema"] != ACCOUNTING_SCHEMA or type(doc["observations"]) is not list:
        raise SetupError("invalid_accounting_schema")
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    expected = {"id", "state", "baseline", "deletion", "cleanup", "independent_disposition"}
    for row in doc["observations"]:
        item = _require_keys(row, expected, expected)
        if not _valid_id(item["id"]):
            raise SetupError("invalid_observation_id")
        if item["id"] in seen:
            raise SetupError("duplicate_observation_id")
        if type(item["state"]) is not str:
            raise SetupError("invalid_accounting_state")
        seen.add(item["id"])
        rows.append(item)
    return rows



def _check_reference(
    root_fd: int,
    git: GitEvidence,
    value: Any,
    observation_id: str,
    field: str,
    add_issue,
    allow_actor: bool = False,
    include_bytes: bool = False,
    allow_disposition_metadata: bool = False,
) -> tuple[str | None, bytes | None, str | None]:
    if type(value) is not dict:
        add_issue(observation_id, field, "malformed_reference")
        return None, None, None
    required = {"path", "revision", "sha256"}
    allowed = required | ({"actor"} if allow_actor else set())
    if allow_disposition_metadata:
        allowed |= {"independent", "actor", "wave_id", "disposition"}
    if not required.issubset(value) or not set(value).issubset(allowed):
        add_issue(observation_id, field, "malformed_reference")
        return None, None, None
    raw_path = value.get("path")
    parts = _safe_relative_parts(raw_path)
    if parts is None:
        add_issue(observation_id, field, "unsafe_path")
    revision_raw = value.get("revision")
    revision = revision_raw if type(revision_raw) is str and REVISION_RE.fullmatch(revision_raw) else None
    if revision is None:
        add_issue(observation_id, field, "revision_invalid")
    digest_raw = value.get("sha256")
    digest = digest_raw if type(digest_raw) is str and SHA256_RE.fullmatch(digest_raw) else None
    if digest is None:
        add_issue(observation_id, field, "hash_invalid")
    actor: str | None = None
    if allow_actor and "actor" in value:
        raw_actor = value["actor"]
        if type(raw_actor) is str and raw_actor.strip() == raw_actor and raw_actor and not any(ord(ch) < 32 for ch in raw_actor):
            actor = raw_actor
        else:
            add_issue(observation_id, field, "actor_invalid")
    data: bytes | None = None
    if parts is not None and digest is not None:
        try:
            actual, data = _read_root_relative(root_fd, parts, include_bytes=include_bytes)
        except FileNotFoundError:
            add_issue(observation_id, field, "evidence_missing")
        except PathProblem as exc:
            add_issue(observation_id, field, exc.code)
        except OSError as exc:
            add_issue(observation_id, field, "evidence_missing" if exc.errno == 2 else "evidence_unavailable")
        else:
            if actual != digest:
                add_issue(observation_id, field, "hash_mismatch")
                data = None
            elif revision is not None:
                git_problem = git.verify(revision, parts, digest)
                if git_problem is not None:
                    add_issue(observation_id, field, git_problem)
                    data = None
    else:
        data = None
    return revision, data, actor


def _finding_id(observation_id: str, code: str) -> str:
    return f"mori-evidence-loss:audit:{observation_id}:{code}"


def _disposition_record_matches(data: bytes | None, observation_id: str, actor: str, wave_id: str, disposition: str) -> bool:
    if data is None:
        return False
    try:
        value = json.loads(data.decode("utf-8"), object_pairs_hook=_unique_object, parse_constant=_reject_constant)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
        return False
    if type(value) is not dict or not {"id", "actor", "wave_id", "disposition", "independent"}.issubset(value):
        return False
    return (
        value.get("id") == observation_id
        and type(value.get("actor")) is str
        and value.get("actor") == actor
        and type(value.get("wave_id")) is str
        and value.get("wave_id") == wave_id
        and type(value.get("disposition")) is str
        and value.get("disposition") == disposition
        and type(value.get("independent")) is bool
        and value.get("independent") is True
    )


def audit(root: str, required_path: str, accounting_path: str) -> tuple[dict[str, Any], int]:
    required_rows = _load_required(required_path)
    accounting_rows = _load_accounting(accounting_path)
    try:
        root_fd = _open_directory_absolute(root)
    except FileNotFoundError:
        raise SetupError("root_missing") from None
    except PathProblem as exc:
        raise SetupError(exc.code) from None
    except OSError as exc:
        raise SetupError("root_missing" if exc.errno == 2 else "unsafe_root") from None
    try:
        root_abs = root if os.path.isabs(root) else os.path.join(os.getcwd(), root)
        git = GitEvidence(root_abs)
        required_by_id = {row["id"]: row for row in required_rows}
        accounting_by_id = {row["id"]: row for row in accounting_rows}
        issues: list[dict[str, str]] = []
        issue_keys: set[tuple[str, str, str]] = set()
        invalid_ids: set[str] = set()

        def add_issue(observation_id: str, field: str, reason: str, invalid: bool = True) -> None:
            key = (observation_id, field, reason)
            if key in issue_keys:
                return
            issue_keys.add(key)
            if invalid:
                invalid_ids.add(observation_id)
            issues.append({
                "id": observation_id,
                "finding_id": _finding_id(observation_id, f"{field}:{reason}"),
                "field": field,
                "reason": reason,
            })

        omitted: list[dict[str, str]] = []
        retained: list[dict[str, str]] = []
        unresolved: list[dict[str, str]] = []
        disposed: list[dict[str, Any]] = []
        for observation_id in sorted(required_by_id):
            row_issue_start = len(issues)
            required = required_by_id[observation_id]
            _check_reference(root_fd, git, required.get("baseline"), observation_id, "required.baseline", add_issue)
            accounting = accounting_by_id.get(observation_id)
            if accounting is None:
                missing = {"id": observation_id, "finding_id": _finding_id(observation_id, "omitted")}
                omitted.append(missing)
                add_issue(observation_id, "accounting", "omitted", invalid=False)
                continue
            state = accounting["state"]
            retained.append({
                "id": observation_id,
                "state": state,
                "finding_id": _finding_id(observation_id, "retained"),
            })
            required_baseline = required.get("baseline")
            account_baseline = accounting.get("baseline")
            required_identity = tuple(required_baseline.get(key) for key in ("path", "revision", "sha256")) if type(required_baseline) is dict else None
            account_identity = tuple(account_baseline.get(key) for key in ("path", "revision", "sha256")) if type(account_baseline) is dict else None
            if required_identity is None or account_identity != required_identity:
                add_issue(observation_id, "baseline", "baseline_mismatch")
            _check_reference(root_fd, git, account_baseline, observation_id, "baseline", add_issue)
            _check_reference(root_fd, git, accounting.get("deletion"), observation_id, "deletion", add_issue)
            _check_reference(root_fd, git, accounting.get("cleanup"), observation_id, "cleanup", add_issue, allow_actor=True)
            cleanup_actor = accounting.get("cleanup", {}).get("actor") if type(accounting.get("cleanup")) is dict else None
            if state == "unresolved":
                unresolved.append({"id": observation_id, "finding_id": _finding_id(observation_id, "unresolved"), "reason": "unresolved"})
                add_issue(observation_id, "disposition", "unresolved", invalid=False)
                if accounting.get("independent_disposition") is not None:
                    add_issue(observation_id, "independent_disposition", "unexpected_disposition_for_unresolved")
            elif state == "disposed":
                disposition = accounting.get("independent_disposition")
                if type(disposition) is not dict:
                    add_issue(observation_id, "independent_disposition", "disposition_missing")
                else:
                    required_disposition = {"path", "revision", "sha256", "independent", "actor", "wave_id", "disposition"}
                    if set(disposition) != required_disposition:
                        add_issue(observation_id, "independent_disposition", "malformed_disposition")
                    independent = disposition.get("independent")
                    if type(independent) is not bool or independent is not True:
                        add_issue(observation_id, "independent_disposition", "independent_flag_invalid")
                    actor = disposition.get("actor")
                    if type(actor) is not str or not actor or actor != actor.strip() or any(ord(ch) < 32 for ch in actor):
                        add_issue(observation_id, "independent_disposition", "actor_invalid")
                        actor = None
                    wave_id = disposition.get("wave_id")
                    if not _valid_id(wave_id):
                        add_issue(observation_id, "independent_disposition", "wave_id_invalid")
                        wave_id = None
                    disposition_kind = disposition.get("disposition")
                    if type(disposition_kind) is not str or disposition_kind not in ALLOWED_DISPOSITIONS:
                        add_issue(observation_id, "independent_disposition", "disposition_invalid")
                        disposition_kind = None
                    _, disposition_bytes, _ = _check_reference(
                        root_fd, git, disposition, observation_id, "independent_disposition", add_issue,
                        include_bytes=True, allow_disposition_metadata=True,
                    )
                    if cleanup_actor is None:
                        add_issue(observation_id, "cleanup", "cleanup_actor_missing")
                    elif actor is not None and actor == cleanup_actor:
                        add_issue(observation_id, "independent_disposition", "independent_actor_not_distinct")
                    if actor is not None and wave_id is not None and disposition_kind is not None:
                        if not _disposition_record_matches(disposition_bytes, observation_id, actor, wave_id, disposition_kind):
                            add_issue(observation_id, "independent_disposition", "disposition_record_mismatch")
                    row_issues = [item for item in issues[row_issue_start:] if item["id"] == observation_id]
                    if not row_issues:
                        disposed.append({
                            "id": observation_id,
                            "finding_id": _finding_id(observation_id, "disposed"),
                            "wave_id": wave_id,
                            "disposition": disposition_kind,
                            "status": "structural_only",
                            "trust_basis": "declared-record-not-authenticated",
                        })
                        unresolved.append({
                            "id": observation_id,
                            "finding_id": _finding_id(observation_id, "external_review_required"),
                            "reason": "external_review_required",
                        })
                        add_issue(observation_id, "disposition", "external_review_required", invalid=False)
                    else:
                        unresolved.append({
                            "id": observation_id,
                            "finding_id": _finding_id(observation_id, "disposition_invalid"),
                            "reason": "disposition_invalid",
                        })
            else:
                add_issue(observation_id, "state", "unknown_state")
        for observation_id in sorted(set(accounting_by_id) - set(required_by_id)):
            add_issue(observation_id, "accounting", "not_required")
        issues.sort(key=lambda item: (item["id"], item["field"], item["reason"]))
        invalid = [
            {"id": observation_id, "finding_id": _finding_id(observation_id, "invalid")}
            for observation_id in sorted(invalid_ids)
        ]
        # This observer has no authenticated outside-acceptance input. It
        # reports retention and uncertainty, never grants pin authority.
        pin_allowed = False
        payload = {
            "schema": AUDIT_SCHEMA,
            "omitted": len(omitted),
            "omitted_ids": omitted,
            "retained": len(retained),
            "retained_ids": retained,
            "unresolved": len(unresolved),
            "unresolved_ids": unresolved,
            "disposed": len(disposed),
            "disposed_ids": disposed,
            "invalid": len(invalid),
            "invalid_ids": invalid,
            "issues": issues,
            "pin_allowed": pin_allowed,
            "trust_basis": "declared-record-not-authenticated",
        }
        return payload, 1
    finally:
        os.close(root_fd)


def _load_rule(path: str) -> dict[str, Any]:
    rule = _require_keys(_read_cli_json(path), {"schema", "evidence_loss_blocks"}, {"schema", "evidence_loss_blocks", "source", "interpretation"})
    if rule["schema"] != RULE_SCHEMA or type(rule["evidence_loss_blocks"]) is not bool:
        raise SetupError("invalid_rule_schema")
    for key in ("source", "interpretation"):
        if key in rule and type(rule[key]) is not str:
            raise SetupError("invalid_rule_schema")
    return rule


def _load_cases(path: str) -> list[dict[str, Any]]:
    doc = _require_keys(_read_cli_json(path), {"schema", "cases"}, {"schema", "cases"})
    if doc["schema"] != CASES_SCHEMA or type(doc["cases"]) is not list or not doc["cases"]:
        raise SetupError("invalid_cases_schema")
    expected = {
        "id", "required_evidence_lost", "independent_disposition", "ordinary_state_change",
        "expected_class", "expected_pin_allowed",
    }
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for case in doc["cases"]:
        item = _require_keys(case, expected, expected)
        if not _valid_id(item["id"]):
            raise SetupError("invalid_case_id")
        if item["id"] in seen:
            raise SetupError("duplicate_case_id")
        for name in ("required_evidence_lost", "independent_disposition", "ordinary_state_change", "expected_pin_allowed"):
            if type(item[name]) is not bool:
                raise SetupError("invalid_case_boolean")
        if type(item["expected_class"]) is not str or item["expected_class"] not in ALLOWED_CLASSES:
            raise SetupError("invalid_expected_class")
        seen.add(item["id"])
        rows.append(item)
    return rows


def classify(rule_path: str, cases_path: str) -> tuple[dict[str, Any], int]:
    rule = _load_rule(rule_path)
    cases = _load_cases(cases_path)
    decisions: list[dict[str, Any]] = []
    mismatched = 0
    for case in sorted(cases, key=lambda item: item["id"]):
        if rule["evidence_loss_blocks"] and case["required_evidence_lost"] and not case["independent_disposition"]:
            observed_class = "census-regression"
            observed_pin_allowed = False
        else:
            observed_class = "live-state"
            observed_pin_allowed = True
        matched = (
            observed_class == case["expected_class"]
            and observed_pin_allowed is case["expected_pin_allowed"]
        )
        if not matched:
            mismatched += 1
        decisions.append({
            "id": case["id"],
            "finding_id": f"mori-evidence-loss:classify:{case['id']}",
            "observed_class": observed_class,
            "observed_pin_allowed": observed_pin_allowed,
            "expected_class": case["expected_class"],
            "expected_pin_allowed": case["expected_pin_allowed"],
            "matched": matched,
        })
    result = {
        "schema": CLASSIFICATION_SCHEMA,
        "rule": {"evidence_loss_blocks": rule["evidence_loss_blocks"]},
        "rule_source": rule.get("source"),
        "cases": decisions,
        "mismatched": mismatched,
        "matched": mismatched == 0,
        "finding_id": "mori-evidence-loss:classify:result",
        "trust_basis": "caller-declared-synthetic-case",
        "decision_scope": "synthetic policy comparison only; not pin authorization or lifecycle acceptance",
    }
    return result, 0 if mismatched == 0 else 1


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")


def _run_fixture_git(root: Path) -> str:
    env = {
        "PATH": os.defpath,
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_PAGER": "cat",
        "LANG": "C",
    }
    commands = [
        ["git", "-C", str(root), "init", "--quiet"],
        ["git", "-C", str(root), "add", "--", "evidence"],
        ["git", "-C", str(root), "-c", "user.name=Mori Evidence Selftest", "-c", "user.email=mori-selftest@example.invalid", "commit", "--quiet", "-m", "fixture"],
        ["git", "-C", str(root), "rev-parse", "HEAD"],
    ]
    for command in commands:
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False, timeout=30, env=env)
        except (OSError, subprocess.TimeoutExpired):
            raise RuntimeError("selftest_git_unavailable") from None
        if result.returncode != 0:
            raise RuntimeError("selftest_git_failed")
    revision = result.stdout.decode("ascii", errors="strict").strip()
    if REVISION_RE.fullmatch(revision) is None:
        raise RuntimeError("selftest_revision_invalid")
    return revision


def _selftest() -> int:
    checks = 0
    failures: list[str] = []

    def check(name: str, condition: bool) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            failures.append(name)

    def has_finding(value: Any, expected: str) -> bool:
        if type(value) is dict:
            if value.get("finding_id") == expected:
                return True
            return any(has_finding(item, expected) for item in value.values())
        if type(value) is list:
            return any(has_finding(item, expected) for item in value)
        return False

    def cli_case(
        name: str,
        rc: int,
        payload: dict[str, Any] | None,
        stderr: str,
        expected_rc: int,
        expected_finding_id: str,
        predicate=None,
    ) -> None:
        check(f"{name}_rc", rc == expected_rc)
        check(f"{name}_finding_id", payload is not None and has_finding(payload, expected_finding_id))
        check(f"{name}_stderr_empty", stderr == "")
        if predicate is not None:
            check(f"{name}_result", payload is not None and predicate(payload))

    scratch_root = os.environ.get("TMPDIR")
    try:
        if not scratch_root:
            raise OSError("TMPDIR is required for isolated selftest fixtures")
        temporary = tempfile.TemporaryDirectory(prefix=".mori-evidence-loss-selftest-", dir=scratch_root)
    except OSError:
        _emit({
            "schema": SELFTEST_SCHEMA,
            "passed": False,
            "checks": 0,
            "failures": ["fixture_directory"],
            "finding_id": "mori-evidence-loss:setup:selftest_fixture_directory",
        })
        return 1
    with temporary as temp_name:
        fixture = Path(temp_name)
        root = fixture / "repo"
        evidence_dir = root / "evidence"
        evidence_dir.mkdir(parents=True)
        files = {
            "baseline.txt": b"frozen baseline evidence\n",
            "deletion.txt": b"deletion provenance\n",
            "cleanup.txt": b"cleanup provenance\n",
            "disposition.json": b'{"actor":"reviewer","disposition":"settlement","id":"aggregator-r10","independent":true,"wave_id":"round-10"}\n',
        }
        for name, data in files.items():
            (evidence_dir / name).write_bytes(data)
        try:
            revision = _run_fixture_git(root)
        except RuntimeError:
            _emit({
                "schema": SELFTEST_SCHEMA,
                "passed": False,
                "checks": 0,
                "failures": ["fixture_git"],
                "finding_id": "mori-evidence-loss:setup:selftest_fixture_git",
            })
            return 1

        def ref(name: str, actor: str | None = None) -> dict[str, str]:
            data = (evidence_dir / name).read_bytes()
            value = {
                "path": f"evidence/{name}",
                "revision": revision,
                "sha256": hashlib.sha256(data).hexdigest(),
            }
            if actor is not None:
                value["actor"] = actor
            return value

        required = {
            "schema": REQUIRED_SCHEMA,
            "observations": [{
                "id": "aggregator-r10",
                "baseline": ref("baseline.txt"),
                "evidence": "history/round-10.md:7",
            }],
        }
        unresolved_row = {
            "id": "aggregator-r10",
            "state": "unresolved",
            "baseline": ref("baseline.txt"),
            "deletion": ref("deletion.txt"),
            "cleanup": ref("cleanup.txt", "cleaner"),
            "independent_disposition": None,
        }
        required_path = fixture / "required.json"
        accounting_path = fixture / "accounting.json"
        _write_json(required_path, required)
        _write_json(accounting_path, {"schema": ACCOUNTING_SCHEMA, "observations": [unresolved_row]})

        def invoke(args: list[str]) -> tuple[int, dict[str, Any] | None, str]:
            stdout = io.StringIO()
            stderr = io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                rc = main(args)
            try:
                payload = json.loads(stdout.getvalue())
            except (json.JSONDecodeError, ValueError):
                payload = None
            return rc, payload if type(payload) is dict else None, stderr.getvalue()

        audit_args = ["audit", "--root", str(root), "--required", str(required_path), "--accounting", str(accounting_path)]
        rc, payload, stderr = invoke(audit_args)
        cli_case(
            "unresolved",
            rc,
            payload,
            stderr,
            1,
            "mori-evidence-loss:audit:aggregator-r10:unresolved",
            lambda item: item.get("omitted") == 0 and item.get("retained") == 1
            and item.get("unresolved") == 1 and item.get("disposed") == 0
            and item.get("invalid") == 0 and item.get("pin_allowed") is False,
        )
        rc_repeat, payload_repeat, stderr_repeat = invoke(audit_args)
        cli_case(
            "unresolved_repeat",
            rc_repeat,
            payload_repeat,
            stderr_repeat,
            1,
            "mori-evidence-loss:audit:aggregator-r10:unresolved",
        )

        _write_json(accounting_path, {"schema": ACCOUNTING_SCHEMA, "observations": []})
        rc, payload, stderr = invoke(audit_args)
        cli_case(
            "empty_accounting",
            rc,
            payload,
            stderr,
            1,
            "mori-evidence-loss:audit:aggregator-r10:accounting:omitted",
            lambda item: item.get("omitted") == 1 and item.get("retained") == 0
            and item.get("unresolved") == 0 and item.get("invalid") == 0
            and item.get("pin_allowed") is False,
        )

        absent = copy.deepcopy(unresolved_row)
        absent["cleanup"]["path"] = "evidence/absent.txt"
        _write_json(accounting_path, {"schema": ACCOUNTING_SCHEMA, "observations": [absent]})
        rc, payload, stderr = invoke(audit_args)
        cli_case(
            "absent_evidence",
            rc,
            payload,
            stderr,
            1,
            "mori-evidence-loss:audit:aggregator-r10:cleanup:evidence_missing",
            lambda item: item.get("invalid") == 1 and item.get("pin_allowed") is False,
        )

        (evidence_dir / "cleanup.txt").write_bytes(b"tampered cleanup provenance\n")
        _write_json(accounting_path, {"schema": ACCOUNTING_SCHEMA, "observations": [unresolved_row]})
        rc, payload, stderr = invoke(audit_args)
        cli_case(
            "tampered_evidence",
            rc,
            payload,
            stderr,
            1,
            "mori-evidence-loss:audit:aggregator-r10:cleanup:hash_mismatch",
            lambda item: item.get("invalid") == 1 and item.get("pin_allowed") is False,
        )
        stale = copy.deepcopy(unresolved_row)
        stale["cleanup"]["sha256"] = hashlib.sha256(b"tampered cleanup provenance\n").hexdigest()
        _write_json(accounting_path, {"schema": ACCOUNTING_SCHEMA, "observations": [stale]})
        rc, payload, stderr = invoke(audit_args)
        cli_case(
            "uncommitted_replacement",
            rc,
            payload,
            stderr,
            1,
            "mori-evidence-loss:audit:aggregator-r10:cleanup:revision_hash_mismatch",
            lambda item: item.get("invalid") == 1 and item.get("pin_allowed") is False,
        )
        (evidence_dir / "cleanup.txt").write_bytes(files["cleanup.txt"])

        duplicate = copy.deepcopy(unresolved_row)
        _write_json(accounting_path, {"schema": ACCOUNTING_SCHEMA, "observations": [unresolved_row, duplicate]})
        rc, payload, stderr = invoke(audit_args)
        cli_case(
            "duplicate_accounting_ids",
            rc,
            payload,
            stderr,
            2,
            "mori-evidence-loss:setup:duplicate_observation_id",
        )

        unsafe = copy.deepcopy(unresolved_row)
        unsafe["cleanup"]["path"] = "../outside.txt"
        _write_json(accounting_path, {"schema": ACCOUNTING_SCHEMA, "observations": [unsafe]})
        rc, payload, stderr = invoke(audit_args)
        cli_case(
            "unsafe_traversal",
            rc,
            payload,
            stderr,
            1,
            "mori-evidence-loss:audit:aggregator-r10:cleanup:unsafe_path",
            lambda item: item.get("invalid") == 1,
        )

        symlink_path = evidence_dir / "linked-cleanup.txt"
        try:
            os.symlink("cleanup.txt", symlink_path)
        except OSError:
            failures.append("unsafe_symlink_fixture_unavailable")
        else:
            symlink_ref = copy.deepcopy(unresolved_row)
            symlink_ref["cleanup"]["path"] = "evidence/linked-cleanup.txt"
            _write_json(accounting_path, {"schema": ACCOUNTING_SCHEMA, "observations": [symlink_ref]})
            rc, payload, stderr = invoke(audit_args)
            cli_case(
                "unsafe_symlink",
                rc,
                payload,
                stderr,
                1,
                "mori-evidence-loss:audit:aggregator-r10:cleanup:unsafe_symlink",
                lambda item: item.get("invalid") == 1,
            )

        unknown = copy.deepcopy(unresolved_row)
        unknown["state"] = "unknown"
        _write_json(accounting_path, {"schema": ACCOUNTING_SCHEMA, "observations": [unknown]})
        rc, payload, stderr = invoke(audit_args)
        cli_case(
            "unknown_state",
            rc,
            payload,
            stderr,
            1,
            "mori-evidence-loss:audit:aggregator-r10:state:unknown_state",
            lambda item: item.get("invalid") == 1 and item.get("pin_allowed") is False,
        )

        baseline_mismatch = copy.deepcopy(unresolved_row)
        baseline_mismatch["baseline"] = ref("deletion.txt")
        _write_json(accounting_path, {"schema": ACCOUNTING_SCHEMA, "observations": [baseline_mismatch]})
        rc, payload, stderr = invoke(audit_args)
        cli_case(
            "baseline_identity",
            rc,
            payload,
            stderr,
            1,
            "mori-evidence-loss:audit:aggregator-r10:baseline:baseline_mismatch",
            lambda item: item.get("invalid") == 1 and item.get("pin_allowed") is False,
        )

        malformed_required = copy.deepcopy(required)
        malformed_required["observations"].append(copy.deepcopy(malformed_required["observations"][0]))
        _write_json(required_path, malformed_required)
        _write_json(accounting_path, {"schema": ACCOUNTING_SCHEMA, "observations": [unresolved_row]})
        rc, payload, stderr = invoke(audit_args)
        cli_case(
            "duplicate_required_ids",
            rc,
            payload,
            stderr,
            2,
            "mori-evidence-loss:setup:duplicate_observation_id",
        )
        _write_json(required_path, required)

        cases = {
            "schema": CASES_SCHEMA,
            "cases": [
                {"id": "loss-unknown", "required_evidence_lost": True, "independent_disposition": False, "ordinary_state_change": True, "expected_class": "census-regression", "expected_pin_allowed": False},
                {"id": "loss-cleanup-only", "required_evidence_lost": True, "independent_disposition": False, "ordinary_state_change": False, "expected_class": "census-regression", "expected_pin_allowed": False},
                {"id": "loss-independent-cleanup", "required_evidence_lost": True, "independent_disposition": True, "ordinary_state_change": False, "expected_class": "live-state", "expected_pin_allowed": True},
                {"id": "loss-independent-settlement", "required_evidence_lost": True, "independent_disposition": True, "ordinary_state_change": True, "expected_class": "live-state", "expected_pin_allowed": True},
                {"id": "ordinary-aging", "required_evidence_lost": False, "independent_disposition": False, "ordinary_state_change": True, "expected_class": "live-state", "expected_pin_allowed": True},
                {"id": "ordinary-state", "required_evidence_lost": False, "independent_disposition": False, "ordinary_state_change": False, "expected_class": "live-state", "expected_pin_allowed": True},
            ],
        }
        cases_path = fixture / "cases.json"
        before_rule_path = fixture / "before-rule.json"
        after_rule_path = fixture / "after-rule.json"
        _write_json(cases_path, cases)
        _write_json(before_rule_path, {
            "schema": RULE_SCHEMA,
            "evidence_loss_blocks": False,
            "source": "corpus/QUALITY.md:245-250",
            "interpretation": "Explicit Q67 cause-only model",
        })
        _write_json(after_rule_path, {"schema": RULE_SCHEMA, "evidence_loss_blocks": True, "source": "round21 supersession"})
        after_rc, after_payload, after_stderr = invoke(["classify", "--rule", str(after_rule_path), "--cases", str(cases_path)])
        cli_case(
            "after_rule",
            after_rc,
            after_payload,
            after_stderr,
            0,
            "mori-evidence-loss:classify:result",
            lambda item: item.get("matched") is True and item.get("mismatched") == 0,
        )

        def check_case_row(name: str, payload: dict[str, Any] | None, rc: int, expected_rc: int, case_id: str, finding_id: str, klass: str, pin: bool, matched: bool) -> None:
            check(f"{name}_rc", rc == expected_rc)
            row = next((item for item in payload.get("cases", []) if item.get("id") == case_id), None) if payload is not None else None
            check(f"{name}_finding_id", type(row) is dict and row.get("finding_id") == finding_id)
            check(
                f"{name}_decision",
                type(row) is dict and row.get("observed_class") == klass
                and row.get("observed_pin_allowed") is pin and row.get("matched") is matched,
            )

        check_case_row("after_loss_unknown", after_payload, after_rc, 0, "loss-unknown", "mori-evidence-loss:classify:loss-unknown", "census-regression", False, True)
        check_case_row("after_loss_cleanup_only", after_payload, after_rc, 0, "loss-cleanup-only", "mori-evidence-loss:classify:loss-cleanup-only", "census-regression", False, True)
        check_case_row("after_independent_cleanup", after_payload, after_rc, 0, "loss-independent-cleanup", "mori-evidence-loss:classify:loss-independent-cleanup", "live-state", True, True)
        check_case_row("after_independent_settlement", after_payload, after_rc, 0, "loss-independent-settlement", "mori-evidence-loss:classify:loss-independent-settlement", "live-state", True, True)
        check_case_row("after_ordinary_aging", after_payload, after_rc, 0, "ordinary-aging", "mori-evidence-loss:classify:ordinary-aging", "live-state", True, True)
        check_case_row("after_ordinary_state", after_payload, after_rc, 0, "ordinary-state", "mori-evidence-loss:classify:ordinary-state", "live-state", True, True)

        before_rc, before_payload, before_stderr = invoke(["classify", "--rule", str(before_rule_path), "--cases", str(cases_path)])
        cli_case(
            "before_rule",
            before_rc,
            before_payload,
            before_stderr,
            1,
            "mori-evidence-loss:classify:result",
            lambda item: item.get("matched") is False and item.get("mismatched") == 2,
        )
        check_case_row("before_loss_unknown", before_payload, before_rc, 1, "loss-unknown", "mori-evidence-loss:classify:loss-unknown", "live-state", True, False)
        check_case_row("before_loss_cleanup_only", before_payload, before_rc, 1, "loss-cleanup-only", "mori-evidence-loss:classify:loss-cleanup-only", "live-state", True, False)
        check_case_row("before_independent_cleanup", before_payload, before_rc, 1, "loss-independent-cleanup", "mori-evidence-loss:classify:loss-independent-cleanup", "live-state", True, True)
        check_case_row("before_independent_settlement", before_payload, before_rc, 1, "loss-independent-settlement", "mori-evidence-loss:classify:loss-independent-settlement", "live-state", True, True)
        check_case_row("before_ordinary_aging", before_payload, before_rc, 1, "ordinary-aging", "mori-evidence-loss:classify:ordinary-aging", "live-state", True, True)
        check_case_row("before_ordinary_state", before_payload, before_rc, 1, "ordinary-state", "mori-evidence-loss:classify:ordinary-state", "live-state", True, True)
        minimal_false_path = fixture / "minimal-false-rule.json"
        _write_json(minimal_false_path, {"schema": RULE_SCHEMA, "evidence_loss_blocks": False})
        rc, payload, stderr = invoke(["classify", "--rule", str(minimal_false_path), "--cases", str(cases_path)])
        cli_case(
            "minimal_false_has_no_phase_gate", rc, payload, stderr, 1,
            "mori-evidence-loss:classify:result",
            lambda item: item.get("mismatched") == 2
            and all(row.get("observed_class") == "live-state"
                    and row.get("observed_pin_allowed") is True
                    for row in item.get("cases", [])),
        )

        bad_rule_path = fixture / "bad-rule.json"
        _write_json(bad_rule_path, {"schema": RULE_SCHEMA, "evidence_loss_blocks": 1, "source": "Q67"})
        rc, payload, stderr = invoke(["classify", "--rule", str(bad_rule_path), "--cases", str(cases_path)])
        cli_case("boolean_not_integer", rc, payload, stderr, 2, "mori-evidence-loss:setup:invalid_rule_schema")
        bad_cases = copy.deepcopy(cases)
        bad_cases["cases"][0]["required_evidence_lost"] = 1
        bad_cases_path = fixture / "bad-cases.json"
        _write_json(bad_cases_path, bad_cases)
        rc, payload, stderr = invoke(["classify", "--rule", str(after_rule_path), "--cases", str(bad_cases_path)])
        cli_case("case_boolean_not_integer", rc, payload, stderr, 2, "mori-evidence-loss:setup:invalid_case_boolean")
        duplicate_cases = copy.deepcopy(cases)
        duplicate_cases["cases"].append(copy.deepcopy(duplicate_cases["cases"][0]))
        duplicate_cases_path = fixture / "duplicate-cases.json"
        _write_json(duplicate_cases_path, duplicate_cases)
        rc, payload, stderr = invoke(["classify", "--rule", str(after_rule_path), "--cases", str(duplicate_cases_path)])
        cli_case("duplicate_case_ids", rc, payload, stderr, 2, "mori-evidence-loss:setup:duplicate_case_id")

        disposed_row = copy.deepcopy(unresolved_row)
        disposed_row["state"] = "disposed"
        disposed_row["independent_disposition"] = {
            **ref("disposition.json"),
            "independent": True,
            "actor": "reviewer",
            "wave_id": "round-10",
            "disposition": "settlement",
        }
        _write_json(accounting_path, {"schema": ACCOUNTING_SCHEMA, "observations": [disposed_row]})
        rc, payload, stderr = invoke(audit_args)
        cli_case(
            "declared_disposition",
            rc,
            payload,
            stderr,
            1,
            "mori-evidence-loss:audit:aggregator-r10:external_review_required",
            lambda item: item.get("disposed") == 1 and item.get("unresolved") == 1
            and item.get("invalid") == 0 and item.get("pin_allowed") is False
            and item.get("trust_basis") == "declared-record-not-authenticated",
        )
        same_actor = copy.deepcopy(disposed_row)
        same_actor["cleanup"]["actor"] = "reviewer"
        _write_json(accounting_path, {"schema": ACCOUNTING_SCHEMA, "observations": [same_actor]})
        rc, payload, stderr = invoke(audit_args)
        cli_case(
            "same_actor_rejected",
            rc,
            payload,
            stderr,
            1,
            "mori-evidence-loss:audit:aggregator-r10:independent_disposition:independent_actor_not_distinct",
            lambda item: item.get("disposed") == 0 and item.get("unresolved") == 1
            and item.get("invalid") == 1 and item.get("pin_allowed") is False,
        )
        contextual_record = json.loads(files["disposition.json"])
        contextual_record["context"] = "synthetic fixture metadata"
        contextual_bytes = json.dumps(contextual_record, sort_keys=True).encode() + b"\n"
        (evidence_dir / "disposition.json").write_bytes(contextual_bytes)
        contextual_revision = _run_fixture_git(root)
        contextual_row = copy.deepcopy(disposed_row)
        contextual_row["independent_disposition"].update({
            "revision": contextual_revision,
            "sha256": hashlib.sha256(contextual_bytes).hexdigest(),
        })
        _write_json(accounting_path, {"schema": ACCOUNTING_SCHEMA, "observations": [contextual_row]})
        rc, payload, stderr = invoke(audit_args)
        cli_case(
            "disposition_context_is_not_acceptance", rc, payload, stderr, 1,
            "mori-evidence-loss:audit:aggregator-r10:external_review_required",
            lambda item: item.get("disposed") == 1 and item.get("invalid") == 0
            and item.get("unresolved") == 1 and item.get("pin_allowed") is False,
        )

    report = {
        "schema": SELFTEST_SCHEMA,
        "passed": not failures,
        "checks": checks,
        "failures": failures,
        "finding_id": "mori-evidence-loss:audit:aggregator-r10:unresolved",
    }
    _emit(report)
    return 0 if not failures else 1


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit retained evidence and classify evidence-loss decisions.", allow_abbrev=False)
    parser.add_argument("--selftest", action="store_true", help="run isolated CLI selftests")
    commands = parser.add_subparsers(dest="command")
    audit_parser = commands.add_parser("audit", allow_abbrev=False)
    audit_parser.add_argument("--root", required=True, help="own-lane Git root containing evidence copies")
    audit_parser.add_argument("--required", required=True, help="required-observations JSON")
    audit_parser.add_argument("--accounting", required=True, help="loss-accounting JSON")
    classify_parser = commands.add_parser("classify", allow_abbrev=False)
    classify_parser.add_argument("--rule", required=True, help="evidence-loss rule JSON")
    classify_parser.add_argument("--cases", required=True, help="frozen classification cases JSON")
    return parser


def _error_payload(command: str | None, error: str) -> dict[str, Any]:
    schema = CLASSIFICATION_SCHEMA if command == "classify" else AUDIT_SCHEMA
    return {
        "schema": schema,
        "error": error,
        "finding_id": f"mori-evidence-loss:setup:{error}",
        "pin_allowed": False,
        "trust_basis": "declared-record-not-authenticated",
    }


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    if args.selftest:
        if args.command is not None:
            _emit(_error_payload(args.command, "selftest_must_be_standalone"))
            return 2
        return _selftest()
    if args.command is None:
        _emit(_error_payload(None, "command_required"))
        return 2
    try:
        if args.command == "audit":
            payload, rc = audit(args.root, args.required, args.accounting)
        else:
            payload, rc = classify(args.rule, args.cases)
    except SetupError as exc:
        _emit(_error_payload(args.command, exc.code))
        return 2
    _emit(payload)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
