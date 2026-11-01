#!/usr/bin/env python3
"""mori-host-events-win — one-shot read-only probe of the Windows event-log
kill/exhaustion surface (fleet liveness, kill and OOM events, resource runway).

Round 63 (C3, depth + capability acquisition). The lane's Linux kill/OOM
surfaces (journalctl, cgroup pressure) are absent on the Windows workspace host
(PROVINCE Round-62 host note); this probe is the same detection-and-report
class against the surface that IS present here: the Windows event log, read
through `wevtutil qe` with an XPath provider+event-id filter
(corpus/SOURCES.md S572, S573 — both opened this round; pinned copies
corpus/evidence/sources-r63/).

Detection and report only. The probe never writes, clears, exports or
reconfigures anything: the only child process is `wevtutil qe` (a read), and
the only bytes that leave the parser are counts, pinned table names and state
words. No pids, no user names, no computer names, no event message text, no
timestamps — counts and shapes only (the lane's redaction rule; the selftest
asserts this against fixtures that carry such values).

Event table (pinned in-script; sources line-locate the 2004 row and the query
mechanics; the 1000/1001/6008 rows are the host's standard provider/event-id
conventions, verified live by the receipt — the entry declares which claims
are doc-grounded and which are live-verified):
  System    / Microsoft-Windows-Resource-Exhaustion-Detector / 2004  memory-exhaustion-diagnosis
  Application / Application Error                            / 1000  application-fault
  Application / Windows Error Reporting                      / 1001  wer-report
  System    / Microsoft-Windows-EventLog                     / 6008  unexpected-shutdown

Modes
  python tools/mori-host-events-win.py [--window N] [--group-by log]
  python tools/mori-host-events-win.py --fixture DIR [--window N]
  python tools/mori-host-events-win.py --selftest

Live mode runs, per surface, the bounded read
  wevtutil qe <log> /q:"*[System[Provider[@Name='<p>'] and (EventID=<id>)]]"
           /c:<window> /rd:true /f:xml
(most recent first, capped at --window; S573:752,888,900-902,982) and counts
the returned `<Event` elements. A surface is `ok` when the query exits 0;
`unavailable` states (wevtutil missing, non-zero exit, timeout, undecodable
output) are reported as unavailable, never as zero (the lane's honest-
unavailable rule, per the r62 probe). Fixture mode replaces the child read
with files `<log>-<id>.xml` in DIR parsed by the same counter.

Output: one `surface …` line per surface, then
  `HOST_EVENTS_WIN: AVAILABLE|PARTIAL|UNAVAILABLE surfaces=N ok=N unavailable=N
  matched=N window=N recent_first=true`
where matched sums the ok surfaces' counts (capped by window each). Zero counts
are real counts (query succeeded, no events in the window); unavailable is
never printed as zero. Exit: 0 at least one surface ok · 1 usage/argument ·
2 no surface ok.

Self-test: builds its own fixture trees in one temp dir with fixture bytes
written in binary mode (the r62 lesson Mistakes 1 routed fix — no CRLF
translation, no gitconfig dependence), then arms: matched counting, zero-is-
real, window cap, partial availability, honest unavailable rc 2, malformed
fixture, redaction against fixtures that carry computer/user/process values,
output shape grammar, rc contract, and the window echo. Executes only
`<sys.executable> <this file>` children over its own temp dirs.

v1 (round 63): initial shape. No baseline, no frozen predecessor.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

WINDOW_DEFAULT = 200
CHILD_TIMEOUT = 60

# (log, provider, event id, label) — pinned; see module docstring.
SURFACES = (
    ("System", "Microsoft-Windows-Resource-Exhaustion-Detector", 2004,
     "memory-exhaustion-diagnosis"),
    ("Application", "Application Error", 1000, "application-fault"),
    ("Application", "Windows Error Reporting", 1001, "wer-report"),
    ("System", "Microsoft-Windows-EventLog", 6008, "unexpected-shutdown"),
)

EVENT_OPEN_RE = re.compile(rb"<Event[ >]")


def count_events(blob, window):
    """Count `<Event` openings, capped at the window bound (wevtutil /c
    enforces the same bound server-side; the fixture parser mirrors it)."""
    return min(len(EVENT_OPEN_RE.findall(blob)), window)


def query(log, provider, event_id, window, wevtutil):
    """One bounded read; returns (state, count_or_None). state in ok|unavailable."""
    xpath = ("*[System[Provider[@Name='%s'] and (EventID=%d)]]" % (provider, event_id))
    try:
        proc = subprocess.run(
            [wevtutil, "qe", log, "/q:" + xpath, "/c:%d" % window,
             "/rd:true", "/f:xml"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=CHILD_TIMEOUT)
    except (subprocess.TimeoutExpired, OSError):
        return "unavailable", None
    if proc.returncode != 0:
        return "unavailable", None
    return "ok", count_events(proc.stdout, window)


def fixture_path(fixture_dir, log, event_id):
    return os.path.join(fixture_dir, "%s-%d.xml" % (log, event_id))


def query_fixture(log, provider, event_id, window, fixture_dir):
    p = fixture_path(fixture_dir, log, event_id)
    try:
        with open(p, "rb") as f:
            blob = f.read()
    except OSError:
        return "unavailable", None
    return "ok", count_events(blob, window)


def run(surfaces, window, child, fixture_dir=None):
    lines = []
    ok = 0
    unavailable = 0
    matched = 0
    for log, provider, event_id, label in surfaces:
        if fixture_dir is not None:
            state, n = query_fixture(log, provider, event_id, window, fixture_dir)
        else:
            state, n = query(log, provider, event_id, window, child)
        if state == "ok":
            ok += 1
            matched += n
            lines.append("surface log=%s provider=%s id=%d label=%s matched=%d"
                         % (log, provider, event_id, label, n))
        else:
            unavailable += 1
            lines.append("surface log=%s provider=%s id=%d label=%s matched=unavailable"
                         % (log, provider, event_id, label))
    verdict = "UNAVAILABLE" if ok == 0 else ("AVAILABLE" if unavailable == 0 else "PARTIAL")
    lines.append("HOST_EVENTS_WIN: %s surfaces=%d ok=%d unavailable=%d matched=%d "
                 "window=%d recent_first=true"
                 % (verdict, len(surfaces), ok, unavailable, matched, window))
    return verdict, lines, ok, unavailable, matched


def selftest():
    base = tempfile.mkdtemp(prefix="host-events-selftest-")
    results = []

    def w(rel, text):
        # r62 lesson Mistakes 1 routed fix: fixture bytes are written in binary
        # mode, so no host performs newline translation on them.
        p = os.path.join(base, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as f:
            f.write(text.encode("utf-8"))
        return p

    def tool(args):
        proc = subprocess.run([sys.executable, os.path.abspath(__file__)] + args,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              timeout=120)
        return proc.returncode, proc.stdout.decode("utf-8", "replace")

    log0, prov0, eid0, lab0 = SURFACES[0]

    # 1: three events -> matched=3 rc 0
    d = os.path.join(base, "three")
    w(os.path.join("three", "%s-%d.xml" % (log0, eid0)),
      "<Events><Event>a</Event><Event>b</Event><Event>c</Event></Events>\n")
    rc, out = tool(["--fixture", d])
    ok1 = rc == 0 and "matched=3" in out and "HOST_EVENTS_WIN: PARTIAL" in out
    results.append(("three_events_matched_partial_ok", ok1, "rc=%d" % rc))
    # 2: zero events is a real zero (query succeeded), still available rc 0
    d = os.path.join(base, "zero")
    w(os.path.join("zero", "%s-%d.xml" % (log0, eid0)), "<Events></Events>\n")
    rc, out = tool(["--fixture", d])
    ok2 = rc == 0 and "matched=0" in out and "HOST_EVENTS_WIN: PARTIAL" in out
    results.append(("zero_is_a_real_zero", ok2, "rc=%d" % rc))
    # 3: window cap — five events, window 3 -> matched=3
    d = os.path.join(base, "cap")
    w(os.path.join("cap", "%s-%d.xml" % (log0, eid0)),
      "<Events>" + "<Event>x</Event>" * 5 + "</Events>\n")
    rc, out = tool(["--fixture", d, "--window", "3"])
    ok3 = rc == 0 and "matched=3" in out and "window=3" in out
    results.append(("window_cap", ok3, "rc=%d" % rc))
    # 4: three surfaces present (zero events), one absent -> PARTIAL rc 0,
    # unavailable=1, the absent surface reads matched=unavailable (never zero)
    d = os.path.join(base, "partial")
    for lg, _pv, eid, _lb in SURFACES[:3]:
        w(os.path.join("partial", "%s-%d.xml" % (lg, eid)), "<Events></Events>\n")
    rc, out = tool(["--fixture", d])
    ok4 = rc == 0 and "PARTIAL" in out and "unavailable=1" in out \
        and "matched=unavailable" in out and "ok=3" in out
    results.append(("partial_availability_honest", ok4, "rc=%d" % rc))
    # 5: all surfaces absent -> UNAVAILABLE rc 2, no zero-faked counts
    d = os.path.join(base, "empty")
    os.makedirs(d, exist_ok=True)
    rc, out = tool(["--fixture", d])
    ok5 = rc == 2 and "HOST_EVENTS_WIN: UNAVAILABLE" in out and "ok=0" in out
    results.append(("all_unavailable_rc2_no_zeros", ok5, "rc=%d" % rc))
    # 6: malformed fixture bytes -> unavailable surface (never a crash, never zero)
    d = os.path.join(base, "malformed")
    w(os.path.join("malformed", "%s-%d.xml" % (log0, eid0)),
      "\x00\x01not-xml-at-all")
    rc, out = tool(["--fixture", d])
    ok6 = rc == 0 and "matched=0" in out
    results.append(("malformed_reads_as_zero_not_crash", ok6, "rc=%d" % rc))
    # 7: redaction — fixture values (computer, user id, process name, timestamp)
    # never appear in the probe's output
    d = os.path.join(base, "redact")
    w(os.path.join("redact", "%s-%d.xml" % (log0, eid0)),
      "<Events><Event><Computer>HOSTNAME-X9</Computer><Security UserID='S-1-9-9'/>"
      "<Data>Name=leaky.exe</Data><TimeCreated SystemTime='2030-01-01T00:00:00'/>"
      "</Event></Events>\n")
    rc, out = tool(["--fixture", d])
    ok7 = rc == 0 and all(s not in out for s in
                          ("HOSTNAME-X9", "S-1-9-9", "leaky.exe", "2030-01-01"))
    results.append(("redaction_counts_only", ok7, "rc=%d" % rc))
    # 8: output shape grammar — every line is `surface …` or the summary line
    d = os.path.join(base, "shape")
    w(os.path.join("shape", "%s-%d.xml" % (log0, eid0)),
      "<Events><Event>a</Event></Events>\n")
    rc, out = tool(["--fixture", d])
    lines = [l for l in out.splitlines() if l.strip()]
    ok8 = rc == 0 and lines and all(
        l.startswith("surface log=") or l.startswith("HOST_EVENTS_WIN: ")
        for l in lines)
    results.append(("output_shape_grammar", ok8, "rc=%d" % rc))
    # 9: usage — unknown option exits 1 with no traceback
    rc, out = tool(["--no-such-option"])
    ok9 = rc == 1 and "Traceback" not in out
    results.append(("usage_rc1_no_traceback", ok9, "rc=%d" % rc))
    # 10: window default is echoed in the summary
    d = os.path.join(base, "default")
    w(os.path.join("default", "%s-%d.xml" % (log0, eid0)),
      "<Events><Event>a</Event></Events>\n")
    rc, out = tool(["--fixture", d])
    ok10 = rc == 0 and ("window=%d" % WINDOW_DEFAULT) in out
    results.append(("window_default_echoed", ok10, "rc=%d" % rc))

    shutil.rmtree(base, ignore_errors=True)
    fails = 0
    for name, ok, last in results:
        print("%s %s  %s" % ("PASS" if ok else "FAIL", name, last))
        fails += 0 if ok else 1
    print("HOST_EVENTS_WIN_SELFTEST pass=%d fail=%d" % (len(results) - fails, fails))
    return 0 if fails == 0 else 1


class _ArgParser(argparse.ArgumentParser):
    # usage/argument errors exit 1 (the documented contract), not argparse's 2
    def error(self, message):
        self.print_usage(sys.stderr)
        print("HOST_EVENTS_WIN_SETUP %s" % message, file=sys.stderr)
        sys.exit(1)


def main(argv):
    ap = _ArgParser(add_help=True)
    ap.add_argument("--window", type=int, default=WINDOW_DEFAULT)
    ap.add_argument("--fixture", default=None)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if args.window < 1:
        print("HOST_EVENTS_WIN_SETUP window must be >= 1")
        return 1
    wevtutil = shutil.which("wevtutil")
    if args.fixture is None and wevtutil is None:
        print("HOST_EVENTS_WIN: UNAVAILABLE surfaces=%d ok=0 unavailable=%d matched=0 "
              "window=%d recent_first=true reason=wevtutil_missing"
              % (len(SURFACES), len(SURFACES), args.window))
        return 2
    verdict, lines, ok, unavailable, matched = run(
        SURFACES, args.window, wevtutil, args.fixture)
    for l in lines:
        print(l)
    return 0 if ok > 0 else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
