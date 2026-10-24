# PatternConsistency — round-17 wave 2

Seat: `MoriR17.PatternConsistency-4`. Advisory only. No admission, no edit of tools, no selftest, no install.

Axes attacked: C1 coverage (`mori-seat-terminal.py`, `mori-round17-seat-regressions.py`), C2 operability (`mori-census.sh` branch receipt, `mori-round17-jj-regressions.py`), C3 calibration (`mori-misroot-sweep.py`), against the lane conventions already in `SKILL.md` rows, `PROTOCOL.md` Gate standard, `tools/mori-journal-window.py`, `tools/mori-round16-*.py`, `scripts/hyaku/jj-lane.sh` `detect_branch`, and Amendment A1. Conventions checked: `finding_id`, rc maps, `--selftest`, input pins, write scopes, read-only Git env flags, branch-tip provenance.

Installs: none. Pacman is paused; this pass was source comparison only.

Attacked and not listed below: the seat-terminal *scan* path emits `finding_id` with rc 0/1/2 matching A1 and `SKILL.md:173`; the r17 context check copies the r16 `finding_id` / rc 0·1·2 map, including r16's own `SELFTEST_FAIL` on rc 1 (`mori-round16-context-check.py:495`); the seat gate's fixture `pins` are per-file SHA-256 and a mismatch is `snapshot_tampered` rc 2; census C2 probes use the row-1 scrub `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0`.

## Discrepancies

### 1. finding_id — misroot JSON key is `finding`

Existing JSON probes and gates emit `finding_id` (`mori-journal-window.py:493`, `mori-round16-context-check.py:35`, `mori-seat-terminal.py:489`). Amendment A1 item 8 says the output key is `finding_id` (not `finding`) (`contract.md:119`). `SKILL.md` Checklist: "Findings carry a stable id".

`mori-misroot-sweep.py` emits `finding` on the scan path (`:203`, `:322`) and on the selftest document (`:502`, `:749`, `:767`). The selftest asserts `payload.get("finding")` (`:650`). `SKILL.md:176` names `MORI_MISROOT_CLEAN` / `_CANDIDATE` / `_SETUP` in the verdict map and does not record that the key is `finding`, so a reader of the journal/seat key reads no verdict.

Selftest ids `MORI_MISROOT_SELFTEST_OK`, `MORI_MISROOT_SELFTEST_FAIL`, `MORI_MISROOT_SELFTEST_SETUP` are absent from that verdict map.

### 2. rc map — probe selftest reuses the observation rc

`PROTOCOL.md` Gate standard: every exit code is declared, and an undeclared use reads as could-not-evaluate. The existing JSON probe keeps selftest failure off the observation rc: `mori-journal-window.py:710-719` always emits `finding_id=MORI_JOURNAL_WINDOW_SELFTEST` and returns 0 or 2.

| CLI | Registry rc 1 (`SKILL.md`) | Selftest failure actually returns |
|---|---|---|
| `mori-seat-terminal.py` | `MORI_SEAT_TERMINAL_DEAD` (`:173`) | rc 1, `finding_id=SELFTEST_FAIL` (`:1695-1706`). Success is rc 0 with `SELFTEST_OK` (`:1707-1715`), not `MORI_SEAT_TERMINAL_OK`. |
| `mori-misroot-sweep.py` | `MORI_MISROOT_CANDIDATE` (`:176`) | rc `RC_CANDIDATE` (1), key `finding`, id `MORI_MISROOT_SELFTEST_FAIL` (`:745-762`). Success is rc 0 with `MORI_MISROOT_SELFTEST_OK` (`:764-779`). |

Same declared code, two classes, second class missing from the registry row.

`--selftest` flag refusal is also split. Misroot returns setup if any sweep flag is set (`mori-misroot-sweep.py:846-853`). Seat-terminal's epilog says `--selftest` "takes no scan arguments" (`:1742-1744`) but `main` only rejects `--sessions-dir` and `--prefix` (`:1797-1807`). `--now-ms`, `--max-tail-bytes`, `--max-files`, and `--settle-seconds` are accepted and ignored. r15's registry row records that `--selftest` refuses its other flags with rc 2 (`SKILL.md:169`).

