# ExecRealRegistryAudit — v3 R5/R6 pin audit of the real registry at entering tip

Seat: `ExecRealRegistryAudit` (leaf, no subagents). Lane: mori-shokunin.
Measured revision: **e5dbac05459887d9597ea5d1da0d8e3d024e0d17** (entering tip, round 47
non-author closure) — the revision named by the assignment for the audit. Note: the
repo HEAD is the round-48 freeze commit `4387cf94`; the SKILL.md bytes audited here are
**e5dbac05**'s (`git show`), per assignment.

## Method

1. `git show e5dbac05:SKILL.md` → 939 lines (scratch `skill-entering.md`).
2. `git archive e5dbac05 | tar -x` into scratch `tree/` (12,111 regular files; the
   scanner skipped non-regular entries, e.g. a dangling symlink), so every candidate
   path resolves against the exact measured revision.
3. Parsed with the v2 tool's `parse_registry` imported from a **scratch copy** of
   `tools/mori-pin-check.py` (verbatim at e5dbac05; sha256
   `9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6`).
   `parse_registry` yields 55 self-test rows, all `state=ok`; no header miss
   (case-insensitive `self-test` header match).
4. Found the two v3 kinds in every self-test cell: line-count pins `(\d+) lines`
   (R5) and truncated digests `[0-9a-f]{8,63}…` (R6, U+2026). Bound per spec:
   R5 → nearest preceding path token in the same cell that resolves to a file inside
   the measured tree; R6 → any path named in the row (all cells) resolving inside the
   tree. Truth: newline count (count of LF bytes) and sha256 prefix at e5dbac05.
5. Same kinds outside self-test cells (pinned-values cells, other table cells, prose)
   enumerated separately as out-of-scope with the same truth values.
6. Whole-tree sha256-prefix scan (12,111 files) to independently confirm every digest
   pin's match or non-match.

## Script used (fenced)

```python
#!/usr/bin/env python3
import re, sys, os, hashlib
sys.path.insert(0, "/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecRealRegistryAudit")
from mori_pin_check_v2 import parse_registry
ROOT = "/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecRealRegistryAudit/tree"
SK = "/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecRealRegistryAudit/skill-entering.md"
LINE_PIN = re.compile(r"(\d+)\s+lines\b")
TRUNC_DIGEST = re.compile(r"[0-9a-f]{8,63}…")
TOK = re.compile(r"(?<![\w./-])[A-Za-z0-9_.][A-Za-z0-9_./-]*\.(?:py|sh|json|md|txt|tsv|html)\b")

def resolve(p):
    p = p[2:] if p.startswith("./") else p
    if p.startswith("/") or ":" in p or p.startswith(".."):
        return None
    fp = os.path.join(ROOT, p)
    return fp if os.path.isfile(fp) else None

def sha(fp, n):
    h = hashlib.sha256(); h.update(open(fp, 'rb').read()); return h.hexdigest()[:n]

def nl(fp):
    return open(fp, 'rb').read().count(b"\n")

def nearest_before(toks, pos):
    best = None
    for p, t in toks:
        if p >= pos:
            break
        fp = resolve(t)
        if fp is not None:
            best = (t, fp)
    return best

def cell_cands(cells):
    cands = []
    for c in cells:
        for m in TOK.finditer(c):
            fp = resolve(m.group(0))
            if fp is not None:
                cands.append((m.group(0), fp))
    return cands

def scan_cell(cell, rowline, rowname, inscope):
    toks = [(m.start(), m.group(0)) for m in TOK.finditer(cell)]
    for m in sorted(list(LINE_PIN.finditer(cell)) + list(TRUNC_DIGEST.finditer(cell)),
                    key=lambda m: m.start()):
        if m.group(0).endswith("…"):
            pref = m.group(0)[:-1]
            cands = cell_cands([cell])
            hit = next(((t, fp) for t, fp in cands if sha(fp, len(pref)) == pref), None)
            tag = "IN-SCOPE" if inscope else "OUT-OF-SCOPE"
            if hit:
                print("%s DIGEST line=%d row=%r %s… -> %s MATCH" % (tag, rowline, rowname, pref, hit[0]))
            else:
                print("%s DIGEST line=%d row=%r %s… -> MISMATCH (cell paths: %s)"
                      % (tag, rowline, rowname, pref, ", ".join(t for t, _ in cands) or "none"))
        else:
            n = int(m.group(1)); b = nearest_before(toks, m.start())
            tag = "IN-SCOPE" if inscope else "OUT-OF-SCOPE"
            if b is None:
                print("%s LINE line=%d row=%r (%d lines) UNBOUND -> unparsed" % (tag, rowline, rowname, n))
            else:
                t, fp = b
                print("%s LINE line=%d row=%r (%d lines) -> %s true_nl=%d %s"
                      % (tag, rowline, rowname, n, t, nl(fp), "MATCH" if nl(fp) == n else "MISMATCH"))

text = open(SK, encoding="utf-8").read()
lines = text.split("\n")
rows = parse_registry(text)

print("== IN-SCOPE (self-test cell) ==")
for r in rows:
    if r["state"] != "ok":
        continue
    scan_cell(r["cells"][r["idx"]], r["line"], r["cells"][0], True)

print("\n== OUT-OF-SCOPE (non-self-test cells of parsed rows) ==")
for r in rows:
    if r["state"] != "ok":
        continue
    for ci, c in enumerate(r["cells"]):
        if ci != r["idx"]:
            scan_cell(c, r["line"], r["cells"][0] + " [cell %d]" % ci, False)

print("\n== OUT-OF-SCOPE (prose lines) ==")
parsed_lines = {r["line"] for r in rows}
for i, line in enumerate(lines, 1):
    if i in parsed_lines or line.strip().startswith("|"):
        continue
    scan_cell(line, i, "(prose)", False)

```

