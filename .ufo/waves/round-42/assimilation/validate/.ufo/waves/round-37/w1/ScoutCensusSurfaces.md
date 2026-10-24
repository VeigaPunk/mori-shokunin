# ScoutCensusSurfaces — census surfaces unchanged (round 37)

**Item attacked:** no census surface changed between entering tip `842a320` and scored tip `e57c58b57c025364e79d130fbdf764d2674d83d6`. Surfaces: `tools/mori-census.sh`, `tools/mori-silence-cases.sh` (silence oracle), and committed oracle or baseline paths.

**Axes:** (1) the name-status list is complete, (2) none of those surfaces appear, (3) a receipt whose name contains "census" is not itself a surface.

**Installs:** none.

## Command

```
git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse 842a320 e57c58b57c025364e79d130fbdf764d2674d83d6
```

Observed:

```
842a32074b5c7972e9728f3f629d83eb92f127c2
e57c58b57c025364e79d130fbdf764d2674d83d6
```

```
git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff 842a320..e57c58b57c025364e79d130fbdf764d2674d83d6 --name-status
```

Observed (25 paths; `wc -l` = 25):

```
A	.ufo/waves/round-37/__pycache__/count-c1.cpython-314.pyc
A	.ufo/waves/round-37/__pycache__/count-c2.cpython-314.pyc
A	.ufo/waves/round-37/contract.md
A	.ufo/waves/round-37/count-c1.py
A	.ufo/waves/round-37/count-c2.py
A	.ufo/waves/round-37/evidence/c1-before-memo.txt
A	.ufo/waves/round-37/evidence/c1-before-summary.txt
A	.ufo/waves/round-37/evidence/c2-before.txt
A	.ufo/waves/round-37/evidence/census-start.txt
A	.ufo/waves/round-37/evidence/drift-live-r37.txt
A	.ufo/waves/round-37/evidence/freeze-r37.txt
A	.ufo/waves/round-37/evidence/r17-jj-selftest-r37.txt
A	.ufo/waves/round-37/fixtures/const.py
A	.ufo/waves/round-37/fixtures/memo-n1.py
A	.ufo/waves/round-37/fixtures/summary-only.py
M	SCORECARD.md
M	corpus/README.md
M	corpus/SOURCES.md
A	corpus/evidence/sources-r37/S221.src
A	corpus/evidence/sources-r37/S222.src
A	corpus/evidence/sources-r37/S223.src
A	corpus/evidence/sources-r37/S224.src
A	corpus/knowledge/source-drift-hardening-r37.md
M	tools/mori-round17-jj-regressions.py
M	tools/mori-source-drift.py
```

## Surface check

Keyword filter on that list (`census|silence|oracle|baseline`, case-insensitive) matched exactly one path:

```
A	.ufo/waves/round-37/evidence/census-start.txt
```

That file is a new wave receipt, not a census surface. It is not `tools/mori-census.sh`, not `tools/mori-silence-cases.sh`, and not an oracle or baseline artifact.

Named tools, restricted diff:

```
git diff --name-status 842a320..e57c58b57c025364e79d130fbdf764d2674d83d6 -- tools/mori-census.sh tools/mori-silence-cases.sh
git diff --quiet 842a320..e57c58b57c025364e79d130fbdf764d2674d83d6 -- tools/mori-census.sh tools/mori-silence-cases.sh
```

Observed: no paths printed; `quiet_exit=0` (byte-identical across the range). Both files exist at the scored tip (`git ls-tree` lists `tools/mori-census.sh` and `tools/mori-silence-cases.sh`).

Committed behavioral baselines at the scored tip, also absent from the 25-path list:

- `corpus/evidence/baseline-r10-20261015T2231Z.json`
- `corpus/evidence/baseline-r20-20261021T1051Z.json`

No path in the diff is under `tools/` except `tools/mori-round17-jj-regressions.py` and `tools/mori-source-drift.py`. Neither is the census, the silence oracle, or a baseline pin. No `*oracle*` or `*baseline*` path is added, modified, or deleted.

## Conclusion

No census surface is in `842a320..e57c58b`. The two census tools are unchanged; the committed baseline pins and every tracked oracle path are outside the diff. The sole "census" name is the receipt `evidence/census-start.txt`.

**Confidence:** high (full name-status, line count, restricted quiet diff, tip `ls-tree`).

**Unknowns:** none for this item. Working-tree files outside the scored range were not scored.

VERDICT: PASS
