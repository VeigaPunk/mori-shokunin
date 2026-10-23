# S169 — man-pages 6.20 proc_pid_comm(5): Gate and SOURCES draft

Seat: MoriR31.SrcManProcPidComm (wave 1, C1 depth). Scope: open candidate source S169 only,
draft its Gate row and SOURCES row, decide admit/reject. No lane commits, no edits outside
this report file and the seat scratch dir.

## 1. Source identity

| field | value |
|---|---|
| URL | https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man5/proc_pid_comm.5?h=man-pages-6.20 |
| access (UTC, `date -u +%FT%TZ` at fetch) | 2026-10-22T23:43:06Z |
| HTTP status / bytes downloaded | `HTTP:200 SIZE:1347` (curl `-w`) |
| byte size on disk | 1347 (`wc -c`), 49 lines (`wc -l`) |
| sha256 of full bytes | `31aee9e50c23579e7983e26edee83bee9ab7a8ba4c7be46027db2cac5ee23c08` |
| saved copy | /fast/scratch/hyaku/mori-r31/SrcManProcPidComm/S169.src (unchanged; re-hashed identical after the grep pass) |
| file type | `S169.src: troff or preprocessor input, ASCII text` — genuine troff man source, not an HTML/JS challenge page (content opens with `.\" Copyright 1994-1995, Daniel Quinlan` and `.TH` at line 7) |

Command shape used (bounds-compliant: `timeout`, bounded fetch):

```
ACCESS=$(date -u +%FT%TZ)
timeout 90 curl -sSL --fail -m 60 -o S169.src -w 'HTTP:%{http_code} SIZE:%{size_download}\n' \
  'https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man5/proc_pid_comm.5?h=man-pages-6.20'
```

## 2. Located verbatim quotes

All three quotes were extracted from the saved file by line range (`awk 'NR>=a&&NR<=b' S169.src`),
then the troff line breaks were joined with single spaces (the lane's established convention for
multi-line anchors, see corpus/lessons/round-30.md:116 `unit.c:2773-2774`). Word counts are
`wc -w` on the joined span. Positive presence checks in the saved file:
`grep -n -F 'Different threads in the same process may have different' S169.src` → 17;
`grep -n -F 'A thread may modify its' S169.src` → 21;
`grep -n -F 'are silently truncated.' S169.src` → 32.

**Q1 — `man/man5/proc_pid_comm.5:30-32` (15 words)**

> Strings longer than .B TASK_COMM_LEN (16) characters (including the terminating null byte) are silently truncated.

Fact it supports: the comm string a pid probe reads is capped at 16 bytes including the terminating
null byte (15 visible characters) and over-long names are truncated with no error — so a comm
comparison against a long watchdog name is a prefix test on 15 bytes and cannot separate two
processes whose names share that prefix.

**Q2 — `man/man5/proc_pid_comm.5:21-23` (21 words)**

