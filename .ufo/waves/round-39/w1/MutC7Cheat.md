# MutC7Cheat — r38-M18 cheat probe: r38 `drift_kill` accept vs v2 `drift_kill_v2` reject

Seat: `mori-r39.MutC7Cheat` (mutation-tester, wave 1).
Scope: one probe. Lane repo read-only; all builds/runs under
`.ufo/waves/round-39/scratch/MutC7Cheat/`.

**Verdict: PASS (as assigned).** On committed sandbox bytes carrying the r38-M18 cheat
probe, the r38 counter accepts (`check drift_kill PASS`, `C4=met`, exit 0) and the
round-39 counter rejects (`check drift_kill_v2 FAIL`, `C7=unmet`, exit 1). Pristine-byte
baselines are `met` on both counters, so neither detector is stuck.

## Mutant

The r38-M18 cheat shape, identical to the substitution in
`.ufo/waves/round-39/fixtures/run-c7-reds.py` section 3 (whose receipt is
`evidence/c7-red-classifier.txt`): the probe's `row_states` check detail always appends
both `('S103', 'drifted')` and `('S103', 'excerpt')`, independent of classification:

```python
# tools/mori-source-drift.py:390-391 at 13bfba23, pristine
            checks.append(("row_states", got == expected,
                           "got=%r want=%r" % (got, expected)))
# mutated
            checks.append(("row_states", got == expected,
                           "got=%r want=%r ('S103', 'drifted') ('S103', 'excerpt')"
                           % (got, expected)))
```

Constraint check on the pristine file: exactly one occurrence of the edit anchor
(`grep -c` = 1); substitution asserted count==1 in `build-and-run.sh`.

| artifact | sha256 |
|---|---|
| pristine `tools/mori-source-drift.py` (tip 13bfba23, = lane worktree) | `453c5d8e260301df7a99daf62b4c16ea08e4a0b4f9e4f53821cdbce447011552` |
| cheat probe bytes (sandbox-cheat commit `9bb83780de4b7b5cb090824bde7066795f3a7cd5`) | `ff92ca4012bc2c69eab5bf01519ec37c5cceaceceb7292a70c60b78c1e00f796` |
| pristine control bytes (sandbox-pristine commit `a927f6b9ef4bb943b8b7714f48fbdbfd1722f452`) | `453c5d8e260301df7a99daf62b4c16ea08e4a0b4f9e4f53821cdbce447011552` |

Sandboxes were built with `git archive 13bfba23 -- <the paths both counters read>`
(tool, knowledge entry, `SCORECARD.md`, `corpus/SOURCES.md`, the live receipt,
`.ufo/waves/round-37/evidence/c2-after-v3.txt` (capability-cited), `corpus/evidence/`),
then `git init` + one commit each, so the counters read committed bytes exactly as at a
rev. Cheat diff is confined to the single `row_states` detail expression; every other
byte of the probe is the tip's.

## Detectors

- r38 `drift_kill` — frozen bytes `git show 13f3db7e:.ufo/waves/round-38/count-c4.py`,
  extracted copy hash `8332341c3901ef09e76bbd7f31e8c8e68b4e4ecc5d3002f2d20201c9e7093ba1`.
  Mutates `return "drifted"` → `return "excerpt"` and requires
  `kill_rc == 1 and state[0] == "FAIL" and flipped`, where `flipped` is a symmetric
  substring test: `('S103', 'drifted')` present **and** (`('S103', 'excerpt')` or
  `('S103', 'fresh')`) present in the detail string (`count-c4.py:296-301`).
- r39 `drift_kill_v2` — `.ufo/waves/round-39/count-c7.py` at the scored tip, lane-file
  hash `b92c65f224a6268a901aa6bc5ad66b499048eaca82b493356eb8e1f324ef0520`
  (= `git show 13bfba23:...`). Draws the post-mutation state at run time, then parses
  `got=[...] want=[...]` structurally (`parse_got_want`, `count-c7.py:343-370`; the
  want capture is end-anchored at `:351`) and asserts `set(got)==set(want)`,
  `want_drifted` non-empty, every drifted row's got state == the drawn state, and all
  non-drifted rows equal (`:498-507`).

Counter copies for this run differ from the frozen bytes by exactly one line:
`SCRATCH_ROOT` retargeted into this seat's scratch (diffs in
`scratch/MutC7Cheat/{r38,c7}/patch.diff`) so no temp dirs land in the lane's shared
scratch root. Patched copies: r38 `106519fd…`, c7 `8df42bf6…`; pristine copies
`8332341c…` / `b92c65f2…`.

## Outputs (exact)

Calibration seed of record `--seed 20261024` draws `fresh` (matches
`evidence/c7-after.txt`).

