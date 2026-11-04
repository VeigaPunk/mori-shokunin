# Mo80M01Mutant — round 80 w1 mutation findings

**Snapshot limit:** after this probe and scratch cleanup, the sweep executor reported adding wildcard citation resolution and two selftest cases (declared 27 rather than the tested 25). This report's C1 results bind only tested SHA-256 `a481cd28371273d899cbbbe52322c1a1f545cfdead8a6a600abfa884222abe99`; the newer sweep was not executed by this seat. Carry the survivor as a historical coverage finding, not a measured verdict on the superseding bytes.

The C2 executor subsequently reported correcting the masked arm by initializing untouched cells from their first clauses. C2 harness/direct-mutant results here likewise bind only pre-correction SHA-256 `8d7fae146589341368399b490ae7c5b4bd55ee9d25496202ca8e0f7e010f1d69` and scratch commit `3bd601d9087d2d3e2d819714c6c5658a77567c5f`. The corrected counter was not exercised; neither executor update invalidates the recorded historical outputs.

Axes: calibration, operability, coverage. Detection/report only; no lane implementation, frozen counter, contract, or predicate changed.
## 1. Method and observed result
Copied each target into `/fast/scratch/hyaku/mori-r80/Mo80M01Mutant/<mutant>/`, applied exactly one replacement, ran the same bounded `python3 -I <copy> --selftest --scratch <mutant-dir>` detector on pristine/mutated/restored bytes (90-second subprocess deadline). Each original byte string was restored in `finally` before its restored run. Environment: TMPDIR and HYAKU_SCRATCH equal the seat scratch root; cwd is that root. A scratch-only git wrapper asserts `rev-parse --show-toplevel == -C` and the seat-root prefix before every fixture add/commit; fixtures use user.name=t and user.email=t@t. The sweep returns immediately at --selftest, so trailing --scratch has no effect there; it uses in-memory fixtures.
The sweep was absent on the first absolute read, then landed before its probes. No target was skipped. Baseline and restoration detectors all exited 0; no inconclusive mutant. Observed: C1 killed 5/6, C3 killed 1/3; frozen C2 harness killed 6/6. Three survivors route to round 81, without changing this round’s predicate.
## 2. Mutant table

| Target | Mutant (exact hunk below) | Pristine rc | Mutated rc | Restored rc | Verdict |
|---|---|---:|---:|---:|---|
| `tools/mori-claim-sweep.py` | C1a_drop_line_suffix | 0 | 1 | 0 | KILLED |
| `tools/mori-claim-sweep.py` | C1b_drop_revision_suffix | 0 | 1 | 0 | KILLED |
| `tools/mori-claim-sweep.py` | C1c_fence_noop | 0 | 1 | 0 | KILLED |
| `tools/mori-claim-sweep.py` | C1d_tally_at_least | 0 | 1 | 0 | KILLED |
| `tools/mori-claim-sweep.py` | C1e_missing_carrier_empty | 0 | 1 | 0 | KILLED |
| `tools/mori-claim-sweep.py` | C1f_count_unresolved_only | 0 | 0 | 0 | SURVIVED |
| `.ufo/waves/round-79/count-c2.py` | C2_any_round_in_cell | 0 | 1 | 0 | KILLED |
| `.ufo/waves/round-79/count-c2.py` | C2_count_other_verdicts | 0 | 1 | 0 | KILLED |
| `.ufo/waves/round-79/count-c2.py` | C2_cut_clause_boundary | 0 | 1 | 0 | KILLED |
| `.ufo/waves/round-79/count-c2.py` | C2_drop_admitted | 0 | 1 | 0 | KILLED |
| `.ufo/waves/round-79/count-c2.py` | C2_met_ignores_mismatch | 0 | 1 | 0 | KILLED |
| `.ufo/waves/round-79/count-c2.py` | C2_raise_ceiling | 0 | 1 | 0 | KILLED |
| `.ufo/waves/round-80/count-c3.py` | C3a_drop_sibling | 0 | 0 | 0 | SURVIVED |
| `.ufo/waves/round-80/count-c3.py` | C3b_allow_extra | 0 | 1 | 0 | KILLED |
| `.ufo/waves/round-80/count-c3.py` | C3c_count_directories | 0 | 0 | 0 | SURVIVED |

## 3. Commands, exact hunks and actual output

