# AttackR18 — frozen R18 "bool line/metric reject2"

Seat: MoriR22.AttackR18 (critic, static review only). Nothing was executed, installed or measured: no tests, selftests, builds or tool runs. The only commands run were read-only Python one-liners that printed field types and counts from the r21 receipt; no matched text was printed. No candidate `tools/mori-retention-reconcile.py` exists in the repo or under `.scratch/round22`. The Impl, Fixture and Oracle seats are registered but have produced nothing readable. I did not wait for them.

## Requirement as frozen

From the contract (`contract.md`): "R18 bool line/metric reject2". The general clauses also say "Explicit booleans not accepted as ints", "required field/type/schema inconsistencies must fail closed", and "Exit1 … valid receipt disagrees". Exit 2 is the setup exit for invalid types or schema.

## Where integers appear in the receipt (observed in r21 `retention-floor.json`, types only)

| Site | r21 value | Python bool collision |
|---|---|---|
| wrapper `exit_code` | int 1 | `True == 1` and `hash(True) == hash(1)` |
| stdout `metric` | int 4 | only if the true value is 0 or 1 |
| stdout `routed` | int 0 | `False == 0`, so it collides on real r21 data |
| stdout `non_author` | int 5 | only if the true value is 0 or 1 |
| `line` in `hits` (95), `unallowlisted_hits` (4), `allowlisted_hits` (86) | int; r21 has no line-1 hit | collides only when line == 1 |
| `line` in `forbidden_allowlist` / `warnings` rows | always `null` (gate lines 241-258) | `False != None`, but this is still a type defect |

The receipt stdout is JSON stored inside a string (`stdout`: str), so bool injection happens one parse level down. Validating only the wrapper does not cover it.

## Strongest counterexample (bool collision, superficial implementation exits 0)

The trap: Python treats `True`/`False` as `1`/`0` for `==`, `hash`, `Counter`, `set`, `sorted` and `int()`. An implementation that compares receipt hits as `Counter((path, line, class, sha))` tuples, or compares counters with `==`, accepts a receipt whose values are bools when the integers are 1 or 0. The existing gate already has this pattern. `_load_population` (`tools/mori-retention-gate.py` line 221) compares `summary != _population_summary(...)` with plain dict equality, so `{"hits": true}` equals `{"hits": 1}`. An implementation that copies that idiom inherits the defect. In contrast, `_normalize_hit` (lines 110-118) correctly excludes bool for `line`, which is the pattern to reuse.

Fixture F18 is a synthetic one-commit repo using the frozen c1 policy:
- `a.txt`: the first line matches exactly one policy class. No other tracked file produces hits. The path is not in `must_redact_paths` and does not match `non_author_paths_glob`.
- The allowlist is an empty array. The policy and allowlist blobs are identical at the target and input revisions, and the input revision is the target revision or a descendant.
- The valid receipt V (`mori-r21-command-receipt-v1`) has: hits = [line 1], unallowlisted_hits = [that hit], allowlisted_hits = [], metric 1, routed 0, non_author 0, forbidden_allowlist [], warnings [], wrapper exit_code 1, and finding_id RETENTION_FINDINGS.
- Control arm: V returns exit 0 with RETENTION_RECONCILED, raw_total 1, policy_excluded 0, scanner_total 1, raw_unallowlisted 1, scanner_unallowlisted 1, non_author 0, forbidden_allowlist 0, receipt_match true, retention_state red, and privacy_clearance false.

Each mutant is V with exactly one value changed. The stdout is re-serialized, re-wrapped and committed as a new receipt blob.

| Arm | Mutation | Naive implementation | Required |
|---|---|---|---|
| R18a | `line` 1 → `true` in both `hits[0]` and `unallowlisted_hits[0]` | 0, RECONCILED | 2, RETENTION_RECONCILIATION_SETUP |
| R18b | `metric` 1 → `true` | 0 | 2, SETUP |
| R18c | `routed` 0 → `false` | 0 | 2, SETUP |
| R18d | `non_author` 0 → `false` | 0 | 2, SETUP |
| R18e | wrapper `exit_code` 1 → `true` | 0 | 2, SETUP |
| R18f (ordering) | `metric` 1 → `false` (numerically wrong and wrongly typed) | 1, MISMATCH | 2, SETUP |
| R18g (null-typed line) | in a variant of the R11 forbidden-allowlist fixture, `forbidden_allowlist[0].line` null → `false` | 1 or 0 | 2, SETUP |

