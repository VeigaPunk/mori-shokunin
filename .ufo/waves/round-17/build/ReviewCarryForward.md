# Round 16 carry-forward review — C1/C2

## Axes and review scope

Relevant axes are **coverage** (C1), **operability** (C2), and the carried **freshness/calibration** limits. This review checks whether the round-17 interfaces preserve the round-16 qualifications; it does not treat either claim as evidence for the other.

## Findings by severity

### Medium — preservation of the r10 drift red is not yet evidenced

Round-16 item 5 says to keep the r10 drift-pin red without re-pin until reasoned semantic review (`corpus/lessons/round-16-verifier-spotcheck.md:224-226`). The scorecard says the old r10 baseline is preserved without re-pin and its red is not made green by the separate capability (`SCORECARD.md:922-925`); round 16 also records freshness unchanged, old pin retained, no re-pin (`SCORECARD.md:982-984`).

C1 is specified as a standalone seat-transcript terminal-status tool, while C2 edits only the census (`.ufo/waves/round-17/contract.md:22-23, 24-67, 80-95`). C1 has no evident path to the r10 journal/census pin. C2 does: it changes `tools/mori-census.sh`, so branch anchoring could change census output covered by the existing baseline. The C2 contract preserves A/B/C grading semantics but does not state that the old r10 red must remain red or require a post-change `--drift` comparison. **Risk:** accidental pin invalidation or implicit re-baselining could erase the carried red. No delivered C2 source diff or post-change drift result was present at review time, so this is a risk/verification gap, not an observed regression.

### Low — journal-window qualifications remain scope-only, not revalidated

| Carried qualification | Round-16 evidence and required interpretation | C1/C2 impact at this review snapshot |
|---|---|---|
| Cursor alias means false-unavailable, not proof of vacuum/deletion | The lesson rejects byte mismatch as proof of vacuum/deletion because one journal entry may have multiple cursor strings; mismatch supports only `unavailable` (`corpus/lessons/round-16-verifier-spotcheck.md:142-145`). | C1 classifies transcript terminal status and C2 changes census probes; neither interface changes journal cursor handling. Unchanged is supported by scope separation only; no implementation diff was available to verify it. |
| Vacuum/cross-boot remains `[UNKNOWN]` | The vacuum positive-trap and foreign-boot spot cases returned `UNAVAILABLE` (`anchor-not-first-record`, `anchor-boot-mismatch`), not a proven vacuum or a cross-boot event conclusion (`corpus/lessons/round-16-verifier-spotcheck.md:95-103`). The scorecard explicitly scopes the window to the anchor boot, not necessarily the current host boot, and disclaims current-boot, all-entries-to-now, and complete-access claims (`SCORECARD.md:937-940`). | Neither C1 nor C2 is specified to alter the journal-window tool. No new evidence upgrades these unknowns. Preserve the unknown classification; do not present the new claims as resolving them. |
| Fixture evidence is not live-behavior evidence | The 64 finite gate cases are capability requirements, not reproduced production defects (`corpus/lessons/round-16-verifier-spotcheck.md:90-93`); scorecard describes the live read as accessible-surface evidence, not complete retention or universal coverage (`SCORECARD.md:915-920`). | C1's synthetic transcript fixtures and C2's census regressions remain separate evidence domains. Neither makes fixture results live evidence. This separation is compatible with the interfaces, not newly measured. |
| Live captures are anchor-only | The two live scopes had `records_after_anchor=0` and zero positive subsets; the scorecard says this establishes host-path reachability, not absence of events, full-store access, or positive live load (`SCORECARD.md:970-975`). The lesson repeats that limit (`corpus/lessons/round-16-verifier-spotcheck.md:118-119`). | C1 does not consume journal captures; C2's specified branch probes do not add post-anchor journal observations. No new live sample was available. Keep the anchor-only caveat and do not imply no events occurred. |

## Actual-diff and verification boundary

Read-only inspection found no C1/C2 implementation diff to review yet:

- Commands and observations (all exited 0):
  - `git -C /home/vgpnk/Projects/shokunin/mori-shokunin status --short` → ` M .gitignore`, `?? .ufo/waves/round-17/`; `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --name-only 24526ea` → `.gitignore`; `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff 24526ea -- .gitignore` → adds only `.ufo/worktrees/`.
  - `git -C /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/SeatTool status --short && git -C /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/SeatTool diff --name-only 24526ea && git -C /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/SeatTool diff 24526ea -- tools` → no output. `git -C /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/SeatFixtures status --short && git -C /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/SeatFixtures diff --name-only 24526ea` → no paths. Both chains exited 0.
  - `git -C /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/CensusJj status --short && git -C /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/CensusJj diff --name-only 24526ea && git -C /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/CensusJj diff 24526ea -- tools/mori-census.sh` → only `?? .scratch/`; no source changes.
- An LSP documentation/status lookup (`read xd://lsp`) returned “No such tool”; no LSP server was available, so no semantic LSP checks were possible. No selftest or runtime probe was run.

**Conclusion:** the contract-level separation makes the alias, vacuum/cross-boot, fixture/live, and anchor-only qualifications plausibly untouched, but actual C1/C2 preservation is not yet verified because the implementation diff is absent. The r10 pin is the concrete risk: C2 touches the census and must be checked against the existing baseline without re-pinning before claiming the red remains carried. This report is a recommendation, not admission.