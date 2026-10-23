measured 2026-10-23T06:05:56Z

# ExecLatencyBudget — FR6 latency budget against `tools/mori-disk-rate.py` (mori round 34, wave A)

Seat: ExecLatencyBudget (executor). Target revision: lane tip `8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3`.
Judged object bytes: `tools/mori-disk-rate.py`, blob `c7ea8bdac9c98b8d350a489fb8aca3a4750bcfbf`, identical at
`ba525e1a0394154837eea5090e8bd27ed69c539c` and at `8d56809a…`
(`git ls-tree 8d56809a… tools/mori-disk-rate.py` → `100755 blob c7ea8bda…`; working copy sha256
`370932deb525b95135f0c30e4caaf2666b95c6feeffe76b70f06b48c09caa74b` = `git cat-file -p c7ea8bda… | sha256sum`).
Reads only; the lane was not written except this report. Scratch: `/fast/scratch/hyaku/mori-r34/a2-ExecLatencyBudget/`.

## 1. The budget, quoted

`corpus/knowledge/surfaces-r8.md:47-48` — the round-8 condition verbatim:

> The round's condition: implement a windowed (two-sample) rate **iff the 0.2 s variant
> adds < 50 ms median wall time**; else record a deferral-with-measurement.

Carried in the lane at `corpus/README.md:340` (FR6 row): "a two-sample rate stays deferred until its added
latency meets the stated budget", and at `SKILL.md:405-408` ("the 0.2 s-window variant measured ≈208–222 ms
across three independent 15–30× isolations (minimum 208 ms) over the two-read floor against a 50 ms budget;
the dwell is the cost, the reads alone 16 ms median — so it stays out of census runtime on measured grounds").

How r8 applied the bar (this fixes the unit of comparison): the number compared with 50 ms is the **whole
two-sample block's added wall time, dwell included** — `corpus/knowledge/surfaces-r8.md:53-57` measures
"reads + 0.2 s dwell median **229 ms**", and `:75-78` records "the 0.2 s variant's *minimum* over all three
isolations is 208 ms — **4.16× the 50 ms budget**". (208 / 50 = 4.16, and 229/50 = 4.58 — so the bar was
applied to the total, not to the overhead beyond the dwell.) `corpus/README.md:178-182` repeats it
("the two-sample reads + 0.2 s dwell at min 210 / median 229 ms … 4.16× the round's 50 ms bar").

## 2. Method

`/usr/bin/time` is absent on this host (`/usr/bin/time -v true` → `error: command not found`), so per-run
wall / user / sys / max-RSS came from `os.fork` + `os.wait4()` (per-child `getrusage`, so `ru_maxrss` is
per-run, not a running maximum): `scratch/harness.py`, `scratch/interleaved.py`, `scratch/extended.py`,
`scratch/final.py`. Arms are **interleaved** run-by-run (never consecutive medians — the r8 lesson's
rule, `corpus/lessons/2026-10-15-probe-pricing-dwell-bounds-filter-drop.md` §2), each arm 5 runs per batch,
5 batches, host load (1/5/15 min) captured before and after every batch. Live arms write stdout to a file in
the scratch dir; nothing is written to the lane, to a device, or to any setting. No process was left running
(`ps` shows none); every command was `timeout`-capped (≤120 s).

No tool was installed or updated (none needed); recorded per the operator tooling directive:
**tool: none · version: n/a · channel: n/a · reason: the measurement needed only the stdlib
(`os.wait4`, `resource`-free `getrusage` via `wait4`) and `/usr/bin/time` is unavailable; pacman is
PAUSED host-wide for this wave, so the stdlib path was taken.**

## 3. Measurement — the tool's live arm at `--interval-ms 100 / 500 / 1000`, 5 runs each

Arms (all `rc=0`, JSON produced every run): `live-N` = `python3 tools/mori-disk-rate.py --interval-ms N`
(live path, `tools/mori-disk-rate.py:175-183` `read_live_samples`: read → `time.sleep(interval_ms/1000.0)` →
read). `offline-100` = `--a FILE --b FILE` (no dwell). `floor-py` = `python3 -c pass` (interpreter floor).

Per-batch medians (ms), `over` = wall median − the requested interval:

| batch (1/5/15-min load) | floor-py | offline-100 | live-100 (over) | live-500 (over) | live-1000 (over) |
|---|---|---|---|---|---|
| I (quiet) | 7.71 | 26.72 | 127.93 (27.93) | 527.37 (27.37) | 1028.03 (28.03) |
| E (24.2/15.1/14.4) | 8.41 | 36.09 | 143.36 (43.36) | 531.54 (31.54) | 1034.39 (34.39) |
| F2 (15.3/30.6/25.2) | 10.97 | 49.85 | 156.48 (56.48) | 549.53 (49.53) | 1057.56 (57.56) |
| F3 (25.4/31.3/25.8) | 8.61 | 29.08 | 133.01 (33.01) | 531.63 (31.63) | 1035.16 (35.16) |
| F4 (75.2/45.0/31.5) | 22.26 | 80.15 | 187.29 (87.29) | 577.92 (77.92) | 1064.74 (64.74) |

