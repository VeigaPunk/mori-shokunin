# Mo59Critic22 — F1: C2=met is attainable with a semantically empty depth entry

Seat: Mo59Critic22 (critic, leaf). Assignment: falsify C2 — cheapest entry
scoring `met` without real claims (trivially repeated quotes / JSON-shape
tautologies). Result: **counterexample found, verified end-to-end on the
frozen counter.**

## Counterexample (verified, not inferred)

Throwaway shared-object clone of the lane at freeze rev
`60b3a76ad0524c8978cc51922940be1c8c388915`, grafted with:

1. **Copies** — the six `corpus/evidence/sources-r59/*.json` files `cp`'d
   byte-equal from their `.ufo` artifacts (the genuine part the counter
   demands; `tree=ok` legitimately).
2. **Entry** `corpus/knowledge/wave-settlement-artifacts-r59.md` — 10 claims
   K1–K10. Claim text is literally `x.` for nine claims and the plainly
   *false* sentence "The artifact encodes waveform audio in YAML form." for
   K9. All ten quotes are the **identical 6-byte span** `` `"lane"` `` at
   **offset 3** — a common structural prefix shared by all five
   `w1-results-r*.json` files (two claims per file). Plus one malformed line
   `- **K99** — dangling claim with no pin or span`.
3. **SOURCES.md** — one appended row `S900` whose every cell except
   `mined`/`used-by` is fabricated ("adversarial fabricated row — cites
   nothing real"). One row for five cited files — no row↔artifact binding is
   required by the counter.

Adversarial clone revision: `9ae856762918594cb447494abf9adb5e67783794`.

```
TMPDIR=… python3 .ufo/waves/round-59/count-c2.py \
  9ae856762918594cb447494abf9adb5e67783794 --repo <clone> --scratch …
→ C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok \
  tree=ok claims=10 files=5 rev=9ae856…            (exit 0)
```

Do-nothing control at entering `2b9f0397` on the same clone:
`C2=unmet … failed=copy_absent:…,drift,entry_absent,scan,selftest,tool_absent,tree,trees,trees_absent`
(exit 1). Control arm intact.

## Defects in the frozen C2 predicate (count-c2.py line pointers)

| # | Defect | Evidence |
|---|--------|----------|
| D1 | **Claim text is unchecked.** `CLAIM` regex `^- \*\*K(\d+)\*\* — .+? Quote: …` (line 78-80) accepts any non-empty text; `eval_entry` never inspects it. Ten claims of `x.` plus a false K9 all count toward `claims_min`. | claims=10 entry=ok above |
| D2 | **Quote spans need not be distinct.** Uniqueness is enforced only on K ids (`kid in seen`, line 125). All 10 claims cite the same 6-byte span `"lane"` @offset 3 — the "quotes repeated trivially" attack lands. | K1–K10 identical `(…:offset:3; …)` |
| D3 | **`grammar:` reasons are orphaned — they do not block `met`.** `entry_ok` excludes `frontmatter/distinct/claims_min/files/span/entry_absent` (line 303-305) but not `grammar`; `met` composes only `entry_ok/rows_ok/pins_ok` (line 360-361). Probe on the materialized root: `eval_entry` returns `ok=False, reasons=['grammar:- **K99** — …']` while `entry_ok=True` and the full counter prints `C2=met`. Hostile tree t12 only exercises the all-malformed case (expect `grammar` + `want_ok=False`); a met entry may carry unlimited malformed claim lines silently. | probe output; t12/expect.txt |
| D4 | **Row↔artifact binding absent.** Rows arm checks only `cells[7]=="mined"` and `cells[10]==ENTRY` (lines 183-189). One fabricated S900 row satisfies the frontmatter `source:` cite for five artifact files; the contract's "one per cited artifact copy" and "status mined" *provenance* intent is unenforced. `sources-census.sh` may catch a fake row at round level, but the frozen predicate does not. | S900 row content; rows=ok |
| D5 | **Copy production is independent of citation.** `tree` arm requires all six copies byte-equal (lines 267-278) even though `files_min` needs only 3 cited files — dead pinned copies pass, and (conversely observed) citing the r53 drift file is impossible since `ARTIFACTS` excludes it: `files:outside` (peer Mo59Executor39 confirms: K11→r53 gave `files:outside=…w1-results-r53.json`, deleting it → met). | count-c2.py:130-138; peer report |

## Impacted axes

- **C2 evidential value**: `C2=met` certifies *shape* (pin/span byte-equality,
  row-cell equality, tree/fixture verdicts), not depth. Any `met` verdict this
  round is consistent with a zero-information entry.
- **C1**: unaffected (not probed; out of seat scope).

## Smallest safe correction

Counter bytes are frozen (kill rule) — cannot patch this round. Judgment
guidance: treat `C2=met` as a shape check only; the C2 claim's "≥10 real
pin-bound claims" needs verifier/manual review of claim-text semantics,
quote distinctness, and row↔copy binding (my entry would fail all three on
inspection). A v60 counter should add `grammar` to the `entry_ok` exclusion
prefixes, enforce distinct (file,kind,offset/line,quote) spans, and bind each
`ARTIFACTS` copy to ≥1 cited claim and each cited SID to ≥1 copy.

## Method bounds / receipts

- Sandbox: `--shared` clone under `/fast/scratch/hyaku/mori-r59/Mo59Critic22/clone`
  (lane working tree untouched; zero mutations to lane/fleet). All git writes
  via `git -C <clone>` after `rev-parse --show-toplevel` assertion.
- Counter run read-only from lane path `…/mori-shokunin/.ufo/waves/round-59/count-c2.py`
  with `--repo <clone>`; frozen bytes unchanged (evaluated vs freeze rev).
- Attack arms exercised: scan=ok, drift=ok, trees=ok, selftest=ok all genuine
  (real tool bytes at PIN, real .ufo files, real hostile trees) — the met is
  carried entirely by the entry/rows arms' semantic vacuity.
- Not checked: C1 counter, census script behavior on fabricated S900 (it would
  likely flag the row — noted as a compensating control, not part of P-C2).
- Scratch cleaned after report write.
