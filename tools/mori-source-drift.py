#!/usr/bin/env python3
"""mori-source-drift.py — re-fetch each corpus/SOURCES.md row that has a committed
copy and classify the copy against today's body (round 36, C1 exploratory probe).

Usage:
  python3 tools/mori-source-drift.py --root DIR
  python3 tools/mori-source-drift.py --selftest

Row rule: a line starting with `| S` and three digits. The row's URL is the first
http(s):// URL in the source cell with trailing `.,;)` stripped. The row's copy is
DIR/corpus/evidence/sources-r<N>/<id>.<ext> (any extension) in the directory with
the highest integer N.

Per row, in registry order, one line `<id> <state>`:
  no-copy     the row has no URL or no copy file (no fetch is made)
  unavailable the GET fails (connection error, timeout, or a non-2xx final status;
              redirects are followed; limited retries)
  fresh       sha256 of the fetched body equals sha256 of the copy bytes
  excerpt     not fresh, and the copy bytes with whitespace stripped at both ends are
              non-empty and occur contiguously in the fetched body
  drifted     otherwise
Then one summary line:
  MORI_SOURCE_DRIFT rows=N fresh=a excerpt=b drifted=c unavailable=d no-copy=e

Exit 0 when drifted=0, 1 when any row is drifted, 2 on a setup error (missing or
unreadable SOURCES.md, bad usage). Read-only: no writes under DIR. `drifted` means
the committed copy is not reproducible from today's body — it is not proof the source
changed (see corpus/knowledge/source-drift-r36.md).
"""

import hashlib
import http.server
import ipaddress
import os
import re
import shutil
import socket
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

ROW_RE = re.compile(r"^\| S\d{3} ")
URL_RE = re.compile(r"https?://[^\s|]+")
COPY_DIR_RE = re.compile(r"^sources-r(\d+)$")

STATES = ("fresh", "excerpt", "drifted", "unavailable", "no-copy")

FETCH_TIMEOUT_S = 30
FETCH_TRIES = 3
FETCH_MAX_BYTES = 4 * 1024 * 1024  # bodies larger than this cannot be classified; read is capped at +1
UA = "mori-source-drift/1.0"


# --------------------------------------------------------------------- registry

