# FR6 candidate source report — sysfs block ABI

## Behavior
Research and draft only. No product code, source registry, Gate, judge, or corpus entry was changed. The requested tag-pinned path exists and was fetched; no fallback path was needed.

## Gates and provenance
- URL: https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/ABI/stable/sysfs-block
- The fetch command returned the v7.2 `Documentation/ABI/stable/sysfs-block` content. First and second fetch timestamps: `2026-10-23T02:39:51Z` for both.
- First copy: `/fast/scratch/hyaku/mori-r33/MoriR33.SrcSysfsBlockAbi/sysfs-block-1.src`; 35,087 bytes; SHA-256 `bf1a82aeb1ecee73d6e80d0fa66f1da984dbc54efbb2e9a24c77edd0f807db61`.
- Second copy: `/fast/scratch/hyaku/mori-r33/MoriR33.SrcSysfsBlockAbi/sysfs-block-2.src`; 35,087 bytes; SHA-256 `bf1a82aeb1ecee73d6e80d0fa66f1da984dbc54efbb2e9a24c77edd0f807db61`. The byte sizes and hashes match.
- `grep` on `corpus/SOURCES.md` for the exact raw URL returned `No matches found`; no existing URL collision was observed.
- Quote locators below refer to the first saved copy. Whitespace is normalized only. These are four Gate excerpts, each within the required 3–25-word range.
- No tools were installed or updated. No git/jj commands, tests, or judge/counter runs were performed.

## Draft SOURCES row
```text
| SRC | Linux v7.2 stable sysfs-block ABI — https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/ABI/stable/sysfs-block | docs | A | Linux v7.2 disk and partition stat, inflight fields, and queue block-size ABI | Documentation/ABI/stable/sysfs-block:90-99,212-218,386-390,476-481,679-689,914-941; tag v7.2 | Disk stat labels the write-sector count and write duration in milliseconds; partition stat uses the disk-stat format; inflight has separate read/write request fields; physical block size may exceed logical block size. | mined | 2026-10-23 | on-release | corpus/knowledge/disk-write-rate-r33.md |
```

## Draft Gate row
```text
| SRC | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/ABI/stable/sysfs-block | 2026-10-23T02:39:51Z | bf1a82aeb1ecee73d6e80d0fa66f1da984dbc54efbb2e9a24c77edd0f807db61 | `SRC.src:928-929` (8 words): "7  sectors written 8  time spent writing (ms)"; `SRC.src:216-218` (20 words): "The /sys/block/<disk>/<partition>/stat files display the I/O statistics of partition <partition>. The format is the same as the format of /sys/block/<disk>/stat."; `SRC.src:97-98` (14 words): "The report contains 2 fields: one for read requests and one for write requests."; `SRC.src:684-685` (13 words): "It is usually the same as the logical block size but may be bigger." | admit, A, mined |
```

## Decision-table facts supported by those quotes
1. The disk stat entry labels its seventh value as a written-sector count and its eighth value as writing time in milliseconds. Quote: `SRC.src:928-929` above.
2. The partition stat entry describes partition I/O and reuses the disk-stat format. Quote: `SRC.src:216-218` above.
3. The inflight entry has distinct read-request and write-request fields. Quote: `SRC.src:97-98` above; its containing ABI entry is identified at `SRC.src:90`.
4. The physical-block description allows the physical unit to be larger than the logical unit. Quote: `SRC.src:684-685` above; its entry heading is at `SRC.src:679`.

The file has separate queue entries for `hw_sector_size` (`SRC.src:386-390`), `logical_block_size` (`SRC.src:476-481`), and `physical_block_size` (`SRC.src:679-689`). The Gate row's fourth excerpt addresses the physical/logical relationship; these observations are recorded for source coverage, not as additional Gate quotes or teaches-cell claims:

- The hardware-sector attribute gives the device's hardware sector size in bytes (`SRC.src:386-390`).
- The logical-block attribute describes the smallest unit the device can address and says it is typically 512 bytes (`SRC.src:476-481`).
- The physical-block attribute describes the smallest physical write unit that can be written atomically (`SRC.src:683-685`).

## Not stated / limits
- These excerpts do not give a byte conversion for the stat's `sectors written` value, nor state whether that unit equals or differs from the logical, physical, or hardware sector sizes. The distinct queue entries are at `SRC.src:386-390,476-481,679-689`; the stat write labels are at `SRC.src:928-929`. Therefore this source alone does not establish the requested claim that the stat unit is not the device block size.
- The cited text does not provide a write-rate formula, sampling interval, counter-wrap/reset handling, or whether to combine partition and whole-disk observations. The partition entry states the same format (`SRC.src:212-218`) but does not state a double-counting rule.
- The stat section contains an internal field-count conflict: line 919 says verbatim, `They contain 11 fields:`; the same list labels fields 12–17 at lines 933–938. The draft does not rely on the disputed total.
- The inflight excerpt says there are separate read/write fields; the file's fuller description says they count requests currently in progress, not completed writes (`SRC.src:94-99`). Inflight should not be treated as a write-completion counter.

## Commands and outcomes
1. `timeout 20 mkdir -p /fast/scratch/hyaku/mori-r33/MoriR33.SrcSysfsBlockAbi` — completed with no output.
2. First fetch: `date -u +%FT%TZ && timeout 70 curl -sSL --fail -m 60 https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/ABI/stable/sysfs-block -o /fast/scratch/hyaku/mori-r33/MoriR33.SrcSysfsBlockAbi/sysfs-block-1.src && sha256sum /fast/scratch/hyaku/mori-r33/MoriR33.SrcSysfsBlockAbi/sysfs-block-1.src && wc -c /fast/scratch/hyaku/mori-r33/MoriR33.SrcSysfsBlockAbi/sysfs-block-1.src` — timestamp `2026-10-23T02:39:51Z`; hash above; `35087` bytes.
3. Second fetch used the same command and URL, output path `.../sysfs-block-2.src` — timestamp `2026-10-23T02:39:51Z`; same hash; `35087` bytes.
4. Source-registry search: `grep` for `https://raw\.githubusercontent\.com/torvalds/linux/v7\.2/Documentation/ABI/stable/sysfs-block` in `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md` — no matches.
5. Inspected saved source ranges `89-108`, `212-219`, `386-399`, `476-493`, `679-694`, and `914-950`; relevant line references are recorded above. No tests, counter, or judge were run.

## Touched surfaces and artifacts
- Report written: `.ufo/waves/round-33/w1/SrcSysfsBlockAbi.md`.
- Scratch copies: `/fast/scratch/hyaku/mori-r33/MoriR33.SrcSysfsBlockAbi/sysfs-block-1.src` and `sysfs-block-2.src`.
- No other lane files were written or modified.
