# FamRosterLanes: falsification of the C1 roster classes (round 20)

**PARTIAL.** 12 of 15 roster tokens hold. `+SURFACE:lane.audio`, `+SURFACE:lane.game-dev-2d` and `+SURFACE:lane.game-dev-3d` are classed census-schema-change on the stated cause "lane was a fleet member at the r10 pin". That cause is false: `99efc52` removed their rows from `shokunin.conf` at 2026-10-15T01:52:09-03, 17h34m before the pin (2026-10-15T19:26:29-03), and `db25a48` re-declared them at 2026-10-19T21:03:43-03. Recommended class for those three: `roster-change`. Register counts would move from census-schema-change 29 / roster-change 2 to 26 / 5 (live-state stays 19). Neither class blocks the re-pin, so the re-pin verdict is unaffected.

Scope: `+FINDING:ROSTER_SET_MISMATCH` and the 14 `+SURFACE:lane.*` tokens of `corpus/evidence/drift-classification-r20.json`. Token set checked against `.ufo/waves/round-20/evidence/c1-drift-entering.json` (token_count 50; roster tokens at lines 15 and 21-34).

## Verdicts

| token | register class | verdict | decisive check |
|---|---|---|---|
| +FINDING:ROSTER_SET_MISMATCH | census-schema-change | AGREE | emitted at pin-time inputs by the r12 check alone |
| +SURFACE:lane.chousa | census-schema-change | AGREE | declared at pin (`99efc52:67`) |
| +SURFACE:lane.kaidoku | census-schema-change | AGREE | declared at pin (`99efc52:45`) |
| +SURFACE:lane.lore | census-schema-change | AGREE | declared at pin (`99efc52:53`) |
| +SURFACE:lane.mado | census-schema-change | AGREE | declared at pin (`99efc52:56`) |
| +SURFACE:lane.mori | census-schema-change | AGREE | declared at pin (`99efc52:63`) |
| +SURFACE:lane.revenger | census-schema-change | AGREE | declared at pin (`99efc52:54`) |
| +SURFACE:lane.tabi | census-schema-change | AGREE | declared at pin (`99efc52:58`) |
| +SURFACE:lane.tameshi | census-schema-change | AGREE | declared at pin (`99efc52:55`) |
| +SURFACE:lane.tsukuroi | census-schema-change | AGREE | declared at pin (`99efc52:57`) |
| +SURFACE:lane.audio | census-schema-change | **DISAGREE: roster-change** | removed `99efc52` pre-pin; re-added `db25a48` post-pin; stated reason false |
| +SURFACE:lane.game-dev-2d | census-schema-change | **DISAGREE: roster-change** | same as audio |
| +SURFACE:lane.game-dev-3d | census-schema-change | **DISAGREE: roster-change** | same as audio |
| +SURFACE:lane.kotodama | roster-change | AGREE | sole conf addition `417b1c2`, post-pin |
| +SURFACE:lane.souji | roster-change | AGREE | sole conf addition `7bf2b1a`, post-pin |

## Method

- Census bytes: `sha256sum tools/mori-census.sh` = `87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28` (matches register and contract). The census was NOT run; the item does not authorize it.
- Replay: I extracted `resolve_roster` verbatim (census lines 444-555, `sed -n`, `/tmp/famroster/resolve_roster.sh`) and ran it with a stub `emit_finding` on two fixtures: the pin-time conf (`git show 99efc52:shokunin.conf`, `/tmp/famroster/conf-99efc52.txt`) and the live `shokunin.conf`, both against the live `.ufo/state`. Read-only. The replay confirms the seat lead's set arithmetic (`TokRosterLanes.md` §5), which I did not take on trust.
- Git: `git --no-pager --no-optional-locks` only (log, show, blame, log -S/-G, show -s).
- Seat report `TokRosterLanes.md` used as a lead only; claims re-derived below.

## Pin-time facts (re-derived)

