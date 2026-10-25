# ExecSkillRowsRun — w1 before-state: every SKILL.md registry self-test pin, plain re-measurement

Seat: ExecSkillRowsRun (mori round 48, wave w1). Measured revision: `e5dbac05459887d9597ea5d1da0d8e3d024e0d17` (entering lane tip). Tool: `tools/mori-pin-check.py` at that revision (v2, sha256 `9832e38c…`).

## 1. Tool run (TMPDIR set per lane rule)

```
TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecSkillRowsRun \
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-pin-check.py \
  --rev e5dbac05459887d9597ea5d1da0d8e3d024e0d17 \
  --repo /home/vgpnk/Projects/shokunin/mori-shokunin \
  --min-tally-pins 26 \
  --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53
```

Exit code: **0**.

Full output (per-pin lines, then final line):

```
pin line=166 kind=tally prefix=MORI_SILENCE_CASES_SELFTEST state=match pinned='pass=24 fail=0' observed='pass=24 fail=0' rc=0 cmd='bash tools/mori-silence-cases.sh --selftest'
pin line=182 kind=tally prefix=R19_SELFTEST state=match pinned='pass=26 fail=0' observed='pass=26 fail=0' rc=0 cmd='python3 tools/mori-round19-regressions.py --selftest'
pin line=183 kind=tally prefix=C1_SELFTEST state=match pinned='pass=6 fail=0' observed='pass=6 fail=0' rc=0 cmd='python3 .ufo/waves/round-44/count-c1.py --selftest'
pin line=184 kind=tally prefix=GATE_REGISTRY_SELFTEST state=match pinned='pass=15 fail=0' observed='pass=15 fail=0' rc=0 cmd='python3 tools/mori-gate-registry.py --selftest'
pin line=184 kind=digest state=match digest=8b82ac999091 file=tools/mori-gate-registry.py
pin line=185 kind=tally prefix=C2_SELFTEST state=match pinned='pass=5 fail=0' observed='pass=5 fail=0' rc=0 cmd='python3 .ufo/waves/round-44/count-c2.py --selftest'
pin line=186 kind=tally prefix=C3_SELFTEST state=match pinned='pass=6 fail=0' observed='pass=6 fail=0' rc=0 cmd='python3 .ufo/waves/round-44/count-c3.py --selftest'
pin line=187 kind=tally prefix=MORI_DISK_RATE_SELFTEST state=match pinned='pass=14 fail=0' observed='pass=14 fail=0' rc=0 cmd='python3 tools/mori-disk-rate.py --selftest'
pin line=188 kind=tally prefix=MORI_WAVE_SETTLEMENT_SELFTEST state=match pinned=': PASS (23 cases, 23 passed, 0 failed)' observed=': PASS (23 cases, 23 passed, 0 failed)' rc=0 cmd='python3 tools/mori-wave-settlement.py --selftest'
pin line=189 kind=tally prefix=MORI_R41_CALIBRATION_SELFTEST state=match pinned='pass=10 fail=0' observed='pass=10 fail=0' rc=0 cmd='python3 tools/mori-round41-calibration.py --selftest'
pin line=190 kind=tally prefix=C1_SELFTEST state=match pinned='pass=16 fail=0' observed='pass=16 fail=0' rc=0 cmd='python3 .ufo/waves/round-45/count-c1.py --selftest'
pin line=190 kind=tally prefix=C1_SELFTEST state=match pinned='pass=15 fail=1' observed='pass=15 fail=1' rc=1 cmd='python3 .ufo/waves/round-45/fixtures/mutants/count-c1.py --selftest'
pin line=190 kind=digest state=match digest=5f2deea0b35c file=.ufo/waves/round-45/count-c1.py
pin line=191 kind=tally prefix=C2_SELFTEST state=match pinned='pass=14 fail=0' observed='pass=14 fail=0' rc=0 cmd='python3 .ufo/waves/round-45/count-c2.py --selftest'
pin line=191 kind=digest state=match digest=153423c48ca9 file=.ufo/waves/round-45/count-c2.py
pin line=191 kind=digest state=match digest=9850b3fcc888 file=.ufo/waves/round-45/fixtures/mutants/count-c2.py
pin line=192 kind=tally prefix=C3_SELFTEST state=match pinned='pass=19 fail=0' observed='pass=19 fail=0' rc=0 cmd='python3 .ufo/waves/round-45/count-c3.py --selftest'
pin line=192 kind=tally prefix=C3_SELFTEST state=match pinned='pass=17 fail=2' observed='pass=17 fail=2' rc=1 cmd='python3 .ufo/waves/round-45/fixtures/mutants/count-c3.py --selftest'
pin line=193 kind=tally prefix=C1_SELFTEST state=match pinned='pass=6 fail=0' observed='pass=6 fail=0' rc=0 cmd='python3 .ufo/waves/round-44/count-c1.py --selftest'
pin line=194 kind=tally prefix=GATE_REGISTRY_SELFTEST state=match pinned='pass=15 fail=0' observed='pass=15 fail=0' rc=0 cmd='python3 tools/mori-gate-registry.py --selftest'
pin line=194 kind=digest state=match digest=8b82ac999091 file=tools/mori-gate-registry.py
pin line=195 kind=tally prefix=C2_SELFTEST state=match pinned='pass=5 fail=0' observed='pass=5 fail=0' rc=0 cmd='python3 .ufo/waves/round-44/count-c2.py --selftest'
pin line=196 kind=tally prefix=C3_SELFTEST state=match pinned='pass=6 fail=0' observed='pass=6 fail=0' rc=0 cmd='python3 .ufo/waves/round-44/count-c3.py --selftest'
pin line=664 kind=tally prefix=MORI_PRESSURE_SELFTEST state=match pinned=': PASS 12/12' observed=': PASS 12/12' rc=0 cmd='python3 tools/mori-pressure.py --selftest'
pin line=665 kind=tally prefix=ROUTED_CHECK_SELFTEST state=match pinned='pass=20 fail=0' observed='pass=20 fail=0' rc=0 cmd='python3 -I tools/mori-routed-check.py --selftest'
pin line=739 kind=tally prefix=MORI_OOM_KILLERS_SELFTEST state=match pinned=': PASS 32/32' observed=': PASS 32/32' rc=0 cmd='python3 -I -B tools/mori-oom-killers.py --selftest'
pin line=740 kind=tally prefix=ROUTED_R24_SELFTEST state=match pinned='pass=26 fail=0' observed='pass=26 fail=0' rc=0 cmd='python3 -I -B tools/mori-routed-r24.py --selftest'
pin line=741 kind=tally prefix=MORI_JOB_RUNWAY_SELFTEST state=match pinned=': PASS 21/21' observed=': PASS 21/21' rc=0 cmd='python3 -I -B tools/mori-job-runway.py --selftest'
pin line=905 kind=tally prefix=MORI_SOURCE_DRIFT_SELFTEST state=match pinned=': PASS (6 cases)' observed=': PASS (6 cases)' rc=0 cmd='python3 tools/mori-source-drift.py --selftest'
pin line=911 kind=tally prefix=CONFORM_SELFTEST state=match pinned='pass=11 fail=0' observed='pass=11 fail=0' rc=0 cmd='python3 .ufo/waves/round-40/conform.py e5dbac05459887d9597ea5d1da0d8e3d024e0d17 --selftest'
pin line=912 kind=tally prefix=MORI_SOURCES_APPENDONLY_SELFTEST state=match pinned='pass=22 fail=0' observed='pass=22 fail=0' rc=0 cmd='python3 tools/mori-sources-appendonly.py e5dbac05459887d9597ea5d1da0d8e3d024e0d17 --selftest'
pin line=938 kind=tally prefix=PIN_CHECK_SELFTEST state=match pinned='pass=34 fail=0' observed='pass=34 fail=0' rc=0 cmd='python3 tools/mori-pin-check.py --selftest'
pin line=939 kind=tally prefix=C2_SELFTEST state=match pinned='pass=13 fail=0' observed='pass=13 fail=0' rc=0 cmd='python3 .ufo/waves/round-47/count-c2.py --selftest'
PIN_CHECK=met tally_pins=28 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 min_tally_pins=26 rev=e5dbac05459887d9597ea5d1da0d8e3d024e0d17 baseline=yes
```

