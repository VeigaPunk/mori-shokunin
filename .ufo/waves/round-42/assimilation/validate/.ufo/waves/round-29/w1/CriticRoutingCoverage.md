author: MoriR29.CriticRoutingCoverage (wave-1 critic; leaf; read-only)

# Round 29 — routing coverage of the claim contract

Contract: `.ufo/waves/round-29/contract.md` at `8a45cefe` (lane HEAD, `git rev-parse HEAD` → `8a45cefe84af0557b457308e4e0f679ca490f9e9`).
Sources mapped: `corpus/lessons/round-28-verifier-spotcheck.md` (§1-§2 caveats, §4, §6 items 1-6) and
`corpus/lessons/round-28.md` (`## Mistakes`, seat notes, wave-2 corrections). Addendum rules:
fleet `.ufo/prompts/mori-round-29.md:343-351`. Also read (allowed, not reports): `wave1-spec.json` item prompts,
rule text `.ufo/waves/round-27/contract.md:47-58`, `.ufo/waves/round-26/contract.md:152-190`, the round-28 C2
counter `.ufo/waves/round-28/count-c2.sh` (grep only), SCORECARD at `7118f320`, fleet MANIFEST at `63729047`.
Not opened: the oom-killers tool, any round-26/27/28 w1 or w2 report. Tools installed: none. No URL fetched.

## Ranked findings (counterexample, evidence, axes, smallest correction)

### F1 (high, C1) — a legacy score claim the closure record contradicts passes every mismatch kind

- Counterexample: the operability row reads `round 14 (6 → 7)` (`git show 7118f320:SCORECARD.md`, line 11). The
  round-14 closure says operability did not move: `round-14-verifier-spotcheck.md:92` "| operability | unchanged |",
  and MANIFEST round 14 `verdicts.operability` = `unchanged` (`git show 63729047:MANIFEST.json | jq` → r14
  `{"coverage":"improved","operability":"unchanged",…,"adjacency":"improved"}`).
- Kind 2 (`contract.md:32-33`) checks only that round 14 is admitted (it is); kind 4 (`:36-37`) fires only when the
  score differs from `7118f320`. So the fix can add the round-28 pointer, keep `round 14 (6 → 7)`, and print
  `mismatches=0`: the calibration claim would certify a row that disagrees with the record it claims to match.
- Axes: calibration (the claimed axis). Other rows are clean on this test: coverage `round 12 (5 → 6)` and depth
  `round 12 (4 → 5)` match MANIFEST r12 `improved`; the rest cite round 1 (N < 12, exempt).
- Smallest correction (contract amendment before the counter lands):

```text
2b. Unsupported last change. When the row's Last change cell states a score move `A → B` for round N ≥ 12, the
    pinned MANIFEST entry for mori round N must hold `verdicts.<axis>` = `improved`.
```

### F2 (high, C1) — the score policy is a second authority the counter never reads

- Counterexample: set freshness to 9, Last change `round 28 (5 → 9)`, cite `round-28-verifier-spotcheck.md`.
  Kind 1 is met (R = 28), kind 2 is met (r28 admitted), kind 3 is met, kind 4 is met (an admitted `improved` closure
  is cited). `mismatches=0`, `C1=met`. The score policy (`contract.md:47-49`) forbids it, but it is declared
  "binding on the fix, not on the counter", so nothing countable fails. Inflating a score is exactly the defect a
  calibration claim exists to catch.
- Evidence of a countable basis: round 28's measured outcome states the number,
  `SCORECARD.md:1771` "… freshness 5 → 6 proposed" (`git show 7118f320:SCORECARD.md | grep -n`).
- Smallest correction:

```text
4b. Score beyond basis. If the row's score is above its 7118f320 value, it must be exactly one higher, and the
    cited admitted round's SCORECARD declaration or measured-outcome row at <rev> must contain
    `<axis> <old> → <new>` (or the cited spot-check per-axis line must state `<old> → <new>`).
```

### F3 (medium-high, C1) — kind 1 cannot see admitted closures that have no lane spot-check file

- MANIFEST at `63729047` carries per-axis `verdicts` for every round; rounds 19, 21 and 22 are admitted with
  improved axes but have no `round-N-verifier-spotcheck.md` (`ls corpus/lessons/` → only `round-19.md`,
  `round-21.md`, `round-22.md`). Latest admitted `improved` round per axis, MANIFEST vs kind-1 rule (command: jq
  over MANIFEST `verdicts`; loop over spot-check files at `7118f320`):

