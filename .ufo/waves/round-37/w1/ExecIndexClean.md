# ExecIndexClean — round 37 wave 1 (executor)

- Seat: `mori-r37-w1-ExecIndexClean`, executor (leaf; no subagent dispatched, no labrat spawned).
- Date: 2026-10-23.
- Item attacked: **the index-clean gate's live check on the lane** — `bash tools/mori-index-clean.sh <lane>`
  must print `MORI_INDEX_CLEAN staged=0 intent_to_add=0` and exit 0.
- Method: read-only git/bash against the lane repo. The only file written is this report. No `git add/
  commit/push/fetch/reset/stash`, no mutating jj command, no `jj new/describe/commit`, no pacman, nothing
  installed. Scratch only under `/fast/scratch/hyaku/mori-r37/ExecIndexClean/` and `/tmp`.
- Environment measured: `git version 2.56.0`; `GNU bash, version 5.3.20(1)-release (x86_64-pc-linux-gnu)`;
  `jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5` (read-only use only: `jj status`, `jj log`,
  `jj config get`, `jj root`, `jj file list`).

## 1. The target command — required output

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && bash tools/mori-index-clean.sh /home/vgpnk/Projects/shokunin/mori-shokunin; echo EXIT=$?
MORI_INDEX_CLEAN staged=0 intent_to_add=0
EXIT=0
```

`staged=0 intent_to_add=0` and exit 0 — the acceptance condition is met.

Repeat stability (three further runs, same command, same lane):

```
MORI_INDEX_CLEAN staged=0 intent_to_add=0   run1 EXIT=0
MORI_INDEX_CLEAN staged=0 intent_to_add=0   run2 EXIT=0
MORI_INDEX_CLEAN staged=0 intent_to_add=0   run3 EXIT=0
```

## 2. Independent corroboration (not the tool's own counting)

```
$ git --no-optional-locks diff --cached --name-only | wc -l                          → 0
$ git --no-optional-locks status --porcelain=v2 --untracked-files=no | grep -c '^1 \.A '  → 0
$ git --no-optional-locks status --porcelain --untracked-files=no | grep -c '^ A'      → 0
$ git --no-optional-locks ls-files --debug | grep -c 'flags: 20004000'                → 0   (CE_INTENT_TO_ADD)
$ git --no-optional-locks ls-files -u | wc -l                                         → 0   (unmerged entries)
$ git --no-optional-locks ls-files -v | grep -vc '^H '                                → 0   (no skip-worktree/assume-unchanged)
$ git --no-optional-locks ls-files | wc -l                                            → 10405
$ git --no-optional-locks ls-tree -r --name-only HEAD | wc -l                        → 10405  (index == HEAD tree)
$ git --no-optional-locks ls-files --stage | awk '{print $3}' | sort -u               → 0     (stage 0 only)
```

The gate's own exit-2 guard (porcelain v1 vs v2 disagreement) did not fire, so the two independent
intent-to-add detectors agreed on 0.

Tip identity at the time of the check: `HEAD` = `1ae1d6d69282f6c4f51355308db6a4be9a8e3d42`
("round-37: late wave-1 reports …"), and `origin/master` = the same hash (tip pushed). The lane moved
underneath this seat during the run (`c31076e` → `1ae1d6d` → `30dfe70`), so the gate was re-run after each
observed move; the verdict did not change.

## 3. The tool is read-only with respect to the lane index (measured)

Index fingerprint before and after a gate run on the lane:

```
h0=$(sha256sum .git/index) ; m0=$(stat -c %Y .git/index)
bash tools/mori-index-clean.sh <lane>
h1=$(sha256sum .git/index) ; m1=$(stat -c %Y .git/index)
→ h0 == h1, m0 == m1   (index byte-identical, mtime unchanged)
```

The script's own `GIT_OPTIONAL_LOCKS=0` + `git --no-optional-locks` + `unset GIT_DIR/GIT_WORK_TREE/
GIT_INDEX_FILE` make this structural rather than incidental.

## 4. The tool can still fail — arms exercised in scratch (never in the lane)

Every arm below was run in `/fast/scratch/hyaku/mori-r37/ExecIndexClean/` on throwaway repos; the lane
was never touched.

| arm | setup | observed |
|---|---|---|
| self-test | `bash tools/mori-index-clean.sh --selftest` | `MORI_INDEX_CLEAN_SELFTEST pass=4 fail=0`, EXIT=0; no `/tmp/mori-index-clean.*` left behind |
| intent-to-add | `git add -N newfile` | `staged=0 intent_to_add=1` + `MORI_INDEX_CLEAN_PATH newfile`, EXIT=1 |
| staged modification | `git add tracked.txt` | `staged=1 intent_to_add=0` + path, EXIT=1 |
| staged new file (unborn HEAD) | `git init` + `git add f.txt` | `staged=1 intent_to_add=0`, EXIT=1 |
| ITA on unborn HEAD | `git add -N f.txt` | `staged=0 intent_to_add=1`, EXIT=1 |
| staged rename | `git mv a.txt b.txt` | `staged=1 intent_to_add=0` + `b.txt`, EXIT=1 |
| staged deletion | `git rm c.txt` | `staged=1 intent_to_add=0` + `c.txt`, EXIT=1 |
| ITA on a directory | `git add -N sub/` | `intent_to_add=2`, both paths listed, EXIT=1 |
| ITA + later content edit | `git add -N newfile` then append | still `intent_to_add=1`, EXIT=1 |
| filename with a space | `git add -N "sp ace.txt"` | counted and listed correctly (`-z` parsing), EXIT=1 |
| merge conflict (unmerged) | conflicting branches | `staged=1 intent_to_add=0`, EXIT=1 (not mis-reported as clean) |
| not a repository | path without `.git` | `MORI_INDEX_CLEAN_ERROR not a git repository: /tmp`, EXIT=2 |
| missing directory | `/nonexistent/path` | `MORI_INDEX_CLEAN_ERROR not a directory: …`, EXIT=2 |
| linked worktree (`.git` is a file) | `git worktree add` | `staged=0 intent_to_add=0`, EXIT=0 (correctly resolved) |
| hostile ambient env | `GIT_INDEX_FILE=/tmp/nope-index GIT_DIR=/tmp/nope-dir` | `staged=0 intent_to_add=0`, EXIT=0 (overrides correctly ignored) |
| minimal env | `env -i PATH=/usr/bin:/bin HOME=…` | `staged=0 intent_to_add=0`, EXIT=0 |
| run from another cwd | `cd /tmp && bash <abs>/tools/mori-index-clean.sh <lane>` | `staged=0 intent_to_add=0`, EXIT=0 |

## 5. Operational note — jj and the lane index (risk, not a defect)

The lane is jj-colocated with git as the backend (`.jj/repo/store/git_target` → `../../../.git`), and the
lane's jj config sets `snapshot.auto-track="none()"`. Measured consequence:

- A jj snapshot run with the **default** auto-track writes an intent-to-add entry into the git index
  (scratch arm: `git add`-less new file → `ls-files --debug` shows `flags: 20004000`, porcelain v2 shows
  `1 .A …`, and the gate then correctly reports `intent_to_add=1`, EXIT=1).
- With the lane's actual `snapshot.auto-track="none()"` setting, the same scratch arm leaves the git index
  untouched (`index_changed=no`, `flags: 20004000` count 0) and the gate stays `staged=0 intent_to_add=0`.

So the lane's clean index state currently depends on `snapshot.auto-track="none()"` staying in force. If a
future jj invocation ran with default auto-tracking while untracked files were present, the gate would
legitimately report `intent_to_add>0` — a true positive about the index, not a tool failure. `[INFERENCE]`
from the two scratch arms; the lane's own jj config value was read directly (`jj config get
snapshot.auto-track` → `none()`).

## 6. Observation against QUALITY 103 (outside my acceptance criterion — reported, not remediated)

`corpus/QUALITY.md:822` (QUALITY 103) requires two things: (a) the lane git index holds no staged path and
no intent-to-add entry after every lane helper commit, and (b) "the round's dispatch log records the check
after each `landed` line".

- (a) holds at the measured tip — §1 and §2.
- (b) does **not** hold for round 37: `.ufo/waves/round-37/dispatch-log.txt` contains two `landed` lines
  (`2026-10-23T16:59Z landed e57c58b5`, `2026-10-23T17:05Z landed bcf65505`) and **zero** occurrences of
  `staged=` or `index` (`grep -c "staged=" … → 0`, `grep -in "index" … → no match`). The comparable round-36
  log does carry them (`.ufo/waves/round-36/dispatch-log.txt:35,44,52`, e.g. "post-land checks: index clean
  staged=0 intent_to_add=0 exit 0 (QUALITY 103)").

Evidence:
```
$ grep -n "landed\|index\|staged=" .ufo/waves/round-37/dispatch-log.txt
7:2026-10-23T16:59Z  landed e57c58b5 — freeze + data (…)
13:2026-10-23T17:05Z  landed bcf65505 — receipts, measured outcome, (…)
$ grep -c "staged=" .ufo/waves/round-37/dispatch-log.txt
0
```

Severity: low — the criterion's first clause is satisfied and independently verified above; only the
dispatch-log *record* of the check is missing. This is a documentation/traceability gap in the L1's own
log, which I am not permitted to edit (lane is read-only for this seat; no remediation in the mori
province). Flagged for the L1's disposition.

## 6b. Live worktree dirt observed (unstaged, not index state)

At the end of the run the lane carried concurrent unstaged worktree edits from other seats / the L1
(not mine — this seat wrote only its report, which is untracked and therefore absent from porcelain
`--untracked-files=no`):

```
$ git --no-optional-locks status --porcelain --untracked-files=no
 M .ufo/waves/round-37/contract.md
 M .ufo/waves/round-37/count-c1.py
 M .ufo/waves/round-37/count-c2.py
 M .ufo/waves/round-37/evidence/drift-live-r37.txt
 M LOG.md
 M SCORECARD.md
 M corpus/README.md
 M corpus/knowledge/source-drift-hardening-r37.md
 M corpus/lessons/round-37.md
