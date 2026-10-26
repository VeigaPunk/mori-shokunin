# Mo51ExecC1Controls — C1 controls re-run (mori round 51, wave w1)

Seat: `Mo51ExecC1Controls` (executor, leaf). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Item as assigned: copy `.ufo/waves/round-51/controls` and `.ufo/waves/round-51/count-c1.py` into scratch preserving
the relative layout, run `python3 <copy>/controls/c1-controls.py aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd
<scratch>/k <scratch>/receipts`, check its write paths, and diff each new receipt's `C1=` line with the committed
`evidence/control-c1-*.txt` (ignoring `rev` and a `kill_residue` count when both are nonzero).
This is a re-execution of the frozen control builder; no counter, predicate, control or kill rule was changed, and no
data was touched. I am a dispatched seat, not an independent judge.

Environment: `Linux 7.2.11-arch1-1`, `Python 3.14.8`, `git 2.56.0`, `bubblewrap 0.13.1`, 32 CPUs, run at
2026-10-26 22:46–22:48 UTC. Scratch root `/fast/scratch/hyaku/mori-r51/Mo51ExecC1Controls` (431 MB peak),
`TMPDIR` inside it, removed at the end. Disk guard before the run: `scripts/hyaku/disk-guard.sh status` rc=0,
/fast 603 G free. No tool was installed or upgraded.

## 1. Copies and path audit before running

```
$ cd /fast/scratch/hyaku/mori-r51/Mo51ExecC1Controls/copy && sha256sum count-c1.py controls/c1-controls.py controls/witness/*
622f650c1ade984d8c9abed20e7a7fd08930861a698398f36d4c3a770aff355c  count-c1.py
8351ba6d4008037ef3f2694b73f9e2e9cad41bb5cb77ea21dc7511556266887a  controls/c1-controls.py
7f5174d542bd983552670b06f6cc424b10e53c81e55ecabcdd919f4043bdfa23  controls/witness/conform.py
35c69d9115b5e45f91a4b0311ce95c03b3b2b929250e2afb31b571a49687b3bf  controls/witness/mori-pin-check.py
```

All four hashes equal the frozen values in `evidence/freeze-sha256.txt` (byte-identical frozen inputs; the copy adds
no edits at this stage).

Write-path audit of the two scripts (`grep -n 'open(.*"w"\|makedirs\|mkdtemp\|clone\|archive\|rmtree'`):
`controls/c1-controls.py:69` writes inside `K`, `:76`/`:81` write `OUT_DIR/control-c1-<name>.txt`, `:80` creates
`SCRATCH/s-<name>`; `count-c1.py:144,165,171,104,135,155,163,189,196,230` write only under its `--scratch` base,
and `:190` runs `git archive` (stdout to a pipe, extracted into scratch). No path in either script names
`.ufo/waves/round-51`, so with `OUT_DIR` and the counter scratch outside the lane the run cannot write there.
Verified after the run (§5).

## 2. The literal copy cannot be run as specified — `C1_SETUP` before any measurement

The builder derives the source repo from its own location: `controls/c1-controls.py:23`
`LANE = os.path.dirname(...4 levels up from HERE...)` and `count-c1.py:38` `DEFAULT_REPO = os.path.dirname(...3 levels
up from HERE...)`. In the lane those resolve to the lane; in a scratch copy they resolve to the scratch's 4th/3rd
ancestor.

```
$ python3 -c "…4x dirname(copy/controls)…; …3x dirname(copy)…"
LANE(copy)= /fast/scratch/hyaku
DEFAULT_REPO(copy counter)= /fast/scratch/hyaku

$ python3 /fast/scratch/hyaku/mori-r51/Mo51ExecC1Controls/copy/controls/c1-controls.py aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd <S>/k <S>/receipts
fatal: repository '/fast/scratch/hyaku' does not exist
Traceback (most recent call last):
  File ".../copy/controls/c1-controls.py", line 94, in <module>
    main(*sys.argv[1:4])
  File ".../copy/controls/c1-controls.py", line 48, in main
    subprocess.run(["git", "clone", "-q", "--no-local", LANE, k], check=True, timeout=600)
subprocess.CalledProcessError: Command '['git', 'clone', '-q', '--no-local', '/fast/scratch/hyaku', '<S>/k/K']' returned non-zero exit status 128.
exit=1
```

