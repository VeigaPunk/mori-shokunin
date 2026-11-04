# Mo82C01Contract — frozen-contract falsification

CONTRACT_CRITIC: defect 7

This is a critic finding, not admission, an axis score, or canonical judgment. Reviewed authority: freeze `20551e564da8bbb941c6a2ace7405192ceb74969`; entering revision is its actual parent `ebcf2c72df203c855cfafb5223c6e22b1e12c481`. Initial lane HEAD was `08e13729`. Working-tree repairs/amendment are distinguished below; they do not retroactively change these frozen-counter results.

## Axes

Operability 7; freshness 5; depth 5; coverage 6; calibration 5; adjacency 6. C1/C2/C3 select distinct axes: operability/freshness/depth. Freshness and depth both meet the tied-lowest non-retired requirement (calibration is also 5). No scalar improvement or canonical harm verdict is asserted. False-green detectors threaten calibration and operability; pins provenance/population gaps threaten depth. Removing a historical baseline or accepting r20 would threaten freshness, but the stated retirement need do neither.

## One verdict per assigned item

1. **Do-nothing reachability — defect.** At the entering revision the retained controls are red for all three; I independently reproduced C2's frozen control (`tokens=64 classified=0 agreed=0 retired=0 cell=0`). However, the real frozen C1 counter accepts a candidate revision containing only a print-stub instead of a mutation harness (D1). A hardcoded killed tally also passes its detector selftest (D3). All-added C2 classification fails: measured split is 45 added-since-r10 / 19 value-changed; the cheat gets agreed=45 of 64. A single revision binding alone fails C3 (bindings=1), but duplicating it three times or adding two legacy command bindings passes the B>=3 check (D5). Pasting only REVISION_MISMATCH into the entering tool does not pass: its unchanged selftest prints pass=26, below 30. An arm-less counterfeit that also fabricates the expected tally/fixture output does pass (D6).
2. **Over-broad arms — defect.** A partially unanchored C1 population still returns met in the frozen grade (D2); the all-added classifier does not collapse the actual 64-token C2 population; C3's defeated bit accepts a tool that never reads any revision (D6).
3. **Claim sizing / non-author re-derivation — defect.** Each counter has a single-command interface and a finite population, not an exhaustive correctness proof. C1's exact target is already met at the freeze commit itself: `C1=met harness=present killed=11 survivors=0 total=11 pristine=green`, rc 0. This is genuine pre-wave capability acquisition by the freeze commit, NOT evidence of post-dispatch work; an unchanged entering round still lacks that commit. C2's live census depends on current fleet/host state even with committed instrument bytes: the command is reproducible, the historical live reading is not immutable. C3 has floors N>=30 and B>=3 rather than exact N/B, and its answer changes when only uncommitted pins change (D4). Finite universal clauses (all anchored mutants, all live tokens/no stale classifications, every registered binding) are enumerable; none licenses universal forgery resistance or completeness of all record rows.
4. **Axis assignment — pass on assignment only.** The three chosen axes are distinct and two are tied lowest. The above detector/provenance problems are potential harms, not permission to invent scores or accept a tradeoff.
5. **C2 honesty versus round 21 — pass as a narrow retirement, not acceptance.** The frozen contract says: “The r20 re-pin was rejected (SCORECARD round-21 correction: the closed-class register licensed away retained evidence loss)” and “the pin therefore cannot go green by re-pinning.” Its vacuity guard requires “The live census run is the same command in both states and must stay **red (exit 1)**.” In contrast, corpus/README.md:415-423 says “The r20 baseline remains byte-unchanged but invalid for acceptance” and the two aggregator identities remain unresolved. Retiring r10 as an acceptance predicate without re-pinning or settling those identities does not contradict that correction. The current SCORECARD.md:60 additionally says: “Round-21's retained-evidence-loss blocker is untouched: no lifecycle closure, no disposition and no baseline acceptance is asserted here.” That last sentence is working-tree prose, not in the original frozen contract. Classification agreement is not evidence-loss clearance. The frozen C2 counter loads baseline bytes at R; it does not enforce their identity against the historical baseline hash, so byte-unchanged remains a separately checked preservation obligation.

