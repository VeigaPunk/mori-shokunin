# MutGateEligible — mutation probe: edit-bounded supersede eligible set

Seat: `MutGateEligible` (mutation-tester), round 40 wave 1, lane `mori-shokunin`.
Target instrument: `tools/mori-sources-appendonly.py` v3 (P-C11), working-tree bytes =
scored tip `265a955cc67be4eae97d2dc5a9338a25f31eb29b`
(`sha256 bde5a9a34c7eb3bcbee39d669b8d187caeb51807ad1bdcd85a05c1bcd06777ec`, verified equal to
`git show 265a955cc:tools/mori-sources-appendonly.py | sha256sum`).
Scratch copy only: `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/mutgate-eligible/gate-mutant.py`.
The lane instrument was never edited. All commands below ran with cwd
`/home/vgpnk/Projects/shokunin/mori-shokunin`.

## Axes

1. Selftest kill power of the P-C11 eligible-set extension (dag-n and dag-r arms).
2. Lane-line fidelity: does the mutant lose never-edited superseded ids at the tip?
3. Specificity: dag-p and the non-P-C11 dag arms (dag-a/c/d) must not be collateral damage.
4. Restoration byte identity.

## Mutant

Smallest behavior-bearing point, one token (`tip` → `ids`) at line 354:

```diff
--- tools/mori-sources-appendonly.py
+++ .scratch/mutgate-eligible/gate-mutant.py
@@ -351,7 +351,7 @@
     # P-C11: the timing line's eligible set is every superseded id present at
     # R, not only the edit-bounded `ids` list — a never-edited superseded id
     # still reaches the as-of/stale test (r39 w1 finding 2).
-    superseded = sorted(cid for cid in tip if cid in sup_map)
+    superseded = sorted(cid for cid in ids if cid in sup_map)
```

This restores exactly the round-39 edit-bounded set named in the tasking.
sha256 pristine `bde5a9a3…77ec` → mutant `21861098e772d0385b074944eeecb142967341cfb21bf1bb14647641042a01f9`.
(`diff -u tools/mori-sources-appendonly.py .scratch/mutgate-eligible/gate-mutant.py` exits 1 with only this hunk.)

## Detector

`python3 <gate> --selftest` (bounded, 15 arms) plus the committed DAG receipt runner
`run-c11-dags.py` for dag-n/dag-p/dag-r, plus the lane line at the tip.

### Baseline — pristine bytes (same detector, before mutation)

```
$ python3 .scratch/mutgate-eligible/gate-mutant.py --selftest
MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0
EXIT=0

$ python3 .ufo/waves/round-40/fixtures/run-c11-dags.py \
    /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/mutgate-eligible/gate-mutant.py \
    /home/vgpnk/Projects/shokunin/mori-shokunin \
    /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/mutgate-eligible/baseline-dags.txt \
    dag-n dag-p dag-r
== never-edited superseded row is as-of (dag-n, --round-base b0=07be6c7f1765)
appendonly_violations=0 ids=[] deleted=[] superseded=[S001] round_changed=[]
supersede_timing superseded_as_of=[S001] stale_supersede=[]
EXIT=0
== first-parent-lacks-path merge contributes no edits (dag-p, --round-base b0=07be6c7f1765)
appendonly_violations=1 ids=[S001] deleted=[] superseded=[S001] round_changed=[S001]
supersede_timing superseded_as_of=[S001] stale_supersede=[]
EXIT=1
== linear delete-then-re-add is not an edit (dag-r, --round-base b0=07be6c7f1765)
appendonly_violations=0 ids=[] deleted=[] superseded=[S008] round_changed=[S008]
supersede_timing superseded_as_of=[S008] stale_supersede=[]
EXIT=1
```

Baseline matches the landed receipts `c11-after-selftest.txt`, `c11-after-fixture-n.txt`,
`c11-after-fixture-p.txt`, `c11-after-fixture-r.txt` verdict lines exactly. Baseline is green,
so a mutant failure is attributable to the mutation.

### Mutant

```
$ python3 .scratch/mutgate-eligible/gate-mutant.py --selftest
FAIL never-edited superseded row is as-of: superseded: want ['S001'] got []; superseded_as_of: want ['S001'] got []
FAIL linear delete-then-re-add is not an edit: superseded: want ['S008'] got []; superseded_as_of: want ['S008'] got []
MORI_SOURCES_APPENDONLY_SELFTEST pass=13 fail=2
EXIT=1
```

Exactly the two required arms fail: **dag-n** and **dag-r**. All eleven other arms (including
dag-p, dag-a, dag-c, dag-d) still pass — the two pre-existing DAG corners are unaffected.

DAG receipts under the mutant (same runner, `mutant-dags.txt`):

