# CaseReview04 — C1 cases `rate_limit_zai_retry_exhausted`, `rate_limit_beats_quota_by_status_and_token`

Reviewer: MoriR17.CaseReview04-4 (wave2 falsification, leaf, read-only). Date 2026-10-20.
Scope: the two assigned cases only — fixture bytes, expected wants, classifier branches in
`tools/mori-seat-terminal.py`, gate comparison in `tools/mori-round17-seat-regressions.py`,
retained L1 before/after manifests. No tool/selftest executed; all verdicts are static
analysis plus read-only inspection of committed receipts. No tools installed or updated
(jq/python3 already present); no pacman/uv/npm transactions performed.

## Verified evidence chain

1. **Pins.** Actual fixture bytes hash-match `expected.json` pins and `PINNED_INPUTS.json`:
   `RateLimitRetryExhausted/zai-retry-exhausted.jsonl` = `fd1cd298…ac35fb69`;
   `RateLimitOrdering/status-beats-quota.jsonl` = `a6844bd6…612b4fdc`;
   `RateLimitOrdering/token-beats-quota.jsonl` = `12ad7566…4917a5`; expected.json =
   `b684c63b…5f57cb01f`; tool = `5819c3c0…adbdba`; gate = `21285c2b…3b97f7a`. Gate persisted
   pins: declared 81, verified true, no missing/extra/mismatched
   (evidence/seat-after/run-manifest.json `.fixtures.pins`).
2. **Case wants.** expected.json cases (jq, both extracted in full):
   - `rate_limit_zai_retry_exhausted`: args `["--now-ms","1761000000000"]`, want rc1,
     `MORI_SEAT_TERMINAL_DEAD`, totals all-zero except `dead_rate_limit:1`, seats
     `{"zai-retry-exhausted":"dead_rate_limit"}`. All eight classes declared.
   - `rate_limit_beats_quota_by_status_and_token`: same args; want rc1 DEAD,
     `dead_quota:2`, all other classes 0, seats both `dead_quota`. All eight classes declared.
3. **Source support / independence of wants.**
   - Case 1 mirrors the contract motivation verbatim (contract.md C1: zai `429 … (type=1302)`
     "Retry budget exhausted after 10 retries") and S043 (corpus/lessons/round-17.md row S043:
     Z.AI 1302/HTTP 429 = "Rate limit reached for requests") ⇒ `dead_rate_limit` is the
     source-supported class.
   - Case 2 pins Amendment A1 item 1 (quota tokens first) and A1 item 10 (code tokens
     override): S043 also maps 1113/1308 to HTTP 429 for usage/balance, so a bare 429 plus
     quota wording must classify `dead_quota`, not rate-limit. M7 row (lessons round-17:
     "A1 business-code/quota-before-generic429 fix") is the recorded cause.
   - Independence: the before manifest (entering tip) grades both cases
     `capability_absent` — there was no tool to fit wants to; wants were pinned in
     expected.json before the delivered tool existed in the lane (PINNED_INPUTS measured
     commit 273aa74).
4. **Classifier branches (static, per case).**
   - Case 1: header `{"type":"session","version":3}` passes `_header_ok`
     (tools/mori-seat-terminal.py:308-324, `SUPPORTED_SCHEMA_VERSION` == 3). Terminal view:
     role assistant, stopReason error (mori-seat-terminal.py:243-252). Settle:
     terminal_ms 1760998000000 ≤ now 1761000000000 − 900 000 = 1760999100000 ⇒ settled,
     not `error_unsettled` (mori-seat-terminal.py:258-261). error_code `1302` ∈ RATE_CODES ⇒
     `dead_rate_limit` (mori-seat-terminal.py:262-266), before the quota-token branch
     (:267-268) and the 429-status/token branch (:269-272). rc1/DEAD per rc semantics.
   - Case 2: neither seat has a `(type=NNNN)` token (observed `error_code: null` in retained
     stdout), so both fall through the code branches to the quota-token branch first:
     status-beats-quota "quota exceeded" + errorStatus 429 ⇒ `dead_quota` at :267-268 — the
     429-status rate-limit branch at :269-272 is never reached, exactly the A1 ordering.
     token-beats-quota "quota 402 rate_limit credits" (no errorStatus) ⇒ `dead_quota`
     likewise.
5. **Gate comparison is non-vacuous for these cases.** Declared totals are compared exactly
   (gate:1218-1221); totals are re-derived from graded seats and compared to the tool's
   totals row (gate:1404-1405); every emitted seat must match want.seats or it is
   `unexpected_seat` (gate:1249-1258); the top-level `retry_exhausted` aggregate is
   re-derived from graded seats and cross-checked (gate:1406-1412); rc↔finding_id coherence
   enforced at load and run (gate:649-655, 1309-1313). A pre-A1 tool (rate-limit before
   quota) would emit `dead_rate_limit:2` here and fail totals+seats; a tool that never
   parses codes still passes case 2 but fails case 1 only if it also misclassifies 1302 —
   cross-case discrimination with `code_rate_1302_beats_quota_token` (CodeRate1302QuotaWord)
   covers that; not my case's gap to close.
