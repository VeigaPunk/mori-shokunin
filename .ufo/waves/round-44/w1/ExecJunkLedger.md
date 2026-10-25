# ExecJunkLedger — cheapest C1 ledger that passes (round 44, w1)

Scope: build the least informative `figures.tsv` the frozen counter will accept, and state
exactly what its verdict buys. Instruments read at freeze commit `7cb59c6891d4`; no frozen
byte edited, no lane git mutation, all scratch work in `/tmp` sandboxes.

## Verdict

**Yes — `C1=met` is reachable with twelve copies of one tautology that names no artifact.**
Two independent cheapest constructions both pass, including one in a repository whose *only*
tracked file is the ledger itself.

## The minimal ledger (12 rows, 1 distinct figure, 4 class labels)

Committed at `.ufo/waves/round-44/figures.tsv` (510 bytes) in a scratch repo:

```
F01	0	registry	git diff @REV@ @REV@ | wc -l
F02	0	evidence	git diff @REV@ @REV@ | wc -l
F03	0	wave	git diff @REV@ @REV@ | wc -l
F04	0	corpus	git diff @REV@ @REV@ | wc -l
F05	0	registry	git diff @REV@ @REV@ | wc -l
F06	0	evidence	git diff @REV@ @REV@ | wc -l
F07	0	wave	git diff @REV@ @REV@ | wc -l
F08	0	corpus	git diff @REV@ @REV@ | wc -l
F09	0	registry	git diff @REV@ @REV@ | wc -l
F10	0	evidence	git diff @REV@ @REV@ | wc -l
F11	0	wave	git diff @REV@ @REV@ | wc -l
F12	0	corpus	git diff @REV@ @REV@ | wc -l
```

`git diff <rev> <rev>` is the empty diff at every revision, so the figure is a constant of the
*instrument*, not of the repository: it cannot be wrong because it is not about anything. It is
still one `git` pipeline naming `@REV@`, still a read verb (`diff` is in `GIT_VERBS`), carries no
`echo`/`printf`/`true`, no `;`, no `&&`, and prints a bare integer (`0`) through the counter's
`| head -c 64` tail. Every grammar gate the contract calls a kill rule is satisfied.

### Run 1 — sandbox `/tmp/c1junk-od13ige8`, rev `67c1641618ee9c1f57e783380aa1b5c766a70b0f`

```
$ python3 .ufo/waves/round-44/count-c1.py 67c16416… --repo /tmp/c1junk-od13ige8/repo
check ledger_present       PASS (510 bytes)
check rows_parse           PASS (12 rows)
check row_floor            PASS (rows=12 min=12)
check class_floor          PASS (classes=corpus,evidence,registry,wave min=4)
check commands_reconcile   PASS (all rows match)
rev=67c1641618ee9c1f57e783380aa1b5c766a70b0f
ledger=.ufo/waves/round-44/figures.tsv rows=12 classes=corpus,evidence,registry,wave
C1=met mismatches=0          (exit 0)
```

### Run 2 — the extreme: repo containing nothing but the ledger

Sandbox `/tmp/c1bare-tcxdisif`, rev `2def62b7362cba16e51040a2dff707dc1b43cb96`,
`git ls-tree -r --name-only 2def62b7…` → `.ufo/waves/round-44/figures.tsv` (one entry, the
ledger). Same twelve rows, same result:

```
check ledger_present       PASS (510 bytes)
check rows_parse           PASS (12 rows)
check row_floor            PASS (rows=12 min=12)
check class_floor          PASS (classes=corpus,evidence,registry,wave min=4)
check commands_reconcile   PASS (all rows match)
C1=met mismatches=0          (exit 0)
```

This is the sharpest form of the finding: a repository with **zero** registry rows, zero
evidence files, zero wave artifacts, zero corpus entries prints `C1=met`.

### Run 3 — the second-cheapest family (existence tautologies)

Sandbox `/tmp/c1junk-od13ige8`, rev `138c537a0b990293675f2ca22cecb17233ae7299`: twelve rows of
`git ls-tree @REV@ -- <path> | wc -l` asserting `1`, spread over all five class labels
(`SKILL.md`, `registry/knowledge.tsv`, `evidence/freeze-r44.txt`,
`.ufo/waves/round-44/contract.md`, `corpus/README.md`, `checks/count-c1.py`, each twice):

