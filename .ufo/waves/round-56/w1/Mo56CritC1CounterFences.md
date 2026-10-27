# Seat Mo56CritC1CounterFences — round 56 wave w1

Task: attempt to make `.ufo/waves/round-56/count-c1.py` print `C1=met` at a
revision where the probe `tools/mori-driver-liveness.py` is subtly broken, via
three constructions: (1) hardcoded fixture outputs, (2) selftest that skips
when fixtures are missing, (3) a health-verdict word in a Unicode lookalike.
Scratch fixture repo + `--repo`; frozen counter untouched.

Axes used: kill (does the frozen counter print unmet?), bypass (do the
functional arms alone detect the breakage?), reachability (is any bypass
reachable under the frozen pin?), noise (did the attack disturb the recorded
at-freeze verdict?).

## Method

- Scratch fixture repo `/fast/scratch/hyaku/mori-r56/Mo56CritC1CounterFences/fix`
  built with `git archive` from lane rev `8be2717b…` for
  `tools/mori-driver-liveness.py`, `corpus/knowledge/driver-liveness-r56.md`,
  `corpus/SOURCES.md`, and `.ufo/waves/round-56/fixtures/driver/`; identity set
  locally in the fixture only; `git rev-parse --show-toplevel` asserted equal
  to the fixture dir before each commit (lane repo never mutated; read-only git
  only there).
- Isolation runs re-point `PIN` inside *scratch copies* of the counter
  (`cc-c1.py`, `cc-c2.py`, `cc-c3a.py`, `cc-c3b.py`) to the mutated tool sha.
  This is a fence-sensitivity probe only; it is not a proposal to change the
  frozen counter (counters are immutable this round).
- `TMPDIR=/fast/scratch/hyaku/mori-r56/Mo56CritC1CounterFences/tmp` for all runs.

## Baseline (reproduced)

```
$ sha256sum tool-real.py   # git show 8be2717b:tools/mori-driver-liveness.py
6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997  tool-real.py
$ python3 .ufo/waves/round-56/count-c1.py 8be2717b0809281d07dffe83dad424a4859e0747
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=8be2717b0809281d07dffe83dad424a4859e0747   exit=0
$ python3 .ufo/waves/round-56/count-c1.py 5b295eeebd87ebd610d8d39bfe2035742f740cfa --repo <lane>
C1=unmet selftest=bad fixtures=bad entry=bad row=bad norem=bad failed=tool_absent rev=5b295eeebd87ebd610d8d39bfe2035742f740cfa   exit=1
```

Benign harness sanity: the same freeze content committed in the scratch repo
(rev `74b531b6aad0c57c92b4c51cbd56ca01d7d8140e`) also prints
`C1=met … exit=0` under `--repo`, so counter behaviour over the fixture repo
matches behaviour over the lane repo.

## Construction 1 — probe hardcodes fixture outputs

Mutated tool sha `ff8ae40048ff96442dc7f5b61a54691b11bf69e8a048a97c91762950ccc9e6fb`:
prints the frozen selftest line, and for `--fixture` never opens the log —
it prints a hardcoded JSON table with exactly the counter's `EXPECT_FIX`
counts (`.ufo/waves/round-56/count-c1.py:40-44`). Fixture commit `4f8a8e7…`,
combined-with-garbage commit `21bbf8c6c54f9020f78f504ec85e4096428490b1`
(malformed fixture replaced by five garbage lines).

Frozen counter:

```
$ python3 count-c1.py 4f8a8e79971ff49b5e0a3ab1d8b62b0dfc7be62a --repo fix
C1=unmet selftest=ok fixtures=ok entry=ok row=ok norem=ok … failed=pins   exit=1
```

KILLED by the pin arm; note `selftest=ok fixtures=ok norem=ok` — the functional
arms pass the hardcoded probe.

Isolation (scratch copy, PIN = mutated sha):

```
cc-c1.py @ 4f8a8e7  (intact fixtures)          → C1=met … exit=0   BYPASSED
cc-c1.py @ 21bbf8c6 (malformed fixture = garbage) → C1=met … exit=0   BYPASSED
```

