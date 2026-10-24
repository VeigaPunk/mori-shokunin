# RevC5Timeout — re-derivation of `timeout_state` (P-C5, mori round 38 wave 2)

**Verdict: PASS** — the claim holds. Every path that runs
`fixtures/hang-after-flush.py` yields `C1=unmet` (exit 1) with an explicit
`tool_timeout` reason; no path prints `C1=met` on the hanging tool and no path
collapses the timeout into a silent/generic unmet. Both FAIL conditions of the
acceptance are unmet by the evidence below.

Scored tip under attack: `f725f3076972e6e70595b5ac8279be524a111ff8`
(`git rev-parse HEAD` = same; `cat-file -t` = commit). Python 3.14.8.
All commands run read-only in the lane repo; the counter's own scratch went to
its designed parent `.ufo/waves/round-38/scratch` (count-c1.py:70, 898-911).

## Flag surface (assignment disambiguation)

`--tool-timeout` is a **counter** flag, not a checker flag:
`count-c1.py` declares `--tool`/`--tool-timeout`/`--arms` (count-c1.py:935-943)
and `--tool-timeout` feeds `_TOOL_BUDGET[0] = max(1, args.tool_timeout)`
(count-c1.py:959). `conform.py` declares only `rev --repo --contract --counter
--selftest` (conform.py:257-263); passing `--tool-timeout 5` exits 2
(`conform.py: error: unrecognized arguments`), run and observed. conform.py's
`timeout_state` check hardcodes the probe `first rev --tool HANG_FIXTURE
--tool-timeout 3 --arms real --seed 5` under an outer `timeout=25`
(conform.py:183-191; `HANG_FIXTURE` at conform.py:42).

## Path 1 — the counter's declared flags, `--tool-timeout 5`

```
python3 .ufo/waves/round-38/count-c1.py f725f3076972e6e70595b5ac8279be524a111ff8 \
  --repo /home/vgpnk/Projects/shokunin/mori-shokunin \
  --tool .ufo/waves/round-38/fixtures/hang-after-flush.py \
  --tool-timeout 5 --arms real --seed 5
```

Output (verbatim, truncated P-C1 line omitted):

```
tool: .ufo/waves/round-38/fixtures/hang-after-flush.py
real arm: FAIL (5.2s)
  tool:   (no summary line)
  oracle: appendonly_violations=18 ids=[S041,...,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  diff: tool_timeout: tool exceeded 5s (SIGTERM, then SIGKILL after 5s)
  diff: no summary line (exit None)
  diff: per-id lines: want changed=[...18 ids...] deleted=[] got changed=[] deleted=[] (malformed=0)
  tool exit=None
C1=unmet
seed=5
head_at_measurement=f725f3076972e6e70595b5ac8279be524a111ff8
EXIT=1
```

- Exit code: **1**. Elapsed: **5.2 s** (counter's own `real arm` timer; call wall
  time 5.20 s — agree). The `SECONDS=0` echo printed 196s, a shell artifact
  (session-shell `SECONDS` never reset; see line after run). Not used.
- `C1=met` absent; `real arm: pass` absent; `tool_timeout` present → the
  timeout is disclosed, not hidden as a generic unmet.

## Path 2 — the conformance checker on the same tool

```
python3 .ufo/waves/round-38/conform.py f725f3076972e6e70595b5ac8279be524a111ff8 \
  --counter .ufo/waves/round-38/count-c1.py --counter .ufo/waves/round-38/count-c4.py
```

```
check predicate        PASS (exit=0 equal=True)
check head_pin         PASS (pin=f725f307... tip=f725f307...)
check tool_resolve     PASS (resolved=.../fixtures/summary-only.py)
check bounded_reads    PASS (count-c1.py: run=True popen=True cap=True mkdtemp=True scratch=True; count-c4.py: run=True popen=True cap=True mkdtemp=True scratch=True)
check timeout_state    PASS (exit=1 timeout_reason=True pass=False)
check scratch          PASS (count-c1.py: mkdtemp_dir=True root=True; count-c4.py: mkdtemp_dir=True root=True)
CONFORM=met
EXIT=0
```

Exit code: **0**. Elapsed: **3.35 s** wall — consistent with the checker's
hardcoded 3 s inner budget plus process overhead (conform.py:186-187).
`timeout_state PASS (exit=1 timeout_reason=True pass=False)` — the check
re-derives exactly the required triple: exit 1, `C1=unmet`+`tool_timeout` in
output, no `real arm: pass` (conform.py:187-191).

## Coverage beyond the conformance arm — `--arms all` with the same tool

```
python3 .ufo/waves/round-38/count-c1.py f725f3076972e6e70595b5ac8279be524a111ff8 \
  --repo /home/vgpnk/Projects/shokunin/mori-shokunin \
  --tool .ufo/waves/round-38/fixtures/hang-after-flush.py --tool-timeout 5 --seed 5
```

- **blind arm:** `0/24 sandbox histories matched the hidden truth (120.9s)` —
  24 × `FAIL: tool_timeout: tool exceeded 5s (SIGTERM, then SIGKILL after 5s)`.
  Every one of the 24 hanging children was SIGTERMed at the 5 s budget and
  mapped to `tool_timeout` (count-c1.py:709-715 mapping; killed via killpg,
  count-c1.py:113-131).
