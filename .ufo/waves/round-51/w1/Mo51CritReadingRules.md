# Mo51CritReadingRules — prose attack on `corpus/knowledge/memavailable-estimate-r51.md`

Seat: Mo51CritReadingRules (leaf critic, mori round 51, w1). Date: 2026-10-26.
Scope: the prose sections of `mori-shokunin/corpus/knowledge/memavailable-estimate-r51.md` — intro (lines 1-16), `## Reading rules` (44-55), `## Boundaries` (57-65). The claim table rows (18-42) are entailment-vote territory; I use them only as citation targets.

Evidence read (all absolute paths):
- `mori-shokunin/corpus/evidence/sources-r51/34e431b0.patch` (S496 copy, sha256 9f571a04…)
- `mori-shokunin/corpus/evidence/sources-r51/show_mem.c.v7.2` (S493 copy, sha256 dba76b26…)
- `mori-shokunin/corpus/evidence/sources-r51/meminfo.c.v7.2` (S494 copy, sha256 d6c58074…)
- `mori-shokunin/corpus/evidence/sources-r51/mm_inline.h.v7.2` (S495 copy, sha256 2d4accbb…)
- `mori-shokunin/corpus/evidence/sources-r51/proc.rst.v7.2` (S492 copy, sha256 e760f716…)
- `mori-shokunin/corpus/SOURCES.md` rows S492-S496 (lines 271-275)
- `/proc/meminfo` (host read, permitted by host guard; no triggering, no config change)

Method: for every factual sentence in the three prose sections, locate the supporting or contradicting line in the five frozen copies; a sentence with no supporting line is flagged. No tools were installed or modified; no git/jj mutation; scratch `/fast/scratch/hyaku/mori-r51/Mo51CritReadingRules/` removed before finishing.

## Verdicts

### 1. "never rebuild it as `MemFree + Cached` — that sum counts tmpfs and shmem pages that sit on anon LRU lists and that the estimate does not add (rows 4, 7, 17, 20)" (line 46-47)

SUPPORTED in substance. The prohibition is exactly the 2014 commit's motivation: `34e431b0.patch:6-14` ("adding up free and cached ... was fine ten years ago, but is pretty much guaranteed to be wrong today", "Cached includes memory that is not freeable as page cache, for example shared memory segments, tmpfs, and ramfs"). Cached including tmpfs/shmem is also documented: `proc.rst.v7.2:1138-1141` (row 4). The estimate's page-cache term is only active+inactive file LRU: `show_mem.c.v7.2:54-55` (row 7). The belief that tmpfs folios sit on the anon LRU rests on row 16 (`mm_inline.h.v7.2:25-26`: "0 if @folio is a normal anonymous folio, a tmpfs folio or otherwise ram or swap backed folio"), which is NOT in the cited row set (rows 4, 7, 17, 20) — row 17 only says what *is* on the file LRU. Citation nit, LOW.

### 2. "The figure excludes swap by construction ("without swapping"): a host with free swap can keep running past `MemAvailable = 0`, and a reading of 0 is a clamp, not an exact zero (rows 1, 12)" (line 48-49)

Split verdict:

- "without swapping" — SUPPORTED: `proc.rst.v7.2:1127-1128` (row 1).
- "excludes swap by construction" — SUPPORTED as a code-reading inference: the formula in `show_mem.c.v7.2:40-71` reads only NR_FREE_PAGES, totalreserve_pages, NR_ACTIVE_FILE/NR_INACTIVE_FILE, NR_SLAB_RECLAIMABLE_B, NR_KERNEL_MISC_RECLAIMABLE and per-zone low watermarks; no SwapTotal/SwapFree/swap-cache counter enters. (It is an inference — no single quote states "no swap term" — but it is directly checkable in the copy.)
- "a host with free swap can keep running past MemAvailable = 0" — NOT supported by any line in the five copies. None of the sources discusses behavior beyond `MemAvailable = 0`; it is a host-behavior claim, true but unsourced. LOW (see replacement below).
- "a reading of 0 is a clamp, not an exact zero" — SUPPORTED: `show_mem.c.v7.2:69-70` (`if (available < 0) available = 0;`, row 12); the clamp is also in the 2014 patch, `34e431b0.patch:113-114`.

### 3. "Units are kB on every meminfo line (row 14)" (line 50)

CONTRADICTED. The helper `show_val_kb` (`meminfo.c.v7.2:28-32`) shifts and appends " kB" — but it is not every line, and not every line's unit is kB:

- The four `HugePages_Total/_Free/_Rsvd/_Surp` lines are printed by `hugetlb_report_meminfo(m)` (`meminfo.c.v7.2:173`), an external function (hugetlbfs) not present in the five copies; they are counts of huge pages with no unit suffix. Host observation confirms: `/proc/meminfo:52-55` print `HugePages_Total:       0` … with no "kB", while `Hugepagesize:       2048 kB` (`:56`) does carry kB.
- Several other lines print via `seq_printf` rather than the helper, though they still emit kB: `Zswapped` (`meminfo.c.v7.2:93-95`), `KernelStack` (`:111-112`, counter already in kB), `ShadowCallStack` (`:114-115`), `VmallocTotal` (`:127-128`), `HardwareCorrupted` (`:137-138`).

