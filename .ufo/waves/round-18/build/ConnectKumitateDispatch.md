# C3 sibling-overlap scan: dispatch payload binding

## Axes

- **C3 operability / provenance:** make each top-level wave task-call attempt auditable against the committed payload.
- **Province boundary clarity:** preserve kumitate ownership of dispatch/orchestration while making Mori's measurement-only role explicit.
- **Reuse / no duplication:** consume existing dispatch and slot evidence rather than recreate dispatch, slot, or settlement machinery.

## Finding

**[INFERENCE] Split ownership:** C3's per-attempt *binding and measurement* belongs in Mori's observability surface; the action it observes—wave planning, slot acquisition, task invocation, dispatch-result production, and orchestration settlement—remains kumitate/operator-owned. This is not a transfer of orchestration semantics to Mori. Mori's current province says it owns read-only probes and wave settlement state, refuses dispatch/orchestration mechanism, and reports rather than remediates (`PROVINCE.md:6-16,22-23`). Kumitate's province declares orchestration/tooling and rejects cross-domain absorption (`../kumitate-shokunin/PROVINCE.md:3-6`).

The frozen C3 claim makes the bounded measurement explicit: a read-only verifier counts attempt rows whose payload digest/byte count/task count do not bind to the committed dispatch JSON, and it checks ledger ordering/result constraints (`.ufo/waves/round-18/contract.md:18,39-43`; `.ufo/waves/round-18/frozen/c3-ledger-format.json:4-21`). The payload is the validated `{context,tasks}` call, not an orchestration policy. C3 also explicitly limits the claim: hashing the committed payload does **not** prove the task tool received those exact bytes, beyond the L1 copying them unchanged and returned IDs matching the registry (`frozen/c3-ledger-format.json:21`).

## Overlap and distinctions

- **Direct orchestration overlap (kumitate):** its documented swarm producer validates/plans and emits the batched dispatch payload, persists registry/dispatch artifacts, and records returned agent IDs; the consumer joins settled outcomes to dispatch members (`../kumitate-shokunin/SKILL.md:37-62`; `../kumitate-shokunin/corpus/knowledge/swarm-wave-lifecycle.md:47-53,74-92,98-138`). These are the operational producer/consumer semantics; Mori should not create a second producer, collector, or outcome taxonomy.
- **Similar word, different counter:** kumitate's queue `attempts` are task-key claim-scoped dispatch tries across repends; `resumeAttempts` and `launchMisses` are distinct queue counters. They are not C3's sequential records for attempts to issue one validated wave task-call payload (`../kumitate-shokunin/corpus/knowledge/queue-and-claim.md:90-110`).
- **Similar record, different unit:** kumitate's native resilient attempt ledger and pre-spawn `dispatch_attempts` describe per-seat fallback/completion and seats that never spawned. Its `native_dispatch_topology` evidence validates transcript-observed task-call/result pairing, roster coverage, and wave-token behavior. These are native judged-round contracts, not the C3 per-wave committed-payload digest ledger (`../kumitate-shokunin/corpus/knowledge/native-transcript-ledger-seats.md:68-141,143-198`). They are a useful adjacent precedent, but not a drop-in C3 verifier or a reason to move the C3 measurement into kumitate.

## Instrument to reuse

Reuse the already-produced `wave-slot.sh acquire` grant only as the C3 row's `slot_grant` observation: the frozen format explicitly defines that field as this attempt's `granted` line or null (`frozen/c3-ledger-format.json:14`; `../scripts/hyaku/wave-slot.sh:8-11,67-79`). Do not make Mori invoke `acquire`/`release`, change the slot ledger, or reinterpret capacity; those are operational effects outside Mori. For dispatch and outcome membership, consume the existing committed dispatch/registry/results artifacts rather than rebuilding kumitate's `ufo-swarm-wave` / `ufo-swarm-collect` behavior.

No inspected kumitate corpus entry specifies a drop-in instrument that recomputes the C3 `{context,tasks}` digest and checks this exact per-call ledger format. The native transcript topology proof is complementary evidence, not a substitute for that committed-payload check. **[INFERENCE]** Keep the C3 verifier Mori-owned and use only the existing slot-grant fact as an input.

## Boundary Mori should state in `PROVINCE.md`

Suggested bounded addition to the kumitate row in the Adjacent table (do not change the dispatch owner):

> Kumitate owns wave/task plan, run, record, collect, slot acquisition, OMP task invocation, and orchestration/result semantics. Mori may passively verify the C3 per-attempt ledger against the already committed dispatch payload and report unbound rows and ledger-shape findings; it does not author or alter the payload/ledger, acquire or release slots, call OMP, retry or settle agents, or decide dispatch/refusal outcomes. The digest binds the committed payload to the ledger only; it does not attest to bytes received by the task tool.

This resolves the apparent tension between the current broad “refuses dispatch and orchestration mechanism” boundary and C3 rows that record observed `refused` / `started` / `partial` outcomes: recording and checking evidence is observational; performing, retrying, or adjudicating dispatch remains out of Mori's province (`PROVINCE.md:12-16`; `frozen/c3-ledger-format.json:14-21`). Preserve any refusal text as ledger data required by the frozen schema, but keep Mori's verifier/report output privacy-safe and non-echoing, consistent with the frozen tool-output rule (`contract.md:45-53`).

## Risks / no-harm check

- **Boundary drift:** if “attempt ledger” is left unqualified, queue claim counts, native per-seat retries, transcript dispatch proofs, and C3 per-wave payload receipts can be conflated. Keep the unit explicit: one validated whole-wave task call per C3 row.
- **False assurance:** do not describe a digest match as proof OMP received or executed the bytes; the frozen C3 limit forbids that claim (`frozen/c3-ledger-format.json:21`).
- **Instrumentation collision:** do not duplicate kumitate's producer/collector or mutate the operator slot gate. The proposed move adds only a passive evidence boundary and reuses the existing grant observation.
- **Axes:** improves C3 provenance clarity and province boundary clarity; no effect on C1 retention or C2 freeze-order claims. No contradiction is hidden: Mori can measure dispatch evidence without owning the dispatch operation, but the current PROVINCE wording does not yet say that specifically.

## Verification and provenance

Read-only evidence collected from the round contract, frozen C3 format, both province/skill/corpus surfaces, and `scripts/hyaku/wave-slot.sh`; the requested corpus searches for `dispatch`, `attempt`, `refus`, and `payload` returned relevant matches cited above. No repository files other than this report were written; no tests, builds, tools, or slot operations were run. The `read`/`grep` tools report retrieved content rather than shell exit statuses, so no shell command exit codes apply. No URLs were consulted; no tooling was installed or updated.