#!/usr/bin/env python3
"""Two-sample disk write-rate arm for frontier FR6 (mori round 34, claim C1).

Purpose
  This tool is the frontier FR6 "two-sample census arm" as a lane operation:
  it reads two samples of ``/proc/diskstats`` and the block class tree under
  ``<sysfs>/class/block``, and reports, per device, the class, the state and
  the write rate in bytes per second, plus the host total over the whole
  disks.

  Detection and report only.  The tool reads ``/proc/diskstats`` and the
  sysfs block class tree and writes nothing: it creates no file, writes to no
  block device, changes no setting and starts no service.

CLI
  python3 tools/mori-disk-rate.py --a FILE --b FILE [--sysfs DIR] --interval-ms N
  python3 tools/mori-disk-rate.py [--sysfs DIR] --interval-ms N
  python3 tools/mori-disk-rate.py --selftest

  --a FILE, --b FILE   two saved ``/proc/diskstats`` samples (offline mode);
                       both or neither must be given
  --sysfs DIR          sysfs root, default ``/sys``; the class of a device is
                       read from DIR/class/block/<name>
  --interval-ms N      the sampling interval in milliseconds; it is the
                       denominator of every reported rate
  --selftest           run the bounded self-test against synthetic samples and
                       a synthetic sysfs tree under TMPDIR (it reads no live
                       /proc or /sys entry), print
                       ``MORI_DISK_RATE_SELFTEST pass=<n> fail=<n>`` and exit
                       0 when every arm passes, 1 when one fails and 2 when
                       the fixtures cannot be built

  stdout is one JSON object with the keys ``interval_ms``, ``devices`` (a
  mapping of device name to ``class``, ``state`` and ``write_Bps``),
  ``host_basis`` and ``host_write_Bps``.  The exit status is 0 whenever that
  JSON is produced and 2 on a usage error.

Rules
  Each rule below is restated in this tool's own words; the label after the
  dash is the source the contract cites for that rule.

  R1 - a line names its device by the third whitespace-separated token, and a
       line with fewer than three tokens names no device and is ignored
       (S187: the line numbers the device name as field 3).
  R2 - a line is valid only when it holds 14, 18 or 20 tokens and every token
       other than the device name is an unsigned decimal; the sectors-written
       counter is token 10 (S187: field counts and field 10; S180).
  R3 - the class comes from ``<sysfs>/class/block/<name>`` in this order: no
       such directory -> ``unknown``; a ``partition`` entry -> ``partition``
       (S191, block/partitions/core.c: the partition-only attribute); a
       non-empty ``slaves`` directory -> ``stacked`` (S192, block/holder.c:
       the slaves/holders links; S182 creates ``slaves`` for every disk, so
       only a non-empty one marks stacking); a ``device`` entry -> ``disk``
       (S193, drivers/base/core.c: the ``device`` link is created only for a
       device whose parent is not a partition); otherwise ``virtual`` (lane
       rule: a parentless, unstacked block device such as loop, zram or ram).
  R4 - the reported device set is the union of the names seen in sample A,
       the names seen in sample B and the entries of ``<sysfs>/class/block``
       (S182: the kernel itself skips a zero-size partition when it prints).
  R5 - the states have this precedence: ``bad-line`` (a malformed line for
       that device in either sample) > ``absent`` (no line for it in either
       sample) > ``gone`` (a line in A only) > ``new`` (a line in B only) >
       ``reset`` (the sectors written fell between A and B) > ``ok``
       (S182 skips zero-size partitions; S181: the counters are set back when
       the device is reinitialised).
  R6 - the rate of an ``ok`` device is ``(B - A) * 512 * 1000 // interval_ms``
       bytes per second, and every other state reports ``write_Bps`` null,
       never zero (S186, S187: the sector unit is 512 bytes; round-33 rows 4
       and 9: an unavailable rate is never a zero rate).
  R7 - ``host_basis`` lists, sorted, the names whose class is ``disk``, and
       ``host_write_Bps`` is the sum of their rates when that basis is
       non-empty and every basis device is ``ok``, and null otherwise
       (S183: a partition's sectors are added to its whole disk, so they are
       counted once; S192: a stacked device maps onto devices already
       counted; the virtual class is excluded by lane rule).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import select
import subprocess
import sys
import tempfile
import threading
import time

DISKSTATS = "/proc/diskstats"
OPEN_TIMEOUT = 30.0
VALID_TOKEN_COUNTS = (14, 18, 20)
NAME_TOKEN_INDEX = 2          # R1: the third whitespace token
SECTORS_WRITTEN_INDEX = 9     # R2: token 10
SECTOR_BYTES = 512            # R6: the sector unit (S186, S187)
UNSIGNED_DECIMAL = re.compile(r"\A[0-9]+\Z")


def parse_sample(text):
    """Return (sectors written per device, names with a malformed line)."""
    sectors = {}
    malformed = set()
    for line in text.splitlines():
        tokens = line.split()
        if len(tokens) < 3:
            continue
        name = tokens[NAME_TOKEN_INDEX]
        if len(tokens) not in VALID_TOKEN_COUNTS:
            malformed.add(name)
            continue
        if any(not UNSIGNED_DECIMAL.match(token)
               for index, token in enumerate(tokens)
               if index != NAME_TOKEN_INDEX):
            malformed.add(name)
            continue
        sectors[name] = int(tokens[SECTORS_WRITTEN_INDEX])
    return sectors, malformed


def _open_for_read(path, timeout):
    """Open a path for reading; None when it cannot be opened in time.

    Opening a FIFO for reading waits for a writer, so the open is done in a
    thread that is given a deadline.
    """
    result = {}

    def worker():
        try:
            result["fd"] = os.open(path, os.O_RDONLY)
        except OSError:
            result["error"] = True

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()
    thread.join(timeout)
    if thread.is_alive() or "fd" not in result:
        return None
    return result["fd"]


def _read_fd(fd, idle, wait_first):
    """Read one sample from an open descriptor.

    The sample ends when the descriptor reaches its end or stays idle for
    ``idle`` seconds; a sample that ends in the middle of a line is held
    open for a while longer, so that a split write is not cut in half.
    """
    chunks = []
    waited = 0.0
    while True:
        timeout = OPEN_TIMEOUT if (wait_first and not chunks) else idle
        try:
            ready, _, _ = select.select([fd], [], [], timeout)
        except (OSError, ValueError):
            break
        if not ready:
            waited += timeout
            text = b"".join(chunks).decode("utf-8", "replace")
            if text.endswith("\n") or waited >= 1.0:
                break
            continue
        try:
            data = os.read(fd, 65536)
        except OSError:
            break
        if not data:
            break
        chunks.append(data)
    return b"".join(chunks).decode("utf-8", "replace")


def read_sample(path, idle):
    """Read one sample from a regular file; None when it cannot be read."""
    fd = _open_for_read(path, OPEN_TIMEOUT)
    if fd is None:
        return None
    try:
        return _read_fd(fd, idle, True)
    finally:
        os.close(fd)


def read_live_samples(idle, interval_ms):
    """Read the two live samples of /proc/diskstats.

    Each sample is a separate open, read and close of the file, and the
    second open starts one full interval after the first sample was closed,
    so the interval the rate divides by is the time between the readings.
    """
    first = read_sample(DISKSTATS, idle)
    time.sleep(interval_ms / 1000.0)
    return first, read_sample(DISKSTATS, idle)


def classify(name, sysfs_root):
    """Class of one device, in the order R3 gives."""
    base = os.path.join(sysfs_root, "class", "block", name)
    if not os.path.isdir(base):
        return "unknown"
    if os.path.lexists(os.path.join(base, "partition")):
        return "partition"
    slaves = os.path.join(base, "slaves")
    if os.path.isdir(slaves) and os.listdir(slaves):
        return "stacked"
    if os.path.lexists(os.path.join(base, "device")):
        return "disk"
    return "virtual"


def sysfs_block_names(sysfs_root):
    """Entries of <sysfs>/class/block (R4)."""
    try:
        return set(os.listdir(os.path.join(sysfs_root, "class", "block")))
    except OSError:
        return set()


def device_state(name, a_sectors, a_malformed, b_sectors, b_malformed):
    """State of one device, by the precedence R5 gives."""
    if name in a_malformed or name in b_malformed:
        return "bad-line"
    in_a = name in a_sectors
    in_b = name in b_sectors
    if not in_a and not in_b:
        return "absent"
    if in_a and not in_b:
        return "gone"
    if in_b and not in_a:
        return "new"
    if b_sectors[name] < a_sectors[name]:
        return "reset"
    return "ok"


def build_report(a_text, b_text, sysfs_root, interval_ms):
    """The JSON object the tool prints."""
    a_sectors, a_malformed = parse_sample(a_text)
    b_sectors, b_malformed = parse_sample(b_text)
    names = (set(a_sectors) | a_malformed | set(b_sectors) | b_malformed
             | sysfs_block_names(sysfs_root))
    devices = {}
    basis = []
    for name in sorted(names):
        device_class = classify(name, sysfs_root)
        state = device_state(name, a_sectors, a_malformed, b_sectors, b_malformed)
        if state == "ok":
            rate = ((b_sectors[name] - a_sectors[name]) * SECTOR_BYTES * 1000
                    // interval_ms)
        else:
            rate = None
        devices[name] = {"class": device_class, "state": state, "write_Bps": rate}
        if device_class == "disk":
            basis.append(name)
    host = None
    if basis and all(devices[name]["state"] == "ok" for name in basis):
        host = sum(devices[name]["write_Bps"] for name in basis)
    return {
        "interval_ms": interval_ms,
        "devices": devices,
        "host_basis": sorted(basis),
        "host_write_Bps": host,
    }


# ---- selftest -------------------------------------------------------------

SELFTEST_PREFIX = "MORI_DISK_RATE_SELFTEST"
SELFTEST_SAMPLE_A = (
    "   8       0 sda 100 0 200 5 10 0 1000 0 0 0 0\n"
    "   8       1 sda1 50 0 100 5 5 0 500 0 0 0 0\n"
)
SELFTEST_SAMPLE_B = (
    "   8       0 sda 120 0 240 6 12 0 3000 0 0 0 0\n"
    "   8       1 sda1 60 0 120 6 6 0 1500 0 0 0 0\n"
)


def _selftest_sysfs(root):
    """Build the synthetic sysfs tree the class arms read (R3, R4)."""
    block = os.path.join(root, "class", "block")
    os.makedirs(block)
    attributes = {"sda": "device", "sda1": "partition"}
    trees = {"dm-0": "slaves/sda", "loop0": "slaves"}
    for name, entry in attributes.items():
        base = os.path.join(block, name)
        os.makedirs(base)
        with open(os.path.join(base, entry), "w", encoding="utf-8"):
            pass
    for name, entry in trees.items():
        base = os.path.join(block, name)
        os.makedirs(base)
        os.makedirs(os.path.join(base, entry))
    return root


def selftest():
    """Run the bounded self-test; 0 when every arm passes, 1 a failed arm, 2 setup."""
    tmpdir = os.environ.get("TMPDIR")
    if not tmpdir:
        print("SELFTEST SETUP TMPDIR is not set")
        print("%s pass=0 fail=0" % SELFTEST_PREFIX)
        return 2
    try:
        temporary = tempfile.TemporaryDirectory(
            prefix=".mori-disk-rate-selftest-", dir=tmpdir)
    except OSError as exc:
        print("SELFTEST SETUP %s" % exc)
        print("%s pass=0 fail=0" % SELFTEST_PREFIX)
        return 2

    passed = 0
    failed = 0

    def arm(name, function):
        nonlocal passed, failed
        try:
            function()
        except Exception as exc:          # noqa: BLE001 - the selftest reports
            failed += 1
            print("SELFTEST FAIL %s: %s: %s" % (name, type(exc).__name__, exc))
        else:
            passed += 1

    with temporary as scratch:
        sysfs = _selftest_sysfs(os.path.join(scratch, "sysfs"))
        a_path = os.path.join(scratch, "a.diskstats")
        b_path = os.path.join(scratch, "b.diskstats")
        with open(a_path, "w", encoding="utf-8") as handle:
            handle.write(SELFTEST_SAMPLE_A)
        with open(b_path, "w", encoding="utf-8") as handle:
            handle.write(SELFTEST_SAMPLE_B)

        def report(a_text, b_text, interval_ms=1000):
            return build_report(a_text, b_text, sysfs, interval_ms)

        def cli(*arguments):
            return subprocess.run(
                [sys.executable, os.path.abspath(__file__)] + list(arguments),
                capture_output=True, text=True, timeout=60)

        def parse_valid():
            sectors, malformed = parse_sample(SELFTEST_SAMPLE_A)
            assert sectors == {"sda": 1000, "sda1": 500}, sectors
            assert not malformed, malformed

        def parse_ignores_short_line():
            sectors, malformed = parse_sample("  8 0\n")
            assert sectors == {} and not malformed, (sectors, malformed)

        def parse_rejects_token_count():
            line = " ".join(["8", "0", "sda"] + [str(value)
                                                 for value in range(1, 13)])
            sectors, malformed = parse_sample(line + "\n")
            assert sectors == {} and malformed == {"sda"}, (sectors, malformed)

        def parse_rejects_non_decimal():
            line = "   8       0 sda 100 0 200 5 10 0 4x00 0 0 0 0\n"
            sectors, malformed = parse_sample(line)
            assert sectors == {} and malformed == {"sda"}, (sectors, malformed)

        def classify_order():
            expected = {"sda": "disk", "sda1": "partition", "dm-0": "stacked",
                        "loop0": "virtual", "ghost": "unknown"}
            observed = {name: classify(name, sysfs) for name in expected}
            assert observed == expected, observed

        def state_precedence():
            pairs = [
                (device_state("x", {"x": 5}, set(), {"x": 9}, set()), "ok"),
                (device_state("x", {"x": 5}, set(), {"x": 4}, set()), "reset"),
                (device_state("x", {}, set(), {"x": 1}, set()), "new"),
                (device_state("x", {"x": 1}, set(), {}, set()), "gone"),
                (device_state("x", {}, set(), {}, set()), "absent"),
                (device_state("x", {}, {"x"}, {}, set()), "bad-line"),
                (device_state("x", {}, set(), {}, {"x"}), "bad-line"),
            ]
            bad = [pair for pair in pairs if pair[0] != pair[1]]
            assert not bad, bad

        def sysfs_names():
            assert sysfs_block_names(sysfs) == {"sda", "sda1", "dm-0", "loop0"}
            assert sysfs_block_names(os.path.join(scratch, "absent")) == set()

        def report_rates():
            got = report(SELFTEST_SAMPLE_A, SELFTEST_SAMPLE_B)
            assert got["interval_ms"] == 1000, got
            assert got["devices"]["sda"] == {
                "class": "disk", "state": "ok", "write_Bps": 1024000}, got
            assert got["devices"]["sda1"] == {
                "class": "partition", "state": "ok",
                "write_Bps": 512000}, got
            assert got["devices"]["loop0"] == {
                "class": "virtual", "state": "absent", "write_Bps": None}, got
            assert got["host_basis"] == ["sda"], got
            assert got["host_write_Bps"] == 1024000, got

        def report_reset_is_null_not_zero():
            higher = (
                "   8       0 sda 100 0 200 5 10 0 9000 0 0 0 0\n"
                "   8       1 sda1 50 0 100 5 5 0 500 0 0 0 0\n")
            got = report(higher, SELFTEST_SAMPLE_B)
            assert got["devices"]["sda"] == {
                "class": "disk", "state": "reset", "write_Bps": None}, got
            assert got["devices"]["sda1"]["write_Bps"] == 512000, got
            assert got["host_write_Bps"] is None, got

        def report_bad_line_blocks_host():
            broken = SELFTEST_SAMPLE_B.replace(
                "   8       0 sda 120 0 240 6 12 0 3000 0 0 0 0",
                "   8       0 sda 120 0 240 6 12 0 3000 0 0 0")
            got = report(SELFTEST_SAMPLE_A, broken)
            assert got["devices"]["sda"]["state"] == "bad-line", got
            assert got["devices"]["sda"]["write_Bps"] is None, got
            assert got["host_write_Bps"] is None, got

        def cli_production_ok():
            proc = cli("--a", a_path, "--b", b_path, "--sysfs", sysfs,
                       "--interval-ms", "1000")
            assert proc.returncode == 0, (proc.returncode, proc.stderr)
            payload = json.loads(proc.stdout)
            assert payload["host_basis"] == ["sda"], payload
            assert payload["host_write_Bps"] == 1024000, payload

        def cli_unreadable_sample():
            proc = cli("--a", os.path.join(scratch, "missing"), "--b", b_path,
                       "--sysfs", sysfs, "--interval-ms", "1000")
            assert proc.returncode == 1, (proc.returncode, proc.stderr)
            assert "cannot read the sample(s) given" in proc.stderr, proc.stderr

        def cli_half_pair():
            proc = cli("--a", a_path, "--interval-ms", "1000")
            assert proc.returncode == 2, (proc.returncode, proc.stdout)
            assert "--a and --b must be given together" in proc.stderr, proc.stderr

        def cli_zero_interval():
            proc = cli("--a", a_path, "--b", b_path, "--interval-ms", "0")
            assert proc.returncode == 2, (proc.returncode, proc.stdout)
            assert "positive number of milliseconds" in proc.stderr, proc.stderr

        arm("parse_valid", parse_valid)
        arm("parse_ignores_short_line", parse_ignores_short_line)
        arm("parse_rejects_token_count", parse_rejects_token_count)
        arm("parse_rejects_non_decimal", parse_rejects_non_decimal)
        arm("classify_order", classify_order)
        arm("state_precedence", state_precedence)
        arm("sysfs_block_names", sysfs_names)
        arm("report_rates", report_rates)
        arm("report_reset_is_null_not_zero", report_reset_is_null_not_zero)
        arm("report_bad_line_blocks_host", report_bad_line_blocks_host)
        arm("cli_production_ok", cli_production_ok)
        arm("cli_unreadable_sample", cli_unreadable_sample)
        arm("cli_half_pair", cli_half_pair)
        arm("cli_zero_interval", cli_zero_interval)

    print("%s pass=%d fail=%d" % (SELFTEST_PREFIX, passed, failed))
    return 0 if failed == 0 else 1


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--selftest" in argv:
        return selftest()
    parser = argparse.ArgumentParser(
        prog="mori-disk-rate.py",
        description=("Two-sample disk write rate, device classes and host "
                     "total; detection and report only."),
    )
    parser.add_argument("--a", metavar="FILE",
                        help="first saved /proc/diskstats sample")
    parser.add_argument("--b", metavar="FILE",
                        help="second saved /proc/diskstats sample")
    parser.add_argument("--sysfs", metavar="DIR", default="/sys",
                        help="sysfs root (default: /sys)")
    parser.add_argument("--interval-ms", type=int, required=True, metavar="N",
                        help="sampling interval in milliseconds")
    args = parser.parse_args(argv)

    if args.interval_ms <= 0:
        parser.error("--interval-ms must be a positive number of milliseconds")
    if (args.a is None) != (args.b is None):
        parser.error("--a and --b must be given together, or neither")

    # A sample served through a FIFO ends when the FIFO goes idle, so the
    # idle window is kept well below the sampling interval.
    idle = min(0.5, max(0.01, args.interval_ms / 1000.0 / 4.0))

    if args.a is not None:
        a_text = read_sample(args.a, idle)
        b_text = read_sample(args.b, idle)
    else:
        a_text, b_text = read_live_samples(idle, args.interval_ms)

    if a_text is None or b_text is None:
        print("mori-disk-rate.py: cannot read the sample(s) given",
              file=sys.stderr)
        return 1

    report = build_report(a_text, b_text, args.sysfs, args.interval_ms)
    json.dump(report, sys.stdout, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
