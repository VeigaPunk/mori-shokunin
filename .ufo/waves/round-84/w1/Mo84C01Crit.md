# Mo84C01Crit — attack the three claims before data (round 84, wave w1, attempt 1)

Read-only critic seat. I changed nothing in the lane except this report. All control fixtures were
built and scored in my own scratch clone (`/fast/scratch/hyaku/mori-r84/Mo84C01Crit/clone`,
`git clone --shared`, fixture commits `-c user.name=t -c user.email=t@t`, deleted before this
report was yielded). No tool was installed or upgraded; no pacman transaction.

Bytes this review is pinned to (the contract worktree was amended while I read it — see §5):

- `master` tip during review: `39190f8a` (A2 counter re-freeze; parent `dbdb1aaa` A1; freeze
  `daa77bd5684c8db75eec1e80c87ee4fa5c3a6bb4`; entering `5adf4337b6510dd246b247092c11cbaa97c930d3`).
- `.ufo/waves/round-84/count-c1.py` sha256-16 `86133aa98df2792f`, `count-c2.py` `2cbe9c87d65bbe7e`,
  `count-c3.py` `dc85d59822e6b674` (worktree == 39190f8a for all three, measured).
- `contract.md` sha256-16 `cfb25f1efa89da9f` (232 lines; A1/A2 committed, A3 uncommitted at
  read time). Line numbers below are against those bytes.

## 0. Verdicts

| Claim | Verdict |
|---|---|
| C1 operability (`mutants=4 killed=2 equivalent=2 survivors=0`) | **attack** — a do-nothing control prints the exact target line rc 0 without the claimed arms (§1.1), and a second control prints `killed=4 equivalent=0` rc 0, bypassing the equivalence adjudication (§1.2) |
| C2 calibration (`arm=all-rows defeated=2 fixtures=3/3`) | **admit** — the do-nothing control is defeated by the counter (§1.3); enforcement is behavioral; separable; axis-attributed; not narrowed |
| C3 depth (`delta=classified tokens=64 classified=union live=derived`) | **attack** — a null classifier that classifies zero tokens prints the target semantics rc 0 (§1.4) |

## 1. Do-nothing controls, scored with the frozen counters

Executed copies were the frozen counter bytes copied to scratch, run as
`python3 -I <frozen copy> <control rev> --repo <fixture clone> --scratch <scratch>` — i.e. the
honest-measurement model (frozen harness, control subjects). Outputs verbatim.

### 1.1 C1 control — self-hash tripwire, no arms landed → TARGET REACHED

Control: r83 `count-c1.py` gains, as the first body lines of `selfcheck()`, a sha256 self-check
that exits 1 with `FAKE pass=0 fail=1` if the file's own bytes (minus a marker) differ from the
pristine bytes. Neither `blind_case_tally` nor `green_requires_fail_zero` exists. Fixture commit
`01d31b1bce8bc521d0ebc45b2a4e3033c84b697a`.

```
MUTANT count-c1.py M24a_killed_tally killed rc=1
MUTANT count-c1.py M24b_green_fail_token killed rc=1
MUTANT count-c2.py M24c_met_unclassified equivalent rc=0
MUTANT count-c2.py M24d_met_residual equivalent rc=0
C1=met mutants=4 killed=2 equivalent=2 survivors=0 total=4 pristine=green detector=green rev=01d31b1bce8b
rc=0
```

That is the frozen target line, contract.md:53, reached with zero claimed work. The counter
enforces "kills happen", not "the arms landed": `FROZEN_MARKERS` (count-c1.py:61) gates only the
r84 harness bytes (checked at :296); nothing checks the graded r83 file for the two arm names, and
`grade()` (:96-153) attributes kills to no mechanism. A mutation-sensitive subject kills any
mutant by construction — this is inherent to the kill rule, but the contract's own seat spec
(contract.md:59-63) says the kills must come from the two named arms, and the counter cannot see
the difference.

