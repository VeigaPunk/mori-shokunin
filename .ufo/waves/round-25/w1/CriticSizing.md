# Round 25 wave 1: CriticSizing (claim-sizing critic)

Seat: `MoriR25.CriticSizing`, critic, a leaf seat with no subagents. Lane tip read: `129832e3e8a710d47ecd0425efb9fc67ecf59697`. Contract: `.ufo/waves/round-25/contract.md` at `7634be75`.
Sizing rules checked: `.ufo/prompts/mori-round-25.md:342-350` (fleet repo) and `.scratch/goal-20261022-hyaku-12h.md:150-158`. The bounds come from `corpus/lessons/round-24-verifier-spotcheck.md`.
All commands were read-only: git object reads, Python byte reads of the omp binary, a read of `~/.omp/agent/config.yml`, and `git ls-remote` against upstream. No tool was installed or upgraded. RULES.md was read (`/home/vgpnk/.omp/agent/RULES.md:1-14`).

## Verdict in one paragraph

Both claims meet the sizing rule as written. Each has one concrete after-value from one command. The two claims can be verified separately, and every before-state the contract expects matches the bytes at `28b79d3d`.

I found two fixable defects that could make a correct round miss or repeat its routed defect:
- **F1.** No committed evidence with a revision is required for either after-value. The closure does not execute lane gates.
- **F2.** C1 contains an ordering trap between D1 and the uncounted mutant replay.

Five more items are tradeoffs that the report should disclose: F3 to F7.

**Sentinel.** The "same axis+surface 3 rounds running" sentinel trips at this round's closure under the class reading of "surface". It does not trip under a strict same-files reading. Either way, the remedy belongs to round 26.

## Checks that pass (with evidence)

| Check | Evidence | Result |
|---|---|---|
| One concrete after-value per claim | C1: `"mismatches": 0`, `"held": 4` of `"items": 4`, exit 0 (`contract.md:30-31`). C2: `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21`, exit 0 (`contract.md:87-88`) | pass |
| C2 freeze order and denominator | `git show --stat 7634be75` adds only `contract.md` and `tools/fixtures/mori-job-runway/cases.json`. `git ls-tree -r 7634be75 -- tools/` has no `mori-job-runway.py`. The blob `48df844a22d74a57204f55a62e54760c7038c60f` is the same at `7634be75` and `129832e`. `jq '.cases\|length'` gives 21, with ids `J01` to `J21` | pass |
| C1 before = 4 mismatches (static re-derivation; the tool does not exist yet) | D1: `git cat-file -e 28b79d3d:.ufo/waves/round-25/evidence/pressure-selftest.txt` exits 128. D2: in `corpus/knowledge/system-pressure-r24.md` at `28b79d3d`, the Corrections section spans lines 8-42. `refreshed` / `on each read` is split across lines 94-95 with no indent on line 95, so folding the line break gives the exact phrase. The other two phrases are on lines 170 and 171, and `K4` occurs nowhere. D3: `corpus/lessons/round-24.md:79-80` has only `PASS 6/6` and no `Correction` line. The supplementary file at `4f05dd5a` has 7 cases. D4: `.gitignore` holds only `.ufo/interactive-sessions/` and `.ufo/worktrees/` | pass: 4 of 4 red as declared |
| Causal separability | C1's predicates name only round-24 paths, the round-25 evidence file and `.gitignore` (`contract.md:19-22`). C2's selftest reads only its own script and `cases.json` (`contract.md:77-81`). Neither predicate reads the other claim's files, so either claim lands and verifies alone. D1 depends on the round-24 `tools/mori-pressure.py`, not on C2 | pass |
| Universal clauses enumerated | D2 lists 3 phrases, D4 lists 6 accepted lines, and the clamp and default "every match" rules are counted as `sites` (`contract.md:61-66`) | pass, except F6 and F7 |
| C2 rules against the real binary | Python `re` over the bytes of `~/.local/bin/omp` (256,702,432 bytes) matched the clamp once, value `100`, and the setting default once, value `100`. The default is spread over several lines (`id: "async.maxJobs",\n  protocolDefault: ["rpc"],\n  type: "number",\n  default: 100`). Line-mode ripgrep finds 0 default matches, so the tool must match over the whole byte string, as Python `re` does. `~/.omp/agent/config.yml:244-245` reads `async:` / `  maxJobs: 200` | pass; [INFERENCE] by rules 4-5, the live verdict is `RUNWAY_CLAMPED`, effective 100, exit 1 |
| C2 "Sourced" can land | `git ls-remote --tags https://github.com/can1357/oh-my-pi` lists `45c35e40c46166dc726ccc52f5d27f40f2449f99 refs/tags/v18.12.6` | pass |
| Scope bound on overrides | `/home/vgpnk/Projects/shokunin/.omp` contains only `agents`. No `maxJobs` appears in the fleet or lane `.omp` directories | the bound holds on this host today |

