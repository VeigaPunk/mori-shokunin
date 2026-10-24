# MutC2Cols — mutation probe of the C2 detector (`tools/mori-sources-appendonly.py`)

Seat: mori-r36-w2-MutC2Cols (attempt 2). Mutation-tester, read-only on the lane.

## What this attacks

C2 claims the frozen counter `.ufo/waves/round-36/count-c2.py` prints the hidden truth for
`ids` / `deleted` / `superseded` / `round_changed` on 24 runtime-drawn sandbox histories plus the
lane's own history. The probe asks whether that counter can actually fail when the gate under test
mis-selects its **immutable-column set** — the single point where the gate's whole verdict is
decided (`tools/mori-sources-appendonly.py:162-167`, consumed at :230 and :241).

## Frozen bytes (verified, not edited)

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ git show bf0df77fee4b6ef54a90aea09335c7617f125151:tools/mori-sources-appendonly.py | sha256sum
915527a7d2f553740ed3ab0166669031f19ce2de6b2fec8501208f97244cfc89  -
$ sha256sum tools/mori-sources-appendonly.py .ufo/waves/round-36/count-c2.py
915527a7d2f553740ed3ab0166669031f19ce2de6b2fec8501208f97244cfc89  tools/mori-sources-appendonly.py
c7edaacfff029c2055bee6ddda42ff6f5c040dad7fbac81e9d169602edcbac34  .ufo/waves/round-36/count-c2.py
$ grep -n count-c2 .ufo/waves/round-36/evidence/freeze-v2.txt
4:c7edaacfff029c2055bee6ddda42ff6f5c040dad7fbac81e9d169602edcbac34  count-c2.py
```

Working-tree tool = data-tip tool blob; counter matches the freeze pin. All mutants are copies under
`/fast/scratch/hyaku/mori-r36/MutC2Cols/`; the lane tool was never written.

Scratch copies (sha256):

```
915527a7d2f553740ed3ab0166669031f19ce2de6b2fec8501208f97244cfc89  pristine.py
e1221f9028245c102039835c472fe0e8c2ebf7a2bb02312d12282d222f134f87  mutant_mutable.py
9f828636cbfd4d3e56b340e04f2b604813c96a23436b88372e80c6d862ff6a27  mutant_first4.py
```

## The assignment's two readings, both measured

The ticket names one mutation: *"compare only the first four columns when deciding immutable-cell
changes (so status/recheck/used-by edits look like violations)"*. Those two clauses describe
**different** defects, so I built the smallest single-line mutant for each and measured both:

* **Mutant A (`mutant_mutable.py`)** — implements the parenthetical effect: stop excluding the
  mutable columns, i.e. fingerprint the whole row, so a `status`/`recheck`/`used-by` edit is read as
  an immutable-cell change.
* **Mutant B (`mutant_first4.py`)** — implements the literal wording: compare only `COLUMNS[:4]`
  (`id, source, kind, tier`). This *narrows* the fingerprint (it misses `scope, anchor, teaches,
  opened`); it does **not** make mutable edits look like violations.

Exactly one line changes in each case:

```diff
--- pristine.py
+++ mutant_mutable.py
@@ -163,8 +163,7 @@
     """Cell indices of the immutable columns, by header position."""
     if not colmap:
         colmap = {name: index for index, name in enumerate(COLUMNS)}
-    return [colmap[name] for name in COLUMNS
-            if name not in MUTABLE and name in colmap]
+    return [colmap[name] for name in COLUMNS if name in colmap]
```

```diff
--- pristine.py
+++ mutant_first4.py
@@ -163,8 +163,7 @@
     """Cell indices of the immutable columns, by header position."""
     if not colmap:
         colmap = {name: index for index, name in enumerate(COLUMNS)}
