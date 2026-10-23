# Round 33 wave 1 — sysstat iostat source candidate

## Result and scope

Axes checked: source suitability, claim coverage, byte provenance, and containment. Selected the tag-pinned `iostat.c` URL below. It is a useful partial source for the basic two-sample write-stat path, unit factors, and 32-bit backward-counter branch. It is **not** sufficient by itself to assert the `io_ticks` to `%util` computation or the expansion of `S_VALUE`.

The official sysstat version page identifies 12.8.0 as the latest version (page lines 66-69), lists its release date as 2026-08-28 (line 83), and lists commit `bf343509a2a5a8019e72191ed6858659b868af6e` (line 84): `https://sysstat.github.io/versions.html`. Its saved bytes were 10,691 bytes and SHA-256 `ac712ca04be0cd697ade4abbc738483abf9d9abcb8b6b4e521111bed250455fd` on both fetches (paths and timestamps below). Therefore the chosen source URL is tag-pinned to `v12.8.0`.

## Source retrieval and provenance

Chosen URL: `https://raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c`

| Fetch | Accessed (UTC) | Bytes | SHA-256 | Scratch path |
|---|---|---:|---|---|
| 1 | 2026-10-23T02:40:11Z | 71,360 | `f099229c0051be9538f220d63fe7953247ee947f112d367ff647d791953b9dce` | `/fast/scratch/hyaku/mori-r33/SrcSysstatIostat/iostat-v12.8.0-1.src` |
| 2 | 2026-10-23T02:41:09Z | 71,360 | `f099229c0051be9538f220d63fe7953247ee947f112d367ff647d791953b9dce` | `/fast/scratch/hyaku/mori-r33/SrcSysstatIostat/iostat-v12.8.0-2.src` |

Both `curl --fail` fetches succeeded; `sha256sum` matched byte-for-byte. Exact commands:

```sh
timeout 10s mkdir -p /fast/scratch/hyaku/mori-r33/SrcSysstatIostat && printf 'accessed=' && timeout 3s date -u +%FT%TZ && timeout 70s curl -sSL --fail -m 60 https://raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c -o /fast/scratch/hyaku/mori-r33/SrcSysstatIostat/iostat-v12.8.0-1.src && timeout 10s sha256sum /fast/scratch/hyaku/mori-r33/SrcSysstatIostat/iostat-v12.8.0-1.src && timeout 10s wc -c /fast/scratch/hyaku/mori-r33/SrcSysstatIostat/iostat-v12.8.0-1.src
printf 'accessed=' && timeout 3s date -u +%FT%TZ && timeout 70s curl -sSL --fail -m 60 https://raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c -o /fast/scratch/hyaku/mori-r33/SrcSysstatIostat/iostat-v12.8.0-2.src && timeout 10s sha256sum /fast/scratch/hyaku/mori-r33/SrcSysstatIostat/iostat-v12.8.0-2.src && timeout 10s wc -c /fast/scratch/hyaku/mori-r33/SrcSysstatIostat/iostat-v12.8.0-2.src
```

Tag discovery used the official version page, fetched twice at `2026-10-23T02:41:09Z` and `2026-10-23T02:41:55Z`; each was 10,691 bytes with SHA-256 `ac712ca04be0cd697ade4abbc738483abf9d9abcb8b6b4e521111bed250455fd`. Scratch paths are `/fast/scratch/hyaku/mori-r33/SrcSysstatIostat/sysstat-versions-1.html` and `.../sysstat-versions-2.html`. Exact fetch command was `timeout 70s curl -sSL --fail -m 60 https://sysstat.github.io/versions.html -o <path>` with `date -u +%FT%TZ`, `sha256sum <path>`, and `wc -c <path>` before/after as in the source commands above. An attempted `https://api.github.com/repos/sysstat/sysstat/releases/latest` fetch returned HTTP 404 (`curl` exit 22); no file remained. The official version page, not that API endpoint, is the release evidence.

