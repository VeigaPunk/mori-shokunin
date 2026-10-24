# CaseReview07 — C1 completed-terminal cases

## Verdict

The two assigned cases correctly distinguish a terminal completion from nonterminal/other-record error traps, and the retained L1 after-run matches every assertion currently encoded in these cases. **Not a clean A2 pass:** both cases are still missing the new A2 metadata expectations, which the current gate cannot accept or compare; the scanner also materializes fields that A2 forbids. No tool or selftest was run.

## Findings

### [P1] The scanner materializes whole records and retains raw error text

A2 allows only a narrow field projection and requires that unapproved content/usage values not be materialized and that permitted error text be reduced immediately to flags/metadata, never retained (`.ufo/waves/round-17/contract.md:133-137`). The assigned fixtures make this a concrete per-case counterexample:

- `fixtures/seat/Completed/completed-after-error.jsonl:2-4` contains message records with unapproved content/usage fields; line 3 also has an aged error record before the final completion. `_terminal_view` calls `json.loads` on each entire line before filtering/projecting (`tools/mori-seat-terminal.py:357-364`), so the full JSON values are materialized. For the line-3 message, `_message_view` reads the complete `errorMessage` string (`:217`), derives tokens (`:222-223`), then stores the original string in `view["error_message"]` (`:232`). This happens even though the view is later superseded by the final completed message.
- `fixtures/seat/CompletedTrailing/completed-trailing-nonmessage.jsonl:3-4` has a trailing `type:"custom"` record with an embedded message object. The whole line is likewise decoded at `tools/mori-seat-terminal.py:357-362` before `_message_view` rejects it on the `type != "message"` check (`:207-212`). Thus the record is not actually skipped unread as the C1 contract says (`contract.md:45-47`), although it does not affect classification.

The retained stdout does not expose these values; the defect is the implementation's field materialization/retention against the explicit A2 privacy invariant, not an asserted output mismatch.

### [P2] The assigned expectations do not implement A2 metadata assertions

A2 says fixture expectations gain independent `want.reason`, `want.records`, and `want.top` assertions (`.ufo/waves/round-17/contract.md:142-144`). Neither assigned case has them: `fixtures/seat/expected.json:389-410` and `:414-435` contain only `rc`, `finding_id`, `totals`, and `seats`. The gate still declares only those four accepted want keys (`tools/mori-round17-seat-regressions.py:216`); `_analyze_case` rejects any other want key (`:639-645`), `CaseSpec` has no corresponding fields (`:467-478`), and `compare_want` compares only declared totals and seat classes (`:1215-1260`). Therefore these cases cannot pin or grade A2's reason/record/top metadata, and their `match` receipts are insufficient evidence for those A2 assertions.

## Checks that did pass for the assigned outcomes

- Independent derivation: C1 defines the terminal record as the last qualifying `type == "message"` record and `completed` as assistant + `stop` (`contract.md:45-48`). The first fixture's final message is completed (`Completed/completed-after-error.jsonl:4`); its preceding aged 429 record (`:3`) would be a real dead-rate-limit counterfactual if incorrectly selected as terminal (the pinned now is `1761000000000`, default settle window 900s; A1 at `contract.md:113`). The trailing fixture has a completed message at line 2, then a `custom` record with an embedded error and a `session_init` record (`CompletedTrailing/completed-trailing-nonmessage.jsonl:2-4`); the C1 type filter requires both trailing records to be ignored. A missing last-message rule or a missing record-type filter would change the class, so these are non-vacuous controls.
- Both expected objects pin all eight class totals, including zeroes (`expected.json:398-410,423-435`). The gate requires exactly the eight observed class keys (`tools/mori-round17-seat-regressions.py:1018-1028`), derives totals from seats, and rejects unexpected seats (`:1215-1260`); neither assigned class assertion is vacuous. Both cases are rc0 cases, so they do not exercise an rc2 setup path; no setup conclusion is drawn from them.
- Fixture pin verification: read-only `jq`/`sha256sum` check returned rc 0. `Completed/completed-after-error.jsonl` pin and SHA-256 both `4f7ff47a37697bb61659f924e6dd00f2f55c51f551a5273254a20fe32ad6abfa`; `CompletedTrailing/completed-trailing-nonmessage.jsonl` pin and SHA-256 both `802b73ee506408042afd99a13091b491e2780f1574b30f0465dd4757734d32be` (`fixtures/seat/expected.json` pins table; files at the fixture paths above).
- The L1 retained after manifest reports both cases `status:"match"`, `ok:true`, empty reasons, `pack_changed:false`, rc 0, `MORI_SEAT_TERMINAL_OK`, and totals `completed:1` with every other class zero (`evidence/seat-after/run-manifest.json:1`). Retained seat rows identify the expected stem and `class:"completed"` (`evidence/seat-after/runs/completed_after_mid_session_error.stdout:1`, `.../completed_trailing_nonmessage_records.stdout:1`). Both retained stderr files are 0 bytes. The before manifest records both as `capability_absent`, not as green (`evidence/seat-before/run-manifest.json:1`).

### Required read-only manifest count

Command (jq over the two retained manifests; no tool execution):

```sh
jq -s '{per_case: [.[] | [.cases[] | select(.id=="completed_after_mid_session_error" or .id=="completed_trailing_nonmessage_records") | {id, status, ok, reasons, pack_changed, observed: {rc: .observed.rc, finding_id: .observed.finding_id, totals: .observed.totals}}]], unmet_before: ([.[0].cases[] | select(.id=="completed_after_mid_session_error" or .id=="completed_trailing_nonmessage_records") | select(.status != "match")] | length), unmet_after: ([.[1].cases[] | select(.id=="completed_after_mid_session_error" or .id=="completed_trailing_nonmessage_records") | select(.status != "match")] | length)}' /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-before/run-manifest.json /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-after/run-manifest.json
```

Observed rc: **0**. Output: `unmet_before: 2`, `unmet_after: 0`; before both cases are `capability_absent` with null observations; after both are `match`, `ok:true`, no reasons, unchanged packs, rc 0 / `MORI_SEAT_TERMINAL_OK`, totals `{aborted:0, completed:1, dead_error_other:0, dead_quota:0, dead_rate_limit:0, error_unsettled:0, incomplete:0, unavailable:0}`.

## Residual risk and verification gaps

- The new A2 metadata assertion shapes are not defined by these case entries or supported by the current gate, so no independent values for them can be asserted from the retained L1 `match` result.
- The assigned cases do not test setup (`rc2`) behavior.
- LSP device unavailable: `read xd://lsp` returned `No such tool` and listed only mounted REA/AST/debug devices. Grep was used only to locate literal symbols; findings above are grounded in source reads and line-level control flow, not grep output. No runtime checks, tests, or selftests were run.
- No tools were installed or updated.
