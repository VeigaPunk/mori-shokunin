# RerunPinnedDriver — round-23 falsification report (pinned driver re-run)

Seat: `RerunPinnedDriver` (read-only falsification seat, wave 23).
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Report path: `.ufo/waves/round-23/falsify/RerunPinnedDriver.md`.
Receipt directory: `.ufo/waves/round-23/falsify/RerunPinnedDriver/`.

## 1. What was run (exactly once)

Single invocation of the committed measurement driver, at the pinned revision and seal,
into an ABSENT scratch output directory:

```
python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/build/MeasureDriver/measure-round23-v2.py \
  --revision f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c \
  --seal 22772c10f6e3c1d8d3fe1b72083a6194e9f4e687 \
  --output /fast/scratch/hyaku/mori-r23/RerunPinnedDriver/observed
```

* invocation count: **1** (no re-run, no second attempt, no retry).
* cwd `/fast/scratch/hyaku/mori-r23/RerunPinnedDriver`; `TMPDIR=/fast/scratch/hyaku/mori-r23/RerunPinnedDriver/`
  (no `/tmp` fallback; no background jobs, no subagents).
* output dir verified **absent** before the run (`OUTPUT_ABSENT_OK`), so the driver took its
  normal fresh-output path (no `OUTPUT_DIR_PRESENT` short circuit).
* driver sha256 `5c12fdc056309966d3e716d25e3427a7908056595383f0353655b42282fdfbcd`, identical to the
  sealed copy at `22772c10…` (driver check `C13.driver_matches_sealed_bytes` = pass).
* exit code: **1** — this is the EXPECTED strict red, not an execution error:
  the driver returns 1 whenever not all claim checks pass, and C2's strict coverage target is
  red by the pre-registered frozen contradiction (see §4).
* stdout: the driver's compact result JSON (verbatim in `driver-stdout.txt`, empty stderr):

```json
{"after": {"c1_original_26": {"capability_absent": 0, "misleading_alias_runs": 0, "pass": 26, "total": 26, "unmet": 0},
           "c2": {"capability_absent": 0, "pass": 29, "total": 30, "unmet": 1}},
 "all_claim_checks_pass": false,
 "before": {"c1_original_26": {"capability_absent": 0, "misleading_alias_runs": 8, "pass": 25, "total": 26, "unmet": 1},
            "c2": {"capability_absent": 30, "pass": 0, "total": 30, "unmet": 0}},
 "measured_revision": "f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c",
 "seal_revision": "22772c10f6e3c1d8d3fe1b72083a6194e9f4e687"}
```

## 2. Result summary — overall exit 1, C1 green, C2 red

| claim | axis | before | after | verdict |
|---|---|---|---|---|
| C1 calibration | misleading-field cutover, original 26 requirements | 25/26 pass, unmet `[R25]`, `misleading_alias_runs=8` | **26/26 pass, unmet `[]`, `misleading_alias_runs=0`** | **GREEN** |
| C1 supplementary guards | 5 separately reported guards (not folded into the 26 denominator) | — | 5/5 pass | **GREEN** |
| C2 coverage | FR2 quota observability over the sealed cases | 0/30, `capability_absent=30` | **29/30, unmet 1** | **RED (strict target stays UNPROVABLE)** |

Aggregate driver flags: `all_claim_checks_pass=false`, `all_claim_checks_pass_excluding_real_controls=false`,
`real_controls_pass=false`, `privacy_clearance=false`.

## 3. C1 — calibration claim reproduced exactly (green)

Original-26 requirement identities (sealed oracle `oracle-rename.py`, staged from the seal bytes):

* requirement ids observed: `R01 … R26` (26 total), the original denominator unchanged.
* before arm (entering revision `1bfe708a…`): `pass 25 / total 26`, `unmet ['R25']`,
  `misleading_alias_runs 8`, `parsed_runs 18`, `schema_v2_runs 0`.