- Baseline `corpus/evidence/baseline-r10-20261015T2231Z.json`: line 2 `census_sha256=d7710981…` = `git show 20e2255:tools/mori-census.sh | sha256sum` (identical at 5be8943). Line 3 `pinned_ts=2026-10-15T22:26:29Z` (epoch 1792103189). Lane rows lines 13-21 are exactly nine IDs (protocol aggregator kasegi kengaku kake kumitate kotoba kagi kama). Line 22 is the silence row without `roster_*`/`conf_*` keys. Lines 1-38 contain no ROSTER_SET_MISMATCH.
- r10 census (`20e2255:tools/mori-census.sh:312`): fixed `ROSTER_LANES=${MORI_ROSTER_LANES:-"protocol … kama"}`. Grep for `shokunin.conf|FLEET_CONF|STATE_DIR|ROSTER_LANES=` finds no conf read and no roster derivation from the state directory (STATE_DIR is read for watchdog values only).
- Current census: `resolve_roster` 444-531 (derivation; blame: 88/88 lines `1f07f1d`), 533-554 (mismatch), `:552` emit `ROSTER_SET_MISMATCH info`, `:2519` loop `for lane in $ROSTER_LANES`, `:2545` emit `SURFACE lane.$lane`. `git log -S ROSTER_SET_MISMATCH -- tools/mori-census.sh` → `1f07f1d` only. The lane-row emitter predates r10 (`1439c47`, 2026-10-15T14:25:51-03), so the 14 new rows come from the `1f07f1d` derivation, not a new emitter.
- Pin-time conf (`99efc52` is the only conf commit between 01:52:09-03 and the pin): 18 IDs = the nine baseline IDs plus chousa, kaidoku, lore, mado, mori, revenger, tabi, tameshi, tsukuroi.
- Pin-time state: all 21 `.round` files have birth time before the pin. Births: 2026-10-13 16:44:48 for the nine baseline IDs; 2026-10-15 01:45:42 for audio, chousa, game-dev-2d, game-dev-3d, kaidoku, lore, mado, mori, revenger, tabi, tameshi, tsukuroi.
- Ledger lines 1-402 (all before the pin; line 402 is `tick=2` at 2026-10-15T01:58:27-03) name exactly those 21 lanes. No pre-pin launch of a lane without a state file, so no sign of pin-time counter deletion. `kotodama` appears nowhere in the ledger; `souji` first appears at line 429 (2026-10-20T02:09:01-03).
- Replay results:
  - Pin-time conf (18) + live state (21): `FINDING ROSTER_SET_MISMATCH severity=info obs=conf_only=none state_only=audio,game-dev-2d,game-dev-3d`; `roster_n=21 conf_n=18 state_n=21`.
  - Live `shokunin.conf` (23) + live state: `FINDING ROSTER_SET_MISMATCH severity=info obs=conf_only=kotodama,souji state_only=none`; `roster_n=23 conf_n=23 state_n=21`.
  - Pin-time union 21 minus nine = 12 new rows; now 23 = 21 + {kotodama, souji}. Matches the register's 12 + 2 split.

## Per-token evidence

### +FINDING:ROSTER_SET_MISMATCH: AGREE (census-schema-change)

- Emitter `tools/mori-census.sh:552`, inside `resolve_roster`; fires only when both sources are readable and their sets differ (`:533-554`).
- Introduced by `1f07f1d` only (`git log -S`); `corpus/knowledge/roster-truth-r12.md:19-21` describes it as info severity, never changing CLEAN/DRIFT (verified).
- Absent from the baseline (lines 1-38).
- The token is produced by the r12 check alone at pin-time inputs (replay above: `state_only=audio,game-dev-2d,game-dev-3d`). The current content (`conf_only=kotodama,souji`) differs, but the token name carries no content: the entering drift lists `+FINDING:ROSTER_SET_MISMATCH` with no payload.

### Nine declared-at-pin lanes: AGREE (census-schema-change)

Each is declared in `99efc52:shokunin.conf` (line in parentheses), has a state file born 2026-10-15 01:45:42 (pre-pin), has a pre-pin launch line in `watchdog.log`, and is absent from the r10 fixed roster. Membership was not removed between declaration and pin.

