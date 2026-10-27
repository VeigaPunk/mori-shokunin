#!/usr/bin/env python3
"""Round 54 C1 counter (freshness) — the lane's remaining v7.2-pinned located-quote claims re-verified at Linux v7.3.

Round 53 re-verified the claim tables of two entries (46 rows). Every other claim|source|quote row the lane holds
whose source row pins Linux tag v7.2 was left at v7.2 (`SCORECARD.md` `Planned (round 54)`: "the v7.3 trigger for
what D does not cover"). This counter takes all of them.

Frozen predicate P-C1 (same sentence in contract.md, this counter and the receipt label):
  At revision R, corpus/knowledge/kernel-v7.3-recheck-r54.md opens with source:, verified-at: and recheck: lines
  and carries one table whose header cells are h, entry, status, source, line, quote, disposition, holding exactly
  one row for each hash of the frozen scope set D and no other row; D is the set of claim rows, read at the
  entering tip 39dcf4d7e410d362781a47e8365ca23b5c807598, of the claim|source|quote tables of every
  corpus/knowledge/*.md entry whose source row's URL names Linux tag v7.2 (raw.githubusercontent.com
  torvalds/linux/v7.2/, cgit plain ?h=v7.2, cdn.jsdelivr.net torvalds/linux@v7.2/, docs.kernel.org/7.2/), minus
  the hashes already in the round-53 ledger corpus/knowledge/kernel-v7.3-recheck-r53.md at that tip; each row's
  entry cell names the entry holding that hash; its status cell equals this counter's own derivation — `held`
  when the row's v7.2 quote occurs (whitespace collapsed; HTML copies with tags removed and entities decoded) in
  the committed v7.3 copy of the same path, else `absent`; its source cell is one S-id naming a corpus/SOURCES.md
  row at R that is mined, opened 2026-10-26 or 2026-10-27, carries the frozen v7.3 URL of that path and lists the
  recheck entry in used-by; its line cell is a line number of that v7.3 copy on which an occurrence of the row's
  quote begins; its quote cell is one backticked span of 6 to 25 words (an escaped \\| reads as |) that occurs in
  that v7.3 copy and equals the v7.2 quote when the status is held; its disposition cell is `holds` or `changed`;
  every committed v7.3 copy matches its frozen sha256; and (vote arm) for every row at least 2 distinct RECHECK
  voters' final unfenced line `RECHECK <h> <word>` in their own report .ufo/waves/round-54/w1/<voter>.md at R
  carries the row's disposition, and no RECHECK voter's final line for that hash carries the other word; a voter
  counts only when .ufo/waves/round-54/w1-results.json at R (the orchestrator's settlement record) lists a result
  whose name is that voter; a voter's line does not count for a row whose quote that voter proposed (an unfenced
  `QUOTE <h> :: <text>` line in its report whose text equals the row's quote); the RECHECK voters are exactly the
  frozen VOTERS list below.

Usage: count-c1.py <rev> [--repo DIR]   |   count-c1.py --selftest   |   count-c1.py --scope
Output: `C1=met|unmet scope=N rows=N matched=N status_ok=N line_ok=N quote_ok=N source_rows=ok|bad pins=ok|bad
  provenance=ok|bad held=N absent=N holds=N changed=N voted=N dissent=N rev=R` (+ `failed=` list when unmet).
Exit 0 met, 1 unmet, 2 setup. Read-only: `git show` / `git ls-tree` / `git rev-parse` only.

Limits (named before data): `held` proves the v7.2 quote's words still occur in the v7.3 file; the line arm proves
the ledger names a line where they begin, not that the surrounding code means the same — the disposition and its
votes carry the meaning; votes are seats of the lane, not outside verification, and the results-file binding
proves the orchestrator recorded a seat of that name, not who wrote the file's bytes; D covers claim|source|quote
tables only (not prose, not oom-tracepoints-r47's catalogue, not system-pressure-r24's anchors); the v7.3 copies
were fetched from git.kernel.org cgit (docs.kernel.org for the rendered cgroup page) and their sha256 pins prove
they are the bytes fetched, not that the server served the tag.
"""
import hashlib
import html
import json
import os
import re
import subprocess
import sys