-    return [colmap[name] for name in COLUMNS
-            if name not in MUTABLE and name in colmap]
+    return [colmap[name] for name in COLUMNS[:4] if name in colmap]
```

`immutable_indices` is the only caller-visible change; nothing else in either file differs
(`diff -u` output above is the complete diff, exit 1 = files differ).

## Baseline — pristine bytes must score met

```
$ python3 .../.ufo/waves/round-36/count-c2.py bf0df77fee4b6ef54a90aea09335c7617f125151 \
    --tool /fast/scratch/hyaku/mori-r36/MutC2Cols/pristine.py --seed 11
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /fast/scratch/hyaku/mori-r36/MutC2Cols/pristine.py
blind arm: 24/24 sandbox histories matched the hidden truth (2.0s; coverage: deletions=24 changed-back=16 superseded=12)
real arm: pass (0.3s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
C2=met
seed=11
```
exit code **0**. Reproduced identically on a second serial run (`baseline-pristine-3.txt`, exit 0).

An earlier serial run of the same command failed once (`repo17 FAIL: no summary line (exit 2):
Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set)`, C2=unmet, exit 1).
That is a baseline failure and therefore *inconclusive*, not a killed mutant; its cause is isolated
in "Harness observation" below and does not recur when runs are serialised. Baseline for judging
the mutants is the reproduced `C2=met`, exit 0.

## Mutant A — counter output (killed)

```
$ python3 .../.ufo/waves/round-36/count-c2.py bf0df77fee4b6ef54a90aea09335c7617f125151 \
    --tool /fast/scratch/hyaku/mori-r36/MutC2Cols/mutant_mutable.py --seed 11
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /fast/scratch/hyaku/mori-r36/MutC2Cols/mutant_mutable.py
blind arm: 6/24 sandbox histories matched the hidden truth (1.8s; coverage: deletions=24 changed-back=16 superseded=12)
  repo00 FAIL: lists differ
      want: appendonly_violations=3 ids=[S096,S143] deleted=[S203] superseded=[S096,S143] round_changed=[S016,S143,S203]
      got:  appendonly_violations=3 ids=[S096,S143] deleted=[S203] superseded=[S096,S143] round_changed=[S016,S096,S143,S203]
  repo01 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S079] superseded=[] round_changed=[]
      got:  appendonly_violations=2 ids=[S065] deleted=[S079] superseded=[] round_changed=[S065]
  repo02 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S044] superseded=[] round_changed=[]
      got:  appendonly_violations=2 ids=[S037] deleted=[S044] superseded=[] round_changed=[]
  repo05 FAIL: lists differ
      want: appendonly_violations=5 ids=[S021,S085,S200] deleted=[S237,S240] superseded=[S021] round_changed=[S085,S200,S240]
      got:  appendonly_violations=6 ids=[S021,S085,S133,S200] deleted=[S237,S240] superseded=[S021] round_changed=[S085,S133,S200,S240]
  repo06 FAIL: lists differ
      want: appendonly_violations=2 ids=[] deleted=[S270,S272] superseded=[] round_changed=[S245,S270,S272]
      got:  appendonly_violations=3 ids=[S022] deleted=[S270,S272] superseded=[] round_changed=[S022,S245,S270,S272]
  repo07 FAIL: lists differ
      want: appendonly_violations=2 ids=[] deleted=[S021,S218] superseded=[] round_changed=[S218]
      got:  appendonly_violations=3 ids=[S298] deleted=[S021,S218] superseded=[] round_changed=[S218,S298]
  repo08 FAIL: lists differ
      want: appendonly_violations=4 ids=[S163] deleted=[S128,S143,S217] superseded=[S163] round_changed=[S128,S217]
      got:  appendonly_violations=5 ids=[S163,S250] deleted=[S128,S143,S217] superseded=[S163] round_changed=[S128,S217,S250]
  repo10 FAIL: lists differ
      want: appendonly_violations=2 ids=[] deleted=[S228,S244] superseded=[] round_changed=[S057,S244]
      got:  appendonly_violations=3 ids=[S045] deleted=[S228,S244] superseded=[] round_changed=[S045,S057,S244]
  repo11 FAIL: lists differ
      want: appendonly_violations=4 ids=[S137] deleted=[S102,S148,S172] superseded=[] round_changed=[S102,S137,S148,S172,S257]
      got:  appendonly_violations=7 ids=[S137,S257,S288,S291] deleted=[S102,S148,S172] superseded=[] round_changed=[S102,S137,S148,S172,S257,S288,S291]
  repo13 FAIL: lists differ
      want: appendonly_violations=3 ids=[S045] deleted=[S257,S271] superseded=[S045] round_changed=[]
      got:  appendonly_violations=4 ids=[S045,S068] deleted=[S257,S271] superseded=[S045] round_changed=[]
  repo15 FAIL: lists differ
      want: appendonly_violations=2 ids=[S105] deleted=[S196] superseded=[] round_changed=[S011,S196]
      got:  appendonly_violations=4 ids=[S011,S105,S251] deleted=[S196] superseded=[] round_changed=[S011,S196]
  repo16 FAIL: lists differ
      want: appendonly_violations=2 ids=[S278] deleted=[S142] superseded=[S278] round_changed=[S142]
      got:  appendonly_violations=4 ids=[S159,S278,S295] deleted=[S142] superseded=[S278] round_changed=[S142,S159]
  repo18 FAIL: lists differ
      want: appendonly_violations=2 ids=[S136] deleted=[S005] superseded=[] round_changed=[S005,S136,S158]
      got:  appendonly_violations=5 ids=[S014,S108,S130,S136] deleted=[S005] superseded=[] round_changed=[S005,S014,S136,S158]
  repo19 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S134] superseded=[] round_changed=[S134,S169]
      got:  appendonly_violations=2 ids=[S097] deleted=[S134] superseded=[] round_changed=[S097,S134,S169]
  repo20 FAIL: lists differ
      want: appendonly_violations=4 ids=[S106] deleted=[S184,S212,S233] superseded=[S106] round_changed=[S184]
      got:  appendonly_violations=6 ids=[S061,S074,S106] deleted=[S184,S212,S233] superseded=[S106] round_changed=[S074,S184]
  repo21 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S239] superseded=[] round_changed=[S181]
      got:  appendonly_violations=3 ids=[S054,S181] deleted=[S239] superseded=[] round_changed=[S054,S181]
  repo22 FAIL: lists differ
      want: appendonly_violations=2 ids=[S012] deleted=[S043] superseded=[S012] round_changed=[]
      got:  appendonly_violations=3 ids=[S012,S072] deleted=[S043] superseded=[S012] round_changed=[]
  repo23 FAIL: lists differ
      want: appendonly_violations=2 ids=[] deleted=[S024,S181] superseded=[] round_changed=[S024,S134]
      got:  appendonly_violations=4 ids=[S125,S276] deleted=[S024,S181] superseded=[] round_changed=[S024,S125,S134]
