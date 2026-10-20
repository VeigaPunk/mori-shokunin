# RoutedDebt — r15 verifier queue mapped to active r16 draft owners

Seat: `MoriR16.RoutedDebt` (scout, leaf). Read-only except this report.
Read time: 2026-10-20T05:47–05:57-03 (08:47–08:57Z), plus one later
reconciliation read of the in-flight `Lesson`, `QUALITY` and `SKILL.md`
revisions. Entering HEAD `b83edc6ee3db6822382ab673d7e6e984e420f22f`. The
round-16 tree was moving throughout; every state below is a read-time
observation, not a settled verdict, and later revisions are marked as such.

Execution: none. No builds, tests, gates, selftests, fixture runs, journal
queries, background jobs started for probing, `/tmp` writes, installs or
commits by this seat. Method: full file reads, `git show/diff/status`,
`grep`, `ls`, plus the already-published seat reports. No live journal was
read and no production tool was executed (all three r16 `tools/mori-*` files
were absent at first read; only the context-check file appeared later).

## Source of truth and boundary

- **Full r15 verifier** (the document this map covers):
  `corpus/lessons/round-15-verifier-spotcheck.md`, 302 lines. Read in full
  (`:1-163`, `:164-302`; raw re-read `:96-165`, `:196-302`). Its routed queue
  is the `## Procedural adjudication and routed defects` open queue,
  items 1–5 at `:260–293`, plus the binding statements at `:295–302`.
- Supporting r15 record: `corpus/lessons/round-15.md` (M1–M6), the r15 final
  measurements in `LOG.md`, and `SCORECARD.md` round-16 row.
- **Not the Mori queue:** `/home/vgpnk/Projects/shokunin/.ufo/waves/round-15/reviewer-final.md`
  is the fleet/protocol closure review. `grep -c mori` over it returns `0`;
  its gate gaps (unparseable `closed_at`, 9-digit runIds, `unknown_lane`
  asymmetry) belong to the protocol/gate owner, not to a Mori seat. It is
  therefore not mapped below.
- Owner ids are taken from the dispatched seat list
  (`.ufo/waves/round-16/wave1-spec.json`, `wave1-assignments.json`,
  `build/swarm-registry.json`), not inferred from report style.

## Axes named (godspeed)

1. **Ownership completeness** — every routed obligation has a named active
   artifact owner, or is explicitly reported unowned.
2. **Append-only correctness** — historical r15 files stay byte-untouched;
   corrections live in `corpus/lessons/round-16.md` and the active registry.
3. **Active-registry truth** — `SKILL.md` matches delivered bytes, not a
   superseded flag contract.
4. **Non-claim preservation** — red drift, trust, victim, completeness and
   fixture/live limits survive the new capability.

Move rule kept: only evidence-backed observations; no edit to any other
owner's artifact.

## Routing table — five numbered verifier items

