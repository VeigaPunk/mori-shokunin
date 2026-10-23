# MutC5Scratch — C5 `scratch` check, single-call `dir=` removal

Seat: `MoriR38.MutC5Scratch` (wave 2, falsify). Lane tip `f725f3076972e6e70595b5ac8279be524a111ff8`
(`git rev-parse HEAD`, run at 2026-10-23 ~20:0x). No tool installs or upgrades were needed.

## Mutant (one edit, one call site)

Target: `.ufo/waves/round-38/count-c1.py:983` (`tool_dir = tempfile.mkdtemp(...)`).
Mutation applied to a scratch copy only (`.ufo/waves/round-38/scratch/MutC5Scratch/mutant.py`):
`dir=_scratch_parent()` deleted, so the tool staging directory is created in the system temp
root (`tempfile.mkdtemp` default) instead of under the lane's `round-38/scratch` parent.

```
--- pristine.py
+++ mutant.py
@@ -980,7 +980,7 @@
             return 2
         fixtures.append((name, path))
 
-    tool_dir = tempfile.mkdtemp(prefix="mori-c1-tool-", dir=_scratch_parent())
+    tool_dir = tempfile.mkdtemp(prefix="mori-c1-tool-")
     try:
         if args.tool:
```

11-line unified diff, one hunk, one line changed; scratch copy still parses (`ast.parse`).
Call-site count unchanged (6 `tempfile.mkdtemp(` calls in both pristine and mutant; only the
`dir` keyword of line 983 is gone).

## Detector (same on pristine, mutant, restored)

Counter under test is first `--counter`; the lane's `count-c4.py` is the second, unchanged
counter. Command, run from the lane root:

```
python3 .ufo/waves/round-38/conform.py f725f3076972e6e70595b5ac8279be524a111ff8 \
  --counter .ufo/waves/round-38/scratch/MutC5Scratch/<copy>.py \
  --counter .ufo/waves/round-38/count-c4.py
```

Why the check should catch it: `static_checks` ANDs `"dir" in kw` across every
`tempfile.mkdtemp(` call (`conform.py:116-117`), and `scratch` ANDs that `mkdtemp_ok` across all
counters plus the literal `SCRATCH_ROOT` parts (`conform.py:193-209`), so dropping the keyword on
any one call must flip `scratch` to FAIL while leaving the other five checks PASS.

## Actual results

| bytes | `scratch` check | `CONFORM=` | exit | evidence |
|---|---|---|---|---|
| pristine copy (byte-identical to lane) | PASS (`pristine.py: mkdtemp_dir=True root=True; count-c4.py: mkdtemp_dir=True root=True`) | `CONFORM=met` | 0 | `scratch/MutC5Scratch/baseline-pristine.txt` |
| lane `count-c1.py` (canonical command) | PASS (`count-c1.py: mkdtemp_dir=True root=True; count-c4.py: mkdtemp_dir=True root=True`) | `CONFORM=met` | 0 | `scratch/MutC5Scratch/baseline-lane.txt` |
| **mutant** | **FAIL (`mutant.py: mkdtemp_dir=False root=True; count-c4.py: mkdtemp_dir=True root=True`)** | **`CONFORM=unmet`** | **1** | `scratch/MutC5Scratch/mutant-run.txt` |
| restored copy (pristine bytes) | PASS (`restored.py: mkdtemp_dir=True root=True; count-c4.py: mkdtemp_dir=True root=True`) | `CONFORM=met` | 0 | `scratch/MutC5Scratch/restored-run.txt` |

Full mutant run (verbatim, from `mutant-run.txt`):

```
check predicate        PASS (exit=0 equal=True)
check head_pin         PASS (pin=f725f3076972e6e70595b5ac8279be524a111ff8 tip=f725f3076972e6e70595b5ac8279be524a111ff8)
check tool_resolve     PASS (exit=0 resolved=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-38/fixtures/summary-only.py)
check bounded_reads    PASS (mutant.py: run=True popen=True cap=True mkdtemp=False scratch=True; count-c4.py: run=True popen=True cap=True mkdtemp=True scratch=True)
check timeout_state    PASS (exit=1 timeout_reason=True pass=False)
check scratch          FAIL (mutant.py: mkdtemp_dir=False root=True; count-c4.py: mkdtemp_dir=True root=True)
CONFORM=unmet
EXIT=1
```

