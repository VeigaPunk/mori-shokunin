# MemAvailable is the kernel's estimate of startable memory, not a count of free pages

source: S492 — https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst — docs, tier A, Documentation/filesystems/proc.rst at tag v7.2 (the /proc/meminfo field definitions), opened 2026-10-26
source: S493 — https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/show_mem.c — code, tier A, mm/show_mem.c at tag v7.2 (si_mem_available, the estimate), opened 2026-10-26
source: S494 — https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/meminfo.c — code, tier A, fs/proc/meminfo.c at tag v7.2 (how the meminfo lines are printed), opened 2026-10-26
source: S495 — https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/mm_inline.h — code, tier A, include/linux/mm_inline.h at tag v7.2 (which folios sit on the file LRU lists), opened 2026-10-26
source: S496 — https://github.com/torvalds/linux/commit/34e431b0ae398fc54ea69ff85ec700722c9da773.patch — code, tier A, the 2014 commit that added MemAvailable (its stated motivation), opened 2026-10-26
verified-at: 2026-10-26
recheck: on-release — `for u in https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/show_mem.c https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/meminfo.c https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/mm_inline.h https://github.com/torvalds/linux/commit/34e431b0ae398fc54ea69ff85ec700722c9da773.patch; do curl -fsSL "$u" | sha256sum; done` -> e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126, dba76b263bbdf93323a277a29c9281a892ff3fb35ddd6f0ddaf9ba1acb5b02f5, d6c5807421a69eac21efd737b39d099c711b3132b371dc34986d181746e3deda, 2d4accbbc1ec139bfe11a356d4d17a55a2543769f3e10057a8a8584429c45ef6, 9f571a04fc365858d8c82d31b309217a5e40f37877732da70416b0b1b42563d0 in that order (ran 2026-10-26; all five matched the committed copies under `corpus/evidence/sources-r51/`)
coverage-map: resource runway (new ground; no FR row held it)

mori reports resource runway: how much memory the host can still give to a new seat before it swaps or kills.
The lane's census fill arm prints `MemAvailable/MemTotal` as `host_mem_avail_pct` (`tools/mori-census.sh:1791-1793`),
and the fleet's hyaku orchestration reads the same line for its own spawn and wave-grant gates (fleet-owned
`scripts/hyaku/inline-dispatcher.py`, `scripts/hyaku/wave-slot.sh`; read, never edited, by this lane). This entry
says what that number is at kernel v7.2: an estimate computed by `si_mem_available()` (`show_mem.c.v7.2:32-72`) from
free pages, the file LRU lists, reclaimable kernel memory and the zones' low watermarks, printed in kB by
`meminfo.c.v7.2:62`.

## Claims

| claim | source | quote |
|---|---|---|
| The proc documentation defines MemAvailable as an estimate for starting new applications, not as a count of free pages. | S492 | `An estimate of how much memory is available for starting new applications, without swapping.` |
| The documentation names the inputs of that estimate as free memory, reclaimable slab, the file LRU list sizes and each zone's low watermark. | S492 | `Calculated from MemFree, SReclaimable, the size of the file LRU lists, and the low watermarks in each zone.` |
| The documentation itself warns that how much cache and slab is really reclaimable differs between machines, so the figure is a model rather than a measurement. | S492 | `The impact of those factors will vary from system to system.` |
| The Cached line of /proc/meminfo counts tmpfs and shmem pages together with ordinary file page cache. | S492 | `In-memory cache for files read from the disk (the pagecache) as well as tmpfs & shmem.` |
| The Shmem line reports the memory held by shared memory segments and tmpfs files as one figure. | S492 | `Total memory used by shared memory (shmem) and tmpfs` |
| The estimate begins with the free page count minus totalreserve_pages, then adds file cache and reclaimable slab. | S493 | `without causing swapping or OOM. */ available = global_zone_page_state(NR_FREE_PAGES) - totalreserve_pages;` |
| Only the active and inactive file LRU lists enter the estimate as page cache; nothing else that Cached counts is added. | S493 | `cache, needs to stay. */ pagecache = global_node_page_state(NR_ACTIVE_FILE) + global_node_page_state(NR_INACTIVE_FILE);` |
| From that file cache the code withholds the smaller of half the cache and the summed low watermarks, then adds the remainder. | S493 | `pagecache -= min(pagecache / 2, wmark_low); available += pagecache;` |
| The kernel's stated reason for holding cache back is that freeing all of it would drive the system into swapping or thrashing. | S493 | `Not all the page cache can be freed, otherwise the system will * start swapping or thrashing.` |
| Reclaimable slab and other reclaimable kernel memory are added under the same rule: withhold the smaller of half and the low watermark sum. | S493 | `reclaimable -= min(reclaimable / 2, wmark_low); available += reclaimable;` |
| The holdback on that kernel term exists because some reclaimable slab objects are still in use and cannot be freed. | S493 | `Part of the reclaimable slab and other kernel memory consists of * items that are in use, and cannot be freed.` |
| A negative result is clamped to zero, so the returned estimate is never negative when the reserves exceed everything counted. | S493 | `if (available < 0) available = 0; return available;` |
| The watermark used for both holdbacks is the low watermark summed over every memory zone of the machine. | S493 | `struct zone *zone; for_each_zone(zone) wmark_low += low_wmark_pages(zone);` |
| The meminfo printer defines one helper that shifts its argument by PAGE_SHIFT minus 10 and writes the kB suffix. | S494 | `seq_put_decimal_ull_width(m, s, num << (PAGE_SHIFT - 10), 8); seq_write(m, " kB\n", 4);` |
| The Cached figure is computed from all file pages minus swap cache and buffers, and clamped at zero if negative. | S494 | `cached = global_node_page_state(NR_FILE_PAGES) - total_swapcache_pages() - i.bufferram;` |
| MemFree prints the sysinfo free count while MemAvailable prints the separately computed estimate, as two adjacent lines. | S494 | `show_val_kb(m, "MemFree: ", i.freeram); show_val_kb(m, "MemAvailable: ", available);` |
| The LRU sorting helper returns zero for tmpfs folios, which places them on an anon LRU list instead of a file list. | S495 | `0 if @folio is a normal anonymous folio, a tmpfs folio or otherwise * ram or swap backed folio.` |
| The file LRU lists hold regular filesystem page cache and also anonymous pages lazily freed through MADV_FREE. | S495 | `1 if @folio is a regular filesystem backed page cache folio * or a lazily freed anonymous folio (e.g. via MADV_FREE).` |
| The 2014 commit says workload placers estimated free memory by summing free and cached, which it calls outdated. | S496 | `They generally do this by adding up "free" and "cached", which was fine ten years ago,` |
| That commit's reason the sum misleads is that Cached includes shared memory, tmpfs and ramfs pages that cannot be dropped like cache. | S496 | `It is wrong because Cached includes memory that is not freeable as page cache, for example shared memory segments, tmpfs, and ramfs,` |
| The commit put the estimate into meminfo so that monitoring programs need not model reclaim internals themselves. | S496 | `user space really should not be expected to know kernel internals to come up with an estimate for the amount of free memory.` |

