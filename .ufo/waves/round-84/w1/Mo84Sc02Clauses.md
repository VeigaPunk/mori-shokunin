# Mo84Sc02Clauses — per-surface recon: unarmed clauses of the r83 counters

Round 84 (attempt 1), wave w1. Seat `Mo84Sc02Clauses`. Read-only reconnaissance; no lane file was
edited, no git/jj mutation was run in the lane. Every execution below used scratch under
`/fast/scratch/hyaku/mori-r84/Mo84Sc02Clauses/` (deleted before yield) and only `git show` /
clone-free fixture repos inside that scratch.

## 0. Pinned surface (bytes graded by P-C1)

Both counters are byte-identical at the entering revision `5adf4337`, the freeze commit `daa77bd`,
and the worktree at the time of this sweep:

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ sha256sum .ufo/waves/round-83/count-c1.py .ufo/waves/round-83/count-c2.py
60e696d87ee4e4b462a479316f57ca568d5c684c64b0ec057898dd70dcb670c3  .ufo/waves/round-83/count-c1.py
d3fadd914ea3d48815a435ebe0db416904e69f4047ffe367815066627540e104  .ufo/waves/round-83/count-c2.py
$ for rev in 5adf4337 daa77bd; do git show $rev:.ufo/waves/round-83/count-c1.py | sha256sum; \
    git show $rev:.ufo/waves/round-83/count-c2.py | sha256sum; done
60e696d87ee4…670c3  -
d3fadd91…0e104  -
60e696d87ee4…670c3  -
d3fadd91…0e104  -
```

Sizes: `count-c1.py` 337 lines, `count-c2.py` 433 lines. The r84 counter was **not** identical
between freeze and HEAD — see §9 D1/D2.

Clause extraction commands (the negative/absence claims below are the output of these sweeps):

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-83
$ grep -n -E 'met = \(|killed_n =|survivors = len|equivalent = len|return rc == 0 and "fail=0"|return rc != 0 or bool|if base.count\(old\)|if mutated == base|if not green\(|if not k and coupling|if not coupled|e\.startswith\("empty-mutation"\) or e\.startswith\("unanchored"\)|or e\.startswith\("coupling-absent"\)|pristine_ok = (True|False)|cases.append' count-c1.py
$ grep -n -E 'met = \(hash_ok|and residual == 0|and agreed == len|and live_ok|if .* is None|if snap_path|if not m|malformed \+= 1|duplicates \+= 1|residual \+=|duplicates == 0|and not stale|return \("|cases.append|return 0 if ok' count-c2.py
$ awk 'NR>=126&&NR<=200{printf "%d\t%s\n",NR,$0}' count-c1.py
$ awk 'NR>=195&&NR<=268{printf "%d\t%s\n",NR,$0}' count-c1.py
$ awk 'NR>=80&&NR<=250{printf "%d\t%s\n",NR,$0}' count-c2.py
$ awk 'NR>=250&&NR<=386{printf "%d\t%s\n",NR,$0}' count-c2.py
```

Arming was measured, not inferred: for every clause a scratch copy of the counter was mutated
(delete / invert), then the copy's own `--selftest` was run and the `FAIL <arm>` lines recorded.
Command shape (repeated per row, cwd inside a scratch work dir):

```
$ python3 -I <scratch>/count-c1.py --selftest --scratch <scratch>/w
$ python3 -I <scratch>/count-c2.py --selftest --scratch <scratch>/w
```

Baseline (unmutated, pinned bytes):

```
C1_COUNTER_SELFTEST pass=6 fail=0     (rc 0)
C2_COUNTER_SELFTEST pass=12 fail=0    (rc 0)
```

## 1. `count-c1.py` — every boolean clause of `met` in `grade()`

`met` is lines 192–194. Atoms, in evaluation order:

| # | clause (line) | text |
|---|---|---|
| 1 | 192 | `pristine_ok` |
| 2 | 192 | `total > 0` |
| 3 | 192 | `survivors == 0` |
| 4a | 193 | `not any(... e.startswith("empty-mutation") ...)` |
| 4b | 193 | `... e.startswith("unanchored") ...` |
| 4c | 194 | `... e.startswith("coupling-absent") ...` |

The guard is one `not any(A or B or C for e in extras)`; the three terms are separate atoms because
each can be dropped independently (M24-style weakening).

## 2. `count-c1.py` — branch inventory

`green()` (128–129), one `return`:

