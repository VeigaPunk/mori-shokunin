# Round 13 — ReviewPromotion (SHONEN seed, author/non-author limits)

Seat: `MoriR13.ReviewPromotion`. Read-only inspection; no edits, no builds/tests/lint, no installs (none needed).

## Findings (by severity)

### F1 — HIGH: working-tree `SHONEN.md` is non-canonical (uncommitted indentation drift)

- `SHONEN.md` (working tree) has all 8 lines indented by 4 spaces. The indent was copied from the indented seed block in the protocol without de-indenting. Markdown renders it as a code block.
- `git status --short -- SHONEN.md` → ` M SHONEN.md`; `git diff --numstat` → `6 6 SHONEN.md` (6 lines in the seed block differ; the two blank lines are unchanged).
- Mtime `2026-10-20 01:07:55 -0300`, after the last commit `1f07f1d` (2026-10-19 19:41:08 -0300). Writer is not identified in this seat's inspection.
- Committed HEAD (`1f07f1d`) `SHONEN.md` is byte-identical to the canonical seed with `<name>` = `mori-shokunin`:
  - Seed source A: `~/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md:453-462` (indented block, de-indented by 4 spaces, `<name>` substituted). Its `git status` in kimi-shokunin is clean.
  - Seed source B: `~/Projects/kimi-shokunin/templates/mint/SHONEN.md:7-14` (`<name>` substituted). `cmp` of B against HEAD = identical.
  - `cmp` of A (de-indented, `<name>` substituted) against HEAD = identical.
- Gate text the file must match: `PROTOCOL.md:446` — "the seed block must diff byte-identical modulo `<name>` = the repo's directory name, and marks are confined to the box character plus one indented evidence line per box".
- **Recommendation:** no content regeneration is needed (the gate text has not changed from HEAD). The working-tree copy must be returned to the committed bytes, which equal the template output. Owner: the lane (sole allowed writer, `PROTOCOL.md:446`). Do not hand-edit; regenerate verbatim from `templates/mint/SHONEN.md` or restore HEAD.
- **Proposed L1 check (not run here):** `cmp SHONEN.md <(git show HEAD:SHONEN.md)`; `diff <(sed -n '7,14p' ~/Projects/kimi-shokunin/templates/mint/SHONEN.md | sed 's/<name>/mori-shokunin/') SHONEN.md`; expect both silent, `git status --short -- SHONEN.md` empty.

### F2 — MEDIUM: author/non-author limit still binds — no `[x]` this round

- `PROTOCOL.md:63-68`: each `[x]` must name a non-author verifier; "a subagent the lane dispatched is still the lane"; `[~]` = asserted by the lane with an evidence pointer; `[x]` without a named non-author verifier counts as `[~]` for the gate.
- Round-13 seats (`MoriR13.*`, including this reviewer) were dispatched by the lane. They are the lane, not non-author verifiers. No `[x]` is admissible.
- `PROTOCOL.md:165-170`: the report must carry a `SHONEN` heading with one line per box. A report that collapses the four boxes (as r5–r11 did, per `.ufo/reports/round-11/mori-goalwave.md:40`) does not satisfy the contract.
- `PROTOCOL.md:446` / `:464-465`: in `SHONEN.md`, marks are the box plus one indented evidence line per box. The working copy carries no evidence lines; that is consistent with the seed, which has none.

### F3 — LOW: residual named blockers that the per-box lines must disclose

- Box 1: SKILL.md has `## Decision table` (`SKILL.md:11`), `## Error patterns` (`:22`), `## Checklist (executable)` (`:51`), `## Gates` (`:58`). It has no sources section; cited sources live in `corpus/SOURCES.md` (SKILL.md:70 points there). Disclose the split.
- Box 3: the r11 audit named "dead-baseline-recipe + inconsistent instructions" (`.ufo/reports/round-11/mori-goalwave.md:32-35`). Round 12 appended an erratum to `corpus/knowledge/drift-pin-r10.md` (LOG.md:680). Whether the recipe is now executable is unverified here.
- Box 4: `PROVINCE.md:9` and `SKILL.md:18` still say "scratch roots". The round-12 correction (`PROVINCE.md:79-81`, LOG.md:677) states `/scratch` is absent and the phrase does not resolve. PROVINCE is therefore not fully self-consistent; the box's "PROVINCE still accurate" claim needs that residual disclosed.

## Recommended per-box lines (for the round-13 report `SHONEN` heading)

These are `[~]` lines, not `[x]`. Use four separate lines, not the collapsed `[ ] · [ ] · [ ] · [ ]` form.

- `- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources` — pointer: `SKILL.md:11`, `:22`, `:51`, `:58`; sources `corpus/SOURCES.md` (SKILL.md:70). Residual: no in-SKILL sources section.
- `- [~] At least one end-to-end domain task executed and logged in LOG.md` — pointer: `LOG.md:643-713` (round-12 census run, census SHA-256 `3da5b098…`, selftest 77/77, mutation battery 12/0/0; `corpus/evidence/roster-r12-20261019T220912Z-mutation.md`). No non-author verifier.
- `- [~] Instructions executable by an agent without oral context` — pointer: `SKILL.md:51` (executable checklist), `LOG.md:675-681` (r12 registry and pointer fixes). Residual: the r11 dead-baseline / inconsistent-instruction debt; re-execution not performed by this seat.
- `- [~] No cross-domain bleed (PROVINCE.md still accurate)` — pointer: `PROVINCE.md:3-16` (domain, refusals), `:46-57` (adjacent table), `:79-81` (corrections). Residual: `PROVINCE.md:9` and `SKILL.md:18` still say "scratch roots" after the correction.

No `[x]` on any line. `[ ]` is used only for an untouched box; none is untouched.

## SHONEN regeneration

- Content regeneration: **not needed** (committed bytes are canonical; gate text unchanged).
- File restore: **needed**. The working-tree indentation drift (F1) must be reverted to the committed/template bytes by the lane. Not performed here (no edits).

## Boundaries

- No file edited outside `.ufo/waves/round-13/build/ReviewPromotion.md`.
- Temporary `/tmp` files created for `cmp` were deleted.
- No builds, tests, lint, or smoke runs.
- No tools installed or upgraded (none needed).
- No credential material or journal `MESSAGE` read.
