# JjEnvFacts — jj 0.45.1 versions and config-path redirection (round 17, wave 1)

Scope: read-only facts for the C2/JjGate sandbox design: tool versions, where
`jj config path --repo` writes for a fresh sandbox, and how `JJ_CONFIG`, `HOME`,
`XDG_CONFIG_HOME` redirect user vs repo/workspace config. No jj command was run
inside any repo and no sandbox was created; repo-config behavior is derived from
`jj config path --help` plus the v0.45.1 sources, which match the installed binary
exactly (tag check below).

## 1. Tool versions (observed)

Commands run, exit codes, verbatim stdout:

| Command | rc | stdout |
| --- | --- | --- |
| `/home/vgpnk/.local/bin/jj --version` | 0 | `jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5` |
| `git --version` | 0 | `git version 2.56.0` |
| `python3 --version` | 0 | `Python 3.14.8` |

- `command -v jj` → `/home/vgpnk/.local/bin/jj`.
- GitHub tag check (accessed 2026-10-20): `GET https://api.github.com/repos/jj-vcs/jj/git/ref/tags/v0.45.1`
  → `refs/tags/v0.45.1 commit 7c41cdeb16b6b321c64e789a966b6adf723816a5`.
  The embedded version hash **is** the v0.45.1 tag commit, so `v0.45.1` source
  cites below describe the installed binary.
- Host env relevant to the question: `HOME=/home/vgpnk`,
  `XDG_CONFIG_HOME=/home/vgpnk/.config` (set, absolute). `/home/vgpnk/.config/jj`
  exists; `/home/vgpnk/.jjconfig.toml` does not (observed via `ls`; only
  existence checked, no user-config contents read).

## 2. Where `jj config path --repo` writes for a fresh sandbox

For a fresh default-workspace colocated sandbox (a `.jj/repo` directory), the
printed path is:

```
<config_root>/jj/repos/<config-id>/config.toml
```

where:

- `<config_root>` = `$XDG_CONFIG_HOME` if it is set to an **absolute** path,
  else `$HOME/.config`.
  `etcetera 0.11.0` `base_strategy/xdg.rs` `env_var_or_none` keeps
  `XDG_CONFIG_HOME` only when `path.is_absolute()` (lines ~176-186), then
  `config_dir()` = that value or `home_dir/.config/` (lines 194-195);
  `jj` selects this strategy on Linux via
  `etcetera::choose_base_strategy().config_dir()` (`cli/src/config.rs:368-370`).
  On this host that is `/home/vgpnk/.config`, so the printed path would be
  **`/home/vgpnk/.config/jj/repos/<config-id>/config.toml`**.
- `<config-id>` = 20 lowercase ASCII hex characters (10 random bytes;
  `CONFIG_ID_BYTES = 10`, `lib/src/secure_config.rs:40,110`; alphabet
  `0123456789abcdef` in `core/src/hex_util.rs:17,84-87`; validation requires
  exactly 20 hex digits at `lib/src/secure_config.rs:374`).
- The id is stored in the repo as `<repo_dir>/config-id`
  (`SecureConfig::new_repo` → `config-id`/`config.toml`,
  `lib/src/secure_config.rs:166-169`). `repo_dir` is `<sandbox>/.jj/repo`
  (`cli/src/cli_util.rs:381-385, 4609-4612, 4655-4658`); when `.jj/repo` is a
  file it is resolved to the shared repo directory
  (`lib/src/workspace.rs:575-586`).
- The per-id directory also gets `metadata.binpb`, which records the absolute
  repo path (`lib/src/secure_config.rs:39,179-196,202-209`).
- `jj config path --repo` uses the *forcing* loader
  (`repo_config_path` → `load_config`; `cli/src/config.rs:546-552,455-462`;
  `lib/src/secure_config.rs:407-419`), so on a fresh sandbox it **creates**
  `<sandbox>/.jj/repo/config-id` and `<config_root>/jj/repos/<id>/`
  (0700 on Unix, `cli/src/config.rs:264-273`) plus `metadata.binpb`, then
  prints the path.
- The printed `config.toml` itself is **not** created by this call:
  `generate_initial_config` passes `content = None` and
  `generate_config` writes the file only when content is `Some`
  (`lib/src/secure_config.rs:179-209`). Help text agrees: "A config file at
  that path may or may not exist" (`cli/src/commands/config/path.rs:27-35`).
