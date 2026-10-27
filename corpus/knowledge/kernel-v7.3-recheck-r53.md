# The round-51 and round-52 kernel claims at Linux v7.3: 46 rechecked, two quotes respelled

source: S502 — https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/filesystems/proc.rst?h=v7.3 — docs, tier A, Documentation/filesystems/proc.rst at tag v7.3, committed copy `corpus/evidence/sources-r53/proc.rst.v7.3`, opened 2026-10-26
source: S503 — https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/mm/show_mem.c?h=v7.3 — code, tier A, mm/show_mem.c at tag v7.3, committed copy `corpus/evidence/sources-r53/show_mem.c.v7.3`, opened 2026-10-26
source: S504 — https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/fs/proc/meminfo.c?h=v7.3 — code, tier A, fs/proc/meminfo.c at tag v7.3, committed copy `corpus/evidence/sources-r53/meminfo.c.v7.3`, opened 2026-10-26
source: S505 — https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/mm_inline.h?h=v7.3 — code, tier A, include/linux/mm_inline.h at tag v7.3, committed copy `corpus/evidence/sources-r53/mm_inline.h.v7.3`, opened 2026-10-26
source: S506 — https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/mm/overcommit-accounting.rst?h=v7.3 — docs, tier A, Documentation/mm/overcommit-accounting.rst at tag v7.3, committed copy `corpus/evidence/sources-r53/overcommit-accounting.rst.v7.3`, opened 2026-10-26
source: S507 — https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/admin-guide/sysctl/vm.rst?h=v7.3 — docs, tier A, Documentation/admin-guide/sysctl/vm.rst at tag v7.3, committed copy `corpus/evidence/sources-r53/vm.rst.v7.3`, opened 2026-10-26
source: S508 — https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/mm/util.c?h=v7.3 — code, tier A, mm/util.c at tag v7.3, committed copy `corpus/evidence/sources-r53/util.c.v7.3`, opened 2026-10-26
source: S509 — https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/mman.h?h=v7.3 — code, tier A, include/linux/mman.h at tag v7.3, committed copy `corpus/evidence/sources-r53/mman.h.v7.3`, opened 2026-10-26
source: S510 — https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/mm/mmap.c?h=v7.3 — code, tier A, mm/mmap.c at tag v7.3, committed copy `corpus/evidence/sources-r53/mmap.c.v7.3`, opened 2026-10-26
verified-at: 2026-10-26
recheck: on-release — `python3 .ufo/waves/round-53/count-c1.py <rev>` re-derives every status below from the committed v7.3 copies; at the next tag, fetch each path with `curl -fsSL 'https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/<path>?h=<tag>'`, add the copies and rows, and run the same ledger shape against them
coverage-map: resource runway (the round-51 MemAvailable and round-52 commit-ledger entries, rechecked; no new ground)

mori reports resource runway from three /proc/meminfo lines whose meaning the lane pinned to Linux v7.2 bytes in
rounds 51 and 52 (`memavailable-estimate-r51.md`, `overcommit-commit-limit-r52.md`), each with `recheck: on-release`.
Linux v7.3 is tagged (`refs/tags/v7.3^{}` → `c03c1a14507d`, `.ufo/waves/round-53/evidence/sweeps.txt`). This entry is
that recheck: every claim row of the two tables that cites a v7.2 file (46 of 49; the other three cite the 2014
commit patch, which no release changes) is read again against the same path at v7.3.

## What changed between v7.2 and v7.3 in the nine files

| path | v7.2 → v7.3 | where |
|---|---|---|
| `fs/proc/meminfo.c`, `Documentation/mm/overcommit-accounting.rst`, `include/linux/mman.h` | byte-identical (same sha256) | — |
| `Documentation/filesystems/proc.rst` | 3 changed lines | outside the meminfo field definitions |
| `mm/show_mem.c` | 22 changed lines | an include, `const nodemask_t *` parameters, printk units (`%luKB` → `%lukB`), two printk format-specifier flips (`%ld`/`%lu`) and one `(unsigned long)` cast; `si_mem_available` untouched |
| `include/linux/mm_inline.h` | 49 changed lines (57 added+removed) | removal of the uffd-wp pte helper and two `memdesc_section(&cur_page->flags)` call sites; `folio_is_file_lru` untouched |
| `Documentation/admin-guide/sysctl/vm.rst` | 64 changed lines (83 added+removed) | a new `panic_on_unrecoverable_memory_failure` section and index line; a dropped `mm/swap.c` pointer |
| `mm/util.c` | 14 changed lines | `vm_mmap_pgoff` (`EMPTY_VMA_FLAGS`), the shadow-stack helper (`vm_flags_t` → `vma_flags_t`), and two `vma->vm_pgoff` → `vma_start_pgoff(vma)` conversions (`compat_set_desc_from_vma`, `call_vma_mapped`); `vm_commit_limit`, `__vm_enough_memory` untouched |
| `mm/mmap.c` | 190 changed lines (205 added+removed) | the `vm_flags_t` → `vma_flags_t` conversion including the `MAP_NORESERVE` block, the `mm_get_unmapped_area_vmflags` → `mm_get_unmapped_area_vmaflags` rename, and the removal of `__install_special_mapping` from this file (38 lines) |

