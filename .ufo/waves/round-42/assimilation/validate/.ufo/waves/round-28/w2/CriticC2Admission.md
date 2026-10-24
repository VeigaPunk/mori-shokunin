**Verdict: partial.** Attacked: the C2 admission at `f2de0eedcd60d2e354da75265ea6122bc3896073`. The counter result holds.
The freeze order holds as far as it can be observed. No tool change happened after the freeze, and `C2=met` follows
amendment A2. Two parts break as written. First, the "ten blind writers" provenance is stated without the disclosed
taints. Second, the contract's "freeze hash in LOG.md in the freeze batch" condition is not met.

Seat: MoriR28.CriticC2Admission (critic, leaf). Wave 2. Clock at the counter run: `2026-10-22T18:52:35Z`.
Scratch: `/fast/scratch/hyaku/mori-r28-w2/CriticC2Admission/` (committed copies of the ten case reports and the frozen file).
Tools installed or updated: none.

## 1. Counter, case file and tool after the freeze: holds

- I ran `bash .ufo/waves/round-28/count-c2.sh f2de0eed…`. The working-tree counter is byte-equal to the committed one
  (`diff` gave no output). Output: `freeze_commit=d21b8bd3…`, `freeze_blob_versions=1`, `cases_changed_since_freeze=0`,
  `tool_blob=3fb78bbc…`, `tool_blob_at_freeze=3fb78bbc…`, `frozen32_selftest=PASS 32/32`, `a2_cases=30`,
  `a2_rules_covered=10/10`, `a2_selftest=PASS 30/30`, `C2=met`, `exit=0`.
- `git diff --stat 6ebd518f f2de0eed -- tools/` lists only `tools/fixtures/mori-oom-killers/cases-a2.json | 1287 +`.
  `tools/mori-oom-killers.py` did not change at all in round 28. In the working tree its mtime is
  `2026-10-22 11:38:47 -0300`, which is before round 28.
- Assembly check: I took the single fenced JSON array from each committed `CaseA2rNN.md` and compared it with
  `cases-a2.json` at `d21b8bd3` after canonicalising both (`json.dumps(sort_keys=True)`). All 30 ids are equal. The
  frozen file has no id that is missing from the reports. So LOG.md:1887-1888, "assembled without edits", holds.
  The frozen file's sha256 is `ec04a74a3eb65f856dedb3f0509122ee07fdfba7f49e90781d86ab2a393ea6aa`.

## 2. Freeze order: holds on what can be observed; one declared condition is missed

- Commit order (from `git log`, committer times):
  - `7b75f45a`, the counter plus its before receipt: 15:50:53 -0300.
  - `d21b8bd3`, the freeze (`LOG.md` + `cases-a2.json` only): 15:50:55.
  - `f2de0eed`, the selftest receipt: 15:51:32.
- `evidence/c2-freeze-selftest.txt:1` records the first tool run at `2026-10-22T18:51:02Z` on a temporary extract of
  `d21b8bd3`. Its file mtime is 15:51:02.38 -0300, which is consistent.
- `evidence/c2-before-r28.txt:1` records a run at `18:50:44Z`, but at `6ebd518f`, which has no A2 cases
  (`a2_schema=absent`). So that run is not a run on the frozen cases.
- The negative cannot be proven. The jj operation log (`jj --ignore-working-copy op log`) shows working-copy snapshots
  only at commit time: 15:34:21, then 15:50:53, then 15:50:55. Also, `snapshot.auto-track` is `none()`, so untracked
  files never appear in snapshots. The lane copy of `cases-a2.json` has mtime 15:50:55.18 -0300, about 0.03 s
  before the freeze snapshot (op `88ce5ac3747c`, 15:50:55.215).
- So "no tool run on it exists before this commit" (LOG.md:1888) is consistent with the evidence but cannot be checked.
  A run on a scratch assembly between 15:34 and 15:50 would leave no trace in the lane. [INFERENCE] Nothing points
  to such a run. This is a limit of the method, not a defect.
