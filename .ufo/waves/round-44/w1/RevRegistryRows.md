# RevRegistryRows — do the four round-44 `## Gates` rows describe the tools as they behave?

Seat: reviewer (leaf member; no subagent dispatch). Round 44, wave 1.
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Measured revision for every claim below: `7cb59c6891d4f5d0266fe062565f094da835dc84`
(the freeze commit). The lane checkout was never mutated; every probe ran in throwaway
clones under `mktemp -d`.

Rows under review (`SKILL.md` `## Gates`, lines 183–186, header at line 162):

| line | row |
|---|---|
| 183 | `r44 figure ledger (C1)` |
| 184 | `r44 gate registry (C2)` |
| 185 | `r44 gate conformance (C2)` |
| 186 | `r44 corpus coverage (C3)` |

The brief names three rows but lists four; all four were reviewed.

Tooling installed or upgraded: **none** (system `python3` 3.14.8, `git` 2.56.0).

---

## 1. Frozen bytes verified before any run

```
$ sha256sum .ufo/waves/round-44/contract.md .ufo/waves/round-44/count-c1.py \
    .ufo/waves/round-44/count-c2.py .ufo/waves/round-44/count-c3.py \
    tools/mori-gate-registry.py .ufo/waves/round-44/fixtures/figures-r43.tsv \
    .ufo/waves/round-44/fixtures/mutants/count-{c1,c2,c3}.py SKILL.md
0c261cb3…  .ufo/waves/round-44/contract.md
9477824d…  .ufo/waves/round-44/count-c1.py
0095d0c6…  .ufo/waves/round-44/count-c2.py
a12170f1…  .ufo/waves/round-44/count-c3.py
743996b1…  tools/mori-gate-registry.py
51e63f01…  .ufo/waves/round-44/fixtures/figures-r43.tsv
f37bd18b…  .ufo/waves/round-44/fixtures/mutants/count-c1.py
919bc783…  .ufo/waves/round-44/fixtures/mutants/count-c2.py
27cbed5a…  .ufo/waves/round-44/fixtures/mutants/count-c3.py
f9b1e2bf…  SKILL.md
```
Every hash equals the corresponding line of
`.ufo/waves/round-44/evidence/freeze-r44.txt`. The audited `SKILL.md` is the frozen
`f9b1e2bf…` bytes (the worktree copy is unmodified: `git status` does not list `SKILL.md`).

Two sandboxes were used:

- `/tmp/r44rev.j5RJxg` — `git clone --no-hardlinks` of the lane at `7cb59c68`, plus a copy
  of the fleet census at `/tmp/r44rev.j5RJxg/fleet/scripts/sources-census.sh`, so that the
  documented C3 default `<repo>/../scripts/sources-census.sh` resolves exactly as in the
  fleet. Fixture commits made here are labelled in each finding.
- `/tmp/r44ws.xnw54J` — a second pristine clone used only for the write-scope measurement.

---

## 2. What was checked, per cell

For each row: the entry path resolves at `7cb59c68`; the documented entry command was run and
its exit code and verdict token compared to the verdict-map cell; the documented `--selftest`
was run and its tally compared to the self-test cell; the pinned-values cell's named artifacts
were resolved; the write-scope cell was tested by hashing the whole repository (including
`.git`) before and after the four entry commands and four selftests.

### 2.1 Per-row, per-cell verdict

