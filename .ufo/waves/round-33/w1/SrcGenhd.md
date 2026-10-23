# Round 33 — FR6 source findings: `block/genhd.c`

## Behavior and result

- Axis/scope: depth, FR6 disk-write-rate source evidence for C1.
- The requested v7.2 URL exists and fetched successfully; no alternate path was needed.
- Drafted one SOURCES row and one Gate row below, using placeholder `SRC` for the L1-assigned ID.
- The URL check against `corpus/SOURCES.md` returned “No matches found”; it was not already registered at the time checked.
- No counter, tests, or product-code changes were run or made. No tools were installed or updated.

## Acquisition and provenance

URL: `https://raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c`

Both fetches reported `2026-10-23T02:39:43Z`; each saved file is 41,823 bytes and has SHA-256 `8c2faa1564190e9a8e4cf3ebac5e2561b96818e38560cdcf44fea1761c8d39a5`.

Scratch copies:
- `/fast/scratch/hyaku/mori-r33/SrcGenhd/genhd-1.src`
- `/fast/scratch/hyaku/mori-r33/SrcGenhd/genhd-2.src`

Commands executed (the two fetches were launched in parallel):

```sh
ulimit -v 2097152; timeout 120s bash -c 'set -eu; mkdir -p /fast/scratch/hyaku/mori-r33/SrcGenhd; date -u +%FT%TZ; curl -sSL --fail -m 60 https://raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c -o /fast/scratch/hyaku/mori-r33/SrcGenhd/genhd-1.src; wc -c /fast/scratch/hyaku/mori-r33/SrcGenhd/genhd-1.src; sha256sum /fast/scratch/hyaku/mori-r33/SrcGenhd/genhd-1.src'
ulimit -v 2097152; timeout 120s bash -c 'set -eu; mkdir -p /fast/scratch/hyaku/mori-r33/SrcGenhd; date -u +%FT%TZ; curl -sSL --fail -m 60 https://raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c -o /fast/scratch/hyaku/mori-r33/SrcGenhd/genhd-2.src; wc -c /fast/scratch/hyaku/mori-r33/SrcGenhd/genhd-2.src; sha256sum /fast/scratch/hyaku/mori-r33/SrcGenhd/genhd-2.src'
timeout 120s sha256sum /fast/scratch/hyaku/mori-r33/SrcGenhd/genhd-1.src /fast/scratch/hyaku/mori-r33/SrcGenhd/genhd-2.src
```

Each fetch command printed the timestamp above, `41823` bytes, and the same hash above. The explicit hash confirmation printed that hash for both paths. The URL search was for the exact raw URL in `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`; result: `No matches found`.

## Draft rows

SOURCES row (11 cells; ID remains for L1):

```text
| SRC | Linux block/genhd.c at v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c | code | A | diskstats_show output and partition iteration; part_stat_show sysfs stat formatting | block/genhd.c:1058-1100, 1353-1410; tag v7.2 | diskstats_show omits zero-sector partitions, reads in-flight via bdev_count_inflight, emits write I/O, merges, sectors and a converted write-time value, and converts io_ticks with jiffies_to_msecs; the sysfs stat format includes %8lu, %8llu and %8u. | mined | 2026-10-23 | on-release | corpus/knowledge/disk-write-rate-r33.md |
```

Gate row (four quotes; locators use the required literal `SRC.src` placeholder):

```text
| SRC | https://raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c | 2026-10-23T02:39:43Z | 8c2faa1564190e9a8e4cf3ebac5e2561b96818e38560cdcf44fea1761c8d39a5 | `SRC.src:1371-1378` (16 words): "if (bdev_is_partition(hd) && !bdev_nr_sectors(hd)) continue; inflight = bdev_count_inflight(hd); if (inflight) { part_stat_lock(); update_io_ticks(hd, jiffies, true); part_stat_unlock();"; `SRC.src:1389-1393` (21 words): "seq_put_decimal_ull(seqf, \" \", stat.ios[STAT_WRITE]); seq_put_decimal_ull(seqf, \" \", stat.merges[STAT_WRITE]); seq_put_decimal_ull(seqf, \" \", stat.sectors[STAT_WRITE]); seq_put_decimal_ull(seqf, \" \", (unsigned int)div_u64(stat.nsecs[STAT_WRITE], NSEC_PER_MSEC));"; `SRC.src:1395` (5 words): "seq_put_decimal_ull(seqf, \" \", jiffies_to_msecs(stat.io_ticks));"; `SRC.src:1073-1077` (17 words): "\"%8lu %8lu %8llu %8u \" \"%8lu %8lu %8llu %8u \" \"%8u %8u %8u \" \"%8lu %8lu %8llu %8u \" \"%8lu %8u\"" | admit, A, mined |
```