| branch | line | expression |
|---|---|---|
| G1 | 129 | `rc == 0` |
| G2 | 129 | `"fail=0" in out` |
| G3 | 129 | `not FAIL.search(out)` |

`killed()` (132–133), one `return`:

| branch | line | expression |
|---|---|---|
| K1 | 133 | `rc != 0` |
| K2 | 133 | `bool(FAIL.search(out))` |

`grade()` (136–198):

| branch | line | shape |
|---|---|---|
| R1 | 147–148 | loader raises → `setup=read:<path>:<exc>`, return False |
| R2 | 149–150 | loader returns None → `setup=absent:<path>`, return False |
| P1 | 156–159 | `not green(rc,out)` → `pristine_ok = False` + `pristine-red` extra (**does not skip grading**) |
| A1 | 161–164 | `base.count(old) != 1` → `unanchored` extra, `continue` |
| E1 | 166–168 | `mutated == base` → `empty-mutation` extra, `continue` |
| C1 | 176–184 | `not k and coupling is not None` → coupling branch |
| C2 | 178 | `coupled = base.count(coupling) == 1` |
| C3 | 181 | label `equivalent` iff coupled else `survived` |
| C4 | 182–183 | `not coupled` → `coupling-absent` extra |
| C5 | 185–187 | otherwise label `killed` iff k else `survived` |
| T1 | 189 | `survivors = len(lines with " survived ")` |
| T2 | 190 | `equivalent = len(lines with " equivalent ")` |
| T3 | 191 | `killed_n = total - survivors - equivalent` (M24a) |
| M1 | 192–194 | the `met` expression above |
| S1 | 195–197 | tail `pristine=green|red` from `pristine_ok` |

`selfcheck()` (201–267) — six arms, each one branch of the detector oracle:

| arm | line | assertion |
|---|---|---|
| `sensitive_killed` | 227–229 | `met` and killed=1, survivors=0, total=1 |
| `blind_survives` | 235 | `not met` and survivors=1 |
| `duplicate_anchor_excluded` | 242–244 | `not met` and `"unanchored" in extras` and `total=0` |
| `red_pristine_reported` | 249–250 | `not met` and `pristine=red` |
| `equivalent_excluded_when_coupled` | 257–258 | `met` and equivalent=1 and survivors=0 |
| `non_equivalent_still_survives` | 262 | `not met` and survivors=1 |
| aggregation | 263–267 | `return 0 if ok == len(cases) else 1` |

