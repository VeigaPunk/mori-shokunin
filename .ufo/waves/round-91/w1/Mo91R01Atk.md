# Mo91R01Atk — attack on the frozen P-C1 predicate (mori round 91, attempt 1)

Read-only seat; only write is this report. No tools installed (none needed). All work in scratch
`/fast/scratch/hyaku/mori-r91/Mo91R01Atk` (deleted after receipts were copied); the lane was only
read at 79eaa8cf via read-only git.

## Scope attacked
Contract `.ufo/waves/round-91/contract.md` (committed at e02b8a39), §Claim C1: the frozen
predicate line, the kill rule, the landing constraint, the do-nothing control, §Ordering 4.
Subject at 79eaa8cf: `.ufo/waves/round-87/count-c2.py` — 26 selftest arms (pins=26), all four
clause bodies present (`counts["absent"] += 1`, `counts["defeated"] += 1`, `def supersede_verdict`,
`replay-mismatch`).

## Method
Scratch clone `…/Mo91R01Atk/repo` (`git clone --shared`, detached at 79eaa8cf, toplevel asserted
before each commit). Fixture commits (identity `forge-mo91r01atk`, scratch-only):
- `RA=bc9a0570cb2b25bba2c5901f26d6a1a2beb90d39` — counters A/C + demo populations P1, P2, P1-clause.
- `RB=6c52808b085b506944277eb52a095b3e8a475cc1` — RA + counter B + subject copy whose ONLY edit is
  an appended arm block inside `selfcheck`'s tail: `git diff --stat 79eaa8cf RB -- <subject>` =
  `12 insertions(+), 0 deletions` — satisfies the landing constraint's letter.

## Forgers, predicate/kill-rule outcome, frozen-wording verdict

**F-A "print the literal"** (`count-c1-a.py`): runs no mutant, reads no anchor; prints the frozen
line when P1 exists at `<rev>`, the control line otherwise. Under the wording: prints
`C1=met families=4 unarmed=0 …` and exits 0 — "Met iff every field above matches and exit is 0"
is satisfied. **ACCEPTED.** Failing-to-reject clause: the predicate sentence makes the counter's
own stdout the receipt; no clause binds counter provenance, requires derived-from-execution
counts, or provides a trusted reference.

**F-B1 "probe-keyed always-red arm"** (`count-c1-b.py --pristine green` + `subject-b.py`): appended
arm prints `FAIL <family> armed=1` whenever env `C1_ARM_PROBE=<family>` is set — pure selftest
text, zero connection to clause code; all P1/P2 anchors are comments/selftest lines. Kill-rule
outcome: every mutant rc≠0, fail>0, failset={family} → `killed`. **ACCEPTED — even by the honest
reference counter** (run R8 below). Failing-to-reject clauses: the kill rule attributes by FAIL
label prefix only (no causal tie to the applied mutation), and the landing constraint permits
arbitrary appended arms without binding their semantics.

**F-B2 "red pristine dropped"** (`count-c1-b.py --pristine drop`): same, but pristine is red
(`C1_ARM_ALWAYS=1`); the kill rule classifies it `pristine`, and the frozen predicate line has no
`pristine` (or `unanchored`) field, so "Met iff every field above matches" cannot see it.
**ACCEPTED.** Failing-to-reject clause: the frozen predicate line enumerates unattributed/isolated
but omits `pristine=0`/`unanchored=0`.

**F-C "comment/selftest anchors + honest counter"** (`count-c1-c.py`, P1 = shebang + two
selftest-block comments + one inline comment; P2 = two inline comments): mutated copies are green →
survivors. Kill-rule outcome: not killed (`rc=0 ∧ fail=0`). **REJECTED — but only when the counter
is honest.** Rejecting clause: kill rule's `(rc≠0 ∨ fail>0)` condition. The wording nowhere
requires the landing's counter to implement this honestly (no counter-independence/provenance
clause), so the same P1 paired with counter A is a accepted landing; the rejection is a property of
the counter, not of the wording.

## Receipts (exact command shape: `python3 -I <repo>/…/round-91/<counter> <rev> --repo <repo>`, env `HYAKU_SCRATCH=TMPDIR=$S/tmp`)

```
R1  A @79eaa8cf  → C1=unmet families=4 unarmed=4 p1_killed=0 … pins=0 rev=79eaa8cfe5e0        rc=1
R2  A @RA        → C1=met families=4 unarmed=0 p1_killed=4 p1_survivors=0 p2_killed=2
                   p2_survivors=0 unattributed=0 isolated=0 pins=0 rev=bc9a0570cb2b          rc=0
R3  C @RA        → MUTANT p1[1..4] … status=survivor; MUTANT p2[5..6] status=survivor;
                   C1=unmet families=4 unarmed=0 p1_survivors=4 p2_survivors=2 pins=26       rc=1
R4  C @RA --p1 mutants-c1-clause.json →
                   MUTANT p1[1] family=c2-supersede status=isolated
                   C1=unmet … unarmed=3 … isolated=1 pins=26                                 rc=1
R5  C @79eaa8cf  → C1=unmet families=4 unarmed=4 … pins=26 rev=79eaa8cfe5e0                   rc=1
R6  B(green) @RB → MUTANT p1[1..4]/p2[5..6] status=killed;
                   C1=met families=4 unarmed=0 p1_killed=4 … p2_killed=2 … pins=26
                   rev=6c52808b085b                                                          rc=0
R7  B(drop) @RB  → PRISTINE red=1 rc=1 (frozen predicate line has no pristine field)
                   MUTANT p1[1..4]/p2[5..6] status=killed; C1=met … pins=26 …                rc=0
R8  C(--probe) @RB → MUTANT p1[1..4]/p2[5..6] status=killed; C1=met … pins=26 …               rc=0
R9  C @RB (no probe) → all survivor; C1=unmet … p1_survivors=4 …                              rc=1
R10 B(green) @79eaa8cf → C1=unmet families=4 unarmed=4 … pins=26                              rc=1
```

