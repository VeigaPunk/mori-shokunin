# Mo90K01Conn — cross-round pin map for the two r90 landings

Axes: operability (C1), calibration (C2). Read-only; measured at
`d1c8488986512a6a0475af88cc52779ce4703e00` (`git rev-parse HEAD` = same).

Selftest arm counts measured by running each counter's `--selftest` at the tip
(`HYAKU_SCRATCH=$(mktemp -d)`, all rc=0):

| file | arms (measured) | internal pin |
|---|---|---|
| round-87/count-c2.py (the gate, C1 subject) | `C2_COUNTER_SELFTEST pass=26 fail=0` | none — no `EXPECTED_ARMS`/`own_arms_pinned` (gap noted in `round-87/w1/Mo87M01Mut.md:272`) |
| round-88/count-c1.py (C2 subject) | `C1_COUNTER_SELFTEST pass=28 fail=0` | `EXPECTED_ARMS = 28` (:76), `own_arms_pinned` arm (:344) |
| round-88/count-c2.py (C2 subject) | `C2_COUNTER_SELFTEST pass=26 fail=0` | none — arm count pinned only externally |
| round-89/count-c1.py | `pass=15` | `EXPECTED_ARMS = 15` (:217) |
| round-89/count-c2.py | `pass=17` | `EXPECTED_ARMS = 17` (:85) |
| round-90/count-c1.py | `pass=12` | `EXPECTED_ARMS = 12` (:67) |
| round-90/count-c2.py | `pass=21` | `EXPECTED_ARMS = 21` (:109) |

All 15 r90-C2 mutant anchors occur exactly once in the current r88 subjects
(verified by `git show <tip>:<path>` + `str.count` per anchor: all `count=1`).

## 1. Pins the C1 landing (gate edit) moves — IF it adds selftest arms

The frozen P-C1 predicate does not name a gate arm count, so a landing that adds
**zero** selftest arms moves nothing below. A landing that adds arms (the lane's
arm-per-clause convention) changes `pass=26` → `pass=N` and activates every pin
below. Current candidate spec (`w1-dispatch.json` Mo90E01Gate) says "copy of the
committed file plus your change … a subtract-only reachability pre-pass inside
`binds`" — it does not order new arms either way.

| file:line | pin | now | after gate arm bump | verdict |
|---|---|---|---|---|
| `round-88/count-c2.py:34` | `SUBJECT_ARMS = 26` | 26 | stale (gate = N) | frozen historical instrument; its own predicate is superseded, not rewritten |
| `round-88/count-c2.py:38` | `TARGET = "real=met fx=4 clean=1 refused=2 absent=1 arms=26"` | arms=26 | stale | same |
| `round-88/count-c2.py:264` | `target_fields` arm requires `"arms=26"` in TARGET | literal 26 | fails if TARGET edited | see §3 — editing it breaks r90 C2 |
| `round-88/count-c2.py:265` | `arms_pinned` arm: `SUBJECT_ARMS == 26` | 26 | fails if edited | same |
| `round-88/count-c2.py:267` | `target_full` arm: exact TARGET literal | arms=26 | fails if edited | same |
| `round-88/count-c2.py:282-284` | `own_ok_red` arm fixtures `pass=26 fail=0` | literal 26 | still self-consistent (fixture strings, not gate-derived) | unaffected unless literals edited |
| `round-88/count-c2.py:353` | `subject_ok = … arms == (SUBJECT_ARMS, 0)` | pins 26 | reads `subject=arms:(N,0)` unmet at after-rev | expected: counter is frozen at its own round |
| `round-89/count-c1.py:30` | `SUBJECT_ARMS = 26` | 26 | stale | frozen historical |
| `round-89/count-c1.py:34` | `TARGET = "equiv=accepted … arms=26"` | arms=26 | stale | frozen historical |
| `round-89/count-c1.py:201-205` | `target_fields` + `arms_pinned` arms pin `"arms=26"`/`SUBJECT_ARMS == 26` | 26 | fail if edited | same |
| `round-89/count-c1.py:267` | `subject_ok = … arms == (SUBJECT_ARMS, 0)` | pins 26 | unmet at after-rev | frozen historical |
| `round-90/count-c1.py` | — | — | **no arm pin**: `tally()` calls only `binding_problems`; `selftest()` uses synthetic gates | unaffected either way |
| `round-90/count-c2.py` | — | — | subjects are the two r88 counters, not the gate | unaffected |
| `round-89/noharm-c1.py`, `round-89/heldout-c1.py` | `ENTERING = "30a29797…"` (:35/:36), `GATE` path (:33/:34) | rev-pinned | no arm pin; `binding_problems` signature has `repo=None` + `TypeError` fallback (:52-56/:64-68) | compatible with any signature-preserving gate edit; at after-rev `heldout` should read `open=22` (matches frozen `open=22`), `noharm` unchanged |

