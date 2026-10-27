# Mo56MutC2Counter — round 56 w1 mutation test of count-c2.py

Scope: mutation-test `.ufo/waves/round-56/count-c2.py` (frozen at
8be2717b0809281d07dffe83dad424a4859e0747) with >=6 mutants, cross-producted
against (a) the freeze tip, (b) the entering tip 5b295eeebd87ebd610d8d39bfe2035742f740cfa
(do-nothing baseline), and (c) single-change fixture branches built in a
`git clone --shared` scratch copy under
`/fast/scratch/hyaku/mori-r56/Mo56MutC2Counter/clone`. Detector in every cell:
`python3 <counter> <rev> --repo <clone>`; output line + exit code. All mutants
and fixtures are scratch files; the lane repo was never touched (restoration
evidence below).

## Baselines (pristine counter)

```
pristine 8be2717b rc=0 C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=8be2717b0809281d07dffe83dad424a4859e0747
pristine 3f494b49 rc=0 C2=met ... rev=3f494b49cde612d929e82887a48e1660c022c359   (receipt rev, identical verdict)
pristine 5b295eee rc=1 C2=unmet selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=5b295eeebd87ebd610d8d39bfe2035742f740cfa failed=tool_absent
```

`git show` bytes of count-c2.py at 8be2717b are byte-identical to the lane
working-tree file: sha256 `4b350c773a3c31e54cf2cb0e3d7a5c8e92d9a1101722c9a94f53db2492812465` (both).

## Fixtures (each an independent branch off 8be2717b; scratch clone only)

- F1  `d3c8f12db195904db1080ffa45c88f8f7e58ffa2` — w1-results.json: Rc05 vote hash `901c19ca0925`→`901c19ca0926`. Frozen-tool tally over it prints `rows=78 agree=78 double=67 single=11 zero=0 dissent=0 voters=16 bound_voters=15` (vs expected `double=68 single=10`).
- F2  `005488b401b5eb6eba67d743743d6ab99d8dfdf8` — tools/mori-vote-bind.py = T*: byte-different, behavior identical + one module-level side effect (writes `T-STAR-MARKER.txt` in the run dir). Selftest `pass=16 fail=0`, real tally line EXACT.
- F2b `3b5f2d56a3a86b4618466d444cedd80b63a7d9eb` — tool = T**: binds full-agree votes when an entry lacks `output`. Selftest pass=16, real tally EXACT.
- TP  `53a1afc95d48e741823c141c95b2d3bf8632b78b` — tool = TP: binds full-want votes when output contains `just prose`. Selftest pass=16, real tally EXACT; on the pristine prose-junk control it prints `zero=0 double=78` (pristine control FAILS it); on junk-without-outputs it prints `zero=78` (m2-style control passes it).
- F4  `15f3bae7cedb6e4cabd577c04624d6dc3db7d9be` — r55 count-c1.py `MIN_VOTES 2`→`0`; its real output at F4 (captured): `C1=met scope=78 rows=78 matched=78 status_ok=78 line_ok=78 source_rows=ok pins=ok provenance=ok same=69 moved=7 changed=2 broken=0 holds=78 stale=0 voted=78 dissent=0 rev=15f3bae7...` — i.e. `voted=0` disappears.
- F5  `543c3bcc3de3ded52953eb845399af0a5fefd6e1` — corpus/knowledge/vote-binding-r56.md present but names neither S545 nor the tool.
- FX  `8facbbb21d01c2908cb070b52c5f20126fc54ea5` — w1-results.json + 17th entry Mo55Rc17; tally 16-voter = EXACT line, tally 17-voter = `voters=17 bound_voters=16`.

Pristine at each fixture (defect controls):
`pristine F1 rc=1 failed=tally`; `pristine F2 rc=1 failed=pins`; `pristine F2B rc=1 failed=pins`;
`pristine TP rc=1 failed=pins,control`; `pristine F4 rc=1 failed=contrast`;
`pristine F5 rc=1 failed=entry`; `pristine FX rc=0 met`.

## Mutants

sha256 (post-run; identical to pre-run):
pristine `4b350c77…`, m1 `e6898c06…`, m2 `4ab6c510…`, m3 `520d3413…`,
m4 `6e7cdf8a…`, m5 `2f302be3…`, m6 `6adb0f91…`, m25 `64f6ed12…`,
mall `7e1f6c29…` (all six deltas verified by `diff` vs pristine: 5 hunks —
the EXPECT_TALLY and PIN changes merge into hunk one; m6 roster insert, m2
junk, m3 contrast-deletion, m4 entry change each show verbatim).

