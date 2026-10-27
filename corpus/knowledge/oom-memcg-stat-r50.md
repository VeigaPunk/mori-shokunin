# A memcg OOM prints its charge three ways: usage line, stats block, victim line

source: S489 — https://docs.kernel.org/7.2/admin-guide/cgroup-v2.html — docs, tier A, Control Group v2 documentation at kernel 7.2 (memory interface files, memory.events, memory.oom.group), opened 2026-10-26
source: S490 — https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/memcontrol.c — code, tier A, mm/memcontrol.c at tag v7.2 (the memcg OOM report path and the memory.stat formatter), opened 2026-10-26
source: S491 — https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c — code, tier A, mm/oom_kill.c at tag v7.2 (the victim record and the memcg-versus-global report split), opened 2026-10-26
verified-at: 2026-10-26
recheck: 90d — `for u in https://docs.kernel.org/7.2/admin-guide/cgroup-v2.html https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/memcontrol.c https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c; do curl -fsSL "$u" | sha256sum; done` -> 2d716cb798eacf8fbcf431b52697fbb8c5ed8ea9f58ac15b2b55351247c0bf34, 8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e, 452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e in that order (ran 2026-10-26; all three matched the committed copies)
coverage-map: FR1

mori attributes a kill at event time: which cgroup was over its charge, what that cgroup held, and which process died.
A memcg OOM prints all three in one burst: a usage/limit line, a `Memory cgroup stats for <path>:` block written by the
same formatter that writes memory.stat, and a per-victim `Killed process` line carrying the victim's own counters.
A global OOM prints a system-wide memory summary in place of that block and names no charged scope, so its burst cannot
place the charge in a cgroup.
That difference is the detection rule this entry serves: a stats block means the OOM was a memcg OOM, scoped to the
cgroup it names (the `oom-kill:` line then reads `constraint=CONSTRAINT_MEMCG`, `oom_kill.c.v7.2:239-244`). It does
not by itself mean a process was killed: `dump_header` also prints before a `panic_on_oom` panic and when no killable
process is found (`oom_kill.c.v7.2:1075`, `:1158`), so pair the block with a `Killed process` line before calling it a
kill.

## Claims

