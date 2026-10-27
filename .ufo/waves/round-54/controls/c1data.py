#!/usr/bin/env python3
"""Round 54 C1 data applier (L1 MoriR54). Writes, into the tree at ROOT, the mechanical part of the C1 landing:
the ledger corpus/knowledge/kernel-v7.3-recheck-r54.md (one row per hash of the frozen scope D, status and line
derived from the committed v7.3 copies, disposition `holds` pending the RECHECK voters), registry rows S515-S520
and the used-by additions to S508 and S514. Used twice: by controls.py for the witness control (before data, in a
throwaway clone) and by the L1 for the data commit, where the ledger prose is then written by hand.

Usage: c1data.py ROOT   (ROOT is a lane checkout; the scope is read from ROOT's git at the entering tip)
"""
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("c1", os.path.join(HERE, "..", "count-c1.py"))
c1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1)

OPENED = "2026-10-27"
TAG = "tag v7.3 (091b06388b11, commit c03c1a14507d)"
NEW_ROWS = {
    "mm/memcontrol.c": ("S515", "Linux mm/memcontrol.c at tag v7.3", "code",
                        "the memcg OOM report lines (usage/limit/failcnt, the Memory cgroup stats block, the "
                        "oom_memcg/task_memcg path fields) and the memory.stat formatter at v7.3",
                        "re-checks the round-50 memcg OOM report claims against the current release"),
    "mm/oom_kill.c": ("S516", "Linux mm/oom_kill.c at tag v7.3", "code",
                      "the OOM victim record, dump_header and the memcg-versus-global report split at v7.3",
                      "re-checks the round-50 victim-record and report-split claims against the current release"),
    "lib/percpu_counter.c": ("S517", "Linux lib/percpu_counter.c at tag v7.3", "code",
                             "percpu_counter_add_batch, the fold of a per-CPU delta into the shared count, at v7.3",
                             "re-checks the round-53 band entry's fold rule against the current release"),
    "include/linux/percpu_counter.h": ("S518", "Linux include/linux/percpu_counter.h at tag v7.3", "code",
                                       "percpu_counter_read_positive at v7.3",
                                       "re-checks the round-53 band entry's clamped read against the current release"),
    "include/uapi/asm-generic/errno.h": ("S519", "Linux include/uapi/asm-generic/errno.h at tag v7.3", "code",
                                         "the generic EDQUOT value at v7.3",
                                         "re-checks the round-48 EDQUOT claim; the file is byte-identical to v7.2 "
                                         "(same sha256 as S481's copy)"),
    "docs:admin-guide/cgroup-v2.html": ("S520", "Control Group v2 (v7.3) — rendered kernel documentation", "docs",
                                        "cgroup v2 memory interface at kernel 7.3: memory.stat keys and units, "
                                        "memory.events oom_kill; not the kernel print formats (S515, S516)",
                                        "re-checks the round-50 memory.stat and memory.events claims against the "
                                        "release-pinned rendered page (the flip the round-53 closure named)"),
}
REUSED = {"mm/util.c": "S508", "mm/mm_init.c": "S514"}


def scope_lines(root):
    rd = c1.git_reader(root, c1.ENTERING)
    ls = c1.git_lister(root, c1.ENTERING)
    d = c1.scope(rd, ls)
    out = []
    for h, (entry, key, q) in sorted(d.items(), key=lambda kv: (kv[1][0], kv[1][1], kv[0])):
        copy, digest, url, kind = c1.V73[key]
        raw = open(os.path.join(root, copy), encoding="utf-8", errors="surrogateescape").read()
        text, offs = c1.norm_map(raw, kind)
        status = "held" if q in text else "absent"
        lines = sorted(c1.lines_of(raw, text, offs, q))
        out.append((h, entry, key, q, status, lines))
    return out


def sid_of(key):
    return NEW_ROWS[key][0] if key in NEW_ROWS else REUSED[key]


def ledger_table(rows):
    t = ["| h | entry | status | source | line | quote | disposition |", "|---|---|---|---|---|---|---|"]
    for h, entry, key, q, status, lines in rows:
        t.append("| %s | `%s` | %s | %s | %s | `%s` | holds |"
                 % (h, entry, status, sid_of(key), lines[0] if lines else "-", q.replace("|", "\\|")))
    return t


def registry_rows(root, rows):
    ledger = c1.LEDGER
    by_key = {}
    for h, entry, key, q, status, lines in rows:
        by_key.setdefault(key, []).append(lines[0] if lines else 0)
    out = []
    for key, (sid, title, kind, scope, teaches) in NEW_ROWS.items():
        copy, digest, url, _k = c1.V73[key]
        anchor = "%s; quote lines %s; sha256 %s; copy %s" % (
            TAG if not key.startswith("docs:") else "rendered page footer 7.3.0",
            ", ".join(str(x) for x in sorted(by_key.get(key, []))), digest[:12], copy)
        out.append("| %s | %s — %s | %s | A | %s | %s | %s | mined | %s | on-release | %s |"
                   % (sid, title, url, kind, scope, anchor, teaches, OPENED, ledger))
    return out


def apply(root):
    rows = scope_lines(root)
    src_path = os.path.join(root, "corpus/SOURCES.md")
    src = open(src_path, encoding="utf-8").read().split("\n")
    # used-by additions to the reused rows
    for key, sid in REUSED.items():
        for i, line in enumerate(src):
            if re.match(r"^ {0,3}\|\s*%s\s*\|" % sid, line):
                cells = line.rstrip().rstrip("|").rstrip()
                if c1.LEDGER not in cells:
                    src[i] = cells + ", " + c1.LEDGER + " |"
    # append new rows after the last registry row
    last = max(i for i, l in enumerate(src) if re.match(r"^ {0,3}\|\s*S[0-9]{3,}\s*\|", l))
    src[last + 1:last + 1] = registry_rows(root, rows)
    open(src_path, "w", encoding="utf-8").write("\n".join(src))
    ids = sorted(set(sid_of(k) for _h, _e, k, _q, _s, _l in rows))
    led = ["# Linux v7.3 recheck of the remaining v7.2-pinned claim rows (round 54)", "",
           "source: " + ", ".join(ids),
           "verified-at: 2026-10-27",
           "recheck: on-release — `python3 .ufo/waves/round-54/count-c1.py <rev>`", "",
           "## Ledger", ""] + ledger_table(rows) + [""]
    path = os.path.join(root, c1.LEDGER)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write("\n".join(led))
    return rows


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: c1data.py ROOT", file=sys.stderr)
        sys.exit(2)
    rows = apply(sys.argv[1])
    print("c1data rows=%d held=%d" % (len(rows), sum(1 for r in rows if r[4] == "held")))
