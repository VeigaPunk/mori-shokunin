#!/usr/bin/env python3
"""Round 55 C2 counter (depth) — disk-runway exhaustion beyond the df block column: which statfs figure decides
ENOSPC on the filesystems the fleet writes (XFS /tmp and /fast, btrfs fleet root, tmpfs), the inode capacity a
block-only census never reads, btrfs's metadata-driven zero Avail and its sysfs allocation counters.

Frozen predicate P-C2 (same sentence in contract.md, this counter and the receipt label):
  At revision R, corpus/knowledge/disk-runway-enospc-r55.md opens with source: lines, verified-at: and
  recheck:, and carries a table whose header cells are claim, source, quote with at least 16 rows;
  each row's claim cell has at least 6 words, is unique in the table (case and whitespace folded) and
  carries at least 3 words of 3+ letters that are absent from its quote; each row's source cell is one
  S-id naming a corpus/SOURCES.md row at R that is mined, opened 2026-10-27, names its URL among
  the nine frozen sources below and lists the entry in used-by; each row's quote cell is one backticked
  span of 6 to 25 words (an escaped \\| reads as |), unique in the table, that occurs (whitespace
  collapsed) in the committed copy of that row's URL; the table draws on at least 6 of the 9 sources; every
  committed copy matches its frozen sha256; and (entailment arm) for every row, at least 2 distinct ENTAILMENT
  voters carry an unfenced line `ENTAIL <h> entailed` in their own report `.ufo/waves/round-55/w1/<voter>.md`
  at R, no ENTAILMENT voter carries an unfenced line `ENTAIL <h> overclaim`, a voter counts only when
  .ufo/waves/round-55/w1-results.json at R (the orchestrator's settlement record) lists a result whose name is
  that voter and whose output contains that same `ENTAIL <h> entailed` line (an `overclaim` line counts from the
  report alone), and a voter's `entailed` line does
  not count for a row whose text that voter wrote (its report carries an unfenced line `REPLACE <old> :: <text>`
  whose <text> hashes to <h>); <h> is the first 12 hex digits of the sha256 of the row's claim cell with
  whitespace collapsed and ends stripped; the ENTAILMENT voters are exactly the frozen VOTERS list below (no
  other file, no L1 file, no other directory counts).

Usage: count-c2.py <rev> [--repo DIR] [--entry PATH]   |   count-c2.py --selftest   |   count-c2.py --hashes <rev>
Output: `C2=met|unmet claims=N located=N quote_missing=N bad_rows=N sources=N source_rows=ok|bad pins=ok|bad
  provenance=ok|bad entailed=N dissent=N rev=R` (+ `failed=` list when unmet).
Exit 0 met, 1 unmet, 2 setup. Read-only: `git show` / `git ls-tree` / `git rev-parse` only.
Limits (named before data): a located quote proves the quoted words exist in the copy; the entailment arm proves
two ENTAILMENT seats that did not write the row text recorded `entailed` for that exact claim text, repeated in
the output the orchestrator captured, and no ENTAILMENT seat recorded `overclaim` — it does not prove the
judgment right, and seats are the lane, not outside verification; the results binding proves the orchestrator
recorded a seat of that name whose output repeats the vote line, not who wrote the report's bytes; a REPLACE line
is the only authorship signal the arm reads; v7.3 bytes say nothing about this host's 7.2.11 kernel beyond what a
seat observes live, and no ENOSPC was observed firing (every filesystem read here had free blocks and inodes).
"""
import hashlib
import html
import json
import os
import re
import subprocess
import sys

