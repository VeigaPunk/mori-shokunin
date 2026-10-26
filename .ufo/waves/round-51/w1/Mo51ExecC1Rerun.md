# Mo51ExecC1Rerun — independent C1 re-run and both separability directions (wave w1, round 51)

Seat: executor, leaf. Item: (1) re-run `count-c1.py` at the data revision with my own scratch; (2) re-run it at
the entering tip (expect unmet); (3) two separability fixtures in a `--no-local` clone — C2's data reverted and
scored with `count-c1.py`, C1's code reverted and scored with `count-c2.py`. No subagent was used (the one labrat
was not needed); no tool was installed or upgraded (nothing was needed). This report writes no vote line of any
kind: the counter's `entailed` / `overclaim` lines are excluded from this file by the wave rule, and no line here
begins with that reserved word.

Environment: MACHINE_ID host, Python 3.14.8, git 2.56.0, bubblewrap 0.13.1. Scratch root
`/fast/scratch/hyaku/mori-r51/Mo51ExecC1Rerun/` with `TMPDIR=/fast/scratch/hyaku/mori-r51/Mo51ExecC1Rerun/tmp`;
`/tmp` was used for nothing. Every command ran with an absolute path and with the scratch dir as cwd; every
fixture repo asserted `git -C <dir> rev-parse --show-toplevel` == `<dir>` before its first commit (printed below).
The scratch dir was removed at the end (`5.1G` → gone, `exists=no`).

Revisions: freeze `4677910eae6df3dabd38fe9a0daf1945146a1110`, data `87e0c374537557754bf71dd68036ded3ddc6699c`
(=`87e0c374…`), entering tip `aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd` (=`aa3af1ec…`), lane tip observed at the
start of the session `b504cb1701568a0038aab9d98ec13d28eff801da`.

Disk guard (`/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`, rc 0 both times):

```
before: root  use%  free            after: root  use%  free
        /tmp         3%  124.1G            /tmp         4%  123.9G
        /var/tmp    35%  584.9G            /var/tmp    35%  587.8G
        /fast/scratch/hyaku 25% 604.2G     /fast/scratch/hyaku 23% 620.8G
```

No ENOSPC at any point; the largest single artefact was one `--no-local` clone plus the counter's own scratch
(`du -sh` of the scratch tree before removal: 5.1G).

## 1. C1 at the data revision — reproduced on my own scratch

```
$ cd /fast/scratch/hyaku/mori-r51/Mo51ExecC1Rerun && export TMPDIR=$PWD/tmp
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-51/count-c1.py \
    87e0c374537557754bf71dd68036ded3ddc6699c --scratch /fast/scratch/hyaku/mori-r51/Mo51ExecC1Rerun/s1
classified: pin line=3 kind=tally prefix=ENVA_SELFTEST state=mismatch pinned='pass=3 fail=0' observed=None rc=2 cmd='python3 tools/enva.py --selftest' class=env
classified: pin line=4 kind=tally prefix=ENVB_SELFTEST state=mismatch pinned='pass=4 fail=0' observed=None rc=1 cmd='python3 tools/envb.py --selftest' class=env
classified: pin line=5 kind=tally prefix=STLA_SELFTEST state=mismatch pinned='pass=4 fail=0' observed='pass=5 fail=0' rc=0 cmd='python3 tools/stla.py --selftest' class=stale
classified: pin line=6 kind=tally prefix=STLB_SELFTEST state=mismatch pinned='pass=2 fail=0' observed='pass=2 fail=0' rc=1 cmd='python3 tools/stlb.py --selftest' class=stale
classified: pin line=7 kind=tally prefix=OKAY_SELFTEST state=match pinned='pass=1 fail=0' observed='pass=1 fail=0' rc=0 cmd='python3 tools/okay.py --selftest'
classified: PIN_CHECK=unmet tally_pins=5 digest_pins=0 mismatches=4 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=- baseline=no env=2 stale=2
kill_residue_first: -
C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=119,fail=0 rev=87e0c374537557754bf71dd68036ded3ddc6699c failed=-
exit=0
WALL=98.8 s
```

