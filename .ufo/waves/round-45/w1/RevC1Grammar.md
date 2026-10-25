# RevC1Grammar — attack on the C1 instrument (round 45, wave 1)

Instrument under test:

    f80e75ac7421e6de00b22b38614a5f069242697140c46552d4b5e6cf0323ef61  .ufo/waves/round-45/count-c1.py
    9b339d84cbdb519eec23db21b19ecfa8e77c893a8b1f4d71cdc074d61c6d3a52  .ufo/waves/round-45/fixtures/mutants/count-c1.py

Contract read: `.ufo/waves/round-45/contract.md` §P-C1 (frozen predicates, floors
12/4, kill rules). Revisions used:

    554ff416459c92f0dea9762f834a556df2990187   entering tip (--other-rev)
    3ad8faaa637ae466c61f9427fea1c208bf49ea82   round-45 freeze
    4e5050378de6a7b7145925b3fae0daf8b6c1f50c   fixture commit 1 (attack ledgers)
    397878bc0142e9bb4bbe5bf689d6c6495992d99d   fixture commit 2 (CONST fixtures)
    93cbf32e2cc140c84e85256c9379e4f19609a40f   fixture commit 3 (absent-show fixture)

## Verdict

**The counter does not reject every attempt.** It rejects the frozen witness
classes and every floor/dedup/shell-metacharacter attempt, but seven shapes reach
`C1=met` with `rc=0`. Two let a committed ledger row **execute a program** and
**write an arbitrary file**; three rest on the unconditional `CONST=` escape
(including one that survives the mid-wave Correction 1); one shows the witness
arm is satisfied by a single malformed file; one admits a short-SHA tip pin.

The counter bytes under test did not change during the review
(`sha256 f80e75ac…`, re-checked after every run), but **the contract did**: a
seat appended `## Correction 1` mid-wave. I tested the predicate I read at the
start (frozen `3ad8faaa` bytes) and map every finding onto the correction below
(§Predicate drift). The counter implements neither `moved>=1` nor
`const<=rows-1`, so both versions are needed to read the receipts.

## Harness (a clone, but real commits and the lane's real bytes)

P-C1 reads the ledger at the measured revision (`git show <rev>:<path>`), and my
lane git is read-only, so the attack ledgers were committed into a `--shared`
clone of this lane under my scratch dir (real object store via alternates, real
commits):

    TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/tmp/RevC1Grammar
    git clone --shared --quiet /home/vgpnk/Projects/shokunin/mori-shokunin $TMPDIR/attack-repo
    # ledgers committed at atk/<name>.tsv in that clone; lane git never mutated.

Every run below is:

    python3 .ufo/waves/round-45/count-c1.py <rev> --other-rev 554ff416 \
      --repo $TMPDIR/attack-repo --ledger atk/<name>.tsv \
      --witness-dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/fixtures/witnesses

No tools were installed or upgraded for this item.

### Control: an honest ledger does reach met

    check rows_parse             PASS (12 rows)
    check commands_reconcile     PASS (all rows match)
    check revision_sensitivity   PASS (12 rows move, 0 CONST)
    check witnesses_rejected     PASS (witnesses=3/3)
    C1=met mismatches=0 rows=12 classes=checks,corpus,evidence,registry,wave floor_rows=12 floor_classes=4 rev=4e5050378de6a7b7145925b3fae0daf8b6c1f50c repo=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/tmp/RevC1Grammar/attack-repo other_rev=554ff416459c92f0dea9762f834a556df2990187 witnesses=3/3
    rc=0

