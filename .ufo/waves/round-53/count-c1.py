#!/usr/bin/env python3
"""Round 53 C1 counter (freshness) — the lane's release-pinned located-quote claims re-verified at Linux v7.3.

Linux v7.3 is tagged (`git ls-remote https://github.com/torvalds/linux refs/tags/v7.3` prints
091b06388b117fefdcb63336ac09956a4914b961). The round-51 and round-52 entries pin their claims to v7.2 bytes and
say `recheck: on-release`: that trigger has fired.

Frozen predicate P-C1 (same sentence in contract.md, this counter and the receipt label):
  At revision R, corpus/knowledge/kernel-v7.3-recheck-r53.md opens with source:, verified-at: and recheck:
  lines and carries one table whose header cells are h, entry, status, source, quote, disposition, holding
  exactly one row for each hash of the frozen scope set D and no other row; D is the set of claim rows, read
  at the entering tip 20edafa59b38dac1ca358893f0259b1f436372d3, of the claim|source|quote tables of
  corpus/knowledge/memavailable-estimate-r51.md and corpus/knowledge/overcommit-commit-limit-r52.md whose
  source row's URL names tag v7.2 of torvalds/linux; each row's entry cell names the entry holding that hash;
  its status cell equals this counter's own derivation — `held` when the row's v7.2 quote occurs (whitespace
  collapsed) in the committed v7.3 copy of the same path, else `absent`; its source cell is one S-id naming a
  corpus/SOURCES.md row at R that is mined, opened 2026-10-26, carries the frozen v7.3 URL of that path and
  lists the recheck entry in used-by; its quote cell is one backticked span of 6 to 25 words (an escaped \\|
  reads as |) that occurs (whitespace collapsed) in that v7.3 copy and equals the v7.2 quote when the status
  is held; its disposition cell is `holds` or `changed`; every committed v7.3 copy matches its frozen sha256;
  and (vote arm) for every row at least 2 distinct RECHECK voters' final unfenced line `RECHECK <h> <word>`
  in their own report .ufo/waves/round-53/w1/<voter>.md at R carries the row's disposition, and no RECHECK
  voter's final line for that hash carries the other word; a voter's line does not count for a row whose
  quote that voter proposed (an unfenced `QUOTE <h> :: <text>` line in its report whose text equals the
  row's quote); the RECHECK voters are exactly the frozen VOTERS list below.

Usage: count-c1.py <rev> [--repo DIR]   |   count-c1.py --selftest   |   count-c1.py --scope
Output: `C1=met|unmet scope=N rows=N matched=N status_ok=N quote_ok=N source_rows=ok|bad pins=ok|bad
  provenance=ok|bad held=N absent=N holds=N changed=N voted=N dissent=N rev=R` (+ `failed=` list when unmet).
Exit 0 met, 1 unmet, 2 setup. Read-only: `git show` / `git ls-tree` / `git rev-parse` only.

Limits (named before data): `held` proves the v7.2 quote's words still occur somewhere in the v7.3 file, not
at the same place nor with the same meaning — the disposition and its votes carry the meaning; the vote arm
proves two RECHECK seats recorded that judgment, and seats are the lane, not outside verification; D covers the
claim tables of two entries (46 rows) and nothing else the lane pins to v7.2 (oom-tracepoints-r47, the
round-50 memcg entry, prose outside the tables, the SOURCES anchors); the v7.3 copies were fetched from
git.kernel.org cgit, and their sha256 pins prove they are the bytes fetched, not that cgit served the tag.
"""
import hashlib
import os
import re
import subprocess
import sys

