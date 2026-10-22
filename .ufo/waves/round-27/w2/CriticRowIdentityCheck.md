# CriticRowIdentityCheck — round 27 wave 2 (falsify QUALITY 81's check)

Seat: MoriR27.CriticRowIdentityCheck. Target: `.ufo/waves/round-27/check-row-identity.py` at lane tip
`5f00fd045c137b7e3835506d69946cfd9d010eb5` (sha256 `21dfa3d7…7db09`, byte-identical scratch copy confirmed with
`sha256sum`). Scratch: `/fast/scratch/hyaku/mori-r27/CriticRowIdentityCheck/` (`cases.py`, `run.py`, `cases.out`,
`cases-fixed.out`, `cri_fixed.py`, `hist.py`). The runner imports the unmodified copy and sets `LANE` to a per-case
scratch repo before calling `main()`. Tools: git 2.56.0, Python 3.14.8. Nothing was installed or upgraded.

## Verdict

The check is **sound for what it compares** (an in-place edit to a well-formed, unique, still-present row on the
first-parent line is always caught), but it **passes at exit 0 on six classes of real violations**. Those are: a row
that is deleted or renumbered, a duplicate id placed after the original, a row whose spacing breaks the exact `" | "`
split, a table whose column count changes (vacuous `rows=0 changed=0`), and a row first published on a side branch
and edited before the merge. QUALITY 81 (`corpus/QUALITY.md:376`) says the check "reads every row's first-published
cells from committed history and must print `changed=0`". A reader who gets that output would wrongly conclude that
CORPUS.md Rules 2 (append-only, `/home/vgpnk/Projects/shokunin/CORPUS.md:116`) holds.

None of these is live in the lane's history today (see "Real-data checks"). They are latent false negatives in a
check that is meant to guard every future round. A 30-line correction (below) closes all of them and gives identical
`changed` lines at the tip, at `fc09f96c` and at `ef9dbee1`.

## Real-data checks (lane, read-only git)

- Script at tip: prints `changed` for S090, S093, S096, S097 and S101, then `rows=141 changed=5`, exit 1. At
  `fc09f96c` it prints the same five plus S124, then `rows=126 changed=6`, exit 1. Both match the lesson
  (`corpus/lessons/round-27.md:40`). QUALITY 81 is therefore not met at the landed tip; the lesson routes the five
  rows to wave 2, so this is context, not a defect of the check.
- Census at tip: 141 rows, 0 malformed (`NF!=13`), no duplicate ids, 0 lines containing `\|`.
- `hist.py` compares the script's `rows()` with the census row regex in each of the 28 commits that touch
  `corpus/SOURCES.md`. In every commit the parsed count equals the census count, with no duplicates and no skipped
  ids, from `1f07f1d census=33 parsed=33` to `5f00fd0 census=141 parsed=141`.
- Commits touching the path: 28 in the full log and 28 with `--first-parent`. `git log --merges -- corpus/SOURCES.md`
  prints nothing, and the whole history has 2 merges. So the first-parent limitation has not bitten yet.

## Cases (scratch repos; expected vs observed with the landed script)

Columns: case, expected, observed (stdout summary, exit), verdict, severity.

