# Mo93R02Atk — round-93 wave w1, seat report (C1 predicate attack)

Seat: Mo93R02Atk · lane `/home/vgpnk/Projects/shokunin/mori-shokunin` · scratch clone at
`/fast/scratch/hyaku/mori-r93/Mo93R02Atk/clone`, branch `seat` = `6d82b8d7ef6d94a5527737f9242cdf04ad018da7`,
forgery branches at `7b3fe9d540c98b8b0390a0f9bbe78de4341092a5`. No lane tree was edited; no git/jj
mutation outside my scratch clone; no tool installs (nothing needed).

## (1) Re-derivation of the 12 mismatch files without the counter

Derived independently of `count-c1.py`:
`git log --diff-filter=A --format=%h 7b3fe9d540c98b8b0390a0f9bbe78de4341092a5 -- corpus/knowledge/<file> | tail -1`,
then the `verified-at:` line looked up at `6d82b8d7` with `git grep -h "verified-at:" 6d82b8d7 -- <file> | head -1`
and boundary membership tested with `case "$va" in *" $ac "*" ..."`.

| file | ac (re-derived) | in `verified-at:` at 6d82b8d7 |
|---|---|---|
| counter-semantics-r78.md | 2360cc3b | NO |
| counter-win-r77.md | 6a230c4b | NO |
| drift-pin-r10.md | 5be89432 | NO |
| execution-binding-r89.md | c89e5b6e | NO |
| kernel-v7.3-recheck-r53.md | 2a4213bf | NO |
| lane-silence-r2.md | 3da84149 | NO |
| rotation-receipt-grammar-r76.md | 71107662 | NO |
| rotation-schedule-r74.md | dc50c80b | NO |
| rotation-series-r75.md | 32132cfb | NO |
| selftest-flake-r9.md | cffb37ef | NO |
| surfaces-r8.md | 9738f1ab | NO |
| workstate-win-r71.md | 3627fac0 | NO |

The 7 untouched files all PASS by the same derivation:
audit-r11 → e4855e8c, progressing-weak-r2 → 3da84149, silence-cutover-r3 → 1439c473,
silence-grading-r2 → 3da84149, verdict-machine-r4 → 5b62c897, verdict-machine-r5 → a420deb7,
verdict-machine-r6 → 92b2e427 — each present at a word-boundary in its file's `verified-at:` line.

**Set difference vs `evidence/measure-c1-entering.txt`: EMPTY.** Every one of the same 12 fails and
every one of the same 7 passes; per-file `ac=` values match the receipt exactly. Counter reproduced
byte-identically: command
`python3 -I .ufo/waves/round-93/count-c1.py 7b3fe9d5 --repo $S/clone --report` at my clone, output
diffed against the frozen receipt → no difference.

## (2) Forgery A — correct admission hashes, original value deleted, plus one body edit

Fixture: from my clone at `78e25fcb5b7d9aa71f55a63ae71e262e5a5b0462`, `corpus/knowledge/counter-semantics-r78.md`
line 1 replaced with `verified-at: 2360cc3b (REPLACED-ORIGINAL) 2026-11-02 (round 78; the S593 claims
below are line-located against the` — the original date text `2026-11-02` deleted, a second body
line changed elsewhere. `count-c1.py` verdict:

```
C1=unmet trio=98 claim_r92_true=0 files=19 adm_ok=7 adm_fail=12 patched12=11 seven_same=7 census=ok checks_failed=admission,patched12 rev=78e25fcb5b7d
```

(Full line at `artifact://164421:raw:1-1` in the wave scratch; code excerpt of the exact eval below.)

**Result: CAUGHT.** The no-body-change rule fires (`patched12=11` for the 12 mismatch files) on the
single body edit. The wrong-hash clause (`admission`, `adm_fail=12`) still fires as designed because
painting `2360cc3b` into one file and leaving the other 11 untouched cannot clear 11 real admission
tests.

## (3) Forgery B — another file's admission hash in each verified-at

12 `verified-at:` values swapped pairwise (counter-semantics↔counter-win, drift-pin↔lane-silence,
execution-binding↔workstate-win, kernel-v7.3-recheck↔selftest-flake, rotation-receipt-grammar↔rotation-schedule,
rotation-series↔surfaces), original text preserved after the hash in parentheses. Forge commit
`115610b3a2c4f90ab06cd78161f8c779b473d545`. Verdict:

```
C1=unmet trio=98 claim_r92_true=0 files=19 adm_ok=7 adm_fail=12 patched12=12 seven_same=7 census=ok checks_failed=admission rev=115610b3a2c4
```

**Result: CAUGHT.** `adm_fail` stays at 12 — every swapped hash misses its own file's admission
commit; no `patched12` regression.

## (4) Could the 7-character prefix be satisfied by a coincidental substring of an unrelated value?

(a) **Cross-file coincidence across the full 19-file verified-at universe at `7b3fe9d5`** (all 19
first-12-lines `verified-at:` values: file A's verified-at containing some other file B's admission
7-char prefix). Result:

```
progressing-weak-r2.md contains lane-silence-r2.md's ac 3da8414
progressing-weak-r2.md contains silence-grading-r2.md's ac 3da8414
silence-grading-r2.md contains lane-silence-r2.md's ac 3da8414
silence-grading-r2.md contains progressing-weak-r2.md's ac 3da8414
total coincidental_other-ac_hits = 4
```

**Interpretation:** this is NOT a false pass — the three files `(lane-silence-r2, progressing-weak-r2,
silence-grading-r2)` share the same true admission commit `3da8414` (one commit admitted all three),
so a hash seen in a neighbour is the same hash, not a coincidence. There is no cross-commit 7-char
prefix collision among the 19 admission commits (checked programmatically: `len(fulls)>1` across a
shared prefix → 0 cases). Within the 12-mismatch-file sub-test the coincidence count is **0**, so
attack step 3's rejection (`adm_fail` stays 12) is fully driven by the real 7-char mismatch, not by
any false-negative suppression.

(b) **Sub-7-char guard:** the predicate demands the full ac (≥7 chars) be a substring of the whole
`verified-at:` line, not of a shorter window. Because admission commits are ≥7 hex chars and verified-at
values that pass step 1's re-derivation inside the counter are matched with `ac[:7] in va` against the
FULL line text, a shorter-than-7-char coincidental match (e.g. `236` inside a date, `6a2` inside
`S592`) does not satisfy `ac[:7] in va` — the substring must span all 7 characters contiguously.

**Residual risk honestly named (this is the one real gap, not manufactured):** the test is a plain
`in` with no word-boundary assertion. A 7-char admission hash `3da8414` sits as a substring of a
LONGER hex token in someone's `source:` sha256 (e.g. `…a3da8414…` inside a 64-char digest on the
same line, wrapping through `verified-at:`). Such an embedding WOULD pass `ac[:7] in va`. None of the
19 files currently exhibits this (measured, `other7=0` when the planted literal is excluded), but the
counter is one sha256-collision-with-substring away from a false pass. **Recommendation for the
integrator:** change `ac[:7] in va` to a regex `(?<![\w])<7chars>(?![\w])`-style boundary check —
this is exactly the clause pattern C2 already uses (`(?<![>\w])/home/...`), so the fix is in-repo
idiomatic, not a new mechanism.

## Summary table

| attack | caught? | gate that fired |
|---|---|---|
| (1) re-derive without counter | n/a — set difference EMPTY | — |
| (2) correct hash, original text deleted, +1 body edit | caught | `patched12=11` (no-body-change rule); `admission` also fires (11 other files legitimately wrong) |
| (3) another file's admission hash | caught | `adm_fail=12` (own-file match required) |
| (4) coincidental 7-char prefix | not exploitable today (0 real coincidences among the 12 mismatch files); plain-`in`-vs-boundary gap named as residual | — |

## Checks run vs unrun

Ran: set-difference re-derivation (1), forgery 2, forgery 3, coincidental-prefix probe (4),
entering-receipt byte reproduction, 7-char cross-commit prefix collision search, seven-unchanged
corroboration (`seven_same=7` in all runs), census corroboration (`census=ok` in all runs).
Unrun: patch construction (seat does not integrate — no patch emitted by design; contract attack
lane only, no lane edit); C2 (out of this seat's scope).
