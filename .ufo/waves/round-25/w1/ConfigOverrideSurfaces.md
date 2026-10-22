# ConfigOverrideSurfaces — round 25, claim C2 (scope bound)

Seat: `MoriR25.ConfigOverrideSurfaces` (scout). Claim C2, contract
`.ufo/waves/round-25/contract.md`. Scope: places other than
`~/.omp/agent/config.yml` that can set `async.maxJobs` for an omp session, with a
located quote for each, plus whether `~/Projects/shokunin` or the lane carries a
project-level settings file. Read-only: no config was edited, no `omp` was run.

Binaries/source opened: installed `~/.local/bin/omp` (18.12.6, 256,702,432 bytes,
`strings -a` filtered) and upstream `can1357/oh-my-pi` at tag `v18.12.6`
(downloaded tarball, extracted under `/tmp/omp-tag/oh-my-pi-18.12.6`; line anchors
below are GitHub permalinks at that tag). No tool was installed or upgraded.

## Verdict in one paragraph

`async.maxJobs` is an ordinary registered setting with **no environment binding**.
Four code paths can change its effective value: (1) the global config file (the C2
baseline), (2) a **project** settings file discovered from the session's cwd
(`.omp/config.yml` or `.omp/settings.json`, plus other providers' project files
such as `.claude/settings.json`), (3) explicit **`--config` / `PI_CONFIG_FILES`**
overlays, and (4) in-memory **runtime overrides** (settings API, SDK constructor
`overrides`, injected `Settings` instance). A fifth path bypasses the *setting*
entirely: an SDK caller can inject its own `AsyncJobManager` with any cap. RPC's
`protocolDefault` does **not** override a configured value; it only pins the
default while the setting is unconfigured, and RPC exposes no command that writes
settings. On this host none of paths 2–4 or the injected manager is active, so the
single file the C2 tool reads is the layer that actually supplies the value.

## Precedence (highest first)

From `docs/config-usage.md:174-188` (upstream tag), matching the code in
`#mergeOwnLayers` (`packages/coding-agent/src/config/settings.ts:3912-3916`) and
`getProvenance` (`settings.ts:884-891`):

1. Environment variable declared on the definition (`env: "NAME"`) — **`async.maxJobs` declares none**
2. Runtime overrides (in-memory, never persisted)
3. Config overlays: `PI_CONFIG_FILES` then every `--config` file, later file wins
4. Project settings (discovery capability: `settings.json` and `config.yml`)
5. Global settings: first present of `~/.omp/agent/config.yml`, `~/.omp/agent/config.yaml`
6. Definition default (`100`)

`#mergeOwnLayers`, verbatim from the tag:

```ts
#mergeOwnLayers(layers: OwnLayers): RawSettings {
    let merged = this.#deepMerge(this.#deepMerge({}, layers.global), projectLayerForMerge(layers.project));
    merged = this.#deepMerge(merged, layers.configOverlay);
    return this.#deepMerge(merged, layers.overrides);
}
```

## Surface 1 — global config file (baseline; path itself is overridable)

`packages/utils/src/dirs.ts:32`: `export const MAIN_CONFIG_FILENAMES = ["config.yml", "config.yaml"] as const;`
`settings.ts:675`: `this.#configPath = options.inMemory ? null : path.join(this.#agentDir, MAIN_CONFIG_FILENAMES[0]);`
`settings.ts:2369-2379` (`#readExistingMainYaml`) loops `MAIN_CONFIG_FILENAMES` and returns the
first file that loads, matching `docs/config-usage.md:181`.

`getAgentDir()` (`packages/utils/src/dirs.ts:641-643`) returns `dirs.agentDir`, which
is relocated by three env vars / one flag:

* `OMP_PROFILE` / `PI_PROFILE` — `dirs.ts:44` `const PROFILE_ENV_KEYS = ["OMP_PROFILE", "PI_PROFILE"] as const;`, resolved at `dirs.ts:96`; agent dir becomes `~/.omp/profiles/<name>/agent` (`dirs.ts:336`).
* `PI_CONFIG_DIR` — `dirs.ts:330-331` `return process.env.PI_CONFIG_DIR || CONFIG_DIR_NAME;` (renames the `~/.omp` root under home).
* `PI_CODING_AGENT_DIR` — full agent-dir override, **default profile only** (`docs/environment-variables.md:564`; `dirs.ts:474-503`).
* `--profile <name>` — CLI: `packages/coding-agent/src/commands/launch-help.ts:49` `profile: Flags.string({ description: "Use an isolated profile for auth, sessions, settings, and caches" })`.

