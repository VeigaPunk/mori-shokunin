# Round 26 wave 2: OperabilityNoHarm (seat MoriR26.OperabilityNoHarm)

Pinned tip: `16935e24c93fa7e7567413d7ec091339a5df1474` (subject: "round-26: S124 teaches corrected (wave-1 SrcResourceControlV262); late wave-1 reports; wave-2 spec and run").
Read-only. No lane writes. No tool installed or upgraded.

## Verdict

No harm to operability at the pin. All five assigned commands exit 0, and each tally equals its last recorded result. For each check, the tool and fixture bytes at the pin are the bytes behind the last recorded run (table, column 6). Three low-severity documentation defects were found (F1 to F3). None changes a tool result.

## Method

1. Lane run of the five assigned commands from the lane root, as instructed (`-I -B` on the Python tools).
2. Clean run: `git archive 16935e24… | tar -x` into `/fast/scratch/hyaku/mori-r26/OperabilityNoHarm/export` (no `.git`). The selftests were repeated there, so no result depends on the dirty working tree.
3. Blob and tree identity: `git rev-parse <rev>:<path>` compared with the hashes in the round-25 evidence files and with the round-24 and round-20 records.
4. Routed tool: `--repo <lane> --rev 16935e24…`. It reads git objects only.
5. Lane-write check: `git ls-files --others --exclude-standard -- tools` is empty. No file under `tools/` or `.ufo/waves/round-25/` changed in the last 35 minutes (`find -newermt`). `tools/__pycache__` (gitignored) dates from 2026-10-22 05:19 -03, before my runs. My runs wrote nothing into the lane.
6. Working tree versus pin: `git diff --name-only 16935e24` lists `SCORECARD.md`, `corpus/lessons/round-25.md` and five round-26 wave files (other seats' in-flight edits). `git diff --stat 16935e24 -- tools/` is empty, so every tool and fixture is the pinned bytes.
7. Tools: none installed or upgraded. Python 3.14.8, `bash` and `jq` used as installed.

## Results: the five assigned commands

| # | Command | Exit | Tally now | Last recorded result | Blob or tree at pin versus recorded | Verdict |
|---|---|---|---|---|---|---|
| 1 | `bash tools/mori-census.sh --selftest` | 0 | `MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)` | 134/134: `SCORECARD.md:11` and `:1526` (round-24 measured outcome). No census file in `.ufo/waves/round-25/evidence/`. | blob `c7d952d6` at `c725aa37`, `28b79d3d` and pin: unchanged since round 24 | holds |
| 1b | same, clean export | 0 | 134/134 | as above | as above | holds |
| 2 | `python3 -I -B tools/mori-pressure.py --selftest` | 0 | `PASS 12/12`; `MATCHER: rejected 48/48 corrupted expectations` | `round-25/evidence/pressure-selftest.txt` (rev `ec840f9d`, exit 0, same two lines); `SCORECARD.md:1518` | blob `5785c5b2` = evidence `tool_blob`; fixtures tree `c28ccfdf` = evidence `fixtures_tree` | holds |
| 3 | `python3 -I -B tools/mori-job-runway.py --selftest` | 0 | `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21` | `round-25/evidence/runway-selftest.txt` (rev `d3b7af2a`, exit 0, PASS 21/21); `SCORECARD.md:1556` | blob `239dd8eb` = evidence `tool_blob`; fixtures tree `eddd10fb` = evidence | holds |
| 4 | `python3 -I -B tools/mori-routed-r24.py --repo <lane> --rev 16935e24…` | 0 | JSON `"status":"held"`, `"items":4`, `"held":4`, `"mismatches":0`; D1, D2, D3, D5 held; hygiene D4 held; `rev_commit` equals the pin | `round-25/evidence/routed-r24-after-a5.txt` (rev `e06d4a02`, exit 0, items 4, held 4, mismatches 0) | blob `ddc7a43d` at `e06d4a02` and at pin: unchanged | holds |
| 5 | `python3 -I -B tools/mori-wave-settlement.py --help` | 0 | usage `[-h] {scan} ...` | no help-output record in round-25 evidence or SCORECARD; the recorded check is the selftest (row 6) | blob `cf2f5dcd`; last commit touching the path is `71abd41` (round 20) | holds; see F1 |

## Results: extra read-only runs (beyond the five assigned)

| # | Command | Exit | Tally now | Last recorded result | Verdict |
|---|---|---|---|---|---|
| 6 | `python3 -I -B tools/mori-wave-settlement.py --selftest` | 0 | `MORI_WAVE_SETTLEMENT_SELFTEST: PASS (23 cases, 23 passed, 0 failed)` | `.ufo/waves/round-20/evidence/c2-final-selftest.txt`: 23/23, rc=0; `SCORECARD.md:1280` and `:1306` say 23/23; `SCORECARD.md:1269` still says 22/22 | holds; see F2 |
| 7 | `python3 -I -B tools/mori-job-runway.py --selftest --cases tools/fixtures/mori-job-runway/supplementary-cases.json` | 0 | `PASS 24/24` | `round-25/evidence/runway-selftest-supplementary.txt`: exit 0, PASS 24/24 | holds |
| 8 | `python3 -I -B tools/mori-pressure.py --selftest --cases tools/fixtures/mori-pressure/supplementary-cases.json` | 0 | `PASS 16/16`; `MATCHER: rejected 64/64` | `SCORECARD.md:1525` says `PASS 7/7`; `corpus/lessons/round-24.md:100` says `PASS 7/7` and `MATCHER: rejected 28/28`; both for 7 cases at `4f05dd5a` | holds; stale record, see F3 |

Rows 6 to 8 agree in exit code and in every tally that a record covers. Row 8 is not a regression: the file has more cases now, and every case passes.

## Findings

**F1. Defect (low, documentation). `--help` of `tools/mori-wave-settlement.py` does not list `--selftest`.**
- Evidence: `main()` tests `if args_list == ["--selftest"]` at line 687 and returns `_selftest()` at 688, before argparse runs. The help text lists only `{scan}` and `-h`. The only mention is the usage error at line 693 (`select scan or --selftest`).
- Attacks: operability (discoverability of the selftest that `SCORECARD.md:1269` cites).
- Not a regression: `--selftest` runs and exits 0 (row 6). [I did not test `--selftest` combined with other arguments.]

**F2. Defect (low, documentation). `SCORECARD.md:1269` still reads "22/22" for the settlement selftest.**
- Evidence: `SCORECARD.md:1306` says the round-20 capability cell's 22/22 "is stale; actual final selftest was 23/23". `.ufo/waves/round-20/evidence/c2-final-selftest.txt` reads `PASS (23 cases, 23 passed, 0 failed)`, rc=0. Today's run is 23/23 (row 6).
- Attacks: the recorded tally (coverage cell, round 20).
- Not a regression: the tool blob has not changed since round 20, and the stale cell is corrected by a later line, not removed.

**F3. Defect (low, documentation). The supplementary pressure record is stale.**
- Evidence: `SCORECARD.md:1525` says `PASS 7/7`. `corpus/lessons/round-24.md:100` says `PASS 7/7` and `MATCHER: rejected 28/28`, both for 7 cases at `4f05dd5a`. The file gained cases S08 to S16 in commit `ec840f9` (round 25, subject "supplementary pressure cases S08-S16 from the survivor replay"). Today's run gives 16/16 and 64/64 (row 8). A `grep` of SCORECARD.md for `PASS 16/16`, `64/64` and `16 cases` found no line.
- Attacks: the recorded supplementary tally. The routed D3 check counts 7 at `4f05dd5a` (a historical pin; `routed-r24` D3 detail `supplementary_case_count: 7`) and stays held.
- Not a regression: the new cases all pass.

**F4. Holds. No regression in any command.**
- Each recorded run used the tool and fixture bytes that the pin still has (table, column 6).
- The routed gate stays held at the pin although round 26 edited the standing Axes-table operability row (R4a, which D5 reads). Its D5 scores still match the pinned round-24 numbers (`axes_rows` in the row 4 detail).
- Clean export and lane runs agree, so the dirty working tree did not change any result.

## Residual risk and verification gaps

- **Not run:** the lane retention scan that the round-26 contract names as its no-harm item (the tip must not exceed 4 unallowlisted; `.ufo/waves/round-26/evidence/retention-scan-base.txt`). It is outside my command list. A sibling seat, `MoriR26.RetentionTip`, is assigned to it (roster).
- **Not run:** `tools/mori-routed-check.py` (present at the pin, not in my list; the round-24 record cites it), `tools/mori-oom-killers.py` (the C2 tool, covered by other seats) and the live, non-selftest census run.
- **Limit of the selftests:** they test each tool on its own fixtures. They show the tool logic still works. They do not show the host's live operability. [INFERENCE: this check says nothing about live host behaviour.]
- **Not re-derived:** the D5 scores and the SCORECARD Last-change text. I relied on the routed tool's own checks.
- **Recorded-tally drift** (F2, F3) is documentation debt, not a tool regression. It should be routed to the scorecard owner.

## Reproduction

```
bash tools/mori-census.sh --selftest                                     # rc 0, 134/134
python3 -I -B tools/mori-pressure.py --selftest                          # rc 0, PASS 12/12, MATCHER 48/48
python3 -I -B tools/mori-job-runway.py --selftest                        # rc 0, PASS 21/21
python3 -I -B tools/mori-routed-r24.py --repo <lane> --rev 16935e24…     # rc 0, held 4 of 4, mismatches 0
python3 -I -B tools/mori-wave-settlement.py --help                       # rc 0
python3 -I -B tools/mori-wave-settlement.py --selftest                   # rc 0, PASS 23/23
```

Privacy: I copied no operator settings, session data or journal text. This report carries only tool outputs, counts, tallies, commit hashes and blob hashes.
