#!/usr/bin/env python3
"""mori-runway-win — one-shot read-only probe of the Windows resource-runway
surface: memory commitment/physical load and volume free space (fleet and host
observability; resource runway per the province's Core row, detection and
report only).

Round 64 (C2, depth + capability acquisition, sourced). The lane's Linux
runway instruments (df -P on $ROOT and /tmp, memory PSI/fill/avail from
/proc) are absent on the Windows workspace host (PROVINCE Round-62 host
note); this probe is the same detection-and-report class against the surfaces
that ARE present here, read through the Windows API with the standard library
only: GlobalMemoryStatusEx (corpus/SOURCES.md S574 — dwMemoryLoad percent plus
physical and paging-file/commit totals and availability in one struct) and
GetDiskFreeSpaceExW (S575 — total, total-free and free-to-caller bytes for a
volume, queried through any directory on it). Pinned copies:
corpus/evidence/sources-r64/.

Detection and report only. The probe never writes, reconfigures or remediates
anything: it reads two API structures and prints counts, percentages and state
words. No process identities, no user names, no paths beyond a drive letter,
no timestamps — counts and shapes only (the lane's redaction rule; the
selftest asserts this against fixtures that carry such values).

Surfaces
  memory  GlobalMemoryStatusEx -> load_pct, phys_total, phys_avail,
          commit_limit (ullTotalPageFile), commit_avail (ullAvailPageFile)
  disk    GetDiskFreeSpaceExW on the workspace drive -> total_bytes,
          free_bytes, free_to_caller; free_pct is computed from the
          free-to-caller figure (S575:854 — free-to-caller can sit below free
          bytes under quotas; the conservative figure is the one the lane can
          actually use, and both counts are printed)

Modes
  python tools/mori-runway-win.py
  python tools/mori-runway-win.py --fixture PATH   (JSON-injected values)
  python tools/mori-runway-win.py --selftest

Output: one `surface …` line per surface, then
  `RUNWAY_WIN: AVAILABLE|PARTIAL|UNAVAILABLE surfaces=N ok=N unavailable=N`
Zero is a real count (a successful read that returns 0); a failed read is
`unavailable`, never zero (the lane's honest-unavailable rule). Exit:
0 at least one surface ok · 1 usage/argument · 2 no surface ok.

Fixture JSON: {"memory": {...}|null, "disk": {...}|null, "note": any} — each
key replaces that surface's live read; null grades the surface unavailable.
Fixture readers must satisfy the same shape the live readers return; extra
keys (paths, names) are never printed (the redaction arm proves it).

Self-test: runs its own fixtures in one temp file with bytes written in
binary mode — arms: output grammar, percentage arithmetic (integer floor
division pinned), zero-is-real, quota boundary (pct from free-to-caller),
honest unavailable (rc 2), partial availability (rc 0), redaction against a
fixture that carries user/path values, rc contract, load_pct bound (>100
rejected as malformed). No child processes, no network, no live API in the
selftest.

v1 (round 64): initial shape. No baseline, no frozen predecessor. One-shot
reads only: S574:846-847 states the values are volatile, so the probe claims
no series and no trend — consecutive runs are separate counts, never a rate.
"""

import argparse
import ctypes
import json
import os
import sys
import tempfile

INT64_MAX = (1 << 63) - 1


class RunwayUnavailable(Exception):
    """A surface read that genuinely could not be taken (never zero)."""


# ----------------------------------------------------------------- live readers

