# CalibScout — C1 calibration reconnaissance (mori, round 96 attempt 1, wave w1)

Seat: CalibScout (scout, read-only). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Entering HEAD `66c5518e239eeacd6070be26d78085ef702392cb` (lane master; worktree HEAD is
`b88c8ae8ff85d1cb7df81fffef2f46a0512e76b5` = "round-96: freeze contract, before receipts,
wave-1 spec and dispatch" — the contract freeze commit; SCORECARD.md is unchanged from
66c5518e, so all readings below are identical at both revs).
Fleet root `/home/vgpnk/Projects/shokunin`; `MANIFEST.json` worktree blob
`23f2ecd3ea234552ee090e9ef2a87b78c2608039` == `git rev-parse HEAD:MANIFEST.json`
(clean, no local edits).

**Manifest grew during the seat.** The fleet ledger was appended to while this seat ran:
`MANIFEST.json` had 1340 `rounds[]` rows at my first read and has **1342** at the final read
(blob `2ceedb1835e…` → `23f2ecd3ea23…`); the two new rows are `kotodama` r91 and `tabi` r68
closures, appended *after* all mori rows. **No mori row and no cited index moved**, and the
derived expectations were recomputed after the growth and are byte-identical (§4). All mori
row indexes quoted below were re-read from the current (1342-row) manifest.

No files were created outside `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-96/w1/scout/`
and the scratch root. No tool was installed (no installs performed — nothing needed).
All git commands were read-only `git -C <abs path> show/log/rev-parse/ls-files/hash-object/status`.

---

## 0. Verdict summary

| Question | Answer |
|---|---|
| Duplicate admitted-true round for lane mori? | **No.** 0 mori rows share a round number with `admitted: true` (only r91 duplicates, both `admitted: false`). |
| Closure-correction row type present for mori? | **Yes, one**: `rounds[1313]` = mori r91, `type: "closure-correction"`, `supersedes` → `rounds[1311]`, `admitted: false`. No mori admitted-true row is of a non-`closure` type. |
| `Last change` convention | Highest admitted mori closure grading that axis **improved or harmed** (r50/r79 convention), *not* the latest score move. Cell leads with `round N (verdict, score held)`, older history kept after the first `;`. |
| Cells whose first round ≠ expected | **5 of 6**: coverage, operability, depth, freshness, calibration. Adjacency is correct at r19. |
| Verdict-word spelling deviations | **None found** (all cells lowercase `improved`; no `harmed`, no capitalization or trailing-space deviations). |
| Unbounded expected cells (contract target) | coverage r80 improved, operability r93 improved, depth r86 improved, freshness r82 improved, calibration r93 improved, adjacency r19 improved (unchanged). Matches the contract §C1 target exactly. |

---

## 1. MANIFEST.json — every `lane == "mori"` row with `round >= 76`

Command (raw):

```
$ cd /home/vgpnk/Projects/shokunin && python3 - <<'EOF'
import json
d=json.load(open('/home/vgpnk/Projects/shokunin/MANIFEST.json'))
rs=d['rounds']
print('total rounds rows:', len(rs))
idx=0
for r in rs:
    idx+=1
    if r.get('lane')=='mori' and isinstance(r.get('round'),int) and r.get('round')>=76:
        print(idx, '| round=',r.get('round'), '| type=',r.get('type'), '| admitted=',repr(r.get('admitted')), type(r.get('admitted')).__name__, '| verdicts=',r.get('verdicts'))
EOF
```

Output (index = **1-based position in `rounds[]`**; 0-based `rounds[]` index in parentheses):

