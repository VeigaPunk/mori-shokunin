#!/usr/bin/env python3
"""mori-drift-recheck.py — the standing adjudicate RE-CHECK: every verdict carries the
moment it was measured, and vendor page-stamp churn no longer masquerades as content
drift (round 66 capability).

Usage:
  python tools/mori-drift-recheck.py --root DIR [--only S###,S###] [--second-ua UA]
  python tools/mori-drift-recheck.py --selftest

Problem this closes (r65 verifier spotcheck routed note 3): hourly-regenerated vendor
template pages (the docs.python.org class) re-drift within hours of a re-pin — the
page-generation stamp line ("Last updated on Nov 01, 2026 (05:22 UTC).") changes on
every rebuild while the teaching content stands still. The r65 instruments record no
fetch-time, so a same-day re-run re-classified 8 of the 14 re-pins `content-drift`
(`adjudicate-baseline-r66.txt`) with nothing in the output binding each verdict to the
snapshot it was derived from: the class certified the day, not the moment.

What this tool does per considered row: takes a FRESH fetch at re-check time (never
reuses an earlier run's bytes), records that fetch's completion moment as `as-of=...Z`
on the row's own line, and re-derives the class against the same-time snapshot:

  pass-through fresh as-of=T   the fresh body at T equals the newest committed copy
  pass-through excerpt as-of=T the copy is an excerpt of the fresh body at T
  receipt-open as-of=T         the copy is an excerpt receipt whose header sha256
                               equals the fresh body's sha256 at T (source unchanged)
  receipt-stale as-of=T        receipt-shaped copy whose header sha256 does not match
                               the fresh body at T
  time-churn as-of=T           fresh body differs from the copy at T, but the diff is
                               confined to page-generation stamp lines (regex below) —
                               teaching content stands still; the copy certifies its
                               own moment, the fetch certifies T
  ua-serving as-of=T           tool-UA body differs beyond stamp lines but the second
                               (pinning) UA body equals the copy byte-identical
  content-drift as-of=T        fresh bodies differ from the copy beyond stamp lines
                               under both UAs — content changed, not the template
  gate as-of=T                 2xx response with an empty body
  unavailable as-of=T          the fetch failed (connection error, timeout, non-2xx,
                               over-cap)
  <id> no-copy                 no URL or no newest committed copy — nothing fetched,
                               so no moment exists to record (honest absence)

Stamp-line grammar (the only normalization applied, disclosed on the header line):
a line consisting solely of
  Last updated on <Mon DD, YYYY> (<HH:MM UTC>).
optionally indented, with an optional trailing period — the Sphinx
`html_last_updated_fmt` render the python docs templates write at every build.
Both sides (copy and fresh body) are reduced to their non-stamp line sequences for the
`time-churn` comparison only; every other class is decided on raw bytes.

Summary line:
  MORI_DRIFT_RECHECK rows=N adjudicated=D fresh=F excerpt=E time-churn=C \
receipt-open=O receipt-stale=S ua-serving=U content-drift=D gate=G unavailable=X \
window=<earliest as-of>..<latest as-of>
(rows = lines printed; adjudicated = copy-bearing resolutions; window bounds the as-of
stamps of every fetch this run took — a row is never compared across runs, so the whole
run's classes are same-time re-derivations bounded by the window; `-` when nothing was
fetched)
Exit 0 when every considered copy-bearing row carries a token, 1 when any is
unresolved, 2 on a setup error (missing upstream tool, missing or unreadable
SOURCES.md, bad usage). Read-only under DIR; the selftest serves fixtures on 127.0.0.1
only.

Shared policy: row/URL grammar, copy discovery, fetch cap, redirect policy, retry
behavior and the instrument UA are imported via the round-65 adjudicator
(tools/mori-drift-adjudicate.py), which imports the frozen sweep
(tools/mori-source-drift.py) — the re-check stands after that sweep, so it reuses the
same implementation chain rather than duplicating it; no frozen byte is edited (the
SKILL:905 `PASS (6 cases)` tally pin stays true). Receipt handling mirrors the
adjudicator's precedence (receipt-shaped copies classify receipt-open/receipt-stale
and are not stamp-normalized — an excerpt receipt quotes lines, it does not carry the
page template). The second (pinning) UA is disclosed on the header line, as in the
adjudicator.

Convention this tool enforces procedurally (QUALITY 158): a re-pin of an
hourly-regenerated vendor template page certifies a MOMENT, not the day — consumers
read `as-of=` beside every class, and `time-churn` marks stamp-only deltas instead of
re-classifying them content drift.
"""

import hashlib
import importlib.util
import os
import re
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ADJUDICATE_FILENAME = "mori-drift-adjudicate.py"
SECOND_UA_DEFAULT = "curl/8.21.0"
ONLY_ID_RE = re.compile(r"^S\d{3}$")