- **Missed condition.** The C2 statement (contract.md:39-40) requires "the freeze hash is written to `LOG.md` in the
  freeze commit's own batch". The freeze batch's LOG lines (LOG.md:1887-1888) give a commit time and a case count.
  They contain no hash: no content sha256, and no commit id. A commit id cannot hold itself (amendment A1's own
  reasoning, contract.md:97-99). But the content sha256 could have been written in the batch, and it was not. The
  counter does not test this condition. This is a literal miss of a declared condition. It is fixable only by an
  honest correction, because the batch cannot be rewritten.

## 3. Blindness evidence: none of the ten writers opened the tool, but three read outside their brief, and the L1 recorded no taint

All ten reports declare that they did not open the tool. Locations: r01:15-19, r02:191-194, r03:174-179, r04:137-141,
r05:200-204, r06:180-184, r07:242-246, r08:146-150, r09:161-164, r10:14-16.

The per-seat brief (wave1-spec.json, the CaseA2r03 prompt) says: "You may read ONLY" the round-27 contract lines
40-80, the round-26 contract, the round-26 `cases.json`, and the upstream earlyoom v1.9.0 sources. The C2 statement
(contract.md:37-38) repeats this: "they read only the rule text, the round-26 contract and the round-26 frozen case file".

| writer | read beyond the brief | when | what it exposes about the tool | disclosed? |
|---|---|---|---|---|
| CaseA2r01 | `CriticC2Design.md` (`head -25`, `tail -20`) (r01:36-47, r01:219-220) | "after the case file was finalised"; the case file and the report landed together in `1c4c186e`, so this order is self-reported only | the field-map verdict for A2-07, A2-08, A2-09; nothing on A2-01 | in the report; not in LOG or the lesson |
| **CaseA2r03** | `CriticC2Design.md` lines 1-45 (r03:187-196) | "**before** I had seen the case file schema and before I wrote any case" (r03:190) | CriticC2Design.md:36-40 names the output columns and says an unknown path from `_lookup` fails as "missing in result"; :13-18 covers A2-07 and A2-10 behaviour | in the report, which asks the L1 to "weigh that before freezing" (r03:194-196); not in LOG or the lesson |
| CaseA2r07 | `.ufo/waves/round-27/count-c2.sh` (r07:259-260) | while writing | only the selftest invocation and coverage logic (r27 count-c2.sh:33-51); no output values | in the report only |
| CaseA2r04, r05, r06, r07 | `.ufo/waves/round-28/contract.md` (r04:149-150, r05:212, r06:194, r07:256-257) | while writing | amendment A1 (contract.md:94-96) gives a fact derived from the tool: "`actions.sigterm` does not decide A2-07". r07 writes the A2-07 cases | sanctioned by the wave context ("Claim contract (read it first)", wave1-spec.json `context`) |

- The strongest counterexample is CaseA2r03. CriticC2Design.md:7-9 says of itself: "The CaseA2r* writers must not
  open it before the freeze commit. If a writer's transcript shows a read of this file, that writer's cases are
  tainted". CaseA2r03 read it before writing any case.
- Despite that, the freeze commit subject ("30 blind cases") and LOG.md:1888 ("the ten blind CaseA2rNN reports") state
  that all ten writers were blind. A `grep -i taint|CriticC2Design|blind` over `corpus/lessons/round-28.md` finds no
  record of the taint, and neither does the same grep over LOG.md. That is false provenance by omission.
- Effect on the case values: low. Lines 1-45 say nothing about A2-03 or `earlyoom.process_group_lines`; I read them at
  `1c4c186e:CriticC2Design.md`. r03's derivation tables cite contract lines for every pinned value. The A2 rulings do
  not depend on this, because no case mismatched.
