# Falsification review — TranscriptShapes token redactions

## Findings (severity order)

### High — session-derived values remain despite the broader minimization rule

`build/TranscriptShapes.md:84-106` retains provider/model strings from terminal records alongside counts. `:112-123` exposes matched fragments drawn from `message.errorMessage`, rather than only normalized class labels and counts. Additional model strings remain at `:173`, `:208-215`, and `:325-329`. The retry analysis at `:148-152` also preserves exact cross-corpus retry/code patterns; it is aggregate rather than per-seat, but is more specific than a class tally.

This conflicts with `corpus/knowledge/evidence-minimization-r18.md:26,29`, which limits other-session transcript evidence to count/class and specifically excludes model strings. The L1 triage's blanket allowance for provider/model and error-message tokens at `.ufo/waves/round-18/out-of-metric-triage.md:26` is not supported by that decision table: these are observed values/fragments, not name-only field or surface names. This finding concerns retained content outside the four edited hunks; the token redactions do not remove it.

### Medium — record-type-name allowance does not satisfy frozen C1 allowlist criteria

The frozen C1 population records an R9 hit for this file at source line 297. The current line remains unchanged (`build/TranscriptShapes.md:296-301`). The R9 class is defined in `.ufo/waves/round-18/frozen/c1-policy.json:15`; its allowlist rule at `:27` restricts eligible lines to specified instruction/boundary/contract, code/contract/fixture, or non-author cases. This corpus-derived record-type census is not one of those contexts. Therefore the triage's general claim that record-type names are allowlistable (`out-of-metric-triage.md:26`) is not sufficient to justify a C1 allowlist row here. This is a frozen-metric/policy mismatch, not evidence of an identity disclosure on that line.

## Changed-line checks

The read-only diff contains four replacements: `build/TranscriptShapes.md:16` (R2 store path) and `:72`, `:192`, `:280` (R1 session identities). Each removes the complete private token and substitutes a withholding marker. The surrounding passages retain only generic field/enum labels, schema shape, counts, sizes, and lane/report context; no session identity, session-store path, tool-log number, personal-document path, configuration location/value, personal identity, routing-table value, or per-seat retry value is left in the edited-line neighborhoods. The remaining generic role/record-type labels do not restore the removed identities.

The replacements preserve the technical claims and Markdown structure: the target path is explicitly withheld; the mid-transcript example and the two session examples remain clearly anonymized. The diff changes no JSON file, so `python3 -m json.tool` was not applicable. Name-only schema/surface mentions are reasonable to retain as text, but they are not automatically eligible for the narrower frozen C1 allowlist (see the R9 finding above).

## Residual risk and verification gaps

C1's frozen policy describes its regex classes as a recall floor (`frozen/c1-policy.json:29`); this review does not establish that the rest of the report is free of other private context. No current-revision retention-gate scan or selftest was run.

The LSP route is unavailable in this tool environment: `read xd://lsp` returned “No such tool”; consequently no LSP status, references, definitions, or diagnostics could be queried. No grep was used. The required read-only diff command, `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff d005cdd e2bfbd6 -- .ufo/waves/round-17/build/TranscriptShapes.md`, completed with exit code 0 (status captured on the repeated read-only invocation). No JSON validation was run because no JSON changed. No tool was installed or updated.