# ConnFleetSeatKillPath — connector, mori round 27 wave 1 (C1 to the fleet)

Seat: MoriR27.ConnFleetSeatKillPath (connector, leaf). Access date 2026-10-22. Read-only on every input.
Scratch: `/fast/scratch/hyaku/mori-r27/ConnFleetSeatKillPath/` (`sends.py`, `wd-b1.txt`, `send-b1.txt`; times and
lane/round labels only). Tooling: no install or update.

## Axes

- C1 depth: the entry's "fleet attribution of a victim" section.
- Calibration (held at 5): stop the corpus from claiming that earlyoom killed seats when the records cannot show it.
- Harm checks: no new tool (contract `.ufo/waves/round-27/contract.md:9-10`), no retention rise (no settings path,
  session id, session-store path or MESSAGE text below).

## Inputs and digests

| Input | sha256 | Notes |
|---|---|---|
| `scripts/hyaku/wave-slot.sh` | `41b487ef51012c099ab704e8c226f3bb701e11c120f7c6973ab73cb1f3737a81` | last change `108a0cd` 2026-10-21T05:39:34-03:00 |
| `.ufo/watchdog.log` (fleet root) | `9bee172a8abe6f5c83d14a25e2a2b69284917f302fec3d32ded824f3c4ab84e8` | 716 lines, first 2026-09-28T15:44:59-03:00, last 2026-10-22T12:40:22-03:00 |
| mori `.ufo/waves/round-26/capture/capture-boots.txt` | `d2c2b2cd63a9f79143a022bffe5ba6028dc5cbb03067275462f0983285e1bdc3` | boot windows lines 3-8 |
| `scripts/hyaku/inline.sh` (writer of the lines) | `40afe1856b16dbd566e3077b8496d1bfc4e9fc012525c7de255fcca06c7e6200` | |
| `scripts/shokunin-watchdog.sh` (legacy writer) | `04a3a2148efad2cd1be9bff2496cac520ab14597cab978eca241771226bb8d85` | |

Boot -1 window from `capture-boots.txt:7`: `first_utc_s=1792501029` to `last_utc_s=1792655690`, that is
2026-10-20T12:57:09Z to 2026-10-22T07:54:50Z (`date -u -d @…`). Boot 0 starts 2026-10-22T07:55:41Z (`:8`).

## Q1. Which fleet records could show that earlyoom (not the kernel) killed a seat's process

Short answer: none of the fleet's own records can. Only the system journal tells earlyoom kills from kernel kills,
and it names a process, never a seat.

1. **watchdog.log `lane-dead-no-report`** has two writers. The in-session driver writes
   `lane-dead-no-report $lane round=$n; retry same round (hyaku-inline attempt=$a: $why)`
   (`scripts/hyaku/inline.sh:136`), where `$why` is free text from the orchestrator (`inline.sh:134`). The legacy
   loop writes `lane-dead-no-report $lane round=$n; retry same round` (`scripts/shokunin-watchdog.sh:402`) when no
   report exists. Neither line records a signal, exit status, pid, boot id or memory state. Whole-log check:
   `rg -c -i '<pattern>' .ufo/watchdog.log` gives 0 for each of `oom`, `sigterm`, `sigkill`, `signal`, `earlyoom`,
   `killed`, `exit`, `memory`, `died`, `crash`. On the 31 `lane-dead-no-report` lines, `oom|memory|kill|signal|sigterm`
   matches 0 and `reboot|restart|boot` matches 0.
   Line kinds in the whole log: `launch` 325, `complete` 210, `lane-round-failed` 35, `lane-dead-no-report` 31,
   `wrap` 22, `steer` 15, `tick=N` 76, `launch-fail` 7, `watchdog` 1 (`awk '{print $2}' | sort | uniq -c`).
2. **hyaku `events.log` `attempt-failed`** mirrors line 1 with the same `$why` (`inline.sh:137`), so it adds
   nothing about the cause.
