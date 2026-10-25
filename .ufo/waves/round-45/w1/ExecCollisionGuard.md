# ExecCollisionGuard — assimilation id-collision guard, r45 w1

Seat: executor (leaf; no spawns, no network fetches). Repo root
`/home/vgpnk/Projects/shokunin/mori-shokunin` (lane), contract read first.
Scratch: `.ufo/waves/round-45/tmp/ExecCollisionGuard/` (created, retained as evidence).
Nothing outside the round-45 wave directory was written; shokuknow and the fleet repo were
read-only.

Files written (all absolute):

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/assimilation/reg-ids`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/assimilation/staged-ids`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/assimilation/collisions`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/assimilation/renumber-map.tsv`
  (written here at 07:41, then rewritten by the census seat at 07:44; the live 5-column version is
  validated in §3 and kept)
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/assimilation/quarantine-slice`
- this report

## 1. The guard, run on this round's bytes

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ A=.ufo/waves/round-45/assimilation
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md \
    | grep -oE 'S[0-9]+' | sort > $A/reg-ids
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' \
    /home/vgpnk/Projects/shokuknow/merge/mori/SOURCES.append.md \
    | grep -oE 'S[0-9]+' | sort > $A/staged-ids
$ comm -12 $A/reg-ids $A/staged-ids > $A/collisions
$ echo $?          # 0
```

Heads and tails (the lists are `sort`-ed, one id per line):

```
$ head -10 $A/reg-ids                $ head -10 $A/staged-ids
S001                                 S471
S002                                 S472
S003                                 S473
S004                                 S474
S005                                 S475
S006                                 S476
S007                                 S477
S008                                 S478
S009                                 S479
S010                                 S480
```

```
$ tail -3 $A/reg-ids                 $ tail -3 $A/staged-ids
S470                                 S604
S471                                 S605
S472                                 S606
```

Counts and ids:

| quantity | value |
|---|---|
| registry row count (`reg-ids` lines, all distinct) | **245** |
| staged row count (`staged-ids` lines, all distinct) | **136** |
| registry numeric maximum | **S472** |
| staged numeric range | S471…S606, contiguous (136 ids) |
| next free id above the registry maximum | **S473** |

Collisions (`comm -12`, 2 lines):

```
S471
S472
```

Each list is duplicate-free internally (`sort | uniq -d` empty in both), so these two
lines are cross-file id collisions, not within-file repeats. The registry is
contiguous `S001…S235`, then only `S241`, `S262`, `S347…S351` and `S470…S472`: the other 227 ids
in that span carry no row. The numeric maximum `S472` is therefore the lane's high-water mark,
and the next free id is `S473` regardless of the gaps below it.

### What the two collisions actually are

The collision is not a numbering accident between unrelated rows; the staged rows re-stage two
documents the lane already adopted:

```
staged S471 -> https://gihyo.jp/article/2026/03/linux_containers-0061  == registry S232
staged S472 -> https://gihyo.jp/article/2024/08/linux_containers-0056  == registry S233
```

`corpus/SOURCES.md` has `S232`/`S233` `mined`, `used-by corpus/knowledge/oom-evidence-loss-r38.md`;
the staged rows carry a longer `used-by` (both add `kernel-oom-line-attribution-r12.md`) and a
different `scope` wording. The registry's own `S471`/`S472` are different documents (proc(5) ja and
zh_TW) whose `used-by` is `corpus/knowledge/pid-probe-conclusion-r44.md` — so an append under the
old ids would silently attach that unrelated entry's citation to the two cgroup articles. So the
campaign allocated `S471`/`S472` to documents whose lane rows are `S232`/`S233`: an id collision
**and** a within-scope URL duplicate.

## 2. Falsification: the guard itself can fail (and does, on an indented row)

Scratch built under `.ufo/waves/round-45/tmp/ExecCollisionGuard/`:

```
$ cat -A scratch-registry.md
| id | source |$
|---|---|$
  | S002 | indented row (two leading spaces) |$
| S001 | column-zero row |$
$ cat -A scratch-staged
S002$
```

The round's pattern (`^ {0,3}\|…`) must catch the two-space row; a column-zero-only pattern
(`^\|…`) must not:

```
=== guard A: '^ {0,3}\|[[:space:]]*S[0-9]{3,}' (the round's pattern) ===
  | S002
| S001
A-ids: S001 S002
A-collisions:
S002
A-size=1
=== guard B: '^\|[[:space:]]*S[0-9]{3,}' (column zero only) ===
| S001
B-ids: S001
B-collisions:
B-size=0
```

Both compiled with `grep -oE 'S[0-9]+' | sort -u` then `comm -12 … scratch-staged`; exit 0 in
every stage. Guard A returns the nonempty set `{S002}`; guard B returns the empty set.
Guard B is not a dead regex: it still matches the column-zero control row `S001`, so its empty
collision set is a real **miss of the indented row**, not a broken pattern. That is the failure
mode the 0-3-space prefix exists to prevent.

Current-file check of the same width, so the proof is anchored to real bytes:

```
$ grep -cE '^ {1,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md                                # 0
$ grep -cE '^ {1,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/mori/SOURCES.append.md  # 0
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md                                      # 245
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/mori/SOURCES.append.md        # 136
```

Both live files are column-zero today, so the two pattern widths agree on them (245/245 and
136/136). The 0-3-space width buys nothing on today's bytes — it buys the *next* append not
vanishing when a row inherits list indentation.

Guard limits, stated so a reader does not overread the empty/nonempty result: it matches only a
first-column id cell, only 0-3 leading spaces, and only ids starting `S` followed by ≥3 digits. A
four-space indent (a Markdown code block, correctly excluded), a blockquote-prefixed row, or a
row whose id cell is not the first cell are invisible to it.

## 3. Renumber map

Rule: one lane id per staged row, staged order (ascending), continuing above the lane maximum
`S472`; an id is assigned by position in the staged file, never computed by adding a constant to
a staged id.

**The deliverable file was rewritten by a concurrent seat and I kept its version.** I wrote a
2-column map (`S471→S473 … S606→S608`) at 07:41; the census seat (`ExecAssimCensus`) wrote a
5-column map at 07:44, and its item's step 1 reads this path, so I validated the live file
instead of clobbering it:

```
$ grep -vc '^#' $A/renumber-map.tsv                    # 136 map rows (162 lines incl. 26 '# ' comments)
$ grep -v '^#' $A/renumber-map.tsv | cut -f1 | diff -q - $A/staged-ids && echo OK-identical-order
OK-identical-order
$ grep -v '^#' $A/renumber-map.tsv | cut -f2 | sort | uniq -d | wc -l                 # 0
$ grep -v '^#' $A/renumber-map.tsv | cut -f2 | sort -t S -k2 -n | sed -n '1p;$p'      # S474 / S609
$ LC_ALL=C comm -12 <(grep -v '^#' $A/renumber-map.tsv | cut -f2 | LC_ALL=C sort) \
      <(LC_ALL=C sort $A/reg-ids) | wc -l                                            # 0
$ grep -v '^#' $A/renumber-map.tsv | cut -f2 | grep -c S473                          # 0 (exit 1: no match)
```

```
$ grep -v '^#' $A/renumber-map.tsv | sed -n '1p;2p;136p'
S471	S474	7	S232	shifted +3 (S473 reserved)
S472	S475	8	S233	shifted +3 (S473 reserved)
S606	S609	142	—	shifted +3 (S473 reserved)
```

Live mapping: staged `S471…S606` → lane `S474…S609` (offset +3), because **`S473` is reserved**
for the round's own admitted kernel cgroup-v2 row (the ScribeRows item and the census reviewer
name `S473`). The map's header (regenerated 07:47) also carries a census pre-flight over the
staged block: 131 of 136 rows are `NF=13` and pipe-free as written, the five rows `S471`,
`S502`–`S505` would be refused `E01 fields=14`, and six rows `S501`–`S506` carry prose rechecks
`E09` refuses — independently consistent with §5.2.

The live map's column 4 records registry rows whose pages a staged row's URL
already appears on: `S471`→`S232`, `S472`→`S233`, `S473`→`S234`, `S474`→`S235,S349`, and — added
after this seat reported the URL overlap — `S490`→`S471`, `S491`→`S472` (§5.1). All 136
staged ids appear once, in staged order; the 136 target ids are unique, lie in `S474…S609`, and
intersect the live registry in zero ids. My own reading of the item's rule (start at `S473`, no
reservation) is the same construction minus the reserved slot; it is not the live map because the
round claims `S473` for its admitted row. If that row does not land, shift the map back by one.

Citation re-pointing rule (not negotiable in the append): **citations are re-pointed by document
— URL plus anchor — never by arithmetic.** A renumbered row is located by the source it cites
(URL and the section/anchor the row names), and every other row that refers to the old id is
rewritten from that same document identity. No tool may compute a new id by adding a constant to
the old one: a shifted id is only valid because the map says so for that row, and a row whose
document is already in the registry is superseded, not shifted.

Two consequences the adopting seat must not skip:

1. `S471→S474` and `S472→S475` are the two rows whose **document** the registry already holds
   (`S232`/`S233`, identical URLs — the live map's column 4 says so and adopts them as new rows,
   "a page can support more than one claim"). That is a decision, not an accident: the adopting
   seat must either supersede (`S471`→`S232`, `S472`→`S233`) or accept the two extra rows
   consciously. The id guard alone cannot tell these apart — which is why the URL check in §5.1
   belongs beside it, and why the decision is logged here rather than silently absorbed.
2. With `S473` reserved, no staged row lands on a lane id already in the registry; the +3 offset
   is the whole of the safety margin. A map started at `S473` without the reservation would
   collide with the round's own admitted row the moment it lands, and the id guard would only
   find out after the append.

## 4. Quarantine slice (the prompt's awk)

```
$ A=.ufo/waves/round-45/assimilation
$ R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
$ awk -F'|' -v l='mori' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ \
    {print $4, $5}' "$R" > "$A/quarantine-slice"
```

Saved slice (3 lines, every line carries an S-id):

