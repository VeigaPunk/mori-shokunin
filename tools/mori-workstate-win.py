#!/usr/bin/env python3
"""mori-workstate-win — one-shot read-only probe of the Windows working-state
time surface: GetTickCount64 (biased, ms) beside QueryUnbiasedInterruptTime
(unbiased, 100-ns units), counts only (fleet and host observability; detection
and report only).

Round 71 (C2, depth + capability acquisition, sourced). The r70 uptime probe
reads the biased tick count and carries the boundary "count=biased" on every
line; its own doc (corpus/SOURCES.md S582, pinned copy
corpus/evidence/sources-r70/S582.html) points at QueryUnbiasedInterruptTime
for time spent in the working state. This probe opens that pointed surface
(corpus/SOURCES.md S584 — pinned copy corpus/evidence/sources-r71/S584.html):
S584:817 "Gets the current unbiased interrupt-time count, in units of 100
nanoseconds. The unbiased interrupt-time count does not include time the
system spends in sleep or hibernation."; S584:830 "reflects only the time
that the system is in the working state".

What the probe reports: the two counts side by side, the derived delta, and
the caveats — never an interpretation of the delta as an episode.
- The unbiased count is 100-NANOSECOND units (S584:817), the biased count is
  milliseconds (S582:834); the probe converts unbiased to ms by integer
  FLOOR division by 10000 and names the conversion on the output line, so
  the 10000x unit trap cannot pass silently (selftest arms unit_math and
  conversion_floor pin exact conversions).
- The delta is biased_ms minus unbiased_ms — a DERIVED count across TWO
  SEPARATE read instants (`read_model=two-separate-reads` travels on the
  line): a small negative is a read-skew artifact when the host has been
  awake for the whole boot; the probe never attributes a sleep/hibernation
  episode, never decomposes the boot, and diagnoses nothing (sleep/power
  behavior stays tsukuroi/operator; PROVINCE refuses).
- Error signature (S584:826-827): "If the function succeeds, the return
  value is nonzero. If the function fails because it is called with a null
  parameter, the return value is zero." — a zero RETURN is a failed call and
  maps to unavailable, never to a zero count.
- Debug builds (S584:833, matching S582's alert): both the interrupt-time
  count and the tick count are advanced by approximately 49 days there, so
  BOTH counts shift together on such builds; `debug_build_caveat=carried`
  travels on every line.
- No boot identity: neither API returns one (`boot_identity=absent` on
  every line, never inferred).

Detection and report only. The probe never writes, reconfigures or
remediates anything: it calls two read-only APIs and prints counts and state
words. No process identities, no user names, no computer names, no paths, no
timestamps — counts and shapes only (the lane's redaction rule; the selftest
asserts this against a fixture that carries such values).

Modes
  python tools/mori-workstate-win.py
  python tools/mori-workstate-win.py --fixture PATH   (JSON-injected values)
  python tools/mori-workstate-win.py --selftest

Output
  surface workstate: state=ok biased_ms=N unbiased_100ns=N unbiased_ms=N
          biased_minus_unbiased_ms=N conversion=unbiased_ms-floor(10000)
          read_model=two-separate-reads count=biased+unbiased
          boot_identity=absent debug_build_caveat=carried
  WORKSTATE_WIN: AVAILABLE surfaces=1 ok=1 unavailable=0
or
  surface workstate: state=unavailable reason=<why>
  WORKSTATE_WIN: UNAVAILABLE surfaces=1 ok=0 unavailable=1
A failed call is `unavailable`, never zero (the lane's honest-unavailable
rule); zero IS a real count (S584:829 — anchor corrected :828->:829 by the
r72 S585 erratum; "The interrupt-time count begins at zero when the system
starts"). Exit: 0 available · 2 unavailable or
unreadable/malformed fixture · argparse's own exit (2) for unknown arguments
— usage errors are never a live reading.

Fixture JSON: {"biased_ms": <non-negative int>, "unbiased_100ns":
<non-negative int>} or null (grades the surface unavailable). Exact-key
gate: extra keys (names, paths, token-shaped values) are rejected BEFORE
rendering — never printed (the redaction arm proves the output stays counts
only). Both counts must fit the APIs' unsigned 64-bit domain; the selftest
pins the exact rendering of the domain maximum for both, so a truncating
restype bug cannot pass (the live reader pins c_ulonglong for both the
GetTickCount64 restype and the QueryUnbiasedInterruptTime out-parameter).

Self-test: offline only — its own fixture files in one temp dir, removed on
exit; binary-mode writes (r62 lesson); no child processes, no network, no
live API call. Arms: output grammar; pinned unit arithmetic and the floor
conversion; zero-is-real; honest unavailable; negative rejected;
non-integer rejected; redaction; unsigned-64-max rendering pinned for BOTH
counts (truncation killer); the signed-delta shape pinned (a negative delta
prints as-is with the read-model token, rc 0).

v1 (round 71): initial shape. No baseline, no frozen predecessor. One-shot
read only: the counts are volatile by nature, so the probe claims no series
and no trend — consecutive runs are separate counts, never a rate.
"""

