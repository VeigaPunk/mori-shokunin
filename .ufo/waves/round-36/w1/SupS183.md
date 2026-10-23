measured 2026-10-23T12:03:45Z

# SupS183 — source re-open and superseding-row draft

## Behavior and finding

- At lane tip `6bd57097`, `corpus/SOURCES.md:189` records S183 as the v7.2 `part_stat.h` source; its scope, anchor and teaches are carried into the draft below. The required tip read (`git show 6bd57097:corpus/SOURCES.md | grep '^| S183 '`) returned that row.
- The round-35 spot-check records S183's earlier in-place anchor change `:10,61-63` → `:10,60-63` and teaches change from `the whole disk (bdev_whole)` to `bdev_whole(part)`, classifies them as real-content changes with no old-to-new log, and calls S183 a defect (`.ufo/waves/round-35/w2/ScoutAppendDebt.md:37,67`). Its named first-published commit is `62db24c0`; `git show 62db24c0:corpus/SOURCES.md | grep '^| S183 '` confirms the old anchor and teaches. The current tip wording is therefore the cell content to carry into a superseding row, not a finding that the historical edit was append-only compliant.
- Re-opened the tip source-cell URL on 2026-10-23 with `curl --fail-with-body --location --silent --show-error --max-time 90 --output /fast/scratch/hyaku/mori-r36/SupS183/S183.src --write-out 'HTTP_STATUS:%{http_code}\n' https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/part_stat.h`; observed `HTTP_STATUS:200`. `sha256sum /fast/scratch/hyaku/mori-r36/SupS183/S183.src` returned `2e22ee58e88396108d9962b122082d899fd517e3c67195e9dee580db63d55a9a`.
- Opened bytes support the tip anchor and teaches: line 10 is `unsigned long sectors[NR_STAT_GROUPS];`; line 62 tests `bdev_is_partition(part)`; line 63 adds to `bdev_whole(part)`. The source lines are in `/fast/scratch/hyaku/mori-r36/SupS183/S183.src:10,60-63` and at the URL above. The tip used-by path exists at `6bd57097` (`git cat-file -e 6bd57097:corpus/knowledge/disk-write-rate-r33.md` exited 0).

VERDICT: supported

This verdict is about the tip cells against the reopened source. The historical in-place immutable-cell edit remains the round-35 append-only defect; the draft superseding row preserves the tip claims.

## Draft superseding row

Modeled on the 11-column rows S073 and S201 (`corpus/SOURCES.md:79,207`). No cell contains a quote mark or embedded pipe.

```DRAFT corpus/SOURCES.md
| S2NN | Linux include/linux/part_stat.h at v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/part_stat.h | code | A | the v7.2 per-device statistics macros: part_stat_add on a partition also adds to the whole disk; sector counters are unsigned long | include/linux/part_stat.h:10,60-63; tag v7.2 | supersedes S183 — part_stat_add applies an add made to a partition a second time to bdev_whole(part); the sectors array is unsigned long. | mined | 2026-10-23 | on-release | corpus/knowledge/disk-write-rate-r33.md |
```

## Draft lesson Gate line

The located-quote table shape follows `corpus/lessons/round-23.md:219-222`. Quotes are contiguous source text, each under 25 words.

```DRAFT corpus/lessons/round-36.md
| S2NN | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/part_stat.h ; 2026-10-23 ; sha256 2e22ee58e88396108d9962b122082d899fd517e3c67195e9dee580db63d55a9a | line 10: `unsigned long sectors[NR_STAT_GROUPS];` (5 words); line 62: `if (bdev_is_partition(part))` (1); line 63: `__part_stat_add(bdev_whole(part), field, addnd);` (1) | supported — tip anchor and teaches match the opened v7.2 bytes |
```

## Gates and surfaces

- Source-open gate: passed, ordinary `curl`, HTTP 200; no bot challenge or retry. SHA-256 and quotes above identify the saved bytes.
- Tip-path gate: passed for the one used-by path, by the `git cat-file -e` command above.
- Touched surfaces: this scoped report and `/fast/scratch/hyaku/mori-r36/SupS183/S183.src` only. No lane product file, git index, or repository history was written; no install, test, build, or other runtime check was performed.
- Out of scope: assigning the final S2NN identifier, applying the drafts to `corpus/SOURCES.md` or a lesson, and integration/closure decisions remain with L1.

## Artifacts

- Report: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/w1/SupS183.md`.
- Re-opened source bytes: `/fast/scratch/hyaku/mori-r36/SupS183/S183.src` — SHA-256 `2e22ee58e88396108d9962b122082d899fd517e3c67195e9dee580db63d55a9a`.
