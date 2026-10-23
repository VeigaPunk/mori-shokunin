# S163 — Linux include/linux/sched.h at v7.2

Seat: MoriR31.SrcSchedCommLen (leaf, no subagents). Lane: /home/vgpnk/Projects/shokunin/mori-shokunin.
Question: does the file carry TASK_COMM_LEN and the `comm` field, and what does it say about the task name being at most 15 bytes plus NUL.

## 1. Fetch facts (observed)

| item | value |
|---|---|
| URL | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/sched.h |
| access time (UTC, `date -u +%FT%TZ` immediately before curl) | 2026-10-22T23:43:05Z |
| bytes | 73653 |
| sha256 of saved full bytes | `a31c63e692cb8ab036d01c0092fcdf4dfb75ec1f17dfda9056b12abecdb3dedf` |
| saved copy | /fast/scratch/hyaku/mori-r31/SrcSchedCommLen/S163.src |
| line count | 2519 (`grep -c "" S163.src`) |
| content check | `file` says C source, ASCII; first line `/* SPDX-License-Identifier: GPL-2.0 */`, last line `#endif` — real file, not a 404 or challenge page; curl rc=0 under `-sSL --fail -m 60` |

Command actually run (scratch dir):

```
T=$(date -u +%FT%TZ); curl -sSL --fail -m 60 -o S163.src \
  https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/sched.h
echo "access_time=$T rc=$?"; sha256sum S163.src; wc -c S163.src; grep -c "" S163.src
# access_time=2026-10-22T23:43:05Z rc=0
# a31c63e692cb8ab036d01c0092fcdf4dfb75ec1f17dfda9056b12abecdb3dedf  S163.src
# 73653 S163.src / 2519
```

## 2. Located lines (observed; grep -n on the saved copy)

```
325:	TASK_COMM_LEN = 16,
1181:	char				comm[TASK_COMM_LEN];
2018:extern void __set_task_comm(struct task_struct *tsk, const char *from, bool exec);
2020:	BUILD_BUG_ON(sizeof(from) != TASK_COMM_LEN);	\
2038:	BUILD_BUG_ON(sizeof(buf) < TASK_COMM_LEN);	\
```

Comment block immediately above the field, lines 1174-1180:

```
1174	/*
1175	 * executable name, excluding path.
1176	 *
1177	 * - normally initialized by begin_new_exec()
1178	 * - set it with set_task_comm() to ensure it is always
1179	 *   NUL-terminated and zero-padded
1180	 */
```

### Quotes (verbatim spans, `wc -w` counted on the exact strings)

1. `include/linux/sched.h:325` (3 words): "TASK_COMM_LEN = 16,"
   Fact for the watchdog question: the task command buffer is 16 bytes in total, so the name itself has room for at most 15 bytes once the terminator is counted.
2. `include/linux/sched.h:1181` (2 words): "char comm[TASK_COMM_LEN];"
   Fact: `comm` is a fixed 16-byte character array inside `task_struct` — not a pointer to arbitrary-length argv or script text, so whatever a probe reads as the name cannot be longer than that array.
3. `include/linux/sched.h:1177-1179` (19 words): "normally initialized by begin_new_exec() * - set it with set_task_comm() to ensure it is always * NUL-terminated and zero-padded"
   Fact: the field is set at exec and is guaranteed NUL-terminated and zero-padded, which is what turns the 16-byte array into a name capped at 15 stored bytes; a longer name cannot be stored in full.

Whitespace note: the counter (`count-c1.py:42,155-156`) compares `norm(quote)` against `norm(copy bytes)`, so line spans are written with single spaces and the per-line `\t * ` prefix is stripped; every quoted token sequence is present in the saved file (verified with that same `norm` in a scratch python run: present=True for all three, word counts 3/2/19).

### The 15-byte statement is arithmetic, not a quoted sentence

