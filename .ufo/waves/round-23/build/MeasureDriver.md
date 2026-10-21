# MeasureDriver — round-23 measurement driver (C1 calibration, C2 coverage)

Seat: `MadoR22-2.MeasureDriver-8` (executor, writer). Author-only deliverable. The driver was
**not executed** in this wave (seat instruction); no build, test, lint or smoke run was performed
on it.

## Delivered file

| Item | Value |
|---|---|
| Lane path | `.ufo/waves/round-23/build/MeasureDriver/measure-round23.py` |
| Bytes | 38061 |
| SHA-256 | `d25857e730b66053856c4cd42af0cd724cd142ec691b6ae29cfa1ed301a6401b` |
| Clone (authoring) | `.scratch/round23/MeasureDriver` (`git clone --no-hardlinks` of the lane), byte-identical copy at `.ufo/waves/round-23/build/MeasureDriver/measure-round23.py` |
| Mode | 0755, `#!/usr/bin/env python3`, stdlib only |
| CLI | `--revision REV --seal SEAL_REV --output ABSENT_DIR` |

The output directory must not exist (`OUTPUT_DIR_PRESENT`, exit 2). Exit code is 0 iff
`all_claim_checks_pass` is true in `summary.json`; the driver writes `summary.json` plus one
command receipt per invocation into the output directory.

## What the driver measures

| Step | Action | Claim covered |
|---|---|---|
| 1 | `git merge-base --is-ancestor <seal> <revision>` on the lane repo; both revisions resolved with `rev-parse --verify <rev>^{commit}` | ordering precondition (contract §Sequencing 4/5) |
| 2 | every file under `.ufo/waves/round-23/frozen/` compared byte-for-byte between `SEAL_REV` and `REV` (`git show` both sides); the two sealed oracles compared the same way; `contract.md` compared as well | frozen-artefact integrity after the seal |
| 3 | the frozen `c1-requirements.json` digests (`contract_sha256`, `fixture_builder_sha256`, `oracle_sha256`, `r22_requirements_v2_sha256`) recomputed from the committed artefacts at `REV` | requirement binding |
| 4 | `tools/mori-retention-reconcile.py` and `tools/mori-quota-surface.py` staged from `REV` and from the entering revision `1bfe708a170c877db3319060d0ab38771efe03ac` with `git show`; the quota tool is confirmed absent at the entering revision | capability absence before |
| 5 | C1 oracle `.ufo/waves/round-23/oracle-rename.py` run **before** (entering tool) and **after** (measured tool) with `--requirements frozen/c1-requirements.json` | C1 requirements R01–R26, R25 headline counter |
| 6 | C1 real control: the measured tool runs `check --repo <lane> --rev 77a5bbe8… --receipt/--policy/--allowlist` from `frozen/c1-expected-real.json` against the real lane paths; every expected key compared with exact type, `inputs_sha256`, `input_revision`, `measured_revision`, `tool_sha256`, `argv`, `privacy_clearance is False`, and the forbidden key `raw_unallowlisted` must be absent. The identical command is re-run against the entering tool to show the alias present before | C1 real control (r21 receipt) |
| 7 | sealed C2 oracle `.ufo/waves/round-23/oracle-quota.py` run **before** (absent tool path ⇒ `capability_absent` for every sealed case) and **after** (measured tool), with the cases directory `frozen/quota-cases`; a third run adds `--real-expected frozen/c2-expected-real.json` | C2 sealed case suite + oracle real control |
| 8 | C2 real control measured directly: the measured quota tool is run with its default paths and compared with `frozen/c2-expected-real.json` (exit, `finding_id`, and per path `fstype`, `mount_point`, `quota_state`, `enforcement`, `basis`, `device_check`, path set equality) | C2 real control |

`summary.json` carries `before`/`after` counts for both claims, the full check list, and
`all_claim_checks_pass`.

## Check list emitted by the driver

