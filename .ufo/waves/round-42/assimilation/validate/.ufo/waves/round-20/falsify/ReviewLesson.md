VERDICT: BROKEN (table-level). Row verdicts: M1 HOLDS · M2 PARTIAL · M3 PARTIAL · M4 PARTIAL · M5 BROKEN · M6 BROKEN · M7 PARTIAL · M8 BROKEN.
Not every row has a class, a resolving pointer, an accurate captured-by, and a fix shown able to fail. M5, M6 and M8 have fixes that cannot fail at all.
Observed 2026-10-21 about 08:15 -0300. Lane artifacts were still changing during the check (X2).
Bounds: read-only on lane, fleet and sibling lanes; scratch only under falsify/ReviewLesson/ and /tmp/rl. Not opened, listed or grepped: .ufo/interactive-sessions/, .ufo/worktrees/, .jj/. mori-census.sh not run. No installs or updates.

## Rows

M1 survivor / wave settlement: HOLDS (residuals)
- Pointers resolve: round-19/wave1-settlement.json (64 / 16 / 8+1+39); evidence/c2-live-mori.json (r19 W1 partial, present 16, missing 48, n 64); build/CensusWavesSurface.md (section 5: seat reports never counted).
- "MANIFEST round-19 mori closure notes" is unqualified. It is fleet MANIFEST.json rounds[398].notes, same numbers. Its strings contain no "hand", "found", "recover" or "manual" (jq search, empty). "By hand" rests only on wave1-settlement.json being hand-written (DraftProvince.md:20) [INFERENCE].
- Fail reproduced: `tools/mori-wave-settlement.py scan --lane-root <lane> --out /tmp/rl/scan-lane.json` gives rc 1; round-19/wave1-run.json = partial, present 16, missing 48, n 64. rc 1 is lane-wide, not W1-specific.
- Residual: QUALITY 64 also requires a committed receipt and a failure on a missing receipt. The tool does neither; receipts carry no tool SHA.

M2 carried-red / freshness: PARTIAL
- Reproduced: `check-register.py .ufo/waves/round-13/evidence/drift-classification.json .ufo/waves/round-20/evidence/c1-drift-entering.json` gives `unclassified=50 invalid=43 regression=0 tokens=50`, rc 1 (matches build/RegisterCheck.md). Live register gives rc 0.
- Counting command is locale-dependent. Contract line 39 sorts the drift side without LC_ALL=C. Under ambient en_US.UTF-8 it prints 37 (r13) and 33 (r20), with comm "not in sorted order". 8 and 0 reproduce only with LC_ALL=C on both sorts.
- Gap: check-register.py:76-77 checks only non-blank evidence. A mutant with `"evidence": "nonexistent/zzz-path.md:1"` gives rc 0. QUALITY 9 requires pointers to resolve.
- Gap: class correctness is unchecked. Flipping WATCHDOG_STALE to census-regression gives rc 1. The label is the one decision the gate cannot check (C1Critic, "Why the count is not an independent check").
- Register pointers `watchdog.log:402,582-585` and `scripts/hyaku/inline.sh:103` resolve only from the fleet root; ABSENT under the lane root.

M3 vacuous count: PARTIAL
- "18 markers at ~10:40Z": supported by build/ContractReview.md section 3 (18 exact-marker files at 10:40:40Z). build/DraftSettlementNote.md has no 18: its finding 4 says 57 files, <=32 bytes beginning `STATUS: started`, time unstated. The row cites both.
- "frozen cases had no marker case": `grep -c 'started\|marker\|stub' frozen/c2-expected.json` gives 0 (true). That is a reason, not a capturer; the capturers are ContractReview section 3 and DraftSettlementNote finding 4.
- "6 stubs at 10:46Z": evidence/c2-live-mori.json, r20 build stub=6, mtime 10:46:42Z (true).
- Fail reproduced: R2 branch cut in a scratch copy gives lane selftest `FAIL (22 cases, 21 passed, 1 failed)`. The repaired independent oracle on the same mutant gives matched 14, mismatched 0. R2 is guarded only by the self-authored selftest.
- R2 is at HEAD (tools/mori-wave-settlement.py:226-228). Working tree adds 10+/2- (16-byte bound, R6, R7). Receipts record no tool SHA.

