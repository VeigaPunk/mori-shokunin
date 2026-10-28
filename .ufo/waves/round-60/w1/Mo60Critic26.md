# Mo60Critic26 — absent-set lie attack on `count-c1.py`

Seat: critic (leaf). Assignment: would a **flipped disposition cell** or a **wrong
at-data cell** in `.ufo/waves/round-60/evidence/r59-absent-set.md` be caught by
`count-c1.py` against real git truth? Drive `parse_absent_table` + `measure()` on
tampered table copies in scratch and report exactly which lies are caught.

Pins used for every claim below: freeze `ac496c7cde8cad965079858accae3bedfe4a73f2`,
entering `ddfb12fb0838b4307c445194a844f0c4b1950195`, measured revision
**R = `b3c256138f00c704d5aa56eb0332d74506502ef2`** (lane tip when read; carrying the
C1 data commit `398d3225`). Nothing here reads an unpinned working-tree blob.

---

## 1. Instrument identity — kill rule does not fire

```
$ for f in .ufo/waves/round-60/count-c1.py .ufo/waves/round-60/contract.md; do
    git show <rev>:$f | sha256sum; done      # rev = ac496c7c and b3c25613
795c1f31…ddbae  count-c1.py    (identical at both revs)
a444e270…5441d  contract.md    (identical at both revs)
$ git diff --stat ac496c7c..b3c25613 -- .ufo/waves/round-60/count-c{1,2,3}.py \
      .ufo/waves/round-60/contract.md .ufo/waves/round-60/build-fixtures-r60.py \
      tools/mori-entry-claims-check.py
(empty)
```

`count-c1.py` sha matches the contract's C3 pin `795c1f31…ddbae`. Counter bytes,
contract bytes, predicate sentence and target output are unchanged since freeze, so
the C1 kill rule cannot fire on byte drift.

## 2. Method (read-only on the lane)

Sandbox clone only; no fixture repo, no lane writes:

```
S=/fast/scratch/hyaku/mori-r60/Mo60Critic26
git clone -q --shared <lane> $S/clone        # HEAD = b3c25613
git -C $S/clone rev-parse --show-toplevel    # -> /fast/scratch/.../Mo60Critic26/clone
python3 <lane>/.ufo/waves/round-60/count-c1.py <rev> --repo $S/clone \
        --scratch $S/run-<tag>               # TMPDIR=$S
```

Each variant = one commit in the clone that rewrites only
`.ufo/waves/round-60/evidence/r59-absent-set.md` (or
`corpus/lessons/round-60.md` for the lesson arm), then a counter run at that commit.
Working tree of the lane was never written; `git status` in the lane shows only other
seats' artifacts (untracked wave receipts plus one in-flight lesson edit; see §6/§8).

Baseline, control and selftest:

```
clone @ b3c25613 : C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=b3c25613…   rc=0
lane  @ b3c25613 : C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=b3c25613…   rc=0
count-c1.py --selftest : C1_SELFTEST pass=6 fail=0                                                rc=0
@ ddfb12fb (clone)     : C1=unmet dead-uncorrected=2 receipts=0/2 absent-set=0/5 lesson=absent      rc=1
                         failed=absent_set=0/5,absent_table_absent,correction_incomplete,dead=2,
                         lesson_absent,receipt_absent:…r59-c1-met.txt,receipt_absent:…r59-c2-met.txt,receipts=0/2
```

The lane/clone baseline line is byte-equal to committed
`evidence/c1-at-data.txt`; the entering-revision line is byte-equal to committed
`evidence/control-c1-do-nothing.txt`.

## 3. Direct answer

Both named lies are caught **when they sit in the operative row**:

| lie (single, operative row) | counter output | verdict |
|---|---|---|
| disposition `late-committed` → `wrong-superseded` (Mo59Executor40) | `C1=unmet … absent-set=4/5 … failed=absent_row:Mo59Executor40,absent_set=4/5` rc=1 | **caught** |
| wrong at-data cell `absent` → `present` (truth at `7b86704d` is absent) | `C1=unmet … absent-set=4/5 … failed=absent_row:Mo59Executor40,absent_set=4/5` rc=1 | **caught** |
| wrong at-R cell `present` → `absent` (truth at R is present) | `C1=unmet … absent-set=4/5 … failed=absent_row:Mo59Executor40,absent_set=4/5` rc=1 | **caught** |

