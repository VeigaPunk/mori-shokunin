# AttackSrc183 — source row S183 (Linux `include/linux/part_stat.h` at v7.2)

Seat: MoriR33.AttackSrc183 (wave 2, attempt 1). Revision read: `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8`.
Scope: `corpus/SOURCES.md:189` (S183 row), `corpus/lessons/round-33.md:18` (Gate row), committed copy
`corpus/evidence/sources-r33/S183.src`, and the C1 row that cites it (`corpus/knowledge/disk-write-rate-r33.md:21`).
I am not the judge; this is a defect search, not a verdict.

## Verdict in one line

The row is real, live, byte-stable, tag-pinned, unique, and `code`/`A` — every provenance check passes. One **major**
defect: the Gate quote and the SOURCES anchor stop one line short of the `#define part_stat_add(...)` line, so the
quoted fragment never names the macro the row's teaches cell and C1 row 3 both talk about. One **major** defect with a
row-3 consequence: "the whole disk" is stated by no cited copy; the only committed statement of what `bdev_whole`
yields is `S186.src:84-85`, a source row 3 does not cite.

## F1 (major) — the quote and the anchor leave out the only line that names `part_stat_add`

Attacks: `corpus/lessons/round-33.md:18` (quote `S183.src:61-63`, 10 words) and `corpus/SOURCES.md:189`
(anchor `include/linux/part_stat.h:10,61-63`; teaches "part_stat_add applies an add made to a partition a second time
to the whole disk (bdev_whole)").

Evidence:
- `sed -n '57,67p' corpus/evidence/sources-r33/S183.src` shows line 57 `#define __part_stat_add(part, field, addnd) \`,
  line 60 `#define part_stat_add(part, field, addnd)	do {			\`, lines 61-63 the body the quote reproduces, line 64
  `} while (0)`.
- The quoted span, unescaped the way the counter does it, contains `__part_stat_add` twice and never `part_stat_add` as
  a distinct token (eval: `quoted span contains bare part_stat_add token: False`).
- `grep -n 'part_stat_add' S183.src` → lines 57, 60, 61, 63, 67, 69, 71; the non-underscore definition is line 60 only.

Why it matters: the teaches cell's subject is `part_stat_add`; the quote's subject is `__part_stat_add`, a different
macro. Under R-R clause 1 the teaches clause needs "a quote located in the committed copy ... [that] states it"; under
R-J the quotes must "state every fact" the cells assert. The binding of those three body lines to the name
`part_stat_add` is line 60, which neither the quote (61-63) nor the anchor (`10,61-63`) covers. C1 row 3 cites S184 as
well, and S184's quote `part_stat_add(bdev, sectors[sgrp], sectors);` does name the macro — but no cited quote says the
part_stat.h:61-63 body belongs to that macro, so the join needs an unquoted line.

Repair, tested not guessed: quote and anchor `60-64` — the wave-1 seat's own draft text
(`.ufo/waves/round-33/w1/SrcPartStat.md:32`, `SRC.src:60-64` (21 words)). Re-checked with the counter's
`unescape`+`norm`: 21 words (inside the 3-25 window, `count-c1-a1.py:226`), contained in the copy (eval:
`seat draft unescaped in copy: True`); it also keeps `do {` and `} while (0)`, so it is self-contained.

Confidence: high that the name is outside both quote and anchor; medium-high that a strict judge calls the clause
unsupported (a lenient judge reads line 60, one line above the quote, in the same committed copy, and accepts).

## F2 (major for C1 row 3, minor for the SOURCES teaches cell) — "the whole disk" is stated by no cited copy

Attacks: `corpus/SOURCES.md:189` (scope "part_stat_add on a partition also adds to the whole disk"; teaches "to the
whole disk (bdev_whole)") and `corpus/knowledge/disk-write-rate-r33.md:21` (reading "the same amount is added again to
the whole disk (`bdev_whole`) ... so the disk's sector count already holds its partitions' sectors").

Evidence:
- `grep -c 'whole disk' corpus/evidence/sources-r33/S183.src corpus/evidence/sources-r33/S184.src` →
  `S183.src:0`, `S184.src:0` — the two sources row 3 cites.
- `grep -n 'whole' S183.src` → line 63 `bdev_whole(part)` only.
- The only committed statement of what `bdev_whole` yields is `corpus/evidence/sources-r33/S186.src:84-85`:
  `#define bdev_whole(_bdev) \` / `((_bdev)->bd_disk->part0)`. S186 is an admitted row this round, but row 3's source
  cell is `S183, S184` (`disk-write-rate-r33.md:21`).
- S184's only "whole" text is the RCU-lifetime comment at `S184.src:1042-1046` ("partitions hold a reference to the
  whole device bdev and thus disk"), not the `bdev_whole` identity.
- Wave 1 warned of exactly this: `.ufo/waves/round-33/w1/SrcPartStat.md:44` — "It does not ... name a displayed
  whole-disk entry `part0`, or say how `bdev_whole(part)` is exported. The supported claim here is limited to the
  header's update path to `bdev_whole(part)`." Its draft teaches said "part_stat_add updates bdev_whole(part) when part
  is a partition" (symbol only). The committed teaches adds "the whole disk", and S183's page never says it.

Why it matters: R-J counts "through a source the row does not cite" as unsupported; R-R counts "a clause the judge
would accept only with a caveat" as unsupported. A gloss whose support sits in an uncited row is the literal case.
Note that adding S186 would not supply the words either — S186 shows `->bd_disk->part0`, not "whole disk".

Repair: state the symbol, not the gloss — "adds a second time to `bdev_whole(part)`" in the teaches cell and in
row 3's reading. If "whole disk" is wanted, cite S186 in row 3 and quote `S186.src:84-85`; that quote is 4 words
(eval: `S186 bdev_whole quote words: 4 | in copy: True`), so it can support the wording but cannot itself serve as the
>=6-word A1 span.

Confidence: high that the words are absent from every cited copy; medium that a strict judge rejects the gloss.

## F3 (minor) — the narrowing of S183's quote is not recorded in the Gate preamble

Attacks: `corpus/lessons/round-33.md:9-11` (Gate preamble).
Evidence: the preamble records one L1 quote replacement (SrcSectorSize). The S183 Gate quote narrows the seat's own
21-word `60-64` quote (`w1/SrcPartStat.md:32`) to 10 words at `61-63`, and the anchor from
`include/linux/part_stat.h:8-14,34-41,60-71` (`w1/SrcPartStat.md:26`) to `10,61-63`; neither change is recorded. The
preamble is not false (it says quotes were re-located, not that nothing else was edited), but the unrecorded narrowing
is what produced F1. Confidence: high.

## F4 (minor, operational) — the only S183 quote long enough to be a judge span is the 10-word one

Attacks: `corpus/lessons/round-33.md:18` quote list, via `count-c1-a1.py:303` (`len(span.split()) < 6` → `spans_bad`
→ `C1=unmet`).
Evidence: eval — the `61-63` quote is 10 words and located in the copy (`S183 61-63 span valid: True`); the line-10
quote is 3 words and cannot serve (`S183 line-10 span valid: False`). If the C1 judge takes row 3's span from the short
quote, the row is dropped and the predicate fails on it. This is an instruction to the judge seat, not a row defect.
Confidence: high.

## Checks run that found no defect

1. Live fetch: `curl -sSL --fail -m 60 <url> -o live.src` → `HTTP:200 SIZE:2497`; sha256
   `2e22ee58e88396108d9962b122082d899fd517e3c67195e9dee580db63d55a9a` equals the Gate sha and
   `sha256sum corpus/evidence/sources-r33/S183.src`. No 429, no retry needed.
2. Measured revision: `git show 62db24c:corpus/evidence/sources-r33/S183.src | sha256sum` → same hash;
   `git show 62db24c:corpus/SOURCES.md | grep '^| S183 '` → identical row text; the Gate row at `62db24c:18` is equal
   to the working tree; `git diff --stat 62db24c -- corpus/SOURCES.md corpus/lessons/round-33.md` → no change.
3. Locators: `sed -n '10p;61,63p'` prints exactly the quoted text (`unsigned long sectors[NR_STAT_GROUPS];` and the
   three body lines); no drift, because the copy is byte-identical to upstream.
4. Collapse containment: with the contract's own escape rule (`contract.md:58-59`) and the counter's `unescape`
   (`count-c1-a1.py:82`), both quotes are substrings of the whitespace-collapsed copy (eval `in_copy=True` twice). The
   `\\` in the Gate row is the markdown escape for one `\` and unescapes correctly; do not read it as a mismatch.
   Word counts 10 and 3 reproduce the Gate's stated counts and sit inside the 3-25 window (`count-c1-a1.py:226`).
5. URL pinning: `git ls-remote` returned no refs in 270 s (git protocol unreachable from here — unavailable, not
   absence). GitHub API instead: `GET /repos/torvalds/linux/git/ref/tags/v7.2` → HTTP 200
   `"ref": "refs/tags/v7.2"`, `"object": {"type": "tag", "sha": "237a1c39..."}`; `GET /git/ref/heads/v7.2` → HTTP 404.
   `v7.2` is an annotated tag, not a branch; the anchor's "tag v7.2" is true and the URL is tag-pinned.
6. Uniqueness and newness: `grep -c -F '<url>' corpus/SOURCES.md` → 1; `grep -n 'part_stat\.h' corpus/SOURCES.md` →
   line 189 only; `git show 7d382043:corpus/SOURCES.md | grep -c part_stat` → 0 (not registered at the entering tip).
7. kind/tier: kernel C source at an official upstream tag → `code` / `A`, matching the lane's own treatment of
   S180-S187.
8. A1 anti-shortcut on row 3: 6-word runs of row 3's reading intersected with those of the S183 and S184 Gate quotes
   → empty set (eval `A1 6-word overlap ... set()`), so the reading cell is not copied from a quote.
9. The teaches clause "the sectors array is unsigned long" is stated exactly by the quoted line 10; no overreach.
10. Status/cadence/used-by: status `mined` (counter reads cell index 7, `count-c1-a1.py:214-215`), cadence
    `on-release`, used-by names the entry that cites S183.

## Drift note

`corpus/knowledge/disk-write-rate-r33.md` changed while I read it: row 3's observation and verdict wording were
edited (`git diff --stat 62db24c -- <entry>` → 12 insertions, 12 deletions). Row 3's **reading** cell is unchanged in
both states, so F2 stands on `62db24c:21` and on the working tree. `SOURCES.md` and `lessons/round-33.md` show no
working-tree drift.

## Remaining unknowns

- Whether the C1 judge will read line 60 as "in the quote" because it is one line above it in the same committed copy.
  That single reading decides F1; the clause is the most exposed one in this row either way.
- Whether the judge treats a decision-table observation cell as a premise or as an assertion. If an assertion, row 3's
  "A whole-disk line next to lines for its partitions" needs a layout source (S182 or S187) that row 3 does not cite.
  I did not raise it as a separate finding because the entry frames observations as inputs, but it is the same class.
- Tag identity rests on the GitHub REST API only; `git ls-remote` could not reach the git endpoint from this host.

## Containment

Only this report was written in the lane. Scratch: `/fast/scratch/hyaku/mori-r33/AttackSrc183/live.src`. No tool was
installed or updated; no pacman command was run; no git or jj write in the lane or the fleet; no subagents. One
`git ls-remote` was backgrounded by the harness and returned empty; I polled nothing and signalled no process.