def read_memory_live():
    """GlobalMemoryStatusEx (S574). Raises RunwayUnavailable on any failure."""
    if os.name != "nt":
        raise RunwayUnavailable("no_windows_kernel32")
    class MEMORYSTATUSEX(ctypes.Structure):
        _fields_ = [
            ("dwLength", ctypes.c_ulong),
            ("dwMemoryLoad", ctypes.c_ulong),
            ("ullTotalPhys", ctypes.c_ulonglong),
            ("ullAvailPhys", ctypes.c_ulonglong),
            ("ullTotalPageFile", ctypes.c_ulonglong),
            ("ullAvailPageFile", ctypes.c_ulonglong),
            ("ullTotalVirtual", ctypes.c_ulonglong),
            ("ullAvailVirtual", ctypes.c_ulonglong),
            ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
        ]
    statex = MEMORYSTATUSEX()
    statex.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
    try:
        ok = ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(statex))
    except OSError as exc:
        raise RunwayUnavailable("kernel32_call_failed:%s" % type(exc).__name__)
    if not ok:
        raise RunwayUnavailable("globalmemorystatusex_returned_zero")
    if statex.dwMemoryLoad > 100:
        raise RunwayUnavailable("load_pct_out_of_range")
    return {
        "load_pct": int(statex.dwMemoryLoad),
        "phys_total": int(statex.ullTotalPhys),
        "phys_avail": int(statex.ullAvailPhys),
        "commit_limit": int(statex.ullTotalPageFile),
        "commit_avail": int(statex.ullAvailPageFile),
    }


def workspace_drive():
    """The drive letter of the lane checkout (a root like `C:`), or None."""
    cwd = os.getcwd()
    drive = os.path.splitdrive(cwd)[0]
    return drive if drive else None


def read_disk_live(drive):
    """GetDiskFreeSpaceExW (S575) on `drive` (a root like `C:`)."""
    if os.name != "nt":
        raise RunwayUnavailable("no_windows_kernel32")
    if not drive:
        raise RunwayUnavailable("no_drive")
    root = ctypes.create_unicode_buffer(drive + "\\")
    caller = ctypes.c_ulonglong()
    total = ctypes.c_ulonglong()
    free = ctypes.c_ulonglong()
    try:
        ok = ctypes.windll.kernel32.GetDiskFreeSpaceExW(
            root, ctypes.byref(caller), ctypes.byref(total), ctypes.byref(free))
    except OSError as exc:
        raise RunwayUnavailable("kernel32_call_failed:%s" % type(exc).__name__)
    if not ok:
        raise RunwayUnavailable("getdiskfreespaceexw_returned_zero")
    return {
        "total_bytes": int(total.value),
        "free_bytes": int(free.value),
        "free_to_caller": int(caller.value),
    }


# ------------------------------------------------------------------- reporting

def pct(part, whole):
    """Integer floor percentage; 0 when whole is 0 (a whole of 0 is a real
    degenerate reading, not an unavailable one)."""
    if whole <= 0:
        return 0
    return (part * 100) // whole


def render(memory, disk):
    """Both surface lines plus the summary line. memory/disk are
    (state, values|None, reason|None) triples; values keys are fixed."""
    lines = []
    ok_count = 0
    if memory[0] == "ok":
        v = memory[1]
        lines.append(
            "surface memory: state=ok load_pct=%d phys_total=%d phys_avail=%d"
            " commit_limit=%d commit_avail=%d commit_avail_pct=%d"
            % (v["load_pct"], v["phys_total"], v["phys_avail"],
               v["commit_limit"], v["commit_avail"],
               pct(v["commit_avail"], v["commit_limit"])))
        ok_count += 1
    else:
        lines.append("surface memory: state=unavailable reason=%s" % memory[2])
    if disk[0] == "ok":
        v = disk[1]
        lines.append(
            "surface disk: state=ok drive=%s total_bytes=%d free_bytes=%d"
            " free_to_caller=%d free_pct=%d"
            % (v["drive"], v["total_bytes"], v["free_bytes"],
               v["free_to_caller"], pct(v["free_to_caller"], v["total_bytes"])))
        ok_count += 1
    else:
        lines.append("surface disk: state=unavailable reason=%s" % disk[2])
    surfaces = 2
    if ok_count == surfaces:
        state = "AVAILABLE"
    elif ok_count:
        state = "PARTIAL"
    else:
        state = "UNAVAILABLE"
    lines.append("RUNWAY_WIN: %s surfaces=%d ok=%d unavailable=%d"
                 % (state, surfaces, ok_count, surfaces - ok_count))
    return "\n".join(lines), state


