measured 2026-10-23T12:22:10Z

# BuildAppendTool — mori round 36 wave 1 (C2 gate: `tools/mori-sources-appendonly.py`)

Scope: write the C2 append-only gate to the scratch path below; the L1 copies it into the lane.
No lane file was edited by this seat except this report. No git/jj write was run in the lane.

## Deliverable

- File: `/fast/scratch/hyaku/mori-r36/BuildAppendTool/tools/mori-sources-appendonly.py`
- sha256: `915527a7d2f553740ed3ab0166669031f19ce2de6b2fec8501208f97244cfc89`
- 499 lines, 20887 bytes, mode 0755, Python 3 stdlib only (`argparse os re shutil subprocess sys tempfile`).
- Promoted from `.ufo/waves/round-35/check-sources-appendonly.py` (read-only source, unchanged in the lane):
  the row-identity rule, the `supersedes` disposition and the endpoint-comparison idea are kept; the
  output format, the `deleted` arm, the summary line, the exit codes and the fixture self-test are
  new, per contract.md "C2 tool interface".

VERDICT: tool written to the named scratch path; sha256 `915527a7d2f553740ed3ab0166669031f19ce2de6b2fec8501208f97244cfc89`

## What the tool implements (contract.md "C2 tool interface")

- CLI: `mori-sources-appendonly.py <rev> [--repo DIR] [--round-base REV] [--path P]`, default path
  `corpus/SOURCES.md`, default repo the cwd. Plus `--selftest`.
- Header-position columns: the header row is located by its first cell (`id`, >=5 columns) and every
  column is taken by its position in that header; cells are compared **stripped**, so whitespace
  padding is not a change. Immutable = every column but `status`, `recheck`, `used-by`
  (tool: `COLUMNS`, `MUTABLE`, `immutable_indices`, `imm_key`).
- Row identity is the id (`S###`), never the line position; the per-id walk keys on `cells[0]`.
- `ids` = rows present at `<rev>` whose immutable cells differ from the cells the id held in the
  **first** ancestry commit that carried it (endpoint comparison) — `first` map built while walking
  `git log --reverse <rev> -- <path>`.
- `deleted` = ids carried by some ancestry commit of `<rev>` and absent at `<rev>` (the round-35 gap
  QUALITY 102 declared).
- `superseded` = ids in `ids` for which a row present at `<rev>` has a `teaches` cell opening
  `supersedes S###` (first superseder wins). Supersession is a disposition, never a discharge.
- `round_changed` = ids whose immutable cells changed, or which were deleted, in any commit of
  `REV..<rev>` that touches the path. A changed-back id inside the range is listed (the change is a
  fact of the round even when the endpoint matches the first cells).
- `appendonly_violations` = len(ids) + len(deleted).
- Output, in order: `changed <id> superseded_by=<id or ->` per changed id, `deleted <id>` per deleted
  id, then the summary
  `appendonly_violations=N ids=[...] deleted=[...] superseded=[...] round_changed=[...]`
  (ids sorted, comma-separated, no spaces; `round_changed=[]` when `--round-base` is absent).
- Exits: 2 on any git or parse error (bad rev, absent path, missing header, git failure); with
  `--round-base`, 1 iff `round_changed` is non-empty, else 0; without `--round-base`, 1 iff `ids` or
  `deleted` is non-empty, else 0.
- Read-only: the only git verbs used are `rev-parse`, `log`, `show` (`grep -n '"log"\|"show"\|"rev-parse"'`
  on the file: lines 91/107/174/182/230/232). No `rev-list` (the range is taken from
  `git log --format=%H <base>..<rev>`), no writes, no network, no clone. The caller's `GIT_DIR`,
  `GIT_WORK_TREE`, `GIT_INDEX_FILE`, `GIT_OBJECT_DIRECTORY`, `GIT_ALTERNATE_OBJECT_DIRECTORIES`,
  `GIT_COMMON_DIR` are stripped from the child environment so `-C <repo>` addresses the repository
  that was asked for (`_clean_env`).

## Acceptance evidence

### 1. `--selftest`

```
$ python3 tools/mori-sources-appendonly.py --selftest
MORI_SOURCES_APPENDONLY_SELFTEST pass=8 fail=0
(exit 0)
```

Eight sandbox repos are built in a temp dir (`tempfile.mkdtemp`, removed in a `finally`); each is
initialised with `git init -q` plus local `user.name`/`user.email`/`commit.gpgsign=false` under an
environment with `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE`/`GIT_OBJECT_DIRECTORY`/
`GIT_ALTERNATE_OBJECT_DIRECTORIES`/`GIT_COMMON_DIR` removed. Each case is driven **through the CLI**
(`HEAD --repo <sandbox> --round-base <sha>` as a child process), so the exit code and the printed
lines are what is checked, not an internal function. Cases and their hand-written expectations:

| case | fixture | expected |
|---|---|---|
| clean history | append one row | ids=[], deleted=[], round_changed=[], exit 0 |
| mutable-only edit | `status` cell changed | ids=[], round_changed=[], exit 0 |
| immutable edit | `anchor` cell changed | ids=[S001], round_changed=[S001], exit 1 |
| changed-back inside the round | edit, then revert | ids=[], round_changed=[S001], exit 1 |
| deletion | row removed | deleted=[S002], round_changed=[S002], exit 1 |
| superseding row | edit + new row `supersedes S001` | ids=[S001], superseded=[S001], `superseded_by=S002`, exit 1 |
| row reorder | rows swapped | ids=[], round_changed=[], exit 0 |
| whitespace padding | cells padded with spaces | ids=[], round_changed=[], exit 0 |

