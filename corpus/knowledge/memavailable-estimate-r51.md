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
The fleet's dispatcher stops spawning seats when `MemAvailable` drops below a floor, and the lane's census and
pressure probes print `MemAvailable/MemTotal`. This entry says what that number is at kernel v7.2: an estimate
computed by `si_mem_available()` (`show_mem.c.v7.2:32-72`) from free pages, the file LRU lists, reclaimable
kernel memory and the zones' low watermarks, printed in kB by `meminfo.c.v7.2:62`.

## Claims

| claim | source | quote |
|---|---|---|
| The proc documentation defines MemAvailable as an estimate for starting new applications, not as a count of free pages. | S492 | `An estimate of how much memory is available for starting new applications, without swapping.` |
| The documentation names the inputs of that estimate as free memory, reclaimable slab, the file LRU list sizes and each zone's low watermark. | S492 | `Calculated from MemFree, SReclaimable, the size of the file LRU lists, and the low watermarks in each zone.` |
| The documentation itself warns that how much cache and slab is really reclaimable differs between machines, so the figure is a model rather than a measurement. | S492 | `The impact of those factors will vary from system to system.` |
| The Cached line of /proc/meminfo counts tmpfs and shmem pages together with ordinary file page cache. | S492 | `In-memory cache for files read from the disk (the pagecache) as well as tmpfs & shmem.` |
| The Shmem line reports the memory held by shared memory segments and tmpfs files as one figure. | S492 | `Total memory used by shared memory (shmem) and tmpfs` |
| The estimate starts from the free page count minus totalreserve_pages, the pages the kernel holds back from userspace allocations. | S493 | `without causing swapping or OOM. */ available = global_zone_page_state(NR_FREE_PAGES) - totalreserve_pages;` |
| Only the active and inactive file LRU lists enter the estimate as page cache; nothing else that Cached counts is added. | S493 | `cache, needs to stay. */ pagecache = global_node_page_state(NR_ACTIVE_FILE) + global_node_page_state(NR_INACTIVE_FILE);` |
| From that file cache the code withholds the smaller of half the cache and the summed low watermarks, then adds the remainder. | S493 | `pagecache -= min(pagecache / 2, wmark_low); available += pagecache;` |
| The kernel's stated reason for holding cache back is that freeing all of it would drive the system into swapping or thrashing. | S493 | `Not all the page cache can be freed, otherwise the system will * start swapping or thrashing.` |
| Reclaimable slab and other reclaimable kernel memory are added under the same rule: withhold the smaller of half and the low watermark sum. | S493 | `reclaimable -= min(reclaimable / 2, wmark_low); available += reclaimable;` |
| The holdback on that kernel term exists because some reclaimable slab objects are still in use and cannot be freed. | S493 | `Part of the reclaimable slab and other kernel memory consists of * items that are in use, and cannot be freed.` |
| A negative result is clamped, so the line reads zero instead of a negative figure when the reserves exceed everything counted. | S493 | `if (available < 0) available = 0; return available;` |
| The watermark used for both holdbacks is the low watermark summed over every memory zone of the machine. | S493 | `struct zone *zone; for_each_zone(zone) wmark_low += low_wmark_pages(zone);` |
| Every meminfo value goes through one helper that shifts a page count by PAGE_SHIFT minus 10 and prints the result in kB. | S494 | `seq_put_decimal_ull_width(m, s, num << (PAGE_SHIFT - 10), 8); seq_write(m, " kB\n", 4);` |
| The Cached figure is computed from all file pages minus swap cache and buffers, a different base from the two file LRU lists. | S494 | `cached = global_node_page_state(NR_FILE_PAGES) - total_swapcache_pages() - i.bufferram;` |
| MemFree prints the sysinfo free count while MemAvailable prints the separately computed estimate, as two adjacent lines. | S494 | `show_val_kb(m, "MemFree: ", i.freeram); show_val_kb(m, "MemAvailable: ", available);` |
| The LRU sorting helper returns zero for tmpfs folios, which places them on an anon LRU list instead of a file list. | S495 | `0 if @folio is a normal anonymous folio, a tmpfs folio or otherwise * ram or swap backed folio.` |
| The file LRU lists hold regular filesystem page cache and also anonymous pages lazily freed through MADV_FREE. | S495 | `1 if @folio is a regular filesystem backed page cache folio * or a lazily freed anonymous folio (e.g. via MADV_FREE).` |
| The 2014 commit says workload placers estimated free memory by summing free and cached, which it calls outdated. | S496 | `They generally do this by adding up "free" and "cached", which was fine ten years ago,` |
| That commit's reason the sum misleads is that Cached includes shared memory, tmpfs and ramfs pages that cannot be dropped like cache. | S496 | `It is wrong because Cached includes memory that is not freeable as page cache, for example shared memory segments, tmpfs, and ramfs,` |
| The commit put the estimate into meminfo so that monitoring programs need not model reclaim internals themselves. | S496 | `user space really should not be expected to know kernel internals to come up with an estimate for the amount of free memory.` |

## Reading rules

- Read `MemAvailable` itself for runway; never rebuild it as `MemFree + Cached` — that sum counts tmpfs and shmem
  pages that sit on anon LRU lists and that the estimate does not add (rows 4, 7, 17, 20).
- The figure excludes swap by construction ("without swapping"): a host with free swap can keep running past
  `MemAvailable = 0`, and a reading of 0 is a clamp, not an exact zero (rows 1, 12).
- Units are kB on every meminfo line (row 14); a ratio `MemAvailable/MemTotal` is unit-free.
- When `Cached` is large but `MemAvailable` is small, compare `Shmem`: tmpfs and shared memory raise `Cached`
  without raising the estimate [INFERENCE from rows 4, 5, 7, 17 — not measured on this host].
- A runway threshold on `MemAvailable` is a threshold on a model whose holdbacks are min(half, low-watermark sum);
  the proc document says the model's accuracy varies by system (row 3). Report the threshold as local, as the lane
  already does for its other thresholds (FR8).

## Boundaries

- Detection and report only: this entry reads `/proc/meminfo`; it never changes `vm.min_free_kbytes`,
  `watermark_scale_factor`, swap or any limit (host configuration is tsukuroi's; the dispatcher's floor is the
  orchestrator's).
- v7.2 only. The formula has had the same shape since the 2014 commit's patch (S496), but this entry claims only
  the v7.2 bytes.
- No host value is claimed as typical; `totalreserve_pages` is not exported to userspace as one line, so the
  estimate cannot be recomputed exactly from `/proc/meminfo` alone.
