# CriticFreezeOrder — round 23 sequencing audit

Seat: `MadoR22-2.CriticFreezeOrder-8` (critic, read-only, leaf). Scope: lane commits
`1bfe708..4dc80c1`, contract §Sequencing, the wave-1 seat specs that implement the seal
(MeasureDriver, OracleQuota, case authors, ImplQuota), and the existing freeze-order tooling.
Method: read-only `git -C` plumbing, file reads, sha256 of committed and working-tree bytes. No
runs, no installs, no lane writes beyond this file.

## Verdict

The pre-registration commit itself is sound. `4dc80c1` is the only commit after `1bfe708`. It
adds only contract, C1 frozen files, the C2 real control and the C1 oracle, and touches no
`tools/` path. Every hash pinned in `c1-requirements.json` matches both the commit and the
working tree. `4dc80c1` is already on `refs/remotes/origin/master`.

**The planned seal and driver do not yet prove that implementation lands after expectations.**
Five loopholes must be fixed before sealing (L1–L5). Four more items are disclosures or minor
corrections (L6–L9). The minimal correction set is at the end.

## Evidence (observed)

| Fact | Observation |
|---|---|
| Range | `git log 1bfe708^..4dc80c1`: `4dc80c1` (parent `1bfe708`, author = committer time `2026-10-21T14:00:53-03:00`) and `1bfe708`. No merges after `1bfe708`. |
| `4dc80c1` diff | `contract.md`, `evidence/sources-start.txt`, `frozen/c1-expected-real.json`, `frozen/c1-requirements.json`, `frozen/c2-expected-real.json`, `oracle-rename.py`, `LOG.md`, `SCORECARD.md`, plus a r22 report rewrite (`round-22/falsify/CodeSafePath.md`). No `tools/**`. |
| Pins | contract `2bb35aef…69e7`, `oracle-rename.py` `a55b2b50…c5f2`, r22 `fixture-builder-v2.py` `1b3e16f7…15d1`, r22 `requirements-v2.json` `48ea2369…0bea`. Each equals the `c1-requirements.json` value, at `4dc80c1` and in the working tree. |
| Entering tool | `1bfe708:tools/mori-retention-reconcile.py` sha256 `0795bac9…de32`; `tools/mori-quota-surface.py` absent at `1bfe708` and `4dc80c1`. |
| Remote pin | `refs/remotes/origin/master` = `4dc80c1` (pushed). `jj-lane.sh` push is fast-forward only (`merge-base --is-ancestor origin/$b $b`, line ~214) and checks lane identity on both author and committer. |
| Committer-time monotonicity | Last 300 first-parent commits: committer and author times are non-decreasing; no two share the same second. |
| Untracked wave-1 state | `wave1-{spec,run,assignments,attempts,response1..8}.json`, `build/swarm-registry.json`, `evidence/context-wave1.json` are untracked. `cases-proposed/` is empty. No `build/ImplQuota`, `build/OracleQuota` or `frozen/quota-cases` exist yet. |
| C1 pre-freeze dry run | `.scratch/round23/c1-before/observed.json` mtime 14:00:33; frozen files mtime 14:00:17; commit 14:00:53. Its `requirements_sha256` `88e1b912…3184` equals the committed `c1-requirements.json`. Its `tool_sha256` equals the entering tool `0795bac9…`. Result: 25/26, R25 unmet, `misleading_alias_runs` 8. |
| r22 precedent | Freeze `df880b4`, then `e825c7f`, then `e2f549b` (frozen v2 rewrite "before implementation"), then impl `8cb4afb`, which landed `frozen/expected-real.json` and `refinement-reconcile.py` with the tool. `3985b3d` (after impl) added `measure-round22.py` and modified `refinement-reconcile.py` and the tool. `4f7cfce` (after impl) added `frozen/expected-real-identities.json`. |
| Wave-1 MeasureDriver spec | "asserts `git merge-base --is-ancestor SEAL_REV REV` and that every frozen file is byte-identical between SEAL_REV and REV". It runs `.ufo/waves/round-23/oracle-rename.py` and `.ufo/waves/round-23/oracle-quota.py` from lane working-tree paths. |
| Existing convention | `tools/mori-freeze-order.py` (`mori-freeze-register-v1`): it walks `rev-list --topo-order base..tip`, reports `pre-build` iff the last commit touching a frozen path precedes the first commit touching an impl path, and binds the register to `--rev`. It makes no ancestry assertion between named commits and no time assertion. |

