measured 2026-10-23T06:07:12Z

# LabIntervalError — the tool's rate denominator vs the real time between its two reads

## Axes named (godspeed)

1. **Gap truth** — which syscall instant is the counter snapshot taken at? (`openat` vs `read`)
2. **Gap distribution** — real snapshot-to-snapshot gap vs nominal `--interval-ms`, per interval
3. **Load** — idle vs `stress-ng` vs the literal 32-core python busy loop
4. **Rate error** — implied error in the reported `write_Bps`, and the measured one
5. **Contract reach** — does this threaten P-C1-A1's "reads the file twice ≥ 0.9 × interval apart"?

## Subject under test

`tools/mori-disk-rate.py` at lane tip. Byte-identical at all three revisions
(md5 `d367f8517e413bb6f843af82adacb72b` at `ba525e1a0394154837eea5090e8bd27ed69c539c`,
at `8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3`, and at the current `fd2521351c6cef47384aef30afbe1e4db7e6912e`):

```
git cat-file -p ba525e1a0394154837eea5090e8bd27ed69c539c:tools/mori-disk-rate.py | md5sum  # d367f8517e413bb6f843af82adacb72b
git cat-file -p 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3:tools/mori-disk-rate.py | md5sum  # d367f8517e413bb6f843af82adacb72b
md5sum tools/mori-disk-rate.py                                                              # d367f8517e413bb6f843af82adacb72b
```

Relevant code (`tools/mori-disk-rate.py:175-184`, `:246-249`): `read_live_samples` does
`read_sample(DISKSTATS)` → `time.sleep(interval_ms/1000.0)` → `read_sample(DISKSTATS)`;
the rate is `((b−a) * 512 * 1000) // interval_ms`. The denominator is the **nominal**
`interval_ms`; the numerator is the counter delta between the two samples, so the rate
is only correct if the real elapsed time between the two snapshots equals `interval_ms`.

## Method

Two independent instruments, both measuring the tool's own code path.

**(a) `strace -f -tt -e trace=openat,read`** on the tool process, exactly as the item
prescribes; the two `openat(AT_FDCWD, "/proc/diskstats", …)` lines and the two
data-bearing `read()` lines on that fd are timestamped
(`scratch measure.py`, `scratch analyze.py`; 618 tool-binary invocations under strace).

**(b) An in-process replica** importing the tool's own `read_sample()` and bracketing
each stage with `time.monotonic()` (`scratch nostrace.py`, `scratch sweep.py`; ~1000 more
runs) — no strace overhead, used to confirm the strace numbers and to sweep load levels.

**Load**: `stress-ng` 0.22.01 (already at `/usr/bin/stress-ng`; `--cpu N --cpu-load 100`),
and the item's literal fallback — 32 concurrent `python3 busy.py` loops, one per core
(`nproc` = 32). **No tool was installed or updated by this seat**; `strace` 7.2 and
`stress-ng` 0.22.01 were already present. All load generators were terminated
(`pgrep -cf busy.py` → 0, `pgrep -cf stress-ng` → 0); the only write load was
`rate-writer.bin` under the scratch dir, deleted.

### Axis 1 — the snapshot is taken at `read()`, not at `openat()`

`/proc/diskstats` is a seq_file: the counter values are produced when the file is
**read**, not when it is opened. Measured directly — a fd opened *before* a 1 MiB write
returned the **post-write** counter when read afterwards:

```
live now: 3806598896   pre-opened fd content: 3806598896   before: 3806307928
pre-opened fd content equals pre-write value?  False
pre-opened fd content equals post-write value? True
```

So the honest gap is **first data-bearing `read()` → second data-bearing `read()`**
(`read_gap_ms`), not open→open. `open_gap_ms` is reported alongside as the item's
prescribed metric; the two agree to <0.5 ms in every run (the open precedes its read
by 0.07–0.73 ms).

## Axis 2/3 — gap distribution (read_gap, i.e. the true denominator)

