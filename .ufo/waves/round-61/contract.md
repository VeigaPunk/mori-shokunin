# mori round 61 — frozen contract (freeze before any seat scores)

Pre-seat amendment 1 (2026-10-30, before dispatch, no seat has scored): C3's frozen
met token names fixed to `r60hole=ok r61repair=ok blobrefusal=ok expectpin=ok
livepins=ok` so every printed token is one measured boolean under the published
TOKEN_MAP (the r60 defect-2 shape, applied to this round's own counter).

Pre-seat amendment 2 (2026-10-30, before dispatch, no seat has scored): C3's r60
red-before pin is the r60 FREEZE bytes — `.ufo/waves/round-60/count-c3.py` at
`ac496c7c…`, sha256 `fabde06c…` (the 4d036fb0 blob was pre-amendment and is not the
frozen counter Reviewer13 audited). C2's selftest cites four synthetic copies so the
live ≥4-copies arm is exercised in selftest too.

L1 MoriR61, 2026-10-30. Entering revision `325f7e639916fcbc77fa2ec7475951a1b86bb1cb`
(round-60 verifier spot-check tip). Fresh-start round: the last three rejected closures
(rounds 58, 59, 60) were read first; the three claims below are declared only where a
do-nothing control cannot reach the after-state (addendum §9), and each control receipt
is committed in `.ufo/waves/round-61/evidence/` before any seat scores.

Scores entering: coverage 6, operability 7, depth 5, freshness 5, calibration 5,
adjacency 6. Lowest-scoring non-retired axes: depth/freshness/calibration (tied 5).
C1 targets calibration, C2 freshness, C3 operability — three distinct axes; the claims
are causally separable (each names files the others do not touch). No scalar score
change is claimed by the lane; the non-author closure rules.

Amendments to this contract or to any counter are barred once any seat has scored.
Frozen bytes from earlier rounds are never edited in place (r58 lesson); all repairs
ship as new round-61 files.

## Claims

### C1 — calibration: the lane gate registry carries every gate landed in rounds 52–60

- **Target (after):** for all 25 paths in `.ufo/waves/round-61/gate-manifest.json`
  (18 wave counters r52–r60, r60 `count-c3.py`, r57 `verify-c2-source.py`, and the five
  lane tools `mori-vote-bind.py`, `mori-driver-liveness.py`, `mori-register-check.py`,
  `mori-settlement-scan.py`, `mori-entry-claims-check.py`), the SKILL.md gate-registry
  tables hold exactly one non-superseded row whose entry cell names the path, with all
  eight cells non-empty, a self-test cell naming a `--selftest` command, and an owner
  cell; every entry path resolves at the measured revision (`git cat-file -e`).
- **Counting command:** `python3 .ufo/waves/round-61/count-c1.py <rev> [--repo DIR] [--scratch DIR] [--manifest PATH]`
- **Frozen met line:** `C1=met gates=25 registered=25 missing=0 thin=0 dup=0 unres=0 noselftest=0 noowner=0 rev=<rev>` (exit 0).
- **Before (control):** at the entering revision the registry tables end at r51
  (r60 closure routed defect 1): `C1=unmet gates=25 registered=0 missing=25 …` (exit 1).
  A do-nothing control cannot write the rows.
- **Kill rule:** the claim fails if any manifest path has no conformant row, two
  non-superseded rows, an unresolved path, or a row with an empty owner/self-test cell
  at the measured revision. Row registration for round-61's own instruments is NOT
  claimed (next round's duty, per the observed one-round lag).
- Note: r58's SHONEN defect is re-filed this round (report contract), unrelated to C1.

### C2 — freshness: the PSI recheck trigger fires and the ledger lands

`corpus/knowledge/system-pressure-r24.md` pins its `recheck:` to "on a kernel release,
re-open S090 and S091"; Linux v7.3 released before round 53 and the entry's prose
anchors were never rechecked (r53 named the gap; r55 covered four other entries only).
The lane now opens the same six files at tag v7.3 (pinned copies
`corpus/evidence/sources-r61/{psi.rst,psi.c,psi_types.h,cgroup-v2.rst,Kconfig,kernel-parameters.txt}`,
sha256s frozen in `count-c2.py`), and lands a recheck ledger.

- **Target (after):** `corpus/knowledge/psi-v73-recheck-r61.md` carries the provenance
  trio and exactly one ledger row per v7.2 line pointer the counter enumerates from
  `system-pressure-r24.md` (floor 40; expected ≈47), each row
  `| <file>:<start> | <same|moved|changed> | <location> | `<quote>` |` whose quote is a
  byte substring of the pinned v7.3 copy at the stated location (same: the enumerated
  range; moved/changed: the row's stated location, anywhere in the copy for changed),
  with every quote ≤25 words, ≥8 distinct bytes, pairwise distinct; the rows cite ≥4 of
  the six pinned copies; each cited copy has a SOURCES.md row opened this round,
  `status=mined`, `used-by` naming the ledger entry.
- **Counting command:** `python3 .ufo/waves/round-61/count-c2.py <rev> [--repo DIR] [--scratch DIR]`
- **Frozen met predicate:** exit 0 with `C2=met pointers=N rows=N quotes_ok=N spans_ok=N sources>=4 rows_src=ok provenance=ok failed=none` (N ≥ 40, pointers == rows).
- **Before (control):** at the entering revision the ledger entry and the S-rows do not
  exist: `C2=unmet … failed=entry_absent,rows_missing,…` (exit 1). A do-nothing control
  cannot open the sources or write the ledger.
- **Kill rule:** anchor-set mismatch (missing or orphan rows), a quote not
  byte-located where its row states, a duplicated span, a sub-8-distinct-byte quote,
  fewer than 4 cited copies, or a cited row not `mined`/`used-by`-bound at the measured
  revision. No vote arm is frozen (the r55 vote-binding failure is deliberately not
  repeated; content binds on committed bytes the closure can re-derive with grep).

### C3 — operability: the counter execution boundary repaired and demonstrated

Round 60's own wave decertified `count-c3.py`: `met` omits any count-c1 pin conjunct
(:255), the three gate tokens print from literals no append site emits (Reviewer13:
`containment=ok` beside `failed=g2_escape_written`), and `count-c1` executes
repo-supplied blobs with no sha comparison (Mo60Sentinel41: four blobs, 21 child
invocations). The repair ships as the new `.ufo/waves/round-61/count-c3.py` (r60 bytes
at the r60 freeze `ac496c7c` stay frozen, sha256 `fabde06c9d0a94a8487e5de45be3e413f6084816fb0507a71fd335bad5153514`).

- **Target (after):** the r61 counter, at the measured revision, demonstrates on
  committed logic and fixtures that (a) static arms parse the pinned r60 bytes and
  confirm the hole (no `c1` conjunct in its `met` line; zero `failed.append("`
  literals against three printed gate tokens) and parse the r61 counter's own bytes to
  confirm the repair (`c1_ok` in `met`; every printed token bound to a measured boolean
  via the in-code TOKEN_MAP); (b) its materialize-and-run helper refuses to execute any
  blob whose sha256 is not pinned (in-process, zero child executions recorded); (c) its
  frozen expect table is sha-pinned and a tampered table is refused; (d) live arm: the
  r61 `count-c1.py`/`count-c2.py` materialize at R with shas equal to the in-script
  pins; and `met` is the conjunction of all measured booleans including `c1_ok`.
- **Counting command:** `python3 .ufo/waves/round-61/count-c3.py <rev> [--repo DIR] [--scratch DIR]`
- **Frozen met line:** `C3=met r60hole=ok r61repair=ok blobrefusal=ok expectpin=ok livepins=ok cases=N rev=<rev>` (exit 0).
- **Before (control):** at the entering revision the r61 counter pins are
  unresolvable: `C3=unmet r60hole=ok r61repair=ok blobrefusal=ok expectpin=ok
  livepins=FAIL cases=5 failed=r61 counters absent or sha pin mismatch at rev` (exit 1);
  the red-before of the repair is the r60hole arm over the pinned r60 freeze bytes (the
  hole is present there), receipt committed at freeze.
- **Kill rule:** any static arm finding the r61 counter itself holey (no `c1_ok`, an
  unbound token), a successful execution of an unpinned blob, an accepted tampered
  expect table, or a live pin mismatch.
- A capability row enters SCORECARD only if the counter runs met in this round's report
  (capability acquisition shape; per the r60 contract ruling, instrument claims stay
  capability-only — no scalar move is claimed).

## Controls (do-nothing, committed before any seat scores)

`evidence/control-c1-do-nothing.txt`, `control-c2-do-nothing.txt`,
`control-c3-do-nothing.txt` — each counter run at the entering revision, capturing
stdout and `rc=` (defect r60-6 receipts carry exit codes from now on). Each control
must read unmet for the stated reason; a control that meets its target invalidates the
claim, not the data.

## Selftests

`evidence/selftest-c1.txt`, `selftest-c2.txt`, `selftest-c3.txt` — synthetic-fixture
batteries run at freeze; a red selftest blocks dispatch (r59 attempt-1 lesson).

## Wave

One v2 wave (policy v2, band 64–128): 64 seats, ≥25% attack roles, few connector
seats, godspeed directive bytes embedded and verified at dispatch time (r60
dispatch-payload defect). Seats attack the frozen counters pre-data; findings route to
the lesson; no post-scoring amendments.

## Sources & frontier step

C2 is the sourced claim: the six v7.3 copies are opened this round (fetch log in the
round lesson `## Gate`), rows S565–S070 appended in the data phase, census before
(337 rows, exit 0) and after recorded. Quarantine slice re-derived (3 rows: S244,
S262, S268 — verdicts maintained, no adoption). Assimilation: the merge/mori id-collision
check runs in scratch; mass id drift → L0 question + adopt nothing (recorded in the
report). One mistake is mined into the lesson `## Mistakes`.
