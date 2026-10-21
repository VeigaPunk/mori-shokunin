# ReportConformance — round-23 report conformance / evidence checklist

Seat: `MadoR22-2.ReportConformance` (scribe, wave2 `mori-r23-falsify`, leaf, no delegation).
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Round: mori round 23, attempt 1. L1: `MadoR22-2` (planner/integration).
Pinned production: `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`.
Expectation seal: `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687`.
Lane branch tip (git `master`, HEAD detached): `6eb889c037163e4886eaa61501258910d6a529b9`.

**What this document is.** A factual checklist of the report-contract items the round must
satisfy, the evidence that exists for each, and the scope deviations observed. It is not the
round report, not a verdict on admission, not a clearance claim, and it asserts no claim
result of its own. Every row below is either (a) a file/byte identity I read, (b) a recorded
receipt, or (c) an explicitly marked observation of absence.

**What this seat did.** Read-only: file reads, `grep`/`sha256sum`/`ls`, `git status|log|rev-parse|
merge-base --is-ancestor` (read-only subset), and read-only JSON parsing. **No** fixture run,
no oracle run, no driver run, no selftest run, no live host quota read, no mountinfo/sysfs
read, no scratch tree created, no source/frozen/oracle/expectation byte touched, no git write,
no jj mutation, no fleet-root write, no sibling write. The only byte written by this seat is
this file. Per the wave context, any `<seat>` scratch placeholder for this seat resolves to
`/fast/scratch/hyaku/mori-r23/ReportConformance/`; it was not needed and does not exist.

## 1. Axes named for this seat

1. **Report-contract completeness** — every clause of the dispatched round report contract
   has a named home in the round's artifacts, or is explicitly open.
2. **Evidence identity** — each required claim/evidence pointer resolves to an exact byte
   identity (path + sha256) or an exact field name, not an aggregate-only claim.
3. **Scope discipline** — frozen/expectation/production bytes unchanged, no special-casing
   of the strict red, no clearance/authority inflation, untracked/dead/disclosed deviations
   surfaced rather than hidden.

## 2. The required report contract (as dispatched)

Source of truth for this section: `/home/vgpnk/Projects/shokunin/.ufo/prompts/mori-round-23.md`
§4 "Report contract" (plus §1/§2b/§3/§5/§6 for the other round obligations), the fleet
`/home/vgpnk/Projects/shokunin/PROTOCOL.md` §report contract (lines ~149–248), and the
lane's own round-22 report `/home/vgpnk/Projects/shokunin/.ufo/reports/round-22/mori.md`
as the worked exemplar.

Required sections, **in order**:

| # | Section | Contract clause |
|---|---|---|
| R1 | **Work performed** | opens by naming the round's declared claims (1–3) and target axes/capability; one bullet per work item, each with an evidence pointer (path:line, command output, or commit hash) |
| R2 | **Landed changes** | every change tied to a `LOG.md` entry and to the commit hash carrying it |
| R3 | **Before → after measurements** | one per claim, each with the counting command and the commit it was measured against |
| R4 | **Sources & frontier** | `SOURCES.md` rows before→after with the counting command, rows added by tier, rows touched old→new, frontier rows advanced; `SOURCES: unchanged — …` form only for corpus-less lanes |
| R5 | **Trend verdicts** | one verdict each for `expansion`, `quality`, `discernment` (`improved`/`harmed`/`unchanged`/`unprovable-but-better`), with evidence, no scalar |
| R6 | **SHONEN** | one line per box of `SHONEN.md`: `[x]` only with a named non-author verifier, `[~]` with a resolvable evidence pointer, `[ ]` if untouched |

Additional binding obligations found in the same prompt/protocol: **Sources & frontier** and
**Trend verdicts** are conformance items, **not** marker predicates; a report missing
**Work performed**, **Landed changes**, **Before → after measurements** or **SHONEN**, or
carrying no evidence pointer, is a *contentless marker* and the round is **failed**;
a report naming real committed work but skipping R4/R5 is `ok` plus a minimum-content
conformance defect. Extra required lines: a **Stale-lane** line, any **tool installs**,
and a **misroot sweep** result. Commit citation rule: cite only the `jj-lane.sh` final
`landed <hash>` line; `rewritten <old> -> <new>` is diagnostic, never citable; record
measured/pinned revisions as the **branch tip**, never bare `HEAD` (git HEAD is detached in
this lane). The report must land **last** and cite the pushed lane hash.

