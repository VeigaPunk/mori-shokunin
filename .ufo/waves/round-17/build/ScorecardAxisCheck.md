# Scorecard axis check — round 17 wave 1

Seat: `MoriR17.ScorecardAxisCheck-5` (leaf, report-only)
Question: (1) current active scores; (2) whether non-author closures accepted the
reading "lowest owned non-retired axis" (coverage 6) while depth/freshness/calibration
sit at 5; (3) whether C1-on-coverage is compliant with `AXES.md`.
Method: read-only document and git-log inspection. No gate, selftest, census, oracle or
closure command was executed. No tool installed. No VCS mutation. Only this file written.

## Bottom line

1. **Active scores at the entering tip `24526ea`**: coverage **6**, operability **7**,
   depth **5**, freshness **5**, calibration **5**, adjacency **6**
   (`SCORECARD.md:977-984`; consistent with the r12 post-review corrections and r13–r16
   results).
2. **No non-author closure adjudicated the reading.** All four closures accepted the
   *scores* and per-axis verdicts (`round-14-verifier-spotcheck.md:87` holds the exact
   distribution), but the word "lowest" occurs **once** across the four files
   (`round-13-verifier-spotcheck.md:23`), and there it paraphrases the dispatched prompt as
   carrying a "lowest-owned-axis duty". The dispatched prompts themselves say
   **"lowest-scoring non-retired axis"** (`/home/vgpnk/Projects/shokunin/.ufo/prompts/mori-round-13.md:15`
   through `mori-round-17.md:15`). So the outside record contains no affirmative acceptance
   of the "owned" qualifier; it contains one reviewer paraphrase that imported it.
3. **C1-on-coverage is not compliant with `AXES.md` as literally worded.** The obligation
   is "the lane's **lowest-scoring non-retired axis**" (`AXES.md:33`; `PROTOCOL.md:97`,
   `:509`; dispatched prompt `:15`). Mori scores all six axes and retires none
   (`SCORECARD.md:3-4`, `:28-30`), so the lowest-scoring non-retired axes are
   depth/freshness/calibration at **5**, below coverage at **6**. The no-waiver claim is
   correct but does not help: the stagnation nudge's own precondition is false
   (`SCORECARD.md:635-637`: saturation line 8/10 on owned axes, held 6 and 7).
   A defensible *owned-subset* counter-reading exists (`AXES.md:4`, `PROTOCOL.md:436`,
   `SCORECARD.md:3-4`), and under it C1 passes; but that qualifier is not in the obligation
   text and is unratified. Strict-text answer: **no**; conditional answer: **yes only under
   the unadjudicated "owned" reading**.
   Under the strict reading **both** round-17 claims miss the obligation (C2 is on
   operability 7), so this is a round-level conformance gap, not a C1-only one.

## 1. Current active scores

`SCORECARD.md` carries a frozen round-1 table and later superseding sections. The top table
must not be used as active state.

Stale table (do not use): `SCORECARD.md:8-15` gives coverage 5 / operability 6 / depth 4 /
freshness 5 / calibration 5 / adjacency 6. It is explicitly superseded:

> `SCORECARD.md:616-617`: "Correction to the score table at the top of this file (frozen at
> round 1; 4 of 6 pointers stale — STATE dossier §2): the table is left as filed; this
> section's scores supersede it."

Active scores, last round recorded before round 17 (no round-17 section exists; `SCORECARD.md`
ends at round 16):

> `SCORECARD.md:977-984`:
> `| coverage | improved | 6 held | new exact-retained anchor-boot window capability; finite64/64 and live2/2 OK |`
> `| operability | unchanged | 7 held | new gate selftests pass after actual setup repairs; prior production bytes unchanged |`
> `| depth | unchanged | 5 held | S014/S015/S039/S040 support narrow mechanics, not a separate depth claim |`
> `| freshness | unchanged | 5 held | old r10 pin and census bytes preserved; prior recorded red remains debt, no re-pin |`
> `| calibration | unchanged | 5 held | capability absence versus defect red and fixture/live scopes separated; procedural nonconformance disclosed |`
> `| adjacency | unchanged | 6 held | no census integration, orchestration or host remediation; unauthorized seat staging remains a violation, not expanded ownership |`

