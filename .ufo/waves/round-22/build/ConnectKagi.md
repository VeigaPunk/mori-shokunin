# ConnectKagi — round 22 privacy/exposure/historical-retention boundary (connector, read-only)

## Verdict

The proposed boundary holds. Mori owns the reconciliation of its own receipts and denominators. Kagi does not own that work, and kagi does not declare ownership of exposure assessment for the non-credential private-context classes R1–R9. Kagi and mori share one discipline: hash-oracle and metadata-only reporting. They share no surfaces and no gates.

One load-bearing contradiction sits inside mori's own contract. The retained receipt does not support "raw95 includes 5 policy-source hits; scanner 90". The 5 excluded hits are **non-author** hits. The exact supplied policy path carries **4** hits, all of them allowlisted. Under the contract's exact-path rule, the scanner total is therefore 91, not 90.

## Axes

The round declares calibration (C1, at 5), adjacency (6) and depth/freshness (5). This report touches calibration (denominator labels) and adjacency (ownership routing, hash disclosure). It finds nothing that changes coverage or operability.

## Evidence

Reads only, plus read-only `git -C` plumbing and `jq` count/metadata projections over committed JSON. No matched text was printed into this report.

- **Mori routes exposure to kagi/operator.** `mori-shokunin/PROVINCE.md:126-131` says mori owns retention over its own committed evidence and redacts lane-authored copies at the tip. It also says "pushed history, exposure assessment, credential rotation and any history rewrite are **kagi/operator**-owned". `corpus/knowledge/evidence-minimization-r18.md:41-45` repeats this and states that line SHA-256 is "provenance, not secrecy".
- **Kagi's declared domain is credential material only.** `kagi-shokunin/PROVINCE.md:3` covers secrets, vault ops and credential-hygiene evidence. `:6` refuses anything outside that domain. `:67` lists "chousa, kasegi and kumitate run their own secret-shaped tripwires over their outputs (hygiene filters, not vault ops)". In other words, kagi treats each lane's output scanners as that lane's own. `corpus/QUALITY.md:26` (QA7) rejects any kagi entry that "restates another lane's mechanism (… scanning tooling)".
- **Kagi never acknowledges mori's routing.** A grep for `\bmori\b` over kagi `PROVINCE.md`, `SKILL.md` and `corpus/**` returns 0 matches.
- **Shared discipline.** Kagi `SKILL.md:14-17` forbids secret values and ref paths in durable artifacts. `SKILL.md:44` makes transcript scanning counts-only. `SKILL.md:222-228` withholds hashes of low-entropy private files because "a committed sha256 of a low-entropy private file is an offline confirmation oracle". Mori's minimization rule makes the same point at `evidence-minimization-r18.md:41-43`.
- **C1 classes are not credential classes.** `.ufo/waves/round-18/frozen/c1-policy.json` `classes` are labels only: R1 session_identity, R2 session_store_path, R3 tool_output_artifact, R4 private_document, R5 shell_history, R6 privileged_config, R7 operator_config_ref, R8 routing_table_key, R9 session_record_value. Its `known_limit` says regex classes are "a recall floor, not a privacy proof".
- **"Retention" means different things in the two lanes.** In kagi it means Vault/OpenBao KV and token retention in vendor documentation (`kagi-shokunin/corpus/lessons/round-22.md:21,25`; `round-23.md:27`). That is unrelated to mori's repository-evidence retention.
- **Retained receipt.** `.ufo/waves/round-21/evidence/final/retention-floor.json` is tracked (file sha256 `4001e2d9…c840`), schema `mori-r21-command-receipt-v1`, `measured_revision` `9fb1f911…3897`, `exit_code` 1. Count projections of the embedded stdout:
  - The raw population is 95 hits: 86 allowlisted, 4 unallowlisted and `non_author`=5. The identities that fall in neither list number exactly 5, so 95 − 5 = 90 = 86 + 4.
  - All 5 non-author hits are in `corpus/lessons/round-17-verifier-spotcheck.md` (3) and `corpus/lessons/round-18-verifier-spotcheck.md` (2). Both match `non_author_paths_glob`.
  - The exact policy path `.ufo/waves/round-18/frozen/c1-policy.json` carries 4 hits (R2:8, R5:11, R6:12, R8:14), all allowlisted.
  - The 4 unallowlisted hits sit at the same class/line positions in `.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json`. Their `line_sha256` multiset equals the policy-path multiset (jq equality returned `true`).
- **Git plumbing.** The copy and the policy file are the same blob, `8bf285bd…2742`, at 9fb1f91, 77a5bbe and HEAD 306e06e. The allowlist blob `f8be55b1…5b15` is unchanged across the same three revisions. 9fb1f91 is an ancestor of the entering commit 77a5bbe, which is an ancestor of HEAD. The real receipt therefore triggers neither R13/R14 (revision/ancestry) nor R15/R16 (policy/allowlist bytes).

## Overlap and non-overlap

**Overlap (shared discipline only; no co-owned artifact):**
1. **Hash disclosure.** Kagi's oracle rule and mori's provenance-not-secrecy rule apply to the same risk. The contract's "digest-only identities" for policy-excluded hits are exposed to it.
2. **Metadata-only reporting.** Kagi's counts-only transcript gate matches mori's R23 (no matched-text leakage).
3. **Credential subset of a hit (conditional).** Kagi's assessment applies only if a C1 hit, most plausibly R1 or R9, turns out to be credential material such as a session token. Whether any of the 95 hits is such material is unknown. No matched text was read.

