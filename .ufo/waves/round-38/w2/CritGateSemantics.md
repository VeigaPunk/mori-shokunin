# CritGateSemantics — P-C6 ancestry is not path-log order

## Scoped acceptance: FAIL

The requested semantics check fails: the scored gate can print `superseded_as_of=[S001]` even though the sole superseder's landing commit is **not a descendant** of S001's last immutable-cell edit. This is a reproducible implementation defect, not an overall round judgment.

Axes: **depth** (actual ancestry semantics), **calibration** (the printed predicate overstates what is measured), and **operability** (an irrelevant side-branch timestamp changes the classification without changing any registry snapshot or parent relationship).

Reviewed/executed source: `f725f3076972e6e70595b5ac8279be524a111ff8:tools/mori-sources-appendonly.py`, SHA-256 `9a6164e391479bcc9e50487f9eabbc95d4f25d57793f77575d33f8520fdb09fa`. The source was obtained with `git show` and executed unchanged, not replaced by a simulated gate.

## Contract and implementation evidence

- `.ufo/waves/round-38/contract.md:93-110`, particularly line 95, requires the landing commit to be a **descendant** of the last immutable-cell edit and otherwise requires `stale_supersede`. This block discloses no linear-history or no-merges bound. `tools/mori-sources-appendonly.py:28-33,76-84` repeats the ancestry claim; calling descendant “strictly later than” in the docstring does not establish a graph restriction.
- `tools/mori-sources-appendonly.py:220-221` obtains `git log --format=%H --reverse REV -- corpus/SOURCES.md`, without parent relationships.
- Lines `238-265` compare each visited snapshot with the previous **log record**, not its actual parent, and retain first-appearance **indices** for superseding rows.
- Lines `272-289` choose a superseder by maximum index and implement the decisive predicate as `landing > last_edit[cid]`. There is no ancestry test at this decision.
- The selftest generator builds only a list of successive snapshots (`380-395`); its timing cases (`437-444`) do not exercise a merge. The changed-back case (`431-433`) already recognizes that reverting an immutable edit remains a historical edit.

## Strongest counterexample: a parallel superseder falsely discharges a later edit

Fresh scratch repository: `/tmp/CritGateSemantics-8ewhn0zj/parallel-superseder-late`.

The fixture has exactly one superseder, no missing S001 snapshots, no duplicate ids, and no row deletions. All unspecified cells remain constant. S002's `teaches` is `supersedes S001 replacement`; S003 is an unrelated appended row.

| Ref | Parents | Commit date | Registry contents |
|---|---|---|---|
| B | none | 2026-02-01 | S001 anchor=`original` |
| C | B | 2026-02-02 | S001 anchor=`v1` |
| E | C | 2026-02-03 | S001 anchor=`v2` |
| F | E | 2026-02-04 | S001 anchor=`v1`; append S003 |
| S | C | 2026-02-05 | S001 anchor=`v1`; append S002 superseding S001 |
| M | F, S | 2026-02-06 | S001 anchor=`v1`; S002; S003 |

Graph, observed with `git -C /tmp/CritGateSemantics-8ewhn0zj/parallel-superseder-late log --graph --format='%h %s %cs' M`:

```text
*   31c082c M 2026-02-06
|\
| * de57944 S 2026-02-05
* | 3f6c9d4 F 2026-02-04
* | 4e14c4b E 2026-02-03
|/
* a9a4f89 C 2026-02-02
* 1866905 B 2026-02-01
```

F is the unique ancestry-latest immutable-cell edit of S001: it changes `v2` back to `v1`. S only appends S002. M retains exactly the same S001 cells as **both** parents, so no merge-parent convention can make M a new S001 edit here. These statements were checked with `git diff E F -- corpus/SOURCES.md`, `git diff C S -- corpus/SOURCES.md`, and both `git diff F M -- corpus/SOURCES.md` and `git diff S M -- corpus/SOURCES.md`: the merge diffs add only S002 and S003 respectively.

S002 first lands at S, not M. Its full commit is `de57944a6e1ce5a9d6988875d5450accf10d2adf`; F is `3f6c9d4c762240b786a8daedc4f5008a297e2bcc`. The implementation's own first-appearance rule records S as the landing (`:242-254`).

### Commands actually executed

```sh
git -C /tmp/CritGateSemantics-8ewhn0zj/parallel-superseder-late merge-base --is-ancestor F S
```

Observed: **exit 1**, no stdout. The reverse test, `merge-base --is-ancestor S F`, also exited 1. They are incomparable, not descendant/ancestor.

