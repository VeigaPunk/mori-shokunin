# Mo100CritC2 — critic report on C2 (calibration), round 100 attempt 1

Seat: Mo100CritC2 (critic, leaf). Scope: attack C2 only. Counter read unchanged:
`.ufo/waves/round-100/count-c2.py` (frozen). Trees: `d1bd1b33…` (entering) and `5e2bcf2c…` (landing), each
`git archive | tar -x` into scratch. No edits to any lane file; fixtures were hardlink trees of the landing extract
with only `corpus/SOURCES.md` replaced. Git used read-only (`archive`, `show`).

## Counter reading (what it actually checks)

- Population: a row is a line matching `^ {0,3}\| *(S\d{3,}) *\|`. A stated count is read only by PA
  `"QUOTE" (` [LOCATOR `, `] `N words` or PB `(` [LOCATOR `, `] `N words): "QUOTE"`. LOCATOR ≤ 80 chars, no `(`/`"`.
- Mismatch: the row must contain the exact text `[r100 word-count correction: K→W, …; counted by whitespace]`
  listing the row's mismatches in order. Uncorrected = count of mismatches whose exact text is absent.
- Altered: every base row that had a read count must equal its base text once the correction is removed (any other
  change to the row, including a fixed number, fails).
- Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <SOURCES.md>` must exit 0. It
  resolves `used-by` paths against the tree, so a bare-file fixture fails E11 (my first fixture run; discarded, not a
  counter finding; rerun with full hardlink tree).

## Do-nothing control (d1bd1b33)

Command: `python3 count-c2.py --root <entering extract> --list`
Output:
```
C2=unmet stated=58 mismatches=7 uncorrected=7 spurious=0 altered=0 census=ok checks_failed=mismatch base=d1bd1b33
  uncorrected S581 10->9,15->14
  uncorrected S582 14->13
  uncorrected S583 14->13
