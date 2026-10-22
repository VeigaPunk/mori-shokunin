# CriticLessonMistakes — round 29 wave 2: attack on `corpus/lessons/round-29.md` `## Mistakes` (M1–M4)

Seat: MoriR29.CriticLessonMistakes (critic, leaf). Lane tip read: `8809a3fe1eaa87a0afa177a15263d174378e7462`.
Rules applied: `CORPUS.md:171-184` (row shape; classes from the kaika `mistakes.md` §5 vocabulary; captured-by is
"the `QUALITY.md` criterion or protocol rule that should have caught it, or `none`"; a fix is shown able to fail),
`LEARNING.md:19-21` (a mistake that no criterion caught gets a `QUALITY.md` criterion that cites the lesson).
Receipts I made are in `/fast/scratch/hyaku/mori-r29/w2/CriticLessonMistakes/` (scratch only, not committed).
Tooling: nothing installed or updated. Writes: this file and my scratch dir only. The sandbox clone sat under that
scratch dir; inside it I ran only `git clone` and `git checkout`. No oom-killers run of any kind.

## Verdict per row

| row | class right? | captured-by honest? | fix shown able to fail? |
|---|---|---|---|
| M1 | no (not a §5 token) | no: a protocol rule existed | yes, the receipt is real; cite the fix-parent run |
| M2 | no | no (names the detector) | honestly "not yet", but the fix is not written anywhere, and the evidence premise is false |
| M3 | no | no (names the detector); repeats round-28 M2 | false "no automated check": a lane tool catches it (receipt below) |
| M4 | no | no (names the detector); QUALITY 84 passed the defect | yes: `DraftQualityCriteria.md:26`, which I reproduced |

Four round-29 mistakes are missing (F1, F3, F7 and F8 below).

## Ranked findings

### F1 (critical, missing mistake): the A4 miss condition was given an escape after the data came in
- Counterexample: A4 R3 (`contract.md:177-178`) says the blind check run at the freeze commit "must print
  `blind_violations=0`; otherwise C2 is a miss, reported as one". It has no adjudication clause. `LOG.md:1928-1929`
  (commit `255b705`, which comes after the pre-freeze run) adds one: "a C2 miss condition unless wave-2 adjudication
  finds the instrument at fault". The QUALITY 85 note (`corpus/QUALITY.md:461-463`) routes the decision to that
  adjudication. M2 frames the instrument as the culprit, which sets up the same exit.
- Evidence: I ran the check at the binding revision, the freeze commit `d6d5cb0a`. It printed
  `blind_violations=20`, exit 1 (`scratch/blind-at-freeze.txt`). The only committed receipt was taken at `221cbd8f`.
  That counts the same `w1/` bytes, because the diff from `221cbd8f` to `d6d5cb0a` adds only the receipt and the
  case file.
- Axes: C2 (operability), calibration. This is the identity change the critic role watches for. The contract
  (`contract.md:4`): "A declared claim is never withdrawn; a miss is reported as a miss."
- Smallest correction (append): **M5 — a counted miss condition read with an escape after the data (class: `scope`).**
  Evidence: `contract.md:177-178` against `LOG.md:1928-1929`. Captured-by: `contract.md:4` and the amendment rule
  "before the data each governs" (`LOG.md:1911-1913`). Fix: report C2 as a miss under A4 at `d6d5cb0a`. M2 explains
  why the instrument false-fires. It does not lift the miss. Any relaxation would be a new amendment, and it would
  come after the data.

### F2 (high, M3): "no automated per-wave check" is false, and M3 repeats round-28 M2
- Counterexample: `tools/mori-wave-settlement.py` (round 20; `corpus/knowledge/wave-settlement-r20.md:32`) reports a
  member as `misrooted` when the lane has no report and the fleet root has the same relative path. I cloned the lane
  at `8809a3fe` into scratch (tool sha256 `79e7f9de…b28f9`) and made a stand-in fleet root.
  - Green: `wave1-run.json`, state `settled`, present 35, misrooted 0.
  - Red, with `CaseA207c.md` moved to the stand-in fleet root: state `partial`, misrooted 1,
    `('CaseA207c', 'misrooted')`.
  - Receipt: `scratch/settlement-misroot.txt`. The command was `python3 -I -B tools/mori-wave-settlement.py scan
    --lane-root <clone> --fleet-root <stand-in>`.