Note: `red_pristine_reported`'s fixture is degenerate — `("tools/red.py", "self_red", "pass=0",
"pass=0")` (line 248) makes `mutated == base`, so it never grades a mutant (`total=0`, line
244/250 shows `mutants=0`). It exercises the tail token but not the met atom.

## 3. `count-c1.py` — measured arming

Column “DEL” = clause deleted/weakened; “INV” = clause inverted. A cell names the arms that went
`FAIL`; `—` means the mutated counter's own selftest stayed `pass=6 fail=0`.

| clause | DEL observed by | INV observed by | verdict |
|---|---|---|---|
| `pristine_ok` (192) | — | `sensitive_killed`, `equivalent_excluded_when_coupled` | **UNARMED for weakening** |
| `total > 0` (192) | — | — (inverted to `total >= 0`) | **UNARMED both ways** |
| `survivors == 0` (192) | `blind_survives`, `non_equivalent_still_survives` | 4 arms | armed |
| `empty-mutation` term (193) | — | — | **UNARMED** |
| `unanchored` term (193) | — | — | **UNARMED** |
| `coupling-absent` term (194) | — | — | **UNARMED (and redundant, §9 D4)** |
| whole `not any(...)` guard | — | `sensitive_killed`, `equivalent_excluded_when_coupled` | weakening **UNARMED** |
| `killed_n` (191, M24a) | — | n/a | **UNARMED** |
| `green()` `"fail=0"` (129, M24b) | — | `sensitive_killed`, `equivalent_excluded_when_coupled` | weakening **UNARMED** |
| `green()` `not FAIL.search` (129) | — | `sensitive_killed`, `equivalent_excluded_when_coupled` | weakening **UNARMED** |
| `green()` `rc == 0` (129) | — | — (no fixture: no rc-1 + `fail=0` pristine) | **UNARMED** |
| `killed()` `bool(FAIL.search)` (133) | — | `blind_survives`, `equivalent_excluded_when_coupled`, `non_equivalent_still_survives` | weakening **UNARMED** |
| `killed()` `rc != 0` (133) | — | — (no rc-1/no-fail-token fixture) | **UNARMED** |
| `grade` unanchored branch `<1` (161) | n/a | `duplicate_anchor_excluded` | armed |
| `grade` pristine-red branch (156) | n/a | `sensitive_killed`, `red_pristine_reported`, `equivalent_excluded_when_coupled` | armed |
| `grade` empty-mutation branch (166) | — (masked by `pristine_ok` in the only fixture) | n/a | **UNARMED** |
| `grade` coupling guard (177) | `equivalent_excluded_when_coupled` | same arm | armed |
| `grade` `not coupled` branch (182) | — (append deleted → no arm) | `equivalent_excluded_when_coupled` | weakening **UNARMED** |

Raw probe results (excerpt; every row rc 0 with `pass=6 fail=0` is an unobserved mutation):

```
met:pristine_ok DEL            rc=0 pass=6 fail=0
met:total>0 DEL                rc=0 pass=6 fail=0
met:survivors==0 DEL           rc=1 FAIL blind_survives, non_equivalent_still_survives
met:empty-mutation term DEL    rc=0 pass=6 fail=0
met:unanchored term DEL        rc=0 pass=6 fail=0
met:coupling-absent term DEL   rc=0 pass=6 fail=0
met:extras guard DEL           rc=0 pass=6 fail=0
tally:killed_n (M24a)          rc=0 pass=6 fail=0
green:fail=0 token DEL (M24b)  rc=0 pass=6 fail=0
green:FAIL.search DEL          rc=0 pass=6 fail=0
green:rc==0 DEL                rc=0 pass=6 fail=0
killed:FAIL.search DEL         rc=0 pass=6 fail=0
killed:rc!=0 DEL               rc=0 pass=6 fail=0
grade:unanchored branch <1     rc=1 FAIL duplicate_anchor_excluded
grade:pristine-red branch INV  rc=1 FAIL sensitive_killed, red_pristine_reported, ...
grade:empty-mutation branch DEL rc=0 pass=6 fail=0
grade:coupling guard INV       rc=1 FAIL equivalent_excluded_when_coupled
grade:coupling-absent branch INV rc=1 FAIL equivalent_excluded_when_coupled
grade:coupling-absent body DEL rc=0 pass=6 fail=0
```

Re-check after the P-C1 seat's planned +2 arms (scratch copy with `blind_case_tally` +
`green_requires_fail_zero`, `pass=8 fail=0`): the five `met` weakenings above still read
`rc=0 fails=NONE` —

```
met:pristine_ok DEL             rc=0 fails=NONE
met:total>0 DEL                 rc=0 fails=NONE
met:empty-mutation term DEL     rc=0 fails=NONE
met:unanchored term DEL         rc=0 fails=NONE
met:coupling-absent term DEL    rc=0 fails=NONE
```

## 4. `count-c2.py` — every boolean clause of `met` in `grade()`

`met` is lines 241–243, twelve conjuncts:

| # | clause (line) | text |
|---|---|---|
| 1 | 241 | `hash_ok` (233: `snap_sha is not None and digest == snap_sha`) |
| 2 | 241 | `asof_ok` (235: `asof is not None and stamp is not None and asof == stamp`) |
| 3 | 241 | `bool(snapshot_tokens)` |
| 4 | 241 | `not unclassified` |
| 5 | 242 | `residual == 0` |
| 6 | 242 | `malformed == 0` |
| 7 | 242 | `duplicates == 0` |
| 8 | 242 | `not stale` |
| 9 | 243 | `agreed == len(snapshot_tokens)` |
| 10 | 243 | `live_ok` (236: `live_rc == 1 and bool(live_tokens)`) |
| 11 | 243 | `retired` (163–167) |
| 12 | 243 | `cell` (170–175) |

Auxiliary predicates that feed `met`:

* `retired_ok()` 163–167: row key `cells[0] == "drift-pin-r10"` (165) **and** `BASELINE in line`
  **and** `CLASSES in line` **and** `snapshot in line` (166); no matching row → `False` (167).
* `cell_state()` 170–175: row key `cells[0].strip("` ") == "freshness"` (172) **and**
  `"r10 pin retired" in line` **and** `CLASSES in line` **and**
  `"round-10 drift pin still red" not in line` (173–174); no row → `False` (175).
* `classifications()` 82–94: non-`DRIFT_CLASS` lines skipped (85–86); `malformed += 1` when the
  regex misses or the class word is unknown (87–90); `duplicates += 1` on a repeated token (91–92);
  last statement wins (93).
* `header()` 97–125: duplicate `Snapshot:`/`Snapshot-sha256:`/`As-of:` counters, all three must
  equal 1 (123–124).
* `run_start()` 137–147: missing (139–140), unparsable (141–144), naive tz (145–146) → None.

## 5. `count-c2.py` — branch inventory

`grade()` (196–275):

| branch | line | shape |
|---|---|---|
| R1 | 201–202 | census/baseline/SCORECARD absent → `setup=…`, return False |
| R2 | 203–204 | `CLASSES` absent → `snapshot=absent`, return False |
| R3 | 205–207 | `header()` returns None (missing or duplicated provenance) → `snapshot=absent` |
| R4 | 208–210 | snapshot path ≠ frozen path → `snapshot=unbound:path=…` |
| R5 | 211–214 | snapshot file absent → `snapshot=unbound:snapshot-absent` |
| L1 | 223–225 | token not in `stated` → unclassified (skipped in the loop) |
| L2 | 226–227 | stated `unexplainable` → `residual += 1` |
| L3 | 228–229 | stated class == derived → `agreed += 1` |
| L4 | 230 | `stale = [token in stated not in snapshot_tokens]` |
| L5 | 231 | `residual += duplicates` (M24d coupling) |
| H1 | 233 | `hash_ok` |
| A1 | 235 | `asof_ok` |
| V1 | 236 | `live_ok` |
| P1 | 239 | `retired` |
| P2 | 240 | `cell` |
| M1 | 241–243 | `met` |
| N1 | 250–274 | seven note branches (`hash`, `asof`, `live-rc`, `unclassified`, `class-disagrees`, `stale`, `malformed`, `duplicates`, `retired`, `cell`) |

`green()`/`killed()` do not exist in this file (they are c1-only); the c2 detector has no such
functions.

`selfcheck()` (278–384) — twelve arms (each a branch of the fixture oracle):

| arm | line | fixture shape | assertion |
|---|---|---|---|
| `conformant` | 328–330 | 4 tokens, all classified/agreed, live stub rc 1 | `met` and `tokens=4` and `live=derived` |
| `snapshot_absent` | 331–333 | `# Snapshot:` line removed | `not met` and `snapshot=absent` |
| `hash_mismatch` | 334–337 | sha replaced with 64 zeros | `not met`, `snapshot=unbound`, hash note |
| `asof_mismatch` | 338–340 | As-of +1 s | `not met` and `asof=0` |
| `unclassified_token` | 341–344 | one token's class line dropped | `not met` and `agreed=3` |
| `class_disagrees` | 345–347 | `fields` stated `added-since-r10` | `not met` and `agreed=3` |
| `green_live_unmet` | 348–349 | live stub exits 0 (`MORI_DRIFT: none`) | `not met` and `live=unavailable` |
| `duplicate_line_residual` | 350–362 | duplicate `+audit` class line | `not met` and `residual=1` |
| `retired_row_snapshot_required` | 363–367 | Retired row loses the snapshot path | `not met` + `retired-row` note |
| `red_cell_keeps_unmet` | 368–370 | Axes cell has the red literal | `not met` and `live=derived` |
| `duplicate_header_unmet` | 371–373 | a second `# Snapshot:` line | `not met` and `snapshot=absent` |
| `foreign_snapshot_path_unmet` | 374–379 | header names `corpus/evidence/other-snapshot.txt` | `not met` and `snapshot=unbound` in tail |
| aggregation | 380–384 | `pass=N fail=0` | `return 0 if ok == len(cases) else 1` |

