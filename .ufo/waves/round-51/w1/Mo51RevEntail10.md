# Mo51RevEntail10 — entailment votes for claim rows 10–12 (mori round 51, wave w1)

Seat: Mo51RevEntail10 (reviewer, ENTAILMENT item). Judged at data commit
87e0c374537557754bf71dd68036ded3ddc6699c. Method per row: the claim and quote cells were parsed
programmatically from the committed entry `corpus/knowledge/memavailable-estimate-r51.md` (21 table rows
parsed, no manual transcription), the row hash was recomputed with the frozen one-liner (sha256 of the
whitespace-collapsed claim cell, first 12 hex) and checked against
`.ufo/waves/round-51/evidence/c2-hashes-at-data.txt`, the quote was located whitespace-collapsed in the
committed copy under `corpus/evidence/sources-r51/`, and about 20 lines of context around it were read
before judging. All three assigned rows cite S493 (`mm/show_mem.c` at v7.2). Scratch
`/fast/scratch/hyaku/mori-r51/Mo51RevEntail10/` with `TMPDIR` inside it; disk-guard status before start:
`/fast/scratch/hyaku` 25 % used, 604.2 G free — no ENOSPC. Files were extracted pinned to the data commit
with `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show <rev>:<path>` (rc 0). No tool installs, no
pacman, no repo or index mutation, no subagents.

Report: .ufo/waves/round-51/w1/Mo51RevEntail10.md

Copy integrity: sha256 of the copies read here match the frozen list
`.ufo/waves/round-51/evidence/freeze-sha256.txt` — show_mem.c.v7.2 = dba76b263bbdf93323a277a29c9281a892ff3fb35ddd6f0ddaf9ba1acb5b02f5,
meminfo.c.v7.2 = d6c5807421a69eac21efd737b39d099c711b3132b371dc34986d181746e3deda (read to check row 12's
printing chain), 34e431b0.patch = 9f571a04fc365858d8c82d31b309217a5e40f37877732da70416b0b1b42563d0 (read
for the history of the row-11 comment).

## Row 10 — hash cbcd91de05ac (source S493)

- Claim cell: "Reclaimable slab and other reclaimable kernel memory are added under the same rule: withhold
  the smaller of half and the low watermark sum."
- Recomputed hash cbcd91de05ac — matches the frozen row hash (row=10 in c2-hashes-at-data.txt).
- Quote located in `corpus/evidence/sources-r51/show_mem.c.v7.2` at lines 66–67 (the collapsed span covers
  both lines); exactly 1 occurrence in the copy.
