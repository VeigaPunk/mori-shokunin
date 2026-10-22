# FreezePressureCases — round 24 wave 1 (C2 case freeze)

Seat: `MoriR24.FreezePressureCases` (leaf executor). Surface: `tools/fixtures/mori-pressure/cases.json`.

## What was produced

The 12 frozen cases P01–P12, in the shared `mori-pressure-cases-v1` format, written in the
sandbox clone `/fast/scratch/hyaku/mori-r24-a2/wt-cases` (branch `r24-wt-cases`, base
`29c1bf45dde6af48fc9a07aef447bd7d7f822cc5`).

| item | value |
|---|---|
| clone | `/fast/scratch/hyaku/mori-r24-a2/wt-cases`, branch `r24-wt-cases` |
| commit | `51b644363804a37ee0f11f6a72d58637da89b335` (`round-24 C2: freeze the 12 mori-pressure selftest cases P01-P12`) |
| path in commit | `tools/fixtures/mori-pressure/cases.json` (391 lines, new file) |
| blob id | `39cc96ab4c689ceb54e7cfaf64420056e6a289f7` |
| file SHA256 | `aeb80ea080436cb344df8dba7ec19eeecc639e347ae87a14bc6835631f28ca94` |
| push | none. The clone's remote is still `origin -> /home/vgpnk/Projects/shokunin/mori-shokunin`, untouched |

Landing it from the lane (no push happened):

```
git fetch /fast/scratch/hyaku/mori-r24-a2/wt-cases r24-wt-cases
git cherry-pick 51b644363804a37ee0f11f6a72d58637da89b335
# or: git checkout 51b6443 -- tools/fixtures/mori-pressure/cases.json
```

## Sources used (no implementation was read)

Only the contract and the Linux v7.2 PSI sources. **No file named `mori-pressure.py` was
opened anywhere** (not in the lane, not in the sibling clone `wt-pressure`); the fixture was
written from the contract text plus the two kernel sources fetched over HTTPS.

| source | used for |
|---|---|
| `Documentation/accounting/psi.rst` v7.2:38–43 | the file set (`cpu`, `memory`, `io`) and the exact line format `some avg10=0.00 avg60=0.00 avg300=0.00 total=0` / `full ...` |
| `Documentation/accounting/psi.rst` v7.2:57–58 | "CPU full is undefined at the system level, but has been reported since 5.13, so it is set to zero for backward compatibility" |
| `kernel/sched/psi.c` v7.2:1290–1293 | the emitted grammar: `%s avg10=%lu.%02lu avg60=%lu.%02lu avg300=%lu.%02lu total=%llu\n` (two decimals, integer total in µs) |
| `kernel/sched/psi.c` v7.2:1274, 1277 | `only_full = res == PSI_IRQ` → the irq file carries **only** a `full` line, so a missing `some` for irq is normal, never malformed |
| `kernel/sched/psi.c` v7.2:1282–1288 | "CPU FULL is undefined at the system level" → the kernel prints zeros for the system cpu `full` line |
| `kernel/sched/psi.c` v7.2:1257, 1261 | `psi_disabled` and `!irqtime_enabled() && res == PSI_IRQ` return `-EOPNOTSUPP` → the `unsupported` state is a real kernel error |
| `kernel/sched/psi.c` v7.2:1713–1719 | `/proc/pressure/{io,memory,cpu}` always, `irq` only under `CONFIG_IRQ_TIME_ACCOUNTING` → irq may legitimately be missing (ENOENT → `absent`) |
| `kernel/sched/psi.c` v7.2:38–47 (comment block) | SOME = at least one task stalled, FULL = all non-idle tasks stalled; the system-level CPU FULL state does not exist |

Contract amendments applied: the frozen topic list is unchanged; **A2** (unsupported carries
no cause note) and **A3** (system cpu `full` gets `total_delta_us: null` / `stall_ratio: null`
under `--interval`; `counter_regressed` counts toward `PRESSURE_PARTIAL`;
`stall_ratio = delta / (requested S × 1e6)`) are reflected in the expectations below.
Amendment A4 is C1-only and touches nothing here.

## Case table

