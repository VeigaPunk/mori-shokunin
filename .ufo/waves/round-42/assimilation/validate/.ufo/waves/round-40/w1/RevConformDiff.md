# RevConformDiff — round-40 conform v2→v3 hunk review

Seat: `RevConformDiff` (reviewer, read-only; no production edits).
Target: `git show bb1f2457:.ufo/waves/round-39/conform.py` (extracted at
`.ufo/waves/round-40/fixtures/extracted/conform-v2-r39.py`, sha256
`fe0be179aba9df7150f0b6cdb50a5f9bbdb411efb1263b46ffa6b21d46ef7987`)
→ `.ufo/waves/round-40/conform.py` at `265a955cc` (sha256
`5025b9664632d01063c11b4f5dadd4f9a063db66d73315d7ed25db8d90b83aaf`;
`git show HEAD:` and `git show 265a955cc:` and the disk file all match).
Measured HEAD at run time: `ede486b7a09afbacfb380d5871c46a8051a6dc2e`
("round-40: repair S229 registry placement …"); the instrument bytes are
identical to the scored tip, so every rerun below exercises the scored
instrument. The default run's `head_pin` line names `ede486b` because that
check is relative to current HEAD; the frozen receipt `c10-after.txt` names
`265a955cc`, which was correct at its measurement time.

No LSP device is exposed in this seat's toolset (no `lsp` tool/namespace in
the session); caller/definition checks were therefore done by importing the
checker with `importlib` and executing `static_checks`/`evaluate` directly,
which is stronger than text grep for this static-audit code.

## Verdict

C1's operational kill rules reproduce:

- default run → `CONFORM=met`, exit 0, all nine checks PASS;
- `--selftest` → `CONFORM_SELFTEST pass=11 fail=0`, exit 0 (57.23 s);
- all ten generated survivors → `CONFORM=unmet`, exit 1, each with the
  declared named check (timeout_scope for shadow-none/shadow-neg/cond/inf/
  divzero; drain_bind for decoy/underscore/second-popen/tuple; barecomm adds
  timeout_state and selftest_conjunct);
- two-counter audit (`count-c8` + `survivor-barecomm.py`) → `unmet` with
  per-counter `drain_bind` and `selftest_conjunct` FAIL;
- gutted-conjunct copy → `unmet`, `selftest_conjunct FAIL … entry_live=False`.

However, P-C10's universal wording is **not** implemented by `timeout_scope`.
The checker prints `CONFORM=met` on counters that violate the frozen words,
including the predicate's own explicit `TIMEOUT = None` shadow example
(F1 below). Two High findings. The new checks also reject runtime-honest
counters in shapes P-C10 does not cover (F5/F6/F7) — behavior beyond the
frozen words. The operational claim survives; the predicate overstates what
the instrument checks.

## Hunk-by-hunk classification

`(a)` P-C10 `timeout_scope` change, `(b)` P-C10 `drain_bind` change,
`(c)` P-C10 `selftest_conjunct` change, `(d)` selftest arm/fixture plumbing,
`(e)` other.

| v3 lines (new) | Content | Class |
|---|---|---|
| 1–64 | docstring rewrite (P-C10 name, eleven arms, check names, scratch round-40) | (e) — two doc/behavior mismatches, F8 |
| 67–122 | `SCRATCH_ROOT`/`DEFAULT_COUNTERS` → round-40; `CHECK_NAMES` renames; `SELFTEST_MUTATION_NAMES`; `MUTATION_CHECK_ALIAS`; P-C10 `PREDICATE` | (c) table + (e) paths/names |
| 192–342 | `_finite_positive`, `_module_assignments`, `_function_bindings`, `_global_names`, `_resolve_timeout_name`, `_popen_name`, `_result_consumed` | (a) + (b) |
| 354–360 | `static_checks` computes `unconditional, conditional` | (a) |
| 397–418 | per-keyword branch: `ast.Name` → scope resolver, other expressions → module fold; fold-error catches | (a) |
| 425–456 | per-`Popen` drain loop: same name, timeout kw, consumed result | (b) |
| 493–501 | removes `has_communicate_timeout`, `first_communicate_segment`, `_first_communicate_segment` | (e) dead-code removal |
| 554–574 | `timeout_value`→`timeout_scope`; `drain_shape`→per-counter `drain_bind` | (a)+(b) rename/scope |
| 597–661 | `evaluate` `selftest_conjunct` rewritten per counter (`entry_live`, strip loop); old first-counter conjunct removed; `CONJUNCT_*`; `selftest_mutations` extraction | (c) |
| 681–744 | `selftest_mutations` arms: `run_comm` shadow anchor, `tool_popen`/`decoy_new`, eleven-arm list | (d), (c)-adjacent |
| 753–766 | `MUTATION_CHECK_ALIAS` resolution and FAIL detail | (d) |

