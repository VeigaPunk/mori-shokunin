# Mo87C01Critic — cheap-path attack on the two frozen r87 claims

seat: `Mo87C01Critic` · round 87, wave w1 · date 2026-11-04
mode: detection and report only. **No lane file outside this report path was created, edited,
moved or deleted by this seat.** No commit, push, checkout, reset, stash or mutating `jj`/`git`
command ran in the lane. Every fixture lived under
`/fast/scratch/hyaku/mori-r87/Mo87C01Critic/` (a `git clone --shared` or a fresh `git init` per
fixture, commits `-c user.name=t -c user.email=t@t`), and that directory was removed before yield.
No tool was installed or upgraded.

**This report is arriving late in the wave, after several sibling findings landed.** §4 reconciles
every path below against what was already filed; the C2 post-data erratum E1 (contract blob
`57c9f32f…`, not present at the freeze) already covers part of my baseline measurement. Nothing
below is restated as new where a sibling measured it first.

## 0. Authority actually read, with hashes

Lane HEAD moved four times while this seat ran
(`98f48dba` → `b9e6f68d` → `a90126ef` → `22fa2919` → `6056d001`); the tracked worktree was clean
each time (the only tracked modifications at the end are my own report and a sibling's). Graded
revisions are immutable, so every reading is from the object database (`git show <rev>:<path>`),
never from a worktree copy. The three graded blobs below are identical at `22fa2919` and
`6056d001`.

| file | blob at freeze `142542e0` | blob at `98f48dba` | blob at HEAD `6056d001` | sha256 read |
|---|---|---|---|---|
| `.ufo/waves/round-87/count-c1.py` | `f99f1e87…` | `f99f1e87…` | `f99f1e87…` | `e2ff9687…2c266e` |
| `.ufo/waves/round-87/count-c2.py` | `073276ee…` | `073276ee…` | `269842f7…` | pre-A1 `e1dfd45a…b2316d`; A1 `264a43f0…236b14d` |
| `.ufo/waves/round-87/contract.md` | `648dffbf…` | `648dffbf…` | `57c9f32f…` (adds E1) | freeze `f28d75a7…905c40`; E1 `afa154ff…22e11a` |

`git diff 142542e0 98f48dba -- count-c1.py count-c2.py contract.md` is empty, so the freeze blobs
are the claim blobs. A1 (`SUBJECT_ARMS 11 → 13`, two labels) landed at `b9e6f68d`, **one commit
after the C2 claim commit**; erratum E1 at `22fa2919` corrects the reading to "counter bytes at
`b9e6f68d` over C2 subject `98f48dba`" and corrects A1's timing sentence.

Also read: `evidence/controls-r87.txt`, `evidence/probe-r87.txt`,
`corpus/lessons/round-86-verifier-spotcheck.md` `## Routed defects` (eight items), `SCORECARD.md`'s
round-87 and planned-88 sections, and (for reconciliation only) `w1/Mo87R01ReviewC1.md`,
`w1/Mo87R02ReviewC2.md`, `w1/Mo87E02C2Supersede.md`, `w1/Mo87M01Mut.md`.

## 1. Baselines — do the frozen targets reproduce?

| # | command | exact line | rc |
|---|---|---|---|
| B1 | `<freeze>/count-c1.py 03b66a43 --repo <lane>` | `C1=met mutants=6 killed=6 survivors=0 total=6 arms=54` | 0 |
| B2 | same at `6fc09d69` | `C1=unmet mutants=6 killed=0 survivors=6 total=6 arms=48` | 1 |
| B3 | `<A1>/count-c2.py 98f48dba --repo <lane>` | the frozen `C2=met … superseded=2 legacy=1 unexpected=0` line | 0 |
| B4 | `<freeze>/count-c2.py 98f48dba` (**counter at R**) | `C2=unmet … subject=selftest arms=(13, 0) labels=True` | **1** |
| B5 | `<A1>/count-c2.py 6fc09d69` | `C2=unmet subject=stub missing=summary_required,binding_required` | 1 |
| B6 | `<freeze>/count-c2.py 6fc09d69` | `C2=unmet receipts=5 absent=2 bindings=7 bound=7 … superseded=0 legacy=3` (the frozen control) | 1 |

B1/B2 reproduce the frozen C1 target and entering control. B3 reproduces the frozen C2 target with
the A1 blob (erratum E1's canonical form). B4 is E1's F1 in my own measurement. **B5/B6 are the
part E1 does not close:** the A1 blob no longer prints the frozen C2 entering control, and the
pre-A1 blob does not print the after line — so the before and after values of C2 are produced by
different detector blobs, and `controls-r87.txt` (which names "the worktree" counter) is stale
against the counter now on disk. Measured, not inferred.

## 2. C1 — paths to `C1=met mutants=6 killed=6 survivors=0 total=6 arms=54`

### P1 — the exact predicate command, from a fabricated repo (MEASURED: target, rc 0)

The predicate is written as `python3 -I .ufo/waves/round-87/count-c1.py R` and carries no `--repo`.
`main()` derives its repo from `__file__` (`abspath(dirname(__file__)/../../..)`), so a repo that
contains the counter at the same path grades *itself*.

Fixture: a fresh `git init` repo (toplevel asserted equal to the fixture before the first commit)
carrying three subjects at the r86 paths. Each subject is a text-integrity puppet:

```python
import base64, os, sys
SRC = open(os.path.abspath(__file__), encoding="utf-8").read()
WANT = [base64.b64decode(x).decode() for x in (<b64 of its anchors>)]
if [w for w in WANT if SRC.count(w) != 1]:
    print("PUPPET_SELFTEST pass=0 fail=1"); sys.exit(1)
print("C1_COUNTER_SELFTEST pass=18 fail=0")      # 13 / 23 in the other two files
sys.exit(0)
# the anchors as comments: the only thing checked is that this text is still present
```

The frozen `MUTANTS` `old` strings were copied verbatim from the counter (never retyped). The
frozen `count-c1.py` was then copied to `.ufo/waves/round-87/count-c1.py` in that repo and the
**exact** predicate command run with cwd = that repo, no flags:

```
C1=met mutants=6 killed=6 survivors=0 total=6 arms=54 rev=47864243ad77      rc=0
```

Six arms total (one text-presence check per mutant), not 54; no clause of any r86 counter runs;
the tallies 18/13/23 are printed literals. The same fixture also reaches the line through
`--repo <puppet>` (rev `5aa7d18c`), and `w1/Mo87M01Mut.md` records that it did **not** mutate "the
`--repo` default", so this path is not one of its survivors.

### P2 — `arms=54` from three subjects that assert nothing (MEASURED: yes)

`arms_total` sums `arms_of(out)[0]`, which the subject prints about itself. `arms_of` returns the
**last** `COUNTER_SELFTEST pass=(\d+) fail=(\d+)` in the output; measured parser behaviour:
`arms_of("…C1_COUNTER_SELFTEST pass=18 fail=0\nEXTRA COUNTER_SELFTEST pass=99 fail=0") == (99, 0)`.
Nothing ties the printed count to the number of assertions. P1 is the end-to-end composition of
this (see §4 for the sibling finding that covers the same mechanism differently).

### P3 — the kill rule accepts a pure syntax break (MEASURED: killed, `met=true`)

Scored with the frozen counter's own `grade()` against the real subject at `03b66a43`:

```
old="def arms_of(out):"  new="def arms_of(out)"   (no colon)
-> MUTANT count-c1.py X-syntax-break killed rc=1
-> tail mutants=1 killed=1 survivors=0 total=1 arms=18   met=true
```

`killed()` is `rc != 0 or FAIL.search(out)`. A `SyntaxError`, `NameError`, missing import or any
other crash is indistinguishable from an arm catching behaviour. Two further channels, both
measured: `killed(0, "note: fail=1") is True` (a string in output kills a green run), and
`killed(124, "timeout") is True` (`selftest_run` maps `TimeoutExpired` to rc 124, so a hang is a
kill). `w1/Mo87R01ReviewC1.md` finding 6 records the *same rule openness* and that no frozen kill
was a crash; P3 is the constructive measurement it did not run.

### P4 — editing `TARGET`/`TARGET_ARMS` (MEASURED: blocked by the detector's own selftest)

A scratch copy with `TARGET=(0,6,6)`, `TARGET_ARMS=48` and `survivors == 0 → survivors == 6`, run
at the entering revision, prints `C1=unmet … detector=red` rc 1; also rewriting the tail prints
`C1=unmet … detector=red`. The `selfcheck` arms `target_split_ok`, `target_split_free`,
`target_arms_free`, `per_file_arms_frozen` pin the constants and `main()` runs that selftest in the
same invocation. A rewrite that also rewrites those arms can print anything — so the residual
requirement is a **blob pin** (§6), not a wording check.

### P5 — pointing it at a different subject

Same mechanism as P1. No extra flag is needed: the repo is `__file__`-relative, so the counter's
location *is* the subject's location.

### 2.6 — what C1 actually gets right (independent attribution)

Each pristine and mutated real subject at `03b66a43`, run directly:

| subject | pristine | mutant | failing arm | traceback |
|---|---|---|---|---|
| `count-c1.py` | `pass=18 fail=0` | M1 | `unanchored_plus_killed_unmet` | no |
| `count-c1.py` | | M2 | `zero_mutants_unmet` | no |
| `count-c1.py` | | M3 | `arms_tally_from_subject` | no |
| `count-c2.py` | `pass=13 fail=0` | M4 | `summary_required` | no |
| `count-c2.py` | | M5 | `binding_required` | no |
| `count-c3.py` | `pass=23 fail=0` | M6 | `derive_keyshape` | no |

Each mutant fails exactly one arm, that arm is the one the commit added for it, and it calls the
graded function. **C1's substance is sound at the named revision**; P1–P3 are gate weaknesses, not
a live falsification of the after-value.

## 3. C2 — paths to `superseded=2 legacy=1` with the rest of the frozen tail

### P6 — a vacuous successor retires a legacy receipt (MEASURED: target, rc 0) — reproduction

Fixture at `98f48dba`: replace the record successor's `# cmd:` with `echo RECORD_SWEEP` and its
body with `RECORD_SWEEP`; keep its genuine `# counter-sha256:` line, `# rev:`, `# replay: clone`,
`# supersedes:` and `# limits:`.

```
REPLAY record-sweep-r87.txt mode=clone rc=0 exported=1
C2=met … replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=e8a0c89133f7   rc=0
```

This is the same defect class as `w1/Mo87R02ReviewC2.md` **F2** (`printf '<body>'`); I reproduced it
independently with a different command before reading that report. Not new.

Stronger form, full from-entering path: at `6fc09d69`, import **only**
`.ufo/waves/round-86/count-c2.py` from `03b66a43` (C1's subject edit — see P10), install the A1
`count-c2.py` at its path, and add two receipts whose command and body are `echo RECORD_SWEEP` /
`RECORD_SWEEP` and `echo CLAIM_SWEEP` / `CLAIM_SWEEP` (each keeping a real binding line, `rev
25a74d4c`, `# replay: clone`, the right `# supersedes:` and a three-word `# limits:`). The **exact
predicate command**, no flags, cwd = fixture:

```
C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4
matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=595be4acb035      rc=0
```

No sweep ran, no legacy receipt was replayed, no digest was recomputed. `# limits:` only needs
"limit" and three words; `exported` is hard-coded to 1 in clone mode, so an `exported>=1` check
would not catch this — the check must be "the command names committed bytes".

### P7 — supersession by two header lines on already-clean receipts, no new receipt, no new replay (MEASURED: target, rc 0) — **not in the filed lists**

Fixture at `98f48dba`: append `# supersedes: record-sweep-r85.txt` to `after-r85.txt` and
`# supersedes: claim-sweep-r85.txt` to `after-c1-r86.txt`. Nothing else changes.

```
C2=met … replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=7efdfb602d78   rc=0
```

`replay=4` is unchanged: no fifth replay exists, and neither legacy body is reproduced. The
superseder for `record-sweep-r85` is `after-r85.txt` — **the receipt the contract itself declares
unreproducible**. `supersede_verdict` only needs `name in clean_names and target == legacy_name`,
and `clean_names` includes legacy receipts. The frozen header-only control blocks a *fabricated
successor*; it does not block an existing clean receipt becoming a superseder.

This differs from the paths already filed:
- R02 F2 / E02 fixture 5 both create **new** counterfeit successors and remove/alter headers; P7
  adds no receipt and removes nothing.
- R02 F4 adds `# replay: clone` to a legacy row to inflate the replay tally; P7 adds `supersedes`.

### P8 — a receipt may supersede itself (MEASURED: counts) — **not in the filed lists**

`# supersedes: after-r85.txt` added to `after-r85.txt` (plus one real link) reads
`superseded=3 legacy=0` rc 1. `supersede_verdict` never checks `target != name`. Alone it
overshoots the target, so it is a rule hole rather than a target path; P7 is the target path.

### P9 — is `legacy=1` the honest count? (MEASURED: not under the natural reading)

Replaying each legacy receipt's own `# cmd:` in a `--shared` clone at its own `# rev: 25a74d4c`:

| receipt | recorded body | replayed | verdict |
|---|---|---|---|
| `after-r85.txt` | C1 line + `C3=met … subject_deltas=0 … detector=green` + two `rc=0` lines | C1 matches; C3 reads `C3=unmet observed=3 aa=stable subject=unmet`; the `rc=0` lines are not printed by either counter; an extra `C2=unmet …` line appears | **fails** |
| `record-sweep-r85.txt` | sweep line + `rc=0` | the sweep line only | **fails as-cmd'd** |
| `claim-sweep-r85.txt` | `… pointers=274` + `rc=0` | `… pointers=266` | **fails** (stale) |

All three legacy receipts fail to replay as written; `legacy=1` is `3 − superseded 2`, i.e. the
number of legacy receipts that **no clean receipt names**, not the number that fail to replay. The
r87 successors' `# limits:` text is honest about this. R02 Attack 4 measured the `after-r85` case
independently (including the harness-written `rc=0` lines); the sweep rows are my addition.

### P10 — C2 reads C1's work, so the contract's separability sentence is false (MEASURED)

The contract says "Two claims … Neither reads the other's work." The C2 counter's subject sub-gate
reads `.ufo/waves/round-86/count-c2.py` and requires 13 arms plus `summary_required` and
`binding_required` — all introduced by C1's `03b66a43`. Same fixture, with and without that one
file:

```
without:  C2=unmet subject=stub missing=summary_required,binding_required        rc 1
with:     C2=met   … the full frozen tail                                        rc 0
```

A1/E1 disclose the dependency, but the frozen separability sentence was never qualified, and the
dependency is one-way (C1 never reads a receipt).

### P11 — the counter at R does not print R (MEASURED; covered by E1)

B4/B5/B6. E1 already states the canonical form (counter `b9e6f68d` over subject `98f48dba`) and
corrects A1's timing; B3 is exactly that form and I reproduced it. **Residual not covered by E1:**
the frozen `controls-r87.txt` §C2 is reproducible only by the pre-A1 blob, and the A1 blob prints a
different (earlier) failure at entering. Before and after therefore come from different detector
blobs, and the controls receipt names a counter version that no longer exists on disk.

## 4. Reconciliation — what was already filed, what is new here

| path | status | first filed by |
|---|---|---|
| P1 exact command from a fabricated repo | **new end-to-end** (mechanism adjacent to R01 f1 "tally-only"); M01 did not mutate `--repo` | this seat |
| P2 printed tally trusted / last-match parsing | mechanism filed | R01 f1; M01 rank 21 (`c1-arms-first`) |
| P3 kill rule accepts crash / `fail=` / timeout | rule openness noted, constructive measurement new | R01 f6 |
| P4 `TARGET`/`TARGET_ARMS` edit blocked | corroboration | R01 control 3 |
| P6 vacuous successor | reproduction (different command) | R02 F2; E02 fixture 5 is the sibling acid test |
| P7 existing-clean-receipt superseder, incl. the unreplayable `after-r85` | **new** | this seat |
| P8 self-supersession | **new** | this seat |
| P9 `legacy=1` counts un-named, not unreplayable | new sweep rows; `after-r85` row independently measured | R02 Attack 4 (after-r85 only) |
| P10 C2 depends on C1 | **new framing**; dependency disclosed | A1/E1 (disclosure only) |
| P11 counter at R vs E1 | reproduction; **controls-blob residual new** | R02 F1 / E1 |

The SCORECARD's `## Planned (round 88)` names three C2 counterfeit paths — stripped `# replay:`
header (E02 fixture 5), vacuous `# cmd:` (R02 F2), `supersede_absent_target` ambiguity. **P7 and P8
are not among them.** If a report I did not read covers them, the L1 should merge rather than
double-count.

## 5. Impacted axes

**operability (C1, score 7).** The after-value is true at the named revision and all six kills are
attributable to the six new behaviour arms, so the arm work is earned. What is not established is
the capability sentence: the counter cannot tell a behaviour arm from a text-presence arm, counts a
crash or a timeout as a kill, trusts the subject's printed tally, and grades whichever repo the
counter file sits in. P1 reaches the exact frozen line with six arms that assert nothing. Bank the
arms; do not bank the gate.

**calibration (C2, score 5, tied lowest).** Directly hit. `superseded` is a naming count satisfiable
with two header lines on already-clean receipts (P7), with a successor whose "replay" is
`echo TOKEN` (P6), and with a receipt naming itself (P8); `legacy=1` counts un-named legacy rows
while all three legacy receipts fail to replay (P9); the before/after pair uses two detector blobs
(B6/B3); and the claim is not separable from C1 (P10). The numeric target is honest for the
*submitted* receipts, but it does not certify that any legacy receipt was reproduced — which is the
axis the round claims to move.

**depth / freshness.** Not measured by this seat; no finding.

## 6. Smallest safe corrections

Marked **[routed]** where already in `## Planned (round 88)`, **[open]** where not.

C1:

1. **Blob pin.** Put the counter's sha256 (`e2ff9687…` for count-c1; `264a43f0…` for count-c2) in
   the frozen predicate and the running receipt; a judge runs the pinned blob. **[open]**
2. **Repo pin.** In `main()`, after `rev-parse --show-toplevel`, require the repo to equal the
   toplevel derived from `__file__`, or forbid `--repo` in the graded command. P1 closes. **[open]**
3. **Attributed kills.** Require the mutated output to contain `FAIL <label>` with `label` in a
   frozen per-mutant set, and require the mutated file to compile before running. Turns "rc != 0"
   into "an arm caught it"; closes P3 and the `fail=`/timeout channels. **[open]**
4. **Structural tally.** Count `^PASS ` lines in the subject's selftest output and require it to
   equal the printed `pass`; otherwise `arms=54` stays a self-report. **[open as an item; mechanism
   in R01 f1]**

C2:

5. **A superseder must replay and must not be itself.** Require the naming receipt's population
   mode to be `clone`/`required` with a successful replay, and reject `target == name`. Kills P7
   and P8. **[open]**
6. **The command must name committed bytes.** Require the successor's `cmd` to contain at least one
   pathish token that exists at its `# rev:`; in `required` mode require `exported >= 1`. Closes
   P6 and the `printf` form. **[routed — planned-88 2(b)]**
7. **Bind the legacy body.** Require the successor to carry the superseded receipt's body digest at
   the legacy's own `# rev:` and to emit it on replay. `legacy` then means "not reproduced", which
   is what the axis claims. **[open]**
8. **Restore `missing-replay`.** A population row declared `clone`/`required` must carry the header;
   a stripped header must be a problem, not a silent skip. **[routed — planned-88 2(a)]**
9. **One detector for before and after.** Re-measure `controls-r87.txt` §C2 with the A1 blob, or
   append an erratum naming the pre-A1 blob for the controls and the A1 blob for the after-value.
   **[open]**
10. **Separability erratum.** Strike or qualify "Neither reads the other's work": C2 reads C1's
    `count-c2.py`. **[open]**

## 7. Limits of this review

- I did not judge the quality of the six r86 arms beyond attribution and reading the three diffs;
  that is the C1 reviewers' brief. My measured claim is narrower: each mutant dies on the arm added
  for it, and the frozen rule would not have noticed if it had not.
- Sibling reports are cited as data for reconciliation only; no sibling measurement is presented as
  mine, and where I reproduced a filed finding I say so (P6, P11).
- Fixtures are gone with the scratch dir; every reading is reproducible from the quoted receipt
  text and the lane revisions (`142542e0`, `03b66a43`, `98f48dba`, `b9e6f68d`, `6fc09d69`,
  `25a74d4c`). No `/tmp` path is cited.
- `SCORECARD.md` was read for context; its after cells are the L1's, not my measurement.
