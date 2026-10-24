# CritPredParenthetical — attack on the P-C11 parenthetical `(19 ids)`

## Finding

The parenthetical `(19 ids)` inside the frozen P-C11 text is **refuted**: the
measured `superseded_as_of` set at the landed tip `265a955cc…` is **35 ids**, not
19 — and **not 34 either**. The "34" carried by the wave spec, LOG.md, and this
item's own prompt is a second counting slip (see below). The parenthetical
arithmetic (18 edit-bounded survivors + the newly eligible S226 = 19) missed
**16 never-edited superseded ids**:

`S067, S070, S071, S083, S084, S090, S093, S096, S097, S101, S124, S127, S128,
S129, S131, S140`

19 predicted + 16 missed = 35 measured. Each of the 16 is a superseded id
present at R whose only "edit" is its first-sighting commit — v2's edit-bounded
eligible set silently dropped all of them, not just S226 (the contract's
"18 ids + S226 once S228 lands" prose only ever counted the famous one).

## Commands run

Working directory `/home/vgpnk/Projects/shokunin/mori-shokunin` throughout.

1. First-hand measurement (read-only gate run, no repo mutation):

   ```
   $ python3 tools/mori-sources-appendonly.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --repo . | grep '^supersede_timing'
   supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S067,S069,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193,S226] stale_supersede=[]
   ```

   Counted via regex split: **35 ids** (ordinal enumeration verified 1–35, S226
   at position 35; `uniq -c` shows no duplicates).

2. Receipt parse (python3, `re.match` on the `supersede_timing` line):

   - `evidence/c11-before-lane.txt` → as_of **18**:
     `S041 S044 S051 S062 S064 S069 S179 S180 S181 S182 S183 S184 S185 S186
     S188 S189 S190 S193`; stale `[]`.
   - `evidence/c11-after-lane.txt` → as_of **35**, stale `[]`; the after
     receipt's `changed` lines cover exactly the 18 before-ids (never-edited
     proof for all 17 newcomers); its summary line's
     `superseded=[35 ids]` set equals as_of ∪ stale.
   - `evidence/c11-after-e37dcc6.txt` → as_of **33**, stale `[S069]`; total
     superseded at that rev = **34** — the plausible provenance of the
     propagated "34" (someone counted the union at e37dcc6, or all superseded
     ids excluding the newcomer S226, instead of the tip's as_of list).

3. `grep -n '19 ids' contract.md tools/mori-sources-appendonly.py` — the
   mispredicted cardinality is frozen in **three** places: contract.md:119
   (P-C11 verbatim), contract.md:137 (declared-after cell), contract.md:145
   (kill rule "mismatches the declared 19 ids"), and
   `tools/mori-sources-appendonly.py:87` inside the `PREDICATE` string the gate
   prints on every run.

## Defect classification

**Claim-sizing defect, not a predicate defect.** The mechanizable sentence —
"the timing line's eligible set is every superseded id present at R" — is
satisfied byte-for-byte: `superseded=[35]` at the tip and `superseded_as_of`
prints all 35 (none stale). The gate code (`superseded = sorted(cid for cid in
tip if cid in sup_map)`) implements the predicate's words correctly. What fails
is the human-sized annotation `(19 ids)`, which computed the new eligible set
as `18 + S226` instead of evaluating the predicate it sits inside over the
registry. Sizing a claim-sized cardinality inside a frozen predicate string is
exactly the "number-drift" hazard lesson M24 targets; the freeze rule makes it
unfixable in place (a predicate edit is a new counter version), so the repair
is erratum-class.

## The claim's real counter

"the timing line's eligible set is every superseded id present at R" is the
claim's real counter — it is the sentence whose semantics the receipts actually
test, and under it the measured set is the full 35-element `superseded` list.
The `(19 ids)` parenthetical is only a defective annotation of that sentence's
output; the sibling factual sentences ("no id is stale at the tip", "S069 is
stale at e37dcc6", the three fixture clauses) are all receipt-true. A reader
testing the parenthetical alone would wrongly conclude the gate is broken; a
reader testing the real sentence finds the predicate sound and the annotation
wrong.

## Secondary error flagged

This item's prompt (and `gen-wave-spec.py` lines 30/59/79/128/133, LOG.md
"lists 34 as-of ids") asserts **34**. The committed receipts and a live re-run
both say **35**. The "34" is an inherited miscount — worth one erratum line of
its own, since SCORECARD/lesson drafts keyed to "34" will mis-state the receipt
by one.

## Smallest safe correction

Append-only erratum: replace `(19 ids)` with `(35 ids)` in any reporting of
P-C11 (SCORECARD row, LOG line, lesson M24); record that the frozen
contract/gate-string annotations are wrong-by-count; correct "34" → "35"
wherever the wave spec or LOG propagated it. No predicate or gate byte changes
— the eligible-set clause and its implementation are correct.
