measured 2026-10-23T08:06:46Z

# MoriR34A3.JudgeRow3r2 — residual re-judgement of row 3r2 (round-34 attempt 3)

Rule, quoted word for word from the round-33 contract:

> A row is supported only when the quotes located in the committed copies of the sources it cites state every fact its observation and reading cells assert, and its verdict cell follows from that reading without any further fact; a row any part of which is not so stated is unsupported, including a row the judge would accept only with a caveat or through a source the row does not cite.

## Bytes judged and identity

- Snapshot: `/fast/scratch/hyaku/mori-r34/a3-L1/residual-snap/corpus_knowledge_disk-write-rate-r33.md`,
  sha256 = `7415fe52a42af52e6850822fd763e2ccc5e0965591014015e660e65e2a06f3db` (`sha256sum`, this run).
  Byte-identical to the lane working copy `corpus/knowledge/disk-write-rate-r33.md` (`diff -q`: identical; same sha256).
- Row 3r2 is the file's last line (line 98 of 98); its framing paragraph is lines 90-94.
- Sources opened: `corpus/evidence/sources-r33/S182.src`, `S183.src`, `S184.src`, `S186.src` — exactly the four the
  row cites; no fact below rests on any other file.
- Committed-copy identity: for each of the four, sha256(working tree) == sha256(`git show HEAD:<path>`):
  S182 `8c2faa15…`, S183 `2e22ee58…`, S184 `52850131…`, S186 `adff86f6…`; `git diff --stat HEAD -- corpus/evidence/sources-r33/`
  is empty. Lane HEAD `406d91a4`. Git used read-only (`show`, `diff`, `rev-parse`) only.
- All line numbers below were pinned with verbatim (`:raw`) reads of the committed copies; the S182 numbers match the
  wave-B re-judge of 3r exactly (1353, 1370-1372, 1380, 1383, 1391, 1465, 1471-1472; S183 58, 60-64; S186 84-85;
  S184 1100-1110).

## Row 3r2 under judgement (snapshot line 98, cells verbatim)

- observation: "`diskstats_show` (S182.src:1353) walks `gp->part_tbl` and skips a partition with zero sectors
  (S182.src:1370-1372); for each remaining entry it reads the statistics into `stat` (S182.src:1380) and prints
  `stat.sectors[STAT_WRITE]` (S182.src:1383,1391)"
- reading: "The disk's own `part0` is inserted into `part_tbl` (S182.src:1465,1471-1472). `part_stat_add` adds to the
  partition and, for a partition, adds the same amount to `bdev_whole(part)` (S183.src:58,61-64), which is the disk's
  `part0` (S186.src:84-85); `bdev_end_io_acct` adds its sectors through `part_stat_add` (S184.src:1100-1110)"
- verdict: "When totalling, count a partition's contribution once: never add a disk's line to the lines of its own
  partitions"
- sources: S182, S183, S184, S186

## Observation cell — per-fact contiguous located quotes

- O1 "the function doing this is `diskstats_show`" — STATED, S182.src:1353:
  `static int diskstats_show(struct seq_file *seqf, void *v)`
- O2 "walks `gp->part_tbl`" — STATED, S182.src:1370: `xa_for_each(&gp->part_tbl, idx, hd) {`
- O3 "skips a partition with zero sectors" — STATED, S182.src:1371-1372:
  `if (bdev_is_partition(hd) && !bdev_nr_sectors(hd))` / `continue;`
- O4 "for each remaining entry it reads the statistics into `stat`" — STATED, S182.src:1380:
  `part_stat_read_all(hd, &stat);` — inside the 1370 loop, after the 1371-1372 skip; "remaining entry" is the loop
  variable surviving that cited `continue`, both cited.
- O5 "prints `stat.sectors[STAT_WRITE]`" — STATED, S182.src:1391:
  `seq_put_decimal_ull(seqf, " ", stat.sectors[STAT_WRITE]);`. The row also cites 1383
  (`seq_printf(seqf, " %pg", hd);`), which prints the entry name, not this value; 1391 alone states the fact, so the
  extra locator is surplus, not an unstated assertion.

## Reading cell — per-fact contiguous located quotes