So "Units are kB on every meminfo line" is false as written, and the row-14 claim text ("Every meminfo value goes through one helper …") is likewise overbroad: the "one helper" claim fails for the lines above, and the "kB" claim fails for the four HugePages counts. This is a factual error in a reading rule. HIGH.

### 4. "When `Cached` is large but `MemAvailable` is small, compare `Shmem`: tmpfs and shared memory raise `Cached` without raising the estimate [INFERENCE from rows 4, 5, 7, 17 — not measured on this host]" (line 51-52)

SOUND as a labeled inference, with a citation gap. Cached = NR_FILE_PAGES − swapcache − bufferram (`meminfo.c.v7.2:48-51`, row 14/15) and includes tmpfs & shmem (`proc.rst.v7.2:1138-1141`, row 4); the `Shmem` line reports shmem+tmpfs (`proc.rst.v7.2:1192-1193`, row 5); the estimate's page-cache term is file LRU only (`show_mem.c.v7.2:54-55`, row 7). The missing link — tmpfs folios are placed on the anon LRU, hence absent from the file-LRU term — is exactly row 16 (`mm_inline.h.v7.2:25-26`), not row 17. The cited row list (4, 5, 7, 17) does not alone establish "sit on anon LRU lists". Also correct that no other term of the v7.2 formula touches shmem counters (slab term is kernel memory, `show_mem.c.v7.2:64-65`). The "not measured on this host" disclaimer is honest. Citation fix only, LOW.

### 5. "v7.2 only. The formula has had the same shape since the 2014 commit's patch (S496), but this entry claims only the v7.2 bytes." (line 62-63)

SUPPORTED as a *shape* statement, with material deltas that the sentence should name:

- Same skeleton in both: free − reserve; + pagecache − min(pagecache/2, wmark_low); + reclaimable − min(reclaimable/2, wmark_low); clamp at 0. Compare `34e431b0.patch:95,102-104,110-111,113-114` with `show_mem.c.v7.2:47,54-57,64-67,69-70`.
- Delta (a) — the reserve subtracted from free changed: 2014: `available = i.freeram - wmark_low;` (`34e431b0.patch:95`); v7.2: `available = global_zone_page_state(NR_FREE_PAGES) - totalreserve_pages;` (`show_mem.c.v7.2:47`; `totalreserve_pages` declared at `:23`). The composition of `totalreserve_pages` is NOT defined in the five copies (UNVERIFIED whether it equals the low-watermark sum; its name and use indicate a different quantity — it is an internal reserve computed elsewhere in mm/). This is a real change in what "free minus reserve" means.
- Delta (b) — the reclaimable term grew: 2014: NR_SLAB_RECLAIMABLE alone (`34e431b0.patch:110-111`); v7.2: NR_SLAB_RECLAIMABLE_B + NR_KERNEL_MISC_RECLAIMABLE (`show_mem.c.v7.2:64-65`). `NR_KERNEL_MISC_RECLAIMABLE` is the KReclaimable-class counter that also feeds the `KReclaimable` meminfo line (`meminfo.c.v7.2:106-107`; doc `proc.rst.v7.2:1194-1197`). So "reclaimable kernel memory" now includes the KReclaimable class, which the 2014 formula did not.
- Delta (c) — cosmetic: helper renames (global_page_state → global_zone_page_state/global_node_page_state_pages), `zone->watermark[WMARK_LOW]` → `low_wmark_pages(zone)` (same quantity by name; macro not in copies, UNVERIFIED), and the function moved from `fs/proc/meminfo.c` (patch hunk) into `mm/show_mem.c` (v7.2).

The sentence as written is defensible — it claims only shape and only v7.2 bytes — but "same shape" invites readers to infer the inputs are the same, which (a) and (b) show they are not (same `wmark_low` heldback capping, but different base reserve and a wider reclaimable term).

### 6. "`totalreserve_pages` is not exported to userspace as one line, so the estimate cannot be recomputed exactly from `/proc/meminfo` alone" (line 64-65)

SUPPORTED within the available evidence.

