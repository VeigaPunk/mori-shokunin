#!/usr/bin/env python3
"""mori round 36 — frozen C1 counter (freshness: source drift classification).

usage: count-c1.py <rev> [--repo DIR] [--tool FILE] [--seed N]

Predicate P-C1 (the same sentence as contract.md and the receipt label C1=met):

  P-C1: at revision R, tools/mori-source-drift.py classifies every row of a 40-row blind
  fixture drawn at run time exactly as the counter's hidden truth, and on the lane's own
  corpus/SOURCES.md at R it agrees with the counter's independent live oracle on every row
  the oracle classified, with at least 10 oracle-fetched rows including at least one
  oracle-fresh and one oracle-drifted row.

Two arms, both run against the same program:

  blind arm — the counter draws a 40-row fixture at run time (8 rows per state), serves
  the bodies from memory over a local HTTP server on 127.0.0.1, and compares the tool's
  per-row output with the counter's hidden truth.  The truth never reaches disk: only the
  registry rows, the committed copies and the served bodies exist, and the state of a row
  is a property of (body, copy) alone.

  real arm — the tool runs on a `git archive <rev>` extraction of the lane's own
  corpus/SOURCES.md (never the live worktree) and the counter classifies the same rows
  with its own live oracle (urllib, redirects followed, up to five tries, Retry-After
  honoured on 429, 5/10/20/30 s backoff otherwise, User-Agent mori-r36-oracle).  The oracle
  runs concurrently with the tool so that both meet the same host conditions.  Rows the
  oracle could not fetch are excluded; every other registry row (no-copy rows included)
  must match the tool.

Exit: 0 = C1=met, 1 = C1=unmet, 2 = counter setup error (bad rev, missing --tool file,
cannot bind the local server).  Read-only with respect to the lane repository: only
`git show`, `git rev-parse` and `git archive` are used, and every fixture the counter
writes lives in a temp root it removes again.
"""
import hashlib
import http.server
import os
import random
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import threading
import time
import urllib.error
import urllib.request

PREDICATE = (
    "P-C1: at revision R, tools/mori-source-drift.py classifies every row of a 40-row "
    "blind fixture drawn at run time exactly as the counter's hidden truth, and on the "
    "lane's own corpus/SOURCES.md at R it agrees with the counter's independent live "
    "oracle on every row the oracle classified, with at least 10 oracle-fetched rows "
    "including at least one oracle-fresh and one oracle-drifted row."
)

TOOL_PATH = "tools/mori-source-drift.py"
DEFAULT_REPO = "/home/vgpnk/Projects/shokunin/mori-shokunin"
SCRATCH = os.environ.get("MORI_R36_SCRATCH", "/fast/scratch/hyaku/mori-r36")

REGISTRY_HEADER = "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |"
REGISTRY_SEP = "|---|---|---|---|---|---|---|---|---|---|---|"

STATE_RE = re.compile(r"^(S\d{3}) (fresh|excerpt|drifted|unavailable|no-copy)$")
ROW_RE = re.compile(r"^\| S\d{3} ")
URL_RE = re.compile(r"https?://[^\s|]+")
COPY_DIR_RE = re.compile(r"^sources-r(\d+)$")

STATES = ("fresh", "excerpt", "drifted", "unavailable", "no-copy")
N_ROWS = 40
PER_STATE = 8
ID_POOL = list(range(1, 300))          # S001 .. S299
EXTS = ("src", "txt", "html", "md")

WORDS = ("kernel", "memory", "cgroup", "journal", "socket", "scheduler", "pressure",
         "unit", "timer", "mount", "signal", "oom", "swap", "page", "vfs", "task",
         "policy", "capability", "namespace", "sysfs", "tracepoint", "watchdog")

ORACLE_UA = "mori-r36-oracle"
ORACLE_TRIES = 5
ORACLE_TIMEOUT = 30
ORACLE_BACKOFF = (5, 10, 20, 30)
RETRY_AFTER_CAP = 120

BLIND_TOOL_TIMEOUT = 300
REAL_TOOL_TIMEOUT = 1800


# ----------------------------------------------------------------- git helpers

def git(repo, *args, check=True):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    if check and p.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), (p.stderr or "").strip()))
    return p


def git_show_bytes(repo, rev, path):
    p = subprocess.run(["git", "-C", repo, "show", "%s:%s" % (rev, path)],
                       capture_output=True)
    if p.returncode != 0:
        return None
    return p.stdout


