#!/usr/bin/env python3
"""mori round-61 C2 counter — PSI v7.3 recheck ledger over committed bytes.

Enumerates every <pinned-file>:<line> pointer in
corpus/knowledge/system-pressure-r24.md (the six files pinned at tag v7.3
under corpus/evidence/sources-r61/), then requires the recheck ledger
corpus/knowledge/psi-v73-recheck-r61.md to carry exactly one row per pointer
whose quote is a byte substring of the pinned v7.3 copy at the stated
location (same: the enumerated range; moved/changed: the row's own location),
quotes <=25 words with >=8 distinct bytes and pairwise distinct, >=4 copies
cited, and every cited copy bound to a mined SOURCES.md row whose used-by
names the ledger entry.

Read-only over the measured repo (git show). Honors TMPDIR; --scratch must be
a writable directory.
"""
import argparse
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

SOURCE_ENTRY = "corpus/knowledge/system-pressure-r24.md"
LEDGER = "corpus/knowledge/psi-v73-recheck-r61.md"
COPY_DIR = "corpus/evidence/sources-r61"
FILES = ["psi.rst", "psi.c", "psi_types.h", "cgroup-v2.rst", "Kconfig",
         "kernel-parameters.txt"]
PINS = {
    "psi.rst": "11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692",
    "psi.c": "c4edc1e7c18ca76e6e29668093fa0b26d4251cb088f2d5feab24681f285ec63f",
    "psi_types.h": "483269b27c82b438450632555aba2ba8a9c47b608243f78a029c4300b3618ccc",
    "cgroup-v2.rst": "2750c11a6324e18f4d3a9bb63032b55f3268bd7077b80897af2f15a712611b68",
    "Kconfig": "d37de2a11baf81cbe6fb3c9ae271e5808a2c6be17f8980fe0375f6e67e677e0d",
    "kernel-parameters.txt": "b5a13c038a27e688380bbcaa8cdbcad24543ad6b64de0c3d5709bc32c94cb39a",
}
FLOOR_DEFAULT = 40
NAMES = re.compile(
    r"(" + "|".join(re.escape(f) for f in FILES) + r"):(\d+)(?:-(\d+))?")
ROW = re.compile(
    r"^\|\s*([a-zA-Z0-9_.\-]+:\d+(?:-\d+)?)\s*\|\s*(same|moved|changed)\s*\|"
    r"\s*([a-zA-Z0-9_.\-]+:\d+(?:-\d+)?|-)\s*\|\s*`([^`]*)`\s*\|")


def sh(repo, *args, binary=False):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout if binary else r.stdout.decode("utf-8", "replace")


def cat(repo, rev, path):
    return sh(repo, "show", f"{rev}:{path}", binary=True)


def enumerate_pointers(text):
    """Ordered, deduped normalized pointer keys."""
    seen, out = set(), []
    for m in NAMES.finditer(text):
        key = f"{m.group(1)}:{m.group(2)}" + (f"-{m.group(3)}" if m.group(3) else "")
        if key not in seen:
            seen.add(key)
            out.append(key)
    return out


def span_of(anchor_or_loc):
    m = re.fullmatch(r"([a-zA-Z0-9_.\-]+):(\d+)(?:-(\d+))?", anchor_or_loc)
    if not m:
        return None
    start = int(m.group(2))
    end = int(m.group(3)) if m.group(3) else start
    return m.group(1), start, end


def distinct_bytes(q):
    return len(set(q.encode("utf-8", "replace")))


def wordcount(q):
    return len(q.split())


def provenance_ok(entry_text):
    head = entry_text[:2000]
    return all(re.search(rf"^{band}:", head, re.M)
               for band in ("source", "verified-at", "recheck"))


