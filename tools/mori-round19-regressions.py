#!/usr/bin/env python3
"""Independent synthetic regression harness for mori round 19.

Only the committed expected.json is an oracle.  Every repository inspected by a
child tool is created under the caller's explicit TMPDIR and contains synthetic
files and commits.  Captured child output is parsed in memory and represented in
the receipt only by return codes, safe finding codes, counts and full SHA-256
values; raw stdout, stderr, review reasons and fixture values are never saved.
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

ORACLE_REVISION = "5e393d20daa628a0b4ca9aa6a1626aa54285b3f0"
ORACLE_RELATIVE_PATH = ".ufo/waves/round-19/frozen/expected.json"
EXPECTED_SCHEMA = "mori-r19-expected-v1"
C1_CASE_NAMES = (
    "complete_safe",
    "missing_review",
    "duplicate_review",
    "unknown_decision",
    "digest_drift",
    "private_content",
    "provenance_only",
    "out_of_population",
    "invalid_revision",
    "tampered_population_pin",
)
C2_CHECK_NAMES = (
    "measured_revision_full_oid",
    "register_sha256",
    "corrections_sha256",
    "script_sha256",
    "resolved_base_per_claim",
    "resolved_tip_per_claim",
    "override_recorded",
    "command_argv",
    "register_digest_matches_loaded_bytes",
    "same_verdicts_as_base",
    "no_private_values",
    "invalid_revision_could_not_evaluate",
)
OID_RE = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
PRIVATE_SENTINEL = "SYNTHETIC_PRIVATE_SENTINEL_R19"
GIT_TIMEOUT = 60
TOOL_TIMEOUT = 60


class HarnessError(Exception):
    """A setup error that can be safely summarized without source values."""



def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate-key")
        result[key] = value
    return result


def reject_constant(_value: str) -> None:
    raise ValueError("invalid-number")


def json_load_bytes(data: bytes) -> Any:
    return json.loads(
        data.decode("utf-8"),
        object_pairs_hook=strict_object,
        parse_constant=reject_constant,
    )


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def clean_env(home: Path, tmpdir: Path) -> dict[str, str]:
    env: dict[str, str] = {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "HOME": str(home),
        "TMPDIR": str(tmpdir),
        "LC_ALL": "C",
        "LANG": "C",
        "TZ": "UTC",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_SYSTEM": os.devnull,
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_TERMINAL_PROMPT": "0",
    }
    return env


def run_git(repo: Path, args: list[str], env: dict[str, str],
            *, timeout: int = GIT_TIMEOUT) -> bytes:
    argv = [
        "git", "--no-optional-locks", "-c", "core.fsmonitor=false",
        "-c", "user.name=Round 19 synthetic fixture",
        "-c", "user.email=round19-fixture@example.invalid",
        "-C", str(repo), *args,
    ]
    try:
        proc = subprocess.run(
            argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, env=env, timeout=timeout, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        raise HarnessError("synthetic-git-unavailable") from None
    if proc.returncode != 0:
        raise HarnessError("synthetic-git-operation-failed")
    return proc.stdout


def init_repo(repo: Path, env: dict[str, str]) -> None:
    repo.mkdir(parents=True, exist_ok=False)
    argv = [
        "git", "--no-optional-locks", "-c", "core.fsmonitor=false",
        "-c", "init.defaultBranch=main", "-C", str(repo), "init", "-q",
    ]
    try:
        proc = subprocess.run(
            argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, env=env, timeout=GIT_TIMEOUT, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        raise HarnessError("synthetic-git-unavailable") from None
    if proc.returncode != 0:
        raise HarnessError("synthetic-git-init-failed")


def safe_repo_path(relative: str) -> PurePosixPath:
    path = PurePosixPath(relative)
    if (not relative or path.is_absolute() or "\\" in relative
            or any(part in ("", ".", "..") for part in path.parts)):
        raise HarnessError("unsafe-synthetic-path")
    return path


def commit_files(repo: Path, files: dict[str, bytes], message: str,
                 env: dict[str, str]) -> str:
    for relative, content in files.items():
        parts = safe_repo_path(relative)
        target = repo.joinpath(*parts.parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    run_git(repo, ["add", "-A"], env)
    run_git(repo, ["commit", "-q", "-m", message], env)
    return run_git(repo, ["rev-parse", "HEAD"], env).decode("ascii").strip()


def tool_environment(home: Path, tmpdir: Path) -> dict[str, str]:
    home.mkdir(parents=True, exist_ok=True)
    return clean_env(home, tmpdir)


def run_tool(script: Path, arguments: list[str], cwd: Path,
             home: Path, tmpdir: Path) -> tuple[subprocess.CompletedProcess[bytes] | None, str | None]:
    if not script.is_file() or script.is_symlink():
        return None, "tool-absent"
    argv = [sys.executable, str(script), *arguments]
    try:
        proc = subprocess.run(
            argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, cwd=cwd,
            env=tool_environment(home, tmpdir), timeout=TOOL_TIMEOUT,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or b""
        stderr = exc.stderr or b""
        return subprocess.CompletedProcess(argv, 124, stdout, stderr), "timeout"
    except (OSError, subprocess.SubprocessError):
        return None, "tool-could-not-start"
    return proc, None


def process_receipt(proc: subprocess.CompletedProcess[bytes] | None,
                    failure: str | None = None) -> dict[str, Any]:
    if proc is None:
        return {"exit_code": None, "launch": failure}
    return {
        "exit_code": proc.returncode,
        "stdout_bytes": len(proc.stdout),
        "stdout_sha256": sha256_bytes(proc.stdout),
        "stderr_bytes": len(proc.stderr),
        "stderr_sha256": sha256_bytes(proc.stderr),
        **({"launch": failure} if failure else {}),
    }


def parsed_stdout(proc: subprocess.CompletedProcess[bytes] | None) -> dict[str, Any] | None:
    if proc is None:
        return None
    try:
        value = json_load_bytes(proc.stdout)
    except (UnicodeError, json.JSONDecodeError, ValueError):
        return None
    return value if isinstance(value, dict) else None


def marker_leaked(proc: subprocess.CompletedProcess[bytes] | None) -> bool:
    if proc is None:
        return False
    marker = PRIVATE_SENTINEL.encode("utf-8")
    return marker in proc.stdout or marker in proc.stderr


def c1_output_valid(data: dict[str, Any], *, revision: str | None,
                    population_sha: str, reviews_sha: str,
                    script_sha: str) -> bool:
    # These are the exact public receipt fields described by the contract.
    required = {
        "revision": revision,
        "population_sha256": population_sha,
        "reviews_sha256": reviews_sha,
        "script_sha256": script_sha,
    }
    metadata = data.get("metadata")
    if not isinstance(metadata, dict):
        return False
    if any(metadata.get(key) != value for key, value in required.items()):
        return False
    counts = data.get("counts")
    findings = data.get("findings")
    if not isinstance(counts, dict) or not isinstance(findings, list):
        return False
    for key in ("population_paths", "review_rows", "blobs_read", "findings"):
        if type(counts.get(key)) is not int or counts[key] < 0:
            return False
    if counts["findings"] != len(findings):
        return False
    for row in findings:
        if (not isinstance(row, dict)
                or not isinstance(row.get("code"), str)
                or set(row) - {"path", "code"}
                or ("path" in row and not isinstance(row["path"], str))):
            return False
    if data.get("status") not in (None, "clean", "failed", "could-not-evaluate"):
        return False
    return True


def c1_code_present(data: dict[str, Any], code: str,
                    expected_path: str | None) -> bool:
    rows = data.get("findings")
    if not isinstance(rows, list):
        return False
    return any(
        isinstance(row, dict)
        and row.get("code") == code
        and (expected_path is None or row.get("path") == expected_path)
        for row in rows
    )


def c1_fixture_payloads(repo_revision: str) -> dict[str, Any]:
    paths = ["synthetic/alpha.txt", "synthetic/beta.txt"]
    population = {
        "schema": "mori-content-population-v1",
        "base": repo_revision,
        "paths": paths,
    }
    blob_data = {
        "synthetic/alpha.txt": b"synthetic retained review fixture alpha\n",
        "synthetic/beta.txt": b"synthetic retained review fixture beta\n",
    }
    safe_rows = [
        {
            "path": path,
            "blob_sha256": sha256_bytes(blob_data[path]),
            "decision": "retain",
            "content_basis": "content-reviewed",
            "reason": "Synthetic safe review fixture.",
        }
        for path in paths
    ]
    return {
        "paths": paths,
        "population": population,
        "blob_data": blob_data,
        "safe_rows": safe_rows,
    }


def c1_case_rows(expected: dict[str, Any], tool: Path, repo: Path,
                 revision: str, root: Path, tmpdir: Path,
                 tool_sha: str | None) -> list[dict[str, Any]]:
    expected_codes = expected["c1_cases"]
    required_findings = expected.get("c1_required_finding", {})
    fixtures = c1_fixture_payloads(revision)
    paths = fixtures["paths"]
    safe_rows = fixtures["safe_rows"]
    path_for_case = {
        "missing_review": "synthetic/beta.txt",
        "digest_drift": "synthetic/alpha.txt",
        "private_content": "synthetic/beta.txt",
        "provenance_only": "synthetic/alpha.txt",
    }
    cases: list[dict[str, Any]] = []
    case_root = root / "c1-inputs"
    case_root.mkdir()
    for case_name in C1_CASE_NAMES:
        population = dict(fixtures["population"])
        rows = [dict(row) for row in safe_rows]
        revision_arg = revision
        expected_pin = ""
        if case_name == "missing_review":
            rows = rows[:1]
        elif case_name == "duplicate_review":
            rows.append(dict(rows[0]))
        elif case_name == "unknown_decision":
            rows[0]["decision"] = "unknown-synthetic-decision"
        elif case_name == "digest_drift":
            rows[0]["blob_sha256"] = sha256_bytes(b"different synthetic bytes\n")
        elif case_name == "private_content":
            rows[1]["decision"] = "unresolved"
            rows[1]["reason"] = "Synthetic disposition marker " + PRIVATE_SENTINEL
        elif case_name == "provenance_only":
            rows[0]["content_basis"] = "provenance-only"
        elif case_name == "out_of_population":
            rows.append({
                "path": "synthetic/not-in-population.txt",
                "blob_sha256": sha256_bytes(b"synthetic extra row\n"),
                "decision": "retain",
                "content_basis": "content-reviewed",
                "reason": "Synthetic extra row.",
            })
        elif case_name == "invalid_revision":
            revision_arg = "round19-invalid-synthetic-revision"
        elif case_name == "tampered_population_pin":
            pass
        population_bytes = canonical_json(population)
        reviews_bytes = canonical_json({
            "schema": "mori-content-reviews-v1",
            "rows": rows,
        })
        population_sha = sha256_bytes(population_bytes)
        reviews_sha = sha256_bytes(reviews_bytes)
        population_path = case_root / (case_name + ".population.json")
        reviews_path = case_root / (case_name + ".reviews.json")
        population_path.write_bytes(population_bytes)
        reviews_path.write_bytes(reviews_bytes)
        expected_pin = population_sha
        if case_name == "tampered_population_pin":
            expected_pin = "0" * 64
        args = [
            "check", "--repo", str(repo), "--rev", revision_arg,
            "--population", str(population_path),
            "--reviews", str(reviews_path),
            "--expected-sha256", expected_pin,
        ]
        proc, launch_failure = run_tool(
            tool, args, root, root / ("home-c1-" + case_name), tmpdir,
        )
        actual = parsed_stdout(proc)
        want_rc = expected_codes[case_name]
        issues: list[str] = []
        if launch_failure:
            issues.append("tool-launch")
        elif proc is None or proc.returncode != want_rc:
            issues.append("exit-code")
        if proc is not None:
            forbidden = [PRIVATE_SENTINEL, *[row["reason"] for row in rows],
                         *[raw.decode().strip() for raw in fixtures["blob_data"].values()]]
            if any(token.encode() in proc.stdout or token.encode() in proc.stderr
                   for token in forbidden):
                issues.append("private-value-leak")
        if proc is not None and actual is None:
            issues.append("invalid-json-result")
        if proc is not None and actual is not None:
            if tool_sha is not None:
                if not c1_output_valid(
                    actual, revision=None if case_name == "invalid_revision" else revision,
                    population_sha=population_sha,
                    reviews_sha=reviews_sha, script_sha=tool_sha,
                ):
                    issues.append("receipt-fields")
            expected_status = {0: "clean", 1: "failed", 2: "could-not-evaluate"}[want_rc]
            if actual.get("exit_code") != want_rc or actual.get("status") != expected_status:
                issues.append("receipt-status")
            code = required_findings.get(case_name)
            if code and not c1_code_present(
                actual, code, path_for_case.get(case_name),
            ):
                issues.append("required-finding")
        cases.append({
            "case": case_name,
            "status": "pass" if not issues else "regression",
            "expected_exit_code": want_rc,
            "actual_exit_code": proc.returncode if proc is not None else None,
            "required_finding": required_findings.get(case_name),
            "issues": issues,
            "inputs_sha256": {
                "population": population_sha,
                "reviews": reviews_sha,
                "expected_pin": expected_pin,
            },
            "process": process_receipt(proc, launch_failure),
        })
    return cases


def expected_verdicts() -> dict[str, str]:
    return {
        "fixture-prebuild": "pre-build",
        "fixture-coevolved": "co-evolved",
        "fixture-absent": "absent",
        "fixture-no-implementation": "no-implementation",
        "fixture-edited-after-implementation": "co-evolved",
        "fixture-override": "co-evolved",
    }


def c2_fixture(root: Path, tmpdir: Path,
               env: dict[str, str]) -> dict[str, Any]:
    repo = root / "c2-repo"
    init_repo(repo, env)
    base_files = {
        "fixture/base.txt": b"synthetic base\n",
        "fixture/prebuild/frozen.txt": b"frozen before synthetic implementation\n",
        "fixture/noimpl/frozen.txt": b"synthetic frozen without implementation\n",
        "fixture/edit/frozen.txt": b"synthetic initial frozen bytes\n",
    }
    base = commit_files(repo, base_files, "synthetic base", env)
    pre_tip = commit_files(
        repo, {"tools/fixture-prebuild.py": b"synthetic implementation\n"},
        "synthetic prebuild implementation", env,
    )
    co_tip = commit_files(
        repo,
        {
            "fixture/coevolved/frozen.txt": b"synthetic frozen and implementation\n",
            "tools/fixture-coevolved.py": b"synthetic implementation\n",
        },
        "synthetic coevolved inputs", env,
    )
    absent_tip = commit_files(
        repo, {"tools/fixture-absent.py": b"synthetic implementation\n"},
        "synthetic absent population path", env,
    )
    noimpl_tip = base
    edit_impl = commit_files(
        repo, {"tools/fixture-edit.py": b"synthetic implementation\n"},
        "synthetic edit implementation", env,
    )
    edit_tip = commit_files(
        repo, {"fixture/edit/frozen.txt": b"synthetic updated frozen bytes\n"},
        "synthetic frozen update", env,
    )
    override_tip = co_tip
    run_git(repo, ["tag", "fixture-override", override_tip], env)
    claims = [
        {
            "id": "fixture-prebuild", "base": base, "tip": pre_tip,
            "frozen": ["fixture/prebuild/frozen.txt"],
            "impl": ["tools/fixture-prebuild.py"], "declared": "pre-build",
        },
        {
            "id": "fixture-coevolved", "base": base, "tip": co_tip,
            "frozen": ["fixture/coevolved/frozen.txt"],
            "impl": ["tools/fixture-coevolved.py"], "declared": "pre-build",
            "synthetic_note": PRIVATE_SENTINEL,
        },
        {
            "id": "fixture-absent", "base": pre_tip, "tip": absent_tip,
            "frozen": ["fixture/absent/frozen.txt"],
            "impl": ["tools/fixture-absent.py"], "declared": "co-evolved",
        },
        {
            "id": "fixture-no-implementation", "base": base, "tip": noimpl_tip,
            "frozen": ["fixture/noimpl/frozen.txt"],
            "impl": ["tools/fixture-noimpl.py"], "declared": "co-evolved",
        },
        {
            "id": "fixture-edited-after-implementation", "base": base,
            "tip": edit_tip, "frozen": ["fixture/edit/frozen.txt"],
            "impl": ["tools/fixture-edit.py"], "declared": "co-evolved",
        },
        {
            "id": "fixture-override", "base": base,
            "tip": "<synthetic override>",
            "frozen": ["fixture/coevolved/frozen.txt"],
            "impl": ["tools/fixture-coevolved.py"], "declared": "co-evolved",
        },
    ]
    register_bytes = canonical_json({
        "schema": "mori-freeze-register-v1",
        "claims": claims,
    })
    corrections_bytes = canonical_json({
        "corrections": [{"id": "fixture-coevolved", "label": "co-evolved"}],
    })
    register_relative = "fixtures/register.json"
    corrections_relative = "fixtures/corrections.json"
    measured = commit_files(
        repo,
        {register_relative: register_bytes,
         corrections_relative: corrections_bytes},
        "synthetic measured inputs", env,
    )
    register_path = repo / register_relative
    corrections_path = repo / corrections_relative
    return {
        "repo": repo,
        "base": base,
        "measured": measured,
        "claims": claims,
        "expected_bases": {claim["id"]: claim["base"] for claim in claims},
        "register": register_path,
        "register_relative": register_relative,
        "register_bytes": register_bytes,
        "register_sha256": sha256_bytes(register_bytes),
        "corrections": corrections_path,
        "corrections_relative": corrections_relative,
        "corrections_bytes": corrections_bytes,
        "corrections_sha256": sha256_bytes(corrections_bytes),
        "override_argument": "fixture-override=refs/tags/fixture-override",
        "expected_tips": {
            "fixture-prebuild": pre_tip,
            "fixture-coevolved": co_tip,
            "fixture-absent": absent_tip,
            "fixture-no-implementation": noimpl_tip,
            "fixture-edited-after-implementation": edit_tip,
            "fixture-override": override_tip,
        },
        "impl_tip": edit_impl,
    }


def c2_invocation(tool: Path, fixture: dict[str, Any],
                  root: Path, tmpdir: Path, *, bound: bool,
                  corrections: bool = True, revision: str | None = None,
                  register_path: Path | None = None,
                  corrections_path: Path | None = None
                  ) -> tuple[subprocess.CompletedProcess[bytes] | None,
                             str | None, list[str]]:
    register = register_path or fixture["register"]
    correction_input = corrections_path or fixture["corrections"]
    args = ["check", "--repo", str(fixture["repo"]),
            "--register", str(register)]
    if corrections:
        args.extend(["--corrections", str(correction_input)])
    args.extend(["--tip-for", fixture["override_argument"]])
    if bound:
        args.extend(["--rev", revision or fixture["measured"]])
    proc, failure = run_tool(
        tool, args, root, root / ("home-c2-" + ("bound" if bound else "legacy")),
        tmpdir,
    )
    return proc, failure, [str(tool), *args]


def claim_verdicts(data: dict[str, Any] | None) -> dict[str, str] | None:
    if data is None or not isinstance(data.get("claims"), list):
        return None
    rows = data["claims"]
    result: dict[str, str] = {}
    for row in rows:
        if (not isinstance(row, dict) or not isinstance(row.get("id"), str)
                or not isinstance(row.get("verdict"), str)
                or row["id"] in result):
            return None
        result[row["id"]] = row["verdict"]
    return result


def c2_metadata_checks(expected_names: list[str], mode: str, tool: Path,
                       tool_sha: str | None, fixture: dict[str, Any],
                       root: Path, tmpdir: Path,
                       legacy_proc: subprocess.CompletedProcess[bytes] | None,
                       legacy_failure: str | None,
                       legacy_expected_argv: list[str],
                       bound_proc: subprocess.CompletedProcess[bytes] | None,
                       bound_failure: str | None,
                       bound_expected_argv: list[str] | None,
                       invalid_proc: subprocess.CompletedProcess[bytes] | None,
                       invalid_failure: str | None,
                       absent_corrections_proc: subprocess.CompletedProcess[bytes] | None,
                       ) -> list[dict[str, Any]]:
    baseline = parsed_stdout(legacy_proc)
    bound = parsed_stdout(bound_proc)
    invalid = parsed_stdout(invalid_proc)
    absent_corrections = parsed_stdout(absent_corrections_proc)
    statuses: dict[str, tuple[str, str | None]] = {}

    def set_result(name: str, ok: bool, unavailable: bool = False) -> None:
        statuses[name] = ("pass" if ok else
                          "capability_absent" if unavailable and mode == "before" else "regression",
                          None if ok else ("metadata-unavailable" if unavailable
                                           else "assertion-mismatch"))

    if mode == "before":
        baseline_verdicts = claim_verdicts(baseline)
        if legacy_failure or baseline_verdicts is None:
            set_result("same_verdicts_as_base", False)
        else:
            set_result("same_verdicts_as_base",
                       baseline_verdicts == expected_verdicts())
        process_set = [legacy_proc, bound_proc, invalid_proc, absent_corrections_proc]
        no_values = not any(marker_leaked(proc) for proc in process_set)
        set_result("no_private_values", no_values)
        observed = c2_metadata_checks(
            expected_names, "after", tool, tool_sha, fixture, root, tmpdir,
            legacy_proc, legacy_failure, legacy_expected_argv,
            bound_proc, bound_failure, bound_expected_argv,
            invalid_proc, invalid_failure, absent_corrections_proc,
        )
        for row in observed:
            if row["check"] not in ("same_verdicts_as_base", "no_private_values"):
                set_result(row["check"], row["status"] == "pass",
                           unavailable=row.get("classification") == "metadata-unavailable")
    else:
        provenance = bound.get("provenance") if isinstance(bound, dict) else None
        if not isinstance(provenance, dict):
            provenance = {}
        legacy_provenance = baseline.get("provenance") if isinstance(baseline, dict) else None
        if not isinstance(legacy_provenance, dict):
            legacy_provenance = {}
        measured = provenance.get("measured_revision")
        set_result("measured_revision_full_oid",
                   measured == fixture["measured"] and isinstance(measured, str)
                   and bool(OID_RE.fullmatch(measured)),
                   unavailable=not isinstance(bound, dict)
                   or "measured_revision" not in provenance)
        set_result("register_sha256",
                   provenance.get("register_sha256") == fixture["register_sha256"]
                   and legacy_provenance.get("register_sha256") == fixture["register_sha256"],
                   unavailable="register_sha256" not in provenance)
        set_result("corrections_sha256",
                   provenance.get("corrections_sha256") == fixture["corrections_sha256"]
                   and legacy_provenance.get("corrections_sha256") == fixture["corrections_sha256"]
                   and absent_corrections is not None
                   and isinstance(absent_corrections.get("provenance"), dict)
                   and absent_corrections["provenance"].get("corrections_sha256") is None,
                   unavailable=("corrections_sha256" not in provenance
                                or absent_corrections is None
                                or not isinstance(absent_corrections.get("provenance"), dict)))
        set_result("script_sha256",
                   tool_sha is not None and provenance.get("script_sha256") == tool_sha
                   and legacy_provenance.get("script_sha256") == tool_sha,
                   unavailable="script_sha256" not in provenance)

        claim_rows = bound.get("claims") if isinstance(bound, dict) else None
        expected_ids = set(expected_verdicts())
        if not isinstance(claim_rows, list):
            by_id: dict[str, dict[str, Any]] = {}
        else:
            by_id = {
                row["id"]: row for row in claim_rows
                if isinstance(row, dict) and isinstance(row.get("id"), str)
            }
        identity_complete = set(by_id) == expected_ids
        bases_ok = identity_complete and all(
            by_id[ident].get("base_revision") == fixture["expected_bases"][ident]
            for ident in expected_ids
        )
        tips_ok = identity_complete and all(
            by_id[ident].get("tip_revision") == fixture["expected_tips"][ident]
            for ident in expected_ids
        )
        set_result("resolved_base_per_claim", bases_ok,
                   unavailable=not identity_complete or any(
                       "base_revision" not in row for row in by_id.values()))
        set_result("resolved_tip_per_claim", tips_ok,
                   unavailable=not identity_complete or any(
                       "tip_revision" not in row for row in by_id.values()))
        override = provenance.get("tip_overrides")
        set_result("override_recorded",
                   override == [fixture["override_argument"]]
                   and legacy_provenance.get("tip_overrides") == [fixture["override_argument"]],
                   unavailable="tip_overrides" not in provenance)
        command_argv = provenance.get("command_argv")
        allowed_argv = []
        if bound_expected_argv is not None:
            allowed_argv = [bound_expected_argv, [sys.executable, *bound_expected_argv]]
        set_result("command_argv", command_argv in allowed_argv
                   and legacy_provenance.get("command_argv") in
                   [legacy_expected_argv, [sys.executable, *legacy_expected_argv]],
                   unavailable="command_argv" not in provenance)
        register_digest_ok = (
            sha256_bytes(fixture["register_bytes"]) == fixture["register_sha256"]
            and provenance.get("register_sha256") == sha256_bytes(fixture["register_bytes"])
            and legacy_provenance.get("register_sha256") == sha256_bytes(fixture["register_bytes"])
        )
        set_result("register_digest_matches_loaded_bytes", register_digest_ok,
                   unavailable="register_sha256" not in provenance)
        base_verdicts = claim_verdicts(baseline)
        bound_verdicts = claim_verdicts(bound)
        same = (base_verdicts is not None and bound_verdicts is not None
                and base_verdicts == expected_verdicts()
                and bound_verdicts == expected_verdicts()
                and base_verdicts == bound_verdicts
                and legacy_provenance.get("status") == "unbound"
                and legacy_provenance.get("measured_revision") is None
                and provenance.get("status") == "bound")
        set_result("same_verdicts_as_base", same,
                   unavailable=(base_verdicts is None or bound_verdicts is None))
        privacy_ok = not any(marker_leaked(proc) for proc in
                             (legacy_proc, bound_proc, invalid_proc,
                              absent_corrections_proc))
        set_result("no_private_values", privacy_ok)
        invalid_ok = (
            invalid_proc is not None and invalid_proc.returncode == 2
            and isinstance(invalid, dict)
            and invalid.get("error") == "unknown-measured-revision"
            and invalid.get("claims") == []
        )
        set_result("invalid_revision_could_not_evaluate", invalid_ok,
                   unavailable=(invalid_proc is None or invalid is None))

    return [
        {"check": name, "status": statuses[name][0],
         **({"classification": statuses[name][1]}
            if statuses[name][1] else {})}
        for name in expected_names
    ]


def supplemental_binding_checks(tool: Path, fixture: dict[str, Any],
                                root: Path, tmpdir: Path,
                                env: dict[str, str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    repo = fixture["repo"]
    register_path = fixture["register"]
    original = fixture["register_bytes"]

    dirty = original + b" "
    register_path.write_bytes(dirty)
    proc, failure, _argv = c2_invocation(
        tool, fixture, root, tmpdir, bound=True,
    )
    rows.append({
        "check": "dirty_register_rejected",
        "status": "pass" if proc is not None and proc.returncode == 2 and not marker_leaked(proc) else "regression",
        "expected_exit_code": 2,
        "actual_exit_code": proc.returncode if proc is not None else None,
        "process": process_receipt(proc, failure),
        "private_value_leak": marker_leaked(proc),
    })
    register_path.write_bytes(original)

    external_register = root / "external-register.json"
    external_register.write_bytes(original)
    proc, failure, _argv = c2_invocation(
        tool, fixture, root, tmpdir, bound=True,
        register_path=external_register,
    )
    rows.append({
        "check": "external_register_rejected",
        "status": "pass" if proc is not None and proc.returncode == 2 and not marker_leaked(proc) else "regression",
        "expected_exit_code": 2,
        "actual_exit_code": proc.returncode if proc is not None else None,
        "process": process_receipt(proc, failure),
        "private_value_leak": marker_leaked(proc),
    })

    external_corrections = root / "external-corrections.json"
    external_corrections.write_bytes(fixture["corrections_bytes"])
    proc, failure, _argv = c2_invocation(
        tool, fixture, root, tmpdir, bound=True,
        corrections_path=external_corrections,
    )
    rows.append({
        "check": "external_corrections_rejected",
        "status": "pass" if proc is not None and proc.returncode == 2 and not marker_leaked(proc) else "regression",
        "expected_exit_code": 2,
        "actual_exit_code": proc.returncode if proc is not None else None,
        "process": process_receipt(proc, failure),
        "private_value_leak": marker_leaked(proc),
    })

    corrections = fixture["corrections"]
    corrections.write_bytes(fixture["corrections_bytes"] + b" ")
    proc, failure, _argv = c2_invocation(
        tool, fixture, root, tmpdir, bound=True,
    )
    rows.append({
        "check": "dirty_corrections_rejected",
        "status": "pass" if proc is not None and proc.returncode == 2 and not marker_leaked(proc) else "regression",
        "expected_exit_code": 2,
        "actual_exit_code": proc.returncode if proc is not None else None,
        "process": process_receipt(proc, failure),
        "private_value_leak": marker_leaked(proc),
    })
    corrections.write_bytes(fixture["corrections_bytes"])
    return rows


def validate_expected(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict) or data.get("schema") != EXPECTED_SCHEMA:
        raise HarnessError("expected-schema-invalid")
    c1 = data.get("c1_cases")
    if (not isinstance(c1, dict) or set(c1) != set(C1_CASE_NAMES)
            or any(type(value) is not int or value not in (0, 1, 2)
                   for value in c1.values())):
        raise HarnessError("expected-c1-cases-invalid")
    required = data.get("c1_required_finding")
    if not isinstance(required, dict) or any(
        not isinstance(key, str) or not isinstance(value, str)
        for key, value in required.items()
    ):
        raise HarnessError("expected-c1-findings-invalid")
    checks = data.get("c2_checks")
    if checks != list(C2_CHECK_NAMES):
        raise HarnessError("expected-c2-checks-invalid")
    return data


def expected_from_pinned_commit(expected_path: Path) -> tuple[Path, bytes, dict[str, Any]]:
    if expected_path.is_symlink() or not expected_path.is_file():
        raise HarnessError("expected-file-invalid")
    resolved = expected_path.resolve(strict=True)
    if resolved.name != "expected.json" or tuple(resolved.parts[-4:]) != (
        "waves", "round-19", "frozen", "expected.json",
    ):
        raise HarnessError("expected-path-invalid")
    repo = resolved.parents[4]
    try:
        rel = resolved.relative_to(repo).as_posix()
    except ValueError:
        raise HarnessError("expected-path-invalid") from None
    if rel != ORACLE_RELATIVE_PATH:
        raise HarnessError("expected-path-invalid")
    env = clean_env(repo, repo)
    argv = [
        "git", "--no-optional-locks", "-c", "core.fsmonitor=false",
        "-C", str(repo), "show", ORACLE_REVISION + ":" + ORACLE_RELATIVE_PATH,
    ]
    try:
        proc = subprocess.run(
            argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, env=env, timeout=GIT_TIMEOUT, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        raise HarnessError("pinned-oracle-unavailable") from None
    if proc.returncode != 0:
        raise HarnessError("pinned-oracle-unavailable")
    try:
        supplied = resolved.read_bytes()
    except OSError:
        raise HarnessError("expected-file-unreadable") from None
    if supplied != proc.stdout:
        raise HarnessError("expected-oracle-mismatch")
    try:
        expected = validate_expected(json_load_bytes(supplied))
    except (UnicodeError, json.JSONDecodeError, ValueError):
        raise HarnessError("expected-json-invalid") from None
    return repo, supplied, expected


def require_tmpdir() -> Path:
    raw = os.environ.get("TMPDIR")
    if not raw or not Path(raw).is_absolute():
        raise HarnessError("explicit-lane-tmpdir-required")
    candidate = Path(raw)
    try:
        resolved = candidate.resolve(strict=True)
        info = resolved.stat()
    except OSError:
        raise HarnessError("explicit-lane-tmpdir-invalid") from None
    lane_root = Path(__file__).resolve().parents[1]
    if (resolved != candidate or not stat.S_ISDIR(info.st_mode)
            or resolved == lane_root or lane_root not in resolved.parents):
        raise HarnessError("explicit-lane-tmpdir-invalid")
    return resolved


def tool_path(raw: str) -> tuple[Path, str | None]:
    path = Path(raw)
    if not path.is_absolute():
        raise HarnessError("tool-path-must-be-absolute")
    try:
        resolved = path.resolve(strict=False)
    except OSError:
        raise HarnessError("tool-path-invalid") from None
    if resolved.exists():
        try:
            info = resolved.lstat()
        except OSError:
            raise HarnessError("tool-path-unreadable") from None
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
            raise HarnessError("tool-path-invalid")
        try:
            digest = sha256_file(resolved)
        except OSError:
            raise HarnessError("tool-path-unreadable") from None
        return resolved, digest
    return resolved, None


def output_path(raw: str, inputs: list[Path]) -> Path:
    path = Path(raw)
    if not path.is_absolute():
        raise HarnessError("output-path-must-be-absolute")
    parent = path.parent.resolve(strict=True)
    target = parent / path.name
    if target.exists() or target.is_symlink():
        raise HarnessError("output-must-be-absent")
    for item in inputs:
        try:
            if target == item.resolve(strict=False):
                raise HarnessError("output-overlaps-input")
        except OSError:
            raise HarnessError("output-path-invalid") from None
    return target


def counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "total": len(rows),
        "pass": sum(row.get("status") == "pass" for row in rows),
        "capability_absent": sum(row.get("status") == "capability_absent" for row in rows),
        "regression": sum(row.get("status") == "regression" for row in rows),
    }


def run_harness(args: argparse.Namespace) -> tuple[dict[str, Any], int]:
    expected_path = Path(args.expected)
    repo_root, oracle_bytes, expected = expected_from_pinned_commit(expected_path)
    expected_sha = sha256_bytes(oracle_bytes)
    tmpdir = require_tmpdir()
    content_tool, content_tool_sha = tool_path(args.content_tool)
    freeze_tool, freeze_tool_sha = tool_path(args.freeze_tool)
    out_path = output_path(args.output, [
        expected_path.resolve(strict=True), content_tool, freeze_tool,
    ])
    script_path = Path(__file__).resolve()
    harness_sha_before = sha256_file(script_path)
    oracle_before = sha256_file(expected_path.resolve(strict=True))
    if oracle_before != expected_sha:
        raise HarnessError("expected-oracle-changed")

    result: dict[str, Any] = {
        "schema": "mori-round19-regressions-v1",
        "mode": args.mode,
        "oracle": {
            "revision": ORACLE_REVISION,
            "path": ORACLE_RELATIVE_PATH,
            "sha256": expected_sha,
        },
        "inputs": {
            "content_tool": {"path": str(content_tool), "sha256": content_tool_sha},
            "freeze_tool": {"path": str(freeze_tool), "sha256": freeze_tool_sha},
            "expected_sha256": expected_sha,
            "harness_sha256": harness_sha_before,
        },
        "c1": {"cases": []},
        "c2": {"checks": [], "supplemental": []},
    }

    setup_home = tmpdir / "mori-r19-home-init"
    setup_home.mkdir(exist_ok=True)
    sandbox_parent = Path(tempfile.mkdtemp(prefix="mori-r19-regressions-", dir=tmpdir))
    try:
        c1_env = clean_env(setup_home, tmpdir)
        c1_repo = sandbox_parent / "c1-repo"
        init_repo(c1_repo, c1_env)
        initial_data = {
            "synthetic/alpha.txt": b"synthetic retained review fixture alpha\n",
            "synthetic/beta.txt": b"synthetic retained review fixture beta\n",
        }
        c1_revision = commit_files(c1_repo, initial_data, "synthetic C1 population", c1_env)
        if content_tool_sha is None:
            c1_rows = [
                {"case": name, "status": "capability_absent",
                 "expected_exit_code": expected["c1_cases"][name],
                 "actual_exit_code": None, "required_finding": expected.get(
                     "c1_required_finding", {}).get(name),
                 "classification": "content-tool-absent"}
                for name in C1_CASE_NAMES
            ]
        else:
            c1_rows = c1_case_rows(
                expected, content_tool, c1_repo, c1_revision,
                sandbox_parent, tmpdir, content_tool_sha,
            )
        result["c1"]["cases"] = c1_rows
        result["c1"]["counts"] = counts(c1_rows)

        c2_repo_env = clean_env(setup_home, tmpdir)
        fixture = c2_fixture(sandbox_parent, tmpdir, c2_repo_env)
        expected_names = expected["c2_checks"]
        if freeze_tool_sha is None:
            c2_rows = [
                {"check": name, "status": "capability_absent",
                 "classification": "freeze-tool-absent"}
                for name in expected_names
            ]
            supplemental = []
        else:
            legacy_proc, legacy_failure, legacy_argv = c2_invocation(
                freeze_tool, fixture, sandbox_parent, tmpdir, bound=False,
            )
            bound_proc, bound_failure, bound_argv = c2_invocation(
                freeze_tool, fixture, sandbox_parent, tmpdir, bound=True,
            )
            invalid_proc, invalid_failure, _ = c2_invocation(
                freeze_tool, fixture, sandbox_parent, tmpdir, bound=True,
                revision="round19-invalid-synthetic-revision",
            )
            absent_proc, _absent_failure, _ = c2_invocation(
                freeze_tool, fixture, sandbox_parent, tmpdir, bound=True,
                corrections=False,
            )
            c2_rows = c2_metadata_checks(
                expected_names, args.mode, freeze_tool, freeze_tool_sha,
                fixture, sandbox_parent, tmpdir,
                legacy_proc, legacy_failure, legacy_argv,
                bound_proc, bound_failure, bound_argv,
                invalid_proc, invalid_failure, absent_proc,
            )
            supplemental = []
            if args.mode == "after":
                supplemental = supplemental_binding_checks(
                    freeze_tool, fixture, sandbox_parent, tmpdir, c2_repo_env,
                )
            # Preserve safe process receipts, but no tool output bytes or values.
            result["c2"]["processes"] = {
                "legacy": process_receipt(legacy_proc, legacy_failure),
                "bound": process_receipt(bound_proc, bound_failure),
                "invalid_revision": process_receipt(invalid_proc, invalid_failure),
                "without_corrections": process_receipt(absent_proc),
            }
        result["c2"]["checks"] = c2_rows
        result["c2"]["counts"] = counts(c2_rows)
        result["c2"]["supplemental"] = supplemental
        result["c2"]["supplemental_counts"] = counts(supplemental)
        result["c2"]["fixture_inputs_sha256"] = {
            "register": fixture["register_sha256"],
            "corrections": fixture["corrections_sha256"],
        }

        tool_after_content = sha256_file(content_tool) if content_tool.exists() else None
        tool_after_freeze = sha256_file(freeze_tool) if freeze_tool.exists() else None
        oracle_after = sha256_file(expected_path.resolve(strict=True))
        harness_after = sha256_file(script_path)
        stability = {
            "content_tool_unchanged": content_tool_sha == tool_after_content,
            "freeze_tool_unchanged": freeze_tool_sha == tool_after_freeze,
            "expected_unchanged": oracle_before == oracle_after,
            "harness_unchanged": harness_sha_before == harness_after,
        }
        result["stability"] = stability
        result["inputs"]["content_tool_sha256_after"] = tool_after_content
        result["inputs"]["freeze_tool_sha256_after"] = tool_after_freeze
        if not all(stability.values()):
            result["status"] = "setup-error"
            result["error_class"] = "input-changed-during-run"
            exit_code = 2
        else:
            total_counts = [result["c1"]["counts"], result["c2"]["counts"],
                            result["c2"]["supplemental_counts"]]
            regressions = sum(row["regression"] for row in total_counts)
            absent = sum(row["capability_absent"] for row in total_counts)
            if args.mode == "before":
                result["status"] = "baseline-recorded" if regressions == 0 else "baseline-defect"
                exit_code = 1 if regressions or absent else 0
            else:
                result["status"] = "pass" if regressions == 0 and absent == 0 else "failed"
                exit_code = 0 if result["status"] == "pass" else 1
        encoded = canonical_json(result)
        try:
            with out_path.open("xb") as stream:
                stream.write(encoded)
        except OSError:
            raise HarnessError("output-write-failed") from None
        return result, exit_code
    finally:
        # This path is created only beneath the explicitly supplied lane TMPDIR.
        import shutil
        shutil.rmtree(sandbox_parent)
        try:
            setup_home.rmdir()
        except OSError:
            pass


# =============================================================================
# --selftest: bounded self-check of this harness over the isolated synthetic git
# fixtures the `--mode after` path builds (c2_fixture), plus mutant inputs every
# check must reject.  No production tool is dispatched and nothing is written
# outside the caller's explicit lane TMPDIR, so the selftest is hermetic and
# offline.  Exit 0 every check passed, 1 a check failed, 2 setup.
# =============================================================================
SELFTEST_VERDICTS = ("pre-build", "co-evolved", "absent", "no-implementation")
# (frozen path present at the bound tip, implementation path present) per claim.
SELFTEST_CLAIM_PRESENCE = {
    "fixture-prebuild": (True, True),
    "fixture-coevolved": (True, True),
    "fixture-absent": (False, True),
    "fixture-no-implementation": (True, False),
    "fixture-edited-after-implementation": (True, True),
    "fixture-override": (True, True),
}


class SelftestTally:
    """Pass/fail counter with failure names (names only, never fixture values)."""

    def __init__(self) -> None:
        self.passed = 0
        self.failures: list[str] = []

    def check(self, name: str, ok: bool) -> None:
        if ok:
            self.passed += 1
        else:
            self.failures.append(name)


def selftest_rejects(fn: Any, *args: Any,
                     errors: tuple[type[BaseException], ...] = (HarnessError,),
                     **kwargs: Any) -> bool:
    try:
        fn(*args, **kwargs)
    except errors:
        return True
    return False


def selftest_path_present(repo: Path, revision: str, path: str,
                          env: dict[str, str]) -> bool:
    """True when `path` is committed at `revision` (a fixture read)."""
    try:
        run_git(repo, ["cat-file", "-e", f"{revision}:{path}"], env)
    except HarnessError:
        return False
    return True


def run_selftest() -> int:
    tmpdir = require_tmpdir()
    tally = SelftestTally()
    sandbox = Path(tempfile.mkdtemp(prefix="mori-r19-selftest-", dir=tmpdir))
    try:
        home = sandbox / "home"
        home.mkdir()
        env = clean_env(home, tmpdir)
        fixture = c2_fixture(sandbox, tmpdir, env)
        repo = fixture["repo"]
        claims = json_load_bytes(fixture["register"].read_bytes())["claims"]

        fixture_oids = [fixture["base"], fixture["measured"],
                        *fixture["expected_tips"].values()]
        tally.check(
            "fixture-commits-resolve",
            all(run_git(repo, ["rev-parse", "--verify", f"{oid}^{{commit}}"], env)
                .decode("ascii").strip() == oid for oid in fixture_oids),
        )
        tally.check(
            "fixture-override-tag-resolves",
            run_git(repo, ["rev-parse", "refs/tags/fixture-override"], env)
            .decode("ascii").strip()
            == fixture["expected_tips"]["fixture-override"],
        )

        tally.check(
            "register-digest-matches-bytes",
            sha256_file(fixture["register"]) == fixture["register_sha256"]
            and sha256_bytes(fixture["register"].read_bytes())
            == fixture["register_sha256"],
        )
        tally.check(
            "corrections-digest-matches-bytes",
            sha256_file(fixture["corrections"]) == fixture["corrections_sha256"],
        )

        tally.check(
            "register-claims-unique",
            len({claim["id"] for claim in claims}) == len(claims)
            == len(fixture["expected_tips"]),
        )
        tips_ok = True
        for claim in claims:
            if (claim["tip"] != "<synthetic override>"
                    and claim["tip"] != fixture["expected_tips"][claim["id"]]):
                tips_ok = False
            if claim["base"] != fixture["expected_bases"][claim["id"]]:
                tips_ok = False
        tally.check("claims-bind-expected-tips", tips_ok)

        presence_ok = True
        for claim in claims:
            tip = claim["tip"]
            if tip == "<synthetic override>":
                tip = fixture["expected_tips"][claim["id"]]
            want_frozen, want_impl = SELFTEST_CLAIM_PRESENCE[claim["id"]]
            observed = (
                all(selftest_path_present(repo, tip, path, env)
                    for path in claim["frozen"]),
                all(selftest_path_present(repo, tip, path, env)
                    for path in claim["impl"]),
            )
            if observed != (want_frozen, want_impl):
                presence_ok = False
        tally.check("claims-bind-expected-path-presence", presence_ok)
        tally.check(
            "absent-frozen-path-detected",
            not selftest_path_present(
                repo, fixture["expected_tips"]["fixture-absent"],
                "fixture/absent/frozen.txt", env,
            ),
        )

        verdicts = expected_verdicts()
        tally.check(
            "verdict-table-covers-claims",
            set(verdicts) == {claim["id"] for claim in claims}
            and all(value in SELFTEST_VERDICTS for value in verdicts.values()),
        )
        declared = next(claim["declared"] for claim in claims
                        if claim["id"] == "fixture-coevolved")
        tally.check(
            "coevolved-verdict-differs-from-declared",
            verdicts["fixture-coevolved"] == "co-evolved"
            and verdicts["fixture-coevolved"] != declared,
        )

        register_obj = json_load_bytes(fixture["register"].read_bytes())
        tally.check(
            "canonical-json-roundtrip",
            json_load_bytes(canonical_json(register_obj)) == register_obj,
        )
        tally.check("duplicate-json-key-rejected",
                    selftest_rejects(json_load_bytes, b'{"a":1,"a":2}',
                                     errors=(ValueError,)))
        tally.check("non-finite-json-rejected",
                    selftest_rejects(json_load_bytes, b'{"a":NaN}',
                                     errors=(ValueError,)))

        tally.check(
            "safe-repo-path-rejects-traversal",
            selftest_rejects(safe_repo_path, "../escape")
            and selftest_rejects(safe_repo_path, "/absolute")
            and selftest_rejects(safe_repo_path, "a\\b")
            and safe_repo_path("a/b").as_posix() == "a/b",
        )

        existing_output = sandbox / "existing-output.json"
        existing_output.write_bytes(b"{}\n")
        tally.check(
            "output-path-guards",
            selftest_rejects(output_path, "relative.json", [])
            and selftest_rejects(output_path, str(existing_output), [])
            and selftest_rejects(output_path, str(sandbox / "input.json"),
                                 [sandbox / "input.json"])
            and output_path(str(sandbox / "fresh-output.json"), [])
            == sandbox / "fresh-output.json",
        )

        script_path = Path(__file__).resolve()
        resolved_self, self_sha = tool_path(str(script_path))
        absent_tool, absent_sha = tool_path(str(sandbox / "absent-tool.py"))
        tally.check(
            "tool-path-digest-and-absence",
            self_sha == sha256_file(script_path)
            and resolved_self.is_file()
            and absent_sha is None and not absent_tool.exists(),
        )
        tally.check(
            "tool-path-rejects-relative-and-directory",
            selftest_rejects(tool_path, "tools/relative.py")
            and selftest_rejects(tool_path, str(sandbox)),
        )

        saved_tmpdir = os.environ.pop("TMPDIR", None)
        try:
            missing_rejected = selftest_rejects(require_tmpdir)
        finally:
            if saved_tmpdir is not None:
                os.environ["TMPDIR"] = saved_tmpdir
        os.environ["TMPDIR"] = str(script_path.parents[1].parent)
        try:
            outside_rejected = selftest_rejects(require_tmpdir)
        finally:
            if saved_tmpdir is not None:
                os.environ["TMPDIR"] = saved_tmpdir
            else:
                os.environ.pop("TMPDIR", None)
        tally.check("tmpdir-guard",
                    missing_rejected and outside_rejected)

        tally.check(
            "counts-classification",
            counts([{"status": "pass"}, {"status": "regression"},
                    {"status": "capability_absent"}, {}])
            == {"total": 4, "pass": 1, "capability_absent": 1, "regression": 1},
        )

        ok_proc = subprocess.CompletedProcess(
            ["synthetic"], 0, b'{"status":"clean"}\n', b"")
        bad_proc = subprocess.CompletedProcess(["synthetic"], 1, b"not-json", b"")
        leak_proc = subprocess.CompletedProcess(
            ["synthetic"], 0, PRIVATE_SENTINEL.encode("utf-8"), b"")
        tally.check(
            "process-receipt-shape",
            process_receipt(ok_proc)["exit_code"] == 0
            and process_receipt(ok_proc)["stdout_bytes"] == len(ok_proc.stdout)
            and parsed_stdout(ok_proc) == {"status": "clean"}
            and parsed_stdout(bad_proc) is None,
        )
        tally.check(
            "private-marker-detected",
            marker_leaked(leak_proc) and not marker_leaked(ok_proc),
        )

        payloads = c1_fixture_payloads("synthetic-revision-placeholder")
        c1_repo = sandbox / "c1-repo"
        init_repo(c1_repo, env)
        c1_revision = commit_files(
            c1_repo, dict(payloads["blob_data"]), "synthetic C1 population", env,
        )
        payloads = c1_fixture_payloads(c1_revision)
        population_sha = sha256_bytes(canonical_json(payloads["population"]))
        reviews_sha = sha256_bytes(b"synthetic reviews\n")
        script_sha = sha256_bytes(b"synthetic content tool source\n")
        receipt = {
            "revision": c1_revision,
            "metadata": {
                "revision": c1_revision,
                "population_sha256": population_sha,
                "reviews_sha256": reviews_sha,
                "script_sha256": script_sha,
            },
            "counts": {"population_paths": 2, "review_rows": 2,
                       "blobs_read": 2, "findings": 1},
            "findings": [{"code": "SYNTHETIC_FINDING",
                          "path": "synthetic/alpha.txt"}],
            "status": "failed",
        }

        def receipt_valid(data: dict[str, Any]) -> bool:
            return c1_output_valid(
                data, revision=c1_revision,
                population_sha=population_sha,
                reviews_sha=reviews_sha, script_sha=script_sha,
            )

        drifted = dict(receipt, metadata=dict(receipt["metadata"],
                                              population_sha256="0" * 64))
        overcounted = dict(receipt, counts=dict(receipt["counts"], findings=2))
        tally.check("c1-receipt-fields", receipt_valid(receipt))
        tally.check("c1-receipt-mutants-rejected",
                    not receipt_valid(drifted) and not receipt_valid(overcounted))
        tally.check(
            "c1-finding-row-lookup",
            c1_code_present(receipt, "SYNTHETIC_FINDING", "synthetic/alpha.txt")
            and not c1_code_present(receipt, "SYNTHETIC_FINDING",
                                    "synthetic/beta.txt"),
        )
        tally.check(
            "c1-fixture-blobs-match-digests",
            all(sha256_bytes(run_git(
                c1_repo, ["cat-file", "blob",
                          f"{c1_revision}:{row['path']}"], env,
            )) == row["blob_sha256"] for row in payloads["safe_rows"]),
        )

        oracle = script_path.parents[1] / ORACLE_RELATIVE_PATH
        try:
            _oracle_repo, oracle_bytes, expected = expected_from_pinned_commit(oracle)
            oracle_ok = (sha256_bytes(oracle_bytes) == sha256_file(oracle)
                         and expected["schema"] == EXPECTED_SCHEMA)
        except HarnessError:
            oracle_ok = False
        tally.check("pinned-oracle-validates", oracle_ok)
    finally:
        shutil.rmtree(sandbox, ignore_errors=True)

    for name in tally.failures:
        sys.stderr.write("FAIL " + name + "\n")
    sys.stdout.write(
        f"R19_SELFTEST pass={tally.passed} fail={len(tally.failures)}\n")
    return 0 if not tally.failures else 1


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--content-tool", required=True, metavar="PATH")
    parser.add_argument("--freeze-tool", required=True, metavar="PATH")
    parser.add_argument("--expected", required=True, metavar="PATH")
    parser.add_argument("--output", required=True, metavar="PATH")
    parser.add_argument("--mode", required=True, choices=("before", "after"))
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    raw = list(sys.argv[1:] if argv is None else argv)
    if "--selftest" in raw:
        if raw != ["--selftest"]:
            sys.stderr.write(
                "R19_SELFTEST setup=--selftest-takes-no-other-arguments\n")
            return 2
        try:
            return run_selftest()
        except (HarnessError, OSError) as exc:
            sys.stderr.write(f"R19_SELFTEST setup={exc}\n")
            return 2
    args = parse_args(raw)
    try:
        result, exit_code = run_harness(args)
    except HarnessError as exc:
        result = {
            "schema": "mori-round19-regressions-v1",
            "mode": args.mode,
            "status": "setup-error",
            "error_class": str(exc),
        }
        exit_code = 2
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
