# Mo59Critic30 — C2 artifact-set scope challenge

Seat question: are the r54–r58 `w1-results.json` files (plus the single r53
drift file) the right artifact set for the C2 scan/drift/pin arms?

Verdict: **adversarial finding — under-coverage + inconsistent set
definition.** No byte/pin counterexample: the landed build's pinned copies and
entry claims verify. The defect is in what the frozen arms *certify*, not in
what they currently measure. Pin-gated (frozen bytes), so this is a fixable
defect for a later round, not a kill-rule trigger.

## Method (bounded)

1. Read frozen contract + `count-c2.py` (`ARTIFACTS`/`REAL_SCAN`/`DRIFT_SCAN`,
   lines 55–76; scan/drift/tree arms lines 219–281).
2. Confirmed working-tree tool `tools/mori-settlement-scan.py` sha256 =
   `4c04bf21…5ac9a9` = frozen `PIN` (lane tip `8ff344ff`).
3. Enumerated every `*results*.json`/`*settlement*.json` under `.ufo/waves/`
   (`find`, rounds 13–58), then ran the **pinned tool itself** on each
   candidate (read-only; scan writes nothing).
4. Verified member key-set uniformity and sha256 of every landed
   `corpus/evidence/sources-r59/` copy against its `.ufo` original.

## Evidence

### A. REAL set — the r54–r58 window is under-inclusive and least-diverse

Conforming `ufo-wave-results` objects committed in the lane (all scan
`SETTLEMENT_SCAN_OK`, exit 0, against the pinned tool):

| file | seats | wave | verdict |
|---|---|---|---|
| round-47/w1-results.json | 45 | w1 | OK (omitted) |
| round-47/w2-results.json | 37 | w2 | OK (omitted) |
| round-48/w1-results.json | 55 | w1 | OK (omitted) |
| round-48/w2-results.json | 34 | w2 | OK (omitted) |
| round-50/a2w1-results.json | 64 | a2w1 | OK (omitted) |
| round-51/w1-results.json | 60 | w1 | OK (omitted) |
| round-52/w1-results.json | 50 | w1 | OK (omitted) |
| round-53/a2r1-results.json | 8 | a2r1 | OK (omitted) |
| round-54..58/w1-results.json ×5 | 74,64,64,64,64 | w1 | OK (**REAL_SCAN**) |

Command: `python3 tools/mori-settlement-scan.py <file>` →
`"verdict":"SETTLEMENT_SCAN_OK"` for all eight omitted files.

So the frozen REAL set is 5 of 13 committed conforming artifacts (38%). The
omitted eight are exactly the diversity: second-wave (`w2`), attempt-2
(`a2w1`, `a2r1`), and seat counts 8/34/37/45/50/55/60 vs the frozen set's
uniform w1 + near-uniform 64 seats. Nothing in the contract explains the
r54–r58 boundary; `contract.md:78` calls them "the five r54–r58 wave-results
files," framing a contiguous window as if canonical. Provenance: results files
begin at round 47; rounds 46 and 49 have none; the r53→r54 gap is the
`report_file` drift. r54–r58 is a recency slice, not a schema boundary —
conforming shape reaches back to r47.

### B. DRIFT set — one file covering 1 of 12 committed FAIL artifacts

`DRIFT_SCAN = [".ufo/waves/round-53/w1-results.json"]` only
(`count-c2.py:76`). Committed settlement-named artifacts that scan FAIL under
the pinned tool (measured, `exit=1`, `SETTLEMENT_SCAN_FAIL`):

- r53/w1-results.json — `extra_keys=report_file` on all 67 members (**the
  only one tested**)
- r17/wave-settlement.json — `results_not_list, seats_mismatch, lane_bad,
  wave_bad`
- r19/wave{1,2}-settlement.json — same top-level failures
- r20/evidence/wave1-settlement-scan.json — same
- r21/evidence/final/wave-settlement{,-observed}.json — same
- r22/evidence/settlement-{final,wave1}.json — same
- r23/falsify/Mut{ModeRead,SetupPartial}/bounded-results.json — same
- **round-58/evidence/w1-settlement.json** — same (`results_not_list,
  seats_mismatch, lane_bad, wave_bad`)

Six of the eleven omitted FAIL files carry the orchestrator's own
`mori-wave-settlement-v1` schema token (measured `schema` key). Drift
coverage is one file exercising one mechanism (`member extra_keys`) out of
two present mechanisms (the other ten are all `results_not_list` + bad
top-level scalars).

