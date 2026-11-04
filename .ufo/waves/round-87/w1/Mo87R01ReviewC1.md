# Mo87R01ReviewC1 — adversarial review of C1 (operability)

seat: Mo87R01ReviewC1 · round: 87 · attempt 1 · wave: w1 · date: 2026-11-04
claim under attack: **C1** at `03b66a437e68d493ce0aacd1d80c321cc2e6bf7c`
target: `C1=met mutants=6 killed=6 survivors=0 total=6 arms=54`
entering control: `C1=unmet mutants=6 killed=0 survivors=6 total=6 arms=48` (rc 1)
mode: detection and report only. No lane file was written; no git mutation in the lane.

## Provenance (bytes actually read)

| path | sha256 (read at this hash) |
|---|---|
| `.ufo/waves/round-87/contract.md` | `bf208a448e096da4da5169e1b27db1b1ca97999119a2e43e49954c894042eb07` |
| `.ufo/waves/round-87/count-c1.py` | `e2ff968721678cc61d6a1674def8da3e27a43f3fed8daab79d53c657ae2c266e` |
| `.ufo/waves/round-87/count-c2.py` (worktree, not my seat) | `264a43f04af1f9f939da7b3890f608a669a0c7fc2922656ee83f35adb236b14d` |
| `.ufo/waves/round-87/evidence/controls-r87.txt` | `53d65a426632acdb5c88721a2e7847110780e8c668f8c8fbd4b1bdd5df75e616` |
| `.ufo/waves/round-87/evidence/probe-r87.txt` | `530e35e6058edfa5d690343e149e53392e3daa81ea3f13f3fe7224f26db3180d` |
| `.ufo/waves/round-86/count-c1.py` @ `03b66a4` | `bcd66561093aa3046739f2be57a5f418e1ce87dd2da451beaece1e6ecffd5e7a` |
| `.ufo/waves/round-86/count-c2.py` @ `03b66a4` | `28d667338674402fa6e72aa9c567f3f18c2387e4f8c1f0f5e4c63a894e02c584` |
| `.ufo/waves/round-86/count-c3.py` @ `03b66a4` | `2e618dce42b38418e85868e48f4da2c895c39dcb634fd5626c5761818927a760` |

Ancestry verified: `6fc09d6` → `03b66a4` → `b9e6f68d` → `a42b1d79` (`git merge-base --is-ancestor`, both checks exit 0).
The lane HEAD moved from `b9e6f68d` to `a42b1d79` while this seat ran (sibling work on the C2 evidence /
LOG / SCORECARD / corpus). `git diff --stat 03b66a4 b9e6f68d -- .ufo/waves/round-86/` and
`git diff --stat 03b66a4 HEAD -- .ufo/waves/round-86/` are both empty, so no post-claim drift touches the
three graded subjects. The frozen r87 counter is byte-identical at `03b66a4` and at HEAD.
Scratch: `/fast/scratch/hyaku/mori-r87/Mo87R01ReviewC1/` (removed before yield). No tool was installed.
No `/tmp` path was used for evidence. All counter runs used `--scratch` under the scratch dir.

**Overall verdict: the C1 measurement stands.** The target string is reproduced byte-for-byte from the lane
worktree and from a `--shared` clone; all six kills are assertion kills, each attributable to exactly one
new arm; every new arm is load-bearing (reverting it makes its mutant survive); the pre-existing arms were
not edited, renamed or weakened (additions only, 2 code lines changed); the arm counts are the pristine
after-revision counts and an extra label-only arm is rejected. Two reach caveats and one gate weakness are
recorded as findings below; none falsifies the frozen predicate P-C1.

---

## Attack 1 — re-run the frozen counter, lane and `--shared` clone

Command (lane, cwd = lane root):

```
python3 -I .ufo/waves/round-87/count-c1.py 03b66a437e68d493ce0aacd1d80c321cc2e6bf7c
```

Output, rc=0:

```
MUTANT count-c1.py M1-unanchored-conjunct killed rc=1
MUTANT count-c1.py M2-total-floor killed rc=1
MUTANT count-c1.py M3-arms-tally killed rc=1
MUTANT count-c2.py M4-receipt-summary killed rc=1
MUTANT count-c2.py M5-binding-digest killed rc=1
MUTANT count-c3.py M6-keyshape killed rc=1
C1=met mutants=6 killed=6 survivors=0 total=6 arms=54 rev=03b66a437e68
```

Command (clone, `git clone --shared` of the lane at `b9e6f68d`, toplevel asserted):

```
python3 -I .ufo/waves/round-87/count-c1.py 03b66a437e68d493ce0aacd1d80c321cc2e6bf7c \
  --repo /fast/scratch/hyaku/mori-r87/Mo87R01ReviewC1/clone
```

Output, rc=0: identical six `killed rc=1` lines and `C1=met mutants=6 killed=6 survivors=0 total=6 arms=54 rev=03b66a437e68`.

Own-detector gate: `python3 -I .ufo/waves/round-87/count-c1.py --selftest` → `C1_COUNTER_SELFTEST pass=18 fail=0`, rc 0.

**Verdict: PASS.** The after-value is not worktree luck; the counter is read-only (`git show` + scratch).

---

## Attack 2 — non-equivalence of each mutant (is a kill evidence, or an equivalent mutant?)

Method: each r86 counter at `03b66a4` was loaded as a module (pristine and each anchored mutation) and the
mutated clause was exercised **outside** the selftest, by calling the graded function directly on a named
input; then, where the counter's CLI can reach that input, the CLI was run against a fixture commit in the
scratch clone. Fixture repo toplevel asserted equal to the fixture dir before every commit; commits used
`-c user.name=t -c user.email=t@t`.

Witnesses:

| mutant | named input (outside the selftest) | pristine | mutant | non-equivalent? |
|---|---|---|---|---|
| `M1-unanchored-conjunct` | `grade(loader, scratch, [dup.py with the anchor twice, sens.py with it once and an assertion])` | `met=False`, extras `['unanchored tools/dup.py A occurrences=2']` | `met=True`, **same tail** `mutants=1 killed=1 survivors=0 total=1 arms=1`, same extras | **yes** (verdict differs) |
| `M2-total-floor` | `grade(loader, scratch, [])` | `met=False`, tail `mutants=0 … total=0` | `met=True`, same tail | **yes** (verdict differs) |
| `M3-arms-tally` | `grade` over a subject whose selftest reports 20 arms | tail `… arms=20` | tail `… arms=26` | **yes** (tally differs) |
| `M4-receipt-summary` | `grade_population` over a present receipt whose body lacks the summary token | `ok=False`, `problems=summary`, `summary=0 matched=0 unexpected=1` | `ok=True`, `problems=-`, `summary=1 matched=1 unexpected=0` | **yes** (bad receipt classified `met`) |
| `M5-binding-digest` | `grade_population` over a receipt with a wrong `counter-sha256` digest | `ok=False`, `problems=sha:payload.txt`, `bound=0` | `ok=True`, `problems=-`, `bound=1` | **yes** (unbound receipt accepted) |
| `M6-keyshape` | `derive("foo*bar", (set(),set(),set()))` and `derive("-MORI.X", …)` | `'value-changed'` | `'added-since-r10'` | **yes** (both) |

Domain split for M6 (same call): `derive("good_key")` → `value-changed` in both; `derive("-window")` and
`derive("+SURFACE:lane.mori")` → `added-since-r10` in both. The mutation only moves the non-keyshape branch.

CLI-level reach (fixture commits in the scratch clone, `--repo clone`):

- **M4** (commit `64a193e3`, `.ufo/waves/round-85/evidence/after-r85.txt` body `C1=met` → `C1=gone`):
  pristine `C2=unmet receipts=5 … summary=4 … matched=3 defeated=1 legacy=3 unexpected=1`;
  mutant `C2=unmet … summary=5 … matched=4 defeated=1 legacy=3 unexpected=0 detector=red`.
  The bad receipt is reported `met problems=-` under the mutation — a real data-path divergence.
- **M5** (commit `cc7c6a49`, binding digest of `.ufo/waves/round-85/count-c1.py` zeroed):
  pristine `C2=unmet … bound=6 … matched=3 … unexpected=1`; mutant `C2=unmet … bound=7 … matched=4 … unexpected=0`.
