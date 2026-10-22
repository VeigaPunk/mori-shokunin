# CriticC1Counter — round 27, wave 1: falsifiers for the frozen C1 counter

Seat: MoriR27.CriticC1Counter (critic, leaf). Subject: `.ufo/waves/round-27/count-c1.sh` as landed at
761b4cdb (sha256 `697fb7d7bcca6c83b2a8fea701a68edcb6c34832558890234e1b58047db4c01c`, same bytes at 761b4cdb,
5fa0a00 and in the working tree: `sha256sum` and `git show <rev>:.ufo/waves/round-27/count-c1.sh | sha256sum`).
The counter was not changed. Nothing was written in the lane except this report.

## Verdict

The counter is a fair floor for honest landings that use the lane's current conventions, but it is not a
proof of C1. Ten synthetic commits that hold none of the knowledge the contract describes all print
`C1=met` (exit 0). Twelve commits that carry a correct landing in a slightly different, lane-precedented
shape all print `C1=unmet` (exit 1). The closure must check by hand that the counted rows were opened,
that each one is new, that the entry is used and on topic, and that the SKILL rows are decisions. Two
cheap counter fixes would remove most of the false `met` cases. Those fixes are for a later round, since
this counter is frozen.

## 1. Runs at real revisions (the lane's own git objects)

Command: `bash .ufo/waves/round-27/count-c1.sh <rev>` from the lane root.

| rev | output | exit |
|---|---|---|
| fc09f96c (entering tip) | `entry=absent new_rows_cited=0 skill_rows=0` / `C1=unmet` | 1 |
| 761b4cdb (contract) | same | 1 |
| 5fa0a00 (current HEAD) | same | 1 |
| root commit ec0664e1 | same (the entry is checked before SOURCES.md, so this is not `bad_rev`) | 1 |
| `nosuchrev` | `bad_rev` | 2 |
| 40 zeros | `bad_rev` | 2 |
| tree id of fc09f96c | git prints `error: … dereferences to tree type` to stderr despite `-q`, then `bad_rev` | 2 |
| blob id of fc09f96c:SKILL.md | same, with `blob type` | 2 |
| no argument, or two arguments | `usage: count-c1.sh <rev>` | 2 |

The fc09f96c result matches `evidence/c1-before.txt` exactly. Premise check: the highest registry id is
S126 at both fc09f96c and HEAD (`git show <rev>:corpus/SOURCES.md | grep -oE '^\| S[0-9]+ ' | sort -V | tail -1`),
and no id is duplicated at fc09f96c (`uniq -d` prints nothing). So `MIN_ROW=127` (`count-c1.sh:9`) is right
about numbering. It is not a test of newness (see G5).

## 2. Falsifier method ("bad revisions")

I made a scratch clone with `git clone --shared` at `/fast/scratch/hyaku/mori-r27/CriticC1Counter/clone`,
which only reads the lane's objects. Each scenario is one commit on fc09f96c, tagged in the clone. The script
that builds them is `/fast/scratch/hyaku/mori-r27/CriticC1Counter/build.sh`, and its output is `run.txt`
next to it. I ran the **frozen script unmodified** with `GIT_DIR=<clone>/.git`. That works because its
`git -C $LANE` calls only use rev-parse, cat-file and show, which do not touch the lane's index or working
tree. `GIT_DIR=<clone>/.git git -C <lane> rev-parse --git-dir` printed the clone's git directory, and the
clone at fc09f96c gave the same output as the lane. All process names, URLs and text in the fixtures are invented
or are public upstream URLs. No host data is used.

### 2a. False `met`: knowledge absent, counter satisfied (all exit 0, `new_rows_cited=3 skill_rows=3`)

| id | what the commit holds | counter line that lets it through |
|---|---|---|
| OK0 | control: honest-shaped landing (three full 11-cell rows, entry, a three-row decision table) | — |
| G1 | entry is the single line `source: S127 S128 S129`; the three rows have 4 cells (`\| S127 \| x \| mined \| <entry> \|`); the SKILL rows are three lines that hold only the entry path | 25-27 test substrings, not columns; 31 counts any `\|` line holding the path |
| G2 | rows appended under `## Leads (unopened)` with `opened`, `anchor`, `scope` and `teaches` all `—`, status `mined` | 25 greps the whole file, not the `## Registry` table (`SOURCES.md:3,179` at fc09f96c) |
| G3 | each id appears twice: one row is `queued` and names the entry; the other is `mined` with used-by `—`. No single row qualifies | 25 keeps every matching line; 26 and 27 can each be satisfied by a different line |
| G4 | status `rejected`; the word `mined` sits in the `teaches` cell; the entry path sits in the `anchor` cell; used-by is `—` | 26 and 27 do not check which column |
| G5 | **identity change**: existing rows S114, S115 and S118 are renumbered to S127, S128 and S129, with the entry appended to used-by. No source was opened. This also breaks the round-26 entry, which cites S114 to S126 | 23 tests the number, not that the row is absent at fc09f96c |
| G5b | three new ids that all re-open the earlyoom README already registered as S114. The contract's bound says that should add an anchor to S114, not a new row | no URL or novelty check |
| G7a | SKILL table header cell names the entry, then a separator and **two** decision rows | 31 counts the header row (and would count any `\|` line) |
| G7b | no Round27 section at all: a fenced ```` ```md ```` example inside the trailing Round26 section holds a `## Round27 example` line and three rows | 31: awk has no idea of code fences, so the `## ` line inside the fence switches `inside` on |
| G8 | three good rows and a good table, but the entry body is `# Empty`. None of `oom_score`, `oom_score_adj`, `--prefer`/`--avoid`/`--ignore`, `--sort-by-rss`, `memory.oom.group`, the fleet's adj values or the share of sends appears | the entry body is never read beyond the first `^source:` line (17) |