M4 oracle fixture defect: PARTIAL
- Reproduced: evidence/c2-after-oracle-v0-fixture-defect.json gives matched 13, mismatched 1 (no-spawn: exit 0 to 1, state no-spawn to unavailable). The v0 payload is `{"context":"c","tasks":null}` (c2-oracle-v0.py:33, 138-139); the row abbreviates it.
- Captured-by "tool selftest 14/14" is wrong. The selftest prints `MORI_WAVE_SETTLEMENT_SELFTEST: PASS (22 cases, 22 passed, 0 failed)`: 14 frozen plus 8 refinements. No 14/14 is printed.
- Repaired harness (c2-oracle.py:33-35, marked "L1 repair") gives 14/14 on the lane tool. It catches a planted frozen-case defect (empty to present gives 13/14 on empty-report), so its fail-capability is real but bounded to the 14 frozen cases; it is blind to R2 removal (M3). The integrator edited the harness the contract calls independent; the row should say so.

M5 number / reference drift: BROKEN
- Holds: contract.md:12-13 "nine census revisions"; `git log 5be89432ab..2061780117e6 -- tools/mori-census.sh` gives 7 commits; 5be89432ab's census blob sha256 = d7710981aa..., the r10 census_sha256 header. The seven-commit count is right.
- Misquote: contract.md:53-54 reads "(MANIFEST round-19 closure notes)"; the row drops "round-19".
- The erratum adds "counted by hand ... per wave1-settlement.json". That JSON has no method statement (see M1).
- Fix is prose ("erratum here"); nothing can fail. Captured-by "none" is wrong: RevR19NoReport.md section 6.6 and VolatileContract.md O2 flagged both numbers.
- Unlisted same-class drift: 17 vs 18 aggregator deletions. VolatileContract K3 and corpus/QUALITY.md:49 say 17; `git show --name-status e20f4fa` lists 18 D rows; approval-list.tsv:56-73 holds 18 "pushed" receipts. VolatileContract O2 labels d7710981 as a commit; it is a census SHA-256 prefix (`git cat-file -t d7710981` fails).

M6 classification dispute: BROKEN
- Pointer `build/VolatileContract.md H2/H3`: `grep -c 'H2\|H3'` gives 0. The file uses K2/K3. The register dissent, its WAVE blind_spot and QUALITY 67 repeat the dead label.
- Cited evidence argues the other way. VolatileContract section 1 item 3, section 5 (F5) and section 7 item 9 say census-regression, which blocks the re-pin ("Do not relabel the tokens to pass the gate"). C1Critic "Smallest safe correction" says make the re-pin conditional on non-author sign-off. The row cites both while the pin went ahead as live-state (commit 8f8c58e, 07:57:29 -0300).
- falsify/AdjudicateWaves.md (08:03:04 -0300): line 1 BROKEN; line 29 "block this re-pin as census-regression"; "A blind_spot note is not a substitute for satisfying the contract's pin gate." The row says "adjudication left to wave 2" and omits the verdict. The lesson never names AdjudicateWaves.
- Fix cannot fail: check-register.py never reads blind_spot (no match for "blind"). Four tokens carry it. The route "a future census round" has no tracked item.
- Captured-by "none" is wrong: C1Critic, VolatileContract, TokWaves and AdjudicateWaves all recorded the dispute.
- STALE re-appearance holds [INFERENCE from absence]: c1-drift-r10-prepin.txt (10:53:07Z) has no WATCHDOG_STALE token; the r10 baseline has one. Post-pin `MORI_DRIFT: none` rc 0 (true).
- Undisclosed: the working-tree register (mtime 08:14:47) differs from 8f8c58e by 17+/14-. WAVE evidence and blind_spot were rewritten; SURFACE:lane.{audio,game-dev-2d,game-dev-3d} moved census-schema-change to roster-change (header 29/19/2 to 26/19/5).

