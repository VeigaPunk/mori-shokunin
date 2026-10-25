# ExecPinTiming — w1 seat report (round 47)

Seat: ExecPinTiming (executor, leaf). Assignment: time the frozen C1 pin-check
command, time each selftest command it binds, judge `TIMEOUT_S=600` and the
per-command cache, and report any command whose output differs between two runs.

Measured instrument: `tools/mori-pin-check.py` at freeze `63eecf27` (sha256
`e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1`).
Measured revision: entering tip `2d85e33d14198d388fd3cda9cc15ec07e57e7a53`.
Host: linux `7.2.11-arch1-1`, `python3` 3.14.8, 2026-10-25 -03. No tools
installed or updated (nothing was needed; no pacman, no uv, no binary installs).

## Method

- Full pinned runs (two): `python3 tools/mori-pin-check.py --rev
  2d85e33d14198d388fd3cda9cc15ec07e57e7a53 --min-tally-pins 26 --baseline-rev
  2d85e33d14198d388fd3cda9cc15ec07e57e7a53`, cwd = lane root,
  `TMPDIR=<lane>/.scratch/r47-ExecPinTiming`. Timing via bash `time`
  (`TIMEFORMAT`), output tee'd to `.scratch/r47-ExecPinTiming/run1.out` /
  `run2.out`.
- Per-command timed runs (two rounds): for each of the 22 unique `cmd=` argv
  sets bound by the tool's output (26 tally pins → 22 unique commands; 4 pins
  reuse a cached argv), ran once per round from a `git archive` export of rev
  `2d85e33` (fresh export for round 2), `TMPDIR` placed inside the exported
  tree under `.scratch/pin-tmp-*` exactly as `run_cmd` does, with
  `PYTHONDONTWRITEBYTECODE=1`. Logs: `.scratch/r47-ExecPinTiming/out/round1/*.txt`
  and `out/round2/*.txt`.

Note on instrument bytes: the working-tree copy of `tools/mori-pin-check.py`
was modified by another in-flight seat while this seat ran (mtime 2026-10-25
16:43:57, sha256 now `104cf3dd8174933799de97ec0b11e6cdb1923bb2bda1130f0bb3afeff1e4f56d`;
diff removes `bound = []` from `pin_commands`, which makes that function raise
`NameError` on any run — see Hazards below). Full run #1 completed before that
modification and only the intact code can produce its fully bound output; full
run #2 executed the frozen bytes via `git show 63eecf27:tools/mori-pin-check.py`
(copy in scratch; sha256 verified = `e3ef425a…`). Both runs print identical
results, so the measurements are on the frozen behavior.

## 1. Full pinned command wall time

| run | wall (real) | user | sys | exit | verdict line |
|---|---|---|---|---|---|
| 1 | 69.99 s | 74.01 s | 39.32 s | 1 | `PIN_CHECK=unmet tally_pins=26 digest_pins=5 mismatches=1 unparsed=0 no_command=0 dropped=0 min_tally_pins=26 rev=2d85e33… baseline=yes` |
| 2 | 70.45 s | 86.67 s | 35.21 s | 1 | identical |

~70 s, stable across runs. Verdict matches the contract's "Before" state
exactly (mismatches=1 = `SKILL.md:912` MORI_SOURCES_APPENDONLY_SELFTEST pinned
`pass=15 fail=0`, observed `pass=22 fail=0` rc=0).

## 2. Per-command timings (22 unique commands)

| # | command | round1 wall | round2 wall | rc (both) | pin prefix (line) |
|---|---|---|---|---|---|
| 1 | `bash tools/mori-silence-cases.sh --selftest` | 0.414 s | 0.473 s | 0 | MORI_SILENCE_CASES (166) |
| 2 | `python3 tools/mori-round19-regressions.py --selftest` | 0.067 s | 0.076 s | 0 | R19 (182) |
| 3 | `python3 .ufo/waves/round-44/count-c1.py --selftest` | 0.112 s | 0.130 s | 0 | C1 (183,193) |
| 4 | `python3 tools/mori-gate-registry.py --selftest` | 0.185 s | 0.232 s | 0 | GATE_REGISTRY (184,194) |
| 5 | `python3 .ufo/waves/round-44/count-c2.py --selftest` | 1.246 s | 1.456 s | 0 | C2 (185,195) |
| 6 | `python3 .ufo/waves/round-44/count-c3.py --selftest` | 0.084 s | 0.107 s | 0 | C3 (186,196) |
| 7 | `python3 tools/mori-disk-rate.py --selftest` | 0.128 s | 0.153 s | 0 | MORI_DISK_RATE (187) |
| 8 | `python3 tools/mori-wave-settlement.py --selftest` | 0.028 s | 0.039 s | 0 | MORI_WAVE_SETTLEMENT (188) |
| 9 | `python3 tools/mori-round41-calibration.py --selftest` | 0.147 s | 0.165 s | 0 | MORI_R41_CALIBRATION (189) |
| 10 | `python3 .ufo/waves/round-45/count-c1.py --selftest` | 0.730 s | 0.748 s | 0 | C1 (190) |
| 11 | `python3 .ufo/waves/round-45/fixtures/mutants/count-c1.py --selftest` | 0.778 s | 0.837 s | 1 | C1 mutant (190) |
| 12 | `python3 .ufo/waves/round-45/count-c2.py --selftest` | 1.018 s | 1.213 s | 0 | C2 (191) |
| 13 | `python3 .ufo/waves/round-45/count-c3.py --selftest` | 0.349 s | 0.387 s | 0 | C3 (192) |
| 14 | `python3 .ufo/waves/round-45/fixtures/mutants/count-c3.py --selftest` | 0.348 s | 0.348 s | 1 | C3 mutant (192) |
| 15 | `python3 tools/mori-pressure.py --selftest` | 0.033 s | 0.038 s | 0 | MORI_PRESSURE (664) |
| 16 | `python3 -I tools/mori-routed-check.py --selftest` | 0.186 s | 0.225 s | 0 | ROUTED_CHECK (665) |
| 17 | `python3 -I -B tools/mori-oom-killers.py --selftest` | 0.029 s | 0.035 s | 0 | MORI_OOM_KILLERS (739) |
| 18 | `python3 -I -B tools/mori-routed-r24.py --selftest` | 0.078 s | 0.089 s | 0 | ROUTED_R24 (740) |
| 19 | `python3 -I -B tools/mori-job-runway.py --selftest` | 0.030 s | 0.036 s | 0 | MORI_JOB_RUNWAY (741) |
| 20 | `python3 tools/mori-source-drift.py --selftest` | 4.544 s | 4.550 s | 0 | MORI_SOURCE_DRIFT (905) |
| 21 | `python3 .ufo/waves/round-40/conform.py 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 --selftest` | 57.189 s | 57.166 s | 0 | CONFORM (911) |
| 22 | `python3 tools/mori-sources-appendonly.py 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 --selftest` | 1.406 s | 1.215 s | 0 | MORI_SOURCES_APPENDONLY (912) |

