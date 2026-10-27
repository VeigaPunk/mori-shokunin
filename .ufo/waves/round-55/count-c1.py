#!/usr/bin/env python3
"""Round 55 C1 counter (freshness) — the line pointers into Linux v7.2 files that the lane's prose and catalogue
entries carry, re-located at Linux v7.3.

Frozen predicate P-C1 (same sentence in contract.md, this counter and the receipt label):
  At revision R, corpus/knowledge/kernel-v7.3-recheck-r55.md opens with source:, verified-at: and recheck: lines
  and carries a table whose header cells are hash, entry, pointer, v7.3 source, v7.3 lines, status, disposition
  with exactly one row for every pointer in SCOPE — SCOPE being every pointer the frozen extractor below finds in
  the four entries ENTRIES as they stand at the entering tip ENTER (a `<file>:<lines>` token or a backticked
  `:<lines>` continuation of the last file on the same line, or in oom-tracepoints-r47.md a `header line(s)
  <lines>` token, whose file basename is the basename of a path that a Linux v7.2-pinned corpus/SOURCES.md row
  cited by that entry names), keyed by the first 12 hex digits of sha256("<entry>|<v7.2 path>|<lines>"); for
  every scoped row the entry and pointer cells name that entry and `<path>:<lines>`; the v7.3 source cell is one
  S-id naming a corpus/SOURCES.md row at R that is mined, opened 2026-10-26 or 2026-10-27, carries the frozen v7.3 URL of that
  path and lists the ledger in used-by; the v7.3 lines cell has as many comma-separated pieces as the v7.2
  pointer and every piece lies inside the committed v7.3 copy; the status cell equals the status the counter
  derives — `broken` when a v7.2 piece lies outside the committed v7.2 copy, otherwise per piece the v7.2 lines
  (each line stripped, inner whitespace collapsed) compared with the v7.3 lines the row names: equal at the
  same numbers → `same`, equal at other numbers → `moved`, unequal → `changed`, which counts only when that
  v7.2 block occurs nowhere in the v7.3 copy as consecutive lines (a v7.2 block that does occur but was not
  located is a line failure); the row's status is `broken`, else `changed` if any piece is changed, else
  `moved` if any piece moved, else `same`; the disposition cell is `holds` or `stale`; every committed copy
  matches its frozen sha256; and (vote arm) at least 2 distinct RECHECK voters' final unfenced line
  `RECHECK <h> <word>` for that hash carries the row's disposition and no RECHECK voter's final word for it
  differs, where a voter counts only when .ufo/waves/round-55/w1-results.json at R lists a result whose name is
  that voter, an agreeing vote counts only when that result's output contains that same final `RECHECK <h> <word>`
  line (a differing final word counts as dissent from the report alone), and the voter's report is
  .ufo/waves/round-55/w1/<voter>.md at R; the RECHECK voters are exactly the frozen VOTERS list.

Usage: count-c1.py <rev> [--repo DIR]   |   count-c1.py --selftest   |   count-c1.py --scope
Output: `C1=met|unmet scope=N rows=N matched=N status_ok=N line_ok=N source_rows=ok|bad pins=ok|bad
  provenance=ok|bad same=N moved=N changed=N broken=N holds=N stale=N voted=N dissent=N rev=R`
  (+ `failed=` list when unmet). Exit 0 met, 1 unmet, 2 setup. Read-only: git show / ls-tree / rev-parse only.
Limits (named before data): the status arm proves where the cited v7.2 lines now sit or that they no longer
occur verbatim; it does not prove that the entry's sentence citing them still means the same thing — the
disposition and its votes carry the meaning, and votes are lane seats, not outside verification; the results
binding proves the orchestrator recorded a seat of that name whose output repeats the vote line, not who wrote
the report bytes; the extractor sees line pointers only — a v7.2 fact cited by S-id without a line number
(watchdog-identity-r31.md cites its kernel rows that way) is outside SCOPE; the pins prove the bytes are what
the L1 fetched — wave seats re-fetch them independently.
"""
import hashlib
import json
import os
import re
import subprocess
import sys

ENTER = "ca52426ea496bc6592e3e867cc9d28843e45f196"
ENTRIES = ["corpus/knowledge/oom-tracepoints-r47.md", "corpus/knowledge/system-pressure-r24.md",
           "corpus/knowledge/watchdog-identity-r31.md", "corpus/knowledge/oom-victim-selection-r27.md"]
