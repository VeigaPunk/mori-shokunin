# AttackRow12 — sysfs stat versus /proc/diskstats

## Scope and axes

Review only of row 12 at `corpus/knowledge/disk-write-rate-r33.md:30`, using the working-tree copies permitted by the assignment for measured revision `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8`. This is advisory evidence, not the C1 judge receipt.

Axes: depth (atomic source entailment), operability (shared-parser instruction), calibration (schema sameness versus value equality), and freshness (the Linux v7.2 boundary). Governing checks: `.ufo/waves/round-33/contract.md:47-50` (R-J), `:119-123` (A1), and the entry's version limit at `corpus/knowledge/disk-write-rate-r33.md:55-56`.

## Atomic facts

All paths below are lane-relative. S180 and S181 are the row's own citations (`corpus/knowledge/disk-write-rate-r33.md:30`). Their complete Gate cells are `corpus/lessons/round-33.md:15-16`.

| fact | quote or NOT STATED | file:line |
|---|---|---|
| Observation: `/sys/block/<dev>/stat` is a device-statistics interface. | "This file documents the contents of the /sys/block/<dev>/stat file." | `corpus/evidence/sources-r33/S180.src:5` |
| Observation: `/proc/diskstats` is the other disk-statistics interface. | "The kernel exposes disk statistics via ``/proc/diskstats`` and ``/sys/block/<device>/stat``." | `corpus/evidence/sources-r33/S181.src:5-6` |
| Observation: the sysfs file can be matched to the same device's procfs record. | "``/sys/block/<device>/stat`` contains the fields for ``<device>``. In ``/proc/diskstats`` the fields are prefixed with the major and minor device numbers and the device name." | `corpus/evidence/sources-r33/S181.src:22-25`; concrete matching `nvme0n1` records at `:12,16-17` |
| Reading: the two interfaces carry the same statistics. | "Both files contain the same 17 statistics." | `corpus/evidence/sources-r33/S181.src:22`; Gate `corpus/lessons/round-33.md:16` |
| Reading: their statistics number 17. | "Both files contain the same 17 statistics." | `corpus/evidence/sources-r33/S181.src:22`; Gate `corpus/lessons/round-33.md:16` |
| Reading: the sysfs file is exactly one line. | "The stat file consists of a single line of text containing 17 decimal values separated by whitespace." | `corpus/evidence/sources-r33/S180.src:21-22`; Gate `corpus/lessons/round-33.md:15` |
| Reading: that line has 17 numbers. | "The stat file consists of a single line of text containing 17 decimal values separated by whitespace." | `corpus/evidence/sources-r33/S180.src:21-22`; Gate `corpus/lessons/round-33.md:15` |
| Reading: those numbers are decimal. | "17 decimal values" | `corpus/evidence/sources-r33/S180.src:21` |
| Reading: whitespace separates those numbers. | "values separated by whitespace." | `corpus/evidence/sources-r33/S180.src:22` |

No observation or reading atom above is NOT STATED. This finding uses only the row's cited copies for support; S182 below is an adversarial cross-check, not substitute provenance.

## Verdict-follows judgment

**Yes, for the instruction actually written:** "one routine over the 17 statistics" (`corpus/knowledge/disk-write-rate-r33.md:30`) shares the statistics-payload decoder. That follows from the common 17-statistic payload described in the reading. It does not assert that an entire `/proc/diskstats` record is itself 17 numbers, or instruct passing the procfs identification prefix to that decoder. The distinct prefix is explicitly documented in the same cited source (`corpus/evidence/sources-r33/S181.src:22-25`). No unsupported factual premise was found in the verdict as written.

## Strongest attempted counterexamples

### 1. Different raw envelopes — severity: none for the written row

Attack target: `corpus/knowledge/disk-write-rate-r33.md:30`, verdict.

The strongest parser counterexample is already in the cited copy: the procfs example begins `259 0 nvme0n1`, while the sysfs example begins with the first statistic, `255999` (`corpus/evidence/sources-r33/S181.src:12,17`). The source explains the three-field procfs prefix at `:23-25`. Thus a raw 17-integer line parser cannot consume both complete records unchanged [INFERENCE].

