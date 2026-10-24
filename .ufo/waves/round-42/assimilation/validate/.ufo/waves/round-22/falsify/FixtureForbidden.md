# FixtureForbidden — frozen v2 `forbidden` variant and R11 oracle predicate

Seat `MoriR22.FixtureForbidden` (critic). Static falsification only. No fixture, oracle, tool, test, build, or selftest was executed. Read-only inputs:

- `denominator-correction.md` (read first) and `contract.md`
- `frozen/fixture-builder-v2.py` (sha `1b3e16f7…`, equal to the `requirements-v2.json` pin) and `frozen/fixture-builder.py` (v1)
- `oracle-reconcile-v2.py` (sha `dcd1c7c6…`, equal to its pin) and `oracle-reconcile.py`
- `refinement-reconcile.py` and `measure-round22.py`
- `tools/mori-retention-reconcile.py`: current sha `d6870fb6…`, which equals `summary.json.tool_sha256` at measured revision `4f7cfce`. `git diff 4f7cfce HEAD` is empty for the tool, frozen dir, oracle, and refinement runner.
- `tools/mori-retention-gate.py` (`validate_policy` L58-86, `_scan_result` L226-308)
- retained `evidence/measure1/*` and `frozen/expected-real.json`

Retained evidence was inspected through jq field projections only: paths, line numbers, digest prefixes, and counters. No matched text appears here. Installs: none.

## Verdict

The forbidden fixture is sound: its receipt is truthful, it differs from the valid fixture by exactly one factor, and an R11 pass cannot be faked by a setup error. Current shipping code reconciles it correctly. R11 is fail-incapable for receipt-side forbidden laundering, though, and neither the frozen 24 nor the 25 refinement cases close that gap. This is a fixable oracle-coverage defect, not a defect in the shipping tool.

## 1. Truth of expected identities and partitions (holds)

Static trace of the `forbidden` variant against the gate's `_scan_result`:

- **Hits at the measured tree.** There are 5 hits: `allowed.txt:1`, `allowed.txt:2`, `non-author.txt:1`, `policy.json` (the `synthetic` key line), and `unallowed.txt:1`. `binary.bin` contains a NUL byte and is skipped. `allowlist.json` produces no hit because its rows hold only digests and reason text. The policy regex literal `[R]22…` does not self-match. `receipt.json` is committed after the measured commit, so the scan never sees it.
- **Allowlist classification.** The gate's `validate_policy` accepts the extra `synthetic` key. The policy row matches a hit, so it is allowlisted. The `allowed.txt` row has `path ∈ must_redact_paths`, so it is classified `allowlist_forbidden` (gate L241) and never enters `allowed_keys`.
- **Derived counts.** `unallowlisted` = {`unallowed.txt:1`, `allowed.txt:1`, `allowed.txt:2`}, so `metric=3`. `routed=2` and `non_author=1`. `warnings` is empty because nothing is stale. `finding_id=allowlist_forbidden` and the exit code is 1.
- **Fixture agreement.** The fixture's L68-75 hand-derived receipt states every one of these values, including the five-key forbidden row `{finding_id, path, class, line_sha256, line:null}`. That is exactly the gate shape and the SUT's `auxiliary` key set.
- **Exclusion basis.** Policy-excluded identities (`non-author.txt:1`) and scanner identities (the other 4) stay on the non-author-glob basis. `must_redact_paths` is correctly not an exclusion basis, which is consistent with the correction.
- **Retained observation agrees.** The R11 run returned exit 0, `RETENTION_RECONCILED`, `differences=[]`, and counts 5/1/4. It reported `raw_unallowlisted=3`, `scanner_unallowlisted=3`, `allowlisted=1`, `forbidden_allowlist=1`, `retention_state=red`, and `privacy_clearance=false`. The observed `raw_hits`, `policy_excluded_hits`, and `scanner_hits` identities (path, line, digest prefix) equal the fixture's expected lists.
- **Qualification.** Receipt truth is established by static trace against the gate source, not by running the gate. The receipt is a hand-modelled gate output, co-authored by L1 with the oracle.

## 2. Mutation and restoration provenance (holds)

