# RevSkillSweep — round-45 digests/tallies in SKILL.md outside target cells

Seat: `L1Mori46.RevSkillSweep` (leaf member, no subagents). Round 46 wave 1.

Scope: sweep the lane `SKILL.md` (working-tree bytes; sha256
`ec31c0f8422b6c5bf0e03586bc874a4ea85e30ed368c35b89778cc465ea36afa`) for **stale
round-45 digests/tallies outside the four predicate target cells**. Target cells are
the rows `count-repins.py` (`ROWS`) pins:
`r44 gate registry (C2)` (line 184), `r45 ledger counter (C1)` (line 190),
`r45 gate conformance (C2)` (line 191), `r44 gate registry (C2) — write scope
superseded` (line 194). Everything else in SKILL.md is in sweep scope.

Method: (1) case-insensitive inventory of every round-45/round-46 mention;
(2) for each non-target round-45 self-test digest, re-run the tool's own
`--selftest` and compare its tally line against the SKILL cell; (3) verify pinned
hashes/line counts against current file bytes and cited evidence files.
No git/jj writes; no tool installs were made (none were needed).

## Findings

### F1 (low — stale citation, the only stale round-45 content found)
The round-45 registry-refresh block (SKILL.md lines 203–204) cites the two routed
rows with wrong line anchors:

- `routed round-23 items (r24, C1)` cited at line **646** — the row is actually at
  line **665** (verified: line 646 is a "Reading system pressure" prose-table row;
  line 665 is the only `ROUTED_CHECK_SELFTEST` row).
- `routed round-24 items (r25, C1)` cited at line **721** — the row is actually at
  line **740** (verified: line 721 is an earlyoom error-pattern row; line 740 is
  the only `ROUTED_R24_SELFTEST` row).

Both cited tallies themselves are current (F2 table, rows 7–8); only the anchors
are stale (off by +19). The block's other two self-test anchors (`silence oracle`
166, `r19 finite regressions` 182) are correct.

### F2 (verified current — no other stale round-45 digest/tally)
Every other non-target round-45 digest/tally site re-ran today and matches its
SKILL cell exactly:

| SKILL line | row / self-test cell | claim | live selftest today |
|---|---|---|---|
| 166 | silence oracle | `MORI_SILENCE_CASES_SELFTEST pass=24 fail=0` | `pass=24 fail=0` rc 0 |
| 182 | r19 finite regressions | `R19_SELFTEST pass=26 fail=0` | `pass=26 fail=0` rc 0 (requires lane TMPDIR, see limits) |
| 187 | disk write rate (r34) | `MORI_DISK_RATE_SELFTEST pass=14 fail=0` rc 0 | `pass=14 fail=0` rc 0 |
| 188 | wave settlement (r20) | `MORI_WAVE_SETTLEMENT_SELFTEST: PASS (23 cases, 23 passed, 0 failed)` rc 0 | identical, rc 0 |
| 189 | r41 calibration | `MORI_R41_CALIBRATION_SELFTEST pass=10 fail=0` rc 0 | `pass=10 fail=0` rc 0 |
| 192 | r45 corpus coverage (C3) — **not a predicate target row** | `C3_SELFTEST pass=19 fail=0` rc 0, sha `37fd7c24ff52…`; mutant sha `69bf9b6eb29b…` | `pass=19 fail=0` rc 0; file sha `37fd7c24ff52d6aa…`, mutant sha `69bf9b6eb29b7818…` (prefix match) |
| 665 | routed round-23 items (r24, C1) | `ROUTED_CHECK_SELFTEST pass=20 fail=0` | `pass=20 fail=0` rc 0 |
| 740 | routed round-24 items (r25, C1) | `ROUTED_R24_SELFTEST pass=26 fail=0` | `pass=26 fail=0` rc 0 |

Also verified current (not stale):

- Pinned hashes match current bytes: `tools/mori-gate-registry.py` =
  `8b82ac999091ebe65e765ed69f759910a57049ff0e7c5c4aa56df9c7168f5832`, 743 lines;
  `round-45/count-c1.py` = `5f2deea0b35c5e1346229d265aa0c07bf7f365bf6c5acda87648045bce658d23`;
  `round-45/count-c2.py` = `153423c48ca90466e85b02707828f5c6b2cf39c87c68ee67e3f9abee956baf93`;
  mutant `count-c2.py` = `9850b3fcc8885456c3e71458b34184d716d54880a91ae5b29c7d003f26708703`. (Rows 184/190/191/194 are predicate targets; they are green under the predicate — see control note.)
- The superseded write-scope rows (193/195/196) cite `.ufo/waves/round-45/evidence/write-scope.txt:82/96/110`; those lines exist and each carries `verdict=TRUE` (and the selftest tallies there match the r44 rows).
- Round-45 artifacts cited in rows 187/189/190/191/192 all exist: `round-45/w1/ScribeRegistryRows.md`, `round-45/figures.tsv`, `round-45/fixtures/mutants/count-c{1,2,3}.py`, `round-45/fixtures/write-scope.json`.

## Control note (reproduced)
`count-repins.py` against the control snapshot (`.ufo/waves/round-46/control-skill.md`,
sha `ed71e8f6e68c059deefb1f9bcfec42f12f2ae3bdb21aff6d5bc9bca2561cb9ad`):
`MORI_R45_REPINS mismatches=4 rows=4` rc 1 (red, as required). Against the current
`SKILL.md`: `mismatches=0 rows=4` rc 0 (green).

## Limits
- Ground truth is the working-tree tool bytes (selftests run against `tools/` and
  `.ufo/waves/round-45/` as they exist now), not a committed revision; no commit
  hash was verified.
- `mori-round19-regressions.py --selftest` refuses any TMPDIR outside the lane root
  (`explicit-lane-tmpdir-invalid`); it was run with `TMPDIR=$PWD/.scratch` (the
  documented lane scratch), which already existed and is a scratch area, not a
  production file.
- The wave-settlement tally's decomposition (14 frozen + 9 in-script = 23) is
  consistent with the printed PASS line; the 9-case list was not re-enumerated.
- The "round-46 finding" sentence inside row 187 (`disk write rate`) is an
  annotation, not a digest/tally; not in sweep scope.
