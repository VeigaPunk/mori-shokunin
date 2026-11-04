# mori round 89 — frozen contract (claims, predicates, populations, kill rules, controls)

Lane: mori (fleet & host observability; detection and report only).
Round: 89, attempt 1. L1: `MoriR89`.
Entering revision: `30a29797012281b9fd0c748b38b929ac67f8c754` (lane `master`).
Frozen before any after-value is measured. This file, each counter's docstring, the printed
target line and the receipt label are the same sentence.

## Why this round

Round 88 was closed `rejected-harmed` (`corpus/lessons/round-88-verifier-spotcheck.md`). Two
routed defects drive the claims:

- **D2** — the r87 receipt gate refuses a *genuine* `./tools/...` replay (`cmd-binding`), and
  two execution-binding evasions pass: a bound path named only inside a shell comment, and a
  self-printing command that merely names the bound path. Operability was harmed.
- **D3** — a kill is not attributed to a declared failing arm: an unrelated nonzero exit
  established "killed", so the checksum canary reached the r88 C1 target with no arm present.

Plus D4 (12 r88 mutation survivors) and the legibility debt (dead assignment, misleading
`FX clean ... refused` wording).

## Claims (2; distinct axes)

### C1 — operability: the receipt gate binds the *executed script*, by path identity

Subject: `.ufo/waves/round-87/count-c2.py` (registered gate, `SKILL.md` row 21/22).
Change: `binding_problems` replaces "the bound path appears as a raw whitespace token" with:

1. the `# cmd:` string is split into invocations on `;`, and each invocation into shell tokens
   with `shlex.split(..., comments=True)` — **comments are dropped**, so a path named after an
   unquoted `#` no longer binds;
2. a token names the bound path iff `os.path.normpath(token) == os.path.normpath(path)`, or,
   with a repo root, the two realpaths are equal — so `./tools/x.py` and `tools/x.py` are the
   same file;
3. the matching token must sit in **script position**: index 1 after an interpreter
   (`python3`, `python`, `bash`, `sh`, `node`, `uv`), or index 2 when index 1 is a flag
   (`-I`, `-B`, ...). A path passed as data, as an assignment, or printed by `printf`/`echo`
   does not bind.

Callers are migrated in the same landing: `.ufo/waves/round-88/count-c2.py` pins the gate's
selftest arm count (`SUBJECT_ARMS`, `TARGET`, its `arms_pinned` and `target_fields` arms).

**Frozen predicate P-C1.** At revision R, `python3 -I .ufo/waves/round-89/count-c1.py R`
prints exactly

```
C1=met equiv=accepted comment=refused selfprint=refused real=met arms=26
```

and exits 0, where:

- the gate at R is green at exactly **26** selftest arms (`C2_COUNTER_SELFTEST pass=26 fail=0`);
- the gate at R still prints the r87 target line on the real seven-receipt population:
  `C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4
  matched=6 defeated=1 superseded=2 legacy=1 unexpected=0`;
- **equiv** — a `clone` receipt whose `# cmd:` is `python3 -I ./tools/mori-record-sweep.py
  --root . --pins .ufo/waves/round-82/record-pins.json` and whose body is the real stdout is
  accepted (`RECEIPT … met problems=-`), the equivalence-positive control;
- **comment** — the same receipt whose `# cmd:` prints the exact body and names the bound path
  only after `#` is refused with `cmd-binding` in its `problems=`;
- **selfprint** — the same receipt whose `# cmd:` is
  `python3 -c "print('RECORD_SWEEP pending=0 pinned=0 carriers=1 bindings=3 revisions=0')" tools/mori-record-sweep.py`
  (prints the exact body, names the bound path as data) is refused with `cmd-binding`.

Fixtures are commits inside `--shared` clones under `--scratch`; the lane is never written.

**Entering (measured, `evidence/controls-r89.txt`):** `C1=unmet equiv=refused
comment=accepted selfprint=accepted real=met arms=23` rc 1.

### C2 — calibration: the twelve r88 survivors armed, and each kill attributed to its declared arm

Subjects: `.ufo/waves/round-88/count-c1.py` (3 survivors) and `.ufo/waves/round-88/count-c2.py`
(9 survivors), population from `.ufo/waves/round-88/w1/Mo88M01Mut.md` (32 mutants, 20 killed,
12 survived).

Change: one new selftest arm per declared mutation, each arm red under exactly that mutation;
`own_ok` is extracted to `own_ok_of(rc, out)`, `met_line(rev)` and `clone_root_ok(top, d)` are
extracted as pure helpers so the arms can call them; the dead `want_met` assignment is deleted
and the `FX … refused` wording becomes `FX … ok` (a clean fixture no longer reads "refused").
New arm counts: `count-c1.py` 25 → **28**, `count-c2.py` 17 → **26**.

**Frozen predicate P-C2.** At revision R, `python3 -I .ufo/waves/round-89/count-c2.py R`
prints exactly

```
C2=met mutants=12 killed=12 survivors=0 unattributed=0 unanchored=0 arms=28,26
```

and exits 0, where, for every declared mutant `(file, label, arm, old, new)` in the population
below: the subject at R is green at exactly its frozen arm count; `old` occurs exactly once in
that subject (else `unanchored`, claim unmet); the mutated copy's own `--selftest` is run and
the mutant is **killed** only when that run exits non-zero or prints `fail=<n>`, n>0, **and**
a `FAIL <arm>` line names the declared arm of that mutant. A red run with no declared-arm FAIL
is `unattributed` and keeps the claim unmet.