## Loopholes (counterexample → evidence → fix)

### L1 — reflexive ancestry plus a caller-chosen seal (MUST FIX in driver)

- **Counterexample.** Integrate the implementation, cases and C2 oracle in one commit `X`, then run
  `measure-round23.py --revision X --seal X`. `git merge-base --is-ancestor X X` exits 0, and
  frozen bytes are trivially identical between `X` and `X`, so the driver passes. The same holds
  for any `--seal` chosen after the implementation commit.
- **Evidence.** The MeasureDriver spec text above. `--is-ancestor` is reflexive.
- **Fix.** Assertions A1 and A5 below. With them, any `SEAL` the caller passes must be a commit
  where the implementation is provably absent, so the caller's choice cannot help.

### L2 — oracles run from the working tree, not from the seal (MUST FIX in driver)

- **Counterexample.** After seeing candidate output, someone edits uncommitted
  `oracle-quota.py` or a `frozen/quota-cases/*.json`. The committed blobs at `SEAL` and `REV`
  stay identical, so the identity check passes. The driver then executes the edited
  working-tree bytes.
- **Evidence.** The MeasureDriver spec names absolute working-tree paths. r22's driver at least
  compared working-tree bytes to `FREEZE` blobs (`freeze_binding_mismatch`); the r23 spec drops
  that comparison.
- **Fix.** Assertion A8: stage every oracle, case and frozen input from `SEAL` via
  `git archive`/`git show`, and execute only the staged bytes.

### L3 — the frozen set omits transitive dependencies (MUST FIX)

- **Counterexample.** `oracle-rename.py` executes
  `HERE.parent/'round-22'/'frozen'/'fixture-builder-v2.py'` from disk. That file defines
  `expected_scanner_hits`/`expected_policy_hits`, which drive R04 and R26. An implementation
  commit can edit it, and a "frozen files under round-23" identity check will not see the edit.
  The oracle only *records* `oracle_sha256`/`fixture_builder_sha256`; it never compares them to
  the pins.
- **Evidence.** `oracle-rename.py` lines 16–19 and 27. The pins live in `c1-requirements.json`.
- **Fix.** Include `round-22/frozen/fixture-builder-v2.py` and `round-22/frozen/requirements-v2.json`
  in the frozen identity set (A7). The driver compares the observation's
  `oracle_sha256`/`fixture_builder_sha256`/`requirements_sha256` to the `c1-requirements.json`
  pins and to the `SEAL` blob digests (A9).

### L4 — the candidate is visible before the seal (MUST FIX in sealing plan; residual is disclosed)

- **Counterexample.** ImplQuota delivers `build/ImplQuota/mori-quota-surface.py` in the same wave 1
  as the case authors, and L1 seals afterward. L1 (or a critic report L1 reads) checks the
  candidate against proposals. L1 then rejects the cases the candidate fails as "ambiguous", or
  edits an expected `basis` to match. The seal commit still precedes the implementation commit,
  so every git assertion passes. Git cannot see an untracked candidate, and file mtimes are
  forgeable.
- **Fix: smallest set that makes selection auditable.**
  1. Sealed case bytes equal the proposed bytes exactly
     (`sha256(frozen/quota-cases/<id>.json) == sha256(cases-proposed/<id>.json)`). L1 never edits
     a case. A defective case is rejected; a replacement must come from a fresh independent author.
  2. The seal commit contains **all** proposals, accepted and rejected. Each rejection carries a
     reason citing a contract row or source (S077–S084), never candidate behaviour.
  3. The driver also runs the after-tool on rejected cases. It reports
     `rejected_cases_matching_author_expectation` and `rejected_cases_failing` as disclosure, not
     as a gate. If every rejected case is one the implementation fails, that is a cherry-pick
     signal for wave 2.
  4. The seal manifest records L1's declaration that it did not open `build/ImplQuota/**`,
     `.scratch/round23/ImplQuota`, or any report quoting candidate output before committing the
     seal. Wave 2 verifies this against L1's transcript; that is the only evidence available.
  5. Preferred ordering: seal as soon as the case, oracle and driver seats finish, before L1 reads
     the ImplQuota result.
