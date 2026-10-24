# MoriR30 round 30, wave 2 — ReviewC1Separability: C1/C2 causal separability

Verdict: **agree — separability holds in both directions, tested not assumed**: with every C2 change reverted the C1 counter still prints `C1=met` exit 0 with byte-identical output; with every C1 file reverted the C2 counter's output is byte-identical (still `C2=unmet`). One off-target defect found (F1, medium): the C2 gate leg is cwd-dependent — the same gate blob at the same commit prints `blind_violations=1` in the lane but `4` in a clone.

## Method

- Base: measured tip `ad0f047` (lane HEAD has since moved to `713be29` wave-2 spec; all experiments pinned at `ad0f047`).
- Sandbox clone (allowed git writes only here): `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --no-hardlinks <lane> /fast/scratch/hyaku/mori-r30-w2/ReviewC1Separability/clone`, branch `sep` at `ad0f047`, clean.
- Counters run from commit blobs: count-c1.sh blob `325168f6` (commit `6c47dd0`), count-c2.sh blob `f4f86b0d` (commit `8ac9535`); both equal the blobs at `ad0f047` (`git rev-parse ad0f047:.ufo/waves/round-30/count-c1.sh count-c2.sh` → `325168f6…`, `f4f86b0d…`).
- The blobs hardcode the lane path (`REPO=` in count-c1.sh:8, `LANE=` in count-c2.sh:133), so per assignment each was copied once to scratch and that one constant repointed to the clone (`count-c1-clone.sh:8`, `count-c2-clone.sh:133`). No other edit.
- Lane runs of the unmodified blobs (read-only) reproduced both receipts first (below). No tools installed (none needed); pacman pause respected; no lane writes except this report.

## Baselines reproduced in the lane (unmodified blobs, rev `ad0f047`)

- count-c1: `rows=13 rows_ok=13 new_ids=5 new_id_rows=13 excerpts_ok=5/5 skill_rows=4`, `C1=met`, exit 0 — matches `.ufo/waves/round-30/evidence/c1-after.txt` (met at `ee61010`, still met at tip).
- count-c2: `C2=unmet`, exit 1; every leg passes (`r29_selftest=PASS 24/24`, older `32/32 / 32/32 / 30/30`, blobs ok, freeze `db1ec469`, 8 cases, provenance 8/8 unselected=0, shape 8/4, base+selftest `PASS 8/8`, shape_verdicts 8/8, differential `94/94 changed=2 disallowed=0 acted_lost=0 errors=0`, receipts 3/3, gate_selftest PASS, gate_mutants 4/4, scanned=4) except `blind_violations=1` — matches commit `0b828c2`'s diagnosis (CaseR30a.md:105).

## Test A — C1 counter under full C2 revert (assignment question 1)

Three clone states, one counter copy, rev = state HEAD:

| state | tree | count-c1 output |
|---|---|---|
| A0 `ad0f047` | C1+C2 intact | `C1=met`, exit 0, 13/13 rows, new_ids=5, excerpts 5/5, skill_rows=4 |
| A1 `4aa2f14` | tool restored to `58b61681` blob + `cases-a2-r30.json` deleted | **byte-identical to A0**, `C1=met`, exit 0 |
| A2 `f8489c3` | A1 + gate `.ufo/waves/round-30/check-blind-wave.sh` deleted | **byte-identical to A0**, `C1=met`, exit 0 |

State proofs at A2: `git rev-parse HEAD:tools/mori-oom-killers.py` = `69296b89…` = `git rev-parse 58b61681:tools/mori-oom-killers.py` (tool truly reverted); `cases-a2-r30=absent`; `gate=absent`.

Answer: **yes — C1 still prints `met` with every C2 change reverted**, including the gate.

Why (code): the C1 counter never touches C2 artifacts. It runs the tool from the entering-tip blob, not the tool at `<rev>` (`tool_data=blob(BASE,TOOL)`, count-c1-clone.sh:186), and reads only the three older fixtures (count-c1-clone.sh:10); a grep of the blob copy for `cases-a2-r30|check-blind-wave` returns no matches. So C2's tool fix, frozen file and gate are outside its input set by construction, and A1/A2 confirm it behaviorally.

## Test B — C2 counter under full C1 revert (assignment question 2)

C1 revert commit `d421703` on the reset clone: entry `corpus/knowledge/earlyoom-invocation-scope-r30.md` deleted; excerpts `S156.txt`–`S160.txt` deleted; `SKILL.md` and `corpus/SOURCES.md` restored to their `6c47dd0` (pre-ee61010) versions — drops the `## Round30` rows and S156–S160 rows, and as a superset also ad0f047's SOURCES R3 note; `corpus/lessons/round-30.md` deleted whole (superset: removes Gate lines and more). Proof the revert bites: count-c1 at `d421703` → `rows=0`, `C1=unmet`, exit 1.

