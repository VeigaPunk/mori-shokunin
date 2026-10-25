# mori round 46 claim — calibration repair

## Frozen predicate

**C1, calibration, score held at 5.** Before: the prior committed SKILL.md has incorrect values in the four round-45 verifier-flagged registry rows (`:184`, `:190`, `:191`, `:194`). After target: four named rows carry the observed selftest tallies and instrument digest/line-count pins, and the prior committed SKILL snapshot remains red under `count-repins.py`. The single predicate label is `MORI_R45_REPINS mismatches=0 rows=4`; counter `count-repins.py` exit 0 is intended as pass, exit 1 as fail.

## Control and freeze-order qualification

The counter code and repaired registry changes existed before the first counter invocation. The control was `git show 12c89ea63491fcca0f46169d809740711d3d052e:SKILL.md`, committed as `.ufo/waves/round-46/control-skill.md`; it scored 4 row mismatches, rc 1. The repaired SKILL scored 0 row mismatches, rc 0. However, this contract text was recorded after those preliminary runs, not before any score; this ordering defect is disclosed, not backdated.

## Falsification boundary

The one-wave counter/predicate was not changed after seats received it. The 32-seat wave found a false green by placing stale receipt strings outside the semantic cells while leaving those cells stale. Thus the frozen counter does not prove that values match observations. C1 is reported **unprovable**; the repaired cell values were separately measured, but that does not rescue the frozen predicate.
