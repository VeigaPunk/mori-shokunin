source: S041 — https://www.rfc-editor.org/rfc/rfc6585 §4; S043 — https://docs.z.ai/api-reference/api-code Error codes 1302, 1113, 1308; measured OMP shapes and counterexamples in .ufo/waves/round-17/build/{TranscriptShapes,RetryRecoveryShape,CriticC1}.md.
verified-at: 2026-10-20 — source-opening receipts .ufo/waves/round-17/build/Src{Rfc6585,ZaiErrorCodes}.md; delivered-tool fixture and live measurements are recorded in corpus/lessons/round-17.md and its run manifests (this header does not certify all OMP versions).
recheck: python3 tools/mori-seat-terminal.py --selftest; python3 tools/mori-round17-seat-regressions.py --tool tools/mori-seat-terminal.py --fixtures .ufo/waves/round-17/fixtures/seat --output .ufo/waves/round-17/evidence/recheck-seat (fresh output directory required).

# Terminal-at-scan seat observation — round 17

## Ground and decision table

This advances FR14 only as passive observation of transcript files, not as an orchestration
result contract. `tools/mori-seat-terminal.py` reads a bounded tail and classifies the last
`type=message` record, never every error anywhere in the file. Earlier error records may
carry retry recovery and be followed by successful output. `session_exit kind=normal` is
not a success signal: the round's field-only survey found it on error-terminal files too.

| Last observed message | Class | What it does not establish |
|---|---|---|
| assistant / stop | completed | task correctness or admission |
| assistant / aborted | aborted | external cause or process kill |
| assistant / error younger than settle window | error_unsettled | that retrying has stopped |
| older error, Z.AI type 1113/1308 or quota token | dead_quota | a permanently dead seat |
| older error, type 1302 or rate-limit/429 token | dead_rate_limit | an incident count or no future resume |
| older error otherwise | dead_error_other | OOM or host health |
| toolResult, user, developer or another nonterminal role | incomplete | still-running process liveness |
| unknown schema, unreadable file, no complete message in tail | unavailable | zero activity |

S043 is operational, not decorative: Z.AI documents both rate-limit and usage/balance
causes under HTTP 429. Business-code and quota tests precede the generic 429 test. RFC
6585 grounds the generic status meaning, not the vendor business cause or OMP recovery.

## Identity, scope and output

Each relative transcript path is a separate observation key, so duplicate stems do not
overwrite one another. Main-session filenames are counted separately, not as subagent seats.
Prefix matching is exact naming convention, not authenticated membership; `SoujiR17-3` is
not `SoujiR17`. A requested prefix matching nothing is setup, never a clean lane report.

The supported transcript header is version 3. The default tail bound is 512 KiB; larger
terminal lines can still become unavailable. Regular files only; no symlink/FIFO traversal.
Only status fields, provider/model labels and numeric retry/error-code metadata are emitted.
No transcript content, errorMessage text, credential-pin record or usage is printed.

## Limits retained after first-wave falsification

- `dead_*` is retained compatibility vocabulary for an **aged terminal error at scan time**.
  Seats have resumed after such records. The default 900-second settle window is a local
  observation policy, not a proof they cannot resume or a host retry timeout.
- One upstream capacity incident can affect many seats. Counts are transcript observations,
  not incidents. Cross-tabulations are views of the same observations, never summed together.
- A scan is not atomic across mutable files. Current observations can change on re-scan.
- Error-string tokens are heuristic outside the explicitly mapped Z.AI codes. They are not
  kumitate's dispatch/fallback decisions. MorI never routes, retries, resumes or replaces seats.
- Exit 0 means no aged `dead_*` found, not healthy: inspect incomplete, unsettled and unavailable.
- No emitter authentication, complete transcript retention or universal schema stability is claimed.

The knowledge entry is admitted only at the finite scope measured in the round-17 lesson.
Any independent closure remains outside the author lane.

## A2 precision after fresh falsification

The initial implementation's timestamp-free errors were not proved older than
the settle window. Final classification makes them unavailable with reason
`terminal-time`, never an aged error. A root symlink or failed traversal is
setup, not a clean empty scan. Safely opened regular descriptors and selective
JSON field projection keep content/usage/credential-pin payloads unmaterialized.
Permitted session-version and timestamp fields support schema/age checks only.

The code mapping is explicitly Z.AI-scoped. S043 does not document OMP's
`(type=NNNN)` text wrapper: equating that token to a business code is
**[INFERENCE]**, not authenticated cause. Only the selected known code rules
are claimed; an unknown Z.AI business code under HTTP 429 without explicit
rate/quota text is an unspecified error, not a guessed rate-limit cause.
Bare `resource_exhausted` likewise does not identify which resource limit was
reached. This narrows cause attribution while retaining the full error count.

The old decision-table rows are superseded for these cases; final committed
measurements and expanded independent expected fields are in the round-17
lesson. Error text is reduced immediately to the permitted flags/code/counts;
neither the raw string nor other transcript payload is retained in the view.

No-follow scope is the selected root's final component and descriptor-relative
descendant traversal/opening. The caller selects the root; OS resolution of
symlinks in its ancestor pathname is not an authenticated-root guarantee.
Use a trusted canonical root for observation. A final-root symlink is rejected.
