# round 45 · wave 1 · ExecControlReceipts

Seat: leaf executor (`ExecControlReceipts`). Assignment: measure the do-nothing controls and
the entering-tip before-states for C1/C2/C3 at `554ff416`, plus the gate-registry population
audit, the round-44 C3 TMPDIR witness, and the census baseline. No lane edit was made except
the eight receipt files listed below. No tool was installed or upgraded.

Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin` (worktree HEAD `3ad8faaa` = entering tip
`554ff416` + the round-45 freeze commit). All runs used `python3` 3.14.8, read-only git, and a
scratch `TMPDIR` under `.ufo/waves/round-45/tmp/ExecControlReceipts/`.

## 1. The table — claim → command → verdict → rc

Every row is an executed command; `E/` = `.ufo/waves/round-45/evidence/`.

| claim | command (absolute paths elided to the lane) | verdict | rc | receipt |
|---|---|---|---|---|
| C1 do-nothing | `python3 .ufo/waves/round-45/count-c1.py 554ff416 --repo $LANE --ledger .ufo/waves/round-45/figures.tsv --other-rev 3ad8faaa --witness-dir .ufo/waves/round-45/fixtures/witnesses` | `C1=unmet` (`ledger_present` FAIL; `witnesses=3/3`) | 1 | `E/control-c1.txt` |
| C2 do-nothing | `python3 .ufo/waves/round-45/count-c2.py 554ff416 --repo $LANE` | `C2=unmet` (9 FAIL: auditor_v2, auditor_mode, population_members, tables, unregistered, no_selftest, duplicate, wrong_row, auditor_rc) | 1 | `E/control-c2.txt` |
| C3 do-nothing | `env -u TMPDIR python3 .ufo/waves/round-45/count-c3.py 554ff416 --entering-rev 554ff416 --entry corpus/knowledge/census-cgroup-levels-r45.md --row S473 --repo $LANE --root /home/vgpnk/Projects/shokunin` | `C3=unmet` (`entry_present`, `rows_present`, `readme_row` FAIL; `entering_absent` PASS; `census_ok` PASS exit=0) | 1 | `E/control-c3.txt` |
| C2 registry population | `python3 tools/mori-gate-registry.py --rev 554ff416 --audit-all --repo $LANE` (v2) | `REGISTRY=unmet` `registered=29 unregistered=3 no_selftest=4 duplicate=0 wrong_row=0 tables=7` | 1 | `E/registry-audit-all.txt` |
| C1 comparison (round 44) | `python3 .ufo/waves/round-44/count-c1.py 554ff416 --repo $LANE` | `C1=met mismatches=0` (16 rows, 5 classes) | 0 | `E/control-r44-c1.txt` |
| C2 comparison (round 44) | same counter + 3 × `--counter .ufo/waves/round-44/count-c*.py`, **default** `--mutants-dir` | `C2=unmet` (`mutant_kill` FAIL: three mutants "absent") | 1 | `E/control-r44-c2.txt` §run A |
| C2 comparison (round 44) | as above + `--mutants-dir .ufo/waves/round-44/fixtures/mutants` | `C2=met` (all 5 checks PASS) | 0 | `E/control-r44-c2.txt` §run B |
| C3 comparison (round 44) | `TMPDIR=<fresh dir under round-45/tmp> python3 .ufo/waves/round-44/count-c3.py 554ff416 --entry corpus/knowledge/pid-probe-conclusion-r44.md --row S471 --row S472 --repo $LANE` | `C3=unmet` (`census_ok` FAIL exit=1) | 1 | `E/witness-r44-c3-tmpdir.txt` |
| census baseline | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` | 19 × `W04` + `mori ok … corpus/SOURCES.md` | 0 | `E/census-baseline.txt` |

Instrument digests executed (the instruments were still being written this wave — see §4):

```
d908aa9afaf0dcc8e6cb8695ec6bfdb9091be17b270620403954563f792b6bef  .ufo/waves/round-45/count-c1.py   (08:02:00)
e8ee29eb885270b0aa056617ab1c44fd8663c0b7e680506976bbcd5156959c64  .ufo/waves/round-45/count-c2.py   (07:58:25)
37fd7c24ff52d6aa27f718ef0b0a2f2e4affa7a1cd0ab67c1fa05f028854a98e  .ufo/waves/round-45/count-c3.py
8b82ac999091ebe65e765ed69f759910a57049ff0e7c5c4aa56df9c7168f5832  tools/mori-gate-registry.py        (v2)
9477824d…f83  0095d0c6…047  a12170f1…c68  .ufo/waves/round-44/count-c1|c2|c3.py  (== r44 freeze pins)
3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30  scripts/sources-census.sh
```

