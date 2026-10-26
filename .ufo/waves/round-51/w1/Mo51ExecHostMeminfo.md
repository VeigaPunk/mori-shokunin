# Mo51ExecHostMeminfo — host falsifier of the C2 entry's formula reading

Seat: read-only falsifier of `corpus/knowledge/memavailable-estimate-r51.md` (C2) on this host. I did not edit
`corpus/`, `tools/`, the counter, the contract or any other seat's files; this report is my only write outside
scratch. No subagents, no builds, no tests.

Host: `uname -r` -> `7.2.11-arch1-1` (MACHINE_ID: the workstation this seat ran on; `MemTotal: 31721796 kB` =
30.25 GiB, one NUMA node `Node 0` with zones DMA, DMA32, Normal, Movable, Device).
Scratch: `/fast/scratch/hyaku/mori-r51/Mo51ExecHostMeminfo/` (TMPDIR `/fast/scratch/hyaku/mori-r51/Mo51ExecHostMeminfo/tmp`),
removed at the end of this seat (`rm -rf`, rc 0); every number below is copied into this report before removal.
Disk guard before the run: `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` -> `/fast/scratch/hyaku`
25 % used, 602.5 G free. Tool installs: none (nothing installed or upgraded in this seat).

## 1. Commands and exit status

```
$ uname -r
7.2.11-arch1-1
$ cd /fast/scratch/hyaku/mori-r51/Mo51ExecHostMeminfo
$ for i in 1 2; do cat /proc/meminfo > meminfo.$i.txt; cat /proc/zoneinfo > zoneinfo.$i.txt; \
    cat /proc/vmstat > vmstat.$i.txt; [ "$i" = 1 ] && sleep 1; done
   # rc 0 (no error reported); sizes: meminfo 1671 B each, zoneinfo 21912/21940 B, vmstat 4477 B each
$ curl -fsSL -o page_alloc.c.v7.2 https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/page_alloc.c
curl_rc=0    sha256 439ae8ec1e47cbf38770865e53e98bf2229e32a20c4b0f8178e6f19f34edbc50
$ curl -fsSL -o mmzone.h.v7.2 https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/mmzone.h
curl_rc=0    sha256 9699e974744414bb37e62f5a3c43ff2691b974ef49e581c11c9fb3578b058ded
```

Three extra bracketed snapshots (rounds 3–5) were taken to separate `MemAvailable` from read-order drift: each round
reads `MemFree/MemAvailable/SReclaimable` (`mi.K.a`), then the zoneinfo watermark lines (`zi.K`), then the five vmstat
counters (`vi.K`), then `MemFree/MemAvailable/SReclaimable` again (`mi.K.b`); measured span per round
5106500 / 4805969 / 3682330 ns.

## 2. Source bytes used (fetched v7.2, quoted as read)

`algorithm: the formula`, `mm/show_mem.c` v7.2:32-72 (the committed copy
`/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r51/show_mem.c.v7.2`):

```
  32 long si_mem_available(void)
  40 	for_each_zone(zone)
  41 		wmark_low += low_wmark_pages(zone);
  47 	available = global_zone_page_state(NR_FREE_PAGES) - totalreserve_pages;
  54 	pagecache = global_node_page_state(NR_ACTIVE_FILE) +
  55 		global_node_page_state(NR_INACTIVE_FILE);
  56 	pagecache -= min(pagecache / 2, wmark_low);
  57 	available += pagecache;
  64 	reclaimable = global_node_page_state_pages(NR_SLAB_RECLAIMABLE_B) +
  65 		global_node_page_state(NR_KERNEL_MISC_RECLAIMABLE);
  66 	reclaimable -= min(reclaimable / 2, wmark_low);
  67 	available += reclaimable;
  69 	if (available < 0)
  70 		available = 0;
  71 	return available;
  72 }
```

`mm/page_alloc.c` v7.2, the reserve approximation (function `calculate_totalreserve_pages`, lines 6355-6397):

```
6365 		for (i = 0; i < MAX_NR_ZONES; i++) {
6366 			struct zone *zone = pgdat->node_zones + i;
6367 			long max = 0;
6368 			unsigned long managed_pages = zone_managed_pages(zone);
6378 			for (j = MAX_NR_ZONES - 1; j > i; j--) {
6379 				if (!zone->lowmem_reserve[j])
6380 					continue;
6382 				max = zone->lowmem_reserve[j];
6383 				break;
6384 			}
6385 			/* we treat the high watermark as reserved pages. */
6386 			max += high_wmark_pages(zone);
6388 			max = min_t(unsigned long, max, managed_pages);
6390 			pgdat->totalreserve_pages += max;
6392 			reserve_pages += max;
6395 	totalreserve_pages = reserve_pages;
```

