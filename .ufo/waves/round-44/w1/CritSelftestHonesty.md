# CritSelftestHonesty — is a `--selftest` tally evidence that the checks ran?

Round 44, wave 1, critic seat. Scope: the `--selftest` evidence of the four frozen
instruments at `7cb59c6891d4f5d0266fe062565f094da835dc84`:

- `.ufo/waves/round-44/count-c1.py` (353 lines)
- `.ufo/waves/round-44/count-c2.py` (388 lines)
- `.ufo/waves/round-44/count-c3.py` (321 lines)
- `tools/mori-gate-registry.py` (308 lines)

No frozen instrument was edited, no lane byte was written except this file. All
adversarial copies were built under `mktemp -d` sandboxes
(`/tmp/crit44.fFjuSR`, `/tmp/c3repro.9ljwAO`); the lane checkout was only read.
Installs: none.

## Verdict in one line

A tally is **not** evidence that the checks ran. It is a count of arm functions that
returned without raising; the same `pass=N fail=0` line is produced with every
assertion stripped (`-O`), and `count-c2.py` scores a counter whose own tally says
`fail=1` as conformant. The strongest evasion is a one-token bug at
`count-c2.py:185`.

## What I ran (evidence base)

```
$ python3 .ufo/waves/round-44/count-c1.py --selftest   -> C1_SELFTEST pass=6 fail=0 rc=0
$ python3 .ufo/waves/round-44/count-c2.py --selftest   -> C2_SELFTEST pass=5 fail=0 rc=0
$ python3 .ufo/waves/round-44/count-c3.py --selftest   -> C3_SELFTEST pass=6 fail=0 rc=0
$ python3 tools/mori-gate-registry.py --selftest       -> GATE_REGISTRY_SELFTEST pass=6 fail=0 rc=0
$ python3 -O <same four> --selftest                    -> identical tallies, rc=0 for all four
$ PYTHONOPTIMIZE=1 python3 count-c1.py --selftest      -> C1_SELFTEST pass=6 fail=0
$ PYTHONOPTIMIZE=1 python3 -c 'import sys; print(sys.flags.optimize, __debug__)'
                                                        -> 1 False
```

All four match `evidence/freeze-r44.txt` ("selftest tallies at freeze"). That file
records the tallies but not the invocation, so it cannot distinguish the asserted run
from the stripped one — see (b) below.

Adversarial probes (each a temp git repo, `count-c2.py` invoked from the frozen
bytes against `--repo <tmp>`):

| probe | fixture | observed |
|---|---|---|
| A | counter `--selftest` prints `pass=2 fail=1`, exit 1; mutant prints `pass=1 fail=1`, exit 1 | `check selftest_tally PASS (fx-one.py pass=2 fail=1)` · `C2=met` |
| B | counter prints `pass=9 fail=0` with no arm and no fixture; mutant prints `pass=8 fail=1` | `check selftest_tally PASS (fx-two.py pass=9)` · `mutant_kill PASS (killed (fail=1))` · `C2=met` |
| C | counter = real `count-c1.py`; mutant = same bytes + a syntax error | `mutant_kill FAIL (SURVIVED (no tally))` · `C2=unmet` |
| D | counter = real `count-c3.py`; "mutant" = same bytes, all five checks intact, one fixture path typo | `mutant_kill PASS (killed (fail=1))` · `C2=met` |
| E | mutant prints `pass=0 fail=1`, exit 1 (zero arms) | `killed (fail=1)` |
| F | mutant prints `pass=4 fail=1`, exit 0 / exit 2 | `SURVIVED` (exit code is genuinely read) |

Per-check mutation sweep (condition of each `record(...)` replaced by `True`, then
`--selftest` re-run):

```
count-c1: ledger_present fail=1 · rows_parse fail=2 · row_floor fail=1
          class_floor  rc=0 C1_SELFTEST pass=6 fail=0     <- SURVIVES
          commands_reconcile fail=1
count-c2: counters_present fail=1 · registry_rows fail=2 · selftest_tally fail=1
          mutant_kill fail=1
          tool_selftest rc=0 C2_SELFTEST pass=5 fail=0    <- SURVIVES
count-c3: entry_present · entry_meta · readme_row · rows_present · census_ok all fail=1
```