```sh
git -C /tmp/CritGateSemantics-8ewhn0zj/parallel-superseder-late log --reverse --format='%h %s %cs' M -- corpus/SOURCES.md
```

Observed order: `B C E F S M`. Thus the code records last edit index 3 and landing index 4 and mistakes `4 > 3` for ancestry.

```sh
git -C /home/vgpnk/Projects/shokunin/mori-shokunin show f725f3076972e6e70595b5ac8279be524a111ff8:tools/mori-sources-appendonly.py |
  python3 - M --repo /tmp/CritGateSemantics-8ewhn0zj/parallel-superseder-late --round-base C
```

Observed after the printed P-C6 predicate:

```text
changed S001 superseded_by=S002
appendonly_violations=1 ids=[S001] deleted=[] superseded=[S001] round_changed=[S001,S003]
supersede_timing superseded_as_of=[S001] stale_supersede=[]
```

Exit **1**, empty stderr: this is the gate's ordinary violation result, not a failed/dead invocation. P-C6 requires `superseded_as_of=[] stale_supersede=[S001]` because F is not an ancestor of S.

Adding only `--topo-order` is not a correction: the executed command `git -C /tmp/CritGateSemantics-8ewhn0zj/parallel-superseder-late log --topo-order --reverse --format='%h %s' M -- corpus/SOURCES.md` returned the same `B C E F S M` order. A topological linearization still orders incomparable commits.

## Timestamp-only control

The independently constructed `/tmp/CritGateSemantics-8ewhn0zj/parallel-superseder-early` has the same logical DAG, all the same registry snapshots, and the same B/C/E/F commits. Only S's author/committer date moves from February 5 to February 2; M's object id consequently changes. Its final tree is identical: `git rev-parse M^{tree}` returned `75a375e17f85db3698ed1c8d03f03b3c197bd3b0` in **both** repositories.

The same pinned-source pipeline, with `--repo /tmp/CritGateSemantics-8ewhn0zj/parallel-superseder-early`, was executed. The path-log order became `B C S E F M` and the gate printed:

```text
changed S001 superseded_by=S002
appendonly_violations=1 ids=[S001] deleted=[] superseded=[S001] round_changed=[S001,S002]
supersede_timing superseded_as_of=[] stale_supersede=[S001]
```

Exit **1**, empty stderr. Both ancestry tests still returned 1. This is timestamp sensitivity of a supposed ancestry predicate, not nondeterministic execution at one revision.

## Supporting inverse case: a valid descendant becomes stale

Also exercised, using the same unchanged pinned source, in `/tmp/CritGateSemantics-8ewhn0zj/unrelated-late`: B has the original S001; E edits S001; S descends from E and appends S002; U forks from B and only appends S003; M merges S and U, retaining S001/S002 from S and S003 from U. `merge-base --is-ancestor E S` returned **0**. `diff B U` and `diff S M` showed only the S003 addition. `git blame -l M -- corpus/SOURCES.md` attributed S001's row to E.

The gate's path order was `B E S U M`; it printed `superseded_as_of=[] stale_supersede=[S001]` (exit 1). The preceding-log comparison fabricates a reversion at U and a new edit at M. Moving only U's date earlier, in `/tmp/CritGateSemantics-8ewhn0zj/unrelated-early`, produced order `B U E S M` and `superseded_as_of=[S001] stale_supersede=[]` (exit 1). Consequently, adding a real ancestry check while leaving log-adjacent edit detection untouched does not fully repair the merge semantics.

## Smallest safe correction / contract boundary

This is fixable without changing P-C6's meaning: retain commit identities for actual row edit/introduction events, derive changes from real parent relationships rather than adjacent traversal records, and require a **strict** ancestry relation between the relevant edit and superseder landing. Preserve changed-back edits such as F. Incomparable relevant edits/superseder landings must not acquire “latest” status merely from their dates or traversal indices. Add the primary diamond and its timestamp-only control as regression cases; retain the inverse case to catch phantom edits.

Merely sorting the log, renaming index order to “descendant,” or silently assuming a linear registry history is not a safe correction to the frozen predicate. An explicitly narrower supported-history contract would be a tradeoff for the canonical judge, not satisfaction of the currently unbounded ancestry statement. Interpreting “landing” as first-parent merge M instead of first appearance S would likewise require an explicit, consistently implemented definition, not an after-the-fact reading of this result.

Scope: constructed counterexamples, not a claim that the current lane's S069 receipt itself fails. No canonical judge/runtime invoked; no lane implementation, fleet state, or configuration changed. Only this report was written in the lane; fixture Git object databases are under the private temporary root above. No tools installed or upgraded.

Report: .ufo/waves/round-38/w2/CritGateSemantics.md
