source: S161 (procps-ng v4.0.7 `man/pgrep.1`), S162 (procps-ng v4.0.7 `src/pgrep.c`), S163 (Linux v7.2 `include/linux/sched.h`), S164 (Linux v7.2 `fs/exec.c`), S165 (Linux v7.2 `fs/binfmt_script.c`), S167 (Linux v7.2 `fs/proc/array.c`), S169 (man-pages 6.20 `proc_pid_comm.5`), S170 (man-pages 6.20 `proc_pid_cmdline.5`), S171 (man-pages 6.20 `proc_pid_stat.5`), S172 (man-pages 6.20 `PR_SET_NAME.2const`), S173 (Linux v7.2 `Documentation/admin-guide/sysctl/kernel.rst`), S174 (man-pages 6.20 `proc_locks.5`); prior lane rows S027 (pidfd_open)
verified-at: 2026-10-22 (round 31; host procps-ng 4.0.7-1, Linux 7.2.11, bash 5.3.20; live probes wave-1 LiveCommProbe and LiveArgvProbe on throwaway processes only)
recheck: on a procps-ng, kernel or man-pages release, or a change to `scripts/shokunin-watchdog.sh:1,380-382`

# Watchdog identity from a pid probe — what each observation can and cannot establish (FR5)

Scope: FR5 (`PROVINCE.md:48`, `corpus/README.md:338`). Detection and report only: no row advises starting, stopping,
signalling or locking anything. The lane census decides the fleet watchdog is alive when
`pgrep -af shokunin-watchdog | grep -E 'shokunin-watchdog' | grep -vF 'pgrep'` prints at least one line
(`tools/mori-census.sh:711-715`); it reads no `/proc/<pid>` file, start time or lock (wave-1 ScoutCensusWatchdog). The
watchdog is `scripts/shokunin-watchdog.sh` under the fleet root: shebang `#!/usr/bin/env bash` (`:1`), no pid file, and a
singleton `flock -n` on `.ufo/.watchdog.lock` (`:380-382`).

Each row: what a probe sees, what that does and does not establish (with the threshold), and the verdict a census
should give. `candidate` means consistent with the watchdog but not identity; `not-identity` means the observation
cannot separate the watchdog from another process; `unavailable` means the probe cannot answer; `absent` is scoped to
the query named in the row.

| observation | reading | verdict | sources |
|---|---|---|---|
| `pgrep -af shokunin-watchdog` (the census probe) prints a line | with `-f` the pattern is matched against the full command line, so any process whose command line mentions the name matches: a pager, an editor or an `exec -a` decoy was counted on this host (LiveArgvProbe (a)); the census counts lines, not processes | candidate | S161, S162 |
| the census filter `grep -vF pgrep` removes a line | pgrep will never report itself as a match (its own pid is skipped with `continue`), so the filter only removes other processes whose command line mentions pgrep; a watchdog started with such an argument was dropped on this host (LiveArgvProbe (b)) | false negative risk, not absence | S161, S162 |
| `pgrep shokunin-watchdog` (no `-f`) prints nothing and exits 1 | without `-f` the pattern is normally only matched against the process name, and procps warns that a pattern longer than 15 characters will result in zero matches; this miss says nothing about the watchdog (LiveCommProbe) | unavailable (probe blind) | S161, S162 |
| `/proc/<pid>/comm` of the running watchdog reads `bash` | exec sets the task name from the basename of the executed filename; a `#!/usr/bin/env bash` script runs env, which then executes bash by name, so the final name is the interpreter (LiveCommProbe: `bash` for the env shebang and for `bash <script>`); a process-name match can never find this watchdog | not-identity (name useless) | S164, S165 |
| `/proc/<pid>/comm` of a directly executed `#!/bin/bash` script with a long name reads its first 15 bytes (`shokunin-watchd`) | the name buffer is TASK_COMM_LEN, 16 bytes including the terminating null byte, and longer strings are silently truncated, so only a 15-byte prefix can ever be compared (LiveCommProbe) | not-identity (prefix only) | S163, S169 |
| a process's comm equals `shokunin-watchd` | any thread can set its own name with PR_SET_NAME from a caller-supplied value of up to 16 bytes including the terminating null byte; a forged python process matched `pgrep -x shokunin-watchd` on this host (LiveArgvProbe (c)) | not-identity | S169, S172 |
| `/proc/<pid>/cmdline` reads empty | the file holds the complete command line unless the process is a zombie, when a read will return 0 characters; an empty read gives no identity and is not by itself proof that the process exited | unavailable | S170 |
| `/proc/<pid>/cmdline` names `scripts/shokunin-watchdog.sh` | a `#!` exec splices the interpreter name into argv[0] and the script filename after it, and after execve a process that modifies its argv strings shows those changes here; a matching path is consistent with the watchdog, not proof of it | candidate | S165, S170 |
| `/proc/<pid>/stat` third value (state) is `Z` | the state letter follows the parenthesised task name, and `Z (zombie)` is the zombie state; [INFERENCE] a zombie has exited and is not yet reaped, so the pid is occupied while the watchdog loop is not running — no cited line carries this gloss (residual JudgeC1Rows: row 9 unsupported; marked here, not re-judged) | absent (exited, unreaped) | S167, S171 |
| `/proc/<pid>/stat` field 22 differs from the start time recorded for that pid | start_time is the time the process started after system boot, converted to clock ticks; a different value under the same pid is a different process (LiveArgvProbe (d): two runs of one command line, two start times) | not-identity (pid reused) | S167, S171 |
| a pid number recorded earlier is present again | PID allocation wraps back to a minimum value when the next pid reaches pid_max, so the same number is handed out again; a pid alone is never identity over time, only the pair pid plus start_time within one boot | not-identity | S173, S167 |
| `pgrep` exits 1 | exit 1 means no processes matched; with the census `-f` pattern that means no command line on this host named the watchdog at that sample, an absence scoped to that one query | absent (that query only) | S161 |
| `pgrep` exits 2 or 3, or the binary is missing | exit 2 is a syntax error and 3 a fatal error: neither says that no processes matched; the census already reports a missing binary as unavailable with liveness unknown (`tools/mori-census.sh:716-720`) | unavailable | S161 |
| `/proc/locks` holds a FLOCK WRITE line whose device and inode are those of `.ufo/.watchdog.lock` | the watchdog opens that file and takes its flock through the `flock` helper (`scripts/shokunin-watchdog.sh:380-382`); `/proc/locks` shows the lock class and the inode number of the locked file, but the PID of the process that owns the lock is the short-lived helper, not the watchdog, and a child that inherited the descriptor keeps the lock after the watchdog dies (round-31 residual CriticC1Tip reproduction) — read it without contending; a `flock -n` probe would contend and is never run | candidate (the watchdog or an orphaned child holds the lock) | S174 |

