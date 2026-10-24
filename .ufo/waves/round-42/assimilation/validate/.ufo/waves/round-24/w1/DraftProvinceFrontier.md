# DraftProvinceFrontier — round 24 wave 1, claim C2 (PROVINCE.md Core/Frontier, corpus/README.md Frontier)

Seat: `MoriR24.DraftProvinceFrontier` (scribe, leaf member — no subagent dispatch).
Claim: **C2**, axis coverage, frontier **FR12**. Date 2026-10-22.
Mode: **draft only.** No lane product file was edited. The only file created inside the lane repo
is this report.

Inputs read (all read-only):

| Input | Location | Note |
|---|---|---|
| PROVINCE.md Core/Frontier | `PROVINCE.md:20-58` (Core list 22-27, Round-15/16 paras 29-40, `## Frontier` 42, FR1..FR14 44-57) | 232 lines total |
| corpus/README.md Frontier | `corpus/README.md:328-346` (`## Frontier` 328, table head 330, FR1..FR14 332-345) | 443 lines total |
| round-24 contract, claim C2 | `.ufo/waves/round-24/contract.md` (C2 **51-102**; Bounds **104-108**; **amendments A1 35-40, A2 110-124, A3 126-135, A4 137-158**) | re-read after the A1-A4 amendments landed |
| lane tip | `06a7686` (`round-24: freeze-order measurement register copy for C2`); tool `6ee6248`; frozen cases `f6a2970`; contract `29c1bf4`, A1 `f38dbbd`… | `git log --oneline -6` |
| sibling wave-1 findings used as relayed (not re-verified by me) | `.ufo/waves/round-24/w1/CriticC2Semantics.md` (F1-F7), `CriticIntervalBoundary.md`, `CriticC2Sizing.md`, `ConnectSiblingPsi.md`, `SrcKconfig.md`, `SrcPsiIrqCommit.md`, `SrcKernelParams.md`, `DraftSkillTable.md` | cited only where the draft text depends on them; each is labelled |

---

## 1. Bottom line

The one-shot **system** PSI read (`/proc/pressure/{cpu,memory,io,irq}`) is drafted into **Core,
pending admission**; FR12 keeps the **resident PSI trigger watcher** and **cgroup-scoped
CPU/IO/IRQ pressure**. Because the assignment is append-only and forbids rewriting older lines,
the whole advance is drafted as a **new appended section at the end of each file**, in the lane's
round-NN style — not as an edit of the Core bullet list, not as an edit of the FR12 row
(`PROVINCE.md:55`, `corpus/README.md:343`), and not as an edit of the `Owns` sentence
(`PROVINCE.md:6-10`). Those three lines stay byte-unchanged; the appended sections carry the
advance, the narrowed FR12 remainder, and the Owns-scope extension. Option B (an in-place FR12
row rewrite, the round-16 precedent) is drafted too, in §4, clearly marked as *not* append-only and
with its pointer-rot cost stated.

Measured by me (read-only, at tip `06a7686`):

```
$ python3 -I tools/mori-pressure.py --selftest
MORI_PRESSURE_SELFTEST: PASS 12/12      # exit 0
$ python3 -I tools/mori-pressure.py      # live host, default --root /proc/pressure
verdict PRESSURE_OK                      # exit 0; cpu/memory/io/irq all state=ok;
                                         # irq.some = null; cpu.full_system_undefined = true;
                                         # threshold 10.0, label "local (not calibrated)"
$ python3 -I tools/mori-pressure.py --interval 0.5
elapsed_us 500255                        # added cost ~= S; cpu.full total_delta_us=null, stall_ratio=null
$ git cat-file -e c725aa37:tools/mori-pressure.py
fatal: path 'tools/mori-pressure.py' exists on disk, but not in 'c725aa37'   # rc 128
```

---

## 2. Draft A — `PROVINCE.md`, appended at end of file (after line 232)

### 2.1 Draft text (paste verbatim)

