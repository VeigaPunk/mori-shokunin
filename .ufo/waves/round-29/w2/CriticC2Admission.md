# CriticC2Admission — round 29 wave 2 (falsify): attack on C2 admission

Seat: MoriR29.CriticC2Admission (critic, leaf). Lane tip reviewed: `8809a3fe1eaa87a0afa177a15263d174378e7462`.
Scratch: `/fast/scratch/hyaku/mori-r29/w2/CriticC2Admission/`. No tool installed or updated. The skill file
`skill://godspeed` did not resolve under `/home/vgpnk/.omp` (glob: 0 files), so I worked from the assignment alone.
The oom-killers tool was run only through `--selftest --cases` and its pure `read_inputs` function on copies in my
scratch directory. It was never run in live mode.

## Verdict proposal: **miss**

C2 fails a condition that amendment A4 itself names as a miss. The blind check run at the freeze commit prints
`blind_violations=20`. I reproduced that result at `d6d5cb0a`. A4 provides no adjudication escape. Every reading that
avoids the miss either adds an exception after the data was known or replaces the mechanical condition with
judgement, and both of those narrow the claim. The blindness is also not evidenced on substance, because five of the
eight writers disclose reading parts of the older case files beyond what their brief allowed. Separately, the
self-test on the frozen file is `FAIL 11/24`. Even the newest tool draft leaves three shape cases failing, so C2 is
`C2=unmet` today regardless of A4.

## Ranked findings

### F1 (decisive): under A4 R3, C2 is a miss, and I reproduced the result at the freeze commit
- Rule: "the `check-blind-wave.sh` run at the freeze commit ... must print `blind_violations=0`; otherwise C2 is a
  miss, reported as one" (`.ufo/waves/round-29/contract.md:177-178`).
- I ran `bash .ufo/waves/round-29/check-blind-wave.sh d6d5cb0a .ufo/waves/round-29/w1 '^CaseA2(07|10)[a-d]\.md$'`. It
  printed `blind_violations=20` and exited 1. Runs at `221cbd8f` and `8809a3fe` gave the same 20 hits.
- The committed receipt was taken at `221cbd8f`, the parent of the freeze, not at the freeze commit
  (`evidence/blind-check-prefreeze.txt:1-2`). This makes no difference in substance: the `w1` tree is the same object
  `af309bbb5b69…` at `221cbd8f`, `d6d5cb0a` and `8809a3fe` (`git rev-parse <rev>:.ufo/waves/round-29/w1`). The check
  script sha256 `b0573035…6e0f` is also the same in the working tree and at `d6d5cb0a`.
- The C2 counter at the tip agrees. `TMPDIR=<scratch> bash .ufo/waves/round-29/count-c2.sh 8809a3fe…` printed
  `blind_exit=1`, `blind_violations=20`, `a2_r29_selftest=FAIL(exit=1)`, `C2=unmet` and exit 1. It also printed
  `provenance=24/24 unselected=0`, `shape_a207=3/2`, `shape_a210=6/2` and `cases_changed_since_freeze=0`.
- Impacted axes: operability (C2), calibration (whether the reported verdict is honest).

### F2: every reading of A4 that avoids the miss narrows the claim
- The LOG entry adds an exception that A4 does not contain: "Under amendment A4 this is a C2 miss condition unless
  wave-2 adjudication finds the instrument at fault" (`git show 255b7051 -- LOG.md`, the added "Pre-freeze blind check"
  bullet). That LOG commit comes after the receipt that already showed 20 hits (`d6d5cb0a`). An escape written after
  the data is known is a narrowing. The contract forbids this: "A declared claim is never withdrawn; a miss is reported
  as a miss" (`contract.md:4-5`), and a failed process condition "is reported as a C2 defect, never dropped"
  (`contract.md:147-148`).
