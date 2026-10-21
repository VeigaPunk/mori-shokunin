# SentinelOutput — static privacy audit

**Axes:** data minimization, provenance, retained-value exposure.

**Scope and limits:** Read only the round-19 contract and retained sanitized artifacts. No private source inspection, tool execution, harness run, or test was performed. I did not inspect free-text field values. Accordingly, I cannot certify that no private source values are retained; the available evidence is insufficient for that claim.

## Finding

**MEDIUM — privacy/schema: unbounded reviewer text can retain source values.**

- **Evidence:** `.ufo/waves/round-19/contract.md:10 — privacy/schema`. The C1 review row accepts a free-form `reason` string; “no quotations or values” is author guidance, not a schema constraint. `.ufo/waves/round-19/content-reviews-before.json:1 — privacy/schema` contains 26 reason strings and a free-form `coverage_note`. A value-blind count found zero reason fields with quote markers or newlines, but 23 exceed 160 characters. This does not establish that their text is free of source values; those values were not opened or compared with source. The C1 stdout contract does correctly prohibit echoing reasons or contents, but that does not constrain the retained review input itself.
- **Exploit path:** A reviewer or untrusted review-row author puts a private source value directly—without quoting it—in `reason` or `coverage_note`; the review JSON is retained even when the tool’s stdout suppresses those fields.
- **Impact:** Private values could be retained in repository artifacts despite a metadata-only tool output. No actual private source value was confirmed present or absent under the permitted inspection.
- **Smallest remediation:** Replace free-form `reason` and `coverage_note` with a closed set of safe reason codes; reject unknown values. A quote-character filter alone is insufficient.

## Output and receipt evidence

- `.ufo/waves/round-19/wave2-context.json:1 — metadata-only receipt`: captured stdout parses as a seven-field static metadata record (counts/identifiers/digest fields, no source-text or reason field); stderr is empty. This is not a runtime receipt from either round-19 tool.
- `.ufo/waves/round-19/falsify/ — receipt coverage`: the directory contained only `swarm-registry.json`; no round-19 tool-output or harness receipt was available to inspect. The contract defers the harness run to the integration owner, and it was not run here.
- `.ufo/waves/round-19/contract.md:10-12 — output/schema`: the specified content-review stdout suppresses review reasons and contents; freeze-order failures must not expose raw inputs. The harness contract calls for synthetic fixtures and contains a `no_private_values` expected assertion, but that assertion is not evidence until the owner runs the harness.
- Whole-blob digests in review/provenance records identify bytes; they do not prove those bytes or associated free text contain no private values.

No tool installations or verification runs were performed.