| axis | MANIFEST latest | kind-1 R | effect |
|---|---|---|---|
| adjacency | 19 | 18 | the counter demands a pointer one closure stale |
| depth | 12 | none | r12 spot-check is prose, not a table; no requirement (harmless today) |
| coverage, operability, freshness, calibration | 26, 28, 28, 25 | same | agree |

- Axes: calibration. Smallest correction: take R from the pinned MANIFEST `verdicts.<axis>`; accept as the pointer
  `round-R-verifier-spotcheck.md` when it exists at `<rev>`, else the fleet report path `.ufo/reports/round-R/mori.md`.

### F4 (high, C2; addendum rule 9) — the C2 statement carries clauses its counter cannot count

- `contract.md:55-57`: "eight blind seats (four per rule) … that read no tool source, no tool output, no critic or
  design report and no lesson; it is committed before the L1 runs the tool on it".
- The counter as briefed (`wave1-spec.json`, item BuildCountC2) counts ≥ 3 distinct authors per rule, the single add
  commit, blob unchanged since, and self-test tallies. It counts nothing about what a seat read, and nothing about
  when the tool was first run. The "read no …" clause is a universal clause over an unenumerated set of reads:
  the addendum says "Use no universal clauses … unless the counting command enumerates the full set"
  (`mori-round-29.md:346-347`).
- "Eight seats (four per rule)" can fail while the counter prints `C2=met` (one dead writer leaves 3 authors).
  That is the round-28 M3 class as corrected by wave 2: a single point of failure in a declared claim
  (`round-28.md:140-141`). This contract's "a miss is reported as a miss" (`contract.md:4-5`) then makes it a miss.
- Smallest correction:

```text
Statement: at the landed tip the C2 counter prints `C2=met`, exit 0 (at least 12 cases, at least 6 per rule, at
least 3 distinct `author` values per rule, … unchanged).
Process conditions (disclosed, not counted): case writers are blind (read list in each writer report; check
.ufo/waves/round-29/check-blind-wave.sh <freeze> .ufo/waves/round-29/w1 '^CaseA2' receipt committed); the first tool
run on the new file comes after the freeze commit (evidence/c2-freeze-selftest.txt names the freeze hash).
```

### F5 (high, C2 vs routed defect 2) — the counter can be met without any case of either breach shape

- `contract.md:13-14` presents C2 as routed defect 2 ("two breach shapes … have no frozen case";
  spot-check `:126-127`). The shapes are steered only by the wave-1 spec's "Input dimension" sentences
  (CaseA207a/b: version lines of several invocations around a bounded scope; CaseA210a/c: stamp-less records with an
  unbounded scope or a non-active unit). No counted clause requires one case of either shape.
- Counterexample: CaseA207a and CaseA207b both place every version line before the scope bound (their brief allows
  "before it"). The other 18 cases are still counted: 6+ per rule, 3+ authors, required fields pinned, `PASS N/N`.
  `C2=met` while the in-scope split shape, the one the routed defect names, stays unpinned.
- Smallest correction (one line per rule in the counter, rule-text terms only, no tool knowledge):

```text
shape_a207=<n>: A2-07 cases whose earlyoom_show has a non-zero ActiveEnterTimestampMonotonic and whose journal has
  at least two version-line records with __MONOTONIC_TIMESTAMP at or above it, one of them followed by
  `dryrun mode enabled`.
shape_a210=<n>: A2-10 cases with a journal record lacking a numeric __MONOTONIC_TIMESTAMP while
  ActiveEnterTimestampMonotonic is missing or 0, or the earlyoom state is not active.
Both ≥ 2, each from ≥ 2 distinct authors, else C2=unmet.
```

### F6 (medium, hygiene 2 / M6) — the blindness line is false as written, and its check has a cross-round blind spot

- `contract.md:93` "wave 1 has no seat that reads or runs the tool": BuildCountC2 is briefed to run the tool's
  `--selftest` on the two older case files, and the wave context grants that exception. So the sentence is false.
- `:93-94` names no check. The wave item BuildBlindCheck supplies `check-blind-wave.sh`. It can fail on the round-28
  freeze state: CriticC2Design.md and ReviewA2SpecVsTool.md were added in `1c4c186` (15:34:21-03:00), before the
  freeze `d21b8bd` (15:50:55-03:00) (`git log --diff-filter=A`; `git ls-tree d21b8bd3 … | grep -c` → 2).
- Blind spot: check (a) scans only the named wave directory, and check (b) is a self-reported read list. The same two
  round-28 reports are still committed (`git ls-tree 7118f320 .ufo/waves/round-28/w1/`) and readable by round-29
  writers. A writer that opens one and leaves it off its list passes both checks.
