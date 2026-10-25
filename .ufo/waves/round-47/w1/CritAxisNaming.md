# CritAxisNaming — round-47 wave w1: axis-naming attack on C1 and C2

Seat: CritAxisNaming (critic, leaf). Scope: attack the axis naming of both claims
against `AXES.md` and addendum §9 ("Name the axis by the surface the round changes"),
the operability/coverage/quality alternatives, and do-nothing reachability. Verdict
per claim. No production file touched; read-only git only.

## Rule text cited

- Canonical rule (fleet `AXES.md`): depth = "Verifiable technical detail — decision
  tables with real thresholds, named error signatures, cited sources"; coverage =
  "Fraction of the domain's real surfaces the skill governs (repo paths, tools, edge
  classes)"; operability = "Runnable artifacts: checklists that are executable,
  commands that exist, scripts that run"; calibration = "Self-assessment quality:
  gaps named honestly, confidence graded, overreach caught — SHONEN.md/SCORECARD
  entries match observed repo state"; freshness = "Drift detection — skill claims
  re-verified against live surfaces; stale items flagged or fixed".
- Addendum §9 (`/home/vgpnk/Projects/shokunin/scripts/hyaku/lane-addendum.md:282-283`):
  "A calibration claim must count mismatches between the lane's self-assessment
  (SCORECARD/SHONEN) and observed repo state. It cannot be an assertion."
- Addendum §9 (`lane-addendum.md:286-290`): "A target must be one a do-nothing
  control cannot reach … Before freezing, build the cheapest control that skips the
  claimed work, score it with the frozen counter, and commit that receipt."
- Addendum §9 (`lane-addendum.md:295-299`): "Name the axis by the surface the round
  changes, not by the number it produces (kaidoku r29). Re-scoring a rule the lane
  already holds on new inputs, or counting rows a sourceless fixture also counts, is
  quality work, never coverage or depth. A coverage claim names the surface it moves
  (frontier → core, a new tool, operation or edge class) and the command that would
  show it unmoved."

## C1 — verdict: calibration is correctly named (no defect)

Surface the round changes (contract.md:21): `SKILL.md` gate-registry tables — "the
lane's self-assessment of its own instruments". P-C1 (contract.md:27-31) counts
mismatches between pins in the self-test cells and the observed `--selftest` output of
the committed bytes. That is verbatim the §9 calibration recipe: count mismatches
between self-assessment and observed repo state.

Counterexample tested — "C1 is operability/coverage because the round ships a new
tool (`tools/mori-pin-check.py`)":

- Evidence: `git show 2d85e33…:tools/mori-pin-check.py` → exit 128 (absent at entering
  tip); present at freeze `63eecf27`. So the instrument IS new this round.
- Why this does not re-label the claim: the tool is the measuring device (frozen
  instrument, contract.md:14), not the surface the claim changes. The claim's
  before→after is a registry-cell property: at entering, exactly one pin mismatches
  (SKILL.md:912 pins `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0`, observed
  `pass=22 fail=0` — `evidence/control-c1-donothing.txt`), and P-C1 flips to met only
  when the cell truth is repaired. The tool alone, without the cell fix, keeps
  `PIN_CHECK=unmet` — so the round's measured surface is self-assessment truth, not
  the tool's existence. The same failure class (round-46 false-green:
  `controls/control-c1-moved.md`) is a cell-truthfulness defect, which is why the
  round-46 closure routed the claim here as calibration (contract.md:22-25).
- Secondary note (not a defect): the new runnable artifact qualifies for the
  `capabilities:` table (AXES.md:57-64) if demonstrated; that is a separate record
  from the claim's axis.

Reachability by do-nothing: not reachable. `evidence/control-c1-donothing.txt`
(entering revision, frozen counter) → `PIN_CHECK=unmet … mismatches=1 … rc=1`. The
three published evasion controls (deleted → `dropped`, moved → `mismatch`, truncated →
token-boundary `mismatch`) each stay unmet, so a no-op revision cannot hit the target
(contract.md:37-41).

## C2 — verdict: depth is correctly named (no defect)

Surface the round changes (contract.md:48-54): the FR13 knowledge area (eBPF
kill/OOM tracing) — a new catalogue entry per TRACE_EVENT of the committed Linux v7.2
`include/trace/events/oom.h` copy, with per-event field sets and emitting call sites,
sourced through new row S475.

Counterexamples tested:

1. "C2 is coverage (a new surface governed)": FR13 is already a governed frontier
   area — `PROVINCE.md:56` ("retain this as knowledge/frontier only"), with prior
   entries (`oom-victim-selection-r27.md`, `oom-victim-context-r41.md`) and OOM
   source rows S002–S021. The round does NOT move frontier → core (the entry stays in
   `corpus/knowledge/`; the counter checks no PROVINCE change), so none of the §9
   coverage surfaces (frontier→core, new tool, operation, edge class) is moved.
   Coverage = fraction of surfaces governed; this round changes detail within an
   already-governed area, not the fraction.
2. "C2 is the §9 'quality work' trap (counting rows a sourceless fixture also counts)":
   the source of the count is pinned v7.2 committed copies (frozen sha256 `PINS`,
   count-c2.py:35-40) plus a mined tier-A code row S475 — not a sourceless fixture.
   The strongest local counterexample is `controls/control-c2-three.md`: the staged
   "exactly three tracepoints" claim rendered as a table stays `C2=unmet
   name_mismatch` — the counter passes only on the full 8-event, field-exact
   catalogue. That proves the measured property is verifiable detail (depth:
   "decision tables with real thresholds … cited sources"), not breadth (coverage) or
   a re-scored rule.
3. Adjacent-axis probe — freshness: correcting the wrong "three" claim is a drift-fix
   flavor, but the round's deliverable is new field-level catalogue detail (the
   corrective count is a consequence), and P-C2 measures the new detail, not a
   re-verification log of a live surface. Freshness is adjacent, not the surface
   changed.

Reachability by do-nothing: not reachable. `evidence/control-c2-donothing-at-freeze.txt`
(freeze commit, frozen counter) → `C2=unmet failed=entry_absent,source_row`; the
staged (`control-c2-staged`) and three (`control-c2-three`) controls likewise stay
unmet (contract.md:70-74).

## Claim-structure checks (AXES.md "Working the axes")

- Distinct axes: C1 calibration vs C2 depth — distinct ✓ (contract.md:80-84
  separability is consistent).
- Lowest-axis obligation: entering scores tie depth/freshness/calibration at 5;
  both claims work tied-low axes ✓ (contract.md:8-10).
- Do-nothing receipts committed before data for both claims ✓ (addendum §9 line 286).

## Impacted axes

None harmed by the naming. Calibration and depth are the correct labels; operability/
coverage/freshness are alternatives the local evidence rejects. No re-scoring or
predicate change is proposed.

## Smallest safe correction

None required. Optional (does not affect verdict): record `tools/mori-pin-check.py`
in the capabilities table when demonstrated, and keep the C1 report's evidence pointer
fresh (the entering-tip absence of the tool means the "before" receipt is necessarily
frozen-tool-on-entering-bytes evidence — the contract already states this at line 17).

## Observed context (mid-w1, not verdict basis)

Working tree currently carries uncommitted integration drafts (SKILL.md, SOURCES.md,
QUALITY.md, README.md modified; entry `corpus/knowledge/oom-tracepoints-r47.md`
untracked; S475 already present in SOURCES.md used-by). These are build-phase WIP; the
axis analysis above is grounded only in the frozen contract, freezed instruments,
controls and receipts.
