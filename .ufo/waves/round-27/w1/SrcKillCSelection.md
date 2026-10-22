# C1 source — earlyoom 1.9.0 victim selection (kill.c)

Seat `MoriR27.SrcKillCSelection`. Read-only: no lane edits, no tool installs, no signals, no
`oom_score_adj` writes, no unit commands. Scratch: `/fast/scratch/hyaku/mori-r27/SrcKillCSelection/`.

Question answered: how earlyoom 1.9.0 chooses its victim, what it reads from `/proc/<pid>/`, which
processes it skips, and what happens when the victim exits before the kill.

## Gate block (assigned file)

- URL: `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c`
- Access: `curl -sS -o kill.c <URL>` → `http=200 bytes=21169`, 666 lines, fetched 2026-10-22T15:46:34Z
- sha256: `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3`
- Same bytes as the ones S118 already records (`corpus/SOURCES.md:124`), so this is an **anchor
  addition to S118, not a new row** (context rule: re-opening a file with an existing row adds an
  anchor).

Verbatim quotes (each ≤ 25 words):

| # | lines | quote | words |
|---|---|---|---|
| Q1 | kill.c:467-468 | `// Skip processes with oom_score_adj = -1000, like the` / `// kernel oom killer would.` | 14 |
| Q2 | kill.c:437 | `if (cur->VmRSSkiB == victim->VmRSSkiB && cur->oom_score <= victim->oom_score) {` | 9 |
| Q3 | kill.c:462 | `if (cur->oom_score == victim->oom_score && cur->VmRSSkiB <= victim->VmRSSkiB) {` | 9 |
| Q4 | kill.c:424 | `if (args->ignore_regex && regexec(args->ignore_regex, cur->name, (size_t)0, NULL, 0) == 0) {` | 11 |
| Q5 | kill.c:653-654 | `if (res != 0) {` / `warn("kill failed: %s\n", strerror(saved_errno));` | 9 |

## What the file says (observed)

**Entry point.** `find_largest_process` (kill.c:527) opens `procdir_path` = `/proc`
(globals.c:5), walks every numeric dirent once (kill.c:551-578, `isnumeric` skip at :562), and keeps
the current best via `is_larger` (kill.c:355) — one linear pass, no sort, lazy field fill
(kill.c:351-354).

**Skips, in evaluation order** (all inside `is_larger`):

1. `cur->pid <= 2` → false (kill.c:357-359, comment "Let's not kill init or kthreadd").
2. `--ignore-root-user` and uid 0 → false (kill.c:363-374; uid via `stat()` of `/proc/<pid>`).
3. `/proc/<pid>/stat` unreadable → false (kill.c:377-381).
4. `cur->stat.ppid == 2` → false (kill.c:391-393; kernel-thread test by ppid, borrowed from
   procps).
5. `oom_score` unreadable → false (kill.c:396-401).
6. `--ignore` regex matches `comm` → false (kill.c:424-426).
7. After the comparison: `oom_score_adj == -1000` → false (kill.c:467-478). Note the position: the
   -1000 process is *not* excluded early; it loses only after it would otherwise have beaten the
   incumbent, so the outcome is the same and the read cost is the same as a normal candidate.

`--prefer`/`--avoid`/`--ignore` are matched with `regexec` against `cur->name`, which is
`/proc/<pid>/comm` (kill.c:405, :410, :417, :424) — **never against `cmdline`**. Magnitudes:
`OOM_SCORE_PREFER 300` / `OOM_SCORE_AVOID -300` (kill.c:24-27) added to `oom_score`, or
`VMRSS_PREFER 3145728` / `VMRSS_AVOID -3145728` KiB (kill.c:29-32) added to `VmRSSkiB` when
`--sort-by-rss` is set (kill.c:411-421). The five kill-selection flags (`--prefer`, `--avoid`,
`--ignore`, `--ignore-root-user`, `--sort-by-rss`) are parsed in main.c:181-186 and the three
regexes compiled with `regcomp(..., REG_EXTENDED | REG_NOSUB)` (main.c:376, :383, :390): flag and
regex handling live in main.c, outside this row's file.

