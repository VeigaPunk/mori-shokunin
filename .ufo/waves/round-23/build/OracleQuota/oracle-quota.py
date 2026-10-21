#!/usr/bin/env python3
"""Round-23 C2 oracle: sealed quota-surface fixture cases plus the frozen real control.

Authored blind: from the pre-registered contract only (no implementation, no proposed
case contents).  The oracle is a measurement instrument, not a re-implementation of the
probe: it only executes the candidate tool, compares the documented public facets and
records the evidence needed to audit the comparison.

CLI
---
  --tool PATH            candidate probe (e.g. tools/mori-quota-surface.py)
  --cases DIR            directory of sealed case files (*.json, sorted by name)
  --output FILE          where the observation record is written
  --real-expected FILE   optional frozen real-control file (see frozen/c2-expected-real.json)

Per case (one *.json file per case, sorted by file name)
  * case['fixture']  -> written verbatim to a fixture file beside --output
  * the tool is run as [sys.executable, TOOL, '--fixture', <fixture file>] (30 s timeout)
  * stdout must parse as exactly one JSON object
  * compared facets: process exit code, 'finding_id', and the ordered per-path tuples
    (path, fstype, mount_point, quota_state, enforcement, basis) against case['expected']

If the tool file is absent every case is recorded as 'capability_absent' (not a failure:
absence is the pre-registered "before" state).

With --real-expected the tool is additionally run with its default paths
([sys.executable, TOOL]) and compared against the frozen expected_exit /
expected_finding_id / expected_paths, where the per-path tuples also carry
'device_check'.

Exit status: 0 iff no check is 'unmet' (mismatch or error).  'capability_absent'
checks are counted separately and never make the run fail.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ORACLE_SCHEMA = "mori-r23-c2-oracle-v1"
CASE_TIMEOUT_S = 30
REAL_TIMEOUT_S = 30

# The ordered per-path tuple compared for fixture cases.
PATH_FIELDS = ("path", "fstype", "mount_point", "quota_state", "enforcement", "basis")
# The frozen real control additionally pins the device check.
REAL_PATH_FIELDS = PATH_FIELDS + ("device_check",)

# Case files are authored independently of this oracle; the key spellings below are the
# contract's own vocabulary plus the obvious synonyms.  Every alias actually used is
# recorded in the observation file, so a mismatch in spelling is visible, not hidden.
EXIT_KEYS = ("exit_code", "exit", "expected_exit", "returncode", "return_code")
FINDING_KEYS = ("finding_id", "finding", "expected_finding_id", "expected_finding")
PATHS_KEYS = ("paths", "expected_paths", "path_expectations", "per_path", "path_rows")
FIXTURE_KEYS = ("fixture", "fixture_json", "fixture_object", "fixture_data", "fixture_document")


def digest_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def digest_file(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def pick(mapping, keys):
    """Return (value, key_used) for the first present key."""
    if not isinstance(mapping, dict):
        return None, None
    for key in keys:
        if key in mapping:
            return mapping[key], key
    return None, None


def as_int(value):
    """Exit codes are integers; a numeric string is accepted and recorded."""
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.strip().lstrip("+").isdigit():
        return int(value.strip())
    return None


def norm_expected_paths(raw, fields):
    """Normalise an expected path list into an ordered list of tuples.

    Entries may be objects keyed by the field names, or arrays carrying the fields in
    the documented order.  Returns (tuples, recognised).
    """
    if raw is None:
        return [], True
    if not isinstance(raw, list):
        return None, False
    out = []
    for entry in raw:
        if isinstance(entry, dict):
            out.append(tuple(entry.get(f) for f in fields))
        elif isinstance(entry, (list, tuple)) and len(entry) == len(fields):
            out.append(tuple(entry))
        else:
            return None, False
    return out, True


def norm_observed_paths(parsed, fields):
    """Extract the ordered per-path tuples from a parsed tool JSON object."""
    if not isinstance(parsed, dict):
        return None
    rows = parsed.get("paths")
    if rows is None:
        return None
    if not isinstance(rows, list):
        return None
    out = []
    for entry in rows:
        if isinstance(entry, dict):
            out.append(tuple(entry.get(f) for f in fields))
        elif isinstance(entry, (list, tuple)) and len(entry) == len(fields):
            out.append(tuple(entry))
        else:
            return None
    return out


def run_tool(argv, timeout):
    """Run the tool and capture argv, exit, stdout, stderr (bytes decoded safely)."""
    record = {"argv": list(argv), "exit": None, "stdout": "", "stderr": "", "timeout": False}
    try:
        completed = subprocess.run(list(argv), capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        record["timeout"] = True
        record["stdout"] = _decode(exc.stdout)
        record["stderr"] = _decode(exc.stderr)
        return record
    except OSError as exc:
        record["stderr"] = "oracle: tool invocation failed: %s" % (exc.__class__.__name__,)
        return record
    record["exit"] = completed.returncode
    record["stdout"] = completed.stdout if isinstance(completed.stdout, str) else _decode(completed.stdout)
    record["stderr"] = completed.stderr if isinstance(completed.stderr, str) else _decode(completed.stderr)
    return record


def _decode(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    try:
        return value.decode("utf-8", "replace")
    except AttributeError:
        return str(value)


def parse_stdout_object(text):
    """Parse stdout as exactly one JSON object; returns (obj, reason)."""
    if text is None or text.strip() == "":
        return None, "stdout_empty"
    try:
        value = json.loads(text)
    except ValueError:
        return None, "stdout_not_json"
    if not isinstance(value, dict):
        return None, "stdout_not_json_object"
    return value, None


def write_fixture(fixture, destination: Path) -> str:
    """Write case['fixture'] to a file beside the output; returns the sha256."""
    if isinstance(fixture, str):
        payload = fixture if fixture.endswith("\n") else fixture + "\n"
    else:
        payload = json.dumps(fixture, indent=2, sort_keys=True) + "\n"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(payload, encoding="utf-8")
    return digest_bytes(payload.encode("utf-8"))


def compare_case(case_obj, parsed, exit_code):
    """Compare exit code, finding id and ordered per-path tuples; returns (ok, details)."""
    details = {"exit_match": False, "finding_match": False, "paths_match": False}
    expected = case_obj.get("expected")
    if isinstance(expected, list):
        # A case may pin only the ordered per-path tuples inside 'expected'; the exit
        # code and finding id then come from the case root.
        expected = {"paths": expected}
    if not isinstance(expected, dict):
        details["reason"] = "case_expected_missing_or_not_object"
        return False, details

    exp_exit, exit_key = pick(expected, EXIT_KEYS)
    exp_finding, finding_key = pick(expected, FINDING_KEYS)
    exp_paths, paths_key = pick(expected, PATHS_KEYS)
    # Case authors may pin the exit/finding at the case root instead of inside
    # 'expected'; the fallback is recorded so the spelling in use stays auditable.
    if exit_key is None:
        exp_exit, exit_key = pick(case_obj, EXIT_KEYS)
        if exit_key is not None:
            exit_key = "case_root:" + exit_key
    if finding_key is None:
        exp_finding, finding_key = pick(case_obj, FINDING_KEYS)
        if finding_key is not None:
            finding_key = "case_root:" + finding_key
    if paths_key is None:
        exp_paths, paths_key = pick(case_obj, PATHS_KEYS)
        if paths_key is not None:
            paths_key = "case_root:" + paths_key
    details["expected_keys_used"] = {
        "exit": exit_key,
        "finding_id": finding_key,
        "paths": paths_key,
    }
    details["expected_exit"] = exp_exit
    details["expected_finding_id"] = exp_finding

    if exit_key is None or finding_key is None:
        details["reason"] = "expected_shape_unrecognised"
        return False, details

    details["exit_match"] = as_int(exp_exit) is not None and exit_code == as_int(exp_exit)

    obs_finding = None
    if isinstance(parsed, dict):
        obs_finding = parsed.get("finding_id", parsed.get("finding"))
    details["observed_finding_id"] = obs_finding
    details["finding_match"] = obs_finding == exp_finding

    exp_tuples, recognised = norm_expected_paths(exp_paths, PATH_FIELDS)
    if not recognised:
        details["reason"] = "expected_paths_unrecognised"
        return False, details
    obs_tuples = norm_observed_paths(parsed, PATH_FIELDS)
    details["expected_paths"] = [list(t) for t in exp_tuples]
    details["observed_paths"] = None if obs_tuples is None else [list(t) for t in obs_tuples]
    details["paths_match"] = obs_tuples is not None and obs_tuples == exp_tuples
    if obs_tuples is None:
        details["reason"] = "observed_paths_unrecognised"
        return False, details

    ok = details["exit_match"] and details["finding_match"] and details["paths_match"]
    if not ok:
        details["reason"] = "facet_mismatch"
    return ok, details


def compare_real(expected_obj, parsed, exit_code):
    """Compare the frozen real control (exit, finding id, per-path tuples + device_check)."""
    details = {"exit_match": False, "finding_match": False, "paths_match": False}
    exp_exit, exit_key = pick(expected_obj, EXIT_KEYS)
    exp_finding, finding_key = pick(expected_obj, FINDING_KEYS)
    exp_paths, paths_key = pick(expected_obj, PATHS_KEYS)
    details["expected_keys_used"] = {"exit": exit_key, "finding_id": finding_key, "paths": paths_key}
    details["expected_exit"] = exp_exit
    details["expected_finding_id"] = exp_finding
    if exit_key is None or finding_key is None or paths_key is None:
        details["reason"] = "real_expected_shape_unrecognised"
        return False, details
    details["exit_match"] = as_int(exp_exit) is not None and exit_code == as_int(exp_exit)
    obs_finding = None
    if isinstance(parsed, dict):
        obs_finding = parsed.get("finding_id", parsed.get("finding"))
    details["observed_finding_id"] = obs_finding
    details["finding_match"] = obs_finding == exp_finding
    exp_tuples, recognised = norm_expected_paths(exp_paths, REAL_PATH_FIELDS)
    if not recognised:
        details["reason"] = "real_expected_paths_unrecognised"
        return False, details
    obs_tuples = norm_observed_paths(parsed, REAL_PATH_FIELDS)
    details["expected_paths"] = [list(t) for t in exp_tuples]
    details["observed_paths"] = None if obs_tuples is None else [list(t) for t in obs_tuples]
    details["paths_match"] = obs_tuples is not None and obs_tuples == exp_tuples
    if obs_tuples is None:
        details["reason"] = "observed_paths_unrecognised"
        return False, details
    ok = details["exit_match"] and details["finding_match"] and details["paths_match"]
    if not ok:
        details["reason"] = "facet_mismatch"
    return ok, details


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="oracle-quota.py",
        description="Round-23 C2 oracle for the mori quota-surface probe.",
    )
    parser.add_argument("--tool", required=True, help="candidate probe path")
    parser.add_argument("--cases", required=True, help="directory of sealed case files")
    parser.add_argument("--output", required=True, help="observation record path")
    parser.add_argument("--real-expected", default=None, help="frozen real-control file")
    args = parser.parse_args(argv)

    tool = Path(args.tool)
    cases_dir = Path(args.cases)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fixture_dir = out_path.parent / (out_path.stem + "-quota-fixtures")

    oracle_path = Path(__file__).resolve()
    observation = {
        "schema": ORACLE_SCHEMA,
        "oracle": {"path": str(oracle_path), "sha256": digest_file(oracle_path)},
        "argv": list(sys.argv),
        "tool": {
            "path": str(tool),
            "exists": tool.is_file(),
            "sha256": digest_file(tool) if tool.is_file() else None,
        },
        "cases_dir": str(cases_dir),
        "cases": [],
        "cases_sha256": {},
        "fixture_dir": str(fixture_dir),
        "results": [],
        "runs": [],
        "real_control": None,
    }

    case_files = sorted(p for p in cases_dir.glob("*.json") if p.is_file()) if cases_dir.is_dir() else []
    observation["case_files"] = [str(p) for p in case_files]
    for case_file in case_files:
        case_bytes = case_file.read_bytes()
        observation["cases_sha256"][case_file.name] = digest_bytes(case_bytes)
        observation["cases"].append(
            {"name": case_file.name, "path": str(case_file), "sha256": observation["cases_sha256"][case_file.name]}
        )
    observation["cases_sha256_combined"] = digest_bytes(
        b"".join(
            observation["cases_sha256"][p.name].encode("ascii") + b" " + p.name.encode("utf-8") + b"\n"
            for p in case_files
        )
    )

    tool_present = tool.is_file()

    for case_file in case_files:
        name = case_file.name
        row = {
            "case": name,
            "case_path": str(case_file),
            "case_sha256": observation["cases_sha256"][name],
            "status": "unmet",
            "reason": None,
            "details": None,
            "run": None,
            "fixture_path": None,
            "fixture_sha256": None,
        }
        if not tool_present:
            row["status"] = "capability_absent"
            row["reason"] = "tool_absent"
            observation["results"].append(row)
            continue
        try:
            case_obj = json.loads(case_file.read_bytes())
        except ValueError:
            row["reason"] = "case_file_not_json"
            observation["results"].append(row)
            continue
        if not isinstance(case_obj, dict):
            row["reason"] = "case_file_not_json_object"
            observation["results"].append(row)
            continue
        fixture, fixture_key = pick(case_obj, FIXTURE_KEYS)
        if fixture is None:
            for nested_key in ("input", "inputs", "case"):
                nested = case_obj.get(nested_key)
                if isinstance(nested, dict):
                    fixture, fixture_key = pick(nested, FIXTURE_KEYS)
                    if fixture is not None:
                        fixture_key = nested_key + "." + fixture_key
                        break
        row["fixture_key_used"] = fixture_key
        if fixture is None:
            row["reason"] = "case_missing_fixture"
            observation["results"].append(row)
            continue
        fixture_path = fixture_dir / (case_file.stem + ".fixture.json")
        try:
            row["fixture_sha256"] = write_fixture(fixture, fixture_path)
        except OSError as exc:
            row["reason"] = "fixture_write_failed: %s" % (exc.__class__.__name__,)
            observation["results"].append(row)
            continue
        row["fixture_path"] = str(fixture_path)
        cmd = [sys.executable, str(tool), "--fixture", str(fixture_path)]
        run = run_tool(cmd, CASE_TIMEOUT_S)
        observation["runs"].append(run)
        row["run"] = run
        if run["timeout"]:
            row["reason"] = "tool_timeout"
            observation["results"].append(row)
            continue
        parsed, parse_reason = parse_stdout_object(run["stdout"])
        row["stdout_parsed"] = parsed is not None
        if parsed is None:
            row["reason"] = parse_reason
            observation["results"].append(row)
            continue
        ok, details = compare_case(case_obj, parsed, run["exit"])
        row["details"] = details
        row["status"] = "pass" if ok else "unmet"
        row["reason"] = details.get("reason")
        observation["results"].append(row)

    if args.real_expected:
        real_path = Path(args.real_expected)
        entry = {
            "status": "unmet",
            "reason": None,
            "file": str(real_path),
            "sha256": digest_file(real_path) if real_path.is_file() else None,
            "run": None,
            "details": None,
        }
        if not real_path.is_file():
            entry["status"] = "unmet"
            entry["reason"] = "real_expected_absent"
            observation["real_control"] = entry
        elif not tool_present:
            entry["status"] = "capability_absent"
            entry["reason"] = "tool_absent"
            observation["real_control"] = entry
        else:
            try:
                expected_obj = json.loads(real_path.read_bytes())
            except ValueError:
                expected_obj = None
            if not isinstance(expected_obj, dict):
                entry["reason"] = "real_expected_not_json_object"
            else:
                cmd = [sys.executable, str(tool)]
                run = run_tool(cmd, REAL_TIMEOUT_S)
                observation["runs"].append(run)
                entry["run"] = run
                if run["timeout"]:
                    entry["reason"] = "tool_timeout"
                else:
                    parsed, parse_reason = parse_stdout_object(run["stdout"])
                    entry["stdout_parsed"] = parsed is not None
                    if parsed is None:
                        entry["reason"] = parse_reason
                    else:
                        ok, details = compare_real(expected_obj, parsed, run["exit"])
                        entry["details"] = details
                        entry["status"] = "pass" if ok else "unmet"
                        entry["reason"] = details.get("reason")
        observation["real_control"] = entry

    checks = list(observation["results"])
    if observation["real_control"] is not None:
        checks.append(
            {
                "case": "<real-control>",
                "status": observation["real_control"]["status"],
                "reason": observation["real_control"].get("reason"),
                "details": observation["real_control"].get("details"),
                "run": observation["real_control"].get("run"),
                "case_sha256": observation["real_control"].get("sha256"),
            }
        )
    counts = {
        "total": len(checks),
        "pass": sum(1 for c in checks if c["status"] == "pass"),
        "capability_absent": sum(1 for c in checks if c["status"] == "capability_absent"),
        "unmet": sum(1 for c in checks if c["status"] == "unmet"),
    }
    counts["cases_total"] = len(observation["results"])
    counts["cases_pass"] = sum(1 for r in observation["results"] if r["status"] == "pass")
    counts["cases_capability_absent"] = sum(1 for r in observation["results"] if r["status"] == "capability_absent")
    counts["cases_unmet"] = sum(1 for r in observation["results"] if r["status"] == "unmet")
    observation["counts"] = counts
    observation["checks"] = checks

    out_path.write_text(json.dumps(observation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if counts["unmet"]:
        finding = "R23_C2_QUOTA_CASES_UNMET"
    elif counts["pass"] == 0 and counts["capability_absent"]:
        # Pre-registered "before" state: the probe does not exist yet.  Absence is
        # reported, never dressed up as a match.
        finding = "R23_C2_QUOTA_CAPABILITY_ABSENT"
    else:
        finding = "R23_C2_QUOTA_CASES_MATCH"
    summary = {
        "schema": ORACLE_SCHEMA,
        "finding_id": finding,
        "counts": counts,
        "output": str(out_path),
        "tool_present": tool_present,
    }
    print(json.dumps(summary, sort_keys=True))
    return 0 if counts["unmet"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
