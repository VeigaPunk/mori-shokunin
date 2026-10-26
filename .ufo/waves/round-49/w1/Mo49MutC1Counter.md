# Mo49MutC1Counter — mutation test of the C1 counter's decision logic (w1, round 49)

Date: 2026-10-25. Lane: mori-shokunin. Lane tip cited: freeze/master `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115`
(working tree HEAD == master at probe time); entering tip per contract `b3e3453d`. Target under test:
`.ufo/waves/round-49/count-c1.py` (frozen), sha256 `3c262a15ae28adffa63f6646d5ec15498d1a4c735dbc3c38f68af16afc616b6d`,
equal to `evidence/freeze-sha256.txt` line for the counter — the probed bytes are the frozen bytes.

## Method

- Detector: `python3 <copy>/count-c1.py --selftest`; **a mutant is killed iff selftest exits non-zero**.
  At freeze the selftest is `C1_SELFTEST pass=44 fail=0` (`evidence/selftest-c1.txt`); every run here was
  bounded at 900 s wall and finished in ~0.2 s each.
- Scratch copies only: each run lives at
  `.scratch/r49-Mo49MutC1Counter/runs/<id>/.ufo/waves/round-49/count-c1.py` with the unchanged round-48
  module copied to the sibling `round-48/` path, because the counter derives `LANE` and the r48 import from
  its own `__file__`. The copy sits inside the lane worktree, so the selftest's `git -C LANE …` reads
  resolve to the real lane (read-only). Harness fidelity check: the **pristine copy in this structure
  passes** (`rc=0`, `pass=44 fail=0`).
- All runs with `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49MutC1Counter/tmp`;
  the selftest's fixture repositories (throwaway identity `c1 <c1@example.invalid>`) are created only under
  that TMPDIR. No pacman, no tool installs (python 3.14.8 and git already present). No subagents used.
- Ten single-point mutations, one behavior-bearing point each, applied by exact-string replace
  (anchor asserted unique). Machine-readable evidence: `.scratch/r49-Mo49MutC1Counter/probe-results.json`,
  `survivor-evidence.json`, `survivor-evidence-m8.json`.

## Result summary

| mutant | point mutated (count-c1.py) | selftest | verdict |
|---|---|---|---|
| M1-error-as-unmet | `run_tool` error classification :241-242 | rc=0, pass=44 fail=0 | **SURVIVED** |
| M2-drop-real-conjunct | `verdict` met conjunction :301 | rc=1, pass=43 fail=1 (`verdict_real_red_unmet`) | **killed** |
| M3-ignore-real-opaque | `plan` staging :266 | rc=0, pass=44 fail=0 | **SURVIVED** |
| M4-drop-honest-unmet | `verdict` met conjunction :301 | rc=1, pass=43 fail=1 (`verdict_honest_red_unmet`) | **killed** |
| M5-skip-clone-variants | `plan` clone loop :267-269 | rc=0, pass=44 fail=0 | **SURVIVED** |
| M6-variant-name-scratch-dir | `plan.stage` tmpdir name :259 | rc=0, pass=44 fail=0 | **SURVIVED** |
| M7-order-follows-expectation | `plan` run-order sort :275 | rc=0, pass=44 fail=0 | **SURVIVED** |
| M8-drop-clone-toplevel-check | `fixture_variant` guard :183-184 | rc=0, pass=44 fail=0 | **SURVIVED** |
| M9-accept-timeout | `run_tool` timeout return :234-235 | rc=0, pass=44 fail=0 | **SURVIVED** |
| M10-change-min-tally | `MIN_TALLY` floor :59 | rc=0, pass=44 fail=0 | **SURVIVED** |

2/10 killed, 8/10 survived, 0 inconclusive (pristine baseline passed, so every run is decidable).

## Mutants

### M1 — treat error as unmet (SURVIVED)

```diff
--- pristine/count-c1.py
+++ mutant/count-c1.py
@@ -240,5 +240,5 @@
             got = m.group(1)
     if rc not in (0, 1) or got is None:
-        got = "error"
+        got = "unmet"
     elif (got == "met") != (rc == 0):
         got = "error"
```

