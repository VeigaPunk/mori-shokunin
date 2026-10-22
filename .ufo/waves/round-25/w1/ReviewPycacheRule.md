# ReviewPycacheRule: C1 item D4, the `tools/__pycache__/` ignore rule

Seat: `MoriR25.ReviewPycacheRule` (reviewer, leaf; no subagents; no lane writes except this file).
Claim: `.ufo/waves/round-25/contract.md:22` (D4 row); hygiene row `contract.md:111-119`.
Tip reviewed: HEAD `6a92d5e` (2026-10-22 07:09:22 -0300). HEAD moved during review. It was `129832e` (06:58:30) when I started; `09f55b6` (07:02:38, "land tools/mori-job-runway.py (C2) ... D4 ignore rule") changed `.gitignore` (E4). All findings are for `6a92d5e`.
Tool availability: this seat has no `lsp` device (tool set: read, bash, edit, eval, glob, grep, task, wait, web_search, write; xd devices ast_edit and debug). Caller checks used the literal text-grep fallback, which is not semantic proof. The import and writer claims were also checked dynamically in a sandbox (E8).

## Recommendation

Set `.gitignore` line 3 to exactly:

    tools/__pycache__/

This replaces the landed `__pycache__/`. Of the six lines D4 accepts (`contract.md:22`), it is the only anchored one and the narrowest that hides the untracked cache. It matches none of the 212 tracked `.pyc` files (E3). It is in the D4 set, so D4 stays held and the declared after-value (`mismatches: 0`) is unchanged. Keep the line LF-terminated with no comment or trailing spaces; the current file is LF-only (E1).

## Findings

### F1 (medium): the landed rule hides 212 committed evidence files
- `.gitignore:3` at HEAD is `__pycache__/` (E1). Commit `09f55b6` is the only round-25 commit that touches `.gitignore`; it adds exactly that line (E4).
- The rule matches 212 tracked files: all `.pyc` under `.ufo/waves/round-20/`, none under `tools/` (E3, E5).
- Git still tracks those files and still reports changes to them (E6: modified tracked `.pyc` stays listed). What the blanket rule hides is untracked matches (F2). It also turns a committed-but-ignored audit red: `git ls-files -c -i --exclude-standard` lists 212 (E3, `head-now` row).

### F2 (medium): under the landed rule, new evidence caches are skipped silently
- E6 sandbox: a new untracked `.ufo/waves/round-25/evidence/Y/tools/__pycache__/n.cpython-314.pyc` is absent from `git status --porcelain` and from `git add --dry-run -A` under the blanket line. `git check-ignore --no-index -v` names `.gitignore:3:__pycache__/`. Under the narrow line the same file shows as `?? .ufo/waves/round-25/` and is staged.

### F3 (medium, process): D4 passes the harmful line and cannot see the harm
- `contract.md:22` accepts five blanket forms (`__pycache__/`, `__pycache__`, `**/__pycache__/`, `*.pyc`, `*.py[cod]`) and one anchored form. Measured: each blanket form hides 212 tracked files; the anchored form hides 0 (E3).
- The hygiene row (`contract.md:111-114`) checks `!` lines and tracked paths under `tools/` only. The 212 caches sit under `.ufo/`, so HEAD `6a92d5e` passes D4 while hiding them. A held D4 does not show the rule is safe.
- Suggestion, not counted, owner's call: add "`git ls-files -c -i --exclude-standard` is empty" to the hygiene row.

### F4 (low): one gate loads a lane-root tool by path without suppressing bytecode
- `.ufo/waves/round-20/falsify/LiveSouji/compare.py:22` sets `TOOL = $MORI/tools/mori-wave-settlement.py`. Lines `:86-88` load it with `spec_from_file_location` and `exec_module`. The file has no `-B` and no `dont_write_bytecode` (E9 grep). If run with bytecode writing on, it writes `tools/__pycache__/mori-wave-settlement.cpython-314.pyc` at the lane root (mechanism: E8 row F2). No such file exists now. I did not run the gate and did not determine why it is absent [INFERENCE on the mechanism].
- The correct pattern is in `.ufo/waves/round-20/falsify/ReviewQuality/c-fixtures.py:14`, which sets `sys.dont_write_bytecode = True` before the copy load at `:174-178`.
- `exec(compile(...))` writes no cache: `.ufo/waves/round-23/falsify/MutModeRead/mode_read_probe.py:125-128` and `permission_loss_probe.py:27-29`.

