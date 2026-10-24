# C1 targeted falsification — CaseReview23

## Scope and verdict

Attacked only `error_unsettled_custom_settle_60` (`ErrorUnsettled`) and `code_quota_1113_beats_429` (`CodeQuota1113`), including their oracle entries, classifier paths, gate assertions, retained L1 before/after records, and the adjacent negative controls. **Pass for these two cases: no actionable static falsifier found.** The inputs distinguish the claimed behavior; the expected values are independently derivable from the contract, fixture timestamps, and the cited vendor code meanings; retained L1 output matches each asserted value.

The baseline/after L1 records and C1 counter are from the pinned wave measurement, not a rerun of the tool. Neither the tool nor a selftest was run for this review.

## Case evidence

### `error_unsettled_custom_settle_60`

- Oracle at `fixtures/seat/expected.json:1207-1232` pins `now_ms=1761000000000`, `settle_seconds=60`, rc 1 / `MORI_SEAT_TERMINAL_DEAD`, all eight totals, and exactly `boundary`, `recent`, `timestamp-recent` with their classes. The source inputs are pinned (`expected.json:17-19`); L1's after manifest reports all 81 fixture pins verified, with no missing/extra/mismatched pin (`evidence/seat-after/run-manifest.json:1`, `.fixtures.pins`).
- Independent arithmetic from the contract rule (`contract.md:113`, `:120`) and fixture bytes:
  - `boundary.jsonl:2` is exactly `now - 900000`; `recent.jsonl:2` is `now - 100000`; both are older than the 60-second cutoff (`now - 60000 = 1760999940000`) and each carries `429 rate_limit`, so both should be `dead_rate_limit`.
  - `timestamp-recent.jsonl:2` supplies `timestamp=1760999950000`, 50 seconds before scan time, so it is newer than the 60-second cutoff and should be `error_unsettled`. This also exercises timestamp fallback, rather than only `completedAt`.
  - The expected tally (2 aged rate-limit + 1 unsettled) therefore justifies rc 1 and the dead finding; it is not inferred from tool output.
- The classifier uses a strict `>` cutoff before checking error code/tokens/status (`tools/mori-seat-terminal.py:257-272`), matching the stated equality behavior. The L1 retained stdout has all expected per-seat classes, totals, `files_scanned=3`, `now_ms`, and echoed `settle_seconds=60` (`evidence/seat-after/runs/error_unsettled_custom_settle_60.stdout:1`). The after manifest is `match`, `ok=true`, `reasons=[]`, rc 1, three seats and the expected totals (`evidence/seat-after/run-manifest.json:1`, case id). The exact same pack's real differential control `error_unsettled_default_settle` is also `match`, with `recent` and `timestamp-recent` unsettled and `boundary` dead (`evidence/seat-after/run-manifest.json:1`, case id; expected oracle at `expected.json:1179-1204`). Thus the 100-second record changes class when the explicit 60-second override is applied, while the 50-second timestamp record remains unsettled; neither result is vacuous.

### `code_quota_1113_beats_429`

