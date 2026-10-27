# Mo56RevSourcesContract — SOURCES.md contract-v1 conformance at freeze tip

Seat: reviewer (leaf). Scope: `corpus/SOURCES.md` in mori-shokunin at
`8be2717b0809281d07dffe83dad424a4859e0747` — shape, row schema, the 0-3
leading-space parser rule, pipes-in-cells, append-only discipline
`5b295eeebd87ebd610d8d39bfe2035742f740cfa..8be2717b0809281d07dffe83dad424a4859e0747`.
Contract text: `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`
(frozen v1, still the authority per `PROTOCOL.md:435`); maintained parser
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (E01–E12, W01–W04);
maintained-parser note at `/home/vgpnk/Projects/shokunin/CORPUS.md:150-155`.

Method: `git archive <rev> corpus/SOURCES.md` into scratch for both commits;
`git archive 8be2717b… corpus tools` plus `git show` of the eight root `*.md`
files to reconstitute a lane root for the E11 used-by disk check; all git ops
read-only. Working-tree `corpus/evidence/sources-r56/` copies hashed directly
(verified identical paths exist at the commit via `git cat-file -e`).

## Evidence

### 1. Append-only diff (entering tip → freeze tip)

```
$ git -C mori-shokunin diff --stat 5b295ee… 8be2717b… -- corpus/SOURCES.md
 corpus/SOURCES.md | 2 ++
 1 file changed, 2 insertions(+)
$ git -C mori-shokunin log --oneline 5b295ee…..8be2717b… -- corpus/SOURCES.md
c419fe6d round-56 data: driver-liveness probe + dual-shape vote binder, entries, S544/S545, fixtures, receipts
```

The full diff is exactly two `+` lines and zero `-` lines: S544 and S545
appended as the last two table rows (file lines 324–325), immediately before
the blank line preceding `## Paths` (line 327). A +2/−0 diff cannot modify any
other line; the single touching commit rules out add-then-revert churn. Row
ids at freeze are strictly increasing S001→S545, so the new rows are also
positionally last. At `5b295ee…` the file has 389 lines, neither `S544` nor
`S545` matches anywhere (`grep` exit 1). Append-only: holds.

### 2. Shape

Headings at freeze (all at column 0):

```
1:# SOURCES — where mori learns          (<id>=mori: correct)
3:## Registry
327:## Paths
337:## Search log
382:## Leads (unopened)
```

Order and spelling match the contract shape block. One anomaly: the last two
`## Search log`–shaped entries, `Round 38 bounded search` (line 389) and
`Round 39 bounded search` (line 391), sit physically *inside*
`## Leads (unopened)` — after its four `- ` bullets (384–387) — as non-bullet
prose paragraphs. Identical bytes at entering tip → pre-existing, not this
round's append.

### 3. Row schema (all 318 rows)

Frozen contract census block, run verbatim against the extract
(`cd <scratch>/freeze`, file `corpus/SOURCES.md`):

```
rows (spacing-tolerant):            318
malformed rows (NF!=13):            0
tier histogram:                     A=287 B=14 C=17
status histogram:                   mined=267 queued=24 rejected=27
duplicate ids:                      (none)
enum violations / tier inflation:   (none)
```

Every registry line has exactly 12 pipes → 11 cells; zero empty cells; ids
unique, `S[0-9]{3,}`, strictly increasing. `opened` all ISO dates ≤ 2026-10-27.

Maintained parser (E-codes + W-codes + E11 disk check against the
reconstituted freeze tree):

```
$ bash scripts/sources-census.sh validate --today 2026-10-27 --file <scratch>/freeze/corpus/SOURCES.md
file  W04  S035 … (23 W04 "duplicate url … across scopes" lines, ids:
  S035,S037,S073,S074,S075,S076,S147,S148,S149,S150,S166,S168,S201,S218,
  S220,S228,S349,S351,S470,S476,S486,S491,S492)
file  ok   …/freeze/corpus/SOURCES.md
exit=0   (W-codes do not affect exit; zero E findings)
```

