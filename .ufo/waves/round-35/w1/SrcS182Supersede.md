measured 2026-10-23T08:51:50Z

# S182 append-only repair

## Finding

VERDICT: admit — the re-opened Linux v7.2 source supports the narrow additional S201 claim at the cited lines; the saved bytes hash-match the existing S182 source copy. The defect is the in-place change to S182's anchor, not unsupported source content. Evidence: `corpus/lessons/round-34-verifier-spotcheck.md:201-204` routes this as a SOURCES rule-2 form defect and asks for a supersede row; `/home/vgpnk/Projects/shokunin/CORPUS.md:116-118` permits only `status`, `recheck`, and `used-by` edits in place and requires a correction row whose teaches opens `supersedes S0NN —`.

Yes: leave S182's tip row unchanged. The closure asks for a supersede row, not a revert (`corpus/lessons/round-34-verifier-spotcheck.md:201-204`). S182's new anchor can be represented append-only by S201 without rewriting its historical row.

## S182 exact first-landed and tip rows

`git show --format= 62db24c -- corpus/SOURCES.md` added S182 in the round-33 source batch; the added row was:

```text
| S182 | Linux block/genhd.c at v7.2 (diskstats_show) — https://raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c | code | A | how v7.2 prints /proc/diskstats: zero-size partitions skipped, in-flight computed at read time, io_ticks converted from jiffies, discard sectors printed from their own counter | block/genhd.c:1371-1374,1395,1403 (diskstats_show); tag v7.2 | diskstats_show skips a partition with zero sectors, computes the in-flight count when the file is read, prints io_ticks through jiffies_to_msecs and prints discard sectors from the separate STAT_DISCARD counter. | mined | 2026-10-23 | on-release | corpus/knowledge/disk-write-rate-r33.md |
```

At lane HEAD `913df22e29f131ef9cb5de9dcb7e3e272256c5f0`, `git diff HEAD -- corpus/SOURCES.md` was empty, and `corpus/SOURCES.md:188` is the tip row:

```text
| S182 | Linux block/genhd.c at v7.2 (diskstats_show) — https://raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c | code | A | how v7.2 prints /proc/diskstats: zero-size partitions skipped, in-flight computed at read time, io_ticks converted from jiffies, discard sectors printed from their own counter | block/genhd.c:1353,1371-1374,1395,1403,1418-1425 (diskstats_show, diskstats_op, proc_create_seq); 485-486,512-518,620-623 (__add_disk parent, holders and slaves directories, device_add_disk); tag v7.2 | diskstats_show skips a partition with zero sectors, computes the in-flight count when the file is read, prints io_ticks through jiffies_to_msecs and prints discard sectors from the separate STAT_DISCARD counter. | mined | 2026-10-23 | on-release | corpus/knowledge/disk-write-rate-r33.md |
```

The exact anchor cell at first publication was `block/genhd.c:1371-1374,1395,1403 (diskstats_show); tag v7.2`; the tip anchor is the longer cell shown above. The in-place round-34 addition is isolated by `git diff 8d56809a^ 8d56809a -- corpus/SOURCES.md` and by the requested `git diff f10a320d 3a7a89ea -- corpus/SOURCES.md`: it appends `; 485-486,512-518,620-623 (__add_disk parent, holders and slaves directories, device_add_disk)` before `tag v7.2`. The round-34 lesson records the used-by change from `corpus/knowledge/disk-write-rate-r33.md` to `corpus/knowledge/disk-write-rate-r33.md; tools/mori-disk-rate.py` and its restoration at `ff334073` (`corpus/lessons/round-34.md:42-45`).

## DRAFT SOURCES S201

```text
| S201 | Linux block/genhd.c at v7.2 (__add_disk and device_add_disk) — https://raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c | code | A | v7.2 assignment of the disk device's parent and attribute groups, creation of its holders and slaves kobjects, and device_add_disk delegation | block/genhd.c:485-486,512-518,620-623 (__add_disk and device_add_disk); tag v7.2; sha256 8c2faa1564190e9a8e4cf3ebac5e2561b96818e38560cdcf44fea1761c8d39a5 | supersedes S182 — the disk device receives the supplied parent and groups; a holders kobject is created for disk->part0 and a slaves kobject for the disk under that device; device_add_disk passes parent, disk, and groups to add_disk_fwnode. | mined | 2026-10-23 | on-release | SKILL.md |
```

