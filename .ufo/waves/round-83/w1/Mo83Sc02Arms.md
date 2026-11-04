# Mo83Sc02Arms — arm map and collision scan for the 20 C1 survivors

Seat: Mo83Sc02Arms (scout, round 83 w1, attempt 1). Read-only reconnaissance: **no lane file
was edited**, no commit, no mutating git/jj command (fixture repos live in my scratch only and
each asserted `git rev-parse --show-toplevel` == the fixture dir before the first commit). No
subagent. No tool installed or upgraded. Scratch `/fast/scratch/hyaku/mori-r83/Mo83Sc02Arms`
(and `/fast/scratch/hyaku/mori-r83/Mo83Sc02Arms/runs`) deleted before this report was written.

**Headline: every one of the 20 survivors has a verified failing arm — but one of them
(`duplicates_accepted`) is a *mathematically equivalent* mutant and cannot be killed by any arm
while the current non-anchor accounting line stands. That is a blocker for the frozen
`killed=23` target, with a behaviour-preserving one-line repair shown below.**

Method: I reconstructed the round-83 counter's grading loop in scratch over the *current* r82
counter bytes, added candidate arms to scratch copies, and ran every one of the 23 frozen mutants'
own `--selftest` against the patched copies. A route counts as a kill only if the patched
*pristine* selftest is green and the mutated copy exits non-zero or prints `fail>0` — the frozen
detector. All figures below were produced by execution, not inspection.

## 1. Bytes measured

| file | sha256 at worktree HEAD `466d28bc` | sha256 at freeze `9075c729` |
|---|---|---|
| `.ufo/waves/round-82/count-c1.py` (299 lines) | `c4876c1b867d3eaa13fbaa2933b3740504b4307a851839ff7b782c7d5652576f` | same |
| `.ufo/waves/round-82/count-c2.py` (317 lines) | `e73d919eccd1475c8915072cdfbddd02e4dfef1e25bd574958b7d5c1776282be` | same |
| `.ufo/waves/round-82/count-c3.py` (308 lines) | `aa56ba485ab6918a3cf91aad7022c9a16730144cb7d9ebd9d7e5e6c9e55dbc7c` | same |

`git diff --stat 9075c729 466d28bc -- .ufo/waves/round-82 .ufo/waves/round-83 tools/mori-record-sweep.py`
shows only the round-83 wave spec/dispatch added at `466d28bc`; no graded byte moved. The three
files read here are therefore the freeze bytes, and every line number below is stable across the
freeze.

Freshness at write time: `count-c2.py` and `count-c3.py` are still the freeze bytes; the c1
executor is already editing `.ufo/waves/round-82/count-c1.py` (worktree sha
`0922bf02282e0f91b677dd516a0d9b60579a74fe94acbe9d2b277abb5e81f094`). I re-scanned that in-flight
file: all seven c1 anchors still occur exactly once, so no anchor has been duplicated or lost so
far. **All `count-c1.py` line numbers in this report refer to the freeze/HEAD bytes
(`c4876c1b…`); after the executor's insertions they shift down** — match by anchor text, not by
line.

Entering control reproduced at the worktree tip (not read from the receipt):

```text
$ HYAKU_SCRATCH=/fast/…/runs python3 -I .ufo/waves/round-83/count-c1.py 466d28bc
… 20 × "MUTANT … survived rc=0" …
C1=unmet mutants=23 killed=3 survivors=20 total=23 pristine=green detector=green rev=466d28bc229f
rc=1
```

So: 3 already killed (`unanchored_still_graded`, `stale_accepted`, `derive_key_eol_only`),
20 survivors, matching `evidence/controls-r83.txt` exactly.

### Anchor multiplicity (the frozen anchor-integrity rule)

Every one of the 23 `old` anchors occurs **exactly once** in its named file at HEAD and at the
freeze (identical hashes), measured by the round-83 counter's own table applied to the current
bytes:

```text
count-c1.py  green_ignores_fail_token 1 · killed_ignores_rc 1 · ignore_pristine_red 1 ·
             accept_empty_population 1 · unanchored_excused 1 · detector_gate_dropped 1 ·
             unanchored_still_graded 1
count-c2.py  stale_accepted 1 · duplicates_accepted 1 · retired_paths_unchecked 1 ·
             red_literal_unchecked 1 · green_census_tokens_accepted 1 ·
             finding_branch_inverted 1 · malformed_not_residual 1 · keyshape_guard_inverted 1 ·
             derive_key_eol_only 1
count-c3.py  population_gate_dropped 1 · defeated_accepted 1 · carrier_drift_allowed 1 ·
             bindings_floor_dropped 1 · selftest_red_accepted 1 · revisions_default_zero 1 ·
             summary_first_line 1
```

No anchor occurs more or fewer than once. Two contract-table cells differ from the code only in
markdown presentation, not content: `derive_key_eol_only` writes the pipe as `\|`
(`contract.md:70`) and `defeated_accepted` writes the two-line anchor as `` … \` + newline +
`            and "REVISION_MISMATCH" in out `` (`contract.md:73`); normalised, both equal the
counter's `MUTANTS` entry. The authority and the operational table agree.

## 2. Arm map — the 20 survivors

`reach`: **in-mem** = the arm can be a `cases.append` in `selfcheck` calling an existing function;
**main-path** = the mutated code only runs in `main()`, so the arm must drive `main()` (or a
deliberately extracted pure gate). Line numbers are `old`-anchor lines in the current bytes;
function ranges are from `ast`.

