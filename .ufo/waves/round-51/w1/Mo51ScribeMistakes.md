# Mo51ScribeMistakes — draft `## Mistakes` for `corpus/lessons/round-51.md`

Seat: Mo51ScribeMistakes (scribe, mori round 51 wave w1). Item: draft the `## Mistakes` section of the
round-51 lesson, with rows M1 (hidden location dependence) and M2 (round-50 residue producers), columns
`id | class | evidence | captured-by | fix | shown able to fail`.

Frozen contract: `.ufo/waves/round-51/contract.md` (sha256 `e5b02168c7…`, per
`.ufo/waves/round-51/evidence/freeze-sha256.txt`). Data commit reviewed: `87e0c374…`. Entering tip: `aa3af1ec…`.

Provenance of this report: every number below is from a committed or frozen byte I read, or from a command I ran
in my own scratch (outputs quoted). I did not author a lane file, run a counter, run a control, or re-execute a
lane gate. This seat is not an entailment seat, so this report records no claim-entailment vote and no line of it
begins with the four-letter vote keyword.

Scratch: `/fast/scratch/hyaku/mori-r51/Mo51ScribeMistakes/` with `TMPDIR` under it; removed before this report was
written. No tool was installed or upgraded; no pacman transaction was attempted.

## 1. Freeze and receipt integrity

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ sha256sum -c .ufo/waves/round-51/evidence/freeze-sha256.txt 2>&1 | grep -c ': OK$'
21
$ sha256sum -c .ufo/waves/round-51/evidence/freeze-sha256.txt 2>&1 | grep -v ': OK$'
(no output)
```

All 21 frozen entries match, including the six C1 control receipts cited below
(`control-c1-do-nothing.txt`, `-scratch-only`, `-conform-only`, `-class-only`, `-always-env`, `-witness`). So the
receipts are the bytes the freeze names, and the numbers I quote are the frozen numbers.

Data-commit surface (for the L1's context; I did not change any of it):

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --stat aa3af1ec 87e0c374 -- \
    tools/mori-pin-check.py .ufo/waves/round-40/conform.py SKILL.md SHONEN.md
 .ufo/waves/round-40/conform.py |   7 ++-
 SHONEN.md                      |   2 +-
 SKILL.md                       |   2 +-
 tools/mori-pin-check.py        | 137 ++++++++++++++++++++++++++++++++---------
 4 files changed, 115 insertions(+), 33 deletions(-)
```

## 2. Evidence for M1 — the hidden location dependence

Read at `aa3af1ec` (read-only `git show` into my scratch, then read/grep there):

- `tools/mori-pin-check.py:884` — `scratch_parent = os.path.join(repo, ".scratch")`; the export itself is
  `:844-862` (`git archive --format=tar`, extracted to `<dest>/tree`), i.e. a full tree **inside** the repo it
  measures.
- `.ufo/waves/round-49/count-c1.py:52-53` — `HERE = os.path.dirname(os.path.abspath(__file__))`,
  `LANE = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))`; `:313` — `"--rev": "master"` is the default;
  `:353` — `git -C LANE rev-parse --verify master^{commit}`; `:422` — the same call again as the
  `lane_head_unchanged` arm.
- `tools/mori-round19-regressions.py:844` — `repo = resolved.parents[4]` (the tree the file runs in);
  `:854` — `["git", …, "-C", str(repo), "show", ORACLE_REVISION + ":" + ORACLE_RELATIVE_PATH]`, whose failure path
  raises `pinned-oracle-unavailable` (`:862-863`).
- `.ufo/waves/round-40/conform.py:69-70` — `LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"`,
  `SCRATCH_ROOT = os.path.join(LANE, ".ufo", "waves", "round-40", "scratch")`; `:522` —
  `run(["git", "-C", repo, "rev-parse", "HEAD"])` with `repo` defaulting to `LANE` (`:773`).