- m1: `EXPECT_TALLY = "TALLY"`.
- m2: junk control entries without `output` keys (`{"name": v}` only).
- m3: contrast arm deleted (whole r55 block → comment).
- m4: entry check reduced to `entry is None`.
- m5: `PIN = None`.
- m6: roster `VOTERS` = sorted names parsed from `results` (try/except fallback to frozen list).
- m25: m2 + PIN=None (cross combo).
- mall: m1+m2+m3+m4+m5 on m6 (all six deltas).

## Matrix (counter, rev-prefix, rc, verdict line)

```
m1 8be2717b rc=0 met | m1 5b295eee rc=1 unmet failed=tool_absent | m1 d3c8f12d(F1) rc=0 C2=met tally=ok  → BYPASSED
m2 8be2717b rc=0 met | m2 5b295eee rc=1 unmet tool_absent        | m2 3b5f2d56(F2B) rc=1 unmet failed=pins,control
                                                                 | m2 53a1afc9(TP) rc=1 unmet failed=pins
m3 8be2717b rc=0 met | m3 5b295eee rc=1 unmet tool_absent        | m3 15f3bae7(F4) rc=0 C2=met contrast=voted0 → BYPASSED
m4 8be2717b rc=0 met | m4 5b295eee rc=1 unmet tool_absent        | m4 543c3bcc(F5) rc=0 C2=met entry=ok → BYPASSED
m5 8be2717b rc=0 met | m5 5b295eee rc=1 unmet tool_absent        | m5 005488b4(F2) rc=0 C2=met selftest=ok tally=ok → BYPASSED
                                                                 | m5 3b5f2d56(F2B) rc=0 C2=met → BYPASSED
                                                                 | m5 53a1afc9(TP) rc=1 unmet failed=control (killed)
m6 8be2717b rc=1 unmet failed=tally                              | m6 5b295eee rc=1 unmet tool_absent
                                                                 | m6 8facbbb2(FX) rc=1 unmet failed=tally
m25 8be2717b rc=0 met| m25 5b295eee rc=1 unmet tool_absent       | m25 3b5f2d56(F2B) rc=1 unmet failed=control
                                                                 | m25 53a1afc9(TP) rc=0 C2=met → BYPASSED
mall FRZ rc=0 met | mall ENT rc=1 tool_absent | mall F1 rc=0 met → BYPASSED | mall F2 rc=0 met → BYPASSED
     | mall F2B rc=1 unmet failed=control (killed) | mall TP rc=0 met → BYPASSED | mall F4 rc=0 met → BYPASSED
     | mall F5 rc=0 met → BYPASSED | mall FX rc=0 met (not a defect — FX is met for pristine too)
```

Counter `--selftest`: pristine `pass=1 fail=0` rc=0; m1 `pass=0 fail=1` rc=1; mall `pass=0 fail=1` rc=1.

T* side-effect evidence: 5 `T-STAR-MARKER.txt` files materialized under
`$TMPDIR/mori-r56-c2-*` (one per tool-run cwd at F2) — the tampered tool's
unauthorized write executed invisibly to every arm once pins were gone.

## Verdicts

- BYPASSED combos printing `C2=met` on defective state: m1@F1, m3@F4, m4@F5,
  m5@F2, m5@F2B, m25@TP, mall@{F1,F2,F4,F5,FX,TP}.
- Killed mutants: m6 (self-kills at freeze — roster-from-results expands to 64
  names: `voters=64 bound_voters=15`, EXPECT_TALLY mismatch); m5@TP (control
  catches prose-binder); m25@F2B and mall@F2B (m2's missing-output junk
  catches T**); m2 (still caught by pins@F2B/TP).
- Survived without bypass (unobservable weakening vs pinned tool): m2 alone.
- Do-nothing gate: EVERY mutant incl. mall still prints `unmet failed=tool_absent`
  at the entering tip — `tool_absent` early-return is unreachable by any of the
  six weakening classes.

Named limits surfaced (for L1 routing; predicate/counters frozen — no fix proposed here):

