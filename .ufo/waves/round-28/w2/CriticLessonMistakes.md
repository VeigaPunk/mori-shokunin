# Round 28 wave 2 — CriticLessonMistakes

**Verdict: partial** — attacked `corpus/lessons/round-28.md` `## Mistakes` (M1–M5) at `f2de0eedcd60d2e354da75265ea6122bc3896073`.
Every fix that has a check can fail. But M3's class is wrong and its fix cannot fail, the captured-by field is used
inconsistently, the M4 fix does not cover its own evidence (S143, S144), and four round-28 mistakes are missing.
The worst missing one: blind case writer CaseA2r03 read a non-blind report *before* writing its cases.

Seat: MoriR28.CriticLessonMistakes (critic, leaf). Clock: 2026-10-22T18:51:49Z start, 18:58:22Z report. Committed
bytes were read with `git show f2de0ee:<path>`. Scripts ran from byte copies, and mutants were built in a
`git clone --no-hardlinks` sandbox under `/fast/scratch/hyaku/mori-r28-w2/CriticLessonMistakes/`. The only lane
write is this file. Tools: git, python3, bash, sqlite3 (I only listed tables, read-only). Installs: none.

## Per-mistake findings

| id | class right? | captured-by honest? | fix able to fail (run) |
|---|---|---|---|
| M1 | yes | no: "none", but the r27 closure caught it | yes: exit 1 |
| M2 | yes | roughly | yes in a sandbox; fooled by one byte; misattributes provenance |
| M3 | **no** | yes | **no**: a contract sentence, not a check |
| M4 | yes (loosely) | arguable: "none" | yes on the eight new rows, **never on S143/S144** |
| M5 | yes | no: "none", but the r27 closure caught it | yes: exit 1; "r27 tip receipts now exist" overclaims |

**M1.** I ran `python3 -I -B check-heading-time.py df886be1 .ufo/waves/round-27/contract.md` and got
`stated=2026-10-22T15:55Z ... cI=2026-10-22T12:50:10-03:00 ... verdict=FUTURE-DATED`, `headings=1 future_dated=1`,
exit 1. With `--bound aI` it also exits 1. The fix can fail.
- The class is right: the lesson cites `round-27-verifier-spotcheck.md:34-37`, and that passage is the defect.
- The captured-by is wrong. "none" contradicts the evidence the lesson itself cites: the round-27 closure found W1
  and routed it (spotcheck `:34-37`, `:144-145`). M3 credits the same closure as "the closure (outside)".
- Side effect (a tradeoff, not a defect): W1 is never rewritten, so at `f2de0ee` the same check on the round-27
  contract still exits 1 (`contract.md:91 FUTURE-DATED`). It stays red unless run with `--heading`.
- Gap: the check only reads `^#{2,6} ` headings (`check-heading-time.py:34`). QUALITY 83 says "a dated amendment or
  heading", so a dated amendment written as a bullet or bold line is not checked.

**M2.**
- Live: `misroot-hash-check.sh 27 f2de0ee` gives `misroot_hits=0`, exit 0. The committed before receipt
  (`evidence/misroot-before.txt`) shows 7 hits, exit 1.
- Sandbox: a fake fleet (a fresh git repo plus a symlinked lane clone; only `FLEET=` changed) holding a byte-exact
  `base.c` gives `misroot base.c sha=cef1a2cf3f34f683 cited-by=.ufo/waves/round-27/w1/CriticC1Novelty.md`,
  `misroot_hits=1`, exit 1. So the fix can fail.
- Counterexample 1: append one newline to that `base.c` and the result is `misroot_hits=0`, exit 0. Any re-fetch,
  partial fetch or edit escapes the check, and so does any seat that never records a sha256.
- Counterexample 2 (false provenance in the fix itself): `misroot-sbx.sh 28` on the same file reports
  `cited-by=.ufo/waves/round-28/evidence/misroot-before.txt`. The check searches all of `.ufo/waves/round-N/`,
  including its own receipts, so it credits the hit to a "report" that is its own output.
