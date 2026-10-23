measured 2026-10-23T12:05:03Z

# S185 supersede review

Axes: source support; append-only correctness; provenance and containment.

## Behavior and gates
- Re-opened by ordinary `curl` from `https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-mq.c`; outcome `HTTP_STATUS=200`. Bytes saved to `/fast/scratch/hyaku/mori-r36/SupS185/S185.src`; SHA-256 `7483f1738ad1a00372f5fca0e553023ff4a683e4e2a73c01b3da31302bba8c11` (curl and sha256sum command outputs).
- Reviewed tip registry with `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 6bd57097:corpus/SOURCES.md | grep '^| S185 '`. Tip cells: source Linux block/blk-mq.c at v7.2; kind code; tier A; scope v7.2 request-based accounting, sectors added from completed bytes in blk_account_io_completion; anchor `block/blk-mq.c:856,858,862; tag v7.2`; teaches the RQF_IO_STAT precondition and shifted-byte sector update; status mined; opened 2026-10-23; recheck on-release; used-by `corpus/knowledge/disk-write-rate-r33.md`.
- `git log --reverse --format='%H %s' -S'| S185 |' -- corpus/SOURCES.md` returned `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8` as the row introduction. `git show 62db24c0:corpus/SOURCES.md | grep '^| S185 '` showed first-published anchor `block/blk-mq.c:856,862; tag v7.2` and teaches without the RQF_IO_STAT precondition. `git show ab8f4cfe:corpus/SOURCES.md | grep '^| S185 '` showed the later in-place addition of line 858 and the RQF_IO_STAT clause; this is the rewrite ScoutAppendDebt records at its line 41. The append-only rule requires corrections to be a new row beginning `supersedes S0NN —` (CORPUS.md:116-118).
- Source evidence from the saved bytes: line 856 `static void blk_account_io_completion(struct request *req, unsigned int bytes)`; line 858 `if (req->rq_flags & RQF_IO_STAT) {`; line 862 `part_stat_add(req->part, sectors[sgrp], bytes >> 9);` (`/fast/scratch/hyaku/mori-r36/SupS185/S185.src:856,858,862`). Each quotation is contiguous and under 25 words.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file -e 6bd57097:corpus/knowledge/disk-write-rate-r33.md` exited 0 (`USED_BY_EXISTS=yes`).

VERDICT: supported

The tip anchor locators and teaches are supported by the reopened v7.2 bytes: the function is guarded by RQF_IO_STAT and adds `bytes >> 9` to the sectors statistic. No tip-cell correction is needed. ScoutAppendDebt.md:41,69 identifies S185 as an unlogged immutable-cell rewrite; round-35's S201 example uses this supersede form (corpus/lessons/round-35.md:20).

## Drafts for L1

```text
DRAFT corpus/SOURCES.md
| S2NN | Linux block/blk-mq.c at v7.2 (request completion accounting) — https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-mq.c | code | A | v7.2 request-based accounting: sectors added from completed bytes in blk_account_io_completion | block/blk-mq.c:856,858,862; tag v7.2 | supersedes S185 — For a request flagged RQF_IO_STAT, blk_account_io_completion adds completed bytes shifted right by 9 to the sector counter. | mined | 2026-10-23 | on-release | corpus/knowledge/disk-write-rate-r33.md |
```

```text
DRAFT corpus/lessons/round-36.md Gate
| S2NN | https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-mq.c (accessed 2026-10-23) | 7483f1738ad1a00372f5fca0e553023ff4a683e4e2a73c01b3da31302bba8c11 | `static void blk_account_io_completion(struct request *req, unsigned int bytes)` — `block/blk-mq.c:856`; `if (req->rq_flags & RQF_IO_STAT) {` — `:858`; `part_stat_add(req->part, sectors[sgrp], bytes >> 9);` — `:862` | admit, A; tip cells supported |
```

## Touched surfaces, limits, artifacts
- Lane write: this report only, `.ufo/waves/round-36/w1/SupS185.md`. Scratch artifact: `/fast/scratch/hyaku/mori-r36/SupS185/S185.src` (SHA-256 above). No product, registry, lesson, judge, commit, or index edits; no tests or other gates were run; no tools installed or updated.
- Scope is the pinned Linux v7.2 source and S185 cells at tip 6bd57097; no claim is made about other kernel versions. No subagents or background processes were started.
