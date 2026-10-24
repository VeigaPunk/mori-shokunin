# C1 focused falsification — quota_402 and quota_credits

Date: 2026-10-20. Scope: `quota_quota_402` / `Quota402` and `quota_quota_credits` / `QuotaCredits`; classifier, gate comparisons, and retained L1 before/after receipts only. No tool or selftest was run.

## Verdict

The delivered classifier conforms to the two asserted synthetic cases in the retained L1 after-run receipts. The cases are non-vacuous: each has a v3 session header, one aged assistant/error message, one scanned file, one output seat, and an `rc=1` dead finding. The targeted `want` fields all match.

**Specific falsifiers:** (1) `quota_quota_402` does not isolate the message-token `402` branch from `errorStatus=402`; the current case would also pass a regression that inferred quota from the status alone. (2) The two generic-token expectations are supported by the local C1 heuristic contract, but not independently by the external provider/HTTP sources cited for C1. They must not be treated as sourced provider-cause observations.

## Findings (by severity)

### Low — `quota_quota_402` is not a discriminating test of the `402` message token

- The synthetic record at `.ufo/waves/round-17/fixtures/seat/Quota402/quota-402.jsonl:2` contains both `errorStatus:402` and `errorMessage:"HTTP 402 Payment Required"`. Its `want` at `.ufo/waves/round-17/fixtures/seat/expected.json:345-360` requires `dead_quota` for the single `quota-402` seat.
- The current implementation classifies quota from the message-token list (`_classify`, `tools/mori-seat-terminal.py:262-273`; token constants at `:86-88`); it does not currently classify on `error_status == 402`. But the fixed input gives both signals together, so a changed implementation that adds a status-only 402→quota rule would produce the same asserted output and still pass this case. This is a test-isolation gap, not a mismatch in the current L1 output. [INFERENCE]
- The existing `code_rate_1302_beats_quota_token` negative control is real for code precedence: its fixture `.ufo/waves/round-17/fixtures/seat/CodeRate1302QuotaWord/code-1302-quota.jsonl:2` combines `quota exceeded` with `(type=1302)` and HTTP 429; the expected rate-limit result is pinned at `expected.json:1286-1308`, and its after receipt is `status=match`, `dead_rate_limit:1`, `dead_quota:0` in `.ufo/waves/round-17/evidence/seat-after/run-manifest.json:1`. That control does not distinguish status 402 from message token 402. A status-402/non-quota-message control, or a status other than 402 while retaining the message token, would make this branch-specific claim discriminating.

### Low — external source support does not establish generic `402`/`credits` as provider quota causes

- `Quota402` is explicitly synthetic and says provider `openai`, model `gpt-synthetic`, with generic “HTTP 402 Payment Required” text; `QuotaCredits` is synthetic `openai`/`gpt-synthetic` text “not enough credits” and has no error status (`QuotaCredits/quota-credits.jsonl:1-2`). Their expected `dead_quota` values are separately recorded at `expected.json:345-385` and follow the local token rule in `contract.md:112`.
- The external S043 receipt documents Z.AI code 1113 as insufficient balance/no resource package, 1308 as usage limit, and 1302 as rate limit (`.ufo/waves/round-17/build/SrcZaiErrorCodes.md:16-18,27-37`; source URL https://docs.z.ai/api-reference/api-code, accessed 2026-10-20). It does not source a generic HTTP 402 or the literal `credits` text for the synthetic OpenAI provider. RFC 9110 §15.5.3 says 402 is “reserved for future use” (https://www.rfc-editor.org/rfc/rfc9110#section-15.5.3, accessed 2026-10-20), not a standardized quota cause.
- The local knowledge note correctly bounds these terms: “Error-string tokens are heuristic outside the explicitly mapped Z.AI codes” (`corpus/knowledge/seat-terminal-status-r17.md:50-51`). Therefore these wants are independent of the classifier implementation as conformance expectations, but their semantic support is the local heuristic contract, not an independent external provider fact. No current classifier defect is implied if C1 keeps that limitation explicit.

## Assertions, controls, and retained results

- The independent manifest pins the two source bytes (`expected.json:54-55`); read-only `sha256sum` returned `7443dbf4…56523ec` for `Quota402/quota-402.jsonl` and `691072a8…75107e3` for `QuotaCredits/quota-credits.jsonl`, matching those pins (rc 0).
- `quota_quota_402` expects `rc=1`, `MORI_SEAT_TERMINAL_DEAD`, all eight class totals with only `dead_quota:1`, and exactly `quota-402:dead_quota` (`expected.json:345-360`). `quota_quota_credits` makes the corresponding assertions for `quota-credits` (`:370-385`). Their fixed scan time is 1761000000000; both terminal times are 1760998000000, 2,000,000 ms older, so neither is accepted as `error_unsettled` (contract A1 `contract.md:113`; fixture lines above).
- The gate reads the external `expected.json` (`tools/mori-round17-seat-regressions.py:701-736`), checks rc and finding consistency (`:1274-1313`), requires the full output schema, derives all class totals from returned seats, checks scans/counts, and calls `compare_want` (`:1364-1448`). For these `rc=1` cases `compare_want` checks each pinned class total and required seat class, and rejects unexpected seats (`:1215-1260`). Each want specifies all eight classes. No setup outcome can satisfy these wants.
- Before receipts show both IDs as `capability_absent`, `observed:null`, with unchanged source pack digests: `.ufo/waves/round-17/evidence/seat-before/run-manifest.json:1` (queried per ID). After receipts show both `status:"match"`, `ok:true`, `reasons:[]`, `rc:1`, `finding_id:MORI_SEAT_TERMINAL_DEAD`, `files_scanned:1`, `seat_count:1`, and exactly one `dead_quota` with every other class zero: `.ufo/waves/round-17/evidence/seat-after/run-manifest.json:1` (queried per ID). Retained stdout for each (`evidence/seat-after/runs/quota_quota_402.stdout:1` and `.../quota_quota_credits.stdout:1`) additionally shows the expected class, key, terminal time, and provider/model. Fields not present in `want`—including provider/model and error status—are observed and schema/type checked where applicable, but are not independently pinned by these two wants.
- The read-only requested count was run against both retained manifests:
  `jq -s '[.[] | [.cases[] | select(.id == "quota_quota_402" or .id == "quota_quota_credits")] | length]' /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-before/run-manifest.json /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-after/run-manifest.json`
  rc 0; stdout `[\n  2,\n  2\n]\n`.
- L1's aggregate retained counter is rc 0, stdout `[54,0]` (`evidence/count-c1.json:5-21`): 54 prior cases capability-absent/mismatched versus zero after; this review did not rerun the gate. The bounded after manifest summary is 54 matched, 0 mismatched, 0 absent (`evidence/seat-after/run-manifest.json:1`).

## Residual risk and verification gaps

- `dead_quota` here means “aged terminal error matching the local token heuristic”; it does not prove a provider-side quota/billing cause. This is stated in the knowledge note and is especially important for the synthetic 402/OpenAI-shaped record.
- The `lsp` device was unavailable: `read xd://lsp` returned “No such tool” (mounted-device list did not include LSP). I used direct source reads and JSON receipt queries; any literal search was only for locating records, not semantic proof.
- No builds, tests, linters, selftests, live probes, or installs/updates were run. The retained L1 outputs above are the only runtime evidence considered.