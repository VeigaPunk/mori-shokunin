# ConnW04Routing — routed-defect-6 (W04 duplicate URLs)

Axes: calibration (owner function), freshness (census receipt vs scored tip), adjacency (do not export this debt). C1 operability and C2 depth are not moved.

## Verdict

The standing 16 W04 lines are intra-mori historical pairs. None was introduced by a round-40 row. The seat prompt's predicate "owned by a non-mori source row" is false for all 16: `sources-census.sh` W04 (`scripts/sources-census.sh:643-645`) fires inside one registry when a later row repeats a normalized URL under a different scope cell. The first-seen owner is an earlier mori id in every case.

S229's normalized URL appears once as a registry row. On HEAD `ede486b7a09a` and the worktree that row is `corpus/SOURCES.md:235` (inside `## Registry`). At the scored tip `265a955cc67b` the same single row is `corpus/SOURCES.md:292`, after `## Leads (unopened)`, which validate classifies as E12.

`evidence/census-end.txt` is byte-identical to `evidence/census-start.txt` (`cmp` exit 0; both committed in `8d3badd`, parent `265a955`). That receipt does not witness the scored tip: a copy of the start census cannot show E12.

## Commands and outputs

Lane validate (worktree = HEAD; this is the census that matches the receipt):

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-10-24 --root /home/vgpnk/Projects/shokunin mori
```

stdout (exit 0), same 16 ids as `evidence/census-end.txt`, then `mori ok`. No S229 line. No E-code.

```
mori	W04	S035 duplicate url raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in across scopes
mori	W04	S037 duplicate url www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html across scopes
mori	W04	S073 duplicate url docs.python.org/3/library/pathlib.html across scopes
mori	W04	S074 duplicate url kubernetes.io/docs/concepts/architecture/controller across scopes
mori	W04	S075 duplicate url ftp.gnu.org/gnu/bash/bash-5.3.tar.gz across scopes
mori	W04	S076 duplicate url michaelfeathers.silvrback.com/characterization-testing across scopes
mori	W04	S147 duplicate url raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/docs/settings.md across scopes
mori	W04	S148 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c across scopes
mori	W04	S149 duplicate url man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html across scopes
mori	W04	S150 duplicate url raw.githubusercontent.com/systemd/systemd/v262/man/systemd.exec.xml across scopes
mori	W04	S166 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c across scopes
mori	W04	S168 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst across scopes
mori	W04	S201 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c across scopes
mori	W04	S218 duplicate url github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch across scopes
mori	W04	S220 duplicate url raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c across scopes
mori	W04	S228 duplicate url docs.python.org/3/library/os.path.html across scopes
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
exit=0
```

Scored-tip blob (`git show 265a955cc67b:corpus/SOURCES.md` to a temp file, then `validate --today 2026-10-24 --file`): the same 16 W04 lines, plus

```
file	E12	S229 row outside Registry section
exit=1
```

`--file` also printed a storm of E11 "missing used-by" lines. Those are an artifact: `resolve_targets` sets the lane dir to `dirname(file)/..` (`sources-census.sh:500-502`), which was the temp dir. The first such path, `corpus/lessons/2026-10-15-free-lunch-measurements-counter-baselines.md`, exists in the real lane (`test -f` → yes). The lane-rooted command above prints no E11. E12 does not depend on that dir.

Registry delta:

```
git diff --stat bb1f2457bb8d 265a955cc67b -- corpus/SOURCES.md
 corpus/SOURCES.md | 1 +
git diff --stat 265a955cc67b HEAD -- corpus/SOURCES.md
 corpus/SOURCES.md | 2 +-
