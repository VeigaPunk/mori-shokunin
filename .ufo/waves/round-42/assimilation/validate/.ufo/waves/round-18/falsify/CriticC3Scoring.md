# C3 scoring attack

## Verdict

Score C3 as a **capability row only**, not an operability improvement. The frozen before population is the round-17 wave-1/wave-2 legacy receipts; the after population is round-18 attempt ledgers (`.ufo/waves/round-18/contract.md:39-43`; `.ufo/waves/round-18/frozen/c3-ledger-format.json:20`). These are different runs and formats. The nine legacy rows are unbound because they lack the new payload identity, not because nine observed deliveries failed. The round-18 contrast establishes adoption of a new ledger capability, not a causal or normalized improvement in delivery performance (`build/CriticC3Operability.md:7-9,13-14`; `corpus/knowledge/dispatch-ledger-r18.md:33-35`).

The capability claim must be stated narrowly: a supplied ledger row can be checked against the payload projection committed at its `dispatch_path`. The frozen rule binds the digest, byte count, and task count to that committed artifact; it does not establish that the task tool received those exact arguments or that every real attempt was logged (`frozen/c3-ledger-format.json:4-5,19-21`; `build/CriticC3Operability.md:15-19`; `corpus/knowledge/dispatch-ledger-r18.md:29-32`). Thus, external receipt and completeness remain unverified, without making the narrower capability wholly unverified. The implementer report records 11/11 selftest arms, including payload tampering and missing-start settlement cases, but its recorded CLI verification is for the round-17 baseline, not the current residual ledger (`build/DispatchLedger.md:19-23`).

## Counterexample and refused-only ledger

The residual-drafting ledger is not a successful or cleanly settled wave: its current file contains seven attempt rows, all refused, with zero started IDs (`residual-drafting-attempts.json:1-94`). That is consistent with the `STARTED_MISSING` state in the provisional C3 row (`draft-verdicts.md:10`): the frozen clean-ledger rule requires exactly one `started` or `partial` row and requires it to be last (`frozen/c3-ledger-format.json:19`). Therefore, the refusal-only ledger cannot demonstrate successful dispatch or an improvement in task delivery.

But `STARTED_MISSING` is a settlement finding, not an unbound-payload finding. A refused attempt is still an attempt whose committed payload can be bound. If the verifier accepts each row's digest/length/count, those refused rows do **not** count against the frozen C3 metric (unbound rows); they demonstrate the refusal-path ledger capability, not successful operability. Keep the two results separate rather than treating `STARTED_MISSING` as either a hash mismatch or proof of end-to-end receipt.

There is also population drift in the draft: it reports the residual call as 5/5 bound, while the current residual ledger has seven rows (`draft-verdicts.md:10`; `residual-drafting-attempts.json:1-94`). The current tree also has a wave-2 attempts ledger with a refused attempt followed by a started attempt (`wave2-attempts.json:1-27`), which was not part of the draft's pre-wave-2 snapshot (`draft-verdicts.md:1,10`). The as-measured after set must be enumerated and checked at one revision; do not carry the earlier 5/5 count forward as the current population. I did not independently rerun the verifier, so I make no claim that the two additional residual rows have been checked as bound.

## Impacted axes

- **Operability:** no comparative improvement is established. The round-17 and round-18 populations differ, and the residual call had no successful settlement.
- **Capability:** supported narrowly as payload-to-committed-ledger binding, subject to verifying the complete current after set.
- **Evidence provenance/completeness:** actual task-tool receipt and omitted-attempt detection are not established by this ledger format, as the critique and knowledge note identify.
- **C1 adjacency / C2 calibration:** no conclusion follows; this counterexample is confined to C3 (`build/CriticC3Operability.md:9`).

## Smallest safe correction

Keep the frozen inputs intact. In the score, label C3 **capability acquisition only**, explicitly exclude a before/after improvement claim, and define the demonstrated boundary as matching ledger rows to committed payload projections. Reconcile the current row counts and included files (including whether the residual and wave-2 ledgers are in the measured set), then report `STARTED_MISSING` separately from the unbound-row count. Leave task-tool receipt and complete attempt coverage unverified until independent invocation evidence exists; do not label refused rows unbound solely because no attempt started.

## Review evidence

Read-only review of the cited contract, frozen C3 format, draft verdicts, critique, implementation report, knowledge note, and current attempt ledgers. No commands, verifier, selftest, build, or external URLs were run; no tooling was installed or updated.