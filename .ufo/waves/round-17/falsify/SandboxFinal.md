# Round 17 final C2/misroot gate isolation falsification

Scope: C2 jj-regression gate and census sandbox; C3 misroot sweep; C1 fixture-copy special-file path. Static source/receipt review only. No selftests, builds, live probes, or mutations were run. No tools installed. No source remediation was authorized; this report is the only write.

## Findings

### F1 — Medium: FIFO replay can create directories outside its sandbox

**Exploit path.** A fixture pack can contain a symlinked directory pointing outside the copied pack and an expected-table `fifo_files` entry below that link (for example, `link/new/pipe.jsonl`). `_validate_fifo_files` rejects absolute/`..` paths and an existing leaf, but does not reject symlinked ancestors (`tools/mori-round17-seat-regressions.py:556-592`). `_copy_fixture_tree` recreates symlinks (`:857-883`). During replay, `materialize_sandbox` calls `target.parent.mkdir(parents=True, exist_ok=True)` before checking whether the resolved parent is under the sandbox (`:911-928`). A missing directory below the copied symlink is therefore created outside the sandbox before the later containment check raises.

**Impact.** A crafted fixture/expected table can cause out-of-sandbox directory creation under the runner's permissions, despite the output guard and the metadata-only FIFO design. This is a write primitive, not arbitrary file overwrite or code execution.

**Evidence / current control.** The committed `fifo_skipped` case uses flat `pipe.jsonl` metadata; source pack `fixtures/seat/FifoSkip/` contains only `real.jsonl`. The retained `evidence/seat-after/run-manifest.json` case is `match`, records equal `pack_before_sha256`/`pack_after_sha256`, and has `pack_changed:false`. This confirms the measured fixture stayed unchanged; it does not exercise the symlinked-ancestor shape.

**Smallest remediation.** Before any `mkdir`, reject every symlink ancestor of a FIFO path in the copied sandbox and verify containment of the nearest existing parent; create missing components one at a time without following symlinks, then create the FIFO.

### F2 — Medium: C2 output and scratch paths are not constrained

**Exploit path.** `main()` resolves `--output`/`--scratch` and immediately creates the directories, with no empty-directory, containment, or overlap guard (`tools/mori-round17-jj-regressions.py:1154-1167`). The normal run writes case output and truncates `run-manifest.json` at predictable names (`:1255-1256`, `:1303-1304`). A caller can point `--output` into an existing repository or other writable directory and overwrite matching artifacts; `--scratch` can place the generated Git/jj workspaces anywhere writable.

**Impact.** A mistaken or hostile invocation can write into the lane/fleet/source tree, Git metadata, or unrelated user data, contrary to the gate's isolated-sandbox contract. The gate does not itself enforce that the selected paths are owned temporary paths.

**Smallest remediation.** Canonicalize and reject output/scratch paths that overlap the source checkout, census/tool inputs, or protected fleet roots; require output absent or empty. Constrain scratch to a fresh gate-owned directory disjoint from those roots (or to an explicitly validated child of output).

### F3 — Medium: C3's read-only Git calls honor inherited trace-file settings

**Exploit path.** Unlike C2's allowlisted `sanitized_env`, C3 copies the caller environment and removes only eight repository-redirection variables (`tools/mori-misroot-sweep.py:63-90`). `_run_git` passes that environment to both `git status` and `git rev-parse` (`:97-115`, `:213-245`). An inherited file-valued `GIT_TRACE*` setting is not scrubbed; Git can append its trace to the selected path during the otherwise read-only scan. `_selftest_git` also uses the same environment (`:410-417`).

**Impact.** Normal scan can write outside the selected fleet root, falsifying the detection-only/read-only claim and potentially disclosing command/path metadata to an unintended file. This is a static exploit path; it was not exercised.

**Smallest remediation.** Build the Git child environment from an allowlist rather than copying `os.environ`; re-add only required variables such as `GIT_OPTIONAL_LOCKS=0` and a deliberate `GIT_CEILING_DIRECTORIES`. At minimum remove all `GIT_TRACE*` and inherited `GIT_CONFIG*` variables.

### F4 — Low: normal C2 runs retain their sandbox tree

**Evidence.** Normal `main()` creates `run_dir` under `--scratch` (default `<output>/scratch`) and records it as `scratch_run` (`tools/mori-round17-jj-regressions.py:1154-1164`, `:1205-1212`). The normal path has no cleanup; the only `shutil.rmtree(work, ...)` is the selftest's `finally` (`:1118-1119`). The committed before/after manifests retain sandbox paths under the `MainChecks` clone. A read-only `glob` of the recorded after path and its parent returned `Path not found` at audit time, so no tree was retained there then; external clone cleanup is the likely explanation **[INFERENCE]**, not cleanup performed by the gate.

**Impact.** Repeated runs using a persistent scratch directory accumulate Git/jj object stores and per-case homes; when an outer worktree is removed, the manifest's sandbox paths become stale.

**Smallest remediation.** Define an explicit retention policy: clean run sandboxes in `finally` by default, with an opt-in keep mode when forensic retention is required; record whether the paths were retained.

## Controls that held in the inspected C2 path

