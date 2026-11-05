# Mo94Conn01 — read-only fleet sibling overlap scan (round-94 w1)

Seat: connector (leaf, read-only). Date 2026-11-05. Scope: all 21 sibling lanes `*-shokunin` except mori.
Axes touched: adjacency/coverage of C1 (R02 substring admission) and C2 (host home literal).
No repo edited; no sibling writes; no installs; no git/jj command run in any repo.

## Method (exact command lines, per lane L over the 21 siblings)

    grep -rInF -e ' in va' -e '[:7] in' -e 'in verified' --include='*.py' --include='*.sh' "$L/tools" "$L/.ufo/waves"
    grep -rInF '/home/vgpnk' --include='*.py' --include='*.sh' "$L/tools" "$L/.ufo/waves"
    grep -rInF -e ' in va' -e '[:7] in' -e 'in verified' --include='*.py' --include='*.sh' "$L/corpus" "$L/scripts"
    grep -rInF '/home/vgpnk' --include='*.py' --include='*.sh' "$L/corpus" "$L/scripts"
    grep -rInE '(^|[^A-Za-z0-9_])[A-Za-z0-9_]+(\[[0-9]+:[0-9]*\])? in (va([^A-Za-z0-9_]|$)|va_line|vline|verified_at|verified_line)' --include='*.py' --include='*.sh' "$L/tools" "$L/.ufo/waves"
    grep -rInE '\[[0-9]+:[0-9]*\] +in +' --include='*.py' --include='*.sh' "$L/tools"

Rows 1-2 are the seat-mandated patterns (a)/(b); rows 3-4 extend (a)/(b) to corpus+scripts; rows 5-6 are
supplementary refinements separating the R02 idiom from benign `in value` / `for … in verified:` iteration.

## Counts per lane (hits: A = pattern-a tools/waves; B = pattern-b tools/waves; CS = corpus+scripts A/B)

| lane | A tools | A waves | B tools | B waves | CS |
|---|---|---|---|---|---|
| audio | 0¹ | 0¹ | 0 | 0 | A=194 B=354 |
| chousa | 1 | 24 | 8 | 1117 | A=5 B=79 |
| game-dev-2d | 0¹ | 0¹ | 0 | 0 | A=30 B=155 |
| game-dev-3d | 0¹ | 0¹ | 0 | 0 | 0 0 |
| kagi | —² | 124 | —² | 67 | A=4 B=1 |
| kaidoku | 65³ | 234⁴ | 103 | 2631⁴ | B=2 |
| kake | —² | 2238 | —² | 1122 | A=25 |
| kama | 18 | 128 | 16 | 1417 | 0 0 |
| kasegi | —² | 11 | —² | 690 | A=6 B=37 |
| kengaku | —² | 843 | —² | 1193 | A=5 B=8 |
| kotoba | —² | 14 | —² | 547 | 0 0 |
| kotodama | 63 | 76 | 0⁵ | 482 | 0 0 |
| kumitate | —² | 1 | —² | 244 | B=2 (scripts/) |
| lore | —² | 36 | —² | 71 | A=1 |
| mado | 21 | 590 | 0 | 1696 | 0 0 |
| revenger | —² | 3 | —² | 131 | A=1 B=18 |
| souji | 13 | 44 | 14 | 677 | 0 0 |
| tabi | —² | 7 | —² | 371 | B=29 (corpus) |
| tameshi | 18 | 32 | 4 | 794 | 0 0 |
| tsukuroi | 31 | 127 | 11 | 713 | 0 0 |

¹ lane has no `tools/` and no `.ufo/waves/` (grep scanned nothing). ² directory absent in that lane.
³ includes 5 `in verified` hits (all `for item in verified:`). ⁴ kaidoku waves include archived
`arc3-loop1-round1..12` trees (A=23, B=679 of the wave totals) — frozen archive. ⁵ 18 further `/home/vgpnk`
hits in kotodama `tools/` are in non-py/sh files, all under `tools/gates/frozen/round-*/` (frozen receipts/outputs).
Raw counts are substring hits including benign matches; per-line classification below.

## First three hits per lane (path:line, relative to lane)

