# Mo54ExecLineArm — C1 independent line arm (mori round 54, wave w1)

Seat: executor (leaf). Lane repo `/home/vgpnk/Projects/shokunin/mori-shokunin`, fleet root
`/home/vgpnk/Projects/shokunin`. Data revision `78295c764093ff1f6cee08d7246679900bde7265`, entering tip
`39dcf4d7e410d362781a47e8365ca23b5c807598`. Scratch `/fast/scratch/hyaku/mori-r54/Mo54ExecLineArm/`
(created, used, removed). No tool installed or upgraded.

Assignment: for each of the 31 ledger rows of `corpus/knowledge/kernel-v7.3-recheck-r54.md`, find **every** line
of the v7.3 copy on which the row quote begins, compare with the ledger's `line` cell; repeat against the v7.2
copies and check every v7.2 line, v7.3 line and `moved` value of the ledger's `## Where the quotes moved` table.

## Method

- Own locator `locator.py` (scratch): parses the ledger table, the movement table, `evidence/c1-claims.txt` and
  the SOURCES rows itself; **does not import** `.ufo/waves/round-54/count-c1.py` and does not run it.
- Match semantics taken from the claim, implemented independently: the ledger quote (backtick span, whitespace
  collapsed) is searched in a whitespace-collapsed copy; the reported line is the **raw** line holding the first
  matched character (byte offset → newline count + 1). All occurrences are collected (`str.find` with `start=i+1`),
  not just the first.
