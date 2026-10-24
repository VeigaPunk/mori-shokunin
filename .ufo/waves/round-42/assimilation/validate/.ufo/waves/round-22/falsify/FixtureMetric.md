# FixtureMetric — frozen v2 `metric` variant (R10) and its oracle predicate

Seat: MoriR22.FixtureMetric (critic, leaf). Static only: I ran no fixture builder, oracle, refinement, selftest, SUT, gate, test, build or formatter. Reads used Python only to parse JSON, hash bytes and list archive members of the already-executed `evidence/measure1`. Writes: this file only. Installs: none.

Order read: `denominator-correction.md`, then `contract.md`, `frozen/requirements-v2.json`, `frozen/fixture-builder-v2.py`, `oracle-reconcile-v2.py`, `refinement-reconcile.py`, `measure-round22.py`, shipping `tools/mori-retention-reconcile.py`, gate `_blob_hits`/`_scan_result`, and the `evidence/measure1` observations and archive.

## Axes
A1 the target reason can be told apart from setup or other mismatch causes · A2 expected identities and partitions are true · A3 mutation and restoration provenance · A4 R10 can actually fail · A5 the correction's M1 lesson (counts ≠ populations).

## Pinned inputs (verified)
- These on-disk SHA-256 values equal the `requirements-v2.json` pins: contract `1658c390…`, correction `968945b2…`, builder `1b3e16f7…`, oracle `dcd1c7c6…`.
- Shipping tool is `d6870fb6…`. That equals the `measure1` committed binding and the archived after/restored observation `tool_sha256`.
- `git diff 4f7cfce..HEAD` is empty for the tool, frozen/, oracle, measure and refinement paths. `4f7cfce` is an ancestor of HEAD `5888b56`.

## Findings

### F1 — Setup separation holds; mismatch-reason separation does not (A1, A4)
**Setup separation holds.**
- In the archived `after-fixtures`, the `metric` receipt differs from `valid` only in the inner `metric` field (1→0). The wrapper differs only by fixture-root paths in `argv`. `exit_code`, `finding_id`, `commit`, the lists and the measured commit are identical.
- So every setup check in `check()` sees the same input as R01's valid arm, which returned exit 0 in the same run. `integer(0)` passes `receipt_counter_type`.
- An unrelated setup failure would give exit 2 and SETUP, which R10's expected exit 1 and MISMATCH rejects. So a setup error cannot make R10 pass falsely.
- Observed shipping output for the metric arm: exit 1, `differences==['metric']`.

**Mismatch reason is not checked.** The oracle records R10 at line 51 with no predicate. It never checks `differences`, `receipt_match`, or the tool's own recomputed counters.

**Counterexample from existing evidence.** In `mutant-wrong-population-observed.json`:
- R10 **passes**: exit 1, MISMATCH, `differences==['unallowlisted_hits','metric']`, and the tool's own `raw_unallowlisted==2`.
- The tool's recomputed metric is wrong (2, not 1), yet R10 is green. The mutant is killed only through R01, R02 and the other valid-fixture arms.
- So an R10 pass does not show that the metric recomputation is correct. Only the all-24 conjunction does.

### F2 — No mutant shows R10 can fail; R10 is the only arm that pins metric comparison (A3, A4)
- None of the four executed mutants fails R10:
  - count-only fails R07–R09;
  - false-clearance fails R02, R11 and R23;
  - wrong-population fails nine arms, but not R10;
  - setup-leak is caught by output safety.
- Static trace of the obvious mutant — dropping `('metric',len(unallowed))` from the comparison tuple — under current source:
  - The valid, forbidden and other frozen arms carry a truthful metric (1 or 3).
  - Among the 27 refinement cases, clean-control is 0 vs 0 and non-author-overlap is 1 vs 1. forged-clean already mismatches on `hits`.
  - So R10 is the **sole** killer `[INFERENCE: static]`. That is load-bearing and has zero execution evidence.

### F3 — A zero-valued, one-direction lie lets a non-exact metric check survive everything (A4, A5)
The lie sets metric to 0, the "clean" value. Counterexample mutant: compare only nonzero-ness (`bool(receipt['metric'])!=bool(unallowed)`). Static trace against current source:

| Arm | Receipt metric vs actual | Truthiness mutant |
|---|---|---|
| valid | 1 vs 1 | no difference (R01 passes) |
| metric | 0 vs 1 | difference (R10 passes) |
| forbidden | 3 vs 3 | no difference (R11 passes) |
| bool-metric | rejected at `integer()` first | — |
| refinement clean-control | 0 vs 0 | no difference |
| refinement non-author-overlap | 1 vs 1 | no difference |

- No frozen or refinement arm carries a nonzero wrong metric. The refinement list has no metric case; `refinement-observed` shows 27/27 with none named metric.
- So a tool that accepts metric=2 on a 1-hit tree passes all 24 + 27 arms `[INFERENCE: static]`. This is exactly the M1 class: scalar agreement standing in for exact value.
- I re-verified the earlier AttackR10 CX7/CX8 direction hole against current source: still open.
- I also verified that CX1, CX2 and CX10 (negative, float, duplicate key) are now rejected by the current SUT, at `integer()` and `no_duplicates`. AttackR10 R6 (path binding) is fixed in current source, lines 172–182. Those notes are stale for the SUT but remain uncovered by the oracle.

