PARTIAL. Both `live-state` assignments survive: every cause pointer the two rows cite holds, and no class is contradicted by the cause. The rows as written are not accepted: one false sentence in the register's dissent field, an incomplete cause for STATE_LAG, an incomplete writer history and an undisclosed clock dependence for STALE, and missing baseline pointers for both. No class change is recommended.

Scope: rows `-FINDING:WATCHDOG_STALE` and `+FINDING:WATCHDOG_STATE_LAG` in `corpus/evidence/drift-classification-r20.json`. Tested against the frozen C1 rule (classify by cause) and the definitions in `corpus/knowledge/drift-repin-r20.md` section 2 (`live-state` = census code unchanged, host/fleet state differs; `census-regression` = unintended behaviour change). Commits: lane HEAD `8f8c58e`, entering tip `2061780`, r10 pin `5be8943`, r7 `d30b4e4`. Last live check: 2026-10-21 08:12:47 -03.

## 1. Verdicts

### -FINDING:WATCHDOG_STALE, class live-state: AGREE (cause holds); row needs corrections
Why: the probe that emits the token is byte-identical from the r10 pin to the entering tip (E1), so the probe did not change. Its input changed. Since 2026-10-19 23:10 hyaku drivers have appended launch, complete and lane-dead lines to `.ufo/watchdog.log` (the headless slot driver, then `hyaku-inline` from 2026-10-20 00:41), and the daemon has not ticked since 2026-10-15 01:58:27 -03. The token is absent at the entering run because the log was written at 07:18:05 -03. That is a live-state explanation.
Corrections:
- C-S1. Dissent field says "census code byte-identical since r10". False for the file (`git diff --stat` shows +2027/-116). True for the watchdog probe, its ledger readers and its helpers (E1).
- C-S2. Writer history is incomplete. Post-stop lines 403-408 (2026-10-19 23:10:53 to 23:24:27) came from the headless slot driver (`driver=hyaku slot=`), introduced in `c030d1f` and removed in `cadb3e3` (2026-10-20). `hyaku-inline` writes start at line 409 (2026-10-20 00:41:08). The row should name both writers and the complete and lane-dead appends (`scripts/hyaku/inline.sh:130`, `:136`). The append path is `log()` at `scripts/shokunin-watchdog.sh:66`, inherited via `scripts/hyaku/inline.sh:24`.
- C-S3. Clock dependence not stated. Absence holds while census clock <= last watchdog.log write + 900 s. The last write is 07:23:21.68 -03 (stat at 08:12:47: unchanged), so absence ends at 07:38:21 -03 unless another write arrives. [INFERENCE] A census run at 08:12 -03 would emit `WATCHDOG_STALE` (age 2966 s; rule and threshold unchanged). Not executed. The token toggles with wall-clock time as well as with writes.
- C-S4. No baseline pointer. Add `corpus/evidence/baseline-r10-20261015T2231Z.json:24` (`FINDING WATCHDOG_STALE severity=warn ... threshold_s=900`).

### +FINDING:WATCHDOG_STATE_LAG, class live-state: AGREE (cause holds); row needs corrections
Why: the lag comparison and emit lines (`tools/mori-census.sh:816-818`) are byte-identical to r7 (`d30b4e4` lines 419-421). The 13 findings are real mismatches between the census's inputs. The inputs diverged because a second writer appends launches that carry a different round counter. That is live state.
Corrections:
- C-L1. "only the stopped daemon writes .round" is true but is half the cause. All 13 lag lanes' last ledger launch line is `driver=hyaku-inline` (watchdog.log lines 519, 541, 553, 558, 561, 567, 574, 578, 580, 582, 583, 584, 585). The 8 equal lanes' last launch lines are daemon `pid=` lines. Recounted over the 402-line pin-time ledger, LAG is 0. The second writer (`scripts/hyaku/inline.sh:103`) must be cited.
- C-L2. The two sides are different round counters, so "lag" is not a stale state file. hyaku takes `round=` from `$STATE/next/<lane>` (`inline.sh:89`) and increments it at `:162`; `STATE` defaults to `~/.local/state/shokunin-hyaku` (`:19`). Live values (read-only): next/kumitate=39 vs kumitate.round=18; next/kagi=25 vs 16; next/mori=20 vs 2; next/kama=21 vs 1. INFO stays correct. The row should not describe these as states frozen behind a shared counter.
- C-L3. "rule unchanged since r7" is exact for lines 816-818 only. The state enumeration changed at r8 (diff `d30b4e4` to entering: five hunks in the walk and the reason field; `-type f` removed, sort added, non-regular entries classified). No effect on the 21 regular `.round` files. Say so. Also add `baseline-r10` lines 1-39, which contain no WATCHDOG_STATE_LAG line. Line 8 masks `state_lag`, so it is not evidence.