| # | case | expected | observed | verdict | sev |
|---|---|---|---|---|---|
| A1 | control: `teaches` edited in place | `changed S002 cells=teaches`, 1 | same, `rows=3 changed=1`, 1 | holds | — |
| A2 | control: `status` edited in place | `changed=0`, 0 | `rows=3 changed=0`, 0 | holds | — |
| B1 | renumber S003 → S004 (S003 gone, same text) | flag, 1 | `rows=3 changed=0`, **0** | **FN** | high |
| B2 | renumber S002 → S0002 | flag, 1 | `rows=3 changed=0`, **0** | **FN** | high |
| C1 | edited copy of S002 appended after the original | flag, 1 | `rows=3 changed=0`, **0** | **FN** | high |
| C2 | edited copy of S002 inserted before the original | flag, 1 | `changed S002 cells=teaches`, 1 | holds (by order luck) | — |
| C3 | first-publish commit already had a draft S002 above the original; later commit keeps only the original | no change visible to a reader | `changed S002 cells=teaches`, 1 | FP, order-dependent | low |
| D1 | row S002 deleted | flag, 1 | `rows=2 changed=0`, **0** | **FN** | high |
| D2 | S002 deleted, re-added with new text | `changed S002`, 1 | `changed S002 cells=teaches`, 1 | holds | — |
| D3 | S002 deleted, re-added identical at the end | 0 | `rows=3 changed=0`, 0 | holds | — |
| D4 | file emptied (all rows deleted) | flag, 1 or 2 | `rows=0 changed=0`, **0** | **FN** | high |
| E1 | side branch adds S004 then edits it; main touches the file; `--no-ff` merge; rev = merge | `changed S004 cells=teaches`, 1 | `rows=4 changed=0`, **0** | **FN** | medium |
| E2 | as E1, main untouched since the branch point | same | `rows=4 changed=0`, **0** | **FN** | medium |
| E3 | side adds S004 unedited; merge; then main edits S004 | `changed S004`, 1 | `changed S004 cells=teaches`, 1 | holds | — |
| E4 | side branch edits existing S001; merge | `changed S001`, 1 | `changed S001 cells=teaches`, 1 | holds | — |
| F1 | cell `a \| b` → `a \| c` | `changed S002`, 1 | `changed S002 cells=teaches`, 1 | holds | — |
| F2 | escaped pipe introduced into `teaches` | `changed S002`, 1 | `changed S002 cells=teaches`, 1 | holds | — |
| F3 | unescaped ` \| ` added to `teaches` plus an edit (12 cells) | flag, 1 | `rows=2 changed=0`, **0** | **FN** | high |
| F4 | `used-by` ends in an escaped pipe, closing pipe kept | 0 | `rows=3 changed=0`, 0 | holds | — |
| G1 | `teaches` edited, and one separator written `\|queued \|` | flag, 1 | `rows=2 changed=0`, **0** | **FN** | high |
| G2 | `teaches` edited, row indented one space | flag, 1 | `rows=2 changed=0`, **0** | **FN** | high |
| G3 | `teaches` edited, compact GFM row `\|S002\|…\|` | flag, 1 | `rows=2 changed=0`, **0** | **FN** | high |
| G4 | `teaches` edited, text after the closing pipe | flag, 1 | `rows=2 changed=0`, **0** | **FN** | high |
| G5 | header and every row gain a 12th column, S001 `teaches` edited | rows checked or error | `rows=0 changed=0`, **0** | **FN (vacuous pass)** | high |
| G6 | S004 first published as a compact row, later normalised with edited `teaches` | `changed S004`, 1 | `rows=4 changed=0`, **0** | **FN** | medium |
| H1 | separator padding widened to two spaces | 0 | `rows=3 changed=0`, 0 | holds | — |
| H2 | trailing spaces after the row | 0 | `rows=3 changed=0`, 0 | holds | — |
| H3 | double space inside `teaches` | tradeoff | `changed S002 cells=teaches`, 1 | holds (byte-strict) | low |
| H4 | whole file converted to CRLF | 0 | `rows=3 changed=0`, 0 | holds | — |
| H5 | tab separators plus an edit | flag, 1 | `rows=2 changed=0`, **0** | **FN** | high |
| I1 | id `S00²` (superscript digit) | malformed, no traceback | `ValueError` traceback, exit **1** | wrong exit class | low |
| I2 | id `S04` (contract needs 3+ digits) | malformed | accepted, `rows=4 changed=0`, 0 | FN (format) | low |
| J1 | bad revision | `bad_rev`, 2 | `bad_rev`, 2 | holds | — |
| J2 | path deleted at rev | `missing_file`, 2 | `missing_file`, 2 | holds | — |

## Root causes (script line references)

1. **Deletions are never compared** (B1, B2, D1, D4). The loop at line 56 walks only ids present at `<rev>`, and
   ids in `first` that are absent from `now` are dropped. Renumbering is a deletion plus a fresh id whose baseline
   defaults to itself (`first.get(rid, now[rid])`, line 57), so it passes.
2. **Duplicates are collapsed by `setdefault`** (C1, C3). Line 32 keeps the first occurrence in file order, so a
   second row with the same id is invisible at `<rev>` and in history. `rows=` counts unique ids, not rows.
3. **Strict, silent line grammar** (F3, G1 to G5, H5, I2). Line 29 requires `| S` at column 0 and a final `|`.
   Line 30 splits on exactly `" | "`, and line 31 drops any row that does not yield 11 cells. A dropped row is
   neither reported nor counted. If every row is dropped (G5), the run ends `rows=0 changed=0`, exit 0. CORPUS.md's
   maintained parser accepts 0 to 3 leading spaces (`CORPUS.md:152`), and its census regex tolerates any spacing, so
   the check is stricter than the lane's own row definition and fails open when the two disagree.
4. **`--first-parent` history** (E1, E2). Line 51 never reads side-branch commits. In both scratch repos,
   `git log --first-parent -- corpus/SOURCES.md` lists only the base commit (plus `main touch` in E1) and the
   merge. The side commit that first published S004 is skipped, so the merge's edited text becomes the
   "first-published" baseline. The docstring (line 6) states first-parent order, but QUALITY 81 (`QUALITY.md:376`)
   claims "committed history".
5. **Malformed first publication** (G6). Same grammar as cause 3: a row the parser could not read when it was first
   published gets its baseline from the first commit it can read.
6. **`isdigit()` is not ASCII** (I1). It accepts `²`, after which `int()` at line 56 raises. The traceback exits 1,
   which the docstring (line 11) reserves for `changed>0`.

Escaped pipes hold: GFM `\|` contains no `" | "`, so the split never breaks inside it (F1, F2, F4). Whitespace at
the edges of a cell and around the separators holds because of `strip()` (H1, H2, H4). An internal double space is
flagged (H3). That matches a byte-strict reading of "keeps its first-published cells" and is a tradeoff, not a
defect; normalising it would also hide real whitespace edits inside code spans.