- Oracle at `fixtures/seat/expected.json:1236-1257` pins the fixed scan time, rc 1 / dead finding, all eight totals, and the only seat as `dead_quota`.
- The sole synthetic record (`CodeQuota1113/code-1113.jsonl:2`) is an assistant error at `1760998000000`, 2,000 seconds before scan time (older than the default 900-second settle window). Its status is 429 and its message is `balance exhausted (type=1113)`. `balance` is not a configured quota token; without the business-code branch, the generic 429 path would classify it `dead_rate_limit`. The tested branch extracts the code and checks `1113` as quota before rate codes/tokens/status (`tools/mori-seat-terminal.py:262-272`).
- The oracle is supported by the normative A1 rule (`contract.md:123`) and the official Z.AI error table: code 1113 maps to HTTP 429 with “Insufficient balance or no resource package”; code 1302 also maps to 429 but is “Rate limit reached for requests” (https://docs.z.ai/api-reference/api-code.md, accessed 2026-10-20; the observed table and response shape are recorded at `build/SrcZaiErrorCodes.md:16-20`). This makes the input a real discriminator against status-only classification.
- L1's retained stdout reports code `1113`, status 429, class `dead_quota`, totals `dead_quota=1` / `dead_rate_limit=0`, and the fixed scan time (`evidence/seat-after/runs/code_quota_1113_beats_429.stdout:1`). The after manifest is `match`, `ok=true`, `reasons=[]`, rc 1, one seat, with the same totals (`evidence/seat-after/run-manifest.json:1`, case id). It cannot pass by merely returning rc 1 or a setup finding: the gate pins rc/finding (`tools/mori-round17-seat-regressions.py:1274-1313`), validates every totals class (`:1018-1027`), requires the rc 0/1 schema/aggregate fields (`:1364-1397`), checks seat/totals consistency and rc/dead consistency (`:1399-1448`), and compares every declared total plus each expected and unexpected seat (`:1215-1260`). Both oracle cases supply all eight total values and non-empty seat maps (`fixtures/seat/expected.json:1215-1232`, `:1242-1257`); the pack file/seat counts also agree.
- The negative code-order controls are non-vacuous and retained as matches: `(type=1302)` with `quota exceeded` expects `dead_rate_limit` (`fixtures/seat/CodeRate1302QuotaWord/code-1302-quota.jsonl:2`, `expected.json:1285-1308`, `build/SeatFixtures.md:308`); 1308 with 429 expects `dead_quota` (`expected.json:1261-1284`). Both have `status=match`, `ok=true`, and empty reasons in the L1 after manifest (`evidence/seat-after/run-manifest.json:1`, filtered case ids). The first reverses the 1113 case's discriminator and catches code-order errors; the second covers the other quota code.

## Retained results and read-only recount

Before, both selected cases are `capability_absent`, `observed=null`, and carry only the `capability_absent` reason (`evidence/seat-before/run-manifest.json:1`, case ids). That is an absent-capability baseline, not a green or a claimed production defect. After, both are `match` with `reasons=[]`; the case-specific observations and retained stdout are cited above. L1's persisted counter is `evidence/count-c1.json:5-21`, rc 0, stdout `[54, 0]`.

Read-only recount performed over just these two IDs in the before and after manifests:

```sh
jq -s '[.[] | .cases[] | select(.id == "error_unsettled_custom_settle_60" or .id == "code_quota_1113_beats_429")] | {selected:length, statuses:(group_by(.status) | map({status:.[0].status,count:length}))}' \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-before/run-manifest.json \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-after/run-manifest.json
```

rc=0; output:

```json
{
  "selected": 4,
  "statuses": [
    {
      "status": "capability_absent",
      "count": 2
    },
    {
      "status": "match",
      "count": 2
    }
  ]
}
```

The scoped committed diff from entering tip `24526ea9617cd020fee16c28fe4d4a2789dc28cb` to measured tip `273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7` was read-only: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --no-ext-diff --stat 24526ea9617cd020fee16c28fe4d4a2789dc28cb 273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7 -- tools/mori-seat-terminal.py tools/mori-round17-seat-regressions.py .ufo/waves/round-17/fixtures/seat/expected.json`; rc=0, output `3 files changed, 5831 insertions(+)`. These are added files at the entering tip; the cited current implementation/oracle is the measured change under review.

## Residual risk and verification gaps

- `[INFERENCE]` The vendor page documents a JSON `error.code` field, but does **not** document OMP transcript text in the `(type=NNNN)` form. The source receipt explicitly records this gap (`build/SrcZaiErrorCodes.md:20`, `:35-38`). A1 itself explicitly defines that token and its classification, so the synthetic case passes the contract oracle; this case alone does not establish that a live OMP transcript's `(type=1113)` token is the same field as Z.AI's documented business `code`.
- LSP was unavailable: `read xd://lsp` returned `No such tool` and enumerated the mounted devices without an LSP device. No references/definition/diagnostics query could run. Literal grep was used only to locate the two expected.json source lines, not as semantic proof; the review relied on direct reads of the relevant classifier and gate bodies.
- No tool, selftest, build, or live probe was run. Verification evidence is static source/fixture review, retained L1 before/after artifacts, and the explicitly requested read-only jq recount.