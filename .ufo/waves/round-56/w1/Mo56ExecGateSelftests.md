# Mo56ExecGateSelftests — no-harm to the lane's standing instruments

Seat: executor, mori round 56, wave `w1`. Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Freeze tip measured: `8be2717b0809281d07dffe83dad424a4859e0747`. Entering tip: `5b295eeebd87ebd610d8d39bfe2035742f740cfa`.
Scratch: `/fast/scratch/hyaku/mori-r56/Mo56ExecGateSelftests/` (`TMPDIR` set there; removed before yield).

Assignment: run the four standing selftests at an archive of the freeze tip, compare each tally with
`round-53/evidence/selftests/` and the `corpus/lessons` references, and report any *new* failure caused
by the round-56 files as HIGH. No lane file was edited; no counter, predicate, control or kill rule was
proposed for change. No tool was installed or upgraded this seat.

## 1. The four named selftests — freeze tip vs entering tip vs baselines

All four were run from `git archive 8be2717b…` extracted to scratch (`$S/work`), plus from
`git archive 5b295eee…` (`$S/enter`), so the round-56 delta is isolated.

```
$ cd /fast/scratch/hyaku/mori-r56/Mo56ExecGateSelftests/work && python3 tools/mori-pin-check.py --selftest
…
PASS r13_self_row_pinned  PIN_CHECK=met tally_pins=2 …
PASS v51_default_scratch_tmpdir_and_master_is_rev  rc=0 left=0
PASS cli_met_rc0  rc=0
PASS cli_bad_rev_rc2  rc=2
PIN_CHECK_SELFTEST pass=125 fail=0
EXIT=0
```

```
$ python3 tools/mori-unlanded-check.py --selftest
PASS list_cap_50_of_60  rc=1 lines=51 last=unlanded ?? .ufo/waves/round-8/w2/F49.md
PASS modified_status_rendered_with_dot  rc=1 ['UNLANDED=dirty round=8 paths=1', 'unlanded .M corpus/lessons/round-8.md']
PASS subdirectory_is_setup_error  --repo is not a repository top level …
PASS missing_directory_is_setup_error  setup
PASS cli_dirty_rc1  rc=1
PASS cli_setup_rc2  rc=2
PASS cli_usage_rc2  rc=2
UNLANDED_SELFTEST pass=17 fail=0
EXIT=0
```

```
$ python3 -I -B tools/mori-commit-runway.py --selftest
MATCHER: rejected 26/26 corrupted expectations
MORI_COMMIT_RUNWAY_SELFTEST: PASS 31/31
EXIT=0
```

```
$ bash tools/mori-census.sh --selftest
PASS disk: device missing from diskstats -> unmeasured disclosed (exit 0 CLEAN)
PASS watchdog: all four non-value classes counted by reason (exit 0 CLEAN)
PASS tmux: sleeping probe is bounded -> rc-124 unavailable, no hang (exit 0 CLEAN)
PASS drift: changed volatile contract is reported (exit 1)
PASS cli: --drift without a path exits 2 (exit 2)
MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)
EXIT=0
```

Same four, run from the entering-tip archive:

```
$ cd .../enter && { python3 tools/mori-pin-check.py --selftest; python3 tools/mori-unlanded-check.py --selftest;
                    python3 -I -B tools/mori-commit-runway.py --selftest; bash tools/mori-census.sh --selftest; }
PIN_CHECK_SELFTEST pass=125 fail=0     PIN_EXIT=0
UNLANDED_SELFTEST pass=17 fail=0       UNL_EXIT=0
MORI_COMMIT_RUNWAY_SELFTEST: PASS 31/31  RW_EXIT=0
MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)  CENS_EXIT=0
```

Baseline comparison, `round-53/evidence/selftests/` (`mori-pin-check.txt`, `mori-unlanded-check.txt`,
`mori-commit-runway-a2.txt`) and `corpus/lessons/`:

| instrument | baseline (r53 receipt / lesson) | entering tip | freeze tip | verdict |
|---|---|---|---|---|
| `mori-pin-check.py --selftest` | `PIN_CHECK_SELFTEST pass=125 fail=0` | 125 / 0 | 125 / 0 | unchanged |
| `mori-unlanded-check.py --selftest` | `UNLANDED_SELFTEST pass=17 fail=0` | 17 / 0 | 17 / 0 | unchanged |
| `mori-commit-runway.py --selftest` | `PASS 31/31` (`mori-commit-runway-a2.txt`) | 31 / 31 | 31 / 31 | unchanged |
| `mori-census.sh --selftest` | no r53 receipt; `corpus/lessons/round-29-verifier-spotcheck.md:170` records `PASS (134 cases)` | 134 / 134 | 134 / 134 | unchanged |

The older `round-53/evidence/selftests/mori-commit-runway.txt` showing `PASS 23/23` is the pre-attempt-2
revision (`2a4213bf`); the later `-a2` receipt (31/31) is the applicable baseline and matches.

**No new failure among the four named selftests.** The round-56 delta (`5b295eee..8be2717b`, 34 files,
`+2942 −0`) touches none of `tools/mori-pin-check.py`, `tools/mori-unlanded-check.py`,
`tools/mori-commit-runway.py`, `tools/mori-census.sh` (verified by `git diff --name-only`).

## 2. Wider sweep: every tool's `--selftest` at both tips

36 tools exist at both tips; two exist only at the freeze tip. Exit code and summary line compared:

```
$ python3 sweep.py            # runs each tools/*.{py,sh} --selftest at both tips
tools at both tips: 36
tools only at freeze tip: ['mori-driver-liveness.py', 'mori-vote-bind.py']

tool                                          enter   freeze   rc=  summary(freeze)
mori-census.sh                                    0        0  same  MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)
mori-commit-runway.py                             0        0  same  MORI_COMMIT_RUNWAY_SELFTEST: PASS 31/31
mori-disk-rate.py                                 0        0  same  MORI_DISK_RATE_SELFTEST pass=14 fail=0
mori-dispatch-ledger.py                           0        0  same  SELFTEST mori-dispatch-ledger PASS 14/14
mori-gate-registry.py                             0        0  same  GATE_REGISTRY_SELFTEST pass=15 fail=0
mori-index-clean.sh                               0        0  same  MORI_INDEX_CLEAN_SELFTEST pass=4 fail=0
mori-job-runway.py                                0        0  same  MORI_JOB_RUNWAY_SELFTEST: PASS 21/21
mori-journal-window.py                            0        0  same  {"cases":16,"failed":0,…}
mori-misroot-sweep.py                             0        0  same  {"arms": 12, "finding": "MORI_MISROOT_SELFTEST_OK", …}
mori-oom-killers.py                               0        0  same  MORI_OOM_KILLERS_SELFTEST: PASS 32/32
mori-pin-check.py                                 0        0  same  PIN_CHECK_SELFTEST pass=125 fail=0
mori-pressure.py                                  0        0  same  MORI_PRESSURE_SELFTEST: PASS 12/12
mori-retention-reconcile.py                       0        0  same  {"finding_id":"RECONCILE_SELFTEST_PASS","passed":4,…}
mori-round13-regressions.py                       0        0  same  SELFTEST: pass checks=33 cases=2
mori-round14-regressions.py                       0        0  same  SELFTEST: pass checks=20 …
mori-round15-regressions.py                       0        0  same  SELFTEST PASS selftest_root=<tmp>/mori-r15-selftest-<rand>
mori-round16-context-check.py                     0        0  same  {"arms": 15, …}
mori-round16-regressions.py                       0        0  same  SELFTEST ok: pin_rc0,green_rc0_verdict_ok,…
mori-round17-context-check.py                     0        0  same  {"arms": 31, …}
mori-round17-jj-regressions.py                    0        0  same  SELFTEST ok: guard_output_repo_root,…
mori-round17-seat-regressions.py                  0        0  same  SELFTEST ok: green_rc0_and_manifest,…
mori-round41-calibration.py                       0        0  same  MORI_R41_CALIBRATION_SELFTEST pass=10 fail=0
mori-routed-check.py                              0        0  same  ROUTED_CHECK_SELFTEST pass=20 fail=0
mori-routed-r24.py                                0        0  same  ROUTED_R24_SELFTEST pass=26 fail=0
mori-seat-terminal.py                             0        0  same  {"arms":49,"finding_id":"SELFTEST_OK","passed":49,…}
mori-silence-cases.sh                             0        0  same  MORI_SILENCE_CASES_SELFTEST pass=24 fail=0
mori-source-drift.py                              0        0  same  MORI_SOURCE_DRIFT_SELFTEST: PASS (6 cases)
mori-sources-appendonly.py                        0        0  same  MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0
mori-unlanded-check.py                            0        0  same  UNLANDED_SELFTEST pass=17 fail=0
mori-wave-settlement.py                           0        0  same  MORI_WAVE_SETTLEMENT_SELFTEST: PASS (23 cases, 23 passed, 0 failed)
mori-blind-check.sh                               0        0  same
mori-evidence-loss.py                             0        0  same
mori-content-review.py                            2        2  same  {"exit_code":2,"findings":[{"code":"CONTENT_REVIEW_SELFTEST_TMPDIR"}],…}
mori-freeze-order.py                              1        1  same  SELFTEST freeze-order FAIL 0/11
mori-retention-gate.py                            2        2  same  SELFTEST retention-gate FAIL 0/21
mori-round19-regressions.py                       2        2  same  R19_SELFTEST setup=explicit-lane-tmpdir-invalid
```

