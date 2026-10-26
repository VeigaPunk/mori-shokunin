# Mo51RevEntail07 — entailment votes, C2 claim rows 7–9

- Seat: Mo51RevEntail07 (ENTAILMENT item, wave w1, mori round 51)
- Date: 2026-10-26 — MACHINE_ID: 432d02b544a5459ebbff9c42ec68334d
- Judged at data commit: `87e0c374537557754bf71dd68036ded3ddc6699c` (lane working tree had advanced to `b504cb1701568a0038aab9d98ec13d28eff801da`, so every byte below was taken with read-only `git show 87e0c374…:<path>` from `/home/vgpnk/Projects/shokunin/mori-shokunin`; no clone was made, nothing in the lane repo was written).
- Scratch used and removed: `/fast/scratch/hyaku/mori-r51/Mo51RevEntail07/` (TMPDIR under it; nothing cited lives only there — all quoted bytes are reproduced below). Tools installed: none.

## Provenance checks (all observed)

1. Copies: the five files under `corpus/evidence/sources-r51/` at `87e0c374…` were sha256-hashed from `git show` output; all five match `evidence/freeze-sha256.txt` (e.g. `show_mem.c.v7.2` = `dba76b263bbdf93323a277a29c9281a892ff3fb35ddd6f0ddaf9ba1acb5b02f5`).
2. Hashes: for rows 7–9 the claim cell was extracted from the `## Claims` table of `corpus/knowledge/memavailable-estimate-r51.md` at `87e0c374…` and hashed with the L1 one-liner (`sha256`, whitespace collapsed, first 12 hex). Recomputed `6c8b6efc9731` / `6b8f33ed528e` / `1b9c863ec2c2` — each MATCHES the L1 file `.ufo/waves/round-51/evidence/c2-hashes-at-data.txt` rows 7/8/9, and the claim text matches the file's rendering character for character.
3. Location: each quote below was searched in the committed copy of `corpus/evidence/sources-r51/show_mem.c.v7.2` with whole-text whitespace collapsing; each occurs exactly once (line ranges given per row).

All three rows cite S493 (`mm/show_mem.c` at tag v7.2). Context read: the whole of `si_mem_available()` plus surrounding helpers, copy lines 24–88 (~30 lines around each quote).

## Row 7

- Claim (hash `6c8b6efc9731`): "Only the active and inactive file LRU lists enter the estimate as page cache; nothing else that Cached counts is added."
- Quote located: `corpus/evidence/sources-r51/show_mem.c.v7.2:52-55` — `cache, needs to stay. */ pagecache = global_node_page_state(NR_ACTIVE_FILE) + global_node_page_state(NR_INACTIVE_FILE);` (comment tail ends line 52, `*/` line 53, the two-counter assignment spans lines 54–55).
- Context (lines 32–72): `si_mem_available()` builds `available` from exactly three terms after the free-page start: the `pagecache` term (these two counters, lines 54–55), the holdback + add (lines 56–57), and the `reclaimable` term (slab-reclaimable + kernel-misc-reclaimable, lines 63–68). No third page-cache counter (e.g. `NR_SHMEM`) is ever added; `wmark_low` is the per-zone low-watermark sum (lines 40–41).
- Judgment: the quote plus that context shows the estimate's page-cache term is composed solely of `NR_ACTIVE_FILE` + `NR_INACTIVE_FILE`, and nothing else is added anywhere in the function. The comparative clause "nothing else that Cached counts is added" asserts only this addition behavior, which the function body states in full. Follows.

## Row 8

- Claim (hash `6b8f33ed528e`): "From that file cache the code withholds the smaller of half the cache and the summed low watermarks, then adds the remainder."
- Quote located: `corpus/evidence/sources-r51/show_mem.c.v7.2:56-57` — `pagecache -= min(pagecache / 2, wmark_low); available += pagecache;`
- Context: `pagecache` is the two file-LRU counters (lines 54–55); `wmark_low` is accumulated `for_each_zone(zone) wmark_low += low_wmark_pages(zone);` (lines 40–41), i.e. the low watermarks summed over zones.
- Judgment: `min(pagecache / 2, wmark_low)` is verbatim "the smaller of half the cache and the summed low watermarks"; `pagecache -=` withholds it; `available += pagecache` adds the remainder. Every element of the claim is in the quoted code plus two context lines. Follows.

## Row 9

- Claim (hash `1b9c863ec2c2`): "The kernel's stated reason for holding cache back is that freeing all of it would drive the system into swapping or thrashing."
- Quote located: `corpus/evidence/sources-r51/show_mem.c.v7.2:50-51` — `Not all the page cache can be freed, otherwise the system will * start swapping or thrashing.` (the `*` is the block-comment continuation marker on line 51).
- Context (lines 48–53): the full comment reads "Not all the page cache can be freed, otherwise the system will start swapping or thrashing. Assume at least half of the page cache, or the low watermark worth of cache, needs to stay." — this comment sits directly above the holdback code judged in row 8.
- Judgment: the comment is the stated reason, and it states exactly what the claim says: freeing all page cache would cause swapping or thrashing, hence the holdback. No extra scope, number, or consequence is added ("would drive into" is the claim's rendering of "otherwise … will start"). Follows.

## Vote lines

Exactly one verdict per assigned row (7, 8, 9); no other rows voted.

ENTAIL 6c8b6efc9731 entailed
ENTAIL 6b8f33ed528e entailed
ENTAIL 1b9c863ec2c2 entailed

## Findings

- No HIGH or MED findings. All three assigned rows (7, 8, 9) are judged entailed by the quoted span plus its immediate context; no replacement claims proposed.
- LOW — `corpus/knowledge/memavailable-estimate-r51.md`, Claims row 7 quote: the backticked span begins mid-comment (`cache, needs to stay. */`), so out of context it reads as a fragment; it is still located (whitespace collapsed) at exactly one place and the claim is faithful. Cosmetic only; the counter's 6–25-word rule is the L1's frozen predicate, not something to change.
- LOW — Claims row 9 quote embeds the literal comment star (`will * start`), an artifact of quoting a block comment across two source lines. Does not affect location (unique match) or the judgment.
- LOW (observation) — quote location was verified with whole-text whitespace collapse and uniqueness in the committed copy; a per-line search that does not collapse across line joins misses these multi-line quotes, so any seat re-checking locations should collapse the whole file first.
