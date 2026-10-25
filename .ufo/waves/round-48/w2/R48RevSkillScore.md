# R48RevSkillScore — w2 falsify of the Round-48 self-assessment surface

Attacked: SKILL.md's Round-48 section (v3 prose, rows 971–973 and decision row 979) plus the
re-pinned r14 cell at SKILL.md:168; SCORECARD.md's Round-48 section (2585–2611) and the Axes
table (8–15); LOG.md's Round-48 entry (2700–2722) and the round-47 erratum (2689–2698).
Verdict: **HOLDS**, with three discrepancies and two limits below — none inside a claim
predicate. Seat class: reviewer (leaf, no probes dispatched). All runs used
`TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48RevSkillScore`; no
repo files were edited.

## Re-run results (every pinned selftest tally and both claims)

| pin | stated | observed | rc |
|---|---|---|---|
| `tools/mori-pin-check.py --selftest` (SKILL.md:938) | `PIN_CHECK_SELFTEST pass=60 fail=0` | `PIN_CHECK_SELFTEST pass=60 fail=0` | 0 |
| `.ufo/waves/round-48/count-c1.py --selftest` (SKILL.md:971) | `C1_SELFTEST pass=34 fail=0` | `C1_SELFTEST pass=34 fail=0` | 0 |
| `.ufo/waves/round-48/count-c2.py --selftest` (SKILL.md:972) | `C2_SELFTEST pass=22 fail=0` | `C2_SELFTEST pass=22 fail=0` | 0 |
| `tools/mori-unlanded-check.py --selftest` (SKILL.md:973) | `UNLANDED_SELFTEST pass=13 fail=0` | `UNLANDED_SELFTEST pass=13 fail=0` | 0 |
| C1 at `e4dfff32`: `count-c1.py --tool tools/mori-pin-check.py --rev e4dfff32d4f97c7ef250e9a7538fa75d4f284492 --jobs 13` | `C1=met` | `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12 rev=e4dfff32…` — J1–J8 `unmet` rc 1, H1–H4 and `real` `met` rc 0 | 0 |
| C2 at `e4dfff32`: `count-c2.py e4dfff32d4f97c7ef250e9a7538fa75d4f284492` | `C2=met` | `C2=met claims=15 located=15 quote_missing=0 bad_rows=0 sources=4 source_rows=ok pins=ok provenance=ok rev=e4dfff32…` | 0 |

C1 wall time was **493 s at --jobs 13** (each variant re-measures the whole registry; a
serial run exceeds 300 s). Relevant below.

Frozen-instrument integrity: working-tree sha256 of `count-c1.py`, `count-c2.py`,
`contract.md`, `v3-spec.md` and all three `controls/*.py` equal `evidence/freeze-sha256.txt`
bytes, and that receipt is byte-identical to `git show 4387cf94:…/freeze-sha256.txt`.
`tools/mori-pin-check.py` correctly differs (`85a89a3b…` vs the pinned v2 `9832e38c…` — v3
is the landed change, and the tool bytes at `e4dfff32` equal the working tree).

## Discrepancies found

1. **SCORECARD.md:2594–2595 — "After" values were never appended.** Both claim rows promise
   "measured at the landed tip, appended below" and the file ends at line 2611 with nothing
   appended. Worse, `evidence/after-c1-at-e4dfff32.txt` is a **0-byte file** (untracked,
   mtime 19:37 — presumably a truncated capture, and the serial run's ~500 s duration makes
   a mid-write kill plausible). `after-c2-at-e4dfff32.txt` holds the C2 receipt. The claim
   itself re-proves green above, so this is a missing-receipt/documentation defect, not a
   predicate defect — but at the committed tip the only C1 `met` receipt in evidence/ is
   empty. Class: landing/reporting, exactly the routed class M1.

2. **contract.md:95–96 — census line count is off by one.** The contract records the start
   census as "20 lines of output with 19 W04 warnings plus one `ok`". The receipt
   `evidence/census-start.txt` has 21 lines: **20** `W04` rows + 1 `ok`. Frozen text
   undercounts the receipt. Not a claim predicate (census is a "not claims" item); worth an
   erratum, not a re-score.

3. **`freeze-sha256.txt` covers only four of six committed copies.** The freeze pins the
   four `COPIES` URLs plus controls; the landing commit added
   `corpus/evidence/sources-r48/arch-mips-errno.h` and `arch-sparc-errno.h` (S483/S484,
   `git log --diff-filter=A` → `e4dfff32`, after freeze `4387cf94`). These files carry no
   frozen digest anywhere and are not in `count-c2.py`'s pin set, so contract P-C2's
   "every committed copy matches its frozen sha256" is unenforceable for them. No predicate
   impact (the claims table never cites them, and `sources=4` is consistent: it counts
   claim-table rows per contract, not `source:` headers) — but the freeze coverage has a
   gap a later mutation could hide in.

