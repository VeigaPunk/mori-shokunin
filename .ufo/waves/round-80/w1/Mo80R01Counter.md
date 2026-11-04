# Mo80R01Counter — round 80 w1: adversarial attack on the C1/C3 counters and the instruments they grade

Leaf seat, no subagents, no lane edits, no tool installs (system `python3` + `git` only; nothing
added to PATH). Scratch was `/fast/scratch/hyaku/mori-r80/Mo80R01Counter/`; deleted before this
report (evidence at §8). The lane worktree moved under me while I worked — HEAD went
`57451ecb` (freeze) → `8108dfcc` (build) → `2a826f17` (evidence) → `108ec314` (C1 precision).
Every byte below names the rev/state it was read at.

## 1. What I did (numbered)

1. Read the frozen contract, `controls-r80.txt`, `count-c1.py`, `count-c3.py`, `mutate-c2.py`,
   round-79 `count-c2.py`, the two r79 mutation reports (`Mo79M01Mutant` on the receipt tool,
   `Mo79M02MutantCounter` on the counter), SCORECARD (Axes, capabilities, r79/r80 sections),
   SKILL registry rows 13/14, QUALITY 90/154/159/161–164/165, PROVINCE.
2. Ran `count-c1.py --selftest` and `count-c3.py --selftest` on the frozen bytes (3/3 each,
   rc 0) and again on the amended bytes (4/4 each, rc 0).
3. Independently re-derived the entering controls (item 4 below) — byte-identical to the
   controls receipt, not read from it.
4. Built 11 scratch git fixtures (A1–A5, B1–B6) attacking count-c1/count-c3 verdict paths;
   every fixture repo passed `git rev-parse --show-toplevel` == fixture dir before its first
   commit and used `-c user.name=t -c user.email=t@t`.
5. Attacked the landed sweep: `--selftest` (30/30), full-tree run, run against a `d5888922`
   export, `--scratch` conformance, 4 planted defects, 3 benign plants.
6. Graded all three claims at `HEAD` at three different tips and at `8108dfcc`; checked the
   count-c2 "arms only, hunks inside the selftest region" constraint.

## 2. Findings by severity

### HIGH-1 — C1 was falsified at `2a826f17` by the integration's own LOG append (fixed at `108ec314`; verified)
At `2a826f17` (the evidence commit whose message headlines "C1 met mismatches=0"):
```
$ python3 -I .ufo/waves/round-80/count-c1.py HEAD
C1=unmet tool=present sweep=1 mismatches=1 unresolved=0 tallies=0 stale=1 row_tally=19 live_tally=19 rev=2a826f17b16c
rc=1
$ python3 -I tools/mori-claim-sweep.py --root .
CLAIM_SWEEP_MISMATCH stale LOG.md:4919 'selftest 18 in-memory cases'
CLAIM_SWEEP mismatches=1 unresolved=0 tallies=0 stale=1 carriers=4 pointers=233
rc=1
```
Cause: the LOG Round 80 section appended by `2a826f17` quotes the retired literal
(`…the control-receipt capabilities row's \`selftest 18 in-memory cases\` (live 19) is
corrected…`, LOG.md:4919); the pins freeze that literal as stale over all four carriers
including append-only LOG.md. The committed `after-r80.txt` itself carries the red sweep bytes
directly under its green `count-c1 8108dfcc` line — internally honest, headline wrong at tip.
The receipt's manual check `grep -c 'selftest 18 in-memory cases' SCORECARD.md → 0` only
covered SCORECARD, not LOG.md. At `8108dfcc` (pre-append) the same command read
`C1=met … mismatches=0 … rc=0`. The L1 fixed it in `108ec314` (LOG.md, 1 line) and my rerun at
the tip reads `C1=met … rev=108ec314258b rc=0`. Residual risk class: any future append to
LOG.md/SKILL.md quoting a pinned stale literal re-reds the gate with no in-place repair path.

