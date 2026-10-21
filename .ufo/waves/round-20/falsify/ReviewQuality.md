# ReviewQuality: falsification of QUALITY 64-68 (round 20)

Verdict: PARTIAL.

Each of 64-68 can fail on a named case, and none is a verbatim copy of criteria 1-63.
Per criterion: 64 PARTIAL, 65 BROKEN, 66 PARTIAL, 67 BROKEN, 68 PARTIAL.
- 65 is BROKEN: its named measure (the counting command) reports 0 on registers that break its own terms, its re-pin branch lacks the census-regression gate the frozen contract has, and its carried-debt wording narrows 41 without a supersession line.
- 67 is BROKEN: it writes into QUALITY the live-state class that wave-2 AdjudicateWaves returned BROKEN and that lesson M6 still lists as an open disagreement; it also covers the same event as 24 with a different duty.

## Scope and snapshot

- Attacked: corpus/QUALITY.md:227-256 (64-68), against corpus/lessons/round-20.md (M1, M2, M3, M6, M9, M10; routed R03, R11), criteria 1-63, and the lane artifacts they cite.
- Lane files changed while I worked. Hashes at the final run (sha256, first 8 hex): tools/mori-wave-settlement.py 79e7f9de; corpus/QUALITY.md 4a748f73; corpus/lessons/round-20.md 139d671e; corpus/evidence/drift-classification-r20.json e244d5b1; .ufo/waves/round-20/build/RegisterCheck/check-register.py 6e602017; .ufo/waves/round-20/evidence/c2-live-mori.json 75f2d35a.
- Reproduction: `python3 .ufo/waves/round-20/falsify/ReviewQuality/c-fixtures.py` (exit 0), output in falsify/ReviewQuality/c-results.txt. Fixture trees live under /tmp/rq-fixtures, never under .ufo/waves.

## Answers

1. Can each fail? Yes, all five. The named failing cases are under each criterion below.
2. Tied to a round-20 row? M1 (64), M2 (65), M3 (66) and M6 (67) exist and cite their numbers. 68 has no M-row; it is tied only to routed item R03. The ties are weaker than stated for 64, 65 and 67 (details below).
3. Duplicates 1-63? No verbatim duplicate. Substantive overlaps: 67 with 24; 65 with 41 (tension, unsuperseded); 64 with 20, 3, 30/34, 56; 66 with 33 and 53; 68 with 9, 20, 23, 51, 57.

## High

### H1. 67 BROKEN: writes the disputed class into QUALITY; duplicates 24

- Text (QUALITY.md:245-250): "A disappearance token whose cause is unchanged census code plus changed host or fleet state is classed live-state ..."
- Dispute state:
  - lesson M6 (round-20.md:27): "an open disagreement for the non-author closure, not a resolved fix".
  - falsify/AdjudicateWaves.md:1 is BROKEN. Line 5: "the register's cause-based live-state choice is not compelled by the contract". Line 29: block the re-pin as census-regression until a non-author record accounts for each removed wave.
  - falsify/AdjudicateStale.md:1 is PARTIAL. Line 15: "Freeze the class boundary ... in the next contract". M6 summarises this as "keep live-state"; the file does not say that without conditions.
  - VolatileContract.md:15: "Labelling them live-state is the laundering the contract exists to prevent."
- Effect: the dissent case (census rule unchanged, host state changed, census blind to it; VolatileContract.md:33, K2) meets 67's trigger on both readings, and 67 selects live-state. The outcome AdjudicateWaves recommends (census-regression) would violate 67. So 67 decides the dispute rather than testing it.
- Concrete failure that 67 does catch: drop blind_spot from -FINDING:WATCHDOG_STALE (present now, register line 208) and 67 fails.
- Concrete failure that 67 does not catch: a re-pin over WAVE_UNSETTLED_AGE for which no non-author record exists (AdjudicateWaves:29). 67 passes it.
- Duplicate of 24: 24 (QUALITY.md:48) says a surface "emptied by another lane's removal is disclosed as empty-by-removal". The register now names e20f4fa as a souji-shokunin operator sweep (register evidence for WAVE_UNSETTLED_AGE), which is that trigger. 67 covers the same event with "live-state + blind_spot" and never cites 24. The two duties are in different vocabularies with no mapping.
- Undefined inputs: "unchanged census code". The register dissent now says "the script as a whole changed in seven commits", and M5 says seven census commits since r10. Only a per-rule reading works, and 67 states neither. Also undefined: "still-real condition" and "route". Five other live-state minus tokens (-attribution, -example, -rowb_files, -subject_commits, -window) carry no blind_spot, and 67 does not say whether they hide a condition.
- Identity gap: C1Critic.md:10 says the token cannot say which wave vanished. AdjudicateWaves:29 requires row mapping. 67 is silent.
- Number drift: M6 says "the 18 removed aggregator files"; VolatileContract K3 (line 35) and 24's source say 17 aggregator-r10* paths; the register says 18 aggregator-r10 and -resume files. Unreconciled.
- Fix: see Suggested wording.

