# AttackRow11 — flush values

Scope: row 11, `corpus/knowledge/disk-write-rate-r33.md:29`, at the supplied measured revision `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8`; inspected the working-tree files identified as identical in the assignment. This is a critic report, not a judge receipt.

Axes: **depth** (correct measurement identity), **calibration** (no implicit narrowing), and **freshness** (the historical flush-counter patch against Linux v7.2). The frozen rule is `.ufo/waves/round-33/contract.md:44-50`; the six-word restriction is at `:119-123`.

Path key: `E` = `corpus/knowledge/disk-write-rate-r33.md`; `G` = `corpus/lessons/round-33.md`; `S187` / `S188` = `corpus/evidence/sources-r33/S187.src` / `S188.src`.

## Per-fact audit

The complete reading is: “They count flushes the disk itself executed after the block layer merged flush requests, partitions do not track them, and the requests that cause flushes are mostly barriers that carry no data” (`E:29`).

| fact | quote or NOT STATED | file:line |
|---|---|---|
| Observation: a diskstats line has flush values. | “Kernel 5.5+ appends two more fields for flush requests:” followed by “19 flush requests completed successfully” and “20 time spent flushing”. | `S187:36-40` |
| Reading, literal plural referent: both flush values count executed flush requests. | **NOT STATED; contradicted.** The source distinguishes “count of completed flush requests and their total time.” Field 20 is duration, not another event count. | `S188:13-14`; `S187:39-40` |
| The flush-request count concerns requests executed by the disk. | “This counts flush requests executed by disk.” This sentence is under the flush-request-count heading, not the duration heading. | `S188:68-75` |
| The block layer can combine several flush requests into one. | “Block layer has sophisticated engine for combining several flush requests into one.” Also: “Block layer combines flush requests and executes at most one at a time.” | `S188:9-10,71` |
| Literal stronger reading of “after ... merged”: every counted flush follows an actual merger of multiple requests. | **NOT STATED.** An engine for combining requests is not a statement that every flush actually combined multiple requests. See the single-pending-request counterexample below. | `S188:9-10,71-72` |
| Partitions do not track the flush-request count. | “Not tracked for partitions.” | `S188:68-72` |
| If “them” covers both values, the added accounting targets the whole disk for both. | The added function uses `struct hd_struct *part = &rq->rq_disk->part0;`, then increments `ios[STAT_FLUSH]` and adds elapsed time to `nsecs[STAT_FLUSH]` on that same `part`. The prose partition exclusion explicitly describes the count. | `S188:127-135,68-75` |
| Requests triggering flushes are mostly barriers. | “Requests which trigger flushes usually are barriers - zero-size writes.” | `S188:11` |
| Those barriers carry no data. | The same sentence calls them “zero-size writes.” This supports the qualified barrier statement, not a claim that every triggering request has no data. | `S188:11` |

All Gate quotes of both cited IDs were read, including their surrounding copy text (`G:22-23`; `S187:1-43`; `S188:5-14,29-118,127-158`). R-J permits quotes located in the cited committed copies; the count/time distinction is present there even though the selected Gate excerpts omit it.

## Findings and strongest counterexamples

### F1 — major: two measurements silently become one

Attack: `E:29`, observation “The flush values on a line” and reading “They count flushes”.

Counterexample: the second flush value is explicitly “time spent flushing” (`S187:40`); the patch defines it as “the total number of milliseconds spent by all flush requests” (`S188:74-75`). It cannot be described as the number of flush requests executed. The two fields' distinct identities are also explicit in `S188:13-14`.

Impact: depth and calibration. Accepting this wording requires the caveat “They means only the count field,” which R-J expressly excludes (`.ufo/waves/round-33/contract.md:47-50`). This is a fixable identity defect, not an axis tradeoff.

Smallest correction: change the observation to the **flush-request count**, and make the reading singular. No new source is necessary (`S187:39`; `S188:68-72`).

### F2 — minor: mandatory merger is stronger than merge capability

Attack: `E:29`, “after the block layer merged flush requests”.

Evidence: `S188:9-10` states the combining capability, while `S188:71` describes its general behavior; neither requires an actual multi-request merger before every counted flush.

