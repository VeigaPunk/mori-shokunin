# AttackRow13 — since-boot average

Scope: row 13, `corpus/knowledge/disk-write-rate-r33.md:31`, revision `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8`. This is a critic report, not the canonical judge receipt. R-J is frozen at `.ufo/waves/round-33/contract.md:44-50`; Amendment A1's six-word condition is at `:119-123`.

Axes: **depth** (correct averaging window), **calibration** (a label must not overstate what survived a reset), and **operability** (a reader must not mistake mismatched numerator/denominator epochs for throughput). These are the impacts of the defects below, not score judgments.

## Finding 1 — major: unsupported observation and false averaging claim

Attack: `corpus/knowledge/disk-write-rate-r33.md:31`, observation and reading. The row cites only S181. Its Gate row is `corpus/lessons/round-33.md:16`; the committed copy is `corpus/evidence/sources-r33/S181.src`. I read the complete copy, including the surroundings of all four Gate quotes (`:22`, `:33-37`, `:75-80`).

### Per-fact support table

“NOT STATED” means no statement in the row's own cited copy supports that fact; uncited lane code does not cure R-J.

| Atomic fact | Quote or NOT STATED | file:line |
|---|---|---|
| Observation: the census computes the quantity being described | **NOT STATED.** The document describes kernel interfaces, not the lane census. | `corpus/evidence/sources-r33/S181.src:1-187`; interfaces at `:5-7` |
| Observation: the calculation divides sectors written by uptime | **NOT STATED.** No uptime divisor or write-rate formula is given. | `corpus/evidence/sources-r33/S181.src:1-187` |
| Observation: that quotient is a since-boot average | **NOT STATED.** Boot is a reset condition, not a guarantee that the present value retains all writes since boot. | `corpus/evidence/sources-r33/S181.src:33-37` |
| The sectors-written field is a total counter | “Field 7 -- # of sectors written (unsigned long)” and “This is the total number of sectors written successfully.” | `corpus/evidence/sources-r33/S181.src:64-65` |
| Reading: this counter is cumulative | “All fields are cumulative, monotonic counters, except for field 9” | `corpus/evidence/sources-r33/S181.src:33-34` |
| Reading: it resets at boot | “The remaining fields reset at boot” | `corpus/evidence/sources-r33/S181.src:34` |
| Reading: it resets on device reattachment | “The remaining fields reset at boot, on device reattachment” | `corpus/evidence/sources-r33/S181.src:34-35` |
| Reading: it resets on reinitialisation | “device reattachment or reinitialization” | `corpus/evidence/sources-r33/S181.src:35` |
| Reading: it resets when its underlying counter overflows | “or when the underlying counter overflows.” | `corpus/evidence/sources-r33/S181.src:35-36` |
| Reading: dividing the present value by uptime gives a mean over the counter's whole life | **NOT STATED, and false after a reset:** the denominator is not the age of the surviving count. | `corpus/evidence/sources-r33/S181.src:33-37`; counterexample below |
| Reading: that mean can straddle a reset | **NOT STATED.** The document names resets but never claims that a post-reset value retains the pre-reset total needed for such a mean. | `corpus/evidence/sources-r33/S181.src:33-37` |

Uncited corroboration does exist for the *implementation*, not its mathematical interpretation: `tools/mori-census.sh:1892-1894` reads field 10 and computes `sectors * 512 / up_s`; `:1907-1908` takes integer uptime seconds; `:1974` emits `io_avg_since_boot`. These files are not S181. Even adding an implementation citation would not make the quotient a genuine lifetime average after reset.

### Strongest counterexample

[INFERENCE — synthetic arithmetic, not a host measurement.] Use a reset explicitly permitted by S181 `:34-37`: at system uptime 90 seconds, a device is reinitialised after 900 sectors have been written. At uptime 100 seconds, its new counter contains 100 sectors.

- Row's quotient: `100 / 100 = 1 sector/s`.
- Mean over the surviving counter's 10-second life: `100 / (100 - 90) = 10 sectors/s`.
- Actual whole-boot mean: `(900 + 100) / 100 = 10 sectors/s`.