| cell | C1 (183) | registry (184) | C2 (185) | C3 (186) |
|---|---|---|---|---|
| name | ✓ | ✓ | ✓ | ✓ |
| kind (`gate`) | ✓ | ✓ | ✓ | ✓ |
| entry: path resolves at `7cb59c68` | ✓ | ✓ | ✓ | ✓ |
| entry: documented command runs | ✓ | ✓ | ✓ | ✓ |
| verdict map: 0 | ✓ (met reachable, §3 D6) | ✓ | **✗ documented command prints `C2=unmet`** (D1) | **✗ documented command cannot reach `C3=met`** (D2) |
| verdict map: 1 | ~ absent ledger and row-command timeout are 1 but unlisted (D7) | ~ basename fallback breaks “unregistered path” (D4) | **✗ `--min-arms` inert; failing selftest scored PASS** (D3) | ~ missing census → 1, entry `source:` lack → `entry_meta` (D7); README strictness (D9) |
| verdict map: 2 | ~ usage prints no `C1_SETUP` (D5) | ~ usage prints no `REGISTRY_SETUP` (D5) | ~ usage prints no `C2_SETUP` (D5) | ~ usage prints no `C3_SETUP` (D5) |
| self-test tally | ✓ `C1_SELFTEST pass=6 fail=0` | ✓ `GATE_REGISTRY_SELFTEST pass=6 fail=0` | ✓ `C2_SELFTEST pass=5 fail=0` | ✓ `C3_SELFTEST pass=6 fail=0` |
| self-test arm list | ✓ six named arms match | ✓ six named arms match | ✓ five named arms match | ✓ six named arms match |
| pinned values | ~ default ledger **absent at the measured revision** (D6) | ✓ in-script rows + `SKILL.md` table exist | **✗ default `fixtures/mutants` contradicts the committed location** (D1) | ~ census default and mutant exist; staging shape unstated (D2) |
| write scope | ✓ | ✓ | ✓ | ~ true as written; 0 needs TMPDIR inside the repo (D2) |
| owner (`mori`) | ✓ | ✓ | ✓ | ✓ |

Cell counts are exactly eight with no empty cell, measured with the auditor's own
`CELL_SPLIT`:

```
8 cells | r44 figure ledger (C1)      empty: []
8 cells | r44 gate registry (C2)      empty: []
8 cells | r44 gate conformance (C2)   empty: []
8 cells | r44 corpus coverage (C3)    empty: []
```

Entry-path resolution and registration at the freeze commit:

```
$ for p in .ufo/waves/round-44/count-c1.py .ufo/waves/round-44/count-c2.py \
      .ufo/waves/round-44/count-c3.py tools/mori-gate-registry.py; do
    git cat-file -e 7cb59c68:$p && echo "PRESENT $p"; done
PRESENT .ufo/waves/round-44/count-c1.py
PRESENT .ufo/waves/round-44/count-c2.py
PRESENT .ufo/waves/round-44/count-c3.py
PRESENT tools/mori-gate-registry.py

$ python3 tools/mori-gate-registry.py --rev 7cb59c68 --audit .ufo/waves/round-44/count-c1.py \
    --audit .ufo/waves/round-44/count-c2.py --audit .ufo/waves/round-44/count-c3.py \
    --audit tools/mori-gate-registry.py
audit .ufo/waves/round-44/count-c1.py     PASS (row 'r44 figure ledger (C1)': 8 cells, entry resolves, --selftest present)
audit .ufo/waves/round-44/count-c2.py     PASS (row 'r44 gate conformance (C2)': 8 cells, entry resolves, --selftest present)
audit .ufo/waves/round-44/count-c3.py     PASS (row 'r44 corpus coverage (C3)': 8 cells, entry resolves, --selftest present)
audit tools/mori-gate-registry.py         PASS (row 'r44 gate registry (C2)': 8 cells, entry resolves, --selftest present)
REGISTRY=met
rc=0
```

### 2.2 Self-test tallies — all four cells exact

```
$ python3 .ufo/waves/round-44/count-c1.py --selftest
selftest PASS honest_ledger_met / offbyone_row_mismatch / junk_producer_rejected /
              below_floor_rejected / absent_ledger_unmet / compound_command_rejected
C1_SELFTEST pass=6 fail=0            rc=0

$ python3 tools/mori-gate-registry.py --selftest
selftest PASS registered_row_met / missing_cell_rejected / unresolved_entry_rejected /
              unregistered_path_rejected / no_selftest_rejected / seven_cell_row_rejected
GATE_REGISTRY_SELFTEST pass=6 fail=0  rc=0

$ python3 .ufo/waves/round-44/count-c2.py --selftest
selftest PASS registered_conformant_met / absent_counter_unmet / unregistered_counter_unmet /
              no_selftest_mode_unmet / surviving_mutant_unmet
C2_SELFTEST pass=5 fail=0            rc=0

$ python3 .ufo/waves/round-44/count-c3.py --selftest
selftest PASS registered_entry_met / absent_entry_unmet / row_without_used_by_unmet /
              red_census_unmet / readme_without_row_unmet / missing_coverage_map_unmet
C3_SELFTEST pass=6 fail=0            rc=0
```

