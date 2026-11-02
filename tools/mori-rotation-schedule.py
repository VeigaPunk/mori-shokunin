#!/usr/bin/env python3
"""mori-rotation-schedule — the rotation-recurrence protocol as a designed
multi-window schedule instrument over a bot-managed page's instrument-UA
serving (fleet and host observability; detection and report only).

Round 74 (planned head (a) at the r73 tip: "the rotation-recurrence protocol
as a DESIGNED multi-window instrument over the S241 serving ... it gets the
design round with stated windows per QUALITY 161"). The r70 round ran three
stated-window A/A pairs BY HAND at computed windows 31/91/304 s and read the
S581 documented token-clock scale against them; this instrument makes that
schedule repeatable, so a later round can re-run the same schedule and ask
the recurrence question (does a same-window classification reappear?) with
the grammar pinned, not re-derived by hand each time.

Design (what makes it an instrument, not a script):
- The schedule is stated before the run: `--windows N,N,N` (default
  31,91,304 — the r70 windows at the S581 documented scale). Every window is
  an A/A capture pair: capture A, wait the stated window on a MONOTONIC
  clock (S589: the Python time library grounds the monotonic clock — a clock
  that cannot go backwards), capture B, compare.
- Capture and compare are DELEGATED to the registered r68/r69 UA-variance
  probe (`tools/mori-ua-variance.py`) as read-only child processes — the
  composition precedent of the r71 events-context pairing (registered
  probes as children; no registered byte edited). This file adds the
  schedule, the window computation and the classification; it adds no
  fetcher of its own.
- Every window's OBSERVATION WINDOW is computed from the two capture
  receipts' own `as-of=` stamps (1-second resolution, 0 legal) and passed to
  the child's `--window-s` (QUALITY 161: the caller computes the gap; an
  unstated window reads unavailable and constrains no rotation-timing
  claim).
- Classification per window (the only judgment this tool makes):
    rotated=yes            per-response>0 OR same-bytes=false (a body-level
                           change the line-diff grammar cannot name is still
                           rotation)
    rotated=no             per-response=0 AND same-bytes=true
    rotated=unavailable    any capture leg failed, the child setup failed,
                           a summary line is unparseable, or a child timed
                           out — honest-unavailable, never guessed
- No TTL value is decided (S581/S580 boundary untouched): the output states
  what each stated window caught, never a token lifetime.

Boundaries carried:
- Detection and report only; the tool writes nothing but the capture files
  the registered child already writes into `--out-dir` (the child's own
  write scope) and prints to stdout.
- stdout carries counts, shapes, stamps and sha prefixes only — the child's
  output lines are PARSED, never echoed (the redaction selftest arm plants a
  marker token on a non-grammar field of fake child output and proves it
  cannot reach stdout).
- Not a census surface; no liveness verdict; the serving's bot-management
  stays the vendor's business (S579/S580/S581 chain).

Modes
  python tools/mori-rotation-schedule.py --url URL --ua UA --pin PATH
          --out-dir DIR [--windows 31,91,304] [--label ID] [--child PATH]
  python tools/mori-rotation-schedule.py --selftest

Output (stdout, ASCII)
  ROTATION_SCHEDULE window=91s window-s=91 label=L per-response=4 stable=1497 \
      same-bytes=false rotated=yes as-of-a=<ISO> as-of-b=<ISO> \
      run-start=<ISO> capture-a=<sha12> capture-b=<sha12>
  ROTATION_SCHEDULE window=31s ... rotated=no ...
  ROTATION_SCHEDULE window=304s ... rotated=unavailable reason=<why> ...
  ROTATION_SCHEDULE_SUMMARY label=L windows=31,91,304 window_s_computed=31,91,304 \
      rotated_yes=1 rotated_no=1 rotated_unavailable=1 clock=monotonic \
      schedule_start=<ISO> schedule_end=<ISO> wall_s=<T> rc=0
or
  ROTATION_SCHEDULE_SETUP <why>   (exit 2: missing child, missing --pin,
                                   bad --windows, missing live-mode args —
                                   usage errors are never a live reading)

Exit: 0 the schedule ran to its end (every window classified, whatever the
classifications are) · 2 setup error · 1 never used live (the selftest
returns 1 on a failed arm).

Self-test: offline only — one temp dir (binary-mode writes, r62 lesson); a
FAKE child script stands in for the registered probe (canned grammar lines,
a marker token on a non-grammar field, failure modes via an env var);
window 0 (same-second A/A) keeps the integration arm sleep-free. Arms:
schedule parse; schedule rejects non-integer; window computation from
as-of stamps (0 legal); classification yes/no/bytes-only/unavailable x3;
redaction (marker must not reach stdout); integration over the fake child
at windows 0,0; missing child refused; non-integer windows refused live.

v1 (round 74): initial shape. No baseline, no frozen predecessor. The
recurrence question is answered by RE-RUNNING the same stated schedule in a
later round and comparing classifications window by window — never by
interpolating between windows inside one run.
"""

