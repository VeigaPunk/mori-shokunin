measured 2026-10-23T05:39:36Z
# RevToolDocstring — citation attack on tools/mori-disk-rate.py R1–R7 docstring

Scope: each cited source id (S180–S193) in the docstring of
tools/mori-disk-rate.py (lines 31–69) was checked against the committed source
copies: corpus/evidence/sources-r33/S1{80..90}.src and
corpus/evidence/sources-r34/S191..S193.src. The working-tree tool is
byte-identical to the judged tip (sha256 370932deb525b95135f0c30e4caaf2666b95c6feeffe76b70f06b48c09caa74b for both
8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3:tools/mori-disk-rate.py and the
working file), so the docstring analyzed is the judged object's text.

## Findings (severity order)

### Finding 1 — R2 cites S180 for claims S180 does not state (unsupported)
Docstring R2: "a line is valid only when it holds 14, 18 or 20 tokens and every
token other than the device name is an unsigned decimal; the sectors-written
counter is token 10 (S187: field counts and field 10; S180)".
Evidence: S180.src (Documentation/block/stat.rst v7.2) documents only the
/sys/block/<dev>/stat file: "The stat file consists of a single line of text
containing 17 decimal values separated by whitespace" (S180.src:21) with a
17-field table (S180.src:26-46). It states no /proc/diskstats token counts
(14/18/20; note its 17 values are the *sysfs* file, not diskstats), no token
position for sectors written (write sectors is the 7th value in its table,
S180.src:35), and no "unsigned" property. The 14/18/20 counts and token 10 are
stated by S187 (S187.src:6-7,19,26-27,36); S180 adds no support for any R2
claim. SOURCES.md row S180's own teach cell agrees ("The stat file is one line
of 17 decimal values …"). The identical label "(S187 field counts and field 10;
S180)" is in the frozen contract (contract.md:36), so the docstring faithfully
mirrors the claim's own attribution — the defect is the claim's source mapping,
not a tool/contract divergence.

### Finding 2 — R6 cites S187 for the 512-byte sector unit S187 does not state (unsupported)
Docstring R6: "… (B - A) * 512 * 1000 // interval_ms … (S186, S187: the sector
unit is 512 bytes; …)".
Evidence: S187.src (Documentation/ABI/testing/procfs-diskstats v7.2) enumerates
field tables for 14/18/20 fields (S187.src:6-41) and names "10 sectors written"
(S187.src:19) but contains no statement of any unit/size for a sector. The
512-byte unit is stated by S186.src:26-28 ("The size of one sector is 512 =
2**9 bytes", SECTOR_SHIFT 9 at S186.src:30-31) and by S180.src:71-72
("standard UNIX 512-byte sectors"), not by S187. SOURCES.md row S187's teach
cell likewise carries no unit claim. Contract.md:46 carries the same "S186/S187
512-byte unit" label.

Both findings are low severity: the *facts* the rules encode remain supported by
other cited sources (R2's counts/token 10 by S187; R6's unit by S186 [and
S180]), so no rule behaviour is invalidated; only the per-source attribution
labels are wrong.

## Per-citation verdicts

| Rule | Citation | Verdict | Supporting line |
|---|---|---|---|
| R1 | S187: device name as field 3 | supported | S187.src:12 ("3 device name"); skip of <3-token lines follows from field 3 being name |
| R2 | S187: field counts and field 10 | supported | S187.src:6-7 (14), 19 (field 10 sectors written), 26-27 (4.18+ → 18), 36 (5.5+ → 20) |
| R2 | S180 | unsupported | S180.src:21 (17 values, sysfs stat file) states none of the attributed claims |
| R3 | S191: partition-only attribute | supported | S191.src:178-182,208,221-246,266-270 (DEVICE_ATTR(partition); part_attrs; part_attr_groups on part_type) |
| R3 | S192: slaves/holders links | supported | S192.src:41-50 (bd_link_disk_holder creates both symlinks; dm-0→sda example) |
| R3 | S182: creates slaves for every disk | supported | S182.src:518-522 (slaves_dir = kobject_create_and_add("slaves", …) in __add_disk, unconditional) |
| R3 | S193: device link only for non-partition with parent | supported | S193.src:3508-3513 (sysfs_create_link("device") iff dev->parent && device_is_not_partition), 2430-2433 (device_is_not_partition = type != part_type), 3542-3543 (same removal condition) |
| R4 | S182: kernel skips zero-size partitions when printing | supported | S182.src:1371 ("if (bdev_is_partition(hd) && !bdev_nr_sectors(hd)) continue;") |
| R5 | S182: skips zero-size partitions | supported | S182.src:1371 |
| R5 | S181: counters set back on reinitialisation | supported | S181.src:33-37 ("The remaining fields reset at boot, on device reattachment or reinitialization, or when the underlying counter overflows") |
| R6 | S186: sector unit 512 bytes | supported | S186.src:24-28,30-31 |
| R6 | S187: sector unit 512 bytes | unsupported | S187.src has no unit statement anywhere (lines 1-43) |
| R6 | round-33 rows 4 and 9: unavailable ≠ zero | supported | corpus/knowledge/disk-write-rate-r33.md:23 (row 4: never print negative/wrapped rate), :28 (row 9: missing line reported unavailable, never zero writes) |
| R7 | S183: partition sectors added to whole disk | supported | S183.src:60-64 (part_stat_add re-adds to bdev_whole(part) when bdev_is_partition; bdev_whole = bd_disk->part0, S186.src:84-85) |
| R7 | S192: stacked device maps onto devices already counted | supported (mapping fact) | S192.src:46-50 (dm-0 maps sda; symlinks); "already counted"/dedup is the tool's own host_basis integration (lane rule) |

VERDICT: R1 supported; R2 S187 supported, S180 unsupported; R3 supported; R4
supported; R5 supported; R6 S186 supported, S187 unsupported, r33 rows 4/9
supported; R7 supported. Judge-object citation surface: defect (two unsupported
attributions, R2/S180 and R6/S187).

## Residual risk / verification gaps
- The two unsupported attributions exactly mirror the frozen contract labels
  (contract.md:36,46); they are claim-level source-mapping defects, consistent
  with contract residual (c) ("a contradicted rule is reported as a defect of
  the claim"). No fix is applied here (detection only).
- S180's 17-value sysfs stat doc was not checked against the tool's offline
  --a/--b input handling (the tool reads diskstats lines, not stat files); the
  R2 validity rule applies to diskstats tokens, so S180 remains outside the
  rule's subject.
- "unsigned decimal" token validity has no direct S-id support beyond S187's
  field enumeration (fields are counts/numbers); treated as lane/tool rule,
  not attributable to S180.
- Only committed copies under corpus/evidence/sources-r33/r34 were used;
  upstream URLs were not re-fetched (tag-pinned at v7.2 per SOURCES.md).
