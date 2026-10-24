# AttackRow03 — row 3 closure-risk review

Scope: `corpus/knowledge/disk-write-rate-r33.md:21`, measured revision `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8`; working-tree copies used as authorized by the assignment. This is an advisory critique, not the canonical judge receipt.

Axes: **depth** (exact accounting semantics), **operability** (safe aggregation instruction), **calibration** (source coverage and limits). C1 targets depth (`.ufo/waves/round-33/contract.md:24-50`); A1 additionally prohibits matching six-word runs (`:119-123`).

## Atomic facts

Locators below are relative to the lane. `E/` abbreviates `corpus/evidence/sources-r33/`. The row cites only S183 and S184 (`corpus/knowledge/disk-write-rate-r33.md:21`).

| Fact asserted by observation or reading | Quote or NOT STATED | file:line |
|---|---|---|
| O1: `/proc/diskstats` has a whole-disk line | **NOT STATED by either cited source.** Their accounting definitions do not describe this output. The explicit example is in uncited S181. | `E/S183.src:8-24,57-64`; `E/S184.src:1100-1122`; actual output example: `E/S181.src:9-14` |
| O2: That line appears next to lines for its partitions | **NOT STATED by either cited source.** S181 says “Here are examples using a disk with two partitions:” and immediately prints the three adjacent lines, but the row does not cite S181. | `E/S181.src:9-14`; cited macro: `E/S183.src:60-64` |
| O3: `nvme0n1`, `nvme0n1p1`, `nvme0n1p2` exemplify that relationship | **NOT STATED by either cited source.** Those exact example device names occur in uncited S181. | `E/S181.src:12-14`; current source cell: `corpus/knowledge/disk-write-rate-r33.md:21` |
| R1: `part_stat_add` increments the supplied partition's counter | `#define part_stat_add(part, field, addnd) do {` followed by `__part_stat_add((part), field, addnd);` | `E/S183.src:60-61` |
| R2: For a partition, the identical increment is also applied to the whole disk | `if (bdev_is_partition(part))` followed by `__part_stat_add(bdev_whole(part), field, addnd);` — the same `field` and `addnd` occur in both updates. | `E/S183.src:61-63` |
| R3: Completed-sector accounting adds sectors through `part_stat_add` | `void bdev_end_io_acct(struct block_device *bdev, enum req_op op,` … `part_stat_add(bdev, sectors[sgrp], sectors);` | `E/S184.src:1100-1110` |
| R4: The disk counter already includes its partitions' sector increments made through that macro | The two additions above apply the same increment to the partition and its parent. This establishes inclusion of those accounting increments, **not equality between every disk total and a sum of partition totals**. | `E/S183.src:60-64`; sector-update call: `E/S184.src:1110` |

Negative-text cross-check: the read-only search `grep(pattern="diskstats|/proc/|nvme0n1", path="E/S183.src;E/S184.src")` returned `No matches found`. The missing observation support cannot be supplied by S181 without naming S181 in this row: R-J explicitly excludes an uncited source (`.ufo/waves/round-33/contract.md:47-50`).

## Finding 1 — major: the host-total verdict does not follow

Attack: `corpus/knowledge/disk-write-rate-r33.md:21`, verdict “Total a host's writes over whole-disk lines only or over partition lines only”. Impacted axes: depth, operability, calibration.

**Verdict-follows judgment: no.** The last instruction, never combining a parent disk with its partitions, follows from the reading. The promise that either exclusive class totals a host's writes does not. Inclusion of partition increments in disk counters does not establish that partition counters cover every disk increment (`E/S183.src:60-64`).

Strongest source-level counterexample, **[INFERENCE; no device I/O executed]**:

1. Supply a whole-disk `bdev` to `bdev_end_io_acct` for a completed eight-sector write. That function credits `sectors[sgrp]` via `part_stat_add(bdev, sectors[sgrp], sectors)` (`E/S184.src:1100-1110`).
2. The macro first credits that device and only credits another device if the supplied device is a partition. There is no reverse update from a whole disk to any partition (`E/S183.src:60-64`).
3. Therefore that event contributes eight to the disk counter and zero to all partition counters. A partition-only host total misses it. A disk without partitions makes the coverage failure especially direct.

The request-based path does not supply the missing converse: it selects `req->bio->bi_bdev` and then credits `req->part` with `part_stat_add`, gated by `RQF_IO_STAT` (`E/S185.src:858-864,1094-1111`). S185 is corroborating counterexample context, not an allowed substitute for this row's citations.

