#!/usr/bin/env python3
"""Collect read-only wave-settlement totals for every top-level fleet lane."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile

SCHEMA = "mori-r20-c2-fleet-live-v1"
SETTLEMENT_SCHEMA = "mori-wave-settlement-v1"
COUNT_FIELDS = (
    "waves", "members", "present", "missing", "empty", "misrooted",
    "unsafe", "unparsed", "unreadable_json",
)
FILENAME_MARKERS = re.compile(
    r"preview|undispatched|validation|not-dispatched",
    re.IGNORECASE,
)


def discover_lanes(fleet_root: Path) -> list[Path]:
    with os.scandir(fleet_root) as entries:
        lanes = [
            Path(entry.path)
            for entry in entries
            if entry.name.endswith("-shokunin") and entry.is_dir(follow_symlinks=False)
        ]
    return sorted(lanes, key=lambda lane: lane.name)


def empty_counts() -> dict[str, int | None]:
    return {field: None for field in COUNT_FIELDS}


def parse_counts(path: Path) -> tuple[dict[str, int | None], str | None, list[str]]:
    counts = empty_counts()
    try:
        with path.open("r", encoding="utf-8") as stream:
            payload = json.load(stream)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return counts, "scan output missing or invalid JSON", []
    if not isinstance(payload, dict) or payload.get("schema") != SETTLEMENT_SCHEMA:
        return counts, "scan output has an unexpected schema", []

    totals = payload.get("totals")
    if not isinstance(totals, dict):
        return counts, "scan output has no totals object", []
    waves = payload.get("waves")
    counts["waves"] = len(waves) if isinstance(waves, list) else None
    filename_flags = []
    if isinstance(waves, list):
        for wave in waves:
            if not isinstance(wave, dict) or not isinstance(wave.get("dispatch_path"), str):
                continue
            raw_path = wave["dispatch_path"]
            if "\\" in raw_path:
                continue
            dispatch_path = PurePosixPath(raw_path)
            if FILENAME_MARKERS.search(dispatch_path.name):
                unsafe_path = dispatch_path.is_absolute() or ".." in dispatch_path.parts
                display_path = dispatch_path.name if unsafe_path else dispatch_path.as_posix()
                filename_flags.append(display_path)
    for field in COUNT_FIELDS[1:-1]:
        value = totals.get(field)
        counts[field] = (
            value if isinstance(value, int) and not isinstance(value, bool) and value >= 0
            else None
        )
    unreadable = payload.get("unreadable_json", totals.get("unreadable_json"))
    counts["unreadable_json"] = (
        unreadable
        if isinstance(unreadable, int) and not isinstance(unreadable, bool) and unreadable >= 0
        else None
    )
    if any(value is None for value in counts.values()):
        return counts, "scan output is missing one or more nonnegative totals", filename_flags
    return counts, None, filename_flags


def tool_command(tool: Path) -> list[str]:
    if tool.suffix.lower() == ".py":
        return [sys.executable, str(tool)]
    return [str(tool)]


def scan_lane(
    tool: Path, lane: Path, fleet_root: Path
) -> tuple[dict[str, object], list[dict[str, str]]]:
    record: dict[str, object] = {"lane": lane.name, **empty_counts(), "exit": None}
    filename_flags = []
    try:
        with tempfile.TemporaryDirectory(prefix="mori-c2-fleet-live-") as temporary:
            output = Path(temporary) / "settlement.json"
            argv = tool_command(tool) + [
                "scan", "--lane-root", str(lane), "--fleet-root", str(fleet_root),
                "--out", str(output),
            ]
            process = subprocess.run(
                argv,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
            record["exit"] = process.returncode
            counts, error, paths = parse_counts(output)
            record.update(counts)
            filename_flags = [
                {"lane": lane.name, "path": dispatch_path} for dispatch_path in paths
            ]
            if error:
                record["error"] = error
    except OSError:
        record["error"] = "scan tool could not be started"
    return record, filename_flags


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--tool", required=True, metavar="PATH",
        help="wave-settlement tool executable or Python file",
    )
    parser.add_argument("--fleet-root", required=True, metavar="DIR")
    parser.add_argument(
        "--out", metavar="FILE", help="write the aggregate JSON here (default: stdout)"
    )
    args = parser.parse_args(argv)

    fleet_root = Path(args.fleet_root).expanduser().resolve()
    tool = Path(args.tool).expanduser().resolve()
    if not fleet_root.is_dir():
        parser.error("--fleet-root must be a readable directory")
    if not tool.is_file():
        parser.error("--tool must name an existing file")
    try:
        lanes = discover_lanes(fleet_root)
    except OSError:
        parser.error("--fleet-root could not be listed")

    lane_results = []
    filename_flags = []
    for lane in lanes:
        record, flags = scan_lane(tool, lane, fleet_root)
        lane_results.append(record)
        filename_flags.extend(flags)
    result = {
        "schema": SCHEMA,
        "fleet_root": str(fleet_root),
        "lanes": lane_results,
        "dispatch_filename_flags": sorted(
            filename_flags, key=lambda flag: (flag["lane"], flag["path"])
        ),
    }
    encoded = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.out:
        try:
            Path(args.out).expanduser().write_text(encoded, encoding="utf-8")
        except OSError:
            print("c2-fleet-live: could not write --out file", file=sys.stderr)
            return 2
    else:
        sys.stdout.write(encoded)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


