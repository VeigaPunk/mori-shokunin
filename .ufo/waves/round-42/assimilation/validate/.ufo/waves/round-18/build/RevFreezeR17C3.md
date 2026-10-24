# Round 17 C3 freeze-order falsification

## Axes checked

- **Chronology:** first implementation-path touch versus last frozen-input touch.
- **Input coverage:** whether the register captures the actual C3 replay requirements.
- **Ruling stability:** whether defensible path-set corrections alter the verdict or outside-ruling comparison.

## Verdict

**Computed verdict: `co-evolved`; `co_committed: true`.** The declared `pre-build` label for `r17-C3` is an overclaim. The frozen register's outside ruling (`co-evolved`) agrees with the independently derived result. Under the register's rule, the strict invariant for `pre-build` is `L` preceding `I`; observed `L` is later than `I`.

## Commands and observed path outputs

All commands below were read-only against the lane repository. The commands completed successfully (rc 0). The `rev-list` output was:

```text
git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-list --reverse --topo-order 24526ea..dcb2eea
273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7
5c1dfb8d0530c74eb0e1630c2b522b735b486274
2be82940828424ef4a2d623173d7e603b8a18f93
fe9fa9083db998ead1554459d656568c4173f288
91940fa339e38006f8db5bd7d78bb6f037f4d016
dcb2eea26d8dff0485b1cd0a9402fa63af82cb99
```

For each listed commit I ran the requested full-path command:

```text
git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff-tree --no-commit-id --name-only -r <commit>
```

The full listings include many unrelated paths. The C3-relevant lines in those outputs were isolated with a read-only path-limited repeat over the register's frozen and impl paths plus `frozen/c3-tree`; its output by commit was:

```text
273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7
.ufo/waves/round-17/frozen/MoriR16.Lesson
tools/mori-misroot-sweep.py

5c1dfb8d0530c74eb0e1630c2b522b735b486274
(no paths in that selected set)

2be82940828424ef4a2d623173d7e603b8a18f93
.ufo/waves/round-17/c3-capture-recipe.json
.ufo/waves/round-17/frozen/c3-final-expected.json
.ufo/waves/round-17/frozen/c3-tree/MoriR16.Lesson
.ufo/waves/round-17/frozen/c3-tree/TabiR16.Lesson
.ufo/waves/round-17/frozen/c3-tree/TrackedMoriR16.Lesson
.ufo/waves/round-17/frozen/c3-tree/seed
tools/mori-misroot-sweep.py

fe9fa9083db998ead1554459d656568c4173f288
(no paths in that selected set)

91940fa339e38006f8db5bd7d78bb6f037f4d016
(no paths in that selected set)

dcb2eea26d8dff0485b1cd0a9402fa63af82cb99
(no paths in that selected set)
```

I also checked the historical oracle path across those commits with:

```text
for c in 273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7 5c1dfb8d0530c74eb0e1630c2b522b735b486274 2be82940828424ef4a2d623173d7e603b8a18f93 fe9fa9083db998ead1554459d656568c4173f288 91940fa339e38006f8db5bd7d78bb6f037f4d016 dcb2eea26d8dff0485b1cd0a9402fa63af82cb99; do
  printf '%s\n' "$c"
  git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff-tree --no-commit-id --name-only -r "$c" -- .ufo/waves/round-17/frozen/c3-expected.json
done
```

That output named `.ufo/waves/round-17/frozen/c3-expected.json` only under `5c1dfb8d0530c74eb0e1630c2b522b735b486274`; the other five commit entries had no matching path.

Applying `.ufo/waves/round-18/frozen/c2-register.json:4-13` to the register's row (`:24-29`):

- **I = `273aa74`** — first commit in the ordered range touching `tools/mori-misroot-sweep.py`.
- **L = `2be8294`** — last commit touching any of the row's frozen paths. It is after I.
- **co_committed = `true`** — `273aa74` touches both the witness and impl; `2be8294` also touches frozen inputs and impl.
- **verdict = `co-evolved`** — L is after I, not strictly before it.

## Path-set assessment

