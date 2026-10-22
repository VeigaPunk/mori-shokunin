# MutToolBatteryA — C2 mutation battery M01–M10 (round 26, wave 2)

Seat: `MoriR26.MutToolBatteryA` (leaf, no subagents). Lane: `mori-shokunin`.
Claim attacked: **C2** (coverage / capability: userspace OOM killer read capability), and the
frozen-case detector that carries it (`tools/mori-oom-killers.py --selftest`).
Sandbox clone: `/fast/scratch/hyaku/mori-r26/wt-w2mutA`, branch `r26-wt-w2mutA`, base
`16935e24c93fa7e7567413d7ec091339a5df1474` (clone working tree clean at start and end).
Design consumed: `/fast/scratch/hyaku/mori-r26/MutCaseDesign/mutants.md` §2 (M01–M10).
Harness (mine, scratch only): `/fast/scratch/hyaku/mori-r26/MutToolBatteryA/run_mutants.py`;
raw log `out.txt`; synthetic probe `inputs-truncated-dryrun.json`.

## What I did

* Baseline first, both case files, in the sandbox clone.
* Applied each mutant to `tools/mori-oom-killers.py` **one at a time**, ran the frozen selftest
  (`--selftest`, default file = `tools/fixtures/mori-oom-killers/cases.json`) and the supplementary
  selftest (`--selftest --cases tools/fixtures/mori-oom-killers/cases-supplementary.json`), then
  restored the original bytes and re-checked the sha256. `git status --porcelain` in the clone is
  empty at the end.
* No install, no tool change: the battery needs only `python3` (3.13, system). Nothing was
  installed or upgraded, so there is no tool/version/channel entry beyond that.
