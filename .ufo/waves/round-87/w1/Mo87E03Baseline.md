# Mo87E03Baseline — round-87 w1 baseline before/after table

seat: Mo87E03Baseline (leaf; judged on operability + calibration)
date: 2026-11-04
role: measure, do not attack, do not change claims. Two counters at the three named revisions, from a
`git clone --shared` copy of the lane, so no worktree state is measured.

**Milestone reached:** both counters were run at the entering revision, the C1 landing and the C2
landing (C1 also at 98f48db, C2 also at 03b66a43), each with rc, full stdout and wall time, plus each
counter's `--selftest`.

**Headline:** C1 is a clean, byte-exact before/after under one unchanged counter. C2's after-value is
byte-exact under the A1 counter, but its claimed before-value is **not reachable with the A1 counter
bytes** — and the freeze-time C2 counter bytes can **not** reach the after-value. The C2 claim is
certifiable only by naming two different counter byte-sets for its two ends. Details in §5.

---

## 1. Provenance actually read (hashes at read time)

The lane HEAD moved while this seat ran: it was `98f48dba…` when this seat started and `b9e6f68d…`
when the counters were read (the L1 landed A1 + the w1 spec/dispatch in between). The clone pins the
later tip and is the immutable measurement base.

```
lane worktree HEAD at measurement: b9e6f68d887c570909c7bacc8bac86579d850d1d
  b9e6f68d round-87: contract A1 (C2 subject arm count follows C1) and the w1 spec/dispatch/ready
  98f48dba round-87 C2: replay-capable successor receipts for the two r85 sweep receipts
  03b66a43 round-87 C1: three r86 counters gain the arms that kill the six surviving clauses
  142542e0 round-87: freeze — C1 population-control counter, C2 supersede counter, contract, controls
  6fc09d69 round-86 verifier spot-check (integrator, hyaku): non-author admit/reject   [entering]
```

| file | sha256 (worktree at read) | git blob | same as freeze commit? |
|---|---|---|---|
| `.ufo/waves/round-87/contract.md` | `bf208a448e096da4da5169e1b27db1b1ca97999119a2e43e49954c894042eb07` | `e0a2156a…` (A1 appended) | NO — A1 section added, body unchanged |
| `.ufo/waves/round-87/count-c1.py` | `e2ff968721678cc61d6a1674def8da3e27a43f3fed8daab79d53c657ae2c266e` | `f99f1e87…` | **YES** (identical at 142542e0, 03b66a43, 98f48db, b9e6f68d) |
| `.ufo/waves/round-87/count-c2.py` | `264a43f04af1f9f939da7b3890f608a669a0c7fc2922656ee83f35adb236b14d` | `269842f7…` (A1) | NO — A1 (`SUBJECT_ARMS` 11→13, +2 labels) |
| `.ufo/waves/round-87/count-c2.py` (freeze bytes, extracted by blob) | `e1dfd45a161b11a1ddfeae9bfe3d83f0f4f64c7d93dc0f85fc81d18e87ba7166` | `073276ee…` | **YES** |
| `.ufo/waves/round-87/evidence/controls-r87.txt` | `53d65a426632acdb5c88721a2e7847110780e8c668f8c8fbd4b1bdd5df75e616` | `5e2cbc85…` | **YES** (byte-compared against the freeze blob) |
| `.ufo/waves/round-87/evidence/probe-r87.txt` | `530e35e6058edfa5d690343e149e53392e3daa81ea3f13f3fe7224f26db3180d` | `0e2c1973…` | **YES** (byte-compared against the freeze blob) |

`count-c1.py` is unambiguous: one byte-set covers all revisions. `count-c2.py` is not: the
`142542e0`/`03b66a43`/`98f48db` trees carry `073276ee…`; only `b9e6f68d` carries `269842f7…`
(the A1 amendment). Both were measured; §4 reports both.

## 2. Method