## Today on this host

- The fleet runs the `hyaku-inline` driver: `.ufo/watchdog.log` holds 208 `driver=hyaku-inline` lines against 3
  `driver=hyaku`, the lock file `.ufo/.watchdog.lock` is absent and no process holds it (wave-1 ScoutCensusWatchdog,
  2026-10-22). So the census's daemon-shaped probe reports `WATCHDOG_ABSENT` against a fleet whose rounds are live; under
  the table this is `absent (that query only)`, not a dead fleet. [INFERENCE] Fleet liveness under the inline driver is
  read from the launch/complete lines, not from a pid.

## Limits

- The `/proc/locks` row: the PID field names the `flock(1)` helper that took the lock and keeps showing it after the
  helper exits, and an orphaned child that inherited the descriptor (the tick `sleep`) keeps the lock alive after a
  SIGKILL of the watchdog (round-31 residual CriticC1Tip, a throwaway reproduction; the kernel side, `fs/locks.c`, was
  not opened as a source this round). So a lock line is a candidate, never `alive`, and its PID is not the watchdog.
  Round-31 correction: the first committed version (`5b728304`) gave this row `alive` and advised checking the PID.
- `/proc/locks` is filtered to the reader's PID namespace (S174 `proc_locks.5:105-116`); a reader in another namespace
  sees nothing, which is `unavailable`, not absence.
- Start times compare only within one boot; across boots pair them with the boot id (prior art in souji
  `process-residue-observations.md:46-48`, cited as adjacent, not as a mori source).
- A pidfd (S027) holds one task across pid reuse only while the descriptor is held; it does not identify the task.
- Name facts already in the lane: `knowledge/oom-victim-selection-r27.md:30` states the 15-byte comm limit from
  earlyoom's code; this entry sources it to the kernel (S163) and the man page (S169). `knowledge/audit-r11.md:201`
  names the argv-substring false-positive class (D06) that rows 1–2 measure.

## Not claimed

- No row changes the census probe; the census still counts `pgrep -af` lines (FR5 stays frontier).
- No row proves the watchdog loop is healthy or making progress; liveness of a pid is not progress.
- Nothing here starts, stops, signals or locks a process, or reads `/proc/<pid>/environ` (the driver's own lane-tag
  rule at `scripts/shokunin-watchdog.sh:231-236` is outside this entry under the privacy bound).