The fixture arm reports `fixtures=ok` even with a garbage log: the hardcoded
tool never reads it. Control: the real tool at the garbage-fixture commit
(`8599236ab4f5bbc246347a6eed9538163fb3fe11`, sha mismatched by design, real
behaviour) trips `selftest=bad` — the real selftest is fixture-content
sensitive, but a probe that prints the frozen lines has no such sensitivity.

## Construction 2 — selftest skips when fixtures are missing

Mutated tool sha `8f9952194dfc89bcf2836d4bdbd1b6beba22328eac457eeddb64d949671d496b`:
if `.ufo/waves/round-56/fixtures/driver` is absent under the repo root it
prints `DRIVER_LIVENESS_SELFTEST pass=0 fail=0 skipped=13` and exits 0; with
fixtures present it prints the frozen pass line. Commit `cb4cf7aa612ee52f1ead434f55c14def0ad4c3cf`.

Frozen counter:

```
$ python3 count-c1.py cb4cf7aa612ee52f1ead434f55c14def0ad4c3cf --repo fix
C1=unmet selftest=ok fixtures=ok entry=ok row=ok norem=ok … failed=pins   exit=1
```

KILLED by the pin arm.

Skip branch is real (direct run, no fixtures present):

```
$ python3 tools/mori-driver-liveness.py --selftest   # in $S/nofix (no .ufo tree)
DRIVER_LIVENESS_SELFTEST pass=0 fail=0 skipped=13   exit=0
```

Isolation:

```
cc-c2.py @ cb4cf7a → C1=met … exit=0   BYPASSED
```

Structural cause: `evaluate()` materializes the fixture tree
(`count-c1.py:127`) *before* the selftest arm runs, so under this counter the
selftest always sees fixtures present; the skip path is unobservable to the
counter. The skip line it would print (`skipped=13`) is not the frozen
`EXPECT_SELFTEST`, but the counter can never reach that branch.

## Construction 3 — health-verdict word in a Unicode lookalike

Variant 3a: `# heаlthy` with Cyrillic а (U+0430) inserted into the tool
*before* the first `# selftest` marker (marker at tool line 248).
Mutated sha `e22fbcf026b808ee5d5a5c680298513a9c8aa82b63b4c4872be3d26c245aa851`,
commit `300342d592ff7bce0c83edb0ed5b1d44a4d563e0`.

Variant 3b: plain ASCII `# wedged` appended *after* the marker (tool end).
Mutated sha `0bdf97717c726369b7546a60a8e6ef78cfd135202b3195dc90bc53661483952f`,
commit `a1d05c5137f647b3db4c4e66f3ca15529d23383e`.

Frozen counter, both variants:

```
$ python3 count-c1.py 300342d592ff7bce0c83edb0ed5b1d44a4d563e0 --repo fix
C1=unmet selftest=ok fixtures=ok entry=ok row=ok norem=ok … failed=pins   exit=1
$ python3 count-c1.py a1d05c5137f647b3db4c4e66f3ca15529d23383e --repo fix
C1=unmet selftest=ok fixtures=ok entry=ok row=ok norem=ok … failed=pins   exit=1
```

KILLED by the pin arm; `norem=ok` in both — the health-word arm did not fire.

Isolation:

```
cc-c3a.py @ 300342d → C1=met … exit=0   BYPASSED (norem defeated by confusable)
cc-c3b.py @ a1d05c5 → C1=met … exit=0   BYPASSED (norem defeated by placement)
```

The norem scan (`count-c1.py:162`) is `tool_src.split("# selftest", 1)[0].lower()`
with a case-folded ASCII substring test against `HEALTH_WORDS`
(`count-c1.py:45`). Two gaps, both demonstrated:

- Confusable gap: `heаlthy` (U+0430) does not match `healthy` byte-wise, so a
  lookalike verdict word before the marker passes the arm.
- Marker gap: only the head before the *first* `# selftest` occurrence is
  scanned. The gap is live in the shipped artifact: the frozen tool itself
  contains the ASCII word `healthy` at tool line 422 (inside its own
  `t_no_health_verdict`) — after the sole `# selftest` marker at line 248 —
  and passes norem only because the split discards that tail:

```
real-tool head (pre-marker) health words: []
real-tool contains ASCII "healthy" post-marker: True
first marker occurrence count: 1
```

## Counterexample analysis

