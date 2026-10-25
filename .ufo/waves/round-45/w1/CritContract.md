# CritContract — falsification of the round-45 frozen contract

Seat: critic (leaf; no subagent). Scope: `.ufo/waves/round-45/contract.md` at the freeze
commit `3ad8faaa` (entering tip `554ff416459c92f0dea9762f834a556df2990187`). I edited no
lane file. Every verdict below quotes the contract line and carries a measured command with
its `rc`. File is byte-identical to the freeze commit (`git diff --stat 3ad8faaa --
.ufo/waves/round-45/contract.md` → empty, rc 0), so the frozen text I judge is the text the
lane will score.

## 0. Verdict matrix

| claim | (a) do-nothing control | (b) one sentence, code=label | (c) one value / one command / committed bytes | (d) causally separable | (e) names the surface | (f) universal enumerated |
|---|---|---|---|---|---|---|
| C1 | **FALSIFIED** | **FALSIFIED** | **FALSIFIED** | **FALSIFIED** | PARTIAL | **FALSIFIED** |
| C2 | **FALSIFIED** | **FALSIFIED** | **FALSIFIED** | **FALSIFIED** | **FALSIFIED** | **FALSIFIED** |
| C3 | **FALSIFIED** | **FALSIFIED** | **FALSIFIED** | HOLDS | **FALSIFIED** | **FALSIFIED** |

| contract section | verdict |
|---|---|
| Kill rules (L79–88) | **FALSIFIED** — 2 of the 3 entering-tip receipts print `met` (measured) |
| Floors and knobs (L90–95) | HOLDS (testable; r44 did not clamp, so the clamp is a real change) |
| Frozen instruments (L97–101) | **FALSIFIED** — manifest absent at the freeze commit and unsatisfiable as written |
| Claims are causally separable (L103–109) | C1 **FALSIFIED**, C2 **FALSIFIED**, C3 HOLDS |

Contract line numbering used throughout is `grep -n '' .ufo/waves/round-45/contract.md`.

---

## 1. C1 — the ledger predicate

Claim line (L13): *"the round's ledger gate stops being vacuous: a committed ledger must be
revision-sensitive, its rows distinct, and each named vacuity witness must be **rejected**"*.

### (a) A do-nothing control meets it — FALSIFIED

Two controls, both cheaper than the round's work.

**Control 1 — the entering-tip receipt prints `met`.** L81–82 states *"A do-nothing control
at the entering tip prints `C1=unmet` … (the three entering-tip receipts)"*. The only C1
instrument that exists at the entering tip is r44's counter:

```
$ TMPDIR=$PWD/.ufo/waves/round-45/tmp/CritContract \
  python3 .ufo/waves/round-44/count-c1.py 554ff416459c92f0dea9762f834a556df2990187
check ledger_present       PASS (1321 bytes)
check rows_parse           PASS (16 rows)
check row_floor            PASS (rows=16 min=12)
check class_floor          PASS (classes=checks,corpus,evidence,registry,wave min=4)
check commands_reconcile   PASS (all rows match)
rev=554ff416459c92f0dea9762f834a556df2990187
ledger=.ufo/waves/round-44/figures.tsv rows=16 classes=checks,corpus,evidence,registry,wave
C1=met mismatches=0
rc=0
```

The round's own receipt agrees byte-for-byte: `.ufo/waves/round-45/evidence/control-r44-c1.txt`
ends `C1=met mismatches=0 / rc=0` (instrument sha256 `9477824d…`, run 2026-10-25T07:41:50).
So the header claim of the kill-rule section is already false for C1 at the moment of freeze,
under the only instrument the entering tip has. The contract never disambiguates which
instrument constitutes "the do-nothing control"; the two readings give opposite verdicts
(r44 counter → `met`, r45 counter → does not exist at the entering tip).

**Control 2 — the `CONST=` escape admits the exact ledger the kill rule forbids.**
L25–26: *"the row declares either a value that **differs** between the measured revision and
`--other-rev`, or `CONST=<reason>`"*. L83–84: *"a ledger of revision-constant figures … must
not print `C1=met`"*. These two sentences contradict each other. A 12-row, 4-class ledger of
revision-constant `git show @REV@:<file> | wc -l` rows, each carrying `CONST=<reason>`, is
admissible under L23–26 (rows distinct, commands distinct, each row "declares … CONST="),
passes `mismatches=0` because no numeric value is declared to compare, and is a "ledger of
revision-constant figures" that L83–84 says must not print `met`. Nothing in the contract
caps the number of `CONST=` rows. That is the cheapest control that skips the whole
revision-sensitivity capability: 12 mechanical rows + a reason string.

Second vacuity hole in the same arm: L33–35 requires *"every ledger in `--witness-dir` is
**rejected** (`witnesses=<n>/<n>`)"*. With `<n>=0` the universal is vacuous — an empty
`--witness-dir` yields `0/0`. The contract sets no floor on `n` and does not require the
three named classes (L39–42: `W-REVCONST`, `W-HEAD`, `W-DUP`) to be *present*, only that
whatever is present is rejected. Cheapest: `mkdir empty; count-c1.py <rev> --ledger <admissible>
--witness-dir empty --other-rev <rev2>` → `witnesses=0/0`.

