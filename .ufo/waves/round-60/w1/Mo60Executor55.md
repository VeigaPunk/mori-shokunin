# Mo60Executor55 — absent-set truth matrix (C1 ABSENT-SET ARM)

Scope: the five frozen names
{Mo59Executor40, Mo59MutationTester31, Mo59MutationTester32, Mo59Critic29,
Mo59Reviewer16} at path `.ufo/waves/round-59/w1/<name>.md`, probed with
`git cat-file -e` at the two frozen revisions and at the lane tip. Read-only:
no commits, no worktree/index writes, no production/corpus/SCORECARD/LOG edits.

## Pinned revisions (everything below is bound to these)

| role | revision | committer date (iso-local) | note |
|---|---|---|---|
| data rev (frozen) | `7b86704d7c0754a09958d131b64dbfa2a6d3eaed` | 2026-10-28 03:00:51 -0300 | `round-59: data correction — K11 demoted to prose` |
| landing rev (frozen) | `f091bd773c4cfec8877061c84f4bae5f11e8bbe5` | 2026-10-28 07:42:42 -0300 | `round-59: w1-results.json (64/64 settled) + 3 late seat reports` |
| lane tip R (measured) | `b3c256138f00c704d5aa56eb0332d74506502ef2` | 2026-10-28 12:59:33 -0300 | tree `af1f1a86b342bfc1af3005c5a41a54111b46a238` |
| round-59 filing commit | `bf6c0ad3acbd60f7561d12d2663d12f9243562ef` | 2026-10-28 03:12:38 -0300 | `round-59: integrate w1 — … lesson+LOG+SCORECARD+…+62 seat reports` |
| round-60 entering rev | `ddfb12fb0838b4307c445194a844f0c4b1950195` | 2026-10-28 07:48:31 -0300 | `round-59 verifier spot-check` (adds the r59 lesson file) |

Ancestry verified: `7b86704d → bf6c0ad3 → f091bd77 → ddfb12fb → … → b3c25613`
(`git merge-base --is-ancestor`, all true). Tip may move; every read below is
pinned, none is a working-tree read.

## 5×3 truth matrix (rc per cell)

Command shape, run once per cell:

```
git -C /home/vgpnk/Projects/shokunin/mori-shokunin \
    cat-file -e <rev>:.ufo/waves/round-59/w1/<name>.md
```

| name | @7b86704d (data rev) | @f091bd77 (landing rev) | @b3c25613 (tip R) |
|---|---|---|---|
| Mo59Executor40 | **absent** rc=128 | **present** rc=0 | **present** rc=0 |
| Mo59MutationTester31 | **absent** rc=128 | **present** rc=0 | **present** rc=0 |
| Mo59MutationTester32 | **absent** rc=128 | **present** rc=0 | **present** rc=0 |
| Mo59Critic29 | **absent** rc=128 | **present** rc=0 | **present** rc=0 |
| Mo59Reviewer16 | **absent** rc=128 | **present** rc=0 | **present** rc=0 |

Absent cells' stderr is the path-not-in-rev form, i.e. truth is "file absent at
that revision", not "bad revision":

```
fatal: path '.ufo/waves/round-59/w1/Mo59Executor40.md' exists on disk, but not in '7b86704d7c0754a09958d131b64dbfa2a6d3eaed'
```

### Supplementary revision evidence (what actually discriminates)

| name | @bf6c0ad3 rc | blob@bf6c0ad3 | blob@f091bd77 | blob@tip | add commit | last-modify commit |
|---|---|---|---|---|---|---|
| Mo59Executor40 | 128 | — | `fe216c4db3` | `fe216c4db3` | `f091bd77` 07:42:42 | `f091bd77` |
| Mo59MutationTester31 | 128 | — | `f6a32a90e7` | `f6a32a90e7` | `f091bd77` 07:42:42 | `f091bd77` |
| Mo59MutationTester32 | 0 | `00e1208afd` | `1fc46af241` | `1fc46af241` | `bf6c0ad3` 03:12:38 | `f091bd77` |
| Mo59Critic29 | 0 | `3f49b8f081` | `3f49b8f081` | `3f49b8f081` | `bf6c0ad3` 03:12:38 | `bf6c0ad3` |
| Mo59Reviewer16 | 0 | `97a905715b` | `97a905715b` | `97a905715b` | `bf6c0ad3` 03:12:38 | `bf6c0ad3` |