The row's implementation path is well-scoped: the round-17 contract identifies `tools/mori-misroot-sweep.py` as the C3 detector (`.ufo/waves/round-17/contract.md:21-27`), and the replay recipe invokes that path for both before and after (`.ufo/waves/round-17/c3-capture-recipe.json:32-54`). I found no evidence in these requirement inputs of another implementation path needed for this measurement.

The row's frozen set is **underinclusive** for the final replay, although its selected paths are relevant. In particular:

- The recipe says to copy **every file** from `frozen/c3-tree` and verify expected digests (`.ufo/waves/round-17/c3-capture-recipe.json:18-25`).
- The final expected record identifies the source hashes and tracked/untracked control roles (`.ufo/waves/round-17/frozen/c3-final-expected.json:4-29,54-57`).
- `FINAL-PINNED_INPUTS.json` pins the recipe, final expected record, and all four `c3-tree` files (`.ufo/waves/round-17/FINAL-PINNED_INPUTS.json:5-11`).

Thus a complete final-replay frozen path set should add:

```text
.ufo/waves/round-17/frozen/c3-tree/MoriR16.Lesson
.ufo/waves/round-17/frozen/c3-tree/TabiR16.Lesson
.ufo/waves/round-17/frozen/c3-tree/TrackedMoriR16.Lesson
.ufo/waves/round-17/frozen/c3-tree/seed
```

The register correctly includes the separate `.ufo/waves/round-17/frozen/MoriR16.Lesson` witness: the recipe names it as `fixture.source` and records its 847-byte digest (`c3-capture-recipe.json:27-30`). I do not reproduce that file's contents; it is cited only by path (`.ufo/waves/round-17/frozen/MoriR16.Lesson:1`) and by the hash/size metadata in the expected record (`c3-final-expected.json:17-20`).

The historical `.ufo/waves/round-17/frozen/c3-expected.json` is an earlier witness/sibling oracle (`:2-13`) changed at `5c1dfb8`, but it is superseded for the final replay: the recipe points to `c3-final-expected.json` (`c3-capture-recipe.json:77`) and the final pinned-input manifest includes the final record, not the earlier one. **[INFERENCE]** It is defensible to include this superseded oracle when auditing the entire requirement history, but not necessary in the active final-replay input set.

The requested “frozen/c3-capture-recipe.json” location is not present; the actual recipe is at `.ufo/waves/round-17/c3-capture-recipe.json`, which is the path in both the register and final pinned-input manifest (`:25`; `FINAL-PINNED_INPUTS.json:5`).

## Would the path correction change the comparison?

No. Adding the four omitted `c3-tree` paths leaves **L = `2be8294`**, because those fixture paths were touched there; I remains `273aa74`. Including the older `c3-expected.json` as historical scope also leaves the latest frozen touch at `2be8294`. Even a narrower but still relevant set containing only the separate byte-exact witness has L equal to I (`273aa74`), which is still `co-evolved`, not `pre-build`. These defensible alternatives therefore preserve `co_committed: true`, the `co-evolved` verdict, and agreement with the outside `co-evolved` ruling.

This matches the non-author spot-check's provenance: it records the real witness at `273aa74`, the initial miss/hit+sibling oracle at `5c1dfb8`, and the expanded exact controls plus tool revision co-committed at `2be8294`; it explicitly distinguishes useful final-patch evidence from blanket pre-build registration (`corpus/lessons/round-17-verifier-spotcheck.md:207-213`). Its routed calibration instruction says not to label the round pre-build (`:398-402`). The row's **computed** outside comparison is therefore sound; its **declared `pre-build`** label is not.

## Sources

- `.ufo/waves/round-18/frozen/c2-register.json:4-13,24-29`
- `.ufo/waves/round-17/contract.md:21-27,148-150`
- `.ufo/waves/round-17/c3-capture-recipe.json:18-30,32-77`
- `.ufo/waves/round-17/frozen/c3-final-expected.json:4-29,33-57`
- `.ufo/waves/round-17/frozen/c3-expected.json:2-13`
- `.ufo/waves/round-17/FINAL-PINNED_INPUTS.json:2-11,25-27`
- `corpus/lessons/round-17-verifier-spotcheck.md:176-213,398-402`