(An *honest* row cannot cite a round-45-only path here: absent at `--other-rev`,
the other-rev run exits non-zero and is scored `unreadable at other-rev` —
correct, and stricter than P-C1's text.)

## Attempt matrix

| # | attack | verdict | rc | rejected? |
|---|--------|---------|----|-----------|
| 1 | 12 revision-constant rows, no `CONST=` | `C1=unmet … failed=revision_sensitivity` | 1 | yes |
| 2a | `git show HEAD:<path> \| grep -c '…'` | `C1=unmet … failed=rows_parse,revision_sensitivity` | 1 | yes |
| 2b | hard-coded 40-hex revision operand | `C1=unmet … failed=rows_parse,revision_sensitivity` | 1 | yes |
| 2c | `@` resolves the tip (`git log --format=%s @ @REV@ \| wc -l`) | `C1=unmet … failed=revision_sensitivity` | 1 | yes |
| 2d | **short SHA of the tip** (`3ad8faa`) | **`C1=met`** | **0** | **NO** |
| 3a | duplicate id `F05` | `C1=unmet … failed=rows_parse,revision_sensitivity` | 1 | yes |
| 3b | duplicate command text | `C1=unmet … failed=rows_parse,revision_sensitivity` | 1 | yes |
| 4 | 5 rows, `--min-rows 1 --min-classes 1` | `C1=unmet … floor_rows=12 … failed=row_floor` | 1 | yes |
| 4b | 5 rows, `--min-rows -5 --min-classes 0` | `C1=unmet … floor_rows=12 … failed=row_floor` | 1 | yes |
| 5a | absent path via `git show … \| wc -l`, `CONST=` | `C1=unmet … failed=commands_reconcile` | 1 | yes |
| 5b | **absent path via `ls-tree` pathspec**, `CONST=` | **`C1=met`** | **0** | **NO** |
| 6a | `; true` appended | `C1=unmet … shell metacharacter ';'` | 1 | yes |
| 6b | `&& true` appended | `C1=unmet … shell metacharacter '&'` | 1 | yes |
| 6c | `$(touch …)` | `C1=unmet … shell metacharacter '$','(',')'` | 1 | yes |
| 6d | backtick `touch …` | ``C1=unmet … shell metacharacter '`'`` | 1 | yes |
| 6e | `\| tee <file>` | `C1=unmet … stage 'tee' is not a read filter` | 1 | yes |
| 6f | **`\| sort -o <abs path> \| wc -l`**, `CONST=` | **`C1=met`**, file written | **0** | **NO** |
| 6g | **`\| sort -S 1K --compress-program=<script> \| wc -l`** | **`C1=met`**, script executed | **0** | **NO** |
| 7 | witness dir = 3 vacuous + 1 honest | `C1=unmet … witnesses=3/4` | 1 | yes |
| 7b | **witness dir = one 3-line malformed file** | **`C1=met … witnesses=1/1`** | **0** | **NO** (weak oracle) |
| — | **all 12 rows carry `CONST=<free text>`** | **`C1=met … (0 rows move, 12 CONST)`** | **0** | **NO** |
| — | **11 CONST rows + 1 moving row** | **`C1=met … (1 rows move, 11 CONST)`** | **0** | **NO** (also under Correction 1) |
| — | `--other-rev` omitted | `C1=unmet … failed=other_rev_present,revision_sensitivity` | 1 | yes |
| — | `WORK` as measured revision | `C1_SETUP WORK is not a scoring revision…` | 2 | yes |
| — | unresolvable revision `deadbeef` | `C1_SETUP cannot resolve revision 'deadbeef' in …` | 2 | yes |
| — | `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` poisoned | `C1=met` (child env scrubbed) | 0 | n/a |

Rows below are quoted with `<TAB>` between cells (the file has real tabs).

## Predicate drift during the wave

The contract was edited while this review ran. Digests:

    0726926c14d3360361333fa2bbfa74412e08ad5e461bb0dff3d62800dd585af2  contract.md at 3ad8faaa (and in the worktree when I began)
    40010eeed46d649586c597f1997809979178e155493f21d3f485e131fb09d939  contract.md in the worktree at review end

The appended `## Correction 1` (28 lines, by another seat — quoted, not judged
here) adds to C1: `moved>=1`, non-empty `CONST=` reasons, `const<=rows-1`, and a
non-empty `--witness-dir`. The counter under test implements **none** of those
thresholds: with all twelve rows annotated it still prints
`check revision_sensitivity PASS (0 rows move, 12 CONST)` and `C1=met` (rc 0),
which the correction forbids — so as landed, instrument and corrected predicate
disagree. Disposition of my findings against the corrected text:

| finding | under Correction 1 | evidence |
|---|---|---|
| S1 writer/exec (`sort -o`, `--compress-program`) | **survives** (about row execution, not counting) | `C1=met`, `CANARY_COMPRESS`/`CANARY_SORT` created |
| S2 all-12-`CONST` | closed by `moved>=1` + `const<=rows-1` | `0 rows move, 12 CONST` → `C1=met` today |
| S2′ 11-`CONST` + 1 moving | **survives** (`moved=1`, `const=11<=11`) | receipt in S2 below |
| S3 junk-only witness dir | **survives** (`--witness-dir` non-empty; one junk file qualifies) | `witnesses=1/1`, `C1=met` |
| S4 short-SHA tip pin | **survives** (40-hex litmus untouched) | `C1=met`, `rows_parse PASS` |
| S5 absent path scored 0 | **survives** (one `CONST=` row is allowed) | `C1=met`, `F12 value=0` |

Correction 1 §4 names `evidence/freeze-r45.txt` as the instrument manifest;
at review end `evidence/` holds eleven files and **`freeze-r45.txt` is not one
of them**, so the digest binding the counter to the freeze does not exist yet.
I record the counter/mutant digests at the top of this report instead.

## Findings by severity

### S1 (critical) — filter options are unchecked: a row executes a program and writes files

`FILTERS` is checked on `argv[0]` only (`count-c1.py:65`); `parse_pipeline`
(`:207-236`) never inspects options, and `run_pipeline` (`:238`) executes the
argv as-is. Any option of an allow-listed filter therefore runs.

(a) Arbitrary program execution, **scoring met without `CONST=`** (the row is
also genuinely revision-sensitive):

    F12<TAB>11852<TAB>wave<TAB>git ls-tree -r --name-only @REV@ | sort -S 1K --compress-program=<scratch>/prog.sh | wc -l

    check rows_parse             PASS (12 rows)
    check revision_sensitivity   PASS (12 rows move, 0 CONST)
    C1=met mismatches=0 rows=12 classes=checks,corpus,evidence,registry,wave floor_rows=12 floor_classes=4 rev=397878bc0142e9bb4bbe5bf689d6c6495992d99d repo=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/tmp/RevC1Grammar/attack-repo other_rev=554ff416459c92f0dea9762f834a556df2990187 witnesses=3/3
    rc=0

    $ ls -l $TMPDIR/CANARY_COMPRESS        # created by the row, absolute path
    -rw-r--r-- 1 vgpnk vgpnk 0 … CANARY_COMPRESS

(b) Arbitrary file write (`sort -o` suppresses stdout, so the figure is 0 and
the row needs `CONST=`):

    F12<TAB>0<TAB>wave<TAB>git ls-tree -r --name-only @REV@ | sort -o <scratch>/CANARY_SORT | wc -l<TAB>CONST=sort output parked in a file, count still 0

    C1=met mismatches=0 rows=12 classes=checks,corpus,evidence,registry,wave floor_rows=12 floor_classes=4 rev=397878bc0142e9bb4bbe5bf689d6c6495992d99d repo=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/tmp/RevC1Grammar/attack-repo other_rev=554ff416459c92f0dea9762f834a556df2990187 witnesses=3/3
    rc=0

    $ ls -l $TMPDIR/CANARY_SORT
    -rw-r--r-- 1 vgpnk vgpnk 863491 … CANARY_SORT      # 11,852 repo paths, outside the repo

This contradicts the instrument's own docstring ("Later stages may only be
passive filters … executed WITHOUT a shell") and P-C1's "one `git` pipeline".
`sort -T <dir>` and `uniq IN OUT` are the same class.

### S2 (high) — `CONST=<anything>` voids revision sensitivity for the whole ledger

`CONST_RE = ^CONST=(\S.*)$` (`:68`) accepts any non-empty text, and `:373`
(`if const or fid not in values: continue`) skips every annotated row:

    F01<TAB>5577<TAB>evidence<TAB>git ls-tree -r --name-only @REV@ .ufo/waves | grep -c 'evidence'<TAB>CONST=value held constant by lane policy
    … (×12: the same twelve revision-constant rows, each annotated)

    check row_floor              PASS (rows=12 floor=12)
    check commands_reconcile     PASS (all rows match)
    check revision_sensitivity   PASS (0 rows move, 12 CONST)
    C1=met mismatches=0 rows=12 classes=checks,corpus,evidence,registry,wave floor_rows=12 floor_classes=4 rev=397878bc0142e9bb4bbe5bf689d6c6495992d99d repo=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/tmp/RevC1Grammar/attack-repo other_rev=554ff416459c92f0dea9762f834a556df2990187 witnesses=3/3
    rc=0

The identical bytes without the annotations are rejected:

    check revision_sensitivity   FAIL (F01 value=5577 at both revisions; F02 value=5777 at both revisions; F03 value=721 at both revisions; F04 value=225 at both revisions)
    C1=unmet mismatches=0 rows=12 classes=checks,corpus,evidence,registry,wave floor_rows=12 floor_classes=4 rev=4e5050378de6a7b7145925b3fae0daf8b6c1f50c repo=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/tmp/RevC1Grammar/attack-repo other_rev=554ff416459c92f0dea9762f834a556df2990187 witnesses=3/3 failed=revision_sensitivity
    rc=1

Even under Correction 1's `moved>=1` + `const<=rows-1`, the floor is *one*
moving row: eleven annotated constants plus one genuine mover still scores met
(`moved=1`, `const=11<=11`):

    check commands_reconcile     PASS (all rows match)
    check revision_sensitivity   PASS (1 rows move, 11 CONST)
    C1=met mismatches=0 rows=12 classes=checks,corpus,evidence,registry,wave floor_rows=12 floor_classes=4 rev=75c4b6e4127531b88e210854504c84041a5117ab repo=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/tmp/RevC1Grammar/attack-repo other_rev=554ff416459c92f0dea9762f834a556df2990187 witnesses=3/3
    rc=0

P-C1 as frozen permits `CONST=` per row, so the counter is faithful to the
predicate. The hole is that the predicate has no floor on the number of *moving*
rows and no structure on the reason — so "the ledger is revision-sensitive" is
one annotation away from false. Route to r46 as a lesson; the receipt must not
claim revision sensitivity from a `CONST`-heavy ledger.

### S3 (medium) — the witness arm is a weak oracle

`check_witnesses` (`:406-437`) requires only `rejected == total`. Rejection is
reason-agnostic and there is no minimum count, no class coverage, and no check
that `W-REVCONST`/`W-HEAD`/`W-DUP` are among them:

    $ cat wdir_junk/junk.tsv
    garbage line one
    garbage line two
    garbage line three

    witness junk.tsv                 rejected (rows_parse,row_floor,class_floor,revision_sensitivity)
    C1=met mismatches=0 rows=12 classes=checks,corpus,evidence,registry,wave floor_rows=12 floor_classes=4 rev=397878bc0142e9bb4bbe5bf689d6c6495992d99d repo=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/tmp/RevC1Grammar/attack-repo other_rev=554ff416459c92f0dea9762f834a556df2990187 witnesses=1/1
    rc=0

So `C1=met witnesses=1/1` proves nothing about the three vacuity classes. The
intended attack 7 *is* blocked — an honest ledger inside the dir:

    witness w-honest.tsv             ACCEPTED (no check failed)
    check witnesses_rejected     FAIL (witnesses=3/4)
    C1=unmet mismatches=0 rows=12 … witnesses=3/4 failed=witnesses_rejected
    rc=1

### S4 (medium) — the tip litmus only matches a 40-hex SHA

`TIP_RES` (`:69-74`) is `HEAD`-word, `@{`, and a 40-hex run:

    SHA40 = re.compile(r"^[0-9a-f]{40}$")
    TIP_RES = (
        re.compile(r"(?<![A-Za-z0-9_])HEAD(?![A-Za-z0-9_])"),
        re.compile(r"@\{"),
        re.compile(r"(?<![0-9a-fA-F])[0-9a-f]{40}(?![0-9a-fA-F])"),
    )

A short SHA of the tip is indistinguishable from honest text, so a row that pins
the tip is admitted:

    F12<TAB>450<TAB>evidence<TAB>git log --format=%s 3ad8faa @REV@ | wc -l

    check rows_parse             PASS (12 rows)
    check revision_sensitivity   PASS (12 rows move, 0 CONST)
    C1=met mismatches=0 rows=12 classes=checks,corpus,evidence,registry,wave floor_rows=12 floor_classes=4 rev=4e5050378de6a7b7145925b3fae0daf8b6c1f50c repo=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/tmp/RevC1Grammar/attack-repo other_rev=554ff416459c92f0dea9762f834a556df2990187 witnesses=3/3
    rc=0

The 40-hex spelling of the same row is rejected:

    check rows_parse             FAIL (row 12: command does not name @REV@; row 12: token '554ff416459c92f0dea9762f834a556df2990187:corpus/SOURCES.md' resolves the tip instead of @REV@; row 12: first stage does not name @REV@)
    C1=unmet mismatches=? … failed=revision_sensitivity,rows_parse
    rc=1

`@` is also undetected but dies at the divergence gate (constant across
`--other-rev`): `F12 value=450 at both revisions`, `C1=unmet`, rc=1. Any
fixed-tip row that also carries a moving `@REV@` term survives — exactly 2d.

### S5 (low) — path absence and a zero figure are indistinguishable for listing verbs

`git ls-tree -r --name-only <rev> <missing-path>` exits 0 with empty output, so
`| wc -l` is a legitimate-looking 0, and `CONST=` suppresses the divergence test
that would otherwise reject the constant 0:

    F12<TAB>0<TAB>evidence<TAB>git ls-tree -r --name-only @REV@ corpus/no-such-dir-r45 | wc -l<TAB>CONST=path absent at both revisions, so the figure is 0

    C1=met mismatches=0 rows=12 classes=checks,corpus,evidence,registry,wave floor_rows=12 floor_classes=4 rev=397878bc0142e9bb4bbe5bf689d6c6495992d99d repo=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/tmp/RevC1Grammar/attack-repo other_rev=554ff416459c92f0dea9762f834a556df2990187 witnesses=3/3
    rc=0

The `git show` spelling is correctly caught by the rc gate:

    check commands_reconcile     FAIL (F12 <- stage 1 rc=128 fatal: path 'corpus/no-such-file-r45.md' does not exist in '93cbf32e2cc140c84e85256c9379e4f19609a40f)
    C1=unmet mismatches=1 … failed=commands_reconcile
    rc=1

## Selftest and mutant

`--selftest` (scratch `TMPDIR` under my dir), untouched counter:

    selftest PASS honest_ledger_met
    selftest PASS offbyone_row_mismatch
    selftest PASS junk_producer_rejected
    selftest PASS below_floor_rejected
    selftest PASS absent_ledger_unmet
    selftest PASS duplicate_id_rejected
    selftest PASS duplicate_command_rejected
    selftest PASS head_reading_row_rejected
    selftest PASS revision_constant_row_rejected
    selftest PASS witness_dir_one_passing_witness
    C1_SELFTEST pass=10 fail=0
    rc=0

Mutant diff — one hunk, one check:

    @@ -307,7 +307,7 @@
    -        if fid in ids:
    +        if False:  # MUTANT: duplicate-id check disabled

Only the duplicate-id branch is disabled; `else: ids[fid] = n` bookkeeping, the
duplicate-command check, the tip litmus, the floors and the witness arm are
byte-identical. **The mutant disables exactly one check.**

Caught — the mutant's own `--selftest` fails exactly the matching arm and
nothing else:

    selftest FAIL duplicate_id_rejected: []
    C1_SELFTEST pass=9 fail=1
    rc=1

Falsifier on the duplicate-id ledger (the check is load-bearing):

    real counter : check rows_parse FAIL (row 12: duplicate id F05 (first at row 5))
                   C1=unmet … failed=revision_sensitivity,rows_parse        rc=1
    mutant       : check rows_parse PASS (12 rows)
                   C1=met mismatches=0 rows=12 … witnesses=3/3              rc=0
    honest ledger under the mutant: C1=met                                 rc=0

Note: `count-c1.py` never invokes the mutant (`grep -n mutant` → rc 1, no
match). P-C1 §4's "mutant caught" half is evidenced only by the mutant's own
failing arm — a valid falsifier, but a receipt convention, not a check the
counter performs.

## What the counter does right (verified, not asserted)

- metacharacters/`;`/`&&`/`$()`/backticks rejected before execution (`CANARY_SUBST`
  and `CANARY_BT` were absent after the runs);
- `tee` rejected as a non-filter; `diff` dropped from read verbs;
- duplicate id and whitespace-normalised duplicate command both rejected;
- floors clamp UP: `--min-rows 1` and `--min-rows -5` both print
  `floors rows>=12 classes>=4 (frozen; requested --min-rows -5 --min-classes 0)`
  and fail the 5-row ledger; `--min-rows 999` is honoured above the floor;
- `--other-rev` absent is a FAIL (`other_rev_present`), never a skip;
- `WORK` and unresolvable revisions are `C1_SETUP`/rc 2, no traceback;
- rc/pipefail gate: a failing `git show` stage or a zero-match `grep` is a
  failure, never a zero figure;
- `GIT_*` scrubbing works: `GIT_DIR=/nonexistent GIT_WORK_TREE=/nonexistent
  GIT_INDEX_FILE=/nonexistent` still reads the right repo (`C1=met`, rc 0);
- the verdict line is self-describing (floors, measured rev, repo, other rev,
  witness counts) as P-C1 requires.

## Residual risk and verification gaps

- Only the revisions listed above were measured. `--other-rev` equal to the
  measured rev, and an `--other-rev` where every cited path is absent, were not
  exercised.
- The tip-litmus gap was probed with `3ad8faa` and `@` only; `ORIG_HEAD`,
  `FETCH_HEAD`, `refs/heads/main` were reasoned from `TIP_RES`, not run.
- The writer/exec proofs used GNU `sort` on this host; other `sort`
  implementations may expose different option side effects, but the class
  (unchecked filter options) is implementation-independent.
- `--compress-program` fires only on temp spill; the row forces it with
  `-S 1K` over an 11,852-line listing. A ledger author controls that flag, so
  the trigger is under the row's control, not the runner's.
- The counter does not sandbox the child's cwd or writable roots: my canaries
  were absolute paths in scratch, and the same row could name any path the
  runner can write. I did not attempt a write outside my own scratch.
- Predicate drift (§Predicate drift) is unreconciled at review end: the counter
  predates `Correction 1` and implements none of its C1 thresholds. Any `met`
  receipt for C1 must state which contract digest and which counter digest it
  pairs.
- The measured revisions are real commits in a `--shared` clone of this lane
  (the lane's own objects and history, plus my ledger commits) because the lane
  git is read-only for me and a ledger must be readable at the measured
  revision. No lane commit was made; no scratch file was deleted that I did not
  create; no subagent was dispatched.
- All bypasses are instrument-level results. Per the contract this is a
  post-freeze finding: lessons for round 46, not patches to `count-c1.py`. No
  verdict here is an admission of C1.
