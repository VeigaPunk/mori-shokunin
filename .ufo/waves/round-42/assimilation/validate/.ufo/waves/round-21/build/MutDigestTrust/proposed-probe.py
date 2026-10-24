#!/usr/bin/env python3
"""Proposed round21 trust-boundary probe; authoring this file does not run it.

Later L1 invocation: python3 proposed-probe.py --audit-script PATH
Only two one-row synthetic fixtures are evaluated, never lane accounting.
The six audit calls are pristine/mutated/restored for each of two mutations.
All Git writes, copied evaluator bytes and receipts stay under this seat.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
from typing import Any


LANE = Path("/home/vgpnk/Projects/shokunin/mori-shokunin")
SEAT = LANE / ".ufo/waves/round-21/build/MutDigestTrust"
TMPDIR = LANE / ".scratch"
TIMEOUT_SECONDS = 10
AUDIT_SCHEMA = "mori-evidence-loss-audit-v1"
COUNT_KEYS = ("omitted", "retained", "unresolved", "disposed", "invalid")
WAVE = "synthetic-round21-mut-digest-trust"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, indent=2) + "\n").encode("utf-8")


def file_state(path: Path) -> dict[str, Any]:
    info = path.lstat()
    kind = "symlink" if stat.S_ISLNK(info.st_mode) else "regular"
    if kind == "regular" and not stat.S_ISREG(info.st_mode):
        raise ValueError("unexpected fixture file type")
    result = {"kind": kind, "mode": stat.S_IMODE(info.st_mode),
              "sha256": sha256(path.read_bytes())}
    if kind == "symlink":
        result["link_target"] = str(path.readlink())
    return result


def clean_env(home: Path) -> dict[str, str]:
    home.mkdir()
    return {
        "PATH": "/usr/bin:/bin", "HOME": str(home), "TMPDIR": str(TMPDIR),
        "LC_ALL": "C", "LANG": "C", "TZ": "UTC",
        "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null",
        "GIT_CONFIG_NOSYSTEM": "1", "GIT_TERMINAL_PROMPT": "0",
        "GIT_OPTIONAL_LOCKS": "0",
    }


def command(argv: list[str], cwd: Path, env: dict[str, str]) -> dict[str, Any]:
    try:
        process = subprocess.run(
            argv, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=TIMEOUT_SECONDS, check=False,
        )
        raw_out, raw_err = process.stdout, process.stderr
        result = {"argv": argv, "returncode": process.returncode, "timeout": False}
    except subprocess.TimeoutExpired as error:
        raw_out, raw_err = error.stdout or b"", error.stderr or b""
        result = {"argv": argv, "returncode": None, "timeout": True}
    except OSError as error:
        raw_out, raw_err = b"", str(error).encode("utf-8")
        result = {"argv": argv, "returncode": None, "timeout": False,
                  "launch_error": type(error).__name__}
    result.update({"stdout": raw_out.decode("utf-8", errors="replace"),
                   "stderr": raw_err.decode("utf-8", errors="replace"),
                   "stdout_sha256": sha256(raw_out), "stderr_sha256": sha256(raw_err)})
    return result


def git(repo: Path, env: dict[str, str], *arguments: str) -> str:
    result = command([
        "git", "-c", "core.hooksPath=/dev/null", "-c", "core.fsmonitor=false",
        "-c", "commit.gpgsign=false", "-c", "protocol.allow=never",
        "-c", "user.name=Round21 synthetic probe",
        "-c", "user.email=round21-probe@example.invalid", "-C", str(repo),
        *arguments,
    ], repo, env)
    if result["returncode"] != 0:
        raise RuntimeError(json.dumps({"synthetic_git_failure": result}, sort_keys=True))
    return result["stdout"].strip()


def make_fixture(repo: Path, env: dict[str, str]) -> tuple[Path, list[Path], str]:
    repo.mkdir()
    empty_template = repo / "empty-git-template"
    empty_template.mkdir()
    git(repo, env, "init", "-q", "--template=" + str(empty_template))
    evidence = repo / "evidence"
    evidence.mkdir()
    payloads = {
        "baseline.json": {"wave_id": WAVE, "actor": "synthetic-observer"},
        "deletion.json": {"wave_id": WAVE, "actor": "synthetic-cleaner"},
        "cleanup.json": {"wave_id": WAVE, "actor": "synthetic-cleaner"},
        "disposition.json": {"id": WAVE, "wave_id": WAVE, "actor": "synthetic-independent-reviewer",
                             "independent": True, "disposition": "cleanup-accounted"},
    }
    for name, payload in payloads.items():
        (evidence / name).write_bytes(json_bytes(payload))
    target = evidence / "disposition.json"
    twin = evidence / "disposition-twin.json"
    twin.write_bytes(target.read_bytes())
    git(repo, env, "add", "--", "evidence")
    git(repo, env, "commit", "-q", "-m", "Synthetic evidence only; no historical disposition")
    revision = git(repo, env, "rev-parse", "HEAD")

    def reference(name: str, **extra: Any) -> dict[str, Any]:
        path = evidence / name
        return {"path": path.relative_to(repo).as_posix(), "revision": revision,
                "sha256": sha256(path.read_bytes()), **extra}

    baseline = reference("baseline.json")
    required = {"schema": "mori-required-observations-v1", "observations": [
        {"id": WAVE, "baseline": baseline, "evidence": "evidence/baseline.json:1"},
    ]}
    accounting = {"schema": "mori-loss-accounting-v1", "observations": [{
        "id": WAVE, "state": "disposed", "baseline": baseline,
        "deletion": reference("deletion.json"),
        "cleanup": reference("cleanup.json", actor="synthetic-cleaner"),
        "independent_disposition": reference(
            "disposition.json", actor="synthetic-independent-reviewer",
            wave_id=WAVE, independent=True, disposition="cleanup-accounted"),
    }]}
    (repo / "required.json").write_bytes(json_bytes(required))
    (repo / "accounting.json").write_bytes(json_bytes(accounting))
    git(repo, env, "add", "--", "required.json", "accounting.json")
    git(repo, env, "commit", "-q", "-m", "Synthetic one-row positive-control accounting")
    protected = [evidence / name for name in payloads if name != "disposition.json"]
    protected += [twin, repo / "required.json", repo / "accounting.json", repo / ".git/index"]
    return target, protected, revision


def parse_audit(result: dict[str, Any]) -> dict[str, Any] | None:
    try:
        value = json.loads(result["stdout"])
    except (ValueError, TypeError):
        return None
    if not isinstance(value, dict) or value.get("schema") != AUDIT_SCHEMA:
        return None
    for key in COUNT_KEYS:
        rows = value.get(key + "_ids")
        if (type(value.get(key)) is not int or value[key] < 0
                or not isinstance(rows, list) or len(rows) != value[key]
                or any(not isinstance(row, dict) or row.get("id") != WAVE for row in rows)):
            return None
    if type(value.get("pin_allowed")) is not bool or not isinstance(value.get("issues"), list):
        return None
    return value


def positive(result: dict[str, Any]) -> bool:
    """Healthy receipt is structurally valid, not independently accepted."""
    value = parse_audit(result)
    expected = {"omitted": 0, "retained": 1, "unresolved": 1, "disposed": 1, "invalid": 0}
    review_issue = {
        "id": WAVE, "field": "disposition", "reason": "external_review_required",
        "finding_id": f"mori-evidence-loss:audit:{WAVE}:disposition:external_review_required",
    }
    return (result["returncode"] == 1 and value is not None
            and all(value[key] == count for key, count in expected.items())
            and value["disposed_ids"][0].get("status") == "structural_only"
            and value["unresolved_ids"][0].get("reason") == "external_review_required"
            and value.get("trust_basis") == "declared-record-not-authenticated"
            and value["pin_allowed"] is False and value["issues"] == [review_issue])


def refusal(result: dict[str, Any], reason: str) -> bool:
    value = parse_audit(result)
    expected_id = f"mori-evidence-loss:audit:{WAVE}:independent_disposition:{reason}"
    return (result["returncode"] == 1 and value is not None
            and value["omitted"] == 0 and value["disposed"] == 0
            and value["invalid"] >= 1 and value["pin_allowed"] is False
            and any(isinstance(issue, dict) and issue.get("id") == WAVE
                    and issue.get("field") == "independent_disposition"
                    and issue.get("reason") == reason and issue.get("finding_id") == expected_id
                    for issue in value["issues"]))


def probe(case: str, workspace: Path, evaluator: Path) -> dict[str, Any]:
    result: dict[str, Any] = {"case": case, "verdict": "inconclusive", "runs": {}}
    try:
        env = clean_env(workspace / (case + "-home"))
        repo = workspace / case
        target, protected, revision = make_fixture(repo, env)
        original = target.read_bytes()
        original_state = file_state(target)
        guard_paths = [*protected, evaluator]
        guards = {str(path): file_state(path) for path in guard_paths}
        result.update({"root": str(repo), "evidence_revision": revision,
                       "target": str(target), "before": original_state,
                       "protected_before": guards})
        argv = [sys.executable, "-I", "-B", str(evaluator), "audit", "--root", str(repo),
                "--required", str(repo / "required.json"),
                "--accounting", str(repo / "accounting.json")]

        def detect(phase: str) -> None:
            before = file_state(target)
            observed = command(argv, repo, env)
            observed["observed"] = parse_audit(observed)
            observed["evidence_before"] = before
            observed["evidence_after"] = file_state(target)
            result["runs"][phase] = observed

        try:
            detect("pristine")
            if case == "digest-mismatch":
                # One legal JSON whitespace byte; semantic disposition is unchanged.
                target.write_bytes(original + b" ")
            else:
                # Same digest, same root, no traversal: rejection must concern the link.
                target.unlink()
                target.symlink_to("disposition-twin.json")
            result["mutated"] = file_state(target)
            detect("mutated")
        except Exception as error:
            result["probe_error"] = {"type": type(error).__name__, "message": str(error)}
        finally:
            # Never write through the substituted link. Restore a regular file.
            target.unlink(missing_ok=True)
            target.write_bytes(original)
            target.chmod(original_state["mode"])
            result["after"] = file_state(target)
            result["restored_exactly"] = result["after"] == original_state
            detect("restored")

        result["protected_after"] = {str(path): file_state(path) for path in guard_paths}
        result["protected_unchanged"] = result["protected_after"] == guards
        runs = result["runs"]
        result["detector_read_only"] = all(
            run["evidence_before"] == run["evidence_after"] for run in runs.values())
        controls_ok = (set(runs) == {"pristine", "mutated", "restored"}
                       and positive(runs["pristine"]) and positive(runs["restored"])
                       and runs["pristine"]["observed"] == runs["restored"]["observed"]
                       and result["restored_exactly"] and result["protected_unchanged"]
                       and result["detector_read_only"] and "probe_error" not in result)
        mutation = result.get("mutated", {})
        injection_ok = (
            mutation.get("kind") == ("regular" if case == "digest-mismatch" else "symlink")
            and (mutation.get("sha256") != original_state["sha256"]
                 if case == "digest-mismatch" else mutation.get("sha256") == original_state["sha256"]))
        result["controls_ok"] = controls_ok
        result["injection_ok"] = injection_ok
        if controls_ok and injection_ok:
            observed = parse_audit(runs["mutated"])
            if refusal(runs["mutated"], "hash_mismatch" if case == "digest-mismatch" else "unsafe_symlink"):
                result.update(verdict="killed", reason="untrusted evidence refused with stable finding")
            elif observed is not None and (observed["pin_allowed"] or observed["disposed"] > 0
                                            or runs["mutated"]["returncode"] == 0):
                result.update(verdict="survived", reason="mutated evidence accepted or counted disposed")
            else:
                result["reason"] = "mutated detector lacked the specified refusal result"
        else:
            result["reason"] = "positive control, injection, read-only, or restoration guard failed"
    except Exception as error:
        result["error"] = {"type": type(error).__name__, "message": str(error)}
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit-script", type=Path, default=LANE / "tools/mori-evidence-loss.py")
    args = parser.parse_args()
    if Path(__file__).resolve().parent != SEAT.resolve() or SEAT.resolve() != SEAT:
        parser.error("run the proposal from its assigned, non-symlinked seat directory")
    workspace = Path(tempfile.mkdtemp(prefix="probe-", dir=SEAT))
    receipt: dict[str, Any] = {"schema": "mori-r21-mut-digest-trust-probe-v1",
        "workspace": str(workspace), "status": "inconclusive", "synthetic_only": True,
        "per_subprocess_timeout_seconds": TIMEOUT_SECONDS, "maximum_audit_calls": 6,
        "cases": [], "historical_disposition_claim": False}
    receipt["control_oracle"] = "co-evolved-structural-only-external-review-v1"
    receipt["frozen_contract_acceptance_claim"] = False
    status = 2
    try:
        source = args.audit_script.absolute()
        source.resolve(strict=True).relative_to(LANE.resolve())
        if source.is_symlink() or not source.is_file():
            raise ValueError("audit script must be a regular lane-local file")
        raw = source.read_bytes()
        evaluator = workspace / "evaluator.py"
        evaluator.write_bytes(raw)
        receipt["evaluator"] = {"source": str(source), "snapshot": str(evaluator),
                                 "sha256": sha256(raw)}
        with ThreadPoolExecutor(max_workers=2) as executor:
            receipt["cases"] = list(executor.map(
                lambda case: probe(case, workspace, evaluator),
                ("digest-mismatch", "symlink-substitution")))
        verdicts = [case["verdict"] for case in receipt["cases"]]
        if "inconclusive" in verdicts:
            receipt["status"] = "inconclusive"
        elif "survived" in verdicts:
            receipt["status"], status = "survived", 1
        else:
            receipt["status"], status = "killed", 0
    except Exception as error:
        receipt["error"] = {"type": type(error).__name__, "message": str(error)}
    receipt_path = workspace / "result.json"
    receipt_path.write_bytes(json_bytes(receipt))
    print(json.dumps({"status": receipt["status"], "receipt": str(receipt_path)}, sort_keys=True))
    return status


if __name__ == "__main__":
    raise SystemExit(main())