mutant sha256 `b07b0f3f62e7ba9a0eafaeaff89b37e179e3cbd9d87bb7341c699bd9f3a69b0c` (pristine `3c262a15…`;
per-mutant before/after hashes for all ten runs are in probe-results.json). Selftest: `C1_SELFTEST pass=44 fail=0`, exit 0.
Observed divergence (unit level): `run_tool` against a stub exiting 2 → pristine `("error", 2)`, mutant
`("unmet", 2)`. With the mutant, a junk edit that crashes is forgiven (`junk_met` stays 0) and the line
prints `errors=0`.
Arm that would kill it: any arm executing the production `run_tool` (:224) against a crashing stub and
asserting `got == "error"` plus `errors ≥ 1` in `verdict`. `verdict_error_unmet` (:389) only feeds the
literal `"error"` to `verdict`; nothing runs `run_tool` — see Finding F1.

### M2 — drop the `real` conjunct (killed)

```diff
--- pristine/count-c1.py
+++ mutant/count-c1.py
@@ -301,5 +301,5 @@
     real = [g for n, e, g, r in results if n == "real"][0]
     errors = sum(1 for n, e, g, r in results if g in ("error", "timeout"))
-    met = junk_met == 0 and honest_unmet == 0 and real == "met" and errors == 0
+    met = junk_met == 0 and honest_unmet == 0 and errors == 0
     line = "C1=%s junk_met=%d honest_unmet=%d real=%s errors=%d variants=%d rev=%s" % (
```

sha256 `9a0f2fe0d06de64456795935e0aed9e2803a8444f9f62b101cf59189c5ed4221`. Selftest exit 1:
`FAIL verdict_real_red_unmet` → `C1_SELFTEST pass=43 fail=1`. Killed.

### M3 — ignore real-opaque (SURVIVED)

```diff
--- pristine/count-c1.py
+++ mutant/count-c1.py
@@ -264,5 +264,4 @@
         for name, expect, fn in list(r48.VARIANTS) + NEW_VARIANTS:
             stage(name, expect, fn(text))
-        stage("real-opaque", "met", text)
         for name, expect, move in CLONE_VARIANTS:
             d, sha, base = fixture_variant(scratch, move)
```

Selftest: `pass=44 fail=0`, exit 0. Observed divergence: production `plan()` stages **26** jobs and
`"real-opaque"` is absent (pristine: 27 jobs, staged). The opaque-named copy of R's SKILL.md is the only
read that catches a filename-sniffing tool; without it that leak class passes C1.
Arm that would kill it: a production-plan arm asserting `real-opaque` staged / 27 jobs. The existing
`handles_carry_no_variant_name` (:376) and sniffer arm (:393-398) run over `plan_text_only` (:434), a
parallel copy — see Finding F1.

### M4 — drop honest_unmet (killed)

```diff
--- pristine/count-c1.py
+++ mutant/count-c1.py
@@ -301,5 +301,5 @@
     real = [g for n, e, g, r in results if n == "real"][0]
     errors = sum(1 for n, e, g, r in results if g in ("error", "timeout"))
-    met = junk_met == 0 and honest_unmet == 0 and real == "met" and errors == 0
+    met = junk_met == 0 and real == "met" and errors == 0
     line = "C1=%s junk_met=%d honest_unmet=%d real=%s errors=%d variants=%d rev=%s" % (
```

sha256 `7d3ff0bd9186d0fc2e8439bb9a83fc21594a7f8c56bf8e27a03bd643bd85f995`. Selftest exit 1:
`FAIL verdict_honest_red_unmet` → `pass=43 fail=1`. Killed.

### M5 — skip the clone variants (SURVIVED)

```diff
--- pristine/count-c1.py
+++ mutant/count-c1.py
@@ -265,7 +265,4 @@
             stage(name, expect, fn(text))
         stage("real-opaque", "met", text)
-        for name, expect, move in CLONE_VARIANTS:
-            d, sha, base = fixture_variant(scratch, move)
-            jobs.append((name, expect, None, d, sha, os.path.join(scratch, "t-" + opaque(sha)), base, 1))
     except Anchor as exc:
         return None, "variant anchor: %s" % exc
```

Selftest: `pass=44 fail=0`, exit 0 — the fixture arms call `fixture_variant` directly, so they still pass.
Observed divergence: production `plan()` stages **25** jobs, N10/H5 absent (pristine: 27). The final line
would print `variants=24`, and nothing ties that number to the predicate's 26.
Arm that would kill it: a production-plan arm asserting `{N10, H5}` staged and `len(plan) == 27`;
`order_covers_every_variant` pins the `ORDER` constant, not the plan.

