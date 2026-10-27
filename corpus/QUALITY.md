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
and states only what the check's predicate tests. Run: `python3 -I tools/mori-routed-check.py --repo <lane> --rev <rev> --round 24`.
Able to fail: the twelve expected-red sandbox mutants in `.ufo/waves/round-24/w1/BuildRoutedCheck.md` (plus two
green controls) and the wave-2 tamper probes in `.ufo/waves/round-24/w2/MutRouted*.md`; the scratch clones
themselves are not committed.

72. routed r23-R1 — Regression guard, not a repair. The check fails when a path containing `quota` is added
    under `tools/` or `corpus/knowledge/`, when any blob under `tools/` contains the string CaseEscapedSpace, when
    `tools/mori-quota-surface.py` or `corpus/knowledge/quota-surface-r23.md` exists, or when the
    `.ufo/waves/round-23` tree differs from `c725aa37`. It does not detect quota logic added under another name
    or inside an existing tool. ← lessons/round-23-verifier-spotcheck.md:62.
73. routed r23-R2 — Regression guard. The check fails when the round-23 retention floor or comparison receipt,
    or either retention tool, differs from `c725aa37`, or when a line added in the self-assessment or knowledge
    surfaces matches the key-separator-true form of the privacy-clearance key (case-insensitive; amendment A1
    scope). It scans additions only: deleting a debt row or asserting clearance in other words passes. An
    agreeing accounting run is agreement, never clearance. ← lessons/round-23-verifier-spotcheck.md:63.
74. routed r23-R3 — Regression guard. The check fails when the `.ufo/waves/round-23` tree (evidence, rejected)
    differs from `c725aa37`; it does not read reconstruction claims written elsewhere.
    ← lessons/round-23-verifier-spotcheck.md:64.
75. routed r23-R4 — The repair, for the binding clause of routed item 4 only. The check fails unless every
    `*-attempts.json` and `*-ledger.json` of the round verifies clean, each row's `at` is no earlier than the
    commit that last changed its dispatch file, and every wave spec has a ledger whose last row is `started` or
    `partial`. It is red on round 23 (`--round 23` at `c725aa37`: eight wave-1 rows precede their dispatch
    commit) and green on both round-24 waves. Limits: both times are lane-written (a backdated commit passes);
    `at` has no upper bound; ledgers are found by file name; the separate-worktree and accurate-invocation
    clauses of item 4 are not checked. ← lessons/round-23-verifier-spotcheck.md:65; amendment A4; wave-2
    CriticC1Admission.

## Criteria added round 25 — round-24 routed defects D1 and D2 (`tools/mori-routed-r24.py`)

76. A self-test evidence file names the measured full revision and carries the full stdout and the exit code
    of the shipping tool. Its header names the full 40-hex commit the run was measured against, the command,
    the tool blob and fixture tree, and the exit code of that same run; the rest is the complete stdout, not an
    excerpt or a remembered tally. The tool blob and fixture tree must be identical at the named revision and at
    the revision that carries the file. Evidence whose bytes differ from what the shipping tool prints at that
    revision (a missing line, or the same line with a different count) is stale and reads red: a tally is never a
    pass because its number looks right. Mechanism to watch: every stale file found in rounds 18–24 landed in a
    commit that also edited the tool it reports on. ← lessons/round-24-verifier-spotcheck.md:137;
    `.ufo/waves/round-25/w1/PatternStaleEvidence.md`.
77. A correction sweeps every mention in place. When the lane corrects a stated fact, every place that states it
    (body prose, decision-table rows, sibling files) carries the corrected wording at the commit that carries the
    correction; the superseded wording is removed, not shadowed. A "this section wins" banner or a general
    disclaimer is not a fix: a contradicted line left standing is a defect whether or not a corrections section
    exists. The sweep runs over whitespace-folded text with emphasis removed, so a phrase split across a line
    break or wrapped in asterisks still matches, and a statement a critic named explicitly gets its own named
    correction row. ← lessons/round-24-verifier-spotcheck.md:138-143.
78. A counting command reads every input from committed bytes at a named revision. It refuses a revision that
    does not resolve to a commit, a missing counted file and a short input list with exit 2, and it never reads a
    list, pattern or fixture from the working directory, so running it from another directory or at a bad revision
    cannot print the after-value. The command is a committed script, not a pasted one-liner. ←
    lessons/round-26.md (M1).
79. A present-tense statement about how a host tool behaves names the release it holds for. When the evidence is
    an upstream branch head or a newer tag than the installed package, the statement is scoped to that ref or it is
    false of the host: check the installed version (package query, binary strings or the tool's own version line)
    before carrying an upstream sentence into a host reading. ← lessons/round-26.md (M4).

## Criteria added round 27 — round-26 routed defects D1 and D3, and a prompt-induced privacy leak

80. Seat output is committed or disposed of before the round's last lane commit. Before the final commit,
    `git -C <lane> status --porcelain --untracked-files=all -- .ufo/waves/round-<N>/` prints nothing, and every file a
    seat wrote after that commit is named in the next round's lesson with its disposition (committed as a late
    report, or withheld with the reason). A report statement may rest only on committed bytes. ←
    lessons/round-27.md (M1).
81. A SOURCES row keeps its first-published cells. After a row lands, only its `status`, `recheck` and `used-by`
    cells change in place; any other correction is a new row whose `teaches` opens `supersedes S0NN —`, and the old →
    new is logged in the lesson. Check: `python3 -I -B .ufo/waves/round-27/check-row-identity.py <rev>` reads every
    row's first-published cells from committed history and must print `changed=0`, exit 0. ← lessons/round-27.md
    (M2).
82. A seat report or capture output is linted for host identifiers before its first commit. The retention scan
    cannot see uid digits or pids, so before committing any seat report the L1 runs
    `grep -nE 'user-[0-9]{3,}\.slice|user@[0-9]{3,}\.service|\bpid[ =:]*[0-9]{3,}|\buid[ =:]+[0-9]{3,}' <files>` and
    redacts every hit that is a value read from this host (a fixture or an upstream format string is not). A
    dispatch prompt never asks a seat to list unit names, pids or uids; it asks for depth, role and counts. ←
    lessons/round-27.md (M3).

## Criteria added round 28 — round-27 routed defects 1 and 2

83. A dated amendment or heading states a time read from the clock or from git, never a time typed from memory, and
    that time is never later than the commit that ships the line. The check reads the contract and every commit time
    from git objects at `<rev>`. The bound is the commit's committer time: in this jj-colocated lane the author time
    is when the empty change was opened, not when its content was written, so an author-time bound false-fires on
    honest text — the round-17 A1 heading states `2026-10-20 ~16:10` and ships in `273aa74` (author
    15:26:13-03:00, committer 16:31:56-03:00). A heading that states only a date is compared by calendar day; a
    zone-less local time by that minute in the commit's own offset; a full instant by the second. Check:
    `python3 -I -B .ufo/waves/round-28/check-heading-time.py <rev> <file> [--heading <substring>]
    [--bound cI|aI]` prints one line per dated heading with `verdict=ok|FUTURE-DATED` and exits 1 when any heading is
    future-dated, 0 when none is, 2 on a bad revision, a missing file or a usage error. It FAILS on round-27 W1 at
    `df886be1` (`stated=2026-10-22T15:55Z`, `added_by=dd4dbb20`, `cI=2026-10-22T12:50:10-03:00`,
    `verdict=FUTURE-DATED`, exit 1) and passes on the appended correction heading at `079a47c` (day granularity,
    exit 0). ← lessons/round-27-verifier-spotcheck.md:144-145; lessons/round-28.md (M1).

84. A round's last lane batch carries tip receipts of every counter and of the retention scan, measured at the first
    parent of that batch — a commit cannot hold a receipt of its own hash — and the round's report cites every receipt.
    A receipt must live under `.ufo/waves/round-<N>/evidence/` in the tree at the batch, name the counter it ran (or
    `mori-retention-gate.py` for the scan), name the measured revision as the full 40-hex first parent, carry an
    `exit:` line and at least one line of stdout, and be cited by name in a report. Check:
    `bash .ufo/waves/round-28/check-tip-receipts.sh <rev> <round> [--report-repo <dir> --report-rev <rev>]` reads
    every input from committed bytes at named revisions (default reports: the lane's `LOG.md` and the round lesson;
    with `--report-repo/--report-rev`, the fleet `.ufo/reports/round-<N>/mori.md` is also required to cite them).
    Exit 0 when every counter and the retention scan have a cited receipt, 1 otherwise, 2 on a bad revision or usage
    error. It FAILS on round-27 at `df886be1` (no receipt naming parent `9c2c7de9…`, exit 1); a synthetic round-28
    tip batch measured at its parent passes (exit 0). ← lessons/round-27-verifier-spotcheck.md:146-147;
    lessons/round-28.md (M5).

## Criteria added round 29 — round-28 routed defects

85. At the freeze commit of a writer-blind wave, no report in the writers' wave directory written by a non-writer
    cites a tool line or carries tool-run output, and every writer report lists the files it opened. A non-writer is
    a committed report whose file name does not match the wave's declared writer-name regex. A citation is
    `mori-oom-killers.py:<digits>`, `mori-oom-killers.py` followed by a line range, or a `Tool lines` table header;
    tool-run output is a `MORI_OOM_KILLERS_SELFTEST:` line other than a PASS tally of an older case file, a
    `KILLERS_QUIET exit` line, or an `--inputs` repro result. A files-opened list is a `Files opened` line or heading
    followed by at least one path, and it names no forbidden path: the tool, any `w1/` or `w2/` report other than its
    own, or `corpus/lessons/`. ← lessons/round-28-verifier-spotcheck.md:126-127; lessons/round-28.md:143-146 (M6),
    :117-118, :121. Check: `bash .ufo/waves/round-29/check-blind-wave.sh <lane-rev> <wave-report-dir>
    <writer-name-regex>` reads only committed bytes at `<lane-rev>`, prints `blind_violations=<n>` and one line per
    violation naming the file and line number (never the matched text), and exits 0 when n=0, 1 otherwise, 2 on a bad
    revision or a usage error. For the M6 fix it must exit 1 on the round-28 freeze `d21b8bd3` at
    `.ufo/waves/round-28/w1` with `^CaseA2r`, and exit 0 on a synthetic clean directory; the round-29 build records
    both runs. Until that script is committed the criterion is unenforced and no round may claim it. Red inputs: a
    non-writer report containing `mori-oom-killers.py:305`; a `CaseA2r` report with no files-opened list; a writer
    list naming `w1/CriticC2Design.md` (the M6 disclosure) or `corpus/lessons/round-28.md`.