| # | label | file:line (expr) | function (range) | reach | exact killing assertion (false under the mutant) | closest existing arm that misses it |
|---|---|---|---|---|---|---|
| 1 | `green_ignores_fail_token` | `count-c1.py:100` | `green` (99–100) | in-mem | a graded pristine whose selftest exits **0** and prints both `fail=2` and `fail=0` ⇒ `(not met) and "pristine=red" in tail` | `red_pristine_reported` :222 — its fixture exits 1, so `rc == 0` alone already reddens it |
| 2 | `killed_ignores_rc` | `count-c1.py:104` | `killed` (103–104) | in-mem | a non-empty mutant whose selftest exits **1** printing no `fail=<n>` ⇒ `met and "killed=1" in tail` | `sensitive_killed` :202 — its mutant exits 1 *and* prints `fail=1` |
| 3 | `ignore_pristine_red` | `count-c1.py:171` | `grade` (107–175) | in-mem | red pristine **plus** one non-empty killed mutant (`total=1`, `survivors=0`) ⇒ `(not met) and "pristine=red" in tail` | `red_pristine_reported` :222 — its mutant set is `pass=0→pass=0`, i.e. empty-mutation, `total=0` |
| 4 | `accept_empty_population` | `count-c1.py:171` | `grade` (107–175) | in-mem | `grade(loader, scratch, [])` ⇒ `(not met) and "total=0" in tail and "pristine=green" in tail` | `duplicate_anchor_excluded` :216 — asserts `total=0` but never `not met`; and its `unanchored` extra masks the gate anyway |
| 5 | `unanchored_excused` | `count-c1.py:172` | `grade` (107–175) | in-mem | one duplicated anchor (unanchored, not graded) **plus** one unique anchor that is killed (`total=1`, `survivors=0`) ⇒ `(not met) and "unanchored" in extras` | `duplicate_anchor_excluded` :216 — same extras, but `total=0`, so the `total > 0` clause also blocks `met` |
| 6 | `detector_gate_dropped` | `count-c1.py:293` | `main` (231–295) | **main-path only** | (a) lift the gate to `def counter_ok(met, own_ok)` containing the anchor verbatim and have `main` call it, then assert `counter_ok(True, False) == 1 and counter_ok(False, True) == 1 and counter_ok(True, True) == 0`; or (b) the spec's copy arm (see §6, recursion hazard) | none — `detector=green` is printed only in `main()`; the 4 selfcheck arms never touch `own_ok` |
| 7 | `duplicates_accepted` | `count-c2.py:168` | `grade` (131–189) | in-mem **only after the accounting split** | a duplicated `DRIFT_CLASS` line ⇒ `(not met) and "residual=1" in tail` — **provided** `count-c2.py:167` reads `residual - duplicates == 0` instead of `residual == 0`; without that, no assertion can distinguish it (§3) | none — `conformant` :236 has no duplicate fixture, and any duplicate fixture is already unmet through `residual += duplicates` (:166) |
| 8 | `retired_paths_unchecked` | `count-c2.py:110` | `retired_ok` (107–111) | in-mem | `## Retired` row `drift-pin-r10` naming the baseline **but not** `CLASSES` ⇒ `(not met) and "retired=0" in tail` | `retired_row_required` :257 — deletes the whole row, so the mutant still returns `False` |
| 9 | `red_literal_unchecked` | `count-c2.py:118` | `cell_state` (114–119) | in-mem | freshness cell carrying `r10 pin retired` **and** `CLASSES` **and** `round-10 drift pin still red` ⇒ `(not met) and "cell=0" in tail` | `red_cell_keeps_unmet` :252 — replaces `r10 pin retired`, so the first conjunct fails and the red literal is never consulted |
| 10 | `green_census_tokens_accepted` | `count-c2.py:167` | `grade` (131–189) | in-mem | census stub exits **0** while printing the 4-token `MORI_DRIFT:` list ⇒ `(not met) and "tokens=4" in tail` | `green_pin_is_unmet` :259 — its rc-0 stub prints `MORI_DRIFT: none`, so `bool(tokens)` is already false |
| 11 | `finding_branch_inverted` | `count-c2.py:71` | `derive` (65–76) | in-mem | token `+FINDING:OOM_KILL_JOURNAL`, baseline holding `FINDING OOM_KILL_JOURNAL` ⇒ `met and "agreed=1" in tail` | `conformant` :236 — the shared stub has no FINDING token, so the branch is never entered |
| 12 | `malformed_not_residual` | `count-c2.py:171` | `grade` (131–189) | in-mem (tail-only) | 4 good tokens + one malformed `DRIFT_CLASS` line ⇒ `(not met) and "residual=1" in tail` | `residual_keeps_unmet` :246 — uses `unexplainable`, never `malformed`; `met` is blocked by `malformed == 0` under both copies, so only the tail discriminates |
| 13 | `keyshape_guard_inverted` | `count-c2.py:75` | `derive` (65–76) | in-mem | token `lane.mori` (fails `KEYSHAPE`, not a baseline key) ⇒ `met and "agreed=1" in tail` | `conformant` :236 — every fixture token passes `KEYSHAPE` |
| 14 | `population_gate_dropped` | `count-c3.py:264` | `main` (204–304) | main-path | fixture repo: 3 bindings that are **not** the frozen population but are all resolvable and clean at the fixture rev, real tool ⇒ `main(...) == 1 and "frozen-population-mismatch" in out` (mutant reaches `C3=met`, rc 0) | `population_frozen_ok`/`_triplicate`/`_subset` :192–196 — pure-function arms; `main`'s gate is never executed |
| 15 | `defeated_accepted` | `count-c3.py:171` | `fixture_run` (116–175) | in-mem | a stub tool that **exits 1** printing `revisions=0` and **no** `REVISION_MISMATCH` ⇒ `fixture_run(..., "one-stale")[0] is False` | none — `fixture_run` is never called from `selfcheck`; the tautology at :187 is unrelated |
| 16 | `carrier_drift_allowed` | `count-c3.py:274` | `main` (204–304) | main-path | frozen three bindings as strings + worktree `SCORECARD.md` differing from `show(rev:SCORECARD.md)`, tool clean after the gate ⇒ `main(...) == 2 and "worktree differs" in stderr` (mutant rc 0) | `carrier_drift_guard` :187–188 — a literal string tautology; `("a\n" != "b\n") and ("a\n" == "a\n")` passes under every mutant |
| 17 | `bindings_floor_dropped` | `count-c3.py:293` | `main` (204–304) | in-mem via lifted gate, else main-path | with `run_met(caught, q, fields, bindings)` holding the anchor: `run_met(True, rc0, {"revisions":0}, 2) is False` while `(…,3)` is True. Main-path alternative: a clean tool stub reporting `bindings=2` ⇒ `main(...) == 1` | none — `met` never runs in `selfcheck` |
| 18 | `selftest_red_accepted` | `count-c3.py:247` | `main` (204–304) | main-path | tool stub prints `RECORD_SWEEP_SELFTEST pass=30 fail=0` **then exits 1**; rest green ⇒ `main(...) == 1 and "selftest=red" in out` (mutant rc 0) | none |
| 19 | `revisions_default_zero` | `count-c3.py:292` | `main` (204–304) | in-mem via lifted gate, else main-path | `run_met(True, rc0, {}, 3) is False` (no `revisions=` token ⇒ −1). Main-path alternative: clean stub printing a summary with no `revisions=` ⇒ `main(...) == 1 and "revisions=-1" in out` | none |
| 20 | `summary_first_line` | `count-c3.py:58` | `summary` (53–60) | in-mem | two `RECORD_SWEEP` lines, last one `revisions=0 bindings=3` ⇒ `summary(...)["revisions"] == 0 and [...]["bindings"] == 3` | `summary_parse` :181 — one summary line only |

