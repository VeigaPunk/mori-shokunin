#!/usr/bin/env python3
"""Round 52 C2 counter (depth) — what /proc/meminfo's CommitLimit and Committed_AS are at kernel v7.2: the
overcommit accounting, the three overcommit modes, where the commit limit is enforced and what it leaves out
(resource runway: an allocation can fail with ENOMEM before memory is exhausted, and only under one mode).

Frozen predicate P-C2 (same sentence in contract.md, this counter and the receipt label):
  At revision R, corpus/knowledge/overcommit-commit-limit-r52.md opens with source: lines, verified-at: and
  recheck:, and carries a table whose header cells are claim, source, quote with at least 12 rows;
  each row's claim cell has at least 6 words, is unique in the table (case and whitespace folded) and
  carries at least 3 words of 3+ letters that are absent from its quote; each row's source cell is one
  S-id naming a corpus/SOURCES.md row at R that is mined, opened 2026-10-26, names its URL among the
  five frozen sources below and lists the entry in used-by; each row's quote cell is one backticked
  span of 6 to 25 words (an escaped \\| reads as |), unique in the table, that occurs (whitespace
  collapsed) in the committed copy of that row's URL under corpus/evidence/sources-r52/; the table
  draws on all 5 sources; every committed copy matches its frozen sha256; and (entailment arm, hardened
  per round-51 closure routed defect 2) for every row, at least 2 distinct ENTAILMENT voters carry an
  unfenced line `ENTAIL <h> entailed` in their own report `.ufo/waves/round-52/w1/<voter>.md` at R, no
  ENTAILMENT voter carries an unfenced line `ENTAIL <h> overclaim`, and a voter's `entailed` line does
  not count for a row whose text that voter wrote (its report carries an unfenced line
  `REPLACE <old> :: <text>` whose <text> hashes to <h>); <h> is the first 12 hex digits of the sha256 of
  the row's claim cell with whitespace collapsed and ends stripped; the ENTAILMENT voters are exactly the
  frozen VOTERS list below (no other file, no L1 file, no other directory counts).

Usage: count-c2.py <rev> [--repo DIR] [--entry PATH]   |   count-c2.py --selftest   |   count-c2.py --hashes <rev>
Output: `C2=met|unmet claims=N located=N quote_missing=N bad_rows=N sources=N source_rows=ok|bad pins=ok|bad
  provenance=ok|bad entailed=N dissent=N rev=R` (+ `failed=` list when unmet).
Exit 0 met, 1 unmet, 2 setup. Read-only: `git show` / `git ls-tree` / `git rev-parse` only.
Limits (named before data): a located quote proves the quoted words exist in the copy; the entailment arm proves
two ENTAILMENT seats that did not write the row text recorded `entailed` for that exact claim text and no
ENTAILMENT seat recorded `overclaim` — it does not prove the judgment right, and seats are the lane, not outside
verification; a REPLACE line is the only authorship signal the arm reads; v7.2 bytes say nothing about other
kernels or about this host's sysctl values.
"""
import hashlib
import html
import os
import re
import subprocess
import sys

ENTRY = "corpus/knowledge/overcommit-commit-limit-r52.md"
SRC_DIR = "corpus/evidence/sources-r52/"
ENTAIL_DIR = ".ufo/waves/round-52/w1/"
VOTERS = ["Mo52Ent%02d" % i for i in range(1, 13)]
MIN_VOTES = 2
OPENED = "2026-10-26"
MIN_CLAIMS = 12
MIN_SOURCES = 5
MIN_CLAIM_WORDS = 6
MIN_BEYOND = 3
MIN_WORDS, MAX_WORDS = 6, 25
# url -> (committed copy, sha256 of the copy fetched 2026-10-26, kind)
COPIES = {
    "https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/mm/overcommit-accounting.rst":
        (SRC_DIR + "overcommit-accounting.rst.v7.2", "767ab88153c4494e54fcf2db4e5bd01921d6bd8350f1596ada508cb5e4b4927f", "text"),
    "https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/sysctl/vm.rst":
        (SRC_DIR + "vm.rst.v7.2", "bf8ca0265fefc019250697b6ee47a0679709b2ee45f4d1893b3dfd95c1f8c1ce", "text"),
    "https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/util.c":
        (SRC_DIR + "util.c.v7.2", "e702754c45bd7bd69e5da22a6505c9c1016eaafe6e883b746cc3cdbd413ebe7c", "text"),
    "https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/mman.h":
        (SRC_DIR + "mman.h.v7.2", "d7bf787c910d9a7cbabee3a50c512ce3aad78d63659b0c968adca16b5916b058", "text"),
    "https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/mmap.c":
        (SRC_DIR + "mmap.c.v7.2", "449b858385c7ece0ff88a8b41893efadb70a437fb8585a296c4ef0461a4c1545", "text"),
}
SPAN = re.compile(r"`([^`]+)`")


