# CriticC2Design — round 29, wave 1: attack on claim C2 before data

Seat: MoriR29.CriticC2Design (critic, leaf). Written 2026-10-22, about 20:00Z, before any round-29 case file, C2
counter or tool run exists in the lane (the new case path is absent at `7118f320`; `w1/` held only `swarm-registry.json`).

Blindness of this report: it holds no tool source, no tool output and no expected value for any concrete input. It
names input shapes and contract lines only. It does contain design analysis, and the C2 statement says the writers
read no critic report (`contract.md:56-57`); see F3 for why this report's location is itself a finding.

## Ranked findings

### F1 (critical) — the A2-07 field map reverts an admitted round-28 hardening and admits pins that do not decide A2-07

- Counterexample: an A2-07 case where an earlier invocation sent real signals and the current invocation is dry-run,
  with an active earlyoom. A tool that lets the current dry-run flag zero every invocation's sends (the exact breach
  A2-07 forbids) gives the same `earlyoom.actions.sigterm`, the same `earlyoom.dryrun_send_lines` and the same verdict
  as a correct tool, because for an active earlyoom the earlier-invocation count "is reported but does not change the
  verdict" (`round-26/contract.md:178`). The only output that differs is `earlyoom.earlier_invocation_send_lines`,
  and the round-29 map excludes it for A2-07 (`round-29/contract.md:59-60`). All 12 A2-07 cases can satisfy the
  required-field rule and every one can be blind to that breach.
- Evidence: the rule text says dry-run is applied "per earlier invocation (split at each version line), so one dry-run
  invocation no longer zeroes the real sends of another" (`round-26/contract.md:180-181`). Round 28 adopted, before
  data, "A2-07's required pinned field is `earlyoom.earlier_invocation_send_lines` with an integer value above 0
  (CriticC2Design F1: `actions.sigterm` does not decide A2-07)" (`round-28/contract.md:94-95`), and the round-28
  counter enforces the integer above 0 (`round-28/count-c2.sh:257-259,266,368-372`). The round-29 contract drops that
  field and drops the value bound, and gives no reason. `earlyoom.dryrun_send_lines` decides A2-04
  (`round-27/contract.md:52`), not A2-07 (`:55`): a case pinning only it is an A2-04 case tagged A2-07.
- Also: no value bound, so `earlyoom.actions.sigterm` pinned to 0 (every invocation dry-run, which brief CaseA207d
  asks for as a control, `wave1-spec.json:23-27`) counts as a decisive pin.
- Axes: operability (the counted value), discernment (a prior admitted fix silently undone: duplicate authority
  between `round-28/contract.md:94-95` and `round-29/contract.md:59-60`).
- Smallest correction: see amendment text M1 below. A2-07's required set becomes `earlyoom.earlier_invocation_send_lines`,
  `earlyoom.actions.sigterm`, `earlyoom.actions.sigkill`, each with an integer value above 0, pinned in a case whose
  journal holds at least two version lines and at least one `dryrun mode enabled` line; plus at least 2 A2-07 cases
  by at least 2 authors that pin `earlyoom.earlier_invocation_send_lines` above 0. Controls may stay in the file;
  they just do not count toward the floor.

### F2 (critical) — nothing links the frozen file to the writers' reports: selection, edits and author forgery are free

- Counterexample: the L1 (not blind: it owns the tool) assembles 24 written cases, keeps the 12 to 18 it expects to
  pass, lightly "fixes" a few expected values, and writes `author` keys itself. The counter (per the BuildCountC2 brief,
  `wave1-spec.json` item at :53-57) checks only that each rule has at least 3 distinct `author` strings, at least 6
  cases and at least 12 total. Every one of these checks passes. Nothing checks that an `author` value is a dispatched
  seat, that the seat's report exists, or that the case bytes equal what the seat wrote.
- Evidence: the statement says "assembled from cases written by eight blind seats (four per rule ...)"
  (`round-29/contract.md:55-56`), but the counted floors are 3 authors per rule and 6 cases per rule
  (`:58-59`). With 4 writers at 3 cases each (`wave1-spec.json` items at :8-47, "Write 3 cases"), 24 cases are
  nominal; the floors let the L1 omit up to 12 of them (half) and still print `C2=met`. The round-28 counter has no
  `author` check at all (`round-28/count-c2.sh:308-347`), so the new check is a string count only.
