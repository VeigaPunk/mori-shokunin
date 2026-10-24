# TokRosterLanes — C1 roster token classification (round 20)

Seat: MoriR20.TokRosterLanes (leaf; no subagents). Scope: the 15 roster tokens of `.ufo/waves/round-20/evidence/c1-drift-entering.json` (`+FINDING:ROSTER_SET_MISMATCH` and `+SURFACE:lane.<id>` for the 14 lanes). Census bytes checked: `sha256sum tools/mori-census.sh` = `87b8d680…ab28` (matches the contract). `tools/mori-census.sh` was NOT run (not in this item); every "now" value below is either read from a file or replicated read-only and is marked [INFERENCE] where so.

## Result

| class | count | tokens |
|---|---|---|
| census-schema-change | 13 | `+FINDING:ROSTER_SET_MISMATCH`, `+SURFACE:lane.{audio,chousa,game-dev-2d,game-dev-3d,kaidoku,lore,mado,mori,revenger,tabi,tameshi,tsukuroi}` |
| roster-change | 2 | `+SURFACE:lane.kotodama`, `+SURFACE:lane.souji` |
| live-state | 0 | — |
| census-regression | 0 | — |

- No token of this scope is a census regression, so none of the 15 blocks a re-pin on this seat's evidence. The re-pin decision is the L1's; the other 35 tokens are out of scope.
- Round-13 register (`.ufo/waves/round-13/evidence/drift-classification.json`): agrees on 13, disagrees on 2 (kotodama, souji). Details in §5.

## 1. Rule used and why

The baseline (r10) and the entering run differ in two inputs: the census (`d7710981` → `87b8d680`) and the fleet (roster inputs at pin → now). I decompose in census-first order:

- Step A: entering census on the pin-time fleet. Tokens created here are **census-schema-change**.
- Step B: pin-time fleet → now, under the entering census. Tokens created only here are **roster-change**.

Census-first matches the contract's class definitions: `live-state` and roster differences are evaluated with the same census logic. A fleet-first order would attribute all 14 lanes to the census; I reject that for the reason in §5.

Replay result (read-only, from §5): union(pin) − builtin9 = the 12 lanes; union(now) − union(pin) = `{kotodama, souji}`; the state-file set has not changed since the pin.

## 2. Census emitters now (`tools/mori-census.sh`, sha `87b8d680`)

- `:552` `emit_finding ROSTER_SET_MISMATCH info "conf_only=… state_only=…"` inside `resolve_roster()` (`:444–555`). Fires only when both conf and state are readable and their sets differ. `emit_finding` (`:419–431`) flips ROLL only for warn/crit, so this info finding never changes CLEAN/DRIFT.
- `:2545` `SURFACE_LINES+=("SURFACE lane.$lane: …")`. This is the only lane-row emitter (`grep -nE 'SURFACE lane\.|emit_finding ROSTER|SURFACE_LINES\+=' tools/mori-census.sh` → `:436` generic emit_surface, `:552`, `:2545`). It sits in `probe_silence()`'s loop `for lane in $ROSTER_LANES` (`:2519`), fed by `resolve_roster` (`:2512`).
- Roster sources: conf rows only inside `LANES="…"` (`:462–484`, `FLEET_CONF` `:370`); state regular `*.round` basenames, symlinks excluded (`:486–502`, `STATE_DIR` `:302`); union `:510–513`; source label and builtin fallback `:515–528` (builtin list `:527`, used only when neither source yields an id).
- Default root: `tools/mori-census.sh:286–295` maps the lane `mori-shokunin` to its parent, `/home/vgpnk/Projects/shokunin`, so conf and state are the fleet's (`MORI_SHOKUNIN_ROOT` unset in this shell: `env | grep -c '^MORI_'` → 0).
- Drift token naming: `drift_line_id` `:2808–2818` maps `SURFACE lane.X:` → `SURFACE:lane.X` and `FINDING ID severity=` → `FINDING:ID`. Pass 3 of `drift_report` (`:2907–2910`) prints `+<id>` for every new-side line with no baseline pair.