def split_cells(line):
    s = line.strip()
    parts = re.split(r"(?<!\\)\|", s)
    if s.endswith("|"):
        parts = parts[1:-1]
    else:
        parts = parts[1:]
    return [p.strip() for p in parts]


def normalise_text(text):
    return re.sub(r"\s+", " ", text)


def words_beyond(claim, quote):
    qw = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z0-9_]{2,}", quote))
    return len(set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z0-9_]{2,}", claim)) - qw)


def normalise(text):
    t = re.sub(r"<(script|style)\b.*?</\1\s*>", " ", text, flags=re.S | re.I)
    t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    return re.sub(r"\s+", " ", t)


def parse_claims(entry_text):
    rows, header, fence = [], None, False
    for line in entry_text.split("\n"):
        if line.lstrip()[:3] in ("```", "~~~"):
            fence = not fence
            continue
        if fence:
            continue
        if not line.lstrip().startswith("|"):
            if header is not None and rows:
                break
            if not line.strip():
                header = header if rows else None
            continue
        cells = split_cells(line)
        if header is None:
            if [c.lower() for c in cells] == ["claim", "source", "quote"]:
                header = ["claim", "source", "quote"]
            continue
        if all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
            continue
        rows.append(cells)
    return header, rows


def claim_hash(claim):
    return hashlib.sha256(re.sub(r"\s+", " ", claim).strip().encode("utf-8")).hexdigest()[:12]


ENTAIL_RE = re.compile(r"^\s*ENTAIL\s+([0-9a-f]{12})\s+(entailed|overclaim)\b")
REPLACE_RE = re.compile(r"^\s*REPLACE\s+([0-9a-f]{12})\s+::\s+(.+?)\s*$")


def entail_votes(read, ls):
    """hash -> set of (kind, voter); authored: voter -> set of hashes that voter wrote (REPLACE lines)."""
    votes, authored = {}, {}
    present = set(ls(ENTAIL_DIR) or [])
    for voter in VOTERS:
        path = ENTAIL_DIR + voter + ".md"
        if path not in present:
            continue
        fence = False
        for line in (read(path) or "").split("\n"):
            if line.lstrip()[:3] in ("```", "~~~"):
                fence = not fence
                continue
            if fence:
                continue
            m = ENTAIL_RE.match(line)
            if m:
                votes.setdefault(m.group(1), set()).add((m.group(2), voter))
            r = REPLACE_RE.match(line)
            if r:
                authored.setdefault(voter, set()).add(claim_hash(r.group(2)))
    return votes, authored


def sources_row(src_text, row_id):
    for line in src_text.split("\n"):
        if re.match(r"^ {0,3}\|\s*%s\s*\|" % re.escape(row_id), line):
            return split_cells(line)
    return None