The tallies and the arm enumerations in the four self-test cells match these outputs exactly.

### 2.3 Write scope — all four cells hold for the documented invocations

In `/tmp/r44ws.xnw54J`, a full sha256 manifest of **every** file including `.git`
(12 873 files) was taken before and after the four entry commands and the four selftests:

```
$ find . -type f -print0 | sort -z | xargs -0 sha256sum > before.sha
  … eight invocations …
$ find . -type f -print0 | sort -z | xargs -0 sha256sum > after.sha
$ diff before.sha after.sha && echo IDENTICAL
IDENTICAL
$ git status --porcelain          # empty
$ find "$TMPDIR" -mindepth 1      # empty: mkdtemp dirs are removed
```

So “stdout only … nothing in the repo is written” is true for C1, the auditor and C2, and
true as literally worded for C3 (“the registry copy handed to the census is materialized under
the caller TMPDIR”). The C3 caveat in D2 is about the *precondition* for `C3=met`, not about
this sentence being false.

---

## 3. Findings, by severity

### D1 — HIGH — C2 row: the documented entry command cannot print `C2=met`

Cell (entry): `python3 .ufo/waves/round-44/count-c2.py <rev> --counter PATH [--counter PATH ...]`
with `--mutants-dir PATH` listed as an option. Cell (pinned values): “`fixtures/mutants/<basename>`
beside each counter”. Cell (verdict map): “0 `C2=met`”.

Observed, exactly as documented (defaults, at the freeze revision):

```
$ python3 .ufo/waves/round-44/count-c2.py 7cb59c68 \
    --counter .ufo/waves/round-44/count-c1.py \
    --counter .ufo/waves/round-44/count-c2.py \
    --counter .ufo/waves/round-44/count-c3.py
check counters_present   PASS (3 counters)
check registry_rows      PASS (REGISTRY=met)
check tool_selftest      PASS (pass=6 fail=0)
check selftest_tally     PASS (count-c1.py pass=6; count-c2.py pass=5; count-c3.py pass=6)
check mutant_kill        FAIL (count-c1.py mutant absent; count-c2.py mutant absent; count-c3.py mutant absent)
C2=unmet
rc=1
```

Cause: `count-c2.py` defaults `--mutants-dir` to `fixtures/mutants`, which `read_at()` resolves
**repo-relative at the measured revision** — and `<repo>/fixtures/mutants` does not exist in any
commit:

```
$ git ls-tree -r --name-only 7cb59c68 | grep -c '^fixtures/'
0
$ git ls-tree -r --name-only 7cb59c68 | grep 'fixtures/mutants'
.ufo/waves/round-44/fixtures/mutants/count-c1.py
.ufo/waves/round-44/fixtures/mutants/count-c2.py
.ufo/waves/round-44/fixtures/mutants/count-c3.py
$ git log --all --oneline -- 'fixtures/mutants'      # empty
```

With the path the pinned cell actually names, the gate is green:

```
$ python3 .ufo/waves/round-44/count-c2.py 7cb59c68 --counter …count-c1.py --counter …count-c2.py \
    --counter …count-c3.py --mutants-dir .ufo/waves/round-44/fixtures/mutants
check mutant_kill        PASS (count-c1.py killed (fail=1); count-c2.py killed (fail=1); count-c3.py killed (fail=1))
C2=met
rc=0
```

Mismatch: the row's own pinned-values cell contradicts the tool's default, and the documented
entry command therefore terminates in the row's documented **1** branch at every revision,
including a landed tip. The contract's After command
(`python3 .ufo/waves/round-44/count-c2.py <landed tip>`) is in the same position: it omits both
`--counter` and `--mutants-dir`. This is routed-defect-4 class: the row does not describe the
tool as it behaves. Independently recorded by `w1/SimpCounters.md` §8.3.

### D2 — HIGH — C3 row: `C3=met` is unreachable under the documented command

