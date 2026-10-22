Verdict: **defect found.** M5 misstates the mistake that caused the C2 miss. QUALITY 93 can fail, but its literal check passes round 29, the round whose M2 it was written to catch. M2 contradicts the lesson's own R3. Two mistakes from this round are missing.

# CriticLessonMistakes — attack on `corpus/lessons/round-30.md` `## Mistakes` (MoriR30 round 30, wave 2)

Attacked revision: `ad0f04745ced2194e58c22a0d6b38131bee3e230`. Every file below was read from committed bytes
(`git show ad0f047:<path>`). Lesson line numbers refer to `ad0f047:corpus/lessons/round-30.md`; QUALITY line numbers
refer to `ad0f047:corpus/QUALITY.md`. Scratch work is under `/fast/scratch/hyaku/mori-r30-w2/CriticLessonMistakes/`.
Tools: none installed or updated. No pacman. The only git writes were in a sandbox clone under scratch.

## 1. M5 and QUALITY 93 (the main item)

**Counterexample A. The A3 gate could have been run on the round's own inputs before the freeze. It was never
run on them until after the freeze.**
- Commit order (`git log --format='%h %cI' a66751b..ad0f047`):
  - writer reports `b039dd4` 18:15:51
  - A2 gate `32e287f` 18:32:49
  - A3 `55f9a69` 18:33:54
  - counter `8ac9535` 18:48:00
  - freeze `db1ec46` 18:48:21 (all times -03:00)
- The gate blob is `dbcbe50e` at `55f9a69`, `8ac9535` and `db1ec46` (`git rev-parse <rev>:.ufo/waves/round-30/check-blind-wave.sh`).
  So the counted blob existed 14 min 27 s before the freeze, and the writer reports it reads already existed.
- I re-ran it at the A3 commit: `bash <(git show 55f9a69:…/check-blind-wave.sh) 55f9a69 .ufo/waves/round-30/w1
  '^CaseR30[a-d]\.md$'` prints `scanned=4`, `blind_violations=1`, `CaseR30a.md:105:writer-forbidden-opened-path`,
  exit 1. The counted miss was therefore visible from committed bytes before the freeze.
- No committed run of the A3 blob on `w1` exists before the freeze:
  - `evidence/c2-before.txt:24-25` reads `scanned=not_run`.
  - `gate-a2-prefreeze.txt:2` ran the `32e287ff` blob.
  - The first A3-blob run on `w1` is `gate-a4-diagnostic.txt:9-13`, at 21:51:01Z (`:1`), after the freeze at 21:48:21Z.
- M5's title (lesson `:94`) says the gate "was bound into a counted condition before it ran on this round's writer
  reports". That is false for the A2 blob: it did run on them before the freeze (`gate-a2-prefreeze.txt:1-9`,
  21:33:43Z; re-derived, it prints the same 4 lines). The real mistake is that **the gate was changed after that run
  (A3) and the changed blob was frozen without being re-run.** Round-29 M2's rule ("a receipt of it on the round's
  own inputs", round-29.md:36-37) was met in letter by the A2 receipt, which makes M5's claim that the rule was "not
  applied" (`:99-100`) imprecise.

**Counterexample B. The A2 receipt was not a full screen, because the gate reports only the first forbidden line of
each report.**
- `gate-freeze.sh:129` (same logic in the A2 blob) reads `if (( entry_forbidden )) && (( ! files_forbidden_seen ))`,
  so one `writer-forbidden-opened-path` hit is recorded per report.
- On CaseR30a the A2 run printed only `:96` (`gate-a2-prefreeze.txt:5`). The RULES.md line `:97` is acknowledged only
  in a hand comment (`:10`), and `:105` (`CaseR30a.md:105`, the closing sentence) was hidden behind `:96`.
- So "every hit adjudicated" on a receipt from this gate means "every *reported* hit". Adjudicating them does not
  surface the next one. Neither M5 nor QUALITY 93 mentions this masking.

