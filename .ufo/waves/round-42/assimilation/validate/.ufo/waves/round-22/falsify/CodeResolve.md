# CodeResolve: `resolve()` and its direct call contracts

Seat `MoriR22.CodeResolve`. Round 22. Static read only: no executions, no edits, no delegation, no installs (none were needed).

## Scope and basis

- Target: `tools/mori-retention-reconcile.py`, shipping source (read in full). Line numbers below are its line numbers.
- Call chain: `check` :158 → `resolve` :65–69 → `git_out` :62–63 → `git` :53–60 → `subprocess` :57.
- Read first: `denominator-correction.md` (`#8B0F`). Then `contract.md` (`#1F41`, lines 11, 15, 19), `frozen/requirements-v2.json`, `oracle-reconcile-v2.py` (`#6BDE`), `frozen/fixture-builder-v2.py` (`#74BD`), `refinement-reconcile.py` (`#9C5B`), `measure-round22.py`.
- Git facts: git 2.56.0 docs (rev-parse, gitrevisions, git, git-config). Host git is `git-2.56.0-1` per `/var/lib/pacman/local/`.
- Stale notes not carried forward: `falsify/FinalR22.md` (R13 row, CX4) cites `resolve(repo,measured)` at L161 and a measured-revision path through `git_read_failed` at L59. The shipping file has no such call. Measured-revision validation is at :164–168.
- The denominator correction does not reach `resolve`. No interaction found.

## Axes

A identity and scope (which repository, which object) · B selector semantics · C error and exit contract · D type and schema at the boundary · E acceptance coverage of the contract · F cost.

## Call edges

| Edge | Callee guarantees | Caller relies on | Result |
|---|---|---|---|
| `check` :158 → `resolve` | 40/64-hex commit, or `Invalid` | `revision` is an OID for all later reads | holds (only caller; `a.rev` read only at :158) |
| `resolve` :67 → `git_out` | stdout bytes, or `Invalid` on non-zero exit | single ASCII line | holds; decode error maps to `input_unavailable` (F4) |
| `git` :57 env and `-C` | `GIT_*` scrubbed, `--no-replace-objects`, no lazy fetch | the `-C` path is the repository | identity not bound (F1) |

Every read after :158 uses an OID: `committed(repo,revision,…)` :160, `merge-base --is-ancestor measured revision` :168, and `input_revision` in the output. One `rev-parse` process per run; cost is not material.

## Findings

### F1 · Medium · axis A · latent, operator-triggered

The repository is never bound to `--repo`.

- :158 `repo=Path(a.repo)`. :57 runs `git --no-replace-objects -C str(repo) …`. :54 drops every `GIT_*` variable, including `GIT_CEILING_DIRECTORIES`. :66 validates only the selector. Nothing compares the discovered repository with `repo`.
- `git -C` discovers upward. The git docs define `GIT_CEILING_DIRECTORIES` as "a list of directories that Git should not chdir up into while looking for a repository directory". :54 removes it, so the operator cannot bound discovery either.
- Counterexample A: `--repo "$LANE"` with `LANE` unset passes `''`. `Path('')` is `.`, so discovery starts at the cwd. Run inside any worktree, `resolve` returns that worktree's HEAD and every read comes from it. Exit 0 is possible when that tree holds the named inputs, and no repository identity is emitted.
- Counterexample B, verified on disk: `--repo /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-22/falsify` is a plain directory. `.git` is absent at that path and at `.ufo/waves/round-22/falsify`, `.ufo/waves/round-22`, `.ufo/waves` and `.ufo`. `mori-shokunin/.git` is present, so discovery climbs to `mori-shokunin`. The directory's own files are ignored. Success is silent only if the mori tree also holds the three repo-relative paths and a valid receipt. Otherwise the run fails with `missing_input_blob` (exit 2).
- Output has no field for the discovered repository. `input_revision` is an OID, and `argv` shows the raw string.
- Current harnesses do not trigger it. `measure-round22.py:137` passes the fixed `LANE`. `fixture-builder-v2.py:37` runs `git init` per fixture. `measure-round22.py:140` requires `input_revision == expected`, which would expose a substitution in that harness.
- Direction: reject empty `--repo`. Require `git -C repo rev-parse --absolute-git-dir` to equal `realpath(repo)/.git`, or `realpath(repo)` for a bare repository.

### F2 · Low · axes A, C · latent, operator-typed names only

Ambiguous names resolve by git precedence, and git's warning is discarded.

- :67 passes the raw selector to `rev-parse`. gitrevisions orders the lookup: `$GIT_DIR/<name>`, `refs/<name>`, `refs/tags/<name>`, `refs/heads/<name>`, `refs/remotes/<name>`, `refs/remotes/<name>/HEAD`.
- :57 captures stderr. :63 returns only `.stdout`. `resolve` never reads stderr.
- git-config documents `core.warnAmbiguousRefs` (default true) as warning when a name "might match multiple refs" (lines 2917–2920). That warning would be dropped. Not observed; documented only.
- Counterexample: a tag `main` and a branch `main`. `--rev main` yields the tag's commit, because `refs/tags` outranks `refs/heads`. The report carries no ambiguity signal.
- Current harness is unaffected: `measure-round22.py:137` passes an OID.
- Direction: reject names that match more than one lookup rule, or fail on the ambiguity warning. Alternatively accept only full OIDs and `refs/…` names.

