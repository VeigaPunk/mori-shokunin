# Mo51CritEntail12 — ENTAILMENT seat (adversarial second vote)

Item: judge claim rows 12–16 of `## Claims` in `corpus/knowledge/memavailable-estimate-r51.md` at
87e0c374537557754bf71dd68036ded3ddc6699c. Verdict lines below are my own judgment only.

Method: for each row, located the quote in the committed copy under
`corpus/evidence/sources-r51/` (whitespace-collapsed match; line numbers from `git show 87e0c374:<path>`),
read ~20 lines around it, and judged whether the CLAIM cell follows from the quote plus that context.
Hashes checked against `evidence/c2-hashes-at-data.txt`; all five recomputed with
`python3 -c 'import hashlib,re,sys;print(hashlib.sha256(re.sub(r"\s+"," ",sys.argv[1]).strip().encode()).hexdigest()[:12])' "<claim text>"`
and matched.

Scratch: `/fast/scratch/hyaku/mori-r51/Mo51CritEntail12/` created; no temp files were needed (all reads were
committed-bytes reads); removed before finish.

## Row 12 — hash `ec0f6c97eeba` (S493, mm/show_mem.c.v7.2)

- Claim: "A negative result is clamped, so the line reads zero instead of a negative figure when the reserves exceed everything counted."
- Quote found at `show_mem.c.v7.2:69-71`: `if (available < 0) available = 0; return available;` (line 69 `if (available < 0)`, line 70 `available = 0;`, line 71 `return available;`).
- Context (lines 32–73): `si_mem_available()` computes `available = global_zone_page_state(NR_FREE_PAGES) - totalreserve_pages;` then adds `pagecache` (after `pagecache -= min(pagecache / 2, wmark_low)`) and `reclaimable` (after `reclaimable -= min(reclaimable / 2, wmark_low)`), then clamps `if (available < 0) available = 0;` and `return available;`. The function is the MemAvailable estimate (S494 prints it at `meminfo.c.v7.2:56,62`).
- Judgment: entailed. The clamp is exactly in the function whose return value the MemAvailable line prints, so "the line reads zero instead of a negative figure" follows. `available < 0` occurs exactly when `NR_FREE_PAGES + cache/slab contributions < totalreserve_pages`, i.e. "the reserves exceed everything counted"; that is a faithful paraphrase, not an added consequence.
- Verdict: `ENTAIL ec0f6c97eeba entailed`

## Row 13 — hash `40b46a312e03` (S493, mm/show_mem.c.v7.2)

- Claim: "The watermark used for both holdbacks is the low watermark summed over every memory zone of the machine."
- Quote found at `show_mem.c.v7.2:38,40-41`: `struct zone *zone; for_each_zone(zone) wmark_low += low_wmark_pages(zone);` (line 38 `struct zone *zone;`, line 40 `for_each_zone(zone)`, line 41 `wmark_low += low_wmark_pages(zone);`).
- Context (lines 34–67): `wmark_low` starts 0, is summed over `for_each_zone(zone)` (all zones), and is used in both holdbacks: `pagecache -= min(pagecache / 2, wmark_low);` (line 56) and `reclaimable -= min(reclaimable / 2, wmark_low);` (line 66).
- Judgment: entailed. The same `wmark_low` (low watermark summed over every zone) appears in both subtracts; "used for both holdbacks" is directly visible in the same function.
- Verdict: `ENTAIL 40b46a312e03 entailed`

## Row 14 — hash `a06f1037d952` (S494, fs/proc/meminfo.c.v7.2)

- Claim: "Every meminfo value goes through one helper that shifts a page count by PAGE_SHIFT minus 10 and prints the result in kB."
- Quote found at `meminfo.c.v7.2:30-31`: `seq_put_decimal_ull_width(m, s, num << (PAGE_SHIFT - 10), 8); seq_write(m, " kB\n", 4);` — the body of `show_val_kb`.
- Context (lines 27–173): `show_val_kb` is one helper, but it is NOT used for every meminfo value. Within `meminfo_proc_show` the following lines print via `seq_printf` directly instead of `show_val_kb`: `Zswapped:` (lines 93–95, CONFIG_ZSWAP), `KernelStack:` (lines 111–112, value already in KB), `VmallocTotal:` (lines 127–128, `VMALLOC_TOTAL >> 10`), `HardwareCorrupted:` (lines 137–138, `<< (PAGE_SHIFT - 10)`), plus the `hugetlb_report_meminfo(m)` (line 173) and `memtest_report_meminfo(m)` (line 134) blocks print further lines through their own code.
- Judgment: OVERCLAIM. "Every meminfo value goes through one helper" adds a universal scope the source contradicts: several `/proc/meminfo` values are printed by `seq_printf` (or by the hugetlb/memtest reporters), not through `show_val_kb`. The exact words going beyond the source: "Every meminfo value goes through one helper". The rest of the claim (shift by `PAGE_SHIFT - 10`, print in kB) is exactly what `show_val_kb` does, but the universal is unsupported and false.
- Verdict: `ENTAIL a06f1037d952 overclaim — Every meminfo value goes through one helper`
- Replacement claim (I judge entailed): "The show_val_kb helper shifts its page count by PAGE_SHIFT minus 10 and prints the value in kB." — hash `56b7a3309d66` (computed with the same one-liner; the quote itself is the body of `show_val_kb`, lines 30–31).
- Replacement verdict: `ENTAIL 56b7a3309d66 entailed`

