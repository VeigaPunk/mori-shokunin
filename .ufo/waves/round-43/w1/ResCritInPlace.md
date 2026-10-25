# ResCritInPlace — C2 counter vs an in-place rewrite of the S235 row

Seat: residual critic w1, round 43. Attack C2 in a /tmp sandbox only; frozen
counter `.ufo/waves/round-43/count-c2.py` read, never edited. Lane repo read
only (clone made with `--no-hardlinks`; lane Git/jj/index untouched).

## Setup

- Scratch clone: `/tmp/c2-inplace`, HEAD = entering tip `e3a2b58f72ba3bd52a90646f7285fb85f0ee5dd2`.
- S235 row = `corpus/SOURCES.md` line 241, sole S235 row (`rows=1`), contains
  transposed anchor `a30cda99` exactly once.
- Exact (no trailing newline) sha256 of the entering-tip line:
  `971df55e9e1ed8826e66dd31d12f9cbb5b2c727cf71201a2c0eabc7311e169a2` ==
  frozen `S235_SHA`. (A raw `sed -n 241p | sha256sum` shows
  `e0f284a0…` because it hashes the trailing newline — measurement artifact,
  not a counter defect.)
- Column note: per the registry header
  `id|source|kind|tier|scope|anchor|teaches|status|opened|recheck|used-by`,
  the transposed sha lives in the **anchor** cell; the **teaches** cell holds
  the lesson text. Both readings of the assigned attack were executed.

## Mutations (scratch clone commits only)

- Mutant A (assigned): anchor cell `a30cda99` → `a30dca99`, in place.
  Rev `0cbca0b0a10e9aa18d6eee030f7cf95c01c6e4c4`.
- Mutant B (literal phrasing): teaches cell text edited in place,
  `a30cda99` left transposed. Rev `156bdcb0d04a2834df8cd48594e85549b3466831`.

## Results

Baseline do-nothing at `e3a2b58f…`: `C2=unmet mismatches=2` exit 1
(`correction_row` FAIL ids=[], `scorecard_correction` FAIL count=0) — matches
`control-c2-donothing.txt`. Those two FAILs are pre-existing entering-tip
residuals (S349 correction row and SCORECARD CORR line are not committed at
the tip), not side effects of my mutation.

Mutant A output:

```
check sources_present        PASS (corpus/SOURCES.md)
check scorecard_present      PASS (SCORECARD.md)
check pdf_present            PASS (corpus/evidence/sources-r42/S235.pdf)
check s235_unrewritten       FAIL (rows=1)
check correction_row         FAIL (ids=[])
check declaration_unrewritten PASS (count=1)
check scorecard_correction   FAIL (count=0)
check pdf_sha                PASS (9855a4986a31)
C2=unmet mismatches=3
exit=1
```

Mutant B: identical shape — `s235_unrewritten FAIL (rows=1)`,
`C2=unmet mismatches=3`, `exit=1`.

Delta vs baseline = exactly +1 mismatch (`s235_unrewritten`); no other check
moved. The line-level sha256 pin makes any in-place rewrite of the S235 row —
anchor cell or teaches cell — flip C2 to unmet, as the contract sentence
requires ("an in-place rewrite of the S235 row is `C2=unmet`"). No bypass
found: the counter reads `git show <rev>:path` bytes only (working-tree
edits invisible), `rows()` matches the line as-is, and the hash covers the
whole line, so cell-local edits cannot dodge it. `--repo` correctly resolves
revs that exist only in the scratch clone.

## Assessment

Counter survives the assigned attack under both readings. Smallest safe
correction: none — behavior is as contracted; the two residual FAILs at the
tip are the known do-nothing state, and the working-tree copies under
`.ufo/waves/round-43/assimilation/` are uncommitted lane state, out of this
seat's scope. Scratch clone left at `/tmp/c2-inplace` for re-execution.

Verdict: SURVIVED
Command: `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-43/count-c2.py 0cbca0b0a10e9aa18d6eee030f7cf95c01c6e4c4 --repo /tmp/c2-inplace`
Output: see block above — stdout ends `C2=unmet mismatches=3`, exit code 1.
