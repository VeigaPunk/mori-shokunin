# ResidLessonBackfill — round-38 lesson: M16 row and Mistakes table vs committed evidence

Seat: `MoriR38.ResidLessonBackfill` (residual falsification re-check, one ordinary 8-seat batch).
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin` (only write scope).
Detection only: no product, corpus, lesson, receipt, or instrument edit was made; nothing committed.

Tip under attack: `b6993744171a05efc627b5e0664489c31aa5214e`.

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse mori
fatal: ambiguous argument 'mori': unknown revision or path not in the working tree.
$ git -C … rev-parse HEAD
b6993744171a05efc627b5e0664489c31aa5214e
$ git -C … log --oneline -1 --all --decorate
b699374 (HEAD, origin/master, origin/HEAD, master) round-38: instrument hardening …
```

There is no `mori` ref in this repo. The tip value was confirmed from `HEAD`/`master`/`origin/master`;
all bytes below were read with `git show b6993744:<path>`, and instrument hashes were recomputed from
those committed blobs (not from the worktree copies).

Audited artifact: `corpus/lessons/round-38.md` (89 lines at the tip), Gate at lines 3–26,
`## Mistakes` at line 28, rows M1–M16 at lines 32–47.

Path note: the assignment's `.ufo/waves/round-38/../../corpus/lessons/round-38.md` normalises to
`.ufo/corpus/lessons/round-38.md`, which does not exist at the tip. The committed lesson is
`corpus/lessons/round-38.md`; this audit targets that blob (verified `git cat-file -e`).

## Verdict

- (c) **16/16 pass.** Every leading class token is one of the nine classes in
  `corpus/evidence/sources-r36/S205.src:171-178`. The M12 relabel claim holds for all sixteen rows.
- (a) **All committed-path citations resolve**, with three caveats: M3 names the wrong receipt for
  its post-fix line; M15 cites a line that the fix itself rewrote; M9's cited fleet path is absent by
  design and its lane replacement is untracked (scratch), not in the tip tree.
- (b) **4 of 16 rows fail the exact-line test: M1, M3, M4, M5.** Two are material:
  - **M3**: the cited `evidence/gate-after.txt` does not contain `stale_supersede=[S069]`; that line
    is in `evidence/gate-after-e37dcc6.txt:2`. M3 also claims S073 landed "4,000+ path commits
    earlier" — measured distance is **31** path commits (227 all-history commits; 386 lane commits
    total).
  - **M5**: the row quotes `CONFORM_SELFTEST pass=2 fail=4`; its receipt's executed output is
    `CONFORM_SELFTEST pass=3 fail=3` (`evidence/m5-red.txt:10`), which is also what M16 quotes for
    the same receipt. The lesson contradicts itself.
  - **M4**: the committed receipt carries 6 of the 9 FAIL lines and no summary; the quoted
    "failed 9/9" line (`MORI_SOURCES_APPENDONLY_SELFTEST pass=0 fail=9`) exists only in the
    untracked scratch output, not in the committed receipt.
  - **M1**: the quoted `paths=[…]` list is not printed by any receipt; the actual line (committed and
    raw) begins with `'tools/mori-source-drift.py'`, which the quote silently dropped.
- M16's own row is **substantively backed**: RevS226Row's FAIL list matches (M1, M3–M6 not backed;
  M2 backed), all five red receipts exist, and the Gate locator now reads `S226.src:657-659`.
  The defects are in the rows M16 was meant to backfill, not in M16's description of what it did.

## Canonical vocabulary and (c) check

`corpus/evidence/sources-r36/S205.src:174-175` (inside the cited 171-178 block):

> `vacuous`, `survivor`, `stale-premise`, `reference-drift`, `number-drift`, `scope`,
> `attribution`, `landing`, `provider`

Leading token per row (all exact matches):

