# MutC5Pin — head_pin mutation probe (round 38, wave 2)

Verdict: **KILLED** — the mutant fails exactly the `head_pin` check and nothing else.

## Mutant

One line of `.ufo/waves/round-38/count-c1.py` (line 951), in the `--pin-only` branch:

```diff
--- pin-pristine.py
+++ pin-mutant.py
@@ -948,7 +948,7 @@
         return 0
     repo_abs = os.path.abspath(args.repo)
     if args.pin_only:
-        print("head_at_measurement=%s" % git_out(repo_abs, "rev-parse", "HEAD").strip())
+        print("head_at_measurement=%s" % "e33bb561712b32f46861362a3fa43762fa70ae4f")
         return 0
     if args.print_tool:
```

The mutant prints the entering tip `e33bb561712b32f46861362a3fa43762fa70ae4f` unconditionally,
never asking git for the measured HEAD; label and format tokens are untouched, so only the
pin *value* can trip a check. Diff artifact:
`.ufo/waves/round-38/scratch/MutC5Pin/w2/mutant.diff`.

## Detector (bounded, identical on pristine / mutant / restored)

```
python3 .ufo/waves/round-38/conform.py f725f3076972e6e70595b5ac8279be524a111ff8 \
  --counter <copy> --counter /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-38/count-c4.py
```

The pristine baseline uses a byte-identical copy of the lane counter
(`scratch/MutC5Pin/w2/pin-pristine.py`), so the only variable between runs is the one line above.

## Actual outputs

Baseline — `scratch/MutC5Pin/w2/conform-baseline.txt`, exit **0**:

```
check predicate        PASS (exit=0 equal=True)
check head_pin         PASS (pin=f725f3076972e6e70595b5ac8279be524a111ff8 tip=f725f3076972e6e70595b5ac8279be524a111ff8)
check tool_resolve     PASS (exit=0 resolved=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-38/fixtures/summary-only.py)
check bounded_reads    PASS (pin-pristine.py: run=True popen=True cap=True mkdtemp=True scratch=True; count-c4.py: run=True popen=True cap=True mkdtemp=True scratch=True)
check timeout_state    PASS (exit=1 timeout_reason=True pass=False)
check scratch          PASS (pin-pristine.py: mkdtemp_dir=True root=True; count-c4.py: mkdtemp_dir=True root=True)
CONFORM=met
```

Mutant — `scratch/MutC5Pin/w2/conform-mutant.txt`, exit **1**:

```
check predicate        PASS (exit=0 equal=True)
check head_pin         FAIL (pin=e33bb561712b32f46861362a3fa43762fa70ae4f tip=f725f3076972e6e70595b5ac8279be524a111ff8)
check tool_resolve     PASS (exit=0 resolved=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-38/fixtures/summary-only.py)
check bounded_reads    PASS (pin-mutant.py: run=True popen=True cap=True mkdtemp=True scratch=True; count-c4.py: run=True popen=True cap=True mkdtemp=True scratch=True)
check timeout_state    PASS (exit=1 timeout_reason=True pass=False)
check scratch          PASS (pin-mutant.py: mkdtemp_dir=True root=True; count-c4.py: mkdtemp_dir=True root=True)
CONFORM=unmet
```

Direct probe of the mutant, exit 0:
`head_at_measurement=e33bb561712b32f46861362a3fa43762fa70ae4f`
(lane `git rev-parse HEAD` = `f725f3076972e6e70595b5ac8279be524a111ff8`).

Independent replay from a second rebuilt mutant (`/tmp/pin-mutant-replay.py`, same one-line change,
exit **1**) reproduced it exactly: `head_pin FAIL (pin=e33bb56… tip=f725f30…)`,
`CONFORM=unmet`, all other five checks PASS.

Flipped checks: `{head_pin}` — exactly one. No collateral from removing the git read: `bounded_reads`
and `scratch` are AST checks over the rest of the source and stay PASS; `timeout_state` exits 1 with
`tool_timeout` and no `real arm: pass`; `predicate` still prints the contract bullets verbatim.

## Restoration evidence

- Mutated bytes: `pin-mutant.py` sha256 `30036609…e958f7`-class copy mutated in place; after restore
  `9ebf10a117851c7451cf3ed7aaf5d6abe176ebffde2ae379ab5dffac50a5669e`.
- `pin-pristine.py` = `9ebf10a117851c7451cf3ed7aaf5d6abe176ebffde2ae379ab5dffac50a5669e`
- `pin-mutant.py` after restore = `9ebf10a117851c7451cf3ed7aaf5d6abe176ebffde2ae379ab5dffac50a5669e`
- lane `.ufo/waves/round-38/count-c1.py` = `9ebf10a117851c7451cf3ed7aaf5d6abe176ebffde2ae379ab5dffac50a5669e` (byte-identical)
- Restored copy re-probed: `head_at_measurement=f725f3076972e6e70595b5ac8279be524a111ff8`, exit 0;
  detector re-run `CONFORM=met`, exit 0 (`scratch/MutC5Pin/w2/conform-restored.txt`).

## Lane counters untouched

Before and after, identical hashes:
- `.ufo/waves/round-38/count-c1.py` `9ebf10a117851c7451cf3ed7aaf5d6abe176ebffde2ae379ab5dffac50a5669e`
- `.ufo/waves/round-38/count-c4.py` `3340d594123e4f983ddadc4759fd108438bd9b314dda17ab56690a08a7302403`
- `.ufo/waves/round-38/conform.py` `6bbcd25854b7ff8448f11e385565a003f6b2c0e1902ccf68c874c01b4d4d8baa`

`git status --porcelain -- .ufo/waves/round-38/{count-c1.py,count-c4.py,conform.py}` prints nothing.
All mutation work happened under `.ufo/waves/round-38/scratch/MutC5Pin/w2/`; only the report and that
scratch subtree were written.

## Note on prior scratch contents

`scratch/MutC5Pin/` already held a wave-1 seat's files (`count-c1.head_pin.py`, a **label-rename**
mutation `head_at_measurement=%s` → `head=%s`, i.e. conform.py's own selftest mutation — a different
mutant from this probe). It was left in place; this seat worked in the `w2/` subdirectory and did not
read wave-1 conclusions as evidence — the kill above was re-derived by running the detector.

Tooling directive: no installs or upgrades performed.
