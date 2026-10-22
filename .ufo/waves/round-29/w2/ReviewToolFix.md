# ReviewToolFix — wave-2 falsify: L1 draft tool change (rule A2-07 / A2-10)

Reviewer: MoriR29.ReviewToolFix (leaf seat). Lane tip 8809a3fe1eaa87a0afa177a15263d174378e7462.
Draft: `/fast/scratch/hyaku/mori-r29/L1/judge/fix.diff` (tool-base.py → tool-fix.py).
Sandbox: `/fast/scratch/hyaku/mori-r29/w2/ReviewToolFix/lane` (clone of lane at 8809a3fe,
`git clone --no-hardlinks`; `tool-fix.py` copied to `tools/mori-oom-killers.py`).
No installs needed; nothing to record per tooling directive.

## 1. What the draft changes

`fix.diff:3-19` (unbounded scope: skip records without a numeric
`__MONOTONIC_TIMESTAMP`, set `unplaced`), `fix.diff:23-33` (earlier bucket: same
stamp filter), `fix.diff:37-95` (scoped loop: per-segment `dryrun` state, closed at
each version line). Verdict assembly, earlier-bucket split, and the `acted` /
`unknown` rules (tool-fix.py:314-342, 455-488) are unchanged.

## 2. Sandbox selftest markers (tool-fix.py as tools/mori-oom-killers.py)

`python3 -I -B tools/mori-oom-killers.py --selftest --cases tools/fixtures/mori-oom-killers/<file>`

| file | marker | exit |
|---|---|---|
| cases.json | `MORI_OOM_KILLERS_SELFTEST: PASS 32/32` | 0 |
| cases-supplementary.json | `PASS 32/32` | 0 |
| cases-a2.json | `PASS 30/30` | 0 |
| cases-a2-r29.json | `FAIL 21/24` (21 FAIL lines, 6 cases) | 1 |

r29 failing cases and their FAIL lines (4/3/1/5/4/4 = 21):
- `r29-a2-07-real-then-dryrun-zero-enter` (4): verdict (got KILLER_ACTED, expected
  KILLERS_UNKNOWN), exit (1 vs 2), `actions.sigterm` (1 vs 0),
  `earlier_invocation_send_lines` (0 vs 1).
- `r29-a2-07-real-dryrun-real-missing-enter` (3): `actions.sigterm` (1 vs 0),
  `dryrun` (true vs false), `earlier_invocation_send_lines` (0 vs 1).
- `r29-a2-07-dryrun-then-real-missing-enter` (1): `dryrun` (true vs false).
- `r29-a2-10-failed-stamped-positive` (5) and
  `r29-a2-10-not-found-earlier-stamped-positive` (4):
  `earlier_invocation_send_lines` (1 vs 0 / 1), `version` (null vs 1.9.0),
  `grammar`, `dryrun_send_lines`, `process_group_lines` null-vs-0.
- `r29-a2-10-inactive-lone-missing-stamp` (4): `version`/`grammar`/
  `dryrun_send_lines`/`process_group_lines` null-vs-0 (verdict/exit pass).

Baseline (freeze evidence `.ufo/waves/round-29/evidence/c2-freeze-selftest.txt`):
tool at 7118f320 on the same frozen file → `FAIL 11/24`, 42 FAIL lines, 13 cases.
So the draft flips the marker to `FAIL 21/24` (6 cases): 10 of the 11 verdict/exit
mismatches are repaired (`dryrun-inside-scope`, `dryrun-then-real-missing-enter`,
`real-dryrun-real-missing-enter`, `unbounded-missing-stamp-alone`,
`inactive-lone-missing-stamp`), but `real-then-dryrun-zero-enter` — correct in the
base at verdict level — is broken by the draft.

## 3. Findings (ranked)

### F1 [HIGH] Unbounded scope is not split per invocation; earlier real sends become current-invocation evidence (A2-07/A2-06 regression)

The draft's scoped loop (tool-fix.py:357-410) never splits at version lines in the
unbounded path: `segment` accumulates from the first journal record, and
`close_segment()` runs only when a version line is seen while iterating scoped
entries. When `ActiveEnterTimestampMonotonic` is missing or 0 (tool-fix.py:288-292),
every stamped record is scoped, so a real send of an earlier invocation lands in the
same segment as the current invocation and is counted as `actions.sigterm` /
`sigkill` — i.e. positive evidence. The comment at tool-fix.py:357-360
("the scoped lines are split at each version line like the earlier lines above") is
not implemented: the earlier bucket (tool-fix.py:323-342) resets per version line and
counts pre-version lines as earlier invocation; the scoped bucket has no such reset.

