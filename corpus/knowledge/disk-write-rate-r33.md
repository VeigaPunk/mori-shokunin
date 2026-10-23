# Reading /proc/diskstats as a disk write rate (round 33, FR6)

source: corpus/SOURCES.md S180-S190 (Linux v7.2 tag-pinned documentation and code, two upstream commit patches, sysstat v12.8.0 iostat.c); copies at corpus/evidence/sources-r33/S###.src
verified-at: 2026-10-23 (round 33, L1 MoriR33; every copy fetched twice with identical sha256; Gate rows in corpus/lessons/round-33.md)
recheck: on-release (tag- and commit-pinned bytes; re-open when the host kernel moves past 7.2 or sysstat past 12.8.0)

Scope: detection and report only. This entry tells a reader how to turn two readings of `/proc/diskstats` (or of
`/sys/block/<dev>/stat`) into a write rate and what each value can and cannot show. It never advises writing a block
device setting, tuning a queue, or acting on a device. Field numbers follow the source each row cites: the ABI file
(S187) numbers a `/proc/diskstats` line from 1 (major) through 3 (name) and 4 onward; `iostats.rst` (S181) numbers
the statistics from 1 after the name, so its field 9 is the ABI file's field 12.

## Decision table

The `verdict` cell is the lane's reporting rule. Each verdict is meant to follow from its row's reading; the judge
receipt (`.ufo/waves/round-33/judge/JudgeC1Rows.md`) records, row by row, whether it does.

| # | observation | reading | verdict | sources |
|---|---|---|---|---|
| 1 | Field 10 of a `/proc/diskstats` line, sectors written | Each unit counted there is a 512-byte sector (2**9 bytes), the kernel's basic block I/O unit, and the procfs line and the sysfs stat file carry the same statistics; the unit does not follow the device's or the filesystem's own block size | Convert a sector delta to bytes by multiplying by 512, and never by the device's logical or physical block size | S187, S180, S186, S181 |
| 2 | The sectors-written value grows between two readings | The kernel adds to the sector counters when an I/O completes: `bdev_end_io_acct` adds the sectors it is given with `part_stat_add`, and for a request flagged `RQF_IO_STAT`, `blk_account_io_completion` adds completed bytes shifted right by 9 | Report the delta as completed-write throughput over the window, not as data submitted during the window | S180, S184, S185 |
| 3 | A whole-disk line next to lines for its own partitions | When a partition's counter is increased through `part_stat_add`, the same amount is added again to `bdev_whole(part)`, which is the disk's `part0`, and completed sectors are added through `part_stat_add`, so the disk's sector count already holds its partitions' sectors | When totalling, never add a disk's line to the lines of its own partitions | S183, S184, S186 |
| 4 | The sectors-written value is lower in the newer reading than in the older one | Outside field 9 every value is cumulative and only grows, yet each one is set back at boot, when the device is reattached or reinitialised, and when the counter itself overflows | Mark that device's write-rate interval unavailable and never print a negative or wrapped rate for it | S181 |
| 5 | Field 12 of a `/proc/diskstats` line, I/Os currently in progress | It is the count of I/Os in progress at the moment the line is printed: the printing loop assigns it from `bdev_count_inflight` for each device instead of reading a stored cumulative total | Report it as the number of I/Os in progress at the read and never subtract two readings of it | S187, S182 |
| 6 | The io_ticks counter as `/proc/diskstats` prints it | The kernel adds the elapsed time (`now - stamp`) to io_ticks when an I/O ends or while at least one is counted in flight, so it measures time rather than a request count or size; the stored jiffies are printed through `jiffies_to_msecs` | Report the io_ticks delta over the elapsed milliseconds only as an approximate busy share of the window, never as an exact share and never as throughput | S184, S182 |
| 7 | Field 11 of a `/proc/diskstats` line, time spent writing in milliseconds | When several requests are waiting at the same time, this millisecond value can climb by more than 1000 for each wall-clock second | Never present the delta of time spent writing divided by elapsed time as a percentage of time | S187, S180 |
| 8 | The number of values on a `/proc/diskstats` line | The ABI file describes 14 fields with sectors written as field 10, states that kernels 4.18 and later append four discard fields for a total of 18, and states that kernels 5.5 and later append two flush fields after those, which makes 20 | Accept a line of 14, 18 or 20 fields and read sectors written as field 10 in each; report missing discard or flush fields as not exported by that kernel, never as zero | S187 |
| 9 | A partition with no line of its own in `/proc/diskstats` | While printing the file the kernel passes over any partition whose size in sectors (`bdev_nr_sectors`) is zero, so such a partition has no line at all | Report a missing line as unavailable for that device, never as zero writes | S182 |
| 10 | The discard values on a line | Discards are kept in four statistics of their own, the same kinds kept for reads and writes, and the discarded sector count is printed from a separate counter (`STAT_DISCARD`) | Leave discarded sectors out of a write rate; if they are reported, report them as their own figure | S189, S182 |
| 11 | The flush request count on a line | It counts flush requests the disk executed, while the block layer merges several flush requests and executes no more than one at a time; partitions do not track it; requests that trigger flushes are usually zero-size barrier writes | Read flush counts from whole-disk lines only and never add them to sectors written | S188, S187 |
| 12 | `/sys/block/<dev>/stat` next to the same device's `/proc/diskstats` line | Both carry the same 17 statistics, and the sysfs file is exactly one line of 17 decimal numbers split by whitespace | Parse both sources with one routine over the 17 statistics, whichever file was read | S181, S180 |
| 13 | The census's since-boot average, sectors written divided by uptime | The sectors-written counter is cumulative from its last reset, and resets happen at boot, when the device is reattached or reinitialised, and when the counter overflows, so the counter covers the whole time since boot only when none of the later resets occurred | Label it a since-boot average that holds only if no reset happened after boot, and never report it as the current write rate | S181 |
| 14 | iostat (sysstat 12.8.0) extended statistics show a write-sector value of zero | In iostat's extended-statistics display, which takes `ioi` as the current and `ioj` as the previous sample, a current sectors-written count below the previous one sets the write-sector value to 0.0 instead of a value from the two samples | Do not read a zero write-sector value in iostat's extended statistics as an unchanged counter without the raw counters | S190 |

