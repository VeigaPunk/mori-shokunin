# MutC1Excerpt — deleting the excerpt rule from `tools/mori-source-drift.py`

**Seat:** mutation-tester, mori round 36 wave 2 (attempt 2), `mori-r36-w2-MutC1Excerpt-25`.
**Item attacked:** C1's classification rule in `tools/mori-source-drift.py` (`classify`,
lane file lines 148–154, sha256 `578667ca…`) and the frozen C1 counter
`.ufo/waves/round-36/count-c1.py` (sha256 `86dd3b7a…`, matching `evidence/freeze-v2.txt`).
**Data tip:** `bf0df77fee4b6ef54a90aea09335c7617f125151`.

**One-purpose mutation:** delete the excerpt rule, leaving only `fresh` / else `drifted`
(the plausible simplification "a copy that is not byte-identical is drift"). No other byte
changed.

## 1. Specimen

The lane tool is read-only for this seat, so the specimen is a scratch copy; the lane file
was never opened for writing.

```
$ mkdir -p /fast/scratch/hyaku/mori-r36/mori-r36-w2-MutC1Excerpt-25
$ cp -p tools/mori-source-drift.py .../pristine.py
$ cp -p tools/mori-source-drift.py .../mutant.py
$ sha256sum tools/mori-source-drift.py .../pristine.py .../mutant.py
578667ca3ad0a3a83ebcc804f063f89aec78af506c9d09383e16c6ed2fcbcf56  tools/mori-source-drift.py
578667ca3ad0a3a83ebcc804f063f89aec78af506c9d09383e16c6ed2fcbcf56  .../pristine.py
578667ca3ad0a3a83ebcc804f063f89aec78af506c9d09383e16c6ed2fcbcf56  .../mutant.py
```

### Mutant diff (exact)

```
$ diff -u pristine.py mutant.py
--- .../pristine.py	2026-10-23 15:19:31.911643420 -0300
+++ .../mutant.py	2026-10-23 15:55:47.117759507 -0300
@@ -148,9 +148,6 @@
 def classify(body, copy):
     if hashlib.sha256(body).digest() == hashlib.sha256(copy).digest():
         return "fresh"
-    stripped = copy.strip()
-    if stripped and stripped in body:
-        return "excerpt"
     return "drifted"
```

Mutant sha256: `0f8672a207ff40e1f74fa347d9f569440b752f932260c9b20113a38065c168e6`
(3 lines deleted, 15189 → 15098 bytes; `python3 -m py_compile mutant.py` → ok).

The mutant leaves the tool's public contract inconsistent: the rest of the program still
advertises the `excerpt` state in `STATES` and the summary line, but no input can now
produce it. That self-contradiction is part of the defect under test.

## 2. Baseline (pristine bytes) — two roots

### 2a. Lane worktree as `--repo` (as assigned)

```
$ python3 .ufo/waves/round-36/count-c1.py bf0df77fee4b6ef54a90aea09335c7617f125151 \
    --tool .../pristine.py --seed 11
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
real=unmet worktree_corpus_differs_from_rev
C1=unmet
seed=11
baseline_exit=1
```

The blind arm (the only detector of this rule, see §5) passes 40/40 with `mismatches=0`.
The real arm refused before fetching because the lane worktree `corpus/` differs from the
rev — four files are being edited in place by concurrent wave-2 seats while this probe ran:

```
$ git status --porcelain -- corpus
 M corpus/QUALITY.md
 M corpus/README.md
 M corpus/SOURCES.md
 M corpus/knowledge/source-drift-r36.md
$ ls -l --time-style=full-iso corpus/SOURCES.md
-rw-r--r-- 1 vgpnk vgpnk 221582 2026-10-23 15:54:25 -0300 corpus/SOURCES.md   (probe ran 15:56)
```

