# Mo60Revenger96 — commit archaeology of the dead evidence pointers

Seat: revenger (leaf). Mode: read-only `git show` / `git log -S` / `git log -G` /
`git rev-list --objects`. No commits, no VCS mutation, no fleet/sibling writes.
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin` @ tip `b3c25613`
(freeze `ac496c7c`, entering `ddfb12fb`).
Scratch: `/fast/scratch/hyaku/mori-r60/Mo60Revenger96` (created, unused for
writes beyond `mkdir`; no clones needed — all reads are `git show` against the lane).

## Headline

The dead names were **never files, in any commit, on any ref**. They were born as a
**write-time naming error inside one integration commit** (`bf6c0ad3`), written
**10 h 18 m after** the correct receipt blobs already existed byte-identically in the
tree. The real names were introduced by the r59 **freeze** commit `ccfd554e`, whose
receipt blobs are the *same two blob SHAs* at freeze, at the r59 data rev, at the r60
entering rev, and at today's tip — so this is a pure pointer hole with **zero content
divergence**. The r60 correction (`398d3225`) re-pointed the two lines in place and
dropped uncorrected occurrences 2 → 0.

## Timeline (all times `-03`, chronological)

| # | Commit | Timestamp | Event | Dead-name total in `SCORECARD.md` |
|---|---|---|---|---|
| 0 | `2b9f0397` | pre-round | r59 **entering** rev (parent of the freeze) | 0 |
| 1 | **`ccfd554e`** | 2026-10-27T16:36:43 | **REAL names created** — `round-59: freeze contract, C1/C2 counters, tools, fixtures, controls`. Adds `.ufo/waves/round-59/evidence/control-c1-do-nothing.txt` (300 B, blob `fe6b02aa`) and `control-c2-do-nothing.txt` (729 B, blob `b7fc827d`). Parent = `2b9f0397`. | 0 |
| 2 | `60b3a76a` | 2026-10-28T02:49:04 | r59 freeze amendment (counter scratch-mkdir, `ls-tree rev:path`, register name boundary) — pre-data | 0 |
| 3 | `8ff344ff` | 02:50:48 | validated w1 dispatch payload (64 seats, v2) | 0 |
| 4 | `be737211` | 02:52:30 | r59 land C2 data | 0 |
| 5 | **`7b86704d`** | 2026-10-28T03:00:09 | r59 **data** rev (K11 demoted to prose). Receipt blobs unchanged. This is the rev C1's receipts arm must reproduce. | **0** |
| 6 | **`bf6c0ad3`** | 2026-10-28T03:00:51 | **FIRST appearance of the dead citation.** `round-59: integrate w1 — …`. Adds `SCORECARD.md:2950` (C1) and `:2951` (C2), each citing `.ufo/waves/round-59/evidence/c{1,2}-entering.txt` for the *“At entering `2b9f0397`”* cell. 0 → 2 occurrences. Parent = `7b86704d`. | **2** (uncorrected 2) |
| 7 | `f091bd77` | 03:12:53 | r59 late landing (`w1-results.json` 64/64 + 3 late seat reports) | 2 (2) |
| 8 | `a86e5f83` | 07:4x | pre-spot-check tip | 2 (2) |
| 9 | **`ddfb12fb`** | 2026-10-28T07:43:47 | **r60 entering rev** — `round-59 verifier spot-check (integrator, hyaku)`. Adds `corpus/lessons/round-59-verifier-spotcheck.md`, whose `## Defects routed` item 1 *names the dead names as defects*. Diagnostic prose, not a defective pointer. | 2 (2) |
| 10 | **`398d3225`** | 2026-10-28T12:53:13 | **CORRECTION** — `round-60: land C1 data …`. In-place re-point of `:2950/:2951` to `control-c{1,2}-do-nothing.txt` with `r60-correction:` markers; first commit to name the real pointers in `QUALITY.md` 156/157 and `corpus/lessons/round-60.md`. | 2 (**0**) |
| 11 | `b3c25613` | tip | `round-60: move S561-S564 rows into the Registry table (census E12 fix)` | 2 (0) |

Machine check of the count column:

