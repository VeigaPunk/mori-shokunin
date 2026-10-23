# SrcDmCore — round 33 wave 1

## Behavior
The requested v7.2 `drivers/md/dm.c` URL returned source bytes, so no alternate path was needed. This candidate supports the device-mapper-side accounting path and describes the target clone parameter. It does **not** by itself state that backing-device block statistics are updated again, so it does not establish the complete “same write appears on both devices” claim.

## Gates and provenance
- `grep` for the exact URL in `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md` returned **No matches found**. A second registry search for `drivers/md/dm.c|device-mapper.*account|dm_start_io_acct` also returned **No matches found**.
- Requested URL: `https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/md/dm.c` (raw v7.2 path; no fallback).
- Fetch 1: `2026-10-23T02:39:49Z`; `curl -sSL --fail -m 60` succeeded; `wc -c` reported **92806** bytes; SHA-256: `b01ff2d6285efff17e52ee7a5ca1844e3fc002f59c9c53e45bc67a40bab8b02b`.
- Fetch 2: `2026-10-23T02:39:49Z`; same `curl` options succeeded; SHA-256 matched; `cmp -s` reported **byte comparison: identical**.
- Scratch copies: `/fast/scratch/hyaku/mori-r33/SrcDmCore/dm.c.src` and `/fast/scratch/hyaku/mori-r33/SrcDmCore/dm-second.src`.
- The Gate row below is a draft with `SRC` placeholder; L1 assigns the source ID. No counter was run. No tool was installed or updated. No build, test, lint, or format check was run.

## Draft SOURCES row
```text
| SRC | Linux Device Mapper core at v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/md/dm.c | code | A | DM-side block-stat helpers for the original bio and the DM remap path's target-owned bio clone; no lower-device accounting semantics claimed | drivers/md/dm.c:508-518,1359-1363,1378-1386; tag v7.2; SHA-256 b01ff2d6285efff17e52ee7a5ca1844e3fc002f59c9c53e45bc67a40bab8b02b | The block-stat helper passes the initial bio's block-device handle to its start and completion paths; a remap comment describes accounting to the DM device for target-claimed I/O, and the second bio parameter is documented as a clone requiring submission. | mined | 2026-10-23 | on-release | corpus/knowledge/disk-write-rate-r33.md |
```

## Draft Gate row
```text
| SRC | https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/md/dm.c | 2026-10-23T02:39:49Z | b01ff2d6285efff17e52ee7a5ca1844e3fc002f59c9c53e45bc67a40bab8b02b | `SRC.src:508-518` (14 words): "struct bio *bio = io->orig_bio; if (dm_io_flagged(io, DM_IO_BLK_STAT)) { if (!end) bdev_start_io_acct(bio->bi_bdev, bio_op(bio), io->start_time); else bdev_end_io_acct(bio->bi_bdev, bio_op(bio), dm_io_sectors(io, bio), io->start_time); }"; `SRC.src:1378-1382` (22 words): "/* * Account io->origin_bio to DM dev on behalf of target * that took ownership of IO with DM_MAPIO_SUBMITTED. */ dm_start_io_acct(io, clone);"; `SRC.src:1359-1360` (10 words): "@tgt_clone: clone of @clone bio that target needs submitted" | admit, A, mined |
```

## Decision-table facts stated by the source
1. When the block-stat flag is enabled, the start helper receives the original bio's device handle, operation, and start time. (Quote Q1.)
2. The completion path sends that same handle and operation to the end helper, with sector count and the recorded start time. (Quote Q1.)
3. The remap comment assigns device-mapper accounting to a target-owned I/O; the following call invokes `dm_start_io_acct` with the I/O and clone. (Quote Q2.)
4. The API annotation describes `tgt_clone` as a clone of `clone` that the target needs to submit. (Quote Q3.)

### Quotes
- Q1 — `SRC.src:508-518` (14 words): "struct bio *bio = io->orig_bio; if (dm_io_flagged(io, DM_IO_BLK_STAT)) { if (!end) bdev_start_io_acct(bio->bi_bdev, bio_op(bio), io->start_time); else bdev_end_io_acct(bio->bi_bdev, bio_op(bio), dm_io_sectors(io, bio), io->start_time); }"
- Q2 — `SRC.src:1378-1382` (22 words): "/* * Account io->origin_bio to DM dev on behalf of target * that took ownership of IO with DM_MAPIO_SUBMITTED. */ dm_start_io_acct(io, clone);"
- Q3 — `SRC.src:1359-1360` (10 words): "@tgt_clone: clone of @clone bio that target needs submitted"

## Not stated by this file
- It does not state that the cloned bio receives a second block-stat accounting update on its backing device. The cited code submits the target clone, but the cited passages do not establish lower-device accounting.
- It does not say that one write is consequently present in both `/proc/diskstats` and `/sys/block/<dev>/stat` entries, or provide either interface's field meanings.
- It does not name runtime devices such as `dm-N`, `sdX`, or NVMe devices, nor define a write-rate calculation, detection threshold, or reporting rule.

## Touched surfaces and limits
- Repository change: this report only, `.ufo/waves/round-33/w1/SrcDmCore.md`. No product source, registry, Gate, contract, judge, or corpus file was edited.
- Scratch artifacts: the two downloaded source copies listed above. No alternate path was used and no other source was opened.
