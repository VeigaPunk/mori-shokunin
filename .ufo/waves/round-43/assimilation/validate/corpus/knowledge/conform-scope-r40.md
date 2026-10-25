# conform-scope-r40 — why the timeout fold is scope-aware

source: S229 — Python execution model, Naming and binding
(https://docs.python.org/3/reference/executionmodel.html#naming-and-binding,
copy `corpus/evidence/sources-r40/S229.src`)
verified-at: 2026-10-24
recheck: on-release

Round 39's `timeout_value` check resolved every `timeout=` keyword from the
module top-level assignment map. Round-39 wave-1 finding 4 (RevC8Value)
reproduced two survivors at the frozen bytes: a function-local
`TIMEOUT = None` shadow and a module-level conditional rebind
(`if cond: NAME = None`) both passed with a runtime-None drain.

Python's execution model is why the module map is not enough (S229 §4.2.2):
"When a name is used in a code block, it is resolved using the nearest
enclosing scope." An assignment anywhere in a function block binds the name
locally for the entire block, so a read of `TIMEOUT` inside `run()` resolves
to the function-local binding even when a module-level `TIMEOUT = 120`
exists. The round-40 checker's `_resolve_timeout_name` therefore models
exactly three cases, in this order:

1. a binding inside the enclosing function shadows the module map for every
   read in that block (function-local `TIMEOUT = None` fails);
2. an explicit `global` sends the read to module scope;
3. a module-level binding nested in `if`/`try`/`for`/`while`/`with` makes the
   name conditionally rebound and fails closed unless every binding agrees
   on one finite positive value.

The value itself must fold to a finite positive number: `1e400` (a float
`inf`) fails, and a fold raising `ZeroDivisionError`/`RecursionError` is a
violation of this check, not a checker setup error (round-39 exit-2 gap).

The same nearest-scope principle grounds the drain half (finding 8): a
`communicate(` bound to the name a `Popen(` result was assigned to is the
drain *of that Popen*, not of every Popen in the function; an existential
"some used communicate exists" reading is the wrong scope for the rule.

Used by claim C1 of round 40 (`.ufo/waves/round-40/contract.md`, P-C10);
evidence receipts under `.ufo/waves/round-40/evidence/c10-*.txt`.
