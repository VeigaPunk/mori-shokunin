# ExecCensusRegression — lane census regression battery after the round-36 changes

**Seat:** ExecCensusRegression (executor, wave 2, attempt 2)
**Lane repo:** `/home/vgpnk/Projects/shokunin/mori-shokunin` (read-only for this seat)
**Fleet repo:** `/home/vgpnk/Projects/shokunin` (read-only for this seat)
**Item attacked:** the lane census regression battery after the round-36 changes —
`bash tools/mori-census.sh --selftest` and `bash tools/mori-silence-cases.sh` — compared against the
SCORECARD-measured baselines. A drop in either tally is a FAIL (no-harm to operability).

## 1. Summary of what was measured

| instrument | command | baseline (SCORECARD) | measured | exit |
|---|---|---|---|---|
| census selftest | `bash tools/mori-census.sh --selftest` | `PASS (134 cases, 134 passed, 0 failed)` (SCORECARD.md:1127, :1260) | `MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)` | 0 |
| silence oracle | `bash tools/mori-silence-cases.sh` | `matched=28 total=28` exit 0 (SCORECARD.md:1127, :1260) | `MORI_SILENCE_CASES: matched=28 total=28` | 0 |

**No drop in either tally.** Both instruments reproduce their recorded baselines exactly, at the landed
data tip `bf0df77fee4b6ef54a90aea09335c7617f125151` and at the newer tip `6b68b2e`.

## 2. Primary measurement — pasted output and exit codes

### 2.1 Census selftest

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && bash tools/mori-census.sh --selftest
PASS cli: unknown arg exit 2 (exit 2)
PASS cli: --help exit 0 (exit 0)
PASS cli: --pin without a path exits 2 (exit 2)
PASS cli: --drift without a path exits 2 (exit 2)
MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)
EXIT=0
```

(Full 134-case transcript: `/fast/scratch/hyaku/mori-r36/ExecCensusRegression/selftest.out`.)

### 2.2 Silence oracle

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && bash tools/mori-silence-cases.sh
PASS subject-hidden-behind-sibling-head (state=progressing via lane finding=0 rc=0 nonce=1)
PASS committed-report-closes (state=not-open via lane finding=0 rc=0 nonce=1)
PASS substring-email-mismatch-weak (state=progressing-weak via lane finding=0 rc=0 nonce=1)
PASS young-under-gate (state=young via lane finding=0 rc=0 nonce=1)
PASS subject-postlaunch-progressing (state=progressing via lane finding=0 rc=0 nonce=1)
PASS main-repo-noise-silent (state=silent via lane finding=1 rc=1 nonce=1)
PASS young-future-launch (state=young via lane finding=0 rc=0 nonce=1)
PASS old-report-before-relaunch-silent (state=silent via lane finding=1 rc=1 nonce=1)
PASS unreadable-git-unavailable (state=unavailable via lane finding=0 rc=0 nonce=1)
PASS report-future-no-close (state=silent via lane finding=1 rc=1 nonce=1)
PASS same-round-relaunch-silent (state=silent via lane finding=1 rc=1 nonce=1)
PASS sibling-clean-checkout-weak (state=progressing-weak via lane finding=0 rc=0 nonce=1)
PASS completed-not-open (state=not-open via lane finding=0 rc=0 nonce=1)
PASS untracked-recent-progress (state=progressing via lane finding=0 rc=0 nonce=1)
PASS author-subject-committer-sibling-progress (state=progressing via lane finding=0 rc=0 nonce=1)
PASS author-sibling-committer-subject-weak (state=progressing-weak via lane finding=0 rc=0 nonce=1)
PASS repo-missing-unavailable (state=unavailable via lane finding=0 rc=0 nonce=1)
PASS report-eq-launch-no-close (state=silent via lane finding=1 rc=1 nonce=1)
PASS nolane-launch-not-open (state=not-open via lane finding=0 rc=0 nonce=1)
PASS untracked-report-progress (state=progressing via lane finding=0 rc=0 nonce=1)
PASS dirty-same-path-as-sibling-progress (state=progressing via lane finding=0 rc=0 nonce=1)
PASS silent-open (state=silent via lane finding=1 rc=1 nonce=1)
PASS legacy-steer-open-silent (state=silent via lane finding=1 rc=1 nonce=1)
PASS substring-name-mismatch-weak (state=progressing-weak via lane finding=0 rc=0 nonce=1)
PASS shape-invariance
PASS young-age-equals-gate (state=young via lane finding=0 rc=0 nonce=1)
PASS ledger-missing-not-silent (state=unavailable via lane finding=0 rc=0 nonce=1)
PASS readonly-no-mutation
SHUFFLE_SEED=1087467048
RUN_NONCE=3357942853
CASE_ORDER=subject-hidden-behind-sibling-head committed-report-closes substring-email-mismatch-weak young-under-gate subject-postlaunch-progressing main-repo-noise-silent young-future-launch old-report-before-relaunch-silent unreadable-git-unavailable report-future-no-close same-round-relaunch-silent sibling-clean-checkout-weak completed-not-open untracked-recent-progress author-subject-committer-sibling-progress author-sibling-committer-subject-weak repo-missing-unavailable report-eq-launch-no-close nolane-launch-not-open untracked-report-progress dirty-same-path-as-sibling-progress silent-open legacy-steer-open-silent substring-name-mismatch-weak shape-invariance young-age-equals-gate ledger-missing-not-silent readonly-no-mutation
MORI_SILENCE_CASES: matched=28 total=28
EXIT=0
```