No line in this file writes "15" or "TASK_COMM_LEN - 1". The cap follows from `TASK_COMM_LEN = 16` (line 325) plus "NUL-terminated and zero-padded" (line 1179) plus the array declaration (line 1181) — [INFERENCE], and the truncation itself happens in `__set_task_comm()`/`strscpy_pad()`, declared at 2018-2021 and 2037-2041, whose definition lives in fs/exec.c (outside this file; S164's ground). This file also says the buffer is the "executable name, excluding path" (line 1175), so a probe matching a full script name or a command line against `comm` is asking the field for text it is not allowed to hold — [INFERENCE] for any specific host script name; the field-size limit is the observed part.

Writer-side constraint worth carrying into the entry: `set_task_comm()` refuses any source buffer not exactly TASK_COMM_LEN bytes (line 2020) and `get_task_comm()` requires a destination of at least TASK_COMM_LEN (line 2038), so readers always copy a padded 16-byte buffer.

## 3. Ready-to-paste rows

Gate row (one line, `corpus/lessons/round-31.md`):

```
| S163 | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/sched.h | 2026-10-22T23:43:05Z | `a31c63e692cb8ab036d01c0092fcdf4dfb75ec1f17dfda9056b12abecdb3dedf` | `sched.h:325` (3 words): "TASK_COMM_LEN = 16,"; `sched.h:1181` (2 words): "char comm[TASK_COMM_LEN];"; `sched.h:1177-1179` (19 words): "normally initialized by begin_new_exec() * - set it with set_task_comm() to ensure it is always * NUL-terminated and zero-padded" | admit, A, mined |
```

SOURCES row (one line, `corpus/SOURCES.md`, column order copied from line 5):

```
| S163 | Linux include/linux/sched.h at v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/sched.h | code | A | task command name buffer and the task_struct comm field in v7.2 only: TASK_COMM_LEN, the comm array, the comment that comm is the executable name kept NUL-terminated and zero-padded, and the set/get helper buffer-size assertions; not the /proc rendering of the name and not any host observation | sched.h:321-325; comm field:1181; comm comment:1174-1180; set_task_comm:2018-2022; get_task_comm:2037-2041; tag v7.2; sha256 a31c63e692cb8ab0 | comm is a 16-byte NUL-terminated executable name, so at most 15 bytes of name can be stored and a probe comparing comm to a longer script name or to argv text cannot match. | mined | 2026-10-22 | on-release | corpus/knowledge/watchdog-identity-r31.md |
```

Both lines use no double quote inside a quote and no unescaped pipe; the sha is the sha256 of the saved 73653 bytes.

## 4. Decision

**admit** — A, code, mined.

Reasons, each observed:

- URL resolves with HTTP success under `curl --fail` (rc=0); body begins with the SPDX line and ends with `#endif`, 2519 lines, so not a 404 body and not a challenge page.
- The bytes carry the fact: `TASK_COMM_LEN = 16` at 325, `char comm[TASK_COMM_LEN];` at 1181, and the NUL-termination/zero-padding comment at 1177-1179. Every quote above was found in the saved file, none typed from memory.
- The exact URL is not already a SOURCES row: `grep -n "v7.2/include/linux/sched.h" corpus/SOURCES.md` exits 1 (no output), and `grep -n "include/linux/sched.h" corpus/SOURCES.md` also exits 1. Existing Linux A rows at v7.2 (S003, S077-S092) cover other paths; none is this header.
- `corpus/lessons/round-31.md` does not exist yet at my check time (`grep` exit 2, "No such file or directory"), so the Gate row cannot collide with an earlier S163 row; `corpus/SOURCES.md` has no `| S163 |` row (grep exit 1).
- The drafted rows parse under the counter's own helpers: 6 gate cells with the last one starting `admit`, an https URL, a 64-hex sha inside backticks equal to the saved-file sha256, 3 quotes of 3/2/19 words all normalized-present in the saved bytes; the SOURCES row is 11 cells in the line-5 order with status mined, opened 2026-10-22, recheck on-release.
- No tool installs were needed for this seat (curl and coreutils only), so there is nothing to record under the tooling directive.
- The sha256 is stable for this tag path: the copy under `corpus/evidence/sources-r31/S163.src` must be this exact byte stream; the C1 counter re-fetches the URL at measurement time and compares (`count-c1.py:159`), so a silent upstream retag would show as `fetch=bad` rather than a stale quote.

## 5. Remaining unknowns (for the L1 and the neighbours)

- How the name is rendered to user space (`/proc/<pid>/comm`, `/proc/<pid>/stat` field 2, `/proc/<pid>/status` Name) is not this file's ground; that belongs to S166/S167/S168/S169/S171 seats.
- Whether `pgrep`/`ps` compare full names or truncated ones is S161/S162 ground; this file only fixes the 15-byte cap and the fact that the stored text is the executable name, not the script path or argv.
- No host observation was taken: the lane host is linux 7.2.11 and procps-ng 4.0.7-1, while this source is tag v7.2; the entry should keep kernel-source claims separate from host probes.
