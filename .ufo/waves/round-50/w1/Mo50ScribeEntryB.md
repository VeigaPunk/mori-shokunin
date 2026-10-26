# Mo50ScribeEntryB — C2 entry draft (independent) — mori round 50, wave w1

Seat: `Mo50ScribeEntryB`, leaf scribe (no subagents). Assignment: independently draft
`corpus/knowledge/oom-memcg-stat-r50.md` for claim **C2** (depth), without reading the peer
scribe's output. Nothing in this report was written into the lane: the draft lives in the fenced
block below. Only this file was written.

Frozen contract read first: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-50/contract.md`
(freeze commit `950e99be6757a52b00e9eb70ae1a1a7bbe2ea379`; entering tip
`7197160b927f04db294c9553fb48fadcc7a3f4e3`). `git rev-parse HEAD` in the lane gave
`950e99be6757a52b00e9eb70ae1a1a7bbe2ea379` (rc 0), i.e. the lane tip is the freeze commit.

## Scratch, tooling, safety

- Scratch: `/fast/scratch/hyaku/mori-r50/Mo50ScribeEntryB/` (`mkdir -p`, `TMPDIR` exported to its
  `tmp/`): normalised source texts, the entry draft, and one fixture repo at `fixture/`.
  `disk-guard.sh status` before the run: `/fast/scratch/hyaku` 28% used, 581.9 G free; `/tmp` 3%
  used. Removed at the end of the seat (`rm -rf` over the seat directory); nothing cited below
  depends on it.
- Tools installed or upgraded: **none**. No pacman transaction was attempted; no network fetch was
  needed, because the three copies are committed.
- Lane mutations: none. Read-only `git rev-parse`, `git cat-file` and the frozen counter's own
  `git show`; plus `git init`/`add`/`commit`/`commit --amend` **inside the scratch fixture only**
  (`git -C "$D" rev-parse --show-toplevel` printed
  `/fast/scratch/hyaku/mori-r50/Mo50ScribeEntryB/fixture` before the first commit; throwaway
  identity used only there).
- Host reads: read-only reads of the three committed copies and of the lane's own text files. No
  kernel log MESSAGE text was read or grepped, no OOM was triggered, no cgroup limit touched.

## Observed evidence

| # | command (cwd = lane root unless noted) | exit | output (trimmed) |
|---|---|---|---|
| 1 | `sha256sum corpus/evidence/sources-r50/cgroup-v2.7.2.html corpus/evidence/sources-r50/memcontrol.c.v7.2 corpus/evidence/sources-r50/oom_kill.c.v7.2` | 0 | `2d716cb798eacf8fbcf431b52697fbb8c5ed8ea9f58ac15b2b55351247c0bf34` cgroup-v2.7.2.html · `8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e` memcontrol.c.v7.2 · `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e` oom_kill.c.v7.2 — all three equal the `COPIES` pins in `count-c2.py` |
| 2 | `wc -l corpus/evidence/sources-r50/{cgroup-v2.7.2.html,memcontrol.c.v7.2,oom_kill.c.v7.2}` | 0 | 3257 / 6068 / 1257 lines, 10582 total |
| 3 | `python3 .ufo/waves/round-50/count-c2.py --selftest` | 0 | 31 × `PASS`, last line `C2_SELFTEST pass=31 fail=0` |
| 4 | `python3 .ufo/waves/round-50/count-c2.py 7197160b927f04db294c9553fb48fadcc7a3f4e3` | 1 | `C2=unmet claims=0 located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=bad provenance=bad rev=7197160b… failed=entry_absent,pins` (matches the contract's entering reading) |
| 5 | `git cat-file -e 7197160b927f04db294c9553fb48fadcc7a3f4e3:corpus/knowledge/oom-memcg-stat-r50.md` | 128 | `fatal: path 'corpus/knowledge/oom-memcg-stat-r50.md' does not exist in '7197160b…'` |
| 6 | regex `^ {0,3}\|\s*S(489\|490\|491)\s*\|` over `corpus/SOURCES.md` | — | 0 / 0 / 0 rows; `S533` also 0 (the staged row is not in the registry yet) |
| 7 | `python3 .ufo/waves/round-50/count-c2.py HEAD --repo /fast/scratch/hyaku/mori-r50/Mo50ScribeEntryB/fixture` | 0 | `C2=met claims=21 located=21 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=de9e912f468a0f922d9c9737da43b6abf389c050` |

Row 7 is the end-to-end proof: a scratch fixture repo committed only the five paths the counter
reads — `corpus/SOURCES.md` (lane bytes plus the three proposed rows), the three frozen copies
unchanged, and the draft entry below as `corpus/knowledge/oom-memcg-stat-r50.md` — and the **frozen**
counter at `.ufo/waves/round-50/count-c2.py` scored that commit `C2=met`. The entry was additionally
scored in-process through the same module's `evaluate()` with an in-memory reader: same line,
`claims=21`.

## Draft — `corpus/knowledge/oom-memcg-stat-r50.md`

```markdown
# A memcg OOM kill: what the kernel prints, and what `memory.stat` says about the charge