import argparse
import ctypes
import json
import os
import sys
import tempfile


class WorkstateUnavailable(Exception):
    """A surface read that genuinely could not be taken (never zero)."""


# ------------------------------------------------------------------ live reader

def read_workstate_live():
    """GetTickCount64 (S582, ms) + QueryUnbiasedInterruptTime (S584, 100 ns).
    Raises WorkstateUnavailable on any failure."""
    if os.name != "nt":
        raise WorkstateUnavailable("no_windows_kernel32")
    try:
        k32 = ctypes.windll.kernel32
    except AttributeError as exc:
        raise WorkstateUnavailable("no_windows_kernel32:%s" % type(exc).__name__)
    # GetTickCount64 — S582:831 signature ULONGLONG GetTickCount64(void)
    try:
        k32.GetTickCount64.restype = ctypes.c_ulonglong  # else c_int truncates
        biased_ms = k32.GetTickCount64()
    except OSError as exc:
        raise WorkstateUnavailable("kernel32_call_failed:%s" % type(exc).__name__)
    if biased_ms is None:
        raise WorkstateUnavailable("gettickcount64_returned_none")
    # QueryUnbiasedInterruptTime — S584:819-820 BOOL(PLULONGLONG out param)
    try:
        k32.QueryUnbiasedInterruptTime.argtypes = [
            ctypes.POINTER(ctypes.c_ulonglong)]
        k32.QueryUnbiasedInterruptTime.restype = ctypes.c_int  # BOOL
        out = ctypes.c_ulonglong(0)
        ok = k32.QueryUnbiasedInterruptTime(ctypes.byref(out))
    except OSError as exc:
        raise WorkstateUnavailable("kernel32_call_failed:%s" % type(exc).__name__)
    if ok == 0:  # S584:826-827 — zero return is a FAILED call, not a zero count
        raise WorkstateUnavailable("qunbiased_return_zero")
    return int(biased_ms), int(out.value)


# -------------------------------------------------------------------- reporting

def derived(biased_ms, unbiased_100ns):
    """The fixed conversions: floor(unbiased/10000) ms and the signed delta."""
    unbiased_ms = unbiased_100ns // 10000
    return unbiased_ms, biased_ms - unbiased_ms


def render(triple):
    """The surface line plus the summary line. `triple` is a
    (state, values|None, reason|None) triple; value keys are fixed."""
    lines = []
    if triple[0] == "ok":
        v = triple[1]
        unbiased_ms, delta = derived(v["biased_ms"], v["unbiased_100ns"])
        lines.append(
            "surface workstate: state=ok biased_ms=%d unbiased_100ns=%d"
            " unbiased_ms=%d biased_minus_unbiased_ms=%d"
            " conversion=unbiased_ms-floor(10000)"
            " read_model=two-separate-reads count=biased+unbiased"
            " boot_identity=absent debug_build_caveat=carried"
            % (v["biased_ms"], v["unbiased_100ns"], unbiased_ms, delta))
        state = "AVAILABLE"
    else:
        lines.append("surface workstate: state=unavailable reason=%s" % triple[2])
        state = "UNAVAILABLE"
    lines.append("WORKSTATE_WIN: %s surfaces=1 ok=%d unavailable=%d"
                 % (state, 1 if state == "AVAILABLE" else 0,
                    1 if state != "AVAILABLE" else 0))
    return "\n".join(lines), state


