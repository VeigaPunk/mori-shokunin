# ExecLedger — round-44 C1 figure ledger draft

Seat: `L1Mori44-4.ExecLedger` (leaf). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Freeze commit: `7cb59c6891d4f5d0266fe062565f094da835dc84`. Lane tip at measurement:
`7cb59c6891d4f5d0266fe062565f094da835dc84` (HEAD; tree clean except untracked
`.ufo/waves/round-44/w1-spec.json`). Entering tip for context: `1429c791db5891c484684feef893799909d2d6a8`.

Wrote exactly one file: this report. No ledger file, no instrument, no `SKILL.md`, no
`corpus/`, no `SCORECARD.md`/`LOG.md`. All scratch work ran in a throwaway clone at
`/tmp/mori44-ledger-RfhAN4/lane` (`git clone` + sandbox commits only); the lane checkout was
read-only (`ls-tree`, `show`, `grep`, `rev-parse`). No `pacman`/`uv`/`npm` install was needed.

## 1. What the draft is

A 20-row ledger (`F01`..`F20`) covering all five declared classes, every row a count the
round's report will cite, every row a single `git` pipeline naming `@REV@`. It parses under the
frozen `parse_ledger` and **reconciles at the freeze commit**:

```
check ledger_present       PASS (1671 bytes)
check rows_parse           PASS (20 rows)
check row_floor            PASS (rows=20 min=12)
check class_floor          PASS (classes=checks,corpus,evidence,registry,wave min=4)
check commands_reconcile   PASS (all rows match)
rev=85fc3bca5c0138eff2f59d206d584a6f1d390801
C1=met mismatches=0
exit=0
```

That run is at sandbox rev `85fc3bca`, a commit whose tree is `7cb59c68` plus this ledger — the
freeze-equivalent tip. Command:

```
python3 .ufo/waves/round-44/count-c1.py 85fc3bca5c0138eff2f59d206d584a6f1d390801
```

**The draft is honest at the freeze and will be stale at the landed tip.** Eight rows count
paths this wave populates (see §4). Freeze and lane tip agree on all 20 rows today only because
the tip *is* the freeze commit; the ledger must be re-derived at the landing commit before it is
filed. §5 gives the exact landing recipe that keeps "no filed byte is rewritten" intact.

## 2. Draft ledger — `.ufo/waves/round-44/figures.tsv`

Four TAB-separated cells, no comment column, no header. Values below are the **freeze/tip
observation**; §4 replaces the eight landing-derived cells.

```
F01	72	wave	git ls-tree -r --name-only @REV@ .ufo/waves/round-43/logs | grep -c .
F02	10	wave	git ls-tree -r --name-only @REV@ .ufo/waves/round-43/w1 | grep -c '\.md$'
F03	8	wave	git grep -l 'provider.rate_limit' @REV@ -- .ufo/waves/round-43/logs | grep -c .
F04	39	wave	git grep -l '429' @REV@ -- .ufo/waves/round-43/logs | grep -c .
F05	32	wave	git ls-tree --name-only @REV@ .ufo/waves/ | grep -c .
F06	0	wave	git ls-tree -r --name-only @REV@ .ufo/waves/round-44/w1 | grep '\.md$' | wc -l
F07	243	registry	git show @REV@:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'
F08	192	registry	git show @REV@:corpus/SOURCES.md | grep -c '| mined |'
F09	6	evidence	git ls-tree -r --name-only @REV@ .ufo/waves/round-44/evidence | grep -c .
F10	3	evidence	git ls-tree -r --name-only @REV@ .ufo/waves/round-44/evidence | grep -c 'control-'
F11	10	evidence	git show @REV@:.ufo/waves/round-44/evidence/freeze-r44.txt | grep -cE '^[0-9a-f]{64}  '
F12	72	corpus	git ls-tree -r --name-only @REV@ corpus/lessons | grep -c '\.md$'
F13	116	corpus	git show @REV@:corpus/QUALITY.md | grep -cE '^[0-9]+\. '
F14	53	corpus	git ls-tree -r --name-only @REV@ corpus/knowledge | grep -c '\.md$'
F15	195	corpus	git ls-tree -r --name-only @REV@ corpus/evidence | grep -c .
F16	28	corpus	git ls-tree -r --name-only @REV@ corpus/lessons | grep -c 'verifier-spotcheck'
F17	4	checks	git show @REV@:SKILL.md | grep -c '^| r44 '
F18	3	checks	git ls-tree --name-only @REV@ .ufo/waves/round-44/ | grep -c 'count-c[0-9]\.py'
F19	4	checks	git ls-tree -r --name-only @REV@ .ufo/waves/round-44/fixtures | grep -c .
F20	6	checks	git show @REV@:.ufo/waves/round-44/count-c1.py | grep -c '^    arm('
```

