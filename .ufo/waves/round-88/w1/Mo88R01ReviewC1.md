# Mo88R01ReviewC1 — surgical C1 review

Axes: operability; arm quality, wrong-reason resistance, kill attribution. Detection/report only. Recommendation, not admission.

## Findings, by severity

**No blocking defect in the six added arms.** Independently reran pristine and all six declared mutations, at both entering and after revisions. Every declared new arm passes pristine and fails its intended mutant. None of these six passes for a wrong reason.

**Medium residual, inherited: two original arms still accept a label substring as evidence.** At `.ufo/waves/round-87/count-c1.py:240` and `:246`, both `unanchored_excluded` and `unanchored_plus_killed_unmet` test `"unanchored" in " ".join(extras)`. Under M6, both still PASS although the doubled anchor is graded, not excluded: the survivor label `M1-unanchored-conjunct` supplies the substring. The second arm's fixture at :241 contains exactly one anchor and no tally; its `not met` comes from a `pristine-arms` mismatch plus a survivor, not an unanchored refusal. These unchanged weaknesses do not account for the six measured kills: the added arms use anchored extra prefixes or numerical fields, and M6 fails the new numerical arm. They remain residual quality defects, not new regressions. No remediation performed.

**Low documentation discrepancy:** the frozen contract's M5 fixture sketch says `arms=24`; the landed arm at :311 uses `arms=54`. The latter is necessary and correct for the r87 counter's `TARGET_ARMS=54`: it leaves `killed=5` as the sole mismatch. Substituting the contract sketch's 24 would mask M5 with an unrelated arms mismatch. The frozen predicate itself is met; the fixture sketch is inaccurate.

## Bytes actually reviewed

Lane HEAD initially observed: `9c775ac2131da13c4c4cfdf2b14077184076f557`. Review and experiments use committed bytes, not moving worktree edits.

| Object | Revision / blob | SHA-256 |
|---|---|---|
| r87 count-c1.py entering, 14904 bytes | `1bd5ec3fa260458f74eb32a2e5bb157209c5934d` / `f99f1e87d0fb319aaba32e94507d1ee8714eaca8` | `e2ff968721678cc61d6a1674def8da3e27a43f3fed8daab79d53c657ae2c266e` |
| r87 count-c1.py after, 17739 bytes | `d5e2eda494877a85edaa4e287d6ad81843d9a8a1` / `ef99b0f929859dd3ccb1f8bab8f40669fea83651` | `85bc0f29865e3c9a9de49940dcf12eef20977aa77899b6ba3290fcb243c7cc2c` |
| r88 C1 counter used for CLI/control runs | lane worktree at initial HEAD | `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2` |

The last hash matches the after receipt. The requested diff is additive six cases plus tally lines in `dup.py` and `empty.py`; no original case was removed. Read the contract, controls and after receipt. `xd://lsp` discovery returned **No such tool**: semantic status/references/definition/diagnostics were unavailable. Source inspection and runtime experiments are the fallback, not semantic-reference proof.

## Six-arm table — independently measured

Every frozen old anchor occurs exactly once in both entering and after bytes; every replacement changes bytes. Pristine after: rc=0, `C1_COUNTER_SELFTEST pass=24 fail=0`.

All paths/line numbers below refer to `.ufo/waves/round-87/count-c1.py` at d5e2eda4.