## 2. Pointer verification (every pointer in both rows)

| ID | Pointer or claim | Check run | Result |
|---|---|---|---|
| P1 | `tools/mori-census.sh:733-737` | read entering 704-737 | HOLDS: 733 `age=$((NOW_EPOCH - ...))`; 734 `if [ "$age" -gt "$WATCHDOG_STALE_S" ]`; 735 `stale=1`; 736 `emit_finding WATCHDOG_STALE warn`; 737 `fi` |
| P2 | `:351` threshold | read | HOLDS: `WATCHDOG_STALE_S=${MORI_WATCHDOG_STALE_S:-900}`; pin line 293 identical text |
| P3 | `.ufo/watchdog.log:402` | read | HOLDS: `2026-10-15T01:58:27-03:00 tick=2`. Recount: 70 `tick=` lines, last at 402 |
| P4 | `.ufo/watchdog.log:582-585` | read | HOLDS: hyaku-inline launches tabi 06:47:50, kama 07:17:03, mori 07:18:05, kagi 07:23:21 |
| P5 | `scripts/hyaku/inline.sh:103` | read | HOLDS: `log "launch $lane round=$n pgid=$$ driver=hyaku-inline attempt=$a"` |
| P6 | baseline-r10 :24 (not cited by row) | grep | HOLDS: `FINDING WATCHDOG_STALE severity=warn ... threshold_s=900` |
| P7 | "WATCHDOG_ABSENT still fires" | baseline-r10:25; baseline-r20:53; `pgrep -af shokunin-watchdog` at 08:03:55 and 08:10:38 | HOLDS: ABSENT present in both baselines; pgrep no output, rc 1 both times |
| P8 | "daemon has not ticked since 01:58:27" | P3 | HOLDS |
| P9 | "STALE rule unchanged since r10" | `sed -n '454,643p'` of pin blob vs `sed -n '665,854p'` of entering blob, sha256 (first 16 hex) | HOLDS: both `4237f1dc5ecf9276` |
| P10 | STATE_LAG rule `tools/mori-census.sh:816-818` | read; pin 605-607; `d30b4e4` 419-421 | HOLDS: `if [ "$v" -lt "$lr" ]`; `state_lag=$((state_lag + 1))`; `emit_finding WATCHDOG_STATE_LAG info` |
| P11 | commit introducing the finding | `git -C mori-shokunin log -S 'WATCHDOG_STATE_LAG' -- tools/mori-census.sh` | HOLDS: `d30b4e4` only; `git show --stat d30b4e4` touches `tools/mori-census.sh` |
| P12 | `scripts/shokunin-watchdog.sh:220` | read 193-222; grep `\.round` over `scripts/` and `templates/` | HOLDS: `echo "$n" > "$UFO/state/${lane}.round"` inside `launch_lane`. Other hits are comments or log text (lines 27, 92, 96) |
| P13 | "13 lanes lag" | recount (section 7) | HOLDS: 13 LAG, 8 equal, 0 AHEAD over 21 `.round` files |
| P14 | "only the stopped daemon writes .round" | P12; `launch_lane` callers at `shokunin-watchdog.sh:361,368,400,403` (tick loop); none in `scripts/hyaku/`; pgrep rc 1 | HOLDS as to writers; daemon stopped. `.round` mtimes 2026-10-15 01:45:42 to 01:50:57 |
| P15 | register dissent: "census code byte-identical since r10" | E1 | BROKEN as written; the scoped statement holds |
| P16 | STALE commit (row has none) | `git log -S 'WATCHDOG_STALE' -- tools/mori-census.sh` | `5be8943` (r10 test and mutant text); `7ca17b1` (round-1 emit line) |
| P17 | C1 counting command over `c1-drift-entering.json` tokens vs r20 register keys | `comm -23` of sorted lists | 0 unclassified (both rows present). Class counts recomputed: census-schema-change 29, live-state 19, roster-change 2 (matches register) |

