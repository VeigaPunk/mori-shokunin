# SrcOmpBunOomAdj — does the fleet's harness runtime set `oom_score_adj`?

Seat: scout, round 27 wave 1. Question only: does the fleet's harness runtime (omp, and
the Bun runtime it is built on) set `oom_score_adj` on the processes it spawns?

**Answer: no.** At the installed versions, neither tree contains the string `oom_score_adj`
or `OOMScoreAdjust` anywhere, and neither exposes any option that would reach it. What they
do expose is process placement (cgroup), identity (uid/gid), process group, `PR_SET_PDEATHSIG`
and a nice-only priority call. A child therefore inherits its parent's `oom_score_adj`.

Observed, inference, and gaps are separated below.

## 1. Installed versions (no `omp --version`, no `bun` run for omp)

| Runtime | Version | Evidence |
|---|---|---|
| omp | 18.12.6 | `/home/vgpnk/.omp/agent/last-changelog-version` is 7 bytes, `xxd` → `3138 2e31 322e 36` = `18.12.6`; installed binary `/home/vgpnk/.local/bin/omp` is an ELF x86-64, 256,702,432 B, mtime 2026-10-21 20:37, and embeds `--user-agent=omp/18.12.6` (`strings -n 4 /home/vgpnk/.local/bin/omp \| grep -n 'omp/18.12.6'` → one hit); the tags listing at `https://api.github.com/repos/can1357/oh-my-pi/tags` returns `v18.12.6` as the first name |
| bun | 1.4.3 | `bun --version` → `1.4.3`; tag `bun-v1.4.3` = commit `c6da4a4d3010e5553438c60f6bd76d981976867c` (`https://api.github.com/repos/oven-sh/bun/git/refs/tags/bun-v1.4.3`, HTTP 200) |

[INFERENCE] The installed omp binary is built from tag `v18.12.6`: the version metadata, the
embedded user-agent and the newest release tag agree, but nothing ties the binary's build id
to that commit. No omp package exists in `npm ls -g --depth=0` (it lists `@openai/codex`,
`agent-browser`, `playwright`, `pnpm`, `solc`, `wakaru`, `npm`; no omp entry), and omp's own
`packages/*/package.json` declares `"name": "omp", "private": true`, so the version stamp file
is the only installed-metadata source.

Repository identity: `can1357/oh-my-pi`, taken from existing lane rows S110–S113 and confirmed
by the fetched tree (`package.json` name `omp`, homepage `https://omp.sh`) — no new repository
guess was needed.

## 2. Method (pinned bytes, ordinary access only)

Both sources were fetched as release tarballs with `curl` from codeload, hashed, extracted in
scratch, and searched as whole trees:

```sh
cd /fast/scratch/hyaku/mori-r27/SrcOmpBunOomAdj
curl -sSL -m 600 -o omp-v18.12.6.tar.gz https://codeload.github.com/can1357/oh-my-pi/tar.gz/refs/tags/v18.12.6
curl -sSL -m 900 -o bun-bun-v1.4.3.tar.gz https://codeload.github.com/oven-sh/bun/tar.gz/refs/tags/bun-v1.4.3
tar xzf omp-v18.12.6.tar.gz && tar xzf bun-bun-v1.4.3.tar.gz
sha256sum omp-v18.12.6.tar.gz bun-bun-v1.4.3.tar.gz
```

| Tree | Tarball | Bytes | sha256 | Files searched |
|---|---|---|---|---|
| oh-my-pi `v18.12.6` | `https://codeload.github.com/can1357/oh-my-pi/tar.gz/refs/tags/v18.12.6` | 76,414,434 | `d5c557d2150ac7181d983d6300cfa4f02eab117667a4a5d8b0d4a268059c377e` | 9,294 |
| bun `bun-v1.4.3` | `https://codeload.github.com/oven-sh/bun/tar.gz/refs/tags/bun-v1.4.3` | 77,357,469 | `2366bc56d092f8535bbe5827788e20d987fbc96798de4d683e0ca78ea286ebf4` | 20,093 |

Search commands and output (run 2026-10-22, scratch tree):

```sh
grep -rn --binary-files=without-match -F 'oom_score_adj' oh-my-pi-18.12.6 bun-bun-v1.4.3 | wc -l   # 0
grep -rn --binary-files=without-match -F 'OOMScoreAdjust' oh-my-pi-18.12.6 bun-bun-v1.4.3 | wc -l   # 0
grep -rni --binary-files=without-match -E 'oom[_ -]?score' oh-my-pi-18.12.6 bun-bun-v1.4.3 | wc -l  # 0
```