Class census: wave 6, registry 2, evidence 3, corpus 5, checks 4 — 20 rows, 5 classes
(floors: 12 rows, 4 classes).

Byte check before committing (`NF` must be 4 everywhere):

```
awk -F'\t' 'NF!=4{print NR": "NF}' .ufo/waves/round-44/figures.tsv
```

### Why these commands

The command vocabulary reuses the frozen witness `fixtures/figures-r43.tsv` wherever the two
overlap (registry regex, criteria regex, seat-log/seat-report forms) so the ledger and the
witness cannot disagree about what a count means. `F01`–`F04` are the round-43 figures the
closure routed (defect 3), carried as *corrected* rows: 72 seat logs, 10 seat reports, 8 logs
carrying `provider.rate_limit`, 39 logs merely containing the string `429`. A ledger that
reconciles these is the calibration evidence the round needs.

## 3. Per-row reconciliation

Required table. `observed-at-freeze` and `observed-at-tip` were produced by the counter's own
invocation (`bash -c "<cmd with @REV@ replaced> 2>/dev/null | head -c 64"`, cwd = lane repo), so
these are the bytes the counter reads, not an eyeball count.

| id | asserted | observed-at-freeze | observed-at-tip | class | count cited by the report |
|---|---|---|---|---|---|
| F01 | 72 | 72 | 72 | wave | round-43 seat logs (defect-3 figure, corrected) |
| F02 | 10 | 10 | 10 | wave | round-43 seat reports (4 `Exec*` + 6 `ResCrit*`) |
| F03 | 8 | 8 | 8 | wave | logs carrying `provider.rate_limit` (was reported as 34) |
| F04 | 39 | 39 | 39 | wave | logs containing the string `429` (byte hits, not rate limits) |
| F05 | 32 | 32 | 32 | wave | `.ufo/waves/` round directories |
| F06 | 0 | 0 | 0 | wave | **round-44 wave-1 seat logs** — landing-derived |
| F07 | 243 | 243 | 243 | registry | **registry rows in `corpus/SOURCES.md`** — landing-derived |
| F08 | 192 | 192 | 192 | registry | registry rows with status `mined` — landing-derived |
| F09 | 6 | 6 | 6 | evidence | **files under `.ufo/waves/round-44/evidence`** — landing-derived |
| F10 | 3 | 3 | 3 | evidence | `control-c{1,2,3}-donothing.txt` |
| F11 | 10 | 10 | 10 | evidence | sha256 pins in `evidence/freeze-r44.txt` |
| F12 | 72 | 72 | 72 | corpus | **lesson files** — landing-derived |
| F13 | 116 | 116 | 116 | corpus | **admission criteria** in `corpus/QUALITY.md` — landing-derived |
| F14 | 53 | 53 | 53 | corpus | **knowledge entries** — landing-derived |
| F15 | 195 | 195 | 195 | corpus | files under `corpus/evidence` |
| F16 | 28 | 28 | 28 | corpus | verifier-spotcheck lessons — landing-derived |
| F17 | 4 | 4 | 4 | checks | `r44 ` rows in `SKILL.md`'s gate table |
| F18 | 3 | 3 | 3 | checks | round-44 counters |
| F19 | 4 | 4 | 4 | checks | **files under `.ufo/waves/round-44/fixtures`** |
| F20 | 6 | 6 | 6 | checks | `count-c1.py` selftest arms |

Freeze == tip for every row (`HEAD` is the freeze commit), so no row needs a freeze-vs-tip
re-derivation *today*. The rows that are rev-sensitive by construction are named in §4.

