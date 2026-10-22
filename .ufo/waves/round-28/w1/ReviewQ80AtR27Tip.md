# ReviewQ80AtR27Tip — QUALITY 80 at the round-27 boundary (mori round 28, wave 1)

Seat: MoriR28.ReviewQ80AtR27Tip (reviewer, leaf). Date: 2026-10-22.
Lane: /home/vgpnk/Projects/shokunin/mori-shokunin; every path below is relative to the lane root.
Tip during this review: `079a47c` (079a47c61691f2b891d35458057b294ca5a99e77); entering tip `6ebd518`.
Criterion: corpus/QUALITY.md:370-374 (80). Method: read-only git only (`log --name-status`, `show`,
`diff`, `status --porcelain`, `ls-files`, `rev-parse`) plus file reads; every command quoted here was run
in this review. The lane is worked by sibling seats concurrently, so the §2 and §4 snapshots carry that
caveat explicitly. No tool was installed or upgraded (none needed).

## 1. Reference commits (round 27)

Source: `git log --format='%h %ci %s' --name-status -- .ufo/waves/round-27/` (round-27 subset below)
and `git show --name-status 6ebd518 079a47c`. All times 2026-10-22, -03:00.

| Commit | Time | Seat-report content |
|---|---|---|
| 761b4cd | 12:42 | none (contract, counters, before evidence) |
| 5fa0a00 | 12:45 | none (wave-1 spec, dispatch) |
| dd4dbb2 | 12:50 | none (amendment W1) |
| 126e192 | 12:58 | 23 w1 reports + w1/swarm-registry.json |
| 79ecf58 | 13:05 | 4 w1 reports |
| 5f00fd0 | 13:07 | none under .ufo/waves/round-27/ |
| 0becc42 | 13:08 | none (wave-2 spec, dispatch) — last report-free round-27 commit |
| b97b2e3 | 14:08 | none (evidence/c1-after.txt only) |
| b89ac34 | 14:15 | 5 w2 reports + w2/swarm-registry.json |
| 47f6543 | 14:17 | 3 w2 reports |
| 5e500d9 | 14:20 | 2 w2 reports |
| 9c2c7de | 14:23 | 12 w2 reports (ReopenS136 modified) |
| df886be | 14:24 | 3 w2 reports (ReopenS137, ReviewEntryFact1 modified) — last round-27 commit |
| 6ebd518 | 14:50 | outside verifier spot-check: adds corpus/lessons/round-27-verifier-spotcheck.md; touches no round-27 wave file |
| 079a47c | 14:56 | round-28 declaration; modifies .ufo/waves/round-27/contract.md (+8) |

## 2. QUALITY 80's own check — untracked under .ufo/waves/round-27/ now

`git -C <lane> status --porcelain --untracked-files=all -- .ufo/waves/round-27/` printed nothing on the
first run. 71 files are tracked under the dir (`git ls-files .ufo/waves/round-27/ | wc -l` → 71).

On a second run minutes later the same command printed ` M .ufo/waves/round-27/contract.md`: an
uncommitted +5-line block "Correction to the correction above (round 28, wave-1 CriticRoutingCoverage)",
which corrects the committed block's time bound (see F3). `git diff --stat` at the same moment also showed
` M corpus/SOURCES.md` (3 rows: S096, S097, S101 — the in-flight C1 restore edits). Both are in-flight
round-28 work, expected mid-wave; both must be committed (or withheld with a reason) before round-28's
final commit (QUALITY 80 with N=28).

[INFERENCE] At df886be the dir was fully committed: no file was added under the dir after df886be (the
only later change is 079a47c's modification of the already-tracked contract.md), and the dir holds no
untracked file now. `git status` cannot be run at a past commit, so this is reconstruction, not a re-run.

## 3. r27 seat reports committed after the round's last pre-report commit

Two readings, both answered.

**(a) QUALITY 80's own reference — the round's final commit df886be (14:24:06).** Zero r27 seat reports
were committed after it. Only two later commits touch round-27 files, and both have an explicit
disposition path:

- 079a47c: `M .ufo/waves/round-27/contract.md`, +8 lines — "Correction to amendment W1 (round 28,
  appended 2026-10-22; W1 above is not rewritten)", fixing a future-dated heading (15:55Z vs the
  `dd4dbb20` committer bound 15:50:10Z); the block names its own routing: round-27-verifier-spotcheck
  routed defect 1 → `corpus/lessons/round-28.md` M1.
