# ExecWriteScopeFixture — P-C2 item 6: write-scope fixture + sandbox runner (round 45 wave 1)

Delivered: the fixture, the sandbox runner, and the arm's first-run receipts.
Nothing outside those four paths was written; `SKILL.md` is untouched
(`git status --porcelain SKILL.md` prints nothing at `3ad8faaa` + wave edits).

## Files

| path (absolute) | bytes | lines | sha256 |
|---|---|---|---|
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/fixtures/write-scope.json` | 7169 | 147 | `2af692da8ec5a25f23c40a3a0b73c12335e880d32dbf22eed89ea276a5b8d753` |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/write-scope-run.py` | 19510 | 504 | `e5c8159403e2c5da8b451f65b374a40b4ea9db7715bbddcc47b4fdbc29c6ceed` |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/evidence/write-scope.txt` | 19539 | 408 | `af1baa6f58df7f0d295a0243e54db3eeb3e9bee697c0346277541a96099f3e3c` |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/w1/ExecWriteScopeFixture.md` | this report | | |

Host: linux 7.2.11-arch1-1 x86_64 · python 3.14.8 (`/usr/bin/python3`) · git 2.56.0 ·
`find` 0.8.0 (not GNU findutils, but `-mindepth/-maxdepth/-prune/-type/-exec {} +` all
behave) · GNU tar 1.35. **No tool was installed or upgraded** (no pacman transaction; the
pause was respected).

## Fixture — `.ufo/waves/round-45/fixtures/write-scope.json`

Schema 1. `entries[]` = 7, each `{id, path, row, declared, claim, command, expect, checkable, note?}`:

- `path` repo-relative; `command` an **argv list** (the instrument's own `--selftest`);
- `declared` is the `## Gates` write-scope cell (column 7 of 8) quoted byte-for-byte;
- `expect` = `{rc, stdout_contains[], repo_unchanged, writes_outside_tmpdir}` — what the run
  must reach to count as *exercised* (`["SELFTEST","fail=0"]` + rc 0, token-level so it does
  not rot when a tally moves 6→10);
- `checkable: true` only where a committed cell exists.

The four committed declarations, verbatim:

| row | path | `declared` |
|---|---|---|
| r44 figure ledger (C1) | `.ufo/waves/round-44/count-c1.py` | `stdout only; reads the repo at `--rev`; the selftest writes only under the caller TMPDIR` |
| r44 gate conformance (C2) | `.ufo/waves/round-44/count-c2.py` | `stdout only; counter bytes materialize under the caller TMPDIR; nothing in the repo is written` |
| r44 corpus coverage (C3) | `.ufo/waves/round-44/count-c3.py` | `stdout only; the registry copy handed to the census is materialized under the caller TMPDIR` |
| r44 gate registry (C2) | `tools/mori-gate-registry.py` | `stdout only; reads the registry and the audited paths at `--rev`; the selftest writes only under the caller TMPDIR` |

The three round-45 counter entries (`.ufo/waves/round-45/count-c1.py|c2.py|c3.py`) carry
`declared: null, checkable: false`: at fixture time **no committed SKILL.md cell names them**
(the rows are still being drafted), and I will not invent a declaration. They are present
because the item names them, their `command`/`expect` are fixed, and the runner re-derives the
cell from the measured revision — the moment a row's entry cell names `…/round-45/count-cN.py`
the entry becomes checkable **with no fixture edit**. Until then they report `UNAVAILABLE`
and are never reported TRUE.

`check{}` in the fixture carries the arm's semantics (sandbox, TMPDIR, digest, verdict
definitions, exit map) so a consumer does not have to re-derive them from code.

## Runner — `.ufo/waves/round-45/write-scope-run.py`

```
TMPDIR=<lane-local scratch> python3 .ufo/waves/round-45/write-scope-run.py \
    [--rev REV | --work] [--repo PATH] [--fixture PATH] [--timeout S] [--keep] [--only ID]
```

Setup guards (exit 2, `WRITESCOPE_SETUP reason=<stable>`, never a traceback): `no_tmpdir`,
`tmpdir_is_tmp` (TMPDIR == `/tmp` or under it is refused), `tmpdir_unreadable`,
`fixture_unreadable`, `no_entries`, `unresolvable_revision`, `copy_failed`, `interrupted`,
`internal`, and "no entry was exerciseable".