| Id | Meaning |
|---|---|
| `C00.revisions_resolve` | both revisions resolve to commits |
| `C01.seal_is_ancestor_of_revision` | `merge-base --is-ancestor SEAL REV` exits 0 |
| `C02.frozen_byte_identical_seal_to_revision` | every frozen artefact identical between seal and revision |
| `C03.sealed_oracles_byte_identical` | `oracle-rename.py`, `oracle-quota.py` identical between seal and revision |
| `C04.contract_unchanged_since_seal` | pre-registered contract unchanged |
| `C05.c1_requirement_bindings` | the four frozen digests match the committed artefacts at the revision |
| `C06.quota_tool_absent_at_entering_revision` | capability absent before |
| `C07.quota_tool_present_at_measured_revision` | capability present after |
| `C08.retention_tool_present_at_both_revisions` | the C1 tool is measurable before and after |
| `C09.c1_before_requirement_counts` | before: total 26, unmet exactly `['R25']` |
| `C10.c1_after_requirement_counts` | after: total 26, unmet empty, `counts.unmet == 0` |
| `C11.c1_alias_removed` | `misleading_alias_runs` > 0 before, 0 after (recomputed from the oracle runs, not only from the oracle counter) |
| `C12.c1_schema_v2_after` | every parsed after-run carries `mori-retention-reconciliation-v2` |
| `C13.c1_real_control_matches_frozen` | C1 real control reproduces the frozen receipt exactly |
| `C14.c1_alias_present_before_absent_after` | the alias exists in the entering output and is gone after |
| `C15.c2_before_capability_absent` | before: every sealed case is `capability_absent` |
| `C16.c2_after_every_case_matches` | after: every sealed case matches, `unmet == 0` |
| `C17.c2_real_control_matches_frozen` | C2 real control reproduces the frozen host observation |
| `C18.c2_oracle_real_control_agrees` | the sealed oracle with `--real-expected` reports no unmet real requirement |
| `C19.c2_oracle_present_at_measured_revision` | the sealed C2 oracle exists at the measured revision |
| `C20.rename_oracle_present_at_measured_revision` | the frozen C1 oracle exists at the measured revision |

`all_claim_checks_pass` = deterministic checks ∧ the three real-control checks. The driver also
reports `all_claim_checks_pass_excluding_real_controls` and `real_controls_pass` separately, so a
host drift on the C2 real control is visible as a drift observation instead of being conflated
with a claim failure (contract: "a later differing run is a drift observation, not an oracle
rewrite").

## Design decisions worth the L1's attention

- **Everything measured is staged from the revision, not the working tree.** The driver stages a
  mirrored wave tree (`.ufo/waves/round-23/{oracle-rename.py,oracle-quota.py,frozen/**}` plus
  `.ufo/waves/round-22/frozen/fixture-builder-v2.py`) out of `REV` and runs the staged oracles.
  The mirror is required: `oracle-rename.py` resolves the r22 fixture builder as
  `HERE.parent/round-22/frozen/fixture-builder-v2.py`, so it must keep that relative layout. The
  sealed cases are staged the same way and handed to the C2 oracle with `--cases`. Working-tree
  copies are compared against the revision but recorded only as observations, never as a gate.
- **The C1 oracle is the C1 measurement, per the contract's "declared consequence".** The r22
  oracle and `measure-round22.py` read the old key and are deliberately not re-run; only the r23
  oracle is.
- **C2 oracle CLI** follows the wave spec (`--tool PATH --cases DIR --output FILE
  [--real-expected FILE]`). If the sealed oracle exposes different option names, the driver falls
  back to the option names printed by `--help` and records the adapted argv in the receipt.
- **Scratch and TMPDIR**: all scratch lives in `LANE/.scratch/round23/measure-<output-name>`;
  `TMPDIR` is set to `LANE/.scratch`. `/tmp` is never used for a deliberate probe or output. The
  driver removes only its own scratch directory when re-run with the same output name.
- **Host reads**: only the C2 real control's reads happen (mountinfo, `os.stat`, `realpath`,
  `/dev/mapper/*` realpath, `/sys/fs/btrfs` listings). No `quotactl`, `btrfs qgroup`,
  `xfs_quota`, `repquota`, mount, write or privileged call is issued anywhere in the driver.

## Evidence retained at authoring time (read-only, lane repo)

