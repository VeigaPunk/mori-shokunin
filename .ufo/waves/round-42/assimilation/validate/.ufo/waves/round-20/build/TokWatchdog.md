STATUS: complete

# C1 token classification: watchdog tokens (MoriR20.TokWatchdog)

Scope: `-FINDING:WATCHDOG_STALE`, `+FINDING:WATCHDOG_STATE_LAG`, and `round`. The bare `round` in the assignment is the lane-line `round=` key, one of the 8 unclassified tokens in `.ufo/waves/round-20/evidence/c1-drift-entering.json` (lines 65-74). I classified only these three. The other 47 tokens are not covered here.

Measured commit 2061780117e6 (entering tip). Census sha256 at the measured commit and at HEAD: `87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28`, verified with `git show <rev>:tools/mori-census.sh | sha256sum`. The r10 pin commit 5be8943 has `d7710981...`, which matches baseline header line 2.

Method: static reading of census emission sites; `git diff -U0 5be8943 HEAD` hunk ranges; `git log -S/-G`; read-only live state (`.ufo/watchdog.log`, `.ufo/state/*.round`, `pgrep`, fleet `scripts/`, fleet `git log`); the r10 baseline; the round-13 register; the round-20 scratch pin. The census was NOT executed. No git or jj mutation, no installs.

## 1. Classification (JSON-ready table: token | class | reason | evidence)

| token | class | reason | evidence |
|---|---|---|---|
| -FINDING:WATCHDOG_STALE | live-state | STALE rule unchanged since r10. The r10 pin saw no daemon and a log idle since 2026-10-15T01:58:27-03 (over 900 s). The entering run saw ledger writes at 07:18:05-03 (age under 900 s), because hyaku-inline now appends to the same ledger. WATCHDOG_ABSENT is present in both r10 and now, so the roll stays DRIFT. | tools/mori-census.sh:733-737, :351 (unchanged; no hunk at new lines 351 or 597-933); baseline-r10 :24, :25; .ufo/watchdog.log:402, :582-585; stat mtime 1792578201 = 2026-10-21 07:23:21 -03; pgrep rc 1 at 2026-10-21T10:30:06Z; scratch c1-pin-probe-scratch.json:52 (ABSENT present, no STALE in :1-68); emit introduced 7ca17b1 (round-1) |
| +FINDING:WATCHDOG_STATE_LAG | live-state | Rule and code unchanged since r7 (d30b4e4). At r10 all 21 `.ufo/state/<lane>.round` values equalled the ledger's last launch round. Now 13 of 21 lag. The daemon, the only writer of `.round` files, has not ticked since 2026-10-15T01:58:27-03, while hyaku-inline appends launches without writing `.round`. INFO by design: SKILL.md:15, :39; SCORECARD.md:359-360. | tools/mori-census.sh:816-818, :762-827, :677-694 (unchanged since r10); baseline-r10 :1-39 (no STATE_LAG line); state mtimes 2026-10-15 01:45:42 / 01:50:57; 13-lane table in section 3; scratch :39-51; scripts/shokunin-watchdog.sh:193, :220-221, :406; scripts/hyaku/inline.sh:24, :103, :130, :136; introduced d30b4e4 (round-7) |
| round | live-state | Lane-line shape unchanged since r3-r4. A second `round=` key appears only in closed-anchor rows (row-4 `reason=ledger-close`, row-6 `reason=committed-report`). drift_scan concatenates duplicate keys (r10 code), so the `round` field of any closed paired lane changes, although the numbers are masked. Live closures absent at r10: kumitate row-4 (complete round 38 at 05:10:38 -03), and kengaku, kake, kagi row-6 (fleet reports committed after launch). Not a schema change. | tools/mori-census.sh:2545, :2363-2364, :2375, :2409-2411, :2823-2824, :2839-2840 (duplicate-key code introduced 5be8943); row shapes introduced 1439c47 (r3) and 5b62c89 (r4); scratch :16, :18-20, :22, :25, :31; .ufo/watchdog.log:561, :579; fleet git: .ufo/reports/round-26/kengaku.md 05:54:27 -03, round-23/kake.md 06:01:39, round-24/kagi.md 07:07:09; rule corpus/knowledge/lane-silence-r2.md:87 |