| claim | source | quote |
|---|---|---|
| Every memory amount the block prints is a byte count, and an unaligned write may be rounded up to a page when read back. | S489 | `All memory amounts are in bytes. If a value which is not aligned to PAGE_SIZE is written,` |
| The anon key counts anonymous mappings such as brk and MAP_ANONYMOUS, so it carries a process heap rather than page cache. | S489 | `anon Amount of memory used in anonymous mappings such as brk() , sbrk() , and mmap(MAP_ANONYMOUS).` |
| The file key includes tmpfs and shared memory, so a filesystem cache total also carries tmpfs pages. | S489 | `file Amount of memory used to cache filesystem data, including tmpfs and shared memory.` |
| The shmem key is the swap-backed part of that cached data, covering tmpfs, shm segments and shared anonymous mmap. | S489 | `shmem Amount of cached filesystem data that is swap-backed, such as tmpfs, shm segments, shared anonymous mmap()s` |
| The documentation defines the kernel key as a total that includes kernel_stack, pagetables, percpu, vmalloc and slab, each also printed under its own name. | S489 | `kernel (npn) Amount of total kernel memory, including (kernel_stack, pagetables, percpu, vmalloc, slab) in addition to other kernel memory use cases.` |
| A parser must match key names, because a newer kernel can insert a counter between existing lines. | S489 | `Don’t rely on items remaining in a fixed position; use the keys to look up specific values!` |
| The oom_kill field counts this cgroup's processes killed by an OOM kill, so on its own it cannot tell a memcg OOM from a global one. | S489 | `The number of processes belonging to this cgroup killed by any kind of OOM killer.` |
| The first usage line prints usage, limit and failcnt in that order, with usage and limit converted to kB. | S490 | `pr_info("memory: usage %llukB, limit %llukB, failcnt %lu\n",` |
| On a cgroup v2 hierarchy the printed failcnt comes from the MEMCG_MAX event counter, not from the page counter's own failcnt field. | S490 | `if (cgroup_subsys_on_dfl(memory_cgrp_subsys)) memory_failcnt = atomic_long_read(&memcg->memory_events[MEMCG_MAX]); else memory_failcnt = memcg->memory.failcnt;` |
| A second line reports swap usage, limit and failcnt on cgroup v2, printed before the stats block header. | S490 | `pr_info("swap: usage %llukB, limit %llukB, failcnt %lu\n",` |
| The stats block is filled by memory_stat_format and printed at KERN_INFO, so its lines reach the kernel log like any other message. | S490 | `seq_buf_init(&s, buf, SEQ_BUF_SIZE); memory_stat_format(memcg, &s); seq_buf_do_printk(&s, KERN_INFO);` |
| The memory.stat file is produced by the same memory_stat_format call, so the file and the block write their keys through one formatter. | S490 | `seq_buf_init(&s, buf, SEQ_BUF_SIZE); memory_stat_format(memcg, &s); seq_puts(m, buf);` |
| When no cgroup is named the OOM context prints global_oom instead of a cgroup path, marking a system-wide kill. | S490 | `if (memcg) { pr_cont(",oom_memcg="); pr_cont_cgroup_path(memcg->css.cgroup); } else pr_cont(",global_oom");` |
| A second label on the same line records the victim's own memory cgroup path, next to the OOM cgroup path. | S490 | `if (p) { pr_cont(",task_memcg="); pr_cont_cgroup_path(task_cgroup(p, memory_cgrp_id)); }` |
| A group kill announces itself with its own line naming every task in the cgroup as about to be killed. | S490 | `pr_info("Tasks in "); pr_cont_cgroup_path(memcg->css.cgroup); pr_cont(" are going to be killed due to memory.oom.group set\n");` |
| The Killed process line carries total-vm, anon-rss, file-rss and shmem-rss in kB, plus pgtables and oom_score_adj. | S491 | `pr_err("%s: Killed process %d (%s) total-vm:%lukB, anon-rss:%lukB, file-rss:%lukB, shmem-rss:%lukB, UID:%u pgtables:%lukB oom_score_adj:%d\n",` |
| The victim line's message prefix says whether the kill was global or a cgroup kill, choosing between two distinct strings. | S491 | `oom_kill_process(oc, !is_memcg_oom(oc) ? "Out of memory" : "Memory cgroup out of memory");` |
| A global OOM prints the system memory summary through __show_mem instead of the memcg stats block. | S491 | `if (is_memcg_oom(oc)) mem_cgroup_print_oom_meminfo(oc->memcg); else { __show_mem(SHOW_MEM_FILTER_NODES, oc->nodemask, gfp_zone(oc->gfp_mask));` |
| The summary header and the oom-kill context line print only when the rate limit allows, so a burst of kills can leave Killed process lines without them. | S491 | `if (__ratelimit(&oom_rs)) { dump_header(oc); dump_oom_victim(oc, victim); }` |
| The oom-kill context line records the constraint and nodemask before the victim name, pid and uid are appended. | S491 | `/* one line summary of the oom killer context. */ pr_info("oom-kill:constraint=%s,nodemask=%*pbl", oom_constraint_text[oc->constraint], nodemask_pr_args(oc->nodemask));` |
| The vm and memcg kill counters are incremented before the signal is sent, so the count predates the victim's death record. | S491 | `/* Raise event before sending signal: task reaper must see this */ count_vm_event(OOM_KILL); memcg_memory_event_mm(mm, MEMCG_OOM_KILL);` |
| The Tasks state table prints total_vm and rss in pages, unlike the kB victim line and the byte-valued charge keys of the stats block. | S491 | `pr_info("Tasks state (memory values in pages):\n"); pr_info("[ pid ] uid tgid total_vm rss rss_anon rss_file rss_shmem pgtables_bytes swapents oom_score_adj name\n");` |

## Reading rules

- Units are per line. The usage and swap lines print kB (their arguments go through `K()`, which turns a page count into
  kB; the macro is defined outside the three frozen copies), the `Killed process` fields print kB, the
  `Tasks state (memory values in pages)` table prints pages except its `pgtables_bytes` column (bytes), and the stats
  block prints its charge amounts (`anon`, `file`, `shmem`, `kernel`, …) in bytes while its event and reclaim keys
  (`workingset_*`, `pgscan*`, `pgsteal*`, `pgrefill`, `pgfault`, …) are counts (`memcontrol.c.v7.2:1628-1665`,
  `:1739-1748`); convert before comparing a number from one line with a number from another.
- Read the block by key, not by position: the entries are ordered for humans and a newer kernel can insert a counter in
  the middle. The key set is also conditional — `zswap`, `zswapped`, `zswap_incomp`, `swapcached`, `anon_thp`,
  `file_thp`, `shmem_thp`, `hugetlb` and others are printed only under their CONFIG options (`hugetlb` also at run
  time), so a missing key is not a zero.