**Counterexample C. QUALITY 93's check passes round 29.** QUALITY 93 is at `QUALITY.md:656-663`. Its Check is prose
with a free variable (`<gate receipt on own inputs>`). It has no runnable command, no exit codes, no "PASSES at", and
no "Red inputs", unlike rows 88-92. I encoded its literal reading as `scratch/q93.sh`:
- the freeze commit is the oldest commit adding the case file;
- the receipt's first commit must be a `git merge-base --is-ancestor` of the freeze;
- the receipt text must contain the freeze gate's git blob or sha256 prefix.

Results:

| input | output |
|---|---|
| r30, `gate-a2-prefreeze.txt` | `receipt_first=55f9a694 ancestor=yes names_freeze_gate=no`, `q93=fail`, exit 1 |
| r30, `gate-selftest.txt` | `ancestor=yes names_freeze_gate=no`, fail, exit 1 |
| r30, `c2-after.txt` / `gate-a4-diagnostic.txt` | `receipt_first=0b828c27 ancestor=no`, fail, exit 1 |
| **r29**, `blind-check-prefreeze.txt` | `freeze=d6d5cb0a receipt_first=d6d5cb0a ancestor=yes strict_before=no names_freeze_gate=yes`, **`q93=pass`, exit 0** |
| sandbox: receipt of blob `dbcbe50e` with 4 hits and no adjudication, committed on top of `8ac9535`, then `db1ec46` cherry-picked | `strict_before=yes names_freeze_gate=yes`, **`q93=pass`, exit 0** |

- Round 29 passes for two reasons. Its receipt was added in the freeze commit itself (`git log --diff-filter=A` for
  both files prints `d6d5cb0`), and `is-ancestor` is reflexive. The receipt also names the gate sha256 (`:1`
  `b0573035…`) while printing `blind_violations=20` (`:3`), with zero adjudication lines
  (`grep -c -i 'adjudicat\|false positive'` prints 0).
- The row's prose says "before the freeze". Its check says "ancestor of the freeze commit". These disagree on the
  exact round-29 shape.
- The sandbox case shows that the check never reads adjudication, and never reads a non-author seat.

**Answer: can QUALITY 93 fail?** Yes. It fails at round 30, but only on the "names the freeze blob" clause. The red
reason the row gives ("4 unadjudicated hits", `:662`) is not something the check measures. Those 4 hits were also
adjudicated, by the author, in A3 (`contract.md:212-216`; `gate-a2-prefreeze.txt:10`). So "unadjudicated" should read
"author-adjudicated". Given counterexample C, QUALITY 93 is not shown able to fail on the defect it names.

**Counterexample D (side issue). The gate's verdict depends on where it runs.** In the sandbox clone, the same blob
`dbcbe50e` flags the `rule-text.md` lane-path line in all four reports (`CaseR30a.md:98`, `b:117`, `c:78`,
`d:111`; 4 hits). The allowlist pins the lane path (A2, `contract.md:166-167`). QUALITY 93 does not say where the
receipt run must happen, so a receipt from a different checkout path can show hits that the lane run does not.

