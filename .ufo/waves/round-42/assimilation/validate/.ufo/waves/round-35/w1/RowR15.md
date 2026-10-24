measured 2026-10-23T08:51:50Z

# Round 15 capability row

Axes: capability behavior and coverage; calibration/evidence traceability; fixture/live scope.

ROW: | rounds[345].capabilities_added[0] | Partial positive journal alarms | On finite committed fixtures, retains individually qualified current-boot OOM and user-signal alarms beside invalid aggregate records while keeping raw totals unavailable; no live positive-load evidence is claimed. | `tools/mori-round15-regressions.py` | 15 |
VERDICT: supported — the closure records the finite-fixture gate execution and observed OOM and user-signal witnesses while their raw arms remain unavailable.

Citations:
- MANIFEST `rounds[345]` records the exact capability string, report path, and verification spot-check. Command: `git -C /home/vgpnk/Projects/shokunin show 37b51a243302e8009c7067431e8a47f9a722fd14:MANIFEST.json | jq -c '.rounds[345] | {capabilities_added,report,verification}'` → capability string and report `.ufo/reports/round-15/mori.md`; verification names `mori-shokunin/corpus/lessons/round-15-verifier-spotcheck.md@b83edc6ee3db6822382ab673d7e6e984e420f22f`.
- The closure report says the implementation uses strict scalar identity/current-boot selectors and names the regression gate at `.ufo/reports/round-15/mori.md:9-10`; it records the commands and outcomes at `.ufo/reports/round-15/mori.md:37-49`.
- The closure spot-check records the OOM positive beside an unavailable aggregate and the signal positive with the unavailable raw arm retained at `corpus/lessons/round-15-verifier-spotcheck.md:118-120`; finite paired-query evidence and its bound are at `:121-127`; no live positive-load claim is at `:167-168`.
- The selected gate describes its fixture assertions for alarms and unavailable raw counts at `tools/mori-round15-regressions.py:17-43`.

Evidence rationale: `tools/mori-round15-regressions.py` is the best pointer because the closure report names it as the landed gate and records its before/after execution and fixture results (`.ufo/reports/round-15/mori.md:10,37-49`).

# Provenance and checks

- Inspected the frozen MANIFEST entry at fleet revision `37b51a243302e8009c7067431e8a47f9a722fd14`, the round-15 spot-check and candidate gate at lane revision `b83edc6ee3db6822382ab673d7e6e984e420f22f`, and the fleet report at the MANIFEST revision.
- Strong-path checks passed for `tools/mori-round15-regressions.py`: `git cat-file -e` succeeded at both the closure commit and lane `HEAD`; `git diff --name-status 0fa5e0de194bcc270a927a166664113e6821442b b83edc6ee3db6822382ab673d7e6e984e420f22f -- tools/mori-round15-regressions.py` returned `A`; the path is under `tools/` and appears in the closure report at lines 10, 37, and 39. The capability string names no specific tools/ or corpus/knowledge/ path.
- The closure report records exit 1 before and exit 0 after, 34→0 behavioral fixture failures, and 63/63 green cases at `.ufo/reports/round-15/mori.md:37-49`. These are reported closure executions, not checks rerun by this seat.
- Commands run for this finding: `timeout 5 date -u +%FT%TZ` → `2026-10-23T08:51:50Z`; read-only `git show`, `git diff --name-status`, `git rev-parse`, and `git cat-file -e` commands against the specified revisions. `git rev-parse HEAD` → `913df22e29f131ef9cb5de9dcb7e3e272256c5f0`.

# Limits and touched surfaces

- Scope is the reported finite committed fixture behavior only. The closure disclaims live positive-load evidence, universal event coverage, authenticated emitters, and victim counts at `corpus/lessons/round-15-verifier-spotcheck.md:167-168`.
- This seat did not run the regression gate, the round-35 `count-c1.py` counter, or a live journal query. No tools were installed or updated.
- Only this scoped report was written: `.ufo/waves/round-35/w1/RowR15.md`; no product code or other lane files were changed.