M7 misroot: PARTIAL
- "removed its own stray file (build/DraftProvince.md)" names the wrong file. build/DraftProvince.md is the seat's report and exists. The stray was fleet `.ufo/waves/round-20/build/DraftProvince/province-r20.md`; it is ABSENT now, as are fleet build/ and build/DraftProvince/ (stat). The lane copy exists (4212 B).
- "belongs to souji" is stated as fact; MisrootSweep section 2 marks the owner [INFERENCE]. Support exists but is uncited: ContractReview.md:41 (souji round-20/final-dispatch.json names the path). AuditCase07.md exists, 8784 B, mtime 07:02:53 (untouched).
- Fix is a one-time sweep, filed as a seat report rather than an L1 act. QUALITY 43 requires a planted byte-exact misroot to be missed by the legacy sweep and found by the new one before the fix counts. MisrootSweep has no planted case; its positive control is name-matching on lesson text (section 1).
- Captured-by "seat self-detected" holds (DraftProvince.md "Side effect to disclose").

M8 scope: BROKEN
- `.ufo/interactive-sessions/*.jsonl`: not verifiable under my bounds.
- "(their reports)" resolves: SrcK8sController.md:61, TokUnitOOS.md:72, TokWatchdog.md:121, TokWaves.md:124, ContractReview.md:12 each disclose matches. ContractReview and SrcK8sController also matched .ufo/worktrees/ or .jj/.
- Captured-by "context forbade opening, not matching" holds: wave1-spec.json says "Never open retained interactive-session transcripts". That is a rule, not a capturer.
- Fix text is present in wave2-spec.json and wave2-run.json. It cannot fail: wave*-run / -dispatch-receipt JSON and evidence/ hold 0 CONTEXT_OK receipts. QUALITY 44 requires one bound to the spec SHA.
- Incomplete. Build reports disclose walks the row omits: MisrootSweep.md section 6 (find over .ufo/worktrees, 32,190 lines); RevR19NoReport.md section 6.4 (os.walk of .ufo/worktrees, to 2,000,000 files) and section 2 (fleet-wide basename search, 361,096 files); ContractReview.md section 0 (21-lane walk). The context those seats ran under is unverified.

## Cross-cutting
X1 Counting command locale defect (M2): the headline 8 to 0 does not reproduce under the ambient locale.
X2 Moving artifacts, unbound receipts: register mtime 08:14:47 (earlier checks 08:11:23 and 08:04:41; pin 07:54:21); lesson 08:11:34; tool working tree differs from HEAD (sha256 203c716e...). c2-after.json and c2-live-mori.json bind no tool SHA; c1-drift-entering.json binds only the census SHA (cf. QUALITY 22, 33). The live scan now shows 14 waves and stub=51 (scan-lane.json), so "6 stubs" is a snapshot.
X3 Label drift: "H2/H3" (M6, register, QUALITY 67) against K2/K3 in the file.
X4 corpus/QUALITY.md criteria 64-68 (lines 227-256) sit under "Criteria added round 19" (line 188).
X5 Captured-by mixes gate, reviewer and reason. Class is free text with no taxonomy; M6's "classification dispute" is a dispute, not a mistake class.
X6 `build/...` and `evidence/...` pointers are relative to .ufo/waves/round-20/; the base is never stated.

## Gaps and tooling
- Unverified: M8's forbidden pointer; contexts of seats other than the wave-2 spec files; the census (not assigned).
- Scratch kept for reproduction: falsify/ReviewLesson/{mut-r2off,mut-empty}/tools/mori-wave-settlement.py, reg/r20-mutant.txt, oracle-{lane,r2off,empty}.out; /tmp/rl/.
- Installs or updates: none. Tools: /usr/bin/jq 1.8.2, python3 stdlib, git read-only (GIT_OPTIONAL_LOCKS=0), sha256sum, comm/sort/join, stat, pgrep.
