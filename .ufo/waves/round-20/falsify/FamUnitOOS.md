# FamUnitOOS — C1 falsification of `+FINDING:UNIT_FAILURE_OUT_OF_SCOPE` (round 20)

## Verdict: HOLDS — AGREE with class `live-state` (register row 42-47 of `corpus/evidence/drift-classification-r20.json`)

The register row's cause claim is correct and every evidence pointer resolves. The token
is in the drift because the current boot's user journal carries 270 non-fleet
unit-failure records while the r10 pin-time boot carried 0; the census-logic change
between r10 and the entering tip is outcome-neutral on this boot, so the delta vs the
baseline is host state, not census behavior.

## Per-pointer verification

| # | Register evidence pointer | Status | What I checked |
|---|---|---|---|
| 1 | `tools/mori-census.sh:1491-1493` | HOLDS | :1491 `if [ "$nonfleetn" -gt 0 ]` → :1492 user-scope branch → :1493 `emit_finding UNIT_FAILURE_OUT_OF_SCOPE info "class=unit_failure_record count=$nonfleetn subject=nonfleet owner=tsukuroi … scope=user …"`. Exact gate+emit for this token. Working-tree census sha256 = `87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28` = the contract's `87b8d680…ab28` and the entering receipt's `census_sha256`, so these line numbers are the measured-commit bytes. |
| 2 | `5be8943 census :766-767` | HOLDS | `git show 5be8943:tools/mori-census.sh` blob sha256 = `d7710981aa1c7571…4a0b20` = the baseline header's `census_sha256` (baseline :2); 5be8943 is the round-10 pin commit itself ("round-10 evidence: drift pin (census d7710981 …)"). :766 = `c_unit=$(… grep -ciE 'Failed with result\|Unit entered failed state')`, :767 = fleet-marker subset `grep -ciE 'shokunin\|ufo-sighting\|tmux-spawn\|the-tick\|fleet'`; gate+emit at :783-784 (`c_unit > c_unit_fleet` → `UNIT_FAILURE_OUT_OF_SCOPE count=$((c_unit - c_unit_fleet))`). |
| 3 | `8d22d18` | HOLDS | `git log -S UNIT_FAILURE_OUT_OF_SCOPE -- tools/mori-census.sh` → exactly `8d22d18` (r14, 2026-10-20 03:40:12 -0300), `18d7d55` (r13), `486a4e3` (r1). 8d22d18's diff ADDS both `UNIT_FAILURE_OUT_OF_SCOPE` and `_SYSTEM` emissions plus selftest assertions (`git show 8d22d18 \| grep -c '^- …OUT_OF_SCOPE'` over the census = 0 added-by-r14 confirmed; `18d7d55` diff removes exactly 1 such line). "r14-restored structured predicate" is accurate. |
| 4 | `corpus/evidence/drift-r12-20261019T2204Z-classification.md:29,31` | HOLDS | :29 = this token's r12 row ("found 3 non-fleet unit failures … Regression? No") — same class reasoning, prior boot (2026-10-19 08:11:44), count 3. :31 = `-FINDING:KILL_SIGNAL_JOURNAL` row with `uptime -s → 2026-10-19 08:11:44` — the boot-scoping precedent the `future_flip: "boot-scoped; next reboot can clear it"` rests on. |
| 5 | seat `.ufo/waves/round-20/build/TokUnitOOS.md` | EXISTS | Used as lead only; all conclusions below re-derived independently. |

## Re-derived cause evidence (count-only host reads; census NOT run)

Same boot as the entering measurement: `uptime -s` → `2026-10-20 09:57:08`.

