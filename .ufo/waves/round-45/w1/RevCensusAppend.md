# RevCensusAppend — census-conformance review of the round-45 append (before it lands)

Lane: mori (`/home/vgpnk/Projects/shokunin/mori-shokunin`). Entering tip `3ad8faaa`.
Role: census-conformance reviewer on the round's append block + validate mirror. I wrote nothing
outside this report and `.ufo/waves/round-45/tmp/RevCensusAppend/` (instruments + scratch).

## Artifacts at final measurement (2026-10-25 07:55)

| artifact | digest / size |
|---|---|
| `assimilation/append-block.md` | `5bc42cf746724878895b885576169a599cd67729703f1c9e12aa082f3e262ebc`; its one row line = `d7ac69926608e76074183c44febe212cc38309557ac86231a3b7988eba0285b6` (row + `\n`, verified) |
| `assimilation/validate/corpus/SOURCES.md` (mirror registry, 246 rows) | `fc4b1f2c974a19b3a09784dc01148699012da65437285d66c3257063dd462fd3` |
| `corpus/SOURCES.md` (lane registry, 245 rows, max **S472**) | `d1381d4f560cf00fb3542872a969549c986289f65a242c5e714c8197e2929dc8` |
| `assimilation/renumber-map.tsv` | `f4724c8704ff4f23dfd314b0dda7a4617902cb3f0d297eab0285bc5a8507b513`; 162 lines = 26 comments + 136 rows |
| entry — lane = mirror | `b066d2dd1361c6cdd953186d58ac364366751ae9d0b89cbb8911e5d14c9e8483` (both sides) |
| lesson — lane / mirror | lane `48964480a219b4bc2dd62e53084ca36330fb75ec4d590728074809cfd7647265` (07:54:12) / mirror `359e0cb648adff6a05f8aa5a613bc411a28ba8aaceff8e644e0b906536db6ca5` (07:53:13) |

**Verdict on the drafted row itself: conformant — no finding on S473.** Two things are open:
item 5 on one file (F1, the lesson, which is still being written) and F3 (the lesson publishes a
renumber map that does not exist).

## Findings

### F1 — OPEN at the final measurement (item 5): the entry now matches; the lesson does not

```
$ compare_mirror.sh <lane> …/assimilation/validate
-- files present in lane, missing from mirror:  (none)
-- files whose bytes differ:
corpus/lessons/round-45.md lane=48964480…47265 (07:54:12) mirror=359e0cb6…b6ca5 (07:53:13)
-- files present in mirror but not in lane:     (none)
-- counts: lane=329 mirror=329 missing=0 differing=1 extra=0
compare rc=1
$ diff -rq corpus …/validate/corpus
Files corpus/SOURCES.md … differ                  <- intended: the appended row
Files corpus/lessons/round-45.md … differ         <- not intended
```

Each state below is a measurement, taken minutes apart while other seats wrote `corpus/`:

| time | entry lane / mirror | lesson lane / mirror | compare |
|---|---|---|---|
| 07:46 | `67049708` / `1f28dd38` (one body hunk: `(7 words)` → `(two lines, 9 words)`, `:3906 (4 words)` → `(10 words)`) | absent | 1 differing + 1 missing |
| 07:49 | `f94b8326` / `1f28dd38` | `f7a6dbc4` / added | 1 differing |
| 07:52 | `b066d2dd` / `c06245fc` | `ceb73ce2` / `805e26c7` | 2 differing |
| 07:54 | `b066d2dd` = `b066d2dd` | `359e0cb6` = `359e0cb6` | 0 differing |
| 07:55 | `b066d2dd` = `b066d2dd` | `48964480` / `359e0cb6` | 1 differing |

Six entry digests and five lesson digests were observed in eleven minutes. The mirror is a
snapshot of a tree that is still being written, so "mirror == lane" has a shelf life of seconds,
and the census cannot detect the drift (`rc=0` in every row above — it checks existence and the
`source:` line only). **Standing control:** run `diff -rq corpus <mirror>/corpus` last and print it
with the digest pair; exactly one differing file (`SOURCES.md`) is the pass condition. Item 6 is
not a control for item 5.

### F2 — item-text defect: a `corpus/`-only mirror cannot pass E11

`validate --file` resolves used-by existence against `dirname(file)/..` = the mirror root
(`sources-census.sh`: `resolve_targets` → `usedby_findings`: `[ -e "$dir/$path" ]`). Built
literally from item 3 (copy of `corpus/` + the row):