source: S489 — Control Group v2, v7.2 page — https://docs.kernel.org/7.2/admin-guide/cgroup-v2.html — the Memory controller sections for memory.stat, memory.events, memory.events.local and memory.oom.group; committed copy corpus/evidence/sources-r50/cgroup-v2.7.2.html, sha256 2d716cb798eacf8fbcf431b52697fbb8c5ed8ea9f58ac15b2b55351247c0bf34. S490 — Linux mm/memcontrol.c at tag v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/memcontrol.c — memory_stat_format, memcg_stat_format, the memory_stats key table, mem_cgroup_print_oom_meminfo and mem_cgroup_print_oom_context; committed copy corpus/evidence/sources-r50/memcontrol.c.v7.2, sha256 8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e. S491 — Linux mm/oom_kill.c at tag v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c — dump_header, dump_oom_victim, __oom_kill_process and the oom_constraint_text table; committed copy corpus/evidence/sources-r50/oom_kill.c.v7.2, sha256 452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e.
verified-at: 2026-10-26 (three frozen copies under corpus/evidence/sources-r50/; sha256 pinned in .ufo/waves/round-50/count-c2.py)
recheck: 90d — `python3 .ufo/waves/round-50/count-c2.py <rev>` re-locates every quote below in the committed copies and checks the three sha256; a new tag re-opens the three URLs
coverage-map: FR1
ground: frontier item **FR1** — "Kernel OOM event-time attribution and fleet correlation"

## Claim

A memory-controller OOM prints **two different records at one instant**: a charge line
(`memory: usage …kB, limit …kB, failcnt …`) and a `Memory cgroup stats for <path>:` block that is
the `memory.stat` formatter run against that cgroup while the OOM lock is held; then a per-victim
`Killed process` line whose memory fields come from the victim's own `mm`, not from the cgroup.
The block is an event-time sample: a later `memory.stat` read is a different sample of a cgroup
whose membership, charge and reclaim state have moved on. Amounts split units too — the charge
line and `Killed process` line print kB, `memory.stat` prints bytes for state keys and bare
counts for event keys.

## The claims table

