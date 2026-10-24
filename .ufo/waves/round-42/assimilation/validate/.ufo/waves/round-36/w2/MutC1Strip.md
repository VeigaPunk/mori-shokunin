# MutC1Strip — C1 excerpt-strip mutation probe

Seat: mori-r36-w2-MutC1Strip-28 · mutation-tester · attack on C1's claimed detector teeth
Target: `tools/mori-source-drift.py` at data tip `bf0df77fee4b6ef54a90aea09335c7617f125151`
Detector: frozen `.ufo/waves/round-36/count-c1.py` (sha256 `86dd3b7ab2d2563bbc811e83717b35dfea3d69717dab4d41d454f8b87c8764c0`,
equal to the `freeze-v2.txt:3` pin — measured below)
Scratch: `/fast/scratch/hyaku/mori-r36/MutC1Strip/` (mutant.py, pristine.py, baseline-repo, fixture_probe.py)

## What this item attacks

The C1 predicate P-C1's `excerpt` rule: "copy bytes with whitespace stripped at both ends
are non-empty and occur contiguously in the fetched body" (`tools/mori-source-drift.py:19-20`,
implementation `:151-152`). The question is whether the frozen counter is actually able to
distinguish the strip from its absence — i.e. whether the whitespace strip is load-bearing
in the blind arm, not decorative. If a mutant that requires the raw copy bytes still scores
`C1=met`, the blind arm never exercises padded copies and the counter's teeth claim is hollow.

**Mutation (one line, one purpose):** skip the whitespace strip in the excerpt test —
require the raw copy bytes to occur in the body.

```diff
--- /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-source-drift.py	2026-10-23 15:19:31.911643420 -0300
+++ mutant.py	2026-10-23 16:13:49.169058745 -0300
@@ -148,7 +148,7 @@
 def classify(body, copy):
     if hashlib.sha256(body).digest() == hashlib.sha256(copy).digest():
         return "fresh"
-    stripped = copy.strip()
+    stripped = copy
     if stripped and stripped in body:
         return "excerpt"
     return "drifted"
```

