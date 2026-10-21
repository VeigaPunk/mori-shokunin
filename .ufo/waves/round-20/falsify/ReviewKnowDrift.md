PARTIAL: the core numbers hold (shas, pinned_ts, post-pin, 50/8 entering, 49/7 pre-pin, 0 unclassified, STALE toggle). The doc is stale against the register at :30, one attribution is unsupported, two citation labels do not resolve, and four time/value claims have no stored receipt.

Scope: corpus/knowledge/drift-repin-r20.md at sha256 d2d16bfd…a44 (74 lines, mtime 08:11:34 -03). Earlier versions read: 476B (72 lines, "(S067)" at old :68) and 125ed4aa (08:05:15; +:11 verified-at, +:12 recheck). Register corpus/evidence/drift-classification-r20.json at sha256 10386a81…d9 (mtime 08:14:47 -03); it changed three times during review, and final checks ran on its final bytes. Receipts re-hashed unchanged: c1-drift-entering.json 91397955…, c1-drift-r10-prepin.txt e75ba1ee…, c1-drift-r20-postpin.txt 9b97c913…, baseline-r20 e528bc15…8433. Doc line numbers are current.
No census run, no edits, no installs, no subagents. Git read-only (cat-file, show, log, rev-list). Scratch in /tmp.

## Mismatches (doc, must fix)
1. :30 "census-schema-change 29, live-state 19, roster-change 2, census-regression 0" vs register .class_counts = 26/19/5/0 (per-token recount agrees). Register moved +SURFACE:lane.audio, +SURFACE:lane.game-dev-2d, +SURFACE:lane.game-dev-3d to roster-change. Reasons cite fleet 99efc52 "exclude the three Devin-owned lanes" (2026-10-15T01:52:09-03, subject verified) and db25a48 (2026-10-19T21:03:43-03). Lane contents of those commits not diffed [INFERENCE]. Update :30 to 26/19/5/0 or revert the register.
2. :37-38 "VolatileContract (H2/H3), C1Critic and the round-12 register argue census-regression" for -FINDING:WATCHDOG_STALE and WAVE_UNSETTLED_AGE. Supported for WAVE only.
   - STALE: build/C1Critic.md (31 lines) has 0 matches for watchdog|daemon|liveness|STALE; its falsifier is WAVE (:7, :32). corpus/evidence/drift-r12-20261019T2204Z-classification.md has 0 watchdog/STALE matches. Only build/VolatileContract.md K2 (:33) argues it.
   - WAVE: C1Critic.md:7,27,32 and r12 row :33 ("Yes—coverage/evidence-loss regression"). r12 :4 says "no token is a census regression".
   - Labels: build/VolatileContract.md has 0 matches for H2|H3|M2|M3. The arguments are K2 (:33) and K3 (:35); dissent at :13-15, :87, :121.
3. :74 "(VolatileContract M2/M3)" for CENSUS_RC / environment. Labels absent; the items are K10 (VolatileContract.md:49) and K11 (:51). The claim holds: run_pin (tools/mori-census.sh:2920-2938) never reads CENSUS_RC, which is set only at :2801.
4. :9 "the eleven Tok* seats": build/ holds 12 Tok*.md seat reports. The register cites 11 (all but TokPinFlap.md, mtime 10:42:03Z). Say twelve, or name the eleven.

## Values with no stored receipt
5. :57 "pre-pin drift 10:51:14Z": c1-drift-r10-prepin.txt has no timestamp; file mtime 10:53:07.386Z (completion). "10:51:14" and epoch 1792579874 appear nowhere in round-20 evidence/ or build/.
6. :56 "entering drift before 10:22Z": c1-drift-entering.json:6 says exact start "not recorded"; file written 10:22:34.8Z. Only support is build/TokIoAvg.md:84, itself [INFERENCE] ("about 10:18Z").
7. :58 "MORI_PIN: ok": no stored r20 pin stdout (pin-r10-…-pin.log exists for r10 only). The string is printed at tools/mori-census.sh:2936. "10:53:07Z" is census NOW (baseline-r20:3); the file was written 10:54:21.66Z (mtime), while :59 uses write time. Mixed conventions.
8. :62 "drifted 65 s later": no stored drift output (build/DraftDriftNote.md:18: "not stored in any file"). Source is L1 task text (.ufo/waves/round-20/wave1-run.json:578, "~65 s later"). Token set reproduced offline (build/TokPinFlap.md:8).