(Transcript: `/fast/scratch/hyaku/mori-r36/ExecCensusRegression/silence.out`. The 28 case ids are exactly
the pre-registered set — 27 named cases plus `shape-invariance` — with no case renamed, removed or added.)

### 2.3 Comparison to the recorded baselines

- SCORECARD.md:1127 — "Census selftest 134/134, terminal 49 arms, other named selftests, oracle 28/28".
- SCORECARD.md:1260 — "census selftest 134/134, silence oracle 28/28, census bytes unchanged".
- Measured now: selftest **134/134** (exit 0), oracle **28/28** (exit 0). **Match, no drop.**

## 3. Why the round-36 changes cannot have altered these instruments

The round-36 diff touches no census or oracle byte, so the round's changes are provably inert for this item:

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ git show 6bd57097:tools/mori-census.sh | sha256sum
87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28  -
$ sha256sum tools/mori-census.sh
87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28  tools/mori-census.sh

$ git show 6bd57097:tools/mori-silence-cases.sh | sha256sum
34cd5770889ec6e7521b477aa9976cece7a64e07b83774c12ce2aea73161abfa  -
$ sha256sum tools/mori-silence-cases.sh
34cd5770889ec6e7521b477aa9976cece7a64e07b83774c12ce2aea73161abfa  tools/mori-silence-cases.sh
```

Round base `6bd57097` and the landed data tip `bf0df77` are **byte-identical** for both instruments
(`git diff --stat 6bd57097 bf0df77` lists only new round-36 tools, SOURCES/QUALITY/SKILL rows and wave
evidence — 118 files, 33850 insertions, no change to `tools/mori-census.sh` or `tools/mori-silence-cases.sh`).
The same two SHAs hold at the newer tip `6b68b2e`.

## 4. Flake battery (round-9's registered flake class was 1/8–25%)

Eight consecutive runs of each instrument, to test for the historical SIGPIPE/grep flake class and for
order/nonce sensitivity:

```
selftest run 1 exit=0 :: 134 pass :: MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)
selftest run 2 exit=0 :: 134 pass :: MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)
selftest run 3 exit=0 :: 134 pass :: MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)
selftest run 4 exit=0 :: 134 pass :: MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)
selftest run 5 exit=0 :: 134 pass :: MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)
selftest run 6 exit=0 :: 134 pass :: MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)
selftest run 7 exit=0 :: 134 pass :: MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)
selftest run 8 exit=0 :: 134 pass :: MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)
--- oracle ---
oracle run 1 exit=0 :: MORI_SILENCE_CASES: matched=28 total=28
oracle run 2 exit=0 :: MORI_SILENCE_CASES: matched=28 total=28
oracle run 3 exit=0 :: MORI_SILENCE_CASES: matched=28 total=28
oracle run 4 exit=0 :: MORI_SILENCE_CASES: matched=28 total=28
oracle run 5 exit=0 :: MORI_SILENCE_CASES: matched=28 total=28
oracle run 6 exit=0 :: MORI_SILENCE_CASES: matched=28 total=28
oracle run 7 exit=0 :: MORI_SILENCE_CASES: matched=28 total=28
oracle run 8 exit=0 :: MORI_SILENCE_CASES: matched=28 total=28
```

```
$ grep -h '^MORI_CENSUS_SELFTEST' st-*.out | sort | uniq -c
      8 MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)
$ grep -h '^MORI_SILENCE_CASES' or-*.out | sort | uniq -c
      8 MORI_SILENCE_CASES: matched=28 total=28
