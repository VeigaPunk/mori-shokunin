measured 2026-10-23T12:04:34Z

# SupS189 — round-35 append-only debt

## Finding

VERDICT: supported

At tip `6bd57097f7ab2b471b4593ed2019c980b1368c68`, S189's cells are the row at `corpus/SOURCES.md:195`; its anchor is `patch lines 7-17 (commit message)` and its teaches says discard I/O has the same four statistics as reads and writes, including completed discard sectors. I captured the tip registry with `timeout 120s git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 6bd57097:corpus/SOURCES.md > /fast/scratch/hyaku/mori-r36/SupS189/tip-SOURCES.md`; searching that snapshot for `^\| S189 \|` returned the row at line 195.

The first-published row at `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8` had the same non-anchor cells and anchor `patch lines 9-10,14`; the `git show --format=fuller --no-ext-diff --unified=0 62db24c... -- corpus/SOURCES.md` diff adds S189 in the round-33 S180-S190 batch. `git show --format=fuller --no-ext-diff --unified=0 ab8f4cfe -- corpus/SOURCES.md` shows only S189's anchor changing to `patch lines 7-17`, with teaches unchanged. This matches `.ufo/waves/round-35/w2/ScoutAppendDebt.md:47` (the in-place locator edit and missing old-to-new lesson entry).

Re-opened the tip URL using ordinary curl: `timeout 120s curl --location --silent --show-error --output /fast/scratch/hyaku/mori-r36/SupS189/S189.src --write-out 'HTTP_STATUS=%{http_code}\n' https://github.com/torvalds/linux/commit/bdca3c87fb7ad1cc61d231d37eb0d8f90d001e0c.patch` returned `HTTP_STATUS=200`. `sha256sum /fast/scratch/hyaku/mori-r36/SupS189/S189.src` returned `f265ef76e862e4e48cdbdae1b4702cbe47b356501d5d6cbfe9abeaaacd4cf318`. The bytes at `S189.src:7-15` support the full tip anchor and teaches; no correction is needed.

Located quotes from the reopened bytes (each contiguous and under 25 words):
- `S189.src:7-8` — Add tracking of REQ_OP_DISCARD ios to the partition statistics and append them to the various stat files in /sys as well as (22 words).
- `S189.src:9-10` — /proc/diskstats. These are tracked with the same four stats as reads and writes: (13 words).
- `S189.src:14` — Number of discard sectors completed (5 words).

`timeout 120s git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file -e 6bd57097:corpus/knowledge/disk-write-rate-r33.md` succeeded; output was `tip path exists`. Thus the carried used-by path exists at the requested tip.

## Drafts for L1

DRAFT corpus/SOURCES.md
```DRAFT corpus/SOURCES.md
| S2NN | Linux commit bdca3c87 block Track DISCARD statistics and output them in stat and diskstat patch view — https://github.com/torvalds/linux/commit/bdca3c87fb7ad1cc61d231d37eb0d8f90d001e0c.patch | code | A | discard accounting: its own four statistics, appended to the stat files and /proc/diskstats | patch lines 7-17 (commit message) | supersedes S189 — Discard I/O is tracked with its own four statistics of the kinds kept for reads and writes, including discard sectors completed. | mined | 2026-10-23 | on-release | corpus/knowledge/disk-write-rate-r33.md |
```

DRAFT corpus/lessons/round-36.md §Gate
```DRAFT corpus/lessons/round-36.md §Gate
| S2NN | https://github.com/torvalds/linux/commit/bdca3c87fb7ad1cc61d231d37eb0d8f90d001e0c.patch | 2026-10-23 | `f265ef76e862e4e48cdbdae1b4702cbe47b356501d5d6cbfe9abeaaacd4cf318` | (22) Add tracking of REQ_OP_DISCARD ios to the partition statistics and append them to the various stat files in /sys as well as — `S189.src:7-8`; (13) /proc/diskstats. These are tracked with the same four stats as reads and writes: — `S189.src:9-10`; (5) Number of discard sectors completed — `S189.src:14` | admit, A, supersedes S189 — (SupS189) |
```

## Surfaces, gates, limits

- Lane write: this report only. Scratch artifacts: `/fast/scratch/hyaku/mori-r36/SupS189/S189.src` (SHA-256 above), `tip-SOURCES.md`, and `first-published-SOURCES.md`. No product file, registry, lesson, judge, or git index was changed.
- Behavior: source evidence confirms S189's tip claim; no product behavior changed. No checker, counter, test, or other code gate was run. The Gate line above is a draft only.
- Out of scope: assigning the final numeric row ID and landing either draft. No tool was installed.