## 3. Baseline and pin-time census

- `corpus/evidence/baseline-r10-20261015T2231Z.json:2` `census_sha256=d7710981…`, `:3` `pinned_ts=2026-10-15T22:26:29Z`.
- Lane rows `:13–21`: exactly nine (`protocol aggregator kasegi kengaku kake kumitate kotoba kagi kama`). No `ROSTER_SET_MISMATCH` line; `:24–38` contain only WATCHDOG/WAVE/KILL/SEGFAULT findings.
- The r10 census (`git show 20e2255:tools/mori-census.sh | sha256sum` → `d7710981…`, identical bytes at `5be8943`) has a fixed roster at `:312`: `ROSTER_LANES=${MORI_ROSTER_LANES:-"protocol aggregator kasegi kengaku kake kumitate kotoba kagi kama"}`. Its lane loop is `:1423` and its row emit `:1439`. It reads `.ufo/state/*.round` values for the watchdog surface and for per-lane not-open grading (`:1316`), but builds the roster only from that fixed default: it never reads conf and never derives lanes from the state directory listing.

## 4. Introducing commits (git, read-only)

- `git log -S ROSTER_SET_MISMATCH --oneline -- tools/mori-census.sh` → `1f07f1d`. The same single commit comes back for `roster_source`, `resolve_roster`, `conf_dropped_n`, `FLEET_CONF`.
- `git blame -L 444,555 -- tools/mori-census.sh` → all 112 lines `1f07f1d` (2026-10-19 19:41:08 -0300). So the roster derivation has not changed since r12. `:552` and `:527` also blame to `1f07f1d`.
- Row emit: `git blame -L 2545,2545` → `1439c47` (2026-10-15 14:25:51 -0300; `git log -S 'SURFACE lane.'` → `1439c47`). Lane loop `:2519` → `7ca17b1` (r1).
- Fixed 9-lane default: `git log -S 'protocol aggregator kasegi'` → `7ca17b1`.
- `git log -S` for the lane ids (`kotodama`, `souji`, `game-dev-2d`, `lane.audio`) returns no census commit: ids are data read from conf and state, not census literals.

## 5. Membership: pin-time replay vs now

Replication (read-only; census not run) of `resolve_roster` set logic: conf = `shokunin.conf` ids, state = regular `.ufo/state/*.round` names. Pin-time conf = `git show 99efc52:shokunin.conf` (commit `99efc52`, 2026-10-15 01:52:09 -0300, subject "ops: exclude the three Devin-owned lanes (18 remain)"). Pin-time state = the 21 `.round` files, all with mtime before the pin (`2026-10-15T22:26:29Z`).

| set | conf_n | state_n | union | conf_only | state_only |
|---|---|---|---|---|---|
| pin-time replay [INFERENCE] | 18 | 21 | 21 | none | audio,game-dev-2d,game-dev-3d |
| now replay [INFERENCE] | 23 | 21 | 23 | kotodama,souji | none |