Demonstration that a subtree of a repository resolves git objects through the enclosing repository (my fixture,
`git -C` asserted on every call; fixture removed afterwards):

```
$ git -C "$D" init -q && git -C "$D" rev-parse --show-toplevel
/fast/scratch/hyaku/mori-r51/Mo51ScribeMistakes/tmp/tmp.FanpSAtPk6
$ mkdir -p "$D/.scratch/exp/tree/tools" && echo x > "$D/.scratch/exp/tree/tools/a.py"
$ git -C "$D/.scratch/exp/tree" rev-parse --show-toplevel
/fast/scratch/hyaku/mori-r51/Mo51ScribeMistakes/tmp/tmp.FanpSAtPk6        # rc=0
$ git -C .../tmp/bare rev-parse --show-toplevel                          # same tree shape, no enclosing repo
fatal: not a git repository (or any parent up to mount point /)
Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set).  # rc=128
```

That is the defect in one line: inside the repo the pin read the lane's objects and passed; outside it has no
repository at all.

Receipt (`evidence/control-c1-scratch-only.txt`, frozen):

```
C1=unmet kill_residue=0 relocated=unmet reloc_mismatch=3 classified=bad selftest=pass=114,fail=0 \
  rev=cb0a8c5255f15015961b70b38a604a9d4fd83603 failed=relocated,classified
exit=1
```

`reloc_mismatch` counts lines carrying `state=mismatch` or `state=no_command` (`.ufo/waves/round-51/count-c1.py:149`),
so 3 = three pins red. The counter writes those lines to `<scratch>/relocated.out` (`:144`) inside scratch that it
removes, and the receipt keeps only the count — so the identification of the three pins with the three instruments
above comes from `contract.md` (C1 surface paragraph) plus my code reading, not from a committed per-pin line. I
say that in the row and repeat it as a finding.

## 3. Evidence for M2 — the residue producers

- Round-50 spot-check D-d (`corpus/lessons/round-50-verifier-spotcheck.md:45-49`) and its routed defect 1
  (`:173-174`), which name `tools/mori-pin-check.py:884-887` and `.ufo/waves/round-40/conform.py:69`.
- At the entering tip, `evidence/control-c1-do-nothing.txt`:

```
kill_residue_first: !! .scratch/pin-check-uphozg94/tree/.gitignore
C1=unmet kill_residue=12547 relocated=unmet reloc_mismatch=1 classified=bad selftest=pass=114,fail=0 \
  rev=aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd failed=kill_residue,relocated,classified
exit=1
```

  12547 untracked/ignored paths inside the repo it reads, left by a SIGKILL 3 s after the first write.
- `conform.py:70` at that tip put its selftest scratch under `<lane>/.ufo/waves/round-40/scratch`
  (`:746` — `tempfile.mkdtemp(prefix="mori-conform-selftest-", dir=SCRATCH_ROOT)`), the untracked debris
  round-49 M6 recorded.

Why no committed check sees this class: `.gitignore:5` is `.scratch/`; `tools/mori-unlanded-check.py:14` states
that `.scratch/` and ignored paths are outside its scope "on purpose"; QUALITY 80 (`corpus/QUALITY.md:368-372`)
reads `git status --porcelain --untracked-files=all -- .ufo/waves/round-<N>/` only. The residue lives for the
duration of a run and is removed by the run's own cleanup, so the only observer of it is a `--ignored` status taken
mid-run (what C1 arm A does).

## 4. The landed fix, as far as the mistake rows need it

`tools/mori-pin-check.py` v5 (`87e0c374`):

- `export_rev` (`:870-887`) clones `--shared --no-checkout` into `<dest>/tree` and checks the revision out detached
  (`:880-883`); the comment at `:871-873` states the reason (round-50 D-d residue and the enclosing-repo reach).
- `scratch_parent = os.path.abspath(args.scratch) if args.scratch else tempfile.gettempdir()` (`:912`); the
  comment at `:911` names round-50 D-d.
