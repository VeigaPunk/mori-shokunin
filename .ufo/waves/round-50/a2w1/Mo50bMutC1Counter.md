# Mo50bMutC1Counter — mutation test of `.ufo/waves/round-50/count-c1.py` (round 50 a2w1)

- MACHINE_ID: `432d02b544a5459ebbff9c42ec68334d`
- Date: 2026-10-26. Leaf seat, no subagents. Detection and report only.
- Target: `.ufo/waves/round-50/count-c1.py` (frozen counter, P-C1), mutated in scratch copies only.
- Scratch: `/fast/scratch/hyaku/mori-r50/Mo50bMutC1Counter/` (removed at end of session; all cited
  outputs are copied inline below). `TMPDIR` pointed inside the scratch dir for every run; every
  counter score run passed `--scratch` inside the scratch dir so the archive tree never landed in
  `/tmp`. No tool was installed or upgraded (none needed; pacman untouched). Disk-guard checked
  before the runs: `/fast/scratch/hyaku` 24% used, 614.2G free — no ENOSPC.
- Kill rule (as tasked): a mutant is **killed iff `--selftest` exits non-zero**. Each mutant was
  additionally scored at the landed data tip `487941b9395e89678af0053cc443cdb49cdee6e3` to show
  real-behavior impact. Survivors are coverage limits, not contract changes.

## Baseline (pristine bytes)

Pristine copy sha256 equals the freeze entry (`evidence/freeze-sha256.txt:16`):

```
2d5c3ee53198124ef001908cc5abba5c71a6fb63773c31ece211b7c6cdae4456  count-c1.py.orig
2d5c3ee53198124ef001908cc5abba5c71a6fb63773c31ece211b7c6cdae4456  count-c1.py
2d5c3ee53198124ef001908cc5abba5c71a6fb63773c31ece211b7c6cdae4456  .ufo/waves/round-50/count-c1.py  (freeze-sha256.txt line 16)
```

```
$ python3 count-c1.py --selftest ; echo exit=$?
...
C1_SELFTEST pass=34 fail=0
exit=0
```

```
$ python3 count-c1.py 487941b9395e89678af0053cc443cdb49cdee6e3 \
    --repo /home/vgpnk/Projects/shokunin/mori-shokunin \
    --fleet-repo /home/vgpnk/Projects/shokunin \
    --scratch /fast/scratch/hyaku/mori-r50/Mo50bMutC1Counter/run-base ; echo exit=$?
item axis coverage expect=round_47_improved got=ok state=ok
item axis operability expect=round_47_improved got=ok state=ok
item axis depth expect=round_49_improved got=ok state=ok
item axis freshness expect=round_28_improved got=ok state=ok
item axis calibration expect=round_49_improved got=ok state=ok
item axis adjacency expect=round_19_improved got=ok state=ok
item pin python3_tools/mori-pin-check.py_--selftest expect=(114/114) got=PIN_CHECK_SELFTEST_pass=114_fail=0 state=ok
item pin python3_tools/mori-unlanded-check.py_--selftest expect=(17/17) got=UNLANDED_SELFTEST_pass=17_fail=0 state=ok
C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=487941b9395e89678af0053cc443cdb49cdee6e3
exit=0
```

Both baseline detectors are green, so every mutant result below is interpretable.

## Mutants

Each row: one single-point edit applied to the scratch working copy, `--selftest` run, score run at
`487941b…`, then the pristine bytes restored (`cp count-c1.py.orig count-c1.py`) and the sha256
re-verified to `2d5c3ee5…4456` after every mutant (12/12 restorations verified; hashes below).