### 3. Input pins — registry names frozen files the CLI never opens

`PROTOCOL.md` Gate standard, Two evidences: a frozen baseline's digest is checked before the verdict; a hand-edit of that artifact contradicts the frozen run; a baseline without digests is `unpinned (legacy)`. r14/r15 keep an in-script `PINNED_*SHA256` and exit 2 on mismatch (`SKILL.md:168-169`).

- `SKILL.md:175` pinned values: "frozen entering census under round-17/frozen". `mori-round17-jj-regressions.py` has no `frozen` path and no pinned digest. `--census PATH` is hashed into the manifest (`:1175-1193`) and graded whatever it is. A different census file is a compared verdict, not `snapshot_tampered`. `PINNED_INPUTS.json` records `f1f8d1b62bb617bbcc4664057ab807d3fed8c275b7aabbdf7b373323c5501ff7` for `.ufo/waves/round-17/frozen/mori-census.sh`; this gate does not read that field.
- `SKILL.md:176` pinned values: "retained `round-17/frozen/MoriR16.Lesson`". `mori-misroot-sweep.py` never opens that path. `--selftest` checks embedded base64 against `_ARCHIVE_SHA256` (`:349-391`). The digest string matches `PINNED_INPUTS.json` `15f9f82d…5510e` today; editing the retained file does not move the selftest. The module comment cites the hyaku archive path (`:19-21`, `:343-345`), not `round-17/frozen/MoriR16.Lesson`.

### 4. Write scope — jj gate has no output guard; only one selftest refuses `/tmp`

r15/r16 `guard_output` refuses a symlink, a non-empty directory, the repo root, and `tools/` `.git/` `corpus/` (`mori-round16-regressions.py:727-750`). The seat gate copies that and adds `.jj` (`mori-round17-seat-regressions.py:744-770`).

`mori-round17-jj-regressions.py` `main` does `output.mkdir(exist_ok=True)` and writes `run-manifest.json` with no guard (`:1154-1164`, `:1303-1304`). Default scratch is `<output>/scratch` (`:1156`). Contract: sandboxes are "never in the lane or fleet" (`contract.md:100`). `SKILL.md:175`: "never live lane VCS". The CLI does not enforce either. The jj helper comment states the opposite assumption: "The gate's scratch lives under the lane checkout" (`:250-252`).

Binding wave context forbids `/tmp` probe or scratch writes (`wave1-context.txt:7`). Only the seat gate encodes that: `_selftest_root` refuses an unset `TMPDIR` and refuses `/tmp` and `/var/tmp` (`mori-round17-seat-regressions.py:2158-2167`). `SKILL.md:174` records that refusal. The other new `--selftest` paths call `tempfile.mkdtemp` with no such check:

- `mori-seat-terminal.py:769`
- `mori-misroot-sweep.py:468` (help text says "under TMPDIR", `:828`, which is false when `TMPDIR` is unset)
- `mori-round17-jj-regressions.py:1066-1068` (`--scratch` omitted → `dir=None`). `SKILL.md:175` prints the entry as `--selftest --scratch DIR`; the flag is optional (`:1135-1138`).
- `mori-round17-context-check.py:597`

The pre-r17 census help still documents `${TMPDIR:-/tmp}` (`mori-census.sh:400`). The new seat gate diverges from that help; the other new CLIs follow the help and not the wave ban.

### 5. Branch-tip provenance — three grammars, and `valid_branch` dropped on the receipt

Production census receipt (`mori-census.sh:2168-2169`, `:2443`, `:2446`):

- `head=` and `branch_tip=` are the first 12 hex characters of the full object names, not `git rev-parse --short`
- `HEAD_BRANCH_MISMATCH` observation ends with `basis=merge-base-not-ancestor`
- `LANE_AUTHOR_MISMATCH` uses `count=` (plus committer, window, and `basis=committer-lane-author-foreign-email`)

