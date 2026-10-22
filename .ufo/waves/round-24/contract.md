# mori round 24 (attempt 2) — claim contract

L1: MoriR24 (fresh in-session lane subagent; attempt 1, a stale 2026-10-21 author, was
failed at T0 and is not resumed). Entering lane tip `c725aa37aa3c9ec4f34e3c2abc8ca1b616c7c130`.
The prior private trees under `/fast/scratch/hyaku/mori-r24-author*` (an unlanded 49-case
pre-registration for a receipt-audit tool) are not continued; nothing from them is reused.

Two claims. Each declares one after-value that one command over committed bytes re-derives.
A miss is an honest stop; the targets below are never narrowed after landing.

## C1 — repair the round-23 routed defects (axis: calibration, lowest active score 5)

Source of the routed items: `corpus/lessons/round-23-verifier-spotcheck.md:60-66`.

New read-only check `tools/mori-routed-check.py --repo PATH --rev REV`
(base revision fixed to `c725aa37aa3c9ec4f34e3c2abc8ca1b616c7c130`, the tip carrying the
spot-check). It compares the lane's round-23 self-assessment with committed bytes at REV
and reports one row per routed item:

| Item | Routed text (abridged) | Predicate at REV (all git object reads, no working tree) |
|---|---|---|
| R1 | keep quota capability absent; never alter CaseEscapedSpace's expected row | `tools/mori-quota-surface.py` and `corpus/knowledge/quota-surface-r23.md` absent; tree OID of `.ufo/waves/round-23/frozen` equals base |
| R2 | preserve four unallowlisted hits, permission red, unknown dispositions, blocked baseline, `privacy_clearance=false` | blobs `.ufo/waves/round-23/evidence/retention-floor-final.json` and `retention-floor-final-comparison.json` equal base; no line added between base and REV matches `privacy_clearance\s*["']?\s*[=:]\s*["']?true` (case-insensitive) |
| R3 | preserve missing transient-source and overwritten-wrapper limitations | blobs `.ufo/waves/round-23/evidence/harness-receipt-overwrite.json` and `tmpfs-source-provenance-erratum.json` equal base; tree OID of `.ufo/waves/round-23/rejected` equals base |
| R4 | bind future dispatches before the call | at least one `.ufo/waves/round-24/*-attempts.json` exists; each verifies clean with `tools/mori-dispatch-ledger.py verify` at REV; for each row, the committer time of the commit that first added its `dispatch_path` is at or before the row's `at` |

Routed item 5 (configuration with tsukuroi/operator, residue with souji, reclamation
with the operator) is an adjacency boundary with no byte predicate; it stays in
`PROVINCE.md` Adjacent and is reported as a why-not, not counted.

Output: one JSON object on stdout, `schema: mori-routed-check-v1`, `items: 4`,
`held: N`, per-item `{id, held, reasons[]}`. Exit 0 when held == 4, 1 when any item
fails, 2 when the repo/rev/base cannot be read.

**Amendment A1 (08:22Z, before any C1 tool landed; finding from wave-1 seat ScoutRoutedBytes):**
the R2 added-line scan covers only the lane's self-assessment and knowledge surfaces —
`SCORECARD.md`, `PROVINCE.md`, `SKILL.md`, `LOG.md`, `README.md` and `corpus/**` — not
`.ufo/**` or `tools/**`, where wave reports and mutant descriptions quote the pattern
(quotation, not assertion). At base the regex has 9 quoted hits under `.ufo/waves/`; none
of them is an added line. The declared before and after values are unchanged.

- **Before:** the same tool run at `--rev c725aa37aa3c9ec4f34e3c2abc8ca1b616c7c130` (R4 has
  no round-24 ledger) — expected `held: 3`. No tool checked these items before this round.
- **After-value (one command):**
  `python3 -I tools/mori-routed-check.py --repo /home/vgpnk/Projects/shokunin/mori-shokunin --rev <landed tip>` prints `"held": 4` with `"items": 4`, exit 0.
- **Able to fail:** one sandbox mutant per item (R1 re-add a quota tool path; R2 add a
  line that sets the privacy-clearance key to true; R3 change one byte of the overwrite receipt; R4 a ledger
  row whose `at` precedes its dispatch commit) each turns that item red. Sandbox clones only.
- Each item becomes a QUALITY.md criterion line tagged `routed r23-R<n>` naming this check.