`live-200` (the r8-comparable 0.2 s variant), batch E: wall min 232.18 / median 242.65 / max 264.13 ms
(over 42.65 ms).

Per-run maxima across all 5 runs of the assignment's three intervals (batch F3, the quietest well-loaded batch):
`live-100` min 129.90 / med 133.01 / max 135.00, spread 5.10 ms; `live-500` min 529.96 / med 531.63 /
max 534.97, spread 5.01 ms; `live-1000` min 1027.92 / med 1035.16 / max 1036.43, spread 8.51 ms.
Best (lowest) batch medians overall: 127.93 / 527.37 / 1028.03 ms; overall minima 126.73 / 526.09 / 1027.83 ms.

**CPU and max RSS** (per-run `wait4` rusage; user+sys = CPU):

| arm | user+sys median (min–max) | user / sys median | max RSS median (min–max) |
|---|---|---|---|
| live-100 | 27.6 ms (26.3–28.4) | 22.3 / 5.0 ms | 15 248–16 008 KiB |
| live-500 | 26.7 ms (25.8–29.0) | 23.5 / 3.9 ms | 15 412–16 012 KiB |
| live-1000 | 27.7 ms (26.9–28.3) | 23.2 / 4.2 ms | 15 764–16 028 KiB |
| offline-100 | 26.4 ms (25.8–28.0) | 21.8 / 5.0 ms | 15 728 KiB |
| floor-py | 7.5 ms | 5.6 / 1.9 ms | 9 556 KiB |

CPU is **flat across intervals** (the dwell is `sleep`, not work) and RSS is flat at ~15–16 MiB
(interpreter floor ~9.6 MiB). So the added latency is wall-clock only: no CPU or memory budget is at risk.

## 4. The overhead beyond the interval is startup, not reads

Decomposition (`scratch/final.py` + ad-hoc arms, quiet host): bare `python3 -c pass` **7.4 ms**; the same
interpreter importing the tool's modules (`argparse,json,os,re,select,sys,threading,time`) **16.2 ms**;
`mori-disk-rate.py --help` (imports + argparse construction, no work) **33.5 ms**; offline `--a/--b` **31.9 ms**;
offline with `--sysfs <empty dir>` **36.5 ms**; live `--interval-ms 1` **32.9 ms**. One open+read+close of
`/proc/diskstats` costs **0.008 ms median** (min 0.007, max 0.042; n=50); the sysfs class walk is 38
`stat`/`listdir` calls over 11 devices (`/sys/class/block`: dm-0, nvme0n1{,p1,p2}, nvme1n1{,p1,p2}, sda{,1,2}, sr0).

⇒ the ~27–35 ms of overhead beyond the dwell is **interpreter start + module imports + argparse**, not the
two `diskstats` reads and not the sysfs walk (empty-sysfs vs real-sysfs are within noise). r8's "extra reads
alone 16 ms median" was the census's own shell idioms; the two raw reads here are 0.016 ms total.

The tool's own latency behaviour is exactly as documented — no hidden cost. Code sub-finding:
**no defect found** in the latency behaviour (the sleep is one `time.sleep(interval_ms/1000.0)` at
`tools/mori-disk-rate.py:183`; the measured gap between the two reads is the nominal interval + 0.13 ms).

## 5. Two facts that decide the frontier question

**(a) The tool is not in census runtime.** `tools/mori-census.sh` contains **no** call to the tool (the only
`disk-rate` hit is a fixture comment at `tools/mori-census.sh:3199`); `SKILL.md:831` tells the *operator* to
run it. So the landed tool adds **0 ms to the census's one-shot runtime**. FR6's frontier row
(`corpus/README.md:340`) still lists "a two-sample census arm" as frontier, and this measurement says that
arm is still unaffordable: a census-embedded two-sample arm at `--interval-ms 100` would add **≥127 ms**
(2.56× the 50 ms bar; 2.9–3.7× across batches), at 200 ms **232–264 ms** (4.6–5.3×, reproducing r8's
208–229 ms), at 500 ms **≥527 ms** (10.5×), at 1000 ms **≥1028 ms** (20.6×). FR6 stays deferred on
measured grounds, exactly as r8 adjudicated.

**(b) The only intervals that could fit a 50 ms budget measure nothing.** Shrinking the dwell to fit the bar
pushes the window below the aliasing floor (r8 lesson §1: 4 of 10 samples at 0.2 s read 0 B/s on an
actively-writing device). Measured here, `host_write_Bps` over 5–9 reps: interval 1 ms → 0 in 5/5;
5 ms → 0 in 5/5; 10 ms → 0 in 5/5; 15 ms → 0 in 2/9 and 1 in 9; 20 ms → non-zero but rep-to-rep spread
2.8×–58×; 30 ms → 2.0×; 100 ms → 2.1× (one batch 38 769×); 500 ms → 2.1×. And the *cost* of the short
intervals is still ≈48–54 ms of wall (15 ms → 48.0 ms median, 20 ms → 53.4 ms) because the overhead is
startup-bound: **a sub-50 ms wall is reachable only at intervals whose readings are zeros or 10²–10⁴×
noise.**

