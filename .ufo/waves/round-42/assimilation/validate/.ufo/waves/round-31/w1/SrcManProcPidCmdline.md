# S170 — proc_pid_cmdline(5) at man-pages 6.20 (C1 candidate source)

Seat: `MoriR31.SrcManProcPidCmdline` (leaf). Round 31, wave 1. Question: can a pid
string probe identify the fleet watchdog? This seat opens the command-line page and
drafts its Gate and SOURCES rows.

**Verdict: admit.** The fetched bytes carry both required facts (empty read for a
zombie, post-exec rewriting of `argv`), the URL returned real troff (not a challenge
page), and the exact URL is not yet a row in `corpus/SOURCES.md`.

## 1. Fetch record

| item | value |
|---|---|
| URL | `https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man5/proc_pid_cmdline.5?h=man-pages-6.20` |
| command | `curl -sSL --fail -m 60 -o S170.src "<URL>"` under `timeout 90` |
| access time (UTC) | `2026-10-22T23:43:06Z` (`date -u +%FT%TZ` taken at fetch) |
| curl exit | 0 |
| bytes | 1557 (`wc -c`) |
| sha256 | `a9f3b83b1b0442319d0a8a5be23787c8024bc485dd54a062da9c37d57733f111` |
| type | `troff or preprocessor input, ASCII text` (`file S170.src`), 50 lines |
| saved copy | `/fast/scratch/hyaku/mori-r31/SrcManProcPidCmdline/S170.src` (unchanged bytes) |
| stability | re-fetch at `2026-10-22T23:44:52Z` → same sha256, `cmp` reports IDENTICAL |

Tag identity: the URL pins the tag in its query (`h=man-pages-6.20`); a non-existent
ref would have failed `--fail`. The in-tree header is the pre-release placeholder, so
the version string itself proves nothing about the tag:

- `S170.src:7` — `.TH proc_pid_cmdline 5 (date) "Linux man-pages (unreleased)"`

Identity therefore rests on the URL's `h=man-pages-6.20` plus the recorded sha256, not
on line 7. [INFERENCE] the released 6.20 tarball's rendered copy most likely differs
only in that `.TH` date/version line; I did not download the tarball to diff it, so the
fact-level text quoted below is verified against the tag-served bytes only.

## 2. Located quotes (verbatim from `S170.src`, word counts by `len(split())`)

All three spans were checked with the counter's own path — `re.findall` over
`\(\s*\d+\s+words?\s*\):\s*"..."`, `unescape`, then `norm(quote) in norm(copy)` where
`norm` collapses whitespace (`count-c1.py:36-38,50-51,...`); all three return True.
Multi-line sentences below are their whitespace-normalized form, which is what the
counter compares.

1. `S170.src:13-14` — 17 words:
   "This read-only file holds the complete command line for the process, unless the process is a zombie."
   Fact: the complete-command-line guarantee is explicitly waived for zombies, so a
   cmdline string match is only defined for a process that is still running.

2. `S170.src:16-17` — 21 words:
   "In the latter case, there is nothing in this file: that is, a read on this file will return 0 characters."
   Fact: an unreaped zombie watchdog reads 0 bytes, so an empty `/proc/<pid>/cmdline`
   read is consistent with a watchdog process that still exists — empty is not a
   death signal; the probe must also read the process state.
   ("the latter case" is the zombie clause of quote 1; the two quotes belong together.)

3. `S170.src:33-37` — 19 words:
   "If, after an .BR execve (2), the process modifies its .I argv strings, those changes will show up here."
   Fact: a live process can rewrite its `argv` strings after `exec`, so the bytes a
   probe reads back are the rewritten content — a cmdline match never proves which
   program was exec'd. (Rendered text: "If, after an execve(2), the process modifies
   its argv strings, those changes will show up here." The markup tokens `.BR`/`.I`
   are part of the fetched bytes, which is why the quote is norm-contiguous and passes
   the counter.)

Two further candidates, also norm-contained, kept out of the three-quote budget:

- `S170.src:42-45` — 22 words: "Furthermore, a process may change the memory location that this file refers via .BR prctl (2) operations such as .BR PR_SET_MM_ARG_START ."
  Fact: the reported bytes need not even live in the original argv image; the page
  documents relocation of the memory region the file refers to.
- `S170.src:47` — 15 words: "Think of this file as the command line that the process wants you to see."
  Fact: the page's own framing — the file is a claim by the process, which caps its
  value as identity evidence.

Warning for later rows quoting this page: `S170.src:26-31` carries the "processes have
the freedom to override the memory region" sentence, but lines 30-31 embed
`.IR /proc/ pid /cmdline` markup, so a quote of that full sentence fails the counter's
`norm` containment. Quote up to `S170.src:28` ("…override the memory region and", 17
words, norm-contained) or use the spans above.

## 3. Ready-to-paste rows

