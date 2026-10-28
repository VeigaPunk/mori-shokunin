# Mo60Critic23 — H4 per-copy row binding: what it catches, what it structurally cannot

Seat: critic (leaf, read-only). Round 60, wave w1. Freeze revision
`ac496c7cde8cad965079858accae3bedfe4a73f2`; entering `ddfb12fb0838b4307c445194a844f0c4b1950195`.
Tool under test: `tools/mori-entry-claims-check.py`, sha256
`cffe9f3359097277a7ea39729309efdc5831a1738994ceb30ee023ac0eae6e69` (matches `PIN_EC` in
`count-c2.py`). All runs sandboxed under `/fast/scratch/hyaku/mori-r60/Mo60Critic23`; lane
working tree never written. No commits, no lane/fleet VCS mutation.

Baseline reproduced first (control arm intact):

```
$ python3 .ufo/waves/round-60/count-c2.py ac496c7cde8cad965079858accae3bedfe4a73f2 --scratch …
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok \
claims=13 files=6 spans=13 rev=ac496c7c…            rc=0
```

## 1. What H4 actually reads (exact code, exact cells)

`eval_root` H4 block is `tools/mori-entry-claims-check.py:189-238`. Per cited row it inspects
**three of eleven cells** plus the cell count:

| line | check | cell |
|---|---|---|
| `206-207` | first `ROW`-matching line for the cited SID wins, then `break` | — positional |
| `211-214` | `len(cells) == 11`, else `rows:bad_row` | width |
| `215-216` | `cells[7] == "mined"`, else `rows:status` | status |
| `217-219` | `cells[10] == entry_rel` (exact string), else `rows:usedby` | used-by |
| `231-233` | binder = **union** over every row with `len==11 ∧ mined ∧ used-by==entry`, collecting `cells[1]` | source |
| `234-238` | for each cited copy, `any(art in binder_source for binder in binders)`, else `rows:binding` | source substring |

Never read: `cells[2]` kind, `cells[3]` tier, `cells[4]` scope, **`cells[5]` anchor**,
**`cells[6]` teaches**, `cells[8]` opened, `cells[9]` recheck. The copy path and its sha256 live
in the anchor cell (`cells[5]`) in this registry, so H4 does not bind a copy to *its own*
provenance evidence at all — only to the substring of the `.ufo` path somewhere in some binder's
source cell. `reg_rows[sid] = cells[1]` (`:220`) is written and **never read** (`:199` is the only
other occurrence): the per-SID source cell is collected and then discarded in favour of the
union test. `copy_prefix` (`:84`) is likewise accepted and unused.

## 2. Catch/miss matrix (18 forged row variants, each run on a tree materialized from `ac496c7c`)

Args: `--min-claims 10 --min-files 3`, `artifacts-json` = count-c2 `ARTIFACTS`.

```
== A. "source cell names the artifact path, wrong ANCHOR/DATE" (seat lie 1)
A1 anchor cell invented                                   ok=True  reasons=[]
A2 opened cell 1900-01-01                                 ok=True  reasons=[]
A3 anchor+opened+scope+teaches all lie, source/status/ok   ok=True  reasons=[]

== B. "a SECOND row for the same artifact" (seat lie 2)
B1 duplicate SID appended after the honest row            ok=True  reasons=[]
B2 duplicate artifact under a different SID               ok=True  reasons=[]
B3 duplicate SID placed BEFORE the honest row             ok=False rows:status=S556,rows:usedby=S556

== C. "mined row whose TEACHES is empty" (seat lie 3)
C1 teaches cell empty on all six cited rows               ok=True  reasons=[]
C2 scope+anchor+teaches all empty                         ok=True  reasons=[]

== D. one fabricated row covers every copy (r59 D4 reopened)
D1 umbrella row replaces all six rows' artifact naming    ok=True  reasons=[]
D2 frontmatter cites ONLY the umbrella row                ok=True  reasons=[]
D3 umbrella row + the six real rows DELETED               ok=True  reasons=[]

== E. further lies H4 structurally cannot see
E1 source cells permuted across the six rows              ok=True  reasons=[]
E2 source cell negates the artifact while naming it       ok=True  reasons=[]
E3 artifact path only as substring of a foreign path      ok=True  reasons=[]
E4 circular self-citation in the source cell              ok=True  reasons=[]
E5 source-cell sha256 tampered to zeros                   ok=True  reasons=[]
E6 anchor cell → nonexistent copy + fake sha              ok=True  reasons=[]
E7 kind/tier/scope/anchor/teaches/opened/recheck garbage  ok=True  reasons=[]

== F. honest input H4 wrongly rejects
F1 honest multi-use used-by cell (comma list)             ok=False rows:usedby=S553,rows:binding=…r54
F2 honest reuse of existing mined row S003                ok=False rows:usedby=S003

== G. lies H4 DOES catch (control)
G1 cited row status=queued                ok=False rows:status=S556,rows:binding=…r57
G2 cited row used-by other entry          ok=False rows:usedby=S556,rows:binding=…r57
G3 cited row source names no artifact     ok=False rows:binding=…r57
G4 cited row has 12 cells                 ok=False rows:bad_row=S553,rows:binding=…r54
G5 cited SID's row deleted                ok=False rows:missing=S556,rows:binding=…r57
G6 no row names any artifact              ok=False rows:binding=×6
```