`count-c1.py:38` would also be wrong in the same way: `c1-controls.py:84` runs the counter without `--hide`, so
`--hide` falls back to the copied counter's `DEFAULT_REPO` — the lane path is what arm B hides and asserts invisible.
A symlink shim (`<scratch>/lane -> lane`, copy placed 4 levels below it) would make `git clone` work but would make
`--hide` the symlink path, leaving the real lane working tree visible inside bwrap and weakening arm B. So the only
choice that preserves the frozen measurement is to restore those two constants to the values the originals compute
in place. Done in a second copy; both edits are one line each and nothing else differs:

```
$ diff -u copy/count-c1.py copy-fixed/count-c1.py
-DEFAULT_REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
+DEFAULT_REPO = "/home/vgpnk/Projects/shokunin/mori-shokunin"  # relocated-copy fix: value the original computes at its real location
$ diff -u copy/controls/c1-controls.py copy-fixed/controls/c1-controls.py
-LANE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
+LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"  # relocated-copy fix: value the original computes at its real location
$ diff -r copy/controls/witness copy-fixed/controls/witness && echo witness-identical
witness-identical
syntax ok
```

The output directory stayed an argument (`<S>/receipts`); no other path was adjusted. The literal `copy/` tree was
left untouched next to it.

## 3. Run

```
$ export TMPDIR=/fast/scratch/hyaku/mori-r51/Mo51ExecC1Controls/tmp; cd /fast/scratch/hyaku/mori-r51/Mo51ExecC1Controls
$ time python3 copy-fixed/controls/c1-controls.py aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd <S>/k <S>/receipts
do-nothing 1
scratch-only 1
conform-only 1
class-only 1
always-env 1
witness 0

real	1m47.111s
user	9m51.110s
sys	7m22.035s
exit=0
```

Fixture repo assertion and the five control commits (all built on base `aa3af1ec`, throwaway identity from the frozen
builder):

```
$ git -C <S>/k/K rev-parse --show-toplevel
/fast/scratch/hyaku/mori-r51/Mo51ExecC1Controls/k/K
$ git -C <S>/k/K log --format='%H %s' --all | head -5
57a7f66c5a08e00e261e6020922670f03494364f control always-env
81a6b1c4a6662fbfbc86e9ae0702ee85ec70c68e control class-only
b7c10188767408656152a2db7b3dad7bb79c71e0 control conform-only
080d5e48c628931b8194eb95b7d2657a159c9ccd control scratch-only
561672d0931004db8223ee887f5864d6d8c7af2e control witness
```

`do-nothing` has no commit (it is `aa3af1ec` itself, `--repo` = the lane, exactly as the committed receipt's header
shows). The builder's per-control diffs against base have the documented shapes:

```
== ctl-scratch-only   tools/mori-pin-check.py | 2 +-                          (1 insertion, 1 deletion)
== ctl-conform-only   .ufo/waves/round-40/conform.py | 7 +++++--              (5 insertions, 2 deletions)
== ctl-class-only     SKILL.md | 2 +- ; tools/mori-pin-check.py | 135 ++++--   (108 insertions, 29 deletions)
== ctl-always-env     SKILL.md | 2 +- ; tools/mori-pin-check.py | 137 ++++--   (114 insertions, 32 deletions)
== ctl-witness        SKILL.md | 2 +- ; tools/mori-pin-check.py | 137 ++++--   (114 insertions, 32 deletions)
```

## 4. Per-control verdict comparison

Normalization as instructed: `rev=` elided and `kill_residue=<n>` replaced by `NONZERO` only when nonzero.
`same verdict` compares the normalized `C1=` line and the `exit=` line; the `classified:` detail lines were compared
byte-for-byte as well (all six identical to the committed receipts).