```
$ for r in 2b9f0397 7b86704d bf6c0ad3 f091bd77 ddfb12fb a86e5f83 398d3225 b3c25613; do
    printf '%s  total=%s  uncorrected=%s\n' "$r" \
      "$(git show $r:SCORECARD.md | grep -c 'c1-entering\.txt\|c2-entering\.txt')" \
      "$(git show $r:SCORECARD.md | grep 'c1-entering\.txt\|c2-entering\.txt' | grep -vc 'r60-correction:')"
  done
2b9f0397  total=0  uncorrected=0
7b86704d  total=0  uncorrected=0
bf6c0ad3  total=2  uncorrected=2
f091bd77  total=2  uncorrected=2
ddfb12fb  total=2  uncorrected=2
a86e5f83  total=2  uncorrected=2
398d3225  total=2  uncorrected=0
b3c25613  total=2  uncorrected=0
```

This is exactly the two committed states QUALITY 156 claims (`dead-uncorrected=2` at
entering, `=0` after correction) — reproduced independently here from bytes.

## Q1 — when did the names first appear as citations?

`git log -S` on `SCORECARD.md` returns **exactly one commit per name**:

```
$ git log --format='%H %ad %s' --date=iso-strict -S'c1-entering.txt' -- SCORECARD.md
bf6c0ad3acbd60f7561d12d2663d12f9243562ef 2026-10-28T03:00:51-03:00 round-59: integrate w1 — …
$ git log --format='%H %ad %s' --date=iso-strict -S'c2-entering.txt' -- SCORECARD.md
bf6c0ad3acbd60f7561d12d2663d12f9243562ef 2026-10-28T03:00:51-03:00 round-59: integrate w1 — …
```

Count at parent vs at commit: **0 → 2**. Word-diff of that one commit shows both
citations inserted as plain text on the C1/C2 rows:

```
$ git show bf6c0ad3 --word-diff=porcelain -- SCORECARD.md | grep -E 'c[12]-entering\.txt'
+| C1: … rc 1 (`.ufo/waves/round-59/evidence/c1-entering.txt`) | At `7b86704d`: …
+| C2: … rc 1 (`.ufo/waves/round-59/evidence/c2-entering.txt`) | At `7b86704d`: …
```

**Methodological caveat worth carrying into the lesson:** `-S` alone is *insufficient
for this class*. Because the correction re-points the line while **retaining** the literal
dead name (“… cited a dead name `c1-entering.txt` …”), the `-S` count stays at 2 across
`398d3225` — `-S` never sees the fix. `-G` (or a content diff) is required:

```
$ git log --format='%h %s' -G'r60-correction:' -- SCORECARD.md
398d3225 round-60: land C1 data — …
$ git log --format='%h %s' -G'.ufo/waves/round-59/evidence/control-c1-do-nothing.txt' -- SCORECARD.md
398d3225 round-60: land C1 data — …
```

The correction diff itself (word-diff, both lines):

```
-[-(`.ufo/waves/round-59/evidence/c1-entering.txt`)-]-
+{+(`.ufo/waves/round-59/evidence/control-c1-do-nothing.txt` — r60-correction: the r59 report
   and this cell cited a dead name `c1-entering.txt`; the committed control receipt is
   `control-c1-do-nothing.txt`)+}
```

## Q2 — was any file ever committed under those names?

**No — not on any ref, ever.**

```
$ git rev-list --all --objects | awk '{ $1=""; sub(/^ /,""); print }' \
    | grep -E '(^|/)(c1|c2)-entering\.txt$'
$ echo $?
1                                   # no match
$ git log --all --oneline --diff-filter=A -- '*c1-entering.txt' '*c2-entering.txt'
$ echo $?
0                                   # empty: no additive commit, no output
$ git rev-list --all --objects | grep -E 'round-59/evidence/' | grep -Ei 'entering'
$ echo $?
1                                   # nothing under the cited directory either
```

What *does* exist in object space (all false friends, all predating r59):

| Object | Path | Why it is not the cited file |
|---|---|---|
| `3a040371` | `.ufo/waves/round-58/w1/Mo58Executor46-evidence/c1-entering-stdout.txt` | r58 seat scratch capture; different directory, name carries `-stdout` |
| `27f23bc3` | `.ufo/waves/round-56/evidence/controls.txt` | round-56 receipt — **this name was real in r56** |
| `68320e79` | `.ufo/waves/round-57/controls.txt` | round-57 receipt — **real in r57** |
| `fb697578` | `.ufo/waves/round-58/evidence/controls.txt` | round-58 receipt — **real in r58** |