### (b) One sentence the code and the label can state identically — FALSIFIED

The frozen sentence (L23) is *"every row is one `git` pipeline naming `@REV@`"*. The bytes
that will enforce it are r44's parser plus the round's additions. r44:85–104 enforces, beyond
the sentence: exactly 4 TSV cells; `id` matching `^F\d{2,3}$` (L29); an integer asserted value
(`DIGITS`, L30); a **read-verb allowlist** `{"show","grep","ls-tree","rev-list","cat-file",
"log","diff"}` (L28); no `;`/`&&`; no `echo|printf|true` producer. The frozen sentence states
none of these, and `diff` is in the allowlist today while `ExecLedgerCounter` says *"drop
`diff` from the read-verb allowlist"* — i.e. the item that builds the instrument enforces a
rule the frozen predicate does not contain.

Conversely the frozen sentence admits what it should not: `git show @REV@:f | tee
/home/vgpnk/pwned` is one `git` pipeline naming `@REV@` and satisfies L23; so is
`git show @REV@:f | sh` (the `sh` verb is in the pipe's second stage, which no clause
restricts), and `$(...)`/backticks are not excluded by L23–26. The counter must either
enforce more than the frozen text (then the report's "admissible" label is a different
predicate) or enforce exactly it (then the ledger can write outside the repo). There is no
sentence both the code and the report can state.

Third ambiguity in the same sentence: where does `CONST=<reason>` live? The r44 shape is
`id\tclass\tcommand\tvalue` (4 cells, `count-c1.py:85`) with `asserted` required to be
`^\d+$` (`:90–91`). Nothing in the contract says which cell carries `CONST=`, and
`grep -n CONST .ufo/waves/round-44/count-c1.py` → no match (rc 1): the r44 instrument has no
such concept, so the executor must invent a row shape the contract does not freeze.

### (c) One concrete value, one command, over committed bytes — FALSIFIED

- The ledger is **not named** anywhere in P-C1. L28–35 says "the ledger"; `ExecLedgerCounter`
  says "start from round-44's", whose `--ledger` default is
  `.ufo/waves/round-44/figures.tsv` (`count-c1.py:297`); `ExecFiguresLedger` delivers
  `.ufo/waves/round-45/figures.tsv.draft` with *"no final values asserted yet"*. No wave item
  commits a final `.ufo/waves/round-45/figures.tsv`. So the object the after-value measures
  does not exist at the freeze and is not owned by any seat.
- `--other-rev` is **not frozen**. It is the free variable that decides admissibility, and it
  decides it completely. I recomputed every r44 row at `554ff416…` and at `b1d7269`
  (`bash -o pipefail -c` per row, all rc 0):

  | row | declared | @554ff416 | @b1d7269 | verdict |
  |---|---|---|---|---|
  | F01 | 245 | 245 | 245 | CONSTANT |
  | F02 | 2 | 2 | 2 | CONSTANT |
  | F03 | 3 | 3 | 3 | CONSTANT |
  | F04 | 54 | 54 | 54 | CONSTANT |
  | F05 | 119 | 119 | 119 | CONSTANT |
  | F06 | 3 | 3 | 3 | CONSTANT |
  | F07 | 4 | 4 | 4 | CONSTANT |
  | F08 | 72 | 72 | 72 | CONSTANT |
  | F09 | 10 | 10 | 10 | CONSTANT |
  | F10 | 8 | 8 | 8 | CONSTANT |
  | F11 | 14 | 14 | 14 | CONSTANT |
  | F12 | 32 | 32 | 32 | CONSTANT |
  | F13 | 4 | 4 | 4 | CONSTANT |
  | F14 | 8 | 8 | 8 | CONSTANT |
  | F15 | 73 | 73 | **74** | moves |
  | F16 | 15 | 15 | 15 | CONSTANT |

  15 of 16 honest rows are revision-constant across exactly the pair `ExecWitnesses` uses for
  the `W-REVCONST` witness (`554ff416` ↔ `b1d7269`). And F15 moves only because the r44
  *verifier's* commit `b1d7269` added a lesson file — i.e. the one "revision-sensitive" figure
  is sensitive to a neighbouring seat's commit, not to the round's work. Pick a distant
  `--other-rev` and everything "moves"; pick an adjacent one and a new ledger cannot reach 12
  moving rows without contrivance. The after-value is a function of a knob the contract leaves
  free, so it is not "one concrete value one command re-derives".
- `witnesses=<n>/<n>` is a *shape*, not a value (see (a)).

### (d) Causally separable — FALSIFIED

L105: *"C1 lands and verifies with C2/C3 untouched (its counter, witnesses, ledger)."*
The round's own ledger catalogue (`ExecFiguresLedger`, read from
`.ufo/waves/round-45/w1-spec.json`) instructs the ledger to catalogue
*"the unregistered count from the r44 inventory"* and *"the count of `--selftest`-capable
tools"*. Both numbers are **changed by C2's own work** this wave (three new registry rows, and
three added `--selftest` branches). A C1 ledger asserting them cannot verify "with C2
untouched": its asserted values move when C2 lands. The ledger also carries
*"the count of `--selftest`-capable tools"*, which changes precisely at
`ExecSelftestModes`'s commit. C1 is therefore order-coupled to C2 through its own row set.