| claim | source | quote |
|---|---|---|
| The memory.stat interface is read-only, flat-keyed and exists only on non-root cgroups | S489 | `A read-only flat-keyed file which exists on non-root cgroups. This breaks down the cgroup’s memory footprint into different types of memory` |
| Every memory amount reads as a byte count, not as a page count | S489 | `All memory amounts are in bytes. The entries are ordered to be human readable, and new entries can show up in the middle.` |
| The file key counts page cache, and it includes tmpfs pages plus shared memory | S489 | `Amount of memory used to cache filesystem data, including tmpfs and shared memory.` |
| The shmem key is the swap-backed slice, so tmpfs and shared anonymous mappings land there | S489 | `Amount of cached filesystem data that is swap-backed, such as tmpfs, shm segments, shared anonymous mmap()s` |
| The kernel key aggregates stack, page table, per-cpu, vmalloc and slab charges | S489 | `Amount of total kernel memory, including (kernel_stack, pagetables, percpu, vmalloc, slab)` |
| The anon key reports anonymous mappings such as brk and anonymous mmap | S489 | `Amount of memory used in anonymous mappings such as brk() , sbrk() , and mmap(MAP_ANONYMOUS).` |
| The oom_kill event counts victims killed by any OOM killer, not only the kernel's | S489 | `The number of processes belonging to this cgroup killed by any kind of OOM killer.` |
| The .local sibling drops the hierarchical sum and reports this cgroup alone | S489 | `Similar to memory.events but the fields in the file are local to the cgroup i.e. not hierarchical.` |
| Key position is not a stable contract, so a reader must look values up by name | S489 | `Don’t rely on items remaining in a fixed position; use the keys to look up specific values! If the entry has no per-node counter` |
| Setting memory.oom.group makes the cgroup an indivisible workload, killed as one unit | S489 | `all tasks belonging to the cgroup or to its descendants (if the memory cgroup is not a leaf cgroup) are killed together` |
| The first memcg OOM line prints usage, limit and failcnt all in kB | S490 | `memory: usage %llukB, limit %llukB, failcnt %lu\n",` |
| The stats block is headed by the memory cgroup path and the same formatter serves memory.stat | S490 | `Memory cgroup stats for "); pr_cont_cgroup_path(memcg->css.cgroup); pr_cont(":");` |
| On cgroup v2 the printed failcnt is the max event counter, not a separate charge field | S490 | `if (cgroup_subsys_on_dfl(memory_cgrp_subsys)) memory_failcnt = atomic_long_read(&memcg->memory_events[MEMCG_MAX]); else memory_failcnt = memcg->memory.failcnt;` |
| The formatter converts each state item to the output unit before printing | S490 | `Translate stat items to the correct unit for memory.stat output` |
| The emitted keys come from a static table whose first three entries are anon, file and kernel | S490 | `{ "anon", NR_ANON_MAPPED }, { "file", NR_FILE_PAGES }, { "kernel", MEMCG_KMEM }, { "kernel_stack",` |
| The oom-kill summary distinguishes an oom_memcg path from the global_oom marker | S490 | `if (memcg) { pr_cont(",oom_memcg="); pr_cont_cgroup_path(memcg->css.cgroup); } else pr_cont(",global_oom"); if (p) { pr_cont(",task_memcg=");` |
| A memcg OOM substitutes the cgroup block; a global OOM calls the zone-wide memory show | S491 | `if (is_memcg_oom(oc)) mem_cgroup_print_oom_meminfo(oc->memcg); else { __show_mem(SHOW_MEM_FILTER_NODES, oc->nodemask, gfp_zone(oc->gfp_mask));` |
| The block and summary are rate-limited, so a burst of kills may print only victim lines | S491 | `if (__ratelimit(&oom_rs)) { dump_header(oc); dump_oom_victim(oc, victim); }` |
| The victim line carries pid, comm, total-vm, anon-rss, file-rss, shmem-rss, UID, pgtables and oom_score_adj | S491 | `Killed process %d (%s) total-vm:%lukB, anon-rss:%lukB, file-rss:%lukB, shmem-rss:%lukB, UID:%u pgtables:%lukB oom_score_adj:%d\n` |
| The message distinguishes the two paths: a memcg OOM says Memory cgroup out of memory | S491 | `"Out of memory" : "Memory cgroup out of memory"` |
| The summary constraint field reads CONSTRAINT_MEMCG when the OOM came from a cgroup limit | S491 | `[CONSTRAINT_NONE] = "CONSTRAINT_NONE", [CONSTRAINT_CPUSET] = "CONSTRAINT_CPUSET", [CONSTRAINT_MEMORY_POLICY] = "CONSTRAINT_MEMORY_POLICY", [CONSTRAINT_MEMCG]` |

