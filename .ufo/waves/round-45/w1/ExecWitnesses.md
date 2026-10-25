# ExecWitnesses — the three C1 vacuity witnesses and their BEFORE receipt

Status: **DONE**. Three witness ledgers are built; the **unmodified round-44
counter scores all three `C1=met mismatches=0` (rc 0)** at a measured tree equal
to `554ff416` plus the witnesses. The three holes named in `contract.md` §P-C1
kill rules are open in the round-44 instrument. One receipt caveat is load-bearing
and is stated first (§2).

| item | path | bytes | sha256 |
|---|---|---|---|
| witness W-REVCONST | `.ufo/waves/round-45/fixtures/witnesses/w-revconst.tsv` | 965 | `bbccaf28e69bbdfa324138d3d0a267d8878a1bd16004c87a8e00d1e98edc0fd4` |
| witness W-HEAD | `.ufo/waves/round-45/fixtures/witnesses/w-head.tsv` | 1122 | `a17d6b1adb43c1fc93aa33ad27a09d015ba4405cb8c4623e344ca71ef7b400cb` |
| witness W-DUP | `.ufo/waves/round-45/fixtures/witnesses/w-dup.tsv` | 980 | `fcaadd3155c245d346202393526ed4a7947d6df459ef79ece3205f4d76ea9b70` |
| receipts | `.ufo/waves/round-45/evidence/witness-r44.txt` | 26989 | `49426427e50efbf03bb06579544859e6c84a1589e5084aedbaae66ccfbaa94bc` |
| instrument (unmodified, read-only) | `.ufo/waves/round-44/count-c1.py` | — | `9477824d5eee45f47d49be52902f7bb0cd67a4d038e0ec7e79094c1e71999f83` |

The receipts file is 40 captured command blocks; every output below is copied
from it, none is reconstructed.

## 1. What each witness is vacuous about

All three are 12-row, 5-class (`checks,corpus,evidence,registry,wave`) ledgers in
the `.ufo/waves/round-44/figures.tsv` 4-cell shape `id \t asserted \t class \t command`
(the cell order the r44 parser actually reads, `fid, asserted, cls, cmd`). No
header, no comment lines, no CONST= marker anywhere.

### W-REVCONST — the whole ledger is revision-blind
Every one of its 12 rows returns the **same integer at `554ff416`, `b1d7269` and
`3ad8faaa`** (measured, §5 of the receipts). Two-rev proof, the two revisions the
assignment names:

| id | class | value @554ff416 | value @b1d7269 | row |
|---|---|---|---|---|
| F01 | registry | 4 | 4 | `git show @REV@:SKILL.md \| grep -c '^\| r44 '` |
| F02 | registry | 245 | 245 | `corpus/SOURCES.md` S-id rows |
| F03 | registry | 29 | 29 | `tools/*.py` count |
| F04 | corpus | 54 | 54 | `corpus/knowledge/*.md` count |
| F05 | corpus | 119 | 119 | `corpus/QUALITY.md` numbered entries |
| F06 | corpus | 3 | 3 | `git grep -l 'Z ゾンビ'` |
| F07 | wave | 72 | 72 | `round-43/logs` files |
| F08 | wave | 10 | 10 | `round-43/w1/*.md` |
| F09 | wave | 63 | 63 | `round-44` tree files |
| F10 | evidence | 4 | 4 | `round-44/fixtures` files |
| F11 | evidence | 15 | 15 | `round-43/evidence` files |
| F12 | checks | 14 | 14 | `round-43/evidence/c1s-after.txt` `^check` lines |

Nothing in the ledger can detect that it was scored at the wrong revision: it would
read the same at any revision whose tree agrees on those paths.

### W-HEAD — the measured `--rev` is ignored by every row
Three tip-resolving mechanisms, all three from the item's list, in one ledger:

| resolver | rows | exec text |
|---|---|---|
| `HEAD` | F01, F04–F08, F10, F11 (8) | `git show HEAD:<path>` / `git ls-tree … HEAD <path>` |
| hard-coded 40-hex `554ff416459c…` | F02, F09 (2) | `git show 554ff416…:SKILL.md`, `…:w1-spec.json` |
| `master@{u}` | F03, F12 (2) | `git show master@{u}:SKILL.md`, `…:c1s-after.txt` |

