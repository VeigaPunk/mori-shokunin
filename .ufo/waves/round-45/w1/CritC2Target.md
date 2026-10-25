# CritC2Target — the C2 target as a claim (`unregistered=0 no_selftest=0 duplicate=0`)

Seat: critic. Scope: the target string, not the files that implement it. Measured on
the worktree at `3ad8faaa` (entering tip) plus the in-flight v2 auditor
(`tools/mori-gate-registry.py`, 600 lines, `git status` `M`, uncommitted at measurement
time). Bytes are quoted verbatim in each receipt. No tool installed, nothing outside
`.ufo/waves/round-45/tmp/CritC2Target/` written.

**Verdict: the target is not an honest claim.** Of its three counters, one is free at
entry (`duplicate=0`), one is reachable with a single extra flag and no registry change
at all (`--audit <one path>` alongside `--audit-all`), and the third (`no_selftest=0`)
is either **unreachable** this round or reachable only through a **false cell**. The
instrument that prints them cannot distinguish a 1-path audit from a 39-path audit, and
its own green fixture is a stub self-test.

---

## 1. Can the target be met by padding?

**Yes — three ways, cheapest first. The cheapest is not padding at all; it is one flag.**

### 1a. Cheapest: narrow the population, keep the counter line (`rc=0`)

`main()` takes `targets = list(args.audit) if args.audit else population(repo, rev)`, so
a supplied `--audit` silently overrides `--audit-all`. Proven at the entering tip:

```
$ python3 tools/mori-gate-registry.py --rev HEAD --audit-all
registered=29 unregistered=3 no_selftest=4 duplicate=0 wrong_row=0 tables=7
REGISTRY=unmet                                    (rc=1)

$ python3 tools/mori-gate-registry.py --rev HEAD --audit-all --audit tools/mori-census.sh
registered=1 unregistered=0 no_selftest=0 duplicate=0 wrong_row=0 tables=7
REGISTRY=met                                      (rc=0)
```

The second invocation **is** the target string, on a command line that contains
`--audit-all`, on a tip whose enumeration is 36 and where 7 of those 36 members fail
(3 `unregistered`, 4 `no_selftest`). The historical receipt has the same
shape: round-44's `count-c2.py` audited only the counters it was handed
(`for c in counters: args += ["--audit", c]`, `count-c2.py:139`), which is why the
committed `after/c2-after.txt` prints `check registry_rows PASS (REGISTRY=met)` over a
3-path population:

```
$ python3 tools/mori-gate-registry.py --rev 5157cdda… --audit .ufo/waves/round-44/count-c1.py \
      --audit .ufo/waves/round-44/count-c2.py --audit .ufo/waves/round-44/count-c3.py
registered=3 unregistered=0 no_selftest=0 duplicate=0 wrong_row=0 tables=7
REGISTRY=met                                      (rc=0)
```

Nothing in stdout records the mode or the population size. `registered=1` and
`registered=39` are both "registered", and the three target counters read identically.
**Check that fails to catch it:** the counter line is computed from `len(targets)`,
never from `population()`; `--audit-all` and `--audit` are not mutually exclusive; no
selftest arm runs the narrowing combination.

### 1b. Row padding: eight cells of `x` pass, in any standard table

`audit()` reduces a row to `not c.strip()` per cell. No cell is ever *evaluated*. Proof
(throwaway repo under `TMPDIR`, real v2 `audit()`; tool is a 4-line stub that asserts
nothing):

```
| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| z1   | x    | `bash tools/j.sh` | x | x | x | x | x |

ALL-JUNK row in an unrelated table -> ok=True status=registered
    detail=8 cells, entry resolves, --selftest argv branch tables=1
```