```
total rounds rows: 1342
1057 (1056) | round= 76 | type= closure | admitted= True bool | verdicts= {'calibration': 'improved', 'depth': 'improved', 'freshness': 'improved', 'coverage': 'unchanged', 'operability': 'unchanged', 'adjacency': 'unchanged'}
1061 (1060) | round= 77 | type= closure | admitted= False bool | verdicts= {'depth': 'improved', 'coverage': 'unchanged', 'operability': 'unprovable', 'freshness': 'improved', 'calibration': 'unchanged', 'adjacency': 'unchanged'}
1065 (1064) | round= 78 | type= closure | admitted= True bool | verdicts= {'operability': 'improved', 'calibration': 'improved', 'freshness': 'improved', 'coverage': 'unchanged', 'depth': 'unchanged', 'adjacency': 'unchanged'}
1159 (1158) | round= 79 | type= closure | admitted= True bool | verdicts= {'coverage': 'unchanged', 'operability': 'improved', 'depth': 'unchanged', 'freshness': 'improved', 'calibration': 'improved', 'adjacency': 'unchanged'}
1164 (1163) | round= 80 | type= closure | admitted= True bool | verdicts= {'calibration': 'improved', 'operability': 'improved', 'coverage': 'improved', 'depth': 'unchanged', 'freshness': 'unchanged', 'adjacency': 'unchanged'}
1172 (1171) | round= 81 | type= closure | admitted= True bool | verdicts= {'calibration': 'improved', 'operability': 'improved', 'coverage': 'unchanged', 'depth': 'unchanged', 'freshness': 'unchanged', 'adjacency': 'unchanged'}
1176 (1175) | round= 82 | type= closure | admitted= True bool | verdicts= {'operability': 'improved', 'freshness': 'improved', 'depth': 'improved', 'coverage': 'unchanged', 'calibration': 'unchanged', 'adjacency': 'unchanged'}
1182 (1181) | round= 83 | type= closure | admitted= True bool | verdicts= {'operability': 'improved', 'calibration': 'improved', 'depth': 'improved', 'coverage': 'unchanged', 'freshness': 'unchanged', 'adjacency': 'unchanged'}
1192 (1191) | round= 84 | type= closure | admitted= True bool | verdicts= {'operability': 'improved', 'calibration': 'improved', 'depth': 'improved', 'coverage': 'unchanged', 'freshness': 'unchanged', 'adjacency': 'unchanged'}
1200 (1199) | round= 85 | type= closure | admitted= True bool | verdicts= {'operability': 'improved', 'calibration': 'improved', 'depth': 'improved', 'coverage': 'unchanged', 'freshness': 'unchanged', 'adjacency': 'unchanged'}
1206 (1205) | round= 86 | type= closure | admitted= True bool | verdicts= {'operability': 'improved', 'calibration': 'improved', 'depth': 'improved', 'coverage': 'unchanged', 'freshness': 'unchanged', 'adjacency': 'unchanged'}
1213 (1212) | round= 87 | type= closure | admitted= True bool | verdicts= {'operability': 'improved', 'calibration': 'improved', 'coverage': 'unchanged', 'depth': 'unchanged', 'freshness': 'unchanged', 'adjacency': 'unchanged'}
1223 (1222) | round= 88 | type= closure | admitted= False bool | verdicts= {'depth': 'unchanged', 'coverage': 'unchanged', 'operability': 'harmed', 'freshness': 'unchanged', 'calibration': 'unchanged', 'adjacency': 'unchanged'}
1285 (1284) | round= 89 | type= closure | admitted= True bool | verdicts= {'operability': 'improved', 'calibration': 'improved', 'depth': 'unchanged', 'coverage': 'unchanged', 'freshness': 'unchanged', 'adjacency': 'unchanged'}
1310 (1309) | round= 90 | type= closure | admitted= True bool | verdicts= {'operability': 'improved', 'calibration': 'improved'}
1312 (1311) | round= 91 | type= closure | admitted= False bool | verdicts= {'calibration': 'unprovable', 'freshness': 'unprovable', 'depth': 'unchanged', 'coverage': 'unchanged', 'operability': 'unchanged', 'adjacency': 'unchanged'}
1314 (1313) | round= 91 | type= closure-correction | admitted= False bool | verdicts= {'calibration': 'unprovable', 'freshness': 'unprovable', 'depth': 'unchanged', 'coverage': 'unchanged', 'operability': 'unchanged', 'adjacency': 'unchanged'}
1318 (1317) | round= 92 | type= closure | admitted= False bool | verdicts= {'depth': 'unprovable', 'freshness': 'unchanged', 'coverage': 'unchanged', 'operability': 'unchanged', 'calibration': 'unchanged', 'adjacency': 'unchanged'}
1328 (1327) | round= 93 | type= closure | admitted= True bool | verdicts= {'calibration': 'improved', 'operability': 'improved'}
1335 (1334) | round= 94 | type= closure | admitted= False bool | verdicts= {'calibration': 'improved', 'operability': 'unchanged', 'depth': 'unchanged', 'freshness': 'unchanged', 'coverage': 'unchanged', 'adjacency': 'unchanged'}
1340 (1339) | round= 95 | type= closure | admitted= False bool | verdicts= {'depth': 'unchanged', 'coverage': 'unchanged', 'operability': 'unchanged', 'freshness': 'unchanged', 'calibration': 'unchanged', 'adjacency': 'unchanged'}
```

(Row order in the file is manifest append order, not round order — e.g. r89 sits after r88 but
r76–r95 are spread across the file.)

Facts established by this listing:

* **Admitted-true mori closures with round ≥ 76**: r76, r78, r79, r80, r81, r82, r83, r84, r85,
  r86, r87, r89, r90, r93 (14 rows). All have `type == "closure"` and `admitted` of Python type
  `bool` (`True`).
