# Mo51CritEntail01 — ENTAILMENT vote (adversarial second vote)

Seat: Mo51CritEntail01 (mori round 51, wave w1; ENTAILMENT item).
Data commit reviewed: `87e0c374537557754bf71dd68036ded3ddc6699c` (entry `corpus/knowledge/memavailable-estimate-r51.md`).
Rows judged: 1–6 of the `## Claims` table. Sources read from the committed copies under
`corpus/evidence/sources-r51/` (`proc.rst.v7.2`, `show_mem.c.v7.2`); quotes located by line, ~20 lines of
context read around each.

Hash check: all six row hashes from `evidence/c2-hashes-at-data.txt` recomputed with the mandated one-liner
(sha256 of whitespace-collapsed claim text, first 12 hex) and match exactly:
row=1 `2d0daa4192f1`, row=2 `eba2b78b47f3`, row=3 `ad57d1b66582`, row=4 `72cdbee44353`,
row=5 `a9cf30c5ed71`, row=6 `5d06a2ae70cf`.

## Verdicts

- Row 1 `2d0daa4192f1` — **entailed**. Quote `proc.rst.v7.2:1127-1128` ("An estimate of how much memory is
  available for starting new applications, without swapping."); context `:1124-1134`. The first half is the
  doc's own definition. The negative clause "not as a count of free pages" is entailed by the definitional
  context: `MemFree` is defined separately as "Total free RAM" (`:1124-1125`) and `MemAvailable` is defined as
  an estimate "Calculated from MemFree, SReclaimable, the size of the file LRU lists, and the low watermarks"
  (`:1128-1130`) — a multi-input estimate, not the free-page count.
- Row 2 `eba2b78b47f3` — **entailed**. Quote `proc.rst.v7.2:1128-1130` ("Calculated from MemFree,
  SReclaimable, the size of the file LRU lists, and the low watermarks in each zone."). The claim is a direct
  paraphrase of the four named inputs: free memory=MemFree, reclaimable slab=SReclaimable, file LRU list
  sizes=size of the file LRU lists, each zone's low watermark=low watermarks in each zone.
- Row 3 `ad57d1b66582` — **entailed**. Quote `proc.rst.v7.2:1134` ("The impact of those factors will vary from
  system to system."); context `:1131-1134` ("The estimate takes into account that the system needs some page
  cache to function well, and that not all reclaimable slab will be reclaimable, due to items being in use.").
  "Those factors" are the cache and slab reclaimability factors just listed, so the doc does warn their impact
  varies by system. The trailing gloss "so the figure is a model rather than a measurement" restates the doc's
  own word "estimate" (`:1127, :1131`) plus the stated variability; it adds no number or scope the doc rejects.
- Row 4 `72cdbee44353` — **entailed**. Quote `proc.rst.v7.2:1139-1140` ("In-memory cache for files read from
  the disk (the pagecache) as well as tmpfs & shmem.") under the `Cached` heading (`:1138`). The claim restates
  the quote exactly; context `:1141` ("Doesn't include SwapCached.") is consistent.
- Row 5 `a9cf30c5ed71` — **entailed**. Quote `proc.rst.v7.2:1193` ("Total memory used by shared memory (shmem)
  and tmpfs") under the `Shmem` heading (`:1192`). The claim restates the quote: shared memory segments and
  tmpfs files reported as one figure.
- Row 6 `5d06a2ae70cf` — **overclaim**. Quote `show_mem.c.v7.2:45-47` ("without causing swapping or OOM. */
  available = global_zone_page_state(NR_FREE_PAGES) - totalreserve_pages;"); context `:32-72`. The first clause
  ("The estimate starts from the free page count minus totalreserve_pages") is entailed by line 47. The
  parenthetical definition "the pages the kernel holds back from userspace allocations" is NOT in the source:
  `show_mem.c` only declares `totalreserve_pages` at `:23` and never defines it; the comment at `:44`
  ("Estimate the amount of memory available for userspace allocations") describes the whole estimate, not what
  `totalreserve_pages` is. That clause adds a definition/scope the source does not state. Exact words going
  beyond the source: `the pages the kernel holds back from userspace allocations`.

ENTAIL 2d0daa4192f1 entailed
ENTAIL eba2b78b47f3 entailed
ENTAIL ad57d1b66582 entailed
ENTAIL 72cdbee44353 entailed
ENTAIL a9cf30c5ed71 entailed
ENTAIL 5d06a2ae70cf overclaim — the pages the kernel holds back from userspace allocations
ENTAIL 0a908e8eb4f3 entailed

Replacement claim (row 6, voted entailed, hash `0a908e8eb4f3` recomputed with the same one-liner):

> The estimate begins with the free page count minus totalreserve_pages, then adds file cache and reclaimable slab.

Constraint check: 15 words (>= 6); words of 3+ letters absent from the quote: The, estimate, begins, with,
free, page, count, minus, then, adds, file, cache, and, reclaimable, slab (>= 3). Entailment: line 47
(`available = global_zone_page_state(NR_FREE_PAGES) - totalreserve_pages;`) for the first clause; lines 54-57
(`available += pagecache` after the holdback) and 64-67 (`available += reclaimable`, "reclaimable slab and other
kernel memory", comment at `:60`) for "then adds file cache and reclaimable slab".

## Findings

- HIGH — `corpus/knowledge/memavailable-estimate-r51.md` claim row 6 (source S493): the parenthetical "the
  pages the kernel holds back from userspace allocations" defines `totalreserve_pages` with words the source
  does not state (`show_mem.c.v7.2` only declares the variable at line 23; no definition in the file). Overclaim
  voted; replacement text above (hash `0a908e8eb4f3`) is proposed for the L1 to substitute.
- LOW — row 3's phrase "a model rather than a measurement" is a gloss (the source says "estimate" and that
  factors vary), not a stated contrast; accepted as entailed but noted as the closest borderline call in the
  judged set.
- LOW — rows 1-5 quotes all located in the committed copies at the line numbers given; no quote/drift issue
  found in the judged rows.
