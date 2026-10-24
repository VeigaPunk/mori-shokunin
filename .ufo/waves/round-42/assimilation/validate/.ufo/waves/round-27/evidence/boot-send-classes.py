#!/usr/bin/env python3
"""Round 27 C1 host capture: aggregates of earlyoom 1.9.0 send lines per retained boot.

Read-only. MESSAGE text stays in memory; the output carries counts, class labels, score and RSS ranges, and UTC
hours only. No pid, uid number, command line, or process name outside the class list is printed.
"""
import json
import os
import re
import statistics
import subprocess
from collections import Counter
from datetime import datetime, timezone

# earlyoom v1.9.0 kill.c:627 — "sending %s to process %d uid %d \"%s\": oom_score %d, oom_score_adj %d, VmRSS %lld MiB, cmdline ..."
SEND = re.compile(r'^sending (SIGTERM|SIGKILL) to process (\d+) uid (\d+) "([^"]*)": oom_score (-?\d+), oom_score_adj (-?\d+), VmRSS (\d+) MiB')
ME = os.getuid()


def klass(name):
    n = name.lower()
    if n.startswith("python"):
        return "python"
    if n in ("omp", "bun", "node"):
        return n
    return "other"


boots = json.loads(subprocess.run(["journalctl", "--list-boots", "-o", "json"], capture_output=True, text=True).stdout)
for b in boots:
    off = b.get("index")
    out = subprocess.run(["journalctl", "-q", "-u", "earlyoom.service", "-b", str(off), "-o", "json",
                          "--output-fields=MESSAGE,__REALTIME_TIMESTAMP"], capture_output=True, text=True).stdout
    sig, cls, uidc, hours, adjs = Counter(), Counter(), Counter(), Counter(), Counter()
    scores, rss, pids, unparsed_send, above = [], [], set(), 0, 0
    for line in out.splitlines():
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        msg = rec.get("MESSAGE")
        if not isinstance(msg, str):
            continue
        m = SEND.match(msg)
        if not m:
            if msg.startswith("sending SIG"):
                unparsed_send += 1
            continue
        s, pid, uid, name, sc, adj, r = m.groups()
        adjs[adj] += 1
        # the kernel's exported oom_score cannot exceed (1000 + adj + 1000) * 2 / 3 (fs/proc/base.c v7.2 :597);
        # a higher send-line score can only come from earlyoom's +300 --prefer adjustment (kill.c:24-25,410-414)
        if int(sc) > (2000 + int(adj)) * 2 // 3:
            above += 1
        sig[s] += 1
        cls[klass(name)] += 1
        uidc["operator" if int(uid) == ME else ("root" if uid == "0" else "other")] += 1
        scores.append(int(sc))
        rss.append(int(r))
        pids.add(pid)
        t = datetime.fromtimestamp(int(rec["__REALTIME_TIMESTAMP"]) / 1e6, tz=timezone.utc)
        hours[t.strftime("%Y-%m-%dT%HZ")] += 1
    n = sum(sig.values())
    print("boot=%s sends=%d %s unparsed_send_lines=%d" % (off, n, dict(sig), unparsed_send))
    if n:
        print("  victim_class=%s uid_class=%s distinct_victim_pids=%d" % (dict(cls), dict(uidc), len(pids)))
        print("  oom_score min=%d median=%g max=%d; VmRSS_MiB min=%d median=%g max=%d" % (
            min(scores), statistics.median(scores), max(scores), min(rss), statistics.median(rss), max(rss)))
        print("  victim_oom_score_adj=%s above_kernel_ceiling_for_adj=%d" % (dict(adjs), above))
        print("  hours_utc=%s" % dict(sorted(hours.items())))
