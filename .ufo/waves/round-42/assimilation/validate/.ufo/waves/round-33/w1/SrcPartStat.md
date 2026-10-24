# FR6 source: `include/linux/part_stat.h` at v7.2

## Axes and outcome
- Axes: source coverage, byte reproducibility, and claim precision.
- Exact requested v7.2 URL fetched successfully; no alternate path was needed.
- The URL did not occur in `corpus/SOURCES.md` (`grep -F` returned “No matches found”). Draft ID remains `SRC` for the L1 to assign.

## Provenance and gates
- URL: https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/part_stat.h
- Accessed: 2026-10-23T02:39:48Z (both fetch timestamps).
- Size: 2,497 bytes per fetch. SHA-256 for both: `2e22ee58e88396108d9962b122082d899fd517e3c67195e9dee580db63d55a9a`.
- `cmp -s` outcome: `identical=yes`; `curl --fail` succeeded for both.
- Scratch copies: `/fast/scratch/hyaku/mori-r33/SrcPartStat/part_stat-1.src` and `/fast/scratch/hyaku/mori-r33/SrcPartStat/part_stat-2.src`.
- Executed fetch command (two curl requests, each `-m 60`, each under `timeout 65s`):

```sh
timeout 115s bash -c 'set -eu; d=/fast/scratch/hyaku/mori-r33/SrcPartStat; mkdir -p "$d"; u=https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/part_stat.h; printf "fetch1_at="; date -u +%FT%TZ; timeout 65s curl -sSL --fail -m 60 "$u" -o "$d/part_stat-1.src"; printf "fetch1_sha256="; sha256sum "$d/part_stat-1.src"; printf "fetch1_bytes="; wc -c < "$d/part_stat-1.src"; printf "fetch2_at="; date -u +%FT%TZ; timeout 65s curl -sSL --fail -m 60 "$u" -o "$d/part_stat-2.src"; printf "fetch2_sha256="; sha256sum "$d/part_stat-2.src"; printf "fetch2_bytes="; wc -c < "$d/part_stat-2.src"; cmp -s "$d/part_stat-1.src" "$d/part_stat-2.src" && echo identical=yes'
```

- Registry uniqueness check: `grep -F 'https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/part_stat.h' /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md` → `No matches found`.
- No tool was installed or updated. No registry, Gate, lesson, product code, or git/jj state was changed.

## Draft SOURCES row

```text
| SRC | Linux include/linux/part_stat.h at v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/part_stat.h | code | A | v7.2 block-device disk_stats declarations; per-CPU part_stat_read accumulation; part-to-whole-device stat update path; not procfs formatting or counter units | include/linux/part_stat.h:8-14,34-41,60-71; tag v7.2; sha256 2e22ee58e88396108d9962b122082d899fd517e3c67195e9dee580db63d55a9a | nsecs is u64[NR_STAT_GROUPS]; sectors, ios, and merges are unsigned long[NR_STAT_GROUPS]; io_ticks is unsigned long; part_stat_read sums field values across possible CPUs; part_stat_add updates bdev_whole(part) when part is a partition; part_stat_inc delegates to part_stat_add. | mined | 2026-10-23 | on-release | corpus/knowledge/disk-write-rate-r33.md |
```

## Draft Gate row

```text
| SRC | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/part_stat.h | 2026-10-23T02:39:48Z | 2e22ee58e88396108d9962b122082d899fd517e3c67195e9dee580db63d55a9a | `SRC.src:8-13` (17 words): "struct disk_stats { u64 nsecs[NR_STAT_GROUPS]; unsigned long sectors[NR_STAT_GROUPS]; unsigned long ios[NR_STAT_GROUPS]; unsigned long merges[NR_STAT_GROUPS]; unsigned long io_ticks;"; `SRC.src:34-41` (25 words): "#define part_stat_read(part, field) \\ ({ \\ TYPEOF_UNQUAL((part)->bd_stats->field) res = 0; \\ unsigned int _cpu; \\ for_each_possible_cpu(_cpu) \\ res += per_cpu_ptr((part)->bd_stats, _cpu)->field; \\ res; \\ })"; `SRC.src:60-64` (21 words): "#define part_stat_add(part, field, addnd) do { \\ __part_stat_add((part), field, addnd); \\ if (bdev_is_partition(part)) \\ __part_stat_add(bdev_whole(part), field, addnd); \\ } while (0)"; `SRC.src:68-69` (7 words): "#define part_stat_inc(part, field) \\ part_stat_add(part, field, 1)" | admit, A, mined |
```

## Facts and quote mapping
1. `struct disk_stats` declares `nsecs` as `u64[NR_STAT_GROUPS]`; `sectors`, `ios`, and `merges` as `unsigned long[NR_STAT_GROUPS]`; and `io_ticks` as `unsigned long`. Quote Q1 (`part_stat-1.src:8-13`): “struct disk_stats { u64 nsecs[NR_STAT_GROUPS]; unsigned long sectors[NR_STAT_GROUPS]; unsigned long ios[NR_STAT_GROUPS]; unsigned long merges[NR_STAT_GROUPS]; unsigned long io_ticks;”
2. The `part_stat_read` macro initializes a result, iterates over possible CPUs, and adds that CPU's `bd_stats` field value. Quote Q2 (`part_stat-1.src:34-41`): “#define part_stat_read(part, field) \\ ({ \\ TYPEOF_UNQUAL((part)->bd_stats->field) res = 0; \\ unsigned int _cpu; \\ for_each_possible_cpu(_cpu) \\ res += per_cpu_ptr((part)->bd_stats, _cpu)->field; \\ res; \\ })”
3. `part_stat_add` adds to the supplied block device and, if it is a partition, performs the same add on `bdev_whole(part)`. Quote Q3 (`part_stat-1.src:60-64`): “#define part_stat_add(part, field, addnd) do { \\ __part_stat_add((part), field, addnd); \\ if (bdev_is_partition(part)) \\ __part_stat_add(bdev_whole(part), field, addnd); \\ } while (0)”
4. `part_stat_inc` calls `part_stat_add` with an increment of one; with Q3 this establishes the same partition-to-`bdev_whole(part)` update for increments. Quote Q4 (`part_stat-1.src:68-69`): “#define part_stat_inc(part, field) \\ part_stat_add(part, field, 1)”

## Not stated by this file
- It declares type names, but does not give a numeric width for `unsigned long` or define the `u64` typedef; do not assign portable bit widths to these fields from this file alone.
- It does not state sector units, map `STAT_READ`/`STAT_WRITE` to these fields, define write-rate arithmetic, or discuss counter reset/wrap behavior or sampling intervals.
- It does not describe `/proc/diskstats` or `/sys/block/<dev>/stat` output, name a displayed whole-disk entry `part0`, or say how `bdev_whole(part)` is exported. The supported claim here is limited to the header's update path to `bdev_whole(part)`.

## Touched surfaces and limits
- Lane file written: `.ufo/waves/round-33/w1/SrcPartStat.md` only. Source bytes were saved only in the assigned scratch directory above.
- Out of scope: editing product files, `corpus/SOURCES.md`, round-33 Gate/lesson, the counter, or any git/jj state; no judge or counter run was requested or performed.