### H2. 65 BROKEN: its named measure cannot enforce its own terms; carried-debt wording conflicts with 41

- Text (QUALITY.md:234-240).
- Fails on: a round that writes "Red retained", "carried" or a free-text [INFERENCE] bucket. Also fails when a token lacks a valid class, which the strict checker catches but the named measure does not.
- Escapes (c-results.txt, current register). The named counting command is the set difference of drift tokens and register keys.
  - Three invalid registers all score 0 on the counting command:
    - census-regression on +SURFACE:lane.audio: strict checker regression=1, exit 1.
    - class "maybe-live" on +SURFACE:lane.chousa: strict unclassified=1 invalid=1, exit 1.
    - evidence removed on +SURFACE:lane.lore: strict unclassified=1 invalid=1, exit 1.
  - The re-pin branch has no gate. 65 reads "then re-pinned" with no census-regression precondition. contract.md:27-31 and :44-46 forbid a re-pin while any token is census-regression, so the first mutant passes 65 and violates the contract.
  - Locale: the frozen command, as typed, gives 44 (r20) and 47 (r13) under LANG=en_US.utf8, with "comm: input is not in sorted order" on stderr. Under LANG=C it gives 0 and 8. M9 (round-20.md:30) reports 37/33; I did not reproduce those exact values, but the defect reproduces. M9's fix (LC_ALL=C for the whole pipeline) is not written into 65.
  - "Evidence pointer" is not measured: the strict checker only requires non-blank evidence (build/RegisterCheck.md:6).
- Tie: M2's fail-capability is the strict checker (unclassified=50 invalid=43; RegisterCheck.md:20). 65 names only the counting command. Its "8 unclassified and 43 invalid" pairs the counting command's 8 with the checker's 43. The checker reports unclassified=50 for the same r13 file (c-results: "r13 strict").
- Conflict: 41 (QUALITY.md:104) says "A red or unevaluated drift pin stays carried debt". 65 says "carried" is not a disposition. 65 narrows 41 with no supersession line. Criterion 25 (QUALITY.md:50) requires narrowing as an explicit correction, and 56 (:181) shows the house form ("Supersedes 53's wording"). Criterion 54 (:171) calls a carried item's status a "disposition", the opposite of 65.

## Medium

### M1. 64 PARTIAL: escape routes on its primary clause

- Text (QUALITY.md:227-233).
- Fails on: a round that cites r19 W2's "22 provider failures" as causes with no per-seat record (round-20.md:67, R11; SpotcheckR19.md:32: "No seat-level error record in any round-19 wave JSON").
- Escapes (c-results.txt; tools/mori-wave-settlement.py at 79e7f9de):
  1. Silent zero. `.ufo/waves` is a symlink to a directory holding one dispatch: rc 0, waves 0, ignored 0, unreadable 0. Fixture C; `_wave_root` returns None at tools lines 95-96. The caveat is disclosed (wave-settlement-r20.md:70-72, "read totals.waves before trusting exit 0"), but 64 does not fail it.
  2. Uncounted dispatches with rc 0. One settled wave sits beside a truncated dispatch (unreadable 1) and a schema-v2 dispatch with a missing report (ignored 1): rc 0. Fixture D; tools lines 339-347, 379.
  3. The count set omits `empty`. A zero-byte report sits in none of present/stub/missing. Fixture A: empty 1; 3 of 4 members accounted for.
  4. "missing" is ambiguous. The per-wave `missing` list includes stub and empty members (tools line 299). In the 10:46Z receipt, sum(len(missing)) = 91 but sum(counts.missing) = 85; round-20 wave1-run.json has counts.missing 0 and six names.
  5. State is not compared. 64 compares counts, not settled/partial/unavailable.
  6. The lesson's receipt does not meet 64's receipt spec. 64 requires "scan time". c2-live-mori.json has no time-like key (top keys: ignored_json, lane_root, schema, totals, unreadable_json, waves). The time appears only in prose (knowledge/wave-settlement-r20.md:71). It matters: marker stubs read 18 at 10:40:40Z (ContractReview.md:52) and 6 at 10:46Z.
  7. Stale snapshot. The receipt lists 11 waves; the scan now finds 14 v1 dispatch files (c-results: waves_tree dispatch_v1=14).
  8. Scope. Discovery covers `.ufo/waves/` and schema v1 only (tools lines 79-97, 331, 347). A dispatch misrooted at the fleet root is never seen; M7 shows the same misroot pattern for a seat artifact this round. The lesson's C2 claim, "every dispatch file" (round-20.md:15-16), is wider than the tool.