$ grep -h '^FAIL ' st-*.out or-*.out | head
(no output)
```

**16/16 green, zero flakes.** The 8 oracle runs used 8 different case orders and 8 different nonces
(per-run shuffle + nonce are independent by construction), so the green is not order- or nonce-pinned.

## 5. Adjacent lane gates exercised (no-harm sweep, same lane)

Not part of the assigned two instruments, but run because the round changed `SKILL.md` gate-registry rows
and `corpus/SOURCES.md`, and the r13 gate pins `SKILL.md` content:

```
$ python3 tools/mori-round13-regressions.py --output $S/r13-out
MORI_R13_REGRESSIONS: claims=24 pass=24 exit=0
GATE registered name=r13 regressions registry=/home/vgpnk/Projects/shokunin/mori-shokunin/SKILL.md
EXIT=0
```
The r13 gate's own two headline oracles are green inside that run, including
`FINDING R13_F02_HONEST_28_OF_28 status=pass ... matched=28 total=28 rc=0` (the honest oracle) and
`FINDING R13_F02_REJECT_BANANA status=pass ... matched=0 total=28 rc=1` (the substituted-verdict control),
so the round's SKILL.md additions did not disturb the registry-row matching or the oracle contract.

Other lane selftests, all green:

```
$ python3 tools/mori-round14-regressions.py --selftest   -> EXIT=0  SELFTEST: pass checks=20 (parsers + real-gate red rc1/tamper rc2)
$ python3 tools/mori-round15-regressions.py --selftest   -> EXIT=0  SELFTEST PASS selftest_root=/tmp/mori-r15-selftest-tv483nq6
$ python3 tools/mori-round16-regressions.py --selftest   -> EXIT=0  SELFTEST ok: pin_rc0,green_rc0_verdict_ok,absent_rc1_capability_absent,tool_drift_rc2,bad_want_rc1_mismatch,pack_drift_rc2
$ python3 tools/mori-seat-terminal.py --selftest        -> EXIT=0  {"arms":49,"passed":49,"finding_id":"SELFTEST_OK",...}
```

The round-36 tools' own declared selftests, all green:

```
$ python3 tools/mori-source-drift.py --selftest         -> EXIT=0  MORI_SOURCE_DRIFT_SELFTEST: PASS (4 cases)
$ python3 tools/mori-sources-appendonly.py --selftest  -> EXIT=0  MORI_SOURCES_APPENDONLY_SELFTEST pass=8 fail=0
$ bash tools/mori-index-clean.sh --selftest             -> EXIT=0  MORI_INDEX_CLEAN_SELFTEST pass=4 fail=0
```

And the two round-36 gates run against the lane itself:

```
$ bash tools/mori-index-clean.sh .
MORI_INDEX_CLEAN staged=0 intent_to_add=0
index-clean EXIT=0