def evaluate(read, rev, entry_path=None, copies=None, ls=None):
    entry_path = entry_path or ENTRY
    votes, authored = entail_votes(read, ls or (lambda d: []))
    entailed = dissent = 0
    copies = copies or COPIES
    failed = []
    # pins
    norm = {}
    pins_ok = True
    for url, (path, digest, kind) in copies.items():
        b = read(path)
        if b is None or hashlib.sha256(b.encode("utf-8", "surrogateescape")).hexdigest() != digest:
            pins_ok = False
        norm[url] = normalise(b or "") if kind == "html" else normalise_text(b or "")
    if not pins_ok:
        failed.append("pins")
    entry = read(entry_path)
    prov = "bad"
    claims = located = missing = bad = 0
    used_sources = set()
    srows_ok = "bad"
    if entry is None:
        failed.append("entry_absent")
    else:
        head = [l for l in entry.split("\n") if l.strip()][:14]
        has = lambda k: any(re.match(r"^[-* ]*%s\s*:" % k, l) for l in head)
        src_lines = [l for l in head if re.match(r"^[-* ]*source\s*:", l)]
        header, rows = parse_claims(entry)
        if header is None:
            failed.append("table")
            rows = []
        claims = len(rows)
        if claims < MIN_CLAIMS:
            failed.append("claims_floor")
        src_text = read("corpus/SOURCES.md") or ""
        seen_quotes = set()
        seen_claims = set()
        row_cache = {}
        ids_in_table = set()
        for cells in rows:
            if len(cells) != 3 or len(cells[0].split()) < MIN_CLAIM_WORDS:
                bad += 1
                continue
            ckey = re.sub(r"\s+", " ", cells[0]).strip().lower()
            sid = cells[1].strip("` ")
            quotes = SPAN.findall(cells[2])
            if not re.fullmatch(r"S[0-9]{3,}", sid) or len(quotes) != 1 or ckey in seen_claims:
                bad += 1
                continue
            q = re.sub(r"\s+", " ", quotes[0].replace("\\|", "|")).strip()
            words = q.split(" ")
            if (not (MIN_WORDS <= len(words) <= MAX_WORDS) or q in seen_quotes
                    or words_beyond(cells[0], q) < MIN_BEYOND):
                bad += 1
                continue
            seen_quotes.add(q)
            seen_claims.add(ckey)
            ids_in_table.add(sid)
            if sid not in row_cache:
                row_cache[sid] = sources_row(src_text, sid)
            srow = row_cache[sid]
            url = None
            if srow and len(srow) == 11:
                for u in copies:
                    if u in srow[1]:
                        url = u
                        break
            row_ok = bool(srow and len(srow) == 11 and url is not None and srow[7] == "mined"
                          and srow[8] == OPENED
                          and entry_path in [u.strip() for u in re.split(r"[,;]", srow[10])])
            if not row_ok:
                bad += 1
                continue
            if q in norm[url]:
                located += 1
                used_sources.add(url)
            else:
                missing += 1
            h = claim_hash(cells[0])
            v = votes.get(h, set())
            ok_voters = set(who for k, who in v if k == "entailed" and h not in authored.get(who, set()))
            if any(k == "overclaim" for k, _ in v):
                dissent += 1
            elif len(ok_voters) >= MIN_VOTES:
                entailed += 1
        if bad:
            failed.append("bad_rows")
        if dissent or entailed != claims:
            failed.append("entailment")
        if missing:
            failed.append("quote_missing")
        if len(used_sources) < MIN_SOURCES:
            failed.append("sources_floor")
        cited = set()
        for l in src_lines:
            cited |= set(re.findall(r"\bS[0-9]{3,}\b", l))
        if has("source") and has("verified-at") and has("recheck") and ids_in_table and ids_in_table <= cited:
            prov = "ok"
        else:
            failed.append("provenance")
        srows_ok = "ok" if (ids_in_table and not bad) else "bad"
        if srows_ok != "ok":
            failed.append("source_rows")
    met = not failed
    line = ("C2=%s claims=%d located=%d quote_missing=%d bad_rows=%d sources=%d source_rows=%s pins=%s "
            "provenance=%s entailed=%d dissent=%d rev=%s" % ("met" if met else "unmet", claims, located, missing, bad,
                                      len(used_sources), srows_ok, "ok" if pins_ok else "bad", prov,
                                      entailed, dissent, rev))
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
    def ls(d):
        p = subprocess.run(["git", "-C", repo, "ls-tree", "--name-only", rev, d],
                           stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=60)
        return p.stdout.decode("utf-8", "surrogateescape").split("\n") if p.returncode == 0 else []
    return ls


