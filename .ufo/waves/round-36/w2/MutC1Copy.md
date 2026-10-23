# w2/MutC1Copy — K13 mutant: read the OLDEST `sources-r<N>` copy

Seat: `mori-r36-w2-MutC1Copy-25` (mutation-tester). Round 36, wave 2, attempt 2.
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin` (read-only for this seat — no lane file was written by me
except this report). Landed data tip under test: `bf0df77fee4b6ef54a90aea09335c7617f125151`.

**Attacks:** claim C1 (exploratory freshness technique) — specifically the contract clause

> Its copy is the file `DIR/corpus/evidence/sources-r<N>/<id>.<ext>` (any extension) with the **highest integer `N`**

(`.ufo/waves/round-36/contract.md`, "C1 tool interface"). The mutant violates exactly that clause and nothing else.

No freshness verdict is asserted or inferred anywhere below; this is a byte-behaviour probe of P-C1's copy
selection only.

---

## 1. Objects and hashes

| object | path | sha256 |
|---|---|---|
| lane tool (unmodified) | `mori-shokunin/tools/mori-source-drift.py` | `578667ca3ad0a3a83ebcc804f063f89aec78af506c9d09383e16c6ed2fcbcf56` |
| pristine control copy | `/fast/scratch/hyaku/mori-r36/MutC1Copy/pristine.py` | `578667ca3ad0a3a83ebcc804f063f89aec78af506c9d09383e16c6ed2fcbcf56` |
| mutant (probe artifact, restored afterwards) | `…/MutC1Copy/mutant.audit.py` | `5e43ce87d7b832b27b67c8dfe6c12fb49746e86e3b008067234036c5875619c6` |
| frozen counter | `.ufo/waves/round-36/count-c1.py` | `86dd3b7ab2d2563bbc811e83717b35dfea3d69717dab4d41d454f8b87c8764c0` |

Counter hash matches the frozen pin:

```
$ sha256sum .ufo/waves/round-36/count-c1.py
86dd3b7ab2d2563bbc811e83717b35dfea3d69717dab4d41d454f8b87c8764c0  .ufo/waves/round-36/count-c1.py
$ grep count-c1 .ufo/waves/round-36/evidence/freeze-v2.txt
86dd3b7ab2d2563bbc811e83717b35dfea3d69717dab4d41d454f8b87c8764c0  count-c1.py
```

Both copies are 15189 bytes; the mutation changes one character class, not a length.

## 2. The mutation (one purpose only: newest → oldest copy)

`find_copy()` in the tool scans `corpus/evidence/sources-r<N>/` and keeps the copy with the highest `N`
(`tools/mori-source-drift.py:73-96`). The mutant inverts that one comparison (line 94):

```
$ diff -u pristine.py mutant.py
--- pristine.py	2026-10-23 15:55:18.501851464 -0300
+++ mutant.py	2026-10-23 15:55:20.319505822 -0300
@@ -91,7 +91,7 @@
             continue
         for entry in entries:
             if entry.startswith(sid + "."):
-                if best is None or n > best[0]:
+                if best is None or n < best[0]:
                     best = (n, os.path.join(d, entry))
     return best[1] if best else None
```

No other byte differs (`grep -n "best\[0\]"` finds exactly one occurrence in each copy). The mutant therefore
keeps the *oldest* (lowest-numbered) directory's file as the row's copy. Note the function docstring still reads
`"""The copy of a row: corpus/evidence/sources-r<N>/<sid>.<ext>, highest N."""` (line 73) — the mutation is not
self-documenting, which is the realistic shape of this defect class.

## 3. Detectors, and what each one is expected to do

| detector | expectation under the mutation |
|---|---|
| frozen counter, blind arm (random decoy copies in lower-numbered dirs) | fails: decoy rows flip `fresh`/`excerpt` → `drifted` |
| frozen counter, real arm (lane `corpus/` at R) | blind to it — see §7: the lane corpus has no row with copies in two `sources-r<N>` dirs |
| tool's own `--selftest` | fails: `S101` has the `sources-r10` decoy deliberately planted |
| independent one-row probe (§6) | `S900 fresh` → `S900 drifted` |

## 4. Baseline control — PRISTINE bytes, same seeds

### 4a. Clean-tree control (proves the baseline can reach `C1=met`)

The lane worktree was dirty while this seat ran (§8), which makes the counter's real arm short-circuit. To get a
true baseline, the rev's `corpus/` was extracted read-only (`git archive`, no lane mutation) into a scratch git repo:

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive bf0df77fe corpus | tar -x -C /fast/scratch/hyaku/mori-r36/MutC1Copy/clean
$ cd /fast/scratch/hyaku/mori-r36/MutC1Copy/clean && git init -q . && git add -A && git commit -qm "corpus at bf0df77"
scratch_sha=c94027ce4a89dc7ac1ee2a71fbe2ff7d91e1c2c0
files=276
```

