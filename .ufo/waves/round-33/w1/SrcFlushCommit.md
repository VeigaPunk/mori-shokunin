# SrcFlushCommit — FR6 source report

## Candidate and provenance

- Found the upstream commit by searching the exact title `block: add iostat counters for flush requests`; the search result identified commit `b6866318657717c8914673a6394894d12bc9ff5e`.
- URL opened: https://github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch
- The requested commit-patch URL returned successfully, so no v7.2 path fallback was needed.
- Registry de-duplication: searched `corpus/SOURCES.md` for the commit SHA and title before fetching; no matches were found.
- First fetch time: `2026-10-23T02:40:15Z`; bytes: `8897`; SHA-256: `a844836a15c04bfb15f44f7398851074d901afff5206509ea9be661ac5758d89`.
- Second fetch time: `2026-10-23T02:40:21Z`; bytes: `8897`; SHA-256: `a844836a15c04bfb15f44f7398851074d901afff5206509ea9be661ac5758d89`; `cmp` exit status `0`.
- Saved copies: `/fast/scratch/hyaku/mori-r33/SrcFlushCommit/flush-commit-1.src` and `/fast/scratch/hyaku/mori-r33/SrcFlushCommit/flush-commit-2.src`.

Fetch commands and observed outputs:

```sh
timeout 120 bash -c 'ulimit -v 524288; mkdir -p /fast/scratch/hyaku/mori-r33/SrcFlushCommit; date -u +%FT%TZ; curl -sSL --fail -m 60 https://github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch -o /fast/scratch/hyaku/mori-r33/SrcFlushCommit/flush-commit-1.src; sha256sum /fast/scratch/hyaku/mori-r33/SrcFlushCommit/flush-commit-1.src; wc -c /fast/scratch/hyaku/mori-r33/SrcFlushCommit/flush-commit-1.src'
# 2026-10-23T02:40:15Z
# a844836a15c04bfb15f44f7398851074d901afff5206509ea9be661ac5758d89  /fast/scratch/hyaku/mori-r33/SrcFlushCommit/flush-commit-1.src
# 8897 /fast/scratch/hyaku/mori-r33/SrcFlushCommit/flush-commit-1.src

timeout 120 bash -c 'ulimit -v 524288; date -u +%FT%TZ; curl -sSL --fail -m 60 https://github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch -o /fast/scratch/hyaku/mori-r33/SrcFlushCommit/flush-commit-2.src; sha256sum /fast/scratch/hyaku/mori-r33/SrcFlushCommit/flush-commit-2.src; wc -c /fast/scratch/hyaku/mori-r33/SrcFlushCommit/flush-commit-2.src; cmp -s /fast/scratch/hyaku/mori-r33/SrcFlushCommit/flush-commit-1.src /fast/scratch/hyaku/mori-r33/SrcFlushCommit/flush-commit-2.src; printf "cmp exit: %s\n" "$?"'
# 2026-10-23T02:40:21Z
# a844836a15c04bfb15f44f7398851074d901afff5206509ea9be661ac5758d89  /fast/scratch/hyaku/mori-r33/SrcFlushCommit/flush-commit-2.src
# 8897 /fast/scratch/hyaku/mori-r33/SrcFlushCommit/flush-commit-2.src
# cmp exit: 0
```

## Draft registry row

`SRC` is a placeholder for the lane-assigned S180+ identifier.

```text
| SRC | block: add iostat counters for flush requests — https://github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch | code | A | flush counter additions and output placement in /proc/diskstats and /sys/class/block/$dev/stat | commit patch message:13-14; block/genhd.c patch:174-181; block/partition-generic.c patch:199-206; commit b6866318657717c8914673a6394894d12bc9ff5e | The patch describes a flush-event count and total flush time in both named outputs; the added values follow the discard values. | mined | 2026-10-23 | on-release | corpus/knowledge/disk-write-rate-r33.md |
```

## Draft Gate row

```text
| SRC | https://github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch | 2026-10-23T02:40:15Z | a844836a15c04bfb15f44f7398851074d901afff5206509ea9be661ac5758d89 | `SRC.src:13-14` (20 words): "This patch adds two iostat counters into /sys/class/block/$dev/stat and /proc/diskstats - count of completed flush requests and their total time."; `SRC.src:175-181` (21 words): "part_stat_read(hd, ios[STAT_DISCARD]), part_stat_read(hd, merges[STAT_DISCARD]), part_stat_read(hd, sectors[STAT_DISCARD]), - (unsigned int)part_stat_read_msecs(hd, STAT_DISCARD) + (unsigned int)part_stat_read_msecs(hd, STAT_DISCARD), + part_stat_read(hd, ios[STAT_FLUSH]), + (unsigned int)part_stat_read_msecs(hd, STAT_FLUSH)"; `SRC.src:200-206` (23 words): "part_stat_read(p, ios[STAT_DISCARD]), part_stat_read(p, merges[STAT_DISCARD]), (unsigned long long)part_stat_read(p, sectors[STAT_DISCARD]), - (unsigned int)part_stat_read_msecs(p, STAT_DISCARD)); + (unsigned int)part_stat_read_msecs(p, STAT_DISCARD), + part_stat_read(p, ios[STAT_FLUSH]), + (unsigned int)part_stat_read_msecs(p, STAT_FLUSH));" | admit, A, mined |
```

The quote locators above refer to the first saved copy; the lane should rename `SRC.src` to the assigned source ID when committing it.

## Decision-table facts stated by the quotes

1. The commit message names both the block-class stat path and `/proc/diskstats` as outputs receiving the counters. → Q1 (`flush-commit-1.src:13-14`).
2. The two measurements are a tally of completed flush events and their accumulated duration. → Q1 (`flush-commit-1.src:13-14`).
3. In the `/proc/diskstats` formatting diff, three discard values and the discard-time value precede the newly added flush tally and flush-time value. → Q2 (`flush-commit-1.src:175-181`).
4. In the per-device stat formatting diff, the discard values likewise precede the added flush tally and flush-time value. → Q3 (`flush-commit-1.src:200-206`).

Quote key: Q1 is the commit-message excerpt at lines 13-14; Q2 and Q3 are the respective formatter diffs at lines 175-181 and 200-206. Their full quoted text and Gate locators are in the draft Gate row above.

## Not stated by this commit patch

- It does not define a write-rate formula, sampling window, or conversion from these flush measurements to write sectors or bytes. A search of the saved patch for `rate|interval|wrap|reset|write bytes|write sectors|sampling` returned no matches.
- It does not give counter wrap or reset handling. The patch describes flush accounting, not a reporting procedure for deriving an instantaneous rate.

## Gates, touched surfaces, and limits

- Duplicate-source check passed (no existing registry match); both source fetches were byte-identical. The commit patch was inspected at the cited lines; no source integration or judge outcome is claimed.
- Touched surfaces: this report; the two immutable fetched copies under the permitted seat scratch directory. No other lane file was changed.
- Not run: the C1 counter, a measurement-time re-fetch, or a judge. The assigned L1 must assign the source ID, place the committed copy and rows, and confirm measurement-time byte identity.
- No tool was installed or updated. No Git operation was run.
- Out of scope: implementing the C1 decision table, claiming a write-rate rule, or evaluating row support.