Exact official version-page fetch commands:
```sh
printf 'accessed=' && timeout 3s date -u +%FT%TZ && timeout 70s curl -sSL --fail -m 60 https://sysstat.github.io/versions.html -o /fast/scratch/hyaku/mori-r33/SrcSysstatIostat/sysstat-versions-1.html && timeout 10s sha256sum /fast/scratch/hyaku/mori-r33/SrcSysstatIostat/sysstat-versions-1.html && timeout 10s wc -c /fast/scratch/hyaku/mori-r33/SrcSysstatIostat/sysstat-versions-1.html
printf 'accessed=' && timeout 3s date -u +%FT%TZ && timeout 70s curl -sSL --fail -m 60 https://sysstat.github.io/versions.html -o /fast/scratch/hyaku/mori-r33/SrcSysstatIostat/sysstat-versions-2.html && timeout 10s sha256sum /fast/scratch/hyaku/mori-r33/SrcSysstatIostat/sysstat-versions-2.html && timeout 10s wc -c /fast/scratch/hyaku/mori-r33/SrcSysstatIostat/sysstat-versions-2.html
```
The helper-file exploration used these exact commands and returned identical hashes and sizes:
```sh
printf 'accessed=' && timeout 3s date -u +%FT%TZ && timeout 70s curl -sSL --fail -m 60 https://raw.githubusercontent.com/sysstat/sysstat/v12.8.0/common.c -o /fast/scratch/hyaku/mori-r33/SrcSysstatIostat/common-v12.8.0-1.src && timeout 10s sha256sum /fast/scratch/hyaku/mori-r33/SrcSysstatIostat/common-v12.8.0-1.src && timeout 10s wc -c /fast/scratch/hyaku/mori-r33/SrcSysstatIostat/common-v12.8.0-1.src
printf 'accessed=' && timeout 3s date -u +%FT%TZ && timeout 70s curl -sSL --fail -m 60 https://raw.githubusercontent.com/sysstat/sysstat/v12.8.0/common.c -o /fast/scratch/hyaku/mori-r33/SrcSysstatIostat/common-v12.8.0-2.src && timeout 10s sha256sum /fast/scratch/hyaku/mori-r33/SrcSysstatIostat/common-v12.8.0-2.src && timeout 10s wc -c /fast/scratch/hyaku/mori-r33/SrcSysstatIostat/common-v12.8.0-2.src
```
The failed API request was `timeout 70s curl -sSL --fail -m 60 https://api.github.com/repos/sysstat/sysstat/releases/latest -o /fast/scratch/hyaku/mori-r33/SrcSysstatIostat/sysstat-latest-release-1.json`; output was HTTP 404 and `curl` exit 22.


The candidate URL was not present in `corpus/SOURCES.md`: `grep` for `sysstat|iostat\.c|rd_stats\.c` and a second search for the exact URL both returned “No matches found.”

## Draft SOURCES row

```text
| SRC | sysstat iostat.c at v12.8.0 — https://raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c | code | A | basic disk write-stat path, display unit factors, and backward-counter handling; not the %util helper formula | iostat.c:1066-1072,1614-1620,1734-1742,1800-1801; tag v12.8.0 | Basic iostat reporting obtains an interval from uptime samples, passes previous/current write-sector samples and that interval to S_VALUE, and divides the resulting write value by fctr in the non-sector display path. The kB and MB factors are 2 and 2*1024. When the current basic write-sector count is below the previous count and the previous count is <=0xffffffff, the code masks the subtraction to 32 bits. Lane rule: do not use this file alone to assert how io_ticks becomes %util. | mined | 2026-10-23 | on-release | corpus/knowledge/disk-write-rate-r33.md |
```

## Draft Gate row

```text
| SRC | https://raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c | 2026-10-23T02:40:11Z | f099229c0051be9538f220d63fe7953247ee947f112d367ff647d791953b9dce | `SRC.src:1800-1801` (14 words): "/* Calculate time interval in 1/100th of a second */ itv = get_interval(uptime_cs[!curr], uptime_cs[curr]);"; `SRC.src:1614-1620` (23 words): "wsectors = S_VALUE(ioj->wr_sectors, ioi->wr_sectors, itv); dsectors = S_VALUE(ioj->dc_sectors, ioi->dc_sectors, itv); if (!DISPLAY_UNIT(flags)) { rsectors /= fctr; wsectors /= fctr; dsectors /= fctr; }"; `SRC.src:1066-1072` (23 words): "if (DISPLAY_KILOBYTES(flags)) { *fctr = 2; units = \"kB\"; spc = \" \"; } else if (DISPLAY_MEGABYTES(flags)) { *fctr = 2 * 1024;"; `SRC.src:1739-1742` (18 words): "wr_sec = ioi->wr_sectors - ioj->wr_sectors; if ((ioi->wr_sectors < ioj->wr_sectors) && (ioj->wr_sectors <= 0xffffffff)) { wr_sec &= 0xffffffff; }" | admit, A, mined |
```

