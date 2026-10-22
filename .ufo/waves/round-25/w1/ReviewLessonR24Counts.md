# ReviewLessonR24Counts — round-24 count claims vs committed bytes at `28b79d3d`

Seat: MoriR25.ReviewLessonR24Counts (reviewer, leaf, read-only). 2026-10-22.
Targets: `corpus/lessons/round-24.md` and `/home/vgpnk/Projects/shokunin/.ufo/reports/round-24/mori.md`.
Ground: lane repo bytes at `28b79d3d` ("round-24 verifier spot-check"). The lesson working copy is
byte-identical to `28b79d3d` (`git show 28b79d3d:corpus/lessons/round-24.md | cmp - corpus/lessons/round-24.md`
→ identical). The fleet report is identical to its committed form at fleet commit `c761358`
(`git show HEAD:.ufo/reports/round-24/mori.md | cmp - .ufo/reports/round-24/mori.md` → identical).
D3 (`corpus/lessons/round-24.md:79-80`, S01–S06 / `PASS 6/6` vs the 7-case tip file) is the known
defect and is excluded per assignment; `PASS 7/7` in mori.md:41 agrees with the tip bytes.

Method: every number in the assigned categories (seat counts, case counts, PASS tallies, mutant
counts, source rows) was re-derived with a read-only command over committed bytes; the two lane
selftests were re-run from working-tree files first proven byte-identical to `28b79d3d` blobs
(`git ls-tree 28b79d3d -- tools/…` vs `git hash-object tools/…`). No LSP server was involved: the
claims are markdown tallies, not code symbols; verification is command-based. No installs were made
(git/python3/bash only). No jj or mutating git command was run.

## Findings

### F1 — Low: mori.md "coverage 6" disagrees with the SCORECARD Axes table at `28b79d3d`