Smallest safe correction: extend the marker gate to the subject — require `blind_case_tally` and
`green_requires_fail_zero` to occur in `git show R:.ufo/waves/round-83/count-c1.py` (a
`SUBJECT_MARKERS` check beside :296), and bind `killed == 2 and equivalent == 2` in `met`
(count-c1.py:148). Residual, stated honestly: a seat could still name the arms and kill via
tripwire; full kill attribution would need mutation-grading of the arms themselves (next round's
C1-class work). The marker+K/E binding is the cheapest correction that forces the named arms to
exist and preserves the equivalence adjudication.

### 1.2 C1 control — tripwires in both files → equivalence adjudication bypassed, K/E free

Second tripwire in r83 `count-c2.py`'s `selfcheck()`; fixture commit
`ed6d130a9bc00d7c87897768bdc9c50bc58018e0`:

```
MUTANT count-c1.py M24a_killed_tally killed rc=1
MUTANT count-c1.py M24b_green_fail_token killed rc=1
MUTANT count-c2.py M24c_met_unclassified killed rc=1
MUTANT count-c2.py M24d_met_residual killed rc=1
C1=met mutants=4 killed=4 equivalent=0 survivors=0 total=4 pristine=green detector=green rev=ed6d130a9bc0
rc=0
```

Two consequences. (a) The predicate sentence (contract.md:20) prints `killed=K equivalent=E` with
K, E free — met accepts `killed=4 equivalent=0`, so the frozen target's 2/2 split
(contract.md:53) is not enforced by the counter that embodies the predicate. (b) The A1-style
equivalence adjudication is decorative against a mutation-sensitive subject: coupling markers are
consulted only for survivors (count-c1.py:127-134), so the two "provably equivalent, unkillable"
mutants convert to kills and the coupling proofs never run. Same correction as §1.1 (bind K=2,
E=2).

### 1.3 C2 control — tool that prints the target tail without the rule → DEFEATED (counter sound)

Stub `tools/mori-record-sweep.py`: carries `ALL_ANCHOR_ROWS`/`REVISION_MISMATCH` literals, prints
`RECORD_SWEEP_SELFTEST pass=44 fail=0` (with the four arm names as PASS lines) and
`RECORD_SWEEP ... revisions=0 bindings=3` rc 0 for every run. Fixture commit
`77f575765ae5d1fdcd1e8656b3fc31274ebf482b`:

```
C2=unmet arm=all-rows defeated=0 fixtures=1/3 bindings=3 revisions=0 arms=44 rev=77f575765ae5
FIXTURE carrier-ambiguous new_rc=0 old_rc=0
FIXTURE rev-ambiguous new_rc=0 old_rc=0
FIXTURE conformant new_rc=0 old_rc=0
rc=1
```

The fixture discrimination is real behavior the stub cannot fake; the conformant fixture keeps
`fixtures=1/3` honest. C2's counter is the soundest of the three.

### 1.4 C3 control — constant (null) delta classifier → TARGET SEMANTICS REACHED

Stub r83 `count-c2.py`: markers `LIVE_DELTA`/`delta=classified` present as assignments, selftest
prints four PASS-only delta arms + 12 fillers and `pass=16 fail=0`, live run prints one tail line
claiming `union=64 live_agree=64 deltas=0` and prints **zero** `LIVE_DELTA` lines — nothing is
classified, nothing is derived. Fixture commit `6150f697a540738d6a23507fb647c85dfb9a65cc`:

```
C3=met delta=classified tokens=64 classified=64 union=64 residual=0 live=derived live_tokens=64 live_agree=64 deltas=0 arms=16 rev=6150f697a540
rc=0
```

Every met conjunct (count-c3.py:195-199) is satisfied by self-reported arithmetic:
`classified == union` compares two numbers the subject made up; `classify_ok([])` is vacuously
true (:88-92); `deltas == union - live_agree == len(pairs)` holds at 0 == 0 == 0; `live=derived`
(:197) is a printed token. The counter cannot distinguish "derived" from "asserted" — by
construction it re-runs the subject and believes its tail.