- Smallest correction: reword `:93` to "no wave-1 seat reads the tool; BuildCountC2 runs `--selftest` on the two
  older files and quotes marker lines only". Name the check in the contract. Add `.ufo/waves/round-2[0-9]/` to check
  (b)'s forbidden paths, and disclose (b) as self-attested, so M6 is shown able to fail only for the same-directory
  shape.

### F7 (medium, C2 sourcing) — false provenance in the sourced-claim line

- `contract.md:18-20` "The case writers and the fix rest on SOURCES rows opened this round (S153 onward)". The writer
  briefs forbid opening the contract and any lesson. They fetch earlyoom v1.9.0 and journal docs themselves by curl
  (CaseA207a/CaseA210a prompts). The Source* seats (SourceEarlyoomDryrun, SourceJournalMonotonic,
  SourceJournalExport) run in the same wave, so no S153+ row exists when the writers write.
- The `sources` top-level key is not counted. The round-28 counter's parse rejects only a non-object top level and a
  non-list `cases` (`round-28/count-c2.sh:291,295`). The older files' top level is `cases, frozen_with, note,
  schema` (`jq keys`). [INFERENCE] Whether the tool's self-test accepts an extra top-level key cannot be checked
  under blindness.
- Smallest correction: "The Source* seats open S153+ rows for the URLs the writers fetched. Where a writer reports a
  digest, the Gate sha256 must equal it. The `sources` key is added by the L1 at assembly and is not counted."

### F8 (medium, hygiene 3) — "record reject decisions met" cannot fail as worded

- `contract.md:95` (spot-check §6.3, `:128`; §4 `:109-110`): nothing defines the set of decisions "met", so a Gate
  that lists no rejects passes. The DraftQualityCriteria brief asks how each criterion can fail, but the contract
  fixes no input.
- Smallest correction: "Every URL listed in a Source* seat's opened list appears in the round-29 Gate with
  `admit` or `reject`. A missing URL fails the check."

### F9 (medium, coverage) — carried items the contract drops by name

Hygiene 6 (`contract.md:99-100`) omits these items, which round 28 carried or routed into round 29:

- S143/S144 superseding-row debt (`round-28.md:51,142`).
- The M7 dangling-id check (`:147-149`).
- Round-27 wave-2 open findings, carried "as named debt for round 29": CriticC1Admission, ReopenS133–S137,
  ReviewEntryFact1, ReviewHygieneD2, ReviewHygieneR7, ScoutMisroot (`:122-124`).
- M2 hash-check weaknesses: a one-byte change defeats it, it credits its own receipt, and the clean-sweep run was
  not saved (`:137-139`). ScoutMisrootBaseline takes a baseline only.
- FixR5RoutedSelftest, not returned (`:158`).
- The "opened this round" dating part of the ReviewReaderSweep item (spot-check `:133`; ScoutCarriedDebt's brief
  has it, the contract does not).

Smallest correction: append those names to hygiene 6.

### F10 (low, hygiene 1) — routed defect 1 is only half carried

- Spot-check `:123-124` also says "act on any finding they carry against C1's counter or QUALITY 83–84". The
  contract's `:92` stops at "re-verified … committed as evidence or disposed".
- File state (`[ -e ]` and `git ls-tree 8a45cefe`): the three w2 files and `wave1-run.err` are present and
  untracked. `w1/FixR1Runway.md` (withheld at closure, spot-check `:26-27`) is now absent from the lane path, and the
  contract does not say where it went. No wave-1 seat covers `wave1-run.err`.
- Smallest correction: add "a reproduced finding becomes a fix or a named carry; dispositions name `wave1-run.err`
  and `w1/FixR1Runway.md`".

### F11 (low, C1 kind 2) — the prescribed held wording escapes kind 2

- Kind 2 applies only when the cell "opens with `round N`" (`:32`). The policy's own wording "improved (closure
  round N), score held" (`:49`) does not open that way, so kind 2 never examines such a cell.
- Correction: apply kind 2 to the first `round N` token anywhere in the cell.

### F12 (low, C1 kind 3) — a dead-pointer check by line count only

- A pointer to the wrong line of a long file passes. This is a tradeoff, not a defect; the wave item
  ReviewAxesPointers covers it by reading the lines. No contract change.

## Coverage map

| Item (source line) | Status | Contract line / note |
|---|---|---|
| §1 untracked: three late w2 outputs (spot `:28-31`) | covered | `:92`; seats ReviewLate* ×3 |
| §1 `wave1-run.err` (`:27`, routed `:123`) | partly | `:92` is generic; no seat (F10) |
| §1 `w1/FixR1Runway.md` withheld (`:26-27`) | missing | absent on disk now, no disposition (F10) |
| §1 `.scratch/` pre-round (`:25`) | n/a | not round work |
| §2 C2 caveat CaseA2r03 read (`:74-75`) | covered, weak | `:55-57`, `:93-94` (F4, F6) |
| §2 C2 verified as counter value only (`:73-74`) | covered | `:71-73` substantive before |
| §2 census nine vs ten W04 (`:80-83`) | covered | `:98` |
| §2 tip receipts at parent (`:58-59`) | covered | `:96-97` (no command named; BuildTipReceipts) |
| §4 Gate holds only admits (`:109-110`) | covered, cannot fail | `:95` (F8) |
| §6.1 late outputs + act on findings (`:123-124`) | partly | `:92` (F10) |
| §6.2 blindness + A2-07/A2-10 shapes (`:125-127`) | covered, uncounted | C2 `:51-80`, `:93-94` (F4, F5, F6) |
| §6.3 Gate rejects (`:128`) | covered, cannot fail | `:95` (F8) |
| §6.4 tip receipt header (`:129-130`) | covered | `:96-97` |
| §6.5 census line (`:131`) | covered | `:98` |
| §6.6 MutCountC1 F1/F2/F3/F6/F10, S146, used-by, r25 R1/R5 (`:132-133`) | carried by name | `:99-100` |
| §6.6 ReviewReaderSweep dating (`:133`) | missing | only "citations" named (F9) |
| M1 typed heading time (`round-28.md:24-30`) | n/a | closed in r28, QUALITY 83 shown able to fail |
| M2 misroot sweep + wave-2 weakness (`:31-41`, `:137-139`) | missing | wave seat ScoutMisrootBaseline only (F9) |
| M3 withdrawn claim / SPOF (`:42-46`, `:140-141`) | re-opened | `:4-5` repeats the sentence; `:55` "eight seats" (F4) |
| M4 S143/S144 (`:47-51`, `:142`) | missing | (F9) |
| M5 tip receipts (`:52-57`) | covered | `:96-97` |
| M6 blindness leak (`:143-146`) | covered | `:93-94`; check able to fail at `d21b8bd` (F6 limits) |
| M7 dangling-id check (`:147-149`) | missing | (F9) |
| Late seats: writers' upstream reads unrecorded (`:150-153`) | covered | `:18-20` (F7 provenance) |
| Withheld FixR1Runway; R1/R5 open (`:154-158`) | partly | R1/R5 `:99`; FixR5RoutedSelftest missing (F9) |
| Round-27 w2 reports' open findings (`:122-124`) | missing | (F9) |
| Freeze hash absent from LOG (`:128`) | superseded | counter derives the freeze by add commit (BuildCountC2 brief) |
| A2-07/A2-10 shapes stay open (`:19-21`, `:129-130`) | covered, uncounted | `:13-14` (F5) |
| jj author time ≠ write time (`:16-17`) | partly | `:45`, `:71` order by ancestry; `:57` run order uncountable (F4) |

## Fixes that cannot fail (as the contract words them)

- Score policy `:47-49`: declared not binding on the counter (F2).
- Hygiene 3 `:95`: no defined input (F8).
- C2 blindness and run-order clauses `:55-57`: no counter (F4).
- `:4-5` "never withdrawn": a sentence; round-28 wave-2 already ruled this form not a fix (`round-28.md:140-141`).
  It is not claimed as a fix here, so this item is informational.

## Addendum check (`mori-round-29.md:343-351`)

| Rule | Result | Evidence |
|---|---|---|
| One concrete after-value per claim, re-derivable by one command | C1 ok; C2 mixed | C1 `:24-25`, `:46-47`; C2 `:55-63` adds uncounted clauses (F4) |
| No universal clause unless enumerated | C1 ok; C2 fails | C1 `:27` enumerates six rows; kind 3 enumerates tokens. C2 "read no …" `:56-57` is not enumerated (F4). Hygiene 1 "each" over an unlisted set `:92` (uncounted, low) |
| Calibration counts self-assessment vs observed state | ok, with gaps | `:27-37` counts mismatches; F1-F3 are uncounted disagreement shapes |
| Prefer 2 claims | ok | two claims, `:8-20` |
| Size to one round | ok [INFERENCE] | 24 briefed cases against a floor of 12 leaves slack for dead writers |