```
$ python3 .ufo/waves/round-36/count-c1.py c94027ce4a89dc7ac1ee2a71fbe2ff7d91e1c2c0 \
    --repo /fast/scratch/hyaku/mori-r36/MutC1Copy/clean \
    --tool /fast/scratch/hyaku/mori-r36/MutC1Copy/pristine.py --seed 11
P-C1: at revision R, tools/mori-source-drift.py classifies every row of a 40-row blind fixture drawn at run time exactly as the counter's hidden truth, and on the lane's own corpus/SOURCES.md at R it agrees with the counter's independent live oracle on every row the oracle classified, with at least 10 oracle-fetched rows including at least one oracle-fresh and one oracle-drifted row.
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
real_rows=220 oracle_fetched=58 oracle_fresh=49 oracle_drifted=9 oracle_excluded=0 tool_exit=1 tool_rows=220 mismatches=0
C1=met
seed=11
```

Exit 0. This reproduces the landed receipt `evidence/c1-after.txt` (`blind 40/40`, `oracle_fetched=58 fresh=49
drifted=9 excluded=0 mismatches=0`) with the pristine bytes, on an independent copy of the same corpus. The
baseline is healthy; the counter is not failing on its own.

### 4b. Same-seed control against the live worktree

```
$ python3 .ufo/waves/round-36/count-c1.py bf0df77fe --tool …/MutC1Copy/pristine.py --seed 11
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
real=unmet worktree_corpus_differs_from_rev
C1=unmet
seed=11
```

and at seed 4242 the same pattern (`blind_rows=40 … mismatches=0`, `real=unmet worktree_corpus_differs_from_rev`).
The **blind arm — the arm that kills the mutant — passes with pristine bytes at both seeds**. The `real=unmet` is
environmental and is diagnosed in §8, not attributable to the tool.

## 5. Mutant under the frozen counter — full output

### seed 11 (the assigned seed)

```
$ python3 .ufo/waves/round-36/count-c1.py bf0df77fee4b6ef54a90aea09335c7617f125151 \
    --tool /fast/scratch/hyaku/mori-r36/MutC1Copy/mutant.py --seed 11
P-C1: at revision R, tools/mori-source-drift.py classifies every row of a 40-row blind fixture drawn at run time exactly as the counter's hidden truth, and on the lane's own corpus/SOURCES.md at R it agrees with the counter's independent live oracle on every row the oracle classified, with at least 10 oracle-fetched rows including at least one oracle-fresh and one oracle-drifted row.
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=12
blind_mismatch S003 tool=drifted truth=fresh
blind_mismatch S047 tool=drifted truth=excerpt
blind_mismatch S101 tool=drifted truth=excerpt
blind_mismatch S120 tool=drifted truth=fresh
blind_mismatch S168 tool=drifted truth=fresh
blind_mismatch S203 tool=drifted truth=excerpt
blind_mismatch S209 tool=drifted truth=excerpt
blind_mismatch S226 tool=drifted truth=excerpt
blind_mismatch S239 tool=drifted truth=fresh
blind_mismatch S244 tool=drifted truth=excerpt
blind_mismatch S256 tool=drifted truth=fresh
blind_mismatch S271 tool=drifted truth=excerpt
real_arm=skipped
C1=unmet
seed=11
```

**exit code 1.**

### seed 4242 (replay, independence check)