Repro (frozen): `r29-a2-07-real-then-dryrun-zero-enter`
(`cases-a2-r29.json:404-455`): version@52000000, real SIGTERM@52000010, version@53000000,
dryrun@53000010, SIGTERM@53000020, AETM=0.
- base: KILLERS_UNKNOWN/2 (matches expect; only the two field mismatches `dryrun_send_lines=2`
  and `earlier_invocation_send_lines=0` — both judged tool error at
  `.ufo/waves/round-29/w2/Judge03.md:28-36`).
- fix: KILLER_ACTED/1, `actions.sigterm=1`, `earlier_invocation_send_lines=0` — the
  earlier real send became current sigterm and positive evidence. Exactly what A2-06
  forbids for an active earlyoom (round-27/contract.md:54) and what Judge03 ruled wrong
  (Judge03.md:47-60). The verdict change is a regression: UNKNOWN → ACTED, exit 2 → 1.

Repro (invented): active unit, missing AETM, journal `[send "pre"@500, version@1000,
dryrun@1100, send "post"@1101]` → base UNKNOWN/2 (no current positive evidence);
fix ACTED/1 (`sigterm=1`). The pre-version send is counted as current-invocation
evidence; under the earlier-bucket semantics it is an unknown-invocation send and
must not flip an active unit's verdict.