Each case also asserts: exactly one summary line matching the counter's `SUMMARY_RE` shape, the
per-id lines match `^changed S\d{3} superseded_by=(\S+)$` / `^deleted S\d{3}$`, and
`violations == len(ids)+len(deleted)`.

### 2. Round run on the lane

```
$ python3 tools/mori-sources-appendonly.py 6bd57097 --repo /home/vgpnk/Projects/shokunin/mori-shokunin --round-base f10a320d
changed S041 superseded_by=-
changed S044 superseded_by=-
changed S051 superseded_by=-
changed S062 superseded_by=-
changed S064 superseded_by=-
changed S069 superseded_by=S073
changed S179 superseded_by=-
changed S180 superseded_by=-
changed S181 superseded_by=-
changed S182 superseded_by=S201
changed S183 superseded_by=-
changed S184 superseded_by=-
changed S185 superseded_by=-
changed S186 superseded_by=-
changed S188 superseded_by=-
changed S189 superseded_by=-
changed S190 superseded_by=-
changed S193 superseded_by=S202
appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
(exit 1)
```

### 3. Full-history run on the lane

```
$ python3 tools/mori-sources-appendonly.py 6bd57097 --repo /home/vgpnk/Projects/shokunin/mori-shokunin
... (the same 18 "changed" lines) ...
appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[]
(exit 1)
```

### 4. Frozen counter (optional scoring)

```
$ timeout 900 python3 .ufo/waves/round-36/count-c2.py 6bd57097 --tool /fast/scratch/hyaku/mori-r36/BuildAppendTool/tools/mori-sources-appendonly.py
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /fast/scratch/hyaku/mori-r36/BuildAppendTool/tools/mori-sources-appendonly.py
blind arm: 24/24 sandbox histories matched the hidden truth (3.1s; coverage: deletions=22 changed-back=15 superseded=8)
real arm: pass (0.6s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
C2=met
seed=7958196063050355317
(counter exit 0)
```

Replayed with fixed seeds 1, 2, 3, 7, 99, 4242, 555, 2024, 31337 and one random draw: every run
printed `blind arm: 24/24` and `real arm: pass` and `C2=met` (exit 0). No seed produced a mismatch.

VERDICT: scored `C2=met` under the frozen counter (`.ufo/waves/round-36/count-c2.py`, sha256 `c7edaacf…`)

## Notes the L1 should know

- The lane's own history has **no deleted rows** at `6bd57097` (`deleted=[]`), and the 18 in-place
  immutable edits are the round-35 debt named in `corpus/lessons/round-35-verifier-spotcheck.md` §6.2
  (15 ids changed before round 34, plus S069 — and the 18 here also cover S179–S190, S182, S193 and
  S041/S044/S051/S062/S064). `superseded=[S069,S182,S193]` is the subset that already has a
  `supersedes` row (S073, S201, S202). The remaining 15 ids still owe a supersede row or a named
  ruling; this gate reports them, it does not discharge them.
- `round_changed=[S182,S193]` for `f10a320d..6bd57097` agrees with the round-35 closure's independent
  re-derivation (`round-35-verifier-spotcheck.md` §2, "the compared cells change only for S182 … and
  S193").
- The gate is a **gate**, not a probe: it exits 1 on a violation, so it can be wired into a CI step
  as-is. Registration as a gate in `SKILL.md` (round-35 §6.3) is outside this seat's write scope; the
  sibling `w1/DraftSkillRows.md` owns the registry-row draft.
- The exit rule with `--round-base` is "1 iff `round_changed` is non-empty" — the counter's blind arm
  expects exit 0 in the histories where `ids` is non-empty but every change predates the round base
  (4 of 24 such histories at seed 31337, probed with the counter's own `build_sandbox`). The
  no-`--round-base` exit rule is "1 iff `ids` or `deleted` is non-empty". Both are the contract's
  wording; the tool implements them literally.

## Risks and blockers

- None blocking. Risk: the tool reads only committed bytes (`git show <rev>:<path>`), so an
  uncommitted edit in the worktree is invisible to it — intended for a gate that runs on a revision.
- Risk: `--path` is honoured but only one path per run; a registry split across files is out of
  scope for this contract.
- The counter's blind arm is the only independent truth available; the tool's self-test expectations
  are hand-written from the contract, so the two checks are not the same oracle.

## Tooling

No package was installed or updated by this seat (the tool is stdlib-only Python 3; no new
dependency was needed). No pacman, uv, cargo or npm transaction was run.

## Handoff draft

```
DRAFT tools/mori-sources-appendonly.py
copy /fast/scratch/hyaku/mori-r36/BuildAppendTool/tools/mori-sources-appendonly.py
  -> <lane>/tools/mori-sources-appendonly.py
sha256 915527a7d2f553740ed3ab0166669031f19ce2de6b2fec8501208f97244cfc89
mode 0755, 499 lines, Python 3 stdlib only
receipt: python3 tools/mori-sources-appendonly.py --selftest
         -> MORI_SOURCES_APPENDONLY_SELFTEST pass=8 fail=0 (exit 0)
```
