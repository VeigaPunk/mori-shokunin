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
