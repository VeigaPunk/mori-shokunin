# MoriR24.CriticC2Admission — round 24 wave 2 (falsify C2 admission)

Seat: critic, leaf, read-only on the lane. Measured tip: `a730ecfefbdb5c31b1db13aca2c40eecd5e97abc`.
Sandbox: `/fast/scratch/hyaku/mori-r24-a2/w2/CriticC2Admission/` (clone `clone/` made with
`git clone --no-hardlinks` and checked out at a730ecf; mutants under `mut/`; scripts
`mutants.py`, `bracket.py`, `bracket2.py` and `edges.py`). Tool under test: `tools/mori-pressure.py`,
sha256 `852d1ea7508004dc44690bb6e358625fbd07d89c26d4196793133559d8a773a5`, the same bytes the sibling
mutation seats measured. Host: kernel `7.2.11-arch1-1`, uid 1000, Python 3.14.8.
Installs and updates: none (no tool was needed beyond git, Python and coreutils already present).

## Verdict

The capability holds as a **one-shot system PSI read on this host**, so a Core advance is
supportable. It is not supported by `PASS 12/12` alone, and the landed wording claims more
than the bytes show. Four points:

1. **Survives:** `PASS 12/12` re-derives, the selftest can fail, and the freeze order is
   `pre-build` by commit topology.
2. **Killed as admission evidence:** the selftest never runs the real read path. Its in-process
   hook replaces `open` plus `read`, so a tool that misreads `/proc/pressure` still prints
   `PASS 12/12`. Of my 19 sandbox mutants, 19 survive the selftest, including four mutants of
   the real read path. On the code side, only the A2 live bracket check shows the capability, and the
   measured tip commits no bracket result.
3. **Not shown:** the frozen cases pin only part of the contract. The Core-relevant behaviors
   left unpinned are:
   - every resource absent gives `PRESSURE_UNAVAILABLE`;
   - the threshold fires on cpu `some`, io `some`/`full` and memory `full`;
   - the threshold fires at exactly X;
   - duplicate kinds are malformed;
   - EPERM gives `unreadable`;
   - `--warn-avg10` takes effect;
   - HIGH outranks PARTIAL;
   - cpu and io require a `full` line.
4. **Overclaim:** "frozen before the implementation" (SKILL.md registry row) and "written by a
   seat that does not see the implementation" (`contract.md:81`) state a reading and timing
   fact that the bytes cannot show. The tool seat read the cases, and both seats were
   dispatched together.

## What I ran, and what came out

### After-value and positive control

| Command (in the clone at a730ecf) | Result |
|---|---|
| `python3 -I tools/mori-pressure.py --selftest` | `MORI_PRESSURE_SELFTEST: PASS 12/12`, exit 0 |
| same, with P06 `expect.exit` flipped 1 → 0 in a sandbox copy of the cases | `MORI_PRESSURE_SELFTEST: FAIL 11/12`, `P06: exit 1 != 0`, exit 1 |

The after-value re-derives and the matcher can reject.

### Freeze order (preflight from `w1/CriticCaseIndependence.md:171-189`)

The cases did land first in commit order, and the cases blob never changed afterwards.

| Check | Result |
|---|---|
| `git cat-file -e 29c1bf45:<cases>` and the same for `<tool>` | exit 128 for both: absent at base |
| `git rev-list --merges 29c1bf45..a730ecf` | empty: no merges |
| commits touching the cases file | exactly one, `f6a29702` (05:22:43-03:00) |
| first commit touching the tool | `6ee62487` (05:25:21-03:00); `merge-base --is-ancestor f6a2970 6ee6248` exits 0 |
| cases blob at f6a2970, 6ee6248, 06a7686, 88f9620, df4db54, 6fce88a, a730ecf and 753d227 | `39cc96ab4c689ceb54e7cfaf64420056e6a289f7` at every one |
| cases blob in the seat's clone (`wt-cases` commit `51b6443`) | same blob, sha256 `aeb80ea0…ca94`; that seat's tree has no tool file (exit 128) |
| `tools/mori-freeze-order.py check` with the frozen register `.ufo/waves/round-24/frozen/c2-freeze-register.json` | exit 2, `invalid-register` (its `tip` is null; already recorded as lesson M2) |
| same, with the measurement copy `.ufo/waves/round-24/evidence/c2-freeze-check-register.json` and `--tip-for r24-C2=a730ecf…` | exit 0, `verdict: pre-build`, `co_committed: false`, `overclaim: false`, `provenance.status: bound` |