86. A round lesson's `## Gate` table records every reject decision its source work met as its own row, so a
    non-author closure can sample a reject from the Gate. Each decision cell reads `admit, …` or `reject, <reason>`;
    a reject row names the source it rejected (a URL, `own-work:` or `gist:`) and a non-empty located quote. A Gate
    with no reject row carries `reject sample: none met` inside its own section; a closure that samples that
    declaration states that it re-opened no reject. ←
    lessons/round-28-verifier-spotcheck.md:128 (§6.3), :107, :109-110; lessons/round-28.md:63-72 (eight rows, all
    admit, so the round's only reject sample came from the re-opened S097/S146). Check, over committed bytes:
    `git -C <lane> cat-file -e <rev>:corpus/lessons/round-<N>.md || exit 2`
    `git -C <lane> show <rev>:corpus/lessons/round-<N>.md | awk -F'|' '/^## Gate/{s=1;next} s&&/^## /{s=0} s&&/^\| *S[0-9]+ *\|/{d=$(NF-1);src=$3;q=$(NF-2);gsub(/^ +| +$/,"",d);gsub(/^ +| +$/,"",src);gsub(/^ +| +$/,"",q); if(d~/^reject, /){rej++; if(d!~/^reject, [^ ]/||src!~/^(https?:\/\/|own-work:|gist:)/||q=="")bad++} else if(d!~/^admit, /)bad++} s&&/^reject sample: none met/{none=1} END{printf "gate_reject_rows=%d none_declared=%d malformed=%d\n",rej+0,none+0,bad+0; exit ((bad==0&&(rej>=1||none==1))?0:1)}'`
    prints `gate_reject_rows=<n> none_declared=<0|1> malformed=<n>` and exits 0 when no row is malformed and a
    reject row or the declaration exists, 1 otherwise, 2 on a missing lesson. It FAILS on round 28 at `7118f320`
    (`gate_reject_rows=0 none_declared=0`, exit 1) and PASSES on `round-25.md` (`gate_reject_rows=7`, exit 0). Red
    inputs: a Gate of admit rows only with no declaration (round 28's state); a decision cell `reject` with no reason;
    a reject row with an empty source or quote cell.

87. A tip receipt measured at the first parent of the batch that lands it says so in its header, and that batch adds
    only receipt files. Every file added at `<rev>` against `<rev>^` lives under `.ufo/waves/round-<N>/evidence/` and
    opens with the exact line `# measured at parent <first-parent 40-hex>; the landed tip adds only receipt files
    under .ufo/waves/round-<N>/evidence/`; the receipts keep QUALITY 84's shape. The report that cites them lies in an
    earlier batch and names the receipt files it expects. ← lessons/round-28-verifier-spotcheck.md:129-130 (§6.4);
    lessons/round-28.md:52-56 (M5), :108. Check: `bash -c 'lane=$1; rev=$2; round=$3; R=$(git -C "$lane" rev-parse "$rev^{commit}")||exit 2; P=$(git -C "$lane" rev-parse "$R^1")||exit 2; bash "$lane/.ufo/waves/round-28/check-tip-receipts.sh" "$R" "$round"||exit 1; a=$(git -C "$lane" diff --name-only "$P" "$R"); [ -n "$a" ]||{ echo no_added_files; exit 1; }; n=0; for f in $a; do case "$f" in ".ufo/waves/round-$round/evidence/"*) ;; *) echo "tip_adds_nonreceipt=$f"; exit 1;; esac; h=$(git -C "$lane" show "$R:$f"|sed -n 1p); w="# measured at parent $P; the landed tip adds only receipt files under .ufo/waves/round-$round/evidence/"; [ "$h" = "$w" ]||{ echo "header_not_parent=$f"; exit 1; }; n=$((n+1)); done; echo "tip_receipts=met receipts=$n only_receipts=yes"; exit 0' _ <lane> <rev> <round>` runs the QUALITY 84 checker
    first, then the header and diff-scope assertions; it prints `tip_receipts=met receipts=<n> only_receipts=yes`,
    exit 0, or names the first offending file, exit 1, 2 on a bad revision. It FAILS on the round-28 receipt batch
    `1fc6bb0` (`header_not_parent=…/tip-count-c1.txt`, exit 1: line 1 is `revision: 5ef4e8db…`) and on a batch that
    also edits `LOG.md` (`tip_adds_nonreceipt=LOG.md`); it PASSES on a synthetic two-commit repo whose tip adds one
    receipt with the header (exit 0). Red inputs: a receipt whose header names the tip's own hash or a grandparent; a
    tip batch that edits the lesson or `LOG.md`; a receipt without the `exit:` line.

Round-29 note on 85 (appended by the L1, MoriR29): the first run on the round-29 writer wave (`221cbd8f`, before the
case freeze) printed `blind_violations=20` (`.ufo/waves/round-29/evidence/blind-check-prefreeze.txt`); wave-2
adjudication of each hit is recorded in `corpus/lessons/round-29.md`. The check was bound into a counted condition
(round-29 amendment A4) before it had been run on a known-clean input: see the round-29 lesson `## Mistakes`.

## Criteria added round 30 — round-29 routed defects

88. A round's tip receipts are cited by name in the files its tip check reads — `LOG.md` and
    `corpus/lessons/round-<N>.md` — before the receipts-only batch that lands them, so the tip holds the citations
    without editing a report. `bash .ufo/waves/round-28/check-tip-receipts.sh <tip> <N>` prints `tip_receipts=met`,
    exit 0. A receipt cited only in another report (`SCORECARD.md`) prints `cited_lane=no` for that counter and
    `tip_receipts=unmet`, exit 1. The check credits a receipt named in either default report, so a `met` line proves
    the receipts are named where the check reads, not that each of the two files names each receipt; a round claiming
    this row records the per-file counts beside the `met` line. Because QUALITY 87 lets the tip batch add only receipt
    files, a citation read at the tip was written in an earlier batch. ← lessons/round-29-verifier-spotcheck.md:154-156
    (routed R1); lessons/round-29.md:102-103 (M4); QUALITY 84, 87.
    Check: `bash .ufo/waves/round-28/check-tip-receipts.sh <tip> <N>` prints one `counter=…` or
    `retention receipt=…` line per required receipt and then `tip_receipts=met|unmet`; exit 0 met, 1 unmet, 2 on a
    bad revision or missing input. It FAILS at `b581173a` (round-29 tip: `counter=count-c1.sh … cited_lane=no`,
    `counter=count-c2.sh … cited_lane=no`, `tip_receipts=unmet`, exit 1; its batch adds only the three receipts) and
    PASSES at `1fc6bb0` (round-28 tip: batch adds exactly `tip-count-c1.txt`, `tip-count-c2.txt`, `tip-retention.txt`;
    `tip_receipts=met`, exit 0; `LOG.md` at the parent already names `tip-count-c1.txt`). Red inputs: a receipt cited
    only in `SCORECARD.md` (round 29's state); a receipts batch that also edits `LOG.md` or the lesson (QUALITY 87's
    `tip_adds_nonreceipt`); a receipt naming its own hash instead of the first parent.

89. A `## Gate` reject row whose reason asserts absence — matching `no line`, `no match`, `no matches`, `no hit`,
    `no occurrence` or `returned no` (case-insensitive) — carries the exact `grep` invocation it ran in backticks and
    that invocation's output in the same row: `exit 1` (grep's own no-match status) or a printed `0`. A row that
    narrates the absence without command and output is malformed even when its decision is right; a reason that
    asserts a fact (a declaration, a duplicate URL, an HTTP status) is out of scope. ←
    lessons/round-29-verifier-spotcheck.md:157-158 (routed R2); lessons/round-29.md:65 (the S155 reject row: "a
    case-insensitive grep for `dryrun` and `version` returned no line in either file", with no command and no output).
    Check, over committed bytes:

    ```sh
    lane=<lane>; rev=<rev>; round=<N>
    git -C "$lane" cat-file -e "$rev:corpus/lessons/round-$round.md" || { echo missing_lesson; exit 2; }
    git -C "$lane" show "$rev:corpus/lessons/round-$round.md" | python3 -I -B -c '
    import re,sys
    ab = re.compile(r"\b(no line|no match(?:es)?|no hit|no occurrence|returned no)\b",re.I)
    cmd = re.compile(r"`[^`]*\bgrep\b[^`]*`")
    wit = re.compile("exit[ =]1\\b|\u2192\\s*`?0\\b|0 matches",re.I)
    g = 0
    rows = bad = 0
    for ln,line in enumerate(sys.stdin,1):
        s = line.rstrip("\n")
        if re.match(r"^##\s+Gate\b",s): g = 1; continue
        if g and re.match(r"^##\s",s): g = 0; continue
        if not g or not s.startswith("|"): continue
        d = s.rstrip().rstrip("|").rsplit("|",1)[-1].strip()
        if not d.startswith("reject,") or not ab.search(d[7:]): continue
        rows += 1
        if not (cmd.search(s) and wit.search(s)):
            bad += 1
            print("line=%d absence_reason_without_grep_command_or_output" % ln)
    print("absence_reject_rows=%d malformed=%d" % (rows,bad))
    sys.exit(0 if bad == 0 else 1)'
    ```

    prints `absence_reject_rows=<n> malformed=<n>`, exit 0 when malformed=0, 1 otherwise, 2 on a missing lesson. It
    FAILS at `a66751b1` on the round-29 Gate (`line=65`, `absence_reject_rows=1 malformed=1`, exit 1) and PASSES on
    a scratch Gate row carrying `` `grep -in dryrun f.go` → `0`, exit 1 `` (`absence_reject_rows=1 malformed=0`,
    exit 0). Red inputs: the round-29 row as written; a row whose only "command" is the word grep in prose; a row
    carrying the command but no output.

90. Every word-count label in a `## Gate` table and in `corpus/SOURCES.md` — a `(N words)` before a quote
    (`(N words): "…"`) or after one (`"…" (N words)`), including `/`-joined pairs — equals `wc -w` of the quoted text
    as carried in the file, between the quote marks, with `\|` still counted as a whitespace-separated token. A label
    that differs by one is a defect, not rounding. A Gate row with no located quote is QUALITY 86's business; this
    row measures labels that exist, and requires at least one (`n>0`) so a Gate that carries no label fails rather
    than passing vacuously. ← lessons/round-29-verifier-spotcheck.md:159 (routed R3); lessons/round-29.md:57, :60-63.
    Check, over committed bytes:

    ```sh
    lane=<lane>; rev=<rev>; round=<N>
    git -C "$lane" cat-file -e "$rev:corpus/lessons/round-$round.md" || { echo missing_lesson; exit 2; }
    git -C "$lane" cat-file -e "$rev:corpus/SOURCES.md" || { echo missing_sources; exit 2; }
    { echo "@@LESSON"; git -C "$lane" show "$rev:corpus/lessons/round-$round.md"
      echo "@@SOURCES"; git -C "$lane" show "$rev:corpus/SOURCES.md"; } | python3 -I -B -c '
    import re,subprocess,sys
    Q = r"\"((?:[^\"\\]|\\.)*)\""
    after = re.compile(Q + r"\s*\((\d+) words?\)")
    before = re.compile(r"\((\d+) words?\)\s*:\s*(" + Q + r"(?:\s*/\s*" + Q + r")*)")
    unit = re.compile(Q)
    def wc(q):
        return int(subprocess.run(["wc","-w"],input=q.encode(),stdout=subprocess.PIPE).stdout.split()[0])
    src = ""; gate = 0; n = bad = 0; el = 0
    for line in sys.stdin:
        if line == "@@LESSON\n": src = "lesson"; el = 0; continue
        if line == "@@SOURCES\n": src = "sources"; el = 0; continue
        el += 1
        if src == "lesson":
            if re.match(r"^##\s+Gate\b",line): gate = 1; continue
            if gate and re.match(r"^##\s",line): gate = 0; continue
            if not gate: continue
        if not line.lstrip().startswith("|"): continue
        spans = []
        for m in after.finditer(line): spans.append((int(m.group(2)),[m.group(1)]))
        for m in before.finditer(line): spans.append((int(m.group(1)),unit.findall(m.group(2))))
        for k,qs in spans:
            n += 1
            w = sum(wc(q) for q in qs)
            if w != k:
                bad += 1
                print("line=%d label=%d wc=%d quote=%s" % (el,k,w," / ".join(qs)[:70]))
    print("word_labels=%d mismatched=%d" % (n,bad))
    sys.exit(0 if bad == 0 and n > 0 else 1)'
    ```

    prints `word_labels=<n> mismatched=<n>` and exits 0 only when `mismatched=0` and `n>0`, 1 otherwise, 2 on a
    missing lesson or `SOURCES.md`. It FAILS at `a66751b1` (`word_labels=16 mismatched=5`, exit 1): `:57` 11 vs 10,
    `:60` 11 vs 10, `:61` 5 vs 4, `:62` 17 vs 16, `:63` 8 vs 6. The routed R3 names two of these (11 vs 10 and 17 vs
    16); the check finds three more in the same Gate, so "Two word-count labels are one high" is under-sampled. It
    PASSES on a scratch lesson (`word_labels=3 mismatched=0`, exit 0). The same check flags round 28's S147
    (`label=11 wc=14`, `corpus/lessons/round-28.md:67`) because the escaped cell separators `\|` count as tokens; a
    round that wants rendered-word semantics must carve out `\|` in the criterion, not in a silent edit. Red inputs:
    a label one high (round 29's five); a label attached to the wrong quote in a multi-quote cell; a label computed
    from the location token instead of the quote.

91. A gate enters a counted condition only with a committed `--selftest` that shows it discriminates: it reports `0`
    (`blind_violations=0`) on a known-clean input adjudicated clean by a non-author closure, and reports a violation
    for each planted leak class it claims to catch — for the round-30 blindness gate: a tool line citation, a tool
    output marker, a forbidden path in a files-opened list, and a missing files-opened list. The selftest is committed
    before the counted run and before the freeze commit it grades; a gate without it may be an observation, never a
    counted condition, and its result can neither certify nor sink a claim. ← lessons/round-29.md:32-37 (M2), :96-99
    (M2 correction: "not yet a QUALITY row; not shown able to fail"); lessons/round-29-verifier-spotcheck.md:162-163
    (routed R5); .ufo/waves/round-30/contract.md:75-79 (the four classes); corpus/QUALITY.md:461-464 (the round-29
    note on 85 records the same gap). Check: `bash .ufo/waves/round-30/check-blind-wave.sh --selftest` prints `PASS`
    and exits 0 when the known-clean input reports 0 and every planted class raises a violation, 1 when a class is
    missed or the clean input reports a hit, 2 on a usage error, a missing input or a gate path absent at `<rev>`. It
    FAILS at `a66751b1`: the path is absent (`git cat-file -e` exits 128), so no selftest can run. The committed
    round-29 gate at `d6d5cb0a` also fails the interface: `--selftest` prints `usage: check-blind-wave.sh <lane-rev>
    <wave-report-dir> <writer-name-regex>` and exits 2, and its first counted run at that freeze printed
    `blind_violations=20`, all 20 adjudicated false positives (lessons/round-29.md:32-37; spot-check :162-163). Until
    the round-30 gate and its selftest are committed this row is unenforced and no round may claim it. Red inputs:
    the round-29 gate's interface; a selftest with no clean-input run; a selftest that catches the four classes but
    not the writer-vocabulary false positives behind round 29's 20 hits; a selftest committed after the counted run.

92. The disputed A2a verdict — an active earlyoom whose `ActiveEnterTimestampMonotonic` is absent or `0`, a journal
    with at least two version lines, a real send line before the last version line and none after it, then a plain
    restart; verdict `KILLERS_UNKNOWN` — is pinned by a frozen case in
    `tools/fixtures/mori-oom-killers/cases-a2-r30.json` whose blob equals the blob at the first commit that added the
    file, and the A2a limit is stated where the next reader looks: a line in `SKILL.md` or a `corpus/knowledge/`
    entry that names the case id and `limit`, saying the rule does not attribute a send that precedes the latest
    version line. ← lessons/round-29-verifier-spotcheck.md:164-165 (routed R6); .ufo/waves/round-30/contract.md:64-69
    (the shape and the pinned fields). Check, over committed bytes:

    ```sh
    lane=<lane>; rev=<rev>
    python3 -I -B -c '
    import json,re,subprocess,sys
    L = sys.argv[1]; R = sys.argv[2]
    def sh(*a):
        return subprocess.run(("git","-C",L)+a,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL).stdout.decode()
    p = "tools/fixtures/mori-oom-killers/cases-a2-r30.json"
    t = sh("show",R+":"+p)
    if not t:
        print("missing_case_file"); sys.exit(2)
    cs = json.loads(t)["cases"]
    SENDS = ("sending SIGTERM to process ","sending SIGKILL to process ","escalating to SIGKILL after ")
    def disputed(c):
        i = c.get("inputs",{})
        kv = dict(x.split("=",1) for x in i.get("earlyoom_show","").splitlines() if "=" in x)
        if kv.get("ActiveState") != "active": return 0
        if kv.get("ActiveEnterTimestampMonotonic","0") not in ("","0"): return 0
        m = [str(e.get("MESSAGE","")).lstrip() for e in i.get("earlyoom_journal",[])]
        v = [k for k,x in enumerate(m) if x.startswith("earlyoom ")]
        s = [k for k,x in enumerate(m) if x.startswith(SENDS)]
        if len(v) < 2 or not s: return 0
        if any(k > v[-1] for k in s) or not any(k < v[-1] for k in s): return 0
        return str(c.get("expect",{}).get("verdict","")) == "KILLERS_UNKNOWN"
    h = [c for c in cs if disputed(c)]
    ids = [c.get("id","") for c in h if c.get("id")]
    limit = "no"
    docs = ["SKILL.md"] + [x for x in sh("ls-tree","-r","--name-only",R,"--","corpus/knowledge/").splitlines() if x.endswith(".md")]
    for d in docs:
        for line in sh("show",R+":"+d).splitlines():
            if re.search(r"\blimit",line,re.I) and any(cid in line for cid in ids):
                limit = "yes"; break
        if limit == "yes": break
    added = sh("log","--format=%H","--diff-filter=A","--max-count=1",R,"--",p).strip()
    blob = sh("rev-parse",R+":"+p).strip()
    frozen = "yes" if added and sh("rev-parse",added+":"+p).strip() == blob else "no"
    print("pinned=%d limit_stated=%s frozen=%s" % (len(h),limit,frozen))
    sys.exit(0 if h and limit == "yes" and frozen == "yes" else 1)' "$lane" "$rev"
    ```

    prints `pinned=<n> limit_stated=<yes|no> frozen=<yes|no>`; exit 0 when `pinned>=1`, `limit_stated=yes` and
    `frozen=yes`; 1 otherwise; 2 when the case file is missing or unparseable. It FAILS at `a66751b1`
    (`missing_case_file`, exit 2: no frozen case for the shape exists at the entering tip) and PASSES on a scratch
    one-commit repo holding one disputed case and a `Limit: case pin-a2a …` line (`pinned=1 limit_stated=yes
    frozen=yes`, exit 0). Red inputs: a case whose verdict is `KILLER_ACTED` (`pinned=0`, exit 1); a second commit
    that edits the frozen case (`frozen=no`, exit 1); a correct case with no limit line in `SKILL.md` or the
    knowledge entry (`limit_stated=no`, exit 1).

93. A gate bound into a counted condition carries, committed before the freeze it governs, a receipt of the frozen
    gate run on the round's own inputs with every hit adjudicated (instrument false positive or real violation) by a
    non-author seat; a gate first run on the round's own inputs after the freeze cannot carry a counted condition.
    Check: `git log --reverse --format=%H -- <gate receipt on own inputs>` names a commit that is an ancestor of the
    freeze commit and the receipt names the gate blob at the freeze. Lesson: `corpus/lessons/round-30.md` M5 (repeats
    round-29 M2). Shown able to fail: round 30 — the A2 gate's first run on the round-30 writers (`32e287ff`,
    `.ufo/waves/round-30/evidence/gate-a2-prefreeze.txt`) printed 4 unadjudicated hits, and the gate blob at the freeze
    `db1ec469` printed 1 more (`evidence/c2-after.txt`); no adjudicated receipt of the freeze blob precedes the freeze.

94. Supersedes criterion 93 (routed D3: criterion 93 cannot fail on its stated property — its check passes a
    receipt whose hits are unadjudicated, `corpus/lessons/round-30.md:215`; criterion 93 stays as written). A gate
    may carry a counted condition only when a receipt committed before the freeze records the exact frozen gate blob
    run on the round's own writer inputs after the gate's last edit, keeps the complete hit list, and carries one
    explicit non-author adjudication per hit; and the gate, replayed on a two-hit negative brief, prints two hit
    lines. A changed gate, an omitted hit or an unadjudicated hit makes the gate ineligible for that condition.
    Check: at freeze F, `git merge-base --is-ancestor <receipt commit> F`, the receipt's gate blob equals
    `git rev-parse F:<gate>`, every receipt hit line has an adjudication line naming a non-author seat, and the gate
    on a brief with two forbidden entries in one files-opened list prints two `writer-forbidden-opened-path` lines.
    Lesson: `corpus/lessons/round-31.md` (routed D3; round-30 M5). Shown able to fail: the round-30 freeze `db1ec469`
    fails it — no adjudicated receipt of the freeze gate blob precedes it (`corpus/lessons/round-30-verifier-spotcheck.md:176-183`),
    and the round-30 parser prints one hit for two forbidden entries (fixture F02 under the do-nothing port,
    `.ufo/waves/round-31/evidence/c2-controls.txt`, `F02 diff want=[(3, …), (4, …)] got=[(3, …)]`).
    Criterion 92 is unmet at the round-30 tip (`limit_stated=no`: no `r30-disputed-*` id is named with a limit in
    `SKILL.md` or `corpus/knowledge/`, `corpus/lessons/round-30.md:228-229`); recorded here, not repaired this round.

## Criteria added round 32 — round-31 routed defect 4 and round-32 mistake M1

95. A judge receipt names the sha256 of the exact bytes it judged, and the counter recomputes the sha256 of the same
    section at the measured revision and requires equality. Naming only a revision does not satisfy this. The judged
    bytes can change after the receipt, as row 9 of the round-31 entry did (`corpus/lessons/round-31-verifier-spotcheck.md:219-220`).
    Check: at revision R, the receipt's `judged-sha256` equals `count-c1.py --section-sha` of the file at R (round 32,
    R4 in `.ufo/waves/round-32/count-c1.py`). Lesson: `corpus/lessons/round-32.md` (routed defect 4). Shown able to
    fail: wave-C0 control (c), a receipt computed before one table cell was edited, scores `judge` on every row
    (`.ufo/waves/round-32/c0/CtlForgedJudge.md:120-125`).

96. A contract, declaration or lesson sentence that says a source row was never re-opened, or was last opened when
    it was added, cites the sweep that found no re-open: the command over `corpus/lessons` and `.ufo/waves` at the
    measured revision, and its output. Without the sweep the sentence is not written. Check: the sentence's line
    carries a command and an output pointer, and re-running the command reproduces the output. Lesson:
    `corpus/lessons/round-32.md` M1. Shown able to fail: the round-32 contract says every population row "was last
    opened in the round that added it" (`.ufo/waves/round-32/contract.md:17-18`, frozen at `29f7d043`), and the
    sweep at the base lists earlier `Reopen*` seats for S041, S043–S047, S068, S117, S128 and S137
    (`.ufo/waves/round-32/evidence/m1-reopen-sweep.txt`).

## Criteria added round 33 — round-32 routed defect 2 (judge rule drift)

97. Every judge dispatch and every judge receipt quotes the decision rule word for word from the frozen contract, and
    the counter checks it at a stated comparison level (whitespace runs collapsed). A judge reason that concedes any
    unsupported part records `unsupported` (or `disagree`), never an agreement with a caveat; a reading of the rule
    that first appears in a receipt is not the claim's rule. Check: at revision R, the frozen rule sentence is a
    substring of the collapsed text of both the committed dispatch and the committed receipt (round 33:
    `.ufo/waves/round-33/count-c1-a1.py` prints `dispatch_rule=yes receipt_rule=yes`), and no receipt line pairs an
    agreement with a conceded gap. Lesson: `corpus/lessons/round-33.md` (Round-32 repair §2, Mistakes M1). Shown able
    to fail: the round-32 receipt does not contain its dispatch's rule sentence — `grep -F 'Reject (disagree) a row when'
    .ufo/waves/round-32/judge/JudgeRecheck.md` prints nothing while `.ufo/waves/round-32/r1-dispatch.json` contains it,
    and its S058/S117/S128/S149/S137 reasons concede unsupported parts beside `agree` (`JudgeRecheck.md:63,73-76`).

## Criteria added round 34 — round-33 routed defect 1 (a counter a no-decision control meets)

98. Before any data seat, a measured claim's contract maps each leg-rejection shape — generic rows or copying the
    observed column; server echo; label- or id-keyed answers; skip-work or do-nothing; content-free output;
    no-decision content; a rule changed, or rows deleted, after data — to a named control or to a stated
    inapplicability with its reason. A control discharges a shape only when it is the claim's deliverable with that
    shape's defect injected (the claimed deliverable minus the claimed work); a control that fails by generic absence
    (deliverable absent, guard tripped) discharges only the skip-work and content-free shapes. Each control is scored
    under the frozen counter and its receipt is committed in a revision that is an ancestor of the first data commit.
    A control the counter scores as met means the counter or the target is wrong: re-design before data, or declare
    the claim exploratory. Check: (a) the contract's control table names every shape above once; (b) each named
    control has a receipt line under the frozen counter; (c) `git merge-base --is-ancestor <receipt commit> <first
    data commit>` holds. Lesson: `corpus/lessons/round-33-verifier-spotcheck.md` §3.2 item 4 and §8 item 1;
    `corpus/lessons/round-34.md`. Shown able to fail: round 33's nine pre-data controls (`.ufo/waves/round-33/contract.md`
    at `fdf4371f`, controls list) name no no-decision control, so (a) fails, and the post-data no-decision control
    CtlGlossaryA1 met P-C1-A1 (spot-check §3.2). Round 34's table (`.ufo/waves/round-34/contract.md`, Pre-data
    controls, at `b9fb029e`) maps each shape, and its receipt `evidence/c1-controls.txt` scores 16 negative controls
    `C1=unmet` under P-C1-A1 before any data seat. Not covered: a control set that discharges every shape can still
    miss a rule-order defect (round-34 Mistakes M1).

## Criteria added round 34 — round-34 mistake M2 (a post-data shortcut met the A1 counter)

99. Before any data seat, a measured claim whose counter runs the deliverable in a harness also scores, under the
    frozen counter, two shortcut controls: (i) a label-keyed control whose judged outputs are a function only of the
    labels the counter's generator emits (device names, fixture ids, seed-shaped values), with one label family per
    class or state the generator draws; a control keyed on the fixed-seed input bytes does not discharge (i); and
    (ii) a harness-keyed control that detects the counter's own harness (a FIFO, a namespace, a tmpfs, a fixed
    interval or seed) and does the claimed work only there, doing nothing or returning a constant on the real input.
    The frozen counter checks each arm the claim names (for example a live arm) on the real input with a bound in
    both directions, so a constant such as zero cannot meet it on an active device; an idle device's correct rate may
    be zero, so the lower bound comes from a witness with known activity. Check: (a) the contract's control table
    names both controls, and the row of (i) lists the generator's label families; (b) each of the two controls has a
    receipt line `unmet` under the frozen counter in a revision that is an ancestor of the first data commit; (c) for
    each named arm, on one real-input witness with known activity, a passing baseline and two mutants that change
    only that arm's numeric output — one below the arm's lower bound, one above its upper bound — each score `unmet`,
    and the receipt names that arm's bound as the failure. Lesson: `corpus/lessons/round-34.md` M2.
    Shown able to fail: round 34's control table (`.ufo/waves/round-34/contract.md` at `b9fb029e`) has C-labelkey,
    which keys only on the 12 fixed-seed input bytes, and no harness-keyed control, so (a) fails; the real-live arm
    of `count-c1-a1.py` rejects only a negative rate or one above the outer readings' delta
    (`.ufo/waves/round-34/count-c1-a1.py:275-278`), so it accepts zero on an active device and (c) fails; a program
    correct offline and on the fed arm can keep that shortcut and meet C1, as the post-data probe `ef936fb4` (class
    from device-name patterns; one real read with every rate 0; two reads only when `/proc/diskstats` is a FIFO) did
    under P-C1-A1 (`.ufo/waves/round-34/evidence/ctl-postdata-shortcut/receipt.txt`, re-scored `rescore-a3.txt`). The
    first draft of this criterion had one Check sentence; mutation seat MutQ99 found it accepted a fixed-seed label
    key and an upper-only bound (`.ufo/waves/round-34/wb/MutQ99.md`, variants 3 and 4 survived), reviewer ReviewQ99
    asked for the bound sentence to get a subject and a check (`wb/ReviewQ99.md`, D1, D2), and critic CritQ99Revised
    found the revised (a)-(c) reject both variants and asked that (c) name the arm and an active witness
    (`wb/residual/CritQ99Revised.md`); this text carries those fixes, applied after that review and not re-judged.
    Correction to 98 (append-only): its last sentence's "round-34 Mistakes M1" is round-34 Mistakes M3 (rule order).
    Not covered: 99's controls are not a certificate that the counter discriminates every rule. Critic CritQ99Gap
    built two more programs that skip part of the claimed operation and met P-C1-A1 (`wb/CritQ99Gap.md`: one drops
    the sysfs-only devices that are not partitions from rule R4's union, one replaces unsigned-decimal validation
    with a blacklist of the generator's corruption characters); rule-level skips are round-34 Mistakes M3.

## Criteria added round 35 — round-34 spot-check §6 items 1 and 5, round-35 mistake M1

98 correction (round 35, append-only; round-34 spot-check §6 item 5). 98's worked example breaks its own rules three
    ways. D1: 98 lists "a rule changed, or rows deleted, after data" as a shape, but round 34's control table
    (`.ufo/waves/round-34/contract.md:65-81`) has no row for a rule changed after data; its inapplicability entry
    covers only rows deleted after judgment. D2: round 34's server-echo row reads `unmet (guard)`
    (`contract.md:77-78`) and the C-echo-v1 receipt shows the guard trip (`evidence/c1-controls.txt:26-28`); by 98's
    own sentence a guard trip discharges only the skip-work and content-free shapes, so server echo was not
    discharged. D4: the contract says three of its 16 negative controls met P-C1 (`contract.md:142-143`); four runs
    met (`c1-controls.txt:29-34,38-43`: C-echo-v2-base64, C-echo-v3-umount, C-emptylive, C-zero-singleread), in three
    shape groups. Round 35's own contract (`.ufo/waves/round-35/contract.md`, Controls) also fails 98(a): it names no
    server-echo, observed-column-copy, no-decision or rule-changed control (round-35 lesson M1).
100. In a depth claim's decision table, every verdict cell names a reader action: an imperative verb and an object
    that resolves (a command, a path or a field), so the reader knows what to run, read or report next. Check: select
    the verdict cells by table position and judge each cell's own text, without its column header or its neighbours;
    a cell that reads as an action only through its header (a bare label such as `candidate`) fails. Lesson:
    `corpus/lessons/round-33-verifier-spotcheck.md:226-228` and `corpus/lessons/round-34-verifier-spotcheck.md:196-197`.
    Shown able to fail: `corpus/knowledge/watchdog-identity-r31.md:21` has the verdict cell `candidate`, which fails;
    `corpus/knowledge/disk-write-rate-r33.md:20` has `Convert a sector delta to bytes by multiplying by 512, and never
    by the device's logical or physical block size`, which passes. Not covered: whether the action is correct or
    sourced, and whether the claim's counter rejects a no-decision control (98).
101. A pre-data control receipt may rule that a control which met the frozen counter "does the claimed work" only if
    the control fills every field of the deliverable's declared shape with content that is not empty, does not deny
    the claim, and is about the claimed object. A met control with an empty field is 98's content-free shape; one
    whose field denies or contradicts the claim, or is a bag of words, is the denial shape (kaidoku round 32,
    `kaidoku-shokunin/corpus/lessons/round-32-verifier-spotcheck.md` routed defect 4). Either forces a re-design before
    data or an exploratory claim, never a "residual" note. Check: for each `C1=met` line in the receipt, list the
    deliverable's fields and the control's content in each; any empty, denying or off-topic field makes a "not a
    skip" ruling fail. Lesson: `corpus/lessons/round-35.md` M1. Shown able to fail: round 35's receipt
    (`.ufo/waves/round-35/evidence/c1-controls.txt`, control 10c) rules CtlSkipDesign B a non-skip although its
    capability and what-it-can-now-do cells are empty (`.ufo/waves/round-35/c0/CtlSkipDesign.md`), so the ruling fails
    101; the register's prose is then held up only by non-author row judges, not by P-C1.
102. A round that changes `corpus/SOURCES.md` lands no in-place change to an existing row: for every `S###` row, the
    cells other than status, recheck and used-by equal the cells the row had in the commit that first held it. A
    later row whose teaches opens `supersedes S###` is the correction's disposition; it does not erase the in-place
    change, which stays listed. Check: `python3 .ufo/waves/round-35/check-sources-appendonly.py <tip> --round-base
    <entering tip>` (read-only git) prints every changed id with its `superseded_by=` disposition,
    `appendonly_violations=N ids=[...] superseded=[...]` and `round_changed=[...]` (every id a round commit changed,
    also one changed back to its first cells; ResNoHarmFixes); the round passes only with
    `round_changed=[]` (exit 0); exit 2 is an error. Lesson: `corpus/lessons/round-35.md` M2 (round 34 edited S182 and
    S193 in place and its lesson said no existing row changed). Shown able to fail: `check-sources-appendonly.py
    dd76eb79 --round-base f10a320d` prints `round_changed=[S182,S193]`, exit 1; at round 35's tip with `--round-base
    dd76eb79` it prints `round_changed=[]`, exit 0, while 18 ids stay listed (S069, S182 and S193 superseded; 15 not),
    all changed in place before round 35 and carried as routed debt. Not covered: deleted rows. (Revised in round 35
    after CritNoHarm N3: the first text let a supersede row discharge the violation, a waiver QUALITY 81 does not
    grant.)
    Notes after round-35 wave 2 (append-only). 101 not covered: a met control whose fields are all filled but whose
    evidence cell also carries an unparsed dangling path (round 35's 9d) passes 101's Check; MutQ101 kept that mutant
    alive (`.ufo/waves/round-35/w2/MutQ101.md`), so evidence validity stays with the counter and the row judges.
    MutQ102 (`.ufo/waves/round-35/w2/MutQ102.md`) showed the first 102 text let a junk `supersedes S041` row with no
    source discharge S041 (mutant iii survived); the revised 102 above keeps every changed id listed, and a new row's
    own validity is rule 1's Gate check (URL, access date, located quote).

## Criteria added round 36 — round-35 spot-check §6 items 3 and 4, round-36 mistakes

103. After every lane helper commit, the lane git index holds no staged path and no intent-to-add entry, and the
    round's dispatch log records the check after each `landed` line. Check: `bash tools/mori-index-clean.sh
    /home/vgpnk/Projects/shokunin/mori-shokunin` prints `staged=0 intent_to_add=0`, exit 0. Lesson:
    `corpus/lessons/round-35.md` M4; `corpus/lessons/round-35-verifier-spotcheck.md` §6 item 4. Shown able to fail: the
    tool's self-test runs `git add -N newfile` in a sandbox repo and gets exit 1 (`intent_to_add=1`); `git diff
    --cached --name-only` alone prints nothing there, so a check built on it passes the round-35 mistake. Not
    covered: it detects index state after the fact; it does not prevent a forbidden git command.
104. QUALITY 102's check runs the registered gate `tools/mori-sources-appendonly.py` (SKILL.md Round36 registry
    row), not the round-35 wave script, which stays round-35 evidence. The gate also lists rows held earlier and
    absent at `<rev>` (`deleted=[...]`) and counts them as violations, closing 102's "Not covered: deleted rows".
    Check: `python3 tools/mori-sources-appendonly.py <tip> --round-base <entering tip>` exits 0 with
    `round_changed=[]`; `--selftest` exits 0. Lesson: `corpus/lessons/round-35-verifier-spotcheck.md` §6 items 2-3.
    Shown able to fail: the self-test's deletion history prints `deleted=[S###]` and exit 1; under count-c2.py the
    round-35 script and a no-deletion variant score `C2=unmet` (`.ufo/waves/round-36/evidence/c0-rescore-v2.txt`, J2
    and J5). Not covered: whether a superseding row's own content is right (rule 1's Gate check).
105. A freshness or drift witness is checked for what changed before it is used as a target: for every real row a
    counter counts as drifted, compare the source's full-document sha256 with the one recorded when the row was
    opened (the copy header or the lesson Gate), and count the row as a source change only when they differ. Lesson:
    `corpus/lessons/round-36.md` M1. Shown able to fail: round 36's frozen P-C1 required "at least one oracle-drifted
    row", and all seven real drifted rows were representation differences (S156–S160 annotated excerpts whose
    header sha256 equals the live body; S176/S177 build footers) (`.ufo/waves/round-36/w1/MineCopyFidelity.md`).
    Not covered: semantic drift of a page whose bytes never change.
