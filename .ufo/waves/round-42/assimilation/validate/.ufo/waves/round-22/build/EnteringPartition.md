# EnteringPartition — r21 entering vs final retention receipt (read-only scout)

Seat `MoriR22.EnteringPartition`. Detection/report only. No tests, builds, gates, or retention scans were run; the two receipts were **not** recomputed. Everything below is (a) parsing of the two committed receipt files, (b) read-only `git -C` plumbing (`rev-parse`, `merge-base --is-ancestor`, `log`, `rev-list --count`, `diff --stat/--name-only`, `cat-file blob`, `status --porcelain`), and (c) reading `tools/mori-retention-gate.py` source. No matched text is reproduced; identities are path/line/class plus truncated digests already present in the receipts. No tools installed or updated.

Files compared (both committed only in `77a5bbe8a0b41dfbfd2546d024d36e294b814bd0`, clean in worktree at HEAD `306e06ecd02e…`):

| | entering | final |
|---|---|---|
| file | `.ufo/waves/round-21/evidence/final/retention-floor-entering.json` | `.ufo/waves/round-21/evidence/final/retention-floor.json` |
| file sha256 | `878991395ec4f0e89364377009748b25ec55993934e016fbf049955228696f72` | `4001e2d94afcc652b710d5d0afe63bffce2185256f120d5a5f7d33de6be8c840` |
| bytes | 33050 | 33050 |
| started_utc | 2026-10-21T13:31:46.908250Z | 2026-10-21T13:31:10.468960Z |
| elapsed_seconds | 8.324 | 8.779 |

## 1. Shape — OBSERVED identical

- Wrapper keys are identical in both: `argv, cwd, elapsed_seconds, exit_code, measured_revision, schema, started_utc, stderr, stdout`. Schema `mori-r21-command-receipt-v1`, `exit_code` 1, `stderr` empty, cwd identical.
- The `stdout` JSON keys are identical in both: `allowlisted_hits, commit, finding_id, forbidden_allowlist, hits, metric, non_author, policy_sha256, routed, unallowlisted_hits, warnings`.
- Neither receipt records an allowlist sha256, the executing gate's sha256, or the resolved input revision separately from argv. Round-22 contract R24 requires these provenance bindings, and the r21 wrapper does not carry them.

## 2. Revision — OBSERVED binding defect in the entering receipt; NOT the same revision

| field | entering | final |
|---|---|---|
| wrapper `measured_revision` | `9fb1f911cfdd6061005c300795f44b1b45523897` | `9fb1f911cfdd6061005c300795f44b1b45523897` |
| argv `--rev` | `e9f340ce986f82a60baad1b8e5ead655ab818a1c` | `9fb1f911cfdd6061005c300795f44b1b45523897` |
| stdout `commit` | `e9f340ce986f82a60baad1b8e5ead655ab818a1c` | `9fb1f911cfdd6061005c300795f44b1b45523897` |

- **Entering receipt is self-inconsistent.** Its wrapper `measured_revision` names `9fb1f911`, but the scan it wraps actually ran on `e9f340ce` (both argv and stdout `commit`). The final receipt is internally consistent. The entering run also started 36 s *after* the final one, so the "entering" label is not reflected in time order. [INFERENCE] The wrapper stamped the then-current measurement revision rather than the scanned `--rev`.
- Git plumbing: `e9f340ce` is a strict ancestor of `9fb1f911`; the reverse is false. Both are ancestors of the round-22 entering branch `77a5bbe8`. There are 8 commits in `e9f340ce..9fb1f911`. The trees differ (`bfb6ad1b…` vs `fbba387a…`), with 120 files changed, 11799 insertions and 8 deletions. Commit subjects: `e9f340ce` "round-20: late wave-2 seat reports"; `9fb1f911` "round-21: integrate residual falsifiers and bind final measurement inputs".
- Consequence for the round-22 reconciler: the contract reads only `measured_revision` from the wrapper. Fed the entering receipt, a reconciler would recompute at `9fb1f911` while the receipt's own stdout `commit` says `e9f340ce`. The contract does not say whether `measured_revision` ≠ argv `--rev` ≠ stdout `commit` is a SETUP (2) or MISMATCH (1) outcome. That is an **open contract gap**: no R-ID covers a wrapper/stdout revision disagreement (R13 covers only a mismatched or unresolvable measured revision versus the input). [INFERENCE] Because the hit multisets happen to be identical (section 3), a reconciler that ignores stdout `commit` would report this entering receipt as RECONCILED against the wrong tree. That would be a false agreement.

## 3. Counts and identities — OBSERVED identical multisets despite different trees

Hit identity = (path, line, class, line_sha256). Neither receipt has duplicate identities in any list.

| measure | entering | final |
|---|---|---|
| `hits` | 95 | 95 |
| `allowlisted_hits` | 86 | 86 |
| `unallowlisted_hits` (= `metric`) | 4 | 4 |
| `non_author` | 5 | 5 |
| `forbidden_allowlist` / `warnings` / `routed` | 0 / 0 / 0 | 0 / 0 / 0 |
| `finding_id` | RETENTION_FINDINGS | RETENTION_FINDINGS |
| distinct hit paths | 32 | 32 |
| hits multiset sha256 (sorted JSON of tuples) | `cbe7d2a6…` | `cbe7d2a6…` |
| allowlisted multiset sha256 | `8396c403…` | `8396c403…` |
| unallowlisted multiset sha256 | `c5f9e790…` | `c5f9e790…` |
| hits by class | R2:3 R4:8 R5:14 R6:37 R7:10 R8:8 R9:15 | same |