| case | topic (frozen) | exit | verdict | key states / asserted values | findings |
|---|---|---|---|---|---|
| P01 | four normal low files | 0 | `PRESSURE_OK` | cpu `ok` (`some` 1.23/0.45/0.12/98765, `full` 0/0/0/0, `full_system_undefined` true), memory `ok`, io `ok`, irq `ok` (`full` 0.31/0.29/0.27/111222) | none |
| P02 | nonzero system cpu full | 0 | `PRESSURE_OK` | cpu `ok`, `full_system_undefined` true, `full` 40.00/12.00/3.00/987654 — reported but never a threshold input | none |
| P03 | irq with only `full` | 0 | `PRESSURE_OK` | irq `ok`, `some` null, `full` 0.05/0.02/0.01/1234 | none |
| P04 | irq absent | 0 | `PRESSURE_PARTIAL` | irq `absent`, `some` null, `full` null; cpu/memory/io `ok` | none |
| P05 | EOPNOTSUPP on all four | 2 | `PRESSURE_UNAVAILABLE` | cpu/memory/io/irq `unsupported`, `some` null, `full` null | none |
| P06 | memory some avg10 25 | 1 | `PRESSURE_HIGH` | memory `ok`, `some` 25.00/12.50/3.25/987654 | `PRESSURE_HIGH` / memory |
| P07 | irq full avg10 15 | 1 | `PRESSURE_HIGH` | irq `ok`, `some` null, `full` 15.00/5.00/1.00/12345 | `PRESSURE_HIGH` / irq |
| P08 | non-decimal avg10 in io | 0 | `PRESSURE_PARTIAL` | io `malformed`; cpu/memory/irq `ok` | none |
| P09 | memory missing `full` | 0 | `PRESSURE_PARTIAL` | memory `malformed`; cpu/io/irq `ok` | none |
| P10 | EACCES on io | 0 | `PRESSURE_PARTIAL` | io `unreadable`, `some` null, `full` null | none |
| P11 | interval with two snapshots | 0 | `PRESSURE_OK` | all `ok`; `cpu.some` `total_delta_us` 125000 / `stall_ratio` 0.125; `cpu.full` null / null (A3); `memory.some` 100000 / 0.1; `io.some` 40000 / 0.04; `irq.full` 6000 / 0.006 | none |
| P12 | interval with a decreasing total | 0 | `PRESSURE_PARTIAL` | cpu `counter_regressed` (200000 → 100000 µs); memory/io/irq `ok` | none |

`args` are `[]` except P11 and P12, which carry `["--interval", "1"]`; those two cases carry
two snapshots, every other case one.

## Judgement calls (the places a reviewer may disagree)

1. **System cpu `full` is reported as read.** P01 and P02 assert the parsed `full` numbers
   (zeros and 40.00/12.00/3.00/987654) while the cpu resource carries
   `full_system_undefined: true`. Contract C2: "System `cpu` `full`: reported but labeled
   `full_system_undefined: true`". If the implementation instead nulls or rewrites the
   system cpu `full` numbers, P01 and P02 fail on the value, not on the state.
2. **P01's system cpu `full` line is all zeros** — the kernel-faithful shape
   (`psi.c:1282-1288`, `psi.rst:57-58`). It is the only line in the fixture whose four fields
   are not pairwise distinct, so a field swap inside that line alone is caught by P02, which
   uses a nonzero system cpu `full` with four distinct values.
3. **P12 verdict is `PRESSURE_PARTIAL`** — now explicit in amendment A3
   ("`counter_regressed` counts toward `PRESSURE_PARTIAL` like `malformed`"), exit 0.
4. **No `notes` assertions.** The shared matching rules cover exit, verdict, resources
   (key equality, `some`/`full` as subset) and `findings_include` only; there is no notes
   predicate. Per the L1 decision, A2's no-cause rule is checked on the tool by review, not by
   the fixture, so P05 asserts `state: unsupported` with `some`/`full` null and nothing about
   notes. A conforming tool that emits a factual note (for example `open failed:
   EOPNOTSUPP`) is not penalised, and A2 forbids only a *cause* inference such as "psi
   disabled".
5. **`args` use the two-token form** `["--interval", "1"]`, which works both with argparse
   and with index-based parsing of the argument list.
