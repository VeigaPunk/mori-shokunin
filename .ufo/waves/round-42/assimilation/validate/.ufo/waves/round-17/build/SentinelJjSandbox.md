# SentinelJjSandbox — C2 gate trust-boundary review (mori round 17 wave 1)

Seat: `MoriR17.SentinelJjSandbox-5` (sentinel, advisory only; no edits, no judging).
Surface: the C2 gate contract (`contract.md:80-94`), the JjGate item spec (`wave1-spec.json`,
item `JjGate`), and env override handling in `tools/mori-census.sh` (lane tip 24526ea).
Question: can jj/git writes in the gate's sandboxes reach the lane, the fleet,
`~/.config/jj/repos` or the real remote, and does the census run make any live host query?

**Verdict:** the contract is sound only if the gate adds guards the spec leaves out. The spec
already redirects HOME, XDG_CONFIG_HOME, JJ_CONFIG and GIT_CONFIG_GLOBAL. It does **not**
cover two problems:

- **jj ancestor discovery.** Every sandbox necessarily sits *inside* the lane's working tree,
  and the lane has a live `.jj`.
- **The census's "empty override means live default" rule.**

There are 2 high and 3 medium findings below. Nothing has been built yet: the JjGate clone
has no `tools/mori-round17-jj-regressions.py`, and `.scratch` is empty (observed). This
review therefore targets the contract and the spec, not code.

## Observed host facts (read-only commands, all rc 0 unless noted)

| Fact | Command / source |
|---|---|
| The lane is jj-colocated: `/home/vgpnk/Projects/shokunin/mori-shokunin/.jj/{repo,working_copy}` exist, and `.jj/repo/config-id` = `118d84571a457bac1fa8` | `ls .jj/repo; cat .jj/repo/config-id` |
| The lane's repo config lives **outside** the repo at `~/.config/jj/repos/118d84571a457bac1fa8/config.toml`. It holds the `user.name="mori-shokunin"` identity, `trunk()=master@origin` and `snapshot.auto-track="none()"` | `jj config path --repo -R <lane>`, cat of that file |
| `~/.config/jj/repos` has **1536** config dirs (leakage from earlier sandbox runs; jj-lane-selftest.sh:26-35 cleans up its own manually) | `ls ~/.config/jj/repos \| wc -l` |
| The lane's origin is `https://github.com/VeigaPunk/mori-shokunin.git` | `git -C <lane> remote -v` |
| The JjGate and CensusJj clones have `remote.origin.url=/home/vgpnk/Projects/shokunin/mori-shokunin`, a **local path to the lane**, with push enabled | `git -C <clone> remote -v; git config --local --list` |
| Sandboxes go under `JjGate/.scratch` (TMPDIR rule, wave1-context.txt:7). That path is inside the lane tree, and the lane `.gitignore:2` ignores `.ufo/worktrees/` | `git check-ignore -v .ufo/worktrees/round-17/JjGate/.scratch/x` → `.gitignore:2` |
| Global user git configuration was listed (key names); its keys and values are withheld (round-18 privacy repair; closure V12). It was observed that no system-wide git config and no legacy jj user config file exist | `git config --global --list --name-only` |
| The user jj configuration was read; its settings are withheld (round-18 privacy repair; closure V12) | cat (values withheld) |
| Session env has `GIT_EDITOR=true GIT_PAGER=cat GIT_TERMINAL_PROMPT=0` and no GIT_DIR/JJ_* set right now | `env \| grep` |
| Tools: jj 0.45.1-7c41cdeb (`~/.local/bin/jj`), git 2.56.0 | `jj --version; git --version` |

jj source checked at tag v0.45.1 (fetched read-only from raw.githubusercontent.com,
accessed 2026-10-20):

