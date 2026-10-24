# RevC8Drain — `drain_shape` audit at `13bfba23b7ca063c76d3504a2ff6eb7b6a294932`

**Verdict: the assigned acceptance passes — both required variants FAIL `drain_shape`. The check is
nevertheless bypassable: `_ = proc.communicate(...)`, a discarded tuple `(proc.communicate(...), None)`,
an extra undrained `Popen`, and the exact r38 M19-B `wait(timeout=)`+`stdout.read()` drain (when paired
with any dummy used communicate in the same function) all print `drain_shape PASS` and `CONFORM=met`.**
`drain_shape` is existentially quantified over communicates, not universally over Popens, so the clause
"every `Popen(` … is drained in its own function by a `communicate(` … so a `wait(timeout=…)` plus
`stdout.read()` drain fails" (`conform.py:24-27`, `:70`) is not enforced by its own implementation.

Scored rev passed to the checker and to every counter: `13bfba2…`. Method: byte-copies of
`.ufo/waves/round-39/count-c7.py` in scratch, one edit each, run through the unmodified checker
(`python3 .ufo/waves/round-39/conform.py 13bfba2… --counter <copy>`). Full transcript:
`.ufo/waves/round-39/scratch/RevC8Drain/receipt.txt`; variants:
`.ufo/waves/round-39/scratch/RevC8Drain/*.py`.

## 1. Variant matrix (one run each, same checker, same rev)

| variant (scratch file) | edit vs `count-c7.py` bytes | `drain_shape` | other failing checks | `CONFORM` | exit |
|---|---|---|---|---|---|
| baseline `count-c7.py` | none | PASS `violations=[]` | — | `met` | 0 |
| **A2-diff-func-defaulted** | module-level `def drain(proc, timeout=TOOL_TIMEOUT_S)` (`:140-142`), `out, err = drain(proc, timeout)` (`:153`) — Popen at `:149` is drained **in another function** | **FAIL** `Popen at line 149 not drained by a used communicate in its function` | none | `unmet` | 1 |
| **B-bare-expr** | bare `proc.communicate(timeout=timeout)` at `:148` (parent `ast.Expr`) | **FAIL** `Popen at line 144 not drained by a used communicate in its function` | none | `unmet` | 1 |
| C-tuple *(bypass)* | `(proc.communicate(timeout=timeout), None)` at `:148` — result discarded | PASS `violations=[]` | none | **`met`** | 0 |
| C2-underscore *(bypass)* | `_ = proc.communicate(timeout=timeout)` at `:148` — result discarded | PASS `violations=[]` | none | **`met`** | 0 |
| E-second-popen *(bypass)* | `leftover = subprocess.Popen([... "-c","pass"], ...)` at `:147`, never waited/communicated | PASS `violations=[]` | none | **`met`** | 0 |
| E2-waitread-plus-dummy *(bypass)* | dummy `dummy_out, dummy_err = dummy.communicate(timeout=timeout)` at `:150`; real tool Popen (`:144`) drained by `proc.wait(timeout=timeout)` + `proc.stdout.read()` at `:152-153` | PASS `violations=[]` | none | **`met`** | 0 |
| F-no-timeout | `out, err = proc.communicate()` at `:148` | PASS `violations=[]` | `timeout_state` (`exit=None`, checker-side 25 s cap), `selftest_conjunct` (`honest_comm=['communicate without timeout at line 148']`) | `unmet` | 1 |
| A-diff-func (no default) | same as A2 but `def drain(proc, timeout)` | **FAIL** (line 149) | `timeout_value` (`line 141 … name 'timeout' has no binding`) | `unmet` | 1 |

A2/B are the assigned variants and both flip `drain_shape` to FAIL with that check as the **only**
failure — the rule is insufficient, not the counter. A2 isolates it by giving the helper parameter a
literal default so `timeout_value` also passes; without the default the same variant additionally trips
`timeout_value` (finding F5).

## 2. Findings

### F1 — HIGH: the M19-B shape passes. Any used `communicate` in the function drains *every* `Popen` in it
`conform.py:232-246` iterates `popens`, but the inner loop over `communicates` never binds a communicate
to a Popen object or variable; it breaks at the first used call in the same function (`:237` function
identity, `:240` parent-kind, `:241-243` break). E2 therefore keeps `proc.wait(timeout=timeout)` +
`proc.stdout.read()` on the tool child (`E2…py:152-153`) and adds a throwaway child whose result *is*
assigned (`:150`): `drain_shape PASS`, all nine checks PASS, `CONFORM=met`, exit 0. This directly
falsifies the check's own stated purpose at `conform.py:24-27` and the P-C8 clause "every `Popen(`
in the first counter is drained in its own function by a `communicate(` … so a `wait(timeout=…)` plus
`stdout.read()` drain fails" (`:70`). The later `except` path still communicates, so the hang fixture
behavioural check is unaffected — the static rule alone is defeated.