Optional real-data arm, run by L1 only: copy r21 `retention-floor.json` into a fixture or scratch location, set `routed` to `false` and `exit_code` to `true`, and leave the original evidence byte-unchanged. The required result is exit 2. The unmutated copy keeps its R02 expectation of exit 0 with privacy_clearance false.

## Exact actionable criterion (for the Oracle and the selftest)

1. Before any comparison, every required integer field must satisfy `type(x) is int` (or `isinstance(x, int) and not isinstance(x, bool)`), and must also be at least 1 for `line` and at least 0 for counters. The required fields are: wrapper `exit_code`; stdout `metric`, `routed`, `non_author`; and every `line` in `hits`, `unallowlisted_hits` and `allowlisted_hits`. Every `line` in `forbidden_allowlist` and `warnings` must be exactly `None`. Any violation means exit 2 with RETENTION_RECONCILIATION_SETUP. No coercion through `int()`, no comparison with `==`, and no Counter or set built from unvalidated values.
2. Type validation takes precedence over comparison. R18f must return 2, not 1. A mismatch exit requires a valid receipt.
3. Each of R18a through R18f is its own isolated CLI subprocess arm. Each one asserts the exact exit code (2), `finding_id == "RETENTION_RECONCILIATION_SETUP"`, and an error code that is a fixed sanitized token. That token must differ from the R17 malformed-JSON code, so a mutant broken in some other way cannot pass for the wrong reason.
4. Each arm also asserts three more things. First, receipt_match is never true. Second, privacy_clearance, if emitted, is exactly JSON `false` (`is False`, not `0`). Third, stdout contains no receipt bytes, hit lists or exception text.
5. Fixture integrity: the generator asserts that V and each mutant differ in exactly one JSON value. It also asserts that V alone returns 0 in the same selftest run. Without the paired control, a 2 could come from an unrelated setup failure.
6. The emitted counters (raw_total, policy_excluded, scanner_total, raw_unallowlisted, scanner_unallowlisted, non_author, forbidden_allowlist) must themselves be `type is int`. receipt_match and privacy_clearance must be `type is bool`. The oracle checks types, not just `==`.

## Superficial-pass risks

- Testing `line: true` on a hit whose real line is not 1. The tool then exits 1 by mismatch, and any assertion that only checks "nonzero" or "!= 0" passes without exercising R18. The arm must use a colliding value.
- Covering only one site, such as `hits[].line`. `unallowlisted_hits`, `allowlisted_hits`, the counters and the wrapper `exit_code` each need an arm, or a validator shared across all of them plus at least the a/c/e arms.
- Validating the wrapper but not the nested stdout JSON, or the reverse.
- Re-serializing and comparing strings. This catches `true` versus `1` but yields exit 1 (mismatch) instead of 2.
- The selftest counting "R18 covered" from in-process function calls instead of CLI subprocess arms, which the contract rejects.

## Ambiguities (smallest safe resolution)

- "metric" scope: read it as every integer the receipt asserts (wrapper exit_code, metric, routed, non_author), not only the `metric` key. The general fail-closed clause supports this.
- Optional population fields (`population_match` is a legitimate bool, plus `new_hits` and `missing_population_hits`) are absent from the r21 receipt. Unknown fields need not be rejected. If an implementation validates them, it must not reject a legitimate bool in `population_match`.
- `elapsed_seconds` (float) is not a required field in the contract. Leave it unvalidated rather than over-reject.
- Floats such as `line: 1.0` or `metric: 4.0` also compare equal to ints and hash the same. Strictly, R18 covers only bool, but the general clause requires exit 2 here too. I recommend one adjacent control arm, not counted as R18.
- Duplicate JSON keys: `{"line": true, "line": 1}` parses to `1` with plain `json.loads`, so a bool can be hidden. This belongs to R17 and R19. I flag it here only because it can mask R18; the fix is an `object_pairs_hook` that rejects duplicate keys and returns exit 2.
- On exit 2, the contract does not say whether privacy_clearance or the counters are emitted. The safe oracle requires that receipt_match is never true and that privacy_clearance is never true.

## Impacted axes

Calibration, which this round's claim targets: a bool-collision false RECONCILED would overstate the agreement guarantee. Correctness of the exit taxonomy is also affected (setup versus mismatch precedence). No privacy or leakage impact, as long as the error output stays a sanitized token.

## Installs

None.
