# Admission bar (probation draft)

1. Every claim falsifiable or marked opinion.
2. Every claim carries a source: a measured anchor (path:line, command, evidence id).
3. Observation, inference and unknown stay separate.
4. Errata are append-only blocks.
5. A rejection is kept, not silently dropped.

## Criteria added round 12 (each cites the lesson that produced it)

6. Every probe pipeline is rc-gated; a crash exit code never equals a verdict code, and each probe carries an unreadable-input canary. ← lessons/2026-10-15-errexit-pipefail-silent-crash.md:24-25,101-103
   - "The gate then exits with the producer's rc — measured 1 — which is the same exit code this gate uses for a real DRIFT verdict" (:24-25); "Make each input surface unreadable once (`chmod 000` on the dir, run, restore) and require the verdict line." (:101-102)
7. No live producer pipe feeds a match test; capture once and assert over the captured bytes (SIGPIPE 141 ≠ 1). ← lessons/2026-10-15-selftest-grep-sigpipe-race.md:202-203
   - "pipeline rc = rightmost non-zero element. A consumer's exit-early death certificate for its producer is 141, and 141 ≠ 1" (:202-203)
8. A "cannot fake / cannot fail / cannot accept" claim enumerates the channels or inputs tested; untested classes are named residuals. ← lessons/2026-10-15-forgeable-oracle-visible-fixtures.md:111-112
   - "List every path and environment value handed to the SUT; if any encodes which scenario is running, there is a sniffer channel." (:111-112)
9. Every path, line or commit pointer resolves at the carrying commit; a report names the commit that carries its work; a replacement artifact lands with a sweep of every mention. ← lessons/2026-10-15-settle-evidence-references-with-artifacts.md:14-18,114-116
   - "Resolve the active recipes against the delivered commit, and record which earlier artifact each replacement supersedes." (:17-18); "an active "adopted baseline" or rerun recipe must resolve, or be explicitly superseded." (:116)
10. A baseline declares its volatile field set, derivation window, host and gate SHA; re-pin is a recorded act with a reason, never a way to turn red green. ← lessons/2026-10-15-volatile-contract-behavioral-baselines.md:173-176
   - "Pair the baseline with its derivation record: mask list, churn tier, window, host, and the gate SHA." (:173-174)
11. A deferred probe carries its four prices before admission: found-ness, marginal wall time, enforced bound (and code vocabulary), and the filter's drop set. ← lessons/2026-10-15-probe-pricing-dwell-bounds-filter-drop.md:37-38
   - "the price is four numbers, none of which appears in the code that asks for the measurement" (:37-38)
12. No cumulative counter is read without its baseline: boot, cgroup/instance creation time, process start, or window anchor. ← lessons/2026-10-15-free-lunch-measurements-counter-baselines.md:266-268
   - "Print the baseline next to every cumulative counter: boot id, cgroup/instance creation time, process start, or the window anchor." (:266-267)
13. A crash-masking fix and a real repair are told apart by a pre-registered expected gradient: exact tally and PASS set against the frozen gate SHA. ← lessons/2026-10-15-oracle-honesty-crash-masking.md:25-26
   - "Pre-register the expected gradient before landing the fix: pin the exact expected tally and PASS-set against the frozen gate SHA" (:25-26)