105-addendum (measured 2026-10-23T16:2x-03: `python3 tools/mori-source-drift.py --root .` →
    `.ufo/waves/round-36/evidence/drift-live-r36.txt`): the drifted set is now nine rows — the criterion's seven plus
    S210 (post-copy stylesheet/script-integrity line; taught passage unchanged) and S211 (fetch-varying PMC page,
    rejected row; never `fresh`, so 105's sha comparison can never succeed for it — treat as a variance witness per
    the knowledge note). 105's "Not covered" clause names only semantic drift of a never-changing page; it also does
    not cover byte-unstable pages (the S211 class). For both, the recorded open-time sha256 105 requires is the
    committed copy's
    (`sha256sum corpus/evidence/sources-r36/<id>.src`: S210 64c60354…, S211 a4e104ec…); neither names a source change
    (w2/ExecDriftLive.md).
106. A measurement's discrimination claim is checked against an arm-detector, not only against a constant: for every
    counter with a published or fixed expected answer, a tool that behaves honestly on the hidden-truth arm and prints
    the published answer elsewhere must be rejected, and the receipt must show that rejection. Lesson:
    `corpus/lessons/round-37.md` M2 (r36 w2/RevNgC2 N1). Check: `python3 .ufo/waves/round-37/count-c1.py <tip>` runs
    `fixtures/memo-n1.py` (honest under `user.name == "mori counter"`, published constant and its `changed` lines
    elsewhere) and requires the `negative memo-n1.py` line to read `rejected` (the receipt prints it column-aligned: `negative memo-n1.py     rejected`); `C1=met` only when it does. Shown able to fail: the round-36
    counter scores that same fixture `C2=met`, exit 0 (`.ufo/waves/round-37/evidence/c1-before-memo.txt`), and a
    counter with no challenge arm leaves the fixture's real and blind arms passing. Not covered: a tool that detects
    the challenge's own parenthood or env (the challenge runs as a sibling child of the counter like the real arm).
