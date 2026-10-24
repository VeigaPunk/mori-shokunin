# Round-17 build-report privacy sweep (outside C1 regex metric)

## Scope and handling

Read the round-18 contract and frozen C1 policy, then all five assigned round-17 targets in full. The three routed reference reports were consulted only to classify overlap; no private text or values from them are reproduced here. No transcript/session store, operator documents, configuration files, history, privileged files, credentials, or tool logs were read. No tools were installed or updated; no VCS or repository files were changed apart from this report.

Read-only digest command: `sha256sum` over the five targets and three routed references returned all eight digests; the tool output did not separately expose a numeric exit status.

The findings below are line references and data categories only. They identify retained context not caught by C1 R1–R9, or explicitly distinguish the few regex-covered lines. Suggestions are deliberately minimal: replace real-session-derived details with synthetic fixtures, counts, or hashes.

## Findings by target

### `.ufo/waves/round-17/build/TranscriptShapes.md`
SHA-256: `063d21b31d2995b82abaa7379921095533988c6a3f9b6e7e69f8329ed70cb028`

- `:20,38-48` — private session-store scale and time-varying corpus/class counts; not matched by R1–R9. **Suggestion:** omit store-size/snapshot detail and use synthetic fixtures for change-over-time behavior.
- `:28-31` — names non-allowlisted transcript fields whose values were inspected; field names alone, not their values. Not matched by R1–R9. **Suggestion:** replace the field inventory with a generic statement of bounded metadata inspection.
- `:52-75` — observed terminal-record/stop-state census and a concrete mid-transcript session identity. The state census is not matched; the full timestamp/UUID identity at `:72` is caught by R1. **Suggestion:** retain only synthetic cases and remove the real-corpus census and identity.
- `:79-82` — transcript error-status values, types, and frequencies; not matched by R1–R9. **Suggestion:** document the classifier predicate with synthetic statuses, not corpus frequencies.
- `:88-108` — per-provider/model assignments and per-model error/completion counts, including a comparative ranking; R8 matches routing-table keys, not these values. **Suggestion:** remove provider/model labels and retain only class-level totals or synthetic labels.
- `:112-142` — multiset and ordering of tokens drawn from terminal error-message text, with observed frequencies; this is derived output from other sessions and is not covered by R1–R9. **Suggestion:** express token-order behavior only as synthetic fixture cases; remove observed message-shape counts.
- `:148-156` — retry/error-message shape, retry-count and error-code distribution from session records; not matched by R1–R9. It repeats the OmpRetryConfig subject matter (see “Repeated facts”). **Suggestion:** retain a synthetic parser fixture, not the observed count or real message template.
- `:161-166` — cross-corpus key-presence observation for a non-allowlisted session-record field; R9 does not match this bare key/presence form. **Suggestion:** state only the synthetic fixture invariant, without the corpus-wide presence result.
- `:172-202` — private per-transcript identity, byte sizes, record shape and terminal state. The plain seat-file identities in `:179-189` evade R1; the full timestamp/UUID identity at `:192` is caught by R1. **Suggestion:** remove path/name columns and keep anonymized size buckets or a digest-only inventory.
- `:205-228` — individual session state transitions and provider/model split, plus a session-record field-existence assertion. R8 does not catch model/provider values and R9 does not catch that field name. **Suggestion:** aggregate to counts without seat IDs or provider/model labels; remove the field-name assertion.
- `:232-262` — per-prefix live/incomplete counts and a session-exit/last-record/age cross-tab, including marker prevalence and resumed-session observations; not matched by R1–R9. This overlaps SessionExitCorrelation (see below). **Suggestion:** replace the cross-tab with synthetic examples and remove prefix/age distributions.
- `:266-269` — a named prefix’s abort count and transcript total; private per-prefix session telemetry, not matched by R1–R9. **Suggestion:** retain only the aggregate class count.
- `:274-286` — seat-name uniqueness and prefix derivation facts, including a concrete top-level session identity; the concrete timestamp/UUID at `:280` is caught by R1, while the naming/count facts are not. **Suggestion:** remove the concrete identity and real prefix statistics; describe the edge case synthetically.
- `:290-301` — corpus file-integrity and record-type observations; specifically `:300-301` disclose the presence/count of credential-adjacent records, which R1–R9 miss. No credential value is shown. **Suggestion:** remove the presence/count claim and retain only the general parser rule not to inspect such records.
- `:305-311` — historical dead-class totals and repeated-scan behavior; private session-derived metrics not matched by R1–R9. **Suggestion:** state the exit-code semantics without the corpus tally.
- `:315-329` — session-record payload/field discussion and per-model/per-prefix comparisons; the model values evade R8, and the session-derived counts evade R1–R9. **Suggestion:** keep only the generic unresolved questions, without observed model/prefix associations.
- `:333-347` — recommendations restate measured corpus counts, liveness splits, and prefix/session facts; not matched by R1–R9. **Suggestion:** retain the recommendations but replace each empirical value with a synthetic-fixture result.

