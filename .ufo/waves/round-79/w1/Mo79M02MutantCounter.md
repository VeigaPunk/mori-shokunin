# C2 counter mutation probe — Mo79M02MutantCounter

Axes: operability (detector execution), calibration (weakening detection), freshness (pinned entering revision and manifest bytes).

## 1. Method and byte controls
Only isolated copies changed; the lane counter and fleet manifest were read-only. Six independent single-point mutants ran sequentially. Every mutant used the same selftest detector on pristine, mutated, and restored bytes. The real-read command pins the entering revision; the fleet manifest is snapshotted once to prevent concurrent fleet changes affecting comparisons.
Counter SHA256: `fed9a8292158b6d69e9d786d48fcbed02cb30772b5a5cb4e0386d0b034472290`.
Manifest snapshot SHA256: `86a82240bbb183b17811b9974de1cad83bd9c58a9b2f84a2a4b310a9d373f1b7`.
Fixture commits use core.hooksPath pointing to a pre-commit containment assertion: `D=$(pwd -P); TOP=$(git -C "$D" rev-parse --show-toplevel); [ "$TOP" = "$D" ]`, additionally requiring D under this seat scratch. No lane/fleet git mutation, installs, network or host-state changes.

## 2. Commands and actual outputs

Run-start: `2026-11-04T05:37:16.357833+00:00`
```text
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter/counter.py 84c6cbc3b47c536a504aaee329c77897d389935e --repo /home/vgpnk/Projects/shokunin/mori-shokunin --manifest /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter/manifest.json --scratch /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter
axis coverage cell=round_47_improved expect=round_56_improved state=mismatch
axis operability cell=round_51_improved expect=round_78_improved state=mismatch
axis depth cell=round_51_improved expect=round_76_improved state=mismatch
axis freshness cell=round_28_improved expect=round_78_improved state=mismatch
axis calibration cell=round_50_improved expect=round_78_improved state=mismatch
axis adjacency cell=round_19_improved expect=round_19_improved state=ok
C2=unmet axes=6 mismatches=5 errors=0 rows=46 through=78 rev=84c6cbc3b47c
stderr=''
rc=1
```

### M1
```diff
--- pristine
+++ M1
@@ -79,3 +79,3 @@
     for r in data.get("rounds") or []:
-        if r.get("lane") != LANE or not r.get("admitted"):
+        if r.get("lane") != LANE:
             continue
```

Run-start: `2026-11-04T05:37:16.398652+00:00`
```text
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter/m1.py --scratch /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter --selftest
PASS conformant_met met=True
PASS stale_cell_unmet met=False
PASS verdict_word_missing_unmet met=False
PASS subsumed_by_higher_round_unmet met=False
C2_COUNTER_SELFTEST pass=4 fail=0
stderr=''
rc=0
```

Run-start: `2026-11-04T05:37:16.455433+00:00`
```text
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter/m1.py --scratch /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter --selftest
PASS conformant_met met=True
PASS stale_cell_unmet met=False
PASS verdict_word_missing_unmet met=False
PASS subsumed_by_higher_round_unmet met=False
C2_COUNTER_SELFTEST pass=4 fail=0
stderr=''
rc=0
```

Run-start: `2026-11-04T05:37:16.510429+00:00`
```text
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter/m1.py 84c6cbc3b47c536a504aaee329c77897d389935e --repo /home/vgpnk/Projects/shokunin/mori-shokunin --manifest /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter/manifest.json --scratch /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter
axis coverage cell=round_47_improved expect=round_56_improved state=mismatch
axis operability cell=round_51_improved expect=round_78_improved state=mismatch
axis depth cell=round_51_improved expect=round_77_improved state=mismatch
axis freshness cell=round_28_improved expect=round_78_improved state=mismatch
axis calibration cell=round_50_improved expect=round_78_improved state=mismatch
axis adjacency cell=round_19_improved expect=round_19_improved state=ok
C2=unmet axes=6 mismatches=5 errors=0 rows=67 through=78 rev=84c6cbc3b47c
stderr=''
rc=1
```

Run-start: `2026-11-04T05:37:16.550938+00:00`
```text
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter/m1.py --scratch /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter --selftest
PASS conformant_met met=True
PASS stale_cell_unmet met=False
PASS verdict_word_missing_unmet met=False
PASS subsumed_by_higher_round_unmet met=False
C2_COUNTER_SELFTEST pass=4 fail=0
stderr=''
rc=0
```