- HTML: a char-wise state machine (not the counter's single regex) drops comments / `script` / `style`, reads every
  other tag token as one space, decodes entities (`html.unescape`), maps each surviving character to its raw offset,
  then collapses whitespace. This is the rendered-text reading of `<dt>anon</dt><dd><p>Amount …`.
- Extra checks per row: both characters bounding each match must be non-word (no mid-token artefact); the span
  `start..end` of each match; ledger `status` vs occurrence; ledger `line` ∈ located lines.
- v7.2 side: same locator on the committed v7.2 copies, compared **both ways** with the claims file and with the
  movement table, plus a diff-based cross-check (net added-minus-deleted lines the v7.2→v7.3 diff places before
  each quoted v7.2 line must equal `moved`).
- Row binding: claim tables of every knowledge entry at `39dcf4d7` → `sha256(ws(claim))[:12]` → ledger row, plus
  an independent re-derivation of the v7.2 pin set from SOURCES at the entering tip.
- Fresh upstream bytes: all 8 v7.3 and all 8 v7.2 copies re-fetched (cgit `?h=<tag>`, `docs.kernel.org/{7.2,7.3}`)
  and the locator re-run on the fetched bytes, so the line cells are confirmed against upstream text, not only
  against the committed copies.

Commands and exit codes (all run in the scratch dir, `TMPDIR` inside it):

```
python3 locator.py        -> EXIT=0   (31 rows, "problems (31)" = my own entry-cell backtick compare bug, fixed for chain.py; see E4)
python3 chain.py          -> EXIT=0   (problems (0))
python3 prose.py          -> EXIT=0   (delta mismatches: 0)
python3 verify_fetch.py   -> EXIT=0   (mismatches vs fresh upstream bytes: 0)
```

## E1 — the bytes I located in are the committed bytes and the pinned bytes

Worktree vs the data commit (read-only `git show`):

```
same corpus/knowledge/kernel-v7.3-recheck-r54.md
same corpus/SOURCES.md
same corpus/evidence/sources-r54/memcontrol.c.v7.3
same corpus/evidence/sources-r54/cgroup-v2.7.3.html
same corpus/evidence/sources-r53/mm_init.c.v7.3
same corpus/evidence/sources-r53/util.c.v7.3
```

Fresh fetches, sha256 (2026-10-27), all equal to the committed copies and to the SOURCES and counter pin prefixes:

```
v7.3  bdb6159cc237… memcontrol.c      452f1348e79c… oom_kill.c        2c26e67751f9… percpu_counter.c
v7.3  4a107bc381b3… percpu_counter.h  66a5ad60566f… errno.h           4dfcce2b8fa8… util.c
v7.3  678410005f88… mm_init.c         b478c1bae998… cgroup-v2 (docs.kernel.org/7.3 rendered page)
v7.2  8a28e0bc010e… memcontrol.c      452f1348e79c… oom_kill.c        2c26e67751f9… percpu_counter.c
v7.2  4a107bc381b3… percpu_counter.h  66a5ad60566f… errno.h           e702754c45bd… util.c
v7.2  ed691b24afbc… mm_init.c         2d716cb798ea… cgroup-v2 (docs.kernel.org/7.2 rendered page)
```

(The docs page currently served for `/7.2/` and `/7.3/` is byte-identical to the committed copies, so the line
cells rest on the same rendered artefacts the ledger cites.)

## E2 — the 31 ledger rows: line cell vs my located beginning lines

`v73` = lines where the quote begins, on the freshly fetched v7.3 bytes (identical set on the committed copies);
`v72` = same on the v7.2 bytes; `moved` = the ledger cell. `OK` = ledger line ∈ v73, v73 == movement v7.3 cell,
v72 == movement v7.2 cell.

| # | h | ledger | v73 | v72 | moved | |
|---|---|---|---|---|---|---|
| 1 | 4aab78fbca9c | 121 | [121] | [121] | +0 | OK |
| 2 | c8fb3a4fb56f | 100 | [100] | [100] | +0 | OK |
| 3 | 0d09a65619e5 | 198 | [198] | [194] | +4 | OK |
| 4 | 47887dc7067f | 203 | [203] | [199] | +4 | OK |
| 5 | da4075a0131e | 208 | [208] | [204] | +4 | OK |
| 6 | 196504e1a96c | 820 | [820] | [820] | +0 | OK |
| 7 | 3b7ff65291be | 937 | [937] | [937] | +0 | OK |
| 8 | 646b97a23371 | 994 | [994] | [994] | +0 | OK |
| 9 | 07524a78c749 | 1225 | [1225] | [1194] | +31 | OK |
| 10 | 202158f50bb3 | 1437 | [1437] | [1406] | +31 | OK |
| 11 | 41496ae6cbe1 | 1409 | [1409] | [1378] | +31 | OK |
| 12 | 460b0cafc999 | 1430 | [1430, 1636] | [1399, 1605] | +31 | OK |
| 13 | 51390e34b4d7 | 1465 | [1465] | [1434] | +31 | OK |
| 14 | ed03d041e844 | 1446 | [1446] | [1415] | +31 | OK |
| 15 | fd3728bdc6d6 | 1443 | [1443] | [1412] | +31 | OK |
| 16 | 0145725d3c6c | 4997 | [4997] | [4913] | +84 | OK |
| 17 | 16a3733a5002 | 1872 | [1872] | [1827] | +45 | OK |
| 18 | 26b9666a61be | 1824 | [1824] | [1779] | +45 | OK |
| 19 | 90f96cf997c2 | 1845 | [1845] | [1800] | +45 | OK |
| 20 | a4965056de62 | 1854 | [1854] | [1809] | +45 | OK |
| 21 | adf25120cfe8 | 2041 | [2041] | [1996] | +45 | OK |
| 22 | de58513701cb | 1819 | [1819] | [1774] | +45 | OK |
| 23 | f5626c899cea | 1850 | [1850] | [1805] | +45 | OK |
| 24 | 0aa4618b2166 | 446 | [446] | [446] | +0 | OK |
| 25 | 3a75d41492ad | 945 | [945] | [945] | +0 | OK |
| 26 | 53d8f38c2827 | 1169 | [1169] | [1169] | +0 | OK |
| 27 | b962596a058b | 1030 | [1030] | [1030] | +0 | OK |
| 28 | d6bf02678216 | 424 | [424] | [424] | +0 | OK |
| 29 | e4e93c6a050c | 934 | [934] | [934] | +0 | OK |
| 30 | fdc2273230e1 | 465 | [465] | [465] | +0 | OK |
| 31 | 687e03745cd9 | 107 | [107] | [107] | +0 | OK |

30 rows have exactly one occurrence; `460b0cafc999` has two in both tags (v7.3 1430, 1636; v7.2 1399, 1605).
The ledger's per-row cell names the first one, which satisfies the counter's membership test.

Multi-line spans confirm each match is a whole statement, e.g. 4aab78fbca9c 121–125, 3b7ff65291be 937–940,
26b9666a61be 1824–1827, 0aa4618b2166 446–449, fdc2273230e1 465–468, ed03d041e844 1446–1448. Boundary characters on
both sides of all 32 matches are non-word: **0 boundary problems**, so no match begins mid-token.

Status arm only: every quote occurs in its v7.3 copy, so the ledger's 31 `held` status cells agree with
my locator (this is the status arm only; the `holds`/`changed` dispositions are the RECHECK seats' judgement and are
not mine to vote).

## E3 — the movement table, every cell

- Path column: 31/31 equals the kernel path of the row's v7.3 source row (S508 `mm/util.c`, S514 `mm/mm_init.c`,
  S515 `mm/memcontrol.c`, S516 `mm/oom_kill.c`, S517 `lib/percpu_counter.c`, S518 `include/linux/percpu_counter.h`,
  S519 `include/uapi/asm-generic/errno.h`, S520 `docs.kernel.org/<ver>/admin-guide/cgroup-v2.html`).