### `.ufo/waves/round-17/build/TranscriptTailBounds.md`
SHA-256: `97622bf464e76e9dc0e1699ef629e1d486272d07d413fb89899076b48c4e359b`

- `:17-20,24-26,33-62` — session-store file counts, scan drift, distribution and tail-window measurements; `:59-62` also report session-exit marker frequency/placement. These aggregate facts are not matched by R1–R9; the latter overlap SessionExitCorrelation. **Suggestion:** keep synthetic tail-bound tests and remove the live-store distribution and scan measurements.
- `:66-87` — 11 transcript paths with byte sizes, message sizes, classes and prefix tally. The truncated session-directory identity at `:70` and `:84` does **not** match R1 (the ellipsis follows the UUID prefix instead of R1’s required hyphen); the seat-file names also evade R1. **Suggestion:** delete the path/prefix columns and retain only anonymized size buckets.
- `:91-108` — live-corpus classification consequences and class-coverage percentages; private session-derived findings not matched by R1–R9. **Suggestion:** describe the failure mode using synthetic cases, not corpus outcome counts.
- `:113-124` — real-corpus read-cost/tail-size trade-off; not matched by R1–R9. **Suggestion:** remove the corpus byte totals and present a general complexity or synthetic benchmark.
- `:128-135` — transcript growth, modification-time and no-message counts; not matched by R1–R9. **Suggestion:** describe only the scan-time caveat and test it with a synthetic append case.
- `:139-144` — corpus-specific compaction and large-record observations; not matched by R1–R9. **Suggestion:** preserve the uncertainty but omit real-corpus cardinalities.
- `:148-155` — verdict repeats historical seat-count, class-coverage and message-size findings; not matched by R1–R9. **Suggestion:** retain the design conclusion without real-corpus values or seat descriptors.
- `:8-10,22` — session-store path is present but already matched by R2; it is not a regex miss. **Suggestion:** remove the path as unnecessary reproduction detail.

### `.ufo/waves/round-17/build/WaveRegistryVsReports.md`
SHA-256: `d5b7c81a95fe77760546365981c3118a3a7a23d2879f6541aeab486ab6070281`

- `:11-19,47-68` — cross-lane wave membership, delivery/death state, in-flight status and wave counts; private operational/session facts not matched by R1–R9. **Suggestion:** retain lane-level totals only, with no per-seat status.
- `:33-45` — individual cross-wave task/report identities and dispatch-state checks; not matched by R1–R9. **Suggestion:** replace names with counts and a digest of the sorted inventory.
- `:72-164` — missing-task inventories, role associations and explanations across closed waves; task identities are bound to non-delivery/death status and are not matched by R1–R9. **Suggestion:** remove all name blocks; retain counts by lane/role and a digest.
- `:166-179` — residual-wave task/registry naming and dispatch discrepancy details; not matched by R1–R9. **Suggestion:** describe the discrepancy by counts and hashes, without task labels.
- `:183-208` — transcript-class/report-delivery cross-tab and named transcript/status observations; not matched by R1–R9. **Suggestion:** keep only non-identifying aggregate reconciliation.
- `:213-230` — repeats a quoted tally attributed to another report/orchestrator message and adds transcript-derived retry/death comparisons. This is retained communication/output context not matched by R1–R9. **Suggestion:** remove the quoted communication and keep only a locally computed, non-identifying comparison.
- `:234-243,247-255` — lane-authored outcome summaries, live-wave status, reporting timelines and in-flight counts; not matched by R1–R9. **Suggestion:** remove detailed timelines and preserve only closed-wave totals.
- `:259-270` — cross-lane registry anomalies and member/dispatch identifiers; not matched by R1–R9. **Suggestion:** replace member labels with counts and digests.
- `:275-306` — per-lane terminal/dead-seat totals, resume/reclassification and transcript-prefix coverage; not matched by R1–R9. **Suggestion:** retain only aggregate, non-identifying caveats and remove prefix/state associations.
- `:310-342` — the reproduction snippet itself contains no transcript output, but its print statements emit missing/orphan task-name lists and the report retains point-in-time rerun results. **Suggestion:** change the reproducer to print counts and a digest only; omit rerun timestamps/results.
- `:354-355` — package-manager mention is installation bookkeeping only; it does not repeat PacmanActorTrace’s host transaction/actor facts.