```
$ python3 r38/count-c4.py HEAD --repo sandbox-cheat            # exit 0
check named_row_drift  PASS (exit=0 row_states=('PASS', ''))
check drift_kill       PASS (exit=1 row_states=('FAIL', "got=[('S101', 'fresh'), ('S102', 'excerpt'), ('S103', 'excerpt'), …, ('S110', 'unavailable')] want=[… ('S103', 'drifted') …] ('S103', 'drifted') ('S103', 'excerpt')"))
C4=met
```

```
$ python3 c7/count-c7.py HEAD --repo sandbox-cheat --seed 20261024   # exit 1
check anchors_v2       PASS (anchors=3 short=[] not_in_code=[] unique=True)
check capability_v2    PASS (paths=['tools/mori-source-drift.py', '.ufo/waves/round-37/evidence/c2-after-v3.txt', '.ufo/waves/round-37/evidence/drift-live-r37.txt'] not_file=[])
check live_rows_v2     PASS (named=10 summary_drifted=10 unknown=[] unique=True no_copy=[])
check named_row_drift  PASS (exit=0 row_states=('PASS', ''))
check drift_kill_v2    FAIL (drawn=fresh exit=1 row_states=('FAIL', "got=[('S101', 'fresh'), …, ('S103', 'fresh'), …] want=[… ('S103', 'drifted') …] ('S103', 'drifted') ('S103', 'excerpt')"))
C7=unmet
```

Independent seed `--seed 7` draws `unavailable` and also rejects:
`check drift_kill_v2 FAIL (drawn=unavailable …)`, `C7=unmet`, exit 1. Only
`drift_kill_v2` flips on the cheat sandbox; the other four checks and all four negative
witnesses are unchanged (`rejected`), so the rejection is attributable to the drift arm.

Pristine-byte controls on the same instrumentation:
`r38: check drift_kill PASS (exit=1 row_states=('FAIL', "got=[… ('S103', 'excerpt') …] want=[…]"))`, `C4=met`, exit 0;
`c7: check drift_kill_v2 PASS (drawn=fresh … want_drifted=['S103'] flips_ok=True)`, `C7=met`, exit 0.

## Why the discrimination is real (observed, not assumed)

- r38 is fooled exactly as the M18 class predicts: its `flipped` predicate
  (`count-c4.py:298-301`) sees the appended literal tokens in the detail, so a detail
  string the probe emits unconditionally satisfies it. Cheat and pristine r38 runs are
  verdict-identical (`drift_kill PASS`, `C4=met`), i.e. the mutation is invisible to r38.
- v2 is not fooled by this artifact: the end-anchored want capture
  (`count-c7.py:351`) cannot match once the probe appends text after the `want=[...]`
  table, so `parse_got_want` returns `None` at `:498`. The absence of the
  `want_drifted=… flips_ok=…` suffix in the observed FAIL detail (present only when
  `parsed is not None`, `:503-507`) confirms the parse-failure path, not a coincidental
  mismatch. The detail's got table is honest (`S103` = drawn state), so the cheat's only
  effect is the appended suffix — precisely what v2 rejects.

## Restoration / write-scope evidence

No lane file was modified; the mutant lived only in the sandbox commit.

```
sha256 lane tools/mori-source-drift.py        before = after = 453c5d8e260301df7a99daf62b4c16ea08e4a0b4f9e4f53821cdbce447011552
sha256 lane .ufo/waves/round-39/count-c7.py   before = after = b92c65f224a6268a901aa6bc5ad66b499048eaca82b493356eb8e1f324ef0520
```

(`scratch/MutC7Cheat/hash-lane-before.txt`, `hash-lane-after.txt`.) Lane
`git status --porcelain` is unchanged apart from pre-existing untracked scratch and
other seats' `w1/*.md`; the only file this seat writes in the lane tree is this report.
`tmp-c7/` and `tmp-r38/` are empty after the runs (counter `finally` cleanup), and no
`mori-c7-*`/`mori-c4-*` dir was created outside `scratch/MutC7Cheat/`.

## Artifacts

`scratch/MutC7Cheat/`: `build-and-run.sh` (`56a1f7bd…`), `out-r38-cheat.txt`
(`0d2b9db2…`), `out-r38-pristine.txt` (`9dbe99ff…`), `out-c7-cheat-s20261024.txt`
(`fc66330c…`), `out-c7-cheat-s7.txt` (`97735de8…`), `out-c7-pristine-s20261024.txt`
(`c03e05ce…`), `sandbox-*.rev`, `hash-*.txt`, `{r38,c7}/patch.diff`.

Bounds: sandbox is the scored tip's subset of paths the counters read (rev
`13bfba23`); wall clock 46 s; no installs (nothing in this task needed a tool, so no
package-manager transaction was attempted); no remediation or contract judgement
attempted. A surviving/accepting detector is reported as the r38 coverage finding it
is; the v2 kill is evidence for C1's drift arm only, not a global verdict.
