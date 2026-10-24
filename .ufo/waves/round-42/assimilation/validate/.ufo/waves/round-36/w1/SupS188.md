measured 2026-10-23T12:05:28Z

# SupS188 — routed SOURCES append-only defect 2

## Behavior and finding

`ScoutAppendDebt.md:45` identifies S188 as changed at `ab8f4cfe` in scope, anchor, and teaches, with the new scope about disk-executed flush requests and zero-size writes, anchor lines 9, 11, 71-72, and teaches about fields 16-17. `git log --format='%H %s' --follow -S'| S188 |' -- corpus/SOURCES.md` returned `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8` as the first-publish commit. At that commit, S188's scope was flush requests executed by the disk after block-layer merging and not tracked for partitions; its anchor was patch lines 9, 11, and 72; its teaches said flush counters count disk-executed flushes, are not tracked for partitions, and are usually triggered by barriers or zero-size writes (`git show 62db24c01d5b7c2247f43852ea2b28d0ae5e40c8:corpus/SOURCES.md | grep '^| S188 '`).

Tip row read as requested: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 6bd57097:corpus/SOURCES.md | grep '^| S188 '` returned source URL `https://github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch`, scope `what the flush counters count: flush requests executed by the disk, which the block layer combines; not tracked for partitions; triggered by requests that are usually zero-size writes`, anchor `patch lines 9,11 (commit message) and 71-72 (iostats.rst hunk)`, and teaches `The flush counters (fields 16-17 in iostats numbering) count flush requests executed by the disk; the block layer combines flush requests and executes at most one at a time; they are not tracked for partitions; requests that trigger flushes are usually barriers, zero-size writes.`

Re-opened that exact URL with curl; HTTP status 200. The saved copy is 8,897 bytes, sha256 `a844836a15c04bfb15f44f7398851074d901afff5206509ea9be661ac5758d89` (`/fast/scratch/hyaku/mori-r36/SupS188/S188.src`). The patch says Field 16 counts flush requests completed successfully (`S188.src:68-69`) and Field 17 is milliseconds spent flushing, totaling milliseconds spent by all flush requests (`S188.src:74-75`). Thus the tip teaches' assertion that fields 16-17 count requests is false for field 17; the scope's broad `what the flush counters count` has the same overreach. The other checked assertions are supported: merging and at most one at a time (`S188.src:9-10,71`), execution by disk and no partition tracking (`:10,72`), and usual barrier/zero-size triggers (`:6,11`). The corrected row separates the field-16 request count from field-17 duration and expands the anchor to include the field definitions.

VERDICT: unsupported

## Gates

The re-opened patch supports the corrected superseding row, so its Gate decision is `admit, A`; it does not support the uncorrected S188 field-17 count claim. Quotes below are contiguous from the saved copy and each is under 25 words (`S188.src:9-11,68-75`).

## Drafts

DRAFT corpus/SOURCES.md
```text
| S2NN | Linux commit b6866318 block: add iostat counters for flush requests (patch view) — https://github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch | code | A | what iostats fields 16-17 mean: field 16 counts flush requests completed successfully and executed by the disk; field 17 is the total milliseconds spent by all flush requests; the block layer combines flush requests and executes at most one at a time; field 16 is not tracked for partitions; requests that trigger flushes are usually barriers, zero-size writes | patch lines 9-11 (commit message) and 68-75 (iostats.rst hunk) | supersedes S188 — In iostats numbering, field 16 counts flush requests completed successfully and executed by the disk; field 17 is the total milliseconds spent by all flush requests. The block layer combines flush requests and executes at most one at a time; field 16 is not tracked for partitions. Requests that trigger flushes are usually barriers, zero-size writes. | mined | 2026-10-23 | on-release | corpus/knowledge/disk-write-rate-r33.md |
```

DRAFT corpus/lessons/round-36.md
```text
| S2NN | https://github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch | 2026-10-23 | a844836a15c04bfb15f44f7398851074d901afff5206509ea9be661ac5758d89 | Block layer has sophisticated engine for combining several flush requests into one. But there is no statistics for actual flushes executed by disk. — S188.src:9-10; Requests which trigger flushes usually are barriers - zero-size writes. — :11; Field 16 -- # of flush requests completed This is the total number of flush requests completed successfully. — :68-69; Block layer combines flush requests and executes at most one at a time. This counts flush requests executed by disk. Not tracked for partitions. — :71-72; Field 17 -- # of milliseconds spent flushing This is the total number of milliseconds spent by all flush requests. — :74-75 | admit, A; corrected row separates field 16 count from field 17 duration |
```

## Gates, touched surfaces, and limits

- The proposed used-by file exists at tip: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree --name-only 6bd57097 corpus/knowledge/disk-write-rate-r33.md` returned `corpus/knowledge/disk-write-rate-r33.md`.
- Touched by this seat: this report and scratch copy `/fast/scratch/hyaku/mori-r36/SupS188/S188.src` only. Lane source, lesson, and Git index were read-only; no code, source row, lesson, or index was changed.
- No tool was installed. No build, test, linter, or formatter was run. No second fetch was made; the hash is for the single HTTP-200 response saved above.
- The new row id remains the requested placeholder `S2NN`; no lane integration or publication was performed.

## Provenance commands

- `timeout 10s git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 6bd57097:corpus/SOURCES.md | grep '^| S188 '` → tip row quoted above.
- `timeout 15s git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --format='%H %s' --follow -S'| S188 |' -- corpus/SOURCES.md` → `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8 round-33: C1 FR6 entry, sources S180-S190, round-32 repair, QUALITY 97, wave-1 reports`.
- `timeout 10s git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 62db24c01d5b7c2247f43852ea2b28d0ae5e40c8:corpus/SOURCES.md | grep '^| S188 '` → first-published cells summarized above.
- `mkdir -p /fast/scratch/hyaku/mori-r36/SupS188 && timeout 40s curl -L -sS --max-time 35 -w 'HTTP_STATUS=%{http_code}\n' -o /fast/scratch/hyaku/mori-r36/SupS188/S188.src 'https://github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch' && timeout 10s sha256sum /fast/scratch/hyaku/mori-r36/SupS188/S188.src` → `HTTP_STATUS=200`; `a844836a15c04bfb15f44f7398851074d901afff5206509ea9be661ac5758d89  /fast/scratch/hyaku/mori-r36/SupS188/S188.src`.
- `timeout 10s wc -c /fast/scratch/hyaku/mori-r36/SupS188/S188.src` → `8897 /fast/scratch/hyaku/mori-r36/SupS188/S188.src`.
- `timeout 10s git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree --name-only 6bd57097 corpus/knowledge/disk-write-rate-r33.md` → `corpus/knowledge/disk-write-rate-r33.md`.

## Artifact paths

- Report: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/w1/SupS188.md`
- Re-opened source: `/fast/scratch/hyaku/mori-r36/SupS188/S188.src` (8,897 bytes; sha256 above)
