# Mo51ExecPatchVsV72 — si_mem_available: the 2014 patch against v7.2

Seat: Mo51ExecPatchVsV72 (executor, leaf). Item: diff the estimate's formula across time; extract the body from the
2014 patch (`corpus/evidence/sources-r51/34e431b0.patch`, where it lived inline in `fs/proc/meminfo.c`) and from
v7.2 (`corpus/evidence/sources-r51/show_mem.c.v7.2:32-72`), print both normalised side by side, list each change,
and rule on the entry's Boundaries sentence "The formula has had the same shape since the 2014 commit's patch".

Repo state read, not written: lane at `87e0c374537557754bf71dd68036ded3ddc6699c` (data); no lane file, no corpus
file, no tool, no counter was modified. Scratch: `/fast/scratch/hyaku/mori-r51/Mo51ExecPatchVsV72/` (created, used,
removed — see §7). No tool installed or upgraded this seat (`curl`, `python3` only; pacman not run, host-wide pause
respected). Disk guard checked before the network reads: `/fast/scratch/hyaku` 25 % used, 603.9 G free, rc 0.

Bytes I read are the frozen copies confirmed by hash:

```
$ sha256sum 34e431b0.patch show_mem.c.v7.2
9f571a04fc365858d8c82d31b309217a5e40f37877732da70416b0b1b42563d0  34e431b0.patch
dba76b263bbdf93323a277a29c9281a892ff3fb35ddd6f0ddaf9ba1acb5b02f5  show_mem.c.v7.2
```