### C. Set inconsistency — the pinned artifact set contains files the pinned tool rejects

`ARTIFACTS` (`count-c2.py:55-68`) pins 6 copies. The landed working tree adds
a 7th (`w1-results-r53.json`, S559) that the `tree` byte-equality arm does
not cover. Both non-REAL pinned artifacts scan **FAIL** under the certified
tool:

- `corpus/evidence/sources-r59/w1-results-r53.json` (S559): sha256
  `0d644e0f…4260` — byte-equal to `.ufo/waves/round-53/w1-results.json`
  (verified), but absent from `ARTIFACTS`; its byte-equality is unverified by
  the counter. Only the quote-pin at line 16 binds it.
- `corpus/evidence/sources-r59/w1-settlement-r58.json` (S558): sha256
  `b259e73c…0b55` — byte-equal (verified); the file is a
  `mori-wave-settlement-v1` rollup (`{schema, lane_root, waves, totals,
  ignored_json:1719, unreadable_json:6}`), not a `*-results.json` object; the
  pinned tool returns `SETTLEMENT_SCAN_FAIL` on it.

So the claim "the lane lands a capability that validates orchestrator
`*-results.json` settlement artifacts" is evidenced over a set containing two
artifacts the capability itself rejects — the artifact set and the scan set
describe different definitions of "settlement artifact," and no arm checks
that the pinned artifact population is verdict-coherent.

### D. No counterexample on the landed bytes (explicit)

- All 7 `corpus/evidence/sources-r59/` copies are sha256-equal to their
  `.ufo` originals (measured; 6 of 6 counter-armed + the unarmed r53 copy).
- Member key sets are uniform per file: r54–r58 members = exactly
  `{name,agent,output,note}` (one distinct keyset/file, all `note:null`);
  r53 = same + `report_file` on 67/67. Entry claims K1–K14 quote/pin
  structure verified; universal claims (K6/K7 every-member-note, K11
  report_file absence) are **true** against the pinned bytes.
- S-rows S553–S559 exist at `corpus/SOURCES.md:333-339`, status `mined`,
  `used-by` = the entry (S553–S557 grade A; S558–S559 grade B).
- The tool's own selftest (`SETSCAN_SELFTEST pass=10`) already covers the
  generic defect classes (extra key, missing key, dup name, bad role,
  seats_mismatch, non-object, non-JSON, zero args, mixed set), so the
  PIN-locked tool cannot be swapped for a permissive one — the residual gap
  is evidence coverage + set coherence, not exploitable tool mutation.
- `contract.md:78` claim "the r53 file MUST scan FAIL" holds (measured
  exit=1); the r54–r58 files all scan OK with `members==seats` (74/64/64/64/
  64 = member counts).

## Impacted axes / smallest safe correction

Axes: C2 depth (evidence coverage, artifact-set coherence). No kill-rule
hit — counter bytes, contract bytes, predicate and target are untouched and
the frozen mechanics behave as frozen. No hostile-fixture bypass found.

Smallest safe corrections (next round; frozen bytes immutable now):
1. Extend `REAL_SCAN` to all committed conforming `*-results.json` (≥13
   files) or state the selection rule (e.g. "the contiguous post-drift
   window"); at minimum include one `w2` and one `a2*` file to cover
   wave-name/shape diversity.
2. Extend `DRIFT_SCAN` beyond r53: at least one `mori-wave-settlement-v1`
   file (e.g. round-58 evidence or r19/r22) to cover the
   `results_not_list`/`*_bad` mechanism, and record the two-mechanism
   drift census in the contract.
3. Add the r53 copy to `ARTIFACTS` (or drop it from sources-r59) so every
   pinned copy's byte-equality is counter-verified; consider a
   scan-consistency note in the entry that pinned artifacts include
   FAIL-shaped artifacts (the entry already calls r53 "drift recorded, not
   repaired" — S558's FAIL shape is not flagged anywhere).
4. Contract wording: name the sets "a contiguous post-drift sample" rather
   than "the five r54–r58 wave-results files" if exhaustiveness is not
   intended.

Scratch: `/fast/scratch/hyaku/mori-r59/Mo59Critic30` (scan outputs only;
cleaned). No production/VCS/fleet writes; all tool invocations read-only.
