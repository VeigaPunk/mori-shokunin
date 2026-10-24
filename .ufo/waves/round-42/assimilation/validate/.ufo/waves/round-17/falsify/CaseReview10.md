# CaseReview10 — C1 incomplete-terminal cases

## Scope / axes

Attacked only `incomplete_user_terminal` (pack `IncompleteUser`) and `incomplete_tooluse_and_no_stop_reason` (pack `IncompleteToolUse`): expected-value independence/source support, terminal classification, complete observation-vs-want comparison, and non-vacuous class/setup controls. This is a recommendation on these two cases, not L1 admission or a blanket C1 review.

## Findings (severity order)

No actionable finding in the two assigned cases.

## Evidence

- **Source supports both expected classes.** Contract `contract.md:47-58` defines terminal-message classification and `:56-57` includes an assistant with any non-`error`/non-`stop`/non-`aborted` stop reason as `incomplete`; Amendment A1 `:117-120` requires schema v3 and says terminal roles other than assistant are `incomplete`. In the implementation, `_terminal_view` retains the last parseable message (`tools/mori-seat-terminal.py:354-365`); `_classify` maps a non-assistant role to `incomplete` (`:247-252`) and assistant stop reasons other than `stop`, `aborted`, or `error` to `incomplete` (`:253-258`).
- **Synthetic bytes and static wants are specific and non-empty.** `IncompleteUser/incomplete-user.jsonl:1-3` is a v3 header, assistant `stop`, then terminal user message; the expected result is one `incomplete-user` seat (`fixtures/seat/expected.json:540-562`). `IncompleteToolUse/no-stop-reason.jsonl:1-2` is an assistant record with no stop reason, and `tool-use-terminal.jsonl:1-2` has assistant `stopReason: toolUse`; the expected result is two named `incomplete` seats (`expected.json:565-588`). Both wants pin rc 0, `MORI_SEAT_TERMINAL_OK`, all eight class totals (not just the nonzero one), and explicit seat identities/classes.
- **Expected values are structurally independent and inputs are pinned.** The gate consumes a separately persisted `expected.json`; its documentation says fixture pins are independent persisted evidence and checks them before any tool run (`tools/mori-round17-seat-regressions.py:17-43,1598-1652`). Expected-table SHA-256 is pinned by `PINNED_INPUTS.json:13` (`b684c63bf3cebe70f24d3d02f3f0df4f63aad3f547a365a3ca1864f5f57cb01f`). The three target fixture hashes from read-only `sha256sum` exactly match `expected.json:22-24`: `8a6bd3e8f451fdb9c210a89c5e09d1d1a14d50c9566ada1ad62f2fe935618530`, `99eec30bf279091ea911906af9fbca92397d9ca4df1b4dce474fd9575f5a1faa`, and `831cf05f933d7717faf9409416ad6d84ad56ac3d3244d61dde91bf59e9cd7bfd` respectively.
- **The gate does not accept a setup outcome for these wants.** For rc 0/1, expected wants must carry totals and seats and the gate checks the seat-derived tally (`tools/mori-round17-seat-regressions.py:657-678`); `compare_want` checks each declared class count, expected seat class, missing seats, and extra seats (`:1215-1260`). Runtime output must contain the strict result fields and valid eight-class totals (`:1364-1448`). Since both assigned wants require rc 0 and nonempty `incomplete` seats, rc 2/setup or empty output cannot satisfy them (`expected.json:547-560,571-586`).
- **Retained L1 observations match every asserted field.** Before, both case rows in `evidence/seat-before/run-manifest.json:1` are `capability_absent`, `ok:false`, `observed:null`, `pack_changed:false` (the intended entering-capability baseline). After, both rows in `evidence/seat-after/run-manifest.json:1` are `status:"match"`, `ok:true`, `reasons:[]`, `pack_changed:false`. Retained stdout `evidence/seat-after/runs/incomplete_user_terminal.stdout:1` has rc-implied OK finding, `files_scanned:1`, `incomplete:1`, all other totals zero, and exactly seat `incomplete-user: incomplete`; `.../incomplete_tooluse_and_no_stop_reason.stdout:1` has `files_scanned:2`, `incomplete:2`, all other totals zero, and exactly `no-stop-reason` plus `tool-use-terminal`, both incomplete. These are exact matches to the two wants above; both retained stderr files are zero bytes per manifest.
- **Controls are real; class/setup acceptance is not vacuous.** The user pack itself has a real earlier assistant `stop` followed by the terminal user record (fixture lines 2-3), exercising last-message precedence. Separate control fixtures contain a completed transcript ending in assistant `stop` after an earlier error (`Completed/completed-after-error.jsonl:1-4`) and an aborted terminal (`Aborted/aborted-terminal.jsonl:1-2`); their wants distinguish `completed` and `aborted` (`expected.json:389-411,439-461`), and retained L1 results are matched with `completed:1/incomplete:0` and `aborted:1/incomplete:0` (`evidence/seat-after/run-manifest.json:1`). `mixed_one_seat_per_class` wants exactly one seat in each of the eight classes (`expected.json:1148-1177`), and L1 observed 8 scanned/8 seats with each class count 1 and matched status (`evidence/seat-after/run-manifest.json:1`). Setup controls are also explicit: missing-directory rc2/setup (`expected.json:718-727`) and zero-prefix-match rc2/setup (`:945-956`) both match in L1 (`evidence/seat-after/run-manifest.json:1`). Their assertions intentionally pin rc/finding only; they do not assert a diagnostic reason.

## Required read-only count

Command (no gate/tool/selftest run):

```sh
jq -s '[.[] | [.cases[] | select(.id=="incomplete_user_terminal" or .id=="incomplete_tooluse_and_no_stop_reason")] | {count:length, cases:map({id,status,ok})}]' \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-before/run-manifest.json \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-after/run-manifest.json; rc=$?; printf 'rc=%d\\n' "$rc"
```

Observed `rc=0`; output:

```json
[
  {"count":2,"cases":[{"id":"incomplete_user_terminal","status":"capability_absent","ok":false},{"id":"incomplete_tooluse_and_no_stop_reason","status":"capability_absent","ok":false}]},
  {"count":2,"cases":[{"id":"incomplete_user_terminal","status":"match","ok":true},{"id":"incomplete_tooluse_and_no_stop_reason","status":"match","ok":true}]}
]
```

## Residual risk / verification gaps

- No fresh gate, tool, build, test, or selftest was run, per assignment; judgment uses retained L1 receipts and static inspection only.
- `read xd://lsp` returned `No such tool: xd://lsp` (no LSP device is mounted), so no LSP status/references/definition/diagnostics were available. Text grep was used only to locate line anchors; conclusions above come from direct source/fixture/manifest reads. [INFERENCE] The reviewed artifacts establish structural separation of the expected table from runtime output, but contain no separate author-identity attestation for who authored the expected values.