## Host observation (round 33; evidence, not a source)

Wave-1 seat ExecHostDiskstats read this host (kernel 7.2.11-arch1-1) on 2026-10-23 between 02:39:52Z and 02:42:18Z
(`.ufo/waves/round-33/w1/ExecHostDiskstats.md`): every `/proc/diskstats` line it read had 20 fields (rows 8 and 12);
in the three 5-second windows it took, the measured whole disk's field-10 delta equalled the sum of its partitions'
deltas (row 3); `dm-0`, whose only slave is `nvme0n1p2`, moved by the same field-10 delta as that slave in two windows
and showed the same since-boot total, so a sum over every line would have counted those sectors on `dm-0`,
`nvme0n1p2` and `nvme0n1` alike. That stacked-device equality is observed on this host, not sourced: no admitted
source states that a device-mapper write is accounted again on the backing device (wave-1 SrcDmCore found dm.c
accounts the original bio on the dm device but does not state the second count). It stays frontier (FR6) until a
source carries it.

## What the lane's census does today, against this table

`tools/mori-census.sh` reports `io_avg_since_boot` from `/proc/diskstats` field 10 times 512 divided by integer uptime
for the device `df` resolves (wave-1 ScoutFR6Census, `tools/mori-census.sh:1879-1895,1958,1974`). Rows 1 and 13
describe it: the unit conversion is right, and the value is the counter divided by host uptime, which is a since-boot
average only when no device reset happened after boot (row 13). The census does not take two readings, so rows 2-7
and 14 apply to a future two-sample arm, which stays deferred under the latency budget in
`corpus/knowledge/surfaces-r8.md:75-89`. No census code changed in round 33.

## Limits

- The kernel facts rest on Linux v7.2 sources and two upstream commit patches; row 14 rests on sysstat 12.8.0. Row 8
  repeats the version boundaries the v7.2 ABI file states; earlier kernels are not otherwise covered.
- iostats.rst says the counters are updated without locks and per-CPU values are summed when read (not quoted in a
  row); small mismatches between a disk and its partitions are possible, and no row relies on exact equality.
- A current rate is a difference of two readings over an elapsed time; the since-boot average (row 13) is a
  different quantity. This entry sets no sampling interval and no threshold.

