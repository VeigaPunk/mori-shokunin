# MutPsiVerdictOrder — round 24 wave 2 (C2 selftest sensitivity: verdict precedence)

Seat: `MoriR24.MutPsiVerdictOrder` (leaf mutation tester). Probe: C2 `tools/mori-pressure.py`
`--selftest` sensitivity to verdict precedence — mutant: PARTIAL wins over HIGH, or PARTIAL
exits 2. Surface: `tools/mori-pressure.py` (evaluate verdict block), fixture
`tools/fixtures/mori-pressure/cases.json` (frozen P01–P12) — cases not edited.

Sandbox: `/fast/scratch/hyaku/mori-r24-a2/w2/MutPsiVerdictOrder/clone`, `git clone --no-hardlinks`
of the lane, checked out and staying at the measured lane tip
`a730ecfefbdb5c31b1db13aca2c40eecd5e97abc` (`round-24: wave-1 seat reports, S090 wording correction, contract amendment A5`).
The lane repo itself was touched only by writing this report; no git mutation was run in it.

## Focus and contract text

`evaluate` (tools/mori-pressure.py:336-345) decides, in order: all-unavailable →
`PRESSURE_UNAVAILABLE`/exit 2; any finding → `PRESSURE_HIGH`/exit 1; any non-ok state →
`PRESSURE_PARTIAL`/exit 0; else `PRESSURE_OK`/exit 0. Contract C2 pins: exit 1 on HIGH; exit 2
when every resource is unavailable; else exit 0, PARTIAL meaning at least one resource
unavailable or malformed. So HIGH must win over PARTIAL.

## Mutant applied (single smallest code change): PARTIAL wins over HIGH

Swapped the two `elif` branches: the PARTIAL branch now precedes the HIGH branch. One hunk,
2 insertions / 2 deletions:

```
diff --git a/tools/mori-pressure.py b/tools/mori-pressure.py
index 4e08739..fc5c0db 100755
--- a/tools/mori-pressure.py
+++ b/tools/mori-pressure.py
@@ -337,10 +337,10 @@ def evaluate(root: str, warn_avg10: float, interval_s: Optional[float]) -> Tuple
     states = [r["state"] for r in resources.values()]
     if all(s in UNAVAILABLE_STATES for s in states):
         verdict, rc = VERDICT_UNAVAILABLE, RC_UNAVAILABLE
-    elif findings:
-        verdict, rc = VERDICT_HIGH, RC_HIGH
     elif any(s != STATE_OK for s in states):
         verdict, rc = VERDICT_PARTIAL, RC_OK
+    elif findings:
+        verdict, rc = VERDICT_HIGH, RC_HIGH
     else:
         verdict, rc = VERDICT_OK, RC_OK
```

## Detector and outputs

Detector: `python3 -I tools/mori-pressure.py --selftest` (Python 3.14.8), run from the clone
root; expected after-value `MORI_PRESSURE_SELFTEST: PASS 12/12`, exit 0.

| copy | SHA256 of tools/mori-pressure.py | selftest output | exit |
|---|---|---|---|
| pristine (a730ecf, HEAD) | `852d1ea7508004dc44690bb6e358625fbd07d89c26d4196793133559d8a773a5` | `MORI_PRESSURE_SELFTEST: PASS 12/12` | 0 |
| mutated (PARTIAL beats HIGH) | `fdca6a151a3b286b28b93faa61ae92a23fe31622c39d49d247301f5dc7ab5eeb` | `MORI_PRESSURE_SELFTEST: PASS 12/12` | 0 |
| restored (exact bytes) | `852d1ea7508004dc44690bb6e358625fbd07d89c26d4196793133559d8a773a5` | `MORI_PRESSURE_SELFTEST: PASS 12/12` | 0 |

Fixture hash unchanged throughout: `aeb80ea080436cb344df8dba7ec19eeecc639e347ae87a14bc6835631f28ca94`
(`tools/fixtures/mori-pressure/cases.json`).

