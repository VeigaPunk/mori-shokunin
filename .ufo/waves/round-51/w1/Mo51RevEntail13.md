# Mo51RevEntail13 — entailment votes, claim rows 13–15 (mori round 51, wave w1)

Seat: Mo51RevEntail13 (reviewer, ENTAILMENT item, leaf — no subagents).
Data commit: `87e0c374537557754bf71dd68036ded3ddc6699c`. Frozen contract: `.ufo/waves/round-51/contract.md` (read first).
Assigned rows: 13–15 of the `## Claims` table of `corpus/knowledge/memavailable-estimate-r51.md` at the data commit.
Row 13 draws on source S493 (committed copy `corpus/evidence/sources-r51/show_mem.c.v7.2`); rows 14–15 draw on
source S494 (committed copy `corpus/evidence/sources-r51/meminfo.c.v7.2`).

## Method and provenance

- Committed bytes, not worktree guesses: every file was read via `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 87e0c374537557754bf71dd68036ded3ddc6699c:<path>`. A read-only `git diff --stat 87e0c374 -- corpus/knowledge/memavailable-estimate-r51.md corpus/evidence/sources-r51/ corpus/SOURCES.md` returned empty and exit 0, so the worktree matches the data commit for every path I judged.
- Copy integrity: `sha256sum` of the extracted copies = `dba76b263bbdf93323a277a29c9281a892ff3fb35ddd6f0ddaf9ba1acb5b02f5` (show_mem.c.v7.2) and `d6c5807421a69eac21efd737b39d099c711b3132b371dc34986d181746e3deda` (meminfo.c.v7.2), equal to the sha256 named in the S493/S494 rows of `corpus/SOURCES.md` (lines 272 and 273 at the data commit).
- Hash verification: the three claim cells were extracted programmatically from the committed entry's table (21 rows parsed; no transcription trusted) and re-hashed with the prescribed one-liner. All three outputs equal the frozen values in `.ufo/waves/round-51/evidence/c2-hashes-at-data.txt` (row 13 `40b46a312e03`, row 14 `a06f1037d952`, row 15 `102feb3debfa`).
- Quote location: each quote, whitespace-collapsed with the counter's collapse (`re.sub(r"\s+"," ", ...)` on the committed bytes), occurs exactly once in its committed copy (count = 1 for each). Locations: row 13 → `show_mem.c.v7.2` lines 38–41; row 14 → `meminfo.c.v7.2` lines 30–31; row 15 → `meminfo.c.v7.2` lines 48–49.
- Context: I read ≈20 lines around each quote in the committed copies (row 13: show_mem.c lines 32–80; rows 14–15: meminfo.c lines 28–69 and the remainder of `meminfo_proc_show`, lines 34–178, to test the "every meminfo value" scope).

## Row judgments

### Row 13 — hash `40b46a312e03`

Claim cell: "The watermark used for both holdbacks is the low watermark summed over every memory zone of the machine."

Quote: `` `struct zone *zone; for_each_zone(zone) wmark_low += low_wmark_pages(zone);` `` — located at `corpus/evidence/sources-r51/show_mem.c.v7.2` lines 38–41 (line 38 `struct zone *zone;`, blank line 39, line 40 `for_each_zone(zone)`, line 41 `wmark_low += low_wmark_pages(zone);`), unique under whitespace collapse.

Context read (show_mem.c.v7.2 lines 32–72): `si_mem_available()` declares `unsigned long wmark_low = 0;` (line 36), sums it at lines 40–41 over `for_each_zone(zone)` (`wmark_low += low_wmark_pages(zone);`), then uses the same `wmark_low` in exactly two holdbacks: line 56 `pagecache -= min(pagecache / 2, wmark_low);` and line 66 `reclaimable -= min(reclaimable / 2, wmark_low);`. `for_each_zone` is the kernel's all-zones iterator, so "summed over every memory zone of the machine" is a plain rendering of the code; "both holdbacks" matches the two `min(..., wmark_low)` uses in the same function.

Verdict: entailed.

### Row 14 — hash `a06f1037d952`

Claim cell: "Every meminfo value goes through one helper that shifts a page count by PAGE_SHIFT minus 10 and prints the result in kB."

Quote: `` `seq_put_decimal_ull_width(m, s, num << (PAGE_SHIFT - 10), 8); seq_write(m, " kB\n", 4);` `` — located at `corpus/evidence/sources-r51/meminfo.c.v7.2` lines 30–31 (the body of `show_val_kb`, defined lines 28–32), unique.