## Defects and smallest correction sentences

### D1 — C1 checks candidate harness presence, not candidate harness capability

**Counterexample:** in a scratch clone, commit a candidate count-c1.py consisting solely of `print('C1=met harness=present killed=11 survivors=0 total=11 pristine=green')`. Invoke the REAL frozen counter on that revision. It still kills the old r80/r81 mutants itself and prints exact target, rc 0. The candidate contains no reusable harness whatsoever. Scratch candidate revision: `292969fb3a65`.

**Evidence:** freeze `.ufo/waves/round-82/count-c1.py` main's `loader('.ufo/waves/round-82/count-c1.py') is None` check only tests existence, then calls the running copy's grade. Full output is retained below. Merely running the candidate's own selftest would not make arbitrary output honest.

**Axes:** operability, calibration. **Status:** fixable provenance/capability-validation defect. The currently observed worktree repair still executes the running file's selftest, not the candidate blob's behavior; no repaired D1 pass is claimed.

**Exact sentence to freeze:** “harness=present is insufficient: export the candidate harness at R and independently require that candidate to grade both a sensitive and a blind fixture with exact expected counts, while preserving and naming the authoritative evaluator blob.”

### D2 — a missing anchor does not veto frozen C1 met

**Counterexample:** call the real frozen grade with two synthetic mutations of one green fixture: one GUARD mutation is killed, the other old anchor does not exist. It returns `met=True`, `killed=1 survivors=0 total=1 pristine=green`, plus `unanchored ... occurrences=0`. This contradicts the frozen kill rule that ANY unanchored mutant is unmet. Losing every anchor does fail total>0; losing only some is the hole.

**Evidence:** freeze count-c1.py grade met conjunction checks empty-mutation, not unanchored. The exact fixture and outputs are below. The full 11/11 receipt is a backstop against a reduced denominator, but does not repair an inconsistent met verdict.

**Axes:** operability, calibration. **Status:** implementation defect; repaired behavior measured in the current, uncommitted working-tree version: the same probe returns met=False. Its SHA-256 is retained below. I did not edit this repair.

**Exact sentence to freeze:** “The counter returns unmet whenever any frozen mutant anchor occurs other than exactly once, including mixed anchored/unanchored populations, and a detector-selftest failure also vetoes met.”

### D3 — hardcoded killed=11 survives the detector's own tests

**Counterexample:** replace only `killed_n = total - survivors` with `killed_n = 11` in a scratch copy of the frozen evaluator, then run its real selfcheck. It reports `C1_COUNTER_SELFTEST pass=4 fail=0`, rc 0. The sensitive fixture falsely prints killed=11 with total=1.

**Evidence:** frozen selfcheck sensitive case searches substring `killed=1`, which matches `killed=11`; other arms do not require exact killed counts. The blind case retains survivors=1 and stays unmet, so this is a metric-integrity hole, not a claim that blind_survives is absent.

**Axes:** calibration, operability. **Status:** fixable detector defect; no repaired check was exercised.

**Exact sentence to freeze:** “Detector fixtures parse exact integer fields, assert K+survivors=T, and require sensitive K=1/T=1 and blind K=0/T=1; a hardcoded K=11 counter must fail the detector.”

### D4 — C3 reads uncommitted pins after inspecting committed pins

**Counterexample:** at one scratch revision `7b51eb1a299e`, the original three A1 bindings yield met. Without committing any new revision, change only worktree record-pins.json to one binding: the same revision yields unmet/bindings=1. Triplicate only that first binding in the worktree: same revision yields met/bindings=3 again. All carrier bytes remain unchanged.

