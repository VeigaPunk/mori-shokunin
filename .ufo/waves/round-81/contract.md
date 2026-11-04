# mori round 81 — frozen contract (L1 MoriR81)

Round 81, attempt 1. Entering revision `44bc941a0e3e9676fa33a882b43d6e9793cbf74d`
(branch `master`). This file is written **before any wave data** and is not rewritten;
corrections land as appended sections in `corpus/lessons/round-81.md` and the round
report, never as edits here.

Two claims, two axes, causally separable. Each counter is revision-agnostic: it exports
the revision under test and grades **that revision's** bytes and counters, so the same
command produces both the before and the after reading. This discharges the r80
review's HIGH-2 class ("the tip run does not re-derive the red conjunct") for this
round: the do-nothing control below is the same command at the entering revision.

Do-nothing controls, measured and committed before the wave
(`.ufo/waves/round-81/evidence/controls-r81.txt`):

```text
$ python3 -I .ufo/waves/round-81/count-c1.py 44bc941a0e3e9676fa33a882b43d6e9793cbf74d
C1=unmet wrong=7 fixtures=7 real_c1=met real_c3=met rev=44bc941a0e3e     rc=1
$ python3 -I .ufo/waves/round-81/count-c2.py 44bc941a0e3e9676fa33a882b43d6e9793cbf74d --pins .ufo/waves/round-81/record-pins.json
C2=unmet pending=3 pinned=1 tool=absent agree=0 rev=44bc941a0e3e         rc=1
```

A do-nothing round cannot reach either target: both counters are red at the entering
bytes with no lane change. A stub counter that always prints `met` is wrong on 4 of the
7 C1 fixtures and one that always prints `unmet` is wrong on the other 3 (the C1
counter's own discrimination selftest asserts both; `C1_COUNTER_SELFTEST pass=7 fail=0`).

## C1 — operability (7): the r80 counters' routed exposures are closed

**Claim.** The seven defeated fixtures the r80 wave's counter reviewer filed
(`.ufo/waves/round-80/w1/Mo80R01Counter.md`: MEDIUM-6, MEDIUM-7, MEDIUM-8, LOW-10,
LOW-11, LOW-12 — seven fixture shapes) are graded to their declared verdicts at the
landed revision by `.ufo/waves/round-80/count-c1.py` and `count-c3.py` themselves, and
both counters still grade the real lane bytes `met`; at the entering revision the same
seven fixtures defeat the counters on all seven (`wrong=7`).

**P-C1 (frozen sentence, implemented by `.ufo/waves/round-81/count-c1.py`, printed by
its receipt).** At revision R,
`python3 -I .ufo/waves/round-81/count-c1.py R` prints
`C1=met wrong=0 fixtures=7 real_c1=met real_c3=met rev=<sha12>` and exits 0; at the
entering revision `44bc941a` the same command prints `C1=unmet wrong=7` and exits 1.

Fixture set and expected verdict at R (frozen; each fixture is a synthetic git repo
built under `--scratch`, graded by the r80 counter at R through its own CLI):

| fixture | shape | expected at R | r80 defect |
|---|---|---|---|
| A2 `summary_contradicts_mismatch_line` | sweep prints a `CLAIM_SWEEP_MISMATCH tally` line then an all-zero summary, rc 0 | unmet | MEDIUM-7 |
| A3 `two_contradicting_summaries` | sweep prints `mismatches=0` then `mismatches=1`, rc 0 | unmet | MEDIUM-7 |
| A4 `second_carrier_row_stale` | two capability rows naming `tools/mori-control-receipt.py`, 19 then 18; live 19 | unmet | MEDIUM-8 |
| A5 `repo_path_with_space` | conformant fixture under a parent path containing a space | met | LOW-10 |
| B1 `subdir_path_counts_as_naming` | PROVINCE names only `` `corpus/tools/mori-census.sh` ``; present = that tool | unmet | MEDIUM-6 |
| B2 `own_lane_prefix_excluded` | PROVINCE names only `` `mori-shokunin/tools/mori-census.sh` ``; present = that tool | met | LOW-11 |
| B6 `directory_named_as_tool` | `tools/pkg.py` exists only as a directory holding a file | met | LOW-12 |

**Kill rule / target.** `C1=met` requires `wrong=0` **and** the two real arms `met`.
`setup` (rc 2) never satisfies a `met` expectation. The graded counter bytes are the
r80 files themselves: the fixes are implementation fixes inside
`.ufo/waves/round-80/count-c1.py` and `count-c3.py`; the r80 frozen predicates in
`.ufo/waves/round-80/contract.md` stay byte-unchanged, and the r80 graded values must
re-derive unchanged at `44bc941a` (`real_c1=met real_c3=met`).

Named limits (before data): the fixtures grade the six routed shapes only; the counters'
other arms are covered by their own `--selftest`; B6's expected `met` adopts "a named
path that exists at R as a directory is not an instrument" as the reading of the r80
sentence — recorded, not silent.

## C2 — calibration (5, the lowest non-retired axis): the record states its own results

**Claim.** The lane lands `tools/mori-record-sweep.py`, a read-only gate that grades the
record carriers' *claims* (unresolved `PENDING` after-cells in SCORECARD round tables and
numeric claim tokens that disagree with their own pinned command), and discharges the r80
closure's D80-1 (three `PENDING` after-cells), D80-2 (`pointers=232` vs the landed 233,
and the "integration re-run pending" wording) and D80-4 (measured-revision precision) as
append-only corrections; the r80 record's after-cells then carry measured values.