def validate_memory(v):
    """Fixture-shape gate: exact keys, non-negative ints, load_pct <= 100."""
    keys = {"load_pct", "phys_total", "phys_avail", "commit_limit", "commit_avail"}
    if set(v) != keys:
        raise ValueError("memory fixture keys %s" % sorted(v))
    for k in keys:
        if not isinstance(v[k], int) or isinstance(v[k], bool) or v[k] < 0:
            raise ValueError("memory fixture %s" % k)
    if v["load_pct"] > 100:
        raise ValueError("load_pct > 100")


def validate_disk(v):
    keys = {"drive", "total_bytes", "free_bytes", "free_to_caller"}
    if set(v) != keys:
        raise ValueError("disk fixture keys %s" % sorted(v))
    for k in ("total_bytes", "free_bytes", "free_to_caller"):
        if not isinstance(v[k], int) or isinstance(v[k], bool) or v[k] < 0:
            raise ValueError("disk fixture %s" % k)
    if not isinstance(v["drive"], str) or len(v["drive"]) != 2 or v["drive"][1] != ":":
        raise ValueError("disk fixture drive must be a bare drive root")


def run(fixture_path=None):
    """One probe pass. Returns (output_text, exit_code)."""
    memory = disk = None
    if fixture_path is not None:
        try:
            with open(fixture_path, "rb") as fh:
                fx = json.loads(fh.read().decode("utf-8"))
        except (OSError, ValueError) as exc:
            return "RUNWAY_WIN_SETUP unreadable fixture: %s" % type(exc).__name__, 2
        memory = fx.get("memory")
        disk = fx.get("disk")
        try:
            if memory is not None:
                validate_memory(memory)
            if disk is not None:
                validate_disk(disk)
        except ValueError as exc:
            return "RUNWAY_WIN_SETUP malformed fixture: %s" % exc, 2

    def memory_triple():
        if fixture_path is not None:
            return ("unavailable", None, "fixture_null") if memory is None \
                else ("ok", memory, None)
        try:
            return ("ok", read_memory_live(), None)
        except RunwayUnavailable as exc:
            return ("unavailable", None, str(exc))

    def disk_triple():
        if fixture_path is not None:
            return ("unavailable", None, "fixture_null") if disk is None \
                else ("ok", disk, None)
        drive = workspace_drive()
        try:
            return ("ok", dict(read_disk_live(drive), drive=drive), None)
        except RunwayUnavailable as exc:
            return ("unavailable", None, str(exc))

    text, state = render(memory_triple(), disk_triple())
    return text, {"AVAILABLE": 0, "PARTIAL": 0, "UNAVAILABLE": 2}[state]


# -------------------------------------------------------------------- selftest

def _write_fixture(directory, name, payload):
    path = os.path.join(directory, name)
    with open(path, "wb") as fh:  # binary mode: no CRLF translation (r62 lesson)
        fh.write(json.dumps(payload).encode("utf-8"))
    return path


