# MutC5Predicate — predicate-token mutant vs conform.py (C2/C5 probe)

Seat: MoriR38.MutC5Predicate (wave 2, falsify). Target: `count-c1.py`'s `--print-predicate` output versus the
contract P-C1 blockquote of record (`.ufo/waves/round-38/contract.md:114`), judged by the `predicate`
check of `.ufo/waves/round-38/conform.py:139-143` (`normalise(stdout) == contract_predicate(...)`;
`normalise` = whitespace-collapse + strip, `conform.py:77-78`).

Verdict: **KILLED** — the mutant flips exactly the `predicate` check to FAIL; all five sibling checks stay PASS.

## Mutant (one non-whitespace token, one byte-range)

Scratch copy of the lane counter, created fresh from
`.ufo/waves/round-38/count-c1.py` (sha256 `9ebf10a117851c7451cf3ed7aaf5d6abe176ebffde2ae379ab5dffac50a5669e`):

- pristine copy: `.ufo/waves/round-38/scratch/MutC5Predicate/count-c1-pristine.py`
- mutated copy: `.ufo/waves/round-38/scratch/MutC5Predicate/count-c1-predicate-mutant.py`
- mutant sha256: `fd4df9a9e284faab0f455753190e6322fc5aa65702fb878e38fcdb0ed0eef1f1`

```diff
--- count-c1-pristine.py
+++ count-c1-predicate-mutant.py
@@ -55,7 +55,7 @@
 PREDICATE = (
     "P-C1: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's "
     "hidden truth for ids, deleted, superseded and round_changed, and exactly the truth's "
-    "per-id `changed`/`deleted` lines, on each of 24 sandbox SOURCES.md histories drawn at "
+    "per-id `changed`/`deleted` lines, on each of 12 sandbox SOURCES.md histories drawn at "
     "run time, on the lane's own history (rev 6bd57097, round base f10a320d) where the "
     "independent oracle lists at least one id, and on one run-time-drawn challenge history "
     "presented in real-arm clothing (lane path, lane git identity, lane title); and the same "
```

Only `PREDICATE` changes; no executable path is touched (mutation is display-only, so no arm can
side-step the detector). Token chosen deliberately different from conform.py's own selftest anchor
(`head_at_measurement=<40-hex>.` → `lane_tip=<40-hex>.`, `conform.py:225-226`), so the kill is not a
replay of the harness self-test string. `24` matches the contract token at `contract.md:114`
("on each of 24 sandbox SOURCES.md histories").

## Expected detector

`python3 .ufo/waves/round-38/conform.py f725f3076972e6e70595b5ac8279be524a111ff8 --counter
<mutant> --counter .ufo/waves/round-38/count-c4.py` → exactly `check predicate FAIL`, `CONFORM=unmet`, exit 1.

## Baseline (control): pristine copy in the same scratch location