107. A tool interface that requires per-id lines is checked on those lines, not only on its summary: a program that
    prints the correct summary lists and omits the per-id lines is rejected. Lesson: `corpus/lessons/round-37.md` M3
    (r36 w2/MutC2Deleted limit 3). Check: `python3 .ufo/waves/round-37/count-c1.py <tip>` parses
    `changed <id> superseded_by=<id|->` / `deleted <id>` against the hidden truth on every arm and requires
    `negative summary-only.py rejected`. Shown able to fail: the round-36 counter scores the same fixture `C2=met`,
    exit 0 (`.ufo/waves/round-37/evidence/c1-before-summary.txt`). Not covered: the `superseded_by` value itself is
    not compared, only the id set.

## Criteria added round 38 — round-37 M9 and ExecGateRound, ExecC1Seed43, LabTimeoutBoundary, SentTools

108. A corpus binding is checked for **resolvability**, not token presence: every `anchor:` line in the knowledge entry
    occurs byte-exactly in the named file at R, every path the capability row cites resolves from the repository root at
    R, and a live receipt's per-row lines enumerate exactly the rows its summary counts. Lesson: `corpus/lessons/round-37.md`
    M9; `corpus/lessons/round-38.md` M1–M2. Check: `python3 .ufo/waves/round-38/count-c4.py <rev>` prints the four checks
    and rejects the three witness fixtures under `.ufo/waves/round-38/fixtures/`. Shown able to fail: the round-37 counter
    scores the fabricated binding `C2=met` (`.ufo/waves/round-38/evidence/v3-token-control.txt`) while `count-c4.py`
    prints `C4=unmet` on the same sandbox (`evidence/c4-witness.txt`). Not covered: an anchor proves presence, not
    semantics (the `drift_kill` mutation arm is the separate statement); the capability check reads the last row
    containing the capability name.
