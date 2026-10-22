source: S118 (earlyoom kill.c at tag v1.9.0 — https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c — victim selection, sha256 b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3); S119 (earlyoom main.c at v1.9.0 — option parsing and the -p self-protection); S115 (earlyoom MANPAGE.md at v1.9.0 — the documented selection options); S120 (earlyoom.service.in at v1.9.0 — the unit's own OOMScoreAdjust); S131 (earlyoom v1.9.0 tag tree and earlyoom.default — the shipped default arguments); S003 (Linux mm/oom_kill.c at v7.2 — oom_badness and the kernel's choice, sha256 452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e); S127 (Linux fs/proc/base.c, include/uapi/linux/oom.h and kernel/fork.c at v7.2 — how /proc/<pid>/oom_score is derived, the oom_score_adj write rules and fork inheritance); S128 (man-pages 6.19 proc_pid_oom_score_adj(5) and proc_pid_oom_score(5) — the documented contract and where it differs from the code); S082 (Linux Documentation/filesystems/proc.rst at v7.2 — the documented badness range); S092 (Linux Documentation/admin-guide/cgroup-v2.rst at v7.2 — memory.oom.group); S129 (systemd v262 systemd.exec.xml and systemd-system.conf.xml — OOMScoreAdjust= and DefaultOOMScoreAdjust=); S130 (systemd v262 units/user@.service.in, src/core/main.c and commit ce7de0ba — the per-user manager at 100 and its children at 100 more); S132 (oh-my-pi v18.12.6 shell.rs and Bun bun-v1.4.3 spawn sources — the fleet's runtimes set no oom_score_adj)
verified-at: 2026-10-22 — upstream bytes opened at earlyoom tag v1.9.0 (commit 202d4db0d308ca6478f68de68b46cae34896ddaf), Linux tag v7.2 and systemd tag v262 (commit 8cc40e0c5e9234bf45084751ac53b1fbfe70b492); host read-only on 2026-10-22 (kernel 7.2.11-arch1-1, systemd 262-1, earlyoom 1.9.0-1 active): process aggregates at 15:56:35Z (committed) and 15:46:40Z, earlyoom send-line aggregates over every retained boot (committed run 15:56Z), unit properties and an unprivileged oom_score_adj probe on processes the probe started (wave-1 seats HostUnitOomAdjust and CriticInheritProbe).
recheck: on a kernel release re-open `fs/proc/base.c` `proc_oom_score` and `mm/oom_kill.c` `oom_badness` at the new tag; on an earlyoom release re-open `kill.c` `is_larger` and the send-line format; on a systemd release re-open `units/user@.service.in` and `src/core/main.c` `determine_default_oom_score_adjust`; host: `python3 -I -B .ufo/waves/round-27/evidence/oom-score-classes.py` and `python3 -I -B .ufo/waves/round-27/evidence/boot-send-classes.py` (aggregates only), `systemctl show earlyoom.service user@$(id -u).service -p OOMScoreAdjust`, `systemctl --user show -p DefaultOOMScoreAdjust`
author: MoriR27 (L1), from the wave-1 seat reports under `.ufo/waves/round-27/w1/` (the drafting scribe seat died at spawn; this text is the L1's).

# Which process an OOM killer on this host picks, and why — earlyoom 1.9.0, the Linux 7.2 kernel, and the fleet's place in the ranking

## Scope

Round 26 recorded that earlyoom 1.9.0 is this host's running userspace OOM killer and that it sent 38 SIGTERM and
1 SIGKILL lines in boot -1 (`corpus/knowledge/userspace-oom-killers-r26.md`). Before this round mori's knowledge entries held no victim-selection
rule; its lessons and source rows held only the one-line default "kill the process with the highest `oom_score`"
(`corpus/lessons/round-26.md:67`, S118's scope) and earlyoom's own `OOMScoreAdjust=-100` (S120), and the sibling
lane tsukuroi had measured the host's `oom_score_adj` bands on 2026-10-14 (Adjacency below). This entry answers the next question,
the FR10 remainder "fleet attribution of a victim": how earlyoom and the kernel choose the process to kill, what
`oom_score_adj` the fleet's processes carry on this host and where that value comes from, and what share of those
39 sends hit the fleet's own runtimes. It is a reading note: it changes no setting, writes no `oom_score_adj` of any
process it did not start, sends no signal, and copies no command line, pid, uid number, journal `MESSAGE` text, or
value of `/etc/default/earlyoom` or of any `--prefer`/`--avoid`/`--ignore` expression.

## Facts

### 1. How earlyoom 1.9.0 picks its victim (S118, S115, S119)

- **One pass, highest score wins.** `find_largest_process` scans the numeric `/proc` entries once and keeps the best
  candidate through `is_larger` (S118 `kill.c:525-527,551-578`). By default the key is the process's
  `/proc/<pid>/oom_score`, read as the kernel exports it (`kill.c:396-401`); an exact tie goes to the larger resident
  set (`kill.c:457-465`). The manual says the same: kill "the process with the highest oom_score" (S115
  `MANPAGE.md:19-21`).
- **`--sort-by-rss`** makes the resident set the primary key with `oom_score` as the tie-break, and falls back to
  `oom_score` when either side reads a resident set of 0 (S118 `kill.c:429-455`; S115 `MANPAGE.md:202-203`).
- **`--prefer`/`--avoid`/`--ignore` match the process name only** (`/proc/<pid>/comm`, at most 15 bytes), never the
  command line (S118 `kill.c:404-427`; S115 `MANPAGE.md:177-200`). A `--prefer` match adds 300 to the candidate's
  `oom_score` and an `--avoid` match subtracts 300 (`kill.c:24-27,410-421`); under `--sort-by-rss` they add or
  subtract 3,145,728 KiB of resident set instead (`kill.c:29-32`). `--ignore` removes the candidate
  (`kill.c:424-426`). Each option takes one regular expression; a repeated flag overwrites the earlier one (S119
  `main.c:289,292,302`).
- **The +300 is larger than it looks.** The kernel exports its score scaled by 2/3 (Fact 2), so earlyoom's +300 on
  the exported value weighs like an `oom_score_adj` of about +450 [INFERENCE: arithmetic over S127 `base.c:597` and
  S118 `kill.c:24-25`, wave-1 CriticC1Novelty].
- **The score in a send line is earlyoom's score, not the kernel's.** The send line prints the candidate's
  `oom_score` after the prefer/avoid adjustment (S118 `kill.c:627`, format `sending %s to process %d uid %d "%s":
  oom_score %d, oom_score_adj %d, VmRSS %lld MiB, cmdline "%s"`).
- **What it skips:** pid 1 and 2 (`kill.c:357-359`), kernel threads (`ppid == 2`, `:391-393`), uid 0 under
  `--ignore-root-user` (`:363-374`), processes whose `stat` or `oom_score` it cannot read (`:377-381,396-401`), and
  `oom_score_adj == -1000`, checked after the comparison (`:467-478`). It does not skip itself during the scan; it
  notices only after choosing itself and then sleeps (`:587-592`).
- **A victim that vanishes** before the signal produces one `kill failed:` line and no re-selection; the next attempt
  is the next poll (S118 `kill.c:640-657`).
- **Defaults.** No prefer, avoid or ignore expression exists by default (S115 has none; the shipped
  `earlyoom.default` sets only `EARLYOOM_ARGS="-r 3600"`, S131 `earlyoom.default:5`). `-i` has been a no-op since
  v1.7 (S115 `MANPAGE.md:89-90`), but the long option `--ignore-root-user` still works and is missing from the 1.9.0
  manual (S119 `main.c:185,281`).
- **earlyoom protects itself through its unit, not its scan:** the upstream unit sets `OOMScoreAdjust=-100` and
  `Nice=-20` (S120 `earlyoom.service.in:12,14`); `-p` would do the same from inside (S119 `main.c:397,401`). -100
  lowers its score; only -1000 would exclude it.

### 2. How the kernel scores a process (S003, S127, S092)

- **Points are pages.** `oom_badness` adds the resident set, swap entries and page tables in pages (S003
  `mm/oom_kill.c:228-229`), then shifts the sum by the adjustment scaled to memory size: `adj *= totalpages / 1000;
  points += adj;` (`:232-234`). An `oom_score_adj` of 200 is therefore worth 20% of RAM plus swap, not 200 points.
- **Who is never chosen:** init and kernel threads (`mm/oom_kill.c:160-167`) and any task at exactly -1000
  (`:216-222`). The kernel keeps the highest score; a tie keeps the first task scanned (`:340`).
- **What `/proc/<pid>/oom_score` shows:** `(1000 + badness * 1000 / totalpages) * 2 / 3`, with `totalpages` = RAM +
  swap, and 0 for an excluded task (S127 `fs/proc/base.c:583-599`). The range is 0 to 2000. A process with no memory
  reads 666 at adjustment 0 and 800 at adjustment 200; each further percent of RAM plus swap it holds adds about
  6.7. This is how the host values below read: 600 for earlyoom at -100, 800 for idle processes at 200.
- **The documentation and the code disagree in three places.** `proc.rst` calls the badness a 0–1000 value (S082
  `proc.rst:1761-1763`) while the exported file is 0–2000; the man page says the adjustment is "added" (S128
  `proc_pid_oom_score_adj(5)`, adj page `:102-103`) while the code scales it by memory size; and the man page's
  "root processes are given 3% extra memory" has no implementation in v7.2 `oom_badness` (S128 adj page `:86-88`
  against S003 `mm/oom_kill.c:226-235`). Read scores from the code, not the pages.
- **`memory.oom.group`.** When it is 1 on a cgroup, a kernel OOM kill takes every task of that cgroup's subtree
  together, sparing only tasks at -1000 (S092 `cgroup-v2.rst:1450-1466`; S003 `mm/oom_kill.c:998-1006,1040-1053`).
  It is 0 at every level measured on this host (wave-1 HostUnitOomAdjust: `user.slice` down to an app scope,
  `system.slice`, `earlyoom.service`). It does not affect earlyoom, which signals one process.

### 3. Where the fleet's adjustment comes from (S129, S130, S127)

- **The per-user service manager runs at 100** (`OOMScoreAdjust=100`, S130 `units/user@.service.in:35`), added by
  systemd commit `ce7de0ba` ("units: run user service managers at OOM score adjustment 100").
- **Its children run at 100 more.** An unprivileged manager sets its default for the processes it starts to its own
  value plus 100 (S130 `src/core/main.c:3045-3063`, `b = saturate_add(a, 100, OOM_SCORE_ADJ_MAX)` at `:3063`; the
  manual sentence is S129 `systemd-system.conf.xml:305-306`). The `systemd.exec(5)` sentence "normally at 0" (S129
  `systemd.exec.xml:1299-1300`) describes the system manager, not a user manager.
- **The fleet's runtimes do not set it.** At the installed versions, oh-my-pi v18.12.6 and Bun bun-v1.4.3 contain no
  `oom_score_adj` or `OOMScoreAdjust` anywhere in their source trees; an omp shell run takes only command, cwd, env,
  timeout, signal, filesystem and stream options, and Bun's only priority call is the nice-range `setpriority` (S132
  `shell.rs:134-152`, `c-bindings.cpp:58`, `node_os.bind.ts:74-75`; whole-tree search in wave-1 SrcOmpBunOomAdj).
  The fleet's 200 is inherited from the session's launch chain, not chosen by the harness.
- **Inheritance.** `fork` copies both the value and its floor (S127 `kernel/fork.c:1768-1769,1949-1966`); nothing in
  `execve` resets them [INFERENCE from absence: `fs/exec.c` at v7.2 writes neither field, wave-1 CriticInheritProbe].
  Every process a user unit starts, and everything those processes start, inherits 200 unless something writes a new
  value.
- **The floor, not a ratchet.** A process may raise its own value and lower it again down to `oom_score_adj_min`;
  only a writer with `CAP_SYS_RESOURCE` may go below that floor or move it (S127 `fs/proc/base.c:1131-1133,
  1156-1157`). The range is -1000 to 1000 (`base.c:1275-1279`). Here the floor is 100, because PID 1 wrote the user
  manager's 100 with privilege. The unprivileged probe on processes it started (wave-1 CriticInheritProbe) raised a
  process from 200 to 500, lowered it to 199 (accepted), and was refused at 99 and at 0 (`EACCES`), with 100 the
  lowest accepted value. "Can raise but never lower" is false here.

### 4. The fleet in the ranking on this host (L1 capture, committed sample 2026-10-22T15:56:35Z)

`python3 -I -B .ufo/waves/round-27/evidence/oom-score-classes.py` (output `evidence/oom-score-classes.txt`) read 792
processes in the committed sample (an earlier run at 15:46:40Z read 1213, most of the difference kernel threads,
with the same ranking). By class:

| Class | Processes | `oom_score` min / median / max | `oom_score_adj` values (count) |
|---|---|---|---|
| omp | 1 | 847 / 847 / 847 | 200 (1) |
| python | 27 | 800 / 800 / 800 | 200 (27) |
| other | 83 | 67 / 800 / 866 | 200 (66), 0 (13), -900 (2), 100 (1), 300 (1) |
| systemd | 12 | 0 / 666 / 733 | 0 (9), -1000 (1), -250 (1), 100 (1) |
| earlyoom | 1 | 600 | -100 (1) |
| kernel threads | 668 | 0 | 0 (668) |

The single `omp` process held the second-highest score on the host (847, about 7% of RAM plus swap above the 800
floor of its band); only one `other`-class process at adjustment 300 ranked above it. The fleet's in-session seats
run as subagents inside that one process [INFERENCE: they are `task` jobs of one session, and no other `omp` process
was visible], so when earlyoom picks it, every in-session seat of every lane ends at once.

### 5. Whom earlyoom actually signalled (L1 capture over every retained boot)

`python3 -I -B .ufo/waves/round-27/evidence/boot-send-classes.py` (output `evidence/boot-send-classes.txt`) parses
the S118 `kill.c:627` send-line format in memory and prints aggregates only. Boots -5 to -2 and boot 0 hold no send
lines; boot -1 holds all 39 (38 SIGTERM, 1 SIGKILL), to 39 distinct processes:

- **By process-name class:** python 27, other 11, omp 1. A name in a fleet runtime's class does not prove the
  process belonged to the fleet: an unrelated `python` reads the same. Every victim ran under the operator's account and at
  `oom_score_adj` 200.
- **Scores:** send-line `oom_score` 1079 / 1101 / 1619 (min / median / max); resident set 4 / 10,232 / 23,653 MiB.
- **8 of the 39 send lines carry a score above the kernel's ceiling for their adjustment** (`(1000 + 200 + 1000) * 2
  / 3 = 1466` for 200; `above_kernel_ceiling_for_adj=8` in the committed output). The ceiling assumes a process's
  resident set, swap entries and page tables together stay within RAM plus swap [INFERENCE]. Only earlyoom's +300 `--prefer` adjustment can produce that (Fact 1), so the host's prefer
  expression — present in earlyoom's argument list, value not read (wave-1 HostUnitOomAdjust) — matched at least 8
  victims. This is a count of send lines, not of how the expression reads.
- **Timing:** 20 of the 39 sends fell in the hour 2026-10-22T06Z; the rest are spread over 2026-10-20 and 2026-10-21.
  The one `omp` send was at 2026-10-22T06:16Z (wave-1 ConnFleetSeatKillPath).

### 6. What the fleet's records can and cannot attribute (wave-1 ConnFleetSeatKillPath)

- No fleet record names a kill cause. `lane-dead-no-report` lines carry no signal, exit status or process id; the
  watchdog log has no kill words; the seat gate keeps no history after `release`.
- The boot -1 `omp` send left no fleet line within 3 h 16 min; seven lanes were marked dead at 2026-10-22T07:58:59Z,
  3 min 18 s into boot 0. That is when the death was detected, after the reboot, not when it happened.
- Only the system journal tells earlyoom kills from kernel kills, and it names a process class, never a seat or a
  lane. Joining a send to a lane is a time-window inference, never an attribution.

## Decision table

| Situation | What to conclude | What not to conclude |
|---|---|---|
| earlyoom sent a signal; which fleet process was most at risk | the process with the highest `oom_score` as earlyoom computes it: kernel score (Fact 2) plus or minus 300 for a prefer/avoid name match (Fact 1); on this host the single `omp` process ranks second (Fact 4) | that the largest process is chosen: the key is `oom_score` unless `--sort-by-rss` is set |
| a send line's `oom_score` exceeds `(2000 + oom_score_adj) * 2 / 3` | a `--prefer` match added 300 to that victim | anything about the expression's text; it is never read |
| a fleet process shows `oom_score_adj` 200 | it descends from a user unit of an unprivileged user manager (100 + 100) and is weighted as if it held 20% more of RAM plus swap | that someone configured it, or that it is pinned: it can be raised, and lowered down to the floor of 100 |
| `memory.oom.group` is 1 on a cgroup | a kernel OOM kill there takes the whole subtree | that earlyoom does the same; it signals one process |
| an in-session seat died and earlyoom sent to an `omp` process in that window | the session process may have been the victim, which ends every in-session seat | which seat or lane the kill was "for"; the journal names a class, not a seat |
| a lane is marked dead early in a boot | detection after a reboot | the time of death |

## Limits

- The process aggregates are one sample; scores move with memory use. The send aggregates cover the retained
  journal only.
- Class labels come from the 15-byte process name; a fleet helper named `python` and an unrelated `python` are the
  same class. The `other` class hides every non-fleet name on purpose.
- The `omp` single-process seat model is inference from the in-session design, not a process-tree read.
- The prefer-match count is a lower bound: a prefer-matched victim whose kernel score plus 300 stays under the
  ceiling is not counted.
- Arch's kernel build was not diffed against the v7.2 tag for `fs/proc/base.c` or `mm/oom_kill.c`.

## What it changes for mori

Before this round mori could count earlyoom's sends but not explain them. It can now read a send line's score
against the kernel formula, tell a prefer-adjusted victim from a plain one, explain the fleet's 200 band from
systemd's code rather than guess it, and say why one earlyoom send to `omp` is a fleet-wide event while a `python`
send kills one tool process. The SKILL.md `Round27` decision table carries the routing.

## Adjacency

Adjacent: `tsukuroi-shokunin/corpus/knowledge/oom-event-plane.md` and `kill-event-deep-r8.md` (tsukuroi, OS state)
record two earlier kill events from before earlyoom was installed (2026-10-20) and the live +200 band with its origin
open; this entry supplies the origin (Fact 3) and corrects one model there: the kernel does not scan the +200 band
first, it makes one pass and keeps the highest adjusted score (S003 `mm/oom_kill.c:228-234,340`). Cited, not
absorbed; neither tsukuroi event enters the earlyoom send counts above (wave-1 ConnSiblingOverlap). Source ids are
lane-local: tsukuroi's S119 and S127 are not mori's.

## Not claimed

No victim identity, pid, uid number, command line, prefer/avoid/ignore expression or `MESSAGE` text. No claim that
earlyoom killed any particular seat. No setting is recommended or changed.