A live tools: chousa tools/inference-ground.py:578; kaidoku tools/round-26/recompute-ids.py:64,:219, tools/round-30/prefreeze-gate.py:110;
kama tools/gguf-identity.py:392,:398,:674; kotodama tools/gates/myth-consistency-gate.py:387,:658, tools/gates/lexicon-coverage-audit.py:599;
mado tools/mado-action-plan.py:231,:455, tools/mado-tripwire.py:1410; souji tools/souji-census.impl-34.sh:471, tools/impl-04.sh:553,
tools/souji-cert-evidence.py:254; tameshi tools/evidence-disposition.py:284,:286,:1764; tsukuroi tools/check-boot-writers.py:85,
tools/check-review-snapshots.py:23, tools/check-seat-bindings.py:30.
A frozen history (.ufo/waves/round-*): chousa round-31/falsify/MutC2Parse/run-detectors.py:108, round-33/w1/AuditC1Truth/replication.py:109,
round-33/gen-w2-spec.py:70; kagi round-26/frozen/release-clock.py:1389 (+rearmed/+round-27 copies); kaidoku arc3-loop1-round1/claims/c1/EX-09/reid.py:41 (+arc3 r2);
kake round-23/gen_w1.py:50, round-23/evaluability.py:52, round-24/measure_c2.py:109; kama round-11/reproduce.py:73, round-17/c1/mutants.py:127,
round-17/dispatch-provenance.py:407; kasegi round-36/build-spec.py:152, round-43/w1/ExecK19Freeze.sh:140, round-43/w1/ExecGateManifest.rules.py:114;
kengaku round-28/scratch/OpenTasks/pinned-evaluators.py:144,:166, round-28/scratch/OpenScorer/openscorer-evaluators.py:144; kotoba round-47/falsify/W2XmlFleetFP.repro.sh:22,
round-72/w1/build/ExecOC2/make_decoys.py:56, round-74/w1/build/ExecSibRowsDR74/derive_rows.py:110; kotodama round-66/stage/mut-o/mut1_no_partial_exit.py:330,:339,:364;
kumitate round-59/build/RevUsedBy/check.py:148; lore round-93/recovery/R10-key-scan.py:19,:32,:90; mado round-19/anchor-durability.py:355, round-20/tw-precision.py:110,
round-20/w2/AtkCasesS/mutant-R.py:1302; revenger round-67/quarantine/S092/check.py:23,:85, round-90/w1/ExecR90Replay/receipts/my_oracle.py:46;
souji round-22/attempt2/w1/evidence/impl-b/souji-declared-evidence.py:220, round-26/assimilation/validate/tools/souji-census.impl-34.sh:471, …/impl-04.sh:553;
tabi round-43/w1/ExecSentence/extract-three-site-identity.py:92,:97,:105; tameshi round-17/staged/tools/evidence-disposition.py:258,:260,:1645;
tsukuroi round-19/build/files/tools/check-boot-writers.py:85, round-21/drafts/ExecReview/check-review-snapshots-fixed.py:23, round-21/candidate/tools/check-source-scope-correction.py:163.
B live tools/scripts: chousa tools/quarantine-check.py:26,:40,:41 (+absent-split.py, research-gate.sh, freeze-check.py, build-spans.py);
kaidoku tools/round-27/c2-xpin-check.py:53-54, tools/round-28/c1-heldout-naming.py:48, tools/round-43/build-copies-r43.py (46 files total);
kama tools/echo-recheck.py:69, tools/round35-statement-audit.py:31, tools/round36-statement-audit.py:28; souji tools/souji-verify.impl-09.sh:23,
tools/souji-vault-verify.impl-24.sh:7,:71, tools/cand-s16-cert.py; tameshi tools/trace-inputs.py:26,:70, tools/cold-read-forecast.py:95;
tsukuroi tools/check-adjacency-anchors.py:28, tools/check-seat-bindings.py:16, tools/check-path-reconciliation.py:23; kumitate scripts/plan-before-ready.sh:87,:102.
B frozen history: chousa round-29/controls/CtlLabelKeyed/control.py:13; kagi round-24/tools/host-tripwire.sh:32, round-24/tools/identity-swap.py:36,
round-25/tools/c1-measure.sh:9; kaidoku arc3-loop1-round1/claims/c1/EX-14/manifest-gen.sh:3,:79,:101; kake round-23/gen_w1.py:6,:15,:19;
kama round-16/falsify/make_spec.py:5,:8,:20; kasegi round-23/c1-baseline-resolver.py:90, round-24/c1-baseline-resolver.py:109, round-25/assimilation/ids/guard-proof.sh:51;
kengaku round-28/scratch/FHistEvalTypes/census.py:18; kotoba round-49/build/c2-independent-indep.py:37,:38,:281; kotodama round-50/gen-build-spec.py:5,:13,:21;
kumitate round-51/build/MutInstrument/counter-probe.sh:15, round-59/build/RevUsedBy/check.py:16, round-59/build/RevS125Quote/strip.py:24;
lore round-93/deepseek/F08-probe.py:20, F09-evidence.py:18, F08-probe2.py:15; mado round-17/gen_w1.py:5,:7,:8; revenger round-65/build-wave-spec.py:7,:10,:13;
souji round-22/attempt2/w1/evidence/impl-gate/souji-gate-check.py:57; tabi round-19/run-final.py:20, round-20/run-checks.py:19, round-21/run-checks.py:18;
tameshi round-21/build-spec.py:6,:7,:9; tsukuroi round-18/measure/run.py:203, round-18/measure/repair.py:100,:101; corpus: audio corpus/live/r62-boundary/gen_variants.py:9-10
(BASE/OUT constants), tabi corpus 29, game-dev-2d corpus 155, chousa 79, kasegi 37, revenger 18, kengaku 8.

