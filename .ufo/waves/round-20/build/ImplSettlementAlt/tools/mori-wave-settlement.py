#!/usr/bin/env python3
"""Read-only per-seat settlement scan for UFO wave dispatch records."""

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath

DISPATCH_SCHEMA = "ufo-swarm-wave-dispatch-v1"
OUTPUT_SCHEMA = "mori-wave-settlement-v1"
STATUS_NAMES = ("present", "empty", "missing", "misrooted", "unsafe", "unparsed")
STATE_NAMES = ("settled", "partial", "unsettled", "no-spawn", "unavailable")
REPORT_LINE = re.compile(r"Report: write your scoped findings to (\S+)")


def _byte_key(value):
    return value.encode("utf-8", "surrogatepass")


def _walk_json_files(waves_root):
    """Yield regular JSON files, never entering or yielding symlinks."""
    pending = [waves_root]
    found = []
    while pending:
        directory = pending.pop()
        with os.scandir(directory) as entries:
            children = sorted(entries, key=lambda entry: os.fsencode(entry.name))
            for entry in children:
                if entry.is_symlink():
                    continue
                if entry.is_dir(follow_symlinks=False):
                    pending.append(Path(entry.path))
                elif entry.name.endswith(".json") and entry.is_file(follow_symlinks=False):
                    found.append(Path(entry.path))
    return sorted(found, key=lambda path: os.fsencode(path.relative_to(waves_root.parent.parent).as_posix()))


def _safe_parts(raw_path):
    """Return normalized relative path components, or None when unsafe."""
    if not isinstance(raw_path, str) or not raw_path or "\x00" in raw_path:
        return None
    posix_path = PurePosixPath(raw_path)
    windows_path = PureWindowsPath(raw_path)
    if posix_path.is_absolute() or windows_path.is_absolute() or windows_path.drive:
        return None
    if any(part == ".." for part in posix_path.parts):
        return None
    if any(part == ".." for part in windows_path.parts):
        return None
    return posix_path.parts


def _regular_report_state(root, parts):
    """Return present/empty for a regular file, otherwise missing; never follow links."""
    current = root
    if not parts:
        return "missing"
    for index, part in enumerate(parts):
        current = current / part
        try:
            info = current.lstat()
        except (OSError, ValueError):
            return "missing"
        if stat.S_ISLNK(info.st_mode):
            return "missing"
        if index < len(parts) - 1:
            if not stat.S_ISDIR(info.st_mode):
                return "missing"
        elif stat.S_ISREG(info.st_mode):
            return "present" if info.st_size > 0 else "empty"
        else:
            return "missing"
    return "missing"


def _report_status(task, lane_root, fleet_root):
    task_text = task.get("task") if isinstance(task, dict) else None
    if not isinstance(task_text, str):
        return "unparsed", False
    lines = task_text.splitlines()
    match = REPORT_LINE.fullmatch(lines[-1]) if lines else None
    if match is None:
        return "unparsed", False

    parts = _safe_parts(match.group(1))
    if parts is None:
        return "unsafe", False

    lane_status = _regular_report_state(lane_root, parts)
    if lane_status in ("present", "empty"):
        return lane_status, True
    if fleet_root is not None:
        fleet_status = _regular_report_state(fleet_root, parts)
        if fleet_status in ("present", "empty"):
            return "misrooted", True
    return "missing", True


def _member(task, lane_root, fleet_root):
    status, has_safe_path = _report_status(task, lane_root, fleet_root)
    if isinstance(task, dict):
        name = task.get("name")
        agent = task.get("agent")
    else:
        name = None
        agent = None
    if not isinstance(name, str):
        name = ""
    if not isinstance(agent, str):
        agent = None
    return {"name": name, "agent": agent, "status": status}, has_safe_path


def _wave_state(task_call, members, safe_paths):
    if task_call is None:
        return "no-spawn"
    if not safe_paths:
        return "unavailable"
    present = sum(member["status"] == "present" for member in members)
    if members and present == len(members):
        return "settled"
    if present:
        return "partial"
    return "unsettled"


def _dispatch_record(path, lane_root, fleet_root, raw):
    document = json.loads(raw)
    if not isinstance(document, dict) or document.get("schema") != DISPATCH_SCHEMA:
        return None

    task_call = document.get("taskCall")
    members = []
    safe_paths = 0
    if isinstance(task_call, dict) and isinstance(task_call.get("tasks"), list):
        for task in task_call["tasks"]:
            member, has_safe_path = _member(task, lane_root, fleet_root)
            members.append(member)
            safe_paths += has_safe_path

    counts = {status: 0 for status in STATUS_NAMES}
    for member in members:
        counts[member["status"]] += 1
    state = _wave_state(task_call, members, safe_paths)
    missing_names = sorted(
        (member["name"] for member in members if member["status"] != "present"),
        key=_byte_key,
    )
    relative_path = path.relative_to(lane_root).as_posix()
    return {
        "dispatch_path": relative_path,
        "dispatch_sha256": hashlib.sha256(raw).hexdigest(),
        "wave": document.get("wave"),
        "members": members,
        "counts": counts,
        "state": state,
        "missing": missing_names,
    }