Run: `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecRealRegistryAudit python3 .scratch/r48-ExecRealRegistryAudit/audit_pins2.py`
— exit 0 (full output retained in `.scratch/r48-ExecRealRegistryAudit/audit2.out`).
Whole-tree prefix confirmation was a separate read-only walk (12,111 files) over the same
exported tree.

## In-scope pins (R5/R6, inside self-test cells)

| # | pin kind | row | SKILL.md line | pin text | binds to (R5 nearest preceding path / R6 any row path) | true value at e5dbac05 | verdict |
|---|---|---|---|---|---|---|---|
| 1 | truncated digest (R6) | r14 regressions | 168 | `c39e5a73…` | none of the row paths (`tools/mori-round14-regressions.py` 533218a566…, `tools/mori-census.sh` 87b8d680…, `.ufo/waves/round-14/frozen/mori-census.sh` 39abda0a67…, `evidence/r14-selftest-accepted.json` → `.ufo/waves/round-14/evidence/r14-selftest-accepted.json` 7c19bc08…); whole-tree scan: **no file** starts `c39e5a73` | no local sha256 prefix matches | **MISMATCH** |
| 2 | line-count (R5) | r44 gate registry (C2) | 184 | `(743 lines)` | `tools/mori-gate-registry.py` (only path token in the cell) | 743 newlines | MATCH |
| 3 | truncated digest (R6) | r45 corpus coverage (C3) | 192 | `37fd7c24ff52…` | `.ufo/waves/round-45/count-c3.py` | sha256 `37fd7c24ff52d6aa…` | MATCH |
| 4 | truncated digest (R6) | r45 corpus coverage (C3) | 192 | `69bf9b6eb29b…` | `.ufo/waves/round-45/fixtures/mutants/count-c3.py` | sha256 `69bf9b6eb29b7818…` | MATCH |
| 5 | line-count (R5) | r44 gate registry (C2) — write scope superseded | 194 | `(743 lines)` | `tools/mori-gate-registry.py` | 743 newlines | MATCH |

Notes:

- The `c39e5a73…` pin is **stale**: `git show 5601d12:tools/mori-round14-regressions.py`
  and `git show 0fa5e0d:tools/mori-round14-regressions.py` both hash to
  `c39e5a7352666d09…` (the accepted r14 harness blob), while the file at e5dbac05 hashes
  to `533218a566030fda…`. It is a J8-class stale truncated digest exposed by R6.
- R5's "no path → unparsed" branch is not triggered anywhere: all three `(N lines)` pins
  have a resolvable preceding path.
- Full 64-hex digests (v2 kind, not v3-new) also sit on lines 184/191/194
  (`8b82ac…`, `153423c48c…`) — all verified matching their tools; they are outside this
  audit's two kinds and were not re-audited beyond this confirmation.