Every exit code is identical at both tips; the only textual difference flagged anywhere was the random
temp-dir name inside `mori-round15-regressions.py`'s summary line. The four non-zero rows are
environment gates, not round-56 regressions: each passes when `TMPDIR` is placed where that tool demands
it (see §3).

## 3. The four non-zero selftests are TMPDIR placement gates, identical at both tips

```
$ TMPDIR=$S/tmp python3 tools/mori-content-review.py --selftest
{"exit_code":2,"findings":[{"code":"CONTENT_REVIEW_SELFTEST_TMPDIR"}],"schema":"mori-content-review-result-v1","status":"could-not-evaluate"}
rc=2
$ TMPDIR=<clone>/.scratch/tmp python3 tools/mori-content-review.py --selftest        # TMPDIR inside the lane root
{"exit_code":0,"findings":[{"code":"CONTENT_REVIEW_SELFTEST_CLEAN"}],"schema":"mori-content-review-result-v1","status":"clean"}
rc=0

$ TMPDIR=$S/tmp python3 tools/mori-freeze-order.py --selftest
SELFTEST freeze-order FAIL 0/11
rc=1
$ TMPDIR=<clone>/.scratch/tmp python3 tools/mori-freeze-order.py --selftest          # TMPDIR inside the checkout
SELFTEST freeze-order PASS 12/12
rc=0

$ TMPDIR=$S/tmp python3 tools/mori-round19-regressions.py --selftest
R19_SELFTEST setup=explicit-lane-tmpdir-required
rc=2
$ TMPDIR=<clone>/.scratch/tmp python3 tools/mori-round19-regressions.py --selftest
R19_SELFTEST pass=26 fail=0
rc=0

$ TMPDIR=$S/tmp python3 tools/mori-retention-gate.py --selftest
SELFTEST retention-gate FAIL 0/21
rc=2
$ TMPDIR=<clone>/.scratch python3 tools/mori-retention-gate.py --selftest            # exactly <repo>/.scratch
SELFTEST retention-gate PASS 21/21
rc=0
```

So all four are green under their documented `TMPDIR` contract and red only under a foreign `TMPDIR` —
the same at the entering tip and at the freeze tip. Not round-56 harm.

## 4. HIGH — the round-56 tools break the lane's standing registry gate