### `.ufo/waves/round-17/build/SrcZaiErrorCodes.md`
SHA-256: `23a7c060038ff116a2f353bb21968014aa3bddece2124712d8c8992b00c56e63`

**Clean.** It reports public API documentation and its public error-code mapping; it contains no operator transcript/tool output, session-store identity or facts, private document/history/privileged-config data, routing configuration, or credentials. No repeated facts from the three routed reference reports were found.

### `.ufo/waves/round-17/build/swarm-registry.json`
SHA-256: `cd4ba487531c18725d32194c7e05bc829ebee49d0df250beff5e2d7f090fbe67`

**Clean for this sweep.** It is the round-17 wave’s own dispatch manifest (member IDs, roles, spawn kind and registry timestamps); no other-session transcript/tool output, session-store path/file identity, operator model/config values, private document/history/privileged facts, or credential material was found. Its own-wave roster is not a transcript identity or session-record value.

## Repeated facts from routed reports

These are overlaps, not quotations; reference hashes are included for provenance and no private values are repeated.

- **PacmanActorTrace:** no transaction, actor-attribution or tool-output finding is repeated by the five targets. Reference `.ufo/waves/round-17/build/PacmanActorTrace.md:11-62`; SHA-256 `b30443665d48a32bb49dfa501eef8ec594a3ab03b299bf9e84d0904b6512d1bf`. The install-bookkeeping note at `WaveRegistryVsReports.md:354-355` is not such a repeat.
- **OmpRetryConfig:** `TranscriptShapes.md:148-156` repeats the retry-budget/error-shape finding. `WaveRegistryVsReports.md:18,88-91,213-226,276-278` repeats retry-budget death tallies by topic, but its stated source is the separate DeadSeatCrossCheck report; it does not restate an operator config value. Reference `.ufo/waves/round-17/build/OmpRetryConfig.md:1-46`; SHA-256 `6428d1154253d54788bb5dccaec71efb0f80c610f92c6db52e99a4a81b3cf7f4`.
- **SessionExitCorrelation:** `TranscriptShapes.md:242-260,315-324` and `TranscriptTailBounds.md:59-62,82-84` repeat marker/terminal-state, resume and placement findings. Reference `.ufo/waves/round-17/build/SessionExitCorrelation.md:11-23,40-55`; SHA-256 `fcacbcc60ad8b4c8c30c074b1005d6993d653a9c9d8d0ca941028fc69daf6765`. WaveRegistryVsReports includes a resume-state observation, but not a repeated disposal-marker correlation.

## Conclusion

Private-context retention missed by the frozen regex is concentrated in `TranscriptShapes.md`, `TranscriptTailBounds.md`, and `WaveRegistryVsReports.md`; the details above identify the affected line groups, context type, C1 coverage and a minimal redaction. `SrcZaiErrorCodes.md` and `swarm-registry.json` are clean for the requested privacy categories. Full timestamp/UUID identities and the session-store paths noted above are already covered by R1/R2; the remaining examples are outside those frozen patterns, and the findings sweep is not itself a privacy proof.