Gaps found by reading the code but not given a separate fixture:
- The `grep -qF "$ENTRY"` test on line 27 is a substring match, so a used-by naming `…/oom-victim-selection-r27.md.draft` or a scratch copy path also passes.
- Line 17 takes the first `^source:` line anywhere in the file, including one inside a fenced block.
- The same `source:` line may list rejected-candidate ids (lane precedent `system-pressure-r24.md:1`, "Rejected candidate: S097"). Only the row's status keeps those out.

### 2b. False `unmet`: correct content, shape the counter misses (all exit 1)

| id | change from OK0 | output | lane precedent that makes it likely |
|---|---|---|---|
| U1 | heading `## Round 27 — …` | `skill_rows=0` | none; every heading uses `RoundNN` (`SKILL.md:518,535,567,611,644,676`) |
| U2 | heading `### Round27 — …` placed at the end | `skill_rows=0` | the file ends in `## Round26`, which has `### ` subsections (`SKILL.md:676,689,704,712`), so a `###` heading is read as part of Round26 |
| U2b | `## round27` (lowercase) | `skill_rows=0` | none |
| U3 | **Round26 shape**: the entry is cited once in prose ("Grounded in …") and the decision rows cite upstream URLs | `skill_rows=0` | exactly how `SKILL.md:684-702` grounds the r26 table. No row there names the r26 entry (`grep -n userspace-oom-killers-r26 SKILL.md` → only line 684) |
| U4 | rows cite `oom-victim-selection-r27` without `.md` | `skill_rows=0` | none |
| U5 | `source: S127–S129 (…)` | `new_rows_cited=2` (endpoints only) | `SKILL.md:646` "sources S098–S104, S112–S113" |
| U6 | `source:` line wrapped, with the new ids on a continuation line | `new_rows_cited=0` | `observability-surfaces-r2.md:3` and `wave-settlement-r20.md:3` wrap their `source:` line |
| U6b | YAML front matter `source:` followed by `- S127` list items | `new_rows_cited=0` | none (entries use one line) |
| U6c | two `source:` lines, with the new ids on the second | `new_rows_cited=0` | `roster-truth-r12.md:1,42` has two `source:` lines |
| U7 | used-by written `knowledge/oom-victim-selection-r27.md` | `new_rows_cited=0` | `corpus/README.md:35` uses the `knowledge/…` short form, while SOURCES used-by never does (at fc09f96c every used-by token is a `corpus/`, `tools/` or similar path, or `—`) |
| U8 | status cell padded to `mined  ` (two spaces), as a Markdown table formatter does when it pads to the `status` header width | `new_rows_cited=0` | none so far, but one formatter pass would drop **every** row to zero |
| U8b | id cell `\|S127 \|` with no inner space | `new_rows_cited=0` | none |

## 3. Classification

Axes: depth (C1's axis; a false `met` overstates it) and calibration (the counter's met/unmet must be
something the closure can rely on).

### 3a. Must be checked by hand at closure. A counter cannot settle these.

| # | check | falsifiers it catches |
|---|---|---|
| H1 | each counted row was really opened: the URL resolves to the pinned tag, the recorded sha256 matches a re-fetch, the access date is 2026-10-22, and each quote is verbatim, at most 25 words, with a line number | G1, G2, G8 |
| H2 | the entry body uses every counted source, either by id **or** by that row's URL or anchor. The r26 entry cites only S118 by id in its body and the other twelve by URL, so a check on ids alone would misfire | G8, G1 |
| H3 | topic coverage and correctness against the contract's list: kernel `oom_score`/`oom_score_adj` badness, the earlyoom `--prefer`/`--avoid`/`--ignore` and `--sort-by-rss` options, `memory.oom.group`, the fleet's adj values on this host, and the share of earlier-boot sends that hit fleet processes (counts and classes only), each traceable to a command and its output | G8 |
| H4 | the SKILL rows under `## Round27` are at least three distinct decision rows (a condition and an action, grounded in a claim the entry makes), not counting header, separator, fenced or registry lines | G1, G7a, G7b |
| H5 | privacy: no command line, uid, pid list, journal `MESSAGE` text, `/etc/default/earlyoom` value, `--prefer`/`--avoid`/`--ignore` expression value or harness settings value in the entry, rows or SKILL; the lane retention scan stays at 4 or below | (out of counter scope) |
| H6 | no harm to identity: every id at or below S126 still names the same source as at fc09f96c, and every id cited by an fc09f96c entry still resolves | G5 |

