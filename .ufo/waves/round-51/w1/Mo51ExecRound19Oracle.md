# Mo51ExecRound19Oracle — why `pinned-oracle-validates` fails from a `git archive` tree

Seat: executor (leaf). Lane: `mori-shokunin`. Machine: MACHINE_ID. Date: 2026-10-26.
Lane working tree read at `b504cb17`; the data commit under test is
`87e0c374537557754bf71dd68036ded3ddc6699c` (entering tip `aa3af1ec…`). No lane file was
written except this report; nothing was added to git or jj; no tool was installed or
upgraded; no subagent and no labrat was used (the answer was reachable with plain reads and
a scratch reproduction).

Report: .ufo/waves/round-51/w1/Mo51ExecRound19Oracle.md

Scratch used: `/fast/scratch/hyaku/mori-r51/Mo51ExecRound19Oracle/` (`TMPDIR` inside it),
removed before this report was written; every command and output cited below is copied
inline, so no scratch path is evidence. Disk guard read before the run:
`/fast/scratch/hyaku 25% … 606.1G` free.

## 1. Answer in one paragraph

The failing arm is a **repository** check, not a bytes check. `run_selftest` builds the
oracle path from its own location (`tools/mori-round19-regressions.py:1386`), then
`expected_from_pinned_commit` runs

```
git --no-optional-locks -c core.fsmonitor=false -C <tree-root> show 5e393d20daa628a0b4ca9aa6a1626aa54285b3f0:.ufo/waves/round-19/frozen/expected.json
```

(`tools/mori-round19-regressions.py:852-855`, `<tree-root> = resolved.parents[4]` computed at
line 844). A plain `git archive` extraction outside any repository has no object database
above it, so git exits 128 and the arm's `except HarnessError` (line 1391-1392) turns that
into `oracle_ok = False`: `R19_SELFTEST pass=25 fail=1`, rc 1. A `--no-local` clone at the
same commit is itself a repository whose object database contains `5e393d2`, so the same
bytes pass (`pass=26 fail=0`). The arm therefore depends on more than committed bytes: a
reachable object DB that resolves `ORACLE_REVISION`, a working-tree copy byte-equal to that
blob, and — under pin-check v5's `--shared` transport — the origin object store surviving at
the absolute alternates path.

## 2. The arm, line by line (read at the data commit; blob `6abd2297…`)

`tools/mori-round19-regressions.py`:

| line | code | effect |
|---|---|---|
| 1386 | `oracle = script_path.parents[1] / ORACLE_RELATIVE_PATH` | oracle = `<tree-root>/.ufo/waves/round-19/frozen/expected.json`; the "lane root" is the directory two levels above the running script, i.e. the **extraction root**, not the lane |
| 1388 | `expected_from_pinned_commit(oracle)` | the only call in the arm |
| 1389-1390 | `sha256_bytes(oracle_bytes) == sha256_file(oracle) and expected["schema"] == EXPECTED_SCHEMA` | second condition: working-tree bytes must equal the bytes git returned |
| 1391-1392 | `except HarnessError: oracle_ok = False` | every failure reason is discarded; the tally prints only the predicate name |
| 1393 | `tally.check("pinned-oracle-validates", oracle_ok)` | adds 1 to `fail` |

`expected_from_pinned_commit` (`836-877`): path-shape checks (`837-850`), then

```
844  repo = resolved.parents[4]
851  env = clean_env(repo, repo)
852  argv = ["git", "--no-optional-locks", "-c", "core.fsmonitor=false",
854          "-C", str(repo), "show", ORACLE_REVISION + ":" + ORACLE_RELATIVE_PATH]
858  proc = subprocess.run(argv, …, env=env, timeout=GIT_TIMEOUT, check=False)
865  if proc.returncode != 0: raise HarnessError("pinned-oracle-unavailable")
869  supplied = resolved.read_bytes()
871  if supplied != proc.stdout: raise HarnessError("expected-oracle-mismatch")
```

