# FinalR22 — static falsification of R22 against the shipping reconciler

Seat: MoriR22.FinalR22 (critic, leaf, static only). Nothing was executed against the SUT, oracle, fixture builder or harness. The only commands run were read-only: `sha256sum`, `git log/show/rev-parse`, and `jq` field and count projections over retained measure1 evidence. No matched text was read or emitted. No tools were installed or updated.

## Inputs verified (current bytes, not prior notes)

| artifact | sha256 (observed) | pinned by |
|---|---|---|
| `tools/mori-retention-reconcile.py` | `d6870fb6…0ce7` | measure1 `executing_input_bindings` (committed == loaded) |
| `.ufo/waves/round-22/oracle-reconcile-v2.py` | `dcd1c7c6…adb` | `requirements-v2.json` `oracle_sha256` (match) |
| `.ufo/waves/round-22/frozen/fixture-builder-v2.py` | `1b3e16f7…15d1` | `requirements-v2.json` `fixture_builder_sha256` (match) |
| `denominator-correction.md` / `contract.md` | `968945b2…` / `1658c390…` | `requirements-v2.json` (match) |

Commit order: the correction, fixture-v2, oracle-v2 and requirements-v2 were all added in `e2f549b` (10:55). The SUT first appears in `8cb4afb` (11:02), which **also adds `frozen/expected-real.json`**. `measure-round22.py` arrives in `3985b3d` together with a 10-line SUT change. `expected-real-identities.json` is added in `4f7cfce`, the measured revision itself.

## Verdict

1. **All 24 requirements hold for the shipping SUT**, judged statically under the v2 correction. Each arm's observed exit code, finding and error reason in `measure1/after-observed.json` matches the branch I traced.
2. **The branch-level reason requirement is not established by the frozen oracle.** No SETUP arm (R13–R21) asserts `error`. For R14, R15, R20 and R21, deleting the intended branch still yields exit 2 / SETUP through a *different* branch. For R13 the reason code is shared with the alternate branch, so even pinning the error cannot identify which branch fired. Branch discrimination exists only in the co-evolved `refinement-reconcile.py`, which was authored with and after the SUT, so it is not pre-registered evidence.
3. **The missing same-command red control is the M1 exclusion-identity control.** The fixture is built so that the v1 rule (policy-path exclusion) and the v2 rule (non-author glob) give the same scalars (5,1,4); `policy.json` and `non-author.txt` each carry exactly one hit. Despite that, no executed variant fails **R04 alone**. The measured `wrong-population` mutant also changes `unallowed`, so it dies on receipt MISMATCH across 9 arms. That kill comes from the exit/finding conjunct, not the identity predicate. On the real command, `all_claim_checks_pass` checks only scalars and input digests. The identity comparison sits outside that gate and has no red twin.

## Per-requirement branch trace (SUT line numbers)

"Frozen arm discriminates?" means: does the frozen arm still pass if the intended branch is deleted?

