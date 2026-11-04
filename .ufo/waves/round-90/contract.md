# mori round 90 — frozen contract

Lane: mori. Round: 90 (attempt 2). L1: MoriR90a2. Entering revision:
`037c02ca43a5ff36e23e449d0d6bcf50a1f2cbec` (lane `master`, clean, remote-equal).
Frozen before any after-value exists. Two claims, two axes, causally separable: C1 grades
`.ufo/waves/round-87/count-c2.py` (the receipt gate), C2 grades
`.ufo/waves/round-88/count-c1.py` and `.ufo/waves/round-88/count-c2.py`; neither counter reads the
other claim's subject, and neither target string contains the other's landing.

Axes: **operability** (C1, score 7) and **calibration** (C2, score 5 — tied lowest with depth 5 and
freshness 5; the stagnation nudge does not waive it). No score move is claimed.

## P-C1 — operability (frozen predicate)

At revision R, `python3 -I .ufo/waves/round-90/count-c1.py R` prints
`C1=met branch_open=0 harm=0 newopen=0 open=22 cases=78 rev=<12>` and a line
`BATTERY cases=<n> branch_cases=<n> branch_open=0 harm=0` with `branch_cases >= 12`, and exits 0,
where:

* `branch_open` counts the frozen branch-class counterfeits (the eight ids in the counter's
  `BRANCH` set) that the receipt gate at R still binds;
* `harm` counts the `met` cases the entering gate binds and the gate at R refuses;
* `newopen` counts the `reject` cases the gate at R binds and the entering gate refuses;
* `open` counts every counted `reject` case the gate at R still binds (`branch_open` plus the
  provenance class).

The provenance class stays bound by design and is **reported, never targeted**: functions,
`PATH`/interpreter substitution, `sitecustomize`, blob overwrite, heredoc data, `uv run -m`,
`bash -n`, `cat`/`$0`. A binding is a statement about the recorded command text; the receipt's
replay is the only execution evidence.

Population (frozen): the two round-89 attack batteries, 78 counted cases
(`.ufo/waves/round-89/r/Mo89R03Repair-evidence/cases.json` and
`.ufo/waves/round-89/r/Mo89C02Critic-evidence/heldout-all.txt`), with the class frozen by case id;
plus every `battery/*.json` committed under `.ufo/waves/round-90/` at R, graded separately and
written by a seat that did not author the rule (`branch_cases >= 12` required there).

Kill rule: the claim is met iff every field above matches and the exit status is 0. Exit 2 is
setup, never a pass. A blanket rule that refuses everything cannot meet it: `harm` counts the
`met` cases it refuses.

## P-C2 — calibration (frozen predicate)

At revision R, `python3 -I .ufo/waves/round-90/count-c2.py R` prints
`C2=met mutants=15 killed=15 survivors=0 unattributed=0 unanchored=0 isolated=0 literal_anchors=0 arms=29,27 rev=<12>`
and exits 0, where for every declared mutant: the subject at R is green at exactly its frozen arm
count, the anchor occurs exactly once in that subject and is not wholly inside a string literal,
and the mutated copy's own `--selftest` is killed **with attribution and isolation**.

Kill rule (frozen): `killed ⟺ (rc≠0 ∨ fail>0) ∧ failset(out) == {declared arm}`.
* a red run whose `FAIL` label set is a strict superset of the declared arm is `isolated`;
* a red run with no `FAIL` line, or with a different single label, is `unattributed`;
* an absent anchor is `unanchored`; an empty mutation is `empty-mutation`; a red pristine or a
  wrong pristine arm count is `pristine`; an anchor lying wholly inside a string literal is
  `literal-anchor`. Any of them keeps the claim unmet. Exit 2 is setup, never a pass.

Population (frozen): the twelve round-89 mutants (ranks 1–12 of
`.ufo/waves/round-88/w1/Mo88M01Mut.md`) plus the three round-89 neighbouring survivors
`.ufo/waves/round-89/r/Mo89M02Mut.md` B1 (`own_ok_of`'s arm-count pin), B4 (`met_line` at its call
site) and B6 (`clone_root_ok`'s negative). Anchors are the **after-revision** bytes: the three new
arms do not exist at the entering revision, so the entering run reports those three `survivor`.

## Pre-data amendments (disclosed; no target, population or kill rule moves)

* **A1** — the two r90 counters were inherited uncommitted from the dead attempt 1. Their selftest
  arms were repaired before any after-value: `count-c1.py`'s four synthetic-gate arms passed the
  fake gates in the wrong order (`deny` binds, `allow` refuses), and both counters' own pins
  (`TARGET`, `labels_unique`, `arms_pinned`, `EXPECTED_ARMS`, `target_split`) were still written
  for an earlier draft. `count-c2.py` also had to implement the frozen isolation and
  literal-anchor clauses it only documented. Every repair is pre-data: `evidence/controls-r90.txt`
  is the entering reading of the repaired bytes.
* **A2** — the C2 anchors for B4 are re-anchored on the after bytes of `.ufo/waves/round-88/count-c2.py`
  as the docstring requires; the defect class (printed line vs helper) and the label are unchanged.
* **A3** — `count-c1.py` prints the battery population as `BATTERY …` (not `BATTERY_RAW …`) so the
  frozen predicate sentence and the printed line are the same string.

## Do-nothing and skip-work controls (committed before any after-value)

`.ufo/waves/round-90/evidence/controls-r90.txt` (script `controls-r90.sh`):

1. do-nothing at `037c02ca`: both counters read unmet (C1 `branch_open=8 open=30`; C2
   `survivors=3`), so a round that lands nothing cannot reach either target;
2. blanket-refusal control: a gate that refuses every command is scored by the C1 counter's own
   tally and must read `harm>0` (it refuses the `met` cases), so refusal-all is not a gain;
3. label-only control: the three new C2 labels declared without their arms leave `survivors=3`.

## After measurement

The after value of each claim is measured at one lane commit that carries both the subjects and the
counters, by the frozen counters themselves, into
`.ufo/waves/round-90/evidence/after-r90.txt` (`# replay: clone`, `# rev:`, `# counter-sha256:`).