Line counts: `diff -u <v7.2 copy> <v7.3 copy> | grep -c '^[-+][^-+]'` over the round-51/52 copies and
`corpus/evidence/sources-r53/` (this pattern skips changed blank lines). Added+removed lines by
`git diff --no-index --numstat`: proc.rst 3, show_mem.c 22, mm_inline.h 57 (2/55), vm.rst 83 (80/3), util.c 14,
mmap.c 205 (92/113) (round-53 wave `w1/Mo53ExecAnchorCheck.md` §4.9). Of the 46 rows, only rows 34 and 37 (the two
`absent` ones) sit in an enclosing function or section that changed at all (`w1/Mo53ExecDiffAudit.md`).

## Ledger

`status` is derived, never typed: `held` when the row's v7.2 quote still occurs (whitespace collapsed) in the v7.3
copy, `absent` otherwise. `quote` is the v7.2 quote when held and a v7.3 quote of the same rule when absent.
`disposition` says whether the claim, read against the v7.3 file, still holds (`holds`) or not (`changed`); it is
the L1's reading at the data commit and is decided by two RECHECK votes per row from seats that did not write the
row (`.ufo/waves/round-53/w1/Mo53Fr01.md`–`Mo53Fr12.md`): all 46 `holds` carry two or three such votes and no
seat voted `changed` or proposed another quote. The claim text of each hash is listed in
`.ufo/waves/round-53/evidence/c1-claims.txt`.