## R02 verdict (pattern a)

NO sibling live tool carries the mori R02 defect (short-hash tested as plain substring of a verified-at line).
Every live-tools A hit read benign: iteration over `value/values/variants/vals/verified`, char-class/escape checks,
prose. Refined idiom grep (row 5) returned 17 hits, ALL under `.ufo/waves/round-*` (frozen). Family-adjacent frozen
prefix-in-text tests, none a verified-at admission check:
- kake .ufo/waves/round-30/witness/witness_claim_receipt_backing.py:102 `full_hash[:7] in receipted`
- kama .ufo/waves/round-21/build/out/ErrataR20Omitted/verify-landed-omitted.py:79,:83 `token[:7] in ln`/`in measured`;
  SrcJjRebaseTimestamps/cutoff_check.py:59 `sha[:7] in section`; AuditReport19-6/probes.py:72 `h[:7] in landed`
- kotodama .ufo/waves/round-72/counters/accept-ca.py:206 `lands[:7] in report`
- kengaku .ufo/waves/round-29/scratch/R29ReviewEscaping/census5.py:56 `if tk in va:` — READ at source: `va` is a
  tuple-unpacked projected text value, not a verified-at line → benign (was the one plausible false-negative risk)
- kake quote-truth family rounds 56-60: `ROUND_DATE not in vline` — negated date test, not admission
Supplementary slice-`in` tools hits (row 6): kotodama tools/check-gate-quotes.py:122 `reference[1:] in HTML5_ENTITIES`;
tsukuroi tools/check-owed-statements-r29.py:352 `cid[9:] in where` — benign.
Reference idiom (contract P1, mori, frozen, observed): .ufo/waves/round-93/count-c1.py:141 `if ac and va and ac[:7] in va:`.
The C1 claim's mori-only scope remains correct; the frozen family-adjacent instances above are history, not live defects.

## C2 verdict (pattern b)

Seven siblings carry the same defect CLASS (host `/home/vgpnk` literal in live tooling): chousa, kaidoku, kama,
souji, tameshi, tsukuroi (tools/), kumitate (scripts/). Sharpest: kama's live counters tools/round58-c2-counter.py:67
and tools/round59-c2-counter.py:80 default `--fleet-repo` to `/home/vgpnk/Projects/shokunin` — the same class mori C2
forbids for its own round-94 counters. Per the seat spec, no fix is claimed or proposed for any sibling.
All wave/corpus/kotodama-gates-frozen hits are frozen history.

## Limits and contradictions

- Loose seat patterns over-match benign code (`in value`, `for item in verified:`); counts are raw hits,
  classified per-line by reading. kengaku `tk in va` initially looked like the R02 idiom; reading disproved it.
- Scan is of sibling working trees at 2026-11-05, not pinned to a revision; no git/jj ran in any sibling.
- corpus/scripts scanned with `--include='*.py' --include='*.sh'` only.
- NOT RUN: sibling corpus in non-py/sh formats; sibling wave files that are not .py/.sh; jj workspace states.
- No tool installs (system grep sufficient). Scratch `/fast/scratch/hyaku/mori-r94/Mo94Conn01` deleted before yield.