- Tie: M1 is cited. "terminal cause record" appears only in 64 (QUALITY.md:232) and is undefined. R11 asked for "a named per-seat record". The spot-check's Q64 draft asked for "a committed record that names that seat and its error; otherwise ... unknown" (SpotcheckR19.md:60). The adopted text keeps neither. It is undecidable as written for R13's provider classes in report prose (SpotcheckR19.md:34) and for the watchdog label "lane-dead-no-report" (R14, :35).
- Overlap: 20 (QUALITY.md:40), 9 (:17), 3 (:5), 56 (:181). The zero and unreadable escapes are already covered in principle by 30 (:72: unreadable is UNKNOWN, never zero) and 34 (:82: a valid empty capture is not evidence that nothing occurred). 64 should cite them, not omit them.
- S02: the lesson says S02 is "documented" (round-20.md:65). knowledge section 2 documents the unreadable case (wave-settlement-r20.md:44-45) and, as a caveat, the zero-discovery and symlink cases (:70-72). The ignored-schema case (fixture D, v2) is documented nowhere. None of this is a criterion; 64 passes fixtures C and D. The spot-check's Q66 rider (SpotcheckR19.md:62) was not adopted.

### M2. 66 PARTIAL: the stub rule is exact bytes

- Text (QUALITY.md:241-244).
- Fails on: a start marker one byte off is counted as delivered. Fixture E: "STATUS: started\r\n", "STATUS: started\n\n", "STATUS: started \n" and "status: started\n" are all `present`. Only the two exact forms are `stub` (tools line 37 STUB_CONTENTS; `_member_status` lines 238-240). 66's own wording, "never counted as a delivered report", is violated.
- The protocol text is "writes the single line `STATUS: started`" (wave1-run.json:493), so deviations are not caught.
- The fix on record is not landed: ContractReview.md:140 (CE-2: whitespace-normalised, at most 64 bytes) is absent from the tool.
- Tie: M3 is cited. It now lists 57 at DraftSettlementNote:19 and 18 at 10:40Z, so the earlier number mismatch is reconciled in the row.
- Overlap (principle, not wording): 33 (QUALITY.md:78: a status line is not content) and 53 (:166: a started row is non-final).

### M3. 68 PARTIAL: routed prose only; falsifier dropped; undefined terms

- Text (QUALITY.md:251-256).
- Fails on: a rerun or pin that cites a present digest as historical. R03 (SpotcheckR19.md:24) records that the working-tree copies differ from the b3602869 bytes for all ten minimized artifacts, including bound round-16 wave1-dispatch.json and wave1-spec.json. [Not re-observed here.]
- Dropped falsifier: the spot-check's draft (SpotcheckR19.md:61) also failed "a bound artifact changes without a mapping row". 68 keeps only the rerun/pin case.
- Undefined: "bound" (53 and 56 define it for dispatch rows only) and "mapping" (no file is named).
- Tension with 51 (QUALITY.md:154): a rerun from the original revision reads un-minimized content. R19 (SpotcheckR19.md:40) says an r18 receipt was minimized for alias, payload and timestamp. 68 is silent on not committing that content.
- Tie: routed R03 only (round-20.md:66). No M-row covers minimized copies. 68 cites "lessons/round-20.md (routed ...)" with no row ID.
- Overlap: 9 (:17), 20 (:40), 57 (:190), 23 (:46).

