# Mori round 17 — terminal-at-scan observation, jj history anchors and blind-sweep calibration

Date: 2026-10-20. Author lane: mori. Evidence: LOG.md round-17 entries;
fleet report `/home/vgpnk/Projects/shokunin/.ufo/reports/round-17/mori.md`.
Entering branch tip: `24526ea9617cd020fee16c28fe4d4a2789dc28cb`.

## Claims and declaration refinement

- C1 coverage: standalone bounded, field-limited OMP transcript terminal-at-scan capability.
- C2 operability: census branch-anchored history and off-branch/ambient-author diagnostics.
- C3 calibration: legacy blind pathspec misses the retained r16 root artifact, corrected
  filename-or-content no-pathspec detector finds it (missed artifact assertions 1→0).

The initial wave declared C1/C2, treating coverage 6 as the lowest owned axis versus
operability 7. `build/ScorecardAxisCheck.md` correctly noted the literal all-six scores
include depth/freshness/calibration 5. Before L1 claim measurement, contract.md was refined
to add C3 calibration, using the already-scoped MisrootSweep work rather than inventing
additional work. C3 is independent of C1/C2. Scores stay held, not inflated by fixture volume.

L1 holds the planner seat. The build wave's seven code writers used separate clones at the
entering tip under `.ufo/worktrees/round-17/<seat>`, all ignored and excluded from commits;
L1 alone integrates production files. Review/source seats wrote only scoped reports.

## Gate

### Candidates and decisions

- Admit the finite C1 terminal-at-scan capability only with its settle, schema, duplicate-path,
  prefix and privacy qualifications. Reject permanent-death, incident-count and authenticated-
  membership interpretations (CriticC1/TranscriptShapes/SeatNaming).
- Admit C2 as a local-branch correctness repair, not remote publication proof. Reject
  treating every nonzero merge-base status as divergence, sibling-shokunin authorship as
  ambient-author violation, or changing row-A parsing by adding committer fields.
- Admit C3 only against byte-exact `frozen/MoriR16.Lesson`, not a synthetic fixture that
  conveniently includes missing lane/round tokens in content. Reject the old pathspec
  sweep's clean result as evidence of a clean fleet root.
- Independent outside admit/reject spotcheck remains required; author-dispatched seats are
  not non-author closure. No SHONEN box or rank is self-certified.

### New source rows, opened by source seats this round

All access dates are **2026-10-20**. Each located quote below is ≤25 words; opening
receipts reside under `.ufo/waves/round-17/build/Src*.md`.

| Row | URL | Location and verbatim located quote |
|---|---|---|
| S041 | https://www.rfc-editor.org/rfc/rfc6585 | §4, plain text lines 134–135: “The 429 status code indicates that the user has sent too many requests in a given amount of time (\"rate limiting\").” |
| S042 | https://www.rfc-editor.org/rfc/rfc9110#section-10.2.3 | §10.2.3: “Servers send the \"Retry-After\" header field to indicate how long the user agent ought to wait before making a follow-up request.” |
| S043 | https://docs.z.ai/api-reference/api-code | Error table, api-code.md:31, code 1302/HTTP429: “Rate limit reached for requests”; :16/:33 also map 1113/1308 to429. |
| S044 | https://docs.jj-vcs.dev/latest/git-compatibility/ | Colocated workspaces: “jj commands will usually put the Git repo in a \"detached HEAD\" state, since in jj there is not concept of a \"currently tracked branch\".” |
| S045 | https://docs.jj-vcs.dev/latest/cli-reference/ | metaedit --update-author: “This updates the author name and email. The author timestamp is not modified – use --update-author-timestamp to update the author timestamp.” |
| S046 | https://git-scm.com/docs/git-merge-base | OPERATION MODES --is-ancestor: “Errors are signaled by a non-zero status that is not 1.” |
| S047 | https://git-scm.com/docs/git-symbolic-ref | OPTIONS -q: “Do not issue an error message if the <name> is not a symbolic ref but a detached HEAD; instead exit with non-zero status silently.” |
| S048 | https://man.archlinux.org/man/pacman.conf.5 | LogFile directive: “Overrides the default location of the pacman log file. The default is /var/log/pacman.log.” |