- union(pin) − builtin9 = `audio,chousa,game-dev-2d,game-dev-3d,kaidoku,lore,mado,mori,revenger,tabi,tameshi,tsukuroi` (12).
- union(now) − union(pin) = `kotodama,souji` (2). The state-file name set is identical at pin and now.
- Pin-time replay of the r20 census therefore already prints the 12 rows and emits `ROSTER_SET_MISMATCH` (state_only = the three physical lanes). The census change alone produces 13 tokens.
- Watchdog first launch of each of the 12 at `2026-10-15T01:45:42-03:00`, before the pin: `.ufo/watchdog.log` lines `336 game-dev-2d`, `337 audio`, `338 tameshi`, `339 lore`, `340 chousa`, `351 kaidoku`, `352 revenger`, `353 game-dev-3d`, `358 mado`, `361 tsukuroi`, `362 tabi`, `363 mori`.
- `kotodama`: no `launch kotodama` line anywhere in `.ufo/watchdog.log` (`grep -m1 -E " launch kotodama round=" …` → none). Its r12 receipt reads `not-open reason=no-launch-line` (`corpus/evidence/roster-r12-20261019T220912Z-live.log:29`).
- `souji`: first launch `.ufo/watchdog.log:429` at `2026-10-20T02:09:01-03:00`. No `.round` file, at pin or now.
- Fleet commits after the pin (`2026-10-15T22:26:29Z` = `2026-10-15 19:26:29 -0300`): `417b1c2` (2026-10-17 01:27:58 -0300, "mint: wire kotodama-shokunin (conf lane + MANIFEST mint entry + roster-scan evidence)") adds the kotodama row and `# minted 2026-10-17`; `7bf2b1a` (2026-10-18 11:55:14 -0300, "mint: souji lane wiring — operator demand, roster scan, conf lane, MANIFEST mint entry") adds the souji row and `# minted 2026-10-18`; `db25a48` (2026-10-19 21:03:43 -0300) and `10405f4` (2026-10-19 21:07:43 -0300, comment "Existing physical lanes added to driver coverage by kaika (not new mints)") re-add audio/game-dev-2d/game-dev-3d to conf. Those three were already state members, so union is unchanged by that re-add.
- Commit `99efc52` diff removed exactly the rows `audio|…`, `game-dev-2d|…`, `game-dev-3d|…`, before the pin.

## 6. Intent lines (round LOG / SCORECARD / knowledge)

- `LOG.md:661–667` (round 12, claim 3 "coverage"): census roster = shokunin.conf ids ∪ `.ufo/state/*.round`; live lane rows 9 → 23; info `ROSTER_SET_MISMATCH` (conf-only kotodama,souji; state-only audio,game-dev-2d,game-dev-3d).
- `LOG.md:669–673`: "After claim 3 the drift additionally names the 14 new lane rows and roster fields … No re-pin (planned r13)."
- `SCORECARD.md:605` (row 3), `:611` "14 lanes graded that were invisible (incl. mori itself)", `:613` freshness "names exactly the 14 new lane rows … detection working, no re-pin this round".
- `corpus/knowledge/roster-truth-r12.md:9–13` (sets; "Declared-only — 2 IDs: kotodama,souji"; "Counter-only — 3 IDs"), `:19–21` (decision; info finding "never changes CLEAN/DRIFT"; "changes remain visible to --drift").
- `corpus/evidence/drift-r12-20261019T2230Z-after-roster.log:4`: "+SURFACE:lane.* (14) and the roster_* fields are the intended round-12 roster change (claim 3)".
- `tools/mori-census.sh:2738–2739`: "Roster source/count fields intentionally remain non-volatile: roster changes alter behavior and must be reported by --drift."
- Round 13: `LOG.md:754`, `SCORECARD.md:694`: "carried r12 roster schema".
- Membership intent for kotodama and souji is not in LOG/SCORECARD. `grep -nE 'kotodama|souji' LOG.md SCORECARD.md` hits only the r12 mismatch measurement (`LOG.md:663`, `SCORECARD.md:605`) and the PROVINCE adjacency row (`SCORECARD.md:614`, `LOG.md:676`, not membership). The membership intent is the fleet commit messages `417b1c2`, `7bf2b1a` and the conf comments "minted 2026-10-17/18 (operator directive, orchestrator-minted)".

## 7. JSON-ready table (`token|class|reason|evidence`)

Same content as `.ufo/waves/round-20/build/TokRosterLanes/register-draft.json` (validated with `jq`: 15 rows, classes 13/2, token set equal to the scope).