| New arm | Declared mutant | Pristine arm | Mutated arm | Mutant rc / full tally | Load-bearing assertion |
|---|---|---|---|---|---|
| `met_guard_unanchored` (:284–286) | M1-met-no-guard | PASS | FAIL | 1 / 22 pass, 2 fail | `not met`; total=1, killed=1 and actual unanchored extra remain true |
| `met_guard_empty` (:293–295) | M2-met-drop-empty (also M1) | PASS | FAIL | 1 / 23 pass, 1 fail | `not met`; total=1 and actual empty-mutation extra remain true |
| `killed_tally_mixed` (:303–305) | M3-killed-n | PASS | FAIL | 1 / 23 pass, 1 fail | `killed == 1`; mutant reports 2 while survivors=1, total=2 stay true |
| `arms_tally_passed` (:309) | M4-arms-total | PASS | FAIL | 1 / 23 pass, 1 fail | `tail.endswith("arms=18")`; met remains True, mutant arms becomes 1 |
| `target_split_killed_not_mutants` (:310–312) | M5-split-field | PASS | FAIL | 1 / 23 pass, 1 fail | `not target_split(...)`; only killed=5 differs from target, other fields match |
| `doubled_anchor_counted_type` (:317–319) | M6-anchor-guard | PASS | FAIL | 1 / 22 pass, 2 fail | mutants=0 and total=0; both become 1 under M6, while `met is False` remains true |

Exact FAIL sets: M1 = `met_guard_unanchored`, `met_guard_empty`; M2 = `met_guard_empty`; M3 = `killed_tally_mixed`; M4 = `arms_tally_passed`; M5 = `target_split_killed_not_mutants`; M6 = `met_guard_unanchored`, `doubled_anchor_counted_type`. Collateral kills are explicit, not six independent one-to-one failure sets.

A trace of real `grade()` return values confirms isolation: for the first two pristine witnesses, extras contain respectively only `unanchored tools/dup.py r88-double occurrences=2` or `empty-mutation tools/empty.py r88-empty`, with `mutants=1 killed=1 survivors=0 total=1 arms=2`. No pristine-red or pristine-arms failure masks either witness. Under M1 met becomes True for both; under M2 only the empty witness becomes True. The tally lines added at :234–235 and :249–250 are therefore load-bearing. Prefix checks are not satisfied by the fixture labels `r88-double`/`r88-empty`.

## Original 18 and 18 + 6

Entering pristine: rc=0, 18 pass / 0 fail. Each of its six mutant copies: rc=0, 18 pass / 0 fail. After pristine: rc=0, 24 pass / 0 fail. Comparing actual printed arm labels: removed=[], added exactly the six names in the table. All original 18 pass in the after pristine run. No case swapped out. The counter's own grading constants still target the r86 subjects at 18/13/23; these are not its own selftest's 24 arms.

## Frozen refusal checks

* Named label-only control rerun: shared clone checked out at entering 1bd5ec3f, six `cases.append(("label-only-N", True, "label-only"))` inserted before `marker_literal`, fixture commit `9b8bfee2b22263c14a9e3e32606d15569d3cd550`. All six mutants survive rc=0; `C1=unmet mutants=6 killed=0 survivors=6 total=6 arms=24 detector=green`, rc=1. Refusal is survivors, not a wrong tally or red pristine.
* Unanchored CLI fixture: shared clone at after d5e2eda4, harmless `_DUP = "killed_n = total - survivors"` before the main guard duplicates only M3's anchor; fixture commit `f7ad470708d49cde5d8414cc784621acc17e1e6d`. `EXTRA unanchored ... M3-killed-n occurrences=2`; `C1=unmet mutants=5 killed=5 survivors=0 total=5 arms=24 detector=green`, rc=1. Unanchored is not counted killed.
* Direct calls to the unmodified r88 counter's `grade()` with synthetic tally-correct green subjects: killed+empty gives `(False, 'mutants=1 killed=1 survivors=0 total=1 arms=2', ..., ['empty-mutation tools/e.py empty'])`; killed+doubled-anchor gives the same numerical tail and only `unanchored tools/d.py double occurrences=2`; zero population gives `(False, 'mutants=0 killed=0 survivors=0 total=0 arms=0', [], [])`. Thus neither unrelated pristine errors nor a survivor masks these refusals. Frozen CLI mutants all have old != new, so an empty mutation is tested through this actual grade API, not falsely claimed as reachable through its fixed CLI population.

