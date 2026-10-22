# ReviewLateW2Reports — round-27 wave 1 (seat MoriR27.ReviewLateW2Reports)

Date: 2026-10-22. Scope: the four uncommitted round-26 wave-2 files in
`.ufo/waves/round-26/w2/` (one modified, three new), the corrected wave-2 tally, and the
round-26 report and closure-lesson comparison. Leaf seat: no subagents, no background jobs.
Everything below was read or run; nothing is inferred unless marked `[INFERENCE]`.

Method (all read-only, no writes outside this report):

- `git -C <lane> diff --stat` and `git -C <lane> diff -- .ufo/waves/round-26/w2/OperabilityNoHarm.md`
- `git -C <lane> status --porcelain -- .ufo/waves/round-26/w2/`
- `git -C <lane> ls-tree --name-only fc09f96c .ufo/waves/round-26/w2/` and the same at `ef9dbee1`
- `git -C <lane> merge-base --is-ancestor ef9dbee1 fc09f96c` (true)
- Full reads of the four files, `.ufo/waves/round-26/wave2-run.json`,
  `/home/vgpnk/Projects/shokunin/.ufo/reports/round-26/mori.md` (read-only),
  `corpus/lessons/round-26-verifier-spotcheck.md:31,:48-52`.
- Tooling record: no tool installed or upgraded; read-only git, grep and file reads only.

## 1. The modified file: OperabilityNoHarm.md

`git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --stat`:

```
 .ufo/waves/round-26/w2/OperabilityNoHarm.md | 16 ++++++++--------
 1 file changed, 8 insertions(+), 8 deletions(-)
```

`git status --porcelain` for the directory shows exactly four entries: ` M` on
OperabilityNoHarm.md and `??` on ReopenS116S117.md, ReopenS118S119.md, ReviewEntryOomdFacts.md.
The other three files are untracked, so they cannot appear in `diff --stat`.

Summary of the change (full diff read): 8 lines reworded, prose only, in six hunks —

1. Verdict paragraph: "byte-identical to the blob or tree recorded in round 24 or round 25"
   becomes "the tool and fixture bytes at the pin are the bytes behind the last recorded run
   (table, column 6)".
2. Method item 3: drops one redundant `git rev-parse` form; blob identity is now also compared
   "with the round-24 and round-20 records" (was round-25 evidence files only).
3. Method item 7: tools sentence merged into one.
4. Results row 8 ("last recorded result" cell): the compressed "say 7/7 and 28/28" becomes the
   split per-source wording (`SCORECARD.md:1525` says `PASS 7/7`; `corpus/lessons/round-24.md:100`
   says `PASS 7/7` and `MATCHER: rejected 28/28`). Same numbers.
5. Finding F3 evidence/attacks bullets: same split per-source wording and a punctuation fix.
6. F4 bullet and the residual-risk RetentionTip sentence: reworded (R4a named directly;
   RetentionTip named as a sibling seat).

No verdict, exit code, tally, hash or path value changes. This matches the closure lesson's
ruling that the diff is "8 lines of prose rewording; verdict, method, the five exit codes and
every tally are unchanged" (`corpus/lessons/round-26-verifier-spotcheck.md:43`, the
OperabilityNoHarm row of the five-path rulings table).

## 2. The four files: completeness and privacy

Privacy bounds applied: no operator settings values, session ids, session-store paths or
session-record fields; no journal `MESSAGE` text naming a process, command line, uid or pid
list; no `/etc/default/earlyoom` values; no `--prefer`/`--avoid`/`--ignore` expression values
(presence only). The closure lesson already ran the lane's frozen retention regex classes over
all four files: 0 matches in each (`corpus/lessons/round-26-verifier-spotcheck.md:45`). My own
read of all four agrees; the sweep below adds what a regex cannot judge.

| File | State | Complete? | Privacy |
|---|---|---|---|
| `w2/OperabilityNoHarm.md` | tracked, modified (uncommitted 8-line rewrite) | Yes: verdict, method, five-command table, extra-runs table, findings F1–F4, residual risk, reproduction block, privacy note | Clean. Tool outputs, tallies, commit/blob hashes and lane paths only |
| `w2/ReopenS116S117.md` | untracked | Yes: verdicts (S116 holds; S117 defect medium D1 with minor D2–D6, info D7), per-row method, fetch log with sizes/hashes, not-run list | Clean. URLs, byte counts, sha256 values, registry line citations only |
| `w2/ReopenS118S119.md` | untracked | Yes: verdict table (S118, S119 hold), anchor lists with quoted lines, gate-quote checks, one minor observation, residual risk | Clean, with one note: it quotes the upstream `kill.c:617-627` action format literal, which contains the placeholders `uid %d` and `cmdline "%s"`. This is a C format template from public source, not journal `MESSAGE` text, and carries no actual uid, pid or command line. Within bounds |
| `w2/ReviewEntryOomdFacts.md` | untracked | Yes: verdict table O1–O21 with per-row sources, findings by severity, explicit not-run marks (O7, O21), tooling record | One flag, see F-2 below. All journal reads are reported as key names and counts only; the file itself states values were not printed |