* after arm (measured revision `f3dc07c…`): `pass 26 / total 26`, `unmet []`,
  `misleading_alias_runs 0`, `parsed_runs 18`, `schema_v2_runs 18`.
  → alias **8 → 0**, schema **v1 → v2 on every parsed run**, and the only before-red requirement
  (R25) is now met. This is the C1 calibration claim as declared.

Supplementary guards (reported apart from the original 26, denominator preserved):

* `C21.c1_source_byte_guard` — pass. Baseline blob of the entering revision
  `tools/mori-retention-reconcile.py` sha256 `0795bac9367c33e534b79599114c1635d83c4b0e4a57fbbe235644858a59de32`
  (mode `100755`); the two pre-registered transformations each occur exactly once in the baseline
  (`SCHEMA='mori-retention-reconciliation-v1'` → `…-v2`; deletion of
  `'raw_unallowlisted':len(unallowed),`); the transformed target sha256
  `4599ee1aff95f21714e320a87fd31260f0435aa9c7a9884ac60ab952fe099a36` equals both the frozen
  driver constant and the observed production source; observed `v2` literal count 1, `v1` literal
  count 0, alias-fragment count 0, mode unchanged `100755`. The frozen artefact
  `frozen/c1-source-delta.json` agrees with every driver constant (entering sha, transformed sha,
  mode, entering revision, replacements, `output_pair_normalization`, `same_fixture_required`).
* `C22.c1_source_guard_discriminates` — pass; all three mutants rejected:
  `appended_statement` `f395a681…`, `removed_line` `e786fdb7…`, `whitespace_only` `d6d9da56…`.
* `C23.c1_same_instance_output_equivalence` — pass; 18 replay arms on the same fixture instance,
  **0 divergent**: 8 `check`/`check` arms and 10 `setup`/`setup` arms; alias present before and
  absent after, frozen tool digests on both sides (`0795bac9…` / `4599ee1a…`), `argv` equal,
  every other key and value equal.
* `C24.c1_selftest_schema` — pass; entering selftest schema `mori-retention-reconciliation-v1`,
  measured selftest schema `mori-retention-reconciliation-v2`, exit 0 on both, no alias key,
  otherwise identical payload.
* `C35.c1_real_identity_pins` — pass; observed identity digests equal the frozen pins
  (`raw_hits c275d2c2…`, `scanner_hits 9690b3a9…`, `policy_excluded_hits 17c348f0…`); the swapped
  scanner/policy twin is rejected; receipt pin `4001e2d9…` matched.

Real control and cutover identity:

* `C25.c1_real_control_matches_frozen` — pass; the measured production tool reproduces the frozen
  receipt exactly (exit 0, all frozen expected keys equal, `inputs_sha256` match, revision pins
  match, `tool_sha256` = `4599ee1a…`, `argv` match, `privacy_clearance=false`, no forbidden key present).
* `C26.c1_alias_present_before_absent_after` — pass; entering output carries
  `raw_unallowlisted = 4` with schema v1; measured output carries no alias key with schema v2.
* The C1 real-control receipt bytes are identical to the prior run's
  (`.ufo/waves/round-23/evidence/measure4/c1-real-control.json`,
  sha256 `f19f02c615bf13fd01554487d3ae257af4bfb5b34d4e8cb0e7bfbc180767750a` in both).

## 4. C2 — strict coverage target stays red at 29/30 (expected)

* `C33.c2_before_capability_absent` — pass; before the cutover every one of the 30 sealed cases is
  `capability_absent` (0 pass / 30 total, 30 capability_absent).
* `C34.c2_after_every_case_matches` — **FAIL (retained)**: after 29/30 pass, 1 unmet.
* `C30.c2_oracle_real_control_agrees` — **FAIL (retained)**: the `--real-expected` oracle run is
  `pass 30 / total 31 / unmet 1`.

Exact red identity — the single unmet case is identical in both runs:

* case file: `.ufo/waves/round-23/frozen/quota-cases/CaseEscapedSpace.json`
* case sha256: `8340738a509e474a94a815637e66b407dfb60c6449511e52db55296d844abeea`
  (byte-identical to the sha recorded in `.ufo/waves/round-23/evidence/frozen-contradiction.json`
  and to `frozen/case-decisions.json` → `selected_sha256` for `CaseEscapedSpace`,
  `primary: true`, `cases-corrected/CaseEscapedSpace.json`).