```bash
S=/fast/scratch/hyaku/mori-r87/Mo87E03Baseline
mkdir -p "$S/lane" "$S/scr"
git clone --shared -q /home/vgpnk/Projects/shokunin/mori-shokunin "$S/lane"
git -C "$S/lane" rev-parse --show-toplevel     # -> $S/lane   (asserted before any git call)
git -C "$S/lane" rev-parse HEAD                # -> b9e6f68d…
export TMPDIR="$S/scr" HYAKU_SCRATCH="$S/scr"
```

- `python3 -I` (Python 3.14.8). The counters were **not** edited; their own scratch is confined to
  `$S/scr`; the lane worktree was only read.
- Wall time from `date +%s%N` taken around the child process.
- The dispatch's four command lines were run as written, with the counter resolved inside the clone
  (`$S/lane/.ufo/waves/round-87/count-*.py`); the counter's default `--repo` resolves from its own
  `__file__` to `$S/lane`, so the measured repo is the clone, never the lane worktree.
- The freeze-bytes C2 variant lives outside the clone (extracted blob), so it was run with explicit
  `--repo "$S/lane" --scratch "$S/scr"`.
- Every population read is `git -C $S/lane show <rev>:<path>`, so untracked sibling artifacts that
  appeared in the lane worktree during this seat (`evidence/after-r87.txt`,
  `evidence/supersede-controls-r87.txt`, `corpus/knowledge/receipt-supersede-r87.md`, edited
  `corpus/*.md`) cannot leak into any measured value. Lane HEAD stayed `b9e6f68d…` for all runs.

## 3. C1 — operability — before/after

Counter bytes: `count-c1.py` blob `f99f1e87…`. Target at `03b66a43` per P-C1:
`C1=met mutants=6 killed=6 survivors=0 total=6 arms=54`.

| # | revision | command | rc | wall | verdict line |
|---|---|---|---|---|---|
| 1 | `6fc09d69` entering | `python3 -I $S/lane/.ufo/waves/round-87/count-c1.py 6fc09d69edbb11e5070ff33258de49f062c0fb9b` | **1** | 692 ms | `C1=unmet mutants=6 killed=0 survivors=6 total=6 arms=48 detector=green rev=6fc09d69edbb` |
| 2 | `03b66a43` C1 landing | `python3 -I $S/lane/.ufo/waves/round-87/count-c1.py 03b66a437e68d493ce0aacd1d80c321cc2e6bf7c` | **0** | 790 ms | `C1=met mutants=6 killed=6 survivors=0 total=6 arms=54 rev=03b66a437e68` |
| 3 | `98f48db` C2 landing | `python3 -I $S/lane/.ufo/waves/round-87/count-c1.py 98f48dba3267a73714b862d0fd4fc8c0e82a1d04` | **0** | 804 ms | `C1=met mutants=6 killed=6 survivors=0 total=6 arms=54 rev=98f48dba3267` |

Full stdout, run 1 (rc=1; byte-identical to `controls-r87.txt` §C1, verified by `diff`):

```
MUTANT count-c1.py M1-unanchored-conjunct survived rc=0
MUTANT count-c1.py M2-total-floor survived rc=0
MUTANT count-c1.py M3-arms-tally survived rc=0
MUTANT count-c2.py M4-receipt-summary survived rc=0
MUTANT count-c2.py M5-binding-digest survived rc=0
MUTANT count-c3.py M6-keyshape survived rc=0
EXTRA pristine-arms .ufo/waves/round-86/count-c1.py arms=15 want=18
EXTRA survivor .ufo/waves/round-86/count-c1.py M1-unanchored-conjunct
EXTRA survivor .ufo/waves/round-86/count-c1.py M2-total-floor
EXTRA survivor .ufo/waves/round-86/count-c1.py M3-arms-tally
EXTRA pristine-arms .ufo/waves/round-86/count-c2.py arms=11 want=13
EXTRA survivor .ufo/waves/round-86/count-c2.py M4-receipt-summary
EXTRA survivor .ufo/waves/round-86/count-c2.py M5-binding-digest
EXTRA pristine-arms .ufo/waves/round-86/count-c3.py arms=22 want=23
EXTRA survivor .ufo/waves/round-86/count-c3.py M6-keyshape
C1=unmet mutants=6 killed=0 survivors=6 total=6 arms=48 detector=green rev=6fc09d69edbb
```