`ORACLE_REVISION = "5e393d20daa628a0b4ca9aa6a1626aa54285b3f0"` (line 26);
`ORACLE_RELATIVE_PATH = ".ufo/waves/round-19/frozen/expected.json"` (line 27).
`clean_env(repo, repo)` (lines 104-119) passes `HOME=<tree-root>`, `TMPDIR=<tree-root>`,
`GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`, `GIT_CONFIG_NOSYSTEM=1` and the
inherited `PATH`; no user or system git config can rescue or break the call, and
`safe.directory` from such config is unavailable (see §6, UNVERIFIED).

Facts that make the reproduction representative: the tool blob and the oracle blob are
**identical at the entering tip and at the data commit** — tool
`6abd22971d32e9f316eb4cb1896d5ccd48b38ac3` (worktree sha256
`3c2c77d4d400412c1b9b3be67e20840ed7af5bda90df168b5e47a98007b7781b`), oracle
`8bde07719e4127d148ac552fc86a25a63ce80243` (sha256
`c5c6c67f104ed1baa57a56bfb22728a2e871ca174a4915ff4005eb3485abe22a`). `git merge-base
--is-ancestor 5e393d2 87e0c37` → rc 0, so the clone can resolve the oracle revision.

## 3. Reproduction (scratch, one archive + one clone)

Setup, both from the lane without mutating it:

```
$ git -C <lane> archive --format=tar 87e0c374537557754bf71dd68036ded3ddc6699c | tar -x -C $S/archive-tree
extract_rc=0            # full tree, 12,498 blobs / 319,680,383 bytes, 1.3 s
$ git -C $S/archive-tree rev-parse --show-toplevel
fatal: not a git repository (or any parent up to mount point /)
Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set).
revparse_rc=128
$ git clone -q --no-local <lane> $S/clone-parent/clone && git -C $S/clone-parent/clone checkout -q 87e0c37…
checkout_rc=0; HEAD=87e0c374537557754bf71dd68036ded3ddc6699c; status --porcelain = 0 lines
```

### A — archive tree outside any repository (the reported case)

```
$ cd $S/archive-tree && TMPDIR=$S/archive-tree/tmp python3 tools/mori-round19-regressions.py --selftest
FAIL pinned-oracle-validates
R19_SELFTEST pass=25 fail=1
selftest_rc=1
```

`pass=25 fail=1` matches the observed reading; `pinned-oracle-validates` is the only failing
predicate. Note the TMPDIR: it has to be *inside* the extracted tree, because the whole
selftest refuses any other value (see §5, dependency d).

### A′ — same tree, caller's TMPDIR (outside the tree)

```
$ cd $S/archive-tree && TMPDIR=$S/tmp python3 tools/mori-round19-regressions.py --selftest
R19_SELFTEST setup=explicit-lane-tmpdir-invalid
selftest_rc=2
```

### B — `--no-local` clone at the same commit

```
$ cd $S/clone-parent/clone && TMPDIR=$S/clone-parent/clone/tmp python3 tools/mori-round19-regressions.py --selftest
R19_SELFTEST pass=26 fail=0
selftest_rc=0
$ git -C $S/clone-parent/clone show 5e393d2:.ufo/waves/round-19/frozen/expected.json | sha256sum
c5c6c67f104ed1baa57a56bfb22728a2e871ca174a4915ff4005eb3485abe22a  -    # show_rc=0
```

Arm probe on the clone (module imported from the clone, calling the real function):

```
OK repo=/fast/scratch/…/clone-parent/clone sha256=c5c6c67f… schema=mori-r19-expected-v1
```

### C — the same archive extracted **inside** the clone (tree has no `.git` of its own)

```
$ mkdir $C/embed && git -C <lane> archive --format=tar 87e0c37… | tar -x -C $C/embed
$ cd $C/embed && TMPDIR=$C/embed/tmp python3 tools/mori-round19-regressions.py --selftest
R19_SELFTEST pass=26 fail=0      selftest_rc=0
$ test -e $C/embed/.git; echo $?   → 1
```

This is the v4 arrangement in miniature (see §4) and shows the requirement is *an enclosing
repository*, not a `.git` inside the tree.

### D — archive tree inside a fresh repo that does not have the objects

