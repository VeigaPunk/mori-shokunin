# mori round 74 — verifier spotcheck (hyaku closure, non-author)

author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))
round: 74 · lane head `dc50c80bac27f85362bf51d42a965d75c6ae625c` · base `a9c3abb70572e5be2eb3afd941b1993b7af8d0d8` · closed 2026-11-02T09:30:14Z
method: every number below was re-derived by this closure over committed bytes (`git show`, `grep`, `awk`, `sha256sum`, `diff`) or re-executed read-only by this closure (the C2 selftest x3 and one live schedule run; the C3 live pin fetches and the standing drift re-check). Redaction rule honored: counts and shapes only.

## 1. Step-1 conformance — PASS

| Check | Command | Observed |
|---|---|---|
| Report committed by lane identity | `git -C <fleet> log --format='%an %ae %H' -1 -- .ufo/reports/round-74/mori.md` | `mori-shokunin mori@shokunin.local bccf8720024a…` |
| SHONEN heading | read of the report | `## SHONEN` with 4 boxes, all `[~]` with resolvable pointers |
| Round head is branch tip and pushed | `rev-parse refs/heads/master` + `ls-remote origin refs/heads/master` | both `dc50c80bac27f85362bf51d42a965d75c6ae625c` (ahead=0) |
| Cited commits exist and ancestral | `merge-base --is-ancestor` in the lane repo | `dc50c80b` (tip), `a9c3abb7` (its parent, the entering base), `986d4b46` (r61 data tip, `present` + ancestral rc 0) — all hold |
| Round work in `a9c3abb7..dc50c80b` | `diff-tree -r --stat` | 22 files changed, +2845/−8 — exactly the report's figures |
| Worktree == HEAD | `git hash-object` vs `ls-tree` for SKILL.md, the r74 tool, ua-variance, the S241 pin | all four byte-identical |
| Dispatch digest corroborated | grep of `.ufo/watchdog.log` | `2026-11-01T22:50:54-08:00 launch mori round=74 base=a9c3abb70572` and `2026-11-02T00:35:03-08:00 complete mori round=74 head=dc50c80bac27 pushed=True` |
| Prompt durable | `cat-file -e HEAD:.ufo/prompts/mori-round-74.md` (fleet) | committed at fleet HEAD |
| Diff shape | `diff-tree -r --numstat` | LOG 105/0, SCORECARD 52/0 (pure appends), SHONEN 4/4, SKILL 2/2, SOURCES 3/2; PROVINCE.md, AGENTS.md, corpus/QUALITY.md, corpus/README.md, the drift family and every r73 artifact absent from the changed-path list |

Marker rule: the report is a real report (work, evidence pointers, landed changes, commit citation) — not a marker. Status `ok`.

## 2. Per-claim re-check

### C1 (calibration) — the r73 routed-defect discharge — RE-MEASURED, verified

- Before/after lines: `git show a9c3abb7:SKILL.md | grep -c ""` → 1327; joined state (HEAD lines 1–1326) → 1326; HEAD → 1327 (row 11 appended).
- Split markers: `grep -c '^ 2 → ` + backtick + `UNAVAILABLE'` → before 1, after 0; joined-cell marker `'receipt) · 2 → ` + backtick + `UNAVAILABLE'` → before 0, after 1. (The report's printed patterns are backtick-mangled by markdown escaping; the receipt and this closure used the same underlying patterns — the counts match the receipt's before→after exactly.)
- Prefix/last-line identity across the join: `head -1324` sha256 before = after = `5e987926df0eb46e…`; the old last line (before :1327) content sha256 = new line at HEAD :1326 = `16974aad6779ab30…` newline-stripped (`bc46407c…` with the newline) — the committed receipt's convention is newline-stripped; both conventions verified identical.
- Joined row shape: `awk -F'|' '{print NF}'` on HEAD SKILL.md line 1325 → 10, equal to every sibling registry row checked (1316/1318/1320/1322/1324/1326/1327 all NF=10); a bad-NF sweep over the registry section prints `bad=0`.
- SKILL:905 tally pin: `sed -n '905p' SKILL.md | grep -c "PASS (6 cases)"` → 1 (unchanged).
- D73-2: `git show dc50c80b:.ufo/waves/round-73/evidence/backfill-selftests-r73.txt | grep -c "rc=0"` → 11; `grep -c "^rc=0$"` → 10; the decomposition (10 run-result lines :8–:53 + 1 embedded sample line :31 `PASS window_default_echoed  rc=0`) verified against the committed receipt `battery-count-precision-r74.txt`. No r73 artifact edited (r73 paths absent from the round diff).

