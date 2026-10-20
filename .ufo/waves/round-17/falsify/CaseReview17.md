# CaseReview17 — C1 prefix-filter falsification

**Verdict:** No actionable falsifier found in the scoped `prefix_filter_kumitate` and `prefix_filter_multi` cases. This is not a blanket C1 pass.

**Axes checked:** independent expected values, exact prefix attribution, live negative controls, and non-vacuous gate assertions.

## Evidence and analysis

The contract defines prefix as the stem before the first dot (`.ufo/waves/round-17/contract.md:41-42`); Amendment A1 requires no-match setup failure and pins `--now-ms` (`.ufo/waves/round-17/contract.md:113-120`). The implementation derives `stem.split(".", 1)[0]` and retains a seat only when that prefix is exactly in the requested set (`tools/mori-seat-terminal.py:449-451`). Classification follows the contract: stop → completed, aborted → aborted, and error timestamps older than the settle cutoff proceed to quota/rate classification (`tools/mori-seat-terminal.py:247-273`; `.ufo/waves/round-17/contract.md:47-59,112-120`).

I independently reconstructed both `want` entries from the synthetic records and contract, not from the retained output:

- `prefix_filter_kumitate` fixes `--now-ms 1761000000000` and selects `KumitateR17-2` (`.ufo/waves/round-17/fixtures/seat/expected.json:885-910`). Its input is schema 3 with assistant `stopReason:"aborted"` (`.ufo/waves/round-17/fixtures/seat/PrefixAttribution/KumitateR17-2.Q.jsonl:1-2`), so exactly one `aborted` seat, zero in the other seven totals, `MORI_SEAT_TERMINAL_OK`, rc 0 are supported.
- `prefix_filter_multi` selects exactly `TsukuroiR17` and `SoujiR17-3` (`.ufo/waves/round-17/fixtures/seat/expected.json:912-942`). The matching records are: `SoujiR17-3.W` and `TsukuroiR17.X` stop/completed (`.ufo/waves/round-17/fixtures/seat/PrefixAttribution/SoujiR17-3.W.jsonl:1-2`, `.ufo/waves/round-17/fixtures/seat/PrefixAttribution/TsukuroiR17.X.jsonl:1-2`); `SoujiR17-3.Z` has `quota exceeded` and timestamp `1760998000000` (`.ufo/waves/round-17/fixtures/seat/PrefixAttribution/SoujiR17-3.Z.jsonl:1-2`); `TsukuroiR17.Y` has `429 rate_limit`, status 429, and the same timestamp (`.ufo/waves/round-17/fixtures/seat/PrefixAttribution/TsukuroiR17.Y.jsonl:1-2`). With the pinned scan time and default 900-second settle window, the error timestamps are 2,000 seconds old and therefore not unsettled; the expected classes are one `dead_quota` and one `dead_rate_limit`, alongside two completed seats. Thus rc 1 and `MORI_SEAT_TERMINAL_DEAD` are supported.

The multi-prefix pack contains real near-prefix negatives, not malformed/setup decoys: `SoujiR17-30.Trap.jsonl` is a schema-3 aborted transcript (`.ufo/waves/round-17/fixtures/seat/PrefixAttribution/SoujiR17-30.Trap.jsonl:1-2`), and `TsukuroiR17Extra.Xtrap.jsonl` is a schema-3 completed transcript (`.ufo/waves/round-17/fixtures/seat/PrefixAttribution/TsukuroiR17Extra.Xtrap.jsonl:1-2`). Their extracted prefixes are `SoujiR17-30` and `TsukuroiR17Extra`, not either requested exact prefix. The other nonmatching pack member is `KumitateR17-2.Q.jsonl` (`.ufo/waves/round-17/fixtures/seat/PrefixAttribution/KumitateR17-2.Q.jsonl:1-2`). The actual fixture digests for all seven `PrefixAttribution` files match the corresponding `.ufo/waves/round-17/fixtures/seat/expected.json:47-53` pins (read-only `sha256sum` output); the expected file and both tool files also match `.ufo/waves/round-17/PINNED_INPUTS.json:8-9,13`.

## Gate assertions and retained L1 observations

The selected cases do not pass through setup: their expected rc values are 0 and 1, and each expects nonempty seat maps and all eight explicit class totals (`.ufo/waves/round-17/fixtures/seat/expected.json:894-909,923-941`). Gate evaluation checks rc and finding identity (`tools/mori-round17-seat-regressions.py:1274-1313`), requires the result schema/seat/totals fields (`tools/mori-round17-seat-regressions.py:1364-1379`), checks every expected total and seat class, and rejects missing or unexpected seats (`tools/mori-round17-seat-regressions.py:1215-1260`). For prefix cases the `files_scanned` bound is intentionally loose (`tools/mori-round17-seat-regressions.py:1428-1436`), but it does not make these cases vacuous: expected seat membership is still exact, and both retained outputs have matching seat counts. The retained after stdout shows one Kumitate seat and four multi-prefix seats, with the exact expected classes and totals (`.ufo/waves/round-17/evidence/seat-after/runs/prefix_filter_kumitate.stdout:1`, `.ufo/waves/round-17/evidence/seat-after/runs/prefix_filter_multi.stdout:1`). The after manifest records `status:"match"`, `ok:true`, `reasons:[]`, rc/finding/totals consistent with those outputs (`.ufo/waves/round-17/evidence/seat-after/run-manifest.json:1`, `cases[]` by the two IDs). The before manifest records both as `capability_absent`, `ok:false`, `observed:null` (`.ufo/waves/round-17/evidence/seat-before/run-manifest.json:1`, same IDs); these are baseline absence records, not green case observations.

Read-only requested manifest count:

```sh
jq -s '[.[] | [.cases[] | select(.id == "prefix_filter_kumitate" or .id == "prefix_filter_multi")] | {selected: length, matched: ([.[] | select(.status == "match")] | length), capability_absent: ([.[] | select(.status == "capability_absent")] | length), mismatched: ([.[] | select(.status == "mismatch")] | length)}]' \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-before/run-manifest.json \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-after/run-manifest.json
```

Observed rc 0; stdout:

```json
[
  {"selected":2,"matched":0,"capability_absent":2,"mismatched":0},
  {"selected":2,"matched":2,"capability_absent":0,"mismatched":0}
]
```

## Verification limits

No LSP device is mounted: `read xd://lsp` returned “No such tool” and listed the available devices without LSP, so LSP status/references/definition/diagnostics could not be requested. `grep` was used only to locate case IDs/branches; conclusions above are from the cited source and fixture reads. I did not run the tool, gate, selftests, build, or other checks. No tool was installed or updated. Scope is only the two named C1 cases and their retained L1 before/after evidence.