SOURCES40→48: eight new tier-A rows; S041/S043/S044/S045/S046/S047 enter mined
with the new knowledge paths, S042/S048 enter queued. No existing status, recheck or used-by
cell changes. Thus there are no old→new mutable-cell transitions on existing rows.
S043 caused the A1 business-code/quota-before-generic429 fix; S046 caused the distinction
between ancestry status1 and error. These are sourced claims, not decorative citations.

## Mistakes

| ID | Class | Evidence pointer | Captured-by | Fix / falsifier |
|---|---|---|---|---|
| M1 | scope | `lessons/round-16-verifier-spotcheck.md:202–209`; fleet archived `MoriR16.Lesson`, sha25615f9f82d…5510e; `build/MisrootR16Facts.md` | prior addendum wrongly prescribed a pathspec; QUALITY19 did not test coverage | C3 no-pathspec sweep checks filename OR content; exact archived bytes retained in `frozen/MoriR16.Lesson`; legacy sweep must miss the root file and corrected sweep find it. Q43. |
| M2 | reference-drift | r16 M7 cites only BootContinuity:31–32; `build/R16LessonM7.md` maps omitted probes | QUALITY38/39, disclosure lacked completeness criterion | Append precision: BootContinuity:23 ran `-b -n 2`; :24 anchor `--cursor`; :25 fabricated cursor rc1; :26 `--user -n 1`; :28 `id -nG`; :42 reasons from inadmissible result. These were unauthorized live probes, not only /tmp writes/bg_2667. No admitted result uses them. Q45. |
| M3 | scope | r16 context-original lacked live-journal ban; r17 `evidence/context-check-wave1-original.json` fails `no_tmp_probe_outputs` | outside closure item3 | Pre-dispatch r16 checker caught r17 wording before dispatch: original rc1, corrected rc0 with spec SHA6969eb19…; new r17 checker adds fleet-root/VCS/background/privacy clauses. Q44; instruction checks never runtime prevention. |
| M4 | stale-premise | `lessons/round-16-verifier-spotcheck.md:220–223` | QUALITY40/correction sweep | Appended PROVINCE closure supersession and r16 knowledge-note dated-version correction. r16 host261.2-1 is historical; today's pacman log records262-1. Q46. |
| M5 | scope | initial C1/C2 declaration; `build/ScorecardAxisCheck.md` | literal AXES lowest non-retired obligation | Added C3 calibration5 before L1 measurements; no owned-subset waiver self-certified. |
| M6 | attribution | JjAuditMori F3/F4; `build/{CriticC2,CriticHarm,CensusConsumers}.md` | exact-author discipline, no jj branch criterion | C2 branch anchor; warn severity (not nonexistent drift severity), separate author parser, legitimate sibling-author control, status1!=error. Q47. |
| M7 | number-drift | `build/{CriticC1,TranscriptShapes,SeatNaming,CriticFrontier}.md` | counted-unit criteria16/34; insufficient temporal/identity controls | A1 settle-window classes, relative keys, main-session separation, exact-prefix-matched-none setup, schema3, vendor codes. Resumed-after-error remains a named limit, never hidden. Q48. |
| M8 | scope | lane jj op45a25744584d, args `jj -R …/mori-shokunin diff --stat`, from ReviewSkillRows-5 | addendum read-only jj requires --ignore-working-copy | A read-looking jj diff snapshotted @ at15:55:07. It did not move the branch. L1 records the violation; no retroactive prevention claim. All subsequent L1 jj reads use --ignore-working-copy; helper owns commits. |
| M9 | scope | `build/SentinelTranscripts.md` self-discloses one credential_pin-line display during grep | transcript field allowlist, CORPUS no credentials | No values retained in report/corpus. Exclude raw dumps from evidence; accept only field-limited counts. Disclosure is not prevention or permission. |
| M10 | scope | wave1-context and seven executor assignments explicitly authorized own selftests | QUALITY39 still requires integration-owner verification after settlement | This L1 authorization conflicts with the stricter lane criterion; seat selftest results are advisory, not admission evidence. L1 runs settled committed tools once. No selftest-prohibition compliance claim. |

## Carry-forward / migration dispositions

