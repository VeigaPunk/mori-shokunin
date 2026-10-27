# Mo53MutC2Counter — mutation probe of the frozen round-53 C2 counter

Seat: mutation-tester. Scope: single-point mutants of `.ufo/waves/round-53/count-c2.py` (its REF function and
its harness), each in its own scratch copy, scored with the assigned detector — the counter's own
`--selftest` (killed iff exit code != 0). Two further arms were added for every survivor: the full counter run
against the real `tools/mori-commit-runway.py` at the landed revision, and a defective tool in a throwaway
fixture repo. I judged nothing, integrated nothing, changed no counter, predicate, fixture or SKILL byte, and
ran no other lane's instrument.

Interpreter and inputs: `python3` 3.14.8. Reads: `.ufo/waves/round-53/count-c2.py`, `.ufo/waves/round-53/contract.md`,
`tools/mori-commit-runway.py`, the lane git objects (`git show`/`git archive`/`rev-parse` only). No tool was
installed or upgraded (nothing was needed; the pacman guard was not touched).

Scratch: `/fast/scratch/hyaku/mori-r53/Mo53MutC2Counter/`, with `TMPDIR=/fast/scratch/hyaku/mori-r53/Mo53MutC2Counter/tmp`
for every run; removed after this report. `bash scripts/hyaku/disk-guard.sh status` read before the runs:
`/fast/scratch/hyaku 25% free 609.6G`.

## Baseline (pristine bytes, before any mutation)

```
$ git show f4da3fd400fa88a6db8ea544a4f7045c15d2410e:.ufo/waves/round-53/count-c2.py | sha256sum
5684b69f7ae9030b33195490f10c650c3c123909f0d61e182b6c1cadfbb168c5  -
$ sha256sum .ufo/waves/round-53/count-c2.py
5684b69f7ae9030b33195490f10c650c3c123909f0d61e182b6c1cadfbb168c5  .ufo/waves/round-53/count-c2.py
$ TMPDIR=…/tmp python3 -I -B …/base/count-c2.py --selftest
C2_SELFTEST pass=30 fail=0                     # exit 0, 25.2 s
$ TMPDIR=…/tmp python3 -I -B …/base/count-c2.py 2a4213bf8da72f7cd78189baa5bb9be825dca1df \
      --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch …/arm2/control
C2=met tool=present selftest=pass n=23 fixtures=80 agree=80 disagree=0 registry=ok live=ok \
rev=2a4213bf8da72f7cd78189baa5bb9be825dca1df   # exit 0, 4.3 s
```

A baseline failure would have made the probe inconclusive; it did not fail, so the detector is live.

## Method

* **Arm 1 (assigned detector).** Copy the pristine bytes to `…/mutants/<id>/count-c2.py`, apply exactly one
  textual mutation, gate it with `ast.parse` (a syntax break is recorded as *invalid build*, never as a kill),
  then `python3 -I -B <copy> --selftest` with `TMPDIR` inside that mutant's directory. `rc != 0` = killed.
  Every mutant's own directory is deleted after scoring.
* **Arm 2 (fixture arm against the real tool).** For each arm-1 survivor:
  `python3 -I -B <mutant> 2a4213bf… --repo <lane> --scratch <dir>`. Caught iff the counter prints `C2=unmet`.
  This is the only arm in which the mutated counter is compared with a tool it does not contain.
* **Arm 3 (defect demonstration).** For the survivors whose meaning is "a check was deleted", a defect is
  planted in the tool inside a throwaway repo — `git archive 2a4213bf… | tar -x`, one edit, `git init -q` in the
  extracted tree, `git rev-parse --show-toplevel` asserted equal to that tree, one commit as
  `Mo53MutC2Counter <mut@localhost>` — then the pristine counter and the mutant counter score the same repo.
  A hole is demonstrated iff pristine = unmet and mutant = met.
* **Arm text.** For every survivor that is a coverage gap, the proposed additional selftest check is applied to
  *both* the mutant copy and the pristine copy: the arm is accepted only if it kills the mutant (`rc != 0`) and
  leaves the pristine counter green (`rc == 0`).

