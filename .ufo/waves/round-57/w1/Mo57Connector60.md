# Mo57Connector60 — `unclosed` interpretation / boundary check

## Verdict

**No-harm boundary holds only for the narrow interpretation: `unclosed` is an unmatched-event pairing count, not a live-process count, failure verdict, or kumitate settlement status.** C2 remains unmet on current evidence: its frozen predicate explicitly needs eight quote-located claims in a newly opened source copy (`.ufo/waves/round-57/contract.md:7`), while the available watchdog grammar copy is round 56. Do not imply this finding establishes the required source or claims.

## Evidence and counterexamples

- Contract scope is C1 calibration and C2 depth; it explicitly says “No axis score delta asserted” (`.ufo/waves/round-57/contract.md:3,5-9`). C2's target is interpretation/limits of the field, not watchdog health or settlement.
- Probe docstring defines `unclosed` as “launches with no same-(lane,round,attempt) complete — a pairing count, not a failure claim” (`tools/mori-driver-liveness.py:32-40`). The implementation emits `len(row["open_launches"])` at `:164-174`; the separate `in_flight` field is simply whether the lane's last event was a launch (`:172-173`), not a process query. The report repeats that these are “log-shape facts, not health verdicts” (`:237-242`).
- Concrete counterexample to “unclosed means running”: a launch with no later matching complete produces an open pairing, but the probe does not inspect a PID or query process liveness; its outputs are derived from parsed records (`:122-163`). Conversely, a process could stop after launch and before complete while the pairing remains open. Thus the count alone cannot distinguish running, exited, or unreported completion. This is an inference from the documented data path, not an assertion about any particular provider.
- A `lane-dead-no-report` event clears open launches for that round and records a dead event (`:151-157`); therefore the count is not simply cumulative launches-minus-completes either. It tracks the parser's pairing state after event-specific transitions.
- The available source copy lists writer forms for launch, complete, lane-dead-no-report, launch-fail, and wrap (`corpus/evidence/sources-r56/watchdog-log-grammar-v2.txt:1-11`). These are evidence about log grammar, not proof that a launch's process is alive or dead. It is not a newly opened round-57 source; do not pass it off as satisfying C2.
- Boundary cross-check: the prior explicit mori↔kumitate analysis says kumitate settlement consumes operator-supplied `ufo-swarm-results-v1` statuses and maps them into mission-result outcomes, unlike mori's lane/driver-round pairing (`.ufo/waves/round-56/w1/Mo56ConnKumitate.md:28-42,137-172`). The apparent `in_flight` homonym is a real lexical risk, but not shared authority/semantics. It must not be used to claim a lane round is accepted, settled, healthy, or a member outcome.

## Contradictions and bounded recommendation

No source evidence supports the contradiction “unclosed == present-running.” It directly conflicts with the frozen definition at `tools/mori-driver-liveness.py:34-36,172-173`. The other important distinction is that this pairing count is distinct from the `in_flight` last-event boolean; even that boolean is a log fact, not a process check. Preserve both distinctions whenever describing the fields. This may strengthen depth/calibration of an explanation without claiming an axis score change or C2 completion. No edits to production, contract, or counters; no settlement semantics inferred.

**Verification:** inspected the frozen contract, implementation and source-copy lines listed above, plus the prior boundary analysis. No runtime checks or mutations performed. The cited `Mo56ConnKumitate.md` is corroborating prior analysis, not independently reverified kumitate source in this seat.

Report: .ufo/waves/round-57/w1/Mo57Connector60.md