- **Residual (disclose).** Git ancestry proves "the seal commit precedes the implementation
  commit". It does not prove "the expectations were not influenced by a candidate that existed
  uncommitted". Byte-identity with independent authors' proposals is the bound.

### L5 — expectation-bearing scripts land after the implementation (MUST FIX)

- **Counterexample.** r22 shows the pattern: `measure-round22.py` (it defines
  `all_claim_checks_pass`) and `refinement-reconcile.py` landed or changed at `3985b3d`, after
  impl `8cb4afb`. `expected-real-identities.json` landed at `4f7cfce`. In r23,
  `measure-round23.py` and `oracle-quota.py` are authored in wave 1. If they land with or after
  the implementation, the pass predicate can be tuned to the implementation.
- **Fix.** Both files go in the seal commit, and the driver must be executed from the `SEAL` blob
  (A10).

### L6 — timestamps are self-asserted (DISCLOSE; keep only as corroboration)

- Git author and committer dates come from the committer (`GIT_COMMITTER_DATE`). Under jj,
  `metaedit --update-author` changes the identity but keeps the author timestamp from change
  creation, so an implementation change created before the seal can carry an earlier author
  date. Ancestry and the remote fast-forward pin are the proof; time is a consistency check
  only, and it must use committer time (`%ct`).

### L7 — local rewrite of the seal (FIX by pushing)

- Before it is pushed, a jj squash or rebase can fold implementation into the seal change and
  produce a new OID. Push the seal through `jj-lane.sh` (fast-forward only) **before** integrating
  the implementation, as was done for `4dc80c1`. The driver then checks that `SEAL` is an
  ancestor of `refs/remotes/origin/master`.

### L8 — topological index is not ancestry (FIX if `mori-freeze-order.py` is reused)

- `mori-freeze-order.py` orders by `rev-list --topo-order` index. With a merge, a side-branch
  frozen edit can sit at a lower index than a mainline implementation commit without being its
  ancestor. Its impl set is also a caller list, so an implementation under an unlisted path is
  "no-implementation". Require a linear range (A3) and define impl as the complement of the seal
  allowlist (A6).

### L9 — minor disclosures (no seal blocker)

- **C1 pre-freeze dry run.** It ran against the entering tool (not a candidate) 20 seconds before
  the freeze commit, using the final requirements bytes. The `before_expected` value `">0"` was
  therefore observable when frozen. This is benign and should be disclosed in the seal LOG entry.
- **Driver parsing.** `c1-requirements.json.before_expected.misleading_alias_runs` is the string
  `">0"`. The driver must parse this predicate explicitly rather than compare for equality.
- **Redundant R02 conjunct.** The `oracle-rename.py` R02 predicate repeats
  `scanner_unallowlisted==1` twice; the substitution turned r22's two conjuncts into one. Values
  are equal, so nothing is lost. Do not edit the oracle (it is frozen); disclose only.

## Seal commit: exact contents

Commit through `jj-lane.sh` with named paths only, then push before any implementation commit.
Parent chain: `1bfe708` ← `4dc80c1` ← (zero or more commits limited to the allowlist) ← `SEAL`.

**MUST contain (added):**

1. `.ufo/waves/round-23/frozen/quota-cases/<id>.json`: each accepted case, byte-identical to its
   proposal.
2. `.ufo/waves/round-23/cases-proposed/<id>.json`: every proposal, accepted and rejected,
   verbatim.
3. `.ufo/waves/round-23/oracle-quota.py`: byte-identical to `build/OracleQuota/oracle-quota.py`,
   or any difference listed in the manifest with a reason.
4. `.ufo/waves/round-23/measure-round23.py`: the driver, byte-identical to
   `build/MeasureDriver/measure-round23.py`, or any difference disclosed.
