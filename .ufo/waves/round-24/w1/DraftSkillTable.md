# Draft — SKILL.md decision table and registry row (round 24, claim C2)

Seat: `MoriR24.DraftSkillTable` (leaf member; no subagent dispatch).
Mode: **draft only.** No product file was edited. The only file created in the lane repo is this
report: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-24/w1/DraftSkillTable.md`.
The lane repo, its jj state and its Git index were not mutated (read-only `git log` / `git status`
only).

---

## 1. What I read (provenance)

| Input | Location | Notes |
|---|---|---|
| round-24 contract, claim C2 | `.ufo/waves/round-24/contract.md` (read in full; C2 = "system pressure capability for CPU, IO and IRQ", axis coverage) | declares the tool CLI, the grammar, the states, the threshold, the verdict/exit map, the 12 frozen cases, the selftest string, and the FR12 boundary |
| lane SKILL.md registry table | `SKILL.md:162` header, rows `SKILL.md:164-184` | the 8-column shape is `name \| kind \| entry \| verdict map \| self-test \| pinned values \| write scope \| owner` |
| lane SKILL.md decision tables | `SKILL.md:11-21` (`## Decision table`, 4 columns: Intent / Correct surface / Never / Expected output), `SKILL.md:23-45` (`## Error patterns`, 2 columns), `SKILL.md:472-486` (r20 wave settlement, 4 columns) | house style: one row per condition, `Never` column written as imperatives with a reason |
| per-round registry tables in the same file | `SKILL.md:520` (Round21), `SKILL.md:584` (Round23) | same 8-column header repeated for round-local registries that supersede or add entries |
| fleet gate standard | `/home/vgpnk/Projects/shokunin/PROTOCOL.md:375-403` | row fields are fixed: *name, `gate\|probe`, entry command, verdict map (code → class), self-test command and spelling, pinned-value path, write scope, owner*; "A tool that cannot fail is a **probe**, and is registered as one"; `0` = clean, `1` = failed, every other code must be declared and mapped onto `clean \| failed \| could-not-evaluate`; a child lane's registry home is its own `SKILL.md` |
| frontier boundary | `PROVINCE.md:55` (FR12) | "a PSI trigger watcher is resident, not a one-shot census probe; system CPU `full=0` is not evidence of no stall" |
| PSI documentation, Linux v7.2 | `https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst` | read in full; cited by line below |
| PSI implementation, Linux v7.2 | `https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c` | read; cited by line below |
| source registry | `corpus/SOURCES.md` | the only PSI row today is **S001** (docs.kernel.org PSI page, opened 2026-10-19). No row yet covers the v7.2 `psi.rst` / `psi.c` bytes opened this round — see §5 handoff |
| repo state | `git log --oneline -3` → `4059ffb round-24: wave 1 attempt ledger, assignments and registry`, `06d4f4d round-24: bind wave 1 spec and validated dispatch payload before the call`, `29c1bf4 round-24: declare claims and contract before implementation`; `git status --short` → `?? .scratch/` (pre-existing, not mine, untouched) | tip under review: `4059ffb` |

### Primary-source facts used below (exact locations)

From `Documentation/accounting/psi.rst` (v7.2):

- `:37-38` — "Pressure information for each resource is exported through the respective file in
  `/proc/pressure/` — **cpu, memory, and io**." (the `irq` file is **not** documented here)
- `:40-43` — the file format: `some avg10=0.00 avg60=0.00 avg300=0.00 total=0` /
  `full avg10=0.00 avg60=0.00 avg300=0.00 total=0`
- `:45-46` — "some" = share of time in which **at least some** tasks are stalled
- `:48-54` — "full" = share of time in which **all non-idle tasks** are stalled simultaneously
- `:57-58` — "**CPU full is undefined at the system level**, but has been reported since 5.13, so it
  is set to zero for backward compatibility"
- `:60-63` — "The ratios (in %) are tracked as recent trends over ten, sixty, and three hundred
  second windows … The **total absolute stall time (in us)** is tracked and exported as well"
- `:67-95` — trigger registration is a **write** into the file (`<some|full> <stall us> <window us>`),
  one `open()` per trigger, `EBUSY` on reuse
- `:178-190` — cgroup2 exposes `cpu.pressure`, `memory.pressure`, `io.pressure` per cgroup

From `kernel/sched/psi.c` (v7.2):

