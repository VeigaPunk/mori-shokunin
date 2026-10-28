# Mo60Executor56 — dead-name census (SCORECARD.md, three pinned revisions)

Seat: Mo60Executor56 (leaf, read-only). No commits, no VCS mutation, no fleet/sibling writes.
Lane: /home/vgpnk/Projects/shokunin/mori-shokunin. Scratch: /fast/scratch/hyaku/mori-r60/Mo60Executor56 (TMPDIR set there; cleaned below).

## Answer

| name | at entering `ddfb12f` | at amended freeze `ac496c7` | at tip `b3c2561` |
|---|---|---|---|
| `c1-entering.txt` | 1 | 1 | 1 |
| `c2-entering.txt` | 1 | 1 | 1 |

Tip occurrences carrying the `r60-correction:` marker: **2 of 2** — `c1-entering.txt` 1/1 (line 2950), `c2-entering.txt` 1/1 (line 2951). Each marker sits on the same SCORECARD line/cell as the occurrence, so "occurrence carries marker" is exact, not inferred.

Counts are identical at all three revisions: the dead names were never removed; they are retained only inside the `r60-correction:` quotations that name them as dead and re-point to the committed control receipts.

## Revisions pinned

- entering: `ddfb12fb0838b4307c445194a844f0c4b1950195` (resolved)
- amended freeze: `ac496c7cde8cad965079858accae3bedfe4a73f2` (resolved)
- tip at census: `b3c256138f00c704d5aa56eb0332d74506502ef2` ("round-60: move S561-S564 rows into the Registry table (census E12 fix)"), re-verified unchanged after all reads; `git status --porcelain SCORECARD.md` empty, so the pinned `git show` content equals the worktree content (both md5 `b5996f3ed73102a9db7fb09dbed9a5c5`).
- All three blobs are 2966 lines.

## Commands and outputs (exact, read-only)

```
$ git show <rev>:SCORECARD.md | grep -c 'c1-entering\.txt'   # per rev
$ git show <rev>:SCORECARD.md | grep -c 'c2-entering\.txt'
$ git show <rev>:SCORECARD.md | grep -c 'r60-correction:'

ddfb12f c1=1 c2=1 marker=0
ac496c7 c1=1 c2=1 marker=0
b3c2561 c1=1 c2=1 marker=2
```

Occurrence (not just line) count cross-check on materialized blobs — `grep -o '<pat>' file | wc -l` gave 1/1/1 for each name at each revision, i.e. one occurrence per matching line; no multi-occurrence lines.

Line pointers (identical at all three revisions; `grep -n` on `git show <rev>:SCORECARD.md`):

```
ddfb12f  2950:| C1: pinned `tools/mori-register-check.py` (sha `38b733d8…`) ...
ddfb12f  2951:| C2: pinned `tools/mori-settlement-scan.py` (sha `4c04bf21…`) ...
ac496c7  2950:| C1: ...      2951:| C2: ...
b3c2561  2950:| C1: ...      2951:| C2: ...
```

Exact tip marker text (`grep -o` on the tip blob):

```
r60-correction: the r59 report and this cell cited a dead name `c1-entering.txt`; the committed control receipt is `control-c1-do-nothing.txt`
r60-correction: the r59 report and this cell cited a dead name `c2-entering.txt`; the committed control receipt is `control-c2-do-nothing.txt`
```

Per-name marker adjacency (occurrence line filtered for the marker): `c1-entering.txt` → 1, `c2-entering.txt` → 1.

Attribution: the marker text was introduced by `398d3225` ("round-60: land C1 data — … SCORECARD r60-correction re-pointing …"), per `git log --oneline -S'r60-correction:' -- SCORECARD.md` (single commit). `git diff --stat ac496c7..b3c2561 -- SCORECARD.md` = `1 file changed, 2 insertions(+), 2 deletions(-)`, matching the two in-place annotated cells (2950, 2951); the later `b3c2561` commit moved S561–S564 rows without touching these lines.

## Notes / residual risk

- No `c1-entering`/`c2-entering` variant occurrences besides the two quoted dead names; `control-c1-tool-v2-entering.txt` on line 2606 does not match `c1-entering\.txt` and was correctly excluded.
- Tip may still move after this census; any re-verification must re-pin `git rev-parse HEAD` and re-run the three `git show` pipelines. The three counts are revision-stable across every commit observed here, so movement between `ac496c7` and the tip cannot change them unless the annotated cells are edited.
- No tool installs or updates were needed. Scratch cleaned; no receipts required beyond this report.
