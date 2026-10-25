# ConnOverlap — overlap with round-45/prior repairs and axis attribution

Seat: connector (leaf). Wave: mori round 46 w1. Lane: mori-shokunin.
Scope: identify overlap between the round-46 calibration-repair proposal and
round-45/prior repairs, and any axis-attribution conflict. Findings only; no
verdict on the claim itself (a dispatched seat is not an independent judge).

## 1. What the frozen predicate targets

`count-repins.py` (sha256 `ebb6a6d3fe08d78791a45643d1ebda2243e5fff271eaada1d7f682317c673327`,
matches the claim's recorded counter hash) pins four `SKILL.md` rows:

| row (SKILL.md line) | pinned needles | origin of the row |
|---|---|---|
| `r44 gate registry (C2)` (:184) | `GATE_REGISTRY_SELFTEST pass=15 fail=0` | round-44 C2 repair created it (v1 auditor); round-45 rewrote the tool description in place (v2) but left the v1 tally |
| `r45 ledger counter (C1)` (:190) | `C1_SELFTEST pass=16 fail=0`, sha `5f2deea0…` | written by round-45 C2 registry repair (commit `18fd68b0`, "SKILL.md registry refresh") |
| `r45 gate conformance (C2)` (:191) | `C2_SELFTEST pass=14 fail=0`, shas `153423c48…`/`9850b3fcc…`/`8b82ac99…`, `743 lines` | same round-45 repair |
| `r44 gate registry (C2) — write scope superseded` (:194) | `GATE_REGISTRY_SELFTEST pass=15 fail=0`, sha `8b82ac99…`, `743 lines` | same round-45 repair (superseder row) |

Three of the four rows are round-45 repair products; the fourth is a round-44
product re-touched by round-45. The repair's surface is therefore entirely
inside earlier repairs' output.

## 2. Overlap with the round-45 repair (primary)

**The round-46 before-state is round-45's documented closure harm, not a newly
discovered drift.** The round-45 non-author verifier already enumerated the same
four cells, with the same pinned-vs-committed mismatches, at the round-45
landing `baabc992`, and ruled the round-45 C2 axis **harmed** over exactly
these cells (`corpus/lessons/round-45-verifier-spotcheck.md`, "Calibration
ruling" table: `:184` pinned pass=6 vs evidence pass=15; `:190` pinned
`f80e75ac…`/pass=10 vs `5f2deea0…`/pass=16; `:191` pinned `64db765e…`/622
lines/`e8ee29eb…`/pass=10 vs `8b82ac99…`/743/`153423c48…`/pass=14; `:194`
pinned pass=10/`64db765e…`/622 vs `8b82ac99…`/743/pass=15). It records that
`w1/CritAxisHarm.md` §1b flagged these cells inside round-45 and "they shipped
unmarked in `SKILL.md`". The worktree SCORECARD round-45 closure section
carries the same statement: "quality harmed due to stale registry cells".

So the round-46 repair is the remediation of round-45's declared
calibration-harm — a pre-declared debt, not a new finding. Overlap: same four
rows, same instruments, same axis, same defect record.

**The repair is not a duplicate claim of completed work.** Round-45's C2
counter (`count-c2.py`) verified registry structure, attribution, and real
`--selftest` argv branches; it never checked that the *recorded* tally/digest
values match the committed bytes. `C2=met` printed while the cells were false —
at `18fd68b0` (the very commit that wrote `:191`) the auditor was already
`8b82ac99…`/743 lines, yet `:191` pinned `64db765e…`/622 lines
(verifier-spotcheck.md). `count-repins.py` closes exactly that verification
gap. Round-45 neither claimed nor verified cell fidelity (it was marked harmed
for its absence), so attributing this repair to round 46 is not double crediting
a prior improvement.

## 3. Overlap with the round-44 repair (secondary)

The base `r44 gate registry (C2)` row is a round-44 product; the repair updates
its selftest cell from the round-44-era v1 measurement (pass=6) to the v2
measurement (pass=15). An r44-named row now carries r45-era instrument content —
already begun by round-45's in-place tool-description rewrite, and cemented by
the predicate's requirement. Not a conflict with the r44 counters: they audit
structural cells (entry resolution, standard cells, `--selftest` argv branch),
not tally text, so the edits do not change their verdict inputs.

The three other round-45 superseder rows (`:193` r44 C1, `:195` r44 C2,
`:196` r44 C3) carry the same kind of selftest re-run tallies and are **not**
pinned and not edited by the repair. I re-measured the r44 counters: their
recorded tallies (`C1_SELFTEST pass=6`, `C2_SELFTEST pass=5`,
`C3_SELFTEST pass=6`) reproduce exactly, so the unpinned cells are accurate;
the repair is consistently scoped to the four rows the predicate targets.

## 4. Axis attribution

Consistent: AXES.md defines calibration as "self-assessment quality … SHONEN.md/
SCORECARD entries match observed repo state"; replacing stale registry cells so
recorded values match measured instrument bytes is squarely that. The claim
declares calibration with the score held at 5 and no score delta — matching the
round-45 closure, which admitted no score changes.

Ambiguity to record (not smoothed): the same change also satisfies the
freshness axis verbatim ("Drift detection — skill claims re-verified against
live surfaces; stale items flagged or fixed"). Calibration and freshness are
both tied lowest at 5 (`SCORECARD.md`), and the round declares only calibration.
If the operator adjudicates "fixing stale pins" as freshness territory, this
single change is dual-attributable; the round should state in the claim why it
is calibration (registry self-description vs observed state) rather than
freshness, to avoid a later attribution dispute. As framed, no distinct-axis
rule is violated (it is one claim on one axis).

## 5. Risks

- Round-45's C2 verdict is "harmed" for the cells this round repairs. If the
  round-46 claim lands as calibration-improved, the scorecard must keep the
  round-45 harm and the round-46 repair as two distinct events (round-45 got no
  score delta; round-46's claim is the remediation, not an increment on an
  already-credited improvement).
- The predicate is substring-based on one row per name; the four-row scope and
  the unpinned superseder rows mean a future edit of `:193`/`:195`/`:196`
  would not be detected. That is a scope property of the frozen counter, not an
  overlap defect.

## 6. Verification (all reproduced this seat)

- Control: `control-skill.md` is byte-identical to `HEAD:SKILL.md`
  (sha256 `ed71e8f6…` both); `count-repins.py control-skill.md` →
  `MORI_R45_REPINS mismatches=4 rows=4`, exit 1.
- Repair: worktree `SKILL.md` → `MORI_R45_REPINS mismatches=0 rows=4`, exit 0;
  `git diff HEAD -- SKILL.md` touches exactly :184/:190/:191/:194 (4 insertions,
  4 deletions).
- Measured pins: `GATE_REGISTRY_SELFTEST pass=15 fail=0` (rc 0);
  `C1_SELFTEST pass=16 fail=0` (rc 0); `C2_SELFTEST pass=14 fail=0` (rc 0).
- File bytes: `tools/mori-gate-registry.py` = `8b82ac99…`, 743 lines;
  `count-c1.py` = `5f2deea0…`; `count-c2.py` = `153423c48…`; mutant
  `count-c2.py` = `9850b3fcc…` — all equal the round-45 freeze manifest
  (`evidence/freeze-r45.txt`) and the predicate needles.
- Round-44 unpinned superseder tallies reproduce: `C1_SELFTEST pass=6`,
  `C2_SELFTEST pass=5`, `C3_SELFTEST pass=6`.
