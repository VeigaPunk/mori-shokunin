# Round 17 CaseReview01 — C1 status/token cases

## Scope and verdict

Axes attacked: independent expected values/source grounding; status-vs-token branch separation; exact output and gate grading; negative controls; non-vacuous class/setup acceptance.

**Recommendation: no actionable falsifier in the two assigned synthetic cases.** This is a contract-level review of `rate_limit_zai_status_429` and `rate_limit_zai_token_429`, not an admission or claim that either fixture proves a live Z.AI incident cause.

## Findings by severity

None in the assigned cases.

## Evidence

- The expected rows are fixed separately from the tool’s captured output, pin `--now-ms 1761000000000`, require `rc: 1` / `MORI_SEAT_TERMINAL_DEAD`, enumerate all eight class totals (one `dead_rate_limit`, seven zero), and require the one named seat/class: `.ufo/waves/round-17/fixtures/seat/expected.json:88-110,113-135`. The copies retained by both L1 runs show the same wants. The byte pins at `.ufo/waves/round-17/fixtures/seat/expected.json:62-63` match the assigned pack file hashes: status `a3747772cffdfe5132dbc05ffad1cce0898269e9d428f4ec80308be9945d031b`; token `752336ea386df7c465127db08bb1cc4b2fefe78042122ea81dedd456dfbbc3b5`. Read-only command `sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/fixtures/seat/RateLimitStatus429/zai-status-429.jsonl /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/fixtures/seat/RateLimitToken429/zai-token-429.jsonl; rc=$?; printf 'rc=%d\n' "$rc"` returned those two hashes and `rc=0`.
- The byte-level branch separation is real: `.ufo/waves/round-17/fixtures/seat/RateLimitStatus429/zai-status-429.jsonl:2` has `errorStatus:429`, generic `upstream capacity unavailable`, and no quota/rate token or `(type=NNNN)` code. `.ufo/waves/round-17/fixtures/seat/RateLimitToken429/zai-token-429.jsonl:2` has `errorStatus:500`, message `HTTP 429 Too Many Requests`, and no code. The timestamps are 2,000,000 ms before the pinned scan time, beyond the output’s 900-second settle window.
- The implementation extracts status and the `(type=NNNN)` token separately (`tools/mori-seat-terminal.py:214-243`), returns `error_unsettled` only for fresh errors, applies code/token precedence, then reaches status-or-rate-token classification (`:247-273`). Thus the first pack exercises only the status arm; the second exercises the literal `429` message-token arm despite status 500.
- Retained L1 before receipts identify each case as `capability_absent`, with `observed:null`, unchanged pack digests within that run, and no output (`.ufo/waves/round-17/evidence/seat-before/run-manifest.json:1`, both case records). After receipts identify both as `match`, `ok:true`, `reasons:[]`, `rc:1`, `MORI_SEAT_TERMINAL_DEAD`, one scanned file/seat, and the exact eight totals (`.ufo/waves/round-17/evidence/seat-after/run-manifest.json:1`). Full retained stdout confirms the expected seat identity and class, status (`429` / `500`), `error_code:null`, `terminal_ms:1760998000000`, `now_ms:1761000000000`, `settle_seconds:900`, and one `dead_rate_limit` (`.ufo/waves/round-17/evidence/seat-after/runs/rate_limit_zai_status_429.stdout:1` and `.ufo/waves/round-17/evidence/seat-after/runs/rate_limit_zai_token_429.stdout:1`). Both outputs have the expected provider/model, one-file aggregates, no stderr, and no extra seat. The after receipt also has 81/81 source pins verified with no missing/extra/mismatched entries.
- The gate does not vacuously accept a class or setup result for these two cases. `compare_want` checks every declared total and expected seat and rejects missing or unexpected seats (`tools/mori-round17-seat-regressions.py:1215-1260`); strict rc 0/1 evaluation requires the full totals schema and seat list, re-derives totals from graded seats, and compares wants (`:1364-1448`). It rejects a wrong rc or finding ID (`:1274-1313`). Both wants require rc 1 and DEAD, so an rc 2 setup path cannot match. All eight expected totals are explicitly non-vacuous in the two manifest rows.
- Negative controls are concrete, not names only. `.ufo/waves/round-17/fixtures/seat/ErrorOther/bare-error.jsonl:2` has no status or error text; `.ufo/waves/round-17/fixtures/seat/ErrorOther/thinking-loop-error.jsonl:2` has a non-matching message. The expected case pins both as `dead_error_other` and zero rate/quota (`.ufo/waves/round-17/fixtures/seat/expected.json:489-511`), and L1 after records `match` with two `dead_error_other` and zero rate/quota (`.ufo/waves/round-17/evidence/seat-after/run-manifest.json:1`). The quota-precedence controls carry actual contradictory inputs—429 plus `quota exceeded`, and `quota 402 rate_limit credits`—and expect two `dead_quota` (`.ufo/waves/round-17/fixtures/seat/RateLimitOrdering/status-beats-quota.jsonl:2`, `.ufo/waves/round-17/fixtures/seat/RateLimitOrdering/token-beats-quota.jsonl:2`; `.ufo/waves/round-17/fixtures/seat/expected.json:263-285`); L1 after records `match`, two quota and zero rate (`.ufo/waves/round-17/evidence/seat-after/run-manifest.json:1`). These controls show that the suite can observe non-rate classes and the A1 precedence rule.
- Source qualification is appropriately limited at the contract level: RFC 6585 §4 says HTTP 429 is rate limiting (`corpus/SOURCES.md:47`; opening receipt `.ufo/waves/round-17/build/SrcRfc6585.md:13-20`). S043 documents Z.AI’s 1113/1308 usage/balance errors and 1302 rate limit under HTTP 429, and explicitly warns that status alone cannot distinguish business cause (`corpus/SOURCES.md:49`; `.ufo/waves/round-17/build/SrcZaiErrorCodes.md:16-18,29-37`). Amendment A1 orders business codes and quota tokens before the generic 429 path and maps 1113/1308 vs 1302 (`.ufo/waves/round-17/contract.md:112-123`). The fixtures test the declared fallback/token rules; they do not independently establish a real-world cause. This limitation is also recorded in `corpus/knowledge/seat-terminal-status-r17.md:26-28,44-53`.

## Count and verification gaps

Read-only count command:

```text
jq -c '[.cases[] | select(.id == "rate_limit_zai_status_429" or .id == "rate_limit_zai_token_429")] | length' /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/fixtures/seat/expected.json; rc=$?; printf 'rc=%d\n' "$rc"
```

Observed output: `2`, then `rc=0`.

No tool or selftest was run; the before/after conclusions above use retained L1 receipts only. LSP was unavailable: reading `xd://lsp` returned “No such tool” and the mounted-device list contained no `lsp` route, so references/definition/diagnostics could not be requested. Static reads provide the evidence above; literal search was used only to locate case/branch lines, not as semantic proof. No installs or updates.

Residual risk: the status-only Z.AI fixture cannot identify a vendor business cause when the business code is absent, and the token fixture deliberately contradicts its textual `429` with status 500. Treat those as tests of the declared heuristic, not as evidence that a real transcript had that cause. No real transcript was inspected for this scoped review.

Report: .ufo/waves/round-17/falsify/CaseReview01.md
