# ScoutCorpusFrontier — round-40 w1

Item: read `corpus/README.md` `## Frontier`; confirm the round-40 admission
(S229 row + `corpus/knowledge/conform-scope-r40.md`) leaves the frontier
statement accurate; flag any README claim the round contradicts.

Seat: scout (read-only). HEAD at time of checks: `ede486b7a09afbacfb380d5871c46a8051a6dc2e`
(descendant of scored tip `265a955cc`). No production bytes written by this seat.

## Verdict

**The `## Frontier` statement (README:335-352, FR1–FR15 incl. the FR15 note and
the FR5/FR6/FR12 narrowing notes) remains accurate under the round-40
admission. No Frontier row is closed, narrowed, or contradicted.**

Round 40 admits S229 (Python execution model — naming and binding,
`SOURCES.md:235`) plus `corpus/knowledge/conform-scope-r40.md`, used by claim
C1 (P-C10 conformance v3). This is instrument-semantics ground — why the
timeout constant-fold must be scope-aware — which no FR row covers:

- FR1/FR10 (OOM attribution, userspace killers), FR11 (journal cursors),
  FR12/FR6 (pressure, disk write-rate), FR13 (eBPF), FR14 (telemetry),
  FR15 (job-capacity runway), FR2–FR5, FR7–FR9: none overlaps Python
  name-resolution or the conformance checker's fold. The S229 row's
  `used-by` (`corpus/knowledge/conform-scope-r40.md`) resolves; the file
  exists and quotes the S229 teaching verbatim at :15-18.
- FR9 (durable fixture evidence) is *consistent* with the round's shape:
  committed builders `fixtures/make-survivor-fixtures.py`,
  `fixtures/run-c11-dags.py`, extracted before-bytes under
  `fixtures/extracted/` (sha-verified below), and `evidence/freeze-r40.txt`.
- No FR-cited line reference drifted: S229 appends at `SOURCES.md:235`,
  the last registry row; the rows FR rows cite by line stay put —
  `SOURCES.md:7-8` = S001/S002 (FR12), `:11-12,23-26` = S005/S006,
  S017–S020 (FR13), `:16` = S010 (FR12), `:20-21` = S014/S015 (FR11),
  `:28-32` = S022–S026 (FR14). Verified by direct read.
- `SOURCES.md` `## Paths` section needs no S229 entry (Paths maps
  topical trails; an execution-model row has no trail). Confirmed S229
  appears exactly once in the file (grep count 1).

## Flagged README claims (staleness, not falsehood)

The README's round rows are historical records, so these are superseded-at-live-path
citations, not contradictions — flagged because the Entry column names the live path:

1. **README:606 (round-39 "Ancestry-based timed supersede" row)** cites
   `python3 tools/mori-sources-appendonly.py --selftest` → `pass=12 fail=0`.
   The live gate is now v3: observed `MORI_SOURCES_APPENDONLY_SELFTEST
   pass=15 fail=0`. Same command, different output.
2. **README:606** claims the v2 gate prints "byte-identical lane-history lines
   at the tip and `e37dcc6`." True of v2 (extracted bytes verified: `git show
   bb1f2457:tools/mori-sources-appendonly.py` sha `62cd4132…` ==
   `fixtures/extracted/gate-v2-bb1f2457.py`), but at the live v3 bytes the tip
   line changed: 35 as-of ids incl. S226 vs v2's 18, and `e37dcc6` still
   prints `stale_supersede=[S069]` (unchanged verdict).
3. **Absence, not contradiction:** README carries no round-40 coverage row and
   no Coverage-map row for `knowledge/conform-scope-r40.md` — pre-admission
   state consistent with prior rounds (the map also lacks a
   `gate-ancestry-r39` row; coverage sections, not the map, carry r37–r39
   entries).

## Commands run and outputs

- `git rev-parse HEAD` → `ede486b7a09afbacfb380d5871c46a8051a6dc2e`
- `ls corpus/evidence/sources-r40/` → `S229.src` (committed copy present;
  sha256 `a7774d77ad6aa9da64484be0f7954b78d5daf497fc73219b1935dbb67304ca54`)
- `read corpus/README.md:335-353` — all 15 FR rows + narrowing notes; none
  mentions conform/scope/Python name binding.
- `python3 tools/mori-sources-appendonly.py --selftest` →
  `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0` (v3 at scored-tip tree)
- `python3 tools/mori-sources-appendonly.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b`
  → `supersede_timing superseded_as_of=[35 ids incl. S226]
  stale_supersede=[]`; ids:
  S041,S044,S051,S062,S064,S067,S069,S070,S071,S083,S084,S090,S093,S096,S097,
  S101,S124,S127,S128,S129,S131,S140,S179,S180,S181,S182,S183,S184,S185,S186,
  S188,S189,S190,S193,S226 — **count 35**, matching committed receipt
  `.ufo/waves/round-40/evidence/c11-after-lane.txt` byte-for-byte.
- `python3 tools/mori-sources-appendonly.py e37dcc6` → same list minus
  S069/S226, `stale_supersede=[S069]` — README:598 ("at `e37dcc6` S069 is
  stale") still holds at v3.
- `git show bb1f2457:tools/mori-sources-appendonly.py | sha256sum` →
  `62cd4132dbe141538371f79723c3caff66670fab9076494cd9cf65efccfc01e7`,
  identical to `fixtures/extracted/gate-v2-bb1f2457.py` (before-bytes
  integrity confirmed).
- `sha256sum tools/mori-sources-appendonly.py` →
  `bde5a9a34c7eb3bcbee39d669b8d187caeb51807ad1bdcd85a05c1bcd06777ec` (v3,
  differs from v2 as expected).
- `read corpus/knowledge/conform-scope-r40.md` — entry present, cites S229,
  `verified-at: 2026-10-24`, `recheck: on-release`, receipts pointer
  `evidence/c10-*.txt`; the S229 located quote is carried verbatim.
- `grep -n 'S229' corpus/SOURCES.md` → exactly one hit at `:235`, appended
  after S228 (`:234`); append-only placement holds.

## Arithmetic anomaly (context, outside README scope but observed)

Both the contract's P-C11 text ("S226 joins superseded_as_of (19 ids…") and
the wave prompt's "34 as-of ids" mis-predict the measured line: the observed
and committed-receipt count is **35** (v2's 18 + 16 additional superseded ids
the widened eligible set reaches + S226). Sibling seat ScrScorecardDraft was
dispatched to mark the same mis-prediction. The README itself makes no count
claim, so this does not flag a README row — recorded here as corroborating
measurement.

## Tooling

None installed (pacman paused per standing guard; no tool needed beyond
python3/git/sha256sum).
