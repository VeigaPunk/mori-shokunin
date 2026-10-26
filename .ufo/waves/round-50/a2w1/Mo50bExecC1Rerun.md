# Mo50bExecC1Rerun — C1 re-run at the landed data (round 50, wave a2w1)

Seat: leaf executor, assigned move: re-run the frozen C1 counter independently at
`487941b9395e89678af0053cc443cdb49cdee6e3` (landed data), `7197160b927f04db294c9553fb48fadcc7a3f4e3` (entering,
expect `mismatches=6`) and `9b8562a371dc916fdc0fc686619ea1e271a3e118` (salvaged attempt-1 tree), plus the counter
selftest, then confirm the six axis targets by hand from the fleet `MANIFEST.json` at
`e014499613f63f8a467821219b0296121119ca53` and from `SCORECARD.md` at the landed rev.

Scratch: `/fast/scratch/hyaku/mori-r50/Mo50bExecC1Rerun/` (removed at the end, see §7).
No tool installs, no pacman transaction, no writes outside this file. Host untouched; no host log read.

## 1. Counter runs — final lines and exit codes (verbatim)

All six runs invoked the committed counter at
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-50/count-c1.py` with `--scratch` inside my scratch dir
(the counter takes its own `git archive <rev>` there when a pin has to be executed; each run's tree was deleted by
the counter's own `finally`).

### 1a. Landed data — `487941b9395e89678af0053cc443cdb49cdee6e3`

```
$ export TMPDIR=/fast/scratch/hyaku/mori-r50/Mo50bExecC1Rerun/tmp
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-50/count-c1.py 487941b9395e89678af0053cc443cdb49cdee6e3 --scratch "$S/c1-landed"
item axis coverage expect=round_47_improved got=ok state=ok
item axis operability expect=round_47_improved got=ok state=ok
item axis depth expect=round_49_improved got=ok state=ok
item axis freshness expect=round_28_improved got=ok state=ok
item axis calibration expect=round_49_improved got=ok state=ok
item axis adjacency expect=round_19_improved got=ok state=ok
item pin python3_tools/mori-pin-check.py_--selftest expect=(114/114) got=PIN_CHECK_SELFTEST_pass=114_fail=0 state=ok
item pin python3_tools/mori-unlanded-check.py_--selftest expect=(17/17) got=UNLANDED_SELFTEST_pass=17_fail=0 state=ok
C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=487941b9395e89678af0053cc443cdb49cdee6e3
EXIT=0
```

Wall time 6.99 s. This reproduces the landed line quoted in the ticket
(`C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0`) and the target row of the contract
(`C1=met … items=8 axes=6 pins>=2 boxes>=4 mismatches=0 errors=0 hidden=0`).

### 1b. Entering tip — `7197160b927f04db294c9553fb48fadcc7a3f4e3` (expect `mismatches=6`)

```
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-50/count-c1.py 7197160b927f04db294c9553fb48fadcc7a3f4e3 --scratch "$S/c1-entering"
item axis coverage expect=round_47_improved got=round=26,evidence_missing:corpus/lessons/round-47-verifier-spotcheck.md state=mismatch
item axis operability expect=round_47_improved got=round=31,evidence_missing:corpus/lessons/round-47-verifier-spotcheck.md state=mismatch
item axis depth expect=round_49_improved got=round=31,evidence_missing:corpus/lessons/round-49-verifier-spotcheck.md state=mismatch
item axis freshness expect=round_28_improved got=ok state=ok
item axis calibration expect=round_49_improved got=round=25,evidence_missing:corpus/lessons/round-49-verifier-spotcheck.md state=mismatch
item axis adjacency expect=round_19_improved got=ok state=ok
item pin python3_tools/mori-pin-check.py_--selftest expect=(60/60) got=PIN_CHECK_SELFTEST_pass=114_fail=0 state=mismatch
item pin python3_tools/mori-unlanded-check.py_--selftest expect=(13/13) got=UNLANDED_SELFTEST_pass=17_fail=0 state=mismatch
C1=unmet items=8 axes=6 pins=2 boxes=4 mismatches=6 errors=0 hidden=0 manifest=a94551c5bc8d rev=7197160b927f04db294c9553fb48fadcc7a3f4e3 failed=mismatch
EXIT=1
```

Wall time 7.21 s. `mismatches=6` exactly as the contract's before row and `evidence/control-c1-do-nothing.txt` state
(coverage 26 vs 47, operability 31 vs 47, depth 31 vs 49, calibration 25 vs 49, pins 60/60 vs 114/114 and 13/13 vs
17/17; freshness and adjacency already agreed).

### 1c. Salvaged attempt-1 tree — `9b8562a371dc916fdc0fc686619ea1e271a3e118`

```
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-50/count-c1.py 9b8562a371dc916fdc0fc686619ea1e271a3e118 --scratch "$S/c1-salvage"
item axis coverage expect=round_47_improved got=round=26,evidence_missing:corpus/lessons/round-47-verifier-spotcheck.md state=mismatch
item axis operability expect=round_47_improved got=round=31,evidence_missing:corpus/lessons/round-47-verifier-spotcheck.md state=mismatch
item axis depth expect=round_49_improved got=round=31,evidence_missing:corpus/lessons/round-49-verifier-spotcheck.md state=mismatch
item axis freshness expect=round_28_improved got=ok state=ok
item axis calibration expect=round_49_improved got=round=25,evidence_missing:corpus/lessons/round-49-verifier-spotcheck.md state=mismatch
item axis adjacency expect=round_19_improved got=ok state=ok
item pin python3_tools/mori-pin-check.py_--selftest expect=(60/60) got=PIN_CHECK_SELFTEST_pass=114_fail=0 state=mismatch
item pin python3_tools/mori-unlanded-check.py_--selftest expect=(13/13) got=UNLANDED_SELFTEST_pass=17_fail=0 state=mismatch
C1=unmet items=8 axes=6 pins=2 boxes=4 mismatches=6 errors=0 hidden=0 manifest=a94551c5bc8d rev=9b8562a371dc916fdc0fc686619ea1e271a3e118 failed=mismatch
EXIT=1
```

Wall time 7.21 s. Identical to the entering tip on the C1 surface: the salvaged working tree carried no C1 data change,
so the round-50 correction came entirely after it.

### 1d. Freeze commit of attempt 1 — `950e99be6757a52b00e9eb70ae1a1a7bbe2ea379` (extra, the receipts' stated archive rev)

```
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-50/count-c1.py 950e99be6757a52b00e9eb70ae1a1a7bbe2ea379 --scratch "$S/c1-freeze"
C1=unmet items=8 axes=6 pins=2 boxes=4 mismatches=6 errors=0 hidden=0 manifest=a94551c5bc8d rev=950e99be6757a52b00e9eb70ae1a1a7bbe2ea379 failed=mismatch
EXIT=1
```

### 1e. Re-run from an independent `git clone --shared` (repo-path independence)

One clone per seat, under my scratch; the counter was pointed at it with `--repo` and `--fleet-repo` so that the lane
repo and the fleet repo were resolved from different paths than in §1a–1d:

```
$ git clone --shared -q /home/vgpnk/Projects/shokunin/mori-shokunin "$S/clone"
$ git -C "$S/clone" rev-parse --show-toplevel
/fast/scratch/hyaku/mori-r50/Mo50bExecC1Rerun/clone
$ for r in 487941b… 7197160b… 9b8562a…; do python3 …/count-c1.py "$r" --repo "$S/clone" --fleet-repo /home/vgpnk/Projects/shokunin --scratch …; done
=== CLONE 487941b9395e89678af0053cc443cdb49cdee6e3
C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=487941b9395e89678af0053cc443cdb49cdee6e3
EXIT=0
=== CLONE 7197160b927f04db294c9553fb48fadcc7a3f4e3
C1=unmet items=8 axes=6 pins=2 boxes=4 mismatches=6 errors=0 hidden=0 manifest=a94551c5bc8d rev=7197160b927f04db294c9553fb48fadcc7a3f4e3 failed=mismatch
EXIT=1
=== CLONE 9b8562a371dc916fdc0fc686619ea1e271a3e118
C1=unmet items=8 axes=6 pins=2 boxes=4 mismatches=6 errors=0 hidden=0 manifest=a94551c5bc8d rev=9b8562a371dc916fdc0fc686619ea1e271a3e118 failed=mismatch
EXIT=1
```

All three lines byte-identical to §1a–1c (same `manifest=a94551c5bc8d` tag, same counts). The readings do not depend on
the lane repo's working directory.

### 1f. Counter selftest

```
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-50/count-c1.py --selftest
PASS targets_from_manifest
PASS honest_met
PASS rejected_round_ignored
PASS through_round_cutoff
PASS other_lane_ignored
PASS harmed_counts
PASS stale_round_unmet
PASS verdict_word_wrong_unmet
PASS evidence_pointer_missing_unmet
PASS absent_spotcheck_needs_manifest
PASS duplicate_axis_row_unmet
PASS missing_axis_row_unmet
PASS table_in_fence_unseen
PASS all_latest_junk_unmet
PASS first_round_token_decides
PASS stale_fraction_pin_unmet
PASS stale_token_pin_unmet
PASS prefix_mismatch_unmet
PASS pins_deleted_unmet
PASS box_deleted_unmet
PASS hidden_fraction_unmet
PASS hidden_token_unmet
PASS absolute_path_unbound
PASS extra_args_unbound
PASS other_interpreter_unbound
PASS missing_tool_unbound
PASS receipt_missing_unmet
PASS receipt_other_tally_unmet
PASS runner_error_counts
PASS failing_arm_mismatch
PASS honest_failing_pin_needs_receipt
PASS bound_path_ok
PASS bound_path_dotdot
PASS heading_renamed_unmet
C1_SELFTEST pass=34 fail=0
EXIT=0
```

34 arms, 34 pass. (This is the *C1 counter's* selftest; it is not one of SHONEN's two pins — those are the instrument
selftests below.)

## 2. Tallies re-measured on my own `git archive` (not the counter's tree)

Own extraction, so the two SHONEN tallies are confirmed from re-derived bytes rather than from the counter's scratch tree:

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ git archive 487941b9395e89678af0053cc443cdb49cdee6e3 | tar -x -C "$S/tree-landed"
archive rc=0
$ cd "$S/tree-landed" && export PYTHONDONTWRITEBYTECODE=1
$ python3 tools/mori-pin-check.py --selftest
… (114 PASS lines) …
PIN_CHECK_SELFTEST pass=114 fail=0
pin EXIT=0
$ python3 tools/mori-unlanded-check.py --selftest
PASS clean_tree_exit0  rc=0 UNLANDED=clean round=8
… (15 more PASS lines) …
UNLANDED_SELFTEST pass=17 fail=0
unlanded EXIT=0
```

