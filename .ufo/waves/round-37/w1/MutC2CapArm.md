# MutC2CapArm — C2 cap policy: is the kill load-bearing in both directions?

**Item attacked.** The C2 cap axis of round 37: the `cap_kill` check in
`.ufo/waves/round-37/count-c2.py:170` and the `huge_cap` arm it exercises in
`tools/mori-source-drift.py:406` (policy at `tools/mori-source-drift.py:54`,
bounded read at `:163-166`). Claim under test: "the drift probe's two fetch
policies (4 MiB bounded read; post-redirect public-destination check) are named,
**each killed by its own mutation**" (P-C2, `count-c2.py:PREDICATE`).

Scored tip: `e57c58b57c025364e79d130fbdf764d2674d83d6` (lane `HEAD` at run time
`0a05f7e`; the counter reads committed bytes at the rev, and the worktree bytes
I copied hash-identical to the rev blobs). No lane byte was modified. No tool
installs were made. No `pacman` invocation.

## Bytes under test

| file | sha256 | identity |
|---|---|---|
| `.ufo/waves/round-37/count-c2.py` (lane) | `71c72929…2cadc3a7c1` | `git show e57c58b:…` = same |
| `tools/mori-source-drift.py` (lane) | `453c5d8e…447011552` | `git show e57c58b:…` = same |
| scratch `count-c2-pristine.py` | `71c72929…2cadc3a7c1` | pristine copy |
| scratch `count-c2-mutcapkill.py` | `c6435b48…e760614932` | counter mutant |
| scratch `tool-pristine.py` | `453c5d8e…447011552` | pristine copy |
| scratch `tool-capmut.py` | `3a84da58…9fa000e6` | tool mutant (same bytes as `repo-capdefect` tool) |

Blob ids at the rev: tool `162ee87b5b0789c6815f967f3db93d277bab38d9`, counter
`6213cf9a5ada709da8cd867581782737b2f06c71`.

Scratch root: `/fast/scratch/hyaku/mori-r37/MutC2CapArm/` (writes only there).
Commands below are run with `cwd` = that root unless stated.

## Mutant A — counter: `cap_kill` forced PASS (single site)

```diff
--- count-c2-pristine.py
+++ count-c2-mutcapkill.py
@@ -167,8 +167,9 @@
             cap_rc, cap_lines, _ = selftest(cap)
-            check("cap_kill", cap_rc == 1 and cap_lines.get("huge_cap") == "FAIL",
-                  "exit=%s huge_cap=%s" % (cap_rc, cap_lines.get("huge_cap")))
+            check("cap_kill", True,
+                  "exit=%s huge_cap=%s (MUTATION: cap_kill forced PASS)"
+                  % (cap_rc, cap_lines.get("huge_cap")))
```

Nothing else changes; the mutant still builds and runs the cap-mutant copy, so
the raw evidence stays visible in the detail string.

### A1 — required run at the scored tip

```
$ python3 count-c2-mutcapkill.py e57c58b57c025364e79d130fbdf764d2674d83d6
check tool_present   PASS (path=tools/mori-source-drift.py)
check selftest       PASS (exit=0 arms=[('exit_code', 'PASS'), ('huge_cap', 'PASS'), ('missing_sources_exit2', 'PASS'), ('redirect_private_refused', 'PASS'), ('row_states', 'PASS'), ('summary', 'PASS')])
check cap_kill       PASS (exit=1 huge_cap=FAIL (MUTATION: cap_kill forced PASS))
check redirect_kill  PASS (exit=1 redirect_private_refused=FAIL)
check knowledge      PASS (present=True rows=['S205', 'S221', 'S222', 'S223', 'S224', 'S225'] cited_commit=True)
check capability     PASS (rows=1 names_tool=True)
check readme         PASS (r36_row=True r37_row=True)
check live           PASS (present=True sentence=True)
C2=met
EXIT=0
```

Observed: `C2=met`, exit 0 — the required control. Its own detail carries the
killed evidence `exit=1 huge_cap=FAIL`; the forced-PASS conversion is what makes
that evidence inert.

Pristine control on the same rev produced `check cap_kill PASS (exit=1
huge_cap=FAIL)` / `C2=met` / `EXIT=0` (`out/counter-pristine-cleanrev.txt`), so
the scratch copy and the lane counter agree on clean bytes.

### A2 — discrimination: defect rev that only `cap_kill` can see