```json
{
  "seat": "MoriR20.TokRosterLanes",
  "scope": "C1 roster tokens of evidence/c1-drift-entering.json: +FINDING:ROSTER_SET_MISMATCH and the 14 +SURFACE:lane.<id> tokens (15 of 50)",
  "rule": "census-first decomposition. Step A replaces the r10 census (sha d7710981, 20e2255) with the entering census (sha 87b8d680) on the pin-time fleet (conf at 99efc52, state files existing at pin 2026-10-15T22:26:29Z); tokens that appear in step A are census-schema-change. Step B changes the fleet from pin to now under the entering census; tokens that appear only in step B are roster-change. Replay is read-only; tools/mori-census.sh was not run.",
  "rows": [
    {"token": "+FINDING:ROSTER_SET_MISMATCH", "class": "census-schema-change", "reason": "Info-level finding introduced by the intended r12 roster reconciliation (never flips ROLL). The r10 census never emitted it. Step A replay (entering census on pin-time fleet: conf 18 ids, a subset of state 21 ids) emits it with state_only=audio,game-dev-2d,game-dev-3d, so the census change alone produces the token. Live content has since changed (replicated now: conf_only=kotodama,souji, state_only=none) but the drift token is keyed by finding id, not content.", "evidence": "emit tools/mori-census.sh:552 (blame 1f07f1d); id list tools/mori-census.sh:271; selftests tools/mori-census.sh:3437-3461 (not run); baseline corpus/evidence/baseline-r10-20261015T2231Z.json has no FINDING ROSTER_SET_MISMATCH line; git log -S ROSTER_SET_MISMATCH -> 1f07f1d only; intent LOG.md:661-663, SCORECARD.md:605, corpus/knowledge/roster-truth-r12.md:19-21; r12 receipt corpus/evidence/roster-r12-20261019T220912Z-live.log:50"},
    {"token": "+SURFACE:lane.audio", "class": "census-schema-change", "reason": "Live fleet lane at the pin: state audio.round mtime 2026-10-15 01:45:42 -03 and first launch watchdog.log:337 (2026-10-15T01:45:42-03:00), both before the pin. The r10 census printed only the fixed 9-lane default, so no row. The intended r12 roster derivation (conf union state) prints it. Pin-time roster union already contained it (state-only at pin).", "evidence": "emit tools/mori-census.sh:2545 (loop :2519, resolve_roster :444-531, state read :486-502); r10 fixed default 20e2255:tools/mori-census.sh:312; baseline corpus/evidence/baseline-r10-20261015T2231Z.json:13-21 (no audio row); introduced 1f07f1d (blame 444-555 all 1f07f1d); intent LOG.md:661-667, SCORECARD.md:611; fleet 99efc52 removed conf row before pin, db25a48 re-added it 2026-10-19 (union unchanged)"},
    {"token": "+SURFACE:lane.chousa", "class": "census-schema-change", "reason": "Live fleet lane at the pin: conf row present at 99efc52 and state chousa.round mtime 2026-10-15 01:50:57 -03; first launch watchdog.log:340 before the pin. Absent from the r10 fixed 9-lane default; printed by the intended r12 roster derivation.", "evidence": "emit tools/mori-census.sh:2545 (roster :444-531); 20e2255:tools/mori-census.sh:312; baseline :13-21 (no row); introduced 1f07f1d; intent LOG.md:661-667, SCORECARD.md:611 ('14 lanes graded that were invisible (incl. mori itself)'); fleet conf 99efc52 contains chousa"},
    {"token": "+SURFACE:lane.game-dev-2d", "class": "census-schema-change", "reason": "Live fleet lane at the pin: state game-dev-2d.round mtime 2026-10-15 01:45:42 -03; first launch watchdog.log:336 before the pin. Conf row was absent at pin (removed by 99efc52), so the lane entered the pin-time roster union through state. The r10 census never read state for the roster; the r12 derivation does.", "evidence": "emit tools/mori-census.sh:2545 (roster :444-531, state read :486-502); 20e2255:tools/mori-census.sh:312; baseline :13-21 (no row); introduced 1f07f1d; fleet 99efc52 (2026-10-15 01:52:09 -0300) removed row, db25a48 (2026-10-19) re-added; r12 receipt roster-r12-...-live.log:32 progressing row (state-only at r12 per :50 obs)"},
    {"token": "+SURFACE:lane.game-dev-3d", "class": "census-schema-change", "reason": "Live fleet lane at the pin: state game-dev-3d.round mtime 2026-10-15 01:45:42 -03; first launch watchdog.log:353 before the pin. Conf row absent at pin (removed by 99efc52); state-only path, same as game-dev-2d. Printed only by the r12 roster derivation.", "evidence": "emit tools/mori-census.sh:2545 (roster :444-531); 20e2255:tools/mori-census.sh:312; baseline :13-21 (no row); introduced 1f07f1d; fleet 99efc52 removed row, db25a48 re-added; r12 receipt roster-r12-...-live.log:33"},
    {"token": "+SURFACE:lane.kaidoku", "class": "census-schema-change", "reason": "Live fleet lane at the pin: conf row present at 99efc52 and state kaidoku.round mtime 2026-10-15 01:50:57 -03; first launch watchdog.log:351 before the pin. Absent from the r10 fixed default; printed by the r12 derivation.", "evidence": "emit tools/mori-census.sh:2545 (roster :444-531); 20e2255:tools/mori-census.sh:312; baseline :13-21 (no row); introduced 1f07f1d; intent LOG.md:661-667"},
    {"token": "+SURFACE:lane.lore", "class": "census-schema-change", "reason": "Live fleet lane at the pin: conf row present at 99efc52 and state lore.round mtime 2026-10-15 01:50:57 -03; first launch watchdog.log:339 before the pin. Absent from the r10 fixed default; printed by the r12 derivation.", "evidence": "emit tools/mori-census.sh:2545 (roster :444-531); 20e2255:tools/mori-census.sh:312; baseline :13-21 (no row); introduced 1f07f1d; intent LOG.md:661-667"},
    {"token": "+SURFACE:lane.mado", "class": "census-schema-change", "reason": "Live fleet lane at the pin: conf row present at 99efc52 and state mado.round mtime 2026-10-15 01:50:57 -03; first launch watchdog.log:358 before the pin. Absent from the r10 fixed default; printed by the r12 derivation.", "evidence": "emit tools/mori-census.sh:2545 (roster :444-531); 20e2255:tools/mori-census.sh:312; baseline :13-21 (no row); introduced 1f07f1d; intent LOG.md:661-667"},
    {"token": "+SURFACE:lane.mori", "class": "census-schema-change", "reason": "Live fleet lane at the pin: conf row present at 99efc52 (minted 2026-10-14) and state mori.round mtime 2026-10-15 01:50:57 -03; first launch watchdog.log:363 before the pin. Absent from the r10 fixed default; the r12 derivation grades the observing lane itself.", "evidence": "emit tools/mori-census.sh:2545 (roster :444-531); 20e2255:tools/mori-census.sh:312; baseline :13-21 (no row); introduced 1f07f1d; intent SCORECARD.md:611 ('incl. mori itself'), LOG.md:661-667"},
    {"token": "+SURFACE:lane.revenger", "class": "census-schema-change", "reason": "Live fleet lane at the pin: conf row present at 99efc52 and state revenger.round mtime 2026-10-15 01:50:57 -03; first launch watchdog.log:352 before the pin. Absent from the r10 fixed default; printed by the r12 derivation.", "evidence": "emit tools/mori-census.sh:2545 (roster :444-531); 20e2255:tools/mori-census.sh:312; baseline :13-21 (no row); introduced 1f07f1d; intent LOG.md:661-667"},
    {"token": "+SURFACE:lane.tabi", "class": "census-schema-change", "reason": "Live fleet lane at the pin: conf row present at 99efc52 and state tabi.round mtime 2026-10-15 01:50:57 -03; first launch watchdog.log:362 before the pin. Absent from the r10 fixed default; printed by the r12 derivation.", "evidence": "emit tools/mori-census.sh:2545 (roster :444-531); 20e2255:tools/mori-census.sh:312; baseline :13-21 (no row); introduced 1f07f1d; intent LOG.md:661-667"},
    {"token": "+SURFACE:lane.tameshi", "class": "census-schema-change", "reason": "Live fleet lane at the pin: conf row present at 99efc52 and state tameshi.round mtime 2026-10-15 01:50:57 -03; first launch watchdog.log:338 before the pin. Absent from the r10 fixed default; printed by the r12 derivation.", "evidence": "emit tools/mori-census.sh:2545 (roster :444-531); 20e2255:tools/mori-census.sh:312; baseline :13-21 (no row); introduced 1f07f1d; intent LOG.md:661-667"},
    {"token": "+SURFACE:lane.tsukuroi", "class": "census-schema-change", "reason": "Live fleet lane at the pin: conf row present at 99efc52 and state tsukuroi.round mtime 2026-10-15 01:50:57 -03; first launch watchdog.log:361 before the pin. Absent from the r10 fixed default; printed by the r12 derivation.", "evidence": "emit tools/mori-census.sh:2545 (roster :444-531); 20e2255:tools/mori-census.sh:312; baseline :13-21 (no row); introduced 1f07f1d; intent LOG.md:661-667"},
    {"token": "+SURFACE:lane.kotodama", "class": "roster-change", "reason": "Fleet membership added after the pin: conf row minted 2026-10-17 (commit 417b1c2); no .round state file and no launch line in watchdog.log at any time (r12 receipt: not-open reason=no-launch-line). Absent from the pin-time roster union (21 ids), so step A does not print it; step B adds it. The r12 derivation makes it visible but does not cause the membership change.", "evidence": "fleet git 417b1c2 (2026-10-17 01:27:58 -0300) adds conf row and '# minted 2026-10-17' comment; pin-time conf = 99efc52 (18 ids, no kotodama); no 'launch kotodama' line in .ufo/watchdog.log; r12 receipt corpus/evidence/roster-r12-20261019T220912Z-live.log:29; emit tools/mori-census.sh:2545; round-13 label .ufo/waves/round-13/evidence/drift-classification.json:16 disagrees"},
    {"token": "+SURFACE:lane.souji", "class": "roster-change", "reason": "Fleet membership added after the pin: conf row minted 2026-10-18 (commit 7bf2b1a); no .round state file; first launch watchdog.log:429 at 2026-10-20T02:09:01-03:00. Absent from the pin-time roster union, so step A does not print it; step B adds it.", "evidence": "fleet git 7bf2b1a (2026-10-18 11:55:14 -0300) adds conf row and '# minted 2026-10-18' comment; pin-time conf = 99efc52 lacks souji; .ufo/watchdog.log:429; r12 receipt roster-r12-20261019T220912Z-live.log:30 (not-open); emit tools/mori-census.sh:2545; round-13 label drift-classification.json:21 disagrees"}
  ],
  "counts": {"census-schema-change": 13, "roster-change": 2, "live-state": 0, "census-regression": 0}
}
```