**Non-overlap:**
1. **Receipt/denominator reconciliation, `retention_state` and the allowlist and non-author partitions.** These are mori's own-record calibration. Kagi refuses them under PROVINCE `:6`, `:67` and QA7.
2. **Exposure assessment of pushed history for non-credential classes R2–R9 (paths, documents, shell history, configuration references, routing keys, session-record values).** Kagi declares nothing here, and kagi's corpus has no mori acknowledgement. Mori's "kagi/operator" route is therefore one-sided. For these classes, ownership is effectively **operator** alone, with kagi advisory only on the credential subset. This is a stated contradiction, not one I can resolve from this seat.
3. **History rewrite and rotation authorization.** Neither lane owns these; the operator does. Kagi `PROVINCE.md:59` refuses to map vault structure, and nothing in kagi licenses rewriting another lane's history.
4. **Non-author hits (the 5 verifier-lesson hits).** These are inside mori's tree but authored outside it. Mori may count and report them, as R12 requires. Redaction authority belongs to their author or the operator, not to mori and not to kagi.
5. **Surfaces.** Kagi's surfaces are the janitor/opencode substrate, measured absent since round 18 (`kagi-shokunin/PROVINCE.md:10-18`). Mori's retention population is mori's own tracked blobs. The two sets share no path.

## Proposed move (one, bounded)

The move is a synthesis of the contract's exact-path rule, R02/R12 and kagi's hash-oracle rule:

1. **Relabel the r21 split in the round-22 lesson and in any expected-value fixture.** The correct statement is "raw 95 = 5 non-author + 4 exact-policy-path (allowlisted) + 86 other allowlisted, including the 4 hits in a byte-identical policy copy that are unallowlisted". This replaces "5 policy-source hits / scanner 90". The real-receipt expectations then become:
   - `raw_total`=95, `non_author`=5, `policy_excluded`=4, `scanner_total`=91
   - `raw_unallowlisted`=4, `scanner_unallowlisted`=4, `privacy_clearance`=false

   These values are derived from the receipt projection above; the reconciler has not been run.
2. **Pin exact-path exclusion against the byte-identical copy.** Exclusion by blob hash, basename or a `*c1-policy.json` glob would remove the copy's 4 unallowlisted hits. `scanner_unallowlisted` would then read 0, which manufactures an apparently clean secondary denominator and violates R02. Exact-path exclusion keeps it at 4.
3. **Emit no digest the committed receipt doesn't already carry.** The policy-excluded digest-only identities equal the 4 unallowlisted digests already in the receipt, so emitting them adds no new confirmation oracle. This satisfies kagi's hash rule without a kagi-side change.

No sibling file changes. Kagi's routing gap is reported to L1 only; it is not filed into kagi.

## Falsifiable no-axis-harm check

Run the integrated reconciler on the real retained receipt:

```sh
python3 tools/mori-retention-reconcile.py check --repo . --rev 77a5bbe8a0b41dfbfd2546d024d36e294b814bd0 --receipt .ufo/waves/round-21/evidence/final/retention-floor.json --policy .ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json
```

**Expected result (all must hold):**
- The run exits 0 with `RETENTION_RECONCILED`.
- The output reports `raw_total`=95, `non_author`=5, `policy_excluded`=4, `scanner_total`=91, `raw_unallowlisted`=4, `scanner_unallowlisted`=4 and `privacy_clearance`=false.
- Every `line_sha256` in the output is a member of the receipt's 60 distinct `line_sha256` values.

**Falsified if any of these occur:**
- `scanner_total` is 90 or `policy_excluded` is not 4. That would be a denominator mislabel or a broadened exclusion, harming calibration.
- `scanner_unallowlisted` is 0. That would be copy exclusion producing a false clean, harming calibration and adjacency.
- The output contains a digest absent from the receipt. That would be a new oracle surface, harming adjacency under kagi `SKILL.md:222-228`.
- The output contains any matched text (R23).
- `privacy_clearance` is not false.

**Paired mutant:** switch the exclusion to basename matching. The mutant must drive `scanner_unallowlisted` to 0 and be caught.

**Not run:** the reconciler is not yet integrated, and this wave forbids execution. L1 runs this after integration.

## Risks

- The contract's frontier text (`contract.md:21`) and SrcRejectHash.md:31 both carry the "5 policy" label. If L1 freezes 90 as an expected value, either the real-receipt arm mismatches, or an implementer "fixes" it by broadening the exclusion, which is the false-clean path described above.
- R03's synthetic 5/1/4 fixture remains valid. The relabel affects real-receipt expectations only.
- `line_sha256` values stay unsalted. This move adds no oracle, but it removes none either; the existing risk is retained as debt.
- Ownership of non-credential exposure (non-overlap item 2) remains unacknowledged by kagi. That needs operator or integrator wording, not a mori edit to kagi.

## Exercised actions and tooling

- Read both `PROVINCE.md` files, the round-22 contract and requirements, round-18 ConnectKagiExposure, mori's minimization knowledge, kagi `SKILL.md`, QUALITY, README and lessons excerpts, mori's round-21 lesson and SCORECARD excerpts, and `tools/mori-retention-gate.py` (non-author handling lines only).
- Ran read-only `git -C` `rev-parse`, `cat-file -e`, `merge-base --is-ancestor`, `ls-tree` and `ls-files`; ran `sha256sum` on one tracked file; ran `jq` count/label projections.
- No tests, builds, selftests, network access, installs or sibling writes. No draft artifacts.
