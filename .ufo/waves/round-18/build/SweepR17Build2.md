# Round-17 build-report privacy reading sweep

## Scope and method

Read the 11 requested reports in `.ufo/waves/round-17/build/` and reviewed the frozen C1 policy and population boundary. This is a manual recall-floor sweep, separate from the C1 metric; `c1-policy.json:29` explicitly says the regex classes are not a privacy proof. The `SW1`–`SW5` tags below are local sweep categories, not new C1 classes. Counts are distinct flagged source lines, not regex-hit counts or a C1 score.

No report text or private values are reproduced here. No OMP transcript, journal, personal document, shell history, credential, or privileged configuration was opened; no URL was fetched. The read-only `git show <base>:<path> | sha256sum` pipelines for the 11 named reports succeeded and produced the digests below. No installs, updates, tests, or VCS mutations were performed. The only write is this report.

**Snapshot caveat:** a later search returned a different live-path snapshot for `OmpRetryConfig.md` than its initial full read. The line findings below describe the initially read report; the digest is the requested base-commit blob digest. Do not apply those line numbers to a later worktree variant without checking that variant separately.

### Sweep tags

- **SW1 — Other-seat tool/report results:** excerpts or paraphrased findings originating in another seat's tools/reports.
- **SW2 — Operator/host configuration:** concrete host environment, local configuration, or model-routing facts.
- **SW3 — Session-record values:** transcript-derived values, counts, or metadata outside the permitted field-only summary.
- **SW4 — Peer artifact:** peer-message content or identifying/provenance details for a private artifact.
- **SW5 — Session/host history:** host probes, tool/dispatch receipts, or time-correlated activity records.

## Findings

| Report and line(s) | Tag; count | Minimal redaction |
|---|---:|---|
| `.ufo/waves/round-17/build/FrontierLinkage.md:7,15-22,28-31,35` | SW1; 14 | Remove sibling-report result summaries; retain only the primary-source linkage and the bounded claim needed by this report. |
| `.ufo/waves/round-17/build/HelperFailureWindows.md:9,34-39,177-178,195,248,264-265` | SW1; 13 | Remove the other seat's sandbox measurements and report-derived result details; retain the source-level invariant and general failure condition. |
| `.ufo/waves/round-17/build/HelperFailureWindows.md:29,202` | SW2; 2 | Replace the concrete local user/config identity with “configured lane identity.” |
| `.ufo/waves/round-17/build/JjEnvFacts.md:20,25-28,41-49,111,161-163` | SW2; 18 | Remove host home/config paths, environment values, and config-directory existence checks; retain generic jj configuration-path rules. |
| `.ufo/waves/round-17/build/JjGate.md:233-243` | SW5; 11 | Drop the prior-pass command and scratch-path history; retain only the current-pass scope. |
| `.ufo/waves/round-17/build/JjGate.md:244-247` | SW1; 4 | Remove peer coordination identity/result details; retain the technical conclusion without its message provenance. |
| `.ufo/waves/round-17/build/KnowledgeJjBranch.md:33-35,56-60,101-103,115,119,123,127,143` | SW1; 16 | Remove the other auditor's sandbox/result details and the draft's repeated copies; retain only the independently sourced, bounded claim. |
| `.ufo/waves/round-17/build/KnowledgeSeatTerminal.md:61,71` | SW3; 2 | Remove the session-derived motivating/error signature; state only that the motivating incident is unverified here. |
| `.ufo/waves/round-17/build/KnowledgeSeatTerminal.md:82` | SW1; 1 | Replace the repeated cross-report resumability result with a generic limitation not tied to another seat's observations. |
| `.ufo/waves/round-17/build/LessonMistakesDraft.md:12` | SW4; 1 | Replace the peer-message excerpt/attribution with a non-identifying statement that an archived note was out of scope. |
| `.ufo/waves/round-17/build/LessonMistakesDraft.md:13-15,21-24` | SW5; 7 | Remove the detailed host-probe, scratch, receipt/timing, and package-query results; retain only the violation class and disposition. |
| `.ufo/waves/round-17/build/LiveLaneHeadVsBranch.md:50-60,66-69` | SW5; 15 | Remove the watchdog/launch correlation and same-session snapshot history; retain only the necessary abstract census conclusion. |
| `.ufo/waves/round-17/build/MisrootR16Facts.md:9-11,24-50` | SW4; 30 | Remove peer-artifact identity, metadata, attribution, and quoted content; replace with a generic evidence-presence statement. |
| `.ufo/waves/round-17/build/MisrootR16Facts.md:12-20,52-74,77-104,106-136,147-161` | SW5; 106 | Remove the detailed sweep/dispatch timeline, command output, host activity, and related historical records; retain only the pathspec defect and its correction. |
| `.ufo/waves/round-17/build/MisrootSweep.md:8-11,91-95,104-110,116-119,130-135,179-202,204-230,232-236` | SW4; 82 | Remove the peer artifact's path/hash/byte-level provenance and every fixture/output repeat derived from it; use a synthetic, non-peer fixture and a high-level result. |
| `.ufo/waves/round-17/build/MisrootSweep.md:165-175` | SW5; 11 | Remove point-in-time fleet/session-state file details and counts; keep only the sweep's pass/fail conclusion. |
| `.ufo/waves/round-17/build/OmpRetryConfig.md:4-6,13-17,20-32,34-60,198-202` | SW2; 53 | Replace operator config/model-routing values and paths with a generic statement about the schema; remove concrete role, provider, and candidate mappings. |
| `.ufo/waves/round-17/build/OmpRetryConfig.md:1,8-9,18-19,87-93,130-131,133-164,168-196,206-213,220-221` | SW3; 85 | Remove transcript-derived signatures, per-session/per-model counts and identities, retry/recovery details, and session-store paths; retain only non-session-specific schema behavior and explicitly marked unknowns. |