- R1 "The disk's own `part0` is inserted into `part_tbl`" — STATED, S182.src:1465
  `disk->part0 = bdev_alloc(disk, 0);` and 1471-1472 `xa_init(&disk->part_tbl);` /
  `if (xa_insert(&disk->part_tbl, 0, disk->part0, GFP_KERNEL))` — part0 allocated as the disk's own and inserted into
  the disk's `part_tbl` at index 0.
- R2 "`part_stat_add` adds to the partition and, for a partition, adds the same amount to `bdev_whole(part)`" —
  STATED, S183.src:58 `__this_cpu_add((part)->bd_stats->field, addnd)` and 61-64
  `__part_stat_add((part), field, addnd);` / `if (bdev_is_partition(part))` /
  `__part_stat_add(bdev_whole(part), field, addnd);` / `} while (0)` — the same `addnd` in both calls (61, 63).
- R3 "`bdev_whole(part)` … is the disk's `part0`" — STATED, S186.src:84-85:
  `#define bdev_whole(_bdev) \` / `((_bdev)->bd_disk->part0)`
- R4 "`bdev_end_io_acct` adds its sectors through `part_stat_add`" — STATED, S184.src:1100-1110: signature
  `void bdev_end_io_acct(struct block_device *bdev, enum req_op op,` / `unsigned int sectors, unsigned long start_time)`
  (1100-1101) and `part_stat_add(bdev, sectors[sgrp], sectors);` (1110) — the function's own `sectors` argument.

No fact in either cell is `missing`. Every quote is contiguous within one committed copy, and every fact is located
in a source the row's sources column lists (S182, S183, S184, S186); no fact needed a source the row does not cite.

## Verdict cell — does it follow with no further fact?

From the cited lines alone: (a) the printer prints each non-skipped `part_tbl` entry's own STAT_WRITE sector count
(O1-O5); (b) `part0` is an entry of `part_tbl` (R1); (c) every `part_stat_add` to a partition adds the same amount to
`bdev_whole(part)` = the disk's `part0` (R2+R3); (d) `bdev_end_io_acct` feeds its sectors through `part_stat_add` (R4).
Hence (c)+(d): whenever a partition's sectors are counted, the identical amount lands on `part0`; so any total that
adds a disk's line to its partitions' lines counts those sectors twice. The verdict — count a partition's
contribution once; never add a disk's line to its partitions' lines — is exactly that prohibition.

Whether `part0` survives the 1371-1372 skip is not stated by any cited line (no cited source defines
`bdev_is_partition`; grep over the four copies finds only uses at S182:349,1371, S183:62, S184:845,1070). That gap
does not reopen a defect: 3r2 asserts no "whole disk has a line" fact, and the prohibition holds in both branches —
if `part0` is printed, the mirror makes the disk line a double count of its partitions; if it is not, there is no
disk line to add and the instruction cannot be violated. The verdict therefore follows from the reading without any
further fact and without a caveat, so the rule's caveat clause is not triggered.

## Closure of the four wave-B defects recorded for 3r (`.ufo/waves/round-34/wb/ReJudgeRow3r.md`)

1. `diskstats_show` attribution unstated — CLOSED: now cited and verified at S182.src:1353.
2. `stat`↔entry binding unstated — CLOSED: now cited and verified at S182.src:1380 (`part_stat_read_all(hd, &stat);`).
3. "so the whole disk has a line too" unquotable — CLOSED by removal: the clause and the claim are absent from 3r2's
   cells; the verdict derivation above needs no such premise.
4. "completed" unstated in S184.src:1100-1110 — CLOSED by removal: 3r2 says "adds its sectors", exactly what
   S184.src:1110 states; the dropped word is gone from the row.

VERDICT: row 3r2: supported

## Residual risk / verification gaps

- The verdict's practical force depends on the disk line actually appearing in `/proc/diskstats`; that appearance is
  an observation of row 3 / the Host-observation section, not a fact 3r2 asserts, so it is outside this row's rule
  scope. A reader wanting the existence claim quoted must look to a future source; 3r2 itself makes no such claim.
- `bdev_is_partition` has no definition in any of the four cited copies; if a future revision re-adds a
  "the disk has a line" clause, that clause would again be unsupported without opening the defining source.
- No installs this run (RULES.md posture noted; standard coreutils/git sufficed; pacman untouched). No scratch files
  written; no background processes remain. Git in the lane was read-only (`show`, `diff --stat`, `rev-parse`).