- 6ebd518: added `corpus/lessons/round-27-verifier-spotcheck.md` — the post-final-commit lane file, and
  the same 079a47c block routes its defect 1.

So QUALITY 80's second clause ("every file a seat wrote after that commit is named in the next round's
lesson") is vacuous for round 27: no late seat report exists. This empty set should be stated in the
round-28 lesson (§6 item 4).

**(b) The assignment's reference — 0becc42 (13:08:31), the last round-27 commit carrying no seat report.**
The 25 wave-2 seat reports were committed after it (paths under .ufo/waves/round-27/):

- b97b2e3 14:08: evidence/c1-after.txt (not a seat report)
- b89ac34 14:15: w2/ConnAdjacencyCheck.md, w2/CriticDecisionVsKernelKill.md, w2/CriticRowIdentityCheck.md,
  w2/CriticSingleOmpProcess.md, w2/ScoutMisroot.md (+ w2/swarm-registry.json)
- 47f6543 14:17: w2/CriticCeilingInference.md, w2/CriticEntryOverclaim.md, w2/CriticSkillWrongTurn.md
- 5e500d9 14:20: w2/CriticC1Admission.md, w2/ReopenS136.md
- 9c2c7de 14:23: w2/ReopenS127.md, w2/ReopenS128.md, w2/ReopenS129.md, w2/ReopenS131.md,
  w2/ReopenS134.md, w2/ReopenS137.md, w2/ReopenS140.md, w2/ReviewEntryFact1.md, w2/ReviewHygieneR7.md,
  w2/ReviewPrivacyLanded.md, w2/SupersedeS090.md, w2/SupersedeS093.md
- df886be 14:24: w2/ReopenS133.md, w2/ReopenS135.md, w2/ReviewHygieneD2.md

(The wave-1 reports at 126e192/79ecf58 pre-date 0becc42; round-27.md is authored from them — its header
names the w1 directory and its routed-disposition table cites w1 files by pointer.)

**Does corpus/lessons/round-27.md name their disposition?** Grep over the lesson for all 25 file stems
(zero-hit stems listed in the last bucket):

| Bucket | Files | Lesson evidence |
|---|---|---|
| Named by seat | CriticSingleOmpProcess; ReopenS127; ReopenS128; ReopenS129; ReopenS131; ReopenS140 | round-27.md:18, :81, :125-128 |
| Content-dispositioned, seat unnamed | ConnAdjacencyCheck ("adjacency lines"); CriticDecisionVsKernelKill ("earlyoom-versus-kernel event routing rows"); CriticCeilingInference ("the ceiling inference's conditions and its upper bound of 27"); CriticEntryOverclaim ("sixteen overclaim wordings"); CriticRowIdentityCheck ("the hardened row-identity check"); SupersedeS090 + SupersedeS093 ("S090 and S093 restored with superseding rows S143 and S144") | round-27.md:120-124 (Applied bullet) |
| Partially dispositioned by content | CriticSkillWrongTurn (F1 → "the earlyoom order being unknown under the host's armed prefer and avoid expressions"; F6 → the `omp` process count; F2/F5 → "the Arch packaged `--avoid`"; F7/F8 have no lesson mapping); ReviewPrivacyLanded (the withhold bullet at :129-131 matches its sweep scope but names no seat) | round-27.md:120-124, :129-131 |
| Neither named nor content-dispositioned | CriticC1Admission; ReopenS133; ReopenS134; ReopenS135; ReopenS136; ReopenS137; ReviewEntryFact1; ReviewHygieneD2; ReviewHygieneR7; ScoutMisroot | zero grep hits |

QUALITY 80's letter requires next-round dispositions only for files written after the final commit, so
the last bucket is compliant-by-letter. But those reports' open findings are routed nowhere:
`.ufo/waves/round-28/contract.md` contains no S133, S134, S135, S136 or S137 token (case-insensitive
grep, zero hits), and C1's eight superseding rows (S145-S152) cover S096/S097/S101/S127/S128/S129/S131/
S140 only. The lesson's M2 promise "their disposition is recorded below" (round-27.md:43) is kept by the
Applied/Carried bullets (:120-128) for the rows it names, not for the bucket-4 reports.