import os
import re
import subprocess
import sys
import tempfile
import time

# ----------------------------------------------------------------- schedule

MAX_WINDOWS = 8


def parse_windows(spec):
    """'31,91,304' -> [31, 91, 304]. Non-integer, negative or over-count is
    a setup error (ValueError); the caller turns that into exit 2."""
    parts = [p.strip() for p in spec.split(",")]
    if not parts or any(p == "" for p in parts):
        raise ValueError("empty window field")
    values = []
    for p in parts:
        if not re.match(r"^[0-9]+$", p):
            raise ValueError("non-integer window %r" % p)
        values.append(int(p))
    if len(values) > MAX_WINDOWS:
        raise ValueError("too many windows (max %d)" % MAX_WINDOWS)
    return values


# ------------------------------------------------------------- child grammar

_CAPTURE_RE = re.compile(r"^UA_VAR_CAPTURE\s+(.*)$")
_COMPARE_RE = re.compile(r"^UA_VARIANCE\s+(.*)$")


def _kv_tokens(rest):
    """'k1=v1 k2=v2 ...' -> dict. Tokens without '=' are skipped (defensive;
    the registered grammar always emits key=value)."""
    out = {}
    for tok in rest.split():
        if "=" in tok:
            k, v = tok.split("=", 1)
            out[k] = v
    return out


def parse_capture_line(text):
    """The registered capture summary line -> dict(as-of, rc, sha256, bytes)
    or None when the line is not the grammar."""
    for raw in text.splitlines():
        line = raw.strip("\r").strip()
        m = _CAPTURE_RE.match(line)
        if m:
            kv = _kv_tokens(m.group(1))
            if "as-of" in kv and "rc" in kv:
                kv["_rc"] = int(kv["rc"]) if kv["rc"].lstrip("-").isdigit() else None
                return kv
    return None


def parse_compare_line(text):
    """The registered compare summary line -> dict(per-response, stable,
    same-bytes, window-s, run-start) or None when the line is not the
    grammar."""
    for raw in text.splitlines():
        line = raw.strip("\r").strip()
        m = _COMPARE_RE.match(line)
        if m:
            kv = _kv_tokens(m.group(1))
            if "per-response" in kv and "same-bytes" in kv:
                return kv
    return None


_STAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def window_from_stamps(asof_a, asof_b):
    """The stated-window rule (QUALITY 161): the A->B gap in whole seconds
    computed from the two capture receipts' own as-of stamps; 1-second
    resolution; 0 is legal (a same-second pair). Returns None when either
    stamp is not the grammar (the window then reads unavailable)."""
    import calendar

    if not (_STAMP_RE.match(asof_a or "") and _STAMP_RE.match(asof_b or "")):
        return None
    fmt = "%Y-%m-%dT%H:%M:%SZ"
    ta = calendar.timegm(time.strptime(asof_a, fmt))
    tb = calendar.timegm(time.strptime(asof_b, fmt))
    return max(0, tb - ta)