### HIGH-2 — P-C1's second conjunct (red at `d5888922`) has no code path in count-c1.py (open at tip)
The contract's P-C1 is two conjuncts: sweep green at R **and** "the same sweep at the entering
revision `d5888922` finds at least one mismatch, the named one being SCORECARD's `18` vs live
`19`". count-c1.py implements only the first:
- `grep -n 'd5888922' .ufo/waves/round-80/count-c1.py` → line 10 only (the docstring's own
  restatement of the predicate); `grade()` exports one rev, runs the sweep once, and `met` is
  `rc==0 and mismatches==0 and unresolved==0 and tallies==0 and stale==0 and stated==live`.
- At `d5888922` the counter reports `C1=unmet tool=absent sweep=- mismatches=- …` — right
  verdict, wrong reason; the anti-vacuity arm is never executed. A sweep that prints
  `mismatches=0 unresolved=0 tallies=0 stale=0` unconditionally (checks nothing) grades
  `C1=met` (fixture A1 below).
- I ran the missing arm by hand; it is satisfiable and currently true:
```
$ git -C <lane> archive d5888922 | tar -x -C <scratch>/export-d588
$ python3 -I tools/mori-claim-sweep.py --root <scratch>/export-d588 --pins <lane>/.ufo/waves/round-80/claim-pins.json
CLAIM_SWEEP_MISMATCH stale SCORECARD.md:4016 'selftest 18 in-memory cases'
CLAIM_SWEEP mismatches=1 unresolved=0 tallies=0 stale=1 carriers=4 pointers=228
rc=1
```
Per QUALITY 154 ("the contract target, counter condition and receipt label must name the same
predicate and output") the receipt label `C1=met` does not certify the full P-C1 sentence.
Fixture A1 (stub sweep printing the all-zero summary, exit 0, row 19/19):
`[A1_vacuous_green_sweep] rc=0 :: C1=met tool=present sweep=0 … rev=761a242a1804`.

### MEDIUM-3 — all three frozen counters were amended post-freeze, pre-grading (adjudicate)
`57451ecb` froze them; `8108dfcc` modified all three (git diff `57451ecb..8108dfcc`):
count-c1 `met` gained `unresolved==0 and tallies==0 and stale==0` plus a 4th selftest arm;
count-c3 gained selftest arm `sibling_and_directory_ignored`; mutate-c2 gained an unmutated
baseline run (rc 2 if not green) and appended `unmutated=green` to the receipt line:
`MUTATION_C2 survivors=0 killed=6 total=6 unmutated=green rev=…`. The contract spells the P-C2
receipt as `MUTATION_C2 survivors=S killed=K total=6`; the token is an appendix to the frozen
grammar (the pre-existing `rev=` suffix makes this a prefix-convention call — flagged for the
L1 to adjudicate, not scored as a violation). The amendments improve detection; they were made
after the freeze and before the graded run.

### MEDIUM-4 — mutate-c2.py docstring entering restatement is false (open at tip)
Docstring lines 9-10: "At the entering revision the same harness prints
`survivors=3 killed=3 total=6`." Measured on the same bytes (amended, at `d5888922` and at
HEAD): `MUTATION_C2 survivors=2 killed=4 total=6 …`. The contract P-C2 says survivors=2 and
resolves the 3-vs-2 conflict in the harness's favor; the docstring asserts the superseded
number as the harness's own output. The 3 refers to Mo79M02's survivors (M1 admission filter,
M4 clause boundary, M5 round search); the frozen `any_round_in_cell` mutant text kills M5's
shape, so only 2 survive. No graded impact; documentation-identity defect.

### MEDIUM-5 — count-c3.py docstring entering restatement is false (open at tip)
Docstring: "At the entering revision it prints `C3=unmet named=15 present=55 missing=40` rc 1."
Measured (frozen bytes, by me; contract and controls agree): `C3=unmet named=14 present=55
missing=41 extra=0 rev=d58889220d3c rc=1`. No graded impact; same class as MEDIUM-4.

