# Mo100RevHarm — lane harm check, mori round 100 wave w1

Scope: entering `d1bd1b339b894de0249b0f60702dff9962da88d9` → landing `5e2bcf2c487e377b51287c587144bdde5b233f8f`.
`git merge-base --is-ancestor` confirms entering is an ancestor of landing. Both trees extracted with
`git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive <rev> | tar -x -C <scratch>/{before,after}`; every run
below executed the archived bytes with `TMPDIR` pointed at the scratch. Read-only git only; no writes outside this
report and the scratch (scratch removed after the runs). No tool installs were needed.

## Run table — rc and decisive line, both revisions

| # | Command (run per tree, from that tree's bytes) | entering d1bd1b3 | landing 5e2bcf2 |
|---|---|---|---|
| 1 | `python3 <tree>/tools/mori-seat-terminal.py --selftest` | rc0 `{"arms":49,"finding_id":"SELFTEST_OK","passed":49,…,"tool_sha256":"de845692…"}` | rc0 `{"arms":53,"finding_id":"SELFTEST_OK","passed":53,…,"tool_sha256":"a7ff6fb6…"}` (+4 disclosed dead_auth arms; diff shows additions only, no arm removed) |
| 2 | `python3 <tree>/tools/mori-round17-seat-regressions.py --selftest` | rc0 `SELFTEST ok:` 19 case ids | rc0 `SELFTEST ok:` same 19 ids, byte-identical list |
| 3 | r17 gate on its fixtures: `--tool <tree>/tools/mori-seat-terminal.py --fixtures <tree>/.ufo/waves/round-17/fixtures/seat --output <scratch>` | rc0 `GATE ok: 66/66 cases matched` | rc0 `GATE ok: 66/66 cases matched` |
| 4 | `bash <tree>/tools/mori-census.sh --selftest` | rc0 `MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)` | rc0 `MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)` (identical) |
| 5 | `python3 <tree>/tools/mori-sources-appendonly.py --selftest` | rc0 `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0` | rc0 `pass=22 fail=0` |
| 6 | `python3 <tree>/tools/mori-source-digest.py --selftest` | rc0 `DIGEST_SELFTEST pass=11 fail=0` | rc0 `pass=11 fail=0` |
| 7 | `python3 <tree>/tools/mori-source-digest.py <tree>/corpus/SOURCES.md <tree>/corpus/evidence` | rc1 `DIGEST_CHECK rows=133 ok=99 mismatch=0 superseded=2 prefix_only=31 unpinned=1` | rc1 `rows=135 ok=101 mismatch=0 superseded=2 prefix_only=31 unpinned=1`; S637 and S638 both `ok` — defect counts byte-equal (31 prefix_only, 1 unpinned: standing red on both sides, unchanged by the landing) |
| 8 | `python3 <tree>/tools/mori-pin-check.py --selftest` | rc0 `PIN_CHECK_SELFTEST pass=125 fail=0` | rc0 `pass=125 fail=0` |
| 9 | `python3 <tree>/tools/mori-source-drift.py --selftest` (reads SOURCES.md; offline form only) | rc0 `MORI_SOURCE_DRIFT_SELFTEST: PASS (6 cases)` | rc0 `PASS (6 cases)` |
| 10 | r99 frozen counter `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-99/count-c1.py --root <tree> --work <scratch> --seed 3` | rc0 `C1=met cases_ok=60/60 seed=3 selftest=ok live=ok(limit=122865,used_lb=7,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-` | rc0 byte-identical line — no regression on the r99 instrument |

Cross-combos (disclosed version lock, contract §C1): entering gate × landing tool → rc1 `GATE mismatch: 5/66 cases matched`; landing gate × entering tool → rc1 `GATE mismatch: 5/66`. Gate and tool updated in the same commit; matched pairs 66/66 on both trees.

## Diff scope (git diff entering..landing — 23 files, +19166/−12)

- `tools/mori-seat-terminal.py` (155 lines): only the disclosed `dead_auth` class — `CLASSES`, `AUTH_STATUSES {401,403}`, `AUTH_TOKENS` spellings, `_auth_evidence` read AFTER quota/rate evidence in both error branches, `auth_token` inside the bounded decoded projection, LIMITS wording, 4 additive selftest arms (incl. precedence arms: 403+quota-text → `dead_quota`; bare "permission denied" word at HTTP 500 → `dead_error_other`). No other behavior touched.
- `tools/mori-round17-seat-regressions.py` (3 lines): `"dead_auth"` added to `CLASSES` and to the totals key set.
- `SKILL.md` (2 registry rows): seat-terminal and r17-seat-regressions rows now name `dead_auth`.
- `corpus/SOURCES.md`: S221 `used-by` (mutable column) + S637/S638 new rows + pins; S581/S582/S583/S584/S634 gain the exact `[r100 word-count correction: …; counted by whitespace]` text — appended to the **`anchor` cell (column 6)**, see finding.
- All other changes are new round-100 wave content (contract, counters, controls, candidate copies, knowledge entry, pinned sources, probe script).

## Finding — the one new red introduced by the landing

`python3 tools/mori-sources-appendonly.py 5e2bcf2… --repo /home/vgpnk/Projects/shokunin/mori-shokunin --round-base d1bd1b3…` → **rc1**, `round_changed=[S581,S582,S583,S584,S634]`, `stale_supersede=[S581,S582,S583,S584]`. The same gate at the entering endpoint reads `round_changed=[]`, `stale_supersede=[]` (the plain-mode `appendonly_violations=50` ids are pre-existing history and unchanged). Cell-level diff of the five rows shows exactly one cell changed each: the immutable `anchor` column. CORPUS rule 2 permits in-place change only in `status`/`recheck`/`used-by`, and SKILL.md:887-890 requires landing a SOURCES.md change only with `round_changed=[]`. `stale_supersede` follows mechanically: the pairs S581→S586, S582→S583, S583→S587, S584→S585 now postdate their targets' last immutable-cell edit. Control: S221's change sits in `used-by` and is correctly not flagged. The frozen P2 predicate (mismatch/spurious/altered/census) has no append-only conjunct, so the C2 counter can still read met — this is an amendment-class defect in the landing's edit placement (corrections should land as superseding rows or in a mutable column), not a counter falsification.

## Axes (SCORECARD.md `## Axes`)

coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6. Measured across both trees: no registered self-test regressed or lost an arm; census tally byte-identical (134/134); r99 frozen counter byte-identical; source-digest defect counts unchanged; the seat-terminal change is class-additive and by its precedence arms only reclasses `dead_error_other` → `dead_auth`. No axis shows a measured harm from these runs. The single new red is the corpus append-only discipline breach above — route to the integrator as an amendment item; it is not a measured axis regression.

## Unrun / skipped

- `mori-source-drift.py` live mode (network fetch) and `mori-pin-check.py` full `--rev` re-pin sweep (long; not in my enumerated set): skipped — their offline `--selftest` forms are green on both trees (rows 8–9).
- `sources-census.sh validate --file`, round-100 `count-c1.py` / `count-c2.py` at both revs: not this seat's enumeration (measurement seats); unrun here.

VERDICT no-harm needs-amend: every measured instrument is green and equal across both revisions (no axis regresses), but the C2 corrections append to the immutable anchor cell of S581–S584/S634, newly tripping `mori-sources-appendonly.py --round-base` (round_changed 0→5 ids, stale_supersede 0→4) against SKILL.md:887-890 / CORPUS rule 2 — amend by superseding rows or by carrying the correction in a mutable column.
