# FR6 source note: Linux v7.2 block statistics

Axes: source fidelity, coverage of the requested facts, and auditability.

## Result and provenance

- URL: https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/block/stat.rst
- The exact requested tag path fetched successfully (curl exit 0); no alternate path was needed.
- First fetch/accessed: `2026-10-23T02:39:46Z`.
- Second fetch: `2026-10-23T02:39:55Z`.
- Both files are 4,315 bytes and both SHA-256 values are `4c35b795a518ceefea985f11e53b51f71d58fc99bf5a0920ca3738f13c90cb2e`; `cmp -s` returned 0 (`cmp=identical`).
- Unchanged saved copies: `/fast/scratch/hyaku/mori-r33/MoriR33.SrcStatRst/stat.rst.src` and `/fast/scratch/hyaku/mori-r33/MoriR33.SrcStatRst/stat-second.rst.src`.
- The saved source identifies itself as documentation for `/sys/block/<dev>/stat` and the file order shows the field table and explanations (saved copy lines 5, 21-23, 29-103). It is a v7.2 tag-pinned source.
- URL-uniqueness check: `grep` for the exact URL in `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md` returned `No matches found`. Existing S033 names `https://docs.kernel.org/admin-guide/iostats.html`, a different URL.
- Commands/outcomes: `mkdir -p /fast/scratch/hyaku/mori-r33/MoriR33.SrcStatRst` succeeded; first `curl -sSL --fail -m 60 https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/block/stat.rst -o /fast/scratch/hyaku/mori-r33/MoriR33.SrcStatRst/stat.rst.src` succeeded; the same curl command with `-o /fast/scratch/hyaku/mori-r33/MoriR33.SrcStatRst/stat-second.rst.src` succeeded. `sha256sum` and `wc -c` produced the identical values above; `cmp -s` succeeded. No tool was installed or updated. No test/build/lint was run.

## Draft SOURCES row

```text
| SRC | Linux block layer statistics in /sys/block/<dev>/stat, v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/block/stat.rst | docs | A | Linux v7.2 sysfs stat format and selected field semantics: sector units and completion, in_flight, io_ticks and time_in_queue | Documentation/block/stat.rst:21-23,38-39,70-73,87-89; tag v7.2; sha256 4c35b795a518ceefea985f11e53b51f71d58fc99bf5a0920ca3738f13c90cb2e | The stat file has 17 whitespace-separated decimal values and a following field summary; sector counters use standard UNIX 512-byte sectors and increment at I/O completion; in_flight counts requests issued to the driver but not completed; the field table describes io_ticks as active-device milliseconds and time_in_queue as total wait milliseconds for all requests. | mined | 2026-10-23 | on-release | corpus/knowledge/disk-write-rate-r33.md |
```

## Draft Gate row

```text
| SRC | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/block/stat.rst | 2026-10-23T02:39:46Z | 4c35b795a518ceefea985f11e53b51f71d58fc99bf5a0920ca3738f13c90cb2e | `SRC.src:21-23` (14 words): "17 decimal values separated by whitespace. The fields are summarized in the following table"; `SRC.src:72-73` (19 words): "standard UNIX 512-byte sectors, not any device- or filesystem-specific block size. The counters are incremented when the I/O completes."; `SRC.src:87-89` (21 words): "This value counts the number of I/O requests that have been issued to the device driver but have not yet completed."; `SRC.src:38-39` (18 words): "io_ticks milliseconds total time this block device has been active time_in_queue milliseconds total wait time for all requests" | admit, A, mined |
```

## Numbered facts stated by these Gate quotes

1. The stat record is one line of 17 whitespace-separated decimal values; the source says its field summary follows in a table. → Gate quote 1; saved copy lines 21-23.
2. Sector counters use the standard UNIX 512-byte sector, not a device- or filesystem-specific block size; the sector-counter passage says they increment when I/O completes. → Gate quote 2; saved copy lines 70-73.
3. `in_flight` counts requests issued to the device driver that have not completed. → Gate quote 3; saved copy lines 87-89. (The draft quote supports only this clause, not the following sentence's queued-but-not-issued exclusion.)
4. The field table labels `io_ticks` as milliseconds of device active time and `time_in_queue` as milliseconds of total wait time for all requests. → Gate quote 4; saved copy lines 38-39.

## Other requested details visible in the copy, but not established by these four Gate quotes

The table at saved copy lines 29-45 lists 17 fields in this order: read I/Os, read merges, read sectors, read ticks, write I/Os, write merges, write sectors, write ticks, in_flight, io_ticks, time_in_queue, discard I/Os, discard merges, discard sectors, discard ticks, flush I/Os, flush ticks. The draft quotes establish the 17-value format and only the named timing-field table entries; they do not quote the complete field sequence. Do not treat the complete sequence, or the unquoted discard/flush rows, as taught by this draft's Gate row.

The copy also says read/write/discard I/O counts increment on completion (line 51), flush I/O counts increment on flush completion (line 56), flushes are combined and at most one executes at a time, flush counts cover disk-executed flushes and are not tracked for partitions (lines 58-59), `io_ticks` counts time with I/O requests queued (lines 91-95), and `time_in_queue` grows with elapsed milliseconds times the number of waiting requests (lines 97-103). These were found in the saved copy, but are not in the four Gate quotations above; this draft does not claim them as quote-supported teaches.

## Not stated by this page

- The page documents `/sys/block/<dev>/stat`, not the `/proc/diskstats` record or a crosswalk between the two (saved copy lines 2, 5).
- It does not give a sampling interval, delta formula, or instruction to convert counter changes into sectors/second or bytes/second. The 512-byte unit is stated, but a rate calculation is not (lines 70-73).
- It does not describe counter reset, wraparound, reboot, or device-replacement handling.
- It does not state a general partition/whole-disk or stacked-device aggregation/deduplication rule. Its partition caveat is specifically about flush counts (lines 58-59).
- It does not claim that the counters establish write durability, successful persistence, or a device's physical media behavior.

## Scope and limits

This is one candidate source, not an FR6 decision table or a C1 verdict. The four-quote Gate draft intentionally teaches only the facts in its quoted passages; the observed full field list, discard/flush semantics, and detailed timing prose need suitable quote coverage before using those claims in a decision row. No lane files other than this report were written; no git/jj commands or other processes were run.