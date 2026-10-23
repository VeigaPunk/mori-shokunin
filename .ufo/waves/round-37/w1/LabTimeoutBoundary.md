# LabTimeoutBoundary — C1 tool-timeout boundary (round 37, wave 1)

**Item under attack:** the C1 timeout contract — `contract.md` "Timeout boundary (r36 routed debt f)":

> the tool budget is 120 s; on expiry the child's process group gets SIGTERM, then SIGKILL after
> a 5 s grace, and the arm reports `tool_timeout` — a distinct state, never a list mismatch.

and the counters' own disclosure (`count-c1.py:27-29`): "A tool timeout is reported as `tool_timeout`
and scored unmet-by-timeout".

**Scope:** measure the boundary with a fixture that sleeps N seconds for
N ∈ {TOOL_TIMEOUT_S−5, TOOL_TIMEOUT_S+5} = {115, 125}; report wall time and the state line for each.
No remediation performed (mori province: detection and report only).

---

## 1. Constants read from the counter

`.ufo/waves/round-37/count-c1.py`:

```
 63:TOOL_TIMEOUT_S = 120
 64:TOOL_GRACE_S = 5
```

Budget = 120 s; budget+grace = **125 s**.

## 2. Method

The state line is produced by the counter's own code, not re-implemented. Three layers of evidence:

| probe | file | what it drives |
|---|---|---|
| arm-level | scratch `arm_probe.py` | `count-c1.py`'s `real_arm()` / `check_blind()` verbatim (same strings `main()` prints) |
| end-to-end | scratch `e2e_c1.py` (`N_SANDBOX=1`, coverage gate relaxed; timeout machinery untouched) | the counter's `main()` — verbatim printed output |
| process-level | scratch `probe.py`, `pg_probe.py`, `group_probe.py` | `run_tool()` + pgid/group-reachability facts |

Fixture `fixture_sleep.py` sleeps `FIX_SLEEP` seconds, then `os.execv`s the **genuine**
`tools/mori-sources-appendonly.py` at the scored tip
(`git show e57c58b5...:tools/mori-sources-appendonly.py`, md5 `923b7d1b8d82c6f795ae990e6b22e239`,
499 lines) with the same argv — so the arm's truth comparison is genuine, not a stub.
Baseline control (sleep 0): arm verdict pass, summary `appendonly_violations=18 ids=[...18 ids...]`.

Scratch root: `/fast/scratch/hyaku/mori-r37/LabTimeoutBoundary/`.

## 3. Measurement — N = TOOL_TIMEOUT_S − 5 = 115 (below budget)

```
$ FIX_SLEEP=115 python3 arm_probe.py $PWD/fixture_sleep.py 115 real
FIXTURE       fixture_sleep.py
SLEEP_S       115
BUDGET        TOOL_TIMEOUT_S=120 TOOL_GRACE_S=5  budget+grace=125
WALL_S        115.25
ARM_VERDICT   pass
TOOL_EXIT     1
ARM_DIFF      (none)
```

End-to-end, the counter's own printed line (blind arm, `N_SANDBOX=1`):

```
$ FIX_SLEEP=115 python3 e2e_c1.py e57c58b57c025364e79d130fbdf764d2674d83d6 --tool $PWD/fixture_sleep.py --seed 4242
tool: /fast/scratch/hyaku/mori-r37/LabTimeoutBoundary/fixture_sleep.py
blind arm: 1/1 sandbox histories matched the hidden truth (115.1s; coverage: deletions=1 changed-back=0 superseded=1)
```

**Result:** completes normally — wall **115.25 s** (< 120 s budget), exit 1 (the genuine tool's own
violations exit), summary and per-id lines match the hidden truth, arm **pass**. The process-level
probe agrees: `WALL_S 115.13`, `RETURNCODE 1`, `STATE_LINE PASS (no diffs)`.

## 4. Measurement — N = TOOL_TIMEOUT_S + 5 = 125 (above budget)

```
$ FIX_SLEEP=125 python3 arm_probe.py $PWD/fixture_sleep.py 125 real
FIXTURE       fixture_sleep.py
SLEEP_S       125
BUDGET        TOOL_TIMEOUT_S=120 TOOL_GRACE_S=5  budget+grace=125
WALL_S        120.13
ARM_VERDICT   FAIL
TOOL_EXIT     124
ARM_DIFF      no summary line (exit 124)
ARM_DIFF      per-id lines: want changed=['S041', ... 'S193'] deleted=[] got changed=[] deleted=[] (malformed=0)
```