**Superseded-by-landing (named, not rewritten):** the r88-c2 and r89-c1 arm pins
above are *receipts of a past measurement*, not live obligations. Nothing in the
lane re-runs them at the after-rev; their after-receipts bind their own counter
bytes (§4). If the gate's arm count moves, the correct disposition is a
scorecard/lesson note that `arms=26` pins are historical — exactly the pattern r89
used when it moved the gate 23 → 26 (`round-89/w1/Mo89K01Conn.md:90` documents the
same migration).

## 2. Pins the C2 landing (r88 counter arm bumps) moves

Landing target per frozen counter: `ARMS_BY_FILE = {"count-c1.py": 29,
"count-c2.py": 27}` (`round-90/count-c2.py:49`), `TARGET … arms=29,27` (:102-103).
`arm_list` records each subject's pristine `--selftest` pass count in sorted-path
order → count-c1 must print 29, count-c2 must print 27.

| file:line | pin | now | after landing | verdict |
|---|---|---|---|---|
| `round-88/count-c1.py:76` | `EXPECTED_ARMS = 28` | 28 | must be 29 (candidate `w1/candidates/r88-count-c1.py` already does this) | required by landing |
| `round-88/count-c1.py:344-345` | `own_arms_pinned`: `len(cases)+1 == EXPECTED_ARMS` | 28/28 | 29/29 | self-adjusts via constant |
| `round-88/count-c1.py:109` | `own_ok_of` regex `pass=%d fail=0 % EXPECTED_ARMS` | dynamic | dynamic | B1 anchor lives here — preserved |
| `round-88/count-c1.py:337-339` | `own_ok_red` fixtures use `% EXPECTED_ARMS` | dynamic | dynamic | unaffected |
| `round-88/count-c1.py:280-282` | `per_file_arms_frozen`/`TARGET_ARMS=24`/`target_split` | pin the **r87 count-c1** subject at 24 | unchanged — different subject | unaffected |
| `round-88/count-c2.py` | no `EXPECTED_ARMS` | — | spec error: E03 prompt says "bump EXPECTED_ARMS 26 -> 27" but no such constant exists in this file | see §5 defect |
| `round-89/count-c2.py:39` | `ARMS_BY_FILE = {"count-c1.py": 28, "count-c2.py": 26}` | 28/26 | stale (29/27) | frozen historical; reads `pristine-arms … want=28/26` unmet at after-rev — superseded, not rewritten |
| `round-89/count-c2.py:81` | `TARGET = "… arms=28,26"` | 28,26 | stale | same |
| `round-89/count-c2.py:142` | `target_split` expects `"28,26"` | 28,26 | unmet at after-rev | same |
| `round-89/count-c2.py:300` | `arms_pinned` arm literal `{"count-c1.py": 28, "count-c2.py": 26}` | 28/26 | fails if edited | do not edit — frozen instrument |
| `round-89/count-c2.py` MUTANTS anchors on r88 subjects | 12 anchors in `round-89/count-c2.py:41-79` | occur once at tip | **must be re-checked against after-bytes**: landing adds arms but must not disturb the 12 anchored strings; the three new arms are appended so old anchors survive (candidate diff confirms for count-c1; count-c2 pending) | landing risk, not a pin |
| `round-89/count-c1.py` | subjects = r87 gate only | — | unaffected by C2 | — |

## 3. The hard cross-landing contradiction (state explicitly)

`round-90/count-c2.py:62-63` mutant `C2-target` anchors on the **literal**
`TARGET = "real=met fx=4 clean=1 refused=2 absent=1 arms=26"` in the after-bytes of
`round-88/count-c2.py` (occurs once at tip — verified). That `arms=26` is the
**gate's** arm count (r88-c2's subject is the r87 gate), frozen when the gate had
26 arms.

If the C1 landing bumps the gate to N≠26 arms, then r88-c2's `SUBJECT_ARMS`/`TARGET`
become *false statements about the current gate*. Two options, both costly:

- **Edit them** (`arms=26`→`arms=N`): the `C2-target` anchor count drops to 0 →
  `unanchored` → **frozen P-C2 unmet**. Forbidden.
- **Leave them**: r88-c2 carries a pin that is false at the after-rev. Acceptable
  only because the counter is a frozen historical instrument (its own round-88
  predicate was measured at `d5e2eda4`), but it must be *named superseded* in the
  r90 report/lesson — the same disclosure r89 made for its own moved pins.

The same applies symmetrically: r90-C2's `C2-printed-target`/`met_line_derived`
anchors and the `arms=26` fixture literals at `round-88/count-c2.py:282-284`
(`pass=26 fail=0`) are all consistent only while the gate stays at 26 arms **or**
while nobody edits those literals. The literals are fixture strings for
`own_ok_of`'s rc/fail parsing — they do not read the gate — so they stay valid
regardless; only `SUBJECT_ARMS`/`TARGET`/`arms_pinned`/`target_fields`/
`target_full`/`subject_ok` go stale, and only if the gate's count moves.