- v7.2 column: 31/31 set-equal to my locator on the v7.2 bytes and to the claims file's `lines` cell.
- v7.3 column: 31/31 set-equal to my locator on the v7.3 bytes (including `1430,1636`).
- `moved`: 31/31 equals the per-pair arithmetic (for the only multi-value row, `460b0cafc999`, both pairs give +31).
- Diff-based cross-check (`prose.py`): the net delta the v7.2→v7.3 diff places before each quoted v7.2 line equals
  `moved` for all 31 rows (`delta mismatches: 0`). Non-zero rows only: 194/199/204 `+4`; 4913 `+84`; the seven
  `1774…1996` rows `+45`; the seven HTML rows `+31`. Every remaining row `+0`.
- The paragraph's file-level numbers reproduce: `diff` of the committed copies prints nothing for `mm/oom_kill.c`,
  `lib/percpu_counter.c`, `include/linux/percpu_counter.h`, `include/uapi/asm-generic/errno.h` (0 changed lines,
  and the v7.3 hashes equal the v7.2 ones for oom_kill.c and errno.h); `mm/util.c` 14 changed diff lines (7 added,
  7 removed) with **no** hunk touching 820/937/994; `mm/memcontrol.c` 258 changed diff lines (204 added, 54 removed)
  with +45 / +84 before the quoted blocks; `mm/mm_init.c` 211 changed diff lines (74 added, 137 removed), +4 before
  `mm_compute_batch`; rendered page 95 changed diff lines, total length +57, +31 before the quoted block.
- Quoted lines themselves are unmodified in every pair (difflib equal blocks at each quoted v7.2 index; consistent
  with "All 31 v7.2 quotes occur verbatim").
- Release-drift paragraph corroborated: a whitespace-split word diff of the tag-stripped page yields exactly **32**
  non-equal blocks (the ledger's "32 places"); none overlaps a quoted row; the three named items are there
  (`memory.pressure`/`io.pressure` "read-only"→"read-write", `io.stat` `delay`/`microseconds`→`delay_nsec`/
  `nanoseconds`, the five CFS bandwidth stats note). No other change touches mori ground near these rows.

## E4 — row binding and the 31-row set, re-derived independently

`chain.py` (exit 0, `problems (0)`), reading every knowledge entry at `39dcf4d7`:

```
knowledge entries scanned: 63
claim|source|quote rows found at entering tip: 115
rows whose SOURCES title pins v7.2: 77 (minus 46 already in the r53 ledger -> 31)
rows pinning v7.2 only in a non-title SOURCES cell: 0
first-table-only variant: claim rows=115 pinned=77 after r53=31; same set as collect-all=True
ledger rows per entry: commit-runway-read-r53.md 8, oom-memcg-stat-r50.md 22, quota-observability-r48.md 1
```

The 31 derived hashes are exactly the 31 ledger hashes; for every row the ledger `h` equals
`sha256(ws(claim))[:12]` of the entry-table row, the ledger quote equals that row's quote, the ledger `entry`
equals the row's file, the ledger `source` equals the claims file's v7.3 source, SOURCES' copy cells for S508 and
S514–S520 equal the claims file's v7.3 paths, and SOURCES' copy cells for S481/S489–S491/S499/S511–S513 equal the
claims file's v7.2 paths. (My first `locator.py` pass printed 31 "problems" that were only my own un-stripped
backticks in the entry comparison; `chain.py` compares them correctly and reports 0.)

## E5 — HTML normalisation sensitivity (7 rows)

| h | ledger | tags→space | tags removed | raw substring occurrences |
|---|---|---|---|---|
| 07524a78c749 | 1225 | [1225] | [1225] | 0 |
| 202158f50bb3 | 1437 | [1437] | none | 0 |
| 41496ae6cbe1 | 1409 | [1409] | [1409] | 0 |
| 460b0cafc999 | 1430 | [1430,1636] | [1430,1636] | 0 |
| 51390e34b4d7 | 1465 | [1465] | none | 0 |
| ed03d041e844 | 1446 | [1446] | none | 0 |
| fd3728bdc6d6 | 1443 | [1443] | none | 0 |

