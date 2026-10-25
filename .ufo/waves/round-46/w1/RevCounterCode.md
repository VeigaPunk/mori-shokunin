# RevCounterCode — review of count-repins.py (round 46)

Scope: inspect `.ufo/waves/round-46/count-repins.py` for wrong path assumptions or a
reachable false green against the frozen predicate ("mismatches=0 rows=4 only when
four specific SKILL.md rows match measured pins; prior committed SKILL snapshot = do-nothing
control, must remain red").

## Method (evidence)

- Executed the counter against the live `SKILL.md`:
  `python3 .ufo/waves/round-46/count-repins.py SKILL.md` → `MORI_R45_REPINS mismatches=0 rows=4`, exit 0.
- Executed it against the committed control `.ufo/waves/round-46/control-skill.md` →
  `MORI_R45_REPINS mismatches=4 rows=4` (`r44 gate registry (C2): stale/missing 1 pin(s)`,
  `r45 ledger counter (C1): stale/missing 2 pin(s)`, `r45 gate conformance (C2): stale/missing 5 pin(s)`,
  `r44 gate registry (C2) — write scope superseded: stale/missing 3 pin(s)`), exit 1. Control stays red as required.
- All four row prefixes occur exactly once in live `SKILL.md` (grep -cF = 1 each; lines 184, 190, 191, 194).
- Pins verified as genuine measurements:
  - `python3 .ufo/waves/round-45/count-c1.py --selftest` → `C1_SELFTEST pass=16 fail=0` (pin: pass=16 fail=0; sha256 `5f2deea0…` matches current bytes of count-c1.py).
  - `python3 .ufo/waves/round-45/count-c2.py --selftest` → `C2_SELFTEST pass=14 fail=0` (pin: pass=14 fail=0; sha256 `153423c48ca…` matches count-c2.py; `9850b3fcc…` matches `fixtures/mutants/count-c2.py`).
  - `python3 tools/mori-gate-registry.py --selftest` → `GATE_REGISTRY_SELFTEST pass=15 fail=0` (pin: pass=15 fail=0; sha256 `8b82ac…` matches auditor; wc -l = 743).
  So today's green is not a current falsehood; the four live rows genuinely carry the measured pins.

## Findings (by severity)

### F1 — Reachable false green: pin matching is column-agnostic substring containment (medium)
Predicate check (count-repins.py:29-33) is:

    matches = [line for line in lines if line.startswith("| " + row + " |")]
    ...
    missing = [needle for needle in needles if needle not in matches[0]]

A needle may sit in **any** cell of the row line; the counter does not verify the pin
occupies the measured (selftest / pinned-values) cell. Demonstrated: took live SKILL.md,
removed `GATE_REGISTRY_SELFTEST pass=15 fail=0` from row 184's selftest cell (left it
"not measured") and appended the phrase to the row's owner cell. Counter still prints
`mismatches=0 rows=4`, exit 0. So a row whose measured cell no longer carries the value
can go green if the literal appears anywhere else in that same row (e.g., in a comment,
description, or owner cell).

### F2 — Reachable false green: needles are unanchored substrings (low-medium)
`needle not in matches[0]` is a raw substring test, so mutated/partial tokens pass:
- Demonstrated: change row 190's tally from `C1_SELFTEST pass=16 fail=0` to
  `C1_SELFTEST pass=16 fail=00` → still green (needle `pass=16 fail=0` is a substring).
- `743 lines` matches any occurrence, e.g. a cell reading "x 743 lines y" or unrelated counts.
- Hash needles match prefixes of longer hex strings (a superset digest starting with the pin hash satisfies it).
- `pass=15 fail=0` matches `pass=15 fail=0` with extra trailing characters in the same token.

### F3 — Pins guard text only, never bytes (low, verification gap)
The counter never touches the underlying tools; it re-checks neither file hashes nor
selftest tallies. If the on-disk tool bytes drift (e.g., count-c1.py changes) while row
text retains the old hashes, the counter stays green although the "measured" state no
longer holds. This is inherent to a text-presence check, but the predicate's "match
measured pins" claim is not re-validated by the instrument.

### F4 — Wrong path assumption: cwd-relative default, no repo-root discovery (low)
`parser.add_argument("skill", nargs="?", default="SKILL.md")` resolves relative to the
current working directory. Demonstrated: running from `/tmp` with no argument →
`FileNotFoundError: 'SKILL.md'`, exit 1. This fails **closed** (red, not green), but the
check's meaning depends on the harness cwd being the lane root; an invocation from
`tools/` or `.ufo/waves/round-46/` silently turns into a non-evaluation rather than a
verdict. No repo-root derivation is attempted.

### F5 — `rows=4` is unconditional (info)
`rows={len(ROWS)}` is printed regardless of how many rows actually matched (count-repins.py:36).
Not a false-green vector by itself (a missing row still appends an error), but the printed
`rows=4` does not report the number of rows actually found.

## Residual risk / verification gaps

- Read-only inspection only: control-skill.md was not byte-compared to the VCS parent
  commit (no git/jj reads of history performed); its row 184 shows the pre-update text
  (`GATE_REGISTRY_SELFTEST pass=6 fail=0`), consistent with the do-nothing control, and the
  counter run on it is red. No claim is made about which commit produced it.
- Hash pins were compared against current disk bytes, not against the bytes at the
  measurement revision; selftest tally runs today match the pinned tallies.
- F1/F2 are demonstrated as reachable states; they do not describe the current live file
  (which is genuinely green by all pins above).