That is in-flight sibling work, not a counter defect, and it makes this baseline
inconclusive for the real arm. Per the mutation-tester rule ("a baseline failure is
inconclusive"), the control was repeated against a clean checkout of the same rev.

### 2b. Clean checkout of the same rev (control baseline)

```
$ git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin .../lane-bf0df77
$ git -C .../lane-bf0df77 checkout bf0df77fee4b6ef54a90aea09335c7617f125151
$ git -C .../lane-bf0df77 rev-parse HEAD
bf0df77fee4b6ef54a90aea09335c7617f125151
$ git -C .../lane-bf0df77 status --porcelain -- corpus | wc -l
0
$ git -C .../lane-bf0df77 cat-file -p HEAD:tools/mori-source-drift.py | sha256sum
578667ca3ad0a3a83ebcc804f063f89aec78af506c9d09383e16c6ed2fcbcf56  -
$ python3 .ufo/waves/round-36/count-c1.py bf0df77fee4b6ef54a90aea09335c7617f125151 \
    --repo .../lane-bf0df77 --tool .../pristine.py --seed 11
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
real_rows=220 oracle_fetched=58 oracle_fresh=49 oracle_drifted=9 oracle_excluded=0 tool_exit=1 tool_rows=220 mismatches=0
C1=met
seed=11
baseline_clone_exit=0
```

Baseline fully green: exit 0, C1=met, blind 40/40, real 220 rows / 58 fetched / 0 mismatches.
(The clone is a read-only derivative of the lane — `git clone` does not mutate the source —
and contains exactly the rev's tool bytes.)

## 3. Mutant against the frozen counter

```
$ python3 .ufo/waves/round-36/count-c1.py bf0df77fee4b6ef54a90aea09335c7617f125151 \
    --tool .../mutant.py --seed 11
P-C1: at revision R, tools/mori-source-drift.py classifies every row of a 40-row blind fixture drawn at run time exactly as the counter's hidden truth, and on the lane's own corpus/SOURCES.md at R it agrees with the counter's independent live oracle on every row the oracle classified, with at least 10 oracle-fetched rows including at least one oracle-fresh and one oracle-drifted row.
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=8
blind_mismatch S047 tool=drifted truth=excerpt
blind_mismatch S101 tool=drifted truth=excerpt
blind_mismatch S203 tool=drifted truth=excerpt
blind_mismatch S209 tool=drifted truth=excerpt
blind_mismatch S226 tool=drifted truth=excerpt
blind_mismatch S232 tool=drifted truth=excerpt
blind_mismatch S244 tool=drifted truth=excerpt
blind_mismatch S271 tool=drifted truth=excerpt
real_arm=skipped
C1=unmet
seed=11
mutant_exit=1
```

Repeated with `--repo` = the clean checkout, identical verdict and identical 8 mismatch
rows (34.2 s each):

```
$ ... --repo .../lane-bf0df77 --tool .../mutant.py --seed 11
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=8
... same 8 blind_mismatch lines ...
real_arm=skipped
C1=unmet
seed=11
mutant_clone_exit=1
```

The mutant is **killed**: exactly the 8 truth-`excerpt` rows are reported `drifted`, every
other row matches, exit 1 with `C1=unmet`. The counter's blind arm thus discriminates the
presence of the excerpt rule, independent of network and worktree state.

## 4. Selftest under the mutant

```
$ python3 .../mutant.py --selftest
selftest exit_code            PASS
selftest row_states           FAIL (got=[('S101', 'fresh'), ('S102', 'drifted'), ('S103', 'drifted'), ('S104', 'unavailable'), ('S105', 'unavailable'), ('S106', 'no-copy'), ('S107', 'no-copy'), ('S108', 'fresh')] want=[('S101', 'fresh'), ('S102', 'excerpt'), ('S103', 'drifted'), ('S104', 'unavailable'), ('S105', 'unavailable'), ('S106', 'no-copy'), ('S107', 'no-copy'), ('S108', 'fresh')])
selftest summary              FAIL (summary=('8', '2', '0', '2', '2', '2'))
selftest missing_sources_exit2 PASS
MORI_SOURCE_DRIFT_SELFTEST: FAIL (2/4)
mutant_selftest_exit=1
```

The pristine selftest passes all 4 cases (`MORI_SOURCE_DRIFT_SELFTEST: PASS (4 cases)`,
exit 0). So this mutant is **not** the strongest class (selftest also catches it); it is
still a valid counter kill — the frozen counter fails on bytes whose selftest failure mode
is a second, independent signal.

Direct rule probe, bypassing both harnesses (same `(body, copy)` pair for both files):

```
$ python3 classify_probe.py pristine.py mutant.py
copy.strip() in body: True
pristine excerpt_pair -> excerpt
pristine fresh_pair   -> fresh
pristine drifted_pair -> drifted
mutant excerpt_pair -> drifted
mutant fresh_pair   -> fresh
mutant drifted_pair -> drifted
```

## 5. Coverage observation (not a contract change)

At `bf0df77` the real arm fetched 58 rows, of which 49 fresh + 9 drifted = 58, so **zero**
oracle-fetched rows are `excerpt`. The excerpt rule is therefore exercised only by the
blind arm; deleting it cannot be caught by the real corpus arm at this rev. The blind arm
does catch it (8/8), so P-C1 as a whole is not weakened — but any future claim that "the
real corpus exercises every classify branch" would be false for `excerpt` at this rev.

## 6. Restoration / bounds evidence

- The lane tool was never modified; after all runs:
  `sha256sum tools/mori-source-drift.py` → `578667ca3ad0a3a83ebcc804f063f89aec78af506c9d09383e16c6ed2fcbcf56`
  (identical to the pre-probe and rev blob hash). No lane file other than this report was
  written; no `git`/`jj` mutation was issued against the lane.
- Mutated bytes are preserved only at
  `/fast/scratch/hyaku/mori-r36/mori-r36-w2-MutC1Excerpt-25/mutant.py`
  (`0f8672a2…`) together with `pristine.py`, `mutant.diff`, and the raw `.out`/`.err`
  captures; the scratch clone lives at `.../lane-bf0df77`.
- Tooling installs: none.
- Commands run only read-only lane operations (`git status`, `git diff`, `git ls-tree`,
  `git cat-file`, `git clone` from the lane, and the lane's own `--selftest`).

## 7. Verdict

**Mutant:** excerpt rule deleted from `classify()` (fresh / else drifted).
**Expected detector:** frozen `count-c1.py` blind arm, 8 truth-`excerpt` rows.
**Observed:** exit 1, `C1=unmet`, `mismatches=8`, all `tool=drifted truth=excerpt`;
baseline pristine exit 0 (`C1=met`, mismatches=0) on the same rev.

VERDICT: **PASS** (no defect found — the frozen C1 counter reliably kills the
excerpt-rule deletion; it does so through the blind arm, and the real arm at `bf0df77`
contains no excerpt rows to corroborate it).

**Attacks:** C1 byte-behavior receipt (`evidence/c1-after.txt`) via the
`tools/mori-source-drift.py:148-154` excerpt branch.
