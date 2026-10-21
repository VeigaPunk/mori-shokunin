# RequirementsFreeze — freeze order, v2 pins, and reuse of rejected semantics

Seat: MoriR22.RequirementsFreeze (critic, static, read-only, report-only).
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`, HEAD `94b9014679c784a13d1963a51c9e0a7955770528`.
Read first: `.ufo/waves/round-22/denominator-correction.md`, then `contract.md`.
Method: read-only `git -C <lane>` plumbing (log/show/cat-file/ls-tree/blame/diff --no-index), `sha256sum` over committed blobs and worktree, and in-memory parsing of retained measure1 JSON evidence (I printed only ids, counts and digests). No tool, oracle, selftest, build or test was executed. No installs. No session, journal or config reads. No matched text appears in this report.

## Verdict

The order of the freeze holds. The four v2 pins match byte for byte. The shipping tool does not reuse the rejected policy-path exclusion. What remains are disclosure and authority defects, plus one weakness in how well the requirements can discriminate:

- No artifact was quietly changed after its freeze.
- The rejected semantics are absent from `tools/mori-retention-reconcile.py`.
- Two prior build-wave findings (ReviewFreeze F1 and F2, AttackR04 F1) are still present at HEAD and have not been addressed in the docs.
- The correction makes two claims that were false as committed.
- The frozen24 set catches the M1 mistake through a single identity check (R04).

## 1. Order of commits (verified)

| commit | time (-0300) | introduces |
|---|---|---|
| df880b4 | 10:51:49 | `contract.md`, `frozen/requirements.json` (v1) |
| 306e06e | 10:52:31 | dispatch context red/green only |
| e825c7f | 10:54:32 | `frozen/fixture-builder.py`, `oracle-reconcile.py` (v1) |
| e2f549b | 10:55:59 | `denominator-correction.md`, `frozen/fixture-builder-v2.py`, `frozen/requirements-v2.json`, `oracle-reconcile-v2.py` |
| 8cb4afb | 11:02:25 | **first** `tools/mori-retention-reconcile.py`, plus `frozen/expected-real.json` |
| 3985b3d | 11:09:37 | tool selftest MISMATCH arm; knowledge-note alias paragraph |
| 4f7cfce / 94b9014 | 11:57 / 11:58 | build reports, `expected-real-identities.json`; measure1 |

- `git cat-file -e <c>:tools/mori-retention-reconcile.py` fails at df880b4, 306e06e, e825c7f and e2f549b. The tool's history is exactly 8cb4afb and 3985b3d.
- Every frozen file (v1 and v2) has exactly one commit in its history, the one that created it. None changed afterwards.
- Git proves the order of commits. It does not prove the order in which things were drafted. The tool's 274 lines landed 6 min 26 s after the correction. [INFERENCE] Git cannot exclude that it was drafted before the correction, and nothing is retained that would.

## 2. Effective v2 pins against committed bytes (verified)

`requirements-v2.json` pins compared with blob SHA-256 at e2f549b, 8cb4afb and HEAD, and with the worktree:

| pin | value | e2f549b | HEAD | worktree |
|---|---|---|---|---|
| contract_sha256 (`contract.md`) | 1658c390… | = | = | = |
| correction_sha256 (`denominator-correction.md`) | 968945b2… | = | = | = |
| fixture_builder_sha256 (`frozen/fixture-builder-v2.py`) | 1b3e16f7… | = | = | = |
| oracle_sha256 (`oracle-reconcile-v2.py`) | dcd1c7c6… | = | = | = |

- `requirements-v2.json` itself is 48ea2369… at e2f549b and at HEAD.
- The v1 files are unchanged: `requirements.json` 3a756e98…, `fixture-builder.py` dbb94e6b…, `oracle-reconcile.py` 90d85e5a….
- The measure1 observations (before, after, every mutant, restored) all record requirements 48ea2369…, fixture 1b3e16f7… and oracle dcd1c7c6…. So measurement used v2 only.
- `executing-input-bindings.json` shows committed bytes equal loaded bytes for all seven bound files, including the tool at d6870fb6….
- The real diffs between v1 and v2 (verified with `diff --no-index`):
  - the fixture adds `rule:'b'` and strips `rule` from forbidden rows;
  - `expected_policy_hits` and `expected_scanner_hits` switch from the `policy.json` path to the `non-author.txt` path;
  - the oracle changes one line: the path it imports the fixture builder from.

## 3. Rejected semantics in shipping code: not reused (verified)

- `check()` builds the excluded and scanner sets only from `is_non_author`, which applies fnmatch to `non_author_paths_glob`. It also emits `'exclusion_basis':'non_author_paths_glob'`.
- `paths['policy']` is used only to read the blob, compare bytes, and bind the recorded path. It never selects hits.
- `scan()` excludes nothing by path or blob. Its per-blob-OID cache shares parsing between identical blobs (such as the real policy and its nested copy) while keeping the path in every identity.
- The partition matches `tools/mori-retention-gate.py` `_scan_result` line for line:
  - allowed keys are `(path,class,line_sha256)`;
  - `must_redact` rows are forbidden;
  - `allowlisted_hits` comes from all hits, so overlap with non-author is preserved;
  - `unallowlisted` is non-author-excluded and not allowed;
  - `routed`, finding precedence and exit code are the same.
- The allowlist check matches the gate's mandatory field set: `rule` must be one of a, b or c.
- The measure `wrong-population` mutant is exactly the v1 policy-path semantics. It was killed (measure1: 9 unmet, failing R01, R02, R03, R04, R11, R12, R22, R23 and R24).

## 4. Findings

### F1 (medium; provenance; still open, re-verified from ReviewFreeze F1): `expected-real.json` is described as frozen next to a "before implementation" claim, but it was born in the implementation commit

- Counterexample: `git blame` puts SCORECARD.md lines 1361–1365 at 8cb4afb. Those lines say the v2 freeze "landed e2f549b… before implementation" and then "Expected real input digests and values are frozen in `frozen/expected-real.json`". That file does not exist until 8cb4afb, the same commit as the tool.
- The contract requires "Expected values and fixture generator must be committed before implementation integration."
- The scalar values (95/86/4/5) do appear in the correction prose at e2f549b. The fields `paths`, `inputs_sha256`, `measured_revision`, `exclusion_basis` and `allowlisted` (as a structured value) do not.
- The digests in `requirements-v2.json` do not cover `expected-real.json`.
- Nothing after 8cb4afb changes this wording.
- Axes: provenance honesty, freshness.
- Smallest safe correction: add one sentence to SCORECARD and LOG classifying `expected-real.json` as "committed with the implementation (8cb4afb); not part of the e2f549b freeze". Do not edit the file.

### F2 (medium; duplicate authority; still open, re-verified from ReviewFreeze F2 and AttackR04 F1): the pinned contract still states the rejected meaning, and the supersession pointer names the wrong artifact

- Counterexample: `requirements-v2.json` pins `contract_sha256` = the bytes of `contract.md`, which still say:
  - "Policy-excluded means exactly the supplied policy path";
  - "removes that one source file only";
  - "R04 scanner hit identities exactly raw minus policy-path hits".
- Its `supersedes` field reads "frozen/requirements.json source-file-exclusion interpretation only". But `requirements.json` holds only IDs and a contract digest, with no interpretation at all. The rejected text is in `contract.md`, which v2 still pins with no supersession marker.
- Only the prose in the correction and the oracle code carry the effective R03 and R04 meanings.
- Axes: authority uniqueness, maintainability.
- Smallest safe correction: append a v3 pointer record, or a LOG line, saying that `denominator-correction.md` overrides `contract.md` line 13 and R04. Do not edit the frozen bytes.

### F3 (low; scope misstatement; new): "only" in `supersedes` understates the scope of v2

- Counterexample: of the three hunks in the v1→v2 fixture diff, two concern the allowlist `rule` field, not exclusion.
- Under v1, a gate-faithful SUT rejects every allowlist row (`allowlist_row`) and cannot pass any exit-0 or exit-1 arm. So v2 also changed which inputs can be evaluated at all.
- The correction prose does disclose this ("Fixture correction also adds… rule=b"). The machine-readable `supersedes` field does not.
- Smallest correction: same pointer record as F2, listing both changes.

### F4 (medium; false-as-committed claim; new): the correction says reviews "are retained and dispositioned" before any review existed in Git

- Counterexample: at e2f549b, `ls-tree .ufo/waves/round-22/build/` contains only `swarm-registry.json`. The 56 build reports first land at 4f7cfce, almost an hour later.
- At HEAD I found no per-review disposition record against the correction. I searched round-22 waves, LOG, SCORECARD, SKILL, and the round-22 lesson and knowledge note.
- The LOG and lesson cite only RawPartition, ReportContract, CriticPopulation, CriticAdmission and AttackR05/08/15/17/18/20/21/23.
- By a heuristic text scan, 19 build reports reason only from the v1 artifacts and cite neither v2 nor the correction. Examples are AttackR12, AttackR13–17, GateRaw and QualityDenom.
- AttackR12's v1-basis finding that R12 checks only a count is still true of `oracle-reconcile-v2.py` line 53. It is not dispositioned anywhere.
- "Main was notified" is unverifiable under this wave's no-session-read bound.
- Axes: provenance honesty, completeness of the correction obligation.
- Smallest correction: append a disposition table with one row per build report and a status of superseded, still-applies or addressed-by-<commit>. Do not change the reports.

### F5 (medium; meaning drift not declared at freeze; new): "All other 24 requirement meanings remain" is false for R12 and the raw/scanner unallowlisted fields

- Counterexample: under v2, the tool emits `policy_excluded` and `non_author` as the same `len(excluded)`, and `raw_unallowlisted` and `scanner_unallowlisted` as the same `len(unallowed)` (lines 221–223).
- The v2 oracle freezes this aliasing: R02 requires both unallowlisted fields to be 1 while the non-author hit is unallowlisted, and R12 requires `raw_unallowlisted==1`.
- So R12's v1 meaning ("non-author exclusions retained separately" from the policy-excluded population) cannot hold under v2. It reduces to R03's count.
- The contract also asked for distinct explicit `raw_unallowlisted` and `scanner_unallowlisted`; they now name one quantity.
- The alias is disclosed only in `corpus/knowledge/retention-reconciliation-r22.md` lines 27–31, and blame dates those lines to 3985b3d, after the implementation. Nothing was declared at e2f549b.
- The count is also off: R03 and R04 changed, so at most 22 "other" requirements could have kept their meaning.
- Axes: requirement identity, calibration honesty.
- Smallest correction: in the F2 pointer record, state that R12 and the two unallowlisted fields are aliases under v2, and date that decision to 3985b3d.

### F6 (medium; discrimination; new, extending ReviewFreeze F7): frozen24 catches the exact M1 mistake through R04 alone

- Counterexample (static trace, not executed): take a "reporting-only v1" mutant. It keeps `unallowed` from the non-author glob, so the receipt agrees, but reports `excluded` and `scanner` by the policy path.
- On the v2 fixture it gets:
  - R01 exit 0, because the receipt comparison is unchanged and the receipt's non_author is 1, equal to the policy.json hit count;
  - R02 pass;
  - R03 (5,1,4) pass;
  - R11 pass;
  - R12 pass, since `non_author` = 1 policy-path hit;
  - R22, R23 and R24 pass.
- Only R04's identity comparison (oracle lines 50–51) fails.
- The measure `wrong-population` mutant is weaker evidence than it looks. It also moves `unallowed`, so it breaks receipt agreement and fails nine arms. It failed R03 only through the exit/finding conjunct; the count predicate itself passes under v1 semantics.
- So the lesson's "fail-capable criterion" (M1) rests on one check. The real arm (`expected-real.json`, 5/90) also catches it, but that expectation is the co-evolved one from F1.
- Axes: discrimination, calibration.
- Smallest correction: add a reporting-only population mutant to the co-evolved mutation set in `measure-round22.py`, with R04 as the expected killer. Leave frozen24 unchanged.

### F7 (low; coverage gap; new): no synthetic arm has the real shape of a nested byte-identical policy copy

- The correction stresses that the four unallowlisted real hits are in "its identical nested copy" and says the policy is "never excluded by path or blob content".
- Neither `fixture-builder-v2.py` nor `refinement-reconcile.py` creates a byte-identical copy at a different path that then gets a match result. `policy-path-substitution` creates a copy but expects setup exit 2, so it asserts no partition.
- A mutant that excludes copies of the policy blob but not the supplied path passes all synthetic arms. Only the co-evolved real arm catches it (scanner_unallowlisted 0 ≠ 4).
- A blob-OID exclusion that also removes `policy.json` is caught by R04.
- Smallest correction: add a co-evolved refinement control with a nested copy, expecting raw 6, policy_excluded 1 and scanner 5, with the copy's hits in `scanner_hits`.

### F8 (low; the freeze commit is not mechanically bound; ReviewFreeze F5 partly fixed): measurement binds to the measured revision, not to e2f549b

- Since b095ecc, `measure-round22.py` binds seven files (tool, itself, refinement, oracle-v2, fixture-v2, requirements-v2, expected-real) as committed equal to loaded at `--revision`. This fixes ReviewFreeze F5's worktree-drift concern.
- But neither the driver, the oracle nor the tool references e2f549b (`rg` count: none).
- A later commit that co-edits `requirements-v2.json` pins together with the oracle or fixture would still produce `all_claim_checks_pass`. "Frozen before implementation" holds today only because I checked history by hand (section 2).
- Smallest correction: the driver should compare `git show e2f549b:<path>` with the loaded bytes for the four pinned files plus `requirements-v2.json`, and record the freeze commit in `summary.json`.

## 5. Prior build-wave notes: verified status at HEAD

| prior note | status at HEAD |
|---|---|
| ReviewFreeze F1 | still open (F1 above) |
| ReviewFreeze F2 / AttackR04 F1 | still open (F2 above) |
| ReviewFreeze F5 | partly fixed in b095ecc; residual is F8 |
| ReviewFreeze F7 | confirmed, and strengthened to sole-killer in F6 |
| AttackR12 #3 (missing `rule` field) | fixed in v2 |
| AttackR12 #4 (non-author/allowlist overlap) | covered by the co-evolved `non-author-overlap` control |
| AttackR12 #2 (R12 checks only a count) | still true, undispositioned (F4) |

## Axes impacted

- Provenance honesty: F1, F4, F8.
- Authority uniqueness: F2, F3.
- Requirement identity and calibration: F5, F6.
- Discrimination and coverage: F6, F7.

No production defect was found in the reconciliation semantics. No axis requires the canonical judge to reject on the code alone. F1, F4 and F5 are claim and provenance corrections that L1 can fix with append-only records.

## Checks for L1 after integration

- Rerun `measure-round22.py` with a reporting-only population mutant added, and confirm R04 is its only unmet requirement.
- Check the pin bytes at e2f549b against the bytes loaded at the measured revision.
- None of these were executed by this seat.
