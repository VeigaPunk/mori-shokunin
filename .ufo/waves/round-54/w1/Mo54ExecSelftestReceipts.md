# Mo54ExecSelftestReceipts — SHONEN tally-pin receipts for round 54

Seat: execution, receipts only (no claim scored by this seat). Lane `mori-shokunin`. Lane repo
`/home/vgpnk/Projects/shokunin/mori-shokunin`. Measured revision: **`78295c764093ff1f6cee08d7246679900bde7265`**
(round-54 data commit, 2026-10-27 01:37:25 -0300). Host MACHINE_ID: this workstation, kernel `7.2.11-arch1-1` (read
only where relevant; no sysctl, cgroup, log-count or poison action taken — none was needed for a selftest receipt).

What this seat produced: the three SHONEN.md line-7 selftests re-run by hand from a `git archive` of the data commit,
as literal-command receipts the L1 can commit under `.ufo/waves/round-54/evidence/selftests/` — plus the mechanical
cross-check that the same three rows re-measure green through `mori-pin-check.py --rev` at that revision.

## Environment (all runs)

```
archive:  cd /home/vgpnk/Projects/shokunin/mori-shokunin && git archive 78295c764093ff1f6cee08d7246679900bde7265 | tar -x -C <S>/arch
          (<S> = /fast/scratch/hyaku/mori-r54/Mo54ExecSelftestReceipts, rc=0)
cwd:      <S>/arch              # archive root; `git -C <S>/arch rev-parse --show-toplevel` -> fatal: not a git repository
TMPDIR:   <S>/tmp               # created empty, exported for every run
started:  2026-10-27T02:05:15-03:00 (each of the three runs stamped its own start, all in that second)
```

Tool bytes in the extracted tree equal the pinned blobs (`sha256sum` of the file vs `git show <rev>:<path>`):

```
32685b9306db061d2c2df21e976823d84a4017cc3524194f4ed76327443081f0  tools/mori-pin-check.py        (archive=git, SAME)
612d50c1590d5a30a1beae19a8e43da3acba18ddd30d47a6b51c2cdeada76109  tools/mori-unlanded-check.py   (archive=git, SAME)
b3c123400f41a8e8d62e678d81175956c68a9735643a8a3cd09975666be1ffe4  tools/mori-commit-runway.py    (archive=git, SAME)
3a1aef20cc03fc4e323ad8b5400feeeda7cff1373ccd6f77498a8ebf5c450623  tools/fixtures/mori-commit-runway/cases.json  (archive=git, SAME; 26 cases, schema mori-commit-runway-cases-v1)
```

Those three tools are byte-identical between the entering tip `39dcf4d7` and the data commit
(`git diff --stat 39dcf4d7 78295c76 -- tools/` printed nothing), so the counts below measure frozen bytes.

## Receipt drafts (copy verbatim; L1 commits them)

### 1 → `.ufo/waves/round-54/evidence/selftests/mori-pin-check.txt`

```
# run from a git archive of 78295c764093ff1f6cee08d7246679900bde7265 (lane data commit), TMPDIR=/fast/scratch/hyaku/mori-r54/Mo54ExecSelftestReceipts/tmp, 2026-10-27T02:05:15-03:00
# tools/mori-pin-check.py sha256=32685b9306db061d2c2df21e976823d84a4017cc3524194f4ed76327443081f0; 126 lines: 125 PASS, 0 FAIL; wall 18.026s
$ python3 tools/mori-pin-check.py --selftest
PASS v5_rev_export_outside_repo  rc=0 left=0
PASS v51_scratch_inside_repo_refused  rc=2
PASS v51_default_scratch_tmpdir_and_master_is_rev  rc=0 left=0
PASS cli_met_rc0  rc=0
PASS cli_bad_rev_rc2  rc=2
PIN_CHECK_SELFTEST pass=125 fail=0
exit=0
```

First two lines of the same run (for the reader who wants the head as well):

```
PASS honest  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no env=0 stale=0
PASS stale_tally  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no env=0 stale=1
```

### 2 → `.ufo/waves/round-54/evidence/selftests/mori-unlanded-check.txt`

```
# run from a git archive of 78295c764093ff1f6cee08d7246679900bde7265 (lane data commit), TMPDIR=/fast/scratch/hyaku/mori-r54/Mo54ExecSelftestReceipts/tmp, 2026-10-27T02:05:15-03:00
# tools/mori-unlanded-check.py sha256=612d50c1590d5a30a1beae19a8e43da3acba18ddd30d47a6b51c2cdeada76109; 18 lines: 17 PASS, 0 FAIL; wall 0.913s
$ python3 tools/mori-unlanded-check.py --selftest
PASS subdirectory_is_setup_error  --repo is not a repository top level (git top level is /fast/scratch/hyaku/mori-
PASS missing_directory_is_setup_error  setup
PASS cli_dirty_rc1  rc=1
PASS cli_setup_rc2  rc=2
PASS cli_usage_rc2  rc=2
UNLANDED_SELFTEST pass=17 fail=0
exit=0
```

