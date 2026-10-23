# SrcSectorSize — FR6 candidate source

## Behavior and axes

- **Observed source facts:** Linux v7.2 `include/linux/blk_types.h` describes a sector as the basic block-I/O unit, says its size is 512 = 2**9 bytes, defines `SECTOR_SHIFT` as 9 and `SECTOR_SIZE` as `1 << SECTOR_SHIFT`, and says `sector_t` offsets/sizes are multiples of 512 bytes (`blk_types.src:24-35`).
- **Axis movement:** improves FR6 source authority, quote-level support, and byte-reproducible provenance. No adverse effect observed; no decision-table row was drafted here.
- The comment gives the 512-byte sector size, but does **not explicitly say** “always regardless of device block size” or compare sector size with a device logical/physical block size (`blk_types.src:24-35`).

## Source and gates

- **URL:** https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/blk_types.h
- **Path check:** exact URL search in `corpus/SOURCES.md` returned “No matches found”; this URL was not already registered. The requested v7.2 path fetched successfully and contains the definitions, so no alternate path was needed.
- **Accessed:** first fetch timestamp `2026-10-23T02:39:40Z`; second fetch timestamp `2026-10-23T02:39:48Z` (both `date -u +%FT%TZ` outputs).
- **Byte size:** 16,897 bytes on both fetches.
- **SHA-256, fetch 1:** `adff86f6d9433c496dc5ddf32d0e353a24969af7ed90191dffc562f1998b2e6e`
- **SHA-256, fetch 2:** `adff86f6d9433c496dc5ddf32d0e353a24969af7ed90191dffc562f1998b2e6e` (identical).
- **Scratch files:** `/fast/scratch/hyaku/mori-r33/SrcSectorSize/blk_types.src` and `/fast/scratch/hyaku/mori-r33/SrcSectorSize/blk_types-second.src`. Both contain the fetched bytes; neither was edited.

Commands and outcomes:

```sh
mkdir -p /fast/scratch/hyaku/mori-r33/SrcSectorSize && date -u +%FT%TZ && timeout 60 curl -sSL --fail -m 60 https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/blk_types.h -o /fast/scratch/hyaku/mori-r33/SrcSectorSize/blk_types.src && wc -c /fast/scratch/hyaku/mori-r33/SrcSectorSize/blk_types.src && sha256sum /fast/scratch/hyaku/mori-r33/SrcSectorSize/blk_types.src
# 2026-10-23T02:39:40Z; 16897 bytes; adff86f6d9433c496dc5ddf32d0e353a24969af7ed90191dffc562f1998b2e6e

date -u +%FT%TZ && timeout 60 curl -sSL --fail -m 60 https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/blk_types.h -o /fast/scratch/hyaku/mori-r33/SrcSectorSize/blk_types-second.src && wc -c /fast/scratch/hyaku/mori-r33/SrcSectorSize/blk_types-second.src && sha256sum /fast/scratch/hyaku/mori-r33/SrcSectorSize/blk_types-second.src
# 2026-10-23T02:39:48Z; 16897 bytes; adff86f6d9433c496dc5ddf32d0e353a24969af7ed90191dffc562f1998b2e6e
```

The literal URL search used the specialized search tool against `corpus/SOURCES.md` and returned no matches. No packages or tools were installed or updated; `/home/vgpnk/.omp/agent/RULES.md` was read as required.

### Draft SOURCES row (placeholder `SRC` for L1 assignment)

```text
| SRC | Linux include/linux/blk_types.h at v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/blk_types.h | code | A | Linux v7.2 block-sector unit and SECTOR_SHIFT/SECTOR_SIZE definitions | include/linux/blk_types.h:24-35; tag v7.2 | The header states that a sector is 512 = 2**9 bytes and sector_t offsets/sizes are multiples of 512 bytes; it defines SECTOR_SHIFT as 9 and SECTOR_SIZE as (1 << SECTOR_SHIFT). | mined | 2026-10-23 | on-release | corpus/knowledge/disk-write-rate-r33.md |
```

### Draft Gate row (placeholder `SRC` for L1 assignment)

```text
| SRC | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/blk_types.h | 2026-10-23T02:39:40Z | adff86f6d9433c496dc5ddf32d0e353a24969af7ed90191dffc562f1998b2e6e | `SRC.src:26` (10 words): "The size of one sector is 512 = 2**9 bytes."; `SRC.src:27-28` (16 words): "Variables of type sector_t represent an offset or size that is a multiple of 512 bytes."; `SRC.src:31` (3 words): "#define SECTOR_SHIFT 9"; `SRC.src:34` (5 words): "#define SECTOR_SIZE (1 << SECTOR_SHIFT)" | admit, A, mined |
```

## Numbered fact list

Each paraphrase below is separated from its literal supporting quote.

1. **Fact:** The header assigns 9 to the sector-shift constant. Quote: `` `SRC.src:31` (3 words): "#define SECTOR_SHIFT 9" ``.
2. **Fact:** The sector-size constant is expressed as one shifted left by the sector-shift constant. Quote: `` `SRC.src:34` (5 words): "#define SECTOR_SIZE (1 << SECTOR_SHIFT)" ``.
3. **Fact:** The header comment gives one sector a size of 512 bytes and equates 512 with 2**9. Quote: `` `SRC.src:26` (10 words): "The size of one sector is 512 = 2**9 bytes." ``.
4. **Fact:** `sector_t` offsets and sizes use multiples of 512 bytes. Quote: `` `SRC.src:27-28` (16 words): "Variables of type sector_t represent an offset or size that is a multiple of 512 bytes." ``.

## Not stated / scope limits

- The header does not explicitly compare the kernel sector unit to device logical or physical block size, nor say in those words that it is always 512 bytes regardless of either block size. Do not attribute that comparison to this quote.
- It does not describe `/proc/diskstats` or `/sys/block/<dev>/stat` field positions, field units, or which field measures written sectors.
- It does not prescribe bytes-per-second conversion, sampling interval, write completion/accounting semantics, counter wrap/reset handling, or disk/partition/stacked-device aggregation.
- It gives source code for Linux v7.2, not evidence of the running host kernel or a runtime measurement.

## Touched surfaces, gates, and out-of-scope

- **Lane file written:** this report only, `.ufo/waves/round-33/w1/SrcSectorSize.md`. The requested SOURCES and Gate content is a draft here; no registry, lesson, or knowledge entry was changed.
- **Scratch files written:** the two downloads listed above, under the authorized seat scratch directory.
- **Not run:** the round counter, tests, builds, or runtime probes. This seat did not judge a decision table or claim C1 is met.
- **Tooling:** no install/update; no package/version/channel change to report.
- **Limit:** the source supports the sector-size facts only. Any diskstats/stat interpretation or reporting rule requires other cited evidence.