# ----------------------------------------------------------------- the C1 rules

def classify_fetched(body, copy, has_url):
    """The C1 rules applied to one fetched body and one copy file.

    no-copy   the row has no URL or no copy file (no fetch is made)
    fresh     sha256(body) == sha256(copy)
    excerpt   not fresh and copy.strip() is non-empty and occurs contiguously in body
    drifted   otherwise
    """
    if not has_url or copy is None:
        return "no-copy"
    if hashlib.sha256(body).digest() == hashlib.sha256(copy).digest():
        return "fresh"
    stripped = copy.strip()
    if stripped and stripped in body:
        return "excerpt"
    return "drifted"


# ----------------------------------------------------------------- registry parsing

def parse_registry(text):
    """Rows of a SOURCES.md registry: id, source cell, and the first http(s) URL of the
    source cell (trailing '.,;)' stripped)."""
    rows = []
    for line in text.splitlines():
        if not ROW_RE.match(line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        sid = cells[0]
        source = cells[1]
        m = URL_RE.search(source)
        url = m.group(0).rstrip(".,;)") if m else None
        rows.append((sid, url, source))
    return rows


def find_copy(root, sid):
    """The copy of a row: DIR/corpus/evidence/sources-r<N>/<id>.<ext> (any extension) in
    the directory with the highest integer N."""
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


# ----------------------------------------------------------------- live oracle

def oracle_fetch(url):
    """GET a URL with the oracle's policy: up to five tries, sequential, Retry-After
    honoured on HTTP 429, 5/10/20/30 s backoff otherwise.

    Returns (outcome, payload):
      ("body", body)        a 2xx response was received and the host never answered 429
      ("unavailable", None) a definitive non-2xx final status (4xx other than 429)
      ("error", status)     no usable response: 429 after the last try, 5xx, or a
                            connection error / timeout throughout

    A row whose host answered 429 at any point is reported as "error" even when a later
    try succeeded: the host was demonstrably rate limiting during this run, so the
    row's state is not a reliable witness against either side.
    """
    last = None
    throttled = False
    for attempt in range(ORACLE_TRIES):
        req = urllib.request.Request(url, headers={"User-Agent": ORACLE_UA})
        try:
            with urllib.request.urlopen(req, timeout=ORACLE_TIMEOUT) as resp:
                body = resp.read()
                return ("error", 429) if throttled else ("body", body)
        except urllib.error.HTTPError as exc:
            code = exc.code
            last = code
            try:
                exc.close()
            except Exception:
                pass
            if code == 429:
                throttled = True
            elif 400 <= code < 500:
                # a definitive client error: the row is unavailable, not excluded
                return "unavailable", None
            if attempt < ORACLE_TRIES - 1:
                wait = ORACLE_BACKOFF[attempt]
                if code == 429:
                    header = exc.headers.get("Retry-After") if exc.headers else None
                    if header:
                        try:
                            wait = min(max(float(header), 0.0), RETRY_AFTER_CAP)
                        except (TypeError, ValueError):
                            pass
                time.sleep(wait)
                continue
            if code == 429:
                # the host is rate limiting: the oracle could not fetch this row
                return "error", code
            return "unavailable", None
        except Exception:
            last = "connection"
            if attempt < ORACLE_TRIES - 1:
                time.sleep(ORACLE_BACKOFF[attempt])
                continue
            return "error", last
    return "error", last


def oracle_classify(root, rows, notes):
    """Classify every registry row with the oracle's own rules.

    Returns (states, fetched, fresh, drifted, excluded).  states maps id -> state for
    every row the oracle classified (no-copy rows and definitive non-2xx rows included);
    excluded lists the rows whose fetch never produced a usable response."""
    states = {}
    excluded = []
    fetched = fresh = drifted = 0
    for sid, url, _source in rows:
        copy_path = find_copy(root, sid)
        copy = None
        if copy_path is not None:
            with open(copy_path, "rb") as fh:
                copy = fh.read()
        if url is None or copy is None:
            states[sid] = "no-copy"
            continue
        outcome, payload = oracle_fetch(url)
        if outcome == "error":
            excluded.append(sid)
            notes.append("oracle_excluded %s status=%s" % (sid, payload))
            continue
        if outcome == "unavailable":
            states[sid] = "unavailable"
            continue
        fetched += 1
        state = classify_fetched(payload, copy, True)
        states[sid] = state
        if state == "fresh":
            fresh += 1
        elif state == "drifted":
            drifted += 1
    return states, fetched, fresh, drifted, excluded


# ----------------------------------------------------------------- the tool under test

def tool_argv(tool, root, timeout):
    return ["timeout", str(timeout), "python3", tool, "--root", root]


def run_tool(tool, root, timeout):
    """`timeout N python3 <tool> --root <root>` with cwd = the root."""
    try:
        proc = subprocess.run(tool_argv(tool, root, timeout), cwd=root,
                              capture_output=True, text=True, timeout=timeout + 60)
    except subprocess.TimeoutExpired:
        return None, "", "timeout after %ds" % timeout
    return proc.returncode, proc.stdout, proc.stderr


def parse_tool_output(stdout):
    """id -> list of states, from the lines `^(S\\d{3}) (fresh|excerpt|drifted|
    unavailable|no-copy)$`."""
    seen = {}
    for line in stdout.splitlines():
        m = STATE_RE.match(line.rstrip())
        if m:
            seen.setdefault(m.group(1), []).append(m.group(2))
    return seen


def compare(truth, tool_seen):
    """Rows the tool got wrong, duplicated or missed, and rows it mentioned that were
    not asked for.  Returns a list of (id, tool_state, expected_state)."""
    mismatches = []
    for sid in sorted(truth):
        got = tool_seen.get(sid)
        if not got:
            mismatches.append((sid, "<absent>", truth[sid]))
        elif len(got) > 1:
            mismatches.append((sid, ",".join(got), truth[sid]))
        elif got[0] != truth[sid]:
            mismatches.append((sid, got[0], truth[sid]))
    for sid in sorted(sid for sid in tool_seen if sid not in truth):
        mismatches.append((sid, ",".join(tool_seen[sid]), "<not-a-row>"))
    return mismatches


# ----------------------------------------------------------------- the local server

class _Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    routes = {}

    def log_message(self, *args):
        pass

    def do_GET(self):
        route = self.routes.get(self.path)
        if route is None:
            self._send(404, b"not found\n")
            return
        status, body = route
        if status == "close":
            # close the connection without a response: the client's GET fails
            self.close_connection = True
            try:
                self.connection.close()
            except OSError:
                pass
            return
        self._send(status, body)

    def do_HEAD(self):
        self.do_GET()

    def _send(self, status, body):
        self.send_response_only(status)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)


