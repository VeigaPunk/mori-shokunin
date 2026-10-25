# ExecFiguresLedger — round-45 figure ledger DRAFT + row catalogue

Seat: executor (leaf). Deliverable:
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/figures.tsv.draft`.
I wrote exactly two files: that draft and this report. No shared file (SKILL.md,
SCORECARD.md, LOG.md, corpus/*, contract.md) was touched, and no tracked file was
modified by me (`git status` shows siblings' in-flight edits to
`tools/mori-gate-registry.py`, `tools/mori-round19-regressions.py`,
`tools/mori-routed-check.py`, none of them mine). No tool was installed or
upgraded. No labrat probe was needed: every figure is one `git` pipeline over
committed bytes.

## 1. Draft shape — matched to the counter that now exists

While I measured, `.ufo/waves/round-45/count-c1.py` (item 7) landed on disk
(33,284 bytes, untracked). I read its `parse_ledger`/`parse_pipeline` and shaped
the draft to the grammar it actually enforces:

* **4 cells** `id<TAB>value<TAB>class<TAB>command` for MOVE rows; **5 cells**,
  the fifth `CONST=<reason>` (`CONST_RE = ^CONST=(\S.*)$`), for
  revision-constant rows.
* The value cell is `?` for all 15 rows: **no value is asserted**, per the
  assignment. `?` is not an integer, so the draft parses with exactly 15
  problems and nothing else (evidence §3) — the L1 only replaces cell 2, then
  commits.
* The counter has no shell: it tokenises the command itself (single quotes
  preserve backslashes; `|` splits stages), allows only `git` read verbs plus
  `FILTERS = {grep, head, tail, wc, sort, uniq, cut, tr, cat, nl}`, rejects
  `; $ \` < > & ( )` outside quotes and any `HEAD`/`@{`/40-hex token, and runs
  with **pipefail semantics** — every stage must exit 0, so a zero-match
  `grep -c` is an unreadable row, never a 0. Every one of my 15 commands
  satisfies that and was executed through the counter's own `run_pipeline`.
* `WORK` is refused by the counter ("C1_SETUP WORK is not a scoring revision"),
  and `read_at` reads the ledger **at the revision**. The L1 therefore cannot
  score this file before committing it as
  `.ufo/waves/round-45/figures.tsv`; a pre-commit run reports
  `ledger_present FAIL`, by design.

## 2. Catalogue — id → command → entering-tip value → expected landed value → class

Entering tip is the contract's `554ff416459c92f0dea9762f834a556df2990187`
(contract.md line 4). "Now" is the current committed tip
`3ad8faaa637ae466c61f9427fea1c208bf49ea82`; the two columns differ only for F02.

