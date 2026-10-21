#!/usr/bin/env python3
"""Independent synthetic audit fixtures for Mori round 21.

The target is invoked only as a subprocess through its public ``audit`` CLI;
this runner never imports target code. All evidence trees and local commits are
created beneath the caller's TMPDIR and removed afterward. The output is a
machine-readable receipt containing every invocation's observed status, counts,
finding identifiers, and captured stdout/stderr.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any

SCHEMA = "mori-evidence-loss-fixture-loss-v1"
AUDIT_SCHEMA = "mori-evidence-loss-audit-v1"
REQUIRED_SCHEMA = "mori-required-observations-v1"
ACCOUNTING_SCHEMA = "mori-loss-accounting-v1"
BASE_REVISION = "e9f340ce986f82a60baad1b8e5ead655ab818a1c"
OBSERVATION_ID = "fixture-wave-observation"
CLEANUP_ACTOR = "fixture-cleanup-actor"
INDEPENDENT_ACTOR = "fixture-independent-actor"
WAVE_ID = "fixture-wave-21"
COUNT_KEYS = ("omitted", "retained", "unresolved", "disposed", "invalid")
TOOL_TIMEOUT_SECONDS = 30
OUTPUT_LIMIT_BYTES = 1024 * 1024
SHA_RE = re.compile(r"^[0-9a-f]{40}(?:[0-9a-f]{24})?$")


class HarnessError(Exception):
    """A bounded runner setup error safe to include in the receipt."""


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate-json-key")
        result[key] = value
    return result


def reject_constant(_value: str) -> None:
    raise ValueError("non-json-number")


def parse_json(data: bytes) -> Any:
    return json.loads(data.decode("utf-8"), object_pairs_hook=strict_object,
                      parse_constant=reject_constant)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def clean_environment(home: Path, tmpdir: Path) -> dict[str, str]:
    home.mkdir(parents=True, exist_ok=True)
    tmpdir.mkdir(parents=True, exist_ok=True)
    return {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "HOME": str(home),
        "TMPDIR": str(tmpdir),
        "LC_ALL": "C",
        "LANG": "C",
        "TZ": "UTC",
        "PYTHONNOUSERSITE": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_SYSTEM": os.devnull,
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_TERMINAL_PROMPT": "0",
    }


def run_git(root: Path, args: list[str], env: dict[str, str]) -> bytes:
    command = [
        "git", "--no-optional-locks", "-c", "core.fsmonitor=false",
        "-c", "user.name=Round 21 synthetic fixture",
        "-c", "user.email=round21-fixture@example.invalid",
        "-C", str(root), *args,
    ]
    try:
        proc = subprocess.run(command, stdin=subprocess.DEVNULL,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              env=env, timeout=30, check=False)
    except (OSError, subprocess.SubprocessError):
        raise HarnessError("synthetic-git-unavailable-or-failed") from None
    if proc.returncode != 0:
        raise HarnessError("synthetic-git-operation-failed")
    return proc.stdout


def safe_repo_path(relative: str) -> PurePosixPath:
    path = PurePosixPath(relative)
    if (not relative or path.is_absolute() or ".." in path.parts
            or any(part in ("", ".") for part in path.parts)):
        raise HarnessError("unsafe-internal-fixture-path")
    return path


def fixture_artifacts(case_name: str) -> dict[str, bytes]:
    disposition_actor = (
        CLEANUP_ACTOR if case_name == "same-actor-cleanup-only"
        else INDEPENDENT_ACTOR
    )
    disposition_independent = case_name != "false-independent-boolean"
    records = {
        "evidence/required-baseline.json": {
            "fixture": True, "kind": "required-baseline",
            "observation": OBSERVATION_ID,
        },
        "evidence/required-evidence.json": {
            "fixture": True, "kind": "required-evidence",
            "observation": OBSERVATION_ID,
        },
        "evidence/row-baseline.json": {
            "fixture": True, "kind": "baseline",
            "observation": OBSERVATION_ID,
        },
        "evidence/row-deletion.json": {
            "fixture": True, "kind": "deletion",
            "observation": OBSERVATION_ID,
        },
        "evidence/row-cleanup.json": {
            "actor": CLEANUP_ACTOR, "fixture": True,
            "kind": "cleanup", "observation": OBSERVATION_ID,
        },
        "evidence/row-disposition.json": {
            "actor": disposition_actor,
            "disposition": "settlement",
            "id": OBSERVATION_ID,
            "independent": disposition_independent,
            "fixture": True,
            "kind": "independent-disposition",
            "wave_id": WAVE_ID,
        },
    }
    return {name: canonical_json(value) for name, value in records.items()}


def create_committed_root(root: Path, artifacts: dict[str, bytes],
                          env: dict[str, str]) -> str:
    root.mkdir(parents=True, exist_ok=False)
    run_git(root, ["init", "--quiet", "--initial-branch=main"], env)
    for relative, content in artifacts.items():
        path = root.joinpath(*safe_repo_path(relative).parts)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    run_git(root, ["add", "--", "evidence"], env)
    run_git(root, ["commit", "--quiet", "-m", "synthetic round 21 evidence"], env)
    revision = run_git(root, ["rev-parse", "HEAD"], env).decode("ascii").strip()
    if SHA_RE.fullmatch(revision) is None:
        raise HarnessError("synthetic-git-returned-invalid-revision")
    return revision


def provenance(relative: str, artifacts: dict[str, bytes], revision: str) -> dict[str, str]:
    safe_repo_path(relative)
    return {"path": relative, "revision": revision,
            "sha256": sha256(artifacts[relative])}


def fixture_documents(case_name: str, root: Path, artifacts: dict[str, bytes],
                      revision: str) -> tuple[dict[str, Any], dict[str, Any]]:
    disposition_actor = (
        CLEANUP_ACTOR if case_name == "same-actor-cleanup-only"
        else INDEPENDENT_ACTOR
    )
    disposition_independent = case_name != "false-independent-boolean"
    required = {
        "schema": REQUIRED_SCHEMA,
        "observations": [{
            "id": OBSERVATION_ID,
            "baseline": provenance("evidence/required-baseline.json", artifacts, revision),
            "evidence": "evidence/required-evidence.json:1",
        }],
    }
    row: dict[str, Any] = {
        "id": OBSERVATION_ID,
        "state": "disposed",
        "baseline": provenance(
            "evidence/row-baseline.json" if case_name == "wrong-baseline-v0"
            else "evidence/required-baseline.json", artifacts, revision),
        "deletion": provenance("evidence/row-deletion.json", artifacts, revision),
        "cleanup": provenance("evidence/row-cleanup.json", artifacts, revision),
        "independent_disposition": {
            **provenance("evidence/row-disposition.json", artifacts, revision),
            "independent": disposition_independent,
            "actor": disposition_actor,
            "wave_id": WAVE_ID,
            "disposition": "settlement",
        },
    }
    observations: list[dict[str, Any]] = [row]
    if case_name == "absent-required-observation":
        observations = []
    elif case_name == "retained-unresolved":
        row["state"] = "unresolved"
        row["independent_disposition"] = None
    elif case_name == "duplicate-accounting-id":
        observations.append(json.loads(json.dumps(row)))
    elif case_name == "false-independent-boolean":
        row["independent_disposition"]["independent"] = False
    elif case_name == "same-actor-cleanup-only":
        row["independent_disposition"]["actor"] = CLEANUP_ACTOR
    elif case_name == "absolute-evidence-path":
        row["independent_disposition"]["path"] = str(
            root / "evidence/row-disposition.json")
    elif case_name == "parent-evidence-path":
        row["independent_disposition"]["path"] = "../outside-disposition.json"
    elif case_name == "missing-evidence-file":
        row["independent_disposition"]["path"] = "evidence/not-present.json"
    elif case_name in (
        "digest-tamper", "symlink-escape", "valid-independently-disposed",
        "wrong-baseline-v0",
    ):
        pass
    else:
        raise HarnessError("unknown-fixture-case")
    accounting = {"schema": ACCOUNTING_SCHEMA, "observations": observations}
    return required, accounting


def apply_filesystem_mutation(case_name: str, case_dir: Path, root: Path,
                              artifacts: dict[str, bytes]) -> None:
    disposition = root / "evidence/row-disposition.json"
    if case_name == "digest-tamper":
        # Preserve valid JSON while making the committed byte digest stale.
        disposition.write_bytes(disposition.read_bytes() + b" ")
    elif case_name == "symlink-escape":
        outside = case_dir / "outside-disposition.json"
        outside.write_bytes(artifacts["evidence/row-disposition.json"])
        disposition.unlink()
        disposition.symlink_to(outside)


def expected_cases() -> list[dict[str, Any]]:
    return [
        {
            "id": "absent-required-observation", "expected_rc": 1,
            "exact": {"omitted": 1, "retained": 0, "unresolved": 0,
                      "disposed": 0, "invalid": 0, "pin_allowed": False},
        },
        {
            "id": "retained-unresolved", "expected_rc": 1,
            "exact": {"omitted": 0, "retained": 1, "unresolved": 1,
                      "disposed": 0, "invalid": 0, "pin_allowed": False},
        },
        {
            "id": "valid-independently-disposed", "expected_rc": 0,
            "exact": {"omitted": 0, "retained": 1, "unresolved": 0,
                      "disposed": 1, "invalid": 0, "pin_allowed": True},
        },
        {
            "id": "wrong-baseline-v0", "expected_rc": 1,
            "exact": {"disposed": 0, "pin_allowed": False},
            "minimum": {"invalid": 1, "unresolved": 1},
        },
        {
            "id": "digest-tamper", "expected_rc": 1,
            "exact": {"disposed": 0, "pin_allowed": False},
            "minimum": {"invalid": 1, "unresolved": 1},
        },
        {
            "id": "duplicate-accounting-id", "expected_rc": 1,
            "exact": {"disposed": 0, "pin_allowed": False},
            "minimum": {"invalid": 1, "unresolved": 1},
        },
        {
            "id": "symlink-escape", "expected_rc": 1,
            "exact": {"disposed": 0, "pin_allowed": False},
            "minimum": {"invalid": 1, "unresolved": 1},
        },
        {
            "id": "absolute-evidence-path", "expected_rc": 1,
            "exact": {"disposed": 0, "pin_allowed": False},
            "minimum": {"invalid": 1, "unresolved": 1},
        },
        {
            "id": "parent-evidence-path", "expected_rc": 1,
            "exact": {"disposed": 0, "pin_allowed": False},
            "minimum": {"invalid": 1, "unresolved": 1},
        },
        {
            "id": "false-independent-boolean", "expected_rc": 1,
            "exact": {"disposed": 0, "pin_allowed": False},
            "minimum": {"unresolved": 1},
        },
        {
            "id": "same-actor-cleanup-only", "expected_rc": 1,
            "exact": {"disposed": 0, "pin_allowed": False},
            "minimum": {"unresolved": 1},
        },
        {
            "id": "missing-evidence-file", "expected_rc": 1,
            "exact": {"disposed": 0, "pin_allowed": False},
            "minimum": {"invalid": 1, "unresolved": 1},
        },
    ]


def finding_ids(value: Any) -> tuple[list[str], list[str]]:
    ids: list[str] = []
    errors: list[str] = []

    def visit(item: Any) -> None:
        if isinstance(item, dict):
            if "finding_id" in item:
                identifier = item["finding_id"]
                if not isinstance(identifier, str) or not identifier:
                    errors.append("finding-id-not-nonempty-string")
                else:
                    ids.append(identifier)
            for child in item.values():
                visit(child)
        elif isinstance(item, list):
            for child in item:
                visit(child)

    visit(value)
    return sorted(ids), errors


def parse_audit_output(stdout: bytes) -> tuple[dict[str, Any] | None, list[str]]:
    errors: list[str] = []
    try:
        value = parse_json(stdout)
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError):
        return None, ["stdout-not-strict-json"]
    if not isinstance(value, dict) or value.get("schema") != AUDIT_SCHEMA:
        return None, ["unexpected-audit-schema"]
    if not isinstance(value.get("issues"), list):
        errors.append("issues-not-list")
    for key in COUNT_KEYS:
        count = value.get(key)
        if not isinstance(count, int) or isinstance(count, bool) or count < 0:
            errors.append("%s-not-nonnegative-integer" % key)
    if not isinstance(value.get("pin_allowed"), bool):
        errors.append("pin-allowed-not-boolean")
    ids, id_errors = finding_ids(value)
    errors.extend(id_errors)
    if value.get("issues") and isinstance(value["issues"], list):
        for issue in value["issues"]:
            if not isinstance(issue, dict):
                errors.append("issue-not-object")
            elif "finding_id" not in issue:
                errors.append("issue-missing-finding-id")
    value["_runner_finding_ids"] = ids
    return value, errors


def observed_counts(value: dict[str, Any] | None) -> dict[str, Any] | None:
    if value is None:
        return None
    result: dict[str, Any] = {key: value.get(key) for key in COUNT_KEYS}
    result["pin_allowed"] = value.get("pin_allowed")
    return result


def bounded_output(data: bytes) -> dict[str, Any]:
    prefix = data[:OUTPUT_LIMIT_BYTES]
    return {
        "text": prefix.decode("utf-8", errors="replace"),
        "byte_length": len(data),
        "sha256": sha256(data),
        "truncated": len(data) > OUTPUT_LIMIT_BYTES,
    }


def invoke_tool(tool: Path, root: Path, required: Path, accounting: Path,
                case_dir: Path, env: dict[str, str]) -> dict[str, Any]:
    argv = [sys.executable, str(tool), "audit", "--root", str(root),
            "--required", str(required), "--accounting", str(accounting)]
    try:
        proc = subprocess.run(argv, cwd=case_dir, env=env,
                              stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, timeout=TOOL_TIMEOUT_SECONDS,
                              check=False)
        rc: int | None = proc.returncode
        stdout = proc.stdout
        stderr = proc.stderr
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        rc = None
        stdout = exc.stdout or b""
        stderr = exc.stderr or b""
        timed_out = True
    except OSError as exc:
        rc = None
        stdout = b""
        stderr = str(exc).encode("utf-8", errors="replace")
        timed_out = False
    document, parse_errors = parse_audit_output(stdout) if not timed_out and rc is not None else (None, [])
    if timed_out:
        parse_errors.append("tool-timeout")
    if rc is None and not timed_out:
        parse_errors.append("tool-launch-failed")
    if len(stdout) > OUTPUT_LIMIT_BYTES or len(stderr) > OUTPUT_LIMIT_BYTES:
        parse_errors.append("captured-output-exceeds-limit")
    return {
        "argv": argv,
        "rc": rc,
        "timed_out": timed_out,
        "counts": observed_counts(document),
        "finding_ids": document.get("_runner_finding_ids", []) if document else [],
        "parse_errors": parse_errors,
        "stdout": bounded_output(stdout),
        "stderr": bounded_output(stderr),
    }


def add_check(case_result: dict[str, Any], check: str,
              passed: bool, expected: Any, actual: Any) -> None:
    case_result["checks"].append({
        "check": check, "passed": passed,
        "expected": expected, "actual": actual,
    })
    if not passed:
        case_result["failures"].append({
            "check": check, "expected": expected, "actual": actual,
        })


def run_case(tool: Path, parent: Path, case_spec: dict[str, Any]) -> dict[str, Any]:
    name = case_spec["id"]
    case_dir = parent / name
    case_dir.mkdir(parents=False, exist_ok=False)
    root = case_dir / "evidence-root"
    home = case_dir / "home"
    tool_tmp = case_dir / "tmp"
    env = clean_environment(home, tool_tmp)
    artifacts = fixture_artifacts(name)
    revision = create_committed_root(root, artifacts, env)
    required_doc, accounting_doc = fixture_documents(name, root, artifacts, revision)
    required_path = case_dir / "required.json"
    accounting_path = case_dir / "accounting.json"
    required_path.write_bytes(canonical_json(required_doc))
    accounting_path.write_bytes(canonical_json(accounting_doc))
    apply_filesystem_mutation(name, case_dir, root, artifacts)
    if name == "parent-evidence-path":
        (case_dir / "outside-disposition.json").write_bytes(
            artifacts["evidence/row-disposition.json"])

    case_result: dict[str, Any] = {
        "id": name,
        "expected_rc": case_spec["expected_rc"],
        "expected_counts": {
            "exact": case_spec.get("exact", {}),
            "minimum": case_spec.get("minimum", {}),
        },
        "runs": [],
        "checks": [],
        "failures": [],
    }
    for _run_number in range(2):
        case_result["runs"].append(invoke_tool(
            tool, root, required_path, accounting_path, case_dir, env))

    for index, run in enumerate(case_result["runs"], start=1):
        prefix = "run-%d" % index
        add_check(case_result, prefix + "-expected-rc",
                  run["rc"] == case_spec["expected_rc"],
                  case_spec["expected_rc"], run["rc"])
        add_check(case_result, prefix + "-valid-output",
                  not run["parse_errors"], "valid audit JSON", run["parse_errors"])
        add_check(case_result, prefix + "-stdout-not-truncated",
                  not run["stdout"]["truncated"], False, run["stdout"]["truncated"])
        add_check(case_result, prefix + "-stderr-not-truncated",
                  not run["stderr"]["truncated"], False, run["stderr"]["truncated"])
        if run["rc"] == 1:
            add_check(case_result, prefix + "-finding-id-present",
                      bool(run["finding_ids"]), "at least one stable finding_id",
                      run["finding_ids"])
        counts = run["counts"]
        if counts is not None:
            for key, expected in case_spec.get("exact", {}).items():
                add_check(case_result, prefix + "-count-" + key,
                          counts.get(key) == expected, expected, counts.get(key))
            for key, minimum in case_spec.get("minimum", {}).items():
                actual = counts.get(key)
                add_check(case_result, prefix + "-minimum-" + key,
                          isinstance(actual, int) and not isinstance(actual, bool)
                          and actual >= minimum,
                          {"at_least": minimum}, actual)

    first, second = case_result["runs"]
    add_check(case_result, "stable-counts-across-identical-runs",
              first["counts"] == second["counts"], first["counts"], second["counts"])
    add_check(case_result, "stable-finding-ids-across-identical-runs",
              first["finding_ids"] == second["finding_ids"],
              first["finding_ids"], second["finding_ids"])
    case_result["status"] = "pass" if not case_result["failures"] else "fail"
    return case_result


def tool_path(raw: str) -> tuple[Path, str]:
    candidate = Path(raw)
    if not candidate.is_absolute():
        raise HarnessError("tool-path-must-be-absolute")
    try:
        info = candidate.lstat()
    except OSError:
        raise HarnessError("tool-path-unavailable") from None
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
        raise HarnessError("tool-path-not-regular-file")
    resolved = candidate.resolve(strict=True)
    try:
        digest = sha256(resolved.read_bytes())
    except OSError:
        raise HarnessError("tool-path-unreadable") from None
    return resolved, digest


def output_path(raw: str, inputs: list[Path]) -> Path:
    path = Path(raw)
    if not path.is_absolute():
        raise HarnessError("output-path-must-be-absolute")
    try:
        parent = path.parent.resolve(strict=True)
    except OSError:
        raise HarnessError("output-parent-unavailable") from None
    target = parent / path.name
    if target.exists() or target.is_symlink():
        raise HarnessError("output-must-be-absent")
    for item in inputs:
        if target == item.resolve(strict=False):
            raise HarnessError("output-overlaps-input")
    return target


def tmpdir_path() -> Path:
    raw = os.environ.get("TMPDIR")
    if not raw:
        raise HarnessError("TMPDIR-required")
    path = Path(raw)
    if not path.is_absolute():
        raise HarnessError("TMPDIR-must-be-absolute")
    try:
        info = path.lstat()
        resolved = path.resolve(strict=True)
    except OSError:
        raise HarnessError("TMPDIR-unavailable") from None
    if stat.S_ISLNK(info.st_mode) or not resolved.is_dir():
        raise HarnessError("TMPDIR-must-be-real-directory")
    return resolved


def write_report(path: Path, value: dict[str, Any]) -> None:
    payload = canonical_json(value)
    try:
        with path.open("xb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
    except OSError:
        raise HarnessError("output-write-failed") from None


def run_harness(tool: Path, tool_sha256: str, output: Path,
                tmpdir: Path) -> tuple[dict[str, Any], int]:
    report: dict[str, Any] = {
        "schema": SCHEMA,
        "base_revision": BASE_REVISION,
        "tool": {"path": str(tool), "sha256": tool_sha256},
        "status": "running",
        "case_count": 0,
        "passed": 0,
        "failed": 0,
        "cases": [],
        "notes": [
            "Synthetic fixtures only; no target-source imports or production writes.",
            "finding_id literals are not named by the contract; each emitted ID is required nonempty and compared across identical reruns.",
            "For malformed rows, the contract does not define whether invalid counts per row or per issue; minimum counts plus exact rc/pin/disposed invariants are asserted.",
            "All controls except wrong-baseline-v0 reuse the exact required baseline provenance; that case retains the original candidate's different baseline as a negative control.",
        ],
    }
    try:
        with tempfile.TemporaryDirectory(prefix="mori-r21-fixture-loss-",
                                         dir=str(tmpdir)) as raw_workspace:
            workspace = Path(raw_workspace)
            case_specs = expected_cases()
            for spec in case_specs:
                try:
                    result = run_case(tool, workspace, spec)
                except HarnessError as exc:
                    result = {
                        "id": spec["id"], "status": "setup-error",
                        "setup_error": str(exc), "checks": [],
                        "failures": [{"check": "fixture-setup",
                                      "expected": "fixture ready",
                                      "actual": str(exc)}],
                    }
                report["cases"].append(result)
    except OSError as exc:
        report["status"] = "setup-error"
        report["setup_error"] = "workspace-setup-failed:%s" % type(exc).__name__
        report["failed"] = 1
        report["case_count"] = len(report["cases"])
        return report, 2
    report["case_count"] = len(report["cases"])
    report["passed"] = sum(item.get("status") == "pass" for item in report["cases"])
    report["failed"] = sum(item.get("status") != "pass" for item in report["cases"])
    report["status"] = "pass" if report["failed"] == 0 else "fail"
    return report, 0 if report["failed"] == 0 else 1


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", required=True, metavar="PATH")
    parser.add_argument("--output", required=True, metavar="FILE")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report: dict[str, Any]
    exit_code = 2
    output: Path | None = None
    try:
        tool, tool_sha = tool_path(args.tool)
        output = output_path(args.output, [tool, Path(__file__).resolve(strict=True)])
        tmpdir = tmpdir_path()
        report, exit_code = run_harness(tool, tool_sha, output, tmpdir)
    except HarnessError as exc:
        report = {
            "schema": SCHEMA, "base_revision": BASE_REVISION,
            "status": "setup-error", "setup_error": str(exc),
            "case_count": 0, "passed": 0, "failed": 1, "cases": [],
        }
    if output is not None:
        try:
            write_report(output, report)
        except HarnessError as exc:
            report["status"] = "setup-error"
            report["setup_error"] = str(exc)
            exit_code = 2
    print(json.dumps({
        "schema": report.get("schema"), "status": report.get("status"),
        "case_count": report.get("case_count", 0),
        "passed": report.get("passed", 0), "failed": report.get("failed", 0),
        "output": str(output) if output is not None else None,
        "setup_error": report.get("setup_error"),
    }, sort_keys=True, separators=(",", ":")))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