- No line of `meminfo.c.v7.2` prints `totalreserve_pages`; the only occurrence in the code copies is as an internal variable read by `si_mem_available()` (`show_mem.c.v7.2:23,47`). The meminfo print list (`meminfo.c.v7.2:60-173`) contains no such line.
- Host observation: `/proc/meminfo` (read above) has no `totalreserve` line — the only "reserve"-adjacent output is the per-zone watermark triple min/low/high and `lowmem_reserve[]` printed by `show_free_areas()` (`show_mem.c.v7.2:301-355`), which is zoneinfo-style output, not a single global line.
- The consequence is valid, and actually holds for an independent reason: the holdback `min(x/2, wmark_low)` needs per-zone low watermarks, which `/proc/meminfo` does not expose at all (they exist only in `/proc/zoneinfo`), so exact recomputation from meminfo alone is impossible regardless of `totalreserve_pages`.
- Caveat: exhaustive proof that no userspace interface anywhere exports it ("as one line") cannot come from five files; the statement is supported as "no such line in the frozen copies, in the meminfo printer, or in host `/proc/meminfo`". No correction needed; note the caveat.

## Fenced replacement wording

Applied to `memavailable-estimate-r51.md:50` (units bullet):

```markdown
- Units are kB on every memory-size line of /proc/meminfo (row 14); the four
  HugePages_Total/_Free/_Rsvd/_Surp lines are counts of huge pages and carry no
  unit suffix (they are printed by hugetlb_report_meminfo, not by the meminfo.c
  helper). A ratio MemAvailable/MemTotal is unit-free.
```

Applied to `memavailable-estimate-r51.md:48-49` (swap bullet); adds the [INFERENCE] tag to the unsourced clause:

```markdown
- The figure excludes swap by construction ("without swapping"): the formula's
  inputs (show_mem.c.v7.2:40-71) contain no swap counter. A host with free swap
  can keep running past MemAvailable = 0 [INFERENCE — not stated in any of the
  five sources], and a reading of 0 is a clamp, not an exact zero (rows 1, 12).
```

Applied to `memavailable-estimate-r51.md:46-47` (bullet 1): add row 16 to the citation set:

```markdown
- Read MemAvailable itself for runway; never rebuild it as MemFree + Cached —
  that sum counts tmpfs and shmem pages that sit on anon LRU lists (rows 4, 16)
  and that the estimate does not add (rows 7, 17, 20).
```

Applied to `memavailable-estimate-r51.md:51-52` (Shmem bullet): row 16 replaces/joins row 17:

```markdown
- When Cached is large but MemAvailable is small, compare Shmem: tmpfs and
  shared memory raise Cached without raising the estimate (rows 4, 5, 7, 16)
  [INFERENCE — not measured on this host].
```

Applied to `memavailable-estimate-r51.md:62-63` (Boundaries, formula shape): name the deltas:

```markdown
- v7.2 only. The formula has kept the same three-term shape since the 2014
  commit's patch (S496) — free minus a reserve, plus file-LRU cache and
  reclaimable kernel memory, each capped by min(half, low-watermark sum),
  clamped at zero — but two inputs changed: the base reserve is now
  totalreserve_pages (show_mem.c.v7.2:47) instead of the low-watermark sum
  (34e431b0.patch:95), and the reclaimable term now includes
  NR_KERNEL_MISC_RECLAIMABLE (KReclaimable class, show_mem.c.v7.2:64-65)
  alongside slab. This entry claims only the v7.2 bytes.
```

## Findings

- HIGH — `memavailable-estimate-r51.md:50` — "Units are kB on every meminfo line" is false: the four `HugePages_Total/_Free/_Rsvd/_Surp` lines are unitless counts (printed by `hugetlb_report_meminfo`, `meminfo.c.v7.2:173`, outside the copies; confirmed on host `/proc/meminfo:52-55`), and several other lines print via `seq_printf` rather than the row-14 helper (`meminfo.c.v7.2:93-95,111-112,127-128,137-138`).
- MED — `memavailable-estimate-r51.md:62-63` — "same shape since the 2014 commit" is accurate only as a skeleton; the base reserve term changed from `wmark_low` to `totalreserve_pages` (`34e431b0.patch:95` vs `show_mem.c.v7.2:47`) and the reclaimable term gained `NR_KERNEL_MISC_RECLAIMABLE` (KReclaimable class; `show_mem.c.v7.2:64-65`). Replace with wording naming the deltas.
- LOW — `memavailable-estimate-r51.md:49` — "a host with free swap can keep running past MemAvailable = 0" has no supporting line in any of the five copies; tag [INFERENCE] or drop.
- LOW — `memavailable-estimate-r51.md:47` — citation set (rows 4, 7, 17, 20) lacks row 16, which is the row that actually places tmpfs on the anon LRU (`mm_inline.h.v7.2:25-26`).
- LOW — `memavailable-estimate-r51.md:52` — same gap: the Shmem [INFERENCE] cites rows 4, 5, 7, 17; row 16 is required for the "anon LRU" step of the inference.
- OK — `memavailable-estimate-r51.md:49` (clamp), `:48` ("without swapping", formula has no swap term), `:64-65` (`totalreserve_pages` not printed in the copies nor in host meminfo; recompute-from-meminfo-alone impossible, independently because per-zone watermarks are absent from meminfo) — supported; no change needed beyond the caveat in verdict 6.