`parse_ledger` sub-rule deletions (`count-c1.py:97,99,101,103,105`), one rule removed
at a time:

```
drop @REV@ rule                rc=0 C1_SELFTEST pass=6 fail=0
drop ;/&& rule                 rc=0 C1_SELFTEST pass=6 fail=0
drop non-byte-producer rule    rc=0 C1_SELFTEST pass=6 fail=0
drop git-verb rule             rc=0 C1_SELFTEST pass=6 fail=0
drop id rule                   rc=0 C1_SELFTEST pass=6 fail=0
```

Auditor branch probes:

```
exists_at() forced to return True        -> GATE_REGISTRY_SELFTEST pass=6 fail=0   (undetected)
row entry cell = "see the appendix, `tools/fixture-tool.sh`" -> ok=True
row entry cell names "tools/fixture-tool.sh.bak"             -> ok=True
nine-cell row (8 standard + 1 extra)                         -> ok=True
```

## (a) Does each arm assert a specific verdict/exit, or merely print PASS?

PASS is **printed, not asserted**. In all four files the loop is
`for name in arms: print("selftest PASS %s" % name)` and `arms.append(name)` happens
only after the arm body returns (`count-c1.py:203-208,278-289`;
`count-c2.py:273-280,336-346`; `count-c3.py:213-220,265-276`;
`mori-gate-registry.py:190-197,258-269`). The only test is the `assert` inside the
arm body. Consequence: the PASS line is a label for "did not raise", not for "the
named check rejected the fixture".

Arm-by-arm:

| instrument | arm | assertion | specific? |
|---|---|---|---|
| c1 | `honest_ledger_met` (:210-217) | `not fails` and `meta["mismatches"] == 0` | no — asserts *absence* of failures, not that the five check names fired |
| c1 | `offbyone_row_mismatch` (:221-230) | `"commands_reconcile" in fails` and `mismatches == 1` | yes |
| c1 | `junk_producer_rejected` (:234-243) | `"rows_parse" in fails` | name only — not which of the five rules |
| c1 | `below_floor_rejected` (:246-253) | `"row_floor" in fails` | yes |
| c1 | `absent_ledger_unmet` (:256-263) | `"ledger_present" in fails` | yes |
| c1 | `compound_command_rejected` (:266-275) | `"rows_parse" in fails` | name only |
| c2 | `registered_conformant_met` | `not fails` | no |
| c2 | `absent_counter_unmet` | `"counters_present" in fails` | yes |
| c2 | `unregistered_counter_unmet` | `"registry_rows" in fails` | yes |
| c2 | `no_selftest_mode_unmet` | `"registry_rows"` **and** `"selftest_tally" in fails` | yes |
| c2 | `surviving_mutant_unmet` | `"mutant_kill" in fails` | yes |
| c3 | `registered_entry_met` | `not fails` | no |
| c3 | `absent_entry_unmet` / `row_without_used_by_unmet` / `red_census_unmet` / `readme_without_row_unmet` / `missing_coverage_map_unmet` | one check name each | yes |
| gr | `registered_row_met` | `assert ok` | yes |
| gr | `missing_cell_rejected` (:208-216) | `assert not ok` | reason measured correct ("missing cells: pinned values") |
| gr | **`unresolved_entry_rejected` (:218-226)** | `assert not ok` | **no — wrong reason, see (c)** |
| gr | `unregistered_path_rejected` (:228-235) | `assert not ok` | reason correct |
| gr | `no_selftest_rejected` (:237-244) | `assert not ok` | reason measured correct ("tool has no --selftest mode") |
| gr | `seven_cell_row_rejected` (:246-255) | `assert not ok` | reason measured = "missing cells: name,kind,entry,…,owner" (the row loses *all* cells), so the assertion does not pin "seven cells" |

