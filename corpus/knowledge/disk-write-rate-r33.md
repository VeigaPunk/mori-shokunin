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

The `verdict` cell is the lane's reporting rule. It adds no fact beyond the row's reading.

| # | observation | reading | verdict | sources |
|---|---|---|---|---|
| 1 | Field 10 of a `/proc/diskstats` line, sectors written | Each unit counted there is a 512-byte sector (2**9 bytes), the kernel's basic block I/O unit; the unit does not follow the device's or the filesystem's own block size | Convert a sector delta to bytes by multiplying by 512, and never by the device's logical or physical block size | S187, S180, S186 |
| 2 | The sectors-written value grows between two readings | The kernel adds to the sector counters when an I/O completes: `bdev_end_io_acct` adds the sectors it is given with `part_stat_add`, and `blk_account_io_completion` adds completed bytes shifted right by 9 | Report the delta as completed-write throughput over the window, not as data submitted during the window | S180, S184, S185 |
| 3 | A whole-disk line next to lines for its partitions (for example nvme0n1, nvme0n1p1, nvme0n1p2) | When a partition's counter is increased through `part_stat_add`, the same amount is added again to the whole disk (`bdev_whole`), and completed sectors are added through `part_stat_add`, so the disk's sector count already holds its partitions' sectors | Total a host's writes over whole-disk lines only or over partition lines only, never over a disk together with its partitions | S183, S184 |
| 4 | A counter is lower in the newer reading than in the older one | Outside field 9 every value is cumulative and only grows, yet each one is set back at boot, when the device is reattached or reinitialised, and when the counter itself overflows | Mark that device's interval unavailable and never print a negative, wrapped or zero-filled rate for it | S181 |
| 5 | Field 12 of a `/proc/diskstats` line, I/Os currently in progress | It is the number of I/Os in progress when the file is read: `diskstats_show` sets it from `bdev_count_inflight` on every read instead of adding to a stored total | Report it as the queue depth at the moment of the read and never subtract two readings of it | S187, S182 |
| 6 | The io_ticks value of a line (iostats.rst field 10) | The kernel adds the elapsed time (`now - stamp`) to io_ticks when an I/O ends or while at least one is counted in flight, not a request count or size; iostats.rst ties its growth to field 9 being nonzero, and the stored jiffies are printed through `jiffies_to_msecs` | Report the io_ticks delta divided by the elapsed milliseconds as the share of the window with I/O in progress, and never as throughput | S184, S181, S182 |
| 7 | Field 11 of a `/proc/diskstats` line, time spent writing in milliseconds | When several requests are waiting at the same time, this tick value climbs by more than 1000 for each wall-clock second | Never present the write-ticks delta divided by elapsed time as a percentage of time | S187, S180 |
| 8 | The number of whitespace-separated values on a `/proc/diskstats` line | The ABI file describes 14 fields with sectors written as field 10; kernels 4.18 and later add four discard fields after them for 18, and kernels 5.5 and later add two flush fields after those | Accept a line of 14, 18 or 20 fields and read sectors written as field 10 in each; report missing discard or flush fields as not exported by that kernel, never as zero | S187 |
| 9 | A partition the host has, with no line of its own in `/proc/diskstats` | While printing the file the kernel passes over any partition whose size in sectors (`bdev_nr_sectors`) is zero, so such a partition has no line at all | Report a missing line as unavailable for that device, never as zero writes | S182 |
| 10 | The discard values on a line | Discards are kept in four statistics of their own, the same kinds kept for reads and writes, and the discarded sector count is printed from a separate counter (`STAT_DISCARD`) | Leave discarded sectors out of a write rate; if they are reported, report them as their own figure | S189, S182 |
| 11 | The flush values on a line | They count flushes the disk itself executed after the block layer merged flush requests, partitions do not track them, and the requests that cause flushes are mostly barriers that carry no data | Read flush counts from whole-disk lines only and never add them to sectors written | S188, S187 |
| 12 | `/sys/block/<dev>/stat` next to the same device's `/proc/diskstats` line | Both carry the same 17 statistics, and the sysfs file is exactly one line of 17 decimal numbers split by whitespace | Parse both sources with one routine over the 17 statistics, whichever file was read | S181, S180 |
| 13 | The census's since-boot average, sectors written divided by uptime | The sectors-written counter is cumulative and is set back at boot, on reattachment or reinitialisation and on overflow, so dividing it by uptime gives a mean over the counter's whole life, which may straddle a reset | Label it a since-boot average and never report it as the current write rate; a current rate needs two readings | S181 |
| 14 | iostat (sysstat 12.8.0) shows 0.0 for a device's write-sector rate | iostat names `ioi` the current and `ioj` the previous sample, and when the current sectors-written count is below the previous one it prints 0.0 instead of a rate from the two samples | Do not read an iostat zero as an idle disk without the raw counters, because a counter set back between samples also yields zero | S190, S181 |

## Host observation (round 33; evidence, not a source)

Wave-1 seat ExecHostDiskstats read this host (kernel 7.2.11-arch1-1) on 2026-10-23 between 02:39:52Z and 02:42:18Z
(`.ufo/waves/round-33/w1/ExecHostDiskstats.md`): every `/proc/diskstats` line had 20 fields (rows 8 and 12); in
three 5-second windows each whole disk's field-10 delta equalled the sum of its partitions' deltas (row 3); `dm-0`,
whose only slave is `nvme0n1p2`, moved by exactly the same field-10 delta as that slave and had the same since-boot
total, so a sum over every line would count the root filesystem's writes three times. That stacked-device double
count is observed, not sourced: no admitted source states that a device-mapper write is accounted again on the
backing device (wave-1 SrcDmCore found dm.c accounts the original bio on the dm device but does not state the second
count). It stays frontier (FR6) until a source carries it.

## What the lane's census does today, against this table

`tools/mori-census.sh` reports `io_avg_since_boot` from `/proc/diskstats` field 10 times 512 divided by integer uptime
for the device `df` resolves (wave-1 ScoutFR6Census, `tools/mori-census.sh:1879-1895,1958,1974`). Rows 1 and 13
describe it: the unit conversion is right, and the value is a lifetime mean that the census labels `since-boot`. The
census does not take two readings, so rows 2-7 and 14 apply to a future two-sample arm, which stays deferred under the
latency budget in `knowledge/surfaces-r8.md:75-89`. No census code changed in round 33.

## Limits

- Every fact rests on Linux v7.2 sources (and sysstat 12.8.0 for row 14); earlier kernels can differ, and rows 8 and 11
  name the versions the sources give.
- Per-CPU counters are summed without locks when read (iostats.rst, not quoted in a row); small mismatches between a
  disk and its partitions are possible and no row relies on exact equality.
- A rate needs two readings and an elapsed time; this entry does not set a sampling interval or a threshold.
