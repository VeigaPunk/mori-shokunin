# SrcProcBaseOomScore — Linux v7.2 `fs/proc/base.c`: how `/proc/<pid>/oom_score` is derived and what the `oom_score_adj` write path enforces

Question: extract `proc_oom_score()` (the `1000 + badness*1000/totalpages` form, the `*2/3`
scaling and the resulting range) and the `oom_score_adj` write path (`__set_oom_adj`: the
CAP_SYS_RESOURCE / `oom_score_adj_min` floor, the -1000..1000 range, and the copy to processes
sharing the mm), then return the SOURCES row (or existing-row anchor) that grounds it for C1.

Bottom line: **no existing row covers `fs/proc/base.c`** — `grep -n 'base\.c\|proc/base' corpus/SOURCES.md`
returns nothing, and the highest id in the working copy is S126 (`corpus/SOURCES.md:132`), so this
is a **new row, S127** (renumber if a sibling seat claimed S127 first; it was free when I read the
file). Two companion files were opened for facts the row needs and neither has an existing row
either (`grep -n 'kernel/fork\.c\|uapi/linux/oom\.h\|OOM_SCORE_ADJ' corpus/SOURCES.md` → no hit):
`include/uapi/linux/oom.h` (the numeric bounds) and `kernel/fork.c` (the fork-time copy that makes
the mm-sharing rule reachable). All three are folded into one row per the multi-URL shape of
S116/S117/S118. `mm/oom_kill.c` is **not** part of this row: S003 already owns it and two sibling
seats in this wave already propose its anchor, so this seat adds nothing there. A sibling seat
(`MoriR27.SrcManProcOomScoreAdj`) also proposes `S127`, for a man-page row that lists the same
`base.c` URL for its enforcing code — the id must be settled by the L1, and the dedupe instruction
is in the Overlap section.

## Gate block

Opening was ordinary `curl` only, no browser. `raw.githubusercontent.com` answered `HTTP 429`
(313 B body, "This request was rate-limited due to too many requests from your network") on my
second fetch and on a retry 27 s later, so the two companion files were fetched from the official
kernel.org cgit plain view at the same tag. Recorded as fetched, not re-pinned to a mirror.

| file | URL | access (UTC) | result | sha256 |
|---|---|---|---|---|
| `fs/proc/base.c` | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c | 2026-10-22T15:46:35Z | HTTP 200, 98,196 B, 3990 lines | `cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6` |
| `include/uapi/linux/oom.h` | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/uapi/linux/oom.h?h=v7.2 | 2026-10-22T15:47:2xZ | HTTP 200, 526 B | `6b00b4d0648bcdc9d6be7ea8a33b8e6b842c063e7b2b71bdabd757de773896ae` |
| `kernel/fork.c` | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/kernel/fork.c?h=v7.2 | 2026-10-22T15:48:0xZ | HTTP 200, 85,725 B | `359882ea981b58f5289293e5644f7c0085a8350e4f1937f39dcb94ae1cd0dd1d` |
| `mm/oom_kill.c` (cross-check only) | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/mm/oom_kill.c?h=v7.2 | 2026-10-22T15:47:5xZ | HTTP 200, 34,311 B | `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e` |

Located quotes (verbatim, <=25 words, whitespace joined across line breaks, word count in
parentheses; kept as a list so the `||` in Q5 is not read as a table delimiter):

- Q1 `base.c:596-597` (17) — `if (badness != LONG_MIN) points = (1000 + badness * 1000 / (long)totalpages) * 2 / 3;`
- Q2 `base.c:593` (10) — `badness value into [0, 2000] range which we have been`
- Q3 `base.c:1131-1133` (10) — `if ((short)oom_adj < task->signal->oom_score_adj_min && !capable(CAP_SYS_RESOURCE)) { err = -EACCES;`
- Q4 `base.c:1173-1174` (9) — `if (!p->vfork_done && process_shares_mm(p, mm)) { p->signal->oom_score_adj = oom_adj;`
- Q5 `base.c:1275-1276` (9) — `if (oom_score_adj < OOM_SCORE_ADJ_MIN || oom_score_adj > OOM_SCORE_ADJ_MAX) {`

