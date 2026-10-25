# CritNoOp — no-op satisfiability of the round-46 calibration-repair predicate

Lane: mori-shokunin, round 46 w1. Predicate under attack: `count-repins.py`
reports `MORI_R45_REPINS mismatches=0 rows=4` only when four specific SKILL.md
rows match measured pins; prior committed SKILL snapshot (do-nothing control)
must remain red. Role: UFO-FSD critic — evaluate whether a **no-op** can satisfy
the predicate, with a concrete replay. No code/production/other-seat files
edited; report only. No tools installed; no pacman.

## 1. Verdict

- **Literal no-op (do-nothing on the committed snapshot): does NOT satisfy.** The
  control is red, exactly as specified.
- **A no-op w.r.t. the calibrated instruments (text-only edit, zero tool/behavior
  change, zero recomputation): DOES satisfy.** The green state is reachable purely
  by string insertion into the four target rows; the checker never measures
  anything. The lane's own working-tree `SKILL.md` already satisfies the predicate
  *today*, before any round-46 commit, with the underlying tools bit-identical to
  the pins.

## 2. Evidence (all reproducible, read-only)

### 2.1 Control stays red (do-nothing correct)
```
$ python3 .ufo/waves/round-46/count-repins.py .ufo/waves/round-46/control-skill.md
MORI_R45_REPINS mismatches=4 rows=4
r44 gate registry (C2): stale/missing 1 pin(s)
r45 ledger counter (C1): stale/missing 2 pin(s)
r45 gate conformance (C2): stale/missing 5 pin(s)
r44 gate registry (C2) — write scope superseded: stale/missing 3 pin(s)
rc=1
```
11 pins missing in total; the control asserts older values (e.g. `GATE_REGISTRY_SELFTEST pass=6 fail=0`, v1 auditor 622 lines) where the needles demand current ones (`pass=15 fail=0`, v2 743 lines).

### 2.2 Green is already reached by the working tree, zero further action
```
$ python3 .ufo/waves/round-46/count-repins.py SKILL.md
MORI_R45_REPINS mismatches=0 rows=4
rc=0
```
`jj status`: `SKILL.md` is modified (uncommitted) in the working copy. Difflib
vs control: exactly **3 non-equal opcodes**, touching precisely the four target
rows (`r44 gate registry (C2)`, `r45 ledger counter (C1)`, `r45 gate conformance (C2)`,
`r44 gate registry (C2) — write scope superseded`) — nothing else differs.

### 2.3 The pins are digests of **unmodified** committed tools
```
8b82ac999091ebe65e765ed69f759910a57049ff0e7c5c4aa56df9c7168f5832  tools/mori-gate-registry.py          (needle "743 lines" == wc -l of same file)
5f2deea0b35c5e1346229d265aa0c07bf7f365bf6c5acda87648045bce658d23  .ufo/waves/round-45/count-c1.py
153423c48ca90466e85b02707828f5c6b2cf39c87c68ee67e3f9abee956baf93  .ufo/waves/round-45/count-c2.py
9850b3fcc8885456c3e71458b34184d716d54880a91ae5b29c7d003f26708703  .ufo/waves/round-45/fixtures/mutants/count-c2.py
```
`jj status` shows **none** of these files modified in the working copy → the
"repair" delta is confined to SKILL.md prose; no behavior of the calibrated tools
changes.

### 2.4 The checker performs no measurement
`count-repins.py` imports `subprocess` (line 5) but never calls it; `main()` only
reads the file argument and does substring containment against 11 hardcoded
literals. It does not recompute selftest tallies, hashes, or line counts, and does
not compare pins to the live repo. Green therefore proves *transcription of fixed
literals*, not calibration authenticity or freshness. Consequences:
- drift (tool digest/size changes without row updates) stays green — false calm;
- a forgery that writes the literals without measuring goes green;
- row uniqueness is enforced (exactly one `| <row> |`-prefixed line), and no
  needle appears anywhere else in control (whole-file scan empty), so the only flip
  path is textual insertion into the four target rows.

## 3. Concrete replay (in-memory, identical matching logic, no files written)

Take the red control, insert only the 11 missing needle literals into the four
matched rows (minimal text-only change, no tool execution, no other line touched):

```
before: mismatches=4 rows=4 (rc=1)
after : mismatches=0 rows=4 (rc=0)
```

This is the exact minimal satisfying delta, and it is a no-op for every calibrated
instrument. The same result is already observable for real at zero cost: run the
frozen predicate against the lane's current working-tree `SKILL.md` (2.2).

## 4. Impacted axes

- **calibration** (freshness/authenticity): the gate does not verify that pins
  equal live repo digests; green does not imply measured.
- **false provenance**: text-only injection satisfies without any measurement.
- **premature saturation**: since the working tree is already green, any pending
  "repair" commit is itself a no-op with respect to the predicate outcome; the
  wave's gate cannot distinguish it from an empty commit.

## 5. Smallest safe correction

Make the predicate verify pins against the repository instead of constant-string
containment: recompute (or read from a pinned manifest) the selftest tallies,
tool sha256s, and line counts **at the checked SKILL.md revision** and compare to
the row text; only then may `mismatches=0` be reported. This preserves the
do-nothing control (red today) while eliminating the text-only flip found here.