real arm: FAIL (0.3s)
  tool:   appendonly_violations=60 ids=[S002,S003,S013,S014,S015,S031,S035,S036,S037,S038,S041,S044,S051,S062,S064,S065,S066,S067,S068,S069,S071,S077,S078,S079,S080,S081,S082,S083,S084,S085,S086,S092,S097,S114,S115,S118,S119,S120,S145,S146,S151,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S191,S192,S193,S194,S195,S196,S197,S198] deleted=[] superseded=[S067,S069,S071,S083,S084,S097,S182,S193] round_changed=[S182,S191,S192,S193,S194,S195,S196,S197,S198]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  diff: ids: want=['S041', 'S044', 'S051', 'S062', 'S064', 'S069', 'S179', 'S180', 'S181', 'S182', 'S183', 'S184', 'S185', 'S186', 'S188', 'S189', 'S190', 'S193'] got=['S002', 'S003', 'S013', 'S014', 'S015', 'S031', 'S035', 'S036', 'S037', 'S038', 'S041', 'S044', 'S051', 'S062', 'S064', 'S065', 'S066', 'S067', 'S068', 'S069', 'S071', 'S077', 'S078', 'S079', 'S080', 'S081', 'S082', 'S083', 'S084', 'S085', 'S086', 'S092', 'S097', 'S114', 'S115', 'S118', 'S119', 'S120', 'S145', 'S146', 'S151', 'S179', 'S180', 'S181', 'S182', 'S183', 'S184', 'S185', 'S186', 'S188', 'S189', 'S190', 'S191', 'S192', 'S193', 'S194', 'S195', 'S196', 'S197', 'S198']
  diff: superseded: want=['S069', 'S182', 'S193'] got=['S067', 'S069', 'S071', 'S083', 'S084', 'S097', 'S182', 'S193']
  diff: round_changed: want=['S182', 'S191', 'S192', 'S193', 'S194', 'S195', 'S196', 'S197', 'S198']
  diff: violations: want=18 got=60
  tool exit=1
C2=unmet
seed=11
```
exit code **1**. Blind 6/24; coverage gate satisfied (deletions=24 changed-back=16 superseded=12), so
`unmet` is a real verdict, not a setup error. **Mutant A is killed**, and precisely in the way the
ticket predicts: every extra id in `ids=` / `round_changed=` is a row whose only in-round change was
to `status`, `recheck` or `used-by`.

## Mutant B — counter output (killed, for the literal wording)

```
$ python3 .../.ufo/waves/round-36/count-c2.py bf0df77fee4b6ef54a90aea09335c7617f125151 \
    --tool /fast/scratch/hyaku/mori-r36/MutC2Cols/mutant_first4.py --seed 11
