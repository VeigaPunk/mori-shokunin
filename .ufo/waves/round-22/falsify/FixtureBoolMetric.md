# FixtureBoolMetric — falsification of frozen v2 variant `bool-metric` (R18 second arm)

Seat: MoriR22.FixtureBoolMetric (critic, static, read-only). Effective correction read first (`denominator-correction.md`).
Method: static reading of the frozen builder, oracle, SUT, gate, and refinement runner, plus read-only inspection of retained measure1 evidence and the retained synthetic fixture repos (read-only `git -C` plumbing and `jq`). No fixture, oracle, SUT, test, or build was executed. No tools were installed or updated. This report contains no matched text.

## Verdict

The fixture variant is sound. Its target reason is distinguishable in the SUT's output, but the frozen oracle conjunct does not distinguish it. The defect is fixable and is not a tradeoff the judge must reject. The observed R18 pass is true for the right reason, according to retained evidence.

## Bindings verified

| Item | Value |
|---|---|
| `frozen/fixture-builder-v2.py` sha256 | `1b3e16f7…d15d1`, which matches the on-disk file, the e2f549b blob, the `requirements-v2.json` pin, and `fixture_builder_sha256` in after/restored observations |
| `oracle-reconcile-v2.py` sha256 | `dcd1c7c6…0adb`, matching the same four places |
| Freeze order | builder, oracle, and requirements are only touched by e2f549b (10:55:59). SUT first appears at 8cb4afb (11:02:25), so the freeze precedes the SUT |
| SUT `tools/mori-retention-reconcile.py` | on disk = HEAD blob = observed `tool_sha256` `d6870fb6…0ce7`. Line 188 strict counter check has been present since 8cb4afb |

## Mutation provenance (builder lines 76–96)

- `bool-metric` sets `result['metric']=True` after `wrapper` is built, and `wrapper['stdout']=json.dumps(result)` (line 88) serializes it afterwards. This is a scalar replacement with no aliasing into `hits`, `allowlisted_hits`, or `unallowlisted_hits`. The aliasing variants `inject`/`digest`/`line`/`class`/`bool-line` mutate dicts or lists shared with `hits`. For `inject`, that also pollutes the returned `expected_scanner_hits`. This is harmless, because the oracle only consumes `expected_*` for `valid` (R04), and it does not affect this variant.
- Restoration is not needed. Each variant is a fresh repo (`mkdir(exist_ok=False)`), and the oracle cache builds it once. `restored-observed.json` (SUT source restored after the measure mutants) repeats the identical bool-metric outcome with tool sha `d6870fb6…`.
- Retained fixture repos, `.scratch/round22/measure1/after-fixtures/{valid,bool-metric}`:
  - Both share the measured commit `a8e8b5df…` and measured tree `b3ea6cdf…`. The dates are fixed, the tree is identical, and there is no parent.
  - The policy blob `85782d09…` and the allowlist blob `34b74af4…` are identical.
  - After normalizing the repo root, the wrapper minus `stdout` is byte-equal, and the inner result differs in exactly one line: `"metric": 1` versus `"metric": true`.
- So the variant is a single-field delta from a fully reconcilable control.

## Truth of expected identities and partitions (unchanged from `valid`)

Static recount, cross-checked against the gate's `_scan_result` (lines 260–267) and the SUT (lines 195–210):

| Partition | Value |
|---|---|
| Raw hits (5) | `policy.json` 1 (the `synthetic` field; the policy file is scanned normally per the correction), `allowed.txt` 2 (lines 1 and 2, the same `line_sha256`), `unallowed.txt` 1, `non-author.txt` 1 |
| Skipped | `binary.bin` (contains NUL). `allowlist.json` holds no token |
| Policy-excluded | 1, the non-author glob identity only |
| Scanner hits | 4 |
| Allowlisted | 3 (the `policy.json` hit and both `allowed.txt` hits) |
| Unallowlisted | 1 (non-author is excluded before allowlist subtraction, exactly as the gate does) |
| Counters | `metric=1`, `routed=0`, `non_author=1`, `RETENTION_FINDINGS`, wrapper exit 1 |

