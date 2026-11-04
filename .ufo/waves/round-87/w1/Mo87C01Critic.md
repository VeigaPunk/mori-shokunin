# Mo87C01Critic — cheap-path attack on the two frozen r87 claims

seat: `Mo87C01Critic` · round 87, wave w1 · date 2026-11-04
mode: detection and report only. **No lane file outside this report path was created, edited,
moved or deleted by this seat.** No commit, push, checkout, reset, stash or mutating `jj`/`git`
command ran in the lane.
Every fixture lived under `/fast/scratch/hyaku/mori-r87/Mo87C01Critic/` (a `git clone --shared`
per fixture, `-c user.name=t -c user.email=t@t`), and that directory was removed before yield.
No tool was installed: nothing was needed, and the pacman guard was respected.

## 0. Authority actually read, with hashes

Lane HEAD moved twice while this seat ran (`98f48dba` -> `b9e6f68d` -> `a90126ef`); the worktree
was clean each time. The graded revisions are immutable, so every reading below is taken from the
lane object database with `git show <rev>:<path>`, never from a worktree copy.

| file | blob at freeze `142542e0` | blob at first HEAD `98f48dba` | blob at HEAD `a90126ef` | sha256 read |
|---|---|---|---|---|
| `.ufo/waves/round-87/count-c1.py` | `f99f1e87…` | `f99f1e87…` | `f99f1e87…` | `e2ff9687…2c266e` |
| `.ufo/waves/round-87/count-c2.py` | `073276ee…` | `073276ee…` | `269842f7…` | pre-A1 `e1dfd45a…b2316d`; A1 `264a43f0…236b14d` |
| `.ufo/waves/round-87/contract.md` | `648dffbf…` | `648dffbf…` | `e0a2156a…` | freeze `f28d75a7…905c40`; A1 `bf208a44…42eb07` |

`git diff 142542e0 98f48dba -- .ufo/waves/round-87/count-c1.py count-c2.py contract.md` is empty:
the freeze blobs are the claim blobs. The A1 amendment landed in `b9e6f68d`, **one commit after the
C2 claim commit**, and changed both `count-c2.py` (`SUBJECT_ARMS 11 -> 13`, two labels) and
`contract.md`. The A1 diff is exactly the two hunks it declares; the `TARGET` string is
byte-identical.

Also read as instructed: `evidence/controls-r87.txt`, `evidence/probe-r87.txt`,
`corpus/lessons/round-86-verifier-spotcheck.md` `## Routed defects (fix in round 87)` (eight
items), and `SCORECARD.md`'s round-87 table (the tail calls the C2 after cell *"measured at
`b9e6f68d` … C2 subject `98f48dba`"*).

## 1. Baseline — do the frozen targets reproduce at all?

| # | command | exact line | rc |
|---|---|---|---|
| B1 | `python3 -I <freeze>/count-c1.py 03b66a43 --repo <lane>` | `C1=met mutants=6 killed=6 survivors=0 total=6 arms=54` | 0 |
| B2 | same at `6fc09d69` | `C1=unmet mutants=6 killed=0 survivors=6 total=6 arms=48` | 1 |
| B3 | `python3 -I <A1>/count-c2.py 98f48dba --repo <lane>` | `C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0` | 0 |
| B4 | `python3 -I <freeze>/count-c2.py 98f48dba --repo <lane>` (**counter at R**) | `C2=unmet … subject=selftest arms=(13, 0) labels=True` | **1** |
| B5 | `python3 -I <A1>/count-c2.py 6fc09d69 --repo <lane>` | `C2=unmet subject=stub missing=summary_required,binding_required` | 1 |
| B6 | `python3 -I <freeze>/count-c2.py 6fc09d69 --repo <lane>` | `C2=unmet receipts=5 absent=2 bindings=7 bound=7 … superseded=0 legacy=3` (matches the frozen control) | 1 |

B1/B2 reproduce the frozen C1 target and entering control with the freeze blob. B3 reproduces the
frozen C2 target **only with the post-claim A1 blob**; B4 shows the blob committed at the claim
revision reads unmet at that same revision. B5/B6 show the converse: the A1 blob no longer
reproduces the frozen C2 entering control, the pre-A1 blob does. **No single counter blob produces
both the frozen before line and the frozen after line for C2.** This is measured, not inferred.

## 2. C1 — paths to `C1=met mutants=6 killed=6 survivors=0 total=6 arms=54`

### P1 — the exact predicate command, run in a fabricated repo (MEASURED: target, rc 0)

The predicate's command carries no `--repo`, but `main()` derives its repo from `__file__`
(`abspath(dirname(__file__)/../../..)`), so a repo that contains the counter at the same path
grades *itself*. Fixture: a fresh `git init` repo (toplevel asserted equal to the fixture before
the first commit) carrying, at the three r86 paths, three subjects that assert nothing about any
counter. Each subject:

