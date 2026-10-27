#!/usr/bin/env python3
"""Round 54 C2 registry applier (L1 MoriR54): rows S521-S524 and the used-by additions to S502 and S507 for
corpus/knowledge/memory-failure-kills-r54.md. Used by controls.py (witness, in a throwaway clone) and by the L1
for the data commit. The entry itself is written by hand; this file writes registry rows only.

Usage: c2data.py ROOT
"""
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("c2", os.path.join(HERE, "..", "count-c2.py"))
c2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c2)

OPENED = "2026-10-27"
TAG = "tag v7.3 (091b06388b11, commit c03c1a14507d)"
CG = c2.CGIT
NEW_ROWS = [
    ("S521", CG + "mm/memory-failure.c?h=v7.3", "Linux mm/memory-failure.c at tag v7.3", "code",
     "the hardware memory-failure handler at v7.3: the kill lines it prints (SIGBUS, forced SIGKILL), the "
     "recovery-action line and its results, the four sysctls, the per-node counters it bumps; not MCE decoding "
     "(arch code) and not any host's values",
     "pr_fmt 37; sysctls 72-78, 134-171; kill_proc 286-311; kill_procs 462-490; action_name 871-876; "
     "action_result 1281-1298",
     "names the kill-event class a census of OOM lines does not see, with the exact kernel lines and counters"),
    ("S522", CG + "Documentation/mm/hwpoison.rst?h=v7.3", "Linux Documentation/mm/hwpoison.rst at tag v7.3", "docs",
     "what hwpoison is, the recovery modes (panic, early kill, late kill) and the user controls at v7.3",
     "Failure recovery modes 54-73; User control 74-105",
     "the early/late kill semantics behind the SIGBUS line"),
    ("S523", CG + "Documentation/ABI/stable/sysfs-devices-node?h=v7.3",
     "Linux Documentation/ABI/stable/sysfs-devices-node at tag v7.3", "docs",
     "the per-node memory_failure/{total,ignored,failed,delayed,recovered} counters at v7.3 (stable ABI)",
     "memory_failure entries 192-229",
     "the counters a census can read for memory-failure events without the journal"),
    ("S524", CG + "include/trace/events/memory-failure.h?h=v7.3",
     "Linux include/trace/events/memory-failure.h at tag v7.3", "code",
     "the ras:memory_failure_event tracepoint (system, fields, printed line) at v7.3",
     "TRACE_SYSTEM ras line 7; TRACE_EVENT(memory_failure_event) 74-98 with its TP_printk",
     "the event-time hook for the recovery action, next to the round-47 OOM tracepoints"),
]
REUSED = ["S502", "S507"]


def apply(root):
    entry = c2.ENTRY
    src_path = os.path.join(root, "corpus/SOURCES.md")
    src = open(src_path, encoding="utf-8").read().split("\n")
    for sid in REUSED:
        for i, line in enumerate(src):
            if re.match(r"^ {0,3}\|\s*%s\s*\|" % sid, line):
                cells = line.rstrip().rstrip("|").rstrip()
                if entry not in cells:
                    src[i] = cells + ", " + entry + " |"
    rows = []
    for sid, url, title, kind, scope, anchor, teaches in NEW_ROWS:
        copy, digest, _k = c2.COPIES[url]
        rows.append("| %s | %s — %s | %s | A | %s | %s; %s; sha256 %s; copy %s | %s | mined | %s | on-release | %s |"
                    % (sid, title, url, kind, scope, TAG, anchor, digest[:12], copy, teaches, OPENED, entry))
    last = max(i for i, l in enumerate(src) if re.match(r"^ {0,3}\|\s*S[0-9]{3,}\s*\|", l))
    src[last + 1:last + 1] = rows
    open(src_path, "w", encoding="utf-8").write("\n".join(src))
    return rows


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: c2data.py ROOT", file=sys.stderr)
        sys.exit(2)
    print("c2data rows=%d" % len(apply(sys.argv[1])))