Rev-sensitivity is real and measured, not asserted: at the **entering** tip `1429c791` eight of
these rows read differently, because the freeze commit is where the round-44 artifacts appear —

```
id   freeze  enter
F05      32     31
F09       6      0
F10       3      0
F11      10      0
F17       4      0
F18       3      0
F19       4      0
F20       6      0
```

A ledger committed at the wrong revision is exactly the round-43 defect 5 shape ("receipt
measured at `dde525ea` while the verdict claims the landed tip"). This table is the proof that
each row is anchored to a specific tree, not to "whatever is on disk".

## 4. Rev-sensitive rows — re-derive at the landed tip

These rows count paths this wave writes. The ledger carries no comment column, so the
explanation lives here: **the asserted cell must hold the landed-tip value, and the value below
is either contract-predicted (grounded in `contract.md`) or unknown-until-landing.**

| id | freeze value | landing disposition | grounded in |
|---|---|---|---|
| F06 | 0 | **unknown** — re-derive | number of `*.md` reports in `.ufo/waves/round-44/w1/`, including this one |
| F07 | 243 | **245 observed in worktree** | contract P-C3: "registry 245 rows (S471, S472)" |
| F08 | 192 | **194 observed in worktree** | contract P-C3: the two new rows are `mined` |
| F09 | 6 | **unknown** — re-derive | evidence files the seats land |
| F12 | 72 | **re-derive** (73 or 74) | `corpus/lessons/round-44.md`, plus `round-44-verifier-spotcheck.md` if the closure lands with it |
| F13 | 116 | **119 observed in worktree** | the round's criteria append to `corpus/QUALITY.md` |
| F14 | 53 | **54 observed in worktree** | contract P-C3: "one admitted knowledge entry" |
| F16 | 28 | **re-derive** (29 predicted) | the round-44 closure spotcheck lesson |

### Worktree re-measurement (in-flight sibling work, uncommitted)

After the freeze-time measurement the worktree gained the C3 entry and a criteria append. These
are **uncommitted** bytes, so they are not what the counter reads at `7cb59c68` — but they are
what the landing commit will contain unless a seat changes course:

```
grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md   -> 245
grep -c '| mined |' corpus/SOURCES.md                          -> 194
grep -cE '^[0-9]+\. ' corpus/QUALITY.md                        -> 119
ls corpus/knowledge/*.md | wc -l                               -> 54
ls corpus/lessons/*.md | wc -l                                 -> 72
ls corpus/lessons/ | grep -c 'verifier-spotcheck'              -> 28
find corpus/evidence -type f | wc -l                           -> 195
```

`git diff --stat` at the same moment: `corpus/QUALITY.md | 40 +++…`, `corpus/SOURCES.md | 2 ++`.
The two added registry rows are `S471` (proc(5) ja translation) and `S472` (proc(5) zh_TW
translation), both `mined` — matching the contract's `245 (S471, S472)` sentence exactly.

**This is why F13 is listed as landing-derived rather than stable.** I first classified
`corpus/QUALITY.md` as untouched by the round; the worktree shows a three-criterion append
(116 → 119). A ledger filed on my first classification would have been off by three — the same
class of slip the round is answering. `F12`/`F16` had not moved at this reading, but both are
still listed as re-derive because the round's own lesson is not yet written.

`F15` (`corpus/evidence`, 195) was unchanged at this reading; re-check it at landing.

`F17` is stable for this landing only because `SKILL.md` is frozen: its sha256
`f9b1e2bf…76d05` is pinned in `evidence/freeze-r44.txt` and the wave context forbids editing it.
`F10`, `F11`, `F18`, `F19`, `F20` are stable because the freeze instruments and their evidence
are byte-pinned. `F01`–`F05` are stable because round-43 artifacts are immutable.

**Prediction arithmetic was mechanically validated, not assumed.** In the sandbox I appended
exactly the artifacts the contract names (two `mined` `S471`/`S472` rows, one knowledge entry,
`round-44.md`, `round-44-verifier-spotcheck.md`, two `w1` reports, one evidence file, three
numbered criteria), wrote the predicted landing values, and re-ran the frozen counter at the
resulting commit:

```
check rows_parse           PASS (20 rows)
check commands_reconcile   PASS (all rows match)
rev=557032875616f99d8cb1fa67eef20bb110741c70
C1=met mismatches=0
exit=0
```

and again after the criteria append was added to the simulation (`F13` 116 → 119):

```
check commands_reconcile   PASS (all rows match)
rev=729ed5aca82ce7ec477c54729efa6df49d4c1cb9
C1=met mismatches=0
exit=0
```

So `245 / 194 / 54 / 119 / 29 / 74` are the arithmetic consequences of the contract's own
sentences plus the worktree's criteria append. Only `F06` and `F09` magnitudes remain genuinely
unknown, because only the seats decide how many reports and evidence files they file.

## 5. Landing recipe (keeps the ledger filed once, correctly)

The counter reads the ledger *at the measured revision* (`read_at` → `git show <rev>:<path>`), so
the ledger cannot be scored against a tree that does not contain it, and a filed byte must not be
rewritten afterwards (round-43 routed defect 2). Order that satisfies both:

1. Land the wave's reports, evidence, corpus and gate changes — commit **A**.
2. `R1=$(git rev-parse HEAD)`. For each of `F06 F07 F08 F09 F12 F13 F14 F15 F16`, run the row's
   command with `@REV@` = `$R1` and transcribe the observed integer into the asserted cell.
3. Commit `figures.tsv` alone — commit **B**. This perturbs no row: every value measured at
   `7cb59c68` (no ledger in the tree) equals the value measured at `85fc3bca` (ledger in the
   tree), which is the self-reference check.
4. `python3 .ufo/waves/round-44/count-c1.py $(git rev-parse HEAD)` → expect
   `C1=met mismatches=0`, exit 0.

If the commit-B run reports a mismatch, the counter names it as
`<id> asserted=<a> observed=<b>`; that is the transcription to fix before filing, not a reason to
weaken a row.

## 6. Fallback: 12-row immovable spine

If the landing sequence cannot be completed (seats file late, the ledger commit lands before the
reports), a ledger restricted to the rows that no wave write can touch still clears the floors at
*any* revision. The spine is `F01 F02 F03 F04 F05 F10 F11 F15 F17 F18 F19 F20` — 12 rows, classes
wave/evidence/corpus/checks — exactly at both floors.

`F13` is **excluded** from the spine: my first version included it and passed, but that pass was
against a tree measured before the criteria append; `F13` is the one corpus row the round is
proven to move (116 → 119). With `F13` removed the spine was re-tested against the
criteria-appended simulated landing (two `w1` reports, one evidence file, two `mined` registry
rows, one knowledge entry, two lessons, three criteria):

```
check row_floor            PASS (rows=12 min=12)
check class_floor          PASS (classes=checks,corpus,evidence,wave min=4)
check commands_reconcile   PASS (all rows match)
rev=d8325d28328c89a375b71b2040401146414a1f81
C1=met mismatches=0
exit=0
```

The spine carries no registry-class row and no `corpus/knowledge` or `corpus/lessons` row, so it
cannot support the report's "245 registry rows", "54 knowledge entries" or "N lessons" sentences
— use it only if `F06`–`F09`/`F12`–`F16` cannot be pinned, and then do not cite those numbers.
Its corpus class rests on `F15` alone, so re-check `corpus/evidence` before relying on it.

## 7. Falsifier receipts

Every command below was run; outputs are verbatim.

**ARM A — witness (frozen fixture, must isolate the two round-43 slips).**
`python3 .ufo/waves/round-44/count-c1.py 7cb59c68 --ledger .ufo/waves/round-44/fixtures/figures-r43.tsv`

```
check commands_reconcile   FAIL (F03 asserted=15 observed=14; F04 asserted=34 observed=8)
C1=unmet mismatches=2
exit=1
```

Matches the contract's witness sentence exactly. The counter isolates the slips and passes the
other ten rows, so it discriminates rather than blanket-failing.

**ARM D — do-nothing control at the entering tip.** `python3 .ufo/waves/round-44/count-c1.py 1429c791`

```
check ledger_present       FAIL (absent)
C1=unmet mismatches=?
exit=1
```

**ARM B — first draft, rejected by the counter (my defect, kept as evidence).** At sandbox
`9cb8735e`:

```
check commands_reconcile   FAIL (F05 asserted=32 observed=1; F18 asserted=3 observed=0)
C1=unmet mismatches=2
```

Cause: `git ls-tree --name-only <rev> .ufo/waves` (no trailing slash, no `-r`) lists **the tree
entry itself**, so the count collapses to 1. Fixed by the trailing slash
(`.ufo/waves/` / `.ufo/waves/round-44/`). This is a silent off-by-31 failure mode that a
hand-written ledger would have filed as truth; it is the reason every row here was executed
rather than counted by eye.

**ARM B2 — fixed draft, met.** Output quoted in §1 (`C1=met mismatches=0`, 20 rows, 5 classes).

**ARM C — same ledger against a simulated landing.** At sandbox `673a7da8` (two `w1` reports +
one evidence file added):

```
check commands_reconcile   FAIL (F06 asserted=0 observed=2; F09 asserted=6 observed=7)
C1=unmet mismatches=2
```

This is the measured proof that exactly `F06` and `F09` (of the two simulated writes) are
landing-derived, and that the counter names them rather than drifting silently.

**ARM E — predicted landing values, met.** Quoted in §4: `C1=met mismatches=0` at `55703287`
(contract-shaped landing) and again at `729ed5ac` (with the criteria append).

**Instrument soundness.** `python3 .ufo/waves/round-44/count-c1.py --selftest` (in the sandbox
clone, frozen bytes):

```
selftest PASS honest_ledger_met
selftest PASS offbyone_row_mismatch
selftest PASS junk_producer_rejected
selftest PASS below_floor_rejected
selftest PASS absent_ledger_unmet
selftest PASS compound_command_rejected
C1_SELFTEST pass=6 fail=0
exit=0
```

## 8. Grammar hazards for the next ledger author

1. **`git ls-tree` needs a trailing slash for a directory's children.** Without `-r`, a bare
   tree pathspec yields one line (the tree). With `-r` it recurses. This is the ARM B defect.
2. **`| wc -l` masks a dead producer; `| grep -c .` does not.** `run_row` takes the *pipeline's*
   rc, which is the last command's. `git show … | grep -c .` returns 1 on empty input, so a
   missing path or failed `git show` surfaces as `unreadable`, not as a clean `0`. `| wc -l`
   always returns 0 and would report a false zero. Every row here ends in `grep -c` except
   `F06`, where the zero value at freeze is legitimate and `grep -c` would mislabel it
   `unreadable`.
3. **A legitimate zero is not expressible with `grep -c`.** `grep -c` exits 1 when the count is
   0, and `run_row` treats rc≠0 as unreadable. `F06` therefore uses
   `grep '\.md$' | wc -l`, accepting the masking in §8.2 because `F05` independently proves the
   `.ufo/waves/` tree exists at every revision measured.
4. **`@REV@` must be a revision, not a path.** `--ledger` resolves inside the measured tree
   (`git cat-file -e <rev>:<path>`); an absolute path outside the repo fails `ledger_present`.
5. `head -c 64` truncation means any row whose output is not a bare integer (e.g.
   `git grep -c` over multiple files, which prints `path:count`) fails as `unreadable`, not as a
   mismatch. All 20 rows print exactly one integer.

## 9. Risks and blockers

- **Ordering risk (blocking for the round, not for me):** `F06` cannot be asserted until every
  wave-1 report is committed, and this report is itself one of the counted files. Land the
  reports first, then the ledger (§5).
- **Prediction risk:** `F12` and `F16` depend on whether the round-44 closure spotcheck lesson
  lands in the same commit. Both are listed as re-derive, not as fixed values.
- **Corpus drift risk:** `F13` is already measured to move (116 → 119) and must be re-derived.
  `F15` (`corpus/evidence`, 195) was unchanged at the worktree reading but is re-checked at
  landing; a seat filing evidence there instead of under the wave dir moves it.
- **No blocker encountered** for this seat: every row's command was executed at the freeze, at
  the lane tip, and (for the rev-sensitive set) under a simulated landing.

## 10. Report

Report: `.ufo/waves/round-44/w1/ExecLedger.md`