def _scan(lane_root_arg, fleet_root_arg):
    try:
        lane_root = Path(lane_root_arg).resolve(strict=True)
        if not lane_root.is_dir():
            raise OSError("lane root is not a directory")
    except (OSError, RuntimeError) as error:
        raise ValueError("lane root is unavailable") from error

    fleet_root = None
    if fleet_root_arg is not None:
        try:
            fleet_root = Path(fleet_root_arg).resolve(strict=True)
            if not fleet_root.is_dir():
                raise OSError("fleet root is not a directory")
        except (OSError, RuntimeError) as error:
            raise ValueError("fleet root is unavailable") from error

    ufo_dir = lane_root / ".ufo"
    waves_root = ufo_dir / "waves"
    try:
        ufo_info = ufo_dir.lstat()
    except FileNotFoundError:
        ufo_info = None
    except OSError as error:
        raise ValueError("lane wave directory is unreadable") from error
    if ufo_info is None or stat.S_ISLNK(ufo_info.st_mode) or not stat.S_ISDIR(ufo_info.st_mode):
        return {
            "schema": OUTPUT_SCHEMA,
            "lane_root": str(lane_root),
            "waves": [],
            "totals": _empty_totals(),
            "ignored_json": 0,
            "unreadable_json": 0,
        }

    try:
        waves_info = waves_root.lstat()
    except FileNotFoundError:
        waves_info = None
    except OSError as error:
        raise ValueError("lane wave directory is unreadable") from error
    if waves_info is None or stat.S_ISLNK(waves_info.st_mode) or not stat.S_ISDIR(waves_info.st_mode):
        return {
            "schema": OUTPUT_SCHEMA,
            "lane_root": str(lane_root),
            "waves": [],
            "totals": _empty_totals(),
            "ignored_json": 0,
            "unreadable_json": 0,
        }

    try:
        files = _walk_json_files(waves_root)
    except OSError as error:
        raise ValueError("lane wave directory is unreadable") from error

    waves = []
    ignored_json = 0
    unreadable_json = 0
    for path in files:
        try:
            info = path.lstat()
            if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
                continue
            raw = path.read_bytes()
            record = _dispatch_record(path, lane_root, fleet_root, raw)
        except (OSError, ValueError, UnicodeError, json.JSONDecodeError):
            unreadable_json += 1
            continue
        if record is None:
            ignored_json += 1
        else:
            waves.append(record)

    waves.sort(key=lambda record: os.fsencode(record["dispatch_path"]))
    totals = _empty_totals()
    totals["waves"] = len(waves)
    for wave in waves:
        totals["states"][wave["state"]] += 1
        totals["members"] += len(wave["members"])
        for status in STATUS_NAMES:
            totals["counts"][status] += wave["counts"][status]

    return {
        "schema": OUTPUT_SCHEMA,
        "lane_root": str(lane_root),
        "waves": waves,
        "totals": totals,
        "ignored_json": ignored_json,
        "unreadable_json": unreadable_json,
    }


def _empty_totals():
    return {
        "waves": 0,
        "members": 0,
        "counts": {status: 0 for status in STATUS_NAMES},
        "states": {state: 0 for state in STATE_NAMES},
    }


def _exit_code(result):
    return 0 if all(wave["state"] in ("settled", "no-spawn") for wave in result["waves"]) else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description="Scan UFO wave reports without reading report contents.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    scan_parser = subparsers.add_parser("scan", help="scan dispatch records under a lane root")
    scan_parser.add_argument("--lane-root", required=True, metavar="DIR")
    scan_parser.add_argument("--fleet-root", metavar="DIR")
    scan_parser.add_argument("--out", metavar="FILE")
    args = parser.parse_args(argv)

    try:
        result = _scan(args.lane_root, args.fleet_root)
        encoded = json.dumps(result, ensure_ascii=True, sort_keys=True, indent=2) + "\n"
        if args.out:
            with open(args.out, "w", encoding="utf-8", newline="\n") as destination:
                destination.write(encoded)
        else:
            sys.stdout.write(encoded)
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2
    except OSError as error:
        print("unable to write scan output", file=sys.stderr)
        return 2
    return _exit_code(result)


if __name__ == "__main__":
    sys.exit(main())