Line-for-line the same as `evidence/c1-at-data.txt` (same five `classified:` lines, same `kill_residue_first: -`,
same `C1=met … selftest=pass=119,fail=0 … failed=-`, exit 0), produced from a different scratch dir, a different
TMPDIR and therefore different clones and a different bubblewrap mount namespace. The `kv` values are in the same
order and identical: `kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=119,fail=0`.

Arm A is non-vacuous at this revision: `kill_residue=0` (not `none`), so the counter's `started` detection fired
(a new path appeared in C0 or `tmpA` reached 100 entries) and the run was killed mid-flight; the reading is a real
zero, not a "no_progress" bail-out.

## 2. C1 at the entering tip — the do-nothing control reproduces

```
$ python3 …/count-c1.py aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd --scratch /fast/scratch/hyaku/mori-r51/Mo51ExecC1Rerun/s2
classified: pin line=3 kind=tally prefix=ENVA_SELFTEST state=mismatch pinned='pass=3 fail=0' observed=None rc=2 cmd='python3 tools/enva.py --selftest'
classified: pin line=4 kind=tally prefix=ENVB_SELFTEST state=mismatch pinned='pass=4 fail=0' observed=None rc=1 cmd='python3 tools/envb.py --selftest'
classified: pin line=5 kind=tally prefix=STLA_SELFTEST state=mismatch pinned='pass=4 fail=0' observed='pass=5 fail=0' rc=0 cmd='python3 tools/stla.py --selftest'
classified: pin line=6 kind=tally prefix=STLB_SELFTEST state=mismatch pinned='pass=2 fail=0' observed='pass=2 fail=0' rc=1 cmd='python3 tools/stlb.py --selftest'
classified: pin line=7 kind=tally prefix=OKAY_SELFTEST state=match pinned='pass=1 fail=0' observed='pass=1 fail=0' rc=0 cmd='python3 tools/okay.py --selftest'
classified: PIN_CHECK=unmet tally_pins=5 digest_pins=0 mismatches=4 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=- baseline=no
kill_residue_first: !! .scratch/pin-check-btbgglve/tree/.gitignore
C1=unmet kill_residue=12474 relocated=unmet reloc_mismatch=1 classified=bad selftest=pass=114,fail=0 rev=aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd failed=kill_residue,relocated,classified
exit=1
WALL=39.2 s
```

Same failed-arm set as `evidence/control-c1-do-nothing.txt` (`kill_residue,relocated,classified`), same
`reloc_mismatch=1`, same `selftest=pass=114,fail=0`, and mismatch lines with no `class=` suffix. The residue count
is 12474 here against 12547 in the receipt and 12475 as the low end of the range the contract names — the count is
a timing artefact of the same kill moment, as the contract says; the verdict (nonzero ⇒ unmet) does not depend on
it.

## 3. Separability A — C2's data reverted, C1's counter at the fixture commit

Fixture built in a `--no-local` clone of the lane under scratch, on top of the data commit; C2's files restored to
the entering tip (`corpus/SOURCES.md` back to `aa3af1ec…`, entry and `corpus/evidence/sources-r51/` removed).

```
$ git clone -q --no-local /home/vgpnk/Projects/shokunin/mori-shokunin $S/clone
clone toplevel=/fast/scratch/hyaku/mori-r51/Mo51ExecC1Rerun/clone
$ git -C $CL checkout -q -B f1-revert-c2 87e0c374… && git -C $CL checkout aa3af1ec… -- corpus/SOURCES.md
$ git -C $CL rm -q -r --ignore-unmatch corpus/knowledge/memavailable-estimate-r51.md corpus/evidence/sources-r51
$ git -C $CL commit -q -m "fixture F1: revert C2 data paths to aa3af1ec"
F1=84a517bf0dcc755b3f33c21b4334d2b0d302152a
```

The fixture is exactly a corpus reversion: `git diff --name-status aa3af1ec… 84a517bf…` lists **no** `corpus/`
path (only the round-51 wave files, `SHONEN.md`, `SKILL.md`, `tools/mori-pin-check.py`,
`.ufo/waves/round-40/conform.py`), `git ls-tree -r 84a517bf… -- corpus/knowledge/memavailable-estimate-r51.md
corpus/evidence/sources-r51/` is empty, and `git show 84a517bf…:corpus/SOURCES.md | grep -c '^| S49[2-6] '` prints
`0`.

