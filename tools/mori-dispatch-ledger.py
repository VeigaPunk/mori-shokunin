#!/usr/bin/env python3
"""Bind and verify per-attempt dispatch payload identities for mori waves."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile

SCHEMA = "mori-dispatch-ledger-v1"
RC_CLEAN = 0
RC_FINDINGS = 1
RC_UNAVAILABLE = 2
GIT_TIMEOUT_SECONDS = 30
_REV_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._/-]*(?:(?:~|\^)[0-9]*)*")


class EvaluationError(Exception):
    def __init__(self, finding_id: str, reason: str):
        super().__init__(reason)
        self.finding_id = finding_id
        self.reason = reason


def _emit(payload: dict, rc: int) -> int:
    sys.stdout.write(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n")
    return rc


def _error(finding_id: str, reason: str, rc: int = RC_UNAVAILABLE) -> int:
    return _emit(
        {
            "schema": SCHEMA,
            "status": "could-not-evaluate" if rc == RC_UNAVAILABLE else "failed",
            "finding_id": finding_id,
            "finding_ids": [finding_id],
            "error": reason,
        },
        rc,
    )


def _git_env() -> dict[str, str]:
    return {
        "PATH": os.defpath,
        "LANG": "C",
        "LC_ALL": "C",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_OPTIONAL_LOCKS": "0",
    }


def _git(repo: str, args: list[str]) -> bytes:
    try:
        proc = subprocess.run(
            ["git", "--no-optional-locks", "-C", repo, *args],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            env=_git_env(),
            timeout=GIT_TIMEOUT_SECONDS,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise EvaluationError("GIT_UNAVAILABLE", "git read failed") from exc
    if proc.returncode != 0:
        raise EvaluationError("GIT_OBJECT_UNAVAILABLE", "requested committed object is unavailable")
    return proc.stdout


def _validate_rev(rev: str) -> None:
    if not rev or not _REV_RE.fullmatch(rev):
        raise EvaluationError("REVISION_INVALID", "revision is not a supported git revision expression")


def _validate_repo_and_rev(repo: str, rev: str) -> None:
    if not repo:
        raise EvaluationError("REPOSITORY_INVALID", "repository path is required")
    _validate_rev(rev)
    _git(repo, ["cat-file", "-e", f"{rev}^{{commit}}"])


def _validate_tree_path(path: str) -> str:
    if not path or "\\" in path or "\x00" in path or path.startswith("/"):
        raise EvaluationError("TREE_PATH_INVALID", "path must be a lane-relative committed path")
    pure = PurePosixPath(path)
    if any(part in ("", ".", "..") for part in path.split("/")):
        raise EvaluationError("TREE_PATH_INVALID", "path must not traverse outside the repository")
    if pure.is_absolute():
        raise EvaluationError("TREE_PATH_INVALID", "path must be a lane-relative committed path")
    return pure.as_posix()


def _read_committed_json(repo: str, rev: str, path: str, kind: str) -> object:
    safe_path = _validate_tree_path(path)
    try:
        raw = _git(repo, ["cat-file", "blob", f"{rev}:{safe_path}"])
    except EvaluationError as exc:
        if exc.finding_id == "GIT_OBJECT_UNAVAILABLE":
            raise EvaluationError(kind, "committed JSON path is unavailable") from exc
        raise
    try:
        return json.loads(raw.decode("utf-8"), parse_constant=_reject_constant)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise EvaluationError(kind, "committed file is not valid UTF-8 JSON") from exc


def _reject_constant(_value: str):
    raise ValueError("non-JSON numeric constant")


def _payload_identity(dispatch: object) -> dict:
    if not isinstance(dispatch, (dict, list)):
        raise EvaluationError("DISPATCH_FORMAT_INVALID", "dispatch JSON must contain an object")

    def is_call(value: object) -> bool:
        return (
            isinstance(value, dict)
            and isinstance(value.get("context"), str)
            and isinstance(value.get("tasks"), list)
        )

    candidates = []
    pending = [((), dispatch)]
    while pending:
        path, value = pending.pop()
        if is_call(value):
            candidates.append((path, value))
            continue
        if isinstance(value, dict):
            pending.extend((path + (key,), child) for key, child in value.items())
        elif isinstance(value, list):
            pending.extend((path + (str(index),), child) for index, child in enumerate(value))
    preferred = [item for item in candidates if item[0] and item[0][-1] in ("run", "taskCall")]
    if len(preferred) == 1:
        call = preferred[0][1]
    elif len(candidates) == 1:
        call = candidates[0][1]
    else:
        raise EvaluationError("DISPATCH_FORMAT_INVALID", "dispatch JSON has no unique validator run object")
    context = call["context"]
    tasks = call["tasks"]
    try:
        payload = json.dumps(
            {"context": context, "tasks": tasks},
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeEncodeError) as exc:
        raise EvaluationError("DISPATCH_FORMAT_INVALID", "validator payload cannot be encoded as UTF-8 JSON") from exc
    return {
        "payload_sha256": hashlib.sha256(payload).hexdigest(),
        "payload_bytes": len(payload),
        "tasks_count": len(tasks),
    }


def _bind(repo: str, rev: str, dispatch_path: str) -> dict:
    _validate_repo_and_rev(repo, rev)
    dispatch = _read_committed_json(repo, rev, dispatch_path, "DISPATCH_UNAVAILABLE")
    identity = _payload_identity(dispatch)
    return {
        "schema": SCHEMA,
        "mode": "bind",
        "status": "bound",
        "finding_id": "PAYLOAD_BOUND",
        "finding_ids": ["PAYLOAD_BOUND"],
        "rev": rev,
        "dispatch_path": dispatch_path,
        **identity,
    }


def _valid_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _parse_at(value: object) -> dt.datetime | None:
    if not isinstance(value, str) or "T" not in value and "t" not in value:
        return None
    normalized = value[:-1] + "+00:00" if value.endswith(("Z", "z")) else value
    try:
        parsed = dt.datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed


def _verify(repo: str, rev: str, ledger_path: str) -> tuple[dict, int]:
    _validate_repo_and_rev(repo, rev)
    ledger = _read_committed_json(repo, rev, ledger_path, "LEDGER_INVALID")
    if not isinstance(ledger, list):
        raise EvaluationError("LEDGER_INVALID", "ledger JSON must be an array")

    identities: dict[str, dict] = {}
    row_results = []
    unbound = 0
    bound = 0
    ledger_findings: list[dict] = []

    def add_finding(finding_id: str, row_index: int | None = None) -> None:
        finding = {"id": finding_id, "scope": "ledger"}
        if row_index is not None:
            finding["row"] = row_index
        ledger_findings.append(finding)

    for index, row in enumerate(ledger, 1):
        reasons: list[str] = []
        identity = None
        if not isinstance(row, dict):
            reasons.append("row_not_object")
        elif "payload_sha256" not in row:
            reasons.append("legacy_no_payload_sha256")
        else:
            path = row.get("dispatch_path")
            if not isinstance(path, str):
                raise EvaluationError("DISPATCH_PATH_UNAVAILABLE", "a bound row has no committed dispatch path")
            safe_path = _validate_tree_path(path)
            if safe_path not in identities:
                dispatch = _read_committed_json(repo, rev, safe_path, "DISPATCH_PATH_UNAVAILABLE")
                identities[safe_path] = _payload_identity(dispatch)
            identity = identities[safe_path]
            if row.get("payload_sha256") != identity["payload_sha256"]:
                reasons.append("payload_sha256_mismatch")
            if not _valid_int(row.get("payload_bytes")) or row["payload_bytes"] != identity["payload_bytes"]:
                reasons.append("payload_bytes_mismatch")
            if not _valid_int(row.get("tasks_count")) or row["tasks_count"] != identity["tasks_count"]:
                reasons.append("tasks_count_mismatch")

        is_bound = not reasons
        if is_bound:
            bound += 1
            row_status = "bound"
        else:
            unbound += 1
            row_status = "unbound"
        attempt = row.get("attempt") if isinstance(row, dict) and _valid_int(row.get("attempt")) else None
        row_result = row.get("result") if isinstance(row, dict) and row.get("result") in ("refused", "started", "partial") else None
        row_results.append(
            {
                "index": index,
                "attempt": attempt,
                "status": row_status,
                "reasons": reasons,
                "result": row_result,
                "tasks_count": identity["tasks_count"] if identity else (
                    row.get("tasks_count") if isinstance(row, dict) and _valid_int(row.get("tasks_count")) else None
                ),
                "started_ids": row.get("started_ids") if isinstance(row, dict) and _valid_int(row.get("started_ids")) else None,
            }
        )

    expected_attempts = list(range(1, len(ledger) + 1))
    observed_attempts = [row.get("attempt") if isinstance(row, dict) else None for row in ledger]
    if any(not _valid_int(value) for value in observed_attempts) or observed_attempts != expected_attempts:
        add_finding("ATTEMPTS_NONCONTIGUOUS")

    previous_at = None
    for index, row in enumerate(ledger, 1):
        at = _parse_at(row.get("at") if isinstance(row, dict) else None)
        if at is None:
            add_finding("AT_INVALID", index)
            continue
        if previous_at is not None and at < previous_at:
            add_finding("AT_DECREASING", index)
        previous_at = at

    started = [
        (index, row)
        for index, row in enumerate(ledger, 1)
        if isinstance(row, dict) and row.get("result") in ("started", "partial")
    ]
    if not started:
        add_finding("STARTED_MISSING")
    if len(started) > 1:
        add_finding("DUPLICATE_STARTED")
    if any(index != len(ledger) for index, _row in started):
        add_finding("STARTED_NOT_LAST")
    for index, row in started:
        if row.get("result") != "started":
            continue
        row_info = row_results[index - 1]
        expected_count = row_info["tasks_count"]
        if not _valid_int(row.get("started_ids")) or not _valid_int(expected_count) or row["started_ids"] != expected_count:
            add_finding("STARTED_IDS_MISMATCH", index)

    row_findings = []
    for result in row_results:
        for reason in result["reasons"]:
            if reason == "legacy_no_payload_sha256":
                finding_id = "LEGACY_ROW_UNBOUND"
            elif reason == "payload_sha256_mismatch":
                finding_id = "PAYLOAD_SHA256_MISMATCH"
            elif reason == "payload_bytes_mismatch":
                finding_id = "PAYLOAD_BYTES_MISMATCH"
            elif reason == "tasks_count_mismatch":
                finding_id = "TASKS_COUNT_MISMATCH"
            else:
                finding_id = "ROW_INVALID"
            row_findings.append({"id": finding_id, "scope": "row", "row": result["index"]})

    findings = row_findings + ledger_findings
    clean = unbound == 0 and not ledger_findings
    if clean:
        finding_id = "LEDGER_CLEAN"
        finding_ids = [finding_id]
    else:
        finding_ids = sorted({item["id"] for item in findings})
        finding_id = "LEDGER_UNBOUND" if unbound else "LEDGER_FINDINGS"
    output = {
        "schema": SCHEMA,
        "mode": "verify",
        "status": "clean" if clean else "failed",
        "finding_id": finding_id,
        "finding_ids": finding_ids,
        "rev": rev,
        "ledger_path": ledger_path,
        "rows": row_results,
        "findings": findings,
        "totals": {
            "rows": len(ledger),
            "bound": bound,
            "unbound": unbound,
            "ledger_findings": len(ledger_findings),
        },
    }
    return output, RC_CLEAN if clean else RC_FINDINGS


class _JsonArgumentParser(argparse.ArgumentParser):
    def error(self, _message: str) -> None:
        _error("INPUT_INVALID", "command line arguments are invalid")
        raise SystemExit(RC_UNAVAILABLE)


def _git_selftest(repo: Path, env: dict[str, str], args: list[str]) -> None:
    proc = subprocess.run(
        ["git", "--no-optional-locks", "-C", str(repo), *args],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        env=env,
        timeout=GIT_TIMEOUT_SECONDS,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError("sandbox git setup failed")


def _selftest_row(digest: dict, *, attempt: int = 1, at: str = "2025-01-01T00:00:00+00:00",
                  result: str = "started", started_ids: int = 1, path: str = "dispatch.json") -> dict:
    return {
        "attempt": attempt,
        "at": at,
        "wave": "selftest",
        "dispatch_path": path,
        **digest,
        "slot_grant": None,
        "result": result,
        "refused_text": None,
        "started_ids": started_ids,
    }


def _write_fixture_repo(repo: Path, *, dispatch: dict | None, rows: list | None,
                        env: dict[str, str]) -> None:
    repo.mkdir(parents=True)
    if dispatch is not None:
        (repo / "dispatch.json").write_text(
            json.dumps(dispatch, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )
    (repo / "attempts.json").write_text(
        json.dumps(rows, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    _git_selftest(repo, env, ["init", "-q"])
    _git_selftest(repo, env, ["add", "--", "attempts.json", *( ["dispatch.json"] if dispatch is not None else [])])
    _git_selftest(repo, env, ["-c", "user.name=Selftest", "-c", "user.email=selftest@example.invalid",
                              "-c", "commit.gpgsign=false", "commit", "-q", "-m", "fixture"])


def _run_selftest_case(tool: Path, repo: Path, want_rc: int, want_id: str,
                       env: dict[str, str]) -> bool:
    proc = subprocess.run(
        [sys.executable, str(tool), "verify", "--repo", str(repo), "--rev", "HEAD", "--ledger", "attempts.json"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        env=env,
        timeout=GIT_TIMEOUT_SECONDS,
        check=False,
    )
    try:
        result = json.loads(proc.stdout.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return False
    ids = result.get("finding_ids", []) if isinstance(result, dict) else []
    return proc.returncode == want_rc and want_id in ids


def _selftest() -> int:
    tmpdir = os.environ.get("TMPDIR")
    if not tmpdir:
        return _error("SELFTEST_SCRATCH_REQUIRED", "TMPDIR must name the executor scratch directory")
    parent = Path(tmpdir)
    if parent.is_symlink() or not parent.is_dir():
        return _error("SELFTEST_SCRATCH_INVALID", "TMPDIR must be an existing real directory")
    resolved_parent = parent.resolve()
    for forbidden in (Path("/tmp"), Path("/var/tmp")):
        try:
            resolved_parent.relative_to(forbidden.resolve())
        except ValueError:
            continue
        return _error("SELFTEST_SCRATCH_FORBIDDEN", "selftest scratch must not be under a system temp directory")

    env = {
        "PATH": os.defpath,
        "LANG": "C",
        "LC_ALL": "C",
        "HOME": str(resolved_parent),
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_AUTHOR_NAME": "Selftest",
        "GIT_AUTHOR_EMAIL": "selftest@example.invalid",
        "GIT_COMMITTER_NAME": "Selftest",
        "GIT_COMMITTER_EMAIL": "selftest@example.invalid",
        "GIT_AUTHOR_DATE": "2025-01-01T00:00:00+00:00",
        "GIT_COMMITTER_DATE": "2025-01-01T00:00:00+00:00",
    }
    failures = []
    try:
        with tempfile.TemporaryDirectory(prefix="mori-dispatch-ledger-", dir=str(resolved_parent)) as work_text:
            work = Path(work_text)
            original = {"run": {"context": "hello", "tasks": [{"id": "a"}]}}
            original_identity = _payload_identity(original)
            clean = _selftest_row(original_identity)
            cases = []

            cases.append(("clean-ledger", original, [clean], 0, "LEDGER_CLEAN"))

            tampered = {"run": {"context": "hullo", "tasks": [{"id": "a"}]}}
            cases.append(("tampered-payload-byte", tampered, [clean], 1, "PAYLOAD_SHA256_MISMATCH"))

            wrong_digest = dict(clean)
            wrong_digest["payload_sha256"] = "0" * 64
            cases.append(("wrong-digest", original, [wrong_digest], 1, "PAYLOAD_SHA256_MISMATCH"))

            missing_started = _selftest_row(original_identity, result="refused", started_ids=0)
            cases.append(("missing-started", original, [missing_started], 1, "STARTED_MISSING"))

            started_first = _selftest_row(original_identity, attempt=1)
            refused_last = _selftest_row(original_identity, attempt=2, at="2025-01-01T00:00:01+00:00",
                                         result="refused", started_ids=0)
            cases.append(("started-not-last", original, [started_first, refused_last], 1, "STARTED_NOT_LAST"))

            started_second = _selftest_row(original_identity, attempt=2, at="2025-01-01T00:00:01+00:00")
            cases.append(("two-started", original, [started_first, started_second], 1, "DUPLICATE_STARTED"))

            gap_first = _selftest_row(original_identity, attempt=1, result="refused", started_ids=0)
            gap_last = _selftest_row(original_identity, attempt=3, at="2025-01-01T00:00:01+00:00")
            cases.append(("non-contiguous-attempt", original, [gap_first, gap_last], 1, "ATTEMPTS_NONCONTIGUOUS"))

            time_first = _selftest_row(original_identity, attempt=1, at="2025-01-01T00:00:02+00:00",
                                       result="refused", started_ids=0)
            time_last = _selftest_row(original_identity, attempt=2, at="2025-01-01T00:00:01+00:00")
            cases.append(("decreasing-at", original, [time_first, time_last], 1, "AT_DECREASING"))

            bad_ids = _selftest_row(original_identity, started_ids=0)
            cases.append(("started-ids-mismatch", original, [bad_ids], 1, "STARTED_IDS_MISMATCH"))

            legacy = {"attempt": 1, "at": "2025-01-01T00:00:00+00:00", "result": "refused", "started_ids": 0}
            cases.append(("legacy-row", original, [legacy], 1, "LEGACY_ROW_UNBOUND"))

            missing_dispatch = _selftest_row(original_identity, path="absent.json")
            cases.append(("missing-dispatch-path", original, [missing_dispatch], 2,
                          "DISPATCH_PATH_UNAVAILABLE"))

            tool = Path(__file__).resolve()
            for name, dispatch, rows, want_rc, want_id in cases:
                repo = work / name
                _write_fixture_repo(repo, dispatch=dispatch, rows=rows, env=env)
                if not _run_selftest_case(tool, repo, want_rc, want_id, env):
                    failures.append(name)
    except (OSError, RuntimeError, subprocess.SubprocessError):
        return _error("SELFTEST_SETUP_FAILED", "sandbox fixture setup failed")

    total = 11
    passed = total - len(failures)
    if failures:
        sys.stdout.write(
            "SELFTEST mori-dispatch-ledger FAIL %d/%d failed=%s\n"
            % (passed, total, ",".join(failures))
        )
        return RC_FINDINGS
    sys.stdout.write("SELFTEST mori-dispatch-ledger PASS %d/%d\n" % (passed, total))
    return RC_CLEAN


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv == ["--selftest"]:
        return _selftest()

    parser = _JsonArgumentParser(
        description="Bind and verify committed mori dispatch attempt ledgers.",
        allow_abbrev=False,
    )
    subparsers = parser.add_subparsers(dest="command", parser_class=_JsonArgumentParser)
    bind_parser = subparsers.add_parser("bind", allow_abbrev=False)
    bind_parser.add_argument("--repo", required=True)
    bind_parser.add_argument("--rev", required=True)
    bind_parser.add_argument("--dispatch", required=True)
    verify_parser = subparsers.add_parser("verify", allow_abbrev=False)
    verify_parser.add_argument("--repo", required=True)
    verify_parser.add_argument("--rev", required=True)
    verify_parser.add_argument("--ledger", required=True)
    args = parser.parse_args(argv)
    if args.command is None:
        return _error("INPUT_INVALID", "select bind, verify, or --selftest")
    try:
        if args.command == "bind":
            return _emit(_bind(args.repo, args.rev, args.dispatch), RC_CLEAN)
        result, rc = _verify(args.repo, args.rev, args.ledger)
        return _emit(result, rc)
    except EvaluationError as exc:
        return _error(exc.finding_id, exc.reason)


if __name__ == "__main__":
    sys.exit(main())