All stderr was empty for the 45 direct detector runs. Baseline/restored stdout was byte-identical for each mutant; full representative outputs per target follow.
### Baseline/restored: `tools/mori-claim-sweep.py`
```text
$ python3 -I /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C1a_drop_line_suffix/mori-claim-sweep.py --selftest --scratch /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C1a_drop_line_suffix
case clean fixture tree pass
case stale present pass
case stale absent pass
case tally equal pass
case tally mismatch pass
case dead pointer pass
case live line suffix pass
case live revision suffix pass
case fenced token ignored pass
case sibling ignored pass
case unreadable carrier pass
case missing pins pass
case malformed pins pass
case capability table pass
case checklist command pass
case ungraded prose ignored pass
case multiple stale occurrences pass
case grammar 'pass=19 fail=0' pass
case grammar 'PASS (12 cases)' pass
case grammar 'PASS 7/7' pass
case grammar 'pass=3' pass
case grammar 'pass=3 fail=1' pass
case grammar 'PASS 2/3' pass
case grammar 'nothing' pass
case grammar 'pass=3\npass=4' pass
CLAIM_SWEEP_SELFTEST pass=25 fail=0
rc=0
```
### Baseline/restored: `.ufo/waves/round-79/count-c2.py`
```text
$ python3 -I /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C2_drop_admitted/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C2_drop_admitted
PASS conformant_met met=True
PASS stale_cell_unmet met=False
PASS verdict_word_missing_unmet met=False
PASS subsumed_by_higher_round_unmet met=False
PASS nonadmitted_below_ceiling_ignored_met met=True
PASS verdict_after_clause_boundary_unmet met=False
PASS later_round_in_cell_ignored_unmet met=False
C2_COUNTER_SELFTEST pass=7 fail=0
rc=0
```
### Baseline/restored: `.ufo/waves/round-80/count-c3.py`
```text
$ python3 -I /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C3a_drop_sibling/count-c3.py --selftest --scratch /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C3a_drop_sibling
PASS complete named=3 present=3 missing=0 extra=0
PASS missing_one named=2 present=3 missing=1 extra=0
PASS extra_stale named=4 present=3 missing=0 extra=1
C3_COUNTER_SELFTEST pass=3 fail=0
rc=0
```
### C1a_drop_line_suffix — KILLED
```diff
--- pristine
+++ mutant
@@ -90,7 +90,7 @@
             name = match[0]
             # Accept either ordering of the two independently optional suffixes.
             for _ in range(2):
-                name = re.sub(r'(?::\d+(?:-\d+)?|@[0-9a-fA-F]+)$', '', name)
+                name = re.sub(r'@[0-9a-fA-F]+$', '', name)
             if '..' not in Path(name).parts:
                 yield name
```
```text
$ python3 -I /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C1a_drop_line_suffix/mori-claim-sweep.py --selftest --scratch /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C1a_drop_line_suffix
case clean fixture tree pass
case stale present pass
case stale absent pass
case tally equal pass
case tally mismatch pass
case dead pointer pass
case live line suffix FAIL CLAIM_SWEEP_MISMATCH unresolved SCORECARD.md:5 corpus/live.md:12-14
CLAIM_SWEEP mismatches=1 unresolved=1 tallies=0 stale=0 carriers=1 pointers=1
case live revision suffix pass
case fenced token ignored pass
case sibling ignored pass
case unreadable carrier pass
case missing pins pass
case malformed pins pass
case capability table pass
case checklist command pass
case ungraded prose ignored pass
case multiple stale occurrences pass
case grammar 'pass=19 fail=0' pass
case grammar 'PASS (12 cases)' pass
case grammar 'PASS 7/7' pass
case grammar 'pass=3' pass
case grammar 'pass=3 fail=1' pass
case grammar 'PASS 2/3' pass
case grammar 'nothing' pass
case grammar 'pass=3\npass=4' pass
CLAIM_SWEEP_SELFTEST pass=24 fail=1
rc=1
```
Pristine/restored SHA-256: `a481cd28371273d899cbbbe52322c1a1f545cfdead8a6a600abfa884222abe99` / `a481cd28371273d899cbbbe52322c1a1f545cfdead8a6a600abfa884222abe99`; mutated SHA-256: `1ec96f622f0456409001193d321d27914406a6de97d707597fe71158d989f73b`.
### C1b_drop_revision_suffix — KILLED
```diff
--- pristine
+++ mutant
@@ -90,7 +90,7 @@
             name = match[0]
             # Accept either ordering of the two independently optional suffixes.
             for _ in range(2):
-                name = re.sub(r'(?::\d+(?:-\d+)?|@[0-9a-fA-F]+)$', '', name)
+                name = re.sub(r':\d+(?:-\d+)?$', '', name)
             if '..' not in Path(name).parts:
                 yield name
```
```text
$ python3 -I /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C1b_drop_revision_suffix/mori-claim-sweep.py --selftest --scratch /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C1b_drop_revision_suffix
case clean fixture tree pass
case stale present pass
case stale absent pass
case tally equal pass
case tally mismatch pass
case dead pointer pass
case live line suffix pass
case live revision suffix FAIL CLAIM_SWEEP_MISMATCH unresolved SCORECARD.md:5 corpus/live.md@abcdef1
CLAIM_SWEEP mismatches=1 unresolved=1 tallies=0 stale=0 carriers=1 pointers=1
case fenced token ignored pass
case sibling ignored pass
case unreadable carrier pass
case missing pins pass
case malformed pins pass
case capability table pass
case checklist command pass
case ungraded prose ignored pass
case multiple stale occurrences pass
case grammar 'pass=19 fail=0' pass
case grammar 'PASS (12 cases)' pass
case grammar 'PASS 7/7' pass
case grammar 'pass=3' pass
case grammar 'pass=3 fail=1' pass
case grammar 'PASS 2/3' pass
case grammar 'nothing' pass
case grammar 'pass=3\npass=4' pass
CLAIM_SWEEP_SELFTEST pass=24 fail=1
rc=1
```
Pristine/restored SHA-256: `a481cd28371273d899cbbbe52322c1a1f545cfdead8a6a600abfa884222abe99` / `a481cd28371273d899cbbbe52322c1a1f545cfdead8a6a600abfa884222abe99`; mutated SHA-256: `da7f5a5a38c106f691c8111239b9fb7a22b28dc9d3791b9f2b8ef5e304638de1`.
### C1c_fence_noop — KILLED
```diff
--- pristine
+++ mutant
@@ -58,7 +58,7 @@
     axes = False
     table = False
     capability = False
-    for number, line in visible_lines(text):
+    for number, line in enumerate(text.splitlines(), 1):
         if carrier == 'SHONEN.md':
             if re.match(r'^\s*- \[', line):
                 yield number, line
```
```text
$ python3 -I /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C1c_fence_noop/mori-claim-sweep.py --selftest --scratch /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C1c_fence_noop
case clean fixture tree pass
case stale present pass
case stale absent pass
case tally equal pass
case tally mismatch pass
case dead pointer pass
case live line suffix pass
case live revision suffix pass
case fenced token ignored FAIL CLAIM_SWEEP_MISMATCH unresolved SCORECARD.md:6 corpus/dead.md
CLAIM_SWEEP mismatches=1 unresolved=1 tallies=0 stale=0 carriers=1 pointers=1
case sibling ignored pass
case unreadable carrier pass
case missing pins pass
case malformed pins pass
case capability table pass
case checklist command pass
case ungraded prose ignored pass
case multiple stale occurrences pass
case grammar 'pass=19 fail=0' pass
case grammar 'PASS (12 cases)' pass
case grammar 'PASS 7/7' pass
case grammar 'pass=3' pass
case grammar 'pass=3 fail=1' pass
case grammar 'PASS 2/3' pass
case grammar 'nothing' pass
case grammar 'pass=3\npass=4' pass
CLAIM_SWEEP_SELFTEST pass=24 fail=1
rc=1
```
Pristine/restored SHA-256: `a481cd28371273d899cbbbe52322c1a1f545cfdead8a6a600abfa884222abe99` / `a481cd28371273d899cbbbe52322c1a1f545cfdead8a6a600abfa884222abe99`; mutated SHA-256: `bf79e9ed6144e9dcc82626e947149b54781ff05134f5fd9bdfefc10412d9c1ca`.
### C1d_tally_at_least — KILLED
```diff
--- pristine
+++ mutant
@@ -170,7 +170,7 @@
             if not exists(path):
                 raise ValueError('missing pinned tool: ' + name)
             actual = runner(path, root)
-            if actual != expected:
+            if actual < expected:
                 mismatches.append(('tally', str(pins_path), 1,
                                    '%s pinned=%d live=%d' % (name, expected, actual)))
     except (OSError, ValueError, UnicodeError, subprocess.SubprocessError) as exc:
```
```text
$ python3 -I /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C1d_tally_at_least/mori-claim-sweep.py --selftest --scratch /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C1d_tally_at_least
case clean fixture tree pass
case stale present pass
case stale absent pass
case tally equal pass
case tally mismatch FAIL CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 stale=0 carriers=1 pointers=0
case dead pointer pass
case live line suffix pass
case live revision suffix pass
case fenced token ignored pass
case sibling ignored pass
case unreadable carrier pass
case missing pins pass
case malformed pins pass
case capability table pass
case checklist command pass
case ungraded prose ignored pass
case multiple stale occurrences pass
case grammar 'pass=19 fail=0' pass
case grammar 'PASS (12 cases)' pass
case grammar 'PASS 7/7' pass
case grammar 'pass=3' pass
case grammar 'pass=3 fail=1' pass
case grammar 'PASS 2/3' pass
case grammar 'nothing' pass
case grammar 'pass=3\npass=4' pass
CLAIM_SWEEP_SELFTEST pass=24 fail=1
rc=1
```
Pristine/restored SHA-256: `a481cd28371273d899cbbbe52322c1a1f545cfdead8a6a600abfa884222abe99` / `a481cd28371273d899cbbbe52322c1a1f545cfdead8a6a600abfa884222abe99`; mutated SHA-256: `a12488fb236ff896f698b474ef0d25d0abcb8d76b9eb7bc43ac372875b45cb42`.
### C1e_missing_carrier_empty — KILLED
```diff
--- pristine
+++ mutant
@@ -153,7 +153,10 @@
         mismatches = []
         pointer_count = 0
         for carrier in carriers:
-            text = read_text(lane_path(root, carrier))
+            try:
+                text = read_text(lane_path(root, carrier))
+            except OSError:
+                text = ""
             for number, line in graded_rows(carrier, text):
                 for name in pointers(line):
                     pointer_count += 1
```
```text
$ python3 -I /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C1e_missing_carrier_empty/mori-claim-sweep.py --selftest --scratch /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C1e_missing_carrier_empty
case clean fixture tree pass
case stale present pass
case stale absent pass
case tally equal pass
case tally mismatch pass
case dead pointer pass
case live line suffix pass
case live revision suffix pass
case fenced token ignored pass
case sibling ignored pass
case unreadable carrier FAIL CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 stale=0 carriers=1 pointers=0
case missing pins pass
case malformed pins pass
case capability table pass
case checklist command pass
case ungraded prose ignored pass
case multiple stale occurrences pass
case grammar 'pass=19 fail=0' pass
case grammar 'PASS (12 cases)' pass
case grammar 'PASS 7/7' pass
case grammar 'pass=3' pass
case grammar 'pass=3 fail=1' pass
case grammar 'PASS 2/3' pass
case grammar 'nothing' pass
case grammar 'pass=3\npass=4' pass
CLAIM_SWEEP_SELFTEST pass=24 fail=1
rc=1
```
Pristine/restored SHA-256: `a481cd28371273d899cbbbe52322c1a1f545cfdead8a6a600abfa884222abe99` / `a481cd28371273d899cbbbe52322c1a1f545cfdead8a6a600abfa884222abe99`; mutated SHA-256: `5aeaad3b84c951719804d3cfc685dca9b69513fccac5c733dadf3f2949765830`.
### C1f_count_unresolved_only — SURVIVED
```diff
--- pristine
+++ mutant
@@ -183,7 +183,7 @@
     counts = {kind: sum(row[0] == kind for row in mismatches)
               for kind in ('unresolved', 'tally', 'stale')}
     print('CLAIM_SWEEP mismatches=%d unresolved=%d tallies=%d stale=%d carriers=%d pointers=%d'
-          % (len(mismatches), counts['unresolved'], counts['tally'], counts['stale'],
+          % (counts['unresolved'], counts['unresolved'], counts['tally'], counts['stale'],
              len(carriers), pointer_count), file=out)
     return int(bool(mismatches))
```
```text
$ python3 -I /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C1f_count_unresolved_only/mori-claim-sweep.py --selftest --scratch /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C1f_count_unresolved_only
case clean fixture tree pass
case stale present pass
case stale absent pass
case tally equal pass
case tally mismatch pass
case dead pointer pass
case live line suffix pass
case live revision suffix pass
case fenced token ignored pass
case sibling ignored pass
case unreadable carrier pass
case missing pins pass
case malformed pins pass
case capability table pass
case checklist command pass
case ungraded prose ignored pass
case multiple stale occurrences pass
case grammar 'pass=19 fail=0' pass
case grammar 'PASS (12 cases)' pass
case grammar 'PASS 7/7' pass
case grammar 'pass=3' pass
case grammar 'pass=3 fail=1' pass
case grammar 'PASS 2/3' pass
case grammar 'nothing' pass
case grammar 'pass=3\npass=4' pass
CLAIM_SWEEP_SELFTEST pass=25 fail=0
rc=0
```
Pristine/restored SHA-256: `a481cd28371273d899cbbbe52322c1a1f545cfdead8a6a600abfa884222abe99` / `a481cd28371273d899cbbbe52322c1a1f545cfdead8a6a600abfa884222abe99`; mutated SHA-256: `d07b4f6d88cc3d4f73f86e440101f0c61c6e346db0fc7999d7f4dca8104cddc9`.
### C2_any_round_in_cell — KILLED
```diff
--- pristine
+++ mutant
@@ -101,7 +101,7 @@
             errors += 1
             items.append((axis, "-", "-", err))
             continue
-        m = ROUND.search(cell)
+        _ms = list(ROUND.finditer(cell)); m = _ms[-1] if _ms else None
         if not m:
             mismatches += 1
             items.append((axis, "no_round", f"round_{want[0]}_{want[1]}" if want else "-",
```
```text
$ python3 -I /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C2_any_round_in_cell/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C2_any_round_in_cell
FAIL conformant_met want_met=True got={'met': False, 'items': [('coverage', 'round_40_improved', 'round_78_improved', 'mismatch'), ('operability', 'round_40_improved', 'round_78_improved', 'mismatch'), ('depth', 'round_40_improved', 'round_78_improved', 'mismatch'), ('freshness', 'round_40_improved', 'round_78_improved', 'mismatch'), ('calibration', 'round_40_improved', 'round_78_improved', 'mismatch'), ('adjacency', 'round_19_improved', 'round_19_improved', 'ok')], 'mismatches': 5, 'errors': 0, 'rows': 2} 
PASS stale_cell_unmet met=False
PASS verdict_word_missing_unmet met=False
PASS subsumed_by_higher_round_unmet met=False
FAIL nonadmitted_below_ceiling_ignored_met want_met=True got={'met': False, 'items': [('coverage', 'round_47_improved', 'round_47_improved', 'ok'), ('operability', 'round_40_improved', 'round_78_improved', 'mismatch'), ('depth', 'round_40_improved', 'round_78_improved', 'mismatch'), ('freshness', 'round_40_improved', 'round_78_improved', 'mismatch'), ('calibration', 'round_40_improved', 'round_78_improved', 'mismatch'), ('adjacency', 'round_19_improved', 'round_19_improved', 'ok')], 'mismatches': 4, 'errors': 0, 'rows': 3} 
PASS verdict_after_clause_boundary_unmet met=False
PASS later_round_in_cell_ignored_unmet met=False
C2_COUNTER_SELFTEST pass=5 fail=2
rc=1
```
Pristine/restored SHA-256: `8d7fae146589341368399b490ae7c5b4bd55ee9d25496202ca8e0f7e010f1d69` / `8d7fae146589341368399b490ae7c5b4bd55ee9d25496202ca8e0f7e010f1d69`; mutated SHA-256: `00b2916251257b90814718d52b510ee722da1337f4922503f2b753bf0126f237`.
### C2_count_other_verdicts — KILLED
```diff
--- pristine
+++ mutant
@@ -84,7 +84,7 @@
             continue
         rows += 1
         for axis, verdict in (r.get("verdicts") or {}).items():
-            if axis in AXES and verdict in ("improved", "harmed"):
+            if axis in AXES and verdict in ("improved", "harmed", "unchanged", "unprovable"):
                 if axis not in last or rn > last[axis][0]:
                     last[axis] = (rn, verdict)
     return last, rows
```
```text
$ python3 -I /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C2_count_other_verdicts/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C2_count_other_verdicts
FAIL conformant_met want_met=True got={'met': False, 'items': [('coverage', 'round_78_improved', 'round_78_improved', 'ok'), ('operability', 'round_78_improved', 'round_78_improved', 'ok'), ('depth', 'round_78_improved', 'round_78_improved', 'ok'), ('freshness', 'round_78_improved', 'round_78_improved', 'ok'), ('calibration', 'round_78_improved', 'round_78_improved', 'ok'), ('adjacency', 'round_19_improved', 'round_78_unchanged', 'mismatch')], 'mismatches': 1, 'errors': 0, 'rows': 2} 
PASS stale_cell_unmet met=False
PASS verdict_word_missing_unmet met=False
PASS subsumed_by_higher_round_unmet met=False
FAIL nonadmitted_below_ceiling_ignored_met want_met=True got={'met': False, 'items': [('coverage', 'round_47_improved', 'round_47_improved', 'ok'), ('operability', 'round_78_improved', 'round_78_improved', 'ok'), ('depth', 'round_78_improved', 'round_78_improved', 'ok'), ('freshness', 'round_78_improved', 'round_78_improved', 'ok'), ('calibration', 'round_78_improved', 'round_78_improved', 'ok'), ('adjacency', 'round_19_improved', 'round_78_unchanged', 'mismatch')], 'mismatches': 1, 'errors': 0, 'rows': 3} 
PASS verdict_after_clause_boundary_unmet met=False
PASS later_round_in_cell_ignored_unmet met=False
C2_COUNTER_SELFTEST pass=5 fail=2
rc=1
```
Pristine/restored SHA-256: `8d7fae146589341368399b490ae7c5b4bd55ee9d25496202ca8e0f7e010f1d69` / `8d7fae146589341368399b490ae7c5b4bd55ee9d25496202ca8e0f7e010f1d69`; mutated SHA-256: `cccd810b4ce38fdafec1bc3409ed2e29f2f1c11ae81a7e7afc91103df85af29d`.
### C2_cut_clause_boundary — KILLED
```diff
--- pristine
+++ mutant
@@ -108,7 +108,7 @@
                           "mismatch"))
             continue
         got_n = int(m.group(1))
-        tail = cell[m.end():].split(";")[0]
+        tail = cell[m.end():]
         vm = VERDICT.search(tail)
         got_v = vm.group(1) if vm else "none"
         if want is None:
```
```text
$ python3 -I /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C2_cut_clause_boundary/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C2_cut_clause_boundary
PASS conformant_met met=True
PASS stale_cell_unmet met=False
PASS verdict_word_missing_unmet met=False
PASS subsumed_by_higher_round_unmet met=False
PASS nonadmitted_below_ceiling_ignored_met met=True
FAIL verdict_after_clause_boundary_unmet want_met=False got={'met': True, 'items': [('coverage', 'round_78_improved', 'round_78_improved', 'ok'), ('operability', 'round_78_improved', 'round_78_improved', 'ok'), ('depth', 'round_78_improved', 'round_78_improved', 'ok'), ('freshness', 'round_78_improved', 'round_78_improved', 'ok'), ('calibration', 'round_78_improved', 'round_78_improved', 'ok'), ('adjacency', 'round_19_improved', 'round_19_improved', 'ok')], 'mismatches': 0, 'errors': 0, 'rows': 2} 
PASS later_round_in_cell_ignored_unmet met=False
C2_COUNTER_SELFTEST pass=6 fail=1
rc=1
```
Pristine/restored SHA-256: `8d7fae146589341368399b490ae7c5b4bd55ee9d25496202ca8e0f7e010f1d69` / `8d7fae146589341368399b490ae7c5b4bd55ee9d25496202ca8e0f7e010f1d69`; mutated SHA-256: `1f49ebb3fb4142f8746060c00fe7f1673603c1677874abc197dcc5f7c986a362`.
### C2_drop_admitted — KILLED
```diff
--- pristine
+++ mutant
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
```text
$ python3 -I /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C2_drop_admitted/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C2_drop_admitted
PASS conformant_met met=True
PASS stale_cell_unmet met=False
PASS verdict_word_missing_unmet met=False
PASS subsumed_by_higher_round_unmet met=False
FAIL nonadmitted_below_ceiling_ignored_met want_met=True got={'met': False, 'items': [('coverage', 'round_47_improved', 'round_60_improved', 'mismatch'), ('operability', 'round_78_improved', 'round_78_improved', 'ok'), ('depth', 'round_78_improved', 'round_78_improved', 'ok'), ('freshness', 'round_78_improved', 'round_78_improved', 'ok'), ('calibration', 'round_78_improved', 'round_78_improved', 'ok'), ('adjacency', 'round_19_improved', 'round_19_improved', 'ok')], 'mismatches': 1, 'errors': 0, 'rows': 4} 
PASS verdict_after_clause_boundary_unmet met=False
PASS later_round_in_cell_ignored_unmet met=False
C2_COUNTER_SELFTEST pass=6 fail=1
rc=1
```
Pristine/restored SHA-256: `8d7fae146589341368399b490ae7c5b4bd55ee9d25496202ca8e0f7e010f1d69` / `8d7fae146589341368399b490ae7c5b4bd55ee9d25496202ca8e0f7e010f1d69`; mutated SHA-256: `3571bc4ca5637aac25feae7774adabfb0a292c966900bfa6eb35fec7050f97e2`.
### C2_met_ignores_mismatch — KILLED
```diff
--- pristine
+++ mutant
@@ -119,7 +119,7 @@
         if state == "mismatch":
             mismatches += 1
         items.append((axis, f"round_{got_n}_{got_v}", f"round_{want[0]}_{want[1]}", state))
