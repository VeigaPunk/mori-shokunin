# Mo60Scribe75 — absent-set reconciliation table, count-c1 grammar (round 60, w1)

Seat: Mo60Scribe75 (scribe). Read-only. No production edits, no VCS mutation, no
fleet/sibling writes, no commits. Deliverable: the C1 ABSENT-SET ARM table drafted
exactly in `count-c1.py`'s row grammar, truth cells filled from `git cat-file -e`.

## Pins

| what | revision |
|---|---|
| lane | `/home/vgpnk/Projects/shokunin/mori-shokunin` |
| entering revision (contract) | `ddfb12fb0838b4307c445194a844f0c4b1950195` |
| r59 data revision (frozen) | `7b86704d7c0754a09958d131b64dbfa2a6d3eaed` |
| r59 landing commit (frozen) | `f091bd773c4cfec8877061c84f4bae5f11e8bbe5` |
| tip at measurement (pinned) | `b3c256138f00c704d5aa56eb0332d74506502ef2` ("round-60: move S561-S564 rows into the Registry table", 2026-10-28 12:59:33 -0300) |
| `count-c1.py` read | lane working tree = pin (`.ufo/waves/round-60/count-c1.py`, W1_DIR = `.ufo/waves/round-59/w1`, NAMES = the five frozen names) |

Disk guard before work: `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`
→ `/fast/scratch/hyaku 26% 598.6G` free — green.

Scratch: `/fast/scratch/hyaku/mori-r60/Mo60Scribe75` (created with `mkdir -p`, `TMPDIR` set to it).

## Truth cells (commands and raw outcomes)

Per-name truth at the r59 data revision (`count-c1.exists()` semantics: rc == 0 means present):

```
$ git -C <lane> cat-file -e 7b86704d7c0754a09958d131b64dbfa2a6d3eaed:.ufo/waves/round-59/w1/<name>.md
fatal: path '.ufo/waves/round-59/w1/Mo59Executor40.md' exists on disk, but not in '7b86704d7c0754a09958d131b64dbfa2a6d3eaed'
Mo59Executor40 rc=128
fatal: path '.ufo/waves/round-59/w1/Mo59MutationTester31.md' exists on disk, but not in '7b86704d7c0754a09958d131b64dbfa2a6d3eaed'
Mo59MutationTester31 rc=128
fatal: path '.ufo/waves/round-59/w1/Mo59MutationTester32.md' exists on disk, but not in '7b86704d7c0754a09958d131b64dbfa2a6d3eaed'
Mo59MutationTester32 rc=128
fatal: path '.ufo/waves/round-59/w1/Mo59Critic29.md' exists on disk, but not in '7b86704d7c0754a09958d131b64dbfa2a6d3eaed'
Mo59Critic29 rc=128
fatal: path '.ufo/waves/round-59/w1/Mo59Reviewer16.md' exists on disk, but not in '7b86704d7c0754a09958d131b64dbfa2a6d3eaed'
Mo59Reviewer16 rc=128
```

At the pinned tip:

```
$ git -C <lane> cat-file -e b3c256138f00c704d5aa56eb0332d74506502ef2:.ufo/waves/round-59/w1/<name>.md
Mo59Executor40 rc=0
Mo59MutationTester31 rc=0
Mo59MutationTester32 rc=0
Mo59Critic29 rc=0
Mo59Reviewer16 rc=0
```

The data revision has no `w1/` directory at all (so absence is structural, not a
per-name quirk):

```
$ git -C <lane> ls-tree --name-only 7b86704d7c0754a09958d131b64dbfa2a6d3eaed:.ufo/waves/round-59/
assimilation
build-w1-spec.py
contract.md
count-c1.py
count-c2.py
evidence
fixtures-c1
trees-c2
w1-dispatch.json
w1-spec.json
w1.ready
```

Landing history (`git log --diff-filter=A` / `git log` on each path):

```
Mo59Executor40        ADD f091bd77 2026-10-28 07:42:42 -0300  (only touch)
Mo59MutationTester31  ADD f091bd77 2026-10-28 07:42:42 -0300  (only touch)
Mo59MutationTester32  ADD bf6c0ad3 2026-10-28 03:12:38 -0300, modified f091bd77 07:42:42
Mo59Critic29          ADD bf6c0ad3 2026-10-28 03:12:38 -0300  (only touch)
Mo59Reviewer16        ADD bf6c0ad3 2026-10-28 03:12:38 -0300  (only touch)
```