## Table — 30 single-point mutants (29 behaviour-bearing, 1 invalid build)

`arm1` = the counter's `--selftest`; `arm2` = full counter vs the landed tool (run only for arm-1 survivors);
`—` = not applicable because arm 1 already killed it.

| id | single-point mutation (counter line) | arm1 | arm2 | arm that kills it |
|---|---|---|---|---|
| M01_band_le_to_lt | `low = usable_kb <= band_kb` → `<` (L141) | survived | caught | arm2 only |
| M02_batch_floor_32 | `max(cpus*2, 32)` → `cpus*2` (L136) | survived | missed | **none** |
| M03_reserve_drop_user | `reserve_kb` = admin only (L139) | killed `ref_mode2_ok,ref_mode2_low,harness_mutant_no_band_unmet,harness_memoriser_unmet` | — | arm1 |
| M04_limit_consistent_true | `limit_consistent` = `True` (L128) | killed `ref_limit_mismatch,harness_mutant_no_hugetlb_unmet` | — | arm1 |
| M05_type_check_dropped | `type(got[k]) is not type(want[k])` dropped (L284) | survived | missed | **none** (arm text below) |
| M06_exit_code_check_dropped | `if rc != code:` block dropped (L285) | survived | missed | **none** (arm text below) |
| M07_selftest_floor_1 | `MIN_SELFTEST = 12` → `1` (L44) | killed `harness_selftest_floor_unmet` | — | arm1 |
| M08_n_eq_total_dropped | `m.group(1) == m.group(2)` dropped (L334) | killed `harness_selftest_partial_unmet` | — | arm1 |
| M09_seeded_not_run | `N_SEEDED = 64` → `0` (L45) | killed `seeded_varies,harness_witness_met,harness_memoriser_unmet` | — | arm1 |
| M10_live_leg_skipped | `live_s = live_check(tool) if live else "skip"` → `"ok"` (L348) | survived | missed | **none** (arm text below) |
| M11_registry_check_dropped | registry loop removed (L353) | killed `harness_witness_met` | — | arm1 |
| M12_tool_absent_not_failing (v1) | `failed.append("tool_absent")` deleted (L329) | *invalid build* `IndentationError` | — | not counted |
| M12b_tool_absent_not_failing | same, replaced by `pass` (L329) | killed `harness_absent_unmet` | — | arm1 |
| M13_batch_floor_max_removed | outer `max(...)` removed (L136) | killed `ref_batch_floor` | — | arm1 |
| M14_registry_relaxed_no_selftest | registry row need not name `--selftest` (L353) | survived | missed | **none** (arm text below) |
| M15_enforced_always_true | `enforced=(mode == 2)` → `True` (L125) | survived | caught | arm2 only |
| M16_present_count_off_by_one | `n += hi - lo + 1` → `hi - lo` (L89) | killed `ref_mode2_ok,ref_small_batch,ref_batch_floor,ref_present_parse` | — | arm1 |
| M17_dup_meminfo_key_ok | duplicate-key `return None` removed (L65) | killed `ref_unknown_dup` | — | arm1 |
| M18_mode2_in_unknown | `mode not in (0, 1, 2)` → `(0, 1)` (L114) | killed 9 checks (all mode-2 REF checks, `fixture_verdict_mix`, 2 harness) | — | arm1 |
| M19_mode1_verdict_ok | `COMMIT_UNLIMITED` → `COMMIT_OK` (L130) | killed `ref_mode1,fixture_verdict_mix` | — | arm1 |
| M20_headroom_sign_flip | `CommitLimit - Committed_AS` reversed (L126) | killed 6 checks (`ref_host_limit`, mode 2, mode 1, 2 harness) | — | arm1 |
| M21_page_kb_pow2_guard_dropped | `page_kb & (page_kb-1)` guard dropped (L106) | survived | missed | **none** (arm text below) |
| M22_n_seeded_16 | `N_SEEDED = 64` → `16` (L45) | killed `harness_witness_met,harness_memoriser_unmet` | — | arm1 |
| M23_cpus_positive_guard_dropped | `cpus < 1` dropped (L111) | survived | missed | **equivalent mutant** |
| M25_limit_swap_term_dropped | `allowed += swap_pages` removed (L123) | killed `ref_host_limit,ref_kbytes` | — | arm1 |
| M26_kbytes_branch_never | `if vmv["overcommit_kbytes"]:` → `if False:` (L119) | killed `ref_kbytes` | — | arm1 |
| M27_hugetlb_not_subtracted | `(ram_pages - huge_pages)` → `ram_pages` (L122) | killed `ref_hugetlb` | — | arm1 |
| M28_live_fields_trimmed | live field tuple loses `limit_consistent` (L315) | survived | missed | **none** (arm text below) |
| M32_islink_guard_dropped | `and not os.path.islink(tool)` dropped (L325) | survived | missed | **none** (arm text below) |
| M34_seed_constant | `random.Random(int(seed_hex,16))` → `Random(0)` (L203) | killed `seeded_varies` | — | arm1 |