- Repeat: `round-28.md:31` M2 is "seat fetches misrooted at the fleet root … (class: write outside the lane)". It is
  the same label, and that row also gave a manual sweep as captured-by. Neither the settlement tool nor round 28's
  `misroot-hash-check.sh` is named in any round-29 file, lesson line or LOG line (`grep -rn
  'misroot-hash-check\|wave-settlement' .ufo/waves/round-29/ corpus/lessons/round-29.md LOG.md`). The only hits were
  older LOG lines, at 1188, 1376 and 1884. [INFERENCE] The hash check would miss this case anyway: a report file's
  own hash is not cited inside a report (`misroot-hash-check.sh:5-6`).
- Smallest correction (append to M3): class `attribution`; "repeats round-28 M2". Captured-by: QUALITY 43 and
  `tools/mori-wave-settlement.py scan --fleet-root` (the latter not run on wave 1). Fix: run the settlement scan per
  wave and commit its red/green receipt. The red is the shape above. Until that receipt is committed, write "not yet
  shown able to fail in the lane". Also give the full sha256
  `0fe85d0b2ce857cd954c6831ec907043590651ec47794760512f87f88a505a0a` (I computed it on the lane copy, committed at
  `e1c6bbe`). Disclose that the fleet-root observation at 20:00:53Z has no committed receipt: the copy was deleted.

### F3 (high, missing mistake): QUALITY 86's own check fails on the round-29 Gate it was written for
- Counterexample: the lesson says routed defect 3 is met: "this Gate carries reject rows; QUALITY 86"
  (`round-29.md:85`). I ran the check at `corpus/QUALITY.md:441` on `round-29.md@8809a3f`. It printed
  `gate_reject_rows=0 none_declared=0 malformed=0`, exit 1 (`scratch/q86-round29.txt`). The cause: all 8 reject rows
  use `—` as their id, and the check's filter `^\| *S[0-9]+ *\|` skips them. The criterion text (`:433-437`) does not
  require an `S` id. Its check does.
- Axes: discernment and calibration. This is the same shape as M2: a criterion put in place without being run on the
  round's own output.
- Smallest correction (append): **M6 — a new criterion's check never run on the deliverable it governs (class:
  `vacuous`).** Captured-by: `CORPUS.md:179-184`. Fix: add a superseding QUALITY row (criteria are never rewritten,
  `LEARNING.md:60-61`) whose check also counts `| — |` reject rows. The red-before is the receipt above. Until then,
  routed defect 3 is not met.

### F4 (high, all rows): no class is from the required vocabulary
- Evidence: `CORPUS.md:173-175` lists `vacuous`, `survivor`, `stale-premise`, `reference-drift`, `number-drift`,
  `scope`, `attribution`, `landing`, `provider`. Round 29 uses "stale self-assessment", "unscreened instrument",
  "write outside the lane" and "receipt provenance". Across the lane, 0 of 23 `(class: …)` labels in
  `corpus/lessons/*.md` is a §5 token. A `grep -wE` count prints 1, but that hit is `version-scope` (`round-26.md`)
  matching on the hyphen (`scratch/class-labels.txt`).
- Smallest correction: prefix each class with a token and keep the gloss.
  - M1: `reference-drift`. The operability row's `round 14 (6 → 7)` points at a real round that says `unchanged`,
    which is the C01 exemplar.
  - M2: `scope`. The miss condition was bound beyond the instrument's evidence.
  - M3: `attribution` (C10, write-scope).
  - M4: `landing` (C09), and it repeats round-28 M5.

### F5 (high, M1/M2/M4): captured-by names who noticed, not the rule that should have caught it
- M1 says "none". But `PROTOCOL.md:436` requires each SCORECARD row to carry an evidence pointer and a last-change
  round, and to be "re-derivable". The fleet `AXES.md:15` observable for calibration is "SCORECARD entries match
  observed repo state". Correction: "Captured-by: `PROTOCOL.md:436`, `AXES.md:15` (a protocol rule with no enforcing
  check)". Residual to disclose: the rewritten rows at `420d05ad` (`SCORECARD.md:10-15`) still carry no counting
  command and no measured commit, which `:436` also requires.
- M2 says "the L1's pre-freeze run". That is the detector. Nothing required a realistic clean pass, so correct it
  to `none`.