def validate(v):
    """Fixture-shape gate: exact keys, non-negative ints, unsigned 64-bit."""
    keys = {"biased_ms", "unbiased_100ns"}
    if set(v) != keys:
        raise ValueError("workstate fixture keys %s" % sorted(v))
    for k in ("biased_ms", "unbiased_100ns"):
        x = v[k]
        if not isinstance(x, int) or isinstance(x, bool) or x < 0:
            raise ValueError("%s must be a non-negative int" % k)
        if x >= (1 << 64):
            raise ValueError("%s exceeds the APIs' unsigned 64-bit domain" % k)


def run(fixture_path=None):
    """One probe pass. Returns (output_text, exit_code)."""
    fixture = None
    if fixture_path is not None:
        try:
            with open(fixture_path, "rb") as fh:
                fixture = json.loads(fh.read().decode("utf-8"))
        except (OSError, ValueError) as exc:
            return "WORKSTATE_WIN_SETUP unreadable fixture: %s" % type(exc).__name__, 2
        if fixture is not None:
            try:
                validate(fixture)
            except ValueError as exc:
                return "WORKSTATE_WIN_SETUP malformed fixture: %s" % exc, 2

    if fixture_path is not None:
        triple = ("unavailable", None, "fixture_null") if fixture is None \
            else ("ok", fixture, None)
    else:
        try:
            biased_ms, unbiased_100ns = read_workstate_live()
            triple = ("ok", {"biased_ms": biased_ms,
                             "unbiased_100ns": unbiased_100ns}, None)
        except WorkstateUnavailable as exc:
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
    root = tempfile.mkdtemp(prefix="mori-workstate-win-selftest-")
    try:
        # 1. grammar: the exact ok-line shape (pinned fixture values;
        #    9_771_840_000_000 x 100-ns units = 977_184_000 ms exactly, delta 0)
        p = _write_fixture(root, "good.json",
                           {"biased_ms": 977_184_000,
                            "unbiased_100ns": 9_771_840_000_000})
        out, rc = run(p)
        lines = out.splitlines()
        checks.append(("grammar", rc == 0 and len(lines) == 2
                       and lines[0] == "surface workstate: state=ok"
                       " biased_ms=977184000 unbiased_100ns=9771840000000"
                       " unbiased_ms=977184000 biased_minus_unbiased_ms=0"
                       " conversion=unbiased_ms-floor(10000)"
                       " read_model=two-separate-reads count=biased+unbiased"
                       " boot_identity=absent debug_build_caveat=carried"
                       and lines[1] == "WORKSTATE_WIN: AVAILABLE surfaces=1"
                       " ok=1 unavailable=0", out))

        # 2. pinned unit arithmetic: the 10000x unit trap (a naive ms-reading
        #    of the 100-ns count would print 9771840000000 here)
        checks.append(("unit_math", "unbiased_ms=977184000" in out
                       and "unbiased_100ns=9771840000000" in out
                       and "unbiased_ms=9771840000000" not in out, out))

        # 3. zero-is-real: a successful read at boot prints zeros, rc 0
        z = _write_fixture(root, "zero.json",
                           {"biased_ms": 0, "unbiased_100ns": 0})
        out0, rc0 = run(z)
        checks.append(("zero_is_real",
                       rc0 == 0 and "biased_ms=0" in out0
                       and "unbiased_100ns=0" in out0
                       and "WORKSTATE_WIN: AVAILABLE" in out0, out0))

        # 4. honest unavailable: null fixture -> UNAVAILABLE, rc 2, no counts
        pn = _write_fixture(root, "none.json", None)
        outn, rcn = run(pn)
        checks.append(("honest_unavailable",
                       rcn == 2
                       and "state=unavailable reason=fixture_null" in outn
                       and "WORKSTATE_WIN: UNAVAILABLE surfaces=1 ok=0"
                       " unavailable=1" in outn, outn))

        # 5/6. malformed: negative and non-integer rejected, rc 2
        b1 = _write_fixture(root, "neg.json",
                            {"biased_ms": -5, "unbiased_100ns": 0})
        outb1, rcb1 = run(b1)
        b2 = _write_fixture(root, "str.json",
                            {"biased_ms": 5, "unbiased_100ns": "soon"})
        outb2, rcb2 = run(b2)
        checks.append(("negative_rejected",
                       rcb1 == 2
                       and outb1.startswith("WORKSTATE_WIN_SETUP malformed fixture"),
                       outb1))
        checks.append(("noninteger_rejected",
                       rcb2 == 2
                       and outb2.startswith("WORKSTATE_WIN_SETUP malformed fixture"),
                       outb2))

        # 7. redaction: fixture carries name/path/token-shaped values;
        #    extra keys are rejected BEFORE rendering, none may print
        leaky = _write_fixture(root, "leaky.json", {
            "biased_ms": 123456, "unbiased_100ns": 1234560000,
            "computer_name": "DESKTOP-SOMEWHERE", "user": "alice",
            "path": "C:\\Users\\somewhere\\secret",
            "token": "0123456789abcdef"})
        outl, rcl = run(leaky)
        checks.append(("redaction",
                       rcl == 2
                       and outl.startswith("WORKSTATE_WIN_SETUP malformed fixture")
                       and "somewhere" not in outl and "alice" not in outl
                       and "secret" not in outl
                       and "0123456789abcdef" not in outl, outl))

        # 8. unsigned-64-max rendering pinned for BOTH counts (a truncating
        #    restype or byref target cannot pass)
        big = _write_fixture(root, "big.json",
                             {"biased_ms": 18_446_744_073_709_551_615,
                              "unbiased_100ns": 18_446_744_073_709_551_615})
        outg, rcg = run(big)
        checks.append(("uint64_max_rendered",
                       rcg == 0
                       and "biased_ms=18446744073709551615" in outg
                       and "unbiased_100ns=18446744073709551615" in outg
                       and "unbiased_ms=1844674407370955" in outg, outg))

        # 9. signed-delta shape: unbiased above biased (read skew on a
        #    never-slept host) prints the negative delta as-is, rc 0
        neg = _write_fixture(root, "negdelta.json",
                             {"biased_ms": 1000, "unbiased_100ns": 20_000_000})
        outd, rcd = run(neg)
        checks.append(("delta_signed_shape",
                       rcd == 0 and "biased_minus_unbiased_ms=-1000" in outd
                       and "read_model=two-separate-reads" in outd
                       and "WORKSTATE_WIN: AVAILABLE" in outd, outd))

        # 10. floor conversion pinned: 9999 100-ns units floors to 0 ms
        f = _write_fixture(root, "floor.json",
                           {"biased_ms": 5, "unbiased_100ns": 9_999})
        outf, rcf = run(f)
        checks.append(("conversion_floor",
                       rcf == 0 and "unbiased_100ns=9999" in outf
                       and "unbiased_ms=0" in outf
                       and "biased_minus_unbiased_ms=5" in outf, outf))
    finally:
        import shutil
        shutil.rmtree(root, ignore_errors=True)

    failed = [c for c in checks if not c[1]]
    for name, ok, detail in checks:
        print("selftest %-20s %s" % (name, "PASS" if ok else "FAIL (%s)" % detail[:80]))
    if failed:
        print("WORKSTATE_WIN_SELFTEST: FAIL (%d/%d)" % (len(checks) - len(failed), len(checks)))
        return 1
    print("WORKSTATE_WIN_SELFTEST: PASS (%d cases)" % len(checks))
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
