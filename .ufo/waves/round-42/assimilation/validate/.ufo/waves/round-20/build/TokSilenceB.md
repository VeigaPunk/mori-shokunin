# C1 token classification (TokSilenceB): basis, obs, +reason, +gate_s, -example

Scope: 5 of the 50 tokens in `.ufo/waves/round-20/evidence/c1-drift-entering.json` (stdout line 10; tokens array lines 13-62; measured_commit 2061780117e6; census sha256 87b8d680...). Read-only. `tools/mori-census.sh` was NOT run (not in my item). No tracked file edited, no mutating git command, no tool installed or updated.

## Result

All five tokens are **live-state**. For each, the emitting census text is the same at r10 (commit 5be8943, census d7710981...) and at HEAD (e4d9384, census 87b8d680...). Each token appears only because a lane row or a wave directory changed state on the host/fleet. None is census-schema-change, roster-change or census-regression, so none of the five blocks the C1 re-pin.

## JSON-ready table

```json
[
 {"token":"basis","class":"live-state","reason":"Six matched lane rows changed basis: aggregator row-B to row-A (new aggregator-shokunin subject commit); kama row-A to row-8 (launched 07:17:03 -03, inside the 7200 s gate); kumitate row-A to row-4 (round 38 completed 05:10:38 -03); kagi, kake, kengaku row-A to row-6 (round reports committed 07:07, 06:01, 05:54 -03). Row emitters unchanged since r3; the r17 rev change is inert for these rows (root rev equals HEAD).","evidence":"tools/mori-census.sh:2545 (basis=${GL_BASIS}); row sources :2363 row-4, :2377 row-8, :2410 row-6, :2472 row-A, :2493 row-B; r10 copy build/TokSilenceB/census-r10-5be8943.sh:1439; baseline lines 13-21 (basis=row-A, line 14 row-B); introduced 1439c47 (git log -S'basis=${GL_BASIS}'); live causes watchdog.log:583,579,543,558,541,390 and commits 1bcf59e,1eed508,4487889,9a28017,204807e; scratch pin .ufo/waves/round-20/evidence/c1-pin-probe-scratch.json (pinned_ts 2026-10-21T10:22:12Z) nine lane lines"},
 {"token":"obs","class":"live-state","reason":"WAVE_UNSETTLED_AGE id set went from 11 to 10 and shifted. aggregator-r10 and aggregator-r10-resume lost swarm-registry, dispatch and run files (directories now empty; dir mtime 2026-10-18 23:56:16 -03) after commit e20f4fa (2026-10-18 23:58:39 -03, operator sweep). shokunin-train-20261016-w24 is new and aged. Pairing by id shifts every obs value. probe_waves is byte-identical from r10 to HEAD, so this is not a census change; empty directories are not counted as unsettled by design.","evidence":"tools/mori-census.sh:424 (FINDING ... obs=$obs), :923 (wave=$base emit), probe_waves :865-932 (sha256 c34c3839... at r10 and HEAD); baseline lines 26-36 (11 WAVE lines); scratch pin lists 10 WAVE lines; git show --stat e20f4fa (17 stat lines match waves/aggregator-r10, both dirs); stat/ls of aggregator-r10 and aggregator-r10-resume; emitter introduced 7ca17b1 (git log -S'obs=$obs'); round-12 register corpus/evidence/drift-r12-20261019T2204Z-classification.md:33,39"},
 {"token":"+reason","class":"live-state","reason":"reason= now appears on five matched lanes in three row classes: row-8 kama (age_le_gate); row-4 kumitate (ledger-close); row-6 kagi, kake, kengaku (committed-report). The baseline has no reason= token at all. Emitter text unchanged since r3 and r4.","evidence":"tools/mori-census.sh:2364 (row-4), :2377 (row-8), :2411 (row-6); r10 copy build/TokSilenceB/census-r10-5be8943.sh:1312,1325,1340 identical text; baseline (no reason= token); introduced 1439c47 (git log -S'reason=committed-report') and 5b62c89 (git log -S'reason=ledger-close'); intent corpus/knowledge/silence-cutover-r3.md:43 (row 6) and :45 (row 8); scratch pin lines for those five lanes"},
 {"token":"+gate_s","class":"live-state","reason":"Only row-8 emits gate_s on a matched lane. kama was launched 07:17:03 -03, a few minutes before the census run (which started after 07:18:05 -03), and the gate is 7200 s, so kama is young. The LANE_SILENT finding that also carries gate_s is not emitted now. Emitter unchanged since r3.","evidence":"tools/mori-census.sh:2377 (gate_s=$LANE_SILENCE_S); :2525 (LANE_SILENT, not emitted); :360 default LANE_SILENCE_S 7200 (r10 copy :302); introduced 1439c47 (git log -S'gate_s' returns only 1439c47); intent corpus/knowledge/silence-cutover-r3.md:54 (gate_s= and basis=row-D added) and corpus/knowledge/silence-grading-r2.md:92; watchdog.log:583; scratch pin kama line"},
 {"token":"-example","class":"live-state","reason":"The row-B example= field left because aggregator is now row-A. Commit 1bcf59e (aggregator-shokunin, 2026-10-19 22:17:33 -03, on master, inside the (launch, NOW] window, passes the root pathspec) gives it a subject commit. The root is attached to master with no .jj and no lane.branch, so the r17 rev switch resolves to HEAD and is inert for this lane.","evidence":"tools/mori-census.sh:2494 (row-B GL_EXTRA example=$example), :2488 (assignment), :2790 (value mask only; key presence is not masked); baseline line 14 (basis=row-B rowb_files=<V> attribution=inference example=<V>); introduced 1439c47 (git log -S'example='); aggregator last launch watchdog.log:390 (2026-10-15T01:50:57-03); git show -s 1bcf59e; git symbolic-ref -q HEAD = refs/heads/master, .jj absent, git config --get lane.branch unset; scratch pin aggregator line (row-A)"}
]
```

