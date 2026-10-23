# ScribeLesson — round 36 lesson draft

**Item attacked:** whether the round-36 Gate can treat C1's byte-behavior receipt as freshness admission, and whether the C1/C2 gate decisions and the two candidate mistake rows are supported by the recorded artifacts.

**Axes:** C1 is exploratory freshness technique only; C2 is measured operability. Calibration requires keeping byte evidence separate from a freshness verdict. This is a draft for L1 to copy or reconcile, not a canonical closure judgment.

## Gate

### C2 — SOURCES append-only gate

**Decision:** admitted as a measured operability capability. The frozen P-C2 receipt records a 24/24 blind match and an exact real-arm match to its independent oracle at the stated historical revision. This supports the bounded predicate; it does not claim every possible history edge.

Archived measurement command (not run by this seat):

```text
python3 .ufo/waves/round-36/count-c2.py bf0df77fee4b6ef54a90aea09335c7617f125151
```

Observed in `evidence/c2-after.txt:2-9`:

```text
blind arm: 24/24 sandbox histories matched the hidden truth (1.6s; coverage: deletions=22 changed-back=17 superseded=10)
real arm: pass (0.2s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
C2=met
seed=15440749816798970567
```

`tool exit=1` is the gate's finding-bearing exit; the receipt labels the counter result `C2=met`. The command and result are also recorded in `w2/CritAdmission.md:28`.

### C1 — source-drift byte probe

**Decision:** the exploratory technique may be recorded, but C1 is **unprovable** at this evidence snapshot—not admitted as a freshness verdict. P-C1 verifies byte-classifier behavior only. The required named non-author reviewer for `unprovable-but-better` is absent from the inspected record (`w2/CritAdmission.md:15,19`; `w2/RevExploratoryHonesty.md:104-109`). The pre-data axis-fit finding explains why the declaration was narrowed; it does not convert `C1=met` into freshness evidence.

Archived measurement command (not run by this seat):

```text
python3 .ufo/waves/round-36/count-c1.py bf0df77fee4b6ef54a90aea09335c7617f125151
```

Observed in `evidence/c1-after.txt:2-6`:

```text
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
real_rows=220 oracle_fetched=58 oracle_fresh=49 oracle_drifted=9 oracle_excluded=0 tool_exit=1 tool_rows=220 mismatches=0
C1=met
seed=7388485190103051243
C1_EXIT=0
```

The recorded `C1=met` is the frozen byte predicate's token, not freshness admission (`contract.md:119-130`; `w2/RevC1Receipt.md:26`). `w2/CritAdmission.md:30` records the same command and outcome. Do not infer source staleness or a freshness-axis gain from the nine `oracle_drifted` rows.

**Disposition boundary:** retain C2's measured result; keep C1's exploratory byte evidence distinct from claim verification. At this snapshot, no qualifying outside judgment is recorded, so the record does not establish overall round admission. Leave the outside closure to decide the final disposition.

**Spot-check result: left for the outside closure.**

## Mistakes

| id | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M-a | axis-fit | `w1/CritAxisFit.md:18-48`: S156's pinned source bytes match its round-30 recorded digest, but the annotated excerpt copy is classified `drifted`; the byte predicate therefore detects representation mismatch, not stale skill claims. The pre-data declaration is recorded at `contract.md:119-130`. | none — found pre-data by the wave-1 critic and converted into the exploratory declaration before the tool landed | Preserve the frozen predicate and report its output as byte-behavior evidence only. For a future freshness claim, compare like representations and connect a live source witness to the skill assertion being checked; never infer freshness admission from `C1=met`. |
| M-b | landing | `dispatch-log.txt:20-29`; `w2/RevWave1Audit.md:79-96`: attempt 1 did not deliver/land the drift tool. A scratch build existed, so the precise failure is non-delivery, not “never built”; attempt 2 rebuilt the landed tool to the frozen interface. | addendum §5 — earlier-attempt inheritance | Apply the inheritance rule explicitly: inventory and re-verify the carried contract, frozen counters, receipts, and reports; distinguish scratch artifacts from landed deliverables; land the missing tool and self-test it before scoring data at the landed tip. |

## Findings, conflicts, and limits

- The C2 and C1 commands/results above are archived measurements from the cited receipt/review artifacts. This seat ran no counter, gate, self-test, live fetch, build, test, or other measurement.
- The candidate lessons preserve the boundary: C2 is admitted on P-C2; C1 remains unprovable absent the outside review and carries no freshness verdict.
- Record this status wording distinction verbatim for closure: current `corpus/lessons/round-36.md:10` says **“admitted as technique; claim lands `unprovable`”**; `w2/CritAdmission.md:19` says **“recommend **admitted=false / rejected-honest-stop**”** because no qualifying outside judgment was found. The draft above distinguishes retaining a technique from admitting the round; it does not substitute for the outside closure.
- Out of scope: adding other Gate rows (SOURCES S205–S220 and README coverage), adjudicating the outside spot-check, or making a canonical round judgment.

## Touched surfaces and artifact paths

- Only this report was written: `.ufo/waves/round-36/w2/ScribeLesson.md`.
- Read-only source artifacts: `.ufo/waves/round-36/contract.md`; `.ufo/waves/round-36/evidence/c1-after.txt`; `.ufo/waves/round-36/evidence/c2-after.txt`; `.ufo/waves/round-36/dispatch-log.txt`; `.ufo/waves/round-36/w1/CritAxisFit.md`; `.ufo/waves/round-36/w2/CritAdmission.md`; `.ufo/waves/round-36/w2/RevC1Receipt.md`; `.ufo/waves/round-36/w2/RevExploratoryHonesty.md`; `.ufo/waves/round-36/w2/RevWave1Audit.md`; `corpus/lessons/round-36.md`.
- No tools were installed or updated.

VERDICT: PASS — no defect found in this draft's evidence boundaries; C1 is explicitly not represented as a freshness verdict, and C2 is limited to its frozen measured predicate. The outside admission/spot-check decision remains unmade here.
