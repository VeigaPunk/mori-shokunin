# Mo82M01Mutants — independent mutation test of the round-82 build

Seat: Mo82M01Mutants (mutation-tester, wave w1, round 82, attempt 1). Detection and report
only; every mutant lived in a scratch copy under `/fast/scratch/hyaku/mori-r82/Mo82M01Mutants`
(deleted before this report was committed). No lane file was edited by this seat except this
report. No subagents. No tools installed (none needed: python3, git, /bin/echo only).

**Headline: `MUTANTS killed=18 total=38 survivors=20`** (primary run, current worktree bytes).
Per-detector: counters' own `--selftest` killed 3/23 counter mutants; the record-sweep tool's
own `--selftest` killed 9/15 of its mutants and my 14-scenario pins fixture killed the other 6
(all 15 rs mutants died; 7 of the 15 were invisible to the tool's own selftest). The 20
survivors are all counter mutants: the counters grade their helpers, not themselves.

## Population and when bytes moved

Entering revision `ebcf2c72df203c855cfafb5223c6e22b1e12c481`; freeze commit `20551e56`.

- `tools/mori-record-sweep.py`: absent of `REVISION_MISMATCH` at first read (r81 bytes,
  225 lines); the **revision arm landed in the worktree during this probe** (343 lines,
  +131/−13 vs HEAD). Per seat spec I mutated the **landed bytes**: sha256
  `4b34f0040a22407b8f950e0e2c04126fafe669d32121d3ea2b5aded46c4e699f`, stable across two
  probes 25 s apart and unchanged from before-hash to after-hash.
- `count-c1/c2/c3.py`: I snapshotted and ran 19 mutants against the freeze bytes
  (`ba0646a3…`, `95a6b856…`, `af57ec5f…`, byte-identical to HEAD at snapshot time); **an
  executor seat then modified all three counters mid-probe**, so I re-derived anchors and
  re-ran 23 mutants against the **current bytes** (`84a85af8…`, `e73d919e…`, `65850d9a…`).
  Both runs are reported; the current-bytes run is primary. Verdicts bind to the hashed
  snapshots, not to later edits.

New graded behaviours that appeared mid-probe and were added to the mutant set: c1 met-gate
`own_ok` (counter re-runs its own selftest in main) and unanchored-extras blocking met; c2
`KEYSHAPE` fallback class and duplicate-line counting into residual/met; c3 `FROZEN`
population identity gate in main.

## Detector (frozen for this probe)

- Counters: `python3 -I <copy> --selftest --scratch <scratch/runs/...>`, cwd and `TMPDIR`
  under my scratch, `GIT_CONFIG_GLOBAL/SYSTEM=/dev/null`, `HYAKU_SCRATCH` under scratch,
  120 s bound per subprocess. Killed iff rc != 0 or `fail=<n>`, n>0. Pristine green first.
- record-sweep: (i) same selftest rule; (ii) a 14-scenario end-to-end pins fixture suite
  (conformant, value-drift, command-fails, missing-row, PENDING cell, carrier escaping root,
  conflicting live readings, missing executable, live boundary `pass=45x`, two bindings with
  the second drifted, combined binding+revision clean, D81-1 rev-bytes shape, separate
  `--git` repo with plain root, unresolvable rev). A mutant is killed if any scenario's
  rc/mismatch-arm-set/stdout deviates from the pristine run; the pristine run must satisfy
  hardcoded expectations first (it did, after I fixed two fixture-authoring bugs of my own —
  s11 worktree card missing the binding row, s12 pinned at the wrong commit; the tool was
  right both times; not kills). Fixture git repos were created only under my scratch; each
  asserted `git rev-parse --show-toplevel` == the fixture dir (host guard). No mutating git
  command touched any real repo.

## Pristine baselines (all green before any mutant was graded)

```text
freeze bytes:   c1 selftest rc=0 pass=4 fail=0 | c2 rc=0 pass=9 fail=0 | c3 rc=0 pass=5 fail=0
current bytes:  c1 selftest rc=0 pass=4 fail=0 | c2 rc=0 pass=9 fail=0 | c3 rc=0 pass=8 fail=0
record-sweep:   selftest rc=0 pass=36 fail=0  +  fixture suite green: 14 scenarios
```
(Freeze-byte counter tallies match `evidence/controls-r82.txt` exactly. c3 grew 5→8 arms
mid-probe: the three new `population_*` arms.)

## Mutant table — primary run (current worktree bytes)

`st` = mutated copy's own `--selftest` (rc, fail). Verdict combines selftest and (rs only)
fixture suite. old→new are literal anchored substrings (each occurred exactly once).

| file | label | old → new | st rc | caught by | verdict |
|---|---|---|---|---|---|
| record-sweep.py | ignore_command_exit | `… or rc != 0 or stated != live:` → `… or stated != live:` | 1/f1 | selftest | killed |
| record-sweep.py | emit_exit_always_zero | `return int(bool(findings))` → `return 0` | 0/f0 | fixture (9 scenarios) | killed |
| record-sweep.py | missing_exe_is_clean | `return 127, ''` → `return 0, ''` | 0/f0 | fixture (s8 stdout) | killed |
| record-sweep.py | pending_all_sections | `in_round = bool(ROUND.match(line))` → `in_round = True` | 1/f2 | selftest | killed |
| record-sweep.py | pending_substring | `cell.strip() == 'PENDING'` → `'PENDING' in cell.strip()` | 1/f1 | selftest | killed |
| record-sweep.py | live_conflict_accepted | `if len(found) == 1 else None` → `if found else None` | 1/f2 | selftest+fixture | killed |
| record-sweep.py | lane_path_escape_allowed | `… or not path.is_relative_to(root):` → `…:` | 0/f0 | fixture (s6) | killed |
| record-sweep.py | value_boundary_dropped | `\b%s=(\d+)\b` → `\b%s=(\d+)` (values) | 0/f0 | fixture (s9 stdout) | killed |
| record-sweep.py | skip_rev_bytes_check | `elif not contains_value(blob,…):` → `elif False:` | 1/f2 | selftest+fixture | killed |
| record-sweep.py | first_binding_only | `for binding in bindings:` → `bindings[:1]:` (revision_sweep) | 1/f1 | selftest | killed |
| record-sweep.py | missing_row_green | `if not row or not contains_value(row,…)` → `if row and …` | 1/f1 | selftest | killed |
| record-sweep.py | rev_against_root | `['git','-C',str(git),` → `['git','-C',str(root),` | 0/f0 | fixture (s11–s13) | killed |
| record-sweep.py | rev_value_boundary_dropped | `(?<![\w.-])%s(?![\w.-])` → `(?<![\w.-])%s` (contains_value) | 1/f1 | selftest | killed |
| record-sweep.py | revisions_flag_dropped | drop `include_revisions=…` from emit call | 0/f0 | fixture (s11–s14) | killed |
| record-sweep.py | revision_summary_zero | `revisions=%d' % sum(…)` → `revisions=%d' % 0` | 0/f0 | fixture (s12,s14) | killed |
| count-c1.py | green_ignores_fail_token | drop `not FAIL.search(out)` from green() | 0/f0 | — | **survived** |
| count-c1.py | killed_ignores_rc | `rc != 0 or bool(FAIL…)` → `bool(FAIL…)` | 0/f0 | — | **survived** |
| count-c1.py | ignore_pristine_red | `met = pristine_ok and total > 0` → `met = total > 0` | 0/f0 | — | **survived** |
| count-c1.py | accept_empty_population | drop `total > 0` from met | 0/f0 | — | **survived** |
| count-c1.py | unanchored_excused | drop `or e.startswith("unanchored")` from met gate | 0/f0 | — | **survived** |
| count-c1.py | detector_gate_dropped | `return 0 if (met and own_ok)` → `return 0 if met` | 0/f0 | — | **survived** |
| count-c1.py | unanchored_still_graded | `if base.count(old) != 1: continue` → `< 1` | 1/f1 | selftest | killed |
| count-c2.py | stale_accepted | drop `not stale` from met | 1/f1 | selftest | killed |
| count-c2.py | duplicates_accepted | drop `duplicates == 0` from met | 0/f0 | — | **survived** |
| count-c2.py | retired_paths_unchecked | `return (BASELINE in line and CLASSES in line)` → `return True` | 0/f0 | — | **survived** |
| count-c2.py | red_literal_unchecked | drop `"round-10 drift pin still red" not in line` from cell_state | 0/f0 | — | **survived** |
| count-c2.py | green_census_tokens_accepted | `p.returncode == 1 and bool(tokens)` → `bool(tokens)` | 0/f0 | — | **survived** |
| count-c2.py | finding_branch_inverted | FINDING derivation `in findings` → `not in findings` | 0/f0 | — | **survived** |
| count-c2.py | malformed_not_residual | `residual={residual + malformed}` → `residual={residual}` | 0/f0 | — | **survived** |
| count-c2.py | keyshape_guard_inverted | KEYSHAPE fallback `value-changed` → `added-since-r10` | 0/f0 | — | **survived** |
| count-c2.py | derive_key_eol_only | KEY regex `(…+)=` → `(…)=$` | 1/f2 | selftest | killed |
| count-c3.py | population_gate_dropped | `if not population_ok(pins):` → `if False:` | 0/f0 | — | **survived** |
| count-c3.py | defeated_accepted | `caught = frc == 1` (drop revisions/token clauses) | 0/f0 | — | **survived** |
| count-c3.py | carrier_drift_allowed | `if here != show(path):` → `if False:` | 0/f0 | — | **survived** |
| count-c3.py | bindings_floor_dropped | `bindings >= 3` → `bindings >= 1` | 0/f0 | — | **survived** |
| count-c3.py | selftest_red_accepted | drop `rc != 0` from tool-selftest gate | 0/f0 | — | **survived** |
| count-c3.py | revisions_default_zero | `fields.get("revisions", -1) == 0` → `…, 0) == 0` | 0/f0 | — | **survived** |
| count-c3.py | summary_first_line | `if m:` → `if m and not fields:` in summary() | 0/f0 | — | **survived** |

`MUTANTS killed=18 total=38 survivors=20`

## Secondary run — freeze-byte counters (superseded but recorded)

19 mutants (the table above minus `unanchored_excused`/`detector_gate_dropped`/
`duplicates_accepted`/`keyshape_guard_inverted`/`population_gate_dropped`, with
`empty_mutation_allowed` on the then-current anchor and pre-duplicate c2 anchors):
killed=3 (`unanchored_still_graded`, `stale_accepted`, `derive_key_eol_only`),
survivors=16 — the same behaviours survive on the entering bytes; the mid-probe counter
hardening did not close any of the gaps below, and added two new ungraded gates
(`unanchored_excused`, `detector_gate_dropped`, `population_gate_dropped`,
`duplicates_accepted`, `keyshape_guard_inverted` are all new-code survivors).

## Coverage findings — exact missing selftest arm for each survivor

Line numbers are the **current worktree bytes**.

count-c1.py (selfcheck, cases block :194–215):
1. `green_ignores_fail_token` (:94–95): missing arm *pristine_fail_token_with_rc0* — a
   synthetic counter that exits 0 while printing both `fail=0` and `fail=2` must read
   pristine=red. Insert a `cases.append` after `red_pristine_reported` (:212–215).
2. `killed_ignores_rc` (:98–99): missing arm *rc_only_kill* — a mutant whose selftest exits 1
   printing no `fail=` token (e.g. traceback) must count killed. Same block, :212–215.
3. `ignore_pristine_red` (:166): the `red_pristine_reported` fixture (:212) pairs a red
   pristine with an empty-mutation set (total=0), so met is False via `total > 0` regardless —
   the pristine clause is untested. Add *red_pristine_with_real_mutant*: red pristine + ≥1
   graded mutant → must be unmet. (:212–215.)
4. `accept_empty_population` (:166): `duplicate_anchor_excluded` (:206–211) asserts tail
   strings only, never `not met`. Add `not met` to that case (all-unanchored ⇒ unmet).
5. `unanchored_excused` (:166–167): no arm has an unanchored anchor beside a green pristine
   and a real kill. Add *unanchored_blocks_met* — one anchor occurring twice, one real mutant
   killed ⇒ still unmet. (:206–211 block.)
6. `detector_gate_dropped` (:259, :272–277): main()'s `own_ok` gate is outside selfcheck and
   unreachable in-memory. Either accept as main-path coverage or add a fixture-repo main()
   arm. (Recommend the c3-style independent-fixture approach.)
7. Status-neutral observation: dead assignment at :163 (`survivors = sum(...)` immediately
   overwritten at :164) — cleanup candidate for the owner seat, no behaviour.

count-c2.py (selfcheck :192–263; fixture builder :199):
8. `duplicates_accepted` (:168): no fixture writes a duplicated `DRIFT_CLASS` line. Add arm
   near `classification_file_absent` (:263) asserting unmet + `stale`/`residual` accounting
   for a duplicated token line.
9. `retired_paths_unchecked` (:110): `retired_row_required` (:257) only deletes the whole
   row. Add *retired_row_missing_path*: row present, classification path absent ⇒ retired=0.
10. `red_literal_unchecked` (:117–118): `red_cell_keeps_unmet` (:252) swaps the literals; a
    cell carrying BOTH `r10 pin retired` and `round-10 drift pin still red` must stay cell=0.
11. `green_census_tokens_accepted` (:167): `green_pin_is_unmet` (:259) uses a token-less
    census, so `bool(tokens)` masks the `rc == 1` clause. Add *green_rc_with_tokens*: census
    exits 0 yet prints a MORI_DRIFT token list ⇒ unmet.
12. `finding_branch_inverted` (:70–71): no fixture token is FINDING-shaped (stub :199 lists
    only `+SURFACE:lane.new +audit fields +VERDICT`). Add `+FINDING:OOM_KILL_JOURNAL` to the
    stub and `value-changed` to the `good` map.
13. `malformed_not_residual` (:171): no malformed-line fixture; add one asserting
    `residual` counts malformed lines in the tail.
14. `keyshape_guard_inverted` (:74–75): no fixture token fails `KEYSHAPE` (all reach the
    SURFACE/FINDING/VERDICT branches or the keys lookup). Add a token like `lane.mori`
    classified `value-changed` per the frozen "anything else" row.

count-c3.py (selfcheck :143–161):
15. `population_gate_dropped` (:225): `population_frozen_ok`/`triplicate`/`subset` (:155–161)
    test the pure function only; main's gate is unexercised. Add a fixture-repo main() arm or
    route the population check through a helper selfcheck can call with a graded verdict.
16. `defeated_accepted` (:215): selfcheck never calls `defeated_fixture` (:116). Add an arm
    with a synthetic tool copy + tiny two-commit repo asserting the `caught` conjunction
    (rc==1 ∧ revisions≥1 ∧ REVISION_MISMATCH in output).
17. `carrier_drift_allowed` (:235): the `carrier_drift_guard` arm (:152–153) is a string
    tautology (`("a\n" != "b\n") and ("a\n" == "a\n")`) that never invokes the worktree-vs-rev
    comparison. Replace with a real comparison arm (two byte strings, differing ⇒ drift).
18. `bindings_floor_dropped` (:254): the `bindings >= 3` gate has no arm. Add one asserting a
    2-binding real-run stays unmet (needs the main-path fixture from #16).
19. `selftest_red_accepted` (:211): add a synthetic tool that prints
    `RECORD_SWEEP_SELFTEST pass=36 fail=0` and then exits 1 ⇒ must be unmet.
20. `revisions_default_zero` (:253): add a summary line lacking `revisions=` ⇒ fields
    default −1 ⇒ unmet (never 0-by-default).
21. `summary_first_line` (:58–59): add a two-`RECORD_SWEEP`-line arm asserting the last line
    wins.

record-sweep.py — 7 selftest-blind kills (its own `--selftest` stayed green; my fixture
caught them). Missing arms in `selftest()` (in-memory, before the revision block ends at
:297) unless noted:
22. `emit_exit_always_zero` (:184–198): no arm calls `emit()` at all. Add
    *emit-exit-and-summary*: findings ⇒ rc 1, empty ⇒ rc 0, counts match.
23. `missing_exe_is_clean` (:155–162): `run_command` is never called (sweep arms stub the
    runner). Add *missing-exe-127*: `run_command(['no-such-tool'], root)` ⇒ `(127, '')`
    (OSError path spawns no child, so the in-memory contract holds).
24. `lane_path_escape_allowed` (:148–153): no arm for `../escape` or absolute carriers ⇒
    must raise ValueError.
25. `value_boundary_dropped` (:48–49): add `live_value('n=45x', 'n') is None` next to
    `live-absent` (:229).
26. `rev_against_root` (:331–334): main()'s `--git` wiring is outside the in-memory selftest;
    the counter's defeated fixture (count-c3.py:116, run at :218–219 with `--root repo
    --git repo` pointing at the SAME dir) is the natural place — split `--root` (plain
    worktree copy) from `--git` (the repo) there so the wiring is graded end-to-end.
27. `revisions_flag_dropped` (:336): add an emit arm asserting `include_revisions=True`
    appends ` revisions=…` and False omits it (:184–198).
28. `revision_summary_zero` (:195): add an emit arm with one revision finding asserting
    `revisions=1` (currently only a fixture with a real git repo can see it).

What the landed revision arm's selftest successfully killed (evidence FOR C3's arm): three of
the four seat-spec example mutants die by selftest — `skip_rev_bytes_check` (the D81-1 shape,
fail=2), `first_binding_only` (fail=1 via revision-second-stale), `missing_row_green` (fail=1
via revision-missing-row); the fourth, `rev_against_root`, is selftest-blind and dies only
end-to-end (fixture s13). `rev_value_boundary_dropped` dies by selftest (fail=1 via
revision-token-boundaries). The r81 five-survivor classes are all dead in the landed bytes:
`ignore_command_exit`, `first_binding_only`, `pending_substring`, `rev_value_boundary_dropped`
die by selftest and `value_boundary_dropped` dies by fixture — none survives.

## Exact commands and outputs (abridged to the decisive lines)

```text
$ python3 /fast/scratch/hyaku/mori-r82/Mo82M01Mutants/mutate.py rs
== PRISTINE ==
rs selftest rc=0 pass=36 fail=0 killed=False
rs fixture suite green: 14 scenarios
== MUTANTS ==
MUTANT rs ignore_command_exit st_rc=1 st_fail=1 st_killed=True fixture=blind -> killed
… (15 rows; see table) …
MUTANTS killed=15 total=15 survivors=0

$ python3 /fast/scratch/hyaku/mori-r82/Mo82M01Mutants/mutate.py counters <snapshot-freeze>
c1 selftest rc=0 pass=4 fail=0 | c2 rc=0 pass=9 fail=0 | c3 rc=0 pass=5 fail=0
MUTANTS killed=3 total=19 survivors=16

$ python3 /fast/scratch/hyaku/mori-r82/Mo82M01Mutants/mutate.py counters <snapshot2-current>
c1 selftest rc=0 pass=4 fail=0 | c2 rc=0 pass=9 fail=0 | c3 rc=0 pass=8 fail=0
MUTANTS killed=3 total=23 survivors=20

$ sha256sum <4 lane files>            # before == after for record-sweep.py;
$ diff before.sha after.sha           # counters differ ONLY by the executor's mid-probe edits
2,4c2,4 < ba0646a3…/95a6b856…/af57ec5f… --- > 84a85af8…/e73d919e…/65850d9a…
$ find <scratch> -maxdepth 4 -name .git -type d
…/fix/s11/repo/.git  …/fix/s12/repo/.git  …/fix/s13/gitrepo/.git   # fixture repos only
```

Full per-mutant stdout is in the session transcript; every mutant run completed under its
120 s bound (no timeouts; slowest file ≈ 7 s wall for the 15-mutant rs suite).

## Verified / not verified

Verified: all pristine baselines green before grading; every anchor occurred exactly once in
its snapshot bytes (driver-asserted); no empty mutations; fixture-repo git operations
contained in scratch with toplevel assertions; lane bytes untouched by this seat (record-sweep
sha identical before/after; counter sha changes are the executor's concurrent work, first seen
via `git status`/hash diff, never written by me).

Not verified: the counters' and tool's `<rev>`/`--root --pins` main paths over the real lane
(not my population; I ran `--selftest` plus scratch fixtures only); whether the current
counter/tool bytes are final — executors were still editing during this probe, so re-run the
primary table against the landed tip before the round receipt cites it. My two initial
fixture-authoring failures (s11, s12) were detector bugs of mine, corrected before grading;
the graded tool was right both times.

Defects found in other seats' bytes (file:line, current bytes): count-c3.py:152–153
(carrier_drift_guard arm is a tautology — a graded guard is asserted by a literal string
comparison that tests nothing); count-c1.py:163 (dead `survivors = sum(...)` assignment);
count-c1.py:212–215 (red-pristine arm cannot detect a pristine-gate inversion because its
mutant set is empty, total=0). All are status-neutral coverage gaps; per my role I change
nothing — a surviving mutant is a coverage finding, not permission to alter the contract.
