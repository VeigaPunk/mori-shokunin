# Lesson — a masked crash and a genuine repair can produce the identical tally

date: 2026-10-15 · lane: mori-shokunin · round: 2 · source seats: falsify-harness, critic, diag-harness (flash wave)

## The lesson

When a behavioral oracle (a fixture harness grading a gate's output) fails during
*setup*, making the crash stop is indistinguishable from actually fixing the
fixtures — unless the fixtures self-assert their preconditions. Measured this
round on `tools/mori-silence-cases.sh`:

- The pre-wave `gc()` chain (`A || B && C` with `commit --allow-empty -am`) died
  in fixture setup: the empty commit "succeeded", the real content never got
  committed, and the trailing commit failed — exit 1 before any case ran.
- A crash-masked variant (same broken chain + `|| true`) and a genuine repair
  (deterministic stage-then-commit) both yield the **same** tally
  (`MORI_SILENCE_CASES: matched=10 total=27`) and the **same** PASS set against
  the r1 census, because the r1 census reads only last-commit epoch and file
  mtimes — which empty commits plus untouched files reproduce exactly.

So a green-or-even-unchanged tally is not evidence the fixtures are right.

## The countermeasures that worked (evidence-backed)

1. **Pre-register the expected gradient** before landing the fix: pin the exact
   expected tally and PASS-set against the frozen gate SHA; a higher count
   without a gate change is assertion/fixture weakening, a different set needs
   per-case justification (falsify-harness §4, executed this round).
2. **Mutant probes** against the oracle: no-op census → `matched=1`, all-zero
   census → `matched=4`, fixture-mutating census → caught by
   `readonly-no-mutation` (critic seat, all correctly red).
3. **Fixture preconditions / honest gc**: deterministic stage-then-commit that
   *dies* on a no-op commit — an empty commit can no longer impersonate fixture
   state (shipped revision `505a7504`).
4. **Freeze and cite SHAs**: every claim in the round's notes carries the harness
   and census SHA it was measured against; the wave's moving-file hazard (six
   concurrent revisions mid-diagnosis) was handled by hash-pinning every quote.

## Applying it

Any future lane landing a fixture harness or oracle: register the expected
output shape and per-case ids before the repair, keep the gate SHA frozen, and
distrust any tally whose fixtures cannot prove their own precondition
(`git ls-tree` contains the intended path; author/epoch match intent).
