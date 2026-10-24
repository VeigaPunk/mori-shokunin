measured 2026-10-23T07:40:40Z
# ReJudgeRow3r — independent re-judgement of entry row 3r (round-34 wave B)

Rule, quoted word for word from the round-33 contract:

> A row is supported only when the quotes located in the committed copies of the sources it cites state every fact its observation and reading cells assert, and its verdict cell follows from that reading without any further fact; a row any part of which is not so stated is unsupported, including a row the judge would accept only with a caveat or through a source the row does not cite.

`judged-sha256:` = `ca489eb41140024e95641a53c7df0ae15f755a4e0a507b9f353bfec1b415f9f6` — sha256 of `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3:corpus/knowledge/disk-write-rate-r33.md`.

Row 3r is at line 76 of `corpus/knowledge/disk-write-rate-r33.md` at 8d56809. It cites `corpus/evidence/sources-r33/S182.src`, `S183.src`, `S184.src`, `S186.src` (committed copies opened via `git show 8d56809:...`).

## Observation cell — per-fact quotes or `missing`

O1 "`diskstats_show` walks `gp->part_tbl`" — PARTIAL. The walk is stated: S182.src:1370 `xa_for_each(&gp->part_tbl, idx, hd) {`. The `diskstats_show` attribution is `missing` from the cited lines: the function name occurs only at S182.src:1353 (`static int diskstats_show(struct seq_file *seqf, void *v)`) and 1420 (`.show = diskstats_show`), neither cited. An identical loop (`xa_for_each(&disk->part_tbl, …)` plus the same zero-sector skip) exists in `disk_uevent` at S182.src:348-350, so the named function is not inferable from the cited lines alone.

O2 "skips a partition with zero sectors" — STATED: S182.src:1371-1372 `if (bdev_is_partition(hd) && !bdev_nr_sectors(hd)) continue;`.

O3 "prints each remaining entry's `STAT_WRITE` sector count" — PARTIAL. The print is stated: S182.src:1391 `seq_put_decimal_ull(seqf, " ", stat.sectors[STAT_WRITE]);`, inside the loop of 1370 after the skip. The fact that this `stat` is the entry's own statistics is `missing` from the cited lines: the binding `part_stat_read_all(hd, &stat);` is at S182.src:1380, uncited. (Cited S182.src:1383 `seq_printf(seqf, " %pg", hd);` prints the entry name, not this fact.)

## Reading cell — per-fact quotes or `missing`

R1 "The disk's own `part0` is inserted into `part_tbl`" — STATED: S182.src:1465 `disk->part0 = bdev_alloc(disk, 0);` plus 1471-1472 `xa_init(&disk->part_tbl); if (xa_insert(&disk->part_tbl, 0, disk->part0, GFP_KERNEL))`.

R2 "so the whole disk has a line too" — `missing`. This requires that the skip of O2 not catch `part0`, i.e. `bdev_is_partition(part0)` is false or `bdev_nr_sectors(part0)` is nonzero. No cited line states either: `bdev_is_partition` is never defined in any of the four cited sources (only used: S182:349,1371; S183:62; S184:845,1070; S186: no hit), and `part0`'s sector count is never stated. The wa report concedes this is inference ("part0 not skipped unless zero sectors") — under the rule, a fact the judge can supply only by inference through a caveat makes the row unsupported.

R3 "`part_stat_add` adds to the partition and, for a partition, adds the same amount to `bdev_whole(part)`" — STATED: S183.src:57-58 `__this_cpu_add((part)->bd_stats->field, addnd)` and 60-64 `#define part_stat_add(part, field, addnd) do { __part_stat_add((part), field, addnd); if (bdev_is_partition(part)) __part_stat_add(bdev_whole(part), field, addnd); } while (0)`.

R4 "[`bdev_whole(part)`] is the disk's `part0`" — STATED: S186.src:84-85 `#define bdev_whole(_bdev) ((_bdev)->bd_disk->part0)`.