`err% = (real_gap − nominal) / nominal × 100`.

| load | interval_ms | n | gap med | gap max | err% med | err% p95 | err% max | n > 5% |
|---|---|---|---|---|---|---|---|---|
| idle | 200 | 12 | 200.497 | 200.602 | 0.248 | 0.266 | 0.301 | 0 |
| idle | 1000 | 12 | 1000.646 | 1004.482 | 0.066 | 0.312 | 0.448 | 0 |
| stress-ng 96w | 200 | 30 | 200.822 | 203.038 | 0.414 | 1.235 | 1.519 | 0 |
| stress-ng 96w | 1000 | 22 | 1000.748 | 1002.999 | 0.075 | 0.139 | 0.300 | 0 |
| stress-ng 220w | 200 | 75 | 200.948 | 211.324 | 0.474 | 3.643 | **5.662** | **1** |
| stress-ng 220w | 1000 | 54 | 1000.583 | 1008.163 | 0.058 | 0.347 | 0.816 | 0 |
| **busy loop ×32** | **200** | **60** | 201.781 | 212.850 | 0.892 | 3.676 | **6.425** | **1** |
| **busy loop ×32** (replicate) | **200** | **70** | 203.160 | 211.535 | 1.590 | 4.146 | **5.768** | **3** |
| busy loop ×32 | 1000 | 40 | 1001.824 | 1033.161 | 0.194 | 0.738 | 3.316 | 0 |

All gap figures in ms. Percentile p95 computed over the sorted absolute errors.
Raw per-rep data and the strace traces are under
`/fast/scratch/hyaku/mori-r34/a2-LabIntervalError/` (`{base,load,sel,tail,busy,c300,c400}*.json`).

**Direction is one-sided.** Across every run — 800+ gaps — the real gap was **never
shorter** than nominal: min(gap)/nominal = **1.00038**. The excess is the sleep
overrun plus the open/read latency of the second sample that the nominal denominator
does not account for. Raw worst-case evidence, `scratch tail200/trace-tail200-044.txt`:

```
openat(AT_FDCWD, "/proc/diskstats", O_RDONLY|O_CLOEXEC) = 3   10335.622595
openat(AT_FDCWD, "/proc/diskstats", O_RDONLY|O_CLOEXEC) = 3   10335.833943   gap 211.324 ms (read-to-read)
```

**Small intervals fail outright**, even idle (in-process replica, n=60 each):
`--interval-ms 1` → err med 11.4%, max 40.0% (60/60 over 5%);
`5` → med 13.7%, max 229% (60/60);
`10` → med 6.2%, max 30.7% (49/60 over 5%);
`20` → med 0.75%; `50` → 0.30%; `100` → 0.17%.
strace-confirmed at 10 ms: med 6.24%, 48/60 over 5%; at 5 ms: med 13.7%, 59/60.

## Axis 4 — implied and measured rate error

The numerator (Δsectors) is measured over the *real* gap; the denominator is the
*shorter* nominal interval, so the tool **overstates** the write rate by
`(gap − nominal)/gap`. Measured end-to-end (writer thread moving the counter,
tool run under strace, `scratch rateerr.py`):

| condition | measured rate error (tool vs true) |
|---|---|
| idle, 200 ms | +0.221% … +0.285% (n=8) |
| load 96w, 200 ms | +0.227% … +0.549% (n=10) |
| load 220w, 200 ms | +0.390% … +1.834% (n=12) |

The error is always positive — the tool never under-reports the rate.

## Axis 5 — does this threaten the judged predicate?

No. P-C1-A1 requires the tool to "read the file twice at least **0.9 × interval_ms**
apart". The measured gap is **always ≥ 1.00038 × interval_ms**, so the predicate's
floor holds with ≥ 11% margin at every interval and load measured. The live `write_Bps`
value is unaffected too: the counter's own oracle (`count-c1-a1.py:101`) uses the same
nominal `interval_ms` denominator, so the tool and the oracle agree regardless of the
real gap — this is a property of the contract's own R6 formula, not a tool deviation.