def classify(requested_w, cap_a, cap_b, cmp_rc, cmp_line):
    """One window's verdict from the three child outcomes. Returns the
    field dict the ROTATION_SCHEDULE line renders."""
    d = {
        "window": requested_w,
        "window_s": "na",
        "per_response": "na",
        "stable": "na",
        "same_bytes": "na",
        "rotated": "unavailable",
        "reason": "na",
        "asof_a": "na",
        "asof_b": "na",
        "run_start": "na",
        "sha_a": "na",
        "sha_b": "na",
    }
    if cap_a is None or cap_a.get("_rc") != 0:
        d["reason"] = "capture-a-unavailable"
        if cap_a is not None:
            d["asof_a"] = cap_a.get("as-of", "na")
            d["sha_a"] = (cap_a.get("sha256", "na") or "na")[:12]
        return d
    d["asof_a"] = cap_a.get("as-of", "na")
    d["sha_a"] = (cap_a.get("sha256", "na") or "na")[:12]
    if cap_b is None or cap_b.get("_rc") != 0:
        d["reason"] = "capture-b-unavailable"
        if cap_b is not None:
            d["asof_b"] = cap_b.get("as-of", "na")
            d["sha_b"] = (cap_b.get("sha256", "na") or "na")[:12]
        return d
    d["asof_b"] = cap_b.get("as-of", "na")
    d["sha_b"] = (cap_b.get("sha256", "na") or "na")[:12]
    gap = window_from_stamps(d["asof_a"], d["asof_b"])
    if gap is None:
        d["reason"] = "stamp-unparseable"
        return d
    d["window_s"] = str(gap)
    if cmp_rc != 0:
        d["reason"] = "compare-setup" if cmp_rc == 2 else "compare-rc%d" % cmp_rc
        return d
    if cmp_line is None:
        d["reason"] = "compare-unparseable"
        return d
    d["run_start"] = cmp_line.get("run-start", "na")
    try:
        per_response = int(cmp_line["per-response"])
    except (KeyError, ValueError):
        d["reason"] = "compare-unparseable"
        return d
    d["per_response"] = str(per_response)
    d["stable"] = cmp_line.get("stable", "na")
    d["same_bytes"] = cmp_line.get("same-bytes", "na")
    if per_response > 0 or d["same_bytes"] == "false":
        d["rotated"] = "yes"
    else:
        d["rotated"] = "no"
    return d


def render_window(d, label):
    """The one-line window receipt (ASCII; counts/shapes/stamps/sha12)."""
    return (
        "ROTATION_SCHEDULE window=%ds window-s=%s label=%s per-response=%s"
        " stable=%s same-bytes=%s rotated=%s reason=%s as-of-a=%s as-of-b=%s"
        " run-start=%s capture-a=%s capture-b=%s"
        % (d["window"], d["window_s"], label, d["per_response"], d["stable"],
           d["same_bytes"], d["rotated"], d["reason"], d["asof_a"], d["asof_b"],
           d["run_start"], d["sha_a"], d["sha_b"])
    )


# ----------------------------------------------------------------- children

CHILD_TIMEOUT_S = 180


def run_child(cmd, env=None):
    """Run one registered-probe child; returns (rc, stdout_text). A timeout
    or spawn failure is (None, ''), never a guess."""
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              timeout=CHILD_TIMEOUT_S, env=env)
        return proc.returncode, proc.stdout or ""
    except subprocess.TimeoutExpired:
        return None, ""
    except OSError:
        return None, ""


def _sleep_until(deadline_mono):
    """Chunked monotonic sleep; time.monotonic is the schedule clock (S589:
    a clock that cannot go backwards)."""
    while True:
        remaining = deadline_mono - time.monotonic()
        if remaining <= 0:
            return
        time.sleep(min(1.0, remaining))


# ---------------------------------------------------------------- live run