### 3b. Worth a counter fix in a later round (cheap and mechanical, and no current-convention landing would fail)

| # | fix | removes |
|---|---|---|
| F1 | parse the `## Registry` table by column: split on `\|`, trim each cell, and require exactly one row per id, 11 cells, status cell `== mined`, the used-by cell split on commas containing the exact entry path, and `opened` equal to `2026-10-22` | G1, G2, G3, G4, U8, U8b |
| F2 | novelty: the row's id **and** its URL are both absent from fc09f96c's SOURCES.md (`git show fc09f96c:corpus/SOURCES.md`) | G5, G5b |
| F3 | SKILL: skip fenced blocks, and do not count a `\|` line that is immediately followed by a `\|---` separator (the header) or is itself a separator | G7a, G7b |
| F4 | ids: expand `Snnn–Snnn` ranges on the `source:` line | U5 |

F1 to F3 fit in about 25 lines of awk and keep the exit-code contract. H2 and H3 could get a mechanical floor
(the body contains the id or the row's URL; the body names each listed term), but only as a supplement.
Matching on keywords is not a test of knowledge.

### 3c. Not a counter defect: tell the integrator to use the exact form (this costs nothing)

U1, U2, U2b, U4, U6, U6b, U6c and U7 match the contract's own words: "a section whose `## ` heading contains
`Round27`", "whose `source:` line cites", "the entry in `used-by`". A landing that strays has missed the
contract's letter. Each one is a cheap trap, though, and U3 is the lane's own most recent template.
Paste-ready guidance for the integrator:

```text
C1 landing form (so the frozen counter can see a correct landing):
- Entry line 1, one physical line: `source: S127 (…), S128 (…), S129 (…)` — every new id written out
  individually, no ranges (S127–S129 counts 2), no wrapping, no YAML list, no second source: line.
- SOURCES.md: rows inside `## Registry`, cells exactly `| S127 |` and `| mined |` (single spaces, never
  run a table formatter over the file), used-by holds the full path
  `corpus/knowledge/oom-victim-selection-r27.md`.
- SKILL.md: a top-level heading `## Round27 — …` (not `###`, not "Round 27"), and EACH decision row
  must name `corpus/knowledge/oom-victim-selection-r27.md` in a cell. The Round26 shape (entry cited
  once in prose above the table) scores skill_rows=0.
- Re-opened files with existing rows (S003, S114, S115, S118, S119) get anchors on those rows and do
  not count; C1 needs at least 3 rows for files no row has yet.
```

## 4. Smallest safe correction

There is no change to the frozen counter this round. The closure runs H1 to H6 by hand on the landed tip
and records each one with its evidence. The integrator lands in the form in §3c. F1 to F4 go to the next
round that writes a counter of this kind.

```text
Closure checklist addendum for C1 (paste into the round-27 closure):
[ ] count-c1.sh <tip> prints C1=met, exit 0 (necessary, not sufficient)
[ ] H1 each counted row: URL at pinned tag, sha256 re-fetched and equal, opened 2026-10-22, quotes verbatim ≤25 words with line numbers
[ ] H2 entry body cites each counted row by id or by its URL/anchor
[ ] H3 entry covers oom_score/oom_score_adj, --prefer/--avoid/--ignore, --sort-by-rss, memory.oom.group, fleet adj values, earlier-boot send share (counts/classes only), each with command+output
[ ] H4 ≥3 distinct decision rows under "## Round27", not counting header, separator, fenced or registry rows
[ ] H5 privacy sweep clean; retention scan metric ≤ 4
[ ] H6 rows S001–S126 unchanged in identity vs fc09f96c (id → source cell); no new row repeats an fc09f96c URL
```

H6's identity part can be run mechanically now. It is a diff of the `id | source` cells against fc09f96c. I did
not run it on a landed tip, because no landing exists yet.

## 5. Notes

- The lane working tree had uncommitted changes by other seats while I worked (`git status --short` showed
  several paths; a moment later `git diff --stat` showed one file, `.ufo/waves/round-26/w2/OperabilityNoHarm.md`).
  The counter reads committed bytes only (`count-c1.sh:2`), so this does not affect any result above.
- Tooling: nothing installed or upgraded. I used the git, bash, awk and sha256sum already on the host.
- I used no subagents or background jobs. Scratch is only at `/fast/scratch/hyaku/mori-r27/CriticC1Counter/`.