### F5 (info): no lane tool imports another lane tool
- Static sweep of `tools/` (all file types), `.ufo/waves/round-25/` and `.scratch/` (E9): no `import`/`from` of a mori or tools module, and no `importlib`, `spec_from_file_location`, `py_compile`, `compileall`, `runpy` or `sys.path` edit in tool code. The only `__import__` calls are `__import__("time")` at `tools/mori-round16-regressions.py:1457,1460`.
- Tools reach other tools only as subprocesses. 18 files in `tools/` launch Python with `sys.executable`. Example: `tools/mori-routed-check.py:352` runs `[sys.executable, "-I", "-", ...]` with the blob on stdin. A script run directly never gets a cache (E8, R0).
- `tools/mori-job-runway.py:67-79` imports stdlib modules only and runs no subprocess.
- Hyphenated tool names cannot be imported by name (E8, R11: `SyntaxError`). A `tools/` cache therefore needs a path load or an explicit compile (E8, R8/R9).
- Fleet scripts: the same pattern family over `scripts/hyaku` finds no Python import or compile of a lane tool. The only hit is a sandbox fixture at `scripts/hyaku/jj-lane-selftest.sh:333-334`, which adds `__pycache__/` to a sandbox `.git/info/exclude`.

### F6 (info): the one untracked cache, and the committed ones
- `tools/__pycache__/mori-dispatch-ledger.cpython-314.pyc` is the only file in that directory, mtime 2026-10-22 05:19:16 -03:00 (E7). Its header source-mtime (1792565552 = 2026-10-21 03:52:32) equals the current `tools/mori-dispatch-ledger.py` mtime, so it was compiled from the current bytes. The writer is not identified. [INFERENCE] an explicit path load or `py_compile` run by a seat or operator, since an ordinary import is impossible (E8, R11) and no committed lane code does either (F5). The round-24 spot-check records the same file (`corpus/lessons/round-24-verifier-spotcheck.md:26`) and routes it at `:145`.
- The 212 committed caches each sit beside a copy of the tool (E5: `.ufo/waves/round-20/falsify/SelftestC2/final/C1-checker-always-true/tools/mori-wave-settlement.py` and `.../tools/__pycache__/mori-wave-settlement.cpython-314.pyc`). They were first committed by `71abd41` (08:18:29) and `b6be916` (08:19:24), 2026-10-21 (E5). [INFERENCE] unsuppressed path loads of tool copies wrote them.

### F7 (answer): does `-B` avoid it?
- `-B` avoids every write that occurs here: imports and path loads (E8: R2, R4, F1).
- `-B` does not stop explicit compilation: `py_compile` (R8, R10) and `compileall` (F3) write anyway. The ignore line is still needed.
- `-I` makes the bytecode env var useless: `PYTHONDONTWRITEBYTECODE=1` is ignored under `-I` (R5, R13). With the declared `python3 -I -B` form (`contract.md:123`), use the `-B` flag, not the env var.
- `-I` also drops the script's directory from `sys.path` (R7). A tool that imports a sibling cannot run under the declared form. None does (F5).
- Keep `python3 -I -B` for every declared run and keep the anchored ignore line.

## Evidence

E1. `cat -A .gitignore` (working copy) and `git show HEAD:.gitignore` (HEAD `6a92d5e`): `.ufo/interactive-sessions/$`, `.ufo/worktrees/$`, `__pycache__/$`. `git show 28b79d3d:.gitignore`: first two lines only. `.jj/.gitignore:1` is `/*`, which is why `.jj/` shows `!!`. No `core.excludesFile` is set; `.git/info/exclude` has comments only.

E2. First `git status --porcelain --ignored` (run before HEAD moved, without `GIT_OPTIONAL_LOCKS=0`): ` M .gitignore`, `?? .scratch/`, `!! .jj/`, `!! .ufo/interactive-sessions/`, `!! .ufo/worktrees/`, `!! tools/__pycache__/`.

E3. Candidate test, lane HEAD. `git ls-files -c -i --exclude-from=<candidate>` gives tracked matches; `git ls-files -o --exclude-from=<candidate> -- tools` gives untracked files that remain visible.

