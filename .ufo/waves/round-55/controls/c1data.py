#!/usr/bin/env python3
"""Round 55 C1 data builder (L1 MoriR55): locates every scoped v7.2 pointer in its v7.3 copy and renders the
ledger table. Used once for the data commit and by the controls (witness, lazy relabels). Location rule, applied
per comma piece: the v7.2 block at the same numbers in v7.3 -> same; else the v7.2 block found as consecutive lines
in v7.3 (nearest to the difflib-mapped position when it occurs more than once) -> moved; else the difflib-mapped
range -> changed. Reads only the committed copies named by the frozen counter's COPIES.
"""
import difflib
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
WAVE = os.path.dirname(HERE)
LANE = os.path.dirname(os.path.dirname(os.path.dirname(WAVE)))

V73_SID = {
    "fs/proc/base.c": "S526", "mm/page_alloc.c": "S527", "include/trace/events/oom.h": "S528",
    "Documentation/accounting/psi.rst": "S529", "kernel/sched/psi.c": "S530",
    "include/linux/psi_types.h": "S531", "Documentation/admin-guide/kernel-parameters.txt": "S532",
    "Documentation/admin-guide/cgroup-v2.rst": "S533", "kernel/fork.c": "S534",
    "mm/oom_kill.c": "S516", "Documentation/filesystems/proc.rst": "S502",
}


def counter():
    spec = importlib.util.spec_from_file_location("count_c1", os.path.join(WAVE, "count-c1.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _lines(read, path):
    t = (read(path) or "").split("\n")
    return t[:-1] if t and t[-1] == "" else t


def locate_all(read, read_enter, c1=None):
    """-> list of (hash, entry, path, spec72, spec73, status)."""
    c1 = c1 or counter()
    out = []
    maps = {}
    for h, entry, path, spec in c1.scope(read_enter):
        c72, _, c73, _ = c1.COPIES[path]
        v72, v73 = _lines(read, c72), _lines(read, c73)
        if path not in maps:
            a = [c1.nl(x) for x in v72]
            b = [c1.nl(x) for x in v73]
            mp = {}
            for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
                for k in range(i1, i2):
                    mp[k + 1] = (j1 + (k - i1) + 1) if tag == "equal" else ("chg", j1 + 1, max(j1 + 1, j2))
            maps[path] = (mp, b)
        mp, n73 = maps[path]
        pcs, sts = [], []
        broken = False
        for a, b in c1.pieces(spec):
            blk = c1.block(v72, a, b)
            if blk is None:
                broken = True
                break
            if c1.block(v73, a, b) == blk:
                pcs.append((a, b)); sts.append("same"); continue
            n = len(blk)
            occ = [i + 1 for i in range(len(n73) - n + 1) if n73[i:i + n] == blk]
            if occ:
                tgt = mp.get(a) if isinstance(mp.get(a), int) else a
                s = min(occ, key=lambda x: abs(x - tgt))
                pcs.append((s, s + n - 1)); sts.append("moved"); continue
            m1 = lambda x, end=False: (mp[x] if isinstance(mp.get(x), int)
                                       else (mp[x][2] if end else mp[x][1]) if mp.get(x) else x)
            s, e = m1(a), m1(b, True)
            pcs.append((s, max(s, e))); sts.append("changed")
        if broken:
            out.append((h, entry, path, spec, "-", "broken"))
            continue
        status = "changed" if "changed" in sts else "moved" if "moved" in sts else "same"
        spec73 = ",".join("%d-%d" % (x, y) if x != y else "%d" % x for x, y in pcs)
        out.append((h, entry, path, spec, spec73, status))
    return out


def ledger_rows(located, disposition=None, spec_override=None, status_override=None):
    rows = ["| hash | entry | pointer | v7.3 source | v7.3 lines | status | disposition |",
            "|---|---|---|---|---|---|---|"]
    for h, entry, path, spec, spec73, status in located:
        d = disposition(h) if callable(disposition) else (disposition or "holds")
        s73 = spec_override(h, spec, spec73) if spec_override else spec73
        st = status_override(h, status) if status_override else status
        rows.append("| `%s` | %s | `%s:%s` | %s | %s | %s | %s |" % (h, entry, path, spec, V73_SID[path], s73, st, d))
    return rows


def ledger(read, read_enter, dispositions=None, c1=None):
    c1 = c1 or counter()
    loc = locate_all(read, read_enter, c1)
    return ["# Linux v7.2 citation pointers rechecked at v7.3 (round 55)", "",
            "source: S526 S527 S528 S529 S530 S531 S532 S533 S534 S516 S502",
            "verified-at: 2026-10-27",
            "recheck: on-release — re-open each pinned v7.2/v7.3 source pair and re-derive the frozen pointer scope; lines and status are mechanically checked by count-c1.py.", "",
            "## Pointer ledger", ""] + ledger_rows(loc, disposition=(lambda h: (dispositions or {}).get(h, "holds"))) + [""]