## Smallest safe correction (verified in scratch; exact old → new for the integration owner)

`cri_fixed.py` (sha256 `9558bc4c…07980c`) applies the change below to the script. Its results:

- It fixes all 19 cases marked FN above, plus I1 and I2. B1, B2, D1 and D4 now print `removed`. C1 prints
  `duplicate`. E1, E2, G1 to G3, G6 and H5 print `changed`. F3, G4, G5, I1 and I2 print `malformed`. Every one exits 1.
- The 15 holding cases are unchanged (`cases-fixed.out`).
- At the lane tip, `fc09f96c` and `ef9dbee1`, the `changed` lines are identical to the landed script's: 5, 6 and 6
  lines, with `removed=0 bad=0`.

C3 (a duplicate inside a historical commit) and H3 are unchanged by design.

```diff
@@ imports
+import re
 import subprocess
@@ constants
 MUTABLE = {"status", "recheck", "used-by"}
+ROW = re.compile(r" {0,3}\|[ \t]*S[0-9]")
+SEP = re.compile(r"(?<!\\)\|")
+ID = re.compile(r"S[0-9]{3,}")
@@ def rows(text):
-    out = {}
-    for line in text.split("\n"):
-        if line.startswith("| S") and line.rstrip().endswith("|"):
-            cells = [c.strip() for c in line.strip().strip("|").split(" | ")]
-            if len(cells) == len(NAMES) and cells[0][1:].isdigit():
-                out.setdefault(cells[0], cells)
-    return out
+    out, bad = {}, []
+    for n, line in enumerate(text.split("\n"), 1):
+        if not ROW.match(line):
+            continue
+        cells = [c.strip() for c in SEP.split(line.strip())]
+        if len(cells) != len(NAMES) + 2 or cells[0] or cells[-1] or not ID.fullmatch(cells[1]):
+            bad.append("malformed line=%d" % n)
+        elif cells[1] in out:
+            bad.append("duplicate %s line=%d" % (cells[1], n))
+        else:
+            out[cells[1]] = cells[1:-1]
+    return out, bad
@@ def main():
-    now = rows(show.stdout)
+    now, bad = rows(show.stdout)
+    for b in bad:
+        print(b)
     first = {}
-    log = git("log", "--first-parent", "--reverse", "--format=%H", rev, "--", PATH).stdout.split()
+    log = git("log", "--full-history", "--topo-order", "--reverse", "--format=%H", rev, "--", PATH).stdout.split()
     for c in log:
-        for rid, cells in rows(git("show", "%s:%s" % (c, PATH)).stdout).items():
+        for rid, cells in rows(git("show", "%s:%s" % (c, PATH)).stdout)[0].items():
             first.setdefault(rid, cells)
+    removed = sorted(set(first) - set(now), key=lambda x: int(x[1:]))
+    for rid in removed:
+        print("removed %s" % rid)
@@ summary
-    print("rows=%d changed=%d" % (len(now), changed))
-    return 1 if changed else 0
+    print("rows=%d changed=%d removed=%d bad=%d" % (len(now), changed, len(removed), len(bad)))
+    return 1 if changed or removed or bad else 0
```

The docstring and QUALITY 81 text must then match the new behaviour:

- Script line 6, old: `in the oldest commit (first-parent order of <rev>'s history of corpus/SOURCES.md) that carries the id, and compares`
  → new: `in the oldest commit (topological order of every commit in <rev>'s history of corpus/SOURCES.md) that carries the id, and compares`
- Script line 10, old: ``Prints one line per changed row (`changed <id> cells=<names>`) and a summary `rows=<n> changed=<k>`.``
  → new: ``Prints `malformed line=<n>`, `duplicate <id> line=<n>`, `removed <id>` and `changed <id> cells=<names>` lines and a summary `rows=<n> changed=<k> removed=<r> bad=<b>`.``
- Script line 11, old: `Exit 0 when changed=0, 1 when changed>0, 2 on a bad revision or a missing file.`
  → new: `Exit 0 when changed, removed and bad are all 0, 1 otherwise, 2 on a bad revision or a missing file.`
- `corpus/QUALITY.md:376`, old: ``row's first-published cells from committed history and must print `changed=0`, exit 0.``
  → new: ``row's first-published cells from committed history and must print `changed=0 removed=0 bad=0`, exit 0.``

Residual tradeoff of the correction [INFERENCE, untested]: if two parallel branches both add the same new id with
different text, the branch that comes first in topological order supplies the baseline, and the other branch's row
is reported `changed`. That is still a failing exit for a real violation, because ids are never reused
(`CORPUS.md:89`).

## Impacted axes

- Check validity (QUALITY 81 enforcement): high. It fails open on deletion, renumbering, duplicates and malformed
  rows, and passes vacuously on a schema change.
- Provenance claim: medium. QUALITY 81 says "committed history"; the script reads first-parent history only.
- Exit-code contract: low. A traceback shares exit 1 with a real finding.
- No impact on the C1 count or the round's admitted content: the lane's 28 historical versions parse cleanly, and
  the tip result is unchanged under the correction.