## Numbered facts and their separate quotes

1. **Interval:** the code defines the reporting interval from two uptime samples and comments that the unit is one hundredth of a second. Separate quote: `SRC.src:1800-1801` (14 words): "/* Calculate time interval in 1/100th of a second */ itv = get_interval(uptime_cs[!curr], uptime_cs[curr]);"
2. **Two-sample write value:** basic output passes the previous and current write-sector fields and `itv` to `S_VALUE`; when `DISPLAY_UNIT` is false it divides `wsectors` by `fctr`. Separate quote: `SRC.src:1614-1620` (23 words): "wsectors = S_VALUE(ioj->wr_sectors, ioi->wr_sectors, itv); dsectors = S_VALUE(ioj->dc_sectors, ioi->dc_sectors, itv); if (!DISPLAY_UNIT(flags)) { rsectors /= fctr; wsectors /= fctr; dsectors /= fctr; }" The macro expansion is not in this file, so this quote does not establish the macro's exact arithmetic.
3. **Unit factors:** the kB branch sets `fctr` to 2 and the MB branch sets it to `2 * 1024`; paired with fact 2's division, those are the displayed-unit divisors. Separate quote: `SRC.src:1066-1072` (23 words): "if (DISPLAY_KILOBYTES(flags)) { *fctr = 2; units = \"kB\"; spc = \" \"; } else if (DISPLAY_MEGABYTES(flags)) { *fctr = 2 * 1024;"
4. **Backward basic counter:** the basic path subtracts previous write sectors from current; if current is lower and the previous value is at most `0xffffffff`, it masks the difference with `0xffffffff`. Separate quote: `SRC.src:1739-1742` (18 words): "wr_sec = ioi->wr_sectors - ioj->wr_sectors; if ((ioi->wr_sectors < ioj->wr_sectors) && (ioj->wr_sectors <= 0xffffffff)) { wr_sec &= 0xffffffff; }"

## Not stated by this file

- The `S_VALUE` definition and its exact delta-per-second algebra are not in `iostat.c`; do not claim a literal `delta * 100 / itv` formula from this file alone (`iostat.c:1614-1619`).
- The file does not identify Linux `io_ticks` as its `tot_ticks` field, nor define the `%util` calculation: it copies `ioi->tot_ticks` and `ioj->tot_ticks` and calls `compute_ext_disk_stats` (`iostat.c:1488-1505`), then displays `xds->util / 10.0 / dev_in_grp` (`iostat.c:1211-1215`). The helper implementation is not in this chosen file.
- The file does not explain the kernel meaning or byte size of a sector, map `/proc/diskstats` field numbers, or give the `/sys/block/<dev>/stat` schema. In particular, the factors alone do not prove the kernel's sector definition.
- The basic backward-counter branch does not say whether a decrease is a wrap or reset; it only masks when the previous count is <= `0xffffffff`. It does not describe recovery for a decreasing value with a larger previous count (`iostat.c:1739-1742`).

## Gates, touched surfaces, and limits

- **Gate status:** candidate is byte-stable across two fetches and uses the official latest-release tag. The exact URL was absent from the existing SOURCES registry. The draft is deliberately partial for C1: it must not support an `io_ticks`/`%util` row without a separate source containing that computation.
- **Exploration:** `common.c` at the same tag was fetched twice to scratch (47,807 bytes each; SHA-256 `4aa91c92577ac27970c55b3778e0718a575a17cf86b40d3bbb9ed8d4412eac21`; paths `/fast/scratch/hyaku/mori-r33/SrcSysstatIostat/common-v12.8.0-1.src` and `.../common-v12.8.0-2.src`). A grep for `compute_ext_disk_stats|tot_ticks|wr_sect|S_VALUE|fctr` returned no matches in that file. It is not proposed as a source row. `rd_stats.c` and `common.h` were not opened; the helper location beyond this file is unverified.
- **Touched surfaces:** this report is the only lane-repository write: `.ufo/waves/round-33/w1/SrcSysstatIostat.md`. All fetched bytes and exploratory files remain under `/fast/scratch/hyaku/mori-r33/SrcSysstatIostat/`. No product entry, SOURCES registry, Gate lesson, judge, commit, or test was changed/run; no git/jj write or tool installation occurred.
- **Out of scope:** no full decision table or row judgment was performed; this seat did not verify kernel input semantics or the `%util` helper implementation.