The row sits in `## Round21 retained-loss observation and policy-test registry`, not in
`## Gates` — and is accepted, because `parse_tables()` reads every standard-header table
and `entry_names()` cares only that the entry cell names the path. So a "gate registry"
row can be filed in a historical round's table, with `kind=x`, `verdict map=x`,
`pinned values=x`, `write scope=x`, and the registry is green.
**Check that fails to catch it:** no arm asserts that a junk cell is a finding; there is
no `kind` vocabulary, no verdict-map grammar, no `pinned values` resolution, and the
auditor's own arm list contains `second_table_registered` — i.e. cross-table filing is
*mandated*, so the padding location is blessed by the instrument.

### 1c. The false-cell route that specifically defeats `no_selftest=0`

v2 keeps a "documented escape": `self-test` cell may declare `selftest-flag=<flag>`, and
the tool is then only checked for *that flag* appearing within ±2 lines of an argv
marker (`PY_ARGV`/`SH_ARGV`). Any argparse flag qualifies. On the **real** bytes of the
two orphans:

```
$ # tools/mori-disk-rate.py copied verbatim; the two rows differ only in name and self-test cell
SKILL0.md  ok=False status=no_selftest  detail=row 'disk rate' tool has no real --selftest argv branch
SKILL1.md  ok=True  status=registered   detail=8 cells, entry resolves, --a argv branch
```

`mori-disk-rate.py`'s `--a` is an input sample file (`--a/--b must be given together`),
not a self-test. Same result for `mori-round41-calibration.py` with
`selftest-flag=--repo` (`ok=True … --repo argv branch`). Two false cells therefore buy
`no_selftest=0` for both orphans with **zero tool edits**. The row is technically
non-empty and factually false, and the auditor cannot tell, because the declared flag is
validated against argv markers rather than against a self-test outcome.
**Check that fails to catch it:** the escape never executes the declared flag and never
asks it for a `pass=/fail=` tally.

### 1d. The sample, not census, write-scope arm

`writescope_mismatch` is computed over `.ufo/waves/round-45/fixtures/write-scope.json`,
which ExecWriteScopeFixture is told to build from exactly five rows (`r44 figure ledger
(C1)`, `r44 gate registry (C2)`, `r44 gate conformance (C2)`, `r44 corpus coverage (C3)`,
round-45 counters) — at most 7 of 39 population members (18%). The padded orphan rows'
`write scope` cells are outside the fixture by construction, so P-C2 item 6
("the audited write-scope cells make no false claim") is satisfied by not auditing them.

### 1e. `duplicate=0` is free and measures the wrong identity

At entry, across all 7 standard tables, **no name occurs twice** (verified over the
parsed rows; v2 prints `duplicate=0` at `HEAD` and at `WORK`). So the counter costs
nothing and cannot fire unless someone copy-pastes a name. Meanwhile the duplication that
*exists* is invisible: four rows name `tools/mori-census.sh` (`census`, `drift pin`,
`r14 regressions`, `r15 regressions`), two name `tools/mori-source-drift.py`, two name
`tools/mori-sources-appendonly.py`. `matches[0]` picks the first in document order and
reports no ambiguity, so attribution depends on row order — v1 said `row 'drift pin'` for
`mori-census.sh`, v2 says `row 'census'`. There is no `ambiguous=<n>` counter.

---

## 2. Is the population enumerable without the caller choosing it?

**The derivation is correct. The exclusivity is not, so the answer is still no.**

`population()` is honest — `git ls-tree --name-only <rev> -- tools/` (non-recursive,
`"/" in rest` filtered), plus direct children of the two counter dirs matching
`count-c.*\.py$`. That correctly excludes the six nested
`.ufo/waves/round-44/fixtures/mutants/count-c*.py` copies and yields:

```
$ population(".", "HEAD") -> population=36
counters: ['.ufo/waves/round-44/count-c1.py', '.ufo/waves/round-44/count-c2.py',
           '.ufo/waves/round-44/count-c3.py']
```

`36 = 33 tools + 3 counters`; at `WORK` it is 39 (the three round-45 counters now exist),
and `30 registered + 6 unregistered + 3 no_selftest = 39` confirms it. Good.

