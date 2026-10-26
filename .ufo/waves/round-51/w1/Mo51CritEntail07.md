# Mo51CritEntail07 — entailment votes, C2 rows 7–11

Seat: Mo51CritEntail07 (ENTAILMENT item, adversarial second vote). Lane: mori-shokunin.
Scoped entry: `corpus/knowledge/memavailable-estimate-r51.md` at `87e0c374537557754bf71dd68036ded3ddc6699c`.
Verified the committed copy is the data commit: `git diff 87e0c374537557754bf71dd68036ded3ddc6699c -- corpus/knowledge/memavailable-estimate-r51.md corpus/evidence/sources-r51/` is empty (0 lines), so the working tree equals the freeze bytes for the entry and the source copies.
Judged rows: 7–11 (all S493 quotes; committed copy `corpus/evidence/sources-r51/show_mem.c.v7.2`).
Method per row: located the quote in the committed copy (whitespace-collapsed match), read ~20 lines of context around it (`si_mem_available()`, show_mem.c.v7.2 lines 32–72), and judged whether the claim cell follows from the quote plus that context. Hashes recomputed with the given one-liner; all five match `c2-hashes-at-data.txt`.

## Verdicts (exactly one per judged row)

```
ENTAIL 6c8b6efc9731 entailed
ENTAIL 6b8f33ed528e entailed
ENTAIL 1b9c863ec2c2 entailed
ENTAIL cbcd91de05ac entailed
ENTAIL 58ba82f481b8 entailed
```

No `overclaim` votes; no replacement lines needed.

## Per-row judgment

### Row 7 (hash 6c8b6efc9731) — entailed
Claim: "Only the active and inactive file LRU lists enter the estimate as page cache; nothing else that Cached counts is added."
Quote located: show_mem.c.v7.2 lines 52–56 (`cache, needs to stay. */ pagecache = global_node_page_state(NR_ACTIVE_FILE) + global_node_page_state(NR_INACTIVE_FILE);`; the code line is 54–55).
Context (lines 43–57): `pagecache` is defined by exactly that single assignment — the two file LRU counters. No other term is ever added to `pagecache` in the whole function (the only later operations are the line 56 subtraction and line 57 `available += pagecache`). The first clause is verbatim-supported; the negative clause is a direct consequence of the complete definition (whatever else the Cached line counts is not among the two terms). Entailed.

### Row 8 (hash 6b8f33ed528e) — entailed
Claim: "From that file cache the code withholds the smaller of half the cache and the summed low watermarks, then adds the remainder."
Quote located: show_mem.c.v7.2 lines 56–57 (`pagecache -= min(pagecache / 2, wmark_low); available += pagecache;`).
Context (lines 40–57): lines 40–41 build `wmark_low` by summing `low_wmark_pages(zone)` over every zone — the "summed low watermarks". Line 56 withholds `min(pagecache / 2, wmark_low)`, i.e. the smaller of half the cache and the watermark sum; line 57 adds the remainder to `available`. Fully entailed.

### Row 9 (hash 1b9c863ec2c2) — entailed
Claim: "The kernel's stated reason for holding cache back is that freeing all of it would drive the system into swapping or thrashing."
Quote located: show_mem.c.v7.2 lines 50–51 (`Not all the page cache can be freed, otherwise the system will * start swapping or thrashing.`).
Context (lines 49–53): the comment continues "Assume at least half of the page cache, or the low watermark worth of cache, needs to stay." — the holdback that follows at lines 54–57. The stated reason is verbatim in the source and directly motivates the holdback. Entailed.

### Row 10 (hash cbcd91de05ac) — entailed
Claim: "Reclaimable slab and other reclaimable kernel memory are added under the same rule: withhold the smaller of half and the low watermark sum."
Quote located: show_mem.c.v7.2 lines 66–67 (`reclaimable -= min(reclaimable / 2, wmark_low); available += reclaimable;`).
Context (lines 64–67): line 64–65 define `reclaimable` as `global_node_page_state_pages(NR_SLAB_RECLAIMABLE_B) + global_node_page_state(NR_KERNEL_MISC_RECLAIMABLE)` — exactly the claim's "reclaimable slab and other reclaimable kernel memory". The rule is the same `min(x / 2, wmark_low)` shape as pagecache (line 56), then added to `available`. Entailed.

### Row 11 (hash 58ba82f481b8) — entailed
Claim: "The holdback on that kernel term exists because some reclaimable slab objects are still in use and cannot be freed."
Quote located: show_mem.c.v7.2 lines 60–61 (`Part of the reclaimable slab and other kernel memory consists of * items that are in use, and cannot be freed.`).
Context (lines 60–63): the comment continues "Cap this estimate at the low watermark." — the stated cause (items in use, cannot be freed) directly precedes and motivates the cap/holdback at line 66. Entailed.

## Scratch hygiene

- Scratch root `/fast/scratch/hyaku/mori-r51/Mo51CritEntail07/` created; `TMPDIR=/fast/scratch/hyaku/mori-r51/Mo51CritEntail07/tmp` exported; scratch removed on completion (`rm -rf`).
- No tools installed or upgraded (Python 3 stdlib only; no pacman, no uv, no binaries). Nothing written to `~/.local/bin` or any PATH directory.
- No repo mutation: read-only git only (`diff`, `rev-parse`, `cat-file`, `log`, `ls-files`); no add/commit/stash/checkout/reset/pull/push, no jj mutation.
- No host reads performed (not needed for this item).

## Findings

- LOW — Row 7's negative clause "nothing else that Cached counts is added" presupposes the meminfo Cached line counts more than the file LRU lists; that composition is established by S492/S494 (entry rows 4 and 15), not by S493 alone. The S493 code still fully supports the claim because `pagecache` is defined by the single two-term assignment, so I voted entailed; this is a cross-source dependency of the wording, not an overclaim. Concern: entry row 7, `corpus/knowledge/memavailable-estimate-r51.md`.
- LOW — `corpus/evidence/sources-r51/` and the entry match `87e0c3` byte-for-byte, but `.ufo/waves/round-51/evidence/c2-hashes-at-data.txt` is not in `87e0c3`: it first appears in `b504cb17` (wave dispatch/at-data receipts commit). The rows 7–11 hashes in it still match recomputation from the claim cells at `87e0c3`, so this does not affect the votes; noted for receipt provenance only. Concern: `.ufo/waves/round-51/evidence/c2-hashes-at-data.txt`.