## Out-of-scope same-kind pins (outside self-test cells)

| line | where | pin | binder | truth at e5dbac05 | verdict |
|---|---|---|---|---|---|
| 31 | data row (journal class counts), claim cell | `fe6faa94…`, `d989611b…`, `fc2e22bc…`, `98e32220…`, `d9b373ed…` | systemd catalog message IDs (external, referenced from URLs); no local repo path in the row | whole-tree scan: no match | N/A — external IDs, no local binder |
| 32 | data row (positive OOM notice), claim cell | `fe6faa94…` | ditto | no match | N/A — external |
| 168 | r14 pinned-values cell (cell 5) | `39abda0a…` | `.ufo/waves/round-14/frozen/mori-census.sh` | sha256 `39abda0a67…` | MATCH |
| 169 | r15 pinned-values cell (cell 5) | `0e41cb83…` | `.ufo/waves/round-15/frozen/mori-census.sh` (named as `--frozen` default in the entry cell) | sha256 `0e41cb83fc…` | MATCH |
| 191 | r45 gate conformance pinned-values cell (cell 5) | `(743 lines)` | `tools/mori-gate-registry.py` (`AUDITOR_REL`) | 743 newlines | MATCH |
| 255 | prose (r14 gate description) | `39abda0a…` | `.ufo/waves/round-14/frozen/mori-census.sh` | sha256 `39abda0a67…` | MATCH |
| 279 | prose (r15 gate description) | `0e41cb83…` | `.ufo/waves/round-15/frozen/mori-census.sh` (committed copy in tree) | sha256 `0e41cb83fc…` | MATCH |
| 322 | prose (drift baseline description) | `d7710981…` | `corpus/evidence/baseline-r10-20261015T2231Z.json` | sha256 `0993b23505…` ≠ `d7710981` (only round-20 falsify census copies carry `d7710981`) | MISMATCH at this revision (dated reference to the 2026-10-15 census) |
| 732 | data row (oom_kill=0), reading cell | `d989611b…` | oomd notice catalog ID; no local path | no match | N/A — external |
| 817 | blind-writer gate pinned-values cell (cell 5) | `79b774f7…` | `tools/mori-blind-check.sh` | sha256 `79b774f773…` | MATCH |
| 817 | blind-writer gate pinned-values cell (cell 5) | `3c26ef69…` | none (siblings: `expected.json` `45226329fa…`, `verify.sh` `31385477cd…`) | whole-tree scan: no match | MISMATCH (stale) |

## What the landed v3 would flag (for L1 repair before measuring)

Under v3 R5/R6 as specified, the real registry at entering tip e5dbac05 contains
exactly **one in-scope failing pin**:

- **SKILL.md:168 — `r14 regressions` row**: truncated digest `c39e5a73…` mismatches
  (no path named in the row, and no file anywhere in the measured tree, carries that
  sha256 prefix; the pin matches the *historical* r14 harness blob at 5601d12/0fa5e0d).
  → v3 would emit `pin line=168 kind=digest state=mismatch …` and the run would end
  `PIN_CHECK=unmet digest_pins=… mismatches=1`.

All other R5/R6 pins in self-test cells (lines 184, 192 ×2, 194) match, so repairing
the single line-168 pin is sufficient for the real registry to stay `PIN_CHECK=met`
under v3 (the two out-of-scope stale entries — line 322 `d7710981…` and line 817
`3c26ef69…` — sit outside self-test cells and would not trip v3). Suggested repair
direction for L1 (registry change, per v3 spec "repaired in the registry, never excused
in the tool"): retarget the harness SHA to the current blob `533218a566…`
(`tools/mori-round14-regressions.py` at e5dbac05) or to the accepted receipt
`.ufo/waves/round-14/evidence/r14-selftest-accepted.json` (`7c19bc08…`), or drop the
stale pin.

## Constraints honored

- No production file touched: only this report plus scratch under
  `.scratch/r48-ExecRealRegistryAudit/` (skill-entering.md, exported tree/, v2 tool
  copy, audit scripts, .out files). Read-only git (`show`/`archive`/`rev-list`) only;
  lane tools run with `TMPDIR=.scratch/r48-ExecRealRegistryAudit`; no installs (no
  tooling authorization record — nothing was installed); `TMPDIR` was set per lane
  rule, though the audit runs no lane tool (only an import of `parse_registry`).