ENTRY = "corpus/knowledge/disk-runway-enospc-r55.md"
SRC_DIR = "corpus/evidence/sources-r55/"
ENTAIL_DIR = ".ufo/waves/round-55/w1/"
RESULTS = ".ufo/waves/round-55/w1-results.json"
VOTERS = ["Mo55En%02d" % i for i in range(1, 13)]
MIN_VOTES = 2
OPENED = ("2026-10-27",)
MIN_CLAIMS = 16
MIN_SOURCES = 6
MIN_CLAIM_WORDS = 6
MIN_BEYOND = 3
MIN_WORDS, MAX_WORDS = 6, 25
CGIT = "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/"
# url -> (committed copy, sha256 of the copy fetched 2026-10-27, kind)
MANP = "https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/"
COPIES = {
    CGIT + "include/uapi/asm-generic/errno-base.h?h=v7.3":
        (SRC_DIR + "errno-base.h.v7.3", "2c148e92b8318deeb767fabd60822113e575ee664ff09a1873aed8f7a495793c", "text"),
    CGIT + "fs/statfs.c?h=v7.3":
        (SRC_DIR + "statfs.c.v7.3", "34e684be1575eb3ce9938a01a8fd2d62e92b0be8fac1a46092884f7600905398", "text"),
    CGIT + "fs/xfs/xfs_super.c?h=v7.3":
        (SRC_DIR + "xfs_super.c.v7.3", "0f806bf4ea1859a482d8a7031e2e4c2a80835b3bdd15a4d5fb2ae11c91eed831", "text"),
    CGIT + "fs/btrfs/super.c?h=v7.3":
        (SRC_DIR + "btrfs_super.c.v7.3", "6715b89d60575dd4438710fab318c1a3f501f2df3b5c5c1d142ebc3c5eee43fc", "text"),
    CGIT + "fs/btrfs/sysfs.c?h=v7.3":
        (SRC_DIR + "btrfs_sysfs.c.v7.3", "098cb522131501deabde61ffcdc56138a8516098f4e980f9c34cb9e62b467377", "text"),
    CGIT + "Documentation/filesystems/tmpfs.rst?h=v7.3":
        (SRC_DIR + "tmpfs.rst.v7.3", "5ce3dffe9323912b9146a5f33744776ff623ef42cf8accd6b2dfbea0b9db5be6", "text"),
    MANP + "man2/statfs.2?h=man-pages-6.19":
        (SRC_DIR + "statfs.2.man-pages-6.19", "3dc4ed703d7e2b5edee6765ea33152c89671b6cde5d3ea6f4236160700713b9d", "text"),
    MANP + "man3/statvfs.3?h=man-pages-6.19":
        (SRC_DIR + "statvfs.3.man-pages-6.19", "5f65e9ce697bf5ce53207c0cc5811762275bcfb44a15f9e7c5a26a8606ae0b58", "text"),
    "https://raw.githubusercontent.com/coreutils/coreutils/v9.12/doc/coreutils.texi":
        (SRC_DIR + "coreutils.texi.v9.12", "e6521c9b2e677dd278820887d7ad94fad8260f2535dd923728462cdcb6148db9", "text"),
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
    outputs = {}
    try:
        res = json.loads(read(RESULTS) or "null")
        for r in (res or {}).get("results", []) if isinstance(res, dict) else []:
            if isinstance(r, dict) and isinstance(r.get("name"), str):
                outputs[r["name"]] = r.get("output") if isinstance(r.get("output"), str) else ""
    except (ValueError, TypeError, AttributeError):
        outputs = {}
    for voter in VOTERS:
        path = ENTAIL_DIR + voter + ".md"
        if path not in present or voter not in outputs:
            continue
        out = outputs[voter].replace("\\n", "\n")
        fence = False
        for line in (read(path) or "").split("\n"):
            if line.lstrip()[:3] in ("```", "~~~"):
                fence = not fence
                continue
            if fence:
                continue
            m = ENTAIL_RE.match(line)
            if m and (m.group(2) == "overclaim" or ("ENTAIL %s %s" % (m.group(1), m.group(2))) in out):
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
                          and srow[8] in OPENED
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
    import importlib.util
    here = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location("st2", os.path.join(here, "checks", "selftest-c2.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.run(sys.modules[__name__])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
