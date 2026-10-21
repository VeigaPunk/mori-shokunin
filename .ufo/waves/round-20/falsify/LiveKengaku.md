HOLDS

# LiveKengaku: C2 falsification on lane kengaku-shokunin (round 20)

Verdict: HOLDS. The live scan matches the wave-1 ground truth (GtLaneKengaku.md) on every dispatch file, all 387 member rows, and the lane totals in the committed snapshot. There are zero differences to explain. The tool has four silent-green or misclassification modes that the frozen contract leaves open. None is triggered on kengaku (section 8).

Scope: lane /home/vgpnk/Projects/shokunin/kengaku-shokunin, fleet root /home/vgpnk/Projects/shokunin. Read-only on the lane. Writes only under falsify/LiveKengaku/ and /tmp/c2-falsify-LiveKengaku/. Installs or updates: none. Subagents, peer messages, git/jj: none.

## 1. Commands and exit codes
- Required scan: `python3 mori-shokunin/tools/mori-wave-settlement.py scan --lane-root /home/vgpnk/Projects/shokunin/kengaku-shokunin --fleet-root /home/vgpnk/Projects/shokunin --out .../falsify/LiveKengaku/scan.json` gave exit 1. The exit is expected because round-26 falsify is `partial` (tool:363). scan.json is 26,833 bytes.
- Rerun to scan-rerun.json gave exit 1, and `cmp` reports byte-identical output (contract.md:85-86).
- `--selftest`: `MORI_WAVE_SETTLEMENT_SELFTEST: PASS (21 cases, 21 passed, 0 failed)`, exit 0. Its writes go only to a TemporaryDirectory (tool:624).
- Independent re-derivation (Python, read-only): re-parsed the 5 dispatch JSON files, took the last trailer line matching the contract regex, lstat'd every report, and recomputed status, size, stub and misroot. Compared against scan.json and GtLaneKengaku/members.tsv.
- sha256 of the 5 dispatch files equals the scan `dispatch_sha256` for 5 of 5.

## 2. Per dispatch file
| dispatch file | wave | members | present | missing | misrooted | empty | stub | state (scan) | state (GT) |
|---|---|---|---|---|---|---|---|---|---|
| round-25/build-dispatch.json | kengaku-r25-build | 92 | 92 | 0 | 0 | 0 | 0 | settled | settled |
| round-25/falsify-dispatch.json | kengaku-r25-falsify | 87 | 87 | 0 | 0 | 0 | 0 | settled | settled |
| round-26/build-dispatch.json | kengaku-r26-build | 72 | 72 | 0 | 0 | 0 | 0 | settled | settled |
| round-26/build-registry-rebuild.json | kengaku-r26-build | 72 | 72 | 0 | 0 | 0 | 0 | settled | settled (duplicate of build-dispatch.json) |
| round-26/falsify-dispatch.json | kengaku-r26-falsify | 64 | 53 | 11 | 0 | 0 | 0 | partial | partial |

- The GT (GtLaneKengaku.md:23-27) has no stub column. GT §5.3 (line 50) says no present file is under 64 bytes. I checked this directly: `find .ufo/waves -type f -size -65c` returns nothing. None of the 304 distinct reports begins with a `STATUS:` line or contains `STATUS: started`.
- The committed snapshot cannot support a per-file comparison. Its kengaku entry (c2-live-fleet.json:311-323) holds lane totals only: empty, exit, lane, members, misrooted, missing, present, unparsed, unreadable_json, unsafe, waves.

## 3. Lane totals
| metric | scan | snapshot :311-323 | GT §3 (GtLaneKengaku.md:33-35) |
|---|---|---|---|
| members | 387 | 387 | 387 |
| present | 376 | 376 | 376 |
| missing | 11 | 11 | 11 |
| misrooted | 0 | 0 | 0 |
| unparsed / unsafe / empty | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| unreadable_json | 0 | 0 | 0 |
| waves | 5 | 5 | 5 |
| states | settled 4, partial 1 | (not recorded) | settled 4, partial 1 |
| ignored_json | 12 | (not recorded) | 12 |
| exit | 1 | 1 | (not stated) |

## 4. Member level (387 rows)
- Keys only in GT: 0. Keys only in scan: 0.
- Status and agent: 0 differences against GT and against the independent re-derivation.
- Size: all 376 present members equal GT `size_bytes`. The smallest is 845 bytes (RevCensusManual), so no stub-sized file exists.
- The 11 missing members match GT §4 and falsify-dead-seats.json as a set. Each expected path is ENOENT under the lane root and under the fleet root (lstat), so misrooted 0 is correct.
- Orphans: round-26/falsify holds 53 .md files and all 53 are referenced by members. The .md count across the four present directories is 304 = 92+87+72+53.
- Trailers: every trailer is the final non-empty line of its task (0 exceptions). Every path is `.ufo/waves/<round>/<build|falsify>/<Name>.md` (0 exceptions). Nine round-25 build members (TallyR01-09) contain a second "Report:" substring mid-body; the anchored regex still selects the trailer.
- Name hints: none (`name_hinted_waves` 0).

## 5. Differences explained
- The only apparent differences are definitional. GT §3 gives "distinct" figures (4 waves: 3 settled, 1 partial; 315 report paths; 304 present). The scan gives raw totals (5 waves: 4 settled, 1 partial; 387 members; 376 present). The GT's own raw figures (lines 33-35) equal the scan's.
- The cause is round-26/build-registry-rebuild.json, which is byte-identical to build-dispatch.json (`cmp` identical; sha256 425b46136aca...). The tool flags it through `duplicate_of` (tool:335-339), but the totals are not deduplicated (tool:341-352). On disk there are 304 distinct present reports plus 11 missing, which gives 315 paths.
- No member or wave classification differs.

