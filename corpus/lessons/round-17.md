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