## Findings

### F1: neither after-value requires committed evidence that names its revision (fixable; high)

- **Counterexample.** The contract declares both after-values as commands (`contract.md:30-31`, `87-88`). The closure will not run them. The canonical protocol says the integrator "verifies a gate's *committed evidence* (self-test tally, frozen-run verdict, the revision measured); it does not execute a sibling's gate" (`~/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md:428-430`). Round 24 is the precedent:
  - the C2 tally was "evidence-verified, not re-run" because the tool is a registered lane gate (`round-24-verifier-spotcheck.md:15-17`);
  - the C1 tool "was not executed" (`round-24-verifier-spotcheck.md:42`);
  - both round-24 tools are registered as gates (`SKILL.md` "Round24 registry additions", about lines 640-643).

  The contract requires committed evidence only for C2's live host run, and that run is explicitly not the after-value (`contract.md:92`). It requires nothing for the selftest tally or the C1 check output. Round 24's D1 defect was exactly this: a tally file that named no revision. Without a requirement, round 25 can repeat D1 for its own after-values.
- **Impacted axes:** calibration, because it repeats D1, and coverage, because the C2 tally could not be checked.
- **Smallest safe correction.** Land an amendment before any code. For each after-value, commit an evidence file in D1's own format, for example `.ufo/waves/round-25/evidence/c1-after.txt` and `c2-selftest-after.txt`:
  - line 1 is `revision: <40 hex>` and names R;
  - line 2 is `exit: <n>`;
  - the rest is the full stdout.

  R must carry the same tool blob and fixture tree as the landed tip. Add C2's cases blob `48df844a…` as the freeze pin, so a closure confirms the freeze with one `git rev-parse` instead of a separate diff.

### F2: ordering trap inside C1, between D1 and the uncounted mutant replay (fixable; high)

- **Counterexample.** D1 holds only if the blob of `tools/mori-pressure.py` and the tree of `tools/fixtures/mori-pressure` are the same at R and at REV (`contract.md:19`). The same section commits the lane to replaying the six surviving round-24 mutants, "killed by new supplementary cases or explained" (`contract.md:35-36`). Killing a mutant with a new case means editing `tools/fixtures/mori-pressure/supplementary-cases.json`, which is inside that tree. Killing a matcher survivor may also need a change to `tools/mori-pressure.py`.

  So if `pressure-selftest.txt` is committed before the replay lands, D1 turns red at the landed tip. The result is `mismatches: 1` and an honest-stop miss, caused by work the contract says does not count. This is a C1-internal collision, not a C1/C2 coupling.
- **Impacted axis:** calibration.
- **Smallest safe correction.** Make the ordering binding in the L1 plan: produce and commit `pressure-selftest.txt` after the last change to `tools/mori-pressure.py` or `tools/fixtures/mori-pressure/`. Alternatively, freeze the pressure tool and fixtures for the rest of the round and answer every survivor with "explained". The target is unchanged either way.

### F3: part of D1 can only be checked from evidence, and D1 holds even when the selftest fails (tradeoff; disclose)