Totals: **18 killed by arm 1**, **11 survivors**, of which arm 2 caught **2** (M01, M15) and is blind to **9**.
One row (M12 v1) is an invalid build of my own making — deleting the only statement of an `else:` suite — and is
excluded from the kill count; it was re-run as M12b, which arm 1 kills. No survivor was counted as killed on a
crash: every kill above is a named `FAIL <check>` line with the counter's own `C2_SELFTEST pass=n fail=m`
summary, never a traceback.

## Why arm 1 is blind to most REF mutants (structural)

`REF_TOOL` (the witness tool used by the harness checks) does
`sys.path.insert(0, os.environ["C2_COUNTER_DIR"])` and imports the counter module, and `selftest()` sets
`C2_COUNTER_DIR = os.path.dirname(os.path.abspath(__file__))` — i.e. the copy under test. A REF mutation is
therefore *in both* the reference and the witness, so the 80-fixture comparison cancels it. Arm 1 can only kill
a REF mutant through the 19 non-harness assertions (`ref_host_limit` … `fixture_verdict_mix`). That is exactly
what the table shows: M01 and M15 were invisible to arm 1 and were caught only when a second, independent
reading (the real tool) was compared. The counter's `--selftest` also never executes
`tools/mori-commit-runway.py` at all; the real tool is exercised only by the full run.

## The nine mutants invisible to both arms

### 1. M06 — the exit code is never compared (predicate clause loses its only check)

Demonstrated end to end (arm 3, repo `/fast/scratch/…/demo/D1_exit0/tree`, rev `60d338b4`): the tool prints the
reference JSON but `return 0` instead of `return code` at the CLI boundary (`tools/mori-commit-runway.py:312`).

```
pristine counter: C2=unmet … fixtures=80 agree=51 disagree=29 registry=ok live=ok failed=fixtures   (rc 1)
                  disagree mode2-low-negative: exit want=1 got=0
M06  counter:     C2=met   … fixtures=80 agree=80 disagree=0  registry=ok live=ok                    (rc 0)
```

So the frozen predicate's clause "exits with the reference exit code" can be deleted from the counter and a tool
that never exits 1 still reads `C2=met`. The live leg does not cover it: it only asserts `rc in (0, 1)`, never
that `rc` corresponds to the verdict.

### 2. M05 — the field type check is never exercised

Same construction (`demo/D2_enforced_int/tree`, rev `7e64cf91`): the tool prints `enforced` as `1`/`0` instead of
`true`/`false` — value-equal under `==`, type-different.

```
pristine counter: C2=unmet … agree=15 disagree=65 failed=fixtures
                  disagree host-mode0-over: enforced want=False got=0
M05  counter:     C2=met   … agree=80 disagree=0                                                  (rc 0)
```

The counter's own `string_numbers` mutant cannot stand in for this arm: `"12" != 12` is already caught by the
value comparison, so no existing check reaches the type clause.

### 3. M14 — the `--selftest` half of the registry row is never required