Rows above are the whole spine: each claim is one statement the quoted span supports, and each
quote is located in the committed copy of its row's URL (HTML normalised: script, style and comment
blocks dropped, tags stripped, entities decoded; C files whitespace-collapsed).

## The report, block by block

Order inside one memcg OOM (`mm/oom_kill.c`, `oom_kill_process` → `dump_header` → `dump_oom_victim` →
`__oom_kill_process`):

1. `invoked oom-killer: gfp_mask=…, order=…, oom_score_adj=…` — which task and allocation tripped it.
2. The `memory:` charge line, then a `swap:` charge line on cgroup v2 — both `usage`, `limit`,
   `failcnt`, all in kB (the `K` macro). On v2 `failcnt` is read from `memory_events[MEMCG_MAX]`.
3. `Memory cgroup stats for <path>:` followed by `seq_buf_do_printk` of `memory_stat_format` — the
   same function the `memory.stat` file handler `memory_stat_show` (memcontrol.c:4905-4918) calls —
   one `key value` line per key, emitted in static-table order.
4. `mem_cgroup_show_protected_memory` and, unless disabled, `Tasks state (memory values in pages)`.
5. `oom-kill:constraint=…,nodemask=…,oom_memcg=<path>,task_memcg=<path>,task=<comm>,pid=<pid>,uid=<uid>`
   — the scope summary, with `global_oom` in place of an `oom_memcg` path for a system-wide OOM.
6. `<message>: Killed process <pid> (<comm>) total-vm:…kB, anon-rss:…kB, file-rss:…kB,
   shmem-rss:…kB, UID:<uid> pgtables:…kB oom_score_adj:<n>` — the victim record; `message` is
   `Memory cgroup out of memory` for a memcg OOM and `Out of memory` for a global one.

The block and the `oom-kill:` summary sit inside `if (__ratelimit(&oom_rs))` in `oom_kill_process`,
while the `Killed process` line is an unconditional `pr_err` in `__oom_kill_process`: a burst of
memcg OOMs inside the ratelimit window can leave victim lines with no block and no summary, so an
absent block is not evidence that the kill was not a memcg OOM.

The `Killed process` fields are the victim's `mm` counters (`MM_ANONPAGES`, `MM_FILEPAGES`,
`MM_SHMEMPAGES`); they say nothing about the cgroup's total charge, which is what the charge line
and the block carry.

## What the memory.stat keys mean

| key | means | unit |
|---|---|---|
| `anon` | anonymous mappings (`brk`, `sbrk`, `mmap(MAP_ANONYMOUS)`) | bytes |
| `file` | page cache, including tmpfs and shared memory | bytes |
| `shmem` | swap-backed cached filesystem data: tmpfs, shm segments, shared anonymous mmaps | bytes |
| `kernel` | aggregate of `kernel_stack`, `pagetables`, `percpu`, `vmalloc`, `slab` and other kernel use | bytes |
| `slab`, `slab_reclaimable`, `slab_unreclaimable` | in-kernel object storage and its reclaimable split | bytes |
| `sock` | network transmission buffers | bytes |
| `inactive_…`, `active_…`, `unevictable` | page-reclaim list state, not type totals | bytes |
| `workingset_*`, `pgscan*`, `pgsteal*`, `pgfault`, `pgmajfault`, `pswpin`, `pswpout` | event counters | bare counts |

Keys are looked up by name: new entries can appear between existing ones, so positional parsing of
the block breaks on a kernel upgrade. Event keys are exported as counts even where the internal
state is in pages; state keys pass through `memcg_page_state_output` and are printed in bytes.

## Global OOM versus memcg OOM

