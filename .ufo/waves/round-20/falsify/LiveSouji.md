# LiveSouji: C2 falsification, souji-shokunin per-dispatch settlement

**Verdict: PARTIAL**

- **Per-dispatch accuracy (assigned comparison): HOLDS.** 12 dispatch files, 783 members. The tool scan (08:01:46), the wave-1 GT (07:34:32) and an independent live probe agree on every member status, per-file count, state and missing list. There are zero unexplained differences. Two byte-count deltas and one labelling convention are explained in section 2.
- **Lane coverage: BROKEN (round 19).** `round-19/w1` is a dispatched wave (registry: 90 `spawn` seats; 67 reports on disk), but it has no dispatch-schema JSON, so `scan` never discovers it. GT shares the same blind spot. See F1.
- **Live change (explained, not a tool error):** `AuditCase07.md` moved from the fleet root into the souji lane at 08:09:21. `round-20/final` went from partial (63/64) to settled (64/64). The committed fleet scan (07:46:53) is now stale for souji (`misrooted` 1, now 0).
- **Tool drift during the run:** `tools/mori-wave-settlement.py` was modified four times by a writer other than me (08:11:12, 08:13:06, 08:15:18, 08:15:31; now 710 lines, 30,142 bytes, sha256 `c134c57b…`). Every scan on this tree produced byte-identical output across those versions (sha256 `a842e7fa…`, scan3–scan6). Selftest passed 23/23 each time.

## 1. Per-dispatch comparison

Columns: tool at 08:01:46 (`falsify/LiveSouji/scan.json`) / GT at 07:34:32 (`build/GtLaneSouji.md`, `build/GtLaneSouji/trailers.tsv`) / live probe (`falsify/LiveSouji/compare.py`, 08:06).

| Dispatch file | Members | Present (tool / GT / live) | Missing (tool / GT, excl. misrooted) | Misrooted (tool / GT) | Stub | Empty | State (tool = GT-derived = live) |
|---|---:|---|---|---|---:|---:|---|
| round-13/w1 | 32 | 32 / 32 / 32 | 0 / 0 | 0 / 0 | 0 | 0 | settled |
| round-14/w1 | 32 | 32 / 32 / 32 | 0 / 0 | 0 / 0 | 0 | 0 | settled |
| round-15/w1 | 64 | 64 / 64 / 64 | 0 / 0 | 0 / 0 | 0 | 0 | settled |
| round-16/w1 | 65 | 63 / 63 / 63 | 2 / 2 | 0 / 0 | 0 | 0 | partial |
| round-16/w2 | 79 | 78 / 78 / 78 | 1 / 1 | 0 / 0 | 0 | 0 | partial |
| round-17/w1 | 78 | 78 / 78 / 78 | 0 / 0 | 0 / 0 | 0 | 0 | settled |
| round-17/w2 | 71 | 43 / 43 / 43 | 28 / 28 | 0 / 0 | 0 | 0 | partial |
| round-18/w1 | 91 | 91 / 91 / 91 | 0 / 0 | 0 / 0 | 0 | 0 | settled |
| round-18/w2 | 79 | 79 / 79 / 79 | 0 / 0 | 0 / 0 | 0 | 0 | settled |
| round-20/final | 64 | 63 / 63 / 63 | 0 / 0 | 1 / 1 | 0 | 0 | partial at 08:01; settled 64/64 after 08:09:21 |
| round-20/recovery | 64 | 39 / 39 / 39 | 25 / 25 | 0 / 0 | 0 | 0 | partial |
| round-20/w1 | 64 | 0 / 0 / 0 | 64 / 64 | 0 / 0 | 0 | 0 | unsettled |
| **Total** | **783** | **662 / 662 / 662** | **120 / 120** | **1 / 1** | **0** | **0** | 6 settled, 5 partial, 1 unsettled |