**Evidence:** freeze count-c3.py:183-207 parses `show(PINS)` and guards carrier bytes against R, but the actual child gets `--pins os.path.join(repo, PINS)`. It never compares or exports the worktree pins themselves. This makes the after-state not a function of committed bytes at R.

**Axes:** depth, calibration, operability. **Status:** fixable implementation/provenance defect.

**Exact sentence to freeze:** “The real-lane sweep consumes an exported byte-for-byte copy of R:record-pins.json; no uncommitted pins may affect the result for R.”

### D5 — total bindings is not the frozen three-revision population

**Counterexample:** triplicating one conformant revision binding passes as bindings=3. One conformant revision binding plus two legacy pinned-command bindings also passes as bindings=3; neither grades the other two required revision bindings. The first mixed probe failed because its chosen `wrong` row contained the earlier wrong=7 before wrong=0; the corrected probe uses row_tally=19 for both legacy bindings and passes. Both attempts are retained, not selectively omitted.

**Evidence:** freeze count-c3.py:188-213 requires a nonempty revisions list but takes `bindings` from the tool's summary; the current tool documents/counts both binding lists. The evaluator never enforces distinct identities or equality with the frozen population.

**Axes:** depth, coverage, calibration. **Status:** fixable population-check defect.

**Exact sentence to freeze:** “B counts distinct revision bindings only, and the normalized revision-binding list must equal the authoritative three-row population exactly; duplicate or legacy command bindings cannot satisfy its floor.”

### D6 — ‘independent fixture’ does not independently establish revision detection

**Counterexample:** a 12-line counterfeit tool never invokes git or reads any revision; it prints pass=30 on --selftest, otherwise prints revisions=1 and REVISION_MISMATCH iff the pins list length is one, and revisions=0 otherwise. The actual frozen C3 counter accepts it: `C3=met tool=present arms=30 defeated=1 bindings=3 revisions=0`, rc 0, scratch revision `2441e63695c3`.

**Evidence:** count-c3.py:175-182 trusts candidate selftest output and a single candidate-generated fixture summary, then :206-213 trusts candidate-generated real summary. The independent fixture INPUT is indeed separately built, but the OUTPUT is from the code being evaluated. The pasted-marker-only attempt failed; this stronger counterexample succeeds.

**Axes:** depth, calibration. **Status:** the one-binding-versus-three-binding shortcut is a fixable finite-test gap; arbitrary self-reporting forgery is a residual tradeoff the canonical judge must evaluate, not a universal safety guarantee that I can admit. A detector is not correct merely because its own output says it is.

**Exact sentence to freeze:** “The independent battery includes matched conformant and stale one-binding fixtures plus a two-binding stale-second fixture with independently checked expected results; defeated=1 and a self-reported tally establish only those finite cases, never authenticity or general correctness of the candidate.”

### D7 — A1 has two incompatible population-replacement readings

**Counterexample/evidence:** current contract.md:185 says “The ‘Real bindings’ table's first row is replaced.” Yet :194-198 supplies THREE new rows (row_tally/survivors/wrong), replacing none of the old pass=26/pass=19 rows. If only the first row is replaced, the other two original rows remain authoritative; if the new whole table replaces the whole population, all three identities change. The original table at :153-158 remains in the file. I verified A1's three row selectors each match one frozen table row and each value exists at the named revision; those measurements do not settle the authority conflict or establish when an uncommitted amendment was authorized.

**Axes:** depth, calibration. **Status:** fixable duplicate-authority prose defect in another seat/L1's working-tree bytes. A1 is explicitly disclosed as pre-data; I cannot independently establish the ‘before any after-value’ timing claim from committed amendment history because it was uncommitted when read. I did not edit or approve it.

**Exact sentence to freeze:** “Amendment A1 supersedes the ENTIRE original three-row Real bindings table; the sole effective population is exactly the three rows in A1, and the original table remains historical only.”

## Commands, fixtures, and provenance

