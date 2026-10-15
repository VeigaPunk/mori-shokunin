# Round 11 capstone audit — evidence integrity is not complete conformance

Seat: `audit-note-writer`; selected round axis: **calibration — deep discernment**.
Audited delivery: `d1e0dd90e6042723617fc75cdfb1987684d21ce4` (Round 10 records).
Measurements: 2026-10-15, during the Round 11 audit. This is a finding and readiness
assessment, not the parent's admission act and not a non-author promotion review.

**Conclusion: defect.** The nine rounds have a real, intact implementation and
receipt chain, and the four re-execution groups below have been exercised at today's
bytes. A claim that *every* admitted evidence chain is fully conformant is not
supported: current production authorship can misgrade, the oracle accepts a corrupt
verdict word, active recipes cite an absent baseline, and several process/evidence
claims need correction. No defect was fixed during this audit.

Evidence strength below means:

- **Direct**: command executed, bytes compared, or source/record quoted at a named revision.
- **Bounded**: a preserved historical receipt or finite witness supports the stated,
  limited result; it does not establish universal correctness or replay a past host.
- **Unrecoverable input**: the original material is absent from the delivery; a later
  substitute cannot verify the original experiment.

The relevant binding rules are the shokunin protocol's evidence standard,
commit-before-report and append-only correction clauses, four-value axis verdicts,
and named non-author SHONEN gate. Historical records are retained, not rewritten here.

## 1. Measured coverage and byte anchors

| Checked universe | Observed coverage | Method and limitation |
|---|---|---|
| Admitted goal-wave rounds 2–10 | 9/9 reports and ledger sections read | `.ufo/reports/round-{2..10}/mori-goalwave.md`, all SCORECARD verdicts and LOG entries; not a claim that every sentence is correct |
| Supplied evidence/records anchors | 17/17 distinct commits resolve, are ancestors, and carry `mori-shokunin <mori@shokunin.local>` | `git rev-parse --verify <ref>^{commit}`, `git merge-base --is-ancestor <ref> HEAD`, `git show -s --format='%an <%ae>' <ref>`; ancestry exits all 0 |
| Historical goal-wave report bytes | 9/9 equal their records-commit versions | `git show <records>:<report>` compared byte-for-byte to the current file |
| Indexed round-2–10 receipt logs | 50/50 SHA-256 values match the evidence index; 50/50 equal their evidence-commit bytes | Counts by round: 3, 5, 5, 6, 7, 7, 7, 5, 5; baseline is additional, not a receipt log |
| Current tools and adopted baseline | 3/3 match the delivered pins below | Whole-file SHA-256, also compared with `git show 5be8943:<path>` |
| Canonical per-axis admission rows | 54/54 present; 9/9 have at least one exact `improved`, zero `harmed` | 22 `improved`, 23 `unchanged`, **9 non-enum `improved narrowly`**; arithmetic is supported, vocabulary conformance is defective |
| Append-only LOG history | 21/21 revisions checked; 0 prefix violations | For each `git log --reverse --format=%H -- LOG.md` revision, next bytes start with previous bytes |
| Corpus inventory before this note | 13 knowledge notes, 9 pre-r11 lessons | `Path('corpus/knowledge').glob('*.md')`; analogous lesson count excluding the new r11 lesson; inventory is not universal claim verification |
| Fresh re-execution selection | 4/4 groups exercised | Section 3; a failed boundary probe is retained, not counted green |

The evidence tree contains 56 files. The receipt-integrity auditor enumerated 275
unique full SHA-256 tokens in 917 occurrences, including 140 historical fixture
fingerprints whose source trees are not preserved. This writer independently checked
the complete 50-log delivery/index universe, the current baseline and all supplied
round tool pins; **50/50 is not 275/275**. The wider auditor's reconstructed-hash
classification is not substituted for a fresh replay of absent input trees.

```text
HEAD d1e0dd90e6042723617fc75cdfb1987684d21ce4
d7710981aa1c7571ff9d6fd7f75822811173010e5f4e298ac3c47fab274a0b20  tools/mori-census.sh
448f77238c73a5c929a898dad0f0c495fd2a66cc4b90a00ae84ede69a86beeb5  tools/mori-silence-cases.sh
0993b23505deab2aeb05b2309bdf7dd6eaad2b82f27852491352511aa9670478  corpus/evidence/baseline-r10-20261015T2231Z.json
RECEIPT_HASH_TOTAL 50 / 50
RECEIPTS_CURRENT_EQUAL_EVIDENCE_COMMIT=50/50
LOG_REVISIONS=21
LOG_PREFIX_VIOLATIONS=0
```

### Round-by-round chain disposition

“Supported” in this table refers to the bounded technical claim, not an erasure of
the defects in section 4 or a retrospective replacement of an admission decision.