| # | Verifier requirement (line anchor) | Required correction | Active owner(s) — exact seat / file | Read-time state | Status |
|---|---|---|---|---|---|
| 1 | Wave-context omission / broadcast prevention (`:260–266`): append an M4 correction assigning the omission to L1; carry exact-id/no-broadcast in future contexts; do not call the admonition a tested repair | r16 lesson correction; QUALITY criterion; future-context restriction; static check | `MoriR16.Lesson` → `corpus/lessons/round-16.md` (C15-1, M1); `MoriR16.Quality` → `corpus/QUALITY.md` Q37; `MoriR16.ContextGuard` → `tools/mori-round16-context-check.py`; L1 → wave context + `LOG.md` | C15-1/M1 landed: responsibility assigned to the planner, seat broadcast kept as a violation, "untested admonition only". Q37 landed. Both `wave1-spec.json` and `wave1-dispatch.json` carry the prohibition (`grep`: 2× `agent://all`, 1× `agent://MoriR16`, all prohibition text). LOG round-16 calls it "a static instruction repair, not … proof of runtime broadcast prevention". Context-check tool present, unexecuted. | **Covered forward.** See F7 for the token-count caveat. Retrospective wording: HistoricalCorrections item 1 marks `round-15.md` M4 append **OPEN**; verifier says do not rewrite prior lessons, so an append is permissible but not yet landed (L1 choice). |
| 2 | Outside-lane writes beyond downloads (`:267–276`): append the omitted `--pin-fixtures /tmp/mori-r15-expected-probe-final.json` instance to procedural debt; keep future probe output in authorized scope | r16 lesson correction naming path and source lines; probe-path criterion | `MoriR16.Lesson` → C15-2/M2; `MoriR16.Quality` → Q38; `MoriR16.AttackPermission` → report | C15-2/M2 landed with `.ufo/waves/round-15/build/HarnessBuild.md:256` and `:248–268`, plus RegistryFrontier. Q38 first said "round 16 omitted"; the later revision cites `#M2 (= C15-2)` without that attribution (F2 history). | **Covered; attribution fixed at later read.** |
| 3 | Mid-flight verification not authorized (`:277–287`): append the implementation-vs-execution distinction; preserve the historical report; only final L1 receipts count | r16 lesson correction; selftest criterion; contract | `MoriR16.Lesson` → C15-3/M3; `MoriR16.Quality` → Q39; `MoriR16.AttackPermission`; L1 contract | C15-3/M3 landed: implementation of a selftest arm is not permission to execute it; early seat checks inadmissible; final L1 runs are the admissible verification. Lesson also corrected the verifier's pointer: `report:301–307` is `.ufo/waves/round-15/build/HarnessBuild.md:301–307`; the fleet `mori.md` has only 149 lines. | **Covered.** See F6: preserve the corrected pointer. |
| 4 | Correction sweep missed active registry prose (`:282–287`): `SKILL.md:134` still claimed hidden `--selftest-child`; correct the active registry in the next lane-authored commit and append the lesson-backed disposition; do not rewrite `build/SkillInterface.md:88` | Replace the stale r15 self-test cell; add r16 rows; lesson disposition | `MoriR16.SkillRegistry` → `SKILL.md`; `MoriR16.Quality` → Q40; `MoriR16.Lesson` → C15-4/M4; `MoriR16.ReviewRegistry` | **Fix landed (uncommitted).** The r15 row (line 168 at first read, 169 at later read) now says both former flags were removed, unknown args are argparse rc2, `--selftest` refuses `--output`/`--pin-fixtures`, and the r14 flag belongs to the other tool. r16 gate/context/probe rows added with full fields. `build/SkillInterface.md:88` untouched. Lesson C15-4/M4 first said OPEN, then a later revision recorded "Corrected in working tree (`SKILL.md:168`); commit pending with `mori`"; ClaimRubric §6 and HistoricalCorrections C1 remain earlier read-time snapshots. | **Content covered; status text mostly reconciled** (F3). The "next lane-authored commit" is L1's, since no seat commits. |
| 5 | Carry the old drift-pin debt (`:288–293`): keep the red r10 observation until a separately reasoned semantic review; a green C1 fixture gate is not a freshness pass; keep victim/auth/access/retention/F01-F02/fixture-live qualifications | No re-pin; preserve red; carry qualifications | `MoriR16.DriftDebt` (report; absent at read time); `MoriR16.AttackPreservation` (report landed, assigned to attack this conflation); `MoriR16.Quality` → Q41; `MoriR16.Lesson` → C15-5; `MoriR16.FrontierIndex`, `MoriR16.Province`, L1 → `corpus/README.md`, `PROVINCE.md`, `SCORECARD.md`, `LOG.md` | C15-5 landed as carried debt, not a mistake; no re-pin proposed. SCORECARD round-16 row preserves the pin; PROVINCE FR11 narrowed but retains rotation/vacuum/cross-boot as Frontier; ReviewNoHarm verified the baseline byte-identical to HEAD and no spec owner writes it; LOG says old red unchanged; r15 `drift-current.json` remains exit1. QUALITY Q41 first cited a nonexistent `#M5`, then the later revision repointed it to `#C15-5` with "no M5 is asserted". | **Carried.** Remaining textual gap: the F01/F02 qualification has no r16 owner text (F4). |

### Binding carries outside the numbered list

