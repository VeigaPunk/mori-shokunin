#!/usr/bin/env python3
"""C1 retained-context gate.

The scan command reads only a revision's Git tree and blob objects. Matched line
contents are never emitted; hit records contain path, line, class, and SHA-256.
"""

from __future__ import annotations

import argparse
import base64
import binascii
import copy
import fnmatch
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from collections import Counter
from typing import Any


SNAPSHOT_FILENAME = "retention.json"
SNAPSHOT_PINS = {
    SNAPSHOT_FILENAME: "55fcdd710d2bec1eef198997b3ccfa4fc584b7c7d44ad447fccf6fa48d8a00e8",
}
HIT_FIELDS = ("path", "line", "class", "line_sha256")
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
OBJECT_ID_RE = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")


class EvaluationError(Exception):
    """A safe-to-report input or evaluation failure."""

    def __init__(self, finding_id: str, error: str) -> None:
        super().__init__(error)
        self.finding_id = finding_id
        self.error = error


def emit(value: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n")


def read_json(path: str | Path) -> tuple[Any, bytes]:
    try:
        raw = Path(path).read_bytes()
        value = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        raise EvaluationError("RETENTION_SETUP", "invalid_json_input") from None
    return value, raw


def validate_policy(policy: Any, require_schema: bool = True) -> tuple[list[tuple[str, re.Pattern[str]]], set[str], list[str]]:
    if not isinstance(policy, dict):
        raise EvaluationError("RETENTION_SETUP", "invalid_policy")
    if require_schema and policy.get("schema") != "mori-retention-policy-v1":
        raise EvaluationError("RETENTION_SETUP", "invalid_policy_schema")
    raw_classes = policy.get("classes")
    must_paths = policy.get("must_redact_paths")
    non_author = policy.get("non_author_paths_glob")
    if not isinstance(raw_classes, list) or not isinstance(must_paths, list) or not isinstance(non_author, list):
        raise EvaluationError("RETENTION_SETUP", "invalid_policy_shape")
    classes: list[tuple[str, re.Pattern[str]]] = []
    seen: set[str] = set()
    for entry in raw_classes:
        if not isinstance(entry, dict) or not isinstance(entry.get("id"), str) or not isinstance(entry.get("regex"), str):
            raise EvaluationError("RETENTION_SETUP", "invalid_policy_class")
        class_id = entry["id"]
        if class_id in seen:
            raise EvaluationError("RETENTION_SETUP", "duplicate_policy_class")
        seen.add(class_id)
        try:
            compiled = re.compile(entry["regex"])
        except re.error:
            raise EvaluationError("RETENTION_SETUP", "invalid_policy_regex") from None
        classes.append((class_id, compiled))
    if not all(isinstance(path, str) and path for path in must_paths):
        raise EvaluationError("RETENTION_SETUP", "invalid_must_redact_paths")
    if not all(isinstance(pattern, str) and pattern for pattern in non_author):
        raise EvaluationError("RETENTION_SETUP", "invalid_non_author_globs")
    return classes, set(must_paths), list(non_author)


def _blob_hits(path: str, data: bytes, classes: list[tuple[str, re.Pattern[str]]]) -> list[dict[str, Any]]:
    if b"\0" in data:
        return []
    text = data.decode("utf-8", errors="replace")
    hits: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.split("\n"), 1):
        for class_id, expression in classes:
            if expression.search(line):
                hits.append({
                    "path": path,
                    "line": line_number,
                    "class": class_id,
                    "line_sha256": hashlib.sha256(line.encode("utf-8")).hexdigest(),
                })
    return hits


def _hit_tuple(hit: dict[str, Any]) -> tuple[str, int, str, str]:
    return (hit["path"], hit["line"], hit["class"], hit["line_sha256"])


def _normalize_hit(hit: Any) -> dict[str, Any]:
    if not isinstance(hit, dict) or set(hit) != set(HIT_FIELDS):
        raise EvaluationError("RETENTION_SETUP", "invalid_population_hit")
    path, line, class_id, digest = (hit.get(field) for field in HIT_FIELDS)
    if not isinstance(path, str) or not path or not isinstance(line, int) or isinstance(line, bool) or line < 1:
        raise EvaluationError("RETENTION_SETUP", "invalid_population_hit")
    if not isinstance(class_id, str) or not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
        raise EvaluationError("RETENTION_SETUP", "invalid_population_hit")
    return {"path": path, "line": line, "class": class_id, "line_sha256": digest}