`include/linux/mmzone.h` v7.2:1169-1188 (what `/proc/zoneinfo` prints as `min`/`low`/`high`):

```
1169 static inline unsigned long wmark_pages(const struct zone *z, enum zone_watermarks w)
1172 	return z->_watermark[w] + z->watermark_boost;
1180 static inline unsigned long low_wmark_pages(const struct zone *z)
1182 	return wmark_pages(z, WMARK_LOW);
1185 static inline unsigned long high_wmark_pages(const struct zone *z)
1187 	return wmark_pages(z, WMARK_HIGH);
```

`fs/proc/meminfo.c` v7.2 (read order inside one generation): `si_meminfo(&i)` at line 44, `cached = ...` at 48,
`pages[lru] = ...` at 53, `available = si_mem_available()` at **56**, `sreclaimable = ...` at 57; the prints are
`MemFree: i.freeram` at 61, `MemAvailable: available` at 62, `Cached: cached` at 64, `Active(file)`/`Inactive(file)`
at 72/73, `SReclaimable: sreclaimable` at 100.

## 3. Zones as read (sample 1; sample 2 differs only in Normal, see §5)

| zone | managed | min | low | high | protection: (…) |
|---|---|---|---|---|---|
| DMA | 3840 | 8 | 56 | 104 | (0, 1910, 30963, 30963, 30963) |
| DMA32 | 489126 | 1042 | 7156 | 13270 | (0, 0, 29052, 29052, 29052) |
| Normal | 7437483 | 15845 | 108813 | 201781 | (0, 0, 0, 0, 0) |
| Movable | 0 | 32 | 32 | 32 | (0, 0, 0, 0, 0) |
| Device | 0 | 0 | 0 | 0 | (0, 0, 0, 0, 0) |

Derived: `wmark_low = 56 + 7156 + 108813 + 32 + 0 = 116057` pages; `totalreserve_pages` per zone =
max(nonzero `lowmem_reserve` of higher zones) + `high`, capped at `managed`:
DMA `min(30963+104, 3840) = 3840` (cap binds), DMA32 `29052+13270 = 42322`, Normal `0+201781 = 201781`,
Movable `min(0+32, 0) = 0`, Device `0`; sum **247943 pages** = 991772 kB of `MemTotal` 31721796 kB.

## 4. Recomputation vs the printed line (formula applied per show_mem.c:32-72)

All values in pages (PAGE_SIZE 4096, meminfo kB / 4); inputs from the same snapshot's `meminfo` where the kernel takes
them (`MemFree`, `Active(file)+Inactive(file)`, `SReclaimable`) and the zone sums above.

| sample | `MemFree` pages | file LRU pages | `SReclaimable` pages | wmark_low | totalreserve | computed | printed `MemAvailable` | diff |
|---|---|---|---|---|---|---|---|---|
| 1 (meminfo.1+zoneinfo.1) | 700960 | 3057444 | 1058755 | 116057 | 247943 | 4337102 pp = **17348408 kB** | 17348408 kB | **0 kB (0 pp)** |
| 2 (meminfo.2+zoneinfo.2) | 427817 | 3217634 | 1070788 | 125785 (boost 9728) | 257671 | 4206998 pp = 16827992 kB | 16866904 kB | **−38912 kB (−9728 pp)** |
| 3 (mi.3.a+zi.3) | 623049 | 3064636 | 1150819 | 116057 | 247943 | 4358447 pp = **17433788 kB** | 17433788 kB | **0 kB** |
| 4 (mi.4.a+zi.4) | 635900 | 3050473 | 1150819 | 116057 | 247943 | 4357135 pp = **17428540 kB** | 17428540 kB | **0 kB** |
| 5 (mi.5.a+zi.5) | 647460 | 3043794 | 1150819 | 116057 | 247943 | 4362016 pp = **17448064 kB** | 17448064 kB | **0 kB** |

Sample 1 trace (the four terms, exactly as the code orders them):
`700960 − 247943 = 453017`; `pagecache = 3057444 − min(1528722, 116057) = 2941387`; `453017 + 2941387 = 3394404`;
`reclaimable = 1058755 − min(529377, 116057) = 942698`; `3394404 + 942698 = 4337102 pp = 17348408 kB`, equal to the
printed `MemAvailable: 17348408 kB` to the page, clamp not triggered.