| Fact | Value |
|---|---|
| lane toplevel | `/home/vgpnk/Projects/shokunin/mori-shokunin` (`git rev-parse --show-toplevel`) |
| lane HEAD at authoring | `4dc80c1be48308075e83af17f15fbfe7e95e6cb8` (contract pre-registration) |
| entering revision | `1bfe708a170c877db3319060d0ab38771efe03ac` |
| `tools/mori-retention-reconcile.py` at entering | present, `SCHEMA='mori-retention-reconciliation-v1'`, emits `raw_unallowlisted` |
| `tools/mori-quota-surface.py` at entering and at HEAD | absent (`git cat-file -e` → “path does not exist”) |
| `frozen/c1-requirements.json` | `88e1b912df1a8d5f3ad3da6a9fd3fec751cab7776919c77a8aa83365f84f3184` |
| `frozen/c1-requirements.json` → `contract_sha256` | `2bb35aefb08d3fafc467260f859453c0f096effe18b2446503f2b2ee87fe69e7` = sha256 of `contract.md` ✓ |
| → `fixture_builder_sha256` | `1b3e16f74a032e066dd881c15affbc4401f2f44447d78efc650ee98a6d2d15d1` = sha256 of `.ufo/waves/round-22/frozen/fixture-builder-v2.py` ✓ |
| → `oracle_sha256` | `a55b2b50d3e7447a1d5312c8b066a13137a6a6895f0343b3240ebf081d97c5f2` = sha256 of `.ufo/waves/round-23/oracle-rename.py` ✓ |
| → `r22_requirements_v2_sha256` | `48ea2369dad5958bd62922483438124b11597a61a5e1ddc02bbeb213c89d0bea` = sha256 of `.ufo/waves/round-22/frozen/requirements-v2.json` ✓ |
| `frozen/c1-expected-real.json` | schema `mori-retention-reconciliation-v2`, `scanner_unallowlisted` 4, `raw_not_allowlisted` 9, `raw_total` 95, `allowlisted` 86, `policy_excluded` 5, `scanner_total` 90, `retention_state` red, `privacy_clearance` false, forbidden key `raw_unallowlisted`, input revision `77a5bbe8a0b41dfbfd2546d024d36e294b814bd0` |
| `frozen/c2-expected-real.json` | exit 0 `QUOTA_DISABLED`; fleet root → btrfs `/home` disabled `btrfs_qgroups_dir_absent` `btrfs_subvolume_skipped`; `/tmp` → xfs `/tmp` disabled `xfs_noquota_option` `match` |

## Risks and blockers

- **The sealed C2 artefacts do not exist yet.** At the current lane HEAD there is no
  `.ufo/waves/round-23/oracle-quota.py` and no `.ufo/waves/round-23/frozen/quota-cases/`. The
  driver is written for a later revision at which L1 has sealed them; until then `C19`, `C15`,
  `C16`, `C17`, `C18` report failure with an explicit "unavailable" reason rather than silently
  passing. `C07` likewise fails until the quota tool lands. This is the intended pre-state, not a
  driver defect.
- **The C2 real control is host-state dependent.** `frozen/c2-expected-real.json` was frozen from
  an independent host observation on 2026-10-21. A remount, a quota enable or a device change
  between the freeze and the measurement turns `C17`/`C18` red. The frozen file itself says a
  later differing run is a drift observation, not an oracle rewrite; the driver reports the drift
  explicitly (expected vs observed per path) and keeps the deterministic verdict separable.
- **C1 real control sensitivity.** The tool scans the lane repository at the receipt's
  `measured_revision` (`9fb1f911…`), so the control is reproducible against the lane regardless
  of how far the branch has advanced; it does not depend on the working tree.
- **Unverifiable at authoring time**: the sealed C2 oracle's exact CLI and output key names are
  fixed only when L1 seals it. The driver uses the wave-spec CLI with a `--help`-derived
  fallback, and it derives the case count from the staged `*.json` files rather than assuming a
  number, so the seal may contain any number of cases.
- **Not done here (by instruction)**: the driver was not executed, so no `summary.json`, no
  before/after counts and no oracle verdict exist yet. L1 owns the post-integration run and the
  wave-2 falsification.

### C2 oracle interface, checked against the delivered build artefact

The OracleQuota seat's build artefact
`.ufo/waves/round-23/build/OracleQuota/oracle-quota.py`
(`982753f4efdb914dedee1dadd4de8c575431d3c992aae50838c8b1f5ae3e1624` at authoring time, **not yet
sealed**) was read for its interface only. It exposes exactly the CLI the driver invokes:
`--tool`, `--cases`, `--output`, `--real-expected` (optional). Its observation file carries
`counts.total/pass/capability_absent/unmet` plus `cases_*` counters, and its real control reads
`expected_exit` / `expected_finding_id` / `expected_paths` — the exact key names in
`frozen/c2-expected-real.json` — and compares the per-path tuple
`(path, fstype, mount_point, quota_state, enforcement, basis, device_check)`. The driver's
`C15`/`C16`/`C18` therefore read the same counters the oracle publishes, and the driver's own
`C17` compares the same facets independently (by path, not by order), so the two verdicts are
independent. The sealed copy at the seal commit is what the driver actually runs; the digest
above is only a statement about the artefact visible now.