No arm anywhere asserts a process exit code. Exit codes are produced only by
`selftest()` returning 0/1 (`count-c1.py:290`, `count-c2.py:347`,
`count-c3.py:277`, `mori-gate-registry.py:270`). So "the arm asserted the verdict"
is nowhere a claim about an exit status.

## (b) Can a counter print `pass=6 fail=0` without executing any check?

Yes, four distinct ways, three measured:

**b1. `-O` / `PYTHONOPTIMIZE`.** Every arm's test is a bare `assert`; `-O` strips
them, and all four instruments print their exact frozen tallies with nothing tested
(measured above). The instruments have no guard: `grep -n '__debug__\|PYTHONOPTIMIZE\|sys.flags'`
over the four files → no match. `count-c2.py:91-98` passes `env=dict(os.environ)`
plus `MORI_GATE_REGISTRY` to every child (`selftest_env`, :109-113), so a
`PYTHONOPTIMIZE=1` in the operator's shell propagates into the counters *and* the
mutants it scores. `freeze-r44.txt` records the tallies without the invocation, so
the frozen evidence cannot rule this out.

**b2. The tally counts arm *completions*, and an arm can complete without its check
running.** In c2/c3/gr, `arm()` catches `Exception` (`count-c2.py:277-279`,
`count-c3.py:217-219`, `mori-gate-registry.py:194-196`), so an arm whose fixture
cannot be found is recorded as a *failure* — the selftest still prints a tally.
Measured: `count-c2.py --selftest` run from a copy outside the checkout prints
`pass=0 fail=5` (five arms each raised `cannot locate tools/mori-gate-registry.py for
the selftest fixture`, `count-c2.py:249-260`). A tally therefore exists even when no
check ran; `tally_of` (:100-106) does not care.

**b3. A hardcoded tally is accepted end-to-end.** Probe B: a counter whose entire
`--selftest` branch is `print("FIX_SELFTEST pass=9 fail=0")`, plus a "mutant" that
prints `pass=8 fail=1`, is scored `selftest_tally PASS`, `mutant_kill PASS`,
`C2=met`. `count-c2.py`'s own positive fixture `COUNTER_OK` (:196-206) is exactly
this shape: it prints `pass=2 fail=0` and runs no check, and the arm
`registered_conformant_met` calls that "conformant". Nothing in `evaluate()`
(:117-188) ties a tally to executed assertions.

**b4. A fixture path silently resolving elsewhere.** The question's own example is
live in `count-c3.py`: `evaluate` stages `SOURCES.md` into `tempfile.mkdtemp()`
(:133-136) and runs the census on it (:139-143). The real census resolves `used-by`
against `realpath(dirname(staged)/..)` — i.e. `/tmp` — so the staged file is read
against the wrong root. Measured on bytes that are genuinely green in the lane:

```
$ git show 1429c791:corpus/SOURCES.md > /tmp/c3repro.9ljwAO/SOURCES.md
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /tmp/c3repro.9ljwAO/SOURCES.md
  file  E11  S235 missing used-by corpus/knowledge/oom-evidence-loss-r38.md
  file  E11  S241 missing used-by corpus/knowledge/oom-evidence-loss-r38.md
  ... inner_rc=1
```

and the counter itself, on a genuinely registered entry at the entering tip:

```
count-c3.evaluate(1429c791, corpus/knowledge/oom-evidence-loss-r38.md, [S235,S241], census=<real>)
  entry_present PASS (6980 bytes) · rows_present PASS (rows S235,S241 mined)
  census_ok FAIL (exit=1)
```

So `census_ok` is false at every revision, and the six arms cannot see it because
they inject a stub the counter writes itself: `CENSUS_OK = "#!/bin/sh\n# fixture
census\nexit 0\n"` (`count-c3.py:172`), placed by `_files()` at :204 and invoked at
:227; the red arm swaps in `CENSUS_RED = "#!/bin/sh\nexit 1\n"` (:173, :249). Neither
stub reads `"$@"`, so the arm proves only that a nonzero exit is propagated. This is
also a check that *cannot pass* — the mirror image of a vacuous check that cannot
fail, and both are invisible to a green tally.