-    met = mismatches == 0 and errors == 0
+    met = errors == 0
     return {"met": met, "items": items, "mismatches": mismatches, "errors": errors,
             "rows": rows}
```
```text
$ python3 -I /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C2_met_ignores_mismatch/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C2_met_ignores_mismatch
PASS conformant_met met=True
FAIL stale_cell_unmet want_met=False got={'met': True, 'items': [('coverage', 'round_47_improved', 'round_78_improved', 'mismatch'), ('operability', 'round_78_improved', 'round_78_improved', 'ok'), ('depth', 'round_78_improved', 'round_78_improved', 'ok'), ('freshness', 'round_78_improved', 'round_78_improved', 'ok'), ('calibration', 'round_78_improved', 'round_78_improved', 'ok'), ('adjacency', 'round_19_improved', 'round_19_improved', 'ok')], 'mismatches': 1, 'errors': 0, 'rows': 2} 
FAIL verdict_word_missing_unmet want_met=False got={'met': True, 'items': [('coverage', 'round_78_improved', 'round_78_improved', 'ok'), ('operability', 'round_78_improved', 'round_78_improved', 'ok'), ('depth', 'round_78_none', 'round_78_improved', 'mismatch'), ('freshness', 'round_78_improved', 'round_78_improved', 'ok'), ('calibration', 'round_78_improved', 'round_78_improved', 'ok'), ('adjacency', 'round_19_improved', 'round_19_improved', 'ok')], 'mismatches': 1, 'errors': 0, 'rows': 2} 
FAIL subsumed_by_higher_round_unmet want_met=False got={'met': True, 'items': [('coverage', 'round_78_improved', 'round_78_improved', 'ok'), ('operability', 'round_40_improved', 'round_78_improved', 'mismatch'), ('depth', 'round_78_improved', 'round_78_improved', 'ok'), ('freshness', 'round_78_improved', 'round_78_improved', 'ok'), ('calibration', 'round_78_improved', 'round_78_improved', 'ok'), ('adjacency', 'round_19_improved', 'round_19_improved', 'ok')], 'mismatches': 1, 'errors': 0, 'rows': 2} 
PASS nonadmitted_below_ceiling_ignored_met met=True
FAIL verdict_after_clause_boundary_unmet want_met=False got={'met': True, 'items': [('coverage', 'round_78_improved', 'round_78_improved', 'ok'), ('operability', 'round_78_improved', 'round_78_improved', 'ok'), ('depth', 'round_78_none', 'round_78_improved', 'mismatch'), ('freshness', 'round_78_improved', 'round_78_improved', 'ok'), ('calibration', 'round_78_improved', 'round_78_improved', 'ok'), ('adjacency', 'round_19_improved', 'round_19_improved', 'ok')], 'mismatches': 1, 'errors': 0, 'rows': 2} 
FAIL later_round_in_cell_ignored_unmet want_met=False got={'met': True, 'items': [('coverage', 'round_78_improved', 'round_78_improved', 'ok'), ('operability', 'round_40_none', 'round_78_improved', 'mismatch'), ('depth', 'round_78_improved', 'round_78_improved', 'ok'), ('freshness', 'round_78_improved', 'round_78_improved', 'ok'), ('calibration', 'round_78_improved', 'round_78_improved', 'ok'), ('adjacency', 'round_19_improved', 'round_19_improved', 'ok')], 'mismatches': 1, 'errors': 0, 'rows': 2} 
C2_COUNTER_SELFTEST pass=2 fail=5
rc=1
```
Pristine/restored SHA-256: `8d7fae146589341368399b490ae7c5b4bd55ee9d25496202ca8e0f7e010f1d69` / `8d7fae146589341368399b490ae7c5b4bd55ee9d25496202ca8e0f7e010f1d69`; mutated SHA-256: `533e40df192e16ac4f2f0e4c5dc1572077b30aabc9381f1136e8c4913aa82636`.
### C2_raise_ceiling — KILLED
```diff
--- pristine
+++ mutant
@@ -80,7 +80,7 @@
         if r.get("lane") != LANE or not r.get("admitted"):
             continue
         rn = r.get("round")
