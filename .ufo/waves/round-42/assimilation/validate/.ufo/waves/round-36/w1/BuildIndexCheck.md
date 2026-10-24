measured 2026-10-23T12:14:00Z

# BuildIndexCheck — round-36 wave 1

Target: round-35 spot-check routed defect 4 / lesson M4 (`git add -N .` in the lane).
Deliverable: a read-only bash gate that makes an index write detectable after each helper commit.

## 1. Artifact

| item | value |
|---|---|
| path | `/fast/scratch/hyaku/mori-r36/BuildIndexCheck/tools/mori-index-clean.sh` |
| sha256 | `8d694948a3146ba6ac09577fd351704005e15376c114016249a40922eaf1ade5` |
| size / lines | 7932 bytes / 242 lines, mode 0755 |
| interpreter | `#!/usr/bin/env bash`, bash 5.3.20, `set -o nounset -o pipefail`, `set -f` |

The L1 copies it into the lane `tools/`; I wrote nothing under the lane's `tools/`.

## 2. Interface as built

`bash tools/mori-index-clean.sh <repo>` (read-only check) and
`bash tools/mori-index-clean.sh --selftest` (sandbox self-test).

- stdout on a check: `MORI_INDEX_CLEAN staged=N intent_to_add=M`, then one
  `MORI_INDEX_CLEAN_PATH <path>` line per offending path (max 20), then
  `MORI_INDEX_CLEAN_MORE <k>` when the list was truncated.
- exit 0 = clean, exit 1 = not clean, exit 2 = usage error / not a git
  repository / git failure. Errors go to stderr as `MORI_INDEX_CLEAN_ERROR …`.
- Read-only: every git call runs under
  `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git --no-optional-locks`,
  plus `GIT_OPTIONAL_LOCKS=0`, so git never refreshes or rewrites `.git/index`.
  Measured: the lane `.git/index` sha256 is byte-identical before and after a run
  (`c8342a01c3aa387b8b01e585bf669976c68d64a1ce02044059b3dfc243176943`).

## 3. How intent-to-add is detected (the M4 case) — method chosen and shown

I measured three candidate methods against a sandbox repo (git 2.56.0):

| method | sees `git add -N newfile`? | why |
|---|---|---|
| `git diff --cached --name-only` | **no** | git skips intent-to-add entries in the cached diff; output was empty after `git add -N newfile` |
| `git ls-files --stage` vs `git diff --cached --diff-filter=A` | ambiguous | the intent-to-add entry carries the empty blob `e69de29…`, identical to a genuinely staged empty file |
| **`git status --porcelain=v2`** | **yes** | the path appears as a type-1 record with XY `.A` |

Chosen method: **porcelain**. The tool counts intent-to-add entries twice — once
from porcelain v1 (an intent-to-add path shows as XY `" A"`) and once from
porcelain v2 (type-1 record whose XY is `.A`) — and **refuses to report a
verdict (exit 2)** if the two counts disagree. The v2 count uses
`grep -c '^1 \.A '`, matching only type-1 records, so rename/copy records
(type 2) and unmerged records (type `u`) cannot inflate it.

Raw evidence, sandbox repo after `git add -N newfile`:
`git status --porcelain=v2 --untracked-files=no` → `1 .A N... 000000 000000
100644 000…0 000…0 newfile`; `git ls-files --stage` lists `100644
e69de29bb2d1d6434b8b29ae775ad8c2e48c5391 0	newfile`; `git diff --cached
--name-only` → no output. The `git diff --cached` blind spot is the load-bearing
fact for M4: a checker built only on it would report the `git add -N .` case as
**clean**. This tool does not.

## 4. Acceptance evidence

### 4a. `--selftest` output

```
$ bash /fast/scratch/hyaku/mori-r36/BuildIndexCheck/tools/mori-index-clean.sh --selftest
MORI_INDEX_CLEAN_SELFTEST pass=4 fail=0     # exit 0
```

The four arms, all run in a temp sandbox repo under `env -u GIT_DIR -u GIT_WORK_TREE
-u GIT_INDEX_FILE`, all passing:

| arm | setup | required | measured |
|---|---|---|---|
| clean | repo with one commit, no changes | exit 0, `staged=0 intent_to_add=0` | exit 0, `staged=0 intent_to_add=0` |
| intent-to-add | `git add -N newfile` | exit 1 | exit 1, `staged=0 intent_to_add=1` |
| staged | `git add tracked.txt` (modified tracked file) | exit 1 | exit 1, `staged=1 intent_to_add=0` |
| not a repo | plain directory | exit 2 | exit 2, `MORI_INDEX_CLEAN_ERROR not a git repository: …` |

The sandbox is removed on exit (0 leftover `/tmp/mori-index-clean.*` after a run).

### 4b. Run against the lane (read-only)

```
$ bash /fast/scratch/hyaku/mori-r36/BuildIndexCheck/tools/mori-index-clean.sh /home/vgpnk/Projects/shokunin/mori-shokunin
MORI_INDEX_CLEAN staged=0 intent_to_add=0
MORI_INDEX_CLEAN_PATH .ufo/waves/round-36/w1-spec.json
MORI_INDEX_CLEAN_PATH corpus/SOURCES.md
$ echo $?
1
```

**Read this carefully: the lane's git index is clean.** `staged=0` and
`intent_to_add=0` — no staged path and no intent-to-add entry in the lane
index. The exit code is 1 only because the spec's first condition
(`git status --porcelain --untracked-files=no` empty) is also not met: two
tracked files carry **unstaged worktree modifications** at this moment, and
the check reports them by path. Confirmed directly:
`git --no-optional-locks -C <lane> status --porcelain --untracked-files=no` →
` M .ufo/waves/round-36/w1-spec.json` and ` M corpus/SOURCES.md`;
`git --no-optional-locks -C <lane> diff --cached --name-only` → no output.