Blob-vs-archive byte equality for everything the C1 surface reads:

```
tools/mori-pin-check.py        blob=697ab2cc6ca6702a archive=697ab2cc6ca6702a equal=True
tools/mori-unlanded-check.py   blob=612d50c1590d5a30 archive=612d50c1590d5a30 equal=True
SHONEN.md                      blob=9e6b89f655091160 archive=9e6b89f655091160 equal=True
SCORECARD.md                   blob=5a741651b3b62308 archive=5a741651b3b62308 equal=True
```

Instrument bytes are unchanged between the freeze commit and the landed tip, so the committed receipts were produced by
the same tool bytes the counter executes at R:

```
tools/mori-pin-check.py      freeze=697ab2cc6ca6702a landed=697ab2cc6ca6702a equal=yes
tools/mori-unlanded-check.py freeze=612d50c1590d5a30 landed=612d50c1590d5a30 equal=yes
```

Receipts at R (`.ufo/waves/round-50/evidence/selftests/`) end in exactly the tallies I observed, and both were added by
the landed commit (`git diff --stat 7197160b 487941b` → `mori-pin-check.txt | 117 +`, `mori-unlanded-check.txt | 20 +`):

```
PIN_CHECK_SELFTEST pass=114 fail=0
exit=0
UNLANDED_SELFTEST pass=17 fail=0
exit=0
```