Smallest safe correction this round: bind at least the snapshot side from repo bytes — recount the
snapshot token lines at R (the snapshot path is fixed in the subject's own bytes) and require
`tokens == recount and union >= recount`, parse the subject's printed snapshot/live token lines
and require every `LIVE_DELTA` token to be one of them, and require `len(pairs) > 0` whenever
`union > live_agree` as claimed. Honest limit: the live census remains the subject's word; full
attribution means mutation-grading the four delta arms (the §1.1 correction class), which does not
fit this wave's frozen counter.

## 2. Separability

- **C2**: fully separable. Its counter reads only `tools/mori-record-sweep.py` and
  `.ufo/waves/round-82/record-pins.json` at R. Named revision: base `39190f8a` + tool edit only —
  count-c2 met while count-c1/c3 print their entering `absent` values (observed structure in §1.3:
  the C2 control commit carried C1/C3-unrelated bytes and no counter cross-read them).
- **C3**: separable from C1 mechanically (its counter reads only the subject), but the reverse
  does not hold — see below. Named revision: base + subject classifier with the A2 conjuncts and
  coupling markers preserved → `C3=met` while count-c1 still reads `survivors=2` unmet.
- **C1 is not separable from C3**: C1's verdict is a function of `.ufo/waves/round-83/count-c2.py`
  — the file C3's seat edits. The A2 anchors (`and not unclassified`, `and residual == 0`) and the
  three coupling markers must each survive C3's edit exactly once, or a landed C1 flips to unmet
  (`unanchored`/`coupling-absent`) after C1's seat is done. This contradicts the preamble's
  "no other claim's landed bytes" (contract.md:12-13) directionally. The preservation clause
  manages the risk, but the claim of full separability is false as written.

## 3. Axis attribution

- **C1 → operability**: right surface (the r83 counter family's own detection adequacy), but the
  counter cannot attribute the axis move to the arms — §1.1 shows the axis moving via a tripwire,
  i.e. by the number printed, not the surface changed. Attribution unenforced.
- **C2 → calibration**: genuine. The all-rows rule is graded behaviorally on two defeated
  fixtures plus the real three-binding run; QUALITY 169's first-match gap actually shrinks.
- **C3 → depth**: claimed move is observation → fact; §1.4 shows the axis reachable by printing
  the fact-shaped tail. Attribution unenforced.

## 4. Admission

- **Reachable by entering bytes?** No. I reproduced all three entering controls exactly
  (`C1=unmet harness=absent`, `C2=unmet arm=absent`, `C3=unmet delta=absent`, each rc 1) at
  `5adf4337`, matching `.ufo/waves/round-84/evidence/controls-r84.txt`.
- **Population control**: the declared value (contract.md:55-56, `mutants=4 killed=0 equivalent=2
  survivors=2`) was NOT receipted at the freeze. Measured at `daa77bd` with the freeze counter:
  `C1=unmet mutants=1 killed=0 equivalent=0 survivors=1 total=1 pristine=green detector=green`
  with three `unanchored` extras (M24b 2 occurrences, M24c/M24d 0) — A2's narrative confirmed.
  The declared value became true only after the A2 re-freeze `39190f8a` (my run of the corrected
  counter at `daa77bd` prints the declared line exactly). This is the D82-2/D83-1 class
  (declared, not receipted); repaired pre-data, but the assignment's "the counters were frozen
  there before any seat ran" no longer holds literally for count-c1.py, and
  `evidence/controls-r84.txt` still contains only the three entering runs — the corrected
  population-control receipt should be committed beside them.
- **Narrowed vs SCORECARD `## Planned (round 84)`?** No. Item 1 (arms for M24a/M24b + A1-style
  adjudication for M24c/M24d) matches; item 2 planned "first-match disambiguation (or
  all-anchor-rows requirement) and its defeated fixture" — the contract requires all-rows with two
  defeated fixtures (expansion); item 3 planned "absent-live / class-changed" — the contract adds
  `added-live`/`agreed`, four arms and tail fields (expansion).
- **Harm to another axis?** None found. The three subjects are the axis-own surfaces; no
  SCORECARD score row, no other lane surface, and no sibling file is touched by the claims as
  specified. The only cross-claim hazard is the C1↔C3 shared file (§2), which the preservation
  clause manages.

## 5. Defect list (file:line)

1. **D84-C1a (decisive, measured §1.1):** C1 target reachable without the arms.
   count-c1.py:61,296 (marker gate covers only the r84 harness), :96-153 (grade attributes kills
   to no mechanism); contract.md:59-63 (seat mechanism) vs :20 (predicate omits it). Correction:
   subject-side arm-name markers + `killed==2 and equivalent==2` in met (:148).
2. **D84-C1b (decisive, measured §1.2):** K/E free; equivalence adjudication bypassable.
   contract.md:20 vs :53; count-c1.py:127-134 (coupling consulted only for survivors), :148.
3. **D84-C3a (decisive, measured §1.4):** null classifier reaches the C3 target.
   count-c3.py:195-199 (self-reported arithmetic), :88-92 (vacuous classify_ok), :36-37 (FIELD
   regex has no `absent_live`/`added_live`/`class_changed`/`agreed`); contract.md:117-118
   ("exactly one LIVE_DELTA line for every union token that is not agreed") is enforced only as
   the deltas identity.
4. **D84-C2a:** the four named selftest arms are unenforced — contract.md:104-105 ("exactly four
   new selftest arms") vs count-c2.py:255-257 (tally-only parse; no arm-name grep; contrast
   count-c3.py:165-167). Correction: grep `PASS <arm>` for the four names, mirroring DELTA_ARMS.
5. **D84-C2b (wording):** contract.md:72 prints literal `arms=44` while :77 says "N ≥ 44";
   counter implements the floor (count-c2.py:37,257). A 45-arm tool prints met with a tail that
   deviates from the quoted target. Same class as D84-C1b; state which governs.
6. **D84-W1 (wording):** contract.md:12-13 "no other claim's landed bytes" is false for C1 (it
   grades C3's seat file). Add the shared-file coupling sentence.
7. **D84-W2 (wording, live trap):** contract.md:128-129 still demands `and not unclassified and
   residual == 0` exactly once — it occurs 0× at entering (r83 count-c2.py:241-242 wraps it), and
   A2 (contract.md §A2, committed) supersedes with the split conjuncts and forbids merging. The
   frozen sentence and A2 contradict; a C3 seat following :128 literally merges the conjuncts
   against A2. Edit :128-129 to A2's five-substring list or mark it superseded.
8. **D84-W3 (wording):** contract.md:126-127 names tail fields `absent_live=`/`added_live=`/
   `class_changed=`; count-c3.py:36-37,:195-199 never check them. Also :123-124 "`agreed` equals
   the counter's `live_agree`" — the counter parses no `agreed` field at all.
9. **D84-W4 (wording, A3-resolved):** contract.md:123-124 "met never requires a particular token
   count" vs the predicate's `tokens=64` (:113) and count-c3.py:196 `tokens == 64`; the counter's
   own docstring (count-c3.py:13-14) repeats the "never requires" sentence and then requires it.
   A3 (uncommitted worktree text at review time) resolves the intent: `tokens=` is the snapshot
   count. Commit A3 and fix the count-c3.py docstring.
10. **D84-P1 (process, repaired):** population control declared but not receipted at the freeze —
    measured `mutants=1` at `daa77bd` with the freeze counter (§4). Commit the corrected-counter
    population receipt beside `evidence/controls-r84.txt`.

## 6. What I ran / verified / could not verify

Ran (all outputs verbatim in this file): the three frozen counters at `5adf4337` (entering
receipts reproduced exactly); the original freeze counter and the corrected counter at `daa77bd`
(population control, both variants); `--selftest` of neither r84 counter was skipped — every §1
run executes the executing copy's own detector selftest internally (`detector=green` in all
receipts); four control fixtures built and scored (§1.1-§1.4); anchor-occurrence counts for all
four old anchors, the A2 replacement anchors and the three coupling markers at both revisions.

Verified: counters byte-identical to `39190f8a`; counter diff vs `daa77bd` confined to the A2
anchor correction (10 lines); SCORECARD `## Planned (round 84)` not narrowed; entering targets
unreachable.

Could not verify: the final integration behavior (no after-revision exists yet — this is pre-data);
whether the L1 will commit A3 and the stale-sentence fix before the C3 seat reads :128; the worktree
contract changed twice while I reviewed (+20 → +91 lines vs `daa77bd`), so line numbers above are
pinned to sha256-16 `cfb25f1efa89da9f`.

Defects found in other seats' bytes: none beyond the contract/counter defects above (no seat had
landed w1 work at review time; `w1/` was untracked and the graded subjects were at entering state).