The sandbox chronology rules out "the cases were written before the implementation started":

- `wave1-attempts.json` (at a730ecf) has one row. It dispatched all 33 wave-1 tasks at
  `2026-10-22T05:14:13-03:00`, so the cases seat and the tool seat started together.
- The file mtimes are: cases `2026-10-22 05:20:27`, tool `05:24:12` (last write only).
  `wt-pressure` has no commits after `29c1bf4`.
- `w1/BuildPressureTool.md:228`: "The frozen cases were read from the other seat's clone …
  A throwaway copy of them and an early implementation copy were briefly placed under the
  private directory". When that early implementation copy was made is not recorded.

So the tool was written **against** the cases, concurrently. That is normal for an oracle,
but it means "frozen before the implementation" is true only in landed order.

### Live bracket check (A2 pass condition, run by me)

`bracket.py` and `bracket2.py` do three things on each run:

1. Read the raw `/proc/pressure/{cpu,memory,io,irq}` totals.
2. Run `python3 -I tools/mori-pressure.py`.
3. Read the raw totals again.

They then assert the A2 conditions: exit 0; all four resources `ok`; every reported `total`
between the two raw totals; `irq.some` null; cpu `full` total 0.

| Tool | Runs | Failing runs |
|---|---|---|
| landed tool | 30, then 20 more | 0 and 0 (`PRESSURE_OK`) |
| mutant M16 (real read path opens the cpu file for every resource) | 3 | 3 (memory, io and irq totals out of bracket; irq `some` not null) |
| mutant M18 (real read path swaps `some` and `full` after parsing) | 3 | 3 (every total out of bracket; cpu `full` total nonzero) |

`python3 -I tools/mori-pressure.py --interval 1` gave `PRESSURE_OK`, `elapsed_us` 1000275,
cpu `full` `stall_ratio` null, and irq `some` null.

The bracket check therefore discriminates real-path defects that the selftest cannot see.
It is not in committed bytes at the tip:

- `git ls-tree a730ecf .ufo/waves/round-24/evidence/` lists only
  `c2-freeze-check-register.json`, `freeze-order-c2.json`, `prose-fused-check.py` and
  `wave1-bind.json`.
- `w1/BuildPressureTool.md:25` says "no automatic bracket assertion was run here".
- `w1/LivePressureCapture.md:298-303` records verdicts and exit codes, not the bracket
  assertion.
- `PROVINCE.md` at a730ecf ("Admission state", appended section) reports "one live host run
  returned `PRESSURE_OK` with all four resources `ok`, `irq` `some` null and system CPU `full`
  flagged undefined". That run is verdict-level, and M16 and M18 also return exactly that.

### Mutants (sandbox, one point each, selftest plus one plain live run)

`python3 -I mutants.py <clone>`. Every one of the 19 prints `MORI_PRESSURE_SELFTEST: PASS 12/12`, exit 0.