SHONEN.md at R, independent scan (the two pins plus a residual-token scan with the pins blanked out):

```
pins found: 2 -> ['`python3 tools/mori-pin-check.py --selftest` (114/114)', '`python3 tools/mori-unlanded-check.py --selftest` (17/17)']
residual fraction tokens: []
residual pass= tokens: []
residual SELFTEST tokens: []
boxes: 4
Counter({'coverage': 1, 'operability': 1, 'depth': 1, 'freshness': 1, 'calibration': 1, 'adjacency': 1})
```

`114/114` == `pass=114 fail=0`, `17/17` == `pass=17 fail=0`; 4 boxes; `hidden=0` confirmed by hand.

## 3. Six axis targets derived by hand from the fleet MANIFEST (no counter code)

Independent implementation (own `json` load of `git -C /home/vgpnk/Projects/shokunin show e0144996…:MANIFEST.json`,
own filter and own `max`; no counter code imported or executed), pasted exactly as run:

```python
import json, subprocess
FLEET="/home/vgpnk/Projects/shokunin"
MAN="e014499613f63f8a467821219b0296121119ca53"
raw = subprocess.run(["git","-C",FLEET,"show",MAN+":MANIFEST.json"],capture_output=True,check=True).stdout
d = json.loads(raw)
AXES=["coverage","operability","depth","freshness","calibration","adjacency"]
rs=[r for r in d["rounds"] if r.get("lane")=="mori"]
print("total mori closure rows:", len(rs))
print("rounds present:", sorted({r["lane_round"] for r in rs}))
best={}
for r in rs:
    n=r["lane_round"]
    if n>49: continue
    admitted = (r.get("verdict")=="admitted") and r.get("admitted") is True
    for a in AXES:
        g=r.get("verdicts",{}).get(a)
        if admitted and g in ("improved","harmed"):
            if a not in best or n>best[a][0]:
                best[a]=(n,g)
print("derived N* per axis:")
for a in AXES: print("  %-12s %s" % (a, best.get(a)))
odd=[(r["lane_round"],r.get("verdict"),r.get("admitted")) for r in rs if (r.get("verdict")=="admitted") != (r.get("admitted") is True)]
print("rows with admitted flag/verdict disagreement:", odd)
print("\nlast mori closures:")
for r in sorted(rs,key=lambda x:x["lane_round"])[-8:]:
    print(" r%-3d %-14s %s" % (r["lane_round"], r.get("verdict"), json.dumps(r.get("verdicts"),sort_keys=True)))
```