- The TMPDIR handed to every pin is created inside the measured tree (`:540-545`, `tmp_parent = os.path.join(root, ".scratch")`),
  whose comment names `mori-round19-regressions.py`'s refusal of a TMPDIR outside its own lane root
  (`tools/mori-round19-regressions.py:880-892`).

`.ufo/waves/round-40/conform.py` (`87e0c374`): `LANE` from `os.path.abspath(__file__)` (`:71-72`),
`SCRATCH_ROOT = tempfile.gettempdir()` (`:73`), used at `:746`.

The clone carries the source's own branch refs, which is what the `master` reader needs. Fixture (branch `master`,
then the same source with a detached HEAD; both exited 0):

```
$ git clone -q --shared --no-checkout "$D" "$D.t1" && git -C "$D.t1" rev-parse --verify master
764f35c69d269cc658cdaa78bff5fd3604fc4f85
$ git -C "$D" checkout -q --detach HEAD && git clone -q --shared --no-checkout "$D" "$D.t2" \
    && git -C "$D.t2" rev-parse --verify master && git -C "$D.t2" branch -a
764f35c69d269cc658cdaa78bff5fd3604fc4f85
* master
  remotes/origin/HEAD -> origin/master
  remotes/origin/master
```

The clone names the source's default branch (a first attempt whose fixture source defaulted to a branch that was
not `master` left `master` unresolvable — `fatal: ambiguous argument 'master'`), so the `master` read resolves
because the lane's branch is `master`, not because v5 forces a branch name.

## 5. Draft — insert as `## Mistakes` of `corpus/lessons/round-51.md`