### (e) Names the surface, not the number — PARTIAL

The claim text (L13) does name the surface ("the round's ledger gate stops being vacuous").
The predicate (L28–35) names only numbers: `mismatches=0`, `witnesses=<n>/<n>`, a passed
selftest. Nothing in P-C1 names the admission rule it moves; a reader of the verdict line
cannot tell whether the gate's *admissibility* or its *arithmetic* changed.

### (f) Universal clause without enumeration — FALSIFIED

- L33–35 *"every ledger in `--witness-dir`"*: no enumeration, no count floor, no required class
  set (the classes of L39–42 are declared but never required to be present).
- L31 *"every declared value"*: no list of values; `CONST=` rows declare none.
- L23 *"every row is one `git` pipeline"*: no definition of a pipeline's permitted stages.

---

## 2. C2 — the registry predicate

Claim line (L14): *"the lane's gate registry stops overstating: one audit over **every**
registry table in `SKILL.md` attributes each audited path to the row that names it, rejects
duplicate rows, requires a real `--selftest` argv branch, and reports `unregistered=0` over the
whole declared population"*.

### (a) A do-nothing control meets it — FALSIFIED (measured, twice)

**Control 1 — the entering-tip C2 receipt already prints `met`.** L81–82 says it must print
`C2=unmet`. The round's own receipt `.ufo/waves/round-45/evidence/control-r44-c2.txt`, run B,
at the entering tip:

```
check counters_present   PASS (3 counters)
check registry_rows      PASS (REGISTRY=met)
check tool_selftest      PASS (pass=6 fail=0)
check selftest_tally     PASS (count-c1.py pass=6; count-c2.py pass=5; count-c3.py pass=6)
check mutant_kill        PASS (count-c1.py killed (fail=1); …)
C2=met
rc=0
```

Run A in the same file prints `C2=unmet` only because `count-c2.py:355`'s default
`--mutants-dir fixtures/mutants` is repo-root-relative while the mutants live at
`.ufo/waves/round-44/fixtures/mutants` — a *mispath*, not the defect C2 claims to fix. I
reproduced both: with `--mutants-dir .ufo/waves/round-44/fixtures/mutants` → `C2=met rc=0`;
without → `C2=unmet rc=1` with `mutant_kill FAIL (… mutant absent)`. A kill rule whose
entering-tip failure is caused by an absent fixture cannot detect an overstated registry.

And the overstatement itself is *green* at the entering tip: the same run shows
`registry_rows PASS (REGISTRY=met)` while v1 reads only the first table
(`tools/mori-gate-registry.py:113–132`, `parse_gate_table`, returns one header+rows). Measured
counterexample: `python3 tools/mori-gate-registry.py --rev 554ff416 --audit
tools/mori-source-drift.py` → `REGISTRY=unmet (unregistered: no row names
mori-source-drift.py)`, although row 883 `source drift (r36)` and row 886 `source drift (r37)`
both name that path — v1's registry arm says `met` and its population arm says `unregistered`.

**Control 2 — a caller-chosen population prints `unregistered=0`.** L56–58 says *"the whole
declared population (`tools/*.py`, `tools/*.sh`, and the round counters …) audits
`unregistered=0`"*, but nothing requires the population to be derived rather than supplied.
v1's CLI is `--audit PATH` repeatable (`:302`), and `--audit-all` does not exist
(`python3 tools/mori-gate-registry.py --rev 554ff416 --audit-all` → argparse
`error: unrecognized arguments: --audit-all`, rc 2). So

```
python3 tools/mori-gate-registry.py --rev 554ff416 --audit tools/mori-census.sh
```

prints `REGISTRY=met` / `unregistered=0` and satisfies L56–58 as written — the whole declared
population was not audited, but no clause forbids that.

### (b) One sentence, code and label identical — FALSIFIED

Five numbers over four scopes and no statement of scope:
`tables=<n>` over *tables*; `duplicate=<n>` over *row names*; `unregistered=<n>` over
*population files*; `no_selftest=<n>` over **either** population files **or** rows whose cell
claims a selftest; `writescope_mismatch=<n>` over *fixture entries*. The `no_selftest` reading
is decidable by the bytes and the two answers differ at the landed tip. Population files with
no `--selftest` argv branch today (byte scan of `add_argument("--selftest"` / a real `case`
arm, 2026-10-25):

```
NONE  tools/mori-silence-cases.sh      (only a comment mentions it: `:20` "…no --selftest)…")
NONE  tools/mori-disk-rate.py          (0 occurrences of `selftest`)
NONE  tools/mori-round19-regressions.py(0 occurrences)
NONE  tools/mori-round41-calibration.py(0 occurrences)
NONE  tools/mori-routed-check.py       (0 occurrences)
NONE  tools/mori-routed-r24.py         (only an evidence path for mori-pressure.py)
```

