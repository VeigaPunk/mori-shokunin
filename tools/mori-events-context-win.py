#!/usr/bin/env python3
"""mori-events-context-win — one-shot read-only PAIRING runner: re-derives the
r63-class Windows event-log kill/exhaustion counts WITH the r70-class boot
window on the same receipt (fleet liveness, kill and OOM events, resource
runway; detection and report only).

Round 71 (C3, operability + capability acquisition). The r70 planned note
asked for exactly this: "pair a fresh host-events re-derivation with the
uptime read so the r63-class event counts travel WITH their boot window (the
context the uptime read exists for)". Before this tool a reader had to run
two probes and bind their outputs mentally; the runner binds them in one
captured receipt, so an events count can never again travel without its
boot-window context line.

It runs the two existing probes as read-only children and prints a bound
summary — it implements nothing against the host itself:
  child 1: <python> tools/mori-host-events-win.py --window N   (r63 build;
           wevtutil qe reads, capped at the window; rc 0 = at least one
           surface ok, rc 2 = no surface ok)
  child 2: <python> tools/mori-uptime-win.py                   (r70 build;
           GetTickCount64; rc 0 available, rc 2 unavailable)
The runner parses ONLY the two children's summary lines (`HOST_EVENTS_WIN:`
and `UPTIME_WIN:`/`surface uptime:` tokens) and prints derived counts and
state words. Child bytes are NEVER echoed: a fixture child-output carrying
computer names, user names, paths or token-shaped values cannot reach this
tool's stdout (the redaction arm proves it). Both children are counts-only
by their own selftests; this runner re-asserts it at its own boundary.

The binding's declared limit (`boot_binding=none` travels on every receipt):
the events window is the probe's RECENT-N window, NOT boot-scoped — the pair
shares the host, never a time window. The boot window value (uptime_ms)
travels beside the events counts as CONTEXT so a reader can grade how much
boot the observation accumulated inside; the runner asserts nothing about
liveness and attributes nothing to the boot (both probes' boundaries carry
through unchanged).

Modes
  python tools/mori-events-context-win.py [--window N]
  python tools/mori-events-context-win.py --fixture-dir DIR
  python tools/mori-events-context-win.py --selftest

Output (fixed grammar)
  events-context: events_state=<AVAILABLE|PARTIAL|UNAVAILABLE> matched=N
          window=N surfaces=N ok=N
  events-context: uptime_state=<AVAILABLE|UNAVAILABLE> uptime_ms=N
          count=<word> boot_identity=<word>
  events-context: boot_binding=none events_window=recent-N-not-boot-scoped
  EVENTS_CONTEXT_WIN: PAIRED events_ok=1 uptime_ok=1        (rc 0)
or the failing-leg reason words (`events_reason=`/`uptime_reason=`) and
  EVENTS_CONTEXT_WIN: UNAVAILABLE events_ok=.. uptime_ok=..  (rc 2)
Exit: 0 both children rc 0 · 2 a leg unavailable/unparseable · 1 usage.

Fixture mode reads pre-captured child stdout blocks `events-output.txt` and
`uptime-output.txt` in DIR through the same parser; a missing file or a
block without its summary line is a leg `unavailable` (reason
fixture_missing / unparseable_summary) — never guessed.

Self-test: offline only — its own fixture dirs in one temp dir, removed on
exit; binary-mode writes (r62 lesson); no live child in the selftest except
`<sys.executable> <this file>` over its own fixture dirs. Arms: pair
grammar; window echo agreement; events leg unavailable; uptime leg
unavailable; unparseable summary rejected; missing fixture file; redaction
against fixture outputs carrying computer/user/path/token values; uptime
echo; PARTIAL events still pairs (state word travels, rc 0); the
boot_binding=none limit line pinned.

v1 (round 71): initial shape. No baseline, no frozen predecessor. One-shot
pair only: counts are volatile, so consecutive runs are separate counts,
never a rate.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

CHILD_TIMEOUT = 60
WINDOW_DEFAULT = 200

EVENTS_SUMMARY_RE = re.compile(
    r"HOST_EVENTS_WIN: (AVAILABLE|PARTIAL|UNAVAILABLE) surfaces=(\d+)"
    r" ok=(\d+) unavailable=(\d+) matched=(\d+) window=(\d+) recent_first=(\w+)")
UPTIME_SUMMARY_RE = re.compile(r"UPTIME_WIN: (AVAILABLE|UNAVAILABLE)")
UPTIME_SURFACE_RE = re.compile(
    r"surface uptime: state=\w+ uptime_ms=(\d+).*?"
    r"count=(\S+) boot_identity=(\S+)")


class LegUnavailable(Exception):
    """One leg genuinely could not be taken or parsed (never guessed)."""


def _child(argv):
    """One bounded read-only child run. Returns stdout text (str)."""
    try:
        proc = subprocess.run(
            [sys.executable] + argv,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=CHILD_TIMEOUT)
    except (subprocess.TimeoutExpired, OSError) as exc:
        raise LegUnavailable("child_failed:%s" % type(exc).__name__)
    if proc.returncode != 0:
        raise LegUnavailable("child_rc=%d" % proc.returncode)
    try:
        return proc.stdout.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise LegUnavailable("child_undecodable:%s" % type(exc).__name__)


def parse_events(blob):
    """Extract the events summary tokens, or raise (never guess)."""
    m = EVENTS_SUMMARY_RE.search(blob)
    if not m:
        raise LegUnavailable("unparseable_summary")
    return {"state": m.group(1), "surfaces": int(m.group(2)),
            "ok": int(m.group(3)), "unavailable": int(m.group(4)),
            "matched": int(m.group(5)), "window": int(m.group(6))}


def parse_uptime(blob):
    """Extract the uptime summary tokens, or raise (never guess)."""
    ms = UPTIME_SUMMARY_RE.search(blob)
    mu = UPTIME_SURFACE_RE.search(blob)
    if not ms or not mu:
        raise LegUnavailable("unparseable_summary")
    return {"state": ms.group(1), "uptime_ms": int(mu.group(1)),
            "count": mu.group(2), "boot_identity": mu.group(3)}


def _fixture_leg(name, fixture_dir):
    path = os.path.join(fixture_dir, name)
    if not os.path.isfile(path):
        raise LegUnavailable("fixture_missing")
    try:
        with open(path, "rb") as fh:
            return fh.read().decode("utf-8", errors="replace")
    except OSError as exc:
        raise LegUnavailable("fixture_unreadable:%s" % type(exc).__name__)


def run(window=None, fixture_dir=None):
    """One paired pass. Returns (output_text, exit_code)."""
    try:
        if fixture_dir is not None:
            events = parse_events(_fixture_leg("events-output.txt", fixture_dir))
        else:
            events = parse_events(_child(
                [os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "mori-host-events-win.py"),
                 "--window", str(window)]))
        if events["state"] == "UNAVAILABLE":
            # fixture mode: a captured UNAVAILABLE summary IS a down leg
            # (live mode already maps it to child_rc=2 before parsing)
            raise LegUnavailable("leg_state_unavailable")
        events_ok = 1
    except LegUnavailable as exc:
        events, events_ok = None, 0
        events_reason = str(exc)
    try:
        if fixture_dir is not None:
            uptime = parse_uptime(_fixture_leg("uptime-output.txt", fixture_dir))
        else:
            uptime = parse_uptime(_child(
                [os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "mori-uptime-win.py")]))
        if uptime["state"] == "UNAVAILABLE":
            raise LegUnavailable("leg_state_unavailable")
        uptime_ok = 1
    except LegUnavailable as exc:
        uptime, uptime_ok = None, 0
        uptime_reason = str(exc)

    lines = []
    if events is not None:
        lines.append("events-context: events_state=%s matched=%d window=%d"
                     " surfaces=%d ok=%d"
                     % (events["state"], events["matched"], events["window"],
                        events["surfaces"], events["ok"]))
    else:
        lines.append("events-context: events_state=unavailable events_reason=%s"
                     % events_reason)
    if uptime is not None:
        lines.append("events-context: uptime_state=%s uptime_ms=%d"
                     " count=%s boot_identity=%s"
                     % (uptime["state"], uptime["uptime_ms"],
                        uptime["count"], uptime["boot_identity"]))
    else:
        lines.append("events-context: uptime_state=unavailable uptime_reason=%s"
                     % uptime_reason)
    lines.append("events-context: boot_binding=none"
                 " events_window=%s"
                 % ("recent-%d-not-boot-scoped" % events["window"]
                    if events is not None else "unavailable"))
    paired = events_ok == 1 and uptime_ok == 1
    lines.append("EVENTS_CONTEXT_WIN: %s events_ok=%d uptime_ok=%d"
                 % ("PAIRED" if paired else "UNAVAILABLE", events_ok, uptime_ok))
    return "\n".join(lines), (0 if paired else 2)


# --------------------------------------------------------------------- selftest

def _write(directory, name, payload):
    path = os.path.join(directory, name)
    with open(path, "wb") as fh:  # binary mode: no CRLF translation (r62 lesson)
        fh.write(payload.encode("utf-8"))
    return path


EVENTS_GOOD = (
    "surface System/2004: state=ok matched=0 window=200\n"
    "surface Application/1000: state=ok matched=0 window=200\n"
    "surface Application/1001: state=ok matched=0 window=200\n"
    "surface System/6008: state=ok matched=0 window=200\n"
    "HOST_EVENTS_WIN: AVAILABLE surfaces=4 ok=4 unavailable=0 matched=0"
    " window=200 recent_first=true")

UPTIME_GOOD = (
    "surface uptime: state=ok uptime_ms=493623375 uptime_s=493623 uptime_d=5"
    " count=biased boot_identity=absent\n"
    "UPTIME_WIN: AVAILABLE surfaces=1 ok=1 unavailable=0")


def _selftest():
    checks = []
    root = tempfile.mkdtemp(prefix="mori-events-context-selftest-")
    try:
        def mkpair(name, events_blob, uptime_blob):
            d = os.path.join(root, name)
            os.makedirs(d, exist_ok=True)
            _write(d, "events-output.txt", events_blob)
            _write(d, "uptime-output.txt", uptime_blob)
            return d

        # 1. pair grammar: the exact four-line shape, rc 0
        d = mkpair("good", EVENTS_GOOD, UPTIME_GOOD)
        out, rc = run(fixture_dir=d)
        lines = out.splitlines()
        checks.append(("pair_grammar", rc == 0 and len(lines) == 4
                       and lines[0] == "events-context: events_state=AVAILABLE"
                       " matched=0 window=200 surfaces=4 ok=4"
                       and lines[1] == "events-context: uptime_state=AVAILABLE"
                       " uptime_ms=493623375 count=biased boot_identity=absent"
                       and lines[2] == "events-context: boot_binding=none"
                       " events_window=recent-200-not-boot-scoped"
                       and lines[3] == "EVENTS_CONTEXT_WIN: PAIRED events_ok=1"
                       " uptime_ok=1", out))

        # 2. window echo agreement (line 1 and line 3 carry the same window)
        checks.append(("window_echo", "window=200" in lines[0]
                       and "events_window=recent-200-not-boot-scoped" in out
                       and "window=" in lines[0], out))

        # 3. events leg unavailable: rc 2, events_ok=0, uptime leg intact
        d = mkpair("evdown",
                   "HOST_EVENTS_WIN: UNAVAILABLE surfaces=4 ok=0"
                   " unavailable=4 matched=0 window=200 recent_first=true",
                   UPTIME_GOOD)
        out3, rc3 = run(fixture_dir=d)
        checks.append(("events_unavailable",
                       rc3 == 2 and "events_ok=0" in out3
                       and "uptime_ok=1" in out3
                       and "EVENTS_CONTEXT_WIN: UNAVAILABLE" in out3, out3))

        # 4. uptime leg unavailable: rc 2, uptime_ok=0, events leg intact
        d = mkpair("uptdown", EVENTS_GOOD,
                   "surface uptime: state=unavailable reason=fixture_null\n"
                   "UPTIME_WIN: UNAVAILABLE surfaces=1 ok=0 unavailable=1")
        out4, rc4 = run(fixture_dir=d)
        checks.append(("uptime_unavailable",
                       rc4 == 2 and "uptime_ok=0" in out4
                       and "events_ok=1" in out4
                       and "uptime_state=unavailable uptime_reason=" in out4,
                       out4))

        # 5. unparseable events summary rejected, never guessed
        d = mkpair("garbage", "totally: unrelated bytes", UPTIME_GOOD)
        out5, rc5 = run(fixture_dir=d)
        checks.append(("unparseable_rejected",
                       rc5 == 2
                       and "events_reason=unparseable_summary" in out5
                       and "events_ok=0" in out5, out5))

        # 6. missing fixture file is a leg unavailable
        d6 = os.path.join(root, "missing")
        os.makedirs(d6, exist_ok=True)
        _write(d6, "events-output.txt", EVENTS_GOOD)
        out6, rc6 = run(fixture_dir=d6)
        checks.append(("fixture_missing",
                       rc6 == 2 and "uptime_reason=fixture_missing" in out6
                       and "uptime_ok=0" in out6, out6))

        # 7. redaction: per-surface child lines carry computer/user/path/token
        #    values; the runner prints ONLY its summary-derived counts — none
        #    of the values may reach its stdout
        leaky_events = (
            "surface System/2004: state=ok computer=DESKTOP-SOMEWHERE"
            " user=alice path=C:\\Users\\somewhere\\secret token=0123456789abcdef\n"
            "HOST_EVENTS_WIN: AVAILABLE surfaces=4 ok=4 unavailable=0 matched=0"
            " window=200 recent_first=true")
        d = mkpair("leaky", leaky_events, UPTIME_GOOD)
        outl, rcl = run(fixture_dir=d)
        checks.append(("redaction",
                       rcl == 0 and "SOMEWHERE" not in outl
                       and "alice" not in outl and "somewhere" not in outl
                       and "0123456789abcdef" not in outl, outl))

        # 8. uptime echo: the parsed boot-window value travels verbatim
        checks.append(("uptime_echo", "uptime_ms=493623375" in out, out))

        # 9. PARTIAL events still pairs: state word travels, rc 0
        d = mkpair("partial",
                   EVENTS_GOOD.replace("HOST_EVENTS_WIN: AVAILABLE",
                                       "HOST_EVENTS_WIN: PARTIAL")
                   .replace("ok=4 unavailable=0", "ok=3 unavailable=1"),
                   UPTIME_GOOD)
        outp, rcp = run(fixture_dir=d)
        checks.append(("partial_pairs",
                       rcp == 0 and "events_state=PARTIAL" in outp
                       and "EVENTS_CONTEXT_WIN: PAIRED" in outp, outp))

        # 10. the boot_binding=none limit line is pinned (the no-boot-
        #     attribution rule travels on every receipt)
        checks.append(("binding_line",
                       "boot_binding=none" in out
                       and "not-boot-scoped" in out, out))
    finally:
        shutil.rmtree(root, ignore_errors=True)

    failed = [c for c in checks if not c[1]]
    for name, ok, detail in checks:
        print("selftest %-20s %s" % (name, "PASS" if ok else "FAIL (%s)" % detail[:80]))
    if failed:
        print("EVENTS_CONTEXT_SELFTEST: FAIL (%d/%d)" % (len(checks) - len(failed), len(checks)))
        return 1
    print("EVENTS_CONTEXT_SELFTEST: PASS (%d cases)" % len(checks))
    return 0


def main(argv):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--window", type=int, default=WINDOW_DEFAULT)
    parser.add_argument("--fixture-dir")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        return _selftest()
    if args.window < 1:
        parser.error("--window must be >= 1")
    text, rc = run(window=args.window, fixture_dir=args.fixture_dir)
    print(text)
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