## Per-file line counts and committed-blob SHA-256

Counts are unique flagged lines per tag; the totals equal the number of distinct lines identified in that file. All digests are from the base revision named by the round-18 contract.

| Report | SW1 | SW2 | SW3 | SW4 | SW5 | Total flagged lines | SHA-256 |
|---|---:|---:|---:|---:|---:|---:|---|
| `FrontierLinkage.md` | 14 | 0 | 0 | 0 | 0 | 14 | `1a7ed8983c1ac5cf003f49cea7227488244e526cea6462ea467c2b98709a919a` |
| `HelperFailureWindows.md` | 13 | 2 | 0 | 0 | 0 | 15 | `4af9ca0b10f75e98c14dfd6cbc01c160945add3f56ab293ed0908496767eb4c4` |
| `JjEnvFacts.md` | 0 | 18 | 0 | 0 | 0 | 18 | `185783bb08f4359a713a1049816561eb9082246e695af97c1dc339385cd23088` |
| `JjGate.md` | 4 | 0 | 0 | 0 | 11 | 15 | `76a05de8dc1c248f28cee37e65e3069922c5551657f2f8fe4c9b27d1c7e5c1e1` |
| `KnowledgeJjBranch.md` | 16 | 0 | 0 | 0 | 0 | 16 | `4d0b6b66c6126c85fb311303b209d9275c21f52e2ca6fed4b887387569e5e396` |
| `KnowledgeSeatTerminal.md` | 1 | 0 | 2 | 0 | 0 | 3 | `4a49e621b867c49ce6b06c1572b36b9c02d6fffc87ae1355bd54f9e98e2c0c1a` |
| `LessonMistakesDraft.md` | 0 | 0 | 0 | 1 | 7 | 8 | `89529fc9857fe2dd555e9ab62cc2be30aaea2fa47ad53d168b18c4f12ed019fd` |
| `LiveLaneHeadVsBranch.md` | 0 | 0 | 0 | 0 | 15 | 15 | `c25b0d8a6b2515ce575839da5a174946c4a4c6a535273535373361631940ede3` |
| `MisrootR16Facts.md` | 0 | 0 | 0 | 30 | 106 | 136 | `1edff8b1fefccaed6ea48a7ee8d7ae18ad75f07cc599038174cdfbd021f6e013` |
| `MisrootSweep.md` | 0 | 0 | 0 | 82 | 11 | 93 | `70795bee0a1aa182fa1b24fc533049199c5b20ef96d9f5f9ced8d7ca0c90028d` |
| `OmpRetryConfig.md` | 0 | 53 | 85 | 0 | 0 | 138 | `d6340be91155b713e327f310f6b1f82eefe8746d46c6455b61fa8fb7392b2ec7` |

## Repeated facts requested by the spot-check

- `.ufo/waves/round-17/build/FrontierLinkage.md:22` repeats the pacman-log actor-attribution caveat also covered by `PacmanActorTrace.md`; remove that repeated attribution finding and retain only the public-source/claim-boundary note.
- `.ufo/waves/round-17/build/KnowledgeSeatTerminal.md:61,71` repeats the session-derived motivating failure signature recorded in `OmpRetryConfig.md`; remove the signature from the knowledge draft.
- `.ufo/waves/round-17/build/KnowledgeSeatTerminal.md:82` repeats the resumability caveat covered by `SessionExitCorrelation.md`; keep a generic limitation, not the session-specific observation.
- No other requested file showed a clearly matching fact from those three named reports in this read. The `LessonMistakesDraft.md:15` package-version note is not treated as a duplicate of PacmanActorTrace's actor attribution.

## Clean files and limits

**Clean files: none.** Each of the 11 requested reports has at least one SW-tagged line above. No actual credential or token value was observed. This sweep did not run the C1 tool or compute any R1–R9 population/count; all counts above are manual line counts for out-of-regex privacy review only.