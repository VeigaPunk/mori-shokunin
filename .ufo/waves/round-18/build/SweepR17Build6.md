# Round-17 build-report privacy sweep (manual / outside C1 regex metric)

## Scope and method

Swept the 11 requested committed blobs at `d005cdde0e009dea6c0cc29b37163de536528658` (1,361 lines total), reading the reports fully and comparing only the relevant sections of `PacmanActorTrace.md` and `OmpRetryConfig.md` to identify repeated facts. This report contains no excerpts, values, session identities, transcript filenames, tool-log IDs, or credentials from the source reports. The manual classes below are this sweep's labels, not additions to frozen C1 classes. C1's frozen policy explicitly describes the regexes as a recall floor (`.ufo/waves/round-18/frozen/c1-policy.json:29`).

The worktree copy of `SessionExitCorrelation.md` changed during the sweep; findings and line numbers below refer to its committed d005 blob (137 lines; SHA-256 `437b902fbc1c74174e06549a107e2dfbab315d8bca0dcfc55dde36175a57a7bf`), not the later working-tree replacement.

Manual classes: **M1** session identity/store and filesystem facts; **M2** non-allowlisted session-record or transcript-derived output; **M3** operator retry/model-routing or provider-specific values; **M4** other-lane document/history identity or content hints; **M5** local privileged/package-manager output; **M6** credential-store path/layout. Counts below are nonblank lines in the listed ranges; ranges can include blank lines. Mixed lines that also contain a frozen-regex match remain listed where they carry additional context outside the match.

## Findings requiring redaction

| Committed report (line count; blob SHA-256) | Lines and manual class | Minimal redaction |
|---|---|---|
| `.ufo/waves/round-17/build/SentinelTranscripts.md` (218; `c8ad0dbd98bf7df6acea3ab659b617ff50b759ce66acb80ed9e26d0333cc68fe`) | **84 lines**: `19-21, 29-33, 37-77, 134, 144-150, 160-162, 165-179, 184-191, 196-200`. M1/M2: private session-store permissions and corpus inventory; an incidental transcript-copy identity and record metadata; transcript sizes, record/key inventories, terminal/error/retry aggregates, provider/model-derived facts, corpus drift and file-stem counts. **M6** also applies to `97`, which gives a credential-store path example. | Remove session-store/copy identities, access metadata, record/key details, all corpus-derived counts and values, and the credential-store path example; retain only the generic security/design findings and synthetic test requirements. |
| `.ufo/waves/round-17/build/SessionExitCorrelation.md` (137; `437b902fbc1c74174e06549a107e2dfbab315d8bca0dcfc55dde36175a57a7bf`) | **97 lines**: `4-7, 11-18, 29-32, 36-56, 60-80, 84-103, 107-117, 121-128, 132-134`. M1/M2/M3: original task/scope and live snapshot details; non-allowlisted fields consulted; the full session-derived cross-tab, terminal/error aggregates, provider/model facts, per-file identities and positions, drift/tail findings, runtime/scope observations and command results. | Remove the session/task identity and snapshot particulars, every field value and file-specific detail, and the tables/counts; retain only a non-identifying statement of the methodological conclusion. |
| `.ufo/waves/round-17/build/SiblingSeatDeathTools.md` (184; `fd60ded4c2fab983827212d35ad199d084b3f7cd9828c1fce318113a103557b9`) | **8 lines**: `99-106`. M3: provider-specific error/retry examples, affected-seat and lane observations, and retry-configuration values. | Delete the provider/retry examples and configuration values; keep only the generic observation that the referenced prose is not an executable detector. |
| `.ufo/waves/round-17/build/SkillRegistry.md` (400; `60f6aaef6c499b57e5222cd149b8c4cd5922d9f056f9bb1326479196e1a2e7ba`) | **7 lines**: `119-123, 371-372`. M4: another lane's historical artifact identity, size and a first-line content-category hint, repeated in the command log. | Remove the other-lane artifact identity, size and content hint; retain only the generic fact that the old query missed a fleet-root candidate. |
| `.ufo/waves/round-17/build/SrcPacmanLog.md` (47; `06eefcbb2778d238685db88f1b507a2d1ad6b9e8ce4f6025a316630a74291e81`) | **6 lines**: `28-34`. M5: local package-log metadata and an invocation example, plus local account/scriptlet and time-zone observations. | Remove the host-log measurements, invocation and account/time-zone details; keep the documentation-based conclusion without local log output. |
| `.ufo/waves/round-17/build/SrcRfc9110.md` (90; `47bc489853a6a82d8fef35756ba6e504d6755bb33cbeaa473c221664204166d0`) | **14 lines**: `55-68`. M2/M3: provider/client-specific retry behavior, error-code context, retry-message data and transcript-field limitations. | Remove the provider-specific retry/error example and the derived runtime details; retain the RFC-only scope statement. |