Full stdout, run 2 (rc=0):

```
MUTANT count-c1.py M1-unanchored-conjunct killed rc=1
MUTANT count-c1.py M2-total-floor killed rc=1
MUTANT count-c1.py M3-arms-tally killed rc=1
MUTANT count-c2.py M4-receipt-summary killed rc=1
MUTANT count-c2.py M5-binding-digest killed rc=1
MUTANT count-c3.py M6-keyshape killed rc=1
C1=met mutants=6 killed=6 survivors=0 total=6 arms=54 rev=03b66a437e68
```

Run 3 prints the same six `killed rc=1` lines and
`C1=met mutants=6 killed=6 survivors=0 total=6 arms=54 rev=98f48dba3267` (rc=0, 804 ms).
A second run of run 3 (795 ms) produced byte-identical stdout.

**Subject arm counts, measured directly** (the three r86 counters extracted at each revision and run
with their own `--selftest`; this is the `arms=` field's composition):

| revision | r86 `count-c1.py` | r86 `count-c2.py` | r86 `count-c3.py` | sum |
|---|---|---|---|---|
| `6fc09d69` | 15 | 11 | 22 | **48** |
| `03b66a43` | 18 | 13 | 23 | **54** |
| `98f48db` | 18 | 13 | 23 | **54** |

Matches the contract's stated move `15/11/22 -> 18/13/23` and `arms=48 -> 54` exactly.

**C1 finding: clean.** Before and after use one unchanged counter byte-set, the before line is
byte-identical to the frozen control, the after line reproduces the frozen target verbatim (prefix
check on the full target string passed), and the arm sum decomposes exactly as frozen.

## 4. C2 — calibration — before/after

Target per P-C2 at `98f48db`:
`C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6
defeated=1 superseded=2 legacy=1 unexpected=0`.

### 4a. A1 counter bytes (`269842f7…`, the counter present at the lane tip `b9e6f68d`)

| # | revision | command | rc | wall | verdict line |
|---|---|---|---|---|---|
| 1 | `6fc09d69` entering | `python3 -I $S/lane/.ufo/waves/round-87/count-c2.py 6fc09d69edbb…` | **1** | 71 ms | `C2=unmet subject=stub missing=summary_required,binding_required rev=6fc09d69edbb` |
| 2 | `03b66a43` C1 landing | `python3 -I $S/lane/.ufo/waves/round-87/count-c2.py 03b66a43…` | **1** | 805 ms | `C2=unmet receipts=5 absent=2 bindings=7 bound=7 revs=5 limits=5 cmd=5 summary=5 replay=2 matched=4 defeated=1 superseded=0 legacy=3 unexpected=0 detector=green rev=03b66a437e68` |
| 3 | `98f48db` C2 landing | `python3 -I $S/lane/.ufo/waves/round-87/count-c2.py 98f48db…` | **0** | 2773 ms | `C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=98f48dba3267` |

Run 1 full stdout:

```
C2=unmet subject=stub missing=summary_required,binding_required rev=6fc09d69edbb
```

Run 2 full stdout:

```
RECEIPT after-r85.txt expect=met met problems=-
RECEIPT record-sweep-r85.txt expect=met met problems=-
RECEIPT claim-sweep-r85.txt expect=met met problems=-
REPLAY after-c1-r86.txt mode=required rc=0 exported=1
RECEIPT after-c1-r86.txt expect=met met problems=-
REPLAY replay-defeat-r86.txt mode=required rc=0 exported=1
RECEIPT replay-defeat-r86.txt expect=reject failed problems=replay-mismatch
RECEIPT record-sweep-r87.txt absent=1 expect=met
RECEIPT claim-sweep-r87.txt absent=1 expect=met
C2=unmet receipts=5 absent=2 bindings=7 bound=7 revs=5 limits=5 cmd=5 summary=5 replay=2 matched=4 defeated=1 superseded=0 legacy=3 unexpected=0 detector=green rev=03b66a437e68
```

Run 3 full stdout (rc=0, target prefix verified verbatim):

```
RECEIPT after-r85.txt expect=met met problems=-
RECEIPT record-sweep-r85.txt expect=met met problems=-
RECEIPT claim-sweep-r85.txt expect=met met problems=-
REPLAY after-c1-r86.txt mode=required rc=0 exported=1
RECEIPT after-c1-r86.txt expect=met met problems=-
REPLAY replay-defeat-r86.txt mode=required rc=0 exported=1
RECEIPT replay-defeat-r86.txt expect=reject failed problems=replay-mismatch
REPLAY record-sweep-r87.txt mode=clone rc=0 exported=1
RECEIPT record-sweep-r87.txt expect=met met problems=-
REPLAY claim-sweep-r87.txt mode=clone rc=0 exported=1
RECEIPT claim-sweep-r87.txt expect=met met problems=-
C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=98f48dba3267
```

A second run of run 3 (3213 ms) produced byte-identical stdout.

### 4b. Freeze counter bytes (`073276ee…`, as committed at `142542e0`/`03b66a43`/`98f48db`)

Command shape: `python3 -I $S/freeze/count-c2-freeze.py <rev> --repo $S/lane --scratch $S/scr`
(extracted with `git -C $S/lane cat-file blob 073276ee…`; not edited).

| # | revision | rc | wall | verdict line |
|---|---|---|---|---|
| 1 | `6fc09d69` entering | **1** | 786 ms | `C2=unmet receipts=5 absent=2 bindings=7 bound=7 revs=5 limits=5 cmd=5 summary=5 replay=2 matched=4 defeated=1 superseded=0 legacy=3 unexpected=0 detector=green rev=6fc09d69edbb` |
| 2 | `03b66a43` C1 landing | **1** | 786 ms | same population counts, then `subject=selftest arms=(13, 0) labels=True rev=03b66a437e68` |
| 3 | `98f48db` C2 landing | **1** | 2907 ms | `C2=unmet receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 subject=selftest arms=(13, 0) labels=True rev=98f48dba3267` |

Run 1 stdout is **byte-identical to `controls-r87.txt` §C2** (verified with `diff`), i.e. the frozen
counter does reproduce the contract's stated entering control at the entering bytes.

But at both landing revisions the freeze counter reaches the *population* counts and then keeps the
claim unmet on `subject=selftest`: its `SUBJECT_ARMS` is 11 while the post-C1 r86 `count-c2.py`
subject reports `C2_COUNTER_SELFTEST pass=13 fail=0`. At `98f48db` the freeze counter therefore prints
every target field (`receipts=7 … superseded=2 legacy=1 unexpected=0`) yet exits **1**.

### 4c. What the two byte-sets say, side by side

| revision | freeze bytes `073276ee` | A1 bytes `269842f7` |
|---|---|---|
| `6fc09d69` | **`C2=unmet` full control line** (`receipts=5 … legacy=3`), rc=1 | `C2=unmet subject=stub missing=summary_required,binding_required`, rc=1 |
| `03b66a43` | `C2=unmet` same counts + `subject=selftest`, rc=1 | `C2=unmet` same counts, `detector=green`, rc=1 |
| `98f48db` | `C2=unmet` **all target counts reached** + `subject=selftest`, rc=1 | **`C2=met` = frozen target, rc=0** |

**C2 finding (material, not a claim change):** the contract's `C2=unmet receipts=5 absent=2 …
superseded=0 legacy=3` before-value and its `C2=met …` after-value cannot both be emitted by either
committed counter byte-set. The before-value is a freeze-bytes property; the after-value is an
A1-bytes property. A1 is disclosed pre-data, so this is not a post-data move — but the before/after
table is only honest if the two ends are labelled with the counter blob they used:

- before = `073276ee` @ `6fc09d69` (`C2=unmet receipts=5 absent=2 … legacy=3`, rc 1)
- after = `269842f7` @ `98f48db` (`C2=met receipts=7 … unexpected=0`, rc 0)
- bridge = `269842f7` @ `03b66a43` reproduces the before *counts* exactly (`receipts=5 … legacy=3`)
  with `detector=green`, so the delta `+receipts2 +bindings2 +bound2 +revs2 +limits2 +cmd2 +summary2
  +replay2 +matched2 +superseded2 -legacy2` is caused solely by the two successor receipts landing
  at `98f48db`, not by the counter amendment.

## 5. `--selftest` tallies (each counter, as run)

| counter | bytes | rc | wall | tally |
|---|---|---|---|---|
| r87 `count-c1.py` | `f99f1e87…`/`e2ff9687…` | 0 | 126 ms | `C1_COUNTER_SELFTEST pass=18 fail=0` (18 PASS lines, 0 FAIL) |
| r87 `count-c2.py` | `269842f7…`/`264a43f0…` (A1) | 0 | 31 ms | `C2_COUNTER_SELFTEST pass=17 fail=0` (17 PASS lines) |
| r87 `count-c2.py` | `073276ee…`/`e1dfd45a…` (freeze) | 0 | 31 ms | `C2_COUNTER_SELFTEST pass=17 fail=0` (17 PASS lines) |

The A1 amendment changes only the values two arms assert: `subject_arms` prints `13/13` under A1 and
`11/11` under the freeze bytes; the arm count is 17 in both.

Do **not** confuse these with the contract's `count-c1.py 18, count-c2.py 13, count-c3.py 23`: those
are the three **r86** subject counters. The r87 detector `count-c1.py` happens to also have 18 arms;
it is a different file with a different role.

## 6. Cross-checks

1. **Determinism.** C1@`98f48db` re-run 795 ms and C2@`98f48db` re-run 3213 ms produced byte-identical
   stdout to the first runs.
2. **Before-values vs frozen controls.** `diff` of my C1 entering stdout against `controls-r87.txt`
   §C1: identical (16 lines). `diff` of my freeze-bytes C2 entering stdout against §C2: identical
   (10 lines).
3. **Target strings.** Both after-lines start with the exact frozen target string (verified by prefix
   comparison in Python, not by eye).
4. **Population arithmetic at `98f48db`.** 7 receipts present; 9 bindings (after-r85 3, each other
   receipt 1) all bound; 7 receipts carry `# rev:`/`# limits:`/`# cmd:`/summary token; `replay=4`
   = 2 × `required` + 2 × `clone`; `matched=6` (six `expect=met`, all clean); `defeated=1`
   (`replay-defeat-r86` still `replay-mismatch`); `superseded=2 legacy=1` (both r87 successors clean
   and each names one r85 sweep; `after-r85.txt` unsuperseded); `unexpected=0`.
5. **Successor headers at `98f48db`.** `record-sweep-r87.txt` and `claim-sweep-r87.txt` both carry
   `# replay: clone`, `# rev: 25a74d4c…` and `# supersedes:` their r85 namesake; both replays in a
   `--shared` clone at `25a74d4c…` reproduce their bodies, which is why the supersede rule fires.

## 7. Discrepancies recorded plainly (no adjustment made)

1. **The dispatch's C2 entering command does not reproduce the contract's C2 before-value with the
   counter bytes now in the lane.** With `269842f7…` at `6fc09d69` the counter short-circuits on
   `subject=stub missing=summary_required,binding_required` (the A1 label tuple names two labels C1
   had not yet added) and never grades the population. The contract's before-value is reachable only
   with the freeze bytes `073276ee…`. Both runs are in §4; nothing was edited.
2. **The counter that certifies the C2 after-value does not exist at the after revision.** `269842f7…`
   is committed at `b9e6f68d`, one commit *after* the measured `98f48db`; the `98f48db` tree carries
   `073276ee…`, which returns `C2=unmet` there. Contract A1 is pre-data and disclosed, so this is
   permitted, but the certificate is revision-order post-hoc and the report must say so.
3. **The freeze counter would never certify C2 after C1 lands** — at `98f48db` it prints the entire
   target population line and still exits 1 solely on `subject=selftest arms=(13, 0)`. A1 is
   load-bearing, not cosmetic. (This is exactly what A1 predicts; recorded as measured, not as a
   defect.)
4. Minor, no effect on the claim: `claim-sweep-r87.txt` reports `pointers=266` where the r85 worktree
   receipt reported `274`; the successor's own `# limits:` declares this. It is a supersede, not a
   re-derivation, and the C2 rule judges only the replay + clean status, so `superseded=2` is correct
   under the frozen rule.

## 8. Risks

- **Before/after asymmetry is now a recurring property of this lane's calibration receipts.** Two
  counters with a revision-order gap between the certificate and the certified revision invites a
  later reader to quote one end with the wrong byte-set. The fix is documentary (name the blob on
  every end), which §4c does.
- **The A1 subject gate couples C2 to C1's arm names.** Any future C1 arm rename or re-count breaks
  C2's subject sub-gate the same way (`subject=stub` before the change, `subject=selftest` after).
- **The supersede rule accepts any clean successor that names a legacy receipt**, regardless of
  whether the successor observes the same quantity. The `274 → 266` drift is caught only by the
  receipt's prose `# limits:`, not by the counter.

## 9. Blockers

None. Every requested run executed; no counter was edited; no lane, OS, service or harness state was
changed. No tool installs were needed (python3 3.14.8, git, coreutils already present).

## 10. Reproduction

```bash
S=/fast/scratch/hyaku/mori-r87/Mo87E03Baseline
L=/home/vgpnk/Projects/shokunin/mori-shokunin
mkdir -p "$S" && cd "$S"
git clone --shared -q "$L" "$S/lane"
test "$(git -C "$S/lane" rev-parse --show-toplevel)" = "$S/lane"
export TMPDIR="$S/scr" HYAKU_SCRATCH="$S/scr"; mkdir -p "$S/scr"

python3 -I "$S/lane/.ufo/waves/round-87/count-c1.py" 6fc09d69edbb11e5070ff33258de49f062c0fb9b
python3 -I "$S/lane/.ufo/waves/round-87/count-c1.py" 03b66a437e68d493ce0aacd1d80c321cc2e6bf7c
python3 -I "$S/lane/.ufo/waves/round-87/count-c1.py" 98f48dba3267a73714b862d0fd4fc8c0e82a1d04
python3 -I "$S/lane/.ufo/waves/round-87/count-c2.py" 6fc09d69edbb11e5070ff33258de49f062c0fb9b
python3 -I "$S/lane/.ufo/waves/round-87/count-c2.py" 03b66a437e68d493ce0aacd1d80c321cc2e6bf7c
python3 -I "$S/lane/.ufo/waves/round-87/count-c2.py" 98f48dba3267a73714b862d0fd4fc8c0e82a1d04
python3 -I "$S/lane/.ufo/waves/round-87/count-c1.py" --selftest --scratch "$S/scr"
python3 -I "$S/lane/.ufo/waves/round-87/count-c2.py" --selftest --scratch "$S/scr"

# freeze-bytes C2 counter, for the before-value:
mkdir -p "$S/freeze"
git -C "$S/lane" cat-file blob 073276ee8a1dd72e793d8f85edd0fffa9a6d6bbe > "$S/freeze/count-c2-freeze.py"
for r in 6fc09d69edbb11e5070ff33258de49f062c0fb9b \
         03b66a437e68d493ce0aacd1d80c321cc2e6bf7c \
         98f48dba3267a73714b862d0fd4fc8c0e82a1d04; do
  python3 -I "$S/freeze/count-c2-freeze.py" "$r" --repo "$S/lane" --scratch "$S/scr"
done
rm -rf -- "$S"
```