(The `subdirectory_is_setup_error` line is 114 characters: the tool truncates the git top-level path in that
diagnostic; the truncation is the tool's own, not the terminal's — the bytes were captured to a file.)

### 3 → `.ufo/waves/round-54/evidence/selftests/mori-commit-runway.txt`

```
# run from a git archive of 78295c764093ff1f6cee08d7246679900bde7265 (lane data commit), TMPDIR=/fast/scratch/hyaku/mori-r54/Mo54ExecSelftestReceipts/tmp, 2026-10-27T02:05:15-03:00
# tools/mori-commit-runway.py sha256=b3c123400f41a8e8d62e678d81175956c68a9735643a8a3cd09975666be1ffe4; 2 lines; wall 0.306s
$ python3 -I -B tools/mori-commit-runway.py --selftest
MATCHER: rejected 26/26 corrupted expectations
MORI_COMMIT_RUNWAY_SELFTEST: PASS 31/31
exit=0
```

## Mechanical cross-check: the same three pins through `mori-pin-check.py --rev`

These receipts are corroboration, not the instrument: `mori-pin-check.py` is the standing tool that re-executes every
self-test pin in `SKILL.md` against a revision and compares pinned text to observed text. Run at the data commit
(read-only `git clone --shared` into `<S>/pcscratch`, no mutation of the lane repo):

```
$ python3 tools/mori-pin-check.py --rev 78295c764093ff1f6cee08d7246679900bde7265 --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch <S>/pcscratch
pin line=938 kind=tally prefix=PIN_CHECK_SELFTEST state=match pinned='pass=125 fail=0' observed='pass=125 fail=0' rc=0 cmd='python3 tools/mori-pin-check.py --selftest'
pin line=973 kind=tally prefix=UNLANDED_SELFTEST state=match pinned='pass=17 fail=0' observed='pass=17 fail=0' rc=0 cmd='python3 tools/mori-unlanded-check.py --selftest'
pin line=1209 kind=tally prefix=MORI_COMMIT_RUNWAY_SELFTEST state=match pinned=': PASS 31/31' observed=': PASS 31/31' rc=0 cmd='python3 -I -B tools/mori-commit-runway.py --selftest'
PIN_CHECK=met tally_pins=37 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=78295c764093ff1f6cee08d7246679900bde7265 baseline=no env=0 stale=0
exit=0
```

47 `state=match` lines and 0 lines in any failure class; wall 2m7.7s. The data commit's registry is green under its own
reconciler, so the hand receipts and the tool agree — a hand receipt that disagreed with `--rev` would be the signal
to look for.

## The three counts against the SKILL.md pins they feed

```
$ grep -o 'PIN_CHECK_SELFTEST pass=[0-9]* fail=[0-9]*' SKILL.md | sort | uniq -c        -> 1  PIN_CHECK_SELFTEST pass=125 fail=0
$ grep -o 'UNLANDED_SELFTEST pass=[0-9]* fail=[0-9]*' SKILL.md | sort | uniq -c         -> 1  UNLANDED_SELFTEST pass=17 fail=0
$ grep -o 'MORI_COMMIT_RUNWAY_SELFTEST: PASS [0-9]*/[0-9]*' SKILL.md | sort | uniq -c  -> 1  MORI_COMMIT_RUNWAY_SELFTEST: PASS 31/31
$ grep -o 'MATCHER: rejected [0-9]*/[0-9]* corrupted' SKILL.md | sort | uniq -c        -> 1  MATCHER: rejected 26/26 corrupted
```

Each token occurs once (rows `SKILL.md:938`, `:973`, `:1209`), and each agrees with the observed output above. The
runway row's prose "26 cases plus 5 built-in hostile-input checks" matches `cases.json` (26 cases) plus the observed
`PASS 31/31`, and the matcher line's 26/26 matches the case count.

## Comparison with `.ufo/waves/round-53/evidence/selftests/`

| selftest | round 53 (receipt) | round 54 at `78295c76` | verdict |
|---|---|---|---|
| pin-check | `PIN_CHECK_SELFTEST pass=125 fail=0` exit 0 at `2a4213bf` (`mori-pin-check.txt`) | `pass=125 fail=0` exit 0 | identical |
| unlanded-check | `UNLANDED_SELFTEST pass=17 fail=0` exit 0 at `2a4213bf` (`mori-unlanded-check.txt`) | `pass=17 fail=0` exit 0 | identical |
| commit-runway | `PASS 23/23`, matcher 23/23 at the r53 data commit `2a4213bf`; `PASS 31/31`, matcher 26/26 at the r53 final integration tip `0b36d23e` (`mori-commit-runway-a2.txt`) | `PASS 31/31`, matcher 26/26 exit 0 | identical to the r53 a2 receipt; the 23→31 gap is round-53's own history (the case set grew between `2a4213bf` and its integration tip), not a round-54 change |
| registry pins (`--rev`) | `PIN_CHECK=met tally_pins=37 digest_pins=8 mismatches=0 … rev=0b36d23e`, exit 0 (`evidence/pin-check-at-landed.txt`) | same line except `rev=78295c76…`, exit 0 | identical |