But the caller still chooses: `--audit` wins over `--audit-all` (1a), and the output
carries no `population=` and no `mode=`. A receipt cannot prove it audited the
enumeration. Note the enumeration trap for anyone implementing this differently: the
literal contract glob does **not** work as a git pathspec —

```
$ git ls-tree -r --name-only HEAD -- '.ufo/waves/round-4[45]/count-c*.py'   -> (empty)
$ git ls-tree -r --name-only HEAD -- 'tools/*.py'                          -> 0 lines
```

so a pathspec-based `--audit-all` would silently audit zero tools and zero counters and
still print `unregistered=0` (caught only by `registered>=1`).

---

## 3. Is `no_selftest=0` reachable this round?

**No. The honest floor is `no_selftest=3`, and the three tools are not all in anyone's
scope.**

Measured `--audit-all` at the entering tip:

```
registered=29 unregistered=3 no_selftest=4 duplicate=0 wrong_row=0 tables=7   (rc=1)
FAIL … mori-round19-regressions.py   no real --selftest argv branch
FAIL … mori-routed-check.py          no real --selftest argv branch
FAIL … mori-routed-r24.py            no real --selftest argv branch
FAIL … mori-silence-cases.sh         no real --selftest argv branch
FAIL … mori-disk-rate.py             unregistered
FAIL … mori-round41-calibration.py   unregistered
FAIL … mori-wave-settlement.py       unregistered
```

Arithmetic of the round as assigned:

| tool | state at entry | owned by ExecSelftestModes? | after assigned work |
|---|---|---|---|
| `tools/mori-silence-cases.sh` | comment-only `--selftest` (line 20, inside `#`), `no_selftest` | yes | registered |
| `tools/mori-round19-regressions.py` | 0 occurrences, `no_selftest` | yes | registered |
| `tools/mori-routed-check.py` | 0 occurrences, `no_selftest` | yes | registered |
| `tools/mori-routed-r24.py` | 4 mentions, **all of `tools/mori-pressure.py --selftest`** (`EVIDENCE_COMMAND`, `:96`); none of its own ⇒ `no_selftest` | **no** | **`no_selftest`** |
| `tools/mori-disk-rate.py` | unregistered; CLI is `--a/--b/--sysfs/--interval-ms`, **no self-test flag** | **no** | row lands ⇒ **`no_selftest`** |
| `tools/mori-round41-calibration.py` | unregistered; CLI is `revision/--repo/--reference-rev`, **no self-test flag** | **no** | row lands ⇒ **`no_selftest`** |
| `tools/mori-wave-settlement.py` | unregistered, but has `if args_list == ["--selftest"]` (`:687`) | n/a | registered |