Mechanism: the table is read with `git_show(repo, rev, ABSENT_TABLE)`
(`count-c1.py:180`) — committed bytes only, so an uncommitted working-tree lie is
invisible (probe v21: dirty worktree row appended, `C1=met` unchanged) — and each
checked cell is compared against `git cat-file -e` truth at `R59_DATA`/R
(`count-c1.py:194-205`). The disposition is *derived*, not read: `want_disp =
"late-committed" if not truth_data else "wrong-superseded"` (`:202-204`), so a flip
is always a lie at this data slice (all five names are absent at `7b86704d`).

**But the check is per-name-last-wins, not per-row.** `parse_absent_table` stores
`rows[cells[0]] = (cells[1], cells[2], cells[3])` (`count-c1.py:117`), so a second
5-cell row for the same name silently replaces the first. A false row earlier in the
file therefore survives scoring:

| probe (committed table bytes) | counter output | verdict |
|---|---|---|
| v18 lie row first (`present \| present \| wrong-superseded`), true row appended last | `C1=met … absent-set=5/5` rc=0 | **not caught** |
| v19 same shape, disposition flip on Mo59Critic29 | `C1=met … absent-set=5/5` rc=0 | **not caught** |
| v22 same shape, at-R flip on Mo59MutationTester32 | `C1=met … absent-set=5/5` rc=0 | **not caught** |
| v20 control: the *same* at-data lie with no duplicate row | `C1=unmet … failed=absent_row:Mo59Executor40` rc=1 | caught |
| v05 duplicate lie placed **last** | `C1=unmet … failed=absent_row:Mo59Critic29` rc=1 | caught (last wins both ways) |

Direct parse probe on the v18 shape: `masked table -> parsed rows: 5 exec40:
('absent','present','late-committed')` with `data rows in masked file: 6`. The file
contradicts the contract's "**one** 5-cell row per frozen name" and one of its rows
disagrees with git truth, yet the frozen target line is emitted.

## 4. Full variant matrix (exact outputs, all under `$S/clone`)

| # | tamper (committed) | rc | counter verdict |
|---|---|---|---|
| v01 | disposition flip, Mo59Executor40 | 1 | `unmet … absent_row:Mo59Executor40,absent_set=4/5` |
| v02 | at-data flip, Mo59Executor40 | 1 | `unmet … absent_row:Mo59Executor40,absent_set=4/5` |
| v03 | at-R flip, Mo59Executor40 | 1 | `unmet … absent_row:Mo59Executor40,absent_set=4/5` |
| v04 | 5th cell (landing pointer) → `deadbeef` | 0 | `met … absent-set=5/5` |
| v05 | duplicate row, lie last | 1 | `unmet … absent_row:Mo59Critic29` |
| v06 | lie first + appended **4-cell** truth row | 1 | `unmet … absent_row:Mo59Critic29` (truncated row silently skipped) |
| v07 | duplicate identical row | 0 | `met` (multiplicity not rejected) |
| v08 | 6-cell row carrying a lie | 0 | `met` (row skipped: `len(cells) != 5`) |
| v09 | extra row for non-frozen `Mo59Ghost99` | 0 | `met` (name not in `NAMES`) |
| v10 | delete Mo59MutationTester31 row | 1 | `unmet … absent_row_missing:Mo59MutationTester31` |
| v11 | disposition value `maybe` | 1 | `unmet … absent_table_shape,absent-set=0/5` |
| v12 | value `Absent` (case) | 1 | `unmet … absent_table_shape,absent-set=0/5` |
| v13 | name cell `Mo59Executor40 (dup)` | 1 | `unmet … absent_row_missing:Mo59Executor40` |
| v14 | lying row inside a fenced code block, last | 1 | `unmet … absent_row:Mo59Critic29` (fenced rows are parsed) |
| v15 | at-data/at-R swapped together | 1 | `unmet … absent_row:Mo59MutationTester32` |
| v18/v19/v22 | duplicate-shadowed at-data / disposition / at-R lie | 0 | `met` |
| v20 | same at-data lie, single row | 1 | `unmet … absent_row:Mo59Executor40` |
| v21 | uncommitted working-tree lie | 0 | `met` (rev-pinned read; correct) |
| v16 | `f091bd77` → `unknown-rev` on the Mo59Executor40 lesson line | 0 | `met … lesson=ok` |
| v17 | names and pointer split onto unrelated lines | 0 | `met … lesson=ok` |
| v23 | every name-bound `f091bd77` stripped, one global mention kept | 0 | `met … lesson=ok` |
| v24 | no `f091bd77` anywhere | 1 | `unmet … lesson=bad`, `failed=lesson:<all 5>` |
| v25 | Mo59Critic29 / Mo59Reviewer16 lines removed | 1 | `unmet … lesson=bad`, `failed=lesson:Mo59Critic29,lesson:Mo59Reviewer16` |
| v26 | all names on one bare line with the pointer | 0 | `met … lesson=ok` |

