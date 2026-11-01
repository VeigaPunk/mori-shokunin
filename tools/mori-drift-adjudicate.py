#!/usr/bin/env python3
"""mori-drift-adjudicate.py — resolve the findings of the source-drift sweep into a closed set
(round 65 capability).

Usage:
  python tools/mori-drift-adjudicate.py --root DIR [--only S###,S###] [--second-ua UA]
  python tools/mori-drift-adjudicate.py --selftest

Background: the source-drift sweep flags `drifted` whenever the newest committed copy is not
reproducible from today's body under the instrument UA. That single state conflates distinct
situations, which the round-65 per-row disposition separated by hand (re-opened sources, two-UA
digests, field-level record diff; `.ufo/waves/round-65/evidence/disposition-*.txt`). This tool
automates that resolution so a future sweep's findings can be adjudicated in one run.

Per considered row, in registry order, one line `<id> <token>`:
  pass-through <state>   today's tool-UA body classifies fresh/excerpt against the copy —
                         nothing to resolve
  receipt-open           the copy is an excerpt receipt (header `id:`/`url:`/`sha256:`/...) and
                         the header's opening sha256 equals today's body sha256 — the source is
                         unchanged; the finding is the artifact shape, not content drift
  receipt-stale          copy is an excerpt receipt whose header sha256 does not equal today's
                         body — the body changed since the receipt was taken
  ua-serving             tool-UA body differs from the copy but a second-UA body equals it — the
                         vendor serves different bytes per User-Agent; under the pinning UA the
                         pin is current
  content-drift          both fetches differ from the copy — a real byte change under the
                         pinning UA (byte-level truth; whether the changed bytes are vendor
                         chrome or content is the semantic-review layer, QUALITY #41)
  gate                   a 2xx response with an empty body — publisher gate, no content evidence
  unavailable            the fetch failed (connection error, timeout, non-2xx, over-cap)
In `--only` mode, requested ids without a URL or copy print `<id> no-copy`.
Summary line:
  MORI_DRIFT_ADJUDICATE rows=N adjudicated=D passthrough=P receipt-open=a receipt-stale=b \
ua-serving=c content-drift=d gate=e unavailable=f
(rows = lines printed; adjudicated = non-passthrough copy-bearing resolutions)
Exit 0 when every considered copy-bearing row carries a token, 1 when any is unresolved, 2 on a
setup error (missing sweep tool, missing or unreadable SOURCES.md, bad usage). Read-only under
DIR; the selftest serves fixtures on 127.0.0.1 only.

Shared policy: row/URL grammar, copy discovery (highest sources-rN), fetch cap, redirect policy
and retry behavior are IMPORTED from the frozen sweep tool (tools/mori-source-drift.py, same
directory) — the adjudicator adjudicates that tool's findings, so it reuses its implementation
rather than duplicating it (v1.1 host-portable bytes). The second fetch applies the pinning UA by
temporarily setting the imported module's UA global (single-threaded, restored in `finally`); the
default `curl/8.21.0` is the UA the lane pinned copies with on this host, and every run prints it
on the header line so the receipt discloses which UA the verdicts bind.
"""

import hashlib
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SWEEP_FILENAME = "mori-source-drift.py"
SECOND_UA_DEFAULT = "curl/8.21.0"
ONLY_ID_RE = re.compile(r"^S\d{3}$")

TOKENS = ("receipt-open", "receipt-stale", "ua-serving", "content-drift",
          "gate", "unavailable")


def load_sweep():
    """Import the frozen sweep module from this tool's directory (None when absent)."""
    path = os.path.join(HERE, SWEEP_FILENAME)
    if not os.path.isfile(path):
        return None
    spec = importlib.util.spec_from_file_location("mori_source_drift", path)
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def fetch_with(mod, url, ua):
    """The sweep's fetch() under a different User-Agent (module-global swap, restored)."""
    original = mod.UA
    try:
        mod.UA = ua
        return mod.fetch(url)
    finally:
        mod.UA = original


def is_receipt(copy):
    """An r30-style excerpt receipt: header starts `id: S…` and carries a `sha256:` line."""
    head = copy[:256]
    return head.startswith(b"id: S") and b"\nsha256: " in head


def header_sha(copy):
    """The receipt header's opening sha256 digest (None when absent or malformed)."""
    for line in copy.splitlines()[:8]:
        if line.startswith(b"sha256: "):
            hexpart = line[len(b"sha256: "):].strip()
            if len(hexpart) == 64:
                try:
                    return bytes.fromhex(hexpart.decode("ascii"))
                except ValueError:
                    return None
    return None