Output:

```
total mori closure rows: 38
rounds present: [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49]
derived N* per axis:
  coverage     (47, 'improved')
  operability  (47, 'improved')
  depth        (49, 'improved')
  freshness    (28, 'improved')
  calibration  (49, 'improved')
  adjacency    (19, 'improved')
rows with admitted flag/verdict disagreement: []
```

Supporting rows (same run, verbatim):

```
last mori closures:
 r42  rejected-honest-stop {"adjacency": "unchanged", "calibration": "improved", "coverage": "unchanged", "depth": "improved", "freshness": "unchanged", "operability": "unprovable"}
 r43  admitted       {"adjacency": "unchanged", "calibration": "improved", "coverage": "unchanged", "depth": "unchanged", "freshness": "unchanged", "operability": "improved"}
 r44  admitted       {"adjacency": "unchanged", "calibration": "improved", "coverage": "unchanged", "depth": "improved", "freshness": "unchanged", "operability": "improved"}
 r45  rejected-harmed {"adjacency": "unchanged", "calibration": "harmed", "coverage": "unchanged", "depth": "improved", "freshness": "unchanged", "operability": "improved"}
 r46  admitted       {"adjacency": "unchanged", "calibration": "improved", "coverage": "unchanged", "depth": "unchanged", "freshness": "unchanged", "operability": "unchanged"}
 r47  admitted       {"adjacency": "unchanged", "calibration": "improved", "coverage": "improved", "depth": "improved", "freshness": "unchanged", "operability": "improved"}
 r48  admitted       {"adjacency": "unchanged", "calibration": "improved", "coverage": "unchanged", "depth": "improved", "freshness": "unchanged", "operability": "unchanged"}
 r49  admitted       {"adjacency": "unchanged", "calibration": "improved", "coverage": "unchanged", "depth": "improved", "freshness": "unchanged", "operability": "unchanged"}
```

