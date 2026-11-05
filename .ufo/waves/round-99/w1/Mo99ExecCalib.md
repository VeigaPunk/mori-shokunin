# Mo99ExecCalib — C2 re-derivation without count-c2.py

Seat: Mo99ExecCalib (executor). Lane: mori. Round 99 attempt 1, wave w1.
Revisions: entering 73308ff6e5c933f53498e9501ef95917b0ef7171, landing 5013f0be8ac9e7fce3c08b680e43cf9cbd49620d.
Fleet pin: MANIFEST.json @ 4ad377eae8e3eed8f7f32ab5d335feb25dbae94b. Fleet HEAD checked: 1873b44294730837764345bd782adca153fa7f62.
Method: read-only git (`show`, `diff`, `rev-parse`). Derivation in Python over MANIFEST `rounds[]`. The frozen counter was not run.

## 1. Expected latest admitted mori closure per axis (pin 4ad377e)

Filter: `lane == mori`, `type == closure`, `admitted is True`, `verdicts[axis] in {improved, harmed}`. Highest `lane_round` wins.

| axis | lane_round | rounds[] index | verdict | pointer |
|---|---|---|---|---|
| coverage | 98 | 1389 | improved | corpus/lessons/round-98-verifier-spotcheck.md:89 |
| operability | 97 | 1384 | improved | corpus/lessons/round-97-verifier-spotcheck.md:78 |
| depth | 86 | 1205 | improved | corpus/lessons/round-86-verifier-spotcheck.md:145 |
| freshness | 97 | 1384 | improved | corpus/lessons/round-97-verifier-spotcheck.md:79 |
| calibration | 98 | 1389 | improved | corpus/lessons/round-98-verifier-spotcheck.md:90 |
| adjacency | 19 | 398 | improved | no spot-check file; MANIFEST rounds[398] |

No axis has a `harmed` verdict in the latest closures.

## 2. Spot-check lines at landing (5013f0be)

Read with `git show 5013f0be…:corpus/lessons/round-NN-verifier-spotcheck.md`. Raw line reads:

- `round-86…:145` → `| depth | **improved** | the 64-row classification is re-derived with a value channel (14 rows), two contradictions named, capability row entered |`
- `round-98…:89` → `| coverage | improved | C1 above |`
- `round-98…:90` → `| calibration | improved | C2 above |`
- `round-97…:78` → `| operability | improved | C1 above |`
- `round-97…:79` → `| freshness | improved | C2 above |`

Each line grades its axis as improved, and each file exists at landing. Adjacency has no spot-check file, as the cell already says.

## 3. SCORECARD `## Axes` cell check (entering → landing)

| axis | Score enter | Score land | Evidence cell | Last-change cell |
|---|---|---|---|---|
| coverage | 6 | 6 | leads with `round-98…:89` pointer; entering text kept verbatim as tail | `round 98 (improved, score held); ` prepended to entering |
| operability | 7 | 7 | leads with `round-97…:78` pointer; tail verbatim | unchanged |
| depth | 5 | 5 | leads with `round-86…:145` pointer; tail verbatim | unchanged |
| freshness | 5 | 5 | leads with `round-97…:79` pointer; tail verbatim | unchanged |
| calibration | 5 | 5 | leads with `round-98…:90` pointer; tail verbatim | `round 98 (improved, score held); ` prepended to entering |
| adjacency | 6 | 6 | unchanged | unchanged |

Results:
- Score cells equal entering for all six axes.
- Last-change cells equal entering or entering with exactly one prepended `round 98 (improved, score held); ` clause (coverage, calibration). Other axes are unchanged.
- Evidence cells: each now leads with a pointer that matches the derivation in section 1. Each pointer's grading line is in section 2. Each tail is the entering text.

Full diff check: `git diff 73308ff6… 5013f0be… -- SCORECARD.md` changes only the five axis rows at the top of `## Axes` (the adjacency row is byte-identical). The diff stat for the whole landing range is 22 files, and SCORECARD.md shows 10 +- lines (the 5 modified table rows and the "Last change" edits, as recorded in the stat).

## 4. Pin vs current fleet HEAD (1873b442)

- `MANIFEST-head.json` begins with the identical 1390-entry prefix of the pin. HEAD has one extra entry (`rounds[1390]`, lane `kagi`, round 45). That entry is not a mori entry.
- Derivation at HEAD gives the same six `(lane_round, index)` pairs as the pin (`HEAD-vs-PIN deltas: {}`).
- No mori closure with `lane_round > 98` exists at HEAD. No mori round 99 entry exists at HEAD (`HEAD mori closures lane_round>98: []`, `HEAD mori r99 entries: []`).
- So the expectations from the pin have not changed. The landing pointers remain correct at HEAD.

## 5. Verdict

C2 holds. An independent re-derivation from the pinned MANIFEST matches all six pointers, and every grading line exists at landing. Scores held. Only the expected cells changed.

Checks not run: count-c2.py (by instruction, the point was to derive without it); controls-r99.py, count-c1.py (out of seat scope).

Tooling: none installed. Used Python (`_eval` kernel, stdlib json/re) and git.

VERDICT C2 holds: independent derivation from MANIFEST 4ad377e matches all six Evidence pointers, the grading lines exist at 5013f0be, Score cells equal entering, Last-change diffs are the single prepended clause, and HEAD adds only a kagi round-45 entry with no change to the mori expectations.
