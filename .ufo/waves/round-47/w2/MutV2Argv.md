# MutV2Argv — round 47 w2 mutation probe: v2 `argv_ok` predicates

Seat: MutV2Argv (leaf, no subagents). Date: 2026-10-25.
Target: `tools/mori-pin-check.py` (v2) — mutated ONLY in scratch copy
`.scratch/r47w2-MutV2Argv/`. Tracked lane path never passed to an edit tool.

## Bytes under test

| what | sha256 |
|---|---|
| working tree `tools/mori-pin-check.py` (before) | `9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6` |
| `git show T:tools/mori-pin-check.py` (T=68d66ca) | `9832e38c…` (identical — working tree equals tip) |
| `git show F:tools/mori-pin-check.py` (F=63eecf2, v1) | `e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1` (matches contract) |

`git status --porcelain -- tools/mori-pin-check.py SKILL.md` → empty (clean).

## Detector (same for pristine / mutated / restored)

`TMPDIR=<scratch> PYTHONDONTWRITEBYTECODE=1 python3 <copy>.py --selftest`; exit 0 with
`PIN_CHECK_SELFTEST fail=0` = detector green. A mutant is **killed** iff its `--selftest`
exits nonzero / prints a FAIL arm; the killing arm is the FAIL line.

**Baseline (pristine):** 34 arms, all PASS, `PIN_CHECK_SELFTEST pass=34 fail=0`, rc 0.
Detector valid — mutant verdicts below are conclusive.

## Mutants (single-point, in `argv_ok` only)

### A — drop the SAFE_PATH check

Diff: `if (not SAFE_PATH.fullmatch(path) or ".." in path.split("/") or "/.scratch/" in "/" + path):`
→ `if (".." in path.split("/") or "/.scratch/" in "/" + path):`
sha256 `2b07d2113442ff1fc2bd618a72551bdcb87182633d0148986b6cb7c4cb31540e`.

- Expected kill arm: `v2_scratch_path_rejected` (or any arm binding a non-`tools/`/`.ufo/` path).
- Actual: `PIN_CHECK_SELFTEST pass=34 fail=0`, rc 0 — **SURVIVED**. Killing arm: **none**.
- Why: the `/.scratch/` clause still rejects the arm's `.scratch/old/foo.py`; the
  `v2_inline_code_rejected` arm (`-c`) is rejected by the argv-tail check, not SAFE_PATH;
  no arm binds a command whose path fails SAFE_PATH alone.

### B — drop the `.scratch` exclusion

Diff: clause `or "/.scratch/" in "/" + path` removed from the same condition.
sha256 `87769442bd1538ac4d54c45e1b1e111b8ea57f98da80aacc3af209553a62f489`.

- Expected kill arm: `v2_scratch_path_rejected`.
- Actual: `PIN_CHECK_SELFTEST pass=34 fail=0`, rc 0 — **SURVIVED**. Killing arm: **none**.
- Why: SAFE_PATH still rejects the arm's `.scratch/old/foo.py` (it does not fullmatch
  `tools/…`/`.ufo/waves/round-N/…`). The two layers are redundant for the one tested path;
  no arm uses a SAFE_PATH-matching scratch path such as `tools/.scratch/x.py`.

### C — accept any trailing args

Diff: `return rest == ["--selftest"] or (rev is not None and rest == [rev, "--selftest"])`
→ `return True`.
sha256 `537c38245f4fb0e6c14424c5136a89eda3561fe22870d908b148dcf341662fde`.

- Expected kill arm: any arm binding a command with extra args (e.g. `--repo DIR --selftest`).
- Actual: `PIN_CHECK_SELFTEST pass=34 fail=0`, rc 0 — **SURVIVED**. Killing arm: **none**.
- Why: no arm binds a nonconforming tail. `bare_flag_rev_entry` cuts `[--repo DIR]` at `[`
  in `derive_command`, and REVTOOL's arg sensitivity is only exercised with the conforming
  `[rev, --selftest]` tail.

## Live-mutant proof (differential `argv_ok` probe, direct call)

| probe argv | pristine | A | B | C |
|---|---|---|---|---|
| `python3 corpus/probe.py --selftest` | False | **True** | False | False |
| `python3 .scratch/old/foo.py --selftest` | False | False | False | False |
| `python3 tools/.scratch/x.py --selftest` | False | False | **True** | False |
| `python3 -c "print('x')" --selftest` | False | False | False | False |
| `python3 tools/foo.py --extra --selftest` | False | False | False | **True** |
| `python3 tools/foo.py --selftest extra` | False | False | False | **True** |
| `python3 tools/foo.py --selftest` (honest) | True | True | True | True |
| `python3 tools/foo.py deadbeef --selftest` (honest) | True | True | True | True |

Each mutant changes exactly its intended predicate and keeps honest commands accepted —
all three are live mutants, not no-ops.

## Verdict

**All three mutants SURVIVE the v2 `--selftest`** (34/34 PASS, rc 0 each). This is a
coverage finding, not permission to change the contract: the v2 selftest never isolates
any single `argv_ok` predicate —

- SAFE_PATH alone is untested (the scratch arm is covered by the `/.scratch/` clause, the
  `-c` arm by the tail check);
- the `/.scratch/` clause alone is untested (SAFE_PATH covers the only scratch arm);
- the strict tail check is untested (no arm passes extra args to a bound command).

Redundancy note: the PAIR (A+B) would be killed by `v2_scratch_path_rejected`
(`.scratch/old/foo.py` would then run and print the stale tally), but each single-point
mutant is equivalent under the current suite. Suggested (not applied) arms: a bound
command with a non-registered path (e.g. `corpus/x.py`), a `tools/.scratch/…` path, and a
bound command carrying an extra arg — each expecting `no_command`.

Scope: this probes the selftest's kill power only. C1's own claim (`PIN_CHECK=met` at T
with the frozen v1 bytes) is not re-judged here, and no tracked byte was changed.

## Restoration evidence

- Tracked `tools/mori-pin-check.py` sha256 after all probes: `9832e38c…` — identical to
  before; `git status --porcelain` for it and SKILL.md empty; HEAD = `68d66ca…` (T).
- Mutations exist only in `.scratch/r47w2-MutV2Argv/{pristine,mutant-a,mutant-b,mutant-c}.py`
  (pristine copy hash = tracked hash; its selftest green = restored-bytes run).
- This seat wrote no other tracked file (the working-tree `LOG.md`/`SCORECARD.md` diffs
  present during the run are not from this seat).
- Commands: all runs used `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-MutV2Argv`;
  no pacman, no mutating git/jj, no subagents.
