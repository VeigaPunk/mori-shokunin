source: S617
verified-at: 2026-11-05
recheck: 90d

# Arming a calibration gate: attributed kills and what a kill does not prove

## 1. Practice from S617

Jia and Harman define the practice this lane's calibration claims use. The located opening of
their survey, Section I, reads (≤25 words, verified by `grep -c -F` = 1 against the pdftotext raw
text of the course-hosted copy, sha256 `056ac9b9…83edff342`):

> "Mutation Testing is a fault-based testing technique which provides a testing criterion called the"

The survey's Section II-B defines a mutant as killed when a test distinguishes it from the original,
and the mutation score as killed mutants over non-equivalent mutants. Those two definitions are read
in the paper, not quoted here, and this entry does not rely on any other sentence of the paper.

## 2. The rule the lane applies (lane rule, not a source claim)

A calibration arm is a named selftest check. A mutant of a gate's clause counts as killed only when
the gate's red run carries FAIL labels that begin with the mutant's declared clause-family name, and
no label outside that family. A red run with no FAIL label is unattributed. A red run with a label
outside the family is isolated: the mutant turned the gate red through a different clause, so it
earned no kill for this family.

## 3. Limits (state these with every use of the rule)

- A structural arm proves the arm is present and labelled. It does not prove the clause decides
  correctly on any input.
- An independent population is an attack, not a proof. A kill of an independently written mutant
  shows the selftest caught that edit. A survivor shows a gap. Neither shows every edit of the
  family is caught.
- A subject that prints each declared label whenever it is mutated meets the label rule by
  construction. The label rule therefore does not establish attribution alone.
- Equivalent mutants cannot be decided in general; the survey's Section IV states the undecidability.
  A survivor may be an equivalent mutant, so a survivor count is an upper bound on the gap.

## 4. What this entry does not claim

- It claims no score move. Round 91 did not land the arms: its populations and counter were not
  measured (see `corpus/lessons/round-91.md`).
- It does not cite any source other than S617. S618 is rejected in `corpus/SOURCES.md` and is not
  cited here.
