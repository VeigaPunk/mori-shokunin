# CritNewSurvivor — new-survivor falsification of C1 (`timeout_scope`)

Seat: critic (read-only + `.scratch/` artifacts). Claim attacked: **C1 / P-C10
`timeout_scope`** — "every `timeout=` keyword in every counter resolves in the
scope of its read site … and the value must be a finite positive number".

**Verdict: C1 is FALSIFIED.** Three independent one-edit counter fixtures,
each derived from the frozen `count-c8.py`
(sha256 `4e4d50eb…f6da`, pin in `evidence/freeze-r40.txt`), print
`CONFORM=met` exit 0 under `conform.py` (sha256 `5025b966…83aaf`, pinned)
while their runtime `communicate(timeout=…)` read-site value is `None` —
an unbounded wait, i.e. *not* a finite positive number. The defect is
fixable, not a judge-reject tradeoff (correction below).

## The seam (two binding-model blind spots in `static_checks`)

`_resolve_timeout_name` reads a function-local `timeout=` name through
`_function_bindings(fn, name)`, which collects `ast.Assign`/`ast.AnnAssign`
nodes via `ast.walk` — **breadth-first** — and resolves
`local_values[-1]`, the *last binding in BFS order, not execution order*.
Any binding nested inside an `if`/`try`/`for`/`while`/`with` body is yielded
after every top-level function binding regardless of source position, so a
dead nested binding outranks an earlier unconditional rebind. Separately,
`ast.NamedExpr` (walrus) and destructuring targets (`Tuple`/`List` as
`targets[0]`) are invisible to the collector, so the name falls through to
the *parameter default* `GIT_TIMEOUT_S` and resolves 120 while the runtime
local is `None`.

Fixture edits (each is exactly the shown insertion after
`def run(cmd, cwd=None, timeout=GIT_TIMEOUT_S, env=None):`):

| fixture | inserted body | static model sees | runtime value |
|---|---|---|---|
| `.scratch/CritNewSurvivor/survivor-deadloop-rebind.py` | `timeout = None` then `for _dead_rebind in (): timeout = GIT_TIMEOUT_S` | `[None, GIT_TIMEOUT_S]` → resolves `[-1]` = 120 | `None` |
| `.scratch/CritNewSurvivor/survivor-walrus-none.py` | `(timeout := None)` | `[]` → param default 120 | `None` |
| `.scratch/CritNewSurvivor/survivor-tupleunpack-none.py` | `timeout, _dead_unpack = None, None` | `[]` → param default 120 | `None` |

## Receipts (commands actually run)

1. `python3 .ufo/waves/round-40/conform.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --counter .scratch/CritNewSurvivor/survivor-deadloop-rebind.py`
   → all nine checks PASS incl. `timeout_scope PASS (… value=[])` → **`CONFORM=met`, exit 0**.
2. Same command with `survivor-walrus-none.py` → **`CONFORM=met`, exit 0** (`value=[]`).
3. Same command with `survivor-tupleunpack-none.py` → **`CONFORM=met`, exit 0** (`value=[]`).
   (`head_pin` printed `pin=ede486b7…dc2e tip=ede486b7…dc2e` — the checker's
   own live-HEAD measurement, equal on both sides; the `rev` argument feeds
   only the `timeout_state` arm. No check was weakened by the fixtures.)

4. Runtime discrimination (honest vs tampered `run`, same interpreter):
   ```
   honest       ProbeTimeout in 0.20s (child exceeded 0s) (timeout enforced, value 0.2)
   deadloop     completed in 2.01s rc=0 (timeout NOT enforced -> runtime value is None)
   walrus       completed in 2.01s rc=0 (timeout NOT enforced -> runtime value is None)
   tupleunpack  completed in 2.01s rc=0 (timeout NOT enforced -> runtime value is None)
   ```
   Each fixture was called as `run([sys.executable,"-c","import time;time.sleep(2)"], timeout=0.2)`:
   the tampered `run` **overrides the caller's bound `timeout=0.2` with `None`**
   inside its own body, so `proc.communicate(timeout=None)` waits the full
   2 s. The read-site value is `None` — a direct violation of P-C10's
   "finite positive number" while the checker resolves 120 / param-default
   120 and prints `met`.

5. Closed candidates (checker correctly fails closed — the hole is
   binding-form blindness + BFS ordering, not universal):
   `timeout=T()` with `T = lambda: GIT_TIMEOUT_S` →
   `value_violations=["line 114 (communicate): expression Call(…)"]`;
   `timeout=GIT.TIMEOUT_S` (attribute read) →
   `value_violations=["line 114 (communicate): expression Attribute(…)"]`.

6. `_function_bindings` dump on the three fixtures (run against the landed
   checker): `[Constant(None), Name('GIT_TIMEOUT_S')]`, `[]`, `[]` — matching
   the seam table above.

## Impacted axes

- **`timeout_scope` (primary)**: resolves name-not-value under execution
  order; P-C10's "resolves in the scope of its read site … finite positive"
  is not computed. All three survivors are admitted name-shadow variants
  the round's own kill rule was meant to close (r39 finding 4 class).
- **`bounded_reads` (secondary)**: prints PASS on a counter whose `run()`
  performs an actually-unbounded wait; the check's words are about kwarg
  presence so this is a consequence, not an independent falsification.
- **`selftest_conjunct` / selftest coverage**: the eleven-arm mutation
  table contains no arm exercising binding-order or non-`Assign` binding
  forms; a v3.1 that only patches walrus still passes `--selftest` while
  the dead-loop survivor stays green — the coverage gap is structural.

## Smallest safe correction

In `_function_bindings`/`_resolve_timeout_name`: collect local bindings for
the read name in **source order** (sort collected nodes by
`(lineno, col_offset)`, not `ast.walk` yield order); count `ast.NamedExpr`,
`Tuple`/`List` destructuring targets containing the name, and loop/with
targets as bindings; when the function carries more than one binding of the
read name and they cannot be linearized into a single dominating last
binding (any binding under a conditional/loop block, or differing resolved
values), fail closed — mirroring the module-level `conditional` rule the
checker already implements. That one change rejects all three fixtures and
keeps the honest counter green (its `run` has a single binding — the
parameter default).

## Boundary notes

- Fixtures + probe live under `.scratch/CritNewSurvivor/` (lane); no
  production bytes touched; fleet repo untouched. Fixture sha256:
  deadloop `9e9319b6…bcc2`, walrus `beb751f4…91bf`, tuple `d0362fae…d8c6`.
- No tools installed this seat (python3 stdlib only).
- Attempt budget: falsified on attempt 1 (dead-loop rebind); walrus and
  tuple-unpack corroborate the same defect class; lambda-alias and
  attribute-read candidates fail closed and are not holes.