Per run:

0. a leading `python3`/`python` in the fixture argv resolves to the running interpreter
   (`interpreter=` in the header), so the arm never tests a different interpreter than the
   one it runs under;
1. copy the lane at `--rev` via `git archive … | tar -x -C <sandbox>/lane` (or `--work`:
   tracked + untracked-non-ignored files; wave scratch `\A\.ufo/waves/[^/]+/tmp/` excluded,
   unreadable files skipped and counted);
2. digest: sorted `find . -type f -exec sha256sum {} +` **plus** a recursive all-path listing
   of the sandbox parent (the run root holding `lane/ home/ xdg/ tmp/`), so a write into a
   sibling of the copy is visible too;
3. run the argv with `TMPDIR=<sandbox>/tmp/<id>` — outside `lane/`, so *any* write inside the
   repo is a violation regardless of TMPDIR — and with `HOME`, `XDG_CACHE_CONFIG_DATA_STATE_HOME`
   redirected into the sandbox, `GIT_CEILING_DIRECTORIES=<sandbox>`,
   `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`, and no inherited
   `GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE` (a minimal allowlist env: `PATH HOME TMPDIR TMP TEMP
   XDG_* LANG LC_ALL SHELL GIT_*`); timeout via `start_new_session` + `killpg`;
4. re-digest and diff — created / modified / deleted / `outside_tmpdir` / `tmp_files`.

Per instrument it prints `path`, `declared_source`, `declared_drift`, `declared`, `command`,
`checkable`, `rows_naming`, `rc`, `selftest=<tally line>`, `repo_unchanged=yes|no`,
`writes_outside_tmpdir=<n>`, `observed=<created/modified/deleted/outside_tmpdir/tmp_files/rc>`,
`verdict=TRUE|FALSE|UNEXERCISED|UNAVAILABLE reason=…`, plus the parent listing. Summary:

```
WRITESCOPE instruments=<n> true=<n> false=<n> unexercised=<n> unavailable=<n> \
  writescope_mismatch=<n> rev=<full sha|WORK> repo=<path>
WRITESCOPE=met|unmet
```

Exit **0** all match · **1** a FALSE or UNEXERCISED entry · **2** setup.

`writescope_mismatch` counts only entries that carry a declaration and whose bytes contradict
it (FALSE). `UNEXERCISED` (no write seen, but the selftest did not reach its own tally) also
fails the run but is *not* in `writescope_mismatch`; a consumer that wants a do-nothing
selftest to fail C2 must require `unexercised=0` as well. Messaged to `L1Mori45.ExecC2Counter`
with the full schema.

## First run — `.ufo/waves/round-45/evidence/write-scope.txt`

Six labelled sections; A/B/C are full captured runner output from the shipped bytes
(D restates the verdicts, E describes the control):

| section | measured state | exit | summary line |
|---|---|---|---|
| A | `--rev HEAD` = `3ad8faaa637ae466c61f9427fea1c208bf49ea82` (committed auditor v1) | 0 | `instruments=7 true=4 false=0 unexercised=0 unavailable=3 writescope_mismatch=0` · `WRITESCOPE=met` |
| B | tooth control, throwaway `git init` repo under TMPDIR (commit `9a8d4bf1`) | **1** | `instruments=2 true=1 false=1 … writescope_mismatch=1` · `WRITESCOPE=unmet` |
| C | `--work` at 2026-10-25T10:49:38Z (r45 counters + auditor v2 uncommitted) | 0 | `instruments=7 true=4 false=0 … writescope_mismatch=0` · `WRITESCOPE=met` |

F records the setup guards actually firing — `TMPDIR=/tmp` → `reason=tmpdir_is_tmp`,
unset TMPDIR → `no_tmpdir`, `--rev nosuchrev` → `unresolvable_revision`, absent fixture →
`fixture_unreadable`, each `rc=2` with no traceback.

Retained evidence, quoted:

- A: `lane_files=11830 tree_digest=c5f4a0d68619f6d5d42bc6645cbb031cd6c287cfec9e2226d2cb8f3d7ecb1bdd`,
  each of the four `repo_unchanged=yes` / `writes_outside_tmpdir=0` / `observed=created=0
  modified=0 deleted=0 outside_tmpdir=0 tmp_files=0 rc=0`, tallies `C1 pass=6`, `C2 pass=5`,
  `C3 pass=6`, `GATE_REGISTRY pass=6`, `declared_drift=no` for all four.