| # | Mutation (site in pristine file) | selftest | score at 487941b | verdict |
|---|---|---|---|---|
| M1 | accept `unchanged` as a target grade (`manifest_targets`, L75: `in ("improved", "harmed")` → `+ "unchanged"`) | exit 0, `pass=34 fail=0` | exit 1, `mismatches=4` | **SURVIVED** |
| M2 | drop the `verdict == "admitted"` round filter (`manifest_targets`, L68) | exit 0, `pass=34 fail=0` | exit 0, identical to baseline | **SURVIVED** |
| M3 | drop the `n > through` cut (L72) | exit 1, `pass=22 fail=12` | exit 0, identical | killed |
| M4 | take the first graded round, not the last (L75: `n >= best.get(ax, (-1, ""))[0]` → `ax not in best`) | exit 1, `pass=24 fail=10` | exit 1, `mismatches=6` | killed |
| M5 | drop the verdict-word check (`check_axes`, L140–141) | exit 1, `pass=33 fail=1` | exit 0, identical | killed |
| M6 | drop the evidence-pointer check (L142–143) | exit 1, `pass=32 fail=2` | exit 0, identical | killed |
| M7 | accept `rows=2` (`check_axes`, L124: `!= 1` → `not in (1, 2)`) | exit 1, `pass=33 fail=1` | exit 0, identical | killed |
| M8 | drop the hidden-token scan (`parse_shonen`, L158) | exit 1, `pass=32 fail=2` | exit 0, identical | killed |
| M9 | drop the receipt check (`check_pins`, L201–203) | exit 1, `pass=31 fail=3` | exit 0, identical | killed |
| M10 | drop the pins floor (`evaluate`, L225–226) | exit 1, `pass=33 fail=1` | exit 0, identical | killed |
| M11 | drop the boxes floor (L227–228) | exit 1, `pass=33 fail=1` | exit 0, identical | killed |
| M12 | treat a runner error as ok (`check_pins`, L186: `"error"` → `"ok"`) | exit 1, `pass=33 fail=1` | exit 0, identical | killed |

Score: **10 killed / 2 survived / 0 inconclusive.** Both survivors sit in `manifest_targets`
(round selection); every per-row and per-pin check is selftest-guarded.

## Survivor evidence

### M1 — accept `unchanged` (selftest exit 0; landed-tip score flips met → unmet)

```
$ python3 count-c1.py --selftest ; echo exit=$?        # mutant bytes
C1_SELFTEST pass=34 fail=0
exit=0
$ python3 count-c1.py 487941b… --repo … --scratch …/run-m1 ; echo exit=$?
item axis coverage expect=round_49_unchanged got=round=47,verdict_word_missing,evidence_missing:corpus/lessons/round-49-verifier-spotcheck.md state=mismatch
item axis operability expect=round_49_unchanged got=round=47,verdict_word_missing,evidence_missing:corpus/lessons/round-49-verifier-spotcheck.md state=mismatch
item axis freshness expect=round_49_unchanged got=round=28,verdict_word_missing,evidence_missing:corpus/lessons/round-49-verifier-spotcheck.md state=mismatch
item axis adjacency expect=round_49_unchanged got=round=19,verdict_word_missing,evidence_missing:corpus/lessons/round-49-verifier-spotcheck.md state=mismatch
C1=unmet items=8 axes=6 pins=2 boxes=4 mismatches=4 errors=0 hidden=0 manifest=a94551c5bc8d rev=487941b… failed=mismatch
exit=1
```

Why the selftest is blind: in the selftest fixture manifest the only `unchanged` grade is
`depth` at round 47, and round 49 grades `depth` `improved`, so the fixture never has an axis whose
**latest** accepted grade is `unchanged` at a round later than its target — the mutant changes no
fixture expectation. On the real MANIFEST at `e014499…` it changes four targets (round 49 grades
coverage/operability/freshness/adjacency `unchanged`), so the landed claim would flip to unmet —
the score run detects it, but the tasked kill rule (selftest-only) does not.

### M2 — drop the `admitted` round filter (selftest exit 0; landed-tip score unchanged)

```
$ python3 count-c1.py --selftest ; echo exit=$?        # mutant bytes
C1_SELFTEST pass=34 fail=0
exit=0
$ python3 count-c1.py 487941b… --repo … --scratch …/run-m2 ; echo exit=$?
C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=487941b…
exit=0
```

Behavioral probe proving the mutant bytes really execute (crafted manifest where a rejected round
is the only one grading an axis):

```
manifest = {"rounds":[{"lane":"mori","lane_round":45,"verdict":"rejected-harmed",
                       "verdicts":{"freshness":"improved"}}]}
mutant   manifest_targets -> {'freshness': (45, 'improved')}
pristine manifest_targets -> {}
```

