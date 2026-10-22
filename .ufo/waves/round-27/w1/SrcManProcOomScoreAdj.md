# SrcManProcOomScoreAdj — man7 oom_score_adj(5) / oom_score(5) vs Linux v7.2 fs/proc/base.c

Seat: leaf scout, round 27 wave 1. Question: what the man-pages project documents for
`/proc/pid/oom_score_adj` and `/proc/pid/oom_score`, and where that text differs from the v7.2 kernel
wording in `fs/proc/base.c`.

Verdict in one line: the two pages state the range and the -1000 rule correctly, but they (a) still carry
a "root processes are given 3% extra memory" factor that v7.2 `oom_badness()` does not implement,
(b) describe the adjustment as *added* where the kernel *scales* it by `totalpages / 1000`, and (c) state
inheritance and the `CAP_SYS_RESOURCE` write rule only inside the legacy `oom_adj` paragraph, never for
`oom_score_adj`. The same text is present in the current man-pages 6.20 sources, so this is not a stale
6.19 rendering.

## Gate

| field | value |
|---|---|
| URL 1 | https://man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html |
| URL 2 | https://man7.org/linux/man-pages/man5/proc_pid_oom_score.5.html |
| URL 3 (comparison) | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c |
| access | date 2026-10-22; `curl` bytes on disk stamped 2026-10-22T15:46:37Z and 15:46:38Z (UTC); HTTP 200 for all three |
| sizes | 11,680 B / 7,955 B / 98,196 B |
| sha256 | `769edf3b9c054934db07f16173297fc5fd63c3a4c807682355f08fa45cde80a9` / `6169628d8a2cdc512795cfda74f3598d5b7a25e5b71921d4088c0539cf71b2bc` / `cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6` |
| man-pages version | footer line: `Linux man-pages 6.19` / page date `2026-02-08` (adj page:175; score page:120); HTML rendering dated 2026-09-09 (adj page:194) from tarball `man-pages-6.19.tar.gz` (adj page:165-168) |

Located quotes, verbatim, at most 25 words each (line numbers are lines of the fetched bytes named above):

1. adj page:104-105 — "Acceptable values range from -1000 (OOM_SCORE_ADJ_MIN) to +1000 (OOM_SCORE_ADJ_MAX)." (9 words)
2. adj page:108-110 — "The lowest possible value, -1000, is equivalent to disabling OOM-killing entirely for that task, since it will always report a badness score of 0." (24 words)
3. adj page:102-103 — "The value of oom_score_adj is added to the badness score before it is used to determine which task to kill." (20 words)
4. adj page:145-146 — "The default value for this file is 0; a new process inherits its parent's oom_adj setting." (17 words)
5. adj page:146-149 — "A process must be privileged (CAP_SYS_RESOURCE) to update this file, although a process can always increase its own oom_adj setting" (20 words)

Also located but outside the quote budget: score page:73-76 (score "displays the current score", higher means more
likely), score page:80 ("whether the process is privileged (-)" listed as a live factor), score page:97-98
(oom_score "also reflects the adjustment specified by the oom_score_adj or oom_adj setting"), adj page:86-88
("root processes are given 3% extra memory over other tasks"), adj page:122-127 (oom_adj scaling and
write-through between the two files).

## Statement by statement against the v7.2 kernel

Commands: fetches as in the Gate; then `grep -n` and `sed -n` on the saved bytes in
`/fast/scratch/hyaku/mori-r27/MoriR27.SrcManProcOomScoreAdj/`. Kernel-side files fetched at the same time:
`include/uapi/linux/oom.h` (526 B, sha256 `6b00b4d0…96ae`), `include/linux/oom.h` (2,873 B, sha256 `42e8e17f…b7fd`),
`kernel/fork.c` (85,725 B, sha256 `359882ea…dd1d`), `fs/exec.c` (51,001 B, sha256 `44e4185b…72c7`),
`mm/oom_kill.c` (34,311 B, sha256 `452f1348…6b4e`). Two first attempts returned HTTP 429 and were retried
successfully except where noted.

