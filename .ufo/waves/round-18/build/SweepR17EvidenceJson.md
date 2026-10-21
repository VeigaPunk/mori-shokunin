# Round-17 machine JSON privacy sweep

## Scope and method

Scanned the frozen tip `d005cdde0e009dea6c0cc29b37163de536528658`: all 2,006 tracked blobs under `.ufo/waves/round-17/evidence/` and exactly 20 tracked top-level `*.json` files in `.ufo/waves/round-17/`. The `git grep -nE` scans used each class regex from `frozen/c1-policy.json:6-15` and the seven requested extra tokens. Output was reduced to lane-relative `path:line` before display; no matched values are reproduced here. Counts below are matching lines, not unique values, and scans overlap.

Read-only inventory commands exited 0: `git ls-tree -r ... evidence | wc -l` (2,006); root-level JSON enumeration (20); whole-repository `.jsonl` path count (86). Final grep scans exited 0 for positive matches and 1 for no matches; there were no evaluation errors. The policy scope and its recall-floor limitation are documented at `frozen/c1-policy.json:5,27-29`.

## Frozen class results

| Class | Matching lines | Result / path:line samples |
|---|---:|---|
| R1 `session_identity` | 8 | Retained-private-context candidate; 2 lines in `evidence/seat-live.json:9,23`, 3 in `wave1-dispatch.json:502,507,707`, 3 in `wave1-spec.json:50,55,255`. |
| R2 `session_store_path` | 0 | No match. |
| R3 `tool_output_artifact` | 0 | No match. |
| R4 `private_document` | 0 | No match. |
| R5 `shell_history` | 0 | No match. |
| R6 `privileged_config` | 0 | No match. |
| R7 `operator_config_ref` | 2 | Path-reference-only class hits in `wave1-dispatch.json:522` and `wave1-spec.json:70`; these are inside task-prompt string fields. No configuration contents were read. |
| R8 `routing_table_key` | 2 | Key-name matches at the same two prompt lines as R7; the scan does not establish that a routing value is present. |
| R9 `session_record_value` | 2 | Field-name matches in task prompts at `wave1-dispatch.json:607` and `wave1-spec.json:155`; the scan does not establish a session-record value. |

R1 locations were also mapped without outputting string values: `evidence/seat-live.json` matches are in its `argv[3]`/`stdout` string fields; the other six are in task-prompt strings in the two wave-1 JSON manifests. These files are not under the dedicated synthetic fixture root. **Classification:** treat the eight R1 hits as retained session-identity context until an authorized redaction is applied. The pattern has high-confidence session-identity syntax per the frozen policy; whether each value is synthetic cannot be proven without inspecting prohibited session material. R7 is a private path reference, not evidence of a config value. R8/R9 are prompt-level key/field mentions; any additional value in the same prompt remains unassessed.

The non-author ruling at `corpus/lessons/round-17-verifier-spotcheck.md:333-336` concerns a separately named safe projection. It should not be generalized to `evidence/seat-live.json`, where R1 hits remain.

## Extra-token results and family classification

