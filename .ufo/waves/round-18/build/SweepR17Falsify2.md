# Round-17 falsify report privacy reading sweep

## Scope and method

Read all 17 requested reports under `.ufo/waves/round-17/falsify/` in full: `CaseReview17.md`–`CaseReview27.md`, `CensusNewBranches.md`, `ConformanceAudit.md`, `CountC1.md`, `CountC2.md`, `CountC3.md`, and `CriticC1Final.md`. Re-read every line the reader truncated. Reviewed the frozen C1 policy and its population snapshot at `d005cdde0e009dea6c0cc29b37163de536528658`; the regex is a recall floor, not the scope of this review. The report-level SHA-256 values below identify the frozen blobs; private text is not reproduced.

The frozen population has 8 class hits on 5 lines in the requested set, all in `ConformanceAudit.md`; the other 16 requested files have no R1–R9 hit. Those existing hits do not cover the additional values and identities noted below.

## Lines retaining private context not fully captured by R1–R9

Redaction suggestions remove the sensitive detail while retaining only a finding-level summary. `[INFERENCE]` marks a conservative classification of local operational metadata rather than an observed secret.

| Lane-relative path:line | Kind / C1 status | Minimal-redaction suggestion |
|---|---|---|
| `.ufo/waves/round-17/falsify/CensusNewBranches.md:55-67` | `[INFERENCE]` Private operational/session-history facts derived from a fleet watchdog log: source path, event-window pairing, exact lane/round aggregates and timing-derived proportions. No R1–R9 hit. | Remove the log path and exact counts, proportions, lane breakdowns, and timing detail; retain only the general conclusion about the reachable-check window. |
| `.ufo/waves/round-17/falsify/CensusNewBranches.md:119-123` | Other-session diagnostic/tool-output excerpt: a raw Git trace and its machine-local time, plus the corresponding command/control comparison. No R1–R9 hit. | Replace the trace and exact time/environment detail with the outcome: trace output precedes the parsed Git result and changes the first-line branch. |
| `.ufo/waves/round-17/falsify/CensusNewBranches.md:148-162, 241-253, 261-266` | `[INFERENCE]` Live fleet/repository configuration and branch-state inventory, including a root branch and per-lane branch/config correspondence. This is not OMP model routing, but is internal environment state and has no R1–R9 hit. | If fleet topology is not intended to be public, remove branch names and the lane-to-branch mapping; retain only aggregate counts and the behavior under test. |
| `.ufo/waves/round-17/falsify/ConformanceAudit.md:36` | Private repository-operation history: a specific operation identifier and time. No R1–R9 hit. | Remove the operation identifier/time; retain only that a prior lane read caused a working-copy snapshot. |
| `.ufo/waves/round-17/falsify/ConformanceAudit.md:38` | Private session-directory/file identity: a timestamped interactive-session directory and transcript glob, outside the frozen session-store path/name patterns. No R1–R9 hit. | Remove the timestamp and complete directory/file pattern; retain only that a lane-resident transcript copy existed. |
| `.ufo/waves/round-17/falsify/ConformanceAudit.md:39` | Private session identity and host-event correlation: a session-name fragment with a personal-document cue, package-transaction timing/details, and a system invocation identifier. The identity does not match R1; no class hit on this line. | Remove session and invocation identities and exact host-event correlation/timing; retain only a generic statement that a separate report cited a host-level event. |
| `.ufo/waves/round-17/falsify/ConformanceAudit.md:43` | Non-allowlisted session-record reason/kind values. R9 matches field-name tokens but not the reported values. Line SHA-256: `f41f1d13d0350d0b30336118bdf7b3189fdd52b8a6664a34a9ba316eed7b48a8`. | Replace all values with “non-allowlisted session-exit fields were read/reported”; do not preserve the value pair. |
| `.ufo/waves/round-17/falsify/ConformanceAudit.md:44` | Operator OMP configuration/model-routing context: configuration path/line-range references and a statement that model-change strings were reported. R7 and R9 catch a path/key, not any corresponding values. Line SHA-256: `8de187ab2fabfdb923a1dde890dc46e0b6dcd772f46eb2c7c0ccda3e9af2a319`. | Remove the configuration location/line references and all model-change detail; retain only that private configuration-backed output was disclosed. |
| `.ufo/waves/round-17/falsify/ConformanceAudit.md:46` | Session-store root and numbered tool-output artifact identities, plus shell-history/login-record and privileged-configuration read facts. R3/R5/R6 hit this line; R2 misses the store root itself. Line SHA-256: `22465d90379d23601814115ba9250f4f5308d1066e212c9410b0a1f7b275af4a`. | Remove the store root, artifact names/IDs, and exact history/privileged-file references; retain only the abstract finding that restricted sources were inspected. |
| `.ufo/waves/round-17/falsify/ConformanceAudit.md:47` | Private user-configuration read activity (raw configuration access is reported, but no setting value is reproduced). No R1–R9 hit. | Remove the raw-read/path detail; if needed, retain only a generic configuration-scope finding. |
| `.ufo/waves/round-17/falsify/ConformanceAudit.md:48` | `[INFERENCE]` Session-record-derived value summaries for retry-related fields (distribution/range disclosure is described, even where exact numbers are not repeated). No R1–R9 hit on these field forms. | Remove distributions and timestamp-range disclosure; retain only that a non-allowlisted value summary was reported. |
| `.ufo/waves/round-17/falsify/ConformanceAudit.md:53-54` | Private host/package-operation history and a specific transaction reference; this is not a transcript value, but is copied operational-log detail. No R1–R9 hit. | Remove exact transaction/path/timing detail; retain only the scoped host-event handoff. |
| `.ufo/waves/round-17/falsify/ConformanceAudit.md:72` | Credential-adjacent incident metadata: says a credential-class record line was displayed, but this report does not reproduce credential contents. No R1–R9 hit. | Replace with a generic “credential-bearing record exposure was reported”; keep no record type or transcript detail. |
| `.ufo/waves/round-17/falsify/ConformanceAudit.md:74-75` | Repeat summaries of the session-record and model-routing disclosures at lines 43–44. R9 hits both lines. Line SHA-256: line 74 `615eb07331c47fe324e42354d643ab63ef95d0410cb5495c9baf1ed7ee5abd17`; line 75 `9634076935132e1cdbcf3d06aef5e5e93ba0536e7c10c1167b02e54c0ae40e02`. | Replace both rows with non-value-bearing incident labels; do not restate fields or model-change details. |
| `.ufo/waves/round-17/falsify/ConformanceAudit.md:80` | Repeats that session content and privileged host reads were exposed/performed. No direct values, but retains the sensitive incident facts. No R1–R9 hit. | Reduce to a generic incident ID/status; remove the source-specific activity detail. |
| `.ufo/waves/round-17/falsify/ConformanceAudit.md:119-120` | Repeats credential-record exposure and retention of a transcript copy; no credential value is printed. No R1–R9 hit. | Remove record type and transcript-retention reference; retain a generic incident closure note. |
| `.ufo/waves/round-17/falsify/ConformanceAudit.md:121-123` | Repeats the host transaction and session-attribution material from line 39. No R1–R9 hit on these repeated details. | Remove exact host action/actor-attribution details; retain only a generic unresolved host-scope note. |
| `.ufo/waves/round-17/falsify/CountC3.md:12,19,23,30` | Other-session command/output identity: exact absolute path of a sibling worktree appears in command lines and captured JSON output. No OMP session data or secret is present, but this exposes another seat’s sandbox identity and raw tool output. No R1–R9 hit. | Replace the worktree path with `[sandbox]`; keep only the finding/count fields needed for the recount and omit the raw command/output envelope. |
| `.ufo/waves/round-17/falsify/CriticC1Final.md:22-24, 29-38` | Live session-receipt aggregates and session-record-derived field values (terminal-time ages, error-code/retry facts, and inventory summaries). These are not synthetic fixture facts; no R1–R9 hit. | Remove exact field values, counts, and timing ranges from the live receipt; retain only the qualitative conclusion and identify the evidence as an aggregate receipt. |
| `.ufo/waves/round-17/falsify/CriticC1Final.md:113-123` | Live session payload-shape/size measurements and the associated truncation inference. No R1–R9 hit. | Remove exact byte measurements and corpus-specific boundary details; keep only the general tail-coverage risk. |
| `.ufo/waves/round-17/falsify/CriticC1Final.md:127-131` | Live session-directory inventory counts and filtered-scan counts. No R1–R9 hit. | Remove exact inventory/scan counts or replace with a coarse coverage statement. |