- r10 drift pin remains red debt without re-pin; fixture green is not freshness green.
- Keep alias false-unavailable, vacuum/cross-boot UNKNOWN and anchor-only live qualifications;
  no census cutover to the window tool.
- JjAuditMori census HEAD hazard is fixed by C2; authorship relies on helper metaedit, not
  setting jj user config alone. Helper-only commits and final `landed` citation retained.
- r13–r16 historical gates retain their original HEAD provenance fields and bytes. They are
  not used as landed-branch identity evidence. JjAuditMori env/output-guard residuals on
  those historical tools remain disclosed; no fleet helper/sibling file edited.

## Cross-domain observations (detection/report only)

`build/PacmanTxnToday.md` locates `/var/log/pacman.log:2462` (09:15:30 -Syu),
its full-upgrade/transaction window and448 actions, plus :3161 (13:23:08 -U zcode).
`build/PacmanActorTrace.md` correlates the -Syu stream and invocation UUID to an OMP bash log
in the separate `-Documents-nvhelpme` session; the zcode user/interactive provenance is an
inference, not authenticated actor attribution. `build/OverlapTsukuroi.md` retains the
boundary: mori detects/reports, tsukuroi/operator owns OS diagnosis, update safety and recovery.
No pacman transaction, package install or service change was performed by this lane.

## Measurement records

Committed measurement manifests, counts and revision are appended below only after execution.

### L1 measurement at committed branch tip273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7

The helper returned `landed273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7` (space
between marker/hash in actual helper stdout). `PINNED_INPUTS.json` retains input
digests and `evidence/*.json` receipts retain exact argv, timestamps, rc, streams,
branch ref and before/after branch tips. All admission checks below are L1 runs
after build writers settled, not quoted seat selftests.

| Claim | Executed counting command from lane root | Observed rc/output |
|---|---|---|
| C1 | `jq -s '[.[] | (.summary.capability_absent + .summary.mismatched)]' .ufo/waves/round-17/evidence/seat-before/run-manifest.json .ufo/waves/round-17/evidence/seat-after/run-manifest.json` | rc0 `[54,0]`; gate exits1→0, delivered54/54 match |
| C2 | `jq -s '[.[].totals.failed_assertions]' .ufo/waves/round-17/evidence/jj-before/run-manifest.json .ufo/waves/round-17/evidence/jj-after/run-manifest.json` | rc0 `[21,0]`; gate exits1→0, cases7/12→12/12 match |
| C3 | `jq -s '[.[] | (.stdout|fromjson) | 1 - ([.candidates[]|select(.path=="MoriR16.Lesson")]|length)]' .ufo/waves/round-17/evidence/c3-before.json .ufo/waves/round-17/evidence/c3-after.json` | rc0 `[1,0]`; probe exits0 false-clean→1 candidate found |

C1 entering capability absence is not54 old production defects. The same
54 synthetic expected cases independently pin81 source inputs; missing/changed
pins are setup/tamper, not a compared green. Generated FIFO and chmod000 live
only in per-case copies; they cannot be committed as POSIX special-file modes.
Copied session sandboxes were removed after capture; source packs, exact
stdout/stderr and their digests remain retained. The root's source fixture FIFO
was caught at commit inventory and replaced by `fifo_files` metadata before
the measured commit; this is an actual reproducibility correction, not a pass
of the untrackable state.

C2 counts failed assertions, not distinct bugs. Assertion totals124→134 because
detail/severity checks run only when the expected diagnostic exists. The same12
scenario expectations are used on both sides; five case mismatches disappear.
The positive/negative controls include plain Git, detached-at-tip, sibling author
and unresolved-branch fallback. Real jj writes are only in isolated gate-created
sandboxes with explicit -R and HOME/XDG_CONFIG_HOME isolation. JjGate disclosed
one accidental removed `/tmp` file in its build report; it is a procedural
violation, not admitted measurement evidence.

C3's separate non-selftest measurement builds a sandbox fleet, plants the exact
847-byte archived root artifact and a sibling control, and invokes both probe
modes. Legacy pathspec detects0, default detects exactlyMoriR16.Lesson by path
alone; sibling stays unclaimed. Frozen `c3-expected.json` pins the witness hash.
The rc1 after is the detector correctly raising a candidate, not a gate failure.