| control | committed line (rev elided) | re-run line (rev elided) | same verdict |
|---|---|---|---|
| do-nothing | `C1=unmet kill_residue=12547 relocated=unmet reloc_mismatch=1 classified=bad selftest=pass=114,fail=0 failed=kill_residue,relocated,classified` exit=1 | `C1=unmet kill_residue=12473 relocated=unmet reloc_mismatch=1 classified=bad selftest=pass=114,fail=0 failed=kill_residue,relocated,classified` exit=1 | yes |
| scratch-only | `C1=unmet kill_residue=0 relocated=unmet reloc_mismatch=3 classified=bad selftest=pass=114,fail=0 failed=relocated,classified` exit=1 | identical (only `rev`) | yes |
| conform-only | `C1=unmet kill_residue=12478 relocated=met reloc_mismatch=0 classified=bad selftest=pass=114,fail=0 failed=kill_residue,classified` exit=1 | `C1=unmet kill_residue=12547 relocated=met reloc_mismatch=0 classified=bad selftest=pass=114,fail=0 failed=kill_residue,classified` exit=1 | yes |
| class-only | `C1=unmet kill_residue=1 relocated=unmet reloc_mismatch=2 classified=ok selftest=pass=118,fail=1 failed=kill_residue,relocated,selftest` exit=1 | identical (only `rev`) | yes |
| always-env | `C1=unmet kill_residue=0 relocated=unmet reloc_mismatch=1 classified=bad selftest=pass=118,fail=1 failed=relocated,classified,selftest` exit=1 | identical (only `rev`) | yes |
| witness | `C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=119,fail=0 failed=-` exit=0 | identical (only `rev`) | yes |

Normalized-diff script output (each block: committed line, re-run line, exit pair, classified-line equality):

```
### always-env same=True
  committed: C1=unmet kill_residue=0 relocated=unmet reloc_mismatch=1 classified=bad selftest=pass=118,fail=1 rev=8ee22bde0174ba973e0cbbf76c13b590da84e626 failed=relocated,classified,selftest
  re-run   : C1=unmet kill_residue=0 relocated=unmet reloc_mismatch=1 classified=bad selftest=pass=118,fail=1 rev=57a7f66c5a08e00e261e6020922670f03494364f failed=relocated,classified,selftest
  exit committed=exit=1 re-run=exit=1  norm_equal=True
  classified lines identical=True (6 vs 6)
### class-only same=True
  committed: C1=unmet kill_residue=1 relocated=unmet reloc_mismatch=2 classified=ok selftest=pass=118,fail=1 rev=a7223fe264a9627d4c0972b632d8d5a2d3e59e77 failed=kill_residue,relocated,selftest
  re-run   : C1=unmet kill_residue=1 relocated=unmet reloc_mismatch=2 classified=ok selftest=pass=118,fail=1 rev=81a6b1c4a6662fbfbc86e9ae0702ee85ec70c68e failed=kill_residue,relocated,selftest
  exit committed=exit=1 re-run=exit=1  norm_equal=True
  classified lines identical=True (6 vs 6)
### conform-only same=True
  committed: C1=unmet kill_residue=12478 relocated=met reloc_mismatch=0 classified=bad selftest=pass=114,fail=0 rev=d57cd56e1ded99675ea560de5b559404ae5e3c4d failed=kill_residue,classified
  re-run   : C1=unmet kill_residue=12547 relocated=met reloc_mismatch=0 classified=bad selftest=pass=114,fail=0 rev=b7c10188767408656152a2db7b3dad7bb79c71e0 failed=kill_residue,classified
  exit committed=exit=1 re-run=exit=1  norm_equal=True
  classified lines identical=True (6 vs 6)
### do-nothing same=True
  committed: C1=unmet kill_residue=12547 relocated=unmet reloc_mismatch=1 classified=bad selftest=pass=114,fail=0 rev=aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd failed=kill_residue,relocated,classified
  re-run   : C1=unmet kill_residue=12473 relocated=unmet reloc_mismatch=1 classified=bad selftest=pass=114,fail=0 rev=aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd failed=kill_residue,relocated,classified
  exit committed=exit=1 re-run=exit=1  norm_equal=True
  classified lines identical=True (6 vs 6)
### scratch-only same=True
  committed: C1=unmet kill_residue=0 relocated=unmet reloc_mismatch=3 classified=bad selftest=pass=114,fail=0 rev=cb0a8c5255f15015961b70b38a604a9d4fd83603 failed=relocated,classified
  re-run   : C1=unmet kill_residue=0 relocated=unmet reloc_mismatch=3 classified=bad selftest=pass=114,fail=0 rev=080d5e48c628931b8194eb95b7d2657a159c9ccd failed=relocated,classified
  exit committed=exit=1 re-run=exit=1  norm_equal=True
  classified lines identical=True (6 vs 6)
### witness same=True
  committed: C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=119,fail=0 rev=42719d0f30724bad64f55a68a61e16e8f14a7567 failed=-
  re-run   : C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=119,fail=0 rev=561672d0931004db8223ee887f5864d6d8c7af2e failed=-
  exit committed=exit=0 re-run=exit=0  norm_equal=True
  classified lines identical=True (6 vs 6)
```