Already killed at entering (not survivors, listed for completeness): `unanchored_still_graded`
(`count-c1.py:144`, in-mem, `duplicate_anchor_excluded` :216 catches it), `stale_accepted`
(`count-c2.py:168`, `stale_classification` :249), `derive_key_eol_only` (`count-c2.py:46`,
`conformant` :236).

## 3. The blocker: `duplicates_accepted` is an equivalent mutant

`count-c2.py:166` adds the duplicate count into `residual`:

```text
166:    residual += duplicates
167:    met = (p.returncode == 1 and bool(tokens) and not unclassified and residual == 0
168:           and malformed == 0 and duplicates == 0 and not stale and agreed == len(tokens)
```

`grade` requires `residual == 0`, and `residual ≥ duplicates` always. So `met` can only be true
when `duplicates == 0`; the mutant's dropped `duplicates == 0` clause is unreachable-by-removal:
**`met_pristine ≡ met_mutant` for every possible input**, and `tail` prints
`residual={residual + malformed}`, identical in both. Measured confirmation on a duplicate-line
fixture (both modules run over the same loader):

```text
pristine met= False | tokens=4 classified=4 agreed=4 residual=1 stale=0 retired=1 cell=1 | ['duplicate-classification-lines=1']
mutant   met= False | tokens=4 classified=4 agreed=4 residual=1 stale=0 retired=1 cell=1 | ['duplicate-classification-lines=1']
```

Consequence: the w1 spec's arm for this mutant (`build-w1-spec.py:137–138`, "a fixture writing a
duplicated `DRIFT_CLASS` line must be unmet and count the duplicate as residual") is a **fake
arm**. It passes under the mutant, because the duplicate is unmet for a *different* reason
(`residual`), so the executor can tick it off while the survivor remains and the frozen target
`killed=23` stays unreachable.

Behaviour-preserving repair (verified): change the non-anchor accounting conjunct on
`count-c2.py:167` from `residual == 0` to `residual - duplicates == 0`. `duplicates` stay in the
printed `residual` (so the tail and notes are byte-identical on every input), and `met` keeps the
same truth table because `malformed == 0` and `duplicates == 0` are still required. The frozen
anchor on :168 is untouched. Then a duplicate-line arm asserting `(not met)` kills the mutant.

Evidence: with `residual - duplicates == 0` plus a `duplicate_line_unmet` arm, the patched
`count-c2.py` selftest is `pass=16 fail=0`, the duplicate fixture still reads
`residual=1 … cell=1`, and **all nine** c2 mutants are killed (`duplicates_accepted rc=1`). A
strictly-larger alternative — deleting `residual += duplicates` — also kills it but changes the
counter's displayed residual, which the claim does not need and reviewers can call a behaviour
change; the accounting split costs nothing observable.

This edit is outside the contract's literal repair envelope ("add arms or make a main-path gate
reachable"). It changes no graded output and no anchor, so I recommend the L1 record the
equivalence proof with the after-receipt. If the L1 refuses the edit, the frozen claim
`killed=23` must be restated before the after value is taken — no arm can produce it.