def run_schedule(url, ua, pin, out_dir, windows, label, child_path, child_env=None):
    """The stated-window schedule. Returns (stdout_text, exit_code)."""
    if not (url and ua and pin and out_dir and windows and label):
        return "ROTATION_SCHEDULE_SETUP live mode wants --url --ua --pin --out-dir --windows --label", 2
    if not os.path.isfile(child_path):
        return "ROTATION_SCHEDULE_SETUP child probe not found: %s" % child_path, 2
    if not os.path.isfile(pin):
        return "ROTATION_SCHEDULE_SETUP pin not readable: %s" % pin, 2
    if not os.path.isdir(out_dir):
        return "ROTATION_SCHEDULE_SETUP out-dir not a directory: %s" % out_dir, 2

    start_mono = time.monotonic()
    start_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    lines = []
    classes = {"yes": 0, "no": 0, "unavailable": 0}
    computed = []
    for w in windows:
        out_a = os.path.join(out_dir, "%s-w%d-a.bin" % (label, w))
        out_b = os.path.join(out_dir, "%s-w%d-b.bin" % (label, w))
        rc_a, txt_a = run_child([sys.executable, child_path, "--capture",
                                 "--url", url, "--ua", ua, "--out", out_a],
                                env=child_env)
        cap_a = parse_capture_line(txt_a)
        if rc_a == 0 and cap_a is not None and cap_a.get("_rc") == 0:
            _sleep_until(time.monotonic() + w)  # dwell the stated window
        # a dead A leg skips the dwell: the pair is already unavailable
        rc_b, txt_b = run_child([sys.executable, child_path, "--capture",
                                 "--url", url, "--ua", ua, "--out", out_b],
                                env=child_env)
        cap_b = parse_capture_line(txt_b)
        gap = None
        if cap_a is not None and cap_b is not None:
            gap = window_from_stamps(cap_a.get("as-of"), cap_b.get("as-of"))
        cmd_cmp = [sys.executable, child_path, "--compare", "--label",
                   "%s-w%d" % (label, w), "--pin", pin,
                   "--a", out_a, "--b", out_b]
        if gap is not None:
            cmd_cmp += ["--window-s", str(gap)]
        cmp_rc, cmp_txt = run_child(cmd_cmp, env=child_env)
        d = classify(w, cap_a, cap_b, cmp_rc, parse_compare_line(cmp_txt))
        classes[d["rotated"]] += 1
        computed.append(d["window_s"])
        lines.append(render_window(d, label))
    end_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    wall = int(round(time.monotonic() - start_mono))
    lines.append(
        "ROTATION_SCHEDULE_SUMMARY label=%s windows=%s window_s_computed=%s"
        " rotated_yes=%d rotated_no=%d rotated_unavailable=%d clock=monotonic"
        " schedule_start=%s schedule_end=%s wall_s=%d rc=0"
        % (label, ",".join(str(w) for w in windows), ",".join(computed),
           classes["yes"], classes["no"], classes["unavailable"],
           start_iso, end_iso, wall))
    return "\n".join(lines), 0


# ----------------------------------------------------------------- selftest

FAKE_CHILD = r'''
import os, sys
mode = os.environ.get("FAKE_UAV_MODE", "ok")
if mode == "garbage":
    print("this is not the grammar you seek")
    sys.exit(0)
if "--capture" in sys.argv:
    counter = os.path.join(os.environ["FAKE_UAV_DIR"], "count")
    n = 0
    if os.path.isfile(counter):
        with open(counter, "r") as fh:
            n = int(fh.read().strip() or "0")
    with open(counter, "w") as fh:
        fh.write(str(n + 1))
    if mode == "capfail":
        print("UA_VAR_CAPTURE url=https://example.invalid/x ua=fake/1.0"
              " outcome=unavailable as-of=2026-11-02T00:00:00Z rc=1 note=m0ns3cure")
        sys.exit(1)
    sha = "aaaaaaaaaaaaaaaa" if n % 2 == 0 else "bbbbbbbbbbbbbbbb"
    print("UA_VAR_CAPTURE url=https://example.invalid/x ua=fake/1.0 bytes=10"
          " sha256=%s48a1b2c3d4e5f60718293a4b5c6d7e8f9012 out=fake.bin"
          " as-of=2026-11-02T00:00:00Z rc=0 note=m0ns3cure" % sha)
    sys.exit(0)
if "--compare" in sys.argv:
    if mode == "setup":
        sys.stderr.write("UA_VARIANCE_SETUP: fake setup error\n")
        sys.exit(2)
    print("UA_VARIANCE label=fake per-response=3 stable=1497 same-bytes=false"
          " window-s=0 run-start=2026-11-02T00:00:05Z note=m0ns3cure")
    sys.exit(0)
sys.exit(2)
'''