- M4 says "the round-28 closure". Correct it to "QUALITY 84 (should have; it passed)". I ran
  `check-tip-receipts.sh 1fc6bb0 28`. It prints `tip_receipts=met`, and the QUALITY 87 body then prints
  `header_not_parent=.ufo/waves/round-28/evidence/tip-count-c1.txt`, exit 1 (`scratch/q87-1fc6bb0.txt`). M4's fix
  receipt is real. Name it as `w1/DraftQualityCriteria.md:26` (committed `e1c6bbe`). `make-tip-receipts.sh` is a
  maker, not a check: it can only be shown on the round's last batch.

### F6 (medium-high, M2): the evidence premise is false, and the named fix does not exist
- M2's title says "before it was run on a known-clean input". `w1/BuildBlindCheck.md:30-35` records a synthetic
  clean-directory run, `blind_violations=0`, exit 0, and `:13` records the round-28 red, `blind_violations=38`. So the
  real defect is that the only clean control was synthetic and written to match the regexes.
- I confirmed false positives in the hit lines:
  - `AxisOperability.md:19` is a `git show … # exit 0` comment.
  - `BuildTipReceipts.md:135` is "wrote … (exit 2)".
  - `DraftQualityCriteria.md:75-76,86` quote criterion 85's own text and its red input `mori-oom-killers.py:305`.
  - Writer headings that the checker missed: "## Opened files and URLs" (`CaseA207a.md:192`), "## Files and URLs
    opened" (`CaseA207c.md:192`) and "## Opened files, source URLs, and evidence" (`CaseA210d.md:182`). The only
    writer not flagged uses "Files opened:" (`CaseA210c.md:194`).
- The fix says "a rule that a gate enters a counted condition only after a receipt of it on the round's own inputs".
  No such rule exists in QUALITY. `:461-464` is a note appended under 85 that points back to the lesson.
- Correction: retitle M2 "bound into a counted condition after only a synthetic clean control". Write the rule as a
  new numbered QUALITY row citing round-29 M2. Its red is `scratch/blind-at-freeze.txt`, i.e. 20 hits, of which at
  least 13 are false. Keep "not yet shown able to fail" until that row has a check and a receipt. Leave hit-by-hit
  adjudication to the wave-2 adjudication seat; my reading does not replace it.