## 8. Round-13 comparison (`.ufo/waves/round-13/evidence/drift-classification.json`)

Round 13 labels all 15 tokens `r12 roster schema carried since r10` (`:7`, `:11–24`). It uses free-text causes, not the closed set, so the class comparison is my mapping [INFERENCE]: "r12 roster schema" = census-schema-change.

| token(s) | round-13 label | this seat | agree? | reason |
|---|---|---|---|---|
| `+FINDING:ROSTER_SET_MISMATCH` | r12 roster schema carried since r10 | census-schema-change | agree | Same mechanism. Pin-time replay emits it with the census change alone. |
| `+SURFACE:lane.{audio,chousa,game-dev-2d,game-dev-3d,kaidoku,lore,mado,mori,revenger,tabi,tameshi,tsukuroi}` (12) | r12 roster schema carried since r10 | census-schema-change | agree | All 12 were fleet members at the pin (state files pre-pin; 9 had conf rows at 99efc52; 3 were state-only). The r10 fixed list never printed them. |
| `+SURFACE:lane.kotodama`, `+SURFACE:lane.souji` | r12 roster schema carried since r10 | roster-change | **disagree** | "Carried since r10" is wrong for these two. Neither was a fleet member at the pin: conf rows minted 2026-10-17 and 2026-10-18 (`417b1c2`, `7bf2b1a`); no state file at pin; watchdog launches start later for souji and never for kotodama. The r12 census made them visible, but the membership change is the cause that separates them from the baseline. |

