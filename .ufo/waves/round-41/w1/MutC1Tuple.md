# MutC1Tuple — mutation probe on C1 binding inventory

Seat: mutation-tester (leaf). Claim under attack: C1 operability / P-C10 binding
inventory "covers ... tuple/list destructuring" and "fails closed" on the three
routed survivors. Target bytes: `.ufo/waves/round-41/conform.py` (r41 checker),
measured in disposable clones at `aa161e998eb22282e3d96ed2710bb0b39e5163de`
(the revision used by `evidence/control-after.txt`; checker bytes there are
identical to the lane working tree, `e1f2e11e…`).

## Mutant

Smallest behavior-bearing point: `_assignment_values()` element-wise RHS→target
extraction, pristine lines 270–277.

```
-    if isinstance(value, (ast.Tuple, ast.List)) \
-            and len(target.elts) == len(value.elts) \
-            and not any(isinstance(child, ast.Starred) for child in target.elts):
-        for child, item in zip(target.elts, value.elts):
-            yield from _assignment_values(child, item, name)
-    else:
-        for target_name in _name_targets(target, name):
-            yield target_name, None, "unresolved destructuring"
+    for target_name in _name_targets(target, name):
+        yield target_name, None, "unresolved destructuring"
```

Effect: every name bound by tuple/list destructuring is recorded as the
fail-closed `"unresolved destructuring"` event instead of resolving the RHS
element that actually binds it.

- pristine checker sha256 `e1f2e11e7556cb4522c36cf22b3666650561e8eba0a7a7e85dc8c22c65475427`
- mutant checker sha256 `1483a1f8249c469a6bda5fc99393f069b49cd77a5e61a8c899444cbdaef4e00f`
- fixtures: `survivor-tupleunpack-none.py` sha256 `d0362fae8b5fa85d8a44f27475de1e1ed685fa927b9ad660d98d4a795bd1d8c6`

## Detector (bounded, same command as the frozen counter)

```
python3 .ufo/waves/round-41/conform.py aa161e99… --repo <sandbox> \
  --contract <sandbox>/.ufo/waves/round-39/contract.md \
  --counter <sandbox>/.ufo/waves/round-41/fixtures/c1/survivor-tupleunpack-none.py
```

Expected detector: nine checks run, `timeout_scope` FAIL and only that check,
`CONFORM=unmet`, exit 1 (frozen C1 target: `survivor_failures=3`, honest counter
`CONFORM=met`).

### Pristine bytes (baseline — passes the frozen target)

```
check bounded_reads      PASS (survivor-tupleunpack-none.py: bounded=[] value=['line 114 (communicate): non-numeric constant'])
check timeout_scope      FAIL (survivor-tupleunpack-none.py: bounded=[] value=['line 114 (communicate): non-numeric constant'])
check drain_bind         PASS (survivor-tupleunpack-none.py: violations=[])
check timeout_state      PASS (exit=1 timeout_reason=True pass=False)
check scratch            PASS (survivor-tupleunpack-none.py: mkdtemp_dir=True root=True)
check selftest_conjunct  PASS (survivor-tupleunpack-none.py: honest_comm=[] strips=6 detected=6 anchor=True entry_live=True)
CONFORM=unmet
EXIT=1
```

(identical to `evidence/control-after.txt` lines 34–46.)

### Mutated bytes (the probe)

```
check bounded_reads      PASS (survivor-tupleunpack-none.py: bounded=[] value=["line 114 (communicate): name 'timeout' has unresolved destructuring"])
check timeout_scope      FAIL (survivor-tupleunpack-none.py: bounded=[] value=["line 114 (communicate): name 'timeout' has unresolved destructuring"])
check drain_bind         PASS (survivor-tupleunpack-none.py: violations=[])
check timeout_state      PASS (exit=1 timeout_reason=True pass=False)
check scratch            PASS (survivor-tupleunpack-none.py: mkdtemp_dir=True root=True)
check selftest_conjunct  PASS (survivor-tupleunpack-none.py: honest_comm=[] strips=6 detected=6 anchor=True entry_live=True)
CONFORM=unmet
EXIT=1
```

