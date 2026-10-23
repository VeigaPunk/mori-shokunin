# w2 AttackSrc186 — attack on source row S186

Seat MoriR33.AttackSrc186 (wave 2, critic). Lane rev 62db24c01d5b7c2247f43852ea2b28d0ae5e40c8.
Question: falsify S186 (SOURCES row `corpus/SOURCES.md:192`, Gate row `corpus/lessons/round-33.md:21`,
copy `corpus/evidence/sources-r33/S186.src`). Verdict is not counted; the C1 judge runs later.

Verdict: **no blocker, no major. One minor (locator coverage for the word "bytes"). Everything else
verified clean, including live byte-stability and tag pinning.**

## F1 — minor — teaches/scope cells assert the unit word "bytes", which no Gate quote and no anchored line carries

Attacks: `corpus/SOURCES.md:192` — anchor cell `include/linux/blk_types.h:25-26,31; tag v7.2`, teaches cell
"The sector is the basic unit of block I/O; one sector is 512 = 2**9 (bytes, per the same comment) and
SECTOR_SHIFT is 9.", scope cell "the v7.2 kernel sector unit: 512 bytes, SECTOR_SHIFT 9"; against the three
Gate quotes at `corpus/lessons/round-33.md:21`.

Evidence:

- `grep -n 'bytes' corpus/evidence/sources-r33/S186.src` → `27: * bytes. Variables of type sector_t
  represent an offset or size that is a` / `28: * multiple of 512 bytes. Hence these two constants.`
  The word "bytes" occurs only on lines 27-28. Lines 25, 26 and 31 contain no "bytes"
  (`sed -n '25p;26p;31p'` output printed in full below, checks section).
- Gate quote at `S186.src:26` stops at `"The size of one sector is 512 = 2**9"` — the sentence's word
  "bytes." sits on line 27, which the anchor cell does not name (25-26, 31).
- Python containment check over the three Gate quotes: `any('bytes' in q for q in quotes)` → `False`.
  So no recorded quote states the unit word that the teaches and scope cells assert.
- The claim itself is true of the committed copy (line 27, same comment block), so this is a coverage
  gap, not a fabrication. It cannot fail P-C1-A1 (that predicate checks that the committed copy contains
  every quote and that a locator is present; it does not check SOURCES-cell support), and it does not
  touch R-J, which governs the decision-table rows. It would be called unsupported by an R-R-style
  reading ("a quote located in the committed copy ... states it").

One-line repair (either, both verified cheap): extend the anchor to `include/linux/blk_types.h:25-27,31`,
or add a fourth quote `` `S186.src:27` (13 words): "bytes. Variables of type sector_t represent an offset
or size that is a" `` — measured `words= 13 in_copy= True in_collapsed= True`.

## F2 — pointer, not a verdict — S186 cannot carry row 1's "does not follow the device's or the filesystem's own block size"

Attacks: `corpus/knowledge/disk-write-rate-r33.md:19` (row 1), the only consumer of S186
(`used-by` cell `corpus/SOURCES.md:192`). Row 1's observation cell asserts "the unit does not follow the
device's or the filesystem's own block size" and cites S187, S180, S186.

Evidence: in the committed copy, `grep -c -i -F` gives `block size` 0, `block_size` 0, `logical_block` 0,
`filesystem` 0 (`file system` 1, an unrelated phrase). S186.src states only that the basic unit of block
I/O is a sector, that one sector is 512 = 2**9 bytes, and that `sector_t` is a multiple of 512 bytes
(lines 25-28, 31).

Consequence for S186: that clause must be stated by S187 or S180 (their copies are other seats' scope, not
checked here). Row 1's own verdict belongs to the row seat; I record it because it is the only place S186
is consumed and a judge reading R-J will look at the cited set, not at S186 alone.

## Checks run that found no defect

1. Live re-open, no 429, one attempt sufficed: `curl -sSL --fail -m 60 <url> -o live.src` → `HTTP 200
   size=16897`. `sha256sum live.src` → `adff86f6d9433c496dc5ddf32d0e353a24969af7ed90191dffc562f1998b2e6e`
   = Gate sha256 (`corpus/lessons/round-33.md:21`) = `sha256sum corpus/evidence/sources-r33/S186.src`
   = `adff86f6d9433c496dc5ddf32d0e353a24969af7ed90191dffc562f1998b2e6e`. Byte-stable at measurement time.
