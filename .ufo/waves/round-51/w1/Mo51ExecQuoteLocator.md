# Mo51ExecQuoteLocator — own quote locator and anchor containment for the C2 entry

Seat: Mo51ExecQuoteLocator (executor, leaf). Lane: mori-shokunin. Wave: round-51 `w1`.
Data revision read: `87e0c374537557754bf71dd68036ded3ddc6699c` (entering tip `aa3af1ec`).
Lane HEAD while I ran: `b504cb1701568a0038aab9d98ec13d28eff801da` (dispatch + at-data receipts).

Scope: my own locator (not `count-c2.py`), the claims table of `corpus/knowledge/memavailable-estimate-r51.md`
at R, S-id -> copy via the `corpus/SOURCES.md` rows, 1-based line spans of each quote in the raw copy, and
whether each quote's span falls inside the anchor ranges of its row S492-S496. I cast no entailment vote and
wrote no vote lines: the vote word appears in this report only inside sentences, never at line start.

## Commands and exit codes

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin show \
    87e0c374537557754bf71dd68036ded3ddc6699c:corpus/knowledge/memavailable-estimate-r51.md > entry.md
$ git -C ... show 87e0c37:corpus/SOURCES.md > sources.md
$ git -C ... show 87e0c37:corpus/evidence/sources-r51/{proc.rst.v7.2,show_mem.c.v7.2,meminfo.c.v7.2,
      mm_inline.h.v7.2,34e431b0.patch} > <same names>            # rc 0 each (one pipeline, rc 0)
$ wc -l entry.md sources.md *.v7.2 34e431b0.patch
      65 entry.md   336 sources.md   188 meminfo.c.v7.2   670 mm_inline.h.v7.2
    2495 proc.rst.v7.2   464 show_mem.c.v7.2   133 34e431b0.patch
$ diff <(cat entry.md) /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/knowledge/memavailable-estimate-r51.md
                                                               # empty; rc 0 -> entry identical at R and HEAD
$ python3 locate.py        # rc 0: rows parsed=21, outside=0
$ python3 verify.py        # rc 0: linecheck_failures=0
$ python3 verify2.py       # rc 0: disagreements=0
$ python3 verify3.py       # rc 0: boundary columns + parsed anchor ranges
$ python3 .ufo/waves/round-51/count-c2.py --hashes 87e0c374537557754bf71dd68036ded3ddc6699c
                                                               # rc 0, 21 rows printed (read-only: git show/ls-tree)
```

Scratch: `/fast/scratch/hyaku/mori-r51/Mo51ExecQuoteLocator/` with `TMPDIR=.../tmp`; removed at the end
(`rm -rf`, exit 0 — verified absent). No clone was needed: the entry, SOURCES.md and the five copies were taken
with read-only `git show`. No pacman, no install, no tool upgrade; nothing written outside the report path.

## Locator method (three independent passes, same answer)

1. **Parse**: claims table = lines between the `| claim | source | quote |` header and the blank line before
   `## Reading rules`; 3 cells per row; quote cell must be exactly one backticked span. 21 rows parsed
   (`grep -c "^| " entry.md` = 22 = header + 21 rows). S-id -> copy is read from the SOURCES row's anchor cell
   (`copy <path> sha256 <hex>`), not from the counter's URL map.
2. **Collapse + line map**: every whitespace run in the raw copy becomes one space while recording, for each
   collapsed character, its 1-based source line; the collapsed quote (same collapse) is `str.find`-ed; the
   start/end line are read off the map. Line-map correctness was re-checked by rebuilding the raw span from
   `splitlines()` of the reported line range and requiring the quote to occur in its collapsed form.
3. **Independent regex pass** (`verify2.py`): the quote's tokens joined with `\s+` are compiled and searched in
   the raw bytes; line number = newline count before the match. This never touches the collapse array. It agreed
   with pass 2 on all 21 rows (`disagreements=0`) and found **exactly one match in the raw copy for every quote**
   (`matches-in-raw` = 1 on all rows), so no row's line number depends on a choice among ambiguous hits.

C-comment continuation is handled as the item requires: it is part of the quote, so e.g. row 9's quote
`Not all the page cache can be freed, otherwise the system will * start swapping or thrashing.` matches with the
`*` of raw line 51 and starts at the `N` of line 50 (col 4). Wrapped prose is likewise handled — row 3's quote
begins at column 67 of line 1133 (word `The`) and ends on line 1134.

