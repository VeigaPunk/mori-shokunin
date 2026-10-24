# AttackR06 — R06 "injected receipt hit returns1"

Seat MoriR22.AttackR06. Static review only; nothing executed except read-only metadata inspection of the r21 receipt (path/line/class/count fields only, no line text). No tests, builds or installs. No Impl/Fixture/Oracle candidate existed under `.ufo/waves/round-22/build/` or `.scratch/round22/` at review time, so this attacks the contract text plus the existing gate (`tools/mori-retention-gate.py`) and receipt shape (`round-21/evidence/final/retention-floor.json`).

## Axes
- A1 detection: an injected identity must be caught by multiset identity comparison, not counts, partitions or ordering.
- A2 attribution: exit 1 must come from the reconciliation verdict, not a crash, a formatting difference or an unrelated provenance check.
- A3 exit-class separation: R06 (exit 1) vs R19 duplicate (exit 2) vs schema/type failure (exit 2).
- A4 raw authority: an injection on the policy path or a non-author path must still count as a mismatch.
- A5 no clearance or leakage: privacy_clearance stays false and no line text is emitted.

## Observed receipt facts that the attack relies on
- Wrapper keys: `argv, cwd, elapsed_seconds, exit_code, measured_revision, schema, started_utc, stderr, stdout`. `stdout` is `json.dumps(sort_keys=True, separators=(",",":"))+"\n"` (gate `emit`, line 46).
- Retention keys: `allowlisted_hits, commit, finding_id, forbidden_allowlist, hits, metric, non_author, policy_sha256, routed, unallowlisted_hits, warnings`. Each hit has exactly `class, line, line_sha256, path`.
- The gate builds the allowlist as a **set of (path, class, line_sha256)** with no line number (gate lines 235–266). Partitions therefore collapse identical line contents at different line numbers.
- In the real receipt there are 0 duplicate 4-tuples among the hits, and the hits are emitted in sorted order.

## Strongest counterexamples (superficial-pass risks)
1. **A crash passes as R06.** An uncaught Python exception exits with code 1, the same code as MISMATCH. An oracle that checks only the exit code passes a crashing implementation. The oracle must also require stdout to be exactly one JSON object with `finding_id == "RETENTION_RECONCILIATION_MISMATCH"`, and stderr to be empty or contain no traceback.
2. **Exit 1 for the wrong reason.** If the mutated receipt is re-serialized differently, or the base receipt does not reconcile, exit 1 proves nothing. The unmutated base receipt G must return 0 in the same selftest run. Each R06 arm must change only the hit lists and counters, and must be re-serialized with the gate's exact canonical form (sort_keys, `(",",":")` separators, trailing `\n`).
3. **Comparing only the scanner population misses a policy-path injection.** This round introduces a scanner denominator that excludes the policy path. An implementation that diffs only scanner identities passes the R03/R04 arms but accepts a forged hit on the policy file.
4. **Comparing only partitions or counters misses non-author and allowlisted injections.** An injection on a non-author path leaves `metric`, `unallowlisted_hits`, `finding_id` and `exit_code` unchanged. An injection on an allowlisted path at a new line, with the same (path, class, sha), lands in `allowlisted_hits` and also leaves `metric`, `finding_id` and `exit` unchanged. Comparison by allowlist-key set (the gate's own semantics) collapses it and misses it.
5. **A self-consistent forgery.** An attacker updates every list, counter, finding and exit coherently. Only an independent recomputation catches this. A reconciler that checks receipt internal consistency first and then trusts the counts passes it.
6. **A tautological oracle.** If expected values are computed at selftest time by the reconciler's own recompute function, or by calling the existing gate, the check proves nothing. Expected values must be committed literals (the contract's commit-before-integration rule).

## Concrete fixture (synthetic git repo, one commit C)
Files (UTF-8, LF line endings; the policy is serialized with `json.dumps(indent=2)` so that each key sits on its own line):
- `policy.json`: schema `mori-retention-policy-v1`; classes `[{"id":"R6","regex":"SYNTH_TOKEN_[0-9]+"}]`; `must_redact_paths ["redact/forbidden.md"]`; `non_author_paths_glob ["vendor/*"]`; plus a key `"example": "SYNTH_TOKEN_9"`. This gives exactly 1 hit on the policy path. The regex line itself does not match, because `[` follows the underscore.
- `allow.json`: one row `{path:"docs/a.md", class:"R6", line_sha256:sha256("SYNTH_TOKEN_1"), reason:"synthetic", rule:"a"}`.
- `docs/a.md`: `x` / `SYNTH_TOKEN_1` / `y` / `SYNTH_TOKEN_1`. This gives 2 hits on lines 2 and 4, both allowlisted.
- `src/b.py`: `a = 1` / `SYNTH_TOKEN_2` / `b = 2`. This gives 1 unallowlisted hit.
- `vendor/c.txt`: `SYNTH_TOKEN_3` / `z`. This gives 1 non-author hit.

Recomputed literals for commit C: raw_total=5, policy_excluded=1, scanner_total=4, non_author=1, forbidden_allowlist=0. raw_unallowlisted=2 (policy.json line N, plus src/b.py line 2). scanner_unallowlisted=1 (src/b.py line 2). retention_state=red, privacy_clearance=false.

G is the gate-shaped receipt for C: `metric 2`, `finding_id RETENTION_FINDINGS`, `exit_code 1`, 5 hits, 3 allowlisted, 2 unallowlisted. Expected result: exit 0, RETENTION_RECONCILED, receipt_match=true. G is committed as a literal.