# docs.python.org page-generation stamp (Sphinx html_last_updated_fmt render),
# as pinned at corpus/evidence/sources-r65/S347.html:3328:
# "      Last updated on Nov 01, 2026 (05:22 UTC)."
STAMP_RE = re.compile(
    rb"^[ \t]*Last updated on [A-Z][a-z]{2} [0-9]{2}, [0-9]{4} "
    rb"\([0-9]{2}:[0-9]{2} UTC\)\.[ \t]*$")

STAMP_CLASS_NAME = "python-docs-page-stamp"

TOKENS = ("fresh", "excerpt", "time-churn", "receipt-open", "receipt-stale",
          "ua-serving", "content-drift", "gate", "unavailable")


def load_adjudicator():
    """Import the r65 adjudicator module from this tool's directory (None when absent)."""
    path = os.path.join(HERE, ADJUDICATE_FILENAME)
    if not os.path.isfile(path):
        return None
    spec = importlib.util.spec_from_file_location("mori_drift_adjudicate", path)
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def stamp_free(body):
    """The body's non-stamp line sequence (bytes)."""
    return [ln for ln in body.splitlines() if not STAMP_RE.match(ln)]


def now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run(root, only=None, second_ua=SECOND_UA_DEFAULT, out=None, _now=now_utc):
    adj = load_adjudicator()
    if adj is None:
        sys.stderr.write("MORI_DRIFT_RECHECK_SETUP: %s missing beside this tool\n"
                         % ADJUDICATE_FILENAME)
        return 2
    mod = adj.load_sweep()
    if mod is None:
        sys.stderr.write("MORI_DRIFT_RECHECK_SETUP: %s missing beside this tool "
                         "(imported via %s)\n"
                         % (adj.SWEEP_FILENAME, ADJUDICATE_FILENAME))
        return 2
    sources = os.path.join(root, "corpus", "SOURCES.md")
    try:
        with open(sources, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError:
        sys.stderr.write("MORI_DRIFT_RECHECK_SETUP: corpus/SOURCES.md missing or "
                         "unreadable\n")
        return 2
    emit = out.write if out is not None else sys.stdout.write
    emit("# MORI_DRIFT_RECHECK second_ua=%s only=%s run-start=%s stamp-class=%s\n"
         % (second_ua, "all" if only is None else ",".join(sorted(only)),
            _now(), STAMP_CLASS_NAME))
    counts = {t: 0 for t in TOKENS}
    unresolved = 0
    rows_printed = 0
    moments = []
    for sid, url in mod.parse_registry(text):
        if only is not None and sid not in only:
            continue
        copy_path = mod.find_copy(root, sid) if url is not None else None
        if url is None or copy_path is None:
            emit("%s no-copy\n" % sid)
            rows_printed += 1
            continue
        try:
            with open(copy_path, "rb") as fh:
                copy = fh.read()
        except OSError:
            emit("%s no-copy\n" % sid)
            rows_printed += 1
            continue
        rows_printed += 1
        token = None

        # one fresh fetch, stamped with its completion moment (the snapshot's T)
        outcome_t, body_t = mod.fetch(url)
        as_of = _now()
        moments.append(as_of)
        if outcome_t != "body":
            token = "unavailable"
        elif adj.is_receipt(copy):
            h = adj.header_sha(copy)
            if h is not None and h == hashlib_sha(body_t):
                token = "receipt-open"
            elif h is None:
                token = None  # receipt-shaped but no parsable opening sha
            else:
                token = "receipt-stale"
        elif (hashlib_sha(body_t) == hashlib_sha(copy)):
            token = "fresh"
        elif copy.strip() and copy.strip() in body_t:
            token = "excerpt"
        elif stamp_free(copy) == stamp_free(body_t):
            token = "time-churn"
        else:
            outcome_c, body_c = adj.fetch_with(mod, url, second_ua)
            if outcome_c != "body":
                token = "unavailable"
            elif len(body_c) == 0:
                token = "gate"
            elif hashlib_sha(body_c) == hashlib_sha(copy):
                token = "ua-serving"
            else:
                token = "content-drift"
        if token is None:
            unresolved += 1
            emit("%s unresolved as-of=%s\n" % (sid, as_of))
        else:
            emit("%s %s as-of=%s\n" % (sid, token, as_of))
            counts[token] += 1
    adjudicated = sum(counts[t] for t in TOKENS)
    window = "%s..%s" % (min(moments), max(moments)) if moments else "-"
    emit("MORI_DRIFT_RECHECK rows=%d adjudicated=%d fresh=%d excerpt=%d time-churn=%d "
         "receipt-open=%d receipt-stale=%d ua-serving=%d content-drift=%d gate=%d "
         "unavailable=%d window=%s\n"
         % (rows_printed, adjudicated, counts["fresh"], counts["excerpt"],
            counts["time-churn"], counts["receipt-open"], counts["receipt-stale"],
            counts["ua-serving"], counts["content-drift"], counts["gate"],
            counts["unavailable"], window))
    return 1 if unresolved else 0


def hashlib_sha(data):
    return hashlib.sha256(data).digest()


# --------------------------------------------------------------------- selftest

def _selftest():
    import hashlib
    import http.server
    import shutil
    import tempfile
    import threading
    from io import StringIO

    checks = []

    adj = load_adjudicator()
    mod = adj.load_sweep() if adj is not None else None
    if mod is None:
        print("MORI_DRIFT_RECHECK_SELFTEST: FAIL (0/1) — upstream tool chain missing")
        return 1

    class Handler(http.server.BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"
        routes = {}  # path -> {ua_prefix: (status, body)}, "*" matches any UA

        def log_message(self, *args):
            pass

        def do_GET(self):
            table = self.routes.get(self.path)
            if table is None:
                self.send_response(404)
                body = b"not found\n"
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            ua = self.headers.get("User-Agent", "")
            entry = table.get(ua, table.get("*"))
            status, body = entry
            self.send_response(status)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    tool_ua = mod.UA
    stamp_v1 = b"      Last updated on Nov 01, 2026 (05:22 UTC).\n"
    stamp_v2 = b"      Last updated on Nov 01, 2026 (08:57 UTC).\n"
    content = b"<html>teaching content stands still\n"
    body_fresh = content + stamp_v1                 # copy == live -> fresh
    body_churn = content + stamp_v2                 # stamp-only delta -> time-churn
    body_drift = content + b"AND the content changed\n" + stamp_v2
    other_body = b"different bytes served to the instrument UA\n"
    body_open = b"alpha\nbeta\n"

    def receipt_for(body):
        return (b"id: S911\nurl: https://127.0.0.1/receipt\nsha256: "
                + hashlib.sha256(body).hexdigest().encode("ascii")
                + b"\naccessed: 2026-11-01T00:00:00Z\nlines: 1-2\n\n"
                b"1 quoted\n2 lines\n")

    routes = {
        "/fresh": {tool_ua: (200, body_fresh), SECOND_UA_DEFAULT: (200, body_fresh)},
        "/time-churn": {tool_ua: (200, body_churn),
                        SECOND_UA_DEFAULT: (200, body_churn)},
        "/content-drift": {tool_ua: (200, body_drift),
                           SECOND_UA_DEFAULT: (200, body_drift)},
        "/ua-serving": {tool_ua: (200, other_body),
                        SECOND_UA_DEFAULT: (200, body_fresh)},
        "/receipt-open": {tool_ua: (200, body_open)},
        "/unavailable": {"*": (404, b"gone\n")},
    }
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), type(
        "H", (Handler,), {"routes": routes}))
    port = srv.server_address[1]
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()

    root = tempfile.mkdtemp(prefix="mori-drift-recheck-selftest-")
    try:
        corpus = os.path.join(root, "corpus")
        os.makedirs(corpus)
        evidence = os.path.join(corpus, "evidence", "sources-r90")
        os.makedirs(evidence)
        copies = {
            "S911": body_fresh,        # fresh
            "S912": body_fresh,        # time-churn (live stamp moved)
            "S913": body_fresh,        # content-drift (stamp + content)
            "S914": body_fresh,        # ua-serving (second UA == pin)
            "S915": receipt_for(body_open),  # receipt-open
            "S916": body_fresh,        # unavailable (404)
        }
        for sid, data in copies.items():
            with open(os.path.join(evidence, sid + ".src"), "wb") as fh:
                fh.write(data)
        registry = ["# SOURCES — recheck selftest fixture", "", "## Registry", "",
                    "| id | source | kind | tier | scope | anchor | teaches | status | "
                    "opened | recheck | used-by |",
                    "|---|---|---|---|---|---|---|---|---|---|---|"]
        for sid, path in (("S911", "/fresh"), ("S912", "/time-churn"),
                          ("S913", "/content-drift"), ("S914", "/ua-serving"),
                          ("S915", "/receipt-open"), ("S916", "/unavailable")):
            registry.append(
                "| %s | Doc — http://127.0.0.1:%d%s | docs | A | selftest | anchor | "
                "teaches | mined | 2026-11-01 | on-release | — |" % (sid, port, path))
        registry.append("")
        with open(os.path.join(corpus, "SOURCES.md"), "w", encoding="utf-8") as fh:
            fh.write("\n".join(registry))

        buf = StringIO()
        rc = run(root, out=buf)
        outtext = buf.getvalue()

        want = {
            "S911": "fresh", "S912": "time-churn", "S913": "content-drift",
            "S914": "ua-serving", "S915": "receipt-open", "S916": "unavailable",
        }
        got = {}
        as_of_re = re.compile(
            r"^%s (%s) as-of=(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)$"
            % ("(S\\d{3})", "|".join(TOKENS)))
        as_of_ok = True
        for line in outtext.splitlines():
            m = re.match(r"^(S\d{3}) (.+)$", line)
            if m and m.group(1) in want:
                got[m.group(1)] = re.sub(r" as-of=\S+$", "", m.group(2))
            m2 = as_of_re.match(line)
            if m2 is None and re.match(r"^S\d{3} ", line) and "no-copy" not in line \
                    and "unresolved" not in line:
                as_of_ok = False
        checks.append(("row_tokens", got == want, "got=%r want=%r" % (got, want)))
        checks.append(("as_of_on_every_row", as_of_ok,
                       "every token row carries as-of=<ISO8601Z>"))
        m = re.search(
            r"^MORI_DRIFT_RECHECK rows=(\d+) adjudicated=(\d+) fresh=(\d+) excerpt=(\d+) "
            r"time-churn=(\d+) receipt-open=(\d+) receipt-stale=(\d+) ua-serving=(\d+) "
            r"content-drift=(\d+) gate=(\d+) unavailable=(\d+) window=(\S+)$",
            outtext, re.M)
        checks.append(("summary", bool(m) and m.groups()[:11] ==
                       ("6", "6", "1", "0", "1", "1", "0", "1", "1", "0", "1"),
                       "summary=%s" % ((m.groups() if m else None),)))
        checks.append(("exit_code", rc == 0, "rc=%d want 0" % rc))
        checks.append(("header_disclosure",
                       "second_ua=%s" % SECOND_UA_DEFAULT in outtext
                       and "stamp-class=%s" % STAMP_CLASS_NAME in outtext
                       and "run-start=" in outtext,
                       "second UA + stamp class + run-start on the header line"))
        window_m = re.search(r"window=(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)"
                             r"\.\.(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)", outtext)
        checks.append(("window_same_run", bool(window_m) and window_m.group(1)
                       <= window_m.group(2),
                       "window bounds parse and are ordered (same-run snapshot pair)"))

        # setup error: missing SOURCES.md
        empty = tempfile.mkdtemp(prefix="mori-drift-recheck-empty-")
        try:
            os.makedirs(os.path.join(empty, "corpus"), exist_ok=True)
            oldout, olderr = StringIO(), StringIO()
            sys_stdout, sys_stderr = sys.stdout, sys.stderr
            sys.stdout, sys.stderr = oldout, olderr
            try:
                rc2 = run(empty, out=StringIO())
            finally:
                sys.stdout, sys_stderr = sys_stdout, sys_stderr
            checks.append(("missing_sources_exit2", rc2 == 2, "rc=%d want 2" % rc2))
        finally:
            shutil.rmtree(empty, ignore_errors=True)
    finally:
        srv.shutdown()
        srv.server_close()
        shutil.rmtree(root, ignore_errors=True)

    failed = [c for c in checks if not c[1]]
    for name, ok, detail in checks:
        print("selftest %-24s %s (%s)" % (name, "PASS" if ok else "FAIL", detail))
    if failed:
        print("MORI_DRIFT_RECHECK_SELFTEST: FAIL (%d/%d)"
              % (len(checks) - len(failed), len(checks)))
        return 1
    print("MORI_DRIFT_RECHECK_SELFTEST: PASS (%d cases)" % len(checks))
    return 0