- If the sandbox previously held the legacy `<repo_dir>/config.toml`, the loader
  migrates it: copies the content to a new id directory and (on Unix) replaces
  the legacy file with a symlink to the new config
  (`lib/src/secure_config.rs:289-299,321-352`).
- If no workspace is loaded, `repo_config_path` returns `None` and the command
  exits with `No repo config path found` (`cli/src/commands/config/mod.rs:89-93`);
  a `-R` target without `.jj` fails earlier in workspace loading. So "fresh
  sandbox" must mean jj-initialized (e.g. `jj git init --colocate`), not a bare
  git clone.

Workspace analog (`--workspace`): `<config_root>/jj/workspaces/<config-id>/config.toml`,
id file `<workspace>/.jj/workspace-config-id`, legacy
`<workspace>/.jj/workspace-config.toml` (`lib/src/secure_config.rs:171-177`,
`cli/src/config.rs:61,597-600`).

Help text on generation, verbatim from `jj config path --help` (rc 0):

> If `--repo` or `--workspace` is specified and the config file does not exist,
> jj will generate a new config directory for this repo/workspace and print the
> path to the config file in that directory.

## 3. Which env vars redirect what (jj 0.45.1)

| Layer | Default location | Redirect knobs | Notes |
| --- | --- | --- | --- |
| System config | `/etc/jj/config.toml`, `/etc/jj/conf.d/*.toml` | `JJ_CONFIG` (any value, incl. empty, disables system layer entirely — `cli/src/config.rs:335-346,387`) | — |
| User config | `$HOME/.jjconfig.toml` (lowest precedence, only if it exists), then `<config_root>/jj/config.toml`, then `<config_root>/jj/conf.d/*.toml` in lexicographic order | `JJ_CONFIG` **replaces** this whole list; `HOME` / `XDG_CONFIG_HOME` move the default locations | `JJ_CONFIG` is a `:`-separated list of files/dirs; empty entries are filtered (`cli/src/config.rs:290-296`), so `JJ_CONFIG=` yields zero user layers; docs `docs/config.md:2264-2315` |
| Repo config | `<config_root>/jj/repos/<id>/config.toml`, id in `<repo>/.jj/repo/config-id` | `XDG_CONFIG_HOME` (absolute) or `HOME` (only through the default `<config_root>`); `JJ_CONFIG` has **no effect** | `root_config_dir` is computed from the user config **directory**, not from `JJ_CONFIG` (`cli/src/config.rs:286-288,455-462`); docs `docs/config.md:2297-2306`: "this variable only affects user-level and system-level config files; repo and workspace configs are unaffected ... (There is no environment variable to disable repo or workspace configs.)" |
| Workspace config | `<config_root>/jj/workspaces/<id>/config.toml`, id in `<workspace>/.jj/workspace-config-id` | same as repo config | same |

Consequences, in order of importance for the gate:

1. **`XDG_CONFIG_HOME` is the single knob that isolates both user and repo/workspace
   config**, because `root_config_dir = config_dir/jj` and repo/workspace dirs are
   `root_config_dir/{repos,workspaces}` (`cli/src/config.rs:60-61,286-288,459`).
2. **`JJ_CONFIG=` alone is not sandbox isolation.** It drops user and system
   layers but repo/workspace configs are still discovered from
   `<config_root>/jj/...` and still written there by forcing commands. This
   matters on this host where `XDG_CONFIG_HOME` is already set: changing only
   `HOME` would **not** move the config root.
3. `HOME` matters in three ways: `$HOME/.jjconfig.toml` (read in addition to the
   platform file, lowest precedence, only if present), the default
   `<config_root>` when `XDG_CONFIG_HOME` is unset or relative, and `etcetera`'s
   home directory for `~`/`~user` expansion (canonicalized,
   `cli/src/config.rs:372-376`). If `HOME` is unset/empty, `std::env::home_dir`
   falls back to the passwd entry (`etcetera src/lib.rs:111-114`) — so unsetting
   `HOME` is not a reliable way to hide the user config.
4. `--config-file <PATH>` / `--config NAME=VALUE` are global flags, not env
   vars; they add override layers and do **not** relocate any config directory
   (`docs/config.md:2317-2321`).
5. `JJ_RANDOMNESS_SEED` (u64) seeds the ChaCha20 RNG used to generate config
   ids (`cli/src/config.rs:410-417`; draw in `lib/src/secure_config.rs:110`).
   With a fixed seed, a fresh sandbox's generated id is reproducible for the
   same jj/rand build; this is the only way observed to make
   `jj config path --repo` output deterministic.

