#!/usr/bin/env python3
"""Round 50 C2 counter (depth) — the memcg OOM report block and memory.stat (FR1 event-time attribution).

Frozen predicate P-C2 (same sentence in contract.md, this counter and the receipt label):
  At revision R, corpus/knowledge/oom-memcg-stat-r50.md opens with source: lines, verified-at: and
  recheck:, and carries a table whose header cells are claim, source, quote with at least 10 rows;
  each row's claim cell has at least 6 words, is unique in the table (case and whitespace folded) and
  carries at least 3 words of 3+ letters that are absent from its quote; each row's source cell is one
  S-id naming a corpus/SOURCES.md row at R that is mined, opened 2026-10-26, names its URL among the
  three frozen sources below and lists the entry in used-by; each row's quote cell is one backticked
  span of 6 to 25 words (an escaped \\| reads as |), unique in the table, that occurs (HTML copy:
  script, style and comment blocks dropped, tags stripped, entities decoded; every copy: whitespace
  collapsed) in the committed copy of that row's URL under corpus/evidence/sources-r50/; the table
  draws on all 3 sources; every committed copy matches its frozen sha256.

Usage: count-c2.py <rev> [--repo DIR] [--entry PATH]   |   count-c2.py --selftest
Output: `C2=met|unmet claims=N located=N quote_missing=N bad_rows=N sources=N
  source_rows=ok|bad pins=ok|bad provenance=ok|bad rev=R` (+ `failed=` list when unmet).
Exit 0 met, 1 unmet, 2 setup. Read-only: `git show` / `git rev-parse` only.
Limits (named before data): a located quote proves the quoted words exist in the copy, not that the
claim cell follows from them; the beyond-quote word floor is a floor, not entailment; a v7.2 copy says
nothing about kernels after v7.2 or about cgroup v1.
"""
import hashlib
import html
import os
import re
import subprocess
import sys

ENTRY = "corpus/knowledge/oom-memcg-stat-r50.md"
SRC_DIR = "corpus/evidence/sources-r50/"
OPENED = "2026-10-26"
MIN_CLAIMS = 10
MIN_SOURCES = 3
MIN_CLAIM_WORDS = 6
MIN_BEYOND = 3
MIN_WORDS, MAX_WORDS = 6, 25
# url -> (committed copy, sha256 of the copy fetched 2026-10-26, kind)
COPIES = {
    "https://docs.kernel.org/7.2/admin-guide/cgroup-v2.html":
        (SRC_DIR + "cgroup-v2.7.2.html", "2d716cb798eacf8fbcf431b52697fbb8c5ed8ea9f58ac15b2b55351247c0bf34", "html"),
    "https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/memcontrol.c":
        (SRC_DIR + "memcontrol.c.v7.2", "8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e", "text"),
    "https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c":
        (SRC_DIR + "oom_kill.c.v7.2", "452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e", "text"),
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


def sources_row(src_text, row_id):
    for line in src_text.split("\n"):
        if re.match(r"^ {0,3}\|\s*%s\s*\|" % re.escape(row_id), line):
            return split_cells(line)
    return None


def evaluate(read, rev, entry_path=None, copies=None):
    entry_path = entry_path or ENTRY
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
        if bad:
            failed.append("bad_rows")
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
            "provenance=%s rev=%s" % ("met" if met else "unmet", claims, located, missing, bad,
                                      len(used_sources), srows_ok, "ok" if pins_ok else "bad", prov, rev))
    if failed:
        line += " failed=" + ",".join(sorted(set(failed)))
    return met, line


def git_reader(repo, rev):
    def read(path):
        p = subprocess.run(["git", "-C", repo, "show", "%s:%s" % (rev, path)],
                           stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=60)
        return p.stdout.decode("utf-8", "surrogateescape") if p.returncode == 0 else None
    return read


