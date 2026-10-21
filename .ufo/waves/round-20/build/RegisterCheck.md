# RegisterCheck findings

## Changed file and behavior

- Added `.ufo/waves/round-20/build/RegisterCheck/check-register.py` (stdlib Python). It accepts `REGISTER DRIFT_STDOUT`; raw `MORI_DRIFT:` stdout and a JSON capture containing a string `stdout` are supported. See `check-register.py:9-17,31-45,90-119`.
- Validates the required `mori-drift-classification-v1` schema, the closed class set, and non-blank `reason` / `evidence` strings. Invalid register entries are counted and do not classify drift tokens; a regression class on a drift token is counted even if its entry is otherwise invalid. Usage/read failures return 2; otherwise it prints the requested summary and returns 0 only when all three failure counts are zero. See `check-register.py:48-87,101-119`.
- Old-style bare-string token entries are invalid, not classifications.

## Requested self-check

Command:

```text
python3 .ufo/waves/round-20/build/RegisterCheck/check-register.py .ufo/waves/round-13/evidence/drift-classification.json .ufo/waves/round-20/evidence/c1-drift-entering.json
```

Observed stdout:

```text
MORI_DRIFT_REGISTER: unclassified=50 invalid=43 regression=0 tokens=50
```

Observed exit code: `1` (the supplied r13 register is the legacy bare-string form, has no required schema marker, and does not validly classify the measured drift). The input capture records 50 tokens and its `stdout` at `round-20/evidence/c1-drift-entering.json:10-11`; the old register has bare-string entries at `round-13/evidence/drift-classification.json:5-48`. The checker’s schema/entry validation and summary/exit logic are at `check-register.py:48-87,109-119`.

## Risks and blockers

- The requested legacy-register self-check was run; no valid v1 register or passing zero-count case was supplied or exercised. No build, lint, formatter, or broader tests were run.
- No blocker. No tools were installed.
