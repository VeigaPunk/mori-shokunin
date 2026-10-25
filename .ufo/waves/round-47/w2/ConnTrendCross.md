# ConnTrendCross — wave w2: cross-check of the round-47 trend story

Seat: ConnTrendCross. Scope: does C2 count as **expansion** (new admitted entry on uncovered
coverage-map ground) or as depth/quality only; does C1 + v2 count as **discernment improved**
(lesson-backed criterion) or unchanged. Per-trend verdict suggestions with evidence.

All reads at the landed tip `68d66ca53d89be5c34a62f46af7c37449d9f9b63` (T). This seat is a
dispatched member of the lane; it is not an independent judge — the verdicts below are
*suggestions* for the outside closure, following the observables in `LEARNING.md` and
`AXES.md`.

## 1. Evidence observed (committed at T unless noted)

### 1.1 The new C2 entry and its map row

- `corpus/knowledge/oom-tracepoints-r47.md` (committed at T) opens with `source:` S475, S476,
  S477, S478, S005; `verified-at: 2026-10-25`; `recheck:` = `count-c2.py <rev>`; header
  `coverage-map: FR13`; `ground: frontier item FR13 — "eBPF kill/OOM tracing …"`.
- `corpus/README.md` Frontier table row FR13 (line 353, committed): `| FR13 | eBPF kill/OOM
  tracing | SOURCES.md:11-12,23-26 | Privilege and version matter; a resident tracer is outside
  the census, so retain this as knowledge/frontier only. |`.
- `corpus/README.md` "Round-47 coverage additions" section (committed, lines 644-655) states
  verbatim: "FR13 ground the map held only as a peer-reviewed abstract
  (`knowledge/oom-victim-context-r41.md`, S262) and one queued field-schema row (S005): the
  **full v7.2 `oom` trace-event set** — eight events … Entry:
  `corpus/knowledge/oom-tracepoints-r47.md` … FR13 stays frontier: no tracer is enabled,
  installed or proposed".
- Comparison entry `corpus/knowledge/oom-victim-context-r41.md` (admitted round 42) holds
  FR13/FR1 as the *victim-selection container-context abstract* (S262); it carries no tracepoint
  inventory. S005 was `queued` until this round (lesson Gate, rule 2: `queued` → `mined`,
  `used-by` → `corpus/knowledge/oom-tracepoints-r47.md`).
- `corpus/SOURCES.md` at T: S475/S476/S477 (own-work)/S478 rows all `mined`, tier A, `used-by`
  naming the entry (grep S475 → 3 hits; rows read at HEAD).

Commands (read-only git):
- `git show HEAD:corpus/README.md | grep -c "Round-47 coverage additions"` → `1`, exit 0.
- `git show HEAD:corpus/README.md | grep -n "^| FR13"` → `353`.
- `git show HEAD:corpus/QUALITY.md | grep -c "123\.\|124\."` → `2`.
- `git show HEAD:corpus/lessons/round-47.md | grep -n "No non-author spot-check"` → `57`.

### 1.2 C2 claim receipts (not re-run by this seat; receipt-cited)

- `evidence/after-c2.txt`: `$ python3 .ufo/waves/round-47/count-c2.py af2250d8…` →
  `C2=met events=8 rows=8 name_mismatch=0 field_mismatch=0 callsite_mismatch=0
  pin_mismatch=0 source_row=ok provenance=ok …` rc=0.
- Counter bytes unchanged freeze→T: `git diff --stat 63eecf27 HEAD -- .ufo/waves/round-47/count-c2.py`
  → empty.

### 1.3 Discernment / calibration evidence