Same killer, different report. `is_memcg_oom(oc)` selects `mem_cgroup_print_oom_meminfo(oc->memcg)`
(the block above); otherwise `__show_mem` dumps the zone-wide picture and there is **no**
`Memory cgroup stats` header and no `oom_memcg=` path — the summary carries `global_oom`. The
constraint field reads `CONSTRAINT_MEMCG` for the memcg case and `CONSTRAINT_NONE` (or
`CONSTRAINT_CPUSET`, `CONSTRAINT_MEMORY_POLICY`) otherwise, so the summary alone identifies which
report shape follows. `memory.oom.group` changes *who* dies, not the report shape: it turns the
cgroup into an indivisible workload and prints `Tasks in <path> are going to be killed`.

[INFERENCE] Because the block is emitted while the OOM lock is held and before the SIGKILL, the
usage figure in it is pre-kill charge; a `memory.current` or `memory.stat` read taken after the kill
can be lower (charge removed with the dead tasks) or higher (other tasks still allocating).

## Decision row

| situation | do | do not | source |
|---|---|---|---|
| A memcg OOM report block was recorded and the question is who held the charge | attribute the charge to the path in `Memory cgroup stats for <path>:` at that timestamp, and treat its `memory:`/`swap:` usage, limit and failcnt as the event-time scalar | do not read the victim's `total-vm`/`anon-rss` as the cgroup charge, and do not promote a later `memory.stat` sample to the killed state | S490, S491 |
| The block path and `task_memcg=` disagree | use the block path (or `oom_memcg=`) as the charge scope and `task_memcg=` as where the victim sat; report both | do not assume the victim was charged to the OOMing cgroup | S490 |
| Only the `Killed process` line survived | name the victim (pid, comm, UID) and its own resident set; mark the cgroup charge unknown and check the ratelimit window before concluding the kill was global | do not reconstruct the cgroup's usage from `total-vm`, `anon-rss`, `file-rss`, `shmem-rss` | S491 |
| A `memory.stat` was read after the kill | report it as a later sample and say membership and charge may have changed | do not difference it against the block and call the result the killed process's footprint | S489, S490 |
| The record is a global OOM | expect the zone-wide `__show_mem` dump and the `Out of memory` message | do not look for a cgroup block or an `oom_memcg=` path in that record | S491 |

## What this changes for mori

- `corpus/knowledge/oom-kill-counter-kernel-only-r12.md` — adds the event-time print path beside the counter increment: the counter says a kill happened, the block says what the charge was.
- `corpus/knowledge/kernel-oom-line-attribution-r12.md` — the summary it already parses is followed by a charge line and a cgroup block, both attributable to `oom_memcg=` before the victim line.
- `corpus/knowledge/oom-tracepoints-r47.md` — `mark_victim` is per-task, so the block is the cgroup-scope companion record a tracer needs to answer who held the charge.
- `corpus/knowledge/oom-victim-context-r41.md` — the victim line is the victim's own `mm`, so cgroup context must come from the block or the summary.
- `corpus/knowledge/census-cgroup-levels-r45.md` — the block names the OOM cgroup directly, a provenance source separate from that row's preferred-fallback `memory.events` read.

## Limits

- A located quote proves the words are in the committed copy, not that the claim follows from it;
  the reviewer waves re-open every row against surrounding text.
- v7.2 code and the v7.2 page say nothing about other kernels, and nothing here is a cgroup v1 claim
  for the v2 block (v1 uses `memory+swap` and `kmem` lines instead).
- No host OOM report is read or grepped (lane rule: no kernel MESSAGE text), so this entry states what
  the kernel prints, not what any past kill on this host printed.