| Claim checked | Verdict | Evidence and evidence strength |
|---|---|---|
| r2 oracle reconciliation produces an honest failing gradient, not a passing cutover | supported | `3da8414970382c1690f7a8b020b75c2def6eaba5`: oracle `505a7504…`, census `e3073a2b…`; 3 watch receipts hash/commit-equal; authorship block re-extracted at `9c91e0a0…`, rerun 10/10. Historical 10/27 is explicitly not all-pass. Direct bytes plus bounded receipt |
| r3 silence cutover, two matcher defects distinguished from census behavior | supported | Evidence `1439c473ba2108dba6423566ade1c56c232c4eec`, records `bbcc1adcefd95f212dcab5dc8b2c39e41b111e63`; census `fe22a14f…`; 5 receipts equal. Frozen matcher vs current census still gives exactly 25/27; matcher-only scratch replacement gives 27/27. Direct replay |
| r4 matcher/state-walk/close-tracking changes and case-id-channel closure | supported | `5b62c89729c9b796cfcca39bd4ee13d95023adeb` / `7a3629a83c2e81774ebeb65b4b92a07b65830add`; oracle `be0e28b8…`, census `af2d4e79…`; 5 intact receipts. The run-order counterexample was named, not denied. Current replay rejects the old case-id attacker. Does not prove full verdict validity: F02 |
| r5 seeded order and nonce close enumerated positional/stale replay classes | supported | `a420deb76216471e56cb7adde03cf57b3a0f9332` / `848b3a6b1a8d68c8c148d18299e5def473ebecbd`; oracle `7143ccc2…`, census unchanged `af2d4e79…`; 6 intact receipts. R1/R2 residuals explicitly carried. Current old run-order attacker 0/28, exit 1 |
| r6 header-after-loop, re-exec scrub, content freshness close named witness classes, not all forgery | supported | `92b2e4278e5f0b67a7e5fb4c87b4d14e2d74e702` / `80a80f6f05f61d7157e4e448ed39e6cffbc2ef41`; oracle `3307761a…`, census unchanged; 7 final receipts. Current honest header begins at line 29 after 28 cases. Full-grammar normalizer and surviving-ancestor pins remain boundaries; stale note receipt paths are F04 |
| r7 four surface gaps receive implementations or an explicit partial deferral | supported | `d30b4e4340b66342d8416f0109eeb5d74cd0db83` / `ed9de4698a82f77ff0db0fca2bbc44662431fbf2`; census `c7c3569b…`, oracle `448f7723…`; 7 intact receipts; source diff adds exactly 8 oracle lines, no deletion. Instantaneous rate and live tmux proof were not delivered as completed |
| r8 residual work, oracle unchanged, measured disk deferral, harness flake disclosed | supported | `9738f1ab8c53a5ec5116c92dbbd55e8f08e2def1` / `c47c888af7f25fd4f3deed3bf1a88582887de63c`; census `390ab9cd…`; oracle `448f7723…` unchanged; **7** intact receipts. No instantaneous implementation; historical all-pass was corrected. Receipt/field counts still conflict in prose: F05 |
| r9 removes the selftest live-pipe grep race without changing production probe bytes | supported | `cffb37ef2f6f0f506cb882a199fdd422ffd4e2a5` / `6a549b9260584e87ebea4b6000b3f49a49e5ab5e`; census `1c49238a…`; `git diff -U0 9738f1a cffb37e -- tools/mori-census.sh` shows +21/−7 inside `run_selftest()`. Current writer battery 20/20 green. Production race is expressly not closed: F01 |
| r10 persisted behavioral pin and current non-volatile detection | supported | `5be89432ab4472f9193b2a787f78199ebeb58cc1` / `d1e0dd90e6042723617fc75cdfb1987684d21ce4`; current pins above; 5 intact logs plus baseline. Current clean drift exit 0, changed `warn_pct` exit 1. Active knowledge recipe does not resolve: F03; structural validation is narrower than “malformed”: F09 |

## 2. Audit inputs and disagreement handling

The consolidation inspected raw artifacts from the receipt-integrity, SHA-chain,
current-battery, cumulative-change, corpus-pointer, disposition, debt-adjudicator,
calibration, adjacency, SHONEN/scope, doc-freshness, counterfactual, sniffer, flake,
critic-of-audit, scope-sentinel, scribe and distiller work. The machine witnesses
under `/tmp/mori-r11-*` are scratch, **not durable evidence merely because they
exist**. Findings retained below were independently re-derived from committed bytes
or re-executed by this writer; essential output and reconstructible recipes are
included here. No 32/32 completion count or realized model-route attestation is
inferred from the requested wave size/model.

Important disagreements/discards:

- The debt auditor's first diskstats-FIFO arm returned a verdict. Its own follow-up
  identified a malformed synthetic `df` percent token, which prevented entry into
  the disk-rate reader. The corrected arm times out. This writer reran both
  writer-less FIFO inputs with a valid `df` row: both exit 124, no verdict. The
  first arm is not evidence of a closed hang.
- A current flake-seat battery has 9 green runs and one quota-aborted run, not 10/10
  green: `tools/mori-census.sh: line 1983: printf: write error: Disk quota exceeded`.
  It stops after 44 PASS lines with no tally. The writer's later 20-run three-worker
  battery is 20/20 green. These windows do not contradict each other; the quota
  failure is not a `grep`/SIGPIPE missing-match and is not silently discarded.
- `r10 drift works` and `r10 public note recipe fails` are both true at identical
  bytes. The `2231Z` artifact does not verify the absent `2210Z` experiment.
- Verdict arithmetic and exact vocabulary are separate checks. All nine tables
  meet the stated arithmetic even without treating the nine qualified cells as
  `improved`; those nine cells still violate the exact four-value vocabulary.
