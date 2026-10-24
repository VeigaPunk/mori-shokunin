# r17-C1 freeze-order falsification

Axes evaluated: chronology/verdict, completeness of the frozen input set, and agreement with the outside ruling.

## Independent derivation

Register rule and claim: `.ufo/waves/round-18/frozen/c2-register.json:4-19` (`R`, `I`, `L`, absent, strict pre-build ordering, and co-commit definition).

Command:

```sh
git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-list --reverse --topo-order 24526ea9617cd020fee16c28fe4d4a2789dc28cb..dcb2eea26d8dff0485b1cd0a9402fa63af82cb99
```

Exit 0; output (`R`, in order):

```text
273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7
5c1dfb8d0530c74eb0e1630c2b522b735b486274
2be82940828424ef4a2d623173d7e603b8a18f93
fe9fa9083db998ead1554459d656568c4173f288
91940fa339e38006f8db5bd7d78bb6f037f4d016
dcb2eea26d8dff0485b1cd0a9402fa63af82cb99
```

For each listed commit, I ran the requested `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff-tree --no-commit-id --name-only -r <commit>`. The unrestricted inventories returned successfully; to avoid copying unrelated committed paths into this report, the following target-path projection records the relevant results. The projection command was `git diff-tree --no-commit-id --name-only -r <commit> -- .ufo/waves/round-17/fixtures/seat/expected.json .ufo/waves/round-17/contract.md tools/mori-seat-terminal.py tools/mori-round17-seat-regressions.py` (same repository `-C` as above), exit 0 for the chained calls:

| Commit in `R` | Matching changed paths |
|---|---|
| `273aa74` | `contract.md`, `fixtures/seat/expected.json`, `tools/mori-round17-seat-regressions.py`, `tools/mori-seat-terminal.py` |
| `5c1dfb8` | none |
| `2be8294` | `contract.md`, `fixtures/seat/expected.json`, `tools/mori-round17-seat-regressions.py`, `tools/mori-seat-terminal.py` |
| `fe9fa90` | none |
| `91940fa` | `tools/mori-seat-terminal.py` only |
| `dcb2eea` | none |

To check the broader fixture input tree without reproducing fixture filenames, I counted `git diff-tree --no-commit-id --name-only -r <commit> -- .ufo/waves/round-17/fixtures/seat/ | wc -l` in the same order. Exit 0; counts: `82, 0, 18, 0, 0, 0` (the changed-path counts include `expected.json`). Thus fixture-pack files, the expected table, and the gate/spec paths changed in the initial implementation commit and again in `2be8294`.

`git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-list --parents 24526ea9617cd020fee16c28fe4d4a2789dc28cb..dcb2eea26d8dff0485b1cd0a9402fa63af82cb99` exited 0 and showed each of these six commits with exactly one parent; there are no merges in `R` that complicate the `diff-tree` interpretation.

Existence probes (`git -C ... cat-file -e REV:path`): frozen `expected.json` is missing at base (git subcommand exit 128) and present at tip (exit 0); `tools/mori-seat-terminal.py` is likewise missing at base (128) and present at tip (0). Therefore the frozen path is not `absent` at tip; its base absence does not invoke the rule's `L=none` fallback because `L` is present.

Derivation:

- `I = 273aa74...`, position 1 of `R`: first commit touching `tools/mori-seat-terminal.py`.
- `L = 2be8294...`, position 3 of `R`: last commit touching the registered frozen table.
- `co_committed = true`: both `273aa74` and `2be8294` touch the registered frozen path and impl path.
- Since `L` is after `I` (not before it), verdict = **co-evolved**.
- The register's outside ruling is `co-evolved`; independent derivation agrees, so this row has **no outside-ruling disagreement**.

## Path-set assessment

The impl path is right: round-17 contract lines 32-36 name `tools/mori-seat-terminal.py` as the C1 tool. The registered frozen path is also the core oracle: contract lines 77-82 define `expected.json` as the expected case table.

[INFERENCE] The registered frozen set is minimal rather than a complete replay-input inventory. The same contract lines 79-86 also define the synthetic fixture-pack tree and a separate regression gate, `tools/mori-round17-seat-regressions.py`. For reproducible end-to-end regression evidence, the referenced fixture bytes (or binding hashes enforced by the gate) and the gate identity are relevant dependencies; the table alone does not name those files as paths. The broader pin evidence partly mitigates this: the round-17 spot-check at `corpus/lessons/round-17-verifier-spotcheck.md:110-130` reports 66 cases and 96 fixture pins, all 96 matching the files at tip, and its freeze qualification says the table/tool were co-committed in `273aa74` and changed together in `2be8294`. `FINAL-PINNED_INPUTS.json:2-3,6,22-27` is explicitly measured at `91940fa`; it records hashes for the expected table, tested tool, and regression gate, so it is useful final provenance, not evidence that those inputs were frozen before implementation.

If the intended register scope is only the oracle table versus the SUT, its frozen/impl pair is correct and sufficient for this chronology verdict. If the intended scope is the complete test contract, I would add the fixture inputs (or their independently checked hash manifest), and identify the gate and contract as measurement/spec dependencies. This is a completeness qualification, not a counterexample to the row's classification: including the fixture-pack tree, gate, or contract leaves the latest relevant touch at `2be8294` (the fixture subtree has 18 changed paths there; the gate and contract also change there). Hence the expanded defensible set still has `L` after `I`, remains **co-evolved**, and still agrees with the outside ruling. A different defensible expansion does not change either comparison.

## Verdict

**Agree with the register's r17-C1 verdict and outside ruling: co-evolved.** Qualify that its frozen path list captures the central expected table but does not enumerate the complete fixture/gate dependency set. That omission does not change this row's verdict or oracle agreement. No tooling was installed or updated for this investigation.