## Round-34 revision (append-only; routed by `corpus/lessons/round-33-verifier-spotcheck.md` §8 items 2 and 3)

The round-33 closure re-judged rows 3, 6, 7 and 13 unsupported under R-J because each needs a line from a source the
row does not cite (spot-check §3.1). The rows above stay as they were judged; the rows below supersede them. Each `r`
row cites every source its cells rely on, with the located lines in the committed copies
(`corpus/evidence/sources-r33/S###.src`). Drafted by round-34 attempt-1 seats RepairRow03, RepairRow06, RepairRow07
and RepairRow13 (`.ufo/waves/round-34/w1/`), integrated by the L1 (attempt 2) and judged by a non-author seat in
round 34 wave A (`.ufo/waves/round-34/wa/`).

| # | observation | reading | verdict | sources |
|---|---|---|---|---|
| 3r | `diskstats_show` walks `gp->part_tbl`, skips a partition with zero sectors and prints each remaining entry's `STAT_WRITE` sector count (S182.src:1370-1372,1383,1391) | The disk's own `part0` is inserted into `part_tbl` (S182.src:1465,1471-1472), so the whole disk has a line too. `part_stat_add` adds to the partition and, for a partition, adds the same amount to `bdev_whole(part)` (S183.src:58,61-64), which is the disk's `part0` (S186.src:84-85); `bdev_end_io_acct` adds completed sectors through `part_stat_add` (S184.src:1100-1110) | When totalling, count a partition's contribution once: never add a disk's line to the lines of its own partitions | S182, S183, S184, S186 |
| 6r | The `io_ticks` value printed in `/proc/diskstats` | When `now` is later than `stamp` and either the I/O is ending or `bdev_count_inflight(part)` is nonzero, the kernel adds `now - stamp` to `io_ticks` (S184.src:1065-1068), and `diskstats_show` prints it through `jiffies_to_msecs` (S182.src:1353,1395). The field is milliseconds spent doing I/Os and grows while field 9 is nonzero (S181.src:75-76); since 5.0 it counts jiffies when at least one request was started or completed, and a request running more than 2 jiffies may leave some I/O time unaccounted when requests are concurrent (S181.src:78-80) | Report the `io_ticks` delta over elapsed milliseconds only as an approximate busy share of the window, never as an exact share and never as throughput | S184, S182, S181 |
| 7r | Field 11 of a `/proc/diskstats` line, time spent writing in milliseconds (S187.src:20) | `/proc/diskstats` and the sysfs stat file carry the same 17 statistics, the procfs line prefixed by major, minor and name (S181.src:22-25); the matching statistic is the total wait time for write requests (S181.src:67-68; S180.src:33-36), and when several requests wait at once these values grow faster than 1000 per second (S180.src:75-80) | Never present the delta of time spent writing divided by elapsed time as a percentage of time | S187, S181, S180 |
| 13r | Lane fact: `tools/mori-census.sh:1869-1871,1879-1894,1907-1908` labels its value an average since boot and computes field 10 (sectors written) × 512 / uptime seconds | Sectors written is a cumulative counter (S181.src:33-34,64-65); counters other than field 9 reset at boot, on device reattachment or reinitialisation, or when the underlying counter overflows, and readers should detect and handle resets when comparing snapshots (S181.src:34-37) | Call the census value a since-boot average only if none of those resets happened after boot, and never report it as the current write rate | S181; lane fact `tools/mori-census.sh` |

**Row 8 correction — discard release boundary (append-only; spot-check §8 item 3).** Row 8 repeats the ABI file's
"Kernel 4.18+ appends four more fields for discard tracking putting the total at 18" (S187.src:26-27), but the
tag-pinned printer code contradicts the 4.18 boundary: the v4.18 `diskstats_show` format has 14 conversions and its
argument list ends after `time_in_queue` (S197.src:1336-1351), while the v4.19 format has 18 conversions with four
`STAT_DISCARD` values last (S198.src:1336-1358). Read the ABI file's "4.18+" as a documentation error: v4.18 prints 14
fields and v4.19 prints 18. Row 8's parsing rule (accept 14, 18 or 20 fields; sectors written is field 10) and its
"not exported, never zero" verdict stand; this correction does not re-check the 5.5+ flush boundary. Sources S197 and
S198 were opened in round 34 (Gate: `corpus/lessons/round-34.md`).
