# MutC2Endpoint — endpoint-only `round_changed` mutation (J4 class)

- Seat: `mori-r36-w2-MutC2Endpoint-28` (mutation-tester, leaf — no subagent dispatch)
- Date: 2026-10-23
- Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin` (read-only); data tip `bf0df77fee4b6ef54a90aea09335c7617f125151`; round base `f10a320d`
- Scratch: `/fast/scratch/hyaku/mori-r36/MutC2Endpoint/`

## Item attacked

Claim C2 (measured, operability): frozen predicate P-C2 and its counter
`.ufo/waves/round-36/count-c2.py` (sha256 `c7edaac…`, pinned in `evidence/freeze-v2.txt`).

Within that claim, this probe attacks the **detector's discrimination of `round_changed`
semantics** — specifically whether the frozen counter can fail a tool that computes
`round_changed` **endpoint-only** (base snapshot vs tip snapshot), ignoring intermediate
commits. That is the J4 class named in the tasking: changes that land and later change back
inside the round must still appear in `round_changed`.

Mutation point: `tools/mori-sources-appendonly.py:246-255`, the block that unioned
`changed_at`/`deleted_at` over every path commit contained in
`git log <base>..<rev>`.

## Artifacts and identity hashes

| Artifact | sha256 |
|---|---|
| lane `tools/mori-sources-appendonly.py` (pristine, at worktree) | `915527a7d2f553740ed3ab0166669031f19ce2de6b2fec8501208f97244cfc89` |
| lane blob `bf0df77:tools/mori-sources-appendonly.py` | `915527a7d2f553740ed3ab0166669031f19ce2de6b2fec8501208f97244cfc89` |
| scratch `control.py` (byte-identical baseline copy) | `915527a7d2f553740ed3ab0166669031f19ce2de6b2fec8501208f97244cfc89` |
| scratch `mutant.py` | `f861d2ed6ed327a096beb2bfada6a3abbef562a84699233ba4d83e95ff194624` |
| lane `.ufo/waves/round-36/count-c2.py` (frozen counter, unmodified) | `c7edaacfff029c2055bee6ddda42ff6f5c040dad7fbac81e9d169602edcbac34` |

`evidence/freeze-v2.txt:4` pins `count-c2.py` to the same `c7edaac…` digest, so the counter
bytes used here are the frozen ones. No tool installs were performed (nothing to record).

## Mutation (one purpose)

Copy of the original, then the `round_changed` block replaced so the verdict reads only the
two endpoints. Diff (verbatim, `diff -u control.py mutant.py`):

```diff
--- /fast/scratch/hyaku/mori-r36/MutC2Endpoint/control.py	2026-10-23 16:14:31.734166238 -0300
+++ /fast/scratch/hyaku/mori-r36/MutC2Endpoint/mutant.py	2026-10-23 16:14:45.735015624 -0300
@@ -247,12 +247,18 @@
     if round_base:
         base_full = git(repo, "rev-parse", "--verify",
                         round_base + "^{commit}").strip()