| id | class | command (verbatim; `@REV@` is substituted by the counter) | entering (554ff416) | now (3ad8faaa) | expected landed | value |
|---|---|---|---|---|---|---|
| F01 | registry | `git show @REV@:corpus/SOURCES.md \| grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` | 245 | 245 | **246** | MOVE (C3 appends S473) |
| F02 | corpus | `git ls-tree -r --name-only @REV@ corpus/lessons \| grep -c '\.md$'` | 73 | 74 | **75** | MOVE (b1d7269f added `round-44-verifier-spotcheck.md`; r45 adds `round-45.md`) |
| F03 | corpus | `git ls-tree -r --name-only @REV@ corpus/knowledge \| grep -c '\.md$'` | 54 | 54 | **55** | MOVE (C3 admits `census-cgroup-levels-r45.md`) |
| F04 | checks | `git ls-tree -r --name-only @REV@ tools \| grep -cE '\.(py\|sh)$'` | 33 | 33 | **33** | CONST (plan rewrites/edits existing tools, adds no filename) |
| F05 | registry | `git show @REV@:SKILL.md \| grep -cE '^\| [^|]+ \| (gate\|probe)'` | 43 | 43 | **50** | MOVE (item 20: 3 orphan-tool rows + 3 r45-counter rows + 1 superseding row) |
| F06 | registry | `git show @REV@:SKILL.md \| grep -cE '^\| name \| kind \| entry \| verdict map \| self-test \| pinned values \| write scope \| owner \|$'` | 7 | 7 | **7** | CONST (rows go into existing eight-cell tables) |
| F07 | evidence | `git show @REV@:.ufo/waves/round-44/w1/ExecGateInventory.md \| grep -c 'unregistered: no row names'` | 14 | 14 | **14** | CONST (round 44 admitted, inventory closed) |
| F08 | checks | `git grep -n -- '--selftest' @REV@ -- tools \| grep -vE ':[0-9]+:[[:space:]]*#' \| cut -d: -f2 \| sort -u \| grep -cE '\.(py\|sh)$'` | 28 | 28 | **31** | MOVE (item 11 gives three tools a real branch) |
| F09 | checks | `git show @REV@:.ufo/waves/round-44/count-c1.py \| wc -l` | 353 | 353 | **353** | CONST (r44 counter bytes closed) |
| F10 | checks | `git show @REV@:.ufo/waves/round-44/count-c2.py \| wc -l` | 388 | 388 | **388** | CONST (r44 counter bytes closed) |
| F11 | checks | `git show @REV@:.ufo/waves/round-44/count-c3.py \| wc -l` | 321 | 321 | **321** | CONST (r44 counter bytes closed) |
| F12 | wave | `git ls-tree -r --name-only @REV@ .ufo/waves/round-43/w1 \| grep -c '\.md$'` | 10 | 10 | **10** | CONST (round 43 closed) |
| F13 | wave | `git ls-tree -r --name-only @REV@ .ufo/waves/round-44/w1 \| grep -c '\.md$'` | 32 | 32 | **32** | CONST (round 44 closed) |
| F14 | evidence | `git show @REV@:.ufo/waves/round-43/logs/residual8/ResCritBulkAppend.log \| grep -oE '\b[EW][0-9]{2}\b' \| sort -u \| wc -l` | 16 | 16 | **16** | CONST (round-43 log closed) |
| F15 | evidence | `git show @REV@:.ufo/waves/round-44/evidence/census-end.txt \| grep -oE '^rows=[0-9]+' \| cut -d= -f2` | 245 | 245 | **245** | CONST (r44 census receipt closed) |

Moves this round: **F01, F02, F03, F05, F08** (4-cell rows).
Revision-constant, fifth cell `CONST=<reason>`: **F04, F06, F07, F09, F10, F11,
F12, F13, F14, F15** (already in the draft). F02 already moves between 554ff416
(73) and 3ad8faaa (74); the landed 75 makes it move against both.

## 2b. Definitions I had to fix (so the L1 can defend them)

* **F01 "registry row count"** is the row *shape* (0–3 leading spaces, then
  `| S<digits>`), as the r44 ledger's F01 did. 245 at both revisions. It does not
  require the row to sit inside `## Registry`; census E12 is what flags a
  row-shaped source outside the section. The C3 append should move it to 246
  whether or not the section guard passes.
* **F05 "SKILL.md registry-row count"** = data rows in the seven tables whose
  header is the eight standard cells (headers at lines 162, 524, 588, 643, 718,
  796, 881 of `SKILL.md@HEAD`). Cross-checked the grep against an escaped-pipe
  TSV parser: 7 tables, 43 data rows, 0 non-8-cell rows, so grep is exact at this
  tip. Table at 718 has 3 rows; a naive `split('|')` said 0 because row 721's
  entry cell carries escaped pipes (`--inputs FILE \| --selftest \|
  --dump-inputs`). F05's grep tolerates that row (escaped pipe is not in its name
  or kind cell); a future row with `\|` in either cell would be missed, so
  re-check F05 against the escaped-pipe parser at the landed tip.
* **F06 "gate-table count"** = occurrences of the exact eight-cell header line =
  7 — `tables=<n>` in contract P-C2 item 1 (a value of 1 is the r44 defect).
* **F07 "the unregistered count from the r44 inventory"** = 14 rows whose audit
  reason is `unregistered: no row names mori-…` in
  `.ufo/waves/round-44/w1/ExecGateInventory.md`. Its §2b FAIL table has **15**
  rows; the 15th (`mori-round19-regressions.py`) fails for *no `--selftest`
  mode*, not for being unregistered. Both numbers are real; the row asserts the
  unregistered 14 because that is the phrase in the assignment.