All of these are true. The retained receipt shows 5/1/3 hit lists. Every check before line 188 holds for this fixture when `--output` is absolute: schema, ancestry, policy/allowlist byte equality, argv repo/policy/allowlist/rev bindings, inner commit, and `policy_sha256`. So the SUT's first failing predicate is `integer(True)`, which gives `receipt_counter_type`. The `bool-metric` variant does not consume the `expected_*` fields.

## Discrimination power of the target

- `True == 1` in Python. A SUT that accepts booleans as ints compares `receipt['metric']!=len(unallowed)` and finds no difference. It therefore returns exit 0 `RETENTION_RECONCILED`, not exit 1, so the oracle conjunct fails. This makes the arm the only frozen arm that kills "bool accepted as an int for metric". R10's `metric=0` lie is caught by any value comparison.
- None of the four measure1 mutants (count-only, false-clearance, wrong-population, setup-leak) removes the strict metric check. The arm's kill capability is therefore unexercised and rests on static inference only [INFERENCE: not executed].
- Observed in after, restored, and all four mutant observations: bool-metric gives exit 2, `RETENTION_RECONCILIATION_SETUP`, `error=receipt_counter_type`, and empty stderr. The SUT's reason code differs from the generic catch-all `input_unavailable` and from every other setup code.

## Counterexamples

1. **The oracle cannot attribute the reason, and the conjunct is not conditioned on the paired control (oracle line 57).**
   - The conjunct checks only `returncode==2` and `finding_id==SETUP`.
   - Strongest concrete case: run the oracle with a relative `--output`. Then `fixture_root` is relative, so the receipt argv `--repo` is relative. The SUT then fails every receipt at `receipt_repo_binding` (line 176) before line 188.
   - The conjunct (and the bool-line arm) would still be credited, so R18 passes while R01 and R05–R12 fail.
   - Retained evidence shows the same independence. In `mutant-wrong-population-observed.json`, R01 is false (valid gives exit 1 mismatch) and R18 is true.
   - R18 credit therefore is not independent evidence of boolean rejection. The global `unmet>0` still prevents a false overall match, so this is an attribution and calibration defect, not a false green.
2. **The bool-metric conjunct is weaker than `record()`.**
   - It omits `cp.stderr==''`, which `record()` applies to the bool-line arm. It also checks neither `privacy_clearance is False` nor the sanitized setup key set.
   - Mitigation: `measure-round22.py safe_outputs` checks every `runs[]` row (stderr empty, markers absent, allowed keys, `privacy_clearance is False`), and that includes this arm. The frozen-24 oracle alone does not.
3. **Results provenance.**
   - The R18 results row records `variant:'bool-line'` only. The bool-metric arm appears only in `runs[]`, so a failing R18 does not say which arm failed.
   - The `data['results'][-2]` positional patch currently targets R18 correctly (R13–R19 are the last 7 records). It depends on record order, though.
4. **No reason is pinned for metric anywhere.**
   - Refinements pin `receipt_counter_type` only for `boolean-routed` and `receipt_exit_type` for `boolean-exit`. They share the line-188 loop with metric, but a per-field regression is not pinned.

## Impacted axes

Calibration (per-requirement attribution) is the main one. Depth (adversarial mutant coverage) is minor. Correctness of the observed R18 pass is not impacted.

## Smallest safe correction

Leave frozen v2 byte-unchanged; it is retained evidence. In a future frozen v3 conjunct, or in the co-evolved `refinement-reconcile.py`:

- Require that the cached `invoke('valid')` in the same run is exit 0 `RETENTION_RECONCILED` with empty stderr.
- Require `cp.stderr==''`, `set(v)=={'schema','finding_id','error','privacy_clearance','receipt_match'}`, and `v['privacy_clearance'] is False`.
- Emit the bool-metric arm as its own named sub-result in `results`.
- Add a refinement case `boolean-metric` that expects `error=='receipt_counter_type'`. A reason pin is legitimate in the co-evolved runner. It must not be added to the frozen-24 oracle post hoc, because that would fit the oracle to the SUT.
- Optionally, add a measure mutant that drops `'metric'` from the line-188 tuple, to exercise the arm's kill capability.