Cross-checks that the meminfo lines are the formula's own operands (sample 1): `nr_file_pages 3252750 −
nr_swapcached 193050 − Buffers 9 = 3059691` pp = `Cached: 12238764 kB` = 3059691 pp exactly; `nr_active_file 59343`
+ `nr_inactive_file 2998101` = 3057444 pp = `Active(file) 237372 + Inactive(file) 11992404` kB / 4 exactly;
`nr_slab_reclaimable 1058755` pp = `SReclaimable 4235020` kB / 4 exactly; `nr_kernel_misc_reclaimable 0`.

Discriminating details the exact match confirms on this host:
- the DMA zone's reserve is capped at its `managed` (31067 -> 3840); uncapped, computed would be 27227 pp low;
- the two zero-populated zones are still summed into `wmark_low` (Movable `low 32`); dropping that 32 makes computed
  16 pp high and breaks the page-exact match.

## 5. The one non-zero residual, and why it is not a formula mismatch

Sample 2 is the only snapshot whose `/proc/zoneinfo` showed a non-zero `watermark_boost`:
`Node 0, zone Normal`, `boost 9728`, `min 25573` (15845+9728), `low 118541` (108813+9728), `high 211509`
(201781+9728). `wmark_pages()` adds `watermark_boost` (mmzone.h.v7.2:1172), so the printed `low`/`high` move with a
runtime transient. Using the boosted values, the recomputation is 9728 pp (38912 kB) **below** the printed line;
using the same snapshot's meminfo with the unboosted watermarks it is 19456 pp (77824 kB) **above**. The printed
value lies between the two reconstructions, i.e. the boost changed between the meminfo generation and the zoneinfo
read, and/or free pages moved between `si_meminfo()` (meminfo.c:44) and `si_mem_available()` (meminfo.c:56).
The host moves that fast: in the bracketed rounds (≈4 ms apart) `MemFree` changed by +27692 kB, +31156 kB and
−12212 kB, and `MemAvailable` by −3472 kB, +4440 kB and −11368 kB.

## 6. Inputs I could not read exactly

- `totalreserve_pages`: no `/proc` or `/sys` line exposes it; recomputed per `calculate_totalreserve_pages` from
  `/proc/zoneinfo` (`protection`, `high`, `managed`). At four snapshots the recomputation lands on the printed
  `MemAvailable` to the page, which is the only evidence that the approximation is right at that instant; it does not
  prove it at an instant when `lowmem_reserve_ratio`, `min_free_kbytes` or hotplug change between reads.
- `wmark_low`: per-zone `low` is readable, but as printed it includes `zone->watermark_boost`, a transient; the value
  the estimate used cannot be sampled exactly (sample 2, §5). Whether `for_each_zone` includes zero-populated zones
  is not stated by any file; the page-exact match shows it does here (Movable `low` 32 is summed).
- `NR_FREE_PAGES` at the estimate instant: `MemFree` is captured earlier in the same generation (meminfo.c:44 vs 56);
  `nr_free_pages` in `/proc/vmstat` is a later, separate sample (sample 1: 700633 pp vs `MemFree`/4 = 700960 pp;
  sample 2: 427381 vs 427817).
- Node vs global counters: this host has one node (Node 0), so `global_node_page_state` and the `/proc/vmstat` totals
  coincide here and the distinction is untested.
- `/proc/zoneinfo` `managed` is taken as `zone_managed_pages()` (page_alloc.c:6368). The cap binds for DMA, so the
  page-exact match requires those bytes to be the same value; I did not read the field definition in `vmstat.c`.

## 7. `MemFree + Cached` vs `MemAvailable`, and `Shmem`

| sample | `MemFree` | `Cached` | sum | `MemAvailable` | sum − avail | `Shmem` |
|---|---|---|---|---|---|---|
| 1 | 2803840 | 12238764 | 15042604 kB | 17348408 kB | **−2305804 kB (−13.29 %)** | 7024 kB (0.057 % of Cached) |
| 2 | 1711268 | 12879472 | 14590740 kB | 16866904 kB | −2276164 kB (−13.49 %) | 6980 kB (0.054 %) |
| 3 | 2492196 | 12264364 | 14756560 kB | 17433788 kB | −2677228 kB (−15.36 %) | 3520 kB (0.029 %) |
| 4 | 2543600 | 12207712 | 14751312 kB | 17428540 kB | −2677228 kB (−15.36 %) | 3520 kB (0.029 %) |
| 5 | 2589840 | 12180996 | 14770836 kB | 17448064 kB | −2677228 kB (−15.34 %) | 3520 kB (0.029 %) |

On this host the sum is an **under**-read by 2.3–2.7 GB, because the estimate adds `reclaimable − wmark_low`
(942698 pp = 3.77 GB at sample 1) and the pages the sum wrongly counts are small: `Cached − file LRU` is 8988 kB
(sample 1: 12238764 vs 12229776 kB) and only 7024 kB of that is `Shmem`; `KReclaimable` is 4235020–4603276 kB.
So the commit's stated mechanism (S496 rows: Cached includes tmpfs/shmem that is not freeable) is visible but tiny
here, and the dominant term making the sum wrong is the one the estimate adds, not the one it withholds.

No host value above is offered as typical; this is one 30.25 GiB single-node machine under heavy fleet load, and every
number in the tables moved between snapshots.

## 8. Entry checks inside my scope

- `show_mem.c.v7.2:32-72` (entry line 15) is exact: `si_mem_available` opens at 32 and closes at 72 in the committed
  copy; the clamp is at 69-70 inside that range.
- `meminfo.c.v7.2:62` (entry line 16) is the `MemAvailable` print; the kB helper itself is at 28-32 of that copy.
- Entry row 34 (low watermark summed over every zone) and rows 29/31 (both holdbacks are `min(half, wmark_low)`) hold
  on this host: the sums, caps and clamps reproduce the printed line to the page at four snapshots.
- Entry lines 64-65 ("cannot be recomputed exactly from `/proc/meminfo` alone") is true; adding `/proc/zoneinfo` and
  `/proc/vmstat` makes it exact here (4/5 snapshots), which the entry does not say.

## Findings

1. **MED** — the formula reading is confirmed to the page on this host (4/5 snapshots, 0 kB difference), but the
   `/proc/zoneinfo` watermarks it uses are boost-adjusted (`mmzone.h.v7.2:1169-1188`) and the boost changes at
   runtime: Normal `boost 9728` appeared between two reads 1 s apart, and the sample that used the boosted values
   differs by exactly one boost quantum (38912 kB). Entry `corpus/knowledge/memavailable-estimate-r51.md:44-55`
   (Reading rules) and the row at :34 do not name `watermark_boost`; a recomputation that samples zoneinfo at a
   different instant than meminfo can be off by up to that transient. Optional correction for the L1 (data, not
   counter): one sentence in Reading rules naming the boost and the need to sample meminfo and zoneinfo together.
2. **MED** — entry `corpus/knowledge/memavailable-estimate-r51.md:64-65` says the estimate cannot be recomputed
   exactly from `/proc/meminfo` alone. Observed: it cannot, but with `/proc/zoneinfo` (`protection`, `high`,
   `managed`, `low`) plus `/proc/vmstat` it reproduces `MemAvailable` to the page at four snapshots. The entry names
   neither input; optional addition, not a wrong claim.
3. **MED** — the estimate's operands are not one atomic snapshot: `fs/proc/meminfo.c` v7.2 computes `MemFree` at :44,
   `Cached` at :48, the LRU array at :53 and `available` at :56, and the host moved `MemFree` 12–31 MB in ≈4 ms during
   this seat (bracketed rounds 3–5). Any runway gate on `MemAvailable` (the dispatcher's `MEM_MIN_GB`) reads a
   moving estimate; this is a property of the number, not an entry error.
4. **LOW** — `MemFree + Cached` is 2.3–2.7 GB **below** `MemAvailable` on this host (13–15 %), dominated by the
   reclaimable-slab term the estimate adds, while `Shmem` (3.5–7 MB; 0.03–0.06 % of `Cached`) makes the sum wrong
   only marginally. Entry `corpus/knowledge/memavailable-estimate-r51.md:46-47` is correct that the sum must not be
   used, but the observed direction of the error is under-, not over-, reading; no change required.
5. **LOW** — `totalreserve_pages` is not readable (no procfs/sysfs line); my approximation (247943 pp = 991772 kB,
   3.1 % of `MemTotal`) is validated only by the page-exact match at four snapshots, so a later seat
   recomputing on another host cannot verify it the same way without the same match test.
6. **LOW** — entry line 15/16 citations verified (`show_mem.c.v7.2:32-72`, `meminfo.c.v7.2:62`); no defect found in
   the two line references I was asked to check.

No blocker. Scratch removed; nothing under `/tmp` was used as evidence.