Strongest local counterexample: a revision whose tool is any of the four
mutated probes *and* whose pin equals that probe's sha prints `C1=met` at a
semantically broken probe — all four isolation runs above. The frozen counter
detects byte drift from the pinned tool (`count-c1.py:122`), not semantic
breakage: the functional arms pass a probe that (a) never reads the log,
(b) skips its selftest whenever fixtures are absent, and (c) carries a
health-verdict word in a lookalike or below the scan marker.

Reachability under this round's freeze: none. The pin is non-empty, frozen,
checked first, and the counter is immutable after scoring; every construction
printed `C1=unmet … failed=pins`, exit 1 at the frozen counter, and the
recorded at-freeze and do-nothing receipts reproduce exactly. C1's verdict is
not disturbed (axis noise: none). The byte-pin is therefore the sole
load-bearing fence of the three attack classes — a defense-in-depth
observation, not a reachable defect this round.

## Routed items for round 57 (named limits; no counter change proposed here)

- N1 (norem marker gap): the health-word scan covers only the pre-`# selftest`
  head; words in the selftest/main section are invisible. Live in the frozen
  tool (line 422). Whole-file scan would close it.
- N2 (norem confusable gap): case-folded ASCII substring matching admits
  Unicode lookalikes (demonstrated with U+0430). NFKC/confusable folding would
  close it.
- N3 (skip unobservability): the selftest arm always runs with fixtures
  materialized, so skip-when-missing selftests are structurally invisible;
  running the selftest once without materialized fixtures would close it.
- N4 (fixture arm has no content-perturbation control): a probe printing the
  frozen counts passes even over a garbage log (`malformed=5` matched by five
  garbage lines in iso1b by construction of the hardcoded table). A perturbed
  fixture whose expected count differs from the frozen table would force the
  tool to actually parse.
- N5 (pin truthiness footgun): `if PIN and sha(tool_src) != PIN`
  (`count-c1.py:122`) silently disables pin enforcement for a falsy PIN; fine
  for the frozen non-empty pin, but any future counter variant that ships with
  an empty/None pin loses the only fence that killed all four constructions.
- N6 (counter selftest thinness): `--selftest` checks only the EXPECT_FIX table
  shape, not the pin/scan logic; the bypasses above pass it.

## Environment notes

- No tools installed or upgraded this seat. No pacman (host-wide pause
  respected). No network use. Disk guard checked before runs: `/fast/scratch`
  28% used, 581.4G free. All artifacts under
  `/fast/scratch/hyaku/mori-r56/Mo56CritC1CounterFences/` removed on completion.
- Fixture repo identity: local `Mo56CritC1CounterFences-fixture
  <mo56critc1@fixture.local>`, used only inside the scratch fixture.
- No host mutation: reads of `/proc`/`/sys` not needed beyond the disk-guard
  status; no journalctl counting.

## Findings

- LOW — Functional arms alone pass all three broken-probe classes; the frozen
  tool-pin is the sole load-bearing fence (constructions 1–3 all
  `C1=unmet failed=pins` at the frozen counter, all `C1=met` with the pin
  re-pointed). Not reachable under the frozen pin; defense-in-depth note.
  Concerns `count-c1.py:122` (pin check) vs the selftest/fixture/norem arms.
- LOW — norem marker gap: scan limited to the pre-`# selftest` head
  (`count-c1.py:162`); the frozen tool itself carries ASCII `healthy` after
  the marker (tool line 422) and passes only by virtue of the split.
- LOW — norem confusable gap: case-folded ASCII substring test
  (`count-c1.py:45,162`); Cyrillic `heаlthy` (U+0430) demonstrated to pass.
- LOW — skip-when-missing selftest structurally unobservable: fixtures are
  materialized before the selftest arm (`count-c1.py:127` vs the selftest arm);
  skip branch prints `pass=0 fail=0 skipped=13`, exit 0, when run directly.
- LOW — fixture arm has no content-perturbation control (`count-c1.py:96-102`
  region): hardcoded counts pass even over a garbage watchdog.log.
- LOW — pin truthiness footgun: `if PIN and …` (`count-c1.py:122`) disables
  pin enforcement for a falsy PIN; a future empty-pin counter variant would
  lose the only fence that killed every construction here.

No HIGH or MED finding against the frozen counter: the C1=met verdict at the
freeze tip and the tool_absent do-nothing at the entering tip both reproduce,
and all four attack revisions print unmet at the frozen counter.