### Preserved instruments and live observation

L1 selftests: census125/125; terminal33 arms; seat gate14 arms; jj gate13 checks;
misroot11 arms; context29 arms — all rc0. Silence oracle28/28 rc0. Existing
gates against the delivered census: r13 24/24, r14 44/44, r15 63/63 with frozen
red34/34 — all rc0. Exact commands/results are the correspondingly named
`evidence/*selftest.json`, `silence-oracle.json`, `r{13,14,15}-preserved.json`.
`preservation.json` verifies7 unchanged historical instruments/pin bytes;
no live drift rerun/re-pin is claimed. Old red remains carried debt.

Live C1 command (`evidence/seat-live.json`, rc1) targets the current session
directory with exact prefixes TabiR17/TsukuroiR17/SoujiR17-3. At
`now_ms1792524914623`, settle900seconds, it reports469 observations:
completed368 / aged rate-limit94 / aborted6 / incomplete1 / unavailable0,
retry-exhausted90. Per-prefix aged rate-limit22/44/28. The earlier first-wave
zai-only tally18/44/28 and operator17/43/28+ are different times/filters, not a
constant incident count. Resumed-after-error remains a measured counterexample
to permanent death. No routing/fallback change was performed.

Source census start/end both rc0 with the existing W04 notices. `source-count.json`
reproduces40→48, A37→45/B2/C1, mined19→25/queued20→22/rejected1.
The wave2 preflight initially failed the explicit transcript-field clause;
`context-check-wave2-original.json` rc1→`context-check-wave2.json` rc0 after the
allowlist was spelled out. This was caught before dispatch, not repaired after it.

## Wave-2 findings and append-only precision corrections

Fresh wave2 dispatched 64 seats after three all-64 job-cap refusals. These are
author-lane falsifiers, not independent outside closure. The initial wave1
ClaimSeparability report predates C3; the later contract/SCORECARD declaration
supersedes its “conformance-only sweep” wording. C3 was committed before L1
measurements. All six scores remain held.

### Corrected verbatim quotes (supersede escaped-byte versions above)

The original S041/S042/S044 table accidentally retained JSON-style backslashes
around internal quotation marks. These are formatting defects, not changed
source facts. Correct byte-verbatim located quotes, all accessed 2026-10-20:

| Row | URL and location | Correct quote (≤25 words) |
|---|---|---|
| S041 | https://www.rfc-editor.org/rfc/rfc6585 §4, text lines 134–135 | The 429 status code indicates that the user has sent too many requests in a given amount of time ("rate limiting"). |
| S042 | https://www.rfc-editor.org/rfc/rfc9110#section-10.2.3 | Servers send the "Retry-After" header field to indicate how long the user agent ought to wait before making a follow-up request. |
| S044 | https://docs.jj-vcs.dev/latest/git-compatibility/ Colocated workspaces | jj commands will usually put the Git repo in a "detached HEAD" state, since in jj there is not concept of a "currently tracked branch". |

S045's quote location is CLI metaedit author options, lines 2220–2238, quoted
sentence at 2226 in its opening extract. Tier A is scoped to that official flag
description despite the page's experimental/generated label; it does not certify
all `/latest/` content against jj 0.45.1. The local help cross-check only verifies
the quoted flag. The commit-author limitation is an explicit boundary, not an
extra documented guarantee.

S043's HTTP/business-code mapping is primary-sourced; interpreting OMP's
`(type=NNNN)` transcript text as that business code is **[INFERENCE]**. Source
scope does not authenticate emitters. A2 binds code overrides to `provider=zai`
and treats bare `resource_exhausted` as unspecified cause rather than inventing
a rate-limit cause. S046 remains a load-bearing sourced C2 claim independently.

### Routing and source-file dispositions

- `JjAuditMori` call sites 1/2 are census grading row6 (fleet-root report presence/
  timestamp); audit 5/6 are grading row9 (lane revision/authorship). The C2 fix
  resolves each repository's own branch, never the child branch for a root report.