### M6 — use the variant name in the scratch dir name (SURVIVED)

```diff
--- pristine/count-c1.py
+++ mutant/count-c1.py
@@ -259,5 +259,5 @@
         with open(path, "w", encoding="utf-8") as f:
             f.write(body)
-        jobs.append((name, expect, path, repo, rev, os.path.join(scratch, "t-" + tag), baseline, min_tally))
+        jobs.append((name, expect, path, repo, rev, os.path.join(scratch, "t-" + name), baseline, min_tally))
```

Selftest: `pass=44 fail=0`, exit 0. Observed divergence: production `plan()` creates scratch dirs
`t-H1, t-H2, …` — the round-48 F1 leak (harness names carrying variant identity) reappears verbatim in
production staging; the run order also collapses to name order (`H5, real, N10, H1, …`, observed).
Arm that would kill it: the existing `handles_carry_no_variant_name` regex (`variant|junk|honest|[JNH]\d|real`,
:376) pointed at production `plan()` instead of `plan_text_only` — it matches `t-H1` immediately.

### M7 — make the order follow expectation (SURVIVED)

```diff
--- pristine/count-c1.py
+++ mutant/count-c1.py
@@ -273,5 +273,5 @@
         return None, "fixture variant: %s" % exc
     jobs.append(("real", "met", None, repo, rev, os.path.join(scratch, "t-" + opaque(rev, "real")), baseline, min_tally))
-    jobs.sort(key=lambda j: os.path.basename(j[5]))
+    jobs.sort(key=lambda j: ORDER.index(j[0]))
     for j in jobs:
         os.makedirs(j[5], exist_ok=True)
```

Selftest: `pass=44 fail=0`, exit 0. Observed divergence: run order becomes exactly ORDER order
(`J1…J8, H1…H4, N1…N9, H6, H7, N10, H5, real, real-opaque`; `order == sorted(order, key=ORDER.index)` is
true for the mutant, false for pristine). Run order then leaks variant identity and expectation, voiding
the "run order follows that hash" clause of P-C1.
Arm that would kill it: the existing `order_not_expect_sorted` (:378) pointed at production `plan()`
(or an arm asserting `plan()` and `plan_text_only()` produce the same order).

### M8 — drop the toplevel check of the clone (SURVIVED)

```diff
--- pristine/count-c1.py
+++ mutant/count-c1.py
@@ -181,6 +181,4 @@
     top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"], stdout=subprocess.PIPE, check=True,
                          timeout=60).stdout.decode().strip()
-    if os.path.realpath(top) != os.path.realpath(d):
-        raise Anchor("fixture is not its own repository")
 
     def commit(msg):
```