- Context read: lines 32–73 (the whole `si_mem_available()` body) plus the function comment at lines 43–46.
- What the context shows: `reclaimable = global_node_page_state_pages(NR_SLAB_RECLAIMABLE_B) +
  global_node_page_state(NR_KERNEL_MISC_RECLAIMABLE);` (lines 64–65) — the two components the claim names
  ("reclaimable slab" and "other reclaimable kernel memory", matching the comment's own "the reclaimable
  slab and other kernel memory" at line 60); then `reclaimable -= min(reclaimable / 2, wmark_low); available
  += reclaimable;` (lines 66–67) — subtract `min(half, wmark_low)` and add the remainder to `available`,
  byte-for-byte the same pattern as the page-cache rule above at lines 56–57 (`pagecache -= min(pagecache /
  2, wmark_low); available += pagecache;`); and `wmark_low` is summed over the zones at lines 40–41
  (`for_each_zone(zone) wmark_low += low_wmark_pages(zone);`).
- Judgment: every operative part is stated by the quote plus context — the two counters summed into
  `reclaimable`; "added" is `available += reclaimable`; "under the same rule" is the identical
  min-half/low-watermark holdback as the cache term immediately above; "withhold the smaller of half and the
  low watermark sum" is exactly `min(reclaimable / 2, wmark_low)`. No added consequence, number or scope.
  No overclaim.

ENTAIL cbcd91de05ac entailed

## Row 11 — hash 58ba82f481b8 (source S493)

- Claim cell: "The holdback on that kernel term exists because some reclaimable slab objects are still in
  use and cannot be freed."
- Recomputed hash 58ba82f481b8 — matches the frozen row hash (row=11).
- Quote located in `corpus/evidence/sources-r51/show_mem.c.v7.2` at lines 60–61 (the collapsed span covers
  both lines); exactly 1 occurrence in the copy.
- Context read: lines 49–73 — the reclaimable term's full block (comment plus computation), the page-cache
  block above it, and the clamp/return below.
- What the context shows: the comment attached to the reclaimable term reads in full (lines 59–63): "Part
  of the reclaimable slab and other kernel memory consists of items that are in use, and cannot be freed.
  Cap this estimate at the low watermark." It sits directly above `reclaimable = …; reclaimable -=
  min(reclaimable / 2, wmark_low); available += reclaimable;` (lines 64–67). The comment is the kernel's
  stated rationale for the cap on the reclaimable term, in the same form as the page-cache rationale above
  it (lines 49–53).
- Judgment: "The holdback on that kernel term" is the `min(reclaimable / 2, wmark_low)` subtraction on the
  reclaimable term (line 66); "exists because some reclaimable slab objects are still in use and cannot be
  freed" restates the comment's reason clause — "Part of the reclaimable slab … consists of items that are
  in use, and cannot be freed" — for the slab component the comment names first, followed by the cap
  instruction "Cap this estimate at the low watermark". The S496 patch copy shows this comment's origin as a
  single-pool sentence ("Part of the reclaimable [slab] consists of items that are in use, and cannot be
  freed"), supporting the slab-specific reading of the v7.2 extension. No added consequence, number or scope
  beyond the source's own components. No overclaim. (Note: a strictly collective parse of "Part of the
  reclaimable slab and other kernel memory" would not isolate the slab subset; the natural distributive
  reading — supported by the sentence's history — does. Recorded as LOW in Findings.)

ENTAIL 58ba82f481b8 entailed

## Row 12 — hash ec0f6c97eeba (source S493)

- Claim cell: "A negative result is clamped, so the line reads zero instead of a negative figure when the
  reserves exceed everything counted."
- Recomputed hash ec0f6c97eeba — matches the frozen row hash (row=12).
- Quote located in `corpus/evidence/sources-r51/show_mem.c.v7.2` at lines 69–71 (the collapsed span covers
  lines 69–71); exactly 1 occurrence in the copy.
- Context read: lines 32–73 — the whole function, including `available =
  global_zone_page_state(NR_FREE_PAGES) - totalreserve_pages;` (line 47), the two `min(…/2, wmark_low)`
  additions (lines 56–57 and 66–67), the clamp `if (available < 0) available = 0;` (lines 69–70) and
  `return available;` (line 71).
- What the context shows: (i) the clamp is stated verbatim — `if (available < 0) available = 0;`; (ii)
  the condition "when the reserves exceed everything counted" follows from the function body — `available`
  starts as `NR_FREE_PAGES − totalreserve_pages` and only non-negative remainders are added, so the
  pre-clamp sum is negative exactly when `totalreserve_pages` exceeds the free count plus those remainders;
  (iii) the function's final statement is `return available;` — it returns the clamped value; nothing in
  `show_mem.c` states that any `/proc/meminfo` line prints this value or that a line "reads" anything.
- Judgment: the clamp and the condition are entailed by the quote plus context. The clause "the line reads
  zero instead of a negative figure" asserts the behavior of the printed `/proc/meminfo` `MemAvailable`
  line. That printing behavior is stated by S494, not by this row's source: `meminfo.c.v7.2` line 56
  `available = si_mem_available();` and line 62 `show_val_kb(m, "MemAvailable:   ", available);` (read to
  confirm the claim is true — it is — but that chain belongs to the S494 row of this same entry, row 16).
  Under the frozen strict rule, a claim that adds a consequence the source does not state is an overclaim:
  `show_mem.c` does not state the printed line's behavior. Overclaim.

ENTAIL ec0f6c97eeba overclaim — the line reads zero instead of a negative figure

Replacement claim cell (judged entailed from the same quote plus context; >= 6 words; >= 3 words of 3+
letters absent from the quote — negative, clamped, zero, never, estimate, reserves, exceed, everything,
counted, result, when):

"A negative result is clamped to zero, so the returned estimate is never negative when the reserves exceed
everything counted."

- Recomputed hash with the frozen one-liner: d901a2d666fb.
- Judgment: the clamp (`if (available < 0) available = 0;`), the return of the clamped value (`return
  available;` — hence "the returned estimate is never negative") and the reserve-overrun condition (from
  the function body, as above) are all within the quote plus context. The phrase "the line reads zero" is
  dropped because it rests on S494, not on this row's source.

ENTAIL d901a2d666fb entailed

## Evidence commands

- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 87e0c374537557754bf71dd68036ded3ddc6699c:corpus/knowledge/memavailable-estimate-r51.md` → rc 0; 21 table rows parsed programmatically, no manual transcription.
- Same command for `corpus/evidence/sources-r51/show_mem.c.v7.2`, `…/meminfo.c.v7.2`, `…/34e431b0.patch` → rc 0 for each.
- Frozen one-liner hash recompute over the claim cells as parsed → cbcd91de05ac, 58ba82f481b8, ec0f6c97eeba — all three match rows 10–12 of `.ufo/waves/round-51/evidence/c2-hashes-at-data.txt`; no mismatches across all 21 rows; replacement → d901a2d666fb.
- Whitespace-collapsed quote search over the S493 copy → row 10 unique at show_mem.c.v7.2:66–67; row 11 unique at :60–61; row 12 unique at :69–71.
- `sha256sum` over the copies → the three values in Copy integrity above, all equal to the frozen entries in `.ufo/waves/round-51/evidence/freeze-sha256.txt`.
- Disk-guard before the run: `/fast/scratch/hyaku` 25 % used, 604.2 G free; no ENOSPC.

## Named limits of this judgment

- Per the frozen predicate, these votes record this seat's judgment that each claim follows from the quote
  plus about 20 lines of context of its own cited source; cross-source facts (e.g. row 12's printing chain
  in S494) were deliberately not allowed to rescue a claim anchored to a different source.
- An `overclaim` vote blocks the row until the L1 replaces the claim text; the replacement above is offered
  as text this seat judges entailed (new hash d901a2d666fb), per the frozen resolution path. Votes are
  never deleted from a report.
- v7.2 bytes only; nothing here speaks about other kernels or hosts.
- The wave expects at least two seats of different roles per row; this report is one seat's judgment, not
  outside verification.

## Findings

- HIGH — row 12 (`corpus/knowledge/memavailable-estimate-r51.md`, Claims row 12): overclaim — the clause
  "the line reads zero instead of a negative figure" asserts the printed `/proc/meminfo` MemAvailable
  line's behavior, which the row's source (show_mem.c.v7.2 / S493) does not state; the printing chain lives
  in meminfo.c.v7.2 (S494), this entry's row 16. The clamp and the reserve-overrun condition are entailed;
  replacement claim proposed with hash d901a2d666fb.
- LOW — row 11 (same file, Claims row 11): the claim attributes the holdback's rationale to "some
  reclaimable slab objects"; the comment says "Part of the reclaimable slab and other kernel memory consists
  of items that are in use, and cannot be freed." Judged entailed under the natural distributive reading
  (and the sentence's origin as a slab-only statement in the S496 patch), but a strictly collective parse
  would not isolate the slab subset; a cell saying "some of the reclaimable slab and other kernel memory is
  in use and cannot be freed" would match the source's scope even more exactly.
- LOW — row 10 (same file, Claims row 10): the block comment above the code (line 61) says only "Cap this
  estimate at the low watermark" while the code caps at `min(reclaimable / 2, wmark_low)`; the claim
  correctly follows the code (the quote), but the comment alone would not support the "half" part.
- No counter weakness observed within this seat's scope (counters, predicates and kill rules are frozen and
  were not changed; the C2 entailment arm behaved as specified — rows 10–12 required exactly one verdict
  line each, plus the replacement line for the dissent).