Slowest selftest command: **#21 `conform.py --selftest` ≈ 57.2 s (82% of the
total)** in both rounds; second slowest #20 source-drift ≈ 4.5 s; everything
else ≤ 1.5 s.

Sum of per-command walls: 69.13 s (round1), 69.72 s (round2) → framework
overhead (git archive export + extract, baseline `git show`, registry parse, tmp
dir setup) ≈ 0.7–0.9 s of the ~70 s full runs.

## 3. Determinism (output differs between two runs?)

- Full-run pin lines: `diff` of run1.out vs run2.out (sans time lines) is
  **identical** (`PINS_IDENTICAL`) — all 26 tally pins and 5 digest pins report
  the same observed values, rc, and verdict.
- Per-command full outputs: 21 of 22 commands byte-identical across rounds
  (ignoring the `WALL` timing line). **One command differs: #14** (mutant
  `count-c3.py --selftest`). Difference is confined to the two `FAIL` arm
  detail lines: `entering_absent` prints `not in <40-hex>` where the hex is a
  freshly created throwaway fixture git repo's entering-commit hash —
  `7a3d0cc33fd4f61d62d7f6f0cd8470ad8a1550bd` / `df73cc01fcc29d458d01849682a1ed51b93b2c7a` in
  round1 vs `054ac3c3532a845b8e2cf1b2408b6249e040db8a` twice in round2
  (`count-c3.py` `_fixture` commits "entering" then `rev-parse main` per run).
  The verdict line `C3_SELFTEST pass=17 fail=2`, both FAIL arm names, and rc=1
  are identical across rounds. Classification: expected cosmetic variance in
  debug detail (throwaway repo ids); not a flaky verdict and not observable by
  the pin-check (it matches only the `C3_SELFTEST pass=17 fail=2` line).

## 4. Judge TIMEOUT_S=600 and the per-command cache

- `TIMEOUT_S=600`: **adequate.** Slowest observed command is 57.2 s, i.e. ~9.5%
  of the budget per command. Margin ≈ 10x even if the host is 2–3x slower under
  load; no command came close to the cap in any run. If `conform.py`'s self-test
  ever regresses, it is the first command to pressure the cap, but 600 s is not
  the binding constraint today.
- Per-command cache: **adequate.** Key = full argv tuple; within one measurement
  it correctly dedupes the 4 pins that reuse an earlier argv (lines 193/194/195/196
  → cmds #3/#4/#5/#6), avoiding 4 re-executions, while every distinct command
  runs. The cache is per-invocation (fresh scratch per run), so it cannot mask
  cross-run drift; cross-run stability was verified separately above (21/22
  byte-identical, #14 stable on its verdict line). No cache staleness risk:
  commands run against the exported tree of the measured rev, so argv+tree are
  consistent within a run.

## Hazards / observations for the L1 (report only)

1. **Working-tree `tools/mori-pin-check.py` is currently broken** and differs
   from the freeze: the `bound = []` line was removed from `pin_commands`
   (mtime 2026-10-25 16:43:57; sha256 `104cf3dd…` vs frozen `e3ef425a…`). Any
   run of the working-tree tool now raises `NameError: name 'bound' is not
   defined` on its first tally pin. Per contract, measurements must use the
   freeze bytes (`git show 63eecf27:tools/mori-pin-check.py`); the seat used
   exactly that for run #2. Whoever owns that edit should restore the frozen
   bytes before integration.
2. `git status` at measurement time also shows in-flight edits by other seats
   (SKILL.md, corpus/QUALITY.md, corpus/README.md, corpus/SOURCES.md) — none
   made or touched by this seat.
3. No tools installed/updated (none required); no pacman usage.

## Evidence

- `.scratch/r47-ExecPinTiming/run1.out`, `run2.out` (full runs; 5324/5325 bytes).
- `.scratch/r47-ExecPinTiming/out/round1/{1..22}.txt`, `out/round2/{1..22}.txt`
  (per-command stdout+stderr+WALL+RC).
- `.scratch/r47-ExecPinTiming/tree-rev/` and `tree-rev2/` (`git archive` exports
  of `2d85e33`).
- `.scratch/r47-ExecPinTiming/mori-pin-check-frozen.py` (sha256
  `e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1`).
- `git diff -- tools/mori-pin-check.py` delta shown in §Hazards.
