#!/usr/bin/env python3
"""Independent black-box oracle for the frozen mori round-20 C2 cases."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

CANARY = b"CANARY-r20-7f3a"
SYMLINK_CANARY = b"SYMLINK-TARGET-CANARY-r20"
DISPATCH_SCHEMA = "ufo-swarm-wave-dispatch-v1"


def _report_path(name):
    return ".ufo/waves/round-1/build/{}.md".format(name)


def _task(name, report=None):
    lines = ["Oracle fixture member {}.".format(name)]
    if report is not None:
        lines.append("Report: write your scoped findings to {}".format(report))
    return {"name": name, "agent": "oracle-{}".format(name), "task": "\n".join(lines)}


def _write_dispatch(lane_root, relative_path, wave, tasks):
    path = lane_root / ".ufo" / "waves" / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    dispatch = {
        "schema": DISPATCH_SCHEMA,
        "wave": wave,
        # L1 repair (round 20): frozen case `no-spawn` says "dispatch with taskCall null";
        # v0 wrote {"tasks": null} instead. Original bytes kept as c2-oracle-v0.py.
        "taskCall": None if tasks is None else {"context": "c", "tasks": tasks},
    }
    path.write_text(json.dumps(dispatch, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _write_report(root, relative_path, content=b"non-empty oracle report\n"):
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return path


def build_fixture(case_id, temp_root):
    """Create exactly one isolated lane fixture for one frozen case."""
    temp_root = Path(temp_root)
    lane_root = temp_root / "sandbox" / "lane"
    lane_root.mkdir(parents=True)
    fleet_root = temp_root / "fleet"
    use_fleet_root = False
    report_a = _report_path("A")

    if case_id == "all-present":
        tasks = []
        for name in ("A", "B", "C"):
            report = _report_path(name)
            tasks.append(_task(name, report))
            _write_report(lane_root, report)
        _write_dispatch(lane_root, "dispatch.json", 1, tasks)
    elif case_id == "one-missing":
        tasks = []
        for name in ("A", "B", "C"):
            report = _report_path(name)
            tasks.append(_task(name, report))
            if name != "C":
                _write_report(lane_root, report)
        _write_dispatch(lane_root, "dispatch.json", 1, tasks)
    elif case_id == "none-present":
        _write_dispatch(
            lane_root,
            "dispatch.json",
            1,
            [_task(name, _report_path(name)) for name in ("A", "B")],
        )
    elif case_id == "empty-report":
        path_a = _report_path("A")
        path_b = _report_path("B")
        _write_report(lane_root, path_a)
        _write_report(lane_root, path_b, b"")
        _write_dispatch(lane_root, "dispatch.json", 1, [_task("A", path_a), _task("B", path_b)])
    elif case_id == "misrooted":
        path_b = _report_path("B")
        _write_report(lane_root, report_a)
        _write_report(fleet_root, path_b)
        use_fleet_root = True
        _write_dispatch(
            lane_root,
            "dispatch.json",
            1,
            [_task("A", report_a), _task("B", path_b)],
        )
    elif case_id == "malformed-dispatch":
        _write_report(lane_root, report_a)
        _write_dispatch(lane_root, "valid/dispatch.json", 1, [_task("A", report_a)])
        malformed = lane_root / ".ufo" / "waves" / "broken.json"
        malformed.parent.mkdir(parents=True, exist_ok=True)
        malformed.write_text('{"schema":"' + DISPATCH_SCHEMA + '", invalid\n', encoding="utf-8")
    elif case_id == "no-trailer":
        path_b = _report_path("B")
        _write_report(lane_root, path_b)
        _write_dispatch(
            lane_root,
            "dispatch.json",
            1,
            [_task("A"), _task("B", path_b)],
        )
    elif case_id == "traversal":
        traversal_path = "../../outside.md"
        _write_report(temp_root, "outside.md")
        _write_dispatch(lane_root, "dispatch.json", 1, [_task("A", traversal_path)])
    elif case_id == "absolute-path":
        absolute_report = temp_root / "absolute-report.md"
        absolute_report.write_bytes(b"absolute path should remain unsafe\n")
        _write_dispatch(
            lane_root,
            "dispatch.json",
            1,
            [_task("A", str(absolute_report))],
        )
    elif case_id == "symlink-report":
        target = temp_root / "symlink-target.md"
        target.write_bytes(SYMLINK_CANARY + b"\n")
        link = lane_root / report_a
        link.parent.mkdir(parents=True, exist_ok=True)
        os.symlink(str(target), str(link))
        _write_dispatch(lane_root, "dispatch.json", 1, [_task("A", report_a)])
    elif case_id == "other-schema-ignored":
        waves_root = lane_root / ".ufo" / "waves"
        waves_root.mkdir(parents=True, exist_ok=True)
        (waves_root / "registry.json").write_text(
            json.dumps({"schema": "ufo-swarm-registry-v1"}) + "\n", encoding="utf-8"
        )
        (waves_root / "plain.json").write_text('{"value":"plain json"}\n', encoding="utf-8")
        _write_report(lane_root, report_a)
        _write_dispatch(lane_root, "settled/dispatch.json", 1, [_task("A", report_a)])
    elif case_id == "no-spawn":
        _write_dispatch(lane_root, "dispatch.json", 1, None)
    elif case_id == "content-not-emitted":
        _write_report(lane_root, report_a, CANARY + b"\n")
        _write_dispatch(lane_root, "dispatch.json", 1, [_task("A", report_a)])
    elif case_id == "deterministic":
        # Create in reverse byte order so the result must sort dispatch paths itself.
        for relative, wave, name in (
            ("z/dispatch.json", 2, "Z"),
            ("a/dispatch.json", 1, "A"),
        ):
            report = _report_path(name)
            _write_report(lane_root, report)
            _write_dispatch(lane_root, relative, wave, [_task(name, report)])
    else:
        raise ValueError("unsupported frozen case id: {}".format(case_id))

    return lane_root, fleet_root, use_fleet_root


def _run_scan(tool, lane_root, fleet_root, use_fleet_root, out_path):
    command = ["python3", tool, "scan", "--lane-root", str(lane_root)]
    if use_fleet_root:
        command.extend(["--fleet-root", str(fleet_root)])
    command.extend(["--out", str(out_path)])
    try:
        completed = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=60,
        )
        stdout = completed.stdout
        stderr = completed.stderr
        returncode = completed.returncode
        process_error = None
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or b""
        stderr = exc.stderr or b""
        returncode = None
        process_error = "timeout"
    except OSError as exc:
        stdout = b""
        stderr = b""
        returncode = None
        process_error = "{}: {}".format(type(exc).__name__, exc)

    out_exists = out_path.is_file()
    try:
        out_bytes = out_path.read_bytes() if out_exists else b""
    except OSError:
        out_exists = False
        out_bytes = b""

    return {
        "returncode": returncode,
        "stdout": stdout,
        "stderr": stderr,
        "out_exists": out_exists,
        "out_bytes": out_bytes,
        "process_error": process_error,
    }


def _json_payload(run):
    if run["out_exists"]:
        candidates = [run["out_bytes"], run["stdout"]]
    else:
        candidates = [run["stdout"]]
    for payload in candidates:
        if not payload:
            continue
        try:
            value = json.loads(payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        if isinstance(value, dict):
            return value
    return None


def _extract_observed(run, payload, second_run=None):
    stdout = run["stdout"]
    out_bytes = run["out_bytes"]
    combined_output = stdout + b"\n" + out_bytes
    observed = {
        "exit": run["returncode"],
        "out_file_exists": run["out_exists"],
        "stdout_nonempty": bool(stdout),
        "stderr_nonempty": bool(run["stderr"]),
    }

    waves = payload.get("waves") if isinstance(payload, dict) else None
    if isinstance(waves, list):
        observed["waves"] = len(waves)
        first_wave = waves[0] if waves and isinstance(waves[0], dict) else None
        if first_wave is not None:
            observed["state"] = first_wave.get("state")
            counts = first_wave.get("counts")
            counts = counts if isinstance(counts, dict) else {}
            for key in ("present", "missing", "empty", "misrooted", "unsafe", "unparsed"):
                if key in counts:
                    observed[key] = counts[key]
            member_list = first_wave.get("members")
            if isinstance(member_list, list):
                observed["members"] = len(member_list)
            missing_names = first_wave.get("missing")
            if isinstance(missing_names, list):
                observed["missing_names"] = missing_names
            if "status" in (member_list[0] if isinstance(member_list, list) and member_list and isinstance(member_list[0], dict) else {}):
                observed["_member_statuses"] = [
                    member.get("status") for member in member_list if isinstance(member, dict)
                ]
        dispatch_paths = [
            wave.get("dispatch_path")
            for wave in waves
            if isinstance(wave, dict) and isinstance(wave.get("dispatch_path"), str)
        ]
        if len(dispatch_paths) == len(waves):
            observed["waves_sorted_by_path"] = dispatch_paths == sorted(
                dispatch_paths, key=lambda value: value.encode("utf-8")
            )
    if isinstance(payload, dict):
        for key in ("unreadable_json", "ignored_json"):
            if key in payload:
                observed[key] = payload[key]

    if b"CANARY-r20-7f3a" in stdout:
        observed["stdout_contains_canary"] = True
    else:
        observed["stdout_contains_canary"] = False
    observed["out_contains_canary"] = CANARY in out_bytes

    if isinstance(payload, dict) and isinstance(waves, list) and waves:
        first_wave = waves[0] if isinstance(waves[0], dict) else {}
        member_list = first_wave.get("members")
        if isinstance(member_list, list) and member_list:
            statuses = [member.get("status") for member in member_list if isinstance(member, dict)]
            observed["not_followed"] = (
                len(statuses) == len(member_list)
                and all(status != "present" for status in statuses)
                and SYMLINK_CANARY not in combined_output
            )

    if second_run is not None:
        observed["byte_identical"] = (
            run["out_exists"]
            and second_run["out_exists"]
            and run["out_bytes"] == second_run["out_bytes"]
        )

    if isinstance(payload, dict) and isinstance(waves, list):
        # The frozen vocabulary is checked below by compare_case; this records
        # whether each forbidden token was absent from externally emitted bytes.
        observed["_output_text"] = combined_output.decode("utf-8", "replace").casefold()
    return observed


def _apply_special_expectations(expected, observed):
    actual = dict(observed)
    output_text = actual.pop("_output_text", "")
    member_statuses = actual.pop("_member_statuses", None)
    if "no_vocab" in expected:
        actual["no_vocab"] = [
            word for word in expected["no_vocab"] if word.casefold() not in output_text
        ]
    if "not_followed" in expected and "not_followed" not in actual:
        actual["not_followed"] = bool(member_statuses) and all(
            status != "present" for status in member_statuses
        )
    return actual


def _compare_case(case, observed):
    expected = case.get("expect", {})
    actual = _apply_special_expectations(expected, observed)
    issues = []
    for key, expected_value in expected.items():
        if key not in actual:
            issues.append({
                "key": key,
                "expected": expected_value,
                "observed": None,
                "reason": "not_observed",
            })
        elif actual[key] != expected_value:
            issues.append({
                "key": key,
                "expected": expected_value,
                "observed": actual[key],
                "reason": "mismatch",
            })
    return actual, issues


def run_case(case, tool, tool_exists):
    case_id = case.get("id", "<missing-id>")
    try:
        with tempfile.TemporaryDirectory(prefix="mori-r20-c2-{}-".format(case_id)) as temp_dir:
            lane_root, fleet_root, use_fleet_root = build_fixture(case_id, temp_dir)
            if not tool_exists:
                return {
                    "id": case_id,
                    "status": "capability_absent",
                    "expected": case.get("expect", {}),
                    "observed": {"tool_exists": False},
                    "issues": [{"reason": "tool_absent", "tool": tool}],
                }

            out_path = Path(temp_dir) / "scan-output.json"
            first_run = _run_scan(tool, lane_root, fleet_root, use_fleet_root, out_path)
            payload = _json_payload(first_run)
            second_run = None
            if case_id == "deterministic":
                second_out = Path(temp_dir) / "scan-output-second.json"
                second_run = _run_scan(tool, lane_root, fleet_root, use_fleet_root, second_out)
            observed = _extract_observed(first_run, payload, second_run)
            actual, issues = _compare_case(case, observed)
            if first_run["process_error"]:
                issues.append({"reason": "process_error", "detail": first_run["process_error"]})
            if not first_run["out_exists"]:
                issues.append({"reason": "out_file_missing"})
            if payload is None:
                issues.append({"reason": "output_json_unavailable"})
            if second_run is not None:
                if second_run["process_error"]:
                    issues.append({"reason": "second_process_error", "detail": second_run["process_error"]})
                if not second_run["out_exists"]:
                    issues.append({"reason": "second_out_file_missing"})
            return {
                "id": case_id,
                "status": "matched" if not issues else "mismatched",
                "expected": case.get("expect", {}),
                "observed": actual,
                "issues": issues,
            }
    except Exception as exc:
        return {
            "id": case_id,
            "status": "mismatched",
            "expected": case.get("expect", {}),
            "observed": {"fixture_error": "{}: {}".format(type(exc).__name__, exc)},
            "issues": [{"reason": "fixture_error"}],
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", required=True, help="path to the wave-settlement tool")
    parser.add_argument("--out", required=True, help="output JSON file")
    args = parser.parse_args()

    expected_path = Path(__file__).resolve().parents[2] / "frozen" / "c2-expected.json"
    expected_doc = json.loads(expected_path.read_text(encoding="utf-8"))
    cases = expected_doc.get("cases")
    if not isinstance(cases, list):
        raise ValueError("frozen expected file has no cases array")

    tool_path = os.path.abspath(os.path.expanduser(args.tool))
    tool_exists = Path(tool_path).exists()
    results = [run_case(case, tool_path, tool_exists) for case in cases]
    counts = {
        "matched": sum(result["status"] == "matched" for result in results),
        "mismatched": sum(result["status"] == "mismatched" for result in results),
        "capability_absent": sum(result["status"] == "capability_absent" for result in results),
    }
    output = {
        "schema": "mori-r20-c2-oracle-v1",
        "tool": tool_path,
        "counts": counts,
        "results": results,
    }
    out_path = Path(os.path.abspath(os.path.expanduser(args.out)))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if counts["mismatched"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
