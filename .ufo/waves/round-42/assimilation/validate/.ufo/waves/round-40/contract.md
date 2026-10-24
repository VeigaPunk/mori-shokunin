# mori round 40 — frozen contract (L1 mori-r40, attempt 1)

Entering tip: `bb1f2457bb8d3e8d5dfe98488b91e8c02e378ca3` (round 39 admitted;
closure `corpus/lessons/round-39-verifier-spotcheck.md`).
Frozen before any data seat or data receipt: this contract, `count-c8.py`
(the round-40 counter bytes), `conform.py` (round-40 version, v3), the
modified `tools/mori-sources-appendonly.py` (the tracked gate, version 3),
the fixture builders and the survivor-fixture payloads. Pins are recorded in
`evidence/freeze-r40.txt` (sha256 over the frozen paths). A change to a
predicate after this freeze is a new counter version, not an edit. The
round-39 instruments under `.ufo/waves/round-39/` stay byte-frozen at their
commits; their receipts remain valid at their frozen commits. Before receipts
run the round-39/v2 bytes extracted via `git show bb1f2457:<path>`.

## Routed inputs this round discharges (r39 closure routed defects 1–4 + lesson findings)

- Finding 11 / routed defect 1 (C2 drain-shape before-control not reproducible;
  report+SCORECARD "bypass-wait likewise → CONFORM=met" wording): the drain
  half is re-claimed with a genuine before-control — the decoy-communicate
  fixture is accepted by the round-39 checker and rejected by the round-40
  checker via `drain_bind`. The wording defect is corrected by
  `corpus/lessons/round-39-erratum.md` (append-only; the r39 fleet report is
  committed fleet history, outside lane write scope).
- Findings 4/8/12 (C2 name-not-value survivors): function-local shadow,
  module-level conditional rebind, decoy/underscore/tuple/second-Popen drain
  bypasses, `1e400` inf, fold crashes as exit 2, conjunct kill rule not read
  from the checker's own mutation list, multi-counter comm_violations
  first-counter-only. → claim C1.
- Findings 2/5 (C3 gate eligible set edit-bounded; first-parent-lacks-path
  second-parent fall-through; "18 ids + S226" prose unreachable; linear
  re-add corner). → claim C2.
- Finding 1 (P-C7 prose "between the honest and mutated runs" exceeds the
  code): narrowed reading recorded in the r39 erratum — the code compares the
  mutant run's got table against the arm's expected (want) table, drawn at run
  time; a wording fix needs no re-freeze.
- Finding 7/10 (r39 contract `pass=11` prose stale; before-cell cites
  `fixtures/make-ancestry-dags.py`, a path in no commit): corrected in this
  contract's citations (r39 bytes stay frozen; corrections are append-only
  notes in the erratum).
- Spotcheck routed defect 4 (lesson Gate labels S227 quote 18 words, actual
  17): corrected in the erratum.
- SimpCounters D1–D4 (~16 dead lines across count-c7/conform): applied to the
  round-40 counter/checker copies (the r39 bytes stay frozen); behavior
  byte-identical including both selftests.
- Debt (f) (SIGTERM/grace tradeoff): OPEN, operator-owned — not worked this
  round.

## Claims

### C1 — operability (7): conformance v3 — scope-aware timeout resolution and per-Popen drain binding (r39 w1 findings 4/8/12)

Round 39's `timeout_value` resolves a `timeout=` name from the module
top-level `Assign` map with no regard for the read site, so a function-local
`TIMEOUT = None` shadow and a module-level conditional rebind
(`if cond: NAME = None`) both pass with a runtime-None drain; it accepts
`1e400` (not finite) and turns `1/0` / `A = A` into exit-2 setup errors.
Round 39's `drain_shape` is existentially quantified over communicates, never
binds a communicate to a Popen, and treats tuple-wrapped or `_`-assigned
results as used, so the r38-M19-B `wait(timeout=…)`+`stdout.read()` drain
passes beside any decoy used communicate, an undrained second `Popen(` passes,
and the drain half of the r38 claim never had a genuine before-control
(lesson finding 11). Its `selftest_conjunct` never reads the checker's own
mutation list (gutting the entry still selftests green) and audits
`comm_violations` for the first counter only.