5. `.ufo/waves/round-23/frozen/seal-manifest.json`, containing:
   - `schema`; `entering` = `1bfe708…`; `prereg` = `4dc80c1…`; `contract_sha256`;
   - sha256 of every 4dc80c1-frozen file and of r22 `fixture-builder-v2.py` and `requirements-v2.json`;
   - `oracle_quota_sha256`, `measure_driver_sha256`;
   - `cases[]`: `{id, author_seat, proposed_sha256, sealed_sha256|null, decision, reason}`;
   - `impl_absent`: `{"tools/mori-quota-surface.py": null, "tools/mori-retention-reconcile.py": "0795bac9…de32"}`;
   - `allowlist` (the path globs below);
   - `l1_candidate_unopened_before_seal: true`.
6. Wave-1 provenance: `wave1-spec.json`, `wave1-run.json`, `wave1-assignments.json`,
   `wave1-attempts.json`, `wave1-response*.json`, `build/swarm-registry.json`,
   `evidence/context-wave1.json`, and every wave-1 report under `build/` **except**
   `build/ImplQuota/**`. These files have to pass the lane privacy scan first.
7. `LOG.md`: a seal declaration that includes the L9 disclosure.

**MUST NOT contain or change:** any `tools/**`, `build/ImplQuota/**`, `.scratch/**`, `corpus/**`,
`SKILL.md`, `PROVINCE.md` or `SCORECARD.md` result rows. The seal also must not change any file
committed in `4dc80c1` (`contract.md`, `frozen/c1-*`, `frozen/c2-expected-real.json`,
`oracle-rename.py`, `evidence/sources-start.txt`).

**Seal allowlist:** `.ufo/waves/round-23/**` excluding `build/ImplQuota/**`, plus `LOG.md`.

## Driver assertions (exact)

Let `ENTER=1bfe708a170c877db3319060d0ab38771efe03ac`,
`PREREG=4dc80c1be48308075e83af17f15fbfe7e95e6cb8`, `SEAL` = the caller value, `REV` = the
measured tip. All git calls use `git -C <lane>` with a scrubbed environment (reuse the
`mori-freeze-order.py` `_git_env` convention). Any failure ends the run with exit 2 and a named
finding; there is no partial pass.

- **A1 resolve.** `rev-parse --verify --quiet <x>^{commit}` gives a full OID for all four
  revisions. Assert `SEAL ∉ {REV, PREREG, ENTER}`.
- **A2 ancestry chain.** `merge-base --is-ancestor` exits 0 for `ENTER→PREREG`, `PREREG→SEAL`
  and `SEAL→REV`. Also `PREREG→refs/remotes/origin/master` and `SEAL→refs/remotes/origin/master`
  (the seal was pushed, fast-forward only).
- **A3 linear.** `rev-list --merges ENTER..REV` is empty. `rev-list --first-parent ENTER..REV`
  equals `rev-list ENTER..REV`.
- **A4 pre-registration identity.** `rev-parse PREREG^1 == ENTER`.
- **A5 implementation absent at the seal** (this defeats L1):
  - `cat-file -e SEAL:tools/mori-quota-surface.py` fails;
  - `rev-parse SEAL:tools/mori-retention-reconcile.py == ENTER:tools/mori-retention-reconcile.py`;
  - `diff --name-only ENTER SEAL -- tools corpus SKILL.md PROVINCE.md` is empty;
  - and in the measured tip, `cat-file -e REV:tools/mori-quota-surface.py` succeeds and the
    reconcile blob differs from `ENTER` (otherwise the result is `no-implementation`).
- **A6 seal and pre-seal commit contents.** For every commit `c` in `rev-list PREREG..SEAL`,
  `diff-tree -r --no-commit-id --name-only c` is a subset of the seal allowlist.
  `SEAL:.ufo/waves/round-23/frozen/seal-manifest.json` exists and its `allowlist` equals the
  driver's built-in allowlist.
- **A7 frozen identity.** The frozen set F is:
  - the `4dc80c1` round-23 files;
  - `frozen/quota-cases/**`, `cases-proposed/**`, `oracle-quota.py`, `measure-round23.py`,
    `frozen/seal-manifest.json`;
  - `.ufo/waves/round-22/frozen/fixture-builder-v2.py` and `.ufo/waves/round-22/frozen/requirements-v2.json`.

  For every `f` in F: `rev-parse SEAL:f == REV:f`. For the `4dc80c1` subset, also
  `PREREG:f == REV:f`. `ls-tree -r --name-only` of `quota-cases/` gives the same list at `SEAL`
  and `REV`, so no case is added or removed. As a disclosure counter (not a gate), report
  `log --format=%H SEAL..REV -- <F>`; a non-empty result means edit-then-revert.
