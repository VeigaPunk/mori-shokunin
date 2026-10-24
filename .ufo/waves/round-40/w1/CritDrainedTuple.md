# CritDrainedTuple — attack drain_bind: tuple-swapped communicate binding

Seat: UFO-FSD critic, C1 / `drain_bind`, round-40 wave 1.
Measured instruments: `.ufo/waves/round-40/conform.py` (v3) and
`.ufo/waves/round-40/count-c8.py` at scored tip
`265a955cc67be4eae97d2dc5a9338a25f31eb29b` (checker run reported
`head_at_measurement=ede486b7a09afbacfb380d5871c46a8051a6dc2e`, the lane tip).

## Assigned question

Construct a counter whose Popen result is drained by a `communicate` bound to a
DIFFERENT name via tuple swap (`a, b = b, a` after assignment) yet consumed;
does v3's same-name binding rule accept or reject?

## Fixture A — different name, genuinely drained (the assigned counter)

`.scratch/CritDrainedTuple/counter-drained-tuple.py` — byte-identical to
`count-c8.py` except `run_tool`'s `out, err = proc.communicate(timeout=timeout)`
becomes:

```python
        other = None
        proc, other = other, proc
        try:
            out, err = other.communicate(timeout=timeout)
        finally:
            proc, other = other, proc
```

The Popen object is bound to `proc` at its `Assign`; the tuple swap moves the
OBJECT into `other`; `other.communicate(timeout=timeout)` drains it and the
result is consumed (`out, err = ...`); the `finally` swap-back restores `proc`
to the Popen before every `except` clause (`killpg(proc.pid)`), so the
counter's runtime behavior is identical to the counter of record — verified:
`run_tool` on a 200 KB-stdout child completes in <0.1 s with
`stdout_len=200000` (receipt below). The drain is real; only the draining
NAME differs.

Command run:

    python3 .ufo/waves/round-40/conform.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b \
        --counter .scratch/CritDrainedTuple/counter-drained-tuple.py

Output (tail): `check drain_bind FAIL (counter-drained-tuple.py:
violations=['Popen at line 143 not drained by a bound, consumed communicate in
its function'])` … `CONFORM=unmet`, `EXIT_A=1`. All other eight checks PASS.

**Verdict: v3 REJECTS the tuple-drained counter — `CONFORM=unmet` on
`drain_bind`, and per P-C10's literal words the rejection is the called-for
verdict.** P-C10 requires "a `communicate(` bound to the same name"; the rule
implements name-identity between the Popen's binding-site target
(`_popen_name`: single `ast.Name` `Assign`) and the communicate's receiver
(`func.value.id == target`). `other` ≠ `proc`, so no communicate qualifies.
Name-strictness survives the object swap: the words gate on the name, and the
rejection is faithful to them.

## The counterexample that matters — fixture B (hole, not tightness)

The symmetric swap shows the same-name test is a *name proxy for object
identity*, and the proxy is bypassable in the direction that counts.

`.scratch/CritDrainedTuple/counter-tuple-rebind.py` — `count-c8.py` plus a
`_StaleProc` stand-in class; `run_tool`'s drain becomes:

```python
        stale = _StaleProc(proc)
        proc, stale = stale, proc
        try:
            out, err = proc.communicate(timeout=timeout)
        finally:
            proc, stale = stale, proc
```

`stale = _StaleProc(proc)` is not a `Popen(` call, so the audit never binds it;
the tuple swap rebinds `proc` to the stand-in; `out, err =
proc.communicate(timeout=timeout)` is consumed, same-name, timed — every
static requirement the check enumerates is met — while the REAL Popen object
(now in `stale`) is never drained. `_StaleProc.communicate` calls
`self._proc.wait(timeout=timeout)`: it reaps the child but never reads the
pipes and returns `("", "")`.

Command run:

    python3 .ufo/waves/round-40/conform.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b \
        --counter .scratch/CritDrainedTuple/counter-tuple-rebind.py

Output: all nine checks `PASS`, **`CONFORM=met`, `EXIT_B=0`**.

Runtime proof the drain is dead (eval, `run_tool` on a child writing 200000
bytes to stdout then exiting):

- `count-c8.run_tool`: `completed rc=0 stdout_len=200000 wall=0.0s`
- fixture A `run_tool`: `completed rc=0 stdout_len=200000 wall=0.0s`
- fixture B `run_tool`: `ProbeTimeout: tool exceeded 5s (SIGTERM, then SIGKILL
  after 5s) wall=5.0s` — a child that finishes instantly under a real drain is
  killed because nobody reads the pipe; and even small-output runs return
  fabricated empty stdout/stderr.