- In each list, the multiset difference between entering and final is 0 in both directions. The `stdout` strings differ only in the `commit` key.
- [INFERENCE, not recomputed] None of the 120 files changed between `e9f340ce` and `9fb1f911` adds or removes a hit under the frozen policy; within `corpus/lessons`, only `round-21.md` changed. Identical receipt outputs are not evidence that the two revisions are identical, and a scan of only one of them cannot stand in for the other.

## 4. Partition — OBSERVED: 95 = 86 allowlisted + 4 unallowlisted + 5 non-author

- The allowlisted list (A) and unallowlisted list (U) are disjoint, and both are subsets of the hits (H). **A ∪ U ≠ H**: 90 of 95. The remaining 5 hits are exactly the hits that match the policy's `non_author_paths_glob` (2 globs, which match all 5 remainder hits and 0 hits in A or U):
  - `corpus/lessons/round-17-verifier-spotcheck.md`: L312 R9, L315 R6, L341 R6
  - `corpus/lessons/round-18-verifier-spotcheck.md`: L60 R5, L60 R6
- Gate semantics (`tools/mori-retention-gate.py` `_scan_result`, lines 260–267): `unallowlisted` excludes non-author hits and allowlisted keys. `allowed_hits` does **not** exclude non-author hits, so A and the non-author set can overlap in general (here they don't). The allowlist key is (path, class, line_sha256) **without line**, so one allowlist row covers every same-digest line in a file. The round-22 reconciler must reproduce both behaviours.
- Therefore the **95 vs 90 gap equals the 5 non-author exclusions, not policy-source hits** in these receipts.

## 5. Policy membership — OBSERVED: 4 exact-path policy hits, all allowlisted; 4 copy-path hits are the unallowlisted

- Exact frozen policy path `.ufo/waves/round-18/frozen/c1-policy.json` has **4** hits (L8 R2, L11 R5, L12 R6, L14 R8), all in A. Its digests start with `8d92bfa3`, `7f23448e`, `0cdc8972` and `1d2b6e6e`.
- The 4 unallowlisted hits are the same four (line, class, digest) tuples, at the copy path `.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json`. This agrees with `corpus/lessons/round-21.md` L141: "red4→4 at identical inherited synthetic-policy copy lines".
- **Discrepancy with the round-22 open-debt statement** "raw95 includes5 policy source hits, scanner90": neither receipt supports 5 policy-source hits. Under the contract's exact-supplied-path rule, `policy_excluded` = 4 and the scanner-compatible total = 95 − 4 = **91**, not 90. The figure 90 equals A + U (95 − 5 non-author). If the copy path were also excluded, that would be a broad path exclusion, which the contract forbids, and it would give 87. The "5 / 90" figures look like a conflation of the non-author exclusion count with policy-source membership. [INFERENCE] I did not locate the "scanner" source of 90: no other file in `round-21/evidence/final/` matches `scanner|policy_excluded|raw_total|95|90|non_author`, and `round-21.md` does not mention them. L1 should re-derive R03/R04 expected values and the debt line from identities rather than reuse 5/90.
- Expected values for the real retained receipt (`9fb1f911`), derived arithmetically from the receipt identities and not measured: raw_total 95, policy_excluded 4, scanner_total 91, raw_unallowlisted 4, scanner_unallowlisted 4 (the copy path is not excluded), non_author 5, forbidden_allowlist 0, retention_state red, privacy_clearance false.

## 6. Input identity across revisions — OBSERVED unchanged

| blob at | `e9f340ce` | `9fb1f911` | `77a5bbe8` |
|---|---|---|---|
| `tools/mori-retention-gate.py` | `988c5484…` | `988c5484…` | `988c5484…` |
| `.ufo/waves/round-18/frozen/c1-policy.json` | `8bf285bd…` | `8bf285bd…` | `8bf285bd…` |
| `corpus/evidence/retention-allowlist.json` | `f8be55b1…` | `f8be55b1…` | `f8be55b1…` |

- The policy blob sha256 at both revisions is `db06e9810bbfd243fb0a753a46960573df39083ea90174ce463cf2a0ab523128`, which equals the `policy_sha256` in both receipts. The allowlist blob sha256 at both revisions is `f46c78ecad4c6d31fa9ac0ba0cfd6c72eb9137ab6b58ab4baf4239d11ea0c63b` (28354 bytes). All three paths are clean in the worktree at HEAD.
- Caveat: both receipts' argv passed **worktree absolute paths** for policy and allowlist, not git blobs. The receipt binds the policy sha256 but not the allowlist bytes at run time, so equality between the run-time allowlist and the blob is [INFERENCE], not observed. R15/R16 would pass for the `e9f340ce`→`9fb1f911` pair (same bytes).

## Confidence and remaining unknowns

- High confidence: receipt shapes, revision fields, ancestry, multiset equality, partition arithmetic, exact-path policy count of 4, and gate partition semantics. All come from direct parsing, plumbing and source reading.
- Not run or unknown: no recomputation of either tree, so whether `e9f340ce` and `9fb1f911` truly yield identical hits is only implied by the receipts. The origin of the "5 policy / scanner 90" figures is unknown. The run-time allowlist bytes are unbound. Privacy clearance remains false; a matched or identical receipt is not clean retention. The R21 original permission control stays RED 11/12, both historical dispositions stay unknown, and baseline acceptance stays blocked.
- Recommended contract additions for L1: (1) require wrapper `measured_revision` == argv `--rev` == stdout `commit`, or fail with SETUP (2); add an R-ID and use this entering receipt as a real-world negative. (2) Correct R03/debt expectations from 5/90 to identity-derived 4/91 for the retained receipt, or else locate the scanner population that yields 90.
