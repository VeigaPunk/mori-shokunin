# CriticAdmission — round 22

Seat `MoriR22.CriticAdmission` (critic, read-only, leaf). Target: the sole C1 claim, calibration 5→5 held, "retention receipt/denominator reconciliation capability". Nothing was installed. No tests, builds, linters, formatters, selftests, oracle runs or gate runs were done. Every SUT statement below comes from static reading, and every behavioral claim about an unexecuted program is marked [INFERENCE]. No matched text appears in this report.

## Verdict

**Yes. All 24 frozen requirements can be green while the tool certifies a false privacy improvement.** `oracle-reconcile-v2.py` checks synthetic fixtures only, and its predicates leave the receipt's own verdict fields untested. It also leaves the input paths and the real retained run unconstrained. So 24/24 is necessary for C1 admission but not sufficient. Admission must require four separately reported gates (§Gate semantics), the held scores below, and the corrections in §Smallest safe corrections. These must be frozen before L1 measures.

The untracked candidate `tools/mori-retention-reconcile.py` (sha256 `8600850fd2e3d07aabe528028835dcd9fc1a76220dc8c68351de2809c97b7a9a`, 262 lines, `??` in status) closes most of these gaps by construction, at `:173-207`. Two exceptions remain: counterexamples B and D. The oracle would not detect a regression of any of the closed gaps.

## Counterexamples

### A. A raw-multiset-only reconciler passes 24/24 and certifies a consistent "clean" lie

**Evidence.**
- Within `oracle-reconcile-v2.py`, the string `receipt_match` occurs 0 times.
- `fixture-builder-v2.py:79-92` mutates only `hits`, `metric`, `measured_revision` and `commit`. It never mutates the receipt's `exit_code`, `finding_id`, `unallowlisted_hits`, `allowlisted_hits`, `forbidden_allowlist`, `routed`, `warnings`, `non_author` or `policy_sha256`. A grep of assignments to those keys found 0 matches.
- The `drop` arm removes the last raw hit, which is the non-author hit, not the unallowlisted one.

**Counterexample SUT [INFERENCE, not executed].**
- It recomputes raw hits honestly and compares only the raw identity multiset.
- It checks `metric == len(unallowlisted_hits)` inside the receipt.
- It computes its own partitions from the caller-supplied policy and allowlist, and ignores every other receipt field.

Against each frozen requirement:
- R05–R09 fail on the raw multiset, as expected.
- R10 fails on the internal metric check, as expected.
- R01–R04, R11, R12, R22 and R23 read only the SUT's own recomputation.
- R13–R21 are pure setup checks.
- R24 reads only the SUT's own provenance fields.

Result: 24/24. Now feed it a receipt with the true raw `hits`, the unallowlisted hit moved into `allowlisted_hits`, `metric: 0`, `finding_id: RETENTION_CLEAN` and `exit_code: 0`. It returns exit 0 `RETENTION_RECONCILED`. A retention gate that said red is now certified as a reconciled clean receipt. This is the exact privacy-improvement lie C1 exists to stop. The same shape applies when a receipt shifts an unallowlisted hit into `non_author` (the denominator-shift lie this round is about), or omits a `forbidden_allowlist` row.

**Impacted axes:** calibration (the claim under test), adjacency (retention semantics).

### B. Input substitution: the allowlist path is not bound to the receipt's argv

**Evidence.**
- The r21 receipt argv names absolute worktree paths for `--policy` and `--allowlist`. It carries `policy_sha256` but no allowlist digest (`retention-floor.json`; corroborated by `ReceiptBinding.md:25`, `ReportContract.md:60,81` G3).
- The candidate binds the policy by digest (`:176`). It never compares the receipt's `--policy` or `--allowlist` argv paths with the supplied REPO_REL paths (`:155-176`).
- The oracle has no substitution arm.

**Counterexample [INFERENCE].**
1. Commit an alternate allowlist whose valid rule/reason rows cover the 4 nested-copy hits.
2. Produce the receipt with the real gate pointed at that file. It honestly says `RETENTION_CLEAN`, exit 0.
3. Reconcile with `--allowlist <alternate>`. Its bytes equal at both revisions, so R16 passes.
4. Output: exit 0 RECONCILED, `raw_unallowlisted 0`, `retention_state: clean-at-frozen-regex-scope`.