So `drain_bind` accepts a counter that never drains `run_tool`'s Popen:
name satisfied, object starved. That is a soundness hole in the check P-C10
calls "made sound" — the r39 decoy/`_`/tuple bypasses are closed, but the
same-name proxy they exposed is still the whole rule.

## Fixable defect or judge-rejectable tradeoff?

Fixable defect, not a tradeoff. The words' primary clause — "is drained … by
a communicate" — is semantic: B's communicate never touches the Popen object,
so the Popen is not "drained by" it. The checker can honor the frozen words by
making its name proxy flow-aware instead of name-only.

**Smallest safe correction (code only, frozen text untouched):** in
`static_checks`' drain loop, for a Popen bound to name `N` in function `F`,
disqualify a `N.communicate` candidate if any `Assign`/`AnnAssign`/`AugAssign`
/`Delete` statement in `F` re-targets `N` (including as a `Tuple`/`List` elt)
at a source line strictly between the Popen-binding `Assign` and the
communicate call. Consequences: B's swap (`proc, stale = stale, proc`) is a
rebinder of `proc` between binding and call → the same-name communicate no
longer qualifies → `drain_violation` → `CONFORM=unmet`. A stays rejected
(receiver is `other` ≠ `proc`), matching the words. Honest counters with no
rebinding keep passing — the guard is monotone-tightening on the current
accept set only at programs that rebind, which the counter of record never
does. A `drain_bind_rebind` selftest arm (swap before call → expect FAIL)
would pin the fix the way `drain_bind_decoy` pins the decoy case.

## Secondary observation (fragility, not this claim's kill rule)

`selftest_conjunct` locates communicates by the textual regex
`communicate\(timeout=[^)]+\)`, not the AST. My first draft of fixture B
carried the literal string `communicate(timeout=...)` inside a *docstring*;
that produced `strips=7 detected=6` → `selftest_conjunct FAIL` on an
otherwise-passing counter. A comment or docstring mentioning
`communicate(timeout=x)` inflates `strips` while the AST `comm_violations`
scan sees no call — a false-positive vector that can reject honest counters.
Smallest fix: iterate `comm_calls` collected during the AST walk instead of
regexing source text.

## Commands run (all under /home/vgpnk/Projects/shokunin/mori-shokunin)

1. `python3 .ufo/waves/round-40/conform.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b`
   → nine PASS, `CONFORM=met`, exit 0 (baseline sanity).
2. `python3 .ufo/waves/round-40/conform.py 265a955cc… --counter
   .scratch/CritDrainedTuple/counter-drained-tuple.py` → `drain_bind` FAIL,
   `CONFORM=unmet`, exit 1.
3. `python3 .ufo/waves/round-40/conform.py 265a955cc… --counter
   .scratch/CritDrainedTuple/counter-tuple-rebind.py` → all nine PASS,
   `CONFORM=met`, exit 0.
4. `run_tool` fat-pipe probe (eval): c8 0.0 s / 200000 B, A 0.0 s / 200000 B,
   B `ProbeTimeout` at 5.0 s — reproduced above.

Fixture files (scratch, non-production):
`.scratch/CritDrainedTuple/counter-drained-tuple.py`,
`.scratch/CritDrainedTuple/counter-tuple-rebind.py`,
`.scratch/CritDrainedTuple/fat-tool.py`.

## Summary for the judge

- Assigned question: v3 **rejects** the tuple-swapped different-name drain
  (`CONFORM=unmet`, `drain_bind` FAIL) — the called-for verdict under P-C10's
  "bound to the same name" wording.
- The rejection exposes that the rule tests *binding-site name*, not the
  drained object. The inverse swap (fixture B) passes `CONFORM=met` while the
  Popen is never drained — a live bypass of the check the claim calls made
  sound. Impacted axis: C1 `drain_bind` soundness (the "three made sound"
  parenthetical and the routed-defect-1 genuine before-control).
- Correction is small, code-only, and word-preserving: interpose a
  no-rebinding-of-the-bound-name guard between Popen `Assign` and qualifying
  communicate; add a `drain_bind_rebind` selftest arm.
- No tools installed or upgraded (python3 stdlib only).