```json
[
  {"token": "-FINDING:WATCHDOG_STALE", "class": "live-state", "reason": "STALE rule unchanged since r10. The r10 pin saw no daemon and a log idle since 2026-10-15T01:58:27-03 (over 900 s). The entering run saw ledger writes at 07:18:05-03 (age under 900 s), because hyaku-inline now appends to the same ledger. WATCHDOG_ABSENT is present in both r10 and now, so the roll stays DRIFT.", "evidence": "tools/mori-census.sh:733-737,:351 (unchanged; no hunk at new lines 351 or 597-933); corpus/evidence/baseline-r10-20261015T2231Z.json:24,:25; .ufo/watchdog.log:402,:582-585; stat mtime 1792578201 = 2026-10-21 07:23:21 -03; pgrep rc 1 at 2026-10-21T10:30:06Z; .ufo/waves/round-20/evidence/c1-pin-probe-scratch.json:52; emit introduced 7ca17b1 (round-1)"},
  {"token": "+FINDING:WATCHDOG_STATE_LAG", "class": "live-state", "reason": "Rule and code unchanged since r7 (d30b4e4). At r10 all 21 .ufo/state/<lane>.round values equalled the ledger's last launch round. Now 13 of 21 lag: the daemon, the only writer of .round files, has not ticked since 2026-10-15T01:58:27-03, while hyaku-inline appends launches without writing .round. INFO by design.", "evidence": "tools/mori-census.sh:816-818,:762-827,:677-694 (unchanged since r10); corpus/evidence/baseline-r10-20261015T2231Z.json:1-39 (no STATE_LAG line); .ufo/state mtimes 2026-10-15 01:45:42 / 01:50:57; scripts/shokunin-watchdog.sh:193,:220-221,:406; scripts/hyaku/inline.sh:24,:103,:130,:136; SKILL.md:15,:39; SCORECARD.md:359-360; introduced d30b4e4 (round-7)"},
  {"token": "round", "class": "live-state", "reason": "Lane-line shape unchanged since r3-r4. A second round= key appears only in closed-anchor rows (row-4 reason=ledger-close, row-6 reason=committed-report). drift_scan concatenates duplicate keys (r10 code), so the round field of any closed paired lane changes although the numbers are masked. Live closures absent at r10: kumitate row-4 (complete round 38 at 05:10:38 -03); kengaku, kake, kagi row-6 (fleet reports committed after launch). Not a schema change.", "evidence": "tools/mori-census.sh:2545,:2363-2364,:2375,:2409-2411,:2823-2824,:2839-2840 (duplicate-key code introduced 5be8943); row shapes introduced 1439c47 (r3) and 5b62c89 (r4); scratch c1-pin-probe-scratch.json:16,:18-20,:22,:25,:31; .ufo/watchdog.log:561,:579; fleet .ufo/reports/round-26/kengaku.md ct 05:54:27 -03, round-23/kake.md ct 06:01:39 -03, round-24/kagi.md ct 07:07:09 -03; corpus/knowledge/lane-silence-r2.md:87"}
]
```

## 2. Per-token evidence

### 2.1 -FINDING:WATCHDOG_STALE, class live-state

