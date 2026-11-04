# Mo79Sc01Recon — bounded data walk for round-79 w1 integration (read-only)

Seat: `Mo79Sc01Recon`, leaf, no subagent dispatch. Detection and report only: this file is my
only write. No clone, no fixture, no git/jj mutation. Scratch: none created
(`/fast/scratch/hyaku/mori-r79/` exists from other seats; I left no tree in it).

Method note: every line number below is absolute, produced by `grep -n` / `sed -n 'A,Bp'` /
`awk 'NR==N'` anchored to a known start line. `awk` was used for field extraction because the
tool display truncates lines at 768 bytes (`[Some lines truncated to 768 bytes]` notices); the
quoted cell prefixes are the first cell bytes, read with field splitting, not from a truncated
view. No `lsp` device is in this seat's tool inventory, so every symbol→line fact here is
text-located, never semantic proof (these are Markdown files; no language server applies).

---

## 1. `SCORECARD.md` — axes-table geometry

Commands and output:

```
$ wc -l SCORECARD.md
3989 SCORECARD.md
$ wc -c SCORECARD.md
458451 SCORECARD.md
$ grep -n '^## Axes' SCORECARD.md
6:## Axes
$ sed -n '1,9p' SCORECARD.md | cut -c1-90 | cat -n
 1  # mori-shokunin — Scorecard
 2
 3  Axes owned by this lane: **coverage + operability** (fleet-2); all six are scored
 4  here, the owned pair drives the round's axis-move.
 5
 6  ## Axes
 7
 8  | Axis | Score | Evidence pointer | Last change |
 9  |---|---|---|---|
$ grep -nE '^\| (coverage|operability|depth|freshness|calibration|adjacency) \|' SCORECARD.md
10:| coverage | 6 | ...
11:| operability | 7 | ...
12:| depth | 5 | ...
13:| freshness | 5 | ...
14:| calibration | 5 | ...
15:| adjacency | 6 | ...
$ grep -n '^Round-25 correction\|^Round-50 correction\|^## Move log' SCORECARD.md
17:Round-25 correction (C1 item D5): ...
21:Round-50 correction (C1, calibration): ...
31:## Move log
```

Facts:

| item | line |
|---|---|
| `## Axes` heading | **6** |
| table header `\| Axis \| Score \| Evidence pointer \| Last change \|` | **8** |
| separator `\|---\|---\|---\|---\|` | **9** |
| coverage row | **10** |
| operability row | **11** |
| depth row | **12** |
| freshness row | **13** |
| calibration row | **14** |
| adjacency row | **15** |
| last line of the table (= adjacency row; there is no separate closing line) | **15** |
| line 16 | blank (verified: `sed -n '16p;30p'` `od -c` → `\n \n`) |
| Round-25 correction paragraph | **17–19** |
| blank | 20 |
| Round-50 correction paragraph | **21–29** (29 ends `…count-c1.py <rev>`. ) |
| `## Move log` | **31** |

