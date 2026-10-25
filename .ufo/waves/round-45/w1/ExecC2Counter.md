# ExecC2Counter — P-C2 counter (round 45, wave 1)

Scope: build the C2 claim counter at `.ufo/waves/round-45/count-c2.py`, its
single-check mutant, and measure it. No other file touched.

Measured outcome: `C2=unmet` at the frozen entering tip `554ff416…` (that
revision's auditor is v1, so no population mode), `C2=met` with rc 0 on the
working tree once the v2 auditor and the six registry rows are in place
(§B). Counter selftest `C2_SELFTEST pass=14 fail=0` rc 0.

Sentinel findings closed since the first measurement: `MORI_GATE_REGISTRY` is
no longer honoured (`--auditor` only), every child subprocess runs with a
`GIT_*`/`MORI_GATE_REGISTRY`-scrubbed env, the mutant is read at `--rev`
instead of the worktree, and absolute/`..` `--write-scope`/`--mutants-dir`
arguments fail with `C2_SETUP`. All four have dedicated selftest arms (§F).

## Delivered

| path | sha256 | lines |
|---|---|---|
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/count-c2.py` | `153423c48ca90466e85b02707828f5c6b2cf39c87c68ee67e3f9abee956baf93` | 1139 |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/fixtures/mutants/count-c2.py` | `9850b3fcc8885456c3e71458b34184d716d54880a91ae5b29c7d003f26708703` | 1139 |

## Interface

```
python3 .ufo/waves/round-45/count-c2.py <rev|WORK> [--rev REV] [--repo PATH]
        [--auditor PATH] [--write-scope PATH] [--mutants-dir DIR] [--timeout S]
python3 .ufo/waves/round-45/count-c2.py --selftest
```

Exit 0 `C2=met` · 1 `C2=unmet` · 2 `C2_SETUP` (usage, unresolvable revision, git/
subprocess timeout, non-git `--repo`). Defaults: `--auditor` = `$MORI_GATE_REGISTRY`
else `<repo>/tools/mori-gate-registry.py` **at the measured revision**;
`--write-scope` = `.ufo/waves/round-45/fixtures/write-scope.json`;
`--mutants-dir` = `.ufo/waves/round-45/fixtures/mutants` (resolved to the absolute
lane path).

Checks recorded, all named (no traceback path): `auditor_present`, `auditor_v2`,
`auditor_mode`, `population_members`, `tables`, `registered`, `unregistered`,
`no_selftest`, `duplicate`, `wrong_row`, `auditor_rc`, `auditor_selftest`,
`writescope_fixture`, `writescope_entries`, `writescope_mismatch`,
`mutant_present`, `mutant_kill`.

Verdict line carries every counter, `mode=`, `population_digest=`,
`population_members=`, `auditor_selftest=`, `mutant=`, the measured revision and
the repo path.

### Correction 1 and the population-mode directive, as built

* `tables >= 7` (`TABLE_FLOOR = 7`), not 2.
* The auditor is invoked `--audit-all` with **no** `--audit` flag. `auditor_mode`
  requires the stdout tokens `mode=population` **and** `population_digest=`; their
  absence is a named failure, so a narrowed audit cannot print met.
* `population_members` asserts the auditor's buckets partition the declared
  population I enumerate at the revision (`tools/*.py`, `tools/*.sh`,
  `.ufo/waves/round-4[45]/count-c*.py`). In every state C2 admits
  (`unregistered=0`, `no_selftest=0`) that is `registered == member count`; in a
  red state it still catches a truncated audit, which `registered == members`
  alone cannot distinguish from findings.
* When the auditor bytes at `--rev` are the **v1** CLI (it refuses `--audit-all`
  with rc 2), the counter runs the per-path `--audit` fallback purely as a
  measurement and reports `auditor_v2` + `auditor_mode` FAIL — the pre-v2 state,
  named, never met. At the frozen entering tip the committed auditor is v1; the
  working tree now carries v2 (materialized sha256 prefix `8b82ac999091`), which
  prints `mode=population` and a 64-hex `population_digest=`.

### Write-scope arm

Reads the fixture entries; skips an entry when it has no argv, when the fixture
marks it `checkable: false`, or when its path does not resolve at `--rev`. For
every other entry it materializes the reachable tree at `--rev` (git archive of
`SKILL.md`, `corpus/README.md`, `tools`, `.ufo/waves/round-44`,
`.ufo/waves/round-45`; `WORK` copies the same paths and prunes scratch), digests
the copy (rel path → sha256), runs the entry's argv with `cwd=<copy>`,
`TMPDIR=<sandbox>/tmp`, `HOME=<sandbox>/home` and `GIT_DIR`/`GIT_WORK_TREE`/
`GIT_INDEX_FILE`/`GIT_OBJECT_DIRECTORY`/`XDG_CONFIG_HOME` unset, re-digests, and
counts everything written outside the sandbox TMPDIR (changed/added/removed files
in the copy, files in the redirected HOME, entries beside the copy). A
disagreement with the entry's `expect` (`rc`, `repo_unchanged`,
`writes_outside_tmpdir`) is `writescope_mismatch`.

