# ExecCollisionGuard — C3 assimilation id-collision guard (round 44, wave 1)

Seat: leaf executor. Wrote exactly this file. No lane byte, frozen instrument, `SKILL.md`,
`SCORECARD.md`, `LOG.md`, `corpus/` file or fleet/sibling repo was modified. No git or jj
mutating command. All work in `mktemp -d` sandboxes under `/tmp`; nothing installed
(no `pacman`, `uv tool`, `npx` or binary channel used — the tools needed were already present).

Sandboxes (fresh, kept for inspection until /tmp is cleared):

| sandbox | what it holds |
|---|---|
| `/tmp/mori44-guard.EeqBAj` | rows built from the staged campaign rows, `guard/` indented-row fixture, `corpus/` (corpus-only mirror, used to show `E11` resolves at the lane root), `mirrorA/` (HEAD registry + my staged-derived rows), `mirror/` (working-tree copy + the two duplicate-id controls), `mirror2/` (HEAD registry + the two landed rows), `mirror3/` (renumbered 134-row staged block appended) |
| `/tmp/staged_c3_rows.txt` | staged `SOURCES.append.md` lines 26–27 (S490, S491 — the two C3 documents) |
| `/tmp/staged_471_472.txt` | staged `SOURCES.append.md` lines 7–8 (S471, S472 — the two gihyo.jp documents) |
| `/tmp/renumber_map.tsv` | verified 136-entry staged→lane renumber map |
| `/tmp/renumbered_block.md` | the 134-row renumbered append block used for the transform-before-append measurement |

Timing fact that matters for every count below: the lane registry moved **under this seat**.
At my first read `corpus/SOURCES.md` held **243** rows (max id `S470`) and `git show
HEAD:corpus/SOURCES.md` also held 243; by my later reads the working tree held **245** rows
with `S471`/`S472` already landed (`git -C … diff --numstat -- corpus/SOURCES.md` → `2 0
corpus/SOURCES.md`). I did not write to the lane; a sibling seat landed those two rows while I
worked. Both readings are reported, and the census receipts are built from **HEAD bytes + the
two rows**, so they do not depend on that drift.

Entering/instrument commit: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD`
→ `7cb59c6891d4f5d0266fe062565f094da835dc84` (the frozen-instrument commit; the contract's
entering tip `1429c791…` is an ancestor state, not HEAD).

---

## 1. Lane ids

```
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md \
  | grep -oE 'S[0-9]+' | sort
```
→ 243 ids at the first read (tail: `S347 S348 S349 S350 S351 S470`), 245 at the later read
(S471, S472 appended). Deduped counts:

```
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' …/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort -u | wc -l
243          # first read (== git show HEAD:corpus/SOURCES.md | … | wc -l → 243, max id S470)
245          # later read, after the sibling landed the C3 rows
$ … | sort | uniq -d
(no output: no duplicate id at either reading)
```

Id space ends at `S470` in 243 allocated ids; the unallocated gaps below it are
`S236-S240`, `S242-S261`, `S263-S346`, `S352-S469` (227 ids never allocated), so `S471` is the
first free id and the staged block's start is not an accident.

## 2. Staged ids

```
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/mori/SOURCES.append.md \
  | grep -oE 'S[0-9]+' | sort -u > /tmp/staged_ids.txt
$ wc -l < /tmp/staged_ids.txt
136
$ head -1 /tmp/staged_ids.txt ; tail -1 /tmp/staged_ids.txt
S471
S606
```
136 unique ids, **contiguous `S471`–`S606`** (`missing = []` over 471..606). The staged block
starts exactly at the first id the entering lane had not allocated — which is why a verbatim
append lands on the C3 ids.

## 3. `comm -12` — collision count

```
$ comm -12 /tmp/lane_head_ids.txt /tmp/staged_ids.txt ; echo "count=$(comm -12 … | wc -l)"
count=0
```
**Collision count at the entering registry (243 rows, max S470) = 0.** Neither `S471` nor
`S472` was allocated there, so the staged numbering lined up with the lane's next free ids —
a coincidence of the entering state, not a document-level agreement (the staged block and the
lane use those two numbers for different documents; see the live reading below).

```
$ comm -12 /tmp/lane_live_ids.txt /tmp/staged_ids.txt ; echo "count=$(comm -12 … | wc -l)"
S471
S472
count=2
```
**Collision count at the live working tree (245 rows) = 2, ids `S471` and `S472`.** The
colliding *documents* (id cell → source cell, from `SOURCES.append.md`):

| id | staged document (the collider) | lane document now holding the id |
|---|---|---|
| `S471` | 第61回 Linuxカーネルのコンテナ機能 - cgroup v2から使うメモリコントローラ（6） — `https://gihyo.jp/article/2026/03/linux_containers-0061` | proc(5) 日本語訳 (Ubuntu 20.04 focal) — `https://manpages.ubuntu.com/manpages/focal/ja/man5/proc.5.html` |
| `S472` | 第56回 Linuxカーネルのコンテナ機能 ーcgroup v2から使うメモリコントローラ（1） — `https://gihyo.jp/article/2024/08/linux_containers-0056` | proc(5) 中文翻譯 (Arch Linux, zh_TW) — `https://man.archlinux.org/man/proc.5.zh_TW` |

