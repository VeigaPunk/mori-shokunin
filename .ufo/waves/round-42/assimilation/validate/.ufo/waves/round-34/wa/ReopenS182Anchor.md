measured 2026-10-23T05:38:58Z

# Reopen S182 anchor — round 34 wave A (seat MoriR34A2.ReopenS182Anchor)

## Scope
The one changed cell of row S182 (corpus/SOURCES.md): the anchor gained
`485-486,512-518,620-623 (__add_disk parent, holders and slaves directories, device_add_disk)`
between f10a320d and 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3.

## Old -> new cell text (anchor column)
Diff `git -C ... diff f10a320d 8d56809... -- corpus/SOURCES.md`, hunk `@@ -185,7 +185,7 @@`:
- OLD: `block/genhd.c:1353,1371-1374,1395,1403,1418-1425 (diskstats_show, diskstats_op, proc_create_seq); tag v7.2`
- NEW: `block/genhd.c:1353,1371-1374,1395,1403,1418-1425 (diskstats_show, diskstats_op, proc_create_seq); 485-486,512-518,620-623 (__add_disk parent, holders and slaves directories, device_add_disk); tag v7.2`
All other S182 cells unchanged in this diff.

## Live fetch (two independent pulls)
- `curl -fsSL https://raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c` run twice,
  at `2026-10-23T05:38:47Z` (`date -u`, command-level output 2026-10-23T05:38:47Z); both downloads 1588 lines.
- sha256 of download 1 = sha256 of download 2 =
  `8c2faa1564190e9a8e4cf3ebac5e2561b96818e38560cdcf44fea1761c8d39a5`.

## S182.src vs live
- `sha256sum corpus/evidence/sources-r33/S182.src` =
  `8c2faa1564190e9a8e4cf3ebac5e2561b96818e38560cdcf44fea1761c8d39a5` (identical to both live pulls).
- `diff -q genhd-v7.2-1.c S182.src` exits 0: byte-identical.
=> line checks below apply to both the live v7.2 file and the local evidence copy.

## Line-by-line check of the new anchor (in live file, line numbers as fetched)
- 427: `static int __add_disk(struct device *parent, struct gendisk *disk,` — line 485-486 live inside __add_disk.
- 485: `ddev->parent = parent;` — "parent" part true.  486: `ddev->groups = groups;`.
- 512-513: `disk->part0->bd_holder_dir = kobject_create_and_add("holders", &ddev->kobj);`
- 518: `disk->slave_dir = kobject_create_and_add("slaves", &ddev->kobj);` — "holders and slaves directories" part true (512-518 also covers the -ENOMEM error paths 514-517).
- 620-621: `int __must_check device_add_disk(struct device *parent, struct gendisk *disk, const struct attribute_group **groups)`
- 622-623: `{ return add_disk_fwnode(parent, disk, groups, NULL); }` — "device_add_disk" part true (definition + body).
Cross-check: S194 (zram) uses S182's device_add_disk signature with `parent` as first argument; signature at 620 has parent first — consistent, no conflict.

## Pre-existing anchor (unchanged, sanity only)
1353 diskstats_show def; 1371-1372 zero-size partition skip; 1374 `inflight = bdev_count_inflight(hd)`; 1395 `jiffies_to_msecs(stat.io_ticks)`; 1403 `stat.sectors[STAT_DISCARD]`; 1416-1421 diskstats_op; 1425 `proc_create_seq("diskstats", ...)` — all present as claimed.

## Verdict
VERDICT: supported

## Residual risk / verification gaps
- The v7.2 tag content could in principle change upstream between fetches; two independent pulls at the same second are identical, so no drift observed at measurement time.
- I did not re-derive the counter/claim semantics; this seat only attacks the changed anchor cell. Nothing else actionable in scope.
- Tooling: no tools installed or updated (curl, git, sha256sum, date already present); no installs to record.