- Nothing here is a threshold or an alarm rule; it is the shape and the scope semantics of the record.
```

## Proposed `corpus/SOURCES.md` rows (not written; the registry is another seat's file)

```markdown
| S489 | Control Group v2, v7.2 page — https://docs.kernel.org/7.2/admin-guide/cgroup-v2.html | docs | A | the v7.2 memory-controller reference for the memory.stat keys and their units, memory.events versus memory.events.local, and memory.oom.group; not any host's values and not the kernel print formats | memory.stat key descriptions and the units sentence; memory.events oom_kill field; memory.events.local; memory.oom.group; committed copy corpus/evidence/sources-r50/cgroup-v2.7.2.html sha256 2d716cb798eacf8fbcf431b52697fbb8c5ed8ea9f58ac15b2b55351247c0bf34 | Every memory.stat amount is in bytes while event keys are bare counts; oom_kill is broad and hierarchical while its .local sibling is the cgroup's own count | mined | 2026-10-26 | on-release | corpus/knowledge/oom-memcg-stat-r50.md |
| S490 | Linux mm/memcontrol.c at tag v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/memcontrol.c | code | A | the memcg OOM print path: the usage/limit/failcnt charge line, the Memory cgroup stats block and the formatter it shares with memory.stat, the stat key table and output units, and the oom_memcg context fields; not cgroup v1-only branches and not any host output | memory_stats table 1546-1609; memcg_stat_format 1693-1749; memory_stat_format 1751-1759; mem_cgroup_print_oom_context 1770-1784; mem_cgroup_print_oom_meminfo 1791-1830; memory_stat_show 4905-4918; committed copy corpus/evidence/sources-r50/memcontrol.c.v7.2 sha256 8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e | The block is the memory.stat formatter run at OOM time under a path header; on cgroup v2 the printed failcnt is the max event counter | mined | 2026-10-26 | on-release | corpus/knowledge/oom-memcg-stat-r50.md |
| S491 | Linux mm/oom_kill.c at tag v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c | code | A | the OOM report assembly at v7.2: dump_header choosing the memcg block or __show_mem, dump_oom_victim's constraint and oom_memcg fields, and __oom_kill_process's Killed process line; the same URL as S003 and S476 with a different scope, a W04 warning not an error | oom_constraint_text 239-244; dump_tasks 422-442; dump_oom_victim 444-454; dump_header 456-475; __oom_kill_process 912-992 (victim line 945; ratelimit guard at 1030-1033); committed copy corpus/evidence/sources-r50/oom_kill.c.v7.2 sha256 452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e | A memcg OOM gets the cgroup block and CONSTRAINT_MEMCG while a global OOM gets __show_mem and the plain Out of memory message | mined | 2026-10-26 | on-release | corpus/knowledge/oom-memcg-stat-r50.md |
```

Line ranges in the anchors were re-derived from the committed copies: `memory_stats` 1546-1609,
`memcg_stat_format` 1693-1749, `memory_stat_format` 1751-1759, `mem_cgroup_print_oom_context`
1770-1784, `mem_cgroup_print_oom_meminfo` 1791-1830, `memory_stat_show` 4905-4918; `oom_kill.c`
`oom_constraint_text` 239-244, `dump_tasks` 422-442, `dump_oom_victim` 444-454, `dump_header`
456-475, `__oom_kill_process` 912-992 with the victim line at 945 and the ratelimit guard at
1030-1033. S491 repeats the URL of S003 and S476 with a different scope, as the contract states
(a W04 warning).

## What was checked, and how

- Every one of the 21 quotes was extracted from the normalised copy by anchor offset, not typed from
  the rendered page, then asserted present (`count >= 1`) in that normalised text: HTML through the
  counter's `normalise()` (script/style/comment blocks dropped, tags stripped, entities decoded),
  C files through whitespace collapse only. Two spans in `cgroup-v2.7.2.html` occur more than once;
  both final quotes were chosen to occur exactly once (the 18-word "All memory amounts…" variant and
  the 24-word "Don’t rely…" variant).
- Rows: 21 total, each with a claim of >= 6 words, unique (case/space folded), >= 3 words of 3+
  letters absent from its quote; quote 6-25 words, unique, no `|`, exactly one backticked span.
- Sources: S489 ×10, S490 ×7, S491 ×4 — all three frozen sources used.
- Front matter: the `source:` line cites S489/S490/S491 (a superset of the table ids), and
  `verified-at:` and `recheck:` sit in the first 14 non-empty lines; the claims table is the first
  table in the file, so the later key and decision tables are not parsed as claim rows.

## Known limits / UNVERIFIED

- The draft is **not on disk in the lane and not committed**; until the entry and the three registry
  rows land at revision R, `count-c2.py R` keeps reporting `entry_absent` (evidence row 4).
- Quote location proves the words occur in the copy, not that the claim follows from them. One row
  ("the same formatter serves memory.stat") is supported by `memory_stat_show`
  (memcontrol.c:4905-4918), which the quote itself does not cover; I cited that range in prose and in
  the S490 anchor.
- Nothing here was measured on this host: no OOM report was read, no `memory.stat` sample taken. The
  entry is about what v7.2 prints; no claim about other kernel versions or about cgroup v1.
- The counter's `pins=ok` only re-hashes the three committed copies; the upstream URLs were not
  re-fetched (no network use this seat).
- Fixture commit `de9e912f468a0f922d9c9737da43b6abf389c050` is scratch-only and was deleted with the
  seat directory; it is a proof vehicle, not a lane revision.

## Findings

- **HIGH** — `corpus/SOURCES.md` has no S489, S490 or S491 row at the lane tip (evidence row 6: 0
  rows each; `S533` also absent). C2 requires one mined, 2026-10-26-opened registry row per cited id
  that names the row's URL and lists the entry in `used-by`; without those rows no entry can score
  `C2=met`, whatever its table says. The three proposed rows above supply them; the registry write
  belongs to another seat.
- **HIGH** — `corpus/knowledge/oom-memcg-stat-r50.md` does not exist at the entering tip
  (`git cat-file -e` rc 128, evidence row 5) and is not in the working tree either, so the
  predicate's `entry_absent` arm stays live until the L1 lands an entry.
- **MED** — The memcg block and the `oom-kill:` summary sit inside `if (__ratelimit(&oom_rs))`
  (`corpus/evidence/sources-r50/oom_kill.c.v7.2:1030-1033`) while the `Killed process` line is an
  unconditional `pr_err` (`:945`). A burst of memcg OOMs can leave victim lines with no block and no
  summary, so an absent block is not evidence that a kill was a global OOM. Carrier: the drafted
  entry, `## The report, block by block` and its decision table.
