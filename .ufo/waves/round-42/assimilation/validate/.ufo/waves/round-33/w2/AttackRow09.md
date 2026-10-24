# AttackRow09 — zero-sector partition omission

Reviewed the assigned row at measured revision `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8`, using the supplied identical working-tree files. This is a critic report, not the canonical judge's receipt.

## Axes and scope

- Depth / FR6: whether the omission rule and reporting consequence are actually established.
- Freshness: whether the v7.2 source or another printing path narrows the rule.
- Calibration: distinguish a conditional source rule from an observed fact about this host.

These are the axes named in `.ufo/waves/round-33/contract.md:12-15`. R-J is at `contract.md:44-50`; Amendment A1 is at `contract.md:119-123` (both paths under `.ufo/waves/round-33/`).

Attack target: `corpus/knowledge/disk-write-rate-r33.md:27`. It cites only S182. Its Gate row is `corpus/lessons/round-33.md:17`; source identity/version is `corpus/SOURCES.md:188`.

Below, `S182.src` means `corpus/evidence/sources-r33/S182.src`.

## Per-fact audit

| fact | quote or NOT STATED | file:line |
|---|---|---|
| Observation: this particular host actually has such a partition | **NOT STATED**. The cited page is kernel implementation, not a host inventory or observation. The code establishes a conditional omission rule, not an occurrence on this host. | Row wording: `corpus/knowledge/disk-write-rate-r33.md:27`; conditional code: `S182.src:1370-1372` |
| Observation: a partition entry can be skipped without receiving its own `/proc/diskstats` line | `if (bdev_is_partition(hd) && !bdev_nr_sectors(hd)) continue;` The `continue` precedes the line emitters, including `seq_printf(seqf, " %pg", hd);` and the terminating `seq_putc(seqf, '\n');`. | `S182.src:1371-1372,1381-1383,1409` |
| Reading: the condition is evaluated during generation of this file | `static int diskstats_show(struct seq_file *seqf, void *v)`; `.show = diskstats_show`; `proc_create_seq("diskstats", 0, NULL, &diskstats_op);` | `S182.src:1353,1420,1425` |
| Reading: the filter concerns partitions, not all devices | `if (bdev_is_partition(hd) && !bdev_nr_sectors(hd))` | `S182.src:1371` |
| Reading: the tested quantity is the partition's sector count, and the tested value is zero | `!bdev_nr_sectors(hd)`; the same file's size emitter returns `sysfs_emit(buf, "%llu\n", bdev_nr_sectors(dev_to_bdev(dev)));`. | `S182.src:1371,1052-1055` |
| Reading: every encountered partition satisfying that guard is passed over | `xa_for_each(&gp->part_tbl, idx, hd) { if (bdev_is_partition(hd) && !bdev_nr_sectors(hd)) continue;` | `S182.src:1370-1372` |
| Reading: that skipped entry emits no line in that traversal | `continue;` is before `part_stat_read_all(hd, &stat);`, all output calls, and `seq_putc(seqf, '\n');`. | `S182.src:1372,1380-1409` |

The host-specific occurrence in the first fact is not supplied by S182. If the observation is meant only as a decision-table scenario, make that explicit rather than relying on the judge to supply that interpretation. The implementation facts themselves have direct support in the row's own cited copy; no additional source is needed for them.

## Verdict-follows judgment

**Yes, as a reporting instruction about this `/proc/diskstats` read:** a skipped line supplies no counter value, so unavailable rather than a fabricated numeric zero follows from the omission. The entry expressly defines verdicts as reporting rules (`corpus/knowledge/disk-write-rate-r33.md:15`).

Two stronger propositions do **not** follow and should not be substituted for this verdict:

- Missing line implies zero capacity: the guard proves zero-sector partition implies omission, not its converse (`S182.src:1370-1372`).
- Missing procfs line means all statistics for the device are unavailable: the separate `part_stat_show` path reads and emits statistics without the zero-sector guard (`S182.src:1058-1099`).

## Findings and strongest counterexamples

### 1. Minor — host-specific wording has no host provenance