23 W04 matches the frozen round-56 start census (`evidence/census-start.txt`:
316 rows, 23 W04); 316 + 2 appended = 318. E11 used-by existence: clean over
the committed tree (the earlier "missing: SKILL.md/PROVINCE.md/SCORECARD.md"
hits were artifacts of my partial extraction; all eight root `*.md` exist at
the commit, verified by `git cat-file -e`). E12: no S-row-shaped lines outside
`## Registry`. `## Paths` bullets (329–335) reference only existing ids
(including S230, S231).

### 4. 0-3 leading-space parser rule

Leading-space histogram over all 391 lines: `{0: 353, 1: 7}`. The seven
single-space lines are the ` - ` bullets of `## Paths` (329–335); `## Leads`
bullets sit at column 0. No line carries ≥4 leading spaces, no tabs, no
trailing whitespace (`grep -nE ' $'` exit 1). Every table line and heading is
at column 0 → the frozen column-0 census grammar and the maintained 0–3-space
grammar parse this file identically; no row or heading is dropped by either.

### 5. Pipes in cells

Zero `|`-containing lines outside the Registry table (Paths/Leads/Search-log
prose all pipe-free); zero `\|` escapes; zero Unicode pipe lookalikes
(`‖｜│∣`); every registry row counts exactly 12 pipes. Holds.

### 6. New rows S544/S545 (file lines 324–325)

Both rows: 11 cells, `id` next unused (S543 max at entering tip),
`opened=2026-10-27`, `recheck=on-release`, `status=mined`, kind `own-work`
/`spec` at tier A (permitted; A is scoped, and `community` is the only
kind–tier bar).

Anchor truth (spot-verified):
- S544 anchor `inline.sh launch 149, complete 176, dead 182;
  shokunin-watchdog.sh launch 266, complete 405, dead 448` — the named lines
  in `scripts/hyaku/inline.sh` (`log "launch …"`, `log "complete …"`,
  `log "lane-dead-no-report …"`) and `scripts/shokunin-watchdog.sh` (same
  three emitters) match exactly. `sha256` of committed
  `corpus/evidence/sources-r56/watchdog-log-grammar.txt` =
  `38ba3e6b…f796` — matches the cell.
- S545 anchor `section 1 line 251, section 2 grammar lines 308 and 461` —
  freeze-tree `corpus/evidence/sources-r56/rfc8259.txt` line 251 is "A JSON
  text is a serialized value…", :308 `value = false / null / true / object /
  array / number / string`, :461 `string = quotation-mark *char
  quotation-mark`. Copy `sha256` `61a5378f…cd2d7` matches the cell.
- `used-by` truth: `corpus/knowledge/driver-liveness-r56.md` cites S544 and
  the tool by name (lines 3,13,22,29-38); `corpus/knowledge/vote-binding-r56.md`
  cites S545 and `tools/mori-vote-bind.py` (lines 3,22,31-33,49).

## Findings

No HIGH findings. Everything below is pre-existing data (byte-identical at
entering tip) unless marked otherwise; none is fixed by this seat — the
counters/predicates stay frozen and these route to round 57 or the L1's data
discretion.

- **MED — `corpus/SOURCES.md:389,391`** — `Round 38` and `Round 39` bounded
  search paragraphs are filed inside `## Leads (unopened)` (heading at :382,
  bullets :384–387), not under `## Search log`. Two violations of the shape
  contract in one: `## Leads` is specified as "bullets; a lead is not
  evidence" yet holds prose search-log entries, and two searches are absent
  from their own section (plus stray blank lines :379–381). Cosmetic to both
  parsers but wrong for any reader or scribe that slices by section.