- Statement: "C2 (coverage 6, frontier FR12)" — `/home/vgpnk/Projects/shokunin/.ufo/reports/round-24/mori.md:13`; the round-24 contract declares the same number (`git show 28b79d3d:.ufo/waves/round-24/contract.md:51` → "## C2 — … (axis: coverage, score 6)").
- Disagreeing bytes: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 28b79d3d:SCORECARD.md | sed -n '10p'` → `| coverage | 5 | six surfaces censed by one gate; the per-surface notes are still owed … | round 1 |`.
- Diagnosis: the Axes table row is stale inside SCORECARD itself, not the report. The move log moved coverage 5 → 6 in Round 12 (`git show 28b79d3d:SCORECARD.md | sed -n '594p;611p'` → "## Round 12 — kaika campaign…", "| coverage | **improved** | 5 → 6 | claim 3; 14 lanes graded…") and held 6 through round 23 (`sed -n '1215p;1255p'` → "6 unchanged", "6 held"). The report's 6 therefore matches the move-log history and the contract; the Axes row self-declares "Last change: round 1".
- Disposition recommendation: the disagreement is real for any non-author checking `SCORECARD.md:10`; reconcile the Axes row (or add a pointer to the move log) rather than editing the report. Calibration "the lowest active score at 5" (mori.md:9) matches both sources (`SCORECARD.md:14` → `| calibration | 5 |`).

No other numeric statement besides D3 disagrees with committed bytes at `28b79d3d`. Every checked claim, its location, and the re-derivation:

## Verified claims (statement → location → re-derivation)

### corpus/lessons/round-24.md

| Statement | Location | Command (read-only) | Output |
|---|---|---|---|
| four byte-checkable items routed; item 5 not counted | round-24.md:9-12 | `git show 28b79d3d:corpus/lessons/round-23-verifier-spotcheck.md \| sed -n '60,66p'` | items 1–4 carry byte predicates; item 5 is the adjacency why-not |
| sources S090–S096 opened this round | round-24.md:15 | `git show 28b79d3d:corpus/SOURCES.md \| grep -E '^\| S09[0-6] ' \| awk -F'\|' '{print $5}'` | seven rows, all tier A |
| S097 rejected, tier C | round-24.md:27-28 | `git show 28b79d3d:corpus/SOURCES.md \| grep '^\| S097 '` | tier C, "no such page exists" reason cell |
| Gate quotes ≤ 25 words | round-24.md:32-33 | word-count of each quoted string | 23, 21, 22, 19, 8, 6, 7, 25, 9 words |
| all new rows; no older row changed | round-24.md:36 | `git diff c725aa37 28b79d3d -- corpus/SOURCES.md \| grep -c '^-[^-]'` | 0 removed lines |
| M1: 256 fused tokens; 53 in round-23 section | round-24.md:60 | `git show c725aa37:SCORECARD.md \| python3 -I <(git show 28b79d3d:.ufo/waves/round-24/evidence/prose-fused-check.py) --file /dev/stdin` | `PROSE_FUSED: FAIL hits=256`; 53 receipted in `.ufo/waves/round-24/w1/MineMistake.md:67-69` |
| M1: 502 added prose lines | round-24.md:60 | `wc -l /fast/scratch/hyaku/mori-r24-a2/r24-added.txt` | 502 |
| M1: 28 hits, all identifiers | round-24.md:60 | `git show 28b79d3d:.ufo/waves/round-24/evidence/prose-ratchet-r24-added.txt \| grep -c FUSED_TOKEN` | 28 (29th line is the summary `PROSE_FUSED: FAIL hits=28`) |
| M2: frozen register `tip: null`, check exited 2 `invalid-register` | round-24.md:62; mori.md:30 | `git show 28b79d3d:tools/mori-freeze-order.py \| python3 -I -B - check --repo <lane> --register .ufo/waves/round-24/frozen/c2-freeze-register.json --rev f6a29702e5b0…` | `{"error":"invalid-register",…}`, exit 2; register cell `"tip": null` |
| M6: 9 quoted hits of the privacy-clearance pattern at base | round-24.md:65 | `git grep -iE 'privacy_clearance\s*["'\'']?\s*[=:]\s*["'\'']?true' c725aa37 -- .ufo/waves/ \| awk -F: '{s+=$NF} END{print s}'` | 9 |
| frozen 12 cases, tool `852d1ea7` | round-24.md:70 | `git show 28b79d3d:tools/fixtures/mori-pressure/cases.json` ids | P01–P12 (12); pristine sha `852d1ea7…` in every MutPsi report |
| killed/survived lists (10 kills, 6 survivors) | round-24.md:72-74; mori.md:95 | verdict lines of the 12 `MutPsi*` reports at 28b79d3d | killed: CpuFullThreshold(P02), IrqSome(1, `FAIL 2/12` = 10 red), Regressed(P12), CpuFullDelta(P11), Ratio(P11), ErrnoMap A(P05)/B(P10), FieldSwap(5 red), EnoentZero(P04), VerdictOrder exits-2 — 10; survived: Grammar×3, Matcher, ThresholdEdge, VerdictOrder precedence — 6 |
| `MATCHER: rejected 48/48` | round-24.md:78 | `python3 -I -B tools/mori-pressure.py --selftest` (blob `5785c5b2` == `28b79d3d`) | `MORI_PRESSURE_SELFTEST: PASS 12/12` + `MATCHER: rejected 48/48 corrupted expectations`, exit 0 (4 corrupted expectations per passing case × 12) |
| routed-check probe: old held 4, fixed red/held 3 | round-24.md:84-85, 94 | probe clones under scratch; see Residual gaps | consistent with committed fix `1046aca3`, not independently re-derived |

### /home/vgpnk/Projects/shokunin/.ufo/reports/round-24/mori.md

| Statement | Location | Command (read-only) | Output |
|---|---|---|---|
| wave 1 at `06d4f4d2`, call `at` 05:14:13-03:00; wave 2 at `753d2273`, 05:56:44-03:00 | mori.md:22-24 | `git show 28b79d3d:.ufo/waves/round-24/wave{1,2}-attempts.json` | rows match exactly, `tasks_count` 33 / 36, `slot_grant … seats=33 / 36` |
| C2 cases landed at `f6a29702`, tool after at `6ee62487` | mori.md:28-29 | `git merge-base --is-ancestor f6a29702 6ee6248` | rc 0 (cases before tool) |
| C1 tool `88f96200`, hardened `1046aca3`, `575a9f3f`; three bypasses | mori.md:25, :96 | `git log --oneline 28b79d3d` | all three commits present with those subjects; lesson:94 lists the same three fixes |
| eight wave-1 scribe seats opened sources | mori.md:31 | w1 listing at 28b79d3d | exactly 8 `Src*` reports |
| knowledge entry with twelve facts | mori.md:36 | `git show 28b79d3d:corpus/knowledge/system-pressure-r24.md \| grep -oE '\bF[0-9]+\b' \| sort -u` | F1–F12 (12) |
| supplementary `PASS 7/7` | mori.md:41 | supplementary-cases.json ids at 28b79d3d | S01–S07 (7) |
| live bracket check passed 5 of 5 | mori.md:44 | `git show 28b79d3d:.ufo/waves/round-24/evidence/bracket-check-run.json` | `"runs": 5, "passed": 5` |
| M1–M9; 256; 502; 28 | mori.md:45 | Mistakes table row count + receipts above | 9 rows; receipts match |
| before: held 3 of 4, exit 1; 8 wave-1 ledger rows precede `22772c1`; `--round 24` at base held 3 (`no_round_ledger`) | mori.md:73 | `git show 28b79d3d:tools/mori-routed-check.py \| python3 -I -B - --repo <lane> --rev c725aa37… --round 23` (and `--round 24`); `git show -s --format=%cI 22772c1` | `{"held":3,"items":4,…}` exit 1 (both); commit time 2026-10-21T18:10:59Z; round-23 ledger has exactly 8 rows, row 1 `utc` 17:03:11Z < 18:10:59Z; cross-receipt `.ufo/waves/round-24/w2/RerunC1Count.md:9,18-29` |
| after: held 4 of items 4, exit 0, `"held":4`; mismatches 8 → 0 | mori.md:74 | same tool, `--rev 4f05dd5a… --round 24` | `{"held":4,"items":4,…}` exit 0 |
| before: `git cat-file -e c725aa37:tools/mori-pressure.py` exits 128 | mori.md:77 | same | `fatal: … not in 'c725aa37'`, exit 128 |
| after: `PASS 12/12`, `MATCHER: rejected 48/48` | mori.md:78 | rerun above | identical output |
| six existing W04 warnings (S035, S037, S073–S076) | mori.md:84 | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` | exactly six `W04` lines, ids S035, S037, S073, S074, S075, S076, exit 0 |
| registry 89 → 97 rows; tier A +7, tier C +1 | mori.md:86 | `git show {c725aa37,28b79d3d}:corpus/SOURCES.md \| awk` Registry-section `\| S[0-9]` counts | 89 → 97; S090–S096 tier A, S097 tier C |
| ten mutant kills and six survivors on the frozen cases; responses not counted toward the 12 | mori.md:95 | MutPsi verdicts (above) | 10 killed / 6 survived; the 12-count refers to the frozen P01–P12 |
| three bypasses; six knowledge statements | mori.md:96 | lesson:94 fix list; M9 six listed statements (round-24.md:76) | 3 and 6 |
| census selftest passes 134/134 before and after | mori.md:97 | `bash tools/mori-census.sh --selftest` (blob `c7d952d6` == `28b79d3d`) | `MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)`, exit 0, 134 `PASS` lines; receipts `.ufo/waves/round-24/w1/CensusNoHarmBaseline.md:60`, `w2/CensusNoHarmAfter.md:11,43-46` |
| wave 1: 33 seats (12 scribe, 5 executor, 5 critic, 4 scout, 4 reviewer, 2 connector, 1 mutation-tester); wave 2: 36 (16 mutation-tester, 14 reviewer, 4 critic, 2 scout); total 69 | mori.md:114-116 | role counts from `registry.members` of `.ufo/waves/round-24/wave{1,2}-run.json` at 28b79d3d | exact match, totals 33 / 36; report files 33 / 36 (`swarm-registry.json` excluded) |
| SKILL decision table + two registry rows; cites S090, S091, S095, S096 | mori.md:38-39 | `git diff c725aa37 28b79d3d -- SKILL.md`; `git show 28b79d3d:SKILL.md \| grep -oE 'S09[0-7]'` | "Round24 registry additions" section with exactly 2 rows; cite set {S090, S091, S095, S096} |
| commit table | mori.md:51-76 | `git cat-file -t <hash>` for all 24 abbreviations | all exist |
| DRIFT with 30 findings | mori.md:128 | receipt `.ufo/waves/round-24/w2/CensusNoHarmAfter.md:13` | `MORI_CENSUS: DRIFT (findings=30 …)` (host state; see gaps) |

## Residual risk and verification gaps

1. Sandbox-probe numbers (lesson:84-85 "held R2 (held 4) / held 3"; lesson:94 "old tool held 4, fixed tool red" ×3): the probes ran in scratch clones (`/fast/scratch/hyaku/mori-r24-a2/r2probe`); no committed byte re-derives them, and this reviewer seat may not create a clone. Consistent with the committed parser fix at `1046aca3`/`575a9f3f`, not independently reproduced. [INFERENCE: consistent]
2. mori.md:128 host-state numbers (30 findings; watchdog `08:31:57Z`) are receipted by `CensusNoHarmAfter.md:13` but are live host state; not re-derived now.
3. Gate digest cells (first-16-hex sha256 per source, round-24.md:34-49) were not re-fetched — outside the assigned count categories.
4. mori.md:132 "Installs: none" and M7's "/tmp" seat listing (lesson:86-88, "nine or more") were not re-enumerated; no contradicting byte found.
5. mori.md:23 `jj-lane.sh state` "ahead=0 behind=0" is round-time lane state, not re-derivable read-only at this tip.
6. The lane working tree now carries untracked round-25 files (`.ufo/waves/round-25/…`) — expected mid-wave state, unrelated to round-24 claims.

Tooling record: no installs or upgrades; used system git, python3 (with `-I -B`), bash, and the fleet's `scripts/sources-census.sh` in its committed form only.