Reported as C1 evidence, this reads as "retention floor 4→0" with full provenance.

The byte-identical nested policy copy is harmless here: it has the same blob `8bf285bd…` at 9fb1f91, 77a5bbe and e9f340c, so its semantics are identical. Only a byte-different policy is blocked, by `:176`.

**Impacted axes:** calibration, adjacency.

### C. The 24 run only synthetic fixtures; the real retained result and the r22 tip are outside them

**Evidence.**
- Every oracle record uses `FIX.make` fixtures (`oracle-reconcile-v2.py:30-61`).
- `requirements-v2.json` freezes no real-receipt expected values. `denominator-correction.md:9` re-freezes only the synthetic 5/1/4. Yet `contract.md:19` requires the expected values to be committed before integration, and `contract.md:7` requires the real result to keep showing 4 unallowlisted.

**Counterexample [INFERENCE].** Any SUT can be 24/24 and still produce any output on the real r21 receipt. Nothing frozen would disagree.

Reconciling the r21 receipt also certifies only tree `9fb1f91`, not the r22 measured tip. A "0 new hits" or "floor unchanged" statement about r22 needs its own retention-gate receipt at the r22 tip. A reconciliation receipt cannot supply it.

**Observation, not a measurement or gate run.** At review time I applied the frozen classes, line by line, to three sets of files: files changed in 77a5bbe..HEAD, untracked round-22 files, and `tools/`. That gave 0 hits and 0 unallowlisted. This was not the gate, and not the tip.

**Impacted axes:** calibration; freshness (the floor is stale if inferred from r21).

### D. Duplicate authority and false corroboration in the reported fields

**Evidence.**
- Candidate `:211` sets `raw_unallowlisted` and `scanner_unallowlisted` from the same variable, `len(unallowed)`, which already excludes non-author hits (`:196`).
- `:210` and `:212` set `policy_excluded` and `non_author` from the same list.
- Under v2 these pairs are equal by definition. R02's "raw/scanner both 1" check and the R03/R12 pairing are each one check reported twice.
- On the real receipt the partition is 86 allowlisted + 4 unallowlisted + 5 non-author = 95, with no overlap. This is my metadata recount of `retention-floor.json`, and it matches `denominator-correction.md:5`.

So `raw_unallowlisted = 4` is not a raw count. Raw minus allowlisted is 9. The 5 non-author hits are policy-exempt, not allowlisted and not cleared.

**Risk.** A report showing 95→90 together with "raw 4 / scanner 4" reads as two independent denominators agreeing. It also makes the 5 exempt hits look removed. This is a tradeoff to disclose, not a code defect, provided the report says it plainly.

**Impacted axes:** calibration.

### E. Revision semantics: the real entering receipt separates measured_revision from the scanned commit

**Evidence.**
- In `retention-floor-entering.json`, `measured_revision` is `9fb1f91…` but argv `--rev` and the inner `commit` are `e9f340c…`.
- The two trees differ (`fbba387…` vs `bfb6ad1…`; `git diff --stat` reports 120 files changed), yet both receipts' hit lists are identical.
- The oracle has no arm where `measured_revision` differs from `commit`.

**Counterexample [INFERENCE].** A SUT that scans `measured_revision` and ignores `commit` passes 24/24. It would then "reconcile" e9f340c's receipt against the 9fb1f91 tree, which is false provenance. Hit agreement cannot reveal this.

The candidate fails closed (exit 2 `receipt_revision_conflict`, `:173`, `:175`). That is acceptable, but the measurement must then claim only the final receipt as reconcilable, never both r21 receipts.

**Impacted axes:** calibration, freshness.

### F. Untested branches

The only `retention_state` value the oracle ever asserts is `red`, so a hard-coded `red` survives. No arm reaches the candidate's `clean-at-frozen-regex-scope` branch (`:213`). `privacy_clearance` is checked only in the valid and forbidden fixtures, never on the exit-1 or exit-2 arms.