The token proof in the receipts cuts each row at its first `#` and shows
`exec_has_@REV@=False` for **all 12 rows**: the executable text never reads
`@REV@`. The token survives the round-44 parser only because the parser's sole
revision test is the substring test `"@REV@" not in cmd` (source line 100), which a
trailing `# @REV@` comment satisfies. That is the exact shape of the hole — a
ledger can *name* the measured revision without *using* it.

### W-DUP — duplicate id and duplicate command, everything else honest
`cut -f1 | sort | uniq -d` → `F05` (rows 5 and 11). `cut -f4 | sort | uniq -d` →
`git ls-tree -r --name-only @REV@ .ufo/waves/round-43/evidence | grep -c .`
(rows F09 and F11, both 15). The duplicate id pair carries *different* commands
(72 wave / 73 corpus), so it is a reused-id defect, not a copy of one row.

The other 10 rows are honest, and two of them are deliberately **revision-
sensitive**, so the ledger is not merely a second W-REVCONST:

| id | asserted | value @554ff416 | value @b1d7269 |
|---|---|---|---|
| F04 | 327 | 327 | 328 |
| F05 (2nd) | 73 | 73 | 74 |

## 2. Receipt 1 — the command exactly as assigned rejects on *absence*, and says nothing about vacuity

`python3 .ufo/waves/round-44/count-c1.py 554ff416 --ledger <absolute witness> --repo <lane>`:

| witness | only failing check | verdict | rc |
|---|---|---|---|
| w-revconst | `ledger_present FAIL (absent)` | `C1=unmet mismatches=?` | 1 |
| w-head | `ledger_present FAIL (absent)` | `C1=unmet mismatches=?` | 1 |
| w-dup | `ledger_present FAIL (absent)` | `C1=unmet mismatches=?` | 1 |

**Saying this loudly, as instructed:** these `C1=unmet` lines are *not* the
counter rejecting a vacuous ledger. `read_at()` reads the ledger out of the
measured revision's tree (`git cat-file -e REV:path`, then `git show REV:path`),
and no round-45 file exists at `554ff416` — the lane is read-only to every seat
this wave, so it never can. Scored literally at that revision, *every* newly
written ledger is "absent", which means the literal command cannot measure the
defect at all. It is still recorded in the receipts (§1) as the honest output of
the named command, and it is itself a fact the round-45 counter must design
around: witnesses have to be read from the filesystem (`--witness-dir`), not from
`--rev`'s tree.

## 3. Receipt 2 — the fair BEFORE receipt: same unmodified counter, ledger committed, tree == `554ff416`

Fixture repo `.ufo/waves/round-45/tmp/ExecWitnesses/clone`: `objects/info/alternates`
→ `mori-shokunin/.git/objects`, index read from `554ff416`, the three witness blobs
added, commit `b957dad8…` parented on `554ff416`.

```
$ git -C clone log --format='%H %p %s' -1 b957dad8
b957dad8ddb38bc6b19e255e88a88bd4f912351f 554ff416 round-45 C1 witness fixture: 554ff416 tree + 3 witness ledgers
$ git -C clone diff --stat 554ff416 b957dad8
 .ufo/waves/round-45/fixtures/witnesses/w-dup.tsv      | 12 ++++++++++++
 .ufo/waves/round-45/fixtures/witnesses/w-head.tsv     | 12 ++++++++++++
 .ufo/waves/round-45/fixtures/witnesses/w-revconst.tsv | 12 ++++++++++++
 3 files changed, 36 insertions(+)
```

Every counted byte is therefore the `554ff416` byte; the measured revision differs
from the entering tip only by the three ledgers being present.

| witness | rows | classes | verdict | rc |
|---|---|---|---|---|
| w-revconst | 12 | 5 | `C1=met mismatches=0` | **0** |
| w-head | 12 | 5 | `C1=met mismatches=0` | **0** |
| w-dup | 12 | 5 | `C1=met mismatches=0` | **0** |

All three pass with the instrument untouched: `rows_parse PASS`, floors satisfied,
`commands_reconcile PASS (all rows match)`.

## 4. Receipt 3 — supplementary, live lane `rev=WORK`

Same counter, witness read off the worktree, rows recomputed at the lane tip
`3ad8faaa`:

| witness | verdict | rc | note |
|---|---|---|---|
| w-revconst | `C1=met mismatches=0` | 0 | accepted on the live lane too |
| w-head | `C1=met mismatches=0` | 0 | accepted on the live lane too |
| w-dup | `C1=unmet mismatches=2` | 1 | `F04 327 observed 328`, `F05 73 observed 74` |

The w-dup failure here is the per-row value check firing because the tip differs
from `554ff416` — **not** duplicate detection, which does not exist (§6). Its
authoritative receipt is §3, measured at the tree the ledger declares.

## 5. `contract.md` kill-rule mapping (the C1 control)

§Kill rules: *"a ledger of revision-constant figures, a HEAD-reading row, or a
duplicate id/command must not print `C1=met`."* Measured against the round-44
counter: **all three print `C1=met`.** The round-44 counter therefore cannot serve
as the C1 control; a do-nothing C1 arm built on it would print met on all three
kill-rule violations.

## 6. Why it passes — measured absence in the round-44 instrument

| probe | result |
|---|---|
| `grep -c 'other-rev'` / `'CONST'` / `'witness'` / `'duplicate'` / `'dup'` / `'rev-parse HEAD'` on count-c1.py | `0` each (rc 1) |
| `count-c1.py <rev> … --other-rev b1d7269` | argparse `unrecognized arguments` → **rc 2** |
| `count-c1.py <rev> … --witness-dir fixtures/witnesses` | argparse `unrecognized arguments` → **rc 2** |
| source line 100 | `if "@REV@" not in cmd:` — the *only* revision control |
| source line 111 | `full = "%s 2>/dev/null \| head -c 64" % cmd.replace("@REV@", rev)` |
| source line 152 | `for fid, asserted, _cls, cmd in rows:` — one revision, one loop |

Consequences, one per witness: no two-revision comparison exists, so
**W-REVCONST** is indistinguishable from a sensitive ledger; no tip-resolver
rejection exists, so **W-HEAD** passes on a trailing comment; no id/command
uniqueness test exists, so **W-DUP** passes.

## 7. Adjacent holes measured (outside the three mandated classes, reported not fixed)

1. **An absent path is scored as integer 0.** Probe ledger = 11 w-revconst rows +
   `F12 0 checks git show @REV@:no/such/path-r45-probe.txt | grep -c x`, committed as
   `c01352a3…` (parent `b957dad8`). `git show` on that path exits **128**; the
   counter appends `2>/dev/null | head -c 64`, so the pipeline status is `head`'s 0
   and the empty stdout count `0` equals the assertion → `C1=met rc=0`. This is on
   the round-45 required-changes list ("an absent path is a FAIL not a zero").
2. **The floors are caller-overridable.** A 3-row / 3-class probe ledger
   (`1cfd300e…`, parent `c01352a3`) prints `C1=met mismatches=0 rc=0` with
   `--min-rows 1 --min-classes 1`, and `C1=unmet rc=1` at the defaults. "Floors hold
   (clamped up)" is a round-45 addition, not an existing property.

Both are recorded because the same producer/résumé lines make them reachable by the
same class of vacuous ledger; neither was patched (write scope is the three
witnesses plus receipts).

## 8. Risks and actionable notes for the round-45 C1 builder

1. **W-HEAD is only caught by a tip-resolver rule, never by the `@REV@` rule.**
   All 12 rows *name* `@REV@` (in a trailing comment). A counter that enforces only
   "row names `@REV@`" will accept `w-head.tsv` whole. The rejection must key on
   `HEAD`, `@{u}` or a 40-hex object name in the **executable** text.