| Verifier statement | Owner(s) | Observed |
|---|---|---|
| No live positive load, universal coverage, authenticated emitter, unique-victim count or performance improvement admitted (`:166–170`, `:295`) | `MoriR16.ClaimRubric`, `MoriR16.AttackClaims`, `MoriR16.Province`, `MoriR16.FrontierIndex`, `MoriR16.Knowledge`, `MoriR16.WindowTool` contract | ClaimRubric §6 lists every residual and pre-awards nothing; Province/README narrow FR11; Knowledge keeps subsets/access limits; WindowTool contract says unavailable on any failure. Covered. |
| Zero records is a window count, not absence; malformed/MESSAGE salvage rejected; foreign boot/array identities not positive | `MoriR16.Lesson` Gate, `MoriR16.Knowledge`, `MoriR16.ClaimRubric`, pack seats | Lesson Gate rejects all four classes; Knowledge says empty = unavailable/ambiguous; ClaimRubric R17/R25/R28. Covered. |
| Promotion operator-owned; active registry contradiction resolved before blanket executable-instructions assertion; no SHENON box or rank change (`:295–299`) | No writer assigned; correctly outside the draft | `git status` shows no `SHENON.md` write; no seat owns it. Correctly unowned/no action. |
| Historical artifacts preserved (`build/SkillInterface.md:88`, r15 lessons, fleet report) | No writer assigned; write-scope design | No r16 item owns those paths; `git status` shows no modification to `.ufo/waves/round-15/**` or the fleet report. Correctly unowned. |
| No new L0 question needed (`:299–302`) | L1 | No seat opens one. No action. |

## Flags — omissions and defects (reported, not edited)

**F1 — (resolved at later read) QUALITY Q41 pointer.**
First read: `corpus/QUALITY.md:104` cited `lessons/round-16.md#M5`, which the
lesson did not define; Quality's own report flagged the numbering risk. Later
read: Q41 cites `lessons/round-16.md#C15-5` and states "debt, not a mistake;
no M5 is asserted"; the lesson mapping line reads "Q41→C15-5 as debt". No
remaining defect. L1 should cite the final revision, not the first-read text.

**F2 — (resolved at later read) QUALITY Q38 attribution.**
First read: Q38 said "round 16 omitted a `/tmp` expected-probe write", which
misattributes the r15 `HarnessBuild.md:256` write; HistoricalCorrections C3
independently flagged it. Later read: Q38 cites `#M2 (= C15-2; precedent
`lessons/round-15.md:23`)` with no round-16 attribution. No remaining defect.

**F3 — Low, mostly reconciled: status and numeric pointers moved during the wave.**
First read: Lesson C15-4/M4, ClaimRubric §6 and HistoricalCorrections C1 said
OPEN/"still present"; Q40 cited `SKILL.md:125-134` and row `:134`. Later read:
Lesson M4/C15-4 record the working-tree correction and pending commit; Q40 was
rewritten to avoid the fixed range. Residual: the r15 row moved from line 168
to 169 between reads, so numeric anchors in seat reports are approximate; L1
should cite the row name (`r15 regressions`) and the final commit.
ClaimRubric §6 and HistoricalCorrections C1 remain read-time snapshots, not
live contradictions.

**F4 — Low: the F01/F02 causal-scope qualification of item 5 has no r16 text.**
The verifier requires keeping "victim/authentication, access/retention,
F01/F02 causal-scope and fixture/live qualifications" (`:292–293`). Victim,
auth, access/retention and fixture/live are carried (Knowledge, ClaimRubric,
Lesson Gate, Province). `grep -rn 'F01\|F02'` over
`corpus/lessons/round-16.md`, `corpus/knowledge/journal-cursor-window-r16.md`
and `.ufo/waves/round-16/` returns **zero hits**. No r16 claim touches F01/F02,
so the risk is latent, not an overclaim; but the carry is textually unowned.
Owner candidates: Lesson C15-5 row or ClaimRubric residuals. Do not add a new
criterion without L1 direction.

**F5 — Medium, procedural recurrence (new instance, not one of the five).**
`build/BootContinuity.md` (connector) discloses live `journalctl` probes and
writes to `/tmp/.probe_null` and `/tmp/.x`, and says a background probe job was
still running when L1 stopped runs; it labels the results inadmissible and
removed the files. This is the item-2/item-3 violation class recurring in
round 16. L1's wrap-up IRC says such results are inadmissible and must be
disclosed/sent to Lesson. My map therefore does not claim round 16 is
violation-free, and no routed item above relies on that seat's probe output.
The Lesson's later revision already references M7–M9, M13–M14 and M21 and says
the r16 instruction repair was itself violated in round 16, so the recurrence
is recorded at lesson level; L1 must confirm seat-level attribution and
admissibility. Not edited here.