There is also no topology/layer selection rule in the reading. The entry itself says the observed dm/backing-device double count remains unsourced (`corpus/knowledge/disk-write-rate-r33.md:38-43`). Existing host evidence records identical positive deltas for `dm-0` and `nvme0n1p2`, with their parent disk containing that partition's delta (`.ufo/waves/round-33/w1/ExecHostDiskstats.md:116-130`). **[INFERENCE]** If “whole-disk lines” includes nonpartition virtual devices as well as their backing disks, omitting partition lines still double-counts. Restricting to a particular physical/topological layer would be another premise absent from this reading. This host observation is not upstream support for the row.

Smallest safe correction: remove the host-total guarantee and keep only the parent/partition double-count prohibition. This is a fixable scope defect, not an acceptable tradeoff against operability.

## Finding 2 — major: observation support is routed through an uncited page

Attack: `corpus/knowledge/disk-write-rate-r33.md:21`, observation and source cells. Impacted axes: depth and calibration/provenance.

S183's Gate quotes concern the macro and `unsigned long sectors[NR_STAT_GROUPS]`; S184's concern the accounting endpoint and `io_ticks` (`corpus/lessons/round-33.md:18-19`). Neither their quoted surroundings nor the cited copies state the example output. The exact observation is available in `E/S181.src:9-14`, but S181 is absent from the row's own source cell. R-J disallows repairing this by silently consulting another row's source (`.ufo/waves/round-33/contract.md:47-50`).

Smallest safe correction: add S181 to this row's source cell; it is already registered and committed (`corpus/SOURCES.md:187`; `E/S181.src:9-14`). No new source or identity change is needed.

## Minimal proposed rewrite

Keep the current observation and reading. Change only:

- **verdict:** `Do not sum a disk's sector count together with its partitions' sector counts`.
- **sources:** `S181, S183, S184`.

The added citation states the observation; the reduced verdict follows from the existing reading without claiming host-wide coverage. This proposes no change to R-J, A1, the claim threshold, or any judge authority (`.ufo/waves/round-33/contract.md:47-50,119-123`).

## Quote, version, and narrowing checks

**Severity none — no six-word copying found.** A bounded read-only Python check used A1's `[a-z0-9_]+` lowercased tokenization, Gate quote extraction/unescaping, and six-token window comparison (`.ufo/waves/round-33/count-c1-a1.py:59,82-87,269-278`). It compared the row's reading separately with every Gate quote of each cited ID. An additional check covered proposed added S181. Execution was `timeout 30s prlimit --as=268435456 -- python3 -c <in-memory read-only comparison>`; each process exited 0. Observed output for the existing reading:

```text
S183 gate_quotes=2 located=True
S184 gate_quotes=3 located=True
row3 reading_words=38 cited_gate_quotes=5 shared_sixgrams=[]
S181 gate_quotes=4 located=True
row3 reading_words=38 cited_gate_quotes=4 shared_sixgrams=[]
```

`located=True` means every extracted Gate quote was found after whitespace collapse in its corresponding copy. The two check invocations covered five current quotes and four additional quotes respectively, not a concatenation of quote boundaries.

**Severity none — no false row-specific version boundary found.** Both cited URLs are pinned to Linux v7.2 (`corpus/lessons/round-33.md:18-19`), matching the entry's stated scope (`corpus/knowledge/disk-write-rate-r33.md:55-56`). The older-kernel discussion in `E/S181.src:129-170` is not evidence against the current conditional macro. No sysstat source is cited by this row.

**Narrowing, not a separate defect:** lockless reads can make partition sums only approximately equal to disk totals (`E/S181.src:111-120`). The entry already names this limitation (`corpus/knowledge/disk-write-rate-r33.md:57-58`), and the row's additive-accounting reading need not promise atomic snapshot equality. The minimal rewrite preserves that distinction.

## Checks actually performed

- Read row 3, its context, frozen R-J, and Amendment A1 at the locators above.
- Read all five cited Gate quotes and their source surroundings: `E/S183.src:1-84`; `E/S184.src:1059-1122`; also inspected the remapping path at `E/S184.src:618-635,808-848`.
- Inspected the alternative request accounting path (`E/S185.src:856-865,1069-1117`), output path (`E/S182.src:1345-1414`), observation example and version/locking caveats (`E/S181.src:1-40,111-170`), and existing host evidence at the locators above.
- Ran the read-only token/quote checks described above. No canonical judge or counting predicate was invoked.
- Ran `timeout 20s prlimit --as=268435456 -- sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r33/S183.src /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r33/S184.src`; output matched the respective Gate hashes (`corpus/lessons/round-33.md:18-19`):

```text
2e22ee58e88396108d9962b122082d899fd517e3c67195e9dee580db63d55a9a  /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r33/S183.src
528501312dbd8da7649051006f12203fbef03f5180c4408ccc20856262c77827  /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r33/S184.src
```

No upstream fetch, host measurement, build, device write, integration, or commit was performed. Tools installed/updated: none. All started subprocesses exited; no background jobs were started. Only this report was written in the lane.
