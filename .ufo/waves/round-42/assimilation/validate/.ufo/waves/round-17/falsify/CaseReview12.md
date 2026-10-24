# CaseReview12 — C1 unavailable cases

## Verdict

**Specific falsifier: low-severity oracle gap.** The two cases have nonzero, exact `unavailable` class assertions and their retained L1 outputs match those assertions. However, neither expected case pins the per-seat `reason`, so they do not reliably distinguish the targeted `no-message` and `unreadable` classifier branches. A wrong unavailable reason can still be a green case.

## Case evidence

- The expected rows independently specify `rc=0`, `MORI_SEAT_TERMINAL_OK`, every class total, and the named seat classes (`fixtures/seat/expected.json:641-662,666-692`). These are source-supported: the contract classifies records only when `type == "message"` and says no parseable message or unreadable input is unavailable; assistant `stopReason == "stop"` is completed (`contract.md:45-58`). A1 retains the schema/metadata additions and fixes `finding_id` and pinned `--now-ms` (`contract.md:111-120`). The expected file also pins the input bytes independently of tool output (`expected.json:82-84`; gate pin validation `tools/mori-round17-seat-regressions.py:35-43`).
- `UnavailableNonMessage/non-message-only.jsonl:1-3` has a v3 header followed only by non-message records; the custom record contains a message-shaped payload, making it a real negative control for the record-type guard. `_message_view` rejects non-`message` types (`tools/mori-seat-terminal.py:207-213`), and `_analyze` maps no selected message to unavailable/no-message (`:392-405`). The L1 after stdout records `unavailable`, `reason: no-message`, and unavailable=1 (`evidence/seat-after/runs/unavailable_non_message_records_only.stdout:1`).
- The unreadable case has `locked.jsonl` pinned to the empty-file SHA-256 (`expected.json:83`) and explicitly lists it for the sandbox-only unreadable setup (`expected.json:690-692`); the gate chmods that copied path to mode 000 (`tools/mori-round17-seat-regressions.py:886-910`). `open.jsonl:1-2` is a real completed control. L1 after stdout records `locked` as unavailable/reason `unreadable` and `open` as completed (`evidence/seat-after/runs/unavailable_unreadable_file.stdout:1`). Thus the retained observations match all fields currently asserted; the current unreadable setup was not skipped or setup-failed.
- The retained before manifest records `capability_absent` for these cases, while the after manifest records `status: match`, `ok: true`, and no reasons (`evidence/seat-before/run-manifest.json:1`; `evidence/seat-after/run-manifest.json:1`). The L1 aggregate is rc 0 and reports 54/54 cases matched (`evidence/c1-after.json:19-24`). I did not run the tool, gate, or selftest.

## Static counterexample (oracle gap)

The gate's accepted `want` shape has only `rc`, `finding_id`, `totals`, and `seats`; its seat comparison compares the expected class, not the observed reason (`tools/mori-round17-seat-regressions.py:213-216,1215-1260`). It validates a reason only against the set `{schema,no-message,unreadable}` (`:1087-1089`). Therefore a result with `locked` still classed `unavailable` but reason `schema` would pass this case. This is not hypothetical input ambiguity: the pinned `locked.jsonl` is empty (`expected.json:83`); if a mode-000 file is readable to the scanner, `_read_head` returns empty bytes, `_header_ok` fails, and `_analyze` returns `unavailable/schema` (`tools/mori-seat-terminal.py:276-316,392-405`). Totals, seat class, and rc stay exactly as expected. Likewise, the non-message case would accept `schema` instead of its actual `no-message` reason. The present L1 output has the right reasons, but the regression oracle does not assert them. This is a branch-coverage false-green, not evidence of a current runtime misclassification.

The class/setup assertions themselves are not vacuous: both cases require unavailable=1 and exact seat names/classes; the non-message fixture challenges type filtering, and the unreadable case has a live completed control plus a copied mode-000 target. The missing discriminator is specifically the reason field.

## Count and verification gaps

Read-only count command:

`jq '[.cases[] | select(.id == "unavailable_non_message_records_only" or .id == "unavailable_unreadable_file")] | length' /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/fixtures/seat/expected.json`

Observed rc=0; stdout=`2`.

LSP was unavailable: `read xd://lsp` returned “No such tool: xd://lsp”. I used bounded source reads and literal grep fallback only; grep is not semantic proof. No tests, selftests, tool execution, or gate execution were run by this review.

Process disclosure: my initial raw read of `UnavailableNonMessage/non-message-only.jsonl` also returned its sensitive-record line, contrary to `wave1-context.txt:9`. I do not reproduce or retain any value here; exclude that raw read output from review evidence.