`ExecSelftestModes` gives branches to exactly three of these (silence-cases.sh,
round19-regressions.py, routed-check.py). Left without a branch: `mori-disk-rate.py`,
`mori-round41-calibration.py`, `mori-routed-r24.py`. So under the literal file-property
reading `no_selftest=3` at the landed tip; under the row-claiming reading it is `0` today and
the check cannot distinguish a selftested population from one that honestly lacks selftests.
The contract cannot state which, so the code and the report cannot state the same sentence.

### (c) One concrete value, one command, committed bytes — FALSIFIED

- Four zero-targets plus a free `tables=<n>`. L48 *"(`tables=<n>`, not 1)"* forbids exactly
  one value. **There are 7 eight-cell registry tables in `SKILL.md`** — header lines
  162, 524, 588, 643, 718, 796, 881 (`grep -n "^| name | kind |"`), holding 43 rows. An
  auditor that reads two tables prints `tables=2` and satisfies "not 1" while missing five
  tables. The target "every table" has no expected value.
- `duplicate=0` is achievable — no duplicate row names exist today (my parse of all 43 rows:
  zero repeats). Fine.
- Item 6's fixture path is wrong. L59–60: *"the write-scope arm's `writescope_mismatch` is 0
  against `fixtures/write-scope.json`"*. That path does not exist:
  `ls fixtures/` → `No such file or directory` (rc 2); `git ls-tree --name-only 554ff416 |
  grep -x fixtures` → no match (rc 1). The wave builds it at
  `.ufo/waves/round-45/fixtures/write-scope.json` (`ExecWriteScopeFixture`, and it exists
  there now as an untracked file). The frozen path and the built path differ, so the arm as
  frozen reads an absent fixture → `C2_SETUP`/unmet, never `writescope_mismatch=0`.
- The population is also defined by *worktree* glob but must be measured *at `--rev`*
  (L46). `.ufo/waves/round-45/count-c*.py` does not exist at the entering tip (33 files) and
  will exist at the landed tip (36). Glob and `--rev` disagree unless the contract says the
  population is `git ls-tree -r --name-only <rev>`; it does not.

### (d) Causally separable — FALSIFIED

L106: *"C2 lands and verifies with C1/C3 untouched"*. C2's own population is
*"the round counters `.ufo/waves/round-4[45]/count-c*.py`"* (L56–57) — including C1's
`count-c1.py` and C3's `count-c3.py`, which do not exist until C1 and C3 land, and must be
registered by a row with a real `--selftest`. C2's write-scope fixture is defined over the
same round counters (`ExecWriteScopeFixture`). So C2 = unmet until C1 and C3 instruments
exist and are registered: a strict ordering dependency, not separability.

### (e) Names the surface, not the number — FALSIFIED

The claim text names the surface ("the lane's gate registry stops overstating"); the predicate
is four counters. Worse, `no_selftest=0` measures a property of *tools*, which is not
"registry overstatement" at all — the lane can satisfy it by adding branches and leave every
overstated row untouched.

### (f) Universal without enumeration — FALSIFIED

- L47 *"**every** registry table in `SKILL.md`"* — seven exist; no expected `n`; L48 accepts
  any `n ≠ 1`.
- L56 *"the whole declared population"* — no enumeration file and no derivation requirement.
- L49 *"every audited path is attributed to the row **that names it**"* presumes a unique
  naming row. The committed registry has five population paths named by 2–4 rows each
  (escape-aware parse of the 7 tables):

  | path | naming rows (line:name) |
  |---|---|
  | `tools/mori-census.sh` | 164:census, 165:drift pin, 168:r14 regressions, 169:r15 regressions |
  | `tools/mori-evidence-loss.py` | 526:retained-loss audit, 527:evidence-loss rule comparison |
  | `tools/mori-journal-window.py` | 170:r16 regressions, 172:journal window (r16) |
  | `tools/mori-source-drift.py` | 883:source drift (r36), 886:source drift (r37) |
  | `tools/mori-sources-appendonly.py` | 884:SOURCES append-only (r36), 893:SOURCES append-only timing (r38) |

  v1 resolves the ambiguity by sorting on entry length (`:127`,
  `sorted(matches, key=lambda r: len(r[2]))[0]`) — a tie-break, not "the row that names it".
  L52's `duplicate=0` counts *names*, so it cannot see this. The frozen predicate is
  undecidable for these five paths and silently picks the shortest cell.

---

## 3. C3 — the assimilation predicate

Claim line (L15): *"shokuknow assimilation, level-naming theme: one admitted entry grounded in
a source this lane opened, one `mined` row whose `used-by` names it, a census-green registry
reached **without** a `TMPDIR` override, and a README coverage-map row"*.

### (a) A do-nothing control meets it — FALSIFIED

Every sub-condition except the counter's own census arm is already true at the entering tip,
with the **r44** entry and row. Measured, r44 counter, correct flags:

```
$ TMPDIR=$PWD/.ufo/waves/round-45/tmp/CritContract \
  python3 .ufo/waves/round-44/count-c3.py 554ff416… \
    --entry corpus/knowledge/pid-probe-conclusion-r44.md --row S472 \
    --census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
check entry_meta       PASS (sources S471,S472)
check rows_present     PASS (rows S472 mined)
check census_ok        FAIL (exit=1)
check readme_row       PASS (names entry)
C3=unmet
rc=1
```