Verdict: **improved** (verified; do-nothing controls receipt shows the split present and the joined cell absent at entering).

### C2 (depth) — the rotation-recurrence schedule capability — RE-EXECUTED, verified

- Before: `git cat-file -e a9c3abb7:tools/mori-rotation-schedule.py` → rc 128; no `library/time.html` row at entering (grep 0); no registry row 11 at entering.
- Selftest: this closure ran `python tools/mori-rotation-schedule.py --selftest` three consecutive times at the landing bytes (worktree hash-verified == HEAD): `MORI_ROTATION_SCHEDULE_SELFTEST: PASS (13 cases)`, rc=0, all three runs — reproduces `rotation-schedule-selftest-r74.txt`.
- Live run: this closure ran one full live schedule (`--url <S241 page> --ua mori-source-drift/1.0 --pin corpus/evidence/sources-r42/S241.html --windows 31,91,304`), read-only fetches into scratch: rc=0, `ROTATION_SCHEDULE` lines — 31s `rotated=no` (sha `5d88b3cc6039` both legs), 91s `rotated=no`, 304s `rotated=yes` (per-response=4, `5d88b3cc6039` → `b4d2a568989d`), `clock=monotonic`, wall_s=429. This reproduces the round's first live run classification exactly (31s=no, 91s=no, 304s=YES) and again differs from the r70 session (31=no, 91=YES, 304=no): the honest window-dependency finding is CONFIRMED by independent re-run and is recorded as an observation, never as a defect, in the live receipt, the report, the LOG entry and the knowledge entry. No TTL decided anywhere (S580/S581 boundary untouched); captured bodies stayed in scratch, never committed.
- One-second stamp resolution note: this closure's run computed `window_s_computed=31,91,305` for the stated 304 s window (the computed gap is read off the children's as-of stamps); the round's own run computed 304. Within the tool's documented design (QUALITY 161 computes from stamps); observation only.
- Redaction: this closure's live stdout carried counts/shapes/stamps/sha12 prefixes only — no child body content; the selftest redaction arm (planted marker token) PASSes.
- Registration at landing: registry row 11 at SKILL.md:1327 (entry/verdict-map/self-test/pins/write-scope/owner cells transcribed from the tool's usage; NF=10), prefix lines 1–1326 sha-identical per receipt `skill-registry-row11-r74.txt` (this closure re-verified the joined-state prefix identity independently in C1), :905 pin = 1.
- Standing battery: `grep -c "^rc=0$"` on `selftests-battery-r74.txt` → 11; 11 distinct `python tools/mori-*.py --selftest` command lines — one per registered instrument, matching the registry cells.
- Sourcing: S589 opened this round (rows 361 → 362, `grep -c "^| S589 "` → 1); knowledge entry `corpus/knowledge/rotation-schedule-r74.md` opens with the provenance trio (`source: S589 …`, `verified-at:`, `recheck:`).

Verdict: **improved** (verified).

### C3 (freshness) — the pin-family re-verification — RE-MEASURED, verified

- Receipt committed: `pin-family-reverify-r74.txt` with `S241: DRIFTED pin=1168b2a6… live=ddb7ba17…` (53963 bytes both) and `S581: IDENTICAL pin=5e5b941e… live=5e5b941e…` (16179 bytes).
- This closure re-fetched both pages independently (curl rc 0): live S241 sha256 `ddb7ba179052f9c3…` (53963 bytes) and live S581 sha256 `5e5b941e97c0aa6e…` (16179 bytes) — BOTH reproduce the receipt's live values exactly.
- Drift named: this closure's own `diff` of pin vs live S241 → exactly 4 changed lines = 2 asset-URL pairs (stylesheet + `scripts/ja-jp/index-docs.js`), build id `0.4.03574.8308-9505b1c8` → `0.4.03589.8339-b0a05127`; old id occurs 2x in the pin, new id 2x in the live body — the receipt's description, byte for byte.
- Adjudication re-executed: this closure ran `python tools/mori-drift-recheck.py --root . --only S241` → `S241 asset-churn as-of=2026-11-02T08:58:35Z`, `rows=1 adjudicated=1 … asset-churn=1 content-drift=0`, rc=0 — the receipt's verdict, freshly stamped.
- Teaching re-verified: line-count method (`grep -c`) pin=3 live=3; occurrence method (`grep -o | wc -l`) pin=6 live=6 — both methods agree on both bodies, matching the receipt's disclosure (lesson mistake 1's fix exercised).
- Disposition: no supersedes row owed — this closure agrees (the anchors hold on the immutable pin; the teaching holds on the live body; the drift is vendor asset churn, the class the r67 grammar separates from content drift). S241/S581 used-by cells updated in place and otherwise byte-unchanged (full-row old/new comparison run); old→new logged in the LOG entry.