-        in_range = set(git(repo, "log", "--format=%H",
-                           "%s..%s" % (base_full, rev_full)).split())
-        for index, commit in enumerate(commits):
-            if commit in in_range:
-                round_changed |= changed_at.get(index, set())
-                round_changed |= deleted_at.get(index, set())
+        # MUTANT (J4, endpoint-only): compare only the base and tip snapshots;
+        # intermediate commits - rows changed and later changed back - are
+        # never inspected.
+        base_text = git_blob(repo, "%s:%s" % (base_full, path))
+        base_rows = parse_registry(base_text)[0] if base_text is not None else []
+        base_state = {cells[0]: cells for cells in base_rows}
+        for cid, cells in tip.items():
+            if cid not in base_state:
+                continue
+            if imm_key(cells, imm_idx) != imm_key(base_state[cid], imm_idx):
+                round_changed.add(cid)
+        round_changed |= set(base_state) - set(tip)
 
     return {
         "rev": rev_full,
```

Semantics of the mutant: an id counts in `round_changed` only if it is present in the base
snapshot and its immutable cells differ at the tip, or it is present at the base and absent
at the tip. No intermediate commit is inspected. This is the plausible J4 defect (a gate
author "simplifying" the walk to a two-snapshot diff); `changed_at`/`deleted_at` are still
computed above but no longer read.

The mutation is confined to the scratch copy. The lane's real tool was never edited.

## Detector run 1 — baseline (pristine control), seed 11

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ TMPDIR=/fast/scratch/hyaku/mori-r36/MutC2Endpoint/tmp \
  python3 .ufo/waves/round-36/count-c2.py bf0df77fee4b6ef54a90aea09335c7617f125151 \
    --tool /fast/scratch/hyaku/mori-r36/MutC2Endpoint/control.py --seed 11
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /fast/scratch/hyaku/mori-r36/MutC2Endpoint/control.py
blind arm: 24/24 sandbox histories matched the hidden truth (3.3s; coverage: deletions=24 changed-back=16 superseded=12)
real arm: pass (0.6s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
C2=met
seed=11
CONTROL-EXIT=0
```

Baseline is green (24/24 blind, real arm pass, `C2=met`, exit 0), so any failure below is
attributable to the mutation, not to the sandbox environment.

## Detector run 2 — mutant, ticket-literal command, seed 11

```
$ TMPDIR=/fast/scratch/hyaku/mori-r36/MutC2Endpoint/tmp \
  python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py \
    bf0df77fee4b6ef54a90aea09335c7617f125151 \
    --tool /fast/scratch/hyaku/mori-r36/MutC2Endpoint/mutant.py --seed 11
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /fast/scratch/hyaku/mori-r36/MutC2Endpoint/mutant.py
blind arm: 21/24 sandbox histories matched the hidden truth (1.9s; coverage: deletions=24 changed-back=16 superseded=12)
  repo00 FAIL: lists differ
      want: appendonly_violations=3 ids=[S096,S143] deleted=[S203] superseded=[S096,S143] round_changed=[S016,S143,S203]
      got:  appendonly_violations=3 ids=[S096,S143] deleted=[S203] superseded=[S096,S143] round_changed=[S143,S203]
  repo09 FAIL: lists differ
      want: appendonly_violations=2 ids=[S282] deleted=[S009] superseded=[S282] round_changed=[S009,S031,S282]
      got:  appendonly_violations=2 ids=[S282] deleted=[S009] superseded=[S282] round_changed=[S009,S282]
  repo11 FAIL: lists differ
      want: appendonly_violations=4 ids=[S137] deleted=[S102,S148,S172] superseded=[] round_changed=[S102,S137,S148,S172,S257]
      got:  appendonly_violations=4 ids=[S137] deleted=[S102,S148,S172] superseded=[] round_changed=[S102,S137,S148,S172]
real arm: FAIL (0.3s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  diff: round_changed: want=['S182', 'S193'] got=['S182']
  tool exit=1
C2=unmet
seed=11
LITERAL-EXIT=1
```

**Mutant verdict at seed 11: unmet, exit 1 — killed.** The blind arm failed 3/24
(the exact `same_lists` comparison at `count-c2.py:517`, blind check at `:608`), and the
real arm failed against the independent oracle (`count-c2.py:573-577`).

Two identical mutant runs produced byte-identical output apart from the printed wall-clock
timings (`diff` of timing-normalized outputs, exit 0), so the kill is deterministic
for this seed.

## Detector run 3 — replication at seed 7 (control then mutant, serialized)

The counter derives its scratch directory name from the seed, so the two arms were run
serially to avoid scratch collision.

```
$ python3 .ufo/waves/round-36/count-c2.py bf0df77fee4b6ef54a90aea09335c7617f125151 \
    --tool .../control.py --seed 7
tool: /fast/scratch/hyaku/mori-r36/MutC2Endpoint/control.py
blind arm: 24/24 sandbox histories matched the hidden truth (4.0s; coverage: deletions=22 changed-back=17 superseded=9)
real arm: pass (0.7s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
C2=met
seed=7
CONTROL7-EXIT=0
```

```
$ python3 .ufo/waves/round-36/count-c2.py bf0df77fee4b6ef54a90aea09335c7617f125151 \
    --tool .../mutant.py --seed 7
tool: /fast/scratch/hyaku/mori-r36/MutC2Endpoint/mutant.py
blind arm: 17/24 sandbox histories matched the hidden truth (3.6s; coverage: deletions=22 changed-back=17 superseded=9)
  repo03 FAIL: lists differ
      want: appendonly_violations=4 ids=[S207] deleted=[S046,S164,S230] superseded=[] round_changed=[S046,S127,S164,S207,S230]
      got:  appendonly_violations=4 ids=[S207] deleted=[S046,S164,S230] superseded=[] round_changed=[S127,S164,S207,S230]
  repo08 FAIL: lists differ
      want: appendonly_violations=4 ids=[S187] deleted=[S033,S102,S238] superseded=[S187] round_changed=[S033,S102,S238]
      got:  appendonly_violations=4 ids=[S187] deleted=[S033,S102,S238] superseded=[S187] round_changed=[S033,S238]
  repo16 FAIL: lists differ
      want: appendonly_violations=4 ids=[S083] deleted=[S015,S085,S175] superseded=[S083] round_changed=[S015,S083,S085,S175,S255]
      got:  appendonly_violations=4 ids=[S083] deleted=[S015,S085,S175] superseded=[S083] round_changed=[S015,S083,S085,S175]
  repo18 FAIL: lists differ
      want: appendonly_violations=3 ids=[] deleted=[S127,S191,S289] superseded=[] round_changed=[S016]
      got:  appendonly_violations=3 ids=[] deleted=[S127,S191,S289] superseded=[] round_changed=[]
  repo21 FAIL: lists differ
      want: appendonly_violations=5 ids=[S281] deleted=[S019,S137,S148,S151] superseded=[] round_changed=[S019,S137,S148,S151,S233,S281]
      got:  appendonly_violations=5 ids=[S281] deleted=[S019,S137,S148,S151] superseded=[] round_changed=[S019,S137,S148,S151,S281]
  repo22 FAIL: lists differ
      want: appendonly_violations=4 ids=[S257] deleted=[S079,S094,S226] superseded=[] round_changed=[S094,S226,S257,S276]
      got:  appendonly_violations=4 ids=[S257] deleted=[S079,S094,S226] superseded=[] round_changed=[S094,S226,S257]
  repo23 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S200] superseded=[] round_changed=[S004,S200]
      got:  appendonly_violations=1 ids=[] deleted=[S200] superseded=[] round_changed=[S200]
real arm: FAIL (0.6s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  diff: round_changed: want=['S182', 'S193'] got=['S182']
  tool exit=1
C2=unmet
seed=7
MUTANT7-EXIT=1
```

**Mutant verdict at seed 7: unmet, exit 1 — killed again** (blind 17/24, real arm FAIL).

## Why the dropped ids are the claimed class (reconstruction of the hidden sandboxes)

I rebuilt the counter's sandbox stream deterministically (same seed, same generator, same
rng draws) in a scratch harness and ran the mutant on each rebuilt repo exactly as the blind
arm does, then classified every id the mutant dropped:

```
== seed 11 failing-sandbox classification ==
repo00 S016  changed-back-in-round      base=present tip=present  trace=c4:edit|c5:edit
repo09 S031  changed-back-in-round      base=present tip=present  trace=c1:edit|c6:edit
repo11 S257  changed-back-in-round      base=present tip=present  trace=c1:edit|c3:edit
== seed 7 failing-sandbox classification ==
repo03 S046  added-after-base-then-changed base=absent tip=absent  trace=c3:edit|c5:gone
repo08 S102  added-after-base-then-changed base=absent tip=absent  trace=c6:edit|c7:gone
repo16 S255  changed-back-in-round      base=present tip=present  trace=c5:edit|c6:edit
repo18 S016  changed-back-in-round      base=present tip=present  trace=c6:edit|c7:edit
repo21 S233  changed-back-in-round      base=present tip=present  trace=c1:edit|c5:edit
repo22 S276  changed-back-in-round      base=present tip=present  trace=c6:edit|c8:edit
repo23 S004  changed-back-in-round      base=present tip=present  trace=c1:edit|c5:edit
```

("changed-back-in-round": present at the base and tip with an identical immutable
fingerprint, but its immutable cells changed at intermediate in-range commits, e.g. edit
away at c4 and back at c5. Trace indices are the counter's own commit indices after the
base.) At seed 11 **all three** blind failures are exactly the expected class. At seed 7
five of seven are that class; the other two are rows appended after the base and deleted
inside the round (also invisible to a two-snapshot diff, because the base snapshot never
held them).