**Kill rule, frozen.** `killed ⟺ (rc≠0 ∨ fail>0) ∧ FAIL <declared arm> present`. Unanchored,
empty mutation, red pristine, wrong pristine arm count, any survivor, any unattributed kill →
`C2=unmet`. Exit 2 is setup, never a pass.

**Entering (measured, `evidence/controls-r89.txt`):** `C2=unmet mutants=7 killed=0
survivors=7 unattributed=0 unanchored=5 arms=25,17` rc 1 — five declared anchors guard code the
entering revision does not have yet (the two `own_ok_of` helpers, `met_line`, `clone_root_ok`
and the `arms=26` target), so they read `unanchored`, never killed; the seven anchors that do
exist all survive.

### Population (C2) — labels, declared arms, anchors re-derived from the after bytes

| file | mutant label (r88) | declared arm | anchor → replacement |
|---|---|---|---|
| count-c1.py | `C1-arms-first` | `arms_last_tally` | `for m in ARMS.finditer(out):\n        pass` → `… break` |
| count-c1.py | `C1-green-drop-fail` | `green_mixed_fail` | `return rc == 0 and "fail=0" in out and not FAIL.search(out)` → drops the FAIL conjunct |
| count-c1.py | `C1-own-ok` | `own_ok_red` | `return (rc == 0 and "C1_COUNTER_SELFTEST" in out` → `return (True or rc == 0 and …` |
| count-c2.py | `C2-target` | `target_full` | `TARGET = "real=met fx=4 clean=1 refused=2 absent=1 arms=26"` → `real=unmet` |
| count-c2.py | `C2-printed-target` | `met_line_derived` | `return "C2=met %s rev=%s" % (TARGET, rev[:12])` → a literal target |
| count-c2.py | `C2-fixture-clean` | `clean_wrong_split` | `verdict.startswith("C2=met " + REAL)` → `startswith("C2=met ")` |
| count-c2.py | `C2-receipt-name` | `receipt_name_bound` | `if m and m.group(1) == name:` → `if m:` |
| count-c2.py | `C2-clone-top` | `clone_top_bound` | `return top_out.strip() == os.path.realpath(d)` → `return True` |
| count-c2.py | `C2-own-ok` | `own_ok_red` | `return (rc == 0 and "C2_COUNTER_SELFTEST" in out` → `return (True or …` |
| count-c2.py | `C2-verdict-first` | `verdict_last_wins` | `last = line\n    return last` → inserts `break` |
| count-c2.py | `C2-no-supersedes` | `absent_without_supersedes` | `raise ValueError("fixture receipt has no '# supersedes:' line")` → `pass` |
| count-c2.py | `C2-vacuous-body` | `vacuous_body_fabricated` | `body = ["RECORD_SWEEP fabricated=1"]` → `body = body` |

The exact anchor and replacement strings live in `.ufo/waves/round-89/count-c2.py` (`MUTANTS`),
which is frozen with this contract.

## Controls (committed before data; `evidence/controls-r89.txt`)

1. **Do-nothing control** — both counters at the entering revision: `C1=unmet`, `C2=unmet`.
2. **Skip-work control** — the cheapest variants that skip each claim's work:
   - C1: the gate with the three new arm labels appended but `binding_problems` unchanged →
     `C1=unmet equiv=refused comment=accepted selfprint=accepted real=met arms=26` (the arms
     are labels, the rule is absent);
   - C2: the r88 counters with twelve always-passing arms appended (labels present, no
     assertion) → `C2=unmet mutants=7 killed=0 survivors=5 unattributed=2 unanchored=5
     arms=26,26`: the five refactored anchors stay absent and the two mutations that break
     another arm's assertion are refused as `unattributed`, not counted killed — the
     attribution rule doing its job on the forger.
3. **Checksum-canary negative control (C2)** — a synthetic subject whose `--selftest` exits 1
   without any declared-arm FAIL must read `unattributed`, never `killed`; the counter's own
   `--selftest` arm `canary_unattributed` asserts it, and the control receipt records the
   counter refusing a canary mutation.

## Scope, no-harm and out of scope

- Write scope: this lane repo only (`.ufo/waves/round-89/**`, `.ufo/waves/round-87/count-c2.py`,
  `.ufo/waves/round-88/count-c1.py`, `.ufo/waves/round-88/count-c2.py`, `SKILL.md` registry
  (append-only superseding row), `corpus/**`, `SCORECARD.md`, `LOG.md`). No fleet-root edit, no
  sibling lane, no domain source tree, no `MANIFEST.json`, no `.ufo/state/`.
- Detection and report only: no remediation, no host or fleet state change.
- **Out of scope this round, declared before data:** `Planned (round 89)` item 3 (the dated
  full-census snapshot for the r86 value channel) is **not claimed** — the round's two claims
  already discharge the two harms on the record, and a third axis (depth) would need a
  population and freeze this contract cannot honestly size. It is carried, not dropped.
  The r87 gate's remaining unarmed clauses (`c2-replay-compare-off`, `c2-supersede-*`,
  `c2-absent-*`, `c2-defeated-accounting`) and F3 hermeticity stay carried: the gate's selftest
  arm count is the C1 subject's pin, and arming them in the same landing would couple the two
  claims.
- Scratch root: `$HYAKU_SCRATCH/mori-r89/<seat>/`, `HYAKU_SCRATCH` default
  `/fast/scratch/hyaku`. Every seat deletes its tree before it yields; no committed tool may
  hardcode `/tmp`.
- Tooling: seats may install or upgrade tools that help the task — read
  `/home/vgpnk/.omp/agent/RULES.md` first (official channels, update-safety gate; record
  tool/version/channel/reason in the seat report). **All pacman transactions are PAUSED
  host-wide**: use `uv tool`, `npx`, or an official binary in `~/.local/bin`.