* All measurements were taken **inside the sandbox clone** at the specified base
  `16935e24`. The lane working tree `/home/vgpnk/Projects/shokunin/mori-shokunin` was being
  edited concurrently by the integration owner while this battery ran (its
  `tools/mori-oom-killers.py` changed at 11:38 local, i.e. after this seat started and after
  this seat's last mutation run); this seat did not touch it, and the numbers above are therefore
  a measurement of the clone at the specified base, not of the moving lane working tree.

## Baseline (pre-mutation, required to pass first)

```
$ python3 -I -B tools/mori-oom-killers.py --selftest
MORI_OOM_KILLERS_SELFTEST: PASS 32/32   exit 0
$ python3 -I -B tools/mori-oom-killers.py --selftest --cases tools/fixtures/mori-oom-killers/cases-supplementary.json
MORI_OOM_KILLERS_SELFTEST: PASS 32/32   exit 0
```

sha256 of the artefacts under test (sandbox clone):

| File | sha256 |
|---|---|
| `tools/mori-oom-killers.py` (before **and** after every mutant) | `1a71b2dfa45ef547b1a5042cc71a28ae63f54af35d0c4973f6056bf439b2f8e4` |
| `tools/fixtures/mori-oom-killers/cases.json` (counted, 32 cases) | `84d2343f1d672a4597a4ec5efe0fd048eb399e8b4f0f5b86cc483ff8f2e547af` |
| `tools/fixtures/mori-oom-killers/cases-supplementary.json` (32 cases) | `277684eb8f622c2c3eeaf118f65c28d02c0196dd459052aa387989b4fb11269d` |

The case-file digests match the digests the wave-1 design seat recorded
(`mutants.md` §1.1), so the sandbox is on the frozen bytes.

## Detector

D1 = the selftest of one file. **Killed** = the run does not print exactly
`MORI_OOM_KILLERS_SELFTEST: PASS 32/32` with exit 0 (a `FAIL n/32` line or a non-zero exit).
**Survived** = `PASS 32/32`, exit 0. Baseline passed, so no result is inconclusive.

## Result table

| Mutant | Frozen `cases.json` | Supplementary | Frozen kill route (first failing cases) |
|---|---|---|---|
| M01 scope anchor exclusive | **KILLED** `FAIL 12/32` exit 1 (20 cases fail) | **KILLED** `FAIL 14/32` exit 1 | c03 (sigterm 0≠1), c02 (scope_complete false), c09, c13, c14, c15, c16, c17, c18, c19, c20, c21, c22, c23, c24, c26, c28, c10–c12 |
| M02 scope filter deleted | **KILLED** `FAIL 29/32` exit 1 | **KILLED** `FAIL 29/32` exit 1 | c02 (verdict ACTED≠QUIET), c04 (scope_complete true≠false, grammar verified≠unverified), c05 (verdict QUIET≠UNKNOWN) |
| M03 anchor compared in seconds | **KILLED** `FAIL 29/32` exit 1 | **KILLED** `FAIL 29/32` exit 1 | c02, c04, c05 — same routes as M02 |
| M03b line timestamp truncated to seconds (extra probe, see adaptations) | **KILLED** `FAIL 10/32` exit 1 (22 cases) | **KILLED** `FAIL 11/32` exit 1 | c01 (thresholds missing, grammar unverified), c03, c13, c14, c09, c11, c12, c15–c24 |
| M04 threshold announcement counted as an action | **KILLED** `FAIL 29/32` exit 1 | **KILLED** `FAIL 29/32` exit 1 | c01 (sigterm 1≠0, verdict ACTED≠QUIET), c20, c28 (supplementary: c33 instead of c28) |
| M05 oomd notice rule dropped | **KILLED** `FAIL 29/32` exit 1 | **KILLED** `FAIL 29/32` exit 1 | c10 (QUIET≠ACTED), c29, c30 (UNKNOWN≠ACTED) |
| M06 escalation not positive evidence | **KILLED** `FAIL 31/32` exit 1 | **KILLED** `FAIL 30/32` exit 1 | c15 (QUIET≠ACTED); supplementary also kills c34 (UNKNOWN≠ACTED) |
| M07 dry-run treated as positive evidence | **KILLED** `FAIL 31/32` exit 1 | **KILLED** `FAIL 31/32` exit 1 | c18 (verdict ACTED≠QUIET) |
| M07b `or dryrun` added to the acted test (extra probe) | **KILLED** `FAIL 31/32` exit 1 | **KILLED** `FAIL 31/32` exit 1 | c18 |
| **M08 dry-run grammar demands the whole sentence** | **SURVIVED** `PASS 32/32` exit 0 | **SURVIVED** `PASS 32/32` exit 0 | none — see survivor analysis |
| M09 kill-failure line counted as a kill action | **KILLED** `FAIL 31/32` exit 1 | **KILLED** `FAIL 31/32` exit 1 | c16 (kill_failed 0≠1, sigkill 1≠0, ACTED≠QUIET) |
| M10 low-memory warning not counted | **KILLED** `FAIL 31/32` exit 1 | **KILLED** `FAIL 31/32` exit 1 | c17 (low_memory_warnings 0≠2) |

Mutant sha256 (tool file under mutation), all restored byte-exact afterwards:

| Mutant | sha256 of mutated tool | restored |
|---|---|---|
| M01 | `3abeb35640d3a562fcae609440c8a0bb89831b15a19eedf86cf5eec75c314b35` | yes |
| M02 | `67dabc9925df66f02bc7f06fd5f0f93bff8078514922682496522ba57e55871e` | yes |
| M03 | `a115565971aadef79e3ca590a46592282959195560873d4de0a369fa20d66f72` | yes |
| M03b | `cbc6ffcf147c4863061d10fd507c0ca1148510b2236d95c057c7960a68a9b0f8` | yes |
| M04 | `fe8a961f58baf0ca991b7f6f4b6117e6194452468d09162a6f29f1e03534dd5d` | yes |
| M05 | `b159a6493203440c84c0aa44d91e5b04fadbc195e938f3549da3a75803b5872d` | yes |
| M06 | `896e3601974f27e675b0751689aa932db3552eeb8e55b31d9ffc6d6224edf461` | yes |
| M07 | `2464e233ada4e0145ad28e10129ee8a00f8f9ed0e9e54ed3e866a4466b9352a4` | yes |
| M07b | `44a725f45ac7baa84ca25b01b9167cb7b6070d7948a14b1bec6fa668a3fa2573` | yes |
| M08 | `ad2448ee66a677776193428724bd140f9e497358f0fa66393aa9e34bc1f898cf` | yes |
| M09 | `5fb69094283901723640404436d0b0e6c5a0486d8f9a5630d8dbdc16c8099457` | yes |
| M10 | `20fe8881a89805e012fe9558c6ba7e65d1b5cb02baf30298cbb0309603fb6775` | yes |

Restoration evidence: after every mutant the tool file hashed back to
`1a71b2dfa45ef547b1a5042cc71a28ae63f54af35d0c4973f6056bf439b2f8e4` (equal to the "before"
value, recorded per mutant in `out.txt`), and `git status --porcelain` in
`/fast/scratch/hyaku/mori-r26/wt-w2mutA` is empty (no tracked change left behind).

## Adaptations to the landed code shape (design → landed)

The design was written blind (pre-landing); three entries needed a decision. All three are noted
here because they change what the design predicted.

* **M01 — direction inverted.** The design lists "minimal code change: `if ts > anchor:` →
  `if ts >= anchor:`", i.e. it wrote the *fix*; the defect it describes is the exclusive test.
  The landed code is already `>=` (`tools/mori-oom-killers.py:297`), so the mutant applied here is
  the defect direction: `if stamp >= aetm:` → `if stamp > aetm:`. Killed as predicted, but much
  more widely than the design predicted: 20 of 32 frozen cases put a line exactly on the anchor,
  so dropping "at the anchor" also empties the scope for c09–c24 and c26/c28.
* **M03 — the design's arithmetic does not reproduce.** The design's minimal change is
  "`anchor_us // 1_000_000` used as the comparison value", and its *expected output* says in-scope
  lines are dropped. With the frozen anchor 19964362 µs the seconds value is 19, so the mutant
  **widens** the scope (every µs stamp is ≥ 19) instead of narrowing it. I applied the design's
  stated change (`if stamp >= aetm:` → `if stamp >= aetm // 1_000_000:`); it is killed, but by
  c02/c04/c05 (pre-anchor lines wrongly in scope), not by c13/c14 as predicted. As an extra probe
  I also ran the inverse unit confusion (the line timestamp truncated to seconds,
  `if stamp // 1_000_000 >= aetm:`): that is the narrowing variant the design expected, and it is
  killed by c01/c03/c13/c14 as predicted (22 frozen cases fail). Both variants die; the C2 verdict
  does not depend on which one is used.
* **M04 — two hunks, one defect.** The design's defect is "the threshold line is counted as a
  SIGTERM action because the matcher only tests the prefix `sending SIGTERM`". In the landed code
  the threshold line is consumed by the term-threshold branch before the action branch
  (`tools/mori-oom-killers.py:343-345`) and the action regex is `^sending SIGTERM to process `
  (`:108`). Realising the defect therefore needs two hunks: widen `RE_SIGTERM_ACTION` to
  `^sending SIGTERM` and drop the `continue` after the term-threshold match, so the threshold line
  falls through into the action branch. Observable result matches the design: sigterm 1, verdict
  `KILLER_ACTED`.
* **M07 — counter choice.** The design routes the dry-run line into the action-counter branch. The
  landed A6 pass (`tools/mori-oom-killers.py:370-374`) zeroes `sigterm`/`sigkill` after the loop
  whenever `dryrun` is set, so a `sigterm` increment there would be invisible and the designed
  symptom would not appear. The mutant increments `escalations` in the dry-run branch
  (`:360-361`), which reproduces the designed symptom exactly (verdict `KILLER_ACTED`, exit 1,
  `dryrun` still true). I also ran the second realisation M07b (`or dryrun` added to the acted
  test, `:419-423`): also killed by c18.
* **M08 — the design's change is in the fix direction.** The design's minimal change
  ("pattern `^dryrun mode enabled, will not kill anything$` → the contract prefix") would *repair*
  the defect; the landed code already implements the contract prefix
  (`PREFIX_DRYRUN = "dryrun mode enabled"`, `:115`, used with `startswith` at `:360`). To test the
  contract rule at all, the mutant is applied in the defect direction: the constant is tightened to
  the full upstream sentence, so a truncated `dryrun mode enabled` line is no longer recognised.
  This is the mutation the design's "Killing input" describes.

## Survivor analysis

**M08 survived both case files. What it means for the C2 claim.**

* The mutant is live, not a no-op. On a synthetic inputs object carrying the contracted bare
  prefix (`dryrun mode enabled`, no trailing sentence), the pristine tool reports
  `earlyoom.dryrun = true`, the M08 mutant reports `false`:
  `--inputs /fast/scratch/hyaku/mori-r26/MutToolBatteryA/inputs-truncated-dryrun.json` →
  pristine `dryrun= True verdict= KILLERS_QUIET`; mutant `dryrun= False verdict= KILLERS_QUIET`.
* The contract rule is `contract.md:89` — "`dryrun mode enabled` → dry-run flag" — i.e. the
  *prefix* is the rule. The frozen files pin `earlyoom.dryrun = true` only on the full upstream
  sentence (`c18`) and `false` on the plural near-miss (`c23`); no case in either file carries the
  bare prefix. So the counted artifact does not exercise the prefix rule at all, and the
  supplementary file does not either.
* Consequence for C2: **coverage gap, not a defect of the tool.** The landed tool implements
  `contract.md:89` correctly (prefix match at `tools/mori-oom-killers.py:115`/`:360`); what is
  unverified is the *artifact*, not the implementation. The same shape as the A2 rules the design
  seat already listed as uncovered (`mutants.md` §1.2): a rule that no frozen case discriminates
  cannot move the counted `PASS 32/32`. Severity: low (the rule is one constant away from the
  upstream sentence; a future editor who tightens it would not be caught by the frozen battery).
* Note that the two dry-run-relevant cases are *full-sentence* cases, so the design's expectation
  ("expected `dryrun = true`, got `dryrun = false`" at `c18`) does not reproduce: `c18` carries the
  full sentence and the tightened matcher still matches it. The design assumed `c18` held the
  truncated prefix; it does not.

## Supplementary-file discrimination (both files pass on the landed tool)

The supplementary file is not a superset of the counted one and it added kill power here:

| Mutant | cases the supplementary file kills that the counted file does not |
|---|---|
| M06 | `c34` (escalation with no version line: the mutant yields `KILLERS_UNKNOWN`/2 where `KILLER_ACTED`/1 is expected) |
| M04 | `c33` (the counted file's `c28` carries the same threshold lines, so the counted file already covers it) |
| M01, M03b | `c33`, `c34` |

Every mutant that the counted file kills is also killed by the supplementary file; the
supplementary file never lost a kill route. That supports the design seat's §1.1 finding that
neither artifact nests the other.

## Findings and verdicts

1. **The frozen case file detects the scope, grammar, verdict and counter defects it claims to
   cover — holds.** M01–M07, M09 and M10 are killed by the counted file
   (`tools/fixtures/mori-oom-killers/cases.json`), each with a named failing case, and the
   supplementary file kills all of them too. Verdict: **holds** (claim C2, detector D1).
2. **The dry-run prefix rule is uncovered — defect (severity: low, coverage).** M08 survives both
   files while being behaviour-bearing on the contracted bare prefix
   (`contract.md:89` vs. `tools/mori-oom-killers.py:115`/`:360`). This is a gap in the frozen
   artifact, not in the tool. Verdict: **defect (severity: low)** — a coverage finding for the C2
   claim; it does not license changing the contract or the tool.
3. **The design's M01/M03/M08 "minimal code change" lines are not all defect-direction, and M03's
   predicted kill route does not reproduce on the frozen numbers** (see adaptations). Verdict:
   **defect (severity: low, design-document accuracy)** — the wave-1 artefact
   `/fast/scratch/hyaku/mori-r26/MutCaseDesign/mutants.md` should be read with the adaptations
   above; the battery result itself is unaffected.
4. **Nothing else changed.** No lane commit, no ref update, no write outside
   `.ufo/waves/round-26/w2/MutToolBatteryA.md` and the seat scratch directory
   `/fast/scratch/hyaku/mori-r26/MutToolBatteryA/`. No unit was started, stopped or enabled; no
   journal was written; no MESSAGE text, process name, uid or command line is quoted in this
   report (case ids, field paths, counts and the grammar phrases of the contract only).

Report: .ufo/waves/round-26/w2/MutToolBatteryA.md