Round 12 (`drift-r12-20261019T2230Z-after-roster.log:4`) also calls all 14 "the intended round-12 roster change". That is right for the mechanism and wrong only for the two membership additions, which were already minted when that receipt was written.

Alternatives considered and rejected:
- All 14 as roster-change: rejected. The 12 lanes were already fleet members at the pin (§5), so nothing about their membership changed since the baseline.
- All 14 as census-schema-change (fleet-first order): rejected. For kotodama and souji the only roster-union change since the pin is their membership (union(now) − union(pin) = `{kotodama, souji}`). The contract's `live-state` / roster definitions evaluate fleet differences under the current census logic, which is census-first.

## 9. Other observations (not classes; no token changes)

- ROSTER_SET_MISMATCH content changed, token did not. The r12 receipt (`roster-r12-…-live.log:50`) reads `conf_only=kotodama,souji state_only=audio,game-dev-2d,game-dev-3d`. Replicated now: `conf_only=kotodama,souji state_only=none`. The three physical lanes were re-added to conf by `db25a48`/`10405f4` on 2026-10-19 after the r12 run (22:38:11Z). Drift keys on the finding id, so this does not appear as a token.
- `.ufo/state/*.round` values are stale. `kagi.round` = `16`, mtime `2026-10-15 01:50:57 -03`, while `.ufo/watchdog.log:585` shows `launch kagi round=25` on 2026-10-21 under `driver=hyaku-inline`. The roster uses only file names, so membership is unaffected. But `ROSTER_SET_MISMATCH` will keep flagging conf-only lanes until a state file exists, and souji has launches but no `.round` file. [observed]
- Policy point (not a token): the three lanes excluded from conf at `99efc52` ("exclude the three Devin-owned lanes") remain graded through their state files. This is the designed state-only path that `ROSTER_SET_MISMATCH` exists to expose (`roster-truth-r12.md:19–21`). Not a regression; for the operator to rule.
- Cross-seat (IRC from MoriR20.TokRosterFields, verified here): the six roster-field keys (`roster_source`, `roster_n`, `conf_n`, `state_n`, `conf_dropped_n`, `state_dropped_n`) are census-schema-change. `tools/mori-census.sh:2552` emits them unconditionally, so they appear in the step-A replay; their values are step-B and are not token classes. Their report carries the pin-to-now `conf_n`/`roster_n` trajectory. Not classified in this report.