The same two patterns were re-run through the `grep` device over both extracted trees (not a
shell pipeline): pattern `oom_score_adj|OOMScoreAdjust` → `No matches found`; pattern
`oom[_ -]?score`, case-insensitive → `No matches found`. This is the pinned negative result.

Bun's many `OOM` identifiers are allocator errors, not the OOM score — for example
`src/bun_core/lib.rs:978` `pub type OOM = AllocError;` and `src/bun_core/lib.rs:977` reference
`bun_core::OOM per PORTING.md type map`. They are not evidence either way and were excluded by
the underscore pattern.

## 3. What the runtimes expose instead (located)

omp runs shell commands through native bindings, not through `Bun.spawn`
(`packages/coding-agent/src/exec/bash-executor.ts:8-15` imports `Shell`, `PtySession`,
`ShellFilesystem`, `ShellRunResult` from `@oh-my-pi/pi-natives`; the file header `:4` says
"Uses brush-core via native bindings for shell execution"). Every option a shell session, run
or execute call accepts is a closed napi struct, and none of the three carries a priority,
nice, rlimit or OOM field:

| Struct in `crates/pi-natives/src/shell.rs` @ `v18.12.6` | Fields, with line numbers |
|---|---|
| `ShellOptions` (session, :112) | `session_env` 114, `snapshot_path` 116, `minimizer` 118, `filesystem` 120 |
| `ShellRunOptions` (:136) | `command` 138, `cwd` 140, `env` 142, `timeout_ms` 144, `signal` 146, `filesystem` 149, `streams` 151 |
| `ShellExecuteOptions` (:237) | `command` 239, `cwd` 241, `env` 243, `session_env` 245, `timeout_ms` 247, `snapshot_path` 249, `minimizer` 251, `signal` 253, `filesystem` 255 |

No priority, nice, rlimit or oom field. `crates/pi-shell` handles signalling and process
groups (`crates/pi-shell/src/process.rs:803`, `:1018` `kill_process_group`) but never sets a
kernel OOM score: `grep -rn -E 'process_group\(|setsid|PR_SET_PDEATHSIG|prctl' crates/pi-shell/src
crates/pi-natives/src` returns only `*process_group` helper hits (`kill_process_group`,
`platform_kill_process_group`, `is_self_process_group`).