Verdict: **improved** (verified).

## 3. Axis harm check

`diff-tree -r -p a9c3abb7 dc50c80b -- SCORECARD.md`: 52 added lines, 0 deleted — the axes table is untouched (no scalar moves; the report claims none and none landed). PROVINCE.md, AGENTS.md, corpus/QUALITY.md, corpus/README.md and the drift family are absent from the changed-path list (byte-identical to HEAD). No owned axis harmed.

## 4. Per-axis verdicts (this closure)

| Axis | Verdict | Basis |
|---|---|---|
| calibration | improved | C1 re-measured: the join and the D73-2 decomposition verify against committed bytes and receipts |
| depth | improved | C2 re-executed: the instrument runs (selftest x3 rc 0, live run rc 0), registered at landing, sourced S589 |
| freshness | improved | C3 re-measured: one identical re-open, one real drift caught/diffed/adjudicated by the standing grammar, teaching re-verified two ways |
| coverage | unchanged | no coverage claim; PROVINCE/README untouched |
| operability | unchanged | no operability claim; the battery re-run evidences existing capability (the capability lives under depth this round) |
| adjacency | unchanged | boundaries held (pairing tool untouched, label-sweep left operator-material, no sibling surface touched) — held, not moved |

## 5. Discernment spot-check (non-author)

The round's `## Gate` carries one new-source admit (S589) and one explicit rejection decision (no supersedes row manufactured for S241). Both sampled; both sources re-opened.

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S589 (docs.python.org/3/library/time.html) admit | admit (row written after opening; tier A scoped to the monotonic-clock grounding) | live fetch this closure (curl rc 0, 129606 bytes, same size as pin; sha differs from pin only by the page's build stamp) + pinned copy byte-check (sha `c8cc430e04d232f9…` = the row's recorded sha; :524/:525 carry the two quotes, 13 words each, ≤25; title in head :20) + `s589-anchor-check-r74.txt` (PASS items=2 rc 0; able-to-fail mislocation arm FAIL rc 1) | agree | the row teaches exactly what the page states (`time.monotonic`: "Return the value (in fractional seconds) of a monotonic clock, i.e. a clock" / "that cannot go backwards.  The clock is not affected by system clock updates."); the quotes ground the instrument's clock claim; sweep-before-fetch receipted; anchor-checker able-to-fail demonstrated |
| S241 "no supersedes row owed" (reject manufacturing a correction) | reject (of a correction) | live S241 re-fetched this closure (sha `ddb7ba17…` reproduced); own 4-line diff (2 asset-URL pairs, build-id move only); own `mori-drift-recheck.py --only S241` run → `asset-churn`, rc 0; teaching counts re-verified both methods | agree | the drift is vendor asset churn with zero content change; the pin is immutable and its anchors hold; a supersedes row would have been manufactured debt — the refusal is correctly calibrated and honestly receipted |