```python
import base64, os, sys
SRC = open(os.path.abspath(__file__), encoding="utf-8").read()
WANT = [base64.b64decode(x).decode() for x in (<b64 of its anchors>)]
if [w for w in WANT if SRC.count(w) != 1]:
    print("PUPPET_SELFTEST pass=0 fail=1"); sys.exit(1)
print("C1_COUNTER_SELFTEST pass=18 fail=0")   # 13 / 23 in the other two files
sys.exit(0)
# the anchor lines, as comments — the only thing checked is that this text is still present
```

with the frozen `MUTANTS` `old` strings copied verbatim from the counter (never retyped). The
frozen `count-c1.py` was then copied to `.ufo/waves/round-87/count-c1.py` in that repo, committed,
and the **exact** predicate command run with cwd = that repo:

```
C1=met mutants=6 killed=6 survivors=0 total=6 arms=54 rev=47864243ad77      rc=0
```

Six arms total (one text-presence check per mutant), not 54; no clause of any r86 counter is
exercised; the tallies 18/13/23 are printed literals. `--repo` is not needed — the only difference
from the canonical invocation is the repository the counter sits in.

### P2 — `arms=54` from three subjects that assert nothing (MEASURED: yes)

The same fixture answers the seat's question directly: `arms_total` is the sum of
`arms_of(out)[0]`, a value the *subject prints about itself*. `arms_of` returns the **last**
`COUNTER_SELFTEST pass=(\d+) fail=(\d+)` in the subject's output; a subject may print `pass=18`
in front of one arm. Measured parser behaviour:
`arms_of("…C1_COUNTER_SELFTEST pass=18 fail=0\nEXTRA COUNTER_SELFTEST pass=99 fail=0") == (99, 0)`.
No structural check ties the printed count to the arms that ran.

### P3 — the kill rule accepts a pure syntax break (MEASURED: killed, claim `met`)

Scored with the frozen counter's own `grade()` against the real subject at `03b66a43`:

```
mutant  count-c1.py  old="def arms_of(out):"  new="def arms_of(out)"   (no colon)
-> MUTANT count-c1.py X-syntax-break killed rc=1
-> tail: mutants=1 killed=1 survivors=0 total=1 arms=18     met=true
```

`killed()` is `rc != 0 or FAIL.search(out)`. A `SyntaxError`, `NameError`, missing import or any
other crash is indistinguishable from an arm catching the behaviour. Two further channels, both
measured on the same predicate: `killed(0, "note: fail=1") is True` (a bare string in output kills
a green run) and `killed(124, "timeout") is True` (`selftest_run` maps `TimeoutExpired` to rc 124,
so a hang of 300 s is a kill).

This is a **rule defect, not a present instance defect**: all six frozen mutated copies *parse*
(measured with `compile()`), and each dies on a named arm (see §2.6). The rule cannot certify that
on its own.

### P4 — editing `TARGET`/`TARGET_ARMS` (MEASURED: blocked by the detector's own selftest)

A scratch copy of the frozen counter with `TARGET=(0,6,6)`, `TARGET_ARMS=48` and
`survivors == 0 -> survivors == 6`, run at the entering revision, prints
`C1=unmet … detector=red` rc 1; adding a rewritten tail prints `C1=unmet … detector=red` too. The
`selfcheck` arms `target_split_ok`, `target_split_free`, `target_arms_free` and
`per_file_arms_frozen` pin the constants, and `main()` runs that selftest in the same invocation.
A counter rewrite that also rewrites those arms can print anything, which is unfalsifiable by
construction — the residual requirement is a **blob pin**, not a wording check (§5).

### P5 — pointing it at a different subject

