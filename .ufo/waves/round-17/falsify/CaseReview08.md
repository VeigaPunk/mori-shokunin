# CaseReview08 — C1 aborted terminal cases

## Axes and verdict

Axes attacked: classification correctness; independence/integrity of expected evidence; non-vacuity of cases and controls.

**No actionable defect found in the assigned cases** `aborted_terminal` and `aborted_beats_error_fields`. This is a scoped result, not a blanket pass of C1.

## Evidence

- **Inputs and supported expectation.** The synthetic records are nonempty schema-v3 sessions: `fixtures/seat/Aborted/aborted-terminal.jsonl:1-2` has assistant `stopReason:"aborted"`; `fixtures/seat/AbortedErrorFields/aborted-with-error-fields.jsonl:1-2` has the same terminal role/reason plus timestamp `1760998000000`, status 429, `Retry budget exhausted after 3 retries ... (type=1302)`, and provider/model fields. The binding rule explicitly maps assistant/aborted to `aborted`, while dead error classes require `stopReason == "error"` (`contract.md:47-59`); Amendment A1's settle window likewise applies to terminal error records (`contract.md:113`). Thus the asserted class is supported independently by the stated contract, not inferred from the implementation. The implementation follows that order: aborted is returned at `tools/mori-seat-terminal.py:251-257`, before any error-only checks at `:259-273`.
- **Expected values are pinned and non-derived.** `fixtures/seat/expected.json:439-460` and `:464-485` separately declare `rc:0`, `MORI_SEAT_TERMINAL_OK`, all eight class totals (exactly one aborted, zero for each other class), and the exact expected seat/class. The input-byte pins are at `expected.json:4-5`; `PINNED_INPUTS.json:13` pins the expected-table digest. Read-only `sha256sum` over the two fixture files returned rc=0 and exactly `1f59604fa5caaf03531167ce2830dc6d0acda6430cb89b890c7afe1edef663fb` and `9b52be45da49eda0cbaa5578e904b3fc68ed2c2e63b5d76134438118706085f7`, matching `expected.json:4-5`. The retained after-manifest also reports fixture pins `verified:true`, no missing/extra/mismatched pins and `inputs_changed:[]` (`evidence/seat-after/run-manifest.json:1`, `.fixtures` fields).
- **Gate checks the declared assertions rather than deriving them from output.** The loader validates rc/finding consistency and that rc 0/1 cases carry totals and seats, then checks the totals against the declared seat tally (`tools/mori-round17-seat-regressions.py:646-679`). `compare_want` compares each declared class total and exact expected seat/class, rejecting missing or unexpected seats (`:1215-1260`); `evaluate` checks rc/finding, requires the scan output fields, validates all class keys and ties totals back to the returned seat rows (`:1274-1313`, `:1364-1448`). Gate code separately verifies fixture pins before execution (`:1598-1668`) and invokes/evaluates the tool for each case (`:1711-1747`).
- **Retained L1 observations.** Before-manifest case rows are `capability_absent`, `ok:false`, `observed:null` for both IDs (`evidence/seat-before/run-manifest.json:1`, case IDs). This is explicitly a capability-absent baseline, not a prior behavioral observation (gate logic: `tools/mori-round17-seat-regressions.py:1670-1707`). After-manifest rows are `match`, `ok:true`, `reasons:[]`, with rc 0, finding OK, `files_scanned:1`, `seat_count:1`, and exactly the declared totals for each case (`evidence/seat-after/run-manifest.json:1`, case IDs). The retained stdout records confirm the asserted seat class is `aborted` in both files (`evidence/seat-after/runs/aborted_terminal.stdout:1`; `.../aborted_beats_error_fields.stdout:1`). The error-bearing output additionally retains status 429, code 1302, retries 3 and retry-exhausted true while the class remains aborted. Those metadata fields are observed, but are not part of these cases' `want` assertions.
- **Controls and non-vacuity.** The error-field case is not a vacuous clean: a real adjacent control uses an aged assistant `stopReason:"error"` with status 429 and code 1302 (`fixtures/seat/RateLimitRetryExhausted/zai-retry-exhausted.jsonl:1-2`); its separate expected result is rc 1/dead_rate_limit with one seat (`expected.json:237-260`), and the retained after result is `match` with `dead_rate_limit:1` (`evidence/seat-after/run-manifest.json:1`; `runs/rate_limit_zai_retry_exhausted.stdout:1`). Each assigned pack contains one ordinary JSONL file, and both observed scans return one file and one seat. For these strict rc-0 cases the gate requires scanned files and returned rows to equal the fixture count (`tools/mori-round17-seat-regressions.py:1428-1435`); expected totals enumerate every class and the nonempty seat map checks the outcome. The setup/finding/rc combination is also compared (`:1274-1313`), so an empty-pack or setup response cannot satisfy these cases.

## Read-only count and verification gaps

Command (read-only retained-manifest count):

```sh
jq -s -c '[.[] | [.cases[] | select(.id == "aborted_terminal" or .id == "aborted_beats_error_fields")] | {count:length,ids:map(.id),statuses:map(.status),ok:map(.ok)}]' \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-before/run-manifest.json \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-after/run-manifest.json
```

rc=0; output:

```json
[{"count":2,"ids":["aborted_terminal","aborted_beats_error_fields"],"statuses":["capability_absent","capability_absent"],"ok":[false,false]},{"count":2,"ids":["aborted_terminal","aborted_beats_error_fields"],"statuses":["match","match"],"ok":[true,true]}]
```

The requested diff from entering `24526ea9617cd020fee16c28fe4d4a2789dc28cb` to measured `273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7` shows the C1 tool, gate and expected table as additions (3 scoped files, 5,831 insertions, no deletions). No selftest, build or live tool run was performed. The `lsp` device is not mounted (`read xd://lsp` returned “No such tool”), so no LSP status/references/definition/diagnostics were available; grep was used only to locate identifiers, with semantic review based on the cited file contents. Remaining scope risk: this review covers only these two cases and retained L1 artifacts, not live transcript behavior or the rest of C1.