### M2
```diff
--- pristine
+++ M2
@@ -82,3 +82,3 @@
         rn = r.get("round")
-        if not isinstance(rn, int) or rn > through:
+        if not isinstance(rn, int) or rn > 1000000:
             continue
```

Run-start: `2026-11-04T05:37:16.616459+00:00`
```text
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter/m2.py --scratch /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter --selftest
PASS conformant_met met=True
PASS stale_cell_unmet met=False
PASS verdict_word_missing_unmet met=False
PASS subsumed_by_higher_round_unmet met=False
C2_COUNTER_SELFTEST pass=4 fail=0
stderr=''
rc=0
```

Run-start: `2026-11-04T05:37:16.675214+00:00`
```text
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter/m2.py --scratch /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter --selftest
FAIL conformant_met want_met=True got={'met': False, 'items': [('coverage', 'round_78_improved', 'round_78_improved', 'ok'), ('operability', 'round_78_improved', 'round_78_improved', 'ok'), ('depth', 'round_78_improved', 'round_90_improved', 'mismatch'), ('freshness', 'round_78_improved', 'round_78_improved', 'ok'), ('calibration', 'round_78_improved', 'round_78_improved', 'ok'), ('adjacency', 'round_19_improved', 'round_19_improved', 'ok')], 'mismatches': 1, 'errors': 0, 'rows': 3} 
PASS stale_cell_unmet met=False
PASS verdict_word_missing_unmet met=False
PASS subsumed_by_higher_round_unmet met=False
C2_COUNTER_SELFTEST pass=3 fail=1
stderr=''
rc=1
```

Run-start: `2026-11-04T05:37:16.741230+00:00`
```text
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter/m2.py --scratch /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter --selftest
PASS conformant_met met=True
PASS stale_cell_unmet met=False
PASS verdict_word_missing_unmet met=False
PASS subsumed_by_higher_round_unmet met=False
C2_COUNTER_SELFTEST pass=4 fail=0
stderr=''
rc=0
```

### M3
```diff
--- pristine
+++ M3
@@ -86,3 +86,3 @@
         for axis, verdict in (r.get("verdicts") or {}).items():
-            if axis in AXES and verdict in ("improved", "harmed"):
+            if axis in AXES and verdict in ("improved", "harmed", "unchanged", "unprovable"):
                 if axis not in last or rn > last[axis][0]:
```

Run-start: `2026-11-04T05:37:16.806001+00:00`
```text
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter/m3.py --scratch /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter --selftest
PASS conformant_met met=True
PASS stale_cell_unmet met=False
PASS verdict_word_missing_unmet met=False
PASS subsumed_by_higher_round_unmet met=False
C2_COUNTER_SELFTEST pass=4 fail=0
stderr=''
rc=0
```

Run-start: `2026-11-04T05:37:16.866531+00:00`
```text
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter/m3.py --scratch /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter --selftest
FAIL conformant_met want_met=True got={'met': False, 'items': [('coverage', 'round_78_improved', 'round_78_improved', 'ok'), ('operability', 'round_78_improved', 'round_78_improved', 'ok'), ('depth', 'round_78_improved', 'round_78_improved', 'ok'), ('freshness', 'round_78_improved', 'round_78_improved', 'ok'), ('calibration', 'round_78_improved', 'round_78_improved', 'ok'), ('adjacency', 'round_19_improved', 'round_78_unchanged', 'mismatch')], 'mismatches': 1, 'errors': 0, 'rows': 2} 
PASS stale_cell_unmet met=False
PASS verdict_word_missing_unmet met=False
PASS subsumed_by_higher_round_unmet met=False
C2_COUNTER_SELFTEST pass=3 fail=1
stderr=''
rc=1
```

Run-start: `2026-11-04T05:37:16.922054+00:00`
```text
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter/m3.py --scratch /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter --selftest
PASS conformant_met met=True
PASS stale_cell_unmet met=False
PASS verdict_word_missing_unmet met=False
PASS subsumed_by_higher_round_unmet met=False
C2_COUNTER_SELFTEST pass=4 fail=0
stderr=''
rc=0
```

### M4
```diff
--- pristine
+++ M4
@@ -110,3 +110,3 @@
         got_n = int(m.group(1))
-        tail = cell[m.end():].split(";")[0]
+        tail = cell[m.end():]
         vm = VERDICT.search(tail)
```