* **Admitted-false mori rows with round ≥ 76**: r77, r88, r91 (closure), r91 (closure-correction),
  r92, r94, r95 (7 rows). r94 carries `calibration: improved` but is not admitted → does not count.
* **`admitted` raw value / Python type**: every mori row has `admitted` of type `bool`
  (`Counter({'bool': 85})` over all 85 mori rows; `Counter({'True': 58, 'False': 27})`). No
  truthy-non-bool, no `"true"`, no missing key on any mori row → a `bool` check and a truthiness
  check are equivalent for this lane.
* **Duplicate-round hazard**: **none among admitted-true rows.**
  `mori admitted-true duplicate rounds: {}`. The only duplicated mori round number is **91**
  (0-based `rounds[1311]` closure + `rounds[1313]` closure-correction; 1-based 1312 and 1314),
  and both are `admitted: false`, so it cannot change any expectation today. Raw evidence:

```
$ python3 -c "... Counter(r['round'] for mori rows with admitted is True) ..."
mori admitted-true duplicate rounds: {}
mori rows with duplicate round numbers: {91: 2}
```

* **Closure-correction row type**: `rounds[1313]` (0-based) — mori, round 91,
  `"type": "closure-correction"`, `"supersedes": {"round": 91, "type": "closure", "date": "2026-11-05", "entry": 1311}`,
  `"admitted": false`, notes: *"Corrects rounds[1311] (superseded): its closed_at … was future-dated
  against the committing commit …"*. It is the **only** non-`closure` mori row of the 85.

Raw:

```
$ python3 -c "print(json.dumps({k:rs[1313].get(k) for k in ('round','type','lane','lane_round','admitted','verdict','verdicts','supersedes','date')}, ensure_ascii=False))"
{"round": 91, "type": "closure-correction", "lane": "mori", "lane_round": 91, "admitted": false, "verdict": "rejected-honest-stop", "verdicts": {"calibration": "unprovable", "freshness": "unprovable", "depth": "unchanged", "coverage": "unchanged", "operability": "unchanged", "adjacency": "unchanged"}, "supersedes": {"round": 91, "type": "closure", "date": "2026-11-05", "entry": 1311}, "date": "2026-11-05"}
```

* **Round-number vs `lane_round`**: identical for every mori row (`none (all equal)`), so `round`
  is the lane round — no ambiguity for the counter.