| R | holds | intended branch → observed reason | frozen arm discriminates? (smallest surviving SUT mutation) | existing red control |
|---|---|---|---|---|
| R01 | yes | full `check` → L218 MATCH, exit 0 | yes | all mutants |
| R02 | yes | L209 `retention_code=1`; L222 `raw_unallowlisted` and `scanner_unallowlisted` **both `len(unallowed)`** | yes for `privacy_clearance`; the two counters are one value, so they can never disagree | false-clearance |
| R03 | yes | L203–205 fnmatch over `non_author_paths_glob` | **no** for v1 vs v2: policy-path exclusion also gives (5,1,4) | none isolated (wrong-population died on the finding conjunct) |
| R04 | yes | L204–205 → L228 `scanner_hits` / `policy_excluded_hits` | partially: lists are checked, but `raw_hits = scanner ⊎ excluded` is not asserted | **none isolated** (see the M1 counterexample) |
| R05/R06 | yes | L212–213 `hits` multiset ≠ → exit 1 | yes | count-only cannot survive (the count changes) |
| R07–R09 | yes | L213 identity Counter | yes | count-only killed exactly {R07,R08,R09}; this is the one isolated scalar-vs-identity red that exists |
| R10 | yes | L215 `metric` | yes | none executed |
| R11 | yes | L200 forbidden, L209–210 precedence | yes | false-clearance |
| R12 | yes | L221 `non_author=len(excluded)` | yes (via MATCH) | wrong-population (finding conjunct) |
| R13 | yes | L161 `resolve` → `git_read_failed` (L59) | **no**: dropping `resolve(..)==measured` still gives `git_read_failed` via L163 merge-base. The reason is the same string, so the branch cannot be identified | refinement `measured-tag` covers the equality only by outcome |
| R14 | yes | L163 `merge-base --is-ancestor` → `git_read_failed` | **no**: the fixture builds `argv` (builder L77) before the diverged mutation (L89–92), so `--rev` keeps the original measured. Deleting L163 returns SETUP `receipt_revision_conflict` (L184) | refinement `diverged-consistent`/`cousin` (co-evolved) |
| R15 | yes | L164–165 → `policy_changed` | **no**: the receipt `policy_sha256` is the digest of the original bytes, so removing `'policy'` from L164 still gives SETUP `receipt_policy_digest` (L187) | refinement `policy-change` error pin (co-evolved) |
| R16 | yes | L164–165 → `allowlist_changed` | yes (without the check: MATCH, exit 0) | none executed |
| R17 | yes | L47 `invalid_json` | n/a | — |
| R18 | yes | L34 `type(value) is int` | yes (bool-line → exit 1, bool-metric → exit 0 if bools were accepted) | none executed |
| R19 | yes | L125 `duplicate_receipt_hit` | yes (→ exit 1) | none executed |
| R20 | yes | L50/L82 `unsafe_input_path` | **no**: without `safe_path`, `ls-tree -- ../receipt.json` fails or returns 0 rows, so SETUP either way [INFERENCE on git's outside-repo error] | refinement `unsafe-*` error pin (co-evolved) |
| R21 | yes | L85 mode check → `input_not_regular` | **no**: the symlink blob text `allowed.txt` fails JSON parsing, so SETUP `invalid_json` | refinement `symlink-identical` (co-evolved) |
| R22 | yes | L145 NUL skip | partially: `raw_total` discriminates, but `all(... for h in raw_hits)` is vacuous for `raw_hits=[]` | none |
| R23 | yes (all arms, statically: every `Invalid` reason is a literal; the generic branch emits `input_unavailable`) | L272–275 | **no** for SETUP arms: the predicate is valid-arm only, and the setup-leak mutant got frozen unmet=0 | harness `safe_outputs` only (outside the 24) |
| R24 | yes | L225–227 | partially: `argv` is checked for type only | refinement and real check bind `argv==cmd[2:]` |

## Counterexamples (smallest, static prediction)

**CX1 — M1 isolating mutant, never executed.** Replace only the output lists at L228:
`'scanner_hits':scanner,'policy_excluded_hits':excluded` becomes `'scanner_hits':[h for h in hits if h['path']!=paths['policy']],'policy_excluded_hits':[h for h in hits if h['path']==paths['policy']]`.
- **Synthetic:** the receipt comparison is untouched, so exit 0 MATCH. R03 (5,1,4) still passes, because the scalars come from `len(excluded)` and `len(scanner)`. Kill set is exactly **{R04}**.
- **Real command:** all expected-real scalars (95/5/90/4/4/86) are unchanged, so the real check (measure L104–105) stays true. Meanwhile `policy_excluded_hits` would list the policy path's 4 hits under `policy_excluded=5`.
- This is precisely the "scalar agreement ≠ population agreement" trap, and it is undemonstrated.

**CX2 — raw authoritative list unchecked inside the claim gate.** Change L228 `'raw_hits':hits` to `'raw_hits':[]`.
- It survives all 24 frozen arms (R22's `all()` is vacuous), all 27 refinement arms (none reads `raw_hits`), `safe_outputs`, and the scalar real check.
- Only `measure1-identity-check.json` would see it. That check self-qualifies as "not part of measure-round22.py all_claim_checks_pass", and its expectations are co-evolved (`4f7cfce`).

**CX3 — frozen R14 confound.** Delete L163. Frozen R14 still passes via `receipt_revision_conflict`, because the builder never rebinds `argv --rev` to the divergent commit.

**CX4 — R13 reason identity.** Delete the `resolve(repo,measured)==measured` conjunct at L161. The invalid-revision arm still reports the identical `git_read_failed` from L163, so no reason pin can tell the two branches apart.

**CX5 — real-command red twin missing.** The only adjacent real control, `contradictory-entering-receipt`, swaps `--receipt` and dies at L184 `receipt_revision_conflict`, before any population comparison. No run of the same real argv produces exit 1 MISMATCH on a population difference.

## Tradeoffs for the canonical judge (not SUT-fixable without a contract change)

- **T1 — `raw_unallowlisted` is scanner-scoped and aliased to `scanner_unallowlisted` (L222).**
  - On raw identities, the unallowlisted count is 2 synthetic and 9 real. Real: 95 − 86 allowlisted = 9, and non-author ∩ allowlisted = 86 − (90 − 4) = 0.
  - The SUT reports 1 and 4, i.e. numerically raw − allowlisted − non-author, the form the correction warns against as an inference. Here it is computed by identity, just over the scanner population.
  - Frozen R02 (==1), R11 (==3), R12 (==1) and expected-real (4) all pin the alias. Any SUT using a literal raw scope fails them. That makes this a duplicate authority/naming issue to rule on, not a requirement failure.
  - The `raw_unallowlisted:4` expectation is the one real scalar not stated in the pre-implementation correction. It was frozen in `8cb4afb` together with the SUT.
- **T2 — pre-registration.** The contract requires that "Expected values and fixture generator must be committed before implementation integration". Synthetic expectations meet this (`e2f549b`). `expected-real.json` does not: it was co-committed with the SUT. The identity expectations came later (`4f7cfce`).
- **T3 — gate divergence, fail-closed.** `tree()` decodes paths with `errors='strict'` (L76), whereas the gate uses `errors='replace'` (gate L202). Any non-UTF-8 tracked path anywhere in the measured tree makes the SUT return SETUP `invalid_tree_path` for a valid gate receipt. This is an operability cost, not a false MATCH.
- **T4 — glob fidelity is by code identity, not by any control.** The SUT and the gate both call `fnmatch.fnmatch`. The synthetic glob `non-author.txt` has no metacharacters, and the real globs only match single-segment names (5 hits under two `*-verifier-spotcheck.md` lesson files). Nothing therefore discriminates whether `*` crosses `/`.

## Smallest safe corrections

These go in co-evolved controls; the frozen artifacts stay byte-unchanged.

1. Add CX1 to the `measure-round22.py` mutations with a **required kill set of exactly {R04}**. That makes M1 fail-capable on the same oracle command.
2. Add a partition-closure assertion to the refinement and real checks: `Counter(raw_hits)==Counter(scanner_hits)+Counter(policy_excluded_hits)` and `len(raw_hits)==raw_total`. Add CX2 as a mutant that must be killed.
3. Fold the identity-digest comparison against `expected-real-identities.json` into `all_claim_checks_pass`. Add a red twin: the same real argv run against the CX1 mutant must produce an identity mismatch.
4. Record in the claim that frozen R13–R21 assert only exit/finding, and that R14, R15, R20 and R21 branch evidence is co-evolved. For R13/R14 to have identifiable branches, L161 and L163 would need distinct reason codes. That is a production change and L1's decision.

Impacted axes: calibration (claim strength exceeds the isolating evidence for M1 and branch reasons), depth (population vs scalar), operability (T3). No coverage, freshness or adjacency regression was found.
