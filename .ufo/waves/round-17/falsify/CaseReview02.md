# CaseReview02 — round-17 C1 token cases

Axes: independent oracle/source support; classifier-branch isolation; gate assertion strength; retained-result integrity.

## Verdict

**One concrete gate falsifier** below. The two assigned token cases themselves have non-vacuous wants and their retained after-run stdout matches every asserted field. The gate nevertheless does not pin the required reason for the real `prefix_filter_no_match` setup control, so a wrong setup cause can be admitted as a match.

## Finding — Medium: setup control does not assert the contract-required reason

Amendment A1 requires a zero-match `--prefix` to return rc 2 with `reason: "prefix-matched-none"` (`.ufo/waves/round-17/contract.md:115`). The `prefix_filter_no_match` expected entry at `.ufo/waves/round-17/fixtures/seat/expected.json:945-956` asserts only rc 2 and `MORI_SEAT_TERMINAL_SETUP`; it has no reason expectation. The gate cannot represent one: `WANT_KEYS` omits `reason` (`tools/mori-round17-seat-regressions.py:214-216`) and `_analyze_case` rejects unknown want keys (`:639-645`). For rc 2, `evaluate` does not restrict top-level keys and only validates optional totals/seats before `compare_want` (`:1301-1313,1450-1458`); `compare_want` has no reason comparison (`:1215-1260`).

**Static per-case counterexample (not executed):** for `prefix_filter_no_match`, rc 2 plus otherwise valid JSON with `schema: "mori-seat-terminal-v1"`, the expected `finding_id`, the correct existing sandbox `sessions_dir`, and the wrong `reason: "unavailable-dir"` reaches the rc-2 path with no expected totals/seats and no reason check. The case can therefore be reported `match` even though its actual prefix-miss contract is violated. This follows from the cited expected/gate code; it is not a claim that the delivered tool emitted that counterexample.

The retained delivered-tool result is correct but does not close the assertion gap: `evidence/seat-after/runs/prefix_filter_no_match.stdout:1` says `reason:"prefix-matched-none"`; the case has `status:"match"` in `evidence/seat-after/run-manifest.json` (case record on line 1). The producer has a separate unavailable-directory branch and the required prefix branch (`tools/mori-seat-terminal.py:416-417,461-466`). The setup branch is real, not empty: the expected case uses the existing `PrefixAttribution` pack and `--prefix Tsukuroi`; the emitted observation has `files_scanned:0` and `prefixes:["Tsukuroi"]`.

## Assigned token-case audit

### Synthetic inputs and oracle

- `fixtures/seat/RateLimitTokenRateLimitUnderscore/zai-token-underscore.jsonl:2` is an assistant/error with `errorMessage:"upstream rate_limit triggered"`, provider `zai`, model `glm-4.6`; it has no `errorStatus` or `(type=NNNN)` code.
- `fixtures/seat/RateLimitTokenCapitalRateLimit/zai-token-capital.jsonl:2` is the same shape with `errorMessage:"Rate limit exceeded"`, also with no status or code.
- Both expected entries (`fixtures/seat/expected.json:138-160,163-185`) pin `--now-ms 1761000000000`, rc 1, `MORI_SEAT_TERMINAL_DEAD`, all eight totals (only `dead_rate_limit` is 1), and the one exact seat/class. Their timestamps are `1760998000000`, i.e. 2,000,000 ms older than `now`, beyond the default 900-second settle window (`contract.md:113`; `tools/mori-seat-terminal.py:259-272`).
- These are independent from the implementation output in the useful test-oracle sense: the fixtures are synthetic and the builder report says expectations were a contract-derived oracle, not copied from a tool run (`build/SeatFixtures.md:17-20,29-34`). The exact token obligations are in the contract (`contract.md:112`) and fixture coverage map (`build/SeatFixtures.md:176-179`). The classifier first recognizes quota tokens, then the rate-limit status/token branch (`tools/mori-seat-terminal.py:78-89,262-272`); the fixture fields isolate the token branch. The gate checks rc/finding, each declared total, each expected seat, and unexpected seats (`tools/mori-round17-seat-regressions.py:1215-1260,1297-1313,1364-1448`). Neither want is empty or setup-only.

