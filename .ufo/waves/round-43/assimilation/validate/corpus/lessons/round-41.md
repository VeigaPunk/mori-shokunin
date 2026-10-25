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
| M27 | count-universe conflation (a supersede-set extension at the r41 tip read as re-opening the calibrated r40 baseline counts) | w1 scribe draft `w1/ScrM26Number.md` §"Draft M26": `evidence/control-after.txt` §"C2 after lane line" (36 as-of incl. S229, stale `[]`) vs `evidence/calibration-after.txt` (`mismatches=0 observed_as_of=35 extension_rows=17`, reference-derived); the two numbers count different revisions of one append-only ledger | none today — the frozen counter is `--reference-rev 62a207f…`-pinned and reads only the three single-line records, so nothing in-round named the 35-vs-36 tension | correction-layer sentence (below, Adjudication) records that 35/17 is the frozen r40 gate's derivation at reference `62a207f…` while 36 is the r41 tip's own timing line (S231 extends the eligible set by one never-edited id); neither supersedes the other. Shown able to fail: in a disposable sandbox clone at `7450722e`, committing the r40 lesson record drifted to `observed_as_of=36` makes the frozen counter report `mismatches=1` exit 1 (mutant `d4475417…`, probe never pushed) |
| M28 | silent-survivor (a conformance checker's function-local binding inventory under-approximates the store forms that reach a `timeout=` read site, so a counter that rebinds its own `timeout` to `None` mid-function still prints `CONFORM=met`) | w1 scribe draft `w1/ScrM25Survivor.md` §"Draft M25"; r40 verifier closure `corpus/lessons/round-40-verifier-spotcheck.md` §"Per-claim re-check — C1" — verdict falsified by the live new-survivor class; reproduction at closure :53-71: three fixtures (`survivor-deadloop-rebind.py`, `survivor-walrus-none.py`, `survivor-tupleunpack-none.py`) each print `CONFORM=met` under the frozen v3 checker | P-C10 (round 41) — the contract predicate for C1, frozen before data; r40 closure routed defect 1 | C1 v4 binding inventory in `.ufo/waves/round-41/conform.py`: source-ordered `Assign`/`AnnAssign`, `NamedExpr`, destructuring, for/with targets; fail-closed on unresolved/unsupported/disagreeing bindings. Shown able to fail: `evidence/control-before.txt` §C1 — the extracted v3 bytes still print `CONFORM=met` exit 0 on all three survivors at the entering tip, while `evidence/control-after.txt` §C1 prints `CONFORM=unmet` exit 1 (only `timeout_scope` FAIL) on each at the landed tip |

Adjudication (L1 mori-r41 attempt 3, 2026-10-24): wave scribe drafts
`w1/ScrM25Survivor.md` (draft M25 = silent-survivor) and `w1/ScrM26Number.md`
(draft M26 = count-universe conflation) collided with the landed M25/M26 ids
(number-drift, landing — committed by attempt 2, cited at `LOG.md:2356` as
"Mistakes M25–M26"). No landed row is rewritten (append-only); both drafted
classes are appended here as M27/M28 with their drafted evidence pointers and
demonstrated fixes. The landed M25/M26 rows remain the canonical records for
their classes.

S230 located-quote erratum: the Gate table above records the S230 quote at
`corpus/evidence/sources-r41/S230.src:301-303` as "22 words". Measured against
the committed copy at `7450722e`, the markup-stripped sentence is 34
whitespace tokens ("Else: The object must be an iterable with the same number of
items as there are targets in the target list, and the items are assigned, from
left to right, to the corresponding targets."), above the 25-word gate limit.
Corrected located quote (verbatim, contiguous, 20 words, same coordinates):
`corpus/evidence/sources-r41/S230.src:301-303` — "The object must be an iterable
with the same number of items as there are targets in the target list." The
SOURCES.md S230 row carries no word count, so no immutable registry cell is
affected; this erratum is the lesson-layer correction (M25-class drift in this
round's own Gate text).

Attempt-1 inheritance note: this attempt re-verified every inherited byte
before reuse — all 19 `freeze-r41.txt` pins hash-match the committed tip
(`evidence/freeze-verify.txt`); the frozen `control-before.txt` semantics were
re-derived (`evidence/control-after.txt` before-state columns agree). The
inherited untracked `.scratch/round22/` (lane-authored 2026-10-21) was
resolved: its JSON/Python measurement records (154 files) are committed under
this round; its `*-fixtures/` trees (~120 nested-git sandbox clones, ~646 MB)
were deleted as transient scratch — regenerable from the committed builder
`.ufo/waves/round-22/frozen/fixture-builder-v2.py` and the committed
`measure-round22.py` driver. The r40 stray `265a955` was already gone and the
three worktree-modified c10 receipts were already committed by attempt 1.