(second value equals the entry's second `recheck:` hash; first equals the truncated fifth hash `9f571a04fc365858…`).
Citation check: `show_mem.c.v7.2:32-72` is exact — `32: long si_mem_available(void)` opens the function, `73:
EXPORT_SYMBOL_GPL(si_mem_available);` closes it, so the cited range is the whole function. No defect there.

## 1. Normalised side by side

Extractor: `/fast/scratch/hyaku/mori-r51/Mo51ExecPatchVsV72/cmp.py` (reads the two committed copies, strips
`/* */` comments, blank lines and indentation, splits on `;`). Command and exit code:

```
$ python3 cmp.py
rc=0
```

Output (verbatim):

```
=== 2014 patch (fs/proc/meminfo.c, added lines) — normalised statements
  1. for_each_zone(zone) wmark_low += zone->watermark[WMARK_LOW];
  2. available = i.freeram - wmark_low;
  3. pagecache = pages[LRU_ACTIVE_FILE] + pages[LRU_INACTIVE_FILE];
  4. pagecache -= min(pagecache / 2, wmark_low);
  5. available += pagecache;
  6. available += global_page_state(NR_SLAB_RECLAIMABLE) - min(global_page_state(NR_SLAB_RECLAIMABLE) / 2, wmark_low);
  7. if (available < 0) available = 0;

=== v7.2 mm/show_mem.c:32-72 (si_mem_available) — normalised statements
  1. for_each_zone(zone) wmark_low += low_wmark_pages(zone);
  2. available = global_zone_page_state(NR_FREE_PAGES) - totalreserve_pages;
  3. pagecache = global_node_page_state(NR_ACTIVE_FILE) + global_node_page_state(NR_INACTIVE_FILE);
  4. pagecache -= min(pagecache / 2, wmark_low);
  5. available += pagecache;
  6. reclaimable = global_node_page_state_pages(NR_SLAB_RECLAIMABLE_B) + global_node_page_state(NR_KERNEL_MISC_RECLAIMABLE);
  7. reclaimable -= min(reclaimable / 2, wmark_low);
  8. available += reclaimable;
  9. if (available < 0) available = 0;
 10. return available;
 11. };

=== side by side (aligned by nearest match) ===
2014 patch                                                                                       | v7.2
-------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------
~ for_each_zone(zone) wmark_low += zone->watermark[WMARK_LOW];                                     | for_each_zone(zone) wmark_low += low_wmark_pages(zone);
~ available = i.freeram - wmark_low;                                                               | available = global_zone_page_state(NR_FREE_PAGES) - totalreserve_pages;
~ pagecache = pages[LRU_ACTIVE_FILE] + pages[LRU_INACTIVE_FILE];                                   | pagecache = global_node_page_state(NR_ACTIVE_FILE) + global_node_page_state(NR_INACTIVE_FILE);
  pagecache -= min(pagecache / 2, wmark_low);                                                      | pagecache -= min(pagecache / 2, wmark_low);
  available += pagecache;                                                                          | available += pagecache;
~ available += global_page_state(NR_SLAB_RECLAIMABLE) - min(global_page_state(NR_SLAB_RECLAIMABLE… | reclaimable = global_node_page_state_pages(NR_SLAB_RECLAIMABLE_B) + global_node_page_state(NR_KERNEL_MISC_RECLAIMABLE);
~                                                                                                  | reclaimable -= min(reclaimable / 2, wmark_low);
~                                                                                                  | available += reclaimable;
  if (available < 0) available = 0;                                                                | if (available < 0) available = 0;
+                                                                                                  | return available;
+                                                                                                  | };

=== unified diff of normalised statement lists ===
--- 2014-patch
+++ v7.2
@@ -1,7 +1,11 @@
-for_each_zone(zone) wmark_low += zone->watermark[WMARK_LOW];
-available = i.freeram - wmark_low;
-pagecache = pages[LRU_ACTIVE_FILE] + pages[LRU_INACTIVE_FILE];
+for_each_zone(zone) wmark_low += low_wmark_pages(zone);
+available = global_zone_page_state(NR_FREE_PAGES) - totalreserve_pages;
+pagecache = global_node_page_state(NR_ACTIVE_FILE) + global_node_page_state(NR_INACTIVE_FILE);
 pagecache -= min(pagecache / 2, wmark_low);
 available += pagecache;
-available += global_page_state(NR_SLAB_RECLAIMABLE) - min(global_page_state(NR_SLAB_RECLAIMABLE) / 2, wmark_low);
+reclaimable = global_node_page_state_pages(NR_SLAB_RECLAIMABLE_B) + global_node_page_state(NR_KERNEL_MISC_RECLAIMABLE);
+reclaimable -= min(reclaimable / 2, wmark_low);
+available += reclaimable;
 if (available < 0) available = 0;
+return available;
+};

statements: 2014=7 v7.2=11 identical=False
```

(The trailing `};` at statement 11 is the extractor picking up the function's closing brace; it is not a statement.)

## 2. Each change, with the first tag that carries it

Dating method: read the same expression from `raw.githubusercontent.com/torvalds/linux/<tag>/<file>` at a ladder of
tags (§3 receipts). "First tag" means the earliest tag in that ladder showing the v7.2 form; the true commit may sit
anywhere in the preceding merge window. Commit ids below are from the GitHub commits API (path + date window), not
guessed.

| # | 2014 patch | v7.2 (mm/show_mem.c:32-72) | first tag with the v7.2 form | commit / receipt |
|---|---|---|---|---|
| 1 | body inline in `meminfo_proc_show()`, value printed by `K(available)` | exported `long si_mem_available(void)`, called from `meminfo.c.v7.2:56` and printed by `show_val_kb` | body extracted into `mm/page_alloc.c` in **v4.6**; moved to `mm/show_mem.c` in the **v6.5** window (`mm/show_mem.c` is absent at v6.0–v6.4, present at v6.5) | `d02bd27bd33d` (2016-03-17, "mm/page_alloc.c: calculate 'available' memory in a separate function"); §3 E5 |
| 2 | `wmark_low += zone->watermark[WMARK_LOW]` | `wmark_low += low_wmark_pages(zone)`, and `low_wmark_pages(z)` = `z->_watermark[WMARK_LOW] + z->watermark_boost` | **v5.0** (macro gained `watermark_boost`; v4.20 macro is still the bare field) | `a921444382b4` (2018-12-28, "mm: move zone watermark accesses behind an accessor"), `1c30844d2dfe` (2018-12-28, "mm: reclaim small amounts of memory when an external fragmentation event occurs"); v7.2 `mmzone.h:1169-1182` |
| 3 | `available = i.freeram - wmark_low` | `available = global_zone_page_state(NR_FREE_PAGES) - totalreserve_pages` | **v4.5** (`v4.4` still `- wmark_low`, `v4.5` already `- totalreserve_pages`) | `84ad5802a33a` (2016-01-15, "proc: meminfo: estimate available memory more conservatively"), patch lines `-available = i.freeram - wmark_low;` / `+available = i.freeram - totalreserve_pages;` |
| 3a | reserve subtracted was the summed zone low watermarks | `totalreserve_pages` = per-zone `max(lowmem_reserve, high_wmark_pages(zone))` capped at `zone_managed_pages`, summed over zones/nodes | v4.5 (same commit) | v7.2 `mm/page_alloc.c:6350-6396` (`calculate_totalreserve_pages`: `max += high_wmark_pages(zone); max = min_t(unsigned long, max, managed_pages); … totalreserve_pages = reserve_pages;`) |
| 4 | `pages[LRU_ACTIVE_FILE] + pages[LRU_INACTIVE_FILE]`, filled by `global_page_state(NR_LRU_BASE + lru)` over zones | `global_node_page_state(NR_ACTIVE_FILE) + global_node_page_state(NR_INACTIVE_FILE)` | accessor only | Same two file-LRU populations aggregated over all zones vs all nodes; no formula change [INFERENCE from the two counter APIs, not measured] |
| 5 | slab term inline: `available += global_page_state(NR_SLAB_RECLAIMABLE) - min(... / 2, wmark_low)`, page-unit counter, one input | named `reclaimable` = `global_node_page_state_pages(NR_SLAB_RECLAIMABLE_B)` (byte counter, converted) **plus** `global_node_page_state(NR_KERNEL_MISC_RECLAIMABLE)`; same `min(half, wmark_low)` holdback; then `available += reclaimable` | second input **v4.20** (absent v4.19); byte counter **v5.9** (v5.8 still `NR_SLAB_RECLAIMABLE`) | `d42f3245c7e2` (2020-08-07, "mm: memcg: convert vmstat slab counters to bytes"); `NR_KERNEL_MISC_RECLAIMABLE /* reclaimable non-slab kernel pages */` at `mmzone.h v4.20:185` |
| 6 | `if (available < 0) available = 0` | identical, then `return available` | unchanged | §1 diff: the two holdback lines and the clamp are byte-identical |
| 7 | comments: "without causing swapping"; separate paragraph "Free memory cannot be taken below the low watermark, before the system starts swapping."; slab comment "Part of the reclaimable **swap**…" | "without causing swapping **or OOM**"; the low-watermark paragraph deleted; "Part of the reclaimable **slab and other kernel memory**…" | comment-only, but it records change 3 (the deleted paragraph is exactly the arithmetic that 84ad5802a33a removed) and change 5 | committed copies, lines 41-58 (v7.2) vs patch added lines |

Sum: **two lines survive verbatim** (`pagecache -= min(pagecache / 2, wmark_low);`, `available += pagecache;`, and the
clamp); **three inputs changed** (free-term reserve, a second reclaimable input, the slab counter's unit), and the
per-zone low watermark now includes `watermark_boost`. The skeleton — free minus a reserve, plus file cache and
reclaimable kernel memory each held back by `min(half, wmark_low)`, clamped at 0 — is preserved.

## 3. Receipts (command, output, exit code)

**E1 — tag ladder, `fs/proc/meminfo.c` / `mm/page_alloc.c` / `mm/show_mem.c`** (rc 0; per-`curl` `--max-time 60`,
`-fsSL`, output through `grep`; in the command as run the file URL was
`https://raw.githubusercontent.com/torvalds/linux/$t/$f` and `…/` in E2-E5 stands for that prefix; `head -120`
truncated the first run after v6.1, the v6.x blocks shown are from the follow-up run):

```
$ for t in v4.4 v4.8 v4.14 v4.19 v4.20 v5.0 v5.4 v5.9 v5.10 v5.15 v6.0 v6.1 v6.6 v6.12 v6.16; do for f in fs/proc/meminfo.c mm/page_alloc.c mm/show_mem.c; do out=$(curl -fsSL --max-time 60 "…/$t/$f" 2>/dev/null | grep -n -E "^	available = |available = global_zone_page_state|reclaimable = |NR_KERNEL_MISC_RECLAIMABLE|NR_SLAB_RECLAIMABLE"); if [ -n "$out" ]; then echo "=== $t $f"; echo "$out"; fi; done; done 2>&1 | head -120
=== v4.4 fs/proc/meminfo.c
64:	available = i.freeram - wmark_low;
79:	available += global_page_state(NR_SLAB_RECLAIMABLE) -
80:		     min(global_page_state(NR_SLAB_RECLAIMABLE) / 2, wmark_low);
=== v4.8 fs/proc/meminfo.c
51:	available = si_mem_available();
=== v4.8 mm/page_alloc.c
4025:	available = global_page_state(NR_FREE_PAGES) - totalreserve_pages;
4040:	available += global_page_state(NR_SLAB_RECLAIMABLE) -
4041:		     min(global_page_state(NR_SLAB_RECLAIMABLE) / 2, wmark_low);
=== v4.14 mm/page_alloc.c
4551:	available = global_zone_page_state(NR_FREE_PAGES) - totalreserve_pages;
4566:	available += global_node_page_state(NR_SLAB_RECLAIMABLE) -
=== v4.19 mm/page_alloc.c
4717:	available = global_zone_page_state(NR_FREE_PAGES) - totalreserve_pages;
4732:	available += global_node_page_state(NR_SLAB_RECLAIMABLE) -
=== v4.20 mm/page_alloc.c
4721:	available = global_zone_page_state(NR_FREE_PAGES) - totalreserve_pages;
4737:	reclaimable = global_node_page_state(NR_SLAB_RECLAIMABLE) +
4738:			global_node_page_state(NR_KERNEL_MISC_RECLAIMABLE);
=== v5.0 mm/page_alloc.c
4892:	available = global_zone_page_state(NR_FREE_PAGES) - totalreserve_pages;
4908:	reclaimable = global_node_page_state(NR_SLAB_RECLAIMABLE) +
4909:			global_node_page_state(NR_KERNEL_MISC_RECLAIMABLE);
=== v5.4 mm/page_alloc.c
5120:	available = global_zone_page_state(NR_FREE_PAGES) - totalreserve_pages;
5136:	reclaimable = global_node_page_state(NR_SLAB_RECLAIMABLE) +
5137:			global_node_page_state(NR_KERNEL_MISC_RECLAIMABLE);
=== v5.9 mm/page_alloc.c
5246:	available = global_zone_page_state(NR_FREE_PAGES) - totalreserve_pages;
5262:	reclaimable = global_node_page_state_pages(NR_SLAB_RECLAIMABLE_B) +
5263:		global_node_page_state(NR_KERNEL_MISC_RECLAIMABLE);
=== v5.10 .. v6.4 mm/page_alloc.c    (v6.4: 5146 `long si_mem_available(void)`, 5166 `available = … - totalreserve_pages;`)
=== v6.5, v6.6, v6.12, v6.16, v6.17 mm/show_mem.c   (v6.5: 32 `long si_mem_available(void)`, 52 `available = …`, 68 `reclaimable = …`)
```

**E2 — the v4.4/v4.5/v4.6 boundary**

```
$ for t in v4.5 v4.6 v4.7; do curl -fsSL "…/$t/fs/proc/meminfo.c" | grep -n -E "si_mem_available|available = i.freeram|available = global"; done
== v4.5
61:	available = i.freeram - totalreserve_pages;
== v4.6
51:	available = si_mem_available();
== v4.7
51:	available = si_mem_available();
```

**E3 — v3.13 has no MemAvailable; v3.14 does; `i.freeram` is `NR_FREE_PAGES` in the introducing series**

```
$ curl -fsSL "…/v3.13/fs/proc/meminfo.c" | grep -c "MemAvailable"
0                                     # rc 1: grep found nothing, so v3.13 predates the feature
$ curl -fsSL "…/v3.14/fs/proc/meminfo.c" | grep -n -E "available = i.freeram|MemAvailable|NR_SLAB_RECLAIMABLE"
64:	available = i.freeram - wmark_low;
79:	available += global_page_state(NR_SLAB_RECLAIMABLE) -
80:		     min(global_page_state(NR_SLAB_RECLAIMABLE) / 2, wmark_low);
91:		"MemAvailable:   %8lu kB\n"
$ curl -fsSL "…/v3.14/mm/page_alloc.c" | grep -n -B2 -A2 "val->freeram"
3003:	val->freeram = global_page_state(NR_FREE_PAGES);
```

So the free-count source (`NR_FREE_PAGES`) is unchanged from v3.14 to v7.2 (`show_mem.c.v7.2:79`:
`val->freeram = global_zone_page_state(NR_FREE_PAGES);`); what changed in 2016 is only what is subtracted from it.

**E4 — `wmark_low` per-zone value, `include/linux/mmzone.h`**

```
== v4.8   259:#define low_wmark_pages(z) (z->watermark[WMARK_LOW])
== v4.20  273:#define low_wmark_pages(z) (z->watermark[WMARK_LOW])
== v5.0   272:#define min_wmark_pages(z) (z->_watermark[WMARK_MIN] + z->watermark_boost)
          273:#define low_wmark_pages(z) (z->_watermark[WMARK_LOW] + z->watermark_boost)
          275:#define wmark_pages(z, i) (z->_watermark[i] + z->watermark_boost)
          367:	unsigned long watermark_boost;
== v5.9   313:#define low_wmark_pages(z) (z->_watermark[WMARK_LOW] + z->watermark_boost)
== v6.0   379:#define low_wmark_pages(z) (z->_watermark[WMARK_LOW] + z->watermark_boost)
== v7.2   973:	unsigned long watermark_boost;
         1169:static inline unsigned long wmark_pages(const struct zone *z, …)
         1172:	return z->_watermark[w] + z->watermark_boost;
         1180:static inline unsigned long low_wmark_pages(const struct zone *z)
```

and the call site itself:

```
== v4.20 (mm/page_alloc.c)  4715:		wmark_low += zone->watermark[WMARK_LOW];
== v5.0  (mm/page_alloc.c)  4886:		wmark_low += low_wmark_pages(zone);
```

**E5 — where the body lived, `mm/show_mem.c` existence**

```
$ for t in v6.0 v6.1 v6.2 v6.3 v6.4 v6.5; do curl -sSL -o /tmp/mo51-sm.$$ -w "%{http_code}" "…/$t/mm/show_mem.c"; echo "$t bytes=$(wc -c < /tmp/mo51-sm.$$)"; done
v6.0 mm/show_mem.c http=404 bytes=14
v6.1 mm/show_mem.c http=404 bytes=14
v6.2 mm/show_mem.c http=404 bytes=14
v6.3 mm/show_mem.c http=404 bytes=14
v6.4 mm/show_mem.c http=404 bytes=14
v6.5 mm/show_mem.c http=200 bytes=12181
$ curl -sS "https://api.github.com/repos/torvalds/linux/contents/mm/show_mem.c?ref=v6.4"
{"message": "Not Found", … "status": "404" }
$ for t in v4.6 v4.7; do curl -fsSL "…/$t/mm/page_alloc.c" | grep -n -A3 "long si_mem_available"; done
== v4.6 mm/page_alloc.c
3732:long si_mem_available(void)
3733-{
3734-	long available;
3735-	unsigned long pagecache;
== v4.7 mm/page_alloc.c
4211:long si_mem_available(void)
4212-{
4213-	long available;
4214-	unsigned long pagecache;
```

**E6 — commit ids and dates (GitHub commits API, path + window)**

```
== fs/proc/meminfo.c 2016-01-10..2016-03-14
   84ad5802a33a 2016-01-15 proc: meminfo: estimate available memory more conservatively
== fs/proc/meminfo.c 2016-03-14..2016-05-16
   d02bd27bd33d 2016-03-17 mm/page_alloc.c: calculate 'available' memory in a separate function
== include/linux/mmzone.h 2018-12-20..2019-03-06
   a921444382b4 2018-12-28 mm: move zone watermark accesses behind an accessor
   1c30844d2dfe 2018-12-28 mm: reclaim small amounts of memory when an external fragmentation event occurs
== mm/page_alloc.c 2019-11-25..2020-10-12
   d42f3245c7e2 2020-08-07 mm: memcg: convert vmstat slab counters to bytes
```

`84ad5802a33a.patch` (fetched whole, grepped) carries the exact pair:

```
3:Date: Thu, 14 Jan 2016 15:20:18 -0800
4:Subject: [PATCH] proc: meminfo: estimate available memory more conservatively
40:-	available = i.freeram - wmark_low;
41:+	available = i.freeram - totalreserve_pages;
```

`totalreserve_pages` is not the low watermark under another name (v7.2 `mm/page_alloc.c:6350-6396`): per zone it is
`max(lowmem_reserve) + high_wmark_pages(zone)`, capped at `zone_managed_pages`, summed — the commit message says it
subtracts "the full amount we know to be unavailable to userspace".

**E7 — `34e431b0.patch` introduction window** — `v3.13` has no MemAvailable, `v3.14` does (E3), so the patch landed in
the v3.14 merge window (commit date Tue, 21 Jan 2014 15:49:05 -0800, from the patch header).

## 4. Verdict on the Boundaries sentence

Entry `corpus/knowledge/memavailable-estimate-r51.md:62-63`:

> v7.2 only. The formula has had the same shape since the 2014 commit's patch (S496), but this entry claims only the
> v7.2 bytes.

**Verdict: the citation does not support the sentence, and the sentence is imprecise about the arithmetic — it should
be replaced.** Two distinct defects:

1. **Span vs source.** S496 is the 2014 patch. It shows the 2014 code and nothing about v4.5 … v7.2, so it cannot
   source "has had the same shape since". The sentence is the entry's only claim that ranges across versions and it
   carries no evidence for the range.
2. **The arithmetic did change, and one of the changes is in a term the entry's own claims describe.** The free term
   is `available = i.freeram - wmark_low` in the 2014 patch and `… - totalreserve_pages` from v4.5 (E2, E6). At v7.2
   the summed low watermarks do not reduce free pages at all; they only cap the page-cache and reclaimable holdbacks.
   Two further input changes follow: a second reclaimable input (`NR_KERNEL_MISC_RECLAIMABLE`, v4.20) and a byte-unit
   slab counter (`NR_SLAB_RECLAIMABLE_B`, v5.9); the per-zone low watermark gained `watermark_boost` in v5.0.
   Only the two holdback lines, the clamp, and the `free − reserve + cache + reclaimable` skeleton survive verbatim.

What survives of the sentence is the skeleton reading of "shape": free minus a reserve, plus the file page cache and
reclaimable kernel memory, each held back by `min(half, wmark_low)`, clamped at zero. That is true of both versions
(§1). The sentence is therefore not a false statement about the skeleton, but as written it implies the 2014
arithmetic and cites a source that cannot date anything after 2014. Severity MED (§Findings).

### Replacement wording — Option A (recommended; precise)

Fenced, drop-in for lines 62-63 (keeps the "v7.2 only" boundary, keeps the S496 attribution, adds no sixth source —
P-C2 freezes the five sources, so the dating is pointed at this report instead of at new SOURCES rows):

```
- v7.2 only. The 2014 commit's patch is where the estimate comes from, and two of its lines survive here verbatim —
  the file page cache and the reclaimable term are still held back by `min(half, wmark_low)` — but three inputs have
  changed since (S496 shows only the 2014 code; the tag-by-tag reads are in
  `.ufo/waves/round-51/w1/Mo51ExecPatchVsV72.md`): the free term subtracts `totalreserve_pages` instead of the
  low-watermark sum from v4.5 on, reclaimable kernel memory adds `NR_KERNEL_MISC_RECLAIMABLE` from v4.20 on, and the
  slab counter is the byte-based `NR_SLAB_RECLAIMABLE_B` from v5.9 on, while `low_wmark_pages()` includes
  `watermark_boost` from v5.0 on. This entry claims only the v7.2 bytes.
```

### Replacement wording — Option B (minimal; if the L1 wants no version numbers in the entry)

```
- v7.2 only. The estimate dates from the 2014 commit (S496), but its terms have changed since — the free term now
  subtracts `totalreserve_pages` rather than the summed low watermarks, and reclaimable kernel memory counts more
  than reclaimable slab — so this entry claims only the v7.2 bytes; the tag-by-tag dating is in
  `.ufo/waves/round-51/w1/Mo51ExecPatchVsV72.md`.
```

Either replacement is prose in Boundaries only: it touches no claim row, so it changes no row hash and invalidates no
recorded judgment; it adds no `source:` line, so the five-source arm of P-C2 is untouched. Pick one and edit lines
62-63 in a single commit; do not keep both.

If the L1 prefers to keep the original sentence and instead add a `source:` row for the intermediate tags, note that a
sixth source URL would break the frozen "names its URL among the five frozen sources / sources=5" arms of P-C2 —
that route is not open this round.

## 5. Named limits of this seat's evidence

- Dating is by tag boundary, not by bisected commit, for changes 1 (v6.4→v6.5), 5's second input (v4.19→v4.20) and 5's
  unit (v5.8→v5.9 via `d42f3245c7e2`). The commit that first created `mm/show_mem.c` was not retrieved: `mm/show_mem.c`
  is 404 at v6.0–v6.4 and 200 at v6.5 (E5), but the GitHub path-filtered commit list for `mm/show_mem.c` in
  2023-06-26..2023-09-05 returns only `8dbbc49345a7` and `1279aa0656bb`, and neither patch contains
  `si_mem_available`, so the file-creating commit is one the path listing does not surface (merge-window commit);
  the API was also returning HTTP 429 on later attempts. The v6.5 boundary itself rests on raw reads, not on the
  missing sha.
- Change 4 (zone-based → node-based counters for the file LRU lists) is read as value-equivalent; I did not measure
  it, and I did not date the accessor change.
- `totalreserve_pages` semantics are read from v7.2 `mm/page_alloc.c` only; the v4.5 form of
  `calculate_totalreserve_pages` (whether `high_wmark_pages(zone)` and the `managed_pages` cap were already there) was
  not fetched, so "the reserve became lowmem_reserve + high watermark" is dated v7.2, and only "the subtraction
  changed in v4.5" is dated to v4.5.
- The extractor's statement splitting is regex-based on `;`; the trailing `};` artefact and the loss of comment text
  are the only known distortions. `for_each_zone(zone) wmark_low += …;` is one source line with a body, so its
  statement boundary is correct.
- Only the five committed copies plus network reads of `raw.githubusercontent.com` at 20 tags were used; no kernel
  tree was cloned (a clone was not needed, and a kernel mirror was out of scope).
- I did not re-run `count-c1.py` or `count-c2.py`; the prose edit proposed here is invisible to both counters'
  judged arms (no claim cell, no copy hash changes).

## 6. Scratch and hygiene

`/fast/scratch/hyaku/mori-r51/Mo51ExecPatchVsV72/` held `cmp.py`, `mmzone.h.v7.2`, two commit patches
(`p.8dbbc49345a7.txt`, `p.1279aa0656bb.txt`), one short-lived `mmzone-or-file.<tag>` file per loop iteration in E4
(deleted inside the loop) and `tmp/`; it was removed with `rm -rf` after the receipts above were copied into this
report (§7). No file in the lane, the fleet root or `~/.local/bin` was created or
modified; no git/jj command that mutates was run (only `sha256sum`, `curl`, `grep`, `python3` reads); no pacman. Host
reads were limited to the disk-guard status; no kernel log text, cgroup, sysctl or systemd state was read or touched.

## 7. Removal receipt

```
$ rm -rf -- /fast/scratch/hyaku/mori-r51/Mo51ExecPatchVsV72; echo "rc_rm=$?"
rc_rm=0
$ ls -d /fast/scratch/hyaku/mori-r51/Mo51ExecPatchVsV72 2>&1; echo "rc_ls=$?"
ls: cannot access '/fast/scratch/hyaku/mori-r51/Mo51ExecPatchVsV72': No such file or directory
rc_ls=2
$ ls -la /tmp/mo51-* 2>&1 | head -3
ls: cannot access '/tmp/mo51-*': No such file or directory
```

Nothing of this seat remains on disk. The `/tmp` pokes in §3 (E5's `-o /tmp/mo51-sm.$$`) were deleted inside the same
loop; that path is a transport buffer, not evidence, and the evidence is the http code and byte count recorded
above.

## Findings

- **MED — `corpus/knowledge/memavailable-estimate-r51.md:62-63`.** Boundaries bullet "The formula has had the same
  shape since the 2014 commit's patch (S496)" cites the 2014 patch for a 2014→v7.2 span it cannot show, and the 2014
  arithmetic does not survive to v7.2: the free term's subtraction changed in v4.5 (`84ad5802a33a`, `wmark_low` →
  `totalreserve_pages`), a second reclaimable input (`NR_KERNEL_MISC_RECLAIMABLE`) arrived in v4.20, the slab counter
  became the byte-based `NR_SLAB_RECLAIMABLE_B` in v5.9, and `low_wmark_pages()` has included `watermark_boost` since
  v5.0. Only the skeleton and the two `min(half, wmark_low)` holdbacks are verbatim. Replacement wording supplied in
  §4 (Option A recommended, Option B minimal); the edit is Boundaries prose only and leaves every claim row, row
  hash and the five-source arm untouched.
- **LOW — `corpus/knowledge/memavailable-estimate-r51.md:15`** (note, no change requested): the intro's "computed …
  from free pages, the file LRU lists, reclaimable kernel memory and the zones' low watermarks" is accurate at v7.2
  only in the sense that the low watermarks cap the holdbacks; they do not reduce the free-page term. If the L1
  replaces the Boundaries bullet as in §4, consider adding "the low watermarks cap the two holdbacks" to this
  sentence so the two statements agree. Not a defect on its own.
- **Verified, no defect:** `show_mem.c.v7.2:32-72` is the exact function range (opens line 32, `EXPORT_SYMBOL_GPL` at
  73), and the two copies cited here match the entry's `recheck:` hashes (`9f571a04fc36…`, `dba76b263bbd…`).
