# ExecC1Controls — C1 controls re-run (round 47, wave w1)

Seat: `ExecC1Controls` (executor, leaf). Lane: `mori-shokunin` at
`/home/vgpnk/Projects/shokunin/mori-shokunin`.

Assignment: re-run the C1 controls with the frozen tool, with and without
`--skill .ufo/waves/round-47/controls/control-c1-{deleted,moved,truncated}.md`;
confirm each is `PIN_CHECK=unmet`; compare line-by-line with the committed
receipts under `.ufo/waves/round-47/evidence/control-c1-*.txt`; also
`sha256sum tools/mori-pin-check.py` vs the contract pin; paste outputs and rc.

Environment: `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47-ExecC1Controls`
(created). No tools installed or updated (operator RULES.md read; nothing
needed). No host writes, no git/jj mutations (only read-only `git show` /
`git rev-parse --verify` / `diff` / `read`).

---

## 1. Instrument pin: `sha256sum` vs contract pin

Contract pin (freeze `63eecf2738db96f46b0bd02b1b2dfd66787493d0`):
`e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1`

| source | sha256 | match |
|---|---|---|
| working tree at session start (16:42) | `e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1` | yes |
| `git show 63eecf2…:tools/mori-pin-check.py` (frozen bytes) | `e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1` | yes |
| working tree after the runs (16:44) | `104cf3dd8174933799de97ec0b11e6cdb1923bb2bda1130f0bb3afeff1e4f56d` | **no — drifted** |

`diff <(git show 63eecf2…:tools/mori-pin-check.py) tools/mori-pin-check.py`:

```
127d126
<     bound = []
```

The current working-tree tool is missing the `bound = []` initialization in
`pin_commands()` and therefore raises `NameError: name 'bound' is not defined`
(line 137 `return bound`) on every run whose registry contains a `SELFTEST`
span — including the do-nothing command (verified by re-run). The frozen bytes
(`git show <freeze>:tools/mori-pin-check.py`) contain `bound = []` and work.