## Run log

- Commands: `git clone --no-hardlinks` into `.scratch/round23/MeasureDriver`; read-only
  `git -C <lane> rev-parse / log / cat-file / show / ls-tree`; `sha256sum`; `cp` of the finished
  file to the lane path; `python3 -c "ast.parse(...)"` and `python3 -m py_compile` on the driver
  **as a static syntax check only** (the driver was not executed, and no measurement artefact was
  produced).
- Tools installed or updated: none. No package manager transaction was needed or run.
- Measurements, tests and builds: none run. The driver's own numbers do not exist yet.
- Files written: `.ufo/waves/round-23/build/MeasureDriver/measure-round23.py` (the deliverable),
  `.ufo/waves/round-23/build/MeasureDriver.md` (this report), and the seat clone under
  `.scratch/round23/MeasureDriver`. No production, frozen, oracle or case file was touched; no
  git/jj mutation was performed in the lane.

## v2 amendment — `measure-round23-v2.py` (all deltas against v1)

Trigger: the L1's IRC of 2026-10-21 (`.ufo/waves/round-23/preseal-amendment.md` plus the
tightening note on the critic's sign-off for the exact source-byte transform).

| Item | Value |
|---|---|
| Lane path | `.ufo/waves/round-23/build/MeasureDriver/measure-round23-v2.py` |
| Bytes / lines | 61281 / 1080 |
| SHA-256 | `82d581643e6cf4387226202efcf9e43ee02ea8db70b74e2db8e2e355eb3159c9` |
| Unique checks | 33 (v1: 20) |
| Preserved | `measure-round23.py` is **byte-unchanged** (`d25857e730b66053856c4cd42af0cd724cd142ec691b6ae29cfa1ed301a6401b`) |
| Execution | none — not run, as instructed |

### Deltas (v1 → v2)

1. **Strict ancestry** — v1 required `merge-base --is-ancestor` only; v2 also requires `SEAL != REV`
   (resolved commits compared): `C01.seal_is_strict_ancestor_of_revision`.
2. **Seal proof added** — `C02` the production quota path is absent at SEAL; `C03` the reconciler
   at SEAL is byte-identical to the entering revision; `C04` the seal carries the oracles, the
   driver, the frozen controls, the contract, the amendment and the r22 builder/requirements
   dependencies; `C05` the seal carries the accepted C2 case files; `C06` the seal retains the
   original case proposals.
3. **`tools/` delta seal→REV** — `C07`: `git diff --name-status SEAL REV -- tools/` must be exactly
   `M tools/mori-retention-reconcile.py` and `A tools/mori-quota-surface.py`, nothing else.
4. **Harness provenance** — v1 staged the oracles from REV; v2 stages every harness (oracles,
   frozen files, r22 builder/requirements) from the **committed seal bytes** and executes them from
   there. `C12` compares the measured working copies with the committed seal bytes; `C13` requires
   the executing driver to be the committed seal copy of itself (`DRIVER_REL`).
5. **Dependency pinning** — `C11` recomputes the four pinned digests of
   `frozen/c1-requirements.json` at the seal **and** at the revision (v1: revision only), and
   `summary['frozen_dependency_digests']` hashes every frozen dependency, both sealed oracles, the
   driver, the contract, the amendment and both tools.
6. **Documents** — `C10` requires `contract.md` and `preseal-amendment.md` to be byte-identical
   between seal and revision.
7. **C1 source-byte guard (new)** — `C21`: the baseline is the **git blob** of the entering
   revision (`sha256 0795bac9367c33e534b79599114c1635d83c4b0e4a57fbbe235644858a59de32`, the digest
   the amendment pins); each of the two pre-registered substrings must occur **exactly once** in
   that baseline (`SCHEMA='mori-retention-reconciliation-v1'` → `…-v2` substitution; deletion of
   the single `'raw_unallowlisted':len(unallowed),` producer fragment); the transformed target
   SHA-256 `4599ee1aff95f21714e320a87fd31260f0435aa9c7a9884ac60ab952fe099a36` is **frozen in the
   driver** and must equal the computed transform, the observed production blob and the tool's
   self-reported `tool_sha256`; the file mode must be `100755` at baseline and target; the target
   must carry the v2 literal exactly once, the v1 literal zero times and the alias fragment zero
   times. This is a syntactic no-other-byte-delta constraint, not a behavioural proof.
   `C22` adds a three-mutant discrimination self-test of that guard (append / remove / whitespace);
   **no historical r22 mutant battery is adapted**.