This equals the six `expect=` values the counter printed in §1a, derived without importing or running the counter:
coverage 47 improved, operability 47 improved, depth 49 improved, freshness 28 improved, calibration 49 improved,
adjacency 19 improved.

### 3a. Sensitivity — is the "admitted" filter load-bearing?

```
admitted only {'coverage': (47, 'improved'), 'operability': (47, 'improved'), 'depth': (49, 'improved'), 'freshness': (28, 'improved'), 'calibration': (49, 'improved'), 'adjacency': (19, 'improved')}
any verdict (sensitivity) {'coverage': (47, 'improved'), 'operability': (47, 'improved'), 'depth': (49, 'improved'), 'freshness': (28, 'improved'), 'calibration': (49, 'improved'), 'adjacency': (19, 'improved')}
max mori lane_round at pinned manifest: 49
```

Re-deriving with the `admitted` clause dropped yields the same six answers, so the target set is not an artefact of the
filter here. The only rejected row that grades these axes at all is r45 (`rejected-harmed`, calibration harmed,
operability improved) at round 45, below both winners. The `<=49` cutoff is likewise not load-bearing at this pinned
manifest (highest mori row is 49); it becomes load-bearing the moment a mori round-50 closure row lands in
`MANIFEST.json`, which is why the frozen counter must not be re-scored after that (contract: no re-scoring under a
changed counter).

## 4. Last change cells at the landed tip lead with N*

Own parse of `git -C … show 487941b…:SCORECARD.md`, `## Axes` table, column 4 (Last change), first `round N` token:

```
== coverage | cells=4
  LAST: round 47 (improved, score held); round 26 (improved, score held) before the round-50 correction
  first_round=47  n*=47  verdict_word_in_segment=True  segment='round 47 (improved, score held)'
  evidence cell contains spot file: True
== operability | cells=4
  LAST: round 47 (improved, score held); round 31 (improved, score held) before the round-50 correction; round-37 C2 re-attributed here (score held, 7)
  first_round=47  n*=47  verdict_word_in_segment=True  segment='round 47 (improved, score held)'
  evidence cell contains spot file: True
== depth | cells=4
  LAST: round 49 (improved, score held); round 31 (improved, score held) before the round-50 correction
  first_round=49  n*=49  verdict_word_in_segment=True  segment='round 49 (improved, score held)'
  evidence cell contains spot file: True
== freshness | cells=4
  LAST: round 28 (improved, score held); round-37 C2 is re-attributed to operability (round-38 axes-cell correction below) and round 38 claims no freshness move
  first_round=28  n*=28  verdict_word_in_segment=True  segment='round 28 (improved, score held)'
  evidence cell contains spot file: True
== calibration | cells=4
  LAST: round 49 (improved, score held); round 25 (improved, score held) before the round-50 correction; round-37 claim C1 closed the r36 measurement-discrimination defect and states no new number
  first_round=49  n*=49  verdict_word_in_segment=True  segment='round 49 (improved, score held)'
  evidence cell contains spot file: True
== adjacency | cells=4
  LAST: round 19 (improved, score held)
  first_round=19  n*=19  verdict_word_in_segment=True  segment='round 19 (improved, score held)'
  evidence cell contains spot file: False
```