Only the control commit ids differ (committer timestamp of the fresh fixture repo): every control commit is built
anew on the same base, so `rev=` is not comparable across runs — the seat spec's normalization is required, not
optional.

## 5. Re-run receipts, verbatim

```
=== control-c1-do-nothing.txt
$ python3 .ufo/waves/round-51/count-c1.py aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch /fast/scratch/hyaku/mori-r51/Mo51ExecC1Controls/k/s-do-nothing
classified: pin line=3 kind=tally prefix=ENVA_SELFTEST state=mismatch pinned='pass=3 fail=0' observed=None rc=2 cmd='python3 tools/enva.py --selftest'
classified: pin line=4 kind=tally prefix=ENVB_SELFTEST state=mismatch pinned='pass=4 fail=0' observed=None rc=1 cmd='python3 tools/envb.py --selftest'
classified: pin line=5 kind=tally prefix=STLA_SELFTEST state=mismatch pinned='pass=4 fail=0' observed='pass=5 fail=0' rc=0 cmd='python3 tools/stla.py --selftest'
classified: pin line=6 kind=tally prefix=STLB_SELFTEST state=mismatch pinned='pass=2 fail=0' observed='pass=2 fail=0' rc=1 cmd='python3 tools/stlb.py --selftest'
classified: pin line=7 kind=tally prefix=OKAY_SELFTEST state=match pinned='pass=1 fail=0' observed='pass=1 fail=0' rc=0 cmd='python3 tools/okay.py --selftest'
classified: PIN_CHECK=unmet tally_pins=5 digest_pins=0 mismatches=4 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=- baseline=no
kill_residue_first: !! .scratch/pin-check-wrktx2jp/tree/.gitignore
C1=unmet kill_residue=12473 relocated=unmet reloc_mismatch=1 classified=bad selftest=pass=114,fail=0 rev=aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd failed=kill_residue,relocated,classified
exit=1

=== control-c1-scratch-only.txt
$ python3 .ufo/waves/round-51/count-c1.py 080d5e48c628931b8194eb95b7d2657a159c9ccd --repo /fast/scratch/hyaku/mori-r51/Mo51ExecC1Controls/k/K --scratch /fast/scratch/hyaku/mori-r51/Mo51ExecC1Controls/k/s-scratch-only
classified: pin line=3 kind=tally prefix=ENVA_SELFTEST state=mismatch pinned='pass=3 fail=0' observed=None rc=2 cmd='python3 tools/enva.py --selftest'
classified: pin line=4 kind=tally prefix=ENVB_SELFTEST state=mismatch pinned='pass=4 fail=0' observed=None rc=1 cmd='python3 tools/envb.py --selftest'
classified: pin line=5 kind=tally prefix=STLA_SELFTEST state=mismatch pinned='pass=4 fail=0' observed='pass=5 fail=0' rc=0 cmd='python3 tools/stla.py --selftest'
classified: pin line=6 kind=tally prefix=STLB_SELFTEST state=mismatch pinned='pass=2 fail=0' observed='pass=2 fail=0' rc=1 cmd='python3 tools/stlb.py --selftest'
classified: pin line=7 kind=tally prefix=OKAY_SELFTEST state=match pinned='pass=1 fail=0' observed='pass=1 fail=0' rc=0 cmd='python3 tools/okay.py --selftest'
classified: PIN_CHECK=unmet tally_pins=5 digest_pins=0 mismatches=4 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=- baseline=no
kill_residue_first: -
C1=unmet kill_residue=0 relocated=unmet reloc_mismatch=3 classified=bad selftest=pass=114,fail=0 rev=080d5e48c628931b8194eb95b7d2657a159c9ccd failed=relocated,classified
exit=1

=== control-c1-conform-only.txt
$ python3 .ufo/waves/round-51/count-c1.py b7c10188767408656152a2db7b3dad7bb79c71e0 --repo /fast/scratch/hyaku/mori-r51/Mo51ExecC1Controls/k/K --scratch /fast/scratch/hyaku/mori-r51/Mo51ExecC1Controls/k/s-conform-only
classified: pin line=3 kind=tally prefix=ENVA_SELFTEST state=mismatch pinned='pass=3 fail=0' observed=None rc=2 cmd='python3 tools/enva.py --selftest'
classified: pin line=4 kind=tally prefix=ENVB_SELFTEST state=mismatch pinned='pass=4 fail=0' observed=None rc=1 cmd='python3 tools/envb.py --selftest'
classified: pin line=5 kind=tally prefix=STLA_SELFTEST state=mismatch pinned='pass=4 fail=0' observed='pass=5 fail=0' rc=0 cmd='python3 tools/stla.py --selftest'
classified: pin line=6 kind=tally prefix=STLB_SELFTEST state=mismatch pinned='pass=2 fail=0' observed='pass=2 fail=0' rc=1 cmd='python3 tools/stlb.py --selftest'
classified: pin line=7 kind=tally prefix=OKAY_SELFTEST state=match pinned='pass=1 fail=0' observed='pass=1 fail=0' rc=0 cmd='python3 tools/okay.py --selftest'
classified: PIN_CHECK=unmet tally_pins=5 digest_pins=0 mismatches=4 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=- baseline=no
kill_residue_first: !! .scratch/pin-check-m4s_7rxg/tree/.gitignore
C1=unmet kill_residue=12547 relocated=met reloc_mismatch=0 classified=bad selftest=pass=114,fail=0 rev=b7c10188767408656152a2db7b3dad7bb79c71e0 failed=kill_residue,classified
exit=1

=== control-c1-class-only.txt
$ python3 .ufo/waves/round-51/count-c1.py 81a6b1c4a6662fbfbc86e9ae0702ee85ec70c68e --repo /fast/scratch/hyaku/mori-r51/Mo51ExecC1Controls/k/K --scratch /fast/scratch/hyaku/mori-r51/Mo51ExecC1Controls/k/s-class-only
classified: pin line=3 kind=tally prefix=ENVA_SELFTEST state=mismatch pinned='pass=3 fail=0' observed=None rc=2 cmd='python3 tools/enva.py --selftest' class=env
classified: pin line=4 kind=tally prefix=ENVB_SELFTEST state=mismatch pinned='pass=4 fail=0' observed=None rc=1 cmd='python3 tools/envb.py --selftest' class=env
classified: pin line=5 kind=tally prefix=STLA_SELFTEST state=mismatch pinned='pass=4 fail=0' observed='pass=5 fail=0' rc=0 cmd='python3 tools/stla.py --selftest' class=stale
classified: pin line=6 kind=tally prefix=STLB_SELFTEST state=mismatch pinned='pass=2 fail=0' observed='pass=2 fail=0' rc=1 cmd='python3 tools/stlb.py --selftest' class=stale
classified: pin line=7 kind=tally prefix=OKAY_SELFTEST state=match pinned='pass=1 fail=0' observed='pass=1 fail=0' rc=0 cmd='python3 tools/okay.py --selftest'
classified: PIN_CHECK=unmet tally_pins=5 digest_pins=0 mismatches=4 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=- baseline=no env=2 stale=2
kill_residue_first: !! .scratch/pin-check-zaojsk57/tree/
C1=unmet kill_residue=1 relocated=unmet reloc_mismatch=2 classified=ok selftest=pass=118,fail=1 rev=81a6b1c4a6662fbfbc86e9ae0702ee85ec70c68e failed=kill_residue,relocated,selftest
exit=1

=== control-c1-always-env.txt
$ python3 .ufo/waves/round-51/count-c1.py 57a7f66c5a08e00e261e6020922670f03494364f --repo /fast/scratch/hyaku/mori-r51/Mo51ExecC1Controls/k/K --scratch /fast/scratch/hyaku/mori-r51/Mo51ExecC1Controls/k/s-always-env
classified: pin line=3 kind=tally prefix=ENVA_SELFTEST state=mismatch pinned='pass=3 fail=0' observed=None rc=2 cmd='python3 tools/enva.py --selftest' class=env
classified: pin line=4 kind=tally prefix=ENVB_SELFTEST state=mismatch pinned='pass=4 fail=0' observed=None rc=1 cmd='python3 tools/envb.py --selftest' class=env
classified: pin line=5 kind=tally prefix=STLA_SELFTEST state=mismatch pinned='pass=4 fail=0' observed='pass=5 fail=0' rc=0 cmd='python3 tools/stla.py --selftest' class=env
classified: pin line=6 kind=tally prefix=STLB_SELFTEST state=mismatch pinned='pass=2 fail=0' observed='pass=2 fail=0' rc=1 cmd='python3 tools/stlb.py --selftest' class=env
classified: pin line=7 kind=tally prefix=OKAY_SELFTEST state=match pinned='pass=1 fail=0' observed='pass=1 fail=0' rc=0 cmd='python3 tools/okay.py --selftest'
classified: PIN_CHECK=unmet tally_pins=5 digest_pins=0 mismatches=4 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=- baseline=no env=4 stale=0
kill_residue_first: -
C1=unmet kill_residue=0 relocated=unmet reloc_mismatch=1 classified=bad selftest=pass=118,fail=1 rev=57a7f66c5a08e00e261e6020922670f03494364f failed=relocated,classified,selftest
exit=1

=== control-c1-witness.txt
$ python3 .ufo/waves/round-51/count-c1.py 561672d0931004db8223ee887f5864d6d8c7af2e --repo /fast/scratch/hyaku/mori-r51/Mo51ExecC1Controls/k/K --scratch /fast/scratch/hyaku/mori-r51/Mo51ExecC1Controls/k/s-witness
classified: pin line=3 kind=tally prefix=ENVA_SELFTEST state=mismatch pinned='pass=3 fail=0' observed=None rc=2 cmd='python3 tools/enva.py --selftest' class=env
classified: pin line=4 kind=tally prefix=ENVB_SELFTEST state=mismatch pinned='pass=4 fail=0' observed=None rc=1 cmd='python3 tools/envb.py --selftest' class=env
classified: pin line=5 kind=tally prefix=STLA_SELFTEST state=mismatch pinned='pass=4 fail=0' observed='pass=5 fail=0' rc=0 cmd='python3 tools/stla.py --selftest' class=stale
classified: pin line=6 kind=tally prefix=STLB_SELFTEST state=mismatch pinned='pass=2 fail=0' observed='pass=2 fail=0' rc=1 cmd='python3 tools/stlb.py --selftest' class=stale
classified: pin line=7 kind=tally prefix=OKAY_SELFTEST state=match pinned='pass=1 fail=0' observed='pass=1 fail=0' rc=0 cmd='python3 tools/okay.py --selftest'
classified: PIN_CHECK=unmet tally_pins=5 digest_pins=0 mismatches=4 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=- baseline=no env=2 stale=2
kill_residue_first: -
C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=119,fail=0 rev=561672d0931004db8223ee887f5864d6d8c7af2e failed=-
exit=0
```