```
$ sources-census.sh validate --file …/mymirror/corpus/SOURCES.md
rc=1
file	E11	S076 missing used-by SKILL.md          (… 26 E11 lines …)
file	E11	S202 missing used-by SKILL.md
E codes: 26
```

All 26 are five targets, every one outside `corpus/`:
`PROVINCE.md  SCORECARD.md  SKILL.md  tools/fixtures/mori-oom-killers/cases-a2-r29.json  tools/mori-disk-rate.py`.
Copying exactly those five into the same mirror yields `rc=0`, `E=0`, `W04=19`, `file ok`. The
delivered mirror is a whole-lane-tree copy (27 MB, no `.git`) and satisfies E11 — keep that, and
fix the item wording so round 46 does not build the corpus-only variant.

### F3 — SERIOUS (id space): the round lesson publishes a renumber map that does not exist, and its routing lands on S473

`corpus/lessons/round-45.md:143-144` (bytes at 07:55; the file moved five times, so pin by quote):

```
`assimilation/renumber-map.tsv` is 136 lines, ascending in staged order, one
target above the registry maximum: `S471→S473` … `S606→S608`.
```

`corpus/lessons/round-45.md:172` (M8) cites `assimilation/renumber-map.tsv:1` (`S471\tS473`).
Measured against the map on disk:

```
$ grep -cP '^S471\tS473\t' renumber-map.tsv     -> 0
$ sed -n '1p' renumber-map.tsv                  -> # renumber-map.tsv — mori lane, round 45 (built 2026-10-25 by ExecAssimCensus)
$ grep -nP '^S471\t|^S606\t' renumber-map.tsv
27:S471	S474	7	S232	shifted +3 (S473 reserved)
162:S606	S609	142	—	shifted +3 (S473 reserved)
$ wc -l renumber-map.tsv                        -> 162   (136 data rows)
```

