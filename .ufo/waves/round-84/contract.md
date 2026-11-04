# mori round 84 — frozen contract

Round 84 (attempt 1), lane `mori`, date 2026-11-04. Entering revision
`5adf4337b6510dd246b247092c11cbaa97c930d3` (branch `master`, r83 verifier spot-check commit).
Axes: **operability** (C1, score 7), **calibration** (C2, score 5, tied lowest) and **depth**
(C3, score 5, tied lowest). This file freezes the three predicates, their populations, kill rules,
targets and do-nothing controls **before any after-value exists**. Nothing below is narrowed after
data; a miss is an honest stop.

The three claims come from `SCORECARD.md` `## Planned (round 84)`. Each is causally separable: the
C1 counter grades only the r83 counter family, the C2 counter only `tools/mori-record-sweep.py`,
the C3 counter only `.ufo/waves/round-83/count-c2.py`; each counter reads its own subject's bytes
at the graded revision and no other claim's landed bytes.

## P-C1 — operability: the r83 counter family's four extra mutants

Frozen predicate sentence:

> At revision R `python3 -I .ufo/waves/round-84/count-c1.py R` prints
> `C1=met mutants=4 killed=K equivalent=E survivors=0 total=4 pristine=green detector=green`
> and exits 0, where the four-mutant table below is re-derived from R's own bytes (each `old`
> anchor occurs exactly once in the named file at R), every mutated copy's own `--selftest` is run
> in scratch and reads killed, a surviving mutant with a registered equivalence counts
> `equivalent` only while every coupling marker of that equivalence occurs exactly once in the
> graded file, the pristine files' own `--selftest` runs are green first, and the counter's own
> detector selftest passes in the same invocation.

Kill rule (frozen): a mutant is killed iff its mutated copy's own `--selftest` exits non-zero **or**
prints `fail=<n>` with n > 0, conditional on the pristine copy being green. Green means rc 0, the
token `fail=0` present, and no `fail=<n>` with n > 0. An anchor that does not occur exactly once is
reported `unanchored` and never counted killed; an empty mutation is `empty-mutation`; a red
pristine, an unanchored anchor, an empty mutation, a missing equivalence coupling or a red detector
keeps the claim unmet. Exit 2 is setup, never a pass.

The four-mutant population (measured by the r83 C1 reviewer at `c4845c83`,
`.ufo/waves/round-83/w1/Mo83R01C1.md` §6 — "extra-mutant sweep", M24a–M24d):

| file | label | old | new | class |
|---|---|---|---|---|
| `.ufo/waves/round-83/count-c1.py` | `M24a_killed_tally` | `killed_n = total - survivors - equivalent` | `killed_n = total - equivalent` | non-equivalent survivor: over-reports `killed=` whenever survivors > 0 |
| `.ufo/waves/round-83/count-c1.py` | `M24b_green_fail_token` | `return rc == 0 and "fail=0" in out and not FAIL.search(out)` | `return rc == 0 and not FAIL.search(out)` | non-equivalent survivor: a rc-0 pristine with no `fail=0` token reads green |
| `.ufo/waves/round-83/count-c2.py` | `M24c_met_unclassified` | `and not unclassified and residual == 0` | `and residual == 0` | equivalent (coupling proof below) |
| `.ufo/waves/round-83/count-c2.py` | `M24d_met_residual` | `and not unclassified and residual == 0` | `and not unclassified` | equivalent (coupling proof below) |

Registered equivalences (A1-style adjudication; the coupling marker is the proof, and it must occur
exactly once in the graded file or the mutant reads `survived`):

| label | coupling markers (each exactly once) | why the dropped clause cannot be observed |
|---|---|---|
| `M24c_met_unclassified` | `agreed == len(snapshot_tokens)` | every unclassified token is absent from `stated`, so it can never be counted `agreed`; `agreed == len(snapshot_tokens)` therefore already implies `unclassified` empty |
| `M24d_met_residual` | `agreed == len(snapshot_tokens)`, `residual += duplicates`, `duplicates == 0` | a stated `unexplainable` class is never equal to `derive(...)`, so it blocks `agreed == len(...)`; duplicate classes are absorbed by `residual += duplicates` while `met` separately requires `duplicates == 0` |