- Attacks: observation at `corpus/knowledge/disk-write-rate-r33.md:27`.
- Evidence: the source only contains the conditional `bdev_is_partition(hd) && !bdev_nr_sectors(hd)` (`S182.src:1371-1372`); no host occurrence is stated by that quote.
- Impacted axis: calibration; literal R-J fact coverage. This is a wording correction, not a kernel-behavior disagreement or an irreconcilable tradeoff.
- Smallest correction: replace the observation with **“A zero-sector partition encountered by `diskstats_show`”**. The existing reading then explains exactly the scenario named by the observation, without claiming an observed host occurrence.

### 2. None — the omission rule survived the kernel-path attacks

- A zero-sector **whole disk** is not covered by this guard: the partition predicate must also hold. The existing row already says partition, so this is not a defect (`S182.src:1371-1372`).
- Strongest same-source boundary: the sysfs `part_stat_show` emitter has no corresponding size check and prints `stat.sectors[STAT_WRITE]` (`S182.src:1058-1085`). [INFERENCE] For a surviving partition sysfs attribute, procfs omission alone therefore does not establish device-wide unavailability. The row's explicit procfs observation keeps its reporting rule local; optionally change the verdict to **“Report its write rate as unavailable from this `/proc/diskstats` read, never as zero writes.”**
- The neighboring `/proc/partitions` emitter has a different filter, `if (!bdev_nr_sectors(part)) continue;`, after a whole-disk capacity/hidden check. It must not be used to broaden the diskstats claim (`S182.src:968-977`).
- `CONFIG_PROC_FS` encloses both the diskstats implementation and registration; the row does not promise a procfs file on kernels without it (`S182.src:1345,1423-1430`).
- No older-version boundary is asserted by row 9. The entry limits its source facts to v7.2 (`corpus/knowledge/disk-write-rate-r33.md:55-56`), matching S182's pinned identity (`corpus/SOURCES.md:188`).

Additional v7.2 cross-checks, **not evidence for accepting this S182-only row**:

- [`include/linux/blkdev.h`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/blkdev.h?h=v7.2): `bdev_nr_sectors` returns `bdev->bd_nr_sectors`; `bdev_nr_bytes` shifts that count by `SECTOR_SHIFT`; `bdev_is_partition` tests `bdev_partno(bdev) != 0`. These corroborate the guard's meanings.
- [`block/partitions/core.c`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/block/partitions/core.c?h=v7.2): `blk_add_partition` immediately returns on `if (!size)`. A zero-length on-disk table description need not even become an enumerated kernel partition. `drop_partition` erases the partition-table entry with `xa_erase`. These paths warn against diagnosing the reason for an arbitrary missing line; they do not contradict the row's one-way implication.

## Six-consecutive-word check

Manually applied the actual lowercase `[a-z0-9_]+` normalization (`.ufo/waves/round-33/count-c1-a1.py:86-91,269-274`) to the reading and **all four** S182 Gate quotes (`corpus/lessons/round-33.md:17`).

- Quote 1's sole six-token run is `if bdev_is_partition hd bdev_nr_sectors hd continue`. It does not occur in the reading at `corpus/knowledge/disk-write-rate-r33.md:27`.
- Quotes 2, 3 and 4 have respectively 3, 5 and 5 normalized tokens, so none contains a six-token run.
- Result: **no prohibited six-word repetition**. The original row also has the two required distinct four-character-or-longer shared tokens, `{bdev_nr_sectors, sectors}`; `sectors` occurs in Gate quote 4. This is a manual local check, not an executed counter result (`count-c1-a1.py:191,237-238,259-267`, same directory as above).

## Checks and limits

Read the row/context; all S182 Gate quotes and their full printing-function surroundings (`S182.src:1345-1430`); iterator setup (`907-938`); sysfs emitter (`1052-1099`); alternate partitions emitter (`952-980`); frozen R-J/A1; and the counter's normalization/overlap code. Opened the two additional tag-pinned v7.2 files linked above. Initial raw.githubusercontent.com reads of those two files returned HTTP 429; ordinary reads of the official kernel.org URLs succeeded. No challenge was encountered or passed.

No canonical judge, counter, build, tests, host/device probe, runtime, or Git/jj command was invoked. No tools were installed or updated, no processes were started, and only this report was written. No unrun check is claimed as a pass.