```

All are ` M` (worktree side modified, index side unmodified) — porcelain v2 confirms index side unchanged
(`1 .M N...`, both object ids equal). Per the tool's documented round-36 semantics ("unstaged worktree edits
to tracked files are not index state and do not count"), these do not make the gate dirty, and the gate
correctly still reports `staged=0 intent_to_add=0` EXIT=0. Recorded for transparency: the index is clean;
the worktree is not, and the difference is the tool's intended one.

## 7. Scope discipline

- Files written: exactly one — this report,
  `.ufo/waves/round-37/w1/ExecIndexClean.md`.
- No lane file was edited, no lane git index entry was created, no git/jj mutating command was run in the
  lane (`jj` was used read-only: `status`, `log`, `config get`, `root`, `file list`).
- Scratch artifacts live only under `/fast/scratch/hyaku/mori-r37/ExecIndexClean/` and `/tmp`
  (`/tmp/tip-tool.sh`, a read-only `git show` dump).
- No tools were installed or upgraded in this seat, so there is nothing to record on the tooling channel.

## Verdict

The target command prints `MORI_INDEX_CLEAN staged=0 intent_to_add=0` and exits 0, corroborated by six
independent index probes, stable across three re-runs and across the lane's tip moving twice underneath the
check, with the tool provably leaving `.git/index` byte-identical. The tool is shown able to fail (exit 1
for staged / intent-to-add / unmerged entries, exit 2 for non-repos and missing paths) in scratch arms.

VERDICT: PASS
