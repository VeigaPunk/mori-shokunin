# CaseReview18 — C1 case falsification

## Scope and method

Reviewed the base-to-measured-tip diff for `tools/mori-seat-terminal.py`, `tools/mori-round17-seat-regressions.py`, and `fixtures/seat/expected.json`; all three are additions relative to `24526ea9617cd020fee16c28fe4d4a2789dc28cb`. Read the contract/A1, pinned inputs, and wave context. No tool, selftest, build, or live probe was run. The `lsp` device was unavailable: `read xd://lsp` returned “No such tool” and listed the mounted devices without LSP. Grep was used only for locating source lines; semantic conclusions below are from direct file reads and retained receipts.

Expected values are static in `expected.json`; the expected table itself is pinned by `PINNED_INPUTS.json:13`. Its fixture pin map includes both packs (`expected.json:47-53,77-79`), and the retained after manifest reports 81 declared pins, `verified: true`, no missing/extra/mismatched inputs (`evidence/seat-after/run-manifest.json:1`). I independently checked the expected values against A1 and the synthetic fixture bytes, rather than deriving them from the after output.

## Findings (severity order)

### MEDIUM — `prefix_filter_no_match` accepts the wrong setup reason

A1 requires an exact zero-match prefix filter to produce rc2 with `reason: "prefix-matched-none"` (`contract.md:114-116`). The fixture is a real exact-match negative control: the expected arg is `--prefix Tsukuroi` (`fixtures/seat/expected.json:945-955`), while the pack contains stems `TsukuroiR17`, `TsukuroiR17Extra`, `SoujiR17-30`, and the other nonmatching prefixes (`fixtures/seat/PrefixAttribution/TsukuroiR17.X.jsonl:1-2`, `TsukuroiR17.Y.jsonl:1-2`, `TsukuroiR17Extra.Xtrap.jsonl:1-2`; `tools/mori-seat-terminal.py:449-466` derives the prefix before the first dot and compares it by equality). Thus the intended no-match is source-supported, not an empty-pack artifact.

However, the expected `want` contains only rc2 and `MORI_SEAT_TERMINAL_SETUP`; it does not pin the setup reason or any other result field (`expected.json:953-956`). The gate’s `WANT_KEYS` omits `reason` (`tools/mori-round17-seat-regressions.py:214-216`); for rc2 it skips the output-key allowlist (`:1301-1305`), checks the finding/rc agreement (`:1309-1313`), then validates only optional totals/seats (`:1449-1458`). `compare_want` is non-strict for rc2 and returns without a seat assertion when `want.seats` is empty (`:1215-1226`). Therefore a static counterexample—same valid sandbox path and schema, rc2/finding `MORI_SEAT_TERMINAL_SETUP`, but `reason: "unavailable-dir"`—would still satisfy this case. That contradicts the case’s specific prefix-empty purpose even though the current tool behaves correctly.

The retained after stdout does report `reason:"prefix-matched-none"` and `files_scanned:0` (`evidence/seat-after/runs/prefix_filter_no_match.stdout:1`); the manifest says `status:"match"` (`evidence/seat-after/run-manifest.json:1`). Those useful observed fields are not asserted by this case. The before manifest records `capability_absent` for this case (`evidence/seat-before/run-manifest.json:1`).

### LOW — `tail_small_window_far_terminal_lost` does not assert why the far seat is unavailable

The class assertions are not vacuous: the expected table pins all eight class totals and all three seat classes (`fixtures/seat/expected.json:959-984`), and the gate validates the class tally against those seats. The source bytes support the values: `tail-far.jsonl` has a v3 header and completed message at lines 1-2, followed by custom records through line 82; read-only `jq -s` over that file found 82 records, the sole message at line 2, and eight custom records in the suffix. Its file size is 12,765 bytes, so the selected 1,000-byte suffix cannot contain that early message. The positive controls are also real: `tail-near.jsonl`’s only message is the final line 3002, and `tail-partial.jsonl` has a long custom record at line 2 followed by its completed message at line 3 (482,025 and 6,186 bytes respectively; see `wc -lc` inspection). `_read_tail` seeks to the bounded suffix and discards a partial first line (`tools/mori-seat-terminal.py:319-351`), then `_terminal_view` selects parseable message records (`:354-365`). The retained after stdout matches the expected classes/totals and reports the far seat as `unavailable` with `reason:"no-message"` (`evidence/seat-after/runs/tail_small_window_far_terminal_lost.stdout:1`); the after manifest is `match`, while before is `capability_absent` (`evidence/seat-after/run-manifest.json:1`, `evidence/seat-before/run-manifest.json:1`).

The remaining test hole is reason-level: the gate accepts any of `schema`, `no-message`, or `unreadable` for an unavailable seat (`tools/mori-round17-seat-regressions.py:191,1087-1089`), and `compare_want` compares only the expected seat class (`:1238-1259`). The expected schema cannot express a reason (`:214-216`). A counterexample row for `tail-far` with the same class but `reason:"schema"` would pass, despite the fixture’s valid version-3 header (`tail-far.jsonl:1`) and the case intending to prove terminal loss beyond the tail window. This does not invalidate the class totals; it leaves the targeted cause unproven.

## Read-only retained-case count

Command:

```sh
jq -s '[.[].cases[] | select(.id == "prefix_filter_no_match" or .id == "tail_small_window_far_terminal_lost")] | {case_count:length, by_case:(group_by(.id) | map({id:.[0].id, occurrences:length, statuses:map(.status)}))}' \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-before/run-manifest.json \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-after/run-manifest.json
```

rc=0; output:

```json
{
  "case_count": 4,
  "by_case": [
    {"id":"prefix_filter_no_match","occurrences":2,"statuses":["capability_absent","match"]},
    {"id":"tail_small_window_far_terminal_lost","occurrences":2,"statuses":["capability_absent","match"]}
  ]
}
```

## Verdict and residual risk

Falsifiers are regression-oracle gaps, not observed wrong after-run outputs: the prefix test treats any setup failure as the intended zero-match setup, and the tail test does not distinguish a tail-window miss from another unavailable reason. The current retained observations match every field that the cases actually assert; both fixture packs and negative controls are non-vacuous. No mutation probe was authorized or run, so these are static acceptance counterexamples.

Report: .ufo/waves/round-17/falsify/CaseReview18.md