## Row 15 — hash `102feb3debfa` (S494, fs/proc/meminfo.c.v7.2)

- Claim: "The Cached figure is computed from all file pages minus swap cache and buffers, a different base from the two file LRU lists."
- Quote found at `meminfo.c.v7.2:48-49`: `cached = global_node_page_state(NR_FILE_PAGES) - total_swapcache_pages() - i.bufferram;` (line 48 `cached = global_node_page_state(NR_FILE_PAGES) -`, line 49 `total_swapcache_pages() - i.bufferram;`).
- Context (lines 44–73): `cached` is computed from `NR_FILE_PAGES` minus `total_swapcache_pages()` minus `i.bufferram` and printed as `Cached:` (line 64). The same function separately prints `Active(file):`/`Inactive(file):` from `pages[LRU_ACTIVE_FILE]`/`pages[LRU_INACTIVE_FILE]` (lines 72–73; the `pages[]` array filled at lines 53–54 from `NR_LRU_BASE` counters). The two bases are visibly different expressions within the same function.
- Judgment: entailed. The formula clause is verbatim in the quote; "a different base from the two file LRU lists" is a comparison between two distinct computations that are both present in the immediate context (Cached from `NR_FILE_PAGES - swapcache - buffers` vs the file-LRU counters printed on their own lines). No extra number, consequence or scope is added that the context does not support (the claim asserts the bases differ, not why).
- Verdict: `ENTAIL 102feb3debfa entailed`

## Row 16 — hash `357c747c23d2` (S494, fs/proc/meminfo.c.v7.2)

- Claim: "MemFree prints the sysinfo free count while MemAvailable prints the separately computed estimate, as two adjacent lines."
- Quote found at `meminfo.c.v7.2:61-62`: `show_val_kb(m, "MemFree: ", i.freeram); show_val_kb(m, "MemAvailable: ", available);` (line 61 MemFree, line 62 MemAvailable).
- Context (lines 44–62): `i` is filled by `si_meminfo(&i)` (line 44), so `i.freeram` is the sysinfo free count; `available = si_mem_available();` (line 56) is the separately computed estimate (S493's `si_mem_available()`); the two `show_val_kb` calls are consecutive, so the lines are adjacent.
- Judgment: entailed. "sysinfo free count" = `i.freeram` from `struct sysinfo` (`si_meminfo`); "separately computed estimate" = `available` from `si_mem_available()`; "two adjacent lines" = consecutive `show_val_kb` calls. All three clauses are directly present in quote + context.
- Verdict: `ENTAIL 357c747c23d2 entailed`

## Assigned verdict lines (one per assigned row; plus replacement)

```
ENTAIL ec0f6c97eeba entailed
ENTAIL 40b46a312e03 entailed
ENTAIL a06f1037d952 overclaim — Every meminfo value goes through one helper
ENTAIL 56b7a3309d66 entailed
ENTAIL 102feb3debfa entailed
ENTAIL 357c747c23d2 entailed
```

## Findings

- HIGH — `corpus/knowledge/memavailable-estimate-r51.md` row 14 (hash `a06f1037d952`): claim "Every meminfo value goes through one helper …" is an overclaim; `fs/proc/meminfo.c.v7.2` prints several values via direct `seq_printf` calls (`Zswapped:` 93–95, `KernelStack:` 111–112, `VmallocTotal:` 127–128, `HardwareCorrupted:` 137–138) and via the hugetlb/memtest reporters, not through `show_val_kb`. Replacement claim proposed (hash `56b7a3309d66`, voted entailed).
- MED — none (rows 12, 13, 15, 16 judged entailed; no other defect found in the assigned rows' quotes/contexts).
- LOW — the C2 entry's claims are located and their hashes reproduce exactly (`evidence/c2-hashes-at-data.txt` matches all five recomputed hashes for rows 12–16); no mismatch found.
