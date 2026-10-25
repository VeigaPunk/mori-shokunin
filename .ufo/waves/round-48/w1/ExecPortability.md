# ExecPortability — round 48 w1: host-path portability count

Seat: ExecPortability (leaf; godspeed). Assignment: `considerthese/2026-10-25.md` suggestion 2 as a counting command — count committed instruments containing an absolute `/home/vgpnk` path, at the round-48 entering tip and at the previous round's entering tip, and check the round-48 instruments add none.

Scope as assigned: files tracked under `tools/` and under `.ufo/waves/round-*/` at the given revision that are `*.py` or `*.sh`. Matches are literal (fixed-string) occurrences of `/home/vgpnk` (`grep -F`), i.e. the absolute host path as a substring. All git commands read-only (`ls-tree`, `grep`, `show`, `cat-file`, `ls-files`); no repo state mutated, no tools installed (nothing was needed).

## Command (run in lane root `/home/vgpnk/Projects/shokunin/mori-shokunin`)

```bash
# 1. enumerate in-scope files at revision
git ls-tree -r --name-only <rev> -- tools/ .ufo/waves/round-*/ | grep -E '\.(py|sh)$' > .scratch/r48-ExecPortability/<rev>-files.txt

# 2. find which contain the literal absolute host path
cat .scratch/r48-ExecPortability/<rev>-files.txt \
  | xargs git grep -l -F '/home/vgpnk' <rev> -- \
  | sed 's/^[^:]*://' > .scratch/r48-ExecPortability/<rev>-hits.txt

# 3. counts
wc -l .scratch/r48-ExecPortability/<rev>-hits.txt                 # total
awk -F/ '$1=="tools"{t++} END{print t}' .scratch/r48-ExecPortability/<rev>-hits.txt   # tools/ alone
```

## Results

| revision | meaning | in-scope py/sh files | hits | tools/ alone |
|---|---|---:|---:|---:|
| `e5dbac05459887d9597ea5d1da0d8e3d024e0d17` | round-48 entering tip (round 47 closure) | 885 | **395** | **3** |
| `2d85e33d14198d388fd3cda9cc15ec07e57e7a53` | previous round's entering tip (round-47 baseline) | 883 | **395** | **3** |

Day-to-day change between the two entering tips: **0** (hit sets identical; `diff` of the two stripped hit lists is empty).

### List grouped by directory (e5dbac05; identical at 2d85e33)

| directory | hits |
|---|---:|
| `.ufo/waves/round-20` | 113 |
| `.ufo/waves/round-16` | 64 |
| `.ufo/waves/round-13` | 53 |
| `.ufo/waves/round-17` | 21 |
| `.ufo/waves/round-40` | 19 |
| `.ufo/waves/round-42` | 16 |
| `.ufo/waves/round-38` | 13 |
| `.ufo/waves/round-23` | 12 |
| `.ufo/waves/round-14` | 11 |
| `.ufo/waves/round-15` | 11 |
| `.ufo/waves/round-41` | 8 |
| `.ufo/waves/round-31` | 7 |
| `.ufo/waves/round-28` | 5 |
| `.ufo/waves/round-30` | 5 |
| `.ufo/waves/round-37` | 5 |
| `.ufo/waves/round-21` | 4 |
| `.ufo/waves/round-32` | 4 |
| `.ufo/waves/round-33` | 4 |
| `.ufo/waves/round-27` | 3 |
| `.ufo/waves/round-29` | 3 |
| `.ufo/waves/round-36` | 3 |
| `.ufo/waves/round-39` | 3 |
| `.ufo/waves/round-26` | 2 |
| `.ufo/waves/round-43` | 2 |
| `.ufo/waves/round-35` | 1 |
| `tools/` | 3 |
| **total** | **395** |

### `tools/` alone (count 3 — the same three the 2026-10-25 considerthese names)

- `tools/mori-blind-check.sh`
- `tools/mori-misroot-sweep.py`
- `tools/mori-round17-context-check.py`

## Round-48 instruments add none

- Neither counter exists at `e5dbac05`: `git ls-tree -r --name-only e5dbac05 -- .ufo/waves/round-48/` lists **0** entries (the round-48 directory is not in that tree), so they contribute nothing to the count at the entering tip.
- Both counters are tracked at the freeze commit `4387cf94` and in the working tree. `grep -Fn '/home/vgpnk' .ufo/waves/round-48/count-c1.py .ufo/waves/round-48/count-c2.py` exits 1 with **no matches** — neither contains the absolute host path. If added to the tree, they would add **0** files to the count.

## Verification / cross-checks

- No in-scope filename contains whitespace (`grep -cE '[[:space:]]'` on the file list → 0), so the `xargs`/`--` handoff is lossless.
- Completeness cross-check: `git grep -l -F '/home/vgpnk' e5dbac05 -- tools/ .ufo/waves/round-*/` on **all** tracked files (5188 hits, incl. out-of-scope md/txt) intersected with the py/sh enumeration: `comm` shows 0 py/sh files missing from the filtered set and 0 extra — the 395 count is complete and exact.
- Both revisions' count outputs were produced by the same pipeline; identical sets confirm the day-to-day delta of 0.
- Host read-only; no credentials/private material involved. No tools installed or updated (none required).

## Scratch artifacts

`.scratch/r48-ExecPortability/` holds `e5-files.txt`, `e5-hits.txt`, `e5-hits-stripped.txt`, `e5-all-hits.txt`, `2d-files.txt`, `2d-hits.txt`, `f1`, `f2` used to derive the numbers above.

## Files changed

- `.ufo/waves/round-48/w1/ExecPortability.md` (this report). No other files written or modified; no lane, fleet, git, or jj state touched.