The two C3 documents exist in the staged campaign under **different** ids, found by URL:

```
$ grep -nE 'manpages\.ubuntu\.com/manpages/focal/ja/man5/proc\.5\.html|man\.archlinux\.org/man/proc\.5\.zh_TW' SOURCES.append.md
… S490 -> proc(5) 日本語訳 (Ubuntu 20.04 focal) — https://manpages.ubuntu.com/manpages/focal/ja/man5/proc.5.html
… S491 -> proc(5) 中文翻譯 (Arch Linux, zh_TW) — https://man.archlinux.org/man/proc.5.zh_TW
```

**Verdict: the staged id must be renumbered in scratch, by document.** The id follows the
document, not the staged offset: staged `S490` (Ubuntu ja proc(5)) → lane `S471`, staged `S491`
(Arch zh_TW proc(5)) → lane `S472`, and the staged block's own `S471`/`S472` (the two gihyo.jp
cgroup articles) must move off the C3 slots. Verified map (`/tmp/renumber_map.tsv`):

```
S471 -> S473  S472 -> S474  S473 -> S475  S474 -> S476  S475 -> S477  S476 -> S478
S477 -> S479  S478 -> S480  S479 -> S481  S480 -> S482  S481 -> S483  S482 -> S484
S483 -> S485  S484 -> S486  S485 -> S487  S486 -> S488  S487 -> S489  S488 -> S490
S489 -> S491  S490 -> S471  S491 -> S472          # the two C3 documents land on the lane ids
S492..S606 unchanged                              # 115 identity entries
```
Rule in words: drop the two C3 documents from the staged block (they are the lane's S471/S472),
then pack the remaining 134 rows, in staged order, into `S473..S606` — which is exactly
`S471..S489 → +2`, `S492..S606 → identity`, `S490/S491 → S471/S472`. Verification:

```
distinct targets: True   min/max: 471 606
contiguous 471..606: True
id clash with C3 S471/S472: []
appended rows: 134   first id: S473   last id: S606
```

Cell-level cross-references also need the map: the staged block contains **56 references to
staged ids inside cells** (e.g. `S519` scope names `S518`; `S539` teaches names `S540`). Under
this particular map **0 of the 56 change value** (every reference points at `S492`–`S606`,
which are identity), but the transform must still run the map over cell text — a future staged
block that cites `S471..S491` would otherwise point at the wrong document after renumbering.

### Negative controls (census catches both failure modes)

Control A — append the staged `S471`/`S472` rows verbatim next to the C3 rows
(`mirror/lane/corpus/SOURCES-idclash-control.md`):

```
$ sources-census.sh validate --file …/SOURCES-idclash-control.md ; echo EXIT=$?
file	E01	S471 fields=12
file	E03	S472 duplicate id
EXIT=1
```
The id collision is the `E03`; the `E01` on `S471` is the escaped-pipe defect of §6 showing up
in the same row (the census stops treating a 14-field row as a row at all).
Control B — append the staged C3 documents verbatim under their campaign ids
(`SOURCES-dupe-control.md`), i.e. the same document twice:

```
file	E04	S490 duplicate url manpages.ubuntu.com/manpages/focal/ja/man5/proc.5.html within scope …
file	E04	S491 duplicate url man.archlinux.org/man/proc.5.zh_TW within scope …
EXIT=1
```
So an id-level collision surfaces as `E03` and a document-level duplicate as `E04`; the
renumber-by-document rule removes both (see §6: `E03=0`, `E04=0`).

## 4. The indented-row guard

Fixture `/tmp/mori44-guard.EeqBAj/guard/SOURCES.md` — a `## Registry` table with three data
rows: `| S001 |` at column zero, `  | S471 |` indented by two spaces, and a control row
`    | S472 |` indented by four (outside the parser's declared 0–3 bound).

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}' guard/SOURCES.md
1                                   # column-zero-only pattern: sees S001, misses S471
$ grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' guard/SOURCES.md
2                                   # 0-3-space pattern: sees S001 and S471
$ grep -oE '^\|[[:space:]]*S[0-9]+' guard/SOURCES.md
| S001
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]+' guard/SOURCES.md
| S001
  | S471
