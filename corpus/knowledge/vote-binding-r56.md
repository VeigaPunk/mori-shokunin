# Vote binding across seat-output shapes (round 56)

source: S545 (RFC 8259 — the JSON grammar the JSON channel parses; section labels corrected by S546)
verified-at: 2026-10-27 (live fetch, `corpus/evidence/sources-r56/rfc8259.txt`, sha256 `61a5378f…`)
recheck: on-release
coverage-map: new capability — seat-output vote binding (no prior lane note)

## The failure class

Round 55 C1 (freshness, 78-row v7.3 recheck ledger) landed **unmet on its vote
arm with every data arm green**, cause (1): the frozen C1 counter bound an
agreeing vote only when the voter's captured output contained the exact
`RECHECK <h> <w>` line as a stripped *text* line
(`.ufo/waves/round-55/count-c1.py:286-301`). All fifteen reporting RECHECK
voters emitted structured JSON yields whose string arrays quote the vote
lines — under varying keys: `vote_lines` on 2 of 15 seats, `votes` on 9,
`final_vote_lines` on 3, `final_votes` and `voteLines` on 1 each — so
stripped-line equality failed for every one of them and the counter read
`voted=0`. (The binder walks every string scalar, which is why the key
variation does not matter to it.) The same round's C2 counter binds by
substring and accepted the identical shape (`entailed=15`) — the two counters
disagreed on the same bytes because they implemented "contains" differently.
The operator's run-10 binding note for exactly this incident: freeze a parser
that accepts both shapes, or bind on files the seat writes.

## The frozen rule (tools/mori-vote-bind.py)

One parser, two channels, chosen per document and never mixed:

* **JSON channel** — if the whole output parses as a JSON value, the vote
  surface is the document's string scalars, walked in document order. A scalar
  binds iff its *stripped content* matches the vote grammar anchored at the
  start: `<verb> <hash12> <word> [<rest>]`, verb `RECHECK|ENTAIL`, hash exactly
  12 lowercase hex, word `[A-Za-z][A-Za-z0-9_-]*`. This is the RFC 8259
  grammar reading: `A JSON text is a serialized value.` (S545 §2, line 251)
  and that value may be `false / null / true / object / array / number /
  string` (S545 §3 grammar, line 308), while a string is
  `string = quotation-mark *char quotation-mark` (S545 §7, line 461) — so a
  seat's vote surface in a JSON yield is the set of string scalars, and a
  scalar that merely *contains* a vote sentence ("the claim is RECHECK …
  holds today") is prose, not a vote. That anchoring is the overclaim guard a
  loose substring binding lacks. (S546 carries the corrected section labels;
  S545's line numbers and quotes were always true substrings.)
* **text channel** — otherwise the output is read as lines; fenced blocks are
  skipped; an unfenced stripped line binds by the same anchored grammar.
* Last write wins per (verb, hash) inside the chosen channel; the channel that
  fired is recorded per vote.

Binding unit: the orchestrator-captured final output (`output` field of the
seat's result record). A report file is not required — the captured output is
the seat's final text no matter where the orchestrator stored it.

## Measured on the round-55 bytes

`python3 tools/mori-vote-bind.py tally --ledger corpus/knowledge/kernel-v7.3-recheck-r55.md --results .ufo/waves/round-55/w1-results.json --verb RECHECK --voter Mo55Rc01 … Mo55Rc16`
over the **committed** round-55 artifacts prints:

    TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15

The identical bytes under the frozen round-55 C1 counter print `voted=0`
(receipt `evidence/c2-old-counter-voted0.txt`). Both readings are receipts,
not interpretations; the difference they measure is the binding shape: under
the round-55 metric's own ≥2-voter rule the dual-shape reading takes 68 rows
to quorum (from 0), while the 10 remaining rows stay single-voted — the
dispatch-coverage hole the round-55 lesson records (rows assigned to
Mo55Rc13+Mo55Rc14, the latter settling with no votes), surfaced honestly by
the binder's `single=10` instead of zeroing the arm. A unanimous-but-wrong
vote set would still read `dissent=0` (the tally counts inter-voter
disagreement only) — a named limit, not a quorum guarantee.

## Limits (named before data)

* The binder proves a captured output *carried* a vote line, not who authored
  the bytes — the round-55 limit on results-binding carries over unchanged.
* Exact-scalar binding rejects a seat that buries its vote mid-sentence; the
  run-10 alternative (bind on files the seat writes) remains available for a
  seat that refuses the plain formats.
* A JSON doc whose votes sit in a scalar with a leading fence marker does not
  bind (the anchored grammar rejects a ```-prefixed scalar); such a shape was
  never observed.
* The tally re-binds history; it does not re-run voters. New votes must still
  come from dispatched seats.
