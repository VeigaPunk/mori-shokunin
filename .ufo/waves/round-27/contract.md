# mori round 27 — claim contract (attempt 1, L1 MoriR27)

Entering tip `fc09f96c8036094bef06370dbb4b436edf96e6e3` (round 26 admitted, `MANIFEST.json` rounds[462]).
Written before any round-27 implementation. Targets, not results. Both counters below are committed with this
contract, before the data they count.

## Why these two claims

- The orchestrator's drift watch: a new one-shot tool was the coverage claim in rounds 24, 25 and 26. This round
  adds no new tool. C1 is a knowledge claim on uncovered FR10 ground; C2 strengthens the existing round-26 tool's
  self-test, which the round-26 closure routed as D7.
- Lowest-scoring active axes are depth, freshness and calibration (5 each, `SCORECARD.md:12-14`). C1 works depth.

## C1 — depth (score 5, tied lowest): which process an OOM killer on this host picks, and why

FR10 frontier remainder (`corpus/README.md` FR10 row): "fleet attribution of a victim". mori knows that earlyoom
1.9.0 is active here and that it sent 38 SIGTERM and 1 SIGKILL lines in boot -1 (`corpus/lessons/round-26.md:22-25`),
but holds no knowledge of how earlyoom and the kernel choose the victim (`oom_score`, `oom_score_adj`, the
`--prefer`/`--avoid`/`--ignore` options, `--sort-by-rss`), what `oom_score_adj` the fleet's processes run with, or
what share of those sends hit fleet processes. Sweep at the entering tip:
`git grep -n -i -E 'oom_score|OOMScoreAdjust' fc09f96c -- corpus/knowledge SKILL.md PROVINCE.md | wc -l` → `0`.

Statement: a new entry `corpus/knowledge/oom-victim-selection-r27.md` exists whose `source:` line cites at least 3
`corpus/SOURCES.md` rows numbered S127 or above (rows that did not exist at the entering tip) with status `mined`
and the entry in `used-by`; and `SKILL.md` holds a section whose `## ` heading contains `Round27` with at least 3
table rows that cite the entry (a decision table grounded in it).

Counting command (committed bytes only; exit 0 met, 1 unmet, 2 bad revision):

```sh
bash /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-27/count-c1.sh <rev>
```

Before (at `fc09f96c`): `entry=absent new_rows_cited=0 skill_rows=0`, `C1=unmet`, exit 1
(`evidence/c1-before.txt`). Declared after (at the landed tip): `C1=met`, exit 0.

Not claimed by C1: any new tool, any change to earlyoom's or the kernel's settings, any victim identity. Privacy
(binding): counts and process classes only; never a command line, a uid, a pid list, journal `MESSAGE` text, the
values of `/etc/default/earlyoom` or of any `--prefer`/`--avoid`/`--ignore` expression, or any OMP settings value.

## C2 — operability (score 7): pin the round-26 amendment-A2 rules with frozen cases (routed D7)

The round-26 tool `tools/mori-oom-killers.py` passes `PASS 32/32` on the pre-freeze cases, but no committed case
file pins the ten rules adopted after its freeze (`.ufo/waves/round-26/contract.md` "Amendment A2"). Frozen rule
list (each case in the new file names exactly one id in a `rule` field):

| Id | Rule (as adopted in round-26 amendment A2) |
|---|---|
| A2-01 | a journald `Suppressed N messages from earlyoom.service` line in scope sets `scope_complete` false |
| A2-02 | an earlyoom `ActiveState` other than `active` or `inactive` maps to state `unavailable` and `KILLERS_UNKNOWN` |
| A2-03 | `killing whole process group ` lines are counted in `earlyoom.process_group_lines` |
| A2-04 | after `dryrun mode enabled`, send lines go to `earlyoom.dryrun_send_lines`, `sigterm`/`sigkill` stay 0, never positive evidence |
| A2-05 | `ActiveEnterTimestampMonotonic` missing or `0` leaves the invocation unbounded: `scope_complete` false |
| A2-06 | send lines of this boot outside the current invocation go to `earlyoom.earlier_invocation_send_lines`; non-zero is positive evidence (`KILLER_ACTED`) for an earlyoom that is not active, reported without a verdict change for an active one |
| A2-07 | dry-run applies per invocation (split at each version line): one dry-run invocation does not zero another invocation's real sends |
| A2-08 | a `null` earlyoom journal reads `KILLERS_UNKNOWN` for any earlyoom state |
| A2-09 | send lines of a removed (`not-found`) earlyoom unit this boot are positive evidence |
| A2-10 | a journal record without a numeric `__MONOTONIC_TIMESTAMP` is left uncounted and makes the scope incomplete; positive evidence elsewhere still stands |

The live-mode readability probe (A1c) is out of scope: `--inputs`/`--selftest` cannot exercise it.

Statement: `tools/fixtures/mori-oom-killers/cases-a2.json` is written by a seat that does not read the tool's
source, committed before the L1 runs the tool on it, unchanged after that freeze commit, holds at least 20 cases,
covers all ten rule ids with a case that pins both a verdict and an exit code, and at the landed tip the tool prints
`PASS N/N` on it and still `PASS 32/32` on the frozen round-26 file.

Counting command (extracts the tool and both case files from the revision; a failing self-test exits 1, closing the
round-26 D6 defect for this claim's counter):

```sh
bash /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-27/count-c2.sh <rev>
```

Before (at `fc09f96c`): `a2_cases=0 a2_rules_covered=0/10`, `C2=unmet`, exit 1 (`evidence/c2-before.txt`).
Declared after (at the landed tip): `C2=met`, exit 0. If the tool fails a frozen case, the L1 may change the tool
(never the case file) and the counter re-runs both files; a case the tool cannot meet without breaking a round-26
frozen case is a miss, reported as one.

## Held, not claimed

Freshness 5, calibration 5, coverage 6, adjacency 6 observed. No retirement, waiver, exploratory claim or promotion.
No-harm check: the lane retention scan reads 4 unallowlisted at `fc09f96c`
(`python3 -I -B tools/mori-retention-gate.py scan --repo <lane> --rev fc09f96c… --policy
.ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json` → `metric 4`); no
landed tip may exceed 4. Operability no-harm: the five round-26 selftests keep their tallies.

## Routed defects (hygiene, never a counted claim)

Round-26 D1–D6 and round-25 R1, R3, R5, R7 are fixed or explained in `corpus/lessons/round-27.md`; D7 is C2.

## Amendment W1 (2026-10-22T15:55Z, before any C2 data exists): C2 withdrawn, not narrowed

Seven of the 34 wave-1 seats died at spawn with `Error: No model selected.` (the scribe, executor and
mutation-tester route was degraded; orchestrator route notice of 15:40Z). One of them was `WriteA2Cases`, the seat
whose independence from the tool is the substance of C2 ("written by a seat that does not read the tool's source").
Session rules forbid replacing or rerouting a dead seat, and an L1-written case file would not meet the stated
condition. C2 is therefore withdrawn before any case exists; `count-c2.sh` stays committed and unchanged, and its
before-value stays the record. Routed D7 is carried as named debt with this reason. The round has one counted claim,
C1. No other part of the contract changes.
