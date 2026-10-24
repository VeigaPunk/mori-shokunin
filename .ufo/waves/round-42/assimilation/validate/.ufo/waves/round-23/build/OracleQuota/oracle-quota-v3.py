#!/usr/bin/env python3
"""Round-23 C2 oracle v3 (strict, W1 case contract) — sealed quota-surface cases.

Third sibling of the C2 oracle.  v1 (oracle-quota.py) is tolerant, v2
(oracle-quota-v2.py) invented its own case envelope; both stay immutable.  v3
implements the explicit wave-1 case contract that every independent case author
already used, and never asks an author to change a file.

Case schema (exact, enforced):
  case file  : exactly {schema, id, scenario, fixture, expected, rationale, sources}
               plus the optional key supplementary_expected
  schema     : exactly "mori-quota-case-v1"
  expected   : exactly {exit, finding_id, paths}          (the key is `exit`)
  path entry : exactly {path, fstype, mount_point, quota_state, enforcement, basis}
  fixture    : passed through untouched; the oracle never judges fixture shape
               (deliberately malformed fixtures are cases in their own right)

supplementary_expected (optional, separate top-level wrapper):
  {"note": <prose>, "paths": [{"path": ..., "device_check": ..., "quota_option_keys": ...,
                               "btrfs_qgroups_mode": ...}]}
  `note` is prose: never compared, never echoed.  `path` is the verified identity of the
  expected row the metadata describes - it must match an entry of expected.paths and the
  matched rows must keep the order of expected.paths.  Only the fields actually given are
  compared; the metadata never enters the scored six-field primary expectation.  A bare
  list of the same row objects is accepted as well.

Headline (scored, six-field denominator, unchanged): exit code + finding_id +
ordered (path, fstype, mount_point, quota_state, enforcement, basis) tuples.
Supplementary checks are counted and listed separately and never fold into the
headline denominator.

Tool output: exactly {schema, finding_id, exit_code, paths, df_covers_quota, limits}.
A setup error (finding_id "QUOTA_SETUP") may add the optional top-level `error` token -
a nonempty ASCII [a-z_]+ string of at most 64 characters, carrying no input text - and
must keep paths == [] and df_covers_quota == false.  Omitting `error` is equally valid.

CLI: --tool PATH --cases DIR --output FILE [--real-expected FILE]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ORACLE_SCHEMA = "mori-r23-c2-oracle-v3"
TOOL_SCHEMA = "mori-quota-surface-v1"
CASE_SCHEMA = "mori-quota-case-v1"

CASE_KEYS = {"schema", "id", "scenario", "fixture", "expected", "rationale", "sources"}
OPTIONAL_CASE_KEYS = {"supplementary_expected"}
EXPECTED_KEYS = {"exit", "finding_id", "paths"}
PATH_KEYS = ("path", "fstype", "mount_point", "quota_state", "enforcement", "basis")
SUPP_PATH_KEYS = ("device_check", "quota_option_keys", "btrfs_qgroups_mode")
SUPP_ITEM_KEYS = set(SUPP_PATH_KEYS) | {"path"}
OUTPUT_KEYS = {"schema", "finding_id", "exit_code", "paths", "df_covers_quota", "limits"}
# A setup error may carry an optional top-level token: nonempty ASCII [a-z_]+, <= 64 chars.
ERROR_TOKEN_RE = re.compile(r"[a-z_]{1,64}")
OUTPUT_PATH_KEYS = set(PATH_KEYS) | set(SUPP_PATH_KEYS)
DEVICE_CHECK_VALUES = {"match", "mismatch", "not_checked", "btrfs_subvolume_skipped"}
QGROUP_MODES = {"qgroup", "squota"}
TIMEOUT_S = 30
OCTAL = {"040": " ", "011": "\t", "012": "\n", "134": "\\"}
# Ordinary option values that legitimately occur in any output; never canaries.
COMMON_VALUES = {
    "rw", "ro", "relatime", "defaults", "nofail", "auto", "noatime", "strictatime",
    "dirsync", "async", "sync", "errors=remount-ro", "0", "1",
}


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


def is_distinctive(value: str) -> bool:
    """A distinctive, non-common string: long enough, not plain alphanumerics."""
    if len(value) < 5 or value in COMMON_VALUES:
        return False
    return any(not char.isalnum() for char in value)


def canaries(fixture):
    """Leakage canaries drawn only from the fixture handed to the tool.

    Full mount sources, btrfs UUIDs, full `key=value` option tokens, distinctive
    option values and distinctive device basenames.  Ordinary values (option
    keys, numbers, rw/ro, mount points, the case paths) are never canaries.
    """
    found = []
    if not isinstance(fixture, dict):
        return found
    sysfs = fixture.get("btrfs_sysfs")
    if isinstance(sysfs, dict):
        for uuid in sysfs:
            if uuid:
                found.append(("uuid", uuid))
    sources = []
    mountinfo = fixture.get("mountinfo")
    for line in (mountinfo or "").splitlines():
        fields = line.strip().split()
        if len(fields) < 3:
            continue
        source = fields[-2]
        sources.append(source)
        for candidate in {source, decode_octal(source)}:
            if candidate.startswith("/"):
                found.append(("mount_source", candidate))
        for token in fields[-1].split(","):
            if "=" not in token:
                continue
            found.append(("option_token", token))
            value = token.split("=", 1)[1]
            if is_distinctive(value):
                found.append(("option_value", value))
    links = fixture.get("device_links")
    if isinstance(links, dict):
        for basename in links.values():
            if isinstance(basename, str) and len(basename) >= 3 and any(not c.isalnum() for c in basename):
                if not any(basename in source for source in sources):
                    found.append(("device_basename", basename))
    if isinstance(sysfs, dict):
        for record in sysfs.values():
            for device in (record or {}).get("devices", []) if isinstance(record, dict) else []:
                if isinstance(device, str) and len(device) >= 3 and any(not c.isalnum() for c in device):
                    if not any(device in source for source in sources):
                        found.append(("device_basename", device))
    return found


def leakage_hits(stdout_text, fixture):
    text = stdout_text or ""
    hits = []
    for kind, value in canaries(fixture):
        if value in text:
            hits.append(kind + ":" + value)
    return hits


def read_supplementary(case_obj, expected_paths):
    """Read the optional supplementary metadata.

    Canonical wrapper (as written by the wave-1 author):

        {"note": <prose>,
         "paths": [{"path": ..., "device_check": ..., "quota_option_keys": ...,
                    "btrfs_qgroups_mode": ...}]}

    `note` is prose: it is never compared and never echoed.  `path` is the verified
    identity of the expected row it describes - it must match an entry of
    expected.paths, and the matched rows must keep the order of expected.paths.  Only
    the fields actually given are compared; the metadata never enters the scored
    six-field primary expectation.

    Returns (per_index, error, note_present).
    """
    raw = case_obj.get("supplementary_expected")
    note_present = isinstance(raw, dict) and "note" in raw
    if raw is None:
        return {}, None, note_present
    if isinstance(raw, dict):
        unknown = set(raw) - {"note", "paths"}
        if unknown:
            return None, "supplementary_expected_keys:%s" % sorted(unknown), note_present
        if "paths" not in raw:
            return {}, None, note_present
        items = raw["paths"]
        if not isinstance(items, list):
            return None, "supplementary_expected_paths_not_list", note_present
    elif isinstance(raw, list):
        items = raw
    else:
        return None, "supplementary_expected_shape", note_present
    order = {}
    for index, entry in enumerate(expected_paths):
        order.setdefault(entry.get("path"), []).append(index)
    per_index = {}
    last = -1
    for item in items:
        if not isinstance(item, dict):
            return None, "supplementary_expected_item_not_object", note_present
        if not set(item) <= SUPP_ITEM_KEYS:
            return None, "supplementary_expected_keys:%s" % sorted(item), note_present
        if "path" not in item:
            return None, "supplementary_expected_row_without_path", note_present
        matches = order.get(item["path"], [])
        if not matches:
            return None, "supplementary_expected_path_unknown:%s" % item["path"], note_present
        if len(matches) > 1:
            return None, "supplementary_expected_path_ambiguous:%s" % item["path"], note_present
        index = matches[0]
        if index <= last:
            return None, "supplementary_expected_out_of_order:%s" % item["path"], note_present
        last = index
        metadata = {key: item[key] for key in SUPP_PATH_KEYS if key in item}
        if metadata:
            per_index[index] = metadata
    return per_index, None, note_present


def supplementary_checks(parsed, exit_code, observed_paths, per_index, fixture, stdout_text):
    """Supplementary sealed checks; each entry is {check, status, detail}."""
    checks = []

    def add(name, ok, detail):
        checks.append({"check": name, "status": "pass" if ok else "unmet", "detail": detail})

    add("schema", parsed.get("schema") == TOOL_SCHEMA, parsed.get("schema"))
    add("exit_consistency", parsed.get("exit_code") == exit_code, parsed.get("exit_code"))
    finding = parsed.get("finding_id")
    # The six documented output keys; a setup error may add the optional top-level
    # `error` token, and only there.
    allowed_keys = OUTPUT_KEYS | {"error"}
    add("output_keys_allowed", set(parsed) <= allowed_keys, sorted(parsed))
    if finding == "QUOTA_SETUP":
        add("output_key_set", set(parsed) <= allowed_keys, sorted(parsed))
    else:
        add("output_key_set", set(parsed) == OUTPUT_KEYS, sorted(parsed))
    if "error" in parsed:
        token = parsed.get("error")
        add(
            "error_token",
            finding == "QUOTA_SETUP"
            and isinstance(token, str)
            and ERROR_TOKEN_RE.fullmatch(token) is not None,
            token,
        )
    else:
        # Omitting the token on a setup error is valid as well.
        add("error_token", True, None)
    add(
        "path_key_set",
        all(set(entry) == OUTPUT_PATH_KEYS for entry in observed_paths),
        [sorted(entry) for entry in observed_paths],
    )
    add("df_covers_quota", parsed.get("df_covers_quota") is False, parsed.get("df_covers_quota"))
    if finding == "QUOTA_SETUP":
        # No partial verdict on a setup error: no path rows, no capacity claim.
        add(
            "setup_no_partial_verdict",
            parsed.get("paths") == [] and parsed.get("df_covers_quota") is False,
            {"paths": parsed.get("paths"), "df_covers_quota": parsed.get("df_covers_quota")},
        )
    limits = parsed.get("limits")
    add("limits_text", isinstance(limits, str) and limits.strip() != "", type(limits).__name__)

    for index in sorted(per_index):
        want = per_index[index]
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
        # Only the strings that must never be echoed are canaries; ordinary values
        # (option keys, 0/1, rw) are not scanned.
        hits = leakage_hits(stdout_text, fixture)
        add("no_leakage", not hits, hits)
    return checks


def evaluate_case(case_obj, parsed, exit_code, stdout_text):
    """Strict headline evaluation of one case; returns (ok, headline, supplementary, reason)."""
    headline = {"exit_match": False, "finding_match": False, "paths_match": False}
    keys = set(case_obj)
    if not keys <= CASE_KEYS | OPTIONAL_CASE_KEYS:
        return False, headline, [], "case_key_set:%s" % sorted(keys - CASE_KEYS - OPTIONAL_CASE_KEYS)
    if not CASE_KEYS <= keys:
        return False, headline, [], "case_missing_keys:%s" % sorted(CASE_KEYS - keys)
    if case_obj["schema"] != CASE_SCHEMA:
        return False, headline, [], "case_schema_value:%s" % (case_obj["schema"],)
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
        if set(entry) != set(PATH_KEYS):
            return False, headline, [], "expected_path_key_set:%s" % sorted(entry)
    per_index, supp_error, note_present = read_supplementary(case_obj, expected_paths)
    if supp_error:
        return False, headline, [], supp_error
    observed_paths = parsed.get("paths")
    if not isinstance(observed_paths, list) or not all(isinstance(entry, dict) for entry in observed_paths):
        return False, headline, [], "observed_paths_not_object_list"

    headline["exit_match"] = exit_code == expected["exit"]
    headline["finding_match"] = parsed.get("finding_id") == expected["finding_id"]
    headline["paths_match"] = [
        tuple(entry.get(field) for field in PATH_KEYS) for entry in observed_paths
    ] == [tuple(entry.get(field) for field in PATH_KEYS) for entry in expected_paths]
    supplementary = supplementary_checks(
        parsed, exit_code, observed_paths, per_index, case_obj["fixture"], stdout_text
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
    per_index = {
        index: {key: entry[key] for key in SUPP_PATH_KEYS if key in entry}
        for index, entry in enumerate(want_paths)
    }
    supplementary = supplementary_checks(parsed, exit_code, observed_paths, per_index, None, stdout_text)
    ok = headline["exit_match"] and headline["finding_match"] and headline["paths_match"]
    return ok, headline, supplementary, None


def count_checks(checks):
    return {
        "total": len(checks),
        "pass": sum(1 for check in checks if check["status"] == "pass"),
        "unmet": sum(1 for check in checks if check["status"] == "unmet"),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(prog="oracle-quota-v3.py", description="Round-23 C2 strict oracle (W1 case contract).")
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
        raw_supp = case_obj.get("supplementary_expected")
        # The note is prose: record only that it exists, never its text.
        row["supplementary_note_present"] = bool(isinstance(raw_supp, dict) and "note" in raw_supp)
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
    supplementary_checks_flat = [check for row in headline_rows for check in row["supplementary"]]
    if observation["real_control"] is not None:
        headline_rows.append({"status": observation["real_control"]["status"]})
        supplementary_checks_flat.extend(observation["real_control"]["supplementary"])
    counts = {
        "total": len(headline_rows),
        "pass": sum(1 for row in headline_rows if row["status"] == "pass"),
        "capability_absent": sum(1 for row in headline_rows if row["status"] == "capability_absent"),
        "unmet": sum(1 for row in headline_rows if row["status"] == "unmet"),
    }
    observation["counts"] = counts
    observation["supplementary_counts"] = count_checks(supplementary_checks_flat)
    observation["supplementary_checks"] = supplementary_checks_flat

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