- **Git environment isolation:** `sanitized_env()` starts empty and copies only `PATH`, locale, timezone, and terminal variables, then sets only the required Git controls; it does not inherit arbitrary `GIT_*` values (`tools/mori-round17-jj-regressions.py:166-199`).
- **jj workspace selection:** each non-init call checks `<repo>/.jj` and uses `jj -R <repo>`; init names the explicit sandbox path and verifies `.jj` afterward (`:249-274`). Git calls use `git -C <repo>` (`:206-207`).
- **Private configuration:** per-case `HOME`, `XDG_CONFIG_HOME`, `JJ_CONFIG`, and Git config paths are directed under the case home (`:180-199`, `:386-396`). The committed after receipt records 12/12 cases matching and `jj_config_redirected` true for both jj cases (`evidence/jj-after/run-manifest.json`, keys `totals` and `cases[].assertions`).
- **No actual remote:** inspected gate code initializes local repositories and uses local Git/jj operations; it has no remote add/fetch/push operation. Its comments explicitly state the sandboxes have no remote (`tools/mori-round17-jj-regressions.py:25-38`). The origin/HEAD resolver input is therefore absent rather than network-backed.
- **No live census surfaces:** the gate overlays fixture files and `MORI_*` paths, places `df`, `pgrep`, `journalctl`, and `tmux` stubs first on `PATH`, directs Git at the sandbox, and runs the census from the sandbox root (`:309-323`, `:386-429`, `:752-755`). The committed after receipt shows 12/12 cases, 0 failed assertions; the jj case output reports fixture-only journal/tmux unavailability, not a live measurement (`evidence/jj-after/run-manifest.json`).
- **C3 normal mode has no output directory argument** and its Git argv is explicit `git -C <fleet-root> status` / `rev-parse`, with no remote operation. Its committed C3-after receipt records the local `git status` command, rc 1, and the retained root artifact candidate (`evidence/c3-after.json`, `argv` and `stdout`). The remaining C3 side-effect is inherited trace configuration (F3).
- **Selftest scratch was not exercised.** C2 selftest cleans its temporary work tree in `finally` (`tools/mori-round17-jj-regressions.py:1061-1069`, `:1118-1119`). C3 selftest uses `tempfile.mkdtemp` without an explicit `dir` and removes it in `finally` (`tools/mori-misroot-sweep.py:466-469`, `:781-782`); its location follows the process temp-directory configuration, so it was not run under the no-/tmp-probe rule.

## Read-only correction closure (2026-10-20)

Compared the settled production tools with the assigned isolated-clone copies using `sha256sum` (rc 0): seat gate `3f3512c41d94c20c5e8aae55ffe17fa219c4c1146ea99e2248d4f924f5da2314` at `tools/mori-round17-seat-regressions.py` and `.ufo/worktrees/round-17/SeatGate/tools/mori-round17-seat-regressions.py`; jj gate `90dee3fafa3387fc008d685bc623e8aeb631ed577a4afacb8aa07e107958e92f` at `tools/mori-round17-jj-regressions.py` and `.ufo/worktrees/round-17/JjGate/tools/mori-round17-jj-regressions.py`; misroot sweep `51072bd7a891fd24779ecadeb4f624de9583c91f798b86f7017ed20b1d6b04c3` at `tools/mori-misroot-sweep.py` and `.ufo/worktrees/round-17/MisrootSweep/tools/mori-misroot-sweep.py`.

### Dispositions

- **F1 closed statically.** Source validation now rejects every existing symlink ancestor before copying (`tools/mori-round17-seat-regressions.py:646-662`); replay uses `_create_fifo_safely`, which lstat-checks and containment-checks existing components before mkdir, then creates missing components one at a time and checks again (`:1117-1184`, called at `:1212-1214`). The old out-of-sandbox `mkdir -p` path is gone.
- **F2 mostly closed; one exact guard bypass remains (Medium).** Output/scratch now have empty/non-symlink/protected-path checks and `/tmp`/`/var/tmp` exclusion (`tools/mori-round17-jj-regressions.py:1188-1218`), with roots/input validation before writes (`:1723-1736`). However, `main()` calls `.resolve()` on both CLI values before passing them to the checkers (`:1718-1721`), while the checkers' symlink rejection tests `path.is_symlink()` (`:1191-1192`, `:1204-1209`). A final-component symlink is therefore already dereferenced when checked: an output symlink to an empty directory outside the protected roots, or a scratch symlink to an allowed writable directory, passes the intended no-symlink guard and writes at its target. The selftest's symlink arm calls `check_output_path` directly with a raw symlink (`:1541-1544`), so it does not exercise the CLI pre-resolution path. **Smallest remediation:** preserve raw CLI paths and reject `is_symlink()` before resolving; then run canonical overlap checks on the resolved paths.
- **F3 closed statically.** C3 now constructs Git environments from `_ENV_ALLOWLIST`, pins global/system config to `/dev/null`, and re-adds only the deliberate discovery ceiling plus fixed Git controls (`tools/mori-misroot-sweep.py:67-100`). The previous inherited trace/config write path is no longer present. The selftest contains poisoned trace/config inputs and checks their paths remain absent (`:488-497`, `:600-621`, `:796-800`); it was not run in this review.
- **F4 closed for ordinary and caught-error runs.** The C2 gate creates a fresh run directory, removes only that directory by default, records cleanup/retention in the manifest, and permits retention only with `--keep-scratch` (`tools/mori-round17-jj-regressions.py:1221-1231`, `:1899-1915`, CLI `:1691-1701`). As documented in source, an uncaught `BaseException` such as interruption can still bypass cleanup. The earlier before/after receipts have the old gate hash and null retention fields; they do not validate the corrected cleanup at runtime.

No post-correction gate or selftest was run. C3 selftest scratch remains governed by the process temp-directory setting and is removed in its `finally` (`tools/mori-misroot-sweep.py:476-478`, `:839-840`); it was not invoked under the no-/tmp-probe rule. Thus the only surviving exact exploit found in the settled source is F2's CLI symlink pre-resolution bypass.

Report: `.ufo/waves/round-17/falsify/SandboxFinal.md`