LEDGER = "corpus/knowledge/kernel-v7.3-recheck-r55.md"
SRC = "corpus/evidence/sources-r55/"
VOTE_DIR = ".ufo/waves/round-55/w1/"
RESULTS = ".ufo/waves/round-55/w1-results.json"
VOTERS = ["Mo55Rc%02d" % i for i in range(1, 17)]
MIN_VOTES = 2
OPENED = ("2026-10-26", "2026-10-27")
CGIT = "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/"
HEADER = ["hash", "entry", "pointer", "v7.3 source", "v7.3 lines", "status", "disposition"]
# v7.2 path -> (v7.2 copy, sha256, v7.3 copy, sha256); v7.3 URL is CGIT + path + "?h=v7.3"
COPIES = {
    "fs/proc/base.c":
        ("corpus/evidence/sources-r47/fs_proc_base.c", "cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6",
         "corpus/evidence/sources-r55/fs_proc_base.c.v7.3", "fb419e9a64d617039d5e90d53f0d634a0a2d4d1d9b1e99698b04e9412df38d5c"),
    "mm/page_alloc.c":
        ("corpus/evidence/sources-r47/mm_page_alloc.c", "439ae8ec1e47cbf38770865e53e98bf2229e32a20c4b0f8178e6f19f34edbc50",
         "corpus/evidence/sources-r55/mm_page_alloc.c.v7.3", "315ef97b0ec1c6d759fe1d57c79177c2fcf00f5228bd8895ff718aa265fda33c"),
    "mm/oom_kill.c":
        ("corpus/evidence/sources-r50/oom_kill.c.v7.2", "452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e",
         "corpus/evidence/sources-r54/oom_kill.c.v7.3", "452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e"),
    "include/trace/events/oom.h":
        ("corpus/evidence/sources-r47/include_trace_events_oom.h", "82f04ad4108ba9499b638fe298967f124269c0a2feb6ddbb14b1ade59c974e0d",
         "corpus/evidence/sources-r55/include_trace_events_oom.h.v7.3", "82f04ad4108ba9499b638fe298967f124269c0a2feb6ddbb14b1ade59c974e0d"),
    "Documentation/accounting/psi.rst":
        ("corpus/evidence/sources-r55/Documentation_accounting_psi.rst.v7.2", "11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692",
         "corpus/evidence/sources-r55/Documentation_accounting_psi.rst.v7.3", "11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692"),
    "kernel/sched/psi.c":
        ("corpus/evidence/sources-r55/kernel_sched_psi.c.v7.2", "452318beaca3e6d19ab81a16528ae6b1695828a9ed080e329d07dedd9a3312c5",
         "corpus/evidence/sources-r55/kernel_sched_psi.c.v7.3", "c4edc1e7c18ca76e6e29668093fa0b26d4251cb088f2d5feab24681f285ec63f"),
    "include/linux/psi_types.h":
        ("corpus/evidence/sources-r55/include_linux_psi_types.h.v7.2", "483269b27c82b438450632555aba2ba8a9c47b608243f78a029c4300b3618ccc",
         "corpus/evidence/sources-r55/include_linux_psi_types.h.v7.3", "483269b27c82b438450632555aba2ba8a9c47b608243f78a029c4300b3618ccc"),
    "Documentation/admin-guide/kernel-parameters.txt":
        ("corpus/evidence/sources-r55/Documentation_admin-guide_kernel-parameters.txt.v7.2", "23b1a690210b6884f040a6b1e5baf1fc18856e844d30d4784470bd210953340c",
         "corpus/evidence/sources-r55/Documentation_admin-guide_kernel-parameters.txt.v7.3", "b5a13c038a27e688380bbcaa8cdbcad24543ad6b64de0c3d5709bc32c94cb39a"),
    "Documentation/admin-guide/cgroup-v2.rst":
        ("corpus/evidence/sources-r55/Documentation_admin-guide_cgroup-v2.rst.v7.2", "a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad",
         "corpus/evidence/sources-r55/Documentation_admin-guide_cgroup-v2.rst.v7.3", "2750c11a6324e18f4d3a9bb63032b55f3268bd7077b80897af2f15a712611b68"),
    "Documentation/filesystems/proc.rst":
        ("corpus/evidence/sources-r51/proc.rst.v7.2", "e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126",
         "corpus/evidence/sources-r53/proc.rst.v7.3", "bc178ff511e05c1b5e0c2413feb18223edcaeb2797ce499b714b98120cabf3c8"),
    "kernel/fork.c":
        ("corpus/evidence/sources-r55/kernel_fork.c.v7.2", "359882ea981b58f5289293e5644f7c0085a8350e4f1937f39dcb94ae1cd0dd1d",
         "corpus/evidence/sources-r55/kernel_fork.c.v7.3", "fa32ca5a79d4d00076022c959a452d936d31edfa0f3c0d4ef2774e0ea6ac0ba0"),
}