```

Counts: **column-zero-only = 1, 0–3-space = 2.** The four-space control is missed by both,
which is correct: `sources-census.sh` declares "0–3 leading ASCII spaces before Markdown
rows/headings" (`scripts/sources-census.sh:40`, `row_pass()` at `:574`), so a 4-space row is
not a row to the parser either. The census's own view of the same fixture agrees with the
guarded pattern, not the naive one:

```
$ sources-census.sh census --file guard/SOURCES.md | grep rows
file	rows	2
FLEET	rows	2
$ sources-census.sh validate --file guard/SOURCES.md ; echo EXIT=$?
file	W03	S471 mined but unused
file	ok	/tmp/mori44-guard.EeqBAj/guard/SOURCES.md
EXIT=0
```
`rows=2` and the `W03` finding naming `S471` prove the parser *did* read the indented row; a
column-zero-only extraction would have under-reported the registry by one and disagreed with
the census. (On the committed lane registry both patterns happen to agree — 245 = 245 — because
every lane row is column-zero; the guard is what keeps an extraction honest if that ever
changes.)

## 5. `sources-census.sh validate --file` on a scratch mirror

Mirror built from **HEAD bytes** (`git show HEAD:corpus/SOURCES.md`, 243 rows) plus the two
proposed rows inserted at the end of the `## Registry` table (after the `S470` row, before
`## Paths`), inside a full copy of the lane tree so `used-by` paths resolve
(`E11` tests `dirname(registry)/..` + path, `scripts/sources-census.sh:538-570`). Measured: a
mirror holding only `corpus/` is **not** enough — the first attempt exited 1 with 26 `E11`
findings over 5 distinct paths naming `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`,
`tools/mori-disk-rate.py` and `tools/fixtures/mori-oom-killers/cases-a2-r29.json`, i.e.
`used-by` is resolved against the lane root, not against `corpus/`.

Rows tested — **two variants**, because `ScribeRowsDraft.md` did not exist when this seat
started (`ls .ufo/waves/round-44/w1/` showed only ExecGateInventory, ExecJunkLedger,
ExecMisrootSweep, MutRegistry, ScoutConsider, ScoutR43Wording):

- **Variant A (fallback, built by me from the staged campaign rows for the two URLs)** —
  staged `S490`/`S491` renumbered to `S471`/`S472`, cells taken verbatim from
  `SOURCES.append.md` except `status=mined`, `opened=2026-10-25`, `recheck=180d`,
  `used-by=corpus/knowledge/pid-probe-conclusion-r44.md` (the cells the C3 row spec fixes).
  `NF=13` for both; no literal or escaped `|`; the entry file resolves in the mirror (it exists
  in the working tree, and `E11` reads existence only). **Flag on this variant: `teaches` is
  33 words (S471) and 42 words (S472)** — the C3 row spec caps it at 25, so the staged teaches
  sentence cannot be appended unshortened.
