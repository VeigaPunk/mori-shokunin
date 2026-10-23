# FR6 source candidate: Linux block-core accounting

## Behavior and provenance

- The requested v7.2 URL succeeded; no alternate path was needed. The fetched file contains `update_io_ticks` and both `bdev_*_io_acct` functions at lines 1060–1115 of the saved copy.
- URL: https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-core.c
- First fetch/accessed: `2026-10-23T02:39:49Z`; size: `36689` bytes; SHA-256: `528501312dbd8da7649051006f12203fbef03f5180c4408ccc20856262c77827`.
- Second fetch/accessed: `2026-10-23T02:39:54Z`; size: `36689` bytes; SHA-256: `528501312dbd8da7649051006f12203fbef03f5180c4408ccc20856262c77827`. The hashes match.
- Scratch copies: `/fast/scratch/hyaku/mori-r33/SrcBlkCore/blk-core.src` and `/fast/scratch/hyaku/mori-r33/SrcBlkCore/blk-core-second.src`.
- Executed in bounded `timeout 120s bash -lc` commands: `date -u +%FT%TZ`, then `curl -sSL --fail -m 60 https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-core.c -o /fast/scratch/hyaku/mori-r33/SrcBlkCore/blk-core.src`; repeated to `blk-core-second.src`; `sha256sum` and `wc -c` on each. Both fetch commands succeeded and produced the values above.
- Duplicate check: `functions.grep` for the exact URL in `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md` returned “No matches found.”

## Draft SOURCES row

```text
| SRC | Linux v7.2 block-core accounting — https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-core.c | docs/code | A | block-device I/O time and completion accounting implementation | block/blk-core.c:1060-1115; v7.2 | update_io_ticks conditionally adds the now-minus-stamp delta to io_ticks; bdev_start_io_acct calls it with end=false and increments in-flight; bdev_end_io_acct calls it with end=true, increments ios[sgrp], adds sectors to sectors[sgrp], and adds jiffies_to_nsecs(duration) to nsecs[sgrp]. | mined | 2026-10-23 | on-release | corpus/knowledge/disk-write-rate-r33.md |
```

## Draft Gate row

```text
| SRC | https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-core.c | 2026-10-23T02:39:49Z | 528501312dbd8da7649051006f12203fbef03f5180c4408ccc20856262c77827 | `SRC.src:1065-1068` (16 words): "if (unlikely(time_after(now, stamp)) && likely(try_cmpxchg(&part->bd_stamp, &stamp, now)) && (end || bdev_count_inflight(part))) __part_stat_add(part, io_ticks, now - stamp);"; `SRC.src:1079-1084` (9 words): "part_stat_lock(); update_io_ticks(bdev, start_time, false); bdev_inc_in_flight(bdev, op); part_stat_unlock(); return start_time;"; `SRC.src:1108-1111` (11 words): "update_io_ticks(bdev, now, true); part_stat_inc(bdev, ios[sgrp]); part_stat_add(bdev, sectors[sgrp], sectors); part_stat_add(bdev, nsecs[sgrp], jiffies_to_nsecs(duration));"; `SRC.src:1103` (5 words): "const int sgrp = op_stat_group(op);" | admit, A, mined |
```

## Numbered facts and supporting quotes

1. `update_io_ticks` adds the `now - stamp` delta to `io_ticks` only after a later-time check and successful stamp compare-and-swap, and when either `end` is true or an I/O is counted in flight.
   - Quote: `SRC.src:1065-1068` (16 words): "if (unlikely(time_after(now, stamp)) && likely(try_cmpxchg(&part->bd_stamp, &stamp, now)) && (end || bdev_count_inflight(part))) __part_stat_add(part, io_ticks, now - stamp);"
2. The start function locks stats, calls the helper with `end=false`, increments in-flight for `(bdev, op)`, unlocks, and returns `start_time`.
   - Quote: `SRC.src:1079-1084` (9 words): "part_stat_lock(); update_io_ticks(bdev, start_time, false); bdev_inc_in_flight(bdev, op); part_stat_unlock(); return start_time;"
3. On completion, the function calls the helper with `end=true`, increments `ios[sgrp]`, adds the supplied `sectors` to `sectors[sgrp]`, and adds the converted duration to `nsecs[sgrp]`.
   - Quote: `SRC.src:1108-1111` (11 words): "update_io_ticks(bdev, now, true); part_stat_inc(bdev, ios[sgrp]); part_stat_add(bdev, sectors[sgrp], sectors); part_stat_add(bdev, nsecs[sgrp], jiffies_to_nsecs(duration));"
4. The completion function defines `sgrp` as `op_stat_group(op)`.
   - Quote: `SRC.src:1103` (5 words): "const int sgrp = op_stat_group(op);"

## Not stated by this source

- It does not document the `/proc/diskstats` or `/sys/block/<dev>/stat` output layout or say how these internal counters map to those files. A search of the saved file for `/proc/diskstats`, `/sys/block`, `diskstats`, `sector_size`, and `op_stat_group` returned only the `op_stat_group` use at line 1103.
- It does not define the operation-group mapping (including which group is writes), a disk write-rate formula, a sampling interval, or a sector-to-byte conversion.
- It does not state reset/wrap handling, partition or stacked-device aggregation/double-count rules, or a reporting/detection policy.
- The shorthand “io_ticks advances while at least one I/O is in flight” needs qualification: the code condition is `end || bdev_count_inflight(part)`, so an `end=true` call bypasses the explicit in-flight test. The source establishes the condition, not a broader standalone policy.
- The start body shown above calls the tick helper and increments in-flight; it does not itself add `ios`, `sectors`, or `nsecs`. The file does not express this as a prose rule.

## Gates, touched surfaces, and limits

- Created only this scoped report in the lane. Source bytes are scratch evidence at the two paths above; no product code, `corpus/SOURCES.md`, Gate/lesson file, judge, counter, or entry was changed or run. No tools were installed or updated.
- A1 applies to later decision-table reading cells: fact prose should not repeat a six-consecutive-word run from cited Gate quotes. This report is not a decision table.
- No build, test, lint, counter, or judge verification was run. The source candidate's formatting, hash, lines, and duplicate check are the observed evidence; final admission and row support remain for the integration/judge process.
- Report artifact: `.ufo/waves/round-33/w1/SrcBlkCore.md`.