Cell (entry): `python3 .ufo/waves/round-44/count-c3.py <rev> --entry PATH --row S### …`; cell
(verdict map): “0 `C3=met`”; cell (pinned values): “`--census` default
`<repo>/../scripts/sources-census.sh`”.

With **every** C3 artifact in place — admitted entry, `S471`/`S472` mined with `used-by` naming
it, README row, the default census script — the documented command fails its own census check:

```
$ env -u TMPDIR python3 .ufo/waves/round-44/count-c3.py WORK \
    --entry corpus/knowledge/pid-probe-conclusion-r44.md --row S471 --row S472
check entry_present    PASS (5526 bytes)
check entry_meta       PASS (sources S471,S472)
check rows_present     PASS (rows S471,S472 mined)
check census_ok        FAIL (exit=1)
check readme_row       FAIL (no line names the entry)
C3=unmet
rc=1
```

Mechanism, measured directly. `count-c3.py:135-140` stages the registry at
`<mkdtemp>/SOURCES.md` and runs `bash <census> validate --file <that path>`. The census resolves
the registry's lane root as `realpath(dirname(file)/..)` (`scripts/sources-census.sh:501`),
so the lane root becomes `TMPDIR`, and rule E11 then demands every `mined` row's `used-by` path
under `TMPDIR`:

```
$ mkdir /tmp/c3probe && cp corpus/SOURCES.md /tmp/c3probe/SOURCES.md
$ bash …/sources-census.sh validate --file /tmp/c3probe/SOURCES.md
    279 E11
     19 W04
rc=1

$ bash …/sources-census.sh validate --file /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
file	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
rc=0
```

The gate does turn green when `TMPDIR` is the repository root (so that `TMPDIR/corpus/…` exists),
and only then:

```
$ TMPDIR="$PWD" python3 .ufo/waves/round-44/count-c3.py WORK --entry … --row S471 --row S472
check census_ok        PASS (exit=0)
check readme_row       FAIL (no line names the entry)      # see D9
C3=unmet

# same run with a README row naming the literal repo-relative path:
$ TMPDIR="$PWD" python3 .ufo/waves/round-44/count-c3.py WORK --entry … --row S471 --row S472
check census_ok        PASS (exit=0)
check readme_row       PASS (names entry)
C3=met
rc=0
```

That precondition is nowhere in the row, and it makes the tool write **inside the repository**
(transiently, then removed) — demonstrated with a census stub that sleeps:

```
$ TMPDIR="$PWD" python3 .ufo/waves/round-44/count-c3.py WORK … --census /tmp/slow-census.sh &
$ ls -d "$PWD"/c3-*        # while it runs
/tmp/r44rev.j5RJxg/fleet/mori-shokunin/c3-6wbgf6ni
/tmp/r44rev.j5RJxg/fleet/mori-shokunin/c3-6wbgf6ni/SOURCES.md
# after exit: none left
```

Mismatch: the row's 0 branch is not reachable by the command it documents; the write-scope cell
omits the TMPDIR-inside-the-repo condition that the verdict depends on. Correction to
`w1/ScribeFrontierRow.md` X1 (“`C3=met` is unreachable … regardless of what lands”): it *is*
reachable, but only with `TMPDIR` set to a directory that contains the lane's `corpus/`, i.e. the
repo root — never with the default `TMPDIR`.

Artifacts used for this probe (live worktree at review time, uncommitted and moving):
`corpus/SOURCES.md` `d1381d4f…`, `corpus/README.md` `4fd32db3…`,
`corpus/knowledge/pid-probe-conclusion-r44.md` `0b89bdf2…`.

### D3 — HIGH — C2 row: `--min-arms` is inert and a failing selftest is scored as a tally

Cell (entry) documents `--min-arms N`; cell (verdict map) assigns “no selftest tally” to **1**.

```
$ python3 .ufo/waves/round-44/count-c2.py WORK --counter …count-c1.py --counter …count-c2.py \
    --counter …count-c3.py --mutants-dir .ufo/waves/round-44/fixtures/mutants --min-arms 99
check selftest_tally     PASS (count-c1.py pass=6 fail=0; count-c2.py pass=5 fail=0; count-c3.py pass=6 fail=0)
check mutant_kill        PASS (…)
C2=met
rc=0
```