| # | Page says | Kernel v7.2 says | Relation |
|---|---|---|---|
| 1 | acceptable values -1000..+1000 (adj:104-105) | `OOM_SCORE_ADJ_MIN (-1000)` / `OOM_SCORE_ADJ_MAX 1000` (uapi/linux/oom.h:9-10) and the writer rejects anything outside with `-EINVAL` (base.c:1275-1279) | agree |
| 2 | -1000 disables OOM-killing "for that task", reporting badness score 0 (adj:108-110) | internal `oom_badness()` returns `LONG_MIN` for `adj == OOM_SCORE_ADJ_MIN` (mm/oom_kill.c:216-223) and `select_bad_process()` skips `points == LONG_MIN` (mm/oom_kill.c:340); the 0 is only the exported file value, because `proc_oom_score()` leaves `points` at 0 when badness is `LONG_MIN` (base.c:586,596-599) | same observable file value, different mechanism: the task is excluded from scoring, not scored 0 |
| 3 | the adjustment is *added* to the badness score (adj:102-103) | `adj *= totalpages / 1000; points += adj;` — scaled by the allowed-memory page count before adding (mm/oom_kill.c:232-235) | wording divergence; the page's own "roughly 50%" example (adj:114-120) only works because of the scaling the sentence omits |
| 4 | "root processes are given 3% extra memory over other tasks" (adj:86-88); score page:80 lists "whether the process is privileged (-)" as a live factor | `oom_badness()` in v7.2 has no privilege term: `points = get_mm_rss_sum + swapents + pgtables/PAGE_SIZE` then `+ adj` (mm/oom_kill.c:226-235); `grep -c capab mm_oom_kill.c` → `0` (also 0 for `capable`) | the page's 3% clause is not implemented anywhere in v7.2 `oom_badness`; when it was removed is not established here [INFERENCE: stale clause, not a different code path] |
| 5 | no statement about `/proc/pid/oom_score` numeric range or about which "allowed memory" the file uses | file value = `(1000 + badness*1000/totalpages) * 2 / 3` with `totalpages = totalram_pages() + total_swap_pages` (base.c:586,596-597), i.e. the [0, 2000] export the code comment names (base.c:591-594); kill-time `oc->totalpages` may instead be a cpuset/mempolicy/memcg limit (mm/oom_kill.c:339) | page documents neither the scaling nor the divergence between the file's basis and the kill-time basis [INFERENCE: max 2000 follows arithmetically from the two line refs] |
| 6 | oom_adj still tunes the score, scaled linearly; writing either file changes the other (adj:122-127) | `oom_adj_read` maps `oom_score_adj` back with `* -OOM_DISABLE / OOM_SCORE_ADJ_MAX` and special-cases `OOM_SCORE_ADJ_MAX` (base.c:1089-1101); `oom_adj_write` scales the other way and routes through `__set_oom_adj(..., true)` (base.c:1213-1231) | agree |
| 7 | file permissions not stated | `ONE("oom_score", S_IRUGO, …)` and `REG("oom_score_adj", S_IRUGO\|S_IWUSR, …)` (base.c:3351-3353): score world-readable, adj world-readable and owner-writable | page silent |

## Inheritance across fork and execve

- The `oom_score_adj` paragraph never says what a child inherits; the only inheritance sentence on the page is
  inside the `oom_adj` HISTORY paragraph (adj:145-146, quote 4).
- Kernel, fork: `sig->oom_score_adj = current->signal->oom_score_adj;` and
  `sig->oom_score_adj_min = current->signal->oom_score_adj_min;` in `copy_signal()` (kernel/fork.c:1768-1769),
  re-synchronised by `copy_oom_score_adj()` for a `CLONE_VM` clone that is not a thread or vfork
  (kernel/fork.c:1949-1964), called from `copy_process()` (kernel/fork.c:2558).
- Kernel, execve: `grep -n 'oom_score_adj' fs/exec.c` → 0 hits, so execve neither resets nor recomputes the value;
  the `signal_struct` carrying both fields survives exec. So `oom_score_adj` is inherited across fork and
  preserved across execve, including the recorded floor `oom_score_adj_min`.
