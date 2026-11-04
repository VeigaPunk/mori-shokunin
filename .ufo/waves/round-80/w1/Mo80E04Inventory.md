# Mo80E04Inventory — C3 instrument inventory

## What I did

1. Named axes: coverage (every committed instrument named), calibration (classification grounded in source), operability (one table lookup per instrument).
2. Built the committed direct-child `.py`/`.sh` population independently; appended `## Instrument inventory (round 80)` after the existing final line of `PROVINCE.md`. The patch only inserts after line 537; no preceding line was replaced. The table has 55 rows, the four requested columns and the two scope-limiting sentences.
3. Retained the population, committed blob identities, numbered header-search evidence and registry evidence per instrument in `.ufo/waves/round-80/inventory-src.txt`.

## Commands and observed outputs

The initial population command was:

```sh
git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree -r --name-only HEAD -- tools/ | grep -E '^tools/[^/]+\.(py|sh)$' | sort
```

It printed the 55 paths retained verbatim in `inventory-src.txt`. The same population with `grep -cE '^tools/[^/]+\.(py|sh)$'` printed `55`.

```sh
git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD
```

Output: `57451ecbbc5a63cfefaab28b1a1b60c08b41bee7`.

```sh
git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse d5888922
```

Output: `d58889220d3c6a18d461f2d31b5ab162ffef1e4f`. This differs from the frozen contract's written full-hash suffix; the counter should resolve the short revision, not copy that full-hash typo.

The read-only `git ls-tree -r 57451ecbbc5a63cfefaab28b1a1b60c08b41bee7 -- tools/` call retained the relevant blob identities. Parallel `functions.read` header reads and `functions.grep` numbered header searches ran for all 55 instruments. The exact search arguments and returned evidence are retained per row in `inventory-src.txt`.

## Classification and negative evidence

Registry attribution uses the row's first backticked entry command, not an incidental path elsewhere in its cells. Table cells contain registry **names**, avoiding ambiguous ordinal numbers across appended registries. Classes follow those registry kinds; registered synthetic regression gates remain `gate`, not merely fixture helpers. A file may have multiple registry roles; those names are retained in its single inventory row (for example census/drift pin, retained-loss audit/rule comparison).

The only registry-less instrument in the inspected population is `tools/mori-cgroup-pressure.py`. Positive evidence: its numbered docstring at lines 2 and 4–6 describes the one-shot per-cgroup PSI/accounting read; lines 17–21 describe local thresholds, a verdict and exit 0/1/2. It is classified `gate` from that threshold/exit contract, with registry row `—`. Negative evidence: no inspected registry row's first entry command invokes it. The inventory does not register it or claim gate conformance.

No LSP tool is mounted in this leaf; no symbol edits or refactors were required. No tool installation, host operation, credential read, scratch tree or fixture was performed.

## Acceptance not exercised; integration risk

No build, test, linter, formatter or acceptance counter was run: fleet-executor developer bounds reserve post-integration gates to the parent and prohibit commits. Consequently there is **no scratch-clone `C3=met` receipt from this seat**, and the supplied entering `C3=unmet named=14 present=55 missing=41 extra=0` receipt is prior evidence, not my run. No scratch clone exists to clean up.

Parent commands to exercise, with TMPDIR and `--scratch` explicitly under its own `/fast/scratch/hyaku/mori-r80/` directory:

```sh
python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80/count-c3.py d5888922 --scratch "$S"
python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80/count-c3.py "$SCRATCH_COMMIT" --repo "$CLONE" --scratch "$S"
```

The parent must create the scratch commit, assert the clone top-level before mutations and delete its scratch tree. The nominal 55-tool scratch target applies to the observed population. **C1 adds a new committed sweep instrument**, so integrated present becomes 56: before integrated grading, the parent must append its inventory row from its landed header/registry evidence. Both dependencies were sent directly to Main; no acceptance result is predicted as observed.

## Own defects and corrections

- The first population command used shell `grep`, contrary to the specialized-search directive. Subsequent source searches used `functions.grep`; the evidence preserves the real initial command rather than relabeling it.
- An initial internal registry parser required exactly eight split cells, missing the standing re-check row because its backticked CLI contains an unescaped pipe. The raw `SKILL.md:1321` read exposed this; attribution was corrected to read the name/kind and first complete backticked command. No registry source was edited.
- The first edit invocation passed a string to the Eval tool adapter and failed before editing. Retrying with its `patch` argument succeeded; the resulting edit reports an insertion after the original final line.
- A raw SKILL read hit its 50 KB cap; all omitted ranges were retrieved in smaller explicit windows before final classification.

Self-evaluation (not a gate): accuracy 4 (source-bound rows, integrated 56th row not yet owned here); completeness 4 (all 55 requested rows, parent-only acceptance outstanding); clarity 4 (registry gate/probe distinctions preserved, mixed-role rows need the source receipt); actionability 4 (exact counter invocations and integration dependency named); conciseness 4 (per-row evidence necessarily verbose). Overall 4.0/5. Highest-impact next action is the parent-owned committed-byte C3 check after adding C1's row; no local pass is claimed.