Census validator re-run by this closure at closure time: `mori ok`, exit 0 (the tolerated 35 W04 duplicate-URL class), matching `census-end-r74.txt`.

## 6. Trend verdicts

- **expansion: improved** — the capability acquisition demonstrably runs and is registered (registry row 11; battery 11/11; live run reproduced by this closure); one new external surface opened, sweep-then-fetch receipted, pinned, anchor-verified (S589); SOURCES 361 → 362 re-counted.
- **quality: improved** — both r73 closure-routed carry-ins discharged with re-derivable evidence (this closure re-derived both); a real freshness finding caught, diffed to 4 lines, and classified by the standing grammar (re-executed by this closure); census rc 0 at both ends (end re-run by this closure); three mistakes mined with fixes, one of them the r73 lesson's own class caught and discharged by that lesson's fix.
- **discernment: improved** — the boundary held where it was tempting (the registered pairing tool NOT edited; the label-sweep instrument left behind its open L0 line; no scalar moves; no manufactured supersedes — the last two re-opened and agreed with by this closure); the D73-2 correction landed of record without touching a frozen r73 byte; the three open mori L0 lines (round-62, round-65, round-73) confirmed present in `.ufo/l0-questions.md` and routed around, never treated as answered.

## 7. Routed defects and notes (status-neutral; none bars admission)

1. **Routed defect (land next round, append-only): the declared C2 capability acquisition has no canonical capabilities-table row.** Rounds 68–72 each landed a 4-column row (`name | what it can do | evidence pointer | first-working round`) for every declared capability acquisition (`| 68 |`, `| 69 |`, `| 70 |`, two at `| 71 |`, `| 72 |`); round 74's SCORECARD section carries the same facts inside the C2 claims-table row but no `| … | 74 |` capabilities row, while the report's trend verdict says "admitted to the repertoire table". Fix: append the canonical 4-column row for `tools/mori-rotation-schedule.py` (first-working round 74) in the round-75 SCORECARD section. Evidence complete and verified; shape only.
2. Cosmetic: the report's −8 deletion decomposition names SHONEN's four re-asserted box lines and SKILL.md's join (= 6); the remaining 2 are the SOURCES used-by row-replacements (numstat SOURCES 3/2). The headline counts (22 paths, +2845/−8) are exact; prose decomposition incomplete. Next-round report may note it; no artifact edit owed.
3. Observation: this closure's live run computed `window-s=305` against the stated 304 s window (the children's 1-second as-of stamps); the round's own run computed 304. Within the tool's documented design (the computed gap is printed beside the stated window); nothing owed, but the lane should expect ±1 s between stated and computed gaps.
4. For the operator: all four SHONEN boxes carry resolvable pointers this closure in fact resolved (registry home with the join + row 11; LOG Round 74 with receipts; the 11/11 battery; PROVINCE byte-frozen). They look fully checkable by a non-author at a promotion review.
5. The S581 teaching cell still narrates the r70 session's per-window pattern (91 s YES); it is anchored to those receipts and the r74 instability is recorded in the r74 artifacts with the used-by cell pointing at the r74 knowledge entry — no stale-unmarked defect. If the lane ever judges the cell misleading, contract rule 2 shapes the repair (a supersedes row), not an in-place edit.

## 8. Closure decision

All three claims verify (C1/C2/C3 re-measured or re-executed by this closure; supporting lane gates evidence-verified from committed receipts, plus re-execution of the read-only C2/C3 surfaces as licensed by the closure contract). No axis harmed. Report is real and conforms. **mori round 74: status ok, admitted.**
