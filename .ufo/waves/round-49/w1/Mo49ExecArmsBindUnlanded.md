# Mo49ExecArmsBindUnlanded — selftest-arm gaps of the bind rules and of the unlanded check

author-date: 2026-10-25
lane tip cited: `0df17b7b` (round-49 freeze; entering tip `b3e3453d`)
seat: w1 executor, leaf (no subagent spawned)

**Deliverable.** Two scratch copies carry new `--selftest` arms that kill every listed round-48
mutant:

| copy | base | new tally | was |
|---|---|---|---|
| `.scratch/r49-Mo49ExecArmsBindUnlanded/unlanded-arms.py` | `tools/mori-unlanded-check.py` (`e6695e04…`) | `UNLANDED_SELFTEST pass=17 fail=0` | `pass=13 fail=0` |
| `.scratch/r49-Mo49ExecArmsBindUnlanded/witness-arms.py` | `.ufo/waves/round-49/controls/tool-r48-merged-witness.py` (`c30ab623…`) | `PIN_CHECK_SELFTEST pass=67 fail=0` | `pass=65 fail=0` |

Both unmutated copies exit 0. Every round-48 survivor now fails on exactly the new arm at the
mutated copy (`rc=1`), and the same arm prints `PASS` on the unmutated copy. No tracked file, no
frozen byte, no git/jj state was touched; the L1 integrates.

## Method

- Scratch root `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ExecArmsBindUnlanded`
  for every lane-tool run; all fixture repositories live under it.
- Baselines first: `python3 unlanded-pristine.py --selftest` → `UNLANDED_SELFTEST pass=13 fail=0`,
  rc 0 (`receipt-unlanded-13.txt`); `python3 witness-pristine.py --selftest` →
  `PIN_CHECK_SELFTEST pass=65 fail=0`, rc 0 (`receipt-witness-65.txt`).
- Detector per mutant: the copy's own `--selftest`; killed iff non-zero exit. Every mutation is a
  single-point text edit in a separate scratch copy (`m_*.py`, `arms-*.py`); the pristine copies
  and both arm copies were never edited after creation (hashes below).
- Reproducer probe (`probe-arms.py`) scores the two new bind-rule case rows through `check()` with
  the pristine and the mutated module, so the gap is shown as a scoring difference, not only as a
  selftest verdict.
- Fixture repos: `D=$(mktemp -d -p <scratch> …)`, `git -C "$D" init -q`, and
  `git -C "$D" rev-parse --show-toplevel` compared to `$D` before the first commit (printed in the
  probe transcript for `probe-sort.*`/`probe-sort2.*`); the arms' own `sandbox()` helper already
  asserts the same. No git write ran in the lane, in `shokuknow`, or in any lane path.

## 1. Unlanded check — `UNLANDED_SELFTEST pass=17 fail=0`

Pre-arm reproduction of the two round-48 survivors (mutants on the **unedited** suite):

```
== m2_rename  rc=0 :: UNLANDED_SELFTEST pass=13 fail=0        # M2 survivor reproduced
== m8_cap     rc=0 :: UNLANDED_SELFTEST pass=13 fail=0        # M8 survivor reproduced
```

Five further single-point probes were run to look for other survivors. Three were real survivors
(`u5`, `u7` below reported as such; `u3`/`u4` were already killed) and one (`u6`) is behaviourally
equivalent — see Limits.

### Added arms (4, all in `selftest()` of the copy)

1. `rename_source_not_listed` — commit top-level `NOTE.md`, `git mv NOTE.md docs/NOTE.md`, expect
   `rc=0` and exactly `['UNLANDED=clean round=8']`. Kills the deleted `-z` rename-source skip: the
   mutant consumes the rename source as a status record and fabricates `unlanded NO E.md`.
