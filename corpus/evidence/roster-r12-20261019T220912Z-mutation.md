# Mutation receipt — roster derivation (claim 3), final census sha 4fe9786d…; seat R12MutationB (lane L2), committed by the lane L1; utc of commit-time copy 2026-10-19T22:28:14Z

# Mutant table — final census bytes `4fe9786d9c0c268f080a8d4b4e89711e02791103bd31e4b76fc6e064684c8b64`

All 12 mutants re-run on fresh private copies of the final bytes. **Baseline (unmutated copy):** `bash $S/green/tools/mori-census.sh --selftest` → rc 0, `PASS (76 cases, 76 passed, 0 failed)`. Live: `MORI_SHOKUNIN_ROOT=/home/vgpnk/Projects/shokunin bash tools/mori-census.sh` → 23 `^SURFACE lane\.` rows, `roster_source=conf+state roster_n=23 conf_n=20 state_n=21`.

| mutant | diff summary | selftest result | killed? |
|---|---|---|---|
| M01 sha `2a8ac994…` | conf parse loop replaced by `. "$FLEET_CONF" \|\| true` | rc 1, 70/76 — `parse conf order…`, `config was not sourced (canary absent)`, both new cases, mismatch, shapes | **killed** |
| M02 sha `61c05569…` | `for sf in "$STATE_DIR"/*.round` → `for sf in;` (drop state set) | rc 1, 72/76 — parse, `unreadable conf is not treated as an empty set`, mismatch, shapes | **killed** |
| M03 sha `96b376ee…` | conf loop body → `continue` (drop conf set) | rc 1, 72/76 — parse, `conf-only set retained…`, mismatch, shapes | **killed** |
| M04 sha `2bbe3b94…` | conf regex `[^\|]+`; both `[a-z0-9-]{0,47}` validators → `if false` | rc 1, 74/76 — parse, shapes (`dropped_n`) | **killed** |
| M05 sha `0c88f27f…` | removed `[ -L "$sf" ] && continue` (follow symlinked `*.round`) | rc 1, 74/76 — shapes counts, `state symlink excluded from roster` | **killed** |
| M06 sha `d73f8cd3…` | added `[[ $line == *'"' ]] && continue` (skip quote-terminated row) | rc 1, 75/76 — parse (`conf_n=3`, `lane.beta`) | **killed** |
| M07 sha `09679af0…` | `ROSTER_SET_MISMATCH info` → `warn` | rc 1, 74/76 — both mismatch cases exit 1, `severity=warn`, DRIFT | **killed** |
| M08 sha `16755364…` | env-override branch → `if false` | rc 1, 75/76 — `MORI_ROSTER_LANES override wins` | **killed** |
| M09 sha `a77b88c7…` | union branch also requires `state_ids > 0` (builtin despite readable conf) | rc 1, 75/76 — `conf-only set retained when state set is empty` | **killed** |
| M10 sha `d20ccae4…` | state sort → `sort -r` | rc 1, 75/76 — mismatch (`state_only=delta,kagi,zeta` order) | **killed** |
| M11 sha `70794883…` | removed `conf_seen` skip in union (duplicates) | rc 1, 74/76 — parse, shapes (`roster_n`) | **killed** |
| M12 sha `0f1ee85f…` | `[ -r "$FLEET_CONF" ] \|\| conf_available=1` (unreadable conf ⇒ false mismatch) | rc 1, 75/76 — `unreadable conf does not manufacture mismatch` | **killed** |

**Survivors: none — 12/12 killed, 0 inconclusive.** (On the earlier `d09ae1` bytes M09/M12 survived; the two cases added in `4fe9786d` close exactly those gaps and were re-verified here.)

**Exact commands** (LANE never written; no `cd`):
1. `S=$(mktemp -d /tmp/mori-r12-final.XXXXXX); cp -a /home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/mori-shokunin "$S/green"` — then `bash "$S/green/tools/mori-census.sh" --selftest` → rc 0, 76/76.
2. `for n in 01 … 12; do cp -a "$S/green" "$S/m$n"; done`; one `edit` per mutant (anchors above); `sha256sum "$S/m$n/tools/mori-census.sh"`.
3. `bash "$S/m$n/tools/mori-census.sh" --selftest > "$S/m$n.out" 2>&1` per mutant; rc and `^FAIL` lines recorded above.
4. `for n in …; do cp "$S/green/tools/mori-census.sh" "$S/m$n/tools/mori-census.sh"; done; sha256sum "$S"/m*/tools/mori-census.sh` → all twelve read back `4fe9786d…`.
5. LANE after probes: `4fe9786d…` (unchanged). `rm -rf "$S"` → scratch removed.

**Restoration evidence:** full pre-restore mutant hashes are in the table; every copy restored to `4fe9786d…`, LANE hash identical before/after, scratch deleted. No open blockers.
---
L1 addendum (after the critic seat's phase-2 finding): the parser at `4fe9786d…` read `id|…` rows
anywhere in the conf, so a row inside another variable (`OTHER="shadow|…"`) became a lane. The
final census `3da5b098…` reads rows only inside `LANES="…"` assignments, with a new selftest case
(`roster: rows outside LANES= are not lanes`; selftest 77/77). Mutant M13 — gating line replaced by
`:` in a /dev/shm scratch copy — **killed**: `FAIL roster: parse conf order…`, `FAIL roster: rows
outside LANES= are not lanes`, `MORI_CENSUS_SELFTEST: FAIL (77 cases, 75 passed, 2 failed)`.
M01–M12 above ran on `4fe9786d…`; the gating change touches only the conf loop (M01/M03/M04/M06
territory) and was not re-run for those twelve.
