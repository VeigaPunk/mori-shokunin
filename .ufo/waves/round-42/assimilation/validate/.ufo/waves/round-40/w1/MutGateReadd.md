# MutGateReadd — C2 mutation probe: v2 linear re-add branch in the v3 gate

Seat: mutation-tester, mori round 40 wave 1. All work under
`/home/vgpnk/Projects/shokunin/mori-shokunin`. No production file was modified; the mutant is a
scratch copy and the pristine gate was never written.

## Target and mutation

- Pristine v3 gate: `tools/mori-sources-appendonly.py`
- sha256 `bde5a9a34c7eb3bcbee39d669b8d187caeb51807ad1bdcd85a05c1bcd06777ec`
- Equal to the scored tip blob: `git show 265a955cc67be4eae97d2dc5a9338a25f31eb29b:tools/mori-sources-appendonly.py | sha256sum`
  printed `bde5a9a34c7eb3bcbee39d669b8d187caeb51807ad1bdcd85a05c1bcd06777ec  -`.
- v2 source of the transplanted branch: `.ufo/waves/round-40/fixtures/extracted/gate-v2-bb1f2457.py`
  (sha256 `62cd4132dbe141538371f79723c3caff66670fab9076494cd9cf65efccfc01e7`), lines 318 and 325-328.

Mutant copy: `.scratch/MutGateReadd/gate-v3-readd-mutant.py`
sha256 `ee729f774fe2851892845c08b57a321cfad5e47d503f90a9322cf68e18ebe930`.

Transplant (exactly the v2 `elif not is_merge` re-add branch, replacing the v3 "no re-add branch"
comment):

```text
@@ -323,6 +323,7 @@
+        is_merge = len(parents_of.get(commit, [])) > 1
@@ -330,10 +331,10 @@
-            # P-C11: no `elif not is_merge` re-add branch — a row whose first
-            # parent lacks it is an addition, not an edit; persistent drift
-            # still surfaces through the ids tip-vs-first-sighting comparison
-            # (r39 w1 finding 5a).
+            elif not is_merge:
+                # present again after an absence on a linear history: a re-add
+                # is a round event even when the cells match the first sighting
+                changed_at.setdefault(index, set()).add(cid)
```

`diff -u tools/mori-sources-appendonly.py .scratch/MutGateReadd/gate-v3-readd-mutant.py` exit 1
(expected: files differ); summary `1 file changed, 5 insertions(+), 4 deletions(-)`. Nothing else
in the 919-line file differs.

## Commands and exact outputs

Baseline (pristine bytes), run from the lane root:

```text
$ python3 tools/mori-sources-appendonly.py --selftest; echo EXIT=$?
MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0
EXIT=0
```

Mutated bytes:

```text
$ python3 .scratch/MutGateReadd/gate-v3-readd-mutant.py --selftest; echo EXIT=$?
FAIL linear delete-then-re-add is not an edit: superseded_as_of: want ['S008'] got []; stale_supersede: want [] got ['S008']
MORI_SOURCES_APPENDONLY_SELFTEST pass=14 fail=1
EXIT=1
```

Exactly one arm fails, and it is the dag-r arm. Its actual plate output, via the fixture runner
(the runner builds the DAGs with the lane gate's builders and executes the supplied script):

```text
$ python3 .ufo/waves/round-40/fixtures/run-c11-dags.py .scratch/MutGateReadd/gate-v3-readd-mutant.py . .scratch/MutGateReadd/dag-mutant.txt dag-n dag-p dag-r
== never-edited superseded row is as-of (dag-n, --round-base b0=07be6c7f1765)
appendonly_violations=0 ids=[] deleted=[] superseded=[S001] round_changed=[]
supersede_timing superseded_as_of=[S001] stale_supersede=[]
EXIT=0

== first-parent-lacks-path merge contributes no edits (dag-p, --round-base b0=07be6c7f1765)
changed S001 superseded_by=S002
appendonly_violations=1 ids=[S001] deleted=[] superseded=[S001] round_changed=[S001]
supersede_timing superseded_as_of=[S001] stale_supersede=[]
EXIT=1

== linear delete-then-re-add is not an edit (dag-r, --round-base b0=07be6c7f1765)
appendonly_violations=0 ids=[] deleted=[] superseded=[S008] round_changed=[S008]
supersede_timing superseded_as_of=[] stale_supersede=[S008]
EXIT=1
```

(The predicate line printed before each summary is elided here; the full receipt is
`.scratch/MutGateReadd/dag-mutant.txt`, runner exit 0.)

## Verdict

| Arm | Pristine selftest | Mutant selftest | Mutant plate output | Verdict |
|---|---|---|---|---|
| dag-n | PASS | PASS | `as_of=[S001] stale=[]`, EXIT=0 | survived (unchanged) |
| dag-p | PASS | PASS | `changed S001`, `as_of=[S001] stale=[]`, EXIT=1 | survived (unchanged) |
| dag-r | PASS | **FAIL** | `as_of=[] stale=[S008]`, EXIT=1 | **killed** |
| other 12 arms | PASS | PASS (summary 14 pass) | — | survived |

**Mutant killed, arm-specific.** The v2 re-add branch flags the linear delete-then-re-add commit
(`r2`) as S008's last edit, which lands after S009's supersede row (`s1`), so the tip test yields
`superseded_as_of=[] stale_supersede=[S008]`. Expected detector behavior was exactly
`stale=[S008]` on dag-r and no other arm failure. The SELFTEST FAIL line names both halves
(`superseded_as_of` and `stale_supersede`). dag-n and dag-p outputs are byte-identical to the
landed after-receipts `.ufo/waves/round-40/evidence/c11-after-fixture-n.txt` /
`c11-after-fixture-p.txt`; the mutant dag-r differs from
`.ufo/waves/round-40/evidence/c11-after-fixture-r.txt`
(`superseded_as_of=[S008] stale_supersede=[]`) in exactly the timing line. The mutant's
`round_changed=[S008]` is unchanged from the pristine receipt (it comes from the r1 deletion,
not the re-add), so the kill is attributable to the timing predicate, not to a changed set.

## Restoration evidence

The pristine instrument was never edited; "restoration" is a byte and behavior check after the
probe:

```text
$ sha256sum tools/mori-sources-appendonly.py
bde5a9a34c7eb3bcbee39d669b8d187caeb51807ad1bdcd85a05c1bcd06777ec  tools/mori-sources-appendonly.py
$ python3 tools/mori-sources-appendonly.py --selftest; echo RESTORED_EXIT=$?
MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0
RESTORED_EXIT=0
```

After-hash equals before-hash and equals the scored-tip blob hash; the pristine detector is green
again. The mutant copy remains only at `.scratch/MutGateReadd/gate-v3-readd-mutant.py`; the raw
dag receipt at `.scratch/MutGateReadd/dag-mutant.txt`. No repo file, lane jj state, Git index,
fleet path, or frozen evidence receipt was touched.

## Notes

- Scope: this probe only tests the dag-r arm and its two neighbors; it makes no judgement about
  C1/C2 as claims and does not integrate anything.
- Tools installed/updated: none. No pacman transaction attempted.
- The `Report:` path was not echoed in the dispatched prompt; report written to the wave spec's
  `reportDir` (`.ufo/waves/round-40/w1/`) under the seat name, matching the existing `Exe*.md`
  seat-report convention.