Pipe form (same content):

token|class|reason
---|---|---
basis|live-state|six lane rows moved: aggregator B to A (commit 1bcf59e); kama A to 8 (launch 07:17:03 -03); kumitate A to 4 (round 38 closed); kagi, kake, kengaku A to 6 (reports committed)
obs|live-state|WAVE_UNSETTLED_AGE set 11 to 10: aggregator-r10 dirs lost markers (e20f4fa); w24 added; probe_waves unchanged
+reason|live-state|reason= on kama (row-8), kumitate (row-4), kagi/kake/kengaku (row-6); baseline has none
+gate_s|live-state|row-8 kama only (launch 07:17:03 -03, gate 7200 s)
-example|live-state|aggregator row-B to row-A (commit 1bcf59e); row-B fields gone

## Per-token evidence

- **basis.** Emitted at tools/mori-census.sh:2545 for every SURFACE lane row. Baseline (corpus/evidence/baseline-r10-20261015T2231Z.json) lines 13-21 carry basis=row-A for protocol, kasegi, kengaku, kake, kumitate, kotoba, kagi, kama, and basis=row-B for aggregator (line 14). In the scratch pin at 10:22:12Z the nine lanes read: protocol, kasegi, kotoba row-A (unchanged); aggregator row-A; kengaku, kake, kagi row-6; kumitate row-4 with age_s=-; kama row-8. Nine-lane comparison: 12 changed lines (six lanes, two lines each).
- **obs.** Emitted at :424 (every FINDING) and :923 (WAVE_UNSETTLED_AGE). Baseline lines 24-25 hold WATCHDOG_STALE and WATCHDOG_ABSENT obs; lines 26-36 hold the 11 WAVE obs values; lines 37-38 the journal obs. Only the WAVE pairs changed: WATCHDOG_ABSENT still reads obs=no (verified in the scratch pin). The base-only WAVE lines are aggregator-r10 and aggregator-r10-resume. The current-only WAVE line is shokunin-train-20261016-w24. The aggregator-r10 directories now hold no swarm-registry.json, dispatch.json or run.json. Their mtime is 2026-10-18 23:56:16 -03, about two minutes before e20f4fa (23:58:39 -03), which removed 17 stat lines under the two aggregator wave directories. shokunin-train-20261013-w5 is closed in its swarm-registry.json ("closed": true), so it is not counted; it is not in the baseline either.
- **+reason.** New on lines whose row emits reason=. :2364 is row-4 (reason=ledger-close round=...), :2377 is row-8 (reason=age_le_gate gate_s=...), :2411 is row-6 (reason=committed-report round=... path=...). Baseline contains no reason= at all, so every +reason is new. Introduced 1439c47 (round-3, silence cutover); intent at corpus/knowledge/silence-cutover-r3.md:43 (row 6 closed by committed report) and :45 (row 8 young).
- **+gate_s.** Only :2377 emits it on a lane row. :2525 (LANE_SILENT) is not emitted now and was not in the baseline. The gate default is 7200 (:360; r10 :302; silence-grading-r2.md:92). Introduced 1439c47 (single git log -S hit). kama is the only row-8 lane among the nine baseline lanes; tabi and mori are also young but are new lanes, so they appear only as +SURFACE tokens.
- **-example.** The example= key exists only on the row-B line (:2494, assignment :2488). Baseline line 14 carries it. The aggregator is now row-A (scratch pin), so the key is gone. Introduced 1439c47 (git log -S'example=' also shows 5be8943, which only touched the volatile list).

