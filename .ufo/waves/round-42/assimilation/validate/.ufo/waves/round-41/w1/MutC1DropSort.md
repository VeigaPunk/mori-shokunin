# MutC1DropSort — mutation probe (C1 operability, round 41)

Seat: `L1-mori-r41-attempt2.MutC1DropSort` (leaf mutation-tester, attempt 2).
Scope: one defect at the source-order binding sort in the frozen r41 checker, probed
with the dead-loop survivor fixture. Read-only against the lane; no production file
edited.

## Verdict

**SURVIVED.** Removing the source-order sort produces **no regression signal** on the
dead-loop fixture: pristine and mutant checker outputs are **byte-identical**
(`CONFORM=unmet`, exit 1, only `timeout_scope` failing). No detector output moved, so
the defect is not killed by the assigned detector. This is a coverage finding, not a
contract change.

## Environment (measured)

- Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin` (never mutated; see restoration).
- Disposable clone: `/tmp/mut-c1-dropsort-Hm0Y9N/repo`, detached at
  `aa161e998eb22282e3d96ed2710bb0b39e5163de` — the revision recorded in
  `evidence/control-after.txt` (`mode=after revision=aa161e9…`), live HEAD equal to it.
- Checker under test: `.ufo/waves/round-41/conform.py`,
  sha256 `e1f2e11e7556cb4522c36cf22b3666650561e8eba0a7a7e85dc8c22c65475427`
  (identical at lane HEAD `7450722e…` and at `aa161e9`).
- Fixture: `.ufo/waves/round-41/fixtures/c1/survivor-deadloop-rebind.py`,
  sha256 `9e9319b6bb2af4e927d82409953fad96db45aed4fef21ec29e6c4b814ddabcc2`.
- Interpreter: `/usr/bin/python3` = Python 3.14.8.

## Mutant

Smallest behavior-bearing point: the only ordering statement in
`_function_bindings`, pristine line 339:

```diff
--- conform.py (pristine)
+++ conform.py (mutant)
@@ -336,7 +336,6 @@
         if isinstance(sub, ast.Name) and sub.id == name \
                 and isinstance(sub.ctx, ast.Store) and id(sub) not in handled_names:
             add(sub, "unsupported local store")
-    events.sort(key=lambda event: (event[0], event[1]))
     return events
```

Mutant file: `/tmp/mut-c1-dropsort-Hm0Y9N/conform-dropsort.py`,
sha256 `b0d81b962effba1e6601aa0fea294514a5df90ea0c19d4c9b937d9e5d6733d8b`.
The deletion is exactly one line (`diff -u` above is the complete diff); the function's
docstring still claims "Return source-ordered binding events for `name`", so the mutant
advertises an ordering it no longer imposes.

## Detector and baseline (pristine, must fire)

Command (replicates the receipt form in `control-after.txt`):

```
/usr/bin/python3 <repo>/.ufo/waves/round-41/conform.py aa161e998eb22282e3d96ed2710bb0b39e5163de \
  --repo <repo> --contract <repo>/.ufo/waves/round-39/contract.md \
  --counter <repo>/.ufo/waves/round-41/fixtures/c1/survivor-deadloop-rebind.py
