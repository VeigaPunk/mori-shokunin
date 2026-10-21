VERDICT: HOLDS for lane kumitate. 0 per-file differences across wave-1 GT, fresh scan, independent recount, and the committed snapshot (lane totals). Tool-level residuals T1-T3 reproduce in fixtures but are not triggered on kumitate.

# LiveKumitate: C2 accuracy on lane kumitate (round-20 falsify)

Seat MoriR20.LiveKumitate (leaf). Lane read-only. Abbreviations: M=/home/vgpnk/Projects/shokunin/mori-shokunin, K=/home/vgpnk/Projects/shokunin/kumitate-shokunin, F=$M/.ufo/waves/round-20/falsify/LiveKumitate (scratch).

## 1. Per dispatch file (fresh scan 08:00 local; GT = GtLaneKumitate.md:27-33)

| dispatch (kumitate .ufo/waves/) | members | present | missing | misrooted | stub | empty | state | GT = scan = indep |
|---|---|---|---|---|---|---|---|---|
| round-35/build-dispatch.json | 95 | 95 | 0 | 0 | 0 | 0 | settled | yes |
| round-35/falsify-dispatch.json | 75 | 75 | 0 | 0 | 0 | 0 | settled | yes |
| round-36/build-dispatch.json | 96 | 96 | 0 | 0 | 0 | 0 | settled | yes |
| round-37/falsify-dispatch.json | 68 | 68 | 0 | 0 | 0 | 0 | settled | yes |
| round-38/build-dispatch.json | 90 | 89 | 1 (ConnSibling) | 0 | 0 | 0 | partial | yes |
| round-38/falsify-dispatch.json | 88 | 45 | 43 | 0 | 0 | 0 | partial | yes |
| total | 512 | 468 | 44 | 0 | 0 | 0 | 4 settled, 2 partial; exit 1 | yes |

Also 0 unsafe, 0 unparsed, 0 unreadable JSON, 0 duplicate report paths, 6 distinct dispatch SHA-256 (equal to GT:58-63), ignored_json 27. Sorted missing-name lists equal GT:43-44.

Committed c2-live-fleet.json:350-362 (lanes[12]) holds lane totals only: members 512, present 468, missing 44, misrooted 0, empty 0, unparsed 0, unsafe 0, unreadable_json 0, waves 6, exit 1. All equal the scan. It has no per-dispatch rows (dispatch_filename_flags has no kumitate entry), so per-file comparison against it is impossible. That is a snapshot granularity limit, not a difference.

## 2. Differences

None per file, so none to explain. Why nothing moved (local -03:00):
- Dispatch mtimes: r35/build 2026-10-20 21:15:31; r35/falsify 22:54:02; r36/build 2026-10-21 01:10:35; r37/falsify 03:20:41; r38/build 04:10:24; r38/falsify 04:36:34.
- Last write under K/.ufo/waves: 05:06:46 (round-38/final/measured-tree-clean.txt). find <waves> -type f -newermt '2026-10-21 07:33:56' | wc -l gives 0; same for 07:46:53. Snapshots: GT 07:33:56, c2-live-fleet.json 07:46:53.
- The 44 missing paths still lstat as absent. Only variant-name hit: round-38/evidence/L1-Check40.txt:1 ("NOT a replacement seat"), correctly not a trailer path.

## 3. Commands and outputs

- python3 $M/tools/mori-wave-settlement.py scan --lane-root $K --fleet-root /home/vgpnk/Projects/shokunin --out $F/scan.json; echo exit=$? gives exit=1. Totals as in section 1.
- python3 $F/indep.py $F/indep.json > $F/indep.txt gives exit 0 and diffs: []. Own stdlib classifier, no import of the tool. Compares per-member name/status, sha256 and state against GT values and scan.json.
- python3 $F/extra_checks.py gives exit 0. Registry names equal task names in 6/6 waves. Lane accounting names (43) equal the tool missing set. Path-shape mismatches 0. Present files older than dispatch 0. Duplicate-content groups 0. Plan files contain every dispatched name (68/90/88 tasks).
- python3 $F/fixtures.py > $F/fixtures.json gives exit 0 (T1-T3 below).
- Misrooted: /home/vgpnk/Projects/shokunin/.ufo/waves/round-38 is absent (lstat). GT's bounded basename search (GT:47-49) was not repeated; a fleet-wide search is outside this seat's bounds.