## 4. Verified kill evidence for the whole map

Scratch replica: the three r82 counters copied from the current worktree, patched with the arms
named above (plus `counter_ok` / `run_met` helpers and the c2 accounting split), then the frozen
r83 counter's own `grade()` run over a loader serving those bytes:

```text
met= True
mutants=23 killed=23 survivors=0 total=23 pristine=green
extras= []
  MUTANT count-c1.py green_ignores_fail_token killed rc=1
  MUTANT count-c1.py killed_ignores_rc killed rc=1
  MUTANT count-c1.py ignore_pristine_red killed rc=1
  MUTANT count-c1.py accept_empty_population killed rc=1
  MUTANT count-c1.py unanchored_excused killed rc=1
  MUTANT count-c1.py detector_gate_dropped killed rc=1
  MUTANT count-c1.py unanchored_still_graded killed rc=1
  MUTANT count-c2.py stale_accepted killed rc=1
  MUTANT count-c2.py duplicates_accepted killed rc=1
  MUTANT count-c2.py retired_paths_unchecked killed rc=1
  MUTANT count-c2.py red_literal_unchecked killed rc=1
  MUTANT count-c2.py green_census_tokens_accepted killed rc=1
  MUTANT count-c2.py finding_branch_inverted killed rc=1
  MUTANT count-c2.py malformed_not_residual killed rc=1
  MUTANT count-c2.py keyshape_guard_inverted killed rc=1
  MUTANT count-c2.py derive_key_eol_only killed rc=1
  MUTANT count-c3.py population_gate_dropped killed rc=1
  MUTANT count-c3.py defeated_accepted killed rc=1
  MUTANT count-c3.py carrier_drift_allowed killed rc=1
  MUTANT count-c3.py bindings_floor_dropped killed rc=1
  MUTANT count-c3.py selftest_red_accepted killed rc=1
  MUTANT count-c3.py revisions_default_zero killed rc=1
  MUTANT count-c3.py summary_first_line killed rc=1
```

Patched-pristine tallies (each green before any mutant was graded):
`C1_COUNTER_SELFTEST pass=10 fail=0` (4 original + 6 new),
`C2_COUNTER_SELFTEST pass=16 fail=0` (9 original + 7 new),
`C3_COUNTER_SELFTEST pass=15 fail=0` for the main-path-fixture route, or `pass=9 fail=0` for the
cheaper lifted-gate route that covers #17 and #19 only. No anchor was lost in any replica
(`grade` printed no `unanchored` extra).

Per-route notes that matter to the executors:

- **c3 #14** works with the **real tool** if the fixture has two commits: commit `SCORECARD.md`
  with rows carrying `k1=1`, `k2=2`, `k3=3`, take that rev, write the pins naming it, commit
  again, then `main([second_rev, "--repo", fixture])`. Observed: pristine
  `C3=unmet … bindings=frozen-population-mismatch` rc 1; mutant `C3=met … bindings=3
  revisions=0` rc 0. A stub tool is *not* required here.
- **c3 #16 and #18** cannot use the real tool: #16's frozen-binding revs do not resolve in a
  fixture, and the mutant would then fail the run for a different reason; #18 needs a tool that
  prints a green summary and exits 1. Both need a small Python tool stub reading `--selftest`,
  `--pins`, `--git`; discriminate the real run from the three `fixture_run` calls by
  `basename(--pins) == "committed-pins.json"` (main writes the committed pins to exactly that
  name under its scratch).
- **c3 #17/#19** are cheapest as the spec says (`build-w1-spec.py:183–186`): lift the two-line
  `met = (…)` conjunction into `run_met(caught, q, fields, bindings)` with the anchors verbatim,
  and have `main` call it. Measured: `C3_COUNTER_SELFTEST pass=9 fail=0`, both mutants killed,
  both anchors still count 1. The stub route also works (`bindings=2`; summary with no
  `revisions=`) if the executor prefers not to touch `main`.

## 5. Fake-arm traps (existing and easy to write)

