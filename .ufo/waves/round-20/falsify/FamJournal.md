HOLDS: 10/10 register rows AGREE. Every class's cause pointer was re-derived from git history, census lines, the r10 pin, and a read-only journal query, and each holds. No token is classed wrong. Five residual defects are recorded (R1-R5); none changes a class.

Scope: rows for +FINDING:JOURNAL_CLASSES_UNMEASURED, +SURFACE:journal.system, +SURFACE:journal.user, -SURFACE:journal, -FINDING:SEGFAULT_JOURNAL, -FINDING:KILL_SIGNAL_JOURNAL, HEADER, volatile_fields, +FINDING:COREDUMP_NOTICE_JOURNAL_USER, +FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER in corpus/evidence/drift-classification-r20.json. Seat reports (TokJournalSchema.md, TokJournalUser.md) were used only as leads. The census was not run (bound). No lane, git-index, or jj mutation; git was read-only (log -S, show, cat-file, rev-parse). Journal reads were counts and metadata; MESSAGE was parsed inside jq and never printed. Scratch: /tmp/famjournal/. Tooling: no installs or updates (git, journalctl, /usr/bin/jq 1.8.2, sha256sum, comm, tr).

## Identity checks
- r10 pin census: `git show 5be8943:tools/mori-census.sh` sha256 d7710981aa1c7571...; matches baseline-r10 line 2 (census_sha256=d7710981...). Exit 0.
- Worktree tools/mori-census.sh = HEAD blob = 87b8d680b9b2572e...; matches register census_sha256 (87b8d680...ab28). Exit 0.
- Round-13 census 18d7d55 = 39abda0a67028575... (matches LOG.md:744).
- Receipt .ufo/waves/round-20/evidence/c1-drift-entering.json: 50 unique stdout tokens; register has 50 keys; in-receipt-not-register = 0; in-register-not-receipt = 0. Each of the 10 tokens appears once in receipt stdout. [INFERENCE] No fresh drift run was made.

## Per-token verdicts

1. +FINDING:JOURNAL_CLASSES_UNMEASURED: census-schema-change. AGREE.
   Cause: added by 18d7d55 (diff-18d7d55.txt:283). Absent from baseline (lines 1-39 contain no such id). Emitted at census:1377, before the first guard at :1378. probe_journal is called unconditionally at census:2704 from run_census (census:2698); run_census is reached from main (:4741) and from cap_census (:2800). Pointer caveat: see R1.

2. +SURFACE:journal.system: census-schema-change. AGREE.
   Cause: 18d7d55 introduces emit_surface "journal.$scope" (`git log -S'journal.$scope'` -> 18d7d55 only; diff-18d7d55.txt:287, 293, 299, 416). Live emitter census:1675 is in the per-scope loop (1633-1676). Unavailable branches at census:1380, 1386, 1392. Baseline line 10 is the single `SURFACE journal:` row.

3. +SURFACE:journal.user: census-schema-change. AGREE. Same hunk and pointers as #2.

4. -SURFACE:journal: census-schema-change. AGREE.
   Cause: the r10 emitters are 5be8943:737, 746, 787 (`emit_surface journal`). 18d7d55 removes them (diff-18d7d55.txt:285, 309, 397). `git log -S'SURFACE journal'` -> 18d7d55, 7ca17b1. Baseline line 10 matches.

5. -FINDING:SEGFAULT_JOURNAL: census-schema-change. AGREE.
   Cause: the r10 emitter is 5be8943:752-761 (text grep 'segfault|general protection fault' at :757, plus unanchored JSON COREDUMP_SIGNAL=11 at :759; combined by max at :761) and :777-779. 18d7d55 removes both (diff-18d7d55.txt:338-346, 388). Id introduced by 7ca17b1 (-S). Baseline line 38 matches.
   Counterfactual: on the current boot the r10 rule gives c_seg = max(text 0, JSON 1) = 1 > 0. The r10 rule would still emit the line, so id retirement, not host state, removes it.