## 3. Conformance checklist (status per item)

Status vocabulary: **MET** = artifact present and byte/field-verified; **OPEN** = required
but not yet produced (round still in flight); **DEVIATION** = produced but non-conformant;
**N/A-now** = deferred to a named later step that is itself declared.

### 3.1 Report-contract items

| Item | Status | Evidence (exact identity / field) |
|---|---|---|
| R1 Work performed: claims named with axes | **MET (claim side)** | `SCORECARD.md:1413` "Round23 declaration — misleading-field cutover and quota-surface coverage"; claims C1 (calibration 5→5, lowest tie with depth/freshness) and C2 (coverage 6→6, FR2). Declared, not yet verified. |
| R1 Work performed: per-item evidence pointers | **OPEN** | Wave-2 seat reports are landing now (see §4.3); the wave-2 presence list must be bound before the report cites them. |
| R2 Landed changes tied to LOG.md + commit hash | **MET (log side)** | `LOG.md:1524` (declaration), `:1537` (source review), `:1564` (seal), `:1592` (production integration), `:1612` (first measurement defect), `:1627` (frozen contradiction), `:1647` (guards + selftest input correction), `:1665` (stable guards + falsification payload). Commits on `master`: `4dc80c1`, `c1e8b81`, `22772c1`, `1979a9d`, `5729e7f`, `56ac3ba`, `f3dc07c`, `6eb889c`. |
| R3 Before→after measurements with counting command | **MET (receipt side)** | `evidence/measure4-invocation.json` records argv `python3 -I …/build/MeasureDriver/measure-round23-v2.py --revision f3dc07c0… --seal 22772c10… --output …/evidence/measure4`, exit **1**, stdout `{"after":{"c1_original_26":{…,"pass":26,"total":26,"unmet":0},"c2":{…,"pass":29,"total":30,"unmet":1}}, "all_claim_checks_pass": false, …}`. Driver sha256 `5c12fdc056309966d3e716d25e3427a7908056595383f0353655b42282fdfbcd` = seal-manifest entry. |
| R4 Sources & frontier: rows before→after | **MET** | `evidence/source-accounting.json`: `before_rows` 76 → `after_rows` 86, `new_ids` S077–S086 (10 rows, tier A per `corpus/SOURCES.md:83-92`), `before_revision` `1bfe708a…`. Start census receipt `evidence/sources-start.txt`: `exit=0`, six `W04` duplicate-URL warnings (S035, S037, S073–S076), ok on `corpus/SOURCES.md`. |
| R4 Sources & frontier: rows touched old→new | **MET** | `corpus/lessons/round-23.md` §"Scope and remaining debt": used-by for all ten S077–S086 changed `corpus/lessons/round-23.md` → `corpus/lessons/round-23.md, corpus/knowledge/quota-surface-r23.md`; `mined`/`on-release` unchanged; no existing immutable row edited. Ten `corpus/lessons/round-23.md` mentions in `corpus/SOURCES.md`. |
| R4 Sources & frontier: frontier rows advanced | **DEVIATION (see §5 D1)** | `corpus/README.md:333` FR2 row still reads only "`df` capacity percentages cannot detect quota exhaustion; observe and report only, never change quota state." — unchanged by r23; and `corpus/README.md` contains **no** row pointing at `corpus/knowledge/quota-surface-r23.md` (grep for `quota` in `corpus/README.md` returns only line 333). The r22 exemplar row exists at `corpus/README.md:420`. |
| R4 end-of-round census exit 0 | **OPEN** | Only the start receipt exists (`evidence/sources-start.txt`, `exit=0`). The end-of-round census is a round-end obligation for the L1; no end receipt is present in `evidence/`. |
| R5 Trend verdicts | **OPEN (L1)** | Must be `expansion`/`quality`/`discernment` with evidence, no scalar. Candidate inputs already in the lane: `SCORECARD.md` round-22 trend block ("expansion unchanged, quality improved, discernment improved") and the r23 evidence set. |
| R6 SHONEN: one line per box | **OPEN (L1)** | `SHONEN.md` has exactly **4** boxes (SKILL.md decision tables / end-to-end task in LOG.md / executable without oral context / no cross-domain bleed). All four are currently `[ ]` in the file; the report may mark `[x]` **only** with a named non-author verifier, otherwise `[~]` + pointer. The outside non-author verification for r23 is not yet recorded → `[x]` is not yet available on evidence. |
| Report path | **OPEN** | Contract path `/home/vgpnk/Projects/shokunin/.ufo/reports/round-23/mori.md` — **absent**; `/home/vgpnk/Projects/shokunin/.ufo/reports/round-23/` currently holds `kagi.md, kaidoku.md, kake.md, kama.md, kotodama.md, tameshi.md, tsukuroi.md` only. It must land last and cite the pushed lane hash. |
| Stale-lane line | **OPEN (L1)** | Prompt §6 requires the line (respawn-per-round driver; no other mori mission open). |
| Tool installs line | **MET (negative)** | No tool install or upgrade was performed by this seat, and no install is recorded for the round in `LOG.md`; the report's tool-install line should stay empty/none. |
| Misroot sweep | **MET (currently clean)** | `git -C /home/vgpnk/Projects/shokunin status --porcelain` (no pathspec) shows only `M .ufo/state/*.report-baseline` and `M .ufo/watchdog.log` (driver-owned), `?? .ufo/state/{kotoba,kotodama,revenger}.report-baseline` (driver-owned), and `?? .ufo/reports/round-22/souji.md` — a **sibling lane's** own report, not a mori seat file, and therefore not mine to touch. No mori r23 seat output is misrooted at the fleet root at check time. |
| Prompt embed / route-map conformance | **MET (prompt side)** | `/home/vgpnk/Projects/shokunin/.ufo/prompts/mori-round-23.md` carries §1 MISSION/AXES binding, §2 claims, §2b frontier step, §3 L2 floor, §4 report contract, §5 commit/push scope + L0 channel, §6 campaign addendum. |
| Commit citation form | **OPEN (L1)** | Only `landed <hash>` lines are citable. Lane tip is `master` = `6eb889c037163e4886eaa61501258910d6a529b9`; `git HEAD` is detached (`(no branch)`), so `HEAD` must not be cited as the tip. The measurement revision is the **parent** `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`; the report must name which revision each number was measured against. |

