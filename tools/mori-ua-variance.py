#!/usr/bin/env python3
"""mori-ua-variance.py — separate PER-RESPONSE tokens from STABLE chrome on a bot-
managed page's instrument-UA body, by same-UA A/A fetches (round 68; the r67
SCORECARD planned item: "the bot-manager chrome is disclosed serving variance but
the instrument-UA body of a bot-managed page is otherwise unadjudicated — a future
round could receipt per-response token variance (two instrument-UA fetches minutes
apart) to separate per-response tokens from stable chrome"). Round 69 adds the
observation-window grammar (below) and the standing re-check cross-check arm.

Usage:
  python tools/mori-ua-variance.py --capture --url URL --ua UA --out FILE
  python tools/mori-ua-variance.py --compare --label ID --pin FILE --a FILE --b FILE
          [--window-s N] [--recheck-summary FILE]
  python tools/mori-ua-variance.py --selftest

Modes:
  --capture  one GET fetch of URL under UA; the raw body is written to FILE
             (capture bodies are WORKING-TREE-ONLY evidence: a capture can embed a
             per-response token value, so bodies stay in scratch and are never
             committed — counts and shapes only, the lane redaction rule); one
             summary line is printed: UA_VAR_CAPTURE ... bytes= sha256= as-of=...
             rc 0 body captured; rc 1 fetch failed (non-2xx, timeout, empty body);
             rc 2 setup error.
  --compare  line-level classification of two same-UA captures (A, B) against the
             pinning-UA body (pin):
               per-response      line positions where A and B DIFFER (counted in
                                 the same `<`+`>` convention as the r67 pin-vs-
                                 live diff: one changed line counts 2). Two
                                 fetches of the same URL under the same UA minutes
                                 apart cannot differ in page CONTENT — a differing
                                 line is serving-generated, not page identity.
               stable            line positions where A and B agree.
               stable-not-in-pin stable lines absent from the pinning body —
                                 UA-conditional serving OR a newer vendor build;
                                 this tool does NOT decide which (QUALITY 159:
                                 no grammar is taught here, no vendor scoping is
                                 crossed — build churn stays the re-check's job).
               stable-in-pin     stable lines the pinning body also carries.
             Output is COUNTS AND SHAPES ONLY: line values are never emitted, so
             the receipt is committable even when a token value exists. Summary
             line: UA_VARIANCE label= ... per-response= stable= stable-not-in-pin=
             stable-in-pin= lines-a= lines-b= lines-pin= same-bytes= sha-a= sha-b=
             sha-pin= window-s=<N|unavailable reason=not-stated> crosscheck=<...>
             run-start=...
             rc 0 compared; rc 2 setup error (missing/unreadable input, a
             --window-s that is not a non-negative integer, or a provided
             --recheck-summary that is not a re-check summary).

Observation-window dependency (r69 — the r68 closure carry-in): the A/A
separation is WINDOW-CONDITIONAL. The motivating observation, recorded by the
r68 non-author closure: a ~15-minute window in the closure's re-derivation
caught no per-response rotation, while the r68 round's 21-minute A/A window
caught per-response=4 — two windows, different catches, same page. Every
compare receipt therefore STATES its window: pass --window-s N, the A->B gap in
seconds computed by the caller from the two UA_VAR_CAPTURE receipts' own
`as-of=` values (1-second resolution; 0 is legal when both stamps land in the
same second). Omitted, the summary carries
`window-s=unavailable reason=not-stated` — never a fabricated gap — and per
QUALITY 161 a receipt whose window is unstated does not constrain any
rotation-timing claim. The window is METADATA, never a TTL measurement: this
tool reports counts and shapes only and decides no rotation clock (see S580:
token content carries the timestamps of the client's latest challenge
responses, so token-bearing bytes are bound to token-lifetime machinery with
its own clocks — clocks this tool does not read).

Standing re-check cross-check arm (r69; the r68 SCORECARD planned item):
pass --recheck-summary FILE holding the standing step's MORI_DRIFT_RECHECK
summary line (tools/mori-drift-recheck.py output) from the same round's paired
run. The arm compares two COUNTS and nothing else: if the compare saw
stable-not-in-pin>0 while the re-check saw asset-churn=0 (or the reverse), the
line reads `crosscheck=inconsistent reason=<which side>` — a review LEAD only.
Agreement reads `crosscheck=consistent` with
`crosscheck-basis=stable-not-in-pin=<n>+recheck-asset-churn=<n>`. Omitted, the
line reads `crosscheck=unavailable reason=not-provided` — never assumed. The
arm decides nothing: it re-classes no SOURCES row, teaches no grammar, and
never resolves UA-conditional vs newer-build (the two arms run different UAs
at possibly different moments; the receipt states both runs' own timestamps).

What this tool does NOT do: it re-classifies no SOURCES row, teaches no churn
grammar, and never generalizes one vendor's bytes to another (the standing step
`tools/mori-drift-recheck.py` owns row classes; this tool only receipts variance).
Read-only on the network; the selftest serves fixtures on 127.0.0.1 only.
"""
import difflib
import hashlib
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