def main(argv):
    if argv == ["--selftest"]:
        return selftest()
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
    met, line = evaluate(git_reader(repo, full), full, entry_path=entry)
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
        (urls[0], quote_from(urls[0], "Amount of memory used to cache filesystem data", 9)),
        (urls[0], quote_from(urls[0], "Amount of cached filesystem data that is swap-backed", 10)),
        (urls[0], quote_from(urls[0], "new entries can show up in the middle", 8)),
        (urls[0], quote_from(urls[0], "Amount of memory used in anonymous mappings", 8)),
        (urls[1], quote_from(urls[1], 'pr_info("Memory cgroup stats for ");', 6)),
        (urls[1], quote_from(urls[1], "void mem_cgroup_print_oom_meminfo(struct", 6)),
        (urls[1], quote_from(urls[1], "memory_failcnt = atomic_long_read(&memcg->memory_events[MEMCG_MAX]);", 6)),
        (urls[2], quote_from(urls[2], "if (is_memcg_oom(oc)) mem_cgroup_print_oom_meminfo(oc->memcg);", 6)),
        (urls[2], quote_from(urls[2], "static void dump_header(struct oom_control", 7)),
        (urls[2], quote_from(urls[2], 'pr_err("%s: Killed process %d (%s)', 8)),
    ]
    sids = {urls[0]: "S901", urls[1]: "S902", urls[2]: "S903"}

    def srow(url, sid, status="mined", opened=OPENED, used=ENTRY, indent=""):
        return ("%s| %s | title — %s | docs | A | scope | anchor | teaches | %s | %s | 180d | %s |"
                % (indent, sid, url, status, opened, used))

    def claim_text(i):
        return "observation number %d explains how the kernel report reads its counters" % i

    def build(claim_rows=None, drop=None, claims=None, **kw):
        rows = ["| claim | source | quote |", "|---|---|---|"]
        for i, (u, q) in enumerate(claim_rows or qs):
            c = claims[i] if claims else claim_text(i)
            rows.append("| %s | %s | `%s` |" % (c, sids[u], q.replace("|", "\\|")))
        entry = "\n".join([
            "# memcg OOM block", "",
            "source: S901 S902 S903", "verified-at: 2026-10-26",
            "recheck: 180d — `curl -s https://docs.kernel.org/7.2/admin-guide/cgroup-v2.html | grep -c memory.stat`", "",
            "## Claims", ""] + rows + [""])
        src = "\n".join(["| id | source |", "|---|---|"] + [
            srow(u, sids[u], **({k: v for k, v in kw.items() if k in ("status", "opened", "used", "indent")}
                                if drop != sids[u] else {"status": "queued"})) for u in urls])
        fl = dict(files)
        fl[ENTRY] = entry
        fl["corpus/SOURCES.md"] = src
        return fl

    def run(fl, **kw):
        return evaluate(lambda p: fl.get(p), "R", **kw)

    checks = []

    def check(name, cond):
        checks.append((name, bool(cond)))

    met, line = run(build())
    check("honest_met", met and "claims=10 located=10" in line and "sources=3" in line)
    met, line = run({k: v for k, v in build().items() if k != ENTRY})
    check("entry_absent_unmet", (not met) and "entry_absent" in line)
    fl = build(); fl[ENTRY] = "# staged\n\nsource: S901\nverified-at: x\nrecheck: y\n\nThe charge is typed.\n"
    met, line = run(fl)
    check("no_table_unmet", (not met) and "table" in line)
    bad_q = list(qs); bad_q[0] = (urls[0], "Amount of memory used to cache filesystem data entirely at random")
    met, line = run(build(claim_rows=bad_q))
    check("altered_quote_unmet", (not met) and "quote_missing=1" in line)
    swap = list(qs); swap[4] = (urls[1], quote_from(urls[0], "Amount of memory used to cache filesystem", 7))
    met, line = run(build(claim_rows=swap))
    check("quote_from_wrong_copy_unmet", (not met) and "quote_missing" in line)
    short = list(qs); short[3] = (urls[0], "memory.stat file")
    met, line = run(build(claim_rows=short))
    check("short_quote_unmet", (not met) and "bad_rows" in line)
    long_q = list(qs); long_q[3] = (urls[0], " ".join(["memory"] * 26))
    met, line = run(build(claim_rows=long_q))
    check("long_quote_unmet", (not met) and "bad_rows" in line)
    dup = list(qs); dup[1] = dup[0]
    met, line = run(build(claim_rows=dup))
    check("duplicate_quote_unmet", (not met) and "bad_rows" in line)
    met, line = run(build(claim_rows=qs[:9]))
    check("claims_floor_unmet", (not met) and "claims_floor" in line)
    two = [x for x in qs if x[0] != urls[2]]
    two = two + [(urls[0], quote_from(urls[0], "A read-only flat-keyed file which exists on non-root", 9)),
                 (urls[1], quote_from(urls[1], "static void memory_stat_format(struct mem_cgroup", 6)),
                 (urls[0], quote_from(urls[0], "All memory amounts are in bytes", 6))]
    met, line = run(build(claim_rows=two))
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
    fl = build(); fl[ENTRY] = fl[ENTRY].replace("source: S901 S902 S903", "source: S901 S902")
    met, line = run(fl)
    check("table_id_uncited_in_source_unmet", (not met) and "provenance" in line)
    fl = build(); fl[ENTRY] = fl[ENTRY].replace("verified-at: 2026-10-26\n", "")
    met, line = run(fl)
    check("verified_at_missing_unmet", (not met) and "provenance" in line)
    fl = build(); fl[ENTRY] = fl[ENTRY].replace("| claim | source | quote |", "| claim | source | evidence |")
    met, line = run(fl)
    check("header_wrong_unmet", (not met) and "table" in line)
    fl = build(claims=[claim_text(i) if i != 3 else "short claim" for i in range(10)])
    met, line = run(fl)
    check("claim_cell_short_unmet", (not met) and "bad_rows" in line)
    fl = build(claims=["the same claim repeated for every row of the table"] * 10)
    met, line = run(fl)
    check("breadcrumb_identical_claims_unmet", (not met) and "bad_rows=9" in line)
    echo = [q for u, q in qs]
    fl = build(claims=[q + " here" for q in echo])
    met, line = run(fl)
    check("claim_echoes_quote_unmet", (not met) and "bad_rows" in line)
    fl = build(); fl[ENTRY] = "```\n" + fl[ENTRY] + "\n```\n"
    met, line = run(fl)
    check("table_inside_fence_unseen_unmet", not met)
    met, line = run(build(), entry_path="corpus/knowledge/other.md")
    check("other_entry_path_unmet", not met)
    pipe = list(qs); pipe[9] = (urls[2], quote_from(urls[2], "if (points == LONG_MIN || points <", 8))
    met, line = run(build(claim_rows=pipe))
    check("escaped_pipe_quote_located", "||" in pipe[9][1] and met and "quote_missing=0" in line)
    check("words_beyond_counts", words_beyond("the anon bucket holds heap pages", "anon heap") == 4)
    check("text_copy_keeps_angle_brackets", "a < b" in normalise_text("if (a <   b) x > y"))
    check("normalise_drops_script_text", "alpha beta" not in normalise("<script>var x = 'alpha beta gamma';</script>visible words"))
    check("normalise_drops_style_text", "color red" not in normalise("<style>p { color red }</style>visible"))
    check("normalise_drops_comment_text", "hidden remark" not in normalise("<!-- hidden remark -->visible"))
    check("normalise_keeps_visible_text", "visible words" in normalise("<p>visible <b>words</b></p>"))
    for name, cond in checks:
        print("%s %s" % ("PASS" if cond else "FAIL", name))
    failn = sum(1 for _, c in checks if not c)
    print("C2_SELFTEST pass=%d fail=%d" % (len(checks) - failn, failn))
    return 0 if failn == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