Supporting history for the same numbers:

- coverage 5→6 landed in r12 (`SCORECARD.md:611`); the r13 author's 6→7 was withdrawn after
  the rejected closure (`SCORECARD.md:735-739`, `round-13-verifier-spotcheck.md:7`), so 6.
- operability 6→7 was verified by the r13 closure (`round-13-verifier-spotcheck.md:96`:
  "C2's F01/F02 repairs independently verify") and held in r14–r16.
- depth 4→5 in r12 (`SCORECARD.md:609`), held since.
- freshness 5, pinned debt carried (`SCORECARD.md:983`).
- calibration held at 5 by the r12 post-review correction
  (`SCORECARD.md:654`: "scalar score **held at 5**, not 6, because the non-author reviewer
  could not re-derive 6").
- adjacency 6 held (`SCORECARD.md:655`, `:984`; `## Retired`, `SCORECARD.md:28-30`: "None.").

Round-17 contract's own statement agrees on the two owned values:

> `.ufo/waves/round-17/contract.md:9`: "**C1 coverage (capability acquisition, lowest owned
> axis 6)**"
> `.ufo/waves/round-17/contract.md:16`: "**C2 operability (7)**"

## 2. What the non-author closures actually accepted

Measured counts (read-only, `grep -c -i 'lowest'`):

| Closure file | occurrences of "lowest" | disposition |
|---|---|---|
| `corpus/lessons/round-13-verifier-spotcheck.md` | 1 | rejected-harmed; the one occurrence describes the dispatched prompt |
| `corpus/lessons/round-14-verifier-spotcheck.md` | 0 | admitted true |
| `corpus/lessons/round-15-verifier-spotcheck.md` | 0 | admitted true |
| `corpus/lessons/round-16-verifier-spotcheck.md` | 0 | admitted true |

**Round 13 closure** — `round-13-verifier-spotcheck.md:23`:

> "Dispatched `.ufo/prompts/mori-round-13.md` carries mission/axes binding, 1–3
> distinct/separable claims, **lowest-owned-axis duty**, frontier/source contract, ..."

This is a paraphrase, not the prompt's text. The prompt at
`/home/vgpnk/Projects/shokunin/.ufo/prompts/mori-round-13.md:15-16` says "the
**lowest-scoring non-retired axis**". The same wording is in the r14, r15, r16 and r17
prompts (`:15` in each; verified by `grep -n 'lowest-scoring'`). The closure also records
"Both owned axes entered at 6" (`:24`) but never tests the clause against the three 5-scored
axes, which already existed then (r12 corrections, `SCORECARD.md:653-655`).

**Round 14 closure** — accepted the exact score distribution while verifying the claim:

> `round-14-verifier-spotcheck.md:87`: "`git diff B H -- SCORECARD.md` showed **82 additions,
> zero deletions**: an appended correction withdraws unsupported prior coverage credit,
> preserves the verified operability gain and holds
> **coverage6/operability7/depth5/freshness5/calibration5/adjacency6**."

Its per-axis table (`:91-96`) marks coverage improved, operability unchanged,
depth/freshness/calibration unchanged. No sentence addresses why coverage (6) was the
selected axis while three non-retired axes sat at 5.

**Round 15 closure** — `round-15-verifier-spotcheck.md:177`:

> `| coverage | improved | C1 finite mixed-invalid alarm failures34→0, raw-total
> unavailability preserved; **owned score6 held** |`

This is the only closure that uses the lane's "owned" vocabulary for the score, but it
still does not state or test a lowest-axis rule. Remaining rows (`:178-182`) are
unchanged/unchanged/unchanged.

**Round 16 closure** — `round-16-verifier-spotcheck.md:12` and `:128-129`:

> "No owned axis is harmed."
> `| coverage | improved | ... Score 6 held. |`
> `| operability | unchanged | ... Score 7 held. |`

Depth/freshness/calibration are recorded "unchanged" (`:130-132`) without any lowest-axis
adjudication.

**Finding (observed):** the non-author closures accepted the numbers and the no-harm
verdicts, and therefore did not object to the selection, but **none of them accepted the
reading explicitly or re-derived it from `AXES.md`**. The only apparent outside endorsement
is the r13 reviewer's "lowest-owned-axis duty" paraphrase, which does not match the prompt
text it purports to describe. Silent inheritance is not adjudication.

