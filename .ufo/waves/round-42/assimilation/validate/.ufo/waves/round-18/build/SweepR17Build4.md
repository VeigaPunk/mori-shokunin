# Round-17 build-report privacy sweep (outside C1 regex metric)

## Scope and method

Read each of the eleven assigned round-17 build reports fully, the round-18 contract and frozen C1/C2/C3 inputs, and the three named reports only to classify repetition. No target report was edited. The report contains only path/line/class/count/hash references and redaction guidance; no private values or verbatim excerpts are reproduced.

The frozen R1–R9 classes do not cover every retained private fact. Sweep-only classes used here:

- **S1 — session identity/location:** unqualified session/transcript names or a private session-store path not matched by R1/R2/R3.
- **S2 — session-record content/derived facts:** non-allowlisted field values, per-record observations, or fine-grained aggregates and snapshots.
- **S3 — model/provider routing:** concrete model/provider assignments or distributions.
- **S4 — local tool/runtime output:** private host/tool inventory or output details not captured by R1–R9. **[INFERENCE]** for installed-tool metadata.
- **S5 — prior-session/system activity:** paraphrased private operational history or host-journal/tool results.
- **S6 — operator/workspace configuration:** external config locations or observed configuration values outside R7/R8.

Line counts below are unique lines per file (a line can carry more than one class). The `RetryRecoveryShape.md` and `ReviewC1Contract.md` session-directory paths are already covered by R1/R2 and are not counted as sweep misses; `ReviewC1Metric.md:43` is a miss because the store-root path has no following slash.

## Findings

| Lane-relative file | Missed lines / class (unique line count) | Minimal redaction | SHA-256 |
|---|---|---|---|
| `.ufo/waves/round-17/build/RetryRecoveryShape.md` | `34-37`, `41-47` S1/S2; `53-55` S2; `63`, `65-68`, `78` S2; `83-90` S1/S2; `94-106` S2; `112-126` S1/S2; `128-145` S2; `149-157` S2; `159-179` S1/S2; `181-195` S2; `199-209` S2; `216-223` S2. **138 unique lines.** | Remove transcript identities/line pointers, per-file changes, exact timings and sizes, record-level values, schema cardinalities, and detailed class/transition counts. If a conclusion must remain, state it only at a non-corpus-specific level without reproducing any observed result. | `d9f6a9fccd8f690a106ca14dbd58c592e4acc4819c5f1aa66477d537dbb6b1de` |
| `.ufo/waves/round-17/build/RevengerCensusHead.md` | `28` S1. **1 line.** | Remove the directory identity; if explanation is needed, use a generic search-scope limitation. | `24e8a8139bc5071bbe9be44e59bec5d4074a990b144c63e0630050858aabcd54` |
| `.ufo/waves/round-17/build/RevengerContextChecker.md` | `9`, `19`, `21`, `23`, `27`, `31-35` S5. **10 lines.** | Remove prior-incident narratives, seat-coded labels, and receipt outcome values; retain only abstract clause IDs and code references. | `29f47794dad85b42c4b3602f0ead84431821e9587a8859841a60031ed88c8955` |
| `.ufo/waves/round-17/build/RevengerOmpTerminal.md` | `11`, `33-39` S4. **8 lines.** | Remove local executable/tool metadata and command outputs; keep any source-availability statement free of paths, versions, diagnostics, and command results. | `fa1b8fac182c8ab07fc17aa0e41cd1bd8496238f829882f52a6c7133ada78bcf` |
| `.ufo/waves/round-17/build/ReviewC1Contract.md` | `9` S2/S3; `13`, `15` S2. **3 lines.** | Remove transcript-derived values and observed signal details; retain only non-sensitive contract/source references. Line 13's directory identity is already matched by R1/R2, but its detailed counts are not. | `356ca2e05e0bfab162da5dd4f783d28d6d4fe29c3c3f6f1304683dac3090df20` |
| `.ufo/waves/round-17/build/ReviewC1Metric.md` | `43` S1. **1 line.** | Replace the actual private store-root path with a placeholder such as `SESSION_STORE`. | `3d171872751c29c4c584c195a2fdf0ae73d316cd6f9fc61ef19274af817934b5` |
| `.ufo/waves/round-17/build/ReviewC2Contract.md` | None. **0 lines.** | Clean under the requested categories. | `bc6224670766fa32c0d6a315699f650eba3de4d434051fdc73ea4c5179f8fbd1` |
| `.ufo/waves/round-17/build/ReviewC2Metric.md` | None. **0 lines.** | Clean under the requested categories; its local repository ref observations were treated as lane-source metadata, not private session/document/config facts. | `fdf87c94b842d51d87a3559abcc8c4e108e01c9010b69d117cde6faf1cd58564` |
| `.ufo/waves/round-17/build/ReviewCarryForward.md` | `19-22` S5. **4 lines.** | Remove host-journal/capture output-derived details; if provenance is required, cite the existing lesson without restating its findings or counts. | `2ba0ec6c92304d74d5d2bb2f714191f52e2f42d2e507ca5d8f01407702fddf24` |
| `.ufo/waves/round-17/build/ReviewExitSemantics.md` | None. **0 lines.** | Clean under the requested categories. | `6c4a326c2e53ae98792693baf5b6b70e913631992d4ff7fd30dd99ddcdea9880` |
| `.ufo/waves/round-17/build/ReviewJjAuditRouting.md` | `67`, `69` S6. **2 lines.** | Remove the home-level configuration location and concrete setting value; do not replace them with another path or setting detail. | `d31038bd8decdb7cb2a8026830712e7ca0d300af2a5ad3b40b7378708de0d2ea` |

