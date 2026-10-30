#!/usr/bin/env python3
"""mori round-62 C1 counter — sound instrument for the r61 PSI v7.3 recheck ledger.

Fixes the r61 routed counter defects (corpus/lessons/round-61.md ## Mistakes 1-3):
  * quote floor is 1 word over multi-line hay (r61 floor of 5 words was
    unsatisfiable for 14 honest anchors of short C lines);
  * v7.2 bytes are pinned at rev (corpus/evidence/sources-r61/v7.2/) so the
    statuses are DERIVED, not trusted: per anchor the counter re-derives
    same/moved/changed from the pinned byte copies (list-based verbatim window
    search; difflib-free, byte-exact);
  * rows bind to Registry ids via a frozen ID_MAP (not substring scans).

Every printed token is one measured value; `met` is the conjunction of all
measured booleans (TOKEN_MAP discipline, r61 count-c3). No repo-supplied blob
is executed: the counter reads bytes with git cat-file / file reads only.
Scratch: --scratch (or TMPDIR) is honored; the selftest builds its synthetic
fixture repos under it with a throwaway identity, never outside it.
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
URL72 = {f: f"?h=v7.2" for f in FILES}
PINS73 = {
    "psi.rst": "11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692",
    "psi.c": "c4edc1e7c18ca76e6e29668093fa0b26d4251cb088f2d5feab24681f285ec63f",
    "psi_types.h": "483269b27c82b438450632555aba2ba8a9c47b608243f78a029c4300b3618ccc",
    "cgroup-v2.rst": "2750c11a6324e18f4d3a9bb63032b55f3268bd7077b80897af2f15a712611b68",
    "Kconfig": "d37de2a11baf81cbe6fb3c9ae271e5808a2c6be17f8980fe0375f6e67e677e0d",
    "kernel-parameters.txt": "b5a13c038a27e688380bbcaa8cdbcad24543ad6b64de0c3d5709bc32c94cb39a",
}
PINS72 = {
    "psi.rst": "11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692",
    "psi.c": "452318beaca3e6d19ab81a16528ae6b1695828a9ed080e329d07dedd9a3312c5",
    "psi_types.h": "483269b27c82b438450632555aba2ba8a9c47b608243f78a029c4300b3618ccc",
    "cgroup-v2.rst": "a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad",
    "Kconfig": "a43f09d89309a6bd7036c96e0836c30c021f2d56b042be288a15533dd9e944bd",
    "kernel-parameters.txt": "23b1a690210b6884f040a6b1e5baf1fc18856e844d30d4784470bd210953340c",
}
URL_FRAG = {
    "psi.rst": "Documentation/accounting/psi.rst?h=v7.3",
    "psi.c": "kernel/sched/psi.c?h=v7.3",
    "psi_types.h": "include/linux/psi_types.h?h=v7.3",
    "cgroup-v2.rst": "Documentation/admin-guide/cgroup-v2.rst?h=v7.3",
    "Kconfig": "init/Kconfig?h=v7.3",
    "kernel-parameters.txt": "Documentation/admin-guide/kernel-parameters.txt?h=v7.3",
}
ID_MAP = {
    "psi.rst": "S565", "psi.c": "S566", "psi_types.h": "S567",
    "cgroup-v2.rst": "S568", "Kconfig": "S569",
    "kernel-parameters.txt": "S570",
}
FLOOR_DEFAULT = 40
MIN_WORDS, MAX_WORDS, MIN_BYTES = 1, 25, 8
NAMES = re.compile(
    r"(" + "|".join(re.escape(f) for f in FILES) + r"):(\d+)(?:-(\d+))?")
ROW = re.compile(
    r"^\|\s*([a-zA-Z0-9_.\-]+:\d+(?:-\d+)?)\s*\|\s*(same|moved|changed)\s*\|"
    r"\s*([a-zA-Z0-9_.\-]+:\d+(?:-\d+)?|-)\s*\|\s*`([^`]*)`\s*\|")
SPAN = re.compile(r"([a-zA-Z0-9_.\-]+):(\d+)(?:-(\d+))?")


def sh(repo, *args, binary=False):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout if binary else r.stdout.decode("utf-8", "replace")


def cat(repo, rev, path):
    return sh(repo, "show", f"{rev}:{path}", binary=True)


def norm(t):
    return " ".join(t.split())


def span_of(key):
    m = SPAN.fullmatch(key)
    if not m:
        return None
    s = int(m.group(2))
    e = int(m.group(3)) if m.group(3) else s
    return m.group(1), s, e


def lines_at(lines, s, e):
    if s < 1 or e < s or e > len(lines):
        return None
    return lines[s - 1:e]


def derive_status(v72l, v73l, f, s, e):
    """Ground truth for one anchor: ('same',None)|('moved',(st,en))|('changed',None)."""
    old = lines_at(v72l, s, e)
    if old is None:
        return "changed", None
    new = lines_at(v73l, s, e)
    if new == old:
        return "same", None
    n = len(old)
    if e <= len(v73l):
        for i in range(0, len(v73l) - n + 1):
            if v73l[i:i + n] == old:
                return "moved", (i + 1, i + n)
    return "changed", None


def enumerate_pointers(text, files):
    rx = re.compile(
        r"(" + "|".join(re.escape(f) for f in files) + r"):(\d+)(?:-(\d+))?")
    seen, out = set(), []
    for m in rx.finditer(text):
        key = f"{m.group(1)}:{m.group(2)}" + (f"-{m.group(3)}" if m.group(3) else "")
        if key not in seen:
            seen.add(key)
            out.append(key)
    return out


def provenance_ok(entry_text):
    head = entry_text[:2000]
    return all(re.search(rf"^{band}:", head, re.M)
               for band in ("source", "verified-at", "recheck"))


def measure(repo, rev, floor=FLOOR_DEFAULT, files=None, pins73=None, pins72=None,
            id_map=None, url_frag=None):
    files = files or FILES
    pins73 = pins73 or PINS73
    pins72 = pins72 or PINS72
    id_map = id_map or ID_MAP
    url_frag = url_frag or URL_FRAG
    res = {"pointers": 0, "rows": 0, "same": 0, "moved": 0, "changed": 0,
           "quotes_ok": 0, "derived_ok": 0, "failed": []}
    failed = res["failed"]

    def bad(tag):
        failed.append(tag)

    src = cat(repo, rev, SOURCE_ENTRY)
    if src is None:
        bad("source_entry_absent")
        return res, False
    pointers = enumerate_pointers(src.decode("utf-8", "replace"), files)
    res["pointers"] = len(pointers)
    if res["pointers"] < floor:
        bad(f"pointer_floor:{res['pointers']}<{floor}")

    led = cat(repo, rev, LEDGER)
    if led is None:
        bad("entry_absent")
        return res, False
    led_text = led.decode("utf-8", "replace")
    if not provenance_ok(led_text):
        bad("provenance")

    v72, v73 = {}, {}
    for f in files:
        for tag, pins, store in (("72", pins72, v72), ("73", pins73, v73)):
            b = cat(repo, rev, f"{COPY_DIR}/v7.2/{f}" if tag == "72" else f"{COPY_DIR}/{f}")
            if b is None:
                bad(f"copy{tag}_absent:{f}")
            elif hashlib.sha256(b).hexdigest() != pins[f]:
                bad(f"copy{tag}_pin:{f}")
            else:
                store[f] = b.decode("utf-8", "replace").splitlines()
    if len(v72) != len(files) or len(v73) != len(files):
        return res, False

    rows = []
    for line in led_text.splitlines():
        m = ROW.match(line.strip())
        if m:
            rows.append(m.groups())
    res["rows"] = len(rows)
    anchors = [r[0] for r in rows]
    if len(anchors) != len(set(anchors)):
        bad("dup_anchor")
    if set(anchors) != set(pointers):
        miss = sorted(set(pointers) - set(anchors))[:5]
        orph = sorted(set(anchors) - set(pointers))[:5]
        if miss:
            bad("rows_missing:" + ",".join(miss))
        if orph:
            bad("rows_orphan:" + ",".join(orph))
    seen_q = set()
    for anchor, status, loc, quote in rows:
        q = quote.strip()
        if not (MIN_WORDS <= len(q.split()) <= MAX_WORDS):
            bad(f"quote_words:{anchor}")
            continue
        if len(set(q.encode("utf-8", "replace"))) < MIN_BYTES:
            bad(f"span_small:{anchor}")
            continue
        if q in seen_q:
            bad(f"quote_dup:{anchor}")
            continue
        seen_q.add(q)
        sp = span_of(anchor)
        if sp is None or sp[0] not in v72:
            bad(f"anchor_bad:{anchor}")
            continue
        f, s, e = sp
        old = lines_at(v72[f], s, e)
        if old is None or norm(q) not in norm("\n".join(old)):
            bad(f"quote_span:{anchor}")
            continue
        res["quotes_ok"] += 1
        derived, dloc = derive_status(v72[f], v73[f], f, s, e)
        res[derived] += 1
        ok_row = derived == status
        if derived == "moved":
            ml = SPAN.fullmatch(loc) if loc and loc != "-" else None
            want = (int(ml.group(2)), int(ml.group(3) or ml.group(2))) if ml else None
            if want != dloc:
                ok_row = False
        elif derived == "same" and loc != "-":
            ok_row = False
        if ok_row:
            res["derived_ok"] += 1
        else:
            bad(f"derived_mismatch:{anchor}")

    registry = cat(repo, rev, "corpus/SOURCES.md")
    if registry is None:
        bad("registry_absent")
    else:
        reg_lines = registry.decode("utf-8", "replace").splitlines()
        for f in files:
            sid = id_map[f]
            hit = None
            for line in reg_lines:
                cells = line.split("|")
                if len(cells) >= 12 and cells[1].strip() == sid:
                    hit = cells
                    break
            if hit is None:
                bad(f"rows_src:{sid}")
                continue
            if len(hit) != 13:
                bad(f"rows_cols:{sid}")
            if hit[2].strip() and url_frag[f] not in hit[2]:
                bad(f"rows_url:{sid}")
            if hit[8].strip() != "mined":
                bad(f"rows_mined:{sid}")
            if Path(LEDGER).name not in hit[11]:
                bad(f"rows_usedby:{sid}")
    ok = not failed
    return res, ok


def fmt(res, ok, rev):
    return (f"{'C1=met' if ok else 'C1=unmet'} pointers={res['pointers']} "
            f"rows={res['rows']} same={res['same']} moved={res['moved']} "
            f"changed={res['changed']} quotes={res['quotes_ok']} "
            f"derived={res['derived_ok']} "
            f"failed={';'.join(res['failed']) or 'none'} rev={rev}")


# ---------- selftest ----------

def selftest(scratch, floor):
    fa, fb = "a.c", "b.rst"
    base_a = [f"alpha token{i} stall window avg" for i in range(1, 41)]
    base_b = [f"beta doc {i} pressure some full total" for i in range(1, 41)]
    # v73: 3-line span moved from a:10-12 to the end; b:30 changed in place
    v73a = base_a[:9] + base_a[12:] + base_a[9:12]
    v73b = list(base_b)
    v73b[29] = "beta doc 30 pressure CHANGED full total"
    copies = {fa: (base_a, v73a), fb: (base_b, v73b)}
    pins72 = {f: hashlib.sha256(("\n".join(v) + "\n").encode()).hexdigest()
              for f, (v, _) in copies.items()}
    pins73 = {f: hashlib.sha256(("\n".join(v) + "\n").encode()).hexdigest()
              for f, (_, v) in copies.items()}
    src_entry = (f"anchors: {fa}:10-12 {fb}:30 {fa}:1 {fb}:5-6 {fa}:9\n")
    # ground truth: a:10-12 moved to 38-40; b:30 changed; rest same
    good = [
        f"| {fa}:10-12 | moved | {fa}:38-40 | `alpha token10 stall window` |",
        f"| {fb}:30 | changed | - | `beta doc 30 pressure some full` |",
        f"| {fa}:1 | same | - | `alpha token1 stall` |",
        f"| {fb}:5-6 | same | - | `beta doc 5 pressure` |",
        f"| {fa}:9 | same | - | `alpha token9 stall` |",
    ]
    reg = ("| id | source | kind | tier | scope | anchor | teaches | status"
           " | opened | recheck | used-by |\n|---|" + "---|" * 10 + "\n"
           + "\n".join(
               f"| S9{i} | x {f} ?h=v7.3-{f} | code | A | psi | anchor | t | mined"
               f" | 2026-10-30 | on-release | psi-v73-recheck-r61.md |"
               for i, f in enumerate((fa, fb), start=1)))

    def build(name, rows, tamper=None, reg_text=reg, prov=True):
        import shutil
        d = Path(scratch) / ("st-" + name)
        shutil.rmtree(d, ignore_errors=True)
        (d / "corpus/knowledge").mkdir(parents=True)
        (d / f"corpus/evidence/sources-r61/v7.2").mkdir(parents=True)
        for f, (vold, vnew) in copies.items():
            a, b = "\n".join(vold) + "\n", "\n".join(vnew) + "\n"
            if tamper == f + "72":
                a = a.replace("token1 ", "tokenX ", 1)
            if tamper == f + "73":
                b = b.replace("token1 ", "tokenX ", 1)
            (d / f"corpus/evidence/sources-r61/v7.2/{f}").write_text(a)
            (d / f"corpus/evidence/sources-r61/{f}").write_text(b)
        (d / "corpus/knowledge/system-pressure-r24.md").write_text(src_entry)
        head = ("source: x\nverified-at: 2026-10-30\nrecheck: on-release\n"
                if prov else "no frontmatter\n")
        ledger = head + "\n| anchor | status | loc | quote |\n" + "\n".join(rows) + "\n"
        (d / "corpus/knowledge/psi-v73-recheck-r61.md").write_text(ledger)
        (d / "corpus/SOURCES.md").write_text(reg_text)
        for args in (["init", "-q"], ["add", "-A"]):
            subprocess.run(["git", "-C", str(d), *args], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(d), "-c", "user.name=t", "-c",
                        "user.email=t@t", "commit", "-qm", "x"],
                       check=True, capture_output=True)
        return str(d), subprocess.run(["git", "-C", str(d), "rev-parse", "HEAD"],
                                      capture_output=True, text=True).stdout.strip()

    kw = dict(pins73=pins73, pins72=pins72, floor=len(good), files=[fa, fb],
              id_map={fa: "S91", fb: "S92"},
              url_frag={fa: f"?h=v7.3-{fa}", fb: f"?h=v7.3-{fb}"})
    cases = [
        ("good", good, {}, True),
        ("floor1-short-quote-passes", [good[0].replace("`alpha token10 stall window`", "`token10 stall`")] + good[1:], {}, True),
        ("same-but-moved", [good[0].replace("| moved |", "| same |")] + good[1:], {}, False),
        ("moved-wrong-loc", [good[0].replace(f"{fa}:38-40", f"{fa}:37-39")] + good[1:], {}, False),
        ("moved-but-same", [good[0].replace("| moved |", "| moved |"), good[1]] + [], {}, True),  # placeholder replaced below
        ("quote-not-in-span", [good[0].replace("`alpha token10 stall window`", "`alpha token20 stall window`")] + good[1:], {}, False),
        ("dup-quote", [good[0], good[1], good[2], good[3].replace("`beta doc 5 pressure`", "`alpha token10 stall window`"), good[4]], {}, False),
        ("row-missing", good[1:], {}, False),
        ("orphan", good + [f"| {fb}:39 | same | - | `beta doc 39 pressure` |"], {}, False),
        ("degenerate-quote", [good[2].replace("`alpha token1 stall`", "`a a a a a a a`")] + [good[0], good[1], good[3], good[4]], {}, False),
        ("tamper-72", good, {"tamper": fa + "72"}, False),
        ("tamper-73", good, {"tamper": fa + "73"}, False),
        ("not-mined", good, {"reg_text": reg.replace("| mined |", "| queued |")}, False),
        ("usedby-miss", good, {"reg_text": reg.replace("psi-v73-recheck-r61.md", "other.md")}, False),
        ("no-prov", good, {"prov": False}, False),
    ]
    # fix "moved-but-same": declare moved for an anchor that is same
    cases[4] = ("moved-but-same",
                [f"| {fa}:1 | moved | {fa}:2 | `alpha token1 stall` |"] + good[1:],
                {}, False)
    npass = 0
    for name, rows, kwx, want in cases:
        repo, rev = build(name, rows, **kwx)
        m = dict(kw)
        m.update(kwx.get("measure", {}))
        res, ok = measure(repo, rev, **m)
        good_case = ok == want
        npass += good_case
        print(f"case {name}: ok={ok} want={want} "
              f"{'pass' if good_case else 'FAIL'} failed={res['failed']}")
    print(f"C1_SELFTEST pass={npass} fail={len(cases) - npass}")
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
    res, ok = measure(a.repo, a.rev)
    print(fmt(res, ok, a.rev))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
