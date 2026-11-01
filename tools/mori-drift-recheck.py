#!/usr/bin/env python3
"""mori-drift-recheck.py — the standing adjudicate RE-CHECK: every verdict carries the
moment it was measured, and vendor build churn (page stamps, asset build-ids) no longer
masquerades as content drift (round 66 capability; asset grammar round 67).

Usage:
  python tools/mori-drift-recheck.py --root DIR [--only S###,S###] [--second-ua UA]
  python tools/mori-drift-recheck.py --root DIR --from-sweep SWEEP_RECEIPT [--second-ua UA]
  python tools/mori-drift-recheck.py --selftest

--from-sweep (r67, the r66 closure's routed note 2) reads the sweep receipt's own
finding list instead of a hand-copied `--only` id list: a row counts only when the
whole line matches `S### drifted` (never the `drifted=N` summary token — the r65
M1 class of counting a summary as rows), the parsed row set must agree with the
receipt's own `drifted=N` summary (rc 2 on disagreement), and a file with neither
drifted rows nor a MORI_SOURCE_DRIFT summary is refused (rc 2, not a sweep receipt).
--from-sweep and --only are mutually exclusive.

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
                               own moment, the fetch certifies T. Decided on the
                               instrument-UA body first; if the instrument UA is
                               served a different variant, on the pinning-UA body
                               (r67 — the pinning variant is what the pin certifies)
  asset-churn as-of=T          fresh body differs from the copy at T, but the diff is
                               confined to the learn.microsoft.com static-asset
                               build-id path segment (regex below) — a vendor rebuild
                               re-versioned its asset URLs, content stands still
                               (r67 grammar; the class the r65 KEEP-CHROME semantic
                               disposition of S241 names at the byte layer). Same
                               two-arm order as time-churn: instrument-UA body
                               first, pinning-UA body second — the S241 live shape
                               (the pinning body shows only the build-id move while
                               the instrument UA additionally receives per-response
                               bot-manager chrome, which is serving variance, not
                               content and not a third grammar)
  ua-serving as-of=T           tool-UA body differs beyond stamp lines but the second
                               (pinning) UA body equals the copy byte-identical
  content-drift as-of=T        fresh bodies differ from the copy beyond both churn
                               grammars under both UAs — content changed, not the
                               template
  gate as-of=T                 2xx response with an empty body
  unavailable as-of=T          the fetch failed (connection error, timeout, non-2xx,
                               over-cap)
  <id> no-copy                 no URL or no newest committed copy — nothing fetched,
                               so no moment exists to record (honest absence)

Churn grammars (the only normalizations applied, each disclosed on the header line;
VENDOR-SCOPED — a grammar taught for one vendor is never silently generalized, another
vendor's build artifact stays honest `content-drift` until its own grammar is taught
from pinned observed bytes, r67 disclosure):

1. python-docs-page-stamp (`time-churn`): a line consisting solely of
     Last updated on <Mon DD, YYYY> (<HH:MM UTC>).
   optionally indented, with an optional trailing period — the Sphinx
   `html_last_updated_fmt` render the python docs templates write at every build.
   Ground: S577 (the stamp is a per-build strftime render) pinned at
   corpus/evidence/sources-r66/S577.html:2638-2639; the render observed at
   corpus/evidence/sources-r65/S347.html:3328.

2. learn-microsoft-asset-build-id (`asset-churn`): the path segment
     /static/assets/<build-id>/
   where <build-id> is four dot-separated numerals, a hyphen and eight lowercase
   hex characters (observed 0.4.03574.8308-9505b1c8 -> 0.4.03589.8339-b0a05127),
   inside an asset URL. Ground: the vendor's own redeploy signature recorded in
   .ufo/waves/round-65/evidence/disposition-diffs-r65.txt (S241, changed_opcodes=2,
   both asset-reference lines, anchors identical — the r65 semantic review's
   KEEP-CHROME naming, now a byte-layer class).

Both sides (copy and fresh body) are reduced to their non-stamp line sequences for
the `time-churn` comparison and to their build-id-substituted line sequences for the
`asset-churn` comparison; a delta that mixes a stamp line and an asset id line
satisfies NEITHER grammar (each normalization only removes its own class of bytes)
and classifies `content-drift`; every other class is decided on raw bytes.

Summary line:
  MORI_DRIFT_RECHECK rows=N adjudicated=D fresh=F excerpt=E time-churn=C \
asset-churn=A receipt-open=O receipt-stale=S ua-serving=U content-drift=D gate=G \
unavailable=X window=<earliest as-of>..<latest as-of>
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

# learn.microsoft.com static-asset build-id path segment, as recorded in the r65
# disposition diff receipt for S241 (changed_opcodes=2, both asset-reference lines):
#   /static/assets/0.4.03574.8308-9505b1c8/styles/site.css
#   -> /static/assets/0.4.03589.8339-b0a05127/styles/site.css
ASSET_RE = re.compile(
    rb"/static/assets/[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+-[0-9a-f]{8}/")

ASSET_CLASS_NAME = "learn-microsoft-asset-build-id"

# sweep-receipt finding-list grammar (r67 --from-sweep): a drifted finding is a row
# line only — `S### drifted` with optional trailing columns; the summary token
# `drifted=N` on the MORI_SOURCE_DRIFT line is a count, never a row (lesson M1).
SWEEP_DRIFTED_RE = re.compile(r"^(S\d{3}) drifted(?: |$)")
SWEEP_SUMMARY_RE = re.compile(r"^MORI_SOURCE_DRIFT\b.*\bdrifted=(\d+)(?: |$)")

TOKENS = ("fresh", "excerpt", "time-churn", "asset-churn", "receipt-open",
          "receipt-stale", "ua-serving", "content-drift", "gate", "unavailable")


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


def asset_free(body):
    """The body's line sequence with each asset build-id substituted (bytes)."""
    return [ASSET_RE.sub(b"/static/assets/<build-id>/", ln)
            for ln in body.splitlines()]