| Mutant | What it breaks | Selftest | Plain live run |
|---|---|---|---|
| M01 | `absent` removed from the unavailable set; on a v7.2 host with PSI boot-disabled (every file ENOENT, A2), this gives PARTIAL with exit 0 instead of UNAVAILABLE with exit 2 | survives | OK (cannot reach) |
| M02 | threshold `>=` becomes `>` | survives | OK |
| M03 | cpu `some` no longer thresholded | survives | OK |
| M04 | io no longer thresholded | survives | OK |
| M05 | memory `full` no longer thresholded | survives | OK |
| M06 | duplicate kind accepted (last line wins) | survives | OK |
| M07 | EPERM mapped to `absent` | survives | OK |
| M08 | `--warn-avg10` ignored (default always used) | survives | OK |
| M09 | `stall_ratio` ignores S (P11 uses S = 1) | survives | OK |
| M10 | PARTIAL outranks HIGH | survives | OK |
| M11 | two non-ok interval reads report the second state, not the worse one | survives | OK |
| M12 | interval thresholds use the first read | survives | OK |
| M13 | cpu `full` not required | survives | OK |
| M14 | io `full` not required | survives | OK |
| M15 | `counter_regressed` checked on `some` only | survives | OK |
| M16 | real read path opens the cpu file for every resource | survives | **OK (wrong data, verdict unchanged)**; bracket check kills it |
| M17 | default root `/proc/pressures` | survives | UNAVAILABLE, exit 2 |
| M18 | real read path swaps `some` and `full` | survives | **OK (wrong data)**; bracket check kills it |
| M19 | real read path reads the first line only | survives | PARTIAL (three resources malformed) |

Sibling seats in this wave agree on the overlaps and add kills:

- **Survived:**
  - `w2/MutPsiGrammar.md:30-32`: extra fields, duplicate kinds and a negative total, 3 of 3.
  - `w2/MutPsiThresholdEdge.md`.
  - `w2/MutPsiVerdictOrder.md:59` (PARTIAL beats HIGH).
  - `w2/MutPsiMatcher.md` (the `findings_include` gate disabled).
- **Killed:**
  - `w2/MutPsiFieldSwap.md` (`FAIL 7/12`).
  - `w2/MutPsiErrnoMap.md` (P05, P10).
  - `w2/MutPsiEnoentZero.md` (P04).
  - `w2/MutPsiIrqSome.md`.
  - `w2/MutPsiCpuFullThreshold.md` (P02).
  - `w2/MutPsiCpuFullDelta.md`.
  - `w2/MutPsiRatio.md`.
  - `w2/MutPsiRegressed.md` (P12).
  - The second probe in `w2/MutPsiVerdictOrder.md:90-94` (PARTIAL exits 2, `FAIL 7/12`).

**What the 12 cases pin:**

- field parsing and the some/full assignment for the documented shapes;
- the irq full-only rule;
- the ENOENT, EOPNOTSUPP and EACCES mappings;
- the cpu `full` threshold exclusion;
- the memory `some` and irq `full` threshold arms;
- `counter_regressed` on cpu `some`;
- interval deltas at S = 1.

**What they do not pin:** the rows M01–M15 above, plus the whole real read path (M16–M19).
The cause of the real-path gap is that `_read_resource` uses `_OPEN_HOOK` whenever it is set
(`tools/mori-pressure.py:153-158`), and the selftest always sets it
(`tools/mori-pressure.py:450`).

### Real-filesystem edge cases (`edges.py`, `--root` on scratch directories, no hook)

| Case | Result | Assessment |
|---|---|---|
| E01 all four absent | UNAVAILABLE, exit 2 | correct; unpinned by the cases (M01) |
| E02 `chmod 000` on io | io `unreadable`, PARTIAL, exit 0 | correct |
| E03 memory is a directory | memory `unreadable` (EISDIR) | consistent with the docstring |
| E04 non-UTF-8 byte in io | io `unreadable` ("failed with UnicodeDecodeError") | **defect** (see below) |
| E05 CRLF line endings | `ok` | tolerated (`tools/mori-pressure.py:171`) |
| E06 empty memory file | `malformed` | correct |
| E07 trailing blank line | `malformed` | correct |
| E08 duplicate `some` | `malformed` | correct |
| E09 cpu `some` avg10 exactly 10.00 | HIGH, exit 1, cpu/some | correct |
| E10 io `some` 20 with irq absent | HIGH, exit 1 | HIGH outranks PARTIAL |
| E11 irq carries an extra `some avg10=50` line | `ok`, PRESSURE_OK, irq `some` reported | contract permits it; the kernel never emits it |
| E12 `avg10=1` with no fraction digits | `ok` | the loose grammar is already disclosed in the knowledge entry's Limits |
| E13 `--warn-avg10 2.0` | HIGH on memory/some and io/some | correct |
| E14 `full` line before `some` | `ok` | correct |