**Comparison.** Default (`--sort-by-rss` false): larger `oom_score` wins; on an exact tie the larger
`VmRSSkiB` wins (kill.c:457-465, Q3). With `--sort-by-rss`: larger `VmRSSkiB` wins, `oom_score`
breaks the tie (kill.c:430-440, Q2); if either side has `rss == 0` ("zombie main thread") the
comparison falls back to `oom_score` and warns for that candidate (kill.c:441-455, warning at
:443-448). So `--sort-by-rss` does not discard `oom_score`. `VmRSSkiB` comes from
`/proc/<pid>/stat` field `rss` × page size / 1024
(kill.c:377-383), **not** from `statm`: the string `statm` has 0 hits in kill.c, meminfo.c,
proc_pid.c, main.c, kill.h, globals.c (`grep -rn statm` over the fetched set, empty).

**What it reads from `/proc/<pid>/`** (helpers resolve to meminfo.c for the `/proc` readers, and to
proc_pid.c for `stat`):

| path | reader | what it yields | used for |
|---|---|---|---|
| `/proc/<pid>/stat` | proc_pid.c:46-75 (parse at :26-38) | `state`, `ppid`, `num_threads`, `rss` | ppid==2 skip, `VmRSSkiB`, `is_alive` zombie test (meminfo.c:138-148) |
| `/proc/<pid>/oom_score` | meminfo.c:175-183 | integer ≥ 0 | primary key (default) |
| `/proc/<pid>/oom_score_adj` | meminfo.c:191-194 | integer, may be negative | -1000 skip; log field |
| `/proc/<pid>/comm` | meminfo.c:199-224 | name, truncated to 16 bytes (:196) | prefer/avoid/ignore match; log field |
| `/proc/<pid>/cmdline` | meminfo.c:230-256 | NULs replaced by spaces | log line only, via `fill_informative_fields` (kill.c:483-506) |
| `/proc/<pid>` (stat) | meminfo.c:260-270 | directory owner uid | `--ignore-root-user` only |

No `/proc/<pid>/statm` and no `/proc/<pid>/status` read on this path.

**Self.** earlyoom does not skip itself during the scan; after the pass it checks
`victim.pid == getpid()` and zeroes the struct (kill.c:587-592), so the next stage sees pid 0 and
only sleeps (kill.c:608-615). The upstream unit template sets `OOMScoreAdjust=-100`, not -1000
(S120 `earlyoom.service.in:14`), so absent a packaging override earlyoom stays a normal candidate
to its own scan.

**Victim exits before the kill — three distinct cases:**

1. Vanishes during the scan: `fopen` of `/proc/<pid>/stat` fails → `is_larger` returns false
   (kill.c:377-381; proc_pid.c:56-58, comment "Process is gone - good").
2. Vanishes between selection and the signal: `pidfd_open` fails, warned, kill proceeds
   (kill.c:285-290); `kill()` fails with ESRCH → `kill_release` returns non-zero and skips
   `process_mrelease` (kill.c:240-253) → `kill_wait` returns non-zero → `kill_process` prints one
   `kill failed:` line with `strerror(errno)` and an error notification if enabled (kill.c:653-657,
   Q5). The 1-second sleep is gated on `EPERM` only (kill.c:661-664).
3. No re-selection and no retry inside that iteration: the poll loop re-reads meminfo after
   selecting (main.c:535-540) but never re-checks victim liveness; the next attempt is the next loop
   pass (main.c:514-539).

## Inference and limits

- [INFERENCE] `/proc/<pid>/stat`'s `rss` field counts resident pages, so swapped-out pages are not
  in `VmRSSkiB`; the code shows the arithmetic, not the kernel semantics. No proc(5) or kernel page
  was opened by this seat.
- [INFERENCE] Because matching is on a 16-byte `comm`, an operator's `--prefer`/`--avoid`/`--ignore`
  expression that names something only present in a command line cannot match. Stated as a
  consequence of kill.c:405-426 + meminfo.c:196; no configured host expression was read or copied.
- Not verified here: whether this host's `EARLYOOM_ARGS` actually sets `--sort-by-rss` or any of the
  three regexes (privacy: presence-only, other seats); the fleet's per-process `oom_score_adj`
  (other seats); the kernel's own selection (S003, other seats).

## Ready-to-paste: S118 (`corpus/SOURCES.md:124`)

S118 already owns kill.c, so no new row. Four cell edits, status stays `mined`, `opened 2026-10-22`
and `recheck on-release` unchanged.

**(1) anchor cell — replace the cell with this (unchanged text plus new anchors; long line, keep
as one cell):**

