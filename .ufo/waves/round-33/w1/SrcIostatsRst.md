# SrcIostatsRst — source findings

## Behavior and acquisition

- Exact requested URL fetched successfully; no alternate path was needed: https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/iostats.rst
- Registry check: searched the literal URL in `corpus/SOURCES.md`; no match, so it was not already registered there.
- Exact acquisition command (both transfers succeeded on the first try):

```sh
ulimit -v 262144; mkdir -p /fast/scratch/hyaku/mori-r33/SrcIostatsRst; date -u +%FT%TZ; curl -sSL --fail -m 60 https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/iostats.rst -o /fast/scratch/hyaku/mori-r33/SrcIostatsRst/iostats.rst.first.src; sha256sum /fast/scratch/hyaku/mori-r33/SrcIostatsRst/iostats.rst.first.src; stat -c '%s bytes' /fast/scratch/hyaku/mori-r33/SrcIostatsRst/iostats.rst.first.src; date -u +%FT%TZ; curl -sSL --fail -m 60 https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/iostats.rst -o /fast/scratch/hyaku/mori-r33/SrcIostatsRst/iostats.rst.second.src; sha256sum /fast/scratch/hyaku/mori-r33/SrcIostatsRst/iostats.rst.second.src; stat -c '%s bytes' /fast/scratch/hyaku/mori-r33/SrcIostatsRst/iostats.rst.second.src; cmp -s /fast/scratch/hyaku/mori-r33/SrcIostatsRst/iostats.rst.first.src /fast/scratch/hyaku/mori-r33/SrcIostatsRst/iostats.rst.second.src && printf 'cmp: identical\n'
```

- First fetch time: `2026-10-23T02:40:16Z`; second: `2026-10-23T02:40:17Z` (the `date -u +%FT%TZ` output immediately before each curl).
- Both files are 8,592 bytes. Both `sha256sum` outputs: `166bdc8fd4ee9e53bcb86804e0d22d50c89314dcfc1a248814b0069300034124`. `cmp -s` succeeded and printed `cmp: identical`.
- Scratch copies: `/fast/scratch/hyaku/mori-r33/SrcIostatsRst/iostats.rst.first.src` and `/fast/scratch/hyaku/mori-r33/SrcIostatsRst/iostats.rst.second.src`.

## Draft SOURCES row

```text
| SRC | Linux I/O statistics fields at v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/iostats.rst | docs | A | v7.2 documentation of /proc/diskstats and sysfs stat fields, counter semantics, and historical disk-versus-partition notes | Documentation/admin-guide/iostats.rst:5-7,33-35,64-73,126-170; tag v7.2; SHA-256 166bdc8fd4ee9e53bcb86804e0d22d50c89314dcfc1a248814b0069300034124; 8,592 bytes | Linux identifies /proc/diskstats and /sys/block/<device>/stat as interfaces; field 7 is an unsigned-long count of sectors written successfully; the fields are cumulative monotonic counters except field 9, which tracks I/Os in progress and is the only field expected to return to zero; the other fields reset at boot or device reattachment. | mined | 2026-10-23 | on-release | corpus/knowledge/disk-write-rate-r33.md |
```

## Draft Gate row

```text
| SRC | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/iostats.rst | 2026-10-23T02:40:16Z | 166bdc8fd4ee9e53bcb86804e0d22d50c89314dcfc1a248814b0069300034124 | `SRC.src:5-7` (21 words): "The kernel exposes disk statistics via ``/proc/diskstats`` and ``/sys/block/<device>/stat``. These stats are usually accessed via tools such as ``sar`` and ``iostat``.", `SRC.src:33-35` (25 words): "All fields are cumulative, monotonic counters, except for field 9, which resets to zero as I/Os complete. The remaining fields reset at boot, on device reattachment", `SRC.src:64-65` (18 words): "Field 7 -- # of sectors written (unsigned long) This is the total number of sectors written successfully.", `SRC.src:71-72` (19 words): "Field 9 -- # of I/Os currently in progress (unsigned int) The only field that should go to zero." | admit, A, mined |
```

## Numbered decision facts, in plain words with separate quotes

1. The v7.2 page identifies both procfs and sysfs disk-stat interfaces.
   Quote Q1: `SRC.src:5-7` (21 words): "The kernel exposes disk statistics via ``/proc/diskstats`` and ``/sys/block/<device>/stat``. These stats are usually accessed via tools such as ``sar`` and ``iostat``."
2. Its field 7 is an unsigned-long total of successfully written sectors.
   Quote Q3: `SRC.src:64-65` (18 words): "Field 7 -- # of sectors written (unsigned long) This is the total number of sectors written successfully."
3. The page characterizes the fields as cumulative counters other than field 9, and identifies boot and device reattachment as reset conditions for the remaining fields.
   Quote Q2: `SRC.src:33-35` (25 words): "All fields are cumulative, monotonic counters, except for field 9, which resets to zero as I/Os complete. The remaining fields reset at boot, on device reattachment"
4. Field 9 represents I/Os currently in progress and is the sole field the page says should reach zero.
   Quote Q4: `SRC.src:71-72` (19 words): "Field 9 -- # of I/Os currently in progress (unsigned int) The only field that should go to zero."

## Coverage notes and facts not stated

- The document enumerates fields 1–17 in headings at `SRC.src:42-109`. Field 7 is the successful sectors-written counter; fields 12–15 describe discards and fields 16–17 describe flushes. The 4-quote Gate row above deliberately claims only the facts its quotes support; it does not reproduce the full heading list.
- Disk-versus-partition behavior is present in the source, not absent: `SRC.src:126-170` discusses differing historical disk/partition statistics, four fields available for partitions on 2.6+ machines in that account, and the full statistic set becoming available again in 2.6.25. This historical material is not one of the four drafted Gate quotes; do not treat it as a teaching claim of the drafted row without an allowed supporting quote.
- The file does not state that `unsigned long` is 32-bit or give a 32-bit wrap rule. It does mention underlying counter overflow at `SRC.src:35-37` and possible overflow while summing per-CPU values into an `unsigned long` at `SRC.src:117-121`; do not turn that into a specific width or wrap procedure.
- The file lists discard and flush fields (`SRC.src:89-109`) but does not say that discard statistics were added in 4.18 or flush statistics in 5.5.
- It explicitly says both files contain 17 statistics (`SRC.src:22-24`); it does not explain versioned 14/18/20 field counts. The example shows a `/proc/diskstats` device prefix as well as statistics (`SRC.src:11-26`), but is not a version-count account.
- It would be inaccurate to say the counters reset only at boot/device re-add: the text also names reinitialization and underlying counter overflow (`SRC.src:34-37`).
- No write-rate formula, sampling interval, sector-byte conversion, or standalone decision/reporting rule is provided in this page.

## Gates, touched surfaces, and limits

- Gates completed: exact-URL check in `corpus/SOURCES.md` returned no matches; both source fetches succeeded and were byte-identical. No counter, judge, build, lint, or tests were run.
- Touched surfaces: this report at `.ufo/waves/round-33/w1/SrcIostatsRst.md`; the two unchanged source copies at the scratch paths above. No product code, Git index, or jj state was changed.
- No tools were installed or updated. No git/jj commands or subagents were used.
- Out of scope: no C1 decision-table rows drafted; no alternate URL needed because the exact v7.2 path fetched successfully; no claim that this source alone establishes a complete disk write-rate procedure.
