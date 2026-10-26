# Mo49ExecCounterTiming — cost profile of the pin reconciler under `count-c1.py`

Seat: round 49, wave w1, lane mori-shokunin. Author date 2026-10-25. Subject bytes: the frozen
entering tool `.ufo/waves/round-49/controls/tool-v3-entering.py`, sha256
`85a89a3b6ba4eb5ed0b3f784763cfe78652e6493b055b3dcf8924feaffff82e1` = `tools/mori-pin-check.py` at
the entering tip `b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86` (verified with `sha256sum` on both files,
identical). Counter: `.ufo/waves/round-49/count-c1.py` (frozen), run as
`--rev b3e3453d --min-tally-pins 26 --baseline-rev 2d85e33d`. Scratch:
`.scratch/r49-Mo49ExecCounterTiming/`. No lane file was written; no frozen byte was touched; no tool,
including `pacman`, was installed (none was needed).

Load caveat, stated once and applied everywhere below: **no idle slot existed.** The host carries 32
CPUs and this wave's live siblings plus long-lived parked peers; `/proc/loadavg` (1 min) ran between
13 and 110 during the seat and is reported for every measurement. Wall times are therefore reported
with their window and load, and the comparisons that matter are **paired** (two runs started in the
same window) or use load-independent invariants (CPU seconds, achieved concurrency
`sum(run wall) / counter wall`).

## 1. Counter wall time, --jobs 3, 4, 6, 8

Each counter run was instrumented with a shim (`shim.py`, sha256 `770e2521…`) passed as `--tool`.
The shim runs the real tool with the identical argv and interpreter flags, forwards stdout and the
exit code verbatim, and appends one line per run: SKILL.md sha256 prefix, repo, rev, wall, rc, peak
RSS, child CPU, verdict. Its overhead is one Python process start per invocation, outside the
measured interval: on the 25 full-registry runs (66–190 s) that is ≤0.05 % of wall, and the two
fixture runs (0.1 s) are timed child-only. Every run below produced the freeze receipt's line
`C1=unmet junk_met=9 honest_unmet=0 real=met errors=0 variants=26` — the shim changed no verdict.

| run | window | load (start→end) | jobs | counter wall | runs | Σ run wall | achieved concurrency | Σ child CPU | max run | median run |
|---|---|---|---|---|---|---|---|---|---|---|
| R1 | 22:02:43–22:36:28 | 109.7 → 83.2 | 3 | **2025.2 s** | 27 | 5913.9 s | 2.92 | 665.1 s | 441.8 s | 189.7 s |
| R2 | 22:36:53–22:44:34 | 74.6 → 64.5 | 6 | **461.3 s** | 27 | 2385.8 s | 5.17 | 522.3 s | 107.4 s | 95.3 s |
| R3 | 22:45:04–22:51:13 | 61.2 → 37.6 | 6 | **369.4 s** | 27 | 2017.6 s | 5.46 | 549.6 s | 97.0 s | 72.0 s |
| R4 | 23:06:47–23:20:19 | 73.9 → 57.6 | **3 vs 6, simultaneous** | **812.2 s vs 470.5 s (1.73×)** | 27 each | — | — | — | — |
| R5 | 23:23:45–23:35:38 | 48.6 → 39.2 | **4 vs 8, simultaneous** | **713.2 s vs 465.5 s (1.53×)** | 27 each | — | — | — | — |

R1/R2/R3 are sequential and their windows differ (load fell through the seat), so R1→R2's 4.4× is
**not** a clean jobs effect. R4 and R5 are the controlled measurements: the same counter, the same
27 runs, the same window, both sides started at the same instant (`jobs_pair.sh`,
`jobs_pair2.sh`), each timing itself in its own subshell. Doubling the in-flight count bought
**1.73×** (3→6) and **1.53×** (4→8), not 2×: each tool run is wait-bound (§2), so a slot is mostly
idle wall time and the extra slots on a host already at load 40–60 were partly absorbed by sibling
work rather than claiming idle cores — the exact conditions under which the seat asked for an idle
slot, which did not exist. With 26 independent runs, `wall ≈ Σ run wall / slots`, so on a host with
free capacity the same doubling should approach 2×; the shortfall here is the host, not the counter.

