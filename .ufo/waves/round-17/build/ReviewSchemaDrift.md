# C1 input-schema drift review

**Axes:** input-schema compatibility; truthful terminal classification/coverage; transcript-field privacy.

## Finding — High, contract-level coverage risk

C1 has no admission check for the OMP transcript input version. Its parsing contract says to skip every record other than `type == "message"` with a dict `message` (including other record types), then classify the last matching message using the current `role`, `stopReason`, and error fields (`.ufo/waves/round-17/contract.md:37-50`). The named `mori-seat-terminal-v1` is the output schema, not an input-version policy (`contract.md:57-64`). An unsupported input can therefore be accepted if its messages happen to resemble the expected fields, or be counted as `incomplete`/`unavailable` if field meanings or placement changed; either outcome could still be reported as a completed scan. That consequence is an inference from the specified parser behavior; no C1 implementation was present in the reviewed lane snapshot to demonstrate runtime behavior.

**Observed header:** a privacy-limited projection of the current project session transcript returned `{"line":2,"type":"session","version":3}` (only line number, `type`, and `version` were emitted; no other transcript fields were read or reported). Evidence location: `<session-store path withheld> transcript>:2` (transcript identifier intentionally omitted). The contract does not document version 3, an accepted-version set, or how to handle an absent/malformed header. This observation establishes only the current transcript's header value, not that version 3 is the only valid OMP format.

### Recommendation for C1

1. Define an explicit allowlist of *input transcript* versions, separately from the output `mori-seat-terminal-v1` schema. Admit only versions whose message shapes are deliberately supported; do not treat an arbitrary future integer as compatible. Version 3 is observed in this session, but should be allowlisted only after its expected shape is documented/covered.
2. Before classifying a selected `*.jsonl`, inspect its `type == "session"` header and require a present, well-typed `version` in that allowlist. Because C1 normally reads only a bounded tail (`contract.md:35-38`), obtain the header via a separate bounded first-record read; a large file's header will not be in its tail. Missing/malformed headers and unknown versions must not fall through to terminal classes.
3. On any unsupported selected transcript, fail the scan with **rc 2** and `finding: "MORI_SEAT_TERMINAL_SETUP"`, using a stable reason such as `unsupported-session-version`. Do not label that seat `unavailable`, `incomplete`, or `dead_*`, and do not emit partial seat totals as though coverage were complete. Keep stdout to one JSON document and no message/error text; define a setup-result shape that is unambiguously not a complete census while preserving the output contract's JSON-only rule.
4. Add synthetic fixtures for a known supported header, an unknown future version, and missing/malformed version/header. Assert rc 2, setup finding/reason, and absence of classified-seat/complete-coverage claims; update the fixture/gate schema if needed (`contract.md:71-78`). Never use real session contents as fixtures.

## Review scope and gaps

- At the inspected lane snapshot, `git diff --name-status` returned only `M .gitignore`; `git status --short` also showed untracked `.ufo/waves/round-17/`. The C1 tool and seat-fixture paths were not present in the lane checkout, so implementation, callers, and regression behavior remain unreviewed. These are snapshot observations and may change as integration proceeds.
- LSP was unavailable: `read xd://lsp` returned “No such tool”; consequently no LSP status, references, definition, or diagnostics could be obtained. No text grep was used as a semantic substitute.
- Read-only checks: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --name-status` (rc 0); `git -C /home/vgpnk/Projects/shokunin/mori-shokunin status --short && git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff -- .gitignore` (rc 0); `jq -c 'select(.type == "session") | {line: input_line_number, type, version}' <current project transcript>` (rc 0; output above). No tests or builds were run; no tools were installed.