```markdown
## Mistakes

| id | class | evidence | captured-by | fix | shown able to fail |
|---|---|---|---|---|---|
| M1 | hidden location dependence | `tools/mori-pin-check.py` at the entering tip `aa3af1ec` exported the measured tree with `git archive` to `<repo>/.scratch/pin-check-*/tree` (`:884` `scratch_parent = os.path.join(repo, ".scratch")`; export `:844-862`), so a pin that ran `git -C <tree> …` resolved against whichever repository enclosed the export. Three pins do that. `.ufo/waves/round-49/count-c1.py:52-53` sets `LANE` from `__file__` and `:353` runs `git -C LANE rev-parse --verify master^{commit}` (`--rev` defaults to `master`, `:313`), so inside the repo it read the lane tip and the arm passed for the wrong reason. `tools/mori-round19-regressions.py:844` takes `repo = resolved.parents[4]` and `:854` runs `git -C repo show ORACLE_REVISION:…`, which raises `pinned-oracle-unavailable` when that tree has no repository. `.ufo/waves/round-40/conform.py:69` at that tip hardcoded `LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"` (scratch under the lane at `:70`) and `:522` runs `git -C repo rev-parse HEAD` with `repo` defaulting to it, so it measured the host lane wherever it ran. Fixture: `git -C <D>/.scratch/exp/tree rev-parse --show-toplevel` printed `<D>` rc 0; the same tree with no enclosing repository printed `fatal: not a git repository` rc 128. Receipt `evidence/control-c1-scratch-only.txt`: `C1=unmet kill_residue=0 relocated=unmet reloc_mismatch=3 classified=bad selftest=pass=114,fail=0`, exit 1 — moving the export out alone turned three pins red. The receipt carries the count only (`count-c1.py:144` writes the per-pin lines to `<scratch>/relocated.out`, removed with the scratch), so "which three" rests on `contract.md` C1 and this code reading, not on a committed per-pin line. | none. Nearest is QUALITY 78 (`corpus/QUALITY.md:357-360`): it binds a counting command to committed bytes and forbids reading a list or fixture from the working directory, and names no check; it never constrains a pin instrument's repository discovery. QUALITY 127 (`corpus/QUALITY.md:1070-1077`) checks only that an instrument carries no absolute host path — its check greps the literal `/home/vgpnk` over `tools/` at a rev, so `.ufo/waves/round-49/count-c1.py` is outside its pathspec, and a file with no absolute path that reaches the lane through `git -C <tree>` is invisible to it. | C1's arms A and B in `tools/mori-pin-check.py` v5 (`87e0c374`). Arm B (relocated): `export_rev` (`:870-887`) measures a `git clone --shared --no-checkout` of the source repo checked out detached at R (`:880-883`) under `--scratch`/TMPDIR (`:912`), so `git -C <tree>` finds the clone's own repository and its `master` — the frozen counter's comment (`.ufo/waves/round-51/count-c1.py:77-78`) says those pins "read `master` from the repository they run in". Arm A (kill residue): the same move takes the export off the measured repo. The lane's `conform.py` now derives `LANE` from `os.path.abspath(__file__)` and puts `SCRATCH_ROOT` at `tempfile.gettempdir()` (`.ufo/waves/round-40/conform.py:71-73`). | Arm B: `evidence/control-c1-do-nothing.txt` (`relocated=unmet reloc_mismatch=1`) and `evidence/control-c1-scratch-only.txt` (`reloc_mismatch=3`) exit 1; `evidence/c1-at-data.txt` reads `relocated=met reloc_mismatch=0` exit 0. Arm A: `control-c1-do-nothing.txt` `kill_residue=12547` (first path `!! .scratch/pin-check-uphozg94/tree/.gitignore`) and `control-c1-conform-only.txt` `kill_residue=12478`; `c1-at-data.txt` `kill_residue=0`. Floor of arm A: `control-c1-class-only.txt` shows `kill_residue=1` is still unmet. |
| M2 | residue producer (round-50 D-d) | The round-50 spot-check named the two producers and routed them: D-d (`corpus/lessons/round-50-verifier-spotcheck.md:45-49`) and routed defect 1 (`:173-174`, `tools/mori-pin-check.py:884-887` and `.ufo/waves/round-40/conform.py:69`). At the entering tip the residue is measured: `evidence/control-c1-do-nothing.txt` carries `kill_residue_first: !! .scratch/pin-check-uphozg94/tree/.gitignore` and `C1=unmet kill_residue=12547 …`, exit 1 — a SIGKILLed `--rev` run left 12547 untracked/ignored paths in the repo it reads, because the export sat at `<repo>/.scratch` (`:884`). `conform.py:70` at that tip put its selftest scratch at `<lane>/.ufo/waves/round-40/scratch` (`:746`, `mkdtemp(prefix="mori-conform-selftest-", dir=SCRATCH_ROOT)`), the untracked debris round-49 M6 recorded; the same in-lane scratch is why a re-execution diverged before rerun (D-d: `conform.py` exited 2 under load). | none, and round 49's fix hid the class. `.gitignore:5` is `.scratch/`; `tools/mori-unlanded-check.py:14` says `.scratch/` and ignored paths are outside its scope "on purpose"; QUALITY 80 (`corpus/QUALITY.md:368-372`) reads `git status --porcelain --untracked-files=all -- .ufo/waves/round-<N>/` only. A transient full tree under `.scratch/` is invisible to every committed check while it exists and gone after the run's own cleanup, and the round-40 selftest scratch would reach QUALITY 80's pathspec only if it outlived the run. | Arms A and B of the frozen P-C1, not a new counter. Arm A (residue): v5's export and its temp dirs live in `--scratch`/TMPDIR (`tools/mori-pin-check.py:911-916`), so a SIGKILL leaves the measured clone's `git status --porcelain --ignored --untracked-files=all` empty. Arm B (relocation): `conform.py`'s `__file__`-derived `LANE` (`:71-72`) and `SCRATCH_ROOT = tempfile.gettempdir()` (`:73`, used at `:746`) move both its measurement and its selftest scratch off the lane. Both arms are frozen in `count-c1.py`'s docstring (`:7-11` arm A, `:12-15` arm B). | Arm A: `control-c1-do-nothing.txt` `kill_residue=12547` and `control-c1-conform-only.txt` `kill_residue=12478` exit 1, `c1-at-data.txt` `kill_residue=0` exit 0, `control-c1-class-only.txt` `kill_residue=1` (any nonzero is unmet, per the contract). Arm B: `control-c1-do-nothing.txt` `reloc_mismatch=1`, `control-c1-class-only.txt` `reloc_mismatch=2`, `control-c1-always-env.txt` `reloc_mismatch=1`, `control-c1-scratch-only.txt` `reloc_mismatch=3`, `c1-at-data.txt` `relocated=met reloc_mismatch=0`. |
```

Cell-length note for the L1: both rows are longer than the round-49/50 five-column rows because the sixth column
exists here. If the section must match the earlier five-column shape, dropping the last column loses the only place
that names which receipt makes each arm red; I would keep the six.

## 6. What I did not do

- Did not run `count-c1.py`, `count-c2.py`, `mori-pin-check.py`, `conform.py`, or any control: the receipts are
  frozen and my item is drafting from them. So the three pins behind `reloc_mismatch=3` are UNVERIFIED by me
  individually (the receipt has no per-pin line).
- Did not read or grep kernel log message text, touch a cgroup, sysctl, swap or watermark, or run
  systemctl/journalctl.
- Did not install or upgrade a tool; did not run pacman.
- Did not write outside my report file and my scratch; the scratch directory is removed.

## Findings

- MED — `.ufo/waves/round-51/evidence/control-c1-scratch-only.txt` records `reloc_mismatch=3` without naming the
  pins: `count-c1.py:144` writes the per-pin lines to `<scratch>/relocated.out`, which the run deletes with the
  scratch, so the three instruments the M1 row blames cannot be checked from committed bytes. Frozen counter —
  a named limit for the report, not a proposal to change it.
- MED — `corpus/lessons/round-50-verifier-spotcheck.md:173-174` (routed defect 1) and `contract.md` C1 group
  `conform.py` with the two instruments that read the enclosing repository, but at `aa3af1ec` `conform.py`'s
  dependence is the opposite kind: a hardcoded absolute lane path (`:69`) plus a lane-resident scratch (`:70`), so
  it measures the host lane even when a repository does enclose the export. The M1 row states the mechanism per
  instrument; if the lesson is meant to teach one class, the phrasing should not credit `conform.py` with
  repository discovery it does not do.
- LOW — `corpus/QUALITY.md:1073-1076` (criterion 127): the check's only signal is the literal string `/home/vgpnk`
  scoped to `tools/`, so a wave instrument that reaches the lane through `git -C <tree>` is outside it and a
  `tools/` file with no absolute path but repository-relative reads would pass.
- LOW — `.gitignore:5` (`.scratch/`) combined with `tools/mori-unlanded-check.py:14` and QUALITY 80's
  `.ufo/waves/round-<N>/` pathspec makes a mid-run residue tree unobservable to every committed check; C1 arm A's
  `--ignored` status is the only observer.
- LOW — `tools/mori-pin-check.py:880-883`: v5's `--shared` clone carries the source's own default branch name. My
  fixture resolved `master` for a source on `master` (attached and detached HEAD) and failed with `fatal: ambiguous
  argument 'master'` for a source defaulting to another branch. Inside the frozen counter this is harmless (its
  clones are made with `checkout -B master <rev>`, `count-c1.py:75-82`), but `--repo` pointed at a repository whose
  default branch is not `master` leaves that one pin's `master` read unresolvable.
- LOW — `evidence/control-c1-class-only.txt` shows arm A can read `kill_residue=1` for the same entering tool that
  reads 12547 in `control-c1-do-nothing.txt`; the contract already names the kill-moment limit and says any nonzero
  is unmet, and the observed floor of 1 confirms the arm does not need a large tree to stay red.