| h | entry | status | source | quote | disposition |
|---|---|---|---|---|---|
| 2d0daa4192f1 | `corpus/knowledge/memavailable-estimate-r51.md` | held | S502 | `An estimate of how much memory is available for starting new applications, without swapping.` | holds |
| 72cdbee44353 | `corpus/knowledge/memavailable-estimate-r51.md` | held | S502 | `In-memory cache for files read from the disk (the pagecache) as well as tmpfs & shmem.` | holds |
| a9cf30c5ed71 | `corpus/knowledge/memavailable-estimate-r51.md` | held | S502 | `Total memory used by shared memory (shmem) and tmpfs` | holds |
| ad57d1b66582 | `corpus/knowledge/memavailable-estimate-r51.md` | held | S502 | `The impact of those factors will vary from system to system.` | holds |
| eba2b78b47f3 | `corpus/knowledge/memavailable-estimate-r51.md` | held | S502 | `Calculated from MemFree, SReclaimable, the size of the file LRU lists, and the low watermarks in each zone.` | holds |
| 357c747c23d2 | `corpus/knowledge/memavailable-estimate-r51.md` | held | S504 | `show_val_kb(m, "MemFree: ", i.freeram); show_val_kb(m, "MemAvailable: ", available);` | holds |
| 6c2327e19df1 | `corpus/knowledge/memavailable-estimate-r51.md` | held | S504 | `seq_put_decimal_ull_width(m, s, num << (PAGE_SHIFT - 10), 8); seq_write(m, " kB\n", 4);` | holds |
| 7e14f1771092 | `corpus/knowledge/memavailable-estimate-r51.md` | held | S504 | `cached = global_node_page_state(NR_FILE_PAGES) - total_swapcache_pages() - i.bufferram;` | holds |
| 8f6d04247472 | `corpus/knowledge/memavailable-estimate-r51.md` | held | S505 | `1 if @folio is a regular filesystem backed page cache folio * or a lazily freed anonymous folio (e.g. via MADV_FREE).` | holds |
| d6001a798ea7 | `corpus/knowledge/memavailable-estimate-r51.md` | held | S505 | `0 if @folio is a normal anonymous folio, a tmpfs folio or otherwise * ram or swap backed folio.` | holds |
| 0a908e8eb4f3 | `corpus/knowledge/memavailable-estimate-r51.md` | held | S503 | `without causing swapping or OOM. */ available = global_zone_page_state(NR_FREE_PAGES) - totalreserve_pages;` | holds |
| 1b9c863ec2c2 | `corpus/knowledge/memavailable-estimate-r51.md` | held | S503 | `Not all the page cache can be freed, otherwise the system will * start swapping or thrashing.` | holds |
| 40b46a312e03 | `corpus/knowledge/memavailable-estimate-r51.md` | held | S503 | `struct zone *zone; for_each_zone(zone) wmark_low += low_wmark_pages(zone);` | holds |
| 58ba82f481b8 | `corpus/knowledge/memavailable-estimate-r51.md` | held | S503 | `Part of the reclaimable slab and other kernel memory consists of * items that are in use, and cannot be freed.` | holds |
| 6b8f33ed528e | `corpus/knowledge/memavailable-estimate-r51.md` | held | S503 | `pagecache -= min(pagecache / 2, wmark_low); available += pagecache;` | holds |
| 6c8b6efc9731 | `corpus/knowledge/memavailable-estimate-r51.md` | held | S503 | `cache, needs to stay. */ pagecache = global_node_page_state(NR_ACTIVE_FILE) + global_node_page_state(NR_INACTIVE_FILE);` | holds |
| cbcd91de05ac | `corpus/knowledge/memavailable-estimate-r51.md` | held | S503 | `reclaimable -= min(reclaimable / 2, wmark_low); available += reclaimable;` | holds |
| d901a2d666fb | `corpus/knowledge/memavailable-estimate-r51.md` | held | S503 | `if (available < 0) available = 0; return available;` | holds |
| 00e2a9db523b | `corpus/knowledge/overcommit-commit-limit-r52.md` | held | S507 | `When overcommit_memory is set to 2, "never overcommit" mode, reserve min(3% of current process size, user_reserve_kbytes) of free memory.` | holds |
| 35d642f1d0d9 | `corpus/knowledge/overcommit-commit-limit-r52.md` | held | S507 | `When this flag is 1, the kernel pretends there is always enough memory until it actually runs out.` | holds |
| 43cf2a78acdd | `corpus/knowledge/overcommit-commit-limit-r52.md` | held | S507 | `When this flag is 0, the kernel compares the userspace memory request size against total memory plus swap and rejects obvious overcommits.` | holds |
| 5c40f6fa5c62 | `corpus/knowledge/overcommit-commit-limit-r52.md` | held | S507 | `Only one of them may be specified at a time. Setting one disables the other (which then appears as 0 when read).` | holds |
| bfb15534fa5e | `corpus/knowledge/overcommit-commit-limit-r52.md` | held | S507 | `That should provide enough for the admin to log in and kill a process, if necessary, under the default overcommit 'guess' mode.` | holds |
| fcd0e7a78872 | `corpus/knowledge/overcommit-commit-limit-r52.md` | held | S507 | `When overcommit_memory is set to 2, the committed address space is not permitted to exceed swap plus this percentage of physical RAM.` | holds |
| 3b02f6680556 | `corpus/knowledge/overcommit-commit-limit-r52.md` | held | S506 | `The current overcommit limit and amount committed are viewable in` | holds |
| 3c2512af8468 | `corpus/knowledge/overcommit-commit-limit-r52.md` | held | S506 | `in most situations this means a process will not be killed while accessing pages but will receive errors on memory allocation as appropriate.` | holds |
| 61b7677d56fe | `corpus/knowledge/overcommit-commit-limit-r52.md` | held | S506 | `The total address space commit for the system is not permitted to exceed swap + a configurable amount (default is 50%) of physical RAM.` | holds |
| 7b2fc298698e | `corpus/knowledge/overcommit-commit-limit-r52.md` | held | S506 | `To Do ===== * Account ptrace pages (this is hard)` | holds |
| 921c2e511e09 | `corpus/knowledge/overcommit-commit-limit-r52.md` | held | S506 | `In mode 2 the MAP_NORESERVE flag is ignored.` | holds |
| 9afaa81505da | `corpus/knowledge/overcommit-commit-limit-r52.md` | held | S506 | `Heuristic overcommit handling. Obvious overcommits of address space are refused. Used for a typical system.` | holds |
| e37e65e64a4c | `corpus/knowledge/overcommit-commit-limit-r52.md` | held | S506 | `SHARED or READ-only - 0 cost (the file is the map not swap)` | holds |
| 02f5bfd6be3b | `corpus/knowledge/overcommit-commit-limit-r52.md` | held | S509 | `static inline void vm_acct_memory(long pages) { percpu_counter_add_batch(&vm_committed_as, pages, vm_committed_as_batch); }` | holds |
| ff0d23e9fde8 | `corpus/knowledge/overcommit-commit-limit-r52.md` | held | S509 | `static inline void vm_unacct_memory(long pages) { vm_acct_memory(-pages); }` | holds |
| 0fbd62f51ce8 | `corpus/knowledge/overcommit-commit-limit-r52.md` | absent | S510 | `We honor MAP_NORESERVE if allowed to overcommit */ if (sysctl_overcommit_memory != OVERCOMMIT_NEVER) vma_flags_set(&vma_flags, VMA_NORESERVE_BIT);` | holds |
| 10ac5a250ac2 | `corpus/knowledge/overcommit-commit-limit-r52.md` | held | S510 | `sysctl_user_reserve_kbytes = min(free_kbytes / 32, SZ_128K);` | holds |
| 1cadeed9914b | `corpus/knowledge/overcommit-commit-limit-r52.md` | held | S510 | `sysctl_admin_reserve_kbytes = min(free_kbytes / 32, SZ_8K);` | holds |
| d7a1dc88dcb3 | `corpus/knowledge/overcommit-commit-limit-r52.md` | absent | S510 | `hugetlb applies strict overcommit unless MAP_NORESERVE */ if (file && is_file_hugepages(file)) vma_flags_set(&vma_flags, VMA_NORESERVE_BIT);` | holds |
| 28d3042fded0 | `corpus/knowledge/overcommit-commit-limit-r52.md` | held | S508 | `allowed = ((totalram_pages() - hugetlb_total_pages()) * sysctl_overcommit_ratio / 100); allowed += total_swap_pages;` | holds |
| 2d64007fa0dc | `corpus/knowledge/overcommit-commit-limit-r52.md` | held | S508 | `The deviation of sync_overcommit_as could be big with loose policy * like OVERCOMMIT_ALWAYS/OVERCOMMIT_GUESS.` | holds |
| 309f4487d8b6 | `corpus/knowledge/overcommit-commit-limit-r52.md` | held | S508 | `if (pages > totalram_pages() + total_swap_pages) goto error; return 0;` | holds |
| 41934e8b2887 | `corpus/knowledge/overcommit-commit-limit-r52.md` | held | S508 | `if (!cap_sys_admin) allowed -= sysctl_admin_reserve_kbytes >> (PAGE_SHIFT - 10);` | holds |
| 967021950067 | `corpus/knowledge/overcommit-commit-limit-r52.md` | held | S508 | `if (percpu_counter_read_positive(&vm_committed_as) < allowed) return 0;` | holds |
| 9cb0e908f997 | `corpus/knowledge/overcommit-commit-limit-r52.md` | held | S508 | `static int sysctl_overcommit_ratio __read_mostly = 50;` | holds |
| a75ce7619818 | `corpus/knowledge/overcommit-commit-limit-r52.md` | held | S508 | `if (sysctl_overcommit_kbytes) allowed = sysctl_overcommit_kbytes >> (PAGE_SHIFT - 10);` | holds |
| ca2418460394 | `corpus/knowledge/overcommit-commit-limit-r52.md` | held | S508 | `pr_warn_ratelimited("%s: pid: %d, comm: %s, bytes: %lu not enough memory for the allocation\n",` | holds |
| cddcf1bc062f | `corpus/knowledge/overcommit-commit-limit-r52.md` | held | S508 | `vm_acct_memory(pages); /* * Sometimes we want to use more memory than we have */ if (sysctl_overcommit_memory == OVERCOMMIT_ALWAYS) return 0;` | holds |