- Per-trailer: 783 of 783 statuses agree across tool, GT and live probe. Parse: 783 of 783 trailers parse under both the GT rule and the tool rule, and the two paths are equal. Missing name lists: 12 of 12 files equal. Six GT `Missing` groups in `GtLaneSouji.md` equal the live sets.
- Lane totals from `scan.json`: members 783, present 662, missing 120, misrooted 1, empty 0, stub 0, unparsed 0, unsafe 0, waves 12, states partial 5 / settled 6 / unsettled 1, `ignored_json` 43, `unreadable_json` 0, exit 1.
- Committed `evidence/c2-live-fleet.json` (07:46:53), souji entry: members 783, present 662, missing 120, misrooted 1, empty 0, unparsed 0, unsafe 0, unreadable_json 0, waves 12, exit 1. It matches the 08:01 scan exactly. It holds **lane totals only**, with no per-wave or per-trailer records, so a per-dispatch comparison against it is impossible (evidence gap, not a difference).

## 2. Every difference, explained

- **D1. Byte counts (GT `lane_bytes`), 2 rows, status unchanged.** Both are in `round-20/recovery`, both written after the GT snapshot:
  - `OracleAuditCases.md`: GT 4001 B, now 3878 B. mtime 07:38:16.163 (GT write 07:34:32.426).
  - `OracleCallerCases.md`: GT 6965 B, now 7692 B. mtime 07:54:52.432.
  - Cause: live lane change. Presence is unchanged, and the tool emits no bytes ("Report bytes are never emitted", `contract.md:76-77`), so the tool is not affected.
- **D2. Labelling convention, not a count difference.** GT's `Missing` = tool `missing` + `misrooted`. GT says "Missing includes the 1 misrooted entry" (`GtLaneSouji.md`, F1 and table). The tool keeps `misrooted` separate (`tools/mori-wave-settlement.py:242-245`, counted in `counts.misrooted`). Its wave `missing` name list includes misrooted members (`:299`), as `contract.md:75-77` requires. So 120 + 1 = GT 121, and the committed fleet scan's `missing` 120 is the same convention.
- **D3. `AuditCase07` relocation: live change after the scan.** The tool was correct at each instant:
  - 08:01:46: the lane copy was absent and a regular file of 8,784 B existed at the fleet root. `_member_status` returned `misrooted` (`:242-245`). GT agrees (fleet bytes 8,784).
  - 08:06 (`compare-out.txt`): `misrooted_member round-20/final-dispatch.json AuditCase07 … fleet_bytes 8784`.
  - 08:09:21.087827 (`mtime = ctime`): `souji-shokunin/.ufo/waves/round-20/final/AuditCase07.md` created, 8,784 B. The lane's `round-20/final/` directory mtime is the same instant.
  - 08:09:21.090827: `.ufo/waves/round-20/final/` at the fleet root changed (entry removed). It now holds 0 entries.
  - Only one fleet path changed after GT: a directory-entry check of fleet `.ufo/waves` finds no file newer than 07:34:32, and the only changed directory is `round-20/final` (08:09:21). The fleet `.ufo/waves` file count went 1,954 (GT note) → 1,953 (now), which is consistent with this single removal.
  - Content and path check: the lane copy's first line is `# AuditCase07: round-20 C1 case deliver-exact-patch (source-only falsifier)`. The souji `final-dispatch.json` task for AuditCase07 says `Report: write your scoped findings to .ufo/waves/round-20/final/AuditCase07.md`. So the lane path is the expected one, and the report was written to the fleet root and then moved (or copied and removed) into the lane.
  - After the change, `scan3` (08:10:19) and later scans show `round-20/final` settled 64/64, totals present 663 / misrooted 0, states partial 4 / settled 7 / unsettled 1, exit still 1 (other waves are not settled). The per-seat probe against the post-change scan (`compare-out-post-relocation.txt`) reports `live_vs_tool` 0 mismatches. The only GT mismatch is `AuditCase07`.
  - Mover identity: not observable from the filesystem. [INFERENCE: copy-then-remove by an agent or the orchestrator.]
- **D4. Committed fleet scan is stale for one member.** Its souji `misrooted: 1` (07:46:53) no longer holds (see D3). Any consumer should re-run the scan.
- **D5. GT round-19 status is incomplete, not wrong.** GT F3 says round 19 has no dispatch-schema file, so dispatch state is unobserved [INFERENCE]. The registry evidence in F1 shows dispatch state is observable. Both GT and the tool omit round 19.

## 3. F1 (BROKEN): round 19 w1 is outside discovery

