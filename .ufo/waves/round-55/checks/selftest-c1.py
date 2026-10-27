#!/usr/bin/env python3
"""Selftest for count-c1.py (round 55). Hermetic over git objects: scope is read from the entering tip ENTER in the
lane's object store; the v7.2/v7.3 copies are read from the lane working tree (their pins are checked); every other
file (ledger, SOURCES rows, voter reports, results file) is synthetic. Run: count-c1.py --selftest.
"""
import json
import os
import subprocess


def run(c1):
    here = os.path.dirname(os.path.abspath(__file__))
    lane = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(here))))
    read_enter = c1.git_reader(lane, c1.ENTER)
    import importlib.util
    spec = importlib.util.spec_from_file_location("c1data", os.path.join(os.path.dirname(here), "controls",
                                                                         "c1data.py"))
    cd = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cd)
    base = {}
    for path, (c72, _, c73, _) in c1.COPIES.items():
        for c in (c72, c73):
            with open(os.path.join(lane, c), "rb") as f:
                base[c] = f.read().decode("utf-8", "surrogateescape")
    rd = lambda p: base.get(p)
    located = cd.locate_all(rd, read_enter, c1)
    sc = c1.scope(read_enter)
    checks = []

    def check(name, cond):
        checks.append((name, bool(cond)))

    sids = sorted(set(cd.V73_SID.values()))
    by_sid = {}
    for path, sid in cd.V73_SID.items():
        by_sid.setdefault(sid, []).append(path)

    def srcs(status="mined", opened="2026-10-27", used=c1.LEDGER, drop=None, url_bad=None):
        rows = ["| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |",
                "|---|---|---|---|---|---|---|---|---|---|---|"]
        for sid in sids:
            path = by_sid[sid][0]
            url = c1.CGIT + path + ("?h=v7.2" if sid == url_bad else "?h=v7.3")
            st = "queued" if sid == drop else status
            rows.append("| %s | t — %s | code | A | s | a | t | %s | %s | on-release | %s |" % (sid, url, st, opened, used))
        return "\n".join(rows) + "\n"

    def ledger(rows, head=True, src_ids=None):
        lines = []
        if head:
            lines += ["source: " + " ".join(src_ids or sids), "verified-at: 2026-10-27", "recheck: on-release", ""]
        return "\n".join(lines + ["# Ledger", ""] + rows + [""])

    def votes_for(hashes, word="holds", names=("Mo55Rc01", "Mo55Rc05"), out_names=None, out_word=None):
        fl = {}
        for n in names:
            fl[c1.VOTE_DIR + n + ".md"] = "\n".join("RECHECK %s %s" % (h, word) for h in hashes) + "\n"
        out_names = names if out_names is None else out_names
        res = {"results": [{"name": n, "output": "\n".join("RECHECK %s %s" % (h, out_word or word) for h in hashes)
                            if n in out_names else "no votes here"} for n in names]}
        fl[c1.RESULTS] = json.dumps(res)
        return fl

    hashes = [x[0] for x in located]

    def build(rows=None, src=None, votes=None, extra=None, ledger_text=None):
        fl = dict(base)
        fl[c1.LEDGER] = ledger_text if ledger_text is not None else ledger(rows or cd.ledger_rows(located))
        fl["corpus/SOURCES.md"] = src if src is not None else srcs()
        fl.update(votes if votes is not None else votes_for(hashes))
        fl.update(extra or {})
        return fl

    def score(fl, copies=None):
        ls = lambda d: [p for p in fl if p.startswith(d) and "/" not in p[len(d):]]
        return c1.evaluate(lambda p: fl.get(p), "R", read_enter, ls=ls, copies=copies)

    n = len(sc)
    met, line = score(build())
    check("witness met (scope %d)" % n, met and ("scope=%d rows=%d matched=%d" % (n, n, n)) in line)
    check("scope non-empty and > 60", n > 60)
    check("scope covers three entries", len(set(x[1] for x in sc)) == 3)
    check("scope has header-line token from oom-tracepoints",
          any(x[2] == "include/trace/events/oom.h" for x in sc))
    check("scope has continuation tokens (proc.rst / cgroup-v2 continuation)",
          any(x[2] == "Documentation/admin-guide/cgroup-v2.rst" and x[3] == "1911-1915" for x in sc))
    check("scope hashes unique", len(set(x[0] for x in sc)) == n)
    stc = {}
    for x in located:
        stc[x[5]] = stc.get(x[5], 0) + 1
    check("statuses discriminate (moved and changed present)", stc.get("moved", 0) > 0 and stc.get("changed", 0) > 0)
    met, line = score({k: v for k, v in build().items() if k != c1.LEDGER})
    check("no ledger unmet ledger_absent", not met and "ledger_absent" in line)
    # lazy relabel: every row same, v7.2 numbers kept
    lazy = cd.ledger_rows(located, spec_override=lambda h, s72, s73: s72, status_override=lambda h, s: "same")
    met, line = score(build(rows=lazy))
    check("lazy all-same relabel fails status and line", not met and "status" in line and "line" in line)
    # honest numbers but status all 'same'
    lab = cd.ledger_rows(located, status_override=lambda h, s: "same")
    met, line = score(build(rows=lab))
    check("status mislabel fails status only", not met and "failed=status" in line)
    # moved row pointed at a wrong place (off by one)
    mv = next(x for x in located if x[5] == "moved")

    def off(h, s72, s73):
        if h != mv[0]:
            return s73
        a = int(s73.split(",")[0].split("-")[0])
        return str(a + 1)
    met, line = score(build(rows=cd.ledger_rows(located, spec_override=off)))
    check("off-by-one v7.3 line fails line", not met and "line" in line)
    # changed row labelled with v7.2 numbers while block occurs nowhere -> still 'changed' status needs same count
    ch = next(x for x in located if x[5] == "changed")
    met, line = score(build(rows=cd.ledger_rows(located, spec_override=lambda h, a, b: a if h == ch[0] else b)))
    check("changed row at v7.2 numbers still derives changed (block absent in v7.3)", met)
    # piece count mismatch
    multi = next((x for x in located if "," in x[3]), None)
    if multi:
        met, line = score(build(rows=cd.ledger_rows(located, spec_override=lambda h, a, b: b.split(",")[0]
                                                     if h == multi[0] else b)))
        check("piece-count mismatch fails line", not met and "line" in line)
    # missing row, extra row, duplicate row
    rows = cd.ledger_rows(located)
    met, line = score(build(rows=rows[:-1]))
    check("one missing row fails matched", not met and "matched" in line)
    met, line = score(build(rows=rows + ["| `000000000000` | x | `y:1` | S526 | 1 | same | holds |"]))
    check("extra row fails rows", not met and "rows" in line)
    met, line = score(build(rows=rows + [rows[2]]))
    check("duplicate row fails rows", not met and "rows" in line)
    # wrong entry cell
    bad = [r.replace("| corpus/knowledge/", "| corpus/knowledgeX/", 1) if i == 2 else r for i, r in enumerate(rows)]
    met, line = score(build(rows=bad))
    check("wrong entry cell fails matched", not met and "matched" in line)
    # sources
    met, line = score(build(src=srcs(status="queued")))
    check("queued rows fail source_rows", not met and "source_rows" in line)
    met, line = score(build(src=srcs(opened="2026-10-20")))
    check("old opened date fails source_rows", not met and "source_rows" in line)
    met, line = score(build(src=srcs(used="corpus/knowledge/other.md")))
    check("used-by missing ledger fails source_rows", not met and "source_rows" in line)
    met, line = score(build(src=srcs(url_bad="S530")))
    check("v7.2 URL in a v7.3 row fails source_rows", not met and "source_rows" in line)
    met, line = score(build(src=srcs(opened="2026-10-26")))
    check("reused row opened 2026-10-26 accepted", met)
    # provenance
    met, line = score(build(ledger_text=ledger(cd.ledger_rows(located), head=False)))
    check("no provenance header fails provenance", not met and "provenance" in line)
    met, line = score(build(ledger_text=ledger(cd.ledger_rows(located), src_ids=sids[:3])))
    check("source line missing cited ids fails provenance", not met and "provenance" in line)
    # pins
    fl = build()
    first = next(iter(c1.COPIES.values()))
    fl[first[2]] = fl[first[2]] + "\n"
    met, line = score(fl)
    check("altered v7.3 copy fails pins", not met and "pins=bad" in line)
    v72copies = dict(build())
    for path, (c72, _, c73, _) in c1.COPIES.items():
        v72copies[c73] = base[c72]
    met, line = score(v72copies)
    check("v7.2 bytes presented as v7.3 fail pins", not met and "pins=bad" in line)
    # votes
    met, line = score(build(votes={}))
    check("no votes fails votes", not met and "votes" in line and "voted=0" in line)
    met, line = score(build(votes=votes_for(hashes, names=("Mo55Rc01",))))
    check("one voter fails votes", not met and "votes" in line)
    met, line = score(build(votes=votes_for(hashes, names=("Mo55Rc01", "Mo55Rc05"), out_names=("Mo55Rc01",))))
    check("voter whose output lacks the line does not count", not met and "votes" in line)
    fl = build(votes=votes_for(hashes))
    fl[c1.RESULTS] = json.dumps({"results": []})
    met, line = score(fl)
    check("voters absent from results do not count", not met and "voted=0" in line)
    met, line = score(build(votes=votes_for(hashes, names=("Mo99Rc01", "Mo99Rc02"))))
    check("non-frozen voter names do not count", not met and "voted=0" in line)
    v = votes_for(hashes)
    v[c1.VOTE_DIR + "Mo55Rc09.md"] = "RECHECK %s stale\n" % hashes[0]
    res = json.loads(v[c1.RESULTS])
    res["results"].append({"name": "Mo55Rc09", "output": "RECHECK %s stale" % hashes[0]})
    v[c1.RESULTS] = json.dumps(res)
    met, line = score(build(votes=v))
    check("a stale dissent fails votes", not met and "dissent=1" in line)
    v = votes_for(hashes)
    v[c1.VOTE_DIR + "Mo55Rc09.md"] = "RECHECK %s stale\n" % hashes[0]
    saved_voters = c1.VOTERS
    c1.VOTERS = saved_voters + ["Mo55Rc09"]
    met, line = score(build(votes=v))
    c1.VOTERS = saved_voters
    check("dissent counts from the report alone (unbound)", not met and "dissent=1" in line)
    v = votes_for(hashes)
    for nme in ("Mo55Rc01", "Mo55Rc05"):
        v[c1.VOTE_DIR + nme + ".md"] = "```\n" + v[c1.VOTE_DIR + nme + ".md"] + "```\n"
    met, line = score(build(votes=v))
    check("fenced votes ignored", not met and "voted=0" in line)
    v = votes_for(hashes)
    v[c1.VOTE_DIR + "Mo55Rc01.md"] += "RECHECK %s stale\nRECHECK %s holds\n" % (hashes[0], hashes[0])
    met, line = score(build(votes=v))
    check("last line wins (stale then holds)", met)
    # disposition stale must be carried by voters
    st = cd.ledger_rows(located, disposition=lambda h: "stale" if h == hashes[0] else "holds")
    met, line = score(build(rows=st))
    check("stale disposition without stale votes fails votes", not met and "votes" in line)
    # derive unit checks
    v72 = ["a", "b", "c", "d"]
    check("derive same", c1.derive(v72, v72, [(2, 3)], [(2, 3)]) == ("same", True))
    check("derive moved", c1.derive(v72, ["x"] + v72, [(2, 3)], [(3, 4)]) == ("moved", True))
    check("derive moved wrong place", c1.derive(v72, ["x"] + v72, [(2, 3)], [(2, 3)]) == (None, False))
    check("derive changed", c1.derive(v72, ["a", "B", "c", "d"], [(2, 2)], [(2, 2)]) == ("changed", True))
    check("derive broken", c1.derive(v72, v72, [(5, 6)], [(1, 1)]) == ("broken", True))
    check("derive whitespace-insensitive", c1.derive(["a  b"], ["\ta b "], [(1, 1)], [(1, 1)]) == ("same", True))
    check("pieces rejects reversed", c1.pieces("5-3") is None)
    check("pieces en dash normalised", c1.pieces(c1.norm_spec("3–5")) == [(3, 5)])
    failn = sum(1 for _, ok in checks if not ok)
    for name, ok in checks:
        if not ok:
            print("FAIL", name)
    print("C1_SELFTEST pass=%d fail=%d" % (len(checks) - failn, failn))
    return 0 if failn == 0 else 1