Context read (meminfo.c.v7.2 lines 28–178): `show_val_kb` is one helper, and dozens of lines are printed through it (lines 60–171). But the same `meminfo_proc_show` also prints meminfo values directly with `seq_printf` and not through `show_val_kb`: `Zswapped` (lines 93–95), `KernelStack` (lines 111–112), `ShadowCallStack` (lines 114–115), `VmallocTotal` (lines 127–128, `>> 10` bytes-to-kB, no `PAGE_SHIFT - 10` shift), `HardwareCorrupted` (lines 137–138), and it hands further meminfo lines to `memtest_report_meminfo(m)` (line 134), `hugetlb_report_meminfo(m)` (line 173) and `arch_report_meminfo(m)` (line 175), which are outside this helper. The universal scope "Every meminfo value goes through one helper" is therefore contradicted by the source copy itself; the claim adds a scope the source does not state (and affirmatively denies). The shift-and-kB half of the claim is exactly the quote, but the "every … one helper" scope is not.

Verdict: overclaim — the words that go beyond the source are "Every meminfo value goes through one helper".

### Row 15 — hash `102feb3debfa`

Claim cell: "The Cached figure is computed from all file pages minus swap cache and buffers, a different base from the two file LRU lists."

Quote: `` `cached = global_node_page_state(NR_FILE_PAGES) - total_swapcache_pages() - i.bufferram;` `` — located at `corpus/evidence/sources-r51/meminfo.c.v7.2` lines 48–49 (line 48 `cached = global_node_page_state(NR_FILE_PAGES) -`, line 49 `		total_swapcache_pages() - i.bufferram;`), unique.

Context read (meminfo.c.v7.2 lines 34–69): `cached` is computed at lines 48–49, clamped at zero at lines 50–51, and printed as the `Cached:` line at line 64. `available = si_mem_available();` at line 56 shows the estimate is computed by a separate function, so the first half of the claim ("computed from all file pages minus swap cache and buffers") and the bare comparative ("a different base" from whatever `si_mem_available()` computes) follow. But the claim names the estimate's page-cache base as "the two file LRU lists" — that fact appears nowhere in this source: `meminfo.c` reads `pages[LRU_ACTIVE_FILE]` / `pages[LRU_INACTIVE_FILE]` (lines 53–54, 72–73) for the `Active(file)`/`Inactive(file)` lines, and never states that the estimate's base is those two lists. That identification is S493's fact (`show_mem.c.v7.2` lines 54–55: `pagecache = global_node_page_state(NR_ACTIVE_FILE) + global_node_page_state(NR_INACTIVE_FILE);`). Per the per-row method (quote plus context in the row's own committed copy), the comparative tail adds a scope the source does not state.

Verdict: overclaim — the words that go beyond the source are "a different base from the two file LRU lists".

## Verdict lines (one per assigned row; plus one replacement line per overclaim)

ENTAIL 40b46a312e03 entailed
ENTAIL a06f1037d952 overclaim — "Every meminfo value goes through one helper"
ENTAIL 6c2327e19df1 entailed
ENTAIL 102feb3debfa overclaim — "a different base from the two file LRU lists"
ENTAIL 7e14f1771092 entailed

## Replacement proposals (for the two overclaims)

Row 14 replacement claim cell (same source S494, same quote, ≥ 6 words, ≥ 3 words of 3+ letters absent from the quote — 16 such words):

> The meminfo printer defines one helper that shifts its argument by PAGE_SHIFT minus 10 and writes the kB suffix.

Hash: `6c2327e19df1` (computed with the prescribed one-liner). Judged entailed: `show_val_kb` is defined in meminfo.c (lines 28–32), `num << (PAGE_SHIFT - 10)` is exactly the shift, and `seq_write(m, " kB\n", 4)` is exactly the kB suffix; "one helper" is scoped by the relative clause (the helper that shifts-and-writes-kB), which matches precisely this one function and does not claim every meminfo value uses it.

Row 15 replacement claim cell (same source S494, same quote, ≥ 6 words, ≥ 3 words of 3+ letters absent from the quote — 16 such words):

> The Cached figure is computed from all file pages minus swap cache and buffers, and clamped at zero if negative.

Hash: `7e14f1771092` (computed with the prescribed one-liner). Judged entailed: the computation is lines 48–49 of meminfo.c.v7.2 and the zero clamp is lines 50–51 (`if (cached < 0) cached = 0;`), both in the quote's immediate context. The comparative tail naming the estimate's base is dropped because S494 does not state it.

## Evidence log (command → output → exit)