- `:1250-1257` — `psi_show()` returns `-EOPNOTSUPP` when `psi_disabled` (PSI switched off)
- `:1259-1262` — `#ifdef CONFIG_IRQ_TIME_ACCOUNTING` / `if (!irqtime_enabled() && res == PSI_IRQ)
  return -EOPNOTSUPP;`
- `:1272-1276` — `only_full = res == PSI_IRQ;` and `for (full = 0; full < 2 - only_full; full++)`
  → the **irq** resource prints the `full` line only
- `:1281-1287` — `/* CPU FULL is undefined at the system level */` — for `group == &psi_system &&
  res == PSI_CPU && full` the averages and the total are left at zero
- `:1289-1294` — `seq_printf(m, "%s avg10=%lu.%02lu avg60=%lu.%02lu avg300=%lu.%02lu total=%llu\n", …)`
  — two decimals, `total` in microseconds
- `:1004-1014` — `psi_account_irqtime()` is the IRQ-side accounting, gated by `psi_disabled` /
  `irqtime_enabled()`
- `:1712-1717` — `proc_create("pressure/io"|"pressure/memory"|"pressure/cpu", 0666, …)` and
  `proc_create("pressure/irq", 0666, …)` **only under `#ifdef CONFIG_IRQ_TIME_ACCOUNTING`**

### Commands actually run (read-only)

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && git log --oneline -3
4059ffb round-24: wave 1 attempt ledger, assignments and registry
06d4f4d round-24: bind wave 1 spec and validated dispatch payload before the call
29c1bf4 round-24: declare claims and contract before implementation
$ git status --short
?? .scratch/
$ ls tools/            # -> census, journal-window, retention-*, wave-settlement, … ; no mori-pressure.py
$ ls tools/fixtures    # -> exit 2, "No such file or directory" (no tools/fixtures at this tip)
```

---

## 2. (a) Registry row — draft

### 2.1 Placement

**Primary:** append as the **last row of the main registry table** in `## Gates`
(`SKILL.md:162-184`, the table introduced at `SKILL.md:161` as
"Registry (PROTOCOL.md §Gate standard fields)"). This lane's registry home is this `SKILL.md`
(`PROTOCOL.md:398-403`), and the r21/r23 tables (`SKILL.md:520`, `:584`) exist to **supersede or
qualify existing rows**, which is not the case for a new tool.