C2 gate oracle (`mori-round17-jj-regressions.py:244-246`, `:506-514`): `obs_contains` is `lane=<id>` plus `git rev-parse --short` of `HEAD` and of `refs/heads/<branch>`. It does not require the tokens `branch_tip=` or `basis=merge-base-not-ancestor`. Author presence requires only `lane=` (`:516-521`).

Dormant fixture that `--selftest` treats as the amended contract (`:987-999`):

- `branch_tip=` is `git rev-parse --short`, and `basis=` is absent
- author observation is `commits=` not `count=`
- `resolve_branch` (`:914-924`) does not call `valid_branch` and does not apply the census `GIT_DIR` / `GIT_WORK_TREE` / `GIT_INDEX_FILE` scrub

`[INFERENCE]` A two-commit sandbox's default abbrev is shorter than 12, so the 7-character short is a substring of the production 12-character field and the live gate stays green. The selftest still goes green against a fixture grammar the production census does not emit. A census that places those short hashes anywhere in the observation, without the key `branch_tip=`, is graded present.

`valid_branch` (reject `jj/*`, `*..*`, and the charset) is in `scripts/hyaku/jj-lane.sh:85` and `:115-125`, and in `mori-census.sh:2108`. Seat-gate `capture_revision` (`mori-round17-seat-regressions.py:1543-1566`) accepts any `refs/heads/<name>` that `rev-parse --verify` resolves, then stores that as `branch_tip`. A name the census would reject can be the manifest receipt. The manifest records `head` as diagnostic only (`:1567-1572`); that part matches the C2 rule.

Citation split, not a request to delete the third step: `contract.md:90-91` says "like `detect_branch`" and then lists unique `refs/heads/master` / `refs/heads/main`. `detect_branch` returns 1 after `origin/HEAD` with no master/main arm (`jj-lane.sh:115-125`). Census `lane_branch_probe` (`mori-census.sh:2130-2136`) and seat `capture_revision` (`:1558-1563`) implement the contract sentence, not the function. On detached HEAD with no `origin/HEAD` and only `master`, those two resolve `master`; `detect_branch` does not. A1's "unresolved branch => old HEAD behavior" therefore does not fire in that case.

The jj-gate run manifest (`mori-round17-jj-regressions.py:1186-1215`) records gate and census SHA-256 and does not record `branch_tip` or `head`. `PROTOCOL.md` Two evidences: a verdict names the revision it was measured against. The seat gate does (`capture_revision`). This gate does not, and it also does not compare `--census` to the frozen pin in item 3.

## Bounded move

Change only `tools/mori-round17-jj-regressions.py`. Point `mismatch_requirement` and the dormant fixture's `HEAD_BRANCH_MISMATCH` / `LANE_AUTHOR_MISMATCH` strings at the production observation grammar already emitted by `mori-census.sh:2443` and `:2446`: `head=` / `branch_tip=` as the first 12 hex characters, `basis=merge-base-not-ancestor`, and `count=` rather than `commits=`. Do not change census `SURFACE` / `GL_EXTRA` text, rc maps, or C1/C3 files.

Affected axis: C2 operability. The gate would lock the branch-tip receipt it claims to grade. C1 and C3 are untouched, so their rc maps and finding keys stay as they are.

Risk: `--selftest` goes red unless the fixture strings change in the same edit. A census that only emitted `rev-parse --short` (longer than 12) would fail; the delivered census uses the 12-character slice, so that file stays compatible. `[INFERENCE]` No gate was re-run. This move does not fix items 1–4 or the seat receipt's missing `valid_branch`.

Verification for the integrator, not this seat: `TMPDIR` set to a clone scratch that is not `/tmp`, then `python3 tools/mori-round17-jj-regressions.py --selftest --scratch "$TMPDIR"` against the delivered census, and one real `--census tools/mori-census.sh` sandbox case whose `HEAD_BRANCH_MISMATCH` observation contains `branch_tip=` plus 12 hex characters and `basis=merge-base-not-ancestor`. Do not treat a green selftest on the current fixture as that check.
