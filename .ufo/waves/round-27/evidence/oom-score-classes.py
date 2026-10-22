#!/usr/bin/env python3
"""Round 27 C1 host capture: per-class aggregates of /proc/<pid>/oom_score and oom_score_adj.

Read-only. Prints no pid, no command line, no uid and no process name outside the fixed class list.
"""
import os
import statistics
from collections import Counter, defaultdict

FLEET = ("omp", "bun", "node", "python", "earlyoom", "systemd")


def klass(comm, has_mm):
    if not has_mm:
        return "kernel-thread"
    c = comm.lower()
    if c.startswith("python"):
        return "python"
    if c in ("bun", "node", "omp", "earlyoom") or c.startswith("systemd"):
        return "systemd" if c.startswith("systemd") else c
    return "other"


def read(path):
    with open(path) as f:
        return f.read().strip()


rows = []
for d in os.listdir("/proc"):
    if not d.isdigit():
        continue
    try:
        comm = read("/proc/%s/comm" % d)
        score = int(read("/proc/%s/oom_score" % d))
        adj = int(read("/proc/%s/oom_score_adj" % d))
        # kernel threads have an empty statm size; VmSize absent from status
        has_mm = "VmSize:" in read("/proc/%s/status" % d)
    except (OSError, ValueError):
        continue
    rows.append((klass(comm, has_mm), score, adj, comm))

by = defaultdict(list)
adjs = defaultdict(Counter)
for k, s, a, _ in rows:
    by[k].append(s)
    adjs[k][a] += 1
print("processes_read=%d" % len(rows))
for k in sorted(by):
    v = by[k]
    print("class=%s count=%d oom_score_min=%d median=%g max=%d oom_score_adj=%s" % (
        k, len(v), min(v), statistics.median(v), max(v),
        ",".join("%d:%d" % (a, n) for a, n in sorted(adjs[k].items()))))
top = sorted(rows, key=lambda r: -r[1])[:10]
print("top10_by_oom_score_classes=" + ",".join("%s(%d,adj=%d)" % (k, s, a) for k, s, a, _ in top))
# per-user service manager and earlyoom: identified by comm and parent, values only
uid = os.getuid()
for k, s, a, comm in rows:
    pass
mgr = [r for r in rows if r[3] == "systemd" and r[2] != 0]
print("systemd_processes_with_nonzero_adj=%s" % ",".join("adj=%d" % r[2] for r in mgr))
eo = [r for r in rows if r[3] == "earlyoom"]
print("earlyoom_processes=%s" % ",".join("score=%d,adj=%d" % (r[1], r[2]) for r in eo))
print("self_oom_score_adj=%s" % read("/proc/self/oom_score_adj"))