## 3. Where the "lowest owned non-retired axis" reading comes from

It is lane-authored and repeated:

> `SCORECARD.md:3-4`: "Axes owned by this lane: **coverage + operability** (fleet-2); all six
> are scored here, the owned pair drives the round's axis-move."
>
> `SCORECARD.md:661-662` (r13): "Both owned axes entered at 6; the lowest-owned-axis
> obligation is met."
>
> `SCORECARD.md:750-751` (r14): "This works the lowest owned non-retired axis, coverage
> (6 versus operability 7)."
>
> `SCORECARD.md:818-819` (r15): "Active owned axes remain coverage **6**, operability **7**;
> the former is the lowest owned non-retired axis. Other scores remain
> depth/freshness/calibration **5/5/5**, adjacency **6**. No stagnation waiver is used."
>
> `SCORECARD.md:913` (r16): "Coverage **6** is the lowest owned non-retired axis versus
> operability **7**; no stagnation waiver or score increase is claimed."

Round 12 was the last round where the literal lowest was worked: depth 4→5
(`SCORECARD.md:609`), with coverage also at 5. The divergence begins at r13, when the lane
first used "both owned axes entered at 6" as the lowest-axis argument while
depth/freshness/calibration were already 5.

## 4. Compliance with AXES.md

### 4.1 The rule as written

> `AXES.md:33-34`: "At least one claim works the lane's **lowest-scoring non-retired axis**,
> except when the stagnation nudge (below) waives it."
>
> `PROTOCOL.md:97`: "... at least one on the lane's **lowest non-retired axis** ..."
>
> `PROTOCOL.md:507-509`: "each lane owns a named subset and works 1–3 declared claims per
> round (... at least one on the lane's **lowest non-retired axis** ...)"
>
> `/home/vgpnk/Projects/shokunin/templates/round-prompt.md:15-16` and
> `/home/vgpnk/Projects/shokunin/.ufo/prompts/mori-round-17.md:15-16`: "At least one claim
> works the **lowest-scoring non-retired axis** — unless the stagnation nudge waives it."

The r17 prompt also states the precedence:

> `.ufo/prompts/mori-round-17.md:6-7`: "Where this prompt conflicts with MISSION.md + AXES.md,
> the mission files win."

No fleet gate enforces the clause: recursive `grep -rn -i 'lowest|non-retired' scripts
.ufo/gates` returns only `scripts/hyaku/inline.sh:9` ("lowest next round first" — round
ordering, not axis work), so the check is documentary.

### 4.2 Mori's scored, non-retired set

- All six axes are scored in this lane's SCORECARD (`SCORECARD.md:3-4`, `:8-15`,
  `:977-984`).