SPEC = r"([0-9]+(?:[-–][0-9]+)?(?:,\s?[0-9]+(?:[-–][0-9]+)?)*)"
TOKEN = re.compile(r"(?<![A-Za-z0-9_./-])((?:[A-Za-z0-9_.-]+/)*[A-Za-z0-9_-]+(?:\.[A-Za-z0-9]+)+|Kconfig):" + SPEC
                   + r"|`:" + SPEC + "`")
HEADER_LINES = re.compile(r"\bheader lines?\s+" + SPEC)
PIN72 = re.compile(r"(\?h=v7\.2\b|/v7\.2/|@v7\.2/|docs\.kernel\.org/7\.2/)")
SID = re.compile(r"\bS[0-9]{3,}\b")


def split_cells(line):
    s = line.strip()
    parts = re.split(r"(?<!\\)\|", s)
    parts = parts[1:-1] if s.endswith("|") else parts[1:]
    return [p.strip() for p in parts]


def registry(src_text):
    rows = {}
    for line in (src_text or "").split("\n"):
        m = re.match(r"^ {0,3}\|\s*(S[0-9]{3,})\s*\|", line)
        if m and m.group(1) not in rows:
            rows[m.group(1)] = split_cells(line)
    return rows


def v72_paths(cells):
    out = []
    for u in re.findall(r"https?://[^\s;,)]+", cells[1] if len(cells) > 1 else ""):
        if not PIN72.search(u):
            continue
        m = (re.search(r"(?:/v7\.2/|@v7\.2/)(.+)$", u) or re.search(r"/plain/(.+)\?h=v7\.2$", u))
        if m:
            out.append(m.group(1))
    return out


def norm_spec(spec):
    return re.sub(r"\s", "", spec).replace("–", "-")


def scope(read_enter):
    """Frozen extractor: list of (hash, entry, path, spec) in first-seen order, unique by (entry, path, spec)."""
    reg = registry(read_enter("corpus/SOURCES.md"))
    seen, out = set(), []
    for entry in ENTRIES:
        text = read_enter(entry) or ""
        cited = set(SID.findall(text))
        bmap = {}
        for sid in sorted(cited):
            if sid in reg:
                for p in v72_paths(reg[sid]):
                    bmap.setdefault(p.split("/")[-1], set()).add(p)
        for line in text.split("\n"):
            found = []
            last = None
            for m in TOKEN.finditer(line):
                if m.group(1):
                    base, spec = m.group(1).split("/")[-1], m.group(2)
                    last = base
                elif last is not None:
                    base, spec = last, m.group(3)
                else:
                    continue
                found.append((m.start(), base, spec))
            if entry.endswith("oom-tracepoints-r47.md"):
                for m in HEADER_LINES.finditer(line):
                    found.append((m.start(), "oom.h", m.group(1)))
            for _, base, spec in sorted(found):
                paths = bmap.get(base, set())
                if len(paths) != 1:
                    continue
                path = next(iter(paths))
                spec = norm_spec(spec)
                key = (entry, path, spec)
                if key in seen:
                    continue
                seen.add(key)
                h = hashlib.sha256(("%s|%s|%s" % key).encode()).hexdigest()[:12]
                out.append((h, entry, path, spec))
    return out


def pieces(spec):
    out = []
    for p in spec.split(","):
        if not p:
            return None
        if "-" in p:
            a, b = p.split("-", 1)
            if not (a.isdigit() and b.isdigit()):
                return None
            a, b = int(a), int(b)
        elif p.isdigit():
            a = b = int(p)
        else:
            return None
        if a < 1 or b < a:
            return None
        out.append((a, b))
    return out


def nl(line):
    return re.sub(r"\s+", " ", line).strip()


def block(lines, a, b):
    if b > len(lines):
        return None
    return [nl(x) for x in lines[a - 1:b]]