That breaks a broader instruction to parse the complete raw records identically, not the row's narrower instruction to share a routine **over the 17 statistics**. No prefix-free procfs claim occurs in its reading. Smallest safe correction: none required for factual support. An optional operability clarification is supplied below; this is not a necessary R-J repair.

### 2. Same statistics does not mean equal samples — severity: none

Attack target: `corpus/knowledge/disk-write-rate-r33.md:30`, reading.

In the source's own examples, the same disk's write-sector value is `36123024` in procfs and `36123056` in sysfs (`corpus/evidence/sources-r33/S181.src:12,17`). This would refute guaranteed equality between separately acquired samples. The row claims common statistics, not equal sampled values. Both kernel printing paths separately call `bdev_count_inflight`, update ticks when appropriate, and call `part_stat_read_all` (`corpus/evidence/sources-r33/S182.src:1065-1071,1374-1380`); neither supplies a cross-file simultaneous snapshot. Smallest safe correction: none; do not expand "same statistics" into sample equality.

### 3. Printer paths and version boundary — severity: none

Attack target: `corpus/knowledge/disk-write-rate-r33.md:30`, 17-statistic claim.

The sysfs implementation emits 17 conversion fields followed by a newline (`corpus/evidence/sources-r33/S182.src:1072-1099`). The procfs implementation emits major/minor/name first and then the corresponding statistics, including discard and flush counters (`:1381-1409`). Its own comment says it "Uses the same stats that the sysfs entries do" (`:1346-1348`). I found no alternate output branch inside these two printers that contradicts row 12.

The cited documentation's historical four-field partition paragraph (`corpus/evidence/sources-r33/S181.src:129-150`) cannot establish a current v7.2 counterexample: the same section restores the full partition statistic set in 2.6.25 (`:165-166`). The entry expressly limits its facts to v7.2 and warns earlier kernels can differ (`corpus/knowledge/disk-write-rate-r33.md:55-56`). Smallest safe correction: none; no unsupported introduction-version claim occurs in row 12.

## A1 six-consecutive-word check

Manual case-folded letter/digit/underscore-token comparison of row 12's entire reading against all eight Gate quotes for S180 and S181: **no shared six-word run**. The longest shared run is four tokens, `the same 17 statistics`, from the S181 equivalence quote. The S180 format quote uses `single line of text containing 17 decimal values separated by whitespace`, whereas the reading uses `exactly one line of 17 decimal numbers split by whitespace`; these do not share six consecutive tokens. Evidence: `corpus/knowledge/disk-write-rate-r33.md:30`, `corpus/lessons/round-33.md:15-16`; normalization rule: `.ufo/waves/round-33/contract.md:119-123`.

## Minimal rewrite

No unsupported fact was found, so no required rewrite is proposed. If the integration owner wants the payload/envelope distinction explicit rather than implicit, this optional change stays within the existing cited sources:

- Reading: "Each interface exports seventeen common statistics. Sysfs places them on one whitespace-delimited decimal line; procfs puts major, minor and device name before that payload."
- Verdict: "Remove procfs's three identification fields, then use the same decoder for either seventeen-statistic payload."
- Sources: retain S181, S180. Prefix evidence is `corpus/evidence/sources-r33/S181.src:22-25`; sysfs format evidence is `corpus/evidence/sources-r33/S180.src:21-22`. This reading introduces no six-token match with the current cited Gate quotes (manual comparison against `corpus/lessons/round-33.md:15-16`).

## Checks and limits

Read R-J/A1; decomposed every observation and reading assertion; opened both cited Gate rows and all surrounding source text; examined the two v7.2 printing paths; checked the cited historical partition narrowing; manually compared all cited Gate quotes for A1. These are source-review checks, not runtime tests. No live URL fetch, counter, C1 judge, build, lint, test suite, git/jj command, tool installation, background job, or subagent was run. Only this assigned report was written.