| Row | token | in vocab | Row | token | in vocab |
|---|---|---|---|---|---|
| M1 | reference-drift | yes | M9 | landing | yes |
| M2 | vacuous | yes | M10 | reference-drift | yes |
| M3 | number-drift | yes | M11 | scope | yes |
| M4 | scope | yes | M12 | attribution | yes |
| M5 | survivor | yes | M13 | survivor | yes |
| M6 | scope | yes | M14 | vacuous | yes |
| M7 | number-drift | yes | M15 | reference-drift | yes |
| M8 | landing | yes | M16 | vacuous | yes |

**M12 relabel claim: verified.** The pre-relabel labels quoted by `w2/RevLessonGate.md:14`
(`tooling`, `measurement`, `tooling`, `tooling`, `measurement`, `wave design` for M1–M6;
`transcription` for M7; `landing` for M8–M9) are all gone; every one of the sixteen labels at the
tip is `<vocabulary-token> (<detail>)`. M12's own statement that the audit ran against the scored
tip's M1–M6 plus the worktree's M7–M9 also matches RevLessonGate.

## Per-row audit

Legend: **PASS** = criterion met by committed bytes; **FAIL** = exact mismatch stated;
**PASS\*** = claim true/backed but not by a committed `evidence/` receipt (seat report, worktree, or
live run); **N/A** = cited path is the defect being removed.

