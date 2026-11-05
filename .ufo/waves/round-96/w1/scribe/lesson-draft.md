# Round 96 — lesson draft (mori)

Lane round: mori round 96, attempt 1, wave `w1`. Entering lane HEAD `66c5518e239eeacd6070be26d78085ef702392cb`.
Frozen contract: `.ufo/waves/round-96/contract.md` (read, never edited by this seat).
Axes: **calibration** (C1) and **freshness** (C2), both tied lowest non-retired at depth 5. Depth is not claimed.
This file is a **draft for the L1 to paste** into `corpus/lessons/round-96.md`. It carries no verdict of its own:
every value below is either a before-measurement quoted from a receipt under `.ufo/waves/round-96/evidence/`
or an explicit `<<...>>` placeholder for the L1 to fill from the wave outputs.

## Gate

Admission bar: `corpus/QUALITY.md`. Lane-dispatched seats are author-side advisers; they are not the independent
non-author verifier. The table below is the L1's to fill from the wave-1 seat reports — this draft leaves it empty
rather than guessing a row.

| Candidates | Admitted | Rejected |
|---|---|---|

spot-check: pending (non-author)

## Mistakes (CORPUS: class · evidence · captured-by · fix)

| # | Class | Evidence | Captured-by | Fix |
|---|---|---|---|---|
| 1 | frozen counter bound stale (THROUGH=78, rounds 79-95 unchecked) | `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-96/w1/calib/` receipts and `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-96/evidence/before-c1-count-c2-through95.txt` (the frozen round-79 counter at `--through 95` reports `C2=unmet axes=6 mismatches=5`, while the same counter at its default `THROUGH=78` reports `C2=met mismatches=0` and reads only 46 manifest rows instead of 58 — the bound hides rounds 79-95) | none | new unbounded counter `tools/mori-scorecard-calibration.py` (C1) |
| 2 | count stated without a command (round-95 lesson said `unpinned=3`; measured `unpinned=6`) | `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-96/evidence/before-c2-digest.txt` (`DIGEST_CHECK rows=124 ok=86 mismatch=0 superseded=1 prefix_only=31 unpinned=6`; unpinned rows S125, S612, S615, S616, S622, S623) | CORPUS rule "A count carries its command", not applied | command receipt in the round-96 evidence |

## Sources & frontier

Census (CORPUS §2b), command as run:

```
scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
```

- Census before: exit 0, `mori ok` — receipt `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-96/evidence/before-census.txt`
  (the same receipt lists the cross-scope duplicate-URL warnings it emitted).
- Census after: `<<AFTER>>` — L1 to paste the landing exit code and receipt path; the census must be exit 0 at round end.

Sourced claim (C2): rows S622, S623, S125, S612, S615, S616 are re-opened this round. Each re-opened row carries
its URL, access date and a located quote of at most 25 words in the Gate block above; the L1 fills that block from the
source-seat reports in `w1/`. The row edits are limited to the existing status/recheck/used-by rules (CORPUS rule 2);
no recorded digest is edited or replaced.

Claim bookkeeping for the L1 (before values measured, after values to be filled):

- C1 calibration — before: `5 mismatches` (`before-c1-count-c2-through95.txt`); after: `<<AFTER>>`.
- C2 freshness — before: `unpinned=6` (`before-c2-digest.txt`); after: `<<AFTER>>`.

Not claimed in this round (from the frozen contract): no new axis beyond calibration and freshness, no exploratory
claim, no SHONEN box change, no prefix-only digest repair, and no remediation of any fleet surface. The prefix-only
rows are out of scope by declaration and are left as they stand.

Out of scope for this seat: this seat drafted prose only and ran no measurement command of its own, so every number in
this draft is quoted from the receipts named beside it, and every after-value is a placeholder.