### R06 arms
Every arm is G plus one injection, with the gate partitions and counters updated coherently. The injected `line_sha256` is the digest of a *real, non-matching* line at that path and line, so a check that the digest exists in the file cannot detect it. The hit is inserted at its sorted position. It has exactly 4 fields and uses known class `R6`.

| Arm | Injected hit (path, line, line text hashed) | Receipt fields changed | Expected exit | Expected finding |
|---|---|---|---|---|
| A author | `src/b.py`, 3, `b = 2` | hits, unallowlisted_hits, metric 2→3 | 1 | RETENTION_RECONCILIATION_MISMATCH |
| B policy path | `policy.json`, 1, `{` | hits, unallowlisted_hits, metric 2→3 | 1 | RETENTION_RECONCILIATION_MISMATCH |
| C non-author | `vendor/c.txt`, 2, `z` | hits, non_author 1→2 | 1 | RETENTION_RECONCILIATION_MISMATCH |
| D allowlist collapse | `docs/a.md`, 3, but with sha256(`SYNTH_TOKEN_1`) | hits, allowlisted_hits | 1 | RETENTION_RECONCILIATION_MISMATCH |
| A′ partial | as in A, but `hits` only; partitions and metric left unchanged | hits | 1 | RETENTION_RECONCILIATION_MISMATCH |

Required counters on every arm: the reported raw_total, policy_excluded, scanner_total, raw_unallowlisted, scanner_unallowlisted and non_author equal the recomputed literals above, not the receipt's values. In addition: receipt_match=false, privacy_clearance=false (JSON boolean), retention_state=red, a receipt-extra-identity count of 1, a receipt-missing-identity count of 0, and stdout containing no fixture line text (no `SYNTH_TOKEN_`, `b = 2` or `z` as a value). Arm B must still report policy_excluded=1 and scanner_total=4, with the extra identity attributed to the raw population. Arm C must report non_author=1. Arm D must not return 2: its 4-tuple is not a duplicate, so it must not be classified under R19.

Recommended additional arms (beyond the frozen wording, but they close the count-only hole the contract's root lesson names):
- **E, count-preserving swap.** Drop the policy.json hit and inject arm A's hit. Every count, `metric`, `finding_id` and `exit` stays identical. Expected: exit 1, extra=1, missing=1.
- **F, order control.** Take G with `hits`, `allowlisted_hits` and `unallowlisted_hits` permuted, then re-serialized canonically. Expected: exit 0 under the contract's multiset semantics. This proves that arms A–D are detected by identity rather than by list-position equality.

## Semantic ambiguities L1 must pin before freezing expected values
1. **Is an internally inconsistent but well-typed receipt exit 1 or exit 2?** This is arm A′. The contract says both "validate lists/counts … against independent recomputation" and "required field/type/schema inconsistencies must fail closed". Recommended pin: exit 2 only for shape, type or format failures (missing required key, wrong JSON type, bool used as int, non-hex sha, non-4-field hit, duplicate 4-tuple). Every well-typed disagreement, including internal count inconsistency, is exit 1.
2. **Does a hit-level unknown field or unknown class count as injection (1) or schema failure (2)?** The gate's `_normalize_hit` requires exactly 4 fields but does not validate the class. The R06 primary arms avoid this by using exactly 4 fields and a known class. The edge cases should be pinned separately.
3. **Is a hit path that is absent from the tree, or a line beyond end of file, injection (1) or invalid path (2)?** The contract's "invalid path" refers to the CLI input paths. Recommended pin: a syntactically valid receipt hit path that does not exist at the measured revision is exit 1.
4. **Is multiset or list order authoritative?** Pin it with arm F.
5. **Exit precedence when an injection coexists with a duplicate (R19).** Recommended: a setup failure (2) takes precedence over a mismatch (1).

## Smallest safe correction (actionable criterion)
R06 passes only if, in one isolated selftest run, all of the following hold:
- G returns 0 with RETENTION_RECONCILED.
- Each of arms A, B, C, D and A′ returns exit 1, emits exactly one JSON object on stdout with `finding_id=="RETENTION_RECONCILIATION_MISMATCH"`, and produces no traceback on stderr.
- Each arm's recomputed counters equal the committed literals (raw_total 5, policy_excluded 1, scanner_total 4, raw_unallowlisted 2, scanner_unallowlisted 1, non_author 1), with receipt_match=false, privacy_clearance=false, extra=1 and missing=0.
- No fixture line text appears in stdout.
- All expected values are committed constants, never derived from the reconciler or the gate at run time.

Adding arms E and F is recommended to make the identity-based detection falsifiable.

## Out-of-R06 flag for L1 (do not act from this seat)
The r21 receipt metadata at measured revision `9fb1f911…` shows **4** hits on the exact policy path `.ufo/waves/round-18/frozen/c1-policy.json`, not 5. Another 4 hits sit on the copy at `.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json`, and those 4 are the real unallowlisted hits. The receipt's `non_author` count is 5, and 95−5=90.

So the contract's statement that the 95 raw hits include 5 policy-source hits and 90 scanner hits matches raw minus non-author, not raw minus the exact policy path. Under the contract's own definition, where only the supplied policy path is excluded, the real scanner_total would be 91. The figure 4 unallowlisted is unaffected, because policy-path hits are allowlisted. This affects R02/R03/R04 and the claim narrative (calibration axis). It is a counterexample to the round's narrative, not to R06.

Installs: none.
