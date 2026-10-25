source: S230 — Python 3.13 Language Reference §7.2, Assignment statements, https://docs.python.org/3.13/reference/simple_stmts.html#assignment-statements; S231 — Python 3.15.1 execution model §4.2.2, https://docs.python.org/3.15/reference/executionmodel.html#naming-and-binding
verified-at: 2026-10-24
recheck: inspect `.ufo/waves/round-41/conform.py` binding collector and run `python3 .ufo/waves/round-41/fixtures/run-r41-controls.py after <measured-tip> --output .ufo/waves/round-41/evidence/control-after.txt`

# Timeout binding inventory for the static conformance check

A timeout fold that searches only `Assign` nodes with one `ast.Name` target can miss local bindings that affect the read site. S230 §7.2 grounds tuple/list target unpacking; S231 §4.2.2 grounds block-local name resolution. The r41 checker uses a deliberately bounded inventory:

| Binding form | Static treatment |
|---|---|
| `Assign` / `AnnAssign` to a name | Resolve scalar values; recursively map a tuple/list RHS to matching tuple/list targets. Mismatched shapes fail closed. |
| `NamedExpr` | Record its target/value in source order. |
| tuple/list destructuring | Map each name target to its corresponding literal element; starred or unresolved unpacking fails closed. |
| `for` / `async for` target | Fail closed; the iterable and whether the body runs are not inferred. |
| `with` / `async with` target | Fail closed; the bound context-manager value is not inferred. |
| multiple function-local bindings | Sort by `(lineno, col_offset)`; accept only when every binding resolves to the same finite-positive value, otherwise fail closed. |
| unsupported local stores, function-level `global` rebinding, or `nonlocal` reads | Fail closed rather than falling through to a module constant. |

This is a conservative static subset, not a complete Python control-flow/dominance proof. It does not claim to prove arbitrary caller-supplied parameter values or every dynamic binding mechanism. The targeted r40 survivor fixtures and the 14-arm selftest are the executable boundary; their exact outcomes are in the round-41 evidence receipt.