2. `in_scope_rename_lists_destination_only` — `git mv corpus/keep.md corpus/moved.md`, expect
   exactly `['UNLANDED=dirty round=8 paths=1', 'unlanded R. corpus/moved.md']` (one line per path,
   rename destination named, source never emitted).
3. `list_cap_50_of_60` — 60 untracked in-scope files in a tracked directory, expect header
   `paths=60`, exactly 51 output lines, first `F00.md` and last `F49.md`. Kills both the removed cap
   and a cap off by one.
4. `modified_status_rendered_with_dot` — one tracked `corpus/` file modified, expect exactly
   `['UNLANDED=dirty round=8 paths=1', 'unlanded .M corpus/lessons/round-8.md']`. The pre-existing
   `modified_tracked_report_exit1` arm passes on any line containing `A.md`, so it never pinned the
   rendered status pair.

### Mutant matrix (all against the 17-arm copy)

| # | single-point mutation | old suite | new suite | killing arm (observed FAIL) |
|---|---|---|---|---|
| M1 | drop `os.path.realpath(top) != os.path.realpath(repo)` setup guard | killed | killed `pass=15 fail=2` | `subdirectory_is_setup_error`, `cli_setup_rc2` |
| M2 | drop `if xy[0] in "RC": i += 1` (rename-source skip) | **SURVIVED 13/13** | **killed** `pass=16 fail=1` | `rename_source_not_listed` — `rc=1 ['UNLANDED=dirty round=8 paths=1', 'unlanded NO E.md']` |
| M3 | drop `or path.startswith("tools/")` | killed | killed `pass=16 fail=1` | `lessons_and_space_in_path_listed` |
| M4 | admit `.scratch/` into `in_scope()` | killed | killed `pass=15 fail=2` | `outside_scope_and_scratch_not_listed`, `other_round_not_listed` |
| M5 | `if in_scope(...)` → `if in_scope(...) and xy[1] != " "` (index-only records dropped) | killed | killed `pass=14 fail=3` | `staged_but_uncommitted_listed`, **`in_scope_rename_lists_destination_only`** (new), `cli_dirty_rc1` |
| M6 | round filter `round-%d/` → `round-` | killed | killed `pass=16 fail=1` | `other_round_not_listed` |
| M7 | `return 1, lines` → `return 0, lines` | killed | killed `pass=8 fail=9` | nine arms incl. `list_cap_50_of_60`, `modified_status_rendered_with_dot` |
| M8 | `found[:LIST_CAP]` → `found` | **SURVIVED 13/13** | **killed** `pass=16 fail=1` | `list_cap_50_of_60` — `rc=1 lines=61 last=unlanded ?? .ufo/waves/round-8/w2/F59.md` |
| u3 | `("/" not in path and path.endswith(".md"))` → `path.endswith(".md")` | killed | killed `pass=15 fail=2` | `other_round_not_listed` (+ new rename arm) |
| u4 | `--untracked-files=all` → `--untracked-files=normal` | killed | killed `pass=14 fail=3` | `untracked_late_result_exit1_names_it`, `other_round_listed_for_that_round`, `lessons_and_space_in_path_listed` |
| u5 | `xy.replace(" ", ".")` → `xy` | **SURVIVED 13/13** | **killed** `pass=15 fail=2` | `modified_status_rendered_with_dot` — `unlanded  M corpus/lessons/round-8.md`; also `in_scope_rename_lists_destination_only` (`unlanded R  corpus/moved.md`) |
| u6 | `sorted(found, key=…)` → `found` | SURVIVED 13/13 | survives (equivalent mutant) | none possible — see Limits |
| u7 | `LIST_CAP = 50` → `51` | **SURVIVED 13/13** | **killed** `pass=16 fail=1` | `list_cap_50_of_60` — `rc=1 lines=52 last=…F50.md` |

Unmutated copy, new arms: `PASS rename_source_not_listed`, `PASS in_scope_rename_lists_destination_only`,
`PASS list_cap_50_of_60`, `PASS modified_status_rendered_with_dot` (`receipt-unlanded-17.txt`).