$ python3 tools/mori-sources-appendonly.py bf0df77fee4b6ef54a90aea09335c7617f125151 --round-base 6bd57097
... (18 superseded rows S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193)
appendonly_violations=18 ids=[...] deleted=[] superseded=[...] round_changed=[]
appendonly EXIT=0
```

`round_changed=[]` with exit 0 — identical to the L1's post-data measurement.

## 6. Live census (context, not a baseline)

```
$ MORI_SHOKUNIN_ROOT=/home/vgpnk/Projects/shokunin bash tools/mori-census.sh
FINDING WATCHDOG_ABSENT severity=warn obs=no shokunin-watchdog process matched by pgrep ...
FINDING OOM_KILL_JOURNAL severity=crit obs=class=oom_kill alarm=1 ...
FINDING WAVE_UNSETTLED_AGE severity=warn obs=wave=shokunin12h-20261014-p1-audit age_s=755937 ...
MORI_CENSUS: DRIFT (findings=32 drift=12 unavailable=1 surfaces=8)
EXIT=1
```

This is live **host** state (no watchdog process running, current-boot OOM journal records, aged
unsettled waves) and not an instrument regression: the census bytes are unchanged from the round base,
the selftest is 134/134, and the drift pin is red on the **round base tree** as well:

```
$ cd $S/base-tree && bash tools/mori-census.sh --drift .../baseline-r20-20261021T1051Z.json
MORI_DRIFT: +FINDING:CGROUP_OOM_KILL_CUMULATIVE +FINDING:DISK_CRITICAL ... -SURFACE:lane.mori ...
BASE DRIFT EXIT=1
```

Both the tip and the base tree exit 1 against the r20 pin, and the differing token sets are live
host-state fields (wave ages, lane rows, disk). This is the already-carried "r10/r20 drift pin stays
red, no re-pin" debt recorded in SCORECARD.md:1222, not a round-36 regression. It is also **not** the
assigned item and this seat does not re-pin.

## 7. Collateral finding (outside the assigned item, NOT a round-36 defect) — the r17-jj gate is environment-dependent

While sweeping the sibling lane gates I found `tools/mori-round17-jj-regressions.py --selftest` red in
this environment. It is **not** caused by the round-36 changes, and it is **not** the assigned item, but it
is a real red against a SCORECARD-recorded baseline, so it is reported with evidence.

Measured, repeatedly:

```
$ python3 tools/mori-round17-jj-regressions.py --selftest --scratch $S/scratch17
SELFTEST FAIL: ok_rc0: rc=1 mori-round17-jj-regressions: cases=17 match=8 mismatch=9 capability_absent=0 setup_failed=0 assertions=204 failed=9 retained=False
EXIT=1
```

**It is not a round-36 regression.** The identical failure reproduces on a pristine copy of the round
base tree `6bd57097` with byte-identical gate bytes:

```
$ git archive 6bd57097 | tar -x -C $S/base-tree
$ cd $S/base-tree && python3 tools/mori-round17-jj-regressions.py --selftest --scratch $S/scratch17c
SELFTEST FAIL: ok_rc0: rc=1 ... cases=17 match=8 mismatch=9 ... assertions=204 failed=9 retained=False
EXIT=1
```

Gate bytes at both the round base and the tip are the same file, `da3e080aa5181e8e00872c1d5f0dd97862c495da03adce0b1aa31e27fbcb89f0`.

**Every one of the 9 failing assertions is the same side-effect assertion**, and all 195 substantive
assertions pass — the jj branch/author behaviour the gate grades is fully correct:

```
$ python3 -c "...read out-ok/run-manifest.json..."
all assertions: 204 failed: 9
cases: {'cases': 17, 'match': 8, 'mismatch': 9, 'assertions': 204, 'failed_assertions': 9, 'failed_cases': 9}
failed assertion ids: Counter({'jj_config_redirected': 9})
jj-helper-commit           mismatch  non-jjcfg failures: 0 of 10
jj-commit-no-bookmark      mismatch  non-jjcfg failures: 0 of 15
jj-ambient-author          mismatch  non-jjcfg failures: 0 of 14
jj-young-ambient-author    mismatch  non-jjcfg failures: 0 of 14
jj-sibling-author          mismatch  non-jjcfg failures: 0 of 10
jj-sidebranch-mirror       mismatch  non-jjcfg failures: 0 of 15
jj-unresolved-mirror       mismatch  non-jjcfg failures: 0 of 11
jj-missingref-mirror       mismatch  non-jjcfg failures: 0 of 11
jj-root-unresolved-closure mismatch  non-jjcfg failures: 0 of 10
git-* cases (7)            match     non-jjcfg failures: 0 of 10..15
```

The failing assertion is `tools/mori-round17-jj-regressions.py:1043-1047`:

```python
    if "jj" in sb and sb["jj"]:
        # The jj repo config is written under the redirected HOME, never under
        # the operator's ~/.config/jj. This is the positive redirect evidence.
        check(
            "jj_config_redirected",
            (sb["home"] / ".config" / "jj").exists(),
            f"path={sb['home'] / '.config' / 'jj'}",
        )
```

**Root cause, isolated by controlled experiment.** The assertion asks whether jj wrote a per-repo
metadata directory under the redirected `$XDG_CONFIG_HOME`. jj 0.45.1 writes
`$XDG_CONFIG_HOME/jj/repos/<hash>/metadata.binpb` only when the workspace's `.jj/repo/config-id` is
present. Isolated probes:

```
# PROBE: colocate a git repo, jj it, run jj against it, with a redirected XDG_CONFIG_HOME
  []                     -> .config/jj: NO
  [GIT_CEILING_DIRECTORIES=/tmp]           -> .config/jj: NO
  [GIT_CONFIG_NOSYSTEM=1]                  -> .config/jj: NO
  [XDG_DATA_HOME/CACHE_HOME/STATE_HOME]    -> .config/jj: NO
  [all of the above together]              -> .config/jj: NO
