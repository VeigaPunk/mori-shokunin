# Mo100ExecCalib — independent C2 re-derivation (mori r100, wave w1)

Seat: executor. Scope: re-derive C2 (stated quote word counts in `corpus/SOURCES.md`) with my own
parser, not the frozen counter's grammar, over the entering tree d1bd1b339b894de0249b0f60702dff9962da88d9
("before") and the landing tree 5e2bcf2c487e377b51287c587144bdde5b233f8f ("landing"). Both trees extracted
with `git archive <rev> | tar -x` into scratch. All counts are whitespace splits; every stated/observed
pair below was also hand-checked from the row text.

## Method (own grammar, no count-c2.py code)
Row anchor `^ {0,3}\| *(S\d{3,}) *\|`; every literal `(\d+) words` phrase inside a row collected
(64 before, 66 landing — complete inventory, listed per row). Quote spans scanned independently:
straight double quotes with `\"` escapes, curly “”, and backtick spans (treated as locators/code,
never as counted quotes — no registry row counts a backtick span). Pairing: right-side
`words): "…"` / `words, "…"` first, else nearest left straight/curly span through a locator filler
(backtick spans and single-paren locator stripped). Classification: (a) stated quote count,
(b) not a quote count, (c) ambiguous. Parser: scratch `mo100_c2_redo.py` (removed with scratch).

## Frozen counter receipts (copied)
- before: `C2=unmet stated=58 mismatches=7 uncorrected=7 spurious=0 altered=0 census=ok checks_failed=mismatch base=d1bd1b33` (rc=1)
- landing: `C2=met stated=60 mismatches=7 uncorrected=0 spurious=0 altered=0 census=ok checks_failed=- base=d1bd1b33` (rc=0)
Both reproduce the frozen receipts in `evidence/` (`before-c2.txt`, `landing-c2.txt`).

## My inventory and result
- before: 64 occurrences = 61 (a) mechanical + 1 (b) + 2 (c). stated quote counts total 63
  (the 2 (c) adjudicated (a)-by-reading: S231, S585 26-word item — both verified, see below).
- landing: 66 occurrences = 63 (a) + 1 (b) + 2 (c); stated total 65 (adds S637 12, S638 12).
- (b): S598 `51 words` sits inside the curly-quoted page section title “How it works in 51 words”
  — the page's own text, not a stated quote count. Correctly excluded by the frozen counter too.
- My mismatch list, before and landing (identical): **S581 10→9, S581 15→14, S582 14→13,
  S583 14→13, S584 17→15, S584 22→26 (26 over the 25-word cap), S634 17→18** — exactly the frozen
  counter's seven, same rows, same values. Each verified by hand, e.g. S634 quote
  `it and all subsequent characters up to, but excluding, the next <newline> shall be discarded as a comment.`
  = 18 tokens; S584 failed-call quote `If the function succeeds, … the return value is zero.` = 26 tokens.
- Reconciliation: counter stated=58/60 = my mechanical (a) 61/63 minus the three counts its
  grammar cannot see (S579 2nd, S580 2nd, S577 — see gaps). Arithmetic closes exactly, both trees.

## Grammar gaps in the frozen counter (missed stated counts — all match, no verdict impact)
1. `("QUOTE", N words)` — quote and count together inside parens: S579 2nd quote 14=14,
   S580 2nd quote 12=12. PA needs `"Q" (`, PB needs `N words): Q`; neither sees these.
2. S577 `the first 11 words` — PA's optional locator cannot cross the prose `tag-stripped; the first`;
   it is a sub-span statement (quoted first 11 of a 16-word quote); 11=11 ✓, and the `16-word`
   full-quote claim verified against pinned `corpus/evidence/sources-r66/S577.html:2638-2639`
   (tag-stripped 11+5 = 16 tokens).
3. Prose-bound count without any quote span: S231 `the exact resolution quote is 17 words at
   S229.src:294-296` — 17 verified: S229's row quote (17 tokens) and the pinned
   `corpus/evidence/sources-r40/S229.src:294-296` sentence.
4. My own grammar also missed one mechanically (backtick locator content holds parens):
   S585 `(`:826-827`, 26 words — the sentence sits wholly on :827…): "If the function succeeds…"`
   — hand-verified 26=26 ✓.
So four stated counts (S579#2, S580#2, S577, S231) are invisible to count-c2.py; all match today.
A future tree that broke one of them would still print `C2=met` — disclosed counter weakness,
does not affect this landing.
5. Other phrasing outside both grammars (`N-word` hyphen forms, no `N words` phrase): S577
   `16-word quote` (verified 16 ✓ above), S599 `24-word sentence` (verified 24 ✓ against pinned
   `corpus/evidence/sources-r84/arXiv-2408.01760-abs.html:121`), S597 `24-word located span` and
   S600 `21-word located span` (pins not read this session — unverified). S598's `51 rendered words`
   block count is prose, not the phrase.

## Landing corrections checked against my numbers
Exactly one exact-text correction per mismatched row, in row order, no others:
S581 `[r100 word-count correction: 10→9, 15→14; counted by whitespace]`; S582 `14→13`; S583 `14→13`;
S584 `17→15, 22→26 (over the 25-word cap)`; S634 `17→18` — each list equals my observed mismatch
set for that row; the >25 item carries the cap note. `altered=0` consistent with the tree diff:
only S581–S584/S634 rows carry corrections (byte-identical to base once removed), S221 gains a
knowledge link (no count), S637/S638 are new rows with matching 12/12 counts.

## Counter finds that are wrong
None. All seven counter mismatches are real; none of the counter's pairings is spurious. The
counter's only blind spots are the four matching counts named above.

VERDICT C2 holds: independent re-derivation finds exactly the same seven mismatches; the landing
answers all seven with the exact required correction texts, adds no spurious correction, alters no
count-bearing row beyond its correction, and every stated count the frozen grammar cannot see
(S579 14, S580 12, S577 11, S231 17) plus both new C1 rows (S637/S638 12/12) matches its quote.
