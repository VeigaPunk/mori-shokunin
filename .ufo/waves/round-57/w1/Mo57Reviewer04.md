# Mo57Reviewer04 — C2 source interpretation review

## Finding — MED: `unclosed` is not a present-running count

The round-56 committed live receipt reports `mori.unclosed=10` and `in_flight=true` (`.ufo/waves/round-56/evidence/driver-liveness-live.txt:195-205,289-303`). The independent round-56 live-run report enumerates the exact unmatched keys as `[(2,None), (19,2), (20,1), (21,1), (22,1), (37,1), (38,1), (38,3), (40,1), (56,1)]` and says only `(56,1)` was current at that observation; nine were historical rounds 2–40 (`.ufo/waves/round-56/w1/Mo56ExecDriverLive.md:88-96`). Therefore ten pairings do **not** mean ten presently running tasks. Even the report's “only `(56,1)` currently-live” is time- and context-bound, not proof of process liveness: the tool reads the driver-authored log, not process state.

Source/code evidence: the entry explicitly says the values are pairing facts, “not health verdicts,” and that unclosed launch does not mean “stuck” (`corpus/knowledge/driver-liveness-r56.md:60-68`). The parser keys open launches by round and optional attempt (`tools/mori-driver-liveness.py:113-133`), closes matching keys on complete/wrap (`:116-120,134-150`), and reports `unclosed=len(open_launches)` (`:164-174`). The source docstring defines it as launches without same-round/attempt complete, “a pairing count, not a failure claim” (`tools/mori-driver-liveness.py:32-40`).

## Pairing semantics and counterexamples

- Same `(lane, round, attempt)` is the intended matching basis where attempt is present; omitted attempts use `None` (`tools/mori-driver-liveness.py:113-120,127-143`). Round is always part of the key, preventing a close in another round from clearing it.
- A `complete` line without an attempt is treated as `(round,None)`; it does not close keyed `(round,attempt)` launches (`:139-143`). A complete with an attempt closes that keyed launch, while an absent matching key changes no open pair (`:116-120`).
- Wrap closes the un-attempted round key (`:144-150`); it does not generally clear every attempt-keyed launch. Dead-no-report instead clears all open keys for that round (`:151-157`). These are log-event accounting rules, not process-liveness evidence.
- Explicit counterexample to reading count as active work: round-56 mori has nine historical unmatched pairs plus one recent pair, yet count is ten (`Mo56ExecDriverLive.md:90-96`). Another: `kagi` in the committed receipt has `unclosed=10` but `in_flight=false` (`driver-liveness-live.txt:63-73`); `kaidoku` has `unclosed=6` but `in_flight=false` (`:75-85`). Nonzero unclosed can coexist with the last event not being a launch. Conversely `in_flight` itself is only the last parsed event being a launch (`tools/mori-driver-liveness.py:164-173`), not authenticated process status.

## Verdict and residual risk

C2's required distinction is supported: `unclosed` counts unmatched log pairings, not currently running work. The committed report and entry are consistent on that point. Residual risk: the historical unmatched pairs can be misread if the count is shown without the pairing semantics; log rewriting, missing completion records, or driver events not represented in the parser can also make the count differ from actual runtime state. No host/process state was inferred. No production changes or commits made.

## Verification gaps

LSP status/references/definition/diagnostics could not be queried: no `lsp` device was exposed in this seat's tool inventory, so this review used the committed report, entry, receipt and implementation text. No tests or live command runs were performed. Scratch was prepared at `/fast/scratch/hyaku/mori-r57/Mo57Reviewer04`; no fixtures were created.