All writes were confined to my named report or my own scratch root. No lane/fleet/sibling git mutation, host/unit/service/credential/orchestration change, tool installation, subagent dispatch, or other runtime invocation occurred. After an initial no-git-anywhere blocker, L1 MoriR82 explicitly authorized fixture-only Git under scratch; my direct fixture mutations asserted the fixture toplevel and used a fixture-only identity. The C3 library probe wrapped its child git add/commit calls with toplevel/scratch assertions; frozen C1 nested selftests ran as inherited. No PATH directory was changed.

Source reads: frozen contract, controls, relevant SCORECARD sections/capabilities, SKILL registry, PROVINCE inventory, QUALITY tail, README frontier and Round21 correction, and r81 lesson/spotcheck D81-1..D81-6. Commands included read-only git log/show/rev-parse/status/diff; freeze stat showed five files, 1038 additions. `git rev-parse 20551e56^` printed the entering revision above.

Main full C1 command (frozen source exported verbatim):

```
python3 -I /fast/scratch/hyaku/mori-r82/Mo82C01Contract/frozen-c1.py 20551e56 --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch /fast/scratch/hyaku/mori-r82/Mo82C01Contract
```

The stub-candidate command is identical except revision `292969fb3a65...` and --repo points to the own scratch shared clone; its full argv is in the raw appendix. Candidate fixture setup used `git clone --shared --quiet <lane> <scratch>/clone-vrykhz0p/repo`, `git -C <fixture> rev-parse --show-toplevel`, path-scoped `git -C <fixture> add -- <paths>`, and `git -C <fixture> -c user.name=contract-fixture -c user.email=fixture@invalid -c commit.gpgsign=false commit -qm <message>` only there. Paths committed: candidate tool and pins, or candidate count-c1.py. No existing repository was committed.

Library probes loaded the 20551e56 modules through `exec(compile(git_show_stdout, absolute_filename, 'exec'), module.__dict__)` (no lane pycache). Exact top-level calls:

```python
c1.grade(loader, scratch, [('tools/a.py','anchored','GUARD = 1','GUARD = 0'),
                          ('tools/a.py','missing','ABSENT = 1','ABSENT = 0')])
c1.selfcheck(scratch)
c2.grade(gitbytes, scratch, '/home/vgpnk/Projects/shokunin')
c2.derive(token, c2.baseline_names(gitbytes(c2.BASELINE)))  # each captured live token
c2.grade(all_added_overlay, scratch, '/home/vgpnk/Projects/shokunin')
c3.main([scratch_revision, '--repo', scratch_clone, '--scratch', own_scratch])
c3.selftest_run(pasted_marker_tool_path, own_scratch)
hardcoded_c1.selfcheck(scratch)
fixed_worktree_c1.grade(loader, scratch, same_mutants)
```

For D2's loader every path returns this green/sensitive fixture:

```python
import sys
GUARD = 1
ok = GUARD == 1
print('FAKE pass=%d fail=%d' % (1 if ok else 0, 0 if ok else 1))
sys.exit(0 if ok else 1)
```

For C2 the frozen grade launched `bash <scratch>/tools/mori-census.sh --drift <scratch>/corpus/evidence/baseline-r10-20261015T2231Z.json`, cwd=<scratch>, MORI_SHOKUNIN_ROOT=/home/vgpnk/Projects/shokunin, with frozen script and baseline. The one live child result (rc 1) was retained IN MEMORY and replayed for all-added classification grading, isolating classification logic from live churn. That overlay supplies `DRIFT_CLASS <each captured token> added-since-r10`, a syntactically valid retired row and retired freshness cell; all other bytes are frozen. This is a real frozen grade-function result over a measured live receipt, not a claim that a synthetic overlay was committed in the lane.

For C3 the baseline scratch commit contains the worktree tool snapshot SHA below and the three A1 binding objects. Each main invocation really runs the tool selftest and independent scratch-repo fixture. Only pins change in the three worktree attacks; the baseline committed revision and carrier bytes remain the same. The counterfeit tool used in D6 is reproduced below. Frozen count-c3.py's fixture-input construction was not changed; the wrapper added only scratch/toplevel safety assertions before mutations.