So the predicate `no_selftest=0` is missed by **three** tools after every assignment in
the wave is completed. `ScribeRegistryRows` is even instructed to *document* the gap
("If a tool has no `--selftest` mode, say so in the self-test cell rather than inventing
one, and name it as a round-46 finding") — which guarantees `no_selftest=2` from the
orphans alone, while `C2=met` requires `no_selftest=0`. The contract and the assignment
contradict each other, and the only ways out are (i) two unassigned tool edits, (ii) the
false `selftest-flag=` cell of 1c, or (iii) narrowing the population (1a).

### Would the mutant arm catch a stub `--selftest`? No — and the instrument's own green fixture is a stub.

Three independent facts:

1. v2's `TOOL_OK` (the body used by the `registered_row_met` arm) is
   `--selftest) echo ok; exit 0` — a self-test with no assertion. The auditor's selftest
   arm *certifies a stub as conformant*.
2. A standalone 4-line stub is `registered`/`ok=True` (receipt in 1b). The check is
   textual: `--selftest` outside a comment within ±2 lines of an argv marker.
3. Every mutant in the wave mutates a **counter** (`MutCounters`), the **auditor**
   (`MutAuditor`), or the **C2 counter** (`ExecC2Counter` item 4). `ExecC2Counter`
   item 2 *executes* each `--selftest` but only compares a pre/post tree digest — a stub
   prints a pass line and touches no bytes, so the digest matches. `MutCounters` is asked
   the right question ("test the STUB hazard … report whether the mutant arm (or the
   auditor) catches it"); the answer is no arm does.

Concrete stub shapes that would pass every check in the wave:

- `mori-silence-cases.sh`: `--selftest) echo "MORI_SILENCE_CASES_SELFTEST pass=28 fail=0"; exit 0 ;;` (28 is the real case count — plausible bytes, zero cases run).
- `mori-round19-regressions.py`: a `run_selftest()` that returns `pass=6 fail=0` without invoking the arm list; the branch structure is real, the assertions are absent.
- `mori-routed-check.py`: print `ROUTED_CHECK_SELFTEST pass=4 fail=0` and return 0.

None of these would be caught. The only thing separating them from the in-flight
`round19` branch (which does have `selftest_rejects` helpers and a real tally) is the
executor's honesty, not a check.

---

## 4. Does the after-value change when a future round adds a tool?

**Both: the predicates are durable invariants; the numbers printed beside them are
snapshots, and today's receipt format does not separate the two.**

- Durable and self-falsifying: `unregistered=0`, `no_selftest=0`, `duplicate=0` are
  properties over a set derived from `git ls-tree` at `--rev`. Add a tool with no row
  next round and `unregistered` becomes 1 — the claim goes false without anyone editing
  the receipt. That is the right shape for a calibration claim.
- Snapshot, and therefore rot: `registered=<n>` (36 at `HEAD`, 39 at the tip), `tables=<n>`
  (7 today; every round that adds a section adds a table), and the population list. If the
  after-value is copied into `figures.tsv`/a receipt as `registered=39`, a future tool
  makes the *record* stale while `unregistered=0` stays true. The receipt must quote the
  predicate plus a **population digest**, never the count alone.
- Self-exclusion at the entering tip: `.ufo/waves/round-45/count-c*.py` does not exist at
  `HEAD` (round-45 has only `contract.md`, `w1-spec.json`, `w1-dispatch.json` and the two
  opened sources), so a `--audit-all` receipt at `HEAD` audits 36 and never audits the
  three counters the round built. The after-value is only honest at a revision that
  contains the round's own counters — and that must be asserted (`population>=39`, or the
  three names present in the audited list), not assumed.

---

## Impacted axes

- **calibration (5, the C2 axis) — primary.** The target can be printed green over a
  1-path population and over a false self-test cell; a calibration claim certified by a
  stub is worse than no claim.
- **operability (7) — secondary, by contagion.** `mori-gate-registry.py` is the lane's
  statement of its gate standard; a standard whose green fixture is
  `echo ok; exit 0` weakens every row that cites it, including the r44 rows.

No effect on coverage, freshness or adjacency.

## The cheapest control (three edits, all inside the instruments this wave builds)

1. **Make the population non-narrowable.** `--audit-all` and `--audit` are mutually
   exclusive (exit 2 on both); the counter line becomes
   `mode=audit-all population=<n> population_sha256=<sha256 of the sorted enumeration>`,
   computed from the enumeration, never from `len(targets)`. One selftest arm:
   `--audit-all --audit <path>` → `REGISTRY_SETUP`, rc 2.
2. **Make `selftest-flag=` executable or drop it.** If kept: run the declared flag and
   require a `pass=<n> fail=<n>` tally with numeric `n`, and require a per-tool mutant to
   make it exit non-zero. Otherwise delete the escape — right now it is the laundering
   route for exactly the two tools nobody owns.
3. **Make `no_selftest` an executed, red-arm property.** For each population member,
   run the tool's own `--selftest` from the audited revision's bytes and require
   (a) rc 0 with a `pass=/fail=` tally, and (b) rc ≠ 0 against a delivered one-check
   mutant of that tool. This is already the standard the round imposes on
   `count-c1/c2/c3` (`fixtures/mutants/*`); it is the standard the three tool selftests
   are exempted from.