- **M1** (commit `9909df66`, the `H-C3-metverdict` anchor duplicated in a trailing comment of the r85 subject;
  subject selftest still `C3_COUNTER_SELFTEST pass=26 fail=0`):
  pristine `C1=unmet mutants=5 killed=5 survivors=0 total=5 arms=26 detector=green`;
  mutant `C1=unmet mutants=5 killed=5 survivors=0 total=5 arms=26 detector=red`.
  Identical tails; the only differing token is the detector gate itself. `target_split` requires `total=6`,
  and an unanchored anchor reduces `total` to 5, so the mutated `met=True` can never surface as `C1=met`.
- **M2**: not CLI-reachable — `MUTANTS` is a module constant of six; no CLI invocation calls `grade` with an
  empty population.
- **M3**: the printed `arms=` differs on a subject whose tally is not 26, but `arms_ok`/`tail_arms` already
  pin the subject tally to 26, so the CLI verdict is unchanged (diagnostic-only divergence).
- **M6**: no committed-data witness. `corpus/evidence/drift-classification-r82.txt` holds 64 `DRIFT_CLASS`
  tokens; **0** have a non-keyshape / non-`SURFACE:`/`FINDING:`/word body, so the non-keyshape branch is
  exercised only by synthetic input.

**Verdict: PASS with a reach caveat.** No mutant is equivalent: each has a named input whose behaviour differs.
M4/M5 diverge on data the counter actually classifies; M1 and M3 diverge in the function's verdict/diagnostic
but not in the CLI verdict; M2 diverges only on an input the CLI never builds; M6 only on synthetic bodies.
The frozen kill rule does not require CLI reach, and the arms assert exactly the function contracts the
mutants violate.

---

## Attack 3 — are the new arms load-bearing?

Method: for each mutant, the two-line/… block that defines its new arm was deleted from the after-revision
counter (line ranges 246–251, 252–253, 254–258 in `count-c1.py`; 298–300, 304–306 in `count-c2.py`;
262–263 in `count-c3.py`), then the mutation was applied on top. Every copy was run with its own
`--selftest --scratch`.

| mutant | arm | pristine | arm reverted | mutant alone | mutant + arm reverted |
|---|---|---|---|---|---|
| M1 | `unanchored_plus_killed_unmet` | 18/0 rc0 | 17/0 rc0 | 17/1 rc1, `FAIL unanchored_plus_killed_unmet` | **17/0 rc0 — survives** |
| M2 | `zero_mutants_unmet` | 18/0 rc0 | 17/0 rc0 | 17/1 rc1, `FAIL zero_mutants_unmet` | **17/0 rc0 — survives** |
| M3 | `arms_tally_from_subject` | 18/0 rc0 | 17/0 rc0 | 17/1 rc1, `FAIL arms_tally_from_subject` | **17/0 rc0 — survives** |
| M4 | `summary_required` | 13/0 rc0 | 12/0 rc0 | 12/1 rc1, `FAIL summary_required` | **12/0 rc0 — survives** |
| M5 | `binding_required` | 13/0 rc0 | 12/0 rc0 | 12/1 rc1, `FAIL binding_required` | **12/0 rc0 — survives** |
| M6 | `derive_keyshape` | 23/0 rc0 | 22/0 rc0 | 22/1 rc1, `FAIL derive_keyshape` | **22/0 rc0 — survives** |