Note the plateau: `--jobs 6` alone in R2 (461.3 s, load 75→64) and `--jobs 8` paired with
`--jobs 4` in R5 (465.5 s) land on the same wall, i.e. past ~6 slots the counter is bounded by
something other than its own slot count on this host.

Counter output bytes were identical in every comparison:
`diff -q c1-j3.txt c1-j6.txt` → identical; `diff -q c1-pair-j3.txt c1-pair-j6.txt` → identical;
`diff -q c1-p48-j4.txt c1-p48-j8.txt` → identical, and both equal to the earlier `--jobs 3` output;
`diff -q c1-j6.txt c1-j6par.txt` → identical (R3 vs the patched-tool run of §4).

### Slowest variant

By wall clock in R1: `N5` 441.8 s (rc 0), then `J6` 441.3 s (rc 1) and the unedited run
(`real`, skill=None) 440.9 s. In R2 the order is entirely different: `N4` 107.4 s, `J8` 105.6 s,
`J3` 105 s. **The wall ranking is scheduler noise, not variant cost.** Decisive evidence inside a
single counter invocation: `real` (skill=None) took 440.9 s and `real-opaque` (the *same SKILL.md
text*, 063be309e5d1, handed over as an opaque `--skill` copy) took 125.5 s — 3.5× apart for identical
work, inside one run. The load-independent measure (child CPU per run) is flat across all 26
variants: **24.2 s – 28.8 s**, nominal maximum `J4` 28.8 s (`MORI_SOURCES_APPENDONLY_SELFTEST`
against the archived `gate-v2-bb1f2457.py`, i.e. one extra bound command), then `real` 28.5 s,
`N6` 28.5 s, `N9` 28.4 s, `J1` 28.3 s. The two fixture-built variants (`N10`, `H5`) are 0.1 s each:
their repository is a two-commit probe fixture with one pin, so they barely contribute to the
counter's wall. Answer: **slowest variant by wall = N5 (R1 window); no variant is materially slower
by its own cost.**

## 2. Where one tool run's time goes

One run = `git archive` the revision → extract it → parse SKILL.md → run every bound `--selftest`
command → compare. Measured three ways.

**cProfile** (`python3 -I -B -m cProfile -o prof-real.out`, load 15, run wall 81.5 s):

| cumulative | share | frame |
|---|---|---|
| 77.14 s | 94.7 % | `check()` — of which 76.88 s is `run_cmd()` (27 calls) |
| 77.15 s | 94.7 % | `select.poll` — i.e. *waiting* on the 27 child processes |
| 3.86 s | 4.7 % | `export_rev()` (0.02 s own; `tarfile.extractall` 3.26 s) |
| 0.002 s | 0.0 % | `check()` own time; `split_cells` tottime 0.13 s (7,050 calls) |

Non-subprocess Python work is small: `posix.lstat` 0.59 s (12,237 files), `_io.open` 0.57 s,
`posix.unlink` 0.35 s (export teardown), `realpath` 0.33 s. **Imports** (`-X importtime`): total
≈ 10–15 ms — `site` 4.0 ms, `_colorize` 4.2 ms, `shutil` 0.8 ms, `subprocess` 0.7 ms. The parse
stage is not a cost centre.

**Export** (`export_rev()`, control lines 609–627; measured serially in a fresh tree): `git archive`
0.43–0.70 s, tar write 0.02–1.89 s, `tarfile.extractall` 1.14–3.26 s, deletes ≈ 0.35 s →
**4.08 s total** for 324,700,160 bytes / 12,237 files (4.6 % of an 89 s run). Concurrency does not
punish it: three simultaneous exports took 5.04 s aggregate on the lane filesystem and 2.16 s on
tmpfs, against 3 × 4.08 s serial. Export is *not* the bottleneck; it is the one cost repeated 26×
(≈17 GB of archive+extract churn per counter run) and it peaks at 641 MB RSS per run (the 325 MB
archive is buffered in memory at line 614–621), i.e. ≈3.9 GB transient at `--jobs 6`.

