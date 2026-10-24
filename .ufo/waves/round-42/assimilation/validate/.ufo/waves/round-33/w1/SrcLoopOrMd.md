# FR6 C1 source findings: loop vs md

## Result and axes
- Axes considered: source provenance, quote-level factual support, and relevance to the stacked-device double-count claim.
- The requested loop candidate exists at the exact v7.2 URL and was fetched, but `loop.c` shows write requests passed to the backing file's `write_iter` (`loop.c:396-400, 428-431`); it does not contain an explicit I/O-stat accounting hook. An exact search for `part_stat|bio_start_io_acct|bio_end_io_acct|blk_queue_io_stat|blk_account_io` returned `No matches found`.
- I therefore used the permitted `drivers/md/md.c` fallback. It provides evidence of MD-path I/O accounting and a separate read of the selected gendisk's sector stats, but does not by itself state that member devices account the same data or that summing lines double-counts it.

## Fetch provenance

### Loop candidate (not selected)
- URL: `https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/block/loop.c`
- First access: `2026-10-23T02:39:46Z`; bytes: `59650`; SHA-256: `05b749e12a0f839a109c71965148f2100b8bd469b73d4e627d8bd08da944d1de`.
- Second access: `2026-10-23T02:39:50Z`; bytes: `59650`; SHA-256: `05b749e12a0f839a109c71965148f2100b8bd469b73d4e627d8bd08da944d1de`.
- Both fetches were identical by SHA-256. Scratch files: `/fast/scratch/hyaku/mori-r33/SrcLoopOrMd/loop.c.src` and `/fast/scratch/hyaku/mori-r33/SrcLoopOrMd/loop.second.src`.

### MD fallback (selected draft)
- URL: `https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/md/md.c`
- First access: `2026-10-23T02:40:14Z`; bytes: `289723`; SHA-256: `61a58304f00d1b215c5e09732f58b96f7edb4f5a0106d1c678a6736f0bb641b1`.
- Second access: `2026-10-23T02:40:20Z`; bytes: `289723`; SHA-256: `61a58304f00d1b215c5e09732f58b96f7edb4f5a0106d1c678a6736f0bb641b1`.
- Both fetches were identical by SHA-256. Scratch files: `/fast/scratch/hyaku/mori-r33/SrcLoopOrMd/md.c.src` and `/fast/scratch/hyaku/mori-r33/SrcLoopOrMd/md.second.src`.
- The exact loop and md URLs were searched in `corpus/SOURCES.md` before fetching; `functions.grep` returned `No matches found` for each. Both exact raw paths fetched successfully at tag `v7.2`; no path correction was needed.

Commands and outcomes:
```sh
timeout 70 sh -c 'mkdir -p /fast/scratch/hyaku/mori-r33/SrcLoopOrMd && date -u +%FT%TZ && curl -sSL --fail -m 60 https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/block/loop.c -o /fast/scratch/hyaku/mori-r33/SrcLoopOrMd/loop.c.src && sha256sum /fast/scratch/hyaku/mori-r33/SrcLoopOrMd/loop.c.src && wc -c < /fast/scratch/hyaku/mori-r33/SrcLoopOrMd/loop.c.src'
```
Output: `2026-10-23T02:39:46Z`; `05b749e12a0f839a109c71965148f2100b8bd469b73d4e627d8bd08da944d1de`; `59650`.
```sh
timeout 70 sh -c 'date -u +%FT%TZ && curl -sSL --fail -m 60 https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/block/loop.c -o /fast/scratch/hyaku/mori-r33/SrcLoopOrMd/loop.second.src && sha256sum /fast/scratch/hyaku/mori-r33/SrcLoopOrMd/loop.second.src && wc -c < /fast/scratch/hyaku/mori-r33/SrcLoopOrMd/loop.second.src'
```
Output: `2026-10-23T02:39:50Z`; `05b749e12a0f839a109c71965148f2100b8bd469b73d4e627d8bd08da944d1de`; `59650`.
```sh
timeout 70 sh -c 'date -u +%FT%TZ && curl -sSL --fail -m 60 https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/md/md.c -o /fast/scratch/hyaku/mori-r33/SrcLoopOrMd/md.c.src && sha256sum /fast/scratch/hyaku/mori-r33/SrcLoopOrMd/md.c.src && wc -c < /fast/scratch/hyaku/mori-r33/SrcLoopOrMd/md.c.src'
```
Output: `2026-10-23T02:40:14Z`; `61a58304f00d1b215c5e09732f58b96f7edb4f5a0106d1c678a6736f0bb641b1`; `289723`.
```sh
timeout 70 sh -c 'date -u +%FT%TZ && curl -sSL --fail -m 60 https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/md/md.c -o /fast/scratch/hyaku/mori-r33/SrcLoopOrMd/md.second.src && sha256sum /fast/scratch/hyaku/mori-r33/SrcLoopOrMd/md.second.src && wc -c < /fast/scratch/hyaku/mori-r33/SrcLoopOrMd/md.second.src'
```
Output: `2026-10-23T02:40:20Z`; `61a58304f00d1b215c5e09732f58b96f7edb4f5a0106d1c678a6736f0bb641b1`; `289723`.