**P-C10 (frozen, verbatim in `conform.py`'s PREDICATE and in the report):**

> P-C10: at revision R, the round-40 conformance checker passes all nine checks on the round-40 counter bytes — the round-39 nine with three made sound — `timeout_scope` (every `timeout=` keyword in every counter resolves in the scope of its read site: a binding inside the enclosing function shadows the module map, a `global` rebinding is read at module scope, a module-level binding nested in `if`/`try`/`for`/`while` makes the name conditionally rebound and fails closed, and the value must be a finite positive number, so `1e400` fails and a fold raising `ZeroDivisionError` or `RecursionError` fails as a violation, not a setup error), `drain_bind` (every `Popen(` in every counter is drained in its own function by a `communicate(` bound to the same name, carrying its own timeout, with the result consumed — assigned to other than `_`, or returned — so a `wait(timeout=…)` plus `stdout.read()` drain fails even beside a decoy used communicate, an undrained second `Popen(` fails, and a tuple-wrapped or `_`-assigned communicate does not qualify), and `selftest_conjunct` (per counter: the counter's communicates all carry timeouts, stripping each communicate timeout one at a time is detected by that same rule, and the checker's own textual-mutation table carries a live `selftest_conjunct` entry whose anchor occurs in the counter — comm_violations are computed and reported per counter, not for the first counter only) — and the checker's `--selftest` applies eleven textual mutations to the counter of record, each flipping exactly its own check to FAIL.

Counter of record: `.ufo/waves/round-40/count-c8.py` (round-39 `count-c7.py`
bytes minus the sixteen dead lines of SimpCounters D1–D4; printed receipts
byte-identical, proven in `evidence/c10-parity.txt`). The first `--counter`
is the instrument under behavioural test; every `--counter` is audited
statically.

**Before** (measured at the entering tip `bb1f2457`, before any data seat):
the round-39 checker bytes (`git show bb1f2457:.ufo/waves/round-39/conform.py`)
print `CONFORM=met` exit 0 on nine survivor fixtures
(`fixtures/make-survivor-fixtures.py` output):
`evidence/c10-red-shadow-none.txt`, `c10-red-shadow-neg.txt`,
`c10-red-cond.txt`, `c10-red-inf.txt` (met),
`c10-red-divzero.txt` (exit 2, no FAIL line), `c10-red-decoy.txt`,
`c10-red-underscore.txt`, `c10-red-second-popen.txt`, `c10-red-tuple.txt`;
`CONFORM=met` on a two-counter audit whose second counter's communicate lacks
a timeout (`c10-red-multicounter.txt`); and a checker copy with the
`("selftest_conjunct", …)` entry gutted from its own mutation table still
prints `CONFORM_SELFTEST pass=8 fail=0` (`c10-red-conjunct.txt`).
**After** (declared): `python3 .ufo/waves/round-40/conform.py <landed tip>`
on the counter of record prints `CONFORM=met` exit 0 (`evidence/c10-after.txt`),
`--selftest` prints `CONFORM_SELFTEST pass=11 fail=0` with each mutation
flipping exactly its own check (`c10-after-selftest.txt`), each of the nine
survivor fixtures prints `CONFORM=unmet` with the named new check FAIL
(`c10-after-<fixture>.txt`), the gutted-conjunct checker copy fails
`selftest_conjunct` (`c10-after-conjunct.txt`), and the two-counter audit
fails with per-counter comm_violations (`c10-after-multicounter.txt`).

Kill rule: a do-nothing control cannot print `CONFORM=met`; a checker that
only adds function-local shadowing still accepts the decoy drain →
`CONFORM=unmet`; a v3 whose own mutation table lacks the
`selftest_conjunct` entry fails `selftest_conjunct`; a v3 selftest with fewer
than eleven arms prints a different `pass=` count than the frozen receipt.

### C2 — depth (5, tied lowest): gate v3 — supersede eligible set and first-parent reference (r39 w1 findings 2/5)

Round 39's `supersede_timing` eligible set is edit-bounded
(`superseded = cid for cid in ids if cid in sup_map`), so a never-edited
superseded row (S226, superseded by S228) never reaches the as-of/stale test
although P-C9's words cover it (its last immutable-cell edit is its landing
commit); the contract's "18 ids + S226 once S228 lands" prose is therefore
unreachable. Its edit reference falls through to a later parent when the
first parent lacks the path, contradicting "against its first parent's
state", and a linear delete-then-re-add contributes a `changed` event v1
never printed, so "on linear histories v1 and v2 agree byte-for-byte"
overclaims. This round makes the gate compute what the predicate says and
pins the two corners the words left open.