Not exploitable, measured: a fixture that never got committed. Suppressing the
fixture commit in `_mk_repo` (`count-c1.py:169-191`) makes the selftest red
(`C1_SELFTEST pass=1 fail=5`, rc=1), because `git rev-parse main` returns empty and
`read_at(repo, "", …)` (:62-75) then probes the index (`cat-file -e ":path"`) instead
of a commit. The arms detect the uncommitted fixture; the *scoring* path
(`main`, :314-318) would reject `rev=""` as `C1_SETUP` anyway.

## (c) Is any arm vacuous — does it assert something that cannot fail?

Four concrete cases, all measured:

**c1. `mori-gate-registry.py:218-226` `unresolved_entry_rejected` is mislabelled and
its target branch is dead.** The fixture replaces only the first occurrence
(`GOOD_ROW.replace("tools/fixture-tool.sh", "tools/ghost-tool.sh", 1)`), so the
*entry* cell names `ghost-tool.sh` while the self-test cell still names
`fixture-tool.sh`. `audit()` therefore finds no matching row and rejects at
`mori-gate-registry.py:122-131` — measured detail: `unregistered: no row names
fixture-tool.sh`. The `exists_at` rejection at :140-143 is never reached by any arm,
and neutering it (`def exists_at(...): return True`) leaves the selftest green
(`pass=6 fail=0`). The registry's "entry path resolves at the measured revision"
guarantee — one of the three things C2 claims — is therefore untested by the tool's
own selftest. This is a fixable defect, not a tradeoff: the arm asserts `not ok`
without pinning a reason, so it cannot distinguish the branch it names from the
branch that actually fires.

**c2. `count-c1.py:147` `class_floor` has no able-to-fail arm.** No arm ever builds a
ledger with ≥12 rows in <4 classes, so the `min_classes` floor cannot fail in any
arm. Measured: `record("class_floor", True, …)` → `C1_SELFTEST pass=6 fail=0`. The
`honest` arm's `assert not fails` (:216) also passes with the floor disabled. The
committed mutant disables `row_floor` (`fixtures/mutants/count-c1.py`), the one check
an arm does cover — so `mutant_kill` is satisfied by choosing the covered check.

**c3. `count-c2.py:149-153` `tool_selftest` has no able-to-fail arm.** No arm makes
the auditor's `--selftest` red. Measured: condition → `True` gives
`C2_SELFTEST pass=5 fail=0`. The committed mutant disables `mutant_kill` — again a
covered check.

