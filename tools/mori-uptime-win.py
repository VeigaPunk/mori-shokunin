#!/usr/bin/env python3
"""mori-uptime-win — one-shot read-only probe of the Windows host-uptime
surface: the system tick count (fleet and host observability; detection and
report only).

Round 70 (C2, operability + capability acquisition, sourced). The lane's Linux
census reads since-boot context (uptime-class facts) for liveness and
evidence-window grading; that instrument class is absent on the Windows
workspace host (PROVINCE Round-62 host note — no /proc, no systemd, no
journalctl). This probe reads the one surface that IS present here for the
same detection-and-report class: GetTickCount64 (corpus/SOURCES.md S582 —
"Retrieves the number of milliseconds that have elapsed since the system was
started", `:829`; returns the millisecond count, `:831-833`). Pinned copy:
corpus/evidence/sources-r70/S582.html.

What the probe is FOR: the boot window of the host's own evidence. The r63
event-log counts and the r64 runway reads accumulate since the host's last
boot; the uptime count states how long that window has been open. It is
evidence CONTEXT, never a verdict.

What the probe is NOT, with the doc's own boundaries carried:
- NOT a liveness verdict: a hung host still accrues uptime; the probe prints
  a context count and no alive/dead state word.
- NOT boot identity: the API returns no boot identifier and none is printed
  (`boot_identity=absent` travels on every receipt); attributing anything to
  a boot is tsukuroi/operator ground (PROVINCE refuses boot-state
  diagnosis).
- NOT working-state time: S582:842 points to QueryUnbiasedInterruptTime for
  time spent in the working state, so this count INCLUDES time the system
  spent asleep or hibernating (`count=biased` travels on every receipt).
- NOT a debug-build-safe measurement: S582:845 — on debug ("checked") builds
  the interrupt-time and tick counts are advanced by approximately 49 days,
  so a shifted count is possible there; the probe prints the raw count and
  this caveat travels with it (the receipt reader grades the host class).
- Resolution: S582:836 — the count is limited to the system-timer resolution
  (typically 10-16 ms); the millisecond digits carry that resolution and the
  probe rounds nothing.

Detection and report only. The probe never writes, reconfigures or
remediates anything: it calls one read-only API and prints counts and state
words. No process identities, no user names, no computer names, no paths, no
timestamps — counts and shapes only (the lane's redaction rule; the selftest
asserts this against a fixture that carries such values).

Modes
  python tools/mori-uptime-win.py
  python tools/mori-uptime-win.py --fixture PATH   (JSON-injected value)
  python tools/mori-uptime-win.py --selftest

Output
  surface uptime: state=ok uptime_ms=N uptime_s=N uptime_d=N
          count=biased boot_identity=absent
  UPTIME_WIN: AVAILABLE surfaces=1 ok=1 unavailable=0
or
  surface uptime: state=unavailable reason=<why>
  UPTIME_WIN: UNAVAILABLE surfaces=1 ok=0 unavailable=1
A failed read is `unavailable`, never zero (the lane's honest-unavailable
rule); zero IS a real count (a successful read inside the first tick of a
boot). Exit: 0 available · 2 unavailable or unreadable/malformed fixture ·
argparse's own exit (2) for unknown arguments — usage errors are never a
live reading.

Fixture JSON: {"uptime_ms": <non-negative int>} or null (grades the surface
unavailable). Exact-key gate: extra keys (names, paths, token-shaped values)
are rejected before rendering — never printed (the redaction arm proves the
output stays counts only). The count must fit the API's unsigned 64-bit
domain; the selftest pins the exact rendering of the domain maximum, so a
truncating restype bug cannot pass (the live reader sets restype
c_ulonglong explicitly).

Self-test: offline only — its own fixture files in one temp dir, removed on
exit; binary-mode writes (r62 lesson); no child processes, no network, no
live API call. Arms: output grammar; pinned unit arithmetic
(ms -> s -> d); zero-is-real; honest unavailable; negative rejected;
non-integer rejected; redaction against a fixture carrying
name/path/token-shaped values; unsigned-64-max rendering pinned (truncation
killer).

v1 (round 70): initial shape. No baseline, no frozen predecessor. One-shot
read only: the count is volatile by nature, so the probe claims no series
and no trend — consecutive runs are separate counts, never a rate.
"""

