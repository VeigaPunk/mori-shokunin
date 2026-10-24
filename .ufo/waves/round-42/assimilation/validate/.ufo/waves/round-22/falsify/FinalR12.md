# FinalR12 — falsify R12 "non-author exclusions retained separately" (round-22, C1)

Seat MoriR22.FinalR12, critic. Static analysis only. I ran no SUT, oracle, fixture builder, selftest, build or test, and installed no tools.

Commands run:
- read-only `git -C` `log`, `diff`, `show`, `ls-tree`
- `sha256sum` over the frozen files
- in-memory `python3 -c` that read already-retained measure1 JSON and compared glob engines on path names only

No matched text was read into or written to this report.

## Inputs read

| File | Status |
|---|---|
| `denominator-correction.md` | read first; sha `968945b2…` = `requirements-v2.correction_sha256` |
| `contract.md` | sha `1658c390…` matches |
| `frozen/requirements-v2.json` | read |
| `oracle-reconcile-v2.py` | sha `dcd1c7c6…` matches |
| `frozen/fixture-builder-v2.py` | sha `1b3e16f7…` matches |
| shipping `tools/mori-retention-reconcile.py` | sha `d6870fb6…`, identical to the measure1 loaded and committed binding at `4f7cfce`, unchanged at HEAD `5888b56` |
| `tools/mori-retention-gate.py:121-122, 226-307` | read |
| `refinement-reconcile.py`, `measure-round22.py` | read |
| retained `evidence/measure1/*` | read |
| prior `build/AttackR12.md` | read; it predates the SUT and the correction, and every claim reused below was re-verified against current source |

## Verdict

**The shipping SUT holds R12 on every branch, read statically.** The frozen oracle cannot fail R12 on its own, however.
- R12's predicate (`oracle-reconcile-v2.py:52`) checks scalars only, and it reuses the cached `valid` invocation shared with R01–R04 and R22–R24.
- No frozen variant changes any non-author accounting.
- In retained evidence, R12 has only ever been red under the `wrong-population` mutant, and there it was red together with R01 (the whole `valid` run exited 1). That is not an R12-specific red.

The same-command red control for R12 is missing from the frozen 24, the selftest and the measure mutation set.

## Branch-level reasons (SUT `tools/mori-retention-reconcile.py`)

| Branch | Lines | Holds/fails | Reason | Fail-capable control that exists |
|---|---|---|---|---|
| B1: non-author classification | 203 | **Holds** | `any(fnmatch.fnmatch(path,pattern))`, the same predicate as the gate's `_is_non_author` (`gate:121-122`). The basis is the non-author glob, not the policy path, as the correction requires. | Frozen R03/R04 (literal glob only). The `wrong-population` mutant was killed (R01–R04, R11, R12, R22–R24 red). |
| B2: raw retention | 204, 228 | **Holds** | `excluded` is filtered from `hits`, so `raw_hits` still carries the non-author identity. Retained `valid` output: `raw_total` 5, `policy_excluded_hits` = [(non-author.txt, 1)]. | Frozen R03, R04, R12, R22 |
| B3: unallowlisted excludes non-author | 205, 207 | **Holds** | `unallowed` is built from `scanner`. This mirrors `gate:262-266`. | Frozen R12 (`raw_unallowlisted`==1), via a receipt-list mismatch |
| B4: allowlisted spans non-author (overlap) | 206 | **Holds** | Built over all `hits`, mirroring `gate:261`. | Co-evolved refinement `non-author-overlap` only (allowlisted 4, observed). No frozen arm. |
| B5: receipt `non_author` value vs recomputation | 214-215 | **Holds** | `receipt['non_author']!=len(excluded)` adds `non_author` to `differences`. | **No frozen arm.** Only refinement `non-author-counter` (exit 1, `differences` [`non_author`] observed), which was committed with the SUT in `8cb4afb`, not frozen before it. |
| B6: receipt `non_author` type guard | 187 | **Holds** | `integer()` rejects bool and float. This guard is load-bearing, because `True!=1` is `False` at line 215. | **None anywhere.** R18 covers only line and metric; refinement covers only `boolean-exit` and `boolean-routed`. |
| B7: output `non_author` provenance | 223 | **Holds** | Emitted as `len(excluded)` (recomputed, not echoed). | **None on a red arm.** The `non-author-counter` predicate checks only exit, finding, `receipt_match` and bindings, not the emitted value. |
| B8: `raw_unallowlisted` vs `scanner_unallowlisted` | 222 | Holds (tradeoff) | Both fields are `len(unallowed)` and can never differ. This is one authority under two names; `expected-real.json` freezes both at 4. It is not an R12 defect, but `raw_` is a misleading label because it does not count raw non-author hits. | n/a |