So items 1, 2 and 4 of P-C3 are satisfied by committed r44 bytes:
`corpus/knowledge/pid-probe-conclusion-r44.md:3-7` carries `source:` ×2, `verified-at:`,
`recheck:`, `coverage-map:`; `corpus/SOURCES.md:251` (S472) is `mined` with `used-by
corpus/knowledge/pid-probe-conclusion-r44.md`; `corpus/README.md:639` names the entry.
And item 3 is *already* satisfied by doing nothing:

```
$ env -u TMPDIR timeout 120 bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh \
    validate --root /home/vgpnk/Projects/shokunin mori
… W04 duplicate url … (14 warning lines) …
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
rc=0
```

`rc=0` with `TMPDIR` unset. The only failing check is the r44 counter's own `--file`
staged-copy census arm (`census_ok FAIL (exit=1)`) — i.e. the *instrument's* defect, not the
registry's. **The cheapest control that meets C3 is: fix that one arm and point
`--entry`/`--row` at the r44 pair.** No new entry, no new row, no new README row, no source
opened. The claim's stated work is not what the predicate measures.

### (b) One sentence, code and label identical — FALSIFIED

Claim text: *"one admitted entry … one `mined` row whose `used-by` names it"*. Predicate L70:
*"every `--row S###` exists, is `mined`, and names the entry in its `used-by` cell"*. r44's
CLI: `ap.add_argument("--row", action="append", default=[])` (`count-c3.py:285`) — zero rows
is a legal run, and `∀` over the empty set is true. The claim's "one row" and the predicate's
"every `--row`" cannot be stated identically, and the entry need not be *this* round's
("admitted" is not defined; L68 only requires the four line prefixes).

### (c) One concrete value, one command, committed bytes — FALSIFIED

P-C3 has **no numeric after-value at all** — "C3=met" over five sub-conditions, two of which
(the census command; the digest pin) are not values. And item 5 (L75) pins *"the census script
the arm invoked"*, which is `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` — outside
the lane repo, so the digest is not "over committed bytes" of the measured repo, and it changes
whenever the fleet script is edited (the lane must never write there).

### (d) Causally separable — HOLDS

C3's own artifacts (entry, row, README row, census arm) do not enter C1's ledger or C2's
population; the counter is separate. One caveat, not a coupling: the SOURCES row and README
row are L1-integrated, so "C3 landed" depends on L1 authorship, not on C1/C2 state.

### (e) Names the surface, not the number — FALSIFIED

The claim says *"grounded in a source this lane opened"*; the predicate accepts any entry with
a `source:` line, including r44's. The surface ("this round opened the source") is in the label
and absent from the predicate.

### (f) Universal without enumeration — FALSIFIED

L70 *"every `--row S###`"* — no minimum size, no enumeration; a run with no `--row` satisfies
it vacuously (and satisfies (a) cheaply).

---

## 4. Kill rules — FALSIFIED (2 of 3 entering-tip receipts print `met`)

L81–82: *"A do-nothing control at the entering tip prints `C1=unmet`, `C2=unmet`, `C3=unmet`
(the three entering-tip receipts)."* Measured at the entering tip, under the instruments that
exist there:

| claim | receipt | verdict |
|---|---|---|
| C1 | `.ufo/waves/round-45/evidence/control-r44-c1.txt` | **`C1=met mismatches=0`, rc 0** |
| C2 | `.ufo/waves/round-45/evidence/control-r44-c2.txt` run B | **`C2=met`, rc 0** |
| C3 | my run, flags above | `C3=unmet`, rc 1 (correct, and for the right reason: `census_ok FAIL`) |

The three receipts the sentence calls existing ("the three entering-tip receipts") did not
exist at the freeze — they are this wave's output — so the sentence was a prediction about
artifacts produced after it was frozen, and it is false for two of three. The per-claim kill
bullets are weaker than the predicate they guard: the C1 bullet forbids "a ledger of
revision-constant figures" while L25–26 explicitly admits them with `CONST=`; the C2 bullet
names only two fixture shapes (junk row, comment-only selftest) and says nothing about a
caller-chosen population or a two-table read, both of which print `met`; the C3 bullet's
"census run that needs a `TMPDIR` override" is not a control at all — the census already
passes without one.

## 5. Frozen instruments — FALSIFIED

L97–101: *"Written by the L1 at the freeze commit; each entry is `sha256  path`. The manifest
is `evidence/freeze-r45.txt`."*

```
$ git cat-file -e 3ad8faaa:.ufo/waves/round-45/evidence/freeze-r45.txt
fatal: path '.ufo/waves/round-45/evidence/freeze-r45.txt' does not exist in '3ad8faaa'
$ git cat-file -e 3ad8faaa:evidence/freeze-r45.txt
fatal: path 'evidence/freeze-r45.txt' does not exist in '3ad8faaa'
$ git show --stat --oneline 3ad8faaa
… 5 files changed: contract.md, w1-spec.json, w1-dispatch.json, 2 opened sources
```