Blind-arm variant (same code path, `check_blind`):

```
WALL_S        120.00
ARM_VERDICT   FAIL
TOOL_EXIT     124
ARM_REASON    no summary line (exit 124):
```

End-to-end, the counter's own printed line:

```
$ FIX_SLEEP=125 python3 e2e_c1.py e57c58b57c025364e79d130fbdf764d2674d83d6 --tool $PWD/fixture_sleep.py --seed 4242
blind arm: 0/1 sandbox histories matched the hidden truth (120.0s; coverage: deletions=1 changed-back=0 superseded=1)
  repo00 FAIL: no summary line (exit 124):
```

**Result:** wall **120.00–120.13 s** (within budget+grace = 125 s ✓), **exit 124**, state line
**`no summary line (exit 124)`** — **not** `tool_timeout`.

## 5. Where `tool_timeout` actually appears (SIGTERM-deaf fixture, sleep 200)

```
$ FIX_SLEEP=200 python3 arm_probe.py $PWD/fixture_trap.py 200 real
WALL_S        185.24
ARM_VERDICT   FAIL
TOOL_EXIT     None
ARM_DIFF      tool_timeout: tool exceeded 180s (SIGTERM, then SIGKILL after 5s)
ARM_DIFF      no summary line (exit None)
```

The literal `tool_timeout` state is keyed on `proc.returncode is None`
(`count-c1.py:736-739`, `:692-694`), which is produced **only** by the `ToolTimeout` exception in
`run()` (`:100-114`, raised at `:113`). `run_tool` calls `run(..., timeout=TOOL_TIMEOUT_S + 60)`
(`:535`) — **180 s**, not 125 s. Therefore the `tool_timeout` token needs ≥ 180 s wall (+ 5 s grace
inside the handler) and was measured at **185.24 s = 60.24 s past budget+grace**.

So the acceptance predicate "above-budget run reports `tool_timeout` within budget+grace" is
**unsatisfiable by construction** for any tool: no fixture sleeping N ≤ 125 can reach it.

## 6. Root cause — the two timeout layers

```
count-c1.py:532  def run_tool(tool, args, cwd="/"):
count-c1.py:533      cmd = ["timeout", str(TOOL_TIMEOUT_S), sys.executable, tool] + list(args)
count-c1.py:535          return run(cmd, cwd=cwd, timeout=TOOL_TIMEOUT_S + 60, env=clean_env())
count-c1.py:537      return subprocess.CompletedProcess(cmd, None, "", str(exc))
```

- GNU `timeout 120` (`:533`) enforces the budget and fires **first** at exactly 120 s. It sends
  SIGTERM to the tool's process group and exits **124**. Measured: `WALL_S 120.00`, `rc=124`.
- The counter's own SIGTERM → `TOOL_GRACE_S` → SIGKILL machinery (`:100-114`) is attached to the
  *outer* `run()` deadline of **180 s** (`:535`), i.e. 60 s late. For any SIGTERM-honoring tool the
  child is already dead at 120 s, so `:100-114` never runs and `ToolTimeout` is never raised.
- Because `:736-739` / `:692-694` test only `returncode is None`, exit 124 is **not** mapped to
  `tool_timeout`; the arm reports a generic missing-summary state instead.

Supporting process-level facts (measured, not inferred):

```
$ python3 pg_probe.py
timeout binary: pid=1997499 pgid=1997499 sid=1997499
counter killpg target would be pgid=1997499
child reports: child pid=1997502 pgid=1997499 sid=1997499
child pgid=1997499  timeout pgid=1997499  SAME_GROUP=True

$ python3 group_probe.py
timeout(3) rc=124 wall=3.00s
grandchild marker present after 22s: False
=> GNU timeout signalled the whole group (grandchild died)
```

i.e. the counter's `killpg` target *does* reach the tool, and GNU timeout *does* signal the whole
group — the defect is not reachability, it is that the counter's own grace/SIGKILL/report path is
scheduled 60 s after the budget and its state token is never produced at the boundary.

## 7. Secondary defect found by the same probe: the real arm does not check the exit code

`real_arm()` computes success from stdout alone (`count-c1.py:733-734`):