Changed check: **none changes verdict.** `timeout_scope` stays FAIL and the
verdict tuple is identical; the only changed bytes are the violation *reason*
inside the `value=` detail (`non-numeric constant` →
`name 'timeout' has unresolved destructuring`). The mutant is indistinguishable
to the frozen detector at verdict level.

The mutant's own 14-arm selftest also misses it:

```
PASS timeout_scope_tupleunpack tuple-unpacked timeout binding to None -> only timeout_scope failed
...
CONFORM_SELFTEST pass=14 fail=0
EXIT=0
```

Routed four under the same mutant bytes (second sandbox, honest counter +
three survivors): `count-c8` CONFORM=met EXIT=0; `survivor-walrus-none`,
`survivor-tupleunpack-none`, `survivor-deadloop-rebind` each CONFORM=unmet
EXIT=1 with only `timeout_scope` failing — i.e. the frozen target
`survivor_failures=3` is still met, so nothing in the C1 kill rule can reach
this mutant.

## Supplementary discrimination probe (why the survivor is blind)

Derived counter: the honest `count-c8.py` plus one line as the first statement
of `run()` — a *sound* positive tuple unpack:

```
def run(cmd, cwd=None, timeout=GIT_TIMEOUT_S, env=None):
    timeout, _dead_unpack = 30, 0
```

Probe sha256 `a05150f76a850d6c8b2722172338f4c6f042d1fbf9b4f51953019c6898897560`.

| checker bytes | probe `timeout_scope` | verdict | exit |
|---|---|---|---|
| pristine | PASS `value=[]` | `CONFORM=met` | 0 |
| mutant | FAIL `name 'timeout' has unresolved destructuring` | `CONFORM=unmet` | 1 |
| restored | PASS `value=[]` | `CONFORM=met` | 0 |

So the removal is behavior-bearing (it false-positives a legitimate
finite-positive tuple binding), but the routed survivor cannot see it: the
survivor binds `None`, and both the extraction path and the blanket
`"unresolved destructuring"` fallback fail closed on `None`. Fail-closedness is
double-covered; only *precision* is lost.

## Verdict

**SURVIVED** — coverage finding, not a contract breach.

- The frozen C1 target is still met by the mutant (3/3 survivors unmet, honest
  counter met, selftest 14/0), so the kill rule cannot reject it.
- The P-C10 sentence "covers ... tuple/list destructuring" is only exercised
  negatively. A checker that records every destructured binding as unresolved
  would satisfy the routed survivor, the honest counter and all fourteen
  selftest arms.
- Discriminating anchor that would kill this mutant (owner decision, not
  applied): a positive tuple-unpack arm/counter resolved as a *value* event and
  required `CONFORM=met`, or a selftest arm asserting the resolved-value reason
  string for tuple extraction.

## Restoration evidence

Sandbox 1 (`/tmp/mori-r41-mut-c1tuple-KkaKDY`, clone at `aa161e99…`):

- pristine copy saved before edit: `e1f2e11e…` (44139 bytes)
- mutated: `1483a1f8…`; `diff -u` shows exactly the 8→2 line replacement at
  pristine lines 270–277
- restored by byte copy, sha256 `e1f2e11e…` = pristine, `git status --porcelain`
  and `git diff --stat` for the path empty
- re-ran the survivor detector on restored bytes: `timeout_scope` FAIL with
  `value=['line 114 (communicate): non-numeric constant']`, other checks PASS,
  `CONFORM=unmet`, EXIT=1 — the baseline detail text, not the mutant's
- re-ran the probe on restored bytes: `CONFORM=met`, EXIT=0
- re-ran the checker selftest on restored bytes:
  `CONFORM_SELFTEST pass=14 fail=0`, EXIT=0 (same as pristine)

Sandbox 2 (`/tmp/mori-r41-mut-c1tuple2-oovxJD`): same mutation, routed-four run,
then `git checkout --` restore; sha256 `e1f2e11e…`, `git status`/`git diff`
empty.

No lane file, Git index, jj state, sibling repo or `.ufo` state was modified;
no production checker bytes were touched (all runs inside `/tmp` clones). No
tools installed or updated.
