# RedactPacmanActorTrace — round-18 C1 minimization draft

Seat: MoriR18Recovery.RedactPacmanActorTrace (leaf, no dispatch). Draft only: the target file was **not** written; L1 integrates.
Target: `.ufo/waves/round-17/build/PacmanActorTrace.md` (committed at 29b0dc7, 157 lines).
Result: replacement body below; scan of the replacement against all nine C1 classes in `.ufo/waves/round-18/frozen/c1-policy.json` returns zero hits (see Scan).

## Method

- Read the committed blob at 29b0dc7 for classification only. No excerpt, path, session name, numbered artifact name or value from it is copied here.
- C1 classification of the original (line numbers only, class from the frozen policy):
  - R1 session identity: lines 32, 34, 66
  - R2 session-store path: lines 31, 66
  - R3 numbered tool-output artifact: lines 36, 45, 47, 48, 90, 144, 145
  - R4 private document: line 53
  - R5 shell-record file: lines 95, 146, 147
  - R6 privileged configuration: lines 103, 152
  - R7, R8, R9: zero hits
- Removed by category (not by content):
  - 30-56: other-session tool-output excerpts, a session identity, planned command text from an operator-owned file, and the 09:15 transaction-to-session mapping that rested on a numbered artifact name.
  - 74-76: heads of other tool outputs (quoted content).
  - 95-103: shell-record contents and a privileged-configuration reference.
  - 131-155: commands-table rows that named the removed stores or artifacts. Rows restated as scoped results with rc preserved.
- Kept: seat identity and task, verdict (09:15 exact; 13:23 yay, user, inference-level actor), transaction records from the system log, counts that are not private values, lane-relative report citations, INFERENCE 1-4, and the unresolved gaps.
- Provenance line in the replacement names the original blob id and SHA-256 so the committed history stays the record.
- No public-source citations exist in the original; the replacement keeps "No URLs consulted."

## Replacement

Draft body removed from this report in round 18 (second pass): it is integrated, and further minimized, at `.ufo/waves/round-17/build/PacmanActorTrace.md`; the draft as delivered remains in commit `b8f5c6c` history only.

## Scan

Method: python `re` run at runtime against `.ufo/waves/round-18/frozen/c1-policy.json` classes R1-R9 (`re.compile(regex).search` per line, lines split on `\n`), over (a) the replacement block only (90 lines, 8572 bytes, sha256 `6796428d34fba3629d9766d866e7ced9540c94230764a66785d5e7eb0b79e93b`) and (b) the full draft file.

## Scan results

- Replacement: R1 0, R2 0, R3 0, R4 0, R5 0, R6 0, R7 0, R8 0, R9 0. Total hits 0. The metric's routed sub-count is 0 for this draft; the replacement carries no allowlist entry.
- Full draft (this report): R1-R9 all 0. Note: `.log` substrings appear in the replacement only as system-log names (pacman.log, snapper log, wtmp, the `/var/log` directory); none matches R3, which requires a numbered tool-output name.
- Category words checked in the replacement with case-insensitive substring match, all 0 hits: session director*, numbered, Documents, document, history, sudo, config.yml, config line, model, fallback, routing, bash_history, .omp.

## Tools installed or upgraded

None. No package-manager transaction; no pacman, yay or paru invocation.

## Artifacts

- This report: `.ufo/waves/round-18/build/RedactPacmanActorTrace.md`.
- No other file written. Target file not written (L1 integrates).
- Routed: exposure assessment for already-pushed history remains with the operator per the round-17 closure; this draft does not authorize rotation, deletion or history rewriting.
