# Round 25, wave 1 — QUALITY criteria 76 and 77 (draft text)

Seat: MoriR25.QualityCriteriaDraft. Scope: draft text only. This seat wrote no product file;
`corpus/QUALITY.md` is the integration owner's (L1 MoriR25) to edit.

Source of both criteria: routed defect D1 and D2 of
`corpus/lessons/round-24-verifier-spotcheck.md` (the round-24 non-author spot-check note),
read at the entering lane tip `28b79d3d1b76824f0c825aabe6cb6c5dc49961bf`.

## Draft criteria text (paste-ready, in the numbering style of `corpus/QUALITY.md:316-336`)

### Heading to add under `corpus/QUALITY.md`

```markdown
## Criteria added round 25 — round-24 routed defects as admission bars

Each line names the routed defect it carries (`corpus/lessons/round-24-verifier-spotcheck.md:135-146`).
```

### 76 (from D1)

```markdown
76. A self-test evidence file names the measured full revision and carries the full stdout
    and the exit code of the shipping tool. The file's first line names the full 40-hex commit
    the run was measured against; the exit code recorded is the exit code of that same run; the
    remaining bytes are the complete stdout of the tool's self-test invocation, not an excerpt, a
    reformatted tally or a remembered output. The evidence binds the tool it shipped with: the
    shipping tool's committed bytes and its fixture tree are identical at the named revision and
    at the revision that carries the evidence file. An evidence file that names no revision, or
    whose output lacks a line the shipping tool prints at that revision, is stale evidence and
    reads red, not green: a tally is never a pass because its number looks right. Self-test green
    is capability, not a measurement; the revision is what makes the measurement comparable.
    ← lessons/round-24-verifier-spotcheck.md:137.
```

Anchor behind it (verbatim from the note): "**D1 — stale gate evidence.**
`.ufo/waves/round-24/evidence/c2-selftest-after.txt` names no revision and predates the tool it
shipped with: no `MATCHER` line, committed at `89849a7`. Commit future selftest outputs with the
measured revision and the full stdout (§Gate standard, "a verdict names the revision")."

Measured facts this criterion binds (read-only, lane tip `28b79d3d`):

- `git cat-file -p 28b79d3d:.ufo/waves/round-24/evidence/c2-selftest-after.txt` → one line,
  `MORI_PRESSURE_SELFTEST: PASS 12/12`, and nothing else: no revision line, no exit code, no
  `MATCHER` line. That is the D1 red, present at the entering tip.
- Governing clause: fleet `PROTOCOL.md:393-394` (§Gate standard, "Two evidences") — "A verdict names
  the revision it was measured against: a gate grades the tree it runs on, so a run over a moving
  worktree is not comparable to one over the cited commit." `PROTOCOL.md:375` starts §Gate standard.
- Precedent in this file: criterion 31 (`corpus/QUALITY.md:73`) already requires a self-test tally
  to name the revision and to be measured on the delivered gate bytes; criterion 76 is its
  evidence-file form, routed as a defect rather than a lesson.

### 77 (from D2)

```markdown
77. A correction sweeps every mention in place. When the lane corrects a stated fact, every
    place that states it — body prose, decision-table rows, sibling files — carries the corrected
    wording at the commit that carries the correction; the superseded wording is removed, not
    shadowed. A "this section wins" banner, a corrections section placed above the body, or a
    general disclaimer is not a fix: a contradicted line left standing is a defect, whether or not
    a correction section exists. The sweep is over whitespace-folded text, so a phrase split
    across a line break is still a match, and a statement the critic named explicitly gets its
    own named correction row (a K-row for K4) instead of being left to a section-wide
    precedence claim. Fix the body lines in place, with a correction note, and stop relying on a
    precedence banner.
    ← lessons/round-24-verifier-spotcheck.md:138-143.
```

Anchor behind it (verbatim from the note): "**D2 — correction sweep incomplete in the knowledge
entry** (§Evidence standard, "Corrections sweep every mention"). At `4f05dd5a`, three lines still
say what wave-2 CriticKnowledgeOverclaim corrected: line 94–95 … line 170 … line 171 …
The report says all six statements were corrected before the report. Fix the body lines in place,
with a correction note, and stop relying on a "this section wins" banner."

Measured facts this criterion binds (read-only, lane tip `28b79d3d`):

- `git show 28b79d3d:corpus/knowledge/system-pressure-r24.md` still carries all three superseded
  statements: "refreshed" / "on each read" split across lines 94–95 (a per-line grep misses it;
  a whitespace-folded match does not), "a shorter spike between two reads can be invisible" on
  line 170, and "`null` means *undefined*" on line 171.
- The same file's corrections section (heading `## Corrections after wave-2 falsification
  (round 24, before closure)`, line 8) carries rows for K3, K5, K6, P2, P3, P4, H1 and Citations;
  it carries no `(K4)` row, and line 11 reads "Where this section and a later line disagree, this
  section wins." — the banner D2 rejects.
- Governing clause: fleet `PROTOCOL.md:363-365` (§Evidence standard) — "**Corrections sweep every
  mention.** Before a round's commit, grep every file the lane touches (`corpus/README.md`,
  `SKILL.md`, `knowledge/`) for the superseded claim — a corrected fact left standing in a sibling
  file is still a defect."

## Why these two and not D3/D4

D3 (`corpus/lessons/round-24-verifier-spotcheck.md:144`, lesson count drift) and D4 (`:145`,
`tools/__pycache__/` hygiene) are lesson-count and hygiene repairs, not admission bars about
evidence binding or correction sweeps; the assignment scopes 76 and 77 to D1 and D2, and criteria
64–68 already carry the settlement/disposition bars those two would otherwise resemble.

## Bounds observed by this seat

- Wrote only this file: `.ufo/waves/round-25/w1/QualityCriteriaDraft.md`. No product file, no
  `corpus/QUALITY.md` edit, no tool, no commit, no jj command at the fleet root, no lane git
  mutation (all git use was `cat-file -p` / `show` / `log` on committed objects).
- No tool was installed or upgraded for this seat: the task was text drafting over files already
  in the lane and the fleet `PROTOCOL.md`, so no install was warranted.