### MEDIUM-6 — count-c3 TOKEN has no left boundary: `<dir>/tools/<name>` counts as naming (open; fixture B1)
```
[B1_subdir_path_counts_as_naming] rc=0 :: C3=met named=3 present=3 missing=0 extra=0 rev=3b0dbd5903af
```
PROVINCE named the instrument only as `` `corpus/tools/mori-census.sh` `` and the counter read
C3=met. The contract's sibling rule excludes `*-shokunin/` paths but says nothing that makes
`corpus/tools/…` a lane-instrument naming. The same wave's sweep POINTER regex
(`(?<![\w./-])(?:corpus|tools|\.ufo)/`) does have the boundary — two same-wave instruments,
two different conventions for "names a tool". The landed inventory uses plain `tools/…` rows so
the landed verdict is unaffected (`C3=met named=56 present=56` at tip), but the counter can be
greened by cross-directory mentions. Mo79/r80 mutation routes covered `../tsukuroi-shokunin/…`
and a `tools/fake-dir.py` directory; this third shape is uncovered.

### MEDIUM-7 — count-c1 trusts the summary against its own MISMATCH lines and against repeated summaries (open; fixtures A2/A3)
```
[A2_mismatch_line_vs_zero_summary] rc=0 :: C1=met … rev=1e7adc439c2c
[A3_second_contradicting_summary] rc=0 :: C1=met … rev=36bafcbce3aa
```
A2: a sweep printing `CLAIM_SWEEP_MISMATCH tally … pinned=19 live=20` followed by an all-zero
summary and exit 0 grades met — the kill rule "any mismatch … is `C1=unmet`" is implemented as
"the summary's `mismatches=` field says 0". A3: with two contradicting `CLAIM_SWEEP` lines and
exit 0, `re.search` reads the first. The amended `inconsistent_summary` selftest arm covers a
single summary with `stale=1`; neither shape above is exercised. Adjacent to Mo80M01Mutant's
survivor `C1f_count_unresolved_only` (sweep-side, routed to round 81); these are the
counter-side exposures and remain even with a correct sweep.

### MEDIUM-8 — count-c1 row_tally reads only the first matching row (open; fixture A4)
```
[A4_second_row_stale_18] rc=0 :: C1=met … row_tally=19 live_tally=19 rev=dc94681eac63
```
Two capabilities rows naming `tools/mori-control-receipt.py` (19 then 18): the counter grades
the first, a stale second row is invisible to it. The real sweep's stale literal covers the
exact phrase `"selftest 18 in-memory cases"`, so the landed bytes are safe; a reworded stale
row (e.g. `18-case in-memory selftest`) passes both.

### LOW-9 — sweep rejects `--scratch` although the frozen interface honours it (open)
Spec: "no `/tmp` path of its own; honours `TMPDIR`/`--scratch` for any child work dir."
```
$ python3 -I tools/mori-claim-sweep.py --root . --scratch <dir>
CLAIM_SWEEP_SETUP unknown option: --scratch   (rc 2)
```
TMPDIR is honoured by inheritance; the counter passes only `--root/--pins`, so grading is
unaffected. Frozen-interface conformance gap.

### LOW-10 — count-c1 export interpolates the repo path into a shell string (open; fixture A5)
`export()` runs `f"git -C {repo} archive {rev} | tar -x -C {dest}"` with `shell=True`:
```
[A5_repo_path_with_space] rc=2 :: C1_SETUP archive failed rev=92d1d6ff7fa2
```
A repo path containing a space degrades to setup rc 2 (fails safe). The lane path has no
spaces today; robustness only.