## 6. Live lane change since snapshot: none
- Times (local, -03): GT members.tsv 07:34:34; GT md 07:36:07; c2-live-fleet.json 07:46:53; scan 08:00.
- `find .ufo/waves -newermt '2026-10-21 07:34:34'` returned no entries. The Python walk found 329 files under .ufo/waves, none newer than 07:34:34, and no subdirectory newer either.
- Directory mtimes under .ufo/waves are all at or before 05:48:14 (round-26/recovery). So no entry was created, removed or renamed in any of them after 05:48:14. This rules out a move that preserves mtimes.
- Dispatch mtimes: round-25/build-dispatch.json 2026-10-20 21:15:42; round-25/falsify-dispatch.json 21:47:13; round-26/build-dispatch.json 02:40:45; round-26/build-registry-rebuild.json 04:54:59; round-26/falsify-dispatch.json 04:40:21.
- Every present report is newer than its own wave's dispatch file. Ranges: round-25 build 21:16:39-21:57:54; round-25 falsify 21:47:51-22:15:37; round-26 build 03:51:38-05:25:47 (vs 02:40:45); round-26 falsify 04:46:33-05:24:33 (vs 04:40:21). Against the registry-rebuild copy time (04:54:59), 69 reports look older, but that is an artifact of the copy's own mtime. Against the original dispatch, 0 are older.
- For the 11 missing: the round-26/falsify directory mtime is 05:21:15. No entry was created or removed in that directory after 05:21:15, so none of the 11 was written and then deleted after that time. Write-then-delete earlier than that is [INFERENCE], unobservable.

## 7. Why the 11 are missing (seat failure, not a C2 defect)
- round-26/falsify-dead-seats.json:4-51: 11 names, set-equal to the missing set. Status "failed (exit 1)"; shared_error turn_rate_limit_exceeded after 5 retries; handling "never a seat report".
- round-26/falsify-dispatch-log.txt:1-2: "first dispatch all64 started, no refusals". Its 64 job names are set-equal to the 64 falsify members.
- round-26/build-dispatch-log.txt:1-5: 72 seats. Job-cap refusals at 03:41:27, 03:44:27 and 03:47:27 (refused=72 each). The spawn at 03:50:27 had refused=0, and the first build report is at 03:51:38. The 72 job names are set-equal to the 72 build members after stripping the `-4` attempt suffix.
- Log line 7: an 80-seat plan was trimmed to 72 before dispatch, and the 8 deferred items moved to the falsify wave or L1 drafting. They never entered a dispatch file, so C2 cannot count them. That is the contract's scope (contract.md:51-52: "which dispatched seats left their report"), not a tool error.

## 8. Tool-level risks (none triggered on kengaku)
Tool = mori-shokunin/tools/mori-wave-settlement.py. Fixtures are in /tmp/c2-falsify-LiveKengaku/ (laneA, laneB, laneC, laneD, storeA).

- R1, silent green on zero discovery. If `.ufo` or `.ufo/waves` is a symlink, `_wave_root` returns None (tool:87-88), so nothing is discovered (tool:315) and the exit is 0 (tool:363). Fixture laneA: exit 0, waves 0. Control laneC (real directory): exit 1, unsettled. contract.md:64-67 says symlinks are not followed and has no zero-discovery rule, so the tool follows the text.
- R2, silent green on corrupt dispatch. The exit ignores unreadable_json (tool:363; counted at tool:325-329). Fixture laneB: exit 0 with unreadable_json 1.
- R3, silent drop. A dispatch JSON whose lstat fails is skipped without any counter (tool:108-111). contract.md:65-66 says unparseable JSON is counted. Fixture: `.ufo/waves/round-1` with mode 644 holding build-dispatch.json gives exit 0 with waves 0, unreadable 0 and ignored 0.
- R4, misclassification. A report that exists but cannot be stat'd is counted missing. `_inspect_report_path` returns "unavailable" (tool:191-192), and `_member_status` maps that to "missing" (tool:234). Fixture: a 900-byte report behind a mode-600 directory gives status missing and exit 1. The control gives present and exit 0.
- R5, fail-closed but misattributed. Any unreadable non-JSON entry under .ufo/waves raises ScanError (tool:112). main prints "lane root is unreadable" and exits 2 (tool:665-667). Observed with a mode-600 directory inside .ufo/waves while the lane root was readable.
- R6, symlinked report is counted missing (tool:197-200, then tool:234). This matches the contract's non-symlink rule, but the label means absence.
- R7, headline totals count the byte-identical duplicate's 72 members again (tool:341-352). Present reads 376 where distinct is 304. The frozen oracle expects raw counts, so this is by design. Coverage readers should use distinct counts.
- R8, doc/code mismatch. The docstring (tool:9-10) says "at most 64 bytes are read"; the gate is 16 bytes (tool:226). There is no classification effect.
- R9, refinements beyond the frozen text: the `stub` status (R2) and last-matching-line trailers (R1, tool:208-211) versus contract.md:70-75. Both are disclosed. Both are inert on kengaku: 0 trailers differ from the final line, and 0 files are stub-sized.

Contract question for the integration owner: R1 and R2 are literal readings of contract.md:64-67 and 87-88. They produce exit 0 when nothing was discovered or a dispatch file is corrupt. Whether that should be exit 2 is a contract decision, not a kengaku finding.

## 9. Not verified
- The fleet-wide basename search in GT §4 was not repeated; the bounds forbid whole-fleet search. The misroot check is path-exact and returned ENOENT for all 11.
- Write-then-delete of any of the 11 before 05:21:15: unobservable [INFERENCE].
- Lane tests and builds were not run (out of scope; the main agent verifies). tools/mori-census.sh was not run (not in this item).