- `anon` is anonymous mappings, `file` is page cache including tmpfs and shared memory, and `shmem` is the swap-backed
  subset inside `file` (tmpfs, shm segments, shared anonymous mmap). Do not add `file` and `shmem`.
- The documentation counts `kernel_stack`, `pagetables`, `percpu`, `vmalloc` and `slab` inside `kernel`, and each is also
  printed on its own line (in v7.2 code `kernel` is its own counter, `MEMCG_KMEM`, at `memcontrol.c.v7.2:1549`); adding
  them to `kernel` double counts by the document's definition.
- The block is the cgroup's charge, not the victim's, and it is aggregated over the cgroup and its descendants
  (`memcontrol.c.v7.2:629`, "Aggregated (CPU and subtree)"). The victim's own `anon-rss`, `file-rss` and `shmem-rss`
  are on the `Killed process` line, and the cgroup over its limit and the victim's own cgroup are two different labels
  on the `oom-kill:` line; the source's NOTE on `mem_cgroup_print_oom_context` says they can differ when hierarchy is
  enabled.
- A group kill prints the selected victim's `Killed process` line, then
  `Tasks in <path> are going to be killed due to memory.oom.group set`, then a line for each further process it kills;
  processes that only share a victim's mm are killed without a line of their own (`oom_kill.c.v7.2:954-985`).
  `oom_kill` counts processes while `oom_group_kill` counts group events.
- What the block cannot tell: which process held which byte, whether the charge was a leak or one large allocation, or
  what caused the cgroup to grow. It reports state at the kill, not history.

## What this changes for mori

- `kernel-oom-line-attribution-r12.md:6` names the summary fields (task, PID, UID, "when available" `task_memcg`); this
  entry adds the label before them — `oom_memcg=<path>`, else the literal `global_oom` — so the summary states whether
  the kill had a charged scope at all.
- `oom-tracepoints-r47.md:56-58` holds that no `oom` trace event carries a cgroup path; the `oom_memcg=` / `task_memcg=`
  printk pair is the record that does, so a tracer keyed on `mark_victim` must be joined to it on pid. [INFERENCE: no
  claims row states the join]
- `oom-victim-context-r41.md:61-64` asks attribution to carry "which cgroup the killed process belonged to"; that token
  is `task_memcg`, beside `oom_memcg`. Its line 12 ("cgroup-scoped") holds for a memcg OOM only: a global OOM prints
  `global_oom` and `__show_mem` in place of the block.
- `oom-kill-counter-kernel-only-r12.md:12,27` labels `oom_kill` kernel-OOM-only from its increment site; this entry
  agrees — its `oom_kill` row says the field counts OOM kills of the cgroup's processes, memcg or global, and the
  increment sits in `__oom_kill_process` (`oom_kill.c.v7.2:935-936`), not in any userspace killer.

## Limits

- Kernel v7.2 only, read from the frozen copies whose sha256 the counter pins; later kernels add or rename keys and can
  change the report path.
- cgroup v2 only. On a v1 hierarchy the same function prints `memory+swap` and `kmem` lines and the page counter's own
  failcnt, which cgroup v2 replaces with the `max` event count; nothing here carries over to v1.
- The summary is rate-limited (`if (__ratelimit(&oom_rs)) { dump_header(oc); dump_oom_victim(oc, victim); }`), but
  the victim line is printed outside that guard; a burst of kills can leave `Killed process` lines with no block at
  all, so a missing block is not evidence that the kill was global.
- The block is formatted into a static `SEQ_BUF_SIZE` buffer under `oom_lock`, and an overflow only prints a warning, so
  a truncated block is possible at event time.
- No host block was read. The lane's rule forbids reading kernel journal MESSAGE text for kill records, so this entry
  states what the kernel prints, not what any past kill on this host printed.
- A located quote proves the quoted words occur in the committed copy, not that the claim cell follows from them.

## Boundaries

- Detection and report only. Setting `memory.max`, `memory.oom.group` or `oom_score_adj` is tsukuroi's work; this entry
  licenses no configuration change.
- No remediation, and no attribution: a memcg OOM block names the cgroup that was charged, not what made it grow.

## Recheck at Linux v7.3 (appended 2026-10-27, round 54)

The claim rows of this entry that pin Linux v7.2 are re-read at tag v7.3 in `corpus/knowledge/kernel-v7.3-recheck-r54.md` (one row per claim hash: status, the v7.3 line the quote now begins on, disposition and its RECHECK votes). The rows above are unchanged and keep their v7.2 anchors; read moved line numbers through that ledger's `## Where the quotes moved` table.