- `tools/mori-pin-check.py`: frozen v1 sha256 `e3ef425a…` (`git show 63eecf27:tools/mori-pin-check.py |
  sha256sum`); tracked tool at T sha256 `9832e38c…` (`sha256sum tools/mori-pin-check.py`);
  `git diff --stat 63eecf27 HEAD -- tools/mori-pin-check.py` → `223` lines changed
  (+186/−37) → the tracked tool at T is the hardened v2. C1 is scored with the frozen v1 bytes
  (`evidence/after-c1-v1-frozen.txt`: `PIN_CHECK=met tally_pins=28 digest_pins=5 mismatches=0
  unparsed=0 no_command=0 dropped=0` rc=0 at `af2250d8`).
- Wave-1 falsification class (M2) shown at freeze rev `63eecf27`:
  - `evidence/v1-junk/skill-v4-weakened.txt` (weakened pin `pass=2`): `PIN_CHECK=met …
    mismatches=0`, rc=0 — frozen v1 scores a junk edit green.
  - `evidence/v2/skill-v4-weakened.txt`: `PIN_CHECK=unmet … mismatches=1 rebound=0 duplicate=0`,
    rc=1 — v2 scores the same junk edit unmet.
- `corpus/QUALITY.md` at T (committed):
  - **123** "A registry pin is calibrated only when an instrument re-runs it from committed bytes
    and reads it from its own cell." Lesson: `corpus/lessons/round-47.md` M1, M2;
    `considerthese/2026-10-25.md` suggestion 1 (operator-authored reflection); rationale cites
    round-46's outside verifier routed defect 1 (`corpus/lessons/round-46-verifier-spotcheck.md`)
    and the stale `SKILL.md:912` pin (`pass=15` vs tool `pass=22`). "Shown able to fail": at
    entering `2d85e33` → `PIN_CHECK=unmet … mismatches=1`; controls stay unmet.
  - **124** "A stated count of kernel objects carries the enumerating command over a pinned
    source." Lesson: `corpus/lessons/round-47.md` M3 (staged "exactly three named tracepoints"
    vs header's eight; `controls/control-c2-three.md` → `name_mismatch=5` at freeze).
- `corpus/lessons/round-47.md` (committed) line 57-58: "No non-author spot-check of this round's
  gate decisions exists yet; the hyaku closure session is the outside check (LEARNING.md). Sample
  offered: admit S478, reject the staged entry's count." No `round-47-verifier-spotcheck.md` exists
  in `corpus/lessons/` (glob).

### 1.4 Capability table — uncommitted at T

- `SCORECARD.md` working tree (NOT at HEAD; `git show HEAD:SCORECARD.md` has no round-47
  section) carries a draft "Round 47" section including a `capabilities:` row "registry pin
  reconciler (v2)", first-working round 47, evidence `PIN_CHECK_SELFTEST pass=34 fail=0`
  (`evidence/after-c1-v2.txt` line 33) and `evidence/v2/` vs `evidence/v1-junk/`. At T this row
  is a proposal, not a committed record (the closure gets the final say).

## 2. The two asked questions

### Q1 — Does C2 count as expansion, or depth/quality only?

Expansion observable (LEARNING.md): "admitted `knowledge/` entries on ground the coverage map did
not hold, each `source:` citing a `mined` `corpus/SOURCES.md` row (`own-work` rows included) …
frontier areas entered; new kinds of source; a capability admitted to `SCORECARD.md`".

- One new knowledge entry admitted this round (net new = 1): `oom-tracepoints-r47.md`.
- Its ground: FR13's *tracepoint event-set/field-schema inventory*. Before this round the map held
  FR13 only as the victim-selection abstract (r41, S262) plus the queued S005 row — the README's
  own Round-47 note says exactly that. The tracepoint inventory ground was therefore not held.
- Every cited source row is `mined`, including own-work S477; S005 moved `queued` → `mined` with
  `used-by` naming the entry.
- The README coverage-additions row exists at T (contrast round 18, where expansion was held
  `unchanged` because the map carried no rows).
- FR13 remains frontier (no Core move claimed); exploring frontier sub-ground is the expansion
  observable "frontier areas entered" (same shape as round-44's FR5 sub-ground entry, graded
  expansion improved by its closure).