### 3.2 Claim-evidence items (facts, not admissions)

| Item | Status | Exact field/byte evidence |
|---|---|---|
| C1 original denominator | **MET (measured)** | `evidence/measure4/summary.json` → `c1_original_26`: before `{"pass":25,"total":26,"unmet":["R25"],"misleading_alias_runs":8}`, after `{"pass":26,"total":26,"unmet":0,"misleading_alias_runs":0}`; `denominators.c1_original_requirements` = 26. Oracle receipt `evidence/measure4/c1-oracle-after.json` stdout: `{"counts":{"capability_absent":0,"misleading_alias_runs":0,"pass":26,"total":26,"unmet":0},"finding_id":"R23_C1_REQUIREMENTS_MATCH"}`, exit 0. |
| C1 supplementary guards (reported apart from the 26) | **MET (measured)** | `summary.json` → `c1_supplementary.pass` = true, guard names `same_instance_replay`, `selftest`, `source_byte_guard`, `source_guard_mutants`; `denominators.c1_supplementary_guards` = 5, kept separate from the original 26 (`summary.json` note: "supplementary guards are reported apart from the original 26 denominator"). Source-guard baseline: `tools/mori-retention-reconcile.py` sha256 `0795bac9367c33e534b79599114c1635d83c4b0e4a57fbbe235644858a59de32`, mode `100755`. |
| C1 production cutover shape | **MET (byte-read)** | `tools/mori-retention-reconcile.py:16` `SCHEMA='mori-retention-reconciliation-v2'` (used at `:231` check, `:274` selftest, `:287`/`:289` setup envelopes); `:234-235` emits `'scanner_unallowlisted'` and `'raw_not_allowlisted'`; grep count of `raw_unallowlisted` in the production tool = **0**; the same cutover is documented in SKILL.md Round23 section and `corpus/knowledge/retention-reconciliation-r22.md:44-52` "Round23 API correction — schema-v2 clean cutover". |
| C2 sealed-case population | **MET** | `summary.json` → `c2.cases_count` 30, `cases_source` "staged from the committed seal bytes", `oracle_sha256` `f1f4a027728180436fc5161171b0f6ad4ca4176229b5240aabb33e3f2af36bec`; `seal_proof.sealed_cases` lists the 27 primary + 3 supplemental (`SupplementHiddenMount`, `SupplementQgroupDisabled`, `SupplementQgroupUnknown`); `denominators.c2_sealed_cases` = 30. |
| C2 before → after | **MET (measured)** | `summary.json` → `c2.before` `{"capability_absent":30,"pass":0,"total":30}`; `c2.after` `{"capability_absent":0,"pass":29,"total":30,"unmet":1}`. Oracle receipt `evidence/measure4/c2-oracle-after.json` stdout: `{"counts":{"capability_absent":0,"pass":29,"total":30,"unmet":1},"finding_id":"R23_C2_QUOTA_CASES_UNMET","supplementary_counts":{"pass":274,"total":274,"unmet":0},"tool_present":true}`, exit **1**. |
| C2 strict red — identity of the failing case | **MET (retained, unchanged)** | `evidence/frozen-contradiction.json`: case `.ufo/waves/round-23/frozen/quota-cases/CaseEscapedSpace.json`, `case_sha256` `8340738a509e474a94a815637e46b407dfb60c6449511e52db55296d844abeea`; `selected_mount_id` 43, `selected_parent_id` 33, `longest_strictly_shorter_cover` = mount 42 `/srv`, `parent_present_in_snapshot` true; `sealed_rule_required` = unknown / n/a / `ambiguous_overmount`; `frozen_expected` = exit 1 `QUOTA_ENABLED` with an enabled `/srv/my data` row; `actual` = exit 2 `QUOTA_STATE_UNKNOWN` with `ambiguous_overmount` / `device_check` `not_checked`; `disposition`: "Contradictory pre-sealed expected output and parent-ID rule. Keep both unchanged. No exception/special case/exclusion/relabel. Strict C2 target unprovable, not admitted". Main's ruling: `evidence/parent-strict-target-disposition.txt`. |
| Driver exit code | **MET (expected red)** | `evidence/measure4-invocation.json` `exit` 1 — the strict red. `summary.json.all_claim_checks_pass` = false and `real_controls_pass` = false; the two failing checks are `C34.c2_after_every_case_matches` (29/30) and `C30.c2_oracle_real_control_agrees` (oracle exit 1, `unmet` 1). |
| Real control (default pair) | **MET (matched)** | `summary.json.c2.real_control`: `exit_code` 0, `finding_id` `QUOTA_DISABLED`, `match` true; fleet root `/home/vgpnk/Projects/shokunin` → fstype `btrfs`, mount `/home`, `disabled`, `btrfs_qgroups_dir_absent`, `device_check` `btrfs_subvolume_skipped`; `/tmp` → fstype `xfs`, mount `/tmp`, `disabled`, `xfs_noquota_option`, `device_check` `match`. |
| Frozen bytes unchanged | **MET (re-verified by hash now)** | Recomputed sha256 equals the seal manifest entries: `frozen/quota-cases/CaseEscapedSpace.json` `8340738a…ebeea`; `frozen/c1-requirements.json` `88e1b912…f3184`; `frozen/case-decisions.json` `b05a0072…c60a`; `oracle-quota.py` `f1f4a027…36bec`; `oracle-rename.py` `a55b2b50…7c5f2`; `build/MeasureDriver/measure-round23-v2.py` `5c12fdc0…fdbcd`. `summary.json` `C08.frozen_byte_identical_seal_to_revision` (37 files, `divergent` []), `C09.sealed_oracles_byte_identical` [], `C10` contract+amendment byte-identical, `C12.working_copies_match_committed_seal_bytes` [], `C13.driver_matches_sealed_bytes` true. |
| Seal ordering | **MET** | `summary.json.ancestry`: `git -C … merge-base --is-ancestor 22772c10f6e3c1d8d3fe1b72083a6194e9f4e687 f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` returncode 0, `seal_equals_revision` false, `seal_is_strict_ancestor_of_revision` true. Independently re-verified by this seat (same command, returncode 0). `C02` quota production path absent at seal, `C03` reconciler entering-identical at seal (`0795bac9…de32` both sides), `C07` tools delta exactly `A tools/mori-quota-surface.py`, `M tools/mori-retention-reconcile.py`. |
| Quota selftest (co-evolved input, distinct from the frozen case) | **MET** | `evidence/quota-selftest-corrected.json`: argv `python3 -I …/tools/mori-quota-surface.py --selftest`, `measured_revision` `f3dc07c0…`, exit 0, stdout `{"arms":49,"exit_code":0,"finding_id":"QUOTA_SELFTEST_OK","schema":"mori-quota-surface-v1"}`. This arm is **not** `CaseEscapedSpace`; `corpus/lessons/round-23.md` §"Frozen rule versus inconsistent expected topology" states the correction was to the co-evolved selftest **input** only (`st_dev` 259:2), with the frozen topology case, its expected row and its rule untouched and still red. |
| Carried open debt (unchanged) | **MET** | `summary.json.carried_open_debt`: `unallowlisted_retention_hits` 4, `original_permission_control` "RED 11/12 retained byte-unchanged, not rerun", `historical_dispositions` "two unknown", `baseline_acceptance` "blocked", `privacy_clearance` false; `summary.json.privacy_clearance` false. `evidence/retention-floor-comparison.json`: `metric` 4, `raw` 95, `allowlisted` 86, `non_author` 5, `new_unallowlisted` 0, `missing_unallowlisted` 0, `same_inherited_identities` true, `privacy_clearance` false. |