- **real arm:** `FAIL (5.1s)` — `diff: tool_timeout: ...`, `tool exit=None`.
- **drawn arm:** `FAIL (10.2s) rev=4bfa049026 base=f04acbe512`,
  `reason: tool_timeout` (~2 × 5 s invocations).
- **challenge arm:** `FAIL (5.0s)`, `reason: tool_timeout: tool exceeded 5s (...)`.
- negatives unchanged in behavior: memo-n1/const/summary-only `rejected`,
  memo-sha `ACCEPTED (disclosed content-keyed bound)` — the disclosed bound
  path, by design (count-c1.py:1100-1110).
- `C1=unmet`, `EXIT=1`. Per-arm timers sum to ~141 s + sandbox builds ≈ the
  tool's measured 164.35 s wall; the `WALL=377s` echo includes the bg-queue
  delay and is not an arm-time measurement. Post-run `pgrep` found no blind-arm
  fixture children left — the counter reaped every child it owned.

## Discrimination control — `tool_timeout` is not a blanket fail

Same command as Path 1 without `--tool` (real `tools/mori-sources-appendonly.py`
blob at the rev), same `--tool-timeout 5`:

```
real arm: pass (0.3s)
  tool:   appendonly_violations=18 ids=[...18 ids...] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: (identical)
  tool exit=1
C1=met
EXIT=0
```

The real tool completes inside the same budget and scores `C1=met`, so the
unmet on the hang fixture is caused by the timeout, not by `--tool-timeout`
poisoning every arm.

## Kill coverage — the `timeout_state` mutation is checked

```
python3 .ufo/waves/round-38/conform.py f725f307... --selftest --counter .ufo/waves/round-38/count-c1.py
→ PASS timeout_state  budget flag ignored -> only timeout_state failed
  CONFORM_SELFTEST pass=6 fail=0
EXIT=0  (wall 41.9 s)
```

The mutation `_TOOL_BUDGET[0] = TOOL_TIMEOUT_S` (ignores `--tool-timeout`,
conform.py:225-226) flips exactly `timeout_state` to FAIL — i.e., a counter that
let the fixture run 120 s would hit conform's outer `timeout=25` (`proc=None`)
and fail the check. All six mutations PASSed; the check is not vacuous.

## Mechanism (cited, matches observed output)

- `count-c1.py:109-132` `run()`: `Popen(..., start_new_session=True)`; on
  `TimeoutExpired` SIGTERM the pgid, `communicate(timeout=TOOL_GRACE_S=5)`
  (count-c1.py:80,123), SIGKILL the pgid, `raise ToolTimeout`.
- `count-c1.py:554-561` `run_tool()`: catches `ToolTimeout` →
  `CompletedProcess(cmd, None, "", str(exc))` — returncode `None`, captured
  output discarded.
- Returncode `None` → `tool_timeout` reason at every arm (count-c1.py:714-715
  blind, 760-763 real — also maps exit 124, 817-818 drawn, 850-851 challenge).
- No inner GNU `timeout` (count-c1.py:549-553 comment); `tool exit=None`
  printed, never a raw 124 or a list mismatch.

## Residual risks / verification gaps (not claim-breaking)

1. **Orphaned grandchild under the outer-kill path.** conform.py's `run()`
   (conform.py:62-70) uses `subprocess.run(timeout=25)` which kills only the
   direct child. When the budget-ignoring mutant is probed, its
   `start_new_session=True` fixture grandchild is orphaned; `pgrep` after the
   selftest showed one live `hang-after-flush.py --repo <lane>` process
   (self-limiting: the fixture's `time.sleep(120)` ends it). The check still
   flips FAIL correctly (`proc=None` → `timeout_state` FAIL), but the outer
   kill leaks a 120 s sleeper per such run. Some foreign fixture processes from
   concurrent peer seats (`--repo /tmp/mori-r38-revtrends...`) also appeared in
   `pgrep`; only the lane-repo-arg one is consistent with my own selftest.
2. **Partial output discarded on timeout.** `run()` drops captured stdout on
   the timeout branch, so `real arm` prints `no summary line (exit None)` and a
   generic `per-id lines` diff alongside `tool_timeout`. The timeout reason
   still leads, so the state is disclosed (conform's grep sees `tool_timeout`),
   but the trailing diffs describe the empty capture, not the flushed bytes —
   cosmetic noise, not a hidden state.
3. **Fixture staleness.** `hang-after-flush.py` prints
   `superseded=[S041,...,S193]` (all 18) while the oracle at the scored tip
   computes `superseded=[S069,S182,S193]` (S226 landed this round). A counter
   that ignored the hang would fail on list content anyway; the timeout mapping
   — the thing under check — is unaffected, but the fixture no longer flushes
   "the right answer" for the lane arm specifically.
4. `timeout_state`'s `pass=False` probe only exercises the real arm
   (`--arms real`, conform.py:186-187); blind/drawn/challenge timeout mapping
   was verified here via `--arms all` instead of by the checker.

## Bounds

One file written (this report). No lane file edited; no git mutation; no
kill/config actions. Tooling: none installed (stock `python3` 3.14.8 only).

Report: .ufo/waves/round-38/w2/RevC5Timeout.md