## 6. Determinism of the control variants (independent of my run's commit ids)

The builder writes the frozen witness bytes and one-line variants of them; verified straight out of my fixture repo:

```
$ git -C <S>/k/K show ctl-witness:tools/mori-pin-check.py | sha256sum
35c69d9115b5e45f91a4b0311ce95c03b3b2b929250e2afb31b571a49687b3bf   (= freeze-sha256.txt witness/mori-pin-check.py)
$ git -C <S>/k/K show ctl-witness:.ufo/waves/round-40/conform.py | sha256sum
7f5174d542bd983552670b06f6cc424b10e53c81e55ecabcdd919f4043bdfa23   (= freeze-sha256.txt witness/conform.py)
$ git -C <S>/k/K show ctl-witness:SKILL.md | grep -o 'PIN_CHECK_SELFTEST pass=[0-9]* fail=[0-9]*'
PIN_CHECK_SELFTEST pass=119 fail=0
$ diff copy/controls/witness/mori-pin-check.py <(git -C <S>/k/K show ctl-class-only:tools/mori-pin-check.py)   # class-only
912c912
<     scratch_parent = os.path.abspath(args.scratch) if args.scratch else tempfile.gettempdir()
---
>     scratch_parent = os.path.join(repo, ".scratch")
$ diff copy/controls/witness/mori-pin-check.py <(git -C <S>/k/K show ctl-always-env:tools/mori-pin-check.py)   # always-env
824c824
<                 kind = "env" if observed is None else "stale"
---
>                 kind = "env"
$ git -C <S>/k/K show aa3af1ec:SKILL.md | grep -o 'PIN_CHECK_SELFTEST pass=[0-9]* fail=[0-9]*'
PIN_CHECK_SELFTEST pass=114 fail=0
$ git -C <S>/k/K show aa3af1ec:tools/mori-pin-check.py | sha256sum
697ab2cc6ca6702a5abcf361f48bee31570b4c58ddcc386f41c84c84b5c08e39
```

