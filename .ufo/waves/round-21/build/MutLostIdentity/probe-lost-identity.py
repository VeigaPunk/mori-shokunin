#!/usr/bin/env python3
"""Proposed round21 C1 probe; execute only when L1 authorizes verification.

Only a private accounting copy loses one row. The required identities, provenance
and evaluator bytes are frozen across three bounded audit calls. No census, pin,
classification, Git write, network operation or disposition synthesis is used.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path("/home/vgpnk/Projects/shokunin/mori-shokunin")
SEAT = ROOT / ".ufo/waves/round-21/build/MutLostIdentity"
IDS = {"aggregator-r10", "aggregator-r10-resume"}
DROPPED = "aggregator-r10-resume"
TIMEOUT = 15
OUTPUT_LIMIT = 1 << 20
COUNTERS = ("omitted", "retained", "unresolved", "disposed", "invalid")
CONTROL = dict(omitted=0, retained=2, unresolved=2, disposed=0, invalid=0,
               pin_allowed=False)
MUTATED = dict(omitted=1, retained=1, unresolved=1, disposed=0, invalid=0,
               pin_allowed=False)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def unique_object(pairs: list) -> dict:
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError("duplicate JSON object key")
        obj[key] = value
    return obj


def reject_constant(value: str) -> None:
    raise ValueError("non-finite JSON number: " + value)


def decode(data: bytes):
    return json.loads(data.decode("utf-8"), object_pairs_hook=unique_object,
                      parse_constant=reject_constant)


def encode(value) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def source_path(root: Path, value: str) -> Path:
    path = Path(value)
    path = (path if path.is_absolute() else root / path).resolve(strict=True)
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError("all source files must be regular files beneath --root")
    return path


def rows(document, schema: str) -> dict:
    if not isinstance(document, dict) or document.get("schema") != schema:
        raise ValueError("unexpected input schema: " + schema)
    observations = document.get("observations")
    if not isinstance(observations, list) or len(observations) != 2:
        raise ValueError("control must contain exactly two historical identities")
    if any(not isinstance(row, dict) or not isinstance(row.get("id"), str)
           for row in observations):
        raise ValueError("control observation must have a string id")
    by_id = {row["id"]: row for row in observations}
    if set(by_id) != IDS or len(by_id) != len(observations):
        raise ValueError("control identity set must be exactly the two r10 waves")
    return by_id


def fingerprints(paths: dict) -> dict:
    return {name: file_digest(path) for name, path in paths.items()}


def audit(phase: str, command: list, root: Path, run: Path,
          copies: dict, expected_hashes: dict) -> dict:
    stdout_path = run / (phase + ".stdout.json")
    stderr_path = run / (phase + ".stderr.txt")
    record = {"command": command, "timeout_seconds": TIMEOUT,
              "stdout_path": str(stdout_path), "stderr_path": str(stderr_path),
              "returncode": None, "errors": [],
              "input_hashes_before": fingerprints(copies)}
    if record["input_hashes_before"] != expected_hashes:
        record["errors"].append("phase input bytes do not match frozen copies")
    env = {"PATH": "/usr/local/bin:/usr/bin:/bin", "LC_ALL": "C",
           "TMPDIR": str(ROOT / ".scratch"), "PYTHONDONTWRITEBYTECODE": "1",
           "PYTHONIOENCODING": "utf-8", "GIT_OPTIONAL_LOCKS": "0",
           "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null",
           "GIT_CONFIG_NOSYSTEM": "1"}
    with stdout_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
        try:
            completed = subprocess.run(command, cwd=root, env=env,
                                       stdin=subprocess.DEVNULL, stdout=stdout,
                                       stderr=stderr, timeout=TIMEOUT, check=False)
            record["returncode"] = completed.returncode
        except subprocess.TimeoutExpired:
            record["errors"].append("audit timeout")
        except OSError as exc:
            record["errors"].append(type(exc).__name__ + ": " + str(exc))
    record["input_hashes_after"] = fingerprints(copies)
    if record["input_hashes_after"] != expected_hashes:
        record["errors"].append("audit changed frozen input bytes")
    record["stdout_sha256"] = file_digest(stdout_path)
    record["stderr_sha256"] = file_digest(stderr_path)
    with stdout_path.open("rb") as stream:
        raw = stream.read(OUTPUT_LIMIT + 1)
    try:
        if len(raw) > OUTPUT_LIMIT:
            raise ValueError("audit JSON exceeds one MiB parsing bound")
        observed = decode(raw)
        if not isinstance(observed, dict):
            raise ValueError("audit output must be a JSON object")
        if observed.get("schema") != "mori-evidence-loss-audit-v1":
            raise ValueError("unexpected audit output schema")
        if any(type(observed.get(key)) is not int or observed[key] < 0
               for key in COUNTERS):
            raise ValueError("audit counters must be nonnegative integers")
        if type(observed.get("pin_allowed")) is not bool or "issues" not in observed:
            raise ValueError("audit must report boolean pin_allowed and issues")
        record["observed"] = observed
    except (ValueError, UnicodeError) as exc:
        record["errors"].append(type(exc).__name__ + ": " + str(exc))
    if record["returncode"] not in (0, 1):
        record["errors"].append("audit setup failure or abnormal exit")
    return record


def differences(record: dict, expected: dict) -> list:
    problems = list(record["errors"])
    if record["returncode"] != 1:
        problems.append("expected rc1: unresolved evidence deliberately blocks pin")
    observed = record.get("observed", {})
    for field, value in expected.items():
        if field not in observed or observed[field] != value:
            problems.append(field + ": expected " + repr(value) +
                            ", observed " + repr(observed.get(field)))
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True)
    parser.add_argument("--required", required=True,
                        help="complete two-identity required fixture, relative to root")
    parser.add_argument("--accounting", required=True,
                        help="valid complete unresolved accounting, relative to root")
    parser.add_argument("--evaluator", default="tools/mori-evidence-loss.py")
    args = parser.parse_args()
    # Refuse relocation so this proposal cannot write outside its assigned seat.
    if Path(__file__).resolve().parent != SEAT or SEAT.resolve() != SEAT:
        parser.error("probe must remain in its non-symlink assigned seat directory")
    run = Path(tempfile.mkdtemp(prefix="omission-", dir=SEAT))
    result = {"schema": "mori-r21-lost-identity-probe-v1", "verdict": "inconclusive",
              "mutation": {"operation": "remove one accounting observation",
                           "id": DROPPED, "required_set_unchanged": True},
              "expected": {"pristine": CONTROL, "mutated": MUTATED,
                           "restored": CONTROL, "returncode_each": 1},
              "scope": "historical accounting only; both wave lifecycles remain unknown",
              "run_directory": str(run), "errors": [], "phases": {}}
    sources = {}
    snapshots = {}
    accounting_copy = None
    try:
        root = Path(args.root).resolve(strict=True)
        if root != ROOT:
            raise ValueError("--root must be the assigned own-lane repository")
        sources = {"required": source_path(root, args.required),
                   "accounting": source_path(root, args.accounting),
                   "evaluator": source_path(root, args.evaluator)}
        snapshots = {name: path.read_bytes() for name, path in sources.items()}
        result["source_paths"] = {name: str(path) for name, path in sources.items()}
        result["source_hashes_before"] = {name: digest(raw)
                                          for name, raw in snapshots.items()}
        required = decode(snapshots["required"])
        original = decode(snapshots["accounting"])
        rows(required, "mori-required-observations-v1")
        accounting_rows = rows(original, "mori-loss-accounting-v1")
        for row in accounting_rows.values():
            if (row.get("state") != "unresolved" or
                    "independent_disposition" not in row or
                    row["independent_disposition"] is not None):
                raise ValueError("control must retain both waves unresolved, disposition null")
        mutant = dict(original)
        mutant["observations"] = [row for row in original["observations"]
                                  if row["id"] != DROPPED]
        mutant_bytes = encode(mutant)
        copies = {"required": run / "required.json",
                  "accounting": run / "accounting.json",
                  "evaluator": run / "evaluator.py"}
        for name, path in copies.items():
            path.write_bytes(snapshots[name])
        accounting_copy = copies["accounting"]
        pristine_hashes = {name: digest(raw) for name, raw in snapshots.items()}
        mutant_hashes = dict(pristine_hashes, accounting=digest(mutant_bytes))
        result["accounting_hashes_expected"] = {
            "pristine": pristine_hashes["accounting"],
            "mutated": mutant_hashes["accounting"],
            "restored": pristine_hashes["accounting"]}
        command = [sys.executable, str(copies["evaluator"]), "audit", "--root", str(root),
                   "--required", str(copies["required"]),
                   "--accounting", str(accounting_copy)]
        try:
            result["phases"]["pristine"] = audit(
                "pristine", command, root, run, copies, pristine_hashes)
            accounting_copy.write_bytes(mutant_bytes)
            result["phases"]["mutated"] = audit(
                "mutated", command, root, run, copies, mutant_hashes)
        finally:
            # Exact source bytes, not JSON reserialization, even on detector failure.
            accounting_copy.write_bytes(snapshots["accounting"])
            result["restored_exact_bytes"] = (
                accounting_copy.read_bytes() == snapshots["accounting"])
            result["restored_sha256"] = file_digest(accounting_copy)
            result["phases"]["restored"] = audit(
                "restored", command, root, run, copies, pristine_hashes)
        result["expectation_failures"] = {
            phase: differences(result["phases"][phase], expected)
            for phase, expected in (("pristine", CONTROL), ("mutated", MUTATED),
                                    ("restored", CONTROL))}
        failures = result["expectation_failures"]
        if not failures["pristine"] and not failures["restored"]:
            if not result["phases"]["mutated"]["errors"]:
                result["verdict"] = "survived" if failures["mutated"] else "killed"
    except Exception as exc:
        result["errors"].append(type(exc).__name__ + ": " + str(exc))
    finally:
        if accounting_copy is not None:
            try:
                accounting_copy.write_bytes(snapshots["accounting"])
                result["restored_exact_bytes"] = (
                    accounting_copy.read_bytes() == snapshots["accounting"])
                result["restored_sha256"] = file_digest(accounting_copy)
            except OSError as exc:
                result["errors"].append("restoration failed: " + str(exc))
        if snapshots:
            try:
                result["source_hashes_after"] = fingerprints(sources)
                result["sources_unchanged"] = (
                    result["source_hashes_after"] == result["source_hashes_before"])
            except OSError as exc:
                result["sources_unchanged"] = False
                result["errors"].append("source rehash failed: " + str(exc))
        if (result["errors"] or not result.get("restored_exact_bytes", False) or
                not result.get("sources_unchanged", False)):
            result["verdict"] = "inconclusive"
        result_path = run / "result.json"
        result["result_path"] = str(result_path)
        payload = encode(result)
        result_path.write_bytes(payload)
        sys.stdout.buffer.write(payload)
    return {"killed": 0, "survived": 1, "inconclusive": 2}[result["verdict"]]


if __name__ == "__main__":
    raise SystemExit(main())