No counter reaches 99 arms, yet the gate is green: the documented floor cannot make it fail.
The same root cause scores a counter whose own selftest **exits 1 with `fail=1`** as conformant:

```
$ python3 .ufo/waves/round-44/count-c2.py WORK \
    --counter .ufo/waves/round-44/fixtures/mutants/count-c1.py \
    --mutants-dir .ufo/waves/round-44/fixtures/mutants
check selftest_tally     PASS (count-c1.py pass=5 fail=1)
check mutant_kill        PASS (count-c1.py killed (fail=1))
C2=met
rc=0
```

Cause: `count-c2.py:185` — `record("selftest_tally", all(" pass=" in t for t in tallies), …)` —
both the good entry (`"<name> pass=%d"`) and the bad entry (`"<name> pass=%d fail=%d"`, which is
also what the below-floor branch emits) contain `" pass="`. Only `absent` and `no tally` can fail.
Root cause independently found by `w1/CritSelftestHonesty.md` §“Strongest evasion found”; the
row-level consequence is mine: the row advertises an option and a cause that the counter cannot
honour.

### D4 — MEDIUM — registry row: a different file sharing a registered basename is “registered”

Cell (verdict map): “1 `REGISTRY=unmet` (unregistered path, …)”.

```
$ python3 tools/mori-gate-registry.py --rev 7cb59c68 \
    --audit .ufo/waves/round-44/fixtures/mutants/count-c1.py
audit .ufo/waves/round-44/fixtures/mutants/count-c1.py PASS (row 'r44 figure ledger (C1)': 8 cells, entry resolves, --selftest present)
REGISTRY=met
rc=0
```