The negative marker-only attempt ran the entering revision's tool text plus `# REVISION_MISMATCH`, using the real c3.selftest_run function. Full inherited output, including pass=26, is retained.

## Limits / unverified

- These are falsification experiments, not final-tip acceptance, admission or no-harm verification. No final-tip C1/C2/C3 reading is claimed.
- Full frozen C1 at 20551e56 and its stub-candidate counterexample were exercised; frozen C2 real census/grade and classification overlay were exercised; frozen C3 was exercised on scratch candidate revisions. C3 has NOT been accepted over the landed lane.
- Only the repaired worktree C1 partial-unanchored behavior was remeasured; other fixes are not assumed landed or green. Worktree input hashes below identify those observations, not committed revisions.
- A1 row/value assertions were independently checked with read-only git, not its chronology or authorization. Old historical record tokens are byte-presence evidence only, not provenance that a command actually produced a count.
- All fixture revisions and source snapshots under scratch were deleted before yielding. The report retains measurements, argv, generator snippets and source identities; scratch hashes are not durable lane commits or evidence URLs.

## Raw measured output

```json
{
  "c1_unanchored": {
    "met": true,
    "tail": "harness=present killed=1 survivors=0 total=1 pristine=green",
    "lines": [
      "MUTANT a.py anchored killed rc=1"
    ],
    "extras": [
      "unanchored tools/a.py missing occurrences=0"
    ]
  },
  "c1_selfcheck": {
    "rc": 0,
    "stdout": "PASS sensitive_killed harness=present killed=1 survivors=0 total=1 pristine=green | MUTANT sensitive.py trip_guard killed rc=1\nPASS blind_survives harness=present killed=0 survivors=1 total=1 pristine=green\nPASS duplicate_anchor_excluded harness=present killed=0 survivors=0 total=0 pristine=green\nPASS red_pristine_reported harness=present killed=0 survivors=0 total=0 pristine=red\nC1_COUNTER_SELFTEST pass=4 fail=0\n"
  },
  "c2_freeze": {
    "met": false,
    "tail": "tokens=64 classified=0 agreed=0 residual=0 stale=0 retired=0 cell=0",
    "notes": [
      "unclassified +FINDING:CGROUP_OOM_KILL_CUMULATIVE",
      "unclassified +FINDING:COREDUMP_NOTICE_JOURNAL_USER",
      "unclassified +FINDING:JOURNAL_CLASSES_UNMEASURED",
      "unclassified +FINDING:OOM_KILL_JOURNAL",
      "unclassified +FINDING:ROSTER_SET_MISMATCH",
      "unclassified +FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER"
    ]
  },
  "c2_split": {
    "census_rc": 1,
    "tokens": [
      "+FINDING:CGROUP_OOM_KILL_CUMULATIVE",
      "+FINDING:COREDUMP_NOTICE_JOURNAL_USER",
      "+FINDING:JOURNAL_CLASSES_UNMEASURED",
      "+FINDING:OOM_KILL_JOURNAL",
      "+FINDING:ROSTER_SET_MISMATCH",
      "+FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER",
      "+FINDING:UNIT_FAILURE_JOURNAL",
      "+FINDING:UNIT_FAILURE_OUT_OF_SCOPE",
      "+FINDING:WATCHDOG_STATE_LAG",
      "+SURFACE:journal.system",
      "+SURFACE:journal.user",
      "+SURFACE:lane.audio",
      "+SURFACE:lane.chousa",
      "+SURFACE:lane.game-dev-2d",
      "+SURFACE:lane.game-dev-3d",
      "+SURFACE:lane.kaidoku",
      "+SURFACE:lane.kotodama",
      "+SURFACE:lane.lore",
      "+SURFACE:lane.mado",
      "+SURFACE:lane.mori",
      "+SURFACE:lane.revenger",
      "+SURFACE:lane.souji",
      "+SURFACE:lane.tabi",
      "+SURFACE:lane.tameshi",
      "+SURFACE:lane.tsukuroi",
      "+alarm_basis",
      "+attribution",
      "+conf_dropped_n",
      "+conf_n",
      "+gate_s",
      "+note",
      "+paths",
      "+positive_basis",
      "+positive_validation",
      "+process_sigkill",
      "+raw_basis",
      "+reason",
      "+repo",
      "+roster_n",
      "+roster_source",
      "+state_dropped_n",
      "+state_n",
      "+trust",
      "+user_positive_process_sigkill",
      "+user_positive_unit_signal",
      "+user_unit_signal",
      "-FINDING:SEGFAULT_JOURNAL",
      "-FINDING:WATCHDOG_STALE",
      "-FINDING:WAVE_UNSETTLED_AGE",
      "-SURFACE:journal",
      "-attribution",
      "-example",
      "-rowb_files",
      "-subject_commits",
      "-window",
      "HEADER",
      "age_s",
      "basis",
      "boot",
      "io_avg_unavailable",
      "launch_epoch",
      "obs",
      "round",
      "volatile_fields"
    ],
    "classes": {
      "added-since-r10": 45,
      "value-changed": 19
    }
  },
  "c2_all_added": {
    "met": false,
    "tail": "tokens=64 classified=64 agreed=45 residual=0 stale=0 retired=1 cell=1",
    "notes": [
      "class-disagrees +attribution stated=added-since-r10 derived=value-changed",
      "class-disagrees -FINDING:SEGFAULT_JOURNAL stated=added-since-r10 derived=value-changed",
      "class-disagrees -FINDING:WATCHDOG_STALE stated=added-since-r10 derived=value-changed",
      "class-disagrees -FINDING:WAVE_UNSETTLED_AGE stated=added-since-r10 derived=value-changed",
      "class-disagrees -SURFACE:journal stated=added-since-r10 derived=value-changed",
      "class-disagrees -attribution stated=added-since-r10 derived=value-changed",
      "class-disagrees -example stated=added-since-r10 derived=value-changed",
      "class-disagrees -rowb_files stated=added-since-r10 derived=value-changed",
      "class-disagrees -subject_commits stated=added-since-r10 derived=value-changed",
      "class-disagrees -window stated=added-since-r10 derived=value-changed",
      "class-disagrees HEADER stated=added-since-r10 derived=value-changed",
      "class-disagrees age_s stated=added-since-r10 derived=value-changed",
      "class-disagrees basis stated=added-since-r10 derived=value-changed",
      "class-disagrees boot stated=added-since-r10 derived=value-changed",
      "class-disagrees io_avg_unavailable stated=added-since-r10 derived=value-changed",
      "class-disagrees launch_epoch stated=added-since-r10 derived=value-changed",
      "class-disagrees obs stated=added-since-r10 derived=value-changed",
      "class-disagrees round stated=added-since-r10 derived=value-changed",
      "class-disagrees volatile_fields stated=added-since-r10 derived=value-changed"
    ]
  },
  "c1_freeze_full": {
    "cmd": [
      "python3",
      "-I",
      "/fast/scratch/hyaku/mori-r82/Mo82C01Contract/frozen-c1.py",
      "20551e56",
      "--repo",
      "/home/vgpnk/Projects/shokunin/mori-shokunin",
      "--scratch",
      "/fast/scratch/hyaku/mori-r82/Mo82C01Contract"
    ],
    "rc": 0,
    "stdout": "MUTANT count-c1.py ignore_row_disagreement killed rc=1\nMUTANT count-c1.py ignore_mismatch_lines killed rc=1\nMUTANT count-c1.py ignore_stale_field killed rc=1\nMUTANT count-c1.py ignore_sweep_exit killed rc=1\nMUTANT count-c3.py ignore_missing killed rc=1\nMUTANT count-c3.py ignore_extra killed rc=1\nMUTANT count-c3.py drop_right_boundary killed rc=1\nMUTANT count-c2.py pending_all_sections killed rc=1\nMUTANT count-c2.py pending_substring killed rc=1\nMUTANT count-c2.py ignore_command_exit killed rc=1\nMUTANT count-c2.py first_binding_only killed rc=1\nC1=met harness=present killed=11 survivors=0 total=11 pristine=green rev=20551e564da8\n",
    "stderr": ""
  },
  "c3_attacks": {
    "baseline": {
      "rc": 0,
      "stdout": "C3=met tool=present arms=36 defeated=1 bindings=3 revisions=0 rev=7b51eb1a299e\n",
      "stderr": ""
    },
    "one_binding": {
      "rc": 1,
      "stdout": "C3=unmet tool=present arms=36 defeated=1 bindings=1 revisions=0 rev=7b51eb1a299e\n",
      "stderr": ""
    },
    "triplicated_first": {
      "rc": 0,
      "stdout": "C3=met tool=present arms=36 defeated=1 bindings=3 revisions=0 rev=7b51eb1a299e\n",
      "stderr": ""
    },
    "mixed_one_revision": {
      "rc": 1,
      "stdout": "C3=unmet tool=present arms=36 defeated=1 bindings=3 revisions=0 rev=7b51eb1a299e\nRECORD_SWEEP_MISMATCH pinned SCORECARD.md:4118 wrong stated=7 live=0 command_rc=0\n",
      "stderr": ""
    },
    "revision": "7b51eb1a299e51ecd11f90e8af6aa29934613716",
    "note": "Only scratch worktree pins change after the baseline commit; committed revision is identical for all four observations.",
    "mixed_one_revision_repaired_probe": {
      "rc": 0,
      "stdout": "C3=met tool=present arms=36 defeated=1 bindings=3 revisions=0 rev=7b51eb1a299e\n",
      "stderr": ""
    }
  },
  "c3_marker": {
    "rc": 0,
    "stdout": "case pending-in-round pass\ncase pending-outside-round pass\ncase pending-prose pass\ncase pending-trimmed pass\ncase pending-exact pass\ncase round-end pass\ncase round-subsection pass\ncase escaped-pipe pass\ncase first-stating-row pass\ncase missing-stated pass\ncase live-single pass\ncase live-repeated-agreement pass\ncase live-conflict pass\ncase live-absent pass\ncase malformed-json pass\ncase malformed-schema pass\ncase malformed-bindings pass\ncase valid-pins pass\ncase command-not-shell pass\ncase clean-totals pass\ncase dirty-totals pass\ncase tool-absent pass\ncase failed-command pass\ncase missing-live pass\ncase conflicting-live pass\ncase missing-stated-mismatch pass\nRECORD_SWEEP_SELFTEST pass=26 fail=0\n",
    "arms_below_30": true
  },
  "stub_counter": {
    "rc": 0,
    "stdout": "C1=met harness=present killed=11 survivors=0 total=11 pristine=green\n"
  },
  "c1_hardcoded": {
    "rc": 0,
    "stdout": "PASS sensitive_killed harness=present killed=11 survivors=0 total=1 pristine=green | MUTANT sensitive.py trip_guard killed rc=1\nPASS blind_survives harness=present killed=11 survivors=1 total=1 pristine=green\nPASS duplicate_anchor_excluded harness=present killed=11 survivors=0 total=0 pristine=green\nPASS red_pristine_reported harness=present killed=11 survivors=0 total=0 pristine=red\nC1_COUNTER_SELFTEST pass=4 fail=0\n"
  },
  "c1_fixed_unanchored": {
    "met": false,
    "tail": "harness=present killed=1 survivors=0 total=1 pristine=green",
    "extras": [
      "unanchored tools/a.py missing occurrences=0"
    ]
  },
  "a1_checks": [
    {
      "row_contains": "row_tally=19",
      "rows_at_freeze": 1,
      "rev": "075574c83eae",
      "token_in_rev": true
    },
    {
      "row_contains": "survivors=0",
      "rows_at_freeze": 1,
      "rev": "075574c83eae",
      "token_in_rev": true
    },
    {
      "row_contains": "wrong=0 fixtures=7",
      "rows_at_freeze": 1,
      "rev": "482dc48d",
      "token_in_rev": true
    }
  ],
  "c2_unknown_default": "added-since-r10",
  "snapshot_shas": {
    ".ufo/waves/round-82/count-c1.py": "84a85af80a13ee306dd64e25765717c14f8173662c62cba60079a360d47549cd",
    "tools/mori-record-sweep.py": "4b34f0040a22407b8f950e0e2c04126fafe669d32121d3ea2b5aded46c4e699f"
  },
  "c1_stub_real_counter": {
    "cmd": [
      "python3",
      "-I",
      "/fast/scratch/hyaku/mori-r82/Mo82C01Contract/frozen-c1.py",
      "292969fb3a655baa51023c1b47abb6f6a54ea56c",
      "--repo",
      "/fast/scratch/hyaku/mori-r82/Mo82C01Contract/clone-vrykhz0p/repo",
      "--scratch",
      "/fast/scratch/hyaku/mori-r82/Mo82C01Contract"
    ],
    "rc": 0,
    "stdout": "MUTANT count-c1.py ignore_row_disagreement killed rc=1\nMUTANT count-c1.py ignore_mismatch_lines killed rc=1\nMUTANT count-c1.py ignore_stale_field killed rc=1\nMUTANT count-c1.py ignore_sweep_exit killed rc=1\nMUTANT count-c3.py ignore_missing killed rc=1\nMUTANT count-c3.py ignore_extra killed rc=1\nMUTANT count-c3.py drop_right_boundary killed rc=1\nMUTANT count-c2.py pending_all_sections killed rc=1\nMUTANT count-c2.py pending_substring killed rc=1\nMUTANT count-c2.py ignore_command_exit killed rc=1\nMUTANT count-c2.py first_binding_only killed rc=1\nC1=met harness=present killed=11 survivors=0 total=11 pristine=green rev=292969fb3a65\n",
    "stderr": "",
    "rev": "292969fb3a655baa51023c1b47abb6f6a54ea56c"
  },
  "c3_counterfeit": {
    "rc": 0,
    "stdout": "C3=met tool=present arms=30 defeated=1 bindings=3 revisions=0 rev=2441e63695c3\n",
    "stderr": "",
    "rev": "2441e63695c3cdfe7d49c75b23cab960af4cc09b"
  }
}
```

## Counterfeit tool used for D6

```python
import sys,json
# REVISION_MISMATCH
if '--selftest' in sys.argv:
    print('RECORD_SWEEP_SELFTEST pass=30 fail=0'); sys.exit(0)
pins=json.load(open(sys.argv[sys.argv.index('--pins')+1]))
n=len(pins['revisions'])
bad=n==1
if bad: print('REVISION_MISMATCH SCORECARD.md:5 rev-bytes')
print('RECORD_SWEEP pending=0 pinned=0 carriers=1 bindings=%d revisions=%d' % (n,int(bad)))
sys.exit(int(bad))
```

## Review self-check

Accuracy 4/5: concrete outputs and source identities retained; final lane acceptance intentionally unrun. Completeness 4/5: all five assigned review items and cheapest cheats addressed; amendment timing not independently provable. Clarity 4/5: frozen/worktree/fixture results separated, at the cost of a long raw appendix. Actionability 4/5: exact correction sentence per defect, without unauthorized edits. Conciseness 4/5: raw outputs retained because deleted scratch cannot be cited as durable evidence. Highest-value corrections are committed-pins isolation, distinct revision-population enforcement, and independent candidate-harness fixtures. The user can distinguish measured failures from residual tradeoffs.