| Token family | Matching lines | Observed classification / samples |
|---|---:|---|
| Operator-home-prefix token (value intentionally not repeated) | 13,669 | 750 are in `evidence/mutations/*` (synthetic mutation-fixture paths). Another 3 are in `evidence/seat-live.json`, 12,772 in other evidence, and 144 in top-level JSON. Treat those 12,919 non-mutation hits as retained private-path candidates; **[INFERENCE]** some preserved test output may echo synthetic paths, which this value-suppressed sweep cannot distinguish. Samples: `evidence/r13-preserved/evidence.json:4662`, `evidence/final/r14-preserved/evidence.json:6929`, `wave1-dispatch.json:712`. |
| `sessions` | 2,276 | 350 in mutation fixtures; 1,909 in other evidence, 3 in `seat-live.json`, 14 in top-level JSON. The frozen R2 session-store-path class is zero; this broad token alone is not a session-store leak. Sample: `evidence/r13-preserved/evidence.json:2998`. |
| `.jsonl` | 2,032 | 278 in mutation fixtures; 1,748 in other evidence; 6 in top-level JSON. These are string hits in machine evidence, not a count of retained transcript files. Sample: `evidence/r13-preserved/evidence.json:57`. |
| `Documents` | 0 | No match; consistent with R4=0. |
| `config.yml` | 2 | Same two R7 path-reference lines above; no config contents were read. |
| `model` | 517 | 220 in mutation fixtures; 283 in other evidence, 1 in `seat-live.json`, 13 in top-level JSON. Broad schema/test term, not by itself a private routing value. Sample: `evidence/mutations/MutQuota/pristine/runs/fifo_skipped.stdout:1`. |
| `provider` | 463 | 217 in mutation fixtures; 237 in other evidence, 1 in `seat-live.json`, 8 in top-level JSON. Broad schema/test term, not by itself a private provider value. Sample: `evidence/mutations/MutQuota/pristine/runs/fifo_skipped.stdout:1`. |

**Synthetic-fixture check:** independently counted all tracked `.jsonl` paths at the frozen tip across the whole repository: 86 total, all 86 under `.ufo/waves/round-17/fixtures/`, zero elsewhere. This re-confirms the spot-check statement at `corpus/lessons/round-17-verifier-spotcheck.md:333`. The `.jsonl` token hits in the requested evidence/manifest scope do not contradict that result: the scan scope contains references to the suffix, while the tracked `.jsonl` files themselves are fixture-rooted.

**Redacted projection:** no hit in the requested scope could be positively classified as a redacted projection. In particular, the R1-bearing `evidence/seat-live.json` is not safe to classify as redacted based on the separate spot-check ruling.

## SHA-256 provenance (whole tracked file at frozen tip)

Hashes are of the complete source file, not the matching private value. They identify the cited hit-bearing samples without reproducing contents.

- `evidence/seat-live.json` — `4690d778d1ab51b33976ce7c7acc90cdc7f10a883fed42ce2bb97975c4e1d619` (R1, 2 lines).
- `wave1-dispatch.json` — `5c145c261a7530f901cb2b0b08d4226a673d3c399ddc59194380fbbc50636efa` (R1/R7/R8/R9; path samples above).
- `wave1-spec.json` — `6969eb19533ea65428c1e950271d91482a21a204f947e248c6db405b3907a416` (R1/R7/R8/R9; path samples above).
- `evidence/r13-preserved/evidence.json` — `71bb7772e6827540d492bfebbde7db762bb9fab52c5fcc14e50701836f5b76fc` (home-prefix and `sessions`/`.jsonl` token samples).
- `evidence/final/r14-preserved/evidence.json` — `b9c504fc1e7e1a853166cc8bdd4e94f7475a6d5f49b344bcd8811f07ba3da896` (home-prefix sample).
- `evidence/mutations/MutQuota/pristine/runs/fifo_skipped.stdout` — `41498969132f53dfa7cf5c2d950db85477f2efb13fdfa84b1549e804400641fa` (synthetic mutation-fixture sample).

## Redaction guidance and limits

1. Redact or replace R1 identities and operator-home paths in preserved evidence and wave task manifests before any handoff. For raw command captures, retain only required status/shape metadata; do not commit raw `argv`/`stdout` or unredacted task text when a digest and redacted projection suffice.
2. Keep synthetic mutation fixtures and the 86 fixture-rooted `.jsonl` paths distinguishable from live/private values; do not blanket-delete generic `sessions`, `.jsonl`, `model`, or `provider` mentions.
3. Keep R7 path mentions only where they are necessary boundary instructions and contain no values; recheck the full prompt before allowing those lines. Do not allowlist R1 or operator-home-path hits in captured evidence merely because neighboring files are fixtures.
4. A regex sweep cannot establish the absence of unrecognized private context. Non-mutation broad-token hits remain value-uninspected by design; C1's frozen recall-floor warning applies.

No source files were modified. No tools were installed or updated.