## 5. Cells and classes the frozen counter does not cover

1. **Duplicate rows** (`:117`) — last row wins; 6 data rows parse as 5. The counter
   never asserts `1` row per frozen name, so a published false 5-cell row can coexist
   with `C1=met` (v18/v19/v22).
2. **The 5th cell ("landing pointer")** — dropped at `:117`; the selftest asserts the
   3-tuple (`count-c1.py:270`). v04 (`deadbeef`) scores met. This is *inside the
   contract's wording* ("one 5-cell row") but *outside the frozen predicate sentence*,
   which binds only the at-data, at-R and disposition cells — i.e. not a counter bug,
   a scope gap in what the claim certifies.
3. **Row shape** — any row with `len(cells) != 5` is skipped (`:108`); rows whose first
   cell does not start with `Mo` are skipped (`:110`). v08/v09 show lying rows of both
   kinds pass untouched. No "extra row" rejection exists.
4. **Location** — any 5-cell line anywhere in the file participates, including fenced
   examples (v14). Over-strict direction: a documentation example row can flip a true
   claim to `unmet`. There is no section/table scoping.
5. **Lesson arm binding** (`:221-230`) — name presence is per-name, pointer is a
   whole-file substring: `(name in lt) and (R59_LANDING[:8] in lt)`. v23 strips every
   name-bound pointer and passes; v26 puts all names on one bare line and passes; v24
   (no token anywhere) and v25 (names gone) fail. So "naming every late-committed name
   **with** landing pointer `f091bd77`" is enforced only as "the file contains the name
   and, somewhere, the token".

## 6. Contract-literal defect the shipped bytes already expose

Truth re-derived independently in the lane (`git cat-file -e <rev>:.ufo/waves/round-59/w1/<name>.md`):

```
Mo59Executor40       7b86704d absent   b3c25613 present
Mo59MutationTester31 7b86704d absent   b3c25613 present
Mo59MutationTester32 7b86704d absent   b3c25613 present
Mo59Critic29         7b86704d absent   b3c25613 present
Mo59Reviewer16       7b86704d absent   b3c25613 present
```

All five are consequently `late-committed` under `:202`, so the contract's lesson rule
("every late-committed name with landing pointer `f091bd77`") applies to all five.
The shipped `corpus/lessons/round-60.md` at R does not do that for two of them:

```
 50: - Mo59Critic29 — supersedes the round-59 lesson claim of absent-at-filing:
 51:   committed pre-filing in `bf6c0ad3` (2026-10-28 03:12:38 -03); …
 53: - Mo59Reviewer16 — supersedes the round-59 lesson claim of absent-at-filing:
 54:   committed pre-filing in `bf6c0ad3`.
```

`f091bd77` occurs only on lines 55-56 (Mo59MutationTester32), 58, 59 and in prose at
60/75. The counter reports `lesson=ok` because of the global substring test (§5.5, v23
proves it cannot distinguish). The table itself says the same thing: its 5th-cell
landing pointers for Mo59Critic29/Mo59Reviewer16 are `bf6c0ad3` (`r59-absent-set.md`
lines 14-15 at R). **The delivered record is more truthful than the frozen sentence —
the sentence over-specifies; the counter under-checks.** That is a predicate-formation
defect, not data dishonesty, and it is not a post-freeze change (kill rule silent).