## 4. Untracked files anywhere in the lane now

Command: `git status --porcelain --untracked-files=all` (snapshot taken during wave 1, after 079a47c;
the lane was being edited concurrently). Groups:

1. `.scratch/` — 3,639 entries, all round-22 mutation-measurement scratch (measure1-3, trial1-3, one
   html). None gitignored. Standing litter from round 22.
2. Lane root — 7 files, all mtime 2026-10-22 14:08:55 -03:00: `MANPAGE.md`, `base.c`, `main.c`,
   `meminfo.c`, `oom_kill.c`, `sd-main.c`, `user@.service.in`.
3. `.ufo/waves/round-28/` — in-flight wave-1 outputs (9): wave1-spec.json, wave1-dispatch.json,
   wave1-run.json, wave1-run.err, w1/swarm-registry.json, w1/ScoutSurfaceRecon.md,
   evidence/misroot-before.txt, evidence/misroot-after.txt, misroot-hash-check.sh.
4. Modified tracked (not untracked; listed for completeness): .ufo/waves/round-27/contract.md (+5),
   corpus/SOURCES.md (S096/S097/S101 rows).

Group 3 is normal mid-wave state. Groups 1 and 2 are standing litter (see F1).

## 5. Findings by severity

**F1 (medium) — QUALITY 80's evidence command cannot see lane-root litter, and seven such files sat
untracked through the round-27 close and still do.** The seven files in §4 group 2 all carry mtime
2026-10-22 14:08:55 -03:00 — 19 s after b97b2e3 (14:08:36) and 15 minutes before the final round-27
commit df886be (14:24:06). The criterion's check (`status ... -- .ufo/waves/round-27/`,
corpus/QUALITY.md:371-372) passed at that close, and passes now, while these files sat outside the
checked path the whole time. They are exactly the byte set of round-27's claims (earlyoom main.c,
meminfo.c, sd-main.c and manpage; kernel base.c and oom_kill.c; systemd user@.service.in template).
round-27.md names no disposition for them, and wave-2 ScoutMisroot swept the fleet root, not the lane
root (ScoutMisroot.md:1-5). [INFERENCE] A wave-2 seat fetched sources into the lane root instead of its
scratch dir, contrary to the write-bounds; the seat is not identifiable from mtimes alone.

**F2 (medium) — eleven wave-2 reports have no disposition anywhere, and their open findings are routed
nowhere.** The bucket-4 list in §3. Concretely open, from the reports' own summaries:

- ReopenS133 — H1 "QUALITY 81 is unmet at the landed tip, and the lesson does not say so" (check prints
  `changed=5`, exit 1 at 5f00fd04) and M1 the r26 entry's citation map omits S133
  (ReopenS133.md:105-111). Round-28 C1's S096/S097/S101 restores close H1 once landed; M1 is not
  carried by C1.
- ReopenS134 — M1-M4: the scope cell claims a cap refusal the row's bytes do not contain; SKILL.md:646
  grounding; four stale commit ids and a reused id S134 in ReviewR7Knowledge.md (ReopenS134.md:9-11).
  No superseding row for S134 in C1.
- ReopenS135 — teaches second clause ("same session-wide cap") wrong for the pool job
  (ReopenS135.md:9-10). Not carried.
- ReopenS136 — H1 false teaches clause ("results: [] belongs to the all-refused shape only"), M1
  over-general clause, and wrong citations at ReviewR7Knowledge.md:64 and :160 (ReopenS136.md §0). Not
  carried.
- ReopenS137 — M1 "merged" unsupported (one parent, no pull request); M2 the row's commits URL does not
  return the anchor's first-page-of-100; M3 the v1.9.0 `main.c:245-246` anchor attributed to no row, plus
  the adjacent dangling "(§3.3)" pointer (ReopenS137.md:33-38). Not carried.
