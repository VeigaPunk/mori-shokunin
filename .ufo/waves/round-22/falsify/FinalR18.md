# FinalR18 — falsification of R18 "bool line/metric reject2"

Seat MoriR22.FinalR18 (critic). Static review only: nothing executed, no tests, builds, selftests, oracle or tool runs, no installs, no production edits, no delegation. The only commands run were read-only `ls`, `sha256sum`, `git log/diff --stat` and `jq` field projections over retained measure1 evidence (exit codes, finding/error tokens, hit path/line/class only; no matched text).

## Verdict

- **R18 holds at the shipping SUT's branch level.** Both bool arms are rejected by a strict type branch with exit 2 and a sanitized token, and type validation happens before any comparison.
- **The frozen oracle's R18 row is reason-agnostic.** It asserts only exit 2, `RETENTION_RECONCILIATION_SETUP` and empty stderr. It never asserts *which* setup branch fired, so any upstream setup failure would also pass R18.
- **The line arm uses a non-colliding value**, so it cannot kill a realistic bool-lax line validator.
- **No same-command red control exists for R18.** No mutant run through the same oracle command has ever turned R18 red.

This is an evidence/calibration defect, not a shipping-SUT defect, and it is fixable without touching frozen bytes.

## Inputs verified (current bytes, not prior notes)

| File | sha256 | Pin |
|---|---|---|
| `tools/mori-retention-reconcile.py` | `d6870fb6…0ce7` | equals measure1 `summary.tool_sha256`; last change 3985b3d; no worktree diff |
| `oracle-reconcile-v2.py` | `dcd1c7c6…8adb` | equals `requirements-v2.json` `oracle_sha256` |
| `frozen/fixture-builder-v2.py` | `1b3e16f7…15d1` | equals `fixture_builder_sha256` |
| `contract.md` / `denominator-correction.md` | `1658c390…21a1` / `968945b2…24f9` | equal pins |

The denominator correction (policy_excluded is the non-author-glob identities) does not change the meaning of R18.

## Branch-level trace in the shipping SUT

`integer(value)` (line 33-34) is `type(value) is int and value>=0`, so `True`/`False` are rejected.

1. **bool-line** (fixture line 85 sets `result['hits'][0]['line']=True`).
   - Every earlier gate passes for this fixture: resolve, committed blobs, wrapper schema, measured OID, ancestry, policy/allowlist byte equality, policy and allowlist rows, `exit_code` 1, empty stderr, argv repo/path/rev binding, inner commit, policy digest, and int counters at line 187.
   - It then fails at `normalize_hits` line 124 → `Invalid('receipt_hit_type')` → exit 2.
2. **bool-metric** (fixture line 86) fails at line 187 → `receipt_counter_type` → exit 2.
3. **Precedence.** All receipt type checks (lines 167-191) run before `scan` (line 195) and the comparison (lines 211-218). A bool that is also numerically wrong therefore exits 2, not 1.
4. **Other integer sites are strict too:** wrapper `exit_code` (line 167), `routed`/`non_author` (line 187), `line` in `unallowlisted_hits`/`allowlisted_hits` (line 189), and auxiliary `line` must be `None` (line 132). Duplicate JSON keys cannot hide a bool, because the `no_duplicates` hook (lines 36-41) rejects them.
5. **Retained corroboration** (L1-authored measure1, same tool sha; this is not outside verification): bool-line returned `receipt_hit_type`, bool-metric returned `receipt_counter_type`, and both exited 2 with empty stderr. The refinement runner also bound `receipt_exit_type` (boolean-exit) and `receipt_counter_type` (boolean-routed, a colliding `False`==0).

## Counterexamples against the R18 evidence

**C1 — the line arm does not collide.**
- Fixture `hits` keep dict order (policy.json first), and retained raw_hits put the policy.json hit at line 13. The bool-line arm therefore replaces 13 with `true`.
- A uniformly lax SUT (`isinstance(int)`) returns 1 (MISMATCH: `hits` and `allowlisted_hits` differ, because `allowlisted_hits[0]` is the same dict object and also serializes as `true`), not 0. The arm never exercises the dangerous `True==1` false-RECONCILED case. This contradicts the prior AttackR18 guidance it was meant to implement ("must use a colliding value").