```
$ python3 …/count-c1.py 84a517bf0dcc755b3f33c21b4334d2b0d302152a \
    --repo /fast/scratch/hyaku/mori-r51/Mo51ExecC1Rerun/clone --scratch …/s3
classified: pin line=3 … class=env
classified: pin line=4 … class=env
classified: pin line=5 … class=stale
classified: pin line=6 … class=stale
classified: pin line=7 … class=match (OKAY_SELFTEST)
classified: PIN_CHECK=unmet tally_pins=5 … env=2 stale=2
kill_residue_first: -
C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=119,fail=0 rev=84a517bf0dcc755b3f33c21b4334d2b0d302152a failed=-
exit=0
WALL=96.5 s
```

C1 reads `met` at a commit that contains none of C2's data: the C1 counter does not read the corpus entry, the
SOURCES rows or the source copies. (This run also exercised the `--repo` path with `--hide` left at its default,
the lane: the `relocated` arm hid the real lane working tree while scoring the fixture clone, and still read
`reloc_mismatch=0`.)

## 4. Separability B — C1's code reverted, C2's counter at the fixture commit

Second fixture commit on the same clone: `tools/mori-pin-check.py`, `.ufo/waves/round-40/conform.py`, `SKILL.md`
and `SHONEN.md` restored to the entering tip.

```
$ git -C $CL checkout -q -B f2-revert-c1 87e0c374… && git -C $CL checkout aa3af1ec… -- \
    tools/mori-pin-check.py .ufo/waves/round-40/conform.py SKILL.md SHONEN.md
$ git -C $CL commit -q -m "fixture F2: revert C1 code paths to aa3af1ec"
F2=bef6e439ecce7bc2e191be680f42e07dc95640c6

$ python3 …/count-c2.py bef6e439ecce7bc2e191be680f42e07dc95640c6 --repo …/clone
C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=bef6e439ecce7bc2e191be680f42e07dc95640c6 failed=entailment
exit=1
WALL=0.0 s
```

Same counter and same clone at the data tip, for comparison:

```
$ python3 …/count-c2.py 87e0c374537557754bf71dd68036ded3ddc6699c --repo …/clone
C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=87e0c374537557754bf71dd68036ded3ddc6699c failed=entailment
```

The two lines differ in `rev` only. Every arm C2 owns — the 21 rows, the located quotes, the five sources, the
five copy pins, the provenance check — reads the same when the pin-check v5 code, `conform.py`, `SKILL.md` and
`SHONEN.md` are reverted to the entering tip. The only failing arm is the vote arm, which fails at both revisions
because no vote line exists in the tree yet (the counter reads `.ufo/waves/round-51/w1/` from git objects; see §6).
That is the wave's current state, not an effect of the C1 code.

`git diff --name-status aa3af1ec… bef6e439…` contains no path under `tools/`, `.ufo/waves/round-40/`, `SKILL.md`
or `SHONEN.md`: the C1 surfaces are exactly those of the entering tip in this fixture.

## 5. Where a full `--rev` run writes — the arm-A zero, measured across the whole run

Arm A kills at one moment, so its `kill_residue=0` only describes that moment. I sampled the measured tree at 2 s
resolution for a complete run at both revisions in fresh `--no-local` clones, and read
`git -C <clone> status --porcelain --ignored --untracked-files=all | wc -l` at every sample:

```
[data]  rc=0 samples=120 max=0     first_nonzero=-          final=120 0
[data]  last: PIN_CHECK=met tally_pins=35 digest_pins=8 mismatches=0 … env=0 stale=0
[enter] rc=0 samples=120 max=12502 first_nonzero=1/max=1    final=120 0
[enter] last: PIN_CHECK=met tally_pins=35 digest_pins=8 mismatches=0 … env=0 stale=0
```

