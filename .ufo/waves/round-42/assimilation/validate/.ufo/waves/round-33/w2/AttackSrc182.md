# AttackSrc182 — source row S182 (`block/genhd.c` at v7.2, diskstats_show)

Scope: the S182 SOURCES row, its Gate row, its committed copy, the live URL, and the entry clauses that rest on it.
Read at lane revision 62db24c01d5b7c2247f43852ea2b28d0ae5e40c8 (working tree identical for these files).
Elements: SOURCES.md:188 (11 cells), lessons/round-33.md:17 (Gate row), corpus/evidence/sources-r33/S182.src (1588 lines,
tracked at the revision: `git cat-file -e 62db24c0:corpus/evidence/sources-r33/S182.src` → tracked-ok).

## F1 — major — the "when the file is read" / "at read time" clause is not stated by any Gate quote

Attacks:
- `corpus/SOURCES.md:188` cell 4 (scope): "in-flight computed at read time"
- `corpus/SOURCES.md:188` cell 6 (teaches): "computes the in-flight count when the file is read"
- entry `corpus/knowledge/disk-write-rate-r33.md:23` (row 5): "It is the number of I/Os in progress when the file is
  read: `diskstats_show` sets it from `bdev_count_inflight` on every read"
- entry `corpus/knowledge/disk-write-rate-r33.md:27` (row 9, S182 as its only source): "While printing the file the
  kernel passes over any partition whose size in sectors (`bdev_nr_sectors`) is zero, so such a partition has no line
  at all"

Gap. The four Gate quotes are `S182.src:1371-1372`, `1374`, `1395`, `1403`. The fact that these lines are the
`/proc/diskstats` read path — the bridge the clause needs — is stated in the committed copy only at line 1353
(`static int diskstats_show(...)`), 1420 (`diskstats_op.show = diskstats_show`) and 1425
(`proc_create_seq("diskstats", 0, NULL, &diskstats_op);`). None of 1353/1416-1425 is quoted, and none is inside the
anchor locators `block/genhd.c:1371-1374,1395,1403` (SOURCES.md:188 cell 5).

