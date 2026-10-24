# Round-17 falsify privacy reading sweep

## Scope and method

Read the 14 requested falsify artifacts in full, against the committed base `d005cdd`. Their committed-blob SHA-256 values below match the inspected text. Read the round-18 contract first and applied `frozen/c1-policy.json:6-15,27-29`; its `known_limit` explicitly makes the lexical metric a recall floor, not a privacy proof.

Focused searches over the 14 files found no exact R1-R9 token matches, credential-like values, session-store/timestamped-session/numbered-tool-log identities, routing-key names, or non-allowlisted session-field names. These searches returned “No matches found” (the read/grep tools do not expose numeric exit codes). The findings below are semantic disclosures missed by those frozen patterns. Supplemental sweep tags S1-S4 are local labels, not new C1 metric classes. No network URLs were accessed.

## Findings

| Tag / kind | Location and count | Minimal redaction |
|---|---|---|
| **S1 — session-derived aggregate tool output** | `.ufo/waves/round-17/falsify/ReportTrace.md:35` (1 line; file SHA-256 `649f5990c3a31d0dff5d3de70d895bc24c4c738e4b1edafd1f5fd534bb2e638c`) | The line carries detailed results from a live seat/transcript scan, including class totals and per-prefix counts. Remove the detailed counts and retain only that the recorded receipt reconciles with the round summary. This is aggregate output, not transcript text or a session identity; treating it as private session-derived context is **[INFERENCE]**. It is outside R3's numbered-log filename pattern. |
| **S2 — local host history / package-log provenance** | `.ufo/waves/round-17/falsify/ReopenPacmanLog.md:78-80` (3 lines; SHA-256 `b405aca6de4c546cd1bafc94cb0559239ef83b0d5939244c078b9659c1f8f899`) | Remove the host log locator and exact entry reference; preserve the conclusion about the public manual without identifying the local history record. |
| **S3 — host configuration value/path** | `.ufo/waves/round-17/falsify/ReopenPacmanLog.md:105,111` (2 lines; same file/hash as above) | Remove the host-specific configuration observation and temporary configuration filename from the argv discussion; retain only the public-documentation/root-path distinction. These do not match R6's `sudoers` token or R7's OMP `config.yml` forms. |
| **S2 — repeated host package-log output** | `.ufo/waves/round-17/falsify/ReportTrace.md:47` (1 line; same SHA-256 as above) | Remove the specific transaction times, command summaries, and package identity; retain only the non-sensitive cross-link result. This repeats the host-log event summary in the routed baseline `PacmanActorTrace.md:21-27`. |
| **S2 — host package history/state** | `.ufo/waves/round-17/falsify/StaleSupersession.md:7,16-17,37,50-54,75-80,83,109` (17 lines; SHA-256 `51be7690b9d17b823bd7753f4a64cfe94ad78e5d568178ed852b6ffa17d0dd06`) | Remove exact package-version, package-query, log-entry, and transaction-time details. The supersession conclusion can remain as relative chronology without host versions or log offsets. Lines 50-53 repeat part of the host-log event covered by routed `PacmanActorTrace.md:21-27`. |
| **S4 — prior live-capture timing/provenance** | `.ufo/waves/round-17/falsify/StaleSupersession.md:55-59` (5 lines; same SHA-256 as above) | Coarsen the capture timestamp and commit timing to “before the package transition”; the exact observation chronology is unnecessary for the correction claim. |
| **S4 — live journal-window result** | `.ufo/waves/round-17/falsify/StaleSupersession.md:65-68` (4 lines; same SHA-256 as above) | Remove the specific finding/result and record count from the earlier live capture; retain only that the older summary conflicts with a prior capture. This is a prior live measurement, not a fresh query in this sweep. |
| **S2 — host package/query facts repeated across build material** | `.ufo/waves/round-17/falsify/TrendGrounding.md:88,93,97,100,108-118,209-212,228-230,240-241` (24 lines; SHA-256 `f3208ac8f93dfc144f103a2540f3bfe85dd2bf13b0dd9c9a83b2bfc840a6ef3e`) | Remove exact package versions, timestamps, host-query references, and log offsets; preserve the stale-index/citation-mismatch finding without host-state details. The same transaction-start event is repeated at `:111` and overlaps the routed `PacmanActorTrace.md:21-27`; the added version/timing details are attributed in this report to other build receipts. |

The lines above total **55 line occurrences** across four target files. They contain no credential, token, OMP session-directory identity, numbered tool-log identity, or raw transcript excerpt observed in this sweep.

## Repeats from the three routed build reports

The comparison uses the original blobs present at `d005cdd`, not later replacement text. The frozen policy names these three paths at `frozen/c1-policy.json:18-20`.

