measured 2026-10-23T05:38:55Z
# ReopenS194 — source row S194 (zram_drv.c v7.2, gendisk registration)

Seat: MoriR34A2.ReopenS194. Object: SOURCES.md row S194 at lane tip 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3.
URL: https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/block/zram/zram_drv.c

## Live fetch (twice) vs committed copy

- Fetch 1: start=2026-10-23T05:38:39Z, sha256 d5d4933a2aed57d667edbb8c8904be3d9569a61cc5a428a2cd8b044aeab00f25, 3301 lines / 78168 bytes (`curl -sSL --fail -m 60 ... -o /fast/scratch/hyaku/mori-r34/a2-ReopenS194/S194.live1.c`).
- Fetch 2: start=2026-10-23T05:38:43Z, sha256 d5d4933a2aed57d667edbb8c8904be3d9569a61cc5a428a2cd8b044aeab00f25, 3301 lines / 78168 bytes (same command, S194.live2.c).
- Committed copy corpus/evidence/sources-r34/S194.src: sha256 d5d4933a2aed57d667edbb8c8904be3d9569a61cc5a428a2cd8b044aeab00f25, 3301 lines / 78168 bytes.
- `cmp` results: S194.live1.c == S194.live2.c; both == S194.src. All three byte-identical.
- The pinned URL serves the v7.2 tag content, and the committed copy matches the live source exactly.

## Anchor cell check

Row anchor: `drivers/block/zram/zram_drv.c:3094; tag v7.2`.
- S194.src:3094 holds exactly `	ret = device_add_disk(NULL, zram->disk, zram_disk_groups);`. Anchor line holds the cited code.
- `grep device_add_disk` over S194.src returns only line 3094; it is the sole device_add_disk call in the file (the rest of the file is byte-identical to the live fetch).
- The call sits in the zram gendisk registration path (blk_alloc_disk at :3074, capacity set at :3093, device_add_disk at :3094, cleanup labels after). Scope `how v7.2 zram registers its gendisk` is accurate.

## Teaches cell, clause by clause

Clause 1: "zram calls device_add_disk with NULL as its first argument (the parent argument per S182's device_add_disk signature)."
- Supported. Contiguous located quote, S194.src:3094 (5 words): "ret = device_add_disk(NULL, zram->disk, zram_disk_groups);"
- The parenthetical "(the parent argument per S182's device_add_disk signature)" is a cross-row pointer to S182 (block/genhd.c, device_add_disk lines at S182 anchor); the first-argument-is-parent identification is consistent with that row's claim and with S193's symlink semantics. Not re-verified against genhd.c here (outside this row's object; the direct claim is anchored at 3094).

Clause 2: "lane rule: with S193, a zram disk has no `device` link and is classed virtual (tool rule R3)."
- Labelled `lane rule:` — exempt from quote sourcing per the reopen instruction. It is a lane-derived rule, not a source claim.

No clause lacks a source anchor: clause 1 is quoted; clause 2 is an exempt lane rule.

## Gate row proposal

| S194 | https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/block/zram/zram_drv.c | 2026-10-23 | d5d4933a2aed57d667edbb8c8904be3d9569a61cc5a428a2cd8b044aeab00f25 | S194.src:3094 (5): "ret = device_add_disk(NULL, zram->disk, zram_disk_groups);" | admit, A, mined |

VERDICT: admit

## Notes

- No tools installed (curl already present; no pacman/uv/cargo action needed).
- Scratch: /fast/scratch/hyaku/mori-r34/a2-ReopenS194/S194.live1.c, S194.live2.c (kept as fetch evidence; ~156 KB total).
