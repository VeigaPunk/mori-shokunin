# AttackRow05 — field 12, I/Os in progress

Scope: decision-table row 5 at measured revision `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8`, using the working-tree copies declared identical by the assignment. Target: `corpus/knowledge/disk-write-rate-r33.md:23`. This is a critic report, not the C1 judge receipt or an admission decision.

Axes: **depth** (what the value actually measures) and **calibration** (an accounting estimate presented as an exact instantaneous quantity). C1's declared axis is depth (`.ufo/waves/round-33/contract.md:12,24`). The findings are fixable wording defects, not a proposed axis trade.

## Cited Gate quotes inspected

The row cites only S187 and S182 (`corpus/knowledge/disk-write-rate-r33.md:23`). Their Gate rows are `corpus/lessons/round-33.md:17,22`. All locators below are under `corpus/evidence/sources-r33/`.

| Source | Gate quotes, with committed-copy locators |
|---|---|
| S182 | `S182.src:1371-1372`: "if (bdev_is_partition(hd) && !bdev_nr_sectors(hd)) continue;"; `:1374`: "inflight = bdev_count_inflight(hd);"; `:1395`: `seq_put_decimal_ull(seqf, " ", jiffies_to_msecs(stat.io_ticks));`; `:1403`: `seq_put_decimal_ull(seqf, " ", stat.sectors[STAT_DISCARD]);` |
| S187 | `S187.src:6-7`: "Each line contains the following 14 fields:"; `:19-21`: "10 sectors written 11 time spent writing (ms) 12 I/Os currently in progress"; `:26-27`: "Kernel 4.18+ appends four more fields for discard tracking putting the total at 18:"; `:36`: "Kernel 5.5+ appends two more fields for flush requests:" |

I opened their surroundings, including S182's counting implementation, both stat emitters, and the callback registration (`S182.src:128-171,1058-1116,1345-1426`), and the complete short ABI description (`S187.src:1-43`).

## Atomic-fact audit

R-J requires every observation/reading fact to be stated by the cited committed sources and the verdict to follow without an additional fact (`.ufo/waves/round-33/contract.md:44-50`). Additional quotes below come from the row's own cited copies, not substitute sources.

| Fact | Quote or NOT STATED | File:line |
|---|---|---|
| Observation: the interface is `/proc/diskstats`. | "The /proc/diskstats file displays the I/O statistics of block devices." | `corpus/evidence/sources-r33/S187.src:5-6` |
| Observation: field 12 is labelled I/Os currently in progress. | "12 I/Os currently in progress" | `corpus/evidence/sources-r33/S187.src:21` |
| Reading: this is an in-progress I/O count. | "bdev_count_inflight - get the number of inflight IOs for a block device." Its explicit scope is "Inflight here means started IO accounting". | `corpus/evidence/sources-r33/S182.src:155,159-161` |
| Reading: the value is the actual number at the time the file is read, without qualification. | **NOT STATED as an exact point-in-time count.** The implementation warns that cross-CPU issue/completion during traversal can cause "the inflight number to be negative", and then clamps each directional sum to zero. See the counterexample below. | `corpus/evidence/sources-r33/S182.src:140-151` |
| Reading: `diskstats_show` obtains it from `bdev_count_inflight`. | "inflight = bdev_count_inflight(hd);" followed by `seq_put_decimal_ull(seqf, " ", inflight);` in `diskstats_show`. | `corpus/evidence/sources-r33/S182.src:1353,1374,1394` |
| Reading: this happens on every read. | The code states the calculation for each emitted device line and registers `.show = diskstats_show`. **NOT STATED literally for every userspace `read(2)` call.** No syscall-level guarantee should be inferred from the callback body. This wording ambiguity is secondary to the exactness defect. | `corpus/evidence/sources-r33/S182.src:1370-1374,1416-1425` |
| Reading: this is recomputed, rather than accumulated into a total across readings. | `int write = 0; int read = 0;`; the loop reads the per-CPU values; the helper returns `inflight[READ] + inflight[WRITE]`; the emitter assigns the result. These statements show recomputation, not accumulation across samples. | `corpus/evidence/sources-r33/S182.src:131-143,163-169,1374` |

## Finding 1 — major: an exact instantaneous queue-depth promise exceeds the source

Attack: `corpus/knowledge/disk-write-rate-r33.md:23`, reading "when the file is read" and verdict "the queue depth at the moment of the read".

The cited source explicitly acknowledges a non-atomic collection artifact:

> While iterating all CPUs, some IOs may be issued from a CPU already traversed and complete on a CPU that has not yet been traversed, causing the inflight number to be negative.

Evidence: `corpus/evidence/sources-r33/S182.src:145-148`. The correction is `inflight[READ] = read > 0 ? read : 0;` and the analogous write expression (`:150-151`). There is no exact-snapshot guarantee in that implementation (`:128-169`).