```
(the frozen receipt `evidence/before-c2.txt` matches; I did not re-verify the remaining lines.)

## Landing positive control (5e2bcf2c)

```
C2=met stated=60 mismatches=7 uncorrected=0 spurious=0 altered=0 census=ok checks_failed=- base=d1bd1b33
```

## Forward attacks: wrong stated count, C2=met printed

All variants = landing extract plus one change; SOURCES.md replaced, everything else hardlinked. Quote used:
`one two three four five six seven eight nine` (9 whitespace words); the stated count written as 10.

| id | construction | counter line |
|---|---|---|
| F1 | new row S699 = copy of landing S583 line, `"Q9" ((10 words)` appended | `C2=met stated=62 mismatches=8 uncorrected=0 spurious=0 altered=0 census=ok checks_failed=-` |
| F2 | same, `"Q9" (ten words)` | same as F1 |
| F3 | same, `"Q9" (10 word)` | same as F1 |
| F4 | same, `"Q9" (see S581.html (p. 54), 10 words)` | same as F1 |
| F5 | same, locator of 81 `x` chars before `, 10 words` | same as F1 |
| F6 | same, curly quotes `“Q9” (10 words)` | same as F1 |
| F7 | same, NBSP `(10\u00a0words)` | same as F1 |
| F8 | same, pattern-B with parenthesised locator `(p. 54 (ed.), 10 words): "Q9"` | same as F1 |
| F9 | new row, 4-space indent, visible `"Q9" (10 words)` | `C2=met stated=60 mismatches=7 uncorrected=0 spurious=0 altered=0 census=ok checks_failed=-` |
| F12 | in-place: hidden `"Q9" ((10 words)` appended to landing S039 (a row with zero read counts at base, so the altered check does not apply) | `C2=met stated=60 mismatches=7 uncorrected=0 spurious=0 altered=0 census=ok checks_failed=-` |
| Z1 | in-place: landing S599 prose `the 24-word sentence` → `the 23-word sentence` (S599 has zero read counts) | `C2=met stated=60 mismatches=7 uncorrected=0 spurious=0 altered=0 census=ok checks_failed=-` |

F1 also shows the "correction names the right numbers on the other quote" case: the S583 copy keeps its own correct
`14→13` correction, and the hidden wrong count on Q9 is not in the correction list, so nothing is flagged.

Caught (not forward escapes): F10 (`| s699 |`) and F11 (`| S699a |`) with a visible wrong count print
`C2=unmet … checks_failed=census` (census rc=1; I did not capture its E-code); the counter's own mismatch check passes
them. Visible wrong count in a normal row, K1 (`| S699 |` copy plus appended `"Q9" (10 words)`):
`C2=unmet stated=63 mismatches=9 uncorrected=2 spurious=0 altered=0 census=ok checks_failed=mismatch`,
`uncorrected S699 14->13,10->9`. K2 (same, with a wrong correction `10→8`) is also unmet, same two uncorrected.

Converse: where the counter is also a gap (correct tree scored unmet).

| id | construction | counter line | claim reading |
|---|---|---|---|
| Y1 | all seven mismatches fixed IN PLACE (`10→9`, `15→14`, … digits changed, no correction text) | `C2=unmet stated=58 mismatches=0 uncorrected=0 spurious=0 altered=5 census=ok checks_failed=altered` (altered S581, S582, S583, S584, S634) | claim says "now match it": satisfied, scored unmet |
| Y2 | landing with one prose word changed in S582 (counts untouched and correct) | `C2=unmet stated=60 mismatches=7 uncorrected=0 spurious=0 altered=1 census=ok checks_failed=altered` (altered S582) | claim does not forbid unrelated row text: scored unmet |
| Y3 | landing plus a new, correct row (copy of S583 with corrected counts) | `C2=met stated=62 mismatches=8 uncorrected=0 spurious=0 altered=0 census=ok checks_failed=-` | sanity, as expected |

## Population: is "only rows of SOURCES.md, only patterns A and B" a fair reading?

Measured on the landing tree (410 rows): the counter reads 60 counts. Raw `N word(s)` tokens inside registry rows: 92.
Nine rows contain count-shaped text and zero read counts; six of them are in the landing tree (S231, S577, S597–S600).
Forms the counter cannot read and that the registry actually uses:
- `"QUOTE", N words)` with no opening parenthesis (S579 `, 14 words)`, S580 `, 12 words)`). Checked by hand: 14 and 12
  match the quote's whitespace count. Read by nothing.
- prose counts: S577 `the first 11 words of the 16-word` (11 matches its quote; the 16 is unchecked), S599 `the 24-word
  sentence`, S597 `24-word loc…`, S600 `21-word loc…`, S231 `the exact resolution quote is 17 words at S229`, S585
  `(…, 26 words — …)` with no adjacent quote, S598 curly-quoted `“How it works in 51 words”` (probably a page claim, not
  a quote count; ambiguous).
- The unread forms in rows that also carry read counts are protected only by the altered check (any change fails); the
  unread-only rows are not protected at all (F12, Z1).

So the population is narrower than the claim sentence "SOURCES.md rows that state a quote's word count": it is the
readable subset of rows, and the contract's "only patterns A and B" is an explicit narrowing that the claim sentence does
not state. On the landing tree, the unread counts I could check are correct; the rest are [INFERENCE]/unverified.

## Summary of attacks

- Forward (wrong count, C2=met): 11 constructions succeed (F1–F9, F12, Z1). Causes: unreadable forms (nested parens,
  spelled numbers, singular, parenthesised locator, >80-char locator, curly quotes, NBSP, `", N words)`-style and
  prose counts), an indented row, and unread-only rows edited in place (no altered protection).
- Forward attempts that failed: visible wrong counts in a normal row (K1/K2), id-variant rows (census), corrections
  with wrong numbers (K2), spurious correction text (already in the frozen controls).
- Converse (correct, C2=unmet): Y1 (count fixed in place, the "match it" branch) and Y2 (unrelated edit to a
  readable row). The altered check forbids any change to a base row with read counts, which is stricter than the claim.

## Verdict on the claim

Measured: the counter's met state on landing is reproduced (X0), and the do-nothing control is unmet (X1). But the
counter prints C2=met on trees with a wrong stated count (F1–F9, F12, Z1), and prints C2=unmet on trees where every
count matches (Y1, Y2). So its predicate does not decide the claim sentence in either direction. The landing tree is
calibrated on the readable forms; the claim as worded is not verified on the unread forms.

VERDICT C2 needs-amend: the counter reads only pattern A/B-readable counts, so C2=met does not establish that every
registry row stating a quote's word count matches it (F1–F9, F12, Z1 print met with a wrong count present); and its altered
check rejects correct in-place fixes (Y1) and unrelated row edits (Y2). Amend either the population (state the
claim as the readable pattern-A/B subset) or the counter (read `"QUOTE", N words)` and prose counts, and allow
in-place count corrections).

## Unrun checks

- Census rerun on the real repo file: not run by me (the frozen receipt `landing-c2.txt` records `census=ok`; my X0 run
  on the hardlink tree also gave `census=ok`).
- Unread-form counts beyond S579/S580/S577 (S599, S231, S597, S600, S585, S598): correctness not checked; [INFERENCE] only.
- No other claim (C1) attacked; no seed or battery run.

## Tools

None installed or updated.