- Consequence for the entry: inheritance is true in v7.2 but is *unstated* on the `oom_score_adj` page; the
  knowledge entry must cite `kernel/fork.c` (or `base.c`) for it, not the man page. This is a gap, not a
  contradiction.

## Privilege rule

- Page: no privilege sentence exists for `oom_score_adj`. `grep -c privileged` on the adj page → 1, and that one
  hit is line 147 inside the `oom_adj` paragraph (quote 5). The score page's single hit is line 80, the 3% factor.
- Kernel, write gate: `if ((short)oom_adj < task->signal->oom_score_adj_min && !capable(CAP_SYS_RESOURCE)) { err = -EACCES; }`
  in the non-legacy branch of `__set_oom_adj()` (base.c:1131-1133). The floor `oom_score_adj_min` is only lowered
  when the *writer* held `CAP_SYS_RESOURCE` without audit: base.c:1156-1157, and the same for processes sharing the
  mm at base.c:1175-1176.
- Therefore the implemented rule is a floor rule, not "must be privileged to write": an unprivileged process may
  raise its own value freely and may lower it back to the lowest value it previously set while privileged; only
  `CAP_SYS_RESOURCE` may go below that floor, down to -1000. The page's nearest sentence is the `oom_adj` one
  ("can always increase its own oom_adj setting", adj:146-149), scoped to the legacy file.
- File mode adds a first gate the page never mentions: `S_IWUSR` only (base.c:3353), so a non-owner cannot open
  for write at all.

## Is the text current? (man-pages 6.20 cross-check)

The project's tag list contains `man-pages-6.19` and `man-pages-6.20`
(`https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/refs/tags`, HTTP 200, 86,480 B, 2026-10-22).
Sources at tag `man-pages-6.20`:
`https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man5/proc_pid_oom_score_adj.5?id=man-pages-6.20`
(HTTP 200, 4,212 B, sha256 `16a0d4b50deca2828d840350262d936f70934272a276b96c750af050f31161f3`) and the same path for
`proc_pid_oom_score.5` (HTTP 200, 1,899 B, sha256 `95c707bd3b4f2d8615085ac5a1bdacbeb5d975cfb94371dcfd4bf33e239f50ea`).
`grep -n` on those bytes finds the same four statement blocks: "3% extra memory" (6.20 adj:25-26), the +-1000 range
(6.20 adj:46-47), "badness score of 0" (6.20 adj:53), "inherits its parent's" and "must be privileged" for `oom_adj`
(6.20 adj:101-105), and "whether the process is privileged (-)" on the score page (6.20 score:28). So the served
6.19 rendering is not behind on these points. (At the 6.20 tag the page lives at `man/man5/`; the `man5/…` form returned 404 while
`man/man5/…` returned 200, so the difference is repository layout, not a missing page.)

## Row decision

No existing row covers either man page. `grep -n 'man7.org/linux/man-pages/man5' corpus/SOURCES.md` returns only
S097 (`proc_pressure(5)`, rejected: HTTP 404, no such page); S027 (`pidfd_open(2)`) and S031 (`pipe(7)`) are man7.org
pages for other interfaces, and nothing in the registry names either proc oom page. The
highest id in the registry is S126 (`grep -o '^| S[0-9]*' corpus/SOURCES.md | sort -V | tail -1`), so the new row
is S127; if a sibling round-27 seat lands a row first, renumber. `mm/oom_kill.c` already has row S003, so the
`oom_badness` evidence is an anchor addition to S003, not a new row.

### Ready-to-paste SOURCES.md row (new, S127)