The opened Linux v7.2 implementation is [block/blk-flush.c](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/block/blk-flush.c?h=v7.2). Its fetched copy is `/fast/scratch/hyaku/mori-r33/AttackRow11/blk-flush-v7.2.c`:

- `:279-292`: `blk_kick_flush` checks for a nonempty pending list and for deferred data I/O; it does not require two pending requests.
- `:294-300`: it then issues/initializes a flush.
- `:220`: completion calls `blk_account_io_flush`.
- `:124-132`: that function increments the request count and separately accumulates elapsed time on `part0`.

[INFERENCE from these paths] With one pending request and neither deferral condition active, one flush can execute and increment the count without combining multiple requests. If the row merely means the post-coalescing accounting stage, that weaker meaning should be stated instead of requiring an implicit interpretation.

Impact: depth and calibration. Smallest correction: say the block layer **can combine** requests, rather than asserting that a merger has occurred for every counted flush.

## Verdict-follows judgment

The request-count verdict is sound: whole-disk-only reporting follows from the partition exclusion, and a request count is not an additional written-sector amount (`S188:68-72`; `S187:19,39`). The verdict does not repair the reading's count/duration conflation. It must not be used to silently narrow the observation from both flush values to one field.

## Minimal safe rewrite

Keep the sources and verdict; replace only the observation and reading:

| observation | reading | verdict | sources |
|---|---|---|---|
| The flush-request count (field 19) on a `/proc/diskstats` line | The count measures flush requests executed by the disk; partitions do not track it, and the block layer can combine several requests into one. Field 10 separately measures sectors written | Read flush counts from whole-disk lines only and never add them to sectors written | S188, S187 |

Support: field identities at `S187:19,39`; disk execution and partition exclusion at `S188:72`; combining capability at `S188:9-10`. The historical “mostly barriers” clause is explicitly sourced (`S188:11`) but is unnecessary to this verdict and is omitted from the correction.

## Additional attempts to break it

- **Data-bearing flush triggers:** v7.2 `blk-flush.c:12-16,22-26` explicitly permits data-bearing PREFLUSH/FUA requests. This narrows any temptation to read “mostly” as “all”; it does not disprove the qualified statement quoted in `S188:11`. The code does not establish a workload-wide majority.
- **No-cache path:** v7.2 `blk-flush.c:423-431` can complete an empty flush without issuing a hardware flush. This reinforces that the count is not a count of submitted flush-triggering requests; it is not an additional defect in the row's disk-execution wording.
- **Partition path:** v7.2 `blk-flush.c:124-132` still accounts both flush measurements against `q->disk->part0`, matching the historical patch's count exclusion (`S188:127-135`).
- **Version boundary:** `S187:36` and `S188:37` both say kernel 5.5+ adds these two fields. Row 11 itself asserts no numeric version boundary (`E:29`); no conflicting boundary was found in the inspected text. The “usually” statement is from the dated 2019 patch (`S188:3,11`), not a fresh workload measurement.

## Six-word check and execution record

Executed a bounded Python `functions.eval` comparison: lowercase, tokenize using `[a-z0-9_]+`, form every consecutive six-token tuple, and intersect the reading's tuples with each individual Gate quote. Inputs were the exact reading at `E:29` and all seven quotes at `G:22-23` (four S187, three S188).

Observed output: `reading_words=32`; each of `S187 Q1`, `S187 Q2`, `S187 Q3`, `S187 Q4`, `S188 Q1`, `S188 Q2`, `S188 Q3` printed `shared_six_word_runs=[]`. The proposed reading was checked by the same method; all seven printed `proposed_shared_six_word_runs=[]`. Thus no prohibited run was found in either reading.

The v7.2 fetch used `timeout 90 bash -c 'ulimit -v 262144; mkdir -p /fast/scratch/hyaku/mori-r33/AttackRow11 && curl --fail --silent --show-error --max-time 60 "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/block/blk-flush.c?h=v7.2" --output /fast/scratch/hyaku/mori-r33/AttackRow11/blk-flush-v7.2.c'`; it completed successfully with no output. Earlier raw GitHub reads returned HTTP 429; the ordinary kernel.org read/fetch succeeded without a challenge.

No C1 counter, judge, UFO runtime, build, test suite, or block-device mutation was run. No tools were installed or updated; no background process was started. Only this report and the permitted scratch source copy were written.
