# AttackRow04 — counter decreases

## Scope and axes

Reviewed row 4 at `corpus/knowledge/disk-write-rate-r33.md:22`, its sole cited source S181, all four S181 Gate quotes (`corpus/lessons/round-33.md:16`), and their committed-copy context. Working-tree reads were permitted by the assignment for measured revision `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8`; no revision identity check was run.

Impacted axes: **depth** (the FR6 decision's scope) and **calibration** (distinguishing a source fact from a conservative reporting rule). C1 targets depth, not a new runtime rate arm (`.ufo/waves/round-33/contract.md:12-22`; `corpus/knowledge/disk-write-rate-r33.md:45-51`). This is an advisory attack, not the C1 judge or a claim-admission verdict.

R-J requires every observation/reading fact to be stated in a cited copy and the verdict to follow without another fact; accepting only with a caveat is insufficient (`.ufo/waves/round-33/contract.md:44-50`).

## Atomic fact audit

Paths in this table are relative to the lane root. Quotes are from the committed copy, not the wave-1 report.

| fact | quote or NOT STATED | file:line |
|---|---|---|
| Observation: the reader compares stat snapshots | “Applications reading these counters should detect and handle resets when comparing stat snapshots.” | `corpus/evidence/sources-r33/S181.src:36-37` |
| Observation: the newer value is lower than the older value | **NOT STATED** as an actual occurrence or explicit lower-than comparison. The source describes resets and snapshot comparisons, not a measured pair. As a hypothetical input, this is a condition rather than evidence of an observed reset. | `corpus/knowledge/disk-write-rate-r33.md:22`; `corpus/evidence/sources-r33/S181.src:33-37` |
| Reading: every statistical field other than field 9 is cumulative | “All fields are cumulative, monotonic counters, except for field 9” | `corpus/evidence/sources-r33/S181.src:33` |
| Reading: those fields “only grow,” meaning nondecreasing between resets | “cumulative, monotonic counters” | `corpus/evidence/sources-r33/S181.src:33` |
| Reading: field 9 is excluded from that monotonic-counter description | “except for field 9, which resets to zero as I/Os complete.” | `corpus/evidence/sources-r33/S181.src:33-34` |
| Reading: the other fields reset at boot | “The remaining fields reset at boot” | `corpus/evidence/sources-r33/S181.src:34` |
| Reading: device reattachment resets them | “on device reattachment” | `corpus/evidence/sources-r33/S181.src:34-35` |
| Reading: device reinitialization resets them | “device reattachment or reinitialization” | `corpus/evidence/sources-r33/S181.src:35` |
| Reading: underlying-counter overflow resets them | “when the underlying counter overflows.” | `corpus/evidence/sources-r33/S181.src:35-36` |

The reading's reset list is directly supported. “Only grows” should not be interpreted as strictly increasing on every read: the source says monotonic, not continuously active (`corpus/evidence/sources-r33/S181.src:33`). There is no basis here for adding a fixed counter width, a unique reset diagnosis, or an overflow-reconstruction procedure; the same source separately describes possible overflow of the per-CPU summation variable (`:117-121`).

## Finding — major: the observation and device-wide verdict exceed the reading's scope

**Attacks:** `corpus/knowledge/disk-write-rate-r33.md:22`, “A counter” and “Mark that device's interval unavailable”.

**Strongest same-source counterexample:** field 9 can fall normally as requests finish. S181 calls it “# of I/Os currently in progress” and says it is “Incremented as requests are given to appropriate struct request_queue and decremented as they finish” (`corpus/evidence/sources-r33/S181.src:71-73`). Its fall therefore does not require a reset of the sectors-written total, which is a separate field (`:64-65`).

[INFERENCE, synthetic example, not a host measurement] An older/newer pair with in-flight I/Os `2 → 0` and sectors written `100 → 101` satisfies the unqualified observation while presenting no sectors-counter decrease. The reading expressly excludes field 9, yet the verdict invalidates the device's interval. Accepting the row requires silently adding “other than field 9” to the observation. Row 5's separate instruction about the in-flight value does not put that restriction into row 4 (`corpus/knowledge/disk-write-rate-r33.md:22-23`).

**Kernel-path narrowing, even if “counter” is taken to exclude the gauge:** exported timing fields can wrap independently of the sectors total. The v7.2 copy stores `nsecs` as `u64`, alongside separate `sectors` counters (`corpus/evidence/sources-r33/S183.src:8-14`). `diskstats_show` prints write sectors separately, then prints write milliseconds using `(unsigned int)div_u64(stat.nsecs[STAT_WRITE], NSEC_PER_MSEC)` (`corpus/evidence/sources-r33/S182.src:1389-1393`). The sysfs path uses the same separate conversion (`:1083-1086`).

[INFERENCE, synthetic arithmetic, not kernel execution] On a 32-bit `unsigned int` target, increasing stored write nanoseconds from `4294967295000000` to `4294967296000000` produces exported milliseconds `4294967295 → 0`, without overflowing the `u64` storage. A separately increasing sectors total need not become unusable merely because this timing representation wrapped. S181 itself distinguishes stored per-CPU counters from a potentially overflowing sum (`corpus/evidence/sources-r33/S181.src:117-120`). These code copies are counterexample evidence, **not** additional support the original S181-only row may borrow under R-J.

**Verdict-follows judgment:** not as an unrestricted, device-wide instruction. It is defensible as a conservative rule for the affected cumulative counter, particularly sectors written. The existing reading does not establish that every falling value is abnormal or that a drop in an unrelated field invalidates sectors-written arithmetic. The no-negative/no-wrap-reconstruction/no-zero-substitution policy adds no empirical fact once applied to a decreased sectors-written counter; it should remain explicitly the lane's reporting policy, not an upstream command (`corpus/knowledge/disk-write-rate-r33.md:15,22`).

**Smallest safe correction:** name the sectors-written counter in the observation and limit unavailability to its write-rate interval. To avoid also treating the hypothetical lower-than input as a source-attested occurrence under the strictest R-J reading, move that condition into the verdict:

| observation | reading | verdict | sources |
|---|---|---|---|
| Comparing two snapshots of the sectors-written counter | The sectors-written total accumulates over time, but rebooting, reconnecting or reinitializing the device, or overflow can reset it; the documentation calls for handling resets between snapshots | If the newer sectors-written total is lower, mark this write-rate interval unavailable; print no negative, wrap-corrected or zero-filled rate | S181 |

This retains the existing reset cases and reporting posture. Support is the sectors-written definition and snapshot/reset passage (`corpus/evidence/sources-r33/S181.src:64-65,33-37`); no new source or relaxed judge rule is needed. This is a fixable row-scope defect, not a reason to alter the frozen contract.

## A1 six-word originality check

**Severity: none.** Used A1's lowercase `[a-z0-9_]+` tokenization and compared every six-token window of the original reading with every window in each of the four cited Gate quotes (`.ufo/waves/round-33/count-c1-a1.py:86-87,269-274`; `corpus/lessons/round-33.md:16`). The in-memory Python calculation was:

```python
words = lambda s: re.findall(r'[a-z0-9_]+', s.lower())
def sixes(s):
    w = words(s)
    return {tuple(w[i:i+6]) for i in range(len(w)-5)}
# Intersect sixes(original_reading) with sixes(each S181 Gate quote).
```

Observed output:

```text
row4_vs_S181_Q1: common_sixgrams=0 []
row4_vs_S181_Q2: common_sixgrams=0 []
row4_vs_S181_Q3: common_sixgrams=0 []
row4_vs_S181_Q4: common_sixgrams=0 []
proposed_reading_common_sixgrams= []
```

The same in-memory calculation produced the synthetic conversion values above and `u64_storage_overflow=False`; it did not execute the kernel path. The calculation used the row and Gate text read in this review, not the claim counter or a judge receipt.

## Version and containment checks

- S181 is explicitly the v7.2-tagged document (`corpus/lessons/round-33.md:16`). Row 4 asserts no earlier release boundary. Inspected its complete committed copy (`corpus/evidence/sources-r33/S181.src:1-187`); no additional release boundary for the reset paragraph was identified. No cross-version comparison was run.
- Inspected the actual reset/snapshot paragraphs, field-9 definition, locking/per-CPU caveats, kernel aggregation, output casts and lifecycle reset. The lifecycle code explicitly clears disk statistics with `part_stat_set_all(disk->part0, 0)` (`corpus/evidence/sources-r33/S182.src:107-125,128-170,700-749,1058-1099,1353-1408`; `S183.src:43-49`). It does not cure the observation/verdict scope mismatch.
- Searched the opened v7.2 accounting copies for `part_stat_(sub|dec)`, `__part_stat_(sub|dec)`, `sectors[` and `nsecs[`. The sector/time matches were additions at `S184.src:1110-1111` and `S185.src:862,1084`; no subtract/decrement match was returned in those two files. This is a bounded search, not a kernel-wide no-decrement claim.
- No source fetch, full C1 counter, judge runtime, build, tests, host disk probe, git/jj command or write, device-setting operation, subagent, shell/background job, or tool installation/update was performed. Only this assigned report was written. No child process tree was started.