**The pins** — one tree, the 27 distinct bound argv, measured serially at load 27–36
(`prof2.py`, child CPU from `RUSAGE_CHILDREN`):

| command | wall | CPU | idle |
|---|---|---|---|
| `python3 .ufo/waves/round-40/conform.py b3e3453d… --selftest` | **58.69 s** | 3.62 s | 93.8 % |
| `python3 tools/mori-pin-check.py --selftest` | 5.87 s | 0.78 s | 86.7 % |
| `python3 tools/mori-source-drift.py --selftest` | 4.10 s | 0.09 s | 97.8 % |
| `python3 .ufo/waves/round-44/count-c2.py --selftest` | 3.03 s | 2.45 s | 19 % |
| `python3 tools/mori-sources-appendonly.py b3e3453d… --selftest` | 2.71 s | 2.24 s | 17 % |
| `python3 .ufo/waves/round-45/count-c2.py --selftest` | 2.31 s | 1.88 s | 19 % |
| the remaining 21 commands (all < 2 s) | 8.55 s | 6.83 s | — |
| **27 commands** | **85.3 s** | **17.9 s** | **67.4 s** |

31 tally pins bind 27 distinct argv (four commands are pinned twice and hit the run-local cache at
control line 565). The profile is therefore not CPU-bound (21 % busy) and not parse-bound and not
export-bound: **it is a wait profile concentrated in one pin.** `conform.py --selftest` is 68.8 % of
all pin wall and 72 % of the whole run. Its own docstring (round-40 `conform.py` lines 39–40 and
728–729) says the `timeout_state` mutation runs `fixtures/hang-after-flush.py` under
`--tool-timeout 3`, and the selftest is eleven mutations: [INFERENCE] the 55 s of idle inside that
pin is those timeout arms waiting, not work.