## Comparison with the round-13 register (.ufo/waves/round-13/evidence/drift-classification.json)

- Lines 27 (+gate_s), 28 (+reason), 40 (-example), 45 (basis), 46 (obs) each read "[INFERENCE] current watchdog/wave/lane activity or finding context; no re-pin/admission claim".
- **Agree** on the class: all five are activity or fleet state, not census change.
- **Disagree** on the evidence status. At r20 each token has an observed commit, ledger line or directory fact (listed above). The [INFERENCE] label is outside the closed set and gives no pointer, which the C1 contract requires.
- The round-12 register (corpus/evidence/drift-r12-20261019T2204Z-classification.md:35,36,38,39) gives the same causes for basis, obs and -example (aggregator wave-ID loss, row-B to row-C). Its "Yes" marks mean weakened fleet evidence, not a census defect. Its line 33 labels the WAVE loss "Yes, coverage/evidence-loss regression"; I disagree with the census-regression reading for the reason in the next paragraph.
- [judgment] I do not classify the WAVE loss as census-regression. probe_waves is byte-identical since r10, and its rule is designed: a directory with no registry, dispatch or run marker is "empty", not "unsettled" (:917-928 and the comment at :862-864). The census never saw those markers, and a commit (e20f4fa) removed them. It is a pre-existing coverage gap, not an unintended behavior change.

## Why not census-schema-change or census-regression

- Emitter text is identical in r10 and HEAD for: the row-4, row-6 and row-8 reason strings, the row-B example string, the basis= field, and the FINDING obs= format (r10 copy :359, :1312, :1325, :1340, :1401, :1439).
- Function bodies are sha256-identical r10 to HEAD for probe_waves, ledger_anchor and probe_watchdog. grade_lane differs by the r17 additions (branch gate, HEAD-vs-branch probe, committer diagnostic), the rev and root_rev choice, the pathspec placement, the git_cap hardening and an awk restructuring; ps_report_closed differs only by its rev argument. The row-4, row-8 and row-6 decision branches and all reason strings are unchanged.
- The r17 rev change (refs/heads/<branch>, per corpus/knowledge/jj-branch-anchor-r17.md:15-19) is inert for all five tokens: root is attached to master (rev equals HEAD), row-4 and row-8 decide before any rev read, and row-6 uses the root rev. The six jj child repos (kagi, kake, kengaku, kumitate, kama, kasegi: .jj present, lane.branch=master, HEAD detached) now read refs/heads/master for rows A to D. No row-A to D token moved for them, and kasegi and kotoba are unchanged.

## Cross-check of the lane reconstruction (not a census run) [INFERENCE from code and host state, corroborated by the scratch pin]