-        if not isinstance(rn, int) or rn > through:
+        if not isinstance(rn, int) or rn > 10 ** 6:
             continue
         rows += 1
         for axis, verdict in (r.get("verdicts") or {}).items():
```
```text
$ python3 -I /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C2_raise_ceiling/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C2_raise_ceiling
FAIL conformant_met want_met=True got={'met': False, 'items': [('coverage', 'round_78_improved', 'round_78_improved', 'ok'), ('operability', 'round_78_improved', 'round_78_improved', 'ok'), ('depth', 'round_78_improved', 'round_90_improved', 'mismatch'), ('freshness', 'round_78_improved', 'round_78_improved', 'ok'), ('calibration', 'round_78_improved', 'round_78_improved', 'ok'), ('adjacency', 'round_19_improved', 'round_19_improved', 'ok')], 'mismatches': 1, 'errors': 0, 'rows': 3} 
PASS stale_cell_unmet met=False
PASS verdict_word_missing_unmet met=False
PASS subsumed_by_higher_round_unmet met=False
FAIL nonadmitted_below_ceiling_ignored_met want_met=True got={'met': False, 'items': [('coverage', 'round_47_improved', 'round_47_improved', 'ok'), ('operability', 'round_78_improved', 'round_78_improved', 'ok'), ('depth', 'round_78_improved', 'round_90_improved', 'mismatch'), ('freshness', 'round_78_improved', 'round_78_improved', 'ok'), ('calibration', 'round_78_improved', 'round_78_improved', 'ok'), ('adjacency', 'round_19_improved', 'round_19_improved', 'ok')], 'mismatches': 1, 'errors': 0, 'rows': 4} 
PASS verdict_after_clause_boundary_unmet met=False
PASS later_round_in_cell_ignored_unmet met=False
C2_COUNTER_SELFTEST pass=5 fail=2
rc=1
```
Pristine/restored SHA-256: `8d7fae146589341368399b490ae7c5b4bd55ee9d25496202ca8e0f7e010f1d69` / `8d7fae146589341368399b490ae7c5b4bd55ee9d25496202ca8e0f7e010f1d69`; mutated SHA-256: `afc4f3189477b4cdcf8bcaee25f206fafd59fa064ef0325a63f476abcbc8b0b5`.
### C3a_drop_sibling — SURVIVED
```diff
--- pristine
+++ mutant
@@ -48,7 +48,7 @@
     named = set()
     for m in TOKEN.finditer(text):
         before = text[max(0, m.start() - 40):m.start()]