Every hunk classifies; no unclassifiable hunk. The three made-sound checks
own hunks 192–418 (timeout_scope), 309–338/425–456 (drain_bind), and
597–640/651–766 (selftest_conjunct). Findings F1–F6 are inside (a);
F7 inside (b); F8 in (e); F9 in (c)/(d).

## Findings (severity order)

### F1 — High: `timeout_scope` accepts a read-site `None` shadow when a later assignment exists

`_resolve_timeout_name` takes the last binding found by `ast.walk`
(`conform.py:239-251`, `281-284`), not the binding that reaches the read
site. `ast.walk` is breadth-first, so "last" is not even textual order.

Probe `/tmp/probe-p3.py` = `count-c8.py` with `run()`'s first drain changed to:

```python
        TIMEOUT = None
        out, err = proc.communicate(timeout=TIMEOUT)
        TIMEOUT = 120
```

Receipt:

```
python3 .ufo/waves/round-40/conform.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --counter /tmp/probe-p3.py
check timeout_scope      PASS (probe-p3.py: bounded=[] value=[])
CONFORM=met
EXIT=0
```

Runtime trace (imported the probe, stubbed `subprocess.Popen`):
`P3 run() communicate timeout seen: [None]`.

P-C10: "every `timeout=` keyword … resolves in the scope of its read site …
a function-local `TIMEOUT = None` shadow … fails". The read-site value is
`None`; v3 passes. The v2 checker rejected the same shape (`value:
["line 5 (run): name 'TIMEOUT' has no binding"]`), so this is also a
regression in the loosening direction. The same last-binding rule accepts
read-before-assignment (runtime `UnboundLocalError`):
`def f(): subprocess.run(..., timeout=TIMEOUT); TIMEOUT = 120` →
`value_violations=[]`.

### F2 — High: conditional module rebinds are not failed closed

P-C10: "a module-level binding nested in `if`/`try`/`for`/`while` makes the
name conditionally rebound and fails closed". `_resolve_timeout_name`
(`conform.py:291-303`) only fails when values disagree; if every conditional
binding agrees — or if there is no unconditional base and one conditional
binding — it returns the value. The function's own docstring
(`conform.py:269`) says "fails closed unless every binding agrees", an
explicit relaxation absent from the frozen predicate; the check docstring
(`conform.py:19-23`) still says "fails closed".

Full-checker receipts:

```
# /tmp/probe-p1c.py: if os.environ.get("MORI_TIMEOUT_UNBOUNDED") is None: NAME = 120
#                    def run(..., timeout=NAME)         (no unconditional NAME)
CONFORM=met  EXIT=0   (timeout_scope PASS)
# /tmp/probe-p1b.py: NAME = 120; if env: NAME = 120; run(..., timeout=NAME)
CONFORM=met  EXIT=0   (timeout_scope PASS)
```

`static_checks` on the same shapes returns `value_violations=[]`. v2 rejected
the conditional-only shape (`name 'NAME' has no binding`). If the condition
is false, the name is unbound at runtime (NameError); v3 accepts it.

### F3 — Medium: composite `timeout=` expressions bypass the scope resolver