### Frozen-class hits present in the requested set

These are not metric misses, but they contain additional values/details beyond the literal tokens the frozen regex catches. All paths below are relative to the lane. The reported line hashes are from the frozen C1 population, not hashes of private content reconstructed here.

| Path:line | Frozen class(es) | Line SHA-256 |
|---|---|---|
| `.ufo/waves/round-17/falsify/ConformanceAudit.md:43` | R9 `session_record_value` | `f41f1d13d0350d0b30336118bdf7b3189fdd52b8a6664a34a9ba316eed7b48a8` |
| `.ufo/waves/round-17/falsify/ConformanceAudit.md:44` | R7 `operator_config_ref`, R9 `session_record_value` | `8de187ab2fabfdb923a1dde890dc46e0b6dcd772f46eb2c7c0ccda3e9af2a319` |
| `.ufo/waves/round-17/falsify/ConformanceAudit.md:46` | R3 `tool_output_artifact`, R5 `shell_history`, R6 `privileged_config` | `22465d90379d23601814115ba9250f4f5308d1066e212c9410b0a1f7b275af4a` |
| `.ufo/waves/round-17/falsify/ConformanceAudit.md:74` | R9 `session_record_value` | `615eb07331c47fe324e42354d643ab63ef95d0410cb5495c9baf1ed7ee5abd17` |
| `.ufo/waves/round-17/falsify/ConformanceAudit.md:75` | R9 `session_record_value` | `9634076935132e1cdbcf3d06aef5e5e93ba0536e7c10c1167b02e54c0ae40e02` |