The E04 defect: a content-shape failure is reported as an access failure. The contract says
"any other shape → resource state `malformed`" and keeps `unreadable` for EACCES/EPERM. The
knowledge entry's decision table also limits `unreadable` to "Read fails `EACCES`/`EPERM`".
The cause is the catch-all `except Exception` at `tools/mori-pressure.py:162-164`. The
resource is still reported as unavailable, never zero, so this is a state-label defect, not
a zero-for-unknown defect.

## Counterexamples, impacted axes, smallest safe corrections

**K1 — `PASS 12/12` does not show that the tool reads `/proc/pressure` correctly.**

- *Counterexample:* M16 and M18 print `PASS 12/12` and give a live `PRESSURE_OK`, yet report
  the wrong numbers.
- *Evidence:* `tools/mori-pressure.py:153-158,450`; the mutant and bracket tables above.
- *Axes:* coverage (C2), calibration.
- *Smallest correction (fixable, no narrowing):* before admission, commit one A2 bracket
  record at the landed tip. It should hold the raw before-read, the tool stdout, the raw
  after-read, each assertion and its result, and the tool sha256. The Core row should cite it
  next to `PASS 12/12` as the real-read evidence, keeping its "supporting observation" label
  (A5). Without it, the Core statement "reads the four system pressure files" rests on a
  verdict-level live run that the M16 and M18 mutants also produce.

**K2 — the frozen suite under-pins the stated behavior.**

- *Counterexample:* M01–M15 (19 of 19 survive across my set; sibling seats confirm the
  grammar, threshold-edge and precedence survivors).
- *Most material is M01.* On v7.2 the only real all-unavailable shape is every file absent
  (A2). P05 pins EOPNOTSUPP, which A2 itself calls defensive. So the UNAVAILABLE / exit 2
  behavior the knowledge table and the SKILL table describe for a PSI-disabled host has no
  frozen case.
- *Axes:* coverage, calibration.
- *Smallest correction:* do not change the 12 or the after-value. Cases added now would be
  written after the tool and must not count toward the 12. The Core row and the SKILL
  registry row should list what the selftest does **not** pin (the M01–M15 behaviors).
  Pre-register freeze-first cases for those behaviors in a later round's contract if a
  stronger claim is wanted.

**K3 — provenance wording overclaims (false provenance).**

- *SKILL.md, the Round24 registry row, self-test column:* "frozen before the implementation".
  - *Evidence:* both seats were dispatched together at 05:14:13-03:00 (`wave1-attempts.json`);
    the tool seat read the cases (`w1/BuildPressureTool.md:228`); and an "early
    implementation copy" was made at an unrecorded time.
  - *Replace with:* "landed in `f6a29702`, a strict ancestor of the only tool commit
    `6ee62487`, and unchanged since (blob `39cc96ab…`); the tool was written against these
    cases; what each seat read is not shown by bytes".
- *`contract.md:81`:* "written by a seat that does not see the implementation" is the same
  claim (already flagged in `w1/CriticCaseIndependence.md:191-196`). Do not repeat it in the
  SCORECARD capability row.
- The register's own note (`frozen/c2-freeze-register.json`) is already correct ("Committed
  bytes show order only").

**K4 — the SKILL decision table cites selftest-backed behavior that the selftest does not test.**

- The rows "`some avg10` ≥ … on `cpu`, `io` or `memory`" and "`full avg10` ≥ … on `memory`,
  `io` or `irq`" are true of the tool (E09, E13), but M03–M05 survive.