- **Counterexample.** D1 requires the remaining bytes to equal the stdout of running R's `tools/mori-pressure.py --selftest` (`contract.md:19`). That is execution of a registered gate. A closure can re-derive D1's ancestry and blob/tree identity with plain git reads, but the stdout-equality part is evidence-verified at best (PROTOCOL.md:428-430).

  Separately, D1 constrains only that `<n>` equals the run's exit code, not that `<n>` is 0. An evidence file that records `exit: 1` and a `FAIL` tally makes D1 "held". The output is deterministic: on a pass `_selftest` prints only the two tally lines (`git show 28b79d3d:tools/mori-pressure.py`, lines 586-587). So this is not a flakiness risk.
- **Impacted axis:** calibration (what "held" proves).
- **Smallest safe correction.** Have the report say that the stdout half of D1 is evidence-verified and that D1 is about provenance, not about passing. Adding `exit: 0` would strengthen the target and is allowed only before the code lands.

### F4: D2 and D3 are lexical predicates (tradeoff; disclose)

- **Counterexample.**
  - D2 holds if line 95 is rewritten as "refreshed on every read". That keeps the K5 error and removes the matched string (`contract.md:20`).
  - D2 needs `(K4)` somewhere in a Corrections section, not a correction at lines 170 and 171.
  - D3 holds for any line containing `Correction` and `PASS 7/7`, such as "Correction pending; PASS 7/7 not re-run" (`contract.md:21`).

  The round-24 closure asked the lane to "Fix the body lines in place, with a correction note" (`round-24-verifier-spotcheck.md:143`). The predicates measure the absence of strings, not the correctness of what replaces them.
- **Impacted axis:** calibration (a false "held" is possible).
- **Smallest safe correction.** Have the report name D2 and D3 as lexical guards and point the closure to read 3 body loci and 1 lesson line: knowledge-entry lines 94-95, 170 and 171 at the entering tip, plus the new D3 line. No target change.

### F5: C1 stretches the calibration rule's object (tradeoff; disclose)

- **Counterexample.** The rule says a calibration claim counts mismatches between "the lane's self-assessment (SCORECARD/SHONEN) and observed repo state" (`mori-round-25.md:346-347`; goal file 155-156). None of D1-D4 is in SCORECARD or SHONEN:
  - D1 is an evidence file;
  - D2 is a knowledge entry;
  - D3 is a lesson;
  - D4 is the absence of an ignore rule for an untracked file. That is not a statement in committed bytes at all.

  The contract widens the object to "a lane-written statement or record" (`contract.md:13`). The round-24 closure accepted a similar widening, the dispatch ledger, only "as a boundary" (`round-24-verifier-spotcheck.md:98`). A stricter closure may read C1 as 3 record mismatches plus 1 hygiene guard.
- **Impacted axis:** calibration (claim–rule fit).
- **Smallest safe correction.** The after-value cannot change. The report should describe D4 as a hygiene guard the tool counts, not as a self-assessment mismatch. It should also name which items are lane self-accounts (D1, D3) and which are corpus wording (D2).

### F6: two "never" clauses contradict the contract's own rules (fixable; wording)

- **Counterexample.**
  - C2 says the tool "never writes" (`contract.md:48`), but rule 7 has `--selftest` write each case's config and binary into a fresh temporary directory (`contract.md:78`).
  - C1 says the tool reads git objects only, with "no working tree" (`contract.md:14`), but D1 requires a run "from a temporary extract of R" (`contract.md:19`).

  A closure that tests the universal clause literally finds it false by the contract's own text.