### F2 — HIGH: "result used" is over-approximated by parent node kind
`used = isinstance(parent, (ast.Assign, ast.Return, ast.Tuple))` (`conform.py:240`) treats *any* call
whose parent is a tuple or assignment as a used drain. Two one-line rewrites pass:
`(proc.communicate(timeout=timeout), None)` (parent `ast.Tuple`, result discarded — variant C) and
`_ = proc.communicate(timeout=timeout)` (parent `ast.Assign`, `_` discard — variant C2). Both are
"communicate result unused" by intent, both yield `drain_shape PASS` and `CONFORM=met` (receipt
`### C-tuple`, `### C2-underscore`). The assigned variant B fails only because its parent is exactly
`ast.Expr`; the rule discriminates the syntactic form, not result use.

### F3 — MEDIUM: an undrained `Popen` passes when the same function has any used communicate
Variant E adds `leftover = subprocess.Popen(..., stdout=PIPE, stderr=PIPE, text=True)` in `run_tool`
(`E…py:147`) and never waits or communicates it; the tool Popen at `:144` is normally drained. Result:
`drain_shape PASS`, `CONFORM=met`. The rule is per-function, not per-Popen, so a counter may spawn an
unreaped child (zombie / unflushed pipe) while satisfying the check. This is the same root cause as F1
(no dataflow binding), isolated to the "every Popen" wording.

### F4 — LOW (spec vs. implementation): `drain_shape` ignores whether the communicate carries a timeout
Variant F's `out, err = proc.communicate()` passes `drain_shape` and `bounded_reads`; it is caught only
behaviourally (`timeout_state` hit the checker's 25 s cap — `exit=None` — and `selftest_conjunct` saw
`comm_violations`). P-C8 assigns "a `communicate(` carrying its own timeout" to `drain_shape`, but
`comm_violations` (`conform.py:268-277`) is consumed only by `selftest_conjunct` (`:408,:416`). The overall
`CONFORM=unmet` verdict is still correct; the per-check attribution in the predicate does not match the
code. Adjacent (likely another seat's scope): the module docstring `conform.py:26-27` says stripping the
communicate timeout flips exactly `bounded_reads`, while `selftest()` expects failing `==
["selftest_conjunct"]` (`:495-505`) and variant F confirms `bounded_reads` stays PASS.

### F5 — LOW: `_resolve` cannot see a required positional argument
`_resolve` (`conform.py:115-126`) consults only module-level assignments and *parameter defaults*
(`:121-123`), so factoring the drain into `def drain(proc, timeout)` fails `timeout_value` with
`name 'timeout' has no binding` even though the call site passes `timeout`, which resolves to
`TOOL_TIMEOUT_S`. Defensible under a literal reading of P-C8 ("resolves through module-level assignments
to a positive numeric literal"), but it makes the rule hostile to any helper signature without a default
and is why the naive required variant A fails two checks instead of one.

## 3. Residual risk and verification gaps

- The bypasses defeat `drain_shape` only; C1/C2/C3 exit-code claims on the *claimed* bytes are untouched
  — C/E/E2 are not the honest bytes and not the two M19 fixtures. C2 as stated (`CONFORM=met` on
  `count-c7.py`, fixtures rejected) survives this audit; the *contract's* `drain_shape` clause does not.
- `--selftest` has no mutation covering these classes: nine textual replacements, none adds a second
  `Popen`, wraps communicate in a tuple, or assigns to `_`. `CONFORM_SELFTEST pass=9 fail=0`
  (`evidence/c8-after-selftest.txt`) is therefore compatible with all four bypasses. I did not run
  `--selftest` myself; that evidence is another seat's and I only read it.
- `drain_shape` is static and first-counter-only (`conform.py:364-367`); no runtime corroboration exists
  that the drained child's result is ever consumed. No narrowing was observed on the true bytes
  (baseline `violations=[]` above matches `evidence/c8-after.txt:8`).
- Lane `HEAD` moved during the audit (`20260b0c…` → `eb986a9e…` → `ecb8a11…`) as peers wrote reports;
  `head_pin` compares the counter's measured pin against live `HEAD`, so it passed in every run. My
  variant runs passed `13bfba2…` explicitly, and `drain_shape` is revision-independent (pure static read
  of the `--counter` bytes), so no verdict here depends on the moving tip.
- Environment/installs: none. No tool version changed; no `pacman` transaction attempted.
- Write discipline: this report is the only file written. Scratch is confined to
  `.ufo/waves/round-39/scratch/RevC8Drain/` (7 variant `.py` + `receipt.txt`). The lane's real
  `conform.py`/`count-c7.py` were never edited (`git status --porcelain` shows only pre-existing
  untracked scratch/reports); no `git`/`jj` mutation was run.