-        if SIBLING.search(before):
+        if False:
             continue          # a sibling lane's tool named by path, not a lane instrument
         named.add(m.group(1))
     missing = sorted(present - named)
```
```text
$ python3 -I /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C3a_drop_sibling/count-c3.py --selftest --scratch /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C3a_drop_sibling
PASS complete named=3 present=3 missing=0 extra=0
PASS missing_one named=2 present=3 missing=1 extra=0
PASS extra_stale named=4 present=3 missing=0 extra=1
C3_COUNTER_SELFTEST pass=3 fail=0
rc=0
```
Pristine/restored SHA-256: `6446de67d2b5e6d9f35664d190ec8dde8ddd4d9dead58dd79abc3867aaf7f2d5` / `6446de67d2b5e6d9f35664d190ec8dde8ddd4d9dead58dd79abc3867aaf7f2d5`; mutated SHA-256: `8b35284e8a7b4ce7e83db2b8783458963f7b792530db00b23d5ef681b1792be3`.
### C3b_allow_extra — KILLED
```diff
--- pristine
+++ mutant
@@ -53,7 +53,7 @@
         named.add(m.group(1))
     missing = sorted(present - named)
     extra = sorted(named - present)
-    met = not missing and not extra
+    met = len(named) >= len(present)
     return {"met": met, "named": len(named), "present": len(present),
             "missing": missing, "extra": extra}
