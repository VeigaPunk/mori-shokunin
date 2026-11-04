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
