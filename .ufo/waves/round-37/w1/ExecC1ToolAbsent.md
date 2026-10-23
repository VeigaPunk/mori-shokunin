# ExecC1ToolAbsent — C1 counter on a rev that predates the append-only tool

Scratch: `/fast/scratch/hyaku/mori-r37/ExecC1ToolAbsent/`
Lane repo read-only throughout; no mutation of lane files; nothing installed (no pacman, no uv, no binaries).

## Assignment

Find the oldest lane rev that lacks `tools/mori-sources-appendonly.py` and run
`python3 .ufo/waves/round-37/count-c1.py <rev>`. PASS iff the `tool_absent` path prints
`C1=unmet` and exits 1 — not a crash.

Item attacks: **the C1 counter's discrimination of a missing gate tool from a failed measurement**
(i.e. that "the tool does not exist at rev R" is a typed, fail-closed verdict, not an
unhandled exception and not a silent pass).

## Locating the rev

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --diff-filter=A --format='%H %ci' -- tools/mori-sources-appendonly.py
bf0df77fee4b6ef54a90aea09335c7617f125151 2026-10-23 15:20:10 -0300

$ git log --all --diff-filter=A --format='%H %ci' -- tools/mori-sources-appendonly.py
1a5f7c1f9da0158695b2d8199193bbb9d427eaf4 2026-10-23 15:20:10 -0300
3db97e6ae1677243c8b3197e42c3de4d576377da 2026-10-23 15:20:10 -0300
bf0df77fee4b6ef54a90aea09335c7617f125151 2026-10-23 15:20:10 -0300
4ea7bd6198c62eced8e44f7ff39a73ef0a15e9da 2026-10-23 09:51:48 -0300
```

Only `bf0df77f` is on HEAD's history (the other three name as `jj/keep/...`: two round-36
snapshot ids sharing its timestamp and the non-ancestor wip save `4ea7bd61`).

```
$ git log -1 --format='%H %P %s' bf0df77fee4b6ef54a90aea09335c7617f125151
bf0df77fee4b6ef54a90aea09335c7617f125151 5842dc045bb3d3b7aa2bdaaf462dcff536358444 round-36: C1/C2 data — drift probe tool, append-only gate + index-clean tools, SOURCES S205-S220, QUALITY 103-105, SKILL rows, wave-1 evidence, attempt-2 log

$ git ls-tree --name-only 5842dc045bb3d3b7aa2bdaaf462dcff536358444:tools | grep -i appendonly
(no match; 29 tool files at that rev)
```

Target rev = **`5842dc045bb3d3b7aa2bdaaf462dcff536358444`** (parent of the add commit, the earliest
rev on the lane's first-parent line at which the tool does not exist yet).

## Measurement (primary)

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ python3 .ufo/waves/round-37/count-c1.py 5842dc045bb3d3b7aa2bdaaf462dcff536358444; echo "EXIT=$?"
P-C1: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed, and exactly the truth's per-id `changed`/`deleted` lines, on each of 24 sandbox SOURCES.md histories drawn at run time, on the lane's own history (rev 6bd57097, round base f10a320d) where the independent oracle lists at least one id, and on one run-time-drawn challenge history presented in real-arm clothing (lane path, lane git identity, lane title); and the same counter rejects all three negative fixtures: a real-arm memoizer, a constant printer, and a summary-only printer.
tool_absent
C1=unmet
seed=5702160280404694033
EXIT=1
```

Repeatable and seed-independent (the verdict does not depend on the drawn seed):

```
$ python3 .ufo/waves/round-37/count-c1.py 5842dc045bb3d3b7aa2bdaaf462dcff536358444 --seed 1
...
tool_absent
C1=unmet
seed=1
EXIT=1
real 0m0.037s   user 0m0.080s   sys 0m0.025s

$ python3 ... count-c1.py 5842dc045bb3d3b7aa2bdaaf462dcff536358444 > absent-run.txt 2> absent-run.err
EXIT=1 ; stderr bytes = 0
```

The same run at the lane root rev (`ec0664e1ae4d1aa94ed7a960bbc87db11c8b354c`) gives
`tool_absent / C1=unmet / EXIT=1`, so the verdict is the same anywhere the tool was never added.

## Discrimination matrix (what makes this a verdict, not a crash)

| Probe | Command tail | stdout | stderr | exit |
|---|---|---|---|---|
| tool absent at rev | `count-c1.py 5842dc04…` | `tool_absent`, `C1=unmet` | empty | **1** |
| tool absent at root rev | `count-c1.py ec0664e1…` | `tool_absent`, `C1=unmet` | empty | **1** |
| unresolvable rev | `count-c1.py deadbeef…` | predicate only | `counter setup error: git rev-parse --verify … failed` | 2 |
| `--tool` missing path | `--tool /nonexistent/tool.py` | predicate only | `counter setup error: no such tool file: …` | 2 |
| `--tool` a directory | `--tool tools` | predicate only | `counter setup error: no such tool file: tools` | 2 |
| tool present at tip (retained receipt, not my run) | `evidence/c1-after-tip.txt` | full arms, `negative memo-n1.py rejected`, `C1=met` | — | 0 |

Absence is judged **from the rev's tree, never from the worktree**: the file exists on disk at the
lane tip (`git cat-file -e e57c58b:tools/mori-sources-appendonly.py` → exists; git's own message
"exists on disk" confirms the worktree copy is present), yet the run at `5842dc04` still prints
`tool_absent`. Direct confirmation of the two sides of the boundary:

```
$ git show 5842dc045bb3d3b7aa2bdaaf462dcff536358444:tools/mori-sources-appendonly.py; echo "EXIT=$?"
fatal: path 'tools/mori-sources-appendonly.py' exists on disk, but not in '5842dc045bb3d3b7aa2bdaaf462dcff536358444'
EXIT=128

$ git show bf0df77f:tools/mori-sources-appendonly.py | head -1   # 499 lines
#!/usr/bin/env python3
```

No cost or side effect on the absent path: the branch returns before `_scratch_parent()`, so no
sandbox/negative scratch is created. `/tmp/mori-c1-tool-*` directory count was 3 before and 3 after
my run (the dirs present belong to concurrently running sibling counters; one appeared and vanished
during the window), and the one `mori-c1-tool-<rand>` dir this path does create is removed by its
`finally: shutil.rmtree(tool_dir)`.

## Risks / observations (advisory, not defects for this item)

1. `count-c1.py:880-885` keys `tool_absent` on `git show <rev>:<path>` returning non-zero, not on a
   path-existence test. Any *other* `git show` failure (shallow clone missing the blob, unreadable
   object, corrupt pack) would also print `tool_absent`/`C1=unmet`. The direction is fail-closed
   (unmet, never met), so it cannot inflate C1, but the diagnostic string can mislabel an
   environmental fault as "the tool was never added".
2. `--tool <existing directory>` reports `no such tool file: tools` — message is imprecise for a
   path that exists but is not a regular file (exit 2 is correct).
3. `/fast/scratch/hyaku/mori-r37` and `/tmp` are shared with concurrently running seats; scratch
   remnants there cannot be attributed to one run. My own run's footprint is empty (see above).

## Verdict

The `tool_absent` path at the oldest rev lacking the tool (`5842dc045bb3d3b7aa2bdaaf462dcff536358444`,
and equally at the root rev) prints `tool_absent` then `C1=unmet` on stdout and exits **1**, with
empty stderr — a typed fail-closed verdict, not a crash, and not reachable as a pass. No fabricated
"met" is produced by a missing tool, and the surrounding failure modes (bad rev, bad `--tool`) are
distinguished by exit 2.

VERDICT: PASS