## 4. Tool-level residuals (reproduced; not triggered on kumitate)

- T1, silent pass when no dispatch tree is discovered. Fixture A0 (no .ufo/waves) and A1 (.ufo/waves symlink to a dir holding an unsettled wave) both give rc 0 and waves []. Cause: tools/mori-wave-settlement.py:87-88 (_wave_root returns None on symlink or absent), :315 (paths=[]), :363 (all() over empty gives rc 0). Contract C2 L64-67 says symlinks are not followed and L87 allows exit 0 for zero waves, so this is a contract gap as well as code. Kumitate .ufo/waves is a real directory (lstat).
- T2, symlinked parent escaping the lane reported missing, contract says unsafe. Fixture B: rc 1, member missing, outside file exists. Contract L71-73 requires unsafe, never read. Cause: _safe_report_path is lexical only (:152-170); _inspect_report_path returns "other" for a non-directory intermediate (:194-196); _member_status falls through to "missing" (:234). No outside bytes are read (_read_regular_bytes is called only for regular lane files, :227). Kumitate has no symlinks (os.walk links=[]; find -type l empty).
- T3, unreadable report reported missing. Fixture C (report outside waves, parent mode 600, file exists): rc 1, missing. Cause: EACCES maps to "unavailable" (:191-192), then to "missing" (:234). [INFERENCE] Inside .ufo/waves the same EACCES aborts with exit 2 (:96-100, :108-112); not fixture-tested. Kumitate has no permission errors (all 512 regular or absent).
- Positive control F (absent in lane, present at fleet root at same path) gives misrooted (:230-233). Detection works while the stray exists.

## 5. Semantic caveat touching kumitate (not a tool error)

- S1, two hand-recovered misroots count as present. Both reached the fleet root through bare lane-relative trailers. The lane then copied them into the lane by hand and deleted the fleet copies (lane's own record). r38 falsify Check27: round-38/evidence/falsify-seat-accounting.txt:7; scan present, 2275 B, mtime 04:46:00. r37 falsify AuditRemainder6: round-38/evidence/misroot-AuditRemainder6.txt:2-7 and round-38/evidence/misroot-final.txt:19; scan present, 8455 B, mtime 03:35:43. Contract L76-77 flags misroot only while the stray remains, so both counts are accurate as filesystem state. "Settled 68/68" (r37 falsify) and "45 present" (r38 falsify) include them. Byte equality and recovery are lane-recorded; session logs were not opened.

## 6. Lane-recorded context (cross-reference only)

- Build r38: 90 dispatched, 89 reports. ConnSibling failed on a provider interruption (round-38/evidence/build-seat-accounting.txt:1-2). The lane notes 90 exceeds its 88 cap (:5). Contract L68 counts dispatched tasks, so 90 is the contract count.
- Falsify r38: 43 misses = Codex capacity (9) + Zai 429 (34) (falsify-seat-accounting.txt:2-6). The lane's word "dead" is not used by the tool, consistent with contract L80-81.

## 7. Bounds, installs, not run

- No subagents; no git or jj; no writes to the lane. Not opened: .ufo/interactive-sessions/, .ufo/worktrees/, .jj/, ~/.omp session logs, falsify-dead-seat-results.json (contains session-log paths).
- Installed or updated: none (python3 3.14.8 and /usr/bin/jq pre-existing).
- Not run: frozen 14-case oracle and --selftest (not kumitate-specific); mori-census.sh (not requested).
- Scratch: F/scan.json, F/indep.json, F/indep.txt, F/fixtures.json, F/*.py, /tmp/liveK-fixtures/.