Strongest counterexample, **[INFERENCE: source-permitted interleaving, not a live-kernel reproduction]**:

1. One read A is outstanding; the two CPU accounting values are `(1, 0)`.
2. The collector samples the first CPU's value, obtaining `1`.
3. Reads B and C start on that already-sampled CPU and complete on the unvisited CPU. The actual values become `(3, -2)`; A remains outstanding throughout.
4. The collector samples `-2` from the second CPU. Its sampled subtotal is `-1`, which the cited code exports as `0`, although A never stopped being outstanding.

This uses exactly the issue/completion movement described by the source (`S182.src:140-151`). The arithmetic was checked in Eval: `sampled subtotal = -1; exported subtotal = 0; actual outstanding = 1`. It is an illustration of the implementation, not evidence that this host experienced the race.

Consequently, accepting the exact-moment wording requires the sampling caveat that R-J expressly disallows leaving unstated (`contract.md:47-50`). Impacted axes: depth and calibration. Smallest safe correction: describe the exported accounting value and its computation, not an exact instantaneous queue depth.

## Finding 2 — major: “queue depth” adds an unidentified measurement scope

Attack: `corpus/knowledge/disk-write-rate-r33.md:23`, verdict "Report it as the queue depth".

The source defines what starts this count: `bdev_start_io_acct()` for bio-based devices and `blk_account_io_start()` for request-based devices (`corpus/evidence/sources-r33/S182.src:159-161`). It separately describes `part_inflight_show` as "Show the number of IOs issued to driver", starting from `blk_mq_start_request()` for request-based devices (`:1102-1105`). That path passes `queue_is_mq(q)` to the counting helper (`:1114`); the diskstats helper passes `false` (`:167`), bypassing the driver's `blk_mq_in_driver_rw` branch (`:135-137`).

**[INFERENCE]** Calling both quantities simply “queue depth” hides the accounting-versus-driver distinction. The row's reading neither identifies a particular queue nor states an equality with its occupancy. A colloquial definition of queue depth might be defensible, but importing that definition is an additional fact under R-J, not a quote from the reading.

An additional Linux v7.2 narrowing, used only to attack the claim, not to support this row: `blk_account_io_start` returns immediately when `!blk_queue_io_stat(req->q)` and can also exclude passthrough requests before incrementing the count (`corpus/evidence/sources-r33/S185.src:1090-1115`). **[INFERENCE]** Such unaccounted requests cannot be recovered by the diskstats summation. S185 is not cited by row 5 and therefore cannot rescue it under R-J.

Impacted axes: depth and calibration. Smallest safe correction: call the value the exported in-progress accounting count; do not identify it with an unspecified queue's depth.

## Verdict-follows judgment

**No, not in full.** Reporting an in-progress count directly instead of deriving a throughput rate from its delta is consistent with the reading. Reporting an exact queue depth at a particular moment additionally requires both a queue-identity equivalence and atomic sampling; the reading establishes neither, and its cited implementation narrows the latter (`S182.src:140-169,1102-1114`). This is a row-local finding, not a claim-level C1 verdict.

The ordinal itself is not the problem: the ABI explicitly gives field 12 (`S187.src:21`). Row 5 contains no historical version boundary to correct; the narrowing is present in its own v7.2 source (`corpus/lessons/round-33.md:17,22`).

## Proposed minimal rewrite

Keep the observation and source IDs. Replace the reading and verdict only:

| # | observation | reading | verdict | sources |
|---|---|---|---|---|
| 5 | Field 12 of a `/proc/diskstats` line, I/Os currently in progress | The exported in-progress value comes from `bdev_count_inflight`: it totals each direction's per-CPU accounting values, clamps negative totals to zero, then adds the read and write results | Report the exported in-progress count itself, not a throughput rate derived from its delta | S187, S182 |

Support for the replacement's added precision is already in the cited committed copy: per-CPU directional sums and clamping at `S182.src:140-151`, accounting scope at `:159-161`, returned sum at `:163-169`, and emitted value at `:1374,1394`. No additional source ID is required.

## Six-consecutive-word check and limits

Applied A1's lowercase `[a-z0-9_]+` tokenization (`.ufo/waves/round-33/count-c1-a1.py:86-87`) to the exact original reading and each of the eight cited Gate quotes listed above. Eval calculated six-token tuples and intersected their sets:

```text
Reading six-word runs: 24
S182 Gate six-word-run counts: 1, 0, 0, 1
S187 Gate six-word-run counts: 2, 9, 10, 5
Every per-quote intersection: []
Total overlap: 0
Proposed reading normalized words: 29
Proposed reading Gate six-word overlap: 0
```

This checks the anti-copy condition only; it does not establish semantic support. All three Eval cells had a 15-second deadline and operated only on the bounded text literals already opened above. No judge, C1 counter, build, test suite, live-device experiment, shell command, background job, package installation, or tool update was run. No lane content was edited except this report.