8. **Output comparison corrected** — v1 paired the oracle's two *separate* runs, i.e. two different
   synthetic fixture instances, whose receipt bytes and embedded paths differ; that comparison
   could not be sound. v2's `C23` replays both tools on the **same synthetic fixture instance**:
   it reuses the oracle's own recorded `argv` and swaps only the tool path, so `sys.argv[1:]` is
   identical and `argv` must be **equal** (not special-cased). Only three keys are special:
   `schema` (v1→v2), the removed alias key (present before, absent after) and `tool_sha256`
   (before must self-report `0795bac9…`, after must self-report the frozen target
   `4599ee1a…`). Every other key — including `inputs_sha256`, `input_revision`,
   `measured_revision`, the hit lists and `argv` — must be equal, and the after replay must
   reproduce the oracle's recorded stdout byte-for-byte.
9. **Selftest** — `C24`: the selftest output must carry the v1 schema before and the v2 schema
   after, contain no alias key, and otherwise be an identical payload (v1 had no selftest handling).
10. **C1 real control** — `C25` now also requires the tool's self-reported `tool_sha256` to equal
    the frozen target SHA; the remaining facets are unchanged.
11. **Scratch** — v1 used `LANE/.scratch/round23/measure-<name>`; v2 uses the heavy scratch
    `/fast/scratch/hyaku/mori-r23/MeasureDriver` for its own files *and* for `TMPDIR`. `/tmp` is
    never used for a probe, an output or a download.
12. **Denominators** — the original 26 requirements keep their own denominator
    (`summary['c1_original_26'].denominator == 26`) and are never merged with the supplementary
    guards, which are reported separately in `summary['c1_supplementary']`.

### Unchanged from v1

The C2 oracle invocations (before with an absent tool path, after with the measured tool, and the
`--real-expected` run), the sealed-case denominators derived from the staged `*.json` files, the
direct C2 real control, the C1 real-control facet comparison, the `OUTPUT_DIR_PRESENT` guard
(exit 2), the exit-code convention (0 iff `all_claim_checks_pass`), the read-only git plumbing,
the absence of any privileged or mutating command, and the rule that a host drift on the C2 real
control is reported as drift rather than rewritten into the oracle.

### v2 pre-seal surgical fix (L1 source review, blocking bug)

The L1's source review found a blocking defect in the unsealed v2: the per-arm comparison
required the alias key and the tool digest on **every** arm, but a reconciler SETUP answer is
`{schema, finding_id, error, privacy_clearance, receipt_match}` and carries neither the alias nor
a tool digest (and no `argv`). The arms that fail that way are the setup arms
(`invalid-revision`, `diverged`, `malformed`, `symlink`, the `../receipt.json` arm).

Fix applied surgically to the same file (no new version, no other behaviour touched):

- a new helper `is_check_output(obj)` classifies an object as a **check** output when it carries
  `raw_total` and `receipt_match` (a check result) and as a **setup** envelope otherwise;
- a **check** arm must carry the alias before and not after, must self-report `0795bac9…` before
  and the frozen target `4599ee1a…` after, and its key set must be the before key set minus the
  removed alias;
- a **setup** arm must carry neither the alias nor `tool_sha256` on either side (their presence is
  flagged), and its key set must be exactly equal on both sides;
- every other key and value is compared on both shapes, `argv` included (it is no longer special:
  on the same fixture instance `sys.argv[1:]` excludes the tool path, so `argv` must be equal);
- a differing exit code, a differing stderr, an unparseable stdout, a missing output and a
  shape mismatch are all still recorded as differences — **no failing exit and no missing output
  is suppressed**;
- the C23 detail text and the module docstring were updated to state the two-shape rule, and the
  check now also reports the per-shape arm counts.

| Build | SHA-256 | Lines |
|---|---|---|
| v2 as first delivered (superseded, hash preserved for the record) | `82d581643e6cf4387226202efcf9e43ee02ea8db70b74e2db8e2e355eb3159c9` | 1080 |
| v2 after the surgical fix (current) | `3f5168b82a554d9217350d010ae6b2673a4b9dc2718c3b0d2c6f2933b7696689` | 1115 |

The C1 selftest was already handled separately by `C24` and was not touched by this fix. The v2
driver was not executed.

### v2 second pre-seal amendment (L1 bounded review, ReviewRealC1 F1)