Revision-pinned sha256 (the commit named in the seat brief):

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse 84c6cbc3b47c536a504aaee329c77897d389935e
84c6cbc3b47c536a504aaee329c77897d389935e
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin log -1 --format='%H %ad %s' --date=iso-strict 84c6cbc...
84c6cbc3b47c536a504aaee329c77897d389935e 2026-11-02T21:03:16Z round-78 verifier spot-check (integrator, hyaku): non-author admit/reject
$ git -C ... show 84c6cbc3b47c536a504aaee329c77897d389935e:SCORECARD.md | sha256sum
a4a488c2355a7389db8c5db24ba0efa347eb3f1fa154de59459abeab331a5c69  -
$ git -C ... show 84c6cbc3...:SCORECARD.md | wc -l
3989
$ sha256sum SCORECARD.md
a4a488c2355a7389db8c5db24ba0efa347eb3f1fa154de59459abeab331a5c69  SCORECARD.md
$ git -C ... status --porcelain SCORECARD.md corpus/SOURCES.md corpus/README.md SKILL.md corpus/lessons/round-78.md
(empty)
```

So the worktree file at HEAD is byte-identical to the pinned commit's blob: 3989 lines,
458451 bytes, `a4a488c2…`. HEAD at walk time: `aa53b4856b615a56bd8dbd60e6ddfb94c46499bd`;
`git ls-tree HEAD -- SCORECARD.md` → blob `251e7af16e518bc99a5f50441a7af5f07eb87c6a`.

Current `Last change` cells (4th cell; `awk 'NR>=10&&NR<=15{n=split($0,a,"|"); printf "%d [%s]\n",NR,a[5]}'`),
leading tokens only:

| line | axis | cell begins |
|---|---|---|
| 10 | coverage | `round 47 (improved, score held); round 26 (improved, score held) before the round-50 correction` |
| 11 | operability | `round 51 (improved, score held); round 47 (improved, score held); round 31 (improved, score held) before the round-50 correction; round-37 C2 re-attributed here (score held, 7)` |
| 12 | depth | `round 51 (improved, score held); round 50 (improved, score held); round 49 (improved, score held); round 31 (improved, score held) before the round-50 correction` |
| 13 | freshness | `round 28 (improved, score held); round-37 C2 is re-attributed to operability (round-38 axes-cell correction below) and round 38 claims no freshness move` |
| 14 | calibration | `round 50 (improved, score held); round 49 (improved, score held); round 25 (improved, score held) before the round-50 correction; round-37 claim C1 …` |
| 15 | adjacency | `round 19 (improved, score held)` |

## 2. `corpus/SOURCES.md` — registry geometry

```
$ wc -l corpus/SOURCES.md
448 corpus/SOURCES.md
$ wc -c corpus/SOURCES.md
350654 corpus/SOURCES.md
$ grep -n '^## Paths' corpus/SOURCES.md
376:## Paths
$ grep -n '^| S593 ' corpus/SOURCES.md
374:| S593 | Memory Performance Information (Windows desktop legacy) — …
$ sed -n '370,378p' corpus/SOURCES.md | cut -c1-100 | cat -n
 1  | S589 | time — Time access and conversions …
 2  | S590 | CAPTCHA and Challenge action behavior …
 3  | S591  | Acquiring high-resolution time stamps …
 4  | S592 | typeperf (Windows Commands reference) …
 5  | S593 | Memory Performance Information (Windows desktop legacy) —
 6  (blank)
 7  ## Paths
$ sed -n '1,/^## Paths/p' corpus/SOURCES.md | grep -c '^|'
368
$ sed -n '1,/^## Paths/p' corpus/SOURCES.md | grep -cE '^ {0,3}\|'
368
$ grep -cE '^\| S[0-9]+ \|' corpus/SOURCES.md
366
```

Facts: total **448 lines** (350654 bytes). Last registry row = **line 374** (id **S593**);
line 375 blank; `## Paths` = **line 376** — the registry ends immediately before it.
Row count over `^|` = **368**; over `^ {0,3}\|` = **368** (no indented rows; the strict and
tolerant forms agree). Of those 368, 2 are the header (line 5,
`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`,
11 columns) and separator (line 6), leaving **366 data rows**.

Id continuity (`grep -oE '^\| S[0-9]+ '` → 366 unique ids, min `S001`, max `S593`):

```
235 -> 241
241 -> 262
262 -> 347
351 -> 470
```

So the registry is **not** id-contiguous: 366 rows, max id S593, four gaps, no duplicate ids.

## 3. `corpus/README.md` — knowledge index

```
$ wc -l corpus/README.md
859 corpus/README.md
$ wc -c corpus/README.md
100433 corpus/README.md
$ sed -n '1,10p' corpus/README.md | cat -n
 1  # mori-shokunin — corpus
 2
 3  ## Coverage map
 4
 5  | Note | Holds | Sources |
 6  |---|---|---|
 7  | `knowledge/observability-census-r1.md` | …
…
$ awk 'NR>=7 && /^$/ {print "first blank at", NR; exit}' corpus/README.md
first blank at 51
$ sed -n '850,859p' corpus/README.md | cut -c1-80 | cat -n
 1  | Ground | Entry | Bounded advance |
 2  |---|---|---|
 3  | The rotation-receipt reading grammar (r70–r75 …
 4  (blank)
 5  ## Round-77 knowledge addition — the performance-counter surface …
 6
 7  | Ground | Entry | Bounded advance |
 8  |---|---|---|
 9  | The Windows performance-counter surface (r77, S592) | `knowledge/counter-win-r…