Fourth, if P-C2 item 6 is to mean anything: the write-scope fixture must be a
**census** of every row whose `write scope` cell makes a checkable claim, and the auditor
must fail on a row absent from the fixture.

## The padding hole, in one sentence

A row is eight non-empty strings plus an entry cell that names the path; the auditor
never evaluates any cell, accepts the row in any of the seven standard tables, and
accepts a `--selftest` branch that prints a pass line without asserting — so the cheapest
padding is three rows of `x` plus three four-line stubs, and the cheapest fake is not
even padding but one `--audit <registered path>` appended to the `--audit-all` command.

## The exact check that must exist for the target to be honest

> For every path in the population derived from `git ls-tree -r` at the receipt revision
> (printed as a digest, with `--audit` narrowing refused), the tool's own `--selftest`
> must be **executed from that revision's bytes**, exit 0 printing a numeric
> `pass=/fail=` tally, and exit non-zero when a delivered single-check mutant of that
> same tool is substituted; the row that attributes the path must be the one whose
> `entry` cell's first command names it, must have `kind`/`verdict map` consistent with
> the tool's own usage text, and its `write scope` cell must appear in a census fixture
> that covers every checkable row.

Without the execution clause, `unregistered=0 no_selftest=0 duplicate=0` is a string
about prose, not about instruments.

---

## Copy-paste prose for the L1 (contract correction, round-45 correction section)

```markdown
### C2 correction (round 45) — the target is a string about prose, not instruments

P-C2 item 5 fixes the population but not the enumerator. Measured on the wave-1 v2
auditor: `--audit-all --audit tools/mori-census.sh` prints
`registered=1 unregistered=0 no_selftest=0 duplicate=0 wrong_row=0 tables=7` and
`REGISTRY=met` on a tip whose enumeration is 36 and where 7 of those 36 members fail
(3 `unregistered`, 4 `no_selftest`); `--audit` silently
overrides `--audit-all`. The counter line therefore cannot be cited as evidence that
"the whole declared population audits unregistered=0".

P-C2 item 4's escape (`self-test` cell may declare `selftest-flag=<flag>`) is a
registry-written exemption validated against argv markers, not against a self-test
outcome: `selftest-flag=--a` makes the real `tools/mori-disk-rate.py` (whose `--a` is an
input sample) `registered`, and `selftest-flag=--repo` does the same for
`tools/mori-round41-calibration.py`. Two false cells buy `no_selftest=0`.

`no_selftest=0` is otherwise unreachable this round: at the entering tip the failing set
is `{round19, routed-check, routed-r24, silence-cases}`; ExecSelftestModes owns three of
those, and registering the three orphans moves `disk-rate` and `round41-calibration` into
the `no_selftest` set. The honest floor after all assigned work is `no_selftest=3`
(`routed-r24`, `disk-rate`, `round41-calibration`), unless two unassigned tools gain real
branches.

Correction: C2 counts only when (i) the population is derived, printed as a digest, and
`--audit` narrowing is refused; (ii) a row's `self-test` cell is honoured only if the
named flag is executed and yields a numeric tally and a red mutant arm; (iii) the
write-scope fixture is a census, not a five-row sample. Until then the round records
`C2=unmet` with `no_selftest=3` and the two unowned tools routed to round 46 — an honest
miss, not a printed zero.
```

## Lesson candidate (M-number for round 46)

> A target expressed as `name=0` invites the cheapest constructor of that name, not the
> cheapest repair. Measure the target **by executing the thing it names**; if the check
> is a substring or a cell's non-emptiness, the zero is about prose. And when a population
> is declared, print the derived enumeration and its digest on the verdict line: a mode
> the caller can narrow, and a count the reviewer cannot verify, are the same defect.
