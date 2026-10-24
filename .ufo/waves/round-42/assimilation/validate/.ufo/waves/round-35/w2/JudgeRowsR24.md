measured 2026-10-23T09:12:48Z

# JudgeRowsR24 — mori round-24 register rows at cedb0ec4

Scope: rows `rounds[443].capabilities_added[0]` and `rounds[443].capabilities_added[1]` in the final `## Capabilities`
section of SCORECARD.md at lane `cedb0ec4f3a4f672804deac388b7191258f01fcd` (section starts line 1941; the two rows are
the 11th and 12th table rows). Decision rule (per `.ufo/waves/round-35/evidence/c1-controls.txt`): (a) non-empty,
closure-faithful capability and what cells; (b) evidence cells holding only backticked paths. Record compared against:
fleet `MANIFEST.json` `rounds[443]` at fleet `37b51a24`, fleet report `.ufo/reports/round-24/mori.md` at `37b51a24`,
lane spot-check `corpus/lessons/round-24-verifier-spotcheck.md` at lane `28b79d3d1b76824f0c825aabe6cb6c5dc49961bf`.

## Row `rounds[443].capabilities_added[0]` — one-shot system pressure read

Cell text: "Reads /proc/pressure cpu, memory, io and irq once per resource; unavailable is never zero, system cpu full
is flagged undefined and irq some is null; frozen selftest PASS 12/12, six wave-2 survivors disclosed."
Evidence cell: `` `tools/mori-pressure.py` `` — one backticked path, nothing else. First-working round cell: 24.

Fact-by-fact against `rounds[443].capabilities_added[0]`:

- "Reads /proc/pressure cpu, memory, io and irq once per resource" ← record: "one-shot system pressure read
  (tools/mori-pressure.py): /proc/pressure/{cpu,memory,io,irq} per-resource states". Same resource set; "once per
  resource" restates "one-shot"/"per-resource", no added claim. Tool docstring at `4f05dd5a:tools/mori-pressure.py:12-13`
  confirms `--root` default `/proc/pressure`, files `cpu, memory, io, irq`.
- "unavailable is never zero" ← record: "unavailable never zero" (verbatim bound).
- "system cpu full is flagged undefined" ← record: "system cpu full flagged undefined". Tool: `FULL_UNDEFINED = {"cpu": True}`
  (`tools/mori-pressure.py:85`), `full_system_undefined` payload flag (`:215`).
- "irq some is null" ← record: "irq some null". Tool: irq requires `full` only, missing `some` expected `some: null`
  (`tools/mori-pressure.py:17-18, 75, 81`).
- "frozen selftest PASS 12/12" ← record: "frozen selftest PASS 12/12 over cases landed before the tool (f6a29702 before
  6ee62487)". Cell drops the commit citations but keeps the count and the frozen-before-tool bound ("frozen selftest").
  Spot-check agrees: 12 cases P01–P12 frozen at `f6a29702` before the tool at `6ee62487`, blob `39cc96ab` unchanged to tip.
- "six wave-2 survivors disclosed" ← record: "6 wave-2 survivors disclosed". Spot-check names them (threshold edge,
  matcher ignoring `findings_include`, three grammar shapes, PARTIAL outranking HIGH) and confirms the responses are
  disclosed as not counted.

No cell fact exceeds the record. Capability name is the record's name verbatim. Non-empty cells; (b) holds.

VERDICT: rounds[443].capabilities_added[0] supported

Pointer relevance (c): at `4f05dd5a`, `tools/mori-pressure.py` is exactly this capability — a read-only PSI survey of
`/proc/pressure/{cpu,memory,io,irq}` with unavailable-never-zero states, `full_system_undefined` on system cpu, irq
`some: null`, and `--selftest` over `tools/fixtures/mori-pressure/cases.json` printing `MORI_PRESSURE_SELFTEST: PASS n/N`
(docstring lines 1–52, code lines 70–85, 122, 175–215). Not another round-24 artifact.

VERDICT: rounds[443].capabilities_added[0] pointer-relevance holds

## Row `rounds[443].capabilities_added[1]` — round-23 routed-item check

Cell text: "Checks the R1-R3 regression pins and R4 dispatch-before-call ordering over lane-written times; held 3 to 4;
round-23 wave-1 timing mismatches 8, round-24 0 of 2."
Evidence cell: `` `tools/mori-routed-check.py` `` — one backticked path, nothing else. First-working round cell: 24.

Fact-by-fact against `rounds[443].capabilities_added[1]`:

- "Checks the R1-R3 regression pins and R4 dispatch-before-call ordering over lane-written times" ← record:
  "R1-R3 regression pins plus R4 dispatch-before-call ordering over lane-written times" — near-verbatim.
- "held 3 to 4" ← record: "held 3 -> 4". Spot-check agrees: `evidence/c1-before-round23.json` held 3,
  `evidence/c1-after-13208d2.json` held 4; report's before/after commands give held 3 of 4 then held 4 of items 4.
- "round-23 wave-1 timing mismatches 8" ← record: "round-23 wave-1 timing mismatches 8". Spot-check: 8 of 9
  `wave1-ledger.json` rows with `at` earlier than dispatch commit `22772c10`.
- "round-24 0 of 2" ← record: "round-24 0 of 2". Spot-check: 2 rows, 0 mismatches; each `at` between payload and
  ledger commit.

No cell fact exceeds the record. Capability name is the record's name verbatim. Non-empty cells; (b) holds.

VERDICT: rounds[443].capabilities_added[1] supported

Pointer relevance (c): at `4f05dd5a`, `tools/mori-routed-check.py` is exactly this capability — it re-derives the
round-23 routed items R1..R4 from git objects (docstring lines 1–25): R1 quota-absence/tree pin (`:72-85`), R2
retention pins plus privacy-clearance-line scan over R2_SCAN_SCOPE (`:49-64, 90-98`), R3 capture-limitation pins
(`:98-103`), R4 dispatch-before-call via the committed `mori-dispatch-ledger.py` (`:10-12`). Not the pressure tool.

VERDICT: rounds[443].capabilities_added[1] pointer-relevance holds

## Residual risk / verification gaps

- Both rows judged against the MANIFEST string and the closure record (fleet report + lane spot-check); the register's
  own preamble states rows record what the closure admitted (SCORECARD.md:1941-1950). No cell restates the record's
  numeric bounds loosely — all numbers match.
- The row-0 cell elides the record's commit citations `(f6a29702 before 6ee62487)`; judged faithful-and-bounded since
  "frozen selftest" preserves the bound's content and nothing is overstated.
- Pointer relevance was established by static read of the tool sources at `4f05dd5a`, not by execution [INFERENCE-free
  for presence/structure; run behavior not re-executed in this lane].

No installs performed.
