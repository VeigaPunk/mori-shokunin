# MisrootSweep — round-17 wave 1 (fleet-executor build)

Seat: `MoriR17.MisrootSweep-5` (executor). Advisory evidence for L1 `MoriR17`; I do not judge.
Scope: build the detection-only fleet-root misroot sweep in my clone, run only its own
selftest, and run the delivered tool read-only. This work now serves contract C3
(`.ufo/waves/round-17/contract.md:21-27`) and the byte-exact witness is in the C3 section
below. The r16 failure this replaces is recorded at
`corpus/lessons/round-16-verifier-spotcheck.md:202-206` (addendum pathspec
`-- .ufo/waves .ufo/reports` missed a fleet-root `MoriR16.Lesson`) and
`LOG.md:1105-1109`; the r16 sweep receipt is
`.ufo/waves/round-16/evidence/misroot-sweep.json` (command field shows the pathspec).

## Deliverable

- File: `.ufo/worktrees/round-17/MisrootSweep/tools/mori-misroot-sweep.py` (clone-relative;
  absolute `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MisrootSweep/tools/mori-misroot-sweep.py`).
- Size: 898 lines / 32993 bytes; SHA-256
  `0a852fe67f14afa1da9f5f8e806c63fa640e8df2a90b87909e6a2453c66b3dca`.
- python3 stdlib only (`argparse`, `base64`, `hashlib`, `json`, `os`, `re`, `shutil`,
  `stat`, `subprocess`, `sys`, `tempfile`). No installs were needed (no
  pacman/uv/npm/cargo activity).

Interface exactly as assigned:

```
mori-misroot-sweep.py --fleet-root R --lane ID --round N [--legacy-pathspec P ...]
mori-misroot-sweep.py --selftest
```

- Git query (`:84-116`): `git --no-optional-locks -c core.fsmonitor=false -C R status
  --porcelain=v1 -z --untracked-files=all` with `GIT_OPTIONAL_LOCKS=0`; the `-- P ...` tail is
  appended only when `--legacy-pathspec` is given. `-z` rename/copy records consume their
  second NUL field and are skipped (`:118-146`).
- Repository redirection hardening (`_REDIRECT_ENV` `:69`, `_git_env` `:84`, `_GIT_GLOBAL`
  `:81`, `_git_cmd` `:93`): every git call, including the selftest sandbox's
  `init`/`add`/`commit`, spawns `git --no-optional-locks -c core.fsmonitor=false` with
  `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, `GIT_COMMON_DIR`, `GIT_OBJECT_DIRECTORY`,
  `GIT_ALTERNATE_OBJECT_DIRECTORIES`, `GIT_NAMESPACE` and `GIT_PREFIX` removed from the child
  environment (JjAudit F10 pattern). `GIT_CEILING_DIRECTORIES` is kept deliberately: it only
  bounds upward discovery (it isolates the selftest sandbox) and a poisoned value can force a
  setup failure, never a different repository. The emitted `git_command` shows the effective
  argv; `git version 2.56.0` was observed to accept both flags.
- Every untracked path is `lstat`ed; only regular files are opened, with
  `O_NOFOLLOW | O_NONBLOCK` and an `fstat` re-check, then at most 65536 bytes are read
  (`:167-198`, cap `:50`). Non-regular entries are counted and skipped; nothing is followed.
- Token match (`:149-165`): lane id is case-insensitive with a left guard only
  (`(?<![A-Za-z0-9])mori` — so `Memori` does not match but `MoriR17.Lesson` does); round
  accepts `R17`, `r17`, `round-17`, `round 17`, `round_17`, `round17` with a right digit guard
  (so `R170` is not round 17) and no left guard (seat ids concatenate lane and round).
  Path and head text are both searched; a candidate is emitted when the lane and round tokens
  are each observed in path or content, tagged `"class": "candidate_misroot"` with
  `matched_in` naming the sources and `truncated`/`read_bytes`/`size_bytes`/`read`.
- Output: exactly one sorted-key JSON line on stdout, schema `mori-misroot-sweep-v1`, keys
  `schema`, `finding`, `fleet_root`, `repo_root`, `lane`, `round`, `legacy_pathspec`,
  `git_command`, `scan` (untracked/regular/non-regular/unreadable/truncated/bytes_read/
  read_cap), `candidate_count`, `candidates`, `detection_only`, `moves_or_deletes` (always
  `false`). Findings: `MORI_MISROOT_CLEAN` (rc0), `MORI_MISROOT_CANDIDATE` (rc1),
  `MORI_MISROOT_SETUP` (rc2: `git_missing`, `git_timeout`, `git_status_failed`,
  `arguments_required`, `invalid_round`, `fleet_root_missing`,
  `selftest_takes_no_sweep_flags`). Unknown flags are argparse rc2 (observed: 0-byte stdout,
  201-byte stderr).
- `--help` states the limits (`:789-800`): candidate is a review lead, not ownership proof;
  first 64 KiB only; git-ignored files are invisible; paths are relative to `--fleet-root`;
  `--legacy-pathspec` is comparison-only; detection only, never moves or deletes.

## Selftest evidence (own item; final run on the delivered digest)

Command, run in my clone with scratch TMPDIR:

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MisrootSweep
TMPDIR="$PWD/.scratch" python3 tools/mori-misroot-sweep.py --selftest
{"arms": 11, "finding": "MORI_MISROOT_SELFTEST_OK", "fixture_bytes": 847,
 "fixture_sha256": "15f9f82d707d5c79b11643eed1ab4754b6959d2bede5887e07364442ada5510e",
 "planted_found_with_legacy_pathspec": false, "planted_found_without_pathspec": true,
 "planted_matched_in": ["path"], "sandbox_unchanged": true,
 "schema": "mori-misroot-sweep-v1"}
rc=0
```