```
$ git -C $D init -q; git -C $D rev-parse --show-toplevel → $D
$ git -C $D -c user.name=… -c user.email=… commit -q --allow-empty -m "fixture: one commit, no oracle objects"
$ cd $D/tree && TMPDIR=$D/tree/tmp python3 tools/mori-round19-regressions.py --selftest
FAIL pinned-oracle-validates
R19_SELFTEST pass=25 fail=1      selftest_rc=1
$ git --no-optional-locks -c core.fsmonitor=false -C $D/tree show 5e393d2:.ufo/waves/round-19/frozen/expected.json
fatal: path '.ufo/waves/round-19/frozen/expected.json' does not exist in '5e393d20daa628a0b4ca9aa6a1626aa54285b3f0'
show_rc=128
```

### E — objects present, working-tree oracle bytes altered (one word, schema `v1`→`v2`)

```
$ git -C $T show 5e393d2:.ufo/waves/round-19/frozen/expected.json | sha256sum
c5c6c67f…  -                          # the object is still there, show_rc=0
$ sha256sum $T/.ufo/waves/round-19/frozen/expected.json
b10128d56f839f25d0191874a227e632514a84897595ff803e3fbdae668a1e46   # worktree, edited
$ git -C $T status --porcelain
 M .ufo/waves/round-19/frozen/expected.json
probe → HarnessError: expected-oracle-mismatch
$ cd $T && TMPDIR=$T/tmp python3 tools/mori-round19-regressions.py --selftest
FAIL pinned-oracle-validates
R19_SELFTEST pass=25 fail=1      selftest_rc=1
```

### F — `--shared` transport (what pin-check v5 uses): origin object store moved away

Clone made with the v5 shape from a hardlink copy of the same tree, then the origin moved
aside; clone bytes unchanged throughout:

```
alternates: …/origin-shared/.git/objects
F1 origin present   → R19_SELFTEST pass=26 fail=0  rc=0
F2 origin moved     → error: unable to normalize alternate object path: …/origin-shared/.git/objects
                      FAIL pinned-oracle-validates
                      R19_SELFTEST pass=25 fail=1  rc=1
F3 origin restored  → R19_SELFTEST pass=26 fail=0  rc=0
```

### G — the landed v5 transport end to end

```
$ TMPDIR=$S/tmp python3 <clone>/tools/mori-pin-check.py --rev 87e0c37… --repo <lane> --scratch $S/pc-scratch
pin line=182 kind=tally prefix=R19_SELFTEST state=match pinned='pass=26 fail=0' observed='pass=26 fail=0' rc=0 cmd='python3 tools/mori-round19-regressions.py --selftest'
pin line=911 kind=tally prefix=CONFORM_SELFTEST state=match pinned='pass=11 fail=0' observed='pass=11 fail=0' rc=0 cmd='.ufo/waves/round-40/conform.py 87e0c37… --selftest'
PIN_CHECK=met tally_pins=35 digest_pins=8 mismatches=0 … env=0 stale=0
pipeline_rc=0    # 83 s
```

## 4. Why the observation appears only *outside* the lane (lesson M1)

In the pre-v5 arrangement the `--rev` tree was a `git archive` extracted **under
`<repo>/.scratch`** (`tools/mori-pin-check.py`, v5 comment at 871-875 and the v5 diff). The
extracted tree had no objects, but `git -C <tree> show …` walked up from
`<repo>/.scratch/tree` into the lane repository, which does hold `5e393d2`. The arm passed
*against the lane's object database*, so the non-hermetic export looked green while proving
nothing about the exported bytes. Move the same archive outside the repo (the relocation
witness, and this reproduction) and the single call has nothing to resolve against: one
predicate fails. v5 replaced the archive with `git clone --shared` (pin-check
`export_rev`, 870-885), which is a repository for a legitimate reason, so the pin goes back
to `state=match` (test G) — but that transport introduces its own live dependency on the
origin object store (test F).

So: `R19_SELFTEST pass=26` is a statement about "these bytes inside a repository that can
resolve `5e393d2`", not about the committed bytes. The old green was accidental.

## 5. What the arm depends on besides committed bytes

