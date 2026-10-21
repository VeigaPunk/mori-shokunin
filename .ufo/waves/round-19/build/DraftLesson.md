# Round 19 Gate / Mistakes — scoped draft

Status: planning lesson from retained round-18 spot-check, round-19 contract, and frozen expected values only. This is not an implementation report, a measurement, or a closure. No round-19 gate or regression execution was performed here.

## Gate lesson: establish ability to fail before making claims

Round 19 C1 is an adjacency capability claim, not evidence that production content is defective. The contract freezes 10 synthetic requirements; absence of the capability is a red capability result, not a production-defect count. Keep the existing R1–R9 all-blob policy and exact allowlist unchanged. The content-population pin must match; every frozen path must exist at the selected revision and have exactly one review row with matching blob SHA-256. Unknown/duplicate rows, stale content, unresolved decisions, and provenance-only reviews cannot produce clean. Content review must decide from content, not infer safety from same-wave provenance. The interface distinguishes clean (0), failed (1), and could-not-evaluate (2), and the output is limited to metadata, counts, and path-level finding codes; do not disclose review reasons or content.

Use the frozen oracle before any capability claim: its 10 C1 cases include a clean control and cases for missing/duplicate review, unknown decisions, digest drift, unresolved/private content, provenance-only review, out-of-population rows, invalid revision, and a tampered population pin. The expected classifications and required finding codes are in `frozen/expected.json`; they are requirements, not observed results. In particular, missing capability is not evidence of historical production defects.

For C2 calibration, attach provenance to the existing freeze-order check without changing its six established verdicts or topology rules. A provenance-capable run must record the measured full revision, loaded input digests, script digest, argv, resolved bases and tips, and tip overrides; the receipt must bind these facts to the inputs actually loaded. Load each file once for hashing and evaluation; do not put raw input values in failures. The 12 frozen assertions cover these details, verdict preservation, redaction, and invalid-revision handling. Keep the distinction explicit: the r18 `4→0` is not four historical defects; the r18 spot-check derives it as one historical overclaim correction plus three prospective labels. Treat provenance acquisition separately from that correction. The old and delivered tools must be compared against the same frozen oracle before claiming the capability; this draft records no such run.

The report of synthetic failures must remain an ability-to-fail demonstration, not a claim that corresponding production defects existed. Do not turn unimplemented or unmeasured behavior into a pass, and do not label a frozen expectation as an execution result.

## Outside-round-18 lessons to carry

- **Source gate evidence:** round 18 identified four newly rejected source rows whose Gate records lacked the required located short quote; one had not been opened beyond its abstract. For each such decision, provide the required located evidence or explicitly identify the permitted screening-only exception. Do not invent or copy source quotations into this report. Reference: `corpus/lessons/round-18-verifier-spotcheck.md:142-145` — gate-evidence gap.
- **Trend claims:** keep expansion unchanged until the coverage map has rows for the new entries; keep quality unchanged unless an existing entry is rechecked, deepened, or superseded. Reference: `corpus/lessons/round-18-verifier-spotcheck.md:148-158` — unsupported trend verdicts.
- **Census arithmetic:** the outside check corrected the round-18 new-row tier tally to 9 A, 1 B, and 5 C across 15 rows, not the report's earlier split. Recount from the retained census evidence before recording any comparable tally; do not silently edit historical bytes. Reference: `corpus/lessons/round-18-verifier-spotcheck.md:164-167` — count discrepancy.
- **Final-tip privacy sweep:** the round-18 resweep receipt was pinned before later edits. A future receipt must name the committed final-content tip and cover every frozen population blob. Reassess routed out-of-metric items with content evidence: the same-wave dead-seat receipt's identifying/diagnostic/time metadata; six historical host-home path entries with conflicting dispositions; and the same-wave SW1 items, for which provenance alone is not a content test. Retain the stated guessability limitation for short-line digests; never publish short-line hashes. Reference: `corpus/lessons/round-18-verifier-spotcheck.md:71-76,168-176` — incomplete final-tip sweep and unresolved dispositions.
- **Freeze-order evidence:** bind revisions and input/script/command provenance in evidence or a receipt, and describe the before/after interpretation as one historical correction plus three prospective labels rather than a flat defect reduction. Reference: `corpus/lessons/round-18-verifier-spotcheck.md:90-95,177-179` — evidence provenance and denominator interpretation.
- **Capability reporting:** use the required `SCORECARD.md` capability-table shape, including evidence and first-working round, rather than prose-only capability enumeration. Reference: `corpus/lessons/round-18-verifier-spotcheck.md:108-110,180-181` — scorecard representation.
- **Append-only history:** round-17 originals and the round-18 draft remain in pushed history. History exposure assessment/action is operator/kagi-owned; do not rewrite history or present tip remediation as history remediation. Reference: `corpus/lessons/round-18-verifier-spotcheck.md:68-70,182-188` — history boundary.

## Axes and scope

- **Adjacency (C1, score 6 held):** target is a bounded content-review capability over the frozen out-of-metric population; no denominator cuts and no change to the R1–R9 policy or allowlist.
- **Calibration (C2, score 5, lowest tie):** target is evidence-bound freeze-order provenance while preserving the established six verdicts.
- Other axes and any trend/closure verdict are not measured or asserted here. No round-19 measurements, successful checks, score changes, or closure are claimed.

## Touched surfaces and out of scope

Only this new scoped report was written. The retained r18 lesson, scorecard, round-19 contract, frozen oracle, product code, historical reports, and other production documentation were not edited. No builds, tests, linters, formatters, smokes, or verification runs were performed. No private source values, quotations, or short-line hashes are reproduced. No installs or external reads were made.

Report: .ufo/waves/round-19/build/DraftLesson.md