- No axis is retired (`SCORECARD.md:28-30`: "None").
- Saturation line is 8/10 on the owned axes (`SCORECARD.md:635-637`).
- Stagnation waiver precondition ("every axis the lane owns sits at or above the lane's
  saturation line", `AXES.md:68`) is false: owned axes are 6 and 7, below 8. The r15/r16
  sections also say the waiver is not used (`SCORECARD.md:820`, `:914`), and the round-17
  contract claims none.

Therefore the lowest-scoring non-retired axes are **depth, freshness and calibration at 5**
(a three-way tie). Coverage 6 and operability 7 are above them.

### 4.3 Application to C1 (and C2)

- C1 names **coverage 6**, not a 5-scored axis. Under the plain wording it does not satisfy
  "lowest-scoring non-retired axis".
- C2 names **operability 7**, also not a 5-scored axis. If the plain wording governs, the
  round has **zero** qualifying claims, not merely a misplaced C1.
- Capability-acquisition type does not exempt the clause: "A claim may instead be a
  **capability acquisition** ...; it still lands a per-axis verdict" (`AXES.md:40-41`).
- Other `AXES.md` claim constraints are met: two claims, distinct axes, declared causally
  separable (`contract.md:22`), within the 1–3 cap (`AXES.md:27`).

### 4.4 The counter-reading and why it is unresolved

Textual footholds for "owned subset":

- `AXES.md:4`: "Every shokunin works its own subset; the protocol and aggregator lanes own
  the fleet-level axes."
- `PROTOCOL.md:436`: "`SCORECARD.md` | Axis scores per `AXES.md`: **owned axes** → score
  0–10 → evidence pointer → last-change round ..."
- `PROTOCOL.md:507`: "each lane owns a named subset".
- The lane's own gloss at `SCORECARD.md:3-4`.

Against them:

- The obligation clause itself carries no ownership qualifier in any of its four homes
  (`AXES.md:33`, `PROTOCOL.md:97`, `PROTOCOL.md:509`, the dispatched prompt `:15`).
- Ownership is scoped explicitly only in the waiver (`AXES.md:68`), which suggests the
  drafters knew how to write the qualifier when they meant it.
- The lane scores all six, so its own scorecard supplies six "scoring" axes; the
  "observed" category it uses for the other four is a lane convention not defined in
  `AXES.md` (which knows only owned and retired, `AXES.md:36-38`).
- The lane itself has worked non-owned axes recently: depth 4→5 in r12
  (`SCORECARD.md:609`), freshness in r10, calibration in r11. The subset sentence is
  therefore not a practical bar to a 5-axis claim.
- Fleet practice is split, so there is no settled convention to import:
  - unqualified use over all scored axes: `.ufo/reports/round-16/tabi.md:10` ("operability 8
    (the lowest non-retired tie with depth/freshness/adjacency)");
  - owned use: `.ufo/reports/round-14/kengaku.md:9` ("lowest owned axis");
    `.ufo/reports/round-16/tameshi.md:7` ("tied-lowest owned axes").
- The closest thing to a fleet ruling is an unanswered operator question on the same
  ambiguity: `.ufo/l0-questions.md:11` (kotoba, round 13) asks the operator to "Ratify that
  a lane may work an advisory axis as its lowest-axis move, or say which owned axis should
  absorb it." No answer is recorded in that append-only file.
- `AXES.md:22-23` offers a third selector ("Pick the round's axis from the trend furthest
  behind"), which the round-17 contract does not cite either; no `LEARNING.md` trend state
  is referenced.

### 4.5 Verdict

**Advisory verdict: C1-on-coverage is not compliant with `AXES.md` as written; it is
conditionally compliant only under the lane's imported "owned subset" reading, which no
non-author closure has ratified.** Confidence: high on the document text; medium on fleet
intent, because the preamble and the SCORECARD field do support the subset reading and the
fleet uses both.

The contract phrase "lowest owned axis 6" is a rewrite of the rule, not a quotation of it.
If the strict reading is applied by the round-17 closure, the likely routing is a
status-neutral conformance defect on the round (neither claim on a 5 axis), not a claim
failure; that is how the r13/r15/r16 closures treated comparable procedural defects
(`round-13-verifier-spotcheck.md:25`, `round-15-verifier-spotcheck.md:249`,
`round-16-verifier-spotcheck.md:11-16`).

## 5. Options for L1 (advisory only, no judgment)

1. **Cheapest evidence-preserving path:** leave C1/C2 as claims and record the reading
   explicitly in the round-17 report, quoting `SCORECARD.md:3-4` plus `AXES.md:4` and
   `PROTOCOL.md:436`, and name the conflict with `AXES.md:33`/the dispatched prompt. This
   turns an unstated gloss into a disclosed one; it does not make it compliant.
2. **Third claim on a 5-scored axis:** `AXES.md:27` allows up to three claims; a bounded
   third claim on depth, freshness or calibration would satisfy the strict reading. This is
   a contract change mid-wave and would need its own falsifiable before→after.
3. **Operator ratification:** append an L0 question (lane-owned append-only file) mirroring
   kotoba's `.ufo/l0-questions.md:11`, asking whether the lowest-axis obligation ranges over
   the owned subset or all scored non-retired axes. This resolves it fleet-wide instead of
   per round.
4. **Do nothing:** a closure critic applying `AXES.md:33` literally will likely route it.
   Per the r13–r16 pattern that is status-neutral, but it costs a correction cycle.

## 6. Observed, inferred, unresolved

**Observed**
- Active scores as in §1, from committed `SCORECARD.md` at `24526ea`.
- Closure "lowest" counts: r13=1, r14=0, r15=0, r16=0.
- All dispatched r13–r17 prompts carry "lowest-scoring", not "lowest owned".
- No stagnation waiver is claimed, and its precondition is false at the declared
  saturation line.
- `## Retired` is "None".
- No fleet gate enforces the clause.

**Inference [INFERENCE]**
- The r13 closure's "lowest-owned-axis duty" is a reviewer paraphrase that imported the
  lane's qualifier; the prompt it cites does not contain that word.
- The fleet has no single settled reading; the split is visible in sibling reports and in
  the unanswered kotoba L0 question.

**Unresolved**
- Whether the operator/protocol lane intends the obligation to range over the owned subset
  or all scored non-retired axes (no ruling located in `AXES.md`, `PROTOCOL.md`,
  `PROTOCOL-APPENDIX.md`, `.ufo/l0-questions.md`, or the four closures).
- Whether L1 will add a third claim or record the reading; this seat does not decide.
- Whether the round-17 closure will treat the gap as status-neutral conformance debt or as
  an admission blocker; precedent favors status-neutral, but that is a closure call.

## 7. Evidence trail

Files read (absolute paths):

- `/home/vgpnk/Projects/shokunin/AXES.md` (esp. `:3-5`, `:18-23`, `:27-38`, `:40-41`,
  `:66-73`)
- `/home/vgpnk/Projects/shokunin/PROTOCOL.md` (`:97`, `:436`, `:505-510`)
- `/home/vgpnk/Projects/shokunin/PROTOCOL-APPENDIX.md:49` (multi-claim row)
- `/home/vgpnk/Projects/shokunin/templates/round-prompt.md:13-17`
- `/home/vgpnk/Projects/shokunin/.ufo/prompts/mori-round-13.md:15`, `-14.md:15`, `-15.md:15`,
  `-16.md:15`, `-17.md:6-7,15-16`
- `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md:11`
- `/home/vgpnk/Projects/shokunin/.ufo/reports/round-14/kengaku.md:9`
- `/home/vgpnk/Projects/shokunin/.ufo/reports/round-16/tabi.md:10`
- `/home/vgpnk/Projects/shokunin/.ufo/reports/round-16/tameshi.md:7`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/SCORECARD.md` (`:3-4`, `:8-15`, `:28-30`,
  `:609-611`, `:616-618`, `:635-637`, `:653-655`, `:661-662`, `:750-751`, `:818-820`,
  `:913-914`, `:977-984`)
- `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-13-verifier-spotcheck.md`
  (`:7`, `:23-24`, `:95-100`)
- `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-14-verifier-spotcheck.md`
  (`:87`, `:91-96`)
- `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-15-verifier-spotcheck.md`
  (`:170-182`, `:249`)
- `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-16-verifier-spotcheck.md`
  (`:11-16`, `:121-133`)
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/contract.md:9-22`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/wave1-context.txt`

Commands (all read-only; run from the stated roots):

```sh
# lane tip
git -C /home/vgpnk/Projects/shokunin/mori-shokunin log -1 --format='%H %cs'
# 24526ea9617cd020fee16c28fe4d4a2789dc28cb 2026-10-20   rc=0

# closure "lowest" counts
for f in corpus/lessons/round-1[3-6]-verifier-spotcheck.md; do
  n=$(grep -c -i 'lowest' "$f"); echo "$f lowest=$n"; done
# round-13=1; round-14=0; round-15=0; round-16=0   rc=0

# obligation wording
grep -c 'lowest-scoring' AXES.md                    # 1   rc=0
grep -c 'lowest non-retired axis' PROTOCOL.md       # 2   rc=0
grep -c 'lowest-scoring' templates/round-prompt.md  # 1   rc=0
grep -n 'lowest-scoring' .ufo/prompts/mori-round-1[3-7].md
# all five prompts: line 15   rc=0

# gate enforcement survey
grep -rn -i -E 'lowest|non-retired' scripts .ufo/gates
# only scripts/hyaku/inline.sh:9 (round ordering), no axis gate   rc=0
```

No `/tmp` writes, no background jobs, no live journal query, no pacman transaction, no
credential or transcript read. No tools installed or updated.
