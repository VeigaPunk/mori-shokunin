#!/usr/bin/env python3
"""Round-23 C2 oracle v2 (strict) — sealed quota-surface cases plus the frozen real control.

Companion to oracle-quota.py (which stays immutable).  v1 was tolerant of key
spellings because the case authors and the oracle were independent.  v2 is the
strict instrument requested by the pre-seal amendment: one exact case schema, no
aliases, no missing expected paths, and the supplementary sealed checks
(schema / exit / key set / device_check / quota options / qgroups mode / leakage).

Case schema (exact, enforced):
  case file   : {"fixture": <object>, "expected": <object>}          -- exactly these two keys
  expected    : {"exit_code": int, "finding_id": str, "paths": [...]} -- exactly these three keys
  path entry  : exactly {"path","fstype","mount_point","quota_state","enforcement","basis"}
                plus, optionally, "device_check", "quota_option_keys", "btrfs_qgroups_mode"
                (the three supplementary fields, compared when the case pins them)

Headline (scored, unchanged denominator): exit code + finding_id + the ordered
six-field per-path tuples.  Supplementary checks are reported separately and never
fold into the headline denominator.

CLI:
  --tool PATH --cases DIR --output FILE [--real-expected FILE]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ORACLE_SCHEMA = "mori-r23-c2-oracle-v2"
TOOL_SCHEMA = "mori-quota-surface-v1"

CASE_KEYS = {"fixture", "expected"}
EXPECTED_KEYS = {"exit_code", "finding_id", "paths"}
PATH_KEYS = ("path", "fstype", "mount_point", "quota_state", "enforcement", "basis")
SUPP_PATH_KEYS = ("device_check", "quota_option_keys", "btrfs_qgroups_mode")
ALLOWED_PATH_KEYS = set(PATH_KEYS) | set(SUPP_PATH_KEYS)
OUTPUT_KEYS = {"schema", "finding_id", "exit_code", "paths", "df_covers_quota", "limits"}
DEVICE_CHECK_VALUES = {"match", "mismatch", "not_checked", "btrfs_subvolume_skipped"}
QGROUP_MODES = {"qgroup", "squota"}
TIMEOUT_S = 30
OCTAL = {"040": " ", "011": "\t", "012": "\n", "134": "\\"}


def sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def decode_octal(text: str) -> str:
    for code, char in OCTAL.items():
        text = text.replace("\\" + code, char)
    return text


def run_tool(argv):
    record = {"argv": list(argv), "exit": None, "stdout": "", "stderr": "", "timeout": False}
    try:
        done = subprocess.run(list(argv), capture_output=True, text=True, timeout=TIMEOUT_S)
    except subprocess.TimeoutExpired as exc:
        record["timeout"] = True
        record["stdout"] = exc.stdout if isinstance(exc.stdout, str) else (exc.stdout or b"").decode("utf-8", "replace")
        record["stderr"] = exc.stderr if isinstance(exc.stderr, str) else (exc.stderr or b"").decode("utf-8", "replace")
        return record
    except OSError as exc:
        record["stderr"] = "oracle: tool invocation failed: %s" % (exc.__class__.__name__,)
        return record
    record["exit"] = done.returncode
    record["stdout"] = done.stdout or ""
    record["stderr"] = done.stderr or ""
    return record


def path_tuples(entries):
    return [tuple(entry.get(field) for field in PATH_KEYS) for entry in entries]


def leakage_hits(stdout_text, fixture):
    """Device / uuid / option-value leakage into the tool output."""
    hits = []
    text = stdout_text or ""
    sysfs = fixture.get("btrfs_sysfs") if isinstance(fixture, dict) else None
    for uuid in sysfs if isinstance(sysfs, dict) else []:
        if uuid and uuid in text:
            hits.append("uuid:" + uuid)
    mountinfo = fixture.get("mountinfo") if isinstance(fixture, dict) else None
    for line in (mountinfo or "").splitlines():
        fields = line.strip().split()
        if len(fields) < 3:
            continue
        source = fields[-2]
        for candidate in {source, decode_octal(source)}:
            if candidate.startswith("/") and candidate in text:
                hits.append("mount_source:" + candidate)
        for token in fields[-1].split(","):
            if "=" not in token:
                continue
            if token in text:
                hits.append("option_value:" + token)
            value = token.split("=", 1)[1]
            if len(value) >= 4 and not value.isdigit() and value in text:
                hits.append("option_value_only:" + value)
    return hits


def supplementary_checks(parsed, exit_code, observed_paths, expected_paths, fixture, stdout_text):
    """Supplementary sealed checks; each entry is (name, status, detail)."""
    checks = []

    def add(name, ok, detail):
        checks.append({"check": name, "status": "pass" if ok else "unmet", "detail": detail})

    add("schema", parsed.get("schema") == TOOL_SCHEMA, parsed.get("schema"))
    add("exit_consistency", parsed.get("exit_code") == exit_code, parsed.get("exit_code"))
    add("output_key_set", set(parsed) == OUTPUT_KEYS, sorted(parsed))
    add(
        "path_key_set",
        all(set(entry) == ALLOWED_PATH_KEYS for entry in observed_paths),
        [sorted(entry) for entry in observed_paths],
    )
    add("df_covers_quota", parsed.get("df_covers_quota") is False, parsed.get("df_covers_quota"))
    limits = parsed.get("limits")
    add("limits_text", isinstance(limits, str) and limits.strip() != "", type(limits).__name__)

    for index, want in enumerate(expected_paths):
        got = observed_paths[index] if index < len(observed_paths) else {}
        for key in SUPP_PATH_KEYS:
            if key not in want:
                continue
            value = got.get(key)
            if key == "device_check":
                add("device_check[%d]" % index, value == want[key] and value in DEVICE_CHECK_VALUES, value)
            elif key == "quota_option_keys":
                shape = isinstance(value, list) and all(isinstance(item, str) for item in value)
                shape = shape and value == sorted(set(value))
                add("quota_option_keys[%d]" % index, value == want[key] and shape, value)
            else:
                ok = value == want[key] and (value is None or value in QGROUP_MODES)
                add("btrfs_qgroups_mode[%d]" % index, ok, value)

    if isinstance(fixture, dict) and fixture:
        # Leakage can only be judged against the fixture the tool was given; the real
        # control has no fixture basis, so the check is skipped there, never faked.
        hits = leakage_hits(stdout_text, fixture)
        add("no_leakage", not hits, hits)
    return checks


def evaluate_case(case_obj, parsed, exit_code, stdout_text):
    """Strict headline evaluation of one case; returns (ok, headline, supplementary)."""
    headline = {"exit_match": False, "finding_match": False, "paths_match": False}
    if set(case_obj) != CASE_KEYS:
        return False, headline, [], "case_key_set:%s" % sorted(case_obj)
    expected = case_obj["expected"]
    if not isinstance(expected, dict):
        return False, headline, [], "expected_not_object"
    if set(expected) != EXPECTED_KEYS:
        return False, headline, [], "expected_key_set:%s" % sorted(expected)
    expected_paths = expected["paths"]
    if not isinstance(expected_paths, list):
        return False, headline, [], "expected_paths_not_list"
    for entry in expected_paths:
        if not isinstance(entry, dict):
            return False, headline, [], "expected_path_not_object"
        if not set(PATH_KEYS) <= set(entry) or not set(entry) <= ALLOWED_PATH_KEYS:
            return False, headline, [], "expected_path_key_set:%s" % sorted(entry)
    observed_paths = parsed.get("paths")
    if not isinstance(observed_paths, list) or not all(isinstance(entry, dict) for entry in observed_paths):
        return False, headline, [], "observed_paths_not_object_list"

    headline["exit_match"] = exit_code == expected["exit_code"]
    headline["finding_match"] = parsed.get("finding_id") == expected["finding_id"]
    headline["paths_match"] = path_tuples(observed_paths) == path_tuples(expected_paths)
    supplementary = supplementary_checks(
        parsed, exit_code, observed_paths, expected_paths, case_obj["fixture"], stdout_text
    )
    ok = headline["exit_match"] and headline["finding_match"] and headline["paths_match"]
    return ok, headline, supplementary, None


def evaluate_real(expected_obj, parsed, exit_code, stdout_text):
    """Strict evaluation of the frozen real control (exit, finding, 7-field paths)."""
    headline = {"exit_match": False, "finding_match": False, "paths_match": False}
    want_exit = expected_obj.get("expected_exit")
    want_finding = expected_obj.get("expected_finding_id")
    want_paths = expected_obj.get("expected_paths")
    if not isinstance(want_paths, list):
        return False, headline, [], "real_expected_paths_not_list"
    fields = PATH_KEYS + ("device_check",)
    for entry in want_paths:
        if not isinstance(entry, dict):
            return False, headline, [], "real_expected_path_not_object"
        if set(entry) != set(fields):
            return False, headline, [], "real_expected_path_key_set:%s" % sorted(entry)
    observed_paths = parsed.get("paths")
    if not isinstance(observed_paths, list) or not all(isinstance(entry, dict) for entry in observed_paths):
        return False, headline, [], "observed_paths_not_object_list"
    headline["exit_match"] = exit_code == want_exit
    headline["finding_match"] = parsed.get("finding_id") == want_finding
    headline["paths_match"] = [
        tuple(entry.get(field) for field in fields) for entry in observed_paths
    ] == [tuple(entry.get(field) for field in fields) for entry in want_paths]
    supplementary = supplementary_checks(parsed, exit_code, observed_paths, want_paths, None, stdout_text)
    ok = headline["exit_match"] and headline["finding_match"] and headline["paths_match"]
    return ok, headline, supplementary, None


def count_checks(checks):
    return {
        "total": len(checks),
        "pass": sum(1 for check in checks if check["status"] == "pass"),
        "unmet": sum(1 for check in checks if check["status"] == "unmet"),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(prog="oracle-quota-v2.py", description="Round-23 C2 strict oracle.")
    parser.add_argument("--tool", required=True)
    parser.add_argument("--cases", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--real-expected", default=None)
    args = parser.parse_args(argv)

    tool = Path(args.tool)
    cases_dir = Path(args.cases)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fixture_dir = out_path.parent / (out_path.stem + "-quota-fixtures")
    oracle_path = Path(__file__).resolve()

    case_files = sorted(p for p in cases_dir.glob("*.json") if p.is_file()) if cases_dir.is_dir() else []
    case_records = [
        {"name": path.name, "path": str(path), "sha256": sha(path.read_bytes())} for path in case_files
    ]
    case_digests = {record["name"]: record["sha256"] for record in case_records}
    observation = {
        "schema": ORACLE_SCHEMA,
        "oracle": {"path": str(oracle_path), "sha256": sha(oracle_path.read_bytes())},
        "argv": list(sys.argv),
        "tool": {"path": str(tool), "exists": tool.is_file(), "sha256": sha(tool.read_bytes()) if tool.is_file() else None},
        "cases_dir": str(cases_dir),
        "cases": case_records,
        "cases_sha256_combined": sha(
            b"".join(("%s %s\n" % (record["name"], record["sha256"])).encode("utf-8") for record in case_records)
        ),
        "fixture_dir": str(fixture_dir),
        "results": [],
        "runs": [],
        "real_control": None,
    }
    tool_present = tool.is_file()

    for case_file in case_files:
        row = {
            "case": case_file.name,
            "case_sha256": case_digests[case_file.name],
            "status": "unmet",
            "reason": None,
            "headline": None,
            "supplementary": [],
            "run": None,
            "fixture_path": None,
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
        if "fixture" not in case_obj:
            row["reason"] = "case_missing_fixture"
            observation["results"].append(row)
            continue
        fixture = case_obj["fixture"]
        payload = fixture if isinstance(fixture, str) else json.dumps(fixture, indent=2, sort_keys=True) + "\n"
        fixture_path = fixture_dir / (case_file.stem + ".fixture.json")
        fixture_path.parent.mkdir(parents=True, exist_ok=True)
        fixture_path.write_text(payload, encoding="utf-8")
        row["fixture_path"] = str(fixture_path)
        row["fixture_sha256"] = sha(payload.encode("utf-8"))
        cmd = [sys.executable, str(tool), "--fixture", str(fixture_path)]
        run = run_tool(cmd)
        observation["runs"].append(run)
        row["run"] = run
        if run["timeout"]:
            row["reason"] = "tool_timeout"
            observation["results"].append(row)
            continue
        try:
            parsed = json.loads(run["stdout"])
        except ValueError:
            row["reason"] = "stdout_not_json"
            observation["results"].append(row)
            continue
        if not isinstance(parsed, dict):
            row["reason"] = "stdout_not_json_object"
            observation["results"].append(row)
            continue
        ok, headline, supplementary, reason = evaluate_case(case_obj, parsed, run["exit"], run["stdout"])
        row["headline"] = headline
        row["supplementary"] = supplementary
        row["status"] = "pass" if ok else "unmet"
        row["reason"] = reason
        observation["results"].append(row)

    if args.real_expected:
        real_path = Path(args.real_expected)
        entry = {
            "status": "unmet",
            "reason": None,
            "file": str(real_path),
            "sha256": sha(real_path.read_bytes()) if real_path.is_file() else None,
            "headline": None,
            "supplementary": [],
            "run": None,
        }
        if not real_path.is_file():
            entry["reason"] = "real_expected_absent"
        elif not tool_present:
            entry["status"] = "capability_absent"
            entry["reason"] = "tool_absent"
        else:
            try:
                expected_obj = json.loads(real_path.read_bytes())
            except ValueError:
                expected_obj = None
            if not isinstance(expected_obj, dict):
                entry["reason"] = "real_expected_not_json_object"
            else:
                cmd = [sys.executable, str(tool)]
                run = run_tool(cmd)
                observation["runs"].append(run)
                entry["run"] = run
                if run["timeout"]:
                    entry["reason"] = "tool_timeout"
                else:
                    try:
                        parsed = json.loads(run["stdout"])
                    except ValueError:
                        parsed = None
                    if not isinstance(parsed, dict):
                        entry["reason"] = "stdout_not_json_object"
                    else:
                        ok, headline, supplementary, reason = evaluate_real(
                            expected_obj, parsed, run["exit"], run["stdout"]
                        )
                        entry["headline"] = headline
                        entry["supplementary"] = supplementary
                        entry["status"] = "pass" if ok else "unmet"
                        entry["reason"] = reason
        observation["real_control"] = entry

    headline_rows = list(observation["results"])
    supplementary_checks = [check for row in headline_rows for check in row["supplementary"]]
    if observation["real_control"] is not None:
        headline_rows.append({"status": observation["real_control"]["status"]})
        supplementary_checks.extend(observation["real_control"]["supplementary"])
    counts = {
        "total": len(headline_rows),
        "pass": sum(1 for row in headline_rows if row["status"] == "pass"),
        "capability_absent": sum(1 for row in headline_rows if row["status"] == "capability_absent"),
        "unmet": sum(1 for row in headline_rows if row["status"] == "unmet"),
    }
    observation["counts"] = counts
    observation["supplementary_counts"] = count_checks(supplementary_checks)
    observation["supplementary_checks"] = supplementary_checks

    out_path.write_text(json.dumps(observation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if counts["unmet"]:
        finding = "R23_C2_QUOTA_CASES_UNMET"
    elif observation["supplementary_counts"]["unmet"]:
        finding = "R23_C2_QUOTA_SUPPLEMENTARY_UNMET"
    elif counts["pass"] == 0 and counts["capability_absent"]:
        finding = "R23_C2_QUOTA_CAPABILITY_ABSENT"
    else:
        finding = "R23_C2_QUOTA_CASES_MATCH"
    summary = {
        "schema": ORACLE_SCHEMA,
        "finding_id": finding,
        "counts": counts,
        "supplementary_counts": observation["supplementary_counts"],
        "output": str(out_path),
        "tool_present": tool_present,
    }
    print(json.dumps(summary, sort_keys=True))
    return 0 if counts["unmet"] == 0 and observation["supplementary_counts"]["unmet"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