## 6. `count-c2.py` — measured arming

| clause | DEL observed by | INV observed by | verdict |
|---|---|---|---|
| `hash_ok` | `hash_mismatch` | `conformant`, `hash_mismatch` | armed |
| `asof_ok` | `asof_mismatch` | `conformant`, `asof_mismatch` | armed |
| `bool(snapshot_tokens)` | — | `conformant` only | weakening **UNARMED** |
| `not unclassified` (M24c) | — | `conformant` only | weakening **UNARMED (provably equivalent)** |
| `residual == 0` (M24d) | — | `conformant` only | weakening **UNARMED (equivalent with #7)** |
| `malformed == 0` | — | `conformant` only | weakening **UNARMED** |
| `duplicates == 0` | — | `conformant` only | weakening **UNARMED (masked by `residual += duplicates`)** |
| `not stale` | — | `conformant` only | weakening **UNARMED** |
| `agreed == len(...)` | `class_disagrees` | `conformant`, `class_disagrees` | armed |
| `live_ok` | `green_live_unmet` | `conformant`, `green_live_unmet` | armed |
| `retired` | `retired_row_snapshot_required` | `conformant`, same arm | armed |
| `cell` | `red_cell_keeps_unmet` | `conformant`, same arm | armed |
| `retired_ok` `BASELINE` (166) | — | n/a | **UNARMED** |
| `retired_ok` `CLASSES` (166) | — | n/a | **UNARMED** |
| `retired_ok` `snapshot` (166) | `retired_row_snapshot_required` | n/a | armed |
| `retired_ok` row-key (165) | — (loosened to `if cells:` → `conformant` fails, but no arm isolates the key) | `conformant` | **UNARMED** |
| `cell_state` `"r10 pin retired"` (173) | — | n/a | **UNARMED** |
| `cell_state` `CLASSES` (173) | — | n/a | **UNARMED** |
| `cell_state` red literal (174) | — | n/a | **UNARMED** |

Raw probe results:

```
met:hash_ok DEL              rc=1 FAIL hash_mismatch
met:asof_ok DEL              rc=1 FAIL asof_mismatch
met:bool(tokens) DEL         rc=0 pass=12 fail=0
met:not unclassified DEL     rc=0 pass=12 fail=0     (M24c)
met:residual==0 DEL          rc=0 pass=12 fail=0     (M24d)
met:malformed==0 DEL         rc=0 pass=12 fail=0
met:duplicates==0 DEL        rc=0 pass=12 fail=0
met:not stale DEL            rc=0 pass=12 fail=0
met:agreed==len DEL          rc=1 FAIL class_disagrees
met:live_ok DEL              rc=1 FAIL green_live_unmet
met:retired DEL              rc=1 FAIL retired_row_snapshot_required
met:cell DEL                 rc=1 FAIL red_cell_keeps_unmet
retired_ok:BASELINE DEL      rc=0 pass=12 fail=0
retired_ok:CLASSES DEL       rc=0 pass=12 fail=0
retired_ok:snapshot DEL      rc=1 FAIL retired_row_snapshot_required
cell_state:r10 literal DEL   rc=0 pass=12 fail=0
cell_state:CLASSES DEL       rc=0 pass=12 fail=0
cell_state:red-literal DEL   rc=0 pass=12 fail=0
```

Every inversion of the twelve `met` atoms is observed by `conformant` (rc 1, `pass=11 fail=1`),
which is expected — inversion flips the conformant fixture. Inversion is not a realistic defect
class here; the deletions are, and six of the twelve survive deletion.

## 7. The one arm that would observe each UNARMED clause

Fixture shapes refer to the existing `selfcheck()` helpers (`write`, `disk`, `grade` for c1;
`build` for c2). “Assertion” is the case predicate that fails when the clause is deleted.

### c1 (post-P-C1-edit state)

| # | clause | arm to add | fixture | assertion |
|---|---|---|---|---|
| U1 | `pristine_ok` (192) | `red_pristine_can_still_kill` | pristine `print('FAKE pass=0 fail=0'); raise SystemExit(1)` (rc 1, no `fail=n`); mutant `pass=0`→`pass=1` (mutated copy still exits 1 → killed) | `not met` and `survivors==0` and `pristine=red` |
| U2 | `total > 0` (192) | `empty_population_unmet` | `grade(disk, scratch, [])` on a scratch dir holding one green fake counter | `not met` and `total=0` and `mutants=0` and `pristine=green` |
| U3 | `empty-mutation` term (193) | `empty_mutation_beside_kill` | one killed mutant (`GUARD=1`→`GUARD=0`) plus one no-op (`GUARD=1`→`GUARD=1`) on a file with two distinct anchors | `not met` and `survivors==0` and `"empty-mutation" in extras` and `total==1` |
| U4 | `unanchored` term (193) | `unanchored_beside_kill` | one killed mutant plus one anchor occurring 0 times | `not met` and `survivors==0` and `"unanchored" in extras` and `total==1` |
| U5 | `coupling-absent` term (194) and append (182–183) | (no arm can observe it) | a missing coupling always prints the line `survived` (line 181), so `survivors==0` already blocks `met` | recommend deleting both the term and the append instead of arming |
| U6 | `green()` `rc == 0` (129) | `green_requires_rc_zero` | `green(1, "FAKE pass=1 fail=0")` | must be False |
| U7 | `green()` `not FAIL.search` (129) | `green_rejects_fail_token` | `green(0, "FAKE pass=1 fail=0 fail=2")` | must be False |
| U8 | `killed()` `bool(FAIL.search)` (133) | `killed_requires_fail_token` | `killed(0, "FAKE pass=1 fail=2")` | must be True |
| U9 | `killed()` `rc != 0` (133) | `killed_requires_rc` | `killed(1, "traceback")` | must be True |
| U10 | `grade` empty-mutation branch (166) | covered by U3 | — | also assert the extra text |
| U11 | `setup=read` (148) | `loader_error_is_setup` | loader that raises | `tail.startswith("setup=read")` and `not met` |
| U12 | `setup=absent` (149–150) | `loader_absent_is_setup` | loader returning None | `setup=absent` and `not met` |
| U13 | `pristine-red` extra text (158–159) | `pristine_red_named` | U1 fixture | `any(e.startswith("pristine-red") for e in extras)` |

### c2

| # | clause | arm to add | fixture | assertion |
|---|---|---|---|---|
| V1 | `bool(snapshot_tokens)` (241) | `empty_token_population_unmet` | snapshot whose last `MORI_DRIFT:` line is `none` (recompute header digest/As-of) | `not met` and `tokens=0` |
| V2 | `malformed == 0` (242) | `malformed_line_unmet` | `DRIFT_CLASS +audit bogus` followed by the valid `DRIFT_CLASS +audit added-since-r10` | `not met`, `malformed=1` note/field |
| V3 | `not stale` (242) | `stale_classification_unmet` | add `DRIFT_CLASS +ghost added-since-r10` (token absent from snapshot) | `not met` and `stale-classification` note |
| V4 | `retired_ok` `BASELINE` (166) | `retired_row_baseline_required` | Retired row with the snapshot and CLASSES paths but not the baseline path | `not met` + `retired-row` note |
| V5 | `retired_ok` `CLASSES` (166) | `retired_row_classes_required` | row omitting `corpus/evidence/drift-classification-r82.txt` | `not met` + `retired-row` note |
| V6 | `retired_ok` row key (165) | `retired_row_key_required` | rename the row's first cell to `drift-pin-r10x` | `not met` + `retired-row` note |
| V7 | `cell_state` `"r10 pin retired"` (173) | `freshness_requires_retired_phrase` | Axes cell with CLASSES path, no red literal, no `r10 pin retired` | `not met` + `freshness-cell-red` note |
| V8 | `cell_state` `CLASSES` (173) | `freshness_requires_classes_path` | Axes cell with `r10 pin retired` and no CLASSES path | same |
| V9 | `cell_state` red literal (174) | `freshness_rejects_red_literal` | Axes cell with both `r10 pin retired` and `round-10 drift pin still red` | same |
| V10 | `classes is None` (203) | `classification_file_absent` | `build("noclasses", head, None)` (CLASSES not written) | `not met` and `snapshot=absent` |
| V11 | `snapshot is None` (212) | `snapshot_file_absent` | build, then unlink `.ufo/waves/round-82/evidence/drift-r82-live.txt` before `grade` | `not met` and `snapshot=unbound:snapshot-absent` |
| V12 | `setup=` (201) | `census_absent_is_setup` | loader returning None for `CENSUS` | `tail.startswith("setup=")` and `not met` |
| V13 | `run_start` missing/naive (139–146) | `asof_requires_tz_stamp` | run-start stamp without tz | `not met` and `asof=0` |
| V14 | `header` sha/asof duplicate counts (123) | `duplicate_sha_header_unmet`, `duplicate_asof_header_unmet` | duplicate `# Snapshot-sha256:` / `# As-of:` | `not met` and `snapshot=absent` |
| V15 | `live_read` timeout (190–191) | (optional) hanging stub | `sleep` stub | `live=unavailable` + metric note |

The two c2 equivalences are **not** armable and must not be armed: M24c (`not unclassified`) is
implied by `agreed == len(snapshot_tokens)`, and M24d (`residual == 0`) is implied by
`agreed == len(...)` for `unexplainable` and by `duplicates == 0` + `residual += duplicates` for
duplicates. This sweep confirms both deletions leave `pass=12 fail=0`.

## 8. The four round-84 mutant labels before this round's edits

Measured against the r83 counters' own selftests (the P-C1 kill rule: the **mutated r83 copy's**
`--selftest`, not the r84 detector's arms):

| label | anchor in the r83 bytes (at the freeze) | mutated copy's own selftest | observed by an arm? |
|---|---|---|---|
| `M24a_killed_tally` | `killed_n = total - survivors - equivalent` ×1 (line 191) | `rc=0 pass=6 fail=0` | **NO** |
| `M24b_green_fail_token` | contract table string ×2 (line 33 table + line 129 body); r84 counter at HEAD scopes it to `    return …` ×1 | `rc=0 pass=6 fail=0` | **NO** |
| `M24c_met_unclassified` | contract table compound `and not unclassified and residual == 0` ×0 (line-wrapped); r84 counter at HEAD uses `and not unclassified` ×1 | `rc=0 pass=12 fail=0` | **NO** (equivalent) |
| `M24d_met_residual` | same compound ×0; r84 counter at HEAD uses `and residual == 0` ×1 | `rc=0 pass=12 fail=0` | **NO** (equivalent) |

Anchor counts, measured directly on `git show <rev>:<path>`:

```
M24a .ufo/waves/round-83/count-c1.py count=1
M24b .ufo/waves/round-83/count-c1.py count=2      # contract-table string
M24c .ufo/waves/round-83/count-c2.py count=0      # contract-table compound
M24d .ufo/waves/round-83/count-c2.py count=0
('and not unclassified', 1) ('residual == 0', 1)
('agreed == len(snapshot_tokens)', 1) ('residual += duplicates', 1) ('duplicates == 0', 1)
```

Population control, run exactly as the contract prescribes:

```
$ python3 -I .ufo/waves/round-84/count-c1.py daa77bd --repo <lane> --scratch <s>
MUTANT count-c1.py M24a_killed_tally survived rc=0
MUTANT count-c1.py M24b_green_fail_token survived rc=0
MUTANT count-c2.py M24c_met_unclassified equivalent rc=0
MUTANT count-c2.py M24d_met_residual equivalent rc=0
C1=unmet mutants=4 killed=0 equivalent=2 survivors=2 total=4 pristine=green detector=green rev=daa77bd5684c
rc=1
```

The same reading at `dbdb1aaa`:

```
C1=unmet mutants=4 killed=0 equivalent=2 survivors=2 total=4 pristine=green detector=green rev=dbdb1aaa4d5b
rc=1
```

## 9. Defects found in other seats' bytes / the frozen authority

**Amendment status at hand-off.** While this sweep ran, the L1 filed **A2** (the three anchor
corrections) and **A4** (`blind_case_tally` assertion; the A4 text cites this seat's D3) in
`.ufo/waves/round-84/contract.md`; both were uncommitted worktree text at the time of this read.
A2/A4 close D1–D3 below. D4 and D5 are still open. The measurements are kept because they are the
evidence A2/A4 rest on and because D2's table-vs-counter inconsistency remains readable in §P-C1.

**D1 — the counter bytes committed at the freeze commit cannot grade the frozen population.**
`git show daa77bd:.ufo/waves/round-84/count-c1.py` has the contract-literal anchors. Executed
against the freeze revision it prints:

```
MUTANT count-c1.py M24a_killed_tally survived rc=0
EXTRA unanchored .ufo/waves/round-83/count-c1.py M24b_green_fail_token occurrences=2
EXTRA unanchored .ufo/waves/round-83/count-c2.py M24c_met_unclassified occurrences=0
EXTRA unanchored .ufo/waves/round-83/count-c2.py M24d_met_residual occurrences=0
C1=unmet mutants=1 killed=0 equivalent=0 survivors=1 total=1 pristine=green detector=green rev=daa77bd5684c
rc=1
```

The contract's “Population control at the freeze commit … `mutants=4 killed=0 equivalent=2
survivors=2`” is therefore **not reproducible with the freeze commit's own counter**, only with the
post-freeze amended counter (`86133aa9…`, HEAD `dbdb1aaa`). A4 now states the control is the
worktree counter at HEAD grading the freeze revision's r83 bytes, which is exactly the run quoted
in §8; the P-C1 paragraph still says “at the freeze commit”, so the two must be read together.

**D2 — the counter's anchors were retargeted after the freeze (now documented in A2).**
`git diff daa77bd..HEAD -- .ufo/waves/round-84/count-c1.py` (10 lines) changes `M24b` from the
unscoped `return …` to the indented `    return …` (uniqueness: 2 → 1) and replaces the
M24c/M24d compound anchor with the single terms `and not unclassified` / `and residual == 0` plus
empty `new` strings (uniqueness: 0 → 1). A2 records these same three defects and the replacement
anchors. The contract's §P-C1 mutant table above still quotes the pre-A2 strings, so a literal
audit of “each `old` anchor occurs exactly once” against the table fails at every revision
(2× / 0× / 0×); the audit must read the table through A2. The term deleted is the same, so the
predicate semantics are unchanged.

**D3 — the prescribed `blind_case_tally` assertion is arithmetically wrong (corrected in A4).** The
seat spec said a fixture with one killed and one surviving mutant “must print `killed=0
survivors=1`”. The correct tally is `killed = total - survivors - equivalent = 2 - 1 - 0 = 1`.
Implemented literally, the **pristine** r83 counter's selftest goes red:

```
=== r83 c1 selftest with literal blind_case_tally (killed==0) rc=1
FAIL blind_case_tally mutants=2 killed=1 equivalent=0 survivors=1 total=2 pristine=green
C1_COUNTER_SELFTEST pass=7 fail=1
=== r83 c1 selftest with corrected blind_case_tally (killed==1) rc=0
C1_COUNTER_SELFTEST pass=8 fail=0
```

Fixture run of the r84 counter over each variant (`<rev>` = scratch repo commit):

```
=== literal (killed==0): rc=1
MUTANT count-c1.py M24a_killed_tally killed rc=1
MUTANT count-c1.py M24b_green_fail_token killed rc=1
MUTANT count-c2.py M24c_met_unclassified equivalent rc=0
MUTANT count-c2.py M24d_met_residual equivalent rc=0
EXTRA pristine-red .ufo/waves/round-83/count-c1.py rc=1 ['C1_COUNTER_SELFTEST pass=7 fail=1']
C1=unmet mutants=4 killed=2 equivalent=2 survivors=0 total=4 pristine=red detector=green
=== corrected (killed==1): rc=0
MUTANT count-c1.py M24a_killed_tally killed rc=1
MUTANT count-c1.py M24b_green_fail_token killed rc=1
MUTANT count-c2.py M24c_met_unclassified equivalent rc=0
MUTANT count-c2.py M24d_met_residual equivalent rc=0
C1=met mutants=4 killed=2 equivalent=2 survivors=0 total=4 pristine=green detector=green
```

So the target is reachable with the corrected assertion and the amended anchors, and unreachable
with the literal one. A4 now prescribes `killed=1 survivors=1 total=2` and `not met`; the fixture
above is the measured proof that this reaches the frozen target line.

**D4 — `coupling-absent` in the c1 `met` is dead weight.** When the coupling marker is missing the
mutant line is labelled `survived` (line 181), so `survivors == 0` already blocks `met`; deleting
both the term (194) and the append (182–183) is unobservable (`pass=6 fail=0`). Keep only if an
audit message is wanted.

**D5 — c2 cross-claim hazard for the C3 seat.** `residual == 0` and `duplicates == 0` each mask the
other's deletion (`residual += duplicates`, line 231). Any new C3 selftest arm that constructs
`residual > 0` with `duplicates == 0`, or `duplicates > 0` with a zeroed residual, would make
M24d non-equivalent and break P-C1's `equivalent=2`. The four coupling substrings
(`and not unclassified`, `residual == 0`, `agreed == len(snapshot_tokens)`,
`residual += duplicates`, `duplicates == 0`) must stay exactly once, as P-C3 already says.

## 10. Not verified

* No lane file was edited; I did not apply the arms or the anchor/assertion corrections — the
  fixture results in §9 use scratch copies only.
* I did not run the r84 `count-c2.py` / `count-c3.py` counters (outside this seat's surface).
* The C3 seat's future edits to `.ufo/waves/round-83/count-c2.py` may change the c2 arming matrix in
  §6; §6 describes the pinned bytes above only.
* The `live_read` timeout branch and the `header` sha/asof duplicate branches (V14/V15) were
  classified statically; I did not build a hanging stub or duplicate-`sha`/`asof` fixture.