## C2 — system pressure capability for CPU, IO and IRQ (axis: coverage, score 6)

Frontier FR12 ("Event-driven pressure and CPU/IRQ PSI") — the census reads only the
user slice's `memory.pressure`; system `/proc/pressure/{cpu,io,irq,memory}` is unobserved.
This claim moves one-shot system PSI reading to Core. The resident trigger watcher and
cgroup-scoped CPU/IO/IRQ pressure stay Frontier.

New read-only tool `tools/mori-pressure.py`:

- `--root DIR` (default `/proc/pressure`): reads the files `cpu`, `memory`, `io`, `irq`.
- Line grammar: `^(some|full) avg10=D avg60=D avg300=D total=N$` with D a decimal and N a
  non-negative integer (microseconds). Duplicate kinds, missing required kinds or any
  other shape → resource state `malformed`.
- Required kinds: `cpu`, `memory`, `io` need `some` and `full`; `irq` needs `full` only, and
  its missing `some` is expected (`some: null`), never malformed.
- System `cpu` `full`: reported but labeled `full_system_undefined: true`; never used for a
  threshold and never read as evidence of no stall.
- Open/read errors: ENOENT → `absent`; EOPNOTSUPP → `unsupported` (PSI disabled);
  EACCES/EPERM → `unreadable`. All three are unavailable, never zero.
- Threshold: `--warn-avg10 X` (default 10.0, labeled local, not calibrated): finding
  `PRESSURE_HIGH` when avg10 ≥ X on `some` of cpu/io/memory or `full` of memory/io/irq.
- `--interval S` (0 < S ≤ 10): reads twice, reports `total_delta_us` and
  `stall_ratio = total_delta_us / (S * 1e6)` per kind; a decreasing total → resource
  state `counter_regressed`.
- Output: one JSON object, `schema: mori-pressure-v1`, `resources` keyed by name, each
  `{state, some, full, notes[]}`, plus `verdict` ∈ `PRESSURE_OK | PRESSURE_HIGH |
  PRESSURE_PARTIAL | PRESSURE_UNAVAILABLE` and `findings[]`. Exit 1 on `PRESSURE_HIGH`;
  exit 2 when every resource is unavailable or on usage error; else exit 0 (PARTIAL
  means at least one resource unavailable or malformed).
- `--selftest`: runs the frozen cases in `tools/fixtures/mori-pressure/cases.json`
  (12 cases P01–P12, written by a seat that does not see the implementation, landed
  before the tool) and prints `MORI_PRESSURE_SELFTEST: PASS n/12` or `FAIL`.
  Error injection (EOPNOTSUPP, EACCES) uses an in-process open hook, documented as such.

Case topics (frozen by number): P01 four normal low files → OK exit 0; P02 nonzero system
cpu full → flagged undefined, still OK; P03 irq with only `full` → ok, `some` null; P04 irq
absent → PARTIAL exit 0; P05 EOPNOTSUPP on all four → UNAVAILABLE exit 2; P06 memory some
avg10 25 → HIGH exit 1; P07 irq full avg10 15 → HIGH exit 1; P08 non-decimal avg10 in io →
io malformed, PARTIAL; P09 memory missing `full` → malformed; P10 EACCES on io → unreadable;
P11 interval with two snapshots → delta and ratio; P12 interval with a decreasing total →
counter_regressed.

- **Before:** `git cat-file -e c725aa37:tools/mori-pressure.py` exits 128; no mori tool reads
  system CPU, IO or IRQ pressure.
- **After-value (one command):**
  `python3 -I tools/mori-pressure.py --selftest` at the landed tip prints
  `MORI_PRESSURE_SELFTEST: PASS 12/12`, exit 0; plus one live host run retained as evidence
  and a SCORECARD capability row.
- **Sourced:** the knowledge entry `corpus/knowledge/system-pressure-r24.md` and the
  decision table in SKILL.md cite `SOURCES.md` rows opened this round (Linux v7.2 PSI
  documentation and `kernel/sched/psi.c`, cgroup-v2 pressure files, PSI Kconfig and boot
  parameter, proc_pressure(5)).

## Bounds

Detection and report only. No host writes, no PSI trigger registration, no cgroup writes,
no service or package changes. Other axes (operability 7, depth 5, freshness 5, adjacency 6)
are held and observed. No retirement, waiver, exploratory claim or promotion.