2. Locators, one by one, from the committed copy (`sed -n '25p'`, `'26p'`, `'31p'`):
   - `:25` = ` * The basic unit of block I/O is a sector. It is used in a number of contexts` — contains
     the recorded quote; 9 words as claimed.
   - `:26` = ` * in Linux (blk, bio, genhd). The size of one sector is 512 = 2**9` — contains the
     recorded quote; 9 words as claimed.
   - `:31` = `#define SECTOR_SHIFT 9` — exact line; 3 words as claimed.
   All three quotes are also substrings of the whitespace-collapsed copy
   (`tr -s '[:space:]' ' ' < S186.src`; each tested with `grep -qF`) → CONTAINED-IN-COLLAPSED for all three.
   The truncation of the `:26` quote before "bytes" is documented in `corpus/lessons/round-33.md:152` (M3)
   as deliberate: the seat's longer draft was not contiguous in the copy.
3. Tag pin: `https://api.github.com/repos/torvalds/linux/git/ref/tags/v7.2` → HTTP 200,
   `ref: refs/tags/v7.2`, object type `tag`, sha `237a1c39e8dfd3e1c6f1f023eea37a48ec04cc63`. That tag object
   (`/git/tags/237a1c39…`) has `tag: v7.2`, tagger date `2026-08-16T21:32:26Z`, peeling to commit
   `8d3ae59288f1e7d58d76558a6ee96d533bc5019f`. Fetching the commit-pinned raw URL
   (`raw.githubusercontent.com/torvalds/linux/8d3ae592…/include/linux/blk_types.h`) → HTTP 200, 16897 B,
   sha256 `adff86f6…b2e6e`, and `cmp` against the tag-pinned bytes → identical. The pin is a real annotated
   release tag, not a mutable branch.
4. Not carried by another row: `grep -c -F <url> corpus/SOURCES.md` → 1 (only S186);
   `grep -c -F <url> corpus/lessons/round-33.md` → 1 (only the S186 Gate row, so exactly one admit Gate row);
   `grep -n 'blk_types' corpus/lessons/round-33.md` → lines 21 and 152 only;
   `git show 7d382043:corpus/SOURCES.md | grep -c -F <url>` → 0 (absent at the entering tip).
   `grep -E '^\| S1(8[0-9]|90) \|' corpus/lessons/round-33.md` sha256 column → no duplicate hashes among
   the new ids (top of `sort | uniq -c -f1 | sort -rn` all count 1).
5. kind/tier: `code` / `A` matches the source — a raw file from `torvalds/linux` (official upstream kernel
   source, SPDX header `/* SPDX-License-Identifier: GPL-2.0 */` at line 1), and it matches the lane's own
   convention for raw upstream files (S003 `code|A`, S004, S005, S006, S013, S019, S020). Gate cell 6
   `admit, A, mined` agrees with SOURCES tier A and status `mined`.
6. Worktree = committed revision for every file used here:
   `git show 62db24c0:<f> | sha256sum` equals `sha256sum <f>` for `corpus/SOURCES.md`,
   `corpus/lessons/round-33.md`, `corpus/knowledge/disk-write-rate-r33.md`,
   `corpus/evidence/sources-r33/S186.src` (all SAME).
7. Considered and not a defect: the teaches clause "SECTOR_SHIFT is 9" is stated verbatim by the `:31`
   quote, so the `#ifndef SECTOR_SHIFT` guard at line 30 (the value is a default) is not an overreach of
   the cell.

## Remaining unknowns

- Gate timestamp `2026-10-23T02:39:40Z` vs the committed copy's mtime `2026-10-22 23:51:27 -0300`
  (= `2026-10-23T02:51:27Z`): the copy was written ~12 min after the recorded open time. [INFERENCE] the
  timestamp is the fetch time and the copy was rewritten by the L1's `build_sources.py` re-location pass
  (M3); the bytes are identical now and commit-pinned, so the timestamp claim is corroborated but its
  relationship to the copy mtime is not verifiable from the tree.
- Whether any arch header overrides `SECTOR_SHIFT` in v7.2 was not checked: unauthenticated code search is
  unavailable (`https://api.github.com/search/code?q=SECTOR_SHIFT+repo:torvalds/linux` → HTTP 401
  "Requires authentication"). This does not affect F1 or any clause above.
- S187 and S180 copies were not opened (other seats' scope), so whether they carry row 1's
  device/filesystem-block-size clause is unchecked here.

## Bounds

Read-only in the lane (git `show`, `grep`, `sed`, `sha256sum`, `stat`); scratch under
`/fast/scratch/hyaku/mori-r33/AttackSrc186/` (`live.src`, `commitpin.src`, `collapsed.txt`, `tagref.json`,
`tagobj.json`, `cs.json`). No lane writes except this report. No subagents, no background jobs. No tool
installed or updated. Every network command ran under `timeout` ≤ 90 s.
