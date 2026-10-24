# RequirementTrace — R01–R24 → separate CLI observables (round 22, C1)

Seat `MoriR22.RequirementTrace` (read-only scout). Nothing was run: no tests, oracle, fixture builder, selftest, builds or linters. Every expected value below comes from statically reading committed blobs. Evidence is metadata only: paths, counts, digests and line numbers. No matched text is reproduced, and the synthetic fixture token is not written here. No tools were installed.

## Inputs read (read-only `git -C` plumbing)

| Item | Revision / blob | Fact |
|---|---|---|
| Contract `.ufo/waves/round-22/contract.md` | HEAD `e2f549b`, sha256 `1658c390…21a1` | Equals the `contract_sha256` pinned in both `requirements.json` and `requirements-v2.json`; the worktree equals HEAD |
| Correction `.ufo/waves/round-22/denominator-correction.md` | sha256 `968945b2…24f9` | Equals the `correction_sha256` pin; supersedes "exclusion of the policy source file" |
| `frozen/requirements-v2.json` | HEAD | Lists 24 IDs, `before_kind=capability_absent`, and supersedes `frozen/requirements.json` only for the source-file-exclusion interpretation |
| `frozen/fixture-builder-v2.py` | sha256 `1b3e16f7…15d1` | Equals the pin |
| `oracle-reconcile-v2.py` | sha256 `dcd1c7c6…8adb` | Equals the pin; differs from v1 only on line 13 (which builder it loads) |
| `tools/mori-retention-reconcile.py` | HEAD and worktree | Absent, so "before" is `capability_absent` |
| `tools/mori-retention-gate.py`, `c1-policy.json`, `retention-allowlist.json`, `round-21/evidence/final/` | `77a5bbe` (entering branch) through HEAD | Byte-unchanged (`git diff --quiet` succeeded) |
| Policy blob `8bf285bd`, allowlist blob `f8be55b1` | e9f340ce, 9fb1f911, 77a5bbe | Identical blob IDs at all three revisions |

Governing order: frozen v2 builder and oracle (executable expectations) > correction document > contract text. The contract text still contains the superseded clauses (see contradiction K1).

## Axes

- **A1. Exit code and `finding_id`.** Every arm requires `stderr == ''` and a stdout that parses as exactly one JSON object (oracle line 42).
- **A2. Accounting fields:** `raw_total`, `policy_excluded`, `scanner_total`, `raw_unallowlisted`, `scanner_unallowlisted`, `non_author`, `forbidden_allowlist` (an integer), `retention_state`, `privacy_clearance`.
- **A3. Identity lists:** `raw_hits`, `scanner_hits`, `policy_excluded_hits`. Each element has exactly the four keys path, line, class and line_sha256.
- **A4. Provenance:** `input_revision`, `measured_revision`, `tool_sha256`, `inputs_sha256{receipt,policy,allowlist}`, `argv`.
- **A5. Leakage:** the serialized stdout contains no synthetic token and no fixture line text.

## Synthetic fixture (v2), derived statically

At the measured commit (first commit), the tree contains `policy.json`, `allowed.txt`, `unallowed.txt`, `non-author.txt`, `binary.bin` and `allowlist.json`. The input commit (second commit) adds `receipt.json`.

Expected raw hits:

| Path | Hits |
|---|---|
| `policy.json` | 1 (line 11 in the valid variant) |
| `allowed.txt` | 2 (identical lines, so the same `line_sha256`, giving one allowlist key) |
| `unallowed.txt` | 1 |
| `non-author.txt` | 1 |
| `binary.bin` | 0 (contains NUL, skipped) |

That gives `raw_total` 5. The allowlist has two rows (`policy.json` and `allowed.txt`), both with `rule='b'` (added in v2). Resulting partitions: allowlisted 3, unallowlisted 1, non-author 1, policy-excluded (non-author identities) 1, scanner total 4.

The receipt's `hits` order follows the builder's file-insertion order (policy, allowed, allowed, unallowed, non-author). The gate's `ls-tree` order is path-sorted. Comparison must therefore be by multiset, never by list order or bytes. The receipt's `stdout` uses Python's default `json.dumps` (unsorted keys, spaces, no trailing newline), while the real receipt is compact, sorted, and ends with a newline. Stdout must be parsed semantically.