The r44 convention exists and is populated — `.ufo/waves/round-44/evidence/freeze-r44.txt` pins
`contract.md`, `count-c1.py` (`9477824d…`), `count-c2.py`, `count-c3.py`,
`tools/mori-gate-registry.py` (`743996b1…`), the three mutants, `figures-r43.tsv`, `SKILL.md`.
The r45 section is unsatisfiable **by construction**: the instruments the round builds
(`count-c1/c2/c3.py`, `mori-gate-registry.py` v2) do not exist at the freeze commit, and the
dispatch was committed in the same commit as the freeze. No wave item owns writing the
manifest (`grep -c freeze-r45 .ufo/waves/round-45/w1-spec.json` → 0). Net effect: **no
instrument byte of this round is pinned**, so a post-freeze edit to any counter is
undetectable — the exact failure the section exists to prevent, and the one the r44 section
actually caught (`ExecControlReceipts` compares its instrument sha to the r44 freeze pin).

## 6. Floors and knobs — HOLDS

L92–95 is testable and is a real change: r44 does **not** clamp (`count-c1.py:145`,
`record("row_floor", len(rows) >= min_rows …)`), so passing `--min-rows 3` to a 3-row ledger
passes today. The frozen clamp, plus "the verdict line prints the frozen floors, the measured
revision and the repo path", is concrete and re-derivable. Only nit: "the repo path" has no
pinned spelling (`--repo` vs resolved realpath); the r44 line prints the resolved path. Minor,
not a falsification.

## 7. Axis question — lowest-axis obligation met on the letter, with a structural gap

`SCORECARD.md:10-15` at the entering tip: coverage 6, **operability 7**, **depth 5**,
**freshness 5**, **calibration 5**, adjacency 6. The contract's L17–19 list is accurate.

- Lowest non-retired = 5, tied three ways (calibration, depth, freshness). C2 targets
  calibration 5, C3 targets depth 5 → **the lowest-axis obligation is met** (a tied-lowest axis
  is worked by two claims).
- But **freshness 5 is also tied-lowest and L18–19 explicitly claims nothing on it**. The round
  therefore leaves one of the three lowest axes with no claim, while spending one of three
  claims on **operability 7** — the lane's owned axis at its maximum, where a claim can only
  *hold* the score, never raise it. If the closure grades C1 "improved", it must also say the
  operability score did not move, or it re-creates the calibration defect C2 claims to fix.
- C2's own axis attribution is arguable both ways: a *gate registry* is operability evidence,
  and calling the fix "calibration" is only defensible because the defect was a self-description
  overstatement. The contract should say which, because the closure table will have to.

## 8. Axis harm — does hardening C1's grammar or C2's auditor remove a relied-on capability?

**No capability is deleted. Four identity/coupling harms are real and one is a substitution.**

1. **The r44 ledger becomes inadmissible under the new clause (identity change of a cited
   artifact).** 15 of 16 rows are revision-constant across `554ff416`↔`b1d7269` with no
   `CONST=` (table in §1(c)). That ledger is cited: `corpus/QUALITY.md:948`,
   `corpus/lessons/round-44.md:106`, and `SKILL.md:183` documents the counter's default
   `--ledger .ufo/waves/round-44/figures.tsv` (`count-c1.py:297`). If `count-c1.py` v2 keeps
   that default, its **default invocation at the landed tip prints `C1=unmet`** on the
   committed r44 ledger, contradicting the `SKILL.md:183` row and the r44 closure's
   `C1=met mismatches=0`. The row-grammar part ("one `git` pipeline naming `@REV@`") does
   **not** invalidate the rows — all 16 satisfy it; it is the revision-sensitivity clause that
   does. Smallest safe correction: name the r45 ledger and change the default to it, and run
   the r44 comparison with an explicit `--ledger`.
2. **`no_selftest=0` forces edits to two live gates and leaves one honest row stale.**
   `tools/mori-round19-regressions.py` (SKILL.md:182) has no `--selftest` today and its
   self-test cell says "Same CLI over isolated synthetic Git fixtures (`--mode after`)";
   `ExecSelftestModes` adds a branch but **no item updates row 182**, so the registry becomes
   *understated* — the same class of falsehood C2 is meant to remove, in the opposite
   direction. The r19 gate's own frozen expectation table
   (`5e393d20:.ufo/waves/round-19/frozen/expected.json`) is the thing that must not move; the
   added branch must not touch `--mode after`.
3. **`tools/mori-silence-cases.sh` is the r13 gate's SUT.** `SKILL.md:167`'s row runs the
   **live** `tools/*.sh` (`--census`/`--oracle` defaults to the repo tools) as the system under
   test, and r13's verdict is "0 clean · 1 failed (claim mismatch)". `FROZEN_PINS`
   (`mori-round13-regressions.py:180-186`) compares digests against
   `frozen_dir / name` (`:457-464`), so the *pin* survives an edit to the live file — but any
   behaviour change in the live oracle flips the r13 SUT claims. Editing it (as
   `ExecSelftestModes` does) couples a C2 capability addition to r13's evidence.