The cited directory's true contents at the data rev:

```
$ git ls-tree -r --name-only 7b86704d -- .ufo/waves/round-59/evidence/
.ufo/waves/round-59/evidence/c1-at-freeze.txt
.ufo/waves/round-59/evidence/c2-at-freeze.txt
.ufo/waves/round-59/evidence/census-start.txt
.ufo/waves/round-59/evidence/control-c1-do-nothing.txt
.ufo/waves/round-59/evidence/control-c2-do-nothing.txt
.ufo/waves/round-59/evidence/selftests.txt
```

The one pre-existing *string* match in the whole repo — `.ufo/waves/round-50/a2w1/
Mo50bScribeQuality.md:253` lists `c1-entering.txt` among *scratch capture* filenames
(`c1-landed.txt`, `c1-entering.txt`, …). That is a scratch-directory listing five rounds
older, not an evidence pointer, and is correctly left alone by the counter.

## Q3 — which commit introduced the real `control-*.txt` names?

**`ccfd554e64084a0b4370806dd12a850e0a7bd7db`**, 2026-10-27T16:36:43 `-03`, parent
`2b9f0397` (= the r59 entering rev) — the r59 **freeze**, i.e. committed *pre-data*,
10 h 18 m before the dead citation was written.

```
$ git -c diff.renames=false show --diff-filter=A --name-status --format='' ccfd554e -- .ufo/waves/round-59/evidence/
A	.ufo/waves/round-59/evidence/census-start.txt
A	.ufo/waves/round-59/evidence/control-c1-do-nothing.txt
A	.ufo/waves/round-59/evidence/control-c2-do-nothing.txt
A	.ufo/waves/round-59/evidence/selftests.txt
```

**Disambiguation (important).** `--all --diff-filter=A` on those paths also returns
`3bc33fd0` and `e314014c`, both with **empty subject and the same parent**
`2b9f0397`, each appearing to add the identical four files. They are jj
abandoned-working-copy keeps, **not** separate introductions:

```
$ git merge-base --is-ancestor <c> HEAD
ccfd554e  YES
3bc33fd0  NO
e314014c  NO
$ git for-each-ref --contains 3bc33fd0 --format='%(refname)'
refs/jj/keep/3bc33fd0d262b940844462dac70a221a720f4524
$ git for-each-ref --contains e314014c --format='%(refname)'
refs/jj/keep/e314014cc8c208af39517262782b2155b6519842
```

Only `ccfd554e` is on the master line. All three carry the *same* `control-c1` blob
`fe6b02aa`, so they are duplicate snapshots of one change, not three authorships.

**Receipt bytes never moved** — blob identity from freeze to tip:

| Rev | `control-c1-do-nothing.txt` | `control-c2-do-nothing.txt` |
|---|---|---|
| `ccfd554e` (freeze) | `fe6b02aa…` 300 B | `b7fc827d…` 729 B |
| `7b86704d` (r59 data) | `fe6b02aa…` 300 B | `b7fc827d…` 729 B |
| `ddfb12fb` (r60 entering) | `fe6b02aa…` 300 B | `b7fc827d…` 729 B |
| `b3c25613` (tip) | `fe6b02aa…` 300 B | `b7fc827d…` 729 B |

Corroboration that the *receipt content* matched the cell it was mis-cited for — the
receipt names the exact entering rev and reproduces the cell's verdict:

```
$ git show 7b86704d:.ufo/waves/round-59/evidence/control-c1-do-nothing.txt
# C1 do-nothing control at entering rev 2b9f03975bfb6e508f35074ac8181ec8bf54e805
$ python3 .ufo/waves/round-59/count-c1.py 2b9f0397…
C1=unmet selftest=bad fixtures=bad real=bad pointers=bad rev=2b9f03975bfb6e508f35074ac8181ec8bf54e805 failed=tool_absent,selftest,fixtures_absent,real,pointers
rc=1
```

So the defect is a **naming error at citation time**, not a fabricated or retyped
receipt. That is what makes `reference-drift` the right class, and it raises the value of
QUALITY 156's mechanical sweep over the value of any prose review.

