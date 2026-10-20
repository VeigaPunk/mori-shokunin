# Round 17 C1 case falsification — CaseReview22

## Verdict

**No actionable falsifier found in the two assigned cases.** Scope/axes attacked: independent expected values, classifier-vs-contract agreement, complete gate comparisons, genuine negative controls, and non-vacuous class/setup assertions for `mixed_one_seat_per_class` and `error_unsettled_default_settle` only.

## Evidence

- The controlling local rules are Amendment A1 in `.ufo/waves/round-17/contract.md:112-120`: quota/rate ordering; `error_unsettled` for a terminal error newer than scan time minus the settle window (default 900 seconds); and all-class expected totals. The amendment states in `:123` that vendor codes 1113/1308 map to quota and 1302 to rate-limit. The implementation branch at `tools/mori-seat-terminal.py:247-273` checks role/stop reason, then the strict `terminal_ms > now_ms - settle_seconds * 1000` unsettled boundary, then quota/rate/error-other. It does not contradict the contract for these inputs.
- The expected cases are separately persisted in `.ufo/waves/round-17/fixtures/seat/expected.json:1147-1204`, rather than being derived from tool output. The gate parses and validates `want` as case input before execution (`tools/mori-round17-seat-regressions.py:639-698`); for rc 0/1 it requires totals and seats and requires rc 1 to carry at least one dead class (`:657-679`). `compare_want` checks every declared total, every requested seat class, and rejects every unrequested output seat (`:1215-1260`); `evaluate` validates all eight totals and equality to re-derived graded-seat counts before comparing the wants (`:1360-1448`). Thus these are not vacuous rc2/setup cases or class-presence checks that accept an empty observation.

### `mixed_one_seat_per_class` / `MixedFinding`

The eight synthetic byte inputs (`fixtures/seat/MixedFinding/m-*.jsonl:1-2`) each carry the session v3 header and one intended terminal shape, except `m-unavailable`, which has a session-init record and no message. The independent mapping in `expected.json:1154-1175` covers all eight classes and the expected rc/finding (`:1155-1165`): completed (`m-completed`), aborted (`m-aborted`), non-assistant incomplete (`m-incomplete`), aged unmatched error (`m-other`), quota token (`m-quota`), aged 429/rate-limit (`m-rate`), recent error (`m-unsettled`), and no-message unavailable (`m-unavailable`). The recent error timestamp is 1760999900000 against now 1761000000000 (100 seconds old); the aged examples are outside the 900-second window. These are real per-class controls, not empty or malformed substitutes for the asserted classes.

The file bytes are independently pinned: `expected.json:30-37` declares all eight MixedFinding file digests. I ran `sha256sum` over those eight fixture files and the three ErrorUnsettled files; **rc 0, all eleven emitted digests exactly match the corresponding pin entries** (`expected.json:17-19,30-37`).

### `error_unsettled_default_settle` / `ErrorUnsettled`

`expected.json:1180-1204` pins `--now-ms 1761000000000`, rc 1 / `MORI_SEAT_TERMINAL_DEAD`, all eight totals (including zeros), and all three seat classes. In the synthetic bytes (`fixtures/seat/ErrorUnsettled/{boundary,recent,timestamp-recent}.jsonl:1-2`), boundary is 1760999100000, exactly 900000 ms before scan time; the implementation's strict `>` check therefore does not classify it unsettled, and its 429 status makes it `dead_rate_limit`. `recent` is 100000 ms old and `timestamp-recent` is 50000 ms old; both fall inside the default 900-second window and are `error_unsettled`. `timestamp-recent` exercises the message `timestamp` fallback, as `_message_view` reads `completedAt` then `timestamp` (`tools/mori-seat-terminal.py:235-240`). The boundary seat is a genuine negative control for the recent/unsettled class.

## Retained L1 results and count

I read, but did not rerun, the retained L1 case rows. In `.ufo/waves/round-17/evidence/seat-before/run-manifest.json:1`, both exact IDs have `status: capability_absent`, `observed: null`, and reason `capability_absent`; this is not a behavioral baseline for the classifier. In `.ufo/waves/round-17/evidence/seat-after/run-manifest.json:1`, both have `status: match`, `ok: true`, `reasons: []`, `pack_changed: false`, rc 1, the expected finding ID, expected totals, and the expected seat counts. The corresponding retained stdout records (`evidence/seat-after/runs/mixed_one_seat_per_class.stdout:1` and `error_unsettled_default_settle.stdout:1`) show the complete seat lists and every class: MixedFinding has exactly one of each of eight classes; ErrorUnsettled has boundary=`dead_rate_limit`, recent=`error_unsettled`, timestamp-recent=`error_unsettled`. Their totals exactly match the `want` maps; both retained stderr streams are empty. The after-manifest `reasons` arrays are empty.

Required read-only count command:

```text
jq -r '[.cases[] | select(.id == "mixed_one_seat_per_class" or .id == "error_unsettled_default_settle")] | length' /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/fixtures/seat/expected.json
rc=0
stdout: 2
```

## Residual risk and verification gaps

This review is limited to these two synthetic cases; the before records prove capability absence, not prior-classifier behavior. No tool, gate, selftest, or other runtime was run. `read xd://lsp` returned `No such tool: xd://lsp` (the mounted device list had no LSP device), so status/references/definition/diagnostics were unavailable; grep was used only to locate case IDs and lines, not as semantic proof. The normative 900-second settle threshold is the lane's A1 policy, not a duration mandated by an external HTTP standard; S042 explicitly notes RFC 9110 §10.2.3 does not define 429 or terminal settle behavior (`build/SrcRfc9110.md:47-73`). No outside-standard claim is made for that policy. No tools were installed or updated.