- **MED** — Quotes must come from normalised bytes, not the rendered page. HTML normalisation leaves
  artefact spacing and typography a typed quote misses: the anon key reads
  `such as brk() , sbrk() , and mmap(MAP_ANONYMOUS).` (space before each comma), and the page uses
  `cgroup’s`, `Don’t`, `‘npn’`. Concern: `count-c2.py` `normalise()` against
  `corpus/evidence/sources-r50/cgroup-v2.7.2.html`.
- **LOW** — The predicate checks quote location and a 3-word divergence floor, not entailment; two
  rows lean on nearby code rather than on the quoted span (`memory_stat_show`,
  memcontrol.c:4905-4918; the `memory`/`swap` line pair at memcontrol.c:1805-1812). Reviewer waves
  should re-open them.
- **LOW** — Internal accounting units differ from output units (`memcg_page_state_unit`,
  memcontrol.c:1624-1642: `NR_KERNEL_STACK_KB` in KiB, `_B` items in bytes, the rest in pages) while
  every printed state key is bytes. [INFERENCE] A reader that multiplies a raw `memcg_page_state`
  value by 4096 mis-scales `kernel_stack`, `percpu`, `zswap`, `slab_reclaimable` and
  `slab_unreclaimable`. Concern: the drafted entry's units table.
- **LOW** — Shorter fragments of two documentation sentences occur 2-3 times in the same HTML copy
  (`All memory amounts are in bytes.` ×3; `The entries are ordered … in the middle.` ×2). The counter
  accepts any located span, so a shorter quote would be ambiguous evidence; this draft avoids them,
  but the predicate does not require it. Concern: `count-c2.py` quote check.
