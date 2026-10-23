# AttackRow02 — completion-time sector accounting

Scope: row 2 at `corpus/knowledge/disk-write-rate-r33.md:20`, measured revision `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8`; working-tree copies permitted by the assignment. Findings only, not a judge receipt.

Axes: **depth / FR6** (accurate accounting paths), **calibration** (qualifying what a counter represents), and **source fidelity / A1 integrity** (stated support without copied readings). C1's depth/FR6 target is ` .ufo/waves/round-33/contract.md:12-15`; the applicable R-J and A1 requirements are at that file's lines 47-50 and 119-123.

## Per-fact support table

All locators below name committed source copies, not wave-1 assertions. The observation is a decision-table condition, not a claim that this seat measured a particular sample pair.

| Fact in observation or reading | Quote or NOT STATED | file:line |
|---|---|---|
| O1. There is a sectors-written value. | `write sectors   sectors       number of sectors written`; the sector section also says these values count sectors written to the block device. | `corpus/evidence/sources-r33/S180.src:35,67-73` |
| O2. Its newer sample exceeds its earlier sample. | `The counters are incremented when the I/O completes.` This supports growth as a possible observation. **NOT STATED** as an actual two-sample measurement in these sources; no such empirical claim is needed for the conditional observation. | `corpus/evidence/sources-r33/S180.src:73`; observation at `corpus/knowledge/disk-write-rate-r33.md:20` |
| R1. Sector-counter increments occur at I/O completion. | `The counters are incremented when the I/O completes.` | `corpus/evidence/sources-r33/S180.src:67-73` |
| R2. `bdev_end_io_acct` takes a sector count. | `void bdev_end_io_acct(struct block_device *bdev, enum req_op op,` / `unsigned int sectors, unsigned long start_time)` | `corpus/evidence/sources-r33/S184.src:1100-1101` |
| R3. That function adds its supplied sectors through `part_stat_add`. | `part_stat_add(bdev, sectors[sgrp], sectors);` within that function; `sgrp` comes from `op_stat_group(op)`. | `corpus/evidence/sources-r33/S184.src:1103,1110` |
| R4. The request helper's byte count is used on completion paths. | `blk_account_io_completion(req, total_bytes);`; another caller documents `@nr_bytes: number of bytes to complete for @req` and calls `blk_account_io_completion(req, nr_bytes);`. | `corpus/evidence/sources-r33/S185.src:881-905,933-936,983` |
| R5. Its sector addition uses bytes shifted right by nine. | `part_stat_add(req->part, sectors[sgrp], bytes >> 9);` | `corpus/evidence/sources-r33/S185.src:862` |
| R6. The reading's unqualified claim that `blk_account_io_completion` adds that count. | **NOT STATED without a condition.** The addition is inside `if (req->rq_flags & RQF_IO_STAT) {`. | `corpus/evidence/sources-r33/S185.src:856-865` |

## Finding 1 — major: the reading omits the request-stat guard

**Attack:** `corpus/knowledge/disk-write-rate-r33.md:20`, specifically “`blk_account_io_completion` adds completed bytes shifted right by 9.”

**Evidence:** the complete helper at `corpus/evidence/sources-r33/S185.src:856-865` encloses its only sector addition in `if (req->rq_flags & RQF_IO_STAT)`. The start path can return at `!blk_queue_io_stat(req->q)` or at the passthrough-stat eligibility check before setting that flag (`S185.src:1090-1099`). The Gate extracts the declaration and addition separately and omits the guard (`corpus/lessons/round-33.md:20`), although the committed copy retains it.

**Strongest counterexample [INFERENCE from the displayed control flow, not a runtime test]:** with `RQF_IO_STAT` clear, a call to this helper performs no sector addition. Another flagged completion can still increase the sampled counter, satisfying the row's observation; the positive delta does not erase the omitted path. The original source seat also explicitly retained the guard in its candidate fact and quote (`.ufo/waves/round-33/w1/SrcBlkMq.md:44`).

**Impact:** accepting the unqualified helper claim requires precisely the caveat forbidden by R-J (`.ufo/waves/round-33/contract.md:47-50`). This is a fixable depth/calibration defect, not a reason to change the frozen rule or an acceptable trade.

## Verdict-follows judgment and further falsification

**The completion-versus-submission timing contrast follows** from the reading's supported completion-timing statement (`S180.src:73`). The guard defect is in the reading; it does not turn counted completions into submissions. This judgment does **not** establish that the delta covers every write or only successful writes.

Two additional boundaries were tested against the cited request source:

- **Partial completion, severity none as an independent literal contradiction:** `blk_update_request` explicitly says “Complete multiple bytes without completing the request” (`corpus/evidence/sources-r33/S185.src:933`), describes ending I/O on bytes while leaving the request structure unfinished (`:938-941`), and credits sectors at `:983`. Thus “completion” must mean completion accounting of bytes, not necessarily completion of a whole request. The row does not expressly claim whole-request-only timing.
- **Error completion, severity none as an independent literal contradiction:** the error branch reports the error (`corpus/evidence/sources-r33/S185.src:977-980`), but accounting follows at `:983`, before the error is assigned to the bio at `:990-991`. [INFERENCE] An eligible failed completion can therefore increase sectors-written; “completed-write throughput” is not proof of successful or durable writes. The row does not expressly assert success or durability. `S184.src:947-949` likewise separates completion notification from success/failure status.

No historical version boundary is asserted by row 2. Its entry-wide v7.2 limit is explicit (`corpus/knowledge/disk-write-rate-r33.md:55-56`); this review found the narrowing in that pinned code, not in a different kernel release. No older-version support or live-host behavior was tested.

## Smallest safe correction

Leave the observation and completion-versus-submission verdict unchanged; insert the request-stat qualification into the reading:

> The kernel adds to the sector counters when an I/O completes: `bdev_end_io_acct` adds the sectors it is given with `part_stat_add`, and, for a request with `RQF_IO_STAT` set, `blk_account_io_completion` adds completed bytes shifted right by 9

The added condition is stated directly at `corpus/evidence/sources-r33/S185.src:858`. No new source, source identity, policy, or version claim is needed. A later implementation must not silently interpret “completed” as “successful” or “whole request”; those stronger claims are narrowed by the paths above.

## Six-word overlap check and checks performed

Read every Gate quote for S180, S184 and S185 (`corpus/lessons/round-33.md:15,19-20`) and their source surroundings: S180 lines 1-103, S184 lines 1039-1124, and S185 lines 750-1155. Also inspected S184's submission comment/body at 939-963 and S185's request initialization at 410-460. Wave-1 reports were context only, not substituted for source support.

The static Eval check used `re.findall(r'[a-z0-9_]+', text.lower())`, formed every contiguous six-word tuple, and intersected the reading's tuples with each of the nine cited Gate quotations. Observed output:

```text
row2_reading_words=30
cited_gate_quotes_checked=9
shared_six_word_runs=0
S180:21-22: NONE
S180:71-73: NONE
S180:73: NONE
S180:79-80: NONE
S184:1100: NONE
S184:1110: NONE
S184:1067-1068: NONE
S185:856: NONE
S185:862: NONE
proposed_minimal_reading_shared_six_word_runs=0
```

Original and proposed readings therefore have no six-consecutive-word overlap with those Gate quotes under A1's normalization (`.ufo/waves/round-33/contract.md:119-123`). This is a scoped static check, not execution of the C1 counter or a judge.

No build, test, counter, judge, runtime, device-setting operation, git/jj command, or source re-fetch was run. No tools were installed or updated; no background jobs were started. Only this report was written.