```
== never-edited superseded row is as-of (dag-n, ...)
appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
supersede_timing superseded_as_of=[] stale_supersede=[]
EXIT=0                                      # as_of lost S001; matches c11-red-neveredited.txt shape
== first-parent-lacks-path merge contributes no edits (dag-p, ...)
appendonly_violations=1 ids=[S001] deleted=[] superseded=[S001] round_changed=[S001]
supersede_timing superseded_as_of=[S001] stale_supersede=[]
EXIT=1                                      # unchanged
== linear delete-then-re-add is not an edit (dag-r, ...)
appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[S008]
supersede_timing superseded_as_of=[] stale_supersede=[]
EXIT=1                                      # as_of lost S008
```

Lane line at the tip (`python3 .scratch/mutgate-eligible/gate-mutant.py
265a955cc67be4eae97d2dc5a9338a25f31eb29b --repo .`, `mutant-lane.txt`):

```
appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] round_changed=[]
supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] stale_supersede=[]
EXIT=1
```

Measured lane delta at the tip, versus `evidence/c11-after-lane.txt`:
as-of **35 → 18**, lost **17** never-edited ids, gained 0:
`S067,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140,S226`.
The superseded list in the summary line loses the same 17 ids. The mutant's timing line is
byte-identical to the round-39 receipt `evidence/c11-before-lane.txt`
(`diff` of the `supersede_timing` lines: empty) — the mutation re-creates the exact pre-P-C11
behavior on the real lane.

Lane line at `e37dcc6` (secondary arm, `mutant-e37.txt`): as-of **33 → 17**, lost the same 16
non-S226 ids, `stale_supersede=[S069]` **preserved**. So the e37dcc6 arm alone does not detect
this mutant; the tip line's id count and the two DAG arms do.

## Verdict

**KILLED.** The mutant survived nothing that matters: both mandated arms (dag-n, dag-r) fail in
the selftest, dag-p and the four round-39 DAG arms remain green, and the lane line demonstrably
loses never-edited superseded ids (17 at the tip, matching v2's 18-id line). The kill is specific:
`ids`-bounded ids still enter through `ids`, so edited superseded rows (`S069`, `S041`, …) never
move, which is why only never-edited rows vanish.

Coverage notes (not contract changes):
- Receipt `c11-after-lane.txt` contains **35** as-of ids at the tip, not 34 as stated in the
  wave tasking. Independent parse of the receipt line and the live run both give 35
  (`S041 … S226`); 18 (v2, before) + 17 never-edited additions = 35. The "34" figure is one short
  — a parser that slices between `=[` and `]` but drops the first token (`S041`) reproduces it.
  Flagged for the scorecard/erratum seats; the integrated lane receipt is self-consistent at 35.
- The contract's own `[19 ids incl. S226]` parenthetical is likewise a mis-prediction (already
  routed as the parenthetical-arithmetic erratum); the measured receipt value is 35.
- Arm sensitivity ordering observed: dag-n = dag-r (kill) > tip lane line (kill by count/list)
  > e37dcc6 stale arm (no kill).

## Restoration evidence

```
$ cp tools/mori-sources-appendonly.py .scratch/mutgate-eligible/gate-mutant.py
$ sha256sum tools/mori-sources-appendonly.py .scratch/mutgate-eligible/gate-mutant.py
bde5a9a34c7eb3bcbee39d669b8d187caeb51807ad1bdcd85a05c1bcd06777ec  tools/mori-sources-appendonly.py
bde5a9a34c7eb3bcbee39d669b8d187caeb51807ad1bdcd85a05c1bcd06777ec  .scratch/mutgate-eligible/gate-mutant.py
$ cmp tools/mori-sources-appendonly.py .scratch/mutgate-eligible/gate-mutant.py && echo CMP=identical
CMP=identical
```

Restored bytes re-run:
- `python3 .scratch/mutgate-eligible/gate-mutant.py --selftest` → `pass=15 fail=0`, EXIT=0.
- DAG runner on restored copy → verdict lines byte-identical to the baseline run
  (`diff` of `^==|^appendonly_violations|^supersede_timing|^EXIT` lines: `DAG_VERDICTS_IDENTICAL`).
- Lane line at the tip on restored copy → `appendonly_violations|supersede_timing` lines identical
  to `evidence/c11-after-lane.txt` (`LANE_BODY_IDENTICAL`), as-of 35, stale empty.

The lane working tree file was never modified; only `.scratch/mutgate-eligible/` was written.

## Tooling

None installed or upgraded; no pacman, no network access used. Only system `python3`, `git` and
coreutils.

## Artifacts (scratch, disposable)

`.scratch/mutgate-eligible/`: `gate-mutant.py` (restored), `mutation.diff`,
`baseline-selftest.txt`, `baseline-dags.txt`, `mutant-selftest.txt`, `mutant-dags.txt`,
`mutant-lane.txt`, `mutant-e37.txt`, `restored-selftest.txt`, `restored-dags.txt`,
`restored-lane.txt`.