## 3. Defects to correct (text and evidence only; no class change)

E1. Register dissent field, "census code byte-identical since r10". Evidence:
- `git --no-optional-locks diff --stat 5be8943 2061780117e6ca637725004897bd288d3ba7e988 -- tools/mori-census.sh` gives `1 file changed, 2027 insertions(+), 116 deletions(-)`.
- `sha256sum` of the blobs: `5be8943` = `d7710981aa1c...b20`; `2061780` = `87b8d680b9b2...ab28` (equal to the lane worktree).
- Scoped truth. Same 16-hex checksums at pin and entering (ranges as pin / entering): probe block and ledger readers 454-643 / 665-854 = `4237f1dc5ecf9276`; `cap` 379-384 / 561-566 = `c9c955ed4f8d23c2`; `emit_finding` 354-366 / 419-431 = `377f68489f3070ac`; `emit_surface` 368-375 / 433-440 = `38cf51e8ce47e71b`; `have` 377 / 559 = `d89da2ace84fb08f`; `read_file` 401-405 / 612-616 = `2edd2071dd17413e`; `NOW_EPOCH` 317-318 / 382-383 = `28d91b5657d9dcc4`. `is_int` text identical (pin 1128, entering 2017). `WATCHDOG_LOG`, `TIMELINE_FILE`, `STATE_DIR`, `WATCHDOG_STALE_S` text identical (pin 259, 263, 264, 293; entering 297, 301, 302, 351).
- Consistent with `git diff -U0 5be8943 2061780`: no hunk between old lines 386 and 722.
Replacement text: "the watchdog probe, its ledger readers and its helpers are byte-identical since r10; the census file as a whole changed (+2027/-116)".

E2. STALE row: C-S2, C-S3, C-S4 (writer history, clock dependence, baseline pointer).

E3. STATE_LAG row: C-L1, C-L2 (second writer and counter), C-L3 (r8 qualifier, baseline absence).

E4. Neither row cites a baseline line that the token's +/- derives from (C-S4, C-L3).

## 4. Dissent: census-regression for STALE (VolatileContract H2/H3, C1Critic)

Under the stated rule (classify by cause; live-state = census code unchanged + host/fleet state differs), both rows qualify. I do not overturn the class.

The dissent's factual core is right. While another writer keeps the log warm, STALE cannot see a dead or hung daemon. Three facts limit its weight:
- WATCHDOG_ABSENT (warn) still fires, so the roll stays DRIFT (baseline-r20:53).
- The r20 baseline records STALE present (baseline-r20:39), so the re-pin does not encode the false-clean.
- STALE returns by itself when the log idles (knowledge doc section 4; the 07:51 -03 pre-pin drift).

I would relabel to census-regression only if the contract defined that class as "the census no longer measures its named condition". The knowledge doc does not say so. The blind spot belongs in the design-residual route it already has.

## 5. Timeline (watchdog.log and the STALE token; from read-only evidence)

| time (-03) | event | source |
|---|---|---|
| 2026-10-15 01:58:27 | last daemon tick | watchdog.log:402 |
| 2026-10-15 ~19:26 (pin 22:26:29Z) | r10 pin; STALE present | baseline-r10:24 |
| 2026-10-19 23:10:53 | first post-stop writer (headless slot driver) | watchdog.log:403 |
| 2026-10-20 00:41:08 | first hyaku-inline writer | watchdog.log:409 |
| 2026-10-21 07:18:05 | census window; last write before entering run; STALE absent | watchdog.log:584; c1-drift-entering.json |
| 2026-10-21 07:23:21 | last write (kagi round 25); none since | watchdog.log:585; stat at 08:12:47 |
| 2026-10-21 07:38:21 | absence window would end without a further write [derived] | rule + mtime |
| 2026-10-21 07:51 (10:51Z) | pre-pin drift: STALE present | knowledge doc section 4; baseline-r20:39 |