`include/uapi/linux/oom.h:9-10` defines the two bounds Q5 compares against: `OOM_SCORE_ADJ_MIN
(-1000)` and `OOM_SCORE_ADJ_MAX 1000`, with the comment at :5-8 saying that a `oom_score_adj` of
`OOM_SCORE_ADJ_MIN` disables OOM killing for that pid (fetched file, 526 B, sha256 above). Q5's
consequence is `err = -EINVAL` at :1277.

## Observed facts (all from the fetched v7.2 bytes)

`proc_oom_score()` at base.c:583-599, registered read-only as `ONE("oom_score", S_IRUGO,
proc_oom_score)` in both the process table (:3351) and the per-thread table (:3706), so
`/proc/<pid>/oom_score` and `/proc/<pid>/task/<tid>/oom_score` expose the same computation:

- :586 `totalpages = totalram_pages() + total_swap_pages` — RAM plus swap, not RAM alone.
- :590 `badness = oom_badness(task, totalpages)`; `points` starts at 0 (:587), so an unkillable
  task or `oom_score_adj == -1000` (`oom_badness` returns `LONG_MIN`, oom_kill.c:204-221) prints 0.
- :596-597 the exported number is `(1000 + badness*1000/totalpages) * 2 / 3` (Q1), integer
  arithmetic, printed with `%lu` at :599. The code's own comment (:592-594, Q2) names the exported
  range `[0, 2000]` and says userspace may depend on it.
- Consequence for reading a live `oom_score`: [INFERENCE] arithmetic on Q1 plus oom_kill.c:228-236
  (badness = rss + swap pages + page tables, then `adj*totalpages/1000` added) gives ~666 for a
  task with no pages and `oom_score_adj = 0`, and the theoretical maximum 2000 needs usage equal
  to all of RAM+swap with `oom_score_adj = 1000`. So a large-looking score is offset by a ~666
  baseline; it is not a percentage of memory and cannot be compared across boots without the
  same `totalpages`. This is arithmetic on observed code, not a measured value.

`oom_score_adj_write()` at base.c:1258-1284 parses an int (:1272 `kstrtoint`) and rejects anything
outside the inclusive range with `-EINVAL` (:1275-1279, Q5); inside the range it calls
`__set_oom_adj(file, oom_score_adj, false)` (:1281). `oom_score_adj_read()` at :1242-1254 prints the
thread-group value with `%hd`. Both files are registered `S_IRUGO|S_IWUSR` (:3353, :3708), i.e.
world-readable, writable only by the process owner (root for system services); `oom_score` itself
is read-only (`S_IRUGO`, :3351/:3706). Note the mode is not the whole gate — `__set_oom_adj`
applies the capability rule below even for the file owner.

`__set_oom_adj()` at base.c:1106-1186:

- The value lives in `task->signal->oom_score_adj` (:1155), i.e. in the thread-group's
  `signal_struct`, so every thread of a process reports and writes one value; the propagation loop
  skips `same_thread_group()` peers (:1165-1166) because they already share it. [INFERENCE] from
  the field's home and that skip, not a separate documented statement.
- Floor rule (:1130-1136, Q3): a non-legacy write below `task->signal->oom_score_adj_min` fails
  `-EACCES` unless the writer has `CAP_SYS_RESOURCE`. The legacy `/proc/<pid>/oom_adj` path instead
  compares against the current `oom_score_adj` (:1118-1122) and warns once that it is deprecated
  (:1127).
- `oom_score_adj_min` rises and falls with privileged writes only: after the assignment at :1155,
  `:1156-1157` sets `oom_score_adj_min = (short)oom_adj` when the writer has `CAP_SYS_RESOURCE`
  and the path is not legacy. So an unprivileged process may raise its own score freely, may lower
  it down to the floor, and a root writer lowering the value also lowers the floor for later
  unprivileged writes — the floor tracks the last privileged value, which is exactly the proc.rst
  sentence the sibling seat found (S082).
