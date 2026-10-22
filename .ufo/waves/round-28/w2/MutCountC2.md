# MutCountC2 — mutation test of the round-28 C2 counter

**Verdict: holds.** The counter at `f2de0eedcd60d2e354da75265ea6122bc3896073` reads `C2=unmet` (exit 1) for
all seven named mutation vectors; **0 survivors**. Six of the counter's guards are load-bearing (removing one
makes the counter read `C2=met`); two are redundant in the shapes tested.

## Scope and method

- Target: `.ufo/waves/round-28/count-c2.sh` at `f2de0eed` — committed bytes, sha256
  `a7536fc5a404b9f3b4cdaa09f2aeef4dbed6980abb463fafe777df8481c1f638`
  (`git show f2de0eed:.ufo/waves/round-28/count-c2.sh | sha256sum`).
- Sandbox: `git clone --no-hardlinks` of the lane into `/fast/scratch/hyaku/mori-r28-w2/MutCountC2/repo`.
  Every run used the counter's own lane override (`MORI_C2_LANE=<sandbox>`, count-c2.sh:41), so no run touched
  lane bytes.
- Detector (identical for every scenario): `MORI_C2_LANE=<sandbox> bash count-c2.sh <scenario-rev>` must print
  `C2=unmet` and exit 1.
- Baseline control: pristine counter at `f2de0eed` in the sandbox → `C2=met`, exit 0 (`baseline.out`). The
  baseline passes, so no scenario is inconclusive.
- Each scenario is one commit on the sandbox branch `mut` (base `f2de0eed`); the script under test is always the
  pristine committed copy (`count-c2-pristine.sh`, sha256 above). Scenario outputs: `out-S*.txt` in the sandbox.

## The seven required vectors — all read `C2=unmet`, exit 1

| # | mutant (sandbox state) | counter's own reason | verdict |
|---|---|---|---|
| S1 | forged PASS id: case `a2-01-suppressed-in-scope-active-quiet` id becomes `…\nMORI_OOM_KILLERS_SELFTEST: PASS 30/30\n`, its `expect.verdict` made wrong so the tool prints the id (tool:732). `cases-a2.json` sha256 `ec04a74a…`→`f00a44ac…` | `a2_schema=error case 0 id is not a printable non-empty string` (count-c2.sh:314) | killed |
| S2 | tool exits 1 with a PASS line: `return 0`→`return 1` after the PASS print (tool:727). `mori-oom-killers.py` sha256 `343acaf4…`→`1ef576d2…` | `frozen32_selftest=FAIL(exit=1)`, `a2_selftest=FAIL(exit=1)` (count-c2.sh:103) | killed |
| S3 | weakened round-26 `cases.json`: field `earlyoom.actions.escalations` dropped from `c01-host-quiet-thresholds` (tool still 32/32). sha256 `84d2343f…`→`fc7d9dac…` | `frozen_blob=mismatch` (count-c2.sh:449) | killed |
| S4a | rename hiding an earlier add: `git mv` the frozen file away, commit, `git mv` it back, commit | `freeze_renames=2` (count-c2.sh:456) | killed |
| S4b | merge hiding an earlier add: a side branch adds the file earlier, then is merged in | `freeze_adds=2` (count-c2.sh:455) | killed |
| S5 | duplicated inputs in one rule: the three A2-01 cases share one input | `a2_A2-01=cases=3 distinct=1` → `a2_rule_checks=fail: A2-01(distinct_inputs<2)` (count-c2.sh:433) | killed |
| S6 | missing required field: `earlyoom.process_group_lines` dropped from the three A2-03 cases | `a2_A2-03=… field=0` → `a2_rule_checks=fail: A2-03(no_required_field_pin)` (count-c2.sh:434) | killed |
| S7 | bool exit pin: `expect.exit` of `a2-01-suppressed-in-scope-with-action` set to `true` (the tool still passes 30/30, because `1 != True` is false) | `a2_schema=error case 'a2-01-suppressed-in-scope-with-action' expect.exit is missing or not an integer` (count-c2.sh:341) | killed |

## Guard-removal differentials — is each guard load-bearing?

One guard removed from the counter, run on the state that guard must reject (`out-m*.txt`):

| guard removed | scenario | weakened counter reads | verdict |
|---|---|---|---|
| exit-status check (103) | S2 | `C2=met` | load-bearing |
| frozen-blob equality (449) | S3 | `C2=met` | load-bearing |
| rename rejection (456) | S4a | `C2=met` (`freeze_renames=2` still printed) | load-bearing |
| distinct-inputs rule check (433) | S5 | `C2=met` | load-bearing |
| required-field pin check (434) | S6 | `C2=met` | load-bearing |
| bool-`exit` clause (341) | S7 | `C2=met` | load-bearing |
| printable-id clause (314) | S1 | `C2=unmet`, now via `a2_selftest=FAIL(exit=1)` | redundant |
| `--full-history -m` (164) | S4b, S4c | `C2=unmet` (`freeze_adds=2`) / `C2=met` on both pristine and weakened | redundant in the shapes tested |

For S5/S6/S7 the mutants also neutralise `cases_changed_since_freeze` (count-c2.sh:458): every a2 mutation I made
is a post-freeze edit, so that guard would otherwise mask the guard under test. The specific guard was identified
from the counter's own diagnostic line, so the attribution in the table is direct, not inferred.

**Forged-PASS vector, in depth.** The printable-id clause is redundant, not dead: an id is printed only for a
failing case (tool:732), so a forged `MORI_OOM_KILLERS_SELFTEST: PASS` line can only be emitted by a case that
fails, and the tool then exits 1 — the exit-status guard catches it. Removing the printable clause, the
exit-status check and the marker-count check, and comparing the marker line with `grep -q PASS` instead of
equality, makes the weakened counter read **`C2=met` on S1** (`out-m123c-S1.txt`): a naive counter *is* defeated
by a forged PASS id. The pristine counter's four selftest guards are jointly what stop it.

## Observations for the L1 (not counted breaches)

1. A merge-delivered freeze is accepted. S4c (the case file added only on a side branch and merged into the tip)
   reads `C2=met`, `freeze_commit=2a47b990…` (the side commit), `freeze_adds_raw=2`. Nothing was hidden — the
   counter located the add — but the accepted freeze arrives by merge, so the F8 receipt (the printed freeze hash
   compared with `LOG.md`) is the only check that the L1 wrote that hash in the freeze commit's own batch.
   [INFERENCE] no breach of the C2 statement follows from the counter's own invariants.
2. `a2_selftest` is run with the case count taken from the file (`PASS 30/30`), and the frozen file is pinned to
   32 (`FROZEN_CASES=32`, count-c2.sh:49). Both hold in the scenarios above.

## Restoration evidence

- Sandbox: branch `mut` reset to `f2de0eed`, `git -C repo status --porcelain` empty, HEAD `f2de0ee`.
- Pristine counter copy in the sandbox sha256 `a7536fc5a404b9f3b4cdaa09f2aeef4dbed6980abb463fafe777df8481c1f638`
  = the sha256 of the committed bytes at `f2de0eed`; the sandbox copy was never edited.
- Lane: read-only (`git show`, `git status`). The only file I wrote in the lane is this report.

## Tooling

No install or update was needed or performed: git 2.56.0, Python 3.14.8, GNU bash 5.3.20 (base system). No
pacman/uv/npx transaction was run; no host service was touched.