## Selftest tally (final bytes)

```
$ TMPDIR=<lane scratch> python3 .ufo/waves/round-45/count-c2.py --selftest
selftest PASS conformant_met
selftest PASS auditor_absent_unmet
selftest PASS auditor_red_unmet
selftest PASS duplicate_row_unmet
selftest PASS comment_only_selftest_unmet
selftest PASS surviving_mutant_unmet
selftest PASS writescope_mismatch_unmet
selftest PASS narrowed_v1_unmet
selftest PASS registered_mismatch_unmet
selftest PASS tables_floor_unmet
selftest PASS env_auditor_ignored
selftest PASS git_dir_poisoned_ignored
selftest PASS worktree_mutant_not_counted
selftest PASS path_escape_refused
C2_SELFTEST pass=14 fail=0
rc=0
```

The seven required arms (conformant, auditor absent, auditor red, duplicate row,
comment-only selftest row, surviving mutant, write-scope mismatch) plus three
falsifiers for this wave's corrections: `narrowed_v1_unmet` (counters without
`mode=`/`population_digest=`, reached through `--audit-all` only),
`registered_mismatch_unmet` (buckets do not close on the declared population),
`tables_floor_unmet` (`tables=6` fails the 7 floor). Fixtures are throwaway git
repos under `$TMPDIR`; the `conformant` arm also asserts the auditor argv contains
`--audit-all` and **not** `--audit`.

## Trust-boundary arms (sentinel findings §F)

* `env_auditor_ignored`: `MORI_GATE_REGISTRY` pointing at a stub that would
  print `tables=1` + `mode=population` cannot change the measurement — the
  verdict stays the repo's auditor's (`tables=7`, `registered=3`, no
  `deadbeef` digest).
* `git_dir_poisoned_ignored`: a caller's `GIT_DIR`/`GIT_WORK_TREE` pointing at a
  second repo cannot retarget the measured revision or the sandbox copy — the
  verdict still reflects the requested repo.
* `worktree_mutant_not_counted`: a mutant present only in the worktree is
  `mutant_present`/`mutant_kill` FAIL at the measured revision (the same bytes
  are killed at WORK, proving the at-rev read).
* `path_escape_refused`: `/abs/...`, `../...` and `fixtures/../../...` for both
  `--write-scope` and `--mutants-dir` exit 2 with `C2_SETUP`.

## Mutant — exactly one check disabled

`diff -u count-c2.py fixtures/mutants/count-c2.py` is a single hunk; the only
change is the verdict link of the write-scope comparison:

```
@@ -605,8 +605,8 @@
         record("writescope_entries", ws["checked"] >= 1,
                "checked=%d skipped=%d" % (ws["checked"], ws["skipped"]))
-        record("writescope_mismatch", ws["mismatch"] == 0,
-               "mismatch=%d" % ws["mismatch"])
+        record("writescope_mismatch", True,
+               "mismatch=%d (check disabled)" % ws["mismatch"])
```

Killed by the counter's own run:

```
$ python3 fixtures/mutants/count-c2.py --selftest
selftest FAIL writescope_mismatch_unmet: []
C2_SELFTEST pass=13 fail=1
rc=1
```

## Measurements

### A. Frozen entering tip (before-state, committed bytes)

```
$ TMPDIR=<lane scratch> python3 .ufo/waves/round-45/count-c2.py 554ff416459c92f0dea9762f834a556df2990187
C2=unmet tables=unmeasured registered=21 unregistered=14 no_selftest=1 duplicate=unmeasured wrong_row=unmeasured writescope_mismatch=0 mode=absent population_digest=absent population_members=unmeasured auditor_selftest=pass=6/fail=0 mutant=absent checks_failed=auditor_v2,auditor_mode,population_members,tables,unregistered,no_selftest,duplicate,wrong_row,auditor_rc,mutant_present,mutant_kill rev=554ff416459c92f0dea9762f834a556df2990187 repo=/home/vgpnk/Projects/shokunin/mori-shokunin
rc=1
```