## Repeats of the three routed build reports

`ConformanceAudit.md` re-exposes facts that the frozen C1 population associates with the three routed reports. The repetition locations are listed here without reproducing the protected values:

- `build/SessionExitCorrelation.md` — source SHA-256 `437b902fbc1c74174e06549a107e2dfbab315d8bca0dcfc55dde36175a57a7bf`; frozen population: 5 hits on 4 lines (R1=1, R2=1, R9=3). Repeated in `falsify/ConformanceAudit.md:43,74` (session-exit field values/disclosure).
- `build/OmpRetryConfig.md` — source SHA-256 `d6340be91155b713e327f310f6b1f82eefe8746d46c6455b61fa8fb7392b2ec7`; frozen population: 17 hits on 16 lines (R7=5, R8=8, R9=4). Repeated in `falsify/ConformanceAudit.md:44,75` (operator configuration/model-change disclosure).
- `build/PacmanActorTrace.md` — source SHA-256 `109e92f4d846c80d08a7ccb18c51dd42d1c0aabb9e921709515421c5f79097ef`; frozen population: 18 hits on 17 lines (R1=3, R2=2, R3=7, R4=1, R5=3, R6=2). Repeated in `falsify/ConformanceAudit.md:39,46,54,80,121-123` (session/tool-output identity, privileged-source activity, and host-event attribution).

The three routed source files account for all 40 frozen hits under `must_redact_paths`. The repeated facts remain in the falsify report even though they are outside those routed files.

## Clean files and exclusions

Clean against the private-context categories in this assignment (no real session identity, private session/document/history/config content or values, credential material, or non-allowlisted live-record values retained):

- `.ufo/waves/round-17/falsify/CaseReview17.md` through `CaseReview27.md`
- `.ufo/waves/round-17/falsify/CountC1.md`
- `.ufo/waves/round-17/falsify/CountC2.md`

`CaseReview21.md` discusses a synthetic credential-record fixture and the no-read requirement, but contains no credential value. `CaseReview25.md` contains a timestamp-shaped **synthetic fixture** filename, not an observed session identity. The remaining CaseReview reports concern fixtures, contracts, and retained case-test outputs; no private operator/session values were found. No credential contents or OMP model/routing values are present in the reviewed falsify reports; ConformanceAudit only repeats the existence/type of such disclosures.

## Provenance and activity

- Frozen policy: `.ufo/waves/round-18/frozen/c1-policy.json`; frozen population: `.ufo/waves/round-18/frozen/c1-population.json` (`d005cdde0e009dea6c0cc29b37163de536528658`).
- Frozen report SHA-256: `CensusNewBranches.md` `c4a292e9cd88ce84b203b6285073e469ca9667c3a06cf6e919422a18db3489b3`; `ConformanceAudit.md` `cb90b3cd64871823abcd4bb0f39e5b193e0106408541bad038091a3167ee5167`; `CountC3.md` `b1782bb83a81702d4b72752b501ba2873d6475720759c2e340c4f45c7be5d116`; `CriticC1Final.md` `b2a4adad41773aa2dc52b70ed35dfd410664f5cf62291eb2c10f2584d5d7a3a6`.
- Read-only hash command pattern: `git -C <lane> show d005cdde0e009dea6c0cc29b37163de536528658:<path> | sha256sum`; seven blob hashes were emitted, each with `rc=0`. No builds, tests, installs, VCS mutations, shell-history access, transcript-store access, or host-log queries were performed.

Report: .ufo/waves/round-18/build/SweepR17Falsify2.md