FETCH_TIMEOUT_S = 60
FETCH_TRIES = 3
RETRY_BACKOFF_S = 1.0
MAX_BODY = 8 * 1024 * 1024
WINDOW_S_RE = re.compile(r"^[0-9]+$")
RECHECK_LINE_RE = re.compile(r"^MORI_DRIFT_RECHECK\b")
ASSET_CHURN_RE = re.compile(r"(?<![\w-])asset-churn=(\d+)")


def now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()


def fetch(url, ua):
    """One URL, up to FETCH_TRIES GETs. Returns (outcome, body) with outcome in
    {body, unavailable}.

    Retries (the frozen sweep's transport discipline, tools/mori-source-drift.py
    fetch()): connection errors and 5xx retry with a short fixed backoff; 4xx
    answers are final (no retry). The retry exists because this host's loopback
    intermittently resets the first request (WinError 10054 observed in the r68
    selftest) — a one-shot fetcher grades a flaky transport `unavailable`."""
    for attempt in range(FETCH_TRIES):
        req = urllib.request.Request(url, headers={"User-Agent": ua}, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT_S) as resp:
                status = resp.getcode()
                body = resp.read(MAX_BODY + 1)
        except urllib.error.HTTPError as exc:
            code = exc.code
            try:
                exc.close()
            except Exception:
                pass
            if 500 <= code < 600 and attempt < FETCH_TRIES - 1:
                time.sleep(RETRY_BACKOFF_S)
                continue
            return "unavailable", b""
        except Exception:
            if attempt < FETCH_TRIES - 1:
                time.sleep(RETRY_BACKOFF_S)
                continue
            return "unavailable", b""
        if status is None or not 200 <= status < 300 or not body:
            return "unavailable", b""
        if len(body) > MAX_BODY:
            return "unavailable", b""
        return "body", body
    return "unavailable", b""


def capture(url, ua, out_path):
    if not url or not ua or not out_path:
        sys.stderr.write("UA_VARIANCE_SETUP: --capture wants --url, --ua and --out\n")
        return 2
    outcome, body = fetch(url, ua)
    as_of = now_utc()
    if outcome != "body":
        print("UA_VAR_CAPTURE url=%s ua=%s outcome=unavailable as-of=%s rc=1" %
              (url, ua, as_of))
        return 1
    with open(out_path, "wb") as fh:
        fh.write(body)
    print("UA_VAR_CAPTURE url=%s ua=%s bytes=%d sha256=%s out=%s as-of=%s rc=0" %
          (url, ua, len(body), sha256_hex(body), out_path, as_of))
    return 0