- **Impacted axes:** operability (the tool's declared write scope) and the honesty of the contract.
- **Smallest safe correction.** Amend both clauses before code to "writes nothing outside a fresh temporary directory it creates and removes". Mirror that in the registry row's write-scope cell.

### F7: universal clause about the carried bound with no enumerating command (minor; disclose)

- **Counterexample.** "each round-25 attempt row records the seat gate's own ledger line" (`contract.md:33-34`) names no counting command. The clause can be enumerated: today `.ufo/waves/round-25/wave1-attempts.json` has 1 row with `slot_ledger_line` `1792663083 34 mori r25-w1`. That epoch is 2026-10-22T09:58:03Z (`date -u -d @1792663083`), 5 s before the row's `at` of 09:58:08Z, and it appears at line 20 of `~/.local/state/shokunin-hyaku/wave-slots`.

  But the committed copy is written by the lane. The source file is mutable, outside git, and only 659 bytes. So the answer rests on a file the closure cannot pin. The clause is not counted, so the claim is not at risk.
- **Impacted axis:** calibration (the carried bound only).
- **Smallest safe correction.** Name the command, for example `jq '[.[]|select(.slot_ledger_line==null)]|length' .ufo/waves/round-25/*-attempts.json` → 0. Have the report state that the source file is uncommitted and mutable.

## Sentinel: "same axis+surface claim or same routed defect class in a lane 3 rounds running"

Rule: goal file line 173. Remedy: "The lane's next round must work a different frontier area."

**Calibration history in SCORECARD.md:**

| Round | Calibration claim | Surface | Score | Cite |
|---|---|---|---|---|
| 17-19 | calibration | not checked | not checked | `SCORECARD.md:1238` ("calibration chosen rounds 17–19") |
| 21 | C2 calibration | evidence-loss permission rule (retention) | 5→5 | `SCORECARD.md:1296`, `1317` |
| 22 | C1 calibration | retention receipt reconciliation | 5→5 | `SCORECARD.md:1355` |
| 23 | C1 | remove misleading `raw_unallowlisted` ("routed by r22 closure") | 5→5 | `SCORECARD.md:1422` |
| 24 | C1 | repair the four round-23 routed items | 5→5 | `SCORECARD.md:1501` |
| 25 | C1 | repair the round-24 routed defects D1-D4 | 5→5 held | `SCORECARD.md:1541` |

**Class reading: trips at the round-25 closure.**
- Rounds 23, 24 and 25 each make calibration's claim a repair of the previous closure's routed list.
- The contract itself defines the defect class as "a lane-written statement or record disagrees with the committed bytes" (`contract.md:13`). Each of these routed defects fits that class: round 23's misleading alias, round 24's R4 (ledger `at` earlier than its dispatch commit, `round-24-verifier-spotcheck.md:44-46`) and round 25's D1-D3.

**Strict same-files reading: does not trip yet.** Only rounds 24 and 25 share a surface: a new git-object routed-item gate (`tools/mori-routed-check.py`, then `tools/mori-routed-r24.py`). That is 2 rounds. The retention surface ran 3 rounds (21-23), but that run ended before this sentinel existed.

**Coverage does not trip.** Coverage has been claimed 3 rounds running (23 FR2 quota, 24 FR12 pressure, 25 job runway), but on 3 different surfaces.

**Why the trap keeps recurring.** The round prompt requires every routed defect to be fixed each round (`mori-round-25.md:320-323`), and calibration wins the "lowest tie" every time. Depth is tied at 5, yet SCORECARD repeatedly records "no separate depth claim" (`SCORECARD.md:872`, `981`, `1115`, `1258`). The result is a loop: each round's closure routes defects, and the next round's counted claim repairs them, with calibration held at 5. The operator directive asks for no recursive loops (goal file line 11).

**A second gate per round.** A new per-round gate (`mori-routed-r24.py` next to `mori-routed-check.py`) avoids editing a pre-existing tool. That keeps round 24's operability evidence of "no pre-existing `tools/` file modified" (`round-24-verifier-spotcheck.md:106`). But it adds one routed gate per round, and round 26 would add a third.

**Smallest safe correction.** Leave round 25's targets alone; the contract has landed and narrowing is forbidden. The round-25 report should:
1. state the sentinel status in both readings;
2. tell round 26 to work routed defects as uncounted fixes, which the prompt allows ("criterion or fix"), and to aim its counted lowest-tie claim at a different frontier area, for example depth at 5, which has been unclaimed for many rounds.

## Classification for the canonical judge

- **Fixable before code:** F1, F2 and F6, by contract amendment or plan ordering. None narrows a target.
- **Tradeoffs to disclose:** F3, F4, F5 and F7. They do not block admission if they are disclosed, but each limits what "held" proves.
- **Sentinel:** reading-dependent. It tripped under the class reading and is a matter for round 26.
