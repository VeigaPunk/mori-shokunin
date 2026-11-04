# mori round 82 — frozen contract (C1 operability, C2 freshness, C3 depth)

Frozen before any wave seat ran. Entering revision: `ebcf2c72df203c855cfafb5223c6e22b1e12c481`
(branch `master`, lane HEAD at freeze time; every earlier round's own "entering" label is not
inherited). Lane axes: coverage 6, operability 7, depth 5, freshness 5, calibration 5,
adjacency 6. Detection and report only; no remediation.

This file is the frozen authority for the three claims. The counters, this contract and the
receipt labels are the same sentence. Nothing here is rewritten after data; a miss is an honest
stop. Frozen counters/controls commit: `.ufo/waves/round-82/` (see LOG.md round-82 section for
the hash).

## C1 — operability (7): the r81 five-survivor mutation set becomes a committed, revision-agnostic harness, and it is green at the landed bytes

Background: `.ufo/waves/round-81/w1/Mo81M01Mutants.md` reported `MUTANTS killed=7 total=12
survivors=5`; r81 killed those five with five new selftest arms but its harness lived in
`/fast/scratch/hyaku/mori-r81/l1/mut5.py` and was deleted at landing (D81-3: the receipt's own
command no longer resolves). No committed instrument can re-derive the kill at a later revision.

**P-C1 (frozen predicate).** At revision R,
`python3 -I .ufo/waves/round-82/count-c1.py R` prints
`C1=met harness=present killed=K survivors=0 total=T pristine=green` and exits 0, where:
- `harness=present` means `R:.ufo/waves/round-82/count-c1.py` exists (it is this counter);
- `T` is the mutant set re-derived at R: the mutants below whose `old` anchor occurs **exactly
  once** in the named file at R (anchors that do not occur are reported as `unanchored` and are
  not graded; the r81 report's `accept_sibling` anchor no longer exists after the r81
  implementation fix, so the frozen population is the 11 mutants below);
- `K` is the number of those mutants whose selftest run is killed: mutated copy's own
  `--selftest` exits non-zero **or** prints `fail=<n>` with n>0;
- `pristine=green` means each of the three files' unmutated `--selftest` exits 0 with `fail=0`
  before any mutant is graded.

At the entering revision `ebcf2c72` the harness does not exist: `C1=unmet harness=absent`, rc 1.

**Frozen mutant set (file · label · anchored replacement).** Anchors are literal, taken from
`.ufo/waves/round-81/w1/Mo81M01Mutants.md`:

| file | label | old → new |
|---|---|---|
| `.ufo/waves/round-80/count-c1.py` | ignore_row_disagreement | `if readings and len(set(readings)) == 1:` → `if readings:` |
| `.ufo/waves/round-80/count-c1.py` | ignore_mismatch_lines | `and not any(line.startswith("CLAIM_SWEEP_MISMATCH")` → `and not any(False and line.startswith("CLAIM_SWEEP_MISMATCH")` |
| `.ufo/waves/round-80/count-c1.py` | ignore_stale_field | `and tallies == 0 and stale == 0 and stated == live)` → `and tallies == 0 and stated == live)` |
| `.ufo/waves/round-80/count-c1.py` | ignore_sweep_exit | `met = (p.returncode == 0 and sweep_consistent` → `met = (sweep_consistent` |
| `.ufo/waves/round-80/count-c3.py` | ignore_missing | `met = not missing and not extra` → `met = not extra` |
| `.ufo/waves/round-80/count-c3.py` | ignore_extra | `met = not missing and not extra` → `met = not missing` |
| `.ufo/waves/round-80/count-c3.py` | drop_right_boundary | `(?![\w.-])` → *(empty)* |
| `.ufo/waves/round-81/count-c2.py` | pending_all_sections | `section is None or not ROUND_SECTION.match(section) or not ROW.match(line)` → `section is None or not ROW.match(line)` |
| `.ufo/waves/round-81/count-c2.py` | pending_substring | `if cell == "PENDING":` → `if "PENDING" in cell:` |
| `.ufo/waves/round-81/count-c2.py` | ignore_command_exit | `or result.returncode != 0 or stated != live:` → `or stated != live:` |
| `.ufo/waves/round-81/count-c2.py` | first_binding_only | `for binding in bindings:` → `for binding in bindings[:1]:` |

**Claim type: capability acquisition** (AXES §Capabilities). The delta this round is the harness
itself and its detector selftest — a do-nothing round prints `harness=absent`. The `killed=11`
reading is a *confirmation at current bytes* of the r81 five-survivor closure, not eleven new
kills; r81 killed them with scratch-only arms whose re-run harness was deleted at landing. The
capability row enters the SCORECARD capabilities table in the same round.

Target: `C1=met harness=present killed=11 survivors=0 total=11 pristine=green`. Kill rule: any
survivor, any unanchored mutant (the set changing silently), or a red pristine → unmet; a setup
exit (2) is never a pass. The counter's own `--selftest` (detector arms: a sensitive fixture is
killed, a blind fixture survives, a duplicated anchor is excluded, a red pristine is reported)
must be green for the claim to hold.

