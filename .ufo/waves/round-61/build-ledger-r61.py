#!/usr/bin/env python3
"""mori round-61 — build the PSI v7.3 recheck ledger (C2 data phase).

Reads the frozen v7.3 copies (corpus/evidence/sources-r61/, sha-pinned in
count-c2.py) and the r24 source entry, classifies every enumerated v7.2 line
pointer against Linux v7.3, and writes corpus/knowledge/psi-v73-recheck-r61.md.

Classification (v7.2 baseline copies fetched to $HYAKU_SCRATCH/mori-r61/v72,
sha256s recorded in the round lesson ## Gate):
  same    - the v7.2 span text is byte-identical at the same v7.3 line span
  moved   - the v7.2 span text is byte-identical elsewhere in the v7.3 copy
            (loc = the found span)
  changed - the span text differs; loc = the difflib-mapped v7.3 span and the
            quote is read from the v7.3 bytes there

Quotes: one per row, exact substring of the v7.3 copy at the stated span,
5-25 words, >=8 distinct bytes, no backtick/pipe, pairwise distinct.
"""
import difflib
import re
import sys
from pathlib import Path

REPO = Path("/home/vgpnk/Projects/shokunin/mori-shokunin")
V72 = Path("/fast/scratch/hyaku/mori-r61/v72")
COPY_DIR = REPO / "corpus/evidence/sources-r61"
ENTRY = REPO / "corpus/knowledge/system-pressure-r24.md"
LEDGER = REPO / "corpus/knowledge/psi-v73-recheck-r61.md"
FILES = ["psi.rst", "psi.c", "psi_types.h", "cgroup-v2.rst", "Kconfig",
         "kernel-parameters.txt"]
NAMES = re.compile(
    r"(" + "|".join(re.escape(f) for f in FILES) + r"):(\d+)(?:-(\d+))?")


def pointers(text):
    seen, out = set(), []
    for m in NAMES.finditer(text):
        key = f"{m.group(1)}:{m.group(2)}" + (f"-{m.group(3)}" if m.group(3) else "")
        if key not in seen:
            seen.add(key)
            out.append(key)
    return out


def span_of(key):
    f, rng = key.split(":")
    a, _, b = rng.partition("-")
    s = int(a)
    e = int(b) if b else s
    return f, s, e


def lines_of(path):
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def map_span(sm, s, e, n2):
    """Map a v7.2 line span to v7.3 coordinates through SequenceMatcher."""
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if i1 <= s - 1 <= i2:  # anchor start line inside this block (1-based s)
            off = (s - 1) - i1
            js = j1 + off
            off_e = min(e, i2) - i1
            je = min(j1 + off_e, j2 - 1)
            return (max(j1, js) + 1, max(j1, je) + 1, tag)
    return (s, e, "oob")


def pick_quote(lines, used):
    """Choose an exact-substring quote from the span lines.

    Backticks are excluded (they end the ledger cell); pipes are kept — the
    frozen counter's ROW regex reads the quote from inside the backticks, so
    pipes are legal there (needed for `Format: {always | ptrace | never}`).
    """
    cands = []
    for ln in lines:
        if "`" in ln:
            continue
        toks = [(t.start(), t.end()) for t in re.finditer(r"\S+", ln)]
        for w in range(min(25, len(toks)), 0, -1):
            for i in range(0, len(toks) - w + 1):
                q = ln[toks[i][0]:toks[i + w - 1][1]]
                if len(set(q.encode())) >= 8:
                    cands.append((-w, i, ln, q))
    for _, _, _, q in sorted(cands):
        if q not in used:
            used.add(q)
            return q
    return None