- Id clashes: all four A2-07 writers are told to use `r29-a2-07-<slug>` and all four A2-10 writers `r29-a2-10-<slug>`
  (`wave1-spec.json` items at :8-47). Independent slugs such as one naming "dry-run then real" can collide between
  CaseA207a and CaseA207c [INFERENCE]. A duplicate id is a schema error in the counter (`round-28/count-c2.sh:317-318`),
  so the L1 must rename before the freeze, and the contract has no rule for how; any rename is an unrecorded edit.
- Same input twice: distinctness is checked per rule only (`round-28/count-c2.sh:360`), never across rules and never
  against the two older files, although every brief says "not copies of cases.json or cases-a2.json".
- Axes: operability (the counted value can be met by a curated file), independence/provenance.
- Smallest correction (M2 below): the counter recomputes the case list from the committed writer reports and requires
  canonical-JSON equality with the file. That one mechanism closes selection, edits, author forgery and makes the
  id-clash rule mechanical.

### F3 (high) — blindness is asserted, not counted; the round-28 M6 fix is not the one being applied

- Counterexample 1 (this report): round 28's leak was a writer reading `w1/CriticC2Design.md` while it was being
  written (`corpus/lessons/round-28.md:143-146`). Round 29 writes this report to the same path in the same directory
  while the eight writers run (`wave1-spec.json:148`, `.ufo/waves/round-29/w1/`). The stated M6 fix — critic reports
  "written outside the writers' readable paths until the freeze" (`round-28.md:145-146`) — is not applied; the wave
  layout repeats the leak path and relies on brief wording.
- Counterexample 2 (tool output by proxy): every writer may read `cases-a2.json` for "schema and journal line shapes
  only" (`wave1-spec.json` items at :8-47). That file passes the tool at 30/30 by claim (`round-29/contract.md:62`),
  so its `expect` blocks are tool-confirmed answers. It holds 3 A2-07 and 3 A2-10 cases, all with an active earlyoom
  (my input-shape count, below), and two of its ids name the exact orders that briefs CaseA207a and CaseA207b assign:
  `a2-07-earlier-real-then-current-dryrun` (`cases-a2.json:795`) and `a2-07-earlier-dryrun-then-current-real`
  (`:856`). A writer who reads that file's expect blocks agrees with the tool by construction; a files-opened list that
  names `cases-a2.json` is allowed and cannot show which parts were read.
- Counterexample 3 (the check cannot see the leak): BuildBlindCheck's check reads committed reports at `<lane-rev>`
  (`wave1-spec.json` item at :58-62). A writer that reads a sibling's uncommitted report leaves nothing in committed
  bytes; part (b) only checks the writer's own self-reported list. And the check is routed hygiene, "never a counted
  claim" (`round-29/contract.md:90-93`): C2 can print `met` with `blind_violations` above 0.
