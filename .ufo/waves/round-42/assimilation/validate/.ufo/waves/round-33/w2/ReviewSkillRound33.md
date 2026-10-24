# ReviewSkillRound33 — SKILL.md `## Round33` section vs the r33 entry and round-33 §1

Attacker: MoriR33.ReviewSkillRound33 (wave 2). Scope: `SKILL.md:811-823` against
`corpus/knowledge/disk-write-rate-r33.md` (rows 1-14) and `corpus/lessons/round-33.md` §1.
Working tree verified identical to 62db24c for all three files (sha256 match per file).

## Findings

### Major 1 — line 819 cites rows 10 and 11 but drops both of their verdicts

`SKILL.md:819` reads "...a missing discard or flush field... (rows 8, 9, 10, 11 and 14)".
Row 8 supports the missing-field clause, but the cited rows 10 and 11 assert different
verdicts that no rule line carries:

- Row 10 (`disk-write-rate-r33.md:28`): "Leave discarded sectors out of a write rate; if
  they are reported, report them as their own figure."
- Row 11 (`:29`): "Read flush counts from whole-disk lines only and never add them to
  sectors written."

An agent given only the five rules has no instruction telling it that present
discard/flush values must not be folded into sectors written — the rule covers only the
*absent*-field case. A writer summing field 18 (discard sectors) into a write rate would
violate rows 10 and 11 while following SKILL.md literally. Both cited verdicts are
silently dropped from the distilled section.

### Major 2 — line 818 swaps row 5's prohibition and drops row 7's verdict

`SKILL.md:818`: "report io_ticks as the share of time with I/O in progress and the
in-flight value as a momentary queue depth, never as throughput (rows 5, 6 and 7)".

- Row 5 (`:23`) says "Report it as the queue depth at the moment of the read and **never
  subtract two readings of it**". The rule replaces that operative prohibition with
  "never as throughput", which row 5 does not state. An agent that subtracts two
  in-progress readings and calls the result "change in queue depth" (not throughput)
  satisfies SKILL.md and violates row 5. The citation also makes an unsupported claim
  against the row.
- Row 7 (`:25`) is cited but the rule contains nothing about field 11 / write-ticks; its
  verdict "Never present the write-ticks delta divided by elapsed time as a percentage of
  time" appears nowhere in the section. Dangling citation plus dropped verdict.

### Major 3 — line 817 totals a wrong number on a documented stacked-device shape

`SKILL.md:817`: "total a host's writes over whole-disk lines or over partition lines but
never both (row 3)". It follows row 3 (`:21`) faithfully, but the same entry's own
"Host observation" section (`:36-43`) records that on this host `dm-0`, whose only slave
is `nvme0n1p2`, moved by exactly the same field-10 delta as that slave — so a sum over
every whole-disk line counts the root filesystem's writes twice. Rule 817 is the only
aggregation instruction the SKILL gives, and it produces a double count on the very host
the entry documents. The rule needs the stacked-device caveat (flagged as host-observed,
unsourced, FR6 per `:43`); as written it is a known-wrong recipe with no pointer to the
only section that names the failure.

### Minor 1 — line 815's row-8 citation is weak; conversion executability is implicit

`SKILL.md:815` cites "rows 1 and 8" for "convert a sectors-written delta to bytes by
multiplying by 512". Row 1 carries the whole rule (`:19`); row 8's contribution is only
that "sectors written" is field 10 (`:26`). The rule text itself never says which field
is sectors-written, so an agent needs row 8 (or the ABI, S187) to map the rule to a
column — fine, but the parenthetical does not distinguish the roles and the rule is not
standalone executable without it. Cosmetic but worth a note since the five rules are the
agent-facing surface.

## Checks that found no defect

- **Line 816** (two readings; lower new reading ⇒ unavailable; resets at boot /
  reattachment / overflow): follows rows 4, 13 and 14 (`:22,:31,:32`). "Reattachment"
  subsumes row 4's "reattached or reinitialised"; the row-14 cite is via the same
  reset-set mechanism (S181); the rule's "mark that interval unavailable" is the
  conservative extension of rows 4 and 14 and adds no fact.
- **Line 819, other clauses**: "missing line ⇒ unavailable, never zero" is row 9's
  verdict verbatim (`:27`); "iostat zero ⇒ not an idle disk" is row 14 (`:32`).
- **Lines 821-823, correction paragraph**: number and wording checked. Round-32's
  `## Recheck` table (`corpus/lessons/round-32.md:21-54`) has 34 rows; verdict tally by
  `awk ... split($0,a,"|")` = 33 `current`, 1 `unreachable` (S056, `:40`), so "five of
  the 33 `current` rows" is exact. The five ids S058, S117, S128, S149, S137 match
  `round-33.md:58-62` §1 in the same order; §1's correction keeps them `current`-labeled
  in the old table but not current on the population page alone (`round-33.md:49-51`),
  matching SKILL.md's phrasing. The pointer "clause-level recheck ... (Round-32 repair)"
  resolves to `round-33.md:38` heading and the five `Repair*.md` reports exist in
  `.ufo/waves/round-33/w1/` (S058, S117, S128, S137, S149 — verified by `ls`).
- **Preamble line 813**: "detection and report only ... never touch a block device
  setting" mirrors the entry Scope (`:7-9`); "Sources S180-S190" matches `SOURCES.md`
  rows S180-S190 and the entry header (`:3`).

## Residual risk / gaps

- Executability judgment is by reading, not by running an agent; a literal-reader test
  of Majors 1-3 (does the agent mis-handle present discard fields, subtract in-progress
  readings, or sum dm-0?) was not exercised.
- Rows 2 (completed-not-submitted delta) and 12 (one parser for /proc and sysfs
  variants) also have verdicts absent from the five SKILL rules — unchecked whether
  omission is intentional SKILL scoping or the same defect class as Majors 1-2. If the
  section is meant to carry every verdict, this widens the finding; if it is meant to
  carry only rules an operator needs, the row-7/10/11 citations on lines 818-819 are
  still wrong.
- No tools installed or updated; no network fetches performed.