- Disposition: `763d346` commits all seven upstream files at the lane root (`git show --stat 763d346`: `base.c`
  3990 lines, `sd-main.c` 4048 lines, and five more). The retention metric did not rise: scan at `6ebd518f` and at
  `f2de0ee` both give `"metric":4`.
- [INFERENCE] The r27 closure ruled these files "Operator items (not lane debt)" (spotcheck `:156-158`). An L1
  deleting fleet-root files is outside lane scope, and the lesson does not say who authorised it.

**M3.**
- Class wrong. The closure ruled "the lesson is about declaration timing (the lane's own M4)"
  (spotcheck `:77-79`). Round 27's lesson classed it "single point of failure in a claim" (`round-27.md:54`).
  Round 28 landed a C2 freeze within one round, so "claim declared beyond what one round can land" is false.
- Fix cannot fail. `contract.md:5-6` is a sentence: no check, and no state can turn it red.
- The "ten writers" do not remove the single point of failure; they multiply it. There is one seat per rule
  (contract C2 Statement, `contract.md:37-38`) and `count-c2.sh:20` prints `a2_rules_covered=<k>/10`. One dead
  writer uncovers its rule and C2 misses. The withdrawal became a miss; the failure mode did not change.

**M4.**
- Fix can fail on the eight new rows. Mutant: add the non-citing `corpus/lessons/round-24.md` to S148's
  `used-by`, commit in the sandbox, and run the counter (only `LANE=` repointed, plus a `sed` line repointing the
  frozen check's `LANE`). Output: `fail S148 used_by_not_citing=corpus/lessons/round-24.md`, `superseding=6/8`,
  exit 1. Pristine `f2de0ee` in the same sandbox: `superseding=7/8`.
- It never fails on the rows M4 uses as evidence. `count-c1.sh:17` fixes `MAP="S145:S096 … S152:S140"`, so S143 and
  S144 are never checked. At `f2de0ee` they still name `used-by` files with 0 citations
  (`system-pressure-r24.md: 0`, `round-24.md: 0`, `round-24-verifier-spotcheck.md: 0`). Neither the pristine nor
  the mutant counter output has an S143 or S144 line.
- The lesson's "shown able to fail" receipt (`c1-before-a1.txt` at `6ebd518f`) has every row `row_absent`, so it
  never reaches the `used_by_not_citing` branch. It shows the counter failing, not the M4 fix failing.

**M5.**
- `check-tip-receipts.sh df886be1 27` gives `receipt=MISSING` for count-c1, count-c2 and retention,
  `tip_receipts=unmet`, exit 1. The fix can fail.
- Captured-by "none" is wrong: closure routed defect 2 (spotcheck `:146-147`).
- "the round-27 tip receipts now exist" overclaims. Only `r27-tip-c1.txt` and `r27-tip-retention.txt` exist
  (`git ls-tree` of `round-28/evidence`). There is no count-c2 receipt, although the check's own rule says "A
  receipt for a withdrawn claim is still required" (`check-tip-receipts.sh:18-19`). Both receipts measure
  `df886be1` itself (`revision: df886be1…`), not its parent, so they do not meet QUALITY 84's definition.

## Missing round-28 mistakes

**X1 — blind case writers read a non-blind report (class: blindness boundary not enforced).**
- CaseA2r03 opened `CriticC2Design.md` lines 1-45 "before I had seen the case file schema and before I wrote any
  case" (`w1/CaseA2r03.md:187-196`).
- Those lines name output columns, `_lookup` and "missing in result" behaviour (`CriticC2Design.md:12-45`).
- CriticC2Design itself says: "If a writer's transcript shows a read of this file, that writer's cases are tainted"
  (`:7-9`).
- CaseA2r01 read head and tail of the same file "after the case file was finalised" (`w1/CaseA2r01.md:36-45`).
  "Finalised" is self-attested; no hash of the case file was taken before the read.
- Both reads break the brief's "You may read ONLY" list (`wave1-run.json` CaseA2r03 task).
- The A2-03 cases were frozen unedited (`cases-a2.json` ids `a2-03-group-kill-*`). Commit `d21b8bd` says "30 blind
  cases", `LOG.md` says "ten blind CaseA2rNN reports", and no lane file outside `w1/` mentions taint
  (`git grep -i taint`: only old lessons).
- Root cause: blind and non-blind seats write into the same `w1/` directory at the same time.
- Smallest correction: add the mistake to the lesson, name the A2-03 taint for the A2 judges, and keep blind
  writers' reports and inputs in a directory that non-blind seats never write to.

**X2 — the S101 superseding seat ran late, not S140 (class: late seat output outside committed bytes; a repeat of
r27 M1).** The brief's example "SupersedeS140 stopping before its report" is not borne out:
- `SupersedeS140.md` is in `1c4c186`: 83 lines, with a findings section (§9), file mtime 15:24:45-03:00.
- The seat with no report at `f2de0ee` is SupersedeS101. It was dispatched (`wave1-spec.json`), but its report's
  mtime is 15:54:02-03:00 and it first lands in `6b695b0` together with S147.
- At `f2de0ee` the counter gives `superseding=7/8`, `fail S147 row_absent`, `C1=unmet`, yet lesson line 11 says
  the corrected text lives in "S145–S147".
- From `1c4c186` to `6b695b0`, S101 sat restored to its first-published (wrong) wording with no superseding row.
  That breaks the lesson's own first rule (line 9).
- I did not read seat transcripts (privacy bound), so why it ran late is not established.

**X3 — a live reader cites a row that does not exist (class: dangling citation; counter blind spot).**
- `corpus/knowledge/harness-job-capacity-r25.md:47` cites `(S147, …)` from `1c4c186` onward
  (`git log -S'S147'`), while the S147 row is absent until `6b695b0`.
- `readers_left=0` at `f2de0ee` because `count-c1.sh:80-81` only looks for old ids. Nothing checks that a cited
  new id exists.

**X4 — a counter landed before its author's report (class: provenance missing from committed bytes).**
- `LOG.md:1885` and `7b75f45` cite "wave-1 BuildCountC2, sha256 a7536fc5…".
- `BuildCountC2.md` is absent at `f2de0ee`. It is first committed in `84abe93` (15:55:05-03:00), five commits
  later, and only reachable via `git log --all`.
- FixR1Runway and FixR5RoutedSelftest also have no wave-1 report at `f2de0ee` (both dispatched per
  `wave1-spec.json`). [INFERENCE] These are hygiene, not claims.

**X5 (minor) — the brief widened the contract.** C2 says writers "read only the rule text, the round-26 contract
and the round-26 frozen case file" (`contract.md:37-39`). The brief adds upstream earlyoom `kill.c`, `main.c` and
`msg.h`. Neither amendment A1 nor A2 records the change.

## Impacted axes
- **Operability (C2):** X1. A2-03 cases from a writer who calls itself tainted are frozen and labelled blind.
- **Freshness (C1):** X2 and X3. C1 is unmet at `f2de0ee`, and a reader points at a missing row.
- **Calibration:** M3's wrong class, the inconsistent captured-by field, and M5's overclaim.

## Smallest safe corrections (lesson text only; the case file and history stay untouched)
1. M1 and M5 captured-by: "the round-27 closure (outside)". M4: "round-28 wave-1 CriticC1Design (non-author)".
2. M3: change the class to "single point of failure in a claim (declaration timing)". Say the fix is a process rule
   that cannot be shown to fail, and that one writer per rule keeps ten single points of failure.
3. M4: say the counter covers only S145–S152, that S143 and S144 remain uncited at the tip, and cite the
   mutant-style failure rather than the all-`row_absent` receipt.
4. M5: "r27 tip receipts exist for C1 and retention only; no C2 receipt; measured at `df886be1`, not its parent".
5. M2: name the one-byte blind spot and the self-citation through `evidence/`. A minimal fix for the latter is to
   exclude `evidence/` from the grep path.
6. Add X1–X4 as M6–M9 with the evidence above.

Checks for the integration owner: re-run `count-c1.sh` at the landed tip, after `6b695b0`. Have the A2-03
judges (JudgeA2r03) weigh X1.
