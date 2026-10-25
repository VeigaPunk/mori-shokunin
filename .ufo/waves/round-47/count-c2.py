#!/usr/bin/env python3
"""Round 47 C2 counter (depth) — the OOM tracepoint catalogue entry.

Frozen predicate P-C2 (same sentence in contract.md, this counter and the
receipt label):
  At revision R, corpus/knowledge/oom-tracepoints-r47.md opens with source:
  (citing S475), verified-at: and recheck:, and carries a table whose header's
  first cell is `tracepoint` with one row per TRACE_EVENT in the committed
  copy of Linux v7.2 include/trace/events/oom.h — the row's backticked
  tracepoint name set equals the header's event set, each row's backticked
  field set equals that event's TP_STRUCT__entry field set, and each row's
  `emitted in` path is a committed v7.2 copy containing `trace_<name>(` —
  every committed copy matching its frozen sha256; and corpus/SOURCES.md at R
  carries S475 as a mined tier-A code row naming v7.2 and
  include/trace/events/oom.h whose used-by names the entry.

Usage: count-c2.py <rev> [--repo DIR] [--entry PATH]   |   count-c2.py --selftest
Output: `C2=met|unmet events=N rows=N name_mismatch=N field_mismatch=N
  callsite_mismatch=N pin_mismatch=N source_row=ok|bad provenance=ok|bad rev=R`
  (+ `failed=` list when unmet). Exit 0 met, 1 unmet, 2 setup.
Read-only: `git show` / `git rev-parse` only.
"""
import hashlib
import os
import re
import subprocess
import sys

ROW_ID = "S475"
ENTRY = "corpus/knowledge/oom-tracepoints-r47.md"
SRC_DIR = "corpus/evidence/sources-r47/"
OOM_H = SRC_DIR + "include_trace_events_oom.h"
# Frozen sha256 of the v7.2 copies fetched 2026-10-25 from
# https://raw.githubusercontent.com/torvalds/linux/v7.2/<path>
PINS = {
    SRC_DIR + "include_trace_events_oom.h": "82f04ad4108ba9499b638fe298967f124269c0a2feb6ddbb14b1ade59c974e0d",
    SRC_DIR + "mm_oom_kill.c": "452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e",
    SRC_DIR + "mm_page_alloc.c": "439ae8ec1e47cbf38770865e53e98bf2229e32a20c4b0f8178e6f19f34edbc50",
    SRC_DIR + "fs_proc_base.c": "cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6",
}
# kernel path named in the entry -> committed copy
COPY_OF = {
    "mm/oom_kill.c": SRC_DIR + "mm_oom_kill.c",
    "mm/page_alloc.c": SRC_DIR + "mm_page_alloc.c",
    "fs/proc/base.c": SRC_DIR + "fs_proc_base.c",
}
SPAN = re.compile(r"`([^`]+)`")


def parse_events(header_text):
    """{event: set(fields)} from TRACE_EVENT(...) blocks' TP_STRUCT__entry."""
    events = {}
    for m in re.finditer(r"^TRACE_EVENT\((\w+),", header_text, re.M):
        name = m.group(1)
        rest = header_text[m.end():]
        nxt = re.search(r"^TRACE_EVENT\(", rest, re.M)
        block = rest[:nxt.start()] if nxt else rest
        sm = re.search(r"TP_STRUCT__entry\((.*?)\n\s*\),", block, re.S)
        fields = set()
        if sm:
            body = sm.group(1)
            for fm in re.finditer(r"__(field|field_struct|array|dynamic_array)\(\s*[^,]+?,\s*(\w+)", body):
                fields.add(fm.group(2))
            for fm in re.finditer(r"__string\(\s*(\w+)\s*,", body):
                fields.add(fm.group(1))
        events[name] = fields
    return events


def split_cells(line):
    parts = re.split(r"(?<!\\)\|", line.strip())
    return [p.strip() for p in parts[1:-1]]


def parse_table(entry_text):
    rows, header = [], None
    for line in entry_text.split("\n"):
        if not line.strip().startswith("|"):
            if header is not None and rows:
                break
            header = None if not line.strip() else header
            continue
        cells = split_cells(line)
        if header is None:
            if cells and cells[0].lower() == "tracepoint":
                header = [c.lower() for c in cells]
            continue
        if all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
            continue
        rows.append(cells)
    return header, rows


def sources_row(src_text, row_id):
    for line in src_text.split("\n"):
        if re.match(r"^ {0,3}\|\s*%s\s*\|" % row_id, line):
            return split_cells(line)
    return None