## Low and cross-cutting

- Heading: 64-68 sit under "## Criteria added round 19" (QUALITY.md:188). No round-20 heading exists.
- M9 is the lesson's named fail-capable item (round-20.md:26: "the fail-capable part is M9"). No criterion in 64-68 cites it.
- Numbering drift: the SpotcheckR19 draft numbers (Q64/Q65/Q66) do not match the adopted ones (64/68/none). Its R03 row still says "QUALITY: Q65" (SpotcheckR19.md:24).
- Current lane: three unreadable JSON files under .ufo/waves, none with dispatch-schema bytes. The two unreadable files in the 10:46Z receipt are unidentified. `round-18/residual-drafting-taskcall.json` is "ordinary task call (not a swarm wave)" (c-results), so it is not a 64 escape.

## Resolved during review (checked at the hashes above)

- 67's "VolatileContract H2/H3" pointer now reads K2/K3 in QUALITY.md:250, round-20.md:27 and the register's dissent and blind_spot strings (register lines 208, 214). VolatileContract.md has no H2/H3 label (c-results).
- M6 now records AdjudicateWaves (BROKEN) and AdjudicateStale (PARTIAL) and says the disagreement is open.
- M3 now carries 57 and 18 with their observation points.
- drift-repin-r20.md no longer states the stale 29/19/2 counts (c-results: knowledge_note_claims_29_19_2=False). The register is 26/19/5.

## Suggested wording (for L1 to decide; not applied)

- 64: Receipt = tool JSON + caller-recorded scan time + lane HEAD + rc. Counts for all seven statuses, summing to members. The receipt state must equal the report's state. Unreadable or ignored dispatch-shaped JSON, or zero discovered records where dispatch evidence exists elsewhere, is non-pass (cite 30, 34). Replace "terminal cause record" with "a committed record naming the seat and its error; otherwise `unknown`" (SpotcheckR19 Q64).
- 65: Measure = the counting pipeline with LC_ALL=C throughout, plus the strict checker's closed-set, non-blank evidence and regression=0 checks. Add: "a re-pin is refused while any token is census-regression" (contract.md:27-31). Add: "supersedes 41's 'stays carried debt' clause".
- 66: Define stub as a whitespace-normalised exact marker with a size bound (CE-2), or enumerate the accepted variants. One fixture per variant.
- 67: Either move the class boundary and the adjudication outcome into the next contract (AdjudicateStale:15), or mark 67 provisional and record AdjudicateWaves:1. Use per-rule granularity. Require row-level identity (C1Critic:10). Cross-reference 24 or state how the two labels map. Define "still-real condition".
- 68: Restore the dropped falsifier. Define "bound" by reference to 53/56 and name the mapping file. Cite R03 by row ID. Add that reruns from original revisions must not commit minimized content (51).
- All: move 64-68 under a "## Criteria added round 20" heading.

## Residual risk and verification gaps

- Not run: census, the tool's --selftest, --pin, --drift (not in scope). No git or jj query was made, so 64's "committed before the round reports" clause is [INFERENCE] only.
- Not re-observed: R03 digests (git show); R11 and R13 seat-level absence; the closure's "two" and "22" claims.
- Lane artifacts moved during review. Line numbers may drift; the defects above reproduce at the recorded hashes.
- The en_US counts differ from M9's 37/33 (I got 44/47); the defect reproduces.
- Criteria 1-63 were checked only where cited.
- The waves-tree walk read bytes of 734 JSON files under .ufo/waves (only names and counts printed), including test JSON under falsify/NoHarmRun/.../sessions/. Nothing under .ufo/interactive-sessions, .ufo/worktrees, .jj or ~/.omp was opened.

## Tools and bounds

- Installs or updates: none. Used /usr/bin/jq 1.8.2, python3 stdlib, coreutils and bash. Locale en_US.utf8 was already present.
- Writes: this report; falsify/ReviewQuality/c-fixtures.py and c-results.txt; /tmp/rq* and /tmp/rq-fixtures (fixtures and copies). No lane production file edited. No git or jj. No subagents. No peer messages.
