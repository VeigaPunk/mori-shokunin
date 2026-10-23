measured 2026-10-23T07:45:48Z

# AuditToolDocstring — attack on the attempt-2 R2→S180 / R6→S187 correction, then audit of wa/RevToolDocstring.md (mori round 34 wave B, seat MoriR34A3.AuditToolDocstring)

Godspeed axes: **A1** evidence fidelity — every attribution resolved to located quotes in the named source's
committed bytes; **A2** independence — verdict fixed from the primary bytes before the wave-A report was opened;
**A3** audit coverage — every claim the round would cite re-checked and line pointers re-pinned by grep (read-tool
display counts proved off-by-one twice; grep anchors were used as final authority); **A4** containment — writes only
at this report path, lane git read-only, no subagents, no background jobs, no installs (none needed).

## Objects and identity

- Judged object `tools/mori-disk-rate.py`: working-tree sha256 `370932deb525b95135f0c30e4caaf2666b95c6feeffe76b70f06b48c09caa74b`
  equals `git show fd2521351c6cef47384aef30afbe1e4db7e6912e:tools/mori-disk-rate.py | sha256sum`. Blob id
  `c7ea8bdac9c98b8d350a489fb8aca3a4750bcfbf` identical at `ba525e1a…`, `8d56809a…`, `fd25213…` and `HEAD`
  (`git rev-parse <rev>:tools/mori-disk-rate.py`, four identical outputs). All line numbers below are working-tree;
  the file is unchanged since the judged tip. Observation: HEAD is `5216d78d…`, not `fd25213…`; the tool blob is
  identical at both, and `git diff --stat fd25213…` over the tool and S180/S186/S187.src is empty.
- Sources: `corpus/evidence/sources-r33/S180.src` (103 lines), `S186.src` (521), `S187.src` (43);
  `corpus/evidence/sources-r34/S191.src`, `S192.src`, `S193.src`. Identities per `corpus/SOURCES.md:186,192,193`:
  S180 = Documentation/block/stat.rst v7.2; S186 = include/linux/blk_types.h v7.2; S187 = Documentation/ABI/testing/procfs-diskstats v7.2.

## Independent reading (formed from the bytes before opening .ufo/waves/round-34/wa/RevToolDocstring.md)

### Attribution 1 — docstring R2 → S180 (tools/mori-disk-rate.py:38-40)

Docstring R2: "a line is valid only when it holds 14, 18 or 20 tokens and every token other than the device name is
an unsigned decimal; the sectors-written counter is token 10 (S187: field counts and field 10; S180)".

What S180 supports — nothing R2 asserts about /proc/diskstats lines:
- S180's subject is `/sys/block/<dev>/stat`, a different file (S180.src:1-3, "Block layer statistics in
  /sys/block/<dev>/stat … This file documents the contents of the /sys/block/<dev>/stat file").
- "The stat file consists of a single line of text containing 17 decimal values separated by whitespace"
  (S180.src:21-22) — 17 values, not 14/18/20.
- Its "write sectors" is the **7th** table value (row at S180.src:35), not token 10.
- No device-name token exists in that file's line, and the word "unsigned" appears nowhere (grep
  `unsigned|signed` over S180.src: no matches).
Steelman rejected: even S180's "decimal values" phrase describes the sysfs stat line, not diskstats tokens, so it
cannot carry R2's validity rule for the tool's `--a`/`--b` sample lines.

What carries R2 — S187 (procfs-diskstats ABI): "Each line contains the following 14 fields" (S187.src:6-7);
"3 device name" (:12); "10 sectors written" (:19); "Kernel 4.18+ appends four more fields … putting the total at
18" (:26-27); "Kernel 5.5+ appends two more fields for flush requests" with rows 19/20 (:36,:39-40).

VERDICT: R2 → S180 unsupported; R2 → S187 supported (S187 carries R2).

### Attribution 2 — docstring R6 → S187 (tools/mori-disk-rate.py:59-62)