6. **P08 uses `avg10=abc`.** No decimal grammar and no float parse accepts it, so the case
   is malformed under either implementation style. A bare integer such as `avg10=12` would be
   ambiguous (tolerant parsers accept it) and was rejected.
7. **Values asserted only where they are unambiguous.** In P11 and P12 the fixture does not
   assert `avg10`/`total` of the reported object (the contract does not say whether the
   reported averages come from the first or the second read); it asserts the delta and ratio
   only.

## Mutation sensitivity

Per the L1 note (a field-swap parse mutant survived elsewhere because no case asserted PSI
values), every asserted line in P01 carries four pairwise-distinct values
(`avg10`, `avg60`, `avg300`, `total`), and P01 asserts the complete `some` and `full` objects
for cpu, memory and io plus the complete irq `full`. An `avg10`↔`avg300` swap, an
`avg`↔`total` swap, a `some`↔`full` swap or a per-field mis-assignment turns P01 red.
P02 carries the same property on the system cpu `full` line; P03, P06 and P07 carry it on
the line that is the subject of the case.

## Validation actually run

```
$ cd /fast/scratch/hyaku/mori-r24-a2/wt-cases
$ python3 -m json.tool tools/fixtures/mori-pressure/cases.json > /dev/null
json.tool: OK

$ python3 /tmp/freeze-cases-check.py tools/fixtures/mori-pressure/cases.json
kernel-faithful zero system cpu FULL line used in: ['P01']
OK: 12 cases, every expectation re-derived from the fixture text
```

The checker is a throwaway seat-side validator in `$TMPDIR` (not committed, not in the
clone): it re-parses every fixture file text with the kernel line grammar, re-derives each
resource state, the verdict, the exit code, the findings and the interval deltas from the
contract rules, then compares them with the assertions in the fixture, and it enforces the
pairwise-distinct rule over the whole fixture set. It found and fixed three real problems in
my first draft (zero-valued `some` lines in P01, and missing delta assertions in P11).

A separate scan confirmed that every fixture line matches
`^(some|full) avg10=D avg60=D avg300=D total=N$` with two decimals and an integer total, and
that the only deviation in the whole file is P08's deliberate `some avg10=abc ...` line.

**Not run:** `python3 -I tools/mori-pressure.py --selftest`. The tool does not exist at
`c725aa37` (`git ls-tree -r HEAD --name-only | grep pressure` is empty) and this seat is
forbidden from reading any file named `mori-pressure.py`, so the fixture was never executed
against the implementation. The C2 after-value `MORI_PRESSURE_SELFTEST: PASS 12/12` is
therefore unmeasured by me; it belongs to the tool seat and to the L1's integration gate.

## Risks

- **R1 — value expectations.** Every number asserted in the fixture comes straight from the
  fixture's own file text, so a failing value means a parse or normalisation disagreement
  between the tool and the contract, not a fixture typo. The two places where that could
  bite are judgement call 1 (system cpu `full` reported as read) and the P11 delta placement.
- **R2 — delta placement.** P11 asserts `total_delta_us`/`stall_ratio` inside the `some` and
  `full` objects, per the shared interface ("with `--interval` also `total_delta_us` int and
  `stall_ratio` float"). If the tool lifts them to the resource level, P11 fails on the key
  lookup.
- **R3 — full-line deltas.** P11 asserts `irq.full` 6000 / 0.006 and `cpu.full` null / null.
  A tool that computes deltas only for `some` lines would fail P11 on `irq.full`.
- **R4 — `elapsed_us`.** A3 allows an additive measured `elapsed_us` (null under the
  selftest's no-op sleep). The fixture does not assert it, so its presence is harmless.

## Tooling

No installs and no package or host changes were needed or made: `python3` 3.14.8 (system
interpreter) and `curl` for the two kernel sources. No pacman transaction was attempted, no
service was restarted, no `/proc`, `/sys` or cgroup file was written, and no PSI trigger was
registered.

## Blockers

None for the fixture itself. The only open dependency is the L1's integration: the fixture
must be landed before the tool's `--selftest` runs against it, and the two judgement calls
above (cpu `full` reported as read, P11 delta placement) are the places where the fixture and
the implementation can legitimately disagree.