| candidate line | tracked files hidden | untracked `tools/__pycache__` file visible |
|---|---|---|
| negative control `zz-no-such-path/` | 0 | yes |
| `tools/__pycache__/` (recommended) | 0 | no |
| `tools/__pycache__` | 0 | no |
| `tools/__pycache__/*.pyc` | 0 | no (not a D4 accepted form, so it would fail the held test) |
| `.ufo/waves/round-25/**/__pycache__/` | 0 | n/a (not a D4 accepted form) |
| `__pycache__/` (landed at `09f55b6`) | 212 | no |
| `__pycache__` | 212 | no |
| `**/__pycache__/` | 212 | no |
| `*.pyc` (positive control) | 212 | no |
| `*.py[cod]` | 212 | no |

Reproduce the recommendation in the lane (read-only): `printf 'tools/__pycache__/\n' > /tmp/cand.txt; git -C <lane> ls-files -c -i --exclude-from=/tmp/cand.txt | wc -l` prints `0`, and `git -C <lane> ls-files -o --exclude-from=/tmp/cand.txt -- tools` prints nothing.

E4. `git log --format='%h %ci %s' -6` (HEAD first): `6a92d5e` 07:09:22 (contract amendment A2); `51ddd01` 07:05:20 (A1); `09f55b6` 07:02:38 ("land tools/mori-job-runway.py (C2) after the frozen cases; D4 ignore rule"); `129832e` 06:58:30; `0099a39` 06:52:16; `7634be7` 06:49:49. `git show --stat 09f55b6`: `.gitignore | 1 +`, `tools/mori-job-runway.py | 510 +`. `git diff 129832e3 HEAD -- .gitignore`: adds `+__pycache__/`. `git log --format='%h %ci %s' -- .gitignore`: `09f55b6` (round 25), `273aa74` (2026-10-20), `20e2255` (2026-10-17).

E5. `git ls-files | grep -E '\.pyc$' | cut -d/ -f1-3 | sort | uniq -c` prints `212 .ufo/waves/round-20`. `git ls-files -- .ufo/waves/round-25/ | grep -cE 'pycache|\.pyc$'` prints `0`. `git log --diff-filter=A --format='%h %ci %s' -- '*.pyc'` prints `b6be916 2026-10-21 08:19:24` and `71abd41 2026-10-21 08:18:29`, two commits. `git ls-files -- '.ufo/waves/round-20/falsify/SelftestC2/final/C1-checker-always-true/tools/'` lists the tool copy and its `.pyc`.

E6. Sandbox at `/tmp/r25-gitlab` (scratch repo, git 2.56.0; not the lane).
- Blanket `__pycache__/`: `git status --porcelain` lists the modified `.gitignore` and the modified tracked `.pyc`. It does not list the new untracked evidence cache. `git status --porcelain --ignored` marks `.ufo/waves/round-25/` and `tools/__pycache__/` as `!!`. `git add --dry-run -A` adds `.gitignore` and the tracked `.pyc` only. `git check-ignore --no-index -v` on the new file prints `.gitignore:3:__pycache__/`.
- Narrow `tools/__pycache__/`: `git status --porcelain` shows `?? .ufo/waves/round-25/`; `tools/__pycache__/` is `!!`; `git add --dry-run -A` adds the new evidence `.pyc`; `check-ignore --no-index` on it prints not-matched.

E7. `stat tools/__pycache__/mori-dispatch-ledger.cpython-314.pyc`: mtime `2026-10-22 05:19:16.164243390 -0300`. Header bytes 8-11 read as 1792565552 (2026-10-21 03:52:32), equal to `stat tools/mori-dispatch-ledger.py`. `ls tools/__pycache__ | wc -l` prints `1`.

E8. Python 3.14.8 (`sys.implementation.cache_tag` = `cpython-314`). Sandbox `/tmp/r25-pylab`; the cache directory was checked after each run.

