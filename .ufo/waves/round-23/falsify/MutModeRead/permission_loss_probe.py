#!/usr/bin/env python3
"""One fully mocked two-UUID device-listing permission-loss witness."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from unittest import mock

TOOL = "/fast/scratch/hyaku/mori-r23/MutModeRead/repo/tools/mori-quota-surface.py"
RESULT = "/fast/scratch/hyaku/mori-r23/MutModeRead/permission-loss.json"
ROOT = "/fast/scratch/hyaku/mori-r23/MutModeRead/permission-loss-sysfs"
HIDDEN = "11111111-2222-4333-8444-555555555555"
VISIBLE = "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee"
PINNED_SOURCE_SHA256 = "e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92"


class UnexpectedIO(RuntimeError):
    pass


def main():
    source = Path(TOOL).read_bytes()
    source_hash = hashlib.sha256(source).hexdigest()
    if source_hash != PINNED_SOURCE_SHA256:
        raise RuntimeError("pinned_source_mismatch_no_probe")
    spec = importlib.util.spec_from_file_location("permission_loss_subject", TOOL)
    subject = importlib.util.module_from_spec(spec)
    exec(compile(source, TOOL, "exec"), subject.__dict__)
    events = []

    def listdir(path):
        path = str(path)
        if path == ROOT:
            events.append({"operation": "listdir", "path": path, "result": [HIDDEN, VISIBLE]})
            return [HIDDEN, VISIBLE]
        if path == ROOT + "/" + HIDDEN + "/devices":
            events.append({"operation": "listdir", "path": path, "exception": "PermissionError"})
            raise PermissionError("synthetic_devices_unreadable")
        if path == ROOT + "/" + VISIBLE + "/devices":
            events.append({"operation": "listdir", "path": path, "result": ["dm-0"]})
            return ["dm-0"]
        raise UnexpectedIO("unexpected_listdir")

    def isdir(path):
        path = str(path)
        if path not in (ROOT + "/" + HIDDEN, ROOT + "/" + VISIBLE):
            raise UnexpectedIO("unexpected_isdir")
        events.append({"operation": "isdir", "path": path, "result": True})
        return True

    def stat(path, *args, **kwargs):
        path = str(path)
        if path not in (ROOT + "/" + HIDDEN + "/qgroups", ROOT + "/" + VISIBLE + "/qgroups"):
            raise UnexpectedIO("unexpected_stat")
        events.append({"operation": "stat", "path": path, "exception": "FileNotFoundError"})
        raise FileNotFoundError("synthetic_qgroups_absent")

    def open_file(path, *args, **kwargs):
        events.append({"operation": "open_rejected", "path": str(path)})
        raise UnexpectedIO("unexpected_open")

    with mock.patch.object(subject, "BTRFS_SYSFS", ROOT), \
         mock.patch.object(subject.os, "listdir", side_effect=listdir), \
         mock.patch.object(subject.os.path, "isdir", side_effect=isdir), \
         mock.patch.object(subject.os, "stat", side_effect=stat), \
         mock.patch("builtins.open", side_effect=open_file):
        scanned = subject.scan_btrfs_sysfs()
        classification, mode = subject.classify_btrfs("dm-0", scanned)
    after_hash = hashlib.sha256(Path(TOOL).read_bytes()).hexdigest()
    passed = classification[0] == "unknown"
    exit_code = int(not passed)
    receipt = {
        "schema": "mori-r23-permission-loss-witness-v1",
        "observed_base": "f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c",
        "argv": [sys.executable, *sys.argv],
        "python_version": sys.version.split()[0],
        "tool": TOOL,
        "source_sha256_before": source_hash,
        "source_sha256_after": after_hash,
        "detector_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "source_modified": False,
        "synthetic_root": ROOT,
        "synthetic_fixture": {
            "device": "dm-0",
            "potential_device_membership": {HIDDEN: ["dm-0"], VISIBLE: ["dm-0"]},
            "unreadable_devices_uuid": HIDDEN,
            "accessible_devices_uuid": VISIBLE,
            "qgroups_absent_for_both": True,
        },
        "io_policy": "BTRFS_SYSFS rebound to own scratch; listdir/isdir/stat/open fully mocked without delegation",
        "events": events,
        "observed_scan_btrfs_sysfs": scanned,
        "observed_classify_btrfs": {"quota_state": classification[0], "enforcement": classification[1], "basis": classification[2], "mode": mode},
        "required": {"quota_state": "unknown", "disabled_permitted": False, "reason": "Unreadable UUID devices membership must not become a complete unique association"},
        "pass": passed,
        "exit_code": exit_code,
        "verdict": "safety_counterexample" if not passed else "required_unknown_observed",
        "actual_sysfs_or_mode_reads": False,
        "runtime_bounds": {"address_space_bytes": 402653184, "wall_seconds": 15, "cpu_seconds": 10, "concurrent_children": 1},
    }
    text = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    Path(RESULT).write_text(text, encoding="utf-8")
    print(text, end="")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
