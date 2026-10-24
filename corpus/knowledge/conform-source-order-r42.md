# Why the conformance checker sorts binding events: walk order is unspecified

source: S347 — https://docs.python.org/3/library/ast.html#ast.walk — §ast.walk — Python 3 documentation (docs.python.org, current CPython 3.x)
source: S230 — Python 3.13 language reference §7.2 assignment statements (opened round 41; grounds the binding-inventory semantics)
verified-at: 2026-10-24
recheck: 90d — `curl -fsSL https://docs.python.org/3/library/ast.html | grep -c 'no specified order'` -> 1 (ran 2026-10-24)
coverage-map: SKILL conformance checker (round-42 C1, operability)
ground: round-42 claim C1 — the three surviving round-41 checker-mutation lanes

### Claim

`ast.walk` documents that it yields descendant nodes "in no specified order",
and child traversal follows field order, not source order. A binding
inventory built by walking a function therefore cannot rely on construction
order to be source order: the checker's fallback sweep records comprehension
targets after every main-loop event regardless of line, so an unsorted
inventory can report a later `value` binding before an earlier comprehension
target.

### What the checker does with this

The inventory sorts its events by `(lineno, col_offset)` before returning,
and the round-42 `timeout_scope_source_order` selftest arm pins the
consequence: on the committed source-order fixture (a comprehension target
at the earlier line, a `None` value binding at the later line) the first
failing-binding reason must be the comprehension target's `unsupported
local store`. Deleting the event ordering (the surviving `sort-deletion`
mutant) makes the checker report the `None` binding first (`non-numeric
constant`) — a different first reason for the same counter — and the arm
fails.

### Boundaries

- The sort fixes the *reported first event* and deterministic ordering of
  kind checks only; it is not a control-flow proof, and the v4 semantics
  (all binding events count; any non-value kind fails closed) are unchanged.
- `lineno`/`col_offset` carry no runtime path sensitivity; an event's
  position says nothing about execution order and the checker never claims
  it does.

### What it changes for mori

The third surviving round-41 checker-mutation lane (sort deletion) is killed
by an arm whose ground is a documented stdlib guarantee rather than an
implementation accident. If the stdlib ever specifies walk order, this
row's justification changes and the row is superseded, never edited.
