# ScribeCriteria — round-44 QUALITY drafts 117–119

Seat: `L1Mori44-4.ScribeCriteria` (scribe, round 44, wave 1). Lane:
`/home/vgpnk/Projects/shokunin/mori-shokunin`. Entering tip `1429c791db5891c484684feef893799909d2d6a8`;
frozen instruments at `7cb59c6891d4f5d0266fe062565f094da835dc84` (`HEAD` at draft time). No frozen
instrument, `SKILL.md`, `SCORECARD.md`, `LOG.md`, `corpus/` file or lane git state was edited; every
command below is read-only and ran from the lane checkout. No subagents dispatched, no tool installs
or upgrades.

**State at draft time (observed, not inferred).** `git status --porcelain` shows the integration
owner's landing in progress: `M LOG.md`, `M SCORECARD.md`, `M corpus/QUALITY.md`, `M corpus/README.md`,
`M corpus/SOURCES.md`, `M corpus/lessons/round-43.md`, `?? corpus/knowledge/pid-probe-conclusion-r44.md`,
`?? .ufo/waves/round-44/w1/`, `?? .ufo/waves/round-44/w1-spec.json`. The round-43 lesson change is an
appended erratum (`git diff corpus/lessons/round-43.md`), not an in-place rewrite. `corpus/QUALITY.md`
already carries an **uncommitted** 117–119 block (40 added lines); this seat did not write it and did
not edit it. §Reconciliation lists the corrections that block needs; the drafts below are the
append-ready versions.

**Pending after-runs (marked `[PENDING]` below).** `.ufo/waves/round-44/figures.tsv` is absent at
`7cb59c68` (`git cat-file -e 7cb59c68:.ufo/waves/round-44/figures.tsv` → `fatal: path ... does not
exist`, exit 128), `corpus/knowledge/pid-probe-conclusion-r44.md` is uncommitted, `corpus/lessons/round-44.md`
does not exist yet (`ls` → `No such file or directory`), and `.ufo/waves/round-44/evidence/c1s-tip-run.txt`
does not exist yet. The integration owner must record the `C1=met` / `C2=met` receipts at the landing
tip and commit the tip-run receipt before citing those verdicts as met.

---

## Draft 117 — reported counts reconciled by a committed ledger

Append-ready text (4-space continuation indent; supersedes the provisional 117 if that block is kept):

```text
117. A round's reported counts are reconciled by a committed figure ledger, not by re-reading the round's own
    prose: every numeric assertion the report makes about a committed artifact class has a row whose asserted
    value equals the value one `git` pipeline over the measured revision prints, and the frozen counter prints
    `C1=met mismatches=0` only when every row matches and the ledger holds at least 12 rows covering at least 4
    of {registry, evidence, wave, corpus, checks}. Rationale: round-43's report asserted "15 checks PASS" where
    its own receipt carried 14, and "34 seat logs carry `provider.rate_limit: 429`" where `git grep -l` found 8;
    re-reading the same evidence cannot catch a count that was never recomputed
    (`corpus/lessons/round-43-verifier-spotcheck.md:209-212`, routed defect 3; the general form is
    `considerthese/2026-10-24.md:24`, "Reproduce headline numbers mechanically"). Lesson:
    `corpus/lessons/round-44.md` (pending at draft time; the round-43 closure is the standing pointer). Check:
    `python3 .ufo/waves/round-44/count-c1.py <landed tip>` prints `C1=met mismatches=0`, exit 0, over the
    committed `.ufo/waves/round-44/figures.tsv`. Shown able to fail:
    `python3 .ufo/waves/round-44/count-c1.py 7cb59c68 --ledger .ufo/waves/round-44/fixtures/figures-r43.tsv`
    prints `check commands_reconcile FAIL (F03 asserted=15 observed=14; F04 asserted=34 observed=8)` and
    `C1=unmet mismatches=2`, exit 1 (run 2026-10-25; independently re-run in `w1/ExecJunkLedger.md`); at the
    entering tip the same counter prints `check ledger_present FAIL (absent)`, `C1=unmet`, exit 1
    (`evidence/control-c1-donothing.txt`). Not covered: the counter measures ledger well-formedness and
    arithmetic agreement, not informativeness or coverage. `w1/ExecJunkLedger.md` (run 2026-10-25) committed
    twelve copies of `git diff @REV@ @REV@ | wc -l` asserting 0 in a repository whose only tracked file was the
    ledger and got `C1=met mismatches=0`, exit 0; the 12-row and 4-class floors are shape costs (duplicate rows
    are legal), the grammar blocks non-byte producers but not revision-invariant constants, and no check proves a
    row is a figure the report states or that the ledger is complete. The witness is revision-bound: F04 reads 0
    before `91cb221f`, where `.ufo/waves/round-43/logs` first appears (`w1/ScoutR43Wording.md` §5).
```

