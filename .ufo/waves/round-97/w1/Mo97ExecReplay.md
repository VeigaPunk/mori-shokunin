# Mo97ExecReplay — round 97 w1 independent replay

Axes: operability, freshness. Method: `git archive <rev> | tar -x -C $S/<rev>` with
$S=/fast/scratch/hyaku/mori-r97/Mo97ExecReplay, then frozen counters with `--root DIR`.
Read-only git only. No tool installs/updates (not needed). No writes outside this report + scratch.

## (a) Counter replay — exact outputs

### Entering 973b2af11f41bd362163d7e29ac08286832f546b
```
$ python3 .../round-97/count-c1.py --root $S/973b2af11f41bd362163d7e29ac08286832f546b
TARGET tools/mori-cgroup-pressure.py unattributed
TARGET tools/mori-drift-recheck.py unattributed
TARGET tools/mori-scorecard-calibration.py unattributed
TARGET tools/mori-source-digest.py unattributed
C1=unmet unregistered=4 registry=unmet targets_ok=0/4 checks_failed=registry,target_mori-cgroup-pressure.py,target_mori-drift-recheck.py,target_mori-scorecard-calibration.py,target_mori-source-digest.py root=/fast/scratch/hyaku/mori-r97/Mo97ExecReplay/973b2af11f41bd362163d7e29ac08286832f546b
rc=1

$ python3 .../round-97/count-c2.py --root $S/973b2af11f41bd362163d7e29ac08286832f546b
TARGET S615 unpinned copy=- copy_sha=-
TARGET S616 unpinned copy=- copy_sha=-
TARGET S623 unpinned copy=- copy_sha=-
LIVE # MORI_DRIFT_RECHECK second_ua=curl/8.21.0 only=S615,S616,S623 from-sweep=- findings=- run-start=2026-11-05T20:52:15Z stamp-class=python-docs-page-stamp asset-class=learn-microsoft-asset-build-id
LIVE S615 no-copy
LIVE S616 no-copy
LIVE S623 no-copy
LIVE MORI_DRIFT_RECHECK rows=3 adjudicated=0 fresh=0 excerpt=0 time-churn=0 asset-churn=0 receipt-open=0 receipt-stale=0 ua-serving=0 content-drift=0 gate=0 unavailable=0 window=-
C2=unmet mismatch=0 unpinned=3 targets_ok=0/3 hole_guard=n/a live=S615:no-copy,S616:no-copy,S623:no-copy checks_failed=unpinned,target_S615,target_S616,target_S623,live root=/fast/scratch/hyaku/mori-r97/Mo97ExecReplay/973b2af11f41bd362163d7e29ac08286832f546b
rc=1
```

### Landing e85ed91249953094b067554bfa79fcdc65791f8e
```
$ python3 .../round-97/count-c1.py --root $S/e85ed91249953094b067554bfa79fcdc65791f8e
TARGET tools/mori-cgroup-pressure.py row='cgroup PSI survey (r62 tool, registry r97)' selftest_rc=0 selftest_line='MORI_CGROUP_PRESSURE_SELFTEST: pass=12 fail=0' stated_in_cell=yes token_in_verdict_map=yes
TARGET tools/mori-drift-recheck.py row='drift re-check (r66 tool, registry r97)' selftest_rc=0 selftest_line='MORI_DRIFT_RECHECK_SELFTEST: PASS (10 cases)' stated_in_cell=yes token_in_verdict_map=yes
TARGET tools/mori-scorecard-calibration.py row='SCORECARD Last-change calibration counter (r96 tool, registry r97)' selftest_rc=0 selftest_line='CALIB_SELFTEST pass=11 fail=0' stated_in_cell=yes token_in_verdict_map=yes
TARGET tools/mori-source-digest.py row='SOURCES digest check (r91 tool, registry r97)' selftest_rc=0 selftest_line='DIGEST_SELFTEST pass=11 fail=0' stated_in_cell=yes token_in_verdict_map=yes
C1=met unregistered=0 registry=met targets_ok=4/4 checks_failed=- root=/fast/scratch/hyaku/mori-r97/Mo97ExecReplay/e85ed91249953094b067554bfa79fcdc65791f8e
rc=0

$ python3 .../round-97/count-c2.py --root $S/e85ed91249953094b067554bfa79fcdc65791f8e
TARGET S615 superseded-by S619 successor_ok=yes copy_equals_successor=yes copy=corpus/evidence/sources-r97/S615.html copy_sha=7891c58897fe9f78
TARGET S616 ok copy_matches_tool=yes copy=corpus/evidence/sources-r97/S616.html copy_sha=6842ed0f53882c5a
TARGET S623 ok copy_matches_tool=yes copy=corpus/evidence/sources-r97/S623.html copy_sha=90ac3b25cb2dd281
LIVE # MORI_DRIFT_RECHECK second_ua=curl/8.21.0 only=S615,S616,S623 from-sweep=- findings=- run-start=2026-11-05T20:52:23Z stamp-class=python-docs-page-stamp asset-class=learn-microsoft-asset-build-id
LIVE S615 time-churn as-of=2026-11-05T20:52:23Z
LIVE S616 time-churn as-of=2026-11-05T20:52:23Z
LIVE S623 time-churn as-of=2026-11-05T20:52:23Z
LIVE MORI_DRIFT_RECHECK rows=3 adjudicated=3 fresh=0 excerpt=0 time-churn=3 asset-churn=0 receipt-open=0 receipt-stale=0 ua-serving=0 content-drift=0 gate=0 unavailable=0 window=2026-11-05T20:52:23Z..2026-11-05T20:52:23Z
C2=met mismatch=0 unpinned=0 targets_ok=3/3 hole_guard=pass live=S615:time-churn,S616:time-churn,S623:time-churn checks_failed=- root=/fast/scratch/hyaku/mori-r97/Mo97ExecReplay/e85ed91249953094b067554bfa79fcdc65791f8e
rc=0
```
Before values match contract/before receipts exactly; after values match `C1=met ... targets_ok=4/4` and `C2=met mismatch=0 unpinned=0 targets_ok=3/3 hole_guard=pass` (all live classes time-churn ∈ {fresh,time-churn}).