ENTERING = "39dcf4d7e410d362781a47e8365ca23b5c807598"
LEDGER = "corpus/knowledge/kernel-v7.3-recheck-r54.md"
R53_LEDGER = "corpus/knowledge/kernel-v7.3-recheck-r53.md"
KNOWLEDGE = "corpus/knowledge/"
SRC_DIR = "corpus/evidence/sources-r54/"
R53_DIR = "corpus/evidence/sources-r53/"
VOTE_DIR = ".ufo/waves/round-54/w1/"
RESULTS = ".ufo/waves/round-54/w1-results.json"
VOTERS = ["Mo54Rc%02d" % i for i in range(1, 13)]
MIN_VOTES = 2
OPENED = ("2026-10-26", "2026-10-27")
MIN_WORDS, MAX_WORDS = 6, 25
CGIT = "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/"
DOCS = "docs:"
# path key -> (committed v7.3 copy, sha256 of the copy fetched 2026-10-26/27, kind)
_COPIES = {
    "mm/memcontrol.c": (SRC_DIR + "memcontrol.c.v7.3",
                        "bdb6159cc2378c44c356b6788f521812f15c4d4936e8b09c66ef70b56bcc41a1", "text"),
    "mm/oom_kill.c": (SRC_DIR + "oom_kill.c.v7.3",
                      "452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e", "text"),
    "lib/percpu_counter.c": (SRC_DIR + "percpu_counter.c.v7.3",
                             "2c26e67751f939dfb21ff6221884280ae84a2a94a54de4468fb9dc8746130d6d", "text"),
    "include/linux/percpu_counter.h": (SRC_DIR + "percpu_counter.h.v7.3",
                                       "4a107bc381b3b5425b8ff441f7487d97ba6883dc6f5b426c4bd361ad7cbef896", "text"),
    "include/uapi/asm-generic/errno.h": (SRC_DIR + "errno.h.v7.3",
                                         "66a5ad60566fdd62e41701bcfc42bfeca5e5696ad1d47d78981575e0c51622be", "text"),
    "mm/util.c": (R53_DIR + "util.c.v7.3",
                  "4dfcce2b8fa8f18c350565950a10248b3590e3d3c0c9335fef6d47daa7a9e1f2", "text"),
    "mm/mm_init.c": (R53_DIR + "mm_init.c.v7.3",
                     "678410005f881a64ae94d180c82174dc4474679b056ace69b6bc3d23978f976c", "text"),
    DOCS + "admin-guide/cgroup-v2.html": (SRC_DIR + "cgroup-v2.7.3.html",
                                          "b478c1bae99899df476d6b4989cbb516f7ca93c5f009cdff64b802bbc24f3d4b", "html"),
}


def _v73_url(key):
    if key.startswith(DOCS):
        return "https://docs.kernel.org/7.3/" + key[len(DOCS):]
    return CGIT + key + "?h=v7.3"


V73 = {k: (c, d, _v73_url(k), kind) for k, (c, d, kind) in _COPIES.items()}
HEADER = ["h", "entry", "status", "source", "line", "quote", "disposition"]
SPAN = re.compile(r"`([^`]+)`")
RECHECK_RE = re.compile(r"^\s*RECHECK\s+([0-9a-f]{12})\s+(holds|changed)\b")
QUOTE_RE = re.compile(r"^\s*QUOTE\s+([0-9a-f]{12})\s+::\s+(.+?)\s*$")
V72_RES = [
    re.compile(r"raw\.githubusercontent\.com/torvalds/linux/v7\.2/(\S+?)(?=[\s)>\]`]|$)"),
    re.compile(r"git\.kernel\.org/pub/scm/linux/kernel/git/torvalds/linux\.git/plain/(\S+?)\?h=v7\.2(?=[\s)>\]`&]|$)"),
    re.compile(r"cdn\.jsdelivr\.net/gh/torvalds/linux@v7\.2/(\S+?)(?=[\s)>\]`]|$)"),
]
DOCS72_RE = re.compile(r"docs\.kernel\.org/7\.2/(\S+?)(?=[\s)>\]`]|$)")
TOKEN_RE = re.compile(r"<(script|style)\b.*?</\1\s*>|<!--.*?-->|<[^>]+>|&(?:#[0-9]+|#[xX][0-9a-fA-F]+|[A-Za-z][A-Za-z0-9]*);?",
                      re.S | re.I)


def split_cells(line):
    s = line.strip()
    parts = re.split(r"(?<!\\)\|", s)
    parts = parts[1:-1] if s.endswith("|") else parts[1:]
    return [p.strip() for p in parts]


def ws(text):
    return re.sub(r"\s+", " ", text).strip()


def claim_hash(claim):
    return hashlib.sha256(ws(claim).encode("utf-8")).hexdigest()[:12]


def norm_map(raw, kind):
    """Whitespace-collapsed text of a copy and, per character, the offset in `raw` it came from.
    HTML: script/style blocks, comments and tags read as one space; entities are decoded."""
    chars, offs = [], []
    if kind == "html":
        pos = 0
        for m in TOKEN_RE.finditer(raw):
            for i in range(pos, m.start()):
                chars.append(raw[i]); offs.append(i)
            tok = m.group(0)
            rep = html.unescape(tok) if tok.startswith("&") else " "
            for ch in rep:
                chars.append(ch); offs.append(m.start())
            pos = m.end()
        for i in range(pos, len(raw)):
            chars.append(raw[i]); offs.append(i)
    else:
        chars, offs = list(raw), list(range(len(raw)))
    out, out_offs, in_ws = [], [], False
    for ch, o in zip(chars, offs):
        if ch.isspace():
            if not in_ws:
                out.append(" "); out_offs.append(o)
            in_ws = True
        else:
            out.append(ch); out_offs.append(o)
            in_ws = False
    return "".join(out), out_offs


def lines_of(raw, text, offs, q):
    found, start = set(), 0
    while q:
        i = text.find(q, start)
        if i < 0:
            break
        found.add(raw.count("\n", 0, offs[i]) + 1)
        start = i + 1
    return found