One property of that pin matters for isolation, not for wall time: `conform.py` carries an
**absolute** lane path (`conform.py:70`, `LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"`,
`SCRATCH_ROOT = <LANE>/.ufo/waves/round-40/scratch`) and its selftest does
`tempfile.mkdtemp(prefix="mori-conform-selftest-", dir=SCRATCH_ROOT)` (`conform.py:743`), removed
with `shutil.rmtree(work, ignore_errors=True)` (`conform.py:765`). So when the reconciler runs this
pin from an export tree, the pin writes into the **lane** repository, once per tool run (26 times per
counter invocation, 6 invocations in flight at `--jobs 6`), against the counter's own claim that "the
lane repo is only read" (`count-c1.py` docstring, usage paragraph). Verified: one pin call from the
export tree created and removed its directory (`residue_dirs_before=6 after=6`,
`CONFORM_SELFTEST pass=11 fail=0`, exit 0, 58.42 s); six orphaned
`.ufo/waves/round-40/scratch/mori-conform-selftest-*` directories (816 KB, timestamps 21:48–21:50,
i.e. before this seat's first counter run at 22:02) show what an interrupted run leaves behind,
because `ignore_errors=True` hides the cleanup failure.

## 3. Is the 900 s TOOL_TIMEOUT ever close?

`TOOL_TIMEOUT = 900` (`.ufo/waves/round-48/count-c1.py:42`, imported by the round-49 counter).
Across seven counter invocations (189 tool runs: R1–R3, both sides of R4 and both of R5) there were
**no `errors`, no timeouts** (`errors=0` in every `C1=` line).

- Uncontended run: 81.5 s (load 15) / 88.7 s paired (load 62–66) → **9–11 %** of the budget.
- Heaviest window: **441.8 s** (R1, load 110) → **49 %** of the budget. That is the closest any run
  came.
  `--jobs 6` windows: max 107.4 s and 97.0 s → 11–12 %.
- Inner bound per pinned command: `TIMEOUT_S = 600` (control line 100) against a slowest pin of
  **58.69 s** (10.2× margin) and a second of 5.87 s. The slowest pin command is
  `python3 .ufo/waves/round-40/conform.py <rev> --selftest`.

The margin is real but not structural: per-run wall scales with host load, and raising the in-flight
count raises per-run wall (441.8 s at `--jobs 3` under load 110), so more jobs trades the counter's
wall against this margin on a loaded host.

## 4. Cheapest change that halves the wall, every output byte kept

**The answer up front.** The cheapest change that halves the wall *without editing the tool* is to
raise the counter's in-flight count (`--jobs`, proposal 1 below): it needs no byte of the tool or the counter's
logic, the counter output is identical, and on an idle host it halves by construction because a slot
carries 85.3 s of wall for 17.9 s of CPU — slots, not cores, are the constraint. Measured on this
contended host it delivered 1.73× and 1.53×. **No change to the reconciler can halve a single run**:
the run must measure every bound command and one of them is 58.69 s of mostly idle wait, so 66 s
(measured with the scratch-copy patch) is the floor.

**The measured floor.** Paired A/B in identical windows (both tools started together, each timing
itself; `ab3.sh`):

| pair | load | unpatched | concurrent-pin patch | ratio | stdout |
|---|---|---|---|---|---|
| pair1 | 62.4 | 88.76 s | 66.93 s | 1.33× | identical |
| pair2 | 66.0 | 88.63 s | 66.28 s | 1.34× | identical |

66 s ≈ 58.7 s (the dominant pin) + 4.1 s (export) + tail — exactly the predicted floor. A micro-test
isolates the mechanism: the four slowest pins take **72.5 s serial vs 59.2 s in a 4-way pool** (the
three short ones hide entirely behind `conform.py`).

**Proposal, ranked by cost.**

1. **Cheapest, no code, no output change: raise the in-flight count.** `--jobs 6` or 8 instead of
   the default 4 (`.ufo/waves/round-49/count-c1.py:314`). Controlled simultaneous pairs: 3→6 =
   **1.73×** (812.2 s → 470.5 s), 4→8 = **1.53×** (713.2 s → 465.5 s); across windows 3→6 was 4.4×
   (2025.2 s → 461.3 s). Counter bytes identical in all of them, and identical to the `--jobs 3`
   output. On an idle host this doubling halves by construction: a run costs 85.3 s of wall but only
   17.9 s of CPU, so **slots, not cores, are the constraint** and 26 runs at 2× slots is 2× the
   throughput; on this host the extra slots were partly absorbed by sibling load, which is why the
   measured factors are 1.5–1.7×. It is the only change with zero risk to the predicate bytes; its
   cost is timeout exposure (§3).
2. **Cheapest code change, proven on a scratch copy: measure the bound commands concurrently.**
   Copy the entering tool to scratch, add `import concurrent.futures`, a `WORKERS` constant
   (`MORI_PIN_WORKERS`, default 4), and one prefetch block before the row loop that measures every
   distinct bound argv in a `ThreadPoolExecutor` and fills the existing `cache` — 10 added lines,
   the row loop and every output line untouched. Scratch copy:
   `.scratch/r49-Mo49ExecCounterTiming/tool-par-pins.py`, sha256 `bb982819b5caf3cef61add016944f1069d6c185abdd36671ac0eb4a11eecc1ec`.
   Effect: per-run **1.34×** (paired, above); the counter at `--jobs 6` went **461.3 s → 369.4 s**
   (adjacent windows, load 75→64 vs 61→38, so treat as corroboration, not proof); achieved
   concurrency 5.17 → 5.46. It lowers the per-run floor from 89 s to 66 s and so halves the
   *timeout exposure*, but it does not halve the counter on its own.
3. **What would actually halve a run (routed, not proposed as cheap):** stop re-paying the dominant
   pin's wait. `--jobs 6` pays `58.69 s × 26 ≈ 1526 s` of identical idle in one counter invocation.
   (a) Memoize pin results per `(commit sha, argv)` across runs — a tool change, outside this seat's
   "without editing the tool" bound; estimate from R2's Σ run wall: 2385.8 s − 25 × 58.69 s ≈ 918 s,
   i.e. ≈160–200 s at `--jobs 6`. **UNVERIFIED — not implemented, not measured.** (b) Shorten
   `conform.py`'s own 55 s of timeout-arm waits by running its eleven mutations concurrently — an
   instrument change; the r40 row (`SKILL.md:911`) pins no 64-hex digest, but whoever lands it must
   re-audit the row's tally/digest pins. **UNVERIFIED.**

**Equality proof for proposal 2, as demanded ("prove the output equality on a scratch copy").**

- Tool stdout byte-identical to the entering bytes in **five** comparisons — one solo
  (`single-run.txt` vs `par-run.txt`), two pairs from `ab.sh` (`ab-orig-*`/`ab-par-*`, whose wall
  timing was void from a `wait`-ordering bug but whose stdout files are valid) and the two clean
  pairs `ab3-A/B-pair1.txt`, `ab3-A/B-pair2.txt`: `diff -q` exit 0 each time; `PIN_CHECK=met
  tally_pins=31 digest_pins=8 mismatches=0 … rev=b3e3453d… baseline=yes` in both.
- Counter output byte-identical across the whole variant set: `count-c1.py --jobs 6` with the shim
  pointed at the patched copy (`SHIM_TOOL=tool-par-pins.py`) produced the same 27 variant lines and
  the same `C1=unmet junk_met=9 honest_unmet=0 real=met errors=0 variants=26` as the unpatched run
  (`diff -q c1-j6.txt c1-j6par.txt` → identical). That covers all 26 variants including the two
  fixture-built ones.
- The patch keeps the tool's own pinned selftest intact: `python3 -I -B tool-par-pins.py --selftest`
  → `PIN_CHECK_SELFTEST pass=60 fail=0`, exit 0 — the same text `SKILL.md:938` pins.

## Reproduction

```bash
S=$PWD/.scratch/r49-Mo49ExecCounterTiming; LANE=/home/vgpnk/Projects/shokunin/mori-shokunin; cd $LANE
# counter at 3 and 6 (shim for per-run wall/CPU/RSS)
SHIM_LOG=$S/shim-j3.log TMPDIR=$S python3 -B .ufo/waves/round-49/count-c1.py --tool $S/shim.py \
  --rev b3e3453d --repo $LANE --jobs 3 --scratch $S/c1-j3 > $S/c1-j3.txt 2>&1
# controlled pairs (both sides started together, each timed in its own subshell)
bash $S/jobs_pair.sh          # jobs 3 vs 6 simultaneously   (R4)
bash $S/jobs_pair2.sh         # jobs 4 vs 8 simultaneously   (R5)
# per-run profile: export steps, per-pin wall and CPU
python3 $S/prof2.py                        # writes $S/prof2.json
# paired A/B unpatched vs concurrent-pin scratch copy
bash $S/ab3.sh .ufo/waves/round-49/controls/tool-v3-entering.py $S/tool-par-pins.py pair3
diff -q $S/ab3-A-pair3.txt $S/ab3-B-pair3.txt     # recorded pairs: pair1 (88.76/66.93), pair2 (88.63/66.28)
```

Note for reading line numbers: the live `tools/mori-pin-check.py` was rewritten by sibling w1 seats
during this wave (now sha256 `697ab2cc…`, 1,425 lines, `check()` cache at line 662). Every line
number in this report is the **entering** control copy (917 lines), which is the byte set the frozen
counter scores as `--tool` and the bytes the profile was taken on. The proposal is expressed
structurally (prefetch the bound argv before the row loop, measure them in a pool, keep the cache
keyed by `tuple(argv)`) so it maps onto whatever bytes land.

Artifacts kept in the seat scratch (1.7 GB total; the two export trees are disposable):
`shim.py`, `tool-par-pins.py`, `prof.py`, `prof2.py`, `varmap.py`, `ab.sh`, `ab3.sh`,
`jobs_pair.sh`, `jobs_pair2.sh`, the `c1-*.txt` counter outputs, `shim-j*.log`, `prof-real.out`
(cProfile), `prof2.json`.

## Findings

- **MED — one pinned command is 69 % of every reconciler run, and it is idle.** `conform.py <rev>
  --selftest` = 58.69 s wall / 3.62 s CPU of an 85.3 s pin phase (68.8 %) and ≈72 % of a whole run;
  the pin phase is 21 % CPU-busy (17.9 s of 85.3 s). The reconciler measures pins strictly serially
  (`tools/mori-pin-check.py:565` at b3e3453d — `cache[key] = run_cmd(...)` inside the row loop), so
  that wait is paid once per run and 26× per counter invocation. Concerns
  `.ufo/waves/round-40/conform.py` as pinned by `SKILL.md:911` and
  `tools/mori-pin-check.py:492–510` (the prefetch site).
- **MED — the counter's isolation claim does not hold for the dominant pin: it writes inside the lane
  repository, 26× per counter invocation.** `conform.py:70` hardcodes the lane as an absolute path and
  `conform.py:743` mkdtemps `.ufo/waves/round-40/scratch/mori-conform-selftest-*` there, so every tool
  run — including runs pointed at an export tree and at the fixture repositories — writes into the lane
  repo, while `count-c1.py`'s usage paragraph states "the lane repo is only read". Cleanup
  (`conform.py:765`) uses `ignore_errors=True`, so an interrupted run leaves residue: six such
  directories (816 KB, 21:48–21:50) are present now. Neither verdicts nor this seat's measurements were
  affected (`residue_dirs_before=6 after=6`; every `C1=` line matched the freeze receipt), but the
  isolation sentence and the residue accounting should be corrected by whoever owns that row.
  Concerns `.ufo/waves/round-40/conform.py:70,743,765` and `.ufo/waves/round-49/count-c1.py`
  (docstring).
- **MED — per-variant wall is scheduler noise on this host, so a wall-based "slowest variant" is not
  a variant property.** Identical SKILL.md text scored 440.9 s (`real`) and 125.5 s (`real-opaque`)
  in one counter run; rankings invert between windows (`N5` 441.8 s at `--jobs 3`, `N4` 107.4 s at
  `--jobs 6`). Child CPU is flat: 24.2–28.8 s over all 26 variants; nominal max `J4` 28.8 s.
  Concerns `.ufo/waves/round-49/count-c1.py:measure()` (no per-run timing is recorded, so any cost
  claim built on counter wall alone inherits the noise).
- **LOW — the 900 s `TOOL_TIMEOUT` is not close today but is load-coupled.** Worst observed run
  441.8 s (49 % of budget) at load 110; 81–107 s (9–12 %) otherwise; inner `TIMEOUT_S = 600` is 10.2×
  the slowest pin (58.69 s). Raising `--jobs` raises per-run wall. Concerns
  `.ufo/waves/round-48/count-c1.py:42` and `tools/mori-pin-check.py:100`.
- **LOW — every run re-exports the same 324.7 MB / 12,237-file tree.** 4.08 s (4.6 %) per run,
  ≈17 GB of churn per counter run, peak RSS 641 MB per run (≈3.9 GB transient at `--jobs 6`).
  Concurrency does not punish the export (3 simultaneous: 5.04 s disk vs 2.24 s/run tmpfs), so it is
  a waste, not the bottleneck. Concerns `tools/mori-pin-check.py:609–627`.
- **LOW — the cheapest lever is a flag, not code, and its measured return is 1.5–1.7×, not 2× on this
  host.** Simultaneous controlled pairs: `--jobs 3` 812.2 s vs `--jobs 6` 470.5 s (1.73×),
  `--jobs 4` 713.2 s vs `--jobs 8` 465.5 s (1.53×), counter output byte-identical in both and equal
  to the `--jobs 3` output; past ~6 slots the wall plateaus (461–466 s) under sibling load. The
  counter's default is 4 (`.ufo/waves/round-49/count-c1.py:314`). The reason it is not 2× here is
  host contention, not the counter; the reason it is bounded at all is that a slot carries 85.3 s of
  wall for 17.9 s of CPU.