No row names that path. `mori-gate-registry.py:122-126` falls back to a substring match on the
basename when no row invokes the exact path, and then checks resolution of the *target*, not of
the row's entry. A committed mutant of a registered counter therefore passes as registered — and
`count-c2.py`'s `registry_rows` check inherits this (D3 run above: `registry_rows PASS
(REGISTRY=met)` for the mutant path). Corroborated by `w1/MutRegistry.md` probes 2b/3b/3c
(SURVIVED fixtures).

### D5 — MEDIUM — all four rows: the documented exit-2 token is absent for the usage sub-case

Cells: “2 `C1_SETUP` (usage, …)”, “2 `REGISTRY_SETUP` (usage, …)”, “2 `C2_SETUP` (usage, …)”,
“2 `C3_SETUP` (usage, …)”.

```
$ python3 .ufo/waves/round-44/count-c1.py
usage: count-c1.py <rev|WORK> [--repo PATH] [--ledger PATH] [--selftest]
rc=2
$ python3 tools/mori-gate-registry.py
usage: mori-gate-registry.py --rev <rev|WORK> --audit <path> [...] [--selftest]
rc=2
$ python3 .ufo/waves/round-44/count-c2.py
usage: count-c2.py <rev|WORK> --counter PATH [--counter PATH ...] [--selftest]
rc=2
$ python3 .ufo/waves/round-44/count-c3.py
usage: count-c3.py <rev|WORK> --entry PATH --row S### [--row S### ...] [--selftest]
rc=2
```

The exit code is right; the named token is not printed. Every other 2 cause does print it
(`C1_SETUP cannot resolve revision 'deadbeef'`, `REGISTRY_SETUP registry absent at 7cb59c68…`,
`REGISTRY_SETUP no gate table with a name/kind header in corpus/README.md`,
`C2_SETUP cannot resolve revision 'deadbeef'`, `C3_SETUP cannot resolve revision 'deadbeef'`).
A harness that greps the documented token sees no match on the usage branch.

### D6 — MEDIUM — C1 row: the pinned default ledger does not exist at the measured revision

Cell (pinned values): “ledger bytes at the measured revision (default
`.ufo/waves/round-44/figures.tsv`)”. The cell names three artifacts; two exist and one does not:

```
$ git cat-file -e 7cb59c68:.ufo/waves/round-44/figures.tsv          → ABSENT
$ git cat-file -e 7cb59c68:.ufo/waves/round-44/fixtures/figures-r43.tsv → PRESENT
$ git cat-file -e 7cb59c68:.ufo/waves/round-44/fixtures/mutants/count-c1.py → PRESENT
```

Consequence for the documented command at the measured revision:

```
$ python3 .ufo/waves/round-44/count-c1.py 7cb59c68
check ledger_present       FAIL (absent)
ledger=.ufo/waves/round-44/figures.tsv rows=0 classes=-
C1=unmet mismatches=?
rc=1
```

This is expected to close when the C1 deliverable lands (the ledger is the round's C1 artifact),
so it is a mid-round state rather than a row error; but at the revision the row names, its 0
branch is unreachable. The 0 branch itself is correct — a committed honest 12-row/5-class ledger
in the sandbox printed `C1=met mismatches=0` rc 0, and the witness fixture printed
`C1=unmet mismatches=2` naming `F03 asserted=15 observed=14; F04 asserted=34 observed=8`,
exactly as the contract's P-C1 witness requires.

### D7 — LOW — verdict-map cause lists are incomplete

Each of these is a 1-branch cause the cells do not enumerate:

| row | cause observed | output |
|---|---|---|
| C1 | absent ledger | `check ledger_present FAIL (absent)` → `C1=unmet` rc1 (cell lists only mismatch/floor) |
| C1 | row-command timeout | `--timeout 0` → `check commands_reconcile FAIL (F01 <- timeout after 0s; …)` → `C1=unmet mismatches=12` rc1 (cell puts “git timeout” under 2) |
| C2 | absent mutant | `check mutant_kill FAIL (… mutant absent)` → `C2=unmet` rc1 (cell lists only “a mutant its own selftest cannot catch”) |
| C3 | missing `--census` file | `check census_ok FAIL (exit=127)` → `C3=unmet` rc1 (setup-shaped, reported as 1) |
| C3 | entry omits a declared `source:` line | `check entry_meta FAIL (source: lacks S472)` (cell lists only verified-at/recheck/coverage-map) |

The `C1` timeout row is the one that actually contradicts the cell's grouping: only `git()`
calls (30 s, fixed) raise `Setup`; the per-row subprocess timeout is a mismatch, i.e. 1.

### D8 — LOW — C1 prints a PASS for reconciliation it never performed

On a rejected ledger (`echo 3` producer), `commands_reconcile` is recorded green because the
reconciliation loop is skipped when `problems` is non-empty:

```
check ledger_present       PASS (66 bytes)
check rows_parse           FAIL (row 1: command is not a git pipeline; row 1: command does not name @REV@; row 1: command carries a non-byte producer)
check row_floor            PASS (rows=2 min=1)
check class_floor          FAIL (classes=registry,wave min=4)
check commands_reconcile   PASS (all rows match)
ledger=.ufo/waves/round-44/figures.tsv rows=2 classes=registry,wave
C1=unmet mismatches=?
rc=1
```

The verdict (`C1=unmet mismatches=?`) is correct and matches “rejected, never scored”, but the
check line claims a reconciliation that did not happen.

### D9 — LOW — C3 `readme_row` is stricter than the cell's wording

Cell: “no README map row”. Tool: `entry.encode() in readme_body`, i.e. the literal
repo-relative path must appear. The live worktree README names the entry as
`knowledge/pid-probe-conclusion-r44.md` (`corpus/README.md:632`), so:

```
check readme_row       FAIL (no line names the entry)
```

A frontier row that names the entry in the corpus's own house style fails the check. (Same
artifact defect as `w1/ScribeFrontierRow.md` X2; the row-cell mismatch is that the cell
describes the requirement more loosely than the tool enforces it.)

### D10 — LOW — option lists omit real options

C1's entry cell omits `--timeout S`; C2's and C3's omit `--repo PATH` and `--timeout S`; all
four accept `WORK` as well as `<rev>` without saying so. Cosmetic, but the same class as D1:
the row is not a complete description of the command it names.

---

## 4. What holds (green, measured)

- Eight non-empty standard cells in all four rows; header at `SKILL.md:162` is exactly
  `| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |`.
- All four entry paths resolve at `7cb59c68`; the auditor returns `REGISTRY=met` rc 0 for all four.
- All four selftest tallies and arm lists match their cells exactly (§2.2).
- Write scope holds for all four documented invocations: whole-repo (including `.git`) hash
  identical, `git status` clean, `TMPDIR` emptied (§2.3).
- C1: 0 branch (`C1=met mismatches=0`), 1 branch with the frozen witness
  (`C1=unmet mismatches=2`, F03/F04), junk-producer rejection (`mismatches=?`), and the
  row/class floors (`--min-rows 13` → `row_floor FAIL` → rc 1) all behave as documented.
- registry: 0 (`REGISTRY=met`), 1 for unregistered path, blank cell and unresolved entry, and
  2 for unresolvable revision, absent registry and absent gate table all behave as documented:
  ```
  audit …count-c1.py FAIL (row 'r44 figure ledger (C1)' missing cells: pinned values)   REGISTRY=unmet rc1
  audit tools/ghost-registry.py FAIL (row 'r44 gate registry (C2)' entry path does not resolve at c49cc8551ecd)  REGISTRY=unmet rc1
  REGISTRY_SETUP registry absent at 7cb59c68…: NOPE.md                                   rc2
  REGISTRY_SETUP no gate table with a name/kind header in corpus/README.md               rc2
  ```
- C2: with the pinned mutants path, `C2=met` rc 0; each committed mutant is killed by its own
  counter (`fail=1`, rc 1) and each disables exactly one check (`row_floor`, `mutant_kill`,
  `census_ok` respectively).
- C3: 0 branch reachable and green under `TMPDIR=<repo>` with a README row naming the full path;
  1 for entry absent; 2 for unresolvable revision.
- The registry's `--selftest` writes only under the caller's `TMPDIR`; `MORI_GATE_REGISTRY` is
  present in the source and is what plumbs the auditor into fixture copies.

---

## 5. Residual risk

- **The C2 gate's `mutant_kill` proves disagreement, not detection.** It accepts any red
  selftest (`CritSelftestHonesty.md` probes D/E); a mutant whose selftest is red for an
  unrelated reason is scored as killed. Combined with D3, a counter could pass C2 while its own
  selftest is failing.
- **The registry auditor's identity check is substring-based** (D4). Every row that matches only
  by basename inherits the same weakness, so “registered” is weaker than the cell claims even
  for honest paths with common basenames.
- **C3's verdict depends on ambient `TMPDIR`.** Two operators running the documented command
  with different `TMPDIR` values get different verdicts on identical bytes (D2). If the round's
  C3 evidence is produced with `TMPDIR=<repo>`, the recorded command must show it, or the
  receipt does not reproduce.
- **The live C3 artifacts are uncommitted and moving.** D9's `readme_row` observation is against
  the snapshot hashed in §3 D2; if the README row is rewritten to name the full path, D9's
  artifact half disappears while the row-cell mismatch remains.

## 6. Verification gaps

- **Git timeout (exit 2) not exercised.** `git()` uses a fixed 30 s with no injection point;
  the row's “git timeout” clause is unverified in the 2 direction. The measurable timeout — the
  per-row subprocess — is a 1 (D7).
- **“No `--selftest` mode” for the registry row** was verified only through the auditor's own
  selftest arm. No real repo path lacks the flag; the audit's test is the byte substring
  `b"--selftest" in body`, so a tool that merely mentions the flag would pass (unexercised).
- **C2's `unregistered` and `no --selftest` arms** are fixture-only; no real counter in the lane
  is unregistered, so those 1-branch causes were not reproduced on a real path.
- **`C1`'s `class_floor`** was exercised only as a failure (`--min-classes` default 4 with a
  two-class ledger); the pass side is covered by the honest-ledger probe.
- **The C3 0-branch probe** used the real census with a sandbox README line appended by me; the
  entry, registry rows and README row in the live tree are a sibling's uncommitted work, not a
  landed revision.
- **Sibling overlap:** D1 is also in `SimpCounters.md` §8.3, D3's root cause in
  `CritSelftestHonesty.md`, D4 in `MutRegistry.md`, D9's artifact half in
  `ScribeFrontierRow.md` X2. D2's refinement (reachable only with `TMPDIR` = repo root, and the
  transient repo write) is the part not previously measured.