ENTERING = "20edafa59b38dac1ca358893f0259b1f436372d3"
LEDGER = "corpus/knowledge/kernel-v7.3-recheck-r53.md"
ENTRIES = ["corpus/knowledge/memavailable-estimate-r51.md", "corpus/knowledge/overcommit-commit-limit-r52.md"]
SRC_DIR = "corpus/evidence/sources-r53/"
VOTE_DIR = ".ufo/waves/round-53/w1/"
VOTERS = ["Mo53Fr%02d" % i for i in range(1, 13)]
MIN_VOTES = 2
OPENED = "2026-10-26"
MIN_WORDS, MAX_WORDS = 6, 25
V72 = "https://raw.githubusercontent.com/torvalds/linux/v7.2/"
CGIT = "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/"
# kernel path -> (committed v7.3 copy, sha256 of the copy fetched 2026-10-26, frozen v7.3 URL)
V73 = {
    "Documentation/filesystems/proc.rst":
        (SRC_DIR + "proc.rst.v7.3", "bc178ff511e05c1b5e0c2413feb18223edcaeb2797ce499b714b98120cabf3c8"),
    "mm/show_mem.c":
        (SRC_DIR + "show_mem.c.v7.3", "c50205bc19974566d7bfe1c161f253cf71321c06ecc1327abb2a775be8a0de71"),
    "fs/proc/meminfo.c":
        (SRC_DIR + "meminfo.c.v7.3", "d6c5807421a69eac21efd737b39d099c711b3132b371dc34986d181746e3deda"),
    "include/linux/mm_inline.h":
        (SRC_DIR + "mm_inline.h.v7.3", "277e99e23ecc1b5babfdf041e7e7e3f9d280113b3b0a9f7e8340c0e13d7b391b"),
    "Documentation/mm/overcommit-accounting.rst":
        (SRC_DIR + "overcommit-accounting.rst.v7.3", "767ab88153c4494e54fcf2db4e5bd01921d6bd8350f1596ada508cb5e4b4927f"),
    "Documentation/admin-guide/sysctl/vm.rst":
        (SRC_DIR + "vm.rst.v7.3", "f81feb3dfca5f054cf8b76c71d7a4525a88d629d3ea8239743996b9d87bb391b"),
    "mm/util.c":
        (SRC_DIR + "util.c.v7.3", "4dfcce2b8fa8f18c350565950a10248b3590e3d3c0c9335fef6d47daa7a9e1f2"),
    "include/linux/mman.h":
        (SRC_DIR + "mman.h.v7.3", "d7bf787c910d9a7cbabee3a50c512ce3aad78d63659b0c968adca16b5916b058"),
    "mm/mmap.c":
        (SRC_DIR + "mmap.c.v7.3", "8e51fb1c10fee6943c9edc26b72952137b4098b00cc050ea1e6ade6e27197feb"),
}
V73 = {p: (c, d, CGIT + p + "?h=v7.3") for p, (c, d) in V73.items()}
HEADER = ["h", "entry", "status", "source", "quote", "disposition"]
SPAN = re.compile(r"`([^`]+)`")
RECHECK_RE = re.compile(r"^\s*RECHECK\s+([0-9a-f]{12})\s+(holds|changed)\b")
QUOTE_RE = re.compile(r"^\s*QUOTE\s+([0-9a-f]{12})\s+::\s+(.+?)\s*$")


def split_cells(line):
    s = line.strip()
    parts = re.split(r"(?<!\\)\|", s)
    parts = parts[1:-1] if s.endswith("|") else parts[1:]
    return [p.strip() for p in parts]


def ws(text):
    return re.sub(r"\s+", " ", text).strip()


def claim_hash(claim):
    return hashlib.sha256(ws(claim).encode("utf-8")).hexdigest()[:12]


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


def scope(read_entering):
    """Frozen scope D: hash -> (entry, kernel path, v7.2 quote). Read at the entering tip only."""
    src = read_entering("corpus/SOURCES.md") or ""
    d = {}
    for entry in ENTRIES:
        text = read_entering(entry) or ""
        _, rows = parse_table(text, ["claim", "source", "quote"])
        for cells in rows:
            if len(cells) != 3:
                continue
            srow = sources_row(src, cells[1].strip("` "))
            if not srow or len(srow) < 2:
                continue
            m = re.search(re.escape(V72) + r"(\S+?)(?=[\s)>\]]|$)", srow[1])
            if not m:
                continue
            q = one_quote(cells[2])
            if q is None:
                continue
            d[claim_hash(cells[0])] = (entry, m.group(1), q)
    return d


