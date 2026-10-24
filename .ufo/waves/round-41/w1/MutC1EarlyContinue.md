# MutC1EarlyContinue — C1 selftest_conjunct mutation probe

Seat: `L1-mori-r41-attempt2.MutC1EarlyContinue` (leaf; no dispatch).
Wave: round-41 prepared v2, w1. Lane root: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Contract claim under attack: C1, frozen guard "an early-continue mutant fails `selftest_conjunct`"
(`.ufo/waves/round-41/contract.md`; control `.ufo/waves/round-41/evidence/control-before.txt`).
Measured revision: `62a207f7521fa2e2fcd2e8b0260f047ccfce8862` (entering tip, detached sandbox HEAD verified equal).
No sibling repo, lane Git/jj, lane index, `.ufo/state` or `.ufo/watchdog.log` was read or written other than this report.

## Mutant

Instrument source (pristine, pinned): `.ufo/waves/round-41/conform.py`
`sha256 e1f2e11e7556cb4522c36cf22b3666650561e8eba0a7a7e85dc8c22c65475427` — equals the
`freeze-r41.txt` pin. Mutation applies to an isolated copy only.

- Anchor (unique, count=1 in pristine), original line 933:
  `        for name, old, new, why in mutations:`
- Inserted immediately after the anchor, as an unconditional statement at the top of the
  mutation-loop body (mutant line 934, before `if old not in source:`):
  `            continue`
- Mutant bytes: `/tmp/mori-mutc1-35s0rovx/checker-mutant.py`
  `sha256 0b39d13eb2498f57dd9acd3d50e8c6d1b4596a0411bca4c68e1b6b224dbf34ea`
- Mutated region is exactly:
  `'        for name, old, new, why in mutations:\n            continue\n            if old not in source:\n'`

Behaviour-bearing point: `_selftest_applies_and_compares()` requires every `ast.Continue`
inside the single `for ... in mutations` loop to be guarded by the `if old not in source:`
test and to be a member of that guard's body. The inserted `continue` sits at loop-body top,
so it is unguarded; the check must report `entry_live=False`. `[INFERENCE]` At runtime the
same line would also skip every arm, making `--selftest` print `CONFORM_SELFTEST pass=0 fail=0`
exit 0; that path was not measured (outside the assigned detector).

## Detector (identical on all three byte states)

Normal evaluation of the checker under test, not `--selftest`:

```
/usr/bin/python3 <checker> 62a207f7521fa2e2fcd2e8b0260f047ccfce8862 \
  --repo /tmp/mori-mutc1-35s0rovx/repo \
  --contract /tmp/mori-mutc1-35s0rovx/repo/.ufo/waves/round-39/contract.md \
  --counter /tmp/mori-mutc1-35s0rovx/repo/.ufo/waves/round-41/fixtures/c1/count-c8.py
```

Sandbox: disposable `git clone --shared --no-checkout` of the lane, `checkout --detach
62a207f...`; sandbox HEAD equals the measured revision; frozen r41 `fixtures/c1` copied into it.
Expected: pristine/restored `CONFORM=met` exit 0 with all nine checks PASS; mutant exit 1 with
failing set exactly `["selftest_conjunct"]` (`CONFORM=unmet`), every other check still PASS.

## Actual outputs

### 1. Pristine (baseline) — exit 0

```
check predicate          PASS (exit=0 equal=True)
check head_pin           PASS (pin=62a207f7521fa2e2fcd2e8b0260f047ccfce8862 tip=62a207f7521fa2e2fcd2e8b0260f047ccfce8862)
check tool_resolve       PASS (exit=0 resolved=/tmp/mori-mutc1-35s0rovx/repo/.ufo/waves/round-39/fixtures/witness-summary-only-live.txt)
check bounded_reads      PASS (count-c8.py: bounded=[] value=[])
check timeout_scope      PASS (count-c8.py: bounded=[] value=[])
check drain_bind         PASS (count-c8.py: violations=[])
check timeout_state      PASS (exit=1 timeout_reason=True pass=False)
check scratch            PASS (count-c8.py: mkdtemp_dir=True root=True)
check selftest_conjunct  PASS (count-c8.py: honest_comm=[] strips=6 detected=6 anchor=True entry_live=True)
CONFORM=met
```

