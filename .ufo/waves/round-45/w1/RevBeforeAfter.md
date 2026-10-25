# RevBeforeAfter — round-45 C1/C2/C3 before-after re-measurement

Seat: reviewer (leaf). Contract read first: `.ufo/waves/round-45/contract.md`.
Lane tip at final measurement: **`18fd68b0`** (the L1's landing commit
"round-45: SKILL.md registry refresh, corpus entry + row + README map, QUALITY
120-122, lesson, selftest branches"). It carries `SKILL.md`, `corpus/*`,
`tools/*`, `corpus/lessons/round-45.md` — **but nothing under
`.ufo/waves/round-45/`**. The counters, `figures.tsv`, the witnesses, the
write-scope fixture and the amended `contract.md` are all still uncommitted
(`git status`: `?? .ufo/waves/round-45/count-c{1,2,3}.py`, `?? figures.tsv`,
`?? fixtures/`, ` M contract.md`).

No `TMPDIR` override was used anywhere below (`env -u TMPDIR …`). No tool was
installed; lane git read-only.

Because the counters score *committed* bytes and the instruments are not
committed, I also encoded the worktree state as a commit in a throwaway repo
(`objects/info/alternates → <lane>/.git/objects`, lane only read):

- **S2 = `a7af6601dded5a1d791ccd1a8092286de2d63cec`**, parent `3ad8faaa`. Tree =
  exactly the claim bytes: `SKILL.md`, `corpus/{SOURCES.md,README.md,QUALITY.md,
  knowledge/*.md,lessons/*.md}`, `tools/`, `.ufo/waves/round-45/{count-c*.py,
  contract.md,figures.tsv,fixtures/**}`. Seat scratch and non-`.md` corpus files
  excluded; every figure/check the claims read is in it and all 15 ledger rows
  reconcile there (`commands_reconcile PASS (all rows match)`).

Instrument digests at the receipts: r44 `count-c1.py` `9477824d…`, v1 auditor
`743996b1…` (== `git show 554ff416:tools/mori-gate-registry.py`); r45
`count-c1.py` `5f2deea0…`, `count-c2.py` `153423c4…`, `count-c3.py` `37fd7c24…`,
auditor v2 `8b82ac99…`, `figures.tsv` `f05b0174…`, witnesses `w-dup` `fcaadd31…`
/ `w-head` `a17d6b1a…` / `w-revconst` `bbccaf28…`. (C2 receipts at S4;
C1/C3 receipts at S2; the earlier `e8ee29eb…` count-c2 digest was superseded
while the C2 seat finalized the mutant arm.)

## 1. Verdict table (as measured)

| claim | before (as declared) | after at worktree bytes (S2) | after at lane tip `18fd68b0` |
|---|---|---|---|
| C1 | literal: `C1=unmet rows=0` ×3 rc 1, red for **absence** · fair: `C1=met` ×3 rc 0 (vacuous green) | `C1=met … witnesses=3/3` rc 0 | **`C1=unmet failed=ledger_present` rc 1** |
| C2 | `--rev 554ff416 --audit-all` on v1: **usage rc 2, no verdict** | auditor `REGISTRY=met tables=7 registered=39 unregistered=0 no_selftest=0 duplicate=0 wrong_row=0` rc 0 · composite `C2=met` rc 0 (S4) | **`REGISTRY=unmet wrong_row=3` rc 1** · composite `C2=unmet wrong_row=3` rc 1 |
| C3 | `C3=unmet` rc 1 (entry/row/readme absent; census PASS) | `C3=met` rc 0, no `TMPDIR` | `C3=met` rc 0, no `TMPDIR` |

"After" answers the item's question on the bytes that exist; `18fd68b0` is the
only lane revision today, and C1/C2 are **red there** (F1).

## 2. C1 — ledger vacuity (operability)

**Before, exactly as spelled** (`count-c1.py 554ff416 --ledger
.ufo/waves/round-45/fixtures/witnesses/<w>.tsv --repo <lane>`): `ledger_present
FAIL (absent)` → `C1=unmet mismatches=? rows=0` rc 1 for all three — the ledger
is read from the measured revision's tree, so the command proves nothing about
vacuity (ExecWitnesses says the same, its §2).

**Before, fair** (unmodified r44 counter, witnesses committed at `b957dad8…`,
parent `554ff416`, `3 files changed, 36 insertions(+)`):
`w-revconst C1=met mismatches=0 rc=0`, `w-head C1=met mismatches=0 rc=0`,
`w-dup C1=met mismatches=0 rc=0`. The r44 counter also prints `C1=met` on its own
ledger at `554ff416` (rc 0; matches `evidence/control-r44-c1.txt`). **So the
before is GREEN, vacuously**: a revision-constant ledger, a HEAD-reading ledger
and a duplicate-id/duplicate-command ledger all pass.

**After** (`count-c1.py` `5f2deea0…`, `--ledger --witness-dir --other-rev`, at S2):
`revision_sensitivity PASS (5 rows move, 10 CONST)`, `witnesses_rejected PASS
(witnesses=3/3)`, `witnesses_vacuous PASS (3/3)` → `C1=met mismatches=0` rc 0.
Rejections are the *named* properties, not incidental parse noise:
`w-revconst` → `revision_sensitivity` only; `w-head` → `rows_parse` on the
tip-resolving tokens (`token 'HEAD:SKILL.md' resolves the tip instead of @REV@`,
same for the hard-coded 40-hex and `master@{u}`); `w-dup` → `rows_parse`
(`row 11: duplicate id F05 (first at row 5)`, `row 12: duplicate command text
(first at row 9)`).

## 3. C2 — registry overstatement (calibration)

**Before, as declared, on the entering-tip instrument** (v1 `743996b1…`):
`mori-gate-registry.py: error: unrecognized arguments: --audit-all`, rc 2, **no
`REGISTRY=` line** — v1's CLI is `--rev/--repo/--registry/--audit/--selftest`
only. Same result independently in `evidence/registry-audit-all.txt`.

**Before, v1's own shape** (36 declared population paths, one `--audit` each):
21 `REGISTRY=met` / 15 `REGISTRY=unmet` = 14 `unregistered: no row names` + 1
`has no --selftest mode`; and `tools/mori-silence-cases.sh PASS (… --selftest
present)` — the false positive (its only `--selftest` occurrences are comment
lines 20/290). Code cause: `parse_gate_table()` reads only the `## Gates`
section while `SKILL.md@554ff416` carries **7** eight-cell tables (headers at
162, 524, 588, 643, 718, 796, 881); the selftest test is `if b"--selftest" not
in body`; there is no population mode.

**Before, v2 at `--rev 554ff416`**: `tables=7 registered=29 unregistered=3
no_selftest=4 duplicate=0 wrong_row=0` → `REGISTRY=unmet` rc 1.

**After at worktree bytes (S2)**: auditor `tables=7 registered=39 unregistered=0
no_selftest=0 duplicate=0 wrong_row=0` → `REGISTRY=met` rc 0. The six
formerly-failing paths are attributed to the row that names them:
`row='disk write rate (r34)'`, `row='r41 calibration'`,
`row='wave settlement (r20)'`, `row='r45 ledger counter (C1)'`,
`row='r45 gate conformance (C2)'`, `row='r45 corpus coverage (C3)'`. Composite
`count-c2.py` (settled `153423c4…`) at S4: 17/17 checks PASS →
`C2=met … writescope_mismatch=0 …
auditor_selftest=pass=15/fail=0 mutant=killed` rc 0. The composite at
`554ff416`: `C2=unmet … unregistered=14 no_selftest=1 tables=unmeasured` rc 1.

**After at lane tip `18fd68b0`**: `wrong_row line=190 row='r45 ledger counter
(C1)' entry=.ufo/waves/round-45/count-c1.py absent at 18fd68b0`, and the same
for `count-c2.py`, `count-c3.py` → `REGISTRY=unmet … registered=36
unregistered=0 no_selftest=0 duplicate=0 wrong_row=3` rc 1; composite
`C2=unmet … wrong_row=3` rc 1.

## 4. C3 — assimilation (depth)

**Before** (`count-c3.py` `37fd7c24…` at `--rev 554ff416`, no `TMPDIR`):
`entry_present FAIL (absent)`, `rows_present FAIL (S473 absent)`, `readme_row
FAIL (no map row names it)`, **`census_ok PASS (exit=0)`** → `C3=unmet …
census_sha256=3fb72615…` rc 1.

**After** (required form `--entering-rev 554ff416`, no `TMPDIR`): `C3=met` rc 0
at both S2 and `18fd68b0`. Grounded bytes: `S473` = 11 cells, status `mined`,
`used-by` = `corpus/knowledge/census-cgroup-levels-r45.md`; the entry carries
`source:`, `verified-at: 2026-10-25`, `recheck: 90d`, `coverage-map: FR1, FR12`;
the README row names `knowledge/census-cgroup-levels-r45.md`. Census exit 0 both
with `env -u TMPDIR` and with a decoy `TMPDIR=<lane root>` — **no environment
override is needed**.

## 5. Findings (severity order)

**F1 — High. The landing commit makes C1 and C2 red at the only lane revision.**
`18fd68b0` carries no `.ufo/waves/round-45/` file: `git cat-file -e
18fd68b0:.ufo/waves/round-45/{figures.tsv,count-c1.py,count-c2.py,count-c3.py,
fixtures/witnesses/w-head.tsv,fixtures/write-scope.json}` all fail. So at the
lane tip the C1 after command prints `C1=unmet failed=ledger_present` rc 1 and
the C2 auditor prints `REGISTRY=unmet wrong_row=3` rc 1 (composite `C2=unmet
wrong_row=3` rc 1). The commit is also self-inconsistent: its SKILL.md rows at
lines 190–192 name `.ufo/waves/round-45/count-c{1,2,3}.py`, which are absent in
the commit — that is exactly what `wrong_row=3` catches. Until
`.ufo/waves/round-45/` is committed, `C1=met`/`C2=met` hold only on my snapshot
commit `a7af6601`, not on any lane revision. The C2 seat's own report states the
same precondition (`w1/ExecC2Counter.md` ~line 250): the working tree already
prints `C2=met` at `rev=WORK`, and the verdict must be re-required from
committed bytes — that commit has not happened.

**F2 — High. C1's verdict flips on counter bytes 27 s apart.** `count-c1.py` sha
`bbe90ce4…` (mtime 08:04:46) **rejected the round's own ledger** at snapshot S1:
`rows_parse FAIL (row 8: git grep option '--selftest' is not allowed; row 8: cut
option '-d:' is not allowed; row 8: cut option '-f2' is not allowed; row 15:
token '^rows=[0-9]+' carries '=' (option-value smuggling))` → `C1=unmet` rc 1.
The next revision `5f2deea0…` (08:05:13) accepts the same ledger → `C1=met` rc 0.
Any `C1=met` declaration must carry the counter digest next to it; a receipt
taken at 08:04 was red.

**F3 — High. C2's declared before command is unrunnable.** v1 has no
`--audit-all`, so the before is an argparse error (rc 2) with no verdict line —
not a red. The honest before is the v2 auditor at `--rev 554ff416`
(`REGISTRY=unmet` rc 1) or the v1 per-path sweep (14 unregistered + 1
no_selftest + a silence-oracle false positive).

**F4 — Medium. The composite C2 counter cannot run at the worktree tip.**
`count-c2.py WORK` aborts with an unhandled `shutil.Error` traceback — **zero
`check` lines, zero verdict lines, rc 1** — because `materialize_tree` copies
the whole worktree and trips on a sibling seat's dangling symlink
(`…/tmp/RevC1Grammar/attack-repo/.ufo/waves/round-17/fixtures/seat/
SymlinkIgnore/Dangling.jsonl`). Reproduced twice (log:
`tmp/RevBeforeAfter/c2-work-crash.txt`); at a committed rev it finishes in ~3 s.
Fix direction (not mine): `copytree(ignore_dangling_symlinks=True)` and exclude
`.ufo/waves/*/tmp`. The landing commit partly hides this (its tree excludes
scratch), but the defect remains for any WORK-mode run.

**F5 — Medium. C3's declared after command is stale, and its filed receipt is
pinned to superseded bytes.** The shipped counter requires `--entering-rev`, so
the declared form is usage rc 2 at *both* revisions; the met receipt needs the
extra flag. `evidence/control-c3.txt` pins `count-c3.py sha256 de5b625c…`; the
shipped bytes are `37fd7c24…`.

**F6 — Medium. C3's census arm is not revision-scoped.** Its stdout names the
on-disk registry (`mori ok /home/vgpnk/Projects/shokunin/mori-shokunin/
corpus/SOURCES.md`) and it passed at `--rev 554ff416` while `S473` existed only
in the worktree. Clause 3 is worded as an on-disk command, so this is
contract-conformant text — but `census_ok PASS` must not be read as evidence
about the measured revision.

**F7 — Medium (population-mode blind spot).** The auditor's `--audit-all`
enumerates the population *at the measured rev*: at `18fd68b0` the three
uncommitted instruments do not exist, so `unregistered=0` and `registered=36`
count them nowhere — they surface only via `wrong_row=3` (because the committed
SKILL.md already names them). A committed SKILL.md row naming an instrument the
commit does not carry is caught by `wrong_row`, but a population made only of
committed files silently excludes anything the wave leaves uncommitted; F1 is
the direct consequence.

**F8 — Low. The C1 "before" command as spelled is red for the wrong reason, and
`w-dup` is unstable.** Witnesses are absent from the `554ff416` tree, so the
literal command yields `C1=unmet rows=0` ×3. The vacuity shows only with the
witness committed (`b957dad8` → met ×3) or in `WORK` mode. In `WORK` mode at the
lane tip `w-dup` is red on stale values — by the time I measured, four rows had
drifted (`F01 asserted=4 observed=8`, `F02 asserted=245 observed=246`,
`F04 asserted=327 observed=330`, `F05 asserted=73 observed=75`) — not duplicates.
A copy with only those four value cells repinned prints `C1=met mismatches=0`
rc 0 while the duplicate id `F05` and the duplicated command remain
(`tmp/RevBeforeAfter/w-dup-repinned.tsv`, re-measured at snapshot `e264ce36`).

**F9 — Observation (transient, not a shipped defect).** `count-c2.py --selftest`
and `count-c3.py --selftest` were red while being written (`pass=1 fail=7`
`NameError: name '_token' is not defined`; `pass=2 fail=14` `TypeError:
evaluate() missing 1 required positional argument: 'timeout'`) and green on the
settled bytes (`pass=10 fail=0`, `pass=19 fail=0`). Recorded because a receipt
taken minutes earlier would have been red.

## 6. Residual risk and verification gaps

- C1's `C1=met` is demonstrated only at snapshot `a7af6601` (worktree bytes);
  once `.ufo/waves/round-45/` is committed it must be re-measured at the new tip
  — including a check that F01/F02/F03/F05/F08's moved values hold there
  (`corpus/lessons/round-45.md` is in `18fd68b0` at 214 lines, so F02's 75 is
  already consistent).
- C2's green depends on the counters being committed; today the committed
  registry names them but they are absent (F1/F7).
- C3's census arm remains an on-disk statement, never a revision-scoped pass
  (F6).
- I did not re-review the write-scope fixture's entries beyond
  `writescope_entries PASS (checked=4 skipped=3)` / `writescope_mismatch=0`
  (ExecWriteScopeFixture/RevAudit scope), nor the entry's quote fidelity
  (RevEntryQuotes scope).
- The snapshot tree excludes non-`.md` corpus files and seat scratch, so it is
  not byte-identical to the worktree; the 15-row ledger reconciles at it, which
  is what would expose a missing input.

Tooling: nothing installed or upgraded; no pacman transaction; lane git
read-only; scratch under `TMPDIR=.ufo/waves/round-45/tmp/RevBeforeAfter`.