- Desktop journal events are host observations (`scope=user`), not proof of a fleet
  kill. Their alerting/routing merits review, but a desktop-only positive by itself
  does not establish a scope violation: PROVINCE explicitly includes host events.
  Likewise, no remediation write is not proof that every observational inference
  is correct.

## 3. Four load-bearing claims re-executed at today's bytes

All current-byte legs below use census `d7710981…` and oracle `448f7723…` unless a
historical oracle is explicitly named. No source file was changed.

| Historical claim selected | Commands actually run and observed results | Verdict / strength |
|---|---|---|
| 1. r2/r3 launch/authorship grading and honest matcher counterfactual | `bash tools/mori-silence-cases.sh` → `MORI_SILENCE_CASES: matched=28 total=28`, exit 0, stderr 0 B; extract/run `progressing-weak-r2.md` check → 10/10, exit 0. `git show 3da8414:tools/mori-silence-cases.sh` scratch oracle against current census → exactly 25/27, exit 1; replace only the expanded-`case` matcher in scratch → 27/27, exit 0 | supported for tested cases, direct. General all-history authorship correctness is falsified by F01 |
| 2. r4–r6 anti-sniff hardening against named old classes | Run embedded case-id m4b (`verdict-r4-…-sniffer-v2.log` source) and r5 sniffer-v3a (`order-r5-…-sniffer.log` SOURCE_A) as SUTs under the current oracle → each `matched=0 total=28`, exit 1. Honest run remains 28/28; `SHUFFLE_SEED` starts at output line 29. The old attack scripts hash `107c8df1…` and `f1c8acdf…` respectively | supported for those classes, direct. Not an impossibility proof; F02 shows another oracle blind spot |
| 3. r9 harness-race removal and present determinism | 20 invocations of `bash tools/mori-census.sh --selftest`, at three-worker concurrency → every tally `PASS (66 cases, 66 passed, 0 failed)`, every rc 0, stderr 0 B, unchanged before/after SHA. Source scan of `run_selftest()` has no executable live `| grep -q`/`-m1` assertion. Historical +21/−7 diff is selftest-only | supported for removal of that harness class, direct. Separate quota failure retained above; no zero-future-failure claim |
| 4. r10 behavioral comparison and detection power | `bash tools/mori-census.sh --drift corpus/evidence/baseline-r10-20261015T2231Z.json` → `MORI_DRIFT: none`, exit 0. Copy baseline under `/tmp`, replace `warn_pct=85` with `warn_pct=86`, drift → `MORI_DRIFT: warn_pct`, exit 1. Counter-only change behind the same finding → `none`, exit 0, by declared mask | supported for declared contract, direct. Historical interim baseline absent; malformed-input validation is limited |

Additional first-hand output:

```text
SELFTEST_EXIT=0
MORI_CENSUS_SELFTEST: PASS (66 cases, 66 passed, 0 failed)
STDERR_BYTES=0
ORACLE_EXIT=0
MORI_SILENCE_CASES: matched=28 total=28
HEADER_START_LINE=29
STDERR_BYTES=0
DRIFT_EXIT=0
MORI_DRIFT: none
LIVE_EXIT=1
MORI_CENSUS: DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)
BATTERY_TOTAL 20 GREEN 20 STABLE_SHAS True
CASE_ID_ATTACK_RC=1
MORI_SILENCE_CASES: matched=0 total=28
RUN_ORDER_ATTACK_RC=1
MORI_SILENCE_CASES: matched=0 total=28
WARN_MUTATION_RC=1
MORI_DRIFT: warn_pct
```

The live run at 22:46:39Z has nine progressing lane rows, zero `LANE_SILENT`, and
`SURFACE tmux: unavailable (cmd=tmux ls; rc=1; …)`. Its DRIFT derives from the
watchdog/waves/journal observations, not from tmux unavailability. The journal
counter is mutable; reproducing today's 338 segfault count is not a historical
byte-stability claim.

## 4. Consolidated findings table