Verification of every run cited above is in §Evidence index, items E1, E2, E5, E6.

---

## Draft 118 — a round counter is a registered gate before it scores

Append-ready text:

```text
118. A round-scoped measurement counter is a registered gate before it scores anything: `SKILL.md`'s `## Gates`
    table carries a row naming its repo-relative path with all eight standard cells (name, kind, entry, verdict
    map, self-test, pinned values, write scope, owner) non-empty, the path resolves at the measured revision, the
    counter's `--selftest` runs over isolated fixtures and prints a `pass=/fail=` tally with fail 0, and a
    committed mutant of that same counter whose one check is disabled is caught by the counter's own selftest;
    the conformance counter prints `C2=met` only when all of those hold for every counter it is given. Rationale:
    round-43's two new counters had no registry row and no `--selftest` mode, and the closure graded no gate
    conformant until the row existed (`corpus/lessons/round-43-verifier-spotcheck.md:213-216`, routed defect 4).
    Lesson: `corpus/lessons/round-44.md` (pending at draft time). Check:
    `python3 .ufo/waves/round-44/count-c2.py <landed tip> --counter .ufo/waves/round-44/count-c1.py --counter
    .ufo/waves/round-44/count-c2.py --counter .ufo/waves/round-44/count-c3.py --mutants-dir
    .ufo/waves/round-44/fixtures/mutants` prints `C2=met`, exit 0. The explicit `--mutants-dir` is required: the
    tool's default is `fixtures/mutants` relative to the repository root, which does not exist at `7cb59c68`
    (`git ls-tree -r --name-only 7cb59c68 fixtures` → empty) or in the worktree, and the same command
    without the flag prints `check mutant_kill FAIL (count-c1.py mutant absent; count-c2.py mutant absent;
    count-c3.py mutant absent)`, `C2=unmet`, exit 1 (run 2026-10-25 at `7cb59c68`; the same revision with the flag
    prints `mutant_kill PASS (count-c1.py killed (fail=1); count-c2.py killed (fail=1); count-c3.py killed
    (fail=1))`, `C2=met`, exit 0). Shown able to fail:
    `python3 tools/mori-gate-registry.py --rev 1429c791 --audit .ufo/waves/round-43/count-c1s.py --audit
    .ufo/waves/round-43/count-c2.py` prints both `FAIL (unregistered: no row names ...)` and `REGISTRY=unmet`,
    exit 1 (`evidence/witness-r43-gates.txt`); the C2 selftest kills the same classes it names
    (`unregistered_counter_unmet`, `no_selftest_mode_unmet`, `surviving_mutant_unmet`;
    `C2_SELFTEST pass=5 fail=0`, run 2026-10-25), and the registry selftest kills `missing_cell_rejected`,
    `unresolved_entry_rejected`, `unregistered_path_rejected`, `no_selftest_rejected`, `seven_cell_row_rejected`
    (`GATE_REGISTRY_SELFTEST pass=6 fail=0`, run 2026-10-25). Not covered: the auditor checks the eight cells for
    non-emptiness and the entry for resolution, not for truth — this round's own `r44 gate conformance (C2)` row
    passes with a pinned-values cell (`fixtures/mutants/<basename>`) that does not resolve at the repository root,
    which is why the check above must spell `--mutants-dir`. `w1/MutRegistry.md` (run 2026-10-25) kept five
    crafted registries green: a ghost-suffix entry, a prefix tool (`not-mori-gate-registry.py`), a
    directory-prefix tool, a nine-cell row, and a duplicate pair whose longer malformed row loses to the shorter
    good row. `w1/ExecGateInventory.md` (run 2026-10-25) found the auditor reads only the first standard-header
    table under `## Gates` and stops at the next `## `, so 11 conforming secondary-table registrations score as
    absent, it cannot distinguish a gate from a probe, and `--selftest` is a byte-substring test. The criterion
    covers only the counters the round names: the same auditor over all 33 `tools/*` presents `REGISTRY=unmet`
    (14 unregistered + 1 thin row).