`MutantPlan.md:57,68` (its M3) still targets the superseded exact-policy-path exclusion. Under v2 it would mutate a dead rule. It must be rebased to the `non_author_paths_glob` exclusion.

**Impacted axes:** calibration.

## Gate semantics: four separate gates, never merged

| Gate | What it may claim | Real expected for C1 |
|---|---|---|
| G1: frozen finite oracle (24 IDs) | the capability exists at synthetic scope | 24/24; the before state is `capability_absent`, not 24 defects |
| G2: real reconciliation of `round-21/evidence/final/retention-floor.json` at 9fb1f91 | accounting agreement only | exit 0, `receipt_match` true, raw 95, non-author/excluded 5, scanner 90, unallowlisted 4, allowlisted 86, forbidden 0, routed 0, warnings 0, `retention_state` red |
| G3: retention gate at the r22 measured tip | the floor | rc 1, 4 unallowlisted (the 4→4 nested policy-copy hits); red |
| G4: privacy clearance | nothing | `false`; not evaluated; no source authenticates absence |

Neither G2 exit 0 nor G1 24/24 may be summarized as green retention. The entering receipt is not part of G2 (counterexample E). Retained debt is unchanged: original permission control RED 11/12, both disappearance dispositions unknown, baseline acceptance blocked.

## Held scores

coverage 6, operability 7, depth 5, freshness 5, calibration 5 and adjacency 6 stay held. The C1 verdict can be at most "improved (bounded capability)" on calibration, and only if G1–G3 are recorded as in the table. The new tool earns no operability credit, following the r20 precedent at `SCORECARD.md:1256`. There is no adjacency or privacy credit, and the scorecard must not describe 95→90 as an exposure reduction. The judge decides whether the corrections below were in place in time to admit.

## Smallest safe corrections

Freeze these before L1 measures, as a v3 oracle with no new requirement IDs. Each arm is conjunctive under an existing ID, following the R18 bool-metric precedent at `oracle-reconcile-v2.py:56`. Because a candidate SUT already exists, the freeze must be labeled co-evolved, following the freeze-order lesson.

1. **R10:** add arms that each expect exit 1 and `receipt_match` false:
   - a consistent clean lie (hit moved to `allowlisted_hits`, `metric` 0, `RETENTION_CLEAN`, `exit_code` 0);
   - `exit_code`-only and `finding_id`-only flips;
   - a `routed` or `warnings` lie.
2. **R11 and R12:** add a receipt that omits its `forbidden_allowlist` row (exit 1), and a receipt that moves an unallowlisted hit into `non_author` (exit 1).
3. **R15:** an altered receipt `policy_sha256` must fail closed.
4. **R01:** assert `receipt_match is True`. **R05–R10:** assert `receipt_match is False` and `privacy_clearance is False`.
5. **R16 and R20 (code and oracle):** the receipt argv's `--policy` and `--allowlist`, made relative to argv `--repo`, must equal the supplied REPO_REL paths, or exit 2. Add a substitution arm. This is the only production change; it is about 3 lines at the candidate's `:171-176`.
6. **R13 or R14:** add an arm where `measured_revision` differs from `commit` and the trees differ, expecting exit 2.
7. **G2 and G3:** commit the expected values from the table above before measuring.
8. **Report wording:** state that `raw_unallowlisted` is the gate metric with non-author hits exempt, and that the 5 non-author hits are exempt but not allowlisted or cleared.

## Checks actually run

- Read-only `git -C` plumbing: `rev-parse`, `show`, `merge-base --is-ancestor`, `diff --stat` / `--name-only`, `ls-tree`, `ls-files`, `log`, `status --porcelain`.
- `sha256sum`.
- Python metadata counts over the two r21 receipts: partitions, path counts and identity duplicates. Duplicate identities: 0.
- Field-name greps of the v2 oracle, the v2 fixture builder and the candidate.
- The ad-hoc frozen-class count in counterexample C, which reported counts only.
- A frozen-class self-scan of this report before finishing.

No SUT, oracle, selftest or gate was executed. No peer messages were sent. Installs: none.