### F3 · Medium · axis E · confirmed gap

No pinned requirement or selftest arm exercises a bad `--rev`.

- `contract.md:15` requires exit 2 for "invalid … revision". `contract.md:19` pins R01–R24. R13 covers the measured revision, R14 ancestry, R20 the receipt path. None covers `--rev`.
- `oracle-reconcile-v2.py:34` always passes `f['rev']`, a valid HEAD.
- `fixture-builder-v2.py:88` (`invalid-revision`) rewrites `measured_revision` and `result['commit']`, not `--rev`.
- `refinement-reconcile.py:161` and `:172` pass valid revisions. `:164` (`symbolic-input`) substitutes `HEAD` and expects exit 0 (`:21`).
- Selftest `tool:258–261` runs four arms: valid, wrong receipt, `../allow.json`, `--unknown`. None uses a bad `--rev`.
- Unpinned reachable branches: `invalid_revision` (:66), `git_read_failed` (:59 via :67), `invalid_resolved_commit` (:68), `git_unavailable` (:58). The contract's exit-2 clause for revision is unverified.
- Arms to add (L1 decision; needs a new freeze): `--rev ''` and `--rev` with a control character give `invalid_revision`. `--rev 'x y'`, `--rev=-x`, an unknown 40-hex name, a tree OID and a blob OID give `git_read_failed`. Each must give exit 2 and `RETENTION_RECONCILIATION_SETUP`.

### F4 · Info · axis C · labels only

- :58 maps `subprocess.TimeoutExpired` to `git_unavailable`, so a slow repository reports "unavailable".
- :67 `.decode('ascii')` raises `UnicodeDecodeError` only on non-ASCII output, which `rev-parse --verify` does not produce. If it did, the error would escape `resolve` and map to `input_unavailable` at :279–280.
- Exit 2 and sanitized reasons hold in both cases.

### F5 · Info · axes C, D · fail-closed false negative [INFERENCE]

- :55 sets `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null`. The git docs define these as skipping system and global config (lines 1791–1800).
- [INFERENCE] git reads `safe.directory` only from those levels, so an operator allowance is ignored. A repository owned by another uid would fail `rev-parse` with `git_read_failed` (exit 2).
- Not material here: the files observed in `round-22` are owned by `vgpnk`.

## Bounded no-findings (checked against shipping source)

- N1 type and schema (:66, :68). `resolve` accepts only a non-empty `str` with no character below 32. argv cannot carry NUL. Output is validated as lowercase 40/64-hex (:20, :68). DEL (127) passes :66 while `safe_path` (:50) rejects it. git's refname rules forbid DEL [INFERENCE], so the outcome is exit 2. Not material.
- N2 option injection (:67). `--end-of-options` precedes the selector. This is the documented idiom (rev-parse docs: `--verify --end-of-options $REV^{commit}`, lines 1164–1165). A `-x` selector becomes a refname and fails.
- N3 peel semantics (:67). `^{commit}` peels annotated tags and rejects trees and blobs (exit 2), as documented in the rev-parse `--verify` section.
- N4 read-only, no network. :54 drops `GIT_DIR`, `GIT_OBJECT_DIRECTORY`, `GIT_CONFIG_*` and the rest. :55 sets `GIT_NO_LAZY_FETCH=1` and `GIT_OPTIONAL_LOCKS=0`. `rev-parse --verify` writes nothing.
- N5 single resolution (:158). All later reads use the OID (:160, :168). No re-resolution by name, so no name-level TOCTOU.
- N6 exit contract. Every `resolve` failure raises `Invalid`, which exits 2 with a fixed reason at :278. Non-`Invalid` exceptions map to `input_unavailable` at :279–280. Git stderr never reaches output (:57 captures it, :63 returns stdout only).
- N7 suffix on `:/` search selectors [INFERENCE, not executed]. `^{commit}` is the documented peel form, and git resolves the base before peeling. `:/` (gitrevisions lines 431–439) is the only grammar that could absorb the suffix. I found no counterexample, so nothing is reported.
- N8 version gates. Host git 2.56.0 documents `--end-of-options` (rev-parse lines 343–345 and 1165), `GIT_CONFIG_GLOBAL` and `GIT_NO_LAZY_FETCH` (lines 1791–1800 and 1992–1995). The tool has no version check. No effect on this host.
- N9 cost (:67). One process per run. Not material.

## Verification gaps

- Nothing was executed. F1 discovery, F2 warning emission for `rev-parse`, F5 `safe.directory`, and N7 come from documentation, code reading, or on-disk checks, not from observed runs.
- No git state was changed. Only read-only file and directory checks and docs reads were used.
- No changes are proposed to be run before integration. If L1 accepts F1 or F3, L1 owns the fix and the new freeze.