(`pass/fail` is the counter's own `C*_COUNTER_SELFTEST` tally.) Each mutant produces **exactly one** `FAIL`,
and it is its own arm: no collateral failure, no arm-count change (17+1=18, 12+1=13, 22+1=23), so the kill is
not a crash, a setup error or an arm-count rejection. Removing the arm leaves a green, otherwise-complete
counter (17/12/22 arms) in which the mutant is green again.

Exact failing lines observed:

```
FAIL unanchored_plus_killed_unmet mutants=1 killed=1 survivors=0 total=1 arms=-1
FAIL zero_mutants_unmet mutants=0 killed=0 survivors=0 total=0 arms=-1
FAIL arms_tally_from_subject mutants=0 killed=0 survivors=0 total=0 arms=26
FAIL summary_required RECEIPT fixture-a.txt expect=met met problems=-
FAIL binding_required RECEIPT fixture-b.txt expect=met met problems=-
FAIL derive_keyshape keyshape
```

**Verdict: PASS.** All six arms are load-bearing; each kill is attributable one-to-one.

---

## Attack 4 — were pre-existing arms edited, renamed or weakened?

Command:

```
git diff 6fc09d69edbb11e5070ff33258de49f062c0fb9b 03b66a437e68d493ce0aacd1d80c321cc2e6bf7c -- .ufo/waves/round-86/
```

`--name-status`: `M` for the three counters only — no added or deleted file.

Per-file change counts (added/removed, excluding file headers):

```
count-c1.py +13 -0
count-c2.py +33 -2
count-c3.py  +2 -0
```

Every changed line (`git diff -U0`, verbatim):

```diff
--- a/.ufo/waves/round-86/count-c1.py
+++ b/.ufo/waves/round-86/count-c1.py
@@ -245,0 +246,13 @@ def selfcheck(scratch):
+    write(d, "sensitive2.py", sensitive)
+    met, tail, _lines, extras = grade(
+        disk, scratch, [("tools/dup.py", "M1-unanchored-conjunct-old", "GUARD = 1", "GUARD = 0"),
+                        ("tools/sensitive2.py", "M2-total-floor-old", "GUARD = 1", "GUARD = 0")])
+    cases.append(("unanchored_plus_killed_unmet",
+                  (not met) and "unanchored" in " ".join(extras), tail))
+    met, tail, _lines, _ = grade(disk, scratch, [])
+    cases.append(("zero_mutants_unmet", (not met) and "total=0" in tail, tail))
+    write(d, "twenty.py", "print('FAKE pass=20 fail=0')\n"
+                          "print('C3_COUNTER_SELFTEST pass=20 fail=0')\n")
+    met, tail, _lines, _ = grade(
+        disk, scratch, [("tools/twenty.py", "M3-arms-tally-old", "FAKE", "FAKE")])
+    cases.append(("arms_tally_from_subject", tail.endswith("arms=20"), tail))
--- a/.ufo/waves/round-86/count-c2.py
+++ b/.ufo/waves/round-86/count-c2.py
@@ -169 +169 @@ def ancestor(repo, rev, tip):
-def grade_population(loader, repo, rev, scratch):
+def grade_population(loader, repo, rev, scratch, population=None):
@@ -170,0 +171 @@ def grade_population(loader, repo, rev, scratch):
+    population = POPULATION if population is None else population
@@ -176 +177 @@ def grade_population(loader, repo, rev, scratch):
-    for path, expect, replay_mode, token in POPULATION:
+    for path, expect, replay_mode, token in population:
@@ -275,0 +277,30 @@ def selfcheck(scratch):
+    fx = os.path.join(scratch, "fixture-repo")
+    os.makedirs(fx, exist_ok=True)
+    genv = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull)
+    run(["git", "-C", fx, "init", "-q"], env=genv)
+    open(os.path.join(fx, "payload.txt"), "w", encoding="utf-8").write("payload\n")
+    run(["git", "-C", fx, "-c", "user.name=t", "-c", "user.email=t@t", "add", "-A"], env=genv)
+    run(["git", "-C", fx, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "fx"],
+        env=genv)
+    frev = run(["git", "-C", fx, "rev-parse", "HEAD"]).stdout.strip()
+    payload_sha = hashlib.sha256(b"payload\n").hexdigest()
+    header = ("# cmd: printf x\n# rev: %s\n# counter-sha256: %s payload.txt\n"
+              "# limits: named limit - fixture receipt for detector arms\n# ---\n" % (frev, payload_sha))
+    stat_a = ("# cmd: printf x\n# rev: %s\n# counter-sha256: %s payload.txt\n"
+              "# limits: named limit - fixture receipt for detector arms\n# ---\nNOTHING-HERE\n"
+              % (frev, payload_sha))
+    stat_b = ("# cmd: printf x\n# rev: %s\n# counter-sha256: %s payload.txt\n"
+              "# limits: named limit - fixture receipt for detector arms\n# ---\nTOKEN\n"
+              % (frev, "0" * 64))
+    tok_loader = lambda _p: stat_a                                   # noqa: E731 - fixture
+    ok_a, lines_a, _c = grade_population(tok_loader, fx, frev, scratch,
+                                         population=[("fixture-a.txt", "met", "legacy", "TOKEN")])
+    cases.append(("summary_required",
+                  (not ok_a) and any("summary" in line for line in lines_a),
+                  " ".join(lines_a)[:80]))
+    bind_loader = lambda _p: stat_b                                  # noqa: E731 - fixture
+    ok_b, lines_b, _c = grade_population(bind_loader, fx, frev, scratch,
+                                         population=[("fixture-b.txt", "met", "legacy", "TOKEN")])
+    cases.append(("binding_required",
+                  (not ok_b) and any("sha:payload.txt" in line for line in lines_b),
+                  " ".join(lines_b)[:80]))
--- a/.ufo/waves/round-86/count-c3.py
+++ b/.ufo/waves/round-86/count-c3.py
@@ -261,0 +262,2 @@ def selfcheck():
+    cases.append(("derive_keyshape",
+                  derive("foo*bar", (set(), set(), set())) == "value-changed", "keyshape"))
```

Assertions on that diff:

- The only removed lines are the two `grade_population` lines (signature + iteration source). **Zero** removed
  lines contain `cases.append`.
- Arm-label sets, extracted from both revisions and diffed: `count-c1.py` 15 → 18 (`+unanchored_plus_killed_unmet
  +zero_mutants_unmet +arms_tally_from_subject`); `count-c2.py` 11 → 13 (`+summary_required +binding_required`);
  `count-c3.py` 22 → 23 (`+derive_keyshape`). No label disappeared and none was renamed.
- The `population=None` default resolves to the frozen `POPULATION`; `main` still calls
  `grade_population(loader, repo, rev, scratch)` without the kwarg. No production-path assertion is weakened.
- The new c2 arms build a throwaway git fixture under `scratch` with `GIT_CONFIG_GLOBAL=GIT_CONFIG_SYSTEM=/dev/null`
  and `-c user.name=t -c user.email=t@t`; the lane is never touched.

**Verdict: PASS.** Additions only plus a behaviour-preserving parameterization.

---

## Attack 5 — are 18/13/23 the pristine counts, and can a label-only subject reach them?

Pristine counts measured from the after-revision bytes themselves (not from the evidence file):

```
$ python3 -I <03b66a4 copy>/.ufo/waves/round-86/count-c1.py --selftest --scratch …
C1_COUNTER_SELFTEST pass=18 fail=0     rc=0
$ … count-c2.py …
C2_COUNTER_SELFTEST pass=13 fail=0     rc=0
$ … count-c3.py …
C3_COUNTER_SELFTEST pass=23 fail=0     rc=0
```

Entering-revision counts, measured independently: `15/11/22` (green, rc 0 each) — matching the claim's
`15/11/22 -> 18/13/23` and the `arms=48` before-value.

Controls, run by the frozen counter against fixture commits in the scratch clone:

1. **Extra label-only arm** — after-revision `count-c1.py` plus `cases.append(("label_only", True, "x"))`
   (commit `16dde59b`):

   ```
   EXTRA pristine-arms .ufo/waves/round-86/count-c1.py arms=19 want=18
   C1=unmet mutants=6 killed=6 survivors=0 total=6 arms=55 detector=green
   rc=1
   ```

   An extra arm cannot reach the target (per-file count gate plus the `arms=54` sum).

2. **Strong label-only do-nothing control** — entering bytes, plus the six new `PASS <label>` lines, plus the
   tallies bumped to 18/13/23, with **no assertions** (commit `4bc36fd1`; subjects verified green at
   `pass=18/13/23`):

   ```
   C1=unmet mutants=6 killed=0 survivors=6 total=6 arms=54 detector=green
   rc=1
   ```

   Labels and tallies alone cannot reach the target; only the arms kill.

3. **Swapped arm (gate weakness)** — after-revision `count-c1.py` with the pre-existing `labels_unique` arm
   replaced by `cases.append(("label_only", True, "x"))`, so the tally stays 18 (commit `ae058ac5`):

   ```
   C1=met mutants=6 killed=6 survivors=0 total=6 arms=54
   rc=0
   ```

**Verdict: PASS for the frozen predicate, with a gate weakness recorded as finding 1.** The predicate is
explicitly tally-based ("green with exactly its frozen arm count"), and the delivered diff is additions-only,
so the delivered claim is not affected; but the gate cannot distinguish the frozen 18-arm set from a
same-size swapped set.

---

## Findings

1. **Low — the per-file arm gate is tally-only, not identity-based.** Measured: a subject at the after
   revision with one pre-existing arm (`labels_unique`) dropped and one inert `cases.append(("label_only", True, "x"))`
   added still yields `C1=met … arms=54` rc 0 (clone commit `ae058ac5`). Scope of the weakness: it cannot hide
   a regression in any of the six graded clauses, because that clause's mutant would survive and fail the
   claim; it can hide removal of a non-clause arm. No action implied for this claim (the delivered bytes are
   additions-only and attack 4 enumerates them), but the gate is weaker than the prose "labels and tallies
   alone are not the work" suggests for same-count substitutions.
2. **Low — three kills (M1, M2, M3) are function-contract kills with no CLI-verdict change.** `target_split`
   (`total=6`) masks M1's `met=True` (an unanchored anchor reduces `total` to 5); `MUTANTS` being a module
   constant makes M2's empty population CLI-unreachable; `arms_ok`/`tail_arms` pin the subject tally to 26,
   masking M3's constant. Measured for M1 at clone commit `9909df66`: pristine and mutant print identical
   `C1=unmet … total=5 arms=26` tails, differing only `detector=green` vs `detector=red`. The kills are still
   legitimate under the frozen kill rule and the arms assert the precise broken contracts; the caveat is about
   how much operational regression each kill demonstrates.
3. **Low — M6's kill is synthetic-input only.** `derive`'s non-keyshape branch is not reached by any committed
   classification token (`0/64` `DRIFT_CLASS` bodies in `corpus/evidence/drift-classification-r82.txt` are
   non-keyshape/non-name-word). The arm is the sole guard on that branch, but no lane datum exercises it.
4. **Info — `mutants=` is the same variable as `total=`** in the summary (`tail` formats `total` twice);
   `target_split` checks `killed/survivors/total/arms` and never `mutants`. Immaterial to P-C1, but the field
   carries no independent information.
5. **Info — `grade_population` gained an optional `population=` parameter**, the only two changed lines in the
   diff. Default resolves to the frozen `POPULATION`; the production call site is unchanged. The c2 selftest
   now also depends on `git` being available (it creates and commits a fixture repo under `scratch`); it was
   green here.
6. **Info — all six kills are assertion kills, not setup kills.** Each mutated copy exits 1 with exactly one
   `FAIL` and still reports its full case count (17+1, 12+1, 22+1); a crash or an `exit 2` would have been
   accepted by the frozen kill rule, but none occurred.

## Residual risk and verification gaps

- The target is a snapshot: it holds at `03b66a4` and at every later lane revision checked here (no round-86
  drift to `a42b1d79`). If the r86 counters are edited again, the after-value must be re-pinned; the counter
  will then read `pristine-arms` or a survivor rather than silently passing (demonstrated by the entering and
  extra-arm controls).
- The frozen label-only control fixture in `controls-r87.txt` §C1 is recorded at fixture rev `bc108f00a111`,
  which is not in the lane history; I could not replay that exact commit. I substituted the equivalent, stronger
  control on the entering bytes (finding above, control 2).
- C2 was not audited here (separate seat); this report makes no C2 claim.
- The lane moved during the seat (`b9e6f68d` → `a42b1d79`); all C1 numbers above were produced from
  `git show 03b66a4:` blobs and the byte-identical frozen counter, and re-hashed after the move.
- No tool was installed or upgraded for this seat; nothing outside the seat scratch and this report was written.