## Verdict: mutant SURVIVED (coverage finding)

The frozen 12 cases do not kill the precedence swap. Result: the selftest is insensitive to the
HIGH-vs-PARTIAL precedence.

The mutant is genuinely behavior-bearing, not equivalent. Ad-hoc probe root (built under the
sandbox, not in the lane): cpu/io low, memory `some avg10=25.00` (≥ default threshold 10.0 →
finding), and no irq file (ENOENT → `absent`):

- pristine: JSON verdict `PRESSURE_HIGH`, findings `['PRESSURE_HIGH']`, exit 1;
- mutated: same findings list but verdict `PRESSURE_PARTIAL`, exit 0.

So the branch swap is a real behavioral change that no frozen case observes.

Why it survives: the 12 cases partition cleanly into pure-HIGH (P06, P07: every resource ok,
findings present) and pure-PARTIAL (P04, P08, P09, P10, P12: one non-ok resource, no findings),
plus pure-OK (P01, P02, P03, P11). No case combines a threshold finding with a non-ok resource
state, which is the only input where the precedence order matters. P04/P08/P09/P10/P12 pin the
PARTIAL verdict and exit 0 only in the absence of findings; P06/P07 pin HIGH and exit 1 only with
every resource ok.

### Missing case, precisely

A case with BOTH (a) at least one threshold finding (`avg10 >= warn` on a `THRESHOLD_KINDS`
kind of an `ok` resource — e.g. P06's memory `some avg10=25.00`) and (b) at least one non-ok
resource state (`absent`/`unreadable`/`unsupported`/`malformed`/`counter_regressed` — e.g. P04's
absent irq), expecting verdict `PRESSURE_HIGH`, exit 1, with the partial finding/state also
present. The contract's precedence (HIGH wins; exit 1) is then pinned. Smallest insertion: clone
P06 and add P04's irq-absent shape (`"errors": {}`, no irq file), or clone P04 and raise a
threshold value. The fixture was not edited (per instructions).

## Secondary probe (same target, other half): PARTIAL exits 2 — KILLED

To bound the gap, the one-token variant `RC_OK` → `RC_UNAVAILABLE` in the PARTIAL branch
(`verdict, rc = VERDICT_PARTIAL, RC_UNAVAILABLE`, tools/mori-pressure.py:343) was also run:
`MORI_PRESSURE_SELFTEST: FAIL 7/12`, exit 1 — P04, P08, P09, P10, P12 fail (`exit 2 != 0`).
So the suite does pin "PARTIAL exits 0"; the uncovered half of the probe is exactly the HIGH-vs-
PARTIAL precedence, not the exit code. (Mutant file hash `7861e966e16ea44143ee443cfd45e5999c11aea96426fea77b81e95da0f3096f`, restored afterwards.)

## Restoration evidence

After each mutant, `git checkout -- tools/mori-pressure.py` (sandbox clone only) restored exact
bytes: SHA256 back to `852d1ea7508004dc44690bb6e358625fbd07d89c26d4196793133559d8a773a5`,
`git diff --stat` empty, selftest `PASS 12/12` exit 0, and the probe root reverts to
`PRESSURE_HIGH`/exit 1. Final clone HEAD still `a730ecfefbdb5c31b1db13aca2c40eecd5e97abc`.

## Tooling

No installs or host changes were needed or made: system `python3` 3.14.8 and `git` only. No
pacman transaction, no service change, no `/proc`/`/sys`/cgroup write, no PSI trigger, no
restart.

## Blockers / handoff

None. Finding for C2 review: the selftest's 12 frozen cases do not exercise the verdict
precedence between `PRESSURE_HIGH` and `PRESSURE_PARTIAL`; the declared after-value
`PASS 12/12` passes with the precedence inverted. Suggest the missing case above if the claim
should pin the contract's HIGH-over-PARTIAL order (unapplied; frozen cases untouched per
assignment).