### Diff — `tools/mori-unlanded-check.py` → `unlanded-arms.py`

```diff
--- tools/mori-unlanded-check.py	2026-10-25 19:21:36.221919857 -0300
+++ .scratch/r49-Mo49ExecArmsBindUnlanded/unlanded-arms.py	2026-10-25 21:39:48.250214189 -0300
@@ -150,6 +150,47 @@
         rc, out = run(d, 8)
         arm("staged_but_uncommitted_listed", rc == 1 and any("round-8.md" in l for l in out), "rc=%d" % rc)
 
+        # round 49 (Mo49ExecArmsBindUnlanded): shapes the arms above never build —
+        # a git rename (the `-z` rename-source skip was dead code to the suite) and a
+        # list longer than LIST_CAP (the 50-path cap was never reached).
+        rn = sandbox("rename")
+        write(rn, "NOTE.md", "note\n")
+        commit(rn, "note")
+        os.makedirs(os.path.join(rn, "docs"), exist_ok=True)
+        subprocess.run(["git", "-C", rn, "mv", "NOTE.md", "docs/NOTE.md"], check=True)
+        rc, out = run(rn, 8)
+        arm("rename_source_not_listed", rc == 0 and out == ["UNLANDED=clean round=8"], "rc=%d %s" % (rc, out))
+        write(rn, "corpus/keep.md", "keep\n")
+        commit(rn, "keep")
+        subprocess.run(["git", "-C", rn, "mv", "corpus/keep.md", "corpus/moved.md"], check=True)
+        rc, out = run(rn, 8)
+        arm("in_scope_rename_lists_destination_only",
+            rc == 1 and out == ["UNLANDED=dirty round=8 paths=1", "unlanded R. corpus/moved.md"],
+            "rc=%d %s" % (rc, out))
+
+        cap = sandbox("cap")
+        write(cap, ".ufo/waves/round-8/w2/keep.md", "x\n")
+        commit(cap)
+        for i in range(60):
+            write(cap, ".ufo/waves/round-8/w2/F%02d.md" % i)
+        rc, out = run(cap, 8)
+        arm("list_cap_50_of_60",
+            rc == 1 and out[0] == "UNLANDED=dirty round=8 paths=60" and len(out) == 51
+            and out[1] == "unlanded ?? .ufo/waves/round-8/w2/F00.md"
+            and out[-1] == "unlanded ?? .ufo/waves/round-8/w2/F49.md",
+            "rc=%d lines=%d last=%s" % (rc, len(out), out[-1]))
+
+        # The rendered status pair is part of the output line (`unlanded .M path`);
+        # `any(" .M " … or "A.md" in l …)` above also passes when the space is kept.
+        fmt = sandbox("format")
+        write(fmt, "corpus/lessons/round-8.md", "v1\n")
+        commit(fmt)
+        write(fmt, "corpus/lessons/round-8.md", "v2\n")
+        rc, out = run(fmt, 8)
+        arm("modified_status_rendered_with_dot",
+            rc == 1 and out == ["UNLANDED=dirty round=8 paths=1", "unlanded .M corpus/lessons/round-8.md"],
+            "rc=%d %s" % (rc, out))
+
         sub = os.path.join(d, "corpus")
         try:
             run(sub, 8)
```

## 2. Bind rules — `PIN_CHECK_SELFTEST pass=67 fail=0`

Pre-arm reproduction of the two round-48 survivors on the merged witness (unedited suite):

```
== m_r5a   rc=0 :: PIN_CHECK_SELFTEST pass=65 fail=0     # m_r5a survivor reproduced
== m_r10b  rc=0 :: PIN_CHECK_SELFTEST pass=65 fail=0     # m_r10b survivor reproduced
```

The six round-48 mutants that the v3 suite killed were re-run against the merged witness to check
the merge did not lose kill power — all six still die:

| mutant | 65-arm result | killing arm |
|---|---|---|
| m_r4a (`rebound = True` → `False`, existing-row argv change) | `pass=63 fail=2` rc 1 | `v2_rebound_to_other_tool`, `v2_entry_rebound` |
| m_r4b (`len(base_bind_prefix[prefix]) == 1` → `== 0`) | `pass=64 fail=1` rc 1 | `r4_rebound_new_row_same_prefix` |
| m_r5b (`line_count_pins` binding → `None`) | `pass=63 fail=2` rc 1 | `r5_line_count_match`, `r5_line_count_mismatch` |
| m_r6a (`.startswith(pfx)` → `.startswith(pfx[:4])`) | `pass=64 fail=1` rc 1 | `r6_trunc_digest_mismatch` |
| m_r6b (`hit = p`) | `pass=63 fail=2` rc 1 | `r6_trunc_digest_mismatch`, `r10_trunc_digest_decoy_file_in_other_cell` |
| m_r10a (digest binds row-wide) | `pass=64 fail=1` rc 1 | `r10_digest_decoy_file_in_other_cell` |

The two survivors, against the 67-arm copy:

| mutant | mutation | 67-arm result | killing arm |
|---|---|---|---|
| m_r5a | `if nl != num:` → `if nl > num:` (over-pin accepted) | `pass=66 fail=1` rc 1 | `r5_line_count_overpin_mismatch` — `PIN_CHECK=met … mismatches=0` |
| m_r10b | `_nearest_in_tree_path(st[:dm.start()], root)` → `st[dm.end():]` | `pass=66 fail=1` rc 1 | `r10_digest_binds_to_nearest_preceding_path_not_following` — `PIN_CHECK=met … mismatches=0` |

Reproducer (same row, pristine vs mutant module; `probe-arms.py`, exit 0):

```
[r5_line_count_overpin] pristine met=False
    pin line=3 kind=lines state=mismatch pinned='43 lines' file=tools/lc.py observed=42
    PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=deadbeef baseline=no
[r5_line_count_overpin] mutant met=True
    pin line=3 kind=lines state=mismatch pinned='43 lines' file=tools/lc.py observed=42
    PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 …

[r10_digest_before_path] pristine met=False
    pin line=3 kind=digest state=mismatch digest=86067065ec46 file=tools/foo.py
    PIN_CHECK=unmet tally_pins=1 digest_pins=1 mismatches=1 …
[r10_digest_before_path] mutant met=True
    pin line=3 kind=digest state=match digest=86067065ec46 file=tools/slow.py
    PIN_CHECK=met tally_pins=1 digest_pins=1 mismatches=0 …
```

Both new arms are the negative counterpart of an existing positive arm, and both positive
counterparts still pass on the unmutated copy (`PASS r5_line_count_match`,
`PASS r10_digest_binds_to_nearest_preceding_path`), so neither arm is satisfied by rejecting
everything. The new negative arms print `PIN_CHECK=unmet … mismatches=1` on the unmutated tool
(`receipt-witness-67.txt`).

### Diff — `controls/tool-r48-merged-witness.py` → `witness-arms.py`