## (b) Counter pins + freeze diff
```
$ sha256sum .../round-97/count-c1.py .../round-97/count-c2.py
78a09016fa8151b72049400600b6b154437c919df6fccb55b8bfa6253b4d2a95  .../count-c1.py
957a7be605ba920734a218388b7ebb50f4f829979931c6e4193caee2149a1e91  .../count-c2.py
$ git diff dd1ae1150f53df54e7530311b2323368e3c0e5e9 e85ed91249953094b067554bfa79fcdc65791f8e -- .ufo/waves/round-97/count-c1.py .ufo/waves/round-97/count-c2.py
(empty, rc=0)
```
Both hashes equal contract.md lines 17-18 and line 1 of evidence/controls-r97.txt verbatim.

## (c) Control battery re-run
```
$ cd $S && HYAKU_SCRATCH=$S bash .../round-97/controls-r97.sh 973b2af11f41bd362163d7e29ac08286832f546b .../round-97/candidate
... (all 9 sub-controls AS_EXPECTED; shown tail:)
C2 forgery (live): C2=unmet mismatch=0 unpinned=0 targets_ok=3/3 hole_guard=pass live=S615:time-churn,S616:time-churn,S623:content-drift checks_failed=live
C2 positive: C2=met mismatch=0 unpinned=0 targets_ok=3/3 hole_guard=pass live=S615:time-churn,S616:time-churn,S623:time-churn checks_failed=-
CONTROLS_DONE unexpected=0
```
`CONTROLS_DONE unexpected=0`, zero `UNEXPECTED` lines. (Scratch nesting under $S/mori-r97/controls/ as the script appends `mori-r97/` to HYAKU_SCRATCH; same hashes since counter sha is content-anchored.)

## (d) Freeze ancestry + freeze touch-set
```
$ git merge-base --is-ancestor dd1ae1150f53df54e7530311b2323368e3c0e5e9 e85ed91249953094b067554bfa79fcdc65791f8e ; echo rc=$?
rc=0 (freeze precedes landing)
$ git show --stat dd1ae1150f53df54e7530311b2323368e3c0e5e9
commit dd1ae1150f53df54e7530311b2323368e3c0e5e9
    round-97: freeze contract, counters C1/C2, pre-freeze control battery (CONTROLS_DONE unexpected=0)
 .ufo/waves/round-97/candidate/S615.html       | 3339 +++++++++++++++++++++++++
 .ufo/waves/round-97/candidate/S616.html       |  715 ++++++
 .ufo/waves/round-97/candidate/S623.html       | 1922 ++++++++++++++
 .ufo/waves/round-97/candidate/skill-append.md |   17 +
 .ufo/waves/round-97/contract.md               |   83 +
 .ufo/waves/round-97/controls-r97.sh           |   74 +
 .ufo/waves/round-97/count-c1.py               |  119 +
 .ufo/waves/round-97/count-c2.py               |  152 ++
 .ufo/waves/round-97/evidence/controls-r97.txt |  111 +
 9 files changed, 6532 insertions(+)
```
Freeze touches only `.ufo/waves/round-97/` — no SKILL.md, no corpus/ bytes. Ancestry confirmed.

## Checks not run
None for (a)-(d). Live legs re-fetched at 20:52Z; vendor stamp may churn again later but live leg met at measurement time.

VERDICT C1 holds: entering unmet (unregistered=4, 0/4) → landing met (unregistered=0, registry=met, targets_ok=4/4, rc=0), pins/freeze diff verified.
VERDICT C2 holds: entering unmet (unpinned=3, 0/3) → landing met (mismatch=0 unpinned=0 targets_ok=3/3 hole_guard=pass, live all time-churn, rc=0), controls CONTROLS_DONE unexpected=0.
