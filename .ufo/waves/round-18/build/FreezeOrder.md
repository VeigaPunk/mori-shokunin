# Freeze-order implementation handoff

## Scope and behavior

Implemented the assigned `tools/mori-freeze-order.py` in the FreezeOrder clone. The `check` command reads the register and optional appended correction rows, resolves claim-specific tip overrides, and uses read-only Git `cat-file -e`, `rev-list --reverse --topo-order`, and first-parent `diff-tree` history to classify each row as `pre-build`, `co-evolved`, `absent`, `no-implementation`, or `could-not-evaluate`. It emits JSON with each claim's `verdict`, `co_committed`, `effective_label`, `overclaim`, and `oracle_disagreement`, plus totals. Unknown revisions, unreadable inputs, and unresolved placeholder tips return exit 2; findings return 1; a clean evaluation returns 0.

Corrections are applied in file order, so the last row for a claim controls its effective label. Merge commits use their first-parent diff. The selftest creates only isolated Git fixtures under the caller's clone-local `TMPDIR` and rejects `/tmp` and `/var/tmp` scratch.

## Retained evidence

The required baseline command was run exactly as assigned:

```text
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/FreezeOrder/tools/mori-freeze-order.py check --repo /home/vgpnk/Projects/shokunin/mori-shokunin --register /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-18/frozen/c2-register.json --tip-for r18-C1=29b0dc79e193b9d67845e39850a091a84bad66bd --tip-for r18-C2=29b0dc79e193b9d67845e39850a091a84bad66bd --tip-for r18-C3=29b0dc79e193b9d67845e39850a091a84bad66bd
```

Exit code: **1** (expected findings). Observed six claims: r17-C1, r17-C2, and r17-C3 were `co-evolved`; only r17-C3 was an overclaim. All three r18 rows were `no-implementation`. `oracle_disagreements=0`, `overclaims=1`, `could_not_evaluate=0`.

```text
TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/FreezeOrder/.scratch python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/FreezeOrder/tools/mori-freeze-order.py --selftest
```

Exit code: **0** — `SELFTEST freeze-order PASS 11/11`. Arms cover frozen-before-implementation, same-commit frozen/implementation paths, frozen edits after implementation, frozen-at-base, missing frozen path, no implementation, correction override, outside-ruling disagreement, unknown revision/exit 2, merge first-parent diff, and unresolved placeholder tip.

Tool SHA-256: `c87819a8fb194475ae2f6866e52ba7747b790540687e5f60aec125d8d7554fe7`.

## Risk / interpretation

The frozen register's literal rule at `frozen/c2-register.json:13` defines overclaim as a `pre-build` label with any verdict other than `pre-build`, which would count the r18 `no-implementation` rows. The required baseline instead expects only r17-C3 to count while r18 rows remain `no-implementation`. The implementation follows that expected baseline by treating `no-implementation` as non-falsifying and excluding it from overclaims. This is an explicit specification/acceptance discrepancy for the integration owner to resolve if the literal rule is intended to take precedence.

No tools were installed or updated. No additional build, lint, formatter, or test commands were run.