def parse_sweep_findings(text):
    """A sweep receipt's drifted finding ids plus its own summary count.

    Rows are lines whose WHOLE head matches `S### drifted`; the summary token
    `drifted=N` is kept separately so the caller can demand row/summary agreement
    (the r65 M1 lesson: a summary token must never be counted as a row).
    """
    ids = []
    seen = set()
    summary_n = None
    for line in text.splitlines():
        m = SWEEP_DRIFTED_RE.match(line)
        if m is not None:
            sid = m.group(1)
            if sid not in seen:
                seen.add(sid)
                ids.append(sid)
            continue
        m = SWEEP_SUMMARY_RE.match(line)
        if m is not None:
            summary_n = int(m.group(1))
    return ids, summary_n


def now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run(root, only=None, second_ua=SECOND_UA_DEFAULT, out=None, _now=now_utc,
        from_sweep_receipt=None):
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
    from_sweep_label = "-"
    findings_n = "-"
    if from_sweep_receipt is not None:
        try:
            with open(from_sweep_receipt, "r", encoding="utf-8",
                      errors="replace") as fh:
                receipt_text = fh.read()
        except OSError:
            sys.stderr.write("MORI_DRIFT_RECHECK_SETUP: --from-sweep %s missing "
                             "or unreadable\n" % from_sweep_receipt)
            return 2
        ids, summary_n = parse_sweep_findings(receipt_text)
        if not ids and summary_n is None:
            sys.stderr.write("MORI_DRIFT_RECHECK_SETUP: --from-sweep %s carries "
                             "neither `S### drifted` rows nor a MORI_SOURCE_DRIFT "
                             "summary — not a sweep receipt\n"
                             % from_sweep_receipt)
            return 2
        if summary_n is not None and summary_n != len(ids):
            sys.stderr.write("MORI_DRIFT_RECHECK_SETUP: --from-sweep %s rows=%d "
                             "disagree with its own drifted=%d summary\n"
                             % (from_sweep_receipt, len(ids), summary_n))
            return 2
        only = set(ids)
        from_sweep_label = from_sweep_receipt
        findings_n = str(len(ids))
    emit = out.write if out is not None else sys.stdout.write
    emit("# MORI_DRIFT_RECHECK second_ua=%s only=%s from-sweep=%s findings=%s "
         "run-start=%s stamp-class=%s asset-class=%s\n"
         % (second_ua, "all" if only is None else ",".join(sorted(only)),
            from_sweep_label, findings_n, _now(), STAMP_CLASS_NAME,
            ASSET_CLASS_NAME))
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
        elif asset_free(copy) == asset_free(body_t):
            token = "asset-churn"
        else:
            outcome_c, body_c = adj.fetch_with(mod, url, second_ua)
            if outcome_c != "body":
                token = "unavailable"
            elif len(body_c) == 0:
                token = "gate"
            elif hashlib_sha(body_c) == hashlib_sha(copy):
                token = "ua-serving"
            elif stamp_free(copy) == stamp_free(body_c):
                token = "time-churn"
            elif asset_free(copy) == asset_free(body_c):
                token = "asset-churn"
            else:
                token = "content-drift"
        if token is None:
            unresolved += 1
            emit("%s unresolved as-of=%s\n" % (sid, as_of))
        else:
            emit("%s %s as-of=%s\n" % (sid, token, as_of))
            counts[token] += 1
    adjudicated = sum(counts[t] for t in TOKENS)
    if from_sweep_receipt is not None and len(only) != rows_printed:
        sys.stderr.write("MORI_DRIFT_RECHECK_SETUP: --from-sweep names %d findings "
                         "but only %d exist in the registry at this --root\n"
                         % (len(only), rows_printed))
        return 2
    window = "%s..%s" % (min(moments), max(moments)) if moments else "-"
    emit("MORI_DRIFT_RECHECK rows=%d adjudicated=%d fresh=%d excerpt=%d time-churn=%d "
         "asset-churn=%d receipt-open=%d receipt-stale=%d ua-serving=%d "
         "content-drift=%d gate=%d unavailable=%d window=%s\n"
         % (rows_printed, adjudicated, counts["fresh"], counts["excerpt"],
            counts["time-churn"], counts["asset-churn"], counts["receipt-open"],
            counts["receipt-stale"], counts["ua-serving"], counts["content-drift"],
            counts["gate"], counts["unavailable"], window))
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
    # the learn.microsoft.com asset build-id pair the r65 disposition diff
    # receipt recorded for S241 (changed_opcodes=2, both asset-reference lines)
    asset_v1 = b"0.4.03574.8308-9505b1c8"
    asset_v2 = b"0.4.03589.8339-b0a05127"

    def learn_page(asset):
        return (b"<html>vendor teaching content stands still\n"
                b"\t\t<link rel=\"stylesheet\" href=\"/static/assets/" + asset
                + b"/styles/site.css\" />\n")

    body_asset_a = learn_page(asset_v1)             # the copy (pin)
    body_asset_b = learn_page(asset_v2)             # live: newer build id -> asset-churn
    # the S241 live shape (r67): the instrument UA additionally receives
    # per-response bot-manager chrome, so the row must resolve on the pinning body
    body_asset_instrument = (
        b"<html>vendor teaching content stands still\n"
        b"\t\t<link rel=\"stylesheet\" href=\"/static/assets/" + asset_v2
        + b"/styles/site.css\" />\n"
        b"\t\t<script >bazadebezolkohpepadr=\"1808992084\"</script>\n")

    def receipt_for(body):
        return (b"id: S911\nurl: https://127.0.0.1/receipt\nsha256: "
                + hashlib.sha256(body).hexdigest().encode("ascii")
                + b"\naccessed: 2026-11-01T00:00:00Z\nlines: 1-2\n\n"
                b"1 quoted\n2 lines\n")

    routes = {
        "/fresh": {tool_ua: (200, body_fresh), SECOND_UA_DEFAULT: (200, body_fresh)},
        "/time-churn": {tool_ua: (200, body_churn),
                        SECOND_UA_DEFAULT: (200, body_churn)},
        "/asset-churn": {tool_ua: (200, body_asset_b),
                         SECOND_UA_DEFAULT: (200, body_asset_b)},
        "/asset-churn-second-arm": {tool_ua: (200, body_asset_instrument),
                                    SECOND_UA_DEFAULT: (200, body_asset_b)},
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
            "S913": body_asset_a,      # asset-churn (live build id moved)
            "S914": body_asset_a,      # asset-churn on the pinning body (S241 shape)
            "S915": body_fresh,        # content-drift (stamp + content)
            "S916": body_fresh,        # ua-serving (second UA == pin)
            "S917": receipt_for(body_open),  # receipt-open
            "S918": body_fresh,        # unavailable (404)
        }
        for sid, data in copies.items():
            with open(os.path.join(evidence, sid + ".src"), "wb") as fh:
                fh.write(data)
        registry = ["# SOURCES — recheck selftest fixture", "", "## Registry", "",
                    "| id | source | kind | tier | scope | anchor | teaches | status | "
                    "opened | recheck | used-by |",
                    "|---|---|---|---|---|---|---|---|---|---|---|"]
        for sid, path in (("S911", "/fresh"), ("S912", "/time-churn"),
                          ("S913", "/asset-churn"),
                          ("S914", "/asset-churn-second-arm"),
                          ("S915", "/content-drift"), ("S916", "/ua-serving"),
                          ("S917", "/receipt-open"), ("S918", "/unavailable")):
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
            "S911": "fresh", "S912": "time-churn", "S913": "asset-churn",
            "S914": "asset-churn", "S915": "content-drift", "S916": "ua-serving",
            "S917": "receipt-open", "S918": "unavailable",
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
            r"time-churn=(\d+) asset-churn=(\d+) receipt-open=(\d+) receipt-stale=(\d+) "
            r"ua-serving=(\d+) content-drift=(\d+) gate=(\d+) unavailable=(\d+) "
            r"window=(\S+)$",
            outtext, re.M)
        checks.append(("summary", bool(m) and m.groups()[:12] ==
                       ("8", "8", "1", "0", "1", "2", "1", "0", "1", "1", "0", "1"),
                       "summary=%s" % ((m.groups() if m else None),)))
        checks.append(("exit_code", rc == 0, "rc=%d want 0" % rc))
        checks.append(("header_disclosure",
                       "second_ua=%s" % SECOND_UA_DEFAULT in outtext
                       and "stamp-class=%s" % STAMP_CLASS_NAME in outtext
                       and "asset-class=%s" % ASSET_CLASS_NAME in outtext
                       and "from-sweep=-" in outtext
                       and "run-start=" in outtext,
                       "second UA + both churn classes + from-sweep=- + run-start "
                       "on the header line"))
        window_m = re.search(r"window=(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)"
                             r"\.\.(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)", outtext)
        checks.append(("window_same_run", bool(window_m) and window_m.group(1)
                       <= window_m.group(2),
                       "window bounds parse and are ordered (same-run snapshot pair)"))

        # --from-sweep (r67): the receipt's own finding list drives the run
        ids_p, n_p = parse_sweep_findings(
            "S156 drifted\nsome prose drifted=9\n"
            "MORI_SOURCE_DRIFT rows=349 fresh=62 excerpt=0 drifted=17 "
            "unavailable=2 no-copy=268\nS156 drifted\n")
        checks.append(("parse_sweep_rows_not_summary",
                       ids_p == ["S156"] and n_p == 17,
                       "row lines only (deduped), summary token kept separate: "
                       "ids=%r summary_n=%r" % (ids_p, n_p)))
        sweep_receipt = os.path.join(root, "sweep-fixture.txt")
        with open(sweep_receipt, "w", encoding="utf-8") as fh:
            fh.write("# fixture sweep receipt\n"
                     "S911 fresh\n"
                     "S912 drifted\n"
                     "S913 drifted\n"
                     "S918 unavailable\n"
                     "MORI_SOURCE_DRIFT rows=4 fresh=1 excerpt=0 drifted=2 "
                     "unavailable=1 no-copy=0\n")
        buf2 = StringIO()
        rc_fs = run(root, out=buf2, from_sweep_receipt=sweep_receipt)
        fs_text = buf2.getvalue()
        fs_rows = sorted(re.findall(r"^(S\d{3}) ", fs_text, re.M))
        checks.append(("from_sweep_selects_drifted",
                       rc_fs == 0 and fs_rows == ["S912", "S913"]
                       and "findings=2" in fs_text
                       and "from-sweep=%s" % sweep_receipt in fs_text
                       and "S911 " not in fs_text,
                       "only the receipt's drifted rows adjudicated: rows=%r rc=%d"
                       % (fs_rows, rc_fs)))
        bad_receipt = os.path.join(root, "not-a-sweep.txt")
        with open(bad_receipt, "w", encoding="utf-8") as fh:
            fh.write("hello world\nno rows or summary here\n")
        disagree_receipt = os.path.join(root, "disagreeing-sweep.txt")
        with open(disagree_receipt, "w", encoding="utf-8") as fh:
            fh.write("S912 drifted\nMORI_SOURCE_DRIFT rows=1 fresh=0 drifted=5\n")
        sys_stdout, sys_stderr = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = StringIO(), StringIO()
        try:
            rc_bad = run(root, out=StringIO(), from_sweep_receipt=bad_receipt)
            rc_dis = run(root, out=StringIO(),
                         from_sweep_receipt=disagree_receipt)
        finally:
            sys.stdout, sys.stderr = sys_stdout, sys_stderr
        checks.append(("from_sweep_malformed_exit2",
                       rc_bad == 2 and rc_dis == 2,
                       "not-a-sweep rc=%d; rows-vs-summary disagreement "
                       "rc=%d (both want 2)" % (rc_bad, rc_dis)))

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
    from_sweep = None
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
        elif args[i] == "--from-sweep" and i + 1 < len(args):
            from_sweep = args[i + 1]
            i += 2
        elif args[i] == "--second-ua" and i + 1 < len(args):
            second_ua = args[i + 1]
            i += 2
        else:
            sys.stderr.write("usage: %s --root DIR [--only S###,… | --from-sweep "
                             "SWEEP_RECEIPT] [--second-ua UA] | --selftest\n"
                             % os.path.basename(args[0] if args else __file__))
            return 2
    if only is not None and from_sweep is not None:
        sys.stderr.write("MORI_DRIFT_RECHECK_SETUP: --only and --from-sweep are "
                         "mutually exclusive\n")
        return 2
    if root is None:
        sys.stderr.write("usage: %s --root DIR [--only S###,… | --from-sweep "
                         "SWEEP_RECEIPT] [--second-ua UA] | --selftest\n"
                         % os.path.basename(__file__))
        return 2
    if not os.path.isdir(root):
        sys.stderr.write("MORI_DRIFT_RECHECK_SETUP: %s is not a directory\n" % root)
        return 2
    return run(root, only=only, second_ua=second_ua, from_sweep_receipt=from_sweep)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