- Emission now: `tools/mori-census.sh:733` (`age=$((NOW_EPOCH - mtime))`), `:734` (`age > WATCHDOG_STALE_S`), `:736` (`emit_finding WATCHDOG_STALE warn ...`). Default threshold `:351` (`${MORI_WATCHDOG_STALE_S:-900}`). `NOW_EPOCH` is `:382-383`.
- Baseline: `corpus/evidence/baseline-r10-20261015T2231Z.json:24` has `FINDING WATCHDOG_STALE severity=warn ... threshold_s=900`. Line 8 has `log=ok; ... stale_threshold_s=900`. Line 25 has `FINDING WATCHDOG_ABSENT`.
- Introduced: `git log -S'emit_finding WATCHDOG_STALE warn'` and `-S'WATCHDOG_STALE_S=${MORI_WATCHDOG_STALE_S:-900}'` both give 7ca17b1 (round-1). `5be8943` (r10) only adds test and mutant text.
- Census logic since pin: `git diff -U0 5be8943 HEAD -- tools/mori-census.sh` has no hunk at new lines 351, 382-383, or 597-933. That range covers `load_ledger` (:665), `ledger_last_launch_round` (:677), `epoch_mtime` (:698), and `probe_watchdog` (:704-854). A `-G` search for the emit, threshold, and age identifiers finds no commit after 5be8943.
- Live (read-only): `.ufo/watchdog.log` mtime 1792578201 = 2026-10-21 07:23:21 -03, 585 lines. Last daemon `tick=` is line 402, `2026-10-15T01:58:27-03:00`. Lines 582-585 are `driver=hyaku-inline` launches (06:47:50, 07:17:03, 07:18:05, 07:23:21). The receipt places the entering run after the 07:18:05 write and records a 103.98 s wall time. No ledger line was written between 07:18:05 and 07:23:21, so the mtime age stayed below 900 s throughout the entering run [INFERENCE on the exact start second; the observed entering token set has no STALE].
- The scratch pin at `2026-10-21T10:22:12Z` has no STALE line (lines 1-68), and does have `FINDING WATCHDOG_ABSENT` at line 52.
- Daemon: `pgrep -af shokunin-watchdog` returned rc 1 at 2026-10-21T10:30:06Z. ABSENT is unchanged and is not in the token list.
- Mechanism: `scripts/hyaku/inline.sh:24` sources `scripts/shokunin-watchdog.sh`, which inherits its `log()` (`shokunin-watchdog.sh:66`, appends `$UFO/watchdog.log`). `inline.sh` emits `launch`, `complete` and `lane-dead-no-report` at `:103`, `:130` and `:136`.
- Caveat: the freshness probe is a log-mtime proxy. It now measures ledger activity, not daemon liveness. ABSENT is the only daemon-liveness signal.

### 2.2 +FINDING:WATCHDOG_STATE_LAG, class live-state

- Emission now: `tools/mori-census.sh:816` (`v < lr`), `:818` (`emit_finding WATCHDOG_STATE_LAG info "lane=... state_round=... ledger_round=... path=..."`). The state walk is `:762-827`. `ledger_last_launch_round` (`:677-694`) takes the last `launch <lane> round=N` line in file order.
- Introduced: `git log -S'WATCHDOG_STATE_LAG'` gives d30b4e4 (round-7) only. The ledger reader came from 1439c47 (r3). Neither changed after 5be8943.
- Baseline: the full 39-line canonical block (lines 1-39) has no STATE_LAG line. At pin time every state file equalled the ledger. State mtimes are 2026-10-15 01:45:42 and 01:50:57, which match the ledger launch lines 336-400.
- Cause, observed:
  - The daemon is the only file under `scripts/` that references `.round` (`grep -rln '\.round' scripts/`). It writes `echo "$n" > .ufo/state/<lane>.round` in `launch_lane` (`scripts/shokunin-watchdog.sh:193`, write at `:220`), then logs the launch at `:221`. Its last tick is ledger line 402 (`2026-10-15T01:58:27-03:00`).
  - From `2026-10-19T23:10:53-03:00` (ledger line 403) the ledger receives hyaku launches: `driver=hyaku slot=1`, then `driver=hyaku-inline` (for example line 419, kama round 12, and line 585, kagi round 25).
  - The operator directive to run in-session is ledger line 406 (`hyaku: headless attempt ended by operator directive to run in-session`).
  - `scripts/hyaku/` never writes `.round`. Its state lives under `$HOME/.local/state/shokunin-hyaku` (`inline.sh:19`).
- Corroboration: the scratch pin lines 39-51 list exactly the 13 lanes in the table below.
- Intent: `SKILL.md:15` (`WATCHDOG_STATE_LAG`/`_AHEAD` are info, "visibility, not severity"). `SKILL.md:39` ("a state file can disagree without the fleet being unhealthy"). `SCORECARD.md:359-360` (round-7 gap closure). Census header `:86-95` (INFO; "neither may flip the roll"). Note that `corpus/knowledge/lane-silence-r2.md:64` says the state advances "only when the driver accepts the report", while the daemon writes it at launch (`:220`). That is a documentation mismatch with no behavior effect.

State versus ledger at the entering time, 2026-10-21 07:18 -03:

| lane | state (.round) | last ledger launch (line, time) | status |
|---|---|---|---|
| aggregator | 10 | round 10 (390, 10-15 01:50:57) | equal |
| audio | 1 | round 1 (337, 10-15 01:45:42) | equal |
| chousa | 1 | round 25 (553, 10-21 02:47:23) | LAG |
| game-dev-2d | 1 | round 1 (336, 10-15 01:45:42) | equal |
| game-dev-3d | 1 | round 1 (353, 10-15 01:45:42) | equal |
| kagi | 16 | round 24 (543, 10-21 02:43:10) | LAG |
| kaidoku | 1 | round 21 (578, 10-21 05:05:02) | LAG |
| kake | 16 | round 23 (558, 10-21 03:26:44) | LAG |
| kama | 1 | round 21 (583, 10-21 07:17:03) | LAG |
| kasegi | 17 | round 23 (519, 10-20 18:30:58) | LAG |
| kengaku | 13 | round 26 (541, 10-21 02:22:27) | LAG |
| kotoba | 16 | round 16 (376, 10-15 01:50:57) | equal |
| kumitate | 18 | round 38 (561, 10-21 04:04:24) | LAG |
| lore | 1 | round 1 (370, 10-15 01:50:57) | equal |
| mado | 1 | round 21 (574, 10-21 04:49:56) | LAG |
| mori | 2 | round 20 (584, 10-21 07:18:05) | LAG |
| protocol | 14 | round 14 (394, 10-15 01:50:57) | equal |
| revenger | 1 | round 1 (386, 10-15 01:50:57) | equal |
| souji | no .round file | round 20 (581) | not compared |
| tabi | 1 | round 20 (582, 10-21 06:47:50) | LAG |
| tameshi | 1 | round 20 (567, 10-21 04:33:16) | LAG |
| tsukuroi | 1 | round 20 (580, 10-21 05:13:11) | LAG |

Totals: 13 LAG, 8 equal, 21 state files, 1 lane with no state file. No AHEAD.

### 2.3 round, class live-state

- Emission now: `tools/mori-census.sh:2545` `SURFACE lane.$lane: $GL_STATE (lane=$lane round=${GL_ROUND} launch_epoch=... age_s=${GL_AGE} basis=${GL_BASIS} ${GL_EXTRA}; ts=...)`. The same text is at 5be8943 line 1439.
- Second `round=` key arises only in closed-anchor rows:
  - row-4 at `:2363-2364`: `GL_STATE=not-open; GL_BASIS='row-4'; GL_EXTRA="reason=ledger-close round=$LA_ROUND"`. `GL_AGE` stays `-` because `GL_AGE=$age` is set at `:2375`, after row-4 returns. That yields `age_s=-`.
  - row-6 at `:2409-2411`: `ps_report_closed ... && GL_EXTRA="reason=committed-report round=$LA_ROUND path=..."`.
- Drift mechanism: `drift_scan` concatenates duplicate keys (`:2823-2824` comment, `:2839-2840` code). A second `round=` therefore turns the baseline's `<V>` into `<V><V>`. That code came in with 5be8943 (r10), the same pin that produced the baseline.
- Shapes: row-4 and row-6 `GL_EXTRA` and the `GL_AGE='-'` default were introduced in 1439c47 (r3), per `git log -S`. `reason=ledger-close round=` was modified in 5b62c89 (r4). None changed after r10. Row-6 closure input moved to a branch revision in r17 (`273aa74`, `ps_report_closed ... rev=$4`, amendment A1 falls back to HEAD; `corpus/knowledge/jj-branch-anchor-r17.md:42-45`). The closures cited here are fleet-root commits strictly after launch, so the classification does not rest on that change.
- Live triggers (absent at pin):
  - kumitate row-4: launch round 38 at 04:04:24 -03 (line 561), complete round 38 at 05:10:38 -03 (line 579).
  - kengaku, kake, kagi row-6: reports committed after launch. Rule `lane-silence-r2.md:87` is committed presence plus `launch < ct <= NOW`.
    - kengaku round 26: launch 02:22:27, report 05:54:27.
    - kake round 23: launch 03:26:44, report 06:01:39.
    - kagi round 24: launch 02:43:10, report 07:07:09.
  - Scratch lines 16-32 also show kaidoku, revenger and chousa in row-6 (new roster lanes), and kotodama `round=- reason=no-launch-line`. Those four lanes are added lines (new roster ids), so they produce no field token.
- r10 baseline lines 13-21: all nine paired lanes are `progressing` with a single numeric `round=<V>`.