- chousa: conf 67 (`cb3c103`, 2026-10-14 21:24:03, comment "minted 2026-10-14T21:17:40"); birth 01:45:42.234; launch line 340.
- kaidoku: conf 45 (declared since `cdb3168`, 2026-10-13); birth 01:45:42.264; launch line 351.
- lore: conf 53 (`cdb3168`); birth 01:45:42.233; launch line 339.
- mado: conf 56 (`9ee7059`, 2026-10-14 09:51:17; closing quote repaired by `14e836c`, 2026-10-14 20:23:28, before the pin); birth 01:45:42.294; launch line 358.
- mori: conf 63 (`cb3c103`, comment "minted 2026-10-14T21:17:36"); birth 01:45:42.320; launch line 363; respawn line 400.
- revenger: conf 54 (`cdb3168`; reformatted by `14e836c`); birth 01:45:42.267; launch line 352.
- tabi: conf 58 (`9ee7059`; `14e836c`); birth 01:45:42.315; launch line 362.
- tameshi: conf 55 (`9ee7059`); birth 01:45:42.230; launch line 338.
- tsukuroi: conf 57 (`9ee7059`); birth 01:45:42.306; launch line 361.

### audio, game-dev-2d, game-dev-3d: DISAGREE (register says census-schema-change; recommended roster-change)

Facts:
- `99efc52` (2026-10-15T01:52:09-03, subject "ops: exclude the three Devin-owned lanes (18 remain)") removed `audio|`, `game-dev-2d|` and `game-dev-3d|` from `shokunin.conf` (`git show 99efc52` hunk `@@ -53,3 +52,0 @@`). The file at 99efc52 has no row for any of them.
- The pin is 2026-10-15T19:26:29-03 (baseline line 3), 17h34m after that removal. The removal was therefore a pre-pin fleet change.
- `watchdog.log` contains these names only at lines 336 (game-dev-2d), 337 (audio) and 353 (game-dev-3d), all `launch … round=1` at 01:45:42, before the removal. No later line mentions them; the daemon's last tick is line 402 (01:58:27), and no line in the ledger after 402 names them.
- Their `.round` files have birth time equal to mtime (2026-10-15 01:45:42.228, .225 and .272): frozen since the pre-removal launch.
- `db25a48` (2026-10-19T21:03:43-03, "Fix fleet lane configuration") re-added the three rows. That is post-pin.
- The register's reason "lane was a fleet member at the r10 pin" is false in the declared sense used for kotodama and souji. The cited pointer `watchdog.log:336-363` shows only pre-removal launches; it cannot establish pin-time membership.

Why roster-change: the only declared-membership change across the pin for these lanes is out (pre-pin) then in (post-pin). Their census rows come from orphan driver counters on the r12 state-only path, which the register does not name as the reason.

Strongest counter-argument, recorded so the L1 can decide: the census roster is declared ∪ driver counters (`1f07f1d` commit message; `roster-truth-r12.md:19`). Under that union the three were in the roster at pin, and `db25a48` changed no row. On that definition census-schema-change would be the only difference-maker, and the class could stand. The register does not state that definition. Its reason text and its kotodama/souji rule both use fleet/declared membership, so under the register's own test the premise fails. If the L1 adopts the union definition instead, the reason must be rewritten to say "driver-counter row present at pin", and it must not say "fleet member".

Suggested reason text for the register: "declared fleet membership removed by 99efc52 (2026-10-15T01:52:09-03, before the r10 pin) and re-added by db25a48 (2026-10-19T21:03:43-03, after it); row from the r12 state-only path over orphan audio.round (born 01:45:42, no launch after 01:45:42)."

### kotodama: AGREE (roster-change)

- Sole addition of a `kotodama|` row to `shokunin.conf`: `417b1c2` (2026-10-17T01:27:58-03, "mint: wire kotodama-shokunin (conf lane + MANIFEST mint entry + roster-scan evidence)"; `shokunin.conf | 5 +`). Post-pin.
- Absent at 99efc52; no `kotodama.round` in `.ufo/state`; zero ledger mentions (`grep -c kotodama` = 0).
- Replay: absent from the pin-time roster (21 names), present now (`conf_only=kotodama,souji`).

### souji: AGREE (roster-change)

- Sole addition of a `souji|` row: `7bf2b1a` (2026-10-18T11:55:14-03, "mint: souji lane wiring …"; `shokunin.conf | 5 +`). Post-pin.
- Absent at 99efc52; no `souji.round`; first ledger mention is line 429 (launch, 2026-10-20T02:09:01-03), after the pin.