Docstring R6: "the rate of an ``ok`` device is ``(B - A) * 512 * 1000 // interval_ms`` … never zero (S186, S187:
the sector unit is 512 bytes; round-33 rows 4 and 9: an unavailable rate is never a zero rate)".

What S187 supports — no unit statement of any kind: S187.src is 43 lines; full read shows field tables and
"10 sectors written" (:19) with no byte-size; grep `512|unit|byte|size` over S187.src: no matches. It ends
"For more details refer to Documentation/admin-guide/iostats.rst" (S187.src:43) — and even that referred file's
committed copy (S181.src) states no 512-byte unit (grep `512|byte` over S181.src: no matches), so no committed
bytes bridge S187 to the 512 constant.

What carries the unit — S186: "The basic unit of block I/O is a sector. … The size of one sector is 512 = 2**9
bytes. … multiple of 512 bytes" (S186.src:25-28), `SECTOR_SHIFT 9` (:30-31), `SECTOR_SIZE` (:33-34).
(S180.src:71-72 "standard UNIX 512-byte sectors" also states a unit, but for the sysfs stat file's counters.)

VERDICT: R6 → S187 unsupported; R6 → S186 supported (S186 carries the 512-byte unit).

### Contract mirror check and the lesson's framing

The docstring labels repeat the frozen contract's labels: R2 "(S187 field counts and field 10; S180)"
(contract.md:36 ≈ docstring :40; the docstring adds a colon after S187); R6 "(S186/S187 512-byte unit)"
(contract.md:46 ≈ docstring :61). The lesson's "they copy the frozen contract's labels" is accurate; per contract
residual (c) the contradicted mapping is a defect of the claim, not of the judged tool, and the tool is correctly
left unedited (blob identical at ba525e1a = 8d56809a = fd25213 = HEAD). Additive observation, same defect class
and same disposition: the R6 half-citation also appears outside the docstring in the code comment
`SECTOR_BYTES = 512  # R6: the sector unit (S186, S187)` at tools/mori-disk-rate.py:86.

## Audit of .ufo/waves/round-34/wa/RevToolDocstring.md

Independence note: my two verdicts above were fixed from the primary bytes before this report was opened; the
audit below re-verified each of its citable claims against the same bytes, with grep-pinned line numbers.

1. agree — identity claim: sha256 `370932de…` for working tree and `8d56809a…:tools/mori-disk-rate.py`; blob
   `c7ea8bda…` (also equal at ba525e1a/fd25213/HEAD).
2. agree — scope "docstring (lines 31–69)": `"""` opens :2, closes :69; "Rules" header :31, R1 :35 (grep-pinned).
3. agree — Finding 1 substance: S180 documents only /sys/block/<dev>/stat; 17 values (S180.src:21-22); no 14/18/20;
   write sectors is 7th value (row :35); no "unsigned" (grep no matches).
4. agree — S180 table "26-46": header rows :26-28, the 17 value rows :29-45, closing rule :46 (grep-pinned).
5. agree — R2 carrier: S187.src:6-7,19,26-27,36 all pinned. Nit (pointer only): the 5.5+ *total* of 20 appears in
   rows :39-40; :36 is the introducing sentence.
6. agree — SOURCES.md:186 S180 teach cell "The stat file is one line of 17 decimal values …" (row pinned).
7. agree — contract.md:36 carries "(S187 field counts and field 10; S180)"; mapping identical, colon differs.
8. agree — Finding 2 substance: S187 has no unit statement anywhere in its 43 lines (grep no matches).
9. agree — unit stated at S186.src:25-28,30-31 (grep-pinned 26,28,31) and S180.src:71-72 (grep-pinned 72); not by S187.
10. agree — SOURCES.md:193 S187 teach cell carries no unit claim (row pinned).
11. agree — contract.md:46 carries "(S186/S187 512-byte unit)".
12. agree — R1 row: S187.src:12 "3 device name".
13. agree — R5 row: S181.src:33-37 reset sentence ("reset at boot" pinned at :34, sentence spans 34-36 in cited range).
14. agree — R4/R5 rows: S182.src:1371 "if (bdev_is_partition(hd) && !bdev_nr_sectors(hd))" (grep-pinned; `continue;` :1372).
15. agree — R3 row: S182.src:518 unconditional `kobject_create_and_add("slaves", &ddev->kobj)` (read-pinned).
16. agree — R7 row: S183.src:60-64 part_stat_add re-adds to `bdev_whole(part)` (grep-pinned :62-63, macro closes :64);
    `bdev_whole` = `bd_disk->part0` at S186.src:84-85.
17. agree — R3/R7 rows: S192.src:41-50 bd_link_disk_holder comment creates both symlinks; dm-0→sda example :46-50
    (read-pinned within the comment block :34-60).
18. agree — R3 row: S191 part_partition_show ≈:178-182, DEVICE_ATTR(partition) ≈:208, part_type.groups =
    part_attr_groups ≈:264-270 (read windows match all three).
19. agree — R3 row: S193 device_is_not_partition `!(dev->type == &part_type)` ≈:2430-2433; create link iff
    `dev->parent && device_is_not_partition(dev)` ≈:3508-3513; same removal condition ≈:3542-3543 (read windows match).
20. agree — R6 row "r33 rows 4 and 9": disk-write-rate-r33.md:23 (row 4, "never print a negative or wrapped rate")
    and :28 (row 9, "never as zero writes") — both grep-pinned exactly as cited.
21. agree — severity framing: facts remain supported by other cited sources, only attribution labels wrong;
    "a contradicted rule is reported as a defect of the claim" verified at contract.md:87-88.
22. agree — stated gap: only committed copies used; upstream URLs not re-fetched (tag-pinned v7.2 per SOURCES.md).

AUDIT: agree 21 / disagree 0 (one pointer nit on item 5, content agrees; no substantive disagreement)

## Verdicts (summary lines)

VERDICT: docstring R2 → S180 unsupported — S180 (Documentation/block/stat.rst) documents the 17-value
/sys/block/<dev>/stat line and carries no 14/18/20 token counts, no token-10 sectors-written position, and no
unsigned-decimal rule for /proc/diskstats lines (S180.src:1-3,21-22,35).
VERDICT: docstring R6 → S187 unsupported — S187 (procfs-diskstats ABI doc) states no sector byte-unit anywhere in
its 43 lines (S187.src:1-43; grep `512|unit|byte|size` empty).
VERDICT: lesson replacement "S187 carries R2" supported (S187.src:6-7,12,19,26-27,36,39-40).
VERDICT: lesson replacement "S186 carries R6" supported (S186.src:25-28,30-31,33-34).
VERDICT: lesson correction at drafts corpus_lessons_round-34.md:120-121 supported as a whole — attributions
unsupported, contract labels copied (contract.md:36,46), tool left unedited as the judged object (blob identical
across ba525e1a/8d56809a/fd25213/HEAD).

## Residual risk / verification gaps

- All line cites above were re-pinned on committed copies by grep; upstream v7.2 bytes were not re-fetched
  (sources opened by ordinary means only).
- The wa report's R3 kernel-source rows (S191/S192/S193) were spot-checked by read windows, not re-derived
  line-by-line; that surface is outside the lesson item's cited claims and carries residual transcription risk.
- HEAD (`5216d78d…`) is ahead of the declared lane tip `fd25213…`; tool blob and the three source copies are
  unchanged, so this audit's objects are unaffected. [INFERENCE: no other file I cite drifted — verified only for
  the tool and S180/S186/S187 via `git diff --stat fd25213…`.]
- Containment: only this report written in the lane; scratch dir `/fast/scratch/hyaku/mori-r34/a3-AuditToolDocstring/`
  created, unused, empty; no installs (channel n/a); no processes left running; no git/jj writes.