- Axes: independence (C2's substance by the wave context), false provenance.
- Smallest correction (M3 below): make `blind_violations=0` a C2 counter condition; require each writer's files-opened
  list to say whether it read any `expect` block of `cases-a2.json`, and count a "yes" as a violation for that rule;
  reject any new case whose canonical inputs equal an older case's inputs; for later rounds, critic reports of a blind
  wave go to a directory the writers' briefs never name, until the freeze. If the operator's harness keeps per-seat
  transcripts, a non-writer seat counts forbidden-path reads per writer (counts only, no session fields)
  [INFERENCE: I did not open any transcript].

Input-shape count (inputs only, no expect values): `cases-a2.json` 30 cases, 3 per rule, no `author` key; its A2-07
cases have 2, 2, 3 version lines and 1 dryrun line each; its A2-10 cases 1, 1, 2 non-numeric or missing stamps.

### F4 (high) — required-field pins can be vacuous for A2-10 (and for A2-07 controls)

- Counterexample: brief CaseA210a covers "an active earlyoom whose scope is unbounded" (`wave1-spec.json:28-32`).
  An unbounded invocation already makes `scope_complete` false by A2-05 (`round-26/contract.md:173-174`), so a
  `scope_complete` false pin in that dimension is satisfied by a tool that ignores A2-10's scope effect entirely.
  The same holds for non-active states whose start stamp is 0 [INFERENCE]. Only bounded-scope, active cases make the
  pin attributable to A2-10: brief CaseA210b and the bounded half of CaseA210d. If CaseA210b dies, A2-10's scope
  effect may rest on one or two cases from one author.
- Count side: "left uncounted" (`round-27/contract.md:58`) applies to every count, but the A2-10 set lists only
  `actions.sigterm` and `earlier_invocation_send_lines` (`round-29/contract.md:61`). A stamp-less SIGKILL or escalation
  record that a tool wrongly counts is caught only if some case happens to pin `sigkill` or `escalations`. A pin of
  `earlier_invocation_send_lines` 0 in a single-invocation journal tests nothing.
- Untested interaction: no brief asks for stamp-less non-send records (a stamp-less version line or `dryrun mode
  enabled` line). Whether such a line splits an invocation or sets dry-run decides A2-07 and A2-10 together, and each
  case carries exactly one rule tag, so no writer owns the shape.
- Axes: operability, coverage of the routed breach.
- Smallest correction (M1, A2-10 part): at least 3 A2-10 cases by at least 2 authors with an active earlyoom, a
  numeric non-zero `ActiveEnterTimestampMonotonic`, at least one stamped version line at or after it and at least one
  record without a numeric stamp, pinning `earlyoom.scope_complete`; at least 2 A2-10 cases with a stamp-less send line
  and a stamped in-scope send line that pin `actions.sigterm`, `actions.sigkill` or `actions.escalations`. All checked
  from inputs only; the counter needs no tool knowledge.

### F5 (medium-high) — the judge reads less than the writers, and tool changes are not tied to rulings

- Counterexample: a case pins a verdict and exit whose deciding line is the base verdict rule
  (`round-26/contract.md:96-104`) or the scope definition (`:78-79,92-93`). Writers may read the whole round-26 spec
  (`wave1-spec.json` items at :8-47). The judge reads "only the rule text" (`round-29/contract.md:75-76`), which this
  contract defines as `round-27/contract.md:47-58` and `round-26/contract.md:152-200` (`:53`; the round-28 judge
  text names the same two ranges, `round-28/contract.md:106-108`). A judge without the base spec can rule `tool
  error` where the base spec makes the case wrong; the L1 then changes the tool to match a wrong case, all files pass,
  and the tool is now wrong with `C2=met`. The reverse direction (base-spec value ruled `unclear text`) is a miss and
  is not a narrowing.
- Judge shopping: "a non-author judge seat" is not named before the run; nothing makes the first ruling binding.
- Tool edits: "only if a judged tool error requires it" is prose (`round-29/contract.md:16-17`); nothing checks that
  each post-freeze tool commit follows a ruling.
- The guard "may not turn any `KILLER_ACTED` of either older file into another verdict" (`:78-79`) adds nothing: every
  older case pins a verdict (schema check `round-28/count-c2.sh:336-339`), so PASS 32/32 and 30/30 already imply it.
- Smallest correction (M4 below).

### F6 (medium) — a passing tool change can still break an A2 rule: the bound is only the pinned (input, field) pairs

- Counterexample: no frozen case anywhere pins an A2-07 shape with a non-active earlyoom, which is the one state where
  A2-06 makes the verdict depend on earlier real sends (`round-26/contract.md:176-177`); the older A2-07 cases are all
  active (F3 count) and no round-29 A2-07 brief names a state (`wave1-spec.json:8-27`). A tool fix made for an A2-10
  ruling that zeroes earlier sends for an inactive earlyoom passes all three files.
- Evidence of the bound: older rules A2-01..A2-06, A2-08, A2-09 hold 3 cases each (F3 count) and the round-28 floor
  was 2 cases and 1 decisive pin per rule (`round-28/count-c2.sh:47-48,430-434`). Unpinned output fields and uncovered
  shapes are free. The round-26 detector inputs (`.ufo/waves/round-26/evidence/a2-detectors/`, 16 entries) are
  uncounted.
- Smallest correction (M5 below): a differential receipt, so any output change outside the judged rulings is visible
  and is a miss.

### F7 (medium) — two round-28 safeguards are missing: the LOG.md freeze hash and a frozen counter

- Round 28: "the freeze hash is written to `LOG.md` in the freeze commit's own batch and the first tool run is later"
  (`round-28/contract.md:39-40`). Round 29 says only "committed before the L1 runs the tool on it"
  (`round-29/contract.md:57`); the counter cannot see run order (`round-28/count-c2.sh:30-32`).
- The counter is "committed before the case file" (`round-29/contract.md:71`) but nothing forbids editing it after the
  first tool run. An edit that lowers the A2-07 set or the floors narrows C2 after data.
- Smallest correction: restore the LOG.md clause; the counter prints the number of blob versions of
  `.ufo/waves/round-29/count-c2.sh` up to `<lane-rev>` and requires 1, with its first commit a strict ancestor of the
  freeze commit.

### F8 (medium) — the floors are sized for one death per rule, and the statement and counter disagree

| Deaths | Same rule | Split across rules |
|---|---|---|
| 1 | 9 cases, 3 authors: met | — |
| 2 | 6 cases, 2 authors: unmet (author floor) | 18 cases, 3 authors each: met |

Arithmetic from 4 writers × 3 cases per rule (`wave1-spec.json` items at :8-47) and the floors at
`round-29/contract.md:58-59`. The 12-total and 6-per-rule floors bind only if writers under-deliver; otherwise their
only effect is the L1 discretion in F2. A dead writer removes a whole input dimension (each brief owns one), and no
floor notices. The statement's "eight blind seats" (`:55`) is false after one death while the counter prints `met`.
- Smallest correction: the statement reads "every case delivered by the dispatched writers, at least 3 authors per
  rule"; the lesson lists each dead writer's dimension as uncovered. Floors stay; M2 removes the discretion.

### F9 (medium) — routed defect 2 is not checkable: no predicate ties a case to the routed breach shapes

- The claim exists to give frozen cases to "A2-07/A2-10 breach shapes found by wave-1 ReviewA2SpecVsTool"
  (`round-28-verifier-spotcheck.md:126-127`). Neither contract nor counter names those shapes; I may not open that
  report, so I cannot say whether the briefs cover them. Correction: a seat that may read it states each shape as an
  input predicate (no expected value) before the freeze; at least one case per predicate, else a miss.

### F10 (low-medium) — false provenance risk in the `sources` key

- The cases are said to "rest on SOURCES rows opened this round (S153 onward)" (`round-29/contract.md:18-20`), but
  writers may read neither those rows nor the scribes' reports (`wave1-spec.json:8-47`); they rest on their own
  fetches. Correction: cite per-author URLs and sha256 values; an S153+ row only where its sha256 matches.

## Amendment text (ready to paste; every item makes C2 harder to meet, none narrows it)

```markdown
## Amendment A1 (round 29, before any case freeze or tool run; CriticC2Design F1-F10)

- **M1 field map.** A2-07: a case counts toward the rule's decisive floor when its journal holds at least two
  `earlyoom <version>` lines and at least one `dryrun mode enabled` line, and it pins
  `earlyoom.earlier_invocation_send_lines`, `earlyoom.actions.sigterm` or `earlyoom.actions.sigkill` with an integer
  above 0 (restores round-28 A1 "C2 field map"). Floor: at least 4 decisive A2-07 cases by at least 2 authors, at
  least 2 of them pinning `earlyoom.earlier_invocation_send_lines`. A2-10: decisive scope cases have an active
  earlyoom, a numeric non-zero `ActiveEnterTimestampMonotonic`, a numeric-stamped version line at or after it and at
  least one record without a numeric `__MONOTONIC_TIMESTAMP`, and pin `earlyoom.scope_complete`; floor 3 by at least
  2 authors. Decisive count cases hold a stamp-less send line and a stamped in-scope send line and pin
  `earlyoom.actions.sigterm`, `.sigkill` or `.escalations`; floor 2. Other cases stay in the file uncounted.
- **M2 assembly.** The case list is every element of the first fenced JSON array in each committed
  `.ufo/waves/round-29/w1/CaseA2(07|10)[a-d].md`, in report-name order, canonical-JSON equal to the file's `cases`
  element by element; `author` must equal the report's seat name. Each writer report's last change is an ancestor of
  the freeze commit and unchanged since. An id clash is resolved only by appending `-<author>` to every clashing id;
  no other edit. Canonical inputs must be distinct across the whole file and from every case of `cases.json` and
  `cases-a2.json`.
- **M3 blindness counted.** The counter runs the committed `check-blind-wave.sh <lane-rev> .ufo/waves/round-29/w1
  '^CaseA2(07|10)[a-d]\.md$'` and requires `blind_violations=0`. A writer's files-opened list that reports reading any
  `expect` block of `cases-a2.json` is disclosed in the lesson per affected case.
- **M4 judging.** One judge per mismatched case, named in the wave-2 spec before the first tool run; reading set equal
  to the writers' (`round-26/contract.md` whole, `round-27/contract.md:40-80`); each ruling cites the deciding line;
  the first ruling is binding. Every tool commit after the freeze names the ruled case ids in its message; a tool
  commit without a `tool error` ruling is a C2 miss.
- **M5 differential receipt.** For each tool commit after the freeze, a receipt lists every input of `cases.json`,
  `cases-a2.json`, `cases-a2-r29.json` and `.ufo/waves/round-26/evidence/a2-detectors/` whose full output JSON
  differs between the tool at the freeze commit and at that commit, each with the ruling it follows from; an
  unlisted or unjustified difference is a C2 miss.
- **M6 freeze order.** The freeze hash is written to `LOG.md` in the freeze commit's batch, before the first tool run;
  `count-c2.sh` has exactly one blob version up to `<lane-rev>` and its first commit is a strict ancestor of the
  freeze commit.
- **M7 routed shapes.** Each routed A2-07/A2-10 breach shape is stated as an input predicate (no expected value)
  before the freeze; at least one case per predicate, else C2 is a miss.
- **M8 provenance and statement.** "Eight blind seats" reads "every case delivered by the dispatched writers, at least
  3 authors per rule"; a dead writer's dimension is listed as uncovered. The `sources` key cites the writers' own
  fetches (URL, sha256); an S153+ row is cited only where its sha256 equals a writer's fetch.
```
Tradeoff: M1 and M7 can force a miss where no brief covers a shape; the fix is an added blind writer before freeze.

## After amendments A2 (`66125164`) and A3 (`69349c2a`), read 20:05Z

Closed: F2 (A3 provenance), F8 and F10 (A2 corrections); F5, F7 promised for the freeze batch. Open residuals:

- **R1 (from F1/F4, high):** neither shape line requires a decisive pin. A `shape_a207` case may pin only
  `dryrun_send_lines`; since both segments are in scope, count it only if it pins `actions.sigterm` or
  `actions.sigkill` with an integer above 0. A `shape_a210` case (unbounded or not active, `contract.md:142-143`) gets
  `scope_complete` false from A2-05 when unbounded, so a scope pin does not test A2-10 there: count it only if it pins
  `actions.sigterm`, `.sigkill`, `.escalations` or `earlier_invocation_send_lines` as an integer. The bounded
  active branch, where the scope pin is decisive, is in no shape line.
- **R2 (F2):** "every case of those eight reports whose author is listed" (`contract.md:158-159`) still allows dropping a
  whole writer. Fix the eight report names; every committed one counts; an absent one is reported as a death.
- **R3 (F3):** a failed process condition is "a C2 defect, never dropped" (`contract.md:145-148`), not a miss. Make a
  failed blindness receipt a C2 miss, as `case error` is.
- **R4 (F6, F9):** the differential receipt (M5) and the earlier-invocation A2-07 shape under a non-active unit remain
  unbounded; PASS 30/30 holds only three active-unit A2-07 cases.

## Files and commands opened

- godspeed `SKILL.md`, `RULES.md` (nothing installed); `.ufo/waves/round-29/contract.md` (whole); `.ufo/waves/round-27/contract.md:30-79`; `.ufo/waves/round-26/contract.md:50-190`;
  `.ufo/waves/round-28/contract.md:30-114`; `.ufo/waves/round-28/count-c2.sh` (whole);
  `corpus/lessons/round-28-verifier-spotcheck.md:100-133`; `corpus/lessons/round-28.md:135-150`.
- `wave1-spec.json`: context and the Case, BuildCountC2, BuildBlindCheck prompts (scratch copy `briefs.txt`).
- `cases.json`, `cases-a2.json`: keys, per-rule counts, ids, A2-07/A2-10 input shapes; pinned field names, no values.
- Read-only git: blobs of both older files at `7118f320`/`d21b8bd3`/`fc09f96c` equal (`7ba553d4…`, `5b4dcee7…`);
  new case path absent at `7118f320`; `git log`; `git diff 8a45cefe 69349c2a -- contract.md` (A1–A3).
- `ls` of `.ufo/waves/round-26/evidence/` and a count of `a2-detectors/` entries (16); contents not opened. Not opened: `tools/mori-oom-killers.py` or any copy, any tool output, any round-26..28 w1/w2 report, any round-29
  report of another seat. No URL fetched.
