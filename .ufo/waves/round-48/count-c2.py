#!/usr/bin/env python3
"""Round 48 C2 counter (depth) — the filesystem-quota observability entry (FR2).

Frozen predicate P-C2 (same sentence in contract.md, this counter and the receipt label):
  At revision R, corpus/knowledge/quota-observability-r48.md opens with source: lines,
  verified-at: and recheck:, and carries a table whose header cells are claim, source,
  quote with at least 8 rows; each row's source cell is one S-id naming a corpus/SOURCES.md
  row at R that is mined, opened 2026-10-25, names its URL among the four frozen URLs below
  and lists the entry in used-by; each row's quote cell is one backticked span of 6 to 25
  words, unique in the table, that occurs (tags stripped, entities decoded, whitespace
  collapsed) in the committed copy of that row's URL under corpus/evidence/sources-r48/,
  and the table draws on at least 3 distinct sources; every committed copy matches its
  frozen sha256.

Usage: count-c2.py <rev> [--repo DIR] [--entry PATH]   |   count-c2.py --selftest
Output: `C2=met|unmet claims=N located=N quote_missing=N bad_rows=N sources=N
  source_rows=ok|bad pins=ok|bad provenance=ok|bad rev=R` (+ `failed=` list when unmet).
Exit 0 met, 1 unmet, 2 setup. Read-only: `git show` / `git rev-parse` only.
Limits (named before data): a located quote proves the quoted words exist in the copy, not
that the claim cell follows from them, and not that the copy is the live page today.
"""
import hashlib
import html
import os
import re
import subprocess
import sys