## 3. Comparison with the round-13 register (`.ufo/waves/round-13/evidence/drift-classification.json`)

- `+FINDING:WATCHDOG_STATE_LAG`: r13 entry (line 8) is `[INFERENCE] current watchdog/wave/lane activity or finding context; no re-pin/admission claim`.
  - AGREE in direction. r13 also attributed the token to current watchdog and lane activity, which matches live-state.
  - DISAGREE in form. It is not one of the four closed classes, it carries no evidence pointer, and the r20 receipt counts it as classified only because the key exists. Under contract section 1 it must be re-classified, which this report does.
  - Reconstruction: r13 measured commit c13df48 at 01:31:55 -03. Its retained drift `started_utc` is `2026-10-20T04:33:14Z` = 01:33:14 -03. That falls inside the ledger gap from line 419 (01:16:19) to line 420 (01:38:55). The reading is consistent with the r13 output: STALE present (log age about 1015 s), LAG present, and no `round` token (kama anchor still open). [INFERENCE: the exact window is derived from the ledger, not from a captured census.]
- `-FINDING:WATCHDOG_STALE`: no r13 entry, and the token is absent from r13 output. There is nothing to agree or disagree with. The r13 stale log is consistent with the new class.
- `round`: no r13 entry, and the token is absent from r13 output. No comparison. The absence is consistent with no paired lane being closed at 01:33 -03.
- All 8 unclassified receipt tokens are new since r13. None of them appears in the r13 register.

## 4. Caveats for the L1 (no classification change)

1. STALE is a freshness proxy. hyaku-inline appends to the same ledger, so STALE can clear with no daemon. ABSENT is the census's only daemon-liveness token. Any freshness claim in C1 should say so.
2. LAG compares two drivers' round numbers. The hyaku-era rounds (for example kumitate 38 against state 18) are not the daemon's counter. The census reports presence only (INFO), so LAG counts are not lag magnitudes.
3. Doc anchors are stale, with no behavior effect (C1 forbids census edits this round). Census comments cite `scripts/shokunin-watchdog.sh:80-81` (census `:88-90`, `:751-753`), but the state write is at `:220` and the launch line at `:221`.
4. The lane-row tokens (`round`, `age_s`, `+path`, `+reason`) are snapshots. The entering receipt is at about 07:18-07:20 -03. Kagi's anchor moved from round 24 to round 25 at 07:23:21, so the closure set moves with the ledger. A re-pin captures live state, and the next `--drift` will name these families again. Classify token families, not single snapshots.
5. `.ufo/waves/round-20/evidence/c1-pin-probe-scratch.json` is a text baseline with a `.json` name (jq cannot parse it). Its census sha is `87b8d680...`, pinned at 10:22:12Z. The author is not recorded. I used it only as corroboration. The ledger had no writes between 07:18:05 and 07:22:12 -03, so its ledger state matches the entering run's.
6. Not verified: whether the entering run's lane lines are byte-identical to the scratch. Only the token set and the row shapes were compared.

## 5. Process, tools, bounds

- Disclosure: one broad `grep` (gitignore:false over the mori-shokunin root) matched fragments of `.ufo/interactive-sessions/*` transcripts. I did not open those files, did not use that text, and cite none of it. Every other read was limited to named files or directories outside `.ufo/interactive-sessions`.
- The census was not executed. No git or jj mutating command was run; only `log`, `show`, `diff`, `cat-file`, `rev-parse` and `hash-object`. Fleet reads were limited to `.ufo/watchdog.log`, `.ufo/state/*`, `scripts/`, and fleet `git log`.
- Tools: none installed or updated. `jq`, `sha256sum`, `grep`, `sed`, `awk` and `stat` were already present.
- No file in the lane was edited except this report. No committed baseline, census, MANIFEST, or lane state was touched.

## 6. Checks the main agent should run

- Record the three rows above in `corpus/evidence/drift-classification-r20.json` with the exact class strings. Re-classify the LAG entry from r13 rather than carrying it forward as [INFERENCE].
- Classify the remaining 47 tokens before the zero-census-regression gate. This report does not establish that gate.
- Re-run the C1 counting command after the register is written.
- Expect the lane-row and LAG token families to move with the live ledger. Do not treat a later non-`none` drift as a regression without re-checking the token family.