- B: clean control `verdict=TRUE`, `tmp_files=1` (TMPDIR bytes counted when they remain);
  dirty control `repo_unchanged=no writes_outside_tmpdir=1
  first_outside=lane/tools/ctl-dirty-out.txt verdict=FALSE`, `EXIT=1`. A false write-scope
  cell cannot print met.
- C: `lane_files=14226 scratch_excluded=2247586 tree_digest=f9f22769…`, r44 four `TRUE`
  (`GATE_REGISTRY pass=10` — the in-flight v2 auditor), r45 three `UNAVAILABLE` but exercised:
  `C1 pass=10`, `C2 pass=8`, `C3 pass=16`, all `repo_unchanged=yes writes_outside_tmpdir=0`.

## Which declarations are TRUE and which are FALSE as written

| row | as written | basis |
|---|---|---|
| r44 figure ledger (C1) | **TRUE** | 2/2 measured states: no repo change, no bytes outside TMPDIR, rc 0, `C1_SELFTEST … fail=0` |
| r44 gate conformance (C2) | **TRUE** | same; `nothing in the repo is written` measured |
| r44 corpus coverage (C3) | **TRUE** | same |
| r44 gate registry (C2) | **TRUE** | same, at v1 (HEAD) and at v2 (working tree) |
| round-45 counters | **not a declaration yet** | no committed write-scope cell names them; reported UNAVAILABLE (never TRUE), exercised clean |

**FALSE: none.** `writescope_mismatch=0` at both measured states.

## Findings and risks the L1 should carry

1. **The cells' negative half is what this arm proves.** Three of the four cells also say
   *where* bytes go ("counter bytes materialize under the caller TMPDIR", "the registry copy
   handed to the census is materialized under the caller TMPDIR"). Those selftests delete
   their `mkdtemp` trees before exit, so `tmp_files=0`: the arm falsifies the *location*
   clause, it does not observe the *materialisation* clause. Control B shows `tmp_files` is
   counted when bytes remain, so the metric is live, not vacuous. Wording for round-46:
   claim "writes no file in the repo outside the caller TMPDIR" and let the materialisation
   be an observed-once note rather than part of the cell.
2. **Coverage today is 4 of 7 entries.** `unavailable=3` is exactly the three round-45
   counters. At the scoring revision, after the round-45 rows land, a scoring run must show
   `unavailable=0` and `checkable` 7/7 (the runner auto-derives). If it still shows
   `unavailable=3`, the rows did not land and C2 item 6 covers only the r44 surface.
3. **`writescope_mismatch` excludes UNEXERCISED on purpose** (a claim with no exercise is not
   a false claim). `count-c2.py` must require `unexercised=0` too, or a selftest that stops
   printing its tally would pass silently. This is in the message to ExecC2Counter.
4. **`--work` enumerates other seats' scratch.** 2 247 586 paths under
   `.ufo/waves/*/tmp/` were enumerated and excluded (24 344 in the first capture, 2.2 M in
   the second as siblings extracted synthetic workspaces), which is why C took 27 s vs 4.5 s
   for A. Scoring should use `--rev`, which copies committed bytes only.
5. **Auditor v2 was mid-flight** when C was captured: `tools/mori-gate-registry.py` is
   uncommitted-modified and printed `GATE_REGISTRY_SELFTEST pass=10 fail=0`, writing nothing
   outside TMPDIR. A at HEAD tested v1 (`pass=6`). If the final v2 changes again, re-run A at
   the scoring revision — the arm is claim-based, not tally-based, so a moved tally does not
   break the fixture.
6. **The arm's reach is filesystem-only.** "stdout only" is consistent with, not proof of, no
   network/secret write; filenames containing a newline are not representable in the
   `sha256sum` digest. Both are stated in the receipt header rather than left implied.

Scratch retained under `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/tmp/ExecWriteScopeFixture/`
(`hdr.txt`, `ftr.txt`, `run-rev-head.txt`, `run-work.txt`, `ctl/`) — my own working files, safe
to delete after integration; the durable receipt is `evidence/write-scope.txt`. No leftover
sandbox: every `mori-writescope-*` run root was removed by the runner (one `--keep` smoke run
was deleted by hand).
