# AttackRow01 — row 1, sector unit

Scope: `corpus/knowledge/disk-write-rate-r33.md:19`, measured revision `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8`; working-tree copies read under the assignment's identical-files assurance. Findings only; no counted judgment or lane edits.

Axes: depth (the C1 source-support claim), calibration (distinguishing a correct Linux fact from a complete cited proof). The frozen requirements are R-J at `.ufo/waves/round-33/contract.md:44-50` and A1 at `:119-123`.

Path abbreviations below: `S###.src` means `corpus/evidence/sources-r33/S###.src`; `entry` means `corpus/knowledge/disk-write-rate-r33.md`; `lesson` means `corpus/lessons/round-33.md`.

## Per-fact audit

| fact | quote or NOT STATED | file:line |
|---|---|---|
| Observation: the record is from `/proc/diskstats`. | "The /proc/diskstats file displays the I/O statistics of block devices." | S187.src:5-6 |
| Observation: its field 10 counts sectors written. | "10 sectors written" | S187.src:19 |
| Reading: the sector is the kernel's basic block-I/O unit. | "The basic unit of block I/O is a sector." The next line explicitly places the contexts in Linux. | S186.src:25-26 |
| Reading: the sector size is 512 bytes. | "standard UNIX 512-byte sectors"; the header also says "The size of one sector is 512 = 2**9", followed by the comment line `* bytes.` | S180.src:72; S186.src:26-27 |
| Reading: 512 bytes equals 2**9 bytes. | "The size of one sector is 512 = 2**9"; the next comment line supplies "bytes." No contiguous `2**9 bytes` quotation is claimed. | S186.src:26-27 |
| Reading: **each unit counted there**, specifically `/proc/diskstats` field 10, uses that 512-byte unit. | **NOT STATED as an explicit interface-to-unit binding by the row's three cited pages.** S187 labels the field without defining its unit; S186 defines the kernel block-I/O sector generally; S180 states the unit for sysfs stat. The direct interface bridge is in uncited S181. | S187.src:5-19; S186.src:24-35; S180.src:2-5,67-73; S181.src:22-25 |
| Reading: that `/proc/diskstats` unit does not follow the device's own block size. | S180 says "not any device- or filesystem-specific block size", **but for its sysfs stat counters**. **NOT STATED for the proc field without the same missing bridge.** | S180.src:2-5,70-73 |
| Reading: that `/proc/diskstats` unit does not follow the filesystem's own block size. | The same explicit sysfs exclusion, with the same proc-binding gap; this is not an independent numerical error. | S180.src:2-5,70-73 |

The currently cited Gate quotes are all present in the inspected surroundings: S180 at `lesson:15` / `S180.src:21-22,67-82`; S186 at `lesson:21` / `S186.src:24-35`; S187 at `lesson:22` / `S187.src:1-43`.

## Finding F1 — missing explicit proc/sysfs proof bridge

**Severity: major (strict quote-support defect, not a demonstrated wrong conversion).**

Attack: `entry:19` cites only S187, S180 and S186. S180 expressly documents `/sys/block/<dev>/stat` (`S180.src:2-5`), while S187 gives the proc field label but no byte unit (`S187.src:5-19`). S186 describes a basic kernel sector in the blk/bio/genhd contexts, not the proc export format (`S186.src:24-35`). Treating the general sector definition as proof that this ABI exports that unit, rather than rescaling it, is the unstated connection.

[INFERENCE] The strongest support counterexample is a hypothetical exporter that prints device-native sector counts in proc while leaving sysfs and internal kernel sectors at 512 bytes. The three quoted descriptions do not explicitly rule out that export-time rescaling. This is a test of the cited proof, not a claim that Linux v7.2 actually does that.

The repository contains the missing explicit statement: "Both files contain the same 17 statistics" followed by the sysfs name and proc prefix explanation (`S181.src:22-25`, interfaces named at `:5-6`). Its seven-word Gate quote already exists at `lesson:16`. However, row 1 does not cite S181 (`entry:19`), and R-J forbids rescue through an uncited source (`.ufo/waves/round-33/contract.md:47-50`). This is a fixable citation-chain defect, not an axis tradeoff or a claim that sector arithmetic is false.

### Smallest safe correction

Keep the observation, reading and verdict unchanged; change only row 1's source cell:

`S187, S180, S186` → `S187, S180, S186, S181`.

The added committed quote supplies precisely the missing interface bridge (`S181.src:22-25`; `lesson:16`). No new source, Gate, or semantic rewrite is needed. This is a proposal only; I made no entry edit.

## Verdict-follows check

**Yes, from the reading as written.** With a fixed 512-byte unit, a sector-count difference converts to a byte difference by multiplication by 512; this is arithmetic, not an additional sampling or kernel fact. "Not any device- ... block size" covers both logical and physical device block sizes (`entry:19`; `S180.src:71-73`). The wording does not require those sizes to differ numerically from 512. The proof gap is in support for the reading's proc binding, not in this deduction.

## Attempts to break the actual unit

- **Different device block sizes:** S180 explicitly excludes any device- or filesystem-specific size (`S180.src:70-73`). The request-accounting implementation adds `bytes >> 9` (`S185.src:856-863`). [INFERENCE] A 4096-byte accounted request therefore contributes eight units, not one 4096-byte unit. This attempted numerical counterexample does not break the intended conversion. S185 is corroboration for this attack, not retroactive support credited to row 1.
- **An export-time rescaling path:** the proc printer emits `stat.sectors[STAT_WRITE]` directly (`S182.src:1380-1392`); the sysfs printer emits that same member (`S182.src:1071-1086`). No rescaling appears in those inspected paths. This refutes the hypothetical exporter for these actual paths, but S182 is also not cited by row 1.
- **A non-request accounting path:** `bio_end_io_acct_remapped` passes `bio_sectors(bio)` into `bdev_end_io_acct`, which adds its sector argument (`S184.src:1100-1121`). The header explicitly includes bio among the 512-byte-sector contexts (`S186.src:25-28`). No different unit was found in this inspected path. I did not exhaustively audit every driver's accounting caller.
- **Unaccounted requests:** the request path is gated by `RQF_IO_STAT` (`S185.src:858-862`). Row 1 says how each counted unit is sized, not that every write is counted (`entry:19`), so this restriction does not contradict it.
- **Version boundary:** the ABI source says discard and flush fields are appended in 4.18+ and 5.5+ (`S187.src:26-40`), not inserted before field 10. Row 1 gives no additional historical boundary; the entry scopes facts to v7.2 (`entry:55-56`). No field-10 unit or index contradiction was found in the inspected version text.

## Six-consecutive-word check

**No six-word overlap found.** I manually lowercased and split the reading and every cited Gate quote into runs of letters, digits and underscores, as required by A1 (`.ufo/waves/round-33/contract.md:119-123`; implementation `.ufo/waves/round-33/count-c1-a1.py:86-87`). Compared the reading at `entry:19` against every quote in `lesson:15,21-22`. For example, reading `basic block i o unit` is not Gate `basic unit of block i o`; reading `512 byte sector` is not Gate `512 byte sectors`. This was a manual text check, not a counter or judge execution.

## Checks and limits

Read the full three cited source passages and their surroundings; searched those source copies for sector, size, unit and diskstats references; inspected the corroborating printer and accounting paths cited above; read Amendment A1 and the counter's tokenization definition. No public fetch, host disk probe, build, test, counter, judge, git/jj write, or additional runtime was invoked. No tools were installed or updated. Only this scoped report was written; no process was started that requires cleanup.