| # | dependency | evidence | verdict |
|---|---|---|---|
| a | a repository at or above the tree root whose object DB resolves `5e393d20…` at `.ufo/waves/round-19/frozen/expected.json` | A fails, C and B pass, D fails with rc 128 | **verified** |
| b | the working-tree oracle byte-equal to that blob (`sha256_file` vs `git show`) | E: `expected-oracle-mismatch` with the object intact | **verified** |
| c | under v5's `--shared` clone, the origin object store must still exist at the absolute path in `.git/objects/info/alternates` | F2 fails with clone bytes unchanged, F3 passes | **verified** |
| d | `TMPDIR` must be strictly inside the tree root for the whole selftest (`require_tmpdir`, 878-891: `lane_root = Path(__file__).resolve().parents[1]`) | A′ → `setup=explicit-lane-tmpdir-invalid`, rc 2 | **verified** |
| e | layout: the oracle must sit at exactly `<root>/.ufo/waves/round-19/frozen/expected.json` (path-shape check 840-850); depth does not matter because `parents[4]` is always the tree root | code read | code-read |
| f | a working `git` on the inherited `PATH`; a repo that git refuses (e.g. dubious ownership, since `safe.directory` is disabled by `GIT_CONFIG_GLOBAL/SYSTEM=/dev/null`) also yields rc≠0 → same FAIL | code read; no ownership change was made | UNVERIFIED |
| g | with `--no-local`, `ORACLE_REVISION` must be reachable from cloned refs (it is: ancestor of `87e0c37`) | merge-base rc 0, B passes | verified for this rev |

## 6. Limits of this probe

- One revision (`87e0c374…`) and one tool/oracle blob pair; the blobs are identical at the
  entering tip, so the result transfers by blob identity, not by a run at `aa3af1ec`.
- Two transports measured: `git archive` extraction and `git clone` (`--no-local`,
  `--shared`). A `git worktree`, a bare-repo export and a repository owned by another uid
  were not measured; the `safe.directory` row (f) is code-read only.
- The arm's `FAIL` line is the only diagnostic: the reason string
  (`pinned-oracle-unavailable` vs `expected-oracle-mismatch`) is discarded at 1391-1392, so a
  relocated run cannot tell "no repository" from "different bytes" from the tally.
- The lane's own selftest was not run (it would need a `TMPDIR` inside the lane, which this
  seat may not create); the clone at the same commit stands in for it.
- No counter, predicate, control or kill rule is questioned here; this is diagnosis only.

## 7. Findings

| severity | finding | file:line |
|---|---|---|
| MED | `pinned-oracle-validates` is not a function of committed bytes: it needs a repository at/above the extraction root that can resolve `ORACLE_REVISION`, so a `git archive` tree outside a repo fails one predicate (`pass=25 fail=1`) while the same bytes in a clone pass (`pass=26 fail=0`). The old green inside `<repo>/.scratch` came from the enclosing lane repo, not from the export. | `tools/mori-round19-regressions.py:844-866`, `:1386-1393` |
| MED | With the v5 transport the pin also depends on the origin object store surviving at the absolute alternates path: moving the source tree of a `--shared` clone flips the pin (`pass=26` → `pass=25`) with identical clone bytes, and back when restored. | `tools/mori-pin-check.py:870-885` (clone at 880) |
| LOW | The arm collapses every failure reason into `oracle_ok = False`; the tally shows only `FAIL pinned-oracle-validates`, so the env/stale distinction C1 lands for pin-check does not reach inside a pinned selftest. | `tools/mori-round19-regressions.py:1391-1392` |
| LOW | The whole selftest refuses a `TMPDIR` outside the *script's own* tree root, so a plain archive tree outside the lane cannot be measured with the caller's scratch TMPDIR at all (`setup=explicit-lane-tmpdir-invalid`, rc 2) — a relocation sweep that keeps TMPDIR in its own scratch gets a setup error, not a verdict. | `tools/mori-round19-regressions.py:878-891` |
| LOW | Recorded documentation under-describes the dependency: the SKILL cell pins `R19_SELFTEST pass=26 fail=0` and the round-45 risk note names only "the committed expected.json and the ORACLE_REVISION being present"; neither says a repository must enclose the tree. The pin itself remains valid inside a clone (test G), so this is a wording gap for the L1, not a broken pin. | `SKILL.md:182`; `.ufo/waves/round-45/w1/ExecSelftestModes.md:217-219`; earlier general record: `.ufo/waves/round-48/w2/R48SentTools.md:180-193` |