Also verified, H1 frontmatter window: a `source: S999` line (no row exists) placed **below** the
10-line head window is invisible (`ok=True`, `reasons=[]`); the same line placed at line 8 fails
with `rows:missing=S999` (`head = lines[:10]`, `:96`). The `binders`-empty guard at `:237`
(`if binders and not any(...)`) is unreachable in the `ok` path: empty `binders` requires every
cited row to fail `rows:status`/`rows:usedby`/`rows:bad_row`/`rows:missing` first, so a `rows:`
reason already blocks. No vacuity hole there.

## 3. End-to-end: the frozen counter still prints `C2=met` on forged rows

Each row is a throwaway `--shared` clone of the lane at `ac496c7c` with one registry edit
committed; `git -C <clone> rev-parse --show-toplevel` asserted in every clone. Lane untouched.

| forgery | clone rev | frozen C2 | census `validate` |
|---|---|---|---|
| six rows' `source` cells gutted + one umbrella row naming all six artifacts | `26d828ba` | **C2=met … rows=ok** rc=0 | silent |
| six real rows **deleted**, one fabricated umbrella row inserted in the table | `1903ea66` | **C2=met … rows=ok** rc=0 | silent |
| real rows kept, frontmatter cites **only** the fabricated umbrella row | `0c95627b` | **C2=met … rows=ok** rc=0 | silent |
| scope/anchor/teaches emptied, `opened` kept valid, status/used-by/source honest | `10357f2b` | **C2=met … rows=ok** rc=0 | silent |
| `opened=1900-01-01` only | `13e61174` | **C2=met … rows=ok** rc=0 | silent |
| anchor+scope+teaches invented, `opened=1900-01-01`, `tier=Z`, kind=blog | `ba2a948c` | **C2=met … rows=ok** rc=0 | E06 ×6 (tier only) |
| invented scope, wrong anchor, empty teaches, `opened=2099-01-01` | `3d180e7f` | **C2=met … rows=ok** rc=0 | E08 ×6 (future date only) |
| scope/anchor/teaches `-`, `opened=-` | `7bc770c9` | **C2=met … rows=ok** rc=0 | E08 ×6 |

The `sources-census.sh` compensating control is *silent* on: invented scope, wrong/blank anchor,
empty teaches on a mined row (W02 fires only for `rejected` rows), past-but-false `opened` dates,
tampered sha256 inside a source cell, and a second row for the same artifact under a new SID
(E04 is URL+scope; `own-work` rows carry no URL). It catches only duplicate *SID* (E03), bad
kind/tier/status enums (E05/E06/E07), future dates (E08), and rows outside `## Registry` (E12).
Fixture note: `--file` against a bare materialized tree floods E11 (used-by paths absent from the
copy), so census verdicts above were taken on the full clones, where E11 count is 0.

## 4. The decisive finding: the r59 D4 attack is re-opened, and the closure claim is false

The r59 routed defect D4 was "one fabricated S900 row satisfies the frontmatter `source:` cite for
five artifact files". H4 blocks the *verbatim* r59 construction (a row naming **no** artifact):

```
m50 D4 exact (umbrella row names NOTHING)  ok=False n_reasons=6  first=rows:binding=…r54
```

but the same attack survives one token later, because `binders` is a **union over all rows** and
the match is a substring of the whole source cell:

```
| S900 | `.ufo/waves/round-54/w1-results.json` `.ufo/waves/round-55/w1-results.json` … (all six)
       | own-work | A |  |  |  | mined | 2026-10-28 | on-release | corpus/knowledge/wave-settlement-artifacts-r59.md |
```

→ every cited copy binds to that one row (`D1`/`D2`/`D3` above), and a committed revision with
this row scores `C2=met` (`26d828ba`, and `1903ea66` with the six real rows deleted). The six
paths are printed verbatim in the entry's own frontmatter, so the forger pays no discovery cost.

This falsifies a **committed lane claim**, not just an intent:

- `corpus/knowledge/entry-claims-hardening-r60.md:23` (landed `398d3225`, present at `b3c25613`):
  `| H4 | … — one fabricated row can no longer cover every copy | Mo59Critic22 D4 |`.
  False as written: one fabricated row naming all six artifact paths covers every copy and scores
  `met`. The same document's Limits paragraph (`:26-29`) simultaneously declares the loophole —
  "a source cell naming two artifacts binds both (over-binding is accepted, never under-binding)" —
  which by induction admits naming six. The entry therefore contradicts itself; the false half is
  the H4 closure cell.
- The **frozen contract** sentence (`contract.md` §C2: "H4 every cited copy binds to a mined
  used-by-exact registry row whose source cell names the copy's `.ufo` artifact") is *not*
  violated — "a row" is singular and the umbrella row is such a row. The frozen C2 target output
  contains no distinct-rows requirement, and the real entry uses six distinct rows, so this is
  **not a met-flip** for `C2=met` as frozen.

Structural cause, not a slip: `reg_rows` at `:199`/`:220` shows the per-SID source cell was
collected and then dropped; `:234-238` tests membership in the union of binder strings instead of
binding copy *k* to row *k*. First-hit-wins at `:206-207` means only the first matching row per
SID is ever inspected, so a later duplicate row is unread (`B1`, `B2`) while an earlier duplicate
row poisons an honest entry (`B3`) — the denial direction of the same defect.

## 5. Test-corpus boundary (why the 13 hostile trees do not cover this)

All 13 trees under `.ufo/waves/round-60/trees-c2h/` were scanned; **no tree contains a row whose
source cell names more than one `.ufo` artifact path**. Row-arm coverage is exactly three trees:
`h07-single-row` (`rows:binding`: one row naming one artifact while four copies are cited),
`h08-row-not-mined` (`rows:status`), `h09-usedby-other` (`rows:usedby`). The tool's own selftest
case 7 (`tools/mori-entry-claims-check.py:387-396`) likewise tests only a row naming **one**
artifact. Nothing in `count-c2.py`'s frozen expect table (`:83-97`) or the selftest exercises an
umbrella row, a duplicated row, a duplicated artifact under a new SID, or any unread cell.
`rows=ok` in the frozen receipt is a statement about the real entry, not about the predicate's
coverage.

## 6. Scope boundary vs. defect, and the smallest safe correction

- **Defect (claim-bearing):** `corpus/knowledge/entry-claims-hardening-r60.md:23` asserts a
  closure that the implementation does not provide; contradicted end-to-end at `26d828ba`. The
  smallest safe correction is textual: replace "one fabricated row can no longer cover every
  copy" with what H4 enforces — "each cited copy's `.ufo` artifact path appears in at least one
  mined, used-by-exact row's source cell; the same row may serve several copies".
- **Scope boundary (declared, no claim depends on it):** anchor/opened/scope/teaches/kind/tier/
  recheck content (`A1-A3`, `C1-C2`, `E6-E7`) are outside H4 by construction; the entry's Limits
  paragraph already declares H3/H4 check "form and binding, not truth". Falsifying an anchor cell
  is therefore a *scope* observation, not an H4 defect — unless an entry cites a row whose anchor
  cell is the only provenance, which the real entry does not.
- **Boundary worth flagging, not a defect this round:** `F1`/`F2` — H4 requires `cells[10]` to be
  *exactly* the entry path, but the registry's own convention is a comma-separated multi-use list
  (e.g. S002 listed for three entries; S003 for five). Any future entry that reuses an existing
  mined non-own-work row is rejected as `rows:usedby`. The real entry avoids this only because
  S553–S559 are single-use rows minted for it.
- **Tool/counter bytes are frozen** (kill rule) — nothing above changes `C2=met` at the freeze
  revision. For a v61 instrument: bind copy *k* to a row whose SID is cited *for* copy *k* and
  whose source cell names that artifact and no other; add a 14th hostile tree exercising a row
  naming all six artifacts; delete the dead `reg_rows`/`copy_prefix` path so the union test cannot
  silently return.

## 7. Method bounds

- Sandboxes: `base/` (materialized `ac496c7c` tree + pinned tool), `work/*` (one dir per forgery),
  `clone{,2..10}` (`git clone --shared --no-checkout`, `rev-parse --show-toplevel` asserted, all
  git writes `git -C <clone>`). Zero lane/fleet writes; no production file, registry, SCORECARD,
  LOG or lane VCS touched.
- `--scratch` passed to every counter run; `TMPDIR` inside the seat scratch root; scratch removed
  after this report.
- Not executed (out of seat scope): C1's counter arms, G1/G2/G3 arm internals, `mori-register-check.py`.
- Reported, not remediated: no edit was made to the tool, the knowledge entry, the contract, or
  any registry row.