**Total:** 167 unique lines in 8 reports retain sweep-class context not fully covered by R1–R9. Three reports are clean: `ReviewC2Contract.md`, `ReviewC2Metric.md`, and `ReviewExitSemantics.md`.

No credential values, personal-document paths/content, shell-history content, or privileged-configuration values were observed in the eleven target reports. The concrete model/provider data in `ReviewC1Contract.md:9` and the external configuration details in `ReviewJjAuditRouting.md:67,69` are the routing/configuration exposures found.

## Repeated-fact spot check

The three comparison files were read only to classify overlap; their values are not reproduced here.

| Comparison source (lane-relative path; SHA-256) | Target report and line references | Result |
|---|---|---|
| `.ufo/waves/round-17/build/PacmanActorTrace.md:11-18,24-32,43-50` — SHA-256 `b30443665d48a32bb49dfa501eef8ec594a3ab03b299bf9e84d0904b6512d1bf` | `RevengerContextChecker.md:17` | No repeated transaction/actor/package fact; the target reference does not duplicate the source evidence. |
| `.ufo/waves/round-17/build/OmpRetryConfig.md:11-18` — SHA-256 `6428d1154253d54788bb5dccaec71efb0f80c610f92c6db52e99a4a81b3cf7f4` | `RetryRecoveryShape.md:88-90,138-145`; possible topical overlap at `ReviewC1Contract.md:9` | Partial S2/S3 subject-area overlap; no repeated source-specific configuration/default values are established. Exact overlap with `ReviewC1Contract` cannot be determined from the minimized comparison source. |
| `.ufo/waves/round-17/build/SessionExitCorrelation.md:40-49,54-56` — SHA-256 `fcacbcc60ad8b4c8c30c074b1005d6993d653a9c9d8d0ca941028fc69daf6765` | `RetryRecoveryShape.md:120-122,170-179,186-195,216-218` | Confirmed S1/S2 overlap in lifecycle/disposal material and record-level anchors. The cited target lines should not retain the duplicated identities or detailed observations. |

## Evidence notes

- Static reads returned the requested report contents; the destination check returned “not found” before creation. The read device does not expose shell-style exit codes.
- `sha256sum` printed digests for all eleven target reports and the three comparison sources; the tool output did not surface the process exit status.
- No tool was installed or updated. No Git/JJ command, test, runtime probe, external URL, or LSP operation was used. The only write is this report.
