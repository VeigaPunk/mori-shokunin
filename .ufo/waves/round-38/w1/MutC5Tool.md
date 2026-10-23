# MutC5Tool — conform `tool_resolve` mutation (scratch copy)

## Mutant

Applied conform's own declared `tool_resolve` mutation anchor (`.ufo/waves/round-38/conform.py:220-221`):
`return os.path.abspath(os.path.join(os.path.abspath(repo), path))` → `return path` in the
scratch copy of the C1 counter's `resolve_tool` (`count-c1.py:914-918`; anchor occurs once).
Scratch root: `.ufo/waves/round-38/scratch/MutC5Tool/`.

- Pristine inputs: `count-c1.pristine.py` (copy of `.ufo/waves/round-38/count-c1.py`),
  `count-c4.pristine.py` (copy of `.ufo/waves/round-38/count-c4.py`).
- Mutant: `count-c1.mut-tool_resolve.py`.

## Detector

Command (run from the lane root; lane counter and contract are read-only inputs):

```
python3 .ufo/waves/round-38/conform.py f725f3076972e6e70595b5ac8279be524a111ff8 \
  --counter .ufo/waves/round-38/scratch/MutC5Tool/count-c1.<variant>.py \
  --counter .ufo/waves/round-38/scratch/MutC5Tool/count-c4.pristine.py
```

Expected on the mutant: `tool_resolve` FAIL, the other five checks PASS, `CONFORM=unmet`, exit 1.

## Runs

- Pristine: exit `0`; all six PASS; `CONFORM=met` (`scratch/MutC5Tool/conform-baseline.txt`;
  `check tool_resolve PASS (exit=0 resolved=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-38/fixtures/summary-only.py)`).
- Mutated: exit `1`; exactly `tool_resolve` FAIL, all other five PASS; `CONFORM=unmet`
  (`scratch/MutC5Tool/conform-mutant.txt`):
  - `check predicate        PASS (exit=0 equal=True)`
  - `check head_pin         PASS (pin=f725f3076972e6e70595b5ac8279be524a111ff8 tip=f725f3076972e6e70595b5ac8279be524a111ff8)`
  - `check tool_resolve     FAIL (exit=0 resolved=.ufo/waves/round-38/fixtures/summary-only.py)`
  - `check bounded_reads    PASS (...)`
  - `check timeout_state    PASS (exit=1 timeout_reason=True pass=False)`
  - `check scratch          PASS (...)`
- Restored: exit `0`; all six PASS; `CONFORM=met` (`scratch/MutC5Tool/conform-restored.txt`).

## Hash and restoration evidence

- Before: `count-c1.py`, `count-c1.pristine.py`, `count-c1.mut-tool_resolve.py` all
  `9ebf10a117851c7451cf3ed7aaf5d6abe176ebffde2ae379ab5dffac50a5669e`;
  `count-c4.py` = `count-c4.pristine.py` =
  `3340d594123e4f983ddadc4759fd108438bd9b314dda17ab56690a08a7302403`.
- After the probe, `count-c1.mut-tool_resolve.py` was overwritten from the pristine copy:
  sha256 `9ebf10a117851c7451cf3ed7aaf5d6abe176ebffde2ae379ab5dffac50a5669e`,
  and `cmp -s` against the lane's `.ufo/waves/round-38/count-c1.py` exits `0` (byte-identical).
  No lane file was modified; all writes stayed under the scratch directory.

## Verdict

**KILLED — PASS (exactly the expected flip).** The mutant is detected only by `tool_resolve`
(`--print-tool` returns the repo-relative path, which the check rejects because it is not
absolute), and the pristine/restored bytes pass all six checks. No tool installs or upgrades
were needed. Runner: Python 3 from the host toolchain; no other runtime invoked.