Canonical rule cited: r88 `count-c1.py` `grade()` (:144–185), `killed()` and `green()` (:93–98), with main's target/detector gates. Kills require nonzero rc or positive fail count; non-exact anchors and empty mutations are skipped and refuse met. No claim of exhaustive mutation resistance follows from 6/6.

## Verification gaps and method

No LSP device; no C2, fleet, service, resume or orchestration behavior reviewed. All execution was Python 3.14.8 and git 2.56.0 as found; no installs/upgrades. Lane code untouched; only this report written there. Temporary mutations and fixture commits were confined to `/fast/scratch/hyaku/mori-r88/Mo88R01ReviewC1/`, deleted before handoff. No /tmp evidence. No tests beyond this seat's requested review experiments.

Self-check: accuracy 4 (runtime evidence, but no semantic diagnostics); completeness 4 (all four questions covered, finite mutant population only); clarity 4 (explicit collateral kills, lengthy reproduction detail); actionability 4 (exact defects/lines, no remediation in detection-only seat); conciseness 4 (tables avoid duplicating full stdout). Mean 4.0. Main can act without confusing residual defects with a failed frozen predicate.

## Measured verdict and exact commands

`C1 review: agree` against `C1=met mutants=6 killed=6 survivors=0 total=6 arms=24` — recommendation scoped to the frozen C1 predicate. New-arm quality is supported; inherited substring weaknesses remain.

Commands actually used (drivers lived only in scratch and are removed, not durable artifacts):

```sh
git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff 1bd5ec3f d5e2eda494877a85edaa4e287d6ad81843d9a8a1 -- .ufo/waves/round-87/count-c1.py
python3 -I /fast/scratch/hyaku/mori-r88/Mo88R01ReviewC1/driver.py
TMPDIR=/fast/scratch/hyaku/mori-r88/Mo88R01ReviewC1 python3 -I /fast/scratch/hyaku/mori-r88/Mo88R01ReviewC1/probe.py
```

`driver.py` read each exact revision via `git show REV:.ufo/waves/round-87/count-c1.py`, asserted each frozen r88 anchor count=1, wrote pristine and six old→new copies, then invoked `["python3", "-I", COPY, "--selftest", "--scratch", FRESH_SCRATCH]` with cwd and TMPDIR below this seat's scratch and both git config files `/dev/null`. It parsed every PASS/FAIL label, rc and final tally. `probe.py` imported actual counter bytes with bytecode disabled, called `grade()` on the three synthetic populations above, then traced `grade` returns during pristine/M1/M2/M3/M4/M6 selfchecks. Those are experiments, not substituted grading implementations.

Exact CLI grading commands:

```sh
TMPDIR=/fast/scratch/hyaku/mori-r88/Mo88R01ReviewC1 python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-88/count-c1.py d5e2eda494877a85edaa4e287d6ad81843d9a8a1 --scratch /fast/scratch/hyaku/mori-r88/Mo88R01ReviewC1/after-run
# rc=0; C1=met mutants=6 killed=6 survivors=0 total=6 arms=24 rev=d5e2eda49487
TMPDIR=/fast/scratch/hyaku/mori-r88/Mo88R01ReviewC1 python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-88/count-c1.py 9b8bfee2b22263c14a9e3e32606d15569d3cd550 --repo /fast/scratch/hyaku/mori-r88/Mo88R01ReviewC1/label-only --scratch /fast/scratch/hyaku/mori-r88/Mo88R01ReviewC1/label-run
# rc=1; C1=unmet mutants=6 killed=0 survivors=6 total=6 arms=24 detector=green
TMPDIR=/fast/scratch/hyaku/mori-r88/Mo88R01ReviewC1 python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-88/count-c1.py f7ad470708d49cde5d8414cc784621acc17e1e6d --repo /fast/scratch/hyaku/mori-r88/Mo88R01ReviewC1/anch-dup --scratch /fast/scratch/hyaku/mori-r88/Mo88R01ReviewC1/anchor-run
# rc=1; C1=unmet mutants=5 killed=5 survivors=0 total=5 arms=24 detector=green
```