`.ufo/waves/round-36/w1-spec.json` was re-rendered by the L1 at 09:03 local and
`corpus/SOURCES.md` is being written by a sibling seat in this wave; both are
live, expected edits, not index writes. The run is idempotent, 0.038 s wall.

## 5. Additional behaviour measured (beyond the acceptance list)

| case | measured |
|---|---|
| `git add -N .` over 30 untracked files | `staged=0 intent_to_add=30`, exit 1, exactly 20 `…_PATH` lines + `MORI_INDEX_CLEAN_MORE 10` |
| staged rename | `staged=1`, exit 1, path reported as the new name |
| path containing spaces | reported whole — `-z` NUL-delimited parsing, no quoting damage |
| repo given as a subdirectory of a repo | works; paths reported relative to the repo root |
| untracked-only working tree | exit 0 (`--untracked-files=no` ignores untracked files) |
| missing directory / 0 args / 2 args | exit 2 (`MORI_INDEX_CLEAN_ERROR …` / usage line) |
| `bash -n` / `shellcheck -S warning` | syntax OK / clean (shellcheck 0.9.0, already installed) |

## 6. Note for the L1 — one semantic point worth deciding

The exit-0 condition is a conjunction of three predicates, one of which
(`status --porcelain --untracked-files=no` empty) is **broader than index
cleanliness**: it also fires on any unstaged worktree edit to a tracked file.
That is what makes today's lane run exit 1 with `staged=0 intent_to_add=0`.

I implemented the condition exactly as written — the frozen wording governs and
I did not narrow it. The two facts are separable in the output: the summary
line always states `staged` and `intent_to_add` separately, so a caller can key
on the index-specific part alone if the L1 wants the stricter reading. If the
gate is to fire only on index writes (what QUALITY 103's draft text describes:
"the lane git index holds no staged path and no intent-to-add entry"), the
condition should be the second and third predicates only. That is a
gate-semantics decision for the L1, not something I should change unilaterally.
**The tool satisfies the specified condition exactly; the ambiguity is in the
condition, not in the implementation.**

## 7. Drafts for the L1

```DRAFT gate-registry-row (routed defect 3 — the gate registry row this tool is missing)

SKILL.md, in the gate table, one row for the round-36 index-clean gate:

| gate | command | exit codes | binds |
|---|---|---|---|
| mori-index-clean | `bash tools/mori-index-clean.sh <repo>` | 0 clean, 1 staged or intent-to-add present, 2 error | QUALITY 103 |

Kind: gate (it has a fixture self-test, `--selftest`, and a shown ability to
fail: in a sandbox clone `git add -N <file>` makes it exit 1 — the self-test arm).
Registry note: this supersedes no earlier gate; round 35 had no such row, which
is why spot-check routed defect 3 named it.
```

```DRAFT quality-103-check (for the DraftQuality103 seat to reconcile against the built tool)

Check: `bash tools/mori-index-clean.sh /home/vgpnk/Projects/shokunin/mori-shokunin`
exits 0 after every lane helper commit, recorded in the round's dispatch log after
each `landed` line.
Shown able to fail: in a sandbox clone `git add -N <file>` makes it exit 1
(measured: exit 1, `staged=0 intent_to_add=1`).
Not covered: the exit-0 condition also requires
`git status --porcelain --untracked-files=no` to be empty, so an unstaged worktree
edit to a tracked file also exits 1 even though the index is clean.
```

## 8. Risks and blockers

- **Risk (small, the L1's to own):** the gate's exit-0 condition is broader
  than "index clean" (see §6). Run on the lane while a sibling seat has
  uncommitted tracked-file edits, it exits 1 with `staged=0 intent_to_add=0` —
  a true report about the worktree, a false alarm about the index.
- **Risk (method-bound):** the intent-to-add count relies on porcelain v1 and
  v2 both reporting intent-to-add entries. Both are reported by git 2.56.0
  (measured) and the tool cross-checks the two, exiting 2 rather than guessing
  if a future git changes one of them. The `git diff --cached` method was
  rejected because it cannot see intent-to-add at all.
- **No blocker.** Tool built, self-tested, run against the lane.
- **Tooling:** nothing installed or updated. `git 2.56.0`, `bash 5.3.20` and
  `shellcheck` were already present; no pacman/uv/npm/cargo transaction was performed.
- **Lane hygiene:** read-only throughout. No git or jj write in the lane or the
  fleet repo; the lane `.git/index` sha256 is unchanged
  (`c8342a01c3aa387b8b01e585bf669976c68d64a1ce02044059b3dfc243176943` before
  and after). The only lane file written is this report.

## 9. Verdict

VERDICT: the tool is built, shown able to fail on `git add -N`, and matches the
specified exit-code contract; the lane's own index is clean today
(`staged=0 intent_to_add=0`).

VERDICT: `git diff --cached --name-only` does **not** list intent-to-add
entries, so any M4 checker built on it alone would report the `git add -N .`
case as clean; this tool uses the porcelain records instead.

VERDICT: the lane run exits 1 solely because of two unstaged worktree
modifications to tracked files (`.ufo/waves/round-36/w1-spec.json`,
`corpus/SOURCES.md`), which the specified condition includes; the index itself
holds no staged path and no intent-to-add entry.

VERDICT: the spec's exit-0 condition conflates "index clean" with "working tree
clean"; the implementation follows the spec exactly and the summary line
exposes the index-specific counts separately.