Run-start: `2026-11-04T05:37:16.984765+00:00`
```text
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter/m4.py --scratch /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter --selftest
PASS conformant_met met=True
PASS stale_cell_unmet met=False
PASS verdict_word_missing_unmet met=False
PASS subsumed_by_higher_round_unmet met=False
C2_COUNTER_SELFTEST pass=4 fail=0
stderr=''
rc=0
```

Run-start: `2026-11-04T05:37:17.042566+00:00`
```text
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter/m4.py --scratch /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter --selftest
PASS conformant_met met=True
PASS stale_cell_unmet met=False
PASS verdict_word_missing_unmet met=False
PASS subsumed_by_higher_round_unmet met=False
C2_COUNTER_SELFTEST pass=4 fail=0
stderr=''
rc=0
```

Run-start: `2026-11-04T05:37:17.098261+00:00`
```text
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter/m4.py 84c6cbc3b47c536a504aaee329c77897d389935e --repo /home/vgpnk/Projects/shokunin/mori-shokunin --manifest /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter/manifest.json --scratch /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter
axis coverage cell=round_47_improved expect=round_56_improved state=mismatch
axis operability cell=round_51_improved expect=round_78_improved state=mismatch
axis depth cell=round_51_improved expect=round_76_improved state=mismatch
axis freshness cell=round_28_improved expect=round_78_improved state=mismatch
axis calibration cell=round_50_improved expect=round_78_improved state=mismatch
axis adjacency cell=round_19_improved expect=round_19_improved state=ok
C2=unmet axes=6 mismatches=5 errors=0 rows=46 through=78 rev=84c6cbc3b47c
stderr=''
rc=1
```

Run-start: `2026-11-04T05:37:17.137444+00:00`
```text
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter/m4.py --scratch /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter --selftest
PASS conformant_met met=True
PASS stale_cell_unmet met=False
PASS verdict_word_missing_unmet met=False
PASS subsumed_by_higher_round_unmet met=False
C2_COUNTER_SELFTEST pass=4 fail=0
stderr=''
rc=0
```

### M5
```diff
--- pristine
+++ M5
@@ -103,3 +103,3 @@
             continue
-        m = ROUND.search(cell)
+        m = next((candidate for candidate in ROUND.finditer(cell) if want and int(candidate.group(1)) == want[0]), ROUND.search(cell))
         if not m:
```

Run-start: `2026-11-04T05:37:17.193379+00:00`
```text
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter/m5.py --scratch /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter --selftest
PASS conformant_met met=True
PASS stale_cell_unmet met=False
PASS verdict_word_missing_unmet met=False
PASS subsumed_by_higher_round_unmet met=False
C2_COUNTER_SELFTEST pass=4 fail=0
stderr=''
rc=0
```

Run-start: `2026-11-04T05:37:17.249007+00:00`
```text
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter/m5.py --scratch /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter --selftest
PASS conformant_met met=True
PASS stale_cell_unmet met=False
PASS verdict_word_missing_unmet met=False
PASS subsumed_by_higher_round_unmet met=False
C2_COUNTER_SELFTEST pass=4 fail=0
stderr=''
rc=0
```

Run-start: `2026-11-04T05:37:17.303343+00:00`
```text
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter/m5.py 84c6cbc3b47c536a504aaee329c77897d389935e --repo /home/vgpnk/Projects/shokunin/mori-shokunin --manifest /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter/manifest.json --scratch /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter
axis coverage cell=round_47_improved expect=round_56_improved state=mismatch
axis operability cell=round_51_improved expect=round_78_improved state=mismatch
axis depth cell=round_51_improved expect=round_76_improved state=mismatch
axis freshness cell=round_28_improved expect=round_78_improved state=mismatch
axis calibration cell=round_50_improved expect=round_78_improved state=mismatch
axis adjacency cell=round_19_improved expect=round_19_improved state=ok
C2=unmet axes=6 mismatches=5 errors=0 rows=46 through=78 rev=84c6cbc3b47c
stderr=''
rc=1
```

Run-start: `2026-11-04T05:37:17.343219+00:00`
```text
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter/m5.py --scratch /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter --selftest
PASS conformant_met met=True
PASS stale_cell_unmet met=False
PASS verdict_word_missing_unmet met=False
PASS subsumed_by_higher_round_unmet met=False
C2_COUNTER_SELFTEST pass=4 fail=0
stderr=''
rc=0
```