Same mechanism as P1 (the repo is `__file__`-relative, so even the flagless command follows the
counter's location). Measured, not separately repeated.

### 2.6 — what C1 actually gets right (independent attribution)

Running each pristine and each mutated real subject at `03b66a43` directly:

| subject | pristine | mutant | failing arm in the mutated copy | traceback |
|---|---|---|---|---|
| `count-c1.py` | `pass=18 fail=0` | M1 | `unanchored_plus_killed_unmet` | no |
| `count-c1.py` | | M2 | `zero_mutants_unmet` | no |
| `count-c1.py` | | M3 | `arms_tally_from_subject` | no |
| `count-c2.py` | `pass=13 fail=0` | M4 | `summary_required` | no |
| `count-c2.py` | | M5 | `binding_required` | no |
| `count-c3.py` | `pass=23 fail=0` | M6 | `derive_keyshape` | no |

Each mutant fails exactly one arm, that arm is the one the commit added for it, and the arm calls
the graded function (`grade()` / `grade_population()` / `derive()`). The arms are real behaviour
arms — I read the three diffs. **C1's substance is sound at the named revision**; the cheap paths
above are latent gate weaknesses, not a live falsification of the after-value.

## 3. C2 — paths to `superseded=2 legacy=1` with `receipts=7 absent=0 bindings=9 bound=9 …`

### P6 — the exact predicate command, from the ENTERING revision, with two `echo` receipts (MEASURED: target, rc 0)

Fixture from `6fc09d69` (toplevel asserted) containing:
- `.ufo/waves/round-86/count-c2.py` copied from `03b66a43` (C1's subject change only — see P10),
- the frozen A1 `count-c2.py` installed at `.ufo/waves/round-87/count-c2.py`,
- two new receipts whose entire command and body are:

```
# receipt: record-sweep-r87.txt
# cmd: echo RECORD_SWEEP
# rev: 25a74d4c34e8430e4fbb18d4038ef5db872fb0ee
# counter-sha256: b8683be2…6e8efa tools/mori-record-sweep.py
# replay: clone
# supersedes: record-sweep-r85.txt
# limits: named limit - tautological fixture receipt, three words
# ---
RECORD_SWEEP
```

(the second is the same shape with `CLAIM_SWEEP` and `claim-sweep-r85.txt`). Exact predicate
command, cwd = fixture, no flags:

```
C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4
matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=595be4acb035      rc=0
```

`REPLAY record-sweep-r87.txt mode=clone rc=0 exported=1` — the "replay" is the shell echoing the
body. No sweep was run, no legacy receipt was replayed, no binding was recomputed (the binding line
is copied and still matches at `25a74d4c`). The `# limits:` line only has to contain "limit" and
three words; `exported` is hard-coded to 1 in clone mode, so an `exported>=1` check would not help.

### P7 — `superseded` from two header lines on already-clean receipts, no new receipt, no new replay (MEASURED: target, rc 0)

Fixture from `98f48dba`: append `# supersedes: record-sweep-r85.txt` to `after-r85.txt` and
`# supersedes: claim-sweep-r85.txt` to `after-c1-r86.txt`; change nothing else.

```
C2=met … replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=7efdfb602d78   rc=0
```

`replay=4` is unchanged from the honest run — no fifth replay exists. The superseder for
`record-sweep-r85` is `after-r85.txt`, i.e. **the very receipt the contract declares unreplayable**
("its body is a live-observation run … no committed-byte successor can reproduce it"). The rule
counts a *name*, not a reproduction: `supersede_verdict` only needs
`name in clean_names and target == legacy_name`. The frozen header-only control blocks a
*fabricated successor*; it does not block an already-clean receipt becoming a superseder.

### P8 — a receipt may supersede itself (MEASURED: counts)

`# supersedes: after-r85.txt` added to `after-r85.txt` (plus one real link) reads
`superseded=3 legacy=0` rc 1. `supersede_verdict` never checks `target != name`, so
self-supersession is counted. (Alone it overshoots the target, so it is evidence of a rule hole
rather than a target path; P7 is the target path.)

### P9 — is `legacy=1` the honest count? (MEASURED: no, under the natural reading)

Replaying each legacy receipt's own `# cmd:` in a `--shared` clone checked out at its own `# rev:
25a74d4c`, against its own recorded body:

| receipt | recorded body | replayed | verdict |
|---|---|---|---|
| `after-r85.txt` | `C1=met … arms=17` + `C3=met observed=3 aa=stable own_tokens=64 subject_tokens=64 …` + `rc=0` lines | C1 line matches; C3 line reads `C3=unmet observed=3 aa=stable subject=unmet`; the `rc=0` lines are not produced by the cmd | **fails** |
| `record-sweep-r85.txt` | `RECORD_SWEEP … revisions=0` + `rc=0` | `RECORD_SWEEP … revisions=0` (no `rc=0`) | **fails as-cmd'd** |
| `claim-sweep-r85.txt` | `CLAIM_SWEEP … pointers=274` + `rc=0` | `CLAIM_SWEEP … pointers=266` | **fails** (stale number) |

All three legacy receipts fail to replay as written; `legacy=1` is `3 - superseded 2`, i.e. the
number of legacy receipts that **no clean receipt names**, not the number that fail to replay. The
two r87 successors are honest about this in their `# limits:` text, but the frozen claim sentence
("a legacy receipt is superseded by a replaying successor") reads stronger than the predicate.

### P10 — C2 is not causally separable from C1 (MEASURED)

The contract says "Neither reads the other's work." The C2 counter's subject sub-gate reads
`.ufo/waves/round-86/count-c2.py` and requires its selftest to be green at **13 arms** with
`summary_required` and `binding_required` present — both introduced by C1's `03b66a43`. Measured
contrast on the same two-echo-receipt fixture:

- without the C1 subject import: `C2=unmet subject=stub missing=summary_required,binding_required` rc 1
- with only `.ufo/waves/round-86/count-c2.py` from `03b66a43`: `C2=met …` rc 0 (P6)

A1 acknowledges the dependency in prose, but the frozen contract's separability sentence was not
amended, and the dependency is asymmetric (C1 never reads a receipt).

### P11 — the counter at R does not reproduce R; before/after use two different blobs (MEASURED)

See B4/B5/B6. The frozen predicate is literally false at `R = 98f48dba` with the file committed at
that revision; the target is reachable only with `b9e6f68d`'s blob against `98f48dba`'s receipts.
`SCORECARD.md`'s round-87 table already discloses "measured at `b9e6f68d` … C2 subject
`98f48dba`", so this is a **labeling/erratum defect**, not a hidden claim — but the frozen contract,
which is the authority the predicate is copied into, still names only `98f48dba`.

## 4. Impacted axes

**operability (C1, score 7).** The measured after-value is true at the named revision and all six
kills are attributable to the six new behaviour arms, so the axis move is earned. What is *not*
established is the capability sentence: the counter cannot tell a behaviour arm from a
text-presence arm, counts a crash or a timeout as a kill, trusts the subject's self-printed tally,
and grades whichever repo the counter file sits in. P1 reaches the exact frozen line with six
arms that assert nothing, so the counter's output is not evidence-preserving; bank the arms, not
the gate.

**calibration (C2, score 5, tied lowest).** Directly hit. `superseded` is a naming count satisfiable
by two header lines on already-clean receipts (P7), by a successor whose "replay" is `echo TOKEN`
(P6), and by self-naming (P8); `legacy=1` counts un-named legacy rows while all three legacy
receipts fail to replay (P9); and the before/after pair is measured by two different counter blobs
(B3-B6). The numeric target is honest for the *submitted* receipts, but it does not certify that
any legacy receipt was reproduced, which is the axis the round claims to move.

**depth / freshness.** Not measured by this seat; no finding.

## 5. Smallest safe corrections (smallest first)

C1 — keep the counter, close the evidence holes:

1. **Blob pin.** Put the counter's sha256 (or `git rev-parse <freeze>:<path>`) in the frozen
   predicate and the receipt; a judge runs the pinned blob, not "the file at that path".
2. **Repo pin.** In `main()`, after `rev-parse --show-toplevel`, require the repo to equal the
   toplevel derived from `__file__`, or remove `--repo` from the graded command. Today the
   `__file__`-relative default makes any repo containing the counter self-grading (P1).
3. **Attributed kills.** For each mutant, require the mutated output to contain `FAIL <label>` with
   `label` in a frozen per-mutant set, and require the mutated file to compile before running.
   This turns "rc != 0" into "an arm caught it" and closes P3 and the `fail=`/timeout channels.
4. **Structural tally.** Count `^PASS ` lines in the subject's selftest output and require it to
   equal the printed `pass`; otherwise `arms=54` remains a self-report (P2).

C2 — keep the population, make supersession mean reproduction:

5. **A superseder must replay.** Require `mode in {"clone", "required"}` for the naming receipt
   (from `POPULATION`, not from the header) and reject `target == name`. Kills P7 and P8.
6. **The command must name committed bytes.** Require the successor's `cmd` to contain at least
   one pathish token that exists at its `# rev:` (and, in `required` mode, require `exported >= 1`).
   `echo RECORD_SWEEP` then fails; P6 closes.
7. **Bind the legacy body.** Require the successor to carry the superseded receipt's body digest at
   the legacy's own `# rev:` and require the successor's replay to emit it. Naming alone stops
   counting as supersession; `legacy` then means "not reproduced", which is what the axis claims.
8. **One detector for before and after.** Re-measure `controls-r87.txt` §C2 with the A1 blob (it
   currently reads `subject=stub`), or append an erratum naming the pre-A1 blob for the controls
   and the A1 blob for the after-value, plus the C2 counter revision (`b9e6f68d`) in the claim.
9. **Separability erratum.** Strike or qualify the contract's "Neither reads the other's work":
   C2 reads C1's `count-c2.py`. If separability is a property the round is scored on, the subject
   gate must not depend on the other claim's arm count.

## 6. Limits of this review

- I did not judge the *quality* of the six r86 arms beyond attribution and reading the diffs; that
  is the C1 reviewers' brief. My measured claim is narrower: each mutant dies on the arm added for
  it, and the rule would not have noticed if it had not.
- The fixtures are gone with the scratch dir; every reading above is reproducible from the quoted
  receipt text and the lane revisions (`142542e0`, `03b66a43`, `98f48dba`, `b9e6f68d`, `6fc09d69`,
  `25a74d4c`). No `/tmp` path is cited.
- `SCORECARD.md` was read for context only; the after cells there are the L1's, not my measurement,
  and I do not restate them as mine.