omp never passes Bun's `cgroup` spawn option, and it carries no systemd integration that could
set `OOMScoreAdjust=`: `grep -rn -E 'ExecStart|\[Service\]' packages scripts` → 0 hits;
`grep -rln 'systemd' packages/coding-agent/src scripts` → 0 files. The whole omp tree mentions
cgroup in five places and none is a spawn option: a comment in
`packages/tui/src/loop-watchdog.ts:30` (cgroup throttling mistaken for sleep), `ps` flag
parsing in `crates/pi-builtins/src/proc_match.rs:509`, a `CGroup:` fixture in
`crates/pi-shell/src/minimizer/defs/systemctl-status.toml:25`, and the kata container-runtime
tuning script `infra/tune-kata-runtime.sh:6-7,107-146` (a GC timer for container cgroups, not
the harness's own children). So every job omp spawns stays in the cgroup of the session that
launched omp.

Bun's side has more knobs, none of them OOM scores:

- `src/spawn_sys/spawn_process.rs:307-350` `PosixSpawnOptions`:
  stdio (308-310), `ipc` (311), `extra_fds` (312), `cwd` (313), `detached` (314),
  `uid`/`gid` (316/318), `argv0` (319), `stream`/`sync` (320-321), macOS exec mode (327),
  `no_sigpipe` (334), `new_process_group` (338, "setpgid(0, 0) in the child"),
  `pty_slave_fd` (340), `linux_pdeathsig` (346), `cgroup_fd` (349). No oom field.
- `src/spawn_sys/spawn_process.rs:347-348`: the cgroup field is "Directory fd of a cgroup the
  child starts inside (`CLONE_INTO_CGROUP`, else a pre-exec `cgroup.procs` write)".
- `src/jsc/bindings/c-bindings.cpp:53-58`: the only priority call is
  `setpriority(PRIO_PROCESS, pid, priority)` (line 58) behind `set_process_priority`.
- `src/runtime/node/node_os.bind.ts:74-76`: that call is wrapped as `os.setPriority` and
  validates `PRI_MIN = -20` … `PRI_MAX = 19` (lines 74-75), i.e. the nice range only.
- `packages/bun-types/bun.d.ts:7701-7725`: the JS-visible `cgroup?: string | number` spawn
  option (doc block 7701-7724, field at 7725) documents that limits "configured on the cgroup
  (`memory.max`, `pids.max`, …) apply from its first instruction" (7706-7707) and that
  "Bun does not create or configure the cgroup; do that with `node:fs` beforehand" (7710-7711).

Teaching for the entry: a job spawned by omp can only be separated from its siblings at the
cgroup level if something supplies a cgroup target, and nothing in omp does. Its OOM score is
whatever it inherits — the runtime contributes no bias of its own, so earlyoom's and the
kernel's view of a fleet child is determined by the session's inherited adj value and by RSS,
not by any harness decision.

## 4. Host corroboration (counts and class labels only)

Read from `/proc/<pid>/oom_score_adj` on 2026-10-22, no signals sent, nothing written:

| Class | Observed value | Note |
|---|---|---|
| `omp` (the session process) | `200` | `oom_score` 877, VmRSS 5,395,272 kB |
| `bash`, `alacritty`, `Hyprland`, `start-hyprland` in that process's parent chain | `200`, `200`, `200`, `200` | chain read via `/proc/<pid>/status` PPid |
| `systemd` (pid <withheld>) | `100` | next link in the same chain; its role is not established here |
| `systemd` (pid 1) | `0` | chain root |
| `python` class | 19 processes, all `200` | class label only |

[INFERENCE] The `200` reaches omp by inheritance from the session launcher chain (it is already
`200` above omp, at `bash` and `alacritty`), and the runtime contributes nothing: this matches
the pinned negative in section 2. Which unit, launcher or profile introduces `200` on this host
is outside this seat — the `HostUnitOomAdjust` and `SrcSystemdUserService` seats own that.

Fleet scripts do not write it either: `grep -rn --binary-files=without-match --exclude-dir=.git
--exclude-dir=.jj -E 'oom_score_adj|OOMScoreAdjust' /home/vgpnk/Projects/shokunin` matches only prose in
documentation and earlier wave reports (e.g. `.ufo/waves/shokunin12h-20261014-p4-mori-r1/members/
CorpusMap.md:452` "no oom_score_adj writes, no kills"); there is no writer.

## 5. Gate block

- URL: `https://raw.githubusercontent.com/can1357/oh-my-pi/v18.12.6/crates/pi-natives/src/shell.rs`
  access 2026-10-22T15:51Z, HTTP 200, 35,623 B,
  sha256 `8a28d0408f7f54854f3dd358833ce0a018bbaded5bce21fbe064d032e6cc03ef`
  (byte-identical to the tarball copy).
- URL: `https://raw.githubusercontent.com/oven-sh/bun/bun-v1.4.3/src/spawn_sys/spawn_process.rs`
  access 2026-10-22T15:51Z, HTTP 200, 41,144 B,
  sha256 `00e8639efff232b94ae2e4a07025a5919177091eac1cc1f956ebd018d17dffb9`
  (byte-identical to the tarball copy).
- URL: `https://raw.githubusercontent.com/oven-sh/bun/bun-v1.4.3/src/jsc/bindings/c-bindings.cpp`
  access 2026-10-22T15:51Z, HTTP 200, 36,976 B,
  sha256 `13f82d5680624a4dbdeadebf511a9784422fff4343a9242a15278b25edab2107`
  (byte-identical to the tarball copy).
- URL: `https://raw.githubusercontent.com/oven-sh/bun/bun-v1.4.3/src/runtime/node/node_os.bind.ts`
  access 2026-10-22T15:51Z, HTTP 200, 1,705 B,
  sha256 `70fa82fef11a7d207d2285573338e24b850e0cd6a28287c12e576aca8539adb6`
  (byte-identical to the tarball copy).
- URL: `https://raw.githubusercontent.com/oven-sh/bun/bun-v1.4.3/packages/bun-types/bun.d.ts`
  access 2026-10-22T15:51Z, HTTP 200, 367,769 B,
  sha256 `c73b98a2b831a772fc5de009b4dc029be6d2dc19dfb2780e98674c709c2f8302`
  (byte-identical to the tarball copy).
- Pinned negative bytes (the whole-tree search basis):
  `https://codeload.github.com/can1357/oh-my-pi/tar.gz/refs/tags/v18.12.6` sha256
  `d5c557d2150ac7181d983d6300cfa4f02eab117667a4a5d8b0d4a268059c377e`;
  `https://codeload.github.com/oven-sh/bun/tar.gz/refs/tags/bun-v1.4.3` sha256
  `2366bc56d092f8535bbe5827788e20d987fbc96798de4d683e0ca78ea286ebf4`.

Verbatim, ≤25 words each, with line numbers at the pinned tags:

> `/// Options for running a shell command.` — `crates/pi-natives/src/shell.rs:134` (omp v18.12.6)

> ``Directory fd of a cgroup the child starts inside (`CLONE_INTO_CGROUP`, else a pre-exec `cgroup.procs` write).`` — `src/spawn_sys/spawn_process.rs:347-348` (bun bun-v1.4.3)

> `return setpriority(PRIO_PROCESS, pid, priority);` — `src/jsc/bindings/c-bindings.cpp:58` (bun bun-v1.4.3)

> `const PRI_MIN = -20;` / `const PRI_MAX = 19;` — `src/runtime/node/node_os.bind.ts:74-75` (bun bun-v1.4.3)

> ``configured on the cgroup (`memory.max`, `pids.max`, …) apply from its first instruction`` — `packages/bun-types/bun.d.ts:7706-7707` (bun bun-v1.4.3)

## 6. Ready-to-paste `corpus/SOURCES.md` row (next free id at read time: S127)

```markdown
| S127 | oh-my-pi v18.12.6 shell-run options and Bun bun-v1.4.3 spawn, priority and cgroup surfaces — https://raw.githubusercontent.com/can1357/oh-my-pi/v18.12.6/crates/pi-natives/src/shell.rs ; https://raw.githubusercontent.com/oven-sh/bun/bun-v1.4.3/src/spawn_sys/spawn_process.rs ; https://raw.githubusercontent.com/oven-sh/bun/bun-v1.4.3/src/jsc/bindings/c-bindings.cpp ; https://raw.githubusercontent.com/oven-sh/bun/bun-v1.4.3/src/runtime/node/node_os.bind.ts ; https://raw.githubusercontent.com/oven-sh/bun/bun-v1.4.3/packages/bun-types/bun.d.ts | code | A | whether the fleet's own runtimes set `oom_score_adj` on children they spawn, and which process-control options they expose instead; the installed omp 18.12.6 and bun 1.4.3 trees only; not this host's unit or launcher values, not the kernel victim formula, not earlyoom's option handling | shell.rs:112 (`ShellOptions`), :136-152 (`ShellRunOptions`, seven fields), :237 (`ShellExecuteOptions`), none with a priority/oom field; spawn_process.rs:307-350 (`PosixSpawnOptions`; `cgroup_fd` doc 347-348); c-bindings.cpp:53-58 (`setpriority(PRIO_PROCESS, …)`); node_os.bind.ts:74-76 (nice range `-20`..`19`); bun.d.ts:7701-7725 (`cgroup?:` spawn option, `memory.max` applies from first instruction); 0 hits for `oom_score_adj` or `OOMScoreAdjust` in 9,294 omp files and 20,093 bun files, and 0 for case-insensitive `oom[_ -]?score`; tag tarballs sha256 d5c557d2150ac7181d983d6300cfa4f02eab117667a4a5d8b0d4a268059c377e (76,414,434 B) and 2366bc56d092f8535bbe5827788e20d987fbc96798de4d683e0ca78ea286ebf4 (77,357,469 B); HTTP 200, 2026-10-22T15:51Z | Neither runtime sets `oom_score_adj`: an omp shell run accepts only command, cwd, env, timeout, signal, filesystem and stream options, Bun's spawn options cover stdio, cwd, uid/gid, detached, process group, pdeathsig and cgroup placement and touch no OOM score, and Bun's one priority call is nice-range `setpriority(PRIO_PROCESS, …)`, so a spawned child inherits its parent's OOM score. | mined | 2026-10-22 | on-release | corpus/knowledge/oom-victim-selection-r27.md |
```

Note on shape: the registry header at `corpus/SOURCES.md:5` is
`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`;
the cell order above matches rows S113 and S126. This is a new row, not an anchor: S112 covers
`tools/bash.ts` and S113 covers `tools/eval.ts`, neither covers `crates/pi-natives/src/shell.rs`
or any Bun file.

## 7. Remaining unknowns

- That the running `/home/vgpnk/.local/bin/omp` executable was compiled from tag `v18.12.6` is
  [INFERENCE] from version-string agreement; no build-id-to-commit mapping exists in the tree.
- The origin of the observed `oom_score_adj=200` on this host is not established here; only the
  runtime's non-contribution is. That attribution belongs to the unit/launcher seats.
- Whether any *other* fleet runtime (not omp, not Bun) writes the value was out of scope; the
  fleet-root grep found no writer in the fleet repo.

## 8. Lane hygiene

- Wrote exactly one file: this report (`.ufo/waves/round-27/w1/SrcOmpBunOomAdj.md`). Scratch:
  `/fast/scratch/hyaku/mori-r27/SrcOmpBunOomAdj/`.
- No subagents, no background jobs, no signals, no unit or settings writes, no pacman, no jj/git
  writes, no omp invocation, no browser.
- Tools installed or upgraded: none.
- Report length: under 300 lines.