- mm sharing (:1138-1180): unless the task is mid-`vfork` (:1143), the function grabs the mm when
  `mm_flags_test(MMF_MULTIPROCESS, p->mm)` (:1147-1149), then after assigning its own
  `signal->oom_score_adj` (:1155) walks `for_each_process()` and, for every process that is not a
  thread-group peer (:1165-1166), not a kernel thread and not global init (:1169), and that passes
  `process_shares_mm(p, mm)` (:1173), copies the same value and — for a privileged writer — the
  same `oom_score_adj_min` (:1174-1176, Q4). `MMF_MULTIPROCESS` is set at fork time by
  `copy_oom_score_adj()` (fork.c:1949-1966) for a child created with `CLONE_VM` but without
  `CLONE_THREAD`/`CLONE_VFORK`, which also copies both values from the parent (:1963-1964); the
  ordinary fork path inherits them in `copy_signal()` (fork.c:1768-1769) from a `kmem_cache_zalloc`
  struct (fork.c:1728). Net effect a reader can rely on: `oom_score_adj` is per thread group, is
  inherited across fork, and is additionally mirrored across processes that deliberately share an
  mm.

## Scope boundary for the entry

- This row grounds: the `oom_score` formula, its `[0, 2000]` exported range and the `-1000` = 0
  special case; the `-1000..1000` write range and file modes; the `oom_score_adj_min` /
  `CAP_SYS_RESOURCE` floor; thread-group home, fork inheritance and mm-sharer propagation.
- It does **not** ground: the `oom_badness` body or the victim-selection loop (S003,
  `mm/oom_kill.c`), cgroup `memory.oom.group` (S002), earlyoom's use of any of this, or this host's
  actual per-process values (other round-27 seats).

## Remaining unknowns

- Whether Arch's 7.2.11-arch1-1 build patches this path: not checked against the distro source
  tree; [INFERENCE] upstream logic, since no Arch delta is known for `fs/proc/base.c`.
- The host's live `oom_score` and `oom_score_adj` values and the fleet's unit-level
  `OOMScoreAdjust=`: out of this seat's scope (unit and live-value seats).
- Exact `oom_score` of a process at a given moment also depends on `totalpages` (RAM + swap) and on
  the OOM constraint in force; this row does not pin numeric examples.
- `oom.h` and `fork.c` were fetched from kernel.org cgit, not `raw.githubusercontent.com` (429).
  The tag is the same, and byte identity is **observed** for `oom.h` and `base.c`: the sibling seats
  fetched those paths from GitHub raw at the same tag and recorded the same sha256 —
  `MoriR27.SrcKernelOomBadness` for `oom.h` (`6b00b4d0…`) and `MoriR27.CriticInheritProbe` for
  `fs/proc/base.c` (`cef1a2cf…`). `fork.c` has no second copy in this wave: [INFERENCE]
  byte-identical, since cgit plain serves the blob for the tag.

## Ready to paste — new row S127

Replace `S127` with the lane's next free id if a sibling claimed it first (S127 was free when I
read `corpus/SOURCES.md`; highest id there was S126 at :132).

```
| S127 | Linux fs/proc/base.c, include/uapi/linux/oom.h and kernel/fork.c at v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c ; https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/uapi/linux/oom.h?h=v7.2 ; https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/kernel/fork.c?h=v7.2 | code | A | the /proc/<pid>/oom_score and /proc/<pid>/oom_score_adj files at the v7.2 tag and the two facts they depend on: how oom_score is rescaled from oom_badness and why -1000 reads 0, the -1000..1000 write range and the file modes, the oom_score_adj_min floor with CAP_SYS_RESOURCE, and how a write reaches other processes that share the mm (fork copy, MMF_MULTIPROCESS); not the oom_badness body or the kill loop (mm/oom_kill.c, S003), not cgroup memory.oom.group (S002), not this host's per-process values or earlyoom's use of them | fs/proc/base.c:583-599 (proc_oom_score), :586 (totalram_pages() + total_swap_pages), :590 (oom_badness call), :592-597 (LONG_MIN skip, (1000 + badness*1000/totalpages)*2/3, exported [0, 2000]), :1106-1186 (__set_oom_adj), :1118-1122 (legacy path vs current value), :1131-1135 (oom_score_adj_min floor, -EACCES without CAP_SYS_RESOURCE), :1143-1153 (MMF_MULTIPROCESS mm grab), :1155-1158 (assignment, min update, tracepoint), :1164-1177 (mm-sharer propagation, kernel-thread and global-init skip), :1242-1254 (read), :1275-1279 (range check, -EINVAL), :3351-3353 (pid entries) and :3706-3708 (task/tid entries), modes S_IRUGO (read-only oom_score) and S_IRUGO plus S_IWUSR (owner-writable oom_score_adj); include/uapi/linux/oom.h:9-10 (OOM_SCORE_ADJ_MIN (-1000), OOM_SCORE_ADJ_MAX 1000); kernel/fork.c:1728 (zalloc signal struct), :1768-1769 (inheritance in copy_signal), :1949-1966 (copy_oom_score_adj sets MMF_MULTIPROCESS, copies both values); tag v7.2; base.c HTTP 200, 98,196 B, sha256 cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6; oom.h HTTP 200, 526 B, sha256 6b00b4d0648bcdc9d6be7ea8a33b8e6b842c063e7b2b71bdabd757de773896ae; fork.c HTTP 200, 85,725 B, sha256 359882ea981b58f5289293e5644f7c0085a8350e4f1937f39dcb94ae1cd0dd1d | A task's oom_score is (1000 + badness*1000/totalpages)*2/3, 0 when the task is unkillable or oom_score_adj is -1000, and a writer may set oom_score_adj only within -1000..1000, below oom_score_adj_min only with CAP_SYS_RESOURCE, with the write copied to every non-thread process sharing the mm. | mined | 2026-10-22 | on-release | corpus/knowledge/oom-victim-selection-r27.md |
```