## Numbered facts and quoted support

1. `diskstats_show` iterates `gp->part_tbl`; its explicit per-entry skip is a partition with zero sectors. It reads the in-flight value with `bdev_count_inflight(hd)` and, when nonzero, locks stats and calls `update_io_ticks(hd, jiffies, true)`. Quote: `SRC.src:1371-1378` above; code context `genhd-1.src:1369-1380`.
2. The exact `/proc/diskstats` output order in this function is: major, minor, `%pg` device name; READ I/Os, merges, sectors, milliseconds; WRITE I/Os, merges, sectors, milliseconds; in-flight; `io_ticks` milliseconds; combined READ+WRITE+DISCARD+FLUSH nanoseconds converted to milliseconds; DISCARD I/Os, merges, sectors, milliseconds; FLUSH I/Os, milliseconds. Evidence is the ordered calls at `genhd-1.src:1381-1409`. The quoted WRITE portion at `SRC.src:1389-1393` directly shows write I/Os, merges, sectors, then `nsecs[STAT_WRITE]` divided by `NSEC_PER_MSEC` and cast to `unsigned int`; `SRC.src:1395` shows `jiffies_to_msecs(stat.io_ticks)`.
3. In `/proc/diskstats`, numeric output uses `seq_put_decimal_ull` (and the major/minor width variant); the device name uses `%pg`. `inflight` is declared `unsigned int` at `genhd-1.src:1355-1359`. Time expressions are explicitly cast to `unsigned int` where shown, while the source does not define the underlying C types of every `disk_stats` member in this file. Locators: `genhd-1.src:1353-1359,1381-1408`; quotes 2-3 above.
4. `part_stat_show` is the sysfs `stat` emitter: the `stat` attribute is bound to it at `genhd-1.src:1167`. Its format slots, in order, are `lu, lu, llu, u; lu, lu, llu, u; u, u, u; lu, lu, llu, u; lu, u` (with width 8), corresponding in the argument list to READ, WRITE, in-flight/io-time/combined time, DISCARD, and FLUSH groups. The format string is quoted at `SRC.src:1073-1077`; argument order and casts are at `genhd-1.src:1079-1099`.
5. The source performs conversions, not a rate calculation: write-time nanoseconds are divided by `NSEC_PER_MSEC`, while `io_ticks` goes through `jiffies_to_msecs`. Relevant quotes: `SRC.src:1389-1393` and `SRC.src:1395`; combined timing expression is at `genhd-1.src:1396-1400`.

The four Gate quotes are limited excerpts, not a quotation of every field in fact 2 or the full argument mapping in fact 4. Those complete sequences are reported with their exact saved-file locators above; do not treat the abbreviated Gate quotes as proof of omitted field clauses under R-J.

## Not stated by this file

- The explicit `diskstats_show` partition skip is zero sector count. This file does not establish that hidden disks are excluded: `diskstats_show` has no `GENHD_FL_HIDDEN` predicate, and the iterator setup at `genhd-1.src:907-925` does not test that flag. Do not claim hidden disks are either omitted or included without evidence about the class iterator and device registration.
- The meaning or implementation of `bdev_count_inflight`, the units of `stat.sectors[]`, a sampling interval, a write-rate formula, counter reset/wrap behavior, and partition/whole-disk or stacked-device double-counting are not stated here.
- The file calls `seq_put_decimal_ull`; it does not define that helper or declare the member types of the `struct disk_stats` fields in this file. Do not turn those call names or types into unsupported semantic claims.

## Gates, touched surfaces, and limits

- Gates exercised: exact-URL duplicate search (no match); both `curl --fail` fetches succeeded; byte counts and SHA-256s matched. Exact requested path was present, so no path search/fallback was needed.
- Touched surfaces: this report only in the lane; two unchanged source copies under the assigned scratch directory. No SOURCES, Gate, entry, counter, or product file was edited.
- Out of scope: no lane Git/jj writes, counter invocation, tests, tools installation, or claims about facts absent from this source.
- Report artifact: `.ufo/waves/round-33/w1/SrcGenhd.md`.