- The "file breaks the line grammar (duplicate kinds, …, a non-integer or negative total)"
  row is true of the tool (E08), but MutPsiGrammar B and C survive.
- *Correction:* either cite the edge runs (E08, E09, E13) as one-off observations, or mark
  those arms "tool behavior, not pinned by the frozen cases". This is wording only.

**K5 — non-UTF-8 content becomes `unreadable` instead of `malformed`** (E04;
`tools/mori-pressure.py:162-164`).

- *Axes:* calibration (state labels).
- *Correction:* a later round maps `UnicodeDecodeError` to `malformed`. For this round,
  disclose it as a known limit in the knowledge entry's decision table. The `unreadable` row
  should not claim it covers only EACCES/EPERM, because the tool also maps EISDIR, any other
  errno and decode errors there (the tool docstring, `tools/mori-pressure.py:22-25`, says so).

**K6 — a declared deliverable is not present at the measured tip.**

- The contract C2 after-value line names "one live host run retained as evidence and a
  SCORECARD capability row".
- At a730ecf, the round-24 SCORECARD section holds only the declaration table (`git diff
  c725aa37 a730ecf -- SCORECARD.md`), and `.ufo/waves/round-24/evidence/` holds no live run.
  The live run exists only inside the wave-1 seat report `w1/LivePressureCapture.md` and in
  uncommitted scratch (`/fast/scratch/hyaku/mori-r24-a2/build-pressure-private/live-evidence.json`).
- A5 demotes the bracket check to supporting status, but it keeps the retained live run and
  the SCORECARD row as declared targets.
- *Correction:* add both at the closing tip (see K1). A judge must not treat their absence
  as met.

## Is the FR12 one-shot Core advance warranted?

Yes, conditionally. Three things are shown:

- the selftest re-derives and can fail;
- the freeze order is `pre-build` by topology with no merges and a pinned blob;
- my live bracket check passes 50 of 50 runs on a v7.2 host with all four files present, and
  it is discriminating, because it kills M16 and M18.

Two conditions must hold:

1. **K1 and K6:** a bracket record committed at the landed tip, plus a SCORECARD capability
   row.
2. **K3 and K4:** wording fixes that state the selftest's limits and drop the
   "frozen before / does not see" provenance.

A judge should reject any admission text that says or implies:

- that `PASS 12/12` shows the whole contract behavior or the real read path;
- that the cases were written independently of, or before, the implementation;
- that cases added after `6ee62487` count toward the 12.

## What must stay Frontier

These are already stated in the appended `PROVINCE.md` notes at a730ecf and are confirmed
here; none may be read as Core:

- the resident event-driven PSI trigger watcher, and cgroup-scoped cpu, io and irq pressure;
- `--interval` mode. It is outside the one-shot Core by A3, and M09, M11, M12 and M15 show
  its semantics beyond P11 and P12 are unpinned, so it must not be cited as tested beyond
  "deltas at S = 1 and one cpu `some` regression";
- threshold calibration (FR8; the 10.0 default stays labeled local);
- detection of a frozen `psi_system` through the root `cgroup.pressure` switch (knowledge
  entry U7);
- PSI-disabled and EOPNOTSUPP host behavior. It was never observed live: E01 was simulated
  with `--root`, and P05 is defensive per A2;
- portability beyond this one v7.2 host (knowledge entry U2 and U5).

## Not run, and limits

- I did not run on a PSI-disabled kernel, and I did not produce a real EOPNOTSUPP. Host
  reconfiguration is out of bounds.
- I did not audit sources S090–S097 row by row; sibling reviewers own that. I note only that
  knowledge-entry F12 and parts of F9 rest on files the entry lists as "supporting reads
  without registry rows" (`kernel/time/sched_clock.c`, `kernel/cgroup/cgroup.c`).
- I made no change in the lane apart from this report. All mutants, clones and scripts are
  under `/fast/scratch/hyaku/mori-r24-a2/w2/CriticC2Admission/`. I did not message any peer.