## DRAFT Gate S201

- URL: https://raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c
- Accessed: 2026-10-23. Reopened bytes saved at `/fast/scratch/hyaku/mori-r35/SrcS182Supersede/genhd-v7.2.c`.
- SHA-256: `8c2faa1564190e9a8e4cf3ebac5e2561b96818e38560cdcf44fea1761c8d39a5`. `timeout 10 sha256sum /fast/scratch/hyaku/mori-r35/SrcS182Supersede/genhd-v7.2.c /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r33/S182.src` printed this same digest for both paths; `timeout 10 bash -c 'cmp -s /fast/scratch/hyaku/mori-r35/SrcS182Supersede/genhd-v7.2.c /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r33/S182.src && printf "cmp=identical\\n"'` printed `cmp=identical`.
- Quotes from the reopened bytes (each is a contiguous snippet of at most 25 words, with no double quote or vertical bar):
  - `ddev->parent = parent;` — `block/genhd.c:485`.
  - `ddev->groups = groups;` — `block/genhd.c:486`.
  - `disk->part0->bd_holder_dir =` — `block/genhd.c:512`; the following call creates it with the `holders` name under `&ddev->kobj` at line 513.
  - `kobject_create_and_add(` — `block/genhd.c:513`.
  - `disk->slave_dir = kobject_create_and_add(` — `block/genhd.c:518`; its name argument is `slaves` and its parent is `&ddev->kobj`.
  - `int __must_check device_add_disk(struct device *parent, struct gendisk *disk, const struct attribute_group **groups)` — `block/genhd.c:620-621`.
  - `return add_disk_fwnode(parent, disk, groups, NULL);` — `block/genhd.c:623`.
- `VERDICT: admit` — the quoted assignments, kobject creation calls and wrapper delegation support only the proposed S201 teaches claim (`genhd-v7.2.c:485-486,512-518,620-623`).

## DRAFT lesson old→new line

Target: append to the round-35 lesson as the correction for `corpus/lessons/round-34.md:46`; do not rewrite the round-34 lesson. The routed request to correct that line is explicit at `corpus/lessons/round-34-verifier-spotcheck.md:201-204`.

```text
- Correction to round-34.md:46 (append-only): S182's anchor at the round-34 base `f10a320d` (`block/genhd.c:1353,1371-1374,1395,1403,1418-1425 (diskstats_show, diskstats_op, proc_create_seq); tag v7.2`) → at `8d56809a` / tip (`block/genhd.c:1353,1371-1374,1395,1403,1418-1425 (diskstats_show, diskstats_op, proc_create_seq); 485-486,512-518,620-623 (__add_disk parent, holders and slaves directories, device_add_disk); tag v7.2`) was edited in place, a CORPUS rule-2 form defect. Its used-by changed from `corpus/knowledge/disk-write-rate-r33.md` to `corpus/knowledge/disk-write-rate-r33.md; tools/mori-disk-rate.py` at `8d56809a`, then was restored at `ff334073` (`round-34.md:42-45`). Round 35 appends S201 with `teaches` opening `supersedes S182 —`; leave the S182 tip row unchanged.
```

## Commands, touched surfaces, and limits

- UTC measurement: `timeout 10 date -u +%FT%TZ` → `2026-10-23T08:51:50Z`.
- Reopen: `timeout 10 mkdir -p /fast/scratch/hyaku/mori-r35/SrcS182Supersede && timeout 110 bash -c 'ulimit -v 262144; exec timeout 100 curl --fail --location --silent --show-error --max-filesize 20000000 https://raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c -o /fast/scratch/hyaku/mori-r35/SrcS182Supersede/genhd-v7.2.c'`. It emitted no text; the following `sha256sum` successfully read the saved file and printed the digest above.
- Changed surfaces: this report path and the reopened scratch source only. No SOURCES row or lesson text was edited; no product code, judge, commit, push, publish, or deploy was touched.
- Out of scope / not run: no census, row-identity checker, counter, build, or test. These are not claimed as passes. No tool install or update occurred.
- Artifacts: `.ufo/waves/round-35/w1/SrcS182Supersede.md`; `/fast/scratch/hyaku/mori-r35/SrcS182Supersede/genhd-v7.2.c`; comparison source `corpus/evidence/sources-r33/S182.src`.