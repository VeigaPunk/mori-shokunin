# Mo81E02C3Fix — C3 routed exposures

## Scope and axes

Changed `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80/count-c3.py` and produced this report at `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/w1/Mo81E02C3Fix.md` only.
Axes: operability (three routed fixes), calibration (retain actual verdicts), coverage (three added arms), depth (file/tree distinction), freshness (current worktree checks), adjacency (read-only graded revision; no external remediation). No tool installs. No LSP tool is exposed in this seat; used explicit local callsite reads instead.

## Implementation / requested diff hunks

`git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff -- .ufo/waves/round-80/count-c3.py` exited 0 and reported these exact hunk headers:

- `@@ -28,7 +28,9 @@`: TOKEN gains `(?<![\w./-])` and an optional captured single directory prefix. Only unprefixed `tools/` or the own-repo prefix is accepted by grade.
- `@@ -36,23 +38,27 @@`: replace `present_set` and `SIBLING` with `tree_sets`; one `git ls-tree -r -t` read separates tree entries from instruments by object type. `grade(text, present, directories, own)` ignores foreign prefixes and named directory basenames; nonexistent names remain extra.
- `@@ -77,31 +83,57 @@`: migrate all selftest callsites; assert fixture toplevel before add/commit; strengthen the prior directory fixture by committing a child and naming the directory; add exactly three cases: `subdir_path_not_naming`, `own_lane_prefix_allowed`, `named_directory_ignored`. The last case also asserts an absent `gone.py` remains extra.
- `@@ -133,15 +165,16 @@`: main consumes both tree sets and derives OWN with `os.path.basename(os.path.realpath(repo))` from the graded repo, including explicit `--repo`.

No r80 contract or output-format statement was edited. Did not touch either count-c1.py. Existing per-case selftest grammar and summary grammar are retained; tally increases from four to seven cases.

## Retained execution evidence

All checks below were explicitly requested by the assignment and L1. Working directory was `/home/vgpnk/Projects/shokunin/mori-shokunin`. Executed this exact shell command (absolute script paths avoid fleet-root ambiguity):

```sh
S=/fast/scratch/hyaku/mori-r81/Mo81E02C3Fix; trap 'rm -rf -- "$S"' EXIT; TMPDIR="$S" python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80/count-c3.py --selftest; printf 'selftest_rc=%s\n' "$?"; python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80/count-c3.py 44bc941a0e3e9676fa33a882b43d6e9793cbf74d --scratch "$S"; printf 'real_rc=%s\n' "$?"; python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/count-c1.py 44bc941a0e3e9676fa33a882b43d6e9793cbf74d --scratch "$S"; printf 'frozen_harness_rc=%s\n' "$?"
```

Complete stdout (shell exited 0):

```text
PASS complete named=3 present=3 missing=0 extra=0
PASS missing_one named=2 present=3 missing=1 extra=0
PASS extra_stale named=4 present=3 missing=0 extra=1
PASS sibling_and_directory_ignored named=3 present=3 extra=[]
PASS subdir_path_not_naming named=0 missing=['mori-census.sh']
PASS own_lane_prefix_allowed named=1 extra=[]
PASS named_directory_ignored named=2 extra=['gone.py']
C3_COUNTER_SELFTEST pass=7 fail=0
selftest_rc=0
C3=met named=56 present=56 missing=0 extra=0 rev=44bc941a0e3e
real_rc=0
A2_summary_contradicts_mismatch_line expected=unmet got=met rc=0
A3_two_contradicting_summaries expected=unmet got=met rc=0
A4_second_carrier_row_stale expected=unmet got=met rc=0
A5_repo_path_with_space expected=met got=setup rc=2
B1_subdir_path_counts_as_naming expected=unmet got=met rc=0
B2_own_lane_prefix_excluded expected=met got=unmet rc=1
B6_directory_named_as_tool expected=met got=unmet rc=1
C1=unmet wrong=7 fixtures=7 real_c1=met real_c3=met rev=44bc941a0e3e
frozen_harness_rc=1
```

Before/after selftest tally: **before 4/0 is historical evidence, not rerun by this seat** (`.ufo/waves/round-80/w1/Mo80R01Counter.md` §1 item 2 reports amended counters 4/4, rc 0; pre-edit source also contains four cases). **After 7/0 is directly executed above.** No claim of a freshly measured before run.

Setup command also executed: `mkdir -p /fast/scratch/hyaku/mori-r81/Mo81E02C3Fix && echo ok && git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse --short HEAD && git -C /home/vgpnk/Projects/shokunin/mori-shokunin status --porcelain | wc -l`; completion notification exit 0; stdout was not delivered, so no HEAD/status count is asserted. This initial command was inadvertently named as a service; it completed immediately and no long-lived process remains. The later check command's EXIT trap removed the seat scratch directory. No scratch artifacts are cited as durable evidence.

## Other-seat defect / coordination

Before editing, read `.ufo/waves/round-81/count-c1.py:150-153`: B2 created a repo named `b2` but named `mori-shokunin/tools/mori-census.sh`. A repo-basename implementation would correctly reject that foreign prefix. Reported exact mismatch to MoriR81; L1 agreed to change the fixture repo's basename to `mori-shokunin` without changing the expected verdict. Did not edit that file.

The requested third command above intentionally grades **entering counter bytes**, not this worktree implementation: `.ufo/waves/round-81/count-c1.py:184-194,259-264` exports counters from the requested revision. Therefore its seven red fixture readings reproduce the entering control and do not falsify the edited C3. Notified L1; meaningful integration measurement must grade the landed revision or use `--counters /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80` against current worktree counters.

## Limits and handoff

Directly verified seven C3 selftest arms and unchanged real-lane `44bc941a` reading. Not verified: landed-revision integrated C1, mutation resistance, all lane batteries, or a fresh before-tally run. Parent owns those checks; no integrated-green claim is made. Only four selftest fixture repositories were mutated, entirely under seat scratch; every add/commit was preceded by a toplevel equality assertion. No lane git mutation, host/service/credential change or external remediation was performed.

Self-evaluation: accuracy 4 (measured outputs distinguished from inherited baseline); completeness 4 (landed integration remains parent-owned); clarity 4 (full seven red lines need revision context); actionability 4 (explicit integration command supplied); conciseness 4 (full command/stdout retained per assignment). Average 4.0. Highest-value next check is the parent's integrated landed-revision keeper; user should agree with the distinction between selftest-green and integration-unmeasured.