## Result: | S-id | copy | line | found

Numbering = claim-table row order. `line` is the 1-based span in the raw copy (start, or start-end when the
quote wraps); `found` = yes when the whitespace-collapsed quote occurs in that copy (unique, one hit per row).

| S-id | copy | line | found |
|---|---|---|---|
| S492 | proc.rst.v7.2 | 1127-1128 | yes |
| S492 | proc.rst.v7.2 | 1128-1130 | yes |
| S492 | proc.rst.v7.2 | 1133-1134 | yes |
| S492 | proc.rst.v7.2 | 1139-1140 | yes |
| S492 | proc.rst.v7.2 | 1193 | yes |
| S493 | show_mem.c.v7.2 | 45-47 | yes |
| S493 | show_mem.c.v7.2 | 52-55 | yes |
| S493 | show_mem.c.v7.2 | 56-57 | yes |
| S493 | show_mem.c.v7.2 | 50-51 | yes |
| S493 | show_mem.c.v7.2 | 66-67 | yes |
| S493 | show_mem.c.v7.2 | 60-61 | yes |
| S493 | show_mem.c.v7.2 | 69-71 | yes |
| S493 | show_mem.c.v7.2 | 38-41 | yes |
| S494 | meminfo.c.v7.2 | 30-31 | yes |
| S494 | meminfo.c.v7.2 | 48-49 | yes |
| S494 | meminfo.c.v7.2 | 61-62 | yes |
| S495 | mm_inline.h.v7.2 | 25-26 | yes |
| S495 | mm_inline.h.v7.2 | 23-24 | yes |
| S496 | 34e431b0.patch | 7-8 | yes |
| S496 | 34e431b0.patch | 11-12 | yes |
| S496 | 34e431b0.patch | 21-23 | yes |

Totals: 21 rows, 21 located (`found=yes`), 0 missing, 0 with a second hit. 14 of the 21 spans wrap lines
(rows 2, 3, 6, 7, 9, 11, 12, 13, 14, 15, 16, 17, 18, 21); the other 7 (rows 1, 4, 5, 8, 10, 19, 20) fit on one
line and are located by start line.

## Cross-checks

- **Copies match the SOURCES sha256 cells and the entry's recheck list** (`sha256sum` of the five files):
  `e760f716f827…` proc.rst, `dba76b263bbd…` show_mem.c, `d6c5807421a6…` meminfo.c, `2d4accbbc1ec…` mm_inline.h,
  `9f571a04fc36…` 34e431b0.patch. The SOURCES anchor cells carry the same five hex strings, and each is the same
  copy the counter's `COPIES` table names (read at `count-c2.py:46-57`), so my SOURCES-derived copy mapping and
  the counter's URL mapping agree for all 5 ids.
- **Claim hashes agree with the counter.** My sha256-of-collapsed-claim first-12 values
  (`2d0daa4192f1, eba2b78b47f3, ad57d1b66582, 72cdbee44353, a9cf30c5ed71, 5d06a2ae70cf, 6c8b6efc9731,
  6b8f33ed528e, 1b9c863ec2c2, cbcd91de05ac, 58ba82f481b8, ec0f6c97eeba, 40b46a312e03, a06f1037d952,
  102feb3debfa, 357c747c23d2, d6001a798ea7, 8f6d04247472, a07e4bd7a5ec, 4d162ecf1409, 50f54829ae20`) equal
  `count-c2.py --hashes 87e0c37` row-for-row, so both readers parsed the same 21 claims and collapsed them
  identically.
- **Anchors and copies are the same file version**: the labelled anchor lines land on the labelled text —
  proc.rst 1124 `MemFree`, 1126 `MemAvailable`, 1138 `Cached`, 1192 `Shmem`, 1194 `KReclaimable`,
  1200 `SReclaimable`; show_mem.c 23 `unsigned long totalreserve_pages __read_mostly;`; meminfo.c 105
  `show_val_kb(m, "Shmem:          ", i.sharedram);`.

## Anchor comparison against SOURCES rows S492-S496

Parsed ranges (from the anchor cells, 1-based lines of the committed copies):

