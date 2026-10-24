# FinalR10: falsification of R10 ("metric lie returns 1")

Seat `MoriR22.FinalR10`. Static analysis only: no executions, no production edits, no delegation, no installs. Inputs were read at lane HEAD `5888b565472af49e9a8528c5af9bfbf69035aeb8`:

| Input | SHA-256 |
|---|---|
| `tools/mori-retention-reconcile.py` | `d6870fb6…0ce7` |
| `oracle-reconcile-v2.py` | `dcd1c7c6…8adb` |
| `frozen/fixture-builder-v2.py` | `1b3e16f7…15d1` |

The oracle and fixture-builder hashes equal the pins in `frozen/requirements-v2.json`. The SUT hash equals the `tool_sha256` in `evidence/measure1/summary.json`, `after-observed.json` and `restored-observed.json`. `git diff 3985b3d HEAD -- tools/mori-retention-reconcile.py` is empty. I read the effective correction (`denominator-correction.md`) first. It does not change R10's meaning: "all other 24 requirement meanings remain".

## Verdict

1. **Exit and finding level: R10 holds.** The shipping source returns exit 1 with `RETENTION_RECONCILIATION_MISMATCH` for the frozen `metric` variant.
2. **Branch-level reason: holds in the SUT, fails as a requirement.** The SUT names `metric` as the only difference, but neither the frozen oracle nor the refinements assert the reason. R10 also tests only one direction of the lie: an understated count of 0 against a true count of 1. So R10 cannot tell exact equality apart from a check that only asks whether the count is zero or nonzero.
3. **Same-command red control: missing.** No retained run of the identical oracle command against a present tool ever shows R10 red.

## Holds: SUT branch trace for the `metric` variant

- **Fixture.** `fixture-builder-v2.py` line 84 sets `result['metric']=0`. Every other field stays truthful: 5 hits, 1 unallowlisted hit, 1 non-author hit, `routed` 0, finding `RETENTION_FINDINGS`, `exit_code` 1.
- **Setup checks.** The variant passes every check in SUT lines 158–194:
  - schema, revision, ancestry and byte equality of the policy and allowlist;
  - `metric` is a non-bool, non-negative `int` (line 187, `integer()` at line 33-34);
  - the absolute `--policy` and `--allowlist` arguments in argv strip back to the repo-relative paths (lines 177–182).
- **Recomputation.** Lines 195–209 compute the unallowlisted population as scanner hits minus allowlisted identities, which here is one hit, so `len(unallowed)=1`. This matches the existing gate's `metric` exactly (`tools/mori-retention-gate.py` lines 262–267, non-author excluded and allowlist by identity).
- **Comparison.** Line 214 compares `receipt['metric']` (0) with `len(unallowed)` (1) and appends `'metric'`. The lists, `routed`, `non_author`, `finding_id`, the forbidden and stale auxiliaries, and `exit_code` all match. So `differences==['metric']`, and lines 219–220 emit exit 1 with `MISMATCH` and `receipt_match:false`.
- **Retained observation agrees.** The `metric` run in `after-observed.json` shows exit 1, empty stderr, `differences:["metric"]`, `receipt_match:false` and `raw_unallowlisted:1`.

## Fails: what R10 actually constrains

- **Oracle.** `oracle-reconcile-v2.py` line 51 records R10 with exit code 1, finding `MISMATCH` and empty stderr. It has no predicate: it does not check `differences`, `receipt_match`, or the population. See `record()` at lines 40–46.
- **Refinements.** The `ok` check in `refinement-reconcile.py` (line 94) never reads `differences`. It has no metric-only arm. The `forged-clean` case also changes the lists, and `non-author-counter` targets a different field.
- **Selftest.** The SUT selftest (lines 233–261) has 4 arms: valid, hits list, unsafe path and unknown flag. None of them is a metric arm.

### Smallest counterexample A (lie direction and magnitude)

Change one token at SUT line 214:

```
('metric',len(unallowed))  ->  ('metric',receipt['metric'] or len(unallowed))
```

- **Frozen `metric` variant:** \(0 \lor 1 = 1 \ne 0\), so R10 still passes.
- **Valid and `forbidden` variants:** truthful metric, so they are unchanged.
- **Refinements:** `clean-control` has 0 = 0, and `forged-clean` mismatches through its lists anyway.

[INFERENCE, statically derived and not run] This mutant passes all 24 frozen arms, all refinement cases and the selftest. Yet a receipt identical to the valid one except `metric: 2` would reconcile with exit 0 and `RETENTION_RECONCILED`, an accepted count that disagrees with the identity population. Two other mutants also pass R10 unchanged: a one-sided check `receipt[field] < actual` and a zero-claim check `bool(receipt[field]) != bool(actual)`. This is exactly the correction's lesson M1: scalar agreement is not population agreement.

### Smallest counterexample B (branch reason)

Change one literal at SUT line 215:

```
differences.append(field)  ->  differences.append('hits')
```

[INFERENCE] All oracle and refinement arms keep passing, because no arm reads `differences`. The metric lie would then be attributed to the wrong branch.

## Missing same-command red control

`measure-round22.py` lines 77–82 run the identical oracle command against four mutants:

| Mutant | Unmet arms | R10 |
|---|---|---|
| `count-only` | 3 | pass |
| `false-clearance` | 3 | pass |
| `wrong-population` | 9 | pass |
| `setup-leak` | 0 | pass |

Source: the R10 row in each `mutant-*-observed.json`.

The kill basis on line 94 is "any unmet > 0", not "R10 red". The only R10 red row is in `before-observed.json`, and it is `capability_absent`: the tool was never invoked and the metric branch never ran. So R10's ability to fail is unobserved.

[INFERENCE] Deleting the `('metric',len(unallowed)),` tuple would turn the frozen R10 arm red, because the metric variant would return exit 0. That mutant is the missing control, and it was never run.

## Impacted axes

- **Calibration (claim C1).** An "R10 pass" overstates what is measured. It shows that a nonzero-to-zero understatement is detected, not that the metric is exactly reconciled.
- **Depth.** R10's ability to fail is not demonstrated by any retained same-command run.
- **Unaffected.** Coverage, operability, freshness and adjacency. The real-input expected values (95/5/90, 4 unallowlisted, `privacy_clearance=false`) and the shipping SUT's metric semantics are correct.

**Fixable defect or tradeoff?** This is a fixable measurement defect, not a SUT defect. The frozen v2 oracle is hash-pinned and must not be rewritten, so the fix belongs in the co-evolved, non-frozen controls.

## Smallest safe correction

1. **Refinement arm.** In `refinement-reconcile.py`, add a `metric-over` case that applies `value['metric']+=1` and expects exit 1 with `MISMATCH`. Add the predicate `obj.get('differences')==['metric']`, and apply the same predicate to the frozen-equivalent understated case (`metric=0`).
2. **Mutant control.** In `measure-round22.py`, add the mutation `('metric-ignored',[("('metric',len(unallowed)),","")])` with an R10-specific kill basis: the R10 row in that mutant's observation has `pass:false`, and its refinement row is red. Optionally add the `receipt['metric'] or` mutant from counterexample A, killed by the new `metric-over` arm.
3. **Keep R10 as is.** Do not edit the frozen oracle, the fixture, or `requirements-v2.json`. Record that frozen R10 covers only the understated direction.

No production change is required to the SUT's `metric` branch.

**Out of scope, noted only:**
- `metric=-1` fails closed as `SETUP` with `receipt_counter_type` (exit 2) rather than `MISMATCH`. That fits the contract's fail-closed rule for types and schema.
- The SUT likewise has no value-lie arm for `routed`. Only the boolean-type case `boolean-routed` exists.

## Tools

No installs or updates. I used only `jq`, `sha256sum`, and read-only `git log`, `status` and `diff` on the lane.