def parse_table(text, header):
    rows, found, fence = [], False, False
    for line in text.split("\n"):
        if line.lstrip()[:3] in ("```", "~~~"):
            fence = not fence
            continue
        if fence:
            continue
        if not line.lstrip().startswith("|"):
            if found and rows:
                break
            continue
        cells = split_cells(line)
        if not found:
            if [c.lower() for c in cells] == header:
                found = True
            continue
        if all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
            continue
        rows.append(cells)
    return found, rows


def sources_row(src_text, row_id):
    for line in src_text.split("\n"):
        if re.match(r"^ {0,3}\|\s*%s\s*\|" % re.escape(row_id), line):
            return split_cells(line)
    return None


def one_quote(cell):
    spans = SPAN.findall(cell)
    if len(spans) != 1:
        return None
    return ws(spans[0].replace("\\|", "|"))


def v72_key(url_cell):
    for rx in V72_RES:
        m = rx.search(url_cell)
        if m:
            return m.group(1)
    m = DOCS72_RE.search(url_cell)
    if m:
        return DOCS + m.group(1)
    return None


def scope(read_entering, ls_entering):
    """Frozen scope D: hash -> (entry, path key, v7.2 quote). Read at the entering tip only."""
    src = read_entering("corpus/SOURCES.md") or ""
    _, done_rows = parse_table(read_entering(R53_LEDGER) or "", ["h", "entry", "status", "source", "quote", "disposition"])
    done = set(r[0].strip("` ") for r in done_rows if r)
    d = {}
    entries = sorted(p for p in (ls_entering(KNOWLEDGE) or []) if p.endswith(".md"))
    for entry in entries:
        _, rows = parse_table(read_entering(entry) or "", ["claim", "source", "quote"])
        for cells in rows:
            if len(cells) != 3:
                continue
            srow = sources_row(src, cells[1].strip("` "))
            if not srow or len(srow) < 2:
                continue
            key = v72_key(srow[1])
            if key is None:
                continue
            q = one_quote(cells[2])
            h = claim_hash(cells[0])
            if q is None or h in done:
                continue
            d[h] = (entry, key, q)
    return d


def final_votes(read, ls):
    """hash -> {voter: last word}; proposed: voter -> {hash: set of quote texts}; voters bound to the results file."""
    votes, proposed = {}, {}
    present = set(ls(VOTE_DIR) or [])
    settled = set()
    try:
        res = json.loads(read(RESULTS) or "null")
        for r in (res or {}).get("results", []) if isinstance(res, dict) else []:
            if isinstance(r, dict) and isinstance(r.get("name"), str):
                settled.add(r["name"])
    except (ValueError, TypeError, AttributeError):
        settled = set()
    for voter in VOTERS:
        path = VOTE_DIR + voter + ".md"
        if path not in present or voter not in settled:
            continue
        fence = False
        for line in (read(path) or "").split("\n"):
            if line.lstrip()[:3] in ("```", "~~~"):
                fence = not fence
                continue
            if fence:
                continue
            m = RECHECK_RE.match(line)
            if m:
                votes.setdefault(m.group(1), {})[voter] = m.group(2)
            q = QUOTE_RE.match(line)
            if q:
                proposed.setdefault(voter, {}).setdefault(q.group(1), set()).add(ws(q.group(2).strip("`")))
    return votes, proposed


