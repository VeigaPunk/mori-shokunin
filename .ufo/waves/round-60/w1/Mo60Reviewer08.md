# Mo60Reviewer08 — H4 row-binding review (round 60, w1)

Seat: Mo60Reviewer08 (reviewer, read-only). Lane repo
`/home/vgpnk/Projects/shokunin/mori-shokunin`.

## Pins (every byte below comes from `git show <rev>:<path>`, never the
working tree)

| item | value |
|---|---|
| contract (frozen) | `ac496c7cde8cad965079858accae3bedfe4a73f2` |
| entering revision | `ddfb12fb0838b4307c445194a844f0c4b1950195` |
| re-derivation revision R | `b3c256138f00c704d5aa56eb0332d74506502ef2` (lane tip while reviewing; C1 data landed at `398d3225`) |
| tool under test | `tools/mori-entry-claims-check.py` sha256 `cffe9f3359097277a7ea39729309efdc5831a1738994ceb30ee023ac0eae6e69` — equals `PIN_EC` at `count-c2.py:48`; byte-identical at `ac496c7c` and `b3c25613`, absent at `ddfb12fb` (added by wave commit `76904b21`) |
| entry | `corpus/knowledge/wave-settlement-artifacts-r59.md` sha256 `441a751d…1ce21` (same at freeze and tip) |
| registry | `corpus/SOURCES.md` sha256 `46c333d2…2d63` at freeze, `e8bda4a8…9441` at tip; the S553–S559 block hashes `efc3b54279d3abde0fad66f4f76e0d982c80b26643b485865389eb0dc43f5355` at **both** revisions (`git diff ac496c7c b3c25613 -- corpus/SOURCES.md` adds only S561–S564) |
| artifact map | `count-c2.py:59-70` (six copies), `ENTRY`/`SOURCES` at `:52-53`, `FROZEN_EXPECTS` row family at `:88-94` |

Method: scratch root at `$HYAKU_SCRATCH/mori-r60/Mo60Reviewer08` (`/fast/scratch/hyaku`,
disk-guard green: `/fast/scratch/hyaku` 26 % use, 598.6 G free); all inputs
materialized from `git show`; each variant differs from the real registry in
exactly the rows named; the pinned tool is executed as a subprocess with
`--min-claims 10 --min-files 3` (same flags as `count-c2.py:311-315`). No
lane, VCS, corpus, SCORECARD or fleet write.

## 1. Requested variants (all built from the real entry + real registry at R)

Each variant rewrites only the S553–S559 rows of `corpus/SOURCES.md`, then
runs the pinned checker on the one materialized root.

| variant | change | exit / ok | reasons |
|---|---|---|---|
| real | none | 0 / True | `[]`, stats `claims=13 files=6 spans=13 min_span=12` |
| A status-queued-all | `| mined |` → `| queued |` in S553–S559 | 1 / False | `rows:status=S553 … rows:status=S559` (7) |
| A2 status-queued-S554 | as A, S554 only | 1 / False | `rows:status=S554`, `rows:binding=corpus/evidence/sources-r59/w1-results-r55.json` |
| B used-by-another-entry | cell 10 (0-based) → `corpus/knowledge/other-entry.md` in S553–S559 | 1 / False | `rows:usedby=S553 … rows:usedby=S559` (7) |
| C source-cell-scrubbed-all | artifact path removed from cell 1 in S553–S559 | 1 / False | `rows:binding=…w1-results-r54.json`, `…r55`, `…r56`, `…r57`, `…r58`, `…w1-settlement-r58.json` (exactly the six cited copies) |
| C2 scrub-S554-only | as C, S554 only | 1 / False | `rows:binding=…w1-results-r55.json` only |

So the three demanded classes fire with the demanded reason prefixes
(`rows:status`, `rows:usedby`, `rows:binding`), per-copy precision holds
(A2/C2), and a queued row additionally loses its binder contribution —
correct, because a non-mined row is not a valid binder.

Independent corroboration of the frozen row-family trees (materialized from
`b3c25613`, same pinned tool):