## Requirement → CLI observable map

All arms use `check --repo <fixture> --rev <input commit> --receipt receipt.json --policy policy.json --allowlist allowlist.json`, unless the arm says otherwise. "valid" means the valid fixture variant.

| ID | Arm (builder variant) | Exit / `finding_id` | Additional observable predicate (oracle-v2 line) |
|---|---|---|---|
| R01 | valid | 0 / RETENTION_RECONCILED | stderr empty (42) |
| R02 | valid | 0 / RETENTION_RECONCILED | `raw_unallowlisted==1`, `scanner_unallowlisted==1`, `retention_state=='red'`, `privacy_clearance is False` (48) |
| R03 | valid | 0 / RETENTION_RECONCILED | `(raw_total,policy_excluded,scanner_total)==(5,1,4)` (49) |
| R04 | valid | 0 / RETENTION_RECONCILED | `scanner_hits` sorted by (path,line) equals the raw hits minus the `non-author.txt` hit (4 dicts, policy.json included); `policy_excluded_hits ==` [the `non-author.txt` hit] (50) |
| R05 | drop (last receipt hit, the non-author hit) | 1 / RETENTION_RECONCILIATION_MISMATCH | — (51) |
| R06 | inject (`injected.txt`, line 1, valid class, zero digest) | 1 / MISMATCH | — (51) |
| R07 | digest (hits[0], the policy.json hit, given a zero digest) | 1 / MISMATCH | — (51) |
| R08 | line (hits[0] line+1) | 1 / MISMATCH | — (51) |
| R09 | class (hits[0] class set to an ID absent from the policy) | 1 / MISMATCH | — (51) |
| R10 | metric (`metric=0`, an integer; exit_code stays 1) | 1 / MISMATCH | — (51) |
| R11 | forbidden (`must_redact_paths=['allowed.txt']`) | 0 / RETENTION_RECONCILED | `forbidden_allowlist==1` (an integer count), `raw_unallowlisted==3`, red, clearance false (52) |
| R12 | valid | 0 / RETENTION_RECONCILED | `non_author==1`, `raw_unallowlisted==1`, `raw_total==5` (53) |
| R13 | invalid-revision (wrapper and stdout commit both set to 40 zeros) | 2 / RETENTION_RECONCILIATION_SETUP | — (54) |
| R14 | diverged (parentless `commit-tree` of the same tree, so the bytes are equal and only ancestry fails) | 2 / SETUP | — (54) |
| R15 | policy-changed (one `\n` appended at the input commit; parsed JSON is equal) | 2 / SETUP | Requires **byte** equality, not parsed equality (54) |
| R16 | allowlist-changed (same as R15, for the allowlist) | 2 / SETUP | Requires byte equality (54) |
| R17 | malformed (receipt blob is not JSON) | 2 / SETUP | — (54) |
| R18 | bool-line (hits[0] line `true`) **and** bool-metric (`metric` `true`) | 2 / SETUP on both | The bool-metric arm is conjunctive in R18 (55–56) |
| R19 | duplicate (hits[0] repeated) | 2 / SETUP | Must be rejected before multiset comparison (54) |
| R20 | `--receipt ../receipt.json` (valid tree) | 2 / SETUP | — (57) |
| R21 | symlink (receipt committed as mode 120000) | 2 / SETUP | Requires an `ls-tree` mode check at `--rev` (58) |
| R22 | valid | 0 / RETENTION_RECONCILED | `raw_total==5`; no `raw_hits` element has path `binary.bin` (59) |
| R23 | valid | 0 / RETENTION_RECONCILED | Serialized stdout contains neither the token nor the fixture line text; clearance false (60) |
| R24 | valid | 0 / RETENTION_RECONCILED | `input_revision==rev`, `measured_revision==` the fixture's measured commit, `tool_sha256==sha256(tool bytes)`, `inputs_sha256` **dict-equal** to exactly the keys {receipt, policy, allowlist}, and `argv` is a list (61) |

The map has 24 IDs and 25 subprocess arms (R18 has two). Each arm is a separate variant directory, except that the valid run is cached and shared by R01–R04, R12 and R22–R24.

