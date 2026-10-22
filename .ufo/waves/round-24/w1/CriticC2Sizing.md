# CriticC2Sizing — round 24 wave 1, claim C2 (sizing and province fit)

Seat: `MoriR24.CriticC2Sizing`, critic, read-only. Written 2026-10-22 around 08:18Z.
Lane tip read: `4059ffb5` (contract landed at `29c1bf45`, entering tip `c725aa37`).
Installs and updates: none. I read `/home/vgpnk/.omp/agent/RULES.md`, and no tool was needed.

## Verdict in one paragraph

As declared, `PASS 12/12` shows that the tool agrees with the case file, and that both agree with
the L1's specification. It does not yet show that mori can read this host's pressure correctly.
That is self-agreement, not a demonstrated capability, for three reasons. First, the tool grades
itself. Second, the real file read path is replaced by a hook. Third, 2 of the 12 frozen topics
describe kernel states that `/proc/pressure` cannot produce, while a reachable state goes
untested. Reading system PSI as a one-shot runway signal does fit mori's province. The fit
breaks only where the contract labels a read error as a kernel or boot configuration cause:
that is tsukuroi's diagnosis. Most problems are fixable defects, not tradeoffs that must be
rejected. Five small corrections are listed at the end, and none of them widens the claim.

## 1. Capability or self-agreement?

