# DraftSettlementNote — report

Seat: MoriR20.DraftSettlementNote (scribe, leaf). No subagents spawned. No installs or updates performed. No builds, tests or census runs. Nothing in the fleet repo, sibling lanes, `.ufo/state/*`, watchdog log, lane jj/git state, `tools/mori-census.sh` or any committed baseline was edited.

## Deliverable

Draft: `.ufo/waves/round-20/build/DraftSettlementNote/wave-settlement-r20.md` (C2 knowledge note; final numbers marked `TODO-L1`).

Sections: what `scan` measures; member statuses; wave states with precedence; exit codes; why missing is not dead and why present is not complete; misrooted detection; undispatched-file caveat; FR3 boundary with kumitate; oracle map (14 cases); limits.

## Findings (with evidence)

1. **The tool does not exist yet.** `tools/mori-wave-settlement.py` is absent in the lane tree (`ls` → no such file). Every tool-behaviour statement in the draft is the frozen contract (`.ufo/waves/round-20/contract.md:49-104`), labelled as such.

2. **Missing is not dead; the round-19 closure already says so.** `MANIFEST.json:10171` (fleet root): W1 = 64 returned IDs, 16 reports, 8 known provider failures, 1 cancellation, 39 unknown no-report causes "(not successful reviews/deaths inferred)". 8+1+39 = 48.

3. **Round-19 W1 reproduced by manual shell (not the tool).** `.ufo/waves/round-19/wave1-run.json`: `counts.total` 64, 64 tasks, every trailer `Report: write your scoped findings to .ufo/waves/round-19/build/<Name>.md`. Same rule as the contract: present 16, empty 0, missing 48, misroot candidates 0, start-stub-only 0. Matches the MANIFEST figures.

4. **Present ≠ complete (design gap for L1).** Contract `present` = size > 0. Round-20 `wave1-run.json` (76 members, all trailers under `.ufo/waves/round-20/build/`): at observation 76 non-empty files, of which 57 are ≤32 bytes beginning `STATUS: started` (first-tool-call stub). Under the frozen rule those 57 count as present. Decision for L1: keep size-only and say so, or add a started sub-status. Not changed in the draft; flagged `TODO-L1`.

5. **Undispatched-file caveat.** `wave1-run.json` registry `agentId` is `null` for all 76 members (jq). Dispatch evidence lives in `wave1-dispatch-receipt.json` (single task call, `taskcall_sha256`, 76 returned IDs), not in the dispatch file. An unsent dispatch and a silent wave look identical to `scan` (`missing` → `unsettled`). Pair scan output with the receipt or with the round-18 dispatch ledger (`corpus/knowledge/dispatch-ledger-r18.md`, which itself states it cannot prove an unlogged attempt never happened).

6. **Two "settled" meanings.** Census `SURFACE waves` (`tools/mori-census.sh:865-931`) calls a dir settled when a settlement-type file exists (results/closeout/mission-result/closeout.md or a closed/settled marker). The new tool's `settled` means every member has a non-empty report. Not comparable; the note keeps them apart. Also: census skips `round-*` children (`tools/mori-census.sh:879`), so round-N wave files are invisible to `SURFACE waves`; the new tool recurses.

7. **Exit-code collision.** Kumitate `ufo-swarm-collect.mjs` (HEAD `31c465f1`): typed error → 1 (`:805`), internal → 1 (`:808`), usage → 64 (`:641`, `:805`). Kumitate `ufo-swarm-wave.mjs`: 0 ok, 1 invalid, 64 usage (`:102`). Mori `scan` (contract): 0 all settled/no-spawn, 1 any other state, 2 usage/unreadable root. In mori, exit 1 is an observation, not a crash. Also exit 0 is compatible with `unreadable_json > 0` (oracle case `malformed-dispatch`).

8. **Misroot precedent.** `tools/mori-misroot-sweep.py` header documents the round-16 `MoriR16.Lesson` written at the fleet root. The `misrooted` status in the contract is a lead, not ownership proof; the fleet root also holds fleet-level `.ufo/waves/*`. Manual check: 0 misroot candidates for round-19 W1 and 0 for round-20 W1.

9. **FR3 boundary.** `corpus/README.md:334`: "Mori reports filesystem shape; kumitate owns orchestration/result semantics; `empty` alone does not prove never-written". Kumitate's settlement is the `collect` join (`unmapped_member` / `unexpected_member`, `ufo-swarm-collect.mjs:549-555`). `ufo-swarm-wave.mjs` contains no `settle` token (grep, empty). The note forbids advising `settle`. C2 advances per-seat filesystem shape only; emptied-by-hygiene vs never-written stays FR3-open (souji receipts, offline).

10. **Citation caveat.** `swarm-wave-lifecycle.md` has a round-35 fidelity notice (24 anchors off at `31c465f1`). Anchors cited from it are secondary; re-checked only the ones marked in the draft.

## Out-of-scope items observed (routed, not absorbed)

- Kumitate `swarm-wave-lifecycle.md` anchor drift (fidelity notice) → kumitate.
- Souji receipts for hygiene-vs-never-written → souji (offline; FR3 stays open).
- `corpus/README.md` FR4 cites a non-existent `../../fleet-ledger/` path (already recorded as F8 in round-16 ReviewCorpus) — pre-existing, not touched.

## TODO-L1 (for integration)

- Tool-run counts: C2 before/after `capability_absent` / `matched` (expect 14 → 0; matched 14); live `scan` on round-19 W1 expected `reports_present = 16` of 64; fleet-wide totals.
- Decide the start-stub `present` question (finding 4) and record it in `frozen/c2-expected.json` before the after-run.
- Confirm the mixed-case precedence in the draft §3 (`unsafe`+`missing` → `unsettled`) against the built tool.
- Re-check kumitate anchors the note relies on, given the fidelity notice.

## Checks not run

No tests, selftests or builds (none assigned). The tool was not executed because it does not exist. The census was not run.