def evaluate(read, pins, rev):
    """read(path) -> str|None at the measured revision."""
    failed = []
    c = {"name_mismatch": 0, "field_mismatch": 0, "callsite_mismatch": 0, "pin_mismatch": 0}
    blobs = {}
    for path, digest in pins.items():
        b = read(path)
        blobs[path] = b
        if b is None or hashlib.sha256(b.encode("utf-8", "surrogateescape")).hexdigest() != digest:
            c["pin_mismatch"] += 1
    if c["pin_mismatch"]:
        failed.append("pins")
    events = parse_events(blobs.get(OOM_H) or "")
    entry = read(ENTRY)
    prov = "bad"
    rows = []
    if entry is None:
        failed.append("entry_absent")
    else:
        head = [l for l in entry.split("\n") if l.strip()][:12]
        has = lambda k: any(re.match(r"^[-* ]*%s\s*:" % k, l) for l in head)
        src_line = next((l for l in head if re.match(r"^[-* ]*source\s*:", l)), "")
        if has("source") and has("verified-at") and has("recheck") and ROW_ID in src_line:
            prov = "ok"
        else:
            failed.append("provenance")
        header, rows = parse_table(entry)
        if header is None or "fields" not in header or "emitted in" not in header:
            failed.append("table")
            rows = []
        else:
            fi, ei = header.index("fields"), header.index("emitted in")
            seen = set()
            for cells in rows:
                if len(cells) != len(header):
                    c["name_mismatch"] += 1
                    continue
                names = SPAN.findall(cells[0])
                if len(names) != 1:
                    c["name_mismatch"] += 1
                    continue
                name = names[0]
                if name not in events or name in seen:
                    c["name_mismatch"] += 1
                    continue
                seen.add(name)
                if set(SPAN.findall(cells[fi])) != events[name]:
                    c["field_mismatch"] += 1
                paths = [p for p in SPAN.findall(cells[ei]) if p in COPY_OF]
                if len(paths) != 1 or ("trace_%s(" % name) not in (blobs.get(COPY_OF[paths[0]]) or ""):
                    c["callsite_mismatch"] += 1
            c["name_mismatch"] += len(set(events) - seen)
            if not events:
                failed.append("no_events")
    for k in ("name_mismatch", "field_mismatch", "callsite_mismatch"):
        if c[k]:
            failed.append(k)
    srow = "bad"
    src = read("corpus/SOURCES.md")
    cells = sources_row(src or "", ROW_ID)
    if cells and len(cells) == 11:
        kind, tier, status, used = cells[2], cells[3], cells[7], cells[10]
        if (kind == "code" and tier == "A" and status == "mined"
                and "v7.2" in cells[1] and "include/trace/events/oom.h" in cells[1]
                and ENTRY in [u.strip() for u in re.split(r"[,;]", used)]):
            srow = "ok"
    if srow != "ok":
        failed.append("source_row")
    met = not failed
    line = ("C2=%s events=%d rows=%d name_mismatch=%d field_mismatch=%d callsite_mismatch=%d "
            "pin_mismatch=%d source_row=%s provenance=%s rev=%s"
            % ("met" if met else "unmet", len(events), len(rows), c["name_mismatch"],
               c["field_mismatch"], c["callsite_mismatch"], c["pin_mismatch"], srow, prov, rev))
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
    global ENTRY
    while "--repo" in args:
        i = args.index("--repo"); repo = args[i + 1]; del args[i:i + 2]
    while "--entry" in args:
        i = args.index("--entry"); ENTRY = args[i + 1]; del args[i:i + 2]
    if len(args) != 1 or args[0].startswith("-"):
        print("C2_SETUP usage: count-c2.py <rev> [--repo DIR] [--entry PATH] | --selftest", file=sys.stderr)
        return 2
    try:
        p = subprocess.run(["git", "-C", repo, "rev-parse", "--verify", args[0] + "^{commit}"],
                           stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=60)
    except (OSError, subprocess.SubprocessError):
        p = None
    if p is None or p.returncode != 0:
        print("C2_SETUP unresolvable revision %s" % args[0], file=sys.stderr)
        return 2
    rev = p.stdout.decode().strip()
    met, line = evaluate(git_reader(repo, rev), PINS, rev)
    print(line)
    return 0 if met else 1


# ---------------------------------------------------------------- selftest
FAKE_H = """TRACE_EVENT(alpha,
\tTP_PROTO(int x),
\tTP_STRUCT__entry(
\t\t__field(int, pid)
\t\t__string(comm, task->comm)
\t),
\tTP_printk("x")
);

TRACE_EVENT(beta,
\tTP_STRUCT__entry(
\t\t__field(unsigned long, total_vm)
\t\t__array(char, name, 16)
\t),
\tTP_printk("y")
);
"""
FAKE_C = "void f(void) { trace_alpha(1); trace_beta(2); }\n"