def _is_non_author(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)


def _population_summary(hits: list[dict[str, Any]], must_paths: set[str], non_author: list[str]) -> dict[str, int]:
    excluded = [hit for hit in hits if _is_non_author(hit["path"], non_author)]
    return {
        "hits": len(hits),
        "non_author": len(excluded),
        "must_redact": sum(1 for hit in hits if hit["path"] in must_paths),
        "files": len({hit["path"] for hit in hits}),
        "metric_before": len(hits) - len(excluded),
    }


def _validate_allowlist(value: Any, classes: list[tuple[str, re.Pattern[str]]]) -> list[dict[str, str]]:
    if not isinstance(value, list):
        raise EvaluationError("RETENTION_SETUP", "invalid_allowlist_shape")
    known_classes = {class_id for class_id, _ in classes}
    rows: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    expected_fields = {"path", "class", "line_sha256", "reason", "rule"}
    for row in value:
        if not isinstance(row, dict) or set(row) != expected_fields:
            raise EvaluationError("RETENTION_SETUP", "invalid_allowlist_row")
        path, class_id, digest, reason, rule = (row.get(key) for key in ("path", "class", "line_sha256", "reason", "rule"))
        if not isinstance(path, str) or not path or not isinstance(class_id, str) or class_id not in known_classes:
            raise EvaluationError("RETENTION_SETUP", "invalid_allowlist_row")
        if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
            raise EvaluationError("RETENTION_SETUP", "invalid_allowlist_row")
        if not isinstance(reason, str) or not reason.strip() or not isinstance(rule, str) or rule not in {"a", "b", "c"}:
            raise EvaluationError("RETENTION_SETUP", "invalid_allowlist_row")
        key = (path, class_id, digest)
        if key in seen:
            raise EvaluationError("RETENTION_SETUP", "duplicate_allowlist_row")
        seen.add(key)
        rows.append({"path": path, "class": class_id, "line_sha256": digest, "reason": reason, "rule": rule})
    return rows