def main(argv):
    if argv == ["--selftest"]:
        return selftest()
    if len(argv) == 2 and argv[0] == "--hashes":
        repo = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        text = git_reader(repo, argv[1])(ENTRY)
        if text is None:
            print("C2_SETUP entry absent at %s" % argv[1], file=sys.stderr)
            return 2
        for n, cells in enumerate(parse_claims(text)[1], 1):
            print("row=%d hash=%s claim=%s" % (n, claim_hash(cells[0]) if cells else "-", cells[0] if cells else ""))
        return 0
    args = list(argv)
    repo = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    entry = ENTRY
    while "--repo" in args:
        i = args.index("--repo"); repo = args[i + 1]; del args[i:i + 2]
    while "--entry" in args:
        i = args.index("--entry"); entry = args[i + 1]; del args[i:i + 2]
    if len(args) != 1 or args[0].startswith("-"):
        print("C2_SETUP usage: count-c2.py <rev> [--repo DIR] [--entry PATH] | --selftest", file=sys.stderr)
        return 2
    try:
        full = subprocess.run(["git", "-C", repo, "rev-parse", "--verify", args[0] + "^{commit}"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60,
                              check=True).stdout.decode().strip()
    except (subprocess.SubprocessError, OSError):
        print("C2_SETUP unresolvable revision %s" % args[0], file=sys.stderr)
        return 2
    met, line = evaluate(git_reader(repo, full), full, entry_path=entry, ls=git_lister(repo, full))
    print(line)
    return 0 if met else 1


def selftest():
    here = os.path.dirname(os.path.abspath(__file__))
    lane = os.path.dirname(os.path.dirname(os.path.dirname(here)))
    files = {}
    for url, (path, digest, kind) in COPIES.items():
        with open(os.path.join(lane, path), "rb") as f:
            files[path] = f.read().decode("utf-8", "surrogateescape")
    texts = {u: (normalise(files[p]) if k == "html" else normalise_text(files[p]))
             for u, (p, d, k) in COPIES.items()}

    def quote_from(url, needle, n=8):
        t = texts[url]
        i = t.index(needle)
        return " ".join(t[i:].split(" ")[:n])

    urls = list(COPIES)
    qs = [
        (urls[0], quote_from(urls[0], "Heuristic overcommit handling. Obvious overcommits of address", 8)),
        (urls[0], quote_from(urls[0], "The overcommit policy is set via the sysctl", 8)),
        (urls[0], quote_from(urls[0], "In mode 2 the MAP_NORESERVE flag is ignored.", 8)),
        (urls[1], quote_from(urls[1], "When this flag is 1, the kernel pretends there is always enough", 12)),
        (urls[1], quote_from(urls[1], "This setting has no effect when overcommit_memory is set to 0 or 1.", 12)),
        (urls[2], quote_from(urls[2], "if (pages > totalram_pages() + total_swap_pages) goto error;", 8)),
        (urls[2], quote_from(urls[2], "allowed = ((totalram_pages() - hugetlb_total_pages()) * sysctl_overcommit_ratio / 100);", 9)),
        (urls[2], quote_from(urls[2], "Committed memory limit enforced when OVERCOMMIT_NEVER policy is used", 9)),
        (urls[3], quote_from(urls[3], "static inline void vm_acct_memory(long pages)", 7)),
        (urls[3], quote_from(urls[3], "static inline void vm_unacct_memory(long pages)", 7)),
        (urls[4], quote_from(urls[4], "We honor MAP_NORESERVE if allowed to overcommit", 8)),
        (urls[4], quote_from(urls[4], "sysctl_user_reserve_kbytes = min(free_kbytes / 32, SZ_128K);", 6)),
    ]
    sids = {u: "S9%02d" % (n + 1) for n, u in enumerate(urls)}

    def srow(url, sid, status="mined", opened=OPENED, used=ENTRY, indent=""):
        return ("%s| %s | title — %s | docs | A | scope | anchor | teaches | %s | %s | 180d | %s |"
                % (indent, sid, url, status, opened, used))

    def claim_text(i):
        return "observation number %d explains how the kernel estimate reads its counters" % i

    def build(claim_rows=None, drop=None, claims=None, votes="all", **kw):
        rows = ["| claim | source | quote |", "|---|---|---|"]
        cl = []
        for i, (u, q) in enumerate(claim_rows or qs):
            c = claims[i] if claims else claim_text(i)
            cl.append(c)
            rows.append("| %s | %s | `%s` |" % (c, sids[u], q.replace("|", "\\|")))
        entry = "\n".join([
            "# Overcommit", "",
            "source: " + " ".join(sids[u] for u in urls), "verified-at: 2026-10-26",
            "recheck: 180d — `curl -s https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/util.c | sha256sum`", "",
            "## Claims", ""] + rows + [""])
        src = "\n".join(["| id | source |", "|---|---|"] + [
            srow(u, sids[u], **({k: v for k, v in kw.items() if k in ("status", "opened", "used", "indent")}
                                if drop != sids[u] else {"status": "queued"})) for u in urls])
        fl = dict(files)
        fl[ENTRY] = entry
        fl["corpus/SOURCES.md"] = src
        if votes == "all":
            for v in ("Mo52Ent01", "Mo52Ent07"):
                fl[ENTAIL_DIR + v + ".md"] = "\n".join("ENTAIL %s entailed — row %d" % (claim_hash(c), n)
                                                       for n, c in enumerate(cl, 1)) + "\n"
        elif votes is not None:
            fl.update(votes(cl))
        return fl

    def run(fl, **kw):
        lister = lambda d: [p for p in fl if p.startswith(d) and "/" not in p[len(d):]]
        return evaluate(lambda p: fl.get(p), "R", ls=lister, **kw)

    checks = []

    def check(name, cond):
        checks.append((name, bool(cond)))

    met, line = run(build())
    check("honest_met", met and "claims=12 located=12" in line and "sources=5" in line and "entailed=12 dissent=0" in line)
    met, line = run({k: v for k, v in build().items() if k != ENTRY})
    check("entry_absent_unmet", (not met) and "entry_absent" in line)
    fl = build(); fl[ENTRY] = "# staged\n\nsource: S901\nverified-at: x\nrecheck: y\n\nThe estimate is a sum.\n"
    met, line = run(fl)
    check("no_table_unmet", (not met) and "table" in line)
    bad_q = list(qs); bad_q[0] = (urls[0], "An estimate of how much memory is available entirely at random")
    met, line = run(build(claim_rows=bad_q))
    check("altered_quote_unmet", (not met) and "quote_missing=1" in line)
    swap = list(qs); swap[4] = (urls[1], quote_from(urls[0], "The overcommit amount can be set via", 8))
    met, line = run(build(claim_rows=swap))
    check("quote_from_wrong_copy_unmet", (not met) and "quote_missing" in line)
    short = list(qs); short[3] = (urls[1], "available = 0;")
    met, line = run(build(claim_rows=short))
    check("short_quote_unmet", (not met) and "bad_rows" in line)
    long_q = list(qs); long_q[3] = (urls[1], " ".join(["available"] * 26))
    met, line = run(build(claim_rows=long_q))
    check("long_quote_unmet", (not met) and "bad_rows" in line)
    dup = list(qs); dup[1] = dup[0]
    met, line = run(build(claim_rows=dup))
    check("duplicate_quote_unmet", (not met) and "bad_rows" in line)
    met, line = run(build(claim_rows=qs[:11]))
    check("claims_floor_unmet", (not met) and "claims_floor" in line)
    four = [x for x in qs if x[0] != urls[4]] + [
        (urls[0], quote_from(urls[0], "Always overcommit. Appropriate for some scientific", 7)),
        (urls[1], quote_from(urls[1], "This value contains a flag that enables memory overcommitment.", 9))]
    met, line = run(build(claim_rows=four))
    check("sources_floor_unmet", (not met) and "sources_floor" in line)
    met, line = run(build(status="queued"))
    check("row_not_mined_unmet", (not met) and "bad_rows" in line)
    met, line = run(build(opened="2026-10-25"))
    check("row_opened_other_day_unmet", (not met) and "bad_rows" in line)
    met, line = run(build(used="—"))
    check("used_by_missing_unmet", (not met) and "bad_rows" in line)
    met, line = run(build(indent="   "))
    check("indented_row_ok", met)
    met, line = run(build(indent="    "))
    check("code_indented_row_unmet", not met)
    fl = build(); fl[COPIES[urls[2]][0]] = fl[COPIES[urls[2]][0]] + "\n"
    met, line = run(fl)
    check("pin_mismatch_unmet", (not met) and "pins=bad" in line)
    fl = build(); fl[ENTRY] = fl[ENTRY].replace("source: S901 S902", "source: S902", 1)
    met, line = run(fl)
    check("table_id_uncited_in_source_unmet", (not met) and "provenance" in line)
    fl = build(); fl[ENTRY] = fl[ENTRY].replace("verified-at: 2026-10-26\n", "")
    met, line = run(fl)
    check("verified_at_missing_unmet", (not met) and "provenance" in line)
    fl = build(); fl[ENTRY] = fl[ENTRY].replace("| claim | source | quote |", "| claim | source | evidence |")
    met, line = run(fl)
    check("header_wrong_unmet", (not met) and "table" in line)
    fl = build(claims=[claim_text(i) if i != 3 else "short claim" for i in range(12)])
    met, line = run(fl)
    check("claim_cell_short_unmet", (not met) and "bad_rows" in line)
    fl = build(claims=["the same claim repeated for every row of the table"] * 12)
    met, line = run(fl)
    check("breadcrumb_identical_claims_unmet", (not met) and "bad_rows=11" in line)
    echo = [q for u, q in qs]
    fl = build(claims=[q + " here" for q in echo])
    met, line = run(fl)
    check("claim_echoes_quote_unmet", (not met) and "bad_rows" in line)
    fl = build(); fl[ENTRY] = "```\n" + fl[ENTRY] + "\n```\n"
    met, line = run(fl)
    check("table_inside_fence_unseen_unmet", not met)
    met, line = run(build(), entry_path="corpus/knowledge/other.md")
    check("other_entry_path_unmet", not met)
    # entailment arm (round 51, hardened round 52)
    def vote_all(c_list, kind="entailed", fmt="ENTAIL %s %s"):
        return "\n".join(fmt % (claim_hash(c), kind) for c in c_list) + "\n"
    A = ENTAIL_DIR + "Mo52Ent01.md"
    B = ENTAIL_DIR + "Mo52Ent02.md"
    met, line = run(build(votes=None))
    check("entail_no_votes_unmet", (not met) and "entailment" in line and "entailed=0" in line)
    met, line = run(build(votes=lambda cl: {A: vote_all(cl)}))
    check("entail_one_voter_unmet", (not met) and "entailed=0" in line)
    met, line = run(build(votes=lambda cl: {A: vote_all(cl) + vote_all(cl)}))
    check("entail_same_voter_twice_unmet", (not met) and "entailed=0" in line)
    met, line = run(build(votes=lambda cl: {A: vote_all(cl), B: vote_all(cl[:-1])}))
    check("entail_one_row_single_vote_unmet", (not met) and "entailed=11" in line)
    met, line = run(build(votes=lambda cl: {A: vote_all(cl), B: vote_all(cl) + "ENTAIL %s overclaim — more\n" % claim_hash(cl[5])}))
    check("entail_dissent_unmet", (not met) and "dissent=1" in line)
    met, line = run(build(votes=lambda cl: {A: vote_all(cl), ENTAIL_DIR + "MoriR52-notes.md": vote_all(cl)}))
    check("entail_l1_file_ignored_unmet", (not met) and "entailed=0" in line)
    met, line = run(build(votes=lambda cl: {A: vote_all(cl), ENTAIL_DIR + "Mo52CritC2.md": vote_all(cl)}))
    check("entail_non_voter_seat_ignored_unmet", (not met) and "entailed=0" in line)
    met, line = run(build(votes=lambda cl: {A: vote_all(cl), ENTAIL_DIR + "Mo52Ent13.md": vote_all(cl)}))
    check("entail_voter_outside_list_ignored_unmet", (not met) and "entailed=0" in line)
    met, line = run(build(votes=lambda cl: {A: vote_all(cl), ENTAIL_DIR + "Mo52Ent02.txt": vote_all(cl)}))
    check("entail_non_md_ignored_unmet", (not met) and "entailed=0" in line)
    met, line = run(build(votes=lambda cl: {A: vote_all(cl), ".ufo/waves/round-52/other/Mo52Ent02.md": vote_all(cl)}))
    check("entail_other_dir_ignored_unmet", (not met) and "entailed=0" in line)
    met, line = run(build(votes=lambda cl: {A: vote_all(cl), B: "```\n" + vote_all(cl) + "```\n"}))
    check("entail_fenced_votes_ignored_unmet", (not met) and "entailed=0" in line)
    met, line = run(build(votes=lambda cl: {A: vote_all(cl), B: vote_all(cl) + "```\nENTAIL %s overclaim\n```\n" % claim_hash(cl[0])}))
    check("entail_fenced_dissent_ignored_met", met)
    met, line = run(build(votes=lambda cl: {A: vote_all(cl), B: vote_all(cl), ENTAIL_DIR + "Mo52CritC2.md": "ENTAIL %s overclaim\n" % claim_hash(cl[0])}))
    check("entail_non_voter_dissent_ignored_met", met)
    met, line = run(build(votes=lambda cl: {A: vote_all(cl) + "REPLACE 0123456789ab :: %s\n" % cl[3], B: vote_all(cl)}))
    check("entail_author_vote_not_counted_unmet", (not met) and "entailed=11" in line)
    met, line = run(build(votes=lambda cl: {A: vote_all(cl) + "REPLACE 0123456789ab :: %s\n" % cl[3], B: vote_all(cl),
                                             ENTAIL_DIR + "Mo52Ent03.md": vote_all(cl[3:4])}))
    check("entail_author_plus_two_others_met", met)
    met, line = run(build(votes=lambda cl: {A: vote_all(cl) + "```\nREPLACE 0123456789ab :: %s\n```\n" % cl[3], B: vote_all(cl)}))
    check("entail_fenced_replace_not_authorship_met", met)
    met, line = run(build(votes=lambda cl: {A: "\n".join("ENTAIL %s entailed" % claim_hash(c + " extra") for c in cl) + "\n", B: vote_all(cl)}))
    check("entail_hash_of_other_text_unmet", (not met) and "entailed=0" in line)
    met, line = run(build(votes=lambda cl: {A: "\n".join("ENTAIL %s entailed" % claim_hash("  " + c.replace(" ", "   ") + " ") for c in cl) + "\n", B: vote_all(cl)}))
    check("entail_hash_whitespace_folded_met", met)
    check("voters_frozen", VOTERS[0] == "Mo52Ent01" and VOTERS[-1] == "Mo52Ent12" and len(VOTERS) == 12)
    check("words_beyond_counts", words_beyond("the anon bucket holds heap pages", "anon heap") == 4)
    check("text_copy_keeps_angle_brackets", "a < b" in normalise_text("if (a <   b) x > y"))
    for name, cond in checks:
        print("%s %s" % ("PASS" if cond else "FAIL", name))
    failn = sum(1 for _, c in checks if not c)
    print("C2_SELFTEST pass=%d fail=%d" % (len(checks) - failn, failn))
    return 0 if failn == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