The L1's last bounded pre-seal review found that the C1 real control pinned the **scalar**
expectations only, so an identity swap inside the observed population (`scanner_hits` ↔
`policy_excluded_hits`) would not be caught. The L1 copied `r22/frozen/expected-real-identities.json`
unchanged to `r23/frozen/c1-expected-real-identities.json` before the seal; that file is now part
of the sealed frozen set and is staged from the seal like every other frozen artefact.

Amendment applied surgically to the same v2 file (no new version, no execution):

- new **supplementary** check `C35.c1_real_identity_pins` (the original 26 denominator is
  untouched; it is reported in `summary['c1_supplementary']` and gates the overall verdict there):
  - the identity digest is the r22 driver's exact encoding —
    `sha256(json.dumps(sorted(tuple(h[k] for k in ('path','line','class','line_sha256')) for h in hits), separators=(',',':')).encode())`,
    default `ensure_ascii`, no JCS claim;
  - it is computed over `raw_hits`, `scanner_hits` and `policy_excluded_hits` of the **observed**
    real-control output and compared with the frozen `digests` map;
  - the same-command failing twin — the observed digests with `scanner_hits` and
    `policy_excluded_hits` swapped — must **not** match the frozen pins;
  - the frozen file's `receipt_sha256` pin is compared with the observed `inputs_sha256.receipt`;
  - a digest that cannot be computed (missing key, wrong type) is recorded as
    `identity_digest_error:<Type>` and fails the check; it is never swallowed;
  - when the real control is unavailable the check is registered as failed with the same reason, so
    it can never vanish silently and leave the supplementary conjunction vacuously true.
- the C21 source-byte guard now also cross-checks the frozen `c1-source-delta.json` artefact
  against the constants frozen in this driver (`entering_sha256`, `transformed_sha256`, `mode`,
  `entering_revision`, the two `replacements` pairs, `output_pair_normalization` and
  `same_fixture_required`); a disagreement fails `C21`. The frozen file's values agree with the
  driver's pins: baseline `0795bac9…`, target `4599ee1a…`, mode `100755`, normalisation
  `[schema, raw_unallowlisted, tool_sha256]`, same fixture required.

| Build | SHA-256 | Bytes / lines |
|---|---|---|
| v2 first delivery (superseded) | `82d581643e6cf4387226202efcf9e43ee02ea8db70b74e2db8e2e355eb3159c9` | 61281 / 1080 |
| v2 after the shape fix (superseded) | `3f5168b82a554d9217350d010ae6b2673a4b9dc2718c3b0d2c6f2933b7696689` | 63546 / 1115 |
| v2 after the identity-pin amendment (current) | `5c12fdc056309966d3e716d25e3427a7908056595383f0353655b42282fdfbcd` | 69853 / 1205 |

**Seal consequence for the L1**: `frozen/seal-manifest.json` still lists the driver at
`3f5168b8…` / 63546 bytes; that entry is now stale and must be regenerated for
`5c12fdc0…` / 69853 bytes before the seal. The v2 driver was not executed; only `ast.parse` and
`py_compile` static checks were run.

### v2 risks

- `C07` (the exact `tools/` delta) and `C13` (the executing driver equals the sealed driver) can
  only pass once L1 has sealed the v2 driver and the implementation commit exists; before that they
  fail with an explicit reason, which is the intended pre-state.
- The source-byte guard is a *byte* constraint: an implementation that also reformats the file
  fails `C21` even if it is behaviourally correct. That is the amendment's intent, but it means
  the guard is unforgiving about whitespace.
- `C23` replays on the oracle's fixture instances, so it inherits the fixture set of the sealed
  `oracle-rename.py`; if the seal changes the oracle's arm set, the replay follows it automatically
  (it enumerates the oracle's recorded runs, it does not hard-code a variant list).

### v2 run log

- Commands: read-only `git -C <lane> rev-parse / show / ls-tree / diff --name-status /
  cat-file`; `sha256sum`; `cp` of the finished file to the lane path; `python3 -m py_compile` and
  `ast.parse` on the v2 driver **as a static syntax check only**, run three times (first delivery,
  shape fix, identity-pin amendment).
- Tools installed or updated: none.
- Measurements, tests and builds: none run; the v2 driver was not executed.
- Files written: `.ufo/waves/round-23/build/MeasureDriver/measure-round23-v2.py` (new, then
  surgically amended twice in place) and this report (appended). `measure-round23.py` is untouched.
  No production, frozen, oracle or case file was modified; no git/jj mutation in the lane; no new
  seat was dispatched.

Report: .ufo/waves/round-23/build/MeasureDriver.md