## Corrections the L1 must make if these verdicts are adopted

1. Reclassify audio, game-dev-2d and game-dev-3d to roster-change, with the reason text above.
2. `corpus/evidence/drift-classification-r20.json` `class_counts`: census-schema-change 26, roster-change 5 (live-state 19). Total 50 unchanged.
3. `corpus/knowledge/drift-repin-r20.md:30` ("census-schema-change 29 … roster-change 2") needs the same change.
4. Re-run the register counting command after editing; the unclassified count is unaffected (all 50 tokens still classed, all with pointers).

## Out-of-scope observations (verified; for the L1)

1. Register `dissent` text says "census code byte-identical since r10". Contradicted: `git log --format='%h %ad %s' 20e2255..HEAD -- tools/mori-census.sh` lists 7 commits (`1f07f1d` 2026-10-19, `18d7d55`, `8d22d18`, `26f6589`, `273aa74`, `2be8294`, `fe9fa90`), and the census sha changed from `d7710981` (baseline line 2) to `87b8d680`. This affects the census-regression routing argued for the WATCHDOG and WAVE tokens; I did not verify those tokens.
2. Commit `9ee7059` subject says "roster rows withheld pending probation", but its diff adds the four rows (tameshi, mado, tsukuroi, tabi) to the conf. Pin membership is unaffected; the message is misleading.
3. The state-only path keeps grading the three excluded lanes from frozen counters; the daemon has made no tick since line 402, and the hyaku driver does not write `.round`. This is the residual `roster-truth-r12.md:25` already names; it keeps ROSTER_SET_MISMATCH and the three rows alive. It is a census design residual, not a class error.
4. Seat lead `TokRosterLanes.md` §8 says "All 12 were fleet members at the pin". Wrong for the three; its own §5 records their pre-pin removal. §5 also says `10405f4` re-added them; the diff of `10405f4` only wraps the LANES block (adds `"`, a blank line, a comment and `LANES="$LANES` after souji's row). The re-add is `db25a48`.

## Limits (not observed)

- Pin-time conf is taken from git history (`99efc52`). Any uncommitted edit to `shokunin.conf` at pin time is unobservable.
- Post-pin deletion of `.round` files cannot be excluded by birth times. The ledger's pre-pin lane set (= the 21 current names) is the only support against it.
- The replay runs the extracted function on fixtures; the census binary was not run, so the emitted SURFACE lines were not captured. [INFERENCE] that the binary prints exactly the replayed rows; the loop (`:2519`) and emitter (`:2545`) were read, not executed.
- Not read, per bounds: `.ufo/interactive-sessions/`, `.ufo/worktrees/`, `.jj/`, `~/.omp` session logs.

## Commands and exit codes

- `sha256sum tools/mori-census.sh` → `87b8d680…ab28`, rc 0.
- `git log -S ROSTER_SET_MISMATCH -- tools/mori-census.sh` → `1f07f1d`, rc 0.
- `git blame -s -L 444,531 -- tools/mori-census.sh` → 88 lines `1f07f1d`, rc 0.
- `git show 99efc52:shokunin.conf > /tmp/famroster/conf-99efc52.txt` → 67 lines, rc 0.
- `git log -G"^<id>\|" -- shokunin.conf` for each of the 21 conf IDs, rc 0.
- `git show --stat` for `417b1c2`, `7bf2b1a`, `99efc52`, `db25a48`, `10405f4`, `9ee7059`, `14e836c`, `cb3c103`, `7d02e96`, rc 0.
- `stat -c '%n birth=%w mtime=%y' .ufo/state/*.round` → births as above, rc 0.
- `grep -nE '(audio|game-dev-2d|game-dev-3d)' .ufo/watchdog.log` → lines 336, 337, 353 only, rc 0.
- `grep -nE 'tick=' .ufo/watchdog.log` → last line 402, rc 0.
- `bash /tmp/famroster/driver.sh` (replay of extracted function) → as above, rc 0.
- First attempt `git show 20e2255:…` ran in the fleet repo → `fatal: invalid object name`, rc 128. Re-run in `mori-shokunin` → `d7710981…`, rc 0.

## Tooling

No tools installed or updated. Scratch files only under `/tmp/famroster/`.
