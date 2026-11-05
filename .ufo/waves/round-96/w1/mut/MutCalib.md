# MutCalib — mutation probe of the frozen round-79 C2 counter selftest (mori r96 w1)

- Seat: MutCalib (mutation tester), 2026-11-05. Lane: /home/vgpnk/Projects/shokunin/mori-shokunin.
- Entering lane HEAD: `66c5518e239eeacd6070be26d78085ef702392cb`. Observed `git -C <lane> rev-parse HEAD` during the probe: `b88c8ae8ff85d1cb7df81fffef2f46a0512e76b5` (observation only; no action taken, no remediation).
- Subject (calibration instrument, frozen, never edited): `.ufo/waves/round-79/count-c2.py`, extracted exactly as `git -C <lane> show 66c5518e…:.ufo/waves/round-79/count-c2.py` → `$S/base.py`, sha256 `4f6c5c251af954f658504da49f69a90dcc0171b7b6c952657bcc19a75e92fe47` (identical to the working-tree file).
- Scratch: `$S=/fast/scratch/hyaku/mori-r96/MutCalib`, `TMPDIR=$S`, `HYAKU_SCRATCH=$S`; removed at end (explicit `rm -rf`, trap-equivalent). Only writes outside `$S`: this report (and its template-path copy).

## Method

Six single-change mutants, each disabling exactly one predicate element; each verified `diff -u base.py mN.py` = one `-`/one `+` line (2 changed lines):

| Mutant | Element mutated | Change |
|---|---|---|
| M1 | admitted filter (`expectations`) | `if r.get("lane") != LANE or not r.get("admitted"):` → `if r.get("lane") != LANE:` |
| M2 | max-round tie-break (`expectations`) | `rn > last[axis][0]` → `rn < last[axis][0]` (MIN instead of MAX) |
| M3 | verdict-word filter (`expectations`) | `verdict in ("improved", "harmed")` → `verdict in ("harmed",)` |
| M4 | through bound (`expectations`) | `if not isinstance(rn, int) or rn > through:` → `if not isinstance(rn, int):` |
| M5 | cell verdict regex (`VERDICT`) | `re.compile(r"\b(improved\|harmed)\b")` → `re.compile(r"\b(\w+)\b")` (any word accepted) |
| M6 | adjacency axis (`grade` loop) | `for axis in AXES:` → `for axis in AXES[:-1]:` (adjacency is last; no longer graded) |

Commands run per file (base + m1..m6), all read-only against the lane and fleet manifest:

```
python3 <file> --selftest --scratch $S/st        # TMPDIR/HYAKU_SCRATCH = $S
python3 <file> 66c5518e239eeacd6070be26d78085ef702392cb --repo /home/vgpnk/Projects/shokunin/mori-shokunin --through 95 --manifest /home/vgpnk/Projects/shokunin/MANIFEST.json
```

Disclosure: the task command omitted `--repo`. A scratch copy cannot derive the repo from `__file__` (the default resolves `../../..` from the script path → `/fast`), so `--repo <lane>` was added to every run including base. Same predicate, same rev, same manifest; the addition is required for the scratch copy to address the lane at all.

## Baseline validity (detector)

- `base.py --selftest`: rc=0, `C2_COUNTER_SELFTEST pass=7 fail=0` (all 7 cases PASS). Detector valid.
- `base.py 66c5518e… --through 95 --manifest /home/vgpnk/Projects/shokunin/MANIFEST.json`: rc=1,
  `C2=unmet axes=6 mismatches=5 errors=0 rows=58 through=95 rev=66c5518e239e`
  — reproduces C1's "before = 5 mismatches at 66c5518e (through=95)". Per-axis detail:
  ```
  axis coverage cell=round_56_improved expect=round_80_improved state=mismatch
  axis operability cell=round_78_improved expect=round_93_improved state=mismatch
  axis depth cell=round_76_improved expect=round_86_improved state=mismatch
  axis freshness cell=round_78_improved expect=round_82_improved state=mismatch
  axis calibration cell=round_78_improved expect=round_93_improved state=mismatch
  axis adjacency cell=round_19_improved expect=round_19_improved state=ok
  ```