## Smallest counterexamples (mutants of the shipping SUT, derived statically, not executed)

1. **M-echo-compare.** Delete `('non_author',len(excluded)),` from line 214.
   - Frozen oracle: still 24/24, because the `valid` receipt has `non_author` 1, which equals the recomputation, and no variant mutates it.
   - Selftest: still 4/4, because its policy has `non_author_paths_glob: []` and the receipt says 0.
   - Real arm: still passes, because 5 equals 5.
   - Killed only by the co-evolved refinement `non-author-counter`.
2. **M-bool.** Change line 187 from `('metric','routed','non_author')` to `('metric','routed')`.
   - Input: the `valid` fixture with receipt `non_author: true`.
   - The current SUT exits 2 with `receipt_counter_type`. The mutant exits 0 with `RETENTION_RECONCILED`, since `True==1`. This violates the contract clause "Explicit booleans not accepted as ints".
   - It survives the frozen 24, all refinement cases, the selftest and the real arm.
3. **M-echo-output.** Change line 223 to `'non_author':receipt['non_author']`.
   - It survives every retained arm: on matched receipts the two values are equal, and `non-author-counter` still exits 1 through line 215 without asserting the emitted value.
   - This is false provenance: the output count would be the receipt's claim, not the recomputation.
4. **Glob-engine gap (not a current defect).** No synthetic arm uses a wildcard glob; the fixture's literal `non-author.txt` makes every glob engine agree.
   - At measured revision `9fb1f911`, the real globs `corpus/lessons/round-*-verifier-spotcheck.md` and `corpus/lessons/operator-*.md` match the same 7 tracked paths under `fnmatch` and `PurePath.match`. I verified this on path names only.
   - So a `PurePath.match` mutant of line 203 survives all retained evidence.
   - An exact-equality mutant (`path in patterns`) would be killed only by the real arm (0 vs 5), not by the frozen 24.

The measure1 mutation set (`measure-round22.py:77-82`) contains none of M1–M4. Its `kill_basis` is the frozen-24 oracle only, so the "all killed" claim (`summary.json` `all_killed_and_restored`) does not cover R12's branches.

## Missing same-command red control

The control should use the oracle's own `check --repo F --rev REV --receipt receipt.json --policy policy.json --allowlist allowlist.json` command, against a fixture that differs from `valid` only in the receipt's non-author accounting.

| Arm | Receipt change | Expect |
|---|---|---|
| `non-author-lie` | `non_author` 1→2 (or 0) | exit 1, `RETENTION_RECONCILIATION_MISMATCH`, `differences`==[`non_author`], emitted `non_author`==1==`policy_excluded`, `policy_excluded_hits`==`expected_policy_hits`, `raw_total` 5 |
| `bool-non-author` | `non_author` `true` | exit 2, `error`==`receipt_counter_type`, sanitized keys only |
| `wildcard-non-author` | policy glob `notes/*-na.md`, plus a tracked `notes/deep/x-na.md` hit and a `nested/notes/x-na.md` hit; receipt built with gate (`fnmatch`) semantics | exit 0. This separates `fnmatch` (`*` crosses `/`, both ends anchored) from `PurePath.match`. |

## Impacted axes

- **Calibration:** "24/24 after" overstates R12's fail-capability. Under M1–M3 the R12 pass is the same as R01's.
- **Depth:** the mutation coverage misses B5–B7.

There is no regression to operability or freshness, and no privacy implication: `privacy_clearance` is hard-coded false at lines 225 and 273, and the real arm stays red at 4.

## Smallest safe correction

This is a fixable defect in evidence, not a tradeoff for the judge. Do not edit the SUT, because its source already holds. Do not rewrite the frozen v2 files or the measure1 evidence.

1. Append the three arms above to `refinement-reconcile.py`, labeled post-implementation co-evolved controls rather than frozen requirements.
2. Strengthen the `non-author-counter` predicate with `differences==['non_author']` and emitted `non_author==1`.
3. Add M1–M3 to the measure mutation set, with kill basis `refinement`.
4. Record R12 as "holds; frozen proof is count-only and shares the `valid` exit gate" until a pre-implementation v3 freeze adds an R12-specific red arm.

No tools were installed or updated.