Binary confirmation: `strings -a ~/.local/bin/omp | grep -n` →
`382475: var h0 = ["OMP_PROFILE", "PI_PROFILE"];`,
`382610: return process.env.PI_CONFIG_DIR || eh;`,
`382702`/`382706`/`382732-382743` `PI_CODING_AGENT_DIR`,
`382697-382700` `agentDirOverride`.

Current host: no `~/.omp/profiles` entries (`ls -a ~/.omp/profiles` → `.`, `..`),
and `~/.omp/agent/config.yaml` does not exist, so the global layer is exactly
`~/.omp/agent/config.yml:244-245`:

```
244:async:
245-  maxJobs: 200
```

The legacy `~/.omp/agent/settings.json` and `agent.db` rows are read only as a
one-time migration when neither YAML file exists (`settings.ts:2532-2600`, `#migrateFromLegacy`;
binary strings `657620-657700`), so they are not a live override path while
`config.yml` is present.

## Surface 2 — project settings, discovered from the session cwd only

Provider: `packages/coding-agent/src/discovery/builtin.ts:883-940` (`loadSettings`).
For every `{dir, level}` from `getConfigDirs`, it reads `<dir>/settings.json` and
then `<dir>/config.yml`; `builtin.ts:61-73`:

```ts
async function getConfigDirs(ctx: LoadContext): Promise<Array<{ dir: string; level: "user" | "project" }>> {
    const projectDir = normalizePathForComparison(ctx.cwd) === normalizePathForComparison(ctx.home)
        ? null
        : await ifNonEmptyDir(ctx.cwd, PATHS.projectDir);
    if (projectDir) result.push({ dir: projectDir, level: "project" });
```

`PATHS.native.projectDir` is `CONFIG_DIR_NAME` = `".omp"` (`discovery/helpers.ts:49`,
`utils/src/dirs.ts:29`). So the project layer is **`<session cwd>/.omp/` and nothing
above it** — the upward "nearest project `.omp`" walk is documented as belonging to
`SYSTEM.md`/`RULES.md`/`.omp/AGENTS.md` only (`docs/config-usage.md:306-308`,
"Nearest-project lookup nuance"), not to settings. Binary confirmation:
`strings … | grep -n` →
`620375: async function lR(...u) {` (`join`, stat, require non-empty dir),
`620383: async function Ka(u) {` … `await lR(u.cwd, Su.projectDir)`.

Merge into the project layer: `settings.ts:2437-2444` in `#readProjectSettings`
(compiled binary equivalent at strings `657594`/`657610`):

```ts
for (const item of result.items as SettingsCapabilityItem[]) {
    if (item.level === "project") {
        merged = this.#deepMerge(merged, dropSettingsGroupShadows(item.data as RawSettings, item.path));
```

`dropSettingsGroupShadows` (`settings.ts:348-368`) only drops a **non-object** value
sitting on a settings-group prefix; a leaf inside the group passes through. For
`async.maxJobs`: `async` is a group prefix (prefixes of `async.enabled|maxJobs|widgets`,
original id deleted at `settings.ts:335`), and `async` here is an object, so
recursion keeps `async.maxJobs: <n>`. A foreign `"async": 5` would be dropped with
the warning `"Settings: ignoring project setting that would shadow a settings group"`.

Other providers feed the same project layer with their own files, and all of them
are merged at `level: "project"`:

| Provider file | Loader | Note |
|---|---|---|
| `<cwd>/.omp/settings.json`, `<cwd>/.omp/config.yml` | `discovery/builtin.ts:883-940` | native; `settings.json` merges first, `config.yml` last within the dir |
| `<cwd>/.claude/settings.json` | `discovery/claude.ts:530-569` (project item at `:555-568`) | file is shared with Claude Code; `dropSettingsGroupShadows` exists for exactly this |
| `<cwd>/.codex/config.toml` | `discovery/codex.ts:596` registration | TOML provider |
| `<cwd>/.gemini/settings.json` | `discovery/gemini.ts:367` registration | |
| `<cwd>/.cursor/settings.json` | `discovery/cursor.ts:217` registration | |
| OpenCode config files | `discovery/opencode.ts:one()` registration | `opencode.json`/`.jsonc` |

