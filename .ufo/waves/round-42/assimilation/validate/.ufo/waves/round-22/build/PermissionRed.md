# PermissionRed — round-21 original 11/12 versus trust-refinement 12/12 controls

Seat: MoriR22.PermissionRed (scout, read-only). Scope: `.ufo/waves/round-21/fixture-loss.py` plus the public evidence it names or produced. The runner was NOT executed. No tests, builds or installs were run, and nothing outside this report was written.

## Answer

The default mode, `original-positive-permission`, and the `--trust-refinement` mode share the same 12 fixture bytes and the same tool. They differ in exactly one case expectation: `valid-independently-disposed`. Round 21 recorded two command receipts against the same tool SHA. The default mode scored 11/12 with exit 1; the refined mode scored 12/12 with exit 0. The 11/12 RED is therefore an intended contradiction of the original positive-permission control, not a regression in the other 11 cases. Both explicit modes must be kept. Neither mode is evidence that a real disposition was accepted.

## Observed facts (source)

- Mode switch. `parse_args` defines `--trust-refinement` as `store_true`, defaulting to off (`fixture-loss.py:652-653`). That flag selects the report's `expectation_mode`: `trust-refinement` when set, otherwise `original-positive-permission` (`:594`).
- Default expectations. `expected_cases()` yields 12 cases (`:252-317`). In the default mode, `valid-independently-disposed` expects `expected_rc 0` and exact counts `omitted0 retained1 unresolved0 disposed1 invalid0 pin_allowed true` (`:264-268`).
- Refined override. This is the only mutation in `run_harness`, at `:612-622`. It applies only when the case `id == "valid-independently-disposed"`. It keeps the original expectation in `superseded_expectation`, citing the reason "CriticTrust/ReviewTrust: submitted declaration is not external acceptance". It then sets `expected_rc 1`, exact `unresolved1 disposed1 pin_allowed false` (the other counts are unchanged), and `expected_finding_id …:disposition:external_review_required`.
- Fixture bytes are mode-independent. `fixture_artifacts`, `fixture_documents` and `apply_filesystem_mutation` never read `trust_refinement` (`:117-249`).
- A second, mode-independent supersession exists. `duplicate-accounting-id` permanently expects rc 2 and records the v0 expectation of rc 1 in `superseded_expectation` (`:280-283`). It appears in both modes and is not part of the 11-versus-12 difference.
- Pass rule. A case passes only if it has no failures (`:521`). Each case runs twice and checks that counts and finding IDs are stable across the two runs (`:480-520`). The runner exits 0 only when `failed == 0` (`:645`).

## Observed facts (public evidence, read via jq/sha256sum/read-only git)

| Item | Original (default) | Trust refinement |
|---|---|---|
| Command receipt | `evidence/final/fixture-original-control.json` | `evidence/final/fixture-trust-refinement.json` |
| argv flag | none | `--trust-refinement` |
| Receipt exit_code | 1 | 0 |
| measured_revision | `9fb1f911cfdd6061005c300795f44b1b45523897` | same |
| Observed report | `fixture-original-observed.json` | `fixture-refined-observed.json` |
| expectation_mode | `original-positive-permission` | `trust-refinement` |
| case_count / passed / failed | 12 / 11 / 1 | 12 / 12 / 0 |
| Tool sha256 (in report) | `de189084…38eb6` | same |
| base_revision | `e9f340ce…5ead655ab818a1c` | same |

- The only failing case in the original run is `valid-independently-disposed`. Six checks failed: run-1 and run-2 `expected-rc` (expected 0, got 1), `count-unresolved` (expected 0, got 1) and `count-pin_allowed` (expected true, got false). The observed counts in both runs were `disposed1 retained1 unresolved1 invalid0 omitted0 pin_allowed false`.
- In the refined run the same case has identical observed counts and passes. Its finding IDs include `…:disposition:external_review_required`.
- `evidence/final/summary.json` `fixtures` records `original_control {matched 11, total 12, rc 1, reason "Expected original-positive-permission contradiction"}` and `trust_refinement {matched 12, total 12, rc 0}`. This agrees with both receipts.
- Hashes for the bytes cited above (sha256): `fixture-loss.py` `502c793a…16662ef`, which equals the blob at `9fb1f911`; `fixture-original-control.json` `f0be2df7326e087395534aeccb9ac303c08279e88dfc9ded2bd250ab33b53eae`; `fixture-trust-refinement.json` `ca184873f9a3f56ace4fa3f5d6c7d69b87c44c87db58e2b7390d0d4e2fffc59a`; `fixture-original-observed.json` `a04a8ade2e7f67cf8fe480f5e9c302fc1ffff70c9030b101c1207c10ceced2eb`; `fixture-refined-observed.json` `124f672653c7b5851823428d0f36bb7c496fa8cb7c54afe961caec8b54c80108`.
- Git (read-only): the runner and evidence were last touched in `77a5bbe8` (the round-22 entering branch). `9fb1f911` is an ancestor of HEAD `306e06ec`. `git status` reports no worktree changes to the runner or `evidence/final/`.
- Rationale sources. `trust-refinement.md:5` says a submitted disposed declaration must never grant baseline acceptance and must return external-review-required. `build/CriticTrust.md:3-20` says `independent:true` is not proof of independence. `residual/ReviewTrust.md:106-127` notes that the default case still expects rc 0. Its proposed correction is to keep the fixture bytes and label the case superseded with expected `rc1 disposed1 unresolved1 invalid0 pin false`, which matches `:619-622`. `build/FixtureLoss.md:40` said in advance that the original control would remain unchanged and a refined audit would show a mismatch.

## Inference

- [INFERENCE] The R21 "original permission control RED 11/12" debt is fully explained by the tool correctly refusing automatic permission for a declared disposition. Any future wave that "fixes" it by flipping the default expectation, removing the default mode, or making the tool return rc 0 for a declared disposition would reintroduce the false permission that CriticTrust blocked. The RED must stay recorded as an expected contradiction, and both receipts must stay byte-unchanged.
- [INFERENCE] 12/12 under `--trust-refinement` shows only that the external-review blocker appears in a synthetic fixture. It does not authenticate any actor or reviewer, and it does not change the real accounting: two unresolved rows with null dispositions, `pin_allowed false` (`summary.json` C1). Baseline acceptance therefore stays blocked, and both historical dispositions stay unknown.
- [INFERENCE] There is no default-mode positive case that reaches rc 0. This is consistent with `trust-refinement.md:9` ("rc0 cannot be reached" for declared dispositions, per ReviewTrust A1) but leaves no positive control for a future authenticated-review path. ReviewTrust T2 (`:98`) found that an independent fixture's disposition record carried extra `fixture`/`kind` keys, which conflicts with the tool's exact key-set check (`tools/mori-evidence-loss.py:462`, not opened here). The current runner's `evidence/row-disposition.json` has exactly `{actor, disposition, id, independent, wave_id}` (`fixture-loss.py:144-150`). The refined run's `external_review_required` finding is consistent with that record reaching the external-review path.

## Remaining unknowns

- Whether `false-independent-boolean` and `same-actor-cleanup-only` exercise their named rejections, or would pass through another rejection path (ReviewTrust A3). This was not traced, because it is outside the named file.
- The full stdout/stderr bodies inside the receipts were not printed. Only receipt metadata and the summary stdout line were read.
- No round-22 recomputation was done, and none was claimed.

## Tooling

No installs or updates. Read-only use of existing `jq`, `sha256sum` and `git -C` (`log`, `status`, `merge-base`, `rev-parse`, `show`).