Command (copy at scratch, so module-path effects are controlled; `--counter` order puts the copy first, i.e.
conform's `first`, so head_pin/tool_resolve/timeout_state/bounded_reads all execute the copy):

```
python3 .ufo/waves/round-38/conform.py f725f3076972e6e70595b5ac8279be524a111ff8 \
  --counter .ufo/waves/round-38/scratch/MutC5Predicate/count-c1-pristine.py \
  --counter .ufo/waves/round-38/count-c4.py
```

```
check predicate        PASS (exit=0 equal=True)
check head_pin         PASS (pin=f725f3076972e6e70595b5ac8279be524a111ff8 tip=f725f3076972e6e70595b5ac8279be524a111ff8)
check tool_resolve     PASS (exit=0 resolved=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-38/fixtures/summary-only.py)
check bounded_reads    PASS (count-c1-pristine.py: run=True popen=True cap=True mkdtemp=True scratch=True; count-c4.py: run=True popen=True cap=True mkdtemp=True scratch=True)
check timeout_state    PASS (exit=1 timeout_reason=True pass=False)
check scratch          PASS (count-c1-pristine.py: mkdtemp_dir=True root=True; count-c4.py: mkdtemp_dir=True root=True)
CONFORM=met
EXIT=0
```

Baseline is clean, so a mutant FAIL is attributable to the mutation, not to copy placement.

## Mutated run (the assigned probe)

```
python3 .ufo/waves/round-38/conform.py f725f3076972e6e70595b5ac8279be524a111ff8 \
  --counter .ufo/waves/round-38/scratch/MutC5Predicate/count-c1-predicate-mutant.py \
  --counter .ufo/waves/round-38/count-c4.py
```

```
check predicate        FAIL (exit=0 equal=False)
check head_pin         PASS (pin=f725f3076972e6e70595b5ac8279be524a111ff8 tip=f725f3076972e6e70595b5ac8279be524a111ff8)
check tool_resolve     PASS (exit=0 resolved=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-38/fixtures/summary-only.py)
check bounded_reads    PASS (count-c1-predicate-mutant.py: run=True popen=True cap=True mkdtemp=True scratch=True; count-c4.py: run=True popen=True cap=True mkdtemp=True scratch=True)
check timeout_state    PASS (exit=1 timeout_reason=True pass=False)
check scratch          PASS (count-c1-predicate-mutant.py: mkdtemp_dir=True root=True; count-c4.py: mkdtemp_dir=True root=True)
CONFORM=unmet
EXIT=1
```

`predicate` line: `check predicate        FAIL (exit=0 equal=False)` — the counter still *printed* its
predicate successfully (`exit=0`), the inequality is in the bytes. Exactly one check flips; per
`conform.py:280` (`met = all(...)`) the aggregate `CONFORM=unmet` and exit 1 follow.

Direct probe pair (independent of conform.py), showing the differing token and that only that token differs:

```
python3 .../count-c1-predicate-mutant.py --print-predicate  -> MUT_EXIT=0
python3 .../count-c1-pristine.py --print-predicate          -> PRISTINE_EXIT=0
diff predicate-mutant.txt predicate-pristine.txt
1c1
< P-C1: ... on each of 12 sandbox SOURCES.md histories drawn at ...
---
> P-C1: ... on each of 24 sandbox SOURCES.md histories drawn at ...
DIFF_EXIT=1
```

## Restoration evidence

Mutated scratch file restored by overwriting with the pristine bytes (`cp count-c1-pristine.py
count-c1-predicate-mutant.py`), then re-verified:

```
9ebf10a117851c7451cf3ed7aaf5d6abe176ebffde2ae379ab5dffac50a5669e  count-c1-pristine.py
9ebf10a117851c7451cf3ed7aaf5d6abe176ebffde2ae379ab5dffac50a5669e  count-c1-predicate-mutant.py
```

Post-restore conform run on the same path:

```
check predicate        PASS (exit=0 equal=True)
check head_pin         PASS (pin=f725f3076972e6e70595b5ac8279be524a111ff8 tip=f725f3076972e6e70595b5ac8279be524a111ff8)
check tool_resolve     PASS (exit=0 resolved=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-38/fixtures/summary-only.py)
check bounded_reads    PASS (count-c1-predicate-mutant.py: run=True popen=True cap=True mkdtemp=True scratch=True; count-c4.py: run=True popen=True cap=True mkdtemp=True scratch=True)
check timeout_state    PASS (exit=1 timeout_reason=True pass=False)
check scratch          PASS (count-c1-predicate-mutant.py: mkdtemp_dir=True root=True; count-c4.py: mkdtemp_dir=True root=True)
CONFORM=met
EXIT=0
```

## Lane untouched

sha256 of the lane counters, before the probe and after restoration (identical):

```
9ebf10a117851c7451cf3ed7aaf5d6abe176ebffde2ae379ab5dffac50a5669e  .ufo/waves/round-38/count-c1.py
3340d594123e4f983ddadc4759fd108438bd9b314dda17ab56690a08a7302403  .ufo/waves/round-38/count-c4.py
6bbcd25854b7ff8448f11e385565a003f6b2c0e1902ccf68c874c01b4d4d8baa  .ufo/waves/round-38/conform.py
```

`git -C . status --porcelain -- .ufo/waves/round-38/count-c1.py .ufo/waves/round-38/count-c4.py
.ufo/waves/round-38/conform.py .ufo/waves/round-38/contract.md` printed no lines (all four clean
against the index). No lane file was written; no git/jj mutating command was run. Mutation work was
confined to `.ufo/waves/round-38/scratch/MutC5Predicate/`.

Note on pre-existing scratch content: `.ufo/waves/round-38/scratch/MutC5Predicate/` already contained
`pristine-copy.py` and `mutant-predicate.py` when this seat started (wave-1 leftovers; that mutant uses
the harness selftest token `lane_tip=<40-hex>.`). They were left untouched and not used as evidence;
all findings above come from `count-c1-pristine.py` / `count-c1-predicate-mutant.py` created and run in
this seat.

## Finding

The `predicate` check is behaviorally sensitive to a single non-whitespace token in `PREDICATE`
(`24`→`12`), and it is the only check that moves — the other five stay green on the same bytes, so the
mutant is killed precisely, not incidentally. [INFERENCE] Because both sides pass through
`normalise()` (`conform.py:77-78`), a whitespace-only difference in the printed predicate would survive
this check by construction; that is the check's declared normalisation, not a defect in this probe, and
it was not exercised here (out of the assigned probe).