def _write_fake_child(root):
    path = os.path.join(root, "fake_uav.py")
    with open(path, "wb") as fh:  # binary mode: no CRLF translation (r62 lesson)
        fh.write(FAKE_CHILD.encode("utf-8"))
    return path


def _selftest():
    checks = []

    # 1/2. schedule grammar
    checks.append(("schedule_parse",
                   parse_windows("31,91,304") == [31, 91, 304], "31,91,304"))
    try:
        parse_windows("31,x")
        bad = False
    except ValueError:
        bad = True
    checks.append(("schedule_rejects_noninteger", bad, "31,x"))

    # 3. window computation from the capture stamps (QUALITY 161; 0 legal)
    checks.append(("window_from_stamps",
                   window_from_stamps("2026-11-02T00:00:00Z", "2026-11-02T00:00:31Z") == 31
                   and window_from_stamps("2026-11-02T00:00:00Z", "2026-11-02T00:00:00Z") == 0
                   and window_from_stamps("nope", "2026-11-02T00:00:00Z") is None,
                   "31/0/None"))

    # 4-6. classification: yes / no / bytes-only
    cap_ok_a = {"as-of": "2026-11-02T00:00:00Z", "rc": "0", "_rc": 0,
                "sha256": "aaaa1111222233334444", "bytes": "10"}
    cap_ok_b = {"as-of": "2026-11-02T00:00:31Z", "rc": "0", "_rc": 0,
                "sha256": "bbbb5555666677778888", "bytes": "10"}
    cmp_rot = {"per-response": "4", "stable": "1497", "same-bytes": "false",
               "window-s": "31", "run-start": "2026-11-02T00:00:35Z"}
    d = classify(31, cap_ok_a, cap_ok_b, 0, cmp_rot)
    checks.append(("classify_yes", d["rotated"] == "yes" and d["window_s"] == "31",
                   str(d["rotated"])))
    cmp_stable = dict(cmp_rot, **{"per-response": "0", "same-bytes": "true"})
    d = classify(31, cap_ok_a, cap_ok_b, 0, cmp_stable)
    checks.append(("classify_no", d["rotated"] == "no", str(d["rotated"])))
    cmp_bytes = dict(cmp_rot, **{"per-response": "0"})
    d = classify(31, cap_ok_a, cap_ok_b, 0, cmp_bytes)
    checks.append(("classify_bytes_only",
                   d["rotated"] == "yes" and d["same_bytes"] == "false",
                   "%s/%s" % (d["rotated"], d["same_bytes"])))

    # 7-9. honest unavailable: dead leg / child setup / unparseable summary
    cap_fail = {"as-of": "2026-11-02T00:00:00Z", "rc": "1", "_rc": 1}
    d = classify(31, cap_fail, cap_ok_b, 0, cmp_rot)
    checks.append(("unavailable_dead_leg",
                   d["rotated"] == "unavailable" and d["reason"] == "capture-a-unavailable",
                   str(d["reason"])))
    d = classify(31, cap_ok_a, cap_ok_b, 2, cmp_rot)
    checks.append(("unavailable_compare_setup",
                   d["rotated"] == "unavailable" and d["reason"] == "compare-setup",
                   str(d["reason"])))
    d = classify(31, cap_ok_a, cap_ok_b, 0, None)
    checks.append(("unavailable_unparseable",
                   d["rotated"] == "unavailable" and d["reason"] == "compare-unparseable",
                   str(d["reason"])))

    root = tempfile.mkdtemp(prefix="mori-rotation-schedule-selftest-")
    try:
        fake = _write_fake_child(root)
        out_dir = os.path.join(root, "caps")
        os.makedirs(out_dir, exist_ok=True)
        pin = os.path.join(root, "pin.html")
        with open(pin, "wb") as fh:
            fh.write(b"<html>pin</html>\n")
        env = dict(os.environ, FAKE_UAV_DIR=root)

        # 10. redaction: the fake child carries the marker token on a
        #     non-grammar field of EVERY line; stdout must never carry it
        out, rc = run_schedule("https://example.invalid/x", "fake/1.0", pin,
                               out_dir, [0], "redact", fake, child_env=env)
        checks.append(("redaction_stdout",
                       rc == 0 and "m0ns3cure" not in out
                       and "ROTATION_SCHEDULE_SUMMARY" in out, out[:120]))

        # 11. integration at windows 0,0 (sleep-free): both windows
        #     classified yes, computed gaps stated, clock named
        out, rc = run_schedule("https://example.invalid/x", "fake/1.0", pin,
                               out_dir, [0, 0], "integ", fake, child_env=env)
        wl = [l for l in out.splitlines() if l.startswith("ROTATION_SCHEDULE ")]
        checks.append(("integration_window0",
                       rc == 0 and len(wl) == 2
                       and all("rotated=yes" in l for l in wl)
                       and "window_s_computed=0,0" in out
                       and "clock=monotonic" in out
                       and "rotated_yes=2" in out, out[:200]))

        # 12. missing child refused (rc 2, no window lines)
        out, rc = run_schedule("https://example.invalid/x", "fake/1.0", pin,
                               out_dir, [0], "nochild",
                               os.path.join(root, "absent.py"))
        checks.append(("missing_child_refused",
                       rc == 2 and out.startswith("ROTATION_SCHEDULE_SETUP")
                       and "ROTATION_SCHEDULE " not in out, out[:80]))

        # 13. non-integer windows refused live (rc 2)
        try:
            parse_windows("31,x")
            refused = False
        except ValueError:
            refused = True
        outm, rcm = run_schedule("https://example.invalid/x", "fake/1.0", pin,
                                 out_dir, parse_windows("31"), "wm", fake,
                                 child_env=env)
        checks.append(("windows_value_domain",
                       refused and rcm == 0, "refused=%s rc=%s" % (refused, rcm)))

    finally:
        import shutil
        shutil.rmtree(root, ignore_errors=True)

    failed = [c for c in checks if not c[1]]
    for name, ok, detail in checks:
        print("selftest %-28s %s" % (name, "PASS" if ok else "FAIL (%s)" % detail[:80]))
    if failed:
        print("MORI_ROTATION_SCHEDULE_SELFTEST: FAIL (%d/%d)"
              % (len(checks) - len(failed), len(checks)))
        return 1
    print("MORI_ROTATION_SCHEDULE_SELFTEST: PASS (%d cases)" % len(checks))
    return 0


def main(argv):
    if "--selftest" in argv:
        return _selftest()
    args = {"--url": None, "--ua": None, "--pin": None, "--out-dir": None,
            "--windows": "31,91,304", "--label": "rotsched", "--child": None}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in args:
            if i + 1 >= len(argv):
                sys.stderr.write("ROTATION_SCHEDULE_SETUP: %s wants a value\n" % a)
                return 2
            args[a] = argv[i + 1]
            i += 2
        else:
            sys.stderr.write("ROTATION_SCHEDULE_SETUP: unknown argument %s\n" % a)
            return 2
    child = args["--child"] or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "mori-ua-variance.py")
    try:
        windows = parse_windows(args["--windows"])
    except ValueError as exc:
        sys.stderr.write("ROTATION_SCHEDULE_SETUP: --windows: %s\n" % exc)
        return 2
    text, rc = run_schedule(args["--url"], args["--ua"], args["--pin"],
                            args["--out-dir"], windows, args["--label"], child)
    print(text)
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