def parse_registry(text):
    """Rows of a SOURCES.md registry: (id, url) in file order."""
    rows = []
    for line in text.splitlines():
        if not ROW_RE.match(line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        m = URL_RE.search(cells[1])
        url = m.group(0).rstrip(".,;)") if m else None
        rows.append((cells[0], url))
    return rows


def find_copy(root, sid):
    """The copy of a row: corpus/evidence/sources-r<N>/<sid>.<ext>, highest N."""
    evidence = os.path.join(root, "corpus", "evidence")
    best = None
    try:
        names = os.listdir(evidence)
    except OSError:
        return None
    for name in names:
        m = COPY_DIR_RE.match(name)
        if not m:
            continue
        n = int(m.group(1))
        d = os.path.join(evidence, name)
        if not os.path.isdir(d):
            continue
        try:
            entries = sorted(os.listdir(d))
        except OSError:
            continue
        for entry in entries:
            if entry.startswith(sid + "."):
                if best is None or n > best[0]:
                    best = (n, os.path.join(d, entry))
    return best[1] if best else None


def _fetchable_initial(url):
    """Initial-request policy: http/https with a host. Loopback and private literals stay
    fetchable — the registry is lane-curated and append-only, and the frozen counter's blind
    fixture legitimately serves on 127.0.0.1 (w2/SentCensus scoping)."""
    try:
        parts = urllib.parse.urlsplit(url)
        return parts.scheme in ("http", "https") and bool(parts.hostname)
    except ValueError:
        return False


def _public_redirect_target(url):
    """Post-redirect policy (w2/SentCensus): a server-driven redirect must land on a public
    http/https destination — loopback, link-local, private literals and localhost names are
    refused (conditional-request CSRF class). Residual, disclosed: DNS-resolved private
    addresses of public names are not re-checked (urllib resolves internally)."""
    try:
        parts = urllib.parse.urlsplit(url)
        if parts.scheme not in ("http", "https"):
            return False
        host = parts.hostname
        if not host:
            return False
        try:
            addr = ipaddress.ip_address(host)
            return addr.is_global
        except ValueError:
            pass
        low = host.lower().rstrip(".")
        if low == "localhost" or low.endswith(".localhost") or low.endswith(".local"):
            return False
        return True
    except ValueError:
        return False


# --------------------------------------------------------------------- fetching

def fetch(url):
    """GET url. Returns (outcome, body):
    ("body", bytes)        a 2xx response was received
    ("unavailable", None)  connection error, timeout, a non-2xx final status, an over-cap
                           body, or a non-public destination (initial or post-redirect)
    Limited retries: on 429 the Retry-After header is honoured (capped); on other
    5xx and on connection errors a short fixed backoff is used."""
    if not _fetchable_initial(url):
        return "unavailable", None
    last_wait = 0.0
    for attempt in range(FETCH_TRIES):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT_S) as resp:
                final = resp.geturl()
                if final != url:
                    # a redirect actually happened: the new authority must be public
                    # (loopback/private targets are refused; w2/SentCensus)
                    if not _public_redirect_target(final):
                        return "unavailable", None
                # bounded read: an untrusted source must not stream past the cap or stall
                # between bytes past the socket timeout (w2/SentTools) — an over-cap or
                # truncated body is not classifiable and grades unavailable.
                body = resp.read(FETCH_MAX_BYTES + 1)
                if len(body) > FETCH_MAX_BYTES:
                    return "unavailable", None
                return "body", body
        except urllib.error.HTTPError as exc:
            code = exc.code
            try:
                exc.close()
            except Exception:
                pass
            if 400 <= code < 600:
                if code == 429 and attempt < FETCH_TRIES - 1:
                    header = None
                    try:
                        header = exc.headers.get("Retry-After") if exc.headers else None
                    except Exception:
                        header = None
                    wait = 5.0
                    if header:
                        try:
                            wait = min(max(float(header), 0.0), 120.0)
                        except (TypeError, ValueError):
                            wait = 5.0
                    last_wait = wait
                    time.sleep(wait)
                    continue
                if 500 <= code < 600 and attempt < FETCH_TRIES - 1:
                    time.sleep(2.0 if attempt == 0 else 8.0)
                    continue
                return "unavailable", None
            return "unavailable", None
        except Exception:
            if attempt < FETCH_TRIES - 1:
                time.sleep(1.0 if attempt == 0 else 3.0)
                continue
            return "unavailable", None
    return "unavailable", None


def classify(body, copy):
    if hashlib.sha256(body).digest() == hashlib.sha256(copy).digest():
        return "fresh"
    stripped = copy.strip()
    if stripped and stripped in body:
        return "excerpt"
    return "drifted"


# --------------------------------------------------------------------- main

