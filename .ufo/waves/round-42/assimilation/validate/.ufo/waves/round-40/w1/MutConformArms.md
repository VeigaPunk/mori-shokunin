# MutConformArms (agent MutConformArms-2) — mutation probe: conform v3 conditional-rebind arm

Role: mutation-tester. Read-only against production bytes; mutant and receipts live under
`.ufo/waves/round-40/scratch/mutconform-arms2/` only. No production file was edited.
No tooling installed.

## Assignment

Mutation-test conform v3: in a copy, neuter the conditional-rebind arm of `timeout_scope`
(treat conditional as unconditional) and run `--selftest` — the `timeout_scope` arm must still
fail but the cond survivor after-receipt must flip to met; report both outputs.

Detectors of record (same bounded invocation on pristine and mutant bytes):

- D1: `python3 <conform> 265a955cc67be4eae97d2dc5a9338a25f31eb29b --selftest`
- D2: `python3 <conform> 265a955cc67be4eae97d2dc5a9338a25f31eb29b --counter .ufo/waves/round-40/fixtures/generated/survivor-cond.py`
  (the cond survivor after-receipt of record: `evidence/c10-after-cond.txt`, `CONFORM=unmet`, only `timeout_scope` FAIL)

## Mutant

Copy of the frozen conform v3 (sha256 `5025b966…b83aaf`, identical to `freeze-r40.txt:9`) with
exactly one line changed in `_resolve_timeout_name`:

```diff
--- conform-pristine.py
+++ conform-mut-cond-unconditional.py
@@ -288,7 +288,7 @@
         params = func_params.get(fn.name, {})
         if name in params and params[name] is not None:
             return _resolve_value(params[name])
-    if name in conditional:
+    if False and name in conditional:
         base = None
         if name in unconditional:
             base = _resolve_value(unconditional[name][-1])
```

Effect: the conditional-rebind fail-closed block is unreachable; a name that has an
unconditional binding plus a conditional rebind resolves only to its unconditional value
(`survivor-cond.py` `NAME = 120` / conditional `NAME = None` resolves to 120 instead of raising
`Unresolvable`). No other line differs (`diff -u` above is the complete diff; `DIFF_EXIT=1`).

## Hashes (before/after the probe)

```
5025b9664632d01063c11b4f5dadd4f9a063db66d73315d7ed25db8d90b83aaf  .ufo/waves/round-40/conform.py
5025b9664632d01063c11b4f5dadd4f9a063db66d73315d7ed25db8d90b83aaf  .ufo/waves/round-40/scratch/mutconform-arms2/conform-pristine.py
5c400fa33c8715d60a4eb54a4305537a451f70cc48001b4be02dbaa7b2aa162e  .ufo/waves/round-40/scratch/mutconform-arms2/conform-mut-cond-unconditional.py
```

The production file hash is unchanged before and after the entire probe (same digest in the
freeze and in this run); restoration was unnecessary because the original was never mutated.

## D1 — `--selftest` on pristine bytes (baseline)

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ python3 .ufo/waves/round-40/scratch/mutconform-arms2/conform-pristine.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --selftest
PASS predicate          predicate token changed -> only predicate failed
PASS head_pin           pin label renamed -> only head_pin failed
PASS tool_resolve       relative resolution removed -> only tool_resolve failed
PASS bounded_reads      git helper run timeout removed -> only bounded_reads failed
PASS timeout_scope      timeout value replaced with None -> only timeout_scope failed
PASS timeout_scope_shadow function-local None shadow inserted -> only timeout_scope failed
PASS drain_bind         communicate drains replaced by wait+read -> only drain_bind failed
PASS drain_bind_decoy   decoy used communicate beside a wait+read drain -> only drain_bind failed
PASS timeout_state      budget flag ignored -> only timeout_state failed
PASS scratch            scratch parent moved off-lane -> only scratch failed
PASS selftest_conjunct  communicate timeout keyword stripped -> only selftest_conjunct failed
CONFORM_SELFTEST pass=11 fail=0
EXIT=0
wall: real 0m57.299s
```

Matches the landed receipt `evidence/c10-after-selftest.txt` (pass=11 fail=0, exit 0).

## D1 — `--selftest` on mutant bytes

```
$ python3 .ufo/waves/round-40/scratch/mutconform-arms2/conform-mut-cond-unconditional.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --selftest
PASS predicate          predicate token changed -> only predicate failed
PASS head_pin           pin label renamed -> only head_pin failed
PASS tool_resolve       relative resolution removed -> only tool_resolve failed
PASS bounded_reads      git helper run timeout removed -> only bounded_reads failed
PASS timeout_scope      timeout value replaced with None -> only timeout_scope failed
PASS timeout_scope_shadow function-local None shadow inserted -> only timeout_scope failed
PASS drain_bind         communicate drains replaced by wait+read -> only drain_bind failed
PASS drain_bind_decoy   decoy used communicate beside a wait+read drain -> only drain_bind failed
PASS timeout_state      budget flag ignored -> only timeout_state failed
PASS scratch            scratch parent moved off-lane -> only scratch failed
PASS selftest_conjunct  communicate timeout keyword stripped -> only selftest_conjunct failed
CONFORM_SELFTEST pass=11 fail=0
EXIT=0
wall: real 0m57.283s
```

Required observation holds: the `timeout_scope` arm still fails its own mutation
(`GIT_TIMEOUT_S = None` → only `timeout_scope` failed), and the `timeout_scope_shadow` arm is
untouched. The mutant is **not detected** by the selftest: 11/11 PASS, byte-identical arm lines
to the baseline.

## D2 — cond survivor on pristine bytes (baseline)

```
$ python3 .ufo/waves/round-40/scratch/mutconform-arms2/conform-pristine.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b \
    --counter .ufo/waves/round-40/fixtures/generated/survivor-cond.py