## Draft rows
The `SRC` identifier is a placeholder for the L1-assigned S180+ id. Gate locators use the required `SRC.src` placeholder; line numbers refer to the saved `md.c.src` bytes above.

SOURCES:
```text
| SRC | Linux kernel drivers/md/md.c at v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/md/md.c | code | A | MD bio-accounting and gendisk sector-stat paths; this source does not compare member-device counts | drivers/md/md.c:9229-9233 (is_mddev_idle); 9387-9409 (md_end_clone_io); 9412-9435 (md_clone_bio); tag v7.2 | The idle check reads accumulated sectors for its selected gendisk; md_clone_bio stores the input bio and conditionally starts I/O accounting when the bio's queue has I/O stats enabled, with completion against the original bio. | mined | 2026-10-23 | on-release | corpus/knowledge/disk-write-rate-r33.md |
```

Gate:
```text
| SRC | https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/md/md.c | 2026-10-23T02:40:14Z | 61a58304f00d1b215c5e09732f58b96f7edb4f5a0106d1c678a6736f0bb641b1 | `SRC.src:9229-9233` (15 words): "disk = mddev_is_dm(mddev) ? mddev->dm_gendisk : mddev->gendisk; if (!disk) return true; mddev->normal_io_events = part_stat_read_accum(disk->part0, sectors);"; `SRC.src:9420` (3 words): "md_io_clone->orig_bio = *bio;"; `SRC.src:9422-9423` (5 words): "if (blk_queue_io_stat(bdev->bd_disk->queue)) md_io_clone->start_time = bio_start_io_acct(*bio);"; `SRC.src:9401-9402` (4 words): "if (md_io_clone->start_time) bio_end_io_acct(orig_bio, md_io_clone->start_time);" | admit, A, mined |
```

## Numbered facts and quote evidence
1. The MD idle check selects its gendisk (or the DM gendisk) and reads that disk's accumulated sector count into `normal_io_events` (`md.c:9229-9233`).
   - Quote: `SRC.src:9229-9233` (15 words): "disk = mddev_is_dm(mddev) ? mddev->dm_gendisk : mddev->gendisk; if (!disk) return true; mddev->normal_io_events = part_stat_read_accum(disk->part0, sectors);"
2. The clone path retains the bio it received as the original bio (`md.c:9412-9420`).
   - Quote: `SRC.src:9420` (3 words): "md_io_clone->orig_bio = *bio;"
3. It initializes accounting only when the bio's block-device queue enables I/O stats, and takes the start time from the input bio (`md.c:9422-9423`).
   - Quote: `SRC.src:9422-9423` (5 words): "if (blk_queue_io_stat(bdev->bd_disk->queue)) md_io_clone->start_time = bio_start_io_acct(*bio);"
4. Completion calls the accounting end routine on the saved original bio when a start time exists (`md.c:9401-9402`).
   - Quote: `SRC.src:9401-9402` (4 words): "if (md_io_clone->start_time) bio_end_io_acct(orig_bio, md_io_clone->start_time);"

## Not stated by these sources
- `md.c` does not state that member-device counters record the same payload, nor that adding the MD and member rows double-counts it.
- These lines do not establish one-to-one or fixed fan-out mapping, RAID-mode-specific accounting, extra metadata traffic, or how sector totals differ after mapping.
- These code lines do not explicitly identify the `bio_start_io_acct` path with `/proc/diskstats` or `/sys/block/<dev>/stat` presentation.
- `loop.c` shows writes handed to the backing file's `write_iter` (`loop.c:396-400, 428-431`), but no explicit self-accounting hook was found by the exact search. This is a bounded search result, not proof that loop-device accounting is absent elsewhere in the kernel.
- Neither file states a reporting rule for summing stacked-device lines. Treat any such rule as lane doctrine or obtain a source that explicitly covers the missing side.

## Gates, touched surfaces, and limits
- No counter, judge, build, test, or formatting check was run; this is a source-opening report, not C1 execution evidence and not a claim that a future decision-table row passes R-J.
- Touched surfaces: this report and the four unchanged upstream source copies under `/fast/scratch/hyaku/mori-r33/SrcLoopOrMd/`. No product code, registry, Gate, judge, commit, or repository state was changed.
- Tool installs/updates: none. `/home/vgpnk/.omp/agent/RULES.md` was read before any tool-install decision.
- Report path: `.ufo/waves/round-33/w1/SrcLoopOrMd.md`.
