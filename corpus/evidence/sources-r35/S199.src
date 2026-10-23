# Shokunin Expertise Axes

What makes a shokunin an expert is decomposed into measurable axes. Every
shokunin works its own subset; the protocol and aggregator lanes own the
fleet-level axes.

## The six axes

| Axis | Definition | Signal an expert shows |
|---|---|---|
| **depth** | Verifiable technical detail — decision tables with real thresholds, named error signatures, cited sources | A reader can act on SKILL.md alone; no filler |
| **coverage** | Fraction of the domain's real surfaces the skill governs (repo paths, tools, edge classes) | PROVINCE.md lists every surface; none unexplored without reason |
| **operability** | Runnable artifacts: checklists that are executable, commands that exist, scripts that run | A checklist item can be run and produces the stated outcome |
| **freshness** | Drift detection — skill claims re-verified against live surfaces; stale items flagged or fixed | Each round LOG entry includes a re-verification result |
| **calibration** | Self-assessment quality: gaps named honestly, confidence graded, overreach caught | SHONEN.md/SCORECARD entries match observed repo state |
| **adjacency** | Cross-domain awareness — evidence belonging to another domain reported, not absorbed | Lane reports name contested scope; integrator arbitrates |

## The learning path

The axes are the unit of work; the learning signal is `LEARNING.md`'s three
trends. Expansion ↔ `coverage` + `adjacency`; quality ↔ `depth` + `freshness`
+ `operability`; discernment ↔ `calibration`. Pick the round's axis from the
trend furthest behind.

## Working the axes — a round is 1–3 claims

A lane's round declares **1–3 claims**; each claim is one axis-move: pick the
axis, land one verifiable improvement, measure it (file exists / command runs /
citation resolves), record before→after in `SCORECARD.md`, log evidence in
`LOG.md`. Every claim carries its own falsifiable before→after. Claims must be
**causally separable** — each verifiable without the others having landed —
and name **distinct axes**; two claims on one axis in one round count as one
claim. At least one claim works the lane's **lowest-scoring non-retired axis**,
except when the stagnation nudge (below) waives it. A round is admitted only if
every claim verifies **and no axis is harmed** — a trade anywhere is not an
improvement: report every verdict and let the operator rule. If an axis
saturates, the lane may retire it or split it into a sub-axis — recorded in
`SCORECARD.md` with reason.

A claim may instead be a **capability acquisition** (below); it still lands a
per-axis verdict, with the claim type recorded in the round report.

A claim may also be declared **exploratory** when the improvement is real but
not countable — elegance, quality of technique, a novel resolution path; the
moves that make a craft a craft. The claim names what it improves and why the
prior state lacked it; no counting command is required. An exploratory claim
verifies only as `unprovable-but-better` **with a named non-author reviewer on
record** (reasons included; a dispatched subagent does not count) — "everyone
knows what it is" made procedural: discernment is checked from outside
(`LEARNING.md`). Without that judgment it lands `unprovable` and the
honest-stop rule applies. At most one exploratory claim per round. The score
on a subjectively-moved axis need not change: the `SCORECARD.md` row then
carries the verdict and the reviewer pointer instead of a number — a score no
reader can re-derive is an opinion, not a measurement, and the row says which
one it is.

## Capabilities — the repertoire table

The six axes measure the quality of what the skill knows; they do not measure
what the shokunin can now *do*. `SCORECARD.md` therefore carries a separate
`capabilities:` table — name → what it can now do (one line) → evidence
pointer (command or path) → first-working round. Rows enter only through a
round that demonstrates the capability running; a capability without a passing
demonstration in the round report is pre-claiming and does not enter the table.

## The stagnation nudge

When every axis the lane owns sits at or above the lane's saturation line and
no capability has entered the table within the lane's stagnation window (both
recorded in `SCORECARD.md`), the lowest-axis obligation is waived: the round
should be a frontier/capability move — grow the repertoire or move
`PROVINCE.md` frontier ground into core, claimed and measured like any other
claim.

## SCORECARD.md contract (per child repo)

| Field | Content |
|---|---|
| axes | Axis name → score 0–10 + evidence pointer (measurable moves) or `unprovable-but-better` verdict + named non-author reviewer (exploratory moves) → last-change round |
| capabilities | The repertoire table (see Capabilities): name → what it can now do → evidence pointer → first-working round |
| planned | The next round's intended claims (1–3), each with its target axis or capability |
| saturation | The lane's saturation line + stagnation window N (drives the nudge) |
| retired | Axes retired with justification (saturation or wrong fit) |