- `cli/src/cli_util.rs:2897-2901`: `find_workspace_dir` = `cwd.ancestors().find(|p| p.join(".jj").is_dir())`. It has **no ceiling**.
- `cli/src/cli_util.rs:4602-4612`: the cwd workspace is loaded even when `-R` is given, but only its repo config is *read*, for alias resolution.
- `cli/src/cli_util.rs:4646-4655`: `-R` loads exactly the given path, and an invalid path is a hard error.
- `cli/src/config.rs:60, 286-288, 368-370, 554-558`: the repo-config root is `etcetera config_dir()/jj/repos`, i.e. `$XDG_CONFIG_HOME` or `$HOME/.config`. `JJ_CONFIG` (`config.rs:291-296`) only replaces the *user* config file list and does **not** move `repos/`.
- `lib/src/git_subprocess.rs:118-140`: jj's git subprocess passes `--git-dir <store>` and `-c core.fsmonitor=false`, and otherwise inherits the environment plus `git.environment` envs.

## Findings

### F1 — HIGH: a jj call in a sandbox without `.jj` falls through to the LANE repo

- **Exploit path:**
  1. The gate builds a case under `JjGate/.scratch/<run>/<case>/`.
  2. Any step that leaves the case without its own `.jj` breaks the chain: `git init` or `jj git init --colocate` fails, a typo in the case path, the cwd still pointing at the parent, or an exception path that keeps going.
  3. The next `jj <cmd>` run with that cwd climbs the ancestors. `JjGate/` has no `.jj`, so jj stops at `/home/vgpnk/Projects/shokunin/mori-shokunin/.jj`, the **live lane**.