Target: `C1=met mutants=4 killed=2 equivalent=2 survivors=0 total=4 pristine=green detector=green`
rc 0 at the after revision. Entering control (frozen): `C1=unmet harness=absent` rc 1 at
`5adf4337`. Population control at the freeze commit: the same command prints `C1=unmet
mutants=4 killed=0 equivalent=2 survivors=2 ...` rc 1 — the equivalence map is frozen, the two
arms are not yet landed.

Seat that lands the arms: `.ufo/waves/round-83/count-c1.py` `selfcheck()` only (+2 arms):
1. `blind_case_tally` — a fixture with one killed and one surviving mutant must print
   `killed=0 survivors=1` (the `M24a` kill).
2. `green_requires_fail_zero` — a pristine whose selftest exits 0 and prints `SELFTEST skipped`
   (no `fail=0` token) must read `pristine=red`, so the run is unmet (the `M24b` kill).
The r83 counter's `grade()`/`green()`/`killed()` bodies are not edited; both `old` anchors above
must still occur exactly once at the after revision.

## P-C2 — calibration: the revision arm grades every anchor row

Frozen predicate sentence:

> At revision R `python3 -I .ufo/waves/round-84/count-c2.py R` prints
> `C2=met arm=all-rows defeated=2 fixtures=3/3 bindings=3 revisions=0 arms=44` and exits 0, where
> the tool at R carries the `ALL_ANCHOR_ROWS` rule, two frozen ambiguous fixtures read red under
> the R tool and green under the entering tool (`5adf4337`), the conformant fixture reads green
> under both, the real lane run with the r82 pins prints `revisions=0` rc 0 over exactly the three
> frozen bindings, and the tool's own selftest prints `RECORD_SWEEP_SELFTEST pass=N fail=0` with
> N ≥ 44.

Rule (frozen): a revision binding's `row_contains` selects **every** row carrying that string. The
carrier side requires each selected row to state `key=value` on that row (the first failing row is
`REVISION_MISMATCH <carrier>:<line> row-value`); the revision side requires each row carrying the
anchor in `git show <rev>:<path>` to carry the token (`REVISION_MISMATCH <carrier>:<line>
rev-bytes`). A binding whose anchor selects no row is `row-value` at line 1; a blob with no anchor
row is `rev-bytes`. This replaces the first-match selection that QUALITY 169 names as not covered.

Frozen fixtures (built in scratch, each in its own fixture git repo with
`git -C "$D" rev-parse --show-toplevel` asserted equal to `$D`):

| fixture | carrier (worktree) | blob at rev A | old tool | R tool |
|---|---|---|---|---|
| `carrier-ambiguous` | `\| Row A \| x \| row_tally=19 \| 80 \|` and `\| Row A extended \| y \| row_tally=18 \| 80 \|` | same two rows | green (first match row 1) | red `row-value` at row 2 |
| `rev-ambiguous` | `\| Row A \| x \| row_tally=19 \| 80 \|` | the two rows above | green (anchored occurrence on row 1) | red `rev-bytes` at row 2 |
| `conformant` | `\| Row A \| x \| row_tally=19 \| 80 \|` | same row | green | green |

Binding for all three: `{"carrier":"SCORECARD.md","row_contains":"Row A","key":"row_tally",
"value":19,"rev":"<rev A>","path":"SCORECARD.md"}`.

Real bindings (frozen population, `.ufo/waves/round-82/record-pins.json`, exactly three):
`row_tally=19` at `075574c8`, `survivors=0` at `075574c8`, `wrong=0 fixtures=7` at `482dc48d`.
At each named revision the anchor selects exactly one row, so the all-rows rule keeps them green;
at the after revision `survivors=0` selects five rows and every one states `survivors=0`.

Seat: `tools/mori-record-sweep.py` only — the all-rows selection on both sides, the marker
`ALL_ANCHOR_ROWS`, and exactly four new selftest arms (`carrier-all-anchor-rows-green`,
`carrier-all-anchor-rows-red`, `rev-all-anchor-rows-green`, `rev-all-anchor-rows-red`), taking the
tally 40 → 44. The existing 40 arms must keep passing unchanged.