* **Verdict vocabulary across mori rows** (all 85 rows): `improved` 156, `unchanged` 308,
  `harmed` 7, `unprovable` 15, `unprovable-but-better` 5.
  On **admitted-true** rows only: `improved` 135, `unchanged` 193, `unprovable-but-better` 1 —
  that single one is mori r36 under the **non-axis** key `freshness-technique` (not one of the six
  axes, so the counter's `axis in AXES` filter excludes it). All 15 `unprovable` verdicts and all
  7 `harmed` verdicts sit on admitted-false rows (harmed at mori r13 coverage/adjacency, r17
  adjacency, r20 freshness/calibration, r45 calibration, r88 operability — all `admitted: false`),
  so **no mori admitted-true row grades any axis `harmed`**. Hence every expected verdict word
  below is `improved`.

Raw:

```
all mori verdict values: {'improved': 156, 'unchanged': 308, 'harmed': 7, 'unprovable': 15, 'unprovable-but-better': 5}
admitted-true mori verdict values: {'improved': 135, 'unchanged': 193, 'unprovable-but-better': 1}
non-standard on admitted-true: [(550, 36, 'freshness-technique', 'unprovable-but-better')]
harmed rows: [(328, 13, 'coverage', False), (328, 13, 'adjacency', False), (373, 17, 'adjacency', False), (406, 20, 'freshness', False), (406, 20, 'calibration', False), (664, 45, 'calibration', False), (1223, 88, 'operability', False)]
```

(The tuple's first field there is the 1-based position; `550` = 0-based `rounds[549]` = mori r36.)
* **Omitted axis keys** (matters for the derivation, not a defect): admitted-true mori rows
  r36, r39, r56, r90, r93 omit axis keys entirely rather than saying `unchanged`. r93 omits
  `coverage, depth, freshness, adjacency` — that is why depth's latest admitted improvement is
  r86 and not r93.
* **Row-shape caveat for the new counter**: 11 mori rows (0-based `rounds[140]`, `rounds[142]`…
  `rounds[151]`; rounds 1–11)
  carry no `lane` key, only `lanes: {"mori": …}`, and have **no** `admitted`/`verdicts` keys.
  A counter filtering on `lane == "mori"` skips them; they carry no verdicts, so no expectation
  changes either way.

---

## 2. `Last change` convention and the six cells at 66c5518e

### 2a. The convention (from the SCORECARD's own correction paragraphs + the r79 counter docstring)

The lane states it twice in `SCORECARD.md`:

* Round-50 correction paragraph: *"`Last change` here means the latest admitted closure grading
  the axis improved or harmed, not the latest score move (a named limit of this convention:
  `.ufo/waves/round-50/a2w1/Mo50bCritAxesSemantics.md`)."*
* Round-79 correction paragraph: *"Each cell now leads with its latest admitted round and verdict
  word and keeps its older history after the first `;`; no score moved and no closure states a new
  number."*

The r79 counter docstring (`count-c2.py`) restates it as the frozen predicate: *"the `Last change`
cell's first `round N` equals N*, the highest mori lane round ≤ 78 that MANIFEST.json records with
`admitted: true` and that axis graded `improved` or `harmed`; and the text from that `round N` up to
the next `;` carries that verdict word."*

So: **`Last change` = the highest admitted mori closure grading that axis improved or harmed**
(r50/r79 convention). It is not the latest score move, and the score number is not part of it.

### 2b. The six cells, byte-exact, at 66c5518e

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 66c5518e239eeacd6070be26d78085ef702392cb:SCORECARD.md
```

`## Axes` table (parsed; `Last change` cells reproduced verbatim):

| Axis | Score | Last change cell (verbatim) | first round | verdict word | expected (unbounded) | state |
|---|---|---|---|---|---|---|
| coverage | 6 | `round 56 (improved, score held); round 47 (improved, score held); round 26 (improved, score held) before the round-50 correction` | 56 | improved | r80 improved | **MISMATCH** |
| operability | 7 | `round 78 (improved, score held); round 51 (improved, score held); round 47 (improved, score held); round 31 (improved, score held) before the round-50 correction; round-37 C2 re-attributed here (score held, 7)` | 78 | improved | r93 improved | **MISMATCH** |
| depth | 5 | `round 76 (improved, score held); round 51 (improved, score held); round 50 (improved, score held); round 49 (improved, score held); round 31 (improved, score held) before the round-50 correction` | 76 | improved | r86 improved | **MISMATCH** |
| freshness | 5 | `round 78 (improved, score held); round 28 (improved, score held); round-37 C2 is re-attributed to operability (round-38 axes-cell correction below) and round 38 claims no freshness move` | 78 | improved | r82 improved | **MISMATCH** |
| calibration | 5 | `round 78 (improved, score held); round 50 (improved, score held); round 49 (improved, score held); round 25 (improved, score held) before the round-50 correction; round-37 claim C1 closed the r36 measurement-discrimination defect and states no new number` | 78 | improved | r93 improved | **MISMATCH** |
| adjacency | 6 | `round 19 (improved, score held)` | 19 | improved | r19 improved | ok |

Parsing detail (raw tool output of the parse I ran):

```
[coverage] score='6'
  cell='round 56 (improved, score held); round 47 (improved, score held); round 26 (improved, score held) before the round-50 correction'
  first_round=56 verdict='improved' tail_after_round=' (improved, score held)'
[operability] score='7'
  cell='round 78 (improved, score held); round 51 (improved, score held); round 47 (improved, score held); round 31 (improved, score held) before the round-50 correction; round-37 C2 re-attributed here (score held, 7)'
  first_round=78 verdict='improved' tail_after_round=' (improved, score held)'
[depth] score='5'
  cell='round 76 (improved, score held); round 51 (improved, score held); round 50 (improved, score held); round 49 (improved, score held); round 31 (improved, score held) before the round-50 correction'
  first_round=76 verdict='improved' tail_after_round=' (improved, score held)'
[freshness] score='5'
  cell='round 78 (improved, score held); round 28 (improved, score held); round-37 C2 is re-attributed to operability (round-38 axes-cell correction below) and round 38 claims no freshness move'
  first_round=78 verdict='improved' tail_after_round=' (improved, score held)'
[calibration] score='5'
  cell='round 78 (improved, score held); round 50 (improved, score held); round 49 (improved, score held); round 25 (improved, score held) before the round-50 correction; round-37 claim C1 closed the r36 measurement-discrimination defect and states no new number'
  first_round=78 verdict='improved' tail_after_round=' (improved, score held)'
[adjacency] score='6'
  cell='round 19 (improved, score held)'
  first_round=19 verdict='improved' tail_after_round=' (improved, score held)'
```

**Cells whose first round number is NOT the highest admitted improved/harmed round: 5 of 6** —
coverage (56 vs 80), operability (78 vs 93), depth (76 vs 86), freshness (78 vs 82),
calibration (78 vs 93). Adjacency (19 vs 19) is correct. This is exactly the frozen before-state.

### 2c. Verdict-word spelling / formatting audit of the six cells

```
$ python3 ... re.findall(r"[A-Za-z]*[Ii]mproved[A-Za-z]*|[A-Za-z]*[Hh]armed[A-Za-z]*", cell) ...
coverage      verdict-ish token: 'improved'  x3   round tokens: ['round 56','round 47','round 26','round-50']   semicolons: 2
operability   verdict-ish token: 'improved'  x4   round tokens: ['round 78','round 51','round 47','round 31','round-50','round-37']  semicolons: 4
depth         verdict-ish token: 'improved'  x5   round tokens: ['round 76','round 51','round 50','round 49','round 31','round-50']  semicolons: 4
freshness     verdict-ish token: 'improved'  x2   round tokens: ['round 78','round 28','round-37','round-38','round 38']  semicolons: 2
calibration   verdict-ish token: 'improved'  x4   round tokens: ['round 78','round 50','round 49','round 25','round-50','round-37']  semicolons: 4
adjacency     verdict-ish token: 'improved'  x1   round tokens: ['round 19']  semicolons: 0
```

Findings: **no spelling deviations.** Every verdict word is the lowercase token `improved`
(no `Improved`, no `improved.`, no `harmed`, no trailing whitespace inside the leading clause).
`harmed` appears in no `Last change` cell (and no mori admitted-true row grades an axis harmed,
so no cell may legitimately say `harmed` today).

Two structural traps a new counter must survive (both visible above):

1. **Hyphenated round tokens do not match `round\s+(\d+)`**: `round-50`, `round-37`, `round-38`
   appear inside cells. The r79 `ROUND` regex is `re.compile(r"round\s+(\d+)", re.I)`, so
   `round-50` is *not* a round number — correct, but only by accident of the space requirement.
2. **Later clauses carry their own round numbers**, including a bare `round 38` in the freshness
   cell (the r38 axes-cell correction sentence) and `round 31`/`round 47`/`round 49`/`round 50`/
   `round 51` in the other cells' history clauses. The convention is **the leading clause only**
   (first `round N`, verdict word before the first `;`). At 66c5518e the leading clause happens
   to hold the largest round number in all six cells, so a "max over the whole cell"
   implementation would coincidentally agree with the convention here — but it would break the
   moment a landing cell's leading clause is *not* the largest (e.g. the freshness cell's
   second clause `round 28` is smaller than its leading `round 78`, while the freshness cell's
   trailing `round 38` is larger than that `round 28` but smaller than the leading `round 78`).
   The r79 counter avoids this by construction: `ROUND.search(cell)` takes the *first* match
   and `cell[m.end():].split(";")[0]` takes only the first clause.

### 2d. `Score` and `Evidence pointer` cell bytes at 66c5518e (the P1 "COLUMNS_UNCHANGED" baseline)

```
axis | sha256(stripped Score) | sha256(stripped Evidence) | sha256(stripped Last change)
coverage | e7f6c011776e8db7cd330b54174fd76f7d0216b612387a5ffcfb81e6f0919683 | f7857b7b198ce572ade7402ab7f1ebeaa83f3d34fd709ee2675a36e9cdbb65f0 | cbfc6bae5d069bdfcc16025786cf52754651e7795a463e19d281b1007d35340d
operability | 7902699be42c8a8e46fbbb4501726517e86b22c56a189f7625a6da49081b2451 | 34244dec6cbb2679335ecff400212eb80fa73f56fa83b79e1b90f5ace62acc34 | 1a5e4e10b3f8151c9678ad3857d9229beadc723ca386f7b96d64ba05f8c54d0c
depth | ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d | 06caf1e18281f34d21dc93b8119b2484068f6aa1f0fa0c78e5104214040dcb98 | fbf230715c97b159efb66cac28175b6d1e79b628b0c04662aa08b30ef6acf7e0
freshness | ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d | 03c2174408e5c1a28ca0cfe671e63d8cf73bb8c347975617a5f3075d27f79783 | 77e1b46adf9e56113796ef818d9f694f5d3a7b0e960023672f6aa50498ecbae4
calibration | ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d | 71fd0c7c38b44f2ac7476e5d65cf95f14bb88d431f831249fd005ffe318053dd | ac55b692ecc18995707e1031a53dec5a579ed4d8a2e1b6a90e54e959d013bcc6
adjacency | e7f6c011776e8db7cd330b54174fd76f7d0216b612387a5ffcfb81e6f0919683 | 0d6164df1e4f18374beadfdce03b6579253e41db85d2dd3e75b79a72229bd625 | 5abc9eeaa5f261dc36d9c79e9aeab2d130d9d6b8fbbbc65a048bf3854e3a15ed
```

Scores are `6 / 7 / 5 / 5 / 5 / 6` — identical values for coverage and adjacency
(sha `e7f6c011…`) and for depth/freshness/calibration (sha `ef2d127d…`); the six `Last change`
digests are all distinct from their Score/Evidence digests, i.e. a byte-equality check on the
Score/Evidence columns is well-defined.

---

## 3. Where the frozen round-79 counter departs from the contract's P1

`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-79/count-c2.py` (not amended, per the
contract). Its expectation logic is `expectations(manifest, through)`:

```python
def expectations(manifest, through):
    last = {}; rows = 0
    for r in data.get("rounds") or []:
        if r.get("lane") != LANE or not r.get("admitted"):
            continue
        rn = r.get("round")
        if not isinstance(rn, int) or rn > through:
            continue
        rows += 1
        for axis, verdict in (r.get("verdicts") or {}).items():
            if axis in AXES and verdict in ("improved", "harmed"):
                if axis not in last or rn > last[axis][0]:
                    last[axis] = (rn, verdict)
    return last, rows
```

**Paragraph.** The frozen counter and the contract's P1 agree on the *shape* of the predicate — the
`Last change` cell must lead with the round and verdict word of the highest admitted mori closure
grading that axis improved or harmed, and the verdict word must sit between that round number and
the next `;` — but they differ in three places that change the answer, plus one that the contract
adds and the counter never implemented. (i) **The bound.** The counter filters
`rn > through` with `THROUGH = 78` as its default, so at its default invocation it considers only
manifest rounds 1–78 and reports `C2=met … mismatches=0`; P1 says explicitly *"any round, no
bound"*, so the same counter at `--through 95` reports `mismatches=5` at the same revision. The
frozen counter is therefore a *bounded* instrument being asked to certify an *unbounded* claim,
and at its default bound it certifies the wrong thing (rows=46 at THROUGH=78 vs rows=58 at 95).
(ii) **The admitted filter combined with the bound.** The counter does count only admitted rows
(`not r.get("admitted")` skips them) exactly as P1 requires, but because the bound is applied to
the *same* row set, the admitted rows of rounds 79–95 are discarded before the admitted test can
matter; the admitted filter is therefore doing no work at the default bound, and the two defects
mask each other. (iii) **The `;` split.** The counter grades the cell by taking the first
`round\s+(\d+)` match anywhere in the cell and then searching for the verdict word only in
`cell[m.end():].split(";")[0]` — it requires the verdict word to appear in the leading
semicolon-delimited clause. P1's phrasing ("leads with the round and verdict word") is the same
idea, but the counter's mechanism is stricter in one respect (the verdict must precede the first
`;`, not merely appear somewhere in the cell) and looser in another (the round match is searched
across the whole cell rather than required to be the leading token, so a cell like
`foo round 5; round 80 (improved…)` would be graded as round 5). (iv) **The contract adds a
column check the counter does not have.** P1 also requires that *the `Score` and `Evidence pointer`
cells equal their bytes at `66c5518e239eeacd6070be26d78085ef702392cb`*, and the contract's
"Met iff" clause names `COLUMNS_UNCHANGED` — but the r79 counter explicitly names the opposite as
its own limitation (*"Named limit: the `Evidence` cell is not graded (the r50 counter graded it);
only the `Last change` clause is in scope"*) and never reads the `Score` or `Evidence pointer`
columns. So the frozen counter can report `met` while the score column has drifted. Two further
tacit behaviours the new counter should state explicitly rather than inherit silently: the
counter's tie-break `rn > last[axis][0]` is **first-row-wins on equal round numbers** (a later
manifest row for the same round can never override an earlier one), whereas the manifest's own
`closure-correction` convention (see `rounds[1313]` with `supersedes`) implies **last-row-wins**;
and the counter ignores `type` entirely, so it would treat a `closure-correction` row exactly like
a `closure` row (harmless today — the sole mori correction is `admitted: false` — but it should be
spelled out in the new counter). There is also a smaller robustness gap: the counter's
`ROUND.search` is a plain first-match scan, so it is only correct because every cell's leading
clause is also its maximum round number — the `freshness` cell contains a later `round 38` and the
`operability` cell a later `round 37`, so a "max over the whole cell" implementation of P1 would be
wrong in general.