## C2 — freshness (5, tied lowest): the red round-10 drift pin is retired with a derived classification of every drifted token

Background: `SCORECARD.md`'s freshness cell carries "round-10 drift pin still red" since round 10.
Measured this round at the entering bytes:
`bash tools/mori-census.sh --drift corpus/evidence/baseline-r10-20261015T2231Z.json` exits 1 and
prints a `MORI_DRIFT:` line whose tokens name surfaces, findings, keys and the verdict. The r20
re-pin was rejected (SCORECARD round-21 correction: the closed-class register licensed away
retained evidence loss); the pin therefore cannot go green by re-pinning, and a permanently red
"acceptance" predicate is not a drift-detection result.

**P-C2 (frozen predicate).** At revision R,
`python3 -I .ufo/waves/round-82/count-c2.py R` prints
`C2=met tokens=N classified=N agreed=N residual=0 retired=1 cell=1` and exits 0, where:
- the census script **at R** (`git show R:tools/mori-census.sh`) is run against the baseline
  **at R** (`corpus/evidence/baseline-r10-20261015T2231Z.json`) with
  `MORI_SHOKUNIN_ROOT` = the fleet root and the run exits **1** (a green pin has nothing to
  classify and is `unmet`, not met);
- the `MORI_DRIFT:` token list is non-empty; `N` is its token count;
- `corpus/evidence/drift-classification-r82.txt` at R carries one `DRIFT_CLASS <token> <class>`
  line per token (class ∈ {`added-since-r10`, `value-changed`}; `unexplainable` is allowed and
  counts as `residual`, which keeps the claim unmet);
- `agreed` re-derives the class from the **baseline bytes at R** and requires the stated class to
  equal it. Derivation table (frozen):
  | token shape | derived class |
  |---|---|
  | `SURFACE:<name>` | `value-changed` if `<name>` is a `SURFACE <name>:` id in the baseline canonical block, else `added-since-r10` |
  | `FINDING:<NAME>` | `value-changed` if `<NAME>` is a `FINDING <NAME> severity=` id in the baseline, else `added-since-r10` |
  | `VERDICT`, `HEADER`, `BLANK` | `value-changed` |
  | `<key>`, `+<key>`, `-<key>` | `value-changed` if `<key>=` occurs in the baseline bytes, else `added-since-r10` |
  | anything else | `value-changed` |
- no `DRIFT_CLASS` line names a token absent from the live run (`stale` classifications are
  counted and keep the claim unmet);
- `retired=1` means `SCORECARD.md` at R has a `## Retired` table row whose first cell is exactly
  `drift-pin-r10` and whose row text contains `corpus/evidence/baseline-r10-20261015T2231Z.json`
  and `corpus/evidence/drift-classification-r82.txt`;
- `cell=1` means the Axes row whose first cell is `freshness` contains the literal
  `r10 pin retired` and `corpus/evidence/drift-classification-r82.txt`, and does **not** contain
  `round-10 drift pin still red`.

At the entering revision `ebcf2c72` (measured in `evidence/controls-r82.txt`):
`C2=unmet tokens=64 classified=0 agreed=0 residual=0 stale=0 retired=0 cell=0`, rc 1 (the
classification file and the retired row do not exist and the cell still carries the red literal).

Vacuity guard (frozen): the claim is not reachable by deleting the debt. The live census run is
the same command in both states and must stay **red (exit 1)**; the classification must name
every token it reports, with a class the baseline bytes independently derive; and the `## Retired`
row must carry both the baseline and the classification paths.

## C3 — depth (5, tied lowest): the record sweep gains a revision-precision arm, and the lane's revision-labelled values are graded against the bytes they name

Background: two consecutive non-author closures routed the same defect class — a record row states
a measured value and a revision, and the revision does not contain the value (D80-4, D81-1: the
r80 capability row states `pointers=240` measured at `075574c8`, where `SCORECARD.md` contains no
`pointers=240`). The r81 pinned arm compares values against a command, never against a revision
label.

**P-C3 (frozen predicate).** At revision R,
`python3 -I .ufo/waves/round-82/count-c3.py R` prints
`C3=met tool=present arms=N defeated=1 bindings=B revisions=0` and exits 0, where:
- `tool=present` means `R:tools/mori-record-sweep.py` exists and its bytes contain the new arm
  (the literal `REVISION_MISMATCH`);
- `arms=N` is `RECORD_SWEEP_SELFTEST pass=N fail=0` from the tool's own `--selftest` at R, and
  N ≥ 30 (the r81 tool had 26);
- `defeated=1` means the counter's **independent** fixture is caught: a scratch repo where
  `SCORECARD.md` states `pointers=240` and names revision A (whose `SCORECARD.md` contains
  `pointers=237`), with a pins file binding row `mori-claim-sweep.py`, key `pointers`, value 240,
  rev A, path `SCORECARD.md`; the tool run there prints `revisions=1` and exits 1;
