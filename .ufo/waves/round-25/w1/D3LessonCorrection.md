# D3 LessonCorrection — round-24.md supplementary-file count (C1 item D3)

Seat: `MoriR25.D3LessonCorrection` (leaf scribe). Lane: `mori-shokunin`.
Date: 2026-10-22. All commands run read-only in the lane (no git/jj mutation, no
`~/.omp` writes, no omp runs; tools run with `python3 -I` / `bash`).

## 1. The mismatch (item D3)

`corpus/lessons/round-24.md:79-80` says:

> a co-evolved file `tools/fixtures/mori-pressure/supplementary-cases.json` (S01–S06)
> covers the threshold edge, the three grammar shapes, HIGH over PARTIAL and EPERM
> (`PASS 6/6`).

Committed bytes disagree. The file at `4f05dd5a` and at HEAD has **7** cases,
S01–S07:

- `git show 4f05dd5a:tools/fixtures/mori-pressure/supplementary-cases.json | python3 -I -c "import json,sys; print([c['id'] for c in json.load(sys.stdin)['cases']])"`
  → `['S01','S02','S03','S04','S05','S06','S07']`.
- `git diff --stat 4f05dd5a HEAD -- tools/fixtures/mori-pressure/supplementary-cases.json`
  → empty (unchanged since `4f05dd5a`).
- `python3 -I tools/mori-pressure.py --selftest --cases tools/fixtures/mori-pressure/supplementary-cases.json`
  → `MORI_PRESSURE_SELFTEST: PASS 7/7`, then `MATCHER: rejected 28/28 corrupted expectations`,
  exit 0.

Origin: the lines were added by commit `a536b18` (round-24: knowledge corrections after
wave-2 falsification; …), where they were accurate at the time — the supplementary file then
held S01–S06 (added by `89849a7`). S07 was added later by commit `c484f6d`
(round-24: threshold still applies to a regressed counter (A3); supplementary S07; knowledge
body made consistent with its corrections; 2026-10-22 06:20:36 -0300; +43 lines in the
fixture). The lesson was not updated afterwards (`a536b18` is an ancestor of `c484f6d`,
which is an ancestor of `4f05dd5a`). The round-24 SCORECARD section already states the
correct value (`SCORECARD.md:1521`: `PASS 7/7`); the lesson line is the stale one.

### Draft appended correction paragraph (for L1 to append at the end of `corpus/lessons/round-24.md`)

> **Correction (D3).** The mutation-results paragraph above (lines 79–80) says the
> co-evolved supplementary file `tools/fixtures/mori-pressure/supplementary-cases.json`
> covers S01–S06 with `PASS 6/6`. Committed bytes disagree: at `4f05dd5a` (and HEAD) the
> file holds seven cases S01–S07; S07 (a regressed memory counter must not hide a threshold
> breach on the second read, A3) was added by commit `c484f6d`, and
> `python3 -I tools/mori-pressure.py --selftest --cases tools/fixtures/mori-pressure/supplementary-cases.json`
> prints `MORI_PRESSURE_SELFTEST: PASS 7/7` (exit 0). The round-24 SCORECARD section
> (`SCORECARD.md:1521`) already records `PASS 7/7`; lines 79–80 are left as written and this
> paragraph is the correction record.

## 2. Sweep of round-24.md and SCORECARD.md round-24 section (lines 1494–1531)

Every count claim was checked against committed bytes. All verified matches are listed with
the command that shows them; the only disagreements are §3.

Verified ✓:

1. **Frozen case count 12** (lesson line 70; SCORECARD 1502/1514/1530) —
   `git show 4f05dd5a:tools/fixtures/mori-pressure/cases.json | python3 -I -c "import json,sys; print(len(json.load(sys.stdin)['cases']))"`
   → `12`; ids P01–P12.
2. **Tool blob `852d1ea7`** (lesson line 70, 569 lines) —
   `git show a730ecf:tools/mori-pressure.py | sha256sum` →
   `852d1ea7508004dc44690bb6e358625fbd07d89c26d4196793133559d8a773a5`;
   `git show a730ecf:tools/mori-pressure.py | wc -l` → `569`.
3. **MATCHER: rejected 48/48** (lesson lines 77–78; SCORECARD 1514) —
   `python3 -I tools/mori-pressure.py --selftest` → `PASS 12/12`, `MATCHER: rejected 48/48
   corrupted expectations`, exit 0.
4. **Supplementary `PASS 7/7`** (SCORECARD 1521) — command in §1; this is the value the
   lesson should carry.
5. **C1 after: held 4 of items 4** (SCORECARD 1501/1513) —
   `python3 -I tools/mori-routed-check.py --repo . --rev HEAD --round 24` → JSON
   `"held":4,"items":4`, exit 0.
6. **C1 before: held 3 of 4, R4 red, 8 ledger rows `at` after dispatch commit**
   (SCORECARD 1513; lesson line 82) — `python3 -I tools/mori-routed-check.py --repo . --rev
   c725aa37 --round 23` → `held 3 items 4`, R4 reasons include exactly 8
   `dispatch_committed_after_dispatch`; `.ufo/waves/round-24/evidence/c1-before-round23.json`
   → `held 3` and Counter has 8 `dispatch_committed_after_dispatch`; also
   `c1-before-round24.json` → `held 3`, R4 false.
7. **Live bracket check 5 of 5** (SCORECARD 1518) — `.ufo/waves/round-24/evidence/bracket-check-run.json`
   → `"runs":5,"passed":5`.