`f091bd77 → tip` blobs are byte-identical for all five (`rev-parse --verify`;
`cat-file -s` 27592 / 7373 / 9850 / 10712 / 10742 bytes). All five are also
present at `ddfb12fb` (rc=0), as is `w1-results.json`.

`.ufo/waves/round-59/w1/` entry counts: `7b86704d` → **0** (the whole tree is
absent; `cat-file -e 7b86704d:.ufo/waves/round-59/w1` → rc 128), `bf6c0ad3` →
63, `f091bd77` → 65, `ddfb12fb` → 65, tip → 65.

## Cross-check against the committed evidence table

Blob read pinned at R:
`git show b3c25613:.ufo/waves/round-60/evidence/r59-absent-set.md`
sha256 `0f881eb9bd872e70dccc0f1343a98057b22cada7b80dbeb375f69af0e6650b24`
(equal to the worktree copy at the time of measurement — no unpinned read used).

Parsed rows: exactly 5, no duplicate names, 5 cells each. Cells 2–4
(`at 7b86704d`, `at r60 tip`, `disposition`) checked against the matrix above
and against the frozen grammar `late-committed` iff absent at `7b86704d`:

| name | cell at-data | truth | cell at-R | truth | cell disposition | required | verdict |
|---|---|---|---|---|---|---|---|
| Mo59Executor40 | absent | absent | present | present | late-committed | late-committed | AGREE |
| Mo59MutationTester31 | absent | absent | present | present | late-committed | late-committed | AGREE |
| Mo59MutationTester32 | absent | absent | present | present | late-committed | late-committed | AGREE |
| Mo59Critic29 | absent | absent | present | present | late-committed | late-committed | AGREE |
| Mo59Reviewer16 | absent | absent | present | present | late-committed | late-committed | AGREE |

**15/15 predicate-relevant cells agree.**

Independent replay of the frozen counter at the pinned tip (read-only, scratch
confined, `TMPDIR` redirected):

```
$ python3 .ufo/waves/round-60/count-c1.py b3c25613… --repo <lane> --scratch <scratch>/c1tip
C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=b3c256138f00c704d5aa56eb0332d74506502ef2
rc=0
```

## Findings

**F1 — the frozen data revision predates the entire w1 tree, so the matrix's
`absent` column is non-discriminating.** `7b86704d` has zero entries under
`.ufo/waves/round-59/w1/` (the directory itself is not in that tree), so *every*
r59 seat report is "absent" at the data revision. The uniform
`late-committed` disposition is therefore entailed by the revision choice, not
by per-name evidence; it carries no information distinguishing the five names
from the other 60 reports. The claim "reconciled with the tree" is true, but the
discriminating evidence lives only in the supplementary `bf6c0ad3` column and in
the landing-pointer cells.

**F2 — the r59 lesson's absent-at-filing set was a 2-name false positive, and
the r60 correction says so correctly.** `corpus/lessons/round-59-verifier-spotcheck.md`
lines 99–101 state: `report says missing = {Executor40, MutationTester31,
MutationTester32}; lesson's "absent at filing" set adds {Critic29, Reviewer16}
which are committed`. Truth: `Mo59Critic29` and `Mo59Reviewer16` have existed
continuously since `bf6c0ad3` (03:12:38), i.e. before every observation
timestamp the lesson itself quotes (03:13 / 03:17 / 07:42 at lines 18–19), and
their bytes at `bf6c0ad3` are identical to tip. The r59 lesson was wrong about
those two; the r60 correction (`corpus/lessons/round-60.md` lines 50 and 53,
phrased with `supersedes`) matches git. Genuinely late were `Mo59Executor40` and
`Mo59MutationTester31` (until `f091bd77`, 07:42:42).

