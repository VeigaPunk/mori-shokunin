VERDICT: HOLDS. Post-pin drift is `none` on an independent run (rc 0, 0 tokens). The window is open but bounded: a scheduled wall-clock gate expiry at 11:47:50Z (lane tabi) will break the pin at the first census after it [INFERENCE: predicted from ledger and census code, not observed].

Scope: claim C1 post-pin (`MORI_DRIFT: none` against corpus/evidence/baseline-r20-20261021T1051Z.json). Leaf seat, no subagents, no tool installs or updates, no lane production file touched. Writes only under falsify/PostPinWindow/ and this report. All times UTC.

## 1. Run (exactly once)
Command: `bash /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-census.sh --drift /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/baseline-r20-20261021T1051Z.json`
- T0 11:00:57Z, T1 11:02:06Z, wall 68.8 s (job bg_511)
- rc = 0
- stdout: `MORI_DRIFT: none` (17 B, sha256 090c9293...bd91), saved at falsify/PostPinWindow/census-drift.out
- stderr: empty (0 B), saved at falsify/PostPinWindow/census-drift.err
- tokens: 0. Classified 0 of 0, unclassified 0.
- Pre-checks: baseline sha256 e528bc15...8433 (matches drift-repin-r20.md header, unchanged). Census sha256 87b8d680... (matches pin census_sha256 and register census_sha256, unchanged). No MORI_* variable in the shell environment (checked by name), so the run used live host defaults, as at pin.

## 2. Stability window
| UTC | event | evidence |
|---|---|---|
| 10:53:07 | pin written | baseline header `pinned_ts` |
| 10:55:31 | post-pin `none`, rc 0 (L1) | drift-repin-r20.md section 4; c1-drift-r20-postpin.txt read, not re-run |
| 11:00:57-11:02:06 | post-pin `none`, rc 0 (this seat) | census-drift.out |
| 11:47:50 | tabi young gate ends (launch 09:47:50 + 7200 s) | watchdog.log line 582; census.sh 360, 2376-2378 |
| 12:17:03 | kama young gate ends | watchdog.log line 583 |
| 12:18:05 | mori young gate ends | watchdog.log line 584 |
| 12:23:21 | kagi young gate ends | watchdog.log line 585 |

Measured no-break span: 10:53:07 to 11:02:06 (8 min 59 s), two `none` readings. Not measured: 10:55:31 to 11:00:57, and anything after 11:02:06.

## 3. Ledger and lane events since 10:53:07 (read-only)
- watchdog.log: 585 lines; mtime 07:23:21.68 -03 (10:23:21.68Z); last line 585 is `launch kagi round=25`. Zero ledger events in the window, and none since 10:23:21Z.
- Lane report commits: `git log --branches -- .ufo/reports` since 10:53:07 returns nothing. No commit of any kind on any fleet branch since 10:35:43 (count 0). master 7fd7c78 (10:35:42, tameshi round-20 report) is the last report commit. The same query returns mado 850b075 at 10:22:39 for a 10:20-10:25 window, so the query is valid.
- .ufo/state/*.round: all mtimes 2026-10-15 (no writes). shokunin.conf mtime 2026-10-19 21:10 -03 (roster unchanged).
- Committed reports absent from HEAD for tabi r20, mori r20, kama r21, kagi r25 (`git cat-file -e HEAD:...` rc 128). All four stay row-8 young until their gate ends.
- Waves, independent replication (read-only, same rule as probe_waves 865-932): 23 dirs carry a registry/dispatch/run or settle marker. 10 are unsettled, all aged (minimum 414492 s). That set equals the 10 WAVE_UNSETTLED_AGE findings in the pin. No young unsettled wave exists, so no scheduled wave flip.

## 4. Token classification
- Zero tokens in this window, so nothing to classify.
- The r20 register (50 tokens: census-schema-change 29, live-state 19, roster-change 2; counted with /usr/bin/jq) classifies r10-to-r20 differences. It does not cover post-pin drift, and no register token is active now.
- [INFERENCE] Next break, by cause: `SURFACE lane.tabi` changes from `young (basis=row-8 reason=age_le_gate gate_s=7200)` to progressing, progressing-weak or silent (row-A/C/D), or to not-open if a report or close line lands first. Expected field tokens: -gate_s, -reason, basis (value changed), +subject_commits and +window, or equivalent. These are the field families the register already holds as live-state (+gate_s, +reason, +subject_commits, +window, basis). Cause: wall-clock gate (LANE_SILENCE_S=7200) with census code unchanged. Young rows return at census.sh 2376-2378, before the row-6 and row-9 git probes.

## 5. What `none` does not certify
- Two `none` readings across 9 minutes is a point-in-time match, not a stability proof.
- Volatile fields are masked (counters, gauges, timestamps, byte rates), so their magnitudes are unobserved.
- drift_scan compares only the first word of multi-word values (io_avg_since_boot device list; the added nvme0n1p1 device is invisible). Duplicate keys concatenate (round=). Findings pair positionally (obs=). A class with zero records on both sides yields no token. These are register blind spots.
- Standing reference warnings: WATCHDOG_ABSENT, WATCHDOG_STALE (log idle 37 min at T0), and 10 WAVE_UNSETTLED_AGE. `none` means unchanged since pin, not healthy.
- Event-driven breaks can occur at any time: a watchdog.log write (toggles STALE and lane rows); a lane report commit (row-6 not-open); a launch or complete line for a young lane; new OOM, coredump or kill journal records; a write inside an aged wave (age reset); a tmux server start; a roster edit; a memory or disk threshold crossing.

## 6. Handoff
- Exactly-once rule: not re-run. Recommend one census --drift run after 11:47:50 to observe the predicted tabi break, then classify that break by cause against watchdog.log lines 582-585.
- Tools: none installed or updated. Used bash, git (read-only, --no-optional-locks), sha256sum, stat, wc, date, /usr/bin/jq, and read-only Python.
- Scratch kept: falsify/PostPinWindow/ (census-drift.out, census-drift.err, register-keys.txt).