| S-id | parsed ranges | quote spans | all inside? |
|---|---|---|---|
| S492 | 1124-1135, 1138-1141, 1192-1201 | 1127-1128, 1128-1130, 1133-1134, 1139-1140, 1193 | yes (5/5) |
| S493 | 23, 32-73 | 38-41, 45-47, 50-51, 52-55, 56-57, 60-61, 66-67, 69-71 | yes (8/8) |
| S494 | 27-31, 48-51, 56, 61-64, 105 | 30-31, 48-49, 61-62 | yes (3/3) |
| S495 | 13-31 | 23-24, 25-26 | yes (2/2) |
| S496 | commit message 6-27 (+ patch hunks, which start at line 65 `diff --git a/fs/proc/meminfo.c`) | 7-8, 11-12, 21-23 | yes (3/3) |

**Quotes outside their row's anchors: none (0 of 21).** No span merely touches a boundary either: every quote's
whole start-end span is contained in one declared range, and no quote lands in an undeclared gap between ranges
(S492's gaps 1136-1137, 1142-1191 and 1202+ hold no quote; every S494-S496 quote likewise lands in a declared
range, and the two declared-but-unused S494 lines 56 and 105 and the S496 patch-hunk block are simply not quoted).

## Notes on what the locator can and cannot say (limits)

- A located quote proves the character sequence occurs contiguously in the committed copy with only whitespace
  between the words. It does not prove the words mean what the claim cell says; that is the entailment arm's
  question, and I cast no vote.
- My line numbers are lines of the committed copies under `corpus/evidence/sources-r51/`; they are not lines of
  upstream `v7.2` at GitHub (the copies are the frozen bytes the predicate names).
- Anchor containment is a scope check on ranges, not an entailment check: a quote inside the declared range can
  still be the wrong sentence for its claim.
- The locator deliberately does not consult `count-c2.py`; the only thing I ran from the frozen set was the
  read-only `--hashes` mode, for the cross-check above.

## Evidence retained

Row 7's start position (raw `show_mem.c.v7.2`, line 52, column 41 — the **second** `cache,` on that line):

```
    50|	 * Not all the page cache can be freed, otherwise the system will
    51|	 * start swapping or thrashing. Assume at least half of the page
    52|	 * cache, or the low watermark worth of cache, needs to stay.
    53|	 */
    54|	pagecache = global_node_page_state(NR_ACTIVE_FILE) +
    55|		global_node_page_state(NR_INACTIVE_FILE);
```

Row 3's wrap (raw `proc.rst.v7.2`, start column 67 on 1133, ends 1134):

```
  1133|              slab will be reclaimable, due to items being in use. The
  1134|              impact of those factors will vary from system to system.
```

Row 4 / row 5 against the S492 anchor groups:

```
  1138|Cached
  1139|              In-memory cache for files read from the disk (the
  1140|              pagecache) as well as tmpfs & shmem.
  1141|              Doesn't include SwapCached.
   ...
  1192|Shmem
  1193|              Total memory used by shared memory (shmem) and tmpfs
```

## Findings

- **LOW — `corpus/knowledge/memavailable-estimate-r51.md` row 7 (quote), located at `show_mem.c.v7.2:52-55`.**
  The quote `cache, needs to stay. */ pagecache = …` starts mid-sentence at the *second* `cache,` on raw line 52
  (col 41), eliding `or the low watermark worth of` from the same sentence. The words are contiguous, so the
  located arm and the anchors both pass; but the fragment reads as the whole clause while the elided half states
  the low-watermark rule that row 8's claim covers. Worth an entailment seat's attention; not a counter or anchor
  defect, and I did not change it.
- **LOW — `corpus/SOURCES.md` row S492 anchor cell (`proc.rst:1124-1135 (MemFree, MemAvailable)`).** The range
  ends on line 1135, which is the `Buffers` heading — one line past the `MemAvailable` paragraph it labels
  (1126-1134). Containment is unaffected (no quote uses 1135); the labelled range is simply one line loose.
  Same pattern, no action needed: 1192-1201 also includes `Slab` (1198-1199) next to the labelled Shmem /
  KReclaimable / SReclaimable.
- **LOW (method) — anchor containment is not part of P-C2.** The counter checks location in the copy only, so a
  quote could pass while sitting outside its row's declared anchor range and no counter would say so. This run
  found zero such rows; the check is mine, not the frozen predicate's.