**P-C11 (frozen, verbatim in the gate's PREDICATE and in the report):**

> P-C11: at revision R, tools/mori-sources-appendonly.py reports, after its summary line, `supersede_timing superseded_as_of=[...] stale_supersede=[...]`; the timing line's eligible set is every superseded id present at R — a never-edited superseded id's last immutable-cell edit is its first-sighting commit, so it reaches the as-of/stale test — and an edit at a commit is a change against its first parent's state only: when the first parent lacks the path the commit contributes no edits (a delete-then-re-add contributes no changed event; ids still compare tip cells against first-sighting cells), never a fall-through to another parent's state; the lane-history verdicts are unchanged except the eligible-set extension — S226 joins superseded_as_of (19 ids) at the landed tip, no id is stale at the tip, S069 is stale at e37dcc6 — and the selftest carries committed fixtures for a never-edited superseded row (as-of), a merge whose first parent lacks the path (no fabricated edit), and a linear delete-then-re-add (no changed event).

Gate: `tracked tools/mori-sources-appendonly.py`, version 3. The output
format (per-id lines, `appendonly_violations` summary, `supersede_timing`
line) is byte-identical in shape to v2.

**Before** (measured at the entering tip): the v2 gate bytes print
`supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S069,S179,S180,
S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] stale_supersede=[]` — 18
ids, S226 absent (`evidence/c11-before-lane.txt`); on the fixture DAGs built
by `fixtures/run-c11-dags.py` the v2 gate omits the never-edited superseded
row from the timing line (`c11-red-neveredited.txt`), fabricates a `changed`
line plus a stale verdict on the first-parent-lacks-path merge
(`c11-red-firstparent.txt`), and prints a `changed` event for the linear
delete-then-re-add (`c11-red-readd.txt`).
**After** (declared): `python3 tools/mori-sources-appendonly.py --selftest`
prints `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0`
(`c11-after-selftest.txt`); on the lane at the landed tip the gate prints
`supersede_timing superseded_as_of=[19 ids incl. S226] stale_supersede=[]`
(`c11-after-lane.txt`) and at `e37dcc6` prints `stale_supersede=[S069]`
(`c11-after-e37dcc6.txt`); the three fixture DAGs print the P-C11 verdicts
(`c11-after-fixture-n.txt`, `c11-after-fixture-p.txt`,
`c11-after-fixture-r.txt`).

Kill rule: a do-nothing control cannot print the fixture verdicts; a gate
keeping the edit-bounded eligible set still omits S226 → the lane line
mismatches the declared 19 ids; a gate with the second-parent fall-through
fabricates the merge-fixture edit → the frozen fixture fails; a gate keeping
the re-add changed event fails fixture R.

## P-C10/P-C11 evidence paths

`evidence/freeze-r40.txt`, `evidence/census-start.txt`, `census-end.txt`,
`evidence/c10-red-*.txt`, `c10-after*.txt`, `evidence/c11-red-*.txt`,
`c11-before-lane.txt`, `c11-after*.txt`.

## Claim-admission hygiene (r38/r39 lessons)

Targets are one command over committed bytes each; no universal clauses; the
before receipts name the exact instrument bytes they ran (v2 bytes extracted
via `git show bb1f2457:<path>`) and are recorded before any data seat runs;
the do-nothing control for C1 is the round-39 checker on the round-40
survivor fixtures (it prints `met` where v3 must print `unmet`); for C2 it is
the round-39 gate bytes on the round-40 fixture DAGs (predicate-word
verdicts). Receipts name the measured revision (r39 lesson finding 9
discipline).

Sourced claim: C1 rests on S229 (Python execution model — naming and binding;
`corpus/knowledge/conform-scope-r40.md`), opened this round: function blocks
bind names locally, which is why the scope-aware fold must read a function
binding before the module map.

Round shape: ONE v2 wave of 64 seats (policy v2 band 64–128, ≥25% attack
roles), dispatched as exactly ONE task call carrying the validator's
taskCall. §3 L2 floor inside the single wave; the canonical planner seat is
the L1 (validator rejects `planner`; orchestrator ruling 2026-10-19).
