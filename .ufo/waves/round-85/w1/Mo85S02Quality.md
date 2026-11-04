# Mo85S02Quality — QUALITY criteria 173–175 and the SKILL registry row 19

Round 85 (attempt 1), wave w1. Seat `Mo85S02Quality` (scribe, leaf member — no subagent dispatch).
Lane `mori-shokunin`, worktree at `ab2608655ea52ba6d151b3a31d69a3b18cd2b41e` (the freeze commit),
entering revision `2cc4b1ae35a83e4fd3fc48bae842bdf38df2e80e`. Written 2026-11-04T08:07-03:00.
Nothing was committed; the L1 owns every lane commit.

## 1. Behavior

Appended only; no existing line was rewritten (QUALITY 4 and 25, and the seat's own rule):

- `corpus/QUALITY.md` — new heading `## Criteria added round 85 — a tally re-run at its cited bytes,
  an arm unarmed-first, a limit inside the receipt` and criteria **173**, **174**, **175**
  (`corpus/QUALITY.md:1933`, `:1935`, `:1970`, `:1999`). 89 insertions, 0 deletions.
- `SKILL.md` — one new table row, **registry row 19** (`SKILL.md:1371`), appended after row 18 at
  the file end. 1 insertion, 0 deletions. Every earlier line is byte-identical, including the
  `SKILL.md:905` selftest-tally pin (still `| source drift (r37) | probe | ...`) and row 18
  (`SKILL.md:1370`).

Diff proof (append-only, measured):

```
$ git diff --stat -- SKILL.md corpus/QUALITY.md
 SKILL.md          |  1 +
 corpus/QUALITY.md | 89 +++++++++++++++++++++++++++++++++++++++++++++++++++++++
 2 files changed, 90 insertions(+)
$ git diff -U0 -- SKILL.md corpus/QUALITY.md | grep -E '^@@|^-[^-]'
@@ -1370,0 +1371 @@ L0 governs.
@@ -1931,0 +1932,89 @@ adjudication of each hit is recorded in `corpus/lessons/round-29.md`. The check
```

No `-` line appears: both hunks are pure insertions.

Post-append digests: `corpus/QUALITY.md` sha256 `bc4d3eb9b955d90d709f6107a519bafc8bd324c600e22f65529f43580bfd6661`,
`SKILL.md` sha256 `ee28e87d620c38c3b8629f4572456ae06e548eae3ca08de3a12fb8eacbef0431`.

One correction to my own new row before yield (no earlier line touched; the diff is still
`1 insertion`): the row's input-scope clause first read "all three read only
`.ufo/waves/round-85/`", which the counters' own constants refute — C1 grades
`.ufo/waves/round-84/count-c1.py` (`count-c1.py:33`), C2 reads the three round-85 receipts
(`count-c2.py:32-39`), and C3 reads `tools/mori-census.sh`, the r10 baseline, the r82 snapshot,
the r82 classification and `.ufo/waves/round-83/count-c2.py` (`count-c3.py:36-40`). The row now
names that measured set.

## 2. The three criteria, and the evidence each carries

**173 — a quoted tally is re-run at the cited bytes; a pointer is re-located at write time.**
Supersedes D84-2's subject (criterion 172's `C1_COUNTER_SELFTEST pass=11 fail=0` and its
`:296-300` pointer) by appending, per the file's own append-only rule; criterion 172's bytes are
untouched. My measurements (lane root, `python3 -I` over `git show` byte images):

```
$ git show dbdb1aaa:.ufo/waves/round-84/count-c1.py  > $S/c1-at-dbdb1aaa.py
$ python3 -I $S/c1-at-dbdb1aaa.py --selftest | tail -1
C1_COUNTER_SELFTEST pass=11 fail=0        (rc 0)
$ git show 5a231ef8:.ufo/waves/round-84/count-c1.py > $S/c1-at-5a231ef8.py
$ sha256sum $S/c1-at-5a231ef8.py
da31c59958329a3e0b26f8b7d1633de9755af3940a5900b4270f9f61e979e240
$ python3 -I $S/c1-at-5a231ef8.py --selftest | tail -1
C1_COUNTER_SELFTEST pass=15 fail=0        (rc 0)
$ git show 5a231ef8:.ufo/waves/round-84/count-c1.py | grep -c 'cases.append(('
15
$ git show 5a231ef8:.ufo/waves/round-84/count-c1.py | awk 'NR>=296 && NR<=300'
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    base = a.scratch or os.environ.get("HYAKU_SCRATCH") or tempfile.gettempdir()
    os.makedirs(base, exist_ok=True)
    scratch = tempfile.mkdtemp(prefix="count-c1-r84-", dir=base)
```

So the quote was true of the pre-arm bytes and is false of the bytes the criterion's pointer
resolves to; and `:296-300` is argument parsing, not the detector gate. Re-located by
`grep -n` on the same bytes: `selfcheck()` `:174`, tally print `:286`, detector gate `:328-345`.

The delivered instrument does not already police this text (measured):

