# CaseReview09 — C1 case falsification

## Axes reviewed

- C1 coverage: terminal-record classification for `ErrorOther` and terminal `toolResult`.
- Oracle independence/source support and gate non-vacuity for these two cases.

## Finding — Low: `incomplete_toolresult_terminal` does not discriminate terminal-record selection

The pack contains an assistant `toolUse` message followed by a `toolResult` message (`.ufo/waves/round-17/fixtures/seat/IncompleteToolResult/incomplete-tool-result.jsonl:2-3`). The intended last-record logic is present in `tools/mori-seat-terminal.py:354-365`, but both possible selected records produce the asserted class: `_classify` returns `incomplete` for a non-assistant role (`:251-252`) and also for an assistant whose `stopReason` is not `error` (`:257-258`). Thus selecting only the first record is a concrete counterexample that still yields `incomplete`.

The gate cannot observe which record supplied the class: its allowed seat fields omit `role` and `stopReason` (`tools/mori-round17-seat-regressions.py:199-213`), and `compare_want` checks class/totals and expected seat membership (`:1215-1260`). Both records have null provider/model/status/timestamp and no retry/error code; `_seat_record` emits only those derived fields (`tools/mori-seat-terminal.py:368-383`). A first-record implementation would therefore produce the same asserted seat fields and totals for this pack. The case is valid for the desired class, but does not falsify a terminal-selection regression specific to this example. To make this assertion discriminating, give the preceding message a class different from `incomplete` while retaining the terminal `toolResult`.

## Checks that held within scope

- `error_other_thinking_and_bare` has two schema-v3 assistant error records (`ErrorOther/thinking-loop-error.jsonl:1-2`; `ErrorOther/bare-error.jsonl:1-2`). The thinking-loop text has no quota/rate token, no 429 status, and its timestamp `1760998000000` is 2,000,000 ms older than the pinned scan time `1761000000000`; the bare error has no status/message/timestamp. These inputs support `dead_error_other`, not `error_unsettled`, under the ordering and settle rules (`contract.md:112-113`, original fallback at `:55`; classifier/token definitions in `tools/mori-seat-terminal.py:78-89,247-273`). The expected `rc:1`, `MORI_SEAT_TERMINAL_DEAD`, two `dead_error_other` seats, and zeroes for all other classes are pinned at `expected.json:489-511`.
- `incomplete_toolresult_terminal` expects `rc:0`, `MORI_SEAT_TERMINAL_OK`, one `incomplete` seat, and zeroes for the other seven classes (`expected.json:515-536`). That class is source-supported by Amendment A1 (`contract.md:118`), although the fixture cannot distinguish the terminal record as described above.
- These expectations are separately persisted in `expected.json`; they are not obtained from a live tool result. The current expected/tool/gate SHA-256 values match `PINNED_INPUTS.json:8-13`. The three input-file SHA-256 values also match the corresponding fixture pins in `expected.json:15-16,21` (command/output below).
- Neither case is a vacuous setup/empty-class pass. Both expected cases pin `--now-ms`; the `ErrorOther` want lists all eight classes and requires two dead seats, while the `IncompleteToolResult` want lists all eight and requires one incomplete seat (`expected.json:489-536`). For `rc` 0/1, the gate requires totals and seats, checks the seat-derived tally and rc/dead consistency, then strictly compares totals, missing/extra seats, and class (`tools/mori-round17-seat-regressions.py:657-679,1215-1260,1364-1448`). Setup `rc:2` cannot match either expected rc/finding pair (`:646-655,1274-1313`).

## Retained L1 results and read-only count

`evidence/seat-before/run-manifest.json:1` records both cases as `capability_absent`, `ok:false`, reason `capability_absent` (not a false green). `evidence/seat-after/run-manifest.json:1` records both as `match`, `ok:true`, reasons `[]`; observed summaries are:

- `error_other_thinking_and_bare`: rc 1, `MORI_SEAT_TERMINAL_DEAD`, 2 files/seats, `dead_error_other:2`, all other classes 0.
- `incomplete_toolresult_terminal`: rc 0, `MORI_SEAT_TERMINAL_OK`, 1 file/seat, `incomplete:1`, all other classes 0.

Read-only count command (only the two named manifest entries; no tool or selftest run):

```sh
jq -s '[.[] | .cases[] | select(.id == "error_other_thinking_and_bare" or .id == "incomplete_toolresult_terminal")] | sort_by(.id) | group_by(.id) | map({id: .[0].id, runs: length, statuses: map(.status), ok: map(.ok), reasons: map(.reasons)})' \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-before/run-manifest.json \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-after/run-manifest.json
```

rc 0; output:

```json
[
  {
    "id": "error_other_thinking_and_bare",
    "runs": 2,
    "statuses": ["capability_absent", "match"],
    "ok": [false, true],
    "reasons": [["capability_absent"], []]
  },
  {
    "id": "incomplete_toolresult_terminal",
    "runs": 2,
    "statuses": ["capability_absent", "match"],
    "ok": [false, true],
    "reasons": [["capability_absent"], []]
  }
]
```

Read-only pin checks (rc 0):

```text
sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/fixtures/seat/ErrorOther/bare-error.jsonl /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/fixtures/seat/ErrorOther/thinking-loop-error.jsonl /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/fixtures/seat/IncompleteToolResult/incomplete-tool-result.jsonl
90aa1d0884b23e3a3224c61d9428f31e78d2d29119c6443927bec0a073b9e708  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/fixtures/seat/ErrorOther/bare-error.jsonl
5f46e413a6b1674330d8af0bee1ed7978c407cede06af8354ad6f3d781398afd  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/fixtures/seat/ErrorOther/thinking-loop-error.jsonl
378812178442010e75ba62396d4a4ba4446567a7b25e9bce5f23821e7ac29fc1  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/fixtures/seat/IncompleteToolResult/incomplete-tool-result.jsonl

sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/fixtures/seat/expected.json /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-seat-terminal.py /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-round17-seat-regressions.py
b684c63bf3cebe70f24d3d02f3f0df4f63aad3f547a365a3ca1864f5f57cb01f  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/fixtures/seat/expected.json
5819c3c06e4ceded02b043ef1edbe15043359f176f1b24830b4d3cae24adbdba  /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-seat-terminal.py
21285c2b7000bf63cd9fd679f4b88a7d5d4ff250eee0279576d6d0dcb3b97f7a  /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-round17-seat-regressions.py
```

## Residual risk and verification gaps

The `lsp` device is not mounted (`read xd://lsp` returned “No such tool” and listed mounted devices without `lsp`), so no LSP status/references/definition/diagnostics were available. Grep was used only to locate lines; semantic checks above use direct file reads and receipts. The case directories contain no retained raw stdout; the after manifest retains output hashes and comparator status/reasons, so the recorded L1 match is supported by the gate implementation but raw output cannot be independently re-parsed from retained files. No tool, selftest, build, or live probe was run.