### M6
```diff
--- pristine
+++ M6
@@ -121,3 +121,3 @@
         items.append((axis, f"round_{got_n}_{got_v}", f"round_{want[0]}_{want[1]}", state))
-    met = mismatches == 0 and errors == 0
+    met = errors == 0
     return {"met": met, "items": items, "mismatches": mismatches, "errors": errors,
```

Run-start: `2026-11-04T05:37:17.400965+00:00`
```text
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter/m6.py --scratch /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter --selftest
PASS conformant_met met=True
PASS stale_cell_unmet met=False
PASS verdict_word_missing_unmet met=False
PASS subsumed_by_higher_round_unmet met=False
C2_COUNTER_SELFTEST pass=4 fail=0
stderr=''
rc=0
```

Run-start: `2026-11-04T05:37:17.457040+00:00`
```text
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter/m6.py --scratch /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter --selftest
PASS conformant_met met=True
FAIL stale_cell_unmet want_met=False got={'met': True, 'items': [('coverage', 'round_47_improved', 'round_78_improved', 'mismatch'), ('operability', 'round_78_improved', 'round_78_improved', 'ok'), ('depth', 'round_78_improved', 'round_78_improved', 'ok'), ('freshness', 'round_78_improved', 'round_78_improved', 'ok'), ('calibration', 'round_78_improved', 'round_78_improved', 'ok'), ('adjacency', 'round_19_improved', 'round_19_improved', 'ok')], 'mismatches': 1, 'errors': 0, 'rows': 2} 
FAIL verdict_word_missing_unmet want_met=False got={'met': True, 'items': [('coverage', 'round_78_improved', 'round_78_improved', 'ok'), ('operability', 'round_78_improved', 'round_78_improved', 'ok'), ('depth', 'round_78_none', 'round_78_improved', 'mismatch'), ('freshness', 'round_78_improved', 'round_78_improved', 'ok'), ('calibration', 'round_78_improved', 'round_78_improved', 'ok'), ('adjacency', 'round_19_improved', 'round_19_improved', 'ok')], 'mismatches': 1, 'errors': 0, 'rows': 2} 
FAIL subsumed_by_higher_round_unmet want_met=False got={'met': True, 'items': [('coverage', 'round_78_improved', 'round_78_improved', 'ok'), ('operability', 'round_40_improved', 'round_78_improved', 'mismatch'), ('depth', 'round_78_improved', 'round_78_improved', 'ok'), ('freshness', 'round_78_improved', 'round_78_improved', 'ok'), ('calibration', 'round_78_improved', 'round_78_improved', 'ok'), ('adjacency', 'round_19_improved', 'round_19_improved', 'ok')], 'mismatches': 1, 'errors': 0, 'rows': 2} 
C2_COUNTER_SELFTEST pass=1 fail=3
stderr=''
rc=1
```

Run-start: `2026-11-04T05:37:17.512869+00:00`
```text
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter/m6.py --scratch /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter --selftest
PASS conformant_met met=True
PASS stale_cell_unmet met=False
PASS verdict_word_missing_unmet met=False
PASS subsumed_by_higher_round_unmet met=False
C2_COUNTER_SELFTEST pass=4 fail=0
stderr=''
rc=0
```

## 3. Mutant table
| Mutant | Selftest | Verdict | Mutated SHA256 | Restored SHA256 |
|---|---|---|---|---|
| M1 | `C2_COUNTER_SELFTEST pass=4 fail=0` | SURVIVED | `356ec6f1854b04caaed632e0a5f8e6d4edb9141fda443b94dc1366872115debd` | `fed9a8292158b6d69e9d786d48fcbed02cb30772b5a5cb4e0386d0b034472290` |
| M2 | `C2_COUNTER_SELFTEST pass=3 fail=1` | KILLED | `30c24c0830c4317d2d48e4c96b8ea6804c752c44f2a24c17e211aeff4ae8dfa0` | `fed9a8292158b6d69e9d786d48fcbed02cb30772b5a5cb4e0386d0b034472290` |
| M3 | `C2_COUNTER_SELFTEST pass=3 fail=1` | KILLED | `54a182d77963343c8ff7d25d04fdbff74d80acf16c74f450f9e69f6f78b0fea3` | `fed9a8292158b6d69e9d786d48fcbed02cb30772b5a5cb4e0386d0b034472290` |
| M4 | `C2_COUNTER_SELFTEST pass=4 fail=0` | SURVIVED | `de742c4055210d249268e6d4c440cf41b4b2ae3dfe2fff4e44d69fea23b97418` | `fed9a8292158b6d69e9d786d48fcbed02cb30772b5a5cb4e0386d0b034472290` |
| M5 | `C2_COUNTER_SELFTEST pass=4 fail=0` | SURVIVED | `c7e389973f4810dc4abce5ffa8770267fc6f39d19f3d42b560155c083145a085` | `fed9a8292158b6d69e9d786d48fcbed02cb30772b5a5cb4e0386d0b034472290` |
| M6 | `C2_COUNTER_SELFTEST pass=1 fail=3` | KILLED | `1dabafbd658a567d6cc7f26a18ac257164f7bbd1fa5f84a72b14e628c896bb00` | `fed9a8292158b6d69e9d786d48fcbed02cb30772b5a5cb4e0386d0b034472290` |