```

Baseline output (sha256 `5e70ac5876825a18607aeaa8aa22645967bc36d4c510019160bf46fc9b7f640c`):

```
check predicate          PASS (exit=0 equal=True)
check head_pin           PASS (pin=aa161e998eb22282e3d96ed2710bb0b39e5163de tip=aa161e998eb22282e3d96ed2710bb0b39e5163de)
check tool_resolve       PASS (exit=0 resolved=…/witness-summary-only-live.txt)
check bounded_reads      PASS (survivor-deadloop-rebind.py: bounded=[] value=['line 116 (communicate): non-numeric constant'])
check timeout_scope      FAIL (survivor-deadloop-rebind.py: bounded=[] value=['line 116 (communicate): non-numeric constant'])
check drain_bind         PASS (survivor-deadloop-rebind.py: violations=[])
check timeout_state      PASS (exit=1 timeout_reason=True pass=False)
check scratch            PASS (survivor-deadloop-rebind.py: mkdtemp_dir=True root=True)
check selftest_conjunct  PASS (survivor-deadloop-rebind.py: honest_comm=[] strips=6 detected=6 anchor=True entry_live=True)
CONFORM=unmet
EXIT=1
```

Baseline passes the frozen C1 target for this fixture (`CONFORM=unmet`, exit 1, only
`timeout_scope` failing), so the probe is conclusive, not inconclusive.

No-harm baseline guards, same sandbox: honest counter `count-c8.py` → `CONFORM=met`,
exit 0 (sha256 `83d2ba7a19f39615ca7a5b67c750c8b3d66d024a35550f7e107550b95ae2a562`);
checker `--selftest` with the measured revision → `CONFORM_SELFTEST pass=14 fail=0`,
exit 0.

## Mutant run (assigned detector)

Same command with the mutant checker. Output sha256
`5e70ac5876825a18607aeaa8aa22645967bc36d4c510019160bf46fc9b7f640c` — **identical to
baseline**, `cmp` exit 0. Exact regression signal: **none**. The mutant still reports
`CONFORM=unmet`, exit 1, only `timeout_scope` FAIL, with unchanged detail
`line 116 (communicate): non-numeric constant`.

Guards under the mutant (all byte-identical to their pristine baselines):

| input | pristine sha256 | mutant sha256 | result |
|---|---|---|---|
| `survivor-deadloop-rebind.py` | `5e70ac58…7f640c` | `5e70ac58…7f640c` | `CONFORM=unmet`, exit 1, only `timeout_scope` |
| `count-c8.py` (honest) | `83d2ba7a…a2a562` | `83d2ba7a…a2a562` | `CONFORM=met`, exit 0 |
| `survivor-walrus-none.py` | `ae6f553d…c5397f` | `ae6f553d…c5397f` | `CONFORM=unmet`, exit 1, only `timeout_scope` |
| `survivor-tupleunpack-none.py` | `681b34f2…c529f9dd` | `681b34f2…c529f9dd` | `CONFORM=unmet`, exit 1, only `timeout_scope` |

Mutant `--selftest`: `CONFORM_SELFTEST pass=14 fail=0`, exit 0 — including the
`timeout_scope_deadloop` arm ("dead-loop rebind must not outrank the source-ordered
binding"), which still flips only `timeout_scope`. The checker's own 14-arm conjunction
therefore cannot see the removed sort either.

## Why it survives (measured, not inferred)

A read-only introspection driver (`/tmp/mut-c1-dropsort-Hm0Y9N/probe-order.py`) imported
both checker copies and called `_function_bindings` / `static_checks` directly:

```
== dead-loop fixture: run() events for 'timeout'
pristine: [(110, 4, 'value', 'None'), (112, 8, 'value', 'GIT_TIMEOUT_S')]
mutant  : [(110, 4, 'value', 'None'), (112, 8, 'value', 'GIT_TIMEOUT_S')]
identical: True

== dead-loop fixture: static_checks value_violations
pristine: ['line 116 (communicate): non-numeric constant']
mutant  : ['line 116 (communicate): non-numeric constant']
identical: True
```

`_function_scope_nodes` walks statements depth-first in document order, and the
dead-loop fixture's two `timeout` bindings (`timeout = None` at line 110, the empty-loop
`timeout = GIT_TIMEOUT_S` at line 112) are already yielded in line order. The sort is
therefore inert on this input, and the fixture's rejection is carried by the
all-bindings-must-resolve-to-one-finite-positive rule (`None` fails), not by ordering.

## Coverage finding (no contract change)

The predicate text says bindings are recorded "in source order", but the frozen routed
detector set never observes that ordering. Supplementary control on a synthetic shape
where DFS order and source order diverge (a comprehension store on an earlier line is
appended by the second pass after a later `timeout = None`):

```
pristine: ["line 6 (communicate): name 'timeout' has unsupported local store"]
mutant  : ['line 6 (communicate): non-numeric constant']
```

The detail string differs, so the deletion is not globally equivalent, but the check
verdict is still `timeout_scope` FAIL in both cases — ordering can only select which
fail-closed message is emitted, never flip a verdict. Removing the sort is consequently
unobservable to any fixture whose read site fails on binding values alone, which is the
entire routed C1 survivor class. Suggested follow-up (not performed here): a detector
arm that requires the *first* failing-binding reason to match source order, if the
"source order" clause is meant to be load-bearing.

## Restoration evidence

The lane checker was never written; only the disposable sandbox copy was mutated. The
mutant copy was nonetheless restored from the committed blob:

```
before: b0d81b962effba1e6601aa0fea294514a5df90ea0c19d4c9b937d9e5d6733d8b  conform-dropsort.py
after : e1f2e11e7556cb4522c36cf22b3666650561e8eba0a7a7e85dc8c22c65475427  conform-dropsort.py
committed blob / sandbox repo copy / lane copy: e1f2e11e…75427 (all equal; cmp clean)
restored detector output: sha256 5e70ac58…7f640c — byte-identical to the pristine baseline
lane `git status --porcelain`: unchanged (only the pre-existing untracked
`.ufo/waves/round-41/evidence/wave-run.*` and `.ufo/waves/round-41/w1/`)
```

No git index, jj state, `.ufo/state`, watchdog log, sibling repo, or production file was
modified. Sandbox `/tmp/mut-c1-dropsort-Hm0Y9N` is disposable and was restored anyway.

Tooling: no installs or updates were performed (none needed).