### 3.3 Frontier-step (round prompt §2b) items

| Item | Status | Evidence |
|---|---|---|
| `corpus/SOURCES.md` curated; rows written only after opening | **MET** | Rows S077–S086 at `corpus/SOURCES.md:83-92`, tier A, `mined`, `2026-10-21`, `on-release`, each with raw-source digest; lesson Gate carries URL, access date and ≤25-word located quote for all ten (`corpus/lessons/round-23.md:34-63`). Raw bytes retained under `evidence/sources/` + `sources-manifest.json`. |
| Census before → after recorded | **PARTIAL** | Start receipt `exit=0` (`evidence/sources-start.txt`); after-count recorded as rows 76→86 in `evidence/source-accounting.json`; the **end-of-round census command output/exit code is not yet in `evidence/`** (OPEN, L1). |
| One mined mistake recorded | **MET** | `corpus/lessons/round-23.md:21` §Mistakes, M1–M8, each with class · evidence pointer · captured-by · fix; M8 records the L1/seat tool-policy deviations (shell `sed`/`grep`/`ls` + Python edits, transient `/tmp` uses by W1 seats `CaseOptionalFields`/`DraftSourceRows`, sibling-case exposures disclosed by `TmpfsUsrquota`/`SetupMalformed`/`NoCover`/`SymlinkRealpath`). Captured-by for the frozen-topology lesson is the **existing** QUALITY55, so no new criterion is required for it. |
| ≥1 sourced claim citing an S-row | **MET** | C2 rests on S077–S086; `corpus/knowledge/quota-surface-r23.md` header `source: S077–S086 in corpus/SOURCES.md`. |
| Knowledge note landed | **MET (not indexed)** | `corpus/knowledge/quota-surface-r23.md` exists (source corrections, decision table, ownership fence, final mode-safety qualification). **Not** referenced from `corpus/README.md` (see §5 D1). |