- On substance, the 20 hits are instrument false positives:
  - The 7 writer hits are writer reports whose files-opened lists sit under headings the regex at
    `check-blind-wave.sh:59` rejects, because extra words follow "opened". Examples: `CaseA207a.md:192` "## Opened files
    and URLs", `CaseA207b.md:195` "## Files and URLs opened" and `CaseA210a.md:203` "## Opened files and scope".
    `CaseA210c.md:194` "Files opened:" passes the regex.
  - None of the 13 non-writer hits is oom-killers tool output. They are `exit N` from git or other counters next to an
    `r27`/`r29`/`Observed:` token: `AxisOperability.md:19`, `BuildTipReceipts.md:135-140` and
    `ReviewLateMutHeadingCheck.md:37,39`. `DraftQualityCriteria.md:75-86` quotes the check's own marker spec.
  - Even so, "the instrument is at fault" is not a condition A4 recognises. A4 fixed this instrument before the data
    arrived, and the lesson admits it was never screened (`corpus/lessons/round-29.md:32-37`, M2: "Not yet shown able
    to fail").
- A repaired instrument would itself be tuned after the data. Strongest counterexample: I loosened only the heading
  regex in a scratch copy (`check-variant-heading.sh`, output in `variant-heading-run.txt`). It printed
  `blind_violations=16`. The 7 heading hits disappeared, but two new `writer-forbidden-opened-path` hits appeared at
  `CaseA210a.md:212` and `CaseA210d.md:191`, which are the writers' denial lines that name the tool file. A
  `CaseA210c` miss also appeared, because "Files opened:" has no `#`. So a repair only moves the hits around, and
  getting to 0 would need several regexes rewritten while looking at the result.
- Re-running the check at a later revision would not be "at the freeze commit", so it cannot rescue C2. See F5 for how
  the counter allows exactly this.

### F3: blindness is not evidenced on substance. Five of eight writers disclose reading older-case content beyond their brief
- The writer brief allows `cases.json` and `cases-a2.json` for "schema and journal line shapes only"
  (`/fast/scratch/hyaku/mori-r29/CriticC2Design/briefs.txt:19`, BLINDNESS clause). The older files pass the tool
  (`PASS 32/32` and `PASS 30/30`, re-run in scratch on `tool-base.py`). So their `expect` blocks equal the tool's output
  on those inputs [INFERENCE: exposure to them is exposure to the tool's behaviour].
- What each writer discloses:
  - `CaseA207a.md:199`: a preview showing initial case content.
  - `CaseA207b.md:209`: the reads "surfaced existing A2-07 case prose and inputs"; "this seat cannot claim an
    uncontaminated blind process".
  - `CaseA207d.md:204`: "displayed existing `expect`/verdict snippets"; "cannot certify a clean blind process. L1 should
    decide whether to accept or discard this draft".
  - `CaseA210a.md:211`: the reads returned `oomd_notices` members.
  - `CaseA210d.md:186`: the reads "surfaced the first example's why/expect text".
- False provenance: the freeze commit message says the cases were "assembled without edits from the eight blind writer
  reports" (`git show -s d6d5cb0a`). The lesson table also says "24 blind cases" (`corpus/lessons/round-29.md:84`). Two
  of those writers explicitly disclaim blindness.
- Correlation, using the base tool on the frozen file: writers who saw `expect` or verdict text (207b, 207d, 210d) have
  9 of 9 cases passing. Writers who disclose no such exposure (207c, 210b, 210c) have 0 of 9 passing. 207a and 210a
  have 2 of 6 passing. This comes from my per-case comparison of `L1/judge/<id>.base.json` against each case's
  `expect`. [INFERENCE: the data fit contamination, but they do not prove it, because those writers may simply have
  picked regions the tool already handled.]
- The instrument cannot catch this. `check-blind-wave.sh:132-147` forbids only the tool file, `corpus/lessons/` and
  other `w1`/`w2` reports in a writer's list, so reads of the older fixtures pass it.
- Impacted axes: operability, and the integrity of the claim (identity of "blind").

### F4: freeze order holds. No run of the tool on the frozen content is found before the freeze commit
- The parent chain is `221cbd8f` → `d6d5cb0a` → `255b7051` → `8809a3fe` (`git show --format='%H %P'`).
  - `221cbd8f` adds only the counter and receipts.
  - `d6d5cb0a` adds only `cases-a2-r29.json` and the blind receipt.
  - `255b7051` touches only `LOG.md`.
  - `8809a3fe` adds the first self-test receipt and the corpus files.
- The run time in the self-test header is `20:28:50Z` (`evidence/c2-freeze-selftest.txt:1`). The freeze commit is
  dated 17:28:24 -03:00 and the LOG commit 17:28:42 -03:00. Commit dates are self-reported.
- Frozen-file sha256 is `1c76ea1f…d252`, the same as `L1/cases-a2-r29.json`. That uncommitted assembly has mtime
  17:07:49, so it existed for about 21 minutes before the freeze. Inside that window, "no tool run" rests only on the
  L1's commit message [INFERENCE: not verifiable from artifacts].
- The `cases-a2-r29.json` in BuildCountC2's sandbox (mtime 17:20) is synthetic. Its sha256 is `2f130c63…`, its ids are
  `synthetic-a2-07-01…`, and its sandbox commit is "Synthetic C2 blind-check violation". `BuildCountC2.md:12`
  confirms this.
- Contract statement versus counter: the counter checks only `cases_changed_since_freeze=0` and a single add. It cannot
  see a working-tree run before the freeze. This gap is a tradeoff, not a defect.

### F5: the counter is fail-open against A4. It runs the blind check at `<rev>` with the script taken from `<rev>`
- `count-c2.sh:126-133` clones the lane, checks out `<rev>` (the landed tip) and runs `<rev>`'s own
  `check-blind-wave.sh` on `<rev>`'s `w1`. A4 instead says the run happens "at the freeze commit".
- Counterexample [INFERENCE: constructed, not run]: a post-freeze commit that only rewords writer headings or edits the
  check script would drive the counter to `blind_violations=0` while the freeze commit stays at 20. The provenance
  check would not stop it, because it compares only fenced JSON (`contract.md:157-160`).
- Correction: run the check at `freeze_commit` (the counter already derives it, printing `freeze_commit=d6d5cb0a…`),
  with the script blob from the freeze commit. Gate on that result.

### F6: the draft fix changes things that no judge ruled `tool error`
No ruling exists yet: `.ufo/waves/round-29/w2/` holds only `swarm-registry.json`, so no judge report is present. All
results below come from my runs in scratch on copies of `L1/judge/tool-base.py` (sha `343acaf4…`, equal to the tool
at `7118f320`) and `L1/judge/tool-fix.py` (sha `26091032…`). I ran `--selftest` and a full-output differential of
`read_inputs` over every case input of all three files.

- **F6a. The judged draft creates a new failure.** In `r29-a2-07-real-then-dryrun-zero-enter`, verdict, exit and
  sigterm matched `expect` under the base tool. The draft flips them: verdict `KILLERS_UNKNOWN`→`KILLER_ACTED`, exit 2→1,
  sigterm 0→1. A judge seat sees only mismatches, so pinned fields that were never mismatched cannot have been ruled.
- **F6b. Older-file outputs change without being pinned.** Three `cases-a2.json` cases change
  `earlyoom.earlier_invocation_send_lines`:
  - `a2-10-malformed-action-line-uncounted`: 1→0.
  - `a2-10-positive-evidence-elsewhere-stands`: 1→0.
  - `a2-10-oomd-notices-positive-malformed-records`: 2→0.

  The field is unpinned, so `PASS 30/30` holds, and no `KILLER_ACTED` verdict changes. The contract guard is therefore
  met, but no judge rules on older-file cases. A4 R4 requires this differential as a judged receipt
  (`contract.md:179-181`).
- **F6c. One change does not fix its mismatch.** In `r29-a2-10-failed-stamped-positive`, `earlier_invocation_send_lines`
  goes from 2 to 1 against an expected 0. The case still fails. The value moves without being resolved.
- **F6d. The draft under judgement is stale, and the newer draft reaches further.**
  - The judge packet `tool-fix.py` has mtime 17:30:17. `L1/fixclone/tools/mori-oom-killers.py` has mtime 17:33:58 and
    sha `41464957…`, and it differs from the packet.
  - The newer draft adds an unbounded-scope cut: for unbounded scope, keep lines from the last version line onward
    (`diff L1/judge/tool-fix.py L1/fixclone/tools/mori-oom-killers.py`, which shows the +292-302 hunk).
  - Its self-test results (scratch copy `tool-fix2.py`) are `PASS 32/32`, `PASS 30/30` and `FAIL 21/24`.
  - Counterexample outside A2-07's dry-run topic (`counterexample-unbounded-restart.txt`): the input is an active
    earlyoom with no `ActiveEnterTimestampMonotonic` and a journal of version, then a real SIGTERM send, then version
    again, with no dry-run line.
    - Base tool and judged draft: `KILLER_ACTED`, exit 1, sigterm 1.
    - Newer draft: `KILLERS_UNKNOWN`, exit 2, sigterm 0, earlier 1.

    This drops positive evidence that the round-26 verdict rule says stands when scope is incomplete
    (`round-26/contract.md` verdict 1, "Positive evidence stands even when the scope is incomplete"). No older case
    covers the input, so the guard against turning `KILLER_ACTED` verdicts passes vacuously.
- **F6e. A residual case error or unclear text appears likely under either draft.** The three `CaseA210c` shape cases
  (inactive, failed and not-found earlyoom) still fail on `version`, `grammar`, `dryrun_send_lines` and
  `process_group_lines`. The tool emits `null` or `unverified` where the writer expected `1.9.0`, `verified-1.9.0` and
  `0`. The writer's own note says the opened contract specifies `actions: null` for inactive or absent units
  (`CaseA210c.md:173`). [INFERENCE: if a judge rules any of these `case error` or `unclear text`, that is an
  independent C2 miss (`contract.md:78-80`). These three are half of `shape_a210`.]

## Answers to the assigned questions
1. **Is the blindness evidenced?** No. The mechanical receipt shows 20 violations at the freeze commit (F1). On
   substance, five of eight writers disclose reading beyond the schema, and two disclaim blindness (F3).
2. **Does A4 make C2 a miss?** Yes (F1).
3. **Is any reading of A4 that avoids the miss a narrowing?** Yes. These readings each narrow the claim: an
   "instrument at fault" exception added after the data, adjudicating the 20 hits down to 0, a repaired instrument,
   and a re-run at a later revision (F2, F5).
4. **Were the cases frozen before any tool run?** Yes, as far as the artifacts show. The commit order is as claimed
   and there is no trace of a pre-freeze run on the frozen bytes. The 21-minute uncommitted window before the freeze
   is attested only by the L1's statement (F4).
5. **Does the draft change anything not ruled `tool error`?** Yes, and no ruling exists yet. The judged draft flips a
   pinned verdict that was matching, changes three unpinned older-file outputs, and moves a value that still fails.
   The newer clone draft, which has not been judged, flips a `KILLER_ACTED` on a dry-run-free input (F6).

## Smallest safe corrections, for the L1 to apply; this seat edits nothing
- Report C2 as **miss** under A4 R3. Delete the "unless wave-2 adjudication finds the instrument at fault" clause from
  the LOG, or mark it as an after-data narrowing. Lesson M2 should say that the instrument's defect does not lift the
  miss.
- Strike "blind" from the freeze-commit wording in the lesson table (`round-29.md:84`). Name the five exposure
  disclosures, and name 207b and 207d as self-declared non-blind.
- Counter: run the blind check at `freeze_commit` using the script blob from the freeze commit (F5).
- Tool: land only what the judges rule `tool error`, case by case. Re-judge the draft that will actually land (the
  `fixclone` version, not the packet). Attach the full-output differential on all 86 case inputs, including the three
  `cases-a2.json` field changes, as the R4 receipt. Do not land the unbounded-scope cut without a ruling on the F6d
  input.

## Evidence files in my scratch directory
- `counterexample-unbounded-restart.txt`: base, judged-draft and newer-draft outputs on the F6d input.
- `variant-heading-run.txt` and `check-variant-heading.sh`: the F2 repair demonstration. This is a scratch copy only;
  the lane instrument was not edited.
- `tool-base.py`, `tool-fix.py`, `tool-fix2.py`, `cases*.json` and `c2funcs.py`: copies used for the self-tests,
  differentials and shape-membership replay. The shape cases are 207a×1, 207c×2, 210a×3 and 210c×3, and all nine fail
  under the base tool.