### F4 — Expected identities and partitions are true but not independently witnessed (A2)
I hand-traced the builder's fixture:
- Hits: policy line 13 synthetic (allowlisted), `allowed.txt` lines 1 and 2 (identical digest, one deduplicated rule=b row), `unallowed.txt` 1, `non-author.txt` 1. `binary.bin` is skipped because it contains NUL. The policy regex line does not self-match. That gives raw 5, excluded 1, scanner 4, unallowlisted 1, allowlisted 3.
- These match the archived after-observation.
- The builder's forged receipt equals gate `_scan_result` semantics line by line:
  - `unallowlisted_hits` excludes non-author paths;
  - `allowlisted_hits` does not;
  - `routed`, the forbidden-row shape (`line: None`), the finding precedence and the exit code all match.
- The receipt and `expected_*` come from the **same** builder `hits` list, using the same algorithm as the SUT and the gate. A shared bug would produce a false red, not a false green.
- The gate is never run on a synthetic fixture, so "the receipt is what the gate would emit" is static only `[INFERENCE]`.
- `expected_policy_hits` is a legacy name: it holds the non-author identity, which is correct per the correction.
- In the SUT, `raw_unallowlisted` and `scanner_unallowlisted` are the same expression. No arm can tell them apart. This is a tradeoff to record, not a fixture defect.

### F5 — R03's count triple cannot discriminate the rejected v1 semantics (A5)
- Wrong-population (exclude the policy-source path) observed `(raw, excluded, scanner) = (5, 1, 4)`, identical to the correct values.
- R03 failed only through its exit/finding precondition, not its predicate. Population discrimination rests entirely on R04's identity predicate.
- This confirms lesson M1 holds in the frozen fixture. Do not cite R03 as evidence of the denominator.

### F6 — Mutation and restoration provenance: bytes verified; "restored" is not a restoration (A3)
- **Mutant bytes verified.** Rebuilding each mutant from current shipping source reproduces the archived mutant hashes exactly:

  | Mutant | SHA-256 prefix |
  |---|---|
  | count-only | `68378bf7` |
  | false-clearance | `c794393a` |
  | wrong-population | `810277e4` |
  | setup-leak | `42c16f40` |

- **false-clearance is wider than one site.** Its replacement hits 4 occurrences, including the setup and selftest dictionaries, not one result site. The kill is still valid, but it is not the single-site design MutationScope specified.
- **Archive matches the summary, but is uncommitted.** The archive hash `575435b6…` equals the summary record. The archive is untracked at HEAD; only `summary.json` binds it.
- **No restoration occurs.** Mutants are written to separate scratch files, and the shipping tool is never modified. `restored_ok` checks `sha(tool.read_bytes())==sha(tool.read_text().encode())`, a text round-trip. It does not compare against the committed binding. It is a second unmutated control, not proof of restoration. The observed restored `tool_sha256` does equal `d6870fb6…`, so there is no defect, only a misleading label.

### F7 — Adjacent risk in the builder environment (A1)
- The builder's `git()` keeps `GIT_OBJECT_DIRECTORY`, `GIT_COMMON_DIR`, `GIT_TEMPLATE_DIR` and alternates. The SUT strips all `GIT_*`.
- A caller environment carrying these would produce SUT `git_read_failed` on every arm.
- R13, R14, R17 and R18 (the bool-metric conjunct) and R20 cannot tell that apart from their target reason, since they check exit 2 and SETUP only, not `error`. R01 failing would still expose it.
- `bool-metric` also omits the `stderr==''` check that `record()` enforces.

## Smallest safe corrections (no frozen or history bytes change)
1. **R10 reason binding** (new v3 requirement or refinement arm; frozen v2 stays as historical): on the metric variant, require `receipt_match is False`, `differences==['metric']`, `raw_unallowlisted==1`, `allowlisted==3`. This kills the F1 counterexample.
2. **Exact-value arms** (refinement): `metric-overclaim` (valid fixture, metric=2, expect 1 MISMATCH with `differences==['metric']`) and `metric-clean-lie` (clean-control, metric=1, expect 1). These kill F3 and close directionality.
3. **Mutation evidence:** add `metric-ignored` (remove the metric tuple; expect R10 as the sole failure) and `metric-truthiness` (expect the new arm 2 to fail). Restrict false-clearance to the result-dictionary occurrence.
4. **Restored control:** compare against `executing-input-bindings[tool].committed_sha256`, and rename it "unmutated control".
5. **Builder environment:** strip all `GIT_*` in the builder, as the SUT does. Assert `error` codes on setup arms where refinements already pin them.

## Verdict
- The metric variant is setup-isolated, and its expected truth is correct (A1 setup and A2 pass).
- R10 is fail-capable only in the one direction where the lie is 0, and it is not bound to its reason. Observed evidence shows R10 passing on a tool with a wrong recomputed metric.
- No mutant has shown R10 can fail. These are fixable oracle and measurement defects, not SUT defects: the current SUT emits the exact `['metric']` reason.
- Claims stay unchanged: `privacy_clearance=false`; RED11/12 retained; both dispositions unknown; baseline acceptance blocked.