- **Single-factor mutation.** The only change is `policy['must_redact_paths']=['allowed.txt']` (L44-46). It is applied before hit computation and before the measured commit, so policy bytes at the measured revision equal those at the input revision and the policy-changed setup path (R15) is not triggered. The retained evidence confirms the single factor:
  - The allowlist digest `255971e9…` is identical in the valid and forbidden fixtures.
  - The policy digest differs (`38ec0221…` vs `d1336f4a…`, observed equal to expected in both).
  - The policy hit moves from line 13 to line 15 because the list expands by two lines; its `line_sha256` (`ff480191…`) is unchanged.
- **No shared state.** `make()` builds a fresh `policy` dict and a fresh repo (`mkdir(exist_ok=False)`) on every call, and nothing module-level is mutated. No restoration is needed and none can leak into other variants.
- **The mutation is proven effective in-tree.** A silently no-op mutation would recompute `metric=1` against the receipt's 3, giving MISMATCH and failing R11. The observed `raw_unallowlisted=3` therefore shows the SUT read `must_redact_paths` from the committed policy blob.
- **Commit ordering.** The v2 builder was committed in `e2f549b`, before the SUT implementation in `8cb4afb`. It is the only commit touching that file, and its sha matches the pin.

## 3. Is the target reason distinguishable from an unrelated setup error? (yes for R11, with two caveats)

R11 expects exit 0 / `RECONCILED`, which no setup path (exit 2) can reach. A setup error therefore always fails R11 and can never pass it.

Caveats:

1. **Failure attribution needs `runs[]`.** The `results[]` row records only `pass`, not the observed exit code, finding, or `error`. A failed R11 cannot be attributed from `results[]` alone; the reason has to be recovered from `runs[]`, which retains it.
2. **Invocation precondition.** `fixture_root` comes from `--output` (oracle L28). With a relative `--output`, the recorded receipt `--repo` is relative and the SUT fails closed with `receipt_repo_binding` (tool L176) on every variant. R11 then fails, but R13-R21 pass spuriously, because the frozen exit-2 arms never check the `error` token. The retained measure1 run used an absolute scratch path, so its evidence is unaffected. This is an oracle invocation fragility outside R11's own reason-binding.

## 4. Counterexample: R11 cannot fail on forbidden laundering (fixable oracle defect)

**Weakened SUT S\*.** Take the shipping tool and delete the comparisons of `routed` and `finding_id` from the L214 tuple, plus L216 (`forbidden_allowlist`), L217 (`warnings`), and L218 (wrapper `exit_code`). All type checks and all hit and partition comparisons stay.

**S\* passes all 24 frozen arms.** R05-R10 mutate only `hits`, `line`, `class`, the digest, or `metric`, all of which S\* still compares. R11 and R12 use honest receipts. Setup arms are unaffected.

**S\* passes all 25 refinement cases** (static trace of `refinement-reconcile.py`):

- Every case is built from `f.make(root/name)`, which is the `valid` variant. No refinement case uses `forbidden`.
- `forged-clean` also deletes the `unallowed.txt` hit, so S\* rejects it through `hits`.
- `allowed-list-only`, `unallowed-list-only`, and `non-author-counter` hit comparisons that S\* keeps.
- `boolean-routed` and `boolean-exit` are type checks, which S\* also keeps.

**Laundered receipt L** (forbidden fixture, with `hits`, both partition lists, `metric`, `routed`, and `non_author` byte-identical to the honest receipt):

| | `forbidden_allowlist` | `finding_id` | `exit_code` |
|---|---|---|---|
| Laundered receipt L | `[]` | `RETENTION_CLEAN` | 0 |
| Recomputed | 1 row | `allowlist_forbidden` | 1 |

- Shipping tool, by trace: exit 1, MISMATCH, `differences ⊇ {finding_id, forbidden_allowlist, exit_code}`. Correct.
- S\*: exit 0, `RETENTION_RECONCILED`. A receipt asserting a clean gate run is certified as an exact match while the recomputed state is forbidden or red.
- The coherent variant (`forbidden_allowlist:[]`, the row moved into `warnings` as `allowlist_stale`, `finding_id=RETENTION_FINDINGS`, exit 1) is also certified by S\*. Gate precedence, not self-consistency, is what catches it.