`demo/D3_no_selftest_word/tree` (rev `023d6326`): SKILL.md says `--self-test` everywhere, so no row names the
tool *and* `--selftest`.

```
pristine counter: C2=unmet … registry=bad failed=registry    (rc 1)
M14  counter:     C2=met   … registry=ok                     (rc 0)
```

The predicate requires "a table row naming `tools/mori-commit-runway.py` **and** `--selftest`"; with this
mutant the second half is silently dropped, and the counter's `harness_registry_unmet` check cannot see it
because its fixture SKILL text ("no row here") fails both halves at once.

### 4. M02 — the 32-page floor of the batch rule is dead in the fixture domain

Measured over the 80 fixtures of this revision (`frozen_fixtures() + seeded_fixtures(sha256(rev))`): of the 44
mode-2 fixtures, the 42 with a parseable CPU list all have `ram_pages // cpus // 256 >= 32`, so
`max(cpus*2, 32)` never binds and `cpus*2` is indistinguishable — hence arm 2 misses it too, even though
`tools/mori-commit-runway.py:182` carries the same floor. Freezing the floor instead of the region:
a fixture with 64 MiB and 4 CPUs gives `16384//4//256 = 16 < max(8,32) = 32`.

### 5. M21 — the page-size guard is dead in the fixture domain

`page_kb` takes only `{4, 16, 64}` across all 80 fixtures (frozen and seeded), every one a power of two, so
dropping `page_kb & (page_kb - 1)` (`count-c2.py:106`) cannot be observed. The real tool keeps the guard
(`tools/mori-commit-runway.py:307`), so the divergence exists but no fixture reaches it.

### 6. M23 — equivalent mutant (unreachable guard), not a coverage gap

`parse_present` returns `hi - lo + 1 >= 1` for every part of every list it accepts, so `cpus < 1`
(`count-c2.py:111`) cannot be true while `cpus is not None`; the real tool's `parse_cpulist`
(`tools/mori-commit-runway.py:115-126`) likewise raises instead of returning 0. No arm can exist; recorded as
equivalent, not as a hole.

### 7. M10 / M28 — the live leg has no coverage in arm 1 at all

`harness_live_witness` asserts `live in ("ok", "error")` (`count-c2.py:553`), so a host-dependent "error" is a
pass, and the check calls `live_check` directly rather than through `evaluate_tree`. Consequence: replacing the
live leg inside `evaluate_tree` with the constant `"ok"` (M10, L348) leaves all 30 checks green, and trimming
the compared field list (M28, L315) does the same. In both cases the full run still prints `live=ok`, and arm 2
cannot distinguish them because this host's live leg passes anyway.

### 8. M32 — "regular file" is not enforced against a symlink

No fixture or repo in the harness uses a symlinked tool, so dropping `and not os.path.islink(tool)`
(`count-c2.py:325`) is invisible; the frozen predicate says "is a regular file". Severity is low because the
landed tree has a plain file.

## Arm text that kills each non-equivalent survivor (validated)

Each block below was inserted into the counter's `selftest()` (anchor noted), then run on the **mutant** and on
the **pristine** bytes. Every arm: mutant → `rc 1` with exactly the named `FAIL`, pristine → `rc 0`,
`C2_SELFTEST pass=31 fail=0`. Nothing here was applied to the frozen counter.

`M02`, inserted before `check("frozen_count", …)`:

```python
    # arm: the 32-page floor of the batch rule binds. 64 MiB, 4 CPUs, mode 2: ram 16384 pages,
    # 16384//4//256 = 16 < max(2*4, 32) = 32 -> batch 32, band 32*4*4 = 512.
    code, o = ref_for(mk("floorbind", 65536, 0, 1000, 2, present="0-3"))
    check("ref_batch_floor_binds", o["batch_pages"] == 32 and o["band_kb"] == 512)
```
→ mutant fails `ref_batch_floor_binds` (pristine reads `batch_pages=32 band_kb=512`; M02 reads `16/256`).

`M21`, same anchor:

```python
    # arm: a page size that is not a power of two is UNKNOWN, never evaluated.
    code, o = ref_for(mk("pk3", 1048576, 0, 1000, 2, page_kb=3))
    check("ref_page_kb_non_pow2", code == 2 and o["verdict"] == "COMMIT_UNKNOWN")
```
→ mutant fails `ref_page_kb_non_pow2` (pristine `code=2 COMMIT_UNKNOWN`; M21 `code=0 COMMIT_OK`).

`M10`, inserted after `check("harness_live_witness", …)`:

```python
        # arm: the live leg must be wired into evaluate_tree, not assumed ok.
        met, line, _ = evaluate_tree(t, "11" * 32, skill, live=False)
        check("harness_live_skip_reported", "live=skip" in line)
```
→ mutant fails `harness_live_skip_reported` (with `live=False` the pristine line says `live=skip`, the mutant
says `live=ok`).

`M28`, same anchor:

```python
        # arm: live_check must reject a tool that misreports a field the counter itself reads.
        lbad = REF_TOOL.replace(
            "print(json.dumps(out)); sys.exit(code)",
            "out['limit_consistent'] = not out['limit_consistent']; print(json.dumps(out)); sys.exit(code)")
        check("harness_live_detects_misreport",
              live_check(os.path.join(tree_with(lbad, "livebad"), TOOL)) == "bad")
```
→ mutant fails `harness_live_detects_misreport`; host-independent, because the synthetic tool derives its reading
from the counter itself and then corrupts one stable field.

`M32`, same anchor:

```python
        # arm: the predicate says regular file -- a symlinked tool is absent, not present.
        sym = tree_with(None, "symlink")
        with open(os.path.join(sym, "witness.py"), "w") as f:
            f.write(REF_TOOL)
        os.symlink("../witness.py", os.path.join(sym, TOOL))
        met, line, _ = evaluate_tree(sym, "11" * 32, skill, live=False)
        check("harness_symlink_absent_unmet", (not met) and "tool_absent" in line)
```
→ mutant fails `harness_symlink_absent_unmet`.

`M06`, two edits — one more `MUT` branch in `REF_TOOL` and one more element in the mutant tuple at L533:

```python
if MUT == "exit_only":
    code = 0                       # JSON untouched: only the exit code deviates
...
        for mut in ("mode_blind", "no_band", "no_hugetlb", "string_numbers", "exit_only"):
```
→ mutant fails `harness_mutant_exit_only_unmet`.

`M05`, two edits, same shape:

```python
if MUT == "enforced_int" and out["enforced"] is not None:
    out["enforced"] = int(out["enforced"])      # 1/0 instead of true/false, value-equal
...
        for mut in ("mode_blind", "no_band", "no_hugetlb", "string_numbers", "enforced_int"):
```
→ mutant fails `harness_mutant_enforced_int_unmet`.

`M14`, one edit at the same anchor:

```python
        # arm: the registry row must name the tool AND --selftest.
        norow = "| commit runway | gate | `python3 -I -B tools/mori-commit-runway.py --meminfo PATH` |\n"
        met, line, _ = evaluate_tree(t, "11" * 32, norow, live=False)
        check("harness_registry_needs_selftest", (not met) and "registry" in line)
```
→ mutant fails `harness_registry_needs_selftest`.

`M23` has no arm: the guard is unreachable (equivalent mutant).

## Context for the survivors (measured, not inferred)

* `usable_kb == band_kb` exactly in two of the 80 fixtures — frozen `mode2-band-edge-low` and seeded
  `seeded-53` — so the `<=` boundary is exercised by the fixture arm, but only against the real tool, which is
  why M01 needs arm 2.
* Fixture domain at this revision: modes `{2: 44, 0: 16, 1: 15, 3: 4, missing: 1}`; `page_kb {4, 16, 64}`;
  `cpus {1, 2, 4, 6, 8, 12, 16, 32, 48, 64, 96, 128, 256}`; two fixtures carry an unparseable `present`
  (`unknown-bad-present`, `seeded-23`).
* The counter's `--selftest` has 30 checks; the tool it scores at the landed revision reports `PASS 23/23`
  (floor `MIN_SELFTEST = 12`).