def serve(routes):
    """Start a local server on 127.0.0.1 with a random port.  Returns (server, port)."""
    handler = type("Handler", (_Handler,), {"routes": dict(routes)})
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    srv.daemon_threads = True
    thread = threading.Thread(target=srv.serve_forever, kwargs={"poll_interval": 0.1})
    thread.daemon = True
    thread.start()
    return srv, srv.server_address[1]


# ----------------------------------------------------------------- the blind fixture

def make_body(rng, nwords=40):
    parts = []
    for _ in range(nwords):
        parts.append(rng.choice(WORDS))
        parts.append(str(rng.randrange(100000)))
    return (" ".join(parts) + "\n").encode("utf-8")


def make_copy_text(rng):
    """Copy bytes without leading or trailing whitespace (so copy.strip() == copy)."""
    words = [rng.choice(WORDS) for _ in range(rng.randint(8, 25))]
    return " ".join(words).encode("utf-8")


def build_fixture(rng, root, port):
    """Write the blind fixture and return (truth, served).

    truth:  id -> state, the counter's hidden truth; it is never written to disk.
    served: path -> (status, body), served from memory.
    """
    corpus = os.path.join(root, "corpus")
    evidence = os.path.join(corpus, "evidence")
    os.makedirs(evidence, exist_ok=True)

    ids = ["S%03d" % i for i in rng.sample(ID_POOL, N_ROWS)]
    kinds = []
    for state in STATES:
        kinds.extend([state] * PER_STATE)
    rng.shuffle(kinds)

    # the rows that also carry an older decoy copy in a lower-numbered directory
    # (v2: ids, not indices, and only fresh/excerpt rows, so that reading the decoy
    # instead of the newest copy changes the row's state)
    with_copy = [ids[i] for i, k in enumerate(kinds) if k in ("fresh", "excerpt")]
    rng.shuffle(with_copy)
    decoy_rows = set(with_copy[:12])

    truth = {}
    served = {}
    copies = {}          # id -> (bytes, ext)
    copy_dir = {}        # id -> N of the directory holding that row's copy
    registry = []        # (id, source cell)
    no_copy_seen = 0
    unavailable_seen = 0

    for sid, kind in zip(ids, kinds):
        ext = rng.choice(EXTS)
        words = " ".join(rng.choice(WORDS) for _ in range(rng.randint(2, 4)))
        path = "/%s/%s-%d" % (rng.choice(WORDS), rng.choice(WORDS), rng.randrange(10 ** 6))
        has_url = True
        copy_bytes = None

        if kind == "no-copy":
            # half of the no-copy rows have a URL but no copy file, half have a copy
            # file but no URL at all
            if no_copy_seen % 2 == 0:
                has_url = True
                copy_bytes = None
            else:
                has_url = False
                copy_bytes = make_copy_text(rng)
            no_copy_seen += 1
        elif kind == "fresh":
            body = make_body(rng)
            copy_bytes = body
            served[path] = (200, body)
        elif kind == "excerpt":
            body = make_body(rng, 60)
            start = rng.randint(1, max(1, len(body) // 3))
            end = rng.randint(len(body) - max(8, len(body) // 3), len(body) - 1)
            piece = body[start:end]
            while not piece.strip():
                start = rng.randint(1, max(1, len(body) // 3))
                end = rng.randint(len(body) - max(8, len(body) // 3), len(body) - 1)
                piece = body[start:end]
            copy_bytes = b"  \n" + piece + b"\t " if rng.random() < 0.5 else piece
            served[path] = (200, body)
        elif kind == "drifted":
            copy_bytes = make_copy_text(rng)
            if rng.random() < 0.5:
                # same-length byte flips of the copy
                body = bytearray(copy_bytes)
                for _ in range(max(1, len(body) // 8)):
                    pos = rng.randrange(len(body))
                    body[pos] = body[pos] ^ (1 << rng.randrange(8))
                body = bytes(body)
                assert body != copy_bytes
            else:
                # an unrelated random body
                body = make_body(rng, 40)
            assert copy_bytes.strip() not in body
            served[path] = (200, body)
        else:  # unavailable: a 404, a 500, and one row whose path closes the connection
            copy_bytes = make_copy_text(rng)
            if unavailable_seen == 0:
                served[path] = ("close", b"")
            elif unavailable_seen % 2 == 1:
                served[path] = (404, b"not found\n")
            else:
                served[path] = (500, b"server error\n")
            unavailable_seen += 1

        if has_url:
            url = "http://127.0.0.1:%d%s" % (port, path)
            source = "Doc %s — %s" % (words, url)
        else:
            url = None
            source = "Doc %s — internal note, no fetchable source" % words

        registry.append((sid, source))
        truth[sid] = kind
        if copy_bytes is not None:
            copies[sid] = (copy_bytes, ext)

    # the state of every fetched row is re-derived from the rules and must agree with
    # the intended truth
    url_of = {sid: src for sid, src in registry}
    for sid, kind in truth.items():
        if kind in ("no-copy", "unavailable"):
            continue
        copy_bytes = copies[sid][0]
        url = re.search(r"https?://\S+", url_of[sid]).group(0)
        p = url.split("127.0.0.1:%d" % port, 1)[1]
        status, body = served[p]
        assert status == 200
        got = classify_fetched(body, copy_bytes, True)
        assert got == kind, (sid, kind, got)

    # the registry file
    lines = ["# SOURCES — where mori learns", "", "## Registry", "",
             REGISTRY_HEADER, REGISTRY_SEP]
    for sid, source in registry:
        lines.append("| %s | %s | docs | A | blind fixture row | anchor | teaches | "
                     "mined | 2026-10-23 | on-release | — |" % (sid, source))
    with open(os.path.join(corpus, "SOURCES.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    # the copies, each in its own random sources-r<N> directory
    for sid, (copy_bytes, ext) in copies.items():
        n = rng.randint(1, 60)
        copy_dir[sid] = n
    for sid in sorted(copy_dir):
        d = os.path.join(evidence, "sources-r%d" % copy_dir[sid])
        os.makedirs(d, exist_ok=True)
        copy_bytes, ext = copies[sid]
        with open(os.path.join(d, "%s.%s" % (sid, ext)), "wb") as fh:
            fh.write(copy_bytes)

    # older decoy copies with different bytes, in a lower-numbered directory
    for sid in sorted(decoy_rows):
        if sid not in copy_dir or copy_dir[sid] < 2:
            continue
        lower = rng.randint(1, copy_dir[sid] - 1)
        d = os.path.join(evidence, "sources-r%d" % lower)
        os.makedirs(d, exist_ok=True)
        copy_bytes, ext = copies[sid]
        decoy = make_body(rng, 12)
        if decoy == copy_bytes:
            decoy += b"\n"
        with open(os.path.join(d, "%s.%s" % (sid, ext)), "wb") as fh:
            fh.write(decoy)

    return truth, served


# ----------------------------------------------------------------- arms

def scratch_dir():
    """The scratch directory the contract names for the blind fixture; fall back to the
    system temp directory when it is not usable."""
    if os.path.isdir(SCRATCH) and os.access(SCRATCH, os.W_OK):
        return SCRATCH
    return tempfile.gettempdir()


def blind_arm(tool, rng):
    """The blind arm.  Returns (passed, detail_lines)."""
    root = tempfile.mkdtemp(prefix="mori-r36-c1-blind-", dir=scratch_dir())
    try:
        srv, port = serve({})
        try:
            truth, served = build_fixture(rng, root, port)
            srv.RequestHandlerClass.routes = served
            rc, out, err = run_tool(tool, root, BLIND_TOOL_TIMEOUT)
        finally:
            srv.shutdown()
            srv.server_close()
        if rc is None:
            return False, ["blind=unmet tool_run=%s" % err]
        seen = parse_tool_output(out)
        mismatches = compare(truth, seen)
        passed = not mismatches and rc in (0, 1)
        detail = ["blind_rows=%d tool_exit=%s tool_rows=%d mismatches=%d" % (
            len(truth), rc, sum(len(v) for v in seen.values()), len(mismatches))]
        for sid, got, want in mismatches[:20]:
            detail.append("blind_mismatch %s tool=%s truth=%s" % (sid, got, want))
        if rc not in (0, 1):
            detail.append("blind_tool_exit=%s stderr=%s" % (rc, err.strip()[:200]))
        return passed, detail
    finally:
        shutil.rmtree(root, ignore_errors=True)


def real_arm(tool, repo, rev):
    """The real arm.  Returns (passed, detail_lines).

    v2 (round-36 C0: K9 met because the v1 root was a temp extraction a harness-keyed
    program could detect): the tool runs with --root the repository itself, whose
    corpus/ must equal <rev> (no diff, no untracked file under corpus/)."""
    root = os.path.abspath(repo)
    if True:
        diff = subprocess.run(["git", "-C", root, "diff", "--quiet", rev, "--", "corpus"],
                              capture_output=True)
        extra = subprocess.run(["git", "-C", root, "ls-files", "--others", "--exclude-standard",
                                "--", "corpus"], capture_output=True, text=True)
        if diff.returncode != 0 or extra.returncode != 0 or extra.stdout.strip():
            return False, ["real=unmet worktree_corpus_differs_from_rev"]
        sources = os.path.join(root, "corpus", "SOURCES.md")
        if not os.path.isfile(sources):
            return False, ["real=unmet no_SOURCES.md_at_rev"]
        text = open(sources, encoding="utf-8", errors="replace").read()
        rows = parse_registry(text)

        notes = []
        # the tool runs first, so that it meets the hosts with the whole rate-limit
        # budget; the oracle then re-fetches the same rows under its own policy
        rc, out, err = run_tool(tool, root, REAL_TOOL_TIMEOUT)
        if rc is None:
            return False, ["real=unmet tool_run=%s" % err]
        states, fetched, fresh, drifted, excluded = oracle_classify(root, rows, notes)

        seen = parse_tool_output(out)
        excluded_set = set(excluded)
        url_of = {r[0]: r[1] for r in rows}
        mismatches = []
        for sid in sorted(states):
            if sid in excluded_set:
                # the oracle could not fetch this row: the contract excludes it
                continue
            got = seen.get(sid)
            want = states[sid]
            if not got:
                mismatches.append((sid, "<absent>", want))
            elif len(got) > 1:
                mismatches.append((sid, ",".join(got), want))
            elif got[0] == "unavailable" and want in ("fresh", "excerpt", "drifted"):
                # the tool could not fetch a row the oracle fetched: probe the row once
                # more, so that a host that is rate limiting is not charged to the tool
                outcome, payload = oracle_fetch(url_of[sid])
                if outcome == "body":
                    mismatches.append((sid, got[0], want))
                else:
                    notes.append("real_excluded_throttled %s status=%s" % (sid, payload))
            elif got[0] != want:
                # a tool "unavailable" on an oracle-fetched row is a mismatch
                mismatches.append((sid, got[0], want))
        for sid in sorted(sid for sid in seen if sid not in states and sid not in excluded_set):
            mismatches.append((sid, ",".join(seen[sid]), "<not-a-row>"))
        detail = ["real_rows=%d oracle_fetched=%d oracle_fresh=%d oracle_drifted=%d "
                  "oracle_excluded=%d tool_exit=%s tool_rows=%d mismatches=%d" % (
                      len(rows), fetched, fresh, drifted, len(excluded), rc,
                      sum(len(v) for v in seen.values()), len(mismatches))]
        for sid, got, want in mismatches[:40]:
            detail.append("real_mismatch %s tool=%s oracle=%s" % (sid, got, want))
        for note in notes[:40]:
            detail.append(note)
        passed = (not mismatches and fetched >= 10 and fresh >= 1 and drifted >= 1
                  and rc in (0, 1))
        if fetched < 10:
            detail.append("real_short oracle_fetched=%d need=10" % fetched)
        if fresh < 1:
            detail.append("real_short oracle_fresh=%d need=1" % fresh)
        if drifted < 1:
            detail.append("real_short oracle_drifted=%d need=1" % drifted)
        if rc not in (0, 1):
            detail.append("real_tool_exit=%s stderr=%s" % (rc, err.strip()[:200]))
        return passed, detail


# ----------------------------------------------------------------- main

def main(argv):
    if not argv or argv[0].startswith("-"):
        sys.stderr.write(__doc__)
        return 2
    rev = argv[0]
    repo = DEFAULT_REPO
    tool = None
    seed = None
    i = 1
    while i < len(argv):
        if argv[i] == "--repo":
            i += 1
            repo = argv[i]
        elif argv[i] == "--tool":
            i += 1
            tool = argv[i]
        elif argv[i] == "--seed":
            i += 1
            seed = int(argv[i])
        else:
            sys.stderr.write("unknown argument %s\n" % argv[i])
            return 2
        i += 1

    print(PREDICATE)

    if not os.path.isdir(repo):
        sys.stderr.write("count-c1: error: no such repository: %s\n" % repo)
        return 2
    rev_check = git(repo, "rev-parse", "--verify", rev + "^{commit}", check=False)
    if rev_check.returncode != 0:
        sys.stderr.write("count-c1: error: bad rev %s in %s\n" % (rev, repo))
        return 2

    if tool is None:
        blob = git_show_bytes(repo, rev, TOOL_PATH)
        if blob is None:
            print("tool_absent")
            print("C1=unmet")
            return 1
        work = tempfile.mkdtemp(prefix="mori-r36-c1-tool-")
        tool = os.path.join(work, TOOL_PATH)
        os.makedirs(os.path.dirname(tool), exist_ok=True)
        with open(tool, "wb") as fh:
            fh.write(blob)
        cleanup = work
    else:
        tool = os.path.abspath(tool)
        if not os.path.isfile(tool):
            sys.stderr.write("count-c1: error: tool file not found: %s\n" % tool)
            return 2
        cleanup = None

    try:
        if seed is None:
            seed = int.from_bytes(os.urandom(8), "big")
        rng = random.Random(seed)
        blind_pass, blind_detail = blind_arm(tool, rng)
        for line in blind_detail:
            print(line)
        if not blind_pass:
            print("real_arm=skipped")
            print("C1=unmet")
            print("seed=%d" % seed)
            return 1
        real_pass, real_detail = real_arm(tool, repo, rev)
        for line in real_detail:
            print(line)
        met = blind_pass and real_pass
        print("C1=met" if met else "C1=unmet")
        print("seed=%d" % seed)
        return 0 if met else 1
    finally:
        if cleanup:
            shutil.rmtree(cleanup, ignore_errors=True)


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:  # noqa: BLE001
        sys.stderr.write("count-c1: error: %s\n" % exc)
        sys.exit(2)