def measure(repo, rev, floor):
    res = {"pointers": 0, "rows": 0, "same": 0, "moved": 0, "changed": 0,
           "quotes_ok": 0, "spans_ok": 0, "sources": 0, "failed": []}
    src = cat(repo, rev, SOURCE_ENTRY)
    if src is None:
        res["failed"].append("source_entry_absent")
        return res, False
    pointers = enumerate_pointers(src.decode("utf-8", "replace"))
    res["pointers"] = len(pointers)
    pset = set(pointers)
    led = cat(repo, rev, LEDGER)
    if led is None:
        res["failed"].append("entry_absent")
        return res, False
    led_text = led.decode("utf-8", "replace")
    if not provenance_ok(led_text):
        res["failed"].append("provenance")
    copies = {}
    for f in FILES:
        b = cat(repo, rev, f"{COPY_DIR}/{f}")
        if b is None:
            res["failed"].append(f"copy_absent:{f}")
            continue
        if hashlib.sha256(b).hexdigest() != PINS[f]:
            res["failed"].append(f"copy_pin:{f}")
            continue
        copies[f] = b.decode("utf-8", "replace")
    rows, seen_q, anchors = [], set(), []
    for line in led_text.splitlines():
        m = ROW.match(line.strip())
        if m:
            rows.append(m.groups())
    res["rows"] = len(rows)
    anchor_list = [r[0] for r in rows]
    if len(anchor_list) != len(set(anchor_list)):
        res["failed"].append("dup_anchor")
    if set(anchor_list) != pset:
        miss = sorted(pset - set(anchor_list))[:5]
        orph = sorted(set(anchor_list) - pset)[:5]
        if miss:
            res["failed"].append("rows_missing:%s" % ",".join(miss))
        if orph:
            res["failed"].append("rows_orphan:%s" % ",".join(orph))
    cited = set()
    for anchor, status, loc, quote in rows:
        q = quote.strip()
        if not (5 <= wordcount(q) <= 25):
            res["failed"].append(f"quote_words:{anchor}")
            continue
        if distinct_bytes(q) < 8:
            res["failed"].append(f"span_small:{anchor}")
            continue
        if q in seen_q:
            res["failed"].append(f"quote_dup:{anchor}")
            continue
        seen_q.add(q)
        res["spans_ok"] += 1
        fname, start, end = (span_of(anchor) if status == "same"
                             else span_of(loc))
        if fname is None or fname not in copies:
            res["failed"].append(f"loc_bad:{anchor}")
            continue
        cited.add(fname)
        lines = copies[fname].splitlines()
        lo, hi = start, max(end, start)
        if hi > len(lines):
            res["failed"].append(f"loc_oob:{anchor}")
            continue
        hay = "\n".join(lines[lo - 1:hi])
        if q in hay:
            res["quotes_ok"] += 1
            res[status] += 1
        else:
            res["failed"].append(f"quote_missing:{anchor}")
    res["sources"] = len(cited)
    if len(cited) < 4:
        res["failed"].append("sources_floor")
    srcs = cat(repo, rev, "corpus/SOURCES.md")
    if srcs is None:
        res["failed"].append("registry_absent")
    else:
        reg = srcs.decode("utf-8", "replace")
        for f in sorted(cited):
            hit = False
            for line in reg.splitlines():
                if (f"{COPY_DIR}/{f}" in line and "| S" in line
                        and "| mined |" in line
                        and "psi-v73-recheck-r61.md" in line):
                    hit = True
                    break
            if not hit:
                res["failed"].append(f"rows_src:{f}")
    if res["pointers"] < floor:
        res["failed"].append(f"pointer_floor:{res['pointers']}<{floor}")
    if len(rows) != len(pointers):
        res["failed"].append("rows_ne_pointers")
    ok = not res["failed"]
    return res, ok


def fmt(res, ok, rev):
    return (f"{'C2=met' if ok else 'C2=unmet'} pointers={res['pointers']} "
            f"rows={res['rows']} same={res['same']} moved={res['moved']} "
            f"changed={res['changed']} quotes_ok={res['quotes_ok']} "
            f"spans_ok={res['spans_ok']} sources={res['sources']} "
            f"failed={';'.join(res['failed']) or 'none'} rev={rev}")


# ---------- selftest ----------