- **Impact:**
  - Even a read such as `jj log` snapshots the lane working copy and writes an operation into the lane `.jj/repo/op_store`.
  - `jj new`, `jj commit`, `jj metaedit`, `jj bookmark set` and `jj describe` (all of which the spec's case list uses) rewrite the lane's working-copy commit. The colocated export then moves the lane's **git HEAD and branch refs**.
  - The gate would manufacture exactly the `HEAD_BRANCH_MISMATCH` it is meant to detect, in the real lane.
  - This happens with the lane's own repo config, since that is what the walk loads.
- **Evidence:**
  - `cli_util.rs:2897-2901` (no ceiling).
  - The lane `.jj` exists.
  - The sandbox location is mandated inside the lane tree (wave1-context.txt:7).
  - Neither `.gitignore` nor `auto-track=none()` stops this: they limit which *files* get tracked, not commit or bookmark operations.
- **Smallest remediation (required):**
  - The gate must run every jj invocation through one wrapper that:
    - passes `-R <abs case dir>`;
    - checks `os.path.isdir(case/".jj")` beforehand, and that `realpath(case)` starts with `realpath(scratch_run_root) + os.sep`;
    - refuses any call without `-R`.
  - The single exception is `jj git init --colocate <abs case dir>`. It must run only after `git init` has created `<case>/.git`, and with `cwd=<case>`.
  - Prefer `--ignore-working-copy` for every read-only jj query.
- **Falsifier to add as a gate case:** create a case dir with *no* `.jj` and assert the wrapper refuses, with rc≠0 and no jj process spawned.

### F2 — HIGH: sandbox remotes can point at the lane or GitHub

- **Exploit path A (lane):**
  1. A sandbox is seeded with `git clone <lane>` or `git clone <JjGate clone>`. The second is tempting, because the base commit 24526ea lives there.
  2. The sandbox's `origin` is then a local path. The JjGate clone itself already has `origin=<lane path>` (observed).
  3. Any `git push`, `jj git push`, or a helper-shaped "push" step writes refs straight into the lane (or into the clone), over the `file` transport with no credentials.
- **Exploit path B (real remote):**
  1. A sandbox ends up with the lane's `.git/config`, for example by copying `.git` or `cp -a` of the lane to "get a colocated repo fast".
  2. Its `origin` is then `https://github.com/VeigaPunk/mori-shokunin.git`.
  3. With the real global config loaded, `credential.https://github.com.helper` authenticates non-interactively. `push.autosetupremote=true` lets a bare `git push` create a remote branch.
- **Impact:** a fabricated test history lands on GitHub or in the lane's branch.
- **Smallest remediation (required):**
  - Build every fixture with `git init`. Never clone or copy from the lane, the fleet or any clone.
  - Need `refs/remotes/origin/HEAD` for the `detect_branch` fallback? Create it locally with `git update-ref refs/remotes/origin/master <sha>` and `git symbolic-ref refs/remotes/origin/HEAD refs/remotes/origin/master`. That needs **no remote at all**.
  - If any remote is configured, it must be a sandbox bare repo. Before *every* push or fetch, assert that `git config --get-regexp '^remote\..*\.(url|pushurl)$'` resolves (realpath) under the run root.
  - Export `GIT_ALLOW_PROTOCOL=file` into the git and jj env. jj's git subprocess inherits it (`git_subprocess.rs:140`), so https and ssh transports are refused even if a URL leaks.
  - Set `GIT_CONFIG_GLOBAL=<sandbox>/gitconfig` (or `/dev/null`) plus `GIT_CONFIG_NOSYSTEM=1`. This drops the credential helpers, `push.autosetupremote` and `filter.lfs.*`.

### F3 — MEDIUM: `~/.config/jj/repos` pollution and identity bleed

- **Exploit path:** each `jj git init --colocate` writes a new `repos/<config-id>/` dir. A `jj config set --repo`, which the helper-shaped case will want for `trunk()` or identity, writes there too. That path is **not** moved by `JJ_CONFIG` (config.rs:554-558); only `XDG_CONFIG_HOME`, falling back to `HOME`, moves it.
- **Copy variant:** if the gate copies the lane's `.jj`, jj detects the copy and *copies the lane's repo config* to a new id. The sandbox then commits as `mori-shokunin <mori@shokunin.local>`. Sources: JjDocIdentity.md:214-224 and JjSentinelHelper.md:260-262 (both earlier sandbox observations).
- **Why `JJ_CONFIG` is still needed:** without it, the real `~/.config/jj/config.toml` (`git.auto-local-bookmark=true`, real name and email) is loaded. That makes the "ambient author" in the LANE_AUTHOR_MISMATCH case the operator's real identity, which is non-deterministic per host and leaks a personal name into `run-manifest.json`.
- **Impact:** permanent writes outside the sandbox (1536 dirs already present show this has happened before), and host-dependent fixtures.
- **Smallest remediation (required):**
  - Set all three of `HOME=<run>/home`, `XDG_CONFIG_HOME=<run>/home/.config` and `JJ_CONFIG=<run>/jj-user.toml`. `JJ_CONFIG` alone is insufficient.
  - In `jj-user.toml`, set `user.name="ambient-tester"` and `user.email="ambient@sandbox.invalid"` (synthetic), `ui.editor="false"`, `ui.paginate="never"` and `git.auto-local-bookmark=false`.
  - Never `cp` a `.jj`.
  - Never run `jj config gc` (it would scan the real config root if the env leaked).
- **Proof invariant:** record the entry count and newest mtime of `~/.config/jj/repos` before and after the run, using `os.scandir`, not jj. Any increase fails the run (rc 2).

### F4 — MEDIUM: an inherited `GIT_DIR`/`GIT_WORK_TREE` redirects sandbox writes and census reads

- **Exploit path, write side:**
  1. L1 invokes the gate from a context that exports `GIT_DIR`, e.g. a git hook, `git rebase -x`, or `git submodule foreach`. All of these export `GIT_DIR`, and some export `GIT_WORK_TREE`/`GIT_INDEX_FILE`.
  2. With that set, `git -C <case> add`/`commit` in the gate writes to the **parent's repository**, i.e. the lane, because `GIT_DIR` overrides `-C` discovery.
- **Exploit path, read side:**
  - `tools/mori-census.sh:2100` and `:2102` (row 6, report-closure `cat-file -e` and `log -1` on `$ROOT`) run `env GIT_OPTIONAL_LOCKS=0 git -C "$ROOT"`. They do **not** do `-u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE`.
  - Every other census git call does: `:2129`, `:2180`, `:2197`, `:2207`.
  - So an inherited `GIT_DIR` makes row 6 read the wrong repo. This is a read-only misgrade, not a write.
  - The C2 change rewrites exactly those two lines. The new `symbolic-ref`, `refs/remotes/origin/HEAD`, `merge-base --is-ancestor` and `log refs/heads/<b>` probes must use the scrubbed form.
- **Smallest remediation (required):**
  - The gate builds every child env from scratch (`env={...}`), never from `os.environ`. That covers its own git calls, its jj calls and the census run.
  - Pattern to reuse: `mori-silence-cases.sh:475-490` (`env -i PATH=/usr/bin:/bin HOME=… GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null` + explicit `GIT_AUTHOR_*`/`GIT_COMMITTER_*`/dates).
  - Do not copy `mori-round14-regressions.py:386` (`"HOME": os.environ.get("HOME", "/tmp")`). That is a real-HOME passthrough with a `/tmp` fallback.
- **Gate case to add (falsifier for the census side):** run the census with `GIT_DIR=<decoy repo>` and `GIT_WORK_TREE=<decoy>` added to its env. Assert the lane verdict and row 6 closure are byte-identical to the clean run.
  - The entering census should fail this through row 6 when the decoy carries a committed report. [INFERENCE: not run]
  - The delivered census must pass.

### F5 — MEDIUM: an empty census override means LIVE host default, and several surfaces are only "stubbed" if every override is set

- **Mechanism:** every override is `${MORI_X:-default}` (`mori-census.sh:282-357`, `:1663-1664`), and the help text says "empty = live host defaults" (`:202`).
  - A gate that sets `MORI_JOURNALCTL_BIN=""` meaning "disabled" gets live `journalctl`, which breaks the wave rule "no live journal queries".
  - `MORI_TMUX_BIN=""` → live `tmux ls` / `list-panes` / `display-message` against the operator's server (`:2325-2407`).
  - `MORI_DISK_TARGETS=""` → `df -P "$ROOT /tmp"` (`:308`).
  - `MORI_SHOKUNIN_ROOT=""` → `DEFAULT_ROOT` derived from the census file's own location (`:269-282`). For the delivered census at `<lane>/tools/`, that is the **real fleet root**, which means live `git -C` reads of every real lane.
  - Binaries are found via `command -v` (`have()`, `:546`), so a bare name resolves on PATH.
- **Required census env.** Every value must be non-empty and absolute, under the run root unless stated:

  | Variable | Value |
  |---|---|
  | `MORI_SHOKUNIN_ROOT` | sandbox fleet root |
  | `MORI_UFO_DIR` | sandbox `.ufo` |
  | `MORI_STATE_DIR`, `MORI_WAVES_DIR`, `MORI_WATCHDOG_LOG`, `MORI_TIMELINE_FILE` | sandbox paths |
  | `MORI_FLEET_CONF` | sandbox `shokunin.conf` |
  | `MORI_ROSTER_LANES` | the sandbox lane id; non-empty, or the conf parse is exercised deliberately |
  | `MORI_TMUX_SCOPE_ROOT` | sandbox fleet root |
  | `MORI_NOW_EPOCH` | pinned |
  | `MORI_BOOT_ID` | 32 hex characters (avoids reading `/proc/sys/kernel/random/boot_id`, `:328-332`) |
  | `MORI_BOOT_ID_FILE` | sandbox file |
  | `MORI_CGROUP_EVENTS`, `MORI_CGROUP_CURRENT`, `MORI_CGROUP_PRESSURE`, `MORI_CGROUP_MAX`, `MORI_CGROUP_PEAK`, `MORI_CGROUP_LOCAL_EVENTS`, `MORI_CGROUP_SERVICE_EVENTS` | sandbox files; the last two are undocumented in the header (`:1663-1664`), so list them explicitly |
  | `MORI_MEMINFO`, `MORI_DISKSTATS`, `MORI_UPTIME` | sandbox files |
  | `MORI_DISK_TARGETS` | sandbox fleet root |
  | `MORI_JOURNALCTL_BIN`, `MORI_TMUX_BIN`, `MORI_PGREP_BIN`, `MORI_DF_BIN` | absolute path to a **non-existent** file or a refusing stub; absent gives `journal: unavailable journalctl=missing` per the census's own selftest at `:3592-3595` |
  | `MORI_JQ_BIN` | absent or real; the journal is off either way |
  | `MORI_GIT_BIN` | `/usr/bin/git`; real git is required for real colocated sandboxes, and absolute avoids PATH capture |
  | `MORI_TIMEOUT_BIN` | `/usr/bin/timeout` |

- **PATH tripwire (required):** put stub `journalctl`, `tmux`, `pgrep`, `df`, `systemctl` and `jj` first on `PATH`. Each appends to `<run>/tripwire.log` and exits 127. The gate asserts the file is empty after every census run. Precedent: `mori-round14-regressions.py:858-866`. The census must never invoke jj; the gate's own jj calls use the absolute `~/.local/bin/jj`.
- **The census env also needs:** `env -i` base, `HOME`/`XDG_CONFIG_HOME` = sandbox, `GIT_CONFIG_GLOBAL`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CEILING_DIRECTORIES` (see F6), `TZ=UTC`, `LC_ALL=C`, and **no `TMUX`/`TMUX_PANE`**. tmux uses those to pick a live socket if a real binary is ever reached.
- **Can every surface be stubbed? Yes.** Every host surface the census reads has an override: journal, tmux, pgrep, df, cgroup ×7, meminfo, diskstats, uptime and boot id. The remaining live calls are `date` and `id -u`, which are harmless and pinned by `MORI_NOW_EPOCH`. So the spec's "if any surface cannot be stubbed, stop" condition does **not** trigger.

### F6 — LOW–MEDIUM: git ancestor walk to the JjGate clone's `.git`

- **Exploit path:** a case dir, or the sandbox fleet root, is missing `.git`. Then:
  - Gate writes (`git -C <case> commit`) land in the **JjGate clone** (`JjGate/.git`). That is a forbidden VCS mutation of the executor's clone.
  - Census row 6 (`git -C "$ROOT" cat-file -e <ref>:.ufo/reports/...`) reads the clone's real history, so a real committed report could grade a sandbox lane `not-open`. This is a false pass or fail.
- **Remediation (required):**
  - Set `GIT_CEILING_DIRECTORIES=<abs run root>` in every git, jj and census env. jj's git subprocess inherits it.
  - Assert `<case>/.git` and `<fleetroot>/.git` exist before each git write.
  - `git init` the sandbox fleet root explicitly. The "report committed only off-branch" case needs it to be a real repo.

### F7 — LOW: hangs and cleanup

- **Hangs:**
  - `jj describe` / `jj commit` without `-m`, under `env -i`, has no `GIT_EDITOR=true` or `JJ_EDITOR`, so it opens an editor with no TTY and hangs.
  - Remediation: always pass `-m`; set `ui.editor="false"` in the sandbox `JJ_CONFIG`; `stdin=DEVNULL`; `timeout=` on every `subprocess.run`; kill the census process group on timeout.
- **Cleanup:** `shutil.rmtree` must target only `realpath(path)` under `realpath(--scratch)` and never `--scratch` itself.
- **`--scratch` validation:**
  - Required, or defaulting to `<clone>/.scratch`, **never** `tempfile` defaults. `tempfile` falls back to `/tmp` when `TMPDIR` is unset, and `/tmp` is forbidden by wave1-context.txt:7.
  - The scratch path must not equal the lane root, the fleet root or any `.git`/`.jj` dir.
  - Each run gets `mkdtemp(dir=scratch)`.
- **`/tmp` precedents the gate must not copy or invoke:**
  - census `--selftest` → `mktemp -d /tmp/mori-census-selftest.XXXXXX` (`mori-census.sh:2768`);
  - `mori-silence-cases.sh:283` → `mktemp -d /tmp/...`;
  - `mori-round14-regressions.py:2643` → `tempfile.mkdtemp` without `dir=`.

## Required guards (checklist for JjGate, plus CensusJj where noted)

1. **G1 jj confinement:** a single jj wrapper with mandatory `-R <abs case>`, a `.jj`-exists check and a realpath-prefix check. `jj git init --colocate` runs only after `git init`. `--ignore-working-copy` on reads. Plus a refusal case. (F1)
2. **G2 fresh env:** every child (git, jj, census) gets an env built from nothing:
   - `PATH=<run>/tripwire:/usr/bin:/bin`, `HOME`, `XDG_CONFIG_HOME`, `JJ_CONFIG` (all sandbox), `GIT_CONFIG_GLOBAL=<sandbox file or /dev/null>`, `GIT_CONFIG_NOSYSTEM=1`;
   - `GIT_CEILING_DIRECTORIES=<run root>`, `GIT_ALLOW_PROTOCOL=file`, `GIT_TERMINAL_PROMPT=0`, `GIT_OPTIONAL_LOCKS=0` for reads, `TZ=UTC`, `LC_ALL=C`;
   - explicit `GIT_AUTHOR_*`/`GIT_COMMITTER_*`/dates or jj `--config user.*` per commit;
   - and no `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, `GIT_COMMON_DIR`, `GIT_OBJECT_DIRECTORY`, `GIT_ALTERNATE_OBJECT_DIRECTORIES`, `GIT_NAMESPACE`, `GIT_CONFIG_PARAMETERS`/`GIT_CONFIG_COUNT`, `TMUX`, `JJ_USER`/`JJ_EMAIL` from the host. (F3, F4, F6)
3. **G3 no clones or copies:** fixtures come only from `git init`. Synthesize `origin/HEAD` with `update-ref`/`symbolic-ref`. Any configured remote URL must realpath under the run root, asserted before each push or fetch. (F2)
4. **G4 census stub env:** the full non-empty absolute `MORI_*` set in F5, plus the PATH tripwire with an empty-log assertion. (F5)
5. **G5 CensusJj (census side):** every new or changed git probe uses `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0`. That includes the rewritten `:2100`/`:2102` and the new `symbolic-ref`/`merge-base`/`refs/remotes/origin/HEAD` calls. Branch detection must stay local-ref only: no `ls-remote`, `fetch` or `remote set-head` (`jj-lane.sh:115-120` detect_branch is local-only; its `ls-remote` at `:237` belongs to push and must not be mirrored). Gate case: the `GIT_DIR` decoy from F4.
6. **G6 zero-mutation proof (required in `run-manifest.json`):** record before/after fingerprints read through files or read-only git with `GIT_OPTIONAL_LOCKS=0`, **never jj**:
   - lane: `git for-each-ref`, `symbolic-ref -q HEAD`, `rev-parse HEAD`, a listing of `.jj/repo/op_heads/heads/`, sha256 of `.jj/working_copy/checkout`;
   - JjGate clone: `for-each-ref` and HEAD;
   - `~/.config/jj/repos`: entry count and newest mtime.

   Any delta → rc 2 with the named delta. Caveat: L1 may legitimately touch the lane during the run, so record a delta as "observed, unattributed" rather than silently passing.
7. **G7 hygiene:** `-m` on every jj/git commit; `ui.editor="false"`; `stdin=DEVNULL`; per-call timeouts with process-group kill; prefix-checked rmtree; an explicit, validated `--scratch`; no `/tmp`; never call the census `--selftest` from the gate. (F7)

## Commands I ran (all read-only; no writes outside this report)

- `cat`/`ls`/`grep`/`stat` of the contract, wave context, census, the JjGate/CensusJj clones, `~/.config/jj/config.toml` (name and email redacted in this report) and `~/.config/jj/repos/118d…/config.toml`, rc 0.
- `git remote -v`, `git config --local --list`, `git config --global --list --name-only` (key names only; credential helper values not printed), `git check-ignore -v`, `git log --oneline -1` / `status --short` per clone, rc 0. `git config --system` rc 128 (no `/etc/gitconfig`).
- One jj call against the lane: `jj config path --repo -R <lane>`, rc 0. Its help says it creates a config dir only when the file is missing, and the file existed.
  - Mutation check afterwards: lane `.jj/repo/op_heads/heads/*`, `.jj/working_copy/*` and `~/.config/jj/repos/118d…` mtimes are all `15:26:13`, earlier than my probe (`date` = 15:54:59). So no op was written.
  - [Note: this was the only jj command, and it should not be repeated by gate code; see G6 "never jj".]
- `curl -fsS https://raw.githubusercontent.com/jj-vcs/jj/v0.45.1/{cli/src/config.rs,cli/src/cli_util.rs,lib/src/workspace.rs,lib/src/git_subprocess.rs}`, piped to grep/sed (stdout only, no files written), accessed 2026-10-20, rc 0. One pipeline reported curl rc 23 because grep closed stdout early (`head`). It was re-run without `head`, rc 0.
- `python3 -c` JSON walk of `wave1-spec.json` to read the JjGate and CensusJj item prompts, rc 0.

No selftests run, no journal queries, no `/tmp` writes, no installs or upgrades, no peer messages.