`tools/mori-gate-registry.py --audit-all` and `.ufo/waves/round-45/count-c2.py` (both registered gates in
`SKILL.md`'s `## Gates` table, lines 184 and 191) declare a population of `tools/*.py` + `tools/*.sh`
plus `.ufo/waves/round-4[45]/count-c*.py`. The round-56 data commits added two files under `tools/` and
touched no registry row, so the population gained two unregistered members:

```
$ cd <clone at 5b295eee> && python3 tools/mori-gate-registry.py --rev 5b295eee… --repo . --audit-all
… audit tools/mori-wave-settlement.py          PASS row='wave settlement (r20)' (8 cells, entry resolves, --selftest argv branch)
tables=13
mode=population
population_digest=7ff3079e467e943847759ca7fd757929ecb8e653b899fcbacae4b409d6a0b933
registered=42 unregistered=0 no_selftest=0 duplicate=0 wrong_row=0 tables=13
REGISTRY=met
ENTER_RC=0

$ cd <clone at 8be2717b> && python3 tools/mori-gate-registry.py --rev 8be2717b… --repo . --audit-all
audit tools/mori-driver-liveness.py            FAIL (no row names tools/mori-driver-liveness.py)
audit tools/mori-vote-bind.py                  FAIL (no row names tools/mori-vote-bind.py)
tables=13
mode=population
population_digest=0a51eace1f6a717c72bb71d1673f4ee7644fb17c4aefe8a4ff23e8d044eed325
registered=42 unregistered=2 no_selftest=0 duplicate=0 wrong_row=0 tables=13
REGISTRY=unmet
FREEZE_RC=1
```

The same regression propagates into the registered round-45 conformance gate:

```
$ python3 .ufo/waves/round-45/count-c2.py 5b295eee…
C2=met tables=13 registered=42 unregistered=0 no_selftest=0 duplicate=0 wrong_row=0 writescope_mismatch=0
   mode=population population_digest=7ff3079e… population_members=42 auditor_selftest=pass=15/fail=0 mutant=killed rev=5b295eee… 
rc=0

$ python3 .ufo/waves/round-45/count-c2.py 8be2717b…
check mutant_kill          PASS (count-c2.py pass=13 fail=1)
C2=unmet tables=13 registered=42 unregistered=2 no_selftest=0 duplicate=0 wrong_row=0 writescope_mismatch=0
   mode=population population_digest=0a51eace… population_members=44 auditor_selftest=pass=15/fail=0 mutant=killed
   checks_failed=unregistered,auditor_rc rev=8be2717b…
rc=1
```

History (same command, prior tips) shows the lane was clean before this round:

```
$ python3 tools/mori-gate-registry.py --rev <R> --repo . --audit-all
R=121093e2  registered=42 unregistered=0 … REGISTRY=met
R=f111d4b0  registered=42 unregistered=0 … REGISTRY=met
R=7b90a3c6  registered=42 unregistered=0 … REGISTRY=met
R=2a4213bf  registered=42 unregistered=0 … REGISTRY=met
```

`2a4213bf` is round 53's data commit, which landed `tools/mori-commit-runway.py` **together with** a
`## Round53` registry row — the lane's established pattern that round 56 did not follow.
`git diff --name-only 5b295eee..8be2717b` lists 34 paths and no `SKILL.md`, `SCORECARD.md`, `SHONEN.md`,
`LOG.md`, `PROVINCE.md` or `corpus/QUALITY.md`/`README.md`.

### Verified remedy (data/registry only — no counter, predicate, control or kill rule changes)

Two eight-cell rows in `SKILL.md`'s `## Gates` table, each whose `entry` cell's first backticked command
names the tool, restore both gates. Tested in a scratch copy only (`$S/fix-test`, scratch commit
`d4bc7c85467458c137d907f8e45eced1c9f3b805`) — the lane was not touched:

```
$ python3 tools/mori-gate-registry.py --rev d4bc7c85… --repo . --audit-all
registered=44 unregistered=0 no_selftest=0 duplicate=0 wrong_row=0 tables=13
REGISTRY=met
rc=0

$ python3 .ufo/waves/round-45/count-c2.py d4bc7c85…
C2=met tables=13 registered=44 unregistered=0 no_selftest=0 duplicate=0 wrong_row=0 writescope_mismatch=0
   mode=population population_digest=0a51eace… population_members=44 auditor_selftest=pass=15/fail=0 mutant=killed
rc=0

$ python3 tools/mori-pin-check.py --rev d4bc7c85… --repo .
PIN_CHECK=met tally_pins=39 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0
   hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=d4bc7c85… baseline=no env=0 stale=0
rc=0
```

The pin-check delta (`tally_pins` 37 → 39) is the two new rows' `self-test` cells: both were measured and
matched, so registering the tools does not disturb the pin set. Re-pin exposure is therefore limited to
the new rows' own cells; no existing pin moved.

## 5. The round-56 counters and the two new tools, re-measured at the freeze tip

```
$ python3 .ufo/waves/round-56/count-c1.py 8be2717b…
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=8be2717b…
rc=0
$ python3 .ufo/waves/round-56/count-c2.py 8be2717b…
C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=8be2717b…
rc=0
$ python3 tools/mori-driver-liveness.py --selftest
DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0        rc=0
$ python3 tools/mori-vote-bind.py --selftest
VOTE_BIND_SELFTEST pass=16 fail=0                       rc=0
$ ls .ufo/waves/round-56/fixtures/driver/ | wc -l
9
$ python3 tools/mori-vote-bind.py tally --ledger corpus/knowledge/kernel-v7.3-recheck-r55.md \
    --results .ufo/waves/round-55/w1-results.json --verb RECHECK \
    --voter Mo55Rc01 … --voter Mo55Rc16
TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15
rc=0
```

Freeze pins all verify against the working bytes:

```
088761f3…  contract.md           c4e58eed…  count-c1.py
4b350c77…  count-c2.py           5bf65ac0…  controls/controls.py
6b3dba74…  tools/mori-driver-liveness.py@8be2717b   (git show | sha256sum)
8be1acdb…  tools/mori-vote-bind.py@8be2717b         (git show | sha256sum)
```

Controls reproduce byte-for-byte from the committed runner:

```
$ python3 .ufo/waves/round-56/controls/controls.py 5b295eee… --repo .
do-nothing-c1                PASS C1=unmet selftest=bad fixtures=bad entry=bad row=bad norem=bad failed=tool_absent rev=5b295eee…
do-nothing-c2                PASS C2=unmet selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=5b295eee…
mut:fence-toggle-dropped     KILLED arm=t_fenced_text_ignored
mut:substring-scalar-binding KILLED arm=t_json_prose_substring_rejected
mut:hash-length-opened       KILLED arm=t_hash_len_drift_rejected
mut:first-wins               KILLED arm=t_last_wins_text
mut:text-channel-closed      KILLED arm=t_plain_binds
mut:json-channel-closed      KILLED arm=t_json_array_binds
mut:roster-filter-dropped    KILLED arm=t_roster_and_name_filter
mut:entail-verb-dropped      KILLED arm=t_entailed_verb_parsed
rc=0
```

## 6. Live-mode standing gates at both tips

```
tool                        enter  freeze   summary (freeze)
mori-pin-check.py (--rev)     0      0      PIN_CHECK=met tally_pins=37 digest_pins=8 mismatches=0 … stale=0
mori-index-clean.sh           0      0      MORI_INDEX_CLEAN staged=0 intent_to_add=0
mori-census.sh                1      1      MORI_CENSUS: DRIFT (findings=35 drift=14 unavailable=1 surfaces=8)
mori-source-drift.py          1      1      MORI_SOURCE_DRIFT rows=318 fresh=54 drifted=21 unavailable=1 no-copy=242
mori-sources-appendonly.py    1      1      appendonly_violations=50 ids=[S041,…,S543] deleted=[] superseded=[…] round_changed=[]
```

Entering-tip equivalents: `PIN_CHECK=met tally_pins=37 digest_pins=8 … rev=5b295eee` (identical counters),
`MORI_SOURCE_DRIFT rows=316 fresh=54 drifted=21 unavailable=1 no-copy=240`,
`appendonly_violations=50` with the identical id set. The census script bytes are unchanged by round-56;
its `DRIFT` findings are host-state classes (`WATCHDOG_STATE_LAG` ×15, `WAVE_UNSETTLED_AGE` ×8,
`OOM_KILL_JOURNAL`, `KILL_SIGNAL_JOURNAL`, `LANE_SILENT`, `ROSTER_SET_MISMATCH`), and no round-56 wave
appears in `WAVE_UNSETTLED_AGE` (the census scans the fleet root's `.ufo/waves`, not the lane's).

## 7. Census receipts (routed defect 1 from round 55)

```
$ grep -c rows .ufo/waves/round-56/evidence/census-start.txt
0
$ tail -3 .ufo/waves/round-56/evidence/census-start.txt | cat -A
mori^IW04^IS492 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst across scopes$
mori^Iok^I/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md$
exit=0$
$ bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori > fresh.txt  # rc=0
$ diff <(grep -v '^exit=' .ufo/waves/round-56/evidence/census-start.txt) fresh.txt
(no output — BYTES_IDENTICAL)
$ bash scripts/sources-census.sh census --file <entering-tip SOURCES.md>
file	rows	316
$ bash scripts/sources-census.sh census --file <freeze-tip SOURCES.md>
file	rows	318
$ awk -F'|' '/^\| S54[45] /{print NF}' corpus/SOURCES.md
13
13
```

The start receipt is a faithful capture of the `validate` command (byte-identical to a fresh run, `exit=0`
appended, 23 `W04` lines) — but the `validate` mode never prints a row count, so the contract's
`316 rows` figure is not in the receipt's bytes and no counting command is recorded with it. The row
count moved 316 → 318 with S544/S545, which is exactly the two new rows and no new `W04`. No
`census-end.txt` exists in `round-56/evidence/` yet (the contract's "End census must exit 0" is a closure
item for the L1).

## 8. Findings

- **F1 (HIGH)** — `SKILL.md` `## Gates` table (`SKILL.md:156` onward; the two missing rows) and
  `tools/mori-driver-liveness.py`, `tools/mori-vote-bind.py`. The round-56 data commits
  (`c419fe6d`, `6ced9da9`) landed two tools under `tools/` with no registry row, so the lane's standing
  population gate `tools/mori-gate-registry.py --audit-all` regresses `REGISTRY=met` (exit 0, at
  `5b295eee`) → `REGISTRY=unmet`, `registered=42 unregistered=2` (exit 1, at `8be2717b`), and the
  registered round-45 conformance gate `.ufo/waves/round-45/count-c2.py` regresses `C2=met` (exit 0) →
  `C2=unmet`, `checks_failed=unregistered,auditor_rc`, `population_members=42→44` (exit 1). Every prior
  tip checked (`121093e2`, `f111d4b0`, `7b90a3c6`, `2a4213bf`) is `unregistered=0 REGISTRY=met`.
  Smallest safe correction, verified in scratch (`d4bc7c85`): add two eight-cell `## Gates` rows naming
  the two tools → `REGISTRY=met` rc 0, `C2=met` rc 0, `PIN_CHECK=met` rc 0 (`tally_pins` 37→39, both new
  pins matched). This is a registry/data correction, not a change to any frozen counter, predicate,
  control or kill rule.

- **MED** — `.ufo/waves/round-56/count-c2.py:69,156-166` and its receipt line in
  `.ufo/waves/round-56/evidence/controls.txt`. The do-nothing control prints six arms as `ok` when the
  tool is absent: `C2=unmet selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok
  failed=tool_absent`. `evaluate()` returns `["tool_absent"]` before any arm runs (`count-c2.py:69`), and
  `main()` prints `"bad"` only for arms named in `failed`, so the receipt reads as if six arms passed at
  the entering tip. Reproduced from committed bytes with
  `controls.py 5b295eee… --repo .` (rc 0). `count-c1.py:188-191` handles the same state honestly (all
  arms `bad`), so the asymmetry is C2-only. Counter bytes are frozen: named limit plus a round-57 routed
  item (either special-case `tool_absent`, or print `unmeasured`).

- **MED** — `.ufo/waves/round-56/evidence/census-start.txt` vs `contract.md` §"Frontier and routed
  defects" (routed defect 1 / QUALITY 152). The contract states the start census receipt carries
  "exit 0, 316 rows, 23 W04"; the receipt's bytes carry `exit=0` and the 23 `W04` lines but no row count
  at all (`grep -c rows` → 0) and no counting command, so the `316 rows` figure is a retyped summary.
  The figure itself is true (entering-tip `census` mode: `file rows 316`; freeze tip: `318`) and the
  receipt is byte-identical to a fresh `validate` run, so the loss is the row-count evidence, not the
  receipt's honesty. Round-57 routed item; no frozen byte is wrong.

- **LOW** — `.ufo/waves/round-56/evidence/c1-at-freeze.txt` and `c2-at-freeze.txt` both stamp
  `rev=3f494b49cde6…`, while the wave's declared freeze tip is `8be2717b…` (the receipts live in the
  later commit). `count-c1.py` and `count-c2.py` bytes are identical at `3f494b49` and `8be2717b`
  (`diff` empty), and I re-ran both counters at `8be2717b` → `C1=met` rc 0, `C2=met` rc 0, so the
  verdicts still hold at the tip; the stamp is one commit stale.