Existing:
1. **`count-c3.py:187–188` — `carrier_drift_guard` is a tautology.** `("a\n" != "b\n") and
   ("a\n" == "a\n")` compares literals; it never calls the worktree-vs-revision comparison and
   stays PASS under `carrier_drift_allowed`. Replace it with the real `main()` drift arm; do not
   count it as coverage.
2. **`count-c3.py:189` — `arms_floor` restates a constant.** `30 >= ARMS_FLOOR and 29 <
   ARMS_FLOOR` asserts the module constant, not the tool's arm count. Harmless, but it is not
   coverage of the gate `main` applies to the *tool's* `pass=` value.
3. **`count-c1.py:216` — `duplicate_anchor_excluded` is a half-arm.** It asserts tail strings
   (`"unanchored" in extras`, `"total=0"`) and never `not met`; `accept_empty_population` and
   `unanchored_excused` both live below that gap.
4. **`count-c1.py:222` — `red_pristine_reported` cannot see the pristine gate.** Its fixture's
   mutant is `pass=0 → pass=0`, i.e. an empty mutation, so `total=0` already blocks `met`; and
   its fixture exits 1, so the `fail=` conjunct of `green` is never isolated.
5. **`count-c2.py:252`, `:257`, `:259` — masked conjuncts.** `red_cell_keeps_unmet` removes the
   `r10 pin retired` phrase instead of adding the red literal; `retired_row_required` deletes the
   whole row instead of one named path; `green_pin_is_unmet` uses a token-less census so the
   `rc == 1` clause is never exercised.
6. **`count-c3.py:192–196` — pure-function arms only.** `population_ok` is graded; `main`'s
   `if not population_ok(pins):` is not. Passing these four says nothing about the gate.

