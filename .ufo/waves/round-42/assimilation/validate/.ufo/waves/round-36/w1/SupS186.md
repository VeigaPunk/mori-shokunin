measured 2026-10-23T12:04:50Z

# SupS186 — round-35 append-only debt

## Axes and verdict

VERDICT: supported

The live v7.2 source supports the tip S186 scope, anchor, and teaches; no tip wording needs correction. The historic in-place changes to immutable scope, anchor, and teaches still require a superseding row under the append-only rule; the round-35 debt note records those changes and that they were not logged old-to-new (`.ufo/waves/round-35/w2/ScoutAppendDebt.md:11,43`; `CORPUS.md:116-118`).

The first-published row was added by `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8` (commit subject says sources S180-S190); its parent has no S186 row. First-published cells were read from that commit and match the older values in the debt note (`ScoutAppendDebt.md:43`; command and output below).

## Re-open and checks

- Tip row: `timeout 120s git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 6bd57097:corpus/SOURCES.md | grep '^| S186 '` → source URL `https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/blk_types.h`, code/A, scope `the v7.2 kernel sector unit (512 bytes, SECTOR_SHIFT 9) and the bdev_whole macro`, anchor `include/linux/blk_types.h:25-28,31,84-85; tag v7.2`, teaches as drafted below, status mined, opened 2026-10-23, recheck on-release, used-by `corpus/knowledge/disk-write-rate-r33.md`.
- First-published row: `timeout 120s git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 62db24c01d5b7c2247f43852ea2b28d0ae5e40c8:corpus/SOURCES.md | grep '^| S186 '` → the first-published scope/anchor/teaches were `the v7.2 kernel sector unit: 512 bytes, SECTOR_SHIFT 9`, `include/linux/blk_types.h:25-26,31; tag v7.2`, and `The sector is the basic unit of block I/O; one sector is 512 = 2**9 (bytes, per the same comment) and SECTOR_SHIFT is 9.` `timeout 120s git -C /home/vgpnk/Projects/shokunin/mori-shokunin show -s --format="%H %ad %s" --date=iso-strict 62db24c01d5b7c2247f43852ea2b28d0ae5e40c8` → `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8 2026-10-22T23:55:24-03:00 round-33: C1 FR6 entry, sources S180-S190, round-32 repair, QUALITY 97, wave-1 reports`; parent check → `PARENT_HAS_S186=no`.
- Live fetch and saved artifact: `timeout 120s bash -c 'mkdir -p /fast/scratch/hyaku/mori-r36/SupS186 && curl -L -sS -w "HTTP_STATUS=%{http_code}\\n" -o /fast/scratch/hyaku/mori-r36/SupS186/S186.src https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/blk_types.h && sha256sum /fast/scratch/hyaku/mori-r36/SupS186/S186.src'` → `HTTP_STATUS=200`; SHA-256 `adff86f6d9433c496dc5ddf32d0e353a24969af7ed90191dffc562f1998b2e6e`.
- Read-only existence check: `timeout 120s git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file -e 6bd57097:corpus/knowledge/disk-write-rate-r33.md` → exit 0, no output; used-by path exists at tip.

Quotes from the opened bytes (all within 25 words; locations are in `S186.src`):
- `The basic unit of block I/O is a sector.` — `include/linux/blk_types.h:25` (9 words).
- `The size of one sector is 512 = 2**9` — `:26` (9 words); `bytes.` — `:27` (1 word). The source comment states the unit is 512 bytes (`:26-28`).
- `#define SECTOR_SHIFT 9` — `:31` (3 words).
- `#define bdev_whole(_bdev)` — `:84` (2 words); `((_bdev)->bd_disk->part0)` — `:85` (one code expression).

These lines support each tip claim, including the macro expansion. No tip words fail; the tip cells are supported. The source file was not imported by a checker or another program.

## Drafts for L1

```DRAFT corpus/SOURCES.md
| S2NN | Linux include/linux/blk_types.h at v7.2 (sector unit) — https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/blk_types.h | code | A | the v7.2 kernel sector unit (512 bytes, SECTOR_SHIFT 9) and the bdev_whole macro | include/linux/blk_types.h:25-28,31,84-85; tag v7.2 | supersedes S186 — The sector is the basic unit of block I/O; one sector is 512 = 2**9 (bytes, per the same comment) and SECTOR_SHIFT is 9; bdev_whole(bdev) is bd_disk->part0. | mined | 2026-10-23 | on-release | corpus/knowledge/disk-write-rate-r33.md |
```

```DRAFT corpus/lessons/round-36.md Gate line
| S2NN | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/blk_types.h (accessed 2026-10-23) | `adff86f6d9433c496dc5ddf32d0e353a24969af7ed90191dffc562f1998b2e6e` | (9 words) The basic unit of block I/O is a sector. — `include/linux/blk_types.h:25`; (9 words) The size of one sector is 512 = 2**9 — `:26`; (1 word) bytes. — `:27`; (3 words) #define SECTOR_SHIFT 9 — `:31`; (2 words) #define bdev_whole(_bdev) — `:84`; (one code expression) ((_bdev)->bd_disk->part0) — `:85` | supported; admit, A, supersedes S186 — |
```

## Gates, surfaces, limits

No test, census, or append-only checker was run; this is a source re-open and row draft only. No tools were installed. Only the requested report and scratch source bytes were written; no product files, source rows, lesson, index, or commits were changed. Scratch artifact: `/fast/scratch/hyaku/mori-r36/SupS186/S186.src` (SHA-256 above). Report: `.ufo/waves/round-36/w1/SupS186.md`.