## 4. Wave-2 falsification state (as observed by this seat)

### 4.1 Dispatch/chronology facts
- `wave2-ledger.json` — attempt 1, `dispatch_path` `.ufo/waves/round-23/wave2-run.json`, `payload_sha256` `d28cc9f2dbf120831d85277e0fa47f0c10b658c4bafc0a36b4099ac069103efd`, `payload_bytes` 159710, `tasks_count` 96, `started_ids` 96, `result` "started".
- `evidence/wave2-payload-binding.json` — `mori-dispatch-ledger.py bind --rev 6eb889c037163e4886eaa61501258910d6a529b9`, exit 0, `finding_id` `PAYLOAD_BOUND`, `status` "bound", `tasks_count` 96 — i.e. the pre-call payload digest is bound to a committed revision for W2 (the W1 retrospective binding debt is recorded separately, §5 D6).
- `wave2-spec.json` — `wave` `mori-r23-falsify`, `reportDir` `.ufo/waves/round-23/falsify`, `maxLanes` 100, 96 items; my seat's item prompt is the one this seat is executing.
- `.ufo/waves/round-23/falsify/swarm-registry.json` — `ufo-swarm-registry-v1`, `reportDir` `.ufo/waves/round-23/falsify`, `createdAt` 2026-10-21T18:28:45Z.