```
```text
$ python3 -I /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C3b_allow_extra/count-c3.py --selftest --scratch /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C3b_allow_extra
PASS complete named=3 present=3 missing=0 extra=0
PASS missing_one named=2 present=3 missing=1 extra=0
FAIL extra_stale named=4 present=3 missing=0 extra=1
C3_COUNTER_SELFTEST pass=2 fail=1
rc=1
```
Pristine/restored SHA-256: `6446de67d2b5e6d9f35664d190ec8dde8ddd4d9dead58dd79abc3867aaf7f2d5` / `6446de67d2b5e6d9f35664d190ec8dde8ddd4d9dead58dd79abc3867aaf7f2d5`; mutated SHA-256: `0f1684b9ef658d41f5ef84b566c4f8f22bb8e25225108dea80d137d4a6939d87`.
### C3c_count_directories — SURVIVED
```diff
--- pristine
+++ mutant
@@ -35,7 +35,7 @@
 
 
 def present_set(repo, rev):
-    p = run(["git", "-C", repo, "ls-tree", "-r", "--name-only", rev, "--", "tools/"])
+    p = run(["git", "-C", repo, "ls-tree", "-r", "-t", "--name-only", rev, "--", "tools/"])
     if p.returncode != 0:
         return None
     return {m.group(1) for line in p.stdout.splitlines() if (m := TREE.match(line.strip()))}