* **F08 "`--selftest`-capable tools"** = 28, not 29. 29 tracked `tools/*.py|*.sh`
  contain the token; `mori-silence-cases.sh`'s only occurrence is comment line
  20, so the pipeline drops it. I read the 28 survivors' branch lines: each is a
  real argv branch (`parser.add_argument("--selftest" …)`,
  `if argv == ["--selftest"]`, `[[ ${1-} == --selftest ]]`, or a `case` arm). At
  entry, `mori-round19-regressions.py` and `mori-routed-check.py` carry no token
  at all (outside the 29) but are the other two tools item 11 fixes — hence the
  landed estimate 28 + 3 = 31.
* **F12/F13 "wave report count"** = `*.md` files under `.ufo/waves/round-4X/w1`
  (seat reports), matching the r44 ledger's use of `round-43/w1` (its F09). If
  the L1 prefers whole-round markdown, the numbers are 144 (round 43) and 34
  (round 44); pick one definition and do not mix them.
* **F14 "census W/E code count"** = the sources-census code space, **16** codes
  (E01–E12, W01–W04). The lane does not vendor `scripts/sources-census.sh` (that
  is `<fleet>/scripts/sources-census.sh`, outside this repo), so the only
  lane-measurable committed copy is the r43 log quoting the census usage block at
  its lines 59–68. Rejected alternatives: distinct codes *emitted* in one lane
  run = 1 (only W04, `census-end.txt`); warn/crit `severity=` emission sites in
  `tools/mori-census.sh` = 17 (a different instrument). The lane's own census has
  no W/E vocabulary.
* **F15** is an independent witness of the same 245: the r44 census receipt's
  `rows=245`. It stays 245 after F01 becomes 246 because it is a frozen r44
  measurement. Do not "reconcile" them; the disagreement is evidence the census
  ran before the C3 append.

## 3. Measured evidence (commands, exit codes, banners)

### 3a. The 15 commands at both revisions

Run through the round-44 counter's invocation tail (`<cmd> 2>/dev/null | head -c
64`), cwd = the lane repo; left = 554ff416…, right = 3ad8faaa…:

```
F01 registry 0 245 | 245 SAME
F02 corpus   0  73 |  74 DIFF
F03 corpus   0  54 |  54 SAME
F04 checks   0  33 |  33 SAME
F05 registry 0  43 |  43 SAME
F06 registry 0   7 |   7 SAME
F07 evidence 0  14 |  14 SAME
F08 checks   0  28 |  28 SAME
F09 checks   0 353 | 353 SAME
F10 checks   0 388 | 388 SAME
F11 checks   0 321 | 321 SAME
F12 wave     0  10 |  10 SAME
F13 wave     0  32 |  32 SAME
F14 evidence 0  16 |  16 SAME
F15 evidence 0 245 | 245 SAME
```

### 3b. The draft parsed and reconciled by the round-45 counter's own code

The counter refuses `WORK` and reads the ledger at a committed revision, which I
must not create (read-only VCS). I therefore loaded its module in-process
(`importlib` on `.ufo/waves/round-45/count-c1.py`) and called its
`parse_ledger`/`check_text` — the same functions `main` uses — on (a) the draft
as written and (b) the draft with the measured values filled in:

```
DRAFT AS WRITTEN: rows 15 problems 15
   row 11: value '?' is not an integer
   … (one per row; the only problem class is the deliberately unasserted value)
FILLED: rows 15 problems []
check rows_parse             PASS (15 rows)
check row_floor              PASS (rows=15 floor=12)
check class_floor            PASS (classes=checks,corpus,evidence,registry,wave floor=4)
check commands_reconcile     PASS (all rows match)
check other_rev_present      PASS (554ff416…)
check revision_sensitivity   FAIL (F01 value=245 at both revisions; F03 value=54 at both revisions;
                                   F05 value=43 at both revisions; F08 value=28 at both revisions)
