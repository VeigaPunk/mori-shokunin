# SrcProcArrayStat — S167 (Linux v7.2 fs/proc/array.c)

Seat: `MoriR31.SrcProcArrayStat`, leaf. Assigned: open candidate S167 for C1, locate the
`/proc/<pid>/stat` `start_time` field and the `State` field letters as identity and liveness
evidence, draft the Gate and SOURCES rows.

**Verdict: admit.** The bytes carry both facts; the URL is HTTP 200 and is not yet a row in
`corpus/SOURCES.md`.

## 1. Fetch record

- URL: `https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/array.c`
- Access (UTC, from `date -u +%FT%TZ` immediately before and after the single `curl`):
  `2026-10-22T23:43:06Z` — both stamps fell inside the same second; the 23 KB transfer
  completed between them.
- Command: `curl -sSL --fail -m 60 -o S167.src <url>`; the re-check header-only fetch returned
  `http=200 bytes=23110 type=text/plain; charset=utf-8`.
- Saved unchanged: `/fast/scratch/hyaku/mori-r31/SrcProcArrayStat/S167.src`
  — 23110 bytes, 822 lines, zero CR bytes (`file`: "C source, ASCII text"), line 1 is the
  `// SPDX-License-Identifier: GPL-2.0` header, so the body is the real file, not a challenge page.
- `sha256sum S167.src` = `a3eb1567e6125bd9c3136efacf1e6ee7526deb4212a895f3c3156d2410985828`
- Dedup check: `grep -n "fs/proc/array.c" corpus/SOURCES.md` → no output, rc=1 (not an existing row).

## 2. Located evidence

All quotes are copied from the saved file; every newline/tab inside a span is rendered as one
space in the transcription below, and the saved bytes are untouched.

**Q1 — `fs/proc/array.c:584-586` (15 words, `awk 'NR>=584&&NR<=586' … | wc -w`)**

```
/* apply timens offset for boottime and convert nsec -> ticks */ start_time = nsec_to_clock_t(timens_add_boottime_ns(task->start_boottime));
```