| ID / claim checked | Verdict | Verbatim evidence, impact and evidence strength |
|---|---|---|
| F01 — exact lane authorship anywhere in the post-launch history always yields progressing | defect | Current `tools/mori-census.sh:1366-1374`, especially `printf '%s\n' "$inwin" \| sed … \| grep -Fxq …` under pipefail. An independently built quiet fixture supplies one exact subject line followed by 12,000 sibling lines: `EXPECTED=progressing`, actual `SURFACE lane.kagi: progressing-weak (… basis=row-C other_authored_commits=12001; …)`, rc 0, stderr 0. The producer/consumer condition inverts when an upstream writer gets SIGPIPE. This is the explicitly carried production class, not a recurrence in the fixed selftest. Direct; Appendix B |
| F02 — oracle green verifies a valid CLEAN/DRIFT roll | defect | Replace only the proxied census's final `MORI_CENSUS: CLEAN`/`DRIFT` word with `BANANA`, preserve actual lane rows, nonce and rc. `bash tools/mori-silence-cases.sh /tmp/<wrapper>` → `MORI_SILENCE_CASES: matched=28 total=28`, exit 0, stderr 0. Current oracle `:569-585` checks presence of `^MORI_CENSUS:`, not its vocabulary/rc consistency. Oracle green proves its lane cases, not the complete verdict contract. Direct; Appendix C |
| F03 — the r10 knowledge note identifies the adopted committed baseline and executable recipe | defect | `corpus/knowledge/drift-pin-r10.md:195-200,224-227` names `…T2210Z.json`, digest `bdf46496…`, census `1ddb7ff8…`. `git cat-file -e 5be8943:corpus/evidence/baseline-r10-20261015T2210Z.json` → `fatal: path 'corpus/evidence/baseline-r10-20261015T2210Z.json' does not exist in '5be8943'`, rc 128. Its drift command → `mori-census: --drift baseline missing: corpus/evidence/baseline-r10-20261015T2210Z.json`, rc 2. Correct delivered artifact is `2231Z`, digest `0993b235…`. Direct |
| F04 — r6 note's primary receipt references resolve | defect | `corpus/knowledge/verdict-machine-r6.md:19-20,110,135,255-266` cites `T190229Z`/`T190453Z` logs. Current evidence glob counts: `190229 0`, `190453 0`, `191216 7`; only the final `191216Z` set lands in `92b2e42`. The evidence index explains supersession at `corpus/evidence/README.md:349-356`, but the active note was not swept. Direct path/commit check; final receipts remain intact |
| F05 — all cited receipt/field tallies agree with delivered artifacts | defect | `SCORECARD.md:429` says “eight r8 receipts”; actual r8 logs 7. `SCORECARD.md:511` says “seven receipts + the baseline”; actual r10 logs 5 plus one baseline. `SCORECARD.md:410-411` says “exactly the 4 new names”; `corpus/knowledge/surfaces-r8.md:203-204` distinguishes 9 names on the fixture from 4 on live. No eighth or sixth/seventh log is manufactured. Direct counted universe |
| F06 — all filed SHONEN assessments have four separate box lines | defect | r2–r4 each have 4 `- [` lines under `## SHONEN`; r5–r10 each have 1. For example `.ufo/reports/round-10/mori-goalwave.md:45-47`: `- [ ] · [ ] · [ ] · [ ] — all four remain [ ] …`. The heading exists and non-promotion intent is honest, but compact tokens do not satisfy one assessment line per box. 6/9 reports affected. Direct |
| F07 — r2 goal-wave report cites the committed work that it reports after landing | defect | `.ufo/reports/round-2/mori-goalwave.md:5` names entering baseline `e30b2e3`, not delivered work `3da8414`; `git log --diff-filter=A --format=%H -- <report>` returns `3da8414970382c1690f7a8b020b75c2def6eaba5`. The report and work first land together, unlike r3–r10 evidence/records separation. A real report exists; this is a conformance defect, not proof that no work occurred. Direct |
| F08 — canonical verdict cells use exactly the four admitted values | defect | Nine SCORECARD cells say `**improved narrowly**`: `:114,115,173,226,281,327,377,427,429`. Exact-cell recount: `{'improved': 22, 'improved narrowly': 9, 'unchanged': 23}`. Put the qualification in evidence, not a fifth verdict value. All nine rounds independently still have ≥1 exact `improved`, zero `harmed`. Direct |
| F09 — the malformed-input guarantee requires a format/version header | unverifiable | `tools/mori-census.sh:1815-1850` validates only the marker, volatile-list presence, and nonempty block. Delete the format/version first line from a copy of the adopted baseline: `NO_FORMAT_HEADER_BASELINE_RC=0`, `MORI_DRIFT: none`. Plain junk with no marker does return 2. Acceptance of this headerless form is directly measured; whether that form is forbidden is not specified precisely enough to call it a proven rejection-contract violation. The validation/format contract needs clarification, not an invented stronger requirement |
| F10 — claimed landed SKILL updates are present in delivered commits | defect | Initial and later `git status --short`: ` M SKILL.md`; `git log --format='%H %s' -- SKILL.md` last touches it at `1439c47`. Current diff against HEAD is +70/−4, including r7–r10/oracle prose. r5 report `:25`, r6 report `:25`, r7 report `:28`, r8 report `:22`, r9 report `:24`, r10 report `:22` mention SKILL rows, but these updates are not in the delivered evidence/records commits. The dirty working-tree drift paragraph also says 65 cases and the absent `2210Z` baseline (`SKILL.md:75-80`). Inherited state, left untouched. Direct |
| F11 — all admission timestamps are chronologically compatible with their carrying commits | defect | `SCORECARD.md:211,258-259,350-351` and `.ufo/reports/round-9/mori-goalwave.md:26` put parent acceptance at 17:55Z, 18:30Z, 20:10Z, 21:50Z. Corresponding records commits are 17:53:05Z (`7a3629a`), 18:28:43Z (`848b3a6`), 20:06:34Z (`ed9de46`), 21:48:43Z (`6a549b9`). These minute labels are later than the already-committed claims. Receipt capture clocks are earlier and intact. Correct chronology or explicitly label estimates; do not infer fabricated execution solely from a rounded timestamp. Direct metadata inconsistency |
| F12 — leading-zero numeric seed is a valid reproducibility pin or a setup error | defect | `env MORI_SHUFFLE_SEED=045484716 bash tools/mori-silence-cases.sh` → `line 1052: 045484716: value too great for base (error token is "045484716")`, exit 1, stdout 0 B. Digits-only validation `:222-226` admits a value then interpreted as invalid octal. Already reported in r10 evidence index `:735-745`; still open, not new from audit. Direct |
| F13 — a current-byte selftest invocation aborted from quota exhaustion, separately from the SIGPIPE class | supported | Flake-seat run 7: exit 1, 44 PASS lines, no tally; stderr verbatim `tools/mori-census.sh: line 1983: printf: write error: Disk quota exceeded`. Writer's separate 20-run set is green, not a reason to omit this result. This is an observed environmental failure, not a newly fabricated implementation defect or a falsification of the structural r9 race fix. Direct preserved stderr plus separately rerun battery |
| F14 — all original experiments can be independently re-created from delivered material | unverifiable | `drift-pin-r10.md:207-214` claims a historical clean run against `2210Z`, but that artifact has no lane Git history; some r6 original fixture fingerprints and raw-output digests likewise lack the original input tree/transcript. The later `2231Z` comparison and fresh salted fixtures are different experiments. Unrecoverable input; not an assertion that the earlier runs never happened |