def fake_tree(entry_rows, source_row=True, header="| tracepoint | fields | emitted in |", trio=True, h=FAKE_H):
    files = {
        OOM_H: h,
        SRC_DIR + "mm_oom_kill.c": FAKE_C,
        SRC_DIR + "mm_page_alloc.c": FAKE_C,
        SRC_DIR + "fs_proc_base.c": FAKE_C,
    }
    pre = ("source: %s — Linux v7.2 include/trace/events/oom.h\nverified-at: 2026-10-25\nrecheck: on-release\n\n" % ROW_ID) if trio else ""
    files[ENTRY] = "# t\n\n" + pre + header + "\n|---|---|---|\n" + "".join(r + "\n" for r in entry_rows) + "\nprose\n"
    if source_row:
        files["corpus/SOURCES.md"] = ("| %s | Linux v7.2 include/trace/events/oom.h — https://x/v7.2/include/trace/events/oom.h | code | A | s | a | t | mined | 2026-10-25 | on-release | %s |\n"
                                      % (ROW_ID, ENTRY))
    else:
        files["corpus/SOURCES.md"] = ""
    pins = {p: hashlib.sha256(files[p].encode()).hexdigest() for p in PINS}
    return files, pins


def selftest():
    A = "| `alpha` | `pid`, `comm` | `mm/oom_kill.c` |"
    B = "| `beta` | `total_vm`, `name` | `mm/oom_kill.c` |"
    cases = []
    f, p = fake_tree([A, B]); cases.append(("honest", f, p, True, None))
    f, p = fake_tree([A]); cases.append(("missing_event_three_of_eight_class", f, p, False, "name_mismatch"))
    f, p = fake_tree([A, B, "| `gamma` | `pid` | `mm/oom_kill.c` |"]); cases.append(("invented_event", f, p, False, "name_mismatch"))
    f, p = fake_tree([A, "| `beta` | `total_vm` | `mm/oom_kill.c` |"]); cases.append(("missing_field", f, p, False, "field_mismatch"))
    f, p = fake_tree([A, "| `beta` | `total_vm`, `name` | `mm/page_alloc.c` |"])
    f[SRC_DIR + "mm_page_alloc.c"] = "nothing\n"; p = {k: hashlib.sha256(f[k].encode()).hexdigest() for k in PINS}
    cases.append(("wrong_callsite", f, p, False, "callsite_mismatch"))
    f, p = fake_tree([A, B]); f[OOM_H] = f[OOM_H] + "\n"; cases.append(("pin_tamper", f, p, False, "pins"))
    f, p = fake_tree([A, B], source_row=False); cases.append(("no_source_row", f, p, False, "source_row"))
    f, p = fake_tree([A, B], trio=False); cases.append(("no_provenance", f, p, False, "provenance"))
    f, p = fake_tree([A, B], header="| event | fields | emitted in |"); cases.append(("no_table", f, p, False, "table"))
    f, p = fake_tree([A, A, B]); cases.append(("duplicate_row", f, p, False, "name_mismatch"))
    f, p = fake_tree([A, B]); del f[ENTRY]; cases.append(("entry_absent_do_nothing", f, p, False, "entry_absent"))
    f, p = fake_tree([A, B]); f["corpus/SOURCES.md"] = f["corpus/SOURCES.md"].replace("| mined |", "| queued |")
    cases.append(("source_row_queued", f, p, False, "source_row"))
    fails = 0
    for name, files, pins, want, tag in cases:
        met, line = evaluate(lambda path, fs=files: fs.get(path), pins, "fixture")
        ok = met == want and (tag is None or tag in line)
        fails += 0 if ok else 1
        print("%s %s  %s" % ("PASS" if ok else "FAIL", name, line))
    import tempfile
    d = tempfile.mkdtemp()
    env = dict(os.environ, GIT_CEILING_DIRECTORIES=os.path.dirname(d))
    p = subprocess.run([sys.executable, os.path.abspath(__file__), "HEAD", "--repo", d],
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60, env=env)
    os.rmdir(d)
    ok = p.returncode == 2
    fails += 0 if ok else 1
    print("%s cli_not_a_repo_rc2  rc=%d" % ("PASS" if ok else "FAIL", p.returncode))
    print("C2_SELFTEST pass=%d fail=%d" % (len(cases) + 1 - fails, fails))
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