- **MED — `corpus/SOURCES.md:65` (S059)** — `anchor` and `teaches` contents
  are swapped: the `teaches` cell is the bare word `rejected`, while the
  contract-mandated `REJECTED: <reason>; flip: <condition>` text (including a
  real flip clause) sits in the `anchor` cell. Passes the awk census because
  enums and NF are unaffected, but the row's teaches field does not carry the
  rejection rationale where every other rejected row puts it.
- **LOW — `corpus/SOURCES.md:305`** — a blank line inside the Registry table
  between S525 (r54 block end) and S526 (r55 block start). Tolerated by both
  lane parsers (line-based, not block-based); splits the single pipe table
  for strict Markdown-table parsers.
- **LOW — `corpus/SOURCES.md:172,174,184,185,217` (S166/S168/S178/S179/S211)**
  — rejected rows whose `teaches` uses the older `Rejected round NN: …`
  wording without the contract's `; flip:` clause, and whose `anchor` is `—`
  (the contract requires "exact section / heading / page / line plus
  revision; never a bare homepage"). S211 additionally is a rejected row that
  opens `supersedes S179 —` (a superseder over a rejected duplicate), and
  S211's `used-by` is `corpus/lessons/round-32.md` on a `rejected` row —
  tolerated by the contract but worth noting.
- **LOW — `used-by` domain drift, incl. this round's rows** — contract cell
  spec: "repo-relative paths of the knowledge entries or lessons citing the
  row". 27 cells cite outside that: `tools/…` (S153–S155, S191–S193, **S544
  :324, S545 :325** — new rows extend the convention), `SKILL.md` (12 rows:
  S076, S134–S136, S145, S148, S150, S194–S196, S201–S202), `PROVINCE.md` (6),
  `SCORECARD.md` (2). Long precedent (earliest r29-era), so a named
  contract-vs-practice limit rather than a new defect; the S544/S545 tool
  citations do exist and are honest.
- **LOW — Search-log coverage gap** — notes exist for rounds 1–24, 30, 37,
  46, 53 (+addendum) and the displaced 38/39; 92 rows were opened
  2026-10-24→10-27 (r40–r55) including new-ground rounds 54 (S515–S525,
  memory-failure) and 55 (S526–S543) with no `## Search log` note. UNVERIFIED
  whether those rounds ran "bounded searches" (some were lead-driven
  re-opens); the contract demands one prose note per bounded search, so this
  is an evidence gap, not a proven rule-5 breach. Round 56 itself has no note
  at freeze — expected: the w1 scribe seat drafts it this wave.
- **LOW — `recheck` vocabulary** — contract names ISO date or cadence
  "`90d`, `180d`, `on-release`"; the file also carries `365d` (20 rows) and
  `per-closure` (S200, :206). The maintained parser accepts any symbolic
  cadence, but the frozen cell spec is narrower than practice.
- **LOW — stale `## Leads` bullets :384,:386** — the round-20 bullet
  self-describes as resolved ("source admitted round 20 … opened … as S070,
  narrowed by S075") and the round-53 lead bullet is closed by the round-54
  bullet beneath it. Ledger hygiene only; no contract clause requires
  removal.
- **Observation (no violation) — sparse id space** — 318 rows span S001–S545;
  227 ids absent in ranges S236–S240, S242–S261, S263–S346, S352–S469.
  Consistent with "next unused; never reused" (dropped candidate ids, no
  reuse detected); recorded because a reader may expect contiguity.

## Limits

- External sources were not re-opened (no network); `anchor`/`teaches` truth
  is verified only for S544/S545. E11 used-by existence is over the committed
  tree, so post-freeze deletions would not show.
- W04 (duplicate URL across scopes, 23 rows) is an accepted warning class in
  the maintained vocabulary, not a contract violation; reported for
  completeness since the wave contract pins the count.
- The maintained `sources-census.sh` is a fleet-root script executed
  read-only against my scratch copy of the registry; it mutated nothing.

Scratch: `/fast/scratch/hyaku/mori-r56/Mo56RevSourcesContract/` (removed on
exit). No installs; no fleet writes; no journal counting by MESSAGE.