Gate row for `corpus/lessons/round-31.md` (one physical line, 6 cells after the
counter's `cells()` strips the outer pipes, last cell starts with `admit`):

```text
| S170 | https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man5/proc_pid_cmdline.5?h=man-pages-6.20 | 2026-10-22T23:43:06Z | `a9f3b83b1b0442319d0a8a5be23787c8024bc485dd54a062da9c37d57733f111` | `proc_pid_cmdline.5:13-14` (17 words): "This read-only file holds the complete command line for the process, unless the process is a zombie."; `proc_pid_cmdline.5:16-17` (21 words): "In the latter case, there is nothing in this file: that is, a read on this file will return 0 characters."; `proc_pid_cmdline.5:33-37` (19 words): "If, after an .BR execve (2), the process modifies its .I argv strings, those changes will show up here." | admit, A, mined |
```

SOURCES row for `corpus/SOURCES.md` (11 columns, order of `corpus/SOURCES.md:5`):

```text
| S170 | proc_pid_cmdline(5) manual page at the man-pages 6.20 tag — https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man5/proc_pid_cmdline.5?h=man-pages-6.20 | docs | A | the documented contract of /proc/pid/cmdline at man-pages 6.20 (the v7.2 kernel read path that serves it is a different row's object): the zombie exception and its 0-character read, the null-byte layout for well-behaved processes, the freedom to override the memory region, the post-exec rewrite of argv strings as distinct from the argv array, the prctl(2) PR_SET_MM_ARG_START relocation, and the command-line-the-process-wants-you-to-see framing | proc_pid_cmdline.5:7 (`.TH proc_pid_cmdline 5 (date) "Linux man-pages (unreleased)"`, the in-tree pre-release placeholder), :13-14, :16-17, :26-31, :33-40, :42-45, :47; 1557 bytes, 50 lines, sha256 a9f3b83b1b0442319d0a8a5be23787c8024bc485dd54a062da9c37d57733f111, tag pinned by the URL query h=man-pages-6.20, fetched 2026-10-22T23:43:06Z and re-fetched byte-identical 2026-10-22T23:44:52Z | A /proc/pid/cmdline match is a self-reported, process-writable view: a zombie reads 0 bytes, so an empty read cannot separate a dead watchdog from a live zombie one, and a running process can rewrite its argv strings or relocate the reported memory, so a cmdline match never proves which executable is running. | mined | 2026-10-22 | on-release | corpus/knowledge/watchdog-identity-r31.md |
```

Evidence copy for the counter: `cp /fast/scratch/hyaku/mori-r31/SrcManProcPidCmdline/S170.src
corpus/evidence/sources-r31/S170.src` — byte-for-byte, no newline normalization; the
committed copy must hash to
`a9f3b83b1b0442319d0a8a5be23787c8024bc485dd54a062da9c37d57733f111` for `count-c1.py` to
pass its `copies_ok` and `fetch_ok` legs.

## 4. Admit / reject

**admit** — each reject condition was tested, not assumed:

- Bytes carry the facts: zombie exception at `:13-14`, 0-character read at `:16-17`,
  argv rewrite at `:33-37`, plus `:42-45` and `:47`. No 404 and no challenge page: the
  body is troff with `.SH NAME`, `.SH DESCRIPTION`, `.SH SEE ALSO` and curl exited 0
  with `--fail`.
- Exact URL not already a row: `grep -c 'proc_pid_cmdline' corpus/SOURCES.md` = 0 and
  `grep -c 'man/man5/proc_pid_cmdline.5' corpus/SOURCES.md` = 0 (`grep` exit 1 on the
  second). The only man-pages-git plain URL in the registry is a different page and a
  different query parameter — `corpus/SOURCES.md:155` carries
  `.../man/man5/proc_pid_oom_score_adj.5?id=man-pages-6.20` under S149. Note for L1:
  S149 used `?id=`, the assignment fixes mine at `?h=`; both resolve, and the counter
  re-fetches my exact `?h=` URL, so it must not be rewritten to `?id=` without the sha
  being re-measured (a parameter change is a different URL string in the Gate row).

## 5. Scope limits for the entry

- This row is documentation only. The kernel-side mechanism (what `fs/proc/base.c`
  returns, whether the state field is `Z`, what `comm` holds after exec) is not in
  these bytes and must rest on the code rows assigned to other seats (S164-S167).
- The page states the zombie read returns 0 characters; it does not say how a probe
  distinguishes the states, and it does not mention the watchdog script at all. The
  entry's decision table must derive the reading from the state field, not from an
  empty cmdline alone.

## 6. Compliance

- Leaf seat: no subagents, no background jobs. Every command ran under `timeout`
  (≤90 s); the two curls finished in the recorded seconds.
- No git/jj writes anywhere; no writes outside this Report and my scratch dir
  `/fast/scratch/hyaku/mori-r31/SrcManProcPidCmdline/`. Lane reads used `read`/`grep`
  and `awk`/`cut` only.
- Privacy: no uid, no real pid (placeholder `<pid>`), no unit names, no journal text,
  no session ids, no settings values.
- Tool installs/updates: none this seat (system `curl`, `sha256sum`, `file`, `cmp`
  already present; no pacman, no uv/npx installs).