Same root cause as F3: the draft's segmentation only works when the earlier real
segment lies outside the scoped bucket (bounded AETM), not when everything is scoped
(unbounded). Because the amendment's own A2-07 shape includes the unbounded case
(round-29/contract.md:139-141, "unbounded: every stamped record of an active unit
whose ActiveEnterTimestampMonotonic is missing or 0"), the regression is in the shape
the round claims to pin.

Consequence for the freeze: if the draft lands, the C2 counter would still fail on
this case (verdict/exit), and the draft actively makes the tool disagree with rule
text A2-06/A2-07 on it.

### F2 [MED] `earlyoom.dryrun` is stale/leaked across invocations

The draft adds `segment["dryrun"]` (tool-fix.py:362,400-401) but keeps the global
`dryrun` flag (tool-fix.py:354,399-401) which is only ever set, never cleared per
segment. Any earlier segment that logged "dryrun mode enabled" leaves `dryrun=true`
in the result even when the current invocation is real. The result field is not
reset for an active unit, so the leak is observable.

Repro (frozen): `dryrun-then-real-missing-enter`
(`cases-a2-r29.json:355-403`): segment 1 dryrun, segment 2 real → `dryrun=true`
(expected false; FAIL line in selftest; Judge02.md:34 "unclear text"; Judge04.md:29
rules the fix's true "tool error (fix still wrong)"). Base already had the same leak
(base evidence `c2-freeze-selftest.txt` shows `dryrun: got true expected false` on both
`dryrun-then-real-missing-enter` and `real-dryrun-real-missing-enter`); the draft leaves it.

Repro (invented): active, AETM=2000, journal `[version@2100, dryrun@2200, send@2201]`
→ `dryrun=true`; replace the dryrun line with a real send → `dryrun=false` (no leak),
confirming the leak is the earlier segment's flag. The result field's meaning
("the current invocation's dry-run mode") is corrupted; consumers of `dryrun` would
believe the current invocation is dry-run when it is not.

### F3 [MED] Lines before the first version line and codes-version segments are merged into one bucket in the unbounded scope

Covered by F1 (pre-version lines) — the same flat-segment bug. Additionally, in the
unbounded path the whole boot is one segment, so a send between two version lines of
an *earlier* invocation is attributed to the current invocation (F1's repro), and a
send after the last version line of a dry-run invocation is handled by the per-segment
flag only when a version line separates it. The earlier bucket's semantics
(pre-first-version = unknown invocation; split at every version line,
tool-fix.py:323-342) are correct and contradict the scoped bucket's flat behavior.

### F4 [LOW] Residual field mismatches (null vs 0) on non-active units — pre-existing, not introduced

Non-active (`inactive`/`failed`/`absent`) units null out `version`, `grammar`,
`dryrun_send_lines`, `process_group_lines` (tool-fix.py:426-435, 446-448); the frozen
r29 cases pin 0 / verified grammar / version (Judge12.md:19-24). The draft doesn't fix
these and they remain FAIL lines. This is a pre-existing gap (base has them too), not
a draft regression.

## 4. Per-invocation dry-run split — what works

- Bounded active scope (non-zero AETM): earlier-bucket split already existed and is
  unchanged (`fix.diff` touches only the stamp filter there); scoped dry-run segment
  split works for the in-scope case (`dryrun-inside-scope` and
  `real-before-scope-current-dryrun` pass; `dryrun_send_lines` correct).
- `dryrun` per-segment counters are reset correctly at each version (tool-fix.py:364-371);
  the leak is only the global result flag (F2).

## 5. Stamp-less records (A2-10)

- Unbounded scope: records without a numeric `__MONOTONIC_TIMESTAMP` are excluded and
  set `unplaced` (tool-fix.py:288-292) → `scope_complete=false` when unplaced; they are
  not counted anywhere. Confirmed: `unbounded-missing-stamp-alone` (ACTED → UNKNOWN,
  matches expect UNKNOWN) and `stamped-send-survives` / `oomd-evidence-survives`
  (positive stamped evidence still stands).
- Earlier bucket: stamp-less records are excluded (tool-fix.py:317-322); they don't add
  to `earlier_invocation_send_lines`. Confirmed on `unclocked-send-alone` (earlier 1→0).
- `failed-stamped-positive` / `not-found-earlier-stamped-positive`: both stamps (one
  non-numeric) are excluded from the earlier bucket; the stamped send remains a send and
  still yields the ACTED verdict (matches expect). The remaining FAIL lines are the F4
  null-vs-0 fields plus the earlier-count discrepancy (base 2 → fix 1; expect 0/1):
  the fix reduces but doesn't eliminate the mismatch. Not a draft regression.

## 6. Verdict ordering / no older-case ACTED loss

Ran the complete differential base-vs-fix on all 118 inputs of the four case files
(32+32+30+24) via `--inputs`:

- cases.json / cases-supplementary.json / cases-a2.json: zero output differences
  (no verdict, exit, or field change). PASS 32/32, 32/32, 30/30 preserved.
- cases-a2-r29.json: 6 output flips, all in the r29 file:
  1. `dryrun-inside-scope` QUIET→ACTED (to expect ACTED) — repair
  2. `dryrun-then-real-missing-enter` UNKNOWN→ACTED (to expect ACTED) — repair
  3. `real-dryrun-real-missing-enter` UNKNOWN→ACTED (to expect ACTED) — repair
  4. `real-then-dryrun-zero-enter` UNKNOWN→ACTED (expect UNKNOWN) — **regression (F1)**
  5. `unbounded-missing-stamp-alone` ACTED→UNKNOWN (to expect UNKNOWN) — repair
  6. `inactive-lone-missing-stamp` ACTED→QUIET (to expect QUIET) — repair
- No older case (the three pre-r29 files) changes verdict. The only ACTED→non-ACTED
  flips are the two r29 repairs #5/#6, both toward the frozen expectation; no ACTED
  evidence is dropped by the draft. The net failure set is exactly one case
  (F1's #4): verdict/exit pass rate on r29 is 23/24 with the draft vs 13/24 in the base
  (11 whole-case failures), so the draft repairs 10 and breaks 1.

## 7. Residual risk / verification gaps

- Live-mode and systemd paths are untouched by the draft (pure reader only) and are not
  exercised (out of scope for `--inputs`/`--selftest`).
- The draft was evaluated as a drop-in for `tools/mori-oom-killers.py` in the sandbox
  only; not landed. Whether the L1's "lands only for mismatches judged tool error"
  rule protects F1's case depends on the L1's judge policy (Judge03 ruled it tool
  error, so an integration that honors that ruling would not land the draft there).
- Verdict-level equivalence was measured for all 118 inputs; full field-level equality
  was checked for the 6 differing cases only (the other 112 have identical output).

## 8. Bottom line

The draft's A2-07 segmentation is correct for bounded scopes and for the earlier
bucket, and the A2-10 stamp exclusion is correct in both buckets. But the unbounded
scope (AETM missing/0) — exactly the shape round-29 pins (contract.md:139-144) — is
not split, so the draft changes `r29-a2-07-real-then-dryrun-zero-enter` from
KILLERS_UNKNOWN to KILLER_ACTED (exit 2→1), contradicting A2-06/A2-07 and the local
judge ruling; it also leaks `dryrun=true` into real invocations (2 frozen cases).
Recommended before any landing: make the scoped loop split at every version line in
both bounded and unbounded paths (mirroring tool-fix.py:323-342), and reset the
result-`dryrun` flag per segment.