For reference, the two timing-sensitive intervals the counter actually uses
(`count-c1-a1.py:261` live → 300 ms; `:312` fed-live → 400 ms), measured under the
32-core busy loop: **300 ms** → med err 1.13%, max **6.256%** (4/50 over 5%);
**400 ms** → med 0.90%, max 4.392% (0/45 over 5%). Both stay above 0.9 × interval.

## Defect assessment against the contract

The tool implements R6 exactly as the contract states it
(`contract.md:46`: "An `ok` rate is `(B − A) * 512 * 1000 // interval_ms`"). Nothing
here contradicts R1–R7, so **no contract defect is asserted** and the counter, rules and
seed are untouched.

One **documentation** inaccuracy is worth reporting, since the tool is the judged
object and its own docstring makes the accuracy claim the item attacks
(`tools/mori-disk-rate.py:178-180`):

> "the second open starts one full interval after the first sample was closed,
>  so the interval the rate divides by is the time between the readings."

The first clause is true; the second does not follow. The `sleep()` starts *after* the
first sample is closed, so the time between the two readings is
`sleep + (close→open→read latency of the second sample) + sleep overrun`, which the
measurement shows is **always larger** than the divisor. The sentence asserts an
equality that does not hold (measured: +0.07% to +6.43%). Reported, not fixed.

## Hypothesis verdict

The hypothesis stated: the denominator differs from the real time between the two reads
by **less than 5% at `--interval-ms` 200 and 1000, also under CPU load**.

- At `--interval-ms 1000`: **supported**, under every load tested — max error 3.32%
  (busy loop), 0.82% (stress-ng 220w), 0.45% (idle); 0 of 116 runs exceeded 5%.
- At `--interval-ms 200`: **supported at idle** (max 0.30%) and under moderate load
  (max 1.52%), but **falsified under the item's own prescribed CPU load** — the 32-core
  busy loop gave max **6.43%** (1/60) and, in the replicate, max **5.77%** with
  **3/70** runs over 5%; `stress-ng --cpu 220` gave max **5.66%** (1/75).
- The failure is one-sided (the gap is never shorter than nominal), so the tool's
  reported rate is biased **high**, by up to ~6% at 200 ms under load.
- Separately and far more severely: at `--interval-ms` ≤ 10 the 5% bound fails even
  idle (11–14% median error), because the fixed per-sample open/read latency is a
  large fraction of a short interval.

VERDICT: unsupported

(The hypothesis is only partly true: it holds at 1000 ms and at idle/light load at
200 ms, and fails in the tail at 200 ms under the CPU load the hypothesis names.
No contract defect; the tool's rate denominator follows the contract's R6 formula
exactly. The single reportable inaccuracy is the docstring claim at
`tools/mori-disk-rate.py:178-180`.)

## Risks / limits

- The machine was already carrying unrelated load (loadavg 12–70 during the sweeps),
  so the idle rows are "idle for this seat", not "idle host".
- Tail percentages are rare-event estimates: 1/60 and 3/70 are 1.7% and 4.3% sample
  rates with wide confidence intervals; the *direction* and the "never shorter than
  nominal" invariant are the robust findings, the exact tail rate is not.
- Nothing was written into the lane except this report; no git/jj mutation, no
  harness, unit, or fleet-script edits; no block device created or written; every
  command was `timeout`-capped and every load process tree killed.

## Files

- Report: `.ufo/waves/round-34/wa/LabIntervalError.md` (this file; the only write into the lane)
- Scratch (evidence, ~20 MB): `/fast/scratch/hyaku/mori-r34/a2-LabIntervalError/`
  — `measure.py`, `analyze.py`, `nostrace.py`, `sweep.py`, `rateerr.py`, `busy.py`,
  `*.json` summaries, and the raw `strace` traces (`tail200/trace-*.txt` etc.).