Raw evidence for (i):

```
$ HYAKU_SCRATCH=/fast/scratch/hyaku python3 .../.ufo/waves/round-79/count-c2.py 66c5518e239eeacd6070be26d78085ef702392cb --through 95 --manifest /home/vgpnk/Projects/shokunin/MANIFEST.json ; echo "exit=$?"
axis coverage cell=round_56_improved expect=round_80_improved state=mismatch
axis operability cell=round_78_improved expect=round_93_improved state=mismatch
axis depth cell=round_76_improved expect=round_86_improved state=mismatch
axis freshness cell=round_78_improved expect=round_82_improved state=mismatch
axis calibration cell=round_78_improved expect=round_93_improved state=mismatch
axis adjacency cell=round_19_improved expect=round_19_improved state=ok
C2=unmet axes=6 mismatches=5 errors=0 rows=58 through=95 rev=66c5518e239e
exit=1

$ HYAKU_SCRATCH=/fast/scratch/hyaku python3 .../.ufo/waves/round-79/count-c2.py 66c5518e239eeacd6070be26d78085ef702392cb --manifest /home/vgpnk/Projects/shokunin/MANIFEST.json ; echo "exit=$?"
axis coverage cell=round_56_improved expect=round_56_improved state=ok
axis operability cell=round_78_improved expect=round_78_improved state=ok
axis depth cell=round_76_improved expect=round_76_improved state=ok
axis freshness cell=round_78_improved expect=round_78_improved state=ok
axis calibration cell=round_78_improved expect=round_78_improved state=ok
axis adjacency cell=round_19_improved expect=round_19_improved state=ok
C2=met axes=6 mismatches=0 errors=0 rows=46 through=78 rev=66c5518e239e
exit=0
```

