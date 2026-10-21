VERDICT: HOLDS. C2 per-dispatch-file settlement for mado-shokunin matches the wave-1 ground truth (GtLaneMado), an independent live oracle, and the committed fleet scan's lane totals with zero differences: 16/16 dispatch files and 1030/1030 members agree on every field. Two scope observations are recorded in section 4: R1, a seat's report sits inside the lane at an undeclared path, which the frozen `misrooted` definition cannot classify; R6, one of the 41 round-21 missing reports is not accounted for in the lane's closure outcome files. Neither changes a per-file figure, and the GT shares R1.

Seat: MoriR20.LiveMado. Leaf, no subagents. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin` read-only. Scratch `.ufo/waves/round-20/falsify/LiveMado/`.

## 1. Per-dispatch-file comparison

Tool (`scan.json`), GT (`build/GtLaneMado/ground-truth.json`) and the live oracle (`compare.py`, own `os.stat`/`islink` logic) agree on every row. Names, agents, declared paths and dispatch SHA-256 also agree for all 16 files.

| # | dispatch file | members | present | missing | misrooted | stub | empty | state |
|---|---|---|---|---|---|---|---|---|
| 1 | fleet-round-1-interactive/dispatch-preview.json | 32 | 0 | 32 | 0 | 0 | 0 | unsettled |
| 2 | round-13/w1/dispatch.json | 32 | 31 | 1 | 0 | 0 | 0 | partial |
| 3 | round-14/w1 | 32 | 32 | 0 | 0 | 0 | 0 | settled |
| 4 | round-15/w1 | 64 | 64 | 0 | 0 | 0 | 0 | settled |
| 5 | round-16/w1 | 64 | 64 | 0 | 0 | 0 | 0 | settled |
| 6 | round-16/w2 | 32 | 32 | 0 | 0 | 0 | 0 | settled |
| 7 | round-17/w1 | 70 | 69 | 1 | 0 | 0 | 0 | partial |
| 8 | round-17/w2 | 78 | 78 | 0 | 0 | 0 | 0 | settled |
| 9 | round-18/w1 | 88 | 88 | 0 | 0 | 0 | 0 | settled |
| 10 | round-18/w2 | 73 | 59 | 14 | 0 | 0 | 0 | partial |
| 11 | round-19/w1 | 86 | 61 | 25 | 0 | 0 | 0 | partial |
| 12 | round-19/w2 | 67 | 67 | 0 | 0 | 0 | 0 | settled |
| 13 | round-20/w1 | 85 | 85 | 0 | 0 | 0 | 0 | settled |
| 14 | round-20/w2 | 78 | 76 | 2 | 0 | 0 | 0 | partial |
| 15 | round-21/w1-run.json | 65 | 50 | 15 | 0 | 0 | 0 | partial |
| 16 | round-21/w2-run.json | 84 | 58 | 26 | 0 | 0 | 0 | partial |

Totals: members 1030, present 914, missing 116, misrooted 0, stub 0, empty 0, unparsed 0, unsafe 0; states settled 8, partial 7, unsettled 1; exit 1 (expected 1).

Committed fleet scan (`evidence/c2-live-fleet.json`, mtime 07:46:53), mado entry: members 1030, present 914, missing 116, misrooted 0, empty 0, unparsed 0, unsafe 0, unreadable_json 2, waves 16, exit 1. Identical to the scan totals. That file holds per-lane totals only (top-level keys `dispatch_filename_flags`, `fleet_root`, `lanes`, `schema`; lane entries have no per-file rows and no stub or state fields). Per-file comparison against it is therefore not possible [observed].

## 2. Differences

None. Every per-file, per-member and per-total value matches across the four sources.
- `compare.py` prints `MEMBER DIFFS 0` over 1030 member rows (name, agent, declared path, status). Output: `falsify/LiveMado/members-live.tsv`, `compare.json`.
- Trailer rule: the tool's last-line rule (`tools/mori-wave-settlement.py:211-214`, `splitlines`) and GT's split-on-newline rule agree on all 1030 tasks. No task contains CR or Unicode line separators. Every task's last line is the trailer; none has two trailers; no member name repeats within a file; no report path is shared (`checks.py` D_*, rp_unique 1030, max multiplicity 1).
- Discovery: 428 regular `.json` under `.ufo/waves` = 16 dispatch-v1 + 410 ignored + 2 unreadable. This matches the tool (`ignored_json` 410, `unreadable_json` 2) and GT. The two unreadable files are the same two GT names. No dispatch-like JSON is missed: the only JSON carrying `taskCall` or a dispatch-like schema is one of the 16 (`checks.py` A_dispatch_like_not_exact = []).

Because nothing differs, no difference needs a live-change or tool-error attribution. The changes that did occur in the window are listed in section 3.

## 3. Live-change and tool-change evidence (mtimes)

- Lane `.ufo/waves`: 0 files and 0 directories have mtime after 2026-10-21 07:30:00 (`find -newermt`). The newest file under `.ufo/waves` is `round-21/final-summary.json` at 07:15:21 (with `round-21/outcomes.json` and `round-21/residual/dispositions.json`). Newest dispatch: `round-21/w2-run.json` 05:51:30. Newest seat report: `round-21/w2/reports/AtkCrossCell.md` 06:21:55 (dir mtime `round-21/w2/reports` 06:21:55.823). The lane therefore has not changed since before the GT snapshot (`members.tsv` 07:31:51, `ground-truth.json` 07:34:56, `GtLaneMado.md` 07:36:44). The fleet scan (07:46:53) and my scans (08:00:35 onward) saw the same lane state.
- Report paths of all 1030 members lie under `.ufo/waves/`, so the `.ufo/waves` mtime check covers every scan input.
- `tools/mori-wave-settlement.py` changed during the window. It was 07:45:51, 28261 B when I listed it near 08:00, and is now 08:04:26, 28797 B. The delta is exactly 536 B, equal to lines 48-50 (new refinement case `r7-dotdot-inside-lane` and its comment) plus lines 528-531 (its `_fixture` branch). Every `def` line shifts by +3 before the fixture branch and by +7 after it (`_safe_report_path` 152→155, `_summarize_wave` 243→246, `scan_lane` 304→307, `main` 653→660). This is consistent with a test-only insertion [INFERENCE: no pre-change copy exists to diff against; the conclusion rests on byte accounting and line offsets]. The production regions `:155-237` and `:246-304` are unchanged under that accounting.
- Effect on C2 output for mado: none. `scan.json` (08:00:35, pre-change) and the re-runs after the change are byte-identical (`cmp`, section 5).
- `frozen/c2-expected.json`: mtime 07:23:14, before the tool was written. Its 14 cases are unchanged during the wave.

## 4. Residual findings (scope gaps, not per-file differences)

R1 In-lane misroute, not classifiable under the frozen contract. Round-13 w1, member `ProtocolRecon` (scout). The task's last-line trailer declares `.ufo/waves/round-13/w1/reports/ProtocolRecon.md`. The file that exists is `.ufo/waves/round-13/w1/ProtocolRecon.md`: 11,415 B, mtime 2026-10-20 01:10:31 (dispatch 01:06:36), header `**Seat:** MadoR13.ProtocolRecon`. Nothing exists at the declared path or at the fleet-root path (`os.path.exists` false).
- Tool: `missing`. `_member_status` (`tools/mori-wave-settlement.py:224-237`) reclassifies only fleet-root same-path files as `misrooted` (`:233-236`). It has no in-lane branch.
- GT: `missing`. Its near-name search covered reportDirs only, so the wave-root file lies outside its stated scope. Its claim "no near-name file" is accurate within that scope.
- Effect: round-13/w1 reads 31/32 partial. Counting any report the seat produced anywhere in the lane would make it 32/32 settled. The frozen C2 text does not define this class. I flag it for L1 and do not change the verdict.

R2 Name reuse (5 of the 116 missing names have same-basename files in other waves). These are not misroutes [INFERENCE from mtime and seat labels]. Path-keyed attribution keeps them from being credited to the wrong seat.
- round-18/w2 `CriticAdmission` → exists in round-17/w2 (label MadoR17, 12:00:06), round-19/w2 (15:11:28) and round-20/a2/review (2026-10-21 04:17:56).
- round-18/w2 `CriticHonestyW2` → round-19/w2 (label MadoR19.CriticHonestyW2, 15:14:17).
- round-19/w1 `RevQualityOverlap` → round-18/w1 (label MadoR18.RevQualityOverlap, 12:49:33).
- round-21/w1 `SourcePartial` → round-21/w2/reports (06:01:14; header "round 21, w2"; w2's own SourcePartial is present).
- round-21/w2 `SourceImap` → round-21/w1/reports (05:11:09, before the w2 dispatch at 05:51:30; w1's own SourceImap is present).

R3 "Present" is shape-only, as the contract says. Of 914 present reports, 323 carry a `Seat:` label, and all 323 match member name and round (`attrib.py`). The other 591 have no label, so their authorship cannot be header-verified. No present report starts with the stub text. None is 64 B or smaller (smallest 211 B). No two present reports share content (914 distinct SHA-256). The stub rule (`tools/mori-wave-settlement.py:229-231`) catches whole-file stubs only. A seat that wrote the stub and then stopped would count as present; none is observed in mado.

R4 `dispatch-preview.json`: 32 missing, and its reportDir `fleet-round-1-interactive/reports` is absent. The tool's state is `unsettled` and `name_hint` flags it (`undispatched-name:preview`). No "Spawned N" record exists under `.ufo/waves` for this wave (scan of non-.md files). Whether it was ever dispatched is therefore unknown to the tool [INFERENCE]. It accounts for 32 of the 116 missing.

R5 Round-21 spawn history. `round-21/w2-dispatch.txt` (05:51:34) records "Failed to start background task jobs … Background job limit reached (100)". The closure's `refused_calls` records one `wave84_attempts` and `spawned_by_refusals: 0`. The retry `round-21/w2-dispatch-2.txt` (05:55:24) records "Spawned 84 background agents" with `-2` IDs, matching w2-run.json's 84. The six spawn records under `.ufo/waves` (round-19 w1 86, w2 67; round-20 w1 85, w2 78; round-21 w1 65, w2 84) each equal their dispatch-v1 count. Five further seat-listing texts (fleet `plan.json`, round-19 `task-result.json` ×2, round-21 `w1-plan.json`, round-21 `w2-dispatch-2.txt`) list exactly the dispatch-v1 report paths (0 extra, 0 missing). No seat is hidden from the dispatch-v1 set.

R6 Round-21 missing reports against the lane's own closure records. The last seat report write under `round-21/w2/reports` is `AtkCrossCell.md` at 06:21:55.82; no other seat report under any round-21 `reports/` directory is newer. Round-21 wrote 56 non-report files between 06:21:55 and 07:15:21 (`final-summary.json`, `outcomes.json`, `residual/*` ×10, `evidence/*` ×41, `w2/final-guards/*`, and two round-21 scripts). Those closure records classify the 41 missing members as follows (observed, by exact name sets):

| bucket | count | closure record |
|---|---|---|
| w2 missing, classified dead | 26 | `outcomes.json` `w2.dead` (26; names match the tool's w2 missing set exactly; error "Codex is at capacity … turn_rate_limit") |
| w1 missing, classified dead | 13 | `outcomes.json` `w1.known_dead` (11 × zai `429 Rate limit … type=1302`; 2 × Codex "at capacity") |
| w1 missing, uncredited | 1 | `outcomes.json` `w1.uncredited_original_without_terminal_receipt` (`OracleGitAddDry`); `final-summary.json` `inherited_uncredited_terminal_unknown` |
| w1 missing, not in any closure outcome | 1 | `OracleHasattr`: absent from `outcomes.json`, `final-summary.json` and `residual/dispositions.json`. `oracle/expected.json` and `w1/oracles/Hasattr.json` (author MadoR21, "L1 static recovery") say "OracleHasattr independently agreed but wrote no proposal due role-card write restriction" |

`final-summary.json` `provider_deaths: 40` = 13 + 26 + 1 (`FinalAssessmentReview`, an ordinary residual reviewer). So the tool's missing set is accurate, and the closure omits one of its 41 without a death or uncredited record. C2 correctly reports `OracleHasattr` as `missing` and does not label it dead. The reason is recorded only in the oracle files. [INFERENCE: closure omission is a gap in the closure, not in C2.]

## 5. Checks run (command → exit → result)

1. `python3 tools/mori-wave-settlement.py scan --lane-root /home/vgpnk/Projects/shokunin/mado-shokunin --fleet-root /home/vgpnk/Projects/shokunin --out …/falsify/LiveMado/scan.json` → rc 1. Totals as in section 1; `ignored_json` 410; `unreadable_json` 2; `name_hinted_waves` 1.
2. Same command → `scan2.json`, rc 1. `cmp scan.json scan2.json` identical; stdout identical to the `--out` file (`cmp` of `scan2.json` and `scan2.stdout`).
3. Same command after the tool change (08:04:26) → `scan3.json`, rc 1. `cmp scan.json scan3.json` identical.
4. `python3 tools/mori-wave-settlement.py --selftest` → `MORI_WAVE_SETTLEMENT_SELFTEST: PASS (22 cases, 22 passed, 0 failed)`, rc 0, run twice. The 22 are the 14 frozen cases plus 8 refinement cases, including the new r7.
5. `falsify/LiveMado/compare.py` → rc 0. `DISCOVERY` 16/16 waves, empty only-sides; `MEMBER DIFFS 0`; per-file rows identical. One field is wrong: `compare.json` key `live_discovery_json_count` = 9395. That is a bug in my scratch script (it sums `len(files)` per `.json` file). The correct count is 428 (`checks.json` `A_json_files`, same as GT).
6. `falsify/LiveMado/checks.py` → rc 0. A: 428 JSON, 16 dispatch, 11 symlinks (none named `*.json`), 2 unreadable; schema census sums to 426 = 428 − 2. B: 914 present, 0 ≤ 64 B, 0 stub-prefixed, 0 zero-size. C: 116 missing; reportDir absent for 32 (preview) and present for 84; exact-path hits at fleet root and 20 sibling lanes = 0; prefix-boundary hits = 0; basename hits = 6 (R1, R2). D: 1030 final-line trailers, 0 multi-trailer, 0 duplicate names.
7. `falsify/LiveMado/attrib.py` → rc 0 (R3). `falsify/LiveMado/hits.py` → rc 0 (R1/R2 detail).
8. Inline python, not saved as files, all rc 0: trailer-text scan of non-JSON files under `.ufo/waves` (8 files: 5 seat-listing texts and 3 reports quoting the trailer); set equality of the 5 seat-listing texts against dispatch-v1 (R5); "Spawned N" scan of non-.md files (6 spawn records, R4/R5); byte-content duplicate hashing of present reports (R3); round-21 outcome reconciliation against `outcomes.json` and `final-summary.json` (R6); round-21 `reports/` mtime window check (R6).
9. `grep` (named directory `round-21`) for `OracleHasattr`: hits (output truncated) in w1-assignments, w1-dispatch.txt, w1-plan.json, w1-record.txt, w1-run.json, w1-spec.json, `w1/oracles/Hasattr.json`, `w1/reports/swarm-registry.json`, `oracle/expected.json`. Separately `grep -c` gives 0 for `outcomes.json`, `final-summary.json` and `residual/dispositions.json`.
10. `/usr/bin/jq` (jq-1.8.2) used for JSON field reads. Bare `jq` in this shell is jaq 3.1.1, not used for counts.

## 6. Tooling and bounds

- Installed or updated: nothing. Tools used: python3 stdlib, `/usr/bin/jq` 1.8.2, `cmp`, `stat`, `find`, `sha256sum`.
- No lane production file, lane jj or git state, or Git index was touched. The only writes are under `falsify/LiveMado/` and this report.
- Reads were confined to the mado lane's `.ufo/waves` tree (directory walks, pattern searches, and reads of the closure and oracle records named above); exact report paths of the 116 missing members under the fleet root and 20 sibling lanes (existence checks only); the committed fleet evidence file; the tool and frozen oracle. Non-JSON files under `.ufo/waves` were read in full for pattern searches (dispatch-schema string, trailer text, `Spawned N`). Report bodies were otherwise read only for header bytes (first 120–600 B), and the R6 closure JSON files were read in full.
- Not opened: `.ufo/interactive-sessions/`, `.ufo/worktrees/`, `.jj/`, ~/.omp session logs.
- Not run: `mori-census.sh` (not requested).
- Not verified: report content correctness (C2 is shape-only by design); trailer paths outside `.ufo/waves`; whether round-21 seats are still running (no process probe) [INFERENCE in R6].
