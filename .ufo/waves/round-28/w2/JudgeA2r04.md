# JudgeA2r04 — Amendment-A2 judgment, rule A2-04 (dry-run send lines)

Verdict: **holds** — all three A2-04 cases in `cases-a2.json` at f2de0eed pin only values that follow from the rule text; no failing case, so no `tool error` / `case error` / `unclear text` ruling is triggered; the tool did not change after the case freeze.

## Rule text attacked against

- Frozen rule table: `.ufo/waves/round-27/contract.md:52` — A2-04 "after `dryrun mode enabled`, send lines go to `earlyoom.dryrun_send_lines`, `sigterm`/`sigkill` stay 0, never positive evidence".
- Adopted form: `.ufo/waves/round-26/contract.md:166-167` — A6 "when the invocation logged `dryrun mode enabled`, send lines go to `earlyoom.dryrun_send_lines`, `sigterm`/`sigkill` stay 0 and they are never positive evidence (X1)".
- Base rules the pins also lean on: scope `.ufo/waves/round-26/contract.md:78-79` (line `__MONOTONIC_TIMESTAMP` ≥ `ActiveEnterTimestampMonotonic`); grammar `.ufo/waves/round-26/contract.md:82-89` (version line, threshold banners at :83-84, `sending SIG… to process ` sends at :85, dry-run flag at :89); output fields `.ufo/waves/round-26/contract.md:90-93` (`scope_complete` true only when the version line of the current invocation is in scope); verdicts `.ufo/waves/round-26/contract.md:96-103` (`KILLER_ACTED` exit 1 on any in-scope send/escalation or `oomd_notices > 0`; `KILLERS_QUIET` exit 0 otherwise).

## Cases and evidence (all read from committed bytes at f2de0eedcd60d2e354da75265ea6122bc3896073)

Freeze order and immutability: `git merge-base --is-ancestor d21b8bd38b1bf72ec903a19ed543c615564e8278 f2de0eedcd60d2e354da75265ea6122bc3896073` → "freeze IS ancestor"; `git log d21b8bd..f2de0eed -- tools/mori-oom-killers.py tools/fixtures/mori-oom-killers/cases-a2.json tools/fixtures/mori-oom-killers/cases.json` → empty; `git diff --quiet d21b8bd f2de0eed -- tools/fixtures/mori-oom-killers/cases-a2.json` → UNCHANGED. So the tool byte-identical at the case freeze and at the attack target: the "L1 changed the tool after the freeze" clause has nothing to check, and no `KILLER_ACTED` flip is possible from a post-freeze change.

Freeze-time selftest receipt `.ufo/waves/round-28/evidence/c2-freeze-selftest.txt`: `PASS 30/30`, `exit=0` at d21b8bd. Reproduced from a temp extract of f2de0eed under `/fast/scratch/hyaku/mori-r28-w2/MoriR28.JudgeA2r04/` (`git archive f2de0eed | tar -x`):
- `python3 -I -B tools/mori-oom-killers.py --selftest --cases tools/fixtures/mori-oom-killers/cases-a2.json` → `PASS 30/30`, exit 0.
- `--selftest` (default round-26 file) → `PASS 32/32`, exit 0.
- Per-case `--inputs` on each A2-04 case, shell exit and every `expect.fields` dotted path diffed against the tool's JSON output: 14/17/14 fields checked, **0 mismatches**, exits 0 / 0 / 1 as pinned.

File shape: 30 cases, exactly 3 per rule id (`A2-01`…`A2-10`), i.e. ≥20 and full coverage of the ten ids.

## Per-case judgment (does each pinned value follow from the rule text?)

**1. `a2-04-dryrun-sigterm-send-not-positive` — follows.**
One invocation (version `earlyoom 1.9.0` at 20000100, equal to `ActiveEnterTimestampMonotonic` 20000100, in scope by ≥ at round-26:78-79 → `scope_complete` true, :92); dry-run flag at 20000120 (round-26:89 → `dryrun` true); one `sending SIGTERM to process ` line at 20000300, after the flag → A2-04 routes it to `dryrun_send_lines: 1` and keeps `sigterm`/`sigkill` at 0 with no positive evidence (round-27:52, round-26:166-167). With `oomd_notices: 0` and oomd inactive, no verdict rule fires → `KILLERS_QUIET` exit 0 (round-26:102, "otherwise"). Earlyoom is active, so `actions` is a real object with zeros, not `null` (round-26:102-103). All 14 pins follow.

**2. `a2-04-dryrun-two-sigterm-sends-counted` — follows.**
Version line at 30015100 ≥ ActiveEnter 30015000 → in scope, `scope_complete` true. Flag at 30015200; two `sending SIGTERM to process ` lines at 30016000/30016500, both after the flag in the same invocation → `dryrun_send_lines: 2`, counts 0, never positive evidence → `KILLERS_QUIET` exit 0. The two banner lines at 30015300 are the threshold grammar (`sending SIGTERM when mem avail <= <a>% and swap free <= <b>%,` and, after leading-whitespace strip, `SIGKILL when mem avail <= <c>%...`, round-26:83-84), a distinct prefix from the send grammar at :85 — so a literal reading of "send lines" cannot swallow them, and `dryrun_send_lines: 2` (not 3) plus thresholds 20/20/12/12 both follow. Nothing in A2-04 suspends threshold parsing inside a dry-run invocation. All 17 pins follow.

**3. `a2-04-dryrun-send-with-oomd-notices` — follows.**
Version line at 40020000 = ActiveEnter → `scope_complete` true; flag at 40020100; one `sending SIGKILL to process ` at 40020200 → `dryrun_send_lines: 1`, `sigkill: 0`, not positive evidence (A2-04). `oomd_notices: 2` with oomd active independently fires `KILLER_ACTED` exit 1 (round-26:97), so the verdict is carried by oomd exactly as the case's `why` states — A2-04 removes the dry-run send as a source without touching the oomd path. All 14 pins follow.

No failing case: no `tool error` / `case error` / `unclear text` ruling is required. The freeze selftest `PASS 30/30` and the f2de0eed rerun agree with every pin.

## Residual risk and verification gaps

- Wording drift, not a defect: round-27:52 says "after `dryrun mode enabled`" (line-order reading) while the adopted A6 at round-26:166-167 says "when the invocation logged `dryrun mode enabled`" (per-invocation reading). All three A2-04 cases have the flag and sends in one invocation, so no case distinguishes the readings; the cross-invocation split is A2-07's territory and outside this judgment. The cases cannot catch a tool that treated "after" as scope-wide.
- A2-04's interaction with `earlier_invocation_send_lines` (a real send in an earlier invocation plus a dry-run current one) is pinned nowhere in the A2-04 cases; untested here by design of this rule's scope.
- I verified the two case files and the tool only between d21b8bd and f2de0eed and at the working-tree evidence receipt; I did not audit the tool's source line-by-line (selftest + `--inputs` behavior is the evidence of record).
- Tool installs: none (used preinstalled `git`, `python3`; no pacman/uv/npm channel used).

[INFERENCE] none — every claim above cites a command output or contract line observed this session.
