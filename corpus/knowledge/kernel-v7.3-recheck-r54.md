# Linux v7.3 recheck of the remaining v7.2-pinned claim rows (round 54)

source: S515 — Linux mm/memcontrol.c at tag v7.3 — https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/mm/memcontrol.c?h=v7.3 — copy `corpus/evidence/sources-r54/memcontrol.c.v7.3`; S516 — mm/oom_kill.c at v7.3 — copy `sources-r54/oom_kill.c.v7.3`
source: S517 — lib/percpu_counter.c at v7.3 — copy `sources-r54/percpu_counter.c.v7.3`; S518 — include/linux/percpu_counter.h at v7.3 — copy `sources-r54/percpu_counter.h.v7.3`; S519 — include/uapi/asm-generic/errno.h at v7.3 — copy `sources-r54/errno.h.v7.3`
source: S520 — rendered Control Group v2 page 7.3.0 — https://docs.kernel.org/7.3/admin-guide/cgroup-v2.html — copy `sources-r54/cgroup-v2.7.3.html`; S508 — mm/util.c at v7.3 and S514 — mm/mm_init.c at v7.3 (round-53 rows, copies under `corpus/evidence/sources-r53/`), all code rows tier A from git.kernel.org cgit, opened 2026-10-27 (S508, S514: 2026-10-26)
verified-at: 2026-10-27
recheck: on-release — `python3 .ufo/waves/round-54/count-c1.py <rev>`
coverage-map: freshness of the claim tables of `oom-memcg-stat-r50.md`, `commit-runway-read-r53.md` and `quota-observability-r48.md`
author: MoriR54 (L1) from `.ufo/waves/round-54/controls/c1data.py` (status and line derived from the committed copies); dispositions are `holds` pending the wave's RECHECK voters (`.ufo/waves/round-54/w1/Mo54Rc*.md`)

## What this ledger is

Round 53 answered the v7.3 release trigger for 46 claim rows of two entries (`kernel-v7.3-recheck-r53.md`). It left
every other claim row that pins Linux tag v7.2 at v7.2. This ledger takes all of them: the counter's `--scope` at
the entering tip `39dcf4d7` lists 31 rows (`.ufo/waves/round-54/evidence/c1-scope.txt`) — 22 of
`oom-memcg-stat-r50.md`, 8 of `commit-runway-read-r53.md`, 1 of `quota-observability-r48.md`. One row per claim
hash: `status` is the counter's derivation (`held` when the v7.2 quote still occurs, whitespace collapsed, in the
v7.3 copy), `line` is a v7.3 line on which the quote begins, `disposition` is whether the claim still holds at v7.3,
judged by the voters.

## Ledger