## Verified true (line-by-line)

- **SKILL.md:168 repair** — `tools/mori-round14-regressions.py` sha256 is
  `533218a566030fdabf7ca6a1c78111ca10be3fb3cb0e4a7b22734959f847e4ef` (prefix `533218a5` as
  pinned); `git show 5601d12:tools/mori-round14-regressions.py` is `c39e5a73…` and the old
  prefix matches no working-tree file — LOG.md:2710–2711's narrative holds.
- **SKILL.md:938 self-test cell** — `PIN_CHECK_SELFTEST pass=60 fail=0` reproduces (60 PASS
  lines incl. r1–r10 v3 arms); the round-47 floor in pinned values matches contract
  `--min-tally-pins 26 --baseline-rev 2d85e33d…`.
- **SKILL.md:941–979 Round48 section** — v3 rule summary matches selftest arm names
  (r9a/b/c hidden tallies, r10 decoy digests, r5 line-count, r6 truncated digest); the
  stated D7 survivor matches `corpus/lessons/round-48.md` M3's "Not closed" clause; row 979's
  `(S479–S484)` citation resolves to six `mined` rows opened 2026-10-25.
- **SCORECARD before-values vs receipts** — C1 row (2594): `control-c1-tool-v2-entering.txt`
  prints `C1=unmet junk_met=8 … variants=12` rc 1; `control-c1-stub-always-met.txt`
  `junk_met=8`; `control-c1-stub-always-unmet.txt` `honest_unmet=4 real=unmet`. C2 row (2595):
  `control-c2-donothing.txt` prints `C2=unmet claims=0 … failed=entry_absent,pins` rc 1.
  The 2598 "22 `C2_SELFTEST` arms" matches `selftest-c2.txt` (`pass=22 fail=0`) and the
  re-run.
- **Axes table (SCORECARD.md:10–15)** — `git show e5dbac05:SCORECARD.md` lines 8–16 are
  byte-identical to HEAD (`sha256 22cc016d…` both ways); `git diff e5dbac05 e4dfff32` shows
  only 30 added lines, all inside the new round-48 section. Coverage 6 / operability 7 /
  depth 5 / freshness 5 / calibration 5 / adjacency 6 — entering scores unchanged, no axis
  harmed.
- **LOG.md:2700–2722** — pure append (`git diff`: 35 additions, 0 deletions); `C1=unmet
  junk_met=8` and `C2=unmet … entry_absent,pins` match receipts; "15 claim rows" matches
  the entry table (S479×7, S480×4, S481×1, S482×3); "Rows S479–S484" all six exist and are
  `mined`; "eight junk and four honest edits" matches counter `variants=12` and selftest
  arm `eight_junk_four_honest`; "49 seats, 39 reports" matches `w1-results.json` (49
  results) and `ls w1/*.md | wc -l` = 39; mistakes M1–M7 all present in
  `corpus/lessons/round-48.md:111–117`; "QUALITY 127" resolves at corpus/QUALITY.md:1070.
- **LOG erratum (2689–2698)** — commit `356fb94a` exists and adds exactly
  `w2-results.json`, `CritV2Junk.md`, `MutV2Rebound.md`, `ScoutMisroot.md` plus a
  round-47 lesson note; S478's browser-User-Agent note is in `corpus/lessons/round-48.md:31–36`.
- **Round-47 capability row (SCORECARD.md:2583)** — its `pass=34` pin is not stale: the
  frozen v2 control `controls/tool-v2-entering.py --selftest` prints
  `PIN_CHECK_SELFTEST pass=34 fail=0`, rc 0. The cell pins the v2 instrument it describes.

## Limits / residual risk

- The two boundary copies (S483/S484) are unpinned — finding 3; a future claim row quoting
  them would be scored on un-frozen bytes.
- The serial `count-c1` run needs >300 s; any harness with a 5-min seat timeout captures a
  truncated receipt (the likely origin of the 0-byte `after-c1` file).
- `pin-check` selftest runtime ~6 s; all runs observed evidence only. Where a claim rests
  on a receipt I did not regenerate (e.g., `w1` seat narratives), the artifact was
  cross-checked by content, not re-execution.

Checks main should run if wanted: fill `after-c1-at-e4dfff32.txt` with the run above
(verbatim `C1=met …` block, rc 0), append the two After cells in SCORECARD.md:2594–2595,
and erratum contract.md:95–96's census count to 21 lines / 20 W04.
Report: .ufo/waves/round-48/w2/R48RevSkillScore.md