1. The tally arm is a substring check; any line starting `TALLY ` satisfies m1.
   Exact-line equality is the intended strength (m1 is the regression guard).
2. The pin check is the single universal tool-integrity guard; behavioral arms
   cover only the four exercised deviations. A byte-different tool that
   selftests, tallies exactly, keeps junk at zero, yet performs arbitrary side
   effects (T* wrote a marker file) is invisible to every arm except `pins`.
3. The control arm samples ONE point of "junk space" (prose outputs). Tools
   binding missing outputs evade it (m5@F2B met); the m2 flavor samples a
   different point (no-outputs) and catches T** but would miss prose-only
   binders. Neither flavor covers both; m25 needed TP-class tooling to bypass.
   Coverage is sample-dependent.
4. The contrast arm accepts rc∈{0,1} and substring `voted=0`; a modified r55
   counter printing `voted=0` while dissenting (`dissent=N>0`) would still pass.
   Verified `voted=0` substring sensitivity only; dissent-token interplay
   [INFERENCE: format field is a direct int, so `voted=0` implies that field — but rc/exit-class and dissent are not examined].
5. The row arm (SOURCES.md S545 shape) was exercised by zero assigned mutants
   and zero fixtures here — its sensitivity is UNVERIFIED by this seat.
6. `count-c2.py --selftest` catches m1/mall (pass=0) but `evaluate()` never
   invokes it; the self-check exists but is opt-in only.
7. The roster VOTERS is load-bearing in THREE places (tally args, junk
   construction, and implicitly the 16-name gate). m6-style indirection is
   self-defeating on real bytes (64-name results → over-strict), so it cannot
   silently weaken — a genuinely dangerous roster mutation would need a filter
   that coincidentally preserves the 16 (none tested plausible).

## Tool installs

None required (python3 stdlib + git only). Pacman untouched (paused host-wide).

## Restoration / non-mutation evidence

- Lane counter file sha256 before all runs: `4b350c77…` ; after all runs:
  `4b350c77…` (byte-identical; file never opened for write).
- `git status --porcelain -- .ufo/waves/round-56/count-c2.py` → 0 lines.
- `git branch --list f1 f2 f2b f4 f5 fx tp mutfix` in lane repo → 0 lines (all
  fixture refs exist only in the scratch clone).
- Lane `HEAD` = `acc62f54fb0f53b47b428594dc27365150cbd76b` unchanged.
- Fixture commits carry a throwaway identity strictly inside the scratch clone;
  `git rev-parse --show-toplevel` asserted `== $C` before every commit.
- All TMPDIR artifacts live under `/fast/scratch/hyaku/mori-r56/Mo56MutC2Counter/tmp`;
  scratch tree removed after this report was written (cleanup line below).

## Findings

- MED — `count-c2.py` pins arm: tool integrity has a single universal gate;
  byte-different tools whose deviation is invisible to selftest/tally/control
  (side effects, missing-output binds, prose binds) are caught ONLY by `pins`
  (demonstrated: m5@F2, m5@F2B met). Named limit → round-57: consider hashing
  tool+selftest or a second integrity arm rather than a lone constant.
- MED — `count-c2.py` control arm: junk coverage samples exactly one shape
  (prose `output` strings). Missing-output-binding tools evade it; the inverse
  (m2) samples no-outputs and misses prose-binding. Neither covers both
  (m25@TP met). Named limit → round-57: multi-shape junk battery.
- MED — `count-c2.py` `main()/evaluate()`: the counter's own `--selftest`
  mode catches the m1/mall weakenings (pass=0) but is never invoked during
  evaluation; running counters through `--selftest` first would self-detect a
  class of counter tampering. Round-57 candidate check.
- LOW — `count-c2.py` tally arm: substring match on EXPECT_TALLY; m1@F1 met on
  tampered results. Recommend exact-line comparison.
- LOW — `count-c2.py` contrast arm: substring `voted=0` + rc∈{0,1}; dissent or
  other `voted=0`-containing anomalies not examined. Recommend parsing the
  field.
- LOW — `count-c2.py` row arm: sensitivity not exercised by this seat's
  mutants/fixtures — arm coverage UNVERIFIED.
- LOW — informational: m6 roster indirection is nonviable on real bytes
  (64-name results → tally `voters=64` → self-kill at freeze); the frozen
  16-name roster is load-bearing and tamper-evident in this construction.
