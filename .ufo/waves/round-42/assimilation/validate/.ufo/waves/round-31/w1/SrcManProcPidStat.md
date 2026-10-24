# S171 — proc_pid_stat(5) at man-pages 6.20 (C1, seat MoriR31.SrcManProcPidStat)

Question: does /proc/<pid>/stat, as documented, support a decision about whether a pid is
the alive fleet watchdog — and where does it stop short?

## 1. Fetch facts

| item | value |
|---|---|
| URL | https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man5/proc_pid_stat.5?h=man-pages-6.20 |
| command | `curl -sSL --fail -m 60 -o S171.src "<url>"` |
| access time (UTC, `date -u +%FT%TZ` before/after) | 2026-10-22T23:43:07Z / 2026-10-22T23:43:08Z |
| saved bytes | `/fast/scratch/hyaku/mori-r31/SrcManProcPidStat/S171.src`, 11350 bytes, 392 lines |
| sha256 | `cba82e47c8c7917ec4f7c24d9c8779c53ecf478fdefe5c7835690989bb060bcd` |
| second fetch, same URL | identical sha256 (`curl … \| sha256sum` → `cba82e47…060bcd  -`) |
| content check | `file` = "troff or preprocessor input, ASCII text"; header `.TH proc_pid_stat 5 (date) "Linux man-pages (unreleased)"` at :7; no `MANIFEST` string, no challenge or error page; body ends at :392 `.BR proc_pid_status (5)` |
| ref check | `refs/tags` lists `man-pages-6.20` as a tag, so `?h=man-pages-6.20` is tag-pinned [INFERENCE: cgit resolves the tag; the `.TH` date/version strings are dist-time placeholders, visible literally as `(date)` and `(unreleased)`] |

No tool was installed or updated for this seat (curl, sha256sum, grep from the host).

## 2. Located verbatim quotes (all re-checked as whitespace-normalised substrings of the saved file; word counts by `wc -w` and by `split()`)

**Q1 — `man5/proc_pid_stat.5:43` (8 words):** `One of the following characters, indicating process state:`
- Field header is `:42` `.RI (3)\~ state \~%c`; shell letters follow at :46 R, :49 S, :52 D, :56 Z, :59 T, :69 X, :96 I.
- Fact it supports: field 3 of the record is a single state character with a documented letter set, so a probe parses position 3 and classifies liveness from one letter — a `Z` (:57 `Zombie`) entry is never a running watchdog, while the idle daemon's normal `S` (:50 `Sleeping in an interruptible wait`) proves nothing beyond the process still having a task.

**Q2 — `man5/proc_pid_stat.5:228-229` (17 words):** `The time the process started after system boot. Before Linux 2.6, this value was expressed in jiffies.`
- Fact it supports: field 22 starttime (:227 `.RI (22)\~ starttime \~%llu`) is a boot-relative start time, not a wall-clock stamp, so a probe can only compare it against boot time or a previous sample — two samples with different starttime mean a restart or pid reuse, and a raw equality across reboots is meaningless.
- Unit sentence is `:230` "Since Linux 2.6, the value is expressed in clock ticks (divide by" continued at `:231` `.IR sysconf(_SC_CLK_TCK) ).`; the divisor is host `CLK_TCK`, not a constant.

**Q3 — `man5/proc_pid_stat.5:39` (10 words):** `(16) characters (including the terminating null byte) are silently truncated.`
- Subject is `:36` `The filename of the executable, in parentheses.` with `:37-38` naming `TASK_COMM_LEN`.
- Fact it supports: comm is at most 15 visible characters, so `shokunin-watchdog.sh` (21 characters) cannot appear whole in field 2 — a stat-only probe matches at most a truncated prefix and cannot prove the script name, let alone the path.

Two more located lines matter for the same decision but are not needed as quotes: `:16-17` places the field list in `fs/proc/array.c`, and `:22-28` says fields marked `[PT]` read 0 when the ptrace access check denies it (15 `[PT]` marks in the page, none on `:227` starttime).

## 3. Ready-to-paste rows

Gate row (`corpus/lessons/round-31.md`):

