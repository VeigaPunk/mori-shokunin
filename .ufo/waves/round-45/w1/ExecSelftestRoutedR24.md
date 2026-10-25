# ExecSelftestRoutedR24 — round 45, wave 1 (residual seat)

Surface: `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-routed-r24.py` only.
Diff: `576 5 tools/mori-routed-r24.py` (`git diff --numstat`).

## 0. What landed

`tools/mori-routed-r24.py` had no self-test mode: the four `--selftest`
occurrences were the module docstring, the `EVIDENCE_COMMAND` constant, the
`_run_pressure_selftest` docstring and its subprocess list (which runs
*mori-pressure.py*). Its argparse kept only `--repo/--rev/--rerun`.

Added:

1. **A real argv branch.** `main()` now reads `raw = sys.argv[1:]` first and, when
   `"--selftest"` is in it, calls `_selftest_dispatch(raw)` *before* argparse
   runs. That is a deliberate ordering: `--repo`/`--rev` stay `required=True`, so
   the production usage error, `--help` text and `--bogus` error stay
   byte-identical (proved in §3). Companion arguments are rejected with exit 2;
   a bare `--selftest` runs the check.
2. **`selftest()`: 26 arms** over one throwaway git repository built in a
   `tempfile.TemporaryDirectory(dir=$TMPDIR)` and removed on exit. The fixture
   repo has four commits: base tree, the correctly recorded round-25 evidence
   file, a forged evidence file (bad `command:` line plus a replayed body), and a
   `.gitignore` carrying a `!tools/*.pyc` negation. Nothing outside `$TMPDIR` is
   read or written; git runs with the tool's own clean env
   (`GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, pinned author/
   committer identity and dates); no network call is made.
3. **`_verdict(rows, d4_held)`** — the exit-0/1 decision extracted from `main`
   unmodified in behaviour (`("held"|"failed", held, mismatches,
   RC_HELD|RC_FAILED)`) so that the held/failed mapping is arm-testable. The
   production payload is unchanged, byte for byte (§3).
4. **Module docstring** documents the mode, its tally format and its limits.

Arm coverage: `_normalize`; `_split_header` (key order, missing key, byte-anchored
body); `_blocks`/`_section_span`/`_data_row_count`; the D2 in/out-of-corrections
partition *and* each `D2_NEGATIVE_PATTERNS` regex against a sample stale line;
`_axes_rows` (incl. an embedded pipe and the absent-heading `None`);
`_parse_pinned_scores` (window, missing axis, duplicate axis); `D5_ROUND1_RE`;
pinned-contract literals (`EXPECTED_BODY`, `EVIDENCE_COMMAND`,
`HEADER_KEY_ORDER`, `REVISION_LINE_RE` width/case); `_count_cases`; `HEX_TOKEN_RE`
7/40 bounds; `_resolve_commit` + `_is_ancestor`; `_ls_tree_entry` + `_blob_bytes`;
`_check_d1` held on correct evidence and rejected on forged evidence; `_check_d4`
held and rejected on the negation line; `_verdict`; `_emit`; `main` failed
verdict (rc 1, D1+D4 held, D2/D3/D5 fail closed on the unreadable pinned bases);
`main` unreadable repo (rc 2) and unresolvable rev (rc 2); the `--selftest`
argv branch itself; and `main([])` still exiting 2 through argparse.

No new dependency: only `contextlib` was added to the import list, which is
stdlib. Runtime 84 ms (limit 120 s).

## 1. Selftest evidence (its own tally, real output)

```
$ export TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/tmp/ExecSelftestRoutedR24/tmpdir
$ python3 -I -B tools/mori-routed-r24.py --selftest
selftest PASS normalize_folds_markers_case_whitespace
selftest PASS split_header_reads_five_keys_and_body
selftest PASS split_header_reports_the_missing_key
selftest PASS body_is_byte_anchored
selftest PASS blocks_and_section_span_partition
selftest PASS data_row_count_excludes_header_and_separator
selftest PASS d2_negatives_absent_positives_present_outside
selftest PASS axes_rows_read_score_and_last_change
selftest PASS pinned_scores_parse_window_and_fail_closed
selftest PASS round1_token_regex
selftest PASS pinned_contract_literals
selftest PASS d2_negative_patterns_match_samples
selftest PASS count_cases_json_arms
selftest PASS hex_token_width_and_boundaries
selftest PASS resolve_commit_and_ancestor
selftest PASS ls_tree_entry_and_blob_bytes
selftest PASS check_d1_holds_on_synthetic_evidence
selftest PASS check_d1_rejects_forged_evidence
selftest PASS check_d4_holds_and_rejects_negation
selftest PASS verdict_maps_held_and_failed
selftest PASS emit_writes_one_json_line
selftest PASS main_failed_verdict_exit_1
selftest PASS main_unreadable_repo_exit_2
selftest PASS main_unresolvable_rev_exit_2
selftest PASS selftest_flag_branch_rejects_companions
selftest PASS repo_and_rev_stay_required
ROUTED_R24_SELFTEST pass=26 fail=0
rc=0        wall_ms=84        fixture residue under $TMPDIR afterwards: 0 entries
```

Exit 2 (setup) arm, verbatim:

```
$ TMPDIR=$TDIR/nope python3 -I -B tools/mori-routed-r24.py --selftest
selftest FAIL setup: fixture base is not a directory: .../ExecSelftestRoutedR24/nope
ROUTED_R24_SELFTEST pass=0 fail=1
rc=2
```

Exit 1 (able to fail): six mutants of a scratch copy, each a one-site text
substitution (`$TDIR/final-mut-<name>.py`, all under the round tmp dir):

| mutant | site changed | rc | tally | first failing arm |
|---|---|---|---|---|
| `body-const` | `48/48` → `47/48` in `EXPECTED_BODY` | 1 | pass=25 fail=1 | `pinned_contract_literals` |
| `verdict-d4` | `ok = mismatches == 0 and d4_held` → `ok = mismatches == 0` | 1 | pass=25 fail=1 | `verdict_maps_held_and_failed` |
| `d2-pattern` | spike pattern → `"spike.{0,60}invisible"` | 1 | pass=25 fail=1 | `d2_negative_patterns_match_samples` |
| `d4-negation` | `stripped.startswith("!")` → `("!!")` | 1 | pass=25 fail=1 | `check_d4_holds_and_rejects_negation` |
| `hex-width` | token width `{7,40}` → `{5,40}` | 1 | pass=25 fail=1 | `hex_token_width_and_boundaries` |
| `header-order` | swap `tool_blob`/`fixtures_tree` in `HEADER_KEY_ORDER` | 1 | pass=21 fail=5 | `split_header_reads_five_keys_and_body` |

## 2. Byte-identical production behaviour

Pre-edit bytes recovered read-only from the lane's `HEAD`
(`git show HEAD:tools/mori-routed-r24.py`), so both files could be run under the
same basename (argparse `prog`):

```
pre_edit_sha256 = cf5ef5815f1118ae3595171edde7f527176fde03480665eb6bbb46921c2969ef
worktree_sha256 = 10a36555904a4dce0ffa1c86575cdeeb164c47fe2f8ccd4571a87d7beef95f18   (1522 lines, +576/-5)
```

Representative call (before → after), plus the reviewer-useful surfaces:

```
held        before_rc=0 after_rc=0 stdout_diff=EMPTY stderr_diff=EMPTY sha_out_equal=yes
failed      before_rc=1 after_rc=1 stdout_diff=EMPTY stderr_diff=EMPTY sha_out_equal=yes
rerun       before_rc=0 after_rc=0 stdout_diff=EMPTY stderr_diff=EMPTY sha_out_equal=yes
help        before_rc=0 after_rc=0 stdout_diff=EMPTY stderr_diff=EMPTY sha_out_equal=yes
noargs      before_rc=2 after_rc=2 stdout_diff=EMPTY stderr_diff=EMPTY sha_out_equal=yes
missingrev  before_rc=2 after_rc=2 stdout_diff=EMPTY stderr_diff=EMPTY sha_out_equal=yes
bogusflag   before_rc=2 after_rc=2 stdout_diff=EMPTY stderr_diff=EMPTY sha_out_equal=yes
```

with

```
held    --repo /home/vgpnk/Projects/shokunin/mori-shokunin --rev 554ff416
failed  --repo /home/vgpnk/Projects/shokunin/mori-shokunin --rev 28b79d3d1b76824f0c825aabe6cb6c5dc49961bf
rerun   --repo /home/vgpnk/Projects/shokunin/mori-shokunin --rev 554ff416 --rerun
```

The pasted diff for the representative call, verbatim (empty — the command
printed nothing):

```
$ diff -u $TDIR/final-before-held.out $TDIR/final-after-held.out
$
```

stdout sha256, before and after (identical, 2734 bytes each):

```
e1af1c404c77cc70e8543181444f37ca902e70b55e0ff6e487bda8c69e7bae82  final-before-held.out
e1af1c404c77cc70e8543181444f37ca902e70b55e0ff6e487bda8c69e7bae82  final-after-held.out
```

`failed` 2115 B, `rerun` 2951 B: same before/after sha256
(`8f78c926…3b41`, `ecd2d7b2…6f56`). All 20 diff files
(`cmp-*.stdout.diff`, `cmp-*.stderr.diff`, `final-*.diff`,
`final-*-err.diff`) are 0 lines (`cat … | wc -l` → 0).

## 3. Gate-registry auditor

Ordered command, at the revision the ticket names:

```
$ python3 tools/mori-gate-registry.py --rev 554ff416 --audit-all
audit tools/mori-routed-r24.py                 FAIL row='routed round-24 items (r25, C1)' (row 'routed round-24 items (r25, C1)' tool has no real --selftest argv branch)
registered=29 unregistered=3 no_selftest=4 duplicate=0 wrong_row=0 tables=7
rev=554ff416459c92f0dea9762f834a556df2990187
REGISTRY=unmet
rc=1
```

It still counts the path as `no_selftest`, and the ticket says to paste that line
and stop, which I did — **no workaround** (no commit, no registry edit, no
`SKILL.md` edit, no altered auditor). The cause is structural: `554ff416` is a
round-44 commit, my edit is uncommitted by this lane's rules, and the auditor
reads the tool body *from that revision's tree*. The blob at `554ff416` is the
pre-edit body (`cf5ef581…`).

The same auditor over the live working tree, which is the state the parent will
commit, does find the branch:

```
$ python3 tools/mori-gate-registry.py --rev WORK --audit-all
audit tools/mori-routed-r24.py                 PASS row='routed round-24 items (r25, C1)' (8 cells, entry resolves, --selftest argv branch)
registered=33 unregistered=6 no_selftest=0 duplicate=0 wrong_row=0 tables=7
rev=WORK
REGISTRY=unmet
rc=1
```

`no_selftest` for this path: 1 → 0. `REGISTRY=unmet` at `WORK` is driven by six
other paths that no row names (`mori-disk-rate.py`, `mori-round41-calibration.py`,
`mori-wave-settlement.py`, …), not by this file. Re-running
`--rev <post-commit HEAD> --audit-all` after the parent commits is the check that
should show the path registered at a committed rev; I cannot produce that rev
without committing.

## 4. Retained evidence

All under `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/tmp/ExecSelftestRoutedR24/`:

- `selftest.out` (26 PASS + tally), `selftest.time`, `tmpdir/` (empty after runs)
- `pre-edit/mori-routed-r24.py` (the `HEAD` blob used as "before")
- `final-before-{held,failed,rerun}.out/.err`, `final-after-*`, `final-*.diff`
- `cmp-*` (7 surfaces × stdout/stderr diffs), `cmp-before-*`, `cmp-after-*`
- `final-mut-<name>.py/.out` (6 mutants), `mutant-*.py`, `mut-d2/d4/hex.out`
- `audit-554ff416.txt`, `audit-WORK.txt`, `audit-before-routed*.txt`
- `skill-at-554ff416.md` (registry row snapshot the audit was checked against)

## 5. Risks, limits, hand-off

- **All-held exit 0 is not reachable from synthetic fixtures.** D2, D3 and D5 are
  pinned to fixed base commits (`28b79d3d…`, `4f05dd5a…`) that a throwaway repo
  cannot carry, so the self-check asserts the held/failed *mapping* (`_verdict`
  arm, plus rc-2 arms) and the all-held end-to-end path is evidenced by the
  production call at `554ff416` (§2, `held`, rc 0). This is stated in the module
  docstring rather than papered over.
- **`--help` deliberately does not list `--selftest`.** Registering it with
  argparse would have changed `--help`/usage bytes; the flag is dispatched before
  argparse and documented in the module docstring, so every pre-existing
  invocation surface stays byte-identical. If the parent prefers it in `--help`,
  that is a one-line `parser.add_argument("--selftest", action="store_true", …)`
  and knowingly changes `--help` only.
- **`SKILL.md` registry row not touched** (out of scope and forbidden here). Its
  self-test cell still reads "none built in — the tool has no `--selftest`"; the
  auditor does not read that cell (it inspects the tool body), which is why the
  `WORK` audit already passes, but the row's prose is now stale and should be
  corrected by whoever owns `SKILL.md`.
- No installs or upgrades were needed or performed; no network; no mutating git
  or jj command; no `pacman` transaction. Standard library only.
