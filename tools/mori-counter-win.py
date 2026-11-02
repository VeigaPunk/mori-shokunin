#!/usr/bin/env python3
"""mori-counter-win — one-shot read-only probe of the Windows performance-
counter surface: the commit gauge pair plus the paging-activity rate, read
through the documented `typeperf` command (fleet and host observability;
resource runway and the kill/OOM-adjacent exhaustion class, detection and
report only).

Round 77 (C1 depth sourced + C2 capability acquisition, sourced). Lineage:
the Linux commit-runway read (tools/mori-commit-runway.py, r53 —
CommitLimit/Committed_AS from /proc/meminfo) and the PSI reads are absent on
the Windows workspace host (PROVINCE Round-62 host note); the r63 probe reads
the event-log EXHAUSTION-EVENT history (Event 2004 — the host's own
commit-limit-exhaustion diagnosis, S572 K4); the r64 probe reads the API-side
totals (GlobalMemoryStatusEx). This probe adds the surface between them: the
PDH performance counters, read once through `typeperf` (corpus/SOURCES.md
S592, opened round 77 — the command writes performance data to the command
window or to a log file; the probe reads the command window only and never
writes a log). Pinned copy: corpus/evidence/sources-r77/.

Counter table (pinned in-script; every path below was enumerated on THIS host
by the documented `typeperf -q Memory` listing — S592:798 — receipted live in
the round-77 evidence; a non-English host resolves different localized paths,
so absence is a named unavailable, never zero):
  \\Memory\\Committed Bytes             gauge bytes   the committed figure
  \\Memory\\Commit Limit                gauge bytes   the commit limit
  \\Memory\\% Committed Bytes In Use   gauge percent in-use share
  \\Memory\\Pages/sec                   rate per-s    paging-activity rate

The gauge pair is the same quantity S572's exhaustion semantics name
(commit-limit exhaustion) — read live, on the OS counter surface, instead of
only as an event history (r63) or an API approximation (r64). The rate is
computed by the OS over typeperf's own collection interval; the lane builds
no two-sample instrument of its own (FR6 stays open) and a rate or gauge
sample is not a stall proof and not a cause (FR12 stays open; the Linux PSI
instruments remain the registered gates on Linux hosts).

Detection and report only. The probe never writes, monitors, alerts or
reconfigures anything: the only child process is one `typeperf` read with a
sample bound (`-sc 2`), and the only bytes that leave the parser are counter
paths, numeric values and state words. The machine name the CSV header
carries and every sample timestamp are REDACTED — never printed (the lane's
redaction rule; the selftest asserts both against fixtures that carry them).
No raw typeperf chatter is echoed.

Modes
  python tools/mori-counter-win.py [--child PATH]
  python tools/mori-counter-win.py --fixture PATH
  python tools/mori-counter-win.py --selftest

Live mode runs, once:
  typeperf "\\Memory\\Committed Bytes" "\\Memory\\Commit Limit"
           "\\Memory\\% Committed Bytes In Use" "\\Memory\\Pages/sec" -sc 2
Two samples so the OS-side rate counter has its collection interval
(S592:806 — `-sc` "Specifies the number of samples to collect."; the default
is until CTRL+C, which this probe never relies on). The parser takes the
LAST sample row only and prints `samples=2` so the bound travels with the
receipt. rc 0 with ZERO sample rows on stdout was observed once in the
round-77 exploration — and the sweep caught the CAUSE: that first exploratory
argv carried `-f csv` without `-o`, and typeperf's format option redirects
the samples into the DEFAULT log file `output.csv` in the working directory
(the stray file was found at the lane root, receipted, and removed; the
stdout carried only the status lines). The state itself is real — a stdout
capture can carry a header and no rows — and it reads unavailable with a
named reason, never zero. The probe never passes `-f`, so its stdout is the
only place samples can land.

Fixture mode parses the named CSV file with the same parser (fixture lines
carry a fake host prefix and fake timestamps; the redaction arms prove neither
reaches stdout).

Value grammar: a cell parses as a value only when the whole token matches
`^[0-9]+(\\.[0-9]+)?$` (dot decimal). Anything else (empty, `n/a`, a
thousands-comma token) is unavailable — refused, never misparsed (a locale
that renders decimal commas makes the counter unavailable rather than wrong).

Output: one `counter …` line per counter, then
  `COUNTER_WIN: AVAILABLE|PARTIAL|UNAVAILABLE surfaces=N ok=N unavailable=N samples=2`
with ` reason=<word>` appended when UNAVAILABLE. Zero is a real value (a
parsed 0); a failed read is `unavailable`, never zero (the lane's honest-
unavailable rule). Exit: 0 at least one counter ok · 1 usage/argument ·
2 no counter ok.

Self-test: builds its own fixture CSVs in one temp dir with bytes written in
binary mode (no CRLF translation), then arms: four-counter read, last-sample
selection, host-prefix redaction, timestamp redaction, zero-sample honest
unavailable rc 2, missing column, non-numeric cell, comma-thousands refusal,
missing child rc 2, output shape grammar, usage rc 1 without traceback, and
the kind labels (rate vs gauge). Executes only
`<sys.executable> <this file>` children over its own temp files.

v1 (round 77): initial shape. No baseline, no frozen predecessor. One-shot
reads only: a sample is volatile (the S574:846-847 volatility boundary carries
to the counter surface), so the probe claims no series and no trend.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

SAMPLES = 2
CHILD_TIMEOUT = 60

# (counter path, kind) — pinned; every path enumerated live by `typeperf -q
# Memory` on this host (receipted round 77); see module docstring.
COUNTERS = (
    ("\\Memory\\Committed Bytes", "gauge"),
    ("\\Memory\\Commit Limit", "gauge"),
    ("\\Memory\\% Committed Bytes In Use", "gauge"),
    ("\\Memory\\Pages/sec", "rate"),
)

VALUE_RE = re.compile(r"^[0-9]+(\.[0-9]+)?$")
CELL_RE = re.compile(r'"([^"]*)"')
PDH_HEADER = "(PDH-CSV 4.0)"


def parse_blob(blob, counters):
    """Parse typeperf CSV bytes. Returns (header_present, sample_rows, columns)
    where columns are the header's counter paths with the machine prefix
    stripped, and sample_rows are the per-sample cell lists."""
    text = blob.decode("utf-8", "replace")
    header = None
    columns = []
    samples = []
    for line in text.splitlines():
        cells = CELL_RE.findall(line)
        if not cells or len(cells) < 2:
            continue  # trailing chatter, spinner frames, blank lines
        if header is None:
            if cells[0] == PDH_HEADER:
                header = cells
                for path in cells[1:]:
                    idx = path.upper().find("\\MEMORY\\")
                    if idx >= 0:
                        columns.append(path[idx:])
                    else:
                        columns.append(path)
            continue
        if len(cells) == len(header):
            samples.append(cells)
    return header is not None, samples, columns


def counter_line(path, kind, value):
    if value is None:
        return "counter path=%s kind=%s value=unavailable" % (path, kind)
    return "counter path=%s kind=%s value=%s" % (path, kind, value)


def run(counters, child, fixture_path=None):
    """Returns (verdict, lines, ok_count)."""
    unavailable_reason = None
    if fixture_path is not None:
        try:
            with open(fixture_path, "rb") as f:
                blob = f.read()
        except OSError:
            blob = None
        if blob is None:
            unavailable_reason = "fixture_unreadable"
        else:
            header_present, samples, columns = parse_blob(blob, counters)
    else:
        argv = [child]
        for path, _kind in counters:
            argv.append(path)
        argv += ["-sc", str(SAMPLES)]
        blob = None
        try:
            proc = subprocess.run(
                argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                timeout=CHILD_TIMEOUT)
            if proc.returncode == 0:
                blob = proc.stdout
            else:
                unavailable_reason = "child_rc_%d" % proc.returncode
        except (subprocess.TimeoutExpired, OSError):
            unavailable_reason = "typeperf_missing_or_timeout"
        if blob is not None:
            header_present, samples, columns = parse_blob(blob, counters)

    lines = []
    ok = 0
    if fixture_path is None and unavailable_reason == "typeperf_missing_or_timeout":
        # nothing was read at all
        for path, kind in counters:
            lines.append(counter_line(path, kind, None))
        return "UNAVAILABLE", lines + [summary("UNAVAILABLE", len(counters), 0,
                                               len(counters), unavailable_reason)], 0

    if fixture_path is None and unavailable_reason and unavailable_reason.startswith("child_rc_"):
        for path, kind in counters:
            lines.append(counter_line(path, kind, None))
        return "UNAVAILABLE", lines + [summary("UNAVAILABLE", len(counters), 0,
                                               len(counters), unavailable_reason)], 0

    if fixture_path is not None and blob is None:
        for path, kind in counters:
            lines.append(counter_line(path, kind, None))
        return "UNAVAILABLE", lines + [summary("UNAVAILABLE", len(counters), 0,
                                               len(counters), unavailable_reason)], 0

    if not header_present:
        for path, kind in counters:
            lines.append(counter_line(path, kind, None))
        return "UNAVAILABLE", lines + [summary("UNAVAILABLE", len(counters), 0,
                                               len(counters), "no_pdh_header")], 0
    if not samples:
        # the observed transient: rc 0 but zero sample rows — never zero values
        for path, kind in counters:
            lines.append(counter_line(path, kind, None))
        return "UNAVAILABLE", lines + [summary("UNAVAILABLE", len(counters), 0,
                                               len(counters), "no_sample_rows")], 0

    last = samples[-1]
    columns_lower = [c.lower() for c in columns]
    for path, kind in counters:
        value = None
        if path.lower() in columns_lower:
            idx = columns_lower.index(path.lower())
            if idx + 1 < len(last):
                token = last[idx + 1]
                if VALUE_RE.match(token):
                    value = token
        if value is None:
            lines.append(counter_line(path, kind, None))
        else:
            ok += 1
            lines.append(counter_line(path, kind, value))
    unavailable = len(counters) - ok
    if ok == 0:
        verdict = "UNAVAILABLE"
        lines.append(summary(verdict, len(counters), ok, unavailable,
                             "no_counter_parsed"))
    elif unavailable:
        lines.append(summary("PARTIAL", len(counters), ok, unavailable))
        verdict = "PARTIAL"
    else:
        verdict = "AVAILABLE"
        lines.append(summary(verdict, len(counters), ok, unavailable))
    return verdict, lines, ok


def summary(verdict, surfaces, ok, unavailable, reason=None):
    out = ("COUNTER_WIN: %s surfaces=%d ok=%d unavailable=%d samples=%d"
           % (verdict, surfaces, ok, unavailable, SAMPLES))
    if reason:
        out += " reason=%s" % reason
    return out


def selftest():
    base = tempfile.mkdtemp(prefix="counter-win-selftest-")
    results = []

    def fixture(name, header_paths, sample_rows, chatter=True):
        p = os.path.join(base, name)
        parts = []
        if header_paths is not None:
            cells = [PDH_HEADER] + header_paths
            parts.append(",".join('"%s"' % c for c in cells))
            for row in sample_rows:
                cells = ["2030-01-01 00:00:0%d.000" % (len(parts) % 10)] + list(row)
                parts.append(",".join('"%s"' % c for c in cells))
        if chatter:
            parts.append("Exiting, please wait...")
            parts.append("The command completed successfully.")
        with open(p, "wb") as f:
            f.write(("\r\n".join(parts) + "\r\n").encode("utf-8"))
        return p

    def tool(args):
        proc = subprocess.run([sys.executable, os.path.abspath(__file__)] + args,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              timeout=120)
        return proc.returncode, proc.stdout.decode("utf-8", "replace")

    hosts = ["\\\\HOSTNAME-X9", "\\\\HOSTNAME-X9", "\\\\HOSTNAME-X9",
             "\\\\HOSTNAME-X9"]
    paths = [h + p for h, (p, _k) in zip(hosts, COUNTERS)]

    # 1: four-counter fixture -> AVAILABLE rc 0, values echoed, samples=2
    fx = fixture("four.csv", paths,
                 [["1024", "2048", "12.5", "0.5"], ["1030", "2049", "12.6", "0.7"]])
    rc, out = tool(["--fixture", fx])
    ok1 = rc == 0 and "COUNTER_WIN: AVAILABLE surfaces=4 ok=4 unavailable=0 samples=2" in out \
        and "value=1030" in out and "value=2049" in out
    results.append(("four_counters_available", ok1, "rc=%d" % rc))
    # 2: last sample wins
    fx = fixture("last.csv", paths,
                 [["1", "2", "3.0", "4.0"], ["5", "6", "7.0", "8.0"],
                  ["9", "10", "11.0", "12.0"]])
    rc, out = tool(["--fixture", fx])
    ok2 = rc == 0 and "value=9" in out and "value=10" in out and "value=12.0" in out \
        and "value=1\n" not in out
    results.append(("last_sample_wins", ok2, "rc=%d" % rc))
    # 3: host prefix redacted — the fixture machine name never reaches stdout
    fx = fixture("redact-host.csv", paths,
                 [["1024", "2048", "12.5", "0.5"]])
    rc, out = tool(["--fixture", fx])
    ok3 = rc == 0 and "HOSTNAME-X9" not in out and "path=\\Memory\\Commit Limit" in out
    results.append(("host_prefix_redacted", ok3, "rc=%d" % rc))
    # 4: timestamps redacted
    fx = fixture("redact-ts.csv", paths,
                 [["1024", "2048", "12.5", "0.5"]])
    rc, out = tool(["--fixture", fx])
    ok4 = rc == 0 and "2030-01-01" not in out and "00:00" not in out
    results.append(("timestamps_redacted", ok4, "rc=%d" % rc))
    # 5: header but zero sample rows (the observed transient) -> honest
    #    unavailable rc 2, no zero-faked values
    fx = fixture("empty.csv", paths, [])
    rc, out = tool(["--fixture", fx])
    ok5 = rc == 2 and "UNAVAILABLE" in out and "reason=no_sample_rows" in out \
        and "value=unavailable" in out and "value=0" not in out
    results.append(("zero_samples_honest_unavailable", ok5, "rc=%d" % rc))
    # 6: missing columns -> PARTIAL rc 0, the missing counters unavailable
    fx = fixture("partial.csv", paths[:2],
                 [["1024", "2048"]])
    rc, out = tool(["--fixture", fx])
    ok6 = rc == 0 and "PARTIAL" in out and "ok=2" in out \
        and out.count("value=unavailable") == 2
    results.append(("missing_columns_partial", ok6, "rc=%d" % rc))
    # 7: a non-numeric cell refuses -> unavailable, never a crash, never zero
    fx = fixture("nonnumeric.csv", paths,
                 [["1024", "2048", "n/a", "0.5"]])
    rc, out = tool(["--fixture", fx])
    ok7 = rc == 0 and "PARTIAL" in out \
        and "counter path=\\Memory\\% Committed Bytes In Use kind=gauge value=unavailable" in out
    results.append(("nonnumeric_cell_refused", ok7, "rc=%d" % rc))
    # 8: comma-thousands token refused (locale-safe), not misparsed
    fx = fixture("comma.csv", paths,
                 [["1,024", "2048", "12.5", "0.5"]])
    rc, out = tool(["--fixture", fx])
    ok8 = rc == 0 and "PARTIAL" in out \
        and "counter path=\\Memory\\Committed Bytes kind=gauge value=unavailable" in out
    results.append(("comma_thousands_refused", ok8, "rc=%d" % rc))
    # 9: missing child -> UNAVAILABLE rc 2, reason named, no traceback
    rc, out = tool(["--child", "Z:\\no-such-typeperf.exe"])
    ok9 = rc == 2 and "reason=typeperf_missing_or_timeout" in out \
        and "Traceback" not in out
    results.append(("missing_child_rc2", ok9, "rc=%d" % rc))
    # 10: output shape grammar — every line is `counter …` or the summary
    fx = fixture("shape.csv", paths,
                 [["1024", "2048", "12.5", "0.5"]])
    rc, out = tool(["--fixture", fx])
    lines = [l for l in out.splitlines() if l.strip()]
    ok10 = rc == 0 and lines and all(
        l.startswith("counter path=") or l.startswith("COUNTER_WIN: ")
        for l in lines)
    results.append(("output_shape_grammar", ok10, "rc=%d" % rc))
    # 11: usage — unknown option exits 1 with no traceback
    rc, out = tool(["--no-such-option"])
    ok11 = rc == 1 and "Traceback" not in out
    results.append(("usage_rc1_no_traceback", ok11, "rc=%d" % rc))
    # 12: kind labels — the rate counter labeled rate, gauges gauge
    fx = fixture("kinds.csv", paths,
                 [["1024", "2048", "12.5", "0.5"]])
    rc, out = tool(["--fixture", fx])
    ok12 = rc == 0 \
        and "counter path=\\Memory\\Pages/sec kind=rate value=" in out \
        and "counter path=\\Memory\\Commit Limit kind=gauge value=" in out
    results.append(("kinds_labeled", ok12, "rc=%d" % rc))

    shutil.rmtree(base, ignore_errors=True)
    fails = 0
    for name, ok, last in results:
        print("%s %s  %s" % ("PASS" if ok else "FAIL", name, last))
        fails += 0 if ok else 1
    print("COUNTER_WIN_SELFTEST: PASS (%d cases)" % len(results)
          if fails == 0 else
          "COUNTER_WIN_SELFTEST: FAIL (%d/%d)" % (len(results) - fails, len(results)))
    return 0 if fails == 0 else 1


class _ArgParser(argparse.ArgumentParser):
    # usage/argument errors exit 1 (the documented contract), not argparse's 2
    def error(self, message):
        self.print_usage(sys.stderr)
        print("COUNTER_WIN_SETUP %s" % message, file=sys.stderr)
        sys.exit(1)


def main(argv):
    ap = _ArgParser(add_help=True)
    ap.add_argument("--fixture", default=None)
    ap.add_argument("--child", default=None)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    child = args.child or shutil.which("typeperf")
    if args.fixture is None and child is None:
        lines = [counter_line(p, k, None) for p, k in COUNTERS]
        lines.append(summary("UNAVAILABLE", len(COUNTERS), 0, len(COUNTERS),
                             "typeperf_missing"))
        for l in lines:
            print(l)
        return 2
    verdict, lines, _ok = run(COUNTERS, child, args.fixture)
    for l in lines:
        print(l)
    return 0 if verdict in ("AVAILABLE", "PARTIAL") else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