- **A8 execute sealed bytes only.** `git archive SEAL -- .ufo/waves/round-23 .ufo/waves/round-22/frozen`
  into `.scratch/round23/<run>/sealed/`, preserving the layout (`oracle-rename.py` resolves
  `../round-22/frozen`). Stage tools from `REV` and `ENTER` with `git show`. Never execute a lane
  working-tree oracle, case or driver. If the working-tree copy differs from `SEAL`, fail with
  `snapshot_tampered`.
- **A9 hash pins.** The C1 observation's `oracle_sha256 == a55b2b50…`,
  `fixture_builder_sha256 == 1b3e16f7…`, and `requirements_sha256 == sha256(SEAL:frozen/c1-requirements.json)`.
  sha256 of `SEAL:contract.md` == `2bb35aef…`. Every manifest digest equals the staged bytes.
  For every accepted case, `sealed_sha256 == proposed_sha256`.
- **A10 driver self-binding.** L1 and wave 2 invoke `git show SEAL:.ufo/waves/round-23/measure-round23.py`
  into the staging directory and run that copy. The driver checks that its own sha256 equals
  `measure_driver_sha256`. Self-check alone is insufficient: only invoking the `SEAL` blob closes
  the loop.
- **A11 time (corroboration only; `%ct` = committer time).**
  - `ct(ENTER) ≤ ct(PREREG) < ct(SEAL) < ct(I1) ≤ ct(REV)`, where `I1` is the first commit in
    `rev-list --reverse SEAL..REV` that touches any path outside the seal allowlist.
  - `ct` is non-decreasing along `rev-list --first-parent --reverse ENTER..REV`.
  - Equality between `SEAL` and `I1` fails with `time_not_ordered`; the fix is to wait one second.
  - The summary states that time is self-asserted and that ancestry (A2) is the proof.
- **A12 before-state.** The C2 before run must observe `capability_absent` for every sealed case
  with the tool absent at `ENTER` (A5 already shows it absent at `SEAL`). The C1 before run stages
  the tool from `ENTER` (blob `0795bac9…`), never from the working tree.
- **A13 optional reuse of the existing convention.** Seal a `mori-freeze-register-v1` register
  (with itself listed in `frozen`) and run `tools/mori-freeze-order.py check --rev REV`, staged
  from `SEAL`. Set `base=PREREG`, frozen = F, and impl = every changed path in `SEAL..REV`
  outside the allowlist. The expected verdict is `pre-build` for both claims. This is valid only
  together with A3.

## Impacted axes

- **Calibration (C1).** The provenance of "requirements frozen before code" depends on A3, A7 and A9
  (the transitive fixture builder).
- **Coverage (C2).** The before→after case match is meaningful only with L1, L2, L4 and L5 closed.
  Otherwise the sealed cases or oracle can be selected or tuned after the candidate is seen.
- **Operability.** The driver's `all_claim_checks_pass` is false provenance if the driver itself
  is not sealed (L5, A10).

Wave 1's scope (case and oracle independence) is unaffected; only sealing and measuring are at
risk.

## Smallest safe correction

1. Add A1 (`SEAL ≠ REV`) and A5 (implementation absent at `SEAL`) to the MeasureDriver; this
   closes the reflexive-ancestry pass.
2. Add A8: execute only `SEAL`-staged oracles, cases and driver; working-tree mismatch fails as
   `snapshot_tampered`.
3. Extend the frozen set and pins to r22 `fixture-builder-v2.py` and `requirements-v2.json` (A7, A9).
4. Seal the C2 oracle, the driver, all proposals (accepted and rejected), the manifest and the
   wave-1 provenance in one allowlisted commit. Cases are byte-identical to proposals, and L1
   makes no case edits.
5. Push the seal with `jj-lane.sh` before any implementation commit; the driver asserts the seal
   is an ancestor of `origin/master` (A2).
6. Keep the committer-time ordering (A11) as corroboration and disclose that it is self-asserted.

Tool installs or updates: none.