def main():
    text = ENTRY.read_text(encoding="utf-8", errors="replace")
    pts = pointers(text)
    v72, v73, sm = {}, {}, {}
    for f in FILES:
        v73[f] = lines_of(COPY_DIR / f)
        p72 = V72 / f
        v72[f] = lines_of(p72) if p72.exists() else None
        if v72[f] is None:
            print(f"WARN no v7.2 baseline for {f}; treating spans as changed",
                  file=sys.stderr)
            v72[f] = ["\x00"] * len(v73[f])
        sm[f] = difflib.SequenceMatcher(None, v72[f], v73[f], autojunk=False)

    used = set()
    rows = []
    stats = {}
    for key in pts:
        f, s, e = span_of(key)
        old = "\n".join(v72[f][s - 1:e])
        same_at = "\n".join(v73[f][s - 1:e]) == old
        loc = None
        if same_at:
            status = "same"
            ls, le = s, e
        else:
            hit = None
            block = old
            joined = "\n".join(v73[f])
            idx = joined.find(block)
            while idx != -1:
                ls = joined.count("\n", 0, idx) + 1
                le = ls + block.count("\n")
                if (ls, le) != (s, e):
                    hit = (ls, le)
                    break
                idx = joined.find(block, idx + 1)
            if hit:
                status = "moved"
                ls, le = hit
            else:
                status = "changed"
                ls, le, tag = map_span(sm[f], s, e, len(v73[f]))
            loc = f"{f}:{ls}" if ls == le else f"{f}:{ls}-{le}"
        hay_lines = v73[f][ls - 1:le]
        q = pick_quote(hay_lines, used)
        if q is None:
            print(f"NOQUOTE {key}", file=sys.stderr)
            sys.exit(2)
        rows.append((key, status, loc or "-", q, ls, le))
        stats.setdefault(f, {}).setdefault(status, 0)
        stats[f][status] += 1

    out = []
    out.append("corpus/knowledge/psi-v73-recheck-r61.md")
    out.append("=" * len(out[0]))
    out.append("")
    out.append("source: recheck of `corpus/knowledge/system-pressure-r24.md` (v7.2 line")
    out.append("anchors) against Linux v7.3, per the entry's `recheck:` trigger and the")
    out.append("round-53 release-recheck rule (`corpus/knowledge/kernel-v7.3-recheck-r53.md`).")
    out.append("verified-at: 2026-10-30 (round 61; six v7.3 copies pinned under")
    out.append("`corpus/evidence/sources-r61/`, sha256 in `.ufo/waves/round-61/count-c2.py`")
    out.append("`PINS`; fetch receipts `.ufo/waves/round-61/w1/Mo61ExecFetch.md`; v7.2")
    out.append("baseline sha256s in the round lesson `## Gate`)")
    out.append("recheck: on the next kernel release that touches `kernel/sched/psi.c`,")
    out.append("`include/linux/psi_types.h`, `Documentation/accounting/psi.rst`,")
    out.append("`Documentation/admin-guide/cgroup-v2.rst`, `init/Kconfig` PSI help, or")
    out.append("`Documentation/admin-guide/kernel-parameters.txt` (v7.4 gate)")
    out.append("")
    out.append("One row per v7.2 line pointer the r24 entry enumerates (deduped, in")
    out.append("first-mention order). `same` = byte-identical at the same v7.3 lines;")
    out.append("`moved` = byte-identical at the stated new span; `changed` = span text")
    out.append("differs at the stated v7.3 span (difflib-mapped). The anchor column keeps")
    out.append("the r24 v7.2 pointer; the location column is a v7.3 span.")
    out.append("")
    out.append("| anchor (v7.2) | status | v7.3 location | quote |")
    out.append("|---|---|---|---|")
    for key, status, loc, q, _, _ in rows:
        out.append(f"| {key} | {status} | {loc} | `{q}` |")
    out.append("")
    LEDGER.write_text("\n".join(out) + "\n", encoding="utf-8")

    total = {"same": 0, "moved": 0, "changed": 0}
    for f in FILES:
        st = stats.get(f, {})
        for k in total:
            total[k] += st.get(k, 0)
        print(f"{f:24} same={st.get('same',0)} moved={st.get('moved',0)} "
              f"changed={st.get('changed',0)}")
    print(f"TOTAL rows={len(rows)} {total}")
    print(f"quotes distinct={len(set(r[3] for r in rows))}/{len(rows)}")
    bad = [r[0] for r in rows
           if not (5 <= len(r[3].split()) <= 25) or len(set(r[3].encode())) < 8]
    print(f"constraint-violations={bad or 'none'}")


if __name__ == "__main__":
    main()