Selftest: `pass=44 fail=0`, exit 0 — the `fixture_%s_own_toplevel` arms (:419) re-verify the property of
a *correctly built* fixture; no arm exercises the negative case. Observed divergence (negative case
demonstrated by doctoring the `--show-toplevel` answer of the fixture repo to a foreign path):
pristine raises `Anchor: fixture is not its own repository`; the mutant builds the fixture without
complaint and the counter would score it.
Arm that would kill it: a negative fixture arm — a fixture whose toplevel resolves elsewhere must raise
`Anchor` (the doctor demo in `survivor-evidence-m8.json` is exactly that arm's body).

### M9 — accept timeout (SURVIVED)

```diff
--- pristine/count-c1.py
+++ mutant/count-c1.py
@@ -233,5 +233,5 @@
         rc = p.returncode
     except subprocess.TimeoutExpired:
-        return "timeout", None
+        return "met", 0
     got = None
     for l in out.splitlines():
```

Selftest: `pass=44 fail=0`, exit 0. Observed divergence (unit level, `TOOL_TIMEOUT` shortened to 1 s
against a 4 s sleeper): pristine `("timeout", None)`, mutant `("met", 0)`. Under the mutant a tool that
merely outlives `TOOL_TIMEOUT` on every run scores `met` on all 26 variants → `C1=met errors=0`.
Arm that would kill it: a `run_tool` arm against a sleeping stub (shortened timeout) asserting
`("timeout", None)`, and/or a verdict arm feeding `got="timeout"` asserting unmet + `errors ≥ 1`
(`verdict_error_unmet` :389 covers only `"error"`).

### M10 — change MIN_TALLY (SURVIVED)

```diff
--- pristine/count-c1.py
+++ mutant/count-c1.py
@@ -57,5 +57,5 @@
 
 BASELINE = r48.BASELINE
-MIN_TALLY = r48.MIN_TALLY
+MIN_TALLY = r48.MIN_TALLY + 1
 TOOL_TIMEOUT = r48.TOOL_TIMEOUT
 Anchor = r48.Anchor
```

Selftest: `pass=44 fail=0`, exit 0. Observed divergence: `MIN_TALLY` 26 → 27 and `plan()`'s default
`min_tally` 27, so every variant run (including `real`) uses `--min-tally-pins 27`, not the frozen
predicate's 26; a lowered mutant (e.g. 20) would demand less than the predicate while still printing
`C1=met`. No selftest arm reads `MIN_TALLY` or any job tuple's floor.
Arm that would kill it: `arm("min_tally_is_predicate_floor", MIN_TALLY == 26 and all(j[7] == 26 for j in plan(...)))`.

## Restoration evidence

- The frozen file `.ufo/waves/round-49/count-c1.py` was never opened for writing. sha256 before the probe
  = after the probe = `3c262a15ae28adffa63f6646d5ec15498d1a4c735dbc3c38f68af16afc616b6d` (matches
  `evidence/freeze-sha256.txt`).
- Restored-bytes run: a fresh copy taken from the frozen path after all mutants ran scores
  `C1_SELFTEST pass=44 fail=0`, exit 0 (`restored-check` in probe-results.json).
- Mutant bytes exist only under `.scratch/r49-Mo49MutC1Counter/runs/` (lane scratch, cleaned at round end
  per the contract); no lane-tracked byte changed, no git/jj state touched (read-only `rev-parse` only).

## Findings

Survivors are coverage findings about the frozen counter's selftest — limits, not edits; the counter is
not modified and no re-score is proposed.

- **F1 HIGH** — `.ufo/waves/round-49/count-c1.py:345-433` (`selftest`) never executes the production
  `run_tool` (:224) or `plan()` (:248): the handle/sniffer/order arms run over `plan_text_only` (:434),
  a near-copy, and verdict arms feed literal `got` strings. This single gap silently hosts six of the
  eight survivors (M3, M5, M6, M7 fully; M1, M9 via the runner). The selftest therefore certifies a
  parallel implementation of the staging logic, not the shipping one. Limit for C1: the selftest pin
  (`C1_SELFTEST pass=44 fail=0`) does not pin the production staging path. Suggested arms (for a future
  round, not this one): route `handles_carry_no_variant_name`/`order_not_expect_sorted` through
  production `plan()`, and add `run_tool` arms over stub tools (crash → `error`, timeout → `timeout`).
- **F2 HIGH** — `count-c1.py:234-235`: nothing in the selftest distinguishes a timed-out tool (M9): a
  counter that scored timeouts as `met` still passes `--selftest`, and in production a hanging tool would
  reach `C1=met errors=0`. The predicate's own protection is only `TOOL_TIMEOUT`'s existence, and
  `verdict_error_unmet` (:389) never sees the `"timeout"` got-value.
- **F3 MED** — `count-c1.py:241-242`: crash classification (`error`) is untested end-to-end (M1 survived);
  a mutant folding crashes into `unmet` forgives crashing junk tools while printing `errors=0`.
- **F4 MED** — `count-c1.py:266`: the `real-opaque` staging — the arm that catches filename-sniffing
  tools, the round-48 F1 leak — is not pinned by any selftest arm over production `plan()` (M3 survived).
- **F5 MED** — `count-c1.py:259,267-269,275`: the opaque scratch/tmpdir names, the clone-variant staging
  (N10/H5, the `variants=26` count) and the hash run order are all unpinned against production `plan()`
  (M5, M6, M7 survived); M6 reintroduces exactly the class the counter was built to close.
- **F6 LOW** — `count-c1.py:183-184`: the fixture self-toplevel guard has no negative test (M8 survived;
  demonstrated by a doctored `--show-toplevel`: pristine raises, mutant builds).
- **F7 LOW** — `count-c1.py:59`: the predicate's floor `--min-tally-pins 26` is not value-pinned by the
  selftest (M10 survived); the frozen sentence in contract.md is the only guard.
- **F8 (positive)** — the `verdict` conjunction is well defended: its two drop-mutants (M2, M4) were each
  killed by exactly the intended arm (`verdict_real_red_unmet`, `verdict_honest_red_unmet`, :387-388),
  with no collateral arm failures.