8. **Census selftest 134/134/0** (SCORECARD 1522) —
   `bash tools/mori-census.sh --selftest` → `MORI_CENSUS_SELFTEST: PASS (134 cases, 134
   passed, 0 failed)`, exit 0 (wall 13.8 s); `git ls-tree c725aa37 -- tools/mori-census.sh`
   → blob `c7d952d6fabe3137a91b9afbea991317ceba1f3e` (matches CensusNoHarmAfter.md).
9. **Source digests first-16-hex** (Gate table lines 25–32) — `curl -sS <url> | sha256sum |
   cut -c1-16` matches all six S090–S096 (`11c6b7129103b454`, `452318beaca3e6d1`,
   `a9433bb0e16a67f0`, `a43f09d89309a6bd`, `23b1a690210b6884`, `483269b27c82b438`);
   S097 404 body → `80c3fe2ae1062abf` (matches).
10. **Quotes at most 25 words** (lesson line 21) — word counts of the seven cells: 24, 22,
    23, 20, 9, 15, 25, 9 → all ≤ 25.
11. **M1: 682 lane-wide hits at base; 53 in round-23 section; 28 on the round's added prose**
    (lesson line 60) — `python3 .ufo/waves/round-24/evidence/prose-fused-check.py --repo . --rev
    c725aa37 --all-surfaces` → `PROSE_FUSED: FAIL hits=682`; `--section-from "Round23"` →
    `FAIL hits=53`; committed evidence `.ufo/waves/round-24/evidence/prose-ratchet-r24-added.txt`
    ends `PROSE_FUSED: FAIL hits=28`. The "502 added prose lines" figure refers to the
    uncommitted scratch file `/fast/scratch/hyaku/mori-r24-a2/r24-added.txt`; the committed
    evidence references lines up to 499 of it, so the count is not byte-verifiable but is not
    contradicted [INFERENCE].
12. **M2: register tip null → exit 2 invalid-register; measurement copy → exit 0 pre-build**
    (lesson line 61) — frozen register `c2-freeze-register.json` has `"tip": null`; `python3 -I
    tools/mori-freeze-order.py check --repo . --register .ufo/waves/round-24/frozen/c2-freeze-register.json
    --rev HEAD` → exit 2 `invalid-register`; measurement copy → exit 0 verdict `pre-build`.
    Validator at `tools/mori-freeze-order.py:183-196` (raised `InputError("invalid-register")`).
13. **M6: 9 quoted hits** (lesson line 65) — ScoutRoutedBytes.md:56-59 lists 9 lines in 6
    files.
14. **M8: BuildPressureTool.md:228** (lesson line 67) — line 228 is "The frozen cases were
    read from the other seat's clone, not edited."
15. **M9: six contradicted statements** (lesson line 68) — CriticKnowledgeOverclaim.md has
    exactly K1–K6 kills; the committed knowledge entry `corpus/knowledge/system-pressure-r24.md`
    gained a "Corrections after wave-2 falsification" section (line 8).
16. **M7: "nine or more seats"** — ScoutMisroot.md §4.1 names nine wave-1 reports.
17. **Freeze order** (SCORECARD 1516) — `git log --oneline --reverse -- tools/fixtures/mori-pressure/cases.json`
    → `f6a2970` first; `-- tools/mori-pressure.py` → first tool commit `6ee6248` after it.
18. **S093 anchor 730–731** (lesson lines 48–49) — `curl -sS <v7.2 Kconfig> | sed -n '728,733p'`
    shows "If you say Y here, the kernel will create /proc/pressure/ with the" at 730 and
    "pressure statistics files cpu, memory, and io." at 731.

## 3. Disagreements found

1. **`round-24.md:79-80`** — S01–S06 / `PASS 6/6` vs committed 7 cases / `PASS 7/7`
   (item D3, §1). The only count error in the lesson.
2. **SCORECARD.md:1504 and :1523** "Held and observed: operability 7, depth 5, freshness 5,
   adjacency 6" vs the committed Axes table `SCORECARD.md:6-15` (coverage 5, operability 6,
   depth 4, freshness 5, calibration 5, adjacency 6), unchanged since round 1 (commit
   `7ca17b1`). Command: `sed -n '6,16p' SCORECARD.md`. The same divergence predates round 24
   (`SCORECARD.md:1237`, round-19: "coverage 6, operability 7, depth 5, freshness 5,
   calibration 5, adjacency 6"), so this is a systemic stale-Axes-table pattern, not a
   round-24-specific miscount; reported as an observation.

## 4. Behavior notes (not count disagreements)

- `prose-fused-check.py --section-from` is fail-open: if the heading string is not found it
  prints `PASS hits=0` (no error). The round-23 section must be addressed as `"Round23"`
  (no space); `"Round 23"` yields a false PASS 0.
- SCORECARD round-24 section is internally consistent: target coverage 6, after "coverage 6 →
  6 pending closure", and the supplementary PASS 7/7 at line 1521 is correct.

## 5. Touched surfaces / bounds

- Written: only `.ufo/waves/round-25/w1/D3LessonCorrection.md` (this report).
- No edits to `round-24.md`, SCORECARD.md, tools, or any other lane file; no git/jj
  mutation; no `~/.omp` access; no tools installed (none needed).
- The correction paragraph is drafted in §1 for L1 (integration owner) to append; per bounds
  this seat does not apply it.