**F3 — `Mo59MutationTester32` is present-at-filing but dirty, and the table's
landing-pointer cell is blob-exact.** Added at `bf6c0ad3` (`00e1208a`), modified
at `f091bd77` (`1fc46af2`), unchanged to tip. The table cell "added `bf6c0ad3`
(03:12:38, pre-filing), modified `f091bd77`" (line 13) is exactly right,
including both commit identities.

**F4 — "pre-filing" in rows 13–15 contradicts the same file's line 20, which is
the accurate wording.** Lines 20–21 read `Critic29/Reviewer16 were committed at
filing time in bf6c0ad3`. Git agrees with line 20: those files are *in* the
`bf6c0ad3` tree, i.e. at the round-59 closure commit, not before it. The word
"pre-filing" in the cells overstates by one commit boundary and is internally
inconsistent with the file's own footer. Documentation imprecision only — the
commit identities themselves are correct, and the fifth cell is free text that
the frozen counter never validates: `parse_absent_table` keeps
`(cells[1], cells[2], cells[3])` only (`count-c1.py:110-118`, returned tuple at
line 125), so the landing-pointer column is shape-checked (5 cells) but never
compared to git.

**F5 — the lesson's per-name landing binding is file-global, not per line.**
`count-c1.py:228` tests `name in lt and R59_LANDING[:8] in lt` — a substring
test over the whole lesson text. Per-name lines:
line 50 Critic29 — no `f091bd77`; line 53 Reviewer16 — no `f091bd77`; line 55
MT32 — no `f091bd77`; line 58 Executor40 — `f091bd77` present; line 59 MT31 —
`f091bd77` present. Under a literal per-name reading of the frozen contract
("naming every late-committed name with landing pointer `f091bd77`") only 2 of 5
rows satisfy it, while the instrument prints `lesson=ok`. Note this is not
fixable by editing: for Critic29/Reviewer16 the true landing pointer is
`bf6c0ad3`, so naming `f091bd77` on those rows would assert something false. The
frozen predicate and the tree are jointly unsatisfiable under the per-name
reading; `C1=met` therefore rests on the file-global binder. Recorded as an
observation for the L1, not a re-scoring.

**F6 — in-flight sibling artifact observed.** `git status --porcelain` on the
lane showed one untracked path during measurement:
`?? .ufo/waves/round-60/evidence/c1-at-data.txt` (not mine, untouched). Evidence
reads below were pinned to `b3c25613` for exactly this reason; a later
re-derivation must pin its own R rather than trust the worktree.

## Method / reproduction

```
L=/home/vgpnk/Projects/shokunin/mori-shokunin
TIP=$(git -C "$L" rev-parse HEAD)              # b3c256138f00c704d5aa56eb0332d74506502ef2
for r in 7b86704d7c0754a09958d131b64dbfa2a6d3eaed \
         f091bd773c4cfec8877061c84f4bae5f11e8bbe5 "$TIP"; do
  for n in Mo59Executor40 Mo59MutationTester31 Mo59MutationTester32 Mo59Critic29 Mo59Reviewer16; do
    git -C "$L" cat-file -e "$r:.ufo/waves/round-59/w1/$n.md"; echo "$r $n rc=$?"
  done
done
```

All git invocations were read-only (`cat-file`, `ls-tree`, `rev-parse`,
`show`, `log`, `merge-base`, `status`); no VCS mutation, no fixture, no clone.
Scratch `/fast/scratch/hyaku/mori-r60/Mo60Executor55` was created with
`mkdir -p`, used with `TMPDIR` set, and removed after the receipts above were
copied in. Disk guard was green before work (`/fast/scratch/hyaku` 26% used,
600.0G free). No tools installed or updated.

## Limits

- Verdict scope is the three pinned revisions plus the two supplementary ones;
  the lane tip moved twice during the round (`7b86704d` data → `bf6c0ad3` →
  `f091bd77` → tip), so the tip cell is only valid for `b3c25613`.
- `count-c1.py --selftest`, receipts re-runs, and the C2/C3 arms belong to other
  seats; only the single C1 replay above was executed here.
- Truth is `git cat-file -e` existence at a revision. This matrix says nothing
  about whether the *contents* of those five reports are correct — only that
  they exist where and when the table claims.