## 5. Final carried-debt register

This register reconciles the debt-adjudicator's probes with direct source/history and
this writer's reruns. **Omission from a later round is not closure.** “Boundary”
means a disclosed limit, not a claim of implementation completion. “Closed” below
means the named implementation task, not every sentence mentioning it, was disposed.

### Disposed implementation debts

| Origin / debt | Disposition at admitted revision | Independently checked evidence |
|---|---|---|
| r1/r2 per-surface notes and authorship discrimination | closed in r2 `3da8414` | 7 numbered surface sections; extracted 10-case block SHA `9c91e0a0…`, rerun 10/10 |
| r2 launch/authorship cutover and `:517`/`:283` crashes | closed in r3 `1439c47` | Source replacement/rc gates, preserved before/after receipts, current 28-case oracle; not closure of row-6 body validation or F01 |
| r3 frozen alternation matcher, `:227`, per-round close tracking | closed in r4 `5b62c897` | Source diff, exact want matching, state-walk canary receipt, close-sequence selftests; current frozen/counterfactual replay |
| r3 case-id leak; r4 order-replay residual | bounded closure in r4/r5 | Opaque case dirs, no exported fixture marker; shuffled cases + nonce. Current old forgers each 0/28; other classes remain below |
| r5 R1/R2 enumerated classes | bounded closure in r6 `92b2e42` | Final `191216Z` attack receipts and final oracle source; header now after cases and content salt changes naive memorizer keys |
| r2 `state_rounds` count-only, disk average, pressure visibility, tmux relevance | implemented in r7 `d30b4e4` | +15 selftests; 8-line additive oracle fixture pin; current source/rows; instantaneous and live-tmux qualifications below |
| r7 tmux freshness, round-entry invisibility, memory scope/live evidence | implemented/dispositioned in r8 `9738f1a` | Timeout-bound freshness; symlink/dir/FIFO classified before read; peak with instance anchor; local thresholds not universal calibration |
| r8 harness missing-match race | closed in r9 `cffb37e`, only selftest path | Selftest-only +21/−7 diff; no producer-piped early-exit match in harness; fresh 20/20 green; production sibling F01 remains |
| r2–r9 missing behavioral pin | implemented in r10 `5be8943` | Persisted `2231Z` baseline and current clean/mutation exits. Citation debt F03 and contract limits remain |

### Still carried, deferred, or boundary-limited