Fact it supports: `start_time` is `task->start_boottime` (a boot-referenced timestamp, adjusted
by the reader's time-namespace offset) converted from nanoseconds to clock ticks; it is a
boot-relative tick counter, not a wall-clock time, and it changes when a pid is reused.

**Q2 — `fs/proc/array.c:588-592` (15 words)**

```
seq_put_decimal_ull(m, "", pid_nr_ns(pid, ns)); seq_puts(m, " ("); proc_task_name(m, task, false); seq_puts(m, ") "); seq_putc(m, state);
```

Fact it supports: the stat line is written pid first, then `" (" + comm + ") "`, then the single state
letter, so the letter is the third whitespace-separated value of the line.

**Q3 — `fs/proc/array.c:136` (5 words)**

```
"Z (zombie)",		/* 0x20 */
```

Fact it supports: the state table has a distinct `Z` letter, so a stat line can belong to a task
that has exited but has not been reaped, while its pid is still reserved and readable.

**Q4 — `fs/proc/array.c:610-611` (8 words)**

```
seq_put_decimal_ull(m, " ", 0); seq_put_decimal_ull(m, " ", start_time);
```

Fact it supports: the `0` placeholder (itrealvalue) sits between `num_threads` and `start_time`,
which is why `start_time` is the twenty-second value rather than the twenty-first.

**Ordering derivation (from the file, not memory):** `fs/proc/array.c:588-611` holds 23
`seq_put*` emissions, and the comm field consumes three source lines (`:589-591`) for one value,
giving 22 whitespace-separated values; `state` is the 3rd and `start_time` the 22nd.
Host cross-check: `man 5 proc_pid_stat` line 153 reads `(22) starttime %llu` and lines 156-158
say the value is "expressed in clock ticks (divide by sysconf(_SC_CLK_TCK))". [INFERENCE] the
mapping of these positions to the proc(5) *names* `state`/`starttime` is the man page's, which
S171 owns; the positions themselves are visible in the emission order above.

**Presence is not execution (the C1-relevant reading):** `do_task_stat` takes
`task->signal->exec_update_lock` at `fs/proc/array.c:489` and reads `task->exit_code` at `:481`,
printing it at `:660`, with no liveness filter anywhere in the span `:466-668`. An exited task
that has not been reaped therefore still answers `/proc/<pid>/stat`. [INFERENCE] a pid probe that
finds the entry proves pid occupancy only; the `S`/`Z`/`t`/`T`/`P` letters distinguish runnable
from sleeping, zombie, stopped, tracing-stop and parked, but none of them proves the watchdog's
loop is executing.

**Identity caveat for the entry:** `start_time` is stable for a given boot-relative start and is
therefore a good PID-reuse discriminator, but it identifies the *task instance*, not the program:
`comm` is produced by `proc_task_name` at `:590` (truncated task-name rendering; rewrite and
length limits are S172/S169 territory, not visible here). `timens_add_boottime_ns` also means a
containerised reader can see an offset tick count relative to the host's own uptime.

## 3. Ready-to-paste Gate row

```
| S167 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/array.c | 2026-10-22T23:43:06Z | `a3eb1567e6125bd9c3136efacf1e6ee7526deb4212a895f3c3156d2410985828` | `fs/proc/array.c:584-586` (15 words): "/* apply timens offset for boottime and convert nsec -> ticks */ start_time = nsec_to_clock_t(timens_add_boottime_ns(task->start_boottime));"; `fs/proc/array.c:588-592` (15 words): "seq_put_decimal_ull(m, \"\", pid_nr_ns(pid, ns)); seq_puts(m, \" (\"); proc_task_name(m, task, false); seq_puts(m, \") \"); seq_putc(m, state);"; `fs/proc/array.c:136` (5 words): "\"Z (zombie)\", /* 0x20 */"; `fs/proc/array.c:610-611` (8 words): "seq_put_decimal_ull(m, \" \", 0); seq_put_decimal_ull(m, \" \", start_time);" | admit, A, mined |
```

## 4. Ready-to-paste SOURCES row

Column order copied from `corpus/SOURCES.md:5`.

```
| S167 | Linux fs/proc/array.c at v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/array.c | code | A | the producer of the /proc/<pid>/stat line: the state-letter table and the start_time computation and emission order | fs/proc/array.c:127-140,136,481,489,584-586,588-592,610-611; tag v7.2 | do_task_stat writes the state letter as the third and start_time as the twenty-second whitespace-separated value, the latter converted from task->start_boottime nanoseconds to boot-relative clock ticks; an exited-but-unreaped task still answers the file, so a pid entry proves presence, not execution. | mined | 2026-10-22 | on-release | corpus/knowledge/watchdog-identity-r31.md |
```

## 5. Decision and its checks

**Admit, A, mined.** Reject conditions from the assignment, checked one by one:

1. *Bytes do not carry the fact* — they do: Q1/Q4 at `:584-586,610-611` carry the tick
   conversion and the field position; Q2/Q3 at `:588-592,136` carry the state letter and its
   third-value position. All four spans were read back with `awk` and counted with `wc -w`.
2. *404 or challenge page* — no: `http=200 bytes=23110`, `text/plain; charset=utf-8`, SPDX
   header at line 1, 822 lines of C.
3. *Exact URL already a SOURCES row* — no: `grep -n "fs/proc/array.c" corpus/SOURCES.md` → rc=1.

## 6. Limits the L1 should carry into the entry

- **Path-to-code link is not in this file.** `array.c` defines `proc_tid_stat`/`proc_tgid_stat`
  at `:671-681` but registers no file name; its only ops table is
  `proc_tid_children_operations` at `:816`. The `"stat"` pathname mapping lives in
  `fs/proc/base.c` (S166). Pair S167 with S166 in the entry if the table cites the path, not just
  the line format. [INFERENCE] until S166 lands.
- **The tick rate is not in this file.** `nsec_to_clock_t` and `USER_HZ` come from headers; the
  host `man 5 proc_pid_stat` cross-check above is the only local statement of "clock ticks".
  S171 is the canonical id for that.
- **Why this still cannot settle liveness.** A `S`/`R` letter only samples the task at read time;
  `Z`, `t`, `T`, `P` are all non-executing yet hold the pid; and `start_time` proves only "same
  boot-relative start", so a probe that reads it twice cannot distinguish "still running" from
  "still not reaped". A liveness claim needs a second channel (a heartbeat the watchdog itself
  advances), which is outside this source.

## 7. Tooling and hygiene

- No installs or updates were needed; nothing was run through pacman, uv, npm or cargo.
- Every command was bounded (`curl -m 60`, `timeout 20 man`); no process was left running and
  none was signalled.
- No writes outside this report and `/fast/scratch/hyaku/mori-r31/SrcProcArrayStat/`; no git or
  jj write in the lane or fleet repo; no real pid, uid, unit name or session data recorded.