| Routed source at base `d005cdd` | Original line count | Original SHA-256 | Repeat result in the 14 falsify artifacts |
|---|---:|---|---|
| `.ufo/waves/round-17/build/PacmanActorTrace.md` | 157 | `109e92f4d846c80d08a7ccb18c51dd42d1c0aabb9e921709515421c5f79097ef` | **Repeated:** package-log event summary in `ReportTrace.md:47`, `StaleSupersession.md:50-53`, and the transaction-start reference in `TrendGrounding.md:111`; `ReopenPacmanLog.md:78` also repeats the host-log entry locator. The target reports do not repeat the routed file's session identity or tool-log identity. |
| `.ufo/waves/round-17/build/OmpRetryConfig.md` | 223 | `d6340be91155b713e327f310f6b1f82eefe8746d46c6455b61fa8fb7392b2ec7` | **No exact private-value repeat found.** `WaveContextHashes.md:65-76` discusses the absence of model parameters; `ReopenZai.md:53-68,78-108` discusses public/vendor 429 classification and code behavior. Neither reproduces the routed configuration or model-routing values. |
| `.ufo/waves/round-17/build/SessionExitCorrelation.md` | 137 | `437b902fbc1c74174e06549a107e2dfbab315d8bca0dcfc55dde36175a57a7bf` | **No exact session-record value, session identity, or cross-tab repeat found.** `ReportTrace.md:35` is a separate aggregate scan result and is flagged independently under S1; shared terminal-class vocabulary is not a repeat of the routed record values. |

## File inventory and clean files

“Clean” below means no private context in the requested categories was identified; it is not a claim that the report has no ordinary repository, public-source, or test-output detail.

| Requested file | Lines | SHA-256 | Sweep result |
|---|---:|---|---|
| `.ufo/waves/round-17/falsify/ReopenJjAuthor.md` | 170 | `87d6ecb815d338bcab0c8ab2843b579c46e32a27bf6c0ce2fdbd93d3d6206c03` | Clean |
| `.ufo/waves/round-17/falsify/ReopenJjCompat.md` | 127 | `238cbf86cea8b35ca5ce9629ce76de8ec17d2e67827dd12e8ef91e24c92b0556` | Clean |
| `.ufo/waves/round-17/falsify/ReopenPacmanLog.md` | 170 | `b405aca6de4c546cd1bafc94cb0559239ef83b0d5939244c078b9659c1f8f899` | Findings: S2/S3 |
| `.ufo/waves/round-17/falsify/ReopenRfc6585.md` | 163 | `52cd48d5c0aec509026e0d62490b124527debf2eebc990bb37dc2f08b734c279` | Clean |
| `.ufo/waves/round-17/falsify/ReopenRfc9110.md` | 134 | `6c46cd849a42a57955f96935338f26fcb53f08d628a37ad360abdf53eba7a0db` | Clean |
| `.ufo/waves/round-17/falsify/ReopenZai.md` | 179 | `741279a11831b2d4d32aae5498004188484fa5205ddcebf1a228c2e43ea5052d` | Clean |
| `.ufo/waves/round-17/falsify/ReportTrace.md` | 148 | `649f5990c3a31d0dff5d3de70d895bc24c4c738e4b1edafd1f5fd534bb2e638c` | Findings: S1/S2 |
| `.ufo/waves/round-17/falsify/SandboxFinal.md` | 64 | `aa1d710da37dd32d1937a7365e16e5b085ec71666fc80d7b7c4be4fd42cdba41` | Clean |
| `.ufo/waves/round-17/falsify/SeparateThree.md` | 134 | `2b96a884d902a8e4816ed4fb5925ad8fc9d0759b93960f80beaea1a3eef85ec2` | Clean |
| `.ufo/waves/round-17/falsify/SourceCensus.md` | 144 | `f8e4b1403d757a6ced2640d23d9ab14aceedd62460a3c6afebe81edd37010c03` | Clean |
| `.ufo/waves/round-17/falsify/StaleSupersession.md` | 116 | `51be7690b9d17b823bd7753f4a64cfe94ad78e5d568178ed852b6ffa17d0dd06` | Findings: S2/S4 |
| `.ufo/waves/round-17/falsify/TrendGrounding.md` | 253 | `f3208ac8f93dfc144f103a2540f3bfe85dd2bf13b0dd9c9a83b2bfc840a6ef3e` | Findings: S2 |
| `.ufo/waves/round-17/falsify/WaveContextHashes.md` | 158 | `c1a686ec3ded462de783eb9ea13b415279fd33350ca7284c891ebd5d2c30464b` | Clean |
| `.ufo/waves/round-17/falsify/swarm-registry.json` | 393 | `eae51027fcdc069a7a65a6027029f9b4350b08d40205a0c9423210fdfe259791` | Clean |

## Command record and limits

- Read-only `git -C <lane> show d005cdd:<path> | sha256sum` and `wc -l` were used for the 14 target blobs and three comparison blobs; hashes and line counts returned for all requested paths (rc 0). No VCS mutation.
- Focused `functions.grep` searches over the 14 target paths for frozen R1-R9 patterns, credential-like forms, and the named session/routing field families returned no matches; the specialized search tool does not report a numeric process exit code.
- No tests, builds, gates, live probes, or network requests were run. No tool was installed or updated. No file other than this scoped report was written.