* every other sealed case (29 of 30) matches exactly; the case's own 9 supplementary
  metadata checks all pass (schema, exit_consistency, output_keys_allowed, output_key_set,
  error_token, path_key_set, df_covers_quota, limits_text, no_leakage) — only the six scored
  headline fields disagree (`exit_match`, `finding_match`, `paths_match` all false).
* observed actual (exit 2, `QUOTA_STATE_UNKNOWN`) is **byte-equal** to the `actual` object recorded
  in `evidence/frozen-contradiction.json` (paths array, exit, finding_id, df_covers_quota all equal):

  | path | observed | frozen expected |
  |---|---|---|
  | `/srv/my data/sub dir` | `fstype=null`, `mount_point=null`, `quota_state=unknown`, `enforcement=n/a`, `basis=ambiguous_overmount`, `device_check=not_checked`, `quota_option_keys=[]`, `btrfs_qgroups_mode=null` | `fstype=xfs`, `mount_point=/srv/my data`, `quota_state=enabled`, `enforcement=enforced`, `basis=xfs_quota_option` |
  | `/srv/plain` | `fstype=xfs`, `mount_point=/srv`, `quota_state=disabled`, `enforcement=n/a`, `basis=xfs_noquota_option`, `device_check=match` | identical |

* mechanism (from the frozen fixture's `mountinfo`, unchanged): mount **43** (`/srv/my\040data`,
  xfs, `usrquota`) has parent id **33**, while the longest strictly-shorter covering mount is
  **42** (`/srv`). The amendment's parent-ID refusal rule therefore requires refusing
  classification (`unknown` / `n/a` / `ambiguous_overmount`, null fstype and mount point,
  `device_check=not_checked`), which is exactly what the tool produced — but the frozen case's
  expected row still says `enabled`/`xfs_quota_option`. Both sides are kept unchanged: no
  special-casing, no exclusion, no relabelling, no rewrite of case, rule or oracle bytes.
  → the strict C2 coverage target stays **UNPROVABLE at 29/30**; nothing here may be read as a pass.