## Real retained receipt: proposed L1 measurement arm (not frozen, not run)

No frozen arm exercises the real `retention-floor.json`, but the claim requires that "the real retained result must continue to show four unallowlisted hits". The values below come from the receipt's own claimed hits; they are not an independent recomputation.

- **Command:** `check --repo /home/vgpnk/Projects/shokunin/mori-shokunin --rev <HEAD or 77a5bbe> --receipt .ufo/waves/round-21/evidence/final/retention-floor.json --policy .ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json`
- **Preconditions (observed):**
  - The receipt has schema `mori-r21-command-receipt-v1`, `measured_revision` 9fb1f911, a stdout commit equal to 9fb1f911, and argv `--rev` equal to 9fb1f911.
  - 9fb1f911 is an ancestor of 77a5bbe and of HEAD.
  - The policy and allowlist blobs are identical at both revisions.
  - The policy blob's sha256 prefix `db06e9810bbfd243` equals the receipt's `policy_sha256` prefix.
  - No receipt hit identity is duplicated.
- **Expected:**
  - Exit 0, `finding_id` RETENTION_RECONCILED, `receipt_match` true.
  - `raw_total` 95, `policy_excluded` 5 (non-author: 3 hits on `round-17-verifier-spotcheck.md` and 2 on `round-18-verifier-spotcheck.md`), `scanner_total` 90.
  - `raw_unallowlisted` 4 and `scanner_unallowlisted` 4, all on the nested copy path `.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json`, with classes R2, R5, R6 and R8.
  - Allowlisted 86, `non_author` 5, `forbidden_allowlist` 0, `retention_state` red, `privacy_clearance` false.
  - The partition 86 + 4 + 5 = 95 has no non-author/allowlisted overlap in this receipt.
- The supplied policy file holds 4 hits, all allowlisted, and it stays in `scanner_hits`. This confirms the correction's diagnosis, and that the v1 source-file exclusion would have produced 4 and 91, not 5 and 90.

## Contradictions and tensions (none resolved by weakening)

- **K1 — superseded text still in the pinned contract (governing-source conflict).**
  - Contract lines 15–16 say policy-excluded means "exactly the supplied policy path, never broad regex/path exclusions" and that the scanner denominator "removes that one source file only". Contract R04 says "raw minus policy-path hits".
  - v2 defines policy-excluded as the identities matched by `non_author_paths_glob`, which is a glob path exclusion, and the builder's lines 107–108 implement that.
  - `requirements-v2.json` pins the unchanged contract hash, so a reader of `contract.md` alone implements the v1 semantics and fails R03/R04 (v1 fixture result: `policy_excluded_hits` would be the policy.json hit).
  - Resolution source: `denominator-correction.md` explicitly supersedes. The keyword "never broad regex/path exclusions" remains literally contradicted by v2.
- **K2 — v1 fixture was unreachable under the gate's semantics (fixed in v2).**
  - The v1 allowlist rows lacked `rule`. The existing gate's `_validate_allowlist` (gate lines 145–147) requires exactly {path, class, line_sha256, reason, rule} with rule in {a, b, c}, so "reproduce existing allowlist semantics" would have returned SETUP for every v1 valid arm.
  - v2 adds `rule='b'`. The v1 oracle and fixture must not be used for measurement.