The bytes that cause it: lesson `S473` where the map holds `S474`, lesson `S608` where the map
holds `S609`, and the cited line `1` where the map's S471 row is line `27` (line 1 is a comment).
The map itself is correct — 136 rows, uniform +3, S473 absent from all targets, targets 474–609
above registry max 472 — but a next-round bulk append that follows the lesson instead of the map
lands a staged row on **S473**, this round's own row → `E03 duplicate id`. M8's own fix ("reserve
every id named by the round's own admitted rows") is already applied in the map, so its "today"
clause is false as well. The lesson needs the map's current bytes and line 27.

### F4 — residual: the block file is 18 comment lines + 1 row

The HTML provenance comment is not a row, so the census ignores it and E12 cannot fire — but the
block must be pasted **row-only**; pasting the file verbatim lands the comment inside `## Registry`.

### F5 — dependency (blocks C3, not the append)

The lesson exists and its `## Gate` records S473 (`:33`: URL, `07:42:13`, http 200, 133236 B,
sha256 `a9433bb0…b7ad`, quotes of 22/10/17 words with anchors, `**admitted S473**`) — SOURCES
rule 1 is satisfied. **Still absent:** `corpus/README.md` has no `census-cgroup-levels-r45` row
(`grep` → rc=1), so P-C3 item 4 is unmet.

## The six checks

### 1. Columns — split on unescaped `|`: 11 cells, no `\|`, no prose recheck

```
$ python3 revparse_rows.py …/append-block.md --registry corpus/SOURCES.md
row line 19: id=S473 cells=11 escaped=False recheck='180d'
  clean
# problems=0
$ awk -F'|' '/^\| S473 /{print "NF="NF" fields="NF-2}' …/validate/corpus/SOURCES.md     -> NF=13 fields=11
$ awk '/^\| S473 /{print gsub(/\\\|/,"&")}' …/validate/corpus/SOURCES.md                 -> 0
```

Cells: `id=S473` · `source`(173) · `kind=docs` · `tier=A` · `scope`(403) · `anchor`(365) ·
`teaches`(340) · `status=mined` · `opened=2026-10-25` · `recheck=180d` ·
`used-by=corpus/knowledge/census-cgroup-levels-r45.md`.

The parser was shown able to fail before it was trusted: 5 mutants (`fixture-mutants.md` — 12-column
row, escaped `\|`, prose recheck `180d — `curl …``, duplicate id, registry collision) all flagged
(`COLUMNS=12`, `ESCAPED_PIPE`, `RECHECK=… (prose/invalid)`, `ID_DUPLICATE_IN_BLOCK`,
`ID_COLLIDES_WITH_REGISTRY line 251`), `problems=7`, rc=1. On real data it flagged the fleet
staging file: 5 escaped pipes (staged S471, S502–S505) and 6 prose rechecks (staged S501–S506) —
**independently the same counts the map header now declares** (`renumber-map.tsv:21-23`).

### 2. Id space — S473 free, ascending, unique; map reserves it (lesson drift: F3)

```
registry rows=245  max_id=S472  duplicate ids=0
drafted S473: not in registry; single row, so no intra-block order to violate
renumber-map.tsv: 136 rows, 5 cols, 471-606 -> 474-609, uniform +3, unique,
                  S473 not a target, min target 474 > registry max 472
collisions file: S471, S472 (= staged ∩ registry; verified exactly)
```

### 3. `used-by` — one path, exists, cites S473 in a `source:` line

```
$ grep -n '^source:' …/validate/corpus/knowledge/census-cgroup-levels-r45.md
3:source: S473 — https://cdn.jsdelivr.net/gh/torvalds/linux@v7.2/Documentation/admin-guide/cgroup-v2.rst — …
check_merged.py: used-by misses: drafted=0 all_rows=0
```
Every entry revision observed keeps the same `source: S473` line, so the citation holds across
the F1 drift.

### 4. `status` / `opened` / `recheck`

`mined` · `2026-10-25` (ISO, equals today → not `>today`, E08 cannot fire) · `180d` (matches
`^[0-9]+d$`). kind `docs`, tier `A`, tier-inflation n/a.

### 5. Mirror reproduces lane `corpus/`? 328 of 329 at 07:55 — the differing file is the lesson (F1)

Registry diff is a clean append:

```
$ diff -u corpus/SOURCES.md …/validate/corpus/SOURCES.md
hunks=1  added=1  removed=0
@@ -249,6 +249,7 @@
+| S473 | Control Group V2 — the aggregation scope of the memory interface, kernel v7.2 (rst) | …
 (blank)
 ## Paths
```
No reordering, no touched neighbour rows, inserted inside `## Registry` after S472.

### 6. Census run (me, not the executor's paste)

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --file …/assimilation/validate/corpus/SOURCES.md
rc=0
E codes: 0
W codes: W04 x19  (S035 S037 S073 S074 S075 S076 S147 S148 S149 S150
                   S166 S168 S201 S218 S220 S228 S349 S351 S470)
file	ok	…/assimilation/validate/corpus/SOURCES.md
```
The W04 id set is byte-identical to the lane baseline run (`diff w04-base.txt w04-exec.txt` →
empty); the baseline is also `rc=0` with the same 19 W04 and no E. The appended row adds no code of
either kind and the insertion shifted no parse.

## Residual risk and verification gaps

- **R1** The mirror is a moving snapshot (F1): stale at three of five measurements and clean once.
  Item 5 passes only if the refresh is the last step before the receipt, with `diff -rq` printed.
- **R2** Adjacent count drift: the Gate says the entry is "122 lines, mtime 07:44"
  (`round-45.md:61`); the entry was 47 lines at 07:45 and 66 lines at 07:49 (`wc -lc` → `66 8140`).
  No 122-line version is observable — a count must carry its command.
- **R3** A green `--file` run is evidence about the mirror only; the same command on the lane
  registry is also `rc=0` (19 W04).
- **R4** `corpus/README.md` coverage row absent (F5).
- **R5** `contract.md` gained a "Correction 1" section during this review (+28 lines, no predicate
  rewritten), tightening C1/C2 and requiring C3's `--entering-rev` with entry absence. None of the
  six checks here depends on it — the census schema (`CORPUS.md` v1) is unchanged — but the
  contract was read at the amended revision.
- Line numbers inside `corpus/lessons/round-45.md` moved four times during the review; F3's
  citations are for the 07:55 bytes and should be re-derived by quote.
- No tool installed or upgraded; no pacman transaction.
- Instruments (scratch): `revparse_rows.py`, `check_merged.py`, `compare_mirror.sh` + mutant
  fixtures and their outputs (`mutants-run.txt`, `mymirror-validate*.txt`, `staged-scan.txt`).