## Divergences against the current record (3 findings)

1. **`controls.txt` is not substantiated in round-59 bytes.** `corpus/lessons/round-59-
   verifier-spotcheck.md:93` (and the r60 restatements) route **three** dead names and
   claim `controls.txt` was *cited* and that “there is no `controls.txt`”. Measured:
   ```
   $ git grep -c 'controls\.txt' bf6c0ad3 -- .ufo/waves/round-59/
   $ echo $?
   1                                   # zero occurrences in the whole r59 subtree
   $ git log --all --format='%h %s' -S'.ufo/waves/round-59/evidence/controls.txt'
                                       # empty: that path was never cited anywhere
   ```
   `controls.txt` was a **real** committed receipt in r56/r57/r58 (blobs `27f23bc3`,
   `68320e79`, `fb697578`), so the sentence “there is no `controls.txt`” is false as
   written — there is no *round-59* `controls.txt`. Recommendation: scope that clause to
   round 59, or drop the third name; the frozen counter's `DEAD_NAMES` already covers
   only `c1-entering.txt` / `c2-entering.txt` (`count-c1.py:42`), which is consistent
   with the *evidence* but not with the *prose*.

2. **The “report” half of “dead pointers in report+SCORECARD” is not lane-verifiable.**
   At `bf6c0ad3` (and at the entering rev) the only committed files containing the dead
   names are `SCORECARD.md:2950–2951` and the unrelated r50 scratch listing. There is
   **no round-59 report file in the lane at all**:
   ```
   $ git ls-tree -r --name-only bf6c0ad3 -- .ufo/waves/round-59/ | grep '\.md$' | grep -v '/w1/'
   .ufo/waves/round-59/contract.md
   .ufo/waves/round-59/fixtures-c1/…/scorecard.md …
   ```
   `[INFERENCE]` The “report” is the L1's out-of-repo wave report. The Mistakes row
   should either cite that surface explicitly or say “SCORECARD (r59 rows 2950–2951)”
   only, so the row's `evidence:` field stays resolvable by QUALITY 156's own sweep.

3. **`-S` cannot find the fix.** The correction preserves the dead name inside the
   corrected line, so `git log -S'c1-entering.txt'` reports one commit and never
   `398d3225`. Any future audit script built on `-S` will conclude the correction does
   not exist. Use `-G` or diff-based checks (`count-c1.py`'s marker-per-line rule is the
   correct shape).

## Confidence

- Timeline commits, timestamps, parents, blob SHAs, byte sizes: **observed**, exact
  commands and outputs above.
- “No file ever committed under those names”: **observed** over `--all` object space
  plus `--diff-filter=A` over all refs (includes `refs/jj/keep/*`).
- `controls.txt` never cited in r59: **observed** (two independent queries).
- “Report” == out-of-repo L1 report: **[INFERENCE]** — not resolvable in lane object
  space; the absence of a lane r59 report is observed.
- Intent of the mis-citation (typo vs. copy-forward from r58's `controls.txt`):
  **[INFERENCE]** not claimed; the r58 name `controls.txt` existing one round earlier is
  a plausible copy-forward source, nothing more.

## Ready-to-use Mistakes row (draft)

```
1. class reference-drift · evidence: SCORECARD.md:2950-2951 at bf6c0ad3
   (2026-10-28T03:00:51-03, parent 7b86704d) cite
   .ufo/waves/round-59/evidence/c1-entering.txt / c2-entering.txt; no object was
   ever committed under those names on any ref (rev-list --all --objects and
   --diff-filter=A --all both empty). The real receipts were introduced 10h18m
   earlier in the r59 freeze ccfd554e (parent 2b9f0397) and are blob-identical
   fe6b02aa (300 B) / b7fc827d (729 B) from freeze to tip — pure pointer hole,
   zero content divergence; the cited cell's verdict matches the receipt's own
   stdout at 2b9f0397. · captured-by: none — no pointer-existence check ran
   before filing · fix: r60-correction: re-pointing in SCORECARD (398d3225,
   uncorrected 2 -> 0), the count-c1 DEAD-NAME ARM, and QUALITY 156.
   Note for the auditor: git log -S cannot see this fix (the corrected line
   retains the dead name); use -G.
```