### 4.2 Seat reports present at check time
Two snapshots taken during this seat's read: **52** `.md` seat reports + 33 seat scratch
directories + `swarm-registry.json` at the first listing, and **69** `.md` reports + 39 seat
scratch directories at the second listing (the second count includes this seat's own
`ReportConformance.md`). Named examples observed: `C1R06.md`, `C1R08.md`, `C1R09.md`, `C1R10.md`,
`C1R13.md`, `C1R19.md`, `C1R20.md`, `InspectModeSafety.md`, `InspectMountScope.md`,
`MutAliasReturn.md`, `MutExtEnabled.md`, `MutModeRead.md`, `MutMountParent.md`,
`MutOutputLeak.md`, `MutQgroupPresence.md`, `MutSetupPartial.md`, `MutTmpfsSuffix.md`,
`QEscapedSpace.md`, `QHiddenMount.md`, `QNoCover.md`, `QStacked.md`, `QSymlinkRealpath.md`,
`QTmpfsHardlimit.md`, `QQgroupDisabled.md`, `QQgroupUnknown.md`, `QSetupMalformed.md`,
`QOptionalFields.md`, `QEnabledPlusUnknown.md`, `QUnsupported.md`, `QXfsDevMismatch.md`,
`QBtrfsDevMatch.md`, `QBtrfsSquota.md`, `QBtrfsTwoUuids.md` and others. **This is a
presence count observed at one instant, not a settlement result** — the wave is still running
and the list grew during this seat's read.

### 4.3 Items that must exist before the round report may cite wave-2 results
- A wave-2 **report-presence** record analogous to `evidence/wave1-report-presence.json`
  (64/64 present, each with path/bytes/sha256 and native assignment id). No wave-2 equivalent
  exists yet.
- A **dead-seat** record: neither `.ufo/waves/round-23/dead-seats-wave1.json` nor
  `.ufo/waves/round-23/dead-seats-wave2.json` exists at check time (both are **absent** from
  `.ufo/waves/round-23/`; the r22 round directory does retain `dead-seats-wave1.json` /
  `dead-seats-wave2.json`, so the r23 equivalents are simply not written yet).
- A **settlement scan** receipt (r22 precedent: `evidence/settlement-final.json`). No r23
  settlement artifact is present in `.ufo/waves/round-23/evidence/`.
- A **misroot sweep** receipt file for r23 (r22 precedent: `evidence/misroot-sweep.json`); the
  raw `git status` output was observed by this seat (§3.1) but no r23 receipt file exists yet.

## 5. Scope deviations (factual, numbered; none invented)

**D1 — Frontier row / knowledge index not advanced (conformance defect).** `corpus/README.md:333`
FR2 is unchanged by round 23 and still describes only df's blindness to quota exhaustion; no
`corpus/README.md` row points at the new `corpus/knowledge/quota-surface-r23.md` (grep for
`quota` in that file returns only line 333), while the r22 note is indexed at line 420. The
report's R4 section must therefore state the frontier movement explicitly (the r23 note records
FR2 as advanced only for *visible mechanism state*, with limits/usage/EDQUOT attribution still
frontier) rather than imply an indexed frontier advance. Fixing the index is a lane-side write
and is **not** this seat's scope.

