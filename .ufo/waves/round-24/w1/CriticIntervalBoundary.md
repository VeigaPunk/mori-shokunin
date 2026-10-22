# CriticIntervalBoundary — round 24 wave 1, claim C2 `--interval` mode

Seat: critic, read-only. Target: `.ufo/waves/round-24/contract.md:66-68` (the `--interval`
clause) and the shared cases interface in the wave context, checked against
`PROVINCE.md:49` (FR6) and `PROVINCE.md:55` (FR12). Lane tip read: `4059ffb`. The tool
(`tools/mori-pressure.py`) and the frozen cases (`tools/fixtures/mori-pressure/cases.json`)
were not landed or drafted in the sandbox when I looked (`/fast/scratch/hyaku/mori-r24-a2/wt-pressure/tools`
had no `mori-pressure.py`, and `wt-cases` had no fixture directory). So this attacks the
contract text and the case interface, not an implementation.

## Sources opened (all fetched 2026-10-22, kept in `/tmp/cib/`)

| File | URL | sha256 |
|---|---|---|
| psi.rst | `https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst` (188 lines) | `11c6b712…dece37b82692` |
| psi.c | `…/v7.2/kernel/sched/psi.c` (1725 lines) | `452318beaca3e6d1…` |
| cputime.c | `…/v7.2/kernel/sched/cputime.c` | `5c9a5f92d5b359c6…` |
| sched.h | `…/v7.2/kernel/sched/sched.h` | `44e7152a593bade4…` |
| tsc.c | `git.kernel.org …/plain/arch/x86/kernel/tsc.c?h=v7.2` (raw.githubusercontent returned HTTP 429 twice) | `1937481d…` |
| clock.c | `git.kernel.org …/plain/kernel/sched/clock.c?h=v7.2` | `efea491e…` |

Host, observed with read-only commands: kernel `7.2.11-arch1-1`, 32 CPUs, `CONFIG_PSI=y`,
`CONFIG_IRQ_TIME_ACCOUNTING=y`, `CONFIG_HZ=1000`, load average 5.94 to 5.99 during the measurements.

## Answers to the three questions

**1. Is a two-sample total delta inside a one-shot probe's latency budget? No.**
The FR6 budget that `PROVINCE.md:49` refers to is the round-8 rule: "implement a
windowed (two-sample) rate **iff the 0.2 s variant adds < 50 ms median wall time**"
(`corpus/knowledge/surfaces-r8.md:47-48`). The disk rate failed that rule because
"the dwell is the entire cost" (`surfaces-r8.md:75-78`). PSI fails it the same way.
I measured with `python3 -I /tmp/cib/measure.py`, which opens the files read-only:

```
one-shot four-file read ms: median 0.012 p90 0.013 max 0.032
S=0.001: added wall ms median 1.1 …; memory elapsed/S median 1.0656
S=0.05:  added wall ms median 50.1 …; memory elapsed/S median 1.0016
S=0.2:   added wall ms median 200.1 …; memory elapsed/S median 1.0005
S=1.0:   added wall ms median 1000.1 …; memory elapsed/S median 1.0001
```

The reads cost about 0.012 ms, so the added latency is almost exactly S. Under the
contract bound `0 < S ≤ 10` (`contract.md:66`), any S above roughly 0.05 s breaks the
50 ms budget. The maximum, 10 s, is 200 times the budget and five times the 2 s
bound on the census's own tmux probe (`surfaces-r8.md:97-98`). FR12 itself is not
breached: a bounded two-read dwell is not the "resident" trigger watcher that
`PROVINCE.md:55` excludes. That holds only if the tool opens the files read-only,
because writing to them registers a trigger (psi.rst:77-81). The after-value command
cannot see any of this: the selftest swaps in a no-op sleep (wave-context case
interface), so `PASS 12/12` measures no latency.