- Duplicate authority: the wave context told every seat to read the round-28 contract first, while the case brief said
  "read ONLY" four sources. The L1's own instructions therefore carried a fact derived from the tool (A1's A2-07 field
  map) to the A2-07 writer. The impact is small (it names which field to pin, not its value), but the C2 statement's
  "read only" is false for r04 through r07 as written.

## 4. Whether `C2=met` follows amendment A2: holds, but the result is saturated

- Amendment A2 (contract.md:102-114) applies only when a frozen case and the tool mismatch. The result is PASS 30/30,
  so there is no mismatch. No `tool error`, `case error` or `unclear text` ruling is triggered, and no tool change was
  made. The guards for a tool change (PASS 32/32, and no `KILLER_ACTED` turning into QUIET or UNKNOWN) are therefore
  never exercised. `C2=met` is consistent with A2.
- Saturation (a tradeoff, not a defect). Wave-1 `ReviewA2SpecVsTool.md` found three shapes where the tool diverges
  from the rule text. None of the 30 frozen cases exercises any of them:
  - A2-04 (ReviewA2SpecVsTool.md:18): an `escalating to SIGKILL after` line inside a dry-run invocation still feeds
    `acted`. No A2-04 case contains an `escalating` line (checked by scanning the inputs).
  - A2-10 (ReviewA2SpecVsTool.md:24), two shapes: stamp-less records under an unbounded scope (AETM missing or 0), and
    stamp-less records that land in the earlier-invocation count of a non-active unit. All three A2-10 cases are
    `ActiveState=active` with AETM above 0, and every record carries `__MONOTONIC_TIMESTAMP`. They are all
    bounded-branch shapes, where the reviewer found no divergence.
- Also, one of the three A2-07 cases does not pin the required field (`a2_A2-07=… field=2`). The counter's floor of
  one pinning case allows this.
- So `C2=met` shows that the tool agrees with 30 blind cases. It does not show that A2-04 or A2-10 hold on the shapes
  already known to break them.

## Impacted axes

- **Operability** (C2's axis): the claim as counted is met; the measured value is real.
- **Calibration**: harmed if the round is admitted with "ten blind writers" and "C2 pins the ten rules" unqualified.
  The disclosed r03 pre-case taint, the r01, r07 and r04-r07 extra reads, the missing freeze hash, and the known
  unpinned A2-04 and A2-10 shapes would all be erased from the record.
- **Freshness, depth, coverage, adjacency**: not touched by C2 (the tools diff is case file only). The retention scan
  was not measured by this seat.

## Smallest safe correction (the case file and tool stay as they are; integration is the L1's)

1. Add a dated LOG and lesson line in a later batch, without rewriting `d21b8bd3`'s lines. It should say:
   - The freeze batch omitted the freeze hash. The case file's sha256 is `ec04a74a3eb6…` (full value in §1); it is
     a single blob since `d21b8bd3`.
   - CaseA2r03 read CriticC2Design.md:1-45 before writing (r03:187-196), and CaseA2r01 read part of it after
     finalising (r01:36-47).
   - CaseA2r07 read the round-27 counter.
   - CaseA2r04 through r07 read the round-28 contract under the wave context.
   - Blindness is therefore "no writer opened the tool; three read outside the brief", not "ten blind".
2. Name, in the lesson or SCORECARD, the open shapes that `C2=met` does not pin: A2-04 escalation in dry-run, and
   A2-10 stamp-less records under an unbounded scope or on a non-active unit. Route them to a later round's blind
   cases, and do not claim the ten rules are fully pinned.
3. The canonical judge decides whether the r03 pre-case read and the missing freeze hash make C2 a miss under
   contract.md:37-40. My reading: the hash condition is a literal miss and the r03 read is a literal breach of "read
   only", but the r03 read has low impact on A2-03 values. I do not apply that ruling here.

## Checks not run

- I did not run the retention scan or the round-26 selftests independently. The counter output covers
  `frozen32_selftest` only.
- I did not open any writer's transcript. The finalisation order for r01 and r03 is self-reported.