Four of the seven quotes contain a raw tag boundary that must read as a space
(`<dt>anon</dt><dd><p>Amount …`, `shmem`, `kernel (npn)`, `file`). No entity occurs inside any matched region, and
no HTML quote is a raw substring of either page. The tags→space (rendered-text) convention is the correct one; the
alternative convention would report four false absences.

## Disagreements on the line arm

**None.** 31/31 ledger `line` cells, 31/31 movement v7.2 lines, 31/31 movement v7.3 lines and 31/31 `moved` values
agree with my locator on both the committed copies and freshly fetched upstream v7.2/v7.3 bytes.

## Findings

1. **MED** — `corpus/knowledge/kernel-v7.3-recheck-r54.md`, `## Where the quotes moved` paragraph (lines 57–65,
   the causal clause on line 62): the cgroup-v2 shift is attributed to "the new top-level navigation", but only 8 of
   the 31 lines before the quoted
   block are navigation captions. The other 23 are document-content additions: a 17-line note that the five CFS
   bandwidth stats are non-hierarchical, plus three net +2 replacements adding the `cgroup_set_bandwidth` /
   `cgroup_set_idle` sentences to `cpu.max`, `cpu.max.burst` and `cpu.idle` (diff opcodes before old line 1194:
   `+1×8`, `+17`, `+2,+2,+2` = 31). The +31 values are right; the cause sentence is not. No counter effect; wording
   fix only (and it slightly contradicts the entry's own drift paragraph, which correctly names the CFS note).
2. **LOW** — same file, line 63: the anchor example "(`memcontrol.c:1774-1830`, …)" exists in no cell. The entry's
   own anchors are version-labelled (`memcontrol.c.v7.2:629`, `:1549`, `:1628-1665`, `:1739-1748`); SOURCES S490's
   locate cell gives `mm/memcontrol.c:629,1546-1608,1628-1665,1693-1748,1751,1770-1784,1787-1830,1994-1999,4905-4919`;
   no cell gives 1774-1830. The substantive claim holds: at v7.3 line 1774 the text is
   `memcg_page_state(memcg, PGSCAN_KSWAPD) +`, not the quoted block, i.e. the anchors are v7.2 positions off by
   `moved`.
3. **LOW** — same paragraph, line 57: "All 31 v7.2 quotes occur verbatim in the v7.3 copies" is true only after
   whitespace collapse and, for HTML, after tag stripping with tags read as a space (0 of the 7 HTML quotes is a raw
   substring; 4 of 7 depend on the tag→space reading, see E5). A later seat re-checking the HTML rows by raw byte
   search will report seven false absences; the ledger should say "in the whitespace-collapsed (rendered) text".
4. **LOW** — `460b0cafc999` occurs twice in each tag (v7.3 1430 and 1636; v7.2 1399 and 1605). The ledger's row
   cell names 1430 only, while SOURCES S520's "quote lines" cell lists `1225, 1409, 1430, 1437, 1443, 1446, 1465`
   and omits 1636. Both are consistent with the counter's membership test (line ∈ located lines) and the movement
   table does name both v7.3 sites, so nothing is wrong; but neither cell is an exhaustive occurrence list, and a
   reader treating them as such would miss the second site.

## Limits / unverified

- I did not judge the `holds`/`changed` dispositions (RECHECK seats) or entailment; the line arm proves where each
  quote begins, not what the surrounding code means.
- No live host read was needed: this seat is source-only; no kernel log line was counted by message text.
- The "32 places" figure reproduces under my tokenisation (whitespace split after tag strip + entity decode); the
  ledger does not name a tokenizer, so exact reproduction by another seat is method-dependent.
- `count-c1.py` was read (predicate, pins, membership test) but never imported or executed; the frozen counters and
  kill rules were not questioned and no change is proposed to them.
- The docs pages are the builds served on 2026-10-27; the 7.3 tag itself (`091b06388b11`) was not re-resolved.

## Scratch

`/fast/scratch/hyaku/mori-r54/Mo54ExecLineArm/` (scripts, fetched copies, tmp) removed at the end; the tables above
are copied into this report before removal. Nothing was written outside this report and that scratch dir; no git or
jj mutation was run.