- `JjTrialMori.md` H1: cite only helper v2 `landed` after remote verification.
  H2: repo config lives outside .jj; isolated gate scratch uses HOME and
  XDG_CONFIG_HOME, and no live .jj copying is used. H3/H5: intent-to-add and jj
  index reset make cached staging reads unsuitable; only the helper tracks/
  commits live lane files. H4: no `@{u}` or attached-HEAD identity assumption.
  Its recommendations2–5 need no live config mutation: preserve helper config,
  explicit refs/unique master-main fallback, local scratch only, no real remote.
- Audit gate-side HEAD fields (rows10/12/15/17), r15/r16 env hardening and old
  .jj output guards remain historical residuals, not silently fixed. The r17
  successor gate uses explicit branch provenance and guarded output. Old gates
  were run only by L1 with scrubbed Git environment and safe evidence paths;
  wrapper branch-tip equality establishes their measured commit on this run.
- The new knowledge entries are `seat-terminal-status-r17.md` and
  `jj-branch-anchor-r17.md`; QUALITY gained Q43–Q48 append-only. A1 was developed
  after initial build dispatch but committed before the first measurements.
  A2 responds to fresh wave2 findings before final measurement. Existing SOURCES
  mutable cells stayed untouched throughout; new field metadata does not change
  that source-registry statement.
- The r16 checker used pre-wave1 had eight clauses **including**
  `no_live_journal_queries` (its committed source), not twelve. The r17 checker
  did not exist before wave1. Wave2 used the twelve-clause checker; neither
  result claims runtime prevention.
- The fleet report is intentionally absent during author-wave review because
  PROTOCOL requires it to land after child work. The header pointer must resolve
  at closure; its temporary absence is not claimed as an already-landed report.
- The original counts/tokens with missing typographic spaces above are historic
  prose defects. Full hashes in PINNED_INPUTS and raw counting receipts are the
  authoritative numeric records; `landed 273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7`
  is the correctly spaced first helper marker.

### Additional Mistakes / conduct precision

| ID | Class | Evidence pointer | Captured-by | Fix / disposition |
|---|---|---|---|---|
| M11 | scope | `falsify/ConformanceAudit.md` V2/V5; `build/JjGate.md:296–328` | wave1 sandbox/write bounds | Ad hoc pre-guard git/jj sandbox experiments without -R and accidental `/tmp/does-not-exist` are violations, not only “own selftests”. L1's C2 receipts use the guarded gate and do not rely on those experiments. No retroactive compliance. |
| M12 | scope | `falsify/ConformanceAudit.md` V6/V7/V12/V14 | QUALITY38/39, read-only jj clause | Entering census's hardcoded /tmp selftest write is inferred from code; MisrootSweep sandbox git writes exceeded its narrow exception; SentinelJjSandbox config-path lookup lacked ignore flag; some git-status calls lacked optional-lock guards. Retain these as scoped deviations, not proof of live data loss. |
| M13 | scope | `falsify/ConformanceAudit.md` V8–V10/V13 | transcript field allowlist | session_exit values, retry-recovery values and parse-then-discard credential records exceeded the stated projection. Those reads are excluded from admission evidence. A2 production projection skips unapproved values before materialization. |
| M14 | scope | `falsify/ConformanceAudit.md` V11 | bounded actor-trace assignment | PacmanActorTrace's shell-history/login/sudoers reads exceeded the command-log-only task. Retain only the command-stream/UUID correlation as bounded evidence; human actor identity remains unknown/inferred. No broader access is authorized. |
| M15 | vacuous | `falsify/MutContext.md` | new context selftest | Background-clause deletion survived because the host-service ban satisfied an overbroad alternative. A2 requires the background-job ban itself; old survivor stays retained and final red/green proof is separately recorded. |
| M16 | scope | `falsify/{PrivacyFinal,SandboxFinal}.md` | source/output invariants | A2 fixes walk-error false-clean, root/FIFO race, FIFO-parent escape, C2 output guards and inherited Git trace writes; final checks use settled committed corrections. |
| M17 | vacuous | `falsify/CaseReview{12,14,15,18,25,26}.md` | expected-field independence | A2 expected reason/records/top metadata prevents wrong reasons, missing relative keys, missing retry/main/duplicate counts from passing merely on classes. Existing initial green is finite and weaker, not rewritten. |
| M18 | reference-drift | `falsify/Receipt{Pins,Inputs,C3}.md`, `CriticC3Final.md` | independent witness pin | Initial C3 receipts omitted witness/tool hashes and the expected/recipe postdated that run. Final C3 uses precommitted expectations/recipe, hashes witness/tool/meaningful tracked+sibling controls before/after, and checks exact candidate sets. |

