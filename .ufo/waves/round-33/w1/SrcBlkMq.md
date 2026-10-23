# FR6 C1 source candidate: Linux blk-mq accounting

## Axes
- Correctness: quote only statements present in the pinned v7.2 source.
- Provenance: preserve both fetched copies and compare their hashes.
- Containment: write only this report in the lane; keep source bytes in seat scratch.

## Findings and provenance
- Candidate URL: `https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-mq.c`. The exact path fetched successfully; no alternate path was needed.
- Registry lookup: the `grep` tool searched `corpus/SOURCES.md` for `https://raw\.githubusercontent\.com/torvalds/linux/v7\.2/block/blk-mq\.c`; outcome: “No matches found.” It is new relative to the checked registry.
- Accessed at both fetches: `2026-10-23T02:39:58Z`.
- Copy 1: `/fast/scratch/hyaku/mori-r33/MoriR33.SrcBlkMq/blk-mq-1.src`; 136,798 bytes; SHA-256 `7483f1738ad1a00372f5fca0e553023ff4a683e4e2a73c01b3da31302bba8c11`.
- Copy 2: `/fast/scratch/hyaku/mori-r33/MoriR33.SrcBlkMq/blk-mq-2.src`; 136,798 bytes; SHA-256 `7483f1738ad1a00372f5fca0e553023ff4a683e4e2a73c01b3da31302bba8c11`. Hashes match.
- Fetch command 1 (one successful curl attempt; command allowed up to three):

```sh
timeout 120 sh -c 'ulimit -v 524288; set -e; printf "accessed="; date -u +%FT%TZ; curl -sSL --fail -m 60 https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-mq.c -o /fast/scratch/hyaku/mori-r33/MoriR33.SrcBlkMq/blk-mq-1.src || curl -sSL --fail -m 60 https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-mq.c -o /fast/scratch/hyaku/mori-r33/MoriR33.SrcBlkMq/blk-mq-1.src || curl -sSL --fail -m 60 https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-mq.c -o /fast/scratch/hyaku/mori-r33/MoriR33.SrcBlkMq/blk-mq-1.src; printf "sha256="; sha256sum /fast/scratch/hyaku/mori-r33/MoriR33.SrcBlkMq/blk-mq-1.src; printf "bytes="; wc -c < /fast/scratch/hyaku/mori-r33/MoriR33.SrcBlkMq/blk-mq-1.src'
```

  Output: `accessed=2026-10-23T02:39:58Z`; SHA-256 and bytes as listed above.
- Fetch command 2:

```sh
timeout 120 sh -c 'ulimit -v 524288; set -e; printf "accessed="; date -u +%FT%TZ; curl -sSL --fail -m 60 https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-mq.c -o /fast/scratch/hyaku/mori-r33/MoriR33.SrcBlkMq/blk-mq-2.src || curl -sSL --fail -m 60 https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-mq.c -o /fast/scratch/hyaku/mori-r33/MoriR33.SrcBlkMq/blk-mq-2.src || curl -sSL --fail -m 60 https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-mq.c -o /fast/scratch/hyaku/mori-r33/MoriR33.SrcBlkMq/blk-mq-2.src; printf "sha256="; sha256sum /fast/scratch/hyaku/mori-r33/MoriR33.SrcBlkMq/blk-mq-2.src; printf "bytes="; wc -c < /fast/scratch/hyaku/mori-r33/MoriR33.SrcBlkMq/blk-mq-2.src'
```

  Output: `accessed=2026-10-23T02:39:58Z`; SHA-256 and bytes as listed above.
- Source locations below refer to the unchanged saved copy `blk-mq-1.src`; v7.2 tag is in the URL. Source lines: completion accounting 856-864; in-flight check 93-103; done accounting 1069-1088.

## Draft SOURCES row