Final line rc: the tool exited **0** (`RC=0`; `PIN_CHECK=met`). 28 tally pins, 5 digest pins (all `sha256` matches: `tools/mori-gate-registry.py` ×2, `.ufo/waves/round-45/count-c1.py`, `count-c2.py`, `fixtures/mutants/count-c2.py`). Zero mismatches/unparsed/no_command/dropped/rebound/duplicate. Total tool wall time: **77.03 s** (shell-measured).

## 2. The 28 tally pins, by SKILL.md line — pinned vs observed vs seconds

Timing method: each **distinct** command was timed once (`date +%s.%N` delta; shell `time` style) in a byte-exact `git archive` export of `e5dbac05`, cwd = export root, env matching the tool's `run_cmd` (`TMPDIR` = fresh dir under `<export>/.scratch`, `PYTHONDONTWRITEBYTECODE=1`). Reused commands (superseded rows) are timed once; the seconds column applies to that command. All 24 distinct commands reproduced the tool's rc (0, or 1 for the two mutant fixtures).

| line | row name | prefix | pinned | observed | seconds |
|---|---|---|---|---|---|
| 166 | silence oracle | MORI_SILENCE_CASES_SELFTEST | pass=24 fail=0 | pass=24 fail=0 | 0.473 |
| 182 | r19 finite regressions | R19_SELFTEST | pass=26 fail=0 | pass=26 fail=0 | 0.081 |
| 183 | r44 figure ledger (C1) | C1_SELFTEST | pass=6 fail=0 | pass=6 fail=0 | 0.129 |
| 184 | r44 gate registry (C2) | GATE_REGISTRY_SELFTEST | pass=15 fail=0 | pass=15 fail=0 | 0.216 |
| 185 | r44 gate conformance (C2) | C2_SELFTEST | pass=5 fail=0 | pass=5 fail=0 | 1.439 |
| 186 | r44 corpus coverage (C3) | C3_SELFTEST | pass=6 fail=0 | pass=6 fail=0 | 0.097 |
| 187 | disk write rate (r34) | MORI_DISK_RATE_SELFTEST | pass=14 fail=0 | pass=14 fail=0 | 0.146 |
| 188 | wave settlement (r20) | MORI_WAVE_SETTLEMENT_SELFTEST | : PASS (23 cases, 23 passed, 0 failed) | : PASS (23 cases, 23 passed, 0 failed) | 0.032 |
| 189 | r41 calibration | MORI_R41_CALIBRATION_SELFTEST | pass=10 fail=0 | pass=10 fail=0 | 0.162 |
| 190 | r45 ledger counter (C1) | C1_SELFTEST | pass=16 fail=0 | pass=16 fail=0 | 0.786 |
| 190 | r45 ledger counter (C1) | C1_SELFTEST | pass=15 fail=1 | pass=15 fail=1 | 0.828 |
| 191 | r45 gate conformance (C2) | C2_SELFTEST | pass=14 fail=0 | pass=14 fail=0 | 1.185 |
| 192 | r45 corpus coverage (C3) | C3_SELFTEST | pass=19 fail=0 | pass=19 fail=0 | 0.392 |
| 192 | r45 corpus coverage (C3) | C3_SELFTEST | pass=17 fail=2 | pass=17 fail=2 | 0.397 |
| 193 | r44 figure ledger (C1) — write scope superseded | C1_SELFTEST | pass=6 fail=0 | pass=6 fail=0 | 0.129 (same cmd as 183) |
| 194 | r44 gate registry (C2) — write scope superseded | GATE_REGISTRY_SELFTEST | pass=15 fail=0 | pass=15 fail=0 | 0.216 (same cmd as 184) |
| 195 | r44 gate conformance (C2) — write scope superseded | C2_SELFTEST | pass=5 fail=0 | pass=5 fail=0 | 1.439 (same cmd as 185) |
| 196 | r44 corpus coverage (C3) — write scope superseded | C3_SELFTEST | pass=6 fail=0 | pass=6 fail=0 | 0.097 (same cmd as 186) |
| 664 | system pressure (r24, C2) | MORI_PRESSURE_SELFTEST | : PASS 12/12 | : PASS 12/12 | 0.036 |
| 665 | routed round-23 items (r24, C1) | ROUTED_CHECK_SELFTEST | pass=20 fail=0 | pass=20 fail=0 | 0.219 |
| 739 | userspace OOM killers (r26, C2) | MORI_OOM_KILLERS_SELFTEST | : PASS 32/32 | : PASS 32/32 | 0.035 |
| 740 | routed round-24 items (r25, C1) | ROUTED_R24_SELFTEST | pass=26 fail=0 | pass=26 fail=0 | 0.088 |
| 741 | harness background-job runway (r25, C2) | MORI_JOB_RUNWAY_SELFTEST | : PASS 21/21 | : PASS 21/21 | 0.037 |
| 905 | source drift (r37) | MORI_SOURCE_DRIFT_SELFTEST | : PASS (6 cases) | : PASS (6 cases) | 4.551 |
| 911 | counter conformance v3 (r40) | CONFORM_SELFTEST | pass=11 fail=0 | pass=11 fail=0 | 57.299 |
| 912 | SOURCES append-only timing (r38) | MORI_SOURCES_APPENDONLY_SELFTEST | pass=22 fail=0 | pass=22 fail=0 | 1.323 |
| 938 | r47 pin reconciler (C1) | PIN_CHECK_SELFTEST | pass=34 fail=0 | pass=34 fail=0 | 5.295 |
| 939 | r47 tracepoint catalogue (C2) | C2_SELFTEST | pass=13 fail=0 | pass=13 fail=0 | 0.040 |