Real control, measured directly (`C29.c2_real_control_matches_frozen` — pass, bytes identical to the
prior run's `evidence/measure4/c2-real-control.json`, sha256 `cb97c7a2398a57cd9b23db7f4f9cadcc4f5fdd73c9b6329198ce0c0e02e6ecab`):

* exit 0, `finding_id=QUOTA_DISABLED`.
* `/home/vgpnk/Projects/shokunin` → `fstype=btrfs`, `mount_point=/home`, `quota_state=disabled`,
  `enforcement=n/a`, `basis=btrfs_qgroups_dir_absent`, `device_check=btrfs_subvolume_skipped`.
* `/tmp` → `fstype=xfs`, `mount_point=/tmp`, `quota_state=disabled`, `enforcement=n/a`,
  `basis=xfs_noquota_option`, `device_check=match`, `quota_option_keys=["noquota"]`.
* inside the sealed oracle's `--real-expected` run the real-control requirement itself PASSED
  (`real_control.headline = {exit_match:true, finding_match:true, paths_match:true}`); the C30
  aggregate fails only because the same single frozen case is unmet in that run as well.

**No additional failures.** Beyond `C34` and `C30`, all 32 remaining checks pass, and both failing
checks trace to the same single frozen case — verified by extracting the unmet set from both
`c2-after-observed.json` and `c2-after-real-observed.json` (each yields exactly one unmet row:
`CaseEscapedSpace.json`). The quota selftest arm at
`.ufo/waves/round-23/evidence/quota-selftest-corrected.json` (`arms: 49`, exit 0,
`QUOTA_SELFTEST_OK`, separate co-evolved fixture input correction) is a **different arm** and is not
the frozen `CaseEscapedSpace` case; it was not re-executed by this seat and is not part of the 29/30.

## 5. Full check ledger (34 checks, all recorded)

All pass (32): `C00.revisions_resolve`, `C01.seal_is_strict_ancestor_of_revision`,
`C02.seal_quota_production_path_absent`, `C03.seal_reconciler_entering_identical`,
`C04.seal_contains_harnesses_driver_and_dependencies`, `C05.seal_contains_accepted_case_files`,
`C06.seal_contains_original_proposals`, `C07.tools_delta_seal_to_revision_exact`,
`C08.frozen_byte_identical_seal_to_revision`, `C09.sealed_oracles_byte_identical`,
`C10.contract_and_amendment_unchanged_since_seal`, `C11.dependencies_pinned`,
`C12.working_copies_match_committed_seal_bytes`, `C13.driver_matches_sealed_bytes`,
`C14.quota_tool_absent_at_entering_revision`, `C15.quota_tool_present_at_measured_revision`,
`C16.retention_tool_present_at_both_revisions`, `C17.c1_before_requirement_counts`,
`C18.c1_after_requirement_counts`, `C19.c1_alias_removed`, `C20.c1_schema_v2_after`,
`C21.c1_source_byte_guard`, `C22.c1_source_guard_discriminates`,
`C23.c1_same_instance_output_equivalence`, `C24.c1_selftest_schema`,
`C25.c1_real_control_matches_frozen`, `C26.c1_alias_present_before_absent_after`,
`C31.rename_oracle_present_at_seal`, `C32.c2_oracle_present_at_seal`,
`C33.c2_before_capability_absent`, `C35.c1_real_identity_pins`,
`C29.c2_real_control_matches_frozen`.

Fail (2, retained): `C34.c2_after_every_case_matches` (29/30), `C30.c2_oracle_real_control_agrees`
(30/31, same single case).

Supporting identities from the same run: seal `22772c10…` is a strict ancestor of revision
`f3dc07c0…` (`merge-base --is-ancestor` returncode 0, `SEAL != REV`); `tools/` delta between
seal and revision is exactly `M tools/mori-retention-reconcile.py` + `A tools/mori-quota-surface.py`;
the quota production path is absent at the seal; the reconciler at the seal is byte-identical to
the entering revision; all 44 working-copy comparisons against committed seal bytes match
(0 divergent); C1 `scanner_unallowlisted`/`raw_not_allowlisted` names are unaffected by the cutover
and the arithmetic/identities/exit/finding behaviour is unchanged.

## 6. Reproducibility against the prior pinned run

Compared against `.ufo/waves/round-23/evidence/measure4/` (same revision, same seal, same driver
bytes):

* the entire `checks` array is **identical** (True);
* `before` and `after` aggregates are identical (True);
* `c1-real-control.json` and `c2-real-control.json` are **byte-identical**;
* every other receipt differs only in `recorded_utc` timestamps and the embedded scratch path
  strings (`.../MeasureDriver/measure-measure4/...` vs `.../MeasureDriver/measure-observed/...`);
* both runs produced exit 1 with the same two failing checks.

## 7. Receipts preserved (not ephemeral pointers)

Under `.ufo/waves/round-23/falsify/RerunPinnedDriver/`:

* `observed-output-receipts.tar.gz` — gzip tar of the complete driver output tree
  `observed/` (all 52 files: summary, all command receipts, all observed oracle/replay/selftest
  outputs), sha256 `9356a1461cb6cb65dabae085ecb1ef940d94f217324028216e2a7e14cab20074`.
* plain selected copies: `summary.json`, `checks-table.json` (compact per-check ledger),
  `invocation.json` (exact argv, exit code, environment, verdicts), `driver-stdout.txt`,
  `driver-stderr.txt` (empty), `c1-oracle-before.json`, `c1-oracle-after.json`,
  `c1-before-observed.json`, `c1-after-observed.json`, `c1-real-control.json`,
  `c2-oracle-before.json`, `c2-oracle-after.json`, `c2-oracle-after-real.json`,
  `c2-before-observed.json`, `c2-after-observed.json`, `c2-after-real-observed.json`,
  `c2-real-control.json`.
* `SHA256SUMS` — digests of every preserved file above.

Scratch copy retained at `/fast/scratch/hyaku/mori-r23/RerunPinnedDriver/observed/`
(ephemeral; the lane copy above is authoritative).

## 8. Bounds and method compliance

* No code, expectation, oracle, frozen case, seal or driver byte was altered; no `git add/commit/push`
  in the lane, no mutating `jj`, no lane index/ref changes. The only lane writes by this seat are the
  assigned report and the receipt directory above.
* The frozen inputs were **not** touched: `CaseEscapedSpace.json` still hashes
  `8340738a509e474a94a815637e66b407dfb60c6449511e52db55296d844abeea`; `C08` (frozen artefacts
  byte-identical seal→revision) and `C12` (working copies = committed seal bytes) both pass.
  The only seal→revision diff under the wave tree is the addition of the candidate source copies
  under `.ufo/waves/round-23/build/ImplQuota/` (`mori-quota-surface.py`, `-v2.py`, `-v3.py`);
  `frozen/`, `oracle-rename.py`, `oracle-quota.py`, `contract.md`, `preseal-amendment.md` and
  `build/MeasureDriver/measure-round23-v2.py` are unchanged between the seal and the revision.
* Live reads were limited to the quota surface declared by the committed driver (real-mode quota
  probe reading `/proc/self/mountinfo` and btrfs sysfs visibility, plus the C1 real reconciler run
  over the lane). No journal/journalctl query, no process/service/session probe, no credential or
  auth file, no `agent.db`, no Documents or shell history, no session transcript read of any kind.
  No `quotactl`/ioctl, no `btrfs qgroup`, no `xfs_quota`, no `repquota`, no mount, no remediation,
  and no direct read of actual qgroups/mode — all quota reads came through the committed driver.
* No quota tool was called by me directly; the driver's own fixture/oracle invocations are the
  committed harness's, and all fixture inputs are synthetic.
* Only the one authorized pinned-driver invocation was executed. No builds, tests, linters,
  formatters, gates or smoke runs were performed.
* Open debt is carried unchanged and not re-measured by this seat: four unallowlisted inherited
  hits (raw 95 / allowlisted 86 / non-author 5), original permission control RED 11/12, two
  unknown historical dispositions, baseline acceptance blocked, `privacy_clearance=false`.
  Probe visibility/accounting consistency is not clearance, health or admission.
* Tooling: **no package installs or updates were performed** by this seat (none needed); nothing
  was installed from any channel.

## 9. Residual risk and verification gaps

* The strict C2 target remains UNPROVABLE at 29/30. The red is a frozen-input contradiction
  (case expectation vs the sealed parent-ID refusal rule), not a tool defect demonstrated here, and
  not a clearance input. Resolving it requires a separate, non-special-cased oracle/case decision
  outside this seat's authority.
* `C30` is an aggregate check: because it is computed over the whole `--real-expected` oracle run,
  it fails whenever any sealed case is unmet. Its failure therefore carries no independent defect
  signal beyond `C34` here; this is stated so the two failures are not double-counted.
* The C1 source-byte guard is a syntactic constraint (exact baseline blob + two registered
  transformations), not a semantic equivalence proof; the same-instance replay and frozen real
  control are the behavioural evidence, and both pass.
* The C1 real control's `raw_unallowlisted = 4` on the entering side and the frozen
  `scanner_unallowlisted`/`raw_not_allowlisted` arithmetic were reproduced, but the four inherited
  unallowlisted retention hits themselves remain open debt; this seat did not adjudicate them.
* The C2 real control is a single-host observation at this moment; sysfs/mountinfo races during
  quota enable/disable/remount are not excluded by the frozen control, and real mode never reads
  `btrfs_qgroups_mode` (null by design).
* `df` capacity percentages still cannot see quota exhaustion (FR2/EDQUOT); `QUOTA_DISABLED` is not
  a capacity or health verdict.
* No unaccounted extra failures exist in this run: 34/34 checks were enumerated, 32 pass, and the
  2 failures were traced to the single frozen case.