- r10 text predicate on today's journal: `journalctl --user -b --no-pager -q | grep -ciE 'Failed with result|Unit entered failed state'` → **270**; exact r10 fleet-marker subset grep → **0**; system scope → **0**. Gate `270 > 0` true → the baseline's own logic would emit `UNIT_FAILURE_OUT_OF_SCOPE count=270` today.
- Current structured predicate (faithful replica of `JOURNAL_JQ_UNITS` at census :1122-1136, `--arg fleet "$FLEET_UNIT_TOKENS"`, over `journalctl --user -b -o json --output-fields=_BOOT_ID,MESSAGE_ID,UNIT,USER_UNIT,UNIT_RESULT MESSAGE_ID=d9b373ed55a64feb8242e02dbe79a49c`; id verified at census :1078): **total 270, fleet 0, nonfleet 270, missing 0, ambiguous 0, malformed 0**; all 270 records carry `_BOOT_ID 3e7084f470464957a8a2c00542a3b469` = current boot id (dashes stripped, per census :342-349). System scope: **0** records → no `_SYSTEM` token, matching the entering receipt (only the user-scope token is in the 50-token list).
- Both predicates therefore yield 270 non-fleet / 0 fleet / 0 unknown on the identical record set — the register reason's central numeric claim reproduces exactly.

## Class adjudication

- **AGREE `live-state`.** The emission gates are count-gated (`nonfleetn > 0` now; `c_unit > c_unit_fleet` at pin) and the pin-time output shows the finding absent.
- **"id existed at r10" — TRUE.** Introduced 486a4e3 (r1), present at the pin commit 5be8943 (:783-784). Not a new-finding-id artifact.
- **"the r10 boot had none" — TRUE.** `grep -c UNIT_FAILURE baseline-r10-20261015T2231Z.json` → 0; the baseline FINDING block (:24-38, WATCHDOG_STALE/ABSENT, 11× WAVE_UNSETTLED_AGE, KILL_SIGNAL_JOURNAL, SEGFAULT_JOURNAL) contains neither `UNIT_FAILURE_JOURNAL` (would require fleet>0) nor `UNIT_FAILURE_OUT_OF_SCOPE` (requires c_unit>fleet) → both counts were 0 at pin. Note `unit_failure=<V>` on baseline :10 is masked, so absence-of-finding is the only readable proof — and it is sufficient.
- **`census-schema-change` — correctly rejected.** The r13 removal / r14 restoration is real (verified), but the drift pair is baseline-r10 vs entering-tip census, and the entering census's structured predicate is outcome-identical to the r10 text predicate on this boot (270/0/0 both). Schema change would require divergent outcomes; there are none. The r13 interlude could only cause a false-clean absence of this token (the M6 blind-spot family), which is not this token's delta.
- **`roster-change` — correctly rejected.** r10 inline marker set at 5be8943:767 (`shokunin|ufo-sighting|tmux-spawn|the-tick|fleet`) is byte-identical to today's `FLEET_UNIT_TOKENS` at census :1121; no roster input feeds the gate.
- **`census-regression` — correctly rejected.** Emission is an intentional, selftest-covered r14 restoration (8d22d18 adds `bad 'journal: fleet failure also routed non-fleet'` and regex assertions); outcome on this state matches r10 logic. Nothing misreports.

## Residual risk / verification gaps

1. The 270 equivalence of text-lines vs structured-records is measured on this boot only (register's own `future_flip` concedes boot scoping). Generalization to future boots is untested — a boot where the text grep and subject triage diverge would reclassify. [INFERENCE-free: scoped claim, correctly worded in the register]
2. The census's own 07:18Z count value for this finding is not recorded anywhere machine-readable (drift receipt lists tokens only); I verified 270 at a later time on the same boot and the census's token presence at 07:18 via the receipt. The seat marks the 07:18 value [INFERENCE]; same caveat here.
3. My structured replication is a re-derivation of the census jq source, not the census binary run (census run out of scope for this seat). Fidelity grounded in reading `JOURNAL_JQ_UNITS` (:1122-1136), `FLEET_UNIT_TOKENS` (:1121), the id (:1078) and boot check (:342-349); the census selftest also asserts this routing.
4. The r12 receipt's "count 3" on the prior boot is taken from the committed receipt (:29), not independently re-measurable (that boot is gone). Consistent with, and only supporting, the boot-scoped live-state story.

## Disclosures

No tool installs or updates. No census run. Host reads: `uptime -s`, `journalctl` count-only queries (no message text read or stored), `tr` of `boot_id`. Git: read-only `log -S`/`show`. Scratch: `/tmp/FamUnitOOS-units.jq` only. No interactive-session, worktree, `.jj/` or `~/.omp` content searched, matched, or opened. Lane production files untouched.