## 2. What the controls prove (the kill rules)

- **All three round-45 counters print `unmet` at the entering tip**, so no do-nothing control
  can print `met`: `C1=unmet` (absent ledger; witnesses 3/3 rejected and 3/3 inside the frozen
  floors, `witnesses_vacuous=3/3`), `C2=unmet` (auditor at
  the rev is v1 → no population mode → priced FAIL), `C3=unmet` (entry/row/README absent).
- **C3's novelty gate is green at the tip**: `entering_absent PASS (not in 554ff416…)`. Passing
  Correction 1.3, no earlier round's entry can be recycled as this round's ground.
- **C3's census arm is green with `TMPDIR` unset** (`census_ok census PASS (exit=0)`, census
  sha256 in the verdict line). The round-44 TMPDIR dependence is gone by construction.
- **C2's registry arm is red for a stated reason**, not vacuously: v2 at the same rev reads
  `tables=7 registered=29 unregistered=3 no_selftest=4 duplicate=0 wrong_row=0`.

## 3. The comparison arms (before-states of the old gates)

1. **r44 C1 prints `met` at the entering tip** over its own honest ledger, but it cannot see the
   predicate the round adds: no `--other-rev`/`CONST=` (a revision-constant ledger also passes),
   no duplicate id/command rejection, no `--witness-dir`, no tip-resolution check beyond
   `rev-parse` being absent from `GIT_VERBS` (`git show HEAD:path` and a hard-coded 40-hex pass;
   `diff` is still a read verb), and `--min-rows/--min-classes` are passed through **unclamped**
   (`count-c1.py:333`). The `met` is exactly the vacuity C1 targets.
2. **r44 C2 needs a hand-repaired default to print `met`.** Its default `--mutants-dir`
   (`fixtures/mutants`, repo-root-relative; `<repo>/fixtures` does not exist) makes all three
   mutants "absent" → `C2=unmet`; with `--mutants-dir .ufo/waves/round-44/fixtures/mutants` it is
   `C2=met`. Even then the `met` covers 3 paths through v1's single-table, substring
   attribution — on the same committed bytes v1 reads 21/14/1 where v2 reads 29/3/4. That
   disagreement is the overstatement C2 measures.
3. **r44 C3's verdict is a function of `TMPDIR`, not of the lane.** Under a plain fresh `TMPDIR`
   it is `C3=unmet` with `census_ok FAIL (exit=1)`. Mechanism, receipted:
   `count-c3.py:133-145` stages the registry at `$TMPDIR/c3-XXXXXX/SOURCES.md` and runs
   `validate --file <staged>`; `sources-census.sh --file` sets the used-by root to
   `realpath(dirname(file)/..)` (`:497-502`) and E11-tests `$dir/$path` (`:567`). So the root is
   `$TMPDIR` itself: green only when `$TMPDIR` is the lane root. Probes in the receipt: same
   staged bytes → 26→0 E11 and `rc=0` once `corpus/`, `tools/`, `SKILL.md`, `SCORECARD.md`,
   `PROVINCE.md` resolve under that root; all three of my witnesses used *different* fresh
   `TMPDIR`s and all three were red.
4. **Item 3 is satisfiable only by v2.** v1 (`743996b1…`, the r44 freeze pin) has no
   population mode: `--audit-all` → argparse `unrecognized arguments`, rc 2, no `REGISTRY=` line.
   v2 landed at 07:46:03 and prints `REGISTRY=unmet` plus the counter line; it also emits
   `mode=population` and `population_digest=4dbf0ca9…` (recorded in the receipt).

## 4. Caveat: the instruments were in flight (state it, don't hide it)

Wave-1 authors were still writing the three counters and the v2 auditor while this seat ran.
Snapshot digests observed, all producing the same verdicts:

| time | c1 | c2 | c3 | gate | verdicts |
|---|---|---|---|---|---|
| 07:41–07:45 | — | — | — | v1 `743996b1` | `--audit-all` rc 2 (v1 has no population mode) |
| 07:45:49 | 84bf5879 | — (not yet written) | de5b625c | v1 `743996b1` | C1 unmet, C3 unmet; `--audit-all` rc 2 |
| 07:48:47 | f80e75ac | d057b67a | 5caea1bb | 3e1cec57 | C1/C2/C3 unmet, REGISTRY unmet |
| 07:50:22 | f80e75ac | d057b67a | 5caea1bb | 5f693651 | same |
| 07:53:04 | f80e75ac | a3b6cb1c | 44aef888 | a82c1fb5 | C3 gained `--entering-rev` (rc 2 without it) |
| 07:56:03 | f80e75ac | 9624c574 | 37fd7c24 | 8b82ac99 | same, stable window 07:55:16–07:56:03 |
| 07:58:25 | f80e75ac | e8ee29eb | 37fd7c24 | 8b82ac99 | same; c2 output identical bar one detail string |
| 08:00:57 | bbe90ce4 | e8ee29eb | 37fd7c24 | 8b82ac99 | same; c1 witness reasons gained `revision_moves` |
| 08:02:00 (receipt) | d908aa9a | e8ee29eb | 37fd7c24 | 8b82ac99 | same; c1 gained a `witnesses_vacuous` floor arm; digest verified before AND after the run |
| 08:02:58 (drift re-check) | a564dcc3 | e8ee29eb | 37fd7c24 | 8b82ac99 | c1 output byte-identical to the 08:02:00 run; digest verified before AND after |

Hand-off: the four receipts name the digest each one executed, and every arm was re-run after
the last byte change observed (c1 moved `f80e75ac → eef2dac6 → bbe90ce4 → d908aa9a` between
08:00:00 and 08:01:48; its digest was re-checked immediately before and after the receipted run
and did not change during it). c2/c3/gate were unchanged over that interval. No verdict changed
at any snapshot. If the freeze pins bytes newer than 08:02:00, re-run with
`bash .ufo/waves/round-45/tmp/ExecControlReceipts/final-run.sh` — it takes all eight arms in
one snapshot and writes `final/meta.txt` (digests + `git status`) beside one `.out`/`.rc` per
arm, so a single command refreshes this whole table.

One transient artefact worth recording so nobody reads it as a finding: at 07:48:47 the shipped
`fixtures/mutants/count-c2.py` **survived** its own selftest (`pass=8 fail=0`); the author
rewrote it at 07:48:53 and every run from 07:50:22 on reports `killed (fail=1)`. Two receipts
(`witness-r44.txt`, `write-scope.txt`) by other seats appeared in `evidence/` while I worked;
I did not touch them.

## 5. Census baseline

`rc=0` with 19 `W04` same-URL warnings and the `mori ok` line, taken at 07:41:44 when
`corpus/SOURCES.md` was still byte-identical to `554ff416` (310 lines both; `S473` absent;
`git status --porcelain corpus/` showing only two untracked files). Confirmed still the
pre-append state at 07:52 and 07:56. The registry append landed after 07:56 and is not covered
by this receipt — a post-append census run must be compared against this baseline, not against
"clean".

Note for whoever repeats item 5: `sources-census.sh` is a **bash** script; invoking it as
`python3 scripts/sources-census.sh …` fails with a `SyntaxError` at line 50 (my first attempt,
rc 1). Run it as `bash …` or execute it directly.

## 6. Files written

```
.ufo/waves/round-45/evidence/control-c1.txt
.ufo/waves/round-45/evidence/control-c2.txt
.ufo/waves/round-45/evidence/control-c3.txt
.ufo/waves/round-45/evidence/control-r44-c1.txt
.ufo/waves/round-45/evidence/control-r44-c2.txt
.ufo/waves/round-45/evidence/registry-audit-all.txt
.ufo/waves/round-45/evidence/witness-r44-c3-tmpdir.txt
.ufo/waves/round-45/evidence/census-baseline.txt
.ufo/waves/round-45/w1/ExecControlReceipts.md            (this report)
.ufo/waves/round-45/tmp/ExecControlReceipts/             (scratch: outputs, final-run.sh, probes)
```

No lane file outside those was created or modified; git in the lane was used read-only.

## 7. Risks / blockers

- **Churn (risk, not blocker).** The counters and the v2 auditor changed five times during the
  seat. The verdicts are stable across every snapshot, but a receipt's digest can lag the
  frozen bytes; the re-run script closes that in one command.
- **C2's unmet at the tip is partly a wave artefact**: the counter grades the auditor *at the
  rev* (v1) and prices the missing population mode as FAIL. That is correct for a before-state,
  but it means no `C2=met` is reachable at `554ff416` regardless of the wave's work — the
  after-measurement must run at a revision that commits v2 and the counter.
- **No blocker.** Every assigned command ran; every claimed verdict is a pasted output with an
  exit code.