Evidence (all paths under `souji-shokunin/.ufo/waves/`):
- `round-19/w1/swarm-registry.json`: schema `ufo-swarm-registry-v1`, wave `souji-r19-w1b`, `reportDir` `.ufo/waves/round-19/w1`. Its 90 members all have `kind: "spawn"` and `agentId: null`. mtime 02:40:44 local (matches `updatedAt` 05:40:44Z).
- `round-19/w1-spec.json`: 90 items, names identical to the registry keys.
- `round-19/w1b-spec.json`: 68 items, all inside the registry. 67 have reports; `ReviewerRevPinHelper` does not.
- `round-19/w2-spec.json`: 65 items. There is no `round-19/w2/` directory. Zero w2 reports exist. The only name overlap (`RevProcEntry`) is a w1 report.
- `round-19/w1/*.md`: 67 files, all 67 names are registry members (0 non-member files). 23 registry seats have no report: ExecAuditFixture, ExecAuditShapes, ExecCarryFixture, ExecD2Pin, ExecD5Recheck, ExecGateCarry, ExecRevFixture, ExecRevHelper, ExecRunner13, ExecRunner14Demo, ExecRunner14Wrap, ReviewerRevPinHelper, ScoutFixturePattern, ScoutGateReplayExpect, ScoutGateSelftest, ScoutR18AuditCounts, ScoutSkillRegistry, ScribeAuditCriterion, ScribeCarryCriterion, ScribeD3, ScribeLogSkeleton, ScribeReportSkeleton, ScribeScorecard.
- Parity check on the 12 dispatch-backed waves: registry member set equals dispatch task set in 12 of 12.
- No dispatch-schema JSON exists under `round-19/`.

Why the tool cannot see it:
- `_dispatch_files` (`tools/mori-wave-settlement.py:125-126`) collects every regular `.json`.
- `scan_lane` (`:346-348`) drops every document whose `schema` is not `ufo-swarm-wave-dispatch-v1`, counting it in `ignored_json`. The 43 ignored files are 27 with no schema, 15 registries and 1 `ufo-swarm-wave-v1`. The round-19 registry is one of the 15.
- Result: round 19 contributes 0 members and 0 states to the lane totals and exit code.

Contract context: discovery is defined by dispatch schema only (`contract.md:64-67`). The motivating failure is the same class: "Nothing in the lane counts which dispatched seats left their report" (`contract.md:51-54`). The contract's live demonstration names the mori lane, not souji (`contract.md:95-97`), so souji round 19 is not a finite requirement. It is still the failure the tool was built to prevent.

Impact: if round 19 w1 were counted it would be **partial, 67 of 90** present. The `rc` line (`scan_lane` `:379`) can only see discovered waves. [INFERENCE: a lane whose discovered waves were all settled would exit 0 while 23 round-19 seats are unreported. Not observed on souji, because other discovered waves are not settled.]

Round 19 w2 (65 spec items, no registry, no directory) has no dispatch evidence at all. Excluding it matches the lane's convention that a spec is a plan, not evidence (`round-15/w2-skipped.json`: "Planned w2-spec.json remains a plan, not evidence of a dispatched wave"). Its dispatch state is unobserved.

Timestamps for the round-19 evidence: `round-19/w1-spec.json` 01:05:41, `round-19/w2-spec.json` 01:04:28, `round-19/w1b-spec.json` 02:40:44, `round-19/w1` directory 03:32:54 (newest report 03:34). Round-20 w1 spawn order for comparison: `round-20/w1-spec.json` 05:18:03, `round-20/w1-dispatch.json` 05:18:24, `round-20/w1-started.json` 05:25:32.

## 4. Checks with no difference

- **Determinism:** `scan.json` and `scan2.json` (08:09:08) are byte-identical (sha256 `51cd43f9…`). The contract requires this (`contract.md:85-86`).
- **Collisions:** 3 same-stem cross-round files exist. In each case the other file belongs to its own wave, so the tool's path-exact `missing` is correct.
  - `round-17/w2` `RerunGateReplays` and `RevQualityRows` → `round-18/w2/` files (18:24). Their header says `STATUS: PARTIAL … Attacked claim: C2 calibration — historical round-17 …`, which is a round-18 report.
  - `round-20/w1` `ScoutS038` → `round-19/w1/ScoutS038.md` (03:17:40). That predates `round-20/w1-dispatch.json` (05:18:24), so it cannot be a round-20 output.