## Receipt reproducibility
9. c1-drift-r10-prepin.txt line 2 is "rc=1". Contract counting command on the file as stored gives r13 → 8, r20 → 1. On line 1 only it gives 7 and 0, as :57 states. Cite line 1, or note the rc line at :61.

## Verified exact
- Shas: census 87b8d680…ab28 (:3) = sha256sum tools/mori-census.sh = blob at measured commit 2061780 = HEAD. Last census commit fe9fa90 (2026-10-20 17:41:42 -03), so "unchanged this round" holds. baseline-r10 0993b235…0478 (:4-5) = BASELINE_SHA256 in pin-r10 log. baseline-r20 e528bc15…8433 (:6).
- pinned_ts 10:53:07Z (baseline-r20:3; :6, :58). Post-pin: postpin.txt:1-2 "MORI_DRIFT: none" / "rc=0"; mtime 10:55:31.565Z (:11, :59).
- Entering (c1-drift-entering.json:3,11,64): census sha, token_count 50, unclassified_count 8, rc 1. Register keys equal the entering token set (50/50, diff empty). Counting command: r13 → 8, r20 → 0.
- Pre-pin stdout: 49 tokens; only difference from entering is -FINDING:WATCHDOG_STALE; r13 → 7, r20 → 0 (:57).
- check-register.py on final register: entering stdout → "unclassified=0 invalid=0 regression=0 tokens=50" rc 0; pre-pin stdout → "tokens=49" rc 0. RegisterCheck.md:20 "unclassified=50 invalid=43" (r13) matches :21.
- r13 register: 42 keys; the 8 entering tokens absent match unclassified_vs_prior_register; 7 remain pre-pin.
- Standing warnings: WATCHDOG_ABSENT x1 (baseline-r20:53), WAVE_UNSETTLED_AGE x10 (:54-63), roll line :69 (:71).
- STALE toggle (:41-42): absent in entering; present in pre-pin. watchdog.log:584 = 07:18:05 -03 mori launch; last write :585 = 07:23:21 -03; idle at 10:51:14Z ~1673 s > 900.
- :40 "probes byte-identical since r10": probe_waves, probe_watchdog, drift_scan bodies identical between r10 census (commit 20e2255, sha d7710981 = baseline-r10:2) and HEAD (awk extract + diff: empty).
- :45-47 comparator limits: tools/mori-census.sh:2836 (words without "=" skipped, so first word only); :2839-2840 (duplicate keys concatenated). nvme0n1p1 new: baseline-r20:13 vs baseline-r10:12.
- Scratch pin 10:22:12Z (c1-pin-probe-scratch.json:3). mado commit 850b075, ct 1792578159 = 10:22:39Z (git) (:63). Row-A to row-6 (scratch:27 vs baseline-r20:27).
- :44 FR5 = PROVINCE.md:48, FR3 = PROVINCE.md:46. :22 QUALITY 65 = corpus/QUALITY.md:234-240. :49 F1/F3 = build/HistR13.md:28. :10 four Hist*. :70 S076 = corpus/lessons/round-20.md:50 (supersedes S067).
- :16 "Rounds 12-19 re-observed or carried" matches build/QualityCriteria.md:140 (own runs 12-15 and 20; carried 16-19). SCORECARD not opened.

## Adjacent (register, not doc)
- Register dissent still reads "VolatileContract (H2, H3) and C1Critic argue -FINDING:WATCHDOG_STALE ..." with the same unsupported STALE attribution as item 2.
- Earlier dissent "census code byte-identical since r10" is corrected in 10386a81 ("script as a whole changed in seven commits"). git rev-list --count 20e2255..HEAD -- tools/mori-census.sh = 7 confirms.

## Residual risk
- :74 "no MORI_* variables set" is unobservable. Times at :56-:58 and :62 rest on L1 notes only.
- Doc and register are still being edited. Re-run items 1 and 3 on final bytes before judging.
- Installs/updates: none.
