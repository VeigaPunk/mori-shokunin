# Round 41 — 2026-10-24 (L1 mori-r41, attempt 2; attempt 1 died post-freeze, pre-report)

Round claims: C1 operability — conformance binding model v4 (P-C10 r41);
C2 depth — append-only gate P-C12; C3 calibration — append-only correction
records for the r40 34/16 → 35/17 count error. Entering tip
`62a207f7521fa2e2fcd2e8b0260f047ccfce8862` (r40 closure
`corpus/lessons/round-40-verifier-spotcheck.md`, REJECTED rejected-honest-stop;
ten routed defects inherited as this round's work list).

## Gate

Candidates considered this round (frontier step):

| source | decision | reason |
|---|---|---|
| S230 — Python 3.13 Language Reference §7.2 Assignment statements, https://docs.python.org/3.13/reference/simple_stmts.html#assignment-statements | **admitted** (tier A, scoped to assignment-target binding semantics incl. tuple/list destructuring) | opened 2026-10-24; grounds C1's binding inventory — the walrus/tupleunpack/deadloop survivors are exactly "not direct `ast.Name` targets" cases. Located quote (copy `corpus/evidence/sources-r41/S230.src:301-303`, 22 words): "Else: The object must be an iterable with the same number of items as there are targets in the target list, and the items are assigned, from left to right, to the corresponding targets." |
| S231 — Python 3.15.1 execution model §4.2.2 (located-quote correction), https://docs.python.org/3.15/reference/executionmodel.html#naming-and-binding | **admitted** (tier A, scoped to the corrected S229 locator/word count) | opened 2026-10-24; the r40 closure (routed defect 9) found S229's recorded 15-word count is 17 and its ":254-256" locator resolves under neither raw-HTML nor stripped-text numbering. S231 `supersedes S229` carrying the corrected anchor: `corpus/evidence/sources-r40/S229.src:294-296` (17 words): "When a name is used in a code block, it is resolved using the nearest enclosing scope." Re-verified byte-exact at `corpus/evidence/sources-r41/S231.src:294-295` — same sentence at the same line coordinates in the 3.15 copy. |
| Rejected: none new | — | the bounded search (contract's routed-defect list) identified 2 sources, screened 2, included 2, excluded 0. Stop: both routed defects (C1 binding grounding, S229 locator repair) discharged. |

Row changes (append-only; `status`/`used-by` mutable cells):
- S230 added `queued`→`mined` at admission: `used-by` `—` → `corpus/knowledge/conform-bindings-r41.md`.
- S231 added `queued`→`mined` at admission: `used-by` `—` → `corpus/knowledge/conform-bindings-r41.md`.
- No existing row's `status`/`recheck`/`used-by` changed in place this round.

Spot-check: no named non-author spot-check in-round (L1-authored gate);
wave seats (prepared, 64-item spec `w1-spec.json`) sample admits/rejects
independently where dispatched.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M25 | number-drift (a correction record recurred off-by-one in three committed files) | r40 closure `corpus/lessons/round-40-verifier-spotcheck.md` §"Number-drift in the correction layer": SCORECARD.md "34 as-of ids", LOG.md:2296 "34", lesson M24 "16 rows" vs the gate's re-measured 35/17 | `tools/mori-round41-calibration.py` (frozen counter, reference `62a207f…`); QUALITY 20 (tally cites the counted universe recomputed from delivered artifacts) — should have caught it; the records were written before the gate re-derivation | appended `Round-41 calibration correction: observed_as_of=35; extension_rows=17.` in SCORECARD.md, LOG.md, and `corpus/lessons/round-40.md`; the counter now reads the correction record, not the stale prose. Shown able to fail: the before-run of the same counter prints `mismatches=6` (`evidence/control-before.txt` C3 section) |
| M26 | landing (registry rows committed without their opened-source copies) | attempt-1 commit `d72ac16` added S230/S231 rows + `corpus/knowledge/conform-bindings-r41.md` citing them, but no `corpus/evidence/sources-r41/` copies existed; QUALITY 9 (every path/citation resolves at the carrying commit) | none — the census checks row shape, not copy presence; the locator claims were unverifiable until the copies landed | fetched and committed `corpus/evidence/sources-r41/{S230,S231}.src` this round; located quotes re-derived from the committed bytes. Shown able to fail: `test -f corpus/evidence/sources-r41/S230.src` exits 1 at `d72ac16` |

Attempt-1 inheritance note: this attempt re-verified every inherited byte
before reuse — all 19 `freeze-r41.txt` pins hash-match the committed tip
(`evidence/freeze-verify.txt`); the frozen `control-before.txt` semantics were
re-derived (`evidence/control-after.txt` before-state columns agree);
`.scratch/round22/` (lane-authored 2026-10-21 fixtures, untracked) committed
for durability; the r40 stray `265a955` was already gone and the three
worktree-modified c10 receipts were already committed by attempt 1.