That a `.claude/settings.json` `{"async":{"maxJobs":40}}` reaches the effective value
is **[INFERENCE]** from the merge path above (no test or live instance exercises it);
the native `.omp/config.yml` path is deterministic code, same merge, same leaf rule.

## Surface 3 — `PI_CONFIG_FILES` and `--config` overlays

`settings.ts:676-678`:

```ts
const configFiles = process.env.PI_CONFIG_FILES?.split(path.delimiter).filter(Boolean) ?? [];
if (options.configFiles) configFiles.push(...options.configFiles);
this.#configFiles = configFiles.map(file => path.resolve(this.#cwd, expandTilde(file)));
```

CLI flag: `packages/coding-agent/src/commands/launch-help.ts:56-59`

```ts
config: Flags.string({
    description: "Load an extra config.yml-style overlay for this run (repeatable)",
    multiple: true,
}),
```

Wiring: `packages/coding-agent/src/main.ts:1908-1910`
`Settings.init, { cwd, configFiles: parsedArgs.config }`. Overlay loader is strict:
missing file / invalid YAML / non-mapping root are hard errors
(`settings.ts:2509-2520`, `docs/config-usage.md:196`). Overlay paths resolve
relative to the project dir after `~` expansion (`settings.ts:678`;
`docs/config-usage.md:184`). ACP uses the same resolver
(`docs/approval-mode.md:173`, `:191`).

Binary confirmation: `382...` `PI_CONFIG_FILES?.split` at strings `656491`; overlay
loop `657630-657655`; flag description at strings `925638`/`927599`/`945407` and
`347201`.

## Surface 4 — runtime overrides (highest layer that can carry a value here)