def _selftest():
    checks = []
    root = tempfile.mkdtemp(prefix="mori-runway-win-selftest-")
    try:
        good_mem = {"load_pct": 62, "phys_total": 33_000_000_000,
                    "phys_avail": 12_000_000_000, "commit_limit": 38_000_000_000,
                    "commit_avail": 20_000_000_000}
        good_disk = {"drive": "C:", "total_bytes": 1_000_000_000_000,
                     "free_bytes": 800_000_000_000, "free_to_caller": 750_000_000_000}

        # 1. grammar + 2. percentage arithmetic (integer floor, pinned values)
        p = _write_fixture(root, "good.json", {"memory": good_mem, "disk": good_disk})
        out, rc = run(p)
        lines = out.splitlines()
        checks.append(("grammar", rc == 0 and len(lines) == 3
                       and lines[0].startswith("surface memory: state=ok ")
                       and lines[1].startswith("surface disk: state=ok drive=C: ")
                       and lines[2] == "RUNWAY_WIN: AVAILABLE surfaces=2 ok=2 unavailable=0",
                       out))
        checks.append(("pct_math",
                       "commit_avail_pct=%d" % ((20_000_000_000 * 100) // 38_000_000_000) in out
                       and "free_pct=%d" % ((750_000_000_000 * 100) // 1_000_000_000_000) in out,
                       out))

        # 3. zero-is-real: a successful read that returns 0 prints 0, rc 0
        zero = _write_fixture(root, "zero.json", {
            "memory": dict(good_mem, load_pct=0, phys_avail=0),
            "disk": dict(good_disk, free_bytes=0, free_to_caller=0)})
        out0, rc0 = run(zero)
        checks.append(("zero_is_real",
                       rc0 == 0 and "phys_avail=0" in out0
                       and "free_to_caller=0" in out0
                       and "free_pct=0" in out0
                       and "RUNWAY_WIN: AVAILABLE" in out0, out0))

        # 4. quota boundary: free_to_caller < free_bytes -> both printed,
        #    free_pct computed from the caller figure
        outq, rcq = run(p)
        checks.append(("quota_boundary",
                       rcq == 0 and "free_bytes=800000000000" in outq
                       and "free_to_caller=750000000000" in outq
                       and "free_pct=75" in outq, outq))

        # 5. honest unavailable: both surfaces null -> UNAVAILABLE, rc 2
        pn = _write_fixture(root, "none.json", {"memory": None, "disk": None})
        outn, rcn = run(pn)
        checks.append(("honest_unavailable",
                       rcn == 2 and "state=unavailable reason=fixture_null" in outn
                       and "RUNWAY_WIN: UNAVAILABLE surfaces=2 ok=0 unavailable=2" in outn,
                       outn))

        # 6. partial: memory ok, disk null -> PARTIAL, rc 0
        pp = _write_fixture(root, "partial.json", {"memory": good_mem, "disk": None})
        outp, rcp = run(pp)
        checks.append(("partial",
                       rcp == 0 and "RUNWAY_WIN: PARTIAL surfaces=2 ok=1 unavailable=1" in outp,
                       outp))

        # 7. redaction: fixture carries user/path values; none may print
        leaky = _write_fixture(root, "leaky.json", {
            "memory": good_mem, "disk": dict(good_disk, drive="C:"),
            "note": "C:\\Users\\somewhere\\secret\\token.txt"})
        outl, rcl = run(leaky)
        checks.append(("redaction",
                       rcl == 0 and "somewhere" not in outl and "secret" not in outl
                       and "token" not in outl and "\\" not in outl, outl))

        # 8. rc contract, offline: the same mapping arms 1 and 5 exercise,
        # asserted together (AVAILABLE/PARTIAL -> 0, UNAVAILABLE -> 2)
        _, rca = run(p)
        _, rcb2 = run(pp)
        _, rcc = run(pn)
        checks.append(("rc_contract", (rca, rcb2, rcc) == (0, 0, 2),
                       "available=%s partial=%s unavailable=%s" % (rca, rcb2, rcc)))

        # 9. malformed fixture: load_pct > 100 rejected, rc 2
        bad = _write_fixture(root, "bad.json", {
            "memory": dict(good_mem, load_pct=101), "disk": good_disk})
        outb, rcb = run(bad)
        checks.append(("malformed_fixture",
                       rcb == 2 and outb.startswith("RUNWAY_WIN_SETUP malformed fixture"),
                       outb))
    finally:
        import shutil
        shutil.rmtree(root, ignore_errors=True)

    failed = [c for c in checks if not c[1]]
    for name, ok, detail in checks:
        print("selftest %-20s %s" % (name, "PASS" if ok else "FAIL (%s)" % detail[:80]))
    if failed:
        print("RUNWAY_WIN_SELFTEST: FAIL (%d/%d)" % (len(checks) - len(failed), len(checks)))
        return 1
    print("RUNWAY_WIN_SELFTEST: PASS (%d cases)" % len(checks))
    return 0


def main(argv):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--fixture")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        return _selftest()
    text, rc = run(args.fixture)
    print(text)
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
