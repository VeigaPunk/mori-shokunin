# MutC2GlobalColmap — global-colmap mutation on the r41 dag-h arm

Seat: `L1-mori-r41-attempt2.MutC2GlobalColmap` (leaf, mutation probe only).
Claim attacked: C2 / P-C12 clause "Immutable cells and `teaches` use each
commit's own header map". Frozen contract:
`.ufo/waves/round-41/contract.md`.

## Mutant

Isolated gate copy: `/tmp/r41-mut-c2-globalcolmap/gate-mutant.py`
(copied from `tools/mori-sources-appendonly.py`, sha256
`75af8f6f…f76b`). One behavior substituted: every commit is read through a
single global header map (fixed at the first walked commit that carries a
header, falling back to the tip map) instead of its own header map. This is
the v3 defect class the dag-h arm exists to kill.

Exact diff (pristine -> mutant):

```diff
     pair_sets = []
+    global_colmap = None
     for commit in commits:
         ...
         rows, commit_colmap = parse_registry(text)
+        if global_colmap is None:
+            global_colmap = commit_colmap
         states.append(rows)
         colmaps.append(commit_colmap)
-        pair_sets.append(supersede_pairs(rows, commit_colmap))
+        pair_sets.append(supersede_pairs(rows, global_colmap))
+    global_colmap = global_colmap or tip_colmap
@@
-                external_pair_sets[parent] = supersede_pairs(rows, parent_colmap)
+                external_pair_sets[parent] = supersede_pairs(rows, global_colmap)
@@
-        commit_colmap = colmaps[index] or tip_colmap
+        commit_colmap = global_colmap
@@
-        ref_colmap = ref_colmap or tip_colmap
+        ref_colmap = global_colmap
@@
-    tip_imm_idx = immutable_indices(tip_colmap)
+    tip_imm_idx = immutable_indices(global_colmap)
```

Hashes: pristine `75af8f6fc63dc736f07c02617bed4bf6c1ad7f880ffb49849b065b4d40d8f76b`;
mutant `b101c73630c1d9d1f3ad889628ffecb07fbea8270452a73f1929861f3698d593`.

## Detector and baseline

Detector A (committed arm): the gate's own committed selftest arm
`per-commit header map prevents fabricated changes` (`r41-dag-h`), run via
`python3 gate.py --selftest` on the isolated copy.

```
$ python3 gate-pristine.py --selftest
MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0        exit 0
```

Baseline is green, so a red arm is attributable to the mutation.

Detector B (direct CLI): the r40 builder `build-dags-r40.py::build_dag_h`
fixture (`b0=5bdfc4ef…`, `m=5e1dcd3e…`), gate invoked as
`gate.py <m> --repo <fixture> --round-base <b0>`.

## Result — mutant is KILLED

Mutant copy, `--selftest`:

```
FAIL per-commit header map prevents fabricated changes: ids: want [] got ['S001', 'S002', 'S003', 'S008']; round_changed: want [] got ['S001', 'S002', 'S008']; superseded_as_of: want ['S001'] got []; stale_supersede: want [] got ['S001']; exit: want 0 got 1
FAIL per-commit teaches map retains permuted superseder: ids: want [] got ['S001', 'S008']; superseded: want ['S001'] got []; round_changed: want [] got ['S001', 'S008']; superseded_as_of: want ['S001'] got []; exit: want 0 got 1
MORI_SOURCES_APPENDONLY_SELFTEST pass=20 fail=2        exit 1
```

The committed dag-h arm goes red, exactly on the predicted predicate: the
permuted tip header is misread through the global map, fabricating immutable
changes (`ids`/`round_changed`) and flipping the timing verdict
(`superseded_as_of` -> `stale_supersede`). The adjacent `r41-dag-h2` arm is
red for the same defect class; that is extra signal, not a requirement.

Direct CLI on the r40 dag-h fixture corroborates:

```
PRISTINE exit=0
appendonly_violations=0 ids=[] deleted=[] superseded=[S001] round_changed=[]
supersede_timing superseded_as_of=[S001] stale_supersede=[]

MUTANT exit=1
changed S001 superseded_by=S002
changed S002 superseded_by=-
changed S003 superseded_by=-
changed S008 superseded_by=-
appendonly_violations=4 ids=[S001,S002,S003,S008] deleted=[] superseded=[S001] round_changed=[S001,S002,S008]
supersede_timing superseded_as_of=[] stale_supersede=[S001]
```

Verdict: **killed** — the committed detector distinguishes the per-commit
header map from a single global colmap on the dag-h shape.

## Restoration evidence

- Mutation applied only to `/tmp/r41-mut-c2-globalcolmap/gate-mutant.py`;
  the lane tool was never edited or copied over.
- Mutant copy restored byte-identically from the pristine copy:
  `cp gate-pristine.py gate-mutant.py; cmp` -> identical, both sha256
  `75af8f6fc63dc736f07c02617bed4bf6c1ad7f880ffb49849b065b4d40d8f76b`.
- Lane `tools/mori-sources-appendonly.py` sha256 before and after the probe:
  `75af8f6fc63dc736f07c02617bed4bf6c1ad7f880ffb49849b065b4d40d8f76b`
  (unchanged); `git status --porcelain -- tools/mori-sources-appendonly.py`
  prints nothing.
- Lane Git/jj index, `.ufo/state` and sibling repos untouched; the only lane
  write is this report.

Tooling: none installed or updated.