4. **The three added `--selftest` branches can be stubs.** L53–55 requires "a real argv branch"
   and forbids a *comment* occurrence — nothing requires the branch's arms to fail when a check
   is disabled. A branch that prints `R19_SELFTEST pass=1 fail=0` without asserting anything
   passes both the auditor and `ExecC2Counter`'s tally check; the wave's mutant arm covers
   counters (`MutCounters`, `MutAuditor`), not the three added branches. That is a capability
   *substitution*: the lane gains a token, not a test.
5. **Pre-existing, not caused by the round:** C2's singular "the row that names it" is
   contradicted by five multi-row paths (§2(f)); v1 already picks one by cell length. The
   frozen text should either allow multiple naming rows explicitly or require exactly one and
   make it a finding.

## 9. Targets unreachable in one round

1. **`C2` item 5, `no_selftest=0` over the whole declared population (literal reading).**
   Population files with no `--selftest` argv branch and no wave item adding one:
   `tools/mori-disk-rate.py` (0 occurrences), `tools/mori-round41-calibration.py`
   (0 occurrences), `tools/mori-routed-r24.py` (its own row at `SKILL.md:721` says *"none
   built in — the tool has no `--selftest`"*). `ExecSelftestModes` fixes only
   silence-cases.sh, round19-regressions.py, routed-check.py. ⇒ `no_selftest ≥ 3` at the
   landed tip. Unreachable without a correction that either adds three more branches or
   re-scopes `no_selftest` to rows whose cell claims one.
2. **`C2` item 6 against the frozen path `fixtures/write-scope.json`.** The path does not
   exist (repo root or entering tip); the wave builds `.ufo/waves/round-45/fixtures/write-scope.json`.
   As frozen the arm reads an absent file ⇒ exit 2 / unmet, never `writescope_mismatch=0`.
   Unreachable without a path correction.
3. **The frozen-instruments manifest at the freeze commit.** `evidence/freeze-r45.txt` (either
   reading of the path) is absent from `3ad8faaa`; by the time it could be written the freeze
   commit is in the past and the instruments it would pin were still being authored. The
   section's stated artifact can never exist as specified.
4. **Not unreachable but unmeasurable as written:** `C2` item 1's "*every* table" — the only
   observable is `tables=<n>`, and L48 accepts any `n ≠ 1`, so no run can prove that all seven
   tables were read (`SKILL.md:162, 524, 588, 643, 718, 796, 881`). A `C2=met` receipt cannot
   distinguish 2-of-7 from 7-of-7.

Reachable only *vacuously / without the claimed work* (not "unreachable", but equally
unearnable): C3 whole-predicate via the r44 entry+row+README (§3(a)); C1 via 12 `CONST=` rows
and/or an empty `--witness-dir` (§1(a)).

## 10. Smallest safe corrections (copy-paste Markdown for the L1)

Append as a **round-45 correction section** (per L6–7, never a rewrite):

```markdown
## Round-45 correction 1 — contract defects found before scoring (CritContract)

### C1
- The measured ledger is `.ufo/waves/round-45/figures.tsv`; `--ledger` defaults to it. The
  round-44 ledger stays a historical r44 receipt and is never the default.
- `--other-rev` is frozen to `554ff416459c92f0dea9762f834a556df2990187` and printed in the
  verdict line; a run with any other `--other-rev` is `C1_SETUP`.
- The row grammar is exactly: one `git` invocation from the read-verb allowlist
  `{show, grep, ls-tree, rev-list, cat-file, log}` as the first stage, `@REV@` present, no
  second `git` stage, no `;`/`&&`/`|&`/backtick/`$(`, no stage named `tee`, `dd`, `sh`, `bash`,
  `python*`, `perl`, `sed -i`, `xargs`. `diff` is not a read verb.
- `CONST=<reason>` lives in the value column; at most 4 of 12+ rows may carry it, and a
  `CONST=` row is admitted only if its command's value is byte-identical at `--rev` and
  `--other-rev`.
- Witness floor: `--witness-dir` must contain at least the three files
  `w-revconst.tsv`, `w-head.tsv`, `w-dup.tsv`; `witnesses=3/3` is the only passing value, and
  the same `--other-rev` is used for the ledger and the witness.

### C2
- `tables=7` is the expected count, enumerated as the header rows at `SKILL.md` lines
  162, 524, 588, 643, 718, 796, 881 measured at `--rev`; any other count is `C2=unmet`.
- The population is derived, never supplied: `git ls-tree -r --name-only <rev> tools/` filtered
  to `*\.py`/`*\.sh`, plus `git ls-tree -r --name-only <rev> .ufo/waves/round-4[45]/` filtered
  to `count-c*.py`. `--audit` is removed from the CLI; a caller-supplied subset is `C2_SETUP`.
- `no_selftest` counts population files with no argv branch (`--selftest` as a parsed argument
  or a `case` arm), not rows. It is therefore 3 at the landed tip unless `--selftest` is added
  to `tools/mori-disk-rate.py`, `tools/mori-round41-calibration.py` and
  `tools/mori-routed-r24.py` in this round; if it is not, the C2 target is restated as
  `no_selftest<=3` with the three named, not `=0`.
- The write-scope fixture is `.ufo/waves/round-45/fixtures/write-scope.json`.
- A path named by more than one row is a finding `multi_row=<n>`, and the attribution prints
  every naming row; the expected value at the landed tip is 0 or the five paths listed in
  CritContract §2(f) are each declared.

### C3
- `--row` is required and must be supplied at least once; a run with no `--row` is `C3_SETUP`.
- The entry must not exist at `--rev~1` (this round's entry), and its `source:` line must cite
  a source the round opened (a `SOURCES.md` id whose `opened` equals the round's date).
- The census digest is frozen as a constant in the counter and compared, not merely printed.

### Kill rules
- Replace the entering-tip claim with the measurement: at `554ff416` the round-44 instruments
  print `C1=met` and `C2=met` (receipts `.ufo/waves/round-45/evidence/control-r44-c1.txt`,
  `control-r44-c2.txt` run B) and `C3=unmet`. The do-nothing control is one named command per
  claim, run with the r45 instrument at the landed tip against the entering-tip worktree.

### Frozen instruments
- The manifest is `.ufo/waves/round-45/evidence/freeze-r45.txt`, written at the **scoring**
  commit, pinning `contract.md`, `SKILL.md`, `count-c1.py`, `count-c2.py`, `count-c3.py`,
  `tools/mori-gate-registry.py`, the witness ledgers, the mutants and the write-scope fixture,
  with each instrument's `--selftest` tally. The freeze commit cannot pin instruments it does
  not yet contain.

### Separability
- C2 is measured after C1 and C3 instruments are committed (ordering, recorded); C1's ledger
  asserts no figure that C2 or C3 changes this round (drop "unregistered count" and
  "`--selftest`-capable tools" from the ledger, or assert them at the entering tip with
  `CONST=`).
```

## 11. Evidence index, tooling, scratch

Commands and outcomes (all read-only; `rc` as printed):

| # | command | result |
|---|---|---|
| 1 | `git log --oneline -3` + `git status --porcelain` | tip `3ad8faaa`, only untracked wave files |
| 2 | `git show --stat --oneline 3ad8faaa` | 5 files, no `evidence/freeze-r45.txt` |
| 3 | `git cat-file -e 3ad8faaa:{.ufo/waves/round-45/evidence/,}freeze-r45.txt` | fatal: does not exist (both paths) |
| 4 | r44 `count-c1.py 554ff416…` | `C1=met mismatches=0`, rc 0 |
| 5 | r44 `count-c2.py 554ff416… --counter tools/mori-gate-registry.py` | `C2=unmet`, rc 1 (`mutant absent` — mispath) |
| 6 | same + `--mutants-dir .ufo/waves/round-44/fixtures/mutants` | `C2=met`, rc 0 |
| 7 | `mori-gate-registry.py --rev 554ff416 --audit-all` | argparse error `unrecognized arguments`, rc 2 |
| 8 | `mori-gate-registry.py --rev 554ff416 --audit tools/mori-source-drift.py` | `REGISTRY=unmet` (rows 883/886 name it) |
| 9 | r44 `count-c3.py 554ff416… --entry …r44.md --row S472 --census …` | `C3=unmet`, rc 1; `entry_meta/rows_present/readme_row` PASS, `census_ok FAIL (exit=1)` |
| 10 | `env -u TMPDIR … sources-census.sh validate --root … mori` | `mori ok`, rc 0 |
| 11 | per-row recompute of all 16 r44 rows at `554ff416` and `b1d7269` | 15 CONSTANT, 1 moves (F15) |
| 12 | escape-aware parse of `SKILL.md` | 7 eight-cell tables, 43 rows, 3 population files with no row, 5 paths with >1 naming row, 0 duplicate names |
| 13 | per-file scan of the 36-file population for a real `--selftest` argv branch | 6 with none: silence-cases.sh, disk-rate.py, round19-regressions.py, round41-calibration.py, routed-check.py, routed-r24.py |
| 14 | `git diff --stat 3ad8faaa -- …/contract.md` | empty (rc 0) — contract unmodified |
| 15 | `grep -n FROZEN_PINS -A6 tools/mori-round13-regressions.py` + `:457-464` | pins compare against `frozen_dir/name`, not the live oracle |
| 16 | `ls -d /tmp/sources-census.*` | no leftover (census `mktemp` removed it) |

- **Tooling:** none installed or upgraded (no pacman/npm/uv/cargo transaction). Read-only git
  only.
- **Scratch:** `.ufo/waves/round-45/tmp/CritContract` (created, used only as `TMPDIR` for
  counter runs, removed at end — `rmdir` rc 0). Command #10 deliberately unsets `TMPDIR` because
  the contract's own wording is "without any `TMPDIR` override"; that is the condition under
  test, and the census's `mktemp -d "${TMPDIR:-/tmp}/…"` cleaned up after itself (check 16).
- **Not touched:** `SKILL.md`, `SCORECARD.md`, `LOG.md`, `corpus/*`, `contract.md`, any
  sibling seat's report, the fleet repo, any other `*-shokunin` repo, `shokuknow`.