```
    ok = (got is not None and same_lists(got, expected) and bool(expected["ids"])
          and same_id_lines(ids, expected))
```

There is no exit-code check (unlike `check_blind` at `:708-711` and `challenge_arm` at `:786-788`).
A tool that emits the correct summary and then hangs past the budget is therefore scored **pass**:

```
$ FIX_SLEEP=200 python3 arm_probe.py $PWD/fixture_tail_hang.py 200 real
WALL_S        120.15
ARM_VERDICT   pass
TOOL_EXIT     124
ARM_DIFF      (none)
```

The tool was killed by the boundary (exit 124) yet the real arm reports "pass" with no diff. Blind
and challenge arms do check the exit code, so they would catch this fixture; the real arm alone
cannot distinguish "completed" from "killed after flushing output".

## 8. Measurement integrity

The lane counter moved under the measurement (concurrent seats): entering blob
`7518fef8f54afff69ee38a99f2acbf518006f5ad` (960 lines, the freeze pin in
`evidence/freeze-r37.txt`) → HEAD `e37dcc6` blob `3e15f9fd35b6a926396732ddc970ff92ced8c113`
(1020 lines, v2 amendment A1: drawn arm + `LANE_TITLE`). Verified the timeout machinery is
**byte-identical** in both:

```
e57c58b57c lines=960 TOOL_TIMEOUT_S=120 TOOL_GRACE_S=5 run=f2a9cd5e8aaedfdb run_tool=6d0202040916d60a
HEAD       lines=1020 TOOL_TIMEOUT_S=120 TOOL_GRACE_S=5 run=f2a9cd5e8aaedfdb run_tool=6d0202040916d60a
```

(`counter_frozen.py` hash-object = `7518fef...` = the freeze pin; `counter_live.py` = `3e15f9f...`.)
The findings therefore apply to both counter versions. No lane file was written or edited; the
end-to-end runs used a scratch copy differing only in `N_SANDBOX = 1` and the blind coverage gate.

## 9. Summary table

| N | relation | wall (s) | exit | state line (arm) | within budget+grace? |
|---|---|---|---|---|---|
| 115 | TOOL_TIMEOUT_S−5 | 115.13 / 115.25 | 1 | `pass` (no diffs) | yes — completes normally |
| 125 | TOOL_TIMEOUT_S+5 | 120.00 / 120.13 | 124 | `no summary line (exit 124)` | wall yes; **state is not `tool_timeout`** |
| 200 (SIGTERM-deaf) | ≫ budget | 185.24 | None | `tool_timeout: tool exceeded 180s (SIGTERM, then SIGKILL after 5s)` | **no — 60.24 s past** |

## 10. Risks / notes

- No remediation attempted (mori province). No tool installs or upgrades were performed.
- The `tool_timeout` wording in `count-c1.py`'s docstring and in `contract.md`'s timeout clause does
  not describe the boundary the code implements; exit 124 at the budget is reported as a generic
  missing-summary state.
- The real arm's missing exit-code check is a per-arm classification gap; the aggregate C1 verdict
  survives it only because the blind and challenge arms do check exit codes.

## VERDICT: FAIL

Defect, with path:line evidence:

1. **`count-c1.py:535`** — `run(cmd, timeout=TOOL_TIMEOUT_S + 60)` places the counter's own
   SIGTERM→grace→SIGKILL deadline at 180 s, 60 s past the 120 s budget, so `tool_timeout`
   (`count-c1.py:736-739`, `:692-694`) is unreachable within budget+grace; measured appearance at
   **185.24 s**.
2. **`count-c1.py:533`** — the inner GNU `timeout 120` fires first and converts expiry into exit
   **124**, which `count-c1.py:736-739` / `:692-694` do not map to `tool_timeout`; the measured
   above-budget state line is `no summary line (exit 124)` at 120.00–120.13 s (within budget+grace).
3. **`count-c1.py:733-734`** — `real_arm()` never checks the exit code, so an over-budget tool that
   flushed a correct summary is scored `pass` at exit 124 (measured: `ARM_VERDICT pass`, `ARM_DIFF (none)`).

The below-budget half of the acceptance predicate is met (N=115 completes normally, wall 115.25 s,
arm pass); the above-budget half is not (`tool_timeout` is not reported within budget+grace).