## P-C3 — depth: the live reading becomes a per-token delta classification

Frozen predicate sentence:

> At revision R `python3 -I .ufo/waves/round-84/count-c3.py R` prints a `C3=met` summary carrying
> `delta=classified tokens=64`, `classified=` equal to `union=` (the union of the snapshot token
> line and the live run's token line), `residual=0` and `live=derived`, and exits 0, where the
> r83 counter at R carries the `LIVE_DELTA` classifier, its selftest prints PASS for the four
> delta arms (`delta_absent_live`, `delta_added_live`, `delta_class_changed`, `delta_agreed`) with
> at least 16 arms, and its live run prints exactly one `LIVE_DELTA <token> <class>` line for
> every union token that is not `agreed`.

Classes (frozen): `absent-live` (in the snapshot, not in the live token line), `added-live` (live
only), `class-changed:<snapshot>-><live>` (in both, the snapshot's stated class differs from the
class derived from the live baseline names), `agreed` (in both, classes equal). The live census
reading stays an observation: `met` never requires a particular token count, only that every token
in the union is classified exactly once and that `agreed` equals the counter's `live_agree`.

Seat: `.ufo/waves/round-83/count-c2.py` only — the classifier, the `LIVE_DELTA` lines, the tail
fields `classified=`/`union=`/`absent_live=`/`added_live=`/`class_changed=` and the four selftest
arms. The substrings `and not unclassified and residual == 0`, `agreed == len(snapshot_tokens)`,
`residual += duplicates` and `duplicates == 0` must each still occur exactly once (P-C1's
equivalence proofs ride them), and no new selftest arm may construct a case where `residual` or
`unclassified` is non-zero while every other `met` conjunct holds.

## Measurement protocol

1. The counters are run at the entering revision (do-nothing controls) and at the freeze commit
   before any seat writes; both receipts are committed under `.ufo/waves/round-84/evidence/`.
2. After the wave settles and the L1 integrates, the same three commands are run at the
   integration revision and pasted into `.ufo/waves/round-84/evidence/after-r84.txt`; the record
   (SCORECARD, LOG) cites that revision.
3. A counter that prints `C1=unmet`/`C2=unmet`/`C3=unmet` at the integration revision is an honest
   stop for that claim; the report states it and no target is narrowed.

## Pre-data amendment A1 — fixture finding line numbers (no predicate, rule or target change)

Filed 2026-11-04 after the L1 prototyped the all-rows rule in scratch against the entering tool and
the 40 existing selftest arms; no after-value existed and no seat had scored anything.

The P-C2 fixture table above said `rev-ambiguous` reads red "at row 2". That line number is wrong
for the tool's existing convention: a revision finding reports the **carrier-side** row the binding
anchors (`revision_sweep`'s `number`), which for `rev-ambiguous` is row 1 (the carrier holds one
`Row A` row), while `carrier-ambiguous` reports row 2 (the first carrier row failing the token). The
graded words are the detail (`row-value` / `rev-bytes`) and `revisions>=1`, not the number, so no
predicate or target changes. The existing arm `revision-second-stale` pins the convention: a
binding whose carrier row is line 2 and whose blob has no anchor row must report
`('revision', 'SCORECARD.md', 2, 'rev-bytes')` — the carrier row's line, never 1. E02's spec is
unchanged; the seat meets this through that arm.

The L1's scratch prototype (not landed, not evidence) also confirmed two facts the contract relies
on: with the rule applied the tool's own 40 arms stay `RECORD_SWEEP_SELFTEST pass=40 fail=0`, and
the real lane run with the r82 pins reads `RECORD_SWEEP pending=0 pinned=0 carriers=1 bindings=3
revisions=0`, rc 0.

## Pre-data amendment A2 — the M24b/M24c/M24d anchors corrected (no predicate, target or kill-rule change)

Filed 2026-11-04 after the L1 ran the frozen counter's population control at the freeze commit
`daa77bd5`; no after-value existed, no seat had landed an arm, and no seat had scored anything.
Found independently by seat `Mo84S02Quality` (its report names the same three anchors) and by the
L1's own run.

The M24 table above took the r83 reviewer's anchor strings as quoted prose
(`.ufo/waves/round-83/w1/Mo83R01C1.md` §6). Measured against the graded bytes, three do not occur
exactly once — the frozen rule "each `old` anchor occurs exactly once at R" therefore read
`unanchored` and the population control printed `mutants=1 killed=0 equivalent=0 survivors=1`
instead of the declared `mutants=4 killed=0 equivalent=2 survivors=2`:

| label | defect in the quoted anchor | measured |
|---|---|---|
| `M24b_green_fail_token` | `return rc == 0 and "fail=0" in out and not FAIL.search(out)` occurs twice: `green()`'s body (line 129) and the r83 counter's own MUTANTS table literal (line 33) | 2 occurrences |
| `M24c_met_unclassified` | `and not unclassified and residual == 0` occurs zero times: the `met` expression wraps, `and not unclassified` ends line 241 and `and residual == 0` starts line 242 | 0 occurrences |
| `M24d_met_residual` | same anchor as M24c | 0 occurrences |

Replacement anchors (each measured exactly once at `daa77bd5` and at the entering revision
`5adf4337`; the L1's count command is `python3 -c "s=open(P).read(); print(s.count(A))"` over
`git show <rev>:<path>`):

| label | file | old | new |
|---|---|---|---|
| `M24a_killed_tally` | `.ufo/waves/round-83/count-c1.py` | `killed_n = total - survivors - equivalent` | `killed_n = total - equivalent` |
| `M24b_green_fail_token` | `.ufo/waves/round-83/count-c1.py` | `    return rc == 0 and "fail=0" in out and not FAIL.search(out)` (four-space indent, unique) | `    return rc == 0 and not FAIL.search(out)` |
| `M24c_met_unclassified` | `.ufo/waves/round-83/count-c2.py` | `and not unclassified` | *(empty — the conjunct is deleted; the parenthesised `met` expression stays valid)* |
| `M24d_met_residual` | `.ufo/waves/round-83/count-c2.py` | `and residual == 0` | *(empty)* |

The mutants are the same edits the reviewer described; only their anchor strings change. The
equivalence map, coupling markers, kill rule, target and controls are byte-unchanged. E01's two
arms still kill M24a/M24b; E03's preservation obligation becomes: `and not unclassified`,
`and residual == 0`, `agreed == len(snapshot_tokens)`, `residual += duplicates` and
`duplicates == 0` each occur exactly once at the after revision (the two conjuncts may be wrapped,
but not merged into one line and not deleted).

## Pre-data amendment A3 — wording clarification: `tokens=64` is the snapshot count (no predicate change)

Filed 2026-11-04 from seat `Mo84S02Quality`'s recorded finding 2 (its report §4.2); no after-value
existed and no arm had landed.

P-C3's sentence "the live census reading stays an observation: `met` never requires a particular
token count" is about the **live** reading (`live_tokens=`), not about `tokens=`. `tokens=64` is
the snapshot's own token-line count — fixed by the committed snapshot
`.ufo/waves/round-82/evidence/drift-r82-live.txt`, already required by the r83 counter's existing
conjuncts — and the frozen target line carries it (`delta=classified tokens=64`). The r84 C3
counter's `tokens == 64` check therefore enforces the snapshot population, never a live count; the
live side is graded only by `classified == union`, `deltas == union - live_agree` and
`live=derived`. No predicate, target, class or counter byte changes.

## Pre-data amendment A4 — the `blind_case_tally` assertion corrected (no predicate or target change)

Filed 2026-11-04 from seat `Mo84Sc02Clauses`'s measured finding D3; no arm had landed at the time
of writing and no after-value existed.

P-C1's seat paragraph said the `blind_case_tally` arm's fixture ("one killed and one surviving
mutant") "must print `killed=0 survivors=1`". That sentence is arithmetically wrong: one killed
mutant makes `killed=1`, and an arm asserting `killed=0` on that fixture goes red on the *pristine*
counter (the seat measured `pass=7 fail=1`). The arm's correct assertion, and the one E01's item
prompt already carries, is `killed=1 survivors=1 total=2` and `not met`; under the M24a mutant
(`killed_n = total - equivalent`) the same fixture prints `killed=2`, so the arm fails and the
mutant is killed. The E01 prompt is the operative text and is unchanged.

Clarification of the population control's bytes (Sc02 finding D1): the control is the **worktree**
counter (the amended `count-c1.py` at HEAD) grading the freeze revision's r83 bytes —
`python3 -I .ufo/waves/round-84/count-c1.py daa77bd5` → `C1=unmet mutants=4 killed=0 equivalent=2
survivors=2 total=4 pristine=green detector=green` rc 1. The counter bytes committed *at*
`daa77bd5` are the pre-A2 version and are superseded by A2; no reader should run that copy as the
control.

## Pre-data amendment A5 — C1's counter binds the arms and the 2/2 split (critic control defeated)

Filed 2026-11-04 from seat `Mo84C01Crit` §1.1/§1.2, before any after-value and before either arm
landed. The critic's cheapest do-nothing control — the r83 counter with a sha256 self-tripwire in
`selfcheck()` and **no** arms — killed all four mutants and printed the exact target line
(`C1=met mutants=4 killed=2 equivalent=2 survivors=0 total=4 pristine=green detector=green`, rc 0),
and a two-tripwire variant printed `killed=4 equivalent=0` while `met` still read true.

Fix (counter bytes, no predicate/target change): `main` now also requires
(a) the graded subject `.ufo/waves/round-83/count-c1.py` to carry both arm labels
(`blind_case_tally`, `green_requires_fail_zero`) — `C1=unmet subject=absent-arms` otherwise — and
(b) the printed split to be exactly `killed=2 equivalent=2 total=4` — `C1=unmet target=split`
otherwise. The population control at the freeze commit still prints
`C1=unmet mutants=4 killed=0 equivalent=2 survivors=2` because the grade runs before the new gates.
The counter's own detector selftest grew 11 → 15 arms (`target_split_ok`, `target_split_free`,
`subject_markers_ok`, `subject_markers_missing`).
Residual, named: a subject that carries the two labels as dead strings and kills via a tripwire
still passes; full kill attribution needs mutation-grading of the arms themselves, which is the
next round's C1-class work.

## Pre-data amendment A6 — C3's counter imports and grades the classifier (null-classifier control defeated)

Filed 2026-11-04 from seat `Mo84C01Crit` §1.4, before any after-value. The critic's stub — markers
present as assignments, four PASS-only delta labels, and a tail claiming `union=64 live_agree=64
deltas=0` with **zero** `LIVE_DELTA` lines — printed `C3=met ...` rc 0: the counter trusted the
subject's own arithmetic.

Fix (counter bytes, no predicate/target change): the counter now
(a) requires the subject's bytes to carry all four delta arm labels,
(b) imports the extracted subject and grades its own pure `live_delta(snapshot_tokens, live_tokens,
names, stated)` on five frozen synthetic cases (absent-live, added-live, agreed,
class-changed:<a>-><b>, duplicate-token collapse), requiring exact ordered output — a stub without
a working classifier fails,
(c) recounts the snapshot population from the repo's own
`.ufo/waves/round-82/evidence/drift-r82-live.txt` at R and requires `tokens == recount`.
The counter's own selftest grew 9 → 11 arms (`snapshot_parse`, `case_expectations`).
Residual, named: the live token list remains the subject's own printed observation (the census is
volatile, so the counter does not re-run it); a subject that fabricates a self-consistent live
reading is outside this counter's discrimination — that is the next round's mutation-grading class.

