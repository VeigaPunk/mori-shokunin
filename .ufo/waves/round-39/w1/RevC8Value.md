# RevC8Value — C8 `timeout_value` fold audit (round 39, wave 1)

Scope: `.ufo/waves/round-39/conform.py` `_resolve` / `_timeout_value` / `static_checks`
timeout map, plus the three mandated `timeout=NAME` variants built from
`count-c7.py` bytes at scored tip `13bfba23b7ca063c76d3504a2ff6eb7b6a294932`.

Lane was treated read-only: every variant and output lives under
`.ufo/waves/round-39/scratch/RevC8Value/`; the only lane file written is this report.
No `lsp` device exists in this seat's tool set (no `lsp` tool in the inventory), so
definition/reference work was done by importing the checker and executing its own
`static_checks` on exact counter bytes — semantic, not grep. Recorded as a tooling gap.

## Assigned test: verdict

All three mandated variants are rejected by `timeout_value`, with `CONFORM=unmet`
exit 1: **the assigned acceptance holds for those three.** The fold itself is not
sound in general: two non-positive runtime values (`None`, `-1`) pass `timeout_value`
with `CONFORM=met` when the name is rebound anywhere other than a top-level
unconditional `Assign` (findings H1/H2). Details below.

## 1. What `_resolve` can and cannot fold

Map construction: `assign` is filled **only** from `tree.body` (module top level),
`ast.Assign`, exactly one target, target is a `Name` (`conform.py:170-174`). Function
defaults are keyed by **function name** (`func_params`, `conform.py:176-190`).
A `Name` that is not a parameter is resolved from the module `assign` map with no
regard for where it is read (`conform.py:120-124`).

### Folds to a number (then positivity-tested at `conform.py:153-154`)

| form | example → value | notes |
|---|---|---|
| int/float literal | `120`, `0.5`, `0x10`, `1e3` | bool/str/bytes/None/complex rejected as "non-numeric constant" (`:116-119`) |
| `Name` → top-level single-target `Assign` | `NAME = 30`, `timeout=NAME` → 30 | chains work: `A = B; B = 120` → 120 |
| `Name` → parameter default | `def run(timeout=GIT_TIMEOUT_S)` → 120 | positional and kw-only defaults; a default that references another parameter cannot fold because `:122` passes `{}` as params |
| `UnaryOp USub` (nested) | `-1` → -1; `-(-5)` → +5 | only `USub`; `UAdd`, `Not`, `Invert` unsupported |
| `BinOp Add/Sub/Mult/Div` | `10+5`, `2*3`, `120/2`, `10-15` → -5 (rejected) | `/` is true division; FloorDiv/Mod/Pow/shifts/bitwise unsupported |
| `List`/`Tuple` | `(30, 60)` → `[30, 60]` | **all** elements resolved eagerly |
| `Subscript` | `(30,60)[1]` → 60; `[30][0]` → 30; `CAPS[0]` with `CAPS=[30,60]` | slice must be an `ast.Constant int`; base must resolve to list/tuple |

### Cannot fold — raises `Unresolvable`, check **fails closed**

- `IfExp` (`30 if FLAG else 60`), `Attribute`, `Compare`, `BoolOp`, `Dict`/`Set`,
  f-string, walrus, `Starred`, and any `Call` (`int("30")`, `abs(-30)`,
  `float("inf")`) — no call form appears in `_resolve`'s dispatch (`:115-147`).
- `BinOp` FloorDiv (`120//2`), Pow (`2**3`), Mod (`120%7`); `UnaryOp UAdd` (`+5`),
  `Invert` (`~0`).
- `Subscript` with a negative constant index (`(30,60)[-1]` parses the slice as
  `USub(1)`, not `Constant`, so it is not folded), a string slice
  (`CAPS["a"]`), a non-constant index, or an out-of-range index.
- `Name` bound only by: a **function-local** assignment, a `global` rebinding inside a
  function, a module-level assignment nested in `if`/`for`/`try` (`tree.body`
  recursion is absent), `AnnAssign` (`TIMEOUT: int = 30`), `AugAssign`,
  multi-target (`A = B = 30`), tuple unpacking, class body, or import alias.
- Win: a tuple whose *other* element is non-numeric, e.g. `(None, 30)[1]`, fails even
  though index 1 is numeric; a module-level non-numeric value fails even when the
  call site is dominated by a valid local (`false-FAIL` probe).