def main(argv):
    args = list(argv)
    if args == ["--selftest"]:
        return _selftest()
    root = only = None
    second_ua = SECOND_UA_DEFAULT
    i = 0
    while i < len(args):
        if args[i] == "--root" and i + 1 < len(args):
            root = args[i + 1]
            i += 2
        elif args[i] == "--only" and i + 1 < len(args):
            parts = [p for p in args[i + 1].split(",") if p]
            if not parts or any(not ONLY_ID_RE.match(p) for p in parts):
                sys.stderr.write("MORI_DRIFT_RECHECK_SETUP: --only wants "
                                 "comma-separated S### ids\n")
                return 2
            only = set(parts)
            i += 2
        elif args[i] == "--second-ua" and i + 1 < len(args):
            second_ua = args[i + 1]
            i += 2
        else:
            sys.stderr.write("usage: %s --root DIR [--only S###,…] [--second-ua UA] "
                             "| --selftest\n"
                             % os.path.basename(args[0] if args else __file__))
            return 2
    if root is None:
        sys.stderr.write("usage: %s --root DIR [--only S###,…] [--second-ua UA] "
                         "| --selftest\n" % os.path.basename(__file__))
        return 2
    if not os.path.isdir(root):
        sys.stderr.write("MORI_DRIFT_RECHECK_SETUP: %s is not a directory\n" % root)
        return 2
    return run(root, only=only, second_ua=second_ua)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