Both lines are byte-identical to the frozen receipts
`.ufo/waves/round-96/evidence/before-c1-count-c2-through95.txt` and
`.ufo/waves/round-96/evidence/before-c1-count-c2-default.txt` — my independent re-run reproduces
the claimed before-state (5 mismatches at `--through 95`; met at the default bound).

Frozen counter's own selftest, re-run unmodified (read-only, it writes only into a temp dir under
`HYAKU_SCRATCH`):

```
$ HYAKU_SCRATCH=/fast/scratch/hyaku python3 .../.ufo/waves/round-79/count-c2.py --selftest ; echo "exit=$?"
PASS conformant_met met=True
PASS stale_cell_unmet met=False
PASS verdict_word_missing_unmet met=False
PASS subsumed_by_higher_round_unmet met=False
PASS nonadmitted_below_ceiling_ignored_met met=True
PASS verdict_after_clause_boundary_unmet met=False
PASS later_round_in_cell_ignored_unmet met=False
C2_COUNTER_SELFTEST pass=7 fail=0
exit=0
```

(7 arms — note the SCORECARD's round-79 paragraph says "the counter's own selftest 4/4"; the file
now has 7 arms. The frozen counter must not be amended, so the new counter writes its own.)

---

## 4. Expected per-axis cell table the new counter should derive