6. -FINDING:KILL_SIGNAL_JOURNAL: census-schema-change. AGREE (see R3).
   Cause: baseline line 37 matches. r10 emitter 5be8943:751 (`grep -ciE 'status=9/KILL|Failed with result .signal|SIGKILL'`) and warn at :773-776. 18d7d55 removes the text emit (diff-18d7d55.txt:383-386). 8d22d18 restores a structured user warn (diff-8d22d18.txt:482). 26f6589 adds positive arms (diff-26f6589.txt:499-507).
   Live counterfactual (current boot): the r10 regex matches 2 user-journal lines. Metadata-only query: both have SYSLOG_IDENTIFIER=sudo and no MESSAGE_ID, EXIT_CODE, EXIT_STATUS, or UNIT_RESULT. Structured killed/9 (98e32220...) = 0. UNIT_RESULT=signal among d9b373ed records = 0 of 270.
   The round-13 label "[INFERENCE] current watchdog/wave/lane activity" is at round-13 register line 35, as the seat reported.

7. HEADER: census-schema-change. AGREE.
   Cause: VERSION census-r5 (5be8943:243) -> census-r6 (diff-18d7d55.txt:67-68). `git log -S'VERSION=census-r6'` -> 18d7d55 only; `-S'VERSION=census-r5'` -> 18d7d55, 9738f1a. Header printf is census:2700 (r10: 5be8943:1594). census:2814 (drift_line_id) maps `mori-census *` lines to the token HEADER. Deliberately unmasked per drift-pin-r10.md:120-124. The r10 pin kept census-r5 (drift-pin-r10.md:4-6).

8. volatile_fields: census-schema-change. AGREE.
   Cause: the comparator is census:2981 (`if [ "$base_vol" != "$DRIFT_VOLATILE_LIST" ]`), printed at :3001. The list is census:2744-2772. Set difference (LC_ALL=C): baseline line 4 has 69 tokens; tip has 103. Only in baseline: kill_signal, segfault, unit_failure (removed by 18d7d55, diff-18d7d55.txt:500-515). Only in tip: 37 = 7 (18d7d55: boot plus 6 counters) + 20 (8d22d18, diff-8d22d18.txt:521-527) + 10 (26f6589, diff-26f6589.txt:533-536). 'boot' has its own mask rule at census:2786, so it is not inert.

9. +FINDING:COREDUMP_NOTICE_JOURNAL_USER: census-schema-change. AGREE (see R5).
   Cause: `git log -S'COREDUMP_NOTICE_JOURNAL_USER'` -> 18d7d55 only (mapping at diff-18d7d55.txt:258). Tip: id census:1076; mapping :1325; query :1433; gate :1457-1459 (js=ok and count>0); emit :1468. r10 (5be8943) has 0 hits each for COREDUMP_NOTICE, coredump_notice, fc2e22bc, segfault_signal11. Baseline has no COREDUMP line.
   Live (read-only): user MESSAGE_ID=fc2e22bc... -> 36; system -> 0 (rc 0).

10. +FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER: census-schema-change. AGREE.
    Cause: `git log -S` -> 18d7d55 only (mapping at diff-18d7d55.txt:260). Tip: mapping census:1327; query :1405-1406; subject :1461-1462; gate :1457-1459; emit :1468. Replaces baseline line 38. Documented by structured-journal-scopes-r13.md:45 and :70-72, and by CensusFix.md:109.
    Live: user MESSAGE_ID=fc2e22bc AND COREDUMP_SIGNAL=11 -> 1. Unanchored user COREDUMP_SIGNAL=11 -> 1.