Baseline was a genuine PASS, not a vacuous one: `predicate`, `head_pin`, `tool_resolve`,
`bounded_reads`, `timeout_state` all PASS on the pristine copy with the pin equal to the tip.

Two process notes, so neither is misread as a finding:
- An earlier copy-path invocation used a doubled prefix (`.ufo/waves/round-38/.ufo/waves/...`) and
  produced `unreadable` for both counters → `CONFORM=unmet`. That run was discarded as an
  inconclusive setup error and overwritten by `baseline-pristine.txt`; it was never evidence.
- In the mutant run `bounded_reads` still shows `mkdtemp=False` yet PASSes. That is by design:
  `bounded_reads` scores only `run_ok and popen_ok` plus the blob cap for the first counter
  (`conform.py:175-178`); `mkdtemp_ok` belongs solely to `scratch`. The flips do not leak.

## Verdict

**KILLED.** Only `scratch` flips to FAIL; exit code moves 0 → 1 and `CONFORM=met` → `CONFORM=unmet`.
The C5 `scratch` check is sensitive to removing `dir=` from a single `mkdtemp` call even when the
runtime path is otherwise healthy (the mutant still passes predicate/head_pin/tool_resolve/
timeout_state, so this is check sensitivity, not collateral breakage).

## Restoration evidence

- Mutant saved before restore: `scratch/MutC5Scratch/mutant-kept.py`,
  sha256 `2fe2395039f793f660890c08e58f7d5553d839f3832ee560f69e8b96666eeaff`.
- `mutant.py` was then overwritten from pristine bytes; post-restore hashes are identical:

```
9ebf10a117851c7451cf3ed7aaf5d6abe176ebffde2ae379ab5dffac50a5669e  pristine.py
9ebf10a117851c7451cf3ed7aaf5d6abe176ebffde2ae379ab5dffac50a5669e  mutant.py
9ebf10a117851c7451cf3ed7aaf5d6abe176ebffde2ae379ab5dffac50a5669e  restored.py
2fe2395039f793f660890c08e58f7d5553d839f3832ee560f69e8b96666eeaff  mutant-kept.py
```

Verbatim `sha256sum` output after restoration (`hashes-after-restore.txt`); `cmp` confirms
`mutant.py == pristine.py` and `pristine.py == ../../count-c1.py` (the lane file). The restored
`mutant.py` is byte-identical to the pristine and lane bytes
(`9ebf10a117851c7451cf3ed7aaf5d6abe176ebffde2ae379ab5dffac50a5669e`).

- Restored bytes re-ran the detector: `CONFORM=met`, `EXIT=0` (`restored-run.txt`).

## Lane counters untouched

- Hashes equal before and after the probe:
  - `.ufo/waves/round-38/count-c1.py` = `9ebf10a117851c7451cf3ed7aaf5d6abe176ebffde2ae379ab5dffac50a5669e`
  - `.ufo/waves/round-38/count-c4.py` = `3340d594123e4f983ddadc4759fd108438bd9b314dda17ab56690a08a7302403`
  - `.ufo/waves/round-38/conform.py` = `6bbcd25854b7ff8448f11e385565a003f6b2c0e1902ccf68c874c01b4d4d8baa`
- `git -C <lane> diff --quiet -- <those three files>` → exit 0; `git status --porcelain` restricted
  to them → empty. HEAD stayed `f725f3076972e6e70595b5ac8279be524a111ff8`, and
  `git cat-file -p f725f30:.ufo/waves/round-38/count-c1.py | sha256sum` equals the working-tree hash
  above, so the measured file is the tip blob.
- All mutation work lived in `.ufo/waves/round-38/scratch/MutC5Scratch/`. Two files there predate
  this seat (`count-c1-pristine.py`, `count-c1-scratch-mut.py`, mtime 19:54) and were not created
  or modified by me; I left them untouched.

## Coverage note (not executed — assigned probe only)

`mkdtemp_ok` is purely syntactic: it asks whether a `dir` keyword is present
(`conform.py:116-117`) and `scratch_root_ok` greps the literal `SCRATCH_ROOT` assignment
(`conform.py:119-125`). Neither constrains the *value* passed to `dir`. [INFERENCE] A variant that
keeps `dir=` but points it at the system temp (`dir="/tmp"`, or a `_scratch_parent()` that returns
`"/tmp"`) would therefore plausibly survive `scratch` while still creating directories off-lane —
untested here, since this seat's assignment is the single `dir=`-removal probe. Reporting only; no
remediation proposed.