```

`bb1f2457..265a955` inserts only the S229 row, at the file tail (line 292). `265a955..ede486b` (`round-40: repair S229 registry placement (E12: row inside ## Registry)`) deletes that tail line and inserts it after S228. Worktree vs HEAD is empty. `git grep -c executionmodel.html 265a955 -- corpus/SOURCES.md` → `1`. `git grep -n executionmodel.html HEAD` → `corpus/SOURCES.md:235`.

Entering tip `bb1f2457` already contains S228 at line 234 and does not contain `executionmodel.html`. S228's `opened=2026-10-24` is the same calendar day as S229; opened-date is not round membership.

## Owner table (worktree / HEAD)

Normalized URL via `url_of` (`sources-census.sh:600-605`): first `https?://` token, fragment and one trailing slash stripped, host lowercased. Owner = first registry row that puts that URL into `url_seen`. Warned id = the later row whose scope cell was not yet seen. All owners are mori rows. Line numbers are `corpus/SOURCES.md`.

| W04 id | line | owner | owner line | warned opened | teaches |
|---|---|---|---|---|---|
| S035 | 41 | S013 | 19 | 2026-10-20 | second scope, no supersedes |
| S037 | 43 | S015 | 21 | 2026-10-20 | second scope, no supersedes |
| S073 | 79 | S069 | 75 | 2026-10-21 | supersedes S069 |
| S074 | 80 | S071 | 77 | 2026-10-21 | supersedes S071 |
| S075 | 81 | S070 | 76 | 2026-10-21 | supersedes S070; status queued |
| S076 | 82 | S067 | 73 | 2026-10-21 | supersedes S067 |
| S147 | 153 | S101 | 107 | 2026-10-22 | supersedes S101 |
| S148 | 154 | S127 | 133 | 2026-10-22 | supersedes S127 |
| S149 | 155 | S128 | 134 | 2026-10-22 | supersedes S128 |
| S150 | 156 | S129 | 135 | 2026-10-22 | supersedes S129 |
| S166 | 172 | S127 | 133 | 2026-10-22 | rejected; third scope (after S148) |
| S168 | 174 | S082 | 88 | 2026-10-22 | rejected |
| S201 | 207 | S182 | 188 | 2026-10-23 | supersedes S182 |
| S218 | 224 | S188 | 194 | 2026-10-23 | supersedes S188 |
| S220 | 226 | S190 | 196 | 2026-10-23 | supersedes S190 |
| S228 | 234 | S226 | 232 | 2026-10-24 | supersedes S226; present at bb1f2457:234 |

S166's URL is also S148's; the first-seen owner is still S127. S148 and S166 are two warnings, not two owners.

## Sibling rows are not the W04 owner

Scan of the other 20 `*-shokunin/corpus/SOURCES.md` files with the same normalizer. Three of the 16 URLs also occur outside mori; thirteen do not. W04 never consults those files.

- `docs.python.org/3/library/pathlib.html` (S073, owner S069): `souji-shokunin/corpus/SOURCES.md:60` S040, opened 2026-10-20.
- `docs.python.org/3/library/os.path.html` (S228, owner S226): `chousa-shokunin/corpus/SOURCES.md:54` S044, opened 2026-10-21; `tameshi-shokunin/corpus/SOURCES.md:93` S084, opened 2026-10-21.
- `raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst` (S168, owner S082): `tsukuroi-shokunin/corpus/SOURCES.md:154` S148, opened 2026-10-22.

No sibling `SOURCES.md` contains `executionmodel.html`.

## S229 appears once

Normalized form `docs.python.org/3/reference/executionmodel.html` (fragment `#naming-and-binding` stripped):

- Registry, once: `mori-shokunin/corpus/SOURCES.md:235` on HEAD/worktree. This is the line that proves a single in-registry occurrence and that the lane validate above does not warn on it.
- Same bytes, wrong section, at the scored tip only: `corpus/SOURCES.md:292`.
- Not registry rows, so not a second census URL: `corpus/knowledge/conform-scope-r40.md:4`, `corpus/lessons/round-40.md:7`, and the fetched page copy `corpus/evidence/sources-r40/S229.src` (og:url line 9, canonical line 46, no fragment).

## Proposed move

Keep `ede486b`'s placement. Do not revert S229 to the scored-tip tail, and do not open another row or edit any of the 16 pairs. Re-derive `evidence/census-end.txt` with the lane-rooted validate at HEAD (or record that the committed receipt is the pre-S229 start census and that exit 0 holds only after the E12 repair). Do not route a fix at souji/chousa/tameshi/tsukuroi: their rows are not what W04 measures.

## Risks

- Reverting the move restores E12 and makes validate exit 1. The 16 W04 lines stay either way, so a "W04 unchanged" check alone misses the break.
- Reading census-end as a scored-tip witness hides that break. The frontier claim "census exit 0" is true on HEAD, not on `265a955` as committed.
- Calling the three sibling hits the owners would push an append-only mori supersession debt into other lanes (adjacency harm) and would still leave the 13 mori-only URLs unexplained.
- A `--file` re-run from a temp dir reprints E11 for the whole registry; that is not lane breakage.

## Verification already run

Lane validate exit 0 with the 16-line set above; `cmp` of census-start and census-end identical; `git diff --stat` of the two registry ranges; `git grep -c` = 1 at `265a955`; `git grep -n` = line 235 at HEAD; sibling SOURCES scan; `test -f` on the used-by path the temp-dir E11 named. No production file was edited. No tool installed.