| run | cache written | result |
|---|---|---|
| R0 `python3 standalone.py` | no | runs |
| R1 `python3 main_tool.py` (imports helper_mod) | yes | runs |
| R2 `python3 -B main_tool.py` | no | runs |
| R3 `python3 -I main_wrap.py` (sys.path insert) | yes | runs |
| R4 `python3 -I -B main_wrap.py` | no | runs |
| R5 `PYTHONDONTWRITEBYTECODE=1 python3 -I main_wrap.py` | yes | env ignored |
| R6 `PYTHONDONTWRITEBYTECODE=1 python3 main_wrap.py` | no | env honoured |
| R7 `python3 -I -B main_tool.py` (no sys.path insert) | no | ModuleNotFoundError, rc 1 |
| R8 `python3 -B -m py_compile helper_mod.py` | yes | -B ignored |
| R9 importlib file-path load of `hyphen-dummy.py`, no flags | yes (`hyphen-dummy.cpython-314.pyc`) | runs |
| R10 `python3 -I -B -m py_compile hyphen-dummy.py` | yes | -B ignored |
| R11 `python3 -c "import mori-dispatch-ledger"` | no | SyntaxError: invalid syntax |
| R12 flags under `-I -B` | n/a | ignore_environment=1, safe_path=True, dont_write_bytecode=1 |
| R13 `PYTHONDONTWRITEBYTECODE=1 python3 -I -c ...` | n/a | sys.dont_write_bytecode = False |
| F1 `python3 -I -B` importlib path load | no | runs |
| F2 `python3 -I` importlib path load | yes | runs |
| F3 `python3 -I -B -m compileall -q hyphen-dummy.py` | yes | -B ignored |

This shell sets no `PYTHON*` bytecode variables (`printenv` shows only `PYTHONUNBUFFERED=1`).

E9. Static sweep, case-insensitive. Pattern: `importlib|spec_from_file_location|py_compile|compileall|runpy|sys\.path\.(insert|append)|__import__\(|^\s*(from|import)\s+(mori|tools)|PYTHONDONTWRITEBYTECODE|dont_write_bytecode|PYTHONPYCACHEPREFIX`. Scope: `tools/`, `.ufo/waves/round-25/`, `.scratch/` (hits: `__import__("time")` in round-16 regressions; `PYTHONDONTWRITEBYTECODE` set for child processes at `tools/mori-round15-regressions.py:2170` and `tools/mori-round17-seat-regressions.py:260`). Whole lane, `**/*.py` and `**/*.sh`: path loaders only in round-20, round-22 and round-23 evidence trees; `tools/` hits are comments. `scripts/hyaku`: no Python import or compile; one sh fixture (F5).

## Verification gaps
- `tools/mori-routed-r24.py` is not in the lane at `6a92d5e`, so its D4 row was not run.
- The narrow line was checked in a sandbox and with `ls-files` against the lane. It was not staged in the lane, because lane writes are out of bounds.
- jj was not run. [INFERENCE] jj's snapshot also honours `.gitignore`; untested here.
- The writers of the lane-root cache and of the 212 caches are inferred from file names, headers and loader code. No harness was re-run and no transcript was read.
- The lane-root cache could come from a run that is not recorded in the repo; I cannot exclude that.

## Residual risk
- The narrow rule leaves future harness caches under `.ufo/waves/round-N/**/tools/__pycache__/` visible. They could be swept into a commit by `git add -A`. Mitigation: set `sys.dont_write_bytecode = True` before a path load (the `c-fixtures.py:14` pattern) or run `-B`; or add a round-scoped anchored line when a round needs one (E3: 0 tracked under round-25).
- `py_compile` and `compileall` ignore `-B`. The anchored line still covers a manual compile into `tools/`.
- The 212 round-20 caches stay tracked. Untracking them would change committed evidence and is out of scope.

## Lane-state notes and installs
- Written: this file only. Scratch: `/tmp/r25-d4`, `/tmp/r25-gitlab`, `/tmp/r25-pylab`.
- Lane git commands were read-only (`log`, `show`, `diff`, `ls-files`, `check-ignore`, `status`, `rev-parse`). The first `git status` ran without `GIT_OPTIONAL_LOCKS=0`, so git may have refreshed index stat data; no content changed. Later commands set `GIT_OPTIONAL_LOCKS=0`.
- Other seats' untracked round-25 files (`w1/*.md`, `evidence/runway-live-run.*`) were not touched.
- Installs and updates: none. In use: git 2.56.0 and Python 3.14.8, both pre-existing. No pacman, uv, cargo or npm invoked. `~/.omp/agent/RULES.md` read.

## Handoff (integration owner, MoriR25)
1. Change `.gitignore` line 3 to `tools/__pycache__/` and commit it. Not done here.
2. Check: `git ls-files -c -i --exclude-standard | wc -l` prints `0`; `git ls-files -o --exclude-standard -- tools` prints nothing.
3. D4 stays held with either line. No counted C1 item changes.
4. Optional: delete `tools/__pycache__/mori-dispatch-ledger.cpython-314.pyc`. It is generated and the new line hides it.
5. Harnesses that load tools by path: set `sys.dont_write_bytecode = True` first, or run `-B`.
