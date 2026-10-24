# PackAnchorValidation — round-16 wave1 report

Seat: MoriR16.PackAnchorValidation (executor, leaf)
Owned file: `.ufo/waves/round-16/fixtures/AnchorValidation.json` — written, 4 cases.
No other file touched. No tool/harness/production code executed; no runs of any kind.

## Cases

| id | arm | want_rc | want_id | want fields |
|---|---|---|---|---|
| ANCHORVAL_SCOPE_MISMATCH_SYSTEM_ANCHOR_USER_QUERY | `--scope user` vs anchor.scope `system`; capture is otherwise valid and contains a `fe6faa94` kernel-oom positive | 2 | MORI_JOURNAL_WINDOW_SETUP | `{}` (rc+id only) |
| ANCHORVAL_BOOT_ID_UPPERCASE_REJECTED | anchor.boot_id = 32 UPPERCASE hex (contract requires lowercase); capture valid + `98e32220` sigkill positive | 2 | MORI_JOURNAL_WINDOW_SETUP | `{}` |
| ANCHORVAL_BOOT_ID_SHORT_REJECTED | anchor.boot_id = 16 lowercase hex chars (length defect, charset clean) | 2 | MORI_JOURNAL_WINDOW_SETUP | `{}` |
| ANCHORVAL_VALID_NEGATIVE_CONTROL | valid anchor + anchor record + one benign non-catalog record (fabricated `aaaaaaaa…a3` MESSAGE_ID, not in census catalog) | 0 | MORI_JOURNAL_WINDOW_OK | scope=user, records_after_anchor=1, all four positive_*=0 |

All anchor objects are schema `mori-journal-anchor-v1` with printable scalar cursors <4096. All case `stdout` is literal JSONL; `stderr` empty; `returncode` 0. First record in each stream exactly matches its anchor cursor+boot so the stream itself is sound — refusal cases isolate anchor-file validation.

## Design decisions (advisory, sent to agent://MoriR16.WindowHarness)

- **SETUP vs UNAVAILABLE.** Contract maps "setup invalid anchor/args -> rc2 MORI_JOURNAL_WINDOW_SETUP" and UNAVAILABLE to capture/continuity failures. Scope mismatch and malformed `boot_id` are anchor-schema validation failures known before journalctl runs, so all three refusal cases pin SETUP. Refusal cases ship a valid-looking capture containing a catalog positive on purpose: any tool or wrapper that trusts the capture instead of refusing produces observable false-positive output and fails the gate.
- **"want": {}** on refusal cases = no output-field assertions beyond rc+finding_id; reason strings were not pinned because the contract names the field but no exact stable vocabulary exists yet.
- **Catalog ids verified against source bytes** `tools/mori-census.sh:1032-1036`: kernel_oom `fe6faa94e7774663a0da52717891d8ef`, unit_sigkill `98e322203f7a4ed290d09fe03c09fe15`, unit_failure `d9b373ed55a64feb8242e02dbe79a49c`, oomd `d989611b15e44c9dbf31e3c81256e4ed`, coredump `fc2e22bc6ee647b6b90729ab34a250b1`. Dispatch-hint `d9b373ed55a64e6c8e2e7d70a0fce472` does NOT appear in the census; census bytes are authority per assignment.

## Coverage boundary (deliberate, owned by siblings)

Record-level `_BOOT_ID` mismatch / foreign boot → PackBootBoundary. Missing/different first cursor → PackMissingAnchor. Non-scalar record cursors → PackCursorShape. Malformed JSON in stream → PackMalformedCapture.

## Risks / blockers

- No blocker. If WindowHarness or WindowTool rules anchor-validation refusals under `MORI_JOURNAL_WINDOW_UNAVAILABLE` instead of `MORI_JOURNAL_WINDOW_SETUP`, the three refusal cases' `want_id` must flip — schema coordination message sent to WindowHarness before pinning.
- Pack assumes `"want": {}` is accepted (or `want` optional). If the shared schema demands `want` be non-empty on refusal cases, a follow-up key choice is needed; not a current blocker.

## Tooling

No installs or updates performed (pacman paused host-wide; nothing needed).

## Process disclosure (per L1 round-16 no-checks clarification)

- No live journalctl query, no measurement/probe loop, no background job, no test/gate/build/smoke/formatter was run.
- Only subprocess use: `python3 -c "json.load(...)"` to statically parse `wave1-spec.json` / `wave1-dispatch.json` task text and to confirm my own pack parses with 4 cases — static file review, not execution of the production tool or harness.
- One `agent://MoriR16.WindowHarness` schema-coordination message sent (contract-permitted coordination, not an outside-lane write).
- All other activity was `read`/`grep`/`ls`/`find` on repo files; no /tmp deliberate output, no agent.db or credential reads.

Report: .ufo/waves/round-16/build/PackAnchorValidation.md