def final_votes(read, ls):
    """hash -> {voter: last word}; proposed: voter -> {hash: set of quote texts}."""
    votes, proposed = {}, {}
    present = set(ls(VOTE_DIR) or [])
    for voter in VOTERS:
        path = VOTE_DIR + voter + ".md"
        if path not in present:
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
    for path, (copy, digest, url) in V73.items():
        b = read(copy)
        if b is None or hashlib.sha256(b.encode("utf-8", "surrogateescape")).hexdigest() != digest:
            pins_ok = False
        norm[path] = ws(b or "")
    if not pins_ok:
        failed.append("pins")
    votes, proposed = final_votes(read, ls or (lambda _d: []))
    c = dict(rows=0, matched=0, status_ok=0, quote_ok=0, held=0, absent=0, holds=0, changed=0, voted=0, dissent=0)
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
            if len(cells) != 6:
                bad += 1
                continue
            h, entry, status, sid, qcell, disp = cells
            h = h.strip("` ")
            if h not in d or h in seen:
                bad += 1
                continue
            seen.add(h)
            c["matched"] += 1
            d_entry, path, q72 = d[h]
            if entry.strip("` ") != d_entry:
                bad += 1
            derived = "held" if q72 in norm[path] else "absent"
            c[derived] += 1
            if status == derived:
                c["status_ok"] += 1
            q = one_quote(qcell)
            if (q is not None and MIN_WORDS <= len(q.split(" ")) <= MAX_WORDS and q in norm[path]
                    and (derived != "held" or q == q72)):
                c["quote_ok"] += 1
            sid = sid.strip("` ")
            if sid not in row_cache:
                row_cache[sid] = sources_row(src_text, sid) if re.fullmatch(r"S[0-9]{3,}", sid) else None
            srow = row_cache[sid]
            ok_row = bool(srow and len(srow) == 11 and V73[path][2] in srow[1] and srow[7] == "mined"
                          and srow[8] == OPENED and LEDGER in [u.strip() for u in re.split(r"[,;]", srow[10])])
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
    line = ("C1=%s scope=%d rows=%d matched=%d status_ok=%d quote_ok=%d source_rows=%s pins=%s provenance=%s "
            "held=%d absent=%d holds=%d changed=%d voted=%d dissent=%d rev=%s"
            % ("met" if met else "unmet", len(d), c["rows"], c["matched"], c["status_ok"], c["quote_ok"], srows,
               "ok" if pins_ok else "bad", prov, c["held"], c["absent"], c["holds"], c["changed"], c["voted"],
               c["dissent"], rev))
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
        d = scope(git_reader(repo, ENTERING))
        for h, (entry, path, q) in sorted(d.items(), key=lambda kv: (kv[1][0], kv[1][1], kv[0])):
            print("h=%s entry=%s path=%s quote=%s" % (h, entry, path, q))
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
    d = scope(git_reader(repo, ENTERING))
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
    for path, (copy, digest, url) in V73.items():
        with open(os.path.join(lane, copy), "rb") as f:
            files[copy] = f.read().decode("utf-8", "surrogateescape")
    norm = {p: ws(files[V73[p][0]]) for p in V73}

    def words_at(path, needle, n):
        t = norm[path]
        i = t.index(needle)
        return " ".join(t[i:].split(" ")[:n])

    e1, e2 = ENTRIES
    held_q = words_at("mm/util.c", "allowed = ((totalram_pages() - hugetlb_total_pages())", 9)
    held_q2 = words_at("Documentation/mm/overcommit-accounting.rst", "In mode 2 the MAP_NORESERVE flag is ignored.", 8)
    held_q3 = words_at("Documentation/filesystems/proc.rst", "MemAvailable", 10)
    gone_q = "We honor MAP_NORESERVE if allowed to overcommit */ if (sysctl_overcommit_memory != OVERCOMMIT_NEVER) vm_flags |= VM_NORESERVE;"
    new_q = words_at("mm/mmap.c", "We honor MAP_NORESERVE if allowed to overcommit", 14)
    d = {
        "aaaaaaaaaaa1": (e2, "mm/util.c", held_q),
        "aaaaaaaaaaa2": (e2, "Documentation/mm/overcommit-accounting.rst", held_q2),
        "aaaaaaaaaaa3": (e1, "Documentation/filesystems/proc.rst", held_q3),
        "aaaaaaaaaaa4": (e2, "mm/mmap.c", gone_q),
    }
    sids = {p: "S9%02d" % (n + 1) for n, p in enumerate(V73)}

    def srow(path, status="mined", opened=OPENED, used=LEDGER, url=None, indent=""):
        return ("%s| %s | title — %s | code | A | scope | anchor v7.3 | teaches | %s | %s | on-release | %s |"
                % (indent, sids[path], url or V73[path][2], status, opened, used))

    def default_rows():
        out = []
        for h, (entry, path, q72) in sorted(d.items()):
            st = "held" if q72 in norm[path] else "absent"
            q = q72 if st == "held" else new_q
            out.append([h, entry, st, sids[path], "`%s`" % q.replace("|", "\\|"), "holds"])
        return out

    def build(rows=None, src_kw=None, votes="all", prov=True, extra_files=None):
        rows = default_rows() if rows is None else rows
        table = ["| h | entry | status | source | quote | disposition |", "|---|---|---|---|---|---|"]
        table += ["| " + " | ".join(r) + " |" for r in rows]
        head = (["source: " + ", ".join(sorted(set(sids.values()))), "verified-at: 2026-10-26",
                 "recheck: on-release — count-c1.py"] if prov else ["verified-at: 2026-10-26"])
        fl = dict(files)
        fl[LEDGER] = "\n".join(["# Recheck at v7.3", ""] + head + ["", "## Ledger", ""] + table + [""])
        kw = src_kw or {}
        fl["corpus/SOURCES.md"] = "\n".join(["| id | source |", "|---|---|"] + [srow(p, **kw) for p in V73])
        if votes == "all":
            for v in ("Mo53Fr01", "Mo53Fr07"):
                fl[VOTE_DIR + v + ".md"] = "\n".join("RECHECK %s %s — row" % (r[0], r[5]) for r in rows) + "\n"
        elif votes is not None:
            fl.update(votes(rows))
        fl.update(extra_files or {})
        return fl

    def run(fl, scope_d=None):
        lister = lambda dn: [p for p in fl if p.startswith(dn) and "/" not in p[len(dn):]]
        return evaluate(lambda p: fl.get(p), "R", d if scope_d is None else scope_d, ls=lister)

    checks = []

    def check(name, cond):
        checks.append((name, bool(cond)))

    met, line = run(build())
    check("honest_met", met and "scope=4 rows=4 matched=4 status_ok=4 quote_ok=4" in line
          and "held=3 absent=1" in line and "voted=4 dissent=0" in line)
    met, line = run({k: v for k, v in build().items() if k != LEDGER})
    check("ledger_absent_unmet", (not met) and "ledger_absent" in line)
    fl = build()
    fl[LEDGER] = "# staged\n\nsource: S901\nverified-at: x\nrecheck: y\n\nnothing yet\n"
    met, line = run(fl)
    check("no_table_unmet", (not met) and "table" in line and "rows" in line)
    rows = default_rows()[:-1]
    met, line = run(build(rows=rows))
    check("missing_row_unmet", (not met) and "rows" in line)
    rows = default_rows() + [["bbbbbbbbbbb9", e2, "held", sids["mm/util.c"], "`%s`" % held_q, "holds"]]
    met, line = run(build(rows=rows))
    check("extra_row_unmet", (not met) and "rows" in line and "bad_rows" in line)
    rows = default_rows() + [list(default_rows()[0])]
    met, line = run(build(rows=rows))
    check("duplicate_row_unmet", (not met) and "bad_rows" in line)
    rows = default_rows()
    rows[3][2] = "held"
    rows[3][4] = "`%s`" % gone_q.replace("|", "\\|")
    met, line = run(build(rows=rows))
    check("all_held_unmet", (not met) and "status" in line and "quote" in line)
    rows = default_rows()
    rows[0][2] = "absent"
    met, line = run(build(rows=rows))
    check("held_labelled_absent_unmet", (not met) and "status" in line and "status_ok=3" in line)
    rows = default_rows()
    rows[0][4] = "`%s`" % words_at("mm/util.c", "Committed memory limit enforced when OVERCOMMIT_NEVER", 8)
    met, line = run(build(rows=rows))
    check("held_with_other_quote_unmet", (not met) and "quote" in line)
    rows = default_rows()
    rows[3][4] = "`an invented quote of seven words here`"
    met, line = run(build(rows=rows))
    check("replacement_not_located_unmet", (not met) and "quote_ok=3" in line)
    rows = default_rows()
    rows[3][4] = "`vma_flags_set(&vma_flags, VMA_NORESERVE_BIT);`"
    met, line = run(build(rows=rows))
    check("replacement_too_short_unmet", (not met) and "quote" in line)
    rows = default_rows()
    rows[3][4] = "`%s`" % words_at("mm/util.c", "Committed memory limit enforced when OVERCOMMIT_NEVER", 8)
    met, line = run(build(rows=rows))
    check("replacement_from_other_file_unmet", (not met) and "quote" in line)
    rows = default_rows()
    rows[0][1] = e1
    met, line = run(build(rows=rows))
    check("wrong_entry_unmet", (not met) and "bad_rows" in line)
    rows = default_rows()
    rows[0][5] = "maybe"
    met, line = run(build(rows=rows))
    check("bad_disposition_unmet", (not met) and "bad_rows" in line)
    met, line = run(build(src_kw={"status": "queued"}))
    check("row_not_mined_unmet", (not met) and "source_rows=bad" in line)
    met, line = run(build(src_kw={"opened": "2026-10-25"}))
    check("row_opened_earlier_unmet", (not met) and "source_rows=bad" in line)
    met, line = run(build(src_kw={"used": "corpus/knowledge/other.md"}))
    check("row_usedby_unmet", (not met) and "source_rows=bad" in line)
    met, line = run(build(src_kw={"url": V72 + "mm/util.c"}))
    check("row_v72_url_unmet", (not met) and "source_rows=bad" in line)
    met, line = run(build(src_kw={"indent": "   "}))
    check("indented_rows_met", met)
    rows = default_rows()
    rows[0][3] = sids["mm/mmap.c"]
    met, line = run(build(rows=rows))
    check("row_other_path_unmet", (not met) and "source_rows=bad" in line)
    met, line = run(build(prov=False))
    check("provenance_unmet", (not met) and "provenance=bad" in line)
    fl = build()
    fl[V73["mm/util.c"][0]] = fl[V73["mm/util.c"][0]] + "\n"
    met, line = run(fl)
    check("pin_tampered_unmet", (not met) and "pins=bad" in line)
    fl = build()
    del fl[V73["mm/mmap.c"][0]]
    met, line = run(fl)
    check("pin_missing_unmet", (not met) and "pins=bad" in line)
    met, line = run(build(votes=None))
    check("no_votes_unmet", (not met) and "votes" in line and "voted=0" in line)
    met, line = run(build(votes=lambda rows: {VOTE_DIR + "Mo53Fr02.md":
                                              "\n".join("RECHECK %s holds" % r[0] for r in rows)}))
    check("one_voter_unmet", (not met) and "votes" in line)
    met, line = run(build(votes=lambda rows: {VOTE_DIR + "Mo53Fr02.md":
                                              "\n".join("RECHECK %s holds\nRECHECK %s holds" % (r[0], r[0])
                                                        for r in rows)}))
    check("same_voter_twice_unmet", (not met) and "votes" in line)
    met, line = run(build(votes=lambda rows: {VOTE_DIR + v + ".md": "\n".join("RECHECK %s holds" % r[0] for r in rows)
                                              for v in ("Mo53Exec01", "Mo53Rev02")}))
    check("non_voters_unmet", (not met) and "votes" in line)
    met, line = run(build(votes=lambda rows: {VOTE_DIR + v + ".md": "\n".join(["```"] + ["RECHECK %s holds" % r[0]
                                                                                          for r in rows] + ["```"])
                                              for v in ("Mo53Fr01", "Mo53Fr02")}))
    check("fenced_votes_unmet", (not met) and "votes" in line)
    met, line = run(build(votes=lambda rows: {VOTE_DIR + v + ".md": "\n".join("RECHECK %s holds" % r[0] for r in rows)
                                              for v in ("Mo53Fr01", "Mo53Fr02")} | {
        VOTE_DIR + "Mo53Fr03.md": "RECHECK %s changed\n" % rows[0][0]}))
    check("dissent_unmet", (not met) and "dissent=1" in line)
    met, line = run(build(votes=lambda rows: {VOTE_DIR + v + ".md": "\n".join("RECHECK %s holds" % r[0] for r in rows)
                                              for v in ("Mo53Fr01", "Mo53Fr02")} | {
        VOTE_DIR + "Mo53Fr03.md": "RECHECK %s changed\nRECHECK %s holds\n" % (rows[0][0], rows[0][0])}))
    check("revised_dissent_met", met and "dissent=0" in line)
    met, line = run(build(votes=lambda rows: {VOTE_DIR + v + ".md": "\n".join("RECHECK %s holds" % r[0] for r in rows)
                                              for v in ("Mo53Fr01", "Mo53Fr02")} | {
        VOTE_DIR + "Mo53Fr03.md": "```\nRECHECK %s changed\n```\n" % rows[0][0]}))
    check("fenced_dissent_ignored_met", met)
    met, line = run(build(votes=lambda rows: {VOTE_DIR + v + ".md": "\n".join("RECHECK %s holds" % r[0] for r in rows)
                                              for v in ("Mo53Fr01", "Mo53Exec09")} | {
        VOTE_DIR + "Mo53Exec08.md": "RECHECK %s changed\n" % rows[0][0]}))
    check("non_voter_dissent_ignored_but_one_voter_unmet", (not met) and "dissent=0" in line and "votes" in line)
    met, line = run(build(votes=lambda rows: {VOTE_DIR + v + ".md": "\n".join(
        ["QUOTE %s :: %s" % (rows[3][0], new_q)] + ["RECHECK %s holds" % r[0] for r in rows])
        for v in ("Mo53Fr01", "Mo53Fr02")}))
    check("author_vote_not_counted_unmet", (not met) and "votes" in line and "voted=3" in line)
    met, line = run(build(votes=lambda rows: {VOTE_DIR + v + ".md": "\n".join(
        ["```", "QUOTE %s :: %s" % (rows[3][0], new_q), "```"] + ["RECHECK %s holds" % r[0] for r in rows])
        for v in ("Mo53Fr01", "Mo53Fr02")}))
    check("fenced_quote_proposal_ignored_met", met)
    rows = default_rows()
    for r in rows:
        r[5] = "changed"
    met, line = run(build(rows=rows))
    check("all_changed_with_votes_met", met and "changed=4" in line)
    met, line = run(build(), scope_d={})
    check("empty_scope_unmet", not met)
    # scope reader over a synthetic entering tree
    ent = {
        "corpus/SOURCES.md": "\n".join([
            "| S001 | t — %smm/util.c | code | A | s | a | t | mined | 2026-10-26 | on-release | x |" % V72,
            "  | S002 | t — https://github.com/torvalds/linux/commit/abc.patch | code | A | s | a | t | mined | d | r | x |",
            "| S003 | t — %sDocumentation/mm/overcommit-accounting.rst | docs | A | s | a | t | mined | d | r | x |" % V72]),
        e1: "| claim | source | quote |\n|---|---|---|\n| one claim here | S001 | `%s` |\n| two claim | S002 | `x y z` |\n" % held_q,
        e2: "```\n| claim | source | quote |\n| fenced | S001 | `a` |\n```\n| claim | source | quote |\n|---|---|---|\n| three | S003 | `%s` |\n" % held_q2,
    }
    sd = scope(lambda p: ent.get(p))
    check("scope_reader", len(sd) == 2 and claim_hash("one claim here") in sd and claim_hash("three") in sd
          and claim_hash("two claim") not in sd and sd[claim_hash("three")][1] == "Documentation/mm/overcommit-accounting.rst")
    failn = 0
    for name, ok in checks:
        print("%s %s" % ("ok  " if ok else "FAIL", name))
        failn += 0 if ok else 1
    print("C1_SELFTEST pass=%d fail=%d" % (len(checks) - failn, failn))
    return 0 if failn == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