**Tradeoff for the canonical judge (not a fixable defect).** QUALITY 93 allows the gate to be edited after it has
seen the round's own writer reports, as long as the frozen blob carries an adjudicated receipt. That turns A3's
disclosed after-data counter change (`contract.md:218-221`, "the closure judges whether C2.4 stands on the A3
version") into routine practice. A gate tuned until it prints 0 on the same inputs it is then graded on certifies
nothing beyond the adjudication. The judge must decide whether that is acceptable.

**Smallest safe correction for M5 and QUALITY 93:**
- Retitle M5 to "the gate was changed after its own-input run (A3) and the changed blob was frozen without a re-run;
  the gate also reports only the first forbidden line per report". Cite `55f9a69` and the command above as the
  pre-freeze red.
- Make QUALITY 93's check runnable over committed bytes:
  - the receipt's first commit is a **strict** ancestor of the freeze;
  - the check itself re-runs `bash <(git show F:gate) <receipt-commit> w1 <regex>` in the lane, rather than trusting
    the receipt text;
  - every printed hit appears in a non-author adjudication file committed before the freeze;
  - the gate reports every forbidden line, not the first per file.
- Add "PASSES at"/"FAILS at" receipts (round 29 `d6d5cb0a` must FAIL) and Red inputs.
- Any gate change after the own-input run is an amendment that needs a fresh receipt of the new blob.

## 2. M1-M4: class, evidence, captured-by, fix, shown able to fail

M1-M4 are copied from the wave-1 draft `w1/MineMistakes.md:20,38,53,70`, written before the data landed. Several
present-tense lines are now false at the tip:
- `:41-42` and `:73-74`: "at `e936482` `corpus/lessons/round-30.md` is absent", offered as the reason the green is
  unobserved;
- `:81`: "the working tree has none";
- `:90-91`: "Both green values are unobserved".

**M1 (lesson `:26-42`).**
- Evidence: correct. The lesson's own R2 re-fetch is consistent with it (`:158-168`).
- Class "reference-drift" is wrong. R2 shows the re-fetched digests and sizes *equal* the row's recorded ones
  (`:160-163`), so nothing drifted. The absence claim was false when it was written. "Unverified absence claim" fits.
- Shown able to fail: unsupported. It promises "a check that re-runs `grep -icE 'dryrun|version'` … and requires the
  correction to name `kill.h:36-37`" (`:38-39`). `git grep -n "grep -icE" ad0f047` finds only that prose, in the
  lesson and in `w1/MineMistakes.md:32`. No such check is committed.
- The routed row for this defect, QUALITY 89 (`QUALITY.md:486-524`), checks form, not truth:
  - At `ad0f047` round 30 it prints `absence_reject_rows=0 malformed=0`, exit 0. That is a vacuous pass. The round-30
    Gate phrases absences as "returns nothing" or "0 occurrences" (lesson `:121-123`), which its regex does not match.
  - On the round-29 row with a *fabricated* witness appended
    (`` (`grep -in -e dryrun -e version kill.h` → `0`, exit 1) ``) it prints `absence_reject_rows=1 malformed=0`,
    exit 0 (`scratch/q89cx`). That witness is false, because `kill.h:36-37` matches.
  - So M1's recurrence (a false absence claim) passes QUALITY 89.
- Correction: name QUALITY 89 as a form-only fix, and either commit the re-grep check or mark "shown able to fail" as
  not met.

**M2 (lesson `:44-57`).**
- Defect: it contradicts the same lesson. M2 says "two quote word-count labels are one high". R3 (`:169-183`) and
  QUALITY 90 (`QUALITY.md:570-573`, which says "Two … are one high" is under-sampled) find five, with `:63` two high.
- Re-derived: QUALITY 90's check at `a66751b` round 29 prints the five lines `57 11/10, 60 11/10, 61 5/4, 62 17/16,
  63 8/6`, then `word_labels=16 mismatched=5`, exit 1. M2's stated red-before (two lines, `:56`) is not the output
  of any committed check.
- Its fix ("append a correction … giving 10 and 16", `:52`) is narrower than the R3 correction that actually shipped.
- Class "number-drift": same objection as M1. The labels were wrong when they were written (`:180-182`).
- QUALITY 90 at `ad0f047` round 30 prints `word_labels=26 mismatched=0`, exit 0, so this round's Gate is clean.
- Correction: M2 should state 5 labels and cite QUALITY 90 and its red.

**M3 (lesson `:59-74`). Agree.**
- Re-derived: `check-tip-receipts.sh b581173a 29` prints `cited_lane=no` for `count-c1.sh` and `count-c2.sh`,
  `cited_lane=yes` for retention, `tip_receipts=unmet`, exit 1.
- `git show b581173a:LOG.md | grep -c tip-c1.txt` prints 0, and `check-tip-receipts.sh:37` is the default report set.
- At `ad0f047`, LOG has 2 and the lesson 4 `tip-c1.txt` mentions.
- The green cannot be observed until the receipts-only batch lands. At `ad0f047 30` it prints `unmet` (receipt
  `MISSING` for c2 and retention), as expected.
- Only defect: the stale line at `:73-74`.

**M4 (lesson `:76-93`). It duplicates M5, and its fix is already shown insufficient.**
- Same class, same cause, same "repeats round-29 M2" (`:77`, `:95`). That is two entries for one mistake.
- M4's fix (gate plus `--selftest` receipt before the freeze, `:87-88`) was carried out: `gate-selftest.txt:2-4`
  shows `PASS`, and `c2-after.txt:18-19` shows `gate_selftest=PASS`, `gate_mutants=4/4`. C2 still missed
  (`c2-after.txt:21-22`). The round therefore shows that QUALITY 91 (`QUALITY.md:580-597`, the selftest-only row)
  can pass while the gate fails on its own inputs. The lesson never says this.
- Its residual claim (`:91-93`), that a blind spot "surfaces only once the data is frozen", is contradicted by
  counterexample A: the reports landed at `b039dd4`, before the gate, so the gate could and did run on them before
  the freeze.
- QUALITY 91 `:594-595` ("Until the round-30 gate and its selftest are committed this row is unenforced") is stale
  at the tip.
- Correction: merge M4 into M5, or mark M4's fix as met-and-insufficient. Record that QUALITY 91 passing does not
  imply anything about own inputs.

**M5 class "scope".** It matches round-29 M2's corrected class (`round-29.md:96`), so no objection. The evidence
pointers are accurate (re-derived above). The defects are in the title, the captured-by and the fix (section 1).

## 3. Missing mistakes (sweep: amendments A1-A3, `evidence/`, LOG `:1952-1989`)

1. **The changed gate was frozen without a re-run (class: unscreened change).** See counterexample A. This is the
   proximate cause of the C2 miss. M5 folds it into a title that misstates it.
2. **The gate masks every forbidden line after the first in each report (class: instrument).** See counterexample B
   (`gate-freeze.sh:129`). It made the round's only pre-freeze own-input receipt incomplete.
3. **The L1's brief and the L1's gate contradict each other (class: prompt-induced, a class already used in the
   corpus).**
   - Each writer brief in `wave1-spec.json` (lines 10, 15, 20, 25; 4 matches) says: "a heading line exactly `## Files
     opened` followed by one line per file path or URL … nothing else under that heading); then one sentence that you
     opened no tool …". No heading follows, so the required sentence necessarily sits under `## Files opened`.
     CaseR30a obeyed (`CaseR30a.md:105`), and the gate parsed that sentence as an entry.
   - The same dispatch tells every seat to read RULES.md first (`wave1-spec.json:5`), while the A2 allowlist
     (`contract.md:166-169`) forbids that file. That is the cause of A3.
   - Both instructions were written by the same author who wrote the gate's contract. M5 calls these "instrument
     false positives" and never names the brief.
4. **M2 is itself a round-30 mistake (class: under-sampled).** The lesson ships a two-label entry beside a
   five-label correction (section 2).
5. **Pre-landing draft text shipped as tip claims (class: stale self-assessment, used at round-29.md:26).** See the
   lines listed at the top of section 2, copied from `w1/MineMistakes.md`.

No mistake was found in A1, the C1 path, the differential (`c2-after.txt:16` 94/94 changed=2, consistent with LOG
`:1980-1982` 126/5) or the SOURCES R3 note (`git diff ee61010 ad0f047 -- corpus/SOURCES.md`: one appended paragraph,
no cell edited). I did not re-fetch any source URL; ReviewCorrectionsR2R3 and the Reopen* seats cover that. [INFERENCE]

## 4. Checks run (all exit codes observed)

- Gate from blobs: `32e287f` printed 4 hits, exit 1; `55f9a69` printed 1 hit, exit 1; `db1ec46` printed 1 hit, exit 1.
- `scratch/q89.sh`, `q90.sh`: extracted verbatim from `QUALITY.md:495-517` and `:535-567`, with only the
  placeholder line changed.
- `scratch/q93.sh` (my literal reading) and the sandbox clone `scratch/clone`, branch `cx`.
- `check-tip-receipts.sh` from the `ad0f047` blob, at `b581173a 29` and `ad0f047 30`.
