# ExecSelftestOrphans — real `--selftest` branches for the two orphan tools

Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`
Seat: `L1Mori45.ExecSelftestOrphans` (round 45, residual executor)
Scratch: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/tmp/ExecSelftestOrphans`

## Files changed (only these two; no other lane file touched)

| path | change | diffstat |
|---|---|---|
| `tools/mori-disk-rate.py` | `--selftest` argv branch + bounded self-test (14 arms) | +206 |
| `tools/mori-round41-calibration.py` | `--selftest` argv branch + bounded self-test (10 arms); `parse_gate_output` extracted from `observed_counts` byte-identically | +200 −2 |

No new dependency: both use only stdlib (`subprocess`, `tempfile`, `os`), already imported families.
No tool was installed or upgraded for this seat.

### Behaviour

- `--selftest` is detected **before** the argparse required-argument contract, so the
  production usage errors stay argparse's own (`--interval-ms` required for
  disk-rate; `revision`/`--repo`/`--reference-rev` required for the calibration
  counter). Both tools' `main` now normalise `argv` to a list first; passing
  `None` still resolves to `sys.argv[1:]`, so a plain CLI run parses the same list
  as before.
- Fixtures are created only under `$TMPDIR` (`tempfile.TemporaryDirectory(dir=TMPDIR)`);
  no `/proc`, no `/sys`, no network, nothing written into the lane. If `TMPDIR` is
  unset the tool prints `SELFTEST SETUP …`, `pass=0 fail=0` and exits 2.
- Tally lines are exactly `MORI_DISK_RATE_SELFTEST pass=<n> fail=<n>` and
  `MORI_R41_CALIBRATION_SELFTEST pass=<n> fail=<n>`; exit 0 all-pass, 1 a failed
  arm, 2 setup.
- The auditor's own predicate accepts both branches (`selftest_flag=True` for both,
  checked in-process against `tools/mori-gate-registry.py`), so the row seats that
  name these paths will count them as registered.

## Arm inventory (every arm asserts; negatives marked)

`tools/mori-disk-rate.py` — 14 arms:

1. `parse_valid` — 14-token sample → `{"sda": 1000, "sda1": 500}`, no malformed.
2. `parse_ignores_short_line` — a 2-token line is ignored (R1).
3. **negative** `parse_rejects_token_count` — a 15-token line is `bad-line`, not a rate (R2).
4. **negative** `parse_rejects_non_decimal` — `4x00` in the sectors field is malformed (R2).
5. `classify_order` — disk / partition / stacked / virtual / unknown from the synthetic
   `class/block` tree, in R3 precedence (non-empty `slaves` beats `device`; empty
   `slaves` falls through to `virtual`).
6. `state_precedence` — ok, reset, new, gone, absent, bad-line (both samples).
7. `sysfs_block_names` — R4 union source; missing tree yields the empty set.
8. `report_rates` — `(3000-1000)*512*1000//1000 = 1024000`; partition rate 512000;
   sysfs-only device is `absent` with `null`; `host_basis=["sda"]`; host sum.
9. **negative** `report_reset_is_null_not_zero` — sectors fall → `reset`, `write_Bps`
   null (never 0) and host null (R5/R6/R7).
10. **negative** `report_bad_line_blocks_host` — a truncated sda line in B → `bad-line`,
    null rate, host null.
11. `cli_production_ok` — real subprocess, two saved samples, exit 0, JSON host 1024000.
12. **negative** `cli_unreadable_sample` — missing sample file → exit 1 and the
    production message.
13. **negative** `cli_half_pair` — `--a` without `--b` → exit 2 and the argparse message.
14. **negative** `cli_zero_interval` — `--interval-ms 0` → exit 2 and the argparse message.

`tools/mori-round41-calibration.py` — 10 arms:

1. `correction_line_wins` — the **last** `Round-41 calibration correction:` line wins.
2. `legacy_scorecard` — `## Round 40 declaration` fallback → (3, 2).
3. `legacy_log` — `## Round 40 ` fallback → (3, None).
4. `legacy_lesson` — lesson fallback → (3, 2).
5. **negative** `unparseable_record_rejected` — no record → `MeasurementError`.
6. `gate_summary_parse` — timing/summary lines → observed (3 as-of, 2 extension).
7. **negative** `gate_missing_timing_rejected` — missing timing line → `MeasurementError`.
8. **negative** `setup_revision` — unresolvable revision → exit 2,
    `MORI_R41_CALIBRATION_SETUP` on stderr.
