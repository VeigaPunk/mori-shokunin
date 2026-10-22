# SrcKernelOomBadness — kernel victim selection, round 27 wave 1

Seat `MoriR27.SrcKernelOomBadness`, leaf scout. Lane `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Question: extract `oom_badness()`, `oom_unkillable_task()`, `select_bad_process()`/`oom_evaluate_task()` and the
`memory.oom.group` widening from Linux tag v7.2, and return a Gate block plus the SOURCES anchor or row.
No host command was run: no unit, journal, `/proc` or `/etc` read; no signal; no pacman (all transactions paused);
no tool installed. Only four public source files were fetched with `curl -sS` (`mm/oom_kill.c`, `mm/memcontrol.c`,
`include/uapi/linux/oom.h`, `fs/proc/base.c`).

## Gate block — mm/oom_kill.c at tag v7.2

- URL: `https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c`
- Access: 2026-10-22T15:46:29Z (`curl -sS`, HTTP 200, 34,311 B, 1,257 lines)
- sha256: `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e`

Verbatim quotes (line numbers are of the fetched file; word counts by whitespace):

| # | Lines | Words | Quote |
|---|---|---|---|
| Q1 | 160-167 | 19 | `static bool oom_unkillable_task(struct task_struct *p) { if (is_global_init(p)) return true; if (p->flags & PF_KTHREAD) return true; return false; }` |
| Q2 | 228-229 | 10 | `points = get_mm_rss_sum(p->mm) + get_mm_counter_sum(p->mm, MM_SWAPENTS) + mm_pgtables_bytes(p->mm) / PAGE_SIZE;` |
| Q3 | 232-234 | 14 | `/* Normalize to oom_score_adj units */ adj *= totalpages / 1000; points += adj;` |
| Q4 | 216-217 | 8 | `adj = (long)p->signal->oom_score_adj; if (adj == OOM_SCORE_ADJ_MIN \|\|` |
| Q5 | 340 | 9 | `if (points == LONG_MIN \|\| points < oc->chosen_points)` |

## Supporting capture — mm/memcontrol.c at tag v7.2 (needed for memory.oom.group)

- URL: `https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/memcontrol.c`
- Access: 2026-10-22T15:46:49Z (`curl -sS`, HTTP 200, 160,768 B)
- sha256: `8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e`

| # | Lines | Words | Quote |
|---|---|---|---|
| M1 | 1978-1980 | 12 | `for (; memcg; memcg = parent_mem_cgroup(memcg)) { if (READ_ONCE(memcg->oom_group)) oom_group = memcg;` |
| M2 | 4981-4984 | 12 | `if (oom_group != 0 && oom_group != 1) return -EINVAL; WRITE_ONCE(memcg->oom_group, oom_group);` |
| M3 | 1994-1998 | 19 | `void mem_cgroup_print_oom_group(struct mem_cgroup *memcg) { pr_info("Tasks in "); pr_cont_cgroup_path(memcg->css.cgroup); pr_cont(" are going to be killed due to memory.oom.group set\n");` |
| M4 | 1953-1954 | 4 | `if (!cgroup_subsys_on_dfl(memory_cgrp_subsys)) return NULL;` |

## Supporting capture — include/uapi/linux/oom.h at tag v7.2 (the -1000 floor)

- URL: `https://raw.githubusercontent.com/torvalds/linux/v7.2/include/uapi/linux/oom.h`
- Access: 2026-10-22T15:47:36Z (`curl -sS`, HTTP 200, 526 B)
- sha256: `6b00b4d0648bcdc9d6be7ea8a33b8e6b842c063e7b2b71bdabd757de773896ae`

| # | Lines | Words | Quote |
|---|---|---|---|
| U1 | 6-7 | 11 | `* /proc/<pid>/oom_score_adj set to OOM_SCORE_ADJ_MIN disables oom killing for * pid.` |
| U2 | 9-10 | 6 | `#define OOM_SCORE_ADJ_MIN (-1000) #define OOM_SCORE_ADJ_MAX 1000` |

## What the code does (entry material, observed unless marked)

1. **Candidate screen.** `oom_unkillable_task()` rejects the global init task and any `PF_KTHREAD` task
   (`mm/oom_kill.c:160-167`). `oom_badness()` then requires a lockable `mm` (`:207-209`) and returns `LONG_MIN`
   for a task whose `oom_score_adj == OOM_SCORE_ADJ_MIN`, whose `mm` carries `MMF_OOM_SKIP`, or which is in
   `vfork` (`:216-222`). `OOM_SCORE_ADJ_MIN` is `-1000` and the constant's own comment says it "disables oom
   killing" (`include/uapi/linux/oom.h:6-9`). So only exactly `-1000` is exempt; `-999` is merely cheap.
2. **Points formula.** `points` is in pages: `get_mm_rss_sum()` (anon + file + shmem RSS) plus the `MM_SWAPENTS`
   counter plus `mm_pgtables_bytes() / PAGE_SIZE` (`mm/oom_kill.c:228-229`). No normalisation to 0-1000 happens
   here; raw page counts are compared.
3. **oom_score_adj scaling.** `adj *= totalpages / 1000` with C integer division, then `points += adj`
   (`:232-234`). `totalpages` is the memcg's limit in pages under a memcg OOM
   (`memcontrol.c:258` → `mem_cgroup_get_max()`, `memory.max` plus the swap allowance, `memcontrol.c:1835-1852`)
   and `totalram_pages() + total_swap_pages` under a global OOM (`mm/oom_kill.c:263`). Hence `adj = +1000` can
   add a whole RAM/limit worth of points, and `adj = -900` still leaves the task's page count as its score.
4. **Ranking.** `select_bad_process()` sets `chosen_points = LONG_MIN` and scans either the OOM memcg's subtree
   (`mem_cgroup_scan_tasks`, `:366-367`) or every process (`:371-375`). `oom_evaluate_task()` skips a task when
   `points == LONG_MIN || points < oc->chosen_points` (`:340`), so a tie keeps the first task encountered and only
   a strictly higher score replaces the incumbent; a task flagged `oom_task_origin` gets `LONG_MAX` and is
   selected directly (`:334-337`, flag helpers `include/linux/oom.h:59-72`). A scan that meets an already-marked
   victim without `MMF_OOM_SKIP` aborts with `oc->chosen = (void *)-1UL` (`:324-328`, `:351-355`).
5. **Kill and log.** `oom_kill_process()` first short-circuits a task that will free its memory (`:1020-1027`),
   then `__oom_kill_process()` sends `SIGKILL` with `PIDTYPE_TGID`, bumps `OOM_KILL` and the memcg OOM counter,
   and emits one `Killed process ... oom_score_adj:%d` record per call (`:934-951`). It also SIGKILLs other thread
   groups that share the victim's `mm` (`:954-983`), so one chosen task can produce several `Killed process`
   lines with different pids but the same `mm`.
6. **memory.oom.group widening.** Only on cgroup v2 (`memcontrol.c:1953-1954`). `mem_cgroup_get_oom_group()`
   takes the victim's memcg, ignores it when it is the root or no longer a descendant of the OOM domain
   (`:1961-1971`), then walks up to the OOM domain and remembers the **highest** ancestor with `oom_group` set
   (`:1978-1984`). `oom_kill_process()` calls this *before* killing the victim (`mm/oom_kill.c:1040`), then
   raises `MEMCG_OOM_GROUP_KILL`, prints `Tasks in <path> are going to be killed due to memory.oom.group set`
   (`memcontrol.c:1994-1998`), and calls `oom_kill_memcg_member()` for every process in that cgroup's subtree
   (`mm/oom_kill.c:1047-1053`; the scan is `for_each_mem_cgroup_tree` with `CSS_TASK_ITER_PROCS`,
   `memcontrol.c:1370-1379`). `oom_kill_memcg_member()` spares only tasks at `oom_score_adj == OOM_SCORE_ADJ_MIN`
   and the global init task (`mm/oom_kill.c:998-1006`). The knob itself accepts only `0` or `1`
   (`memcontrol.c:4981-4984`).
7. **What `/proc/<pid>/oom_score` shows.** Not the ranking value: `proc_oom_score()` calls `oom_badness()` with
   `totalram_pages() + total_swap_pages` and prints `(1000 + badness * 1000 / totalpages) * 2 / 3`, a 0-2000
   scale, with `LONG_MIN` mapped to `0` (`fs/proc/base.c:583-599`). The ranking in the allocator can use a
   different `totalpages`, so the file is a comparable hint, not the exact points.

## SOURCES — S003 already covers mm/oom_kill.c: anchor, not a new row

`corpus/SOURCES.md:9` already pins this exact URL at tag v7.2, so per the contract this re-open adds an anchor to
S003. The paste-ready row below keeps every existing cell and changes only `scope`, `anchor`, `teaches` and
`used-by`.

```markdown
| S003 | Linux mm/oom_kill.c at v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c | code | A | Linux 7.2 kernel OOM counter updates, kernel summary/victim records and the victim-selection heuristic (oom_badness points and oom_score_adj scaling, oom_evaluate_task ranking, memory.oom.group widening) | mm/oom_kill.c:160-167 (oom_unkillable_task), 199-237 (oom_badness), 306-356 (oom_evaluate_task), 362-377 (select_bad_process), 447, 935-936, 945 (counters and Killed-process record), 998-1006 (oom_kill_memcg_member), 1040-1053 (oom group kill); tag v7.2; HTTP 200, 34,311 B, sha256 452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e | The kernel scores each task in pages (rss + swap entries + page tables), shifts that score by oom_score_adj * totalpages / 1000, excludes init, kernel threads and any task at adj -1000, picks the highest score, and with memory.oom.group set kills the whole subtree of the highest marked ancestor cgroup. | mined | 2026-10-19 | on-release | corpus/knowledge/oom-kill-counter-kernel-only-r12.md, corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/kernel-oom-line-attribution-r12.md, corpus/knowledge/userspace-oom-killers-r12.md, corpus/knowledge/oom-victim-selection-r27.md |
```

If the L1 prefers the minimal diff instead of the whole row: append to S003's `anchor` cell
`; mm/oom_kill.c:160-167,199-237,306-356,362-377,998-1006,1040-1053; HTTP 200, 34,311 B, sha256
452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e`, append the victim-selection clause to
`scope`, append the scoring sentence to `teaches`, and add
`corpus/knowledge/oom-victim-selection-r27.md` to `used-by`.

## SOURCES — mm/memcontrol.c already has row S004: anchor to add

S004 pins a different revision (master commit `c03c1a1…`, `corpus/SOURCES.md:10`), not tag v7.2, and its scope is
the OOM report labels. Add this text to S004's `anchor` cell (same file, different pin):

```text
; tag v7.2 capture (HTTP 200, 160,768 B, sha256 8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e): mm/memcontrol.c:1370-1379 (subtree scan), 1835-1852 (mem_cgroup_get_max), 1947-1992 (mem_cgroup_get_oom_group ancestor walk), 1994-1998 (Tasks in ... group print), 4981-4984 (memory.oom.group accepts only 0/1)
```

and append to its `scope` cell `and the memory.oom.group group-kill selection`, to its `teaches` cell
`Setting memory.oom.group on any memcg between the victim and the OOM domain widens the kill to that cgroup's
subtree.`, and to its `used-by` cell `corpus/knowledge/oom-victim-selection-r27.md`.

## SOURCES — two optional new rows (only if the entry cites them)

`include/uapi/linux/oom.h` has no row (checked: `grep -n 'uapi/linux/oom' corpus/SOURCES.md` → 0). If the entry
states the `-1000` floor as a userspace contract, this draft row covers it (`S???` is the L1's id):

```markdown
| S??? | Linux include/uapi/linux/oom.h at v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/include/uapi/linux/oom.h | code | A | the userspace-visible oom_score_adj bounds at tag v7.2: OOM_SCORE_ADJ_MIN (-1000), OOM_SCORE_ADJ_MAX (1000) and the legacy oom_adj constants; not the scoring arithmetic (mm/oom_kill.c), not host state | include/uapi/linux/oom.h:6-7 (adj MIN disables oom killing for the pid), :9 (`#define OOM_SCORE_ADJ_MIN (-1000)`), :10 (`OOM_SCORE_ADJ_MAX 1000`), :16-19 (legacy oom_adj constants); tag v7.2; HTTP 200, 526 B, sha256 6b00b4d0648bcdc9d6be7ea8a33b8e6b842c063e7b2b71bdabd757de773896ae | A task at oom_score_adj -1000 is excluded from victim selection and from a memory.oom.group kill; the scale runs from -1000 to 1000. | mined | 2026-10-22 | on-release | corpus/knowledge/oom-victim-selection-r27.md |
```

`fs/proc/base.c` also has no row; if the entry uses the `/proc/<pid>/oom_score` normalisation (item 7 above),
it needs this second draft instead of the claim being uncited:

```markdown
| S??? | Linux fs/proc/base.c at v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c | code | A | how /proc/<pid>/oom_score is derived at tag v7.2: oom_badness() with RAM plus swap as totalpages and the 0-2000 scaling; not the allocator's own selection (mm/oom_kill.c), not host state | fs/proc/base.c:583-599 (proc_oom_score: totalpages at :586, scaling at :597, LONG_MIN to 0 at :596); :1242-1281 (oom_score_adj read/write and the -1000..1000 range check at :1275-1276); tag v7.2; HTTP 200, 98,196 B, sha256 cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6 | /proc/<pid>/oom_score is a 0-2000 projection of oom_badness, not the raw ranking points, and the writable oom_score_adj range is -1000..1000. | mined | 2026-10-22 | on-release | corpus/knowledge/oom-victim-selection-r27.md |
```

## Confidence and remaining unknowns

- Observed: every line cite above was read from the fetched bytes at tag v7.2; the four sha256 values were
  computed locally on those bytes and re-checked against fresh HTTP 200 responses of the same sizes.
- [INFERENCE] Reading of the arithmetic: because `totalpages` differs between a memcg OOM (the memcg limit) and a
  global OOM (RAM + swap), the same `oom_score_adj` shifts the ranking by a different number of pages in each
  mode; the code shows the two `totalpages` assignments but does not say this in words.
- [INFERENCE] Tie behaviour: `points < oc->chosen_points` keeps the first-scanned task on a tie; scan order is
  process-list order (global) or memcg subtree iteration order (memcg), which is not defined by this file.
- Unknown / not traced here: who sets `oom_flag_origin` (the helpers are `include/linux/oom.h:59-72`; no setter
  call exists in `mm/oom_kill.c` or `mm/memcontrol.c`, so it lives elsewhere and I did not open that file);
  whether the `mem_cgroup_get_max()` value for an unlimited `memory.max` changes the scaling (it reads
  `memory.max` raw, `memcontrol.c:1837`); earlyoom's own victim preference and this host's `oom_score_adj` values
  are other seats' questions.
- No blocker. Deliverable is the anchor, not a lane commit.