## Residual defects (none changes a class)
- R1, weak pointer (#1). structured-journal-scopes-r13.md:34-38 describes the census-r6 surfaces and never names JOURNAL_CLASSES_UNMEASURED. Better support: CensusFix.md:94-100 (r13 design: "emitted even when journalctl/jq is absent") and structured-journal-scopes-r13.md:106-114 (line 112, the r14 reason rewrite, matching diff-8d22d18.txt:310->316).
- R2, named-coverage gap in the census (not a C1 issue). census:1372-1376 promises "Named coverage loss", and census:1073 says text-only surfaces are never a look-alike 0. The classes list at census:1377 (kernel_victim_text, gpf_text, other_signals, uncataloged_unit_failure) does not name the r10 'segfault' word sub-rule (5be8943:757). gpf_text covers only 'general protection fault'. The r10 SIGKILL-text sub-rule (5be8943:751) is covered only by the generic other_signals note.
  Measured effect on this boot: segfault-word text = 0; SIGKILL text = 2 sudo command-log lines, no systemd unit record. Historically the segfault text grep also read 0 while JSON read 656 (LOG.md:38-40). Route to a future census round.
- R3, decision-rule gap in TokJournalUser.md:43-50. The rule has no clause for "same id, changed input rule, documented change". #6 is right by cause, since the r10 rule would still fire today. But the written rule does not derive it, because the id is present in both schemas and its live-state clause, read literally, matches. Amend the rule. No class change.
- R4, overstatement in a seat lead. TokJournalUser.md says the coredump emission path is "unchanged since 18d7d55". The gate, mapping, and query strings are unchanged, but the shared journal_query parser changed in 8d22d18 (diff-8d22d18.txt:218-276) and 26f6589 (journal_positive_scan at diff-26f6589.txt:152-160; JOURNAL_JQ_* rewrites at :111-118). The seat's analysis says the rewrites are equivalent for object records. The register text does not repeat the claim.
- R5, count-gated symmetry [INFERENCE] (#9, #10). Presence needs both the new id and a positive count. The class follows the id, since the baseline lacks it; presence follows the host. A zero-count boot would remove both lines, which the register already notes as a live-state flip (census:1457-1459).

## Pointer-method notes
- `-S 'KILL_SIGNAL_JOURNAL'` does not list 8d22d18 (occurrence count unchanged). The warn restoration is shown by diff-8d22d18.txt:482.
- `-S 'DRIFT_COUNTER_KEYS'` lists only 5be8943. List edits in 18d7d55, 8d22d18, and 26f6589 are shown by the diff hunks cited above. The commits cited in the register are correct.

## Commands and outputs (all exit 0)
    git -C <lane> log --format='%h %ad %s' --date=short -S'<s>' -- tools/mori-census.sh
      COREDUMP_NOTICE_JOURNAL_USER -> 18d7d55 | SEGFAULT_SIGNAL11_JOURNAL_USER -> 18d7d55
      journal.$scope -> 18d7d55 | JOURNAL_CLASSES_UNMEASURED -> 8d22d18, 18d7d55
      SEGFAULT_JOURNAL -> 18d7d55, 7ca17b1 | KILL_SIGNAL_JOURNAL -> 26f6589, 18d7d55, 7ca17b1
      SURFACE journal -> 18d7d55, 7ca17b1 | VERSION=census-r6 -> 18d7d55 | VERSION=census-r5 -> 18d7d55, 9738f1a
      user_unit_oom_result_unknown -> 8d22d18 | positive_kernel_oom -> 26f6589
    sha256sum (first 16 hex): 5be8943 d7710981aa1c7571 | 7ca17b1 7432255ff56dc69f | 18d7d55 39abda0a67028575 | 8d22d18 0e41cb83fce2e8c5 | 26f6589 f1f8d1b62bb617bb | 9738f1a 390ab9cd2db17b9d | worktree = HEAD 87b8d680b9b2572e
    Live, boot 3e7084f4-7046-4957-a8a2-c00542a3b469, 2026-10-21 08:03 -03 (read-only):
      journalctl --user -b, MESSAGE_ID=fc2e22bc... -> 36 | --system -> 0 (rc 0)
      --user fc2e22bc... COREDUMP_SIGNAL=11 -> 1 | --user COREDUMP_SIGNAL=11 -> 1
      --user text 'segfault|general protection fault' -> 0
      --user text r10 KILL regex -> 2; metadata-only: 2 x SYSLOG_IDENTIFIER=sudo, no MESSAGE_ID/EXIT_CODE/EXIT_STATUS/UNIT_RESULT
      --user MESSAGE_ID=98e32220... EXIT_CODE=killed EXIT_STATUS=9 -> 0
      --user MESSAGE_ID=d9b373ed... -> 270 | with UNIT_RESULT=signal -> 0

## Not checked
- Pointers outside the 10 rows: receipt lines :13, :16, :47, :66-67; SCORECARD.md:678; journal-alarm-routing-r14.md; round-13 and round-14 lessons.
- No census run. Presence of these tokens at HEAD is [INFERENCE] from the code and the live counts above.

## For the main agent
- No re-run is required for these 10 classes. Optional confirmation: `bash tools/mori-census.sh --drift corpus/evidence/baseline-r10-20261015T2231Z.json` would show these tokens. Not run here (bound).
