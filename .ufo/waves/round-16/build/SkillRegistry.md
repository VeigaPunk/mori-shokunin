# Round 16 — SkillRegistry (SKILL.md) report

Seat: `MoriR16.SkillRegistry` (scribe). Scope: `/home/vgpnk/Projects/shokunin/mori-shokunin/SKILL.md` only, plus this report.
Commit: none. Builds, tests, gates, and smoke runs: none executed (contract). Tools installed or updated: none.

## Edited surface (SKILL.md, 50 insertions, 1 deletion vs HEAD `b83edc6`)

1. **Stale r15 hidden-flag prose corrected** (Gates table, `r15 regressions` row, self-test cell). The prior text said `--no-frozen-control` is selftest-internal and requires a hidden `--selftest-child`. Measured in source: `tools/mori-round15-regressions.py` contains neither string (`grep -c` = 0); its `parse_args` (around lines 2308-2320) defines only `--census --fixtures --output --frozen --expected --pin-fixtures --case --timeout --selftest`. `--no-frozen-control` exists only in `tools/mori-round14-regressions.py:2745`, a different tool. The row now states both former flags are removed, that unknown arguments fail argparse with rc2, and that `--selftest` refuses `--output`/`--pin-fixtures` with rc2 (verified against `main()` in the r15 source).
2. **Registry rows added** (full fields: name | kind | entry | verdict map | self-test | pinned values | write scope | owner):
   - `r16 regressions` (gate): `tools/mori-round16-regressions.py --tool … --fixtures … --output <dir>`, `--expected`, `--pin-fixtures`; rc 0/1/2 per spec (1 includes `capability_absent`); pinned digest table for every pack and the probe; write scope `<dir>` only.
   - `r16 context check` (gate): `tools/mori-round16-context-check.py --spec PATH`; rc0 `CONTEXT_OK` / rc1 `CONTEXT_MISSING`; explicitly a static text check, not runtime prevention.
   - `journal window (r16)` (**probe**, not a gate): `tools/mori-journal-window.py --anchor … --scope user|system [--journalctl] [--timeout] [--max-bytes]`; rc0 `MORI_JOURNAL_WINDOW_OK`; rc2 `MORI_JOURNAL_WINDOW_UNAVAILABLE reason=<stable>` or `MORI_JOURNAL_WINDOW_SETUP`; no severity, DRIFT, or victim count; writes nothing.
   - No predicted selftest tallies are written. Each self-test cell says the tally is measured at L1 integration.
3. **Decision-table row** added for the window probe (after the "Did something get killed?" row): surface, never-list, expected output.
4. **New section** `## Window probe (r16) — exact retained anchor, no census change` (before "Boundaries"): no production census change, the exact-anchor precondition, continuity and unavailable rules, and the claims it does not make (FR11 remains open; `PROVINCE.md:51`).
5. **Regression-gate paragraph** `Regression gate and probe (r16)` after the r15 paragraph.
6. **Secret-exclusions paragraph**: the window probe's query excludes `MESSAGE` and its stdout never echoes a raw cursor or record text.

## Exact anchor precondition (as written in SKILL.md)

- The caller supplies an anchor file: `schema` = `mori-journal-anchor-v1`, `scope` = `user|system`, `boot_id` = 32 lowercase hex, `cursor` = opaque printable scalar ≤4096 chars with no control characters.
- The probe only reads the anchor. It never creates, rewrites, or advances it, and it writes no cursor state.
- Success requires the first parsed record to carry exactly the anchor cursor and boot. That record is dropped. Every later record must be a same-boot object with a unique valid scalar cursor.
- Missing or vacuumed anchor, mismatched cursor, foreign boot, duplicate or malformed cursor, nonzero rc, stderr, timeout, or overflow: `rc2 MORI_JOURNAL_WINDOW_UNAVAILABLE`. Unavailable is never zero.

## No production census change

`tools/mori-census.sh` is not modified by this seat and is not described as calling the probe. The probe adds no `SURFACE` or `FINDING` row and changes no alarm, drift verdict, or r15 positive token. The r10 drift pin remains red and is not re-pinned.

## Findings for L1 (not verified by this seat)

- At the time this report was written, `tools/mori-journal-window.py`, `tools/mori-round16-regressions.py`, and `tools/mori-round16-context-check.py` were **absent** (`test -e`). The registry rows are therefore registrations of planned entry points. L1 must confirm presence and digests at integration, and must confirm that the flag set and finding ids match the registered text (`--cursor=<anchor>`, the four-field output list, `--journalctl` override, `--max-bytes`, `--timeout`).
- The context-check gate's setup/usage return code is not fixed by the r16 spec. The row says so and defers confirmation to L1.
- The probe row's selftest tally is intentionally absent. L1 records the measured tally once after integration.
- The r14 `--no-frozen-control` flag is untouched (different tool).

## Out of scope / not changed

- `corpus/` (owned by Registry/Knowledge lanes), `tools/*`, `PROVINCE.md`, `LOG.md`, `SCORECARD.md`: not written.
- Pre-existing stale census-row figures (for example `104/104 at 8d22d18`) were observed but not reviewed or changed.

## Checks left for L1 (main agent)

- `git diff -- SKILL.md` review against this report.
- Gate presence checks listed above, then the single post-integration selftest and gate runs, which fill the tallies.
