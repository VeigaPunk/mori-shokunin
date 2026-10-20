# CaseReview27 — C1 malformed/FIFO falsification

**Verdict: scoped pass; no actionable falsifier found** for `malformed_lines_skipped` and `fifo_skipped`. This is not a blanket C1 closure.

## Axes checked

1. Expected result is independent of the implementation and supported by the contract.
2. The malformed-byte and FIFO controls are meaningful inputs, not empty/setup cases.
3. Gate comparison rejects wrong class, totals, finding/rc, missing/unexpected seats, or scan-count mismatches.
4. Retained L1 before/after evidence identifies what was actually observed.

## Static evidence

- The contract requires malformed/undecodable lines to be skipped without a crash and discovery to admit only regular files (no FIFOs): `contract.md:44-46,116`. It defines these as synthetic fixtures and the `want` table as separate inputs: `contract.md:77-86`.
- The two expected rows are explicit, fixed at `--now-ms 1761000000000`, and assert `rc:0`, `MORI_SEAT_TERMINAL_OK`, all eight class totals (`completed:1`, every other class zero), and exactly the named completed seat: `fixtures/seat/expected.json:1414-1464`. Their source bytes are separately pinned there: `FifoSkip/real.jsonl` SHA-256 `76e28a1b6fd4176dc68361f99990b165db2615ca520bd697fbd7626cb797b722` (line 20); `MalformedLineSkip/malformed-then-completed.jsonl` SHA-256 `8eab5db35ed7fa95c8eb6740d88a778fa518c90b823d5bb6f1f6bd17b10df7e5` (line 27). The current tool, gate, and expected-table hashes match the pins in `PINNED_INPUTS.json:8-13`.
- The malformed fixture's raw bytes contain a valid v3 header, malformed JSON/shape records and a non-UTF-8 line, followed by a valid assistant `stop` message (189 bytes). The classifier skips JSON/UTF-8 parse failures and keeps the last parseable message: `tools/mori-seat-terminal.py:354-365`; the v3 header is also valid under `:302-316`. Thus `completed:1` is supported by the input and the contract, not by a setup/empty transcript.
- `FifoSkip` has a regular `real.jsonl` positive control with a valid v3 header and assistant `stop` message (`fixtures/seat/FifoSkip/real.jsonl:1-2`); the source pack listing contains that file only. `pipe.jsonl` is declared separately in the expected row (`expected.json:1439-1443`). The gate rejects a FIFO metadata path that already exists in the source pack (`tools/mori-round17-seat-regressions.py:556-592`), creates the FIFO with `os.mkfifo` in the isolated per-case sandbox (`:886-932`), and calls sandbox materialization before launching the tool (`:1711-1739`). The classifier lstat-filters non-regular paths before analysis (`tools/mori-seat-terminal.py:420-433`). This makes the FIFO control real by construction, with the regular `real.jsonl` as a non-vacuous positive control.
- Gate assertions are not vacuous: rc 0/1 cases require totals and seats and validate their internal counts (`tools/mori-round17-seat-regressions.py:639-679`); `evaluate` enforces rc/finding/schema and validates totals/seats (`:1263-1448`); `compare_want` checks expected class totals, seat class, missing seats, and unexpected seats (`:1215-1260`). Scan-count validation also requires scanned/output-seat counts to equal the fixture regular-file count when not prefix-filtered/unreadable (`:1428-1439`). Both cases have a positive expected class and one scanned regular input.

## Retained L1 results

- **Before:** both target rows are `capability_absent` with `observed:null`, `sandbox:null`, and unchanged input-pack hashes in `evidence/seat-before/run-manifest.json:1`. The retained before summary says the tool path was absent and all 54 cases were recorded absent (`:1`); this is a capability baseline, not a case-behavior observation or a false clean.
- **After:** both rows are `status:"match"`, `ok:true`, `reasons:[]`, with unchanged pack hashes and empty stderr in `evidence/seat-after/run-manifest.json:1`. That manifest records rc 0 for each case; retained stdout at `evidence/seat-after/runs/malformed_lines_skipped.stdout:1` and `.../fifo_skipped.stdout:1` shows the OK finding, one scanned file, one completed seat, totals completed 1 / all other classes 0, and the expected seat key. The run manifest records `fifo_files:["pipe.jsonl"]` for the FIFO case.
- Read-only count required for these two case IDs:
  ```sh
  jq -s '[.[] | [.cases[] | select(.id == "malformed_lines_skipped" or .id == "fifo_skipped")] | length]' \
    /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-before/run-manifest.json \
    /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-after/run-manifest.json
  ```
  **rc=0; stdout:** `[2, 2]` (before, after).
- Hash command: `sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-seat-terminal.py /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-round17-seat-regressions.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/fixtures/seat/expected.json` (**rc=0**). Output, in command order: `5819c3c06e4ceded02b043ef1edbe15043359f176f1b24830b4d3cae24adbdba`, `21285c2b7000bf63cd9fd679f4b88a7d5d4ff250eee0279576d6d0dcb3b97f7a`, `b684c63bf3cebe70f24d3d02f3f0df4f63aad3f547a365a3ca1864f5f57cb01f`; all equal `PINNED_INPUTS.json:8-13`.

## Residual risk and verification gaps

The retained `seat-after/cases/fifo_skipped` and `.../malformed_lines_skipped` directories are empty now, so the post-run sandbox inode/bytes are not independently inspectable from the retained tree. The FIFO's runtime presence is therefore supported by the recorded metadata/result plus the deterministic gate call path, not a retained inode snapshot. No tool or selftest was run. LSP is unavailable in this environment: `read xd://lsp` returned `No such tool`; grep was used only to locate case entries, not as semantic proof. No installs or updates were made.

Report: .ufo/waves/round-17/falsify/CaseReview27.md