- **K3 — R12 "retained separately" versus v2 equality.** `policy_excluded` (v2) and `non_author` now count the same identity population (1 = 1 synthetic, 5 = 5 real). R12 holds only as two separately emitted fields. Neither the oracle nor the contract defines any case where they differ.
- **K4 — `scanner_unallowlisted` is identical to `raw_unallowlisted` by construction.** Gate unallowlisted already excludes non-author hits (gate lines 263–266), so the secondary denominator can differ from raw only in totals. R02's "raw/scanner_unallowlisted > 0" pair is therefore one observable stated twice, not two independent checks.
- **K5 — "required field/type/schema inconsistencies fail closed" versus the mismatch arms.**
  - R09 (class absent from policy), R06 (path absent from tree) and R10 (a metric contradicting the receipt's own exit_code and finding) must all return 1, not 2.
  - Schema validation must therefore stay at type and shape (string, integer that is not bool, 64-hex digest, line ≥ 1). It must not check membership or internal receipt consistency.
  - Ordering constraint: bool (R18), duplicate (R19), path (R20) and symlink (R21) rejection must run before multiset comparison, because each also produces a disagreement.
- **K6 — "preserve duplicates in recomputation" versus "reject duplicate receipt hits".**
  - Within one blob, identities are unique (unique line numbers, and the gate rejects duplicate class IDs at gate line 74).
  - Recomputed duplicates can arise only when two tree paths decode to the same string under `errors=replace` (gate line 202).
  - In that case a byte-faithful receipt must contain the duplicate and is then rejected with 2, so exact agreement is unreachable. No fixture covers this. It is an edge contradiction to state, not to suppress.
- **K7 — `policy_excluded_hits` as "digest-only identities" versus the R04 equality.** Contract line 15 says "digest-only identities". The oracle requires full four-key hit dicts, including path and line. A digest-only list fails R04. "Digest-only" must be read as "no matched text".
- **K8 — "symlink input rejected" versus scanning.** The gate scans mode-120000 entries as blobs and skips only gitlinks (gate line 199). The rejection applies only to the three CLI inputs; symlink blobs in the measured tree must still be scanned to reproduce raw hits.
- **K9 — the word "receipt" is overloaded.** Contract line 11 says provenance "appear in receipt", but the oracle reads provenance from the reconciler's stdout. Implementers should emit A4 fields in stdout. The contract does not say whether `argv` means the reconciler's argv or the receipt's argv; the oracle accepts any list.

## Contract clauses with no frozen observable (L1 measurement gaps)

These are named so that a PASS of 24/24 is not over-read:

1. `--selftest` with real subprocess arms: never invoked by the oracle, and executing it is forbidden this wave.
2. Blob-not-worktree reads: in every variant the worktree equals `--rev`, so no arm distinguishes the two. Static review is required.
3. Not importing or calling the existing gate: static review only.
4. `receipt_match` field: named in the contract, never checked.
5. `retention_state` green value: undefined; only `red` is tested.
6. Measured-revision **mismatch**: R13 exercises only the unresolvable case (wrapper and stdout commit both set to zeros).
   - Unspecified: whether wrapper `measured_revision` ≠ stdout `commit`, or ≠ argv `--rev`, yields 2.
   - Real case: `retention-floor-entering.json` has wrapper 9fb1f911 but stdout commit and argv `--rev` e9f340ce.
7. Path safety for `--policy` and `--allowlist`, and for absolute, empty or control-character receipt paths: only `../receipt.json` is tested. Symlink rejection is tested only for the receipt.
8. Bool rejection for `exit_code`, `non_author`, `routed` and other integers: only `line` and `metric` are tested.
9. Invalid or unsupported policy (bad regex, wrong schema): no arm. Sanitized output is required.
10. Receipt `stderr` non-empty, receipt `exit_code` disagreeing with recomputation, or a receipt produced with `--expect-population`: unspecified. In the last case the population fields cannot be recomputed from the CLI inputs.
11. Allowlist bytes at the r21 run time: the gate read the policy and allowlist from the worktree (receipt argv uses absolute filesystem paths). The receipt binds only `policy_sha256`, so allowlist run-time equality with the blob is unverifiable from the receipt.
12. The wrapper fields `cwd`, `started_utc` and `elapsed_seconds` are present in real receipts but absent from fixtures, so they must not be required.

## Implementation-visible constraints derived from the oracle

- stderr must stay empty on every path, including argparse errors and setup failures.
- stdout must be a single JSON object that always carries `finding_id`.
- `forbidden_allowlist` is an integer count, not the receipt's list.
- Hit dicts in output lists carry exactly four keys.
- `inputs_sha256` has exactly three keys.
- The tool must accept a policy with unknown extra keys (the fixture adds one) and an allowlist object without `schema` or `note`, as the gate does.

## Remaining unknowns

- Real-run numbers are taken from the receipt's own claims and were not independently recomputed (nothing was run). They are `[INFERENCE]` until L1 measures.
- Fixture expectations were traced by reading `fixture-builder-v2.py`; they were not generated.
- No LSP server was used; the semantic claims rest on direct reads of the committed blobs cited above, not on grep output.
