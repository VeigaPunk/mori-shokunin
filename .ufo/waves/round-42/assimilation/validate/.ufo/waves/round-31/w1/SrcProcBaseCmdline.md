# S166 — Linux v7.2 `fs/proc/base.c` (cmdline, comm, exe) — scout report

Seat: `MoriR31.SrcProcBaseCmdline` (leaf, no subagents). Date: 2026-10-22. Assigned question:
does the pinned `fs/proc/base.c` carry what `/proc/<pid>/cmdline` returns for a task with no mm
and for a setproctitle-rewritten argument area, and what `/proc/<pid>/exe` and
`/proc/<pid>/comm` return — and should S166 be admitted?

**Decision: reject.** The exact URL is already carried by SOURCES rows S127
(`corpus/SOURCES.md:133`) and S148 (`corpus/SOURCES.md:154`). The bytes do carry the facts, so
the L1 can override; both the reject-shaped and admit-shaped rows are ready below. If the
reject stands, the C1 entry MUST NOT cite S166: `count-c1.py:128-136` requires exactly one
*admit* Gate row for every new id cited in the entry table.

## 1. Fetch receipt

- URL: `https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c`
- Command (same shell chain, so the timestamp follows the completed fetch):
  `curl -sSL --fail -m 60 -o S166.src -w 'http_code=%{http_code} size=%{size_download}\n' <url>`
  → `http_code=200 size=98196`
- Access time (`date -u +%FT%TZ`): `2026-10-22T23:43:05Z`
- Saved bytes: `/fast/scratch/hyaku/mori-r31/SrcProcBaseCmdline/S166.src` (unmodified curl output)
- `sha256sum S166.src`:
  `cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6`
- Size/lines: 98,196 bytes, 3990 lines; first line `// SPDX-License-Identifier: GPL-2.0`,
  last line `}` — a complete plain-text source file, not a challenge page.
- Duplicate check: `grep -c 'https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c' corpus/SOURCES.md`
  → `2` (lines 133 = S127, 154 = S148). `grep -o 'https\?://[^ ;|]*fs/proc/base\.c[^ ;|]*' corpus/SOURCES.md | sort | uniq -c`
  → `2` hits, both this raw URL; no git.kernel.org form of base.c is present.

## 2. Located evidence (verbatim, from the saved file)

Word counts are `wc -w` on the whitespace-normalized quote (verified: 7, 20, 17).

**Q1 — no mm ⇒ empty cmdline. `base.c:376-378` (7 words):**
`mm = get_task_mm(tsk); if (!mm) return 0;`
Fact: `get_task_cmdline()` returns 0, i.e. an empty read, whenever `get_task_mm()` yields NULL;
the surrounding function is `:370-383` and `proc_pid_cmdline_read()` (`:385-401`) only adds
`-ESRCH` when the task entry itself is gone (`:393-395`). `base.c:814` states the kernel's
no-mm states as `PF_KTHREAD or PF_EXITING`. A zombie (mm already dropped) is the same branch
[INFERENCE from :376-378 + :814; exit_mm is not in this file].

**Q2 — setproctitle can own the argv bytes. `base.c:323-324` (20 words):**
`* Magical special case: if the argv[] end byte is not * zero, the user has overwritten it with setproctitle(3).`
Fact: a nonzero byte at `arg_end-1` is read as the process having rewritten its argument area,
and the read is routed through `get_mm_proctitle()` (`:329-330`); `:305-307` adds that
setproctitle overwrite is allowed to overflow into the environment area, and `:309-311` extends
the readable window to `env_end`. Nonempty cmdline text is therefore not proof of the executed
command line.

**Q3 — exe resolves the task's exe_file or fails. `base.c:1766-1773` (17 words):**
`exe_file = get_task_exe_file(task); if (exe_file) { *exe_path = exe_file->f_path; path_get(&exe_file->f_path); fput(exe_file); return 0; } else return -ENOENT;`
Fact: `/proc/<pid>/exe` is a link to the task's `exe_file` path or `-ENOENT`; its caller
`call_proc_get_link()` returns `-EACCES` first when `ptrace_may_access(task,
PTRACE_MODE_READ_FSCREDS)` fails (`:1787-1788`), so an unprivileged probe of a root watchdog
may not read the target even when it exists.

