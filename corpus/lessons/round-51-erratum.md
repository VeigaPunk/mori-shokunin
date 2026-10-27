# Round 51 erratum (append-only; filed round 52)

Appended to the filed round-51 lesson per the round-51 closure's routed defects D-c and D-d
(`corpus/lessons/round-51-verifier-spotcheck.md` §1). Nothing in the filed lesson is rewritten.

## D-c — S493 locators in the round-51 lesson's `### Spot-check`

The round-51 lesson cited `:55-57`, `:62`, `:67-69`, `:71-72` for the S493 Gate table. The committed copy
`corpus/evidence/sources-r51/show_mem.c.v7.2` holds the lines at different numbers; the closed ranges are:

| lesson said | copy actually holds | command |
|---|---|---|
| `:55-57` `pagecache = … NR_ACTIVE_FILE + … NR_INACTIVE_FILE` | `:54-55` (`pagecache = global_node_page_state(NR_ACTIVE_FILE) +` / `global_node_page_state(NR_INACTIVE_FILE);`) | `grep -nF 'pagecache = global_node_page_state(NR_ACTIVE_FILE) +' corpus/evidence/sources-r51/show_mem.c.v7.2` |
| `:62` `pagecache -= min(pagecache / 2, wmark_low);` | `:56` | `grep -nF 'pagecache -= min(pagecache / 2, wmark_low);' …` |
| `:67-69` the reclaimable slab/misc terms under the same `min(… / 2, wmark_low)` cap | `:64-67` (`reclaimable = …NR_SLAB_RECLAIMABLE_B) +` `:65`, `global_node_page_state(NR_KERNEL_MISC_RECLAIMABLE);` `:66`, `reclaimable -= min(reclaimable / 2, wmark_low);` `:67`) | `grep -nF 'reclaimable = global_node_page_state_pages(NR_SLAB_RECLAIMABLE_B) +' …` |
| `:71-72` `if (available < 0) available = 0;` | `:69-70` | `grep -nF 'if (available < 0)' …` |
| the Gate table's `23,32-73` anchor | holds (function at `:32-73`, totalreserve_pages at `:23`, export at `:73`) | — |

The Gate table (54-56) and the SOURCES anchor (`23,32-73`) in the filed lesson are right; only the Spot-check
bullets drifted. The round-52 lesson M2 records that a frozen data applier's axes edit matched history rows too,
and the C1 arm (D) now checks quoted strings against named lines for the Axes rows and SHONEN boxes.

## D-d — the famzah 2014 page

The filed lesson called the only `memavailable` hit on the refused page "a reader's 2017 comment". Verified
2026-10-26 (round 52):

- `https://blog.famzah.net/2014/09/22/know-your-linux-memory-usage/` returns HTTP 200 (134475 bytes, sha256
  `0de988789c371c2c800a2b5fc320389d307efa390c11fb55dfc7061070ada6bb`).
- `grep -c 'MemAvailable'` → 0 (rc 1); case-insensitive `memavailable` → 3 hits, all the 2017 **author reply**
  (Ivan Zahariev, May 13 2017) linking `https://github.com/famzah/linux-memavailable-procfs`.
- The exact string `MemAvailable` occurs 0 times; the page never defines the estimate, so the S-row rejection
  stands. The attribution is corrected: the 2017 post is the blog author's reply, not a reader's.
