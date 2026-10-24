# MutC1Walrus — delete the `NamedExpr` binding branch from C1 `timeout_scope`

Assignment: in a disposable sandbox, remove the `NamedExpr` binding branch of the
r41 checker and run the walrus survivor; report whether the C1 target turns red.
Read-only lane; the only lane write from this seat is this report.

## Isolation

- Sandbox `/tmp/mori-r41-mutwalrus-ofWSwTad` (disposable):
  `git clone -q --shared /home/vgpnk/Projects/shokunin/mori-shokunin repo`,
  then `git checkout -q --detach 7450722e5f3b4fc6df3d719386ed643af59630e3`
  (lane tip, the measured after-revision). Sandbox `HEAD == 7450722e…`.
- Checker under test: `.ufo/waves/round-41/conform.py` at that revision.
  Pristine bytes saved at `pristine-conform.py`; mutant at
  `conform-mut-namedexpr.py`.
- No lane source, fixture, Git index, jj state, `.ufo/state`, watchdog log or
  sibling repo was modified. Lane checker hash is unchanged before and after
  (`e1f2e11e…`). No tools installed or updated; no pacman transaction.

## Mutant

Delete the three-line `NamedExpr` arm in `_function_bindings` (pristine lines
301–303). Smallest behavior-bearing point: the branch is the only place a
walrus target is recorded as a `value` binding.

```diff
@@ -298,9 +298,6 @@
             for target_name in _name_targets(sub.target, name):
                 add(target_name, "value" if sub.value is not None else
                     "annotation-only binding", sub.value)
-        elif isinstance(sub, ast.NamedExpr):
-            if isinstance(sub.target, ast.Name) and sub.target.id == name:
-                add(sub.target, "value", sub.value)
         elif isinstance(sub, (ast.For, ast.AsyncFor)):
             for target_name in _name_targets(sub.target, name):
                 add(target_name, "loop target")
```

| bytes | sha256 | size |
|---|---|---|
| pristine / restored | `e1f2e11e7556cb4522c36cf22b3666650561e8eba0a7a7e85dc8c22c65475427` | 44139 |
| mutant | `630d43cb5409d2710209f65af7c9d89df1b3d1aa535a1f9ca4aa90d70544350d` | 43967 |

## Detector

```sh
/usr/bin/python3 <sandbox>/repo/.ufo/waves/round-41/conform.py \
  7450722e5f3b4fc6df3d719386ed643af59630e3 \
  --repo <sandbox>/repo \
  --contract <sandbox>/repo/.ufo/waves/round-39/contract.md \
  --counter <sandbox>/repo/.ufo/waves/round-41/fixtures/c1/survivor-walrus-none.py
```

Frozen expectation (C1 target): `EXIT=1`, `CONFORM=unmet`, exactly
`timeout_scope` FAIL and the other eight checks PASS. Same command, same
fixture, same sandbox for pristine, mutated and restored bytes.
Survivor bytes: `beb751f42f480d4305eeb9c3e07a70734516b1e8fa471e29066af912940e91bf`
(walrus `(timeout := None)` inserted at `run()` line 110).

## Observed

| bytes | exit | CONFORM | failing checks | `timeout_scope` detail |
|---|---|---|---|---|
| pristine | 1 | `unmet` | `[timeout_scope]` | `line 114 (communicate): non-numeric constant` |
| mutant | 1 | `unmet` | `[timeout_scope]` | `line 114 (communicate): name 'timeout' has unsupported local store` |
| restored | 1 | `unmet` | `[timeout_scope]` | `line 114 (communicate): non-numeric constant` |

Full mutant line set: `predicate PASS`, `head_pin PASS`, `tool_resolve PASS`,
`bounded_reads PASS`, `timeout_scope FAIL`, `drain_bind PASS`,
`timeout_state PASS`, `scratch PASS`, `selftest_conjunct PASS`.

**Verdict: SURVIVED.** The C1 target does not turn after the branch is removed —
the walrus survivor still exits 1 with only `timeout_scope` failing, exactly the
frozen target. The mutant is indistinguishable from pristine at the frozen
granularity; the only delta is the failure-reason string, which the target does
not pin.

Mechanism: the walrus target `timeout` is an `ast.Name` with `Store` context.
With the branch gone it is no longer added to `handled_names`, so the trailing
sweep (`isinstance(sub, ast.Name) … isinstance(sub.ctx, ast.Store) and id(sub)
not in handled_names`, pristine lines 336–338) records it as
`unsupported local store`, which raises `Unresolvable` on the same read site.
That generic sweep is a fail-closed superset of the deleted arm for a `None`
binding.

## No-harm guards under the mutant

- Honest counter `count-c8.py`: all nine checks PASS, `CONFORM=met`, exit 0 —
  unchanged.
- Checker `--selftest` on the mutated bytes: `CONFORM_SELFTEST pass=14 fail=0`,
  exit 0. The `timeout_scope_walrus` arm inserts `(timeout := None)`, which the
  store sweep still catches, so the self-check is blind to the deletion.

## Auxiliary discrimination probe (same mutant)

Fixture `walrus-positive.py` = `count-c8.py` plus `(timeout := GIT_TIMEOUT_S)` in
`run()` (sha256 `49f6e8cb65cc1ab9b4280d574757b998c4899620aee63c3634960cd6ea7eee35`),
so the walrus target binds a finite positive value:

| bytes | exit | CONFORM | failing checks |
|---|---|---|---|
| pristine | 0 | `met` | `[]` |
| mutant | 1 | `unmet` | `[timeout_scope]` (detail: `name 'timeout' has unsupported local store`) |

The deleted arm is behavior-bearing precisely for a walrus binding that resolves
to a finite positive value; there it is the only path that resolves the binding,
and the mutant turns a sound fixpoint into a fail-closed violation. No routed
survivor and no selftest arm exercises that shape — all bind `None`, where the
store sweep is a superset.

## Restoration

- Restored bytes: `cp pristine-conform.py → repo/.ufo/waves/round-41/conform.py`;
  restored sha256 `e1f2e11e…` equals pristine, and `diff -q` reports the files
  byte-identical.
- Restored run re-executed the same detector command and reproduced the pristine
  output exactly (table above), so the sandbox is back at pristine behavior.
- Sandbox left at `/tmp/mori-r41-mutwalrus-ofWSwTad` as disposable; no lane
  artifact other than this report.

## Coverage finding

Deleting the `NamedExpr` arm never greens the routed walrus survivor, so the
C1 kill rule cannot catch this removal; the generic `Store` sweep preserves
fail-closed behavior at that fixture. Killing the mutant requires a fixture
whose walrus target binds a finite positive value (pristine `met`, mutant
`unmet`) — the shape probed above. This is a coverage observation, not a
contract change.
