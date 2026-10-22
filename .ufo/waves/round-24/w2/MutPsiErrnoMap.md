# Wave 2 falsify — MoriR24.MutPsiErrnoMap

Round 24 (attempt 2), wave 2, C2 (`tools/mori-pressure.py` selftest sensitivity).
Seat: MoriR24.MutPsiErrnoMap. Leaf, no subagents.

Target commit: `a730ecfefbdb5c31b1db13aca2c40eecd5e97abc` (detached checkout of the
measured lane tip), cloned with `git clone --no-hardlinks` from the lane into
`/fast/scratch/hyaku/mori-r24-a2/w2/MutPsiErrnoMap/mori-shokunin/`.

## Probe

Two single-statement mutants of `_state_for_oserror` (`tools/mori-pressure.py:135-148`),
each flipping the smallest behavior-bearing point of an errno mapping:

- Mutant A: EOPNOTSUPP maps to `absent` (instead of `unsupported`) — line 142.
- Mutant B: EACCES maps to `ok` (instead of `unreadable`) — line 144.

Detector: `python3 -I tools/mori-pressure.py --selftest` on the clone at the target tip
(same bounded detector on pristine, mutated, restored bytes).

## Results

| Stage | Hash (sha256, tools/mori-pressure.py) | Detector output | Exit | Verdict |
|---|---|---|---|---|
| Pristine baseline | `852d1ea7508004dc44690bb6e358625fbd07d89c26d4196793133559d8a773a5` | `MORI_PRESSURE_SELFTEST: PASS 12/12` | 0 | baseline OK (declared after-value re-derived) |
| Mutant A (EOPNOTSUPP -> absent) | `95921519ac2a371541a95177c78bcf9141e47bec6b8a18b150352a0f1721dd18` | `MORI_PRESSURE_SELFTEST: FAIL 11/12`; `P05: cpu.state is 'absent', expected 'unsupported'; memory.state is 'absent', expected 'unsupported'; io.state is 'absent', expected 'unsupported'; irq.state is 'absent', expected 'unsupported'` | 1 | **KILLED by P05** |
| Restored after A | `852d1ea7508004dc44690bb6e358625fbd07d89c26d4196793133559d8a773a5` (`cmp` clean) | `MORI_PRESSURE_SELFTEST: PASS 12/12` | 0 | restored bytes = pristine |
| Mutant B (EACCES -> ok) | `c69b6e96794ef5c41e3a4d76489321abc3a5c37e6f112a5cd72bd70fcb08802a` | `MORI_PRESSURE_SELFTEST: FAIL 11/12`; `P10: verdict PRESSURE_OK != PRESSURE_PARTIAL; io.state is 'ok', expected 'unreadable'` | 1 | **KILLED by P10** |
| Restored after B | `852d1ea7508004dc44690bb6e358625fbd07d89c26d4196793133559d8a773a5` (`cmp` clean) | `MORI_PRESSURE_SELFTEST: PASS 12/12` | 0 | restored bytes = pristine |

Both mutants are killed; neither survives. The frozen cases pin each mapping exactly:

- P05 (`tools/fixtures/mori-pressure/cases.json:136-162`) injects EOPNOTSUPP on all four
  resources and expects per-resource `state: "unsupported"` for each of cpu/memory/io/irq
  (plus verdict `PRESSURE_UNAVAILABLE`, exit 2). `_case_failures`
  (`tools/mori-pressure.py:461-486`) compares the state string, so a
  EOPNOTSUPP->absent mapping fails on all four state assertions.
- P10 (`cases.json:279-304`) injects EACCES on io and expects `io.state: "unreadable"`
  plus verdict `PRESSURE_PARTIAL`; the mutant flips the verdict to `PRESSURE_OK` and
  `io.state` to `ok`, failing both checks.

## Coverage observation (not a contract violation)

The frozen injection corpus only exercises ENOENT (P04), EOPNOTSUPP (P05) and EACCES
(P10). The `EPERM -> unreadable` branch (`tools/mori-pressure.py:145-146`) and the
unknown-errno fallback (`:147-148`) are never exercised by any frozen case (no case
injects `EPERM` or an unmapped token; `error_aliases` default is `EIO`, still unused).
An EPERM->ok mutant would be expected to survive today. This is a coverage gap report,
not a claim that the contract is violated.

## No tool installs

No tool installations/updates were performed (the tool is pure stdlib; nothing was
needed). No host writes, no registry/PSI triggers, no service changes. The lane repo
was touched only by this report file.