1b. **A literal `git rev-parse HEAD` row cannot be the fixture.** Measured: the r44
   parser's read-verb allowlist is `cat-file, diff, grep, log, ls-tree, rev-list,
   show`, so `git rev-parse HEAD | grep -c .` is rejected as
   `git verb 'rev-parse' is not a read verb` *and* `does not name @REV@` — a format
   rejection that would make the witness unmet for the wrong reason. `w-head.tsv`
   therefore reaches the same tip through `show`/`ls-tree` (allowed verbs) reading
   `HEAD`, a fixed 40-hex, or `@{u}`. The `--selftest` arm should carry this exact
   shape (token present but unused), not a bare rev-parse row.
2. **`@{u}` has an availability precondition.** In this lane `master@{u}` resolves to
   `3ad8faaa` only because `master` tracks `origin/master`; bare `@{u}` on the
   detached HEAD fails. The r45 selftest must create the upstream explicitly (or skip
   that arm) so an unresolvable row is never counted as a "tip-reader rejected" pass.
3. **W-DUP is not sole-cause isolated under the 4-cell shape.** The r44 shape has no
   `CONST=` slot, so 10 of its 12 rows are revision-constant. If round 45 enforces
   per-row "value moves, or `CONST=<reason>`", `w-dup.tsv` will be rejected at
   constancy *before* duplication, and a mutant that deletes the duplicate check
   would survive its own fixture. Recommendation: once the round-45 grammar for
   `CONST=` is fixed, add `CONST=<reason>` to the constant rows of `w-dup.tsv` (one
   member of each pair included) so duplication is the only admissible defect. I did
   not guess a grammar I could not verify, so the file stays in the r44 shape.
4. **Revision-sensitive material between these two revisions is thin.** The only
   tree delta is `corpus/lessons/round-44-verifier-spotcheck.md` (42 lines), so
   exactly two tree-based figures move: `corpus` file count 327→328 and
   `corpus/lessons/*.md` count 73→74. Do **not** use `git rev-list --count @REV@` for
   this pair: it counts the measured commit itself and therefore shifts under any
   fixture commit (measured 447 / 448 / 449). My first w-dup draft asserted 447 and
   the fixture commit observed 448 — corrected to tree-based rows.
5. **Witness population.** `fixtures/witnesses/` holds exactly the three `*.tsv`
   files, so `witnesses=3/3` is reachable with a plain non-recursive glob. My two
   scratch probe ledgers live under `tmp/ExecWitnesses/probe/` (`absent-path.tsv`,
   `below-floor.tsv`) — a **recursive** `.tsv` glob under `round-45/` would pick them
   up; the `--witness-dir` arm should target `fixtures/witnesses` non-recursively.
6. **No seat can produce a new ledger at `554ff416`.** Any verification run that
   repeats the literal command and sees `C1=unmet` is seeing the absent-ledger
   artifact from §2, not a witness rejection. The round-45 counter must read
   witnesses from disk; a receipt that names `554ff416` as `--rev` cannot read a
   round-45 file.

## 9. Verification actually run (all in `evidence/witness-r44.txt`)

- `sha256sum` of instrument and witnesses; `git rev-parse` of HEAD, master,
  origin/master, `554ff416`, `b1d7269`.
- Literal assigned command on all three witnesses (3 verdicts + rc).
- Fixture-commit construction proof: `log -1`, `diff --stat 554ff416 b957dad8`,
  `rev-parse HEAD master@{u}` in the fixture repo.
- Fair run on all three (3 verdicts + rc): all `C1=met`, rc 0.
- `rev=WORK` run on all three on the live lane.
- Per-row audit of every row at `554ff416`, `b1d7269`, `3ad8faaa`
  (`tmp/ExecWitnesses/audit_rows.py`, replicating `run_row` exactly), duplicate
  detection, and the `@REV@`/tip-resolver token proof for w-head.
- Source-level absence proofs with line numbers; argparse rc=2 for both missing flags.
- Two adjacent-hole probes (absent path, floor override) with their control runs.

## 10. Scope, tooling, open items

- Files written: the three witness ledgers, `evidence/witness-r44.txt`, this report,
  plus scratch under `tmp/ExecWitnesses/` (`probe.py`, `audit_rows.py`,
  `gen_evidence.sh`, `clone/`, `probe/`). Nothing else in the lane was touched;
  `SKILL.md`, `SCORECARD.md`, `LOG.md`, `corpus/*`, `contract.md`, the round-44
  instruments and other seats' reports were not modified.
- No tool installs or upgrades; no `pacman` transaction (paused host-wide); host
  `git` and `python3` only.
- Open item for the L1, not for me: the fair receipt's measured revision is
  `b957dad8…` (tree = `554ff416` + the three witnesses), because `554ff416` itself
  cannot contain a round-45 file. The lock is the `diff --stat` proof, not a claim
  that `b957dad8` is `554ff416`.