Unbounded (P1: any round, no `through` bound), lane `mori`, `admitted: true`, verdict word
`improved` or `harmed`. MANIFEST index given both ways: **0-based `rounds[]` index** is the
convention the SCORECARD itself cites (`fleet MANIFEST.json rounds[398]` for mori round 19 — and
`rounds[398]` is indeed the mori r19 admitted-true row); 1-based position is given for convenience.

| Axis | Expected round | Expected verdict | MANIFEST 0-based index (`rounds[]`) | 1-based position | Current cell at 66c5518e | Action for the landing revision |
|---|---|---|---|---|---|---|
| coverage | **80** | improved | `rounds[1163]` | 1164 | `round 56 (improved, score held); …` | prepend `round 80 (improved, score held); ` |
| operability | **93** | improved | `rounds[1327]` | 1328 | `round 78 (improved, score held); …` | prepend `round 93 (improved, score held); ` |
| depth | **86** | improved | `rounds[1205]` | 1206 | `round 76 (improved, score held); …` | prepend `round 86 (improved, score held); ` |
| freshness | **82** | improved | `rounds[1175]` | 1176 | `round 78 (improved, score held); …` | prepend `round 82 (improved, score held); ` |
| calibration | **93** | improved | `rounds[1327]` | 1328 | `round 78 (improved, score held); …` | prepend `round 93 (improved, score held); ` |
| adjacency | **19** | improved | `rounds[398]` | 399 | `round 19 (improved, score held)` | no change (already correct) |

Raw derivation (unbounded, no `through`) — re-run against the **current** 1342-row manifest after
the append:

```
$ python3 - <<'EOF'
import json, collections
d=json.load(open('/home/vgpnk/Projects/shokunin/MANIFEST.json'))
rs=d['rounds']
AX=["coverage","operability","depth","freshness","calibration","adjacency"]
mori=[(i,r) for i,r in enumerate(rs) if r.get('lane')=='mori']
last={}
for i,r in mori:
    if r.get('admitted') is not True: continue
    rn=r.get('round')
    for ax,v in (r.get('verdicts') or {}).items():
        if ax in AX and v in ('improved','harmed'):
            if ax not in last or rn>last[ax][0]: last[ax]=(rn,v,i)
print('--- unbounded expected: (round, verdict, 0-based rounds[] index) ---')
for a in AX: print(' ', a, last[a])
EOF
--- unbounded expected: (round, verdict, 0-based rounds[] index) ---
  coverage (80, 'improved', 1163)
  operability (93, 'improved', 1327)
  depth (86, 'improved', 1205)
  freshness (82, 'improved', 1175)
  calibration (93, 'improved', 1327)
  adjacency (19, 'improved', 398)
```

