# ReviewRegistry — SKILL.md registry review (round 16)

Scope: `SKILL.md` Gates registry (home, verdict map, write scope, pinned values) and the r15 hidden-flag correction. Read-only; no execution, no installs (none needed; tools were `read`, `grep`, `git show`, `git diff`, `sha256sum`).

## Read-time state (changes may be in flight)

- Read at 2026-10-20T08:48Z against HEAD `b83edc6`.
- `git status --porcelain`: only `?? .ufo/waves/round-16/` is untracked. `SKILL.md` and `tools/` are clean vs HEAD (`git diff --quiet HEAD -- SKILL.md tools` passes).
- `SKILL.md` mtime 07:51Z, which predates the round-16 registry creation at 08:47Z. The SkillRegistry seat's r16 edits have **not landed** in the tree at read time.
- `tools/mori-journal-window.py` does not exist (no grep hits anywhere in the repo).

Any finding below marked "in flight" may be resolved by the SkillRegistry seat after this read.

## Findings (by severity)

### F1 — Medium: hidden-flag prose still stale (correction not landed)

- Location: `SKILL.md:134` (r15 regressions row, self-test column). It says `--no-frozen-control` "is selftest-internal and requires the hidden `--selftest-child`".
- Code truth (verified at read time):
  - `tools/mori-round15-regressions.py` has zero hits for `selftest-child` or `no-frozen-control` (`grep -c` = 0).
  - `parse_args` (≈2310-2319) declares only `--census --fixtures --output --frozen --expected --pin-fixtures --case --timeout --selftest`.
  - The argparse refusal receipt `.ufo/waves/round-15/evidence/control-bypass-refused.json` records `"exit": 2` with stderr `unrecognized arguments: --selftest-child --no-frozen-control`.
  - `selftest()` (≈2200-2290) runs the normal gate and asserts the full pinned frozen control, so no bypass exists.
- Verdict: the code correction is complete. The prose is wrong and still describes both flags as live. Wave spec requires "both former flags removed/refused" in SKILL prose; **not met at read time.**
- Suggested replacement for the self-test cell: "`--selftest` runs the full pinned frozen control; the r15 CLI has no bypass (`--selftest-child`/`--no-frozen-control` removed; argparse exits 2, receipt `.ufo/waves/round-15/evidence/control-bypass-refused.json`)."

### F2 — Medium: r14 row omits a live control-bypass flag (same defect class r15 removed)

- `tools/mori-round14-regressions.py:2745` registers `--no-frozen-control` (`store_true`), with help text "skip the red control (green-only measurement)".
- `prepare()` (≈2209) skips loading the frozen red control when set. Line 2577 then reports `frozen_control: skipped`.
- The `SKILL.md:133` r14 row mentions neither the flag nor a `skipped` state in its verdict map (`0 clean · 1 failed · 2 could-not-evaluate`).
- Not traced: whether `skipped` maps to exit 0. The r15 repair only removed the bypass from r15, so this remains live in r14.
- Constraint: `.ufo/waves/round-15/expected.json` pins `r14_helper_sha256` `533218a5…`, which matches the current helper bytes. Any r14 edit (including removing the flag) requires an expected-table re-pin, per the r15 row text. Documenting the flag in SKILL does not require a re-pin.
- Recommendation: either document the flag and its `skipped` semantics in the r14 row, or route removal to the harness owner with re-pin.

### F3 — Medium (in flight): r16 registration absent

- Wave spec requires: register the new window tool as a `probe` (per PROTOCOL §Gate standard, "a tool that cannot fail is a probe, and is registered as one"), and add r16 regression/context gate rows with the full eight fields (name, kind, entry, verdict map, self-test, pinned values, write scope, owner).
- Neither exists at read time. No probe row, no r16 gate row, no statement of "no production census change", no "exact retained anchor precondition" paragraph.
- Blocks the SkillRegistry assignment; cannot be reviewed for content until it lands.

### F4 — Low: census row self-test cites a historical tally against an unlabeled live SHA

- `SKILL.md:129`: `--selftest (104/104 at 8d22d18, census SHA 0e41cb83…)`.
- `0e41cb83…` is correct for `8d22d18` and `0fa5e0d`. The live tracked census at HEAD (`tools/mori-census.sh`) hashes to `f1f8d1b6…` (`git show HEAD:… | sha256sum`).
- The r14/r15 census-affecting work is not reflected in this row. The "at 8d22d18" label is accurate, so this is a stale-identity risk, not a false claim. No current-bytes tally exists in the registry.
- Recommendation: add the live SHA and state that the tally is pre-r14, or re-measure (L1's job, not mine).

### F5 — Low: r15 row omits two parser options

- `parse_args` declares `--case` (≈2316) and `--timeout` (≈2318) (range 1..3600 per `main`). The `SKILL.md:134` row lists neither. Full-fields standard applies to gate rows generally.

### F6 — Low: stale or unresolved citations

- `SKILL.md:265` cites `tsukuroi-shokunin/PROVINCE.md:19` for the quoted line "never restarts services. Detection and report; the operator remediates." The quote is at **line 28**; line 19 is a table separator.
- Both PROVINCE paths are relative to the parent `/home/vgpnk/Projects/shokunin/`, not the mori repo root; they do not resolve from the repo. The kama citation (`PROVINCE.md:45-47`) does match its quoted text.
- `SKILL.md:121-125` cites `PROTOCOL.md §Gate standard fields` without a path. The file is `/home/vgpnk/Projects/shokunin/PROTOCOL.md` (outside this repo); the heading is `## Gate standard` (line 375). The "fields" list lives under its **Registry** bullet.

## Passes (verified)

- Registry columns match PROTOCOL §Gate standard Registry row fields exactly: name, gate|probe, entry, verdict map, self-test, pinned-value path, write scope, owner.
- Verdict maps: census, drift pin, r13, r14, r15 and silence oracle all use `0 clean / 1 failed / 2 could-not-evaluate`, matching PROTOCOL's required 0/1 and the declared-code rule.
- Pins: `expected.json` `gate_sha256` `6a55c33c…` equals live `tools/mori-round15-regressions.py`; `frozen_sha256` and `pinned_frozen_sha256` are `0e41cb83…`, matching the in-script `PINNED_FROZEN_SHA256`. `PINNED_BASE_COMMIT` is `0fa5e0d…`.
- Write scope (r15): `guard_output` (≈1380-1435) refuses output that covers or equals fixtures, frozen dir, expected table, repo root, `tools/`, `.git/`, or `corpus/`, matching the row text.
- Drift pin: "old red pin remains, no re-pin" is consistent with the spec and the r15 text.
- Selftest arms exit-code and id assertions are present in `selftest()` (≈2246-2290).

## Verification gaps

- Not traced: r14 exit-code path when `--no-frozen-control` reports `skipped` (F2).
- Not re-measured: census self-test tally against live `f1f8d1b6…` (F4).
- Not checked: `silence oracle` row claim "28 cases" (a rough grep gave a different count; I did not confirm the true number).
- Not reviewed: any r16 SKILL content (absent, F3).
- Not run: no gate or selftest was executed, per the no-execution rule.

## Read-time summary

Hidden-flag correction: **code side done, prose side not landed** (F1). r16 registration: **not landed** (F3). Registry home/verdict/write-scope columns otherwise conform to PROTOCOL; remaining issues are accuracy and citation gaps (F2, F4–F6).