M8 precision: ReviewSkillRows ran three unflagged jj commands — `status`,
`diff --stat`, and `diff --git` (`build/ReviewSkillRows.md:37–38`). The observed
op45a25744584d snapshot is specifically the diff-stat command; a read-only
operation receipt records its args/time. No claim that all three were harmless
is made. M9's display remains a real breach; no values are copied into corpus.
Network source openings alone are not violations under the wave context (V15).
Host package events (V4) are detections by another session, not transactions by
these round-17 seats; whether an operator-scoped pause applied there is not
resolved by mori.

Resumed-after-error support is the field-only historical analyses in
`build/{CriticC1,TranscriptShapes,RetryRecoveryShape}.md`, not the one terminal
live scan. They falsify permanent-death interpretation even though the current
tool reports only terminal-at-scan state. C2 process exits1→0 are captured by
the outer `evidence/c2-{before,after}.json` wrappers, not inferred from a missing
exit_code key inside the nested manifests.

## Final-check oracle failure and bounded repair

At corrected source commit `2be82940828424ef4a2d623173d7e603b8a18f93`,
L1 ran checks from an isolated verification clone. Terminal selftest49 arms,
seat-gate selftest, jj-gate selftest, misroot12 arms, context31 arms and the
silence oracle28/28 returned rc0. Census selftest returned rc1:
`FAIL (132 cases, 131 passed, 1 failed)` with
`FAIL git env: trace canary written — GIT_TRACE* leaked to the Git child`.
The exact failed run is retained as `evidence/final/census-selftest.json`;
it is not silently overwritten by a later green.

| ID | Class | Evidence pointer | Captured-by | Fix / falsifier |
|---|---|---|---|---|
| M19 | vacuous | M3 census selftest trace-canary failure; common dispatcher source3034–3038 at that commit | independent fixture realism | The shared fake-binary dispatcher simulated Git trace writes for **all** binaries, including df/journalctl. Real non-Git binaries do not honor GIT_TRACE. Gate the simulator by executable name `git`; add direct positive Git-canary and negative df-canary controls, so disabling the canary cannot fake a pass. Production Git scrubbing is not weakened. Re-run only after this committed correction. |

This is a real test-oracle repair, not a new claim or suppression of an
observed production warning. Other passed instruments' source bytes remain
unchanged; final primary C1/C2/C3 measurements use the corrected committed
input set, and the failing receipt retains its original revision.

### Independent metadata failure, not an expectation reroll

At `fe9fa9083db998ead1554459d656568c4173f288`, the repaired census
selftest passed **134/134**. C2's fixed universe measured **204 assertions on
both sides, 60→0 failed**, cases7/17→17/17. C1 capability-absent before
recorded66 unmet requirements, but delivered initially matched **65/66**:
`long_code_13_digit_unknown` returned the correct `dead_error_other` class
while omitting its numeric `error_code`. The independent fixture required
`"9999999999999"`, consistent with the original digit-string contract.
`evidence/final/{c1-after.json,seat-after/run-manifest.json}` retains this failure.
The entering implemented prototype matched58/66 under the stronger table;
that is eight failed expectations, not eight distinct bugs.

| ID | Class | Evidence pointer | Captured-by | Fix / falsifier |
|---|---|---|---|---|
| M20 | scope | final C1 65/66 failure, LongCode13 record metadata | independent `want.records` expectation | An arbitrary 12-digit display cap contradicted the promised code-string extraction. Retain the complete numeric code within the already bounded input span, never convert it to a large integer; remove the now-redundant overflow-state bit. Keep the fixture unchanged and keep unknown Z.AI codes conservatively classified as other. |

The selftest's own long-code expected metadata is corrected to the same
contract; the separate fixture is not changed to make the run green. The
metadata failure and the earlier census oracle failure remain separate,
revision-pinned records. Other C2 inputs are unchanged by this C1-only fix.

