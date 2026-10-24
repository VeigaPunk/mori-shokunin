# Mutant C9-index-order — gate timing reverted to walk index

## Mutant

Single-axis mutation of the v2 gate at scored tip `13bfba23b7ca063c76d3504a2ff6eb7b6a294932`
(`tools/mori-sources-appendonly.py`, 818 lines), applied only to a scratch copy
`.ufo/waves/round-39/scratch/MutC9IndexOrder/gate-mutant.py`:

- `analyze()`'s `last_edit` map stores the walk index instead of the edit commit hash
  (line 347: `last_edit[cid] = commits[index]` → `last_edit[cid] = index`).
- The supersede-as-of decision reverts from `git merge-base --is-ancestor`
  to the round-38 walk-order comparison: `landing_index > edit_index`
  (replaces `is_ancestor(repo, edit_commit, commits[landing_index])`, lines 352–354).

Change detection (first-parent vs walk record), `--full-history`, `round_changed`,
and all other behavior are untouched. Diff (also at
`scratch/MutC9IndexOrder/mutant.diff`, 8 changed lines):

```diff
-            last_edit[cid] = commits[index]
+            last_edit[cid] = index
...
-        edit_commit = last_edit.get(cid)
-        if edit_commit is not None and is_ancestor(
-                repo, edit_commit, commits[landing_index]):
+        edit_index = last_edit.get(cid)
+        if edit_index is not None and landing_index > edit_index:
```

## Expected detector

`python3 <gate> --selftest` → `MORI_SOURCES_APPENDONLY_SELFTEST pass=12 fail=0`, exit 0 on
pristine bytes. The ticket predicted the mutant would yield `pass=11 fail=1` naming fixture D
(`landing is the last edit commit`, dag-d), where v2's ancestry test says `superseded_as_of=[S001]`
but index order says stale because the supersede row rides the same commit as the id's last edit.

## Actual outputs

Baseline, pristine bytes copied verbatim from the scored tip blob
(`sha256 62cd4132…`), command
`python3 .ufo/waves/round-39/scratch/MutC9IndexOrder/gate-pristine.py --selftest`:

```
MORI_SOURCES_APPENDONLY_SELFTEST pass=12 fail=0
BASELINE_EXIT=0
```

Mutant, command `python3 .ufo/waves/round-39/scratch/MutC9IndexOrder/gate-mutant.py --selftest`
(full output; 12 cases = 9 linear + 3 DAG fixtures):

```
FAIL side-branch superseder is stale: superseded_as_of: want [] got ['S001']; stale_supersede: want ['S001'] got []
FAIL landing is the last edit commit: superseded_as_of: want ['S001'] got []; stale_supersede: want [] got ['S001']
MORI_SOURCES_APPENDONLY_SELFTEST pass=10 fail=2
MUTANT_EXIT=1
```

Fixture D fails exactly as predicted: v2 expects `superseded_as_of=['S001'] stale_supersede=[]`,
the mutant prints the opposite. A second fixture also dies: dag-a (`side-branch superseder is
stale`) is misclassified as-of, because walk index order cannot tell a side-branch landing
(index after the edit) from an ancestor landing — the edit at `e1` precedes the row landing at
`s1` in walk order yet `e1` is not an ancestor of `s1`. That is 1 failure more than the ticket
predicted (`pass=10 fail=2`, i.e. "or worse"), not fewer. The 9 linear cases and dag-c
(`merge does not fabricate an edit`, including `round_changed=[]`) still pass, so the kill is
confined to the mutated timing predicate, not collateral breakage.

## Verdict

**KILLED.** The forbidden index-order timing behavior is observed by the bounded detector as
`FAIL landing is the last edit commit` (fixture D) plus `FAIL side-branch superseder is stale`
(fixture A), `pass=10 fail=2`, exit 1. Expected detector failure is genuine: the mutant runs,
executes all 12 cases, and only the two ancestry-discriminating fixtures differ. Acceptance
("pass=11 fail=1 or worse, naming fixture D"): **PASS** on the actual shape `pass=10 fail=2`,
with fixture D named. The predictive detail "11/1" is under-counted by one; recorded as a
finding, not a contract change.

## Restoration evidence

| Stage | File | sha256 |
|---|---|---|
| pristine | `scratch/MutC9IndexOrder/gate-pristine.py` | `62cd4132dbe141538371f79723c3caff66670fab9076494cd9cf65efccfc01e7` |
| mutated | `scratch/MutC9IndexOrder/gate-mutant.py` (before restore) | `1ae8f20e3ea5414a6dd4d0573acd17492fe37bd669c4b807a793f93c7e9d38e1` |
| restored | `scratch/MutC9IndexOrder/gate-mutant.py` (after `cp gate-pristine.py gate-mutant.py`) | `62cd4132dbe141538371f79723c3caff66670fab9076494cd9cf65efccfc01e7` |

Post-restore check: `cmp gate-pristine.py gate-mutant.py` → `CMP=identical`; rerun of the same
detector on the restored bytes → `MORI_SOURCES_APPENDONLY_SELFTEST pass=12 fail=0`,
`RESTORED_EXIT=0`. `sha256sum tools/mori-sources-appendonly.py` in the lane equals the scored-tip
blob hash `62cd4132…`; `git status --porcelain` reports only the untracked scratch directory —
the lane's real gate bytes were never modified and no lane file was written.

## Scope and artifacts

Only file written: `.ufo/waves/round-39/w1/MutC9IndexOrder.md` (this report). Scratch artifacts,
all under `.ufo/waves/round-39/scratch/MutC9IndexOrder/`: `gate-pristine.py`, `gate-mutant.py`
(restored), `mutant.diff`, `selftest-baseline.txt`, `selftest-mutant.txt`. No `git add/commit/push/fetch/reset/stash`,
no jj mutation, no installs (nothing needed), no sibling or fleet files touched.