| ID / origin | Final disposition | Owner and next falsifier/unblock |
|---|---|---|
| D01 r9 production authorship pipeline | **open defect**, F01; large valid window misgrades subject as weak | mori; a future isolated production fix plus a long-history positive and sibling-only negative must pass; do not call the harness fix a production fix |
| D02 oracle verdict-line validation | **open defect**, F02 | mori; BANANA/roll-rc/tally-corruption mutants must fail without weakening lane-state cases |
| D03 r2 row-6 presence/window closure | **open semantic boundary**; fresh empty committed report still yields `basis=row-6 not-open` | mori plus driver/integrator owner kumitate; decide whether to validate report substance or explicitly keep narrower closure semantics. Must distinguish mission closed from work admitted |
| D04 r7/r8 disk input FIFO latency | **open hang** for `MORI_DISKSTATS` and `MORI_UPTIME`; writer rerun each timeout 124, no verdict | mori; reject non-regular inputs or bound reads in a future round, retaining honest unavailable diagnostics. Does not imply default `/proc` files hang |
| D05 r1/r2 missing-pgrep early return / unreachable log check | **open probe-degradation gap** at current `probe_watchdog`; unavailable pid probe returns before independently checking log freshness/state | mori; missing pgrep plus stale/missing log must still observe whatever independent facts remain readable; never convert unknown pid to absent |
| D06 r2 argv-substring watchdog match | **open false-positive class**; `pgrep -af` plus substring filter can count an editor/command merely mentioning the name | mori with kumitate for authoritative daemon identity; positive real-process and negative argv-mention fixtures needed |
| D07 r1 `WaveAgeMath` | **open calibration boundary**; current `probe_waves` ages newest file mtime, not authoritative dispatch/terminal history | mori/kumitate; anchor a launch/settlement contract or keep “aged surface without settlement token”, not proven dead wave. Touching a file is not proof of settlement |
| D08 r1 system-journal coverage | **still absent**; current journal probe is `--user` | mori with tsukuroi triage; separate signal-specific system-journal finding and unavailable fixtures if selected. Do not conflate all coredumps with signal 11 |
| D09 r1 journal/cgroup attribution | **boundary**, not fleet-kill proof: user-journal OOM/SIGKILL counts can be desktop events; local/service absence is disclosed `local_oom_kill=unavailable` | tsukuroi diagnoses host events; mori carries typed scope, kumitate diagnoses orchestration, operator alone remediates. Desktop OOM fixture emitted `OOM_KILL_JOURNAL … scope=user` and DRIFT |
| D10 r1/r7 thresholds | **local proposals/placeholders remain**; disk 85/95 and memory PSI/fill/avail values are not universally calibrated | mori/operator; host/workload distribution and a falsifiable alert-cost rule before any threshold tuning. A measured quiet window is not calibration |
| D11 r7/r8 instantaneous disk write-rate | **measured deferral**, not implemented | operator decides runtime budget; 0.2 s serial dwell alone exceeds 50 ms, corroborated by debt-seat median 201.9 ms. Current since-boot average is not a burst rate or fleet attribution |
| D12 r7/r8 tmux relevance/freshness | **implemented but live arm unavailable on this host**, fixture-proved; pane-cwd rule and per-call N×timeout bound remain | mori; obtain an authorized real relevant-session observation, without creating/steering the user's sessions merely to force proof |
| D13 r6 full-grammar normalizer | **accepted finite-fixture boundary**; deterministic finite answers can be memorized after annotation normalization | mori; do not promise anti-forgery impossibility. A future randomized semantic workload needs held-out graded outcomes, not just renamed salt |
| D14 r6 surviving-ancestor pinned environ | **operator invocation boundary**; oracle re-exec cannot scrub a caller that survives with exported pins | operator/kumitate wrapper owner; keep pins out of surviving ancestor environments, or adopt an authorized private channel. Do not inspect unrelated process environments |
| D15 r10 leading-zero seed | **open**, F12 | mori; normalize explicit base-10 or reject safely with exit 2; retain deterministic valid-pin behavior |
| D16 r10 drift counter mask / absent invocation record / baseline aging | **declared boundaries**; count-only same-id changes are masked, env changes can be false-red context, legitimate state changes age a pin | mori/operator; compare same invocation, record env shape, add optional masked-delta visibility if desired; re-pin only with a reason, never to hide red |
| D17 r10 malformed baseline validation | **open narrow contract gap**, F09 | mori; specify minimum structural format and reject corrupt/missing mandatory headers while preserving valid old pins |
| D18 r2 blocked-attempt routing and receipt identity | **external/not discharged by these nine goal waves** | operator/integrator; supply authorized binding surface and authoritative receipt bag if that integration is resumed. Lane cannot invent task identities. Successful local goal-wave artifacts are not a Sighting receipt |
| D19 unlanded/incorrect documentation and metadata | **open provenance/conformance**, F03–F11/F14 | parent/mori in a future authorized correction round; resolve inherited SKILL changes, append named record corrections, sweep active recipes/receipt paths, preserve historical reports |
| D20 SHONEN external verification | **gate not satisfied**, four boxes unchecked | a named reviewer who did not author the changes and is not a dispatched lane seat; complete review after public instructions are executable |
| D21 audit-time quota abort | **environmental failure retained**, not evidence of r9 SIGPIPE recurrence | operator/tsukuroi diagnose quota if operationally relevant; no audit cleanup/remediation. Selftest should eventually distinguish setup failure from a case result |

No closure is claimed for `/scratch/tmp` coverage absent from default disk targets,
operator-supplied live `MORI_*_BIN`/unquoted target-list effects, quota observability,
or universal resource thresholds. These are inherited observability/threat-model
limits (`observability-census-r1.md:182-184,216-221`, `SKILL.md:147-175`), not tasks
silently absorbed by this read-only audit.

## 6. SHONEN readiness — no self-attestation

`SHONEN.md:5-8` still has four `[ ]` boxes. The audit found no named non-author
attestation in that gate. A strong model, a fresh same-wave seat, or this note's
writer is still the lane for promotion purposes. **No box is checked here.**

| Gate item | Readiness assessment | Evidence / remaining blocker |
|---|---|---|
| Real decision tables, error patterns, checklists, cited sources | substantive material present; ready for an outside review after provenance cleanup | `SKILL.md` tables/checklist; 13 pre-audit knowledge notes; F03/F04/F10 prevent calling every active pointer settled |
| At least one end-to-end domain task executed and logged | substantive evidence present | LOG r1/r2 onward plus current live census, finding ids, unavailable separation and operator handoff boundary; live result is an observation, not a remediation claim |
| Instructions executable without oral context | **not ready as written** | r10 adopted-baseline recipe exits 2; inherited SKILL changes are not delivered; gate registry prose says “Registry row lands with the gate” but no complete standardized gate/probe row with all required fields is present |
| No cross-domain bleed; PROVINCE accurate | detection/report boundary substantially supported, not externally attested | PROVINCE refuses remediation/dispatch/OS ownership; fixtures and live probes were read-only in scope. Journal scope/attribution and orchestration routing must be reviewed as observations rather than inferred causal diagnoses |