- **LOW** — `tools/mori-freeze-order.py:500-513,666` — the failure path prints `FAIL 0/11` while the pass
  path prints `PASS 12/12` for the same 12-arm selftest. Cosmetic count mismatch in one tool's two
  summary strings; pre-existing and identical at both tips.

- **LOW** — `corpus/knowledge/driver-liveness-r56.md` and `corpus/knowledge/vote-binding-r56.md` have no
  `corpus/README.md` map row, while `kernel-v7.3-recheck-r53/r54/r55.md`, `disk-runway-enospc-r55.md` and
  `memory-failure-kills-r54.md` each have 1–2. Pre-existing exceptions exist (`c1s-cwd-r43.md`,
  `conform-scope-r40.md`, `conform-source-order-r42.md`, `inheritance-d72ac16-r42.md`,
  `s235-sha-correction-r43.md`), so this is a convention gap, not a gate.

## 9. Limits and scratch hygiene

- Vote-shape self-check: the lane's own binder finds zero vote lines in this report —
  `python3 tools/mori-vote-bind.py extract --verb RECHECK .ufo/waves/round-56/w1/Mo56ExecGateSelftests.md`
  and the same with `--verb ENTAIL` both produce 0 bytes of output (rc 0). Every command line, verb name
  and tally line quoted above sits inside a fenced block or mid-sentence, never at line start with a vote
  verb.

- UNVERIFIED: I did not evaluate the *content* correctness of the two new tools or their entries against
  their sources (other seats own that); this seat measured instrument behaviour only.
- The 36-tool sweep and the live-mode sweep ran inside scratch clones; live-mode coverage is partial
  (five tools ran in live mode at both tips; the rest need invocation arguments and were exercised only
  through `--selftest`).
- Scratch deviation, disclosed: the assignment allows one clone per seat; I used four copies under my own
  scratch dir (`clone` at the freeze tip, `clone-enter` at the entering tip, `clone-tmp` for the
  `TMPDIR`-placement arms, `fix-test` for the registry-row remedy test). All four are inside
  `/fast/scratch/hyaku/mori-r56/Mo56ExecGateSelftests/` and were removed before yield; nothing under
  `/tmp` was used as evidence, and no fleet or lane git/jj state was mutated (all git calls were
  `archive`, `show`, `rev-parse`, `diff`, `log`, `ls-tree`; the one commit made was inside my own scratch
  copy `fix-test`, with the git identity `probe`).
- No pacman transaction was run; no tool was installed or upgraded.