**2. Is `stall_ratio = total_delta_us / (S * 1e6)` a correct reading of `total`?
The units and the cross-CPU aggregation are right. The denominator and three edge
cases are not.**
- Units: `total` is the "total absolute stall time (in us)" (psi.rst:62-63). The kernel
  stores nanoseconds and divides by `NSEC_PER_USEC` when the file is read
  (psi.c:1286-1287). Dividing microseconds by `S * 1e6` gives a unitless fraction.
  That fraction is on a 0–1 scale, while `avgN` is a percentage (psi.rst:60, "The ratios
  (in %)"). It has to be labeled as a fraction, never compared with `--warn-avg10`.
- Cross-CPU aggregation: psi.rst does not describe it. It only defines `some` and `full`
  as a "share of time" (psi.rst:45-55). The source has the rule:
  `tSOME = sum(tSOME[i] * tNONIDLE[i]) / tNONIDLE` (psi.c:125-133), and in code each CPU's
  stall time is weighted by its non-idle time "normalized to wall clock time"
  (psi.c:372-394, 409-411). So `total` is already a non-idle-weighted average over CPUs
  measured in wall-clock time, not a sum of CPU-seconds. Dividing by wall time without
  dividing again by the CPU count is therefore correct, for both `some` and `full`.
- Defects are listed under Counterexamples below: system cpu `full`, the nominal-S
  denominator, ratios above 1.0, and intervals too short to carry data.

**3. Can a decreasing `total` occur legitimately? Not within one boot for the system
group.** `group->total[...]` only ever increases (`+=` at psi.c:409-411). The read path
only divides it (psi.c:1286-1287). It is a u64 nanosecond count, so wrapping needs about
584 years of accumulated stall [INFERENCE: 2^64 ns]. Reading the file runs the collection
step first (psi.c:1266-1271), so two reads in order are non-decreasing. A decrease can
only mean a different object (another `--root`, a fixture, a remount) or a reader or
kernel fault. `counter_regressed` is a correct conservative state. It must not be
described as a counter wrap or reset, and it must never yield a delta.

## Counterexamples (strongest first)

**CE1 — system cpu `full` turns into a numeric "no stall" reading in interval mode.**
The case interface says each `some`/`full` object carries `total_delta_us` and
`stall_ratio` "with --interval". For system cpu `full` the kernel reports zero by
construction: "CPU full is undefined at the system level … set to zero"
(psi.rst:57-58), and in code `total = 0` is never filled for `psi_system` + `PSI_CPU` +
`full` (psi.c:1282-1288). Live host: `cpu` `full … total=0` while `cpu` `some … total=1473454`.
Interval mode would therefore print `full: {total_delta_us: 0, stall_ratio: 0.0}` for cpu.
That is exactly the reading `contract.md:59-60` ("never read as evidence of no stall")
and `PROVINCE.md:55` forbid. `full_system_undefined: true` sits on the resource, but the
number itself is a plain zero ratio. Classification: fixable defect.

**CE2 — irq can legitimately switch from ok to unsupported between the two reads, and the
contract does not say what happens then.** `psi_show` returns `-EOPNOTSUPP` for irq
whenever `!irqtime_enabled()` (psi.c:1260-1262). That key can be turned off at runtime:
the clocksource watchdog marks the TSC unstable (tsc.c:1126-1134), which calls
`clear_sched_clock_stable()` (clock.c:182-199) and schedules `__sched_clock_work`, which
calls `disable_sched_clock_irqtime()` (clock.c:155-176). That function turns off the
`sched_clock_irqtime` static key (cputime.c:36-40; key checked at sched.h:3490-3494).
This host has `CONFIG_IRQ_TIME_ACCOUNTING=y`, so the path exists here. I did not trigger
it. The contract (`contract.md:66-68`) defines only `counter_regressed`. It does not say
what a resource reports when the two snapshots have different states. It also does not
say which snapshot's `avg10` feeds `PRESSURE_HIGH` in interval mode. Classification:
fixable defect (missing rule).

**CE3 — the nominal-S denominator overstates the ratio, and the frozen interface prevents
fixing it in place.** The delta spans the real gap between the two reads of the same file,
which is S plus sleep overshoot plus the time to read the other files. Measured
`elapsed/S` on this host was 1.0656 at S=0.001 and 1.0016 at S=0.05. Round 8, at load
around 100, saw `sleep 0.2` take 206 ms (`surfaces-r8.md:53`), about 3% over. Dividing by
the measured elapsed time would fix the bias, but the selftest's no-op sleep makes that
time close to zero, so P11 would divide by nearly nothing. The interface therefore forces
the nominal S. Classification: tradeoff. It is acceptable only if the ratio is labeled
nominal and the measured elapsed time is also reported.

**CE4 — a ratio above 1.0 can be legitimate.** The kernel says lockless sampling lets
"recorded time deltas … slip into the next period, which under full pressure can result
in samples in excess of the period length" (psi.c:552-557). It clamps only the averages
(psi.c:569-570). `total` is never clamped (psi.c:409-411). Together with CE3, a fully
stalled resource over a short S can show `stall_ratio > 1`. The tool must not clamp that
value or mark it malformed. Classification: documentation and labeling only.

**CE5 — very short intervals can read zero during a real stall.** Each CPU's weight is
`nsecs_to_jiffies(times[PSI_NONIDLE])`, which truncates to whole jiffies
(psi.c:389-393). The per-CPU snapshot advances whether or not the time gets weight
(psi.c:311-312). If every CPU had less than one jiffy of non-idle time since the last
collection, the summed weight is 0. The total then grows by `0 / max(0,1) = 0`, and that
stall time is lost for good [INFERENCE from source; not exercised under real stall]. Every
read of a `/proc/pressure` file triggers a collection (psi.c:1268), so the tool's own four
reads and any other reader split the window. With HZ=1000 here, S=0.001 is one jiffy.
The contract's lower bound is only `0 < S`. Classification: fixable bound.

**CE6 — psi.rst does not cover irq at all.** psi.rst lists only "cpu, memory, and io"
(psi.rst:38-39, 183-185). irq `full` is charged IRQ time (psi.c:1040). It is not added
for the idle task (psi.c:1017-1018) or when the previous and current tasks share a PSI
group (psi.c:1021-1022). The time builds up from `rq->psi_irq_time` and is charged at the
next eligible call (psi.c:1024-1028), so short-interval irq deltas can arrive in lumps
[INFERENCE]. Any irq row in the knowledge entry or decision table (`contract.md:92-95`)
has to cite psi.c, not the PSI documentation. Classification: provenance fix.

## Impacted axes

- **Coverage (C2 claim scope):** if the SCORECARD or Core row counts `--interval` as part
  of the "one-shot system PSI reading" (`contract.md:46-49`), the row claims a two-sample
  measure that fails the FR6 budget.
- **Calibration:** CE1 prints a false zero. CE3 and CE4 produce unlabeled values above 1.
  CE5 can print a false zero.
- **Operability:** up to 10 s of added latency on a probe described as one-shot.
- **Freshness/provenance:** CE6.

## Smallest safe correction (for L1; I made no edits)

1. Scope: list `--interval` as an explicit opt-in mode that is outside the one-shot Core
   row and never called by the census. Record next to it that it fails the 50 ms FR6
   budget (`surfaces-r8.md:47-48`) because its added cost equals S. Leave a no-dwell
   interval delta in FR12 or FR6 Frontier. The after-value stays `--selftest`.
2. CE1: for system cpu `full`, emit `total_delta_us: null` and `stall_ratio: null` with a
   note, never `0`. If frozen P11 already expects a numeric cpu `full` ratio, that is a
   conflict between the contract and the case. L1 has to rule on it; it must not be
   resolved quietly in the tool.
3. CE2: per resource, if the two snapshots have different states, report the worse
   state with no delta and count it toward `PRESSURE_PARTIAL`. State which snapshot's
   `avg10` drives `PRESSURE_HIGH` (suggest the second).
4. CE3 and CE4: keep the frozen formula. Add a measured `elapsed_us` per resource. This
   is additive, and the interface's subset matching keeps P11 valid. Label `stall_ratio`
   as a nominal-interval fraction (0–1 scale, not percent) that may exceed 1.0. Never
   clamp it.
5. CE5: raise the lower bound to `S ≥ 0.5`. That is the kernel's own minimum tracking
   window (psi.rst:102), and the existing upper bound of 10 s already mirrors that same
   line and `WINDOW_MAX_US` (psi.c:167). Alternatively, document that shorter S can read zero.
6. Question 3: say that `counter_regressed` counts like `malformed` toward
   `PRESSURE_PARTIAL` (`contract.md:72` currently names only unavailable or malformed),
   with null deltas and a note that it means a different object or a fault, not a wrap.
7. CE6: cite psi.c for every irq statement.

## Not run or not established

- No implementation or frozen `cases.json` existed to execute. No P11 or P12 behavior
  was checked.
- CE2's runtime disable path is shown only from source; I did not cause or watch a TSC
  unstable event. CE5's zero-weight loss is from source only and was not reproduced
  under stall. Latency numbers come from a quiet host (load about 6), not wave load.
- I did not open the call sites of `psi_account_irqtime` in `core.c`.
- No writes to `/proc`, `/sys` or cgroups. Files were opened read-only, no triggers were
  registered, and nothing in the lane repo was written except this report. No tools
  were installed or updated.