```
 S244`   the cited source could not be fetched, so no quote was checked 
 S262`   the cited source could not be fetched, so no quote was checked 
 S268`   the cited source could not be fetched, so no quote was checked 
```

| line | id as printed | id (trailing backtick is the register's malformed cell) | class cell | register class |
|---|---|---|---|---|
| 1 | `S244\`` | S244 | `the cited source could not be fetched, so no quote was checked` | `unreachable` (unverifiable, **not** fabrication) |
| 2 | `S262\`` | S262 | same | `unreachable` |
| 3 | `S268\`` | S268 | same | `unreachable` |

All three are prose-class ("could not be fetched"), i.e. the register's unchecked family: they
are quarantined and unverifiable until fetched and located, never payload-absent. The slice
already existed at that path before this seat started (mtime 07:33); my derivation is
byte-identical to it, so the write at 07:42 changed no content:

```
$ sha256sum tmp/ExecCollisionGuard/quarantine-slice.derived $A/quarantine-slice
8494dc0b4942527cdcc724cf1550653b98be679bd811b74d20e43ce5a6207349  …/quarantine-slice.derived
8494dc0b4942527cdcc724cf1550653b98be679bd811b74d20e43ce5a6207349  …/quarantine-slice
```

## 5. Findings beyond the two id lines (all measured, none acted on)

1. **The id guard is necessary but not sufficient.** URL-level comparison of the same two files
   finds **11 shared URLs covering 17 staged rows** (and 14 registry rows), while the id guard
   flags 2 rows. Examples:
   `gihyo …/linux_containers-0061` reg S232 / staged S471; `man.archlinux.org/man/proc.5.zh_TW`
   reg S472 / staged S491; `manpages.ubuntu.com/…/proc.5.html` reg S471 / staged S490;
   `journalctl.html` reg {S014,S351,S470} / staged {S532,S593,S601}. Census `E04`
   ("duplicate URL+scope, no supersedes", `scripts/sources-census.sh:648-650`) is the complement,
   and the census separates the two cases in code: the same URL with a *different* scope string is
   `W04 … duplicate url … across scopes`, a warning that "does not affect clean lanes"
   (`:26-27,645`), while only an identical `(url, scope)` pair is `E04`. A reworded second row
   about one document therefore passes the gate as a warning and passes the id guard silently.
   Measured live: the census seat's primary run over the mirror is `rc=0` with 19 `W04` lines,
   0 error lines and 0 stderr bytes (`assimilation/validate-receipt.txt`), and the live renumber
   map annotates staged `S490`/`S491` as one-document second rows against lane `S471`/`S472`. The
   collision guard must therefore be paired with a document-identity (URL) check at adoption
   time.
2. **One of the five malformed staged rows is one of the two colliding ones.** `awk -F'|'` field
   counts on `/home/vgpnk/Projects/shokuknow/merge/mori/SOURCES.append.md`: rows 7, 38, 39, 40,
   41 (`S471`, `S502`, `S503`, `S504`, `S505`) have `NF=14` where a valid 11-cell row has `NF=13`.
   `S471` is one of them: its teaches cell contains `\|` inside a code span
   (`grep -ciE 'inotify\|POLLPRI' corpus/SOURCES.md -> 0`), which a pipe split reads as an extra
   column. This is the addendum's known campaign-schema hazard: such a row cannot be appended
   byte-exact through the census gate, so renumbering alone would not make it adoptable.
3. **Map reservation vs. my literal rule.** The live map shifts every row by +3 to keep `S473`
   free for the round's admitted row; my earlier, strictly literal map (start at `S473`) differs
   by exactly that one slot and was superseded by the live file (§3). Neither map places a staged
   row on an id the registry already holds.

## 6. Verification actually run

Only the commands pasted above were run (grep/comm/awk/sha256sum/python3 parse, all read-only on
shokuknow and the fleet repo); every pasted block is real output with exit code 0 unless shown
otherwise. No build, lint, test or formatter was run (editing wave; the L1 owns the gate). No
tool was installed or upgraded in this seat. `git` was used read-only (`status --porcelain`): the
four files this seat wrote (`reg-ids`, `staged-ids`, `collisions`, `quarantine-slice`), the live
`renumber-map.tsv` written by the census seat (§3) and this report are untracked additions under
`.ufo/waves/round-45/`; nothing was staged, committed or mutated.

Risks: `S473` is unclaimed in the registry at this snapshot — if the round's admitted row does not
land, the live map's reservation note becomes false (the +3 offset itself merely leaves a gap).
If the registry gains ids from a sibling append, re-run the guard (`grep … | sort > reg-ids`) at
append time rather than trusting these files. The five `NF=14` rows must be normalized before any
append, and the id guard alone does not catch same-document/different-id duplicates (§5.1).

The live map's header now names the entering tip `554ff416` and the measured bytes at the freeze
commit `3ad8faaa`, stating the registry reading is identical at both; that matches this seat's
`git log` (`3ad8faaa` = "round-45: frozen contract, wave-1 spec and dispatch and opened sources",
`554ff416` = "round-44: ExecOffHostReplay final bytes").