The expectation in the tasking — *blind arm fails on changed-back histories* — is observed.

### Real-arm kill anatomy (reported precisely, not over-claimed)

The deterministic real arm also fails for this mutant, but its dropped id is a **different**
endpoint-only blindness, not the changed-back sub-class. Trace for `S193` on the lane's own
history (`f10a320d` is the round base, `6bd57097` the tip, path `corpus/SOURCES.md`):

```
f10a320d (round base): ABSENT
8d56809a: anchor='drivers/base/core.c:3508-3510,3542-3543; tag v7.2' imm_sha1=c2c39e20fb16
ff334073: anchor='drivers/base/core.c:3508-3510,3542-3543; tag v7.2' imm_sha1=c2c39e20fb16
406d91a4: anchor='drivers/base/core.c:3508-3510,3542-3543,4653-4657; tag v7.2' imm_sha1=88e1e7cd53a4
cedb0ec4: anchor='drivers/base/core.c:3508-3510,3542-3543,4653-4657; tag v7.2' imm_sha1=88e1e7cd53a4
```

`S193` is absent at the base, appended in the round, then edited in the round, so the
mutant's `cid not in base_state → continue` branch skips it and prints
`round_changed=[S182]` instead of `[S182,S193]`. The real arm therefore kills this mutant
on both seeds, deterministically (same rev/base), but via the "id absent at the base"
branch. The changed-back sub-class kill is carried by the blind arm (and by the tool's own
selftest fixture, below).

## The mutant's own selftest

The tool's `--selftest` is applicable and was run on the pristine copy and on the mutant
(scratch dirs under `TMPDIR=/fast/scratch/hyaku/mori-r36/MutC2Endpoint/tmp`):

```
$ python3 control.py --selftest
MORI_SOURCES_APPENDONLY_SELFTEST pass=8 fail=0
control-selftest-exit=0

$ python3 mutant.py --selftest
FAIL changed-back inside the round: round_changed: want ['S001'] got []; exit: want 1 got 0
MORI_SOURCES_APPENDONLY_SELFTEST pass=7 fail=1
mutant-selftest-exit=1
```

So this mutation does **not** have the strongest form (selftest green while counter red).
The tool's own fixture `("changed-back inside the round", …)` at
`tools/mori-sources-appendonly.py:370-372` independently red-flags the class: the fixture
is `[base, edited, reverted]` with `base_sha = shas[0]`, hand-expected
`round_changed=["S001"]`, and the mutant returns `[]` with exit 0. Both detectors
(the tool's fixture and the frozen counter's blind arm) catch this defect, which is
consistent — not contradictory — evidence.

## Verdict

- Mutant: `round_changed` computed endpoint-only (base vs tip), intermediate commits
  ignored — `tools/mori-sources-appendonly.py:246-255` semantics.
- Expected detector: frozen C2 counter blind arm (`same_lists` on `ids`/`deleted`/`superseded`/
  `round_changed` plus exit-code equality, `count-c2.py:517`, `:603-615`) and real arm vs
  oracle (`count-c2.py:573-577`).
- Observed: `C2=unmet`, exit 1 at seed 11 (blind 21/24, real arm FAIL) and seed 7
  (blind 17/24, real arm FAIL); baseline pristine copy `C2=met`, exit 0 at both seeds.
- Status: **KILLED** (not survived, not inconclusive). A baseline failure would have been
  inconclusive; the baseline passed, so the kill stands.
- No coverage defect in the frozen counter or in the P-C2 claim was found by this probe:
  the counter can fail, and it fails on the changed-back histories as expected.

**VERDICT: PASS (no defect found)**

## Observations (measurements, no contract change proposed)