The quotient is neither claimed mean. A no-reset history containing only 100 sectors produces the identical observed `(counter=100, uptime=100)` but has a true boot mean of 1 sector/s. Thus the single observation cannot distinguish the two histories. Calling its denominator a boot interval does not restore the discarded numerator.

The same source supplies an additional narrowing: “the per-CPU counters are summed (possibly overflowing the unsigned long variable they are summed to)” (`corpus/evidence/sources-r33/S181.src:117-120`). Consequently, even interpreting “whole life” as an uninterrupted stored counter is not an unconditional exported-total guarantee. No particular counter width or wrap period is asserted here.

The erroneous “lifetime mean” interpretation is repeated outside the table at `corpus/knowledge/disk-write-rate-r33.md:47-50`; a correction to row 13 should not leave that prose asserting it.

## Finding 2 — major: the verdict does not follow in full

Attack: verdict at `corpus/knowledge/disk-write-rate-r33.md:31`.

| Verdict clause | Follows from the reading without another fact? |
|---|---|
| “Label it a since-boot average” | **No.** Even the asserted counter-life mean is not necessarily a boot mean; a reset separates the epochs. The permitted reset above defeats the label as a mathematical claim. |
| “never report it as the current write rate” | A conservative reporting rule consistent with a lifetime-mean premise, but that premise is unsupported and false in the reset case. This clause does not rescue the row. |
| “a current rate needs two readings” | **Not established by this reading.** It introduces a sampling requirement absent from the reading. S181 says to handle resets “when comparing stat snapshots” (`:36-37`), not that two readings are necessary for a current rate or how to derive one. |

This is a fixable content defect, not a tradeoff that permits caveated support. The canonical judge cannot supply the missing uptime/lifetime/sampling facts from uncited code under R-J (`.ufo/waves/round-33/contract.md:47-50`). No canonical verdict was produced by this seat.

### Smallest source-safe replacement using S181 alone

- **Observation:** One sectors-written field value
- **Reading:** It totals successfully written sectors; the count is cumulative but can restart at boot, after device reattachment or reinitialisation, or after an overflow
- **Verdict:** Label it a cumulative count, without claiming an uninterrupted since-boot total
- **Sources:** S181

The supporting statements are S181 `:33-37,64-65`. This removes the unsourced census formula and the false lifetime interpretation rather than attaching a caveat to them. It retains a one-value interpretation distinct from row 4's falling-value comparison (`corpus/knowledge/disk-write-rate-r33.md:22`). Preserving an average/two-reading assertion instead would require a cited committed source that actually states it; S181 does not.

## Six-word check — none found

Against the frozen revision, I extracted row 13's reading and **all four** S181 Gate quotes. Normalisation was `re.findall(r'[a-z0-9_]+', text.lower())`, matching `count-c1-a1.py:86-87,268-275`. Intersection of consecutive six-word tuples was empty:

```text
revision=62db24c01d5b7c2247f43852ea2b28d0ae5e40c8
row=13 cited_ids=S181 gate_quotes=4
reading_words=38 gate_six_word_matches=0
matches=[]
exit=0
```

Executed via Eval `subprocess.run` with command prefix `timeout 25s prlimit --as=268435456 --cpu=10 -- env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python -c`; its inline script used read-only `git show <revision>:<path>` for the entry and Gate table, each bounded by `timeout 8s`. A separate bounded arithmetic computation produced `reported_quotient=1`, `mean_since_last_reset=10`, and `actual_since_boot_mean=10` sectors/s. That computation also found zero six-word matches for the proposed replacement reading against the same four Gate quote strings.

## Additional checks and limits

- Inspected sysstat 12.8.0's committed `S190.src:1473-1517,1800-1806,1984-2006,2306-2308`: it has explicit overflow handling discussion, sample intervals, uptime reads, and a since-boot display flag. These are **not** row 13 citations and were not imported to cure it.
- Row 13 asserts no numerical version boundary. The counterexample uses the reset conditions in its own v7.2 source; no kernel-version extrapolation is needed (`S181.src:33-37`).
- No canonical counter/judge, build, tests, host probes, kernel execution, network fetches, tool installs/updates, background jobs, or subagents were run. Only this report was written.