**Alternative (L1's call):** a round-24 section carrying its own copy of the same 8-column table
(`| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |` +
`|---|---|---|---|---|---|---|---|`), as r21 and r23 did. If that is chosen, the row text below is
copied verbatim; only the surrounding heading changes.

### 2.2 The row (one line, exact 8-column shape)

```markdown
| system pressure (r24, C2) | gate (host-surface verdict; not a census or fleet-admission gate) | `python3 tools/mori-pressure.py [--root DIR] [--warn-avg10 X] [--interval S] [--selftest]` — `--root` defaults to `/proc/pressure`; reads `cpu`, `memory`, `io`, `irq` | 0 → clean (`PRESSURE_OK`; `PRESSURE_PARTIAL` also exits 0 and means at least one resource was unavailable or malformed) · 1 → failed (`PRESSURE_HIGH`) · 2 → could-not-evaluate (every resource unavailable, or usage error) | `python3 tools/mori-pressure.py --selftest` → `MORI_PRESSURE_SELFTEST: PASS 12/12` over `tools/fixtures/mori-pressure/cases.json` (P01–P12, frozen before the implementation); error injection (EOPNOTSUPP, EACCES) uses an in-process open hook, documented as such | `tools/fixtures/mori-pressure/cases.json` (schema `mori-pressure-cases-v1`; each case pins exit, verdict, per-resource state, `some`/`full` subsets and `findings_include` pairs); `--warn-avg10` default 10.0 is labeled local, not calibrated | none live — stdout only; reads `/proc/pressure/{cpu,memory,io,irq}` (or `--root`); no `/proc`, `/sys` or cgroup write, no PSI trigger registration, no service or package change; selftest is in-process over the frozen cases | mori |
```

### 2.3 Cell-by-cell rationale

- **name** — `system pressure (r24, C2)`: the r-tag matches the file's house convention
  (`r19 finite regressions`, `retention reconciliation schema-v2 (r23)`); the claim tag keeps it
  traceable to the round-24 contract.
- **kind** — `gate`. PROTOCOL.md:377-378: "A **gate** is a committed, re-runnable verdict script a
  lane owns … A tool that cannot fail is a **probe**, and is registered as one."
  `mori-pressure.py` **can fail** (exit 1 on `PRESSURE_HIGH`), so `gate` is the reading that follows
  the protocol text; the parenthetical records that it grades a host surface and gates nothing in
  the fleet. See §6 conflict 2 for the alternative.
- **entry** — the four CLI flags declared by contract C2, plus the default `--root /proc/pressure`
  and the four file names, so the row is runnable from the registry alone.
- **verdict map** — code → class, as PROTOCOL.md:379-384 requires. `0` = clean, `1` = failed are
  fleet-wide conventions; `2` is declared here and mapped onto `could-not-evaluate` (usage error, or
  every resource unavailable — nothing could be evaluated). The `PRESSURE_PARTIAL` clause is written
  into the `0` cell because the contract fixes PARTIAL at exit 0; see §6 conflict 1.
- **self-test** — the exact flag spelling `--selftest` (protocol: the spelling is lane-owned but the
  registry must record it), the exact expected output string `MORI_PRESSURE_SELFTEST: PASS 12/12`,
  the frozen case file, and the documented in-process open hook for EOPNOTSUPP/EACCES injection.
  The frozen cases also serve the "two evidences" clause (PROTOCOL.md:391-394): the live surface
  (`/proc/pressure`) is mutable by nature, so the committed case file with committed expected
  verdicts is the frozen-input arm.
- **pinned values** — the frozen case file and its schema; the per-case matching rule (exit and
  verdict exact, each `expect.resources.<r>` key equal, expected objects under `some`/`full` matched
  as subsets, every `[id, resource]` pair in `findings_include` present in `findings`); and the
  labeled-local threshold default.
- **write scope** — `none live`, stdout only; the reads are named; the three prohibitions
  (`/proc`/`sys`/cgroup writes, PSI trigger registration, service/package change) are stated
  because the contract bounds them and because PSI trigger registration is a *write* to the same
  files (`psi.rst:67-95`).
- **owner** — `mori`, as every other row in the table.

### 2.4 Facts the row must not imply

- The row is **prospective at the reviewed tip**: `tools/mori-pressure.py` and `tools/fixtures/`
  do not exist at `4059ffb` (evidence above). The row may only land together with the tool and the
  frozen cases; it must not be read as a statement that the capability exists now.
- The row claims **no census integration**: nothing in the contract wires this tool into
  `tools/mori-census.sh`, so it adds no `SURFACE` row, no finding id in the census vocabulary and no
  DRIFT verdict — the same posture as the r16 window probe (`SKILL.md:105-108`).
- The row claims **no threshold calibration**: `--warn-avg10 10.0` is a labeled-local placeholder,
  like `psi_warn_avg10` in the census (`SKILL.md:41`).

---

## 3. (b) Decision table draft — `Reading system pressure`

Proposed new section (title and placement are L1's call; the natural home is a new
`## Round24 — one-shot system pressure read (C2)` section near the end of `SKILL.md`, after the
round-23 section at `SKILL.md:567-609`, so it does not disturb the round-21/round-23 registry
tables):

```markdown
## Round24 — one-shot system pressure read (C2)

`python3 tools/mori-pressure.py` reads the **system** pressure files `/proc/pressure/{cpu,memory,io,irq}`
once (or twice with `--interval S`) and returns a verdict. It is detection and report only: it
never writes to `/proc`, `/sys` or a cgroup, never registers a PSI trigger, and never changes a
service. The resident trigger watcher and cgroup-scoped CPU/IO/IRQ pressure stay Frontier
(`PROVINCE.md:55`).

### Reading system pressure

| Condition | Report as | Never infer |
|---|---|---|
| system `/proc/pressure/cpu` shows `full avg10=0.00 … total=0` | `cpu.full` reported with `full_system_undefined: true`; the value is never a threshold input | that the CPU had no full stall — system CPU `full` is undefined and exported as zero for backward compatibility ([psi.rst:57-58](https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst); [psi.c:1281-1287](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)) |
| `some avg10` ≥ `--warn-avg10` on `cpu`, `io` or `memory` | finding `PRESSURE_HIGH` naming the resource and the kind; the threshold is labeled local, not calibrated | that the fleet, a lane or a task caused the stall — `/proc/pressure/*` is system-wide ([psi.rst:37-38](https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst)); per-cgroup numbers live in the cgroup2 `*.pressure` files ([psi.rst:178-190](https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst)) |
| `full avg10` ≥ `--warn-avg10` on `memory`, `io` or `irq` | finding `PRESSURE_HIGH` on the `full` kind of that resource | that `full` means "all non-idle tasks stalled" for `irq` — that wording is the documented cpu/memory/io definition ([psi.rst:48-54](https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst)); the `irq` resource is exported only by the kernel code and is not described in `psi.rst` |
| the `irq` file carries no `some` line | `irq.some = null`, resource state `ok` | that irq "some" pressure is zero, or that a missing `some` line is malformed — the kernel prints only the `full` line for `PSI_IRQ` ([psi.c:1272-1276](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c), [psi.c:1289-1290](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)) |
| `/proc/pressure/irq` cannot be opened (ENOENT) | resource state `absent` | that there was no IRQ pressure — the file is created only under `CONFIG_IRQ_TIME_ACCOUNTING` ([psi.c:1716-1717](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)) |
| the read returns EOPNOTSUPP | resource state `unsupported` (PSI disabled, or IRQ time accounting off) ([psi.c:1256-1262](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)) | a zero reading — unavailable is never zero |
| the read returns EACCES/EPERM | resource state `unreadable` | a zero reading |
| any resource is `absent`, `unsupported` or `unreadable` | that resource is unavailable; verdict `PRESSURE_PARTIAL` (exit 0) unless every resource is unavailable → `PRESSURE_UNAVAILABLE` (exit 2) | that the resources that did read describe the whole system, or that partial coverage is a clean bill of health |
| the file breaks the line grammar (duplicate kinds, a missing required kind, a non-decimal avg, a non-integer or negative total) | resource state `malformed` | that the missing or unparsable value was low or zero — a malformed file is not a low-pressure reading; `total` is cumulative stall microseconds and `avg*` are percentages over 10/60/300 s windows ([psi.rst:40-43](https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst), [psi.rst:60-63](https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst), [psi.c:1289](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)) |
| two reads with `--interval S` | `total_delta_us` and `stall_ratio` per kind; a decreasing total → resource state `counter_regressed` | that pressure fell because the counter decreased, or any stall duration from a single `total` without a delta |
| one-shot read (no `--interval`) | a point-in-time sample: system-wide stall percentages plus cumulative stall microseconds | that no stall happened between reads — a PSI trigger watcher stays Frontier (`PROVINCE.md:55`), and writing a trigger into `/proc/pressure/*` is a host write this lane never performs ([psi.rst:67-95](https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst)) |
```

### 3.1 Row coverage check against the contract and the sources

| Contract C2 clause | Covered by table row |
|---|---|
| `full_system_undefined: true`, never a threshold, never evidence of no stall | row 1 (and `PROVINCE.md:55`) |
| `some` of cpu/io/memory, `full` of memory/io/irq at/over `--warn-avg10` | rows 2, 3 |
| irq `some` missing is expected, `some: null`, never malformed | row 4 |
| ENOENT → absent; EOPNOTSUPP → unsupported; EACCES/EPERM → unreadable; all three unavailable, never zero | rows 5, 6, 7, 8 |
| duplicate kinds / missing required kinds / other shape → malformed | row 9 |
| `--interval S` → `total_delta_us`, `stall_ratio`; decreasing total → `counter_regressed` | row 10 |
| one-shot reading only; trigger watcher and cgroup-scoped pressure stay Frontier | rows 2, 11 |

### 3.2 Shape note

The table above uses `Condition | Report as | Never infer` — the shape the assignment asks for.
It is deliberately **not** folded into the existing `## Decision table`
(`SKILL.md:11-21`, columns Intent / Correct surface / Never / Expected output) nor into
`## Error patterns` (`SKILL.md:23-45`): those tables are lane-wide contracts with fixed column
sets, and a third column set inside them would break the file's own shape. The 4-column r20 table
(`SKILL.md:476-486`) shows the house precedent — a round-scoped table in its own section.

---

## 4. Out of scope for this seat (hand-off to the integration owner)

These are C2 surfaces named by the contract that are **not** the SKILL.md table/row and that I did
not draft, to avoid colliding with other seats:

1. **`SCORECARD.md` capability row** — contract C2 requires "a SCORECARD capability row". The
   lane root has `SCORECARD.md`; I did not draft a row there.
2. **`corpus/knowledge/system-pressure-r24.md`** — the knowledge entry; another seat owns it.
3. **`corpus/SOURCES.md` rows for the sources opened this round** — the contract requires the
   knowledge entry and the decision table to cite "SOURCES.md rows opened this round (Linux v7.2 PSI
   documentation and `kernel/sched/psi.c`, cgroup-v2 pressure files, PSI Kconfig and boot
   parameter, proc_pressure(5))". Today only **S001** exists (the docs.kernel.org PSI page, opened
   2026-10-19, `corpus/SOURCES.md:7`); there is no row for the v7.2 `psi.rst` / `psi.c` bytes I
   opened. My table therefore cites the v7.2 URLs inline, and new `SOURCES.md` rows (e.g. S090+)
   still have to be minted by whoever owns that file. I did not edit `SOURCES.md`.
4. **C1 surfaces** — the `QUALITY.md` criterion lines tagged `routed r23-R<n>` belong to C1, not
   here.
5. **The tool and the frozen cases** — `tools/mori-pressure.py` and
   `tools/fixtures/mori-pressure/cases.json` are the build seat's and the freeze seat's; my row and
   table are text drafts only.

---

## 5. Conflicts and open decisions for the canonical judge

**Conflict 1 — `PRESSURE_PARTIAL` exits 0, and 0 means "clean".**
PROTOCOL.md:379-384: "`0` = `clean` and `1` = `failed` fleet-wide". Contract C2 fixes
"Exit 1 on `PRESSURE_HIGH`; exit 2 when every resource is unavailable or on usage error; **else exit
0** (PARTIAL means at least one resource unavailable or malformed)". So a run where, say, `io` was
unreadable exits 0 — `clean` by the outer interface — while the measurement is incomplete. The
draft resolves this by declaring the class *inside* the `0` cell of the verdict map
("`PRESSURE_OK`; `PRESSURE_PARTIAL` also exits 0 and means at least one resource was unavailable or
malformed") rather than by silently calling PARTIAL clean. The judge may prefer a different outer
mapping; the contract's exit codes are not mine to change.

**Conflict 2 — `gate` vs `probe` for the kind cell.**
PROTOCOL.md:377-378 makes "cannot fail" the probe test, and this tool can fail (exit 1), which
pushes to `gate`. But the same paragraph defines a gate as one that "compares them against expected
values persisted in its own repo", and `--warn-avg10`'s default 10.0 is a labeled-local constant,
not a repo-persisted expected value — the tool has no committed expected verdict for a live host
surface. The draft uses `gate` with the parenthetical "host-surface verdict; not a census or
fleet-admission gate". The defensible alternative is `probe` with the same verdict map declared
verbatim (PROTOCOL.md:382-383 requires every non-0/1 code to be declared in the registry entry
either way). L1 picks one; the rest of the row is unchanged.

**Conflict 3 — the `irq` surface is code-level, not documentation-level.**
`psi.rst` v7.2 documents only `cpu`, `memory`, `io` (`psi.rst:37-38`). `/proc/pressure/irq` exists
only because `kernel/sched/psi.c:1716-1717` creates it under `CONFIG_IRQ_TIME_ACCOUNTING`, and its
`full`-only shape comes from `psi.c:1272-1276`. Consequence for the table: the `irq` row and the
`irq full` threshold row are grounded in code, not in the documentation, and the "all non-idle tasks
stalled" wording of `psi.rst:48-54` is **not** transferred to `irq`. I flagged this in the table
itself rather than in a footnote.

**Conflict 4 — threshold semantics for `irq full`.** Contract C2 puts `irq` `full` in the threshold
set. `psi.rst` never defines the irq resource, so the row reports a `PRESSURE_HIGH` finding on
`irq full` as a *kernel-exported* value without attaching the cpu/memory/io "full" semantics to it.
Whether `irq full` should carry its own threshold at all is a contract decision; the draft follows
the contract.

---

## 6. Tooling

**No installs or upgrades were performed** for this seat. The task needed only repository reads
(`read`, `grep`), two read-only `git` commands and two web reads of the upstream v7.2 files; the
pre-existing `python3`/`git`/`rg` toolchain was sufficient. Nothing was installed, nothing was
upgraded, and no host service was touched.

---

## 7. Summary of deliverables

| Deliverable | Where in this report | State |
|---|---|---|
| (a) registry row for `tools/mori-pressure.py` in the exact 8-column shape | §2.2 (row text), §2.3 (cell rationale), §2.1 (placement) | draft, unlanded |
| (b) decision table `Reading system pressure` (condition → report as → never infer) | §3 (table text), §3.1 (coverage check against contract C2), §3.2 (shape note) | draft, unlanded |
| Grounding | §1 primary-source facts (psi.rst and psi.c line citations), cited inline in every table row | verified against the two upstream v7.2 files |
| Conflicts | §5, four items for the judge | open |
| Handoffs | §4, five items | open |

No file in the lane repo other than this report was created or modified.