10  | The vendor counter-name association (r78, S593) | `knowledge/counter-semantics-…
$ tail -c 40 corpus/README.md | od -c | tail -3
… o u n d . | \n
```

Facts: total **859 lines** (100433 bytes), file ends with `| \n` (single trailing newline).

- Knowledge index (`## Coverage map`) header = **line 5**, separator 6, first row 7; the table's
  first following blank is **line 51**, so the Coverage-map table is **rows 7–50** (44 rows).
- Per-round index tables (the append pattern a new r79 row must follow): `## Round-76 …` =
  **848**, its header **850**, its single row **852**; `## Round-77 …` = **854**, header **856**,
  separator **857**, rows **858–859**.
- Last index row = **line 859**: `| The vendor counter-name association (r78, S593) | `knowledge/counter-semantics-r78.md` (S593) | …`.

## 4. `SKILL.md` — instrument registry

```
$ wc -l SKILL.md
1352 SKILL.md
$ wc -c SKILL.md
220295 SKILL.md
$ grep -n '^| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |$' SKILL.md | tail -3
1207:…
1271:…
1315:| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
$ sed -n '1314,1330p' SKILL.md | cut -c1-70 | cat -n
 1  (blank)
 2  | name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
 3  |---|---|---|---|---|---|---|---|
 4  | receipt-complete guard (r63 tool) | gate | …
…
15  | counter probe (r77 tool) | probe | …
16  (blank)
17  ## Round76 — reading rotation-schedule receipts (the r70–r75 grammar at the registry h…
$ sed -n '1328p' SKILL.md | awk -F'|' '{print NF-2}'
8
```

Facts: the registry home table is header **1315**, separator **1316**, rows **1317–1328**
(12 rows); its **last row is line 1328** = `| counter probe (r77 tool) | probe | …`.
The table has **8 columns** (`name | kind | entry | verdict map | self-test | pinned values |
write scope | owner`; `awk -F'|'` on line 1328 → `NF-2 = 8`). Line 1329 blank, `## Round76` at
**1330**, file ends at **1352** (the section's prose runs 1330–1352; no further table header
appears after 1315 — 15 tables in the whole file carry that same 8-column header).

## 5. `corpus/lessons/round-78.md` — lesson shape

```
$ wc -l corpus/lessons/round-78.md
204 corpus/lessons/round-78.md
$ grep -n '^## ' corpus/lessons/round-78.md
8:## Fresh start (r59/r60/r61 rejected closures re-read and re-derived; what was ruled out)
53:## Gate
104:## Mistakes
151:## Foreign evidence found in the worktree (disclosure, not a claim)
167:## Wave
175:## Assimilation
185:## Mistakes addendum (post-landing, same round — …)
```

`## Gate` = **line 53**, `## Mistakes` = **line 104** (Mistakes body 104–150; next heading 151).
The same shape holds for `corpus/lessons/round-77.md` (`## Gate` 59, `## Mistakes` 107,
`## Fresh start` 8) — 204 vs 189 lines; both put Gate before Mistakes and both carry the
post-`## Assimilation` addendum.

## 6. Insertion points this walk pins (what L1 needs, derived — not applied)

1. **C2 / axes cells**: edit only the 4th cell of `SCORECARD.md` lines **10–15**; the table's
   geometry (lines 6, 8, 9, 16) and the two correction paragraphs (17–19, 21–29) stay put. If a
   new correction paragraph is wanted, it goes at **line 30** (currently blank, between 29 and
   `## Move log` at 31) or after `## Move log` — line 31 must remain the heading.
2. **C3 / SOURCES row**: insert one row at **line 375** (currently blank) so the registry keeps
   `## Paths` at 376→377. Max id at the walk is **S593**, so a new row is **S594**; a counter
   that derives the next id from the row count (366) instead of the max id would collide.
3. **C3 / knowledge index**: append after **line 859** (EOF), following the `## Round-77 …`
   pattern at 854–859 (`## Round-79 knowledge addition — …`, blank, header, separator, rows).
4. **C1 / instrument registry**: append a new section **after line 1352** (EOF) — the two
   alternatives both disturb committed bytes: inserting inside 1317–1328 renumbers the r77 row
   at 1328 and every later line, which the lane's append-only registry convention avoids — stated
   in the `## Round73` section itself at `SKILL.md:1308`: "The section is append-only at this
   file's end: the `SKILL:905` tally pin … and every earlier line are byte-and-line-number
   unchanged".

