# Mo98RevC2 — reviewer report, mori round 98 wave w1 (C2 calibration)

Scope: C2 only (SCORECARD Last-change cells), plus SHONEN.md stated counts. Detection and report only; nothing remediated.
Revisions: entering `b2a67ce562bbf2f0cc73f47d8e79f792badf5e63`, landing `600deb7ed2695f54b289cf5b6c3931e0fa9c8bb3`. Lane HEAD read-only extra check: `379a2f616c146f29341987e73b2828a0ce728ce2`.
Read-only throughout (`git -C`, `git show`, `archive`-free). Selftests run from scratch with `python3 -B -I`. No lane, fleet or sibling file written.

## 1. SCORECARD diff (entering → landing)

Command: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff b2a67ce5… 600deb7e… -- SCORECARD.md`
Result: one file, two changed lines (hunk `@@ -8,9 +8,9 @@`), lines 11 (operability) and 13 (freshness).

Check run in Python on both `git show <rev>:SCORECARD.md` blobs (4860 split-lines each):
- changed 0-based indexes `[11, 13]`; no other line differs.
- new Last-change cell == `"round 97 (improved, score held); " + old cell` for both rows: `True`, `True`.
- all non-last cells identical (Score, Evidence, axis name): `True`, `True`.

Old → new lead:
- operability: `round 93 (improved, score held); round 78 …` → `round 97 (improved, score held); round 93 …`
- freshness: `round 82 (improved, score held); round 78 …` → `round 97 (improved, score held); round 82 …`

Score cells unchanged (operability 7, freshness 5).

## 2. MANIFEST rounds[1384]

`python3 -c 'import json;print(json.load(open("/home/vgpnk/Projects/shokunin/MANIFEST.json"))["rounds"][1384])'` (list length 1386):
- round 97, date 2026-11-05, type closure, lane mori, lane_round 97, lanes {"mori":"ok"}
- admitted true, verdict "admitted"
- verdicts: operability improved, freshness improved, depth unchanged, coverage unchanged, calibration unchanged, adjacency unchanged
- verification.reviewer: "hyaku-closure (@m_zfl session, non-author)"; spotcheck `mori-shokunin/corpus/lessons/round-97-verifier-spotcheck.md@b2a67ce5…`
- The entry has no score field. "score held" is the lane's own cell convention and is not recorded in rounds[1384].

Scan of all 1386 rows for lane mori with an operability or freshness verdict: no mori row after index 1384. Round 97 is the highest admitted mori round graded improved on both axes.

## 3. Calibration tool hash

`git show <rev>:tools/mori-scorecard-calibration.py | sha256sum`:
- 600deb7e: `662fafde7ba446e13a30bc88c10a61d99f933be72902053b1e1e871fc5835113`
- b2a67ce5: `662fafde7ba446e13a30bc88c10a61d99f933be72902053b1e1e871fc5835113`
- TOOL_SHA pinned in `count-c2.py`: `662fafde7ba446e13a30bc88c10a61d99f933be72902053b1e1e871fc5835113`. Match.

## 4. Counter runs (frozen `count-c2.py`, `--work $S`)

- Landing: `C2=met mismatches=0 columns_unchanged=yes tool=ok tool_rc=0 mismatched_axes=- rev=600deb7ed269`, exit=0
- Entering: `C2=unmet mismatches=2 columns_unchanged=yes tool=ok tool_rc=1 mismatched_axes=operability,freshness rev=b2a67ce562bb`, exit=1
- HEAD (extra): `C2=met mismatches=0 columns_unchanged=yes tool=ok tool_rc=0 mismatched_axes=- rev=379a2f616c14`, exit=0

Both match the frozen receipts `evidence/before-c2.txt` and `evidence/landing-c2.txt`.

Independent cross-check of all six axes (tool expectation = highest admitted mori row with the verdict, derived from MANIFEST by me; cell = SCORECARD lead):

| axis | cell lead | MANIFEST max admitted improved/harmed | row |
|---|---|---|---|
| coverage | round 80 improved | 80 | 1163 |
| operability | round 97 improved | 97 | 1384 |
| depth | round 86 improved | 86 | 1205 |
| freshness | round 97 improved | 97 | 1384 |
| calibration | round 93 improved | 93 | 1327 |
| adjacency | round 19 improved | 19 | 398 |

All six agree. Rejected rows (r13, r17, r20, r45, r88, r94, r96) and non-admitted rows were excluded by the tool.

## 5. Is C2 a calibration move under AXES.md?

Frozen predicate: holds (section 4 reproduces it exactly).

Calibration as AXES.md defines it: "SHONEN.md/SCORECARD entries match observed repo state". The counter does not measure that:
- It compares the SCORECARD lead round and verdict word with `MANIFEST.json`, the fleet-root admitted-closure record outside the lane repo. That is an external record, not the lane repo's observed state.
- It never reads SHONEN.md, so half of the rule's named surfaces is outside the count.
- Score and Evidence cells are checked only for equality with the base revision. Their text is not checked against anything.
- The counter's `--base` default is `66c5518e…`, not the entering revision. It does not change the result for this range because the diff shows only the two Last-change cells changed.

Stale prose left by this move (not countable under the frozen contract, which forbids editing Evidence):
- Freshness Evidence cell still says "latest admitted closure grades freshness improved and states no new number (`corpus/lessons/round-28-verifier-spotcheck.md:92`)". Round 97 is now the latest admitted freshness-improved closure, so the cell contradicts its own lead.
- Operability Evidence cell has the same pattern for the round-31 closure.

So the move is real, but as calibration it is a record-agreement repair on two cells, not a measured reduction of mismatches against observed repo state. Verdict below.

## 6. SHONEN.md stated counts (report only, not fixed)

SHONEN.md is 8 lines. Counts checked against the repo:

| stated | current observation | status |
|---|---|---|
| `mori-register-check --selftest` 12/12 | `REGCHECK_SELFTEST pass=12 fail=0`, rc 0 | matches |
| `mori-settlement-scan` 10/10 | `SETSCAN_SELFTEST pass=10 fail=0`, rc 0 | matches |
| `mori-vote-bind` 16/16 | `VOTE_BIND_SELFTEST pass=16 fail=0`, rc 0 | matches |
| `mori-pin-check` 125/125 | `PIN_CHECK_SELFTEST pass=125 fail=0`, rc 0 | matches |
| `mori-drift-adjudicate` 5/5 | `PASS (5 cases)`, rc 0 | matches |
| `mori-drift-recheck` 10/10 | `PASS (10 cases)`, rc 0 | matches |
| `mori-ua-variance` 14/14 | `PASS (14 cases)`, rc 0 | matches |
| `mori-uptime-win` 8/8 | `PASS (8 cases)`, rc 0 | matches |
| `mori-workstate-win` 10/10 | `PASS (10 cases)`, rc 0 | matches |
| `mori-events-context-win` 10/10 | `PASS (10 cases)`, rc 0 | matches |
| `mori-anchor-check` 11/11 | `PASS (11 cases)`, rc 0 | matches |
| `mori-rotation-schedule` 13/13 | `PASS (13 cases)`, rc 0 | matches |
| `mori-counter-win` 12/12 | `PASS (12 cases)`, rc 0 | matches |
| `mori-record-sweep` 44/44 | `pass=44 fail=0`, rc 0 | matches |
| r84 `count-c2.py` 9/9 | `C2_COUNTER_SELFTEST pass=9 fail=0`, rc 0 | matches |
| r84 `count-c3.py` 11/11 | `C3_COUNTER_SELFTEST pass=11 fail=0`, rc 0 | matches |
| r84 `count-c1.py` 15/15 (re-run "2026-11-04 at da7631f4") | HEAD: `C1_COUNTER_SELFTEST pass=17 fail=0`, rc 0. At `da7631f4` tree: `pass=15 fail=0`, rc 0 | **stale** |

The `count-c1.py` mismatch: `git log -- .ufo/waves/round-84/count-c1.py` shows commit `25a74d4c` ("round-85: C1 arms …", 2026-11-04) after `da7631f4`. That commit added two selftest arms, so the count moved from 15 to 17. SHONEN's bullet is dated, but it is written in present tense without pointing at the current bytes. Reported, not fixed.

Line pointers:
- `SKILL.md:1178` (Round53 header) and `SKILL.md:1211` (Round54 header): resolve.
- `corpus/QUALITY.md:1479` begins QUALITY 148: resolves.
- `SKILL.md:1370` is the r84 registry row 18: resolves.
- "SKILL:905 tally pin, grep 1": current `SKILL.md:905` is the `source drift (r37)` registry row. The pin the bullet names is not on that line, and I did not locate it. Stale pointer, unverified which line now holds the pin.

Historical landing counts (dated r75–r78 receipts, not present-tense claims; current values differ because later rounds appended): SKILL.md 1327→1351/1352 (now 1460 lines), corpus/README.md 808→852 and 858→859 (now 962 lines), SCORECARD 3819 lines at `32132cfb` (now 4859), capability headings 25→26 and 26→27.

## 7. Verification gaps (named)

- UNRUN: `tools/mori-scorecard-calibration.py --selftest` (the lane's own calibration tool selftest). Not run by me.
- UNRUN: the frozen `count-c1.py` and the C1 surfaces (not in my scope).
- UNRUN: `git log` for SCORECARD across all rounds beyond the landing diff; only the entering→landing range was examined.
- Read-only git only; no fixture repo was created.

## 8. Tooling

No tools installed or updated. pacman not used. Only `python3`, `git`, `sha256sum`, `grep`, `sed`, `wc`, `ls`, `tar` used.

## 9. Verdicts

VERDICT C2 holds: frozen predicate reproduces at 600deb7e (`C2=met mismatches=0 columns_unchanged=yes`, entering `mismatches=2`), calibration tool sha matches TOOL_SHA, rounds[1384] verified.
VERDICT C2-calibration-framing needs-amend: the counter checks SCORECARD leads against MANIFEST.json (fleet record), not against observed repo state and not SHONEN.md; the freshness and operability Evidence cells still cite older "latest admitted" closures that round 97 supersedes.