## 10. Unobserved / inferred, and checks

- [INFERENCE] "now" and "pin-time" roster sets are replicated read-only with `comm`/`sort`. The census was not run. Pin-time membership is evidenced by birth times, not only mtimes: `stat -c %W` on all 21 regular `.ufo/state/*.round` files gives a latest birth of `1792039542` (2026-10-15 01:45:42 -0300) against the pin epoch `1792103189` (2026-10-15 19:26:29 -0300); none is born after the pin or has unknown birth time. The watchdog launch lines corroborate it for all 12 lanes.
- [INFERENCE] `roster_source=conf+state` at the entering run. The receipt records only the token list, not the roster source value or the environment. `MORI_*` variables are unset in this shell; the L1's runner environment is unrecorded.
- Selftests, oracle and mutation runs were not executed (not assigned).
- Git: read-only only (`log`, `show`, `blame -L`, `log -S`/`-L`, `sha256sum`). No git or jj mutating command. No edits to the census, any baseline, the fleet repo, lane repos or `.ufo/state`.
- Tools: no installs or updates. Scratch files in `/tmp` were removed.
- Writes: this report; `.ufo/waves/round-20/build/TokRosterLanes/register-draft.json` (seat-local draft, validated with `jq`).
- Not read: any retained session transcript or `~/.omp` session log.