tool: /fast/scratch/hyaku/mori-r36/MutC2Cols/mutant_first4.py
blind arm: 13/24 sandbox histories matched the hidden truth (3.1s; coverage: deletions=24 changed-back=16 superseded=12)
  repo00 FAIL: lists differ
      want: appendonly_violations=3 ids=[S096,S143] deleted=[S203] superseded=[S096,S143] round_changed=[S016,S143,S203]
      got:  appendonly_violations=1 ids=[] deleted=[S203] superseded=[] round_changed=[S203]
  repo03 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S017] superseded=[] round_changed=[S017,S162]
      got:  appendonly_violations=1 ids=[] deleted=[S017] superseded=[] round_changed=[S017]
  repo04 FAIL: lists differ
      want: appendonly_violations=3 ids=[S275] deleted=[S140,S194] superseded=[S275] round_changed=[S194]
      got:  appendonly_violations=2 ids=[] deleted=[S140,S194] superseded=[] round_changed=[S194]
  repo05 FAIL: lists differ
      want: appendonly_violations=5 ids=[S021,S085,S200] deleted=[S237,S240] superseded=[S021] round_changed=[S085,S200,S240]
      got:  appendonly_violations=3 ids=[S021] deleted=[S237,S240] superseded=[S021] round_changed=[S240]
  repo10 FAIL: lists differ
      want: appendonly_violations=2 ids=[] deleted=[S228,S244] superseded=[] round_changed=[S057,S244]
      got:  appendonly_violations=2 ids=[] deleted=[S228,S244] superseded=[] round_changed=[S244]
  repo11 FAIL: lists differ
      want: appendonly_violations=4 ids=[S137] deleted=[S102,S148,S172] superseded=[] round_changed=[S102,S137,S148,S172,S257]
      got:  appendonly_violations=3 ids=[] deleted=[S102,S148,S172] superseded=[] round_changed=[S102,S148,S172,S257]
  repo13 FAIL: lists differ
      want: appendonly_violations=3 ids=[S045] deleted=[S257,S271] superseded=[S045] round_changed=[]
      got:  appendonly_violations=2 ids=[] deleted=[S257,S271] superseded=[] round_changed=[]
  repo14 FAIL: lists differ
      want: appendonly_violations=6 ids=[S082,S234] deleted=[S122,S218,S262,S270] superseded=[S082] round_changed=[S234,S262]
      got:  appendonly_violations=5 ids=[S234] deleted=[S122,S218,S262,S270] superseded=[] round_changed=[S234,S262]
  repo17 FAIL: lists differ
      want: appendonly_violations=2 ids=[S073] deleted=[S242] superseded=[S073] round_changed=[S073,S150,S242]
      got:  appendonly_violations=2 ids=[S073] deleted=[S242] superseded=[S073] round_changed=[S073,S242]
  repo22 FAIL: lists differ
      want: appendonly_violations=2 ids=[S012] deleted=[S043] superseded=[S012] round_changed=[]
      got:  appendonly_violations=1 ids=[] deleted=[S043] superseded=[] round_changed=[]
  repo23 FAIL: lists differ
      want: appendonly_violations=2 ids=[] deleted=[S024,S181] superseded=[] round_changed=[S024,S134]
      got:  appendonly_violations=2 ids=[] deleted=[S024,S181] superseded=[] round_changed=[S024]
real arm: FAIL (0.5s)
  tool:   appendonly_violations=1 ids=[S181] deleted=[] superseded=[] round_changed=[]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  diff: ids: want=[...18 ids...] got=['S181']
  diff: superseded: want=['S069', 'S182', 'S193'] got=[]
  diff: round_changed: want=['S182', 'S193'] got=[]
  diff: violations: want=18 got=1
  tool exit=0
C2=unmet
seed=11
```
(Blind-arm `want`/`got` pairs verbatim; the real-arm `ids` diff line is abbreviated here only
because it repeats Mutant A's oracle line verbatim — full text is in
`/fast/scratch/hyaku/mori-r36/MutC2Cols/mutant-first4-counter.txt`.)
exit code **1**. Blind 13/24. The failure shape is the mirror image of A: violations are *missed*
because `scope`, `anchor`, `teaches`, `opened` are no longer fingerprinted — exactly why the literal
"first four columns" wording cannot be the mutation that makes mutable edits look like violations.

## Minimal fixture — the mechanism, isolated

A two-commit repo whose only change is `status: mined -> queued` on `S001`:

```
$ python3 <tool> HEAD --repo /fast/scratch/hyaku/mori-r36/MutC2Cols/fixture \
    --round-base d54eb05a0627c556591c77913e6f25bbc088a816