## 4. Gate-relevant side effects (observed in code, impact inference)

- Ordinary jj commands in a workspace use the **non-forcing** loader
  (`reload_repo_config` → `maybe_load_config`, `cli/src/config.rs:586-594,359-405`).
  With no `.jj/repo/config-id` and no legacy file, nothing is read or written.
  So `git clone`-style sandboxes gain no repo config until someone runs
  `jj config path/set/edit --repo` (force) or a legacy file exists.
- A sandbox **copied** from another jj repo with `.jj` retained carries the old
  `config-id`; `handle_metadata_path` then sees a metadata path mismatch, detects
  the copy, copies the old config to a **new** id directory under
  `<config_root>/jj/repos/` and rewrites `config-id`
  (`lib/src/secure_config.rs:217-287`). [INFERENCE] For a hermetic gate this is a
  write outside the sandbox whenever `config_root` is the shared user dir.
- Missing the `metadata.binpb` for an existing `config-id` regenerates the id
  directory with the warning `Per-repo config not found. Generating an empty one.`
  (`lib/src/secure_config.rs:48-52,381-392`). [INFERENCE] Gate output parsers
  should tolerate this stderr line only on the forcing path.
- [INFERENCE] Recommended sandbox setup from the above: set both
  `XDG_CONFIG_HOME=<sandbox>/.config` (absolute) and `HOME=<sandbox>` for every
  jj invocation, and use `JJ_CONFIG=` only as an extra belt for user/system
  layers. This keeps ids, `metadata.binpb`, and any copied config inside the
  sandbox. Before it, the C2 gate must accept that a repo-config probe writes
  `<sandbox>/.jj/repo/config-id` (a `.jj` mutation, invisible to git status).

## 5. Remaining unknowns

- Not executed: `jj config path --repo` itself was not run (forbidden: no repo
  execution in this seat's scope, and no assigned clone to create a sandbox in).
  The path/side effects above are read from the exact tag sources and the
  installed binary's embedded help.
- [INFERENCE] Exact `rand` draw→id mapping is stable only for the same
  jj/rand build; treat `JJ_RANDOMNESS_SEED` determinism as same-binary only.
- Not checked: whether any workspace-level config currently exists under
  `/home/vgpnk/.config/jj/workspaces/` (user config directories were not
  enumerated beyond the two `ls` existence checks above).

## 6. Tools and installs

None installed or upgraded. Only `strings(1)` on `~/.local/bin/jj`, `curl`
against raw.githubusercontent.com / api.github.com / crates.io, and the
`jj`/`git`/`python3` version commands were used.

## 7. Mutations

None. This report file is the only write. No VCS, jj, or pacman command ran.

## Sources (all accessed 2026-10-20)

- `jj config path --help` and `jj config path -h` output from
  `/home/vgpnk/.local/bin/jj` (rc 0); `jj --version` (rc 0).
- https://raw.githubusercontent.com/jj-vcs/jj/v0.45.1/cli/src/config.rs
- https://raw.githubusercontent.com/jj-vcs/jj/v0.45.1/cli/src/cli_util.rs
- https://raw.githubusercontent.com/jj-vcs/jj/v0.45.1/cli/src/commands/config/path.rs
- https://raw.githubusercontent.com/jj-vcs/jj/v0.45.1/cli/src/commands/config/mod.rs
- https://raw.githubusercontent.com/jj-vcs/jj/v0.45.1/lib/src/secure_config.rs
- https://raw.githubusercontent.com/jj-vcs/jj/v0.45.1/lib/src/workspace.rs
- https://raw.githubusercontent.com/jj-vcs/jj/v0.45.1/core/src/hex_util.rs
- https://raw.githubusercontent.com/jj-vcs/jj/v0.45.1/docs/config.md
- https://crates.io/api/v1/crates/etcetera/0.11.0/download
  (`src/base_strategy/xdg.rs`, `src/lib.rs`; dependency pinned as
  `etcetera = "0.11.0"` in jj 0.45.1 `Cargo.toml`)
- https://api.github.com/repos/jj-vcs/jj/git/ref/tags/v0.45.1
- https://api.github.com/repos/jj-vcs/jj/commits/7c41cdeb16b6b321c64e789a966b6adf723816a5
  (commit date 2026-09-03T15:45:49Z)