def _git(repo: str, *args: str, input_bytes: bytes | None = None) -> bytes:
    try:
        result = subprocess.run(
            ["git", "-C", repo, *args],
            input=input_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError:
        raise EvaluationError("RETENTION_SETUP", "git_unavailable") from None
    if result.returncode != 0:
        raise EvaluationError("RETENTION_SETUP", "git_read_failed")
    return result.stdout


def _scan_git_revision(repo: str, revision: str, classes: list[tuple[str, re.Pattern[str]]]) -> tuple[str, list[dict[str, Any]]]:
    if not revision or "\0" in revision or "\n" in revision:
        raise EvaluationError("RETENTION_SETUP", "invalid_revision")
    resolved = _git(
        repo,
        "cat-file",
        "--batch-check=%(objectname) %(objecttype)",
        input_bytes=(revision + "^{commit}\n").encode("utf-8"),
    ).decode("ascii", errors="replace").strip().split()
    if len(resolved) != 2 or resolved[1] != "commit" or not OBJECT_ID_RE.fullmatch(resolved[0]):
        raise EvaluationError("RETENTION_SETUP", "revision_not_commit")
    commit = resolved[0]
    tree_output = _git(repo, "ls-tree", "-r", "-z", "--full-tree", commit)
    hits: list[dict[str, Any]] = []
    for entry in tree_output.split(b"\0"):
        if not entry:
            continue
        try:
            metadata, path_bytes = entry.split(b"\t", 1)
            mode, kind, object_id = metadata.split()
        except ValueError:
            raise EvaluationError("RETENTION_SETUP", "invalid_git_tree") from None
        if kind != b"blob" or mode == b"160000":
            continue
        blob = _git(repo, "cat-file", "blob", object_id.decode("ascii"))
        path = path_bytes.decode("utf-8", errors="replace")
        hits.extend(_blob_hits(path, blob, classes))
    return commit, hits


def _load_population(path: str | Path, policy_sha256: str, must_paths: set[str], non_author: list[str]) -> tuple[str, list[dict[str, Any]]]:
    value, _ = read_json(path)
    if not isinstance(value, dict) or value.get("schema") != "mori-retention-population-v1":
        raise EvaluationError("RETENTION_SETUP", "invalid_population_schema")
    commit = value.get("commit")
    if not isinstance(commit, str) or not OBJECT_ID_RE.fullmatch(commit):
        raise EvaluationError("RETENTION_SETUP", "invalid_population_commit")
    if value.get("policy_sha256") != policy_sha256:
        raise EvaluationError("RETENTION_SETUP", "population_policy_mismatch")
    raw_hits = value.get("hits")
    if not isinstance(raw_hits, list):
        raise EvaluationError("RETENTION_SETUP", "invalid_population_hits")
    expected_hits = [_normalize_hit(hit) for hit in raw_hits]
    summary = value.get("summary")
    if not isinstance(summary, dict) or summary != _population_summary(expected_hits, must_paths, non_author):
        raise EvaluationError("RETENTION_SETUP", "invalid_population_summary")
    return commit, expected_hits


def _scan_result(
    hits: list[dict[str, Any]],
    must_paths: set[str],
    non_author: list[str],
    allowlist: list[dict[str, str]],
    commit: str | None,
    policy_sha256: str | None,
    population: tuple[str, list[dict[str, Any]]] | None = None,
) -> tuple[dict[str, Any], int]:
    hit_key_set = {(hit["path"], hit["class"], hit["line_sha256"]) for hit in hits}
    forbidden_rows: list[dict[str, Any]] = []
    stale_rows: list[dict[str, Any]] = []
    allowed_keys: set[tuple[str, str, str]] = set()
    for row in allowlist:
        key = (row["path"], row["class"], row["line_sha256"])
        if row["path"] in must_paths:
            forbidden_rows.append({
                "finding_id": "allowlist_forbidden",
                "path": row["path"],
                "line": None,
                "class": row["class"],
                "line_sha256": row["line_sha256"],
            })
        elif key in hit_key_set:
            allowed_keys.add(key)
        else:
            stale_rows.append({
                "finding_id": "allowlist_stale",
                "path": row["path"],
                "line": None,
                "class": row["class"],
                "line_sha256": row["line_sha256"],
            })

    non_author_hits = [hit for hit in hits if _is_non_author(hit["path"], non_author)]
    allowed_hits = [hit for hit in hits if (hit["path"], hit["class"], hit["line_sha256"]) in allowed_keys]
    unallowlisted_hits = [
        hit for hit in hits
        if not _is_non_author(hit["path"], non_author)
        and (hit["path"], hit["class"], hit["line_sha256"]) not in allowed_keys
    ]
    metric = len(unallowlisted_hits)
    routed = sum(1 for hit in unallowlisted_hits if hit["path"] in must_paths)
    population_match: bool | None = None
    new_hits: int | None = None
    missing_hits: int | None = None
    if population is not None:
        _, expected_hits = population
        actual_counter = Counter(_hit_tuple(hit) for hit in hits)
        expected_counter = Counter(_hit_tuple(hit) for hit in expected_hits)
        new_hits = sum((actual_counter - expected_counter).values())
        missing_hits = sum((expected_counter - actual_counter).values())
        population_match = new_hits == 0 and missing_hits == 0

    if forbidden_rows:
        finding_id = "allowlist_forbidden"
    elif metric or population_match is False:
        finding_id = "RETENTION_FINDINGS"
    elif stale_rows:
        finding_id = "allowlist_stale"
    else:
        finding_id = "RETENTION_CLEAN"
    exit_code = 1 if metric or forbidden_rows or population_match is False else 0
    result: dict[str, Any] = {
        "finding_id": finding_id,
        "commit": commit,
        "policy_sha256": policy_sha256,
        "metric": metric,
        "routed": routed,
        "non_author": len(non_author_hits),
        "hits": hits,
        "unallowlisted_hits": unallowlisted_hits,
        "allowlisted_hits": allowed_hits,
        "forbidden_allowlist": forbidden_rows,
        "warnings": stale_rows,
    }
    if population is not None:
        result["population_commit"] = population[0]
        result["population_match"] = population_match
        result["new_hits"] = new_hits
        result["missing_population_hits"] = missing_hits
    return result, exit_code


def scan(args: argparse.Namespace) -> tuple[dict[str, Any], int]:
    policy_value, policy_raw = read_json(args.policy)
    classes, must_paths, non_author = validate_policy(policy_value)
    policy_sha256 = hashlib.sha256(policy_raw).hexdigest()
    commit, hits = _scan_git_revision(args.repo, args.rev, classes)
    allowlist_rows: list[dict[str, str]] = []
    if args.allowlist:
        allowlist_value, _ = read_json(args.allowlist)
        if isinstance(allowlist_value, dict):
            allowlist_value = allowlist_value.get("rows")
        allowlist_rows = _validate_allowlist(allowlist_value, classes)
    population = None
    if args.expect_population:
        population = _load_population(args.expect_population, policy_sha256, must_paths, non_author)
    return _scan_result(hits, must_paths, non_author, allowlist_rows, commit, policy_sha256, population)


def _snapshot_failure(error: str) -> tuple[dict[str, Any], int]:
    return {"finding_id": "snapshot_tampered", "error": error}, 2


def frozen_run(snapshot_dir: str | None) -> tuple[dict[str, Any], int]:
    root = Path(__file__).resolve().parents[1]
    directory = Path(snapshot_dir) if snapshot_dir else root / ".ufo" / "waves" / "round-18" / "gate-snapshots" / "retention"
    try:
        if directory.is_symlink() or not directory.is_dir():
            return _snapshot_failure("snapshot_missing")
        entries = list(directory.iterdir())
        if {entry.name for entry in entries} != set(SNAPSHOT_PINS) or any(entry.is_symlink() or not entry.is_file() for entry in entries):
            return _snapshot_failure("snapshot_file_set_mismatch")
        snapshot_bytes = (directory / SNAPSHOT_FILENAME).read_bytes()
    except OSError:
        return _snapshot_failure("snapshot_unreadable")
    snapshot_sha256 = hashlib.sha256(snapshot_bytes).hexdigest()
    if snapshot_sha256 != SNAPSHOT_PINS[SNAPSHOT_FILENAME]:
        return _snapshot_failure("snapshot_digest_mismatch")
    try:
        snapshot = json.loads(snapshot_bytes.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError):
        return _snapshot_failure("snapshot_invalid_json")
    if not isinstance(snapshot, dict) or snapshot.get("schema") != "mori-retention-frozen-snapshot-v1":
        return _snapshot_failure("snapshot_invalid_schema")
    try:
        classes, must_paths, non_author = validate_policy(snapshot.get("policy"), require_schema=False)
        files = snapshot.get("files")
        expected = snapshot.get("expected")
        if not isinstance(files, list) or not isinstance(expected, dict):
            raise EvaluationError("snapshot_tampered", "snapshot_invalid_shape")
        hits: list[dict[str, Any]] = []
        seen_paths: set[str] = set()
        for item in files:
            if not isinstance(item, dict) or set(item) != {"path", "content_b64"} or not isinstance(item.get("path"), str) or not item["path"] or not isinstance(item.get("content_b64"), str):
                raise EvaluationError("snapshot_tampered", "snapshot_invalid_file")
            if item["path"] in seen_paths:
                raise EvaluationError("snapshot_tampered", "snapshot_duplicate_path")
            seen_paths.add(item["path"])
            try:
                content = base64.b64decode(item["content_b64"], validate=True)
            except (ValueError, binascii.Error):
                raise EvaluationError("snapshot_tampered", "snapshot_invalid_file_data") from None
            hits.extend(_blob_hits(item["path"], content, classes))
        result, scan_exit = _scan_result(hits, must_paths, non_author, [], None, None)
        actual = {
            "finding_id": result["finding_id"],
            "exit_code": scan_exit,
            "metric": result["metric"],
            "routed": result["routed"],
            "hits": result["hits"],
        }
        if expected != actual:
            return {
                "finding_id": "FROZEN_VERDICT_MISMATCH",
                "snapshot_sha256": snapshot_sha256,
                "verdict_match": False,
                "expected": expected,
                "actual": actual,
            }, 1
        return {
            "finding_id": "FROZEN_OK",
            "snapshot_sha256": snapshot_sha256,
            "verdict_match": True,
            "expected": expected,
            "actual": actual,
        }, 0
    except EvaluationError as error:
        return _snapshot_failure(error.error)


def _run_git_fixture(repo: Path, files: dict[str, bytes], env: dict[str, str]) -> None:
    repo.mkdir(parents=True)
    initialized = subprocess.run(["git", "-C", str(repo), "init", "--quiet"], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if initialized.returncode != 0:
        raise RuntimeError("fixture_init")
    for relative, content in files.items():
        target = repo / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    added = subprocess.run(["git", "-C", str(repo), "add", "--all"], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if added.returncode != 0:
        raise RuntimeError("fixture_add")
    committed = subprocess.run(
        ["git", "-C", str(repo), "-c", "user.name=Retention selftest", "-c", "user.email=retention-selftest@example.invalid", "commit", "--quiet", "-m", "fixture"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if committed.returncode != 0:
        raise RuntimeError("fixture_commit")


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def _selftest_policy(original: dict[str, Any], path: Path, must_paths: list[str] | None = None, non_author: list[str] | None = None) -> Path:
    policy = copy.deepcopy(original)
    if must_paths is not None:
        policy["must_redact_paths"] = must_paths
    if non_author is not None:
        policy["non_author_paths_glob"] = non_author
    _write_json(path, policy)
    return path


def _invoke(script: Path, args: list[str], env: dict[str, str]) -> tuple[int, dict[str, Any] | None, str, str]:
    try:
        completed = subprocess.run(
            [sys.executable, str(script), *args],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except OSError:
        return 127, None, "", ""
    try:
        value = json.loads(completed.stdout)
    except json.JSONDecodeError:
        value = None
    return completed.returncode, value if isinstance(value, dict) else None, completed.stdout, completed.stderr


def selftest() -> tuple[str, int]:
    root = Path(__file__).resolve().parents[1]
    expected_tmp = (root / ".scratch").resolve()
    supplied_tmp = os.environ.get("TMPDIR")
    if not supplied_tmp:
        return "SELFTEST retention-gate FAIL 0/19", 2
    try:
        actual_tmp = Path(supplied_tmp).resolve(strict=True)
    except OSError:
        return "SELFTEST retention-gate FAIL 0/19", 2
    if actual_tmp != expected_tmp or not actual_tmp.is_dir():
        return "SELFTEST retention-gate FAIL 0/19", 2

    policy_path = root / ".ufo" / "waves" / "round-18" / "frozen" / "c1-policy.json"
    try:
        original_policy, _ = read_json(policy_path)
        validate_policy(original_policy)
    except EvaluationError:
        return "SELFTEST retention-gate FAIL 0/19", 2

    arm_results: list[bool] = []
    env = os.environ.copy()
    env["GIT_CONFIG_GLOBAL"] = "/dev/null"
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_AUTHOR_NAME"] = "Retention selftest"
    env["GIT_AUTHOR_EMAIL"] = "retention-selftest@example.invalid"
    env["GIT_COMMITTER_NAME"] = "Retention selftest"
    env["GIT_COMMITTER_EMAIL"] = "retention-selftest@example.invalid"
    script = Path(__file__).resolve()

    def scan_fixture(
        base: Path,
        name: str,
        files: dict[str, bytes],
        policy: Path,
        extra: list[str] | None = None,
        revision: str = "HEAD",
    ) -> tuple[int, dict[str, Any] | None, str, str]:
        repo = base / name / "repo"
        _run_git_fixture(repo, files, env)
        command = ["scan", "--repo", str(repo), "--rev", revision, "--policy", str(policy)]
        if extra:
            command.extend(extra)
        return _invoke(script, command, env)

    def fixture(encoded: str) -> bytes:
        return base64.b64decode(encoded, validate=True)

    texts = {
        "R1": fixture("Zml4dHVyZSAyMDI2LTEwLTIxVDEyLTM0LTU2LTc4OVpfMDEyM2FiY2QtdGVzdAo="),
        "R2": fixture("Zml4dHVyZSAub21wL2FnZW50L3Nlc3Npb25zL2NoaWxkCg=="),
        "R3": fixture("Zml4dHVyZSA4Ny5yZWFkLmxvZwo="),
        "R4": fixture("Zml4dHVyZSB+L0RvY3VtZW50cy9jMS1maXh0dXJlLnR4dCBGQUtFX1NFQ1JFVF9SMThfTkVWRVJfRU1JVAo="),
        "R5": fixture("Zml4dHVyZSAuYmFzaF9oaXN0b3J5Cg=="),
        "R6": fixture("Zml4dHVyZSBzdWRvZXJzCg=="),
        "R7": fixture("Zml4dHVyZSAub21wL2FnZW50L2NvbmZpZy55bWwK"),
        "R8": fixture("Zml4dHVyZSBmYWxsYmFja0NoYWlucwo="),
        "R9": fixture("Zml4dHVyZSBkYXRhLnJlYXNvbgo="),
    }
    try:
        with tempfile.TemporaryDirectory(prefix="mori-retention-selftest-", dir=str(actual_tmp)) as temp_root:
            base = Path(temp_root)
            base_policy = _selftest_policy(original_policy, base / "policy.json")
            for class_id, text in texts.items():
                exit_code, result, _, _ = scan_fixture(base, "positive-" + class_id, {"fixture/payload.txt": text}, base_policy)
                arm_results.append(
                    exit_code == 1
                    and result is not None
                    and result.get("finding_id") == "RETENTION_FINDINGS"
                    and result.get("metric") == 1
                    and [hit.get("class") for hit in result.get("hits", [])] == [class_id]
                )

            exit_code, result, _, _ = scan_fixture(base, "negative-R2-root", {"fixture/payload.txt": fixture("Lm9tcC9hZ2VudC9zZXNzaW9ucy8K")}, base_policy)
            arm_results.append(exit_code == 0 and result is not None and result.get("finding_id") == "RETENTION_CLEAN" and result.get("hits") == [])

            exit_code, result, _, _ = scan_fixture(base, "negative-R4-no-slash", {"fixture/payload.txt": fixture("fi9Eb2N1bWVudHMK")}, base_policy)
            arm_results.append(exit_code == 0 and result is not None and result.get("finding_id") == "RETENTION_CLEAN" and result.get("hits") == [])

            exit_code, result, _, _ = scan_fixture(base, "binary-skip", {"fixture/payload.bin": fixture("fi9Eb2N1bWVudHMveABzdWRvZXJzCg==")}, base_policy)
            arm_results.append(exit_code == 0 and result is not None and result.get("finding_id") == "RETENTION_CLEAN" and result.get("hits") == [])

            allow_text = fixture("Zml4dHVyZSB+L0RvY3VtZW50cy9hbGxvdy50eHQgRkFLRV9TRUNSRVRfUjE4X0FMTE9XTElTVA==")
            allow_digest = hashlib.sha256(allow_text).hexdigest()
            allowlist_path = base / "allowlist.json"
            _write_json(allowlist_path, [{
                "path": "fixture/payload.txt",
                "class": "R4",
                "line_sha256": allow_digest,
                "reason": "synthetic selftest fixture",
                "rule": "a",
            }])
            exit_code, result, _, _ = scan_fixture(
                base,
                "allowlist-match",
                {"fixture/payload.txt": allow_text + b"\n"},
                base_policy,
                ["--allowlist", str(allowlist_path)],
            )
            arm_results.append(
                exit_code == 0
                and result is not None
                and result.get("finding_id") == "RETENTION_CLEAN"
                and result.get("metric") == 0
                and len(result.get("allowlisted_hits", [])) == 1
            )

            forbidden_path = "fixture/must-redact.txt"
            forbidden_text = fixture("fi9Eb2N1bWVudHMvZm9yYmlkZGVuLnR4dA==")
            forbidden_policy = _selftest_policy(original_policy, base / "forbidden-policy.json", [forbidden_path])
            forbidden_allowlist = base / "forbidden-allowlist.json"
            _write_json(forbidden_allowlist, [{
                "path": forbidden_path,
                "class": "R4",
                "line_sha256": hashlib.sha256(forbidden_text).hexdigest(),
                "reason": "synthetic forbidden fixture",
                "rule": "b",
            }])
            exit_code, result, _, _ = scan_fixture(
                base,
                "allowlist-forbidden",
                {forbidden_path: forbidden_text + b"\n"},
                forbidden_policy,
                ["--allowlist", str(forbidden_allowlist)],
            )
            arm_results.append(
                exit_code == 1
                and result is not None
                and result.get("finding_id") == "allowlist_forbidden"
                and result.get("metric") == 1
                and result.get("routed") == 1
                and len(result.get("forbidden_allowlist", [])) == 1
            )

            stale_allowlist = base / "stale-allowlist.json"
            _write_json(stale_allowlist, [{
                "path": "fixture/absent.txt",
                "class": "R4",
                "line_sha256": "0" * 64,
                "reason": "synthetic stale fixture",
                "rule": "c",
            }])
            exit_code, result, _, _ = scan_fixture(
                base,
                "allowlist-stale",
                {"fixture/clean.txt": b"clean\n"},
                base_policy,
                ["--allowlist", str(stale_allowlist)],
            )
            arm_results.append(
                exit_code == 0
                and result is not None
                and result.get("finding_id") == "allowlist_stale"
                and len(result.get("warnings", [])) == 1
            )

            non_author_policy = _selftest_policy(
                original_policy,
                base / "non-author-policy.json",
                non_author=["corpus/lessons/round-*-verifier-spotcheck.md"],
            )
            exit_code, result, _, _ = scan_fixture(
                base,
                "non-author-exclusion",
                {"corpus/lessons/round-3-verifier-spotcheck.md": fixture("Zml4dHVyZSBzdWRvZXJzCg==")},
                non_author_policy,
            )
            arm_results.append(
                exit_code == 0
                and result is not None
                and result.get("finding_id") == "RETENTION_CLEAN"
                and result.get("metric") == 0
                and result.get("non_author") == 1
                and len(result.get("hits", [])) == 1
            )

            exit_code, result, _, _ = scan_fixture(
                base,
                "missing-revision",
                {"fixture/clean.txt": b"clean\n"},
                base_policy,
                revision="missing-revision-r18",
            )
            arm_results.append(exit_code == 2 and result is not None and result.get("finding_id") == "RETENTION_SETUP")

            snapshot_source = root / ".ufo" / "waves" / "round-18" / "gate-snapshots" / "retention" / SNAPSHOT_FILENAME
            tampered_dir = base / "tampered-snapshot"
            tampered_dir.mkdir()
            (tampered_dir / SNAPSHOT_FILENAME).write_bytes(snapshot_source.read_bytes() + b" ")
            exit_code, result, _, _ = _invoke(script, ["--frozen-run", "--snapshot-dir", str(tampered_dir)], env)
            arm_results.append(exit_code == 2 and result is not None and result.get("finding_id") == "snapshot_tampered")

            _, r4_result, r4_stdout, r4_stderr = _invoke(
                script,
                ["scan", "--repo", str(base / "positive-R4" / "repo"), "--rev", "HEAD", "--policy", str(base_policy)],
                env,
            )
            fake_secret = fixture("RkFLRV9TRUNSRVRfUjE4X05FVkVSX0VNSVQ=").decode("ascii")
            arm_results.append(
                r4_result is not None
                and fake_secret not in r4_stdout
                and fake_secret not in r4_stderr
                and texts["R4"].decode("utf-8") not in r4_stdout
            )
    except Exception:
        arm_results = [False] * 19

    passed = sum(1 for passed_arm in arm_results if passed_arm)
    total = 19
    if len(arm_results) != total:
        return f"SELFTEST retention-gate FAIL {passed}/{total}", 1
    if passed == total:
        return f"SELFTEST retention-gate PASS {passed}/{total}", 0
    return f"SELFTEST retention-gate FAIL {passed}/{total}", 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="C1 retained-context gate")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--frozen-run", action="store_true")
    mode.add_argument("--selftest", action="store_true")
    parser.add_argument("--snapshot-dir")
    subparsers = parser.add_subparsers(dest="command")
    scan_parser = subparsers.add_parser("scan")
    scan_parser.add_argument("--repo", required=True)
    scan_parser.add_argument("--rev", required=True)
    scan_parser.add_argument("--policy", required=True)
    scan_parser.add_argument("--allowlist")
    scan_parser.add_argument("--expect-population")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as error:
        if error.code == 0:
            return 0
        emit({"finding_id": "RETENTION_SETUP", "error": "bad_arguments"})
        return 2
    if args.selftest:
        if args.command is not None or args.snapshot_dir is not None:
            emit({"finding_id": "RETENTION_SETUP", "error": "bad_arguments"})
            return 2
        message, code = selftest()
        sys.stdout.write(message + "\n")
        return code
    if args.frozen_run:
        if args.command is not None:
            emit({"finding_id": "RETENTION_SETUP", "error": "bad_arguments"})
            return 2
        result, code = frozen_run(args.snapshot_dir)
        emit(result)
        return code
    if args.snapshot_dir is not None or args.command != "scan":
        emit({"finding_id": "RETENTION_SETUP", "error": "bad_arguments"})
        return 2
    try:
        result, code = scan(args)
    except EvaluationError as error:
        emit({"finding_id": error.finding_id, "error": error.error})
        return 2
    except Exception:
        emit({"finding_id": "RETENTION_SETUP", "error": "internal_error"})
        return 2
    emit(result)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