Operator recommendation: **hold promotion**. Fixing provenance and obtaining a named
non-author review are separate actions; neither is accomplished by declaring this
32-seat audit independent. Keep the canonical checklist and rank unchanged.

## 7. Top recommendations for the operator

1. Select a future, explicitly scoped correctness round for **F01 and F02** before
   relying on all-history attribution or treating oracle green as a full verdict
   contract. Preserve the counterexamples as positive/negative regressions.
2. Land a provenance-only correction with explicit supersession: final `2231Z`
   baseline, final `191216Z` receipt set, true receipt/field counts, inherited SKILL
   disposition, four SHONEN assessment lines, canonical verdict tokens, honest
   chronology. Append corrections to LOG/SCORECARD/report records; do not rewrite
   old evidence or recreate an imaginary historical baseline.
3. Keep the debt register durable. Prioritize FIFO/partial-probe degradation by
   operational exposure, and keep measured disk deferral and anti-forgery/masking
   boundaries distinct from completed implementations.
4. Commission a **named non-author promotion review** after executable instructions
   are settled; run public recipes from delivered commits, not an author's dirty
   tree. Do not use seat count or model strength as the gate's verifier identity.
5. Preserve the r11 failed quota invocation and audit disagreements. No blanket
   “all checks passed” or “zero writes” statement is warranted.

The scope sentinel's bounded 22:44:45Z–22:51:45Z watch reports
`changed_paths=4`, `forbidden_changed_paths=0`, but **198 forbidden-path events**
were transient `.git/index.lock` activity (222 events total, zero queue overflows).
That supports no unauthorized content change in that interval, not literally zero
filesystem writes, attribution of every event, or coverage after the watch ended.
This writer added only this knowledge note in the lane; all experiments lived in
`/tmp`. The pre-existing dirty SKILL and untracked interactive-session material were
not repaired, committed, or used as a promotion attestation.

## Appendix A. Reproduce the chain checks

Run from the lane root. These are checks, not writes to lane history:

```sh
for ref in 3da8414 1439c47 bbcc1ad 5b62c897 7a3629a a420deb7 848b3a6 92b2e42 80a80f6 d30b4e4 ed9de46 9738f1a c47c888 cffb37e 6a549b9 5be8943 d1e0dd9; do
  git rev-parse --verify "${ref}^{commit}"
  git merge-base --is-ancestor "$ref" HEAD || exit
  git show -s --format='%an <%ae>' "$ref"
done
sha256sum tools/mori-census.sh tools/mori-silence-cases.sh corpus/evidence/baseline-r10-20261015T2231Z.json
```

Receipt counting/byte-comparison method actually used (Python, no dependencies):

```python
from pathlib import Path
import hashlib, subprocess
r = Path('.')
index = (r/'corpus/evidence/README.md').read_text()
pairs = [('3da8414','watch-r2-'), ('1439c47','cutover-r3-'),
         ('5b62c897','verdict-r4-'), ('a420deb7','order-r5-'),
         ('92b2e42','backchannel-r6-'), ('d30b4e4','surfaces-r7-'),
         ('9738f1a','residuals-r8-'), ('cffb37e','flake-r9-'),
         ('5be8943','pin-r10-')]
n = hashes = same = 0
for commit, prefix in pairs:
    for p in sorted((r/'corpus/evidence').glob(prefix+'*.log')):
        b = p.read_bytes(); n += 1
        hashes += hashlib.sha256(b).hexdigest() in index
        same += b == subprocess.check_output(['git','show',commit+':'+str(p)])
print(n, hashes, same)  # observed: 50 50 50
```

The 20-run writer battery ran `bash <absolute lane>/tools/mori-census.sh --selftest`
20 times through a Python `ThreadPoolExecutor(max_workers=3)`, capturing each
stdout/stderr/rc and hashing the census immediately before and after each run.
Observed: 20 identical 66/66 tallies, zero nonzero exits/stderr, stable pins.

## Appendix B. Reproduce the production wrong-grade without a real host history

The following is the independent quiet fixture generator actually run by this writer.
It writes only a new `/tmp` directory, supplies one exact subject commit followed by
12,000 sibling commits through the documented Git override, and runs unmodified
current census bytes. It isolates the production pipeline, not the selftest harness.