## Result table

| Mutant | selftest rc | selftest tally | through-95 verdict (C2 line, rc) | killed-by-selftest |
|---|---|---|---|---|
| base | 0 | `pass=7 fail=0` | unmet, rc=1; `mismatches=5 errors=0 rows=58` | — (baseline valid) |
| M1 drop admitted filter | 1 | `pass=6 fail=1` (FAIL nonadmitted_below_ceiling_ignored_met) | unmet, rc=1; `mismatches=5 errors=0 rows=85` (rows 58→85: 27 non-admitted mori rounds now count) | **yes** |
| M2 MIN instead of MAX | 0 | `pass=7 fail=0` | unmet, rc=1; `mismatches=6 errors=0 rows=58` (one more axis mismatch) | **no — survives** |
| M3 harmed only | 1 | `pass=5 fail=2` (FAIL conformant_met, FAIL nonadmitted_below_ceiling_ignored_met; expectations empty → `no_manifest_row` errors) | unmet, rc=1; `mismatches=0 errors=6 rows=58` | **yes** |
| M4 remove `rn > through` | 1 | `pass=5 fail=2` (FAIL conformant_met, FAIL nonadmitted_below_ceiling_ignored_met; depth expectation jumps to round_90) | unmet, rc=1; `mismatches=5 errors=0 rows=58` — C2 line identical to base on today's data | **yes** |
| M5 any verdict word | 0 | `pass=7 fail=0` | unmet, rc=1; `mismatches=5 errors=0 rows=58` — C2 line identical to base | **no — survives** |
| M6 skip adjacency | 0 | `pass=7 fail=0` | unmet, rc=1; `mismatches=5 errors=0 rows=58` — C2 line identical to base (adjacency was `ok`, and `axes=6` prints `len(AXES)`, unchanged) | **no — survives** |

Every through-95 verdict stayed `unmet` for all six mutants; the mutant-killing signal lives entirely in the selftest, which has the three gaps below.

## Survivors — what the frozen selftest does NOT kill, and why

- **M2 (min vs max):** no selftest fixture ever holds two admitted, in-through, verdict-bearing entries for the same axis at different rounds. In `nonadmitted_below_ceiling_ignored_met` the shared rounds have coverage stripped and only `(60, False, …)` + `(47, True, …)` are added, leaving exactly one eligible coverage round; with one candidate per axis, MIN == MAX, so the tie-break direction is unobservable. Live-data symptom only: mismatches 5→6.
- **M5 (any verdict word):** every negative-case cell that lacks the true verdict word still carries another parenthetical word (e.g. `round 78 (score held)`), which the widened `\b(\w+)\b` accepts but which still ≠ the expected word → identical mismatch either way; every positive-case parenthetical begins with the expected word, which the widened regex also matches. No case distinguishes "no accepted verdict word" from "any word accepted". No live-data symptom at this rev.
- **M6 (skip adjacency):** adjacency is never planted as a wrong cell in any of the 7 cases — `good["adjacency"]` is pinned to the conformant `round 19 (improved, score held)` and no negative case mutates it — so removing adjacency from the graded loop changes no expected outcome. (`axes=6` in the C2 line is the constant `len(AXES)`, so even the output shape is unchanged.) No live-data symptom at this rev because adjacency's own comparison was `ok`.

These are coverage findings in the calibration instrument, not defects in the frozen contract; no counter, SCORECARD, MANIFEST, or contract file was changed.

## Diffs (verbatim, minimal — 2 changed lines each)

```diff
--- base.py  (m1: drop admitted filter)
@@ -77,7 +77,7 @@
     last = {}
     rows = 0
     for r in data.get("rounds") or []:
-        if r.get("lane") != LANE or not r.get("admitted"):
+        if r.get("lane") != LANE:
             continue
         rn = r.get("round")
         if not isinstance(rn, int) or rn > through:
```