**Time-bound note (13:19, not scored here).** While this seat ran, another seat's
in-flight *working-tree* edit to the lesson (13 insertions / 3 deletions; tip still
`b3c25613`, so uncommitted and unscorable) added `` `f091bd77` `` to the Mo59Critic29
and Mo59Reviewer16 lines plus a "Reading note (fixed here so both readings of the
frozen C1 sentence hold on the same bytes)". If that edit is committed, the literal
per-name reading above is satisfied at the new revision and C1 must be re-scored there
(`count-c1.py <new-R>`, which reads committed bytes — `count-c1.py:214`); at R this
paragraph stands as written.

## 7. Verdict for the canonical judge

- **C1=met at R is not falsified by this seat.** The shipped table has exactly one row
  per frozen name at R, and all three checked cells per row agree with `git cat-file -e`
  truth at `7b86704d` and R (independently re-verified above). Receipts re-run 2/2,
  lesson present with all five names plus `supersedes round-59`, target line exact,
  instrument bytes unchanged since freeze.
- **The absent-set arm is lie-resistant to a single-cell tamper of the operative row**
  (3/3 caught: disposition, at-data, at-R; plus deleted row, mangled name, swapped
  columns, and out-of-vocabulary cells all fail closed).
- **It is not lie-resistant to duplicate-row shadowing**, and it certifies a table whose
  published 5th cell it never reads. On its own that would let a
  predicate-violating table (`6` data rows for `5` names, one row false) score `met`.
- **Smallest safe correction** (round-61 hardening; counter bytes are frozen this round
  and no round-60 action is implied): (1) in `parse_absent_table`, count accepted rows
  per name and emit `absent_table_duplicate:<name>` when `count != 1`; (2) either bind
  `cells[4]` to the contract's landing pointers or drop the column from the artifact;
  (3) make the lesson check per-name-bound (`- <name> …<pointer>` within one record) or
  restate the sentence as the file-level token test it actually is, and let the
  `f091bd77` clause admit `bf6c0ad3` for the two pre-filing names.

## 8. Incidental observation (detection only — not my artifact, not removed)

`/home/vgpnk/Projects/shokunin/mori-shokunin/EXEC-MARKER` appeared untracked in the lane
worktree (`git status --porcelain` → `?? EXEC-MARKER`) between my 13:16 and 13:18 reads;
it was absent again at 13:19 (removed by someone else — not me). Observed at 92 bytes,
mtime `2026-10-28 13:16:28 -03`, content:

```
executed /fast/scratch/hyaku/mori-r60/Mo60Executor58/full-old/real2/round-53/w1-results.json
```

It appeared between my first lane `git status` and my later one and post-dates my runs;
the path names another seat's scratch. [INFERENCE] it is the r59-counter hole marker
(`.ufo/waves/round-60/count-c3.py:69-70` writes exactly `"executed " + " ".join(argv[:3])`)
produced by an old-counter control run whose cwd was the lane root, i.e. a marker
written **outside** the seat's scratch root. Observed bytes/mtime are fact; authorship is
inference. It was never committed (`git log --all --oneline -- EXEC-MARKER` → empty at
13:20); flagged for the L1 and the C3/G2 seats — I did not create, modify or delete it.

Also at 13:19 the lane worktree shows `M corpus/lessons/round-60.md` (another seat's
in-flight edit, §6); tip is unchanged at `b3c25613`, and all C1 numbers in this report
are pinned to committed bytes at that revision.

## 9. Cleanup

- No tools installed or updated; `pacman` untouched (host-wide pause honored); nothing
  needed beyond the preinstalled `python3`/`git`.
- All git writes confined to `/fast/scratch/hyaku/mori-r60/Mo60Critic26/clone`; the lane
  received no commit, no index change, no file write.
- Scratch tree removed after extracting the receipts above:
  `rm -rf /fast/scratch/hyaku/mori-r60/Mo60Critic26`.