A bare cap removal is also visible to the tool's own `selftest` (collateral
`row_states`/`summary` failures, see B), so it cannot isolate `cap_kill`. The
isolating defect is a vacuous `huge_cap` arm: cap policy intact, arm condition
forced True (`repo-vacuous`, rev `cc8b2994bdb1dba7746a60154a9b287b919be0ca`,
built from rev bytes by `build-repos.py`; tool sha256
`2efc52e6…c5842dac`):

```diff
-                outcome_over == "unavailable" and outcome_at == "body"
+                True  # MUTATION: huge_cap arm condition forced True
```

The tool itself grades green on that rev, so `selftest` PASSes; only the
counter's re-run of the cap mutation can expose that the arm is vacuous.

```
$ python3 count-c2-pristine.py cc8b2994bdb1dba7746a60154a9b287b919be0ca --repo $S/repo-vacuous
check selftest       PASS (exit=0 arms=[('exit_code', 'PASS'), ('huge_cap', 'PASS'), ('missing_sources_exit2', 'PASS'), ('redirect_private_refused', 'PASS'), ('row_states', 'PASS'), ('summary', 'PASS')])
check cap_kill       FAIL (exit=1 huge_cap=PASS)
check redirect_kill  PASS (exit=1 redirect_private_refused=FAIL)
check knowledge      PASS (present=True rows=['S205', 'S221', 'S222', 'S223', 'S224', 'S225'] cited_commit=True)
check capability     PASS (rows=1 names_tool=True)
check readme         PASS (r36_row=True r37_row=True)
check live           PASS (present=True sentence=True)
C2=unmet
EXIT=1

$ python3 count-c2-mutcapkill.py cc8b2994bdb1dba7746a60154a9b287b919be0ca --repo $S/repo-vacuous
check selftest       PASS (exit=0 arms=[('exit_code', 'PASS'), ('huge_cap', 'PASS'), ('missing_sources_exit2', 'PASS'), ('redirect_private_refused', 'PASS'), ('row_states', 'PASS'), ('summary', 'PASS')])
check cap_kill       PASS (exit=1 huge_cap=PASS (MUTATION: cap_kill forced PASS))
check redirect_kill  PASS (exit=1 redirect_private_refused=FAIL)
check knowledge      PASS (present=True rows=['S205', 'S221', 'S222', 'S223', 'S224', 'S225'] cited_commit=True)
check capability     PASS (rows=1 names_tool=True)
check readme         PASS (r36_row=True r37_row=True)
check live           PASS (present=True sentence=True)
C2=met
EXIT=0
```

**Killed, counter direction.** With `cap_kill` present, the vacuous-arm defect
yields `cap_kill FAIL` and `C2=unmet` (exit 1); with the check forced PASS, the
same bytes yield `C2=met` (exit 0). The check is the sole aggregate detector for
that defect class, so removing it changes the verdict on a genuinely defective
tree.

### A3 — bounded observation (not a defect)

On `repo-capdefect` (rev `39ca5786…`, tool = cap anchor `1 << 40`, tool sha256
`3a84da58…9fa000e6`):

```
$ python3 count-c2-pristine.py 39ca57868af06ca35a988078eb871949f7854cd8 --repo $S/repo-capdefect
check selftest       FAIL (exit=1 arms=[('exit_code', 'PASS'), ('huge_cap', 'FAIL'), ('missing_sources_exit2', 'PASS'), ('redirect_private_refused', 'PASS'), ('row_states', 'FAIL'), ('summary', 'FAIL')])
check cap_kill       PASS (exit=1 huge_cap=FAIL)
check redirect_kill  PASS (exit=1 redirect_private_refused=FAIL)
C2=unmet
EXIT=1
```

`cap_kill` PASSes here because `CAP_ANCHOR` is absent in that tool, so
`str.replace` is a no-op and the "mutant" equals the already-broken tool, whose
arm fails. The aggregate is still `C2=unmet` via `selftest`. [INFERENCE] On a
green tool the same anchor drift cannot pass silently: the mutant would be a
no-op, `cap_rc` would be 0, and `count-c2.py:170` requires `cap_rc == 1`, so
`cap_kill` would FAIL. So the check is fail-closed for anchor drift; it cannot
distinguish "tool already broken" from "mutation killed the arm" on its own, and
does not need to — `selftest` covers the first case.

## Mutant B — tool: cap anchor mutated (single site)

```diff
--- tool-pristine.py
+++ tool-capmut.py
@@ -51,7 +51,7 @@
-FETCH_MAX_BYTES = 4 * 1024 * 1024  # bodies larger than this cannot be classified; read is capped at +1
+FETCH_MAX_BYTES = 1 << 40  # bodies larger than this cannot be classified; read is capped at +1
```