## 7. Cross-checks and inconsistencies noticed

1. **MANIFEST vs axes cells (C2's evidence, recomputed here for L1).** Fleet
   `/home/vgpnk/Projects/shokunin/MANIFEST.json`: 3809938 bytes, 1153 `rounds[]` entries,
   67 mori closures, 46 admitted. Latest **admitted** mori closure whose `verdicts[axis]` is
   `improved` or `harmed` (there is no `harmed` and no `improved narrowly` in any admitted mori
   closure; the only odd token is one `unprovable-but-better` on axis `freshness-technique` at
   round 36, not one of the six scored axes):

   | axis | latest admitted improved | axes cell leads with |
   |---|---|---|
   | coverage | **56** | 47 |
   | operability | **78** | 51 |
   | depth | **76** | 51 |
   | freshness | **78** | 28 |
   | calibration | **78** | 50 |
   | adjacency | **19** | 19 |

   Round 78's entry: `admitted: true`, `verdicts = {"operability":"improved","calibration":"improved","freshness":"improved","coverage":"unchanged","depth":"unchanged","adjacency":"unchanged"}`;
   round 77 is `admitted: false`. So five of six cells are stale relative to the MANIFEST
   convention the round-50 correction states, and round 78 is the latest admitted grading for
   three axes — this is the precise reconciliation C2 has to land. Admitted verdict vocabulary
   over all axes/rounds: `improved` 104, `unchanged` 160, `unprovable-but-better` 1.

2. **MANIFEST `commit` is not a bare sha for mori rounds 71–78.** The r78 `commit` value is
   `C:/Users/jpvei/.zcode/workspace/95b1ba4d-…/fleet/mori-shokunin@22dbaae4364425e59c9cbc07d9c83363a6b4426e`
   (tail after `@` = `22dbaae4364425e59c9cbc07d9c83363a6b4426e`). A checker comparing the field to
   `/^[0-9a-f]{40}$/` yields a false red on 71–78; the convention is `<path>@<sha>`.

3. **Sources registry is id-gapped** (366 rows, max S593, gaps 235→241, 241→262, 262→347,
   351→470). Any "next id = count+1" logic is wrong; next id is max+1.

4. **`SCORECARD.md:1781` cited by the freshness cell exists and does contain `5 → 6`**
   (`sed -n '1781p' | grep -o '5 → 6'` → `5 → 6`; the line is a `| C1 freshness, eight carried
   row defects superseded …` claim row). The freshness cell's pointer is honest.

5. **`round-38 axes-cell correction below` cited by the freshness cell exists** at
   `grep -n 'axes-cell correction' SCORECARD.md` → `2181:### Round 38 axes-cell correction
   (append-only note; names the superseded text)`, with the cross-reference also at 2186.

6. **`corpus/README.md` Round21 correction cited by the freshness cell exists** at line 413
   (`## Round21 correction — loss accounting before baseline acceptance`).

7. The seat brief's phrasing "registry table near line 1290-1320" understates its end: the table
   starts at 1315 and its last row is 1328, i.e. it runs past 1320; nothing between 1290 and
   1314 is part of that table.

## 8. Owner defects / limits of this walk

- My first pass read the axes table with `sed -n '/^## Axes/,/^## /p'` and `cat -n`, which
  numbers from 1 at the range start — it would have reported the header as "line 3". Caught by
  re-running `grep -n '^## Axes'` and the explicit `sed -n '1314,1330p'`/`awk 'NR>=10&&NR<=15'`
  anchored form. All numbers above are from the anchored runs.
- All quoted cell text is first-bytes only (tool display truncates at 768 bytes per line); I read
  it with `awk -F'|'` field extraction and `cut -c1-…`, so no conclusion here rests on truncated
  text. Multi-line cells cannot occur (every row is one physical line — confirmed by the column
  counts: 368 pipe-lines for 366 rows + header + separator).
- I did not verify the *content* of the round-78 closure beyond its MANIFEST entry and its
  lesson headings; I did not touch C1's receipt guard, C3's RFC pin, `MANIFEST.json`,
  `.ufo/state/`, counters, or any sibling lane. C1 and C3 remain unverified by this seat.
- No scratch tree, no fixture, no install, no tool upgrade; nothing to clean up.
