# SrcExecComm — S164 (Linux v7.2 fs/exec.c) for C1

Seat: MoriR31.SrcExecComm. Question: where does exec set the task name (comm), and from what?
Verdict: **admit**. New id S164, kind code, tier A, status mined.

## 1. Provenance

| item | value |
|---|---|
| URL | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/exec.c |
| access (UTC, captured immediately before and after the fetch: 2026-10-22T23:43:07Z both times) | 2026-10-22T23:43:07Z |
| saved bytes (unchanged) | /fast/scratch/hyaku/mori-r31/SrcExecComm/S164.src |
| byte size | 51001 (stat -c %s) |
| lines | 2029 (`grep -c ''`) |
| sha256 | 44e4185bf9332d86a2fd6bbe33c22cdd0b5129521499b703058813d2106572c7 |
| first bytes | `// SPDX-License-Identifier: GPL-2.0-only` — source, not an HTML challenge page |
| fetch command | `curl -sSL --fail -m 60 -o S164.src <url>` (exit 0; `--fail` would have rejected a 404) |

## 2. Located facts and verbatim quotes

Exec-time name write site — `begin_new_exec()`, tags `fs/exec.c:1094-1104` and `1243-1257`:

- `fs/exec.c:1094`: `void __set_task_comm(struct task_struct *tsk, const char *buf, bool exec)` — the one writer of `tsk->comm` on the exec path (body 1094-1104).
- `fs/exec.c:1131`: `bprm->point_of_no_return = true;` and `fs/exec.c:1698`: `if (bprm->point_of_no_return || (retval != -ENOEXEC)) {` — with the comment at `fs/exec.c:1709` ("binfmt handlers will call back into begin_new_exec() on success."), this is the one-shot structure that makes the name write a single exec-time event, not a per-handler sequence.
- `fs/exec.c:1733-1734`: `bprm->file = bprm->interpreter;` / `bprm->interpreter = NULL;` — the script interpreter pass replaces only `bprm->file`; `bprm->filename` is assigned only in `alloc_bprm()` at `fs/exec.c:1444` and `1468` (single `grep -n 'bprm->filename ='` result set), so the name used at 1257 is still the path the caller passed.

Quotes (each verified present exactly once in the saved file with `grep -cF`; word counts from `wc -w`):

1. `fs/exec.c:1096` (7 words): `size_t len = strnlen(buf, sizeof(tsk->comm) - 1);`
   Fact for a pid probe: the exec-time name is silently truncated to the comm buffer size minus one byte, so a long watchdog path or script name is stored shortened and cannot be compared whole.
2. `fs/exec.c:1253` (1 word): `smp_load_acquire(&bprm->file->f_path.dentry->d_name.name)`
   Fact: in the dentry branch (`fs/exec.c:1243`, entered only when `bprm->comm_from_dentry` is set at `fs/exec.c:1448`, i.e. an empty filename via `execveat`) the name comes from the opened file's dentry name under RCU.
3. `fs/exec.c:1257` (3 words): `__set_task_comm(me, kbasename(bprm->filename), true);`
   Fact: in the ordinary branch the name is the basename of the file path handed to execve — no directory component and no argv, so a probe reading comm gets a bare file name only.

Host corroboration (observed, kernel 7.2.11-arch1-1; scratch only, no real pid recorded):

```
$ cat t-script.sh            # #!/bin/bash ; read -r c < /proc/self/comm ; echo "$c" > out.comm ; sleep 2
$ timeout 6 ./t-script.sh; echo "exit=$?"; cat out.comm
exit=0
t-script.sh
```

A directly executed `#!/bin/bash` script reports the **script basename** as comm, not `bash`. [INFERENCE] The mechanism is the one above: the interpreter pass swaps `bprm->file` while `bprm->filename` keeps the script path, and the one-shot `point_of_no_return` guard prevents a second name write; S165 (fs/binfmt_script.c) should confirm that `load_script()` sets `bprm->interp` only and never `bprm->filename`.

What this source cannot establish (boundary for the C1 decision table):

- Whether an arbitrary process may carry the watchdog's name: `comm` is writable later via PR_SET_NAME → S172.
- How `/proc/<pid>/comm` renders the buffer (length, newline): fs/proc → S166/S169.
- The buffer's real size `TASK_COMM_LEN`: include/linux/sched.h → S163.
- Whether pid 1 / a service unit re-execs or renames the script after start: not a kernel-source question.

## 3. Ready-to-paste rows

Gate row:

```
| S164 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/exec.c | 2026-10-22T23:43:07Z | `44e4185bf9332d86a2fd6bbe33c22cdd0b5129521499b703058813d2106572c7` | `fs/exec.c:1096` (7 words): "size_t len = strnlen(buf, sizeof(tsk->comm) - 1);"; `fs/exec.c:1253` (1 word): "smp_load_acquire(&bprm->file->f_path.dentry->d_name.name)"; `fs/exec.c:1257` (3 words): "__set_task_comm(me, kbasename(bprm->filename), true);" | admit, A, mined |
```

SOURCES row:

```
| S164 | Linux fs/exec.c at v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/exec.c | code | A | the single exec-time write of the task name in v7.2: the __set_task_comm body and its truncation, the two name branches (dentry name only for an empty exec filename, else the basename of bprm->filename), and the one-shot begin_new_exec guard that keeps a script's interpreter pass from rewriting the name; not the comm buffer size definition, not /proc rendering, not PR_SET_NAME | __set_task_comm:1094-1104 (strnlen:1096, memcpy:1099); name set site:1243-1257 (dentry branch:1243-1254, kbasename:1257); comm_from_dentry set:1448; point of no return:1131,1698 (handlers call back:1709); interpreter swap touches only bprm->file:1733-1734; tag v7.2; sha256 44e4185bf9332d86 | exec sets comm from the basename of the file path given to execve, truncated to the comm buffer size minus one byte, written once at the point of no return; a script keeps its own basename rather than the interpreter's, so comm carries no directory, no argv and no interpreter identity. | mined | 2026-10-22 | on-release | corpus/knowledge/watchdog-identity-r31.md |
```

## 4. Decision

**admit** — the saved bytes carry the assigned fact at the cited lines, all three quotes are byte-verified substrings of the saved file (`grep -cF` = 1 each, word counts 7/1/3), the URL is live source text (SPDX header, 51001 bytes, `--fail` did not trip), and neither the id nor the URL is present in `corpus/SOURCES.md` (`grep -c 'S164'` = 0, `grep -c 'fs/exec.c'` = 0).

L1 still owns: copy the bytes to `corpus/evidence/sources-r31/S164.src` and keep or drop the id.

## 5. Hygiene

- No tool installs or updates this seat (nothing was needed).
- No git/jj writes, no lane writes, no edits outside this report and /fast/scratch/hyaku/mori-r31/SrcExecComm/.
- Every command bounded (`timeout 6` probe, `-m 60` curl); probe process exited 0, `pgrep -af 't-script.sh'` = 0 leftovers.
- No uid, real pid, unit name, journal text or OMP setting is recorded here.