**Counterexample A: the instrument judges itself, and nothing can make it fail.**
The after-value is printed by `--selftest`, and the builder seat writes that matcher inside the
tool under test (`.ufo/waves/round-24/wave1-spec.json`, item `BuildPressureTool`: "`--selftest`
loads tools/fixtures/... and prints `MORI_PRESSURE_SELFTEST: PASS n/N`"). Some matcher defects
would still print `PASS 12/12`, for example:
- treating a missing output key as a match;
- matching some/full subsets on an empty object;
- counting a case as passed before its comparison runs.

C1 declares an "Able to fail" arm with one sandbox mutant per item (`contract.md:39-41`). C2 has
none (`contract.md:43-96`). The only mutation tester in wave 1 is `MutateDispatchLedger`, which
covers C1 (wave1-spec roles list: one `mutation-tester`). So C2's declared number has no
falsifier for its own instrument.

**Counterexample B: the selftest never touches the real read path.**
Error injection, and all snapshot input, goes through "an in-process open hook" (`contract.md:76-77`).
The cases file supplies each file's text, so `PASS 12/12` never exercises:
- the real `open`/`read` of `/proc/pressure/*`;
- read errors raised by `read()` after a successful `open()` (see 2b below);
- the real kernel bytes.

The contract does mention "one live host run retained as evidence" (`contract.md:89-91`). But
the run has no predicate, so any output satisfies it. The SCORECARD row drops it entirely
(`SCORECARD.md:1502` declares only the selftest line). Two authorities therefore disagree about
what the after-value is.

**Counterexample C: two frozen topics are unreachable in the kernel, and one reachable state is missing.**
Source: the sibling-fetched `/fast/scratch/hyaku/mori-r24-a2/srcpsic/psi.c`. The `SrcPsiC` seat
fetched it at 2026-10-22T08:14:54Z, and its URL is v7.2 per the wave spec. [INFERENCE] I did not
independently confirm the tag.
- **P02 "nonzero system cpu full":** `psi.c:1282-1288` skips the averages and total for
  `group == &psi_system && res == PSI_CPU && full`, so system cpu `full` is always printed as
  zeros. Live host, `cat /proc/pressure/cpu` on 7.2.11-arch1-1:
  `full avg10=0.00 avg60=0.00 avg300=0.00 total=0`. P02 can still serve as a defensive check,
  but it tests a fabricated input, not host behaviour.
- **P05 "EOPNOTSUPP on all four":** `psi_disabled` is enabled only in `psi_init` when
  `!psi_enable` (`psi.c:228-231`, the only `static_branch_enable(&psi_disabled)` in the file).
  Under that same condition `psi_proc_init` never creates `/proc/pressure` (`psi.c:1710-1720`).
  So booting with PSI disabled produces **ENOENT on all four files** (state `absent`), not
  EOPNOTSUPP. The only EOPNOTSUPP reachable on a system file is `irq` when `!irqtime_enabled()`
  (`psi.c:1260-1262`), and it is raised from `psi_show`, which runs on read, not on open
  (`psi.c:1251-1262,1684-1691`).
- **Untested reachable state:** "whole directory absent" (booted with `psi=0`, or a kernel
  without PSI). P04 covers only `irq` absent.

Impacted axes: coverage (the claimed axis is overstated), calibration (the number certifies
conformance to the spec, not correctness on the host).

## 2. Province fit: mori's runway or tsukuroi's OS state?

**a. Reading fits mori.** The domain covers whether "its host [is] alive and progressing"
(`PROVINCE.md:3-4`). Mori owns "resource runway (... memory pressure)" (`PROVINCE.md:10`) and
Core already reads memory PSI (`PROVINCE.md:25`). PSI is the kernel's stall and progress
accounting, so extending it to CPU, IO and IRQ falls in the same class. Tsukuroi's Core lists
pacman, systemd, journal and boot triage, and drivers (`../tsukuroi-shokunin/PROVINCE.md:8-14`).
It does not list PSI. Its own text routes host-pressure correlation to mori
(`../tsukuroi-shokunin/PROVINCE.md:30-33`, ADJ-04 at `:49`). This is no duplicate authority.

**b. The cause label crosses the line.** `contract.md:61-62` maps "EOPNOTSUPP → `unsupported`
(PSI disabled)". The C2 sourcing also opens rows for "PSI Kconfig and boot parameter"
(`contract.md:94-95`). Naming why PSI is unavailable means diagnosing kernel configuration or
boot state, which mori refuses (`PROVINCE.md:12-14`: "boot state (→ tsukuroi)"). Per
section 1C, the cause label is also false: the real disabled-at-boot state reads as `absent`.
The label therefore attaches false provenance to a tsukuroi-owned fact.

**c. A missing scope boundary.** System PSI is host-wide and includes non-fleet load. A
`PRESSURE_HIGH` finding is not fleet attribution. Tsukuroi's ADJ-04 handoff explicitly asks for
"correlation, not a claim that a wave caused" it (`../tsukuroi-shokunin/PROVINCE.md:49`). The
contract states no boundary like this for C2. Also, `PROVINCE.md:10` lists only "memory
pressure" under Owns, so moving CPU, IO and IRQ PSI to Core (`contract.md:48-49`) needs that
sentence amended, or Core will exceed the Owns text.

Impacted axes: adjacency (declared held at 6, `SCORECARD.md:1504`; the cause label risks a
regression), coverage.

## 3. The one extra observation that strengthens the claim without widening it

**Live bracket check on kernel counters.** At the landed tip, run the following in one shell:
1. an independent raw read of `/proc/pressure/{cpu,memory,io,irq}`;
2. `python3 -I tools/mori-pressure.py` (default root, no `--interval`);
3. a second raw read.

The predicate holds when all of these are true:
- for every resource and kind, `raw_before.total ≤ tool.total ≤ raw_after.total`;
- `cpu`, `memory`, `io` and `irq` are each `state: ok`;
- `irq.some` is null;
- `cpu.full_system_undefined` is true;
- both raw reads show `cpu full total=0`.

Why this is the right single observation:
- **Kernel-grounded.** PSI totals are cumulative and monotonic, so the expected range comes from
  the kernel, not from a seat's written case.
- **Exercises the real path.** It covers the real `open`/`read` and real bytes that the hook in
  counterexample B skips.
- **Can fail.** On this host, raw counter windows were 0 to 2,840 microseconds over about
  0.1 seconds. The gaps between `some` and `full` totals are much larger: memory 24,675 and IO
  421,561 microseconds. A some/full swap would therefore fall outside the bracket (measured:
  memory `some` inside the `full` bracket → `False`). Dropped digits or a wrong file would also
  fail it. The command was a `python3 -I` three-read probe at 08:17:30Z, and every one of the
  7 kinds printed `bracket_ok`.
- **Not a widening.** It is the contract's own "one live host run" (`contract.md:90-91`), turned
  into a predicate. It adds no new capability, resource, mode or host write.

## 4. Universal clauses in the declaration

| Clause | Location | Finding |
|---|---|---|
| "no mori tool reads system CPU, IO or IRQ pressure" | `SCORECARD.md:1502`, `contract.md:86-87` | True for defaults: `git grep -e /proc/pressure -e cpu.pressure -e io.pressure -e irq.pressure c725aa37 -- tools SKILL.md` returned no lines. Overbroad as written: the census reads any operator-pinned PSI path (`tools/mori-census.sh:224,306-308`) and parses the same `some`/`full` grammar (`:1736-1741`). Root-cgroup files are byte-identical to the system ones on this host: `cmp /proc/pressure/$f /sys/fs/cgroup/$f.pressure` printed `same` for cpu, memory, io and irq. [INFERENCE, not run] `MORI_CGROUP_PRESSURE=/proc/pressure/cpu` would make the census read system CPU PSI, mislabeled as memory. |
| "the census reads only the user slice's `memory.pressure`" | `contract.md:46-47` | Same scope: true by default (`tools/mori-census.sh:304,308`), false under operator pins. |
| "over cases landed before the tool" / "written by a seat that does not see the implementation" | `SCORECARD.md:1502`, `contract.md:74-75` | Non-viewing is enforced only by a prompt instruction (`FreezePressureCases`: "do not open any file named mori-pressure.py"). No committed byte can prove it. Independence from the implementation is also not independence from the spec: the L1's contract fixes both the topics and the behaviour the tool implements. Commit ordering is `CriticCaseIndependence`'s question. |
| "(FR12, sourced)" in the C2 row title | `SCORECARD.md:1502` | Reads as FR12 coverage, but only the one-shot half moves. The resident watcher and cgroup-scoped CPU, IO and IRQ PSI stay Frontier (`contract.md:48-49`); the row does not say so. "Sourced" is not checked by the after-value command. |
| "EOPNOTSUPP → unsupported (PSI disabled)" | `contract.md:61-62` | False as a universal (section 1C): disabled-at-boot reads as ENOENT, and EOPNOTSUPP on system files means irq time accounting is off. |

## 5. Smallest safe corrections (fixable defects, no widening)

1. Add a C2 "able to fail" arm: sandbox mutants of the selftest matcher (always-match on a
   missing key, some/full swap, zero cases loaded), each of which must turn the selftest to
   `FAIL`. Impacted axis: calibration.
2. Make the live bracket check in section 3 part of the after-value. List it in both
   `contract.md` and the SCORECARD row so there is one authority. Impacted axes: coverage,
   calibration.
3. Relabel EOPNOTSUPP as `unsupported` with no cause. Note that PSI disabled at boot reads as
   all-`absent`, and that EOPNOTSUPP on system `irq` means irq time accounting is off.
   Route any cause question (Kconfig, `psi=` parameter, irq time accounting) to tsukuroi as a
   finding. Keep the frozen P05 topic unchanged and record it as defensive and
   kernel-unreachable; this needs no change to the targets after landing. Impacted axis:
   adjacency.
4. Narrow the "no mori tool reads" clause to "by default" or "under its own label".
   Retitle the row "FR12 one-shot system PSI only". Impacted axes: coverage, calibration.
5. Add a knowledge and province boundary line: system PSI is host-scope; it does not attribute
   a stall to the fleet and it does not diagnose the OS. Amend the Owns sentence at
   `PROVINCE.md:10` to cover CPU, IO and IRQ pressure. Impacted axis: adjacency.

Tradeoff, not a defect: keeping P02 and P05 as kernel-unreachable defensive cases is acceptable
if they are labeled as such. The judge should reject only a reading of `PASS 12/12` as evidence
of host correctness without corrections 1 and 2.

## What I did not run

- `python3 -I tools/mori-pressure.py --selftest`: neither the tool nor the cases file exists yet
  (`/fast/scratch/hyaku/mori-r24-a2/wt-pressure/tools/mori-pressure.py` and
  `wt-cases/tools/fixtures/mori-pressure` both returned "No such file or directory", and both
  clones are clean at `29c1bf4`).
- The census under an operator pin (the clause-1 counterexample is inferred from code).
- Any test on a host with PSI disabled or irq time accounting off. The section 1C kernel states
  come from the source text only.
- I did not confirm that the fetched `psi.c` matches the v7.2 tag.