```markdown

## Round-24 appended scope notes (2026-10-22)

- **Core, one-shot system pressure reading (FR12 partial advance, admission pending):**
  `tools/mori-pressure.py` (round-24 build) reads the four **system** pressure files
  `/proc/pressure/{cpu,memory,io,irq}` once each and reports one JSON object
  (`schema: mori-pressure-v1`): a per-resource `state` (`ok`, `absent`, `unsupported`,
  `unreadable`, `malformed`, `counter_regressed`), the `some`/`full` averages and the
  cumulative `total`, a `verdict` (`PRESSURE_OK` | `PRESSURE_HIGH` | `PRESSURE_PARTIAL` |
  `PRESSURE_UNAVAILABLE`) and `findings[]` (`PRESSURE_HIGH` at or above `--warn-avg10`,
  default 10.0, **labeled local, not calibrated**). System CPU `full` is reported with
  `full_system_undefined: true` and is never a threshold input and never evidence of no
  stall; the `irq` resource carries `full` only, so its absent `some` line is expected
  (`some: null`) and never malformed. Unavailable is never zero: `absent`, `unsupported`
  and `unreadable` are named states and **no cause is inferred** from them — kernel and
  boot configuration diagnosis belongs to tsukuroi. The reading is host scope: a
  system-wide `PRESSURE_HIGH` is evidence to correlate, never proof that a lane, a wave
  or the fleet caused it. Read-only: the probe opens the PSI files read-only, registers
  no PSI trigger, writes nothing to `/proc`, `/sys` or a cgroup, and changes no service
  or package. It is not a census surface: no `SURFACE` row, no census finding id, no
  DRIFT verdict, no baseline re-pin; by default the census keeps reading only the
  user-slice `memory.pressure` it already reads (an operator can pin
  `MORI_CGROUP_PRESSURE` elsewhere). Knowledge: `corpus/knowledge/system-pressure-r24.md`
  (lands with this round); sources opened this round are the Linux v7.2 PSI
  documentation, `kernel/sched/psi.c`, the cgroup-v2 pressure files, the PSI Kconfig and
  boot parameter, and `proc_pressure(5)`.
- **Still FR12 frontier:** the resident, event-driven PSI trigger watcher and
  **cgroup-scoped** CPU/IO/IRQ pressure. A trigger watcher is a *write* of a threshold
  into `/proc/pressure/*` plus a polling process, not a one-shot read, and the
  per-cgroup `*.pressure` files are a different scope; the one-shot system read above
  observes neither. The opt-in `--interval S` two-sample mode is **outside** the one-shot
  Core statement: its added cost is about S seconds and it fails the round-8 dwell rule
  (`corpus/knowledge/surfaces-r8.md:47-48`), so a stall rate and its latency budget stay
  with FR6/FR12. FR12 is narrowed here, not closed.
- **Limits carried with the Core row:** a zero or non-advancing `total` is not evidence of
  no stall — the root cgroup's `cgroup.pressure` switch can stop `psi_system` accounting
  while `/proc/pressure/*` stays readable, and the probe does not detect that (wave-1
  finding `CriticC2Semantics.md` F3; the upstream anchors are carried by the knowledge
  note); the threshold is a local placeholder, so FR8 stays open; `avg10` is a decaying
  average, not a ten-second window; and the `full` arm of memory and IO adds no verdict
  information beyond their `some` arm at an equal threshold (`CriticC2Semantics.md` F4).
- **Owns-scope extension (append-only; `PROVINCE.md:6-10` is left byte-unchanged):** the
  Core row above extends the owned read-only probe list named at `PROVINCE.md:6-10`,
  which today names memory pressure, to the one-shot system CPU/IO/IRQ/memory pressure
  read. The header sentence itself is not rewritten by this round; the extension is
  recorded here so no sibling line-range pointer into `PROVINCE.md:3-16` moves.
- **Adjacent tsukuroi (shared file, shared evidence, not shared ownership):** tsukuroi's
  own census reads the system `/proc/pressure/memory` file
  (`../tsukuroi-shokunin/tools/tsukuroi-census.sh:376`, `:1100-1115`) for OS memory
  triage. Two lanes reading one kernel file is not a contest: mori reads and reports
  host pressure for fleet correlation, tsukuroi retains OS memory, journal and boot
  diagnosis. A `PRESSURE_HIGH` on `irq` that needs device or driver attribution routes
  to tsukuroi's driver plane. This advance closes neither tsukuroi's pre-kill PSI
  capture gap nor mori's FR12.
- **Admission state (2026-10-22):** the tool and its twelve frozen cases are landed
  (`tools/mori-pressure.py`, `tools/fixtures/mori-pressure/cases.json`); the declared
  after-value command prints `MORI_PRESSURE_SELFTEST: PASS 12/12` (exit 0) and one live
  host run returned `PRESSURE_OK` with all four resources `ok`, `irq` `some` null and
  system CPU `full` flagged undefined. The Core row above is **pending admission** by the
  L1. No frontier row is closed, no other lane's surface is claimed, and no remediation
  is added.
```

### 2.2 Why the append rather than an in-place Core bullet

- The lane's own later-round style is exactly this: rounds 17, 18 and 20 added Core
  capabilities as `**Core, …**` bullets inside an appended section
  (`PROVINCE.md:96-120`, `:123-141`, `:143-160`) without touching the Core bullet list.
  Round 23 likewise recorded a disposition in an appended section
  (`PROVINCE.md:211-232`, the file's last lines).
- Editing `PROVINCE.md:6-10` (the `Owns` sentence) or inserting a Core bullet inside
  `PROVINCE.md:22-27` would either rewrite an older line or shift every later line
  number. `tsukuroi-shokunin/PROVINCE.md:33,49,50` cite `../mori-shokunin/PROVINCE.md:6-16`,
  `:3-16` and `:12-16` as live evidence; wave-1 seat `ConnectSiblingPsi.md` (§"Proposed
  move") records the same constraint. The append keeps all three ranges resolving.
- `CriticC2Sizing.md` §2c flagged that Core would otherwise exceed the `Owns` text; the
  "Owns-scope extension" bullet above closes that gap **without** rewriting the header.

### 2.3 Facts the draft text depends on, with anchors

| Draft statement | Anchor | Kind |
|---|---|---|
| four system files, one read each, `mori-pressure-v1` schema, states, verdict set, exit map | `tools/mori-pressure.py:66-70`, `:91-97`, `:112-118`, `:312-345` | observed in the landed bytes |
| `PRESSURE_HIGH` at `--warn-avg10`, default 10.0, label "local (not calibrated)" | `tools/mori-pressure.py:353-355`, `:382`, `:283-311`; `contract.md:70-71` | observed / contract |
| system CPU `full` flagged undefined, never a threshold input | `tools/mori-pressure.py:194`, `:211-212`; contract `:66-67`; `psi.rst:57-58`; `psi.c:1282-1288` | observed + upstream |
| `irq` `full` only, `some` null expected, never malformed | contract `:64-65`; `psi.c:1273-1275` (`only_full = res == PSI_IRQ`), `:1277` (the `2 - only_full` loop), `:1290-1291` (the `full || only_full ? "full" : "some"` label); `SrcPsiIrqCommit.md` (Linux 6.1, `52b1364ba0b1`) | contract + upstream |
| unavailable never zero; `unsupported` carries no cause | contract `:68-69`; **amendment A2** (`contract.md:112-117`); `tools/mori-pressure.py:141-142` | contract + observed |
| read-only, no trigger, no write, no service change | contract "Bounds" `:104-108`; `tools/mori-pressure.py:157`, `:504` (both `open(path, "r")`); `psi.rst:77-83` (registering a trigger requires *writing* the threshold into the PSI file) | observed + upstream |
| not a census surface; census keeps reading only user-slice `memory.pressure` | `tools/mori-census.sh:308`, `:1735-1762`; `ScoutCensusPsi.md` §1-2 | observed |
| host scope; not fleet attribution | amendment A2 (`contract.md:122`); `ConnectSiblingPsi.md` contradiction 2 | contract + sibling finding |
| `--interval` outside the one-shot Core statement, ≈S added cost, fails the r8 dwell rule | amendment A3 (`contract.md:128-129`); `corpus/knowledge/surfaces-r8.md:47-48`; `CriticIntervalBoundary.md` §1 (measured `S=0.05` → 50.1 ms added); my own `--interval 0.5` run: `elapsed_us 500255` | contract + upstream + measured |
| root `cgroup.pressure=0` silent-zero limit | `CriticC2Semantics.md` F3 (relayed; upstream anchors `psi.h:37-40`, `cgroup.c:4123-4133`, `:5585-5589`) | relayed finding, not re-verified by me |
| `full` arm of memory/IO adds no verdict information | `CriticC2Semantics.md` F4 (relayed) | relayed finding |
| before-value absent at `c725aa37` | `git cat-file -e c725aa37:tools/mori-pressure.py` → rc 128 | measured |
| after-value `PASS 12/12` | `python3 -I tools/mori-pressure.py --selftest` at `06a7686` | measured |
| tsukuroi's census also reads system `/proc/pressure/memory` (shared evidence) | `../tsukuroi-shokunin/tools/tsukuroi-census.sh:376`, `:1100-1115` (read by me) | observed |
| sibling line-range pointers that must keep resolving | `tsukuroi-shokunin/PROVINCE.md:33,49,50` cite `../mori-shokunin/PROVINCE.md:6-16`, `:3-16`, `:12-16` | observed |

### 2.4 Wording risks the L1 must rule on

1. **"pending admission" is load-bearing.** The tool, cases and selftest are landed and
   measured, but the *admission* of a Core row is the L1's act. The draft says "admission
   pending" in the heading and in the admission-state bullet so the text cannot be read
   as an admitted capability before the L1 signs it. If the L1 prefers the row to read
   as admitted at landing, delete only the two "pending" phrases — do not delete the
   admission-state bullet, which carries the before/after receipts.
2. **"memory" in the Core row is the *system* memory PSI**, not the user-slice
   `memory.pressure` the census already reads under `SURFACE cgroup`. The draft says
   "system" in the first sentence and "by default the census keeps reading only the
   user-slice `memory.pressure` it already reads", so the two scopes cannot be
   conflated. This distinction is the one thing `ScoutCensusPsi.md` §5 item 8 flags as a
   coverage trap.
3. **The `Owns`-scope extension is a claim about scope, not a rewrite.** If the L1 later
   amends `PROVINCE.md:6-10` in place, the appended bullet must be replaced by a
   pointer, not left to contradict the header.
4. **The `CriticC2Semantics.md` F3/F4 limits are relayed, not independently re-verified by
   me.** I did not open `include/linux/psi.h` or `kernel/cgroup/cgroup.c`. The draft
   attributes them to the wave-1 finding and to the knowledge note (which is where the
   upstream anchors belong), which is the honest form until that note lands.
5. **Do not let the `PRESSURE_HIGH` exit code become a fleet gate.** `ConnectSiblingPsi.md`
   §"Risks" notes that if a dispatcher consumed exit 1, a labeled-local threshold would
   become a dispatch control, which crosses mori's refusal of dispatch mechanism
   (`PROVINCE.md:12-16`). The draft contains no such consumer and claims none.

---

## 3. Draft B — `corpus/README.md`, appended at end of file (after line 443)

### 3.1 Draft text (paste verbatim)

```markdown

## Round-24 coverage additions — C2 one-shot system pressure (admission pending)

| Ground | Entry | Bounded advance |
|---|---|---|
| One-shot system pressure read (FR12 partial advance) | `knowledge/system-pressure-r24.md` | System `/proc/pressure/{cpu,memory,io,irq}` read once per resource with per-resource states (`ok`, `absent`, `unsupported`, `unreadable`, `malformed`, `counter_regressed`), a `PRESSURE_OK`/`PRESSURE_HIGH`/`PRESSURE_PARTIAL`/`PRESSURE_UNAVAILABLE` verdict and `PRESSURE_HIGH` findings against a labeled-local, uncalibrated `--warn-avg10` (default 10.0). System CPU `full` is reported undefined and is never evidence of no stall; `irq` carries `full` only, so its absent `some` is expected, not malformed; unavailable is never zero and no cause is inferred from it. Host scope: a system-wide high reading is not evidence that the fleet caused it. Read-only: no PSI trigger, no write to `/proc`, `/sys` or a cgroup, no service or package change. No census surface, no census finding id, no baseline re-pin. The resident PSI trigger watcher and cgroup-scoped CPU/IO/IRQ pressure stay frontier, as does the two-sample `--interval` stall rate (its added cost is about S seconds and it misses the round-8 dwell budget). |

## Round-24 Frontier note — FR12 narrowed, not closed

The FR12 row above (`corpus/README.md:343`) and its PROVINCE counterpart (`PROVINCE.md:55`)
are byte-unchanged by this round. This appended note records what the round-24 C2 advance
changes about FR12's scope:

- **Advanced to Core (pending admission):** the one-shot read of the **system** pressure
  files `/proc/pressure/{cpu,memory,io,irq}` (`tools/mori-pressure.py`). This is the
  reading the frontier row always excluded from a *census* probe; it is a separate
  read-only probe, not a census surface, and it adds no `SURFACE` row, no census finding
  id, no DRIFT verdict and no baseline re-pin.
- **Still frontier, unchanged:** the resident, event-driven PSI trigger watcher — a
  threshold written into `/proc/pressure/*` plus a polling process — and the
  **cgroup-scoped** CPU/IO/IRQ pressure files. Neither is observed by the new probe. The
  two-sample `--interval` stall rate also stays frontier with FR6: its added cost is
  about S seconds and it does not meet the round-8 dwell rule
  (`corpus/knowledge/surfaces-r8.md:47-48`).
- **Boundaries that travel with the Core row:** the system CPU `full` line stays
  undefined (`full_system_undefined: true`) and is never read as evidence of no stall; a
  missing, unsupported or unreadable file is an unavailable state and never a zero
  reading, with no cause inferred from it (boot and kernel configuration diagnosis is
  tsukuroi's); the threshold is a labeled-local placeholder, so FR8 stays open; the
  reading is host scope, so a high value is evidence to correlate, never proof that a
  lane, a wave or the fleet caused it.
- **Open at the FR12 boundary:** the root-cgroup `cgroup.pressure` switch can stop
  `psi_system` accounting while `/proc/pressure/*` stays readable, so a zero or
  non-advancing `total` is not evidence of no stall and the probe does not detect that
  case (wave-1 finding `CriticC2Semantics.md` F3; the upstream anchors belong to
  `knowledge/system-pressure-r24.md`).

No frontier row is closed by this round, and no quota, retention, wave-settlement or
telemetry ground is touched.
```

### 3.2 Placement and pointer cost

- The appended section goes **after `corpus/README.md:443`**. Nothing above line 443
  moves, so `corpus/README.md:343` (FR12) keeps its line number, and the coverage-map
  pointers used inside the lane (`corpus/README.md:7`, `:13-14`, `:16-18`, `:41`) are
  untouched.
- The new knowledge entry is listed in the appended table, **not** inserted into the
  top coverage-map table (lines 5-41). That is the lane's own recent style: rounds 17,
  19, 20, 22 and 23 all recorded new notes in appended sections rather than editing the
  coverage map (e.g. `corpus/README.md:355` in the round-17 section, `:387` in the
  round-19 section, `:401` in the round-20 section, `:420` in the round-22 section).
  Inserting a coverage-map row would shift lines 42+ and make the
  `corpus/README.md:41` pointer stale — that line is cited from the round-16 wave report
  `.ufo/waves/round-16/build/AttackPreservation.md:236`, and the coverage-map range is
  cited from live notes (`corpus/knowledge/observability-surfaces-r2.md:18,185,305,379`;
  `silence-grading-r2.md:43`; `progressing-weak-r2.md:20`; `silence-cutover-r3.md:19`).
- `knowledge/system-pressure-r24.md` **does not exist at the tip I read** (`06a7686`);
  the wave-1 seat `DraftKnowledgeEntry` is drafting it. Under QUALITY 9 the row may land
  only together with the note, or with the note's path replaced by the tool path. I
  flagged this rather than writing a dangling pointer.

---

## 4. Option B (NOT append-only) — in-place FR12 row rewrite, for the L1 only

The round-16 precedent rewrote the FR11 rows in place (`PROVINCE.md:54`,
`corpus/README.md:342`). If the L1 prefers that shape for FR12, the replacement text
below is the same content in one row each. **This is a rewrite of older lines**: it
changes the bytes of `PROVINCE.md:55` and `corpus/README.md:343` and leaves every
pointer into those rows stale, so it is offered as an explicit alternative, not as the
draft.

`PROVINCE.md:55` replacement:

```markdown
- **FR12 — Event-driven pressure and CPU/IRQ PSI** (art F4). First evidence: `corpus/SOURCES.md:7-8,16`; `corpus/lessons/2026-10-15-free-lunch-measurements-counter-baselines.md:57-73`. Boundary: a PSI trigger watcher is resident, not a one-shot census probe; system CPU `full=0` is not evidence of no stall. Round 24 advances only the one-shot **system** read of `/proc/pressure/{cpu,memory,io,irq}` (`tools/mori-pressure.py`, admission pending) to Core; the resident trigger watcher, cgroup-scoped CPU/IO/IRQ pressure and the two-sample `--interval` stall rate stay frontier, and no census surface, finding id or baseline changes.
```

`corpus/README.md:343` replacement:

```markdown
| FR12 | Event-driven pressure and CPU/IRQ PSI | `SOURCES.md:7-8,16`; `lessons/2026-10-15-free-lunch-measurements-counter-baselines.md:57-73` | A PSI trigger watcher is resident, not a one-shot census probe; system CPU `full=0` is not evidence of no stall. Round 24 advances only the one-shot system read of `/proc/pressure/{cpu,memory,io,irq}` (`tools/mori-pressure.py`, admission pending) to Core; the resident trigger watcher, cgroup-scoped CPU/IO/IRQ pressure and the two-sample `--interval` stall rate stay frontier. |
```

---

## 5. Boundaries and claims this draft does **not** make

- It does not claim the C2 capability is admitted; it says "admission pending".
- It does not claim any frontier row is closed, and it does not rewrite `FR12`'s row or
  the `Owns` header.
- It does not claim a census surface, finding id, DRIFT verdict, baseline re-pin or
  threshold calibration; FR8 stays open.
- It does not claim host cause, fleet attribution or OS diagnosis: `unsupported` carries
  no inferred cause (boot and kernel configuration belong to tsukuroi), and a
  system-wide reading is host evidence only.
- It does not claim a stall rate: `--interval` is outside the one-shot Core statement and
  stays with FR6/FR12.
- It does not claim the tool observes cgroup-scoped CPU/IO/IRQ pressure, nor a resident
  trigger watcher, nor a `cgroup.pressure=0` detection.
- It does not claim the sibling scan outcome: `ConnectSiblingPsi.md` reports no sibling
  contests mori's C2 and that tsukuroi's census also reads system
  `/proc/pressure/memory` (`tsukuroi-census.sh:376`, `:1100-1115`) — shared evidence, not
  shared ownership. I read those two tsukuroi lines myself and confirm them: `:376` sets
  `PRESSURE_FILE=${TSUKUROI_PRESSURE_FILE:-/proc/pressure/memory}` and `:1100-1115` is
  the C6 arm that parses `some`/`full` `avg300` and `full total`, labelling an
  unreadable file `C6-psi` (unknown). The rest of that seat's report I treat as relayed.

---

## 6. Out of scope for this seat (not done, deliberately)

- No edit to `PROVINCE.md`, `corpus/README.md`, `SKILL.md`, `SCORECARD.md`,
  `corpus/SOURCES.md`, `corpus/knowledge/` or `corpus/lessons/`. The SCORECARD capability
  row, the `SKILL.md` registry row and decision table (`DraftSkillTable.md`), the
  knowledge entry (`DraftKnowledgeEntry`) and the `SOURCES.md` rows (the seven source
  seats) are other owners' surfaces.
- No `git add/commit/stash/checkout/reset/pull/push` and no mutating `jj` command in the
  lane repo; only read-only `git log`, `git cat-file`, `git ls-tree`, `git status`,
  `git show`.
- No write to `/proc`, `/sys` or any cgroup file; no PSI trigger registration; no
  service, package or configuration change; nothing restarted.
- No sandbox clone was needed: this seat produced no code and ran no git-writing check.

---

## 7. Tooling

No install, upgrade or configuration change was performed. The task needed only
pre-installed tools: `python3` (3.14.x, standard library only), `curl` 8.23.0 (upstream
v7.2 reads), `git`, `grep`, `sed`, `awk`. Under the pacman guard, no pacman transaction
was attempted and no host service was restarted; `sudo` was not used.

---

## 8. What the L1 should check on integration

1. That the appended `PROVINCE.md` section lands after line 232 and the appended
   `corpus/README.md` sections after line 443, so `PROVINCE.md:3-16`, `:6-16`, `:12-16`,
   `:55` and `corpus/README.md:343` keep resolving.
2. That `knowledge/system-pressure-r24.md` exists in the same commit as the README row
   that names it (QUALITY 9), or that the row names the tool path instead.
3. That the `PROVINCE.md:6-10` `Owns` sentence is left untouched, matching the appended
   "Owns-scope extension" bullet.
4. That "admission pending" is either kept or deliberately replaced with the admitted
   wording — not left half-way.
5. That the after-value command is re-run at the landed tip:
   `python3 -I tools/mori-pressure.py --selftest` → `MORI_PRESSURE_SELFTEST: PASS 12/12`,
   exit 0.

---

## 9. Artifact paths

- This report (the only file created inside the lane repo by this seat):
  `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-24/w1/DraftProvinceFrontier.md`
- Read, not modified: `/home/vgpnk/Projects/shokunin/mori-shokunin/PROVINCE.md`,
  `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/README.md`,
  `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-24/contract.md`,
  `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-pressure.py`,
  `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/fixtures/mori-pressure/cases.json`
- Upstream bytes read outside the lane repo: Linux v7.2 `Documentation/accounting/psi.rst`,
  `kernel/sched/psi.c`, `Documentation/admin-guide/cgroup-v2.rst`,
  `Documentation/admin-guide/kernel-parameters.txt`, `init/Kconfig` (fetched with `curl`;
  not retained as a file).