```
$ TMPDIR=$S/tmp python3 -I tools/mori-claim-sweep.py --root . --carriers corpus/QUALITY.md
CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 stale=0 carriers=1 pointers=0      (rc 0)
```

`tools/mori-claim-sweep.py`'s default carriers are `SCORECARD.md,SKILL.md,SHONEN.md,LOG.md`
(`:33`) and its `stale_literals` are a pinned string list (`:150-156,178`), not a re-run. The
stale text sits at `corpus/QUALITY.md:1916`.

**174 — the arm is run against the unarmed subject first; a fixture that fails pristine is not a
kill.** Ground is QUALITY 165 plus the A4/Sc02 D3 class. Sibling measurement cited as such (not
mine): `.ufo/waves/round-84/w1/Mo84Sc02Clauses.md:444-466` — the literal `killed=0` assertion read
`FAIL blind_case_tally mutants=2 killed=1 equivalent=0 survivors=1 total=2 pristine=green`,
`C1_COUNTER_SELFTEST pass=7 fail=1` on the pristine counter, while the r84 counter over that same
variant still printed both mutant lines `killed` beside `EXTRA pristine-red ... ['C1_COUNTER_SELFTEST
pass=7 fail=1']` and `C1=unmet ... pristine=red`, and the acceptance bar at
`.ufo/waves/round-84/w1/Mo84R01C1.md:214,219-221` rejects that variant as a fake kill.
My own measurement (scratch copy of the r85 counter, one arm's expected tally flipped from
`killed == 1` to `killed == 0`; no lane byte touched):

```
$ python3 -I $S/c1-defective-arm.py --selftest
FAIL killed_counted mutants=1 killed=1 survivors=0 total=1 arms=-1
C1_COUNTER_SELFTEST pass=17 fail=1        (rc 1)
```

The unarmed counter is red while that same tail still counts its mutant killed — the fixture, not
discrimination, explains the red. The lane's whole-subject pristine gate
(`.ufo/waves/round-85/count-c1.py:120,140-141,167`, arm `red_pristine_reported` `:271-272`) blocks
`met` but cannot attribute the defect to one arm; 174 adds the per-arm-first order.

**175 — the limit travels inside the receipt.** Ground: D84-4 and D84-5, and this round's frozen
P-C2 grammar. Measured by me:

```
$ grep -c '^# *limits:' .ufo/waves/round-84/evidence/after-r84.txt
0
$ sed -n '1p' .ufo/waves/round-84/evidence/after-r84.txt
# round-84 after measurements — measured 2026-11-04T10:17:36Z at revision da7631f4a44aaa6d7c1c822308df4d265fb8d7da (worktree == that revision for the graded carriers)
$ grep -l '^# limits:' .ufo/waves/round-84/evidence/*        # five receipts present -> no file
$ for f in .ufo/waves/round-84/evidence/*; do printf "%s cmd=%s rev=%s sha=%s limits=%s\n" \
    "$(basename $f)" "$(grep -c '^# *cmd:' $f)" "$(grep -c '^# *rev:' $f)" \
    "$(grep -c 'sha256' $f)" "$(grep -c '^# *limits:' $f)"; done
after-r84.txt cmd=0 rev=0 sha=0 limits=0
battery-r84.txt cmd=0 rev=0 sha=2 limits=0
controls-r84-defeated.txt cmd=0 rev=0 sha=0 limits=0
controls-r84.txt cmd=0 rev=0 sha=0 limits=0
controls-verify-r84.txt cmd=0 rev=0 sha=0 limits=0
```

The frozen counter's own rule (`weak-limits` when the text lacks `limit` or has fewer than three
words) is implemented at `.ufo/waves/round-85/count-c2.py:41-45,56-109,107-109`; the receipts are
written by `.ufo/waves/round-85/make-receipts.sh <rev> [--repo DIR]` (round item `Mo85E02Receipts`).

## 3. Arm counts cited by this report — RUN, not copied

Run from the lane root with scratch pinned (`HYAKU_SCRATCH` and `TMPDIR` under my scratch dir, so
the counters do not fall back to `/tmp`), full stdout:

```
### python3 -I .ufo/waves/round-85/count-c1.py --selftest
PASS killed_counted mutants=1 killed=1 survivors=0 total=1 arms=-1
PASS survivor_counted mutants=1 killed=0 survivors=1 total=1 arms=-1
PASS arms_parse 17/0
PASS arms_floor 15 arms
PASS arms_requires_labels no labels
PASS arms_green 17 arms
PASS green_boundary green()
PASS killed_boundary killed()
PASS unanchored_excluded mutants=0 killed=0 survivors=0 total=0 arms=-1
PASS empty_mutation_unmet mutants=0 killed=0 survivors=0 total=0 arms=-1
PASS red_pristine_reported mutants=1 killed=1 survivors=0 total=1 arms=-1
PASS target_split_ok 2/0/2 arms=17
PASS target_split_free 1/1/2
PASS r84_target_ok r84 met
PASS r84_target_free 3/1/4
PASS subject_markers_ok all
PASS subject_markers_missing one
PASS marker_literal X1 label
C1_COUNTER_SELFTEST pass=18 fail=0
rc=0
### python3 -I .ufo/waves/round-85/count-c2.py --selftest
PASS headers_ok []
PASS body_after_separator body
PASS missing_binding no sha
PASS duplicate_cmd 2 cmds
PASS bad_rev bad
PASS weak_limits weak
PASS missing_separator none
PASS binding_verifies []
PASS stale_sha_mismatch ['sha:tools/x.py']
PASS unsafe_path ['unsafe-path:../x.py']
PASS safe_path path
PASS ancestor_equal equal
PASS hex_shape hex
PASS receipt_count 3
PASS marker_literal marker
C2_COUNTER_SELFTEST pass=15 fail=0
rc=0
### python3 -I .ufo/waves/round-85/count-c3.py --selftest
PASS derive_surface_known known
PASS derive_surface_new new
PASS derive_finding finding
PASS derive_key key
PASS derive_unknown_key non-key shape
PASS derive_table_word verdict
PASS delta_pairs [('+memory.peak', 'agreed'), ('B', 'absent-live'), ('C', 'added-live')]
PASS delta_class_changed [('SURFACE:z', 'class-changed:value-changed->added-since-r10')]
PASS delta_dedupe [('+memory.peak', 'agreed')]
PASS snapshot_parse last line
PASS classifications {'A': 'value-changed'} 1 1
PASS subject_signal {'live': 'derived', 'live_tokens': '64', 'deltas': '1'}
PASS reconcile_mismatch 1 1
PASS reconcile_clean clean
PASS reconcile_unnamed unnamed
PASS class_words words
PASS class_word_bogus bogus
PASS observations 3
PASS marker_literal marker
C3_COUNTER_SELFTEST pass=19 fail=0
rc=0
```

The row's self-test cell states exactly these three tallies (18/15/19) at
`ab260865`; the three worktree counters are byte-identical to the freeze commit
(`da5fb27b…`/`b7a4e691…`/`c035e32f…` at both), so "freeze bytes" is the worktree. The r84
counter's own subject tally at the same worktree is 15 (`grep -c 'cases.append(('`), which is what
the C1 counter's 17-arm floor refuses (`PASS arms_floor 15 arms`).

## 4. Findings

1. **The SKILL row's generator path does not exist yet.** `.ufo/waves/round-85/make-receipts.sh` is
   absent at write time (other seat's item, `Mo85E02Receipts`). The row names it as the round's
   receipt generator inside the self-test/pinned-values cells; the row's **entry** cell (the three
   counters) does resolve at `ab260865`, so the registry row is not dangling for its gate entry.
   Reported, not repaired — writing another seat's file is out of my scope.
2. **The target `arms=17` in P-C1 is the subject's arm count, the counters' own selftest arms are
   18/15/19.** No contradiction, but a reader comparing "arms=17" with "pass=18" needs the
   distinction; the row spells the three counter tallies out.
3. **QUALITY 172 retains its stale quote** (`corpus/QUALITY.md:1916`, `pass=11`). 173 supersedes it
   as an appended row; editing 172 would violate the file's own criteria 4/25. The lane's `SKILL.md`
   row 18 already cites 15, so the file is internally inconsistent until a reader applies 173.
4. **The claim sweep does not cover criterion prose** (measured in §2). A reader of
   `CLAIM_SWEEP ... stale=0` must not read it as "no stale quoted tally anywhere in the corpus".
5. **The r84 receipts carry the D84-4/D84-5 shape in full**: no `# cmd:`, no `# rev:`, no `# limits:`
   in any of the five; only `battery-r84.txt` mentions `sha256` (twice, not as a header line).

## 5. Not executed by this seat (limits of this report)

- I ran **only** `--selftest` modes of the three r85 counters. I did not run
  `count-c1.py <rev>`, `count-c2.py <rev>` or `count-c3.py <rev>`; the after-value of P-C1/P-C2/P-C3
  at the integration revision is the L1's measurement, not mine.
- I did not run `make-receipts.sh` (absent) and generated no receipt; the C2 real-mode target is
  unverified here.
- I did not edit the counters, `contract.md`, `SCORECARD.md`, `SHONEN.md`, `LOG.md`, or any
  `.ufo/state/` path, and wrote no report outside `.ufo/waves/round-85/w1/`.
- The D3 measurement in QUALITY 174 is a sibling's (`Mo84Sc02Clauses`); it is cited as such. The
  defective-arm probe I report as mine was run on a scratch copy only.

## 6. Tooling

No tool was installed or upgraded; no `pacman` transaction of any kind; no `~/.local/bin` or PATH
write. Scratch: `/fast/scratch/hyaku/mori-r85/Mo85S02Quality` (deleted before yield).

## 7. Artifact paths

- `corpus/QUALITY.md` (appended 173–175; sha256 `bc4d3eb9…`)
- `SKILL.md` (appended registry row 19; sha256 `047d97ef…`)
- this report, `.ufo/waves/round-85/w1/Mo85S02Quality.md`
