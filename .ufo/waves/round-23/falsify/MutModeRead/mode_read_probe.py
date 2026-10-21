#!/usr/bin/env python3
"""One synthetic real-reader mutation detector; never delegates mocked I/O."""
import argparse
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
from unittest import mock

ROOT = "/fast/scratch/hyaku/mori-r23/MutModeRead/synthetic-sysfs"
UUID = "11111111-2222-4333-8444-555555555555"
DEVICE = "dm-synthetic"
DIRECTORY = ROOT + "/" + UUID
QGROUPS = DIRECTORY + "/qgroups"
CASES = (
    ("enabled_then_disabled_before_mode", "1\n", True, True),
    ("disabled", "0\n", True, False),
    ("enabled_unreadable", None, True, False),
    ("qgroups_absent", None, False, False),
)


class ForbiddenModeOpen(RuntimeError):
    pass


class UnexpectedIO(RuntimeError):
    pass


def run_case(module, name, enabled_text, present, disable_after_read):
    events = []
    mode_opens = []
    enabled_opens = []
    current_enabled = enabled_text == "1\n"

    class EnabledHandle(io.StringIO):
        def __exit__(self, *args):
            nonlocal current_enabled
            result = super().__exit__(*args)
            if disable_after_read:
                current_enabled = False
                events.append({"operation": "synthetic_disable_after_enabled_read"})
            return result

    def listdir(path):
        events.append({"operation": "listdir", "path": str(path)})
        if path == ROOT:
            return [UUID]
        if path == DIRECTORY + "/devices":
            return [DEVICE]
        raise UnexpectedIO("unexpected_listdir")

    def isdir(path):
        events.append({"operation": "isdir", "path": str(path)})
        if path != DIRECTORY:
            raise UnexpectedIO("unexpected_isdir")
        return True

    def stat(path, *args, **kwargs):
        events.append({"operation": "stat", "path": str(path)})
        if path != QGROUPS:
            raise UnexpectedIO("unexpected_stat")
        if not present:
            raise FileNotFoundError("synthetic_absence")
        return object()

    def open_file(path, *args, **kwargs):
        path = str(path)
        events.append({"operation": "open", "path": path})
        if path == QGROUPS + "/mode":
            mode_opens.append({"path": path, "synthetic_enabled_now": current_enabled})
            raise ForbiddenModeOpen("synthetic_mode_open_intercepted")
        if path != QGROUPS + "/enabled":
            raise UnexpectedIO("unexpected_open")
        enabled_opens.append(path)
        if enabled_text is None:
            raise PermissionError("synthetic_enabled_unreadable")
        return EnabledHandle(enabled_text)

    observed = None
    failure = None
    with mock.patch.object(module, "BTRFS_SYSFS", ROOT), \
         mock.patch.object(module.os, "listdir", side_effect=listdir), \
         mock.patch.object(module.os.path, "isdir", side_effect=isdir), \
         mock.patch.object(module.os, "stat", side_effect=stat), \
         mock.patch("builtins.open", side_effect=open_file):
        try:
            observed = module.scan_btrfs_sysfs()
        except (ForbiddenModeOpen, UnexpectedIO) as exc:
            failure = type(exc).__name__
        except Exception as exc:
            failure = "unexpected_" + type(exc).__name__

    expected = {UUID: {
        "devices": [DEVICE],
        "qgroups": present,
        "enabled": None if enabled_text is None else enabled_text == "1\n",
        "mode": None,
    }}
    expected_opens = [QGROUPS + "/enabled"] if present else []
    passed = not mode_opens and failure is None and observed == expected and enabled_opens == expected_opens
    return {
        "case": name,
        "pass": passed,
        "expected": expected,
        "observed": observed,
        "failure": failure,
        "enabled_open_attempts": enabled_opens,
        "mode_open_attempts": mode_opens,
        "events": events,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool", required=True)
    parser.add_argument("--phase", required=True, choices=("before", "mutant", "after"))
    parser.add_argument("--result", required=True)
    args = parser.parse_args()
    source_path = Path(args.tool)
    source_bytes = source_path.read_bytes()
    spec = importlib.util.spec_from_file_location("synthetic_quota_subject", source_path)
    module = importlib.util.module_from_spec(spec)
    # Execute exactly the hashed scratch bytes, without any stale bytecode cache.
    exec(compile(source_bytes, str(source_path), "exec"), module.__dict__)
    results = [run_case(module, *case) for case in CASES]
    exit_code = int(not all(row["pass"] for row in results))
    receipt = {
        "schema": "mori-r23-mut-mode-read-probe-v1",
        "phase": args.phase,
        "argv": [sys.executable, *sys.argv],
        "tool": str(source_path),
        "tool_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "detector_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python_version": sys.version.split()[0],
        "production_root_not_accessed": "/sys/fs/btrfs",
        "synthetic_root": ROOT,
        "io_policy": "BTRFS_SYSFS rebound to scratch; listdir/isdir/stat/open fully mocked with no delegation",
        "cases_passed": sum(row["pass"] for row in results),
        "cases_total": len(results),
        "mode_open_attempts": sum(len(row["mode_open_attempts"]) for row in results),
        "exit_code": exit_code,
        "results": results,
    }
    text = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    Path(args.result).write_text(text, encoding="utf-8")
    print(text, end="")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