## Observed tree drift during this probe (not caused by me)

The lane worktree moved while the probe ran. When I read the files, `tools/mori-commit-runway.py` was the landed
316-line blob (`sha256 80cb169650bf02578439703bc006173aab7b759ff9cf57337611b27164676156`, the same bytes as
revision `2a4213bf…` and as HEAD `95cf78ee…`). At `2026-10-26 23:14:17 -0300` the worktree copy became 429 lines,
`sha256 82924be72e7784dd76d16a53deebfbbc96aed5e2936b162912b5e20f10506506`, and `git status --porcelain
--untracked-files=no` now reports ` M SKILL.md`, ` M corpus/knowledge/commit-runway-read-r53.md`,
` M tools/mori-commit-runway.py` (`git diff --stat`: 142 insertions, 27 deletions, HEAD unchanged at
`95cf78ee…`). `.ufo/waves/round-53/count-c2.py` never changed: `5684b69f…`, 565 lines, at the freeze commit, at
HEAD and in the worktree throughout.

Every reading in this report was produced from the revision's own bytes (`git archive 2a4213bf…`), so it
describes the same bytes as `evidence/c2-at-data.txt`; nothing here was measured on the edited worktree, and I
touched none of those three files.

## Restoration evidence

* The lane file was only read: sha256 `5684b69f7ae9030b33195490f10c650c3c123909f0d61e182b6c1cadfbb168c5`
  before the first mutant and the same value after the last; it equals the blob in the freeze commit
  `f4da3fd400fa88a6db8ea544a4f7045c15d2410e` and in HEAD. `git status --porcelain` in the lane lists no file
  I created (only the orchestrator's `w1.ready*`, `w1/`, `evidence/selftests/`).
* Every mutant lived in `/fast/scratch/hyaku/mori-r53/Mo53MutC2Counter/mutants*/<id>/` (or `arms*/`, `demo/`,
  `arm2/`), each with its own `tmp/`; each mutant's sha256 is recorded in the driver output
  (for example M01 `35299107d1a992037b25065f6cf61be1cbf6428ccf2ba3d75f2a55735c4f505d`,
  M06 `754b258ae187de992141cd1280858b004671fb39337fa03bbb35b35a913fe0d2`), against the pristine
  `5684b69f…`. No mutant was ever written next to the frozen file.
* Throwaway fixture repos (`demo/*/tree`) were `git init`-ed inside the extracted tree, the toplevel asserted
  before the single commit, all commits authored by `Mo53MutC2Counter <mut@localhost>`; nothing was added,
  committed, stashed, checked out or reset in the lane or the fleet root.
* The whole scratch tree `/fast/scratch/hyaku/mori-r53/Mo53MutC2Counter/` (including `base/`, `mutants*/`,
  `arms*/`, `demo/`, `arm2/`, `tmp/`) was removed after this report was written; nothing it cites lives there
  any more, the text above is the copy of record.

## Named limits of this probe

* The assigned detector is the counter's own self-test, so these verdicts measure the counter's
  self-knowledge, not kernel correctness: a survivor says "the counter would not notice", not "the claim is
  false". The landed claim was re-measured only once, as a control, at `2a4213bf…`.
* Mutations are textual single points; a semantic rewrite of a rule (for example changing what `band_kb` means)
  is out of scope, as is anything that needs a different kernel reading.
* Arm 3's defective tools are synthetic and the repos were disposable; they demonstrate that a check is load
  bearing, not that any real tool ever carried those defects.
* The seeded fixture set depends on the scored revision, so the demonstration repos had different seeded
  fixtures from the landed one; the frozen 16 are identical in both.
* Two of my own constructs were invalid before being fixed (M12 v1 syntax, demo repo rooted one level above the
  extracted tree) — both are disclosed above rather than scored.

## Findings

1. **HIGH — `count-c2.py:285` (`.ufo/waves/round-53/count-c2.py`): the exit-code comparison in `compare()` carries
   no test.** Mutant M06 (delete `if rc != code: …`) survives the counter's `--selftest` and the full run, and a
   planted tool that prints the exact reference JSON while always exiting 0 is scored `C2=met … agree=80` by the
   mutant (pristine: `C2=unmet … agree=51 disagree=29`, first disagreement `exit want=1 got=0`). The predicate
   clause "exits with the reference exit code" is therefore unverified by anything. Routed to round 54; the
   validated arm is in the "Arm text" section.
2. **MED — `count-c2.py:284`: the field type comparison is unreachable by the existing mutants.** M05 (drop
   `type(got[k]) is not type(want[k])`) survives both arms, and a tool printing `enforced` as `1`/`0` is scored
   `C2=met agree=80` by the mutant against `C2=unmet agree=15 disagree=65` for the pristine counter. The frozen
   `string_numbers` mutant cannot cover it because `"12" != 12` is already a value difference.
3. **MED — `count-c2.py:353`: the registry check does not require the `--selftest` word it is specified to
   require.** M14 survives both arms; a SKILL.md whose rows name the tool but never `--selftest` is scored
   `registry=ok C2=met` by the mutant against `registry=bad C2=unmet` for the pristine counter. The frozen
   predicate names both halves of the row.
4. **MED — `count-c2.py:348` and `:315` with `:553`: the live leg has no coverage inside the counter's
   `--selftest`.** `harness_live_witness` accepts `"error"` and bypasses `evaluate_tree`, so replacing the live
   leg with a constant `"ok"` (M10) or trimming the compared field list (M28) leaves all 30 checks green while
   the full run still prints `live=ok`.
5. **MED — `count-c2.py:136`: the 32-page floor of the batch rule never binds in any fixture of this revision.**
   All 42 parseable mode-2 fixtures have `ram_pages // cpus // 256 >= 32`, so M02 (floor → `cpus*2`) survives
   both arms even though `tools/mori-commit-runway.py:182` implements the floor; the floor is covered only by
   `ref_batch_floor` at L484, which uses 64 CPUs where `2*cpus` alone already exceeds 32.
6. **LOW — `count-c2.py:106`: the page-size power-of-two guard is never exercised.** Fixture `page_kb` is
   `{4, 16, 64}` only, so M21 survives both arms while the real tool keeps the same guard at
   `tools/mori-commit-runway.py:307`.
7. **LOW — `count-c2.py:325`: "regular file" is not enforced against a symlink.** M32 (drop
   `not os.path.islink(tool)`) survives both arms; no fixture or repo uses a symlinked tool, although the frozen
   predicate says the tool is a regular file.
8. **LOW — `count-c2.py:111`: `cpus < 1` is an unreachable guard (equivalent mutant).** `parse_present` cannot
   return 0 for an accepted list and the real tool raises instead, so M23 has no possible arm; recorded so no
   later round mistakes it for a covered condition.
9. **LOW (structural, `count-c2.py:426-455` with `:515`): the counter's self-test cannot see REF mutations
   through its fixtures.** `REF_TOOL` imports the counter under test (`C2_COUNTER_DIR`), so a REF mutation is
   present on both sides of the 80-fixture comparison; only the 19 non-harness assertions can kill a REF
   mutant, and the real tool is never executed by `--selftest`. Evidence: M01 and M15 were invisible to arm 1
   and were caught only when the independent real tool was compared. This is a named limit of the frozen
   counter, not a defect of the landed data.
10. **MED (observed drift, not mine) — the worktree no longer equals the revision C2 is measured at.** As of
    `2026-10-26 23:14:17` `tools/mori-commit-runway.py` is `82924be7…` (429 lines, uncommitted) while the
    revision `2a4213bf…` — and HEAD `95cf78ee…` — carry `80cb1696…` (316 lines); `SKILL.md` and
    `corpus/knowledge/commit-runway-read-r53.md` are also modified and uncommitted. Every verdict in this report
    was taken from `2a4213bf…` bytes, so none of them is affected; but a re-score of C2 from the worktree would
    measure different bytes than `evidence/c2-at-data.txt`, so the correction needs its own commit before any
    counter run is treated as the claim's reading.