14. A counter's semantics cite its increment site, not only documentation wording. ← lessons/round-12.md#M20
   - "any kind of OOM killer" vs the single increment site at S003 `:935-936` (round-12.md#M20)
15. A journal class is counted by MESSAGE_ID or another trusted structured field, never by message text. ← lessons/round-12.md#M13
   - "text grep 0 segfaults vs COREDUMP_SIGNAL 656" (round-12.md#M13)
16. A kill count names its unit (kill vs notice) and its journal scope; scopes are never summed. ← lessons/round-12.md#M19
   - "5 kernel kills vs 7 user + 9 system fe6faa94… notices, same boot" (round-12.md#M19)
   - Qualifier added round 14 (the quote above is retained unchanged): the 5/7/9 sample is text-selected — `journalctl --grep` matches `MESSAGE`, and `--output-fields` restricts output, not matching — so "5 kernel kills" is a retained-journal record count, not a MESSAGE-free structured count, unique-victim tally, or structured gate. ← lessons/round-14.md#M6; corpus/knowledge/kill-classes-by-message-id-r12.md §"Round-13 correction — matching MESSAGE is not structured counting".
17. A detection recipe states which delivery paths it cannot see. ← lessons/round-12.md#M21
   - "S020 probes only kill/tkill/tgkill syscalls" (round-12.md#M21)
18. Kill attribution comes from records written at event time, never from re-reading the victim's cgroup. ← lessons/round-12.md#M22
   - "cgroup path now ENOENT" (round-12.md#M22)
19. A sweep's nonzero hits are inspected before the count is cited; regexes use word boundaries. ← lessons/round-12.md#M18
   - "bare cursor matched 3 files; \bcursor\b matched 0" (round-12.md#M18)
20. A tally cites the counted universe recomputed from delivered artifacts at the carrying commit. ← lessons/round-12.md#M6
   - "eight r8 receipts; the delivered r8 count is 7" (round-12.md#M6)
21. Verdict cells use exactly the four admitted values (improved, harmed, unchanged, unprovable-but-better); qualifications live in the evidence cell. ← lessons/round-12.md#M7
   - "grep -c 'improved narrowly' SCORECARD.md → 9" (round-12.md#M7)
22. An evidence timestamp is no later than the commit that carries it; rounded labels are marked estimates. ← lessons/round-12.md#M8
   - "labels 17:55Z/18:30Z/20:10Z vs commit clocks 17:53:05Z/18:28:43Z/20:06:34Z" (round-12.md#M8)
23. A /tmp path is never evidence; commit the fixture generator and a digest. ← lessons/round-12.md#M9
   - "140/275 fingerprints not recomputable" (round-12.md#M9)
24. An observation surface emptied by another lane's removal is disclosed as empty-by-removal, never as never-written. ← lessons/round-12.md#M17
   - "17 waves/aggregator-r10* paths deleted" (round-12.md#M17)
25. A claim is admitted at the scope it was measured; narrowing is an explicit correction, not a silent edit. ← lessons/round-12.md#M1
   - "at the first revision the claim did NOT hold" (round-12.md#M1)

Source tiers: see corpus/SOURCES.md (contract v1); this file holds claim admission only.

## Provenance of criteria 1–5

- 1. Falsifiable or marked opinion → seed — no lesson.
- 2. Measured anchor for every claim → seed — no lesson.
- 3. Observation, inference and unknown kept separate → lessons/2026-10-15-settle-evidence-references-with-artifacts.md:20-29.
- 4. Errata are append-only blocks → lessons/2026-10-15-settle-evidence-references-with-artifacts.md:120-122.
- 5. A rejection is kept, not silently dropped → seed — no lesson.

## Criteria added round 13

26. A final census verdict is exactly one complete `MORI_CENSUS: CLEAN|DRIFT` record, and its roll agrees with exit 0|1 respectively; a prefix, arbitrary word, duplicate, or opposite roll cannot certify a case. ← lessons/round-13.md#M2 (audit-r11 F02; adversarial wrapper evidence).
27. Long-history membership checks consume captured input without an early-exiting downstream pipe; an exact author near the start and many later sibling records must not lose subject progress. ← lessons/round-13.md#M1 (audit-r11 F01; large-history regression evidence).
28. Canonical seed conformance compares the delivered bytes with the canonical mint template's content block after the sole name substitution; Markdown code-block indentation in PROTOCOL.md is presentation, not checklist content. ← lessons/round-13.md#M3 (round-12 non-author assertion correction and round-13 ReviewPromotion catching an indentation mistake).

## Criteria added round 14

29. A selector cutover is no-harm only when every alarm it replaces keeps its behavioral equivalent: the same positive fixture still raises the same stable finding id, a severity no lower than before, its prior verdict effect on the census roll, and the same named adjacent-owner route; a correct new typed counter does not substitute for a discarded alarm unless that before/after equivalence is measured on both revisions. ← lessons/round-14.md#M1/M2 (`round-13-verifier-spotcheck.md:72–89`; critical `OOM_KILL_JOURNAL`/DRIFT and fleet vs tsukuroi-routed non-fleet findings).
30. Unit classification is read from the failed subject's own `UNIT`/`USER_UNIT` structured metadata, never inferred from manager emitter fields; missing, malformed or unreadable subject metadata is an explicit UNKNOWN/unavailable class and is never counted as fleet, non-fleet, or zero. ← lessons/round-14.md#M2 (`round-13-verifier-spotcheck.md:86`; `_SYSTEMD_UNIT` describes the emitter, not necessarily the failed subject).
31. A verdict-producing gate carries its PROTOCOL §Gate standard registry row at the lane registry home before its results are cited, and any self-test tally names the revision and is measured on the bytes of the actually delivered gate; an earlier revision's tally, or a predicted total, is not a self-test of the delivered gate. ← lessons/round-14.md#M4 (`round-13-verifier-spotcheck.md:25,70`; 24 checks at `80bd58a`, not the delivered `c13df48`).
32. A mutation witness states the exact code delta it installs — whole-function transplant, reconstructed shim, or byte-exact original — and the causal scope it does not establish; historical failures are cited from original frozen-byte runs, and a reconstructed witness never reads as original-byte single-locus causality. ← lessons/round-14.md#M5 (`round-13-verifier-spotcheck.md:57`; F01 whole `grade_lane`, F02 `frozen_source=null` prefix-presence shim).

## Criteria added round 15

33. A receipt's provenance is the exact identity and content of every verdict-driving input, not a `dirty` boolean or a porcelain status line: porcelain records status and path, never content, so an edit to an already-dirty input leaves its line byte-identical while a scope-only delta reports `moving: false`. A gate receipt must hash each declared input at load and at end (`__file__`/imported module bytes, census, frozen control, fixture packs), record the observed `rev-parse HEAD` rather than an asserted pin, and report `moving: false` only when the scope is equal and every declared input digest is equal; otherwise the run is a dirty or moving working-tree observation that cannot be cited as committed bytes or as a complete dirty-path list. ← lessons/round-15.md#M1 (`round-14-verifier-spotcheck.md:83,136`; `AttackProvenance.md` CE1/CE2/CE6).
   - "Exact contemporary porcelain was not retained; untracked output receipts are a supported explanation, not a proved complete dirty-path list." (`round-14-verifier-spotcheck.md:83`)
   - "The status line stayed byte-identical the whole time." (`AttackProvenance.md` CE1 counterexample: a content edit to an already-dirty input still reports `moving:false`).

34. Class wording names the counted unit and its validation scope: a raw class token counts the records that survived that class's aggregate validation (or reads `unavailable:<reason>` when any record invalidates the class), a validated-positive token counts only records individually satisfying the typed predicate, and neither is a kill, victim, event or completeness total; a valid empty capture is a positive 0 (no record satisfied the predicate), never evidence that no event occurred, and a positive value is never renamed, summed across scopes, or printed into a raw token. ← lessons/round-15.md#M2 (`journal-alarm-routing-r14.md:218–222,386–390`; QUALITY #16).
   - "The r14 phrase “fail-loud on positive validated records” meant positive validated **class counts**, not every record; mixed invalid records could suppress otherwise valid positives." (`lessons/round-15.md:20`)
   - "A parsed stream with no individually valid record is a real 0 for the positive token (it is NOT a class total)." (`tools/mori-census.sh:981`)

35. An alarm that survives an invalid aggregate is proved by an independently valid current-boot record witness, not by the aggregate: the gate carries one mixed case per alarm path in which one object record with scalar `_BOOT_ID` equal to the current boot and scalar exact `MESSAGE_ID` (plus exact string `UNIT_RESULT` `oom-kill`/`signal`, or exact string `EXIT_CODE` `killed` with scalar string/number `EXIT_STATUS` 9) sits beside a malformed, nonmatching or foreign-boot record; expected are the raw class/split tokens `unavailable:<reason>` (never 0), the positive token (`positive_kernel_oom`/`positive_unit_oom` for the OOM path, `positive_process_sigkill`/`positive_unit_signal` for the signal path) an integer ≥1, and exactly one crit OOM line for that OOM witness or exactly one user warn signal line for that signal witness, and the same case must be red on the frozen pre-fix bytes and green on the delivered bytes. A positive is never inferred from an unavailable aggregate, a `MESSAGE` match, a second journal query, or a record that fails a scalar/current-boot/result guard; subject `UNIT`/`USER_UNIT` validity neither gates nor supplies a positive count (the owner partition stays aggregate-only). A failed capture (nonzero rc, timeout, stderr bytes) or a failed JSON parse makes every positive token `unavailable:<reason>`, never 0; only a successfully parsed stream with no individually valid record is a positive 0. On a healthy class the positive value equals the raw subset it refines, and a capture with no independently valid positive must not fire. ← lessons/round-15.md#M2/M3 (`round-14-verifier-spotcheck.md:138`; `journal-alarm-routing-r14.md:382–384`).
   - "Legacy KILL_SIGNAL `count`/`process_sigkill` can be `unavailable:<reason>` while an independently available user-unit signal arm raises WARN. Neither unavailable nor the distinct unit-signal count is a fabricated process zero." (`lessons/round-15.md:21`)
   - "OOM_KILL_JOURNAL fires once if ANY positive_kernel_oom or positive_unit_oom is > 0, even while the matching raw counter is `unavailable:<reason>`." (`tools/mori-census.sh:982-984`)
   - "The r15 frozen-red comparison must fail that suppression case before repair counts." (`lessons/round-15.md:20`)

36. A nonzero positive vector is labelled by its source: a fixture observation names its case id and pack, a live observation names boot, scope, capture window and receipt, and a fixture vector is never reported as live positive load, a class total, or census completeness. ← lessons/round-15.md#M3 (`round-14-verifier-spotcheck.md:138`; SCORECARD round-14 vector correction).
   - "The prior raw nonzero vectors in SCORECARD.md round-14 (`3/0/2/1/2/1` user and `2/1/4/3/0/2` system) are **fixture vectors**, not live positive load." (`lessons/round-15.md:23-25`)

## Criteria added round 16

37. A dispatcher carries every messaging restriction into the seat assignment it writes; an omitted restriction is an L1 dispatch defect, while a prohibited seat broadcast remains a separate seat violation. Exact-id correction is not retroactive compliance or runtime prevention. ← lessons/round-16.md#M1 (= C15-1; precedent `lessons/round-15.md:22`).
   - "L1 sent exact-id correction to every seat; no broadcast is authorized." (`lessons/round-15.md:22`)
38. A seat's probe, download, or expected-output file is written only to a path its assignment authorizes; a `/tmp` write is never durable evidence and is disclosed as an out-of-lane write even when its bytes are later reproduced in-lane. ← lessons/round-16.md#M2 (= C15-2; precedent `lessons/round-15.md:23`).
   - "Temporary source downloads are not admitted durable evidence or an authorized lane write expansion." (`lessons/round-15.md:23`)
39. Writing a selftest, or a `--selftest` entry, is not permission to run it. A seat records its selftest as unexecuted until the integration owner runs it once after all seats settle; having written the implementation never justifies an executed result. ← lessons/round-16.md#M3 (= C15-3; precedent `lessons/round-15.md:24`).
   - "implementing a subprocess selftest arm is not permission to execute it" (`lessons/round-16.md` C15-3 fix text)
40. A registry row is swept whenever its gate, selftest, or source changes: the active registry must match the delivered entry points and pinned values. A row found stale at read time is a finding for that read; its current status is whatever the active row shows after correction, not what an earlier read recorded. ← lessons/round-16.md#M4 (= C15-4).
   - The read-time stale observation at `SKILL.md:134` is recorded historically in `lessons/round-16.md#M4`; this criterion does not assert the current state of that row.
41. A green fixture or sibling gate never establishes drift freshness. A red or unevaluated drift pin stays carried debt. Any re-pin requires a separately reasoned semantic review that names what changed and why the new pin is correct; a stated reason alone is not sufficient, and a re-pin that only turns red green is rejected (QUALITY #10). ← lessons/round-16.md#C15-5 (debt, **not** a mistake; no M5 is asserted; outside closure of the prior r15 round).
   - "A green C1 fixture gate does not establish freshness." (`lessons/round-16.md` C15-5)
42. Exact anchor start, not gap-free continuity: an incremental journal window counts records only after its first record reproduces the anchor cursor bytes and boot. A mismatch, boot boundary or failed/truncated capture is unavailable, not an empty success. Cursors remain opaque: exact-byte equality is conservative acceptance, while inequality may refuse an alias and does not prove deletion; no general entry-equivalence, deduplication or complete-access guarantee follows. ← lessons/round-16.md ## Gate, S039/S040.
   - "If no entry matching the specified cursor is found the call will seek to the next closest entry" (S039, `sd_journal_seek_cursor`, opened 2026-10-20). A seek fallback is therefore never an anchor observation.
   - "cursor strings do not uniquely identify an entry" (S040, `sd_journal_test_cursor`, opened 2026-10-20).
   - "The format of the cursor is private and subject to change." (S014, `journalctl(1)` `--show-cursor`).
   - Transfer caveat: S039/S040 document the libsystemd `sd_journal_*` API. The `journalctl --cursor` missing-anchor behavior is not stated in the S014 text read here and is not measured; the criterion does not assume it.

## Criteria added round 17

43. A fleet-root misroot sweep has no pathspec, and candidate attribution checks
    filename **as well as** content. A planted byte-exact prior misroot must be
    missed by the legacy scoped sweep and found by the corrected sweep before the
    fix counts. A clean limited sweep is not a clean fleet-root sweep.
    ← lessons/round-17.md#M1; lessons/round-16-verifier-spotcheck.md:202–209.
44. Before every wave dispatch, retain a `CONTEXT_OK` receipt bound to that
    spec's SHA-256; a missing clause blocks dispatch until corrected. This tests
    instruction text only, never runtime prevention.
    ← lessons/round-17.md#M3; lessons/round-16-verifier-spotcheck.md:216–219.
45. Probe disclosures enumerate every live query (including failed queries),
    write and background job; naming only the `/tmp` writes while omitting the
    host-probe section is an under-disclosure. Correct it by appended precision.
    ← lessons/round-17.md#M2; lessons/round-16-verifier-spotcheck.md:210–215.
46. A stale pending/version statement is superseded by a dated appended note
    naming the observation time and closure, never rewritten into a claim about
    the current host. Sweep active province, index and knowledge prose too.
    ← lessons/round-17.md#M4; lessons/round-16-verifier-spotcheck.md:220–223.
47. In a jj-colocated lane, distinguish an observed commit from the resolved
    branch and from remote publication. `--is-ancestor` status 1 means divergence,
    another nonzero status means error; rows A/C keep their exact-author parser
    separate from committer diagnostics. Sibling-shokunin authorship is not an
    ambient-author violation. ← lessons/round-17.md#M6.
48. Transcript classes count observations at scan time, not incidents or
    permanent deaths. Match exact prefixes, preserve duplicate relative paths,
    exclude main sessions, and never turn a missing prefix into a clean lane
    report. Vendor business codes take priority over generic HTTP 429.
    ← lessons/round-17.md#M7.
49. A shared fake-binary dispatcher models only the selected binary's side
    effects: Git trace variables must affect the Git stub, not df/journalctl.
    Prove the simulator boundary with a direct positive Git control and negative
    non-Git control before treating a canary as a production-scrub failure.
    ← lessons/round-17.md#M19 (retained rc1 oracle failure, then 134/134).
50. Derived metadata honors the declared retention contract, not an arbitrary
    display cap. Numeric error codes remain strings within the configured input
    span; unknown cause is not permission to drop the code. Independent
    `want.records` expectations stay unchanged across the fix.
    ← lessons/round-17.md#M20 (65/66 to 66/66 with the same fixture table).

## Criteria added round 18

51. Committed handoff material (reports, dispatch specs, evidence JSON) carries scoped
    summaries, counts and SHA-256 of private sources, never excerpts, session or store
    identities, or operator configuration values. The retention gate at the measured
    revision must report zero unallowlisted hits, and a must-redact file carries no
    allowlist row. Disclosing a copy does not satisfy this criterion; a digest of a short,
    guessable private line is provenance, not redaction.
    ← lessons/round-18.md#M1; lessons/round-17-verifier-spotcheck.md:322-350,388-397.
52. A `pre-build` freeze label is a verdict from the freeze-order check, not prose: frozen
    inputs must strictly precede the first implementation commit and stay unchanged. A
    co-committed input grades `co-evolved`; a `no-implementation` verdict does not yet
    support a pre-build label. Corrections are appended rows, never rewritten labels.
    ← lessons/round-18.md#M2; lessons/round-17-verifier-spotcheck.md:120-130,207-213,398-402.
53. Every dispatch attempt is logged before the call with the SHA-256 and byte length of
    its committed payload and completed with the observed result (exact refusal text for a
    refusal). A row without a digest, with a mismatched digest, or a non-final or duplicate
    started row is unbound. Spec-level binding (criterion 44) does not satisfy this.
    ← lessons/round-18.md#M3; lessons/round-17-verifier-spotcheck.md:291-297,408-411.
54. Carried procedural defects stay named debt: every wave context restates the pre-action
    VCS (read-only `git -C` verbs only, no plain lane `git status`, no lane jj), scratch and
    field-projection bounds, and each carried V-item keeps its disposition. Instruction
    text is never cited as runtime prevention; a clean final state closes nothing.
    ← lessons/round-18.md#M4; lessons/round-17-verifier-spotcheck.md:303-320,403-407.
55. Acceptance examples in a contract are derived by applying the frozen rule, and the
    frozen rule wins when they disagree. An executor that meets an example contradicting
    the rule reports the conflict; the integrator fixes the implementation to the rule and
    records the contradiction, never the rule to the example.
    ← lessons/round-18.md#M5 (C2 `no-implementation` overclaim; C1 freeze-commit self-hits).
56. Supersedes 53's wording: a dispatch-attempt **row** is bound or unbound (digest and
    bytes recompute from the committed payload at the measured revision); a **ledger** is
    clean or failed (contiguous attempts, non-decreasing time, exactly one final
    started/partial row, `started_ids` equal to `tasks_count`, result values only
    refused/started/partial). A refused-only ledger can have every row bound and still fail.
    ← lessons/round-18.md#M3; .ufo/waves/round-18/falsify/ReviewQuality51to55.md.

## Criteria added round 19

57. A content-review decision binds the whole blob and exact measured revision,
    covers every path in its frozen population, and says what content was reviewed.
    Missing, changed, unresolved or provenance-only decisions cannot certify clean.
    Same-wave origin is provenance, not a content-safety predicate. An additional
    bounded review never replaces the all-blob retention gate or narrows its
    allowlist denominator. ← lessons/round-19.md#M1.
58. A freeze-order receipt carries the measured full commit, exact loaded-byte
    register/correction digests, executing-script digest, resolved claim bases/tips,
    overrides and argv. Unbound legacy output remains unbound; new metadata does
    not retroactively bind old JSON. A historical correction and prospective-label
    verification are separate units, not interchangeable defects.
    ← lessons/round-19.md#M2.
59. Trend verdicts use LEARNING's observables: repairs, source-row counts and
    capability-table formatting do not by themselves establish new covered-ground
    knowledge or re-verification of an old entry. State the census histogram from
    the actual rows and qualify source scope rather than inflating tiers.
    ← lessons/round-19.md#M3.
60. Rejected source rows still need a located quote of at most 25 words in Gate,
    or an explicit unavailable screening-only limitation with the access attempts;
    never imply an unopened body was read. A capabilities table records the actual
    first-working round, not the later formatting-repair round.
    ← lessons/round-19.md#M4.
61. A reader's transport presentation is not source bytes: never integrate
    line anchors, elision text or continuation notices. Validate every changed
    source/JSON path on its delivered bytes, retaining a malformed intermediate
    control when repairing an accidental projection copy.
    ← lessons/round-19.md#M5; round19 `evidence/q13-stable-paths.json` (9→0).
62. A present delivered instrument that crashes or returns malformed metadata
    is an after-mode regression, not proof that its capability is absent.
    Missing-capability red is reserved for the explicitly measured before
    boundary; source and receipt failure must remain distinguishable.
    ← lessons/round-19.md#M8; first `finite-after.json` versus corrected run.
63. A before counter derives failure or absence from the target's actual
    returned fields and exit outcomes, not from a phase label that presupposes
    the desired delta. Retain compatible and unsupported-binding observations;
    use the same final counting instrument and unchanged expected requirements
    for both sides. ← lessons/round-19.md#M9.
64. Every dispatched wave's per-seat report presence is counted by
    `tools/mori-wave-settlement.py scan` and the receipt (scan time, dispatch
    path and sha256, present/stub/missing counts) is committed before the
    round reports that wave's settlement. Fails when a reported wave count
    differs from the receipt, when no receipt exists, or when a missing report
    is called a dead/failed seat without a terminal cause record.
    ← lessons/round-20.md#M1; r19 W1 scan 16/64 partial, exit 1.
65. A red drift baseline re-observed in a round is dispositioned in that
    round: every token classified into the closed set with an evidence pointer
    (unclassified count 0 by the counting command), then re-pinned, or a named
    census-regression routed with owner, or the reason no pin is safe. "Red
    retained", "carried" or a free-text [INFERENCE] bucket is not a
    disposition and not a classification. ← lessons/round-20.md#M2; r13
    register 8 unclassified and 43 invalid against the r20 entering drift.
66. A seat start marker is never counted as a delivered report: settlement
    and seat-count claims exclude the `stub` status, and a protocol that
    writes a marker must ship with the counter that distinguishes it.
    ← lessons/round-20.md#M3; frozen `present` = size>0 counted 18 markers.
67. A disappearance token whose cause is unchanged census code plus changed
    host or fleet state is classed live-state, and when the disappearance
    hides a still-real condition it also carries `blind_spot` with a route;
    re-pinning never certifies health, only sameness since the pin.
    ← lessons/round-20.md#M6; -FINDING:WATCHDOG_STALE and
    -FINDING:WAVE_UNSETTLED_AGE dissent (VolatileContract K2/K3).
68. A minimized or sanitized copy never moves a pinned digest: the mapping
    records the entering-revision digest, the present digest and whether the
    artifact was bound; a bound artifact is re-run from its original revision,
    never from the sanitized working copy. Fails when a rerun or pin cites a
    present digest as historical. ← lessons/round-20.md (routed r19 closure
    R03 via `.ufo/waves/round-20/build/SpotcheckR19.md`).

## Criteria added round21 — outside-closure correction

Attribution correction (2026-10-21): criteria64–68 above were authored round20, despite
their placement beneath the round19 heading. Their original bytes remain.

69. **Supersedes67.** Classify a disappearance by evidence assurance before
    causal explanation: disappearance of required observation evidence without
    an independently evidenced, per-identity settlement or cleanup-accounted
    disposition is `census-regression` and blocks baseline acceptance. Unchanged
    census code plus changed host/fleet state explains cause, not observation
    completeness. Same-identity posthoc pushed receipts prove cleanup, never
    independent lifecycle closure. Preserve each unresolved identity and its
    provenance; do not infer it is still unsettled. Ordinary observed state
    changes remain `live-state`. A `blind_spot` note cannot override the blocker.
    The r20 baseline is a retained historical artifact, **not an accepted
    behavioral reference**; no post-pin `none` rescues its premature acceptance.
    ← lessons/round-21.md#M1 and #M2; round20 non-author closure C1_class_ruling
    and quality_criteria; frozen round21 loss-unknown/cleanup-only cases.

Q64/65/66/68 remain explicitly qualified debt in lessons/round-21.md.
This supersession does not assert those separate gates were repaired.

## Criterion added round22 — population identity before scalar agreement

70. Every reconciled count names its exact population, measured commit and
    policy-excluded identities. Compare full path/line/class/digest multisets
    and independent policy membership; do not derive exclusions by subtracting
    two totals or exclude source-policy copies to force agreement. A matched
    receipt is accounting agreement only, never privacy clearance or acceptance
    authority. Wrapper/argv/inner measured revisions must agree even when hit
    lists happen to be equal. Demonstrate rejection with the same instrument
    against a valid, count-preserving identity mutation and retain the red
    receipt; also preserve the original permission control and unknown-loss
    blockers. ← lessons/round-22.md#M1 and #M3; corrected pre-implementation
    denominator freeze and exact-multiset oracle.

## Criterion added round23 — negative claims require complete enumeration

71. Do not turn a partial collection into a negative or uniqueness verdict.
    If one candidate mapping cannot be enumerated, retain the failure and refuse
    “disabled”/unique association; a successful sibling read does not complete
    the missing population. Likewise, accounting-active evidence does not prove
    runtime enforcement. Use only the narrower observed proposition, or withdraw
    a capability whose advertised negative/positive verdicts cannot support it.
    Demonstrate the rejection with a genuine controlled counterexample, not a
    rewritten expected row. Ground: lessons/round-23.md#M9; actual mocked
    permission-loss receipt and source-bit distinction; production withdrawal
    rather than an unsealed repair. This is an admission rule, not a score or a
    new supported quota implementation.

## Criteria added round 24 — round-23 routed items as checks (`tools/mori-routed-check.py`)

Each line names the round-23 routed item it carries (`corpus/lessons/round-23-verifier-spotcheck.md:60-66`)
and the check row that can fail it. Run: `python3 -I tools/mori-routed-check.py --repo <lane> --rev <rev> --round 24`.
Able to fail: thirteen sandbox mutants in `.ufo/waves/round-24/w1/BuildRoutedCheck.md` turn the named row red.

72. routed r23-R1 — The quota capability stays absent until a new sourced declaration,
    an independently frozen oracle and a prospective proof exist: no path containing
    `quota` is added under `tools/` or `corpus/knowledge/`, no tool names the case
    CaseEscapedSpace, and the `.ufo/waves/round-23` tree is byte-identical to `c725aa37`.
    Regression guard, not a repair. ← lessons/round-23-verifier-spotcheck.md:62.
73. routed r23-R2 — The retention debt stays visible: the round-23 retention floor and
    comparison receipts and both retention tools are byte-identical to `c725aa37`, and no
    added line in the self-assessment or knowledge surfaces asserts privacy clearance.
    An agreeing accounting run is agreement, never clearance. Regression guard.
    ← lessons/round-23-verifier-spotcheck.md:63; contract amendment A1.
74. routed r23-R3 — Missing transient-source and overwritten-wrapper limitations stay
    recorded, not reconstructed: the `.ufo/waves/round-23` tree (evidence, rejected) is
    byte-identical to `c725aa37`. Regression guard. ← lessons/round-23-verifier-spotcheck.md:64.
75. routed r23-R4 — A wave's dispatch payload is committed before the call: every ledger of
    the round verifies clean, each row's `at` is no earlier than the commit that last changed
    its dispatch file, and every wave spec has a started ledger row. This is the repair; it
    is red on round 23 (`--round 23` at `c725aa37`: eight wave-1 rows precede their dispatch
    commit). Limit: both times are written by the lane, so this proves recorded ordering, not
    harness-observed ordering. ← lessons/round-23-verifier-spotcheck.md:65; amendment A4.