Evidence (command → output):
```
$ grep -n 'diskstats\|proc_create\|procfs' corpus/evidence/sources-r33/S182.src
1353:static int diskstats_show(struct seq_file *seqf, void *v)
1416:static const struct seq_operations diskstats_op = {
1420:	.show	= diskstats_show
1425:	proc_create_seq("diskstats", 0, NULL, &diskstats_op);
```
Line 1374 in isolation (`inflight = bdev_count_inflight(hd);`) states a call, not when the call runs. The
procfs `.show`-runs-per-read convention is an outside fact, exactly the kind R-J excludes ("a row the judge would
accept only with a caveat"). `count-c1-a1.py:40-41` fixes matching to whitespace collapse and nothing else, so the
counter cannot license a name-based bridge either.

Consequence if the judge strikes the clause: the SOURCES row loses its support under R-R, and entry rows 5 and 9 assert
the same unquoted fact, so both are exposed (row 9 cites S182 alone). C1's floor is "at least 10 rows are supported, of
which at least 8 cite a new id" (contract.md:40-41), so a two-row loss does not by itself sink C1; the exposure is the
row count, not the id count.

Cheap fix (L1's call, measured here, not applied): quotes 1 and 2 are separated only by the blank line 1373, so they
collapse to one contiguous 8-word quote `S182.src:1371-1374`
("if (bdev_is_partition(hd) && !bdev_nr_sectors(hd)) continue; inflight = bdev_count_inflight(hd);"), which frees a
slot for `S182.src:1416-1425` (the `seq_operations` initialiser plus `proc_create_seq("diskstats", ...)`), or the cells
drop "at read time" / "when the file is read" and rows 5 and 9 are reworded to "set from `bdev_count_inflight`" only.

## F2 — minor — "separate" / "their own" counter

Attacks SOURCES.md:188 cell 6 ("from the separate STAT_DISCARD counter"), cell 4 ("from their own counter"), and entry
row 10 (disk-write-rate-r33.md:28). Quote 4 shows only the discard index (`stat.sectors[STAT_DISCARD]`, S182.src:1403);
the write-sectors counter the word "separate" contrasts with is at S182.src:1391, which is neither quoted nor in the
anchor locators. The index name `STAT_DISCARD` against `STAT_WRITE` carries "separate" well enough that a literal judge
will very likely accept it — logged only so the wording can be tightened if the clause is rewritten for F1.

## No defect found — checks run

1. Live re-open: `curl -sSL --fail -m 60 https://raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c` → HTTP 200,
   41823 bytes; sha256 `8c2faa1564190e9a8e4cf3ebac5e2561b96818e38560cdcf44fea1761c8d39a5`, equal to the Gate sha256
   (round-33.md:17) and to `sha256sum corpus/evidence/sources-r33/S182.src`; `cmp` of the two files → identical
   (`cmp live.src S182.src` → no output, exit 0; no retry needed, no 429 seen). Wave-1
   `.ufo/waves/round-33/w1/SrcGenhd.md` records two
   independent fetches, each 41823 bytes at the same hash.
2. Quote containment (own script, `/fast/scratch/hyaku/mori-r33/AttackSrc182/qcheck.py`): each of the four quotes, after
   the documented `\"`→`"` unescape (`count-c1-a1.py:41`, `contract.md:57-59`) and whitespace-run collapse, is present
   in the committed copy and inside its stated locator lines. Printed result, one line per quote:
   `1371-1372 words=5 in_copy_unescaped=True in_stated_lines=True`; `1374 words=3 True True`;
   `1395 words=4 True True`; `1403 words=4 True True`. Byte-literal containment fails only for quotes 3 and 4, because
   of the escaped `\" \"` separators the Gate syntax defines — not a defect.
3. Word counts 5/3/4/4 match the Gate annotations and lie inside 3-25 (contract.md:29); 4 quotes ≤ 4.
4. Quote 1 spans 1371→1372 with only tabs/newline between, so it is contiguous under the counter's norm; the
   round-33 preamble's displaced-quote rule (round-33.md:7-9) is respected.
5. Anchor sanity: 1371-1374, 1395 and 1403 all sit inside `diskstats_show` (1353-1414 in the copy); the anchor's
   `(diskstats_show)` and `tag v7.2` are both true of the copy and the URL path.
6. URL pinning and uniqueness: the path is `/v7.2/...` (tag-pinned, not `master`/`linux-next`);
   `grep -n -F '<url>' corpus/SOURCES.md` → line 188 only; `git show 7d382043:corpus/SOURCES.md | grep -n -F
   'block/genhd.c'` → exit 1 (absent at the entering tip); `grep -c -F '<url>' corpus/lessons/round-33.md` → 1 (one
   admit row); `grep -n 'genhd' corpus/SOURCES.md` → no other row cites the file in any other form.
7. Row shape: `grep -c '^| S182 ' corpus/SOURCES.md` → 1, and the row splits into 11 cells over the 11 header columns
   (id, source, kind, tier, scope, anchor, teaches, status, opened, recheck, used-by). Gate decision "admit, A, mined"
   agrees with `status: mined`; `opened 2026-10-23` agrees with the Gate access date `2026-10-23T02:39:43Z`.
8. Cross-row sha distinctness: the 11 new ids S180-S190 carry 11 distinct sha256 values (`uniq -c` → 11 rows × 1);
   S182's URL is not a substring of any other new id's source cell.
9. kind/tier: `code` and `A` are right — the file is upstream kernel source from `torvalds/linux` at tag v7.2.
10. `recheck: on-release` is in-vocabulary (150 rows carry it, including S180 and S181).

## Remaining unknowns

- The reading of R-J's "the quotes located in the committed copies": if the judge admits any quote locatable in the copy
  (not only the four Gate quotes), F1 weakens to minor, because 1420/1425 do state the binding. I record the strict
  reading as the risk; the wording fix costs nothing under either reading.
- The tag-to-tree mapping (`v7.2` → this blob) was confirmed only through raw.githubusercontent.com; a second fetch from
  git.kernel.org cgit was not made (not required by the brief).

## Tools

None installed or updated: the checks used the host `curl` and `python3` already present; no pacman, no network install.

Scratch kept under `/fast/scratch/hyaku/mori-r33/AttackSrc182/` (`live.src`, `qcheck.py`). No lane file other than this
report was written; no git or jj write was run in the lane or the fleet repo.