109. A drawn-arm measurement is replayable only with the tip it drew from: the counter prints
    `head_at_measurement=<40-hex>` on every run, and a conformance check fails a counter that cannot print it, cannot
    resolve a repo-relative `--tool`, ignores its timeout budget, or keeps an unbounded read. Lesson: ExecC1Seed43
    R2/R4, LabTimeoutBoundary, SentTools MEDIUM/LOW; `corpus/lessons/round-38.md` M5. Check:
    `python3 .ufo/waves/round-38/conform.py --selftest` → `CONFORM_SELFTEST pass=6 fail=0`. Shown able to fail: the
    round-37 counters score `CONFORM=unmet` with all six checks FAIL (`.ufo/waves/round-38/evidence/c5-before.txt`);
    a counter whose budget flag is ignored fails `timeout_state` with a flush-then-hang tool. Not covered: the pin is
    HEAD, not the drawn rev (the receipt's `rev=`/`base=` name the drawn arm).
110. A supersede disposition is **timed**, not just present: an id is superseded-as-of only when its latest superseding
    row's landing commit postdates the id's last immutable-cell edit commit; presence alone leaves it in
    `stale_supersede`. Lesson: ExecGateRound D3; `corpus/lessons/round-38.md` M3. Check:
    `python3 tools/mori-sources-appendonly.py <rev> --round-base <base>` prints
    `supersede_timing superseded_as_of=[...] stale_supersede=[...]`; `--selftest` carries a supersede-before-edit
    fixture that lists the id in `stale_supersede`. Shown able to fail: at `e37dcc6` the field lists S069 in
    `stale_supersede` although the presence-based `superseded=[...]` had listed it as superseded since round 35
    (`.ufo/waves/round-38/evidence/gate-after.txt`); a gate whose field is presence-based lists S069 as-of. Not covered:
    commit order in the path's history, not global ancestry.
111. QUALITY 109's check command as printed (`conform.py --selftest`, no revision) exits 2 with `conformance setup
    error`; the runnable form is `python3 .ufo/waves/round-38/conform.py <rev> --selftest --counter
    .ufo/waves/round-38/count-c1.py` → `CONFORM_SELFTEST pass=6 fail=0`, exit 0. This row supersedes 109's check
    cell only; 109's criterion stands. Lesson: `corpus/lessons/round-38.md` M10. Shown able to fail: the bare
    `--selftest` invocation printed `conformance setup error: expected str, bytes or os.PathLike object, not
    NoneType`, exit 2 (`conform.py:266-270` requires `rev`); the runnable form printed `pass=6 fail=0`, exit 0.
    Not covered: the selftest mutates only the first `--counter`.
112. QUALITY 110's "Not covered" line is discharged by the round-39 gate: "postdates" and "descends from" are now the
    reachability relation (`git merge-base --is-ancestor` between the id's last edit commit and the superseding row's
    landing commit), the walk carries parent hashes with `--full-history`, and an edit is a change against the first
    parent's state, not the previous walk record. Lesson: `corpus/lessons/round-38.md` F1/F2 (resid/ResidGateTiming);
    source: S227. Check: `python3 tools/mori-sources-appendonly.py --selftest` → `pass=12 fail=0`;
    `python3 .ufo/waves/round-39/fixtures/run-c9-dags.py tools/mori-sources-appendonly.py <lane> <out>` prints
    `stale_supersede=[S001]` on fixture A, `round_changed=[]` exit 0 on fixture C, `superseded_as_of=[S001]` on
    fixture D. Shown able to fail: the round-38 gate bytes print `round_changed=[S001]` exit 1 on fixture C and
    `stale_supersede=[S001]` on fixture D where the predicate's words read as-of
    (`.ufo/waves/round-39/evidence/c9-red-a.txt`); the lane-history receipts are byte-identical to round 38
    (`evidence/c9-after-lane.txt`). Not covered: "latest superseding row" on two incomparable branches is still
    walk-order (r38 ResidGateTiming residual 2), and the last-edit attribution is walk-order when two incomparable
    commits edit the same id.
113. A registry row's located-quote correction rides a superseding row, never an in-place `anchor` edit: S228
    (`supersedes S226`) carries the corrected `:657-659` suffix the round-38 closure routed, because the gate's
    `anchor` cell is immutable. Lesson: `corpus/lessons/round-39.md` M20; routed defect r38 spotcheck §Routed 1.
    Check: `python3 tools/mori-sources-appendonly.py <r39-tip> --round-base <entering-tip>` lists S226 in
    `superseded_as_of` (S228's landing descends from S226's) and the census stays `ok` exit 0. Shown able to fail: an
    in-place anchor edit would appear in the gate's `ids=[...]` changed list with `appendonly_violations` ≥ 1; the
    pre-fix S226 row at the entering tip still prints the `:657-658` suffix (`corpus/SOURCES.md` at `13f3db7e`).
    Not covered: the round-38 fleet report's `:2` cite (fleet history, outside lane write scope; recorded in the
    round-39 report).
114. Every named checker-selftest survivor (a mutation a wave seat or closure report says survived, or a committed
    survivor fixture) enters a committed fixture under the round's wave tree, and the next checker version's selftest
    must kill it via an arm named for the survivor class; a cumulative ledger re-runs every committed survivor fixture
    against the newest conformance checker and reports any that still pass. Rationale: rounds r32–r41 each left a
    survivor for the next round to chase (considerthese/2026-10-24.md, "Keep a cumulative survivor ledger" proposal —
    operator-authored reflection, mined round 42; the r41 closure independently routed the same class as defect 1).
    Check: `python3 .ufo/waves/round-42/conform.py <rev> --repo <lane> --contract .ufo/waves/round-39/contract.md
    --counter .ufo/waves/round-41/fixtures/c1/count-c8.py --selftest` → `CONFORM_SELFTEST pass=17 fail=0`, with the
    three survivor arms (walrus-positive, tupleunpack-positive, source-order) each failing under exactly its own
    committed checker mutant. Shown able to fail: the v4 checker bytes print `pass=14 fail=0` with all three
    r41 mutants surviving (`evidence/control-c1-v4.txt`). Not covered: survivor classes no fixture names yet.
115. A frozen instrument's green control must replay with `--repo` pointing at a scratch clone, not only a hardcoded home path. A receipt that cannot be re-run off that path is weaker evidence. Rationale: considerthese/2026-10-24.md, "Check that frozen instruments replay off-host" (operator-authored reflection, mined round 43; not edited). The r40 `conform.py` hardcoded `LANE` is the pointer, not the evidence. Check: the round-43 green control runs `count-c1s.py <scratch-rev> --repo <scratch-clone>` and prints `C1S=met`. Shown able to fail: the same counter against the entering tip, where the successor file is absent, prints `C1S=unmet`. Not covered: instruments this round did not re-run.
116. An "unreachable" or "not fetchable" verdict must carry a full GET probe (status line, content-type and the first bytes or magic) for every candidate endpoint, not a HEAD probe alone. A HEAD-only probe cannot distinguish a mitigation page from an endpoint that rejects HEAD but serves GET, so the verdict is weaker than it reads. Rationale: the round-43 residual seat's S268 attack (`.ufo/waves/round-43/w1/ResCritS268.md`) — `curl -sI` returns HTTP 418 with `content-type: text/html` and content-length 15410, while the round-42 record shows the same endpoint serving a GET under other channels. Check: the refusal receipt records a GET probe. Shown able to fail: the round-43 receipt is a HEAD probe (`evidence/s268-headers.txt` records the `-I` response only), so the criterion does not yet hold for this round's own S268 refusal — the refusal stands on the absence of any committed PDF, not on the probe's completeness. Not covered: endpoints that need authentication or a session.

## Criteria added round 44 — the round-43 closure's three routed defects

117. A round's reported counts are reconciled by a committed ledger re-derived at the measured revision, not by
    re-reading the round's own prose. Lesson: `corpus/lessons/round-44.md`; round-43 closure routed defect 3 (two
    counts wrong: "15 checks" observed 14, "34 seat logs" observed 8). Rationale also cites
    `considerthese/2026-10-24.md` ("Reproduce headline numbers mechanically", operator-authored reflection, mined
    round 44 on 2026-10-25 — the general form had no artifact: `tools/mori-round41-calibration.py` is round-40-only
    and `.ufo/waves/round-44/figures.tsv` was absent at the entering tip). Check:
    `python3 .ufo/waves/round-44/count-c1.py <tip>` prints `C1=met mismatches=0` over a ledger of at least 12 rows
    covering at least 4 of the declared classes, each row one `git` pipeline naming `@REV@`. Shown able to fail: the
    witness fixture `.ufo/waves/round-44/fixtures/figures-r43.tsv` reproduces round-43's two figures and the counter
    prints `C1=unmet mismatches=2`, naming F03 (asserted 15, observed 14) and F04 (asserted 34, observed 8). Not
    covered: **the counter measures ledger well-formedness and arithmetic agreement, not informativeness** — a
    twelve-row ledger of revision-constant figures (`git diff @REV@ @REV@ | wc -l`, asserted 0) prints `C1=met`
    (`w1/ExecJunkLedger.md`), so `C1=met` never certifies that a row is a figure the report states. The tightening
    (a revision-sensitivity arm: every row's value must differ from its value at a second revision, or the row must
    be declared a constant) is routed to round 45; the frozen bytes are not amended.
118. A round-scoped measurement counter is a registered gate before it scores anything: eight non-empty standard
    cells in `SKILL.md`'s `## Gates` table, an entry path that resolves at the audited revision, and a `--selftest`
    over isolated fixtures whose `pass=/fail=` tally a committed mutant of that same counter flips. Lesson:
    `corpus/lessons/round-44.md`; round-43 closure routed defect 4 ("no `SKILL.md` registry row and no `--selftest`
    mode"). Check: `python3 .ufo/waves/round-44/count-c2.py <tip> --counter .ufo/waves/round-44/count-c1.py
    --counter .ufo/waves/round-44/count-c2.py --counter .ufo/waves/round-44/count-c3.py` prints `C2=met`, and
    `python3 tools/mori-gate-registry.py --rev <tip> --audit <path>` prints `REGISTRY=met` per row. Shown able to
    fail: at the entering tip the counters are absent (`C2=unmet`); the two round-43 counters audit `REGISTRY=unmet`
    (`.ufo/waves/round-44/evidence/witness-r43-gates.txt`); a mutant whose gutted check its own selftest cannot catch
    fails `mutant_kill`. Not covered: a row's *content* is checked for presence and by the round's reviewer, not
    machine-compared to the tool's behaviour; and the auditor's own selection rule is weak under crafted input — a
    duplicate row wins by shortest entry cell and flips the verdict, a row naming an absent path still registers a
    present target, and a nine-cell row passes (`w1/MutRegistry.md`). Gates landed before round 44 remain
    unregistered; the inventory is in the round report.
119. A receipt names the revision it measured, and the verdict names that same revision. Lesson:
    `corpus/lessons/round-44.md`; round-43 closure routed defect 5 (the C1S receipt was measured at `dde525ea` while
    the verdict cell said "at the landed tip"). Check: `head -3 .ufo/waves/round-44/evidence/c1s-tip-run.txt` names
    the revision the run measured, and every counter prints `rev=<full commit>` on its verdict path
    (`grep -L 'rev=' .ufo/waves/round-44/evidence/control-c*.txt` → empty). Shown able to fail: the round-43
    receipt header names `dde525ea4a7fca365e8ff2f3c486bccf28b94e52` while its verdict cell says "at the landed tip",
    which the round-43 closure had to reconcile by hand. Not covered: a tool that never prints its measured revision
    (most of the lane's older gates) is caught only by review, not by this check.

## Criteria added round 45 — the round-44 routed instrument defects, and one operator reflection

120. **A branch-presence check credits a flag only when the tool's own argv or case pattern
    handles it.** A comment, a docstring, a help string, or a subprocess list that runs *another*
    tool's flag is not a self-test branch. Lesson: `corpus/lessons/round-45.md` M1/M6; round-44
    routed defect 2 (`selftest_tally` and the comment-only pass). Rationale: the round-44 auditor
    credited `tools/mori-silence-cases.sh` from the comment `# ... (bash "$CENSUS", no --selftest)`,
    and a token grep over the whole population credited `tools/mori-routed-r24.py` from a
    subprocess list that invokes `mori-pressure.py --selftest` — so the class was undercounted by
    three (`routed-r24`, `disk-rate`, `round41-calibration`) as well as over-counted by one. Check:
    `python3 tools/mori-gate-registry.py --rev <tip> --audit-all` prints `no_selftest=0` over the
    derived population and prints `mode=population` (a `--audit <path>` narrowing must be refused).
    Shown able to fail: at the entering tip the same command prints
    `registered=29 unregistered=3 no_selftest=6 duplicate=0 wrong_row=0 tables=7` and its own
    selftest's `comment_only_selftest` arm goes red on a comment-only fixture. Not covered: the
    help-string (`add_argument("--verbose", help="see --selftest ...")`) and `selftest-flag=--help`
    escapes still pass — routed to round 46 (`w1/RevAudit.md` E4/E5).
121. **A write-scope cell separates observed behaviour from executed-input capability.** "This
    instrument's selftest writes only under the caller's `TMPDIR`" is a measured claim; "nothing
    else writes" is a capability claim about the input the instrument executes, and a cell that
    means the second must say so. Lesson: `corpus/lessons/round-45.md` M10; round-44 sentinel F8.
    Rationale: the round-45 sandbox arm measured all four round-44 cells true on their observed
    half (`writescope_mismatch=0`, repo tree unchanged, no write outside `TMPDIR`) while the same
    instruments execute committed ledger rows (`count-c1.py`) and a caller-named census program
    (`count-c3.py`), so the cells were false only in the capability half — and a reader relying on
    them reads the wrong half. Check:
    `TMPDIR=<lane>/.scratch python3 .ufo/waves/round-45/write-scope-run.py --rev <tip>` prints
    `WRITESCOPE=met instruments=7 true=<n> false=0 unavailable=0 writescope_mismatch=0` and the
    fixtures' `declared` cells are byte-diffs of the registry cells. Shown able to fail: the tooth
    control's declared-clean-but-writes-in-repo writer prints `verdict=FALSE ... first_outside=...`,
    `writescope_mismatch=1`, exit 1. Not covered: "stdout only" is consistent with, not proof of,
    no network write.
122. **A negative membership count names the corpus that can discharge it, and a census that
    publishes its own finding has discharged it.** Lesson: `corpus/lessons/round-45.md` M9;
    `considerthese/2026-10-24.md` proposal P24-3 (operator-authored reflection, mined 2026-10-25 —
    the proposal itself is not implemented and stays open). Rationale: "no receipt cites these
    three scratch files" was measured as 3 uncited at `7cb59c68` and 0 uncited at the tip, because
    the only tracked text naming them is round 44's own seat report listing them *as* uncited — the
    count's membership test let the finding discharge itself. Check: a census whose arm is "uncited"
    restricts `receipt` to `corpus/evidence/*` and `.ufo/waves/<round>/evidence/*`, excluding
    `w1/*` seat prose, and prints its population at two revisions. Shown able to fail: at `d72ac16`
    the same narrow definition prints 71 tracked / 40 uncited, at the tip 225 tracked / 0 uncited
    under the wide definition. Not covered: the narrower corpus is not yet built (this criterion is
    the admission, not the instrument).

## Criteria added round 47 — the round-46 routed counter defect, a stale pin, and a count the source refutes

123. **A registry pin is calibrated only when an instrument re-runs it from committed bytes and reads
    it from its own cell.** Lesson: `corpus/lessons/round-47.md` M1, M2; `considerthese/2026-10-25.md`
    suggestion 1 (operator-authored reflection, opened 2026-10-25). Rationale: round 46's counter
    matched needles anywhere in the row and turned green with the stale receipt still in the
    self-test cell (`corpus/lessons/round-46-verifier-spotcheck.md` routed defect 1); and
    `SKILL.md:912` pinned `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0` from round 40 to round 47
    while the committed tool printed `pass=22` from the round-41 freeze `d72ac167` on. Check:
    `python3 tools/mori-pin-check.py --rev <rev> --baseline-rev <entering>` exits 0 before a round
    that edits a registry row or a registered tool lands. Shown able to fail: at the round-47
    entering tip `2d85e33` it prints `PIN_CHECK=unmet … mismatches=1` (line 912), and the committed
    controls for a deleted row, a moved-cell receipt and a truncated pin each stay unmet
    (`.ufo/waves/round-47/evidence/control-c1-*.txt`). Not covered: line-count pins and truncated
    digests.
124. **A stated count of kernel objects carries the enumerating command over a pinned source.**
    Lesson: `corpus/lessons/round-47.md` M3. Rationale: the staged assimilation entry
    `oom-tracing-tracepoints-r42.md` headlined "exactly three named tracepoints" from a paper whose
    own sentence says "such as"; the v7.2 header defines eight (`grep -c '^TRACE_EVENT('` → 8).
    Check: "exactly N", "the N …" or "only" about kernel events, fields, files or knobs is admitted
    only with the command that enumerates them in the cited revision's bytes. Shown able to fail:
    `.ufo/waves/round-47/controls/control-c2-three.md` scores `name_mismatch=5` under
    `count-c2.py` at the freeze commit (`evidence/control-c2-three-at-freeze.txt`).

## Criteria added round 48 — hidden pins, junk next to honest edits, host paths, a located quote per claim

125. **A pin is calibrated only when the checker can see it, and it counts what it cannot see.**
    Lesson: `corpus/lessons/round-48.md` M2, M3. Rationale: the v2 checker printed `PIN_CHECK=met` on eight
    structural edits that leave a false tally in the registry — a header spelled `selftest`, a fullwidth or
    Cyrillic tally prefix, a fenced or blank-line-detached gate row, a tally on a continuation line or in another
    cell, a digest of a decoy file named elsewhere in the row (`.ufo/waves/round-48/evidence/control-c1-tool-v2-entering.txt`,
    `w1/CritJunkClasses.md`). Check: `python3 tools/mori-pin-check.py --rev <rev> --baseline-rev <entering>` has
    `hidden=0 unparsed=0`, and every digest binds to the nearest preceding in-tree path of its own cell. Shown able
    to fail: selftest arms `r2_hidden_row_outside_table`, `r9a_…`, `r9b_…`, `r9c_…`, `r10_…` and the frozen counter's
    J1–J8 under the entering tool (`junk_met=8`). Not covered: a row that names instrument A in its entry cell while
    its self-test cell runs instrument B (`w1/CritJunkClasses.md` D7).
126. **A calibration counter scores named junk edits and honest edits together, and the real registry is one of the
    honest cases.** Lesson: `corpus/lessons/round-48.md` M2. Rationale: round 47's frozen scorer was green on
    five junk edits and could not tell a repair from a pass; a counter that only wants `unmet` on junk is met by a
    tool that rejects every row. Check: `python3 .ufo/waves/round-48/count-c1.py --tool <tool> --rev <rev>` prints
    `junk_met=0 honest_unmet=0 real=met errors=0`, and the tool bytes contain no branch on a variant filename or a
    scratch directory name (`w1/CritC1Counter.md` F1 shows the harness leaks both). Shown able to fail:
    `controls/stub-always-met.py` (`junk_met=8`), `controls/stub-always-unmet.py` (`honest_unmet=4 real=unmet`),
    the entering tool (`junk_met=8`) — `evidence/control-c1-*.txt`.
127. **Instruments carry no absolute host path, and the count of those that do is stated with its scope.**
    Lesson: `corpus/lessons/round-48.md` Gate (considerthese item); `considerthese/2026-10-25.md` suggestion 2
    (operator-authored reflection, opened 2026-10-25). Rationale: the reflection's "13 files" reproduces only for
    the three `tools/` scripts plus ten top-level wave instruments of rounds 40–43; all tracked `.py`/`.sh` under
    `tools/` and `.ufo/waves/round-*/` give 395 at both `e5dbac05` and `2d85e33d`. Check:
    `git ls-tree -r --name-only <rev> -- tools/ | grep -E '\.(py|sh)$' | xargs git grep -l -F '/home/vgpnk' <rev> --`
    lists only files that predate the criterion (3 at `e5dbac05`), and a new instrument adds none. Shown able to
    fail: the same command run on `.ufo/waves/round-48/build-w1-spec.py` lists it. Not covered: older wave
    instruments (the 10 and the wider 395 are history, not repaired).
128. **A depth entry carries a located quote per claim, and the counter proves location, not entailment.**
    Lesson: `corpus/lessons/round-48.md` Gate, Wave 1 findings. Rationale: round 47's entry was checked by field
    and call-site names; a prose entry has no such handle, and `w1/CritC2Counter.md` shows eight fragments of
    page script text score `C2=met`, `w1/CritEntryRisk.md` six claim/quote pairs a reader rejects. Check:
    `python3 .ufo/waves/round-48/count-c2.py <rev>` is `met` and a reviewer re-opens every row against the page
    text around the quote (claim no stronger than the quote, no negation or example context, no other-filesystem
    or other-product page used as a Linux fact, no number from a comment). Shown able to fail: `C2_SELFTEST` arms
    `altered_quote_unmet`, `quote_from_wrong_copy_unmet`, `used_by_missing_unmet`; the do-nothing receipt
    `evidence/control-c2-donothing.txt`. Not covered: entailment, and script/JSON text inside a page.

## Criteria added round 49 — an opaque harness, rows a reader can see, bound pins, a dated reach, a flag that must land

129. **A scoring harness hands the tool under test only opaque names, and a tool that keys on the harness's own
    artifacts cannot pass.** Lesson: `corpus/lessons/round-49.md` M1. Rationale: round 48's counter passed a tool
    that never parsed the registry — it read `--skill`'s basename (`variant-J1.md`) and the per-variant `TMPDIR`
    (`c1-J1-…`) and returned red on J, green on H (`w1/CritC1Counter.md` F1). The successor names each copy and
    scratch directory by a sha256 prefix of its bytes (`s-<12 hex>.md`, `t-<12 hex>`), orders the runs by that
    hash, and builds its two fixture edits in a repository whose path and commit message carry no variant name.
    Check: the harness is read as well as run. `grep -n 'def opaque' .ufo/waves/round-49/count-c1.py` shows the
    sha256 handle, and `grep -n 's-%s.md\|"t-" + ' .ufo/waves/round-49/count-c1.py` shows the only two names
    handed to the tool; then `python3 .ufo/waves/round-49/count-c1.py` run with
    `--tool .ufo/waves/round-49/controls/stub-filename-sniffer.py` and `--rev <rev>` prints `junk_met=18` — the
    name-keyed stub cannot pass. Shown able to fail: the same sniffer
    prints `C1=met … variants=12` under the round-48 counter (`evidence/control-c1-sniffer-under-r48-counter.txt`)
    and `C1=unmet junk_met=18 … variants=26` here (`evidence/control-c1-stub-filename-sniffer.txt`). Not covered:
    content-keying — a tool may still special-case a literal the variants carry (`pass=999`), and the harness does
    not randomise the edits; the names stay opaque only while the variant bytes are unknown to the tool.

130. **A registry checker reads what a reader sees: any line that renders as, or is quoted as, a table row is a row
    for the hidden-pin scan.** Lesson: `corpus/lessons/round-49.md` M4; `.ufo/waves/round-48/w2/R48CritV3Junk1.md`
    §1-§8. Rationale: v3's hidden scan recognised a row only when it began with up to three spaces and a pipe, so a
    row inline in an HTML comment after a blank line, a tab-indented fenced row, a four-space row outside a table
    and HTML table markup each kept a false pin (`PIN_CHECK_SELFTEST pass=999 fail=0`) while the tool printed
    `PIN_CHECK=met` (§1, §3, §4, §8) — and R2 already made a plain fenced row fatal on exactly that reasoning.
    Check: `python3 .ufo/waves/round-49/count-c1.py --tool tools/mori-pin-check.py --rev <rev>` prints one
    `variant name=…` line per edit; the four lines matching `name=N[1347] ` read `expect=unmet got=unmet rc=1`, and
    the two matching `name=H[67] ` read `expect=met got=met rc=0` (the same shapes carrying no pin token are not
    flagged); the real registry's verdict line carries `hidden=0 unparsed=0`. Shown able to fail: the entering tool
    prints `got=met rc=0` for N1, N3, N4 and N7
    (`evidence/control-c1-tool-v3-entering.txt`, `junk_met=9`), and R11 alone leaves them met
    (`evidence/control-c1-tool-r48-r11-only.txt`, `junk_met=7`). Not covered: "renders" is the GFM rule as read,
    not a renderer's output; the adjacency repair makes honest prose that quotes a tally on the first line after a
    table `hidden` (cost on the real registry: 0 lines, `w2/R48CritV3Junk1.md` §1); a pin token laundered into
    another script (fullwidth, Cyrillic) is a different class.

131. **A row's pin is bound to the instrument its own cells claim, and two rows binding one command agree on its
    exit contract.** Lesson: `corpus/lessons/round-49.md` M4 and `corpus/lessons/round-48.md` M3 ("Not closed:
    D7"); `.ufo/waves/round-48/w2/R48ExecD7.md` §2, §6. Rationale: v3 related no cell to the argv it measured, so
    a row whose entry cell names the source-drift probe while its self-test cell runs the pin checker and pins that
    checker's true tally scored `PIN_CHECK=met` (`w2/R48ExecD7.md` §2), and a second row for an already-registered
    command with a contradicting verdict map scored `met` with `duplicate=0` (`w2/R48CritV3Junk1.md` §6). Check:
    `python3 .ufo/waves/round-49/count-c1.py --tool tools/mori-pin-check.py --rev <rev>` — the lines matching
    `name=(N[589]|H[67]) ` read N5, N8 and N9 `got=unmet rc=1` and H6, H7 `got=met rc=0`; the real registry's
    verdict line carries `misattributed=0 duplicate=0`. Shown able to fail: N8 and N9 print `got=met` under the
    entering tool (`evidence/control-c1-tool-v3-entering.txt`); with only the five surface rules N9 stays `met`
    (`junk_met=1`, `evidence/control-c1-tool-r48-surface-fixes.txt`), and with only R11 N5-N9 stay `met`
    (`junk_met=7`, `evidence/control-c1-tool-r48-r11-only.txt`) — each half is separately required. Not covered:
    the carve-out for a `fixtures/`/`mutants/` path carrying the claimed instrument's basename
    (`w2/R48ExecD7.md` §8) is what keeps three legitimate rows green and is a stated limit, not a closed class; a
    junk row that copies the authority row's contract verbatim is consistent by construction.

132. **A depth entry about a retention bound names the journal, and dates every number it takes from the host.**
    Lesson: `corpus/lessons/round-49.md` Gate (the C2 named limits). Rationale: the staged entries this round
    rewrote state one bound for "the journal" — the reach is "bounded by **size**, not by age", 258.3M
    against a 256M ceiling, in the staged
    `/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/journal-reach-at-ceiling-r46.md` —
    while the 2026-10-25 receipt prints two journals with two ceilings (`Runtime Journal … max 64M`,
    `System Journal … max 256M`) and a total that moved from 269M (2026-10-24,
    `corpus/knowledge/journal-disk-usage-total-r51.md:10`) to 56M in one day
    (`corpus/evidence/sources-r49/host-journal-reach.txt:2,5`). A reach number without its day is a fact about
    another day. Check: `grep -nE '/(var|run)/log/journal' corpus/knowledge/journal-reach-r49.md` names both
    journals, `grep -oE '[0-9]+(\.[0-9])?M' corpus/knowledge/journal-reach-r49.md | sort -u` is a subset of the
    receipt's `56M 19M 37M 256M 64M 8M 45M 210.9M` plus the dated 269M (S470) and the `50M` of a quoted vacuum command, and the entry carries `verified-at: 2026-10-25`;
    `python3 .ufo/waves/round-49/count-c2.py <rev>` is `met`. Shown able to fail: the staged r46/r45 entries carry
    `258.3M`, `250.3M` and `243.6M`, none of which is in the 2026-10-25 receipt, and the r46 entry gives one size
    bound where the receipt prints two ceilings. Not covered: a number that matches the receipt is not thereby
    true today (the receipt is one capture; 269M → 56M inside a day), and the check does not decide which journal
    a window spans — that is a reader's claim against the located quotes, which the counter locates but does not
    entail.

133. **A round counts the defects its critics flagged and whether the landing fixed them.** Lesson:
    `corpus/lessons/round-49.md` Gate (considerthese item; `considerthese/2026-10-25.md` suggestion 3, opened
    2026-10-25). Rationale: round 45's `w1/CritAxisHarm.md` §1b flagged four false `SKILL.md` registry cells
    (`:184`, `:190`, `:191`, `:194`) in the worktree before they were committed, and no round-45 commit fixed
    them: `18fd68b0` wrote the cells, `git diff --numstat 18fd68b0 baabc992 -- SKILL.md` prints nothing, and
    `:190` still pins `C1_SELFTEST pass=10` at `baabc992` — so the flag changed no outcome and nothing in the
    round graded it (`corpus/lessons/round-45-verifier-spotcheck.md:50-57` re-measures the same cells as harmed).
    Check:
    `python3 .ufo/waves/round-49/flagged-fixed/count-flagged.py` reads the round's defect list (one row per `## Findings` line of that round's
    `w1/Crit*.md` and `Rev*.md`), the landing diff and a re-run at the landing revision, and prints
    `flagged=N fixed=N unfixed=N` (round 48: `flagged=45 fixed=18 unfixed=9`, `na=18`; control with the freeze as landing: `fixed=0 unfixed=27`); the closure states the three numbers, and a defect counts FIXED only when the landing
    changes the named file/line or the defect no longer reproduces at the landing, UNFIXED when neither holds,
    NOT-APPLICABLE only with a stated reason. Shown able to fail: round 45 measures `flagged=4 fixed=0` against
    `baabc992` (cells `:184` and `:194` still pin `GATE_REGISTRY_SELFTEST pass=6`, `:190` still `pass=10` at
    `f80e75ac7421…`). Not covered: the script reads flags and diffs, not intent — a false flag counts like a true
    one (precision is not measured), and a defect fixed by an unrelated later edit counts FIXED.

## Criteria added round 50 — a self-assessment that is reconciled, a unit per line, a closure that is re-executed

134. **A round reconciles its own self-assessment with the fleet record and with the instruments, and every pin it
    corrects carries a committed receipt.** Lesson: `corpus/lessons/round-50.md` M1 (self-assessment drift).
    Rationale: `SHONEN.md` pinned `(60/60)` and `(13/13)` from round 48 on while the committed instruments printed
    `PIN_CHECK_SELFTEST pass=114 fail=0` and `UNLANDED_SELFTEST pass=17 fail=0`, and four `SCORECARD.md` `## Axes`
    Last change cells named rounds 26, 31, 31 and 25 while the fleet `MANIFEST.json` at
    `e014499613f63f8a467821219b0296121119ca53` graded rounds 47, 47, 49 and 49 `improved` — six mismatches at the
    entering tip `7197160b` (`evidence/control-c1-do-nothing.txt`); QUALITY 123 reads `SKILL.md`'s registry only
    ("A registry pin is calibrated only when an instrument re-runs it from committed bytes and reads it from its
    own cell", `:1028-1029`), so the lane's own self-assessment was outside every check. Check:
    `python3 .ufo/waves/round-50/count-c1.py <rev>` prints
    `C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0` and exits 0, and each pinned tally's
    observed line is committed under `.ufo/waves/round-50/evidence/selftests/<stem>.txt`. Shown able to fail: at
    `7197160b` the same command prints `C1=unmet items=8 axes=6 pins=2 boxes=4 mismatches=6 errors=0 hidden=0 …
    failed=mismatch` exit 1 (`evidence/control-c1-do-nothing.txt`); a corrected tally with no committed receipt
    stays unmet (`evidence/control-c1-pins-updated-no-receipt.txt`, `mismatches=6`); a blanket "every cell names
    round 49" edit stays unmet (`evidence/control-c1-all-latest.txt`, `mismatches=6`); deleting the pins fails the
    floor (`evidence/control-c1-pins-deleted.txt`, `pins=0`). Not covered: the Score column (the MANIFEST carries
    verdicts, not scores); the counter trusts the fleet MANIFEST instead of re-judging the closures; the
    Last-change convention itself is not scored; a tally pin outside `SHONEN.md` is not enumerated (`hidden` scans
    `SHONEN.md` only); and the counter's fleet revision is pinned, so a later closure moves the expected `round N`
    without moving this receipt.
135. **A memcg OOM report is read key by key with each line's own unit, and the cgroup's composition is taken from
    the stats block, never from the victim line.** Lesson: `corpus/lessons/round-50.md` Gate — the C2 named limits
    (the class is the rejected `scope-charge-fields-r46.md` hypothesis; `M1`–`M3` do not cover it). Rationale: the
    staged r46 entry reasoned from the victim's own growth — "a child that writes into `/tmp` consumes the scope's
    cap **without the victim process growing at all** — and the victim's own `anon-rss` would never show it" — a
    statement about the cgroup's composition drawn from a per-process line; and the report's numbers split three
    ways, the usage and swap lines and the `Killed process` fields in kB, the `Tasks state (memory values in
    pages)` table in pages, and the `Memory cgroup stats` block in bytes. Check:
    `for p in 'Units are per line' 'Read the block by key' 'charge, not the victim'; do printf '%s -> ' "$p";
    grep -c -- "$p" corpus/knowledge/oom-memcg-stat-r50.md; done` prints `Units are per line -> 1`,
    `Read the block by key -> 1`, `charge, not the victim -> 1`, and
    `awk '/^- Units are per line/,/^$/' corpus/knowledge/oom-memcg-stat-r50.md | grep -oE 'kB|bytes|pages' |
    sort -u` prints `bytes`, `kB`, `pages` — the anchors are the check, so an entry whose prose moves keeps its
    verdict (at `487941b9` the rules sat at `:46-48`, `:49`, `:56-58`; a same-day data correction moved two of
    them to `:52` and `:61`). Shown able to fail: the three greps over the rejected staged
    `/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/scope-charge-fields-r46.md` print `0`,
    `0`, `0` (exit 1), and over a copy of the landed entry with the units bullet deleted and the charge bullet
    reworded into a victim-property claim they print `0`, `1`, `0` — an entry that does infer composition
    (demonstrated in `.ufo/waves/round-50/a2w1/Mo50bScribeQuality.md` §5; no committed evidence receipt, so this
    arm is `not yet shown` as a file under `evidence/`). Not covered: the greps prove the rule is written, not
    that a reader follows it, and no counter reads prose (the round's C2 counter locates quotes and checks
    provenance); the `pg*`/`workingset_*` keys of memory.stat are event counts, not bytes, and the check does not
    test that; and the entry states what kernel v7.2 prints, not what any kill on this host printed (no MESSAGE
    read — lane rule).
136. **The round after a closure re-executes that closure's frozen counter at the revision the closure scored, and
    reports a divergence instead of smoothing it.** Lesson: `corpus/lessons/round-49.md` Gate ("Ruling:
    **verified** (evidence-verified, not re-executed)"); `considerthese/2026-10-26.md` suggestion 3 (operator
    reflection, opened 2026-10-26); `corpus/lessons/round-50.md` Gate (to be written). Rationale: the round-49
    ruling rests on committed receipts the integrator did not run, and the same closure records an "undocumented
    off-by-one (27 `variant` lines vs `variants=26`)" that only a re-execution settles — the counter's verdict
    line prints `len(results) - 1` (`.ufo/waves/round-49/count-c1.py:304-305`), counting out the `real` run, which
    is one of the 27 `variant` lines in both of the round's receipts; a reader holding only the receipt cannot tell
    a wrong line from a wrong closure. Round 50 re-ran its own counters at the landed revision with committed
    receipts (`evidence/a2-c1-at-data.txt`, `evidence/a2-c2-at-data.txt`; `a2w1/Mo50bExecC1Rerun.md` §1a). Check:
    `git show 64c2d5fc:tools/mori-pin-check.py > <scratch>/pin-check-at-64c2d5fc.py` then
    `python3 .ufo/waves/round-49/count-c1.py --tool <scratch>/pin-check-at-64c2d5fc.py --rev 64c2d5fc --scratch
    <scratch>/r49c1 --jobs 4 | grep '^C1='` compared with `grep '^C1='
    .ufo/waves/round-49/evidence/after-c1-at-tip.txt` — the two lines are equal and `diff` of them is empty, exit
    0, and the round's report quotes the re-executed line with its exit code. Shown able to fail: the same counter
    run with the v3 tool at `b3e3453d` prints `C1=unmet junk_met=9 honest_unmet=0 real=met errors=0 variants=26 rev=
    b3e3453d…` (`.ufo/waves/round-49/evidence/control-c1-tool-v3-entering.txt`), so a stale tool and a re-executed
    one are distinguishable by the verdict line; no committed receipt yet records a closure whose re-execution
    contradicts it, so the divergence arm is `not yet shown`. Run once for the agreement arm: 9m29s wall with
    `--jobs 4`, `C1=met … variants=26 rev=64c2d5fc…`, `diff` empty, and
    `python3 .ufo/waves/round-49/count-c2.py 24ebc799` printing the same `C2=met claims=21 located=21 …` line as
    `evidence/after-c2-at-24ebc799.txt`, `diff` empty
    (`.ufo/waves/round-50/a2w1/Mo50bScribeQuality.md` §5f). Not covered: a matching line proves the counter and
    the bytes are re-runnable at R, not that the counter's arms are good (its `--selftest` does that); the
    re-execution trusts the committed counter, so a counter edited after its freeze is not detected (that is
    `sha256sum -c evidence/freeze-sha256.txt`'s job); a closure scored at a revision no longer reachable from the
    lane's branches cannot be re-executed at all; and the C1 run costs minutes of CPU, so it is one check per
    round, not per seat.

## Criteria added round 51 — a re-execution outside the repo, a mismatch class, a runway reading, an entailment vote

137. **An instrument that re-executes pins runs on a tree outside the repo it reads, and the re-execution holds
    with that repo's path hidden.** Lesson: `corpus/lessons/round-51.md` M1 (hidden location dependence; the row
    is drafted this wave with `captured-by` QUALITY 127). Rationale: at the entering tip
    `tools/mori-pin-check.py`'s `--rev` mode exported the tree it measured under `<repo>/.scratch`, so a
    SIGKILLed run left 12,547 untracked or ignored paths in the repo it read
    (`C1=unmet kill_residue=12547 relocated=unmet reloc_mismatch=1`,
    `.ufo/waves/round-51/evidence/control-c1-do-nothing.txt`, exit 1); moving that export to TMPDIR removed the
    residue but left three pins failing outside the repo (`reloc_mismatch=3`,
    `.ufo/waves/round-51/evidence/control-c1-scratch-only.txt`, exit 1) because
    `.ufo/waves/round-49/count-c1.py` reads the `master` branch and `tools/mori-round19-regressions.py` reads git
    objects from the tree it runs in — a `git archive` export has neither. v5 checks out a `git clone --shared`
    of R under `--scratch`, else a TMPDIR outside the repo, else /var/tmp (v5.1 sets the tree's `master` to R and
    refuses a `--scratch` inside the repo; `tools/mori-pin-check.py` docstring v5/v5.1). Check:
    `python3 .ufo/waves/round-51/count-c1.py <rev>` exits 0 with
    `C1=met kill_residue=0 relocated=met reloc_mismatch=0`, where arm A starts
    `tools/mori-pin-check.py --rev R --repo C0` in a fresh `--no-local` clone C0 with TMPDIR in scratch, waits
    until it is writing, waits 3 s, SIGKILLs the process group, and counts
    `git -C C0 status --porcelain --ignored --untracked-files=all` lines; arm B runs in a second clone inside
    bubblewrap with `--tmpfs <lane>` and asserts `<lane>/SKILL.md` is absent. At the data commit `87e0c374` it
    printed `C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=119,fail=0
    rev=87e0c374… failed=-`, exit 0 (`.ufo/waves/round-51/evidence/c1-at-data.txt`). Shown able to fail: the two
    receipts above, `kill_residue=12547` and `reloc_mismatch=3`, each `C1=unmet` and exit 1. Not covered: arm A
    kills at one moment (3 s after the first write) and proves nothing about a kill at another; arm B hides one
    path and does not prove portability to another host, user or kernel; the counter's C0/C1 are `--no-local`
    clones but v5's own measured tree is `--shared`, so a repack or prune of the source repo during the run is
    untested; `--root` mode still writes `<root>/.scratch` and is not claimed; other lane instruments that write
    inside the lane (`.ufo/waves/round-39/conform.py`, round-48/49 `count-c1.py`) are outside this check
    (`.ufo/waves/round-51/w1/Mo51RevenScratchProducers.md`, `Mo51RevPromptConformance.md`).

138. **A pin mismatch carries a class that separates "could not run here" from "the pin is stale", and the
    summary counts both.** Lesson: `corpus/lessons/round-51.md` M1 — the hidden dependence surfaced as a bare
    mismatch; the class rule itself is `considerthese/2026-10-26.md` suggestion 1 (operator reflection, opened
    2026-10-26), not an M row. Rationale: at the entering tip a mismatch line read `state=mismatch …
    observed=None rc=2` and ended with no class (`.ufo/waves/round-51/evidence/control-c1-do-nothing.txt`; this
    seat reproduced that shape with the `aa3af1ec` tool on the frozen five-row fixture), so a pin that could not
    run and a pin that had drifted looked alike. v5 tags `class=env` when the pinned command printed no tally
    line for its prefix (setup error, missing path, timeout, OS error), `class=stale` when it ran and printed a
    different tally, a tally its exit code contradicts, or a digest/line-count difference, and its summary ends
    `env=N stale=N` with env + stale = mismatches (`tools/mori-pin-check.py:804-866`). Check:
    `python3 .ufo/waves/round-51/count-c1.py <rev>` prints `classified=ok` and five `classified:` lines —
    `ENVA_SELFTEST … class=env`, `ENVB_SELFTEST … class=env`, `STLA_SELFTEST … class=stale`,
    `STLB_SELFTEST … class=stale`, `OKAY_SELFTEST state=match` with no class — and a summary ending
    `env=2 stale=2`; at `87e0c374` the receipt's lines are those
    (`.ufo/waves/round-51/evidence/c1-at-data.txt`). Shown able to fail: a classifier that says env for
    everything prints `class=env` on the two stale rows and ends `env=4 stale=0`, with `classified=bad` and
    `C1=unmet` (`.ufo/waves/round-51/evidence/control-c1-always-env.txt`, exit 1); the class-only control is
    green on this arm (`classified=ok`) while residue and relocation still fail
    (`.ufo/waves/round-51/evidence/control-c1-class-only.txt`, exit 1), so the class alone is not the claim. Not
    covered: a tool that prints a tally and then dies for an environmental reason is classed stale (named in the
    contract; v5.1 narrowed the rest of `w1/Mo51CritClassRule.md`'s cases: an absent instrument file, disagreeing
    tally lines and a different tally before a timeout are stale, the pinned tally then a timeout is env, each
    with a selftest arm, `PIN_CHECK_SELFTEST pass=125 fail=0`); an ImportError of a repo-local module is env; every class observed so far is on a synthetic
    five-row registry — no real lane pin mismatched at the data commit; `--root` mode's classes are not claimed.

139. **A runway reading is read from `MemAvailable`, and no lane instrument or entry rebuilds it as the sum of
    free and cached memory.** Lesson: no round-51 M row covers this rule; the pointer is
    `corpus/knowledge/memavailable-estimate-r51.md` Reading rules, sourced by S496 (the 2014 commit says workload
    placers summed "free" and "cached" and calls that wrong because `Cached` includes shmem and tmpfs). Rationale:
    the fleet's hyaku gates read `MemAvailable` (fleet-owned `scripts/hyaku/`), and `tools/mori-census.sh:1792` reads the field itself
    (`mavail=$(meminfo_field MemAvailable)`), while a `MemFree + Cached` sum counts tmpfs and shmem pages the
    estimate does not add (entry rows 4, 7, 17, 20) — the reading the commit that introduced the line replaced.
    Check: `grep -n 'meminfo_field MemAvailable' tools/mori-census.sh` prints
    `1792:    mavail=$(meminfo_field MemAvailable)`; `grep -c 'never rebuild it as'
    corpus/knowledge/memavailable-estimate-r51.md` prints `1`; and
    `for p in 'MemFree[[:space:]]*\+' '\+[[:space:]]*MemFree'; do printf '%s -> ' "$p"; grep -rE "$p" tools/
    corpus/knowledge/ | grep -v 'never rebuild' | wc -l; done` prints `MemFree[[:space:]]*\+ -> 0` and
    `\+[[:space:]]*MemFree -> 0`. Shown able to fail: on a scratch copy of the entry whose bullet reads
    "rebuild it as `MemFree + Cached`" the same loop prints `1` for the first pattern and the rule count prints
    `0` (run in this seat's scratch; no committed receipt under `.ufo/waves/round-51/evidence/`, so the committed
    arm is `not yet shown`). Not covered: the greps prove no lane file spells the sum, not that every reading
    uses `MemAvailable` (a reading could use `MemTotal` or swap); row 2 legitimately names `MemFree` as an input
    of the kernel's formula, so the rule is about rebuilding the output, not about mentioning the input;
    `MemAvailable` is itself a model (entry rows 1 and 3), so a threshold on it is a threshold on an estimate;
    S116 (earlyoom) records a fallback guesstimate and is not covered by the grep.

140. **A depth claim carries a committed entailment vote for every row, and an `overclaim` vote blocks the row
    until its text is replaced.** Lesson: `corpus/lessons/round-50.md` M4 (an overclaim survived the counter),
    carried by `corpus/lessons/round-50-verifier-spotcheck.md` §5 item 4; no round-51 M row. Rationale: round
    50's depth counter met at `487941b9` with `claims=22 located=22` while wave a2w1 found six claims their quotes
    do not carry (M4) — location proves the quoted words exist, not that the claim follows. P-C2 adds: for every
    row, the report files committed at R under `.ufo/waves/round-51/w1/` whose names do not start `MoriR51` carry
    at least one line `ENTAIL <h> entailed` and no line `ENTAIL <h> overclaim`, where `<h>` is the first 12 hex
    digits of the sha256 of the row's claim cell with whitespace collapsed and ends stripped; `--hashes R` prints
    each `<h>` (`count-c2.py:117-133`). Check: `python3 .ufo/waves/round-51/count-c2.py <rev>` exits 0 and prints
    `C2=met claims=21 located=21 … entailed=21 dissent=0`, and
    `python3 .ufo/waves/round-51/count-c2.py --hashes <rev>` lists 21 row hashes equal to
    `.ufo/waves/round-51/evidence/c2-hashes-at-data.txt`. At the data commit the counter printed
    `C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok
    entailed=0 dissent=0 … failed=entailment`, exit 1 (`.ufo/waves/round-51/evidence/c2-at-data.txt`), and the
    same command reproduced that line in this seat's run. Shown able to fail: that receipt;
    `C2_SELFTEST pass=34 fail=0` (`.ufo/waves/round-51/evidence/selftest-c2.txt`) carries
    `entail_one_row_unreviewed_unmet`, `entail_dissent_unmet`, `entail_l1_file_ignored_unmet`,
    `entail_other_dir_ignored_unmet`, `entail_hash_of_other_text_unmet` and `entail_non_md_ignored_unmet`. Not
    covered: a vote records that a non-L1 seat asserted the judgment for that exact text, not that the judgment
    is right; the counter filters `MoriR51*` files by name and accepts any other `.md` under `w1/`, so it cannot
    tell an ENTAILMENT seat's vote from another seat's line, and it parses lines inside fenced blocks; one
    `entailed` vote meets the arm although the wave dispatches two seats per row; the hash covers the claim cell
    only, not the quote; an `overclaim` clears only when the claim text is replaced (new hash), never by deleting
    the vote.

## Criteria added round 52 — a living pin is current or superseded, and a self-assessment pointer lands on its words

141. **A command-tally pin in a living document (`corpus/QUALITY.md`, `corpus/README.md`) prints its tally when run
    today, or a later line supersedes it; the stale pin itself is never rewritten.** This row supersedes 112's check
    cell only; 112's criterion stands. Lesson: round-52 M1 (a living check pinned at one round's tally and never
    superseded), carried by `corpus/lessons/round-52.md`; round-51 closure §5 item 4 for the K4 scope.
    Rationale: 112's check pinned the gate's selftest at the round-39 count while
    the committed tool has printed 22 since the round-41 freeze `d72ac167` (QUALITY 123). Check:
    `python3 tools/mori-sources-appendonly.py --selftest` → `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0`, exit 0, run in a `git archive` of the tip with `TMPDIR` in scratch. Counter:
    `python3 .ufo/waves/round-52/count-c1.py <rev>` arm (C) lists every single-line pin in both files as good,
    superseded or a mismatch. Shown able to fail: at the entering tip `4f266ef2` the arm read three mismatches
    (`.ufo/waves/round-52/evidence/control-c1-do-nothing.txt`); rewriting a stale pin in place reads
    `pin_removed_or_rewritten`. Not covered: a pin split across lines or carrying a placeholder is not enumerated
    as a pin when it spans lines.
142. **A self-assessment pointer lands on the words it reports.** In `SCORECARD.md` `## Axes` and in the
    `SHONEN.md` boxes, a `path:N` pointer after a quoted string or a `proposed A → B` phrase names lines that hold
    that string or pair; every pointer names lines that exist. Lesson: round-52 M2 (a scorecard pointer named
    `:1771` for a pair that lives at `:1781`), carried by `corpus/lessons/round-52.md` and the round-51 closure
    D-c. Rationale: the freshness cell pointed round 28's
    proposed `5 → 6` at `SCORECARD.md:1771`, which holds the amendment A1 paragraph; the pair is at `:1781`.
    Check: `python3 .ufo/waves/round-52/count-c1.py <rev>` arm (D), `item locator … state=` lines. Shown able to
    fail: the entering tip reads `item locator SCORECARD.md:1771 expect=pair:5_→_6 got=absent state=mismatch`.
    Not covered: prose before a pointer other than a quoted string or a `proposed A → B` pair is checked for range
    only.

143. **A depth row needs two `entailed` votes from voters that did not write its text; an `overclaim` vote blocks the row until its text is replaced.** This row supersedes 140's "Not covered" text only; 140's criterion stands. Lesson: round-51 closure §5 item 2; round-52 M5 (the r51 arm took one vote, fenced lines and any .md). Check: `python3 .ufo/waves/round-52/count-c2.py <rev>` exits 0 and prints `C2=met … entailed=N dissent=0`; `C2_SELFTEST pass=45 fail=0` carries `entail_one_voter_unmet`, `entail_author_vote_not_counted_unmet`, `entail_fenced_votes_ignored_unmet`, `entail_non_voter_seat_ignored_unmet`. Shown able to fail: the data commit printed `failed=entailment` with `entailed=0` (`.ufo/waves/round-52/evidence/c2-at-data.txt`); row 3 had two overclaim votes and needed text replacement (lesson §Wave). Not covered: two files written by one seat look like two voters; a voter's REPLACE line is the only authorship signal.

## Criteria added round 53 — a release recheck answers a pin, a runway verdict names its mode and band, a scorecard row matches the receipt it cites, a report names its own commit

144. **An entry whose claim rows pin a tag and whose provenance line says `recheck: on-release` is answered by a
    recheck ledger once a newer tag exists: one row per claim hash, the counter-derived status, a quote located in
    the new tag's copy, a disposition, and two votes that did not propose that row's quote.** Lesson: round-53 C1
    (the round-51 and round-52 entries pin 46 of their 49 claim rows to v7.2 files and each carries one
    `recheck: on-release` line; `evidence/sweeps.txt:19` reads `refs/tags/v7.3^{}` → `c03c1a14507d…`, so the
    trigger fired with no answer in `corpus/knowledge`). Rationale: a `recheck: on-release` line is a promise the
    entry makes about itself; without a ledger the promise is prose, and a reader of the round-51/52 tables cannot
    tell a quote that still holds from one the release respelled. Check: `python3 .ufo/waves/round-53/count-c1.py
    <R>` exits 0 and prints `C1=met scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok
    provenance=ok … voted=46 dissent=0`; the ledger `corpus/knowledge/kernel-v7.3-recheck-r53.md` carries the same
    next-tag procedure on its own `recheck:` line (line 13), so the entry that answers one trigger states how the
    next is answered. At the data commit `2a4213bf` the counter printed `… voted=0 dissent=0 … failed=votes`,
    exit 1 (`.ufo/waves/round-53/evidence/c1-at-data.txt`) — rows and located quotes before votes. Shown able to
    fail: `.ufo/waves/round-53/evidence/control-c1-do-nothing.txt` (`rows=0 … pins=bad provenance=bad …
    failed=ledger_absent,pins`, exit 1); `control-c1-all-held.txt` (`status_ok=44 quote_ok=44 … failed=quote,status`)
    fails exactly the two `mm/mmap.c` rows whose quote v7.3 respelled to `vma_flags_set(&vma_flags,
    VMA_NORESERVE_BIT)`; `control-c1-v72-copies.txt` (`pins=bad … failed=pins,quote,status`) fails v7.2 bytes
    presented as v7.3; `control-c1-no-votes.txt` reproduces the data line. Not covered: `held` proves the v7.2
    quote's words still occur somewhere in the v7.3 file, not at the same place nor with the same meaning; the two
    `absent` rows carry disposition `holds` because the rule survived a respelling, so `holds=46 changed=0` must not
    be read as "no quote moved" (the entry title says "two quotes respelled"); 3 of the 49 rows cite the 2014 commit
    patch and are out of scope; D is the two entries' claim tables only — not `oom-tracepoints-r47.md`, the
    round-50 memcg entry, prose outside the tables, or the SOURCES anchors; the votes are lane seats, not outside
    verification; and the pins prove the copies are the bytes fetched from cgit, not that cgit served the tag.

145. **A runway verdict names the enforcement mode, and under mode 2 the error band that decides `COMMIT_LOW`; a
    band field that the verdict does not use is not the rule.** Lesson: round-53 C2 (the commit ledger moves from
    `corpus/knowledge/overcommit-commit-limit-r52.md` into `tools/mori-commit-runway.py`; the band is
    `mm_compute_batch` × present CPUs × page size, rows S511–S513). Rationale: one "commit headroom" number
    misleads in every mode — under mode 0 nothing below RAM + swap is refused, under mode 1 nothing is refused at
    all, and under mode 2 the enforced value is the global part of a per-CPU counter whose signed local deltas put
    it above or below the printed exact sum by up to one batch per CPU, so inside the band the printed figures do
    not decide the next request (wave correction: `w1/Mo53RevC2Counter.md` finding 1, `w1/Mo53ScribeSkill.md`). A tool that prints `band_kb` but
    declares `COMMIT_LOW` only below zero usable room is band-blind and its fields look honest. Check:
    `python3 -I -B tools/mori-commit-runway.py` prints one JSON object in which `mode` and `enforced` name the
    policy (host 2026-10-26: `"mode": 0, "enforced": false, "band_kb": null, "verdict": "COMMIT_HEURISTIC"`,
    exit 0), and under mode 2 `usable_kb` and `band_kb` are numbers; the frozen edge pair decides the rule —
    `mode2-band-edge-equal-is-low` prints `usable_kb 32768 = band_kb 32768`, `COMMIT_LOW`, exit 1, and
    `mode2-band-edge-one-page-above` prints `usable_kb 32772 > band_kb 32768`, `COMMIT_OK`, exit 0 (both cases
    materialised from `tools/fixtures/mori-commit-runway/cases.json` and run with `--meminfo --vm-dir
    --cpu-present --page-kb`); `python3 .ufo/waves/round-53/count-c2.py <R> --scratch DIR` exits 0 printing
    `C2=met tool=present selftest=pass n=31 fixtures=80 agree=80 disagree=0 registry=ok live=ok`. Shown able to
    fail: `control-c2-mode-blind.txt` (`agree=53 disagree=27`), `control-c2-no-band.txt` (`agree=71 disagree=9`,
    including `mode2-band-edge-low want=COMMIT_LOW got=COMMIT_OK`) and `control-c2-memoriser.txt` (`71/9`); all
    three print `selftest=pass n=12`, so the fixture arm and not the selftest is what separates them. Not covered:
    REF and the tool share one author, so a shared misreading of the kernel passes both; the band is an upper bound
    from the batch rule with present CPUs and totalram at read time, not a measured deviation; `COMMIT_LOW` is
    "inside the counter's own band", not a calibrated alarm (FR8 stays open); the live leg compares stable fields
    only, and on a mode-0 host — this one — the band fields are `null` live, so the mode-2 rule is exercised by
    fixtures alone; the tool reads no cgroup-level commit and sets no alert threshold.

146. **A SCORECARD row's numbers are the numbers of the receipt it cites.** Lesson: round-52 closure D2 — row
    `SCORECARD.md:2746` records `items=42 … locators=27` while citing `evidence/c1-at-landed.txt`, which prints
    `items=43 … locators=28`; the digits are verbatim from `evidence/c1-at-data.txt` measured at `8524904a`, so the
    citation anticipates the later receipt (the verdict is unaffected — both receipts print `C1=met …
    mismatches=0 errors=0`, rc 0). Rationale: a scorecard row is where a reader checks a round's arithmetic; a row
    whose citation names one receipt and whose digits come from another silently rewrites the round in the
    direction of whichever receipt the author last had open. Check: the loop below takes, for each tally key, the
    row's last occurrence and the `^C1=` line of the receipt named last in the row (the after-cell), and prints
    `ok|mismatch`:

    n=2746; row=$(sed -n "${n}p" SCORECARD.md)
    rec=$(printf '%s' "$row" | grep -o 'evidence/[a-z0-9-]*\.txt' | tail -1)
    for k in items locators; do
      a=$(printf '%s' "$row" | grep -o "$k=[0-9]*" | tail -1 | cut -d= -f2)
      b=$(grep -h '^C1=' ".ufo/waves/round-52/$rec" | grep -o "$k=[0-9]*" | tail -1 | cut -d= -f2)
      printf '%s row=%s receipt=%s %s\n' "$k" "$a" "$b" "$([ "$a" = "$b" ] && echo ok || echo mismatch)"
    done

    on the round-52 pair it prints `items row=42 receipt=43 mismatch` and `locators row=27 receipt=28 mismatch`,
    while the same row against `c1-at-data.txt` prints `row=42 receipt=42` and `row=27 receipt=27` — which names
    the attribution; for the round-53 row, `n=$(grep -n 'count-c1.py R' SCORECARD.md | tail -1 | cut -d: -f1)` and
    the receipt prefix `.ufo/waves/round-53/`. Shown able to fail: that reading, and the round-53 instantiation is
    the appended correction line the round-52 closure requires (routed defect 1). Not covered: only the keys the
    row displays are compared, so a count the row omits is unchecked; the receipt side is read at whatever bytes
    the tree holds, so an edit to the receipt after the row moves the comparison silently (no pin binds it); a row
    citing no `evidence/*.txt` path is skipped by the selector; the selector takes the last path in the cell, so a
    row naming its after-receipt before its before-receipt compares the wrong pair.

147. **A report names its own commit by command, never by a placeholder.** Lesson: round-52 closure D1 — the report
    carries `[FILL]` at line 5 (`… Report commit `[FILL]`.`), where its own commit hash belongs, and at line 46
    (`| `[FILL]` | receipts at landed tip: …`); the hash that exists is
    `aacd7a83027cdee8e950a2c39d490feaed3be13c` (`git log --format=%H -- .ufo/reports/round-52/mori.md` on the fleet
    repo). Rationale: a report is written before its own commit exists, so the commit cell is the one value the
    author cannot know while writing; a placeholder left there survives every later reading and makes the report
    unverifiable from its own text. The round-53 convention replaces it with the command that prints the value.
    Check: the report carries the literal command `git log --format=%H -- .ufo/reports/round-53/mori.md` where its
    own commit belongs (on the fleet repo the command prints one 40-hex hash once the report is committed), and `grep -nE 'Report commit `?\[FILL\]|^\| `\[FILL\]` \|' .ufo/reports/round-53/mori.md`
    prints nothing, rc 1. Shown able to fail: the same grep on `.ufo/reports/round-52/mori.md` prints
    `5:… Report commit `[FILL]`.` and `46:| `[FILL]` | receipts at landed tip: `c1-at-landed.txt`,
    `c2-at-landed.txt`, `census-end.txt` | Round 52 |`. Not covered: the grep matches the two positions round 52
    used (a metadata line and a commit-table row); a placeholder spelled `TBD`, `<hash>` or `pending`, or one placed
    in prose, is not matched; the positive arm holds only after the report is committed, so at writing time only the
    negative arm runs; the criterion binds the report to a commit that touched it, not to the commit the author
    intended.

148. **A SCORECARD claim row cites the receipt measured at the landed revision, never an intermediate one.** Lesson:
    `lessons/round-54.md#M1` — round-53 closure D2: the round-53 C1/C2 After cells cite `c1-at-salvage.txt` and
    `c2-at-salvage.txt` (R = `0df80303`), while the report measures `0b36d23e` (`c1-at-landed.txt`,
    `c2-at-landed.txt`); the round-50 C1/C2 rows repeat the pattern with `a2-c1-at-data.txt`/`a2-c2-at-data.txt`
    beside existing `*-at-landed.txt`. QUALITY 146 did not fire because the numbers matched. Check:
    `python3 .ufo/waves/round-54/checks/receipt-stage.py <rev>` flags every claim row of a `## Round N` section whose
    After cell cites `evidence/<x>-at-data.txt` or `<x>-at-salvage.txt` while `<x>-at-landed.txt` exists in that
    round's evidence directory and no later `Round-N correction` line names `<x>-at-landed`. Shown able to fail: at
    `39dcf4d7` it prints `flagged=5` (round 50 C1, C2; round 53 C1, C2 and the C2 cell's `c2-at-data` aside); after
    this round's appended corrections it prints `flagged=0`. Not covered: receipts named in another style
    (`after-c1.txt`, `c1-tip.txt`) are not classed as intermediate; a correction line is matched by name, not by
    content; rows before the `*-at-landed` naming (rounds ≤ 49) are out of its reach.

149. **A misroot relocation lands under the wave directory of the round that swept it, never at the lane root.**
    Lesson: `lessons/round-54.md#M2` — round-53 closure D3: seven round-27 seat fetches (`base.c`, `main.c`,
    `meminfo.c`, `oom_kill.c`, `sd-main.c`, `user@.service.in`, `MANPAGE.md`) were relocated by round 28 and one file
    (`0`) by round 38 "into the same relative path under the lane" — the lane root — and stayed tracked there for 26
    rounds. Check: `git ls-tree --name-only <rev>` lists at the lane root only the lane's own files and directories
    (`.gitignore .scratch .ufo AGENTS.md LOG.md MINT.md PROVINCE.md README.md SCORECARD.md SHONEN.md SKILL.md
    considerthese corpus tools`). Shown able to fail: at `39dcf4d7` it also lists `0 MANPAGE.md base.c main.c
    meminfo.c oom_kill.c sd-main.c user@.service.in`; at the round-54 data commit `1116c092` it lists none of them
    (`.ufo/waves/round-54/evidence/d3-relocation.txt`, byte-exact, `cmp` ok). Not covered: a misroot deeper in the
    tree (e.g. under `corpus/`) is not caught by a root listing; the allowed set is this round's list and must be
    amended when the lane adds a root file on purpose.

150. **A release recheck says where each quote now begins, not only that its words survive.** Lesson:
    `lessons/round-54.md` (round-53 named limit: `held` proves the words occur somewhere). Check:
    `python3 .ufo/waves/round-54/count-c1.py <rev>` requires each ledger row's `line` cell to be a line of the new
    copy on which the quote begins (`line_ok`). Shown able to fail: `evidence/control-c1-no-line.txt` — every row
    held, quoted and voted, lines blank — reads `line_ok=0 … failed=line`, exit 1. Not covered: the line proves place,
    not meaning (the votes carry meaning); a quote that occurs twice passes on either line.

151. **A death with no OOM record is not called unexplained until the memory-failure counters are read.** Lesson:
    `lessons/round-54.md` (C2, `knowledge/memory-failure-kills-r54.md`): the kernel kills for a hardware memory error
    outside the OOM path (SIGBUS/SIGKILL from `mm/memory-failure.c`), so OOM evidence alone cannot exclude a kernel
    kill. Check: a kill/death reading that reports "no cause" names the values of
    `/sys/devices/system/node/node*/memory_failure/total` and `HardwareCorrupted` it read (SKILL `## Round54`).
    Shown able to fail: the round-54 sweep at `39dcf4d7` finds no mori tool, SKILL row or PROVINCE line naming those
    surfaces (`.ufo/waves/round-54/evidence/sweeps.txt`), so any earlier "no cause" reading fails the check. Not
    covered: no tool enforces it yet (knowledge only); corrected errors (EDAC) are not counted by these surfaces.

152. **A census receipt is the command's captured bytes, not a retyped summary.** Lesson: `corpus/lessons/round-54-verifier-spotcheck.md` D1 — `census-end.txt` had spaces where the command emits tabs, no final newline, and a mistranscribed S349 URL. Check: run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` with stdout/stderr redirected directly to the receipt, then append the actual exit code; do not reconstruct its rows by hand. Shown able to fail: the r54 spot-check compared the saved bytes with a fresh run and found those byte-level differences. The r55 `evidence/census-end.txt` is a direct capture and ends `exit=0`. Not covered: whether the census validator itself classifies source rows correctly; this criterion checks receipt fidelity only.