| h | entry | status | source | line | quote | disposition |
|---|---|---|---|---|---|---|
| 4aab78fbca9c | `corpus/knowledge/commit-runway-read-r53.md` | held | S518 | 121 | `s64 ret = READ_ONCE(fbc->count); if (ret >= 0) return ret; return 0;` | holds |
| c8fb3a4fb56f | `corpus/knowledge/commit-runway-read-r53.md` | held | S517 | 100 | `if (unlikely(abs(count + amount) >= batch)) { raw_spin_lock_irqsave(&fbc->lock, flags);` | holds |
| 0d09a65619e5 | `corpus/knowledge/commit-runway-read-r53.md` | held | S514 | 198 | `s32 nr = num_present_cpus(); s32 batch = max_t(s32, nr*2, 32);` | holds |
| 47887dc7067f | `corpus/knowledge/commit-runway-read-r53.md` | held | S514 | 203 | `For policy OVERCOMMIT_NEVER, set batch size to 0.4% of * (total memory/#cpus), and lift it to 25% for other policies` | holds |
| da4075a0131e | `corpus/knowledge/commit-runway-read-r53.md` | held | S514 | 208 | `if (overcommit_policy == OVERCOMMIT_NEVER) memsized_batch = min_t(u64, ram_pages/nr/256, INT_MAX);` | holds |
| 196504e1a96c | `corpus/knowledge/commit-runway-read-r53.md` | held | S508 | 820 | `1. changing the batch * 2. sync percpu count on each CPU * 3. switch the policy` | holds |
| 3b7ff65291be | `corpus/knowledge/commit-runway-read-r53.md` | held | S508 | 937 | `unsigned long vm_memory_committed(void) { return percpu_counter_sum_positive(&vm_committed_as); }` | holds |
| 646b97a23371 | `corpus/knowledge/commit-runway-read-r53.md` | held | S508 | 994 | `if (percpu_counter_read_positive(&vm_committed_as) < allowed) return 0;` | holds |
| 07524a78c749 | `corpus/knowledge/oom-memcg-stat-r50.md` | held | S520 | 1225 | `All memory amounts are in bytes. If a value which is not aligned to PAGE_SIZE is written,` | holds |
| 202158f50bb3 | `corpus/knowledge/oom-memcg-stat-r50.md` | held | S520 | 1437 | `anon Amount of memory used in anonymous mappings such as brk() , sbrk() , and mmap(MAP_ANONYMOUS).` | holds |
| 41496ae6cbe1 | `corpus/knowledge/oom-memcg-stat-r50.md` | held | S520 | 1409 | `The number of processes belonging to this cgroup killed by any kind of OOM killer.` | holds |
| 460b0cafc999 | `corpus/knowledge/oom-memcg-stat-r50.md` | held | S520 | 1430 | `Don’t rely on items remaining in a fixed position; use the keys to look up specific values!` | holds |
| 51390e34b4d7 | `corpus/knowledge/oom-memcg-stat-r50.md` | held | S520 | 1465 | `shmem Amount of cached filesystem data that is swap-backed, such as tmpfs, shm segments, shared anonymous mmap()s` | holds |
| ed03d041e844 | `corpus/knowledge/oom-memcg-stat-r50.md` | held | S520 | 1446 | `kernel (npn) Amount of total kernel memory, including (kernel_stack, pagetables, percpu, vmalloc, slab) in addition to other kernel memory use cases.` | holds |
| fd3728bdc6d6 | `corpus/knowledge/oom-memcg-stat-r50.md` | held | S520 | 1443 | `file Amount of memory used to cache filesystem data, including tmpfs and shared memory.` | holds |
| 0145725d3c6c | `corpus/knowledge/oom-memcg-stat-r50.md` | held | S515 | 4997 | `seq_buf_init(&s, buf, SEQ_BUF_SIZE); memory_stat_format(memcg, &s); seq_puts(m, buf);` | holds |
| 16a3733a5002 | `corpus/knowledge/oom-memcg-stat-r50.md` | held | S515 | 1872 | `seq_buf_init(&s, buf, SEQ_BUF_SIZE); memory_stat_format(memcg, &s); seq_buf_do_printk(&s, KERN_INFO);` | holds |
| 26b9666a61be | `corpus/knowledge/oom-memcg-stat-r50.md` | held | S515 | 1824 | `if (p) { pr_cont(",task_memcg="); pr_cont_cgroup_path(task_cgroup(p, memory_cgrp_id)); }` | holds |
| 90f96cf997c2 | `corpus/knowledge/oom-memcg-stat-r50.md` | held | S515 | 1845 | `if (cgroup_subsys_on_dfl(memory_cgrp_subsys)) memory_failcnt = atomic_long_read(&memcg->memory_events[MEMCG_MAX]); else memory_failcnt = memcg->memory.failcnt;` | holds |
| a4965056de62 | `corpus/knowledge/oom-memcg-stat-r50.md` | held | S515 | 1854 | `pr_info("swap: usage %llukB, limit %llukB, failcnt %lu\n",` | holds |
| adf25120cfe8 | `corpus/knowledge/oom-memcg-stat-r50.md` | held | S515 | 2041 | `pr_info("Tasks in "); pr_cont_cgroup_path(memcg->css.cgroup); pr_cont(" are going to be killed due to memory.oom.group set\n");` | holds |
| de58513701cb | `corpus/knowledge/oom-memcg-stat-r50.md` | held | S515 | 1819 | `if (memcg) { pr_cont(",oom_memcg="); pr_cont_cgroup_path(memcg->css.cgroup); } else pr_cont(",global_oom");` | holds |
| f5626c899cea | `corpus/knowledge/oom-memcg-stat-r50.md` | held | S515 | 1850 | `pr_info("memory: usage %llukB, limit %llukB, failcnt %lu\n",` | holds |
| 0aa4618b2166 | `corpus/knowledge/oom-memcg-stat-r50.md` | held | S516 | 446 | `/* one line summary of the oom killer context. */ pr_info("oom-kill:constraint=%s,nodemask=%*pbl", oom_constraint_text[oc->constraint], nodemask_pr_args(oc->nodemask));` | holds |
| 3a75d41492ad | `corpus/knowledge/oom-memcg-stat-r50.md` | held | S516 | 945 | `pr_err("%s: Killed process %d (%s) total-vm:%lukB, anon-rss:%lukB, file-rss:%lukB, shmem-rss:%lukB, UID:%u pgtables:%lukB oom_score_adj:%d\n",` | holds |
| 53d8f38c2827 | `corpus/knowledge/oom-memcg-stat-r50.md` | held | S516 | 1169 | `oom_kill_process(oc, !is_memcg_oom(oc) ? "Out of memory" : "Memory cgroup out of memory");` | holds |
| b962596a058b | `corpus/knowledge/oom-memcg-stat-r50.md` | held | S516 | 1030 | `if (__ratelimit(&oom_rs)) { dump_header(oc); dump_oom_victim(oc, victim); }` | holds |
| d6bf02678216 | `corpus/knowledge/oom-memcg-stat-r50.md` | held | S516 | 424 | `pr_info("Tasks state (memory values in pages):\n"); pr_info("[ pid ] uid tgid total_vm rss rss_anon rss_file rss_shmem pgtables_bytes swapents oom_score_adj name\n");` | holds |
| e4e93c6a050c | `corpus/knowledge/oom-memcg-stat-r50.md` | held | S516 | 934 | `/* Raise event before sending signal: task reaper must see this */ count_vm_event(OOM_KILL); memcg_memory_event_mm(mm, MEMCG_OOM_KILL);` | holds |
| fdc2273230e1 | `corpus/knowledge/oom-memcg-stat-r50.md` | held | S516 | 465 | `if (is_memcg_oom(oc)) mem_cgroup_print_oom_meminfo(oc->memcg); else { __show_mem(SHOW_MEM_FILTER_NODES, oc->nodemask, gfp_zone(oc->gfp_mask));` | holds |
| 687e03745cd9 | `corpus/knowledge/quota-observability-r48.md` | held | S519 | 107 | `#define EDQUOT 122 /* Quota exceeded */` | holds |