## 4. Surviving-mutant analysis
M1 removes admission filtering; its excluded selftest row is round 95, already excluded by the independent round ceiling. Missing arm: a non-admitted row at or below 78 that supersedes an admitted improvement.
M4 searches past semicolon. Missing arm: first clause with correct round but no verdict, with the required verdict only in a later clause.
M5 chooses a matching round anywhere rather than the first. Missing arm: stale leading round followed by the expected round and verdict in a later clause.
Actual real-read comparisons below determine which survivors change the entering measurement; an unchanged live reading does not establish equivalence.
M1: baseline final line `C2=unmet axes=6 mismatches=5 errors=0 rows=46 through=78 rev=84c6cbc3b47c`; mutant final line `C2=unmet axes=6 mismatches=5 errors=0 rows=67 through=78 rev=84c6cbc3b47c`.
M4: baseline final line `C2=unmet axes=6 mismatches=5 errors=0 rows=46 through=78 rev=84c6cbc3b47c`; mutant final line `C2=unmet axes=6 mismatches=5 errors=0 rows=46 through=78 rev=84c6cbc3b47c`.
M5: baseline final line `C2=unmet axes=6 mismatches=5 errors=0 rows=46 through=78 rev=84c6cbc3b47c`; mutant final line `C2=unmet axes=6 mismatches=5 errors=0 rows=46 through=78 rev=84c6cbc3b47c`.

All three survivors leave the real entering mismatch count at 5 (delta 0). M1 nevertheless changes the real depth expectation from round 76 to round 77 and manifest_rows from 46 to 67; the live axis outputs above expose an admission-filter hole even though the stale cell remains a mismatch. M4 and M5 leave the displayed real axis readings unchanged. Missing arms above are coverage findings, not proposed changes to the frozen predicate.

## 5. Restoration, limitations, own defects
Each pristine and restored selftest produced `C2_COUNTER_SELFTEST pass=4 fail=0`, rc 0 (full per-run output above). All six restored hashes match the pristine counter. Lane source SHA256 after probe: `fed9a8292158b6d69e9d786d48fcbed02cb30772b5a5cb4e0386d0b034472290`.
Fixture containment assertions recorded: 72. Each successful fixture commit was preceded by the hook assertion; no assertion failure occurred.
Own defects: initial source read was declaration-only and a subsequent ranged read stopped before main; caught by the elision footer and remedied by reading the omitted ranges before mutation. Initial commentary was unnecessarily verbose. No implementation remediation was attempted.
Limit: manifest is the observed fleet snapshot, not a historical manifest reconstructed at the entering lane commit. Tests exercise the frozen counter selftest and survivor entering reads only; no full lane suite run.
Cleanup defect caught and fixed: the first `test ! -e /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter && printf 'SCRATCH_CLEANUP absent rc=0\n'` returned rc 1, no stdout: the enclosing persistent shell had not exited, so its EXIT trap had not fired. Ran `rm -rf -- /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter && test ! -e /fast/scratch/hyaku/mori-r79/Mo79M02MutantCounter && printf 'SCRATCH_CLEANUP absent rc=0\n'`; actual output `SCRATCH_CLEANUP absent rc=0`, rc 0. No scratch tree remains.

Self-evaluation: accuracy 4/5 (live manifest is a snapshot, not historical fleet bytes); completeness 5/5 (six prescribed mutations and all survivor reads); clarity 4/5 (full outputs increase length); actionability 5/5 (missing arms named); conciseness 4/5 (restoration triplets intentionally repetitive). Overall 4.4/5. Would the user agree? Evidence is explicit; no survivor is treated as equivalent merely because its live count holds.