```

Verification in §Evidence index, items E3, E4, E7, E8, E10, E11.

---

## Draft 119 — the receipt and the verdict name the same revision

Append-ready text:

```text
119. A receipt names the revision it measured and the verdict names the same revision: for every measured claim,
    the committed receipt's `# command:`/`rev=` line, the report's measured-against cell and SCORECARD's
    measured-commit cell name the same full 40-hex commit, and a counter that prints `rev=` is cited only through
    a run whose `rev=` is that commit; a symbolic `rev=WORK` receipt names no revision and does not satisfy the
    rule. Rationale: round-43's C1S receipt
    measured `dde525ea4a7fca365e8ff2f3c486bccf28b94e52` while the verdict said "at the landed tip", whose lane tip
    the same report names as `91cb221f35f7cb9afeff99ef1959512dabddfc46`; the equivalence rested on a sha256
    assertion, not on a run at the claimed revision (`corpus/lessons/round-43-verifier-spotcheck.md:217-219`,
    routed defect 5). Lesson: `corpus/lessons/round-44.md` (pending at draft time). Check:
    `python3 .ufo/waves/round-44/count-c1.py <landed tip>` prints `rev=<40-hex>` equal to the commit named in the
    committed receipt, in the report's measured-against cell and in SCORECARD's measured-commit cell; every
    committed counter receipt carries a `rev=`
    line (`grep -L 'rev=' .ufo/waves/round-44/evidence/control-c*.txt` → empty, run 2026-10-25), and the receipt
    the round commits for its tip run repeats the tip's full 40-hex, never a prefix and never `WORK`. Shown able
    to fail: `.ufo/waves/round-43/evidence/c1s-after.txt:1` reads
    `command: python3 .ufo/waves/round-43/count-c1s.py dde525ea4a7fca365e8ff2f3c486bccf28b94e52` while
    `.ufo/reports/round-43/mori.md:114-115` says the clause is "discharged at the landed tip" and `:257` names the
    lane tip `91cb221f35f7cb9afeff99ef1959512dabddfc46`; and this round
    `python3 .ufo/waves/round-44/count-c1.py WORK --ledger .ufo/waves/round-44/fixtures/figures-r43.tsv` prints
    `rev=WORK` even though it substitutes the resolved tip for `@REV@` in every row (run 2026-10-25), so a
    WORK-mode receipt cannot satisfy the rule. Not covered: the revision label is not the instrument's identity —
    a receipt at revision R produced by a locally mutated counter still prints `rev=R`, so the counter's sha256 pin
    (QUALITY 109's class) remains a separate check; older gates that never print a measured revision
    (`w1/ExecGateInventory.md`: most `tools/*` probes) are caught only by review; and a receipt whose `rev=` line is
    hand-edited is not detected, the committed bytes being the only witness.
```

Verification in §Evidence index, items E9, E12, E13, E14.

---

## Reconciliation with the provisional block already in `corpus/QUALITY.md`

The worktree block (`corpus/QUALITY.md:941-979`, uncommitted, 40 added lines, not authored by this seat)
is close to the drafts above. If it is kept, these cells must change; each correction is backed by a run:

| provisional cell | observed this round | correction |
|---|---|---|
| 118 `Check:` names `count-c2.py <tip> --counter ...` with **no** `--mutants-dir` | at `7cb59c68` the printed form prints `check mutant_kill FAIL (count-c1.py mutant absent; count-c2.py mutant absent; count-c3.py mutant absent)`, `C2=unmet`, exit 1; with `--mutants-dir .ufo/waves/round-44/fixtures/mutants` it prints `mutant_kill PASS (... killed (fail=1))`, `C2=met`, exit 0 | add `--mutants-dir .ufo/waves/round-44/fixtures/mutants`; the row's `fixtures/mutants/<basename>` pinned-values cell is wrong for the committed layout |
| 118 `Not covered:` cites `w1/MutRegistry.md` and a pointer to "the inventory", but not `w1/ExecGateInventory.md`'s specific findings | `w1/ExecGateInventory.md` additionally observed: first-table-only scope (11 secondary registrations invisible), `kind` not enforced, `--selftest` byte-substring, 14 unregistered + 1 thin row over all 33 `tools/*` | add those limits; they are the auditor's, not this round's counters' |
| 119 `Check:` begins `head -3 .ufo/waves/round-44/evidence/c1s-tip-run.txt` | the file is absent (`ls` → `No such file or directory`, 2026-10-25); the receipt is `[PENDING]` until ExecC1STip's text is committed | keep the command only after the integration owner commits the receipt; until then the check cannot run. Add the rev-equality clause and the `rev=WORK` failure (both run this round) |
| 117 `Check:` expects `C1=met` at `<tip>` | `figures.tsv` is absent at `7cb59c68` (`git cat-file -e` exit 128); the after-run is `[PENDING]` | record the `C1=met` receipt at the landing tip before citing it; the witness and do-nothing halves are verified now |
| 117/118/119 `Lesson:` points at `corpus/lessons/round-44.md` | the file does not exist yet (`ls` → `No such file or directory`) | land the lesson first, or cite `corpus/lessons/round-43-verifier-spotcheck.md` until ScribeLesson's draft is finalized |

The provisional 117's `Not covered:` already carries the ExecJunkLedger vacuity finding correctly, and
its `Rationale:` cite `considerthese/2026-10-24.md:24` resolves (`grep -n "Reproduce headline numbers
mechanically"` → line 24). Those cells need no correction.

---

## Evidence index

All commands ran 2026-10-25 from `/home/vgpnk/Projects/shokunin/mori-shokunin`; all read-only.

**E1 — C1 witness (run this seat).**
```
$ python3 .ufo/waves/round-44/count-c1.py 7cb59c68 --ledger .ufo/waves/round-44/fixtures/figures-r43.tsv
check ledger_present       PASS (1518 bytes)
check rows_parse           PASS (12 rows)
check row_floor            PASS (rows=12 min=12)
check class_floor          PASS (classes=checks,corpus,evidence,registry,wave min=4)
check commands_reconcile   FAIL (F03 asserted=15 observed=14; F04 asserted=34 observed=8)
rev=7cb59c6891d4f5d0266fe062565f094da835dc84
ledger=.ufo/waves/round-44/fixtures/figures-r43.tsv rows=12 classes=checks,corpus,evidence,registry,wave
C1=unmet mismatches=2
exit=1
```

**E2 — C1 selftest (run this seat).** `python3 .ufo/waves/round-44/count-c1.py --selftest` → six
`selftest PASS` lines (`honest_ledger_met`, `offbyone_row_mismatch`, `junk_producer_rejected`,
`below_floor_rejected`, `absent_ledger_unmet`, `compound_command_rejected`), `C1_SELFTEST pass=6 fail=0`,
exit 0. Matches the freeze tally (`evidence/freeze-r44.txt`).

**E3 — C2 selftest (run this seat).** `python3 .ufo/waves/round-44/count-c2.py --selftest` → five
`selftest PASS` lines (`registered_conformant_met`, `absent_counter_unmet`, `unregistered_counter_unmet`,
`no_selftest_mode_unmet`, `surviving_mutant_unmet`), `C2_SELFTEST pass=5 fail=0`, exit 0. Matches the
freeze tally.

**E4 — C3 and registry selftests (run this seat).** `python3 .ufo/waves/round-44/count-c3.py --selftest`
→ six PASS arms, `C3_SELFTEST pass=6 fail=0`, exit 0. `python3 tools/mori-gate-registry.py --selftest` →
six PASS arms (`registered_row_met`, `missing_cell_rejected`, `unresolved_entry_rejected`,
`unregistered_path_rejected`, `no_selftest_rejected`, `seven_cell_row_rejected`),
`GATE_REGISTRY_SELFTEST pass=6 fail=0`, exit 0. Both match the freeze tallies.

**E5 — C1 do-nothing (committed receipt, `evidence/control-c1-donothing.txt`).**
`check ledger_present FAIL (absent)`, `rev=1429c791db5891c484684feef893799909d2d6a8`,
`ledger=.ufo/waves/round-44/figures.tsv rows=0 classes=-`, `C1=unmet mismatches=?`, exit 1.

**E6 — ExecJunkLedger (seat run, `w1/ExecJunkLedger.md`).** Twelve rows of
`git diff @REV@ @REV@ | wc -l` asserting `0`, in a repo whose only tracked file is the ledger →
`check commands_reconcile PASS (all rows match)`, `C1=met mismatches=0`, exit 0. Also the one-lying-row
control → `FAIL (F01 asserted=7 observed=0)`, `C1=unmet mismatches=1`, exit 1.

**E7 — Registry audit of the round's three counters (run this seat).**
```
$ python3 tools/mori-gate-registry.py --rev 7cb59c68 --audit .ufo/waves/round-44/count-c1.py \
    --audit .ufo/waves/round-44/count-c2.py --audit .ufo/waves/round-44/count-c3.py
audit .ufo/waves/round-44/count-c1.py          PASS (row 'r44 figure ledger (C1)': 8 cells, entry resolves, --selftest present)
audit .ufo/waves/round-44/count-c2.py          PASS (row 'r44 gate conformance (C2)': 8 cells, entry resolves, --selftest present)
audit .ufo/waves/round-44/count-c3.py          PASS (row 'r44 corpus coverage (C3)': 8 cells, entry resolves, --selftest present)
rev=7cb59c6891d4f5d0266fe062565f094da835dc84
REGISTRY=met
exit=0
```

**E8 — C2 with and without the mutants flag (run this seat, both at `7cb59c68`).**
Without `--mutants-dir`: `check counters_present PASS (3 counters)`, `registry_rows PASS (REGISTRY=met)`,
`tool_selftest PASS (pass=6 fail=0)`, `selftest_tally PASS (count-c1.py pass=6; count-c2.py pass=5;
count-c3.py pass=6)`, `check mutant_kill FAIL (count-c1.py mutant absent; count-c2.py mutant absent;
count-c3.py mutant absent)`, `C2=unmet`, exit 1.
With `--mutants-dir .ufo/waves/round-44/fixtures/mutants`: same four PASS lines and
`check mutant_kill PASS (count-c1.py killed (fail=1); count-c2.py killed (fail=1); count-c3.py killed
(fail=1))`, `C2=met`, exit 0. `git ls-tree -r --name-only 7cb59c68 fixtures` → empty; the committed
mutants are at `.ufo/waves/round-44/fixtures/mutants/{count-c1,count-c2,count-c3}.py`.

**E9 — Round-43 gate witness (committed receipt, `evidence/witness-r43-gates.txt`).**
`python3 tools/mori-gate-registry.py --rev 1429c791 --audit .ufo/waves/round-43/count-c1s.py --audit
.ufo/waves/round-43/count-c2.py` → `audit .ufo/waves/round-43/count-c1s.py FAIL (unregistered: no row
names count-c1s.py)`, `audit .ufo/waves/round-43/count-c2.py FAIL (unregistered: no row names
count-c2.py)`, `REGISTRY=unmet`, exit 1.

**E10 — MutRegistry (seat run, `w1/MutRegistry.md`).** KILLED: empty verdict-map cell, empty owner,
ghost entry, `-old.py` substring, renamed header, escaped pipe (8 cells), escaped-pipe-plus-empty-owner,
escaped column boundary, duplicate bad-short, duplicate tie. SURVIVED: ghost-suffix entry (basename
match), prefix tool `not-mori-gate-registry.py`, directory-prefix tool, nine-cell row, duplicate
long-bad-loses. All verdicts with fixture and rev in the report's table at lines 24-42.

**E11 — ExecGateInventory (seat run, `w1/ExecGateInventory.md`).** `mori-gate-registry.py --rev 7cb59c68`
over all 33 `tools/*` gate/probe presentations → `REGISTRY=unmet`, exit 1 (14 unregistered + 1 thin row).
The auditor attributes `tools/mori-census.sh` to the `drift pin` row, reads only the first
standard-header table (11 secondary registrations invisible), does not enforce `kind`, and tests
`--selftest` as a byte substring.

**E12 — WORK mode (run this seat).**
```
$ python3 .ufo/waves/round-44/count-c1.py WORK --ledger .ufo/waves/round-44/fixtures/figures-r43.tsv
...
rev=WORK
...
C1=unmet mismatches=2
exit=1
```
`@REV@` was substituted with the resolved tip (`7cb59c68...`), but the printed revision is the symbolic
`WORK`.

**E13 — Round-43 receipt vs verdict (committed bytes, read this seat).**
`sed -n '1,3p' .ufo/waves/round-43/evidence/c1s-after.txt` → line 1
`command: python3 .ufo/waves/round-43/count-c1s.py dde525ea4a7fca365e8ff2f3c486bccf28b94e52`.
`sed -n '114,115p;257p' /home/vgpnk/Projects/shokunin/.ufo/reports/round-43/mori.md` →
```
line 114: - **C1S — verified (measured), with a disclosed instrument-tamper limitation.** Every clause of
line 115:   the frozen P-C1S sentence is discharged at the landed tip by the receipt and the generated
line 257:   lane lines are its `landed <hash>` outputs: `dde525ea4a7fca365e8ff2f3c486bccf28b94e52`,
```
The same report names the lane tip `91cb221f35f7cb9afeff99ef1959512dabddfc46` at `:259` (report
integrity bullet). The closure routed the mismatch as defect 5
(`corpus/lessons/round-43-verifier-spotcheck.md:217-219`).

**E14 — Control receipts carry `rev=` (run this seat).**
`grep -L 'rev=' .ufo/waves/round-44/evidence/control-c*.txt` → no output, exit 0; each of the three
control receipts carries `rev=1429c791db5891c484684feef893799909d2d6a8`, matching its `# command:` line.

**E15 — Pending-artifact probes (run this seat).**
`git cat-file -e 7cb59c68:.ufo/waves/round-44/figures.tsv` → `fatal: path ... does not exist`, exit 128.
`git cat-file -e 7cb59c68:corpus/knowledge/pid-probe-conclusion-r44.md` → `fatal: path ... exists on
disk, but not in '7cb59c68'`, exit 128. `ls .ufo/waves/round-44/evidence/c1s-tip-run.txt` → `No such
file or directory`. `ls corpus/lessons/round-44.md` → `No such file or directory`.

**E16 — Round-43 closure item pointers (run this seat).**
`grep -nE '^[0-9]+\. ' corpus/lessons/round-43-verifier-spotcheck.md` → item 3 at 209, item 4 at 213,
item 5 at 217. `grep -n "Reproduce headline numbers mechanically" considerthese/2026-10-24.md` → line 24.

---

## Findings

1. **The provisional 118 check command cannot print `C2=met`.** As appended (`corpus/QUALITY.md:962-964`),
   it omits `--mutants-dir`; the frozen default is `fixtures/mutants` relative to the repository root,
   which does not exist at `7cb59c68` (`git ls-tree -r --name-only 7cb59c68 fixtures` → empty) or in the
   worktree. Observed at `7cb59c68`: `C2=unmet`, `mutant_kill FAIL`, exit 1; with the
   wave-tree flag: `C2=met`, exit 0 (E8). This is the same class QUALITY 111 corrected for round 38 (a
   printed check that exits non-green).
2. **The provisional 119 check command cites an absent receipt.** `head -3
   .ufo/waves/round-44/evidence/c1s-tip-run.txt` fails today (E15). The receipt is ExecC1STip's deliverable;
   until the integration owner commits it, the check cannot run, and the criterion must not be cited as met.
3. **`WORK` mode prints `rev=WORK`, not the measured revision** (E12). The counter resolves the tip and
   substitutes it into every row, but the receipt would name no commit. A round receipt must use an
   explicit 40-hex revision.
4. **The registry auditor is green on wrong rows.** The round's own `r44 gate conformance (C2)` row's
   pinned-values cell (`fixtures/mutants/<basename>`) does not resolve at the repo root (E8), and
   MutRegistry's five survivor classes (E10) plus ExecGateInventory's table-scope/`kind` findings (E11)
   are not caught. Criterion 118's check is only as strong as those runs; the not-covered cell must say so.
5. **C1's floors are shape costs, not content costs.** ExecJunkLedger's twelve `git diff @REV@ @REV@`
   rows pass (E6). Criterion 117 must not be read as certifying report coverage; the tightening (a
   revision-sensitivity arm) is routed to round 45 by the contract's freeze rule.
6. **Concurrent landing observed, not judged.** The worktree carries the integration owner's append-only
   erratum to `corpus/lessons/round-43.md` and the uncommitted 117-119 block; this seat measured committed
   bytes at `1429c791` / `7cb59c68` and wrote only this report. No conflict between the erratum's figures
   and E1: the erratum says 14 and 8, and the witness fixture's asserted 15 and 34 reproduce the
   superseded values.

---

## Out of scope / not done

- Did not edit `corpus/QUALITY.md`; the provisional 117-119 block is not this seat's write.
- Did not run the landed-tip `C1=met` / `C2=met` after-measurements: `figures.tsv` and the knowledge
  entry are not committed at draft time (`[PENDING]`).
- Did not run `count-c3.py` at a landed tip: the entry is uncommitted; the do-nothing receipt is
  `evidence/control-c3-donothing.txt` (`check entry_present FAIL (absent)`, `C3=unmet`, exit 1).
- Did not re-run the round-43 C1S counter at the round-44 tip; ExecC1STip owns that receipt.
- Did not audit the registry rows' prose beyond the runs cited (RevRegistryRows owns that).
- No subagent dispatch, no tool installs or upgrades, no git write command, no host mutation.