### LOW-11 — count-c3 sibling exclusion also excludes the lane's own prefixed path (open; fixture B2)
```
[B2_own_lane_prefix_excluded] rc=1 :: C3=unmet named=2 present=3 missing=1 extra=0 … missing_first=mori-census.sh
```
`mori-shokunin/tools/mori-census.sh` is excluded by the same `*-shokunin/` lookbehind meant
for siblings. Deviates from the sentence (which excludes sibling lanes' paths) in the safe
direction. True siblings are correctly excluded (B3: `kata-shokunin/…` → unmet, expected).

### LOW-12 — a named `tools/<name>.py` that exists only as a directory counts as `extra` (open; fixture B6)
```
[B6_dot_py_directory] rc=1 :: C3=unmet named=3 present=3 missing=1 extra=1 … extra_first=pkg.py
```
The sentence "every named path exists at R" is ambiguous for directories; the counter fails
safe. Partially covered by the r80-routed `sibling_and_directory_ignored` arm on the tree side.

### INFO (no counter/instrument defect)
- B4 trailing colon `` `tools/mori-census.sh:` `` → counted as named → met. Predicate-conforming.
- B5 all names inside one fenced block → met. The predicate grades basenames only, so a bare
  filename dump greens C3 while the deliverable's class/registry/purpose richness is graded by
  no counter. Predicate-vs-deliverable gap to keep in mind; not a code defect.
- C8 unparseable pinned selftest (`print('banana')`, rc 0) → `CLAIM_SWEEP_SETUP unparseable or
  conflicting selftest counts`, rc 2 — a setup error, never a pass. Spec-conformant.
- count-c2 arms-only constraint PASSES: `git diff d5888922..HEAD -- .ufo/waves/round-79/count-c2.py`
  is one hunk, `@@ -159,6 +159,22 @@ def selfcheck(scratch)` (selfcheck spans 141-200, main
  starts at 201); predicate/CLI/output grammar untouched.
- Sweep selftest `CLAIM_SWEEP_SELFTEST pass=30 fail=0` rc 0 (matches SKILL row 14's "30 arms").
- Planted defects are caught: dead pointer in a capabilities row (`unresolved SCORECARD.md:4056
  tools/ghost.py`), tally pin 18 vs live 19 (`tally … pinned=18 live=19`), planted stale literal
  and live checklist ghost in SHONEN (`stale SHONEN.md:10`, `unresolved SHONEN.md:11`).
- Benign plants stay green: `` `tools/mori-control-receipt.py:12-14` `` in a graded row resolves
  (suffix stripping); a fenced `tools/ghost.py` in SHONEN is ignored. (The only red in that run
  was HIGH-1's pre-existing LOG.md hit, unrelated to the plants.)

## 3. Predicate identity (item 3)

| Claim | Contract sentence | Counter/harness code path | Receipt label | Identity |
|---|---|---|---|---|
| P-C1 | Two conjuncts: green at R; red at `d5888922` with the named 18-vs-19 mismatch | Only conjunct 1 (plus an independent row-tally arm); no `d5888922` path (HIGH-2) | `C1=met\|unmet tool= sweep= mismatches= unresolved= tallies= stale= row_tally= live_tally= rev=` | GAP — receipt cannot certify conjunct 2 (QUALITY 154 class) |
| P-C2 | Six frozen mutants on a scratch copy of round-79 count-c2.py at R; `MUTATION_C2 survivors=0 killed=6 total=6`, rc 0; entering survivors=2 | `MUTANTS` (6) applied one at a time to pristine text; selftest per mutant; rc 0 iff survivors=0; entering measured survivors=2 | `MUTATION_C2 survivors=S killed=K total=6 unmutated=green rev=` | MATCH on logic and numbers; label carries one appendix token (MEDIUM-3); docstring entering restatement false (MEDIUM-4) |
| P-C3 | PROVINCE's `tools/*.py\|*.sh` basenames ⊇ ls-tree paths of that shape at R, and every named path exists; entering named=14 present=55 missing=41 extra=0 | `TOKEN` regex over all of PROVINCE.md (incl. fenced, incl. `<dir>/tools/`), sibling lookbehind `*-shokunin/`, extra = named−present | `C3=met\|unmet named=N present=M missing=K extra=E rev=` | MATCH on numbers; grammar wider than the sentence on left boundary (MEDIUM-6) and sibling own-prefix (LOW-11); docstring entering restatement false (MEDIUM-5) |

## 4. Independent re-derivation (item 4)

Frozen bytes, run by me (not read from the controls receipt):
```
$ python3 -I .ufo/waves/round-80/mutate-c2.py --rev d5888922
mutant drop_admitted survived rc=0 C2_COUNTER_SELFTEST pass=4 fail=0
mutant raise_ceiling killed rc=1 C2_COUNTER_SELFTEST pass=3 fail=1
mutant count_other_verdicts killed rc=1 C2_COUNTER_SELFTEST pass=3 fail=1
mutant cut_clause_boundary survived rc=0 C2_COUNTER_SELFTEST pass=4 fail=0
mutant any_round_in_cell killed rc=1 C2_COUNTER_SELFTEST pass=3 fail=1
mutant met_ignores_mismatch killed rc=1 C2_COUNTER_SELFTEST pass=1 fail=3
MUTATION_C2 survivors=2 killed=4 total=6 rev=d58889220d3c
rc=1
$ python3 -I .ufo/waves/round-80/count-c3.py d5888922
C3=unmet named=14 present=55 missing=41 extra=0 rev=d58889220d3c
missing_first=mori-anchor-check.py,mori-blind-check.sh,mori-cgroup-pressure.py,mori-content-review.py,mori-control-receipt.py,mori-counter-win.py,mori-disk-rate.py,mori-drift-adjudicate.py
rc=1
```
Both byte-identical to `controls-r80.txt`. Corroborations on amended/landed bytes:
`sha256(d5888922:.ufo/waves/round-79/count-c2.py) = fed9a829…` matches Mo79M02's pristine
counter hash exactly. At tip `108ec314`: `C1=met … rc=0`; `MUTATION_C2 survivors=0 killed=6
total=6 unmutated=green rc=0`; `C3=met named=56 present=56 missing=0 extra=0 rc=0`.

## 5. Fixtures built (all under scratch, all deleted)

Git fixtures with `-c user.name=t -c user.email=t@t`, toplevel asserted before first commit:
A1/A2/A3 (stub sweeps with vacuous-green, mismatch-line-vs-zero-summary, double-summary
shapes + SCORECARD row 19 + stub CAPTOOL 19 + empty pins); A4 (two CAPTOOL rows 19/18);
A5 (repo path `…/spa ce/r`); B1–B4 (PROVINCE naming via `corpus/tools/…`, own-lane prefix,
true sibling, trailing colon over 3-tool trees); B5 (fenced filename dump); B6 (`tools/pkg.py`
directory plus its `__init__.py`). Sweep probe trees: full worktree copies (`.git`,
`.scratch`, `.ufo/state`, `.ufo/watchdog.log` excluded) with fresh-copy-before-mutate
discipline; plants per §2. Entering export: `git archive d5888922 | tar -x` into scratch.

## 6. What I could not verify

- Whether the L1 intends the `unmutated=green` receipt token to be inside the frozen P-C2
  grammar (MEDIUM-3) — adjudication, not measurement.
- Whether any future LOG/SKILL append will re-quote pinned literals (HIGH-1 residual) — the
  gate would catch it red, which is the designed behavior; the repair path (append-only file)
  is the costly part.
- count-c1 at a hypothetical future rev where the sweep is vacuously green — structurally
  untestable until HIGH-2 is routed (that is the finding).

## 7. Own defects (what I got wrong and how I caught it)

1. First probe-tree copies omitted `corpus/` → 227 unrelated unresolved pointers drowned the
   planted-defect signals. Caught by designing C0 as a clean baseline; fixed with full-tree
   copies in driver 2.
2. Driver 2 used `cp -al` hardlinks and overwrote `tools/mori-control-receipt.py` in place in
   tree8, truncating the shared inode — tree0, tree9 and the c1repo fixture silently inherited
   a `print('banana')` stub, invalidating that run's C8/C9/F1. Caught because C9 returned the
   C8-shaped setup error; fixed in driver 3 with remove-then-fresh-copy before every mutation.
3. An early `grep -c … || echo FILE-ABSENT` loop conflated "no match" (rc 1, prints 0) with
   "file absent"; re-read the output as `0` per carrier.
4. My first `git status` showed SCORECARD.md clean and my grep minutes later showed the
   corrected 19 row — a sibling seat edited the shared worktree between my calls. Caught by
   re-running status; from then on every claim in this report is pinned to a rev.
5. Initial `head -40` on a SCORECARD grep buried the `selftest 18` matches under `## ` heading
   noise; re-ran with a targeted pattern before drawing any conclusion.

## 8. Scratch cleanup

`rm -rf -- /fast/scratch/hyaku/mori-r80/Mo80R01Counter && test ! -e …` →
`SCRATCH_CLEANUP absent rc=0`. No tree left on disk; nothing written outside the seat-specified
report path, the scratch dir, and counter-owned temp dirs under it.