```
```text
$ python3 -I /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C3c_count_directories/count-c3.py --selftest --scratch /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/C3c_count_directories
PASS complete named=3 present=3 missing=0 extra=0
PASS missing_one named=2 present=3 missing=1 extra=0
PASS extra_stale named=4 present=3 missing=0 extra=1
C3_COUNTER_SELFTEST pass=3 fail=0
rc=0
```
Pristine/restored SHA-256: `6446de67d2b5e6d9f35664d190ec8dde8ddd4d9dead58dd79abc3867aaf7f2d5` / `6446de67d2b5e6d9f35664d190ec8dde8ddd4d9dead58dd79abc3867aaf7f2d5`; mutated SHA-256: `0784c884dd09a2792c7c4fb23d5540c109793c33b355f5972123764fee767a42`.

## 4. Frozen C2 harness on the executor’s stable arms

The executor confirmed its three arms had landed before snapshotting. Cloned the lane with shared objects and no checkout, loaded HEAD into the scratch index, copied only the current C2 counter into the scratch worktree, and committed that counter in the scratch clone. No mutation of lane git state. This is a scratch snapshot result, not a claim about a future integrated lane revision.
```text
$ git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/mori-shokunin /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/c2repo
Cloning into '/fast/scratch/hyaku/mori-r80/Mo80M01Mutant/c2repo'...
done.
rc=0
```
```text
$ git -C /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/c2repo rev-parse --show-toplevel
/fast/scratch/hyaku/mori-r80/Mo80M01Mutant/c2repo
rc=0
```
```text
$ git -C /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/c2repo read-tree HEAD
rc=0
```
```text
$ git -C /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/c2repo -c user.name=t -c user.email=t@t add .ufo/waves/round-79/count-c2.py
rc=0
```
```text
$ git -C /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/c2repo -c user.name=t -c user.email=t@t commit -qm isolated C2 working-byte snapshot
rc=0
```
Scratch commit: `3bd601d9087d2d3e2d819714c6c5658a77567c5f`; copied counter SHA-256 `8d7fae146589341368399b490ae7c5b4bd55ee9d25496202ca8e0f7e010f1d69`. Frozen harness SHA-256 `16a203b919e33f1cb7d957c1062a559295aa6abe3b9d3e95146871a2998cf7aa`.
```text
$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80/mutate-c2.py --rev 3bd601d9087d2d3e2d819714c6c5658a77567c5f --repo /fast/scratch/hyaku/mori-r80/Mo80M01Mutant/c2repo --scratch /fast/scratch/hyaku/mori-r80/Mo80M01Mutant
mutant drop_admitted killed rc=1 C2_COUNTER_SELFTEST pass=6 fail=1
mutant raise_ceiling killed rc=1 C2_COUNTER_SELFTEST pass=5 fail=2
mutant count_other_verdicts killed rc=1 C2_COUNTER_SELFTEST pass=5 fail=2
mutant cut_clause_boundary killed rc=1 C2_COUNTER_SELFTEST pass=6 fail=1
mutant any_round_in_cell killed rc=1 C2_COUNTER_SELFTEST pass=5 fail=2
mutant met_ignores_mismatch killed rc=1 C2_COUNTER_SELFTEST pass=2 fail=5
MUTATION_C2 survivors=0 killed=6 total=6 rev=3bd601d9087d
rc=0
```
Counter baseline and after-harness selftest both exited 0 with `C2_COUNTER_SELFTEST pass=7 fail=0`; scratch counter SHA-256 remained `8d7fae146589341368399b490ae7c5b4bd55ee9d25496202ca8e0f7e010f1d69`. The six independent direct trials above additionally establish pristine/mutated/restored detector behavior and individual mutant hashes.

## 5. Survivor analysis and routed arms (round 81)

These are coverage findings, not permission to revise P-C1/P-C3 or remediate frozen tools.

| Survivor | Class | Existing detector gap | Arm that would kill it (proposed, not executed) |
|---|---|---|---|
| C1f_count_unresolved_only | Summary aggregation/accounting | Stale/tally arms check return status and class details, not the aggregate mismatches count; all 25 cases remain green. | Stale-only fixture with two occurrences must assert the complete summary `mismatches=2 unresolved=0 tallies=0 stale=2`; tally-only fixture must assert `mismatches=1 unresolved=0 tallies=1 stale=0`. The mutant reports mismatches=0 while still returning 1. |
| C3a_drop_sibling | Namespace/provenance exclusion | All three selftests contain only lane-local tool tokens. | A complete lane inventory plus `../other-shokunin/tools/gone.py` must remain met, with named unchanged and extra empty; removing the skip then adds a spurious extra. |
| C3c_count_directories | Instrument-type confusion | Fixtures contain no directory basename ending .py/.sh, and hence `ls-tree -t` adds no matching token. | Commit a directory `tools/phantom.py/` containing a noninstrument child; PROVINCE names only genuine instrument files. Assert present excludes phantom.py and the inventory remains met. The mutant includes phantom.py and reports it missing. |

Negative findings: no survivor in the assigned six C2 mutations; five assigned C1 mutations are killed; C3’s extra-stale arm already kills `named >= present`. The new C2 `later_round_in_cell_ignored_unmet` arm itself stays PASS under `any_round_in_cell` because operability becomes correct but four other cells select their last round 40 and remain mismatches, masking that intended per-axis change; nevertheless existing conformant_met and the new nonadmitted arm both kill this mutant (pass=5 fail=2). The frozen predicate is satisfied on this scratch snapshot despite this per-arm specificity limit. No live fleet/host surface, source-fetch behavior, integrated after-revision counter, or full gate battery was exercised by this seat.

## 6. Own defects and limits

1. An initial glob used an invalid local:// multi-path form and returned a local-file-not-found error; subsequent discovery used absolute reads. It supplied no evidence and changed nothing.
2. The initial commentary exposed a verbose internal planning paragraph despite the action-first instruction; subsequent work used direct tools and this terminal report.
3. A copied selftest is not an integration check. C2 was pinned to the recorded scratch commit and all targets to SHA-256; no claim is made that a future lane commit has the same bytes.
4. No tools installed/upgraded. No remediation, OS/unit/session change, sibling edit, or lane git mutation. The only permanent seat artifact is this report.

Self-evaluation: accuracy 4 (snapshot, not integrated revision); completeness 4 (all assigned mutants exercised, proposed new killing arms deliberately not implemented); clarity 4 (long C2 diagnostics retained for evidence); actionability 4 (three concrete round-81 arms, not implementation); conciseness 4 (duplicate direct C2 probes retained for restoration evidence). Overall 4.0. Improvements: retain these snapshot limits in closure; route the three exact survivor hunks rather than changing frozen criteria. User-agreement check: evidence includes every assigned mutation, actual harness output and restoration hashes, with limits explicit.

## 7. Cleanup evidence

```text
$ S=/fast/scratch/hyaku/mori-r80/Mo80M01Mutant; trap 'rm -rf -- "$S"' EXIT; test -d "$S" && printf "scratch_present_before_cleanup=yes\n"
scratch_present_before_cleanup=yes
cleanup_rc=0
scratch_exists_after_cleanup=False
```
All scratch clones, fixture repositories, copied mutants and the git guard were removed. Original target bytes were restored before deletion, with equality hashes above.
