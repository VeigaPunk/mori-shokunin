measured 2026-10-23T05:38:55Z
# JudgeRow3r — row 3r verdict (round-34 wave A)

Rule, quoted word for word from the round-33 contract (as carried in the assignment; the same clause is at `corpus/lessons/round-33-verifier-spotcheck.md:93-98` context):

> A row is supported only when the quotes located in the committed copies of the sources it cites state every fact its observation and reading cells assert, and its verdict cell follows from that reading without any further fact; a row any part of which is not so stated is unsupported, including a row the judge would accept only with a caveat or through a source the row does not cite.

`judged-sha256:` = `ca489eb41140024e95641a53c7df0ae15f755a4e0a507b9f353bfec1b415f9f6` — sha256 of `git show 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3:corpus/knowledge/disk-write-rate-r33.md`.

Row 3r (entry line 76 of the §Round-34 revision) cites S182, S183, S184, S186. All four committed copies at 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3 are byte-identical to the working-tree files read here (git-show blob sha256 == file sha256: S182 8c2faa…, S183 2e22ee…, S184 528501…, S186 adff86…).

## Observation cell facts (S182)

O1 "`diskstats_show` walks `gp->part_tbl`" — S182.src:1370: `xa_for_each(&gp->part_tbl, idx, hd) {` (the loop iterates the partition table). Present.
O2 "skips a partition with zero sectors" — S182.src:1371-1372: `if (bdev_is_partition(hd) && !bdev_nr_sectors(hd)) continue;`. Present.
O3 "prints each remaining entry's `STAT_WRITE` sector count" — S182.src:1391: `seq_put_decimal_ull(seqf, " ", stat.sectors[STAT_WRITE]);` (in the same loop body, after the skip). Present.

## Reading cell facts

R1 "The disk's own `part0` is inserted into `part_tbl`" — S182.src:1471-1472: `xa_init(&disk->part_tbl); if (xa_insert(&disk->part_tbl, 0, disk->part0, GFP_KERNEL))`. Present (also 1465 `disk->part0 = bdev_alloc(disk, 0);`).
R2 "`part_stat_add` adds to the partition and, for a partition, adds the same amount to `bdev_whole(part)`" — S183.src:60-64: `#define part_stat_add(part, field, addnd) do { \ __part_stat_add((part), field, addnd); \ if (bdev_is_partition(part)) \ __part_stat_add(bdev_whole(part), field, addnd); \ } while (0)`. Present, exact.
R3 "which is the disk's `part0`" (i.e. `bdev_whole(part)` is part0) — S186.src:84-85: `#define bdev_whole(_bdev) \ ((_bdev)->bd_disk->part0)`. Present, exact.
R4 "`bdev_end_io_acct` adds completed sectors through `part_stat_add`" — S184.src:1100-1110: `void bdev_end_io_acct(struct block_device *bdev, enum req_op op, unsigned int sectors, unsigned long start_time) { … part_stat_add(bdev, sectors[sgrp], sectors); … }` (contiguous span lines 1100-1110; the add is at 1110). Present.

Every fact in both cells has a contiguous located quote (≥6 words where the line allows) in a committed copy the row cites. No fact depends on a source the row does not cite.

## Verdict follows?

Yes. O1+O3+R1: the disk's own `part0` is an entry of `part_tbl`, so `diskstats_show` prints a line for the whole disk (zero-sector partitions skipped, part0 not skipped unless zero sectors). R2+R4: sector completions are added to the partition counter and, for a partition, again to `bdev_whole(part)` = the disk's `part0` (R3). Therefore adding a disk's line to the lines of its own partitions counts each partition's sectors twice; the verdict "count a partition's contribution once: never add a disk's line to the lines of its own partitions" follows from the reading without any further fact.

Routed-defect context: spot-check §3.1 (:94) had flagged row 3 unsupported because "the line printing `part0` is only in S182:1370,1472, which the row does not cite"; §8 item 2 (:229-230) requires citing S182:1370,1472 or narrowing the cells, in an append-only revision. Row 3r cites S182:1370-1372,1383,1391 and 1465,1471-1472, S183:58,61-64, S186:84-85, S184:1100-1110 — the routed defect is addressed.

VERDICT: row 3r: supported

Residual risk / verification gaps: (1) The reading presupposes a whole-disk `part0` has nonzero sectors so it is not skipped; that is [INFERENCE] from O2's code (skip applies only to zero-sector partitions), not a fact the row asserts, so it is not required by the rule. (2) Row 3r supersedes row 3; row 3's verdict cell is unchanged and remains as previously judged (out of scope here). (3) No tool installs were needed; no tools were installed this run.