The listed ranges total 216 nonblank findings across six reports. Frozen-pattern overlaps within the findings are: `SentinelTranscripts.md:40,173` (R9), and the committed `SessionExitCorrelation.md:5,12,30` (R9; R1/R2; R9 respectively). These matches do not cover the additional context on those lines. No credentials or raw transcript text were present in the reviewed excerpts; the sensitive retention is principally identifiers, record-derived values and paraphrased tool output.

## Repeated facts

- `SrcPacmanLog.md:28-34` repeats the package-log/actor-attribution limitation also reported in `PacmanActorTrace.md:21-27,123-129` (source blob SHA-256 `109e92f4d846c80d08a7ccb18c51dd42d1c0aabb9e921709515421c5f79097ef`). The report's local log observations add host-specific material beyond that shared conclusion.
- `SentinelTranscripts.md:64-75,165-179` and `SessionExitCorrelation.md:22-32,60-70` repeat or overlap the retry/error-field and provider-derived observations in `OmpRetryConfig.md:87-93,116-164` (source blob SHA-256 `d6340be91155b713e327f310f6b1f82eefe8746d46c6455b61fa8fb7392b2ec7`).
- `SiblingSeatDeathTools.md:99-106` and `SrcRfc9110.md:55-68` repeat provider/retry examples and conclusions also present in `OmpRetryConfig.md:87-93,116-131,151-164`. `SkillRegistry.md:185` repeats a subset as an explicitly synthetic test vector; that line contains no observed session value and is not independently classified as private.
- No other requested report repeats the unique disposal-marker cross-tab or per-file identities from the committed `SessionExitCorrelation.md` blob. Direct filename-reference search over the 11 targets found no mentions of the three repeat-source filenames; the repeats above are content-level overlaps.

## Clean files

No manual-only private context in the requested categories was found in these five reports. Their local branch/version observations, public-source material and configuration key names did not disclose operator configuration/model values or session-record values.

| Clean committed report | Lines | Blob SHA-256 |
|---|---:|---|
| `.ufo/waves/round-17/build/SrcGitMergeBase.md` | 39 | `8d6cf4a5cbf1356888d8c414ce2f4f126efde01a82fde21db26111aabc968580` |
| `.ufo/waves/round-17/build/SrcGitSymbolicRef.md` | 54 | `78349cdf6f60742b7e7a90a3cdb876f8d298676de2de63478f9831b720a444b7` |
| `.ufo/waves/round-17/build/SrcJjGitCompat.md` | 109 | `f17e31b1fe8fd68398fa84dbcbe7c90782523b6024f637890e6ec2cbd07b6508` |
| `.ufo/waves/round-17/build/SrcJjMetaedit.md` | 49 | `057a248e213e99e5c2f38db214202dc68294ae96f015dc81d3042c5b09ce8249` |
| `.ufo/waves/round-17/build/SrcRfc6585.md` | 34 | `bbec02a2f68d96754dca91dc649b1b7d41482d13d3bd01f36797fc53eb2324fe` |

## Provenance and checks

- Read the round-18 contract and its frozen C1/C2/C3 inputs; read all 11 requested committed report blobs. The two additional repeat-source reports were read only for classification.
- Read-only command family, all exit 0: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show d005cdde0e009dea6c0cc29b37163de536528658:<lane-relative-path> | sha256sum` and the corresponding `| wc -l` for each requested blob; also `sha256sum`/`wc -l` for the requested worktree files. Repeat-source blob hashes came from the same read-only `git show | sha256sum` form.
- No URLs fetched, tools installed or updated, transcript stores opened, VCS mutations performed, or tests run.