ENTRY = "corpus/knowledge/quota-observability-r48.md"
SRC_DIR = "corpus/evidence/sources-r48/"
OPENED = "2026-10-25"
MIN_CLAIMS = 8
MIN_SOURCES = 3
MIN_WORDS, MAX_WORDS = 6, 25
# url -> (committed copy, sha256 of the copy fetched 2026-10-25)
COPIES = {
    "https://man7.org/linux/man-pages/man8/xfs_quota.8.html":
        (SRC_DIR + "xfs_quota.8.html", "6375e40e9c0e950d78b38edbe9b7e7fdf5868d55be07040d4a029c552c437d5f"),
    "https://man7.org/linux/man-pages/man2/quotactl.2.html":
        (SRC_DIR + "quotactl.2.html", "0d4ab273503d078ee0d9765c616b5082514e7d86e2c6a6b16c70cb7fba8b6ee8"),
    "https://raw.githubusercontent.com/torvalds/linux/v7.2/include/uapi/asm-generic/errno.h":
        (SRC_DIR + "errno.h", "66a5ad60566fdd62e41701bcfc42bfeca5e5696ad1d47d78981575e0c51622be"),
    "https://help.aliyun.com/zh/nas/user-guide/set-quotas-on-the-subdirectories-of-nas-nfs-volumes":
        (SRC_DIR + "aliyun-nas-quota.html", "747fef1bcc8c6d6c18908f4534879922bebdaece1a476831d48be93c4e22719f"),
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


def normalise(text):
    t = re.sub(r"<[^>]+>", " ", text)
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
    for url, (path, digest) in copies.items():
        b = read(path)
        if b is None or hashlib.sha256(b.encode("utf-8", "surrogateescape")).hexdigest() != digest:
            pins_ok = False
        norm[url] = normalise(b or "")
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
        row_cache = {}
        ids_in_table = set()
        for cells in rows:
            if len(cells) != 3 or len(cells[0].split()) < 5:
                bad += 1
                continue
            sid = cells[1].strip("` ")
            quotes = SPAN.findall(cells[2])
            if not re.fullmatch(r"S[0-9]{3,}", sid) or len(quotes) != 1:
                bad += 1
                continue
            q = re.sub(r"\s+", " ", quotes[0]).strip()
            words = q.split(" ")
            if not (MIN_WORDS <= len(words) <= MAX_WORDS) or q in seen_quotes:
                bad += 1
                continue
            seen_quotes.add(q)
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
    for url, (path, digest) in COPIES.items():
        with open(os.path.join(lane, path), "rb") as f:
            files[path] = f.read().decode("utf-8", "surrogateescape")
    texts = {u: normalise(files[p]) for u, (p, d) in COPIES.items()}

    def quote_from(url, needle, n=8):
        t = texts[url]
        i = t.index(needle)
        return " ".join(t[i:].split(" ")[:n])

    urls = list(COPIES)
    qs = [
        (urls[0], quote_from(urls[0], "Quota exceeded", 3) if False else quote_from(urls[0], "distinguishes between quota accounting and limit enforcement", 8)),
        (urls[0], quote_from(urls[0], "may also take a long time", 6)),
        (urls[1], quote_from(urls[1], "No disk quota is found for the indicated user", 9)),
        (urls[1], quote_from(urls[1], "quotactl_fd", 6)),
        (urls[2], "#define EDQUOT 122 /* Quota exceeded */"),
        (urls[3], quote_from(urls[3], "Disk quota exceeded", 6)),
        (urls[0], quote_from(urls[0], "Quota exceeded", 6)),
        (urls[2], quote_from(urls[2], "ENOTRECOVERABLE", 6)),
    ]
    sids = {urls[0]: "S901", urls[1]: "S902", urls[2]: "S903", urls[3]: "S904"}

    def srow(url, sid, status="mined", opened=OPENED, used=ENTRY, indent=""):
        return ("%s| %s | title — %s | docs | A | scope | anchor | teaches | %s | %s | 180d | %s |"
                % (indent, sid, url, status, opened, used))

    def build(claim_rows=None, drop=None, **kw):
        rows = ["| claim | source | quote |", "|---|---|---|"]
        for i, (u, q) in enumerate(claim_rows or qs):
            rows.append("| claim number %d states a located fact | %s | `%s` |" % (i, sids[u], q))
        entry = "\n".join([
            "# Quota observability", "",
            "source: S901 S902 S903 S904", "verified-at: 2026-10-25",
            "recheck: 180d — `curl -s https://man7.org/linux/man-pages/man2/quotactl.2.html | grep -c ESRCH`", "",
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
    check("honest_met", met and "claims=8 located=8" in line)
    met, line = run({k: v for k, v in build().items() if k != ENTRY})
    check("entry_absent_unmet", (not met) and "entry_absent" in line)
    fl = build(); fl[ENTRY] = "# staged\n\nsource: S901\nverified-at: x\nrecheck: y\n\nThe OOM lifecycle is three named tracepoints.\n"
    met, line = run(fl)
    check("no_table_unmet", (not met) and "table" in line)
    bad_q = list(qs); bad_q[0] = (urls[0], "XFS distinguishes between quota accounting and disk fullness entirely")
    met, line = run(build(claim_rows=bad_q))
    check("altered_quote_unmet", (not met) and "quote_missing=1" in line)
    swap = list(qs); swap[2] = (urls[1], quote_from(urls[0], "may also take a long time", 6) + " x")
    met, line = run(build(claim_rows=swap))
    check("quote_from_wrong_copy_unmet", (not met) and "quote_missing" in line)
    short = list(qs); short[3] = (urls[1], "quotactl_fd addresses")
    met, line = run(build(claim_rows=short))
    check("short_quote_unmet", (not met) and "bad_rows" in line)
    long_q = list(qs); long_q[3] = (urls[1], " ".join(["quotactl_fd"] * 26))
    met, line = run(build(claim_rows=long_q))
    check("long_quote_unmet", (not met) and "bad_rows" in line)
    dup = list(qs); dup[1] = dup[0]
    met, line = run(build(claim_rows=dup))
    check("duplicate_quote_unmet", (not met) and "bad_rows" in line)
    met, line = run(build(claim_rows=qs[:7]))
    check("claims_floor_unmet", (not met) and "claims_floor" in line)
    only2 = [(urls[0], q) for u, q in qs if u == urls[0]] + [(urls[1], q) for u, q in qs if u == urls[1]]
    only2 = only2 + only2[:1]
    met, line = run(build(claim_rows=only2[:8] if len(only2) >= 8 else only2))
    check("sources_floor_unmet", not met)
    met, line = run(build(status="queued"))
    check("row_not_mined_unmet", (not met) and "bad_rows" in line)
    met, line = run(build(opened="2026-10-24"))
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
    fl = build(); fl[ENTRY] = fl[ENTRY].replace("source: S901 S902 S903 S904", "source: S901 S902 S903")
    met, line = run(fl)
    check("table_id_uncited_in_source_unmet", (not met) and "provenance" in line)
    fl = build(); fl[ENTRY] = fl[ENTRY].replace("verified-at: 2026-10-25\n", "")
    met, line = run(fl)
    check("verified_at_missing_unmet", (not met) and "provenance" in line)
    fl = build(); fl[ENTRY] = fl[ENTRY].replace("| claim | source | quote |", "| claim | source | evidence |")
    met, line = run(fl)
    check("header_wrong_unmet", (not met) and "table" in line)
    fl = build(); fl[ENTRY] = fl[ENTRY].replace("| claim number 3 states a located fact |", "| short |")
    met, line = run(fl)
    check("claim_cell_short_unmet", (not met) and "bad_rows" in line)
    fl = build(); fl[ENTRY] = fl[ENTRY].replace("```", "") ; fl[ENTRY] = "```\n" + fl[ENTRY] + "\n```\n"
    met, line = run(fl)
    check("table_inside_fence_unseen_unmet", not met)
    met, line = run(build(), entry_path="corpus/knowledge/other.md")
    check("other_entry_path_unmet", not met)
    for name, cond in checks:
        print("%s %s" % ("PASS" if cond else "FAIL", name))
    failn = sum(1 for _, c in checks if not c)
    print("C2_SELFTEST pass=%d fail=%d" % (len(checks) - failn, failn))
    return 0 if failn == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