3. **The pid fields do not point at the killed process.** Inline `launch` lines record `pgid=$$` (`inline.sh:103`),
   the pid of the short-lived `inline.sh` shell, not the omp process. Equality check without printing values: of
   229 `pid=`/`pgid=` fields in the log, 0 equal the pid that earlyoom sent SIGTERM to in boot -1's one `omp`-class
   send.
4. **The wave-slot gate keeps no history.** It holds a grant while `MemAvailable < MIN_AVAIL_MB` (comment
   `wave-slot.sh:8-9`; test `:80`). The floor defaults to 6144 MiB (`:21`), which is 19.8% of this host's MemTotal
   (31721800 kB, `/proc/meminfo`). The ledger row holds only `time seats lane wave` (`:81`). `release` deletes the
   rows (`:94`), and no memory reading is stored at grant, release or death time. So it cannot show a death. The floor
   arrived in `cc57d9a` at 2026-10-21T03:09:19-03:00 (`git log -S MIN_AVAIL_MB`). It was in force for the
   2026-10-22 kills below and did not prevent them, because it gates only new grants.
5. **Seats have no process of their own** [INFERENCE]. In-session L1 rounds and closures are `task` subagents
   inside the parent omp session (`inline.sh:2-6`). At sampling time the host had 1 to 3 `omp` processes
   (`ps -eo comm=`: 3; a `/proc` walk a moment later: 1), while the peer roster lists dozens of running seats.
   earlyoom picks a process (`kill.c`, rows S118/S119). So killing an `omp` process ends the whole session and every
   seat in it at once. A `python`/`python3` send kills a tool child, and the seat only sees a failed command in its
   own transcript.
6. **Only the journal can tell earlyoom from the kernel.** For earlyoom, the source is the `earlyoom.service` send
   lines (`sending SIGTERM|SIGKILL to process … "<comm>"`, followed by one `process … exited after` line each). For
   the kernel, it is `Out of memory: Killed process` plus `oom-kill:` in `journalctl -k`, and the user manager's
   `Failed with result 'oom-kill'` on the unit whose cgroup held the victim. An earlyoom kill never sets that unit
   result (earlyoom has no `--kernel-oom` in v1.9.0, `corpus/lessons/round-26.md:20-21`) [INFERENCE for the unit
   result].

## Q2. Do boot -1 earlyoom sends coincide with dead seats or lane-dead lines

Command: `python3 /fast/scratch/hyaku/mori-r27/ConnFleetSeatKillPath/sends.py -1` (journal JSON; it classifies
MESSAGE text in memory and prints only times, signal and process class).

Totals: 39 sends (38 SIGTERM, 1 SIGKILL), and 39 `exited after` lines. That matches `capture-boots.txt:16`.
By class: `python3` 17 TERM, `python` 10 TERM, `omp` 1 TERM, `other` 10 TERM and 1 KILL. Grouping sends no more
than 600 s apart gives 13 clusters:

| Cluster (UTC) | Sends | Classes | watchdog lines within ±30 min |
|---|---|---|---|
| 2026-10-20 16:54:08 to 22:51:30 (8 clusters) | 11 | other 10 TERM + 1 KILL | launch 16, complete 13, lane-dead 0 |
| 2026-10-21 06:05:25 to 07:09:23 (4 clusters) | 8 | python3 8 | launch 15, complete 8, lane-dead 7 |
| 2026-10-22 06:15:59 to 06:16:05 | 20 | omp 1, python 10, python3 9 | none |
| Kernel kill 2026-10-22 06:54:59 (`journalctl -b -1 -k`) | 1 | other; one user `app-*.scope` `Failed with result 'oom-kill'` | none |

All 10 `lane-dead-no-report` lines in boot -1 come from the inline writer. Their distance to the nearest send or
kernel kill:

| Lines (UTC) | Count | Nearest kill |
|---|---|---|
| 2026-10-21 03:47:34 to 03:47:36 | 2 | first send of the next cluster 8269 to 8271 s later |
| 2026-10-21 05:47:15 to 05:47:21 | 5 | first python3 send 1084 to 1090 s later (the death came before the send) |
| 2026-10-21 07:33:14 to 07:40:20 | 3 | last python3 send of the cluster 1431 to 1857 s earlier |

No lane-dead line falls within 600 s of any send. The `events.log` `attempt-failed` lines match these 10 to the
second.

**The only `omp` send leaves no fleet record.** The last boot -1 watchdog line is at 2026-10-22T02:59:43Z, 3 h 16
min before the `omp` SIGTERM. The send line's numeric fields give `oom_score` 1079, `oom_score_adj` 200 and `VmRSS`
10232 MiB. Its exit line, two records later, reads 2.603 s. The nearby low-memory report reads mem avail 9.43% and
swap free 0.00%. At the end of boot -1, 12 lanes have a `launch` with no later `complete` or lane-dead line. Eight
of them launched between 2026-10-21T23:34Z and 2026-10-22T00:54Z. Four are older (2026-10-20T21:30Z and
2026-10-21T14:47Z to 17:54Z) and got no dead line afterwards.

**Dead seats are recorded after the reboot, with the detection time.** Boot 0 holds 11 lane-dead lines: 7 at
2026-10-22T07:58:59Z (the same second, 3 min 18 s after boot 0 starts), all 7 among the 12 in-flight lanes above,
then 4 at 08:31:12Z to 08:31:57Z (3 retries of those lanes plus one lane that was not in flight at the end of boot
-1). Boot 0 has 0 earlyoom sends (the only `sending SIG` match is the threshold banner) and 0 kernel kills at
access time.

## Q3. What mori can and cannot attribute

Can attribute (counts, classes, windows):
- earlyoom versus kernel, per kill event, from the journal only (Q1 item 6).
- The victim's process class and its `oom_score`, `oom_score_adj` and `VmRSS` at send time.
- Which lanes were in flight in a boot (from the last `launch` with no later `complete` or dead line), and whether a
  fleet line falls inside a kill window.
- That the one `omp` kill in boot -1 hit while the fleet log was silent and while 8 recent lanes were in flight.

Cannot attribute:
- **Which seat died.** Seats share the omp process [INFERENCE, Q1 item 5]. The best possible result is "the session
  was killed".
- **Which session the killed `omp` was.** The fleet stores no omp pid (Q1 item 3), and the journal's fleet-runtime
  records for that boot carry none of the `omp`, `bun` or `node` command names (0 records by `_COMM`). So an
  interactive omp cannot be told apart from the orchestrating one.
- **Why a lane died.** Lane-dead lines carry no cause, and the boot 0 batch is equally consistent with the 06:16Z
  `omp` SIGTERM, the 06:54Z kernel kill, or the reboot at 07:54Z.
- **Python sends.** `python`/`python3` victims (27 of 39) cannot be tied to a fleet helper or to an unrelated
  program, because the class label is all mori may keep.