Per the contract ("if the working-tree bytes ever differ, the claim is
measured with `git show <freeze>:<path>`"), all measurements below were taken
with the frozen bytes materialized into my scratch
(`.scratch/r47-ExecC1Controls/frozen-mori-pin-check.py`, hash verified =
pin). I passed `--repo <lane>` explicitly because the materialized copy sits
deeper than `tools/`; the receipts' commands omitted it because the tool lived
at `tools/` then. Observable behavior is identical (verified below).

Timeline note: during my first batch (all four runs in one shell), the
do-nothing run succeeded while the three `--skill` runs crashed with this
same `NameError`; a later re-run of do-nothing on the current tree also
crashes. `stat` on the working-tree tool shows mtime `2026-10-25
16:43:57.523` (i.e. the file changed mid-batch, between my do-nothing run and
my `--skill` runs). Cause: UNVERIFIED — my seat only read `tools/`; this
looks like a concurrent edit to the working tree by another process. The L1
should verify the lane's working state of `tools/mori-pin-check.py` at
integration time.

---

## 2. Runs (frozen bytes) and results

All commands run with `cwd = <lane>`, `TMPDIR = <scratch>`, frozen tool bytes.
Output is captured below; each run's `EXIT=` line is the process exit code.

### 2a. do-nothing (no `--skill`)

Command:
```
python3 .scratch/r47-ExecC1Controls/frozen-mori-pin-check.py --repo <lane> --rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 --min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53
```

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
pin line=911 kind=tally prefix=CONFORM_SELFTEST state=match pinned='pass=11 fail=0' observed='pass=11 fail=0' rc=0 cmd='python3 .ufo/waves/round-40/conform.py 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 --selftest'
pin line=912 kind=tally prefix=MORI_SOURCES_APPENDONLY_SELFTEST state=mismatch pinned='pass=15 fail=0' observed='pass=22 fail=0' rc=0 cmd='python3 tools/mori-sources-appendonly.py 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 --selftest'
PIN_CHECK=unmet tally_pins=26 digest_pins=5 mismatches=1 unparsed=0 no_command=0 dropped=0 min_tally_pins=26 rev=2d85e33d14198d388fd3cda9cc15ec07e57e7a53 baseline=yes
EXIT=1
```

Result: `PIN_CHECK=unmet`, exit **1**. Matches receipt
`evidence/control-c1-donothing.txt` (diff below).

### 2b. deleted (`--skill .ufo/waves/round-47/controls/control-c1-deleted.md`)

Command:
```
python3 .scratch/r47-ExecC1Controls/frozen-mori-pin-check.py --repo <lane> --rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 --min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 --skill .ufo/waves/round-47/controls/control-c1-deleted.md
```

```
pin kind=baseline state=dropped row='SOURCES append-only timing (r38)' pin=MORI_SOURCES_APPENDONLY_SELFTEST count=1
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
pin line=911 kind=tally prefix=CONFORM_SELFTEST state=match pinned='pass=11 fail=0' observed='pass=11 fail=0' rc=0 cmd='python3 .ufo/waves/round-40/conform.py 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 --selftest'
PIN_CHECK=unmet tally_pins=25 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=1 min_tally_pins=26 rev=2d85e33d14198d388fd3cda9cc15ec07e57e7a53 baseline=yes
EXIT=1
```

Result: `PIN_CHECK=unmet`, exit **1** (`tally_pins=25`, `dropped=1`). Matches
receipt `evidence/control-c1-deleted.txt` (diff below).

### 2c. moved (`--skill .ufo/waves/round-47/controls/control-c1-moved.md`)

Command:
```
python3 .scratch/r47-ExecC1Controls/frozen-mori-pin-check.py --repo <lane> --rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 --min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 --skill .ufo/waves/round-47/controls/control-c1-moved.md
```

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
pin line=911 kind=tally prefix=CONFORM_SELFTEST state=match pinned='pass=11 fail=0' observed='pass=11 fail=0' rc=0 cmd='python3 .ufo/waves/round-40/conform.py 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 --selftest'
pin line=912 kind=tally prefix=MORI_SOURCES_APPENDONLY_SELFTEST state=mismatch pinned='pass=15 fail=0' observed='pass=22 fail=0' rc=0 cmd='python3 tools/mori-sources-appendonly.py 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 --selftest'
PIN_CHECK=unmet tally_pins=26 digest_pins=5 mismatches=1 unparsed=0 no_command=0 dropped=0 min_tally_pins=26 rev=2d85e33d14198d388fd3cda9cc15ec07e57e7a53 baseline=yes
EXIT=1
```

Result: `PIN_CHECK=unmet`, exit **1** (`mismatches=1` at line 912). Matches
receipt `evidence/control-c1-moved.txt` (diff below).

### 2d. truncated (`--skill .ufo/waves/round-47/controls/control-c1-truncated.md`)

Command:
```
python3 .scratch/r47-ExecC1Controls/frozen-mori-pin-check.py --repo <lane> --rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 --min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 --skill .ufo/waves/round-47/controls/control-c1-truncated.md
```

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
pin line=911 kind=tally prefix=CONFORM_SELFTEST state=match pinned='pass=11 fail=0' observed='pass=11 fail=0' rc=0 cmd='python3 .ufo/waves/round-40/conform.py 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 --selftest'
pin line=912 kind=tally prefix=MORI_SOURCES_APPENDONLY_SELFTEST state=mismatch pinned='pass=2' observed='pass=22 fail=0' rc=0 cmd='python3 tools/mori-sources-appendonly.py 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 --selftest'
PIN_CHECK=unmet tally_pins=26 digest_pins=5 mismatches=1 unparsed=0 no_command=0 dropped=0 min_tally_pins=26 rev=2d85e33d14198d388fd3cda9cc15ec07e57e7a53 baseline=yes
EXIT=1
```

Result: `PIN_CHECK=unmet`, exit **1** (`mismatches=1`; `pinned='pass=2'` is
the token-boundary mismatch vs observed `pass=22 fail=0`, matching the
contract's "pin weakened to `pass=2`"). Matches receipt
`evidence/control-c1-truncated.txt` (diff below).

---

## 3. Line-by-line comparison vs committed receipts

For each control, `diff <(tail -n +2 <receipt> | head -n -1) <(head -n -1 <run>)`
(removes the receipt's `$ cmd` line and trailing `rc=1`; the run's trailing
`EXIT=` line is the rc record):

| control | receipt | diff vs run | receipt rc | run rc |
|---|---|---|---|---|
| do-nothing | `control-c1-donothing.txt` | 0 (identical, line-for-line) | `rc=1` | `EXIT=1` |
| deleted | `control-c1-deleted.txt` | 0 (identical, line-for-line) | `rc=1` | `EXIT=1` |
| moved | `control-c1-moved.txt` | 0 (identical, line-for-line) | `rc=1` | `EXIT=1` |
| truncated | `control-c1-truncated.txt` | 0 (identical, line-for-line) | `rc=1` | `EXIT=1` |

Verdict lines (identical to receipts):

```
do-nothing: PIN_CHECK=unmet tally_pins=26 digest_pins=5 mismatches=1 unparsed=0 no_command=0 dropped=0 min_tally_pins=26 rev=2d85e33… baseline=yes
deleted:    PIN_CHECK=unmet tally_pins=25 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=1 min_tally_pins=26 rev=2d85e33… baseline=yes
moved:      PIN_CHECK=unmet tally_pins=26 digest_pins=5 mismatches=1 unparsed=0 no_command=0 dropped=0 min_tally_pins=26 rev=2d85e33… baseline=yes
truncated:  PIN_CHECK=unmet tally_pins=26 digest_pins=5 mismatches=1 unparsed=0 no_command=0 dropped=0 min_tally_pins=26 rev=2d85e33… baseline=yes
```

All four controls stay **unmet** with exit 1, as required.

---

## 4. Summary / findings

1. **Controls reproduce the committed receipts exactly** when run with the
   frozen instrument bytes (`git show 63eecf2…:tools/mori-pin-check.py`):
   all four `PIN_CHECK=unmet`, rc 1, line-for-line identical to
   `evidence/control-c1-*.txt`.
2. **Working-tree instrument drifted mid-session**: `tools/mori-pin-check.py`
   matched the contract pin (`e3ef425a…`) at session start but now hashes to
   `104cf3dd…`; the only diff vs frozen bytes is the deleted line
   `    bound = []` in `pin_commands()`. The current working-tree tool crashes
   with `NameError: name 'bound' is not defined` on every C1 command (including
   do-nothing; confirmed by re-run). `stat` mtime `16:43:57.523` indicates the
   change landed during my first batch, between my successful do-nothing run
   and my three `--skill` runs.
3. Per contract, the claim is measured with `git show <freeze>:<path>` when
   working-tree bytes differ — that measurement is the one reported above and
   it fully matches the receipts.
4. Risks for L1: any C1 scoring run against the current working tree will
   crash (NameError) rather than score; the working-tree file should be
   restored byte-exact to the pin (or scoring must use the frozen bytes). The
   author of the observed working-tree change is UNVERIFIED (not this seat).
5. No tools installed or updated (none needed); TMPDIR used for all lane-tool
   runs. Scratch evidence kept under
   `.scratch/r47-ExecC1Controls/`: `run-*.out` (first batch), `cur-donothing.out`
   (working-tree rerun crash), `frozen-mori-pin-check.py` (materialized frozen
   bytes), `fz2-*.out` (frozen-tool runs, 33 lines each).