## Final verified delivery scope

Final C1/C3 input commit: **91940fa339e38006f8db5bd7d78bb6f037f4d016**.
C2 input commit: **fe9fa9083db998ead1554459d656568c4173f288**; its census,
gate and frozen-control hashes are identical at the final C1/C3 commit.
`FINAL-PINNED_INPUTS.json` and `final-measurements.json` are the current
measurement indexes; the earlier declarations and failed receipts remain history.

| Claim | Final result | Actual evidence under `.ufo/waves/round-17/evidence/final/` |
|---|---|---|
| C1 coverage | **66→0** unmet, **66/66** match with the unchanged independently pinned fixture; 96 source-file pins | `count-c1.json`, `seat-after-fixed/run-manifest.json`, `stream-integrity.json` (132 exact streams) |
| C2 operability | **60→0** failed out of the same **204** assertions; **17/17** match after | `count-c2.json`, `jj-before/run-manifest.json`, `jj-after/run-manifest.json`; default scratch retention false |
| C3 calibration | known missed artifact **1→0**, unexpected candidates **0→0**, all strict controls match | `c3-fixture-setup.json`, `c3-before-pinned.json`, `c3-after-pinned.json`, `c3-assertions.json` (all input hashes bound) |

Other unprefixed receipt names in this closing section use that same
`evidence/final/` base; code/input ledgers remain at the round root.

The C1 tool's fixed selftest passes 49 arms. Census selftest passes 134/134.
The seat-gate/jj-gate selftests, misroot 12-arm selftest, context 31-arm
selftest and silence oracle 28/28 pass; unchanged instrument bytes allow
the M3 selftest receipts to remain valid at the final input pin. Final
preservation gates against the corrected census pass r13 24/24, r14 44/44,
r15 63/63 with frozen red 34/34. The seven historical instruments/pin bytes
remain unchanged (`evidence/final/preservation.json`). No live drift re-run or
re-pin is asserted.

The exact background-ban mutant that survived now returns rc1 with only
`no_background_jobs` missing, while its original returns rc0 and the positive
spec remains green (`context-survivor-before.json`, `context-survivor-after.json`,
`context-positive-after.json`).
The live-journal deletion remains correctly red. These are static instruction
checks only, never runtime prevention.

Fresh live C1 observation again reports **469** scoped files: completed 368,
aged rate-limit 94, aborted 6, incomplete 1, unavailable 0; retry-exhausted 90.
Actual answering labels for the aged-error cohort are **zai/glm-5.3-flash:93**
and **anthropic/claude-opus-5-5:1**. This is not an endpoint-health or incident
claim. The final live receipt canonical-redacts the directory identifier and
marks the transformation plus raw/canonical hashes. The older unredacted
identifier is metadata, not authentication; its retained history is not silently
rewritten. No raw live message, usage or credential payload is admitted.

Source census start/final both exit0, retaining only the existing W04 notices.
The final unrestricted `git status --porcelain` sweep has no pathspec and the
misroot detector reports **0 candidates**. Ten untracked entries belonged to
driver baselines or unattributed material; none was claimed or deleted as an
own-seat artifact. A transient `stdout.toon` was observed in status and was
already absent when read; ownership remains unknown. All driver state is left
unmodified. No runtime-prevention or universal-clean-fleet claim is made.

Both genuine waves settled **70/70** and **64/64** reports: **134** unique
identities, **0 reported dead**, no replacements. L1 holds planner; role mixes
and failed all-wave job-cap attempts are in `wave-settlement.json`. Resumed
correction writers kept their identities and isolated clones. No third wave or
new round was started.

Learning verdicts: expansion improved through the sourced bounded FR14 entry
and capabilities; quality improved through actual code/oracle/wording repairs;
discernment improved through prior non-author r16 disagreements becoming
Q43–Q46 and precise appended corrections. Author-lane findings produced
Q47–Q50 but are **not** outside agreement. Current non-author admit/reject
spotcheck remains pending. Execution is not fully conformant: conduct findings
V1–V15 and M8–M20 retain their admitted/inferred/non-violation dispositions and
actual failures. No SHONEN promotion, new L0 question, tool install/update,
package transaction or service action is claimed.
