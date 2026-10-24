# RevC5Selftest — `conform.py --selftest` six-mutation re-derivation (round 38, w2)

Verdict: **PASS 6/6** — every mutation is a single-line, non-whitespace change and
flips exactly its own declared check to FAIL. No mutation is a no-op; no second
check flips on any mutant.

## Method (all read-only against the lane; mutants on scratch copies only)

1. Ran the canonical command at the scored tip (HEAD == f725f30…, confirmed via
   `git rev-parse HEAD`):
   `python3 .ufo/waves/round-38/conform.py f725f3076972e6e70595b5ac8279be524a111ff8 --selftest --counter .ufo/waves/round-38/count-c1.py`
   → `CONFORM_SELFTEST pass=6 fail=0`, exit 0 (matches `evidence/c5-after-selftest.txt`;
   also `pass=6 fail=0` without `--counter`, i.e. default counters).
2. Re-derived the pristine baseline:
   `conform.py <rev> --counter count-c1.py --counter count-c4.py` → all six checks
   PASS, `CONFORM=met`, exit 0.
3. Independent inspection: `scratch/RevC5Selftest/inspect_mutations.py` extracts
   the literal `mutations = [...]` table out of `selftest()` in `conform.py` via
   `ast.literal_eval` (so the table under test is the checker's own, not a hand
   copy), applies `source.replace(old, new, 1)` to copies of `count-c1.py` under
   `scratch/RevC5Selftest/mutants/`, byte-diffs each mutant vs pristine, and runs
   `conform.evaluate()` on every mutant to observe which of the six checks flip.

## Per-mutation results

| mutation | anchor occurrences | line changed | expected check | observed flip(s) | verdict |
|---|---|---|---|---|---|
| predicate | 1 | 65 | predicate | predicate | PASS |
| head_pin | **5** | 951 | head_pin | head_pin | PASS |
| tool_resolve | 1 | 918 | tool_resolve | tool_resolve | PASS |
| bounded_reads | 1 | 136 | bounded_reads | bounded_reads | PASS |
| timeout_state | 1 | 959 | timeout_state | timeout_state | PASS |
| scratch | 1 | 70 | scratch | scratch | PASS |

Diff evidence (each mutant differs from pristine in exactly one non-whitespace line):

- `predicate` — `65: "head_at_measurement=<40-hex>." → "lane_tip=<40-hex>."`;
  failing detail `predicate=exit=0 equal=False`. The `<40-hex>.` token lives only
  in the P-C1 predicate bytes; the `head_pin` regex keys on
  `head_at_measurement=<40-hex>` per-line output of `--pin-only`, so no crosstalk.
- `head_pin` — `951: print("head_at_measurement=%s" → print("head=%s"`;
  detail `head_pin=pin=None tip=f725f30…`. The anchor occurs 5× in
  `count-c1.py` (lines 951, 997, 1008, 1035, 1125); `replace(…, 1)` hits line 951,
  which **is** the `--pin-only` handler (`count-c1.py:950-952`) — the correct
  kill site. See residual risk on positional fragility.
- `tool_resolve` — `918: return os.path.abspath(os.path.join(…)) → return path`;
  detail `tool_resolve=exit=0 resolved=.ufo/waves/round-38/fixtures/summary-only.py`
  (relative, non-absolute → check fails). `timeout_state` unaffected because it
  passes an absolute `HANG_FIXTURE` path, taking the `isabs` branch untouched.
- `bounded_reads` — `136: run(["git","-C",repo]+list(args), timeout=timeout, …)
  → run(…, env=clean_env())`; detail `run=False` via the AST keyword scan
  (`static_checks`, `conform.py:110-111`). Note: the counter's `run()` helper
  defaults `timeout=120` (`count-c1.py:109`), so the mutant's git child is still
  bounded at runtime — the check enforces the *explicit-kwarg* contract at every
  `run(` call, and the mutation violates it honestly. No masking: the check
  still fails exactly where declared.
- `timeout_state` — `959: _TOOL_BUDGET[0] = max(1, args.tool_timeout) →
  = TOOL_TIMEOUT_S`; detail `timeout_state=exit=None timeout_reason=False
  pass=False`. The mutant ignores `--tool-timeout 3` and lets the hang fixture
  run under the 120 s default, exceeding the checker's own 25 s subprocess bound
  (`conform.py:185`) — killed before it can print `tool_timeout` *or*
  `real arm: pass`. A correct kill of the check's intent (the mutant never
  yields `tool_timeout`); the failure shape is the outer bound, not counter
  output — worth knowing, not a defect.
- `scratch` — `70: SCRATCH_ROOT = os.path.join(DEFAULT_REPO, ".ufo", "waves",
  "round-38", "scratch") → "/tmp/mori-r38-scratch"`; detail `mkdtemp_dir=True
  root=False`. The static check reads the assignment's literal args
  (`conform.py:118-124`), so the `/tmp` literal fails `root=` while `dir=`
  kwargs stay intact. Runtime `_scratch_parent()` (`count-c1.py:898-911`) would
  silently fall back to `/tmp` anyway, so the static check is the only line of
  defense — and it fires.

## Findings

- **PASS (6/6, tally `pass=6 fail=0`, exit 0).** Both acceptance criteria met:
  no whitespace-only mutation, no second check flips on any mutant.
- **LOW / informational:** bare `python3 .ufo/waves/round-38/conform.py
  --selftest` (no `rev`) exits 2 with `conformance setup error: expected str,
  bytes or os.PathLike object, not NoneType` — `rev` is `nargs="?"` and
  `evaluate()` feeds `None` into the `timeout_state` argv (`conform.py:184-185`).
  The docstring shows `<rev> [--selftest]`; the scored claim C2 commands the
  non-selftest form (`conform.py <rev> --counter … --counter …`), so the claim
  is unaffected, but the crash surfaces as a raw TypeError rather than a clean
  usage error.

## Residual risk / verification gaps

- `head_pin` mutation correctness is position-dependent: if a future
  `print("head_at_measurement=%s"` were inserted before line 951,
  `replace(…, 1)` would hit a non-probe site and `head_pin` would *not* flip —
  producing a spurious selftest FAIL (safe direction: false alarm, not false
  pass).
- `timeout_state`'s mutant fails via the checker's 25 s outer bound, so a
  future relaxation of that bound could let a misbehaving counter run longer;
  currently the bound is the honest discriminator.
- Independent re-derivation used the checker's own `evaluate()` on my own mutant
  copies — the mutations and their application were extracted/applied by my
  harness, but per-check semantics are the checker's (that is what C2 claims to
  test).

## Tooling

No installs or upgrades performed (pacman transactions paused host-wide);
`python3` and `git` already present sufficed.

## Bounds

Lane read-only except: this report (`.ufo/waves/round-38/w2/RevC5Selftest.md`)
and scratch artifacts under `.ufo/waves/round-38/scratch/RevC5Selftest/`
(`inspect_mutations.py`, six mutant copies). The selftest's own `mkdtemp` work
dir (`mori-conform-selftest-*`) is created and removed by the checker itself.