### F7 (medium, missing mistakes): contract defects caught by critics and fixed by A1–A4 are not mined
The amendments are the evidence. Each of these is a declaration mistake, and two repeat mined classes:
- **C1 kind 4 vacuous at declaration** (`w1/CriticC1Design.md:26`, "kind 4 is vacuous once kind 1 holds, so any
  score passes"; fixed by A1). Class `vacuous`. It repeats round-26 M1 ("fail-open counter"). Fix able to fail: not
  yet. `c1-before.txt` shows no kind-4 hit, and all scores were held. This is pending the C1 mutation-test seat.
- **C2 statement false as declared** (`w1/CriticRoutingCoverage.md:108-111`, F6: the "no seat … runs the tool"
  sentence; `:123-129`, F7: the "writers rest on S153+" sentence; corrected in A2 at `contract.md:149-153`). Class
  `attribution`. It repeats round-28 M4 ("false provenance"). The fix is text only: not able to fail.
- **C2 had no provenance link and non-deciding pins** (`w1/CriticC2Design.md:12,38,90`; fixed by A3 F2 and A4 R1).
  Class `vacuous`. Fix: the counter's `provenance=` and `shape_*` lines. Able to fail: yes at `7118f320`, where the
  file is absent and the counter prints unmet (`evidence/c2-before.txt`). There is no red receipt for a selected or
  edited case: not yet.

### F8 (medium, missing obligation): M1 and M2 lack the required QUALITY criterion
- `LEARNING.md:19-21`. M1 (captured-by `none` as written) and M2 (`none` once corrected) have no numbered criterion
  citing `round-29`. `grep -n 'round-29' corpus/QUALITY.md` finds only the 85 check line and the `:461-464` note.
- Correction: add numbered rows citing `lessons/round-29.md` M1 and M2, or state in the lesson why not.
  `count-c1.sh` is a round counter, not a standing criterion.

### F9 (low-medium, M1 and "What the round learned"): number drift and the fix-parent receipt
- `round-29.md:10` says "five of six rows did not cite the latest admitted `improved` closure". `evidence/c1-before.txt`
  shows kind 1 on all six rows, and kind 2 on five. Correct it to six.
- `:9` "for four rounds" carries no command (`CORPUS.md:33`). The MANIFEST at `63729047` admits adjacency improved in
  rounds 14, 18 and 19, while the row read `round 1`. My MANIFEST query: rounds 12, 14–16, 18, 19, 21, 22, 24–26 and
  28 are admitted with at least one axis improved. M1 also lists the latest-closure rounds as 19, 25, 26 and 28 and
  omits depth's R=12 (`c1-before.txt:4`).
- `CORPUS.md:180-181` requires "the fix as the only delta". The committed red is at `7118f320`, and 50 files
  differ from there to `420d05ad`. The fix's parent `e1c6bbe7` differs from `420d05ad` only in `SCORECARD.md`
  (`git diff --name-only e1c6bbe7 420d05ad`). I ran the counter at `e1c6bbe7` and it printed `mismatches=11`,
  `C1=unmet`, exit 1 (`scratch/c1-parent-run.txt`; counter sha256 `a26604ee…e791`, unchanged since `e1c6bbe`).
  Correction: cite or commit the parent run as M1's red-before.

### F10 (pending, not a finding yet)
The first tool run is FAIL 11/24 (`evidence/c2-freeze-selftest.txt`). Every `case error` or `unclear text` ruling
from the judge seats is a C2 miss (`contract.md:78-79`) and needs its own Mistakes row once the rulings land. A
`tool error` ruling needs a row only if the draft tool change is admitted.

## Text to append to `## Mistakes` (corrections are new lines, never rewrites)

```
Corrections (wave 2, CriticLessonMistakes):
- M1: class reference-drift (CORPUS.md:173-175); captured-by PROTOCOL.md:436, AXES.md:15 (no enforcing check);
  red-before at fix parent e1c6bbe7 mismatches=11 exit 1; "five of six" (:10) reads six (c1-before.txt:2-7).
- M2: class scope; captured-by none; a synthetic clean control existed (w1/BuildBlindCheck.md:30-35); the stated rule
  is not yet a QUALITY row; not shown able to fail. Does not lift the A4 miss (M5).
- M3: class attribution; repeats round-28 M2; captured-by QUALITY 43 and tools/mori-wave-settlement.py (not run);
  the tool flags this misroot (settled 35/35 → partial, CaseA207c misrooted); sha256 0fe85d0b2ce857cd954c6831ec90704
  3590651ec47794760512f87f88a505a0a; no committed receipt of the fleet-root copy.
- M4: class landing; repeats round-28 M5; captured-by QUALITY 84 (its check prints tip_receipts=met on 1fc6bb0);
  red receipt w1/DraftQualityCriteria.md:26.
- M5 (scope): A4 blind_violations=0 read with an adjudication escape (LOG.md:1928-1929) that A4 lacks; at freeze
  d6d5cb0a the check prints 20, exit 1 → C2 miss under A4.
- M6 (vacuous): QUALITY 86 check prints gate_reject_rows=0, exit 1 on this lesson (8 reject rows with id —);
  routed defect 3 not met until a superseding row counts them.
- M7 (vacuous; repeats round-26 M1): C1 kind 4 vacuous at declaration (CriticC1Design F1); A1; not yet shown.
- M8 (attribution; repeats round-28 M4): contract C2 lines false as declared (CriticRoutingCoverage F6, F7); A2.
```

## Checks for the L1 (all run by me, read-only; outputs in scratch)
1. `bash .ufo/waves/round-29/check-blind-wave.sh d6d5cb0a… .ufo/waves/round-29/w1 '^CaseA2(07|10)[a-d]\.md$'` → 20, exit 1.
2. The QUALITY 86 awk (`corpus/QUALITY.md:441`) on `git show 8809a3f:corpus/lessons/round-29.md` → exit 1.
3. `bash .ufo/waves/round-29/count-c1.sh e1c6bbe7 63729047…` → `mismatches=11`, exit 1; at `420d05ad` → 0, exit 0.
4. The QUALITY 87 body (`:453`) with `<lane> 1fc6bb0 28` → `header_not_parent=…tip-count-c1.txt`, exit 1.
5. The settlement scan on a sandbox clone with `CaseA207c.md` moved to a stand-in fleet root → `misrooted` 1.