**Smallest counterexample: a "type-check only on mismatch" line validator** that passes the whole frozen 24.
- The mutant compares first. Only when there are differences does it strict-type the hit lines, to choose 2 over 1. Counters stay strict.
- Frozen results:
  - bool-line (13→`true`): differences found, then bool found → 2. **R18 passes.**
  - bool-metric: counter strict → 2. The conjunctive arm passes.
  - R08 line lie: int, so → 1. R19 duplicate → 2. Every other row is unchanged.
- Uncaught false green: a receipt with `true` in place of the line-1 hit `unallowed.txt` (in both `hits` and `unallowlisted_hits`) gives Counter equality → **exit 0 RECONCILED**.
- The shipping SUT is not this mutant: line 124 types unconditionally before comparison. The frozen evidence simply cannot tell the two apart.

**C2 — the row is reason-agnostic.**
- Oracle lines 40-45: R18 checks exit, finding and stderr only. Lines 56-57: the conjunctive bool-metric arm checks only exit and finding. It does **not** check stderr, does not check `receipt_match is False` or `privacy_clearance is False`, and has no result row of its own.
- R18 is not conjunctively bound to its paired control R01, which is a different fixture, repo path and rev. Its pass is therefore attributable to any setup branch. Example: run the oracle with a relative `--output`. The fixture wrapper argv then records a relative `--repo`, and every arm exits 2 `receipt_repo_binding` (SUT line 176). The R18 row reads `pass:true` even though R01 fails.
- The aggregate stays red in that case, so this mislabels a row rather than producing a false overall green. measure-round22 passes absolute paths.

## Missing same-command red control

- measure-round22 has four mutations: count-only, false-clearance, wrong-population and setup-leak. None touches R18.
- Retained evidence confirms the frozen R18 row is `pass:true` in **all four** mutant observations. R18 has therefore never been shown fail-capable under the same `oracle-reconcile-v2.py --tool <mutant> --requirements … --output …` command.
- The refinement runner has bool controls for exit and routed with bound error tokens, but no bool `line` case and no bool `metric`/`non_author` case.

## Impacted axes

- **Calibration** (the claim axis): R18's pass overstates what was demonstrated. The bool-collision guarantee on `line` is shown only by source reading and retained tokens, not by a fail-capable black-box arm.
- **Exit-taxonomy correctness:** whether setup-versus-mismatch precedence holds for colliding values is untested.
- No privacy or leakage impact: setup output is the sanitized 5-key object.

## Smallest safe correction (append-only; frozen bytes unchanged)

1. **Add a same-command red control** to the measure-round22 `mutations` list: `('bool-lax',[("return type(value) is int and value>=0","return isinstance(value,int) and value>=0")])`. The old string occurs exactly once (line 34).
   - Require the frozen R18 row to be `pass:false`, not just `unmet>0`.
   - Statically predicted under the mutant: bool-line → 1, bool-metric → 0 (`True==1`), so R18 goes red and no other row changes.
2. **Add co-evolved refinement cases** with a bound `error`:
   - `boolean-line-colliding`: set `line` to `true` on the `unallowed.txt` line-1 hit in both `value['hits']` and `value['unallowlisted_hits']`. They are separate dicts after `json.loads`, so both must be set. Expected: 2, `receipt_hit_type`. The lax mutant would return 0.
   - `boolean-metric`: expected 2, `receipt_counter_type`.
   - `boolean-non-author`: set `non_author` to `true` (true value 1). Expected 2, `receipt_counter_type`.
   - Optional: auxiliary `line:false` in the forbidden fixture. Expected 2, `receipt_auxiliary_type`.
3. When reporting R18, attribute the result through the bound error tokens and the paired clean-control from the refinement run in the same measurement. Do not rely on the frozen row alone.

## Installs

None.