The auditor bytes at that revision are v1 (`--audit-all` → rc 2, `unrecognized
arguments`), so `mode=absent` and the narrowed per-path measurement is shown
(36 declared population paths: 21 pass, 14 unregistered, 1 without a real
`--selftest`). Write-scope: 4 entries match (r44 count-c1/c2/c3,
`tools/mori-gate-registry.py`), 3 skipped (the r45 counters do not exist at that
revision), `writescope_mismatch=0`. `mutant=absent` because the mutant is not
committed at that revision — the at-rev read (sentinel §C3) deliberately does
not count the worktree copy.

### B. Working tree, final (registry rows landed) — `C2=met`

```
$ TMPDIR=<lane scratch> python3 .ufo/waves/round-45/count-c2.py WORK
auditor tools/mori-gate-registry.py sha256=8b82ac999091
auditor| tables=7
auditor| rev=WORK
auditor| mode=population
auditor| population_digest=2d1e9096f7622639f3bb45624ffee594caa81c05ee200c9a22323f86d4a9c056
auditor| registered=39 unregistered=0 no_selftest=0 duplicate=0 wrong_row=0 tables=7
auditor| REGISTRY=met
writescope .ufo/waves/round-44/count-c1.py match rc=0 repo_unchanged=yes writes_outside_tmpdir=0 declared='stdout only; reads the repo at `--rev`; the selftest writes only under the caller TMPDIR'
writescope .ufo/waves/round-44/count-c2.py match rc=0 repo_unchanged=yes writes_outside_tmpdir=0 declared='stdout only; counter bytes materialize under the caller TMPDIR; nothing in the repo is written'
writescope .ufo/waves/round-44/count-c3.py match rc=0 repo_unchanged=yes writes_outside_tmpdir=0 declared='stdout only; the registry copy handed to the census is materialized under the caller TMPDIR'
writescope tools/mori-gate-registry.py match rc=0 repo_unchanged=yes writes_outside_tmpdir=0 declared='stdout only; reads the registry and the audited paths at `--rev`; the selftest writes only under the caller TMPDIR'
writescope .ufo/waves/round-45/count-c1.py SKIP (fixture marks it uncheckable)
writescope .ufo/waves/round-45/count-c2.py SKIP (fixture marks it uncheckable)
writescope .ufo/waves/round-45/count-c3.py SKIP (fixture marks it uncheckable)
check auditor_present      PASS (tools/mori-gate-registry.py at WORK)
check auditor_v2           PASS (tables=7 registered=39 unregistered=0 no_selftest=0 duplicate=0 wrong_row=0)
check auditor_mode         PASS (mode=population population_digest=2d1e9096f7622639f3bb45624ffee594caa81c05ee200c9a22323f86d4a9c056)
check population_members   PASS (registered+unregistered+no_selftest+other=39+0+0+0=39 members=39)
check tables               PASS (tables=7 floor=7)
check registered           PASS (registered=39)
check unregistered         PASS (unregistered=0)
check no_selftest          PASS (no_selftest=0)
check duplicate            PASS (duplicate=0)
check wrong_row            PASS (wrong_row=0)
check auditor_rc           PASS (rc=0)
check auditor_selftest     PASS (pass=15 fail=0)
check writescope_fixture   PASS (.ufo/waves/round-45/fixtures/write-scope.json)
check writescope_entries   PASS (checked=4 skipped=3)
check writescope_mismatch  PASS (mismatch=0)
check mutant_present       PASS (.ufo/waves/round-45/fixtures/mutants/count-c2.py)
check mutant_kill          PASS (count-c2.py pass=13 fail=1)
rc=0
```

Measured on the working tree because the v2 auditor and the six registry rows are
still uncommitted; at a committed revision the counter measures that revision's
bytes instead (the auditor is materialized from `--rev`).

### B†. Poisoned-environment receipts (all must stay `C2=met`)

```
$ MORI_GATE_REGISTRY=$TMPDIR/hostile-stub.py python3 .ufo/waves/round-45/count-c2.py WORK
C2=met ... mode=population population_digest=2d1e9096... src=0
$ GIT_DIR=$PWD/.git python3 .ufo/waves/round-45/count-c2.py WORK
C2=met ... rc=0
$ python3 .ufo/waves/round-45/count-c2.py WORK --write-scope /etc/passwd
C2_SETUP path argument must be repo-relative: /etc/passwd       rc=2
$ python3 .ufo/waves/round-45/count-c2.py WORK --mutants-dir ../outside
C2_SETUP path argument escapes the repo: ../outside             rc=2
```

The hostile stub would print `mode=population population_digest=deadbeef
tables=1 registered=1` and exit 0; the verdict ignores it entirely. `GIT_DIR`
pointing at the lane's own `.git` does not retarget anything: every child
subprocess runs under the scrubbed env (`GIT_*`, `MORI_GATE_REGISTRY` removed).

### B′. Intermediate state, before those rows landed (same counter bytes)