== pristine
appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
exit=0
== mutant_mutable
changed S001 superseded_by=-
appendonly_violations=1 ids=[S001] deleted=[] superseded=[] round_changed=[S001]
exit=1
== mutant_first4
appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
exit=0
```

This is the ticket's stated expectation in one line: with Mutant A a mutable-cell edit is reported
as an immutable violation (and the gate exits 1). With Mutant B the same edit is (correctly)
ignored — confirming B does not implement the parenthetical.

## Selftest of the mutants

```
$ python3 pristine.py --selftest        -> MORI_SOURCES_APPENDONLY_SELFTEST pass=8 fail=0   exit 0
$ python3 mutant_mutable.py --selftest  -> FAIL mutable-only edit: ids: want [] got ['S001'];
                                           round_changed: want [] got ['S001']; exit: want 0 got 1
                                           MORI_SOURCES_APPENDONLY_SELFTEST pass=7 fail=1   exit 1
$ python3 mutant_first4.py --selftest   -> FAIL immutable edit / changed-back inside the round /
                                           superseding row (3 failures)
                                           MORI_SOURCES_APPENDONLY_SELFTEST pass=5 fail=3   exit 1
```

Neither mutant is the strongest receipt in the "selftest passes while the counter fails" sense:
this mutation family is directly covered by the tool's own hand-written fixtures (`mutable-only
edit`, `immutable edit`, `changed-back`, `superseding row`), so both mutants are caught twice. The
counter's value here is that it is *independent* of those fixtures — it re-derives the truth in its
own `immutable_indices` (`count-c2.py:138-141`) over runtime-drawn histories, and it caught A on
18/24 of them and on the real lane history without consulting the tool's selftest.

## Restoration evidence

* Lane tool never mutated; byte-identical before and after:
  `915527a7d2f553740ed3ab0166669031f19ce2de6b2fec8501208f97244cfc89  tools/mori-sources-appendonly.py`
  (same value at the start of this report, after all runs, and equal to the blob at
  `bf0df77fee4b6ef54a90aea09335c7617f125151`).
* Frozen counter untouched: `c7edaacfff029c2055bee6ddda42ff6f5c040dad7fbac81e9d169602edcbac34`.
* No `git`/`jj` mutation was run in the lane. `git -C ... status --porcelain` at the end of the
  probe lists this report as untracked and shows no change to any file this seat touched; the only
  tracked modification present (` M tools/mori-source-drift.py`) and the other `w2/*.md` untracked
  files belong to concurrently running sibling seats (they appeared during the probe, and the drift
  tool is not a file this probe copied or wrote — every mutant lives under `/fast/scratch`, and
  `pristine.py` hash-matches the tip blob).
* All scratch bytes live under `/fast/scratch/hyaku/mori-r36/MutC2Cols/`; the counter's own
  run-scoped directories were removed by its `finally` block (`ls -d /fast/scratch/hyaku/mori-r36/c2-*`
  returns nothing).
* No tool was installed or upgraded for this probe.

## Harness observation (not this probe's verdict)

One baseline run of the frozen counter (pristine tool, `--seed 11`) failed spuriously with
`repo17 FAIL: no summary line (exit 2): Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set)`.
Cause is isolated and reproducible: the sandbox root is derived from the same `rng` that `--seed`
seeds, so two concurrent invocations with the same seed share one directory and delete each other's
repos:

```
count-c2.py:689:  scratch = os.path.join(SCRATCH_ROOT, "c2-%08x" % rng.randrange(1 << 32))
count-c2.py:718:  shutil.rmtree(scratch, ignore_errors=True)
```

Two simultaneous pristine runs at `--seed 11`:

```
collision-a.txt: counter setup error: [Errno 17] File exists:
                 '/fast/scratch/hyaku/mori-r36/c2-7734d7c1/repo00/corpus'
collision-b.txt: counter setup error: git config commit.gpgsign false failed in
                 /fast/scratch/hyaku/mori-r36/c2-7734d7c1/repo00: fatal: not in a git directory
```

Both runs chose the identical scratch path `c2-7734d7c1`. This is why a sibling seat running the
same seed concurrently can make a truthful tool print `C2=unmet`. The frozen C2 evidence is not
affected (the serial baseline reproduced `C2=met` twice at the same seed), and the failure mode is
loud (setup error / blind FAIL), never a silent false `met`; recorded here as an operability caveat
for anyone re-running the counter in a wave, not as a defect in the C2 truth predicate.

VERDICT: PASS — the assigned defect (immutable-column set mis-selected so mutable-cell edits look
like violations) is detected: mutant A scores blind 6/24, real arm FAIL, `C2=unmet`, exit 1 against a
pristine baseline that scores `C2=met`, exit 0, and the minimal fixture pins the exact defect
(`status`-only edit reported as `ids=[S001]`). No defect found in the C2 detector's ability to fail.