**c4. `count-c1.py`'s grammar has five independent rules and zero per-rule arms.**
`:97` (not a git pipeline), `:99` (read verb), `:101` (`@REV@`), `:103` (single
pipeline), `:105` (non-byte producer) all feed one boolean recorded at :143. The two
`rows_parse` arms are cross-masked: `junk_producer`'s `echo 3` trips :97 *and* :105;
`compound_command_rejected`'s `… | grep -c x; true` trips :103 *and* :105. Measured:
deleting **any one** of the five rules leaves `C1_SELFTEST pass=6 fail=0`. The
contract makes this grammar load-bearing ("A ledger whose commands do not read
committed bytes … is rejected, not scored"), yet no arm can detect the loss of any
rule.

Not vacuous (checked, and worth recording): `missing_cell` (:208-216) reaches the
intended `missing` branch with the intended reason; `no_selftest_rejected` reaches
:146; `seven_cell_row_rejected` does reject, but for the generic reason "all eight
cells missing" (`cells = {}` because `len(row) < len(header)`, :133), so the arm name
overstates what it pins.

## (d) Does the mutant-kill check run the mutant's own selftest and read its exit?

Yes, mechanically. `count-c2.py:170-186`: the mutant is materialized from committed
bytes at `rev` (`read_at`, :168-170), written to `tmp/mutant-<basename>`, run as
`[sys.executable, mfile, "--selftest"]` (:177) with `env` carrying
`MORI_GATE_REGISTRY`, and judged at :179 as
`mproc.returncode == 1 and mt and mt[1] >= 1`. Exit **is** read: `fail=1` with exit
0 or 2 is `SURVIVED` (probe F). A mutant that crashes before printing a tally is
**not** miscounted as killed — probe C: `SURVIVED (no tally)`, `C2=unmet`. So the
crash direction is conservative.

The false-positive direction is wide open, though:

- **No pass floor.** `pass=0 fail=1` (zero arms) is `killed` (probe E). A mutant that
  dies before any arm is counted as caught.
- **No attribution.** Probe D: a "mutant" that is byte-for-byte the counter with
  **no check disabled** — only one fixture path in its own selftest broken — is
  recorded `killed (fail=1)` and `C2=met`. Because c2/c3/gr arms convert any
  `Exception` into a failure, "the mutant's selftest is red for any reason" is
  scored as "the mutant's own selftest caught the disabled check". `mutant_kill`
  therefore proves only that two committed files disagree, not that the counter
  detects a disabled check.
- **No provenance.** The counter and its mutant are both author-supplied. Probe B
  shows the pair can be two hardcoded print statements. Nothing in `evaluate()`
  derives the mutant from the counter, verifies the diff is exactly one disabled
  condition, or requires the mutant to name the check it disables.
- **Last-match tally.** `tally_of` (:100-106) keeps the last `pass=/fail=` match in
  stdout, so a counter that prints an inner failing tally before a final green one is
  read as green (`pass=6 fail=2\npass=6 fail=0` → `(6, 0)`).

## Strongest evasion found

`count-c2.py:185`:

```python
record("selftest_tally", all(" pass=" in t for t in tallies), "; ".join(tallies))
```

`tallies` entries are built at :156-166 as either `"<name> pass=%d"` (the good case)
or `"<name> pass=%d fail=%d"` (the bad case) — **both contain the substring
`" pass="`**. Only the absent-counter entry (`"<name> absent"`, :157) and the
no-tally entry (`"<name> no tally"`, :165-166) fail the test. Measured consequence
(probe A):

```
check selftest_tally     PASS (fx-one.py pass=2 fail=1)
check mutant_kill        PASS (fx-one.py killed (fail=1))
C2=met
```

A counter whose own `--selftest` reports `fail=1` and exits 1 is scored as a
conformant gate. That directly contradicts the frozen predicate P-C2 ("the counter's
`--selftest` runs over isolated fixtures and prints a `pass=/fail=` tally with fail
0") and the SKILL row's verdict map ("no selftest tally"). `evaluate()` already has
the parsed tally in hand at :163-166 (`t`, with `t[0]`/`t[1]`); the substring test
throws that information away. This is the single highest-value defect because it is
in the *scoring* instrument, it is reachable without any environment trickery, and
its fix is one expression.

Ranked behind it: (2) `mutant_kill` accepts any red selftest (probe D) and any
zero-arm red tally (probe E); (3) `-O`/`PYTHONOPTIMIZE` makes every tally
unfalsifiable and the frozen evidence does not record the invocation; (4) the
uncovered checks `class_floor`, `tool_selftest`, all five grammar rules, and the
auditor's `exists_at`; (5) the stub census in `count-c3.py:172-173,204,227,249`,
which hides a real, measured `census_ok` falsehood (b4).

## Impacted axes

- **operability (C2's axis):** the predicate's own selftest clause is defeated at
  `count-c2.py:185`, and the mutant clause at :179 accepts non-mutants. C2's `met`
  is not evidence of "a selftest that can fail" for any counter whose check was not
  chosen for the mutant.
- **calibration (C1's axis):** `evidence/freeze-r44.txt` publishes four tallies
  without the invocation that produced them; `-O` reproduces them exactly. A
  calibration record whose numbers are not reproducible from the record is a
  self-assessment, not a measurement.
- **coverage (C3's axis):** `census_ok` is structurally false at every revision
  (b4), so a green C3 at any tip would have to come from a census the arms do not
  exercise.
- Not implicated: the figure ledger's *arithmetic* (C1 rows), which the arms do
  exercise honestly (off-by-one, floor, absent, reconcile all fire).

## Tightening for round 45 (smallest safe corrections, ordered)

Frozen bytes are not amended this round; these are routed as a lesson.

1. **`count-c2.py:185`** — replace the substring test with the parsed tally:
   `all(t is not None and t[1] == 0 and t[0] >= min_arms for t in tallies_parsed)`
   plus `proc.returncode == 0` per counter. Keep `tallies` (strings) for the detail
   cell only. One expression; closes probe A.
2. **Attribution-based mutant kill.** Ship the mutant as a declared patch
   (`fixtures/mutants/<basename>.patch`), applied by the counter to the bytes at
   `rev`, and require the patch to touch exactly one `record(...)` condition
   (mechanical check: the applied diff has one hunk, one line, and the line matches
   `record\("([a-z_]+)",`). Run the mutant with `--mutant-of <name>`; require
   `rc==1`, `fail>=1`, **and** `pass>=min_arms-1`, **and** the mutant's stdout to
   name `FAIL <name>`. Reject mutants that differ from the counter in fixture or
   environment bytes. Closes probes B, D, E.
3. **Assertion-derived tallies, and refuse stripped runs.** Each arm returns the set
   of check names it asserted; the tally prints `pass=<assertions>` and
   `checks=<names>`. At the top of every `selftest()`:
   `if not __debug__: print("<X>_SELFTEST_SETUP asserts disabled (python -O / PYTHONOPTIMIZE)"); return 2`.
   In `count-c2.py:109-113`, scrub `PYTHONOPTIMIZE` from the child env and assert
   `__debug__` in each child. Record the invocation line in the freeze evidence next
   to the tally.
4. **One mutant per check, not one per counter.** Add `class_floor` (c1) and
   `tool_selftest` (c2) mutants, and one deletion mutant per `parse_ledger` rule
   (`count-c1.py:97,99,101,103,105`) with a fixture that trips that rule alone
   (e.g. a git row with no `@REV@`; a git row piped into `printf`; a row whose verb
   is `commit`). Closes c2-c4.
5. **Auditor: pin the reason, and reach `exists_at`.** In
   `mori-gate-registry.py`, every negative arm asserts on the detail string
   (`"does not resolve"`, `"missing cells: pinned values"`, `"no --selftest mode"`),
   and add an arm where the row's entry cell names the audited path but the file is
   absent, so :140-143 is exercised. Also reject rows with more than eight cells
   (`len(row) != len(header)` → "thin or fat row"), and require the path named in
   the entry cell — not just the audit target — to resolve. Closes (c1) and the
   nine-cell/prose-cell looseness.
6. **C3 census arm must read the bytes, and the census must be pinned.** The fixture
   census should fail unless the staged file contains a sentinel row
   (`grep -q '^| S901 ' "$2"`-style), so `census_ok` distinguishes "exit 0" from
   "validated the staged bytes". Stage the file at
   `<tmp>/repo/corpus/SOURCES.md` so the census's `dirname/..` resolution matches
   production, and add the real census (`../scripts/sources-census.sh`, currently
   outside the lane repo and absent from `freeze-r44.txt`) to the freeze manifest.
   The measured `census_ok` falsehood itself is a lesson for round 45, not a patch
   here.

## Limits of this seat

- I read and executed only the four instruments and their fixtures; I did not audit
  the ledger rows, the SKILL gate rows' content, or the corpus entry (other seats).
- The census defect (b4) was independently reproduced by this seat and separately
  reported by `L1Mori44-4.RevEnteringBaseline`; the two measurements agree
  (`exit=1`, `E11` on genuinely mined rows).
- Every adversarial mutation lived in `/tmp`; the lane checkout has no new tracked
  bytes from this seat except this report.