### <5 s vs ≥5 s

- **Under 5 seconds** (26 pins / 22 distinct commands): everything except the two below; fastest 0.032 s (wave settlement), closest to the floor 4.551 s (source drift r37).
- **≥5 seconds** (2 pins / 2 distinct commands):
  - line 911 `python3 .ufo/waves/round-40/conform.py e5dbac05459887d9597ea5d1da0d8e3d024e0d17 --selftest` — **57.299 s**
  - line 938 `python3 tools/mori-pin-check.py --selftest` — **5.295 s**

## 3. Notes

- This is the before-state for v3: `PIN_CHECK=met`, rc 0, at the entering `e5dbac05`, with baseline `2d85e33d…` (round-47 baseline). All 28 tally pins and all 5 digest pins match; no dropped/rebound/duplicate/unparsed/no_command findings. Convert 28 ≥ floor 26.
- Mutant fixture pins (line 190 `pass=15 fail=1`, line 192 `pass=17 fail=2`) exit 1 as pinned — the tool treats them as matches because the observed tail equals the pinned text and the pin records nonzero fail (the tool's `fail=0`-plus-rc0 conjunct does not apply).
- Timing runs were performed on the byte-exact archive export (same bytes the tool measures); rc reproduces the tool's rc on every distinct command.
- Files changed: only this report (wrote scratch helper `…/.scratch/r48-ExecSkillRowsRun/time-pins.sh` and a temp export tree under `…/.scratch/r48-ExecSkillRowsRun/export`; both are scratch, not production). No tools installed (nothing was needed; no pacman/uv/npx/cargo action taken). No production file read-write beyond read-only reads ordered by the assignment.
- Risks/blockers: none observed. The two slow selftests (conform r40 ~57 s, pin-check selftest ~5.3 s) are the only commands that would push a 5 s budget; the parent integration gate should budget ≥60 s per distinct command or rely on the tool's 600 s per-command timeout.