Baseline does not fail; the probe is conclusive.

### 2. Mutant (early continue) — exit 1

```
check predicate          PASS (exit=0 equal=True)
check head_pin           PASS (pin=62a207f7521fa2e2fcd2e8b0260f047ccfce8862 tip=62a207f7521fa2e2fcd2e8b0260f047ccfce8862)
check tool_resolve       PASS (exit=0 resolved=/tmp/mori-mutc1-35s0rovx/repo/.ufo/waves/round-39/fixtures/witness-summary-only-live.txt)
check bounded_reads      PASS (count-c8.py: bounded=[] value=[])
check timeout_scope      PASS (count-c8.py: bounded=[] value=[])
check drain_bind         PASS (count-c8.py: violations=[])
check timeout_state      PASS (exit=1 timeout_reason=True pass=False)
check scratch            PASS (count-c8.py: mkdtemp_dir=True root=True)
check selftest_conjunct  FAIL (count-c8.py: honest_comm=[] strips=6 detected=6 anchor=True entry_live=False)
CONFORM=unmet
```

Failing set is exactly `["selftest_conjunct"]`; the flip is isolated to `entry_live`
(True → False), i.e. the applied-and-compared conjunct, not to the anchor or strip tallies.

### 3. Restored exact bytes — exit 0

Restoration wrote the pristine bytes back to the mutated copy path (no byte-level patching).
Restored `sha256 e1f2e11e7556cb4522c36cf22b3666650561e8eba0a7a7e85dc8c22c65475427`,
equal to the pristine pin; restored bytes byte-identical to pristine (`True`). Detector:

```
check predicate          PASS (exit=0 equal=True)
check head_pin           PASS (pin=62a207f7521fa2e2fcd2e8b0260f047ccfce8862 tip=62a207f7521fa2e2fcd2e8b0260f047ccfce8862)
check tool_resolve       PASS (exit=0 resolved=/tmp/mori-mutc1-35s0rovx/repo/.ufo/waves/round-39/fixtures/witness-summary-only-live.txt)
check bounded_reads      PASS (count-c8.py: bounded=[] value=[])
check timeout_scope      PASS (count-c8.py: bounded=[] value=[])
check drain_bind         PASS (count-c8.py: violations=[])
check timeout_state      PASS (exit=1 timeout_reason=True pass=False)
check scratch            PASS (count-c8.py: mkdtemp_dir=True root=True)
check selftest_conjunct  PASS (count-c8.py: honest_comm=[] strips=6 detected=6 anchor=True entry_live=True)
CONFORM=met
```

## Verdict

**Killed.** The frozen C1 no-harm guard discriminates the early-continue defect: pristine and
restored bytes meet the detector, the mutated copy fails exactly `selftest_conjunct`
(`entry_live=False`) and exits 1 with `CONFORM=unmet`. No surviving-mutant coverage finding.

## Restoration / non-interference evidence

- Mutated copy restored to pristine bytes before exit; hash equality proven above
  (`0b39d13e…` → `e1f2e11e…`, both 64-hex SHA-256, equal to pristine and to `freeze-r41.txt`).
- Lane instrument untouched: `.ufo/waves/round-41/conform.py` read-back SHA-256
  `e1f2e11e7556cb4522c36cf22b3666650561e8eba0a7a7e85dc8c22c65475427`, unchanged, `True`.
- Detector ran only inside the disposable sandbox `/tmp/mori-mutc1-35s0rovx`
  (`checker-pristine.py`, `checker-mutant.py`, `repo`); `--repo` pointed at the sandbox clone,
  so no counter scratch or evidence path in the lane was written. Only this report was written
  in the lane.
- No tools installed or updated; no pacman invoked; no network fetch; no sibling repo opened;
  lane Git/jj state and index untouched. No Git subcommands beyond read-only
  `rev-parse`/`git show`-class reads inside the sandbox clone.