def run(root, only=None, second_ua=SECOND_UA_DEFAULT, out=None):
    mod = load_sweep()
    if mod is None:
        print("MORI_DRIFT_ADJUDICATE_SETUP: %s missing beside this tool" % SWEEP_FILENAME,
              file=sys.stderr)
        return 2
    sources = os.path.join(root, "corpus", "SOURCES.md")
    try:
        with open(sources, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError:
        print("MORI_DRIFT_ADJUDICATE_SETUP: corpus/SOURCES.md missing or unreadable",
              file=sys.stderr)
        return 2
    emit = out.write if out is not None else sys.stdout.write
    emit("# MORI_DRIFT_ADJUDICATE second_ua=%s only=%s\n"
         % (second_ua, "all" if only is None else ",".join(sorted(only))))
    counts = {t: 0 for t in TOKENS}
    counts["passthrough"] = 0
    unresolved = 0
    rows_printed = 0
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
        if is_receipt(copy):
            outcome, body = mod.fetch(url)
            if outcome != "body":
                token = "unavailable"
            else:
                h = header_sha(copy)
                if h is None:
                    token = None  # receipt-shaped but no parsable opening sha
                elif h == hashlib.sha256(body).digest():
                    token = "receipt-open"
                else:
                    token = "receipt-stale"
        else:
            outcome_t, body_t = mod.fetch(url)
            copy_digest = hashlib.sha256(copy).digest()
            if outcome_t == "body" and hashlib.sha256(body_t).digest() == copy_digest:
                token = "pass-through fresh"
            elif outcome_t == "body" and copy.strip() and copy.strip() in body_t:
                token = "pass-through excerpt"
            elif outcome_t != "body":
                token = "unavailable"
            else:
                outcome_c, body_c = fetch_with(mod, url, second_ua)
                if outcome_c != "body":
                    token = "unavailable"
                elif len(body_c) == 0:
                    token = "gate"
                elif hashlib.sha256(body_c).digest() == copy_digest:
                    token = "ua-serving"
                else:
                    token = "content-drift"
        if token is None:
            unresolved += 1
            emit("%s unresolved\n" % sid)
        else:
            emit("%s %s\n" % (sid, token))
            if token.startswith("pass-through"):
                counts["passthrough"] += 1
            else:
                counts[token] += 1
    adjudicated = sum(counts[t] for t in TOKENS)
    emit("MORI_DRIFT_ADJUDICATE rows=%d adjudicated=%d passthrough=%d receipt-open=%d "
         "receipt-stale=%d ua-serving=%d content-drift=%d gate=%d unavailable=%d\n"
         % (rows_printed, adjudicated, counts["passthrough"], counts["receipt-open"],
            counts["receipt-stale"], counts["ua-serving"], counts["content-drift"],
            counts["gate"], counts["unavailable"]))
    return 1 if unresolved else 0


# --------------------------------------------------------------------- selftest

def _selftest():
    import http.server
    import shutil
    import tempfile
    import threading

    checks = []

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

    mod = load_sweep()
    if mod is None:
        print("MORI_DRIFT_ADJUDICATE_SELFTEST: FAIL (0/1) — sweep module missing")
        return 1

    tool_ua = mod.UA
    pin_body = b"pin bytes that must equal the copy\n"
    other_body = b"different bytes served to the instrument UA\n"
    body_open = b"alpha\nbeta\n"

    def receipt_for(body):
        return (b"id: S901\nurl: https://127.0.0.1/receipt\nsha256: "
                + hashlib.sha256(body).hexdigest().encode("ascii")
                + b"\naccessed: 2026-10-22T00:00:00Z\nlines: 1-2\n\n"
                b"1 quoted\n2 lines\n")

    routes = {
        "/receipt-open": {tool_ua: (200, body_open)},
        "/receipt-stale": {tool_ua: (200, b"a changed body\n")},
        "/ua-serving": {tool_ua: (200, other_body),
                        SECOND_UA_DEFAULT: (200, pin_body)},
        "/content-drift": {tool_ua: (200, other_body),
                           SECOND_UA_DEFAULT: (200, b"changed under both UAs\n")},
        "/gate": {"*": (200, b"")},
        "/unavailable": {"*": (404, b"gone\n")},
        "/fresh": {tool_ua: (200, pin_body), SECOND_UA_DEFAULT: (200, pin_body)},
    }
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), type(
        "H", (Handler,), {"routes": routes}))
    port = srv.server_address[1]
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()

    root = tempfile.mkdtemp(prefix="mori-drift-adjudicate-selftest-")
    try:
        corpus = os.path.join(root, "corpus")
        os.makedirs(corpus)
        evidence = os.path.join(corpus, "evidence", "sources-r90")
        os.makedirs(evidence)
        copies = {
            "S901": receipt_for(body_open),      # receipt-open
            "S902": receipt_for(body_open),      # receipt-stale (body changed)
            "S903": pin_body,                    # ua-serving
            "S904": pin_body,                    # content-drift
            "S905": pin_body,                    # gate
            "S906": pin_body,                    # unavailable (404)
            "S907": pin_body,                    # pass-through fresh
        }
        for sid, data in copies.items():
            with open(os.path.join(evidence, sid + ".src"), "wb") as fh:
                fh.write(data)
        registry = ["# SOURCES — adjudicate selftest fixture", "", "## Registry", "",
                    "| id | source | kind | tier | scope | anchor | teaches | status | "
                    "opened | recheck | used-by |",
                    "|---|---|---|---|---|---|---|---|---|---|---|"]
        for sid, path in (("S901", "/receipt-open"), ("S902", "/receipt-stale"),
                          ("S903", "/ua-serving"), ("S904", "/content-drift"),
                          ("S905", "/gate"), ("S906", "/unavailable"),
                          ("S907", "/fresh")):
            registry.append(
                "| %s | Doc — http://127.0.0.1:%d%s | docs | A | selftest | anchor | "
                "teaches | mined | 2026-11-01 | on-release | — |" % (sid, port, path))
        registry.append("")
        with open(os.path.join(corpus, "SOURCES.md"), "w", encoding="utf-8") as fh:
            fh.write("\n".join(registry))

        from io import StringIO
        buf = StringIO()
        rc = run(root, out=buf)
        outtext = buf.getvalue()
        want = {
            "S901": "receipt-open", "S902": "receipt-stale", "S903": "ua-serving",
            "S904": "content-drift", "S905": "gate", "S906": "unavailable",
            "S907": "pass-through fresh",
        }
        got = {}
        for line in outtext.splitlines():
            m = re.match(r"^(S\d{3}) (.+)$", line)
            if m and m.group(1) in want:
                got[m.group(1)] = m.group(2)
        checks.append(("row_tokens", got == want, "got=%r want=%r" % (got, want)))
        m = re.search(
            r"^MORI_DRIFT_ADJUDICATE rows=(\d+) adjudicated=(\d+) passthrough=(\d+) "
            r"receipt-open=(\d+) receipt-stale=(\d+) ua-serving=(\d+) content-drift=(\d+) "
            r"gate=(\d+) unavailable=(\d)$", outtext, re.M)
        checks.append(("summary", bool(m) and m.groups() ==
                       ("7", "6", "1", "1", "1", "1", "1", "1", "1"),
                       "summary=%s" % ((m.groups() if m else None),)))
        checks.append(("exit_code", rc == 0, "rc=%d want 0" % rc))
        checks.append(("header_line", "second_ua=%s" % SECOND_UA_DEFAULT in outtext,
                      "second UA disclosed on the header line"))

        # setup error: missing SOURCES.md
        empty = tempfile.mkdtemp(prefix="mori-drift-adjudicate-empty-")
        try:
            os.makedirs(os.path.join(empty, "corpus"), exist_ok=True)
            oldout, olderr = StringIO(), StringIO()
            sys_stdout, sys_stderr = sys.stdout, sys.stderr
            sys.stdout, sys.stderr = oldout, olderr
            try:
                rc2 = run(empty, out=StringIO())
            finally:
                sys.stdout, sys.stderr = sys_stdout, sys_stderr
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
        print("MORI_DRIFT_ADJUDICATE_SELFTEST: FAIL (%d/%d)"
              % (len(checks) - len(failed), len(checks)))
        return 1
    print("MORI_DRIFT_ADJUDICATE_SELFTEST: PASS (%d cases)" % len(checks))
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
                print("MORI_DRIFT_ADJUDICATE_SETUP: --only wants comma-separated S### ids",
                      file=sys.stderr)
                return 2
            only = set(parts)
            i += 2
        elif args[i] == "--second-ua" and i + 1 < len(args):
            second_ua = args[i + 1]
            i += 2
        else:
            print("usage: %s --root DIR [--only S###,…] [--second-ua UA] | --selftest"
                  % os.path.basename(args[0] if args else __file__), file=sys.stderr)
            return 2
    if root is None:
        print("usage: %s --root DIR [--only S###,…] [--second-ua UA] | --selftest"
              % os.path.basename(__file__), file=sys.stderr)
        return 2
    if not os.path.isdir(root):
        print("MORI_DRIFT_ADJUDICATE_SETUP: %s is not a directory" % root, file=sys.stderr)
        return 2
    return run(root, only=only, second_ua=second_ua)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