def parse_recheck_summary(path):
    """Read a provided --recheck-summary file. Returns (asset_churn, None) on a
    parsed MORI_DRIFT_RECHECK summary line, or (None, reason) when the file is
    unreadable or carries no re-check summary (caller turns that into rc 2)."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError as exc:
        return None, "unreadable: %s" % exc
    for line in text.splitlines():
        if RECHECK_LINE_RE.match(line):
            m = ASSET_CHURN_RE.search(line)
            if m is None:
                return None, "recheck-summary-has-no-asset-churn-token"
            return int(m.group(1)), None
    return None, "no-mori-drift-recheck-line"


def crosscheck_verdict(stable_not_in_pin, asset_churn):
    """The standing consistency predicate over two counts. Decides nothing: the
    verdict is a review lead, never a row class and never a failure."""
    if stable_not_in_pin > 0 and asset_churn == 0:
        return "inconsistent reason=stable-not-in-pin-without-asset-churn"
    if stable_not_in_pin == 0 and asset_churn > 0:
        return "inconsistent reason=asset-churn-without-stable-not-in-pin"
    return "consistent"


def compare(label, pin_path, a_path, b_path, window_s=None, recheck_path=None):
    paths = {"pin": pin_path, "a": a_path, "b": b_path}
    bodies = {}
    for name in ("pin", "a", "b"):
        try:
            with open(paths[name], "rb") as fh:
                bodies[name] = fh.read()
        except OSError as exc:
            sys.stderr.write("UA_VARIANCE_SETUP: --%s %s unreadable: %s\n" %
                             (name, paths[name], exc))
            return 2
    if window_s is not None and not WINDOW_S_RE.match(window_s):
        sys.stderr.write("UA_VARIANCE_SETUP: --window-s wants a non-negative "
                         "integer (the A->B gap in seconds, from the capture "
                         "receipts' as-of values)\n")
        return 2
    window_field = "window-s=%s" % window_s if window_s is not None \
        else "window-s=unavailable reason=not-stated"
    if recheck_path is not None:
        asset_churn, reason = parse_recheck_summary(recheck_path)
        if asset_churn is None:
            sys.stderr.write("UA_VARIANCE_SETUP: --recheck-summary %s: %s\n" %
                             (recheck_path, reason))
            return 2
    lines_a = bodies["a"].splitlines()
    lines_b = bodies["b"].splitlines()
    lines_pin = bodies["pin"].splitlines()
    pin_set = set(lines_pin)
    matcher = difflib.SequenceMatcher(a=lines_a, b=lines_b, autojunk=False)
    per_response = 0
    stable = 0
    stable_not_in_pin = 0
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            stable += i2 - i1
            stable_not_in_pin += sum(1 for ln in lines_a[i1:i2] if ln not in pin_set)
        else:
            per_response += (i2 - i1) + (j2 - j1)
    stable_in_pin = stable - stable_not_in_pin
    if recheck_path is not None:
        verdict = crosscheck_verdict(stable_not_in_pin, asset_churn)
        crosscheck_field = ("crosscheck=%s crosscheck-basis=stable-not-in-pin=%d"
                            "+recheck-asset-churn=%d"
                            % (verdict, stable_not_in_pin, asset_churn))
    else:
        crosscheck_field = "crosscheck=unavailable reason=not-provided"
    print("UA_VARIANCE label=%s per-response=%d stable=%d stable-not-in-pin=%d "
          "stable-in-pin=%d lines-a=%d lines-b=%d lines-pin=%d same-bytes=%s "
          "sha-a=%s sha-b=%s sha-pin=%s %s %s run-start=%s"
          % (label, per_response, stable, stable_not_in_pin, stable_in_pin,
             len(lines_a), len(lines_b), len(lines_pin),
             str(bodies["a"] == bodies["b"]).lower(),
             sha256_hex(bodies["a"]), sha256_hex(bodies["b"]),
             sha256_hex(bodies["pin"]), window_field, crosscheck_field,
             now_utc()))
    return 0


# --------------------------------------------------------------------- selftest

def _selftest():
    import http.server
    import shutil
    import tempfile
    import threading

    checks = []
    nonce_counter = {"n": 0}
    NONCE = b"SECRETNONCE7f3a9c"
    pin_lines = [b"<html>teaching page stands still",
                 b"chrome: STABLE-CHROME-LINE-1",
                 b"footer line"]
    botmgr_line = b"botmgr: script src=/static/botmgr/chrome.js"
    token_line_a = b"TOKEN:" + NONCE
    token_line_b = b"TOKEN:" + b"SECRETNONCEd81b40e"
    pin_body = b"\n".join(pin_lines) + b"\n"
    body_instrument_a = b"\n".join(
        pin_lines[:2] + [botmgr_line, token_line_a, pin_lines[2]]) + b"\n"
    body_instrument_b = b"\n".join(
        pin_lines[:2] + [botmgr_line, token_line_b, pin_lines[2]]) + b"\n"
    body_static = pin_body + b"stable extra chrome\n"

    class Handler(http.server.BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *args):
            pass

        def do_GET(self):
            if self.path == "/variance":
                nonce_counter["n"] += 1
                body = body_instrument_a if nonce_counter["n"] % 2 else body_instrument_b
                status = 200
            elif self.path == "/static":
                body = body_static
                status = 200
            else:
                body = b"gone\n"
                status = 404
            self.send_response(status)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    port = srv.server_address[1]
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    root = tempfile.mkdtemp(prefix="mori-ua-variance-selftest-")
    from io import StringIO
    sys_stdout, sys_stderr = sys.stdout, sys.stderr
    try:
        UA = "mori-ua-variance-selftest/1.0"
        base = "http://127.0.0.1:%d" % port

        def cap(path, out):
            sys.stdout, sys.stderr = StringIO(), StringIO()
            try:
                rc = capture(base + path, UA, os.path.join(root, out))
            finally:
                sys.stdout, sys.stderr = sys_stdout, sys_stderr
            return rc

        def cmp_capture(text_buf, *args, **kw):
            sys.stdout, sys.stderr = text_buf, StringIO()
            try:
                rc = compare(*args, **kw)
            finally:
                sys.stdout, sys.stderr = sys_stdout, sys_stderr
            return rc

        pin_file = os.path.join(root, "pin.bin")
        with open(pin_file, "wb") as fh:
            fh.write(pin_body)
        # re-check summary fixtures for the cross-check arm (grammar of
        # tools/mori-drift-recheck.py's summary line; counts only)
        rc_consistent = os.path.join(root, "recheck-churn2.txt")
        with open(rc_consistent, "w", encoding="ascii") as fh:
            fh.write("MORI_DRIFT_RECHECK rows=1 adjudicated=1 fresh=0 excerpt=0 "
                     "time-churn=0 asset-churn=2 receipt-open=0 receipt-stale=0 "
                     "ua-serving=1 content-drift=0 gate=0\n")
        rc_nochurn = os.path.join(root, "recheck-nochurn.txt")
        with open(rc_nochurn, "w", encoding="ascii") as fh:
            fh.write("MORI_DRIFT_RECHECK rows=1 adjudicated=1 fresh=1 excerpt=0 "
                     "time-churn=0 asset-churn=0 receipt-open=0 receipt-stale=0 "
                     "ua-serving=1 content-drift=0 gate=0\n")
        rc_churn3 = os.path.join(root, "recheck-churn3.txt")
        with open(rc_churn3, "w", encoding="ascii") as fh:
            fh.write("MORI_DRIFT_RECHECK rows=2 adjudicated=2 fresh=0 excerpt=0 "
                     "time-churn=0 asset-churn=3 receipt-open=0 receipt-stale=0 "
                     "ua-serving=2 content-drift=0 gate=0\n")
        rc_notasummary = os.path.join(root, "not-a-summary.txt")
        with open(rc_notasummary, "w", encoding="ascii") as fh:
            fh.write("hello world, no recheck line here\n")

        # case 1: two captures minutes-apart semantics are the caller's; here the
        # server hands a fresh nonce per request, so A and B differ only there
        rc_a = cap("/variance", "a.bin")
        rc_b = cap("/variance", "b.bin")
        buf = StringIO()
        rc_cmp = cmp_capture(buf, "S-fix", pin_file, os.path.join(root, "a.bin"),
                             os.path.join(root, "b.bin"))
        text = buf.getvalue()
        m = re.search(r"per-response=(\d+) stable=(\d+) stable-not-in-pin=(\d+) "
                      r"stable-in-pin=(\d+) lines-a=(\d+) lines-b=(\d+) "
                      r"lines-pin=(\d+)", text)
        checks.append(("separates_per_response_from_stable",
                       rc_a == 0 and rc_b == 0 and rc_cmp == 0 and m is not None
                       and m.groups() == ("2", "4", "1", "3", "5", "5", "3"),
                       "rc=%d,%d,%d counts=%s" % (rc_a, rc_b, rc_cmp,
                                                  m.groups() if m else None)))
        checks.append(("token_value_never_emitted",
                       NONCE.decode("ascii", "replace") not in text
                       and "SECRETNONCE" not in text and "botmgr:" not in text,
                       "compare output carries counts only, no line values"))
        checks.append(("summary_line_shape",
                       re.search(r"^UA_VARIANCE label=S-fix .*run-start=\d{4}-"
                                 r"\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", text, re.M)
                       is not None,
                       "label + counts + run-start on one line"))

        # case 2: identical bodies -> per-response=0
        rc_s1 = cap("/static", "s1.bin")
        rc_s2 = cap("/static", "s2.bin")
        buf2 = StringIO()
        cmp_capture(buf2, "S-static", pin_file, os.path.join(root, "s1.bin"),
                    os.path.join(root, "s2.bin"))
        text2 = buf2.getvalue()
        m2 = re.search(r"per-response=(\d+) .*same-bytes=(\w+)", text2)
        checks.append(("identical_bodies_zero_per_response",
                       rc_s1 == 0 and rc_s2 == 0 and m2 is not None
                       and m2.group(1) == "0" and m2.group(2) == "true",
                       "per-response=%s same-bytes=%s"
                       % (m2.groups() if m2 else None)))

        # case 3: capture failure -> rc 1, no bytes written
        rc_404 = cap("/gone", "gone.bin")
        checks.append(("capture_failure_rc1_no_body",
                       rc_404 == 1
                       and not os.path.exists(os.path.join(root, "gone.bin")),
                       "rc=%d out-written=%s" % (
                           rc_404,
                           os.path.exists(os.path.join(root, "gone.bin")))))

        # case 4: compare with a missing input -> rc 2
        buf3 = StringIO()
        sys.stdout, sys.stderr = buf3, StringIO()
        try:
            rc_miss = compare("S-miss", os.path.join(root, "nope.bin"),
                              os.path.join(root, "a.bin"),
                              os.path.join(root, "b.bin"))
        except SystemExit:
            rc_miss = -1
        finally:
            sys.stdout, sys.stderr = sys_stdout, sys_stderr
        checks.append(("missing_input_exit2", rc_miss == 2, "rc=%d" % rc_miss))

        # case 5 (r69): a stated window lands in the summary line; an unstated
        # window is marked unavailable, never fabricated
        buf_w = StringIO()
        rc_w = cmp_capture(buf_w, "S-fix", pin_file,
                           os.path.join(root, "a.bin"),
                           os.path.join(root, "b.bin"), window_s="1260")
        text_w = buf_w.getvalue()
        mw = re.search(r"window-s=(\d+)", text_w)
        checks.append(("window_stated_when_given",
                       rc_w == 0 and mw is not None and mw.group(1) == "1260",
                       "rc=%d window-s=%s" % (rc_w, mw.group(1) if mw else None)))
        buf_u = StringIO()
        rc_u = cmp_capture(buf_u, "S-fix", pin_file,
                           os.path.join(root, "a.bin"),
                           os.path.join(root, "b.bin"))
        text_u = buf_u.getvalue()
        checks.append(("window_unstated_marked_unavailable",
                       rc_u == 0
                       and "window-s=unavailable reason=not-stated" in text_u,
                       "rc=%d unstated-window field present=%s"
                       % (rc_u, "window-s=unavailable reason=not-stated" in text_u)))
        buf_badw = StringIO()
        rc_badw = cmp_capture(buf_badw, "S-fix", pin_file,
                              os.path.join(root, "a.bin"),
                              os.path.join(root, "b.bin"), window_s="abc")
        checks.append(("window_rejects_non_integer",
                       rc_badw == 2 and buf_badw.getvalue() == "",
                       "rc=%d stdout-empty=%s" % (rc_badw,
                                                  buf_badw.getvalue() == "")))

        # case 6 (r69): the cross-check arm — agreement, disagreement as a lead
        # (rc stays 0), the omitted arm unavailable, and a non-summary input rc 2
        buf_c = StringIO()
        rc_c = cmp_capture(buf_c, "S-fix", pin_file,
                           os.path.join(root, "a.bin"),
                           os.path.join(root, "b.bin"),
                           recheck_path=rc_consistent)
        text_c = buf_c.getvalue()
        # fixture-derived expectation: A/B stable-not-in-pin=1 (the botmgr line),
        # recheck fixture says asset-churn=2 -> consistent
        checks.append(("crosscheck_consistent",
                       rc_c == 0
                       and "crosscheck=consistent" in text_c
                       and "crosscheck-basis=stable-not-in-pin=1"
                           "+recheck-asset-churn=2" in text_c,
                       "rc=%d consistent-with-basis=%s"
                       % (rc_c, "crosscheck=consistent" in text_c)))
        buf_i = StringIO()
        rc_i = cmp_capture(buf_i, "S-fix", pin_file,
                           os.path.join(root, "a.bin"),
                           os.path.join(root, "b.bin"),
                           recheck_path=rc_nochurn)
        text_i = buf_i.getvalue()
        checks.append(("crosscheck_inconsistent_is_lead_not_failure",
                       rc_i == 0 and "crosscheck=inconsistent reason="
                                     "stable-not-in-pin-without-asset-churn"
                                     in text_i,
                       "rc=%d (a disagreement is a reported lead, never rc 1)"
                       % rc_i))
        buf_r = StringIO()
        rc_r = cmp_capture(buf_r, "S-revpin", pin_file, pin_file, pin_file,
                           recheck_path=rc_churn3)
        text_r = buf_r.getvalue()
        # pin vs pin: stable-not-in-pin=0 while the recheck fixture says
        # asset-churn=3 -> the reverse disagreement
        checks.append(("crosscheck_reverse_disagreement",
                       rc_r == 0 and "crosscheck=inconsistent reason="
                                     "asset-churn-without-stable-not-in-pin"
                                     in text_r,
                       "rc=%d reverse-lead=%s"
                       % (rc_r, "asset-churn-without-stable-not-in-pin"
                                in text_r)))
        buf_n = StringIO()
        rc_n = cmp_capture(buf_n, "S-fix", pin_file,
                           os.path.join(root, "a.bin"),
                           os.path.join(root, "b.bin"))
        text_n = buf_n.getvalue()
        checks.append(("crosscheck_absent_unavailable",
                       rc_n == 0
                       and "crosscheck=unavailable reason=not-provided" in text_n,
                       "rc=%d absent-arm marked unavailable=%s"
                       % (rc_n, "crosscheck=unavailable reason=not-provided"
                                in text_n)))
        buf_b = StringIO()
        rc_b2 = cmp_capture(buf_b, "S-fix", pin_file,
                            os.path.join(root, "a.bin"),
                            os.path.join(root, "b.bin"),
                            recheck_path=rc_notasummary)
        checks.append(("crosscheck_nonsummary_input_exit2",
                       rc_b2 == 2 and buf_b.getvalue() == "",
                       "rc=%d (a provided file that is not a re-check summary "
                       "is a setup error, matching --from-sweep strictness)"
                       % rc_b2))
    finally:
        srv.shutdown()
        srv.server_close()
        shutil.rmtree(root, ignore_errors=True)

    failed = [c for c in checks if not c[1]]
    for name, ok, detail in checks:
        print("selftest %-42s %s (%s)" % (name, "PASS" if ok else "FAIL", detail))
    if failed:
        print("MORI_UA_VARIANCE_SELFTEST: FAIL (%d/%d)"
              % (len(checks) - len(failed), len(checks)))
        return 1
    print("MORI_UA_VARIANCE_SELFTEST: PASS (%d cases)" % len(checks))
    return 0


def main(argv):
    args = list(argv)
    if args == ["--selftest"]:
        return _selftest()
    mode = None
    url = ua = out = label = None
    pin = a = b = window_s = recheck_path = None
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--capture":
            mode = "capture"
            i += 1
        elif arg == "--compare":
            mode = "compare"
            i += 1
        elif arg in ("--url", "--ua", "--out", "--label", "--pin", "--a", "--b",
                     "--window-s", "--recheck-summary"):
            if i + 1 >= len(args):
                sys.stderr.write("UA_VARIANCE_SETUP: %s wants a value\n" % arg)
                return 2
            val = args[i + 1]
            if arg == "--url":
                url = val
            elif arg == "--ua":
                ua = val
            elif arg == "--out":
                out = val
            elif arg == "--label":
                label = val
            elif arg == "--pin":
                pin = val
            elif arg == "--a":
                a = val
            elif arg == "--b":
                b = val
            elif arg == "--window-s":
                window_s = val
            else:
                recheck_path = val
            i += 2
        else:
            sys.stderr.write("usage: %s --capture --url URL --ua UA --out FILE | "
                             "--compare --label ID --pin FILE --a FILE --b FILE "
                             "[--window-s N] [--recheck-summary FILE] | "
                             "--selftest\n"
                             % os.path.basename(args[0] if args else __file__))
            return 2
    if mode == "capture":
        return capture(url, ua, out)
    if mode == "compare":
        if label is None:
            sys.stderr.write("UA_VARIANCE_SETUP: --compare wants --label\n")
            return 2
        return compare(label, pin, a, b, window_s=window_s,
                       recheck_path=recheck_path)
    sys.stderr.write("usage: %s --capture ... | --compare ... | --selftest\n"
                     % os.path.basename(args[0] if args else __file__))
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