meta {'rows': 15, 'classes': [...5...], 'mismatches': 0, 'moved': 1, 'const': 10}
```

Interpretation: `mismatches=0` — all 15 commands reproduce their measured values
at the committed tip through the counter's own tokenizer and pipefail runner.
The sensitivity failure lists exactly the four rows I classify MOVE whose change
lands **at the landed tip** (C3's S473/knowledge entry, C2's SKILL rows, item
11's three selftest branches). At 3ad8faaa they have not landed yet; `moved=1`
is F02. This is the expected before-state, not a defect in the draft: a landed
`figures.tsv` must show `moved=5, const=10`, or the round did not do the work the
rows claim.

### 3c. Supplementary measurements behind §2b

```
$ git show HEAD:SKILL.md | grep -cE '^\| name \| kind \| entry \| verdict map \| self-test \| pinned values \| write scope \| owner \|$'
7
$ git show HEAD:SKILL.md | grep -cE '^\| [^|]+ \| (gate|probe)'
43
$ git show HEAD:.ufo/waves/round-44/w1/ExecGateInventory.md | grep -c 'unregistered: no row names'
14
$ # §2b FAIL table, rows between '### 2b.' and '## 3.' starting '| tools/'
15   (14 x `unregistered: no row names`, 1 x `tool has no --selftest mode`)
$ git grep -l -- '--selftest' HEAD -- tools | grep -cE '\.(py|sh)$'
29
$ git show HEAD:.ufo/waves/round-43/logs/residual8/ResCritBulkAppend.log | grep -oE '\b[EW][0-9]{2}\b' | sort -u | tr '\n' ' '
E01 E02 E03 E04 E05 E06 E07 E08 E09 E10 E11 E12 W01 W02 W03 W04
$ git show HEAD:tools/mori-census.sh | grep -cE 'severity=(warn|crit)'
17
$ git log --oneline --name-status 554ff416..HEAD -- corpus/lessons
b1d7269f round-44 verifier spot-check (integrator, hyaku): non-author admit/reject
A	corpus/lessons/round-44-verifier-spotcheck.md
```

## 4. Risks the L1 must resolve at the landed tip

1. **F02's entering-tip column is ambiguous by construction.** contract.md names
   554ff416 as the entering tip, but `b1d7269f` (the round-44 verifier
   spot-check, parent of the r45 freeze commit) is an admitted post-tip commit
   that added one lesson. I record 73 at the contract revision and 74 at the
   current tip; expected landed 75. State which revision the "entering" column
   used; do not present 74 as the entering value.
2. **F05's +7 is a plan number, not a measurement.** It assumes item 20's seven
   rows all land verbatim (3 orphan tools + 3 r45 counters + 1 append-only
   superseding row). If the supersede replaces instead of appending, F05 is 49.
   Re-measure; do not copy 50 into the ledger without running the command.
3. **F08 is a lower-bound proxy.** "Occurrence outside a comment line" is not a
   proof of an argv branch; I hand-read all 28 at entry and each is a real
   branch. If a landed edit moves a branch behind a docstring/comment, the
   pipeline still counts it — the counter's `no_selftest` arm (P-C2 item 4) is
   the authority; this row is a cheap gross count.
4. **F04 and F06 are CONST only under the plan.** Any seat that adds a new
   `tools/*.py|*.sh` moves F04; any new eight-cell table moves F06. Both were
   33/7 before and after the r45 freeze commit; verify at the tip.
5. **The census instrument is not in this repo.** F14 measures the lane's
   committed *copy* of the code space (an r43 log), not
   `<fleet>/scripts/sources-census.sh` bytes. A live-script count is not a lane
   `git` pipeline and does not belong in this ledger.
6. **Five rows must move or be re-marked.** At the landed tip, F01/F03/F05/F08
   are 4-cell rows and the counter will reject them if their values still equal
   the other revision's. If the round lands without all of C2/C3/item 11, the
   honest repair is to add `CONST=<reason>` **and say the round did not land the
   work** — not to fake a moving value. F01/F03 are the two I am most confident
   move (one source row + one knowledge file); F05/F08 depend on two other
   seats' deliverables landing.
7. **Pipefail turns a zero into a failure.** Every stage must exit 0. If a
   landed append makes any pattern match zero lines (e.g. F07's inventory phrase
   edited away), the row becomes `unreadable`, not `0`. That is the counter
   working as designed; fix the command, do not weaken it.

No blockers. Nothing in this seat required a network read, a package install, or
a labrat probe.