`f091bd77` diff for `w1/`: adds `Mo59Executor40.md` (+556), `Mo59MutationTester31.md`
(+111), modifies `Mo59MutationTester32.md` (5 +-, 2 deletions), and adds
`w1-results.json`. No deletions of `w1/*.md` exist in history
(`git log --diff-filter=D -- .ufo/waves/round-59/w1/ | wc -l` → `0`), so the
"present at tip" cells hold for any later R that keeps `f091bd77` an ancestor.

## Finding F1 — the seat premise is contradicted by git truth (verbatim conflict)

Seat text: "Mo59Critic29 and Mo59Reviewer16 present at 7b86704d -> wrong-superseded;
the other three absent there -> late-committed, pointer f091bd77".

Measured truth: **all five are absent at `7b86704d`**; `7b86704d` (2026-10-28
03:00:51) predates the first commit that contains any `w1/` report. Critic29,
Reviewer16 and MutationTester32 exist at `bf6c0ad3` (2026-10-28 03:12:38, the r59
integrate/filing commit), which is **not** an ancestor of the data revision:

```
$ git -C <lane> merge-base --is-ancestor bf6c0ad3 7b86704d7c0754a09958d131b64dbfa2a6d3eaed
rc=1
```

So "present at 7b86704d" is really "present at filing (`bf6c0ad3`)" for those
names. Under count-c1's frozen predicate ("disposition is `late-committed`
exactly when the file was absent at `7b86704d…`, else `wrong-superseded`"),
**no frozen name is `wrong-superseded`; all five are `late-committed`**. This
matches the already-landed table and `corpus/lessons/round-60.md` ("Round-59
absent-set correction (supersedes round-59)": Critic29/Reviewer16 are described as
committed pre-filing in `bf6c0ad3`, superseding the r59 lesson's absent claim).

Counterfactual replay of count-c1's absent-set arm over the seat's premise
(`Critic29`, `Reviewer16` set to `present`/`wrong-superseded`):

```
COUNTERFACTUAL-rows_ok=3/5 failed=['Mo59Critic29', 'Mo59Reviewer16']
```

i.e. the premise as stated would score `absent-set=3/5` and fail C1.

## Draft table (exact bytes)

418 bytes, sha256 `96183cd847220b148bc6d1bc32e5c0607498067231a59f2ad099807ccd324afc`:

```
| name | at 7b86704d | at tip | disposition | pointer |
|---|---|---|---|---|
| Mo59Executor40 | absent | present | late-committed | f091bd77 |
| Mo59MutationTester31 | absent | present | late-committed | f091bd77 |
| Mo59MutationTester32 | absent | present | late-committed | bf6c0ad3 |
| Mo59Critic29 | absent | present | late-committed | bf6c0ad3 |
| Mo59Reviewer16 | absent | present | late-committed | bf6c0ad3 |
```

Pointer cells carry the true add-commit (short hash) per file: `f091bd77` for the
two seats landed after filing, `bf6c0ad3` for the three committed at the filing
commit but after the data revision. `MutationTester32` was modified again in
`f091bd77`; its tip bytes come from there, though it first landed at `bf6c0ad3`.

## Validation against count-c1 itself

`parse_absent_table` (imported read-only from the frozen counter via
`importlib.util.spec_from_file_location`) over the draft bytes:

```
parse_absent_table -> 5 rows
{'Mo59Executor40': ('absent', 'present', 'late-committed'),
 'Mo59MutationTester31': ('absent', 'present', 'late-committed'),
 'Mo59MutationTester32': ('absent', 'present', 'late-committed'),
 'Mo59Critic29': ('absent', 'present', 'late-committed'),
 'Mo59Reviewer16': ('absent', 'present', 'late-committed')}
Mo59Executor40        cell=('absent', 'present', 'late-committed') truth=('absent', 'present', 'late-committed') match=True
Mo59MutationTester31  cell=('absent', 'present', 'late-committed') truth=('absent', 'present', 'late-committed') match=True
Mo59MutationTester32  cell=('absent', 'present', 'late-committed') truth=('absent', 'present', 'late-committed') match=True
Mo59Critic29          cell=('absent', 'present', 'late-committed') truth=('absent', 'present', 'late-committed') match=True
Mo59Reviewer16        cell=('absent', 'present', 'late-committed') truth=('absent', 'present', 'late-committed') match=True
ABSENT-SET-ARM-VALIDATION PASS
```

Grammar notes (from the frozen parser, lines 105–124): the header row is skipped
because its first cell is `name`; the separator row is skipped because its first
cell does not start with `Mo`; every data row is exactly 5 cells with
`present|absent`, `present|absent`, and an exact `late-committed|wrong-superseded`
token. The draft satisfies all three checks with no duplicated-name overwrite
(5 distinct names, matching `NAMES`).

## Comparison with the landed evidence file

`.ufo/waves/round-60/evidence/r59-absent-set.md` is committed (added at
`398d3225`, 2026-10-28 12:58:36 -0300; 1596 bytes, sha256
`0f881eb9bd872e70dccc0f1343a98057b22cada7b80dbeb375f69af0e6650b24`). Parsed at the
pinned tip it yields the same five rows and the same three checked cells as the
draft; it differs only by prose in the pointer cells ("`f091bd77` (07:42:42 -03,
post-filing)", "added `bf6c0ad3` …") and the explanatory paragraphs. The draft is
the byte-compact canonical rendering, not a correction of content.

Lesson arm replayed read-only at the pinned tip (`corpus/lessons/round-60.md`):
`supersedes round-59` present; for each of the five (all absent at data rev) the
arm `name in lesson and 'f091bd77' in lesson` is `True` → `lesson=ok`.

## Findings / limits

- **F1** above: the seat's `wrong-superseded` premise for `Mo59Critic29` /
  `Mo59Reviewer16` is false at `7b86704d`; the table must carry `absent` for both.
- **F2 (pointer-cell semantics tension, report-only):** the contract's
  ABSENT-SET ARM sentence "every late-committed name with landing pointer
  `f091bd77`" is not literally true for `Mo59MutationTester32`, `Mo59Critic29`
  and `Mo59Reviewer16` if "landing pointer" means the add-commit — they landed at
  `bf6c0ad3`. `count-c1.py` never validates the pointer cell (it checks only
  cells 1–3), and its lesson arm needs only the literal `f091bd77` anywhere in
  the lesson, so both renderings pass the frozen gate; the landed table and
  lesson use the true add-commits plus `f091bd77` as the round-closing pointer.
  No action taken; frozen text left untouched.
- **F3:** `git cat-file -e` exits **128**, not 1, for a path that exists on disk
  but not in the named tree. `count-c1.exists()` only tests `rc == 0`, so truth
  resolves correctly; anyone grepping for `rc=1` would misread absence.
- **F4 (unattributed artifact, not relied on):** `.ufo/waves/round-60/evidence/c1-at-data.txt`
  exists untracked (109 bytes, 12:59) reading
  `C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=b3c25613…`.
  It was not produced by this seat and is cited only as context.
- **F5 (observed at cleanup, detection only, not produced by this seat):** the lane
  working tree carries an untracked `EXEC-MARKER` at the lane root
  (`-rw-r--r-- 92 bytes, 2026-10-28 13:16:28 -0300`), content
  `executed /fast/scratch/hyaku/mori-r60/Mo60Executor58/full-old/real2/round-53/w1-results.json`
  (no trailing newline). It is the G1 PoC marker, but it landed in the **lane
  root**, not under any scratch root — i.e. that replay's marker write was
  cwd-relative with cwd = lane. Left in place (not my artifact); flagged for the
  L1 because the G1 predicate is phrased over "its scratch" and the G2 containment
  story is about nothing being written outside the scratch root. Attribution is
  by content only; no process was inspected. Other untracked entries at 13:16
  (`evidence/c1-at-data.txt`, `w1.ready`, `w1.ready.dispatched`, `w1/`) are not
  this seat's either, except `w1/Mo60Scribe75.md` (this report).
- **Limits:** the full `count-c1.py` (which re-runs the two r59 counters for the
  RECEIPTS ARM) was **not** executed here — only its `parse_absent_table` and the
  absent-set/lesson arm logic were replayed read-only, plus git truth. No
  counter ran with `--scratch`; no lane gate/selftest ran. No commits, no VCS
  mutation, no writes outside this report and scratch.

Scratch `/fast/scratch/hyaku/mori-r60/Mo60Scribe75` held only `draft-table.md`,
`validate_draft.py`, `validate_landed.py` and was removed after copying the draft
bytes into this report; the embedded block was re-extracted and byte-compared to
the validated draft before cleanup.
