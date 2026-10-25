# ExecAssimCensus — scratch append validation for the r45 assimilation rows

Seat: executor (leaf; no spawns). Lane `/home/vgpnk/Projects/shokunin/mori-shokunin`;
contract read first. **Nothing under `corpus/` was written by this seat** — the registry under
test is the mirror. Readings from shokuknow and the fleet repo were read-only; the four
`renumber-staged.py` / `merge-plan.py` / `quote-lint.py` / `absent-defect-register.py` writers
were not run. Scratch: `.ufo/waves/round-45/tmp/ExecAssimCensus/`. No tool was installed.

Files written (all absolute):

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/assimilation/renumber-map.tsv`
  (absent when this seat started; built here — 136 mapping rows + reserved id)
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/assimilation/append-block.md`
  (the S473 row + a provenance/normalization comment block)
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/assimilation/validate/`
  (mirror: whole lane tree, `SOURCES.md` +1 row, entry copied)
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/assimilation/validate-receipt.txt`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/assimilation/validate-neg-*/`
  (five control mirrors, hardlinked from `validate/`; each is mine and deletable)
- this report

## 1. Renumber map — built, because it was absent

Rule applied: the lane's current highest id is its registry maximum, staged rows continue above
it. Measured with `git show` at both revisions the contract names — entering tip `554ff416` and
the freeze commit `3ad8faaa` (HEAD):

```
$ git show 554ff416:corpus/SOURCES.md | grep -oE '^\| S[0-9]+ \|' | ... | tail -1   -> S472
$ git show 3ad8faaa:corpus/SOURCES.md | grep -oE '^\| S[0-9]+ \|' | ... | tail -1   -> S472
$ grep -cE '^\| S[0-9]+ \|' corpus/SOURCES.md                                      -> 245
$ awk ... | sort | uniq -d                                                          -> (none)
```

Maximum **S472** at both revisions, 245 rows, zero duplicate ids (the L1's
`evidence/s472-reopen-l1.txt` is the S472 re-open receipt). The staged file
`/home/vgpnk/Projects/shokuknow/merge/mori/SOURCES.append.md` holds **136 rows, S471..S606**, so
every staged id collides with nothing only after a shift.

**S473 is reserved**, not allocated by the shift: it is the lane id of this round's own row for
the kernel cgroup-v2 rst, the id both the `ScribeRows` item and the census reviewer name. Hence
staged S471 opens at **S474** and the block shifts **+3** (staged S606 -> S609). The map is
`staged_id <TAB> lane_id <TAB> staged_line <TAB> related_lane_rows <TAB> note`, 136 rows, target
ids S474..S609, all unique, none in 471..472, S473 absent (verified by grep; ExecCollisionGuard
re-verified the same invariants — 162 lines, 26 comment lines, 136 rows, zero intersection with
`reg-ids` — and kept this version). Pinned digest:
`f4724c8704ff4f23dfd314b0dda7a4617902cb3f0d297eab0285bc5a8507b513` (162 lines).

Two annotations the MERGE-REPORT's own cross-reference table does not carry, added because the
byte comparison shows them:

- staged **S490 -> S493** and **S491 -> S494** are the *same URLs and the same claims* the lane
  landed in round 44 as **S471** and **S472** (identical source cell, same Z/X and swap-out
  teaching, lane copy fetched 2026-10-25). Appending them adds a second row about one document
  (W04 only; the scope cells differ so E04 does not fire). Evidence: the merge package was
  generated 2026-10-24 23:33, before those two rows landed.

Pre-flight of the staged block against the census grammar (measured here, not asserted):

```
136 staged rows | NF==13 and no escaped pipe: 131
NF!=13 (escaped '|' inside a cell) -> E01 fields=14: S471, S502, S503, S504, S505
recheck not an ISO date / NNd / symbolic cadence   -> E09: S501, S502, S503, S504, S505, S506
```

Every such row needs the normalization this round's S473 row received before it can be appended.
The map records both counts in its header.

## 2. The append block — one row, and why exactly one

The admitted entry (`corpus/knowledge/census-cgroup-levels-r45.md`, sha256
`1f28dd38…ef1b46`, 47 lines) contains exactly two registry tokens:

```
$ grep -oE '\bS[0-9]{3,}\b' corpus/knowledge/census-cgroup-levels-r45.md | sort -u
S002
S473
```

`S002` is already in the lane registry (it is where the entry says the events-vs-`local`
distinction is first held), so it is not appended. `S473` is absent — it is the row this block
drafts. No other row is cited, so the block is one row, not a rubber-stamped 136.

### S473 — cell-by-cell normalization (`| S473 | … |`, awk NF=13, 11 cells)

| cell | value written | why it changed from the raw item text |
|---|---|---|
| id | `S473` | lane max S472 -> next free id; reservation documented in the map |
| source | `Control Group v2 — the aggregation scope of the memory interface, kernel v7.2 (rst) — https://cdn.jsdelivr.net/gh/torvalds/linux@v7.2/…/cgroup-v2.rst` | the URL of the copy this round actually opened (sha256 `a9433bb0…b7ad`, 3524 lines), not the item's shorthand; title names the aspect so the row is not a second "Control Group v2" |
| kind | `docs` | `.rst` kernel documentation; `docs` is the enum value the census accepts (E05 would reject a free-text kind) |
| tier | `A` | upstream kernel documentation, primary; kind is not `community`, so E10 cannot fire |
| scope | aggregation scope of three memory files only + four explicit negatives (`not this host's readings`, `not cgroup v1`, `not systemd resource-control man pages`, `not the docs.kernel.org HTML rendering`); states the events/local split stays S002's | the item's raw teaching overlapped S002 almost exactly. S002 (same document, docs.kernel.org rendering) already holds "distinguish hierarchical memory.events from memory.events.local". Keeping that as this row's claim would be a duplicate teaching the census cannot see (different URL, so no E04/W04). The row therefore claims the **increment**: that aggregation scope is a property of the *file*, and that `memory.peak` is subtree-inclusive — and it says S002 holds the split |
| anchor | `cgroup-v2.rst:1468` + `:1474-1477` quote (15 words); `:1517-1520` + `:1518-1519` quote (7 words); `:1440-1444` (5 words) + tag, fetch date, sha256 | located quotes, each <= 25 words, on the opened copy's own line numbers (verified by `awk NR` against the opened `cgroup-v2.rst.src`). The digest is in-cell so a line number cannot travel without its copy — the entry makes the same point about the docs.kernel.org rendering numbering the same sentences 1505–1509 |
| teaches | the file-property framing + the peak-subtree asymmetry + the consequence for a two-level row | the increment over S002, stated as a consequence a census row can act on |
| status | `mined` | required by P-C3.2; also W03 avoided because used-by is not `—` |
| opened | `2026-10-25` | today; E08 rejects a future date |
| recheck | `180d` | **normalized**: the item asked for "`180d` plus the command". E09 accepts only an ISO date, `NNd` or a symbolic cadence, so prose in this cell refuses the row (proved by control E09 below). The command moved to the append block's comment header and to the entry's own `recheck:` line, which no E09 rule governs |
| used-by | `corpus/knowledge/census-cgroup-levels-r45.md` | exactly the admitted entry, one path, no comma (E11 splits on commas and resolves each against the registry's parent) |

Pipes: no literal `|` and no escaped `\|` in any cell (`grep -c '\\|'` -> 0). The staged rows
that do carry one are listed in §1. Row digest, identical in the block and in the mirror:
`d7ac69926608e76074183c44febe212cc38309557ac86231a3b7988eba0285b6`.

## 3. The mirror

`assimilation/validate/` is a copy of the whole lane tree — `corpus/` plus the top-level files
and `tools/` — because `usedby_findings` resolves each `used-by` against
`dirname(SOURCES.md)/..`, i.e. the mirror root. The corpus-only construction the item's step 3
describes **cannot pass**: it produces 26 E11s over 5 targets outside `corpus/`
(`SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, `tools/mori-disk-rate.py`,
`tools/fixtures/mori-oom-killers/cases-a2-r29.json`); RevCensusAppend rebuilt that variant
independently and got the same 26/5. The item text should say "a copy of the lane tree" for
future rounds; that is a wording lesson, not a defect in this run.

Fidelity:

```
$ diff /…mori-shokunin/corpus/SOURCES.md validate/corpus/SOURCES.md
251a252
> | S473 | Control Group v2 — … | mined | 2026-10-25 | 180d | corpus/knowledge/census-cgroup-levels-r45.md |
$ diff -rq /…mori-shokunin/corpus validate/corpus ; echo rc=$?
Files …/corpus/SOURCES.md and …/validate/corpus/SOURCES.md differ
rc=1                                            (one file, and it is the intended one)
$ sha256sum validate/corpus/knowledge/census-cgroup-levels-r45.md
b066d2dd1361c6cdd953186d58ac364366751ae9d0b89cbb8911e5d14c9e8483   8357 B / 66 lines  (== lane copy)
```

**The entry is a live file, and the mirror had to chase it.** ScribeEntry wrote
`census-cgroup-levels-r45.md` at 07:44:28 and kept editing it; this seat observed it at
`1f28dd38…ef1b46` (7197 B / 47 lines, 07:44), `bf45e4b1…52ee2` (8337 B / 66 lines, 07:50),
`c06245fc…87ddfe` (8315 B / 66 lines) and `b066d2dd…e8483` (8357 B / 66 lines, the snapshot
pinned above); RevCensusAppend measured further digests of its own. Each time the mirror was
re-copied and the primary re-run, and `corpus/lessons/round-45.md` was re-copied when it changed
too. The result of the final refresh is the `diff -rq` above: exactly one differing file,
`corpus/SOURCES.md`, which is the row under test. The census cannot see the entry's bytes at all
(E11 is existence-only), so **the pinned digest is the only record of which copy ran** — re-copy
and re-pin if ScribeEntry writes again.

## 4. Census receipt — run, stdout, warnings, rc

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --file /…/assimilation/validate/corpus/SOURCES.md
file	W04	S035 duplicate url raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in across scopes
file	W04	S037 duplicate url www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html across scopes
file	W04	S073 duplicate url docs.python.org/3/library/pathlib.html across scopes
file	W04	S074 duplicate url kubernetes.io/docs/concepts/architecture/controller across scopes
file	W04	S075 duplicate url ftp.gnu.org/gnu/bash/bash-5.3.tar.gz across scopes
file	W04	S076 duplicate url michaelfeathers.silvrback.com/characterization-testing across scopes
file	W04	S147 duplicate url raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/docs/settings.md across scopes
file	W04	S148 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c across scopes
file	W04	S149 duplicate url man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html across scopes
file	W04	S150 duplicate url raw.githubusercontent.com/systemd/systemd/v262/man/systemd.exec.xml across scopes
file	W04	S166 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c across scopes
file	W04	S168 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst across scopes
file	W04	S201 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c across scopes
file	W04	S218 duplicate url github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch across scopes
file	W04	S220 duplicate url raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c across scopes
file	W04	S228 duplicate url docs.python.org/3/library/os.path.html across scopes
file	W04	S349 duplicate url www.openeuler.org/whitepaper/openEuler%2024.03%20LTS%20%E6%8A%80%E6%9C%AF%E7%99%BD%E7%9A%AE%E4%B9%A6.pdf across scopes
file	W04	S351 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
file	W04	S470 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
file	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/assimilation/validate/corpus/SOURCES.md
rc=0        stderr: 0 bytes
```

**E = 0.** The 19 W04 lines are the lane baseline, not something this row introduced: they are
identical in id and order (verified by `diff` of the id column) to the round-43 receipt's 19, which
covers the same registry content through S470; round-42 carried 16 because its registry stopped
earlier. S473 adds no warning because its URL is new to the registry
(`grep -c cdn.jsdelivr.net corpus/SOURCES.md` -> 0). No E03, no E04, so **no row is refused**.

### Negative controls — the arm is not vacuous

Each control is a hardlinked copy of the delivered mirror with exactly one mutation; each must be
refused.

| control | mutation | rc | finding |
|---|---|---|---|
| E11 | entry file removed | 1 | `E11 S473 missing used-by corpus/knowledge/census-cgroup-levels-r45.md` |
| E09 | recheck -> `180d — curl -fsSL the pinned URL and sha256sum` | 1 | `E09 S473 recheck=180d — curl …` |
| E01 | one literal `|` inside the teaches cell | 1 | `E01 S473 fields=12` |
| E03/E04 | the S473 row appended twice | 1 | `E03 S473 duplicate id` + `E04 S473 duplicate url cdn.jsdelivr.net/… within scope …` |
| staged-verbatim | staged `S503` appended as written | 1 | `E01 S503 fields=12` + `E11 S503 missing used-by grep -c '受管树'` -> 1 (ran 2026-10-23)` |

The last control is the point of §2: a staged row copied verbatim breaks the registry twice over.

## 5. Risks and what the L1 must do

- **The row is not in the lane registry.** `S473` absent from `corpus/SOURCES.md` (verified). P-C3
  at `--root` needs it appended; this seat's mandate stopped at the mirror. Append the single row
  from `append-block.md` (its comment block is not content), then the `--root` census arm is
  already green by construction — the mirror is the same bytes plus that row.
- **`corpus/README.md` has no map row naming the entry yet** (`grep -c census-cgroup-levels-r45`
  -> 0). P-C3.4 fails until ScribeRows' README row is appended; that is outside this item's file
  scope and is flagged, not done.
- **Entry digest.** The entry is a live file. The receipt pins the snapshot digest
  `b066d2dd…e8483` (8357 B / 66 lines) and the mirror matches it byte-for-byte; four of this
  seat's own snapshots differed (`1f28dd38`, `bf45e4b1`, `c06245fc`, `b066d2dd`), and
  RevCensusAppend measured further ones. The census verdict does not move with those bytes (E11 is
  existence-only), but any later edit needs a re-copy and a re-pin.
- **The staged 136 rows are not census-clean as written** (5 escaped pipes, 6 prose rechecks, and
  S490/S491 duplicating landed S471/S472). They are the L1's integration, not this round's
  assimilation payload; the map and its header carry the counts so none of them is appended blind.
- The five `validate-neg-*` mirrors are mine and deletable; `validate/` and
  `validate-receipt.txt` are the deliverables and should be kept with the round.

### F3 — `corpus/lessons/round-45.md` describes a map that is not on disk (reported, not edited)

Found by RevCensusAppend while re-running against this seat's bytes, and verified here. The lesson
is itself a live file (ScribeLesson kept editing it during the review), so its line numbers moved
between the reviewer's read and mine; the claims did not. Anchored on the digest
`477704ab6811fa5a9e993786fb615b3d322b4051465fd6b5d06f483a17e96715` (193 lines):

```
$ grep -n 'is 136 lines\|S471→S473\|S606→S608\|renumber-map.tsv:1' corpus/lessons/round-45.md
142:`assimilation/renumber-map.tsv` is 136 lines, ascending in staged order, one
143:target above the registry maximum: `S471→S473` … `S606→S608`. It is a routing
171:| M8 | … | `assimilation/renumber-map.tsv:1` (`S471\tS473`) …            # the M8 row
$ grep -cP '^S471\tS473\t' .ufo/waves/round-45/assimilation/renumber-map.tsv   -> 0
$ sed -n '1p'  …/renumber-map.tsv   -> # renumber-map.tsv — mori lane, round 45 …   (a comment)
$ grep -nP '^S471\t' …/renumber-map.tsv  -> 27:  S471  S474  7  S232  …
$ grep -nP '^S606\t' …/renumber-map.tsv  -> 162: S606  S609  142  —     …
$ wc -l …/renumber-map.tsv               -> 162      (136 rows + 26 comment lines)
```

Consequence: a next-round append that follows the lesson targets **S473 — this round's own row**
and is refused by E03 (`duplicate id`), and it reads line 1 (a comment) as a mapping row. The map
is the correct artifact — S473 reserved, +3 shift, S606→S609 — and the lesson's own M8 *rule*
("reserve every id named by the round's own admitted rows before computing the map") is exactly
what produced it, so the lesson's rule and the lesson's description contradict each other. The
file is ScribeLesson's, so this is reported to the L1 and left unedited here; the fix is the two
phrases, not the map.

## 6. Evidence index

```
.ufo/waves/round-45/assimilation/renumber-map.tsv        136 mappings, S473 reserved, pre-flight counts
.ufo/waves/round-45/assimilation/append-block.md         the S473 row + normalization header
.ufo/waves/round-45/assimilation/validate/               mirror (whole lane tree, +1 registry row)
.ufo/waves/round-45/assimilation/validate-receipt.txt    command, full stdout, rc, controls, fidelity
.ufo/waves/round-45/assimilation/validate-neg-*/         five control mirrors
.ufo/waves/round-45/tmp/ExecAssimCensus/primary.json     captured rc/stdout/stderr for every run
```