- **Variant B (the rows that actually landed, i.e. the draft's visible form)** — the working
  tree's `| S471 |`/`| S472 |` rows (taken by exact prefix from `corpus/SOURCES.md`), `NF=13`,
  no literal or escaped `|`, `teaches` 22 / 24 words, `opened=2026-10-25`, `recheck=180d`,
  `used-by=corpus/knowledge/pid-probe-conclusion-r44.md` (which exists in the tree, so no
  placeholder is needed).

Results:

```
# Variant A — /tmp/mori44-guard.EeqBAj/mirrorA/lane/corpus/SOURCES.md (HEAD 243 + my 2 staged-derived rows)
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$SB/mirrorA/lane/corpus/SOURCES.md"
…
file	ok	/tmp/mori44-guard.EeqBAj/mirrorA/lane/corpus/SOURCES.md
EXIT=0
# 20 output lines = 19 W04 (pre-existing duplicate-URL warnings) + the ok line; 0 E-codes; no S471/S472 finding

# Variant B — /tmp/mori44-guard.EeqBAj/mirror2/lane/corpus/SOURCES.md (HEAD 243 + the two landed rows)
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$SB/mirror2/lane/corpus/SOURCES.md"
…
file	ok	/tmp/mori44-guard.EeqBAj/mirror2/lane/corpus/SOURCES.md
EXIT=0
# 19 warnings (W04), 0 E-codes, no S471/S472 finding
```

**Exit code 0 in both variants; last output line `file	ok	<scratch path>`.** Row count and
tier/status effect of the append, same file:

```
$ sources-census.sh census --file "$SB/mirror2/lane/corpus/SOURCES.md" | grep ^FLEET
FLEET	rows	245
FLEET	tier.A	214
FLEET	tier.B	14
FLEET	tier.C	17
FLEET	tier.invalid	0
FLEET	status.queued	25
FLEET	status.mined	194
FLEET	status.rejected	26
FLEET	status.invalid	0
FLEET	missing	0
```
243 → 245 rows, `tier.A` 213 → 214 (S471), `tier.B` 13 → 14 (S472), `status.mined` 192 → 194,
`invalid 0`. This matches the contract's after-value ("registry 245 rows (S471, S472) with
census exit 0") and the live lane census (`rows 245`, `invalid 0`).

## 6. Transform-before-append, measured

`/tmp/mori44-guard.EeqBAj/mirror3` = working-tree lane mirror + the **renumbered** 134-row
staged block (C3 documents dropped, ids `S473..S606`, cell id-references mapped) appended to
the registry (245 → 379 rows):

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$F" > v3.out 2>&1 ; echo EXIT=$?
EXIT=1
$ grep -oE 'E[0-9]{2}' v3.out | sort | uniq -c
      5 E01
      2 E09
    126 E11
$ grep -cE 'E0[34]' v3.out
0
$ tail -1 v3.out
file	E11	S606 missing used-by corpus/knowledge/journal-boots-read-r52.md
```
- `E03 = 0`, `E04 = 0`: renumbering by document removes the id collision and the
  same-document duplicate — the guard's actual job, done.
- `E01 = 5` — **five staged rows are malformed before any append**: `S473` (=staged `S471`),
  `S502`, `S503`, `S504`, `S505` carry `NF=14` because a cell holds an escaped pipe
  (`… grep -ciE 'inotify\|POLLPRI' corpus/SOURCES.md -> 0 …`). Census row grammar is
  `awk -F'|'` with no unescaping, so the escaped pipe splits the row. The append transform must
  de-pipe those five cells; renumbering alone does not make the block appendable.
- `E09 = 2` — `S501`, `S506` have free-text `recheck` cells (`180d — \`aaron papers fetch …\``,
  `90d — \`wc -l < …\``) where the lane schema wants a bare cadence/date.
- `E11 = 126` findings over **77 distinct `used-by` paths** (`corpus/knowledge/quota-observability-r38.md`,
  `… journal-boots-read-r52.md`, …) that do not exist in the lane — expected for a campaign
  corpus, and the reason a wholesale staged append is not an append: those paths must land as
  lane entries (or the rows must not be appended).

## What this establishes, and what it does not

Establishes, with the commands above: the C3 id pair `S471`/`S472` was free at the entering
registry (0 collisions over 243 ids); the staged campaign reuses `S471`/`S472` for two
different documents (gihyo.jp cgroup-v2 articles) and holds the C3 documents at `S490`/`S491`,
so assimilation must renumber **by document** (`S490→S471`, `S491→S472`, block shifted to
`S473..S606`); the 0–3-space id pattern sees an indented row the column-zero pattern misses
(2 vs 1, corroborated by the census's own `rows=2`); and `sources-census.sh validate --file`
over a scratch copy of the lane registry plus the two proposed rows exits **0** with last line
`file	ok	<scratch path>` (both the staged-derived rows and the landed draft rows), yielding
`rows 245`, `invalid 0`.

Does not establish (out of this seat's scope): the `count-c3.py` verdict, the registry-row
prose quality (teaches ≤ 25 words, anchor locatedness), the knowledge entry's content, the
frozen instruments' hashes, or any committed state — nothing here is committed, and the
census receipts come from scratch mirrors, not from the lane.

Risks routed to the integration owner:

1. **Lane drift mid-wave** — the registry gained `S471`/`S472` while this seat ran (243 → 245,
   `git diff --numstat` = `2 0`). Any later seat that re-extracts ids must re-run `comm -12`:
   the answer is 0 at HEAD and 2 at the working tree, and only the working-tree answer matches
   what the lane will commit.
2. **Variant A's `teaches` overruns the 25-word cap** (33 / 42 words) — if the draft's rows are
   not the ones that land, they must be shortened before append.
3. **Staged block is not appendable as-is** even after renumbering: 5 `E01` rows (escaped
   pipe), 2 `E09` rows (free-text recheck), 126 `E11` findings over 77 paths. Append only after
   de-pipe + cadence fix + entry landing, and re-validate.
