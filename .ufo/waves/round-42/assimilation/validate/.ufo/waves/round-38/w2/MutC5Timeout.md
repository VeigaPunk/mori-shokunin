# MutC5Timeout — C2 / P-C5 `timeout_state` mutation probe (L1 MoriR38, wave 2)

Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin` @ `f725f3076972e6e70595b5ac8279be524a111ff8`
(`git rev-parse HEAD`). Leaf seat: no dispatch, lane read-only, all scratch under
`.ufo/waves/round-38/scratch/MutC5Timeout/`; the only non-scratch write is this report.

## Claim and detector under test

C2/P-C5 clause: a tool that flushes then hangs must map to `tool_timeout`, "never a pass and never a
silent unmet" (`contract.md` C2). Detector: `conform.py` check `timeout_state`
(`.ufo/waves/round-38/conform.py:18-19`, `:183-191`), which runs the first `--counter` as

`<counter> <rev> --repo <lane> --tool fixtures/hang-after-flush.py --tool-timeout 3 --arms real --seed 5`

and passes only when `returncode == 1`, `"C1=unmet"` in output, `"tool_timeout"` in output, and
`"real arm: pass"` absent (`conform.py:187-188`).

## Mutation

Scratch copy of the frozen counter v4.1 (sha256 `9ebf10a1…`):
`.ufo/waves/round-38/scratch/MutC5Timeout/count-c1-mutant.py`.

One line, at the real arm's timeout branch (pristine `count-c1.py:760-761`; `diff` exit 1, single hunk):

```
     if proc.returncode is None:
-        diffs.append("tool_timeout: %s" % proc.stderr.strip())
+        ok = True
```

Effect: a child whose `communicate()` deadline expired — `returncode is None`, the `ToolTimeout`
path (`count-c1.py:108-131`, `:558`) — is scored `ok=True`, so `real_arm()` returns pass.

* before (pristine copy): `9ebf10a117851c7451cf3ed7aaf5d6abe176ebffde2ae379ab5dffac50a5669e`
* mutated: `4997e2b309c2f957efd3bace06df90a7272c636ecd7545a1e4337718757be008`

## Baseline — pristine bytes (run first; inconclusive if it fails)

```
$ python3 .ufo/waves/round-38/conform.py f725f3076972e6e70595b5ac8279be524a111ff8 \
    --counter .ufo/waves/round-38/scratch/MutC5Timeout/count-c1-pristine.py \
    --counter .ufo/waves/round-38/count-c4.py
check predicate        PASS (exit=0 equal=True)
check head_pin         PASS (pin=f725f3076972e6e70595b5ac8279be524a111ff8 tip=f725f3076972e6e70595b5ac8279be524a111ff8)
check tool_resolve     PASS (exit=0 resolved=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-38/fixtures/summary-only.py)
check bounded_reads    PASS (count-c1-pristine.py: run=True popen=True cap=True mkdtemp=True scratch=True; count-c4.py: run=True popen=True cap=True mkdtemp=True scratch=True)
check timeout_state    PASS (exit=1 timeout_reason=True pass=False)
check scratch          PASS (count-c1-pristine.py: mkdtemp_dir=True root=True; count-c4.py: mkdtemp_dir=True root=True)
CONFORM=met
EXIT=0
```

## Detector run on mutated bytes

Same command, `--counter .ufo/waves/round-38/scratch/MutC5Timeout/count-c1-mutant.py`:

```
check predicate        PASS (exit=0 equal=True)
check head_pin         PASS (pin=f725f3076972e6e70595b5ac8279be524a111ff8 tip=f725f3076972e6e70595b5ac8279be524a111ff8)
check tool_resolve     PASS (exit=0 resolved=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-38/fixtures/summary-only.py)
check bounded_reads    PASS (count-c1-mutant.py: run=True popen=True cap=True mkdtemp=True scratch=True; count-c4.py: run=True popen=True cap=True mkdtemp=True scratch=True)
check timeout_state    FAIL (exit=0 timeout_reason=False pass=True)
check scratch          PASS (count-c1-mutant.py: mkdtemp_dir=True root=True; count-c4.py: mkdtemp_dir=True root=True)
CONFORM=unmet
EXIT=1
```

`timeout_state` flips PASS→FAIL; exactly the other five checks stay PASS (mutation is specific).
Counter-level confirmation — the mutant run directly on the same fixture/args:

```
real arm: pass (3.2s)
  diff: no summary line (exit None)
  diff: per-id lines: want changed=['S041','S044','S051','S062','S064','S069','S179','S180','S181','S182','S183','S184','S185','S186','S188','S189','S190','S193'] deleted=[] got changed=[] deleted=[] (malformed=0)
  tool exit=None