- **Misroot:** no fleet `.ufo/waves` file (1,953 files indexed) has a stem matching any of the 120 missing seats. Only `AuditCase07` is misrooted, and it has since moved (D3).
- **Trailer shape:** 783 of 783 trailers are the last non-empty line of their task. None has CR characters, leading whitespace, or characters that differ between `splitlines()` and `split("\n")`.
- **Sizes:** the 662 present files range 1,457–170,776 B. There are 0 whitespace-only, 0 zero-byte, and 0 stub files.
- **Symlinks:** 0 in lane `.ufo/waves`. Walk errors: 0.
- **Name hints:** 0 (no basename matches `preview|undispatched|not-dispatched|validation`).
- **Duplicates:** 0 cross-wave duplicate report paths. 12 unique dispatch hashes.
- **Selftest:** `--selftest` → `MORI_WAVE_SETTLEMENT_SELFTEST: PASS (23 cases, 23 passed, 0 failed)`, exit 0. The frozen `frozen/c2-expected.json` holds 14 cases, as the contract says.

## 5. Tool observations (latent; no effect on souji)

Line numbers refer to the 08:15:31 version (710 lines). Each item is a case the code handles differently from the contract or from the GT method. All were **zero-count** on this lane.
- **L1. Trailer selection** (`_trailer`, `:214-228`): takes the last *matching* line anywhere in the task. The contract says "the LAST line of a task" (`contract.md:70`). Souji has 0 cases where the trailer is not the last non-empty line.
- **L2. Whitespace-only file** (`_member_status`, `:236-241`): only `size == 0` is `empty`. A whitespace-only file counts as `present`. GT treats it as `empty`. Souji has 0 such files.
- **L3. Symlinked `.json` silently skipped** (`_dispatch_files`, `:125`): not counted in `ignored_json` or `unreadable_json`. The contract says symlinks are "not followed" and other JSON is "counted as ignored_json" (`contract.md:64-67`). Souji has 0 symlinks.
- **L4. Non-regular entries and `unavailable` fold into `missing`** (`_member_status`, `:246`): a directory or FIFO at a report path, or an lstat error other than ENOENT/ENOTDIR, is reported as `missing`. Souji has 0 such entries. Every lstat result agrees with the independent probe.
- **L5. Intermediate symlink is `unsafe`** (`_inspect_report_path`, `:203-204`). This is new in the 08:11+ versions. Not triggered here.
- **L6. `--out` parent not created** (`main`, `:703-704`): prints `mori-wave-settlement: cannot write --out` and returns 2. My first run hit this (I created the scratch dir and re-ran). This is operator error on my side, not a contract violation.

## 6. Timeline (local time, from mtime or ctime)

| Time | Event |
|---|---|
| 07:30:18 | `trailers.tsv` written |
| 07:34:32.426 | `GtLaneSouji.md` written (GT snapshot) |
| 07:38:16.163 | lane `OracleAuditCases.md` modified (3,878 B) |
| 07:45:51.879 | tool last modified before this run (version V0) |
| 07:46:53.061 | `evidence/c2-live-fleet.json` written |
| 07:54:52.432 | lane `OracleCallerCases.md` modified (7,692 B) |
| 08:01:46.388 | `scan.json` (V0): misrooted 1, exit 1 |
| 08:06:29.010 | `compare-out.txt`: 0 mismatches; `AuditCase07` still in fleet (8,784 B) |
| 08:09:08.526 | `scan2.json` (V0): sha equals `scan.json` |
| 08:09:21.087 | lane `round-20/final/AuditCase07.md` created (8,784 B); lane `final/` mtime same instant |
| 08:09:21.091 | fleet `.ufo/waves/round-20/final/` entry removed; directory now empty |
| 08:10:19.861 | `scan3.json` (V0): round-20/final settled 64/64, misrooted 0, present 663 |
| 08:11:12.537 | tool modified by another writer (28,880 B, 690 lines) |
| ~08:12 | `scan4.json` (V1): sha equals `scan3` |
| 08:13:06.041 | tool modified (29,851 B, sha `5027bdc7…`) |
| 08:15:18.061 | tool modified (29,833 B, sha `aae79d15…`) |
| 08:15:31.695 | tool modified (30,142 B, 710 lines, sha `c134c57b…`) |
| 08:15:42.747 | fleet `round-20/residual/ResidualFrozen.md` created. Not a souji member: no match in the 783-trailer GT. |
| 08:16 | `scan6.json` on V3 (`c134c57b…`): sha equals `scan4` |

