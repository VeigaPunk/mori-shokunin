# C1 exit-code and finding-name review

Axes checked: exit-code semantics and compatibility of stable finding identifiers with the lane's output convention.

## Findings

### P2 — C1 contract uses `finding`, unlike the lane's `finding_id` convention

The C1 contract says the terminal-status JSON places `MORI_SEAT_TERMINAL_DEAD` and `MORI_SEAT_TERMINAL_SETUP` in the `finding` key and lists `MORI_SEAT_TERMINAL_OK` / `_DEAD` / `_SETUP` as its values (`.ufo/waves/round-17/contract.md:61-64`). The lane's r16 probe reports `finding_id` instead: `SKILL.md:18,172`; its implementation builds `{"finding_id": ...}` in `_fail` (`tools/mori-journal-window.py:109-116`) and on success (`:492-506`). The identifiers themselves follow the lane's stable `MORI_<surface>_<state>` naming pattern; the field name is the inconsistency.

This is a contract-level interface risk, not a confirmed runtime defect: both the lane `tools/mori-seat-terminal.py` and the C1 clone path `.ufo/worktrees/round-17/SeatTool/tools/mori-seat-terminal.py` were absent when checked, so no delivered output could be compared. Align the C1 output, fixture expectation (`contract.md:73-78`), and regression reader on `finding_id`, or explicitly document and consistently consume a C1-specific `finding` field before delivery.

## Exit-code assessment

The specified mapping is coherent with the lane's general 0/1/2 gate convention: C1 returns 0 for a complete scan with no `dead_*` seats, 1 for a complete scan with one or more `dead_*` seats, and 2 for setup/unavailable-directory failure (`contract.md:61-64`). The census convention is 0 CLEAN, 1 DRIFT, 2 setup/usage (`SKILL.md:159-160`). The journal-window probe is narrower: it uses 0 for OK and 2 for unavailable or setup (`SKILL.md:172`; implementation `_fail` returns 2 at `tools/mori-journal-window.py:109-116`, success returns 0 at `:492-506`). That difference is appropriate for the stated C1 result contract: 1 is a completed positive observation, not a scan error. Per-seat `unavailable` is a tally class, so the contract implies it does not itself force rc2; only a setup/unavailable-directory failure does. The C1 names `_OK`, `_DEAD`, `_SETUP` are surface-scoped and do not collide with the journal probe's `_OK`, `_UNAVAILABLE`, `_SETUP` identifiers.

## Verification gaps and residual risk

- C1 implementation unavailable: `read` reported the lane tool path missing; `glob` of lane `tools/` listed no `mori-seat-terminal.py`; `glob` of the assigned `SeatTool/` clone likewise listed no such file. The focused read-only `git diff` command exited 0 with no output for the requested paths; this does not expose untracked files, hence the directory checks above.
- No C1 selftest or runtime behavior was verified. The wave context says a selftest's existence is not permission to run it and limits runs to the commands named by the assignment (`.ufo/waves/round-17/wave1-context.txt:7`).
- LSP status/references/definition/diagnostics were unavailable: `read xd://lsp` returned “No such tool” and the mounted device list did not include LSP. Literal grep was used only to locate text; semantic comparisons above are based on direct reads of the contract, SKILL, and journal implementation.
- No tooling was installed or updated.