def evaluate(read, rev, d, ls=None):
    failed = []
    norm, pins_ok = {}, True
    for key, (copy, digest, url, kind) in V73.items():
        b = read(copy)
        if b is None or hashlib.sha256(b.encode("utf-8", "surrogateescape")).hexdigest() != digest:
            pins_ok = False
        raw = b or ""
        text, offs = norm_map(raw, kind)
        norm[key] = (raw, text, offs)
    if not pins_ok:
        failed.append("pins")
    if any(key not in V73 for (_e, key, _q) in d.values()):
        failed.append("scope_path_without_copy")
    votes, proposed = final_votes(read, ls or (lambda _d: []))
    c = dict(rows=0, matched=0, status_ok=0, line_ok=0, quote_ok=0, held=0, absent=0, holds=0, changed=0, voted=0,
             dissent=0)
    prov, srows = "bad", "bad"
    ledger = read(LEDGER)
    if ledger is None:
        failed.append("ledger_absent")
    else:
        head = [l for l in ledger.split("\n") if l.strip()][:20]
        has = lambda k: any(re.match(r"^[-* ]*%s\s*:" % k, l) for l in head)
        cited = set()
        for l in head:
            if re.match(r"^[-* ]*source\s*:", l):
                cited |= set(re.findall(r"\bS[0-9]{3,}\b", l))
        found, rows = parse_table(ledger, HEADER)
        if not found:
            failed.append("table")
        src_text = read("corpus/SOURCES.md") or ""
        seen, bad, ids, row_cache = set(), 0, set(), {}
        for cells in rows:
            c["rows"] += 1
            if len(cells) != 7:
                bad += 1
                continue
            h, entry, status, sid, lcell, qcell, disp = cells
            h = h.strip("` ")
            if h not in d or h in seen:
                bad += 1
                continue
            seen.add(h)
            c["matched"] += 1
            d_entry, key, q72 = d[h]
            if entry.strip("` ") != d_entry:
                bad += 1
            if key not in norm:
                bad += 1
                continue
            raw, text, offs = norm[key]
            derived = "held" if q72 in text else "absent"
            c[derived] += 1
            if status == derived:
                c["status_ok"] += 1
            q = one_quote(qcell)
            if (q is not None and MIN_WORDS <= len(q.split(" ")) <= MAX_WORDS and q in text
                    and (derived != "held" or q == q72)):
                c["quote_ok"] += 1
            lv = lcell.strip("` ")
            if q is not None and re.fullmatch(r"[1-9][0-9]*", lv) and int(lv) in lines_of(raw, text, offs, q):
                c["line_ok"] += 1
            sid = sid.strip("` ")
            if sid not in row_cache:
                row_cache[sid] = sources_row(src_text, sid) if re.fullmatch(r"S[0-9]{3,}", sid) else None
            srow = row_cache[sid]
            ok_row = bool(srow and len(srow) == 11 and V73[key][2] in srow[1] and srow[7] == "mined"
                          and srow[8] in OPENED and LEDGER in [u.strip() for u in re.split(r"[,;]", srow[10])])
            if not ok_row:
                bad += 1
            else:
                ids.add(sid)
            if disp not in ("holds", "changed"):
                bad += 1
                continue
            c[disp] += 1
            v = votes.get(h, {})
            agree = [w for w, word in v.items() if word == disp and q not in proposed.get(w, {}).get(h, set())]
            if any(word != disp for word in v.values()):
                c["dissent"] += 1
            elif len(agree) >= MIN_VOTES:
                c["voted"] += 1
        if c["matched"] != len(d) or c["rows"] != len(d):
            failed.append("rows")
        if bad:
            failed.append("bad_rows")
        if c["status_ok"] != len(d):
            failed.append("status")
        if c["line_ok"] != len(d):
            failed.append("line")
        if c["quote_ok"] != len(d):
            failed.append("quote")
        if c["dissent"] or c["voted"] != len(d):
            failed.append("votes")
        if has("source") and has("verified-at") and has("recheck") and ids and ids <= cited:
            prov = "ok"
        else:
            failed.append("provenance")
        srows = "ok" if ids and not bad else "bad"
    met = not failed and len(d) > 0
    line = ("C1=%s scope=%d rows=%d matched=%d status_ok=%d line_ok=%d quote_ok=%d source_rows=%s pins=%s "
            "provenance=%s held=%d absent=%d holds=%d changed=%d voted=%d dissent=%d rev=%s"
            % ("met" if met else "unmet", len(d), c["rows"], c["matched"], c["status_ok"], c["line_ok"],
               c["quote_ok"], srows, "ok" if pins_ok else "bad", prov, c["held"], c["absent"], c["holds"],
               c["changed"], c["voted"], c["dissent"], rev))
    if failed:
        line += " failed=" + ",".join(sorted(set(failed)))
    return met, line


def git_reader(repo, rev):
    def read(path):
        p = subprocess.run(["git", "-C", repo, "show", "%s:%s" % (rev, path)],
                           stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=60)
        return p.stdout.decode("utf-8", "surrogateescape") if p.returncode == 0 else None
    return read


def git_lister(repo, rev):
    def ls(dirname):
        p = subprocess.run(["git", "-C", repo, "ls-tree", "--name-only", rev, dirname],
                           stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=60)
        return p.stdout.decode("utf-8", "surrogateescape").split("\n") if p.returncode == 0 else []
    return ls