```
$ python3 .ufo/waves/round-36/count-c1.py bf0df77fe --tool …/MutC1Copy/mutant.py --seed 4242
P-C1: at revision R, tools/mori-source-drift.py classifies every row of a 40-row blind fixture drawn at run time exactly as the counter's hidden truth, and on the lane's own corpus/SOURCES.md at R it agrees with the counter's independent live oracle on every row the oracle classified, with at least 10 oracle-fetched rows including at least one oracle-fresh and one oracle-drifted row.
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=12
blind_mismatch S015 tool=drifted truth=fresh
blind_mismatch S065 tool=drifted truth=fresh
blind_mismatch S073 tool=drifted truth=excerpt
blind_mismatch S081 tool=drifted truth=fresh
blind_mismatch S088 tool=drifted truth=fresh
blind_mismatch S093 tool=drifted truth=excerpt
blind_mismatch S120 tool=drifted truth=excerpt
blind_mismatch S122 tool=drifted truth=fresh
blind_mismatch S164 tool=drifted truth=excerpt
blind_mismatch S195 tool=drifted truth=fresh
blind_mismatch S229 tool=drifted truth=excerpt
blind_mismatch S292 tool=drifted truth=excerpt
real_arm=skipped
C1=unmet
seed=4242
```

**exit code 1.** Twelve mismatches at both seeds = exactly the twelve `decoy_rows` the fixture arms with a
lower-numbered decoy (`count-c1.py:399`, `decoy_rows = set(with_copy[:12])`); every flipped row moved
`fresh`/`excerpt` → `drifted`, which is what reading the older, unrelated decoy bytes must produce. No row outside
the decoy set changed state.

## 6. Independent probe (not the counter) — one row, two copies

Fixture: `S900` → `http://127.0.0.1:P/x`, `sources-r40/S900.src` = served body, `sources-r10/S900.src` = `b"decoy bytes"`.

```
$ python3 decoy_probe.py pristine.py
tool=pristine.py
exit=0
stdout='S900 fresh\nMORI_SOURCE_DRIFT rows=1 fresh=1 excerpt=0 drifted=0 unavailable=0 no-copy=0\n'
stderr=''

$ python3 decoy_probe.py mutant.py
tool=mutant.py
exit=1
stdout='S900 drifted\nMORI_SOURCE_DRIFT rows=1 fresh=0 excerpt=0 drifted=1 unavailable=0 no-copy=0\n'
stderr=''
```

The two binaries differ only on the row that carries two copies, and the difference is exactly the contract clause.

## 7. The tool's own selftest — and the "strongest receipt" question

```
$ python3 pristine.py --selftest
selftest exit_code            PASS
selftest row_states           PASS
selftest summary              PASS
selftest missing_sources_exit2 PASS
MORI_SOURCE_DRIFT_SELFTEST: PASS (4 cases)      exit 0

$ python3 mutant.py --selftest
selftest exit_code            PASS
selftest row_states           FAIL (got=[('S101','drifted'),('S102','excerpt'),('S103','drifted'),('S104','unavailable'),('S105','unavailable'),('S106','no-copy'),('S107','no-copy'),('S108','fresh')] want=[('S101','fresh'),…])
selftest summary              FAIL (summary=('8','1','1','2','2','2'))
selftest missing_sources_exit2 PASS
MORI_SOURCE_DRIFT_SELFTEST: FAIL (2/4)          exit 1
```

**The mutant does not produce the "selftest passes while the counter fails" receipt** — the tool's selftest already
plants the K13 decoy (`w("sources-r10", "S101.src", b"older decoy bytes")`, `tools/mori-source-drift.py:270`) and
catches it (`row_states`, `summary`). That is a defence of the *tool*, not a weakness of the *counter*: the counter's
blind arm remains independently discriminating, with a randomised decoy set, random ids/paths/extensions and a truth
that never touches disk — none of which the selftest provides.

**Coverage observation (not a defect, no contract change asked for):** the real arm cannot see this mutation class.
The lane's own corpus has seven copy generations but no row that appears in more than one of them:

```
$ ls -d corpus/evidence/sources-r*
corpus/evidence/sources-r30 … sources-r36
$ ls corpus/evidence/sources-r*/* | xargs -n1 basename | sed 's/\..*//' | sort | uniq -d
(no output)
```

So newest-vs-oldest selection is unobservable on real bytes, and P-C1's K13 sensitivity rests entirely on the blind
fixture's decoys. That is what the frozen predicate claims (blind arm first, real arm second), so the predicate is
doing what it says; the note is recorded because a future reader should not assume the real arm covers K13.

