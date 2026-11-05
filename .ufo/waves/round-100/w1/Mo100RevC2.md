# Mo100RevC2 — C2 calibration review (mori round-100, wave w1)

Scope: C2 only. Lane HEAD at review: `5e2bcf2c487e377b51287c587144bdde5b233f8f` (= landing; `git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD`). Everything below was run by this seat; cited receipts are inlined verbatim.

## 1. Frozen counter reproduction — byte-identical to committed receipts

```
$ python3 .ufo/waves/round-100/count-c2.py --root <archive of d1bd1b33…> --list
C2=unmet stated=58 mismatches=7 uncorrected=7 spurious=0 altered=0 census=ok checks_failed=mismatch base=d1bd1b33
  uncorrected S581 10->9,15->14
  uncorrected S582 14->13
  uncorrected S583 14->13
  uncorrected S584 17->15,22->26
  uncorrected S634 17->18
exit=1
$ python3 .ufo/waves/round-100/count-c2.py --root <archive of 5e2bcf2c…> --list
C2=met stated=60 mismatches=7 uncorrected=0 spurious=0 altered=0 census=ok checks_failed=- base=d1bd1b33
exit=0
```

Matches `evidence/before-c2.txt` and `evidence/landing-c2.txt`. `evidence/controls-r100.txt` ends `CONTROLS_DONE unexpected=0`; C2 mutants K0c/K2c fail `mismatch`, K1c/K4c `altered`, K3c `spurious`, K5c `mismatch,spurious`, P2 met on the candidate output (`C2=met stated=58 … base=d1bd1b33`) — the counter can fail every way the contract names.

## 2. Independent recount (own parser, whitespace split — not the counter's code)

Re-extracted all stated counts (patterns A/B) and recounted every quote by whitespace split; all 118 (row, stated, observed) instances printed and audited:

- base: 58 stated; mismatches exactly S581 10→9, 15→14; S582 14→13; S583 14→13; S584 17→15, 22→26; S634 17→18. The other 51 match.
- landing: 60 stated; +S637 12/12, +S638 12/12 (causal separability confirmed), same 7 mismatches, each answered in-row.
- Cross-validation: the lane's own r71/r72 correction rows already held the true counts before this round — S585 states 26 for the failed-call quote, S586 states 9 for the `:54` quote, S587 states 13 for the `:829` quote — and my recount flags no mismatch on S585/S586/S587. Every r100 correction agrees with the lane's prior ground.

## 3. Delta is exactly five correction-only anchor-cell appends (+ C1's disclosed rows)

`difflib.SequenceMatcher` opcode set over `corpus/SOURCES.md` base→landing — nothing else:

- 5 replaces, each `landing_line == base_line + " [" + TAG + ": …]"` inserted at the end of cell 6 (anchor), preceded by exactly one space, text byte-equal to the correction built from my own counts:
  - S581 `[r100 word-count correction: 10→9, 15→14; counted by whitespace]`
  - S582 `[r100 word-count correction: 14→13; counted by whitespace]`
  - S583 `[r100 word-count correction: 14→13; counted by whitespace]`
  - S584 `[r100 word-count correction: 17→15, 22→26 (over the 25-word cap); counted by whitespace]`
  - S634 `[r100 word-count correction: 17→18; counted by whitespace]`
- 1 replace: S221 used-by append `, corpus/knowledge/seat-auth-deaths-r100.md` (C1; `used-by` is a rule-2-mutable column — clean).
- 1 insert: new rows S637/S638 before `## Paths` (C1).
- 11-cell parse (`split("|")==13`): 0 violations in both files. Stripping `" <correction>"` restores each base line byte-for-byte (`apply-c2.py` writes nothing else; it errors on any row whose split is not 13 parts).

## 4. Census on the live lane — exit 0

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
…W04 duplicate-url warnings on pre-existing rows (S035…S634 classes, unchanged by this landing)…
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
exit=0
```

## 5. Append-only gate — the in-row correction TRIPS it

`tools/mori-sources-appendonly.py`: `MUTABLE = ("status", "recheck", "used-by")`; the anchor cell is immutable; edits compare first-parent.

```
$ python3 tools/mori-sources-appendonly.py d1bd1b33…9d9 --repo <lane>
appendonly_violations=50 ids=[S041,…,S543] round_changed=[] supersede_timing superseded_as_of=[…] stale_supersede=[]   (exit 1)
$ python3 tools/mori-sources-appendonly.py 5e2bcf2c…f8f --round-base d1bd1b33…9d9 --repo <lane>
appendonly_violations=55 … round_changed=[S581,S582,S583,S584,S634] … stale_supersede=[S581,S582,S583,S584]   (exit 1)
```

The 50 entering violations are historical (pre-dating the round). The landing adds exactly the 5 corrected rows: `round_changed` names precisely the in-row corrections, and S581–S584 are additionally `stale_supersede` (each already superseded by S586/S583/S587/S585 yet edited in place). This conflicts with CORPUS.md rule 2 ("Only `status`, `recheck` and `used-by` change in place … A correction is a new row whose `teaches` opens `supersedes S0NN —`") and with the round-30 precedent (DraftCorrectionsR2R3 published wrong word counts as a search-log note precisely so "no cell here is edited"). The frozen wave contract P2 nevertheless specifies this exact in-row mechanism — its `altered` conjunct requires the correction to live in the row — and claims are judged only on the frozen predicate. So: a real contract-vs-CORPUS-rule-2 tension for the closure to weigh, not a P2 failure; the contract does not disclose that the gate will trip.

## 6. Whitespace word counting is the right convention

CORPUS.md rule 1 caps quotes at "≤25 words" and defines no counting convention. Whitespace split is the lane's established one: round-30 published "True `wc -w` values" as its correction ground, and the r71/r72 correction rows' counts reproduce exactly under whitespace split in my recount. It is deterministic (punctuation-bearing tokens and hyphenated compounds count once), and the convention is disclosed in the annotation text itself ("counted by whitespace"). No convention change is smuggled in.

## 7. Residual risk / gaps

- The frozen stated-grammar (A/B) leaves ≥3 word-count statements in SOURCES.md out of scope, identical before and after the landing: S231's teaches "the exact resolution quote is 17 words at S229.src:294-296"; S579's two `("…", N words)` forms (hand-recounted 14 and 12 — both correct); S585's prose "26 words —" (agrees with the corrected value). `stated=58/60` is grammar-scoped, not every word-count mention — a coverage limit of the claim, not an error in it.
- Unrun: re-execution of `controls-r100.py` (receipt read, not re-run — pre-freeze committed evidence); S637/S638 pin sha256 verification (C1 scope).
- No `corpus/lessons/round-100.md` exists in the landing tree, so rule-2's old→new logging of the in-place changes is absent (not a P2 conjunct; recorded for closure).

VERDICT C2 holds: counter output reproduces the receipts byte-for-byte on extracted trees; independent recount confirms exactly the 7 claimed mismatches and their exact in-row corrections; the file delta is exactly the 5 anchor-cell appends plus C1's S221 used-by append and S637/S638 rows; rows stay 11-cell; live census exits 0. Caveat: the in-row correction trips the lane's own append-only gate (round_changed = the 5 corrected rows, violations 50→55, stale_supersede S581–S584) — a frozen-contract-vs-CORPUS-rule-2 tension, by the contract's own design, for the closure.