`Setting.override`/`cfgX.override` writes the in-memory layer
(`packages/coding-agent/src/config/registry.ts:728-731` →
`settings.ts:902` `writeValue(..., "override")`; docs `docs/extensions.md:304`: "`override(scope, value)`
writes the in-memory runtime layer; it is never persisted and outranks project,
global, and `--config` layers"). Extensions/hooks can do it from code
(`docs/extensions.md:297-303` example). Settings-panel / `cfg://` writes go to the
**global** layer instead (`docs/config-usage.md:157-162`), i.e. they edit
`config.yml`, not an override.

SDK callers can also construct the store with overrides or supply a whole store:
`packages/coding-agent/src/sdk.ts:873` `settings?: Settings;` and
`:873-877` `settingsManager?: Settings | Promise<Settings>;`; the CLI accepts a
supplied instance at `main.ts:1907-1908` (`deps.settings`). Constructor `overrides`
go through `#overrideLayer` (`settings.ts:691-713`).

Consequence for the cap: the clamp is read **at use time** from the merged value —
`sdk.ts:2282-2286` `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings))` —
so a runtime override can only lower the effective cap; anything above `100` is
still clamped to `100`.

## Surface 5 — SDK `asyncJobManager` injection (bypasses the clamp)

`packages/coding-agent/src/sdk.ts:848-850`:

```ts
/** Parent's async jobs and delivery sinks; child sessions never resolve a process-global manager. */
asyncJobManager?: AsyncJobManager;
```

The session builds its own manager only when there is no parent prefix and only
with the clamped function (`sdk.ts:2277-2286`, verbatim):

```ts
const asyncJobManager = !options.parentTaskPrefix
    ? new AsyncJobManager({
            maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings)),
        })
    : undefined;
```

The manager itself applies no upper clamp — it only floors at 1
(`packages/coding-agent/src/async/job-manager.ts:331-335`: `return Math.max(1,
Math.floor(value ?? DEFAULT_MAX_RUNNING_JOBS));`) and enforces the option at
`job-manager.ts:364-374`. So a host that calls `createAgentSession({ asyncJobManager })`
with its own manager sets the real cap with **no** `Math.min(100, …)`, and a child
session (`parentTaskPrefix` set) uses the parent's manager rather than building one.
Binary confirmation: `strings … | grep -n` → `867745: const Ui = !u.parentTaskPrefix ? new Xm({`,
`867747: maxRunningJobs: () => Math.min(100, XPe.get(R)) }`,
`283603: asyncJobManager`.

## Surface 6 — RPC `protocolDefault` (pins the default, never overrides a configured value)

Definition: `packages/coding-agent/src/tools/settings.ts:941-946`

```ts
export const cfgAsyncMaxJobs = register({
    id: "async.maxJobs",
    protocolDefault: ["rpc"],
    type: "number",
    default: 100,
});
```

No `env:` key on the definition — there is no per-setting environment variable
(confirmed: `grep -in 'max_jobs\|maxjobs'` over the binary strings returns only
`async.maxJobs` / `cfgAsyncMaxJobs`, no env-shaped name).

`packages/coding-agent/src/main.ts:261-272`,

```ts
// Protocol hosts inherit OMP's neutral defaults for settings declaring `protocolDefault`
// instead of the local user's interactive preferences. The pin holds only while nothing
// configures the setting — caller `Settings.isolated` overrides, project `.claude/settings.yml`,
// `--config` overlays, or global `config.yml` always win (#2598, #3207), including a config
// edit the RPC file watcher picks up later and an ACP session's own project config.
function applyProtocolDefaults(host: ProtocolHost, targetSettings: Settings = settings): void {
    for (const setting of all()) {
        if (setting.definition.protocolDefault?.includes(host)) setting.pinDefault(targetSettings);
    }
}
```

`pinDefaultValue` (`settings.ts:1012-1018`):

```ts
pinDefaultValue(setting: AnySetting): void {
    const value = setting.default;
    if (value === undefined || this.isConfigured(setting)) return;
    this.writeValue(setting, value, "override");
    this.#softPins.add(setting);
}
```

Call sites: `main.ts:1939` (`"rpc"`) and `:1941` (`"acp"`). Because `async.maxJobs`
declares `["rpc"]` only, ACP never pins it; RPC pins `100` only when the merged
layers configure nothing. With this host's `async:maxJobs: 200` the pin is skipped
(`isConfigured` → `true`), so RPC behaves like any other mode. RPC also has **no**
settings-write command: `packages/coding-agent/src/modes/rpc/wire/commands.ts`
holds 67 `name:` entries; the only `set_*` entries are
`set_fast_mode, set_slow_mode, set_ask_dialog, set_todos, set_host_tools,
set_host_uri_schemes, set_subagent_subscription, set_event_filter, set_model,
set_thinking_level, set_steering_mode, set_follow_up_mode, set_interrupt_mode,
set_auto_compaction, set_cache_warming, set_auto_retry, set_session_name` — none
touches `async.*`. A config edit reaches a live RPC session through the settings
file watcher (`settings.ts:1116` `startWatching`, `main.ts:265-267`).

Binary confirmation: setting schema at strings `626623-626627`
(`id: "async.maxJobs", protocolDefault: ["rpc"], type: "number", default: 100`),
default gate at `904073-904077` (`if (p.definition.protocolDefault?.includes(u)) p.pinDefault(h);`),
rpc/acp calls at `904906`/`904909`, pin implementation at `656676-656682`.

## Surface 7 — writes that change the global file (not overrides)

`omp config set async.maxJobs N` writes the **global** layer
(`packages/coding-agent/src/cli/config-cli.ts:297` `def.setting.set(settings,
def.setting.parse(value));`; `docs/config-usage.md:157` "`cfgX.set(scope, v)` —
writes the **global** layer"), and `omp config reset` removes the key
(`docs/config-usage.md:158`). The settings panel and `cfg://` device write the same
layer (`docs/config-usage.md:157-162`). These mutate the baseline file, so they do
not create an extra override path; the C2 tool's byte-grammar reader sees their
result.

## Does this host or the lane carry a project-level settings file?

Read-only checks (`ls -a`; no writes):

```
$ ls -a /home/vgpnk/Projects/shokunin | tr '\n' ' '
. .. .devin .git .gitignore .jj .omp .ruff_cache .scratch .tower .ufo AXES.md CORPUS.md
LEARNING.md LOG.md MANIFEST.json MISSION.md PROTOCOL-APPENDIX.md PROTOCOL.md README.md
ROADMAP.md SCORECARD.md audio-shokunin bash:  chousa-shokunin game-dev-2d-shokunin
game-dev-3d-shokunin kagi-shokunin kaidoku-shokunin kake-shokunin kama-shokunin
kasegi-shokunin kengaku-shokunin kotoba-shokunin kotodama-shokunin kumitate-shokunin
local lore-shokunin mado-shokunin mori-shokukin mori-shokunin reports research
revenger-shokunin scripts shokunin.conf souji-shokunin tabi-shokunin tameshi-shokukin
tameshi-shokunin templates tsukuroi-shokunin write

$ ls -a /home/vgpnk/Projects/shokunin/mori-shokunin | tr '\n' ' '
. .. .git .gitignore .jj .scratch .ufo AGENTS.md LOG.md MINT.md PROVINCE.md README.md
SCORECARD.md SHONEN.md SKILL.md considerthese corpus tools

$ ls -d /home/vgpnk/Projects/shokunin/.omp /home/vgpnk/Projects/shokunin/mori-shokunin/.omp
/home/vgpnk/Projects/shokunin/.omp
ls: cannot access '/home/vgpnk/Projects/shokunin/mori-shokunin/.omp': No such file or directory

$ find /home/vgpnk/Projects/shokunin/.omp -maxdepth 2 -type f
/home/vgpnk/Projects/shokunin/.omp/agents/executor.md

$ ls /home/vgpnk/Projects/shokunin/.omp/config.yml \
      /home/vgpnk/Projects/shokunin/.omp/config.yaml \
      /home/vgpnk/Projects/shokunin/.omp/settings.json
ls: cannot access '/home/vgpnk/Projects/shokunin/.omp/config.yml': No such file or directory
ls: cannot access '/home/vgpnk/Projects/shokunin/.omp/config.yaml': No such file or directory
ls: cannot access '/home/vgpnk/Projects/shokunin/.omp/settings.json': No such file or directory
```

(The `bash: ` token in the fleet listing is a literal directory name with a trailing
blank, not an error message; it is unrelated to omp.)

No `.claude`, `.codex`, `.gemini`, `.cursor` or `opencode.json` in either directory
(`ls -a | grep -E '^\.(claude|codex|gemini|cursor)$|^opencode\.json'` → no output,
both paths).

Live session context: the running omp process is pid 2750, `cwd=/home/vgpnk/Projects/shokunin`,
argv `omp` (no `--config`, no `--profile`), and **none** of
`PI_CONFIG_FILES|PI_CONFIG_DIR|PI_CODING_AGENT_DIR|OMP_PROFILE|PI_PROFILE` is set in
its environment; the same holds for the other four `omp` processes on the host
(pids 3591, 9003, 2442876, 3199294). No dotenv files exist at
`~/Projects/shokunin/.env`, `~/Projects/shokunin/mori-shokunin/.env`,
`~/.omp/.env`, `~/.omp/agent/.env`, `~/.env` (existence checks only; a dotenv could
otherwise carry `PI_CONFIG_FILES` — `docs/environment-variables.md:17-25`).

So: **the fleet root has a `.omp/` directory but no settings file inside it, and the
lane repo has no `.omp/` at all.** For this session the project layer resolves to
`/home/vgpnk/Projects/shokunin/.omp` (non-empty, so it is returned by
`ifNonEmptyDir`) and contributes zero items. The lane's absence of `.omp` is
irrelevant to the running session, because settings discovery uses the process cwd
(fleet root), not the repo under work.

## What this means for C2's declared scope bound

The tool's docstring (`tools/mori-job-runway.py:14-17`) says it reads one config file
and that "project-level or environment overrides are out of scope". That is accurate
and the bound is complete with the surfaces above. Two consequences the integrator
should keep in the entry's wording:

1. `effective` equals the session's real cap **only when the baseline file is the
   layer that supplies the value**. A project `.omp/config.yml`, a `--config` /
   `PI_CONFIG_FILES` overlay, or a runtime override can supply a value lower than the
   baseline (e.g. 40); the tool would then report `configured` from the baseline and a
   cap of 100 while the session really allows 40. An override or overlay cannot push
   the cap above 100, because the clamp is applied to the merged value at use time
   (`sdk.ts:2284`).
2. On this host the caveat is inert: no project settings file, no overlay, no
   profile, no relocated agent dir, no runtime override visible from outside, and the
   live run recorded in `w1/BuildJobRunwayTool.md` (`configured 200 / clamp 100 / effective 100`) matches
   `~/.omp/agent/config.yml:245`. The RPC pin cannot change it (configured value wins),
   and no RPC command can write it.

Remaining unknowns (frontier, not needed for the bound): whether any future launcher
passes `--config`/`PI_CONFIG_FILES` or injects `asyncJobManager` (only observable from
that process's argv/env or SDK call site); whether a foreign tool writes
`<cwd>/.claude/settings.json` with an `async` object (possible by code path, not
exercised — [INFERENCE]).