**Recommendation to L1:** prefer a gate landing that adds the reachability rule
*without* new selftest arms if that keeps P-C1 met (the predicate does not require
arms); otherwise land the arms and mark every `arms=26` pin above superseded in
the round report. Do not edit the pinned literals — the frozen r90 counter reads
the after-bytes.

## 4. `# counter-sha256:` bindings — do they break?

Binding semantics (verified `round-87/count-c2.py:489-495`):
`sha256_at(repo, fields["rev"], bpath)` — the digest is checked against the bound
path **at the receipt's own `# rev:`**, inside `grade_population`. HEAD edits do
not reach it.

| receipt | binds | stays valid? |
|---|---|---|
| `round-87/evidence/after-r87.txt:5` | `round-87/count-c2.py` @ `264a43f0…` | **yes** — replay clone checks out `b9e6f68d`, where those bytes live |
| `round-88/evidence/after-r88.txt:4-5` | `round-88/count-c1.py` @ `3ba0f97b…`, `count-c2.py` @ `8904a3d0…` | **yes** — `# rev: d5e2eda4` |
| `round-89/evidence/after-r89.txt:4-6` | r89 counters @ `f8e6c39e…`/`40eacccc…`/`3b8c7b14…` | **yes** — `# rev: 9f4d20b9`; already superseded by after-r89-final per scorecard |
| `round-89/evidence/after-r89-final.txt:4-7` | r89 counters + noharm/heldout | **yes** — `# rev: 7715bb56` |
| `round-90/evidence/controls-r90.txt:5-6` | r90 counters (pre-data control) | n/a — binds r90 counter bytes, not subjects |

**None break.** The bindings pin counter bytes *at a named revision*; the landings
edit the same paths at a *later* revision. This is exactly why r89 could move the
gate 23→26 without invalidating `after-r87.txt`/`after-r88.txt`.

Caveat: `round-88/w1/Mo88Si01Simplify.md:140` already flagged that deleting the
dead `want_met` in r88-c2 would change sha `8904a3d0…`→`271218503e…` — that
receipt binds the *old* bytes at `d5e2eda4`, so even that edit leaves the receipt
valid; it only matters for byte-identity claims in prose.

## 5. Defects / contradictions found (state, do not smooth)

1. **`arms=29,27` vs "two new arms" in r88-c2.** r88-c2 has 26 arms and **no**
   `EXPECTED_ARMS` constant. E03's prompt says "exactly TWO new arms, then bump
   EXPECTED_ARMS 26 -> 27" — there is no such constant in count-c2.py (it exists
   only in count-c1.py), and two appended arms yield 28, not the frozen 27.
   Either the landing merges B4+B6 coverage into one arm, removes an existing
   arm, or the frozen `arms=29,27` is wrong (should be `29,28`). The L1 must
   resolve before integration; the frozen counter will read `pristine-arms
   count-c2.py arms=28 want=27` → unmet if 28 lands.
2. **`arms=26` pins are load-bearing frozen anchors.** `round-90/count-c2.py:62`
   makes `TARGET = "…arms=26"` an exact-once anchor; any "truthfulness" edit to
   r88-c2's TARGET under a gate arm bump breaks P-C2. The pins must be left stale
   and named superseded — contradiction between instrument truth and frozen
   counter, disclosed not resolved.
3. **r88-c2 has no self-count pin.** Unlike count-c1 (`EXPECTED_ARMS` +
   `own_arms_pinned`), count-c2's arm count is pinned only externally
   (`round-89/count-c2.py:39,300`). The r90 landing is the first round to pin it
   via `ARMS_BY_FILE` — fine — but the file's own docstring/arms table will drift
   if arms are added without a matching internal pin.
4. **`w1-dispatch.json` E01Gate prompt truncation** — the frozen class list is cut
   mid-sentence at "H09…" in the dispatch JSON I read; the authoritative list is
   `BRANCH` in `round-90/count-c1.py:55-64` (8 ids, verified). Not a defect in the
   lane, noted so nobody treats the dispatch text as the class definition.

## Verification commands run

- `git -C …/mori-shokunin rev-parse HEAD` → `d1c8488986512a6a0475af88cc52779ce4703e00`
- `python3 -I <each counter> --selftest` for all seven counters → tallies above, all rc=0
- anchor occurrence counts: AST-extracted `MUTANTS` from `round-90/count-c2.py`,
  `git show <tip>:<subject>` + `str.count(old)` → all 15 anchors `count=1`
- `grep -rn "counter-sha256" .ufo/waves/**/evidence/*.txt` + receipt header reads
- `round-87/count-c2.py:489-495` read for sha-binding semantics
