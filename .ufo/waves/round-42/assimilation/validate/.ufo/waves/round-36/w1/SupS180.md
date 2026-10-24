measured 2026-10-23T12:05:15Z

# SupS180 — round 36 source re-open

## Finding

VERDICT: supported

At lane tip `6bd57097`, S180 is a mined A-tier docs row with scope `the v7.2 /sys/block/<dev>/stat format: the 17-value line, the 512-byte sector unit, completion-time counting and the tick fields`; anchor `Documentation/block/stat.rst:2-5,21-22,71-73,75-80; tag v7.2`; and the teaches recorded in the draft below. Evidence: `timeout 120s bash -o pipefail -c "git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 6bd57097:corpus/SOURCES.md | grep '^| S180 '"` returned that row, with status `mined`, opened `2026-10-23`, recheck `on-release`, and used-by `corpus/knowledge/disk-write-rate-r33.md`.

The first-published row at `62db24c0` had anchor `Documentation/block/stat.rst:21-22,71-73,79-80; tag v7.2` and said tick values; command `timeout 120s bash -o pipefail -c "git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 62db24c0:corpus/SOURCES.md | grep '^| S180 '"` returned those cells. The round-35 routed finding identifies `62db24c0` as first publish and the later in-place anchor/teaches changes (`.ufo/waves/round-35/w2/ScoutAppendDebt.md:33`).

## Re-opened evidence

The source URL was opened by ordinary curl, HTTP 200. Command: `timeout 120s sh -c 'mkdir -p /fast/scratch/hyaku/mori-r36/SupS180 && curl --location --connect-timeout 15 --max-time 90 --silent --show-error --output /fast/scratch/hyaku/mori-r36/SupS180/S180.src --write-out "HTTP_STATUS:%{http_code}\n" https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/block/stat.rst && sha256sum /fast/scratch/hyaku/mori-r36/SupS180/S180.src && wc -c /fast/scratch/hyaku/mori-r36/SupS180/S180.src'`. Output: `HTTP_STATUS:200`; SHA-256 `4c35b795a518ceefea985f11e53b51f71d58fc99bf5a0920ca3738f13c90cb2e`; 4315 bytes. No retry was needed. Opened bytes are `/fast/scratch/hyaku/mori-r36/SupS180/S180.src`.

The four tip anchor locators and their contiguous quotes from the opened bytes:

- `Documentation/block/stat.rst:2-5` — (5 words) Block layer statistics in /sys/block/<dev>/stat — source line 2.
- `Documentation/block/stat.rst:21-22` — (17 words) The stat file consists of a single line of text containing 17 decimal values separated by whitespace. — lines 21-22.
- `Documentation/block/stat.rst:71-73` — (19 words) standard UNIX 512-byte sectors, not any device- or filesystem-specific block size. The counters are incremented when the I/O completes. — lines 72-73.
- `Documentation/block/stat.rst:75-80` — (17 words) If there are multiple I/O requests waiting, these values will increase at a rate greater than 1000/second; — lines 79-80.

These quotes support the title/file identity, 17 decimal values, standard 512-byte sector unit and completion counting, and millisecond waiting values increasing faster than 1000 per second with multiple requests waiting. The tip anchor and teaches hold against the reopened v7.2 bytes; no cell correction is needed. The used-by file exists at the tip: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree 6bd57097 corpus/knowledge/disk-write-rate-r33.md` returned `100644 blob 6f4f905c110861eefa74fee3b4853b40b1f7f04b corpus/knowledge/disk-write-rate-r33.md`.

## Drafts for L1

DRAFT corpus/SOURCES.md
```text
| S2NN | Linux block-device stat file documentation v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/block/stat.rst | docs | A | the v7.2 /sys/block/<dev>/stat format: the 17-value line, the 512-byte sector unit, completion-time counting and the tick fields | Documentation/block/stat.rst:2-5,21-22,71-73,75-80; tag v7.2 | supersedes S180 — The stat file is one line of 17 decimal values; its sector counts use the standard 512-byte sector, not a device or filesystem block size, and grow when an I/O completes; the millisecond wait values can rise faster than 1000 per second when several requests wait. | mined | 2026-10-23 | on-release | corpus/knowledge/disk-write-rate-r33.md |
```

DRAFT corpus/lessons/round-36.md § Gate
```text
| S2NN | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/block/stat.rst (accessed 2026-10-23) | `4c35b795a518ceefea985f11e53b51f71d58fc99bf5a0920ca3738f13c90cb2e` | (5 words) Block layer statistics in /sys/block/<dev>/stat — Documentation/block/stat.rst:2; (17 words) The stat file consists of a single line of text containing 17 decimal values separated by whitespace. — :21-22; (19 words) standard UNIX 512-byte sectors, not any device- or filesystem-specific block size. The counters are incremented when the I/O completes. — :72-73; (17 words) If there are multiple I/O requests waiting, these values will increase at a rate greater than 1000/second; — :79-80 | admit, A, supersedes S180 |
```

## Gates, touched surfaces, and limits

- Source gate: opened URL returned HTTP 200; the four located quotes are within the 25-word limit and match the saved bytes. Gate decision: admit, A; the row verdict above is supported.
- Touched surfaces: this report and scratch artifact `/fast/scratch/hyaku/mori-r36/SupS180/S180.src` only. No product source, registry, lesson, git index, or commit was changed.
- Out of scope: no builds, tests, lint, or unrelated round-36 gates were run; no tools were installed. This assignment required the source check and drafts only.
- Artifact SHA-256: `/fast/scratch/hyaku/mori-r36/SupS180/S180.src` — `4c35b795a518ceefea985f11e53b51f71d58fc99bf5a0920ca3738f13c90cb2e`.
- Report: `.ufo/waves/round-36/w1/SupS180.md`.