```
check class_floor          PASS (classes=checks,corpus,evidence,registry,wave min=4)
check commands_reconcile   PASS (all rows match)
C1=met mismatches=0          (exit 0)
```

`ls-tree -- <path> | wc -l` is `1` exactly when the path is in the tree, so the row asserts
presence and nothing about the file's content. Two rows per path mean the twelve "figures" are
six existence bits.

## The pass is not vacuous — it is merely uninformative

Three controls confirm the counter discriminates equality, and only equality.

- One lying row (sandbox `/tmp/c1junk-od13ige8`, rev `e6a19ff881c4…`):
  `check commands_reconcile FAIL (F01 asserted=7 observed=0)` → `C1=unmet mismatches=1`, exit 1.
- 11 rows (sandbox `/tmp/c1bare-tcxdisif`, rev `c4ef0078a3d8…`):
  `check row_floor FAIL (rows=11 min=12)` → `C1=unmet mismatches=0`, exit 1.
- 12 rows over 3 labels (rev `e0186c4d214a…`):
  `check class_floor FAIL (classes=evidence,registry,wave min=4)` → `C1=unmet mismatches=0`, exit 1.

So the two floors are the only structural cost, and both are shape costs, not content costs:
"12 rows" is 12 *lines* (duplicates legal — the instrument's own selftest `_honest_rows()`
uses twelve copies of one `git show @REV@:data.txt | grep -c x`), and "4 classes" is 4
*distinct strings in the class cell*, with no check that the string matches what the command
reads.

Witness sanity, for contrast (lane repo, read-only, ledger `fixtures/figures-r43.tsv`):

```
$ python3 .ufo/waves/round-44/count-c1.py 7cb59c68… --ledger .ufo/waves/round-44/fixtures/figures-r43.tsv
check commands_reconcile   FAIL (F03 asserted=15 observed=14; F04 asserted=34 observed=8)
C1=unmet mismatches=2          (exit 1)
```

(That fixture is not committed at the entering tip `1429c791…`, where the same invocation prints
`check ledger_present FAIL (absent)`; the witness only resolves at/after the freeze commit.)

## What `C1=met` certifies, and what it does not

**Certifies (one sentence):** that the committed `.ufo/waves/round-44/figures.tsv` at the
measured revision parses into at least twelve four-cell rows spanning at least four distinct
class labels, and that each row's asserted integer equals the integer its own single `git`
pipeline over that revision prints.

**Does not certify (one sentence):** that any row's number is a number the round's report
actually states, that the class label names the artifact class the command reads, that the
twelve rows are twelve distinct figures, or that the ledger is complete — because a repo whose
only committed file is the ledger, filled with twelve copies of `git diff @REV@ @REV@ | wc -l`
asserting `0`, prints `C1=met mismatches=0` exit 0.

The mechanism is precise and worth naming for round 45: the grammar blocks *lies about bytes*
(no `echo`/`printf`/`true` producer, must name `@REV@`, must be a read verb), but it does not
block *vacuity about bytes*. `git diff @REV@ @REV@` reads committed objects and yields a
revision-invariant constant, so a ledger can be a fixed point of the instrument while carrying
no information about the round. Reconciliation of a *self-consistent* ledger is therefore a
necessary condition for calibration, not a sufficient one; C1 as frozen measures ledger
well-formedness plus arithmetic agreement, and its verdict should be read as "the ledger does
not lie about what it chose to count", never as "the round's reported counts are right".

## Files changed

- `.ufo/waves/round-44/w1/ExecJunkLedger.md` (this report). Nothing else. No frozen instrument,
  no `SKILL.md`/`SCORECARD.md`/`LOG.md`/`corpus/` file, no lane git state touched.

## Risks / blockers

- None blocking. The finding is a scoping risk for the C1 claim's framing, not a defect to patch
  post-freeze (contract §Freeze: routed to round 45, never patched in place).
- Scratch sandboxes left in place for reproduction: `/tmp/c1junk-od13ige8`,
  `/tmp/c1bare-tcxdisif`.
- No tool installs or upgrades were needed.