```text
kill.c:24-32,272,282,318,329,338,609,617-627,654; msg.c:14,66-73,75-82,99-107; msg.h:10; tag v1.9.0 = commit 202d4db0d308ca6478f68de68b46cae34896ddaf; kill.c 21,169 B sha256 b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3; msg.c 6,864 B sha256 a771c91529053341c290ede2a7df1d9fdf16e07fb9584db8a64604a45dea5197; victim-selection anchors added 2026-10-22 on re-open, kill.c sha256 unchanged: kill.c:351-361 (is_larger contract, pid <= 2), :363-374 (--ignore-root-user uid 0), :377-383 (stat rss -> VmRSSkiB), :391-393 (ppid == 2), :396-401 (oom_score read), :404-427 (comm target for prefer/avoid/ignore), :429-455 (--sort-by-rss primary, oom_score tie-break, rss=0 fallback), :457-465 (oom_score primary), :467-478 (oom_score_adj -1000 after the comparison), :525-527 (find_largest_process), :551-578 (one linear /proc pass), :587-592 (self-selection guard), :606-615 (no victim -> sleep 1 s), :240-253,:285-290,:640-641,:649-654 (kill_release, pidfd, "kill failed" on a vanished victim); opened 2026-10-22
```

**(2) scope cell — append after "whether warn() reaches stderr or syslog" and replace the
"not the poll-loop decision logic" exclusion:**

```text
; the same file's victim-selection algorithm (is_larger, find_largest_process): the
oom_score-versus-VmRSS comparison and its --sort-by-rss branch, the prefer/avoid/ignore regexes
matched against comm, the pid <= 2, ppid == 2, uid 0 and oom_score_adj = -1000 skips, and the
self-selection guard; not the main.c poll-loop act rule, not the meminfo threshold parsing, not
this host's unit configuration
```

**(3) teaches cell — append before the status column:**

```text
The victim is the largest oom_score, with a larger-VmRSS tie-break, unless --sort-by-rss makes
VmRSS primary (oom_score still breaks ties and decides rss=0 processes); prefer/avoid shift the
score by +-300 or the RSS by +-3 GiB and ignore drops the process, all matched against comm and
never the command line; pid 1, pid 2, children of kthreadd and oom_score_adj = -1000 processes are
never chosen; a victim that exits first yields one "kill failed" line, no retry until the next poll.
```

**(4) used-by cell — append:**

```text
, corpus/knowledge/oom-victim-selection-r27.md
```

S118 is S118 (< 127), so this anchor does **not** count toward C1's "≥ 3 rows numbered S127+" — the
entry must cite other seats' new rows for that. It is the grounding for the entry's "how earlyoom
picks a victim" and "what it reads" paragraphs.

## Companion file findings (outside the assigned file, for the L1 to route)

1. **`proc_pid.c` / `proc_pid.h` have no SOURCES row.** They hold the `/proc/<pid>/stat` reader
   (`proc_pid.c:26-38`), which kill.c depends on for `rss` and `ppid`. If the entry asserts "reads
   stat, not statm", a row is needed. Candidate row:
   `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/proc_pid.c` (2,682 B, sha256
   `e5b654466cd92fb49cc1dcd905922dab56a1d156f10f4108d8af262a70b212d5`) and
   `.../proc_pid.h` (312 B, sha256
   `b8adf99fc88d61cd31ca9bdb2f1d4ad906e57374d2bae16dda94ef84243dcd90`), anchors `proc_pid.c:15-18`
   (`strrchr(')')` name rule), `:26-38` (sscanf walk to `ppid`, `num_threads`, `rss`), `:39-41`
   (all-or-nothing `ret != 4`), `:51` (512-byte buffer), `:54-58` (open failure = "Process is gone"),
   `proc_pid.h:7-12` (`pid_stat_t`).
2. **`meminfo.c` has row S116, but S116's scope excludes the proc readers** it now needs
   (`get_oom_score` :175-183, `get_oom_score_adj` :191-194, `get_comm` :199-224 with the 16-byte
   truncation at :196, `get_cmdline` :230-256, `get_uid` :260-270, `is_alive` :125-149,
   `read_proc_file_integer` :156-170). Same file → anchor to S116 plus a scope clause, not a new
   row. This seat did not edit S116; the L1 decides.
3. **`main.c` re-check after selection** (main.c:535-540) and **regex compilation** (main.c:376,
   :383, :390) belong to S119's file; if the entry asserts either, add those lines to S119.

## Status

Observed: kill.c algorithm, ordering, skip list, `/proc` read set, vanished-victim path, no `statm`.
Inference: two items above. Unresolved by this seat: the host's configured earlyoom options and the
fleet's `oom_score_adj` (other seats); kernel-side selection (S003, other seats). No tool was
installed or upgraded this run.
