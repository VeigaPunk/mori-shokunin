# AttackRow07 — field 11 write ticks

Scope: row 7 at `corpus/knowledge/disk-write-rate-r33.md:25`, measured revision `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8`. Working-tree reads were used under the assignment's stated identity with that revision. This is a critic report, not a canonical judge receipt.

Axes: depth/FR6, source fidelity under R-J, calibration of the time-window claim, and A1 reading originality (`.ufo/waves/round-33/contract.md:12-15,44-50,119-123`).

## Finding 1 — major: capability is sourced; guaranteed growth in each second is not

Attack: `corpus/knowledge/disk-write-rate-r33.md:25`, particularly “climbs by more than 1000 for each wall-clock second.”

The general lesson is sound: overlapping request waits can produce more accumulated request milliseconds than elapsed wall milliseconds. The defect is making that a necessary increase in every wall-clock second while requests wait. The cited documentation uses a general accumulation-rate description; the actual v7.2 completion paths allow a full second of concurrent waiting with no change to field 11. This is a fixable wording defect, not a reason to discard the lesson or relax R-J.

### Atomic facts

Paths below are relative to the lane. `S180.src` and `S187.src` mean files under `corpus/evidence/sources-r33/`.

| Fact in observation/reading | Quote or NOT STATED | File:line |
|---|---|---|
| The observed record is `/proc/diskstats`. | “What: /proc/diskstats”; “The /proc/diskstats file displays the I/O statistics” | `corpus/evidence/sources-r33/S187.src:1,5-6` |
| Its field 11 measures time spent writing. | “11 time spent writing (ms)” | `corpus/evidence/sources-r33/S187.src:20` |
| The unit is milliseconds. | “11 time spent writing (ms)” | `corpus/evidence/sources-r33/S187.src:20` |
| The reading concerns write ticks, a request-wait-time counter. | “write ticks milliseconds total wait time for write requests”; “These values count the number of milliseconds that I/O requests have waited on this block device.” | `corpus/evidence/sources-r33/S180.src:36,75-79` |
| Multiple requests waiting simultaneously are the relevant condition. | “If there are multiple I/O requests waiting” | `corpus/evidence/sources-r33/S180.src:79-80`; Gate at `corpus/lessons/round-33.md:15` |
| A tick accumulation rate greater than 1000 per second is possible. | “these values will increase at a rate greater than 1000/second”; example: “if 60 read requests wait for an average of 30 ms, the read_ticks field will increase by 60*30 = 1800.” | `corpus/evidence/sources-r33/S180.src:80-82` |
| Concurrent waiting guarantees a gain greater than 1000 in **each** wall-clock second. | **NOT STATED as a per-snapshot-window guarantee.** The closest quote describes a rate and a sum of request waits, not a mandatory update in each sampled second. Completion accounting below supplies a counterexample. | Row wording: `corpus/knowledge/disk-write-rate-r33.md:25`; closest source: `corpus/evidence/sources-r33/S180.src:78-82` |

The source example is specifically read requests affecting `read_ticks`, and the field table calls write ticks the wait time **for write requests** (`S180.src:36,81-82`). Explicitly saying “write requests” also removes the original reading's unnecessary ambiguity about which requests contribute.

### Strongest counterexample: ordinary enabled accounting, no completion inside the window

[INFERENCE — static path trace, not a host I/O experiment.] Start two accounted write requests before the first sample; let both remain outstanding beyond the second sample, exactly one second later; allow no other write completion in between.

1. `blk_account_io_start` sets `RQF_IO_STAT` and `start_time_ns`, updates `io_ticks`, and increments in-flight count. It does not add request duration to `nsecs` (`corpus/evidence/sources-r33/S185.src:1090-1117`).
2. `blk_account_io_done` adds `now - req->start_time_ns` to `nsecs[sgrp]` at completion (`corpus/evidence/sources-r33/S185.src:1069-1087`). The containing completion path calls it at `S185.src:1119-1133`.
3. Reading diskstats can update `io_ticks`, but field 11 is printed from the stored `stat.nsecs[STAT_WRITE] / NSEC_PER_MSEC`; the read does not charge pending write durations to that counter (`corpus/evidence/sources-r33/S182.src:1374-1395`).
4. Therefore both sampled field-11 values can be identical: delta **0 ms**, despite two write requests waiting concurrently throughout the second. This falsifies the literal “for each wall-clock second” guarantee, not the weaker “can exceed 1000/s” lesson.