Suggestion: **expansion: improved** — C2 is a new admitted entry on previously-uncovered FR13
sub-ground, all sources mined, map row present. Caveat: if the closure reads "uncovered ground"
at whole-FR granularity (any prior entry on FR13 blocks expansion), C2 is depth/quality only and
expansion is `unchanged`; the README's own "held only as an abstract + queued row" framing
supports the former reading.

### Q2 — Does C1 + v2 count as discernment improved, or unchanged?

Discernment observable (LEARNING.md): "gate decisions vs the outside spot-check; `QUALITY.md`
criteria"; `improved` when "the spot-check agrees with the gate on admits *and* rejects, **or** a
disagreement becomes a lesson that adds a grounded `QUALITY.md` criterion".

- This round's gate decisions (admits S475–S478; rejects: staged entry's "exactly three" claim,
  staged S501) have no outside spot-check on record yet — the lesson says so, and no
  `round-47-verifier-spotcheck.md` exists.
- However, a *prior outside disagreement* was learned this round: round-46's non-author verifier
  routed defect 1 (row-wide needle-matching `count-repins.py` scored green with a stale receipt in
  the cell; the r46 closure ruled C1 `unprovable`). That disagreement became lesson M1/M2 and
  grounded QUALITY 123 (cited to `round-46-verifier-spotcheck.md`, the r47 lesson, and the
  operator-authored considerthese suggestion), with able-to-fail controls. QUALITY 124 grounds the
  count-overclaim (M3). Both criteria are committed at T and cite their lessons.
- Precedent: the r14 and r17 closures granted discernment `improved` when a prior outside
  disagreement became lesson-backed grounded criteria even with the current round's spot-check
  pending; r17 explicitly denies that credit to author-lane findings alone ("Author-lane findings
  produced Q47–Q50 but are **not** outside agreement"; r13: "Neither self-dispatched reviews nor
  this mixed result establish an unqualified discernment improvement"). The M1–M3 mistakes are
  lane-found; the *outside* element is the r46 routed defect.

Suggestion: **discernment: improved is defensible via the prior-outside-disagreement-learned
path** (QUALITY 123 grounded on r46's outside routed defect 1 + operator suggestion, with
able-to-fail witnesses; QUALITY 124 grounded on M3) — this matches the r14/r17 standard. If the
closure requires *this round's* outside agreement on admits+rejects before crediting the trend,
hold **unchanged** until the hyaku closure spot-checks the offered sample (admit S478, reject
staged entry). C1+v2 alone (internal lessons + v2 hardening) would not suffice under either
reading: internal finds are calibration work, not outside agreement (r13/r17).

## 3. Other-trend notes

- **Quality: suggested unchanged.** No existing entry was re-verified, deepened, or superseded by
  a stronger one; the C2 entry is a new admission, not a quality movement under LEARNING's
  observable.
- The C2 claim's axis is depth (held 5); counting the entry as expansion does not conflict with the
  claim's axis label (LEARNING.md: expansion ↔ coverage/adjacency; a depth claim can still feed the
  expansion trend if the observable is met).

## 4. Risks / limits

- No outside spot-check of the r47 gate exists at T; the trend verdicts are the closure's to
  make. My suggestions follow the committed observables and prior closures.
- The SCORECARD capabilities row ("registry pin reconciler v2") is uncommitted at T; this seat does
  not count it as a committed expansion signal.
- Working tree at read time carried uncommitted edits to `LOG.md`/`SCORECARD.md` (the in-flight
  round record) plus `.scratch/pin-check-*` debris; every file cited above as committed was
  verified against HEAD via `git show`.
- UNVERIFIED: this seat did not re-run `mori-pin-check.py` or `count-c2.py`; the claim outcomes
  are receipt-cited (`evidence/after-c1-v1-frozen.txt`, `after-c1-v2.txt`, `after-c2.txt`).
