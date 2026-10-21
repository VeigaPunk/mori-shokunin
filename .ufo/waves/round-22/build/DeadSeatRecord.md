# DeadSeatRecord — round-21 dead-seat provenance (observation only)

Seat: MoriR22.DeadSeatRecord (scout, read-only). Scope: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-21/dead-seats.json` plus read-only `git -C` plumbing on that path. No seat revived, replaced, re-dispatched or reinterpreted. No tests/builds/measurements run. No installs.

## Verdict

12 round-21 seats are recorded dead, all `replaced=false`. Every recorded cause is a provider capacity/rate-limit refusal; the record carries no seat output, no finding, and no file reference. None of these 12 may be counted as a successful, partial, or "reported" seat. Any round-21 report file that happens to share one of these ids is outside this record and is not evidence of seat success. [INFERENCE: such files were not opened or searched, by bound.]

## Artifact identity (observed)

| Fact | Value |
|---|---|
| Worktree SHA-256 | `2f666cf3f87fb571f8ae362febfcd157cc5a24201f57ac060f0f544998525e05` |
| Git blob at HEAD `306e06ecd02e0ea8e544fbd30d1ff7e7359c581e` | `56de30eae40e824fb48f3a31807fb5cf3cce1f70` (worktree clean, `git status` empty) |
| Blob at round-22 entering revision `77a5bbe8a0b41dfbfd2546d024d36e294b814bd0` | same blob `56de30ea…`; entering rev is ancestor of HEAD; 0 commits touch the file in `77a5bbe8..HEAD` |
| Top-level keys | `seats` only |
| Seat keys (union) | `id, role, error, replaced, batch, metadata_minimization` |

## Provenance chain (observed, `git log -- <file>`)

The record grew in three commits, all authored and committed as `mori-shokunin`, with additions only and 0 removed lines between consecutive versions:

| Commit | Time (committer TZ) | Blob | Seats |
|---|---|---|---|
| `a8442a018aa9c51b21b92c3ce3b17736317375b1` "invalidate unsafe pin and supersede QUALITY67 honestly" | 2026-10-21T09:41:41-03:00 | `6f3024e4…` | 4: LessonDraft-4, CriticCalibration-4, CriticFreshness-4, OracleLoss-4 |
| `ce413b9de2cbf34dc498a47fdb75f212ef211474` "land retained-loss probe and evidence-first rule comparison" | 2026-10-21T10:00:34-03:00 | `1ecfb0b7…` | 9: adds AuditTranscript-4, SourceApproval-4, AuditRevision-4, AuditExtra-4, HistoryContract-4 |
| `9fb1f911cfdd6061005c300795f44b1b45523897` "integrate residual falsifiers and bind final measurement inputs" | 2026-10-21T10:29:35-03:00 | `56de30ea…` | 12: adds batch `residual8` seats ReviewSafety, ReviewClaimBounds, ReviewClassify |

Earlier entries were never edited or removed (same per-entry fields and error lengths in every version). The death record is original and has not been rewritten.

## Seat ledger (minimized; error text by class and digest only)

Digest = first 16 hex chars of SHA-256 over the exact `error` string bytes. It identifies the text and authenticates nothing.

| id | role | batch | provider label in error | class | err digest | replaced |
|---|---|---|---|---|---|---|
| MoriR21.LessonDraft-4 | scribe | — | anthropic/claude-haiku-5-5 | HTTP 429 account rate limit, retry-after given | `1b4ec69f2fb131c7` | false |
| MoriR21.CriticCalibration-4 | critic | — | openai-codex/gpt-6-luna | capacity, retry budget exhausted (5) | `ce6281353b00f168` | false |
| MoriR21.CriticFreshness-4 | critic | — | openai-codex/gpt-6-luna | same | `ce6281353b00f168` | false |
| MoriR21.OracleLoss-4 | executor | — | openai-codex/gpt-6-luna | same | `ce6281353b00f168` | false |
| MoriR21.AuditTranscript-4 | reviewer | — | openai-codex/gpt-6-luna | same | `ce6281353b00f168` | false |
| MoriR21.SourceApproval-4 | scout | — | openai-codex/gpt-6-luna | same | `ce6281353b00f168` | false |
| MoriR21.AuditRevision-4 | reviewer | — | openai-codex/gpt-6-luna | same | `ce6281353b00f168` | false |
| MoriR21.AuditExtra-4 | reviewer | — | zai/glm-5.3-flash | HTTP 429, retry budget exhausted (5) | `b392a74ce7879baf` | false |
| MoriR21.HistoryContract-4 | scout | — | zai/glm-5.3-flash | same | `b392a74ce7879baf` | false |
| MoriR21.ReviewSafety | sentinel | residual8 | openai-codex/gpt-6-luna | capacity, retry budget exhausted (5) | `ce6281353b00f168` | false |
| MoriR21.ReviewClaimBounds | reviewer | residual8 | Devin stream (no bracketed model label) | resource_exhausted free-tier limit, timed reset | `07b561512fa1dfb0` | false |
| MoriR21.ReviewClassify | reviewer | residual8 | Devin stream (no bracketed model label) | same class; reset-minute text differs by 1 | `a01bbf540d041cc5` | false |

Totals (jq): 12 seats. Roles: reviewer 5, critic 2, scout 2, executor 1, scribe 1, sentinel 1. Provider labels: openai-codex 7, zai 2, Devin 2, anthropic 1. `batch` present on 3 (all `residual8`); `-4` suffix on 9. `replaced != false`: 0. `metadata_minimization` present on 2 (the Devin seats), stating that a provider trace identifier was withheld, message text was kept, and no replacement was made.

## Observed vs inference vs unknown

Observed:
- All 12 errors are infrastructure refusals (rate limit, capacity, or quota) that the provider reported in its own error text. None is a task-level failure, timeout on work, or partial output.
- The record holds no output paths, report references, or finding IDs. A field scan found no path-like value; the only `/` characters are inside provider/model labels.
- The record is append-only across its 3 commits, and its bytes are unchanged from the round-22 entering revision through HEAD.

Inference:
- [INFERENCE] The `-4` suffix suggests a fourth attempt/instance of the seat name. The record does not say whether attempts 1–3 existed or succeeded, so this cannot count toward seat success.
- [INFERENCE] `residual8` suggests an 8-seat residual batch with 3 deaths recorded. The other 5 seats' dispositions are not in this file.
- [INFERENCE] The two Devin errors were recorded about one minute apart (reset minute text differs by 1). Error text carries a clock time without a date. The record has no death timestamps of its own.

Unknown (not resolvable from this file):
- Absolute death times per seat. Only commit times bound when each entry was recorded.
- Whether any round-21 claim relied on work these seats were meant to produce. Coverage loss has to be traced from the round-21 contract and plan, which are outside this assignment.
- Whether the withheld trace identifiers still exist anywhere. The record says they were withheld, and this seat did not look.

## Bindings for L1

- Treat the 12 ids as dead and unreplaced. A seat-success denominator for round 21 must exclude them by identity, not by count.
- Any later file named after one of these ids does not make the seat successful unless a separate, committed provenance record says so. This record contains none.
- This record does not change the debt carried forward: r21 admitted ≠ privacy clearance; original permission control RED11/12; historical wave dispositions unknown; baseline acceptance blocked.

## Commands run (all read-only)

`sha256sum` on the file; `git -C <repo>` with `rev-parse`, `status --porcelain`, `log`, `ls-files -s`, `show <rev>:<path>`, `diff`, `merge-base --is-ancestor`, `show -s`/`--stat`; `jq` projections over the file and the historical blobs. No writes except this report. No installs or updates.
