# MutPsiMatcher — wave 2 falsify report (round 24, attempt 2)

Seat: `MoriR24.MutPsiMatcher` (leaf mutation tester). Lane tip measured: `a730ecfefbdb5c31b1db13aca2c40eecd5e97abc` (branch master). Target claim: C2 — `tools/mori-pressure.py` selftest, `MORI_PRESSURE_SELFTEST: PASS 12/12` over `tools/fixtures/mori-pressure/cases.json`.

## Mutant

Single smallest behavior-bearing point in `tools/mori-pressure.py`, function `_case_failures` (the selftest matcher): disable the `findings_include` enforcement gate — "findings_include ignored".

Pristine (line 491):

```python
        if not any(f.get("id") == fid and f.get("resource") == resource for f in payload.get("findings") or []):
```

Mutated (line 491):

```python
        if False:
```

All other bytes identical. This is a pure permissiveness increase: the matcher never flags a missing finding pair, so `findings_include` expectations are ignored.

## Detector runs (python3 -I tools/mori-pressure.py --selftest, from clone root)

| Run | File SHA-256 | Output | exit |
|---|---|---|---|
| Pristine | `852d1ea7508004dc44690bb6e358625fbd07d89c26d4196793133559d8a773a5` | `MORI_PRESSURE_SELFTEST: PASS 12/12` | 0 |
| Mutated | `2057e4d2062640f1020e181e8baa9d70091f705f556ff195a05993041df70dd0` | `MORI_PRESSURE_SELFTEST: PASS 12/12` | 0 |
| Restored | `852d1ea7508004dc44690bb6e358625fbd07d89c26d4196793133559d8a773a5` (== pristine) | `MORI_PRESSURE_SELFTEST: PASS 12/12` | 0 |

Restoration evidence: `git checkout -- tools/mori-pressure.py` in the scratch clone; restored SHA-256 equals the pristine backup (`mori-pressure.pristine.py`, same hash) and the baseline hash; selftest re-run passes. Lane repo was never touched (read-only; no git/jj mutating commands). Pristine copy kept at `/fast/scratch/hyaku/mori-r24-a2/w2/MutPsiMatcher/mori-pressure.pristine.py`.

## Verdict: MUTANT SURVIVED

The frozen cases do not kill the weakened matcher. Mutated and pristine runs are byte-identical (`PASS 12/12`, exit 0), even though the `findings_include` check is fully disabled.

Reason: the corpus is entirely positive. `_case_failures` is only ever exercised with outputs that satisfy every expectation — cases P06 and P07 declare `findings_include` pairs (`[["PRESSURE_HIGH", "memory"]]`, `[["PRESSURE_HIGH", "irq"]]`), but in both the tool genuinely emits those findings, so the strict check passes and disabling it is unobservable. No case asserts the negative branch: expecting a finding that must NOT be present (or that the injected snapshots fail to produce).

## Missing case (precise, not edited)

A case whose `expect.findings_include` is non-empty while its `snapshots`/`errors` are crafted so the tool's emitted `findings` lacks that pair — e.g. id e.g. `P13`, `args: []`, snapshots with all four resources below the local threshold (verdict `PRESSURE_OK`), `expect: {"exit": 0, "verdict": "PRESSURE_OK", "resources": {...ok...}, "findings_include": [["PRESSURE_HIGH", "memory"]]}`. Under the strict matcher that case fails (`finding PRESSURE_HIGH on memory missing`); under the mutated matcher it passes — killing the mutant via a `FAIL 11/12` vs `PASS 12/12` divergence. The current 12-case corpus has no such negative case.

## Note on the sibling variant

The alternative weakening "subset match always true" (e.g. neutralizing the some/full missing-key or value-equality checks at lines 477–481) would survive for the same structural reason: every `expect.resources` block matches the correct tool output exactly, so any permissiveness increase is invisible. Same missing-case class: each resource expectation needs a negative counterpart (a case where the tool's emitted resource omits/mismatches an expected field under the strict matcher).

## Tooling record

No installs or updates were performed; `python3` was already present. No new tools beyond the existing shell/read/edit/write set.

## Evidence paths

- Pristine run: clone root, `python3 -I tools/mori-pressure.py --selftest` → `PASS 12/12`, exit 0.
- Mutated run: same command after one-line edit → `PASS 12/12`, exit 0.
- Restored run: same command after `git checkout -- tools/mori-pressure.py` → `PASS 12/12`, exit 0; SHA-256 matches pristine `852d1ea7...`.
- Mutation site: `tools/mori-pressure.py:491` (was: `if not any(... findings_include ...)`; now: `if False:`).
