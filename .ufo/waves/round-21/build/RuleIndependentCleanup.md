# RuleIndependentCleanup review

## Finding — low: no positive audit acceptance case for independent `cleanup-accounted`

The contract permits an explicitly evidenced per-wave `cleanup-accounted` disposition for a `disposed` row (`.ufo/waves/round-21/contract.md:14`) while C1 keeps baseline acceptance blocked only while disposition is unknown (`contract.md:7`). So a valid independent cleanup-accounting record may permit Mori's own census-baseline acceptance without establishing that the wave settled. The contract separately says this repair is not proof of settlement (`contract.md:7,27`), and the current province clarification limits “acceptance” to Mori's census baseline and says an audit `disposed` row is not lifecycle settlement, result acceptance, or a reap/re-dispatch licence (`PROVINCE.md:175-181`). That distinction is honest as written.

The concrete uncovered case is a required wave with a valid, hash-bound independent record explicitly saying `disposition: cleanup-accounted`, while the wave's lifecycle outcome remains unknown. The frozen `loss-independent-cleanup` row only exercises `classify` with `independent_disposition: true` and expects `live-state`/`pin_allowed: true` (`.ufo/waves/round-21/frozen/cases.json:21-26`); it does not exercise `audit` parsing the typed enum or its resulting baseline gate. The self-test requirement names an unknown disposition but no valid cleanup-accounted audit case (`contract.md:16`). Thus the current specified checks do not demonstrate that this permitted disposition can clear only the baseline-loss blocker and remain distinct from settlement.

**Smallest safe change:** add one isolated `audit --selftest` positive fixture with a required observation and a valid independent `cleanup-accounted` disposition (distinct from the cleanup actor). Assert the row is accounted (`disposed`), `unresolved` is zero, and `pin_allowed` is true only for Mori's own census baseline; keep the wave settlement outcome unknown and make no lifecycle-settlement claim. Keep the existing classifier case separate: its boolean decision is not a typed audit-enum test.

No live row should be changed on this basis: the retained accounting still has both historical identities `unresolved` with `independent_disposition: null` (`corpus/evidence/loss-accounting-r21.json:3-45`), and the provenance explicitly says settlement is unknown (`.ufo/waves/round-21/evidence/historical-provenance.json:38-40`).

## Residual risk and verification gaps

- The CLI implementation is not present in the listed `tools/` files yet; this was a before-implementation contract review, so no behavior was executed and no tests were run.
- No `lsp` device is mounted (`xd://lsp` returned “No such tool”); the cited contract and lane text were read directly. Literal search results were used only to locate the relevant text, not as semantic proof.
- Actor identity / independence remains declared evidence requiring outside adjudication, not something Mori's hash check authenticates (`PROVINCE.md:180-181`).