## Pre-data amendment A7 — separability wording, C3 import hardening, defeated-control receipts

Filed 2026-11-04 from seat `Mo84C01Crit` §2/§4, before any after-value.

**Separability wording corrected.** The preamble's sentence "each counter reads its own subject's
bytes at the graded revision and no other claim's landed bytes" is false for C1: its population
contains two mutants of `.ufo/waves/round-83/count-c2.py`, the file C3 edits. The operative
statement is: **C1 is verifiable at a revision where C3 has not landed** (its anchors exist at the
freeze and after A2), and when both land the preservation clause — `and not unclassified`,
`and residual == 0`, `agreed == len(snapshot_tokens)`, `residual += duplicates`,
`duplicates == 0`, each exactly once — keeps the anchors; the after-value is measured at the
integrated revision where both hold. C3 is verifiable without C1's arms (the classifier import and
the tail are independent of them), and C2 reads only `tools/mori-record-sweep.py` and the r82 pins.
The claim is separability, not byte-disjointness.

**C3 import hardened.** A subject that calls `sys.exit()` at import time (the critic's stub shape)
escaped the `except Exception` and its stdout leaked into the counter's receipt; the import now
runs under `contextlib.redirect_stdout` and catches `(Exception, SystemExit)` →
`C3=unmet delta=absent import-failed:<type>`. Counter selftest unchanged at 11 arms.

**Defeated-control receipts committed.** `.ufo/waves/round-84/evidence/controls-r84-defeated.txt`
records, at worktree counter bytes: the freeze population control; the A5 tripwire control
(pristine green, all count-c1 mutants killed, target split printed) defeated as
`C1=unmet subject=absent-arms`; the A6 stub control defeated as
`C3=unmet ... import-failed:SystemExit`; and a null classifier defeated as
`C3=unmet ... selftest=red`. The corrected population-control receipt sits beside the three
entering controls as the critic asked.

## Pre-data amendment A8 — supersede pointers and the per-fixture mismatch kind (critic/reviewer F1–F5)

Filed 2026-11-04 from seat `Mo84R03Record` §1 (F1–F5), before any after-value.

- **F1/F3 (supersede pointers).** The P-C1 four-mutant table at the top of this file quotes the
  r83 reviewer's prose anchors; **it is superseded by A2**, which carries the operative anchors
  (M24b four-space-indented, M24c `and not unclassified`, M24d `and residual == 0`) and the
  measurement that each occurs exactly once. F3's "both `old` anchors" is likewise superseded:
  there are four, two per graded file. No frozen byte above is rewritten.
- **F2** is fixed by A4 (the `blind_case_tally` assertion is `killed=1 survivors=1 total=2`).
- **F4 (split not bound).** Already fixed by A5: `main` now requires the printed split
  `killed=2 equivalent=2 total=4`, not `survivors == 0` alone; a `killed=3 equivalent=1` run reads
  `C1=unmet target=split`. The record must still cite the literal target line, not rc 0 alone.
- **F5 (per-fixture kind).** The C2 counter now requires `carrier-ambiguous` → `row-value` and
  `rev-ambiguous` → `rev-bytes` (previously either token satisfied either fixture). Named limit,
  unchanged from A1: the finding's line number is not bound (the fixture's HEAD line numbering is
  an implementation detail); the graded words are the detail and `revisions>=1`. `arms` stays a
  floor (`>= 44`), not an exact equality: the target names 44 and the tool lands exactly 44, but a
  later arm addition must not make the claim unverifiable.

## Pre-data amendment A9 — P-C3's preservation list superseded by A7 (prose only)

Filed 2026-11-04 from seat `Mo84R01C1` §3 residual (a), before any after-value. P-C3's seat
paragraph still lists the pre-A2 string `and not unclassified and residual == 0` as the
must-occur-once item; that single-line substring occurs zero times in the graded bytes. **The
operative list is A7's**: `and not unclassified`, `and residual == 0`,
`agreed == len(snapshot_tokens)`, `residual += duplicates`, `duplicates == 0`, each exactly once.
No counter enforces the stale sentence and no predicate, target or class changes. Residual (b):
`SCORECARD.md` `## Planned (round 84)` item 1 repeats the r83 reviewer's shorthand for M24a
(`killed_n = total - survivors` → `total`); the operative anchor is A2's
(`killed_n = total - survivors - equivalent` → `killed_n = total - equivalent`). The plan row is
a historical plan, not a claim, and is not rewritten.