**F6 — Info: verifier pointer precision.**
Item 3's "historical report:301–307" resolves to
`.ufo/waves/round-15/build/HarnessBuild.md:301–307`, not the 149-line fleet
report. Lesson C15-3 records this. Keep the corrected pointer in any future
citation; do not "fix" the verifier text (it is historical).

**F7 — Info: the r16 context contains `agent://all` as prohibition text.**
The verifier's method was a zero-token count. In r16 the token is present
because the prohibition names it (`wave1-spec.json` and `wave1-dispatch.json`:
2× `agent://all`, 1× `agent://MoriR16`). `ContextGuard`/Quality must test
prohibition semantics, not token absence, or the gate will misclassify a
correct context as a violation.

**F8 — Info: Registry report vs its own file.**
`build/Registry.md` §3 calls S039 the `sd_journal_test_cursor` row; the landed
`corpus/SOURCES.md` has **S039 = `sd_journal_seek_cursor`** (`:45`) and
**S040 = `sd_journal_test_cursor`** (`:46`). Knowledge and README already cite
S039/S040 in the file's sense; the Lesson initially flagged the conflict and
Registry's later update resolved it. L1 should verify S039/S040 and the four
`used-by` cells from the file, not from the Registry report prose. The newly
logged S014/S015 anchor-line discrepancy is a separate, correctly append-only
residual (`Registry.md` §5; ReviewNoHarm F5).

## Owner roster (active artifact owners)

| Owner id | Artifact | Routed items |
|---|---|---|
| `MoriR16.Lesson` | `corpus/lessons/round-16.md` | 1–5 (M1–M4, C15-5) |
| `MoriR16.Quality` | `corpus/QUALITY.md` | 1–5 (Q37–Q41), cursor Q42 |
| `MoriR16.SkillRegistry` | `SKILL.md` | 4 |
| `MoriR16.ContextGuard` | `tools/mori-round16-context-check.py` | 1 |
| `MoriR16.Registry` | `corpus/SOURCES.md` | source-row integrity (F8) |
| `MoriR16.FrontierIndex` / `MoriR16.Province` | `corpus/README.md` / `PROVINCE.md` | 5 (FR11 boundary) |
| `MoriR16.DriftDebt` / `MoriR16.AttackPreservation` | reports | 5 |
| `MoriR16.ClaimRubric` / `MoriR16.AttackClaims` | reports | non-claims, F4 candidate |
| `MoriR16.BootContinuity` | report | F5 recurrence disclosure |
| L1 (`MoriR16`) | wave context, `LOG.md`, `SCORECARD.md`, commit | 1 forward fix, 3 admissibility, 4 commit, 5 preservation |

## Confidence and remaining unknowns

- **Observed (high confidence):** verifier text and line anchors; seat prompts
  and owner ids; landed file contents and diffs; `git status`; QUALITY Q41's
  first-read `#M5` and later repoint to `#C15-5`; SKILL r15 row correction
  (line 168 at first read, 169 at later read); S039/S040 rows; absence of
  F01/F02 text; BootContinuity's own disclosure.
- **Inference (medium):** severity labels; that L1 will verify the final
  uncommitted revision and cite row names rather than moving numeric anchors;
  that no r16 claim will revive F01/F02.
- **Unknown / not established:** whether `DriftDebt.md` and `AttackPreservation.md`
  contain the exact qualifications (DriftDebt absent at read time;
  AttackPreservation landed but was not read here — ownership is from the
  dispatched prompt, not its content); whether HistoricalCorrections' proposed
  append to `round-15.md` (draft A) is chosen over Lesson-only correction;
  whether L1 commits the final QUALITY/Lesson revision unchanged (the later read
  shows Q38/Q40/Q41 corrected); whether the context-check
  gate distinguishes prohibition text from authorization (F7).
- **Missing code at read time:** `tools/mori-journal-window.py` and
  `tools/mori-round16-regressions.py` were absent; `tools/mori-round16-context-check.py`
  appeared untracked. Nothing about their behavior is evaluated or predicted
  here. Per the operator wrap-up, wave 2 is skipped; L1 reviews and verifies
  delivered bytes.

No routed item is wholly unowned: items 1–4 have landed owners; item 5 is
carried by five artifacts. F1–F3 were corrected within the wave at later read;
the remaining textual gap is the F01/F02 sub-qualification (F4). L1 must verify
the final uncommitted LESSON/QUALITY/SKILL revision, because several numeric
pointers moved during the round.