## 8. Environmental note — why the live-worktree control printed `real=unmet`

The lane worktree was being written by concurrent wave-2 seats while this probe ran; I made no lane write. Observed
state (read-only `git status`):

```
$ git -C mori-shokunin status --porcelain corpus/
 M corpus/QUALITY.md
 M corpus/README.md
 M corpus/SOURCES.md
 M corpus/knowledge/source-drift-r36.md
?? corpus/lessons/round-36.md
$ git -C mori-shokunin rev-parse HEAD
bf0df77fee4b6ef54a90aea09335c7617f125151
```

mtimes 15:52:46 … 15:57:22, i.e. inside this seat's run window (probe start 15:55), and the counter's real arm
refuses a worktree whose `corpus/` differs from the rev (`count-c1.py:575-580`). §4a shows the same pristine bytes
reaching `C1=met` on an extracted, clean copy of the same rev, so the `real=unmet` is the dirty worktree, not the
tool and not the mutation. **This does not weaken the kill**: the mutant failed on the blind arm, which runs in a
fresh temp root and never touches the lane corpus, and the pristine bytes passed that same blind arm at the same
two seeds.

## 9. Restoration evidence

The lane tool was never opened for writing. After the probe:

```
$ cp mutant.py mutant.audit.py        # preserve the attested mutant
$ cp pristine.py mutant.py            # restore exact original bytes
$ cmp mutant.py pristine.py && echo scratch_restored=byte-identical
scratch_restored=byte-identical
$ cmp pristine.py /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-source-drift.py && echo scratch_pristine==lane_tool
scratch_pristine==lane_tool
$ sha256sum tools/mori-source-drift.py pristine.py mutant.py mutant.audit.py
578667ca3ad0a3a83ebcc804f063f89aec78af506c9d09383e16c6ed2fcbcf56  mori-shokunin/tools/mori-source-drift.py
578667ca3ad0a3a83ebcc804f063f89aec78af506c9d09383e16c6ed2fcbcf56  /fast/scratch/hyaku/mori-r36/MutC1Copy/pristine.py
578667ca3ad0a3a83ebcc804f063f89aec78af506c9d09383e16c6ed2fcbcf56  /fast/scratch/hyaku/mori-r36/MutC1Copy/mutant.py
5e43ce87d7b832b27b67c8dfe6c12fb49746e86e3b008067234036c5875619c6  /fast/scratch/hyaku/mori-r36/MutC1Copy/mutant.audit.py
```

Before = after = `578667ca…` for the lane tool and for the restored scratch copy; the only surviving difference is
the deliberately kept `mutant.audit.py` in disposable scratch (`/fast/scratch/hyaku/mori-r36/MutC1Copy/`).

## 10. Installs

None. No `pacman`, no `uv tool`, no `npx`, no cargo/npm — nothing was installed or upgraded for this probe.

---

## Verdict

| question | answer |
|---|---|
| mutant | `find_copy` reads the **oldest** `sources-r<N>` copy instead of the newest (`tools/mori-source-drift.py:94`, `n > best[0]` → `n < best[0]`) |
| expected detector | frozen counter `count-c1.py` blind arm (random lower-numbered decoy copies) |
| observed, seed 11 | `blind_rows=40 … mismatches=12`, all `drifted` vs truth `fresh`/`excerpt`; `real_arm=skipped`; `C1=unmet`; **exit 1** |
| observed, seed 4242 | identical shape, `mismatches=12`, `C1=unmet`, **exit 1** |
| control, pristine bytes | blind arm `mismatches=0` at both seeds; clean-corpus run `C1=met`, exit 0 (`oracle_fetched=58 fresh=49 drifted=9 mismatches=0`) |
| mutant selftest | FAIL (2/4) — caught, so the "selftest passes while counter fails" receipt is not available for this class |
| restoration | `cmp` byte-identical; lane tool hash unchanged at `578667ca…` |

**VERDICT: PASS** — no defect found in the C1 detector for the K13 copy-selection class. The frozen counter kills
this mutant deterministically at both seeds tested, from the blind arm alone, while the pristine bytes reach
`C1=met` on the same rev from a clean tree; the real arm is (documented above) blind to this class by corpus shape,
not by any error in the predicate.