R1/R10: both forgers pass the do-nothing control (`C1=unmet families=4 unarmed=4 …`, exit 1) —
both frozen receipts (control + met) are forgeable. R8 is the strongest result: the honest
reference counter itself accepts F-B1, so acceptance is not contingent on counter dishonesty.
R9 shows B1's acceptance hinges on the counter feeding `C1_ARM_PROBE` — an invocation interface
the frozen wording never specifies.

## Item 4 — anchor check at 79eaa8cf (mismatch found)

- `git grep -E 'c2-(replay-compare-off|supersede|absent|defeated-accounting)' 79eaa8cf` over the
  whole tree: the names appear only in `.ufo/waves/round-87/w1/Mo87M01Mut.md` (as round-87 MUTANT
  names, rows 30–39, most `survived`), `.ufo/waves/round-89/contract.md` (lines 155–156, "remaining
  unarmed clauses"), `SCORECARD.md`, and one results JSON. **Zero occurrences in the subject.**
- Subject label universe (blob-parsed): 26 selftest arm labels + all `problems.append` labels —
  none begins with `c2-` (`any-c2-dash-label: []`).
- Consequently, under the frozen kill rule, NO mutant of real clause code can ever be `killed`:
  R4 mutates the genuine supersede clause (`target == legacy_name` → `!=`, the exact mutation
  round-87 recorded as killed via `FAIL supersede_matched/counts_positive/wrong_target`) and gets
  `isolated` — those labels do not begin with `c2-supersede`. The frozen family names match no
  label prefix the subject can emit, so every kill must be manufactured by appended-arm label
  text — the exact F-B1 laundering path.

## Item 3 — minimal additional rules (text only) for each accepted forger

- Against F-A: "the printed counts must equal classifications the counter itself derived from
  executions at R — the subject bytes at R and each P1/P2 mutant produced by applying
  `anchor_old→anchor_new` to those bytes; the counter's text at R must implement the kill rule."
- Against F-B1: "every FAIL label counted toward a kill must be emitted by an arm that FAILs when
  and only when the applied mutation changes the copy's behavior relative to the pristine copy;
  unconditional or externally keyed FAILs are void; each P1/P2 anchor must lie inside the named
  family's clause code, not comments/docstrings/the selftest block."
- Against F-B2: "the printed line must include `pristine=0` and `unanchored=0`; a red pristine copy
  or any anchor occurring ≠1 times exits nonzero."
- Voiding: **adding any of these after the controls commit would void the frozen claim** —
  §Ordering 4: "Any change to a frozen predicate, population, kill rule or landing constraint after
  step 2 voids the claim; nothing is rewritten." They can only enter a revised contract committed
  before step 2 (before the controls receipts). Said plainly: post-data hardening = void claim.

## Files written (absolute path → sha256)

- `/fast/scratch/hyaku/mori-r91/Mo91R01Atk/forge/count-c1-a.py` → 645d770153c868e3bbad03525f8ee108ff61543ab4a269c2dfeef45760dcb186
- `/fast/scratch/hyaku/mori-r91/Mo91R01Atk/forge/count-c1-b.py` → 7c48bb042def906944664beb29cef29401c6dd8ac2fb81a06f56d0dd9ad8c651
- `/fast/scratch/hyaku/mori-r91/Mo91R01Atk/forge/count-c1-c.py` → c021349d1e9a8e2924b7e4ca2dcef5f09d6d9b958fffa0f2e0de459a3eb2fc09
- `/fast/scratch/hyaku/mori-r91/Mo91R01Atk/forge/mutants-c1.json` → 125781e486c516ad8794e6ce28ee7db9a0ddad80ea475a1e8f155e21fd215923
- `/fast/scratch/hyaku/mori-r91/Mo91R01Atk/forge/mutants-c1-independent.json` → b32a02e9d4603fbcd73bf898503b521c2691d5fa4fd5e8d27729f00e04875fef
- `/fast/scratch/hyaku/mori-r91/Mo91R01Atk/forge/mutants-c1-clause.json` → 2fe36e4690a823cf600cc5e495197a33baf60c380ce86937cbd44c3dc583247a
- `/fast/scratch/hyaku/mori-r91/Mo91R01Atk/forge/subject-b.py` → 76ddf70a22b4aa1a13e54040de5260ed1af1ea3ff8b6dbc46ede9a6d7a529f10
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-91/w1/Mo91R01Atk.md` (this report)
- Scratch clone commits RA=bc9a0570…, RB=6c52808b… (deleted with the scratch tree).

## Limits and open defects

- Demo populations are forger-authored, not the frozen P1/P2 (correctly absent at 79eaa8cf — that
  absence is what the do-nothing control pins). Counter filenames carry `-a/-b/-c` suffixes; a real
  landing would use the canonical `count-c1.py` — cosmetic, does not affect any clause.
- The honest counter's pristine gate is my faithful reading of the kill rule's `pristine` state;
  the wording does not spell out how a counter must invoke the subject selftest, which is itself
  part of finding F-B1/R9.
- Not attacked here: P2's independence guarantee (writer Mo91M01Mut never seeing P1) — process-level,
  not checkable by a counter or predicate clause; noted as residual risk.

## Verdict

`ATTACK C1 forger-accepted=3 rejected=1`