The selftest (`:466-788`) builds a fresh `git init` sandbox under `TMPDIR` and plants, at the
sandbox root, `MoriR16.Lesson` holding the **byte-exact archived r16 bytes** (see the C3
section; its content names neither lane nor round — only the name does); plus a sibling `TabiNote.md`
(`TabiR17`), a tracked `tracked.txt` whose committed body also names Mori/round-16, an
ignored `ignored-MoriR16.Lesson` (`.gitignore: ignored-*`), a nested
`.ufo/waves/round-16/build/MoriNote.md`, an empty `MoriR15.note` (path-only match), and a
70 KB `big-notes.txt` whose round token sits beyond the read cap.

Arms (all passed; candidate sets are exact set assertions):

| arm | args | want → observed |
|---|---|---|
| no-pathspec-round16 | Mori/16, no pathspec | rc1, `{nested, MoriR16.Lesson}`, ignored/big/tracked/sibling absent, `truncated_files>=1` |
| legacy-pathspec-round16 | Mori/16, `-- .ufo/waves .ufo/reports` | rc1, `{nested}` only — **planted root file absent** |
| poisoned-env-scans-intended-fleet | Mori/16 with `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` pointing at a decoy repo whose untracked `MoriR16.decoy.md` names Mori+round-16 | rc1, `{nested, MoriR16.Lesson}`, decoy absent, `fleet_root` == intended sandbox, `untracked_entries=5` (decoy holds 1) |
| other-lane-not-flagged | Mori/17 | rc0 clean (`TabiNote.md` not flagged) |
| sibling-detected-for-own-lane | Tabi/17 | rc1, `{TabiNote.md}` (positive control: the zero above is not blindness) |
| unrelated-lane-round | Tameshi/16 | rc0 |
| path-only-match | Mori/15 | rc1, `{MoriR15.note}`, `matched_in=["path"]` |
| round-normalization | `mori` + `R16` | same candidate set as arm 1 |
| invalid-round | `--round sixteen` | rc2 `MORI_MISROOT_SETUP` |
| fleet-root-missing | absent path | rc2 |
| fleet-root-not-repo | non-repo dir | rc2 (arm run with `GIT_CEILING_DIRECTORIES=<tmp>` because the sandbox sits inside a git clone; without the ceiling, `git -C` adopts the enclosing repo) |

The headline booleans are the r16 failure, shown able to fail:
`planted_found_without_pathspec=true` while `planted_found_with_legacy_pathspec=false`, and
the planted candidate is matched by `matched_in=["path"]` with `read_bytes=size_bytes=847`
(file content alone names nothing). The sandbox snapshot taken before the arms is asserted
equal to the archived bytes, and the whole tree (including `.git`) is byte-identical after all
eleven arms (`sandbox_unchanged=true`), which is the no-move/no-delete assertion. The temp tree is
removed in `finally`; `.scratch` was empty after every run.

### Falsifiers of the selftest itself (disclosed extra execution, same own-selftest scope)

Four mutated copies of the delivered digest were written under my clone `.scratch`, run with
the same `TMPDIR`, and deleted; no other code was touched. All four fail the selftest, each on
its intended axis:

- M1 — make the legacy pathspec the default (`pathspecs = pathspecs or [".ufo/waves",
  ".ufo/reports"]`): FAIL, rc1, 14 failures, `planted_found_without_pathspec=false`,
  `planted_matched_in=null`; first failures
  `arm no-pathspec-round16: candidates=['.ufo/waves/round-16/build/MoriNote.md']
  want=['.ufo/waves/round-16/build/MoriNote.md', 'MoriR16.Lesson']` and
  `arm no-pathspec-round16: byte-exact planted witness not detected`.
  This is exactly the r16 regression.
- M3 — disable path matching (content tokens only): FAIL, rc1, 9 failures,
  `planted_found_without_pathspec=false`, `planted_matched_in=null`. The real artifact's
  filename-only shape is therefore required for the green run, not merely tolerated.
- M2 — raise `READ_CAP` to 16 MiB: FAIL, rc1, 5 failures; `big-notes.txt` becomes an
  unexpected candidate and the truncation-cap arm fires.
- M4 — drop the environment scrub (keep the global flags): FAIL, rc1, 3 failures, all in the
  poisoned arm: `candidates=['MoriR16.decoy.md'] want=['.ufo/waves/round-16/build/MoriNote.md',
  'MoriR16.Lesson']` and `unexpected candidate 'MoriR16.decoy.md'`. The intended fleet is still
  scanned in the unpoisoned arms, so this mutant isolates exactly the redirection defence.

## Read-only runs of the delivered tool