Control that makes the runway row apples-to-apples: `0b36d23e` is an ancestor of `78295c76`, and
`git diff --stat 0b36d23e 78295c76 -- tools/` is empty. I re-ran all three selftests from a tools-only archive of
`0b36d23e` in the same scratch/TMPDIR and got `pass=125 fail=0` exit 0, `pass=17 fail=0` exit 0, `PASS 31/31` exit 0
— the same numbers as the data commit, so the counts are a property of the tool bytes, not of the repository state
the selftest happens to run inside (and not of the 30-odd sibling wave seats running concurrently on this host).

## Reproducibility and cleanliness

```
$ python3 tools/mori-pin-check.py --selftest      # run 1 and run 2, identical output, both exit=0, last line PIN_CHECK_SELFTEST pass=125 fail=0
$ diff pin-r1.out pin-r2.out                      # no output (identical)
$ python3 tools/mori-unlanded-check.py --selftest # repeat exit=0
$ python3 -I -B tools/mori-commit-runway.py --selftest  # repeat exit=0
$ ls -A <S>/tmp | wc -l                           # 0 after every run: no temp dir left behind
```

The pin-check selftest includes timeout-class cases (`v51_class_wrong_then_timeout_stale`,
`v51_class_right_then_timeout_env`); both repeats printed them PASS under the wave's concurrent load, so the 125/125 is
not a load artifact on this host at this moment.

## Compliance

- Scratch: everything under `/fast/scratch/hyaku/mori-r54/Mo54ExecSelftestReceipts/` (archive, tools-only r53 archive,
  TMPDIR, `pcscratch` clone); removed before this seat finished. Disk checked first:
  `scripts/hyaku/disk-guard.sh status` → `/fast/scratch/hyaku 28% use, 585.8G free`; no ENOSPC.
- No mutation: no `git add/commit/stash/checkout/reset/pull/push` anywhere, no jj command, no write into
  `~/.local/bin` or any PATH dir, no pacman, no installs (nothing needed installing). The only clone is
  `pin-check`'s own read-only `--shared` clone into my scratch, made by the tool.
- Files written by this seat: this report only. No SKILL/SCORECARD/LOG/PROVINCE/corpus/tools/considerthese edits.
- No line in this report starts with a vote token (the four reserved line starts are avoided).
- Read-only host access: not exercised — a `--selftest` never touches `/proc`; the live runway read is another seat's
  item and I did not run it.

UNVERIFIED by this seat: that `SHONEN.md` line 7 was re-written to the round-54 receipt paths (that is the L1's
integration edit); that the three receipt files exist under `.ufo/waves/round-54/evidence/selftests/` (drafts only
here, per the seat spec).

## Findings

- **LOW — `SHONEN.md:7` still names the round-53 receipt paths** and the round-53 parenthetical "(23/23 at the data
  commit)" plus the a2 file, while the counts it states (125/125, 17/17, 31/31) are already the round-54 numbers. The
  L1's integration edit must swap the three paths to `.ufo/waves/round-54/evidence/selftests/…` and drop the stale
  23/23 aside, or SHONEN will cite round-53 evidence for a round-54 pin. The counts themselves need no change.
- **LOW — `tools/mori-unlanded-check.py` truncates the git-top-level path in its setup diagnostic** to 114 characters
  (`subdirectory_is_setup_error`, observed line ends `…/hyaku/mori-`). Under a deep scratch root the distinguishing
  tail of the wrong top level is lost. Cosmetic; the case still PASSes and the exit code (2) is unchanged. Routed as a
  named limit, not a round-54 fix.
- **LOW — `tools/mori-pin-check.py` selftest is wall-clock sensitive** (18.0 s here; it contains two timeout-class
  cases). It produced identical output twice under the wave's load, so the pin is reliable on this host now, but a
  receipt taken while the host is starved could flake; the receipt's `# … wall 18.026s` comment is there so a later
  reader can see the timing context.
- **INFO — the receipt set proves tool self-consistency, not freshness of anything outside `tools/`.** The three
  selftests read only their own fixtures (`tools/fixtures/mori-commit-runway/cases.json`, 26 cases, sha
  `3a1aef20…`); none of them touches `corpus/knowledge/`, so these receipts carry no weight on C1 or C2. That is by
  design (execution seat, no claim), and the round-54 claim votes remain the only evidence for both claims.