The bio-based accounting path has the same separation: start accounting updates `io_ticks` and in-flight count; end accounting adds the elapsed duration to `nsecs[sgrp]` (`corpus/evidence/sources-r33/S184.src:1076-1085,1100-1113`). The counterexample does not depend on disabled statistics, reset, overflow, or unusual hardware.

These additional committed files are attack evidence only. Row 7 cites neither S182 nor S184 nor S185; they cannot silently become its support under R-J (`corpus/knowledge/disk-write-rate-r33.md:25`; `.ufo/waves/round-33/contract.md:47-50`).

### Verdict-follows judgment

**Yes.** The reading's greater-than-1000-ms-per-second behavior permits a ratio above one, whereas an occupied-wall-time fraction cannot exceed one. The prohibition on presenting this as a percentage of time needs no additional kernel fact. That logical consequence does not repair the reading's overstrong per-second guarantee.

### Smallest safe correction

Change only the reading cell to:

> With concurrent write requests, this counter can gain more than 1000 milliseconds per wall-clock second

Keep the observation, verdict, and sources `S187, S180` unchanged. “Can” preserves exactly the supported capability without claiming continuous or per-window charging; “write” follows `S180.src:36`. Supporting passages remain `S187.src:20` and `S180.src:75-82`. No new source or claim-boundary change is needed.

## A1 six-word copying check — none found

Read all four Gate quotes for each cited ID, S180 and S187 (`corpus/lessons/round-33.md:15,22`). Executed a Python text-only comparison of the transcribed reading against each of those eight quotes, using lowercase `[a-z0-9_]+` tokens and intersections of all six-token windows. This matches the normalization and window rule at `.ufo/waves/round-33/count-c1-a1.py:86-87,268-275`; the counter itself was not run.

Executed comparison: `grams6(reading) & grams6(quote)` for every cited Gate quote, where `grams6` tokenizes with `re.findall(r'[a-z0-9_]+', text.lower())` and collects `tuple(words[i:i+6])`.

Observed output:

```text
reading_words=22
S180 Q1: shared_6grams=[]
S180 Q2: shared_6grams=[]
S180 Q3: shared_6grams=[]
S180 Q4: shared_6grams=[]
S187 Q1: shared_6grams=[]
S187 Q2: shared_6grams=[]
S187 Q3: shared_6grams=[]
S187 Q4: shared_6grams=[]
total_shared_6grams=0
proposed_reading_shared_6grams=[]
```

## Version boundary and checks performed

- Row 7 makes no row-specific version-transition claim; the entry limits its facts to Linux v7.2 (`corpus/knowledge/disk-write-rate-r33.md:25,55-56`). No incorrect version boundary was found in this scoped review. The additional iostats passage says nanosecond precision began in 4.19 and is truncated for display; it does not establish guaranteed per-second growth (`corpus/evidence/sources-r33/S181.src:123-124`).
- Read R-J and Amendment A1, the full row and its surrounding scope, all S180/S187 Gate quotes, and both complete cited committed copies, including the quoted passages' surroundings.
- Inspected the committed v7.2 request/bio accounting and diskstats-export paths cited above; searched the committed S182-S186 copies for `nsecs` update/export sites. Read `corpus/SOURCES.md:186,193` and the wave-1 S180 report for provenance context; no live-source identity claim was added.
- Ran only the described text-overlap calculation. No canonical judge/counter, build, tests, host I/O workload, Git/JJ write, or device-setting change was run. No tools were installed or updated; no background job was started.
