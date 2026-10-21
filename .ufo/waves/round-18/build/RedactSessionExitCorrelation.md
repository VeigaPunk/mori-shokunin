# RedactSessionExitCorrelation — round-18 redaction draft for SessionExitCorrelation.md

Seat: `MoriR18Recovery.RedactSessionExitCorrelation` (leaf; no subagent dispatch; no VCS mutation; no file written except this report).

## Behavior

Read the round-17 original of `.ufo/waves/round-17/build/SessionExitCorrelation.md` at 29b0dc7 (read-only `git show`), the spot-check routing at `corpus/lessons/round-17-verifier-spotcheck.md:322-350` and `:388-397`, and the frozen C1 policy `.ufo/waves/round-18/frozen/c1-policy.json`. Drafted a minimized replacement body (below, under `## Replacement`). It keeps the seat identity, task, verdict-level conclusions, non-private counts, the INFERENCE label, and a provenance line. It withholds all private values. The lane file itself was not written; the L1 integrates.

## Gates

- Provenance: original blob `61578ee9ad2204e8c4d5c93e778668bc9e583aee` (`git rev-parse 29b0dc7:.ufo/waves/round-17/build/SessionExitCorrelation.md`); SHA-256 of blob content `437b902fbc1c74174e06549a107e2dfbab315d8bca0dcfc55dde36175a57a7bf` (`git show ... | sha256sum`, rc 0).
- Scan of the original blob against every C1 class (python `re`, per-line, UTF-8 decode with errors=replace; counts only, no matched text printed):
  - R1 session_identity: 1 line
  - R2 session_store_path: 1 line
  - R3 tool_output_artifact: 0
  - R4 private_document: 0
  - R5 shell_history: 0
  - R6 privileged_config: 0
  - R7 operator_config_ref: 0
  - R8 routing_table_key: 0
  - R9 session_record_value: 3 lines
- Scan of the draft replacement body against every class (python `re` on the exact body text, same method): **R1 0, R2 0, R3 0, R4 0, R5 0, R6 0, R7 0, R8 0, R9 0; total 0.**
- Post-write scan of this report file: see `## Self-scan` below.
- The draft contains no session directory names, no numbered tool-log names, no document references, no history references, no privileged-config reference, no config line numbers, and no model routing or provider values.

## Touched surfaces

- Written: this report only, `.ufo/waves/round-18/build/RedactSessionExitCorrelation.md`.
- Read: lane file at 29b0dc7 (via `git show`); lesson lines `corpus/lessons/round-17-verifier-spotcheck.md:322-350` and `:388-397`; `.ufo/waves/round-18/frozen/c1-policy.json`.
- Not touched: lane checkout, MANIFEST, `.ufo/state`, sibling lanes, OMP configuration, any session store, any clone.

## Findings

- The original retains: a session-directory identity (R1 hit), a session-store path (R2 hit), and three lines of non-allowlisted custom-record field values (R9 hits). The lesson's routing (`:339-346`) matches what the scan shows for this file.
- The replacement carries the same verdict-level answers as the original: 168/168 error-terminal seats carry a disposal marker; 75 of 2197 completed seats lack one (all open or in flight); `aborted` 80/80 carry a marker; `incomplete` 5/64 carry one. Also retained: the 4 resume files, multi-marker counts, drift counts, tail-window caveat count, the advisory reading, and the INFERENCE label on `dead_*` irreversibility.
- Withheld from the replacement (private or non-allowlisted): session-directory name and path; per-file names and record indices; lane names (replaced by a lane count); per-provider and per-model breakdown (omitted); error-text prefix (replaced by a class count); error-code digits (replaced by presence counts); the verbatim question (paraphrased); the constant values of the disposal-detail fields (withheld by name-free description).
- The replacement reports only counts that the original already reported as counts; no new claims were added.

## Out-of-scope / residual risk (not decided here)

- R-class regexes are a recall floor, not a privacy proof (c1-policy `known_limit`). The reading sweep of the replacement found no further private context, but that is a reading, not a proof.
- Already-pushed history still carries the original; exposure assessment and any history action belong to the operator/kagi. This draft does not rewrite history or authorize rotation.
- Other must-redact files (`PacmanActorTrace.md`, `OmpRetryConfig.md`) and the lesson file are out of this seat's assignment.

## Commands run (all read-only)

- `git -C <lane> show 29b0dc7:.ufo/waves/round-17/build/SessionExitCorrelation.md | cat -n` — rc 0
- `git -C <lane> rev-parse 29b0dc7:.ufo/waves/round-17/build/SessionExitCorrelation.md` — rc 0; output `61578ee9ad2204e8c4d5c93e778668bc9e583aee`
- `git show ... | sha256sum` — rc 0; `437b902fbc1c74174e06549a107e2dfbab315d8bca0dcfc55dde36175a57a7bf`
- `cat .ufo/waves/round-18/frozen/c1-policy.json` — rc 0
- `read` of `corpus/lessons/round-17-verifier-spotcheck.md:322-350` and `:388-397`
- In-process python: loaded the frozen class regexes and scanned the original blob and the draft body per line; counts above. No file written, no scratch, nothing under /tmp.

Tool installs/upgrades: none. No pacman, no journal query, no VCS mutation.

## Replacement

Draft body removed from this report in round 18 (second pass): it is integrated, and further minimized, at `.ufo/waves/round-17/build/SessionExitCorrelation.md`; the draft as delivered remains in commit `b8f5c6c` history only.

## Self-scan

Python `re`, per line, all nine frozen C1 classes, run on this file after the write: R1 0, R2 0, R3 0, R4 0, R5 0, R6 0, R7 0, R8 0, R9 0; total 0. The embedded replacement body is byte-identical to the scanned draft (7983 bytes, sha256 fcacbcc60ad8b4c8c30c074b1005d6993d653a9c9d8d0ca941028fc69daf6765).