import argparse
import ctypes
import json
import os
import sys
import tempfile


class UptimeUnavailable(Exception):
    """A surface read that genuinely could not be taken (never zero)."""


# ------------------------------------------------------------------ live reader

def read_uptime_live():
    """GetTickCount64 (S582). Raises UptimeUnavailable on any failure."""
    if os.name != "nt":
        raise UptimeUnavailable("no_windows_kernel32")
    try:
        k32 = ctypes.windll.kernel32
    except AttributeError as exc:
        raise UptimeUnavailable("no_windows_kernel32:%s" % type(exc).__name__)
    try:
        k32.GetTickCount64.restype = ctypes.c_ulonglong  # 64-bit count, else c_int truncates
        ms = k32.GetTickCount64()
    except OSError as exc:
        raise UptimeUnavailable("kernel32_call_failed:%s" % type(exc).__name__)
    if ms is None:
        raise UptimeUnavailable("gettickcount64_returned_none")
    return int(ms)


# -------------------------------------------------------------------- reporting

def render(triple):
    """The surface line plus the summary line. `triple` is a
    (state, values|None, reason|None) triple; value keys are fixed."""
    lines = []
    if triple[0] == "ok":
        v = triple[1]
        lines.append(
            "surface uptime: state=ok uptime_ms=%d uptime_s=%d uptime_d=%d"
            " count=biased boot_identity=absent"
            % (v["uptime_ms"], v["uptime_ms"] // 1000, v["uptime_ms"] // 1000 // 86400))
        state = "AVAILABLE"
    else:
        lines.append("surface uptime: state=unavailable reason=%s" % triple[2])
        state = "UNAVAILABLE"
    lines.append("UPTIME_WIN: %s surfaces=1 ok=%d unavailable=%d"
                 % (state, 1 if state == "AVAILABLE" else 0,
                    1 if state != "AVAILABLE" else 0))
    return "\n".join(lines), state


def validate(v):
    """Fixture-shape gate: exact keys, non-negative int, fits unsigned 64 bit."""
    keys = {"uptime_ms"}
    if set(v) != keys:
        raise ValueError("uptime fixture keys %s" % sorted(v))
    ms = v["uptime_ms"]
    if not isinstance(ms, int) or isinstance(ms, bool) or ms < 0:
        raise ValueError("uptime_ms must be a non-negative int")
    if ms >= (1 << 64):
        raise ValueError("uptime_ms exceeds the API's unsigned 64-bit domain")


def run(fixture_path=None):
    """One probe pass. Returns (output_text, exit_code)."""
    fixture = None
    if fixture_path is not None:
        try:
            with open(fixture_path, "rb") as fh:
                fixture = json.loads(fh.read().decode("utf-8"))
        except (OSError, ValueError) as exc:
            return "UPTIME_WIN_SETUP unreadable fixture: %s" % type(exc).__name__, 2
        if fixture is not None:
            try:
                validate(fixture)
            except ValueError as exc:
                return "UPTIME_WIN_SETUP malformed fixture: %s" % exc, 2

    if fixture_path is not None:
        triple = ("unavailable", None, "fixture_null") if fixture is None \
            else ("ok", fixture, None)
    else:
        try:
            triple = ("ok", {"uptime_ms": read_uptime_live()}, None)
        except UptimeUnavailable as exc:
            triple = ("unavailable", None, str(exc))

    text, state = render(triple)
    return text, {"AVAILABLE": 0, "UNAVAILABLE": 2}[state]


# --------------------------------------------------------------------- selftest

def _write_fixture(directory, name, payload):
    path = os.path.join(directory, name)
    with open(path, "wb") as fh:  # binary mode: no CRLF translation (r62 lesson)
        fh.write(json.dumps(payload).encode("utf-8"))
    return path


def _selftest():
    checks = []
    root = tempfile.mkdtemp(prefix="mori-uptime-win-selftest-")
    try:
        # 1. grammar + 2. pinned unit arithmetic (ms -> s -> d, integer floor)
        p = _write_fixture(root, "good.json", {"uptime_ms": 977_184_000})
        out, rc = run(p)
        lines = out.splitlines()
        checks.append(("grammar", rc == 0 and len(lines) == 2
                       and lines[0] == "surface uptime: state=ok uptime_ms=977184000"
                       " uptime_s=977184 uptime_d=11 count=biased boot_identity=absent"
                       and lines[1] == "UPTIME_WIN: AVAILABLE surfaces=1 ok=1 unavailable=0",
                       out))
        checks.append(("unit_math",
                       "uptime_s=977184" in out and "uptime_d=11" in out, out))

        # 3. zero-is-real: a successful read inside the first tick prints 0, rc 0
        z = _write_fixture(root, "zero.json", {"uptime_ms": 0})
        out0, rc0 = run(z)
        checks.append(("zero_is_real",
                       rc0 == 0 and "uptime_ms=0" in out0
                       and "UPTIME_WIN: AVAILABLE" in out0, out0))

        # 4. honest unavailable: null fixture -> UNAVAILABLE, rc 2, no counts
        pn = _write_fixture(root, "none.json", None)
        outn, rcn = run(pn)
        checks.append(("honest_unavailable",
                       rcn == 2 and "state=unavailable reason=fixture_null" in outn
                       and "UPTIME_WIN: UNAVAILABLE surfaces=1 ok=0 unavailable=1" in outn,
                       outn))

        # 5/6. malformed: negative and non-integer rejected, rc 2
        b1 = _write_fixture(root, "neg.json", {"uptime_ms": -5})
        outb1, rcb1 = run(b1)
        b2 = _write_fixture(root, "str.json", {"uptime_ms": "soon"})
        outb2, rcb2 = run(b2)
        checks.append(("negative_rejected",
                       rcb1 == 2 and outb1.startswith("UPTIME_WIN_SETUP malformed fixture"),
                       outb1))
        checks.append(("noninteger_rejected",
                       rcb2 == 2 and outb2.startswith("UPTIME_WIN_SETUP malformed fixture"),
                       outb2))

        # 7. redaction: fixture carries name/path/token-shaped values;
        #    extra keys are rejected BEFORE rendering, none may print
        leaky = _write_fixture(root, "leaky.json", {
            "uptime_ms": 123456, "computer_name": "DESKTOP-SOMEWHERE",
            "user": "alice", "path": "C:\\Users\\somewhere\\secret",
            "token": "0123456789abcdef"})
        outl, rcl = run(leaky)
        checks.append(("redaction",
                       rcl == 2 and outl.startswith("UPTIME_WIN_SETUP malformed fixture")
                       and "somewhere" not in outl and "alice" not in outl
                       and "secret" not in outl and "0123456789abcdef" not in outl,
                       outl))

        # 8. unsigned-64-max rendering pinned (a truncating restype cannot pass)
        big = _write_fixture(root, "big.json",
                             {"uptime_ms": 18_446_744_073_709_551_615})
        outg, rcg = run(big)
        checks.append(("uint64_max_rendered",
                       rcg == 0
                       and "uptime_ms=18446744073709551615" in outg
                       and "uptime_s=18446744073709551" in outg, outg))
    finally:
        import shutil
        shutil.rmtree(root, ignore_errors=True)

    failed = [c for c in checks if not c[1]]
    for name, ok, detail in checks:
        print("selftest %-20s %s" % (name, "PASS" if ok else "FAIL (%s)" % detail[:80]))
    if failed:
        print("UPTIME_WIN_SELFTEST: FAIL (%d/%d)" % (len(checks) - len(failed), len(checks)))
        return 1
    print("UPTIME_WIN_SELFTEST: PASS (%d cases)" % len(checks))
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