All four are complete reports in the round-26 sense: each names what it attacks and gives a
verdict (holds / defect with severity / not run). None is a stub or fragment.

## 3. Findings

**F-1 (conformance, status-neutral; confirms round-26 routed D1 still open at `fc09f96c`).**
The round-26 report rests one statement on uncommitted bytes. `/home/vgpnk/Projects/shokunin/.ufo/reports/round-26/mori.md:75`
cites ReopenS116S117's finding ("Wave-2 ReopenS116S117 found S117's description … differs"),
but `.ufo/waves/round-26/w2/ReopenS116S117.md` is absent from `git ls-tree fc09f96c` and sits
untracked in the working tree. The closure lesson routed this as D1
(`corpus/lessons/round-26-verifier-spotcheck.md:46`, ReopenS116S117 row: "round work,
uncommitted … Conformance defect (status-neutral); routed D1"). Nothing since has committed the
file, so the defect stands. Fix: commit the file (its content is complete and privacy-clean).

**F-2 (low, privacy-bound mismatch; actionable before any round-27 commit).**
`ReviewEntryOomdFacts.md:23` names a systemd user-slice unit with the numeric uid embedded
(the `user-<uid>.slice` name; value not repeated here). Judgements:

- Against the round-26 seat bound as written, this is not a violation: that bound forbids uid
  naming inside journal `MESSAGE` text, and line 23 is the seat's own host read of unit
  properties, not journal text.
- Against the round-27 contract's binding privacy clause ("never a command line, a uid, a pid
  list, journal MESSAGE text, …", `.ufo/waves/round-27/contract.md` C1 section), it is a uid in
  committed bytes.
- The lane's frozen retention scan does not catch it (0 regex matches, lesson line 45), so
  committing the file as-is would not raise the scan — it would still breach the round-27
  phrasing.

Fix if the L1 adopts these files: redact to `user-<uid>.slice` (or "the per-uid user slice")
before committing. No other line of the four files carries a bound-forbidden value.

**F-3 (info).** The uncommitted OperabilityNoHarm.md rewrite changes no recorded result. The
closure lesson's ruling stands: "a late rewrite by the returned seat. Not new round work; the
committed version is the evidence this note uses" (`corpus/lessons/round-26-verifier-spotcheck.md:42`).
If the L1 lands the rewrite, no tally in any record changes.

**F-4 (info, wording).** The round-26 report's cancelled list overstates "cancelled with no
file" by two: ReopenS118S119 and ReviewEntryOomdFacts are listed as cancelled
(`/home/vgpnk/Projects/shokunin/.ufo/reports/round-26/mori.md:98`) yet both wrote complete,
verdict-bearing reports that sit uncommitted (ruling rows at
`corpus/lessons/round-26-verifier-spotcheck.md:44-45` say the same: "late output of a seat the
report counts as cancelled"). Cancellation as an L1 event remains true for all 15; the file
level is what the corrected tally below fixes.

## 4. Corrected wave-2 tally

Inputs:

- Seat list: `.ufo/waves/round-26/wave2-run.json`, `registry.members` — 34 members: 22 reviewer,
  6 critic, 5 mutation-tester, 1 scout (`counts.spawn` = 34; same split as the report's shape
  line, `/home/vgpnk/Projects/shokunin/.ufo/reports/round-26/mori.md:98`).
- Committed report files at `fc09f96c`: `git ls-tree --name-only fc09f96c .ufo/waves/round-26/w2/`
  lists 17 `.md` reports plus `swarm-registry.json`. The 17: the 6 critics
  (CriticA2Amendment, CriticC1Admission, CriticCapabilityRow, CriticEntryOverclaim,
  CriticMistakes, CriticRoundConformance), the 5 mutation-testers (MutC1Script,
  MutPostFreezeRules, MutToolBatteryA, MutToolBatteryB, MutToolBatteryC), the scout
  (ScoutMisroot), and 5 reviewers (OperabilityNoHarm, ReopenS114S115, ReopenS120S126,
  RerunC1Count, RerunC2Count).
- Working tree: `git status --porcelain` — 3 untracked report files (ReopenS116S117,
  ReopenS118S119, ReviewEntryOomdFacts) plus the modified committed OperabilityNoHarm.md.
- The same directory listing at `ef9dbee1` (round-26 pushed tip, an ancestor of `fc09f96c`) is
  identical, so admission dropped nothing; the files were never committed.

Buckets (seat → evidence):

- Returned with a committed report: 17 — the ls-tree list above.
- Returned, report withheld from the lane: 1 — RetentionTip; not in the cancelled list, and the
  report discloses the withholding with the scratch location
  (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-26/mori.md:105`).
- Returned late (file present but uncommitted): 3 — ReopenS116S117 (a returner: absent from the
  cancelled list and cited as found by the report, line 75), ReopenS118S119 and
  ReviewEntryOomdFacts (both in the report's cancelled list, line 98, yet both files exist and
  are complete).
- Cancelled with no file: 13 — the 15 listed cancelled minus the two that wrote; the 13 are all
  reviewers: ReviewR12Rewrite, ReviewEntryEarlyoomFacts, ReviewEntryCapturePointers,
  ReviewEntryAdjacency, ReviewStaleSweepTip, ReviewToolCode, ReviewToolLive, ReviewToolPrivacy,
  ReviewSkillTable, ReviewRegistryRows, ReopenS121S124, ReopenS122S123S125, ReviewLessonGate.

Arithmetic: 17 + 1 + 3 + 13 = 34. Reviewer check: 5 committed + 1 withheld + 3 late + 13
no-file = 22; all 6 critics, 5 mutation-testers and the scout returned and committed.

Comparison with the round-26 report (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-26/mori.md:98`):
"19 returned, 15 cancelled by the L1 at the run-budget stop". As seat events that is exact
(19 = 17 committed + RetentionTip + ReopenS116S117; 15 cancellations all happened). As file
reality it is short on both ends: only 17 returned reports are committed bytes at `fc09f96c`,
and 2 of the 15 "cancelled" seats did write complete reports. The report also discloses the
RetentionTip withholding itself (line 105), so the tally sentence is the only place the two
numbers mislead.

Comparison with the closure lesson: my independent recount agrees with it everywhere it speaks.
Line 31 (seat-shape row): "wave 2: 34 (22 reviewer, 6 critic, 5 mutation-tester, 1 scout),
17 reports committed". Lines 48–52 (attack-share paragraph): "19 returned (17 committed,
`RetentionTip` withheld, `ReopenS116S117` uncommitted)" and "Cancellation: 15 of 34 wave-2
seats (44%) by the L1 at its run budget, not dead seats". The only refinement I add is the
explicit file-level wording: "cancelled with no file" is 13, not 15, because two cancelled
seats left files — which the lesson's own ruling rows already record individually.

### Exact corrected tally sentence (ready to paste)

```
Corrected wave-2 tally (seats: wave2-run.json registry.members; committed bytes: git ls-tree
fc09f96c .ufo/waves/round-26/w2/; working tree: git status --porcelain, 2026-10-22): 34
dispatched; 17 returned with a committed report; 1 returned with its report withheld from the
lane by the round-26 privacy rule (RetentionTip, disclosed in the round-26 report); 3 returned
late with a file present but uncommitted (ReopenS116S117 — a seat the report counts as returned
— plus ReopenS118S119 and ReviewEntryOomdFacts, both counted as cancelled); 13 cancelled with
no file. The round-26 report's "19 returned, 15 cancelled" is exact on return and cancellation
events but wrong at file level: only 17 returned reports are committed bytes at fc09f96c, and 2
of the 15 "cancelled" seats did write complete reports.
```

## 5. Residual risk and verification gaps

- The "late" bucket is true of the working tree now; any commit of the three files flips them
  to "returned with a committed report" and the sentence needs re-running. The committed-side
  numbers (34 seats, 17 reports) are revision-pinned at `fc09f96c` and stable.
- I did not re-verify file mtimes (the lesson's evidence for "late rewrite" vs "late output");
  I verified state, completeness and content directly, which is what the tally needs.
- I did not open the withheld RetentionTip report in scratch; its existence and location are
  cited from the round-26 report (line 105). Its content is outside this seat's scope.
- The retention regex claim (0 matches) is cited from the lesson (line 45), not re-run; my full
  read plus the targeted sweep found no forbidden value except the F-2 uid naming, which the
  frozen regexes do not model.
- [INFERENCE] The three untracked files are the seats' own final outputs, not drafts: each is
  self-contained, carries a verdict section and a not-run/residual section, and two of them are
  consistent with findings the round-26 report and lesson cite (S117 mismatch; O10 re-check).

Privacy: this report carries counts, file names, line references and verdicts only; no settings
value, session data, journal MESSAGE text, earlyoom expression or uid value is reproduced.