Why nothing catches it: the selftest's only check named for this filter,
`rejected_round_ignored`, asserts `manifest_targets(manifest)["calibration"] == (49, "improved")`
— vacuous under the mutant, because the fixture's rejected round 45 (calibration `harmed`) is
superseded by admitted round 49 either way. The real MANIFEST at `e014499…` is also insensitive:
its rejected mori rounds (13, 17, 20, 23, 27, 29, 30, 32–35, 40, 42, 45) grade axes only at rounds
at or below the admitted targets (the highest, round 45: operability/calibration/depth, superseded
by admitted 47/49). So today the filter is unenforced by both detectors; it would start to matter
only if a future MANIFEST recorded a rejected round as the latest round grading some axis.

## Restoration evidence

After every mutant the pristine bytes were restored with `cp count-c1.py.orig count-c1.py` and the
sha256 re-checked; 12/12 restorations printed `2d5c3ee53198124e…` (full hash
`2d5c3ee53198124ef001908cc5abba5c71a6fb63773c31ece211b7c6cdae4456`, equal to the freeze entry).
Mutant hashes observed while testing (first 16 hex): M1 `f99fa73a94dbb277`, M2 `027794b054fdff1b`,
M3 `fd4196cc8fe755b4`, M4 `9f2ab9b9218f4e64`, M5 `d8cb45c0e4c6e238`, M6 `8a08db710786f0a9`,
M7 `8721696331e0f3a3`, M8 `f8bc487c06d6646a`, M9 `27e12f45008250b0`, M10 `8434e5829aace879`,
M11 `8ccd528d1e6135c8`, M12 `ca65453d5be3bfaa`. The frozen lane file itself was never opened for
writing; its hash was re-verified at the end (`2d5c3ee5…4456`).

## Notes for the L1 (no contract change proposed)

- For M5–M12 the landed-tip score run is byte-identical to baseline: on honest landed data the
  selftest is the only detector for those mutations. That is the intended design (the negative
  fixtures live in the selftest), not a defect.
- M3 is killed by the selftest alone; the pinned MANIFEST has no mori round above 49, so real data
  cannot exercise the through cut today. Fixture-only protection, currently sufficient.
- M4 is double-detected (selftest + landed score): under the mutant the targets become the
  earliest graded rounds (coverage 12, operability 18, depth 12, freshness 21, calibration 12,
  adjacency 14) and the landed tip scores `mismatches=6` unmet.
- Per the tasked kill rule both survivors are limits of the frozen counter's selftest, not grounds
  to change the counter, the predicate or the controls.

## Findings

- **HIGH** — `count-c1.py:68` (`manifest_targets`): dropping the `verdict == "admitted"` round
  filter survives `--selftest` (34/34) and leaves the landed-tip score unchanged. The only
  selftest check named for the filter (`rejected_round_ignored`) is vacuous under the mutant, and
  the real MANIFEST at `e014499…` has no rejected round above an admitted target. The filter is
  currently enforced by neither detector; a future MANIFEST where a rejected round is the latest
  to grade an axis would silently move targets (probe: rejected round 45 alone →
  `freshness (45, improved)` instead of absent).
- **MED** — `count-c1.py:75` (`manifest_targets`): accepting `unchanged` as a target grade
  survives `--selftest` (34/34). The fixture manifest never has an axis whose latest accepted
  grade is `unchanged` at a round later than its target. On real data the mutant flips the landed
  tip to `C1=unmet mismatches=4` (coverage/operability/freshness/adjacency targets move to
  round 49 `unchanged`), so the score run catches it — but the tasked selftest-only kill rule
  does not.
- **LOW** — `count-c1.py:72` (through cut): killed by the selftest only; the pinned MANIFEST
  contains no mori round above 49, so the cut is fixture-protected but real-data-untested today.
- **LOW** — selftest check `rejected_round_ignored` (in `selftest()`) asserts a value the M2
  mutant preserves; strengthening it (e.g. asserting that a rejected round's grade never appears
  in the targets, using a fixture where the rejected round is the latest) would close the HIGH
  finding. Named as a limit only — the counter bytes are frozen this round.