| state | count-c2 output |
|---|---|
| B0 clone `ad0f047` (C1 intact) | 21 lines, `C2=unmet`, exit 1 |
| B1 clone `d421703` (C1 reverted) | **byte-identical** (`diff` → no differences), `C2=unmet`, exit 1 |

Answer: **no — reverting the C1 files does not affect the C2 counter at all** (output identical line for line).

Why (code): count-c2 reads only TOOL, cases-a2-r29, the three older fixtures, cases-a2-r30, the gate, the four w1 reports and three evidence receipts (count-c2-clone.sh:7-12,136); a grep of the blob copy for `SOURCES|SKILL|lessons|sources-r30|earlyoom-invocation` returns no matches. The contract's separability claim ("Neither counter reads the other claim's files", `.ufo/waves/round-30/contract.md` §Why-these-two-claims) is thus verified as code fact and as behavior, both directions.

## F1 (medium) — the C2 gate leg is cwd-dependent; `blind_violations` is not a function of committed bytes

Evidence:

1. Gate blob is one and the same: `git rev-parse` → `dbcbe50e…` at `ad0f047`, at freeze `db1ec46`, and at clone HEAD.
2. Same args (`db1ec46 .ufo/waves/round-30/w1 '^CaseR30[a-d]\.md$'`), two cwds:
   - lane cwd: `scanned=4 blind_violations=1`, sole violation `CaseR30a.md:105:writer-forbidden-opened-path`;
   - clone cwd: `scanned=4 blind_violations=4`, violations `CaseR30a.md:98`, `CaseR30b.md:117`, `CaseR30c.md:78`, `CaseR30d.md:111` (all `writer-forbidden-opened-path`).
3. The four clone-flagged lines are, verbatim, the rule-text file by its absolute lane path (raw reads): CaseR30a.md:98 and CaseR30b.md:117 and CaseR30d.md:111 = `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-30/rule-text.md`; CaseR30c.md:78 = `- /home/…/rule-text.md:1-114`. CaseR30a.md:105 is the closing sentence already adjudicated in `0b828c2`.
4. Mechanism: the gate derives `repo_root=$(git rev-parse --show-toplevel)` from its cwd (gate:240) and sets `rule_abs="$repo_root/$rule_rel"` (gate:86-87); the allowlist admits an opened entry equal to `rule_abs` (gate:23). In the lane, the writers' absolute-lane-path entries match `rule_abs` and pass, so the first (and only) failure per report is a:105. In a clone, `rule_abs` points into the clone, the four lane-absolute entries match nothing → four violations, and the per-report first-forbidden guard (gate:129-130) records a:98 and masks a:105 (98 < 105). `own_scratch` is hardcoded (gate:95-96), so it is not the cwd-dependent part; `rule_abs` is.
5. The counter inherits this: it runs the gate with `cwd=LANE` (count-c2-clone.sh:195,198), so `blind_violations` — printed by the counter (count-c2-clone.sh:210) and used in `gate_ok` (count-c2-clone.sh:200,212) — equals 1 only when the repository sits at its canonical path. My clone baseline B0 prints `blind_violations=4` vs the lane's 1; all other 20 output lines are identical.

Impact: the number C2 currently misses on, and the number the closure will use to judge C2.4, is environment-sensitive, so the C2 receipt is not reproducible outside the canonical lane path — which is exactly how outside verifiers (this wave's reviewers and mutation testers) run it. The verdict (`C2=unmet`) is stable today only because 1>0 and 4>0. Amendment A2's allowlist says an entry passes if it is "the lane path of `.ufo/waves/round-30/rule-text.md`" (contract, A2 G3/G4) — the writers' entries are that path, so the clone behavior is stricter than the spec text, a symptom of deriving the lane path from cwd instead of pinning it (count-c1 pins `REPO`; the gate should pin the lane path the same way).

Recommendation (L1's call; I changed nothing): pin `rule_abs` to the canonical lane constant (or accept both `rule_rel` and the canonical absolute path) so the gate verdict is cwd-independent, then re-run the A2/A3 gate receipts; until then, any `blind_violations` number must be quoted with the cwd it was produced in.

## Residual risk and verification gaps

- Tests pinned at `ad0f047`; `713be29` (wave-2 spec) landed after. Its message says it adds wave-2 spec/dispatch files only; I did not re-derive its diff, so [INFERENCE] it does not touch counter inputs.
- B0's `blind_violations=4` vs lane 1 is attributed to cwd per F1's mechanism evidence (direct two-cwd gate runs on identical bytes), not to my one-line `LANE` edit; I did not run a third variant isolating them.
- I did not run count-c2 at A2 (`f8489c3`, C2 files reverted) — that direction is trivially destructive to C2 and outside the assignment.
- Scratch clone and counter copies remain under `/fast/scratch/hyaku/mori-r30-w2/ReviewC1Separability/`; no lane mutation beyond this report.