```
| S171 | https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man5/proc_pid_stat.5?h=man-pages-6.20 | 2026-10-22T23:43:07Z | `cba82e47c8c7917ec4f7c24d9c8779c53ecf478fdefe5c7835690989bb060bcd` | `man5/proc_pid_stat.5:43` (8 words): "One of the following characters, indicating process state:"; `man5/proc_pid_stat.5:228-229` (17 words): "The time the process started after system boot. Before Linux 2.6, this value was expressed in jiffies."; `man5/proc_pid_stat.5:39` (10 words): "(16) characters (including the terminating null byte) are silently truncated." | admit, A, mined |
```

SOURCES row (`corpus/SOURCES.md`):

```
| S171 | proc_pid_stat(5) at man-pages 6.20 — https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man5/proc_pid_stat.5?h=man-pages-6.20 | docs | A | the /proc/pid/stat field list in the man-pages 6.20 source tree: positional fields, field 3 state letters (S at :49-50, Z at :56-57, X at :69-70), field 22 starttime as clock ticks since boot (:227-233) and comm truncated at TASK_COMM_LEN (:35-39), read as man-page source whose `.TH` date and version are dist-time placeholders (:7) | man5/proc_pid_stat.5:35-39,42-43,49-50,56-57,69-70,227-233; tag man-pages-6.20 | /proc/<pid>/stat carries field 3 state and field 22 starttime in clock ticks since boot, so a pid probe can test liveness and detect a restart or pid reuse, but comm is the executable filename truncated to 16 bytes including NUL and cannot carry a 21-character script name | mined | 2026-10-22 | on-release | corpus/knowledge/watchdog-identity-r31.md |
```

Optional extra Gate quote group, if the L1 wants the tick unit quoted inside the row — append
before the decision cell:
`man5/proc_pid_stat.5:230` (10 words): "Since Linux 2.6, the value is expressed in clock ticks"
(verified verbatim, 10 words; the divisor continues with a troff macro on :231, which is why the
group stops there).

Upstream copy for the L1 (this seat may not write in the lane):

```
mkdir -p corpus/evidence/sources-r31 && cp /fast/scratch/hyaku/mori-r31/SrcManProcPidStat/S171.src corpus/evidence/sources-r31/S171.src && sha256sum corpus/evidence/sources-r31/S171.src
```

## 4. Decision: admit, A, mined

Checks run:
- URL returns 200 with a real troff man page (11350 bytes, ends with SEE ALSO) — not a 404 and
  not a challenge page; second fetch hashes identically, so the C1 measurement-time re-fetch is
  stable.
- Exact URL is **not** already a row: `grep -nF "proc_pid_stat.5?h=man-pages-6.20" corpus/SOURCES.md`
  → exit 1; `grep -c "proc_pid_stat" corpus/SOURCES.md` → 0. S149 cites man7.org 6.19 renders of
  oom_score_adj(5)/oom_score(5), a different URL and page set.
- Every quote re-checked against the saved bytes with the counter's own normalisation
  (`' '.join(text.split())` substring test): all three found; declared word counts equal both
  `wc -w` and `len(q.split())`; all ≤25.
- Gate row shape re-checked against `count-c1.py:141-161`: row starts `| S171 |`, first `https://`
  cell is the URL, one backticked 64-hex sha, quotes match
  `\(\s*\d+\s+words?\s*\):\s*"…"`, last cell starts `admit`, `S171` appears exactly once in the
  SOURCES row (`count-c1.py:136-139` counts duplicate rows).

## 5. Remaining unknowns (for the entry, not for this Gate row)

1. The page never states that the record is a single line, nor that comm may contain spaces or
   parentheses beyond being wrapped in them; the newline/paren-aware parse rule has to come from
   `fs/proc/array.c` (S167, another seat). [INFERENCE] today's probes that split on spaces break on
   a comm containing a space, and this page neither warns nor confirms it.
2. `CLK_TCK` is host state, not documented here: converting starttime to seconds needs
   `getconf CLK_TCK` on the measured host (100 on x86_64 hosts of this class — not asserted by
   these bytes). A row that converts ticks to seconds without recording the divisor is not backed
   by S171.
3. `.TH` reads `(date)` / `(unreleased)`; if the L1 wants the row to say the page *renders* as
   6.20, that needs the release tarball (S146) — not checked here, marked [INFERENCE].

Counters: this row alone moves `count-c1.py` no closer to met; it supplies 1 of the 4+ new ids and
one admit Gate row. `count-c1.py` also needs `corpus/lessons/round-31.md` to exist
(it is absent at write time) and the copy above.