> A thread may modify its .I comm value, or that of any of other thread in the same thread group (see

Fact it supports: the process itself (any of its threads) can rewrite its own comm at runtime by
writing to `/proc/self/task/tid/comm` — so a comm value is a mutable label under the watched
process's control, not a kernel-assigned identity, and a comm match alone is not proof that the
process is the fleet watchdog. (The span ends mid-clause at `(see`; the write path continues at
lines 24-29, ending `.IR /proc/self/task/ tid /comm .` at line 29 — cited here, not quoted, to keep
the quote inside the 25-word cap.)

**Q3 — `man/man5/proc_pid_comm.5:17-20` (21 words)**

> Different threads in the same process may have different .I comm values, accessible via .IR /proc/ pid /task/ tid /comm .

Fact it supports: comm is per-thread and `/proc/<pid>/comm` exposes one thread's value only, with
each thread's own name at `/proc/<pid>/task/<tid>/comm` — so a probe of `/proc/<pid>/comm` reads the
main thread's name and can disagree with what a worker thread of the same process carries.

Additional located (not quoted, outside the Gate row to respect the 1-3 quote cap): lines 34-41 state
that the file is a superset of `prctl(2)` `PR_SET_NAME`/`PR_GET_NAME` and is used by
`pthread_setname_np(3)` to rename threads other than the caller — i.e. a probe can observe a name
set by any library, and reading `/proc/pid/comm` is exactly `PR_GET_NAME` semantics.

## 3. Ready-to-paste Gate row

```
| S169 | https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man5/proc_pid_comm.5?h=man-pages-6.20 | 2026-10-22T23:43:06Z | `31aee9e50c23579e7983e26edee83bee9ab7a8ba4c7be46027db2cac5ee23c08` | `man/man5/proc_pid_comm.5:30-32` (15 words): "Strings longer than .B TASK_COMM_LEN (16) characters (including the terminating null byte) are silently truncated."; `man/man5/proc_pid_comm.5:21-23` (21 words): "A thread may modify its .I comm value, or that of any of other thread in the same thread group (see"; `man/man5/proc_pid_comm.5:17-20` (21 words): "Different threads in the same process may have different .I comm values, accessible via .IR /proc/ pid /task/ tid /comm ." | admit, A, mined |
```

No quote contains a double quote or a pipe, so no `\"` or `\|` escapes were needed.

## 4. Ready-to-paste SOURCES row

```
| S169 | man-pages 6.20 proc_pid_comm(5) — https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man5/proc_pid_comm.5?h=man-pages-6.20 | docs | A | the documented contract of /proc/pid/comm at the man-pages-6.20 tag: the per-thread comm value and its /proc/pid/task/tid/comm access path, a thread modifying its own or a sibling thread's comm by writing there, silent truncation at TASK_COMM_LEN (16 bytes including the terminating null byte), and the file as a superset of prctl(2) PR_SET_NAME/PR_GET_NAME employed by pthread_setname_np(3) | man/man5/proc_pid_comm.5:17-20,21-23,30-32,34-41; tag man-pages-6.20 | A pid probe's comm reading is a mutable, per-thread, at-most-15-visible-byte label that the process itself can rewrite, so a comm match is a prefix comparison on 15 bytes and never an identity assignment. | mined | 2026-10-22 | on-release | corpus/knowledge/watchdog-identity-r31.md |
```

Column order copied from corpus/SOURCES.md:5 (`id | source | kind | tier | scope | anchor | teaches |
status | opened | recheck | used-by`); source-cell style ("descriptive title — URL") copied from
corpus/SOURCES.md:7 row S001. `used-by` is the C1 entry path required by the ticket; that entry file
does not exist yet (`ls corpus/knowledge/watchdog-identity-r31.md` → No such file or directory),
which is expected at draft time.

## 5. Decision: admit

Reason: the fetched bytes carry both required facts verbatim (truncation at `:30-32`; a thread
changing its own comm at `:21-23`), the URL answered `HTTP:200` with genuine troff bytes rather than
a 404 or a challenge page, and the URL is not yet a row in SOURCES.md.

Duplicate checks run in the lane (read-only grep, no writes):
- `grep -c 'man-pages.git/plain/man/man5/proc_pid_comm' corpus/SOURCES.md` → `0` (no-exact-url)
- `grep -n 'proc_pid_comm' corpus/SOURCES.md` → no matches
- `grep -n '^| S169 ' corpus/SOURCES.md` → no matches (id S169 is free; highest existing id seen is S160 at corpus/SOURCES.md:166)
- `grep -rn 'proc_pid_comm' corpus/SOURCES.md corpus/evidence/` → no matches

## 6. Caveats for the L1 and the verifier

- **Version identity rests on the URL tag, not the page header.** Line 7 of the fetched bytes reads
  `.TH proc_pid_comm 5 (date) "Linux man-pages (unreleased)"` — the tag `man-pages-6.20` serves a
  file whose TH line still carries the `(unreleased)` placeholder and a literal `(date)` token. The
  row's identity is therefore the `?h=man-pages-6.20` ref, exactly as the ticket's URL specifies; a
  reader must not expect the page header to name 6.20. [INFERENCE] This is the upstream tag content
  as served, not a fetch error, because the bytes are the complete 49-line file with the tag's other
  content intact.
- **Quotes are troff source, not rendered prose.** Words such as `.I`, `.B`, `.IR` are roff requests
  present in the file; the `:L-M` anchors are the checkable ground truth. Anyone rendering the quotes
  for the C1 decision table should read `comm`, `TASK_COMM_LEN`, and `/proc/pid/task/tid/comm` as the
  emphasised tokens and drop the request names.
- **Not verified here (out of scope):** that the truncation and mutability behaviour holds on the
  host kernel; that is the kernel-side claim of the sibling rows (S163/S164/S165/S166/S167 in the
  round-31 id block) and is not asserted by this row. This row carries documentation only.
- **Unrun checks:** no rendering with `man`/`groff` was attempted (no need for the Gate); no
  re-fetch was made, so the sha256 binds the single 2026-10-22T23:43:06Z fetch only.

## 7. Tooling

No installs or updates were made. Tools used as already present: `curl 8.23.0`, coreutils
`sha256sum`/`wc`/`date`/`grep`/`awk`/`tr`. All commands were wrapped in `timeout`; no background jobs,
no subagents, no process trees left running.