- Uncaught crashes (not `Unresolvable`): `timeout=1/0` or `120/NAME` with `NAME = 0`
  raises `ZeroDivisionError` (`:138`), and a cyclic assignment `A = A` recurses
  until `RecursionError` (`:124`). Both escape `static_checks` and become exit-2
  "conformance setup error" (main's blanket `except Exception`), never a FAIL line.

Evidence: `scratch/RevC8Value/fold-table.json` (40 cases) and `fold-extra.json`
(12 cases); each was produced by loading `conform.py` via importlib and calling
`static_checks(source)` on a synthetic counter whose `timeout=` expression is the
case.

## 2. Mandated variants and verdicts

Variants are one-line edits of `count-c7.py`: insert `NAME = <binding>` after
`GIT_TIMEOUT_S = 120` (count-c7.py:69) and change the `run()` default
`timeout=GIT_TIMEOUT_S` (count-c7.py:110) to `timeout=NAME`. Command per variant:

```
python3 .ufo/waves/round-39/conform.py 13bfba23b7ca063c76d3504a2ff6eb7b6a294932 \
        --counter .ufo/waves/round-39/scratch/RevC8Value/counter-<v>.py
```

| variant | binding | `timeout_value` | exit / CONFORM | receipt |
|---|---|---|---|---|
| base (unmodified) | — | PASS | 0 / met | `out-base.txt` |
| `neg` | `NAME = -1` | **FAIL** `timeout value -1 is not positive` | 1 / unmet | `out-neg.txt` |
| `zero` | `NAME = 0` | **FAIL** `timeout value 0 is not positive` | 1 / unmet | `out-zero.txt` |
| `str` | `NAME = "30"` | **FAIL** `non-numeric constant` | 1 / unmet | `out-str.txt` |
| `none` (control) | `NAME = None` | **FAIL** `non-numeric constant` | 1 / unmet | `out-none.txt` |
| `cond` (H2) | `NAME = 120` + `if os.environ.get(...): NAME = None` | **PASS** | 0 / **met** | `out-cond.txt` |
| `shadow-none` (H1) | module `TIMEOUT = 120`; local `TIMEOUT = None` at run() | **PASS** | 0 / **met** | `out-shadow-none.txt` |
| `shadow-neg` (H1) | same, local `TIMEOUT = -1` | **PASS** | 0 / **met** | `out-shadow-neg.txt` |
| `inf` | `NAME = 1e400` | **PASS** | 0 / **met** | `out-inf.txt` |

Violations are attributed to the consuming call, e.g. `line 115 (communicate)` —
the default declaration itself is only audited where a call passes it through.
The unmodified counter reproduces `CONFORM=met` with all nine checks PASS
(`out-base.txt`), and my independent `--selftest` run prints
`CONFORM_SELFTEST pass=9 fail=0` (exit 0, 50.7 s; `scratch/RevC8Value/selftest-mine.txt`),
matching `evidence/c8-after-selftest.txt`.

## 3. Findings

### H1 (High) — function-local shadowing defeats `timeout_value`; runtime `None`/`-1` passes with `CONFORM=met`

`conform.py:120-124` resolves a non-parameter `Name` from the module map regardless
of the read site, and `conform.py:170-174` never walks function bodies. A two-line
insertion in `run()` —

```
        TIMEOUT = None                     # counter-shadow-none.py:115
        out, err = proc.communicate(timeout=TIMEOUT)   # :116
```

with module-level `TIMEOUT = 120` — is reported `check timeout_value PASS
(counter-shadow-none.py: bounded=[] value=[])` and `CONFORM=met` (exit 0). The
runtime value is `None`: monkeypatching `subprocess.Popen` and calling the variant's
`run(["true"])` captures `communicate(timeout=None)`; the same capture for
`shadow-neg` is `-1`. `timeout=None` means no bound at all — exactly the r38 M19
bypass A class the check claims to close, resurrected without any module-level
`None`. The same map miss occurs through a `global NAME; NAME = None` rebinding
inside a function (static probe: PASS).

### H2 (High) — module-level conditional/loop/try assignment is invisible, though P-C8 says "module-level assignments"

`assign` is built only from `tree.body` (`conform.py:170-174`). A module-level
`if os.environ.get("MORI_TIMEOUT_UNBOUNDED"): NAME = None` after `NAME = 120`
is nested in an `If` node and never recorded. Result: `check timeout_value PASS`,
`CONFORM=met` (`out-cond.txt`), while importing `counter-cond.py` with
`MORI_TIMEOUT_UNBOUNDED=1` yields `NAME = None` and `run()` then calls
`communicate(timeout=None)`. Same PASS for `try:`-nested and `for:`-nested
assignments (static probes). This one sits inside P-C8's own wording ("resolves
through module-level assignments"): a module-level assignment making the value
`None` exists, but the fold does not see it.

*Discriminator:* P-C8's literal checkable text is exactly the checker's algorithm,
so a claim owner could rule H1/H2 out of predicate scope by reading "module-level"
narrowly. They cannot be ruled out of the predicate's stated purpose: the frozen
justification "so `timeout=NAME` with `NAME = None` fails" is false for these
byte-level variants — `NAME`/`TIMEOUT` is `None` at the call site and the checker
still says the value is positive.

### M3 (Medium) — non-finite literal `1e400` is accepted as a "positive numeric literal"

`ast.Constant` value is `inf`; `isinstance(inf, float)` and `inf <= 0` are false, so
`_timeout_value` (`conform.py:153-154`) accepts it: `NAME = 1e400` →
`timeout_value PASS`, `CONFORM=met` (`out-inf.txt`). Runtime check on this host
(CPython 3.14.8, Linux): `subprocess.run(["sleep","0.3"], timeout=1e400)` raises
`OverflowError: cannot convert float infinity to integer` in 0.00 s — so on this
platform it is a fail-open crash rather than an unbounded wait, and `run()` catches
only `TimeoutExpired`, so the counter would die. The check still certifies a value
that cannot function as a bounded timeout; `math.isfinite` is not required.
(Not a violation of my assigned FAIL condition — inf is positive and numeric.)

### L4 (Low) — arithmetic crashes escape as setup errors instead of FAIL

`timeout=1/0`, `120/NAME` with `NAME = 0` (`conform.py:138`), and `A = A`
(`:124`) raise `ZeroDivisionError`/`RecursionError`, which `static_checks` does not
convert to `Unresolvable`; the CLI exits 2 with "conformance setup error". Honest
(non-met), but `--selftest` would abort mid-loop on such a counter, and a legitimate
counter containing a guarded `x/y` timeout expression cannot be audited.

### L5 (Low, over-strictness — false FAIL only)

Valid counters can be rejected: a `Name` bound by `AnnAssign`, `AugAssign`,
multiple-target, a function-local assignment, or any conditional; `IfExp`; `UAdd`;
FloorDiv; negative subscript indices; `Subscript` of a dict; tuple/list elements that
are not numeric. Also, `func_nodes`/`func_params` are keyed by function name
(`conform.py:176,190`), so a call inside an earlier same-name definition sees no
params and fails with `name 'timeout' has no binding` (synthetic two-`run`
probe). All are conservative — they cannot let a non-positive value through.

## 4. Residual risk

- The three mandated variants are rejected, and the shipped counter is unchanged and
  passes; H1/H2 require editing counter bytes, so they do not falsify C2 **as
  measured**. They falsify the general wording of `timeout_value` and would let a
  future counter ship an unbounded read while `CONFORM=met`.
- `inf` (M3) is accepted; on a runtime where `select`/`poll` accepts `inf` instead of
  raising `OverflowError`, the same bytes would mean an unbounded wait. The observed
  behaviour here is a crash, not a hang.
- Adjacent to C8, not my target: `head_pin` is tautological. `--pin-only` prints live
  `git rev-parse HEAD` (count-c7.py:405-410) and `evaluate` compares it to a second
  live `git rev-parse HEAD` (conform.py:319-322), so it cannot bind the scored rev.
  During this audit the lane advanced through `20260b0c` → `296b2c56` → `eb986a9` →
  `ecb8a11` (reflog "export from jj"); my runs printed `head_pin PASS` at both
  `20260b0c` and `296b2c56` against the same `13bfba23` rev argument, and the
  recorded evidence used `f920eaf7`. `head_at_measurement` therefore labels the live
  worktree, not the measured bytes.
- The fold's module map is shared across scopes and unconditionally overwritten by
  the last top-level assignment; a conditional is not the only divergence — the
  static value can also be *stricter* than runtime (L5).

## 5. Verification gaps

- No `lsp` tool was available to this seat; caller/definition/diagnostics claims are
  backed by importing `conform.py` and executing its own `static_checks`/`_resolve`
  on exact AST inputs, which is stronger than text grep but is not an LSP server
  result.
- Independent `--selftest` was run once (pass=9/fail=0, exit 0). The `none`, `cond`,
  `inf`, `shadow-*` variants were run through full `conform.py` `evaluate` (all nine
  checks), not only `static_checks`.
- Runtime capture for H1 used a fake `Popen` recording the `timeout=` argument;
  the `None`/`-1` values are the actual values `run()` passes to `communicate`.
- Tool installs/upgrades: none (no package manager or network tool was needed).