C1=met
exit=0
```

The flush-then-hang tool is scored a pass while `tool exit=None` — the exact defect class the check
exists to reject.

## Restoration and restored-byte detector run

`cp count-c1-pristine.py count-c1-mutant.py`; sha256 after restore
`9ebf10a117851c7451cf3ed7aaf5d6abe176ebffde2ae379ab5dffac50a5669e` = the lane's `count-c1.py` = the
`freeze-r38-v2.txt` pin. Same conform command on the restored bytes:

```
check timeout_state    PASS (exit=1 timeout_reason=True pass=False)
CONFORM=met
EXIT=0
```

## Lane counters untouched

* `.ufo/waves/round-38/count-c1.py` sha256 before and after: `9ebf10a117851c7451cf3ed7aaf5d6abe176ebffde2ae379ab5dffac50a5669e`
* `.ufo/waves/round-38/count-c4.py` before and after: `3340d594123e4f983ddadc4759fd108438bd9b314dda17ab56690a08a7302403`
* `git status --porcelain -- .ufo/waves/round-38/{count-c1.py,count-c4.py,conform.py,fixtures/}`
  prints nothing (clean).
* Pin provenance: `evidence/freeze-r38.txt` is the v1 pin set (count-c1 `4e59eeff…`, count-c4
  `5d416a1c…`, 17:49); tip bytes match `evidence/freeze-r38-v2.txt` (same two hashes as above) added
  by `f725f30`, whose message records the v4.1/v4.2 instrument changes. No drift beyond the
  documented version bump.
* Tooling: no installs or upgrades were needed or made (no package-manager transactions).

## Verdict

**KILLED.** `timeout_state` flips to FAIL (`check timeout_state    FAIL (exit=0 timeout_reason=False pass=True)`),
`CONFORM=unmet`, exit 1, all other checks PASS; restored bytes return `CONFORM=met`, exit 0.
Acceptance PASS.

## Coverage findings (observations only — no contract change claimed)

1. `real_arm()` never forces `ok=False` on a timeout: the `returncode is None` branch only appends a
   diff (`count-c1.py:760-762`) and the exit-code guard is skipped for `None`
   (`count-c1.py:757-758`). The arm fails on the frozen fixture only because `run_tool` discards the
   child's stdout on timeout (`run()` collects `out, err` but raises `ToolTimeout` on
   `count-c1.py:108-131`; `run_tool` returns `stdout=""` at `:558`). Observed: a scratch fixture
   printing the byte-exact correct summary plus all 18 per-id lines and then hanging
   (`scratch/MutC5Timeout/hang-correct.py`) still scores `real arm: FAIL` / `C1=unmet` exit 1 on
   frozen bytes — because the flushed bytes are thrown away, not because the scorer rejects a
   timeout. A counter that preserved `TimeoutExpired.output` would be blocked only by the
   `expected_exit=1` comparison at `:757-758` [INFERENCE from source; not exercised].
2. The check is fixture-keyed: `conform.py` hardcodes `HANG_FIXTURE` and passes because that
   fixture's flushed summary differs from the oracle. Mutation distance to a scored pass is one
   line, as measured.
3. A plain-unmet variant (`run_tool` returning `CompletedProcess(cmd, 1, "", "")` at `:558`) would
   also flip `timeout_state` to FAIL by the literal `"tool_timeout"` term of
   `conform.py:187-188`; not run, as the assigned probe is the pass-mapping mutant above.

## Scratch provenance (pre-existing, not this seat's run)

`scratch/MutC5Timeout/` already contained artifacts from an earlier attempt of the same seat id,
left before this session: `count-c1-base.py` (18:01), `count-c4.py` (19:34), `baseline.txt` /
`count-c1-mut.py` / `mutant.txt` (19:53-19:54). They are not mine and nothing in this report relies
on them; my files are `count-c1-pristine.py`, `count-c1-mutant.py`, `hang-correct.py` (20:03-20:05).
Their `mutant.txt` records that attempt's mutation (the conform selftest's
`_TOOL_BUDGET[0] = TOOL_TIMEOUT_S`) scored `check timeout_state    FAIL (exit=None
timeout_reason=False pass=False)` → `CONFORM=unmet`: killed, but by conform's own 25 s subprocess cap
expiring (`exit=None`) rather than by observing a timeout reason — a note on kill style for the C2
owner, not part of this seat's verdict.