## Preconditions / hashes (before)

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin show bf0df77fee4b6ef54a90aea09335c7617f125151:tools/mori-source-drift.py | sha256sum
578667ca3ad0a3a83ebcc804f063f89aec78af506c9d09383e16c6ed2fcbcf56  -
$ sha256sum pristine.py            # byte-copy of the rev blob
578667ca3ad0a3a83ebcc804f063f89aec78af506c9d09383e16c6ed2fcbcf56  pristine.py
$ sha256sum mutant.py              # after mutation
e5f76e9ec4b1a6758ede84771f2303e5d0ca0c42a1008e6e1fb278f93ebc10c0  mutant.py
$ sha256sum .ufo/waves/round-36/count-c1.py
86dd3b7ab2d2563bbc811e83717b35dfea3d69717dab4d41d454f8b87c8764c0  count-c1.py
$ grep -n "count-c1" .ufo/waves/round-36/evidence/freeze-v2.txt
3:86dd3b7ab2d2563bbc811e83717b35dfea3d69717dab4d41d454f8b87c8764c0  count-c1.py
```

Frozen counter file matches its freeze pin; mutant differs from the rev blob only in the
one line shown.

## Detector runs (same counter, same seed 11, same corpus)

The live lane worktree is no longer at the data tip (siblings committed past it; see
"Lane drift" below), so the counter's real-arm precondition
`git diff --quiet <rev> -- corpus` fails in the live repo. All three legs below were
therefore run with `--repo` a scratch `git clone --shared` checked out exactly at
`bf0df77fee4b6ef54a90aea09335c7617f125151` (`baseline-repo`, corpus diff rc=0, 0 untracked
under corpus), so pristine, mutant and restored legs see identical repo and network bytes.
The mutant's blind failure is reproduced identically against the live lane repo as well.

### Baseline — pristine rev blob (expect met)

```
$ python3 .ufo/waves/round-36/count-c1.py bf0df77fee4b6ef54a90aea09335c7617f125151 \
    --repo /fast/scratch/hyaku/mori-r36/MutC1Strip/baseline-repo \
    --tool /fast/scratch/hyaku/mori-r36/MutC1Strip/pristine.py --seed 11
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
real_rows=220 oracle_fetched=58 oracle_fresh=49 oracle_drifted=9 oracle_excluded=0 tool_exit=1 tool_rows=220 mismatches=0
C1=met
seed=11
PRISTINE_COUNTER_RC=0
```

### Mutant — strip removed (expect unmet)

```
$ python3 .ufo/waves/round-36/count-c1.py bf0df77fee4b6ef54a90aea09335c7617f125151 \
    --repo /fast/scratch/hyaku/mori-r36/MutC1Strip/baseline-repo \
    --tool /fast/scratch/hyaku/mori-r36/MutC1Strip/mutant.py --seed 11
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=5
blind_mismatch S047 tool=drifted truth=excerpt
blind_mismatch S101 tool=drifted truth=excerpt
blind_mismatch S232 tool=drifted truth=excerpt
blind_mismatch S244 tool=drifted truth=excerpt
blind_mismatch S271 tool=drifted truth=excerpt
real_arm=skipped
C1=unmet
seed=11
MUT_COUNTER_CLONE_RC=1
```

Same mutant against the live lane repo (no `--repo`), same seed:

```
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=5
... identical five blind_mismatch lines ...
real_arm=skipped
C1=unmet
MUT_COUNTER_RC=1
```

The counter fails exactly where the padded copies are: five blind rows flip
`excerpt` → `drifted`.

### Restored — original bytes back (expect met)

```
$ cp pristine.py mutant.py
$ sha256sum mutant.py
578667ca3ad0a3a83ebcc804f063f89aec78af506c9d09383e16c6ed2fcbcf56  mutant.py
$ cmp mutant.py pristine.py; echo $?
RESTORE_CMP_RC=0
$ python3 mutant.py --selftest
selftest exit_code            PASS
selftest row_states           PASS
selftest summary              PASS
selftest missing_sources_exit2 PASS
MORI_SOURCE_DRIFT_SELFTEST: PASS (4 cases)
RESTORED_SELFTEST_RC=0
$ python3 .ufo/waves/round-36/count-c1.py bf0df77fee4b6ef54a90aea09335c7617f125151 \
    --repo .../baseline-repo --tool .../mutant.py --seed 11
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
real_rows=220 oracle_fetched=58 oracle_fresh=49 oracle_drifted=9 oracle_excluded=0 tool_exit=1 tool_rows=220 mismatches=0
C1=met
seed=11
RESTORED_COUNTER_RC=0
```

Restored leg reproduces the frozen receipt `evidence/c1-after.txt` numbers exactly
(blind 40/40, 58/49/9/0, mismatches=0), differing only in seed (11 vs 7388485190103051243
as recorded there).

## Selftest behavior of the mutant (honest note)

The mutant does **not** pass its own selftest: the tool hard-pads the excerpt fixture copy
`w("sources-r40", "S102.txt", b"  \n" + piece + b"\t ")` (`tools/mori-source-drift.py:276`).

```
$ python3 mutant.py --selftest
selftest exit_code            PASS
selftest row_states           FAIL (got=[('S101', 'fresh'), ('S102', 'drifted'), ('S103', 'drifted'), ('S104', 'unavailable'), ('S105', 'unavailable'), ('S106', 'no-copy'), ('S107', 'no-copy'), ('S108', 'fresh')] want=[('S101', 'fresh'), ('S102', 'excerpt'), ('S103', 'drifted'), ('S104', 'unavailable'), ('S105', 'unavailable'), ('S106', 'no-copy'), ('S107', 'no-copy'), ('S108', 'fresh')])
selftest summary              FAIL (summary=('8', '2', '0', '2', '2', '2'))
selftest missing_sources_exit2 PASS
MORI_SOURCE_DRIFT_SELFTEST: FAIL (2/4)
MUT_SELFTEST_RC=1
```

So this mutant is not the "selftest passes, counter fails" strongest-receipt shape — but the
counter is not relying on the tool's selftest for detection, and the counter kill is
independent of it.

## Why exactly five failures (blind-fixture anatomy)

`fixture_probe.py` replays the counter's own `build_fixture` at seed 11 (same module, same
`random.Random(11)`) and inspects the written copies:

```
$ python3 fixture_probe.py
excerpt_rows=8
excerpt S047 padded=True stripped_in_body=True raw_in_body=False
excerpt S101 padded=True stripped_in_body=True raw_in_body=False
excerpt S203 padded=True stripped_in_body=True raw_in_body=True
excerpt S209 padded=True stripped_in_body=True raw_in_body=True
excerpt S226 padded=True stripped_in_body=True raw_in_body=True
excerpt S232 padded=True stripped_in_body=True raw_in_body=False
excerpt S244 padded=True stripped_in_body=True raw_in_body=False
excerpt S271 padded=True stripped_in_body=True raw_in_body=False
mutant_blind_mismatch_ids=S047,S101,S232,S244,S271
padded_ids=S047,S101,S203,S209,S226,S232,S244,S271
all_mismatches_padded=True
all_padded_mismatched=False
```

Reading: all 8 excerpt copies have whitespace at an edge (`padded=True`), but only the 5
synthetically padded ones (`b"  \n" + piece + b"\t "`, counter `count-c1.py:448`) have
`raw_in_body=False`; the other 3 are literal body slices whose edge whitespace is part of
the body, so raw bytes still occur (`raw_in_body=True`). The mutant's mismatch set is exactly
the `raw_in_body=False` set — no false positives, no missed padded rows. The strip is
therefore exercised by ~5/8 excerpt rows per seed on average (per-row synthetic-padding
probability 0.5), and the counter's blind arm has real teeth against this rule.

## Lane drift observed (not caused by this seat; no lane writes by me)

- Lane HEAD is now `7c6fbac`; the data tip `bf0df77` is 3+ commits back.
- `tools/mori-source-drift.py` in the **worktree** has an uncommitted sibling edit
  (` M` in `git status`, adds `FETCH_MAX_BYTES = 4 * 1024 * 1024`, bounded read, `/huge`
  selftest row). Worktree sha256 is now
  `31b49a5362670a402fa4508fbeef3866ca89c6dab157762a26b49d843e476429`; both the rev blob at
  `bf0df77` and `HEAD:` are still `578667ca…`. My probe and restore target the rev blob
  (`pristine.py`), never the live worktree file.
- `corpus/` in the worktree differs from `bf0df77` in 5 files (QUALITY, README, SOURCES,
  knowledge/source-drift-r36.md, lessons/round-36.md), which is why the counter's real-arm
  worktree precondition fails in the live repo; hence the pinned scratch clone for the
  three-way legs.

## Compliance / tooling

- Lane repo: read-only. No `git add/commit/push/fetch/reset`, no mutating `jj`, no lane file
  edited. The one lane write is this report.
- No tools installed; no `pacman` invoked. Scratch confined to
  `/fast/scratch/hyaku/mori-r36/MutC1Strip/` (mutant.py, pristine.py, baseline-repo,
  fixture_probe.py, probe fixture root).
- Restoration: mutant.py restored to exact rev-blob bytes before the final re-run;
  `cmp` rc=0 against `pristine.py`, sha256 `578667ca…`.

## Verdict

Mutant: require raw copy bytes in the excerpt test (`stripped = copy`), one line.
Expected detector: frozen `count-c1.py --seed 11` blind arm.
Observed: `blind_mismatch` ×5 (all synthetically padded excerpt rows), `C1=unmet`, exit 1;
pristine and restored bytes both give `blind mismatches=0`, `real 58/49/9/0 mismatches=0`,
`C1=met`, exit 0.

The C1 counter can fail and fails precisely on the strip rule; the excerpt whitespace strip
is load-bearing in the blind arm, and the fixture exercises it. No defect found in the C1
claim's detector teeth. A separate observation (not a defect in this claim): the lane
worktree has drifted past the data tip with an uncommitted sibling edit to the very tool
under test, so any future re-score must pin `--repo` to a clean checkout of the rev.

VERDICT: PASS (no defect found; mutant killed, detector teeth confirmed)