Traps a hurried repair can add:
7. A "duplicate line must be unmet" arm (the spec's c2 item 1) — **passes under the mutant**;
   the duplicate is unmet through `residual`, not through the `duplicates == 0` clause (§3).
8. An arm that asserts `not met` for the **unanchored** fixture and expects the `total > 0` clause
   to be the reason — the `unanchored` extras block `met` on their own; pair it with an empty
   population arm instead.
9. An arm that asserts against the mutant's **label/tail text** that the mutation did not change
   (e.g. `"unanchored" in extras` under `unanchored_excused`): the extras string is produced by
   the *uncherished* branch, so it is identical under the mutant. Assert `not met`.
10. An arm that fabricates a passing `RECORD_SWEEP` summary (hardcoded `revisions=0 bindings=3`)
    without checking that the tool path was actually exercised. For #14/#16/#18 the stub is
    legitimate only because the gate under test runs *before* the tool's semantics; the arm must
    assert the discriminating token (`frozen-population-mismatch`, `worktree differs`,
    `selftest=red`) as well as the exit code, which is what the verified arms do.
11. Kill-by-timeout: see §6, item 1 — an arm that hangs is "killed" by `selftest_run`'s rc 124
    for the *pristine* copy too, which reddens `pristine` and makes C1 unmet, not met.

## 6. Collision scan — repairs that would duplicate a frozen anchor

Anchor count is `base.count(old)`, so **any second occurrence anywhere in the file** (comment,
docstring, fixture literal, new helper) reads `unanchored` and fails C1. Demonstrated by
inspection of the patched bytes (each right-hand count is what the frozen counter would see):

| repair pattern | anchor | count after |
|---|---|---|
| add a `counter_ok` helper **without** replacing `main`'s return | `return 0 if (met and own_ok) else 1` | **2** |
| write the population gate inside `selfcheck` (`if not population_ok(pins):`) | `if not population_ok(pins):` | **2** |
| restate the summary default in an arm | `fields.get("revisions", -1) == 0` | **2** |
| restate the binding floor as a conjunction (`… and bindings >= 3`) | `and bindings >= 3` | **2** |
| an 8-space-indented `if m:` inside `selfcheck` | `        if m:` (leading spaces are part of the anchor) | **2** |
| restate `fixture_run`'s caught conjunction in an arm | `ok = p.returncode == 1 and fields.get("revisions", 0) >= expect[1] \` + newline + `            and "REVISION_MISMATCH" in out` | **2** |
| restate the anchor-count guard in a helper | `if base.count(old) != 1:` | **2** |
| restate the pristine gate in an arm | `met = pristine_ok and total > 0` | **2** |

Safe patterns used by the verified arms: call the function (`green(...)`, `killed(...)`,
`derive(...)`, `summary(...)`, `fixture_run(...)`, `main(...)`) and assert on its **result**; never
paste the guard text. If a helper is extracted, the anchor must move into it and the old site must
call the helper — never leave both (this is the one anchor-motion risk in the whole map; see §7).

Insert points: `count-c1.py:224`, `count-c2.py:264`, `count-c3.py:197` (the `ok = sum(...)` line in
each `selfcheck`). Arms added after `ok = sum(...)` would not be counted or run.

## 7. Anchor-motion risk (the claim forbids removing/duplicating an anchor)

- **`detector_gate_dropped` is the only survivor whose kill cannot be produced in memory without
  relocating the anchor line.** `main`'s `own_ok` is computed by re-running the counter's *own*
  `--selftest`; inside `selfcheck`, that call recurses. Two honest routes:
  (a) extract `def counter_ok(met, own_ok)` whose body is the anchor verbatim, `main` returns
  `counter_ok(met, own_ok)`, and an arm asserts the truth table. The anchor stays byte-identical
  and occurs exactly once, but its *site* moves — the contract's letter forbids removal and
  duplication, not relocation, and the c3 brief already sanctions exactly this shape for `met`
  (`build-w1-spec.py:183–186`). This is what I verified.
  (b) the c1 brief's copy-and-rewrite arm (`build-w1-spec.py:107–111`). It works **only** at a
  revision where `met` is already True; during the executor's pre-commit worktree it reads red
  for pristine and mutant alike and kills nothing, and the arm's spawned copy re-enters
  `selfcheck`, which re-runs the arm — an unbounded process chain unless the arm guards on an env
  var. Do not land (b) without the guard.
- No other survivor needs an anchor to move: every other arm is a call + assertion, and the c2
  accounting split edits `count-c2.py:167`, which is not an anchor.

## 8. Defects found in other seats' bytes (file:line)

1. **`build-w1-spec.py:137–138` (c2 executor brief, item 1) — the prescribed arm cannot kill
   `duplicates_accepted`.** It is the fake arm described in §3; the executor will report a green
   selftest and a surviving mutant, or (worse) record the arm as the fix.
2. **`build-w1-spec.py:174–176` (c3 brief, item 1) — "`record-pins.json` with ONE binding" cannot
   kill `population_gate_dropped`.** The mutant then reaches `met`, but `bindings >= 3` is false
   (`bindings=1`), so `main` still exits 1 for both copies. The fixture must carry **three**
   non-frozen bindings (or a tool stub reporting `bindings=3`), as verified in §4.
3. **`build-w1-spec.py:181–182` (c3 brief, item 3) — "the fixture may pin the frozen three
   bindings as strings … because the drift check runs before the tool" is necessary but not
   sufficient.** Under the mutant the tool *does* run, and the real tool cannot resolve
   `075574c8`/`482dc48d` in a fixture, so it returns findings and `met` stays false; the arm
   needs a clean tool stub for the post-gate path.
4. **`build-w1-spec.py:107–111` (c1 brief, item 6) — the copy arm has an unbounded recursion and
   a pre-commit blind spot** (see §7(b)). Suggest the L1 steer the c1 executor to route (a).
5. **`.ufo/waves/round-82/count-c3.py:187–188` — the `carrier_drift_guard` tautology** still
   ships in the graded bytes and passes under `carrier_drift_allowed`; it should be replaced, not
   kept alongside the new arm.

## 9. Exact commands run (decisive lines)

```text
$ git rev-parse --short HEAD && git log --oneline -3
466d28bc
466d28bc round-83: wave w1 spec, dispatch and handoff (14 seats)
9075c729 round-83: freeze contract, counters and entering controls
68185d6e round-82 verifier spot-check (integrator, hyaku): non-admit/reject

$ git diff --stat 9075c729 466d28bc -- .ufo/waves/round-82 .ufo/waves/round-83 tools/mori-record-sweep.py
 .ufo/waves/round-83/build-w1-spec.py          | 567 ++++++++++++++++++++++++++
 .ufo/waves/round-83/evidence/controls-r83.txt |  29 ++
 .ufo/waves/round-83/w1-dispatch.json          | 267 ++++++++++++++++++
 .ufo/waves/round-83/w1-spec.json              | 157 +++++++++
 .ufo/waves/round-83/w1-validator.err          |   0
 .ufo/waves/round-83/w1.ready                  |   1 +
 6 files changed, 1021 insertions(+)

$ HYAKU_SCRATCH=/fast/…/runs python3 -I .ufo/waves/round-83/count-c1.py 466d28bc
C1=unmet mutants=23 killed=3 survivors=20 total=23 pristine=green detector=green rev=466d28bc229f

$ python3 <scratch driver: ast + anchor counts over the three r82 counters>
count-c1.py 299 lines; every anchor count=1 (7 entries)
count-c2.py 317 lines; every anchor count=1 (9 entries)
count-c3.py 308 lines; every anchor count=1 (7 entries)

$ python3 <scratch driver: patched copies, per-mutant selftest>
PRISTINE c1 rc=0  C1_COUNTER_SELFTEST pass=10 fail=0
PRISTINE c2 rc=0  C2_COUNTER_SELFTEST pass=16 fail=0
PRISTINE c3 rc=0  C3_COUNTER_SELFTEST pass=15 fail=0   (stub route)
PRISTINE c3 rc=0  C3_COUNTER_SELFTEST pass=9  fail=0   (lifted-gate route)
20/20 survivors killed rc=1; full population mutants=23 killed=23 survivors=0 total=23
pristine=green; extras=[]

$ python3 <scratch driver: equivalence probe for duplicates_accepted>
pristine met= False | tokens=4 … residual=1 … | ['duplicate-classification-lines=1']
mutant   met= False | tokens=4 … residual=1 … | ['duplicate-classification-lines=1']

$ python3 <scratch driver: collision demos>
counter_ok helper left beside main's return        -> 2
"if not population_ok(pins):" inside selfcheck    -> 2
fields.get("revisions", -1) == 0 restated         -> 2
"and bindings >= 3" restated                      -> 2
8-space "if m:" inside selfcheck                  -> 2
fixture_run conjunction restated                  -> 2
"if base.count(old) != 1:" restated               -> 2
"met = pristine_ok and total > 0" restated        -> 2
```

## 10. Not verified / limits

- I did not run the round-83 counter end-to-end against a **git revision** carrying the repairs
  (committing is the L1's, and I ran no mutating git command). The full-population result above
  comes from the frozen counter's own `grade()` over a loader serving the patched bytes — the same
  code path `main` uses after `loader`, with `pristine`/`mutant` copies written to scratch and
  each copy run as `python3 -I <copy> --selftest` under scratch cwd/TMPDIR. The `harness=present`
  + `FROZEN_MARKERS` + `own_ok` wrapper of `main` was not part of that run.
- The c3 main-path arms were verified against **my stub tool** and, for #14, the **current real
  tool** (`tools/mori-record-sweep.py` sha `4b34f004…`, `ANCHORED_OCCURRENCE` count 0 — the C3
  executor has not landed yet). When the tool changes, #15's three `fixture_run` kinds and #14's
  real run must be re-checked against the landed tool; #16/#18 use the stub by design.
- The c2 accounting split (`residual - duplicates == 0`) is behaviour-preserving for `met` and the
  tail but is a **non-anchor edit outside the literal repair envelope**; permissibility is the
  L1's call, and if refused the frozen target must be restated.
- I did not measure the round-83 counters' own mutation adequacy (a sibling seat owns that), nor
  the C2/C3 claims. Only C1's arm surface was in scope.
- No lane byte was changed by me; `git status --porcelain` was not needed because my only writes
  were this report and scratch (deleted).