def selftest(scratch, floor):
    f1, f2, f3, f4 = "a.rst", "b.c", "c.txt", "d.h"
    copy1 = "\n".join(f"alpha line {i} stalled some full total" for i in range(1, 31))
    copy2 = "\n".join(f"beta line {i} decayed window avg10" for i in range(1, 31))
    copy3 = "\n".join(f"gamma line {i} omega shared best" for i in range(1, 31))
    copy4 = "\n".join(f"delta line {i} window misfit total" for i in range(1, 31))
    src_entry = ("Body mentions %s:5-7 and %s:9 and %s:30 and %s:9 and %s:12"
                 " and %s:20.\n" % (f1, f2, f1, f1, f3, f4) * 22)

    def build(name, ledger_rows, extra="", reg_status="mined",
              usedby="psi-v73-recheck-r61.md", tamper=None, prov=True):
        import shutil
        d = Path(scratch) / ("st-" + name)
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True, exist_ok=True)
        (d / "corpus/knowledge").mkdir(parents=True, exist_ok=True)
        (d / "corpus/evidence/sources-r61").mkdir(parents=True, exist_ok=True)
        c1, c2, c3, c4 = copy1, copy2, copy3, copy4
        if tamper == f1:
            c1 = copy1.replace("alpha", "ALPHA", 1)
        for f, c in ((f1, c1), (f2, c2), (f3, c3), (f4, c4)):
            (d / f"corpus/evidence/sources-r61/{f}").write_text(c)
        (d / "corpus/knowledge/system-pressure-r24.md").write_text(src_entry)
        prov_head = ("source: x\nverified-at: 2026-10-30\nrecheck: on-release\n"
                     if prov else "no frontmatter here\n")
        ledger = prov_head + extra + "\n| anchor | status | loc | quote |\n" + "\n".join(ledger_rows) + "\n"
        (d / f"corpus/knowledge/psi-v73-recheck-r61.md").write_text(ledger)
        reg_rows = [
            (f, f"S90{i}") for i, f in enumerate((f1, f2, f3, f4), start=1)]
        (d / "corpus").mkdir(exist_ok=True)
        (d / "corpus/SOURCES.md").write_text(
            "| id | source | kind | tier | scope | anchor | teaches | status"
            " | opened | recheck | used-by |\n|---|" + "---|" * 10 + "\n"
            + "\n".join(
                f"| {sid} | x {f} copy corpus/evidence/sources-r61/{f} | code"
                f" | A | psi | anchor | teaches | {reg_status} | 2026-10-30 |"
                f" on-release | {usedby} |" for f, sid in reg_rows) + "\n")
        for args in (["init", "-q"], ["add", "-A"]):
            subprocess.run(["git", "-C", str(d), *args], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(d), "-c", "user.name=t", "-c",
                        "user.email=t@t", "commit", "-qm", "x"],
                       check=True, capture_output=True)
        return str(d), subprocess.run(["git", "-C", str(d), "rev-parse", "HEAD"],
                                      capture_output=True, text=True).stdout.strip()

    # selftest pins: recompute from the synthetic copies
    saved_pins = dict(PINS)
    PINS.clear()
    for f, c in ((f1, copy1), (f2, copy2), (f3, copy3), (f4, copy4)):
        PINS[f] = hashlib.sha256(c.encode()).hexdigest()
    FILES[:] = [f1, f2, f3, f4]
    global NAMES
    NAMES = re.compile(r"(" + "|".join(re.escape(f) for f in FILES) + r"):(\d+)(?:-(\d+))?")

    good = [f"| {f1}:5-7 | same | - | `alpha line 5 stalled some` |",
            f"| {f1}:9 | same | - | `alpha line 9 stalled some full` |",
            f"| {f2}:9 | moved | {f2}:10 | `beta line 10 decayed window` |",
            f"| {f1}:30 | changed | {f2}:30 | `beta line 30 decayed window` |",
            f"| {f3}:12 | same | - | `gamma line 12 omega shared` |",
            f"| {f4}:20 | same | - | `delta line 20 window misfit` |"]
    cases = [
        ("good", good, {}, True),
        ("quote-missing", [good[0].replace("`alpha line 5 stalled some`", "`alpha line 20 stalled some`")] + good[1:], {}, False),
        ("row-missing", good[1:], {}, False),
        ("orphan", good + [f"| {f2}:25 | same | - | `beta line 25 decayed` |"], {}, False),
        ("small-span", [good[0].replace("`alpha line 5 stalled some`", "`a a a a a a`")] + good[1:], {}, False),
        ("dup-quote", [good[0], good[1].replace("`alpha line 9 stalled some full`", "`alpha line 5 stalled some`")] + good[2:], {}, False),
        ("not-mined", good, {"reg_status": "queued"}, False),
        ("usedby-miss", good, {"usedby": "other-entry.md"}, False),
        ("tampered-copy", good, {"tamper": f1}, False),
        ("no-prov", good, {"prov": False}, False),
    ]
    npass = 0
    for name, rows, kw, want in cases:
        repo, rev = build(name, rows, **kw)
        res, ok = measure(repo, rev, floor)
        good_case = ok == want
        npass += good_case
        print(f"case {name}: ok={ok} want={want} "
              f"{'pass' if good_case else 'FAIL'} failed={res['failed']}")
    PINS.clear(); PINS.update(saved_pins)
    print(f"C2_SELFTEST pass={npass} fail={len(cases) - npass}")
    return npass == len(cases)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rev", nargs="?")
    ap.add_argument("--repo", default=os.getcwd())
    ap.add_argument("--scratch", default=None)
    ap.add_argument("--floor", type=int, default=FLOOR_DEFAULT)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    scratch = a.scratch or os.environ.get("TMPDIR") or "/tmp"
    os.makedirs(scratch, exist_ok=True)
    if a.selftest:
        sys.exit(0 if selftest(scratch, a.floor) else 1)
    if not a.rev:
        ap.error("rev required without --selftest")
    res, ok = measure(a.repo, a.rev, a.floor)
    print(fmt(res, ok, a.rev))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