**Supporting evidence for the M1 lesson.** The retained `mutant-count-only-observed.json` shows R11 `pass:true`. R11's predicate is scalar-only: `forbidden_allowlist==1` and `raw_unallowlisted==3` are derived from the SUT's own recomputation. On an honest receipt those scalars cannot fail, so R11 alone cannot separate population agreement from count agreement. That is exactly lesson M1.

**Second fail-capability gap (ordering).** The fixture's forbidden row matches real hits. A SUT that checks stale before must-redact (`key not in hits → stale; elif path in must → forbidden`) behaves identically on this fixture and survives. The gate checks must-redact first (L241), and so does the shipping tool (L200), so this is again an oracle gap only.

**Prior-note check.** `build/AttackR11.md` reached the S\* conclusion before `refinement-reconcile.py` existed. I re-verified it against the current runner and it still holds. That note's §7 claim that v1 forbidden rows "retain `rule` (6 keys)" is wrong. In v1, allowlist rows never had `rule` (v2 adds it at L59), so v1 forbidden rows had five keys. The actual v1 defect was every allowlist row failing the gate- and SUT-required `rule` field, an unrelated `allowlist_row` setup error on every variant. The correction's "adds mandatory rule=b" fixes exactly this. There is no impact on v2.

## 5. Minor observations (no action required)

- **Unused fixture fields.** The fixture's `expected_raw_unallowlisted` (3/1), `expected_raw_total`, `expected_excluded`, and `expected_scanner_total` are never read by the oracle, which re-encodes them as literals. The values agree, so there is no defect, but there are two authorities for the same fact.
- **R11 omits checks the fixture already supports.** It does not assert `differences==[]`/`receipt_match`, `scanner_unallowlisted`, `allowlisted==1`, or the forbidden variant's `inputs_sha256` (R24 checks digests only on `valid`).
- **Identical unallowlisted counters.** `raw_unallowlisted` and `scanner_unallowlisted` are the same expression, `len(unallowed)` (tool L222). That is correct under gate semantics: the gate's unallowlisted already excludes non-author, giving the real values 4/4. Still, no fixture can tell the two output fields apart.
- **Untested overlap.** A forbidden path that is also non-author (routed over excluded hits) is not exercised by any arm.
- **Real input never hits this path.** The real input expects `forbidden_allowlist:0`, so R11 rests entirely on this synthetic arm.

## Impacted axes

- **Calibration (this round's C1 claim).** "Exact accounting agreement" is overstated: a laundering-blind SUT is admissible under all measured evidence.
- **Depth and fail-capability.** R11 is honest-only and scalar-only.
- **Provenance.** Holds for the forbidden fixture: single-factor mutation, digest-bound, committed before the SUT.
- **No regressions.** Shipping-tool behaviour is unaffected, `privacy_clearance=false` is preserved, and no identity changes.

## Smallest safe correction

Leave the frozen v2 files byte-unchanged. Add co-evolved cases to `refinement-reconcile.py` that build from `f.make(root/name,'forbidden')`, mutate only the declared receipt fields, and assert the exact `differences` set:

| Case | Mutation | Expected `differences` |
|---|---|---|
| `forbidden-laundered-clean` | `forbidden_allowlist=[]`, `finding_id=RETENTION_CLEAN`, `exit_code=0` | `{forbidden_allowlist, finding_id, exit_code}` |
| `forbidden-as-stale` | row moved to `warnings`, `finding_id=RETENTION_FINDINGS` | `{forbidden_allowlist, warnings, finding_id}` |
| `routed-lie` | `routed=0` | `{routed}` |

Each case also asserts exit 1, `MISMATCH`, `receipt_match:false`, `retention_state=red`, and `forbidden_allowlist==1`. Optionally add a no-hit forbidden row case, expecting exit 0 and `forbidden_allowlist==1`, to kill stale-first ordering.

Exact `differences` assertions keep MISMATCH from being satisfied by an unrelated divergence. An S\* mutant should be added to `measure-round22.py`'s mutation list to prove these cases kill it.

**Tradeoff for the judge.** Putting these arms into the frozen R11 instead would invalidate the v2 pins and require a v3 freeze and re-measure. The refinement placement keeps the frozen evidence intact but is co-evolved, authored after the SUT, so it is weaker independence. The canonical judge must decide whether C1's agreement claim may ship with the R11 laundering surface covered only by co-evolved controls, or must be narrowed until it is covered.
