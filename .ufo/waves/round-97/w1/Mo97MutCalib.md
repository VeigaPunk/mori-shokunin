# Mo97MutCalib — r97 w1: mutation sweep of `tools/mori-scorecard-calibration.py --selftest`

Seat Mo97MutCalib, mutation-tester, 2026-11-05. Carried debt (r96 routed defect 7), evidence only —
this round claims nothing on C1/C2 through this file; no claim predicate, counter, target or receipt
was touched. Only lane file written: this report. Scratch `/fast/scratch/hyaku/mori-r97/Mo97MutCalib`
removed after evidence capture (report is the only record). Tools installed: none. Env: Python
3.14.8, git 2.56.0, `TMPDIR` pinned to the scratch dir for every run. The tool was copied into
scratch; every mutant ran from the scratch copy — `tools/` was never executed mutated nor written.

## Baseline (pristine) — detector conclusive

`sha256` before — pristine copy and in-tree original agree:

```
662fafde7ba446e13a30bc88c10a61d99f933be72902053b1e1e871fc5835113  /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-scorecard-calibration.py
662fafde7ba446e13a30bc88c10a61d99f933be72902053b1e1e871fc5835113  /fast/scratch/hyaku/mori-r97/Mo97MutCalib/pristine.py
```

`python3 $S/pristine.py --selftest` (rc=0):

```
arm conformant_met: pass
arm stale_cell_unmet: pass
arm not_admitted_higher_ignored_met: pass
arm verdict_word_missing_unmet: pass
arm duplicate_axis_row_unmet: pass
arm score_cell_changed_unmet: pass
arm evidence_cell_changed_unmet: pass
arm cell_round_missing_unmet: pass
arm no_admitted_expectation_mismatch: pass
arm verdict_word_disagrees_unmet: pass
arm setup_bad_manifest_exit2: pass
CALIB_SELFTEST pass=11 fail=0
```

Baseline failure would have made every verdict inconclusive; it passed, so verdicts below are valid.

## Method

11 mutants (spec asked ≥8), each exactly one string replacement applied to the pristine copy; the
driver asserted the replaced string occurs exactly once in pristine source before writing each
mutant. Detector, identical for all: `TMPDIR=$S python3 <mutant> --selftest`.
Killed = selftest exits non-zero OR reports `fail>0`.

## Results — mutant | change | killed | survivor

| mutant | single change (function) | sha256[:16] | rc | CALIB_SELFTEST | verdict |
|---|---|---|---|---|---|
| M01-min-not-max-admitted-round | `rnd > expected[axis][0]` → `rnd < …` (`load_expectations`) | c56b068c5062f2fe | 1 | pass=1 fail=10 | KILLED |
| M02-any-verdict-word-admitted | `word in VERDICT_WORDS` → `word is not None` (`load_expectations`) | 75cb70bab1def6a3 | 1 | pass=1 fail=10 | KILLED |
| M03-axis-skipped-expectations | `for axis in AXES:` → `AXES[:-1]` (`load_expectations`; drops adjacency) | 2cf1fcab15932351 | 1 | pass=1 fail=10 | KILLED |
| M04-columns-unchanged-ignored | column-diff branch `columns_ok = False` → `pass` (`measure`) | 4a8d5256bb0fba51 | 1 | pass=9 fail=2 | KILLED |
| M05-not-admitted-rows-counted | `if row.get("admitted") is not True:` → `if False:` (`load_expectations`) | 9477a5b146a1d2d6 | 1 | pass=10 fail=1 | KILLED |
| M06-closure-correction-tail-counted | `head = cell.split(";", 1)[0]` → `head = cell` (`cell_round_verdict`) | d4f11c2ca1787981 | 1 | pass=10 fail=1 | KILLED |
| M07-wrong-base-rev-as-base | `resolve_rev(args.repo, args.base)` → `…, args.rev` (`measure`) | 65a2a42e326625a5 | 1 | pass=9 fail=2 | KILLED |
| M08-exit-code-swap-measure | `return (0 if met else 1)` → `(1 if met else 0)` (`measure`) | 44078378030540b5 | 1 | pass=1 fail=10 | KILLED |
| M09-duplicate-axis-row-accepted | `if axis in rows:` → `if False and axis in rows:` (`parse_axes`) | 206ac68e7aed8055 | 1 | pass=10 fail=1 | KILLED |
| M10-verdict-vocab-widened-cells | `for word in VERDICT_WORDS:` → `("improved", "harmed", "neutral")` (`cell_round_verdict`) | 4ca75759adfc745b | 0 | pass=11 fail=0 | **SURVIVED** |
| M11-selftest-exit-code-swap | `return 0 if failed == 0 else 1` → `1 … else 0` (`selftest`) | 9cff328cbed49038 | 1 | pass=11 fail=0 | KILLED |

M11 was killed by the exit-code criterion alone (summary still says `pass=11 fail=0` but rc=1): the
detector honors exit codes, per the kill rule. Per-arm FAIL detail was captured only for the
baseline and M10 reruns; for the other mutants only rc + the `CALIB_SELFTEST` line above were
recorded (unrun: per-arm FAIL text for M01–M09, M11).

## Survivor M10 — coverage finding (defect report, not a contract change)

Full rerun output — byte-for-byte the baseline, rc=0:

```
arm conformant_met: pass
arm stale_cell_unmet: pass
arm not_admitted_higher_ignored_met: pass
arm verdict_word_missing_unmet: pass
arm duplicate_axis_row_unmet: pass
arm score_cell_changed_unmet: pass
arm evidence_cell_changed_unmet: pass
arm cell_round_missing_unmet: pass
arm no_admitted_expectation_mismatch: pass
arm verdict_word_disagrees_unmet: pass
arm setup_bad_manifest_exit2: pass
CALIB_SELFTEST pass=11 fail=0
```

Grounds (code reading of the pristine file): `cell_round_verdict` scans each `Last change` cell for
the words in `VERDICT_WORDS`, but no fixture cell built by `arms()` ever contains a word outside
{improved, harmed}; the fixture's lone `neutral` verdict sits on the expectation side
(`FIXTURE_MANIFEST` round 99) and flows through `load_expectations`, which this mutant does not
touch. Widening the cell-side vocabulary therefore changes no arm's expected line. The selftest
never pins the cell-side verdict vocabulary to {improved, harmed}.

## Restoration evidence

After the sweep (mutant files deleted as each finished):

```
RESTORE-CHECK pristine-sha=662fafde7ba446e13a30bc88c10a61d99f933be72902053b1e1e871fc5835113 orig-sha=662fafde7ba446e13a30bc88c10a61d99f933be72902053b1e1e871fc5835113 identical=True
RESTORE-RERUN rc=0 | CALIB_SELFTEST pass=11 fail=0
```

Before and after hashes of `tools/mori-scorecard-calibration.py` are identical
(`662fafde…35113`); the restored-bytes rerun reproduces the baseline exactly. No in-tree byte was
modified at any point.

## Unrun checks (named)

- Per-arm FAIL output for mutants M01–M09 and M11: unrun (only rc + summary captured).
- `--selftest` mutation sweeps of `mori-gate-registry.py`, `mori-drift-recheck.py`,
  `mori-source-digest.py`, `count-c1.py`, `count-c2.py`: unrun, out of seat scope.
- Any C1/C2 claim measurement at the landing revision: unrun, not this seat's claim.
