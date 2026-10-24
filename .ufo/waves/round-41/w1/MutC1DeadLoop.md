# MutC1DeadLoop — restore unordered AST-walk binding selection

Mutation test on C1 `timeout_scope` under P-C10. Isolated copy only; no lane
source, fixture, Git index, jj state, `.ufo/state` or watchdog file was
modified. Findings live only in this report.

## Isolation

- Sandbox: `/tmp/mori-r41-mut-deadloop-2244225` (disposable).
  `git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/mori-shokunin`,
  then `git checkout --detach aa161e998eb22282e3d96ed2710bb0b39e5163de`
  (the measured after-tip; sandbox `HEAD == aa161e99…`).
- Checker under test: `.ufo/waves/round-41/conform.py` at that revision,
  copied byte-identically to `mut/conform-pristine.py` and `mut/conform-mutant.py`.
- No tools installed or updated; no pacman transaction attempted.

## Mutant

Restore the r40 selection defect: collect function-local bindings with the
unordered `ast.walk` order, drop the source-order sort, and select only the
last walk-order binding instead of requiring every source-ordered binding to
resolve to one finite-positive value.

Diff (pristine → mutant), 4 hunks:

```diff
 def _function_bindings(fn, name):
-    """Return source-ordered binding events for `name` in one function block."""
+    """Return AST-walk-ordered binding events for `name` in one function block."""
...
-    nodes = list(_function_scope_nodes(fn))
+    nodes = list(ast.walk(fn))
...
-    events.sort(key=lambda event: (event[0], event[1]))
...
     local_values = [] if (fn is None or is_global) else bindings
     if local_values:
-        values = []
-        for _, _, kind, expr in local_values:
-            if kind != "value":
-                raise Unresolvable("name %r has %s" % (name, kind))
-            values.append(_resolve_value(expr))
-        if all(value == values[0] for value in values[1:]):
-            return values[0]
-        raise Unresolvable("multiple bindings of %r do not resolve to one value" % name)
+        return _resolve_value(local_values[-1][3])
```

Target of the defect: `run()` in `survivor-deadloop-rebind.py` binds
`timeout = None` (line 110) then `timeout = GIT_TIMEOUT_S` inside
`for _dead_rebind in ():` (line 112). Walk-order last is the dead-loop body
value, so the dead loop regains its `timeout` binding and the survivor passes.

Hashes (sha256):

| bytes | sha256 |
|---|---|
| pristine / restored | `e1f2e11e7556cb4522c36cf22b3666650561e8eba0a7a7e85dc8c22c65475427` |
| mutant | `01cf0f66461b7798af35c3f2cf24a612c4bd78e36bc7ea5811d1ed7a9d247cbf` |

The lane and sandbox checker copies both hash `e1f2e11e…`; the mutant exists
only at `mut/conform-mutant.py`.

## Detector (identical on all three byte sets)

```
/usr/bin/python3 <checker> aa161e998eb22282e3d96ed2710bb0b39e5163de \
  --repo <sandbox>/repo \
  --contract <sandbox>/repo/.ufo/waves/round-39/contract.md \
  --counter <sandbox>/repo/.ufo/waves/round-41/fixtures/c1/survivor-deadloop-rebind.py
```

C1 frozen target for this counter: exit 1, `CONFORM=unmet`, with only
`timeout_scope` failing.

## Results

| bytes | exit | `check timeout_scope` | verdict line |
|---|---|---|---|
| pristine | 1 | `FAIL (survivor-deadloop-rebind.py: bounded=[] value=['line 116 (communicate): non-numeric constant'])` | `CONFORM=unmet` |
| mutant | 0 | `PASS (survivor-deadloop-rebind.py: bounded=[] value=[])` | `CONFORM=met` |
| restored | 1 | `FAIL (survivor-deadloop-rebind.py: bounded=[] value=['line 116 (communicate): non-numeric constant'])` | `CONFORM=unmet` |

In all three runs `predicate`, `head_pin`, `tool_resolve`, `bounded_reads`,
`drain_bind`, `timeout_state`, `scratch` and `selftest_conjunct` report PASS.

Baseline is conclusive: the pristine run fails closed exactly as recorded in
`evidence/control-after.txt` at this revision, so the mutant's `met` is caused
by the mutation, not by a broken baseline.

No-harm probe (extra): the mutant still reports `CONFORM=met` and `timeout_scope
PASS` on the honest counter `fixtures/c1/count-c8.py`, and still passes
`selftest_conjunct`. The mutation is therefore selective to the dead-loop class,
not a general checker breakage.

## Verdict

**Killed** by the C1 dead-loop survivor probe. The restored unordered selection
reproduces the r40 counterexample exactly (`CONFORM=met`, exit 0), which
contradicts the frozen `survivor_failures=3` target: the checker no longer fails
closed on the empty-loop rebinding. Restoration of the ordered implementation
returns `CONFORM=unmet`, so the kill is attributable to source-ordered
selection and not to any other difference in the copied bytes.

Coverage finding: this survivor is the only observed discriminator for the
ordering change. The in-process `selftest_conjunct` arm (early-continue) and the
honest counter both stay green under the mutation, so a future regression to
walk-order/last-binding selection would be visible only through the dead-loop
survivor. Recorded as an observation; the contract is unchanged.

## Restoration evidence

- `mut/conform-restored.py` is a copy of the pristine bytes:
  sha256 `e1f2e11e…`, identical to `mut/conform-pristine.py`,
  `<sandbox>/repo/.ufo/waves/round-41/conform.py` and the lane checker at
  `aa161e99…`.
- Restored bytes rerun: exit 1, `timeout_scope FAIL`, `CONFORM=unmet`.
- The mutant was never written inside the lane repo or a sibling repository;
  the lane's only write from this seat is this report.