9. `matching_records` — synthetic git repo (reference-gate commit + record commit):
    exit 0, `mismatches=0`, and all three per-path lines exact.
10. **negative** `mismatched_records` — records claim 4/1 against observed 3/2 →
    exit 1, `mismatches=6`.

## Tallies with exit codes

```
$ TMPDIR=$PWD/.ufo/waves/round-45/tmp/ExecSelftestOrphans/tmp \
    python3 tools/mori-disk-rate.py --selftest
MORI_DISK_RATE_SELFTEST pass=14 fail=0
EXIT=0

$ TMPDIR=$PWD/.ufo/waves/round-45/tmp/ExecSelftestOrphans/tmp \
    python3 tools/mori-round41-calibration.py --selftest
MORI_R41_CALIBRATION_SELFTEST pass=10 fail=0
EXIT=0
```

Setup arm (TMPDIR unset), both tools:

```
$ env -u TMPDIR python3 tools/mori-disk-rate.py --selftest
SELFTEST SETUP TMPDIR is not set
MORI_DISK_RATE_SELFTEST pass=0 fail=0
EXIT=2

$ env -u TMPDIR python3 tools/mori-round41-calibration.py --selftest
SELFTEST SETUP TMPDIR is not set
MORI_R41_CALIBRATION_SELFTEST pass=0 fail=0
r41_setup_EXIT=2
```

Mutation check (the self-tests are not vacuous; mutants are scratch copies, lane files
untouched; long assertion messages elided with `...`):

```
SECTORS_WRITTEN_INDEX = 8     # R2: token 10   (mutant of tools/mori-disk-rate.py)
SELFTEST FAIL parse_valid: AssertionError: {'sda': 0, 'sda1': 0}
SELFTEST FAIL report_rates: ...
SELFTEST FAIL report_reset_is_null_not_zero: ...
SELFTEST FAIL cli_production_ok: ...
MORI_DISK_RATE_SELFTEST pass=10 fail=4
disk-rate_mutant_EXIT=1

mismatches += 0                                (mutant of tools/mori-round41-calibration.py)
SELFTEST FAIL mismatched_records: AssertionError: (0, '')
MORI_R41_CALIBRATION_SELFTEST pass=9 fail=1
r41_mutant_EXIT=1
```

Bounded runtime (wall clock, subprocess timing):

```
tools/mori-disk-rate.py rc=0 wall=0.143s tally=MORI_DISK_RATE_SELFTEST pass=14 fail=0
tools/mori-round41-calibration.py rc=0 wall=0.170s tally=MORI_R41_CALIBRATION_SELFTEST pass=10 fail=0
```

## Production behaviour is byte-for-byte unchanged

Reproduction script: `.ufo/waves/round-45/tmp/ExecSelftestOrphans/run-evidence.sh`
("before" = the committed blobs at `HEAD`; both tools were clean at `HEAD` before the
edit, so those blobs are the pre-edit bytes. "after" = the working-tree tools.)

Representative disk-rate call (`--a`/`--b` saved samples + synthetic `--sysfs`):

```
$ python3 <before|after> --a fixtures/a.diskstats --b fixtures/b.diskstats \
    --sysfs fixtures/sysfs --interval-ms 1000
{"devices": {"sda": {"class": "disk", "state": "ok", "write_Bps": 1024000}, "sda1": {"class": "partition", "state": "ok", "write_Bps": 512000}}, "host_basis": ["sda"], "host_write_Bps": 1024000, "interval_ms": 1000}
exit 0   (stderr empty)
```

Representative calibration call (positional revision + `--repo` + `--reference-rev`
against the synthetic fixture repo):

```
SCORECARD.md recorded_as_of=3 observed_as_of=3 recorded_extension=2 observed_extension=2
LOG.md recorded_as_of=3 observed_as_of=3 recorded_extension=2 observed_extension=2
corpus/lessons/round-40.md recorded_as_of=3 observed_as_of=3 recorded_extension=2 observed_extension=2
MORI_R41_CALIBRATION mismatches=0 observed_as_of=3 extension_rows=2
```

exit 0, stderr empty.

Before/after diff for that representative pair — **empty**, all six streams:

```
$ bash run-evidence.sh
IDENTICAL disk-rate.out
IDENTICAL disk-rate.err
IDENTICAL disk-rate.rc
IDENTICAL r41.out
IDENTICAL r41.err
IDENTICAL r41.rc
SCRIPT_EXIT=0

$ diff -u disk-rate-before.out disk-rate-after.out ; echo $?
0
$ diff -u disk-rate-before.err disk-rate-after.err ; echo $?
0
$ diff -u r41-before.out r41-after.out ; echo $?
0
$ diff -u r41-before.err r41-after.err ; echo $?
0
$ echo "rcs: disk-rate=$(cat disk-rate-before.rc)/$(cat disk-rate-after.rc) r41=$(cat r41-before.rc)/$(cat r41-after.rc)"
rcs: disk-rate=0/0 r41=0/0
$ wc -c disk-rate-out.diff disk-rate-err.diff disk-rate-rc.diff r41-out.diff r41-err.diff r41-rc.diff
0 disk-rate-out.diff
0 disk-rate-err.diff
0 disk-rate-rc.diff
0 r41-out.diff
0 r41-err.diff
0 r41-rc.diff
```

Additional production arms compared before/after (all identical output/stderr):

```
dr-missing   before_rc=1 after_rc=1 out_diff=empty err_diff=empty
dr-halfpair  before_rc=2 after_rc=2 out_diff=empty err_diff=empty
dr-noargs    before_rc=2 after_rc=2 out_diff=empty err_diff=empty
dr-zero      before_rc=2 after_rc=2 out_diff=empty err_diff=empty
r41-badrev   before_rc=2 after_rc=2 out_diff=empty err_diff=empty
r41-norepo   before_rc=2 after_rc=2 out_diff=empty err_diff=DIFF
```

`r41-norepo` differs only in argparse's `prog` (= the invoked filename) and the
consequent line wrap: run from a copy at the same basename the stderr is identical:

```
$ diff -u x-sameb.err r41-norepo-after.err && echo SAME-BASENAME_STDERR_IDENTICAL
SAME-BASENAME_STDERR_IDENTICAL
$ cat r41-norepo-after.rc
2
```

## Auditor (`--rev WORK --audit-all`, no `--audit`)

```
$ python3 tools/mori-gate-registry.py --rev WORK --audit-all
audit tools/mori-disk-rate.py                  FAIL (no row names tools/mori-disk-rate.py)
audit tools/mori-round41-calibration.py        FAIL (no row names tools/mori-round41-calibration.py)
...
tables=7
rev=WORK
mode=population
population_digest=2d1e9096f7622639f3bb45624ffee594caa81c05ee200c9a22323f86d4a9c056
registered=33 unregistered=6 no_selftest=0 duplicate=0 wrong_row=0 tables=7
REGISTRY=unmet
AUDIT_EXIT=1
```

- Counter line: `registered=33 unregistered=6 no_selftest=0 duplicate=0 wrong_row=0 tables=7`.
- `no_selftest` is **0** in this run (it was 1 at my baseline: `mori-routed-r24.py`, whose
  branch landed in the working tree from another seat while I worked).
- Both of my paths are still counted `unregistered=`, with the printed reasons:
  - `tools/mori-disk-rate.py` → `no row names tools/mori-disk-rate.py`
  - `tools/mori-round41-calibration.py` → `no row names tools/mori-round41-calibration.py`
  i.e. they wait on the registry-row seats, not on a missing self-test branch.
- `unregistered=6` = my two paths + `.ufo/waves/round-45/count-c1.py`, `count-c2.py`,
  `count-c3.py` and `tools/mori-wave-settlement.py` (all other seats' rows).
- `REGISTRY=unmet` is therefore driven by the still-missing rows/wrong_row state, not by
  these two tools.

Prior baseline, same command, taken before my edits (recorded so the delta is checkable):

```
registered=32 unregistered=6 no_selftest=1 duplicate=0 wrong_row=0 tables=7
```

## Risks / notes

- `--selftest` is honoured wherever it appears in argv (an argv-scan before argparse),
  so a production invocation that literally passes `--selftest` runs the self-test instead
  of the measurement. That is the intended flag contract and the only observable argv
  change; the same flag previously failed as unrecognised (exit 2).
- Both self-tests require `TMPDIR` to name an existing directory and return 2 otherwise;
  this matches the lane's existing convention (`mori-evidence-loss.py`,
  `mori-dispatch-ledger.py`) and keeps fixtures out of the lane. A gate that runs them
  must therefore export `TMPDIR`.
- The calibration self-test shells out to `git` inside a scratch repo (isolated
  `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, no network). If `git` is
  absent the fixture arms fail as arms (exit 1), not as setup (exit 2).
- `observed_counts` was refactored to delegate to `parse_gate_output`; the extraction
  moves the same statements, and the byte-identical production receipts above (plus the
  additional six arms) cover it.

No blockers.