check predicate          PASS (exit=0 equal=True)
check head_pin           PASS (pin=ede486b7a09afbacfb380d5871c46a8051a6dc2e tip=ede486b7a09afbacfb380d5871c46a8051a6dc2e)
check tool_resolve       PASS (exit=0 resolved=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-39/fixtures/witness-summary-only-live.txt)
check bounded_reads      PASS (survivor-cond.py: bounded=[] value=['line 116 (communicate): non-numeric constant'])
check timeout_scope      FAIL (survivor-cond.py: bounded=[] value=['line 116 (communicate): non-numeric constant'])
check drain_bind         PASS (survivor-cond.py: violations=[])
check timeout_state      PASS (exit=1 timeout_reason=True pass=False)
check scratch            PASS (survivor-cond.py: mkdtemp_dir=True root=True)
check selftest_conjunct  PASS (survivor-cond.py: honest_comm=[] strips=6 detected=6 anchor=True entry_live=True)
CONFORM=unmet
EXIT=1
```

Same verdict and same `timeout_scope` detail as `evidence/c10-after-cond.txt` (`CONFORM=unmet`,
exit 1, `value=['line 116 (communicate): non-numeric constant']`). The only line that differs
from the committed receipt is `head_pin`, because the lane HEAD at probe time is
`ede486b7a09afbacfb380d5871c46a8051a6dc2e` (wave commits landed after the scored tip); the
counter pins whatever HEAD it measures, so the check still passes. No other line differs.

## D2 — cond survivor on mutant bytes

```
$ python3 .ufo/waves/round-40/scratch/mutconform-arms2/conform-mut-cond-unconditional.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b \
    --counter .ufo/waves/round-40/fixtures/generated/survivor-cond.py
check predicate          PASS (exit=0 equal=True)
check head_pin           PASS (pin=ede486b7a09afbacfb380d5871c46a8051a6dc2e tip=ede486b7a09afbacfb380d5871c46a8051a6dc2e)
check tool_resolve       PASS (exit=0 resolved=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-39/fixtures/witness-summary-only-live.txt)
check bounded_reads      PASS (survivor-cond.py: bounded=[] value=[])
check timeout_scope      PASS (survivor-cond.py: bounded=[] value=[])
check drain_bind         PASS (survivor-cond.py: violations=[])
check timeout_state      PASS (exit=1 timeout_reason=True pass=False)
check scratch            PASS (survivor-cond.py: mkdtemp_dir=True root=True)
check selftest_conjunct  PASS (survivor-cond.py: honest_comm=[] strips=6 detected=6 anchor=True entry_live=True)
CONFORM=met
EXIT=0
```

The cond survivor after-receipt flips `CONFORM=unmet` → `CONFORM=met` (exit 1 → 0), and only
`timeout_scope` changed state (`value=['line 116 …']` → `value=[]`). This is exactly the
assigned discriminator.

## Honest-counter control (no false negative introduced elsewhere)

```
$ python3 .ufo/waves/round-40/scratch/mutconform-arms2/conform-mut-cond-unconditional.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b
...
check timeout_scope      PASS (count-c8.py: bounded=[] value=[])
...
CONFORM=met
EXIT=0
```

Pristine bytes on the same counter also print `CONFORM=met`. The mutant is a false-negative on
the conditional-rebind survivor only.

## Verdict

| Detector | Pristine | Mutant | Verdict |
|---|---|---|---|
| D1 `--selftest` (11 arms) | pass=11 fail=0 / exit 0 | pass=11 fail=0 / exit 0 | **SURVIVED** |
| D2 cond survivor receipt | `CONFORM=unmet` / exit 1 | `CONFORM=met` / exit 0 | **KILLED** |

- The mutant is killed by the cond survivor after-receipt: the `timeout_scope` conditional-rebind
  arm is load-bearing for P-C10's survivor claim.
- The mutant survives `--selftest`: the checker's own eleven-mutation table contains no
  conditional-rebind mutation (only `timeout_scope` = `GIT_TIMEOUT_S = None` and
  `timeout_scope_shadow` = function-local shadow). Coverage finding: `--selftest` alone cannot
  distinguish v3 from a checker with the conditional fail-closed rule removed; only the
  `survivor-cond.py` receipt does. This is a coverage observation, not a contract change request.

## Notes / exactness

- `--selftest` requires the positional revision: invoking it without one fails before any arm
  runs (`conformance setup error: expected str, bytes or os.PathLike object, not NoneType`,
  exit 2 — `evaluate` forwards `rev=None` to the counter's `timeout_state` run). The claimed
  invocation and the landed receipt both pass `265a955cc…`, which is what all runs above used.
- Lane tip at probe time: `ede486b7a09afbacfb380d5871c46a8051a6dc2e`; explicit revision argument
  was the scored `265a955cc67be4eae97d2dc5a9338a25f31eb29b` in every run.
- Evidence files (scratch, disposable): `conform-pristine.py`, `conform-mut-cond-unconditional.py`,
  `selftest-pristine.txt`, `selftest-mutant.txt`, `cond-pristine.txt`, `cond-mutant.txt`
  under `.ufo/waves/round-40/scratch/mutconform-arms2/`.
- Production bytes untouched; no fleet/sibling writes; no jj/git mutations; no pacman.