def lane_root():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def main(argv):
    if argv == ["--selftest"]:
        return selftest()
    args = list(argv)
    repo = lane_root()
    while "--repo" in args:
        i = args.index("--repo")
        repo = args[i + 1]
        del args[i:i + 2]
    if args == ["--scope"]:
        d = scope(git_reader(repo, ENTERING), git_lister(repo, ENTERING))
        for h, (entry, key, q) in sorted(d.items(), key=lambda kv: (kv[1][0], kv[1][1], kv[0])):
            print("h=%s entry=%s path=%s quote=%s" % (h, entry, key, q))
        print("scope=%d" % len(d))
        return 0 if d else 2
    if len(args) != 1 or args[0].startswith("-"):
        print("C1_SETUP usage: count-c1.py <rev> [--repo DIR] | --selftest | --scope", file=sys.stderr)
        return 2
    try:
        full = subprocess.run(["git", "-C", repo, "rev-parse", "--verify", args[0] + "^{commit}"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60,
                              check=True).stdout.decode().strip()
    except (subprocess.SubprocessError, OSError):
        print("C1_SETUP unresolvable revision %s" % args[0], file=sys.stderr)
        return 2
    d = scope(git_reader(repo, ENTERING), git_lister(repo, ENTERING))
    if not d:
        print("C1_SETUP empty scope at entering tip %s" % ENTERING, file=sys.stderr)
        return 2
    met, line = evaluate(git_reader(repo, full), full, d, ls=git_lister(repo, full))
    print(line)
    return 0 if met else 1


def selftest():
    """In-memory fixtures over the committed v7.3 copies; asserts verdict and the named failure for each arm."""
    lane = lane_root()
    files = {}
    for key, (copy, digest, url, kind) in V73.items():
        with open(os.path.join(lane, copy), "rb") as f:
            files[copy] = f.read().decode("utf-8", "surrogateescape")
    nm = {k: norm_map(files[V73[k][0]], V73[k][3]) for k in V73}

    def words_at(key, needle, n):
        t = nm[key][0]
        i = t.index(needle)
        return ws(" ".join(t[i:].split(" ")[:n]))

    def line_at(key, q):
        raw = files[V73[key][0]]
        return min(lines_of(raw, nm[key][0], nm[key][1], q))

    e1, e2, e3 = KNOWLEDGE + "oom-memcg-stat-r50.md", KNOWLEDGE + "commit-runway-read-r53.md", KNOWLEDGE + "q-r48.md"
    q_mc = words_at("mm/memcontrol.c", 'pr_info("memory: usage %llukB, limit %llukB, failcnt %lu\\n",', 6)
    q_ok = words_at("mm/oom_kill.c", "/* one line summary of the oom killer context. */", 9)
    q_html = words_at(DOCS + "admin-guide/cgroup-v2.html", "All memory amounts are in bytes.", 12)
    gone_q = "pr_info(\"memory: usage %llukB, limit %llukB, fail count %lu\\n\","
    new_q = words_at("mm/memcontrol.c", 'pr_info("swap: usage %llukB, limit %llukB, failcnt %lu\\n",', 6)
    d = {
        "aaaaaaaaaaa1": (e1, "mm/memcontrol.c", q_mc),
        "aaaaaaaaaaa2": (e1, "mm/oom_kill.c", q_ok),
        "aaaaaaaaaaa3": (e1, DOCS + "admin-guide/cgroup-v2.html", q_html),
        "aaaaaaaaaaa4": (e2, "mm/memcontrol.c", gone_q),
    }
    sids = {k: "S9%02d" % (n + 1) for n, k in enumerate(V73)}

    def srow(key, status="mined", opened="2026-10-27", used=LEDGER, url=None, indent=""):
        return ("%s| %s | title — %s | code | A | scope | anchor v7.3 | teaches | %s | %s | on-release | %s |"
                % (indent, sids[key], url or V73[key][2], status, opened, used))

    def default_rows():
        out = []
        for h, (entry, key, q72) in sorted(d.items()):
            st = "held" if q72 in nm[key][0] else "absent"
            q = q72 if st == "held" else new_q
            out.append([h, entry, st, sids[key], str(line_at(key, q)), "`%s`" % q.replace("|", "\\|"), "holds"])
        return out

    def results(names):
        return json.dumps({"lane": "mori", "round": 54, "wave": "w1",
                           "results": [{"name": n, "agent": "reviewer", "output": "x"} for n in names]})

    def build(rows=None, src_kw=None, votes="all", prov=True, extra_files=None, settled=None):
        rows = default_rows() if rows is None else rows
        table = ["| h | entry | status | source | line | quote | disposition |", "|---|---|---|---|---|---|---|"]
        table += ["| " + " | ".join(r) + " |" for r in rows]
        head = (["source: " + ", ".join(sorted(set(sids.values()))), "verified-at: 2026-10-27",
                 "recheck: on-release — count-c1.py"] if prov else ["verified-at: 2026-10-27"])
        fl = dict(files)
        fl[LEDGER] = "\n".join(["# Recheck at v7.3", ""] + head + ["", "## Ledger", ""] + table + [""])
        kw = src_kw or {}
        fl["corpus/SOURCES.md"] = "\n".join(["| id | source |", "|---|---|"] + [srow(k, **kw) for k in V73])
        if votes == "all":
            for v in ("Mo54Rc01", "Mo54Rc07"):
                fl[VOTE_DIR + v + ".md"] = "\n".join("RECHECK %s %s — row" % (r[0], r[6]) for r in rows) + "\n"
        elif votes is not None:
            fl.update(votes(rows))
        fl[RESULTS] = results(VOTERS if settled is None else settled)
        fl.update(extra_files or {})
        return fl

    def run(fl, scope_d=None):
        lister = lambda dn: [p for p in fl if p.startswith(dn) and "/" not in p[len(dn):]]
        return evaluate(lambda p: fl.get(p), "R", d if scope_d is None else scope_d, ls=lister)

    checks = []

    def check(name, cond):
        checks.append((name, bool(cond)))

    met, line = run(build())
    check("honest_met", met and "scope=4 rows=4 matched=4 status_ok=4 line_ok=4 quote_ok=4" in line
          and "held=3 absent=1" in line and "voted=4 dissent=0" in line)
    met, line = run({k: v for k, v in build().items() if k != LEDGER})
    check("ledger_absent_unmet", (not met) and "ledger_absent" in line)
    fl = build()
    fl[LEDGER] = "# staged\n\nsource: S901\nverified-at: x\nrecheck: y\n\nnothing yet\n"
    met, line = run(fl)
    check("no_table_unmet", (not met) and "table" in line and "rows" in line)
    fl = build()
    fl[LEDGER] = fl[LEDGER].replace("| h | entry | status | source | line | quote | disposition |",
                                    "| h | entry | status | source | quote | disposition |")
    met, line = run(fl)
    check("r53_header_unmet", (not met) and "table" in line)
    met, line = run(build(rows=default_rows()[:-1]))
    check("missing_row_unmet", (not met) and "rows" in line)
    rows = default_rows() + [["bbbbbbbbbbb9", e1, "held", sids["mm/oom_kill.c"], "1", "`%s`" % q_ok, "holds"]]
    met, line = run(build(rows=rows))
    check("extra_row_unmet", (not met) and "rows" in line and "bad_rows" in line)
    met, line = run(build(rows=default_rows() + [list(default_rows()[0])]))
    check("duplicate_row_unmet", (not met) and "bad_rows" in line)
    rows = default_rows()
    rows[3][2] = "held"
    rows[3][5] = "`%s`" % gone_q
    met, line = run(build(rows=rows))
    check("all_held_unmet", (not met) and "status" in line and "quote" in line)
    rows = default_rows()
    rows[0][2] = "absent"
    met, line = run(build(rows=rows))
    check("held_labelled_absent_unmet", (not met) and "status" in line and "status_ok=3" in line)
    rows = default_rows()
    rows[0][5] = "`%s`" % new_q
    rows[0][4] = str(line_at("mm/memcontrol.c", new_q))
    met, line = run(build(rows=rows))
    check("held_with_other_quote_unmet", (not met) and "quote" in line)
    rows = default_rows()
    rows[3][5] = "`an invented quote of seven words here`"
    met, line = run(build(rows=rows))
    check("replacement_not_located_unmet", (not met) and "quote_ok=3" in line and "line_ok=3" in line)
    rows = default_rows()
    rows[3][5] = "`failcnt %lu`"
    met, line = run(build(rows=rows))
    check("replacement_too_short_unmet", (not met) and "quote" in line)
    rows = default_rows()
    rows[3][5] = "`%s`" % q_ok
    met, line = run(build(rows=rows))
    check("replacement_from_other_file_unmet", (not met) and "quote" in line)
    # line arm
    rows = default_rows()
    rows[0][4] = str(int(rows[0][4]) + 1)
    met, line = run(build(rows=rows))
    check("line_off_by_one_unmet", (not met) and "line" in line and "line_ok=3" in line)
    rows = default_rows()
    rows[1][4] = "-"
    met, line = run(build(rows=rows))
    check("line_blank_unmet", (not met) and "line_ok=3" in line)
    rows = default_rows()
    rows[2][4] = "0"
    met, line = run(build(rows=rows))
    check("line_zero_unmet", (not met) and "line_ok=3" in line)
    rows = default_rows()
    rows[2][4] = "%d" % line_at(DOCS + "admin-guide/cgroup-v2.html", q_html)
    met, line = run(build(rows=rows))
    check("html_line_located_met", met)
    rows = default_rows()
    rows[1][4] = "0%s" % rows[1][4]
    met, line = run(build(rows=rows))
    check("line_leading_zero_unmet", (not met) and "line_ok=3" in line)
    raw = "a\n  b   c\n d\ne f g"
    t, o = norm_map(raw, "text")
    check("norm_map_text_lines", lines_of(raw, t, o, "b c d") == {2} and lines_of(raw, t, o, "e f") == {4})
    rh = "<p>x</p>\n<p>All&nbsp;memory <b>amounts</b>\n are</p>&amp;"
    t, o = norm_map(rh, "html")
    check("norm_map_html_lines", lines_of(rh, t, o, "memory amounts are") == {2} and t.endswith("&")
          and "All memory amounts are" in t)
    r50_norm = lambda s: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", re.sub(
        r"<!--.*?-->", " ", re.sub(r"<(script|style)\b.*?</\1\s*>", " ", s, flags=re.S | re.I), flags=re.S))))
    hc = files[V73[DOCS + "admin-guide/cgroup-v2.html"][0]]
    check("html_norm_equals_r50_normalise", norm_map(hc, "html")[0] == r50_norm(hc))
    rows = default_rows()
    rows[0][1] = e2
    met, line = run(build(rows=rows))
    check("wrong_entry_unmet", (not met) and "bad_rows" in line)
    rows = default_rows()
    rows[0][6] = "maybe"
    met, line = run(build(rows=rows))
    check("bad_disposition_unmet", (not met) and "bad_rows" in line)
    met, line = run(build(src_kw={"status": "queued"}))
    check("row_not_mined_unmet", (not met) and "source_rows=bad" in line)
    met, line = run(build(src_kw={"opened": "2026-10-25"}))
    check("row_opened_earlier_unmet", (not met) and "source_rows=bad" in line)
    met, line = run(build(src_kw={"opened": "2026-10-26"}))
    check("row_opened_r53_day_met", met)
    met, line = run(build(src_kw={"used": "corpus/knowledge/other.md"}))
    check("row_usedby_unmet", (not met) and "source_rows=bad" in line)
    met, line = run(build(src_kw={"used": R53_LEDGER}))
    check("row_usedby_r53_ledger_only_unmet", (not met) and "source_rows=bad" in line)
    met, line = run(build(src_kw={"url": "https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/util.c"}))
    check("row_v72_url_unmet", (not met) and "source_rows=bad" in line)
    met, line = run(build(src_kw={"indent": "   "}))
    check("indented_rows_met", met)
    met, line = run(build(src_kw={"indent": "    "}))
    check("code_indented_rows_unmet", not met)
    rows = default_rows()
    rows[0][3] = sids["mm/oom_kill.c"]
    met, line = run(build(rows=rows))
    check("row_other_path_unmet", (not met) and "source_rows=bad" in line)
    met, line = run(build(prov=False))
    check("provenance_unmet", (not met) and "provenance=bad" in line)
    fl = build()
    fl[V73["mm/util.c"][0]] = fl[V73["mm/util.c"][0]] + "\n"
    met, line = run(fl)
    check("pin_tampered_unmet", (not met) and "pins=bad" in line)
    fl = build()
    del fl[V73["mm/oom_kill.c"][0]]
    met, line = run(fl)
    check("pin_missing_unmet", (not met) and "pins=bad" in line)
    # vote arm
    met, line = run(build(votes=None))
    check("no_votes_unmet", (not met) and "votes" in line and "voted=0" in line)
    one = lambda rows: {VOTE_DIR + "Mo54Rc02.md": "\n".join("RECHECK %s holds" % r[0] for r in rows)}
    met, line = run(build(votes=one))
    check("one_voter_unmet", (not met) and "votes" in line)
    met, line = run(build(votes=lambda rows: {VOTE_DIR + "Mo54Rc02.md": "\n".join(
        "RECHECK %s holds\nRECHECK %s holds" % (r[0], r[0]) for r in rows)}))
    check("same_voter_twice_unmet", (not met) and "votes" in line)
    two = lambda names: (lambda rows: {VOTE_DIR + v + ".md": "\n".join("RECHECK %s holds" % r[0] for r in rows)
                                       for v in names})
    met, line = run(build(votes=two(("Mo54Exec01", "Mo54Rev02"))))
    check("non_voters_unmet", (not met) and "votes" in line)
    met, line = run(build(votes=two(("Mo53Fr01", "Mo53Fr02"))))
    check("round53_voter_names_unmet", (not met) and "voted=0" in line)
    met, line = run(build(votes=two(("Mo54Rc01", "Mo54Rc02")), settled=["Mo54Rc01"]))
    check("voter_not_in_results_unmet", (not met) and "voted=0" in line)
    met, line = run(build(votes=two(("Mo54Rc01", "Mo54Rc02")), settled=["Mo54Rc01", "Mo54Rc02"]))
    check("voters_in_results_met", met)
    fl = build(votes=two(("Mo54Rc01", "Mo54Rc02")))
    del fl[RESULTS]
    met, line = run(fl)
    check("results_absent_unmet", (not met) and "voted=0" in line)
    fl = build(votes=two(("Mo54Rc01", "Mo54Rc02")))
    fl[RESULTS] = "{not json"
    met, line = run(fl)
    check("results_malformed_unmet", (not met) and "voted=0" in line)
    fl = build(votes=two(("Mo54Rc01", "Mo54Rc02")))
    fl[RESULTS] = json.dumps({"results": [{"seat": "Mo54Rc01"}, {"seat": "Mo54Rc02"}]})
    met, line = run(fl)
    check("results_wrong_key_unmet", (not met) and "voted=0" in line)
    fl = build(votes=two(("Mo54Rc01", "Mo54Rc02")))
    fl[RESULTS] = json.dumps(["Mo54Rc01", "Mo54Rc02"])
    met, line = run(fl)
    check("results_bare_list_unmet", (not met) and "voted=0" in line)
    met, line = run(build(votes=lambda rows: {VOTE_DIR + v + ".md": "\n".join(
        ["```"] + ["RECHECK %s holds" % r[0] for r in rows] + ["```"]) for v in ("Mo54Rc01", "Mo54Rc02")}))
    check("fenced_votes_unmet", (not met) and "votes" in line)
    met, line = run(build(votes=lambda rows: two(("Mo54Rc01", "Mo54Rc02"))(rows) | {
        VOTE_DIR + "Mo54Rc03.md": "RECHECK %s changed\n" % rows[0][0]}))
    check("dissent_unmet", (not met) and "dissent=1" in line)
    met, line = run(build(votes=lambda rows: two(("Mo54Rc01", "Mo54Rc02"))(rows) | {
        VOTE_DIR + "Mo54Rc03.md": "RECHECK %s changed\nRECHECK %s holds\n" % (rows[0][0], rows[0][0])}))
    check("revised_dissent_met", met and "dissent=0" in line)
    met, line = run(build(votes=lambda rows: two(("Mo54Rc01", "Mo54Rc02"))(rows) | {
        VOTE_DIR + "Mo54Rc03.md": "```\nRECHECK %s changed\n```\n" % rows[0][0]}))
    check("fenced_dissent_ignored_met", met)
    met, line = run(build(votes=lambda rows: two(("Mo54Rc01", "Mo54Rc02"))(rows) | {
        VOTE_DIR + "Mo54Rc03.md": "RECHECK %s changed\n" % rows[0][0]}, settled=["Mo54Rc01", "Mo54Rc02"]))
    check("unsettled_dissent_ignored_met", met)
    met, line = run(build(votes=lambda rows: {VOTE_DIR + v + ".md": "\n".join(
        ["QUOTE %s :: %s" % (rows[3][0], new_q)] + ["RECHECK %s holds" % r[0] for r in rows])
        for v in ("Mo54Rc01", "Mo54Rc02")}))
    check("author_vote_not_counted_unmet", (not met) and "votes" in line and "voted=3" in line)
    met, line = run(build(votes=lambda rows: {VOTE_DIR + v + ".md": "\n".join(
        ["```", "QUOTE %s :: %s" % (rows[3][0], new_q), "```"] + ["RECHECK %s holds" % r[0] for r in rows])
        for v in ("Mo54Rc01", "Mo54Rc02")}))
    check("fenced_quote_proposal_ignored_met", met)
    rows = default_rows()
    for r in rows:
        r[6] = "changed"
    met, line = run(build(rows=rows))
    check("all_changed_with_votes_met", met and "changed=4" in line)
    met, line = run(build(), scope_d={})
    check("empty_scope_unmet", not met)
    met, line = run(build(), scope_d=dict(d, ccccccccccc1=(e3, "include/linux/other.h", q_mc)))
    check("scope_path_without_copy_unmet", (not met) and "scope_path_without_copy" in line)
    # scope reader over a synthetic entering tree
    V72 = "https://raw.githubusercontent.com/torvalds/linux/v7.2/"
    ent = {
        "corpus/SOURCES.md": "\n".join([
            "| S001 | t — %smm/memcontrol.c | code | A | s | a | t | mined | 2026-10-26 | on-release | x |" % V72,
            "  | S002 | t — https://github.com/torvalds/linux/commit/abc.patch | code | A | s | a | t | mined | d | r | x |",
            "| S003 | t — https://docs.kernel.org/7.2/admin-guide/cgroup-v2.html | docs | A | s | a | t | mined | d | r | x |",
            "| S004 | t — %slib/percpu_counter.c?h=v7.2 | code | A | s | a | t | mined | d | r | x |" % CGIT,
            "| S005 | t — https://cdn.jsdelivr.net/gh/torvalds/linux@v7.2/include/uapi/asm-generic/errno.h | c | A | s | a | t | mined | d | r | x |",
            "| S006 | t — %sinclude/linux/mman.h?h=v7.3 | code | A | s | a | t | mined | d | r | x |" % CGIT,
            "| S007 | t — https://man7.org/linux/man-pages/man2/quotactl.2.html | docs | A | s | a | t | mined | d | r | x |"]),
        R53_LEDGER: ("| h | entry | status | source | quote | disposition |\n|---|---|---|---|---|---|\n"
                     "| %s | x | held | S1 | `q` | holds |\n" % claim_hash("done before")),
        KNOWLEDGE + "a.md": ("| claim | source | quote |\n|---|---|---|\n| one claim here | S001 | `%s` |\n"
                             "| two claim | S002 | `x y z` |\n| done before | S001 | `%s` |\n" % (q_mc, q_mc)),
        KNOWLEDGE + "b.md": ("```\n| claim | source | quote |\n| fenced | S001 | `a` |\n```\n| claim | source | quote |\n"
                             "|---|---|---|\n| three | S003 | `%s` |\n| four | S004 | `p q` |\n| five | S005 | `r s` |\n"
                             "| six | S006 | `t u` |\n| seven | S007 | `v w` |\n" % q_html),
        KNOWLEDGE + "c.txt": "| claim | source | quote |\n|---|---|---|\n| eight | S001 | `z z` |\n",
    }
    sd = scope(lambda p: ent.get(p), lambda dn: [p for p in ent if p.startswith(dn)])
    check("scope_reader", set(sd) == {claim_hash(x) for x in ("one claim here", "three", "four", "five")}
          and sd[claim_hash("three")][1] == DOCS + "admin-guide/cgroup-v2.html"
          and sd[claim_hash("four")][1] == "lib/percpu_counter.c"
          and sd[claim_hash("five")][1] == "include/uapi/asm-generic/errno.h")
    failn = 0
    for name, ok in checks:
        print("%s %s" % ("ok  " if ok else "FAIL", name))
        failn += 0 if ok else 1
    print("C1_SELFTEST pass=%d fail=%d" % (len(checks) - failn, failn))
    return 0 if failn == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
