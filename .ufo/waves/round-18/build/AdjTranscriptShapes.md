# TranscriptShapes C1 population adjudication

## Scope and result

Axes: privacy minimization, evidence/provenance retention, and recall outside the frozen regex metric.

Reviewed `.ufo/waves/round-17/build/TranscriptShapes.md` against the frozen C1 population and policy. The frozen population has **5** rows for this path: **R1 × 3, R2 × 1, R9 × 1**. All five are **redact**. None names a surface without contents, names a schema field/key in lane code/contract/synthetic fixture, or falls under the non-author exception. The frozen C1 policy excludes only non-author files from the metric; this file is not in that exception. No allowlist disposition is appropriate.

For each hit, preserve provenance with a short neutral replacement containing only the adjudication, hit count, class ID, and original line SHA-256 (the final JSON records those hashes). Remove the private-source value, and any sample-specific detail that would retain the same identification. Do not preserve copied exemplars merely to explain the finding.

- **Line 16 / R2:** Replace with provenance-only metadata for one R2 hit. Remove the concrete session-store location; the line describes an actual private source, not a boundary or abstract surface.
- **Line 72 / R1:** Replace with provenance-only metadata for one R1 hit. Remove the concrete transcript identity and any identifying reference to that source. A generic contract observation can be retained only if rewritten without the exemplar.
- **Line 192 / R1:** Replace with provenance-only metadata for one R1 hit. Remove the concrete transcript identity and its sample-specific size/record-composition details.
- **Line 280 / R1:** Replace with provenance-only metadata for one R1 hit. Remove the concrete transcript identity used as an example; do not retain that source instance as a pattern exemplar.
- **Line 297 / R9:** Replace with provenance-only metadata for one R9 hit. Remove the copied, corpus-observed record-type value that triggered R9. It is an observed data value, not a schema field/key eligible for allow-b.

## Full-file sweep: context not captured by C1

The complete reviewed artifact is 347 lines; its SHA-256 at the frozen review revision is `063d21b31d2995b82abaa7379921095533988c6a3f9b6e7e69f8329ed70cb028`. The following is a separate privacy review, **outside the frozen C1 metric**: these are lines not represented by the five C1 population rows, except that lines 280 and 297 are already adjudicated above. No source text or private values are reproduced here. For these additional references the frozen class is **none / no regex hit**; the cited artifact digest identifies the reviewed source.

- `:3` — one non-regex seat/actor identifier.
- `:20-48` — session-corpus volume, snapshot timing, and changing activity/counts.
- `:66-82` — transcript-derived terminal-state, role/status distributions, including values from fields outside the minimal permitted transcript-field set.
- `:84-108` — provider/model names and their distributions: private model/provider routing values not recognized by the frozen routing-key class.
- `:112-157` — error-message-derived tokens, codes, retry details, and distributions; derived session content not covered by the current regex classes.
- `:161-166` — session-field presence and corpus-wide count.
- `:170-201` — individual transcript/sample identifiers, sample sizes, record sizes, and resulting state classifications.
- `:203-228` — seat/transcript identities, state transitions, provider/model distribution, and per-file freshness observations.
- `:230-270` — session liveness/exit correlations, status counts, and group/seat identities.
- `:274-286` — seat/prefix identities, transcript naming relationships, and associated population counts; `:280` is the R1 hit already listed.
- `:288-301` — observed record-shape inventory and presence counts. The record-type/custom-type fields themselves are among the explicitly permitted field subset, but their corpus-specific observations are still source-derived; `:297` is the R9 hit already listed.
- `:305-311` — historical state/count and corpus-run measurements.
- `:315-329` — session-derived uncertainty/behavior claims and additional provider/model identifiers at `:325-329`.
- `:333-347` — recommendations supported by session-derived counts and outcomes, including another reference to transcript identities.

No raw message-content excerpt was observed in the report. The out-of-metric items above are identifiers, field-derived results, and other corpus-specific facts rather than message-body quotations. No additional private-document, operator-config, or shell-history fact was observed beyond the session-store location already adjudicated at `:16`. The model/provider values and the session-derived observations above are reported by line and kind only; none is copied here.

## Evidence and verification gaps

- Read the round-18 contract and frozen C1 policy/population, plus frozen C2 register and C3 ledger format. Filtered the frozen C1 population by this path; it yielded the five rows listed below.
- Read the five requested line windows from `29b0dc7` using `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 29b0dc7:.ufo/waves/round-17/build/TranscriptShapes.md | sed -n '<range>p'`; ranges `13-19`, `69-75`, `189-195`, `277-283`, and `294-300` each completed with exit code **0**. The full-file review was read separately. The frozen-revision artifact SHA-256 is recorded above.
- No tool installation/update was needed. No test, runtime, or gate selftest was run; this is an adjudication/review only. No LSP checks were run: the reviewed target is a Markdown evidence report, and no LSP device/server for it was available.

```json
[
  {
    "path": ".ufo/waves/round-17/build/TranscriptShapes.md",
    "line": 16,
    "class": "R2",
    "line_sha256": "cfac1a99492465d7cd7d2bd18fe20a237faa3bf2888ad491baa9d1ad2490a11e",
    "decision": "redact",
    "reason": "A concrete private-source session-store location, not a surface-only boundary or contract name."
  },
  {
    "path": ".ufo/waves/round-17/build/TranscriptShapes.md",
    "line": 72,
    "class": "R1",
    "line_sha256": "0609d87a6d0e459cffb9992604bf63640ff20ab494efeade53a822577a65f8d2",
    "decision": "redact",
    "reason": "A concrete transcript identity copied from a private source, not only an abstract instruction or boundary."
  },
  {
    "path": ".ufo/waves/round-17/build/TranscriptShapes.md",
    "line": 192,
    "class": "R1",
    "line_sha256": "5137db98a4c1bff4279f0413d5eac47fa57b7a68e755b3dea8a90ba6f5f733ca",
    "decision": "redact",
    "reason": "A concrete transcript identity and sample-specific context copied from a private source."
  },
  {
    "path": ".ufo/waves/round-17/build/TranscriptShapes.md",
    "line": 280,
    "class": "R1",
    "line_sha256": "5cfe8e40a897686e15367315f9a186eb64448bea75eca82948cffec5cddfd62c",
    "decision": "redact",
    "reason": "A concrete transcript identity used as a data exemplar, not an abstract surface name."
  },
  {
    "path": ".ufo/waves/round-17/build/TranscriptShapes.md",
    "line": 297,
    "class": "R9",
    "line_sha256": "33edad9ca53949886ec6c8d08a800a9212a3f0476c6ff9ae0e7de0aae5c537db",
    "decision": "redact",
    "reason": "The matching item is an observed record-type value, not a schema field/key in lane code, contract, or synthetic fixture."
  }
]
```