(The same derivation run against the earlier 1340-row manifest returned identical
rounds/verdicts and the identical 0-based indices 1163 / 1327 / 1205 / 1175 / 1327 / 398 — the two
appended rows sit after every mori row, so no index moved.)

Source rows for the expected cells (verbatim `verdicts`):

```
rounds[1163]  mori r80  admitted True  {'calibration':'improved','operability':'improved','coverage':'improved','depth':'unchanged','freshness':'unchanged','adjacency':'unchanged'}
rounds[1175]  mori r82  admitted True  {'operability':'improved','freshness':'improved','depth':'improved','coverage':'unchanged','calibration':'unchanged','adjacency':'unchanged'}
rounds[1205]  mori r86  admitted True  {'operability':'improved','calibration':'improved','depth':'improved','coverage':'unchanged','freshness':'unchanged','adjacency':'unchanged'}
rounds[1327]  mori r93  admitted True  {'calibration':'improved','operability':'improved'}
rounds[398]   mori r19  admitted True  {'adjacency':'improved','calibration':'improved','depth':'unchanged','coverage':'unchanged','operability':'unchanged','freshness':'unchanged'}
```

This table matches the contract's stated target exactly ("coverage r80 improved; operability r93
improved; depth r86 improved; freshness r82 improved; calibration r93 improved"), computed
independently from the manifest.

Counter-design consequences the executor should honour (from §1–§3):

1. Bound must be **unbounded** (no `through` default); the counter must still accept an explicit
   bound if given, but the default/graded mode must consider every manifest round.
2. Admission filter: `lane == "mori"` **and** `admitted is True` (bool); the manifest is clean
   (`bool` on all 85 mori rows), but `is True` is stricter than the r79 truthiness test and matches
   P1's "admitted: true".
3. Tie-break on equal round numbers: **last admitted row wins** (manifest `closure-correction`
   semantics), not the r79 first-wins. Only r91 duplicates today and both are admitted-false.
4. Grading must read the **leading clause only**: first `round\s+(\d+)` (so hyphenated
   `round-50`/`round-37`/`round-38` are not round numbers) and the verdict word from
   `cell[match.end():].split(";")[0]`.
5. `Score` and `Evidence pointer` columns must be byte-compared against 66c5518e
   (`COLUMNS_UNCHANGED`), using the §2d digests (or by comparing the two git blobs directly).
6. A stale-cell selftest arm that is **unmet** is required by the contract; the r79 counter has one
   (`stale_cell_unmet`), but the new counter needs its own.

---

## 5. Checks NOT run (named, not implied)

* **C2 (freshness) was not measured by this seat** — out of the assigned scope (C1 reconnaissance
  only). `tools/mori-source-digest.py corpus/SOURCES.md corpus/evidence` was **not run**; the
  claimed `unpinned=6` is not re-verified here (DigestSeat territory).
* `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` — **not run**.
* The new counter `tools/mori-scorecard-calibration.py` — **does not exist yet** and was **not
  written or run** by this seat (read-only scout role; CalibExec's deliverable).
* No `--selftest` of a round-96 counter, no post-edit SCORECARD measurement, no landing-revision
  verification — the landing revision does not exist yet.
* No `git` mutation of any kind was performed; no commit/push/`fleet-commit.sh`/`jj-lane.sh`.
* Host sysctls/services/limits were not touched.
* The §2d digests were produced by one hashing run; the `calibration` Evidence digest was
  re-verified in a second run against the same blob and matched
  (`71fd0c7c38b44f2ac7476e5d65cf95f14bb88d431f831249fd005ffe318053dd`).
* `MANIFEST.json` was read from the fleet worktree, not from a git blob; I confirmed the worktree
  blob hash equals `HEAD:MANIFEST.json` (`23f2ecd3ea234552ee090e9ef2a87b78c2608039` at the final
  read), so the two are the same bytes at the fleet HEAD.
* The `## Axes` table in SCORECARD.md was parsed from the `git show` blob of 66c5518e, not from
  the lane worktree file; the two are the same bytes —
  `git hash-object SCORECARD.md` = `698d278f2a22f74f3b196d7acec233fd2b980234` =
  `git rev-parse 66c5518e239eeacd6070be26d78085ef702392cb:SCORECARD.md`. The only untracked
  paths in the lane are `.ufo/waves/round-96/w1.ready.dispatched` and `.ufo/waves/round-96/w1/`.
* Tooling installs: **none** (nothing installed; pacman not run; `~/.local/bin` untouched).
