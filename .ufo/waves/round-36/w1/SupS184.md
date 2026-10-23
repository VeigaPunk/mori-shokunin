measured 2026-10-23T12:03:33Z

# SupS184 — round-35 routed defect 2

## Behavior and gates
- Axes: source fidelity, provenance, containment. Timestamp command: `timeout 120s date -u +%FT%TZ` → `2026-10-23T12:03:33Z`.
- Tip row: `timeout 120s git -C /home/vgpnk/Projects/shokunin/mori-shokunin show '6bd57097:corpus/SOURCES.md' | grep '^| S184 '` returned the tip cells, including status `mined`, opened `2026-10-23`, recheck `on-release`, and used-by `corpus/knowledge/disk-write-rate-r33.md`. The used-by path exists: `timeout 120s git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file -e '6bd57097:corpus/knowledge/disk-write-rate-r33.md' && printf 'exists at 6bd57097\\n'` → `exists at 6bd57097`.
- First publication: `timeout 120s git -C /home/vgpnk/Projects/shokunin/mori-shokunin show '62db24c0:corpus/SOURCES.md' | grep '^| S184 '` returned the first cells; `timeout 120s git -C /home/vgpnk/Projects/shokunin/mori-shokunin show '62db24c0^:corpus/SOURCES.md' | grep '^| S184 '` returned no output, exit 1. The parent tree exists (`timeout 120s git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file -e '62db24c0^:corpus/SOURCES.md' && printf 'parent tree exists\\n'` → `parent tree exists`), so `62db24c0` is first publication. Anchor changed from `block/blk-core.c:1067-1068,1100,1110` to `block/blk-core.c:1067-1068,1100,1108-1110`; `.ufo/waves/round-35/w2/ScoutAppendDebt.md:39` records commit `ab8f4cfe` and classifies it as real locator content, not formatting or an allowed column. `timeout 120s git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 'ab8f4cfe:corpus/SOURCES.md' | grep '^| S184 '` returned the tip anchor. This is the routed immutable-cell defect; reopened bytes support the tip cells.
- Re-open command: `timeout 120s bash -c 'mkdir -p /fast/scratch/hyaku/mori-r36/SupS184 && curl --max-time 100 --silent --show-error --output /fast/scratch/hyaku/mori-r36/SupS184/S184.src --write-out "%{http_code}" https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-core.c'` → HTTP `200`. Hash command: `timeout 120s sha256sum /fast/scratch/hyaku/mori-r36/SupS184/S184.src` → `528501312dbd8da7649051006f12203fbef03f5180c4408ccc20856262c77827`.
- Quotes from `/fast/scratch/hyaku/mori-r36/SupS184/S184.src` (each contiguous and ≤25 words): lines `1067-1068` — `(end || bdev_count_inflight(part)) __part_stat_add(part, io_ticks, now - stamp);`; line `1100` — `void bdev_end_io_acct(struct block_device *bdev, enum req_op op,`; lines `1108-1110` — `update_io_ticks(bdev, now, true); part_stat_inc(bdev, ios[sgrp]); part_stat_add(bdev, sectors[sgrp], sectors);`. These support the tip anchor and teaches. Lines `1089-1098` document `bio_start_io_acct`; `1117-1122` show `bio_end_io_acct_remapped` calling `bdev_end_io_acct`. No cell correction is needed.
- Fetched bytes are at `/fast/scratch/hyaku/mori-r36/SupS184/S184.src` and contain 1329 lines (read selector output). No tool was installed or updated. No product file, judge, or git index was changed; no build or tests were run.

## Drafts

DRAFT corpus/SOURCES.md
```text
| S2NN | Linux block/blk-core.c at v7.2 (bio accounting and update_io_ticks) — https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-core.c | code | A | v7.2 bio-based accounting: sectors added in bdev_end_io_acct through part_stat_add; io_ticks advanced by elapsed time when I/O is in flight or ending | block/blk-core.c:1067-1068,1100,1108-1110; tag v7.2 | supersedes S184 — bdev_end_io_acct adds the completed sectors with part_stat_add; update_io_ticks adds the elapsed time to io_ticks only when an I/O ends or one is in flight. | mined | 2026-10-23 | on-release | corpus/knowledge/disk-write-rate-r33.md |
```

DRAFT corpus/lessons/round-36.md — Gate row (URL accessed 2026-10-23)
```text
| S2NN | https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-core.c (accessed 2026-10-23) | `528501312dbd8da7649051006f12203fbef03f5180c4408ccc20856262c77827` | `(end \|\| bdev_count_inflight(part)) __part_stat_add(part, io_ticks, now - stamp);` — `block/blk-core.c:1067-1068`; `void bdev_end_io_acct(struct block_device *bdev, enum req_op op,` — `:1100`; `update_io_ticks(bdev, now, true); part_stat_inc(bdev, ios[sgrp]); part_stat_add(bdev, sectors[sgrp], sectors);` — `:1108-1110` | admit, A, supersedes S184 (SrcS184Supersede) |
```

VERDICT: supported

## Surfaces and limits
- Written surfaces: this report and `/fast/scratch/hyaku/mori-r36/SupS184/S184.src` only. Scratch SHA-256 and HTTP status are recorded above.
- Out of scope: editing `SOURCES.md` or the round-36 lesson, assigning the placeholder ID, integrating, committing, or running checks.
