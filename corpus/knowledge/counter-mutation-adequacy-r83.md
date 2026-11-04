source: S598
verified-at: 2026-11-04
recheck: 365d

# Counter mutation adequacy (round 83)

Axes: operability, depth, calibration; freshness, coverage and adjacency are held as boundaries,
not claimed numerical improvements. The source id is assigned by this round's Gate; S598 was
absent from `corpus/SOURCES.md` when this entry was written (registry maximum S597 at round 82).
No guarantee about PIT's software or about this lane is inferred from the page.

## K1 — The rule the source states

Mutation testing seeds faults into code and runs the tests: a failing test kills the mutation, a
passing test lets it live, and "the quality of your tests can be gauged from the percentage of
mutations killed" (S598, pinned line 114; the page's own "How it works in 51 words" block,
pinned lines 106-114 (body 107, 110-112, 114; 51 rendered words), defines killed and lived). Read into this lane's terms: a surviving mutant
is a **coverage finding about the test suite**, not evidence that the mutated behaviour is
correct, and not a pass. The killed share measures how much of the graded behaviour the suite
actually constrains.

The page says nothing about this lane, about a counter's `--selftest`, about anchored mutants, or
about any exit status. Those are the lane's decisions below, grounded in its own frozen
contracts, never in S598.

## K2 — What a counter selftest must do to be mutation-adequate

A counter's `--selftest` is the suite under test; the counter's own gates are the code. The
round-82 probe showed the asymmetry this entry names: the counters graded their helpers but not
themselves (`.ufo/waves/round-82/w1/Mo82M01Mutants.md`, `killed=18 total=38 survivors=20`). The
adequate shape has four requirements:

| Requirement | Why it is required | Failure it prevents |
|---|---|---|
| A pristine green run before any mutant is graded | a red pristine makes every verdict meaningless | a broken fixture scored as a kill |
| Anchored mutants: the `old` string occurs **exactly once**, and an unanchored anchor is never counted as killed | an anchor occurring twice mutates two sites or none | a mutation graded on bytes it did not change |
| A kill rule that reads both channels: non-zero exit **or** `fail=<n>` with n > 0 | a counter may fail by traceback (no `fail=` token) or by a tally with exit 0 | an rc-blind or token-blind detector |
| The counter's own detector selfcheck bound into its verdict | the counter's gates are the graded code, so the selftest is the suite | a counter that grades helpers and passes itself unconditionally |

The r82 harness demonstrates the price of each missing requirement: its own selftest killed 3 of
23 counter mutants, because the arms exercised the helpers' pure functions and left the main-path
gates (`met`, the exit code, the population gate) unreached. The r83 counter (`.ufo/waves/
round-83/count-c1.py`) re-derives the same population at any revision and grades all three
channels, so the claim "the survivor got its arm" is a kill verdict, not an arm count.

## K3 — The twenty survivor classes (r82 probe, primary run)

Each row names the mutated gate and the arm class that reaches it. `in-memory` means a pure
assertion on the function; `main-path` means a scratch fixture that runs the counter's own `main`
with a fixture repository, because the gate is reachable only there.

| Counter | Mutated gate | Arm class |
|---|---|---|
| count-c1 | `green()` forgiving a `fail=<n>` token under rc 0 | in-memory |
| count-c1 | `killed()` ignoring a non-zero exit with no token | in-memory |
| count-c1 | `met` dropping the pristine clause | in-memory (red pristine + ≥1 mutant) |
| count-c1 | `met` dropping the non-empty population clause | in-memory (all-unanchored ⇒ unmet) |
| count-c1 | `met` excusing an `unanchored` anchor | in-memory (unanchored beside a real kill ⇒ unmet) |
| count-c1 | main's `detector` gate dropped | subprocess copy with a doctored summary |
| count-c2 | `met` dropping the duplicate-line clause | in-memory (duplicate `DRIFT_CLASS` ⇒ residual) |
| count-c2 | `retired_ok` returning true without the paths | in-memory (row without the classification path) |
| count-c2 | `cell_state` ignoring the red literal | in-memory (both literals in the cell) |
| count-c2 | live census accepted without the red exit | in-memory (stub exits 0 with tokens) |
| count-c2 | FINDING derivation inverted | in-memory (token in / not in the baseline) |
| count-c2 | malformed line not in the residual tally | in-memory (malformed line ⇒ `residual=1`) |
| count-c2 | "anything else" branch inverted | in-memory (`lane.mori` ⇒ `value-changed`) |
| count-c3 | population gate dropped in main | main-path fixture (wrong population ⇒ named refusal) |
| count-c3 | defeated fixture accepted on exit alone | in-memory stub tool (exit 1, no `REVISION_MISMATCH`) |
| count-c3 | carrier drift comparison dropped | main-path fixture (worktree differs ⇒ setup exit 2) |
| count-c3 | `bindings >= 3` weakened | lifted `met` helper (bindings=1 ⇒ unmet) |
| count-c3 | tool selftest red accepted | main-path fixture (summary + exit 1 ⇒ refused) |
| count-c3 | `revisions` defaulting to 0 | lifted `met` helper (missing token ⇒ unmet) |
| count-c3 | first summary line winning | in-memory (two `RECORD_SWEEP` lines ⇒ last wins) |

## K4 — Limits

- A killed mutant proves the arm's assertion constrains that byte-level expression; it does not
  prove the arm is meaningful, and a fake arm (a tautology, a hardcoded token, an assertion on the
  mutant's label) can kill without testing. The round's reviewers attack exactly this.
- Anchored mutants are brittle by construction: a repair that rewrites the mutated expression
  makes the anchor unanchored, and the frozen population reports that as unmet rather than as a
  silent drop. That is the intended failure mode, not a defect.
- The 23-mutant population is the r82 probe's table, not a complete mutation coverage of the
  three counters. Survivors found later are new claims, never amendments.
- A mutation score is a property of a suite, never of a claim's truth: it says the suite
  constrains the mutated behaviour, not that the measured value is correct.