At the data revision the measured tree never showed a single residue line across the whole run (and the sampler's
`max=0` includes the samples taken after the tool had exited, when the loop was still counting a zombie to its
120-sample cap — no drift in those either). At the
entering tip the same sampler peaked at 12502 lines and its first sample was already nonzero: the old export wrote
into `<repo>/.scratch` from the first two seconds. At both revisions the tool cleans up on normal exit, so the
final sample is 0 (`final=120 0`) and the entering peak is the in-flight export, not a post-run residue; only a
kill leaves it behind. The sampler therefore detects this class of write, and the data
tip's zero is not a measurement that cannot see residue.

Phase timing of one complete data-tip run (1 s sampling of the export's TMPDIR and of `<clone>/.scratch`):

```
exit=0 WALL=78s   PIN_CHECK=met tally_pins=35 digest_pins=8 mismatches=0 … env=0 stale=0
tmpA first entry at 2 s, ~14192 entries by 2 s, stable ~14207 through 60 s, churn 14202→14354 at 70-76 s,
tmpA back to 0 at 79 s (the export tree is removed in the tool's `finally`)
max pin-tmp-* dirs seen under <clone>/.scratch during the run: 0
```

The churn in the last ~18 s is the pin phase: `run_cmd` (`tools/mori-pin-check.py:539-556`) creates
`TMPDIR=<root>/.scratch/pin-tmp-*` for every pinned command and removes it in a `finally`, and in `--rev` mode
`root` is the exported tree (`main` at `tools/mori-pin-check.py:960-967`, `rev, root = got` from `export_rev`),
which lives under `--scratch`, not under the measured repo. So the 35 tally pins and 8 digest pins write inside
the export tree in scratch; the measured repo is not written in that phase either. The only git work on the
measured repo is the read `git clone --shared` does on its object store; no worktree write happens at any point
of the run.

Timed kills, for completeness (fresh clone, `setsid` process group, `SIGKILL`, then the same status count):

```
kill_after=25s post_residue=0 pin_tmp_dirs=0 tmpA_entries=14197
kill_after=45s post_residue=0 pin_tmp_dirs=0 tmpA_entries=14202
kill_after=60s post_residue=0 pin_tmp_dirs=0 tmpA_entries=14202
kill_after=72s post_residue=0 pin_tmp_dirs=0 tmpA_entries=14248
```

Four kill moments between the export's completion and the start of the pin phase, all zero: the arm's zero holds
outside the single moment it samples, for the moments I tested. What a kill leaves behind in these runs is the
export tree inside `--scratch` (14197-14248 entries in the TMPDIR), which the counter deletes with its own scratch
directory and which is therefore never counted as residue against the repo.

## 6. Frozen bytes, frozen-path drift, and what I did not touch

```
$ sha256sum .ufo/waves/round-51/count-c1.py .ufo/waves/round-51/count-c2.py
622f650c1ade984d8c9abed20e7a7fd08930861a698398f36d4c3a770aff355c  .ufo/waves/round-51/count-c1.py
19553792d74d8f3ca9c09e6a018b9c66f61a58e8ad78e72b524a69ec892cfb26  .ufo/waves/round-51/count-c2.py
```

Both match their `evidence/freeze-sha256.txt` entries, and

```
$ git -C …/mori-shokunin diff --name-status 4677910eae6df3dabd38fe9a0daf1945146a1110 87e0c374… -- \
    .ufo/waves/round-51/count-c1.py .ufo/waves/round-51/count-c2.py .ufo/waves/round-51/contract.md \
    .ufo/waves/round-51/controls | wc -l
0
```

so the counts above were produced by the frozen counters under the frozen contract.

The counters read votes from the git tree only (`count-c2.py` `git_lister` → `git ls-tree --name-only <rev>
.ufo/waves/round-51/w1/`). At both revisions I scored, that directory does not exist in the tree, which is why
`entailed=0 dissent=0` is a true reading of an empty vote set in §4 and not a counter failure; the final C2
reading must be taken at a successor commit that contains the seat reports.

Nothing in `/home/vgpnk/Projects/shokunin/mori-shokunin`, `/home/vgpnk/Projects/shokunin` or `~/.local/bin` was
written by this seat. The lane's working tree at the end of my session carries other seats' changes (`LOG.md`,
`SCORECARD.md`, `SHONEN.md`, `corpus/lessons/round-51.md` modified; new files under
`.ufo/waves/round-51/w1/`), none of them mine; every read above used committed revisions or the untracked report
directory. No jj or git mutating command was run in the lane or the fleet root; the only writes outside scratch
are this report file. Kernel log message text was not read; no OOM, cgroup, sysctl, swap or watermark was touched.

## Findings

No defect in the C1 claim was found: at `87e0c374…` the frozen counter reports `C1=met` on my own scratch with all
four arms green, the same reading reproduces at the entering tip as `C1=unmet` with the documented failing set,
and either claim scores unchanged when the other claim's data (both directions) is reverted. The findings below
are limits and hygiene items, not reasons to re-open either claim.

- **LOW — the contract's parenthetical range for the do-nothing residue is one too high at the low end**
  (`contract.md`, §C1 "Before (entering `aa3af1ec`)" prose after the control table, and
  `evidence/control-c1-do-nothing.txt`): the contract says the residue "varies between runs (12475–12547
  observed)"; my independent run at `aa3af1ec…` measured `kill_residue=12474`. The verdict rule ("Any nonzero
  value is unmet") is unaffected and the residue is a timing artefact of where the kill lands, but the stated
  lower bound is contradicted by an observed run.