```diff
--- .ufo/waves/round-49/controls/tool-r48-merged-witness.py	2026-10-25 20:42:21.653394178 -0300
+++ .scratch/r49-Mo49ExecArmsBindUnlanded/witness-arms.py	2026-10-25 21:40:46.703409150 -0300
@@ -931,6 +931,12 @@
                                                           entry="`python3 tools/lc.py`"), 1, False, "mismatch"))
         cases.append(("r5_line_count_no_path", HDR + row("(7 lines) `python3 tools/lc.py --selftest` → `LC_SELFTEST pass=1 fail=0`",
                                                          entry="`python3 tools/lc.py`"), 1, False, "unparsed"))
+        # round 49 (Mo49ExecArmsBindUnlanded): an over-pin is a mismatch too — every other
+        # arm pins fewer lines than the file has, so `nl != num` flipped to `nl > num`
+        # survived the 65-arm suite (round-48 w2 R48MutV3Bind m_r5a).
+        cases.append(("r5_line_count_overpin_mismatch", HDR + row(
+            "`python3 tools/lc.py --selftest` → `LC_SELFTEST pass=1 fail=0` (43 lines)",
+            entry="`python3 tools/lc.py`"), 1, False, "mismatch"))
         cases.append(("r6_trunc_digest_match", HDR + row(good + " at sha256 `%s…` of `tools/foo.py`" % digest[:12]), 1, True, None))
         cases.append(("r6_trunc_digest_mismatch", HDR + row(good + " at sha256 `%s…` of `tools/foo.py`"
                                                             % (digest[:11] + ("0" if digest[11] != "0" else "1"))), 1, False, "mismatch"))
@@ -959,6 +965,12 @@
         cases.append(("r10_digest_binds_to_nearest_preceding_path", HDR + row(
             "`python3 tools/foo.py --selftest` → `FOO_SELFTEST pass=3 fail=0` at sha256 `%s` of `tools/foo.py`"
             % digest), 1, True, None))
+        # round 49 (Mo49ExecArmsBindUnlanded): the digest binds to the nearest *preceding*
+        # path, never to one written after it — `st[:dm.start()]` flipped to `st[dm.end():]`
+        # survived the 65-arm suite (round-48 w2 R48MutV3Bind m_r10b).
+        cases.append(("r10_digest_binds_to_nearest_preceding_path_not_following", HDR + row(
+            "`python3 tools/foo.py --selftest` → `FOO_SELFTEST pass=3 fail=0`; sha256 `%s` of `tools/slow.py`"
+            % slow_digest, entry="`python3 tools/foo.py`"), 1, False, "mismatch"))
         # R9a (D5): a tally-looking token in a cell other than the self-test cell.
         cases.append(("r9a_tally_in_pinned_values_cell", HDR + row(
             "`python3 tools/foo.py --selftest` → `FOO_SELFTEST pass=3 fail=0`",
```

## Integrity

- `sha256sum` after every run: `tools/mori-unlanded-check.py e6695e04026b…6a2b85`,
  `tools/mori-pin-check.py 85a89a3b6ba4…f82e1`,
  `controls/tool-r48-merged-witness.py c30ab6232893…9c9f0` — all identical to the values read
  before the first run, and identical to the freeze receipts' reference digests.
- Arm copies: `unlanded-arms.py 612d50c1590d…6109`, `witness-arms.py 305c904729517a…52a0`.
- `git status --porcelain=v1 -- tools/ .ufo/ corpus/ SKILL.md` → 13 lines, all `??` under
  `.ufo/waves/round-40/scratch/mori-conform-selftest-*` (pre-existing, already present at the
  21:39 status, created by a conform selftest that is not part of this seat) plus the L1's
  `?? .ufo/waves/round-49/w1-dispatch.json` and `?? .ufo/waves/round-49/w1-spec.json`. No `M`,
  `A`, `D` or `R` record; `tools/`, `corpus/` and `SKILL.md` clean. HEAD `0df17b7b` unchanged.
- Read-only git only in the lane (`log`, `status`); every write-bearing git call was
  `git -C "$D" …` in a scratch fixture after the toplevel identity check. No jj command ran.
- No tool installed or upgraded (none needed); `pacman` not run. No credential material read.
- Receipts kept in the scratch dir: `receipt-unlanded-13.txt`, `receipt-unlanded-17.txt`,
  `receipt-witness-65.txt`, `receipt-witness-67.txt`, `diff-unlanded-arms.patch`,
  `diff-witness-arms.patch`, `probe-arms.py`, plus `*.py` mutants.

## Limits