`static_checks:401-407` sends only a bare `ast.Name` through
`_resolve_timeout_name`; every other expression falls back to
`_timeout_value(..., assign, params)`, i.e. the module map. P-C10 says
"every `timeout=` keyword … resolves in the scope of its read site".

Probe `/tmp/probe-p7c.py` appends (module `TIMEOUT = 120`):

```python
def _probe_composite():
    TIMEOUT = None
    return subprocess.run(["true"], timeout=TIMEOUT * 1)
```

Receipt: `CONFORM=met`, `timeout_scope PASS (value=[])`. Runtime trace of the
same function: `TypeError: unsupported operand type(s) for *: 'NoneType' and
'int'` — the read-site value is `None`, the checker read module 120.
(`except Exception` at `conform.py:414-416` also turns any fold bug into a
"violation"; broader than P-C10's named `ZeroDivisionError`/`RecursionError`.)

### F4 — Medium: the `global` clause ignores the function's own global write

`_global_names` (`conform.py:254-260`) makes a `global` declaration skip the
function-local bindings, then the resolver reads only the top-level map
(`conform.py:271-281`); a `global TIMEOUT; TIMEOUT = None` inside the
function is not added to the module map. P-C10: "a `global` rebinding is read
at module scope" and "the value must be a finite positive number".

Probe `/tmp/probe-p11g.py` appends (module `TIMEOUT = 120`):

```python
def _probe_global():
    global TIMEOUT
    TIMEOUT = None
    return subprocess.run(["true"], timeout=TIMEOUT)
```

Receipt: `CONFORM=met`, `timeout_scope PASS`. Runtime trace:
`P11g _probe_global read timeout: [None] | module TIMEOUT after call: None`.
v3 reads the stale top-level 120, not the value at the read site.

### F5 — Medium: scope-blind `ast.walk` misattributes nested-function bindings

`_function_bindings` and `_global_names` walk the whole enclosing function,
including nested `def`s (`conform.py:239-260`); `_module_assignments` walks
all nodes inside a top-level `if`/`try`/`for`/`while`/`with`, including
function bodies (`conform.py:227-236`). Consequences:

- False reject: `/tmp/probe-p5n.py` appends (module `TIMEOUT = 120`):
  `def _probe_nested(): def inner(): TIMEOUT = None; return
  subprocess.run(["true"], timeout=TIMEOUT)` → full checker `CONFORM=unmet`,
  `timeout_scope FAIL … non-numeric constant`; runtime trace of the same
  function reads `120`.
- False reject: module `TIMEOUT = 120; if True: def helper(): TIMEOUT = 5`
  plus `timeout=TIMEOUT` → `static_checks` reports `name 'TIMEOUT' is
  conditionally rebound` although the module read is 120.
- False accept: module `TIMEOUT = 120`, outer `def f(): def inner(): global
  TIMEOUT; TIMEOUT = None; subprocess.run(..., timeout=TIMEOUT)` →
  `value_violations=[]`; the outer read is local `None`.

P-C10's "a binding inside the enclosing function shadows" is a Python-scope
claim; nested-function locals and nested `global` declarations are not
bindings of the enclosing function.

### F6 — Medium-low: `with` is added to the enumerated conditional constructs

P-C10 enumerates `if`/`try`/`for`/`while`; `_module_assignments` also treats
top-level `with` as conditional (`conform.py:227`), and the function
docstring says so (`conform.py:214`), while the check docstring omits it
(`conform.py:19-23`). This is stricter than the frozen words.

Probe `/tmp/probe-p8b.py` = module `TIMEOUT = 120`, top-level
`with open("/dev/null"): TIMEOUT = 60`, appended
`def _probe_with(): return subprocess.run(["true"], timeout=TIMEOUT)`:

```
check timeout_scope      FAIL (probe-p8b.py: … name 'TIMEOUT' is conditionally rebound)
CONFORM=unmet
EXIT=1
```

The counter executes with `TIMEOUT = 120` (traced) — an honest counter
rejected by a construct outside P-C10's list.

### F7 — Low: `drain_bind` rejects name bindings/consumption the words cover

`_popen_name` (`conform.py:309-316`) requires the `Popen` call's direct parent
to be a single-Name `Assign`; `_result_consumed` (`conform.py:318-338`)
requires `Assign`/`Return` with Name or all-Name tuple/list targets.
`static_checks` receipts (v2 verdicts from the same snippets):

| Shape | v3 `drain_violations` | v2 |
|---|---|---|
| `with subprocess.Popen(...) as proc: out, err = proc.communicate(timeout=5)` | `Popen … result not bound to a named variable` | accepted |
| `self.out, self.err = proc.communicate(timeout=5)` | `Popen … not drained by a bound, consumed communicate` | accepted |

P-C10 says "bound to the same name" and "assigned to other than `_`"; a
`with … as proc` binding and an attribute assignment are within those words.
`proc = other = Popen(...)` and `(proc,) = (Popen(...),)` are likewise
rejected. No effect on the counter of record, but a future counter change
could be rejected for reasons outside the predicate.

### F8 — Low: two docstring/behavior mismatches introduced by the v3 docstring

- `conform.py:12` says the `predicate` check compares "the contract's P-C10
  sentence"; `contract_predicate` (`conform.py:142`) extracts the **P-C7**
  blockquote from `DEFAULT_CONTRACT` (`conform.py:74`, round-39). Verified:
  `contract_predicate(round-39 contract)` → `P-C7: at revision R, the
  committed drift…`; `count-c8 --print-predicate` → `P-C7:`; the check passes.
  The docstring is wrong; the code is faithful to the round-39 nine.
- `conform.py:43-44` says the counter's scratch parent is under
  `.ufo/waves/round-40/scratch`; `static_checks` still requires the literal
  `"round-39"` (`conform.py:469-470`). Verified: `count-c8.py` carries
  `round-39` and the receipt says `root=True`; a source with a `round-40`
  `SCRATCH_ROOT` yields `scratch_root=False`. The documented behavior is not
  implemented; a counter moved to the documented path would fail.

### F9 — Residual: `selftest_conjunct` proxy and strip-regex coverage

`entry_live` (`conform.py:617-621`) is a substring check on
`inspect.getsource`; an entry returned by `selftest_mutations` but filtered
out of the `selftest` loop would still satisfy it (the independent
`pass=11` receipt catches that variant, so C1 is not falsified — this is the
proxy CritConjunctSemantics is attacking). The strip loop's regex
(`conform.py:624`) only matches `communicate(timeout=<no-parens>)` with the
timeout keyword last: `communicate(input=None, timeout=5)` yields
`strips=0`, and `communicate(timeout=max(1,2))` yields a `SetupError` that is
skipped, so `detected < strips` → false reject. The counter of record is
unaffected (`strips=6 detected=6`). Pre-existing, unchanged by v3:
`bounded_reads`' docstring claims every `communicate(` carries a timeout,
but `bounded_violations` only covers `run`/`check_output`/`check_call`;
communicate-timeout presence is enforced by `comm_violations` under
`selftest_conjunct`.

## Commands run and observed output

All paths relative to `/home/vgpnk/Projects/shokunin/mori-shokunin` unless
absolute.

1. Byte pinning:
   `git show bb1f2457:.ufo/waves/round-39/conform.py | sha256sum` →
   `fe0be179…7987` = extracted v2;
   `git show 265a955cc:.ufo/waves/round-40/conform.py | sha256sum` →
   `5025b966…3aaf` = `git show HEAD:…` = disk;
   `git show 265a955cc:.ufo/waves/round-40/count-c8.py | sha256sum` →
   `4e4d50eb…6da` = disk.
2. `python3 .ufo/waves/round-40/conform.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b`
   → all nine PASS, `CONFORM=met`, exit 0, 3.23 s.
3. `python3 .ufo/waves/round-40/conform.py 265a955cc… --selftest` → eleven
   PASS lines, `CONFORM_SELFTEST pass=11 fail=0`, exit 0, 57.23 s.
4. `python3 .ufo/waves/round-40/fixtures/generated/conform-v3-conjunct-gutted.py 265a955cc…`
   → `selftest_conjunct FAIL (… entry_live=False)`, `CONFORM=unmet`, exit 1.
5. `python3 .ufo/waves/round-40/conform.py 265a955cc… --counter .ufo/waves/round-40/count-c8.py --counter .ufo/waves/round-40/fixtures/generated/survivor-barecomm.py`
   → `drain_bind FAIL`, `selftest_conjunct FAIL` (per-counter comm_violation),
   `CONFORM=unmet`, exit 1.
6. Survivor sweep, one command per file
   (`python3 …conform.py 265a955cc… --counter <survivor>`): all ten exit 1,
   `CONFORM=unmet`; named FAILs: cond/inf/shadow-neg/shadow-none/divzero →
   `timeout_scope`; decoy/second-popen/tuple/underscore → `drain_bind`;
   barecomm → `drain_bind` + `timeout_state` + `selftest_conjunct`.
7. Static probes via `importlib` + `conform.static_checks` on constructed
   sources (v2 vs v3):

   | probe | v2 | v3 |
   |---|---|---|
   | conditional-only `NAME` | `name 'NAME' has no binding` | `[]` |
   | base + agreeing conditional | `[]` | `[]` |
   | local `None` then 120 | `name 'TIMEOUT' has no binding` | `[]` |
   | read before local assign | `name 'TIMEOUT' has no binding` | `[]` |
   | nested-function local | `[]` | `non-numeric constant` |
   | nested `global` + outer local `None` | `[]` | `[]` |
   | composite `TIMEOUT * 1` + local `None` | `[]` | `[]` |
   | top-level `with` binding ≠ base | `[]` | `conditionally rebound` |
   | with-as `Popen` | `[]` drain | `result not bound to a named variable` |
   | attribute-target communicate | `[]` drain | `not drained by a bound, consumed communicate` |
   | function `global TIMEOUT = None` | `[]` | `[]` |
   | tuple-unpacked `out, err = communicate` | `[]` | `[]` (expected) |
8. Full-checker probes (each `/tmp/probe-*.py` is a `count-c8.py` copy with
   one edit; `--counter /tmp/probe-X.py`):
   `p3` → met; `p1b` → met; `p1c` → met; `p7c` → met; `p11g` → met;
   `p5n` → unmet (`timeout_scope` FAIL); `p8b` → unmet (`timeout_scope`
   FAIL). Exit codes 0/1 as shown.
9. Runtime read-site traces: `P3 run() communicate timeout seen: [None]`;
   `P5n _probe_nested read timeout: [120]`; `P11g _probe_global read
   timeout: [None] | module TIMEOUT after call: None`; `P7c
   _probe_composite runtime error: TypeError …`.
10. `contract_predicate(round-39 contract)` → `P-C7: …`; v3 `PREDICATE` →
    `P-C10: …`; `count-c8` `PREDICATE = ("P-C7: …`; `static_checks` on a
    `round-40` `SCRATCH_ROOT` source → `scratch_root=False`, on a `round-39`
    source → `True`; `count-c8` → `True`.

## Residual risk and verification gaps

- C1's operational receipts are reproducible; the findings are against
  P-C10's universal wording, not against the counter of record or the nine
  declared survivors. If the round wants the predicate to mean only "the
  counter of record and the fixtures", P-C10 needs narrowing; if it wants
  the words, `timeout_scope` needs a read-site binding model (F1–F5) and
  `drain_bind` needs name-binding coverage (F7).
- I did not rerun the nine **before** (v2-on-survivor) controls; the
  committed `c10-red-*.txt` receipts and the v2 static comparisons above
  were used. I did not rerun the gutted-conjunct `--selftest` (57 s); I ran
  its non-selftest mode and rely on `c10-after-conjunct.txt` for the arm
  table.
- The gate/C2 side is out of scope for this seat. The wave's `--selftest`
  wall time is 57.23 s (default run 3.23 s); both are inside the wave's
  1 800 000 ms mechanical budget.
- Tools installed: none.