## Overlap with sibling seats in this wave (read-only observation, no coordination sent)

- `MoriR27.SrcKernelOomBadness` already proposes the S003 anchor for `mm/oom_kill.c` including
  `oom_badness` at 199-237, so **this seat adds nothing to S003**; my cgit reading of
  `mm/oom_kill.c` (sha256 `452f1348…`, identical to their GitHub-raw copy) was only used to confirm
  what `badness == LONG_MIN` means for Q1. Use their S003 anchor, not a second one.
- The same seat drafted an *optional* thin `fs/proc/base.c` row (:583-599 only) and an *optional*
  `include/uapi/linux/oom.h` row. The row above supersedes the base.c draft — the entry needs one
  base.c row, not two, and this one adds the write path, floor, mm-sharing and file modes.
- If the L1 lands the sibling's `oom.h` row, **trim this row's `oom.h` URL and its `:9-10` anchor
  clause**; the `-1000..1000` range in the `teaches` cell then rests on that row, and nothing else
  in this row changes. If it does not land, keep them: the write-path range check at
  `base.c:1275-1279` compares against constants defined only in that header.
- Observed duplication check (run, not inferred): `grep -c 'fs/proc/base\.c' .ufo/waves/round-27/w1/*.md`
  returns 7 in this file, 7 in `CriticInheritProbe.md`, 4 in `SrcKernelOomBadness.md`, 4 in
  `SrcManProcOomScoreAdj.md`, 1 in `ScoutTsukuroiMemPressure.md`; `SrcProcRstOom.md` matches the
  looser `base\.c|kernel/fork\.c` pattern without naming the file.
- `MoriR27.SrcManProcOomScoreAdj` proposes its **own S127** for a man-pages row whose `source` cell
  lists `fs/proc/base.c` as URL 3 and whose scope is "the documented contract ... plus the v7.2
  kernel code that enforces it" (`SrcManProcOomScoreAdj.md:110-114`). That overlaps this row's
  ground. Recommended split for the L1: keep the man-pages row as the `docs` row for the written
  contract **without** the `base.c` URL and without base.c line anchors, and keep one `code` row on
  `base.c` — this one, because it carries the write path, the `oom_score_adj_min` floor, the
  mm-sharer propagation, the fork copy and the entry modes. If the L1 instead merges everything
  into the man-pages row, delete this row and move its `anchor` clauses there; do not land both with
  the base.c anchors split across them.
- Ids: the man-pages row keeps `S127` if it lands first; this row then takes the next free id. C1's
  counter accepts any id >= S127, so the order does not affect the claim.

## Checks not run by this seat (for the L1)

- No build, no test, no counter run: C1's counter (`count-c1.sh`) belongs to the L1 after landing.
- Report line count (`wc -l` on this file) and the lane retention scan were not run here by design;
  this seat wrote only this report file.
- No tool was installed or upgraded for this task; `curl` (system) and the read tool were enough.