1. `count-c2.py:598` increments `coverage["changed_back"]` when `truth["changed_back"]` is
   non-empty, and `truth_from_states` (`:206-215`) computes `changed_back` against each id's
   **first-held** cells across the **whole** history, not against the round base. At seed 11
   it reported `changed-back=16`, but only 3/24 sandboxes contained a changed-back **inside
   the round window** (the classification above). At seed 7 it reported 17 while 5/24 did.
   The frozen minimum (`:703`, `changed_back < 12`) is satisfied by whole-history
   changed-backs, so that number overstates in-round changed-back exercise. The counter
   still killed this mutant at both seeds, and the real arm is seed-independent, so P-C2 as
   frozen is not weakened by this; recorded only as a diagnostic-granularity observation.
2. The real arm's deterministic kill of this mutant comes from the "id absent at the base"
   branch (`S193`), not from the changed-back branch. Readers should not cite the real-arm
   diff as changed-back evidence; the changed-back kill is the blind arm (3/24 at seed 11,
   5/24 at seed 7) plus the tool's own fixture at `:370`.
3. `--seed` is not the only determinant of the sandbox stream in general use, but with an
   explicit `--seed` the stream (and therefore the scratch directory name) is fully
   deterministic; hence control and mutant runs for a given seed must be serialized. They
   were.

## Restoration and bounds evidence

The lane copy was never mutated; only a scratch copy was. Before and after:

```
$ sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-sources-appendonly.py
915527a7d2f553740ed3ab0166669031f19ce2de6b2fec8501208f97244cfc89  tools/mori-sources-appendonly.py
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin show \
    bf0df77fee4b6ef54a90aea09335c7617f125151:tools/mori-sources-appendonly.py | sha256sum
915527a7d2f553740ed3ab0166669031f19ce2de6b2fec8501208f97244cfc89  -
$ sha256sum .ufo/waves/round-36/count-c2.py
c7edaacfff029c2055bee6ddda42ff6f5c040dad7fbac81e9d169602edcbac34  .ufo/waves/round-36/count-c2.py
$ git status --porcelain -- tools/mori-sources-appendonly.py \
    .ufo/waves/round-36/count-c2.py corpus/SOURCES.md
(no output; exit 0)
```

Scope note: `tools/` as a whole is not clean at the time of writing, but the one dirty entry
is not mine. `git status --porcelain -- tools/` reports
` M tools/mori-source-drift.py` (mtime 2026-10-23 16:18:19, sha256 `e22e549e…`), a
concurrent sibling's in-progress edit adding `_public_url` destination policy with a comment
naming `w2/SentCensus`. I never ran, copied or edited that tool; it is an external
concurrent change, left untouched. Every path this probe touched —
`tools/mori-sources-appendonly.py`, `.ufo/waves/round-36/count-c2.py`, `corpus/SOURCES.md` —
is clean and hash-identical to the tip blob.

- Pristine worktree bytes = tip blob bytes = baseline copy bytes (`915527a…`). The mutant
  exists only at `/fast/scratch/hyaku/mori-r36/MutC2Endpoint/mutant.py` (`f861d2ed…`).
- No lane mutation commands were run (no `git add/commit/push/fetch/reset`, no `jj` writes);
  no lane file was edited except this report.
- The counter's own scratch (`/fast/scratch/hyaku/mori-r36/c2-*`) was created and removed
  by the frozen counter itself; `ls -d /fast/scratch/hyaku/mori-r36/c2-*` → `none` after
  each run. My remaining files are the scratch copies, raw outputs and the classification
  harness under `/fast/scratch/hyaku/mori-r36/MutC2Endpoint/`.
- Hard bounds: exactly one lane file written (this report); no `pacman`; no tool
  installs; no subagent dispatch (leaf seat); no sibling-lane or protected-path access.
- Scratch artifact inventory: `control.py`, `mutant.py`, `control-seed11.out`,
  `mutant-seed11.out`, `mutant-seed11-literal.out`, `mutant-seed11-literal2.out`,
  `mutant-seed11-exit.txt`, `control-seed7.out`, `mutant-seed7.out`,
  `classification.out`, `replica_classify.py`, `a.norm`, `b.norm`.

Items kept out of scope by design: no judgment of whether C2 should be met, no integration,
no remediation; the mutation probe stops here.