```diff
--- base.py  (m2: MIN instead of MAX)
@@ -85,7 +85,7 @@
         rows += 1
         for axis, verdict in (r.get("verdicts") or {}).items():
             if axis in AXES and verdict in ("improved", "harmed"):
-                if axis not in last or rn > last[axis][0]:
+                if axis not in last or rn < last[axis][0]:
                     last[axis] = (rn, verdict)
     return last, rows
```

```diff
--- base.py  (m3: harmed only)
@@ -84,7 +84,7 @@
             continue
         rows += 1
         for axis, verdict in (r.get("verdicts") or {}).items():
-            if axis in AXES and verdict in ("improved", "harmed"):
+            if axis in AXES and verdict in ("harmed",):
                 if axis not in last or rn > last[axis][0]:
                     last[axis] = (rn, verdict)
     return last, rows
```

```diff
--- base.py  (m4: remove through bound)
@@ -80,7 +80,7 @@
         if r.get("lane") != LANE or not r.get("admitted"):
             continue
         rn = r.get("round")
-        if not isinstance(rn, int) or rn > through:
+        if not isinstance(rn, int):
             continue
         rows += 1
         for axis, verdict in (r.get("verdicts") or {}).items():
```

```diff
--- base.py  (m5: any verdict word)
@@ -32,7 +32,7 @@
 LANE = "mori"
 THROUGH = 78
 ROUND = re.compile(r"round\s+(\d+)", re.I)
-VERDICT = re.compile(r"\b(improved|harmed)\b")
+VERDICT = re.compile(r"\b(\w+)\b")
```

```diff
--- base.py  (m6: skip adjacency)
@@ -94,7 +94,7 @@
     cells = axes_cells(text)
     last, rows = expectations(manifest, through)
     items, mismatches, errors = [], 0, 0
-    for axis in AXES:
+    for axis in AXES[:-1]:
         cell, err = cells.get(axis, (None, "missing_row"))
```

## Hashes and restoration evidence

- `$S/base.py` sha256 `4f6c5c251af954f658504da49f69a90dcc0171b7b6c952657bcc19a75e92fe47` before and after the battery (unchanged; equals the `git show` blob of the frozen rev and the working-tree counter).
- Mutant sha256: m1 `7584d2d8…`, m2 `b69a453f…`, m3 `493d74ff…`, m4 `ed976148…`, m5 `baf5d771…`, m6 `08ccd951…` (full values recorded in scratch receipts; diffs above are the authoritative minimal-change evidence).
- Working-tree counter `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-79/count-c2.py` sha256 `4f6c5c25…` measured before the probe and again after — identical. The lane source was never modified; the scratch copy is disposable and was deleted with `$S`.
- Direct git usage: `git show` and `git rev-parse` only, read-only, `-C` absolute lane path. The instrument's own `--selftest` creates and commits throwaway git fixtures inside its scratch tempdir under `$S` (task-sanctioned; nothing outside `$S`).

## Tooling installs

None. No tool installed or upgraded (python3 and diff were sufficient). pacman not used.

## Unrun checks (named)

- `--selftest` case-level stdout for mutants other than M1/M3/M4's FAIL lines was captured but only tallies are tabulated above (full stdout kept in scratch, now deleted — FAIL lines quoted are verbatim).
- Did not run the counter at its default `--through 78` against `66c5518e…` (C1's "reads met" re-confirmation was not part of this probe).
- Did not run any mutant at `--through` values other than 95.
- Did not run the mutants against any rev other than `66c5518e…`.
- Did not independently enumerate MANIFEST.json rows to attribute the 5 (or 6, under M2) mismatching axes beyond the counter's own per-axis output.
- Did not run sibling seats' detectors (e.g. the C2 source-digest freshness check) — outside this probe.
