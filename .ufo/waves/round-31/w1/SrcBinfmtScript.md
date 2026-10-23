# S165 — Linux v7.2 fs/binfmt_script.c (source scout report)

Seat: MoriR31.SrcBinfmtScript. Question: does running a `#!` script change the name the task
gets (interpreter versus script file name), and what does `load_script()` change in the binprm?

## 1. Fetch

| field | value |
|---|---|
| URL | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/binfmt_script.c |
| access time (UTC) | 2026-10-22T23:43:06Z (`date -u +%FT%TZ` recorded before the fetch) |
| HTTP | 200, no redirect; `curl -w` reported `http_code=200 size=4358 url=%{url_effective}` equal to the URL |
| bytes | 4358 (159 lines) |
| saved unchanged | /fast/scratch/hyaku/mori-r31/SrcBinfmtScript/S165.src (curl wrote the file directly; no edit, no line-ending change) |
| sha256 | 81b0293a89908d56575f2b00b3550f927eb80714ef540f9634272bce56f9c656 |
| content type | `text/x-c; charset=utf-8` (`file -i`); S165.src:1 `// SPDX-License-Identifier: GPL-2.0-only`, S165.src:3 `*  linux/fs/binfmt_script.c` |
| stability | a second `curl -sSL --fail -m 60 <URL> \| sha256sum` returned the same digest |

Command run: `curl -sSL --fail -m 60 -o S165.src -w 'http_code=%{http_code} size=%{size_download} url=%{url_effective}\n' '<URL>'`.

## 2. Located quotes (verbatim from the saved bytes)

Line numbers are `grep -n` on S165.src. Q1 is a three-line C comment span, so the file's own
continuation markers (` * `) sit inside the quote; the C1 counter compares whitespace-normalised
text (.ufo/waves/round-31/count-c1.py:47, :171), and the exact string below was tested as a
normalised substring of the saved copy (`q1_norm_substring=True`). None of the three quotes
contains a double quote or a pipe, so the Gate row needs no escaping.

**Q1 — S165.src:99-101 (22 words).** `grep -n "Splice in (1)"` → 99; the span ends at 101.

```
	 * Splice in (1) the interpreter's name for argv[0]
	 *           (2) (optional) argument to interpreter
	 *           (3) filename of shell script (replace argv[0])
```

Fact it supports: a `#!` exec does not keep the script path in argv[0] — `load_script` splices
the interpreter in as argv[0], optionally the interpreter's single argument, and then the script
filename, so a cmdline match against the script path as argv[0] misses while the path still
appears later in the same cmdline (after `remove_arg_zero`, S165.src:106, deleted the caller's
argv[0]).

**Q2 — S165.src:125 (4 words).** `grep -n 'bprm_change_interp' S165.src` → 109 (copy of
`bprm->interp`), 125 (the change).

```
	retval = bprm_change_interp(i_name, bprm);
```

Fact it supports: the bprm's tracked interpreter name is replaced with the `#!` interpreter path
`i_name` — the script's own path does not remain the bprm interp, so anything read from that
field names the interpreter, not the watchdog script. The function body is fs/exec.c (S164), not
this file. [INFERENCE] the field is `bprm->interp` because the callee is `bprm_change_interp()`
and S165.src:109 copies that same field; the definition was not opened in this seat.

**Q3 — S165.src:136 (3 words).** `grep -n 'bprm->interpreter = file' S165.src` → 136.

```
	bprm->interpreter = file;
```

Fact it supports: `open_exec(i_name)` (S165.src:132) leaves the exec to restart on the
interpreter's dentry, so the executable file the process ends up running is the interpreter
(`/bin/bash` for the watchdog), not the script — an `exe`-based probe will not see the script
path. [INFERENCE] the swap of `bprm->file` with `bprm->interpreter` happens in the handler retry
in fs/exec.c (S164), which was not opened here.

**Negative observation (not a quote).** `grep -c 'bprm->filename' S165.src` → 0, and the only
occurrences of the token `filename` are inside comments at S165.src:88 and :101. `load_script()`
writes no `bprm->filename`; which field the task's comm is derived from is decided in
fs/exec.c / fs/proc/array.c (S164, S167), so this file supports only the "interpreter takes
over argv, interp and interpreter file; script path survives as an argument" half of the
identity question.

## 3. Ready-to-paste rows

Gate row (one physical line; no rewrapping inside a quote):