```text
| SRC | Linux block multiqueue request accounting at v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-mq.c | code | A | v7.2 request accounting only: completion-path sector credit; done-path ios and nsecs updates; in-flight request counting by direction after stat, device and state checks. Not a /proc/diskstats or /sys/block/<dev>/stat field mapping, not write-only behavior, and not a rate, reset, wrap or aggregation rule. | blk_account_io_completion:856-864; blk_mq_check_in_driver:93-103; blk_account_io_done:1069-1088; tag v7.2; 136798 B, opened 2026-10-23T02:39:58Z; sha256 7483f1738ad1a00372f5fca0e553023ff4a683e4e2a73c01b3da31302bba8c11 | The RQF_IO_STAT completion path selects an operation-stat group and adds the supplied byte count shifted right nine bits to sector statistics; blk_account_io_done increments the operation group's ios and adds now minus req->start_time_ns to nsecs; the in-flight branch increments a direction-indexed bucket only for requests passing its stat, device and in-flight-state filters. | mined | 2026-10-23 | on-release | corpus/knowledge/disk-write-rate-r33.md |
```

## Draft Gate row

```text
| SRC | https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-mq.c | 2026-10-23T02:39:58Z | 7483f1738ad1a00372f5fca0e553023ff4a683e4e2a73c01b3da31302bba8c11 | blk_account_io_completion: `SRC.src:856-862` (25 words): "static void blk_account_io_completion(struct request *req, unsigned int bytes) { if (req->rq_flags & RQF_IO_STAT) { const int sgrp = op_stat_group(req_op(req)); part_stat_lock(); part_stat_add(req->part, sectors[sgrp], bytes >> 9);"; blk_account_io_done declaration: `SRC.src:1069` (8 words): "static inline void blk_account_io_done(struct request *req, u64 now)"; done-path counters: `SRC.src:1083-1084` (7 words): "part_stat_inc(req->part, ios[sgrp]); part_stat_add(req->part, nsecs[sgrp], now - req->start_time_ns);"; in-flight branch: `SRC.src:97-100` (15 words): "if (rq->rq_flags & RQF_IO_STAT && (!bdev_is_partition(mi->part) \|\| rq->part == mi->part) && blk_mq_rq_state(rq) == MQ_RQ_IN_FLIGHT) mi->inflight[rq_data_dir(rq)]++;" | admit, A, mined |
```

## Numbered facts and quoted support

1. `blk_account_io_completion` gates this code on `RQF_IO_STAT`, selects the operation-stat group, and adds `bytes >> 9` to that group's sector counter. Quote Q1: `SRC.src:856-862` (25 words): "static void blk_account_io_completion(struct request *req, unsigned int bytes) { if (req->rq_flags & RQF_IO_STAT) { const int sgrp = op_stat_group(req_op(req)); part_stat_lock(); part_stat_add(req->part, sectors[sgrp], bytes >> 9);"
2. `blk_account_io_done` is the named done hook; its body increments the operation group's `ios` and adds the `now - req->start_time_ns` difference to `nsecs`. Quotes Q2 and Q3: `SRC.src:1069` (8 words): "static inline void blk_account_io_done(struct request *req, u64 now)"; `SRC.src:1083-1084` (7 words): "part_stat_inc(req->part, ios[sgrp]); part_stat_add(req->part, nsecs[sgrp], now - req->start_time_ns);"
3. An in-flight counter indexed by `rq_data_dir(rq)` is incremented when the request-stat and in-flight-state conditions pass and the target is not a partition or the request's partition matches it. Quote Q4: `SRC.src:97-100` (15 words): "if (rq->rq_flags & RQF_IO_STAT && (!bdev_is_partition(mi->part) \|\| rq->part == mi->part) && blk_mq_rq_state(rq) == MQ_RQ_IN_FLIGHT) mi->inflight[rq_data_dir(rq)]++;"

## Facts a reader might assume but this page does not state

- The file does not name `/proc/diskstats` or `/sys/block/<dev>/stat`, describe either field layout, or connect these internal counters to those user-visible fields.
- It does not say the shown sector accounting is write-only or define how to select write operations for a write-rate calculation.
- It gives no sampling interval or rate formula, nor counter reset/wrap behavior or whole-disk/partition/stacked-device aggregation rules.

## Gates, touched surfaces, and limits

- Gate evidence: the URL lookup in `corpus/SOURCES.md` had no match; both independently saved fetches returned 136,798 bytes with identical SHA-256; the requested v7.2 raw path therefore worked without fallback.
- Touched surfaces: only this report was written in the lane; the two unchanged source copies are in the seat scratch directory listed above. No registry, entry, lesson, judge, or source-copy commit was made.
- Out of scope: no counter or tests were run; no judge, runtime, `/proc` observation, or block-device setting was touched. No tools were installed or updated.
- Artifact: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/w1/SrcBlkMq.md`.
