# MutC5Bounds — bounded_reads mutation probe (C2 / P-C5)

Seat: mutation-tester, mori round 38. Target revision `f725f3076972e6e70595b5ac8279be524a111ff8`
(`git rev-parse HEAD` printed this at probe start). Lane files read-only; all mutation work on
copies under `.ufo/waves/round-38/scratch/MutC5Bounds/probe/`.

## Mutant

`conform.py`'s declared `bounded_reads` mutation (`conform.py:222-224`), applied to a scratch copy
of `count-c1.py`: drop the caller-supplied `timeout=timeout` kwarg from the git helper's `run(`
call.

```diff
--- count-c1.pristine.py
+++ count-c1.mut.py
@@ -133,7 +133,7 @@
 def git(repo, *args, check=True, timeout=120):
-    proc = run(["git", "-C", repo] + list(args), timeout=timeout, env=clean_env())
+    proc = run(["git", "-C", repo] + list(args), env=clean_env())
```

One-line diff, no other byte changed. sha256 `9ebf10a117851c7451cf3ed7aaf5d6abe176ebffde2ae379ab5dffac50a5669e`
pristine → `e758e829cc4100c05e6ba6ca8e960147266d05ccf444d9574dc3773b5b5c0a8a` mutant. The mutated
line is byte-for-byte the anchor `conform.py`'s own selftest uses for this arm (`conform.py:222-224`,
"git helper run timeout removed").

## Expected detector

Static AST arm in `conform.py:110-111`: every `run(` Call node must carry a `timeout` keyword.
Dropping the kwarg sets `run=False` for the first counter, so `bounded_reads` (`conform.py:166-182`)
must FAIL and no other check should flip.

## Detector command (identical bytes run on pristine, mutant, restored)

```
python3 .ufo/waves/round-38/conform.py f725f3076972e6e70595b5ac8279be524a111ff8 \
  --counter .ufo/waves/round-38/scratch/MutC5Bounds/probe/count-c1.{pristine,mut}.py \
  --counter .ufo/waves/round-38/count-c4.py
```

## Output

Baseline, pristine copy — **CONFORM=met, exit 0** (`probe/baseline.out`, 3.37 s):

```
check predicate        PASS (exit=0 equal=True)
check head_pin         PASS (pin=f725f3076972e6e70595b5ac8279be524a111ff8 tip=f725f3076972e6e70595b5ac8279be524a111ff8)
check tool_resolve     PASS (exit=0 resolved=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-38/fixtures/summary-only.py)
check bounded_reads    PASS (count-c1.pristine.py: run=True popen=True cap=True mkdtemp=True scratch=True; count-c4.py: run=True popen=True cap=True mkdtemp=True scratch=True)
check timeout_state    PASS (exit=1 timeout_reason=True pass=False)
check scratch          PASS (count-c1.pristine.py: mkdtemp_dir=True root=True; count-c4.py: mkdtemp_dir=True root=True)
CONFORM=met
```

Mutant — **CONFORM=unmet, exit 1** (`probe/mutant.out`, 3.36 s):

```
check predicate        PASS (exit=0 equal=True)
check head_pin         PASS (pin=f725f3076972e6e70595b5ac8279be524a111ff8 tip=f725f3076972e6e70595b5ac8279be524a111ff8)
check tool_resolve     PASS (exit=0 resolved=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-38/fixtures/summary-only.py)
check bounded_reads    FAIL (count-c1.mut.py: run=False popen=True cap=True mkdtemp=True scratch=True; count-c4.py: run=True popen=True cap=True mkdtemp=True scratch=True)
check timeout_state    PASS (exit=1 timeout_reason=True pass=False)
check scratch          PASS (count-c1.mut.py: mkdtemp_dir=True root=True; count-c4.py: mkdtemp_dir=True root=True)
CONFORM=unmet
```

Exactly one check flipped — `bounded_reads`, and within it only `run=False` on the mutated counter
(`popen`, `cap`, `mkdtemp`, `scratch`, and the untouched `count-c4.py` row all stayed True). All five
other checks stayed PASS and `head_pin` still printed the real tip.

## Verdict

**KILLED by `bounded_reads` alone — acceptance PASS.** The single behavioural detector on the
declared mutation flipped exactly its own check, exit 0 → 1, and Console met → unmet.

Observation (no remediation, not a contract change): the mutant is behaviourally silent to
`timeout_state` because the helper's own default `timeout=120` still applies at the call site
(`count-c1.py:109`), and the tool path's bound lives at `count-c1.py:556`
(`timeout=_TOOL_BUDGET[0]`). Only the static call-site audit (`conform.py:110-111`) detects this
mutation. That matches P-C5's "bounds every child and git read by a timeout" as a call-site
property; noted as a coverage finding only.

## Restoration evidence

- `cp count-c1.pristine.py count-c1.mut.py`; `sha256sum` of restored `count-c1.mut.py` =
  `9ebf10a117851c7451cf3ed7aaf5d6abe176ebffde2ae379ab5dffac50a5669e` (equal to lane
  `.ufo/waves/round-38/count-c1.py`); `cmp` against the lane counter: byte-identical.
- Restored bytes re-run through the same detector: **CONFORM=met, exit 0**, all six PASS
  (`probe/restored.out`, 3.34 s).
- Lane untouched: `git status --porcelain -- .ufo/waves/round-38/{conform.py,count-c1.py,count-c4.py,contract.md}`
  printed nothing (exit 0); hashes unchanged all probe long: `conform.py`
  `6bbcd25854b7ff8448f11e385565a003f6b2c0e1902ccf68c874c01b4d4d8baa`, `count-c1.py`
  `9ebf10a1…669e`, `count-c4.py` `3340d594123e4f983ddadc4759fd108438bd9b314dda17ab56690a08a7302403`,
  `contract.md` `8cfeed27f0ce715089f18ff5cb20d18d211f2e31ed0f0aecf09105d79fb4eac9`.
- Witnesses: `scratch/MutC5Bounds/probe/{baseline.out,baseline.err,mutant.out,mutant.err,restored.out,mutation.diff}`.

## Tooling

No installs or upgrades were needed; no package manager was invoked. Evidence files are in the
seat scratch directory above; the only lane-relative file written by this seat is this report.
