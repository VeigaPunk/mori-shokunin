measured 2026-10-23T09:12:09Z

# JudgeRowsR19 — mori round-19 register row judgment

Scope: one row, key `rounds[398].capabilities_added[0]`, in the final `## Capabilities`
section of SCORECARD.md at lane tip cedb0ec4f3a4f672804deac388b7191258f01fcd.
Decision rule quoted verbatim from `.ufo/waves/round-35/evidence/c1-controls.txt:41-44`
(non-empty, closure-faithful capability/what cells; evidence cells holding only
backticked paths). Non-author judgment: this seat did not write the register.

## Row under test

SCORECARD.md:1968 @ cedb0ec4:

```
| `rounds[398].capabilities_added[0]` | blob-bound content-review coverage gate | Passes 10/10 frozen finite requirements; on the actual 194-path population it exits 1 with 155 unresolved dispositions, so it is not privacy clearance. | `tools/mori-content-review.py` | 19 |
```

## Closure record (what the row must be faithful to)

Fleet `MANIFEST.json@37b51a24`, `rounds[398]`:

- `capabilities_added[0]`:
  "bounded blob-bound content-review coverage gate: 10/10 frozen finite
  requirements; the actual 194-path population remains RED, exit 1, with 155
  unresolved dispositions, not privacy clearance"
- `rounds[398].admitted = true`, `verdicts.adjacency = "improved"`,
  `lane_rounds.mori = 19`, `report = .ufo/reports/round-19/mori.md`.
- `verification.rechecks`: "Independently executed report jq counting commands:
  C1 capability_absent [10,0] ... All 194 unique population paths equal review
  rows and all 194 blob hashes match HEAD. Decisions retain35/minimized4/
  unresolved155 ... Actual committed-population receipt exit1, findings155
  exclusively CONTENT_REVIEW_UNRESOLVED; red preserved, no privacy-clearance
  claim." (truncated at 768 bytes in my read; substance cited above observed)

Fleet report `.ufo/reports/round-19/mori.md@37b51a24`: C1 described as "a bounded,
blob-bound content-review coverage gate that refuses missing/stale/unresolved/
provenance-only clearance"; "Actual committed-population run:194/194 blobs and
review rows,155 `CONTENT_REVIEW_UNRESOLVED`, exit1. This is a correct negative
observation, not a failed-clearance result disguised as green."

Lane lesson `corpus/lessons/round-19.md@2061780117e6` (spot-check per
`verification.spotcheck`): lines ~235-237 — "The actual194-path gate reads and
binds all194 blobs but returns exit1 for155 unresolved dispositions:151
provenance-only/unreviewed and4 reviewed unresolved. Missing reviews were never
replaced with fabricated successful workers or semantic clearance."

## (a) capability and what cells, sentence by sentence

Capability cell "blob-bound content-review coverage gate":
- Drops the leading adjective "bounded" from the MANIFEST name
  ("bounded blob-bound content-review coverage gate"). This is a truncation of
  the label, not an added fact; the bound is preserved in the what cell
  ("frozen finite requirements", "actual 194-path population"). No fact the
  record does not state is introduced. Not a defect under the rule; noted as a
  residual nit.

What cell, claim by claim:
1. "Passes 10/10 frozen finite requirements" — record: "10/10 frozen finite
   requirements" (MANIFEST capabilities_added[0]); "C1 capability_absent [10,0]"
   (verification.rechecks); "After10/10 match" (report C1). Faithful; "passes"
   is implied by an admitted capability claim. Bound preserved: finite frozen
   requirements, not live clearance.
2. "on the actual 194-path population it exits 1" — record: "the actual
   194-path population remains RED, exit 1" (capabilities_added[0]); "Actual
   committed-population receipt exit1" (verification.rechecks). Faithful;
   RED≡exit 1 restated without loss.
3. "with 155 unresolved dispositions" — record: "155 unresolved dispositions"
   (capabilities_added[0]); "findings155 exclusively CONTENT_REVIEW_UNRESOLVED"
   (verification.rechecks). Faithful, exact count.
4. "so it is not privacy clearance" — record: "not privacy clearance"
   (capabilities_added[0]); "no privacy-clearance claim" (verification.rechecks).
   Faithful; the cell preserves the record's negative bound rather than
   overstating the tool as a cleaner.

No cell fact exceeds or contradicts the record; non-empty.

## (b) evidence cell

`` `tools/mori-content-review.py` `` — a single backticked path, nothing else in
the cell. Satisfies "only backticked paths". The path exists at tip and at the
closure commit (cat-file -t returns blob at 2061780117e6).

## (c) pointer relevance at closure commit 2061780117e6 (outside the rule)

`tools/mori-content-review.py` @ 20617801 implements exactly this capability:
- line 2 docstring: "Bounded, content-based review gate for the frozen Mori
  population."
- lines 26-42: INVALID_CODES / FAIL_CODES incl. CONTENT_REVIEW_UNRESOLVED,
  CONTENT_REVIEW_STALE, CONTENT_REVIEW_INCOMPLETE — the refuse-missing/stale/
  unresolved behavior the record claims.
- lines 176-199 finish(): exit 1 on fail findings, exit 0 clean, exit 2
  could-not-evaluate — the "exit 1" the row and record state.
- lines ~415-430 selftest: 10 named finite cases (complete_safe,
  missing_review, duplicate_review, unknown_decision, digest_drift,
  private_content, provenance_only, out_of_population, invalid_revision,
  tampered_population_pin) — the "10 frozen finite requirements" population.
- Blob binding: read_blob + blob_sha256 verification against the frozen
  mori-content-population-v1 pin (lines 16, 55-56, 132-140).

It is the artifact for THIS capability (round-19 C1), not a different round-19
artifact (the C2 freeze-order work lives in `tools/mori-freeze-order.py`).

## Verdicts

VERDICT: rounds[398].capabilities_added[0] supported
VERDICT: rounds[398].capabilities_added[0] pointer-relevance holds

Reasons: what cell restates every MANIFEST bound (10/10 finite, 194-path
population RED/exit 1, 155 unresolved, no privacy clearance) with no added or
inflated fact; evidence cell is one backticked path; the pointed file at the
closure commit is the implementing gate itself. Residual nit (not a defect
under the rule): capability cell truncates the MANIFEST name's leading
"bounded".

## Checks run (commands, all read-only in the lane)

- `git -C <lane> show cedb0ec4:SCORECARD.md` → row at line 1968; final
  `## Capabilities` section begins line 1941.
- `git -C <fleet> show 37b51a24:MANIFEST.json` → rounds[398] parsed (JSON above).
- `git -C <fleet> show 37b51a24:.ufo/reports/round-19/mori.md` → C1 narrative.
- `git -C <lane> show 2061780117e6:tools/mori-content-review.py` (493 lines) and
  `cat-file -t` → blob exists; implementation matches claim.
- `git -C <lane> show 2061780117e6:corpus/lessons/round-19.md` → lesson
  corroborates 194/155/exit1 figures.

No installs performed; no lane writes other than this report.