- **u6 is an equivalent mutant, not a survivor.** `return sorted(found, …)` → `return found` cannot
  be killed: `git status --porcelain=v1 -z --untracked-files=all` emits records already sorted by
  path. Two probes agree byte-for-byte (4-path untracked set created z,a,m,q; and a mixed set with
  a staged rename plus a modification plus an untracked file — raw `-z` order `M corpus/b.md`,
  `R corpus/c.md`, `?? tools/zz.py`, pristine and mutant output identical). No arm text can
  distinguish it while the tool reads git status; if the tool ever gains a second input path the
  sort becomes load-bearing and an arm would be needed.
- **Copy records (`C `) remain unexercised.** `xy[0] in "RC"` covers both; `git status` does not
  detect copies under default config, so no fixture can build a `C` record without changing the
  tool's git invocation. Reported rather than armed.
- Observed but unarmed behaviour (not required by the docstring's wording): an in-scope source
  renamed out of scope (`git mv corpus/x.md notes/x.md`) prints `UNLANDED=clean round=8` (the
  record path is the destination) and an unstaged deletion prints `unlanded .D corpus/d.md`. Both
  behaviours are the tool's; whether they are the intended contract is an L1 decision, so no arm
  pins them.
- Single-point mutants only, one per named rule; compound weakenings are untested.
- The new witness arms were added to a **copy of a control**, not to `tools/mori-pin-check.py`.
  Whether the merged witness lands as v4, and whether `count-c1.py` still reaches `C1=met` with
  these two extra arms in its selftest, is out of this seat's scope and **UNVERIFIED** (the counter
  does not run the tool's `--selftest` per the contract, so no scoring effect is expected).
- Seats do not judge; the L1 integrates both diffs and owns the post-integration gate.

## Findings

| # | severity | finding | file / line |
|---|---|---|---|
| F1 | MED | The unlanded check's selftest had no rename arm: deleting the `-z` rename-source skip fabricated `unlanded NO E.md` on a clean tree while the suite still printed 13/13. Now killed by `rename_source_not_listed` (17-arm copy). | `tools/mori-unlanded-check.py:68-69` (skip); arm added in diff |
| F2 | MED | The 50-path cap was never reached by any arm, so removing the cap or moving it to 51 changed the documented "at most 50" contract silently (`pass=13 fail=0` both). Now killed by `list_cap_50_of_60`. | `tools/mori-unlanded-check.py:30,80`; arm added in diff |
| F3 | MED | `modified_tracked_report_exit1` is near-vacuous: its `or "A.md" in l` disjunct is satisfied by any listing of the modified file, so the rendered status pair was never pinned and `xy.replace(" ", ".")` could be dropped (survivor u5). Now killed by `modified_status_rendered_with_dot`. | `tools/mori-unlanded-check.py:127`; arm added in diff |
| F4 | MED | The bind rules had no over-pin arm: every line-count arm pins fewer lines than the file has, so `nl != num` → `nl > num` accepted a pin claiming 43 lines for a 42-line file (`PIN_CHECK=met`). Now killed by `r5_line_count_overpin_mismatch`. | `tool-r48-merged-witness.py:596` (and `tools/mori-pin-check.py` counterpart); arm added in diff |
| F5 | MED | The full-digest binding had no following-path arm: `st[:dm.start()]` → `st[dm.end():]` bound a digest to the path written after it (`PIN_CHECK=met`). Now killed by `r10_digest_binds_to_nearest_preceding_path_not_following`. | `tool-r48-merged-witness.py:661`; arm added in diff |
| F6 | LOW | `sorted()` in `check()` is redundant against git's already-sorted status output; an unsort mutant survives and is behaviourally equivalent, so the suite cannot and need not kill it. | `tools/mori-unlanded-check.py:72` |
| F7 | LOW | The `C` (copy) branch of the rename/copy skip is unexercised and not constructible with the tool's current git invocation. | `tools/mori-unlanded-check.py:68` |