```
| S127 | /proc/pid/oom_score_adj(5) and /proc/pid/oom_score(5) manual pages with the v7.2 read and write path they describe — https://man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html ; https://man7.org/linux/man-pages/man5/proc_pid_oom_score.5.html ; https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c | docs | A | the documented contract of the two proc files as served from man-pages 6.19, plus the v7.2 kernel code that enforces it: the -1000..+1000 range, the -1000 reading, the added-versus-scaled adjustment wording, the 3% root clause, the oom_adj legacy scaling, the owner-only write mode, and the fact that inheritance and the CAP_SYS_RESOURCE rule are documented only inside the oom_adj paragraph; not kill-time victim ordering, not OOM_SCORE_ADJ_MIN exclusion, not this host's oom_score_adj values, not earlyoom's own selection logic | adj page:72 (since 2.6.36), :86-88 (3% root), :102-103 (adjustment "added"), :104-110 (range and -1000), :122-127 (oom_adj scaling), :145-149 (oom_adj inheritance and privilege), :175 (footer "Linux man-pages 6.19 2026-02-08"); score page:72-80 (since 2.6.11, factors), :97-98 (reflects the adjustment), :120 (footer); base.c:583-601 (proc_oom_score, totalpages :586, formula :596-597, [0, 2000] comment :591-594), :1089-1101 and :1213-1231 (oom_adj scaling), :1131-1133 (CAP_SYS_RESOURCE floor gate, -EACCES), :1156-1157 (:1175-1176 shared-mm copy of oom_score_adj_min), :1242-1256 (oom_score_adj read), :1275-1279 (range check, -EINVAL), :3351-3353 (S_IRUGO / S_IRUGO\|S_IWUSR); HTTP 200 on 2026-10-22T15:46:37Z–15:46:38Z, 11,680 B sha256 769edf3b9c054934db07f16173297fc5fd63c3a4c807682355f08fa45cde80a9, 7,955 B sha256 6169628d8a2cdc512795cfda74f3598d5b7a25e5b71921d4088c0539cf71b2bc, base.c 98,196 B sha256 cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6; Linux tag v7.2; man-pages 6.20 sources carry the same four statement blocks (adj 6.20:25-26,46-47,53,101-105) | The two files are different contracts: oom_score_adj is the writable -1000..+1000 preference whose value the kernel scales by totalpages/1000, oom_score is a read-only [0, 2000] export folding that preference in, and the page's inheritance and privilege sentences belong to the legacy oom_adj file, not to oom_score_adj. | mined | 2026-10-22 | on-release | corpus/knowledge/oom-victim-selection-r27.md |
```

### Companion anchor addition to existing row S003 (same file, no new row)

Append to S003's `anchor` cell, after `mm/oom_kill.c:447,935-936,945`:

```
oom_badness:191-237 (OOM_SCORE_ADJ_MIN -> LONG_MIN :216-223, adj scaled :232-235), select_bad_process LONG_MIN skip:340, oom_task_origin force-select:334-337
```

and append to S003's `used-by` cell:

```
, corpus/knowledge/oom-victim-selection-r27.md
```

## Confidence and remaining unknowns

- High confidence: every page statement above is quoted from bytes whose sha256 is recorded, and every kernel
  statement is a line reference in the pinned v7.2 file, with downloads from `raw.githubusercontent.com` at the
  v7.2 tag.
- High confidence that the 3% root clause has no implementation in v7.2 `oom_badness`: `grep -c capab mm/oom_kill.c`
  → 0 over the whole file.
- Not established here, left to the kernel-OOM seats: when the 3% root factor was removed from the kernel
  [INFERENCE: before v7.2]; what sets `oom_flag_origin`, the flag that lets `select_bad_process` force-select a task
  with `LONG_MAX` points (mm/oom_kill.c:334-337; the setter is `set_current_oom_origin()` at
  include/linux/oom.h:59-62, and its callers were not traced); whether `oom_score_adj_min` starts at 0 for a fresh
  `signal_struct` (inferred from the copy-only writes at kernel/fork.c:1768-1769, not read from the allocator).
- `include/linux/sched/signal.h` returned HTTP 429 twice and was dropped; it is not needed because fork.c shows both
  assignments.
- A first `curl` of `include/linux/oom.h` returned 429 and its 313-byte error body was overwritten by the retry
  (2,873 B, sha256 `42e8e17f…`); the constants themselves are in `include/uapi/linux/oom.h`, not in that header.

## Tooling

No installs or upgrades. `curl` and coreutils already present; all bytes were fetched with plain `curl` from
`man7.org`, `raw.githubusercontent.com` and `git.kernel.org`, and stored under
`/fast/scratch/hyaku/mori-r27/MoriR27.SrcManProcOomScoreAdj/`. No unit, service, `/etc` file or process signal was
touched; no host process attribute was read or written.