Six axes, one row each, four cells each; every Last change cell's first round token is N* and the verdict word inside
that clause is the MANIFEST word. The adjacency `False` is the correct branch, not a defect: the N* spot-check file does
not exist at R, so the cell must name `MANIFEST.json`, and it does.

```
$ git cat-file -e 487941b…:corpus/lessons/round-19-verifier-spotcheck.md   → rc 128 (absent)
round-19 ABSENT
round-28 EXISTS
round-47 EXISTS
round-49 EXISTS
adjacency EV contains 'MANIFEST.json': True
```

### 4a. Evidence pointers spot-checked against the lines they cite

The four corrected cells appended a pointer to the closing spot-check file and line; all four resolve to the claimed
grade (Calibration is exactly "self-assessment matches observed state", so a wrong line number would matter):

```
--- corpus/lessons/round-47-verifier-spotcheck.md:67
| operability | improved | new reconciler `tools/mori-pin-check.py` with a registered 34-arm selftest (evidence-verified, not executed) |
--- corpus/lessons/round-47-verifier-spotcheck.md:68
| coverage | improved | FR13 held as a full event set plus lifecycle; README block added; previously only abstract-level S262 and queued S005 |
--- corpus/lessons/round-49-verifier-spotcheck.md:75
| calibration | 5 | improved | C1 verified; no score change claimed |
--- corpus/lessons/round-49-verifier-spotcheck.md:76
| depth | 5 | improved | C2 re-measured 21/21 |
```

The adjacency pointer `MANIFEST.json@63729047 … rounds[398]` also resolves, at the abbreviation `63729047` (a fleet
revision, per the round-29 convention) and at the pinned `e0144996`:

```
63729047644f len=479  mori19 index: [398] adjacency: improved
e014499613f6 len=750  mori19 index: [398] adjacency: improved
rounds[398] = {"lane":"mori","lane_round":19,"verdict":"admitted", …}
```

### 4b. What the landed commit actually changed on the C1 surface

```
 .../round-50/evidence/selftests/mori-pin-check.txt | 117 +++++++++++++++++++++
 .../evidence/selftests/mori-unlanded-check.txt     |  20 ++++
 SCORECARD.md                                       |  14 ++-
 SHONEN.md                                          |   2 +-
 4 files changed, 148 insertions(+), 5 deletions(-)
```

`git diff -U0 7197160b 487941b -- SCORECARD.md` is 16 changed lines: the four stale rows (coverage, operability,
depth, calibration; freshness and adjacency untouched because they already agreed) plus the six-line
"Round-50 correction (C1, calibration)" paragraph. SHONEN gains exactly one line: `(60/60)` → `(114/114)`,
`(13/13)` → `(17/17)`, plus the two receipt paths. No score cell changed; no other axis text changed. That is the
minimal edit the target needs and nothing beyond it.

## 5. Verdict per frozen predicate

P-C1 at R = `487941b9395e89678af0053cc443cdb49cdee6e3`: counter exit 0 with
`C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0`, reproduced from a fresh archive, from an
independent clone, and by hand for the six axis targets and the two tallies. Entering tip and the salvaged tree both
give `mismatches=6`; the freeze commit also gives `mismatches=6`. The before/after pair in the contract is real work,
not a counter artefact.

## 6. Named limits of this re-run (not defects, per the frozen contract)

1. I verified that the MANIFEST rows exist with the stated verdicts; I did not re-judge whether the closures were
   rightly admitted (the counter trusts the fleet manifest; so did I).
2. A matching tally proves the instrument prints `pass=114`/`pass=17` at R; it does not prove the arms are good.
3. The predicate checks the Last change convention the table already uses; I did not evaluate whether that convention
   is the best one.