**(c) The instrument cannot resolve a 50 ms bar at gate level.** The same arm's median moves 127.93 → 187.29 ms
across batches for identical work (Δ59 ms), and within-batch spread reached 96.4 ms (F4 offline) / 78.4 ms
(F4 live-1000); the *overhead beyond the interval* alone ranged 27.4 → 87.3 ms across batches. The r8
lesson's rule (`…probe-pricing-dwell-bounds-filter-drop.md` §2, round-level form): "a budget rule of the shape
'implement X iff cost(X) < T' is decidable only if the instrument's noise is below T." Here the noise equals
or exceeds T, so only the isolated arm is a decision instrument — which is what this report uses.

## 6. Secondary measurement: the divisor is nominal, not measured

The tool computes `(B − A) * 512 * 1000 // interval_ms` from the **nominal** interval
(`tools/mori-disk-rate.py:240`, contract rule R6 at `:59`). Measured true gap between the two reads
(replicating the tool's own read path, 5 reps each): interval 1 → 1.091 ms (**+9.1 %**), 10 → 10.133
(+1.3 %), 100 → 100.128 (+0.13 %), 200 → 200.132 (+0.07 %), 500 → 500.136 (+0.03 %), 1000 → 1000.136
(+0.014 %). The r8 lesson requires the *measured* elapsed as divisor ("`sleep 0.2` was 206–226 ms under this
load"); here the effect is small at the intervals that matter (≤0.13 %) but is ~1–9 % at 1–10 ms. This is
contract-frozen behaviour, not a tool defect — reported as an observation only.

## 7. Answers

- **Does the tool's added latency fit the stated budget?** **No**, on r8's own unit of comparison (the whole
  two-sample block's added wall time, dwell included): ≥127 ms at `--interval-ms 100`, ≥232 ms at 200 ms,
  ≥527 ms at 500 ms, ≥1028 ms at 1000 ms — 2.6×–21× the 50 ms bar, reproducing r8's 4.16× at the 0.2 s
  variant. The overhead *beyond* the dwell (27–35 ms in a quiet batch, 49–87 ms under wave load) is the only
  quantity near the bar, and it is startup-bound and unresolvable against a 50 ms threshold at this host's noise.
- **May FR6 leave the frontier?** **No.** The landed tool is a standalone lane operation (not called by the
  census), so it adds no census latency at all; but the census arm FR6's row still wants
  (`corpus/README.md:340`) is unaffordable at every measured interval, and the only intervals that could fit
  a 50 ms wall return zero or 10²–10⁴×-spread readings. FR6 stays deferred with the measured numbers attached.
- **C1's coverage claim is unaffected by this measurement.** The claim is that the *operation* exists
  (`tools/mori-disk-rate.py`, `rc=0`, JSON with `interval_ms`/`devices`/`host_basis`/`host_write_Bps`; live
  runs here: 11 devices, states `ok`, classes `disk`/`partition`/`stacked`, `host_basis`
  `['nvme0n1','nvme1n1','sda','sr0']`). Latency is not a C1 predicate; this report decides only the
  FR6-frontier question.

VERDICT: unsupported

(Subject of the verdict: the proposition that the tool's added latency meets FR6's stated 50 ms budget and
that FR6 may therefore leave the frontier on latency grounds. Code sub-finding on the tool's latency
behaviour: no defect found — the sleep is one `time.sleep` at `tools/mori-disk-rate.py:183` and the measured
gap is nominal + 0.13 ms.)

## 8. Evidence index (all under the scratch dir)

`interleaved.json` (batch I), `extended.json` (batch E, incl. live-1/10/200 and load), `final-F2.json`,
`final-F3.json`, `final-F4.json` (batches F2–F4, with load before/after), `divisor.json` (measured gaps and
the serial-vs-overlapped in-span price: serial 200 ms span 500.14 ms vs overlapped 300.23 ms — the dwell
hides behind other work, r8's §2(b) result), `live-{100,500,1000}.json` (the tool's own live JSON outputs),
`harness.py`/`interleaved.py`/`extended.py`/`final.py`/`divisor.py` (the runners). Host: 32 CPUs,
kernel 7.2.11-arch1-1, Python 3.14.8, `/proc/diskstats` 11 lines, `/sys/class/block` 11 entries.
Reads only; the tool wrote nothing but stdout (verified: the only `open()` in the tool is `O_RDONLY`
at `:121`, the only write is `sys.stdout.write` at `:295`).