def run(root):
    sources = os.path.join(root, "corpus", "SOURCES.md")
    try:
        with open(sources, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError:
        print("MORI_SOURCE_DRIFT_SETUP: corpus/SOURCES.md missing or unreadable",
              file=sys.stderr)
        return 2
    rows = parse_registry(text)
    counts = {s: 0 for s in STATES}
    lines = []
    for sid, url in rows:
        copy_path = find_copy(root, sid) if url is not None else None
        if url is None or copy_path is None:
            state = "no-copy"
        else:
            try:
                with open(copy_path, "rb") as fh:
                    copy = fh.read()
            except OSError:
                copy = None
            if copy is None:
                state = "no-copy"
            else:
                outcome, body = fetch(url)
                if outcome != "body":
                    state = "unavailable"
                else:
                    state = classify(body, copy)
        counts[state] += 1
        lines.append("%s %s" % (sid, state))
    for line in lines:
        print(line)
    print("MORI_SOURCE_DRIFT rows=%d fresh=%d excerpt=%d drifted=%d unavailable=%d "
          "no-copy=%d" % (len(rows), counts["fresh"], counts["excerpt"],
                          counts["drifted"], counts["unavailable"],
                          counts["no-copy"]))
    return 1 if counts["drifted"] else 0


# --------------------------------------------------------------------- selftest

class _Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    routes = {}

    def log_message(self, *args):
        pass

    def do_GET(self):
        route = self.routes.get(self.path)
        if route is None:
            self.send_response(404)
            body = b"not found\n"
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        status, body = route
        if status == "close":
            self.connection.shutdown(socket.SHUT_RDWR)
            self.connection.close()
            return
        if status == "redir":
            self.send_response(302)
            self.send_header("Location", body % {"port": self.server.server_address[1]})
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        self.send_response(status)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def _serve(routes):
    handler = type("H", (_Handler,), {"routes": routes})
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    port = srv.server_address[1]
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    return srv, port


def _selftest():
    checks = []
    root = tempfile.mkdtemp(prefix="mori-source-drift-selftest-")
    try:
        corpus = os.path.join(root, "corpus")
        evidence = os.path.join(corpus, "evidence")
        routes = {}
        base = "http://127.0.0.1:%d" % 0  # placeholder, fixed after serve()
        srv, port = _serve(routes)
        try:
            base = "http://127.0.0.1:%d" % port
            body_fresh = b"The quick brown fox\njumps over the lazy dog\n" * 4
            body_excerpt = b"header line\n" + b"alpha beta gamma delta epsilon\n" * 12
            piece = body_excerpt[20:120]
            body_drifted = bytearray(body_fresh)
            body_drifted[5] ^= 0x10
            body_drifted = bytes(body_drifted)
            routes["/fresh"] = (200, body_fresh)
            routes["/excerpt"] = (200, body_excerpt)
            routes["/drifted"] = (200, body_drifted)
            routes["/gone"] = (404, b"not found\n")
            routes["/boom"] = (500, b"server error\n")
            routes["/close"] = ("close", b"")
            routes["/trail"] = (200, body_fresh)
            routes["/huge"] = (200, b"x" * (4 * 1024 * 1024 + 64))
            routes["/redir"] = ("redir", "/fresh")

            def w(reldir, name, data):
                d = os.path.join(evidence, reldir)
                os.makedirs(d, exist_ok=True)
                with open(os.path.join(d, name), "wb") as fh:
                    fh.write(data)

            w("sources-r40", "S101.src", body_fresh)           # fresh, newest
            w("sources-r10", "S101.src", b"older decoy bytes")  # decoy: lower N
            w("sources-r40", "S102.txt", b"  \n" + piece + b"\t ")
            w("sources-r40", "S103.md", body_fresh)             # drifted vs flipped body
            w("sources-r40", "S104.src", body_fresh)            # 404
            w("sources-r40", "S105.src", body_fresh)            # close
            w("sources-r40", "S106.src", body_fresh)            # URL but no route? no:
            w("sources-r40", "S108.html", body_fresh)           # trailing punctuation URL
            w("sources-r40", "S109.src", b"x" * 100)            # over-cap body -> unavailable
            w("sources-r40", "S110.src", body_fresh)            # 302 -> loopback -> refused

            registry = "\n".join([
                "# SOURCES — selftest fixture",
                "",
                "## Registry",
                "",
                "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |",
                "|---|---|---|---|---|---|---|---|---|---|---|",
                "| S101 | Doc fresh — %s/fresh | docs | A | selftest | anchor | teaches | mined | 2026-10-23 | on-release | — |" % base,
                "| S102 | Doc excerpt — %s/excerpt | docs | A | selftest | anchor | teaches | mined | 2026-10-23 | on-release | — |" % base,
                "| S103 | Doc drifted — %s/drifted | docs | A | selftest | anchor | teaches | mined | 2026-10-23 | on-release | — |" % base,
                "| S104 | Doc gone — %s/gone | docs | A | selftest | anchor | teaches | mined | 2026-10-23 | on-release | — |" % base,
                "| S105 | Doc close — %s/close | docs | A | selftest | anchor | teaches | mined | 2026-10-23 | on-release | — |" % base,
                "| S106 | Doc has-url-no-copy — %s/fresh | docs | A | selftest | anchor | teaches | mined | 2026-10-23 | on-release | — |" % base,
                "| S107 | Doc no-url — internal note, no fetchable source | docs | A | selftest | anchor | teaches | mined | 2026-10-23 | on-release | — |",
                "| S108 | Doc trail — %s/trail). | docs | A | selftest | anchor | teaches | mined | 2026-10-23 | on-release | — |" % base,
                "| S109 | Doc huge — %s/huge | docs | A | selftest | anchor | teaches | mined | 2026-10-23 | on-release | — |" % base,
                "| S110 | Doc redir — %s/redir | docs | A | selftest | anchor | teaches | mined | 2026-10-23 | on-release | — |" % base,
                "",
            ])
            with open(os.path.join(corpus, "SOURCES.md"), "w", encoding="utf-8") as fh:
                fh.write(registry)

            # fixture rows above include a copy for S106 in r40? no: S106's copy must
            # be absent for no-copy. Remove the accidentally written one.
            os.remove(os.path.join(evidence, "sources-r40", "S106.src"))

            expected = [
                ("S101", "fresh"), ("S102", "excerpt"), ("S103", "drifted"),
                ("S104", "unavailable"), ("S105", "unavailable"),
                ("S106", "no-copy"), ("S107", "no-copy"), ("S108", "fresh"),
                ("S109", "unavailable"), ("S110", "unavailable"),
            ]
            from io import StringIO
            buf = StringIO()
            old = sys.stdout
            sys.stdout = buf
            try:
                rc = run(root)
            finally:
                sys.stdout = old
            out = buf.getvalue()
            checks.append(("exit_code", rc == 1, "rc=%d want 1 (one drifted)" % rc))
            lines = [l for l in out.splitlines()
                     if re.match(r"^S\d{3} (fresh|excerpt|drifted|unavailable|no-copy)$", l)]
            got = []
            for l in lines:
                sid, state = l.split(" ", 1)
                got.append((sid, state))
            checks.append(("row_states", got == expected,
                           "got=%r want=%r" % (got, expected)))
            m = re.search(r"^MORI_SOURCE_DRIFT rows=(\d+) fresh=(\d+) excerpt=(\d+) "
                          r"drifted=(\d+) unavailable=(\d+) no-copy=(\d+)$",
                          out, re.M)
            checks.append(("summary", bool(m) and m.groups() == ("10", "2", "1", "1", "4", "2"),
                           "summary=%s" % ((m.groups() if m else None),)))

            # Round 37 named arms for the two w2/SentCensus hardening policies. Each
            # policy is asserted directly, so a copy with that policy removed fails
            # exactly its own arm (the round-37 counter mutates both anchors).
            outcome_over, _ = fetch(base + "/huge")
            cap_body = 4 * 1024 * 1024  # the frozen cap value, literal: a mutated cap must
            routes["/big"] = (200, b"y" * cap_body)  # not resize this fixture
            outcome_at, body_at = fetch(base + "/big")
            checks.append((
                "huge_cap",
                outcome_over == "unavailable" and outcome_at == "body"
                and body_at is not None and len(body_at) == cap_body,
                "over_cap=%s at_cap=%s len=%s" % (
                    outcome_over, outcome_at,
                    None if body_at is None else len(body_at))))
            outcome_redir, _ = fetch(base + "/redir")
            checks.append((
                "redirect_private_refused",
                outcome_redir == "unavailable",
                "redirect_to_loopback=%s" % outcome_redir))
        finally:
            srv.shutdown()
            srv.server_close()

        # setup error: missing SOURCES.md
        empty = tempfile.mkdtemp(prefix="mori-source-drift-empty-")
        try:
            os.makedirs(os.path.join(empty, "corpus"), exist_ok=True)
            from io import StringIO
            oldout, olderr = sys.stdout, sys.stderr
            sys.stdout = StringIO()
            sys.stderr = StringIO()
            try:
                rc2 = run(empty)
            finally:
                sys.stdout, sys.stderr = oldout, olderr
            checks.append(("missing_sources_exit2", rc2 == 2, "rc=%d want 2" % rc2))
        finally:
            shutil.rmtree(empty, ignore_errors=True)
    finally:
        shutil.rmtree(root, ignore_errors=True)

    failed = [c for c in checks if not c[1]]
    for name, ok, detail in checks:
        print("selftest %-20s %s%s" % (name, "PASS" if ok else "FAIL",
                                       "" if ok else " (%s)" % detail))
    if failed:
        print("MORI_SOURCE_DRIFT_SELFTEST: FAIL (%d/%d)" % (len(checks) - len(failed), len(checks)))
        return 1
    print("MORI_SOURCE_DRIFT_SELFTEST: PASS (%d cases)" % len(checks))
    return 0


def main(argv):
    if argv == ["--selftest"]:
        return _selftest()
    if len(argv) == 2 and argv[0] == "--root":
        root = argv[1]
        if not os.path.isdir(root):
            print("MORI_SOURCE_DRIFT_SETUP: %s is not a directory" % root,
                  file=sys.stderr)
            return 2
        return run(root)
    print("usage: %s --root DIR | --selftest" % os.path.basename(argv[0] if argv else __file__),
          file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
