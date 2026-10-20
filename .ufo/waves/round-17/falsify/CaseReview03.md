# CaseReview03 — assigned C1 cases

Axes attacked: C1 coverage and class correctness; independent source authority; gate non-vacuity.

## Findings

### Medium — Devin `resource_exhausted` is not source-supported as `dead_rate_limit`

`fixtures/seat/RateLimitResourceExhausted/devin-resource-exhausted.jsonl:2` is an assistant error from `devin/devin-2` with only `errorMessage: "resource_exhausted: concurrency pool empty"`; it carries neither `errorStatus` nor a typed error code. `fixtures/seat/expected.json:213-234` nevertheless requires `dead_rate_limit` (rc 1, `MORI_SEAT_TERMINAL_DEAD`, one rate-limit seat, zero for every other class). The implementation makes that exact mapping solely because `resource_exhausted` is in `RATE_TOKENS` (`tools/mori-seat-terminal.py:78-85, 267-272`), and Amendment A1 repeats it (`.ufo/waves/round-17/contract.md:112`).

That is a contract-conformance expectation, not an independent source-backed cause: the official gRPC status-code guide says `RESOURCE_EXHAUSTED` means a resource was exhausted, “perhaps a per-user quota” or “perhaps the entire file system is out of space” (https://grpc.io/docs/guides/status-codes/, “Full list of Status codes,” RESOURCE_EXHAUSTED row; read 2026-10-20). It does not identify rate limiting. The routed S041/S043 sources are HTTP 429 semantics and Z.AI business-code distinctions, respectively (`corpus/lessons/round-17.md:47-49`; `.ufo/waves/round-17/build/SrcZaiErrorCodes.md:15-17,25,36-37`); neither covers this Devin token. The earlier C1 authority audit also records that `resource_exhausted` is absent from the canonical failure needles and that Devin cases matched only this token (`.ufo/waves/round-17/build/CriticC1.md:118-140`).

**Specific falsifier:** this exact fixture asks the regression suite to certify a generic resource/concurrency exhaustion marker as a rate-limit cause without a rate-limit status/code or provider-specific source. The current tool matches the declared token rule, but the expected semantic class is not justified by the cited source set. [INFERENCE] The exact Devin provider error may have additional meaning not captured by this synthetic record; that meaning is not evidenced here. Either source the provider-specific mapping or keep this expected value explicitly limited to contract-token conformance rather than rate-limit semantics.

### Low — Z.AI `RATE_LIMITED` expected value is contract-only, not independently sourced

`fixtures/seat/RateLimitTokenUpper/zai-token-upper.jsonl:2` has only the literal `RATE_LIMITED` error text (provider/model tags aside), with no HTTP status or `(type=1302)` code. `fixtures/seat/expected.json:187-209` expects `dead_rate_limit`; the implementation reaches that class through the case-sensitive token list (`tools/mori-seat-terminal.py:78-85, 267-272`). S041 supports HTTP 429 as rate limiting, while S043 supports Z.AI code 1302 / HTTP 429 with the message “Rate limit reached for requests” (`corpus/lessons/round-17.md:47-49`; `.ufo/waves/round-17/build/SrcZaiErrorCodes.md:15-17,25`). Neither source establishes that this token-only fixture represents that status/code. Thus the expected row is independent as a separately pinned table entry, but not an independent semantic oracle: its class is simply the contract’s token rule (`contract.md:112`). It is valid as a tokenizer regression, not evidence that the external classification is source-supported.

## Gate and receipt checks

The expected values are not vacuously met. Both assigned `want` objects pin rc, finding, all eight class totals, and a non-empty seat-to-class mapping (`expected.json:194-209, 219-234`). The fixture timestamps are 2,000,000 ms before the pinned `--now-ms=1761000000000`, older than the default 900-second settle window (`contract.md:113`), so `error_unsettled` is not the expected outcome. The comparator checks rc/finding and totals, requires strict-seat comparison for rc 0/1, detects missing/unexpected seats, and compares each expected seat class (`tools/mori-round17-seat-regressions.py:1274-1313, 1364-1448, 1215-1260`).

L1’s retained before manifest records both cases as `capability_absent`, `ok:false`, `observed:null` (not a green baseline). The after manifest records both as `match`, `ok:true`, unchanged pack digests, rc 1, `MORI_SEAT_TERMINAL_DEAD`, `files_scanned:1`, `seat_count:1`, and exactly one `dead_rate_limit`; see `.ufo/waves/round-17/evidence/seat-before/run-manifest.json` and `evidence/seat-after/run-manifest.json` case rows. The retained stdout confirms every asserted seat/class field: `evidence/seat-after/runs/rate_limit_zai_token_upper.stdout:1` reports `zai-token-upper: dead_rate_limit`, and `.../rate_limit_devin_resource_exhausted.stdout:1` reports `devin-resource-exhausted: dead_rate_limit`; both have all other totals zero and empty stderr per their after-manifest rows.

Negative controls are substantive and retained: the quota-only fixture says `weekly quota exceeded` (`fixtures/seat/QuotaWord/quota-word.jsonl:2`) and is expected/observed as one `dead_quota`, zero `dead_rate_limit` (`expected.json:289-310`; `evidence/seat-after/runs/quota_quota_word.stdout:1`); the bare error fixture has no error marker (`fixtures/seat/ErrorOther/bare-error.jsonl:2`) and the paired case is expected/observed as two `dead_error_other`, zero rate/quota (`expected.json:489-510`; `evidence/seat-after/runs/error_other_thinking_and_bare.stdout:1`). Setup is not folded into a class: `missing_dir_rc2` pins rc 2 / `MORI_SEAT_TERMINAL_SETUP` (`expected.json:718-727`) and its retained stdout has that finding (`evidence/seat-after/runs/missing_dir_rc2.stdout:1`).

Read-only count command, run only over the two committed manifests (no tool or selftest rerun):

```sh
jq -s 'map(.cases | map(select(.id == "rate_limit_zai_token_upper" or .id == "rate_limit_devin_resource_exhausted")) | {count: length, cases: map({id, status, ok})})' \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-before/run-manifest.json \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-after/run-manifest.json
```

rc 0; output:

```json
[
  {"count":2,"cases":[
    {"id":"rate_limit_zai_token_upper","status":"capability_absent","ok":false},
    {"id":"rate_limit_devin_resource_exhausted","status":"capability_absent","ok":false}
  ]},
  {"count":2,"cases":[
    {"id":"rate_limit_zai_token_upper","status":"match","ok":true},
    {"id":"rate_limit_devin_resource_exhausted","status":"match","ok":true}
  ]}
]
```

## Verification gaps

LSP was unavailable: first attempted `xd://lsp` with `{ "action":"status" }`; the tool returned “No such tool” and listed mounted devices without LSP. Literal grep was used only to locate case/token text; semantic conclusions above come from reading the contract, classifier, comparator, receipts, and cited source documents. No tool, gate, selftest, build, or live probe was run. No tool was installed or updated.