## Where the quotes moved (v7.2 copy line → v7.3 copy line)

All 31 v7.2 quotes occur in the v7.3 copies, read whitespace-collapsed (and, for the rendered page, with tags read as a space and entities decoded — none of its seven quotes is a raw byte substring of the HTML). Four of the eight files did not change at all between the tags
(`mm/oom_kill.c`, `lib/percpu_counter.c`, `include/linux/percpu_counter.h`, `include/uapi/asm-generic/errno.h`:
`diff` of the committed copies prints nothing; errno.h has the same sha256 as S481's copy). `mm/util.c` changed 14
lines, none at the three quoted lines. Three files moved the quoted lines: `mm/memcontrol.c` (258 changed lines;
the OOM report block +45 lines, the `memory.stat` reader +84), `mm/mm_init.c` (the `mm_compute_batch` block +4)
and the rendered cgroup-v2 page (+31 lines: 8 lines of new navigation captions and 23 lines of new page content above
the quoted block — the note that the five CFS bandwidth stats are non-hierarchical and the `cgroup_set_bandwidth` /
`cgroup_set_idle` sentences added to `cpu.max`, `cpu.max.burst` and `cpu.idle`; `Mo54ExecLineArm` diff opcodes).
The S490-backed memcontrol prose anchors in `oom-memcg-stat-r50.md` are v7.2 positions; their v7.3 locations are
off by the `moved` column. S491's `oom_kill.c` anchors did not move. The v7.2 lines below are from committed copies
(`sources-r50/`, `sources-r52/util.c.v7.2`, `sources-r53/*.v7.2`, `sources-r48/errno.h`).

| h | path | v7.2 line | v7.3 line | moved |
|---|---|---|---|---|
| 4aab78fbca9c | include/linux/percpu_counter.h | 121 | 121 | +0 |
| c8fb3a4fb56f | lib/percpu_counter.c | 100 | 100 | +0 |
| 0d09a65619e5 | mm/mm_init.c | 194 | 198 | +4 |
| 47887dc7067f | mm/mm_init.c | 199 | 203 | +4 |
| da4075a0131e | mm/mm_init.c | 204 | 208 | +4 |
| 196504e1a96c | mm/util.c | 820 | 820 | +0 |
| 3b7ff65291be | mm/util.c | 937 | 937 | +0 |
| 646b97a23371 | mm/util.c | 994 | 994 | +0 |
| 07524a78c749 | docs.kernel.org/<ver>/admin-guide/cgroup-v2.html | 1194 | 1225 | +31 |
| 202158f50bb3 | docs.kernel.org/<ver>/admin-guide/cgroup-v2.html | 1406 | 1437 | +31 |
| 41496ae6cbe1 | docs.kernel.org/<ver>/admin-guide/cgroup-v2.html | 1378 | 1409 | +31 |
| 460b0cafc999 | docs.kernel.org/<ver>/admin-guide/cgroup-v2.html | 1399,1605 | 1430,1636 | +31 |
| 51390e34b4d7 | docs.kernel.org/<ver>/admin-guide/cgroup-v2.html | 1434 | 1465 | +31 |
| ed03d041e844 | docs.kernel.org/<ver>/admin-guide/cgroup-v2.html | 1415 | 1446 | +31 |
| fd3728bdc6d6 | docs.kernel.org/<ver>/admin-guide/cgroup-v2.html | 1412 | 1443 | +31 |
| 0145725d3c6c | mm/memcontrol.c | 4913 | 4997 | +84 |
| 16a3733a5002 | mm/memcontrol.c | 1827 | 1872 | +45 |
| 26b9666a61be | mm/memcontrol.c | 1779 | 1824 | +45 |
| 90f96cf997c2 | mm/memcontrol.c | 1800 | 1845 | +45 |
| a4965056de62 | mm/memcontrol.c | 1809 | 1854 | +45 |
| adf25120cfe8 | mm/memcontrol.c | 1996 | 2041 | +45 |
| de58513701cb | mm/memcontrol.c | 1774 | 1819 | +45 |
| f5626c899cea | mm/memcontrol.c | 1805 | 1850 | +45 |
| 0aa4618b2166 | mm/oom_kill.c | 446 | 446 | +0 |
| 3a75d41492ad | mm/oom_kill.c | 945 | 945 | +0 |
| 53d8f38c2827 | mm/oom_kill.c | 1169 | 1169 | +0 |
| b962596a058b | mm/oom_kill.c | 1030 | 1030 | +0 |
| d6bf02678216 | mm/oom_kill.c | 424 | 424 | +0 |
| e4e93c6a050c | mm/oom_kill.c | 934 | 934 | +0 |
| fdc2273230e1 | mm/oom_kill.c | 465 | 465 | +0 |
| 687e03745cd9 | include/uapi/asm-generic/errno.h | 107 | 107 | +0 |

## Release drift near these rows that the claim tables do not hold

The rendered cgroup-v2 page changed in 32 places between 7.2.0 and 7.3.0 (word-level diff of the tag-stripped
text). None touches a quoted row: the `memory.stat` keys, units and the `oom_kill` event text are unchanged. Three
changes sit on mori ground and are recorded here, not as claims: `memory.pressure` and `io.pressure` are now
documented "read-write" (7.2: "read-only" — the files always accepted PSI trigger writes, round 24's F8); the
`io.stat` throttle field is now `delay_nsec` in nanoseconds (7.2: `delay`, microseconds) — an io observer keyed on
the old name or unit reads wrong; and the CFS bandwidth stats in `cpu.stat` are now documented as non-hierarchical.
They are leads for the entries that own those surfaces (`corpus/SOURCES.md` `## Leads (unopened)`).