4. `hidden=0` covers `SHONEN.md` only. Tally-like tokens elsewhere (report drafts, LOG.md, lessons) were not enumerated.
5. I did not run the C1 controls (`controls/c1-controls.py`); they are another seat's surface and the receipts under
   `evidence/control-c1-*` were not re-scored.
6. C2 is out of my scope: I read no corpus entry and no source copy.
7. No host state was read for this claim (no cgroup, proc, journal or dmesg path touched), consistent with the lane's
   detection-only rule.

## 7. Scratch and housekeeping

- Scratch root `/fast/scratch/hyaku/mori-r50/Mo50bExecC1Rerun/` held: `tmp/` (TMPDIR for every counter run and both
  selftests), `c1-landed/ c1-entering/ c1-salvage/ c1-freeze/ c1-clone-*/` (counter trees, deleted by the counter's
  own `finally`), `tree-landed/` (my `git archive` extraction) and `clone/` (the single `--shared` clone). Removed with
  `rm -rf` after this report was written; nothing cited here lives only in scratch.
- No mutating git command was issued anywhere: `clone --shared`, `archive`, `show`, `cat-file -e`, `diff`, `rev-parse`,
  `ls-tree` only. No command touched `/home/vgpnk/Projects/shokuknow*`.
- No tool install and no pacman transaction was needed; disk guard was read first (`rc=0`, `/fast/scratch/hyaku` 24 %
  used, 615.2 G free) — no ENOSPC risk.

## Findings

1. **LOW (no defect, verified)** — `SCORECARD.md:11-14` (coverage, operability, depth, calibration Last change cells) at
   `487941b9395e89678af0053cc443cdb49cdee6e3`: each first `round N` token equals the hand-derived N* (47, 47, 49, 49)
   from `MANIFEST.json@e0144996`, each clause carries the MANIFEST verdict word, and `SHONEN.md:6` pins (114/114,
   17/17) equal the tallies I re-ran from a fresh `git archive`. C1 is met on independent re-measurement.
2. **LOW** — `SCORECARD.md:15` (adjacency Evidence cell): the pointer reads `MANIFEST.json@63729047 … rounds[398]`.
   The abbreviation is a fleet *revision*, not a MANIFEST digest (the pinned MANIFEST's own sha256 prefix is
   `a94551c5bc8d`), and the same cell also carries the string `verifier-spotcheck` from an unrelated round-14 history
   pointer. Both facts are accurate (`rounds[398]` is mori 19 with `adjacency: improved` at `63729047` and at
   `e0144996`), but a reader looking for "which file must this cell name" can be misled. No action required under the
   frozen predicate; worth a clarifying word if this cell is ever rewritten.
3. **LOW** — contract §C1 kill rule and the `THROUGH = 49` cutoff: the cutoff is not load-bearing at
   `MANIFEST.json@e0144996` (highest mori row is 49), but the fleet will add a mori round-50 closure. Once that row
   exists the frozen counter's target set can move under a later re-run, so any post-closure re-scoring must use
   `git show <freeze>:count-c1.py` bytes (as the contract already requires) rather than the working tree. Named limit,
   not a defect.
4. **LOW** — `9b8562a371dc916fdc0fc686619ea1e271a3e118` (salvaged attempt-1 tree) is on the C1 surface identical to the
   entering tip (`mismatches=6`, same six item lines). The salvage contributed nothing to C1; the correction landed
   wholly in `487941b93`. Recorded so the closure does not attribute C1 progress to the salvage commit.
5. **LOW** — receipts `.ufo/waves/round-50/evidence/selftests/mori-pin-check.txt` and `…/mori-unlanded-check.txt` state
   their archive rev as `950e99be6757a52b00e9eb70ae1a1a7bbe2ea379` (the freeze commit) while the counter executes at R;
   the two instrument blobs are byte-identical at both revs (`697ab2cc…`, `612d50c1…`), so the receipt is valid at R,
   but the header alone does not say so. Cosmetic only.
