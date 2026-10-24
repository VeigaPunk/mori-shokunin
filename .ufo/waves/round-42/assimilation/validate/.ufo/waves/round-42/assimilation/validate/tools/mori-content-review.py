#!/usr/bin/env python3
"""Bounded, content-based review gate for the frozen Mori population."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

POPULATION_SCHEMA = "mori-content-population-v1"
REVIEWS_SCHEMA = "mori-content-reviews-v1"
RESULT_SCHEMA = "mori-content-review-result-v1"
DECISIONS = frozenset(("retain", "minimized", "unresolved"))
CONTENT_BASES = frozenset(("content-reviewed", "provenance-only"))
ROW_FIELDS = frozenset(("path", "blob_sha256", "decision", "content_basis", "reason"))
SHA256_RE = re.compile(r"[0-9a-fA-F]{64}\Z")
OID_RE = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")

INVALID_CODES = frozenset((
    "CONTENT_REVIEW_INVALID_ARGUMENTS",
    "CONTENT_REVIEW_INVALID_REVISION",
    "CONTENT_REVIEW_INPUT_UNAVAILABLE",
    "CONTENT_REVIEW_PATH_UNAVAILABLE",
    "CONTENT_REVIEW_POPULATION_PIN",
    "CONTENT_REVIEW_OUT_OF_POPULATION",
    "CONTENT_REVIEW_DUPLICATE",
    "CONTENT_REVIEW_INVALID",
    "CONTENT_REVIEW_SCRIPT_UNAVAILABLE",
))
FAIL_CODES = frozenset((
    "CONTENT_REVIEW_INCOMPLETE",
    "CONTENT_REVIEW_STALE",
    "CONTENT_REVIEW_UNRESOLVED",
))


class CliUsageError(Exception):
    pass


class DuplicateJsonKey(Exception):
    pass


class SafeArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise CliUsageError


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read_script_digest() -> str | None:
    try:
        return sha256(Path(__file__).resolve(strict=True).read_bytes())
    except OSError:
        return None


def json_object_without_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJsonKey
        result[key] = value
    return result


def parse_json_object(raw: bytes) -> dict[str, object] | None:
    try:
        value = json.loads(raw, object_pairs_hook=json_object_without_duplicate_keys)
    except (UnicodeError, json.JSONDecodeError, DuplicateJsonKey, TypeError, ValueError):
        return None
    return value if isinstance(value, dict) else None


def git_environment() -> dict[str, str]:
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env.update({
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_NO_REPLACE_OBJECTS": "1",
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_TERMINAL_PROMPT": "0",
        "LC_ALL": "C",
    })
    return env


def git_run(repo: Path, args: list[str], config: tuple[tuple[str, str], ...] = ()) -> subprocess.CompletedProcess[bytes] | None:
    command = ["git", "--no-pager"]
    for key, value in config:
        command.extend(("-c", f"{key}={value}"))
    command.extend(("-C", str(repo), *args))
    try:
        return subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
            env=git_environment(),
            timeout=60,
        )
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return None


def resolve_revision(repo: Path, revision: str) -> str | None:
    proc = git_run(repo, ["rev-parse", "--verify", "--end-of-options", f"{revision}^{{commit}}"])
    if proc is None or proc.returncode != 0:
        return None
    try:
        resolved = proc.stdout.decode("ascii").strip()
    except UnicodeError:
        return None
    return resolved if OID_RE.fullmatch(resolved) else None


def valid_repo_path(path: object) -> bool:
    if not isinstance(path, str) or not path or path.startswith("/") or "\x00" in path:
        return False
    parts = path.split("/")
    return all(part not in ("", ".", "..") for part in parts)


def read_blob(repo: Path, revision: str, path: str) -> bytes | None:
    object_name = f"{revision}:{path}"
    kind = git_run(repo, ["cat-file", "-t", object_name])
    if kind is None or kind.returncode != 0 or kind.stdout.strip() != b"blob":
        return None
    content = git_run(repo, ["show", "--no-ext-diff", "--no-textconv", object_name])
    if content is None or content.returncode != 0:
        return None
    return content.stdout


def empty_result(script_digest: str | None) -> dict[str, object]:
    return {
        "schema": RESULT_SCHEMA,
        "status": "could-not-evaluate",
        "exit_code": 2,
        "metadata": {
            "revision": None,
            "population_sha256": None,
            "reviews_sha256": None,
            "script_sha256": script_digest,
            "population_blobs": [],
        },
        "counts": {
            "population_paths": 0,
            "review_rows": 0,
            "blobs_read": 0,
            "findings": 0,
            "finding_codes": {},
        },
        "findings": [],
    }


def add_finding(result: dict[str, object], code: str, path: str | None = None) -> None:
    findings = result["findings"]
    assert isinstance(findings, list)
    finding: dict[str, str] = {"code": code}
    if path is not None:
        finding["path"] = path
    if finding not in findings:
        findings.append(finding)


def finish(result: dict[str, object]) -> tuple[dict[str, object], int]:
    findings = result["findings"]
    assert isinstance(findings, list)
    if not findings:
        findings.append({"code": "CONTENT_REVIEW_CLEAN"})
    findings.sort(key=lambda item: (item.get("path", ""), item["code"]))
    codes: dict[str, int] = {}
    for finding in findings:
        code = finding["code"]
        codes[code] = codes.get(code, 0) + 1
    counts = result["counts"]
    assert isinstance(counts, dict)
    counts["findings"] = len(findings)
    counts["finding_codes"] = dict(sorted(codes.items()))

    if any(finding["code"] in INVALID_CODES for finding in findings):
        status, exit_code = "could-not-evaluate", 2
    elif any(finding["code"] in FAIL_CODES for finding in findings):
        status, exit_code = "failed", 1
    else:
        status, exit_code = "clean", 0
    result["status"] = status
    result["exit_code"] = exit_code
    return result, exit_code


def check(args: argparse.Namespace, script_digest: str | None) -> tuple[dict[str, object], int]:
    result = empty_result(script_digest)
    metadata = result["metadata"]
    counts = result["counts"]
    assert isinstance(metadata, dict) and isinstance(counts, dict)

    if script_digest is None:
        add_finding(result, "CONTENT_REVIEW_SCRIPT_UNAVAILABLE")
        return finish(result)

    try:
        population_raw = Path(args.population).read_bytes()
        reviews_raw = Path(args.reviews).read_bytes()
    except OSError:
        add_finding(result, "CONTENT_REVIEW_INPUT_UNAVAILABLE")
        return finish(result)
    population_digest = sha256(population_raw)
    reviews_digest = sha256(reviews_raw)
    metadata["population_sha256"] = population_digest
    metadata["reviews_sha256"] = reviews_digest

    try:
        repo = Path(args.repo).resolve(strict=True)
    except OSError:
        add_finding(result, "CONTENT_REVIEW_INVALID_REVISION")
        return finish(result)
    if not repo.is_dir():
        add_finding(result, "CONTENT_REVIEW_INVALID_REVISION")
        return finish(result)
    revision = resolve_revision(repo, args.rev)
    if revision is None:
        add_finding(result, "CONTENT_REVIEW_INVALID_REVISION")
        return finish(result)
    metadata["revision"] = revision

    expected_digest = args.expected_sha256
    if not SHA256_RE.fullmatch(expected_digest or "") or population_digest != expected_digest.lower():
        add_finding(result, "CONTENT_REVIEW_POPULATION_PIN")
        return finish(result)

    population = parse_json_object(population_raw)
    reviews = parse_json_object(reviews_raw)
    if population is None or reviews is None:
        add_finding(result, "CONTENT_REVIEW_INVALID")
        return finish(result)
    if population.get("schema") != POPULATION_SCHEMA or not isinstance(population.get("paths"), list):
        add_finding(result, "CONTENT_REVIEW_INVALID")
        return finish(result)
    if reviews.get("schema") != REVIEWS_SCHEMA or not isinstance(reviews.get("rows"), list):
        add_finding(result, "CONTENT_REVIEW_INVALID")
        return finish(result)

    paths_value = population["paths"]
    rows_value = reviews["rows"]
    paths: list[str] = []
    path_set: set[str] = set()
    population_invalid = False
    for path_value in paths_value:
        if not valid_repo_path(path_value) or path_value in path_set:
            population_invalid = True
            continue
        path_set.add(path_value)
        paths.append(path_value)
    counts["population_paths"] = len(paths)
    counts["review_rows"] = len(rows_value)
    if population_invalid:
        add_finding(result, "CONTENT_REVIEW_INVALID")
        return finish(result)

    blob_digests: dict[str, str] = {}
    population_blobs: list[dict[str, str]] = []
    for path in paths:
        content = read_blob(repo, revision, path)
        if content is None:
            add_finding(result, "CONTENT_REVIEW_PATH_UNAVAILABLE", path)
            continue
        digest = sha256(content)
        blob_digests[path] = digest
        population_blobs.append({"path": path, "sha256": digest})
    metadata["population_blobs"] = population_blobs
    counts["blobs_read"] = len(blob_digests)

    invalid = any(finding["code"] == "CONTENT_REVIEW_PATH_UNAVAILABLE" for finding in result["findings"])
    rows_by_path: dict[str, dict[str, object]] = {}
    for row in rows_value:
        if not isinstance(row, dict):
            add_finding(result, "CONTENT_REVIEW_INVALID")
            invalid = True
            continue
        path_value = row.get("path")
        if not isinstance(path_value, str):
            add_finding(result, "CONTENT_REVIEW_INVALID")
            invalid = True
            continue
        if path_value not in path_set:
            add_finding(result, "CONTENT_REVIEW_OUT_OF_POPULATION")
            invalid = True
            continue
        if path_value in rows_by_path:
            add_finding(result, "CONTENT_REVIEW_DUPLICATE", path_value)
            invalid = True
            continue
        rows_by_path[path_value] = row
        if set(row) != ROW_FIELDS:
            add_finding(result, "CONTENT_REVIEW_INVALID", path_value)
            invalid = True
            continue
        blob_sha256 = row.get("blob_sha256")
        decision = row.get("decision")
        content_basis = row.get("content_basis")
        reason = row.get("reason")
        if (
            not isinstance(blob_sha256, str)
            or not SHA256_RE.fullmatch(blob_sha256)
            or not isinstance(decision, str)
            or decision not in DECISIONS
            or not isinstance(content_basis, str)
            or content_basis not in CONTENT_BASES
            or not isinstance(reason, str)
            or not reason.strip()
        ):
            add_finding(result, "CONTENT_REVIEW_INVALID", path_value)
            invalid = True
            continue
        if path_value in blob_digests and blob_sha256.lower() != blob_digests[path_value]:
            add_finding(result, "CONTENT_REVIEW_STALE", path_value)
        if decision == "unresolved" or content_basis == "provenance-only":
            add_finding(result, "CONTENT_REVIEW_UNRESOLVED", path_value)

    for path in paths:
        if path not in rows_by_path:
            add_finding(result, "CONTENT_REVIEW_INCOMPLETE", path)
    if invalid and not any(finding["code"] in INVALID_CODES for finding in result["findings"]):
        add_finding(result, "CONTENT_REVIEW_INVALID")
    return finish(result)


def emit(result: dict[str, object]) -> None:
    sys.stdout.write(json.dumps(result, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n")


def build_parser() -> SafeArgumentParser:
    parser = SafeArgumentParser(prog="mori-content-review.py")
    subparsers = parser.add_subparsers(dest="command", required=True, parser_class=SafeArgumentParser)
    check_parser = subparsers.add_parser("check")
    check_parser.add_argument("--repo", required=True)
    check_parser.add_argument("--rev", required=True)
    check_parser.add_argument("--population", required=True)
    check_parser.add_argument("--reviews", required=True)
    check_parser.add_argument("--expected-sha256", required=True)
    return parser


def selftest_tmpdir() -> Path | None:
    value = os.environ.get("TMPDIR")
    if not value:
        return None
    try:
        tmpdir = Path(value).resolve(strict=True)
        lane_root = Path(__file__).resolve(strict=True).parent.parent
        if not tmpdir.is_dir() or tmpdir == lane_root:
            return None
        if os.path.commonpath((str(lane_root), str(tmpdir))) != str(lane_root):
            return None
        return tmpdir
    except (OSError, ValueError):
        return None


def selftest(script_digest: str | None) -> int:
    if script_digest is None:
        emit({"schema": RESULT_SCHEMA, "status": "could-not-evaluate", "exit_code": 2,
              "findings": [{"code": "CONTENT_REVIEW_SCRIPT_UNAVAILABLE"}]})
        return 2
    tmpdir = selftest_tmpdir()
    if tmpdir is None:
        emit({"schema": RESULT_SCHEMA, "status": "could-not-evaluate", "exit_code": 2,
              "findings": [{"code": "CONTENT_REVIEW_SELFTEST_TMPDIR"}]})
        return 2

    try:
        with tempfile.TemporaryDirectory(prefix="mori-content-review-", dir=tmpdir) as scratch:
            root = Path(scratch)
            repo = root / "repo"
            repo.mkdir()
            (repo / "docs").mkdir()
            (repo / "docs" / "reviewed.md").write_bytes(b"synthetic-private-marker\n")
            init = git_run(repo, ["init", "--quiet"], (("init.templateDir", os.devnull), ("core.hooksPath", os.devnull)))
            if init is None or init.returncode != 0:
                raise RuntimeError
            staged = git_run(repo, ["add", "--", "docs/reviewed.md"])
            if staged is None or staged.returncode != 0:
                raise RuntimeError
            committed = git_run(
                repo,
                ["commit", "--quiet", "--no-verify", "-m", "synthetic fixture"],
                (("user.name", "ContentReviewSelftest"), ("user.email", "selftest@example.invalid"), ("core.hooksPath", os.devnull)),
            )
            if committed is None or committed.returncode != 0:
                raise RuntimeError
            revision = resolve_revision(repo, "HEAD")
            if revision is None:
                raise RuntimeError
            content = b"synthetic-private-marker\n"
            content_digest = sha256(content)
            population_raw = json.dumps({"schema": POPULATION_SCHEMA, "paths": ["docs/reviewed.md"]}).encode()
            population_path = root / "population.json"
            reviews_path = root / "reviews.json"
            population_path.write_bytes(population_raw)
            base_row = {
                "path": "docs/reviewed.md",
                "blob_sha256": content_digest,
                "decision": "retain",
                "content_basis": "content-reviewed",
                "reason": "synthetic safe explanation",
            }
            expected = sha256(population_raw)
            cases = (
                ("complete_safe", [base_row], "HEAD", expected, 0, "CONTENT_REVIEW_CLEAN"),
                ("missing_review", [], "HEAD", expected, 1, "CONTENT_REVIEW_INCOMPLETE"),
                ("duplicate_review", [base_row, base_row], "HEAD", expected, 2, "CONTENT_REVIEW_DUPLICATE"),
                ("unknown_decision", [{**base_row, "decision": "unknown"}], "HEAD", expected, 2, "CONTENT_REVIEW_INVALID"),
                ("digest_drift", [{**base_row, "blob_sha256": "f" * 64}], "HEAD", expected, 1, "CONTENT_REVIEW_STALE"),
                ("private_content", [{**base_row, "decision": "unresolved"}], "HEAD", expected, 1, "CONTENT_REVIEW_UNRESOLVED"),
                ("provenance_only", [{**base_row, "content_basis": "provenance-only"}], "HEAD", expected, 1, "CONTENT_REVIEW_UNRESOLVED"),
                ("out_of_population", [{**base_row, "path": "outside.md"}], "HEAD", expected, 2, "CONTENT_REVIEW_OUT_OF_POPULATION"),
                ("invalid_revision", [base_row], "not-a-commit", expected, 2, "CONTENT_REVIEW_INVALID_REVISION"),
                ("tampered_population_pin", [base_row], "HEAD", "0" * 64, 2, "CONTENT_REVIEW_POPULATION_PIN"),
            )
            for _, rows, rev, pin, expected_exit, expected_code in cases:
                reviews_path.write_bytes(json.dumps({"schema": REVIEWS_SCHEMA, "rows": rows}).encode())
                command = [
                    sys.executable, Path(__file__).resolve(), "check",
                    "--repo", str(repo), "--rev", rev,
                    "--population", str(population_path), "--reviews", str(reviews_path),
                    "--expected-sha256", pin,
                ]
                try:
                    completed = subprocess.run(
                        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        check=False, timeout=60,
                    )
                    stdout = completed.stdout.decode("utf-8")
                    result = json.loads(stdout)
                except (OSError, subprocess.TimeoutExpired, UnicodeError, json.JSONDecodeError):
                    raise RuntimeError
                if not isinstance(result, dict) or completed.returncode != expected_exit or result.get("exit_code") != expected_exit:
                    raise RuntimeError
                findings = result.get("findings")
                if not isinstance(findings, list) or not any(
                    isinstance(item, dict) and item.get("code") == expected_code
                    for item in findings
                ):
                    raise RuntimeError
                if "synthetic-private-marker" in stdout or "synthetic safe explanation" in stdout:
                    raise RuntimeError
    except Exception:
        emit({"schema": RESULT_SCHEMA, "status": "could-not-evaluate", "exit_code": 2,
              "findings": [{"code": "CONTENT_REVIEW_SELFTEST_FAILED"}]})
        return 2

    emit({"schema": RESULT_SCHEMA, "status": "clean", "exit_code": 0,
          "findings": [{"code": "CONTENT_REVIEW_SELFTEST_CLEAN"}]})
    return 0


def main(argv: list[str] | None = None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    script_digest = read_script_digest()
    if arguments == ["--selftest"]:
        return selftest(script_digest)
    try:
        args = build_parser().parse_args(arguments)
    except CliUsageError:
        result = empty_result(script_digest)
        add_finding(result, "CONTENT_REVIEW_INVALID_ARGUMENTS")
        completed, exit_code = finish(result)
        emit(completed)
        return exit_code
    if args.command != "check":
        result = empty_result(script_digest)
        add_finding(result, "CONTENT_REVIEW_INVALID_ARGUMENTS")
        completed, exit_code = finish(result)
        emit(completed)
        return exit_code
    result, exit_code = check(args, script_digest)
    emit(result)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