Kept for the ledger: the identical command printed `C2=unmet` with
`registered=33 unregistered=6 ... mode=population ... rc=1`, the six
`unregistered` paths being exactly the rows this wave still owed at that moment —
`.ufo/waves/round-45/count-c1.py`, `count-c2.py`, `count-c3.py`,
`tools/mori-disk-rate.py`, `tools/mori-round41-calibration.py`,
`tools/mori-wave-settlement.py`. Nothing in the counter changed between the two
runs; only `SKILL.md` gained the rows.

### C. Exit-2 and absent-auditor receipts

```
$ python3 .ufo/waves/round-45/count-c2.py                     # usage
usage: count-c2.py <rev|WORK> [--rev REV] [--repo PATH] ...
rc=2
$ python3 .ufo/waves/round-45/count-c2.py deadbeefcafe
C2_SETUP cannot resolve revision 'deadbeefcafe'
rc=2
$ python3 .ufo/waves/round-45/count-c2.py 3ad8faaa --auditor <absent path>
C2=unmet tables=unmeasured registered=unmeasured ... checks_failed=auditor_present,auditor_v2,auditor_mode,population_members,tables,registered,unregistered,no_selftest,duplicate,wrong_row,auditor_rc,auditor_selftest rev=3ad8faaa637ae466c61f9427fea1c208bf49ea82 repo=/home/vgpnk/Projects/shokunin/mori-shokunin
rc=1
```

An absent auditor is `C2=unmet` with `auditor_present` named — no
`UnboundLocalError`, no traceback.

## Defects this build exposed and fixed (all in my own bytes)

1. `RecursionError` when `TMPDIR` lives inside the lane: the WORK sandbox copied
   `.ufo/waves/round-45`, which contained the sandbox being built. The copy now
   prunes the sandbox itself, the caller TMPDIR and `.ufo/waves/round-45/tmp`.
2. A sibling seat's scratch under the same `tmp/` carried a dangling symlink, so
   the copy aborted (`cannot copy .ufo/waves/round-45`). Pruning the round scratch
   root (not just my own TMPDIR) fixes it; copy errors now surface as
   `writescope_mismatch`, not a traceback.
3. The fixture auditor's argv receipt was overwritten by its own `--selftest`
   invocation; it now writes the receipt only on the audit call and appends per
   invocation, so the `conformant` arm can assert `--audit-all` without `--audit`.
4. `population_members` first compared `registered` to the population, which fired
   in every red state even when the audit was complete; it now asserts the
   bucket partition, which is the property the assertion exists for.

## Risks and limits

* The write-scope arm measures writes it can see: the copied tree, the redirected
  HOME, and siblings of the copy. A write to an absolute path outside those
  (`/var/...`, the real lane repo) is not observable from inside the sandbox.
  What the arm does prove is that a declared no-write claim survives the
  instrument's own `--selftest` in an isolated copy, and it fails a writer that
  touches the tree (selftest arm `writescope_mismatch_unmet`).
* The mutant is read at `--rev`; `--write-scope` is read from disk inside the
  repo (the fixture is wave-local and uncommitted by design). Both arguments are
  repo-relative and containment-checked — absolute or `..` values fail with
  `C2_SETUP`, at WORK as at a revision. The mutant subject path is only its
  basename, so a stale mutant cannot silently pass — a mutant that stops killing
  fails `mutant_kill`.
* Sandbox population is the reachable tree (`SKILL.md`, `corpus/README.md`,
  `tools`, `.ufo/waves/round-44`, `.ufo/waves/round-45`), not all 11 834 files /
  308 MB at HEAD. Historical waves are not copied; a write into one from inside
  the sandbox would appear as a creation in the copy and still be counted.
* The auditor's population set is verified only through the bucket partition
  against my enumeration. If v2 and I ever disagree about what the population is,
  the check fails rather than picking a winner — that is a round-46 finding.
* Post-integration gate for the L1: the working tree already prints `C2=met`
  (rc 0) on these bytes. After committing the counter, the mutant, the v2 auditor
  and the six registry rows, re-run
  `TMPDIR=<lane scratch> python3 .ufo/waves/round-45/count-c2.py <integration rev>`
  and require the same verdict from committed bytes: `C2=met`, `tables=7`,
  `unregistered=0`, `mode=population`, `population_digest=` present,
  `mutant=killed` (the mutant must be committed along with the counter; at a
  committed revision the worktree copy is deliberately not read). The write-scope
  fixture is wave-local and read from disk inside the repo at any revision.

## Tooling

`pyflakes` 4.0.3 was already present at `/home/vgpnk/.local/bin/pyflakes` (no
install performed; pacman not touched). `pyflakes count-c2.py` → no output, rc 0.