```
h07-single-row    exit=1 ok=False expect=['rows:binding']  match=True
  reasons=["rows:missing=S902", "rows:missing=S903", "rows:missing=S904",
  "rows:binding=corpus/evidence/sources-r59/w1-results-r55.json",
  "rows:binding=…r56.json", "rows:binding=…r57.json"]
h08-row-not-mined exit=1 ok=False expect=['rows:status']   match=True
h09-usedby-other  exit=1 ok=False expect=['rows:usedby']   match=True
```

and `python3 .ufo/waves/round-60/count-c2.py b3c25613 --scratch <scratch>/c2scratch`
→ `C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok
tree=ok claims=13 files=6 spans=13 rev=b3c256138f00c704d5aa56eb0332d74506502ef2`,
exit 0 (the committed `evidence/c2-at-freeze.txt` has the same line at
`ac496c7c`).

## 2. Real registry rows S553–S559 bind all six cited copies — confirmed

`corpus/SOURCES.md:333-339` (tip line numbers), each row 11 cells, status
`mined`, used-by cell exactly `corpus/knowledge/wave-settlement-artifacts-r59.md`,
source cell naming the `.ufo` artifact:

| row | artifact named in source cell | cited copy (claim `cfile`) | bound |
|---|---|---|---|
| S553 | `.ufo/waves/round-54/w1-results.json` | `corpus/evidence/sources-r59/w1-results-r54.json` | yes |
| S554 | `.ufo/waves/round-55/w1-results.json` | `…/w1-results-r55.json` | yes |
| S555 | `.ufo/waves/round-56/w1-results.json` | `…/w1-results-r56.json` | yes |
| S556 | `.ufo/waves/round-57/w1-results.json` | `…/w1-results-r57.json` | yes |
| S557 | `.ufo/waves/round-58/w1-results.json` | `…/w1-results-r58.json` | yes |
| S558 | `.ufo/waves/round-58/evidence/w1-settlement.json` | `…/w1-settlement-r58.json` | yes |
| S559 | `.ufo/waves/round-53/w1-results.json` | *(prose-only; no K claim cites r53; not in the frozen artifact map)* | n/a |

Six cited copies, six binders, one-to-one. The seven quoted copy sha256 values
in the source cells also byte-match the committed copies at R
(r54 `ea48a0cc…`, r55 `2e5b0a0f…`, r56 `19536201…`, r57 `29e7a35d…`,
r58 `a57b660d…`, settlement `b259e73c…`, r53 `0d644e0f…`). r53 is frontmatter-
cited, so the per-sid status/used-by checks do apply to S559, and it passes.

## 3. Findings

No blocking/high defect in the assigned scope: the three requested classes
fire, per-copy precision holds, and the real rows bind all six cited copies.
The following are concrete gaps found while probing the binding predicate.

**F1 — MEDIUM — H4 binding is a path-substring test, so a row naming a
different file that *extends* the artifact path still binds.**
`tools/mori-entry-claims-check.py:237`:
`if binders and not any(art in b for b in binders)`.
Variant K changes the S554 source cell from `.ufo/waves/round-55/w1-results.json`
to `.ufo/waves/round-55/w1-results.json.orig` (a different path):

```
== K suffix alias S554 only  exit=0  ok=True  reasons=[]
```

The frozen predicate requires the source cell to name "the copy's `.ufo`
artifact"; a suffix-extended path is not that artifact, yet the copy binds and
the entry is `ok`. Not reachable at R (no such alias exists in
`corpus/SOURCES.md`; block hash above), so C2's frozen target is unaffected —
but the enforcement is weaker than the predicate for any attacker-controlled
registry, which is exactly H4's threat model. Suggested shape (no change made
by me): anchor the artifact match at a path boundary (regex with
`(^|[^A-Za-z0-9._/-])art([^A-Za-z0-9._/-]|$)` or compare extracted
backtick-delimited paths for equality).

**F2 — MEDIUM — one fabricated banner row still covers every cited copy.**
Docstring rationale at `:20-22` says H4 closes "r59: one fabricated row could
cover every copy". Probe: real registry + one mined, used-by-exact row S999
whose source cell enumerates all six artifact paths; entry frontmatter rewritten
in scratch to cite only `source: S999`:

```
exit 0 ok True stats {'claims': 13, 'files': 6, 'spans': 13, 'min_span': 12}
reasons []
frontmatter source lines: ['source: S999 — single banner row naming all six artifacts']
```

So the r59 construction survives in the form "one row naming *all* artifacts".
This is consistent with the frozen predicate sentence (it asks only that each
copy bind to *a* qualifying row; it never requires distinct rows or a
per-copy sid), so it is not a contradiction of the C2 target — it is a predicate
ceiling worth recording before a later round cites H4 as closing that defect.
Tightening candidate: require the cited sid's own row to name the copy
(sid↔copy correspondence), not any row in the registry.

**F3 — LOW — binding is not injective; permuted assignments pass.**
Variant G swaps the artifact paths between S553 and S554 (S553's cell now names
round-55's artifact and vice versa):

```
== G cross-wired S553<->S554  exit=0  ok=True  reasons=[]
```

Every copy is still named by *some* mined/used-by row, so the predicate is
literally satisfied while row 554's title/source pairing is scrambled. Same
class as F2: no row↔copy binding.

**F4 — LOW — binding diagnostics are suppressed when the binder set is empty.**
`if binders and …` (`:237`) means a registry where no row is both `mined` and
used-by-exact emits no `rows:binding` at all. Variant E (scrub + queued):
`exit=1`, reasons only `rows:status=S553…S559`. The verdict still fails, so
there is no verdict hole, but the output cannot distinguish "every copy
unbound" from "binding arm never considered". Variant B shows the same:
`rows:usedby` ×7 and no `rows:binding`.

**F5 — LOW — the row's quoted copy sha256 is never checked by the tool.**
Variant M rewrites every `sha256 <hex>` value in the registry (142
occurrences, including the seven S553–S559 source cells) to zeros, paths
untouched: `exit=0 ok=True reasons=[]`. At R this is covered by
`count-c2.py:275-291` (`tree` arm: each cited copy byte-equals its `.ufo`
artifact; `tree=ok` in the run above), so no claim break — but an entry-claims
pass alone does not establish that the binding row's own hash claim is true.

**F6 — NIT — dead code / weak diagnostic.** `reg_rows` is populated at
`:199,:220` and never read (binding re-scans the registry at `:224-233`).
`rows:binding=<copy>` names the copy but not the sid whose row was expected to
bind it, which makes F1/F3-style mis-bindings harder to see in a failing tree.

## 4. Residual risk

- H4's effective guarantee is: *some* `mined` + used-by-exact row contains each
  cited artifact path as a substring somewhere in its source cell. Path-suffix
  aliases (F1), banner rows (F2), permuted rows (F3) and unverified row hashes
  (F5) all survive that guarantee; none of them can be produced from the frozen
  registry at R, and all 13 frozen trees still separate their classes.
- The registry is trusted input for the tool: it is materialized from the same
  revision R (`count-c2.py:293-305`), so a registry committed in the same
  revision as the entry is scored without any registry-level provenance check.
- S559/r53 is frontmatter-cited but claim-uncited; binding for it is never
  demanded. That is coherent with the frozen artifact map (r53 excluded,
  `count-c2.py:59-70`), and the prose ("recorded, not repaired") is explicit —
  noted so a later round does not read H4 as covering it.

## 5. Verification gaps

- Scope was H4 only; C1 and C3 arms were not exercised here (C3 pins this tool
  by sha, so any H4 change would need the counter pins re-derived).
- Registry parsing was probed with 0-indent rows only; the `ROW` grammar
  (`:57`) allows ≤3 leading spaces, and rows with escaped pipes were not
  exercised (`grep -n '\\|' corpus/SOURCES.md` → none today).
- I executed trees h07/h08/h09 directly and relied on the counter run for
  h00–h06/h10–h12 (`trees=ok` in the same run).
- Host-tool installs: none. No pacman, no network fetch, no new tool needed.

## 6. Scratch hygiene

All artifacts were created under
`/fast/scratch/hyaku/mori-r60/Mo60Reviewer08/`; the directory was removed after
these receipts were copied into this report.