```
| S165 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/binfmt_script.c | 2026-10-22T23:43:06Z | `81b0293a89908d56575f2b00b3550f927eb80714ef540f9634272bce56f9c656` | `binfmt_script.c:99-101` (22 words): "Splice in (1) the interpreter's name for argv[0] * (2) (optional) argument to interpreter * (3) filename of shell script (replace argv[0])"; `binfmt_script.c:125` (4 words): "retval = bprm_change_interp(i_name, bprm);"; `binfmt_script.c:136` (3 words): "bprm->interpreter = file;" | admit, A, mined |
```

Counter fit, checked against .ufo/waves/round-31/count-c1.py: the row starts `| S165 |` (:144),
its last cell starts with `admit` (:146), it holds an `https://` cell (:151), a backticked 64-hex
sha256 (:152), and three `(N words): "..."` quotes each with `len(q.split()) <= 25` (:153); the
same digest comes back from the live URL (:173) and every quote is present in the committed copy
after normalisation (:171). Copy /fast/scratch/hyaku/mori-r31/SrcBinfmtScript/S165.src to
corpus/evidence/sources-r31/S165.src unchanged; its sha256 is the digest in the row.

SOURCES row (11 columns, order from corpus/SOURCES.md:5):

```
| S165 | Linux fs/binfmt_script.c at v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/binfmt_script.c | code | A | the exec-time splice `load_script()` performs for a `#!` script at the v7.2 tag only: removal of the caller's argv[0], the interpreter name copied as argv[0], the optional interpreter argument, the script filename added next, `bprm_change_interp(i_name)` for the bprm interp name, and the `bprm->interpreter` dentry the exec restarts on; no assignment to `bprm->filename` anywhere in this file; not the `bprm_change_interp()` body or the handler retry that swaps `bprm->file`, not the /proc/<pid> comm, cmdline or exe renderers, not this host's watchdog script | load_script:34; splice comment:99-101; remove_arg_zero:106; interp copy:109; i_name copy:121; bprm_change_interp:125; bprm->interpreter:136; tag v7.2; sha256 81b0293a89908d56 | A `#!` exec puts the interpreter in argv[0] and the script path in a later argument, and records the interpreter as the bprm interp and interpreter file, so an exe or interp reading of the process names the interpreter while the script path survives only in argv; the field this file never assigns is left for fs/exec.c to explain. | mined | 2026-10-22 | on-release | corpus/knowledge/watchdog-identity-r31.md |
```

## 4. Decision

**admit.**

- The bytes carry the mechanism, not a mention: the exact argv order (99-101), the interp rewrite
  (125), and the interpreter restart (136), each at a line number reproduced by `grep -n`.
- Not a 404, not a challenge page: HTTP 200, no redirect, 4358 bytes of real C with the upstream
  SPDX line and the file banner (S165.src:1-3), `file -i` → `text/x-c`.
- Not already registered: `grep -c 'raw.githubusercontent.com/torvalds/linux/v7.2/fs/binfmt_script.c' corpus/SOURCES.md` → 0;
  `grep -n 'binfmt_script' corpus/SOURCES.md` → no output; `grep -n '^| S165 ' corpus/SOURCES.md` → no output;
  the highest id present is S160 (corpus/SOURCES.md:165), so S165 is free.

Caveats the L1 should weigh when writing the C1 rows:

- This source answers "what does the exec do to argv, interp and the interpreter file". It does
  not answer "what does comm show". A row that claims comm equals the script basename needs
  S164 (`__set_task_comm` reading `bprm->filename`) or S167, not S165; from S165 alone the
  supportable observation is that the script path is an argv element while the interpreter owns
  argv[0], `exe` and the interp name.
- The `*` tokens inside the Q1 quote are the file's own comment-continuation characters. If a
  reviewer prefers a marker-free quote, the single-line fallbacks are S165.src:99
  (8 words: "Splice in (1) the interpreter's name for argv[0]") and S165.src:101
  (7 words: "(3) filename of shell script (replace argv[0])"), both also normalised substrings of
  the saved copy.

## Bounds and tooling

- Wrote only this report and `S165.src` under /fast/scratch/hyaku/mori-r31/SrcBinfmtScript/.
  No git or jj command run; nothing else in the lane written; no unit started or signalled;
  no pacman run (host transactions are paused).
- No tool installed or updated; curl, sha256sum, file and grep were already present.
- Processes: every command bounded (`curl -m 60`, bash tool deadlines); nothing left running.
- Privacy: no uid, real pid, slice or unit name, journal text, settings value or session path in
  this report; `/proc/<pid>` is a placeholder.
