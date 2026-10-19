source: FLEET/shokunin.conf; FLEET/scripts/shokunin-watchdog.sh:14; FLEET/PROTOCOL-APPENDIX.md 'Lane universe' row; tools/mori-census.sh:312-319,383-489,1530-1563
verified-at: 2026-10-19 (census sha 3da5b098dc23aeb3e1c31ce82664b24a22c2847a168308a755525593881b3164)
recheck: MORI_SHOKUNIN_ROOT=/home/vgpnk/Projects/shokunin bash tools/mori-census.sh | grep -c '^SURFACE lane\.' → 23 (roster_source=conf+state; conf_only=kotodama,souji; state_only=audio,game-dev-2d,game-dev-3d)

# Silence roster truth (round 12)

## Measured sets

- **Declared config set — 20 IDs.** Command: `grep -oE '^[a-z0-9][a-z0-9-]*\|' /home/vgpnk/Projects/shokunin/shokunin.conf | cut -d'|' -f1 | LC_ALL=C sort -u` (count: append `| wc -l`). IDs: `aggregator,chousa,kagi,kaidoku,kake,kama,kasegi,kengaku,kotoba,kotodama,kumitate,lore,mado,mori,protocol,revenger,souji,tabi,tameshi,tsukuroi`.
- **Regular driver-counter set — 21 IDs.** Command: `for f in /home/vgpnk/Projects/shokunin/.ufo/state/*.round; do [[ -L "$f" ]] && continue; [[ -f "$f" ]] || continue; name=${f##*/}; printf '%s\n' "${name%.round}"; done | LC_ALL=C sort -u` (count: append `| wc -l`). IDs: `aggregator,audio,chousa,game-dev-2d,game-dev-3d,kagi,kaidoku,kake,kama,kasegi,kengaku,kotoba,kumitate,lore,mado,mori,protocol,revenger,tabi,tameshi,tsukuroi`. Symlink entries are excluded before the regular-file check.
- **Declared-only — 2 IDs.** `comm -23 <(printf '%s\n' "$conf_ids") <(printf '%s\n' "$state_ids")` with the two preceding sets held in `conf_ids` and `state_ids`: `kotodama,souji`.
- **Counter-only — 3 IDs.** `comm -13 <(printf '%s\n' "$conf_ids") <(printf '%s\n' "$state_ids")`: `audio,game-dev-2d,game-dev-3d`.
- **Union — 23 IDs.** `printf '%s\n' "$conf_ids" "$state_ids" | LC_ALL=C sort -u | wc -l` → `23`; the live census also emitted exactly 23 `SURFACE lane.*` rows (`MORI_SHOKUNIN_ROOT=/home/vgpnk/Projects/shokunin bash tools/mori-census.sh | grep -c '^SURFACE lane\.'`).

The commands above were evaluated with `conf_ids=$(grep -oE '^[a-z0-9][a-z0-9-]*\|' /home/vgpnk/Projects/shokunin/shokunin.conf | cut -d'|' -f1 | LC_ALL=C sort -u)` and the state loop shown above assigned to `state_ids`; exact output is retained in `corpus/evidence/roster-r12-20261019T220912Z-live.log`.

## Decision

`tools/mori-census.sh` now uses a non-empty `MORI_ROSTER_LANES` override as-is (`roster_source=env`); otherwise it parses lane IDs from `MORI_FLEET_CONF` (default `$ROOT/shokunin.conf`) as data, never sourcing or evaluating config lines. It takes only regular `*.round` basenames from `MORI_STATE_DIR`, excludes symlinks before checking regular files, and accepts IDs matching `^[a-z0-9][a-z0-9-]{0,47}$`. Invalid IDs are dropped and counted. The roster keeps unique config IDs in file order, then appends unique state-only IDs in C-sorted order. `roster_source` reports `conf+state`, `conf`, `state`, or `builtin`; the historical nine IDs are used only if neither source supplies a valid ID. The aggregate row reports `roster_n`, `conf_n`, `state_n`, `conf_dropped_n`, and `state_dropped_n`.

When both sources are readable and their valid sets differ, `ROSTER_SET_MISMATCH` reports `conf_only=` and `state_only=` with severity `info`; this never changes CLEAN/DRIFT. An unavailable source is not treated as an empty source when comparing sets, so unreadability alone does not create a mismatch. Roster fields are deliberately absent from the r10 volatile list: changes remain visible to `--drift`.

## Limits

This census covers the declared config IDs plus regular state-counter IDs; the driver may launch a lane absent from both sets. Removing a state file can hide a state-only lane again, the residual called out by `PROTOCOL-APPENDIX.md`'s 'Lane universe' row (mutant m10). The implementation cannot infer missing state that neither input contains. Live observations here are counts and lane surface states, not a claim that the inputs are a complete fleet inventory.

## Correction before admission (round 12, critic seat)

At census `4fe9786d…` the parser accepted any `id|…` row anywhere in the conf; a read-only fixture
with `OTHER="shadow|…"` produced `SURFACE lane.shadow`. From `3da5b098…` the parser reads rows only
inside `LANES="…"` assignments (opening `LANES="` or `LANES="$LANES`, closing at the next double
quote — the live conf's `mori|…"` row closes its own block). Selftest case `roster: rows outside
LANES= are not lanes` (77/77); the gating mutant (gate line → `:`) fails 2 cases. The live counts
above are unchanged (20 / 21 / 23): every `id|` row of the live conf sits inside a `LANES` block, so
the whole-file grep in §Measured sets and the census agree today — they would diverge only if
another variable held lane-shaped rows. `resolve_roster()` now spans `tools/mori-census.sh:386-497`.