R5 "`bdev_end_io_acct` adds completed sectors through `part_stat_add`" — PARTIAL. STATED at S184.src:1100-1110: `void bdev_end_io_acct(struct block_device *bdev, enum req_op op, unsigned int sectors, unsigned long start_time)` … `part_stat_add(bdev, sectors[sgrp], sectors);` (line 1110). The asserted word "completed" is `missing`: no line in 1100-1110 says the sectors are completed; the word is read in from the function name or from `blk_account_io_completion` (S185), which the row does not cite.

## Verdict cell

"When totalling, count a partition's contribution once: never add a disk's line to the lines of its own partitions" follows from the *intended* reading with no further fact: R3+R4 make every partition stat add also land on `part0`; O1+O3+R1+R2 make the disk line appear beside its partitions'. However the reading cell itself contains the unstated facts above (R2, the `stat` binding, the function attribution, "completed"), so the row fails the rule's first clause before the verdict is reached. Accepting it requires exactly the caveats the rule names.

VERDICT: row 3r: unsupported

## SKILL.md:816-818 at 8d56809 under 3r

- :817 rests on row 3 ("total a host's writes over whole-disk lines or over partition lines but never both; a dm-N line repeats its backing device's writes … observed, unsourced"). Substantively holds under 3r: 3r's verdict cell is the same prohibition ("never add a disk's line to the lines of its own partitions"), and the dm-N clause rests on the unchanged Host-observation section (lines 35-45), which 3r does not disturb. Caveat: the rule's row-3 leg is now carried by a row I judge unsupported for unstated premises — the rule text is right, its sourcing incomplete.
- :816 (rows 2, 4, 13 → 13r) holds: 13r's verdict preserves "a since-boot average … never the current write rate."
- :818 (rows 5, 6, 7 → 6r, 7r) holds: 6r still says approximate busy share/never throughput; 7r still says never a percentage.

## Audit of .ufo/waves/round-34/wa/JudgeRow3r.md

- agree — `judged-sha256` ca489eb4… matches my recomputation.
- agree — blob-vs-working-tree identity of the four .src copies (I recomputed: e.g. S182 8c2faa…, S186 adff86… match its prefixes).
- agree — O2 quote S182:1371-1372 is exact and contiguous.
- agree — R1 quote S182:1471-1472 (+1465) states part0 insertion.
- agree — R2 quote S183:60-64 states the double-add.
- agree — R3 quote S186:84-85 states bdev_whole = part0.
- agree — routed-defect context: spotcheck §3.1 (:94) says "the line printing `part0` is only in S182:1370,1472, which the row does not cite"; §8 item 2 (:229-230) names S182:1370,1472 and SKILL.md:816-818, verbatim.
- agree — its residual claim (2): "the rows below supersede them" matches knowledge file :68.
- disagree — its O1 "Present": S182:1370 states a walk of `gp->part_tbl` but no cited line names `diskstats_show` (name at 1353, 1420; a parallel loop in `disk_uevent` at 348-350 shares the same skip).
- disagree — its O3 "Present": 1391 prints `stat.sectors[STAT_WRITE]`, but the `stat`↔`hd` binding (1380 `part_stat_read_all`) is uncited.
- disagree — its R4 "Present": the cited span shows `part_stat_add` of `sectors`, but "completed" appears nowhere in 1100-1110; S185 is uncited.
- disagree — its :25 "Every fact … has a contiguous located quote": false for O1's function attribution, O3's stat binding, R2's premise, R5's "completed".
- disagree — its :29 "part0 not skipped unless zero sectors": that premise is unstated in every cited line, and no cited source defines `bdev_is_partition` at all (grep S182/S183/S184/S186 → uses only, no definition).
- disagree — its :35(1) framing: a needed premise supplied by the judge's own inference is precisely the caveat case the rule marks unsupported.
- disagree — its VERDICT "supported".

AUDIT: agree 8 / disagree 7

## Residual risk / verification gaps

- No installs this run (RULES.md read; standard git/coreutils sufficed; pacman untouched).
- My judgment is stricter than the wa seat's: the deciding defect is R2's unstated `part0`-not-skipped premise, which is unquotable from the four cited sources (no `bdev_is_partition` definition in the corpus). A lenient "clause-level" reading could still find the row supported; the rule's letter as quoted does not.
- I did not re-run the C1 counter or open the L1 drafts directory; out of this seat's scope.