- `bindings=B` and `revisions=0` come from the tool run over the **real lane** at the landed
  bytes with `--pins .ufo/waves/round-82/record-pins.json`, B ≥ 3, all bindings green
  (`revisions=0`), rc 0.

At the entering revision `ebcf2c72` (measured in `evidence/controls-r82.txt`):
`C3=unmet tool=present arm=absent`, rc 1 (the r81 tool exists; the `REVISION_MISMATCH` arm does
not).

**Frozen arm interface** (addition to `tools/mori-record-sweep.py`; the r81 arms and their
summary tokens stay byte-compatible):
- pins file may carry `"revisions": [{"carrier": "SCORECARD.md", "row_contains": "<text>",
  "key": "pointers", "value": 240, "rev": "<sha>", "path": "SCORECARD.md"}, ...]`;
- per binding, in order: the carrier's **first** table row containing `row_contains` must state
  `key=value` (else `REVISION_MISMATCH <carrier>:<line> row-value`); `rev` must resolve to a
  commit (else `rev-unresolvable`); `path` must exist at `rev` (else `path-absent`); and
  `key=value` must occur in `path`'s bytes at `rev` (else `REVISION_MISMATCH <carrier>:<line>
  rev-bytes`). Every binding is graded — never the first only — and a missing row is a mismatch.
- git reads use `--git DIR` (default `--root`); the summary line gains `revisions=<count>`.
- the tool's `--selftest` gains arms for: conformant binding, the D81-1 defeated shape
  (value not in the rev's bytes), unresolvable rev, path absent at rev, missing row, and a
  two-binding list where the second is stale.

Real bindings (frozen population; each verified at the freeze):
| carrier | row_contains | key | value | rev | path |
|---|---|---|---|---|---|
| SCORECARD.md | `mori-claim-sweep.py` | pointers | 240 | `482dc48d` | SCORECARD.md |
| SCORECARD.md | `mori-record-sweep.py` | pass | 26 | `142998f5` | SCORECARD.md |
| SCORECARD.md | `Control-receipt binding guard` | pass | 19 | `142998f5` | SCORECARD.md |

## Do-nothing controls (frozen; committed in `evidence/controls-r82.txt`)

A round that does nothing leaves all three red, and each counter was run at `ebcf2c72` before any
wave seat existed:
- C1: `C1=unmet harness=absent` (no committed harness; the r81 harness was scratch-only).
- C2: `C2=unmet tokens=64 classified=0 agreed=0 residual=0 stale=0 retired=0 cell=0` (the pin
  is red and nothing classifies it; the cell still carries the red literal).
- C3: `C3=unmet tool=present arm=absent` (the r81 tool exists; the revision arm does not).

Cheapest cheats and their expected failure, checked by the critic seat: a stub counter that
always prints `met` (the counters are the graded objects, and each counter is graded by its own
revision-agnostic bytes and independent fixture); deleting the red cell literal without the
retired row or the classification (cell=1 requires the retired row and the file, and the live
census must stay red); a classification that labels every token `added-since-r10` (the derivation
table disagrees on every baseline-present token); a pins file with one binding (B ≥ 3).

## Wave shape

ONE v1 wave, 14 seats, band 8–16 (`scripts/hyaku/ufo-wave-policy.json`, `maxLanes` 256 hard
ceiling), ≥25 % attack seats: 4 attack (reviewer, critic, mutation-tester, labrat) = 28.6 %,
1 connector, 5 executor, 2 scribe, 2 scout. Residual: none. The planner seat is the L1
(the validator rejects `planner`).

## Pre-data amendment A1 (disclosed; made after the freeze commit `20551e56`, before any after-value existed)

The "Real bindings" table's first row is replaced. Reason: the r80 capability row
(`SCORECARD.md:4038` at the freeze) states the claim-sweep `pointers=` count that the r81
**pinned** arm grades against the live command; r81's D80-2 maintenance rule requires that cell
to state the landed value, so the row's number moves whenever the lane's record grows. Binding a
revision to it would make P-C3 fight the r81 pinned arm at landing. The replacement population
uses three historical claim-table rows whose values are frozen history (round-80 and round-81
tables; corrections are appended, never rewritten). P-C3's predicate, kill rule and target are
unchanged: B ≥ 3, all green, `revisions=0`.

| carrier | row_contains | key | value | rev | path |
|---|---|---|---|---|---|
| SCORECARD.md | `row_tally=19` | row_tally | 19 | `075574c83eae` | SCORECARD.md |
| SCORECARD.md | `survivors=0` | survivors | 0 | `075574c83eae` | SCORECARD.md |
| SCORECARD.md | `wrong=0 fixtures=7` | wrong | 0 | `482dc48d` | SCORECARD.md |

Each of the three `row_contains` strings matches exactly one table row in `SCORECARD.md` at the
freeze (measured: 1, 1, 1), and each `key=value` occurs in `SCORECARD.md` at the named revision
(measured: 1, 1, 1). The D81-1 defeated shape — the row stating `pointers=240` bound to
`075574c8`, whose `SCORECARD.md` holds no `pointers=240` — stays the counter's independent
fixture and is not a lane binding.