- Lane-row changes reproduce the receipt's token families. subject_commits and window are removed on kengaku, kake, kagi, kumitate, kama and added on aggregator. rowb_files, attribution and example are removed on aggregator. reason, gate_s and basis change as listed.
- Three bare or added tokens outside my five also follow from the same rows. `age_s`: row-4 returns before GL_AGE is set (:2362-2375), so it prints age_s=- (scratch pin: "age_s=- basis=row-4"). `round`: row-4 and row-6 emit a second round= key (:2364, :2411), and drift_scan concatenates duplicate keys (:2840). `+path`: row-6 emits path= (:2411). These are r3 emitters, not regressions, so they belong in the L1 register as the same live-state family.
- The HEADER token is census-r5 to census-r6 (VERSION at :281, introduced 18d7d55, round 13). That is census-schema-change, consistent with the round-13 register's "intentional journal schema/version/mask change".

## Limits

- The census NOW of the entering run is not recorded. The receipt says the job ran after the 07:18:05 -03 launch. kagi's row-6 holds only while NOW is before its round-25 launch at 07:23:21 -03 (watchdog.log:585). The scratch pin at 10:22:12Z (07:22:12 -03) shows the same states, so the window is covered. [INFERENCE]
- No census was executed. Lane rows are reconstructed from HEAD code plus host state, and the scratch pin (census sha 87b8d680...) corroborates them line by line.
- The exact WAVE set at the entering run is not recorded. I used the scratch pin (10 lines) and the receipt's single -FINDING:WAVE_UNSETTLED_AGE token (count fell below 11).

## Verification performed

1. `sha256sum tools/mori-census.sh` = 87b8d680... (equals the receipt). `git show 5be8943:tools/mori-census.sh | sha256sum` = d7710981... (equals the baseline header). `git log --oneline -n 1 -- tools/mori-census.sh` = fe9fa90, an ancestor of the measured commit.
2. Function body comparison r10 vs HEAD (awk extraction, sha256): probe_waves, ledger_anchor, probe_watchdog identical; grade_lane and ps_report_closed diffs saved under build/TokSilenceB/.
3. `git log -S` on: gate_s, age_le_gate, GL_BASIS row-8, example=, rowb_files=, reason=committed-report, reason=ledger-close, WAVE_UNSETTLED_AGE, WATCHDOG_ABSENT, obs=$obs, basis=${GL_BASIS}, census-r6.
3b. `git show 1439c47 -- tools/mori-census.sh` (round-3 silence cutover, 2026-10-15 14:25:51 -03, before the r10 pin) adds these exact emitter lines: row-4 `reason=ledger-close`, row-8 `reason=age_le_gate gate_s=`, row-6 `reason=committed-report path=`, row-B `rowb_files= attribution=inference example=`, LANE_SILENT `gate_s= basis=row-D`, and the SURFACE line `basis=${GL_BASIS}`.
4. Commits (read-only git show, log, cat-file): 1bcf59e (2026-10-19 22:17:33 -03, aggregator-shokunin); 1eed508 (kagi r24 report, 07:07:09 -03); 4487889 (kake r23, 06:01:39); 9a28017 (kengaku r26, 05:54:27); 204807e (kumitate r38, 05:09:07); e20f4fa (souji, operator sweep, 2026-10-18 23:58:39 -03). Root: symbolic-ref refs/heads/master, no .jj, lane.branch unset. Child jj repos: .jj present, lane.branch=master, refs/heads/master resolves.
5. Ledger (read-only grep of .ufo/watchdog.log): lines 390 (aggregator launch), 541 (kengaku), 543 (kagi), 558 (kake), 561 and 579 (kumitate launch and complete), 583 (kama), 585 (kagi, after the run).
6. Wave directories (read-only find, stat, grep): markers, JSON closed flags, newest mtimes.
7. Scratch pin c1-pin-probe-scratch.json: nine lane lines, 10 WAVE lines, census-r6 header.

Not run: tools/mori-census.sh, builds, tests, formatters.

## Notes for the L1

- None of the five needs a census edit or blocks the re-pin. [judgment]
- The WAVE marker blind spot (a dispatched wave whose markers are deleted becomes invisible) is pre-existing since r1. A knowledge note would record it. [judgment]
- Written under build/TokSilenceB/: census-r10-5be8943.sh (copy of git show), census-r10-to-head.diff, grade_lane.{r10,head}.txt, ps_report_closed.{r10,head}.txt.
- Tooling: none installed or updated.