**D2 — Round report not yet filed.** `/home/vgpnk/Projects/shokunin/.ufo/reports/round-23/mori.md`
does not exist at check time. It must be filed last, cite the pushed lane hash from the
`jj-lane.sh` `landed <hash>` line, and carry R1–R6; otherwise the round is a marker/failed
lane-round under PROTOCOL.

**D3 — End-of-round sources census receipt absent.** Only the start receipt exists
(`evidence/sources-start.txt`, `exit=0`, rows 76, six `W04` warnings). The end-of-round
census command output and exit code are a conformance requirement of prompt §2b step 2 and
must be captured before the report is filed.

**D4 — Wave-2 closure artifacts incomplete.** Wave-2 report presence, dead seats and
settlement are not yet recorded (§4.3). The prompt requires each wave's seat count, role mix,
dead seats and round total in the report.

**D5 — Uncommitted round artifacts in the lane working tree.** `git status --porcelain` in the
lane shows untracked `.ufo/waves/round-23/wave2-assignments.json`,
`wave2-attempt1-start.json`, `wave2-ledger.json`, `wave2-record.json`, `wave2-response1.json`,
`evidence/wave2-payload-binding.json`, the whole `falsify/` tree, plus
`__pycache__/` directories (`.ufo/waves/round-22/frozen/__pycache__`,
`.ufo/waves/round-23/__pycache__`, `tools/__pycache__`) and `.scratch/`. Under the
landed-means-committed rule these are round work to be committed (via the helper) or reverted;
`.scratch/` is intentionally excluded by contract item 3 (646 MB at entry, stays uncommitted),
and `__pycache__` should not be committed.

**D6 — Wave-1 chronology debt already disclosed (carried, not hidden).** `LOG.md:1583-1586`
records that `wave1-ledger.json` is a **retrospective** binding of seven zero-spawn refusals and
one 64-seat start, not proof of pre-call committed payload logging, and that "Q53/56's chronology
is not retroactively satisfied". The r23 W2 binding is by contrast pre-call
(`evidence/wave2-payload-binding.json`, `PAYLOAD_BOUND`, bound to `6eb889c…`).

**D7 — W1 process deviations already disclosed.** `corpus/lessons/round-23.md` M8 and
`LOG.md:1587-1591` record static source/fixture in-memory checks and `py_compile`, plus three
disclosed transient `/tmp` uses by W1 seats, exceeding W1's no-verification/scratch prose;
"no candidate or live quota command ran". These are conformance debt, never hidden by a final
clean tree, and must appear in the round report's Mistakes/procedural-disclosure text.

**D8 — Strict C2 red is a fact of the round, not a defect to repair.** The driver exits 1 and
`all_claim_checks_pass` is false, with `C34` (29/30) and `C30` (oracle exit 1, `unmet` 1)
failing on `CaseEscapedSpace` alone. `evidence/frozen-contradiction.json` and
`evidence/parent-strict-target-disposition.txt` bind the contradiction and Main's ruling
(no special-casing, no exclusion, no relabel, no expectation rewrite; strict C2 unprovable, not
admitted). The report must present C1 (26/26 with the 5 supplementary guards reported apart
from the original denominator) and C2 (29/30) as separate claims, and must not present an
aggregate "30/30" or "capability demonstrated".

**D9 — Reporting boundaries observed by this seat.** No live host quota read was performed
(no `quotactl`/`btrfs`/`xfs_quota`/`repquota`/`mount`, no `qgroups`/`mode` read, no
`/proc/self/mountinfo` read); no fixture, oracle, driver or selftest was executed; no transcript
or session file was read; no credential/auth/`agent.db` file was touched; no fleet-root, sibling
or frozen/oracle/production byte was written; no git write or jj mutation was performed.

## 6. Factual summary for the L1's report (no admission asserted)

- **C1 (calibration, declared held 5)** — measured at `f3dc07c0…`: original 26 requirements
  25/26 before → **26/26 after**, `misleading_alias_runs` **8 → 0**, schema
  `mori-retention-reconciliation-v2` on 18 parsed runs, `raw_unallowlisted` absent from the
  production source and from every parsed output, plus 5 supplementary guards (source-byte,
  output-object-equality, selftest-schema, same-instance replay, real-identity) green and
  reported **apart from** the original-26 denominator. Frozen bytes unchanged; seal a strict
  ancestor of the measured revision. **This is a measurement, not an admission.**