**Empty cmdline has three code paths, not one.** Besides no-mm (Q1), `get_mm_cmdline()`
returns 0 when `!mm->env_end` (`:291-292`, comment `:290` "Check if process spawned far enough
to have cmdline") and when `arg_start >= arg_end` (`:301-302`). So an empty cmdline does not by
itself prove death or kernel-thread status; it only fails to identify a watchdog.

**comm is not established by this file.** `comm_show()` (`:1731-1746`) calls
`proc_task_name(m, p, false)` at `:1740`; `grep -n 'proc_task_name' S166.src` returns only that
one line, so the naming and truncation rules live outside base.c. The file does show the
registration modes: `comm` is `S_IRUGO|S_IWUSR` (`:3303`) and `cmdline` is `S_IRUGO`
(`:3307`, tid table `:3660`), so cmdline is world-readable and its read path (`:385-401`) has
no ptrace gate, unlike the exe link.

## 3. Gate row — reject (paste into `corpus/lessons/round-31.md` `## Gate`)

```markdown
| S166 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c | 2026-10-22T23:43:05Z | `cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6` | `base.c:376-378` (7 words): "mm = get_task_mm(tsk); if (!mm) return 0;"; `base.c:323-324` (20 words): "* Magical special case: if the argv[] end byte is not * zero, the user has overwritten it with setproctitle(3)."; `base.c:1766-1773` (17 words): "exe_file = get_task_exe_file(task); if (exe_file) { *exe_path = exe_file->f_path; path_get(&exe_file->f_path); fput(exe_file); return 0; } else return -ENOENT;" | reject, duplicate URL already carried by S127 (corpus/SOURCES.md:133) and S148 (corpus/SOURCES.md:154); round-30 precedent corpus/lessons/round-30.md:134 rejects a URL already shown inside a SOURCES row |
```

Reason: the ticket's reject rule ("the exact URL is already a row in `corpus/SOURCES.md`")
and the round-30 precedent both apply. The S127/S148 scopes cover only `/proc/<pid>/oom_score`
and `oom_score_adj` (`corpus/SOURCES.md:133,154`), so the cmdline/comm/exe code is unmined, but
the URL identity is already registered twice.

## 4. If the L1 overrides the duplicate finding — admit-shaped rows

Admit Gate row (same sha, access time and quotes; only the decision cell changes):

```markdown
| S166 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c | 2026-10-22T23:43:05Z | `cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6` | `base.c:376-378` (7 words): "mm = get_task_mm(tsk); if (!mm) return 0;"; `base.c:323-324` (20 words): "* Magical special case: if the argv[] end byte is not * zero, the user has overwritten it with setproctitle(3)."; `base.c:1766-1773` (17 words): "exe_file = get_task_exe_file(task); if (exe_file) { *exe_path = exe_file->f_path; path_get(&exe_file->f_path); fput(exe_file); return 0; } else return -ENOENT;" | admit, A, mined |
```

SOURCES row (column order copied from `corpus/SOURCES.md:5`):

```markdown
| S166 | Linux fs/proc/base.c at v7.2 — the /proc/<pid>/cmdline, comm and exe handlers — https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c | code | A | what fs/proc/base.c itself decides for /proc/<pid>/cmdline, /proc/<pid>/comm and /proc/<pid>/exe only: get_task_cmdline returns 0 when get_task_mm() gives NULL (no mm), get_mm_cmdline returns 0 when mm->env_end is zero or arg_start >= arg_end, a nonzero byte at arg_end-1 routes the read through get_mm_proctitle() so a setproctitle() rewrite is served and may extend to env_end, comm_show delegates to proc_task_name(m, p, false) which this file does not define, proc_exe_link returns the task's exe_file path or -ENOENT behind a ptrace_may_access(PTRACE_MODE_READ_FSCREDS) gate, and the registration modes are read-only for all (S_IRUGO) on cmdline and read-only for all plus owner-writable (S_IRUGO with S_IWUSR) on comm; not the proc_task_name naming or truncation rules, not get_task_exe_file's no-mm behavior, not the exported proc(5) wording, not exec-time argv construction | base.c:290-302 (empty returns), :323-330 (setproctitle branch), :370-383 (no-mm return), :1731-1746 (comm_show), :1766-1773 (proc_exe_link), :1787-1788 (ptrace gate), :3303 and :3307 (tgid modes), :3660 (tid cmdline); fetch 2026-10-22T23:43:05Z, HTTP 200, 98,196 B, sha256 cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6 | a pid probe cannot treat an empty /proc/<pid>/cmdline as proof of death (three zero-return paths), cannot treat nonempty cmdline as the executed argv (setproctitle can own the bytes), and cannot rely on /proc/<pid>/exe without ptrace access; comm is a separate task-name file, not the command line | mined | 2026-10-22 | on-release | corpus/knowledge/watchdog-identity-r31.md |
```

If admitted, the counter also needs a byte-identical copy at
`corpus/evidence/sources-r31/S166.src`; this seat may not write it (bounds). The verified
original is at the scratch path above with sha256
`cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6`.

## 5. Alternative URL if the duplicate must be cleared

The same blob at a URL not present in `corpus/SOURCES.md` would be
`https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/fs/proc/base.c?h=v7.2`
(the tree S127 already uses for oom.h/fork.c). It was **not fetched by this seat** ([INFERENCE]
it serves identical text; a fresh fetch, sha256 and quotes would have to be re-recorded before
any Gate row cites it).

## 6. Remaining unknowns / limits

- `proc_task_name()` is defined outside base.c; where exactly at v7.2 is not established here
  (`grep -n` finds only the call at `:1740`). The comm truncation/PR_SET_NAME contract comes
  from S169 and the kernel rows (S163-S165).
- `get_task_exe_file()`'s behavior for a task with no mm is not in base.c (definition outside);
  do not cite base.c for that.
- Source is tag v7.2; the host runs 7.2.11. No patch-level comparison was made (rows S127/S148
  use the same tag convention).
- No host `/proc` behavior was exercised and no process was signalled; detection and report only.
- No tool was installed or updated (no pacman/uv/npm transaction). No privacy-bearing value
  (pid, uid, unit/session id, journal text) was written.
- Bounds deviation, stated for the record: the fetch was capped with `curl -m 60` and every
  command was read-only and short, but this seat did not wrap each individual command in
  `timeout` as the wave bounds word it. No process tree is left running.
- No lane counter, git or jj write was run by this seat; the only lane write is this report.