This is byte-identical to what the counter's own `cap_kill` mutant produces.

```
$ python3 tool-capmut.py --selftest
selftest exit_code            PASS
selftest row_states           FAIL (got=[('S101', 'fresh'), ('S102', 'excerpt'), ('S103', 'drifted'), ('S104', 'unavailable'), ('S105', 'unavailable'), ('S106', 'no-copy'), ('S107', 'no-copy'), ('S108', 'fresh'), ('S109', 'excerpt'), ('S110', 'unavailable')] want=[('S101', 'fresh'), ('S102', 'excerpt'), ('S103', 'drifted'), ('S104', 'unavailable'), ('S105', 'unavailable'), ('S106', 'no-copy'), ('S107', 'no-copy'), ('S108', 'fresh'), ('S109', 'unavailable'), ('S110', 'unavailable')])
selftest summary              FAIL (summary=('10', '2', '2', '1', '3', '2'))
selftest huge_cap             FAIL (over_cap=body at_cap=body len=4194304)
selftest redirect_private_refused PASS
selftest missing_sources_exit2 PASS
MORI_SOURCE_DRIFT_SELFTEST: FAIL (3/6)
EXIT=1

$ python3 tool-pristine.py --selftest
selftest exit_code            PASS
selftest row_states           PASS
selftest summary              PASS
selftest huge_cap             PASS
selftest redirect_private_refused PASS
selftest missing_sources_exit2 PASS
MORI_SOURCE_DRIFT_SELFTEST: PASS (6 cases)
EXIT=0
```

**Killed, tool direction.** `selftest huge_cap FAIL` with the diagnostic
`over_cap=body at_cap=body len=4194304`: the 4 MiB cap is what made the over-cap
body unclassifiable, and removing it flips the arm. The collateral `row_states`
and `summary` failures are consistent with the policy removal (S109 now grades
`excerpt`), not independent damage; the redirect arm stays green, so the
mutation is confined to the cap axis. Restoring the anchor (pristine copy)
returns 6/6 PASS.

## Verdict rationale — both directions

1. **Policy → arm (tool).** Cap anchor `4 * 1024 * 1024` → `1 << 40` flips
   `huge_cap` PASS→FAIL; pristine bytes are 6/6 green.
2. **Check → detection (counter).** A defect the rest of the counter cannot see
   (vacuous `huge_cap` arm, rev `cc8b2994`) is `cap_kill FAIL`/`C2=unmet` with
   the check intact and `C2=met` with the check forced PASS — removal changes
   the verdict on defective bytes, which is exactly what "killed by its own
   mutation" requires.

The required pair is observed verbatim: the counter mutant at the scored tip
prints `C2=met` (exit 0) and the tool mutant prints `selftest huge_cap FAIL`
(exit 1). No contradiction with P-C2 at `e57c58b`; nothing in the contract needs
to change.

## Restoration / lane integrity

The lane was never written. Byte-identical before and after all measurements:

```
$ sha256sum .ufo/waves/round-37/count-c2.py tools/mori-source-drift.py
71c72929f9ac4dc8af0c079fb91220413064cb043391bf495f5ce32cadc3a7c1  .ufo/waves/round-37/count-c2.py
453c5d8e260301df7a99daf62b4c16ea08e4a0b4f9e4f53821cdbce447011552  tools/mori-source-drift.py
$ git rev-parse e57c58b57c025364e79d130fbdf764d2674d83d6:tools/mori-source-drift.py e57c58b57c025364e79d130fbdf764d2674d83d6:.ufo/waves/round-37/count-c2.py
162ee87b5b0789c6815f967f3db93d277bab38d9
6213cf9a5ada709da8cd867581782737b2f06c71
```

Same sha256s and blob ids as the pre-mutation reading; `git status --porcelain`
shows no modification to either tracked path. Scratch mutants and their
transcripts (`out/counter-mut-cleanrev.txt`, `out/counter-pristine-capdefect.txt`,
`out/counter-pristine-vacuous.txt`, `out/counter-mut-vacuous.txt`,
`out/tool-capmut-selftest.txt`, `out/tool-pristine-selftest.txt`,
`out/mutdiff-*.txt`, `out/repo-build.txt`) are retained under
`/fast/scratch/hyaku/mori-r37/MutC2CapArm/`.

VERDICT: PASS