- **C2 (coverage, declared held 6)** — measured at `f3dc07c0…`: 30/30 `capability_absent`
  before → **29/30 exact matches after**, 274/274 supplementary output checks green, default
  real control exit 0 `QUOTA_DISABLED` matching the frozen control. The single red is
  `CaseEscapedSpace`, whose sealed expected row contradicts the sealed parent-ID rule; both are
  retained unchanged. Strict C2 stays **UNPROVABLE** at 29/30 per the contract and Main's
  ruling.
- **Carried debt unchanged** — 4 unallowlisted retention hits (raw 95 / allowlisted 86 /
  non-author 5), original permission control RED 11/12 (not rerun), two unknown historical
  dispositions, baseline acceptance blocked, `privacy_clearance` false. Probe visibility is not
  clearance, health or admission.

## 7. Outstanding for the L1 (ordered, each with its required artifact)

1. Run and record the **end-of-round sources census** (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`) — exit 0 required for conformance; paste both outputs/exit codes in R4.
2. Produce the **wave-2 report-presence, dead-seat and settlement** records, and bind each wave-2 seat report by path/bytes/sha256 before citing any falsifier conclusion.
3. Resolve the **untracked lane artifacts** (D5) through the helper (commit the round evidence; keep `.scratch/` out; do not commit `__pycache__`).
4. File the **round report** at `/home/vgpnk/Projects/shokunin/.ufo/reports/round-23/mori.md` with R1–R6 in order, the Stale-lane line, the tool-install line (none), the misroot sweep result, the disclosed deviations (D6, D7, D8) and the r23 frontier statement that does **not** claim an indexed FR2 advance unless D1 is fixed lane-side.
5. Cite only `landed <hash>` values; record revisions as the branch tip `master` (`6eb889c0…`) and name the measured revision `f3dc07c0…` per measurement.
6. Keep C1 and C2 verdicts separate and unaggregated; state the strict C2 disposition as unprovable/not admitted, with the contradiction file as the pointer.

## 8. Artifact paths (absolute)

- Round contract: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/contract.md`
- Pre-seal amendment: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/preseal-amendment.md`
- Seal manifest: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/frozen/seal-manifest.json`
- Case decisions: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/frozen/case-decisions.json`
- Sealed C2 cases: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/frozen/quota-cases/`
- Oracles: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/oracle-quota.py`, `…/oracle-rename.py`
- Driver: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/build/MeasureDriver/measure-round23-v2.py`
- Measurement: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/evidence/measure4/summary.json`, `…/evidence/measure4-invocation.json`
- Contradiction + ruling: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/evidence/frozen-contradiction.json`, `…/evidence/parent-strict-target-disposition.txt`
- Selftest receipt: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/evidence/quota-selftest-corrected.json`
- Retention floor: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/evidence/retention-floor-comparison.json`
- Sources: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/evidence/source-accounting.json`, `…/evidence/sources-start.txt`
- Lesson / knowledge: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-23.md`, `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/knowledge/quota-surface-r23.md`
- Registry rows: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md:83-92`
- Frontier table: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/README.md:333`
- Round declaration (lane scorecard): `/home/vgpnk/Projects/shokunin/mori-shokunin/SCORECARD.md:1413`
- Lane log: `/home/vgpnk/Projects/shokunin/mori-shokunin/LOG.md:1524-1700`
- Checklist seed: `/home/vgpnk/Projects/shokunin/mori-shokunin/SHONEN.md`
- Dispatched prompt (report contract): `/home/vgpnk/Projects/shokunin/.ufo/prompts/mori-round-23.md`
- Fleet protocol (report contract): `/home/vgpnk/Projects/shokunin/PROTOCOL.md:149-248`
- Worked exemplar (r22): `/home/vgpnk/Projects/shokunin/.ufo/reports/round-22/mori.md`
- This seat's report: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/ReportConformance.md`

**Standing limits.** This report carries no admission, no clearance, no promotion, no
baseline-acceptance change, no Core movement, no retirement, no waiver and no round-24
initiation. It records observed facts and open items only.