## Reading rules

- Read `MemAvailable` itself for runway; never rebuild it as `MemFree + Cached`. The 2014 commit names that sum as
  the wrong estimate (rows 19, 20): `Cached` counts tmpfs and shmem pages (row 4), which sit on anon LRU lists
  (row 17) that the estimate does not add (row 7), and it leaves out the reclaimable slab the estimate does add
  (row 10). On one host capture the sum read 13–15 % below `MemAvailable`, driven by reclaimable slab, with `Shmem`
  a few MB (`.ufo/waves/round-51/w1/Mo51ExecHostMeminfo.md`); the direction of the error is host-dependent.
- The estimate has no swap term (row 1 says "without swapping"; rows 6-13 add no swap figure). A reading of 0 is the
  clamp (row 12), not an exact zero.
- `MemAvailable`, `MemFree`, `Cached` and `Shmem` print in kB through the one shift helper (rows 14, 16); not every
  meminfo line does (`meminfo.c.v7.2:93-95,111-112,127-128,137-138` use `seq_printf`, and the `HugePages_*` lines
  printed by `hugetlb_report_meminfo` are counts). A ratio `MemAvailable/MemTotal` is unit-free.
- When `Cached` is large but `MemAvailable` is small, compare `Shmem`: tmpfs and shared memory raise `Cached`
  without raising the estimate [INFERENCE from rows 4, 5, 7, 17 — not measured on this host].
- A runway threshold on `MemAvailable` is a threshold on a model whose holdbacks are min(half, low-watermark sum)
  (rows 8, 10, 13), and the low watermark includes the runtime `watermark_boost`; the proc document says the
  model's accuracy varies by system (row 3). Report the threshold as local, as the lane already does for its other
  thresholds (FR8). The operands are read one after another, not as one snapshot (`meminfo.c.v7.2:44-56`), so a
  gate reads a moving value.

## Boundaries

- Detection and report only: this entry reads `/proc/meminfo`; it never changes `vm.min_free_kbytes`,
  `watermark_scale_factor`, swap or any limit. OS state is tsukuroi's to diagnose and the operator's to change
  (`../tsukuroi-shokunin/PROVINCE.md:8-14,28`); the orchestration's floors are the orchestrator's.
- v7.2 only. The estimate comes from the 2014 commit (S496), and its two `min(half, wmark_low)` holdbacks survive
  verbatim, but other inputs changed since (S496 shows only the 2014 code; the tag-by-tag reads are in
  `.ufo/waves/round-51/w1/Mo51ExecPatchVsV72.md`): the free term subtracts `totalreserve_pages` instead of the
  low-watermark sum from v4.5 on, reclaimable kernel memory adds `NR_KERNEL_MISC_RECLAIMABLE` from v4.20 on, the
  slab counter is the byte-based `NR_SLAB_RECLAIMABLE_B` from v5.9 on, and `low_wmark_pages()` includes
  `watermark_boost` from v5.0 on. This entry claims only the v7.2 bytes.
- No host value is claimed as typical. `/proc/meminfo` alone cannot reproduce the estimate: it needs the per-zone
  `low`, `high`, `protection` and `managed` figures of `/proc/zoneinfo` as well; one read-only host check with those
  inputs reproduced `MemAvailable` to the page at four of five samples
  (`.ufo/waves/round-51/w1/Mo51ExecHostMeminfo.md`).

## What this changes for mori

- `surfaces-r7.md:83-85`, `observability-surfaces-r2.md:234-235`: the census grades `host_mem_avail_pct` against a
  local 10 % floor; rows 1, 6, 8 and 13 make that value a model, so a low row is not by itself pressure [INFERENCE].
- `system-pressure-r24.md:176`: PSI `avg10` is decayed stall time, not startable bytes — `PRESSURE_OK` is no runway.
- `userspace-oom-killers-r26.md:57-60`: earlyoom's "mem avail %" divides by `MemAvailable + AnonPages`, not
  `MemTotal`, so it is not the census figure.
- `harness-job-capacity-r25.md:178`: that gate's floor (`6144`, MiB despite the "MB" label — `int(kB/1024)`) and the
  census's 10 % read the same estimate in two units; neither is calibrated off this host (row 3).