## Reading rules (mori)

| question | answer at v7.3 | pointer |
|---|---|---|
| May a reader still use the round-51/52 entries on a v7.3 kernel? | yes, row by row, as far as each row's disposition says `holds` | the ledger above |
| Why do two round-52 quotes no longer match? | v7.3 writes the `MAP_NORESERVE` decision with `vma_flags_set(&vma_flags, VMA_NORESERVE_BIT)` instead of `vm_flags \|= VM_NORESERVE`; the two conditions are the same | `mmap.c.v7.3:563-571` |
| Does a held quote prove the claim? | no: it proves the words occur; the vote on the disposition carries the meaning | `count-c1.py` limits |

## Boundaries

- v7.2 and v7.3 bytes only; the host runs 7.2.11 (`uname -r`, 2026-10-26), so the v7.2 entries remain the host's
  reading and this ledger says what a v7.3 host would read.
- Not rechecked here: `oom-tracepoints-r47.md`, the round-50 memcg entry (its recheck is `90d`), prose outside the
  two tables, and the anchors of rows S492–S501 (they stay true for v7.2, the version they name).
- `panic_on_unrecoverable_memory_failure` (new in v7.3 vm.rst) is a kill/panic surface; it is a lead for mori's
  kill-event frontier, not a claim of this entry.