| Row | (a) cited path at tip | (b) quoted red/green line in that receipt | (c) token | Exact mismatch |
|---|---|---|---|---|
| M1 | PASS `count-c4.py`, `evidence/c4-before.txt` | **FAIL** | PASS | Quoted `paths=['ufo/waves/round-37/evidence/c2-after.txt', 'evidence/drift-live-r37.txt']` is not literal in `evidence/m1-red.txt` or `evidence/c4-before.txt`; `m1-red.txt:5` prints `paths=['tools/mori-source-drift.py', 'ufo/waves/round-37/evidence/c2-after.txt', 'evidence/drift-live-r37.txt'] missing=[…]`. The quote drops the first element; the red phenomenon (dot stripped, phantom path missing) is present. Post-fix line `c4-before.txt:7` shows `.ufo/…` and only `evidence/drift-live-r37.txt` missing — correct. |
| M2 | PASS `fixtures/make-witness-sandbox.py`, `evidence/v3-token-control.txt`, `evidence/c4-witness.txt` | PASS | PASS | `v3-token-control.txt:12` `C2=met`; `c4-witness.txt:12` `C4=unmet`. |
| M3 | PASS (file exists) | **FAIL** | PASS | `stale_supersede=[S069]` is **not in `evidence/gate-after.txt`** (line 22 there is `… stale_supersede=[]`, run at `f725f30`). It is in `evidence/gate-after-e37dcc6.txt:2`. Pre-fix `stale_supersede=[]` at `e37dcc6` is backed by `evidence/m3-red.txt:5` (reconstruction). Separately, "S073 landed 4,000+ path commits earlier" is false: 31 path commits / 227 all-history commits / 386 lane commits (see Finding H2). |
| M4 | PASS* (no path in row; `evidence/m4-red.txt` exists via M16) | **FAIL** | PASS | Quoted "`--selftest` failed 9/9" is not in the committed receipt. `evidence/m4-red.txt` has six `FAIL … per-id line malformed: "P-C6: …"` lines (clean history, mutable-only edit, immutable edit, changed-back, deleted row, superseding row) and **no summary line**; the 9/9 output (`… pass=0 fail=9`, plus `supersede before edit`, `row reorder`, `whitespace padding`) exists only in untracked `scratch/red-receipts/m4-out.txt`. The abbreviated `per-id line malformed` fragment is present. |
| M5 | PASS* (no path in row; `evidence/m5-red.txt` exists via M16) | **FAIL** | PASS | Row quotes `CONFORM_SELFTEST pass=2 fail=4`. Committed receipt output is `CONFORM_SELFTEST pass=3 fail=3` (`m5-red.txt:10`); the `pass=2 fail=4` string occurs only in the receipt's provenance header (`m5-red.txt:1`, "observed pre-fix as …"), never as output. M16 quotes 3/3 for the same receipt — internal contradiction. |
| M6 | PASS* (no path in row; `evidence/m6-red.txt` exists via M16) | PASS* | PASS | Receipt prints `VALIDATOR_EXIT=1` and JSON `"code":"unknown_role","message":"items[0].role \"planner\" is not a swarm role"` (`m6-red.txt:3-4`). M16's `unknown_role: items[0].role "planner" is not a swarm role` is a compaction of two JSON fields, not a verbatim line (LOW). |
| M7 | PASS `evidence/gate-after.txt` | PASS (pointer off) | PASS | The quoted `supersede_timing superseded_as_of=[…18 ids…] stale_supersede=[]` is at `gate-after.txt:22`, not `:21`; `:21` is `appendonly_violations=18 … superseded=[18 ids]`. The SCORECARD claim-3 cell (`SCORECARD.md:2155`) is byte-equal to `gate-after.txt:22` (verified). The 3-id pre-fix cell is quoted in `w2/RevScorecardClaims.md:24,30-36`; the counter's `superseded=[S069,S182,S193]` is in `evidence/c1-before-rerun-summary.txt:6`. |
| M8 | PASS `dispatch-log.txt`, `w1/ExecIndexCleanLog.md`, `w2/RevIndexClean.md` | PASS | PASS | `dispatch-log.txt:6-9` discloses the four missing records; `:10-17` has four `landed`/`staged=0` pairs, each marked post-hoc. `ExecIndexCleanLog.md:3` and `RevIndexClean.md:3-7,23-27` independently report 4/5 unrecorded. |
| M9 | **N/A** cited fleet path absent; lane copy untracked | PASS* | PASS | `{fleet}/.ufo/waves/round-38/…` is gone (fleet `git status -uall` names no round-38 path); lane copy `.ufo/waves/round-38/scratch/RevC4Anchors/mori-source-drift-f725f30.py` exists in the worktree only (`??`), sha256 `453c5d8e…`, `cmp`-equal to `f725f30:tools/mori-source-drift.py`; `w2/RevMisroot.md:3-9,16-31` documents both. Not committed. |
| M10 | PASS `conform.py`, `evidence/c5-after-selftest.txt` | PASS* | PASS | Green: `c5-after-selftest.txt:8` `CONFORM_SELFTEST pass=6 fail=0`, command on `:1` is the runnable form. Red: the error string is in `w2/RevQualityRows.md:74`, not an `evidence/` receipt; QUALITY 111 (`corpus/QUALITY.md:898-903`) records it split. "requires the positional rev" is loose: `conform.py:266` is `nargs="?"`; the failure is `args.rev=None` reaching `selftest` at `:275`. |
| M11 | PASS `w2/CritGateSemantics.md`, `evidence/freeze-r38-v2.txt` | PASS | PASS | `CritGateSemantics.md:54-57` records both `merge-base --is-ancestor` directions exit 1; `:75` prints `supersede_timing superseded_as_of=[S001] stale_supersede=[]`. v2 pins the same contract blob `8cfeed27…` as v1/v3. |
| M12 | PASS `w2/RevLessonGate.md`, `sources-r36/S205.src:171-178`; `mistakes.md` resolves at fleet `.ufo/waves/kaika-w1/mistakes.md` | PASS | PASS | RevLessonGate.md:14: "7 of the 9 rows in the current worktree are off-vocabulary; all six rows present at the scored tip were off-vocabulary" and lists the old labels — matches the row. Relabel verified above. |
| M13 | PASS `w2/RevC5Bounds.md`, `count-c1.py`, `count-c4.py`, `evidence/m13-drain-unbounded.txt` | PASS | PASS | Receipt: `bounded_reads FAIL (… popen=False …)` at `:5`, `CONFORM=unmet` at `:8`, `EXIT=1` at `:9`. The pre-fix `CONFORM=met exit 0` is **not** in that receipt; it is in `RevC5Bounds.md:52-58` (F1; 4.51 s PoC at `:73`). The fix-cell sentence attributes it to the receipt; the row's evidence column does cite F1 (LOW). |
| M14 | PASS `w2/ScoutC4Bounds.md`, `w2/MutC4Anchor.md`, `w2/MutC4Live.md`, `w2/MutC4CapPath.md` | PASS* | PASS | Overclaims 1,2,7,8 are exactly `ScoutC4Bounds.md:22,24,37,39`; the three mutation reports each record KILLED (`MutC4Anchor.md:7`, `MutC4Live.md:128-134`, `MutC4CapPath.md:91`). The green detail `empty=0 unique=True` is not in a committed receipt (`evidence/c4-after.txt:9` predates it and prints `PASS (anchors=3 missing=[])`); the tip blob emits it (`count-c4.py:186`) and a live read-only run at `b6993744` printed `check anchors PASS (anchors=3 missing=[] empty=0 unique=True)`. |
| M15 | PASS `SCORECARD.md:2147`, `evidence/freeze-r38.txt`, `evidence/freeze-r38-v3.txt` | PASS (amended line) | PASS | At the tip `SCORECARD.md:2147` reads "pins in `evidence/freeze-r38.txt` (v1) and `evidence/freeze-r38-v3.txt` (final instrument bytes)"; the quoted pre-fix phrase survives as a prefix, but the original line was rewritten in place (no append-only note naming the old text). Pin values verified: v1 `4e59eeff…`/`5d416a1c…`, v2 `9ebf10a1…`/`3340d594…`, v3 `5aa51556…`/`8332341c…` = sha256 of the tip blobs. `RevC5Bounds.md:89-94` (F3) records the stale-pin defect. |
| M16 | PASS `w2/RevS226Row.md`, `evidence/m{1,3,4,5,6}-red.txt`, `evidence/c4-before.txt`, gate/c5 receipts | PASS* | PASS | RevS226Row.md:19-24 lists M1 and M3–M6 "Not backed" and M2 "Backed" — matches. Each named receipt exists and prints its documented red line, with the M4/M5 caveats above (those belong to M4/M5's rows; M16 quotes the 3/3 and `per-id line malformed` forms that the receipts do show). Gate locator: `S226.src:657-659`; the sentence spans 657–659 and is 24 words (≤25). |

## Findings by severity

### H1 — M3 cites the wrong receipt for its post-fix line (evidence path misdirected)

`corpus/lessons/round-38.md:34` says the post-fix reading is `stale_supersede=[S069]` "at `e37dcc6`
(`evidence/gate-after.txt`)". The committed `evidence/gate-after.txt` is a run at
`f725f307… --round-base f10a320d`; its timing line is
`supersede_timing superseded_as_of=[…18 ids…] stale_supersede=[]` (`:22`). The claimed line exists
in `evidence/gate-after-e37dcc6.txt:2`:

```
supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] stale_supersede=[S069]
```

`w2/RevS226Row.md:21` had already flagged this exact mis-citation; M16 added the correct receipt
but did not correct M3's pointer. This is a live `reference-drift` defect inside the lesson's
M3 row.

### H2 — M3's "4,000+ path commits" is false by two orders of magnitude

The row says S069 looked as-of "although S073 landed 4,000+ path commits earlier". The gate walks
`git log --format=%H --reverse REV -- corpus/SOURCES.md` (`tools/mori-sources-appendonly.py:220-221`)
and indexes that list. Measured at the tip:

```
$ git log --reverse --format=%H e37dcc6 -- corpus/SOURCES.md | wc -l        -> 51
  71abd41 (S073 landing)  = line 11 (1-based)
  62db24c (S069 edit)     = line 42
$ git rev-list --count 71abd41..62db24c -- corpus/SOURCES.md                -> 31
$ git rev-list --count 71abd41..62db24c                                     -> 227
$ git rev-list --count HEAD                                                 -> 386
$ git rev-list --count HEAD -- corpus/SOURCES.md                            -> 52
```

Distance in the gate's own index: **31**. Full-history distance: 227. Lane total: 386. No lane
quantity is 4,000+. This is a `number-drift` row carrying a drifted number; it should read 31 (or
"31 path commits / 227 commits").

### H3 — M5's quoted red line contradicts its own receipt (and M16)

`corpus/lessons/round-38.md:36` quotes `CONFORM_SELFTEST pass=2 fail=4`. `evidence/m5-red.txt:10`
records the executed run:

```
FAIL predicate      predicate whitespace-only change -> failing=[]
PASS head_pin       pin label renamed -> only head_pin failed
FAIL tool_resolve   semantic no-op mutation -> failing=[]
PASS bounded_reads  git helper run timeout removed -> only bounded_reads failed
FAIL timeout_state  semantic no-op mutation -> failing=[]
PASS scratch        scratch parent moved off-lane -> only scratch failed
CONFORM_SELFTEST pass=3 fail=3
```

The only `pass=2 fail=4` string in the receipt is its header (`m5-red.txt:1`, "observed pre-fix as
…"), not an output line; the raw run `scratch/red-receipts/m5-out.txt` also ends 3/3. M16 quotes
"`CONFORM_SELFTEST pass=3 fail=3`" for the same receipt. The M5 row and M16 therefore state
different red lines for one receipt; the executed evidence supports 3/3, so M5's 2/4 is the
unsupported one.

### M1 — committed M4 receipt is a truncated copy; the quoted "9/9" line is not in it

`corpus/lessons/round-38.md:35` quotes "`--selftest` failed 9/9 with `per-id line malformed: "P-C6:
…"`". `evidence/m4-red.txt` has exactly six FAIL lines and stops after `FAIL superseding row`; it
omits the case `supersede before edit`, `row reorder`, `whitespace padding`, and the summary
`MORI_SOURCES_APPENDONLY_SELFTEST pass=0 fail=9`. Those exist in the untracked
`scratch/red-receipts/m4-out.txt` (9 FAIL lines + summary). The committed-byte claim "9/9" is thus
not evidenced by committed bytes; a fresh clone sees 6/6-with-no-total. The receipt should include
the full output and the summary line.

### M2 — M1's quoted paths list is an edited line, not the printed line

`corpus/lessons/round-38.md:32` quotes
`paths=['ufo/waves/round-37/evidence/c2-after.txt', 'evidence/drift-live-r37.txt']`.
`evidence/m1-red.txt:5` (and the raw `m1-out.txt`) prints three elements:

```
paths=['tools/mori-source-drift.py', 'ufo/waves/round-37/evidence/c2-after.txt', 'evidence/drift-live-r37.txt'] missing=['ufo/waves/round-37/evidence/c2-after.txt', 'evidence/drift-live-r37.txt']
```

The quote drops the first element without an ellipsis; a reader checking the receipt finds a
different line. The substance (leading dot stripped, two paths missing) is correct and the post-fix
line (`c4-before.txt:7`) is correct, so the repair itself is backed; the red quote is not verbatim.

### L1 — M7's line pointer is off by one (`:21` vs `:22`)

`gate-after.txt` line 21 is `appendonly_violations=18 … superseded=[…] round_changed=[…]`; line 22
is the `supersede_timing superseded_as_of=[…] stale_supersede=[]` line the SCORECARD cell quotes and
is byte-equal to the cell. The row (and the appended claim-3 note at `SCORECARD.md:2185`) cite `:21`
for the 18-id `superseded_as_of` value.

### L2 — M13's pre-fix `CONFORM=met` is in the seat report, not the receipt

`evidence/m13-drain-unbounded.txt` documents only the fixed checker on the mutant (`:5` FAIL,
`:8` `CONFORM=unmet`, `:9` `EXIT=1`). The pre-fix `CONFORM=met, EXIT=0` is `RevC5Bounds.md:52-58`
(and F1 at `:62-73`). The row's evidence column cites F1, so the claim is backed; the fix sentence's
"the pre-fix checker prints … exit 0" reads as part of the receipt description and should name the
report instead.

### L3 — M14's green detail line has no committed receipt

`evidence/c4-after.txt:9` (run at `f725f30`) prints `check anchors PASS (anchors=3 missing=[])`;
the `empty=0 unique=True` detail was added later. The tip blob emits it (`count-c4.py:186`) and a
read-only run at `b6993744` printed exactly
`check anchors          PASS (anchors=3 missing=[] empty=0 unique=True)`.
The claim is true; the receipt trail is short one committed file (e.g. a `c4-after` at the final
tip).

### L4 — M10's red quote is seat-report-backed; the causal citation is loose

The quoted error `conformance setup error: expected str, bytes or os.PathLike object, not NoneType`
is in `w2/RevQualityRows.md:74`, not in an `evidence/` receipt; QUALITY 111
(`corpus/QUALITY.md:898-903`) records it in two pieces. Also `conform.py:266` declares
`rev` with `nargs="?"` and the `--selftest` branch returns at `:275` before the `:277` guard, so
"`--selftest` still requires the positional rev (`conform.py:266-270`)" describes the outcome, not
the code: the selftest simply does not run without a rev and the `None` reaches `evaluate`/`git`.
The green line (`c5-after-selftest.txt:8`, `pass=6 fail=0`, exit 0) is correctly receipted.

### L5 — M9's lane relocation is uncommitted; "the report's Misroot line" has no committed report

The lane copy is `?? .ufo/waves/round-38/scratch/RevC4Anchors/mori-source-drift-f725f30.py` (sha256
`453c5d8e260301df7a99daf62b4c16ea08e4a0b4f9e4f53821cdbce447011552`), `cmp`-equal to the `f725f30`
tool blob; the fleet copy is gone and fleet `git status -uall` names no round-38 path. But
`.ufo/waves/round-38/scratch/` has **zero** committed files at the tip, so a fresh clone cannot see
the copy. Also, no round-38 report file exists in the lane tree (106 round-38 files: specs, evidence,
`w1/`, `w2/`; no `report.md`), so M9's "recorded in the report's Misroot line" and the Round-shape
sentence "Seat deaths and the missing reports are listed in the round report" point at a file that
is not committed. (The seat report `w2/RevMisroot.md` does document the relocation.)

### L6 — M16's M6 quote is a compaction, not a verbatim line

M16 quotes `unknown_role: items[0].role "planner" is not a swarm role`, exit 1. The receipt
`m6-red.txt:4` is JSON: `{"schema":"ufo-swarm-wave-error-v1","code":"unknown_role","message":"items[0].role \"planner\" is not a swarm role"}`.
The content matches; the rendering is synthesized. Low severity, same abbreviated-quote convention
as M4.

### L7 — lesson seat total undercounts the round by 8

`corpus/lessons/round-38.md:57` says "Round total 108 seats, inside the 128 ceiling; the residual
re-check … rides one ordinary `task` call of 8 seats." `LOG.md:2231-2232` says "wave 1 at 65 seats
(13 reports), wave 2 at 43 seats (40 reports), residual re-check at 8 seats; round total 116."
65+43+8 = 116; the lesson's "Round total 108" is the w1+w2 subtotal, not the round total. Both
values are below the 128 ceiling, so the saturation conclusion is unchanged; the number is.

## What was checked and how

- Tip and refs: `rev-parse mori` (absent), `rev-parse HEAD`, `log --all --decorate`.
- Lesson: `git show b6993744:corpus/lessons/round-38.md`, parsed table cells programmatically;
  leading-token regex against the nine-class set; every row has 5 fields.
- (a): every backticked path token resolved with `git cat-file -e tip:<path>` against the lane root
  and `.ufo/waves/round-38/`; `{fleet}` and shorthand (`evidence/…`, `w1/…`, `w2/…`) resolved against
  their documented bases; `mistakes.md`/`CORPUS.md` resolved at the fleet root
  (`.ufo/waves/kaika-w1/mistakes.md`, `CORPUS.md`).
- (b): exact substring searches at the tip for every quoted red/green line, plus line-numbered reads
  of `m1-red.txt`, `m3-red.txt`, `m4-red.txt`, `m5-red.txt`, `m6-red.txt`, `m13-drain-unbounded.txt`,
  `c4-before.txt`, `c4-witness.txt`, `v3-token-control.txt`, `gate-after.txt`,
  `gate-after-e37dcc6.txt`, `dispatch-log.txt`, `c5-after-selftest.txt`, `freeze-r38*.txt`.
- Pin integrity: sha256 of `git show tip:.ufo/waves/round-38/{count-c1.py,count-c4.py,conform.py}`
  vs v1/v2/v3 pin files. Tip: `5aa51556…`, `8332341c…`, `580a0bf1…`; v3 matches all three.
- Vocabulary: `S205.src:171-178` read verbatim; fleet `mistakes.md:447-448` carries the same nine.
- One live read-only instrument run at the tip (`count-c4.py b6993744`) to test M14's green line;
  no mutant scripts were executed.

## Residual risk

1. **Committed receipts are not reproducible from committed bytes.** The `command:` lines in
   `m1/m3/m4/m5/m6-red.txt` reference `.ufo/waves/round-38/scratch/red-receipts/*.py`, and the tip
   tree has **zero** files under `.ufo/waves/round-38/scratch/` (they are untracked worktree files).
   A fresh-clone audit can verify the text but cannot re-run the one-spot mutations; M4 shows the
   concrete cost (the committed receipt is truncated).
2. **M3's green reading depends on a file the row does not name.** The only committed post-fix
   `stale_supersede=[S069]` at `e37dcc6` is `gate-after-e37dcc6.txt`; if a future sweep trusts the
   row's pointer, it reads `stale_supersede=[]` at a different revision and may reopen the finding.
3. **The P-C6 ancestry defect (M11) is routed, not fixed.** The gate still decides "descendant"
   from per-path log order (`tools/mori-sources-appendonly.py:272-289`); the diamond
   counterexample in `w2/CritGateSemantics.md` stands. Not re-tested here beyond reading the report.
4. **M15's pre-fix line was rewritten in place.** The append-only convention the SCORECARD uses for
   the axes and claim-3 corrections was not used here; only RevC5Bounds F3 preserves the old
   wording (as a paraphrase). The pin values themselves are consistent v1→v2→v3 and v3 matches the
   shipped bytes.
5. **No round report exists at the tip.** The lesson's "the round report" references (lines 24, 59)
   and M9's "report's Misroot line" are unverifiable in a fresh clone; the seat reports are the only
   committed accounts.

## Verification gaps

- No LSP device is mounted in this runtime (`xd://` exposes `ast_edit` and `debug` only); this is a
  markdown/receipt audit with no code symbols, so text/git checks were the applicable method. No
  empty LSP result was used as evidence of absence.
- I did not re-execute the untracked mutant reproducers or the append-only gate at `e37dcc6`; I read
  the committed receipts and cross-checked the raw untracked outputs where they exist.
- The "4,000+" figure was tested against every plausible lane quantity (path log 51/52, between-commit
  31, all-history 227, lane total 386) and the fleet total (2,069); no 4,000+ quantity was found. If
  the author measured something else, that measurement is not recorded in the round-38 evidence.
- I did not reopen the S226 URL; the captured `corpus/evidence/sources-r38/S226.src` at the tip is
  the evidence, and the Gate quote matches its lines 657–659 at 24 words.

## Tooling

No tool was installed or updated; no package manager was run (pacman paused host-wide). The audit
used git, coreutils, and python3 already present.

Report: .ufo/waves/round-38/resid/ResidLessonBackfill.md