**P-C2 (frozen sentence, implemented by `.ufo/waves/round-81/count-c2.py`, printed by
its receipt).** At revision R,
`python3 -I .ufo/waves/round-81/count-c2.py R` prints
`C2=met pending=0 pinned=0 tool=present agree=1 rev=<sha12>` and exits 0; at the entering
revision `44bc941a` (with the frozen pins file) it prints
`C2=unmet pending=3 pinned=1 tool=absent agree=0` and exits 1.

Arms, each re-derived from committed bytes of R:

- `pending` — every cell whose trimmed value is exactly `PENDING` inside a
  `## Round ...` section of `SCORECARD.md` (a round section's claim table is the
  record's own result column; `PENDING` there is an unpaid debt). Entering: 3.
- `pinned` — every binding in `.ufo/waves/round-81/record-pins.json` states a value the
  row carries (`<key>=<int>`) that its own pinned read-only command prints at R. Entering:
  1 (the capability row states `pointers=232`; the pinned sweep prints `pointers=233`).
- `tool` — `tools/mori-record-sweep.py` exists at R, and its `RECORD_SWEEP pending=P
  pinned=Q` agrees with this counter's independent reading (`agree=1`). Entering: absent.

**Kill rule / target.** `C2=met` requires all three arms; a conflict between two readings
of the same key is a mismatch, never a pass (`live_value` returns `None` on conflicting
match sets). Correcting a claim by deleting the row is not a pass: the `pinned` arm needs
the row to state the live value, and the capability row is retained with the corrected
count and a named supersession.

Named limit (before data): the counter grades the lane's own record carriers
(`SCORECARD.md`, and any carrier a binding names); it does not grade fleet report prose
(D80-4's correction is a lesson/report act, deliberate, not a counter arm), and `pending`
is a cell-value test, not a reading of intent.

## `tools/mori-record-sweep.py` — frozen interface

The C2 capability, built in-wave to this spec; Python 3 standard library only, `python -I`
safe, one file, read-only (stdout only, no sockets, no temp files, no child processes
except the pinned read-only commands, whose cwd is `--root`).

```text
usage: mori-record-sweep.py --root DIR [--pins FILE] [--carriers A[,B]] | --selftest | --help
pins:  {"schema": "mori-record-pins-v1", "bindings": [{"carrier","row_contains","key","command"}]}
       default pins path: ROOT/.ufo/waves/round-81/record-pins.json
arms:  pending  a cell exactly PENDING inside a `## Round ...` section's table row
       pinned   a binding row's stated <key>=<int> differs from the pinned command's
                stdout `<key>=<int>` (conflicting or absent values are mismatches)
out:   per mismatch: `RECORD_SWEEP_MISMATCH <pending|pinned> <carrier>:<line> <detail>`
       then      `RECORD_SWEEP pending=N pinned=M carriers=C bindings=B`
exit:  0 clean · 1 mismatches · 2 setup (missing root, malformed pins, unreadable carrier)
```

The tool and `count-c2.py` must agree on both fields at the landed revision (`agree=1`);
the tool is the capability, the counter is the frozen grade — neither may grade itself
alone.

## No-harm conditions

- `.ufo/waves/round-80/count-c1.py` and `count-c3.py` still print `met` on the real lane
  bytes at `44bc941a` (the `real_c1`/`real_c3` arms above).
- The r80 frozen contract bytes are unchanged; the r80 graded values re-derive unchanged.
- The standing instrument battery stays green; `sources-census.sh validate` exits 0 at
  round end; `PROVINCE.md`'s instrument inventory names the new tool (the r80 C3
  predicate would otherwise read `missing=1` at the tip).
- Detection and report only: no lane, OS, unit, credential or orchestration state changed.