## 7. Commands and exit codes

1. `python3 tools/mori-wave-settlement.py scan --lane-root …/souji-shokunin --fleet-root …/shokunin --out …/falsify/LiveSouji/scan.json` → stderr `mori-wave-settlement: cannot write --out`, EXIT 2 (scratch parent missing; no output written).
2. `mkdir -p …/falsify/LiveSouji`, then the same scan → EXIT 1; `scan.json` 57,571 B at 08:01:46.
3. `scan2.json` at 08:09:08 → EXIT 1; sha256 `51cd43f9…` (equal to `scan.json`).
4. `scan3.json` at 08:10:19 → EXIT 1; sha256 `a842e7fa…`.
5. `scan4.json`, `scan5.json`, `scan6.json` (after the 08:11, 08:13, 08:15 edits) → EXIT 1 each; sha256 `a842e7fa…` each.
6. `--selftest` (run twice, after edits) → PASS 23/23, EXIT 0.
7. `compare.py` (scratch, read-only probe): pre-change run `compare-out.txt` → no mismatches. Post-change run (`scan4`) → `gt_vs_tool` 1 (AuditCase07), `live_vs_tool` 0.
8. `/usr/bin/jq` (jq 1.8.2) for JSON counts and per-wave diffs (the bash `jq` is jaq 3.1.1; not used for counts).

Scratch artifacts (all under `falsify/LiveSouji/`): `scan.json`, `scan2.json`, `scan3.json`, `scan4.json`, `scan5.json`, `scan6.json`, `compare.py`, `compare-out.txt`, `compare-out-post-relocation.txt`.

## 8. Unobserved, residual risk, verification gaps

- Why round 19 has no dispatch JSON: not observed. [INFERENCE: written by a different mechanism, or the wave predates the dispatch format.] The dispatch format exists for rounds 13–20, so its absence is anomalous.
- Whether round-19 w1's 23 missing seats are still running: no timestamps observed. Round-19 w2 dispatch state: no evidence either way.
- Who moved `AuditCase07.md` and why: not observable.
- Report content is not judged (contract scope). A `STATUS: PARTIAL` report counts as present.
- Misroots outside fleet `.ufo/waves` and outside the contract's fleet-root rule were not searched (bounds).
- Other lanes were not examined. GT claims F5 (90 non-trailer `Report` lines) and F6 (unreferenced files) were re-checked only for md counts: `round-17/w2` 1, `round-18/w1` 5, `round-19/w1` 67.
- The 08:15:31 tool version is reviewed only on the scan path cited above. The rest of the file (fixtures, selftest) changed too and was not reviewed.

## 9. Recommendations (not applied; for the integration owner)

1. Decide the coverage rule explicitly. Either require a dispatch JSON for every spawned wave, or make discovery read `ufo-swarm-registry-v1` and report a `registry-only` state. Add a selftest fixture: registry with 90 spawn seats and 67 reports, expected `partial 67/90`.
2. Stop folding registry and spec files into one `ignored_json` count. List them by wave.
3. Re-run `evidence/c2-live-fleet.json` for souji. Its `misrooted 1` is stale.
4. Pin the tool version in every evidence file. The current sha is `c134c57b…`.

## 10. Bounds and installs

- Read-only on lane and fleet. The only fleet read was `final/AuditCase07.md`, to read its header before it moved.
- Writes only under `falsify/LiveSouji/` (scratch and this report). I created `falsify/LiveSouji/`.
- Never wrote to `tools/`, `corpus/`, or any lane production file. The tool file changed four times during the run by another writer. Not mine.
- No subagents. No git or jj. `tools/mori-census.sh` not run. `.ufo/interactive-sessions/`, `.ufo/worktrees/`, `.jj/` and `~/.omp` not opened.
- While locating changes I listed names and mtimes under mori `.ufo/waves/round-20/` and fleet `.ufo/waves/round-20/`. No contents were read.
- Installs or updates: **none** (no pacman, uv, npm, or cargo use).
