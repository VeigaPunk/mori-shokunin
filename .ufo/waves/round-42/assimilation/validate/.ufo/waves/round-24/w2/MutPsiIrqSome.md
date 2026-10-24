# MutPsiIrqSome — round 24 wave 2, claim C2 (selftest sensitivity), mutation probe

Seat: `MoriR24.MutPsiIrqSome`, mutation-tester, leaf. Written 2026-10-22 around 08:57Z.
Lane tip measured: `a730ecfefbdb5c31b1db13aca2c40eecd5e97abc` (branch master), the measured lane tip
for this wave.
Scratch clone: `/fast/scratch/hyaku/mori-r24-a2/w2/MutPsiIrqSome/work` (git clone --no-hardlinks
of the fleet repo, checked out at the tip, detached HEAD). The lane repo was never touched;
no git mutation (add/commit/stash/checkout/reset/pull/push) was run anywhere.
Installs and updates: none. Read `/home/vgpnk/.omp/agent/RULES.md`; system `python3` (3.14.8)
was already present and sufficient, so no tool was installed or upgraded.

## Mutant (single smallest code point)

Target claim: C2 — `tools/mori-pressure.py --selftest` prints `MORI_PRESSURE_SELFTEST: PASS
12/12` over the frozen `tools/fixtures/mori-pressure/cases.json`, with the contract rule
(`contract.md:64-65`) that `irq` needs `full` only and its missing `some` is expected
(`some: null`), never malformed.

Mutation implemented: *an irq file without a some line is treated as malformed*. The smallest
behavior-bearing point is the `irq` required-kind table entry:

```
before:  "irq": ("full",),
after:   "irq": ("some", "full"),
```

One line, `tools/mori-pressure.py:75` (in `REQUIRED_KINDS`). `_parse_resource`
(`tools/mori-pressure.py:186-189`) turns `irq` into `STATE_MALFORMED` when neither `some` nor
`full` is present; with the mutant, a full-only irq file now reports `missing required 'some'
line` → `malformed`. No other line changed.

## Detector and runs

Detector: `python3 -I tools/mori-pressure.py --selftest` (the declared after-value command),
run from the clone root.

Pristine clone (tip bytes, hash `852d1ea7508004dc44690bb6e358625fbd07d89c26d4196793133559d8a773a5`
of `tools/mori-pressure.py`, `aeb80ea080436cb344df8dba7ec19eeecc639e347ae87a14bc6835631f28ca94`
of `cases.json`):

```
MORI_PRESSURE_SELFTEST: PASS 12/12
exit=0
```

Mutated clone (hash `19aec5ea9c26be3d68d66533cfd3aa8e30359ef3bf0293f6f64454b497fb1dfc`):

```
MORI_PRESSURE_SELFTEST: FAIL 2/12
P01: verdict PRESSURE_PARTIAL != PRESSURE_OK; irq.state is 'malformed', expected 'ok'; irq.full is not an object
P02: verdict PRESSURE_PARTIAL != PRESSURE_OK; irq.state is 'malformed', expected 'ok'
P03: verdict PRESSURE_PARTIAL != PRESSURE_OK; irq.state is 'malformed', expected 'ok'; irq.full is not an object
P06: irq.state is 'malformed', expected 'ok'
P07: exit 0 != 1; verdict PRESSURE_PARTIAL != PRESSURE_HIGH; irq.state is 'malformed', expected 'ok'; irq.full is not an object; finding PRESSURE_HIGH on irq missing
P08: irq.state is 'malformed', expected 'ok'
P09: irq.state is 'malformed', expected 'ok'
P10: irq.state is 'malformed', expected 'ok'
P11: verdict PRESSURE_PARTIAL != PRESSURE_OK; irq.state is 'malformed', expected 'ok'; irq.full is not an object
P12: irq.state is 'malformed', expected 'ok'
exit=1
```

Only P04 (irq absent) and P05 (all EOPNOTSUPP) still pass: neither supplies irq file content.

## Verdict: KILLED

The frozen suite detects the mutant: 10 of 12 cases turn red and the selftest prints
`FAIL 2/12` (exit 1) instead of `PASS 12/12`. The claim's after-value detector is sensitive to
this defect — an implementation that wrongly treats full-only irq as malformed cannot pass.

The canonical detector is **P03** (topic "irq carries only a full line; irq is not malformed
for the missing some line, some stays null"): it feeds irq exactly `full ...` content and
asserts `irq.state == "ok"`, `irq.some == null`, `irq.full` dict — all three break under the
mutant. **P07** independently pins the same behavior through a different axis (irq full-only
`avg10=15` must yield verdict `PRESSURE_HIGH`/exit 1; under the mutant it yields
`PRESSURE_PARTIAL`/exit 0). P01/P02/P06/P08/P09/P10/P11/P12 additionally fail on
`irq.state == "ok"`.

No missing case needs to be named: the mutant was killed. Had it survived, the missing case
would have had to be exactly P03's scenario (an irq file with only a `full` line asserting
state ok and `some: null`), which already exists — i.e. the suite's irq-full-only coverage is
strong and redundant. `cases.json` was not edited.

## Restoration evidence

After the mutated run, line 75 was restored to `"irq": ("full",)`. Restored hash
`852d1ea7508004dc44690bb6e358625fbd07d89c26d4196793133559d8a773a5` equals the pristine hash;
`git diff --stat` and `git status --short` are both empty (worktree identical to the tip
commit). The restored clone reruns `MORI_PRESSURE_SELFTEST: PASS 12/12`, exit 0.

## Report

Trailer: `Report: .ufo/waves/round-24/w2/MutPsiIrqSome.md` (this file). Lane repo untouched;
scratch-only mutation, fully restored.