def occurs(lines_n, blk):
    n = len(blk)
    for i in range(0, len(lines_n) - n + 1):
        if lines_n[i:i + n] == blk:
            return True
    return False


def derive(v72_lines, v73_lines, p72, p73):
    """-> (status, line_ok) for one pointer; p72/p73 piece lists (p73 may be None)."""
    for a, b in p72:
        if b > len(v72_lines):
            return "broken", True
    if p73 is None or len(p73) != len(p72):
        return None, False
    n73 = [nl(x) for x in v73_lines]
    st = []
    for (a, b), (c, d) in zip(p72, p73):
        blk72 = block(v72_lines, a, b)
        blk73 = block(v73_lines, c, d)
        if blk73 is None:
            return None, False
        if blk72 == blk73:
            st.append("same" if (a, b) == (c, d) else "moved")
        elif occurs(n73, blk72):
            return None, False
        else:
            st.append("changed")
    if "changed" in st:
        return "changed", True
    if "moved" in st:
        return "moved", True
    return "same", True


def parse_ledger(text):
    rows, header, fence = [], None, False
    for line in (text or "").split("\n"):
        if line.lstrip()[:3] in ("```", "~~~"):
            fence = not fence
            continue
        if fence:
            continue
        if not line.lstrip().startswith("|"):
            if header is not None and rows:
                break
            continue
        cells = split_cells(line)
        if header is None:
            if [c.lower() for c in cells] == HEADER:
                header = HEADER
            continue
        if all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
            continue
        rows.append(cells)
    return header, rows


VOTE_RE = re.compile(r"^\s*RECHECK\s+([0-9a-f]{12})\s+(holds|stale)\b")


def final_votes(text):
    fence, last = False, {}
    for line in (text or "").split("\n"):
        if line.lstrip()[:3] in ("```", "~~~"):
            fence = not fence
            continue
        if fence:
            continue
        m = VOTE_RE.match(line)
        if m:
            last[m.group(1)] = m.group(2)
    return last


def votes(read, ls):
    present = set(ls(VOTE_DIR) or [])
    outputs = {}
    try:
        res = json.loads(read(RESULTS) or "null")
        for r in (res or {}).get("results", []) if isinstance(res, dict) else []:
            if isinstance(r, dict) and isinstance(r.get("name"), str):
                outputs[r["name"]] = r.get("output") if isinstance(r.get("output"), str) else ""
    except (ValueError, TypeError, AttributeError):
        outputs = {}
    per = {}
    for voter in VOTERS:
        path = VOTE_DIR + voter + ".md"
        if path not in present:
            continue
        out_lines = set(l.strip() for l in outputs.get(voter, "").replace("\\n", "\n").split("\n"))
        for h, w in final_votes(read(path)).items():
            bound = voter in outputs and any(l == "RECHECK %s %s" % (h, w) or l.startswith("RECHECK %s %s ")
                                              for l in out_lines)
            per.setdefault(h, {})[voter] = (w, bound)
    return per