1. `git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree -r --name-only 87e0c374537557754bf71dd68036ded3ddc6699c -- corpus/evidence/sources-r51/` → the five frozen copies (`34e431b0.patch`, `meminfo.c.v7.2`, `mm_inline.h.v7.2`, `proc.rst.v7.2`, `show_mem.c.v7.2`) → exit 0.
2. `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --stat 87e0c374537557754bf71dd68036ded3ddc6699c -- corpus/knowledge/memavailable-estimate-r51.md corpus/evidence/sources-r51/ corpus/SOURCES.md` → empty output, exit 0 (worktree matches the data commit for these paths).
3. `git show 87e0c374…:corpus/evidence/sources-r51/show_mem.c.v7.2` and `…:meminfo.c.v7.2`, then `sha256sum` → `dba76b263bbdf93323a277a29c9281a892ff3fb35ddd6f0ddaf9ba1acb5b02f5`, `d6c5807421a69eac21efd737b39d099c711b3132b371dc34986d181746e3deda` → match SOURCES.md:272 (S493) and :273 (S494) → exit 0.
4. Programmatic extraction of the committed Claims table (21 rows) + hash one-liner on rows 13–15 → `40b46a312e03`, `a06f1037d952`, `102feb3debfa` → all equal `.ufo/waves/round-51/evidence/c2-hashes-at-data.txt` rows 13–15.
5. Whitespace-collapsed (`re.sub(r"\s+"," ", ...)`) occurrence count of each quote in its committed copy → 1, 1, 1 (unique each). Note: a naive per-line join reports 0 for row 13 because the quote spans a blank line (39); the counter's collapse finds it at lines 38–41.
6. `grep -nE 'seq_printf|show_val_kb|_report_meminfo'` on the committed meminfo.c.v7.2 → seq_printf at lines 93, 111, 114, 127, 137; external meminfo reporters called at lines 134 (`memtest_report_meminfo`), 173 (`hugetlb_report_meminfo`), 175 (`arch_report_meminfo`) → exit 0.
7. `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` → `/fast/scratch/hyaku 25% 604.0G free`, no ENOSPC.

## Limits and UNVERIFIED

- I judged the claim cells against the committed copies only. I did not re-fetch the five source URLs; that the URLs still return these bytes today is UNVERIFIED by me (the counter's pin arm and the entry's `recheck:` line cover it; both copies' sha256 match their SOURCES rows, which is the internal consistency check available locally).
- Per the per-row method, a claim whose comparative tail rests on a different source (row 15's "the two file LRU lists", which is S493's fact) is judged an overclaim even though the entry as a whole supports it. This strictness is a named method limit: the row's own source must carry the claim; cross-source synthesis would need the row to cite or quote the second source.
- The C2 counter's entailment arm is read as specified: a line starting `ENTAIL` + 12 lowercase hex + `overclaim` blocks the row until the L1 replaces the claim cell; my two replacement cells above carry `entailed` lines (new hashes) so the rows can be resolved by text replacement without touching the frozen counter.
- I wrote no verdict for rows 1–12 or 16–21 and no vote on any text other than the three assigned claim cells and my two replacement proposals.

## Tooling

No tool was installed or upgraded (nothing needed: `git show`, `sha256sum`, `grep`, `python3` hashlib/re only). No pacman transaction was run (host-wide pause respected). No writes outside my report file and my scratch.

## Scratch

Scratch root `/fast/scratch/hyaku/mori-r51/Mo51RevEntail13/` (with `tmp/` as TMPDIR). Every cited line and quote is quoted inside this report; the directory is removed after this report is written. No clone was made (read-only `git show` from the lane only); the lane repo, its jj state and its git index were not mutated. Host reads were read-only (no `/proc`, kernel-log or configuration reads beyond `/etc/machine-id`); free disk checked before work via the disk guard.

## Findings

- HIGH — `corpus/knowledge/memavailable-estimate-r51.md` row 14 (claim cell; source `corpus/evidence/sources-r51/meminfo.c.v7.2:28-178`): the claim "Every meminfo value goes through one helper" is contradicted by the source copy: `Zswapped` (93–95), `KernelStack` (111–112), `ShadowCallStack` (114–115), `VmallocTotal` (127–128) and `HardwareCorrupted` (137–138) are printed with `seq_printf`, and `memtest_report_meminfo`/`hugetlb_report_meminfo`/`arch_report_meminfo` (134, 173, 175) print further meminfo lines outside `show_val_kb`. Overclaim voted; replacement cell proposed (hash `6c2327e19df1`).
- MED — `corpus/knowledge/memavailable-estimate-r51.md` row 15 (claim cell; source `corpus/evidence/sources-r51/meminfo.c.v7.2:48-56`): the tail "a different base from the two file LRU lists" names the estimate's page-cache base, which S494 never states (that fact is S493's, `show_mem.c.v7.2:54-55`). Overclaim voted; replacement cell proposed (hash `7e14f1771092`).
- LOW — `corpus/knowledge/memavailable-estimate-r51.md` Reading rules, first bullet of "Units are kB on every meminfo line (row 14)": this rule leans on the row-14 claim; as written, row 14 is an overclaim. Within `meminfo.c.v7.2` itself every printed line is indeed kB (the `seq_printf` lines all print a kB suffix), so the units statement is supported for the lines this file prints; but `/proc/meminfo` also contains lines from `hugetlb_report_meminfo`/`arch_report_meminfo` (called at lines 173/175), whose units are outside this copy — UNVERIFIED here. If the L1 replaces the row-14 cell, the reading rule should be re-anchored.
- LOW — Method limit (named, not a defect): the per-row entailment method judges overclaim any claim whose support requires a sibling source of the same entry (row 15's tail). This is the strict reading of the seat instruction; it is recorded so the L1 can weigh it against the entry-wide reading if it prefers.