| target | command | observed |
|---|---|---|
| fleet root | `--fleet-root /home/vgpnk/Projects/shokunin --lane Mori --round 17` | rc0 `MORI_MISROOT_CLEAN`, 0 candidates, `untracked_entries=10`, `regular_files=10`, `bytes_read=13264`, `repo_root=/home/vgpnk/Projects/shokunin` (2026-10-20T18:58:54Z) |
| fleet root (post-C3 digest) | same command | rc0 `MORI_MISROOT_CLEAN`, 0 candidates, `untracked_entries=9`, `regular_files=9`, `bytes_read=612`, `repo_root=/home/vgpnk/Projects/shokunin` (2026-10-20T19:10:33Z) |
| fleet root (post-hardening digest) | same command; emitted `git_command` = `["git", "--no-optional-locks", "-c", "core.fsmonitor=false", "-C", "/home/vgpnk/Projects/shokunin", "status", "--porcelain=v1", "-z", "--untracked-files=all"]` | rc0 `MORI_MISROOT_CLEAN`, 0 candidates, `untracked_entries=9`, `regular_files=9`, `bytes_read=612` (2026-10-20T19:15:07Z) |
| same, legacy pathspec | plus `--legacy-pathspec .ufo/waves --legacy-pathspec .ufo/reports` | rc0, 0 candidates, `untracked_entries=1` (fewer entries visible than the full sweep) |
| lane checkout (advisory, pre-refinement; matcher unchanged) | `--fleet-root .../mori-shokunin --lane Mori --round 17` | rc1, 37 candidates of 42 untracked files; every candidate is under `.ufo/waves/round-17/build/` (the lane's own reports); 424155 bytes read, 2 truncated |

The fleet-root baseline at read time was 10 untracked entries at 18:58:54Z (`.ufo/reports/round-19/mado.md`
and nine `.ufo/state/*.report-baseline` files) and 9 at 19:10:33Z, plus one modified tracked file
(`.ufo/watchdog.log`), with no fleet-root file naming Mori + round 17. Counts moved between
runs (10 → 1 → 10 → 9 untracked) as sibling seats wrote and removed files, so these are
point-in-time observations, not a stable baseline.

## C3 calibration witness (contract.md:21-27; L1 refinement 2026-10-20)

Contract C3 declares: on a sandbox retaining byte-exact `MoriR16.Lesson` content, the legacy
`.ufo/waves .ufo/reports` pathspec misses the root file while the no-pathspec,
filename-or-content detector finds it; missed known artifacts **1→0**; sibling and tracked
controls stay unclaimed.

Artifact provenance (read-only):

- `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/misroots/MoriR16.Lesson` (the relocated r16
  fleet-root file), 847 bytes, SHA-256
  `15f9f82d707d5c79b11643eed1ab4754b6959d2bede5887e07364442ada5510e`, read 2026-10-20.
- A byte scan (case-insensitive regex) of those 847 bytes finds no `Mori` token, no
  `R16`/`round-16` token, and no `R17` token: the artifact names lane and round only in its
  filename, confirming CriticFrontier's observation on the bytes themselves.

Implementation delta (fixture and assertions only; candidate matching already searched path OR
content before this refinement — `_scan` `:213`, path token checks `:290-294`):

- `_ARCHIVE_SHA256` (`:349`) and `_ARCHIVE_B64` (`:352`) pin the archived bytes; `_archive_bytes()`
  (`:384`) decodes them and refuses on digest mismatch (`MORI_MISROOT_SELFTEST_SETUP`).
- `_write_bytes` (`:402`) plants them under `MoriR16.Lesson`. The selftest asserts that the
  pre-arm snapshot bytes equal the archive, and that the no-pathspec candidate carries
  `matched_in=["path"]` with `read_bytes=size_bytes=847` (no content match), while the
  `--legacy-pathspec .ufo/waves .ufo/reports` arm does not contain the file.
- Both selftest payloads now emit `fixture_sha256`, `fixture_bytes`, `planted_matched_in`.

Reproduction (read-only; the sandbox is removed in `finally`, so the printed fixture keys are
the retained witness):

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MisrootSweep
$ python3 -B - <<'PY'   # pinned literal decodes to the archive digest
import importlib.util, hashlib
spec = importlib.util.spec_from_file_location("m", "tools/mori-misroot-sweep.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
d = m._archive_bytes(); print(len(d), hashlib.sha256(d).hexdigest())
PY
847 15f9f82d707d5c79b11643eed1ab4754b6959d2bede5887e07364442ada5510e

$ sha256sum /home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/misroots/MoriR16.Lesson
15f9f82d707d5c79b11643eed1ab4754b6959d2bede5887e07364442ada5510e  .../MoriR16.Lesson

$ TMPDIR="$PWD/.scratch" python3 tools/mori-misroot-sweep.py --selftest
{"arms": 11, "finding": "MORI_MISROOT_SELFTEST_OK", "fixture_bytes": 847,
 "fixture_sha256": "15f9f82d707d5c79b11643eed1ab4754b6959d2bede5887e07364442ada5510e",
 "planted_found_with_legacy_pathspec": false, "planted_found_without_pathspec": true,
 "planted_matched_in": ["path"], "sandbox_unchanged": true,
 "schema": "mori-misroot-sweep-v1"}
rc=0
```

C3 measurement on this witness: known misroot artifacts missed **1→0**; the sibling
`TabiNote.md` (Tabi/17, arm 4) and the tracked/ignored controls stay unclaimed. Content-token
coverage is still witnessed separately by `.ufo/waves/round-16/build/MoriNote.md` (its content
names `MoriR16`), so replacing the synthetic planted body did not drop that path. Mutation M3
(path matching disabled) fails the selftest, so the filename-only shape is required for green.

## Limits and risks

- A candidate is a review lead, not proof of seat ownership; act only after reading the file
  header, as r16 did with attribution.
- Only the first 64 KiB of each regular file is inspected; a round token past that offset and
  path-only naming is still caught, content past it is not.
- Git-ignored files are unreachable through `git status`, and modified tracked files are not
  scanned — the sweep covers the r16 mechanism (an untracked file written into the fleet
  checkout), not every possible outside-lane write.
- Pointing the tool at the lane itself yields its own round-17 reports as candidates (37 at
  read time). That is expected; the fleet root is the intended target.
- `git -C R` adopts an enclosing repository when `R` is a subdirectory; `repo_root` is emitted
  so the caller can see it. Paths stay relative to `R`, which is what the tool reads.
- Matching is lexical: lane ids are left-guarded only, round tokens are not left-guarded
  (seat ids concatenate them), and `mori` also matches the lane checkout path
  `/home/.../mori-shokunin`. Candidates are deliberately over-inclusive.

## Discipline

- No tool installs or upgrades; no pacman/uv/npm/cargo; no network; no `/tmp` writes (all
  scratch under `<clone>/.scratch` via `TMPDIR`); no background jobs; no journalctl.
- No VCS mutation in the lane, fleet root, or my clone. The selftest's `git init/add/commit`
  runs only in the throwaway sandbox under `TMPDIR` (a nested repo inside `.scratch`, removed
  afterwards); main queries use `GIT_OPTIONAL_LOCKS=0`.
- Writes: the assigned tool in my clone and this report. Clone `git status` at completion:
  `?? tools/mori-misroot-sweep.py` (scratch clean).
- Verdict: capability delivered and self-falsified; fleet root was clean at the observed time.