### Source boundary

S043's primary source, https://docs.z.ai/api-reference/api-code.md (accessed 2026-10-20), documents code 1302 / HTTP 429 with message “Rate limit reached for requests”; it also maps usage/balance codes to HTTP 429. The retained receipt records the exact table text and scope (`build/SrcZaiErrorCodes.md:16-20,25,35-38`; `corpus/SOURCES.md:49`). Thus the capital-case token `Rate limit` is directly supported as a phrase, though the full fixture string remains synthetic. **The exact underscore text `rate_limit` is not evidenced by that external source**; it is supported as a synthetic input only by the explicit local token contract. Treat that case as a test of the contract's literal matcher, not evidence that Z.AI/OMP emits that string. [INFERENCE] No real transcript was read.

### Retained output, controls, and vacuity

- Post-run raw outputs `evidence/seat-after/runs/rate_limit_zai_token_underscore.stdout:1` and `.../rate_limit_zai_token_capital.stdout:1` show rc-compatible `MORI_SEAT_TERMINAL_DEAD`, exactly one `dead_rate_limit`, all other totals zero, and the expected seat/key. Both records report `error_status:null`, `error_code:null`, `terminal_ms:1760998000000`, `now_ms:1761000000000`, and `settle_seconds:900`. Their after-manifest records have `status:"match"`, `reasons:[]`, `files_scanned:1`, `seat_count:1` and identical before/after pack digests (`evidence/seat-after/run-manifest.json`, case records on line 1).
- The retained before-manifest records have `status:"capability_absent"`, `observed:null`, and no stdout digest (`evidence/seat-before/run-manifest.json`, line 1). That is absence of the tool, not a pre-fix misclassification; I do not claim these cases demonstrate an old behavior failure.
- Negative class control is substantive: `ErrorOther/bare-error.jsonl:2` is a valid assistant/error with no message or timestamp, while `thinking-loop-error.jsonl:2` is an old assistant/error message with no rate/quota marker. The after manifest classifies both as `dead_error_other` (`evidence/seat-after/run-manifest.json`, line-1 `error_other_thinking_and_bare` record). The all-class case is also non-vacuous: its after record has eight files/seats and exactly one count for each of the eight classes, with `status:"match"` (`expected.json:1148-1176`; after manifest line 1, `mixed_one_seat_per_class`). Missing-directory setup is separately exercised and emits `reason:"unavailable-dir"` (`evidence/seat-after/runs/missing_dir_rc2.stdout:1`); its reason is not contract-pinned by A1 in the way the prefix-miss reason is.

## Requested read-only recount

Command (input order = before, after):

```sh
jq -s '[.[] | (.cases | map(select(.id == "rate_limit_zai_token_underscore" or .id == "rate_limit_zai_token_capital"))) as $c | {selected: ($c | length), match: ($c | map(select(.status == "match")) | length), not_match: ($c | map(select(.status != "match")) | length)}]' \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-before/run-manifest.json \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-after/run-manifest.json
```

rc 0; output:

```json
[
  {"selected": 2, "match": 0, "not_match": 2},
  {"selected": 2, "match": 2, "not_match": 0}
]
```

## Review gaps / procedure

- LSP was unavailable: attempted `read xd://lsp`, which returned `No such tool`; the mounted-tool list had no LSP device. Consequently references/definition/diagnostics were unavailable and the review used static path/line reads as the literal fallback.
- Read-only committed diff reviewed from entering commit `24526ea9617cd020fee16c28fe4d4a2789dc28cb` to measured commit `273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7` for the three C1 files; rc 0, summary `3 files changed, 5831 insertions(+), 0 deletions(-)` (new C1 tool, gate, and expected fixture file).
- No tool/selftest/build/test was run and no tool was installed or updated. The requested jq recount and the committed git diff were the only subprocess commands; both were read-only.