## 6. Seat reports (leads only)

TokWatchdog.md (MoriR20.TokWatchdog). Re-derived here: last tick at 402; hyaku-inline lines 582-585; 13-lane LAG set; daemon as the only `.round` writer; watchdog probe unchanged; hyaku counters separate. Not relied on: its scratch-file citations (`c1-pin-probe-scratch.json`), its SKILL.md and SCORECARD.md citations, and its kagi "round 24 at line 543" anchor. None of those were checked here.

## 7. Recount (read-only python over `.ufo/state/*.round` and `.ufo/watchdog.log`)

Rule as the census states it: a ledger line counts when field 1 starts with a digit and contains `T`, field 2 is `launch`, field 3 is the lane, field 4 is `round=N`; last match wins.

| ledger prefix | LAG | equal | AHEAD |
|---|---|---|---|
| 402 lines (pin time) | 0 | 21 | 0 |
| 584 lines (census time, last line mori 07:18:05) | 13 | 8 | 0 |
| 585 lines (now) | 13 | 8 | 0 |

Per lane at 585 lines (state / last ledger round / ledger line / writer):

| lane | .round | ledger | line | writer | status |
|---|---|---|---|---|---|
| aggregator | 10 | 10 | 390 | daemon | equal |
| audio | 1 | 1 | 337 | daemon | equal |
| chousa | 1 | 25 | 553 | hyaku-inline | LAG |
| game-dev-2d | 1 | 1 | 336 | daemon | equal |
| game-dev-3d | 1 | 1 | 353 | daemon | equal |
| kagi | 16 | 25 | 585 | hyaku-inline | LAG |
| kaidoku | 1 | 21 | 578 | hyaku-inline | LAG |
| kake | 16 | 23 | 558 | hyaku-inline | LAG |
| kama | 1 | 21 | 583 | hyaku-inline | LAG |
| kasegi | 17 | 23 | 519 | hyaku-inline | LAG |
| kengaku | 13 | 26 | 541 | hyaku-inline | LAG |
| kotoba | 16 | 16 | 376 | daemon | equal |
| kumitate | 18 | 38 | 561 | hyaku-inline | LAG |
| lore | 1 | 1 | 370 | daemon | equal |
| mado | 1 | 21 | 574 | hyaku-inline | LAG |
| mori | 2 | 20 | 584 | hyaku-inline | LAG |
| protocol | 14 | 14 | 394 | daemon | equal |
| revenger | 1 | 1 | 386 | daemon | equal |
| tabi | 1 | 20 | 582 | hyaku-inline | LAG |
| tameshi | 1 | 20 | 567 | hyaku-inline | LAG |
| tsukuroi | 1 | 20 | 580 | hyaku-inline | LAG |

`souji` has a hyaku launch (line 581) but no `.round` file, so the census does not compare it. Its roster status is not part of this row.

The 13 lag lanes match the 13 `WATCHDOG_STATE_LAG` lines in `corpus/evidence/baseline-r20-20261021T1051Z.json` lines 40-52.

## 8. Bounds, tools, commands

- Read-only throughout. The census was not run. The census file and all committed files were not edited. Git was used read-only (`--no-optional-locks`; `log`, `show`, `diff`, `diff --stat`).
- Read four host counter files under `~/.local/state/shokunin-hyaku/next/` (`kumitate`, `kagi`, `mori`, `kama`). Outside `~/.omp`; read-only.
- Not opened: `.ufo/interactive-sessions/`, `.ufo/worktrees/`, `.jj/`, `~/.omp`.
- Scratch under `/tmp/fam/` only: census blobs at `5be8943`, `d30b4e4`, `2061780`, `8f8c58e`; hunk diffs; the r7-to-entering watchdog block diff; the python recount.
- Tool installs: none. Used existing `/usr/bin/jq` (jq 1.8.2), `python3`, `sha256sum`, `diff`, `stat`, `pgrep`.

## 9. For the L1

- Apply C-S1 to C-S4, C-L1 to C-L3 and the E1 wording. No class change.
- Both tokens move with wall-clock time and with hyaku launches. Before treating a later drift on either token as a regression, re-check the log mtime against the census clock and the last ledger line.