- **LOW — `.scratch/` is tracked in the repo while `.gitignore:5` lists `.scratch/`** (`git ls-tree -r --name-only
  87e0c374… -- .scratch | wc -l` → 225 tracked files, e.g. `.scratch/CritConjunctSemantics/…`,
  `.scratch/round22/…`). Consequence for arm A of P-C1: none at this revision — with `--ignored` the status
  metric still lists new untracked paths there (that is how `kill_residue_first:
  !! .scratch/pin-check-btbgglve/tree/.gitignore` appears at the entering tip), and my sampler read 0 across a
  full data-tip run. The cost is weight: every fresh clone in the counter carries the 225-file scratch tree (two
  clones per `count-c1.py` run — one in arm A, one in arm B). A hygiene item for the lane, not this round's
  data.
- **LOW — arm A's metric cannot see an empty directory** (`count-c1.py` `status_lines`, contract §C1 arm A): the
  measured quantity is `git status --porcelain --ignored --untracked-files=all` lines, and git reports no line for
  a directory that contains nothing. [INFERENCE] A future instrument that did `mkdir <repo>/.scratch/x` and died
  before writing a file would leave a real directory in the repo it reads while the arm still read 0. This is a
  property of the frozen metric, named as a limit; it does not affect the data tip, where my full-run sampler saw
  the measured tree unchanged.
- **LOW — the landed C1 bytes are the witness bytes** (`evidence/freeze-sha256.txt` together with
  `tools/mori-pin-check.py`, `.ufo/waves/round-40/conform.py`): the freeze lists
  `.ufo/waves/round-51/controls/witness/mori-pin-check.py` as
  `35c69d9115b5e45f91a4b0311ce95c03b3b2b929250e2afb31b571a49687b3bf` and
  `.ufo/waves/round-51/controls/witness/conform.py` as
  `7f5174d542bd983552670b06f6cc424b10e53c81e55ecabcdd919f4043bdfa23`,
  and those are the sha256 of the landed `tools/mori-pin-check.py` and `.ufo/waves/round-40/conform.py`. The
  contract describes the witness as "feasibility only; built by the L1 — disclosed, not the claim's landing"; the
  bytes say the landing is byte-identical to the witness. The claim still holds on my independent re-run, but the
  contract sentence overstates the separation between the witness and the data and should read "the landing is
  the witness bytes" (a wording/provenance item for the L1 and the lesson, not a counter issue).
- UNVERIFIED: portability of the relocated arm to another host, user or kernel (arm B hides one path inside
  bubblewrap 0.13.1 on this host only); whether a kill during the first ~2 s of the export, before any write,
  behaves like a no-op (my first sample at 2 s already showed the export populated).