- ReviewEntryFact1 — M1-M5 (wrong MANPAGE quote at MANPAGE.md:20-21, `-p` conflict, `--sort-by-rss`
  ±300 error, zero-RSS order, incomplete skip list) and R1-R3 (S115/S118/S119 do not record the lines
  Fact 1 cites) (ReviewEntryFact1.md:11-20). Not carried.
- ReviewHygieneD2 — M1-M3: dangling section pointers in the r26 entry survive although round-27.md:107
  records r26 D2 as "fixed" — a standing QUALITY 77 contradiction (ReviewHygieneD2.md Summary and M1
  block). Not carried.
- CriticC1Admission — verdict "verified (C1 is met for the right reasons), with six fixable defects",
  exact corrections in its §6 (CriticC1Admission.md:6-9, :169). Applied-or-not is recorded nowhere.
- CriticSkillWrongTurn and ReviewPrivacyLanded — see the partial bucket in §3; the unmapped parts (F7/F8;
  the sweep's own verdict) need a disposition line.
- ScoutMisroot — found one expected orchestrator log line and concluded the residual directory can be
  ignored (ScoutMisroot.md:7-9); record the no-action disposition.

**F3 (low) — the committed W1 correction asserts a time bound its own follow-up retracts.** 079a47c
committed "the amendment existed no later than 15:45:38Z"; the uncommitted working-tree block
(CriticRoutingCoverage) corrects it: in this jj-colocated lane a commit's author time is when its empty
change was opened, so the proven bound is dd4dbb20's committer time, 15:50:10Z. Until the +5 lines are
committed, HEAD carries the unproven claim.

**F4 (info) — in-flight round-28 edits touch round-27 files.** The +5 contract.md block and the
S096/S097/S101 restore edits are uncommitted now (§2). Legal mid-wave; both must land (or be withheld
with a reason) before round-28's final commit, and the contract.md edit must be named in the round-28
lesson exactly like the 079a47c one.

## 6. Dispositions the round-28 lesson must record

1. The 079a47c post-close correction to .ufo/waves/round-27/contract.md (+8) — committed as a correction,
   routed from round-27-verifier-spotcheck defect 1 to round-28.md M1 (the block names this itself).
2. The uncommitted +5 "correction to the correction" (CriticRoutingCoverage) — commit before the round-28
   final commit, or withhold with the reason.
3. The seven untracked lane-root source files (§4 group 2) — removed or moved with the reason; and the
   QUALITY 80 scope gap (F1: the check's path scoping misses lane-root litter) as a routed defect or a
   criterion amendment, logged old → new.
4. The empty set: no r27 seat report was committed after df886be — state it so the criterion's second
   clause is on record as vacuously met for round 27.
5. A disposition line for each of the eleven §3 bucket-4 reports (applied in wave 2 / carried as debt /
   not carried), at minimum the open findings in F2 that round-28 C1 does not carry: ReopenS133 M1;
   ReopenS134 M1-M4; ReopenS135; ReopenS136 H1/M1; ReopenS137 M1-M3; ReviewEntryFact1 M1-M5 and R1-R3;
   ReviewHygieneD2 M1-M3; CriticC1Admission §6.
6. The corpus/SOURCES.md S096/S097/S101 restore edits — land with C1 and record the row-identity check
   flipping to `changed=0`, exit 0 (this also closes ReopenS133's H1).
7. The wave-1 in-flight outputs (§4 group 3) — commit before the round-28 final commit (QUALITY 80,
   N=28).

## 7. Verification gaps and residual risk

- Snapshot race: sibling seats are actively editing the lane; §2 and §4 were true at the moment of each
  command and will drift (the contract.md +5 block appeared between my first and second status runs).
- The at-df886be cleanliness claim is reconstruction [INFERENCE] (§2); `git status` cannot run at a past
  commit.
- F2 items were read from each report's own summary/verdict section, not every report in full; the
  lesson's disposition lines should be drafted from the full reports.
- The writer of the seven lane-root files is inferred from mtimes only.
- corpus/lessons/round-28.md does not exist yet (corpus/lessons glob at check time); §6 is a
  requirements list for a lesson not yet written.

Tooling record: no tool installed or upgraded by this seat (none needed); read-only git and file reads
only; no pacman transaction; no subagents, no background jobs.