def evaluate(read, rev, read_enter, ls=None, copies=None):
    copies = copies if copies is not None else COPIES
    failed = []
    texts = {}
    pins_ok = bool(copies)
    for path, (c72, d72, c73, d73) in copies.items():
        for c, d in ((c72, d72), (c73, d73)):
            b = read(c)
            if b is None or hashlib.sha256(b.encode("utf-8", "surrogateescape")).hexdigest() != d:
                pins_ok = False
            texts[c] = (b or "").split("\n")
            if texts[c] and texts[c][-1] == "":
                texts[c] = texts[c][:-1]
    if not pins_ok:
        failed.append("pins")
    sc = scope(read_enter)
    ledger = read(LEDGER)
    per = votes(read, ls or (lambda d: []))
    rows = matched = status_ok = line_ok = voted = dissent = 0
    counts = {"same": 0, "moved": 0, "changed": 0, "broken": 0, "holds": 0, "stale": 0}
    prov = "bad"
    srows = "bad"
    if ledger is None:
        failed.append("ledger_absent")
    else:
        head = [l for l in ledger.split("\n") if l.strip()][:14]
        has = lambda k: any(re.match(r"^[-* ]*%s\s*:" % k, l) for l in head)
        src_lines = [l for l in head if re.match(r"^[-* ]*source\s*:", l)]
        header, lrows = parse_ledger(ledger)
        if header is None:
            failed.append("table")
            lrows = []
        rows = len(lrows)
        byhash = {}
        dup = False
        for cells in lrows:
            if len(cells) == 7:
                h = cells[0].strip("` ")
                if h in byhash:
                    dup = True
                byhash[h] = cells
        reg = registry(read("corpus/SOURCES.md"))
        bad_src = False
        used_ids = set()
        scoped = set(h for h, _, _, _ in sc)
        extra = [h for h in byhash if h not in scoped]
        for h, entry, path, spec in sc:
            cells = byhash.get(h)
            if not cells:
                continue
            if cells[1].strip("` ") != entry or cells[2].strip("` ") != "%s:%s" % (path, spec):
                continue
            matched += 1
            sid = cells[3].strip("` ")
            srow = reg.get(sid)
            url = CGIT + path + "?h=v7.3"
            ok_row = bool(srow and len(srow) == 11 and url in srow[1].split() and srow[7] == "mined"
                          and srow[8] in OPENED and LEDGER in [u.strip() for u in re.split(r"[,;]", srow[10])])
            if not ok_row or path not in copies:
                bad_src = True
            else:
                used_ids.add(sid)
            c72, _, c73, _ = copies.get(path, (None, None, None, None))
            p72 = pieces(spec)
            p73 = pieces(cells[4].strip("` ").replace(" ", "").replace("–", "-"))
            st, lok = (derive(texts.get(c72, []), texts.get(c73, []), p72, p73) if (c72 and p72)
                       else (None, False))
            if lok:
                line_ok += 1
            status = cells[5].strip("` ").lower()
            if st is not None and status == st:
                status_ok += 1
                counts[st] += 1
            disp = cells[6].strip("` ").lower().split(" ")[0] if cells[6].strip() else ""
            if disp in ("holds", "stale"):
                counts[disp] += 1
                v = per.get(h, {})
                agree = [w for w, bound in v.values() if w == disp and bound]
                other = [w for w, bound in v.values() if w != disp]
                if other:
                    dissent += 1
                elif len(agree) >= MIN_VOTES:
                    voted += 1
        if dup or extra or rows != len(sc):
            failed.append("rows")
        if matched != len(sc):
            failed.append("matched")
        if status_ok != len(sc):
            failed.append("status")
        if line_ok != len(sc):
            failed.append("line")
        if bad_src or not used_ids:
            failed.append("source_rows")
        else:
            srows = "ok"
        if voted != len(sc) or dissent:
            failed.append("votes")
        cited = set()
        for l in src_lines:
            cited |= set(SID.findall(l))
        if has("source") and has("verified-at") and has("recheck") and used_ids and used_ids <= cited:
            prov = "ok"
        else:
            failed.append("provenance")
    if not sc:
        failed.append("scope_empty")
    met = not failed
    line = ("C1=%s scope=%d rows=%d matched=%d status_ok=%d line_ok=%d source_rows=%s pins=%s provenance=%s "
            "same=%d moved=%d changed=%d broken=%d holds=%d stale=%d voted=%d dissent=%d rev=%s"
            % ("met" if met else "unmet", len(sc), rows, matched, status_ok, line_ok, srows,
               "ok" if pins_ok else "bad", prov, counts["same"], counts["moved"], counts["changed"],
               counts["broken"], counts["holds"], counts["stale"], voted, dissent, rev))
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


def lane_root():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def main(argv):
    if argv == ["--selftest"]:
        import importlib.util
        here = os.path.dirname(os.path.abspath(__file__))
        spec = importlib.util.spec_from_file_location("st1", os.path.join(here, "checks", "selftest-c1.py"))
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        return m.run(sys.modules[__name__])
    args = list(argv)
    repo = lane_root()
    while "--repo" in args:
        i = args.index("--repo"); repo = args[i + 1]; del args[i:i + 2]
    if args == ["--scope"]:
        for h, entry, path, spec in scope(git_reader(repo, ENTER)):
            print("%s %s %s:%s" % (h, entry, path, spec))
        return 0
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
    if git_reader(repo, ENTER)("corpus/SOURCES.md") is None:
        print("C1_SETUP entering tip %s unreadable" % ENTER, file=sys.stderr)
        return 2
    met, line = evaluate(git_reader(repo, full), full, git_reader(repo, ENTER), ls=git_lister(repo, full))
    print(line)
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