- **Durability.** `watchdog.log` is mutable and never committed (`scripts/hyaku/closure-prompt.md:15` "mutable —
  copy this digest into notes"; `scripts/hyaku/fleet-commit.sh:32` refuses it). Any citation needs the sha256 and
  line count above.

Contradiction to state, not to smooth over: `corpus/lessons/round-26.md:23-24` says "earlyoom can still kill
running seats". The capability is true, but the boot -1 record does not show it happening. Zero lane-dead lines fall
within 600 s of a send, and the only kill that could end a whole session left no fleet line before the reboot.

## Proposed move (one, bounded)

Add an attribution limit to C1 as prose in the entry plus three SKILL `Round27` rows: mori reports kills at the
session level, never the seat level, joins records only by time window, and treats lane-dead lines written after a
reboot as the time the death was detected. This needs no tool. It turns the frontier remainder into a stated limit
backed by counts. It improves depth (C1 rows have something real to decide) and calibration, and it does not touch
C2, retention or any tool.

Ready to paste into `corpus/knowledge/oom-victim-selection-r27.md`, in a fleet-attribution section:

```markdown
**Fleet attribution stops at the session.** In-session seats are `task` subagents of one omp process, so an
earlyoom or kernel kill of an `omp`-class process ends every seat in that session at once; a `python`/`python3`
send kills a tool child, not a seat. Fleet records carry no cause: `lane-dead-no-report` and `attempt-failed` hold
lane, round, attempt and free text only, and launch lines record the driver shell's pid, not omp's. Only the
journal separates earlyoom sends (`earlyoom.service`) from kernel kills (`journalctl -k` plus a unit result of
`oom-kill`). In boot -1, 39 sends (python3 17, python 10, other 11, omp 1) and one kernel kill (other) met zero
lane-dead lines within 600 s; the one omp send (oom_score_adj 200) came 3 h 16 min after the last fleet line, and
the 7 lanes then in flight were marked dead 3 min after the next boot, at detection time.
```

Ready to paste as `SKILL.md` `## … Round27` rows (the heading belongs to the planner; the entry slug is kept):

```markdown
| Situation | Decide | Grounded in |
|---|---|---|
| A seat or lane is dead and you want the cause | Check the journal for the boot: earlyoom send lines or kernel `Killed process`/`oom-kill`; fleet lines never name a cause | `corpus/knowledge/oom-victim-selection-r27.md` |
| An earlyoom or kernel victim has class `omp` | Report a session-level kill of every in-session seat; never name one seat | `corpus/knowledge/oom-victim-selection-r27.md` |
| A `lane-dead-no-report` line is in the first minutes of a boot | It marks when the death was detected after the reboot; bound the death to the old boot's last fleet line through its end | `corpus/knowledge/oom-victim-selection-r27.md` |
```

## Risks

- The in-process seat model is [INFERENCE] from `inline.sh:2-6` and process counts. If some seats run as separate
  omp processes, the first and second rows still hold for those seats but the "every seat" scope narrows.
- The "detected after reboot" reading of the 07:58:59Z batch rests on timing (7 lines in one second, 3 min into
  boot 0). The free text of those lines was not read into this report because of the line-kinds-only bound.
- The unit result `oom-kill` appearing only for kernel kills is [INFERENCE]. The S-row scouts on systemd and cgroup
  should confirm it before the row cites it as a source fact.
- Process counts were sampled live at about 2026-10-22T15:50Z and will drift. The entry should cite them as a sample.
- Retention: the text above has no settings path, session id, session-store path or MESSAGE text, so the scan
  should not rise [INFERENCE until the planner reruns `tools/mori-retention-gate.py scan`].

## Verification for the planner (read-only, rerunnable)

```sh
sha256sum /home/vgpnk/Projects/shokunin/.ufo/watchdog.log            # compare with the digest above
awk '{print $2}' /home/vgpnk/Projects/shokunin/.ufo/watchdog.log | sort | uniq -c
rg -c -i 'oom|sigterm|sigkill|signal|earlyoom|killed' /home/vgpnk/Projects/shokunin/.ufo/watchdog.log   # expect no output (0)
python3 /fast/scratch/hyaku/mori-r27/ConnFleetSeatKillPath/sends.py -1   # expect sends 39, 13 clusters, kernel 1
journalctl -b 0 -u earlyoom -o cat --no-pager | rg -c 'sending SIG(TERM|KILL) to process'      # expect no output (0)
bash /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-27/count-c1.sh <landed rev>   # C1 rows count
```

Not run by this seat: `count-c1.sh`, `count-c2.sh` and the retention scan (none of them are in scope for a
connector).