So each control differs from the witness by exactly the documented knob (`class-only`: scratch export put back under
`<repo>/.scratch`; `always-env`: every mismatch tagged env) and carries the 114 -> 119 SKILL pin, matching the
committed intent. `conform-only` and `scratch-only` are base-only diffs (per §3 stat: 1 file each).

## 7. Nothing in the wave was written by this run

`sha256sum` of the frozen files after the run, compared with `evidence/freeze-sha256.txt`: `count-c1.py`
`622f650c…`, `controls/c1-controls.py` `8351ba6d…`, `controls/witness/conform.py` `7f5174d5…`,
`controls/witness/mori-pin-check.py` `35c69d91…`, and the six committed receipts `1f9362e6…`, `a29b4ecf…`,
`68bacf6d…`, `385de819…`, `75b26a6d…`, `bbe08012…` — all unchanged. `git -C <lane> status --porcelain
--untracked-files=all -- .ufo/waves/round-51` lists only pre-existing untracked wave artefacts (`w1.ready`,
`w1.ready.partial`, sibling seats' `w1/*.md`, `w1/swarm-registry.json`); no modified tracked file. My only write in
the lane is this report.

## Named limits of this re-execution

- The control builder and the counter both derive the source repo from their own file location, so a scratch copy
  measured nothing until two constants were restored (§2). That fix is mine, not the L1's: the control commits were
  rebuilt from the same frozen base by the same frozen builder bytes, but the L1's throwaway fixture repo
  (`/fast/scratch/hyaku/mori-r51/L1/ctl/K`, named in the committed receipt headers) no longer exists, so the
  committed commit ids `8ee22bde…`, `a7223fe2…`, `d57cd56e…`, `cb0a8c52…`, `42719d0f…` cannot be
  re-verified, only the receipts and the builder's determinism (§6).
- `kill_residue` in arm A is a timing measurement: I observed 12473 (do-nothing) and 12547 (conform-only) where the
  committed receipts had 12547 and 12478. Both nonzero, so both remain `unmet` for that arm; no verdict moves.
- One run per control, on one host, with the same kernel/bwrap/python as the committed receipts. A second host or a
  different bwrap would be a new check, not a repetition.
- The do-nothing receipt here ran with `--repo` = the lane worktree (as the committed one did); the other five ran
  against my rebuilt `K`. Six counters ran concurrently, as the builder always does, so their arm-A kill timings
  interleave — this is the builder's own behaviour and matches the committed run.

## Findings

- **MED** — `.ufo/waves/round-51/controls/c1-controls.py:23` (`LANE` four levels up from `HERE`) and
  `.ufo/waves/round-51/count-c1.py:38` (`DEFAULT_REPO` three levels up from `HERE`): the control harness cannot be
  re-run from a copy outside the lane. A literal copy runs `git clone --no-local /fast/scratch/hyaku` and dies with
  `CalledProcessError` exit 1 before any arm runs, and the counter's `--hide` (arm B's hidden path) would silently
  follow the copy's own location, so a symlink shim would hide a path the tool never uses rather than the lane. A
  re-run therefore needs either these two constants restored (what I did, disclosed above) or an explicit repo/hide
  argument. Named as a limit for the report; not a request to change the frozen counter.
- **LOW** — `evidence/control-c1-do-nothing.txt` / `evidence/control-c1-conform-only.txt`: `kill_residue` varies
  between runs (12547 vs my 12473; 12478 vs my 12547). The contract already names the variance ("12475–12547
  observed"); my lower value 12473 widens that range, and none of it changes a verdict because the arm only tests
  "zero or not".
- **LOW** — `evidence/control-c1-*.txt` headers: committed receipt revs are rebuild-specific commit ids and the
  fixture repo that produced them is gone, so a future reviewer comparing receipts must normalize `rev=` (as the
  seat spec says) and can only cross-check the variants through the frozen witness sha256 (§6), not through the
  commits.
- **LOW** — `.ufo/waves/round-51/controls/c1-controls.py:84` runs the counter without `--hide`, so arm B's hidden
  path is whatever `count-c1.py` computes as its default repo. In place that is the lane (correct); in any relocated
  copy it is not. Worth one sentence in the C1 named limits ("the relocated arm hides the counter's own default
  repo").