```python
from pathlib import Path
import os, subprocess, tempfile
lane = Path('/home/vgpnk/Projects/shokunin/mori-shokunin')
f = Path(tempfile.mkdtemp(prefix='mori-r11-history-own-', dir='/tmp'))
root = f/'root'; ufo = root/'.ufo'; bins = f/'bin'
for p in (ufo/'state', ufo/'waves', root/'kagi-shokunin/.git', bins, f/'home', f/'cg'):
    p.mkdir(parents=True, exist_ok=True)
(ufo/'watchdog.log').write_text('TIMESTAMP launch kagi round=7 ts=1699998000\n')
os.utime(ufo/'watchdog.log', (1700000000,1700000000))
(ufo/'state/kagi.round').write_text('7\n')
stubs = {
 'pgrep': "printf '123 bash /path/shokunin-watchdog.sh\\n'\n",
 'journalctl': 'exit 0\n', 'tmux': 'exit 1\n',
 'df': "printf 'Filesystem 1024-blocks Used Available Capacity Mounted on\\n/dev/fake0 1000000 10000 990000 1%% /fake\\n'\n",
 'git': '''for a in "$@"; do case "$a" in
rev-parse) printf '.git\\n'; exit 0;;
ls-files) exit 0;; cat-file) exit 1;;
log) printf '1699999000 kagi-shokunin <kagi@shokunin.local>\\n'; for ((i=0;i<12000;i++)); do printf '1699999000 aggregator-shokunin <aggregator@shokunin.local>\\n'; done; exit 0;;
esac; done; exit 2
'''}
for name, body in stubs.items():
    p = bins/name; p.write_text('#!/bin/bash\n'+body); p.chmod(0o700)
for name, text in {'memory.events':'high 0\nmax 0\noom 0\noom_kill 0\n',
 'memory.current':'100\n', 'memory.max':'max\n',
 'memory.pressure':'some avg10=0.00\nfull avg10=0.00\n', 'memory.peak':'100\n'}.items():
    (f/'cg'/name).write_text(text)
(f/'meminfo').write_text('MemTotal: 100000 kB\nMemAvailable: 90000 kB\n')
(f/'uptime').write_text('1000.00 1.00\n')
(f/'diskstats').write_text('8 0 fake0 0 0 0 0 0 0 20000 0\n')
e = {'PATH':'/usr/bin:/bin', 'HOME':str(f/'home'), 'TZ':'UTC', 'LC_ALL':'C',
 'MORI_FIXTURE':str(f), 'MORI_SHOKUNIN_ROOT':str(root), 'MORI_UFO_DIR':str(ufo),
 'MORI_NOW_EPOCH':'1700000000', 'MORI_ROSTER_LANES':'kagi',
 'MORI_LANE_SILENCE_S':'900', 'MORI_DISK_TARGETS':str(root),
 'MORI_MEMINFO':str(f/'meminfo'), 'MORI_UPTIME':str(f/'uptime'),
 'MORI_DISKSTATS':str(f/'diskstats')}
for k,b in [('EVENTS','memory.events'),('LOCAL_EVENTS','memory.events'),
 ('SERVICE_EVENTS','memory.events'),('CURRENT','memory.current'),
 ('MAX','memory.max'),('PRESSURE','memory.pressure'),('PEAK','memory.peak')]:
    e['MORI_CGROUP_'+k] = str(f/'cg'/b)
for n in ('pgrep','journalctl','tmux','df','git'):
    e['MORI_'+n.upper()+'_BIN'] = str(bins/n)
p = subprocess.run(['bash',str(lane/'tools/mori-census.sh')], env=e,
                   capture_output=True, text=True, timeout=30)
print('RC='+str(p.returncode), 'EXPECTED=progressing')
print('\n'.join(x for x in p.stdout.splitlines()
                if x.startswith(('SURFACE lane.kagi:', 'MORI_CENSUS:'))))
```

Observed output at `d7710981…`:

```text
RC=0 EXPECTED=progressing
SURFACE lane.kagi: progressing-weak (lane=kagi round=7 launch_epoch=1699998000 age_s=2000 basis=row-C other_authored_commits=12001; ts=2023-11-14T22:13:20Z)
MORI_CENSUS: CLEAN (findings=0 drift=0 unavailable=1 surfaces=7)
```

The size widens the SIGPIPE window; the fact that ordinary short fixtures pass is
not a negative control for a large-history bug. No assertion is made about a real
lane currently having this exact synthetic history.

## Appendix C. Reproduce the oracle's verdict-word blind spot

Save this wrapper only under `/tmp`; invoke it as the optional census argument of
`bash tools/mori-silence-cases.sh /tmp/<wrapper>`. These are the exact wrapper bytes
run by the writer, apart from its temporary filename:

```bash
#!/usr/bin/env bash
set +e
out=$(bash /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-census.sh "$@" 2>&1)
rc=$?
out=${out//MORI_CENSUS: CLEAN/MORI_CENSUS: BANANA}
out=${out//MORI_CENSUS: DRIFT/MORI_CENSUS: BANANA}
printf '%s\n' "$out"
exit "$rc"
```

Observed: `MORI_SILENCE_CASES: matched=28 total=28`, exit 0, stderr 0 B. This wrapper
proxies real grading rather than being a zero-logic forger; the finding is specifically
that the complete final-roll grammar is not asserted. It does not negate rejection
of the old case-id/run-order attackers.

## Strongest historical claim not independently verified

The clean historical cross-revision drift reading against the supposedly committed
`baseline-r10-20261015T2210Z.json` (`drift-pin-r10.md:207-214`) cannot be independently
verified from the delivered lane. Its original input is absent from the evidence
commit and lane history. The valid `2231Z` baseline, matching digest, current clean
run and mutation detection support a different, narrower claim; they do not
retroactively verify that missing experiment. The exact historic normalizer/ancestor
attack tallies also remain bounded by their stated witness classes and preserved
material, not elevated to universal anti-forgery proof.