6. **Retained observation matches every asserted field.** seat-after/run-manifest.json:
   both cases `status:"match"`, `reasons:[]`, `pack_changed:false`, stderr_bytes 0.
   Retained stdout digests re-hash to the manifest values:
   `runs/rate_limit_zai_retry_exhausted.stdout` sha256 `cf09a10b…99a32d6` (1119 bytes),
   `runs/rate_limit_beats_quota_by_status_and_token.stdout` sha256 `a62413ec…e9e3b4fe`
   (1551 bytes). Case 1 stdout: totals dead_rate_limit 1, seat record class
   dead_rate_limit, error_status 429, retries 10, error_code "1302", retry_exhausted
   true, terminal_ms 1760998000000, now_ms 1761000000000, settle_seconds 900. Case 2
   stdout: totals dead_quota 2, both seat records dead_quota, error_status 429 present on
   status-beats-quota (negative signal demonstrably seen and overridden), error_code null.
7. **Sandbox isolation / no source mutation.** Tool ran against per-case sandbox copies
   (`sessions_dir` = evidence/seat-after/cases/<id>/sessions; gate re-points
   `--sessions-dir` at the sandbox, gate:936-956, default append at :829). Pack snapshot
   digests in the manifest reproduce exactly from the pinned file hashes under the gate's
   `pack_digest`/canonical construction (gate:368-374): pack1 `35b032ff…788aa0a` ✓,
   pack2 `e73e64c3…6015a164` ✓, before == after.
8. **Privacy.** grep over both retained stdouts for errorMessage text ("Retry budget
   exhausted", "Too Many Requests", "quota exceeded", "rate_limit credits"): 0 matches in
   each; only contract field-limited keys present. stderr_bytes 0 (JSON-only stdout).

## Required count (read-only, over committed receipts)

Command (cwd `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence`):

```
jq -s '[.[].cases[] | select(.id=="rate_limit_zai_retry_exhausted" or .id=="rate_limit_beats_quota_by_status_and_token") | .status] | group_by(.) | map({(.[0]): length}) | add' seat-before/run-manifest.json seat-after/run-manifest.json
```

rc=0, output: `{"capability_absent": 2, "match": 2}` — consistent with PINNED C1 before=54
(all cases capability_absent at entering tip) → after=0 (54/54 match). Follow-up check rc=0:
pack digests stable for both cases (pack_changed false, digests above).

## Findings

### F1 (low, naming — not a falsifier): case id contradicts its own want
`rate_limit_beats_quota_by_status_and_token` (.ufo/waves/round-17/fixtures/seat/expected.json,
case 2 of my pair) asserts `dead_quota` for both seats — i.e. rate limit does **not** beat
quota via 429 status or the literal "rate_limit" token; only the vendor code branch
(mori-seat-terminal.py:262-266) can do that. The id reads as the pre-A1 expectation, and the
sibling id `code_rate_1302_beats_quota_token` uses "beats" for the actual winner, so the
convention is inconsistent. Risk: a maintainer "fixing" the tool to match the id would break
A1/S043 conformance while the fixture name appears to endorse it. Want itself is
contract-correct; recommend a future rename or a note field (gate already accepts `note`,
gate:214). No current behavior is wrong.

### F2 (info, coverage note): per-seat emit fields are not fixture-asserted
want.seats pins class only (contract-defined schema), so `retries`, `error_code`,
`terminal_ms`, `retry_exhausted` per seat are unconstrained in gate runs; they are exercised
in the tool selftest arms (mori-seat-terminal.py:860-870, 1375-1379) which I did not run per
lane rules. The gate does transitively assert the aggregate retry_exhausted (gate:1406-1412)
and I verified the retained stdout shows the correct field values for both cases, so the
delivered run is corroborated; this is a residual coverage observation, not a defect.

### F3 (info, cosmetic): top-level `retry_exhausted` type ambiguity
Retained stdout shows top-level `retry_exhausted` as int (1/0) while seat rows carry booleans;
the gate accepts bool or int (gate:1406-1412) and the contract does not pin the type. No
misclassification possible from this; recorded for schema hygiene.

## Verdict

**Pass — no falsifier for either assigned case.** Attacked scope: fixture bytes and pins
(3 files), both want entries, settle/code/token classifier branches (mori-seat-terminal.py
:243-273, :308-324), gate want-validation/comparison/derivation (mori-round17-seat-
regressions.py :480-698, :1215-1258, :1300-1458), sandbox/argv isolation (:807-956), retained
before/after manifests and both stdout receipts. Negative controls are real (rate-limit
signals present yet must classify quota; all-zero totals enforced; before side
capability_absent proves the gate is not rubber-stamping); no class or setup is vacuously
accepted for these two cases. Residual risk is limited to F1 naming confusion and F2/F3
coverage notes above.