```

Copying the real lane's `.jj` (which carries `.jj/repo/config-id`) into a scratch tree makes the gate
green; removing that one file makes it red again, with nothing else changed:

```
$ cp -a .jj $S/ws-lane/.jj && cd $S/ws-lane && python3 tools/mori-round17-jj-regressions.py --selftest --scratch $S/ws-lane/wt
SELFTEST ok: guard_output_repo_root,guard_output_tools,guard_output_corpus,guard_output_git,guard_output_jj,...
totals: {"cases": 17, "match": 17, "mismatch": 0, "assertions": 204, "failed_assertions": 0, "failed_cases": 0}
gate sha: da3e080aa5181e8e00872c1d5f0dd97862c495da03adce0b1aa31e27fbcb89f0
EXIT=0

$ cd $S/lane-copy && cp $S/ws-lane/.jj/repo/config-id .jj/repo/config-id   # config-id PRESENT
SELFTEST ok: ... -> EXIT=0
$ cd $S/lane-copy && rm -f .jj/repo/config-id                              # config-id ABSENT
SELFTEST FAIL: ok_rc0: rc=1 ... cases=17 match=8 mismatch=9 ... failed=9
```

This reproduces exactly the recorded round-17 green receipt, which was taken with the scratch inside the
lane's own jj workspace:

```
.ufo/waves/round-17/evidence/final/jj-after/run-manifest.json
  gate sha: da3e080aa5181e8e00872c1d5f0dd97862c495da03adce0b1aa31e27fbcb89f0
  totals: {"cases": 17, "match": 17, "mismatch": 0, "assertions": 204, "failed_assertions": 0, "failed_cases": 0}
  scratch_run: .../.ufo/worktrees/round-17/FinalVerificationFixed/.scratch/jj-after/run-20261020T204321Z-...
  jj_config_redirected  ok=True  path=.../jj-helper-commit/home/.config/jj   (all 9 jj cases True)
```

The green receipt's scratch path sits inside the lane checkout (which carries `.jj/repo/config-id`); a
scratch outside any jj workspace does not. The gate's own guard refuses `.ufo/` outside `.ufo/waves/`
(`tools/mori-round17-jj-regressions.py:1173-1176`), so a compliant scratch today lands outside the
lane's jj workspace and the side-effect assertion cannot pass.

**Consequences for this item, stated plainly:**
- It does **not** affect the assigned instruments. The census selftest (134/134) and the silence oracle
  (28/28) are green in 8/8 runs each, and the r13 gate's own honest-oracle arm (`matched=28 total=28 rc=0`)
  and substituted-verdict control (`matched=0 total=28 rc=1`) are green.
- It is **not** attributable to round-36: identical red on the round base tree with identical gate bytes.
- It is a **latent environment-dependence in the r17-jj gate's own selftest**, not a census or oracle
  defect: the graded behaviour (all 195 substantive assertions) is correct in every case.
- Per the province rules this seat is detection-and-report only: no remediation, no re-pin, no edits to
  the lane. The r17-jj selftest's fixture should arrange a `.jj/repo/config-id` for its jj sandbox
  workspaces (or the assertion should be qualified), so the red stops depending on where the scratch
  tree happens to live.

## 8. Lane-immutability check

This seat wrote exactly one file in the lane (this report). No `git add/commit/push/fetch/reset`, no
mutating jj command, no lane file edited. All scratch output is under
`/fast/scratch/hyaku/mori-r36/ExecCensusRegression/`. After the whole battery:

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && git status --short
?? .scratch/
```

(`.scratch/` is a pre-existing untracked directory from other seats, present before this seat's first
command; the wave-36 evidence files and `w2/` tree were committed by the integrator during this seat's
run, which is why the earlier untracked list is now gone.) No instrument, no corpus file and no wave
evidence file was modified by this seat.

**Tooling installs: none.** No package was installed or upgraded during this seat's work; every command
used is a stock binary already present on the host (`bash`, `python3`, `git`, `jj` 0.45.1,
`/usr/bin/timeout`, `jq`, `tmux`).

## 9. Risks / blockers

- None for the assigned item: both instruments meet their recorded baselines exactly, with zero flakes
  across 8 repeats each.
- Carried, not caused here: the r20 drift pin is red on the base tree as well (SCORECARD.md:1222).
- Carried, not caused here: the r17-jj gate selftest is environment-dependent (§7) — 9/204 assertions
  red for a side-effect reason, all substantive assertions green, identical on the round base tree.

## 10. What my item attacks

The lane census regression battery after the round-36 changes — the census selftest and the silence
oracle — measured against their SCORECARD-recorded baselines, plus the sibling lane gates that the
round's SKILL.md/SOURCES edits could have disturbed. The battery is unchanged by the round, the tallies
match the recorded baselines exactly (134/134 and 28/28, both exit 0, 8/8 repeats), and no drop in
operability was found.

VERDICT: PASS
