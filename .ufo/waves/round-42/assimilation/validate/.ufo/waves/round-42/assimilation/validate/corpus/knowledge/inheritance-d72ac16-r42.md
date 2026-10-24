# The d72ac16 inheritance — 145 unnamed files, named

source: fleet lane git commit d72ac167535229d737b9fa844513431d9a12f5ea (round-41 attempt-1 freeze)
verified-at: 2026-10-24
recheck: git -C <lane> diff-tree --no-renames --no-commit-id --name-only -r d72ac167535229d737b9fa844513431d9a12f5ea | wc -l -> 165

Commit `d72ac16` added 165 paths in one freeze commit. 20 of them were the
round-41 freeze set (named in `evidence/freeze-r41.txt` and the round-41
declaration); the other 145 were inherited uncommitted lane outputs swept in
unnamed — the round-41 closure routed that as defect 4. This manifest names
every one of the 145, by category and provenance, and names no path the
commit did not add. The content itself is benign (closure finding); only
the naming was missing. Provenance per category:

### seat_reports

67 paths — round-40 wave-1 seat reports, authored by the round-40 wave's seats and swept unreviewed into the r41 attempt-1 freeze commit.

```
.ufo/waves/round-40/w1/ConnSiblingOverlap.md
.ufo/waves/round-40/w1/ConnW04Routing.md
.ufo/waves/round-40/w1/CritConjunctSemantics.md
.ufo/waves/round-40/w1/CritDrainedTuple.md
.ufo/waves/round-40/w1/CritExploratoryBoundary.md
.ufo/waves/round-40/w1/CritFreezeTiming.md
.ufo/waves/round-40/w1/CritLaneLine.md
.ufo/waves/round-40/w1/CritNewDag.md
.ufo/waves/round-40/w1/CritNewSurvivor.md
.ufo/waves/round-40/w1/CritPredParenthetical.md
.ufo/waves/round-40/w1/CritScoringHonesty.md
.ufo/waves/round-40/w1/ExeCensus.md
.ufo/waves/round-40/w1/ExeConformMet.md
.ufo/waves/round-40/w1/ExeConformSelftest.md
.ufo/waves/round-40/w1/ExeConjunctAfter.md
.ufo/waves/round-40/w1/ExeDagDeterminism.md
.ufo/waves/round-40/w1/ExeDagN.md
.ufo/waves/round-40/w1/ExeDagP.md
.ufo/waves/round-40/w1/ExeDagR.md
.ufo/waves/round-40/w1/ExeExtractPins.md
.ufo/waves/round-40/w1/ExeFreezePins.md
.ufo/waves/round-40/w1/ExeGateE37.md
.ufo/waves/round-40/w1/ExeGateLane.md
.ufo/waves/round-40/w1/ExeGateSelftest.md
.ufo/waves/round-40/w1/ExeParity.md
.ufo/waves/round-40/w1/ExeSelftestTiming.md
.ufo/waves/round-40/w1/ExeSurvivorSweep.md
.ufo/waves/round-40/w1/ExeWitnessBytes.md
.ufo/waves/round-40/w1/LabDagDeterminism.md
.ufo/waves/round-40/w1/MutConformArms.md
.ufo/waves/round-40/w1/MutGateEligible.md
.ufo/waves/round-40/w1/MutGateFirstParent.md
.ufo/waves/round-40/w1/MutGateReadd.md
.ufo/waves/round-40/w1/RevC1Receipts.md
.ufo/waves/round-40/w1/RevC2Receipts.md
.ufo/waves/round-40/w1/RevCensusPair.md
.ufo/waves/round-40/w1/RevConformDiff.md
.ufo/waves/round-40/w1/RevContractConformance.md
.ufo/waves/round-40/w1/RevErratum.md
.ufo/waves/round-40/w1/RevFindingsCoverage.md
.ufo/waves/round-40/w1/RevFreezeHonesty.md
.ufo/waves/round-40/w1/RevGateDiff.md
.ufo/waves/round-40/w1/RevKnowledgeProvenance.md
.ufo/waves/round-40/w1/RevLessonGate.md
.ufo/waves/round-40/w1/RevParityScope.md
.ufo/waves/round-40/w1/RevPriorIntent.md
.ufo/waves/round-40/w1/RevRoutedCoverage.md
.ufo/waves/round-40/w1/RevScorecardClaims.md
.ufo/waves/round-40/w1/RevShonenBoxes.md
.ufo/waves/round-40/w1/RevWaveDedup.md
.ufo/waves/round-40/w1/ScoutCorpusFrontier.md
.ufo/waves/round-40/w1/ScoutDriftProbe.md
.ufo/waves/round-40/w1/ScoutInstrumentLayout.md
.ufo/waves/round-40/w1/ScoutPriorWaves.md
.ufo/waves/round-40/w1/ScoutQualityBar.md
.ufo/waves/round-40/w1/ScoutSiblingConform.md
.ufo/waves/round-40/w1/ScrErratumCheck.md
.ufo/waves/round-40/w1/ScrLandedChanges.md
.ufo/waves/round-40/w1/ScrLessonDraft.md
.ufo/waves/round-40/w1/ScrReportWork-work-performed.md
.ufo/waves/round-40/w1/ScrReportWork.md
.ufo/waves/round-40/w1/ScrScorecardRow.md
.ufo/waves/round-40/w1/ScrSourcesRow.md
.ufo/waves/round-40/w1/SentArtifactSafety.md
.ufo/waves/round-40/w1/SentToolingBounds.md
.ufo/waves/round-40/w1/SimpConformV3.md
.ufo/waves/round-40/w1/SimpGateV3.md
```

### r40_evidence_scratch

7 paths — round-40 evidence and mutation-scratch files (freeze receipt and mutconform-arms2 scratch), same sweep.

```
.ufo/waves/round-40/evidence/freeze-r40.txt
.ufo/waves/round-40/scratch/mutconform-arms2/cond-mutant.txt
.ufo/waves/round-40/scratch/mutconform-arms2/cond-pristine.txt
.ufo/waves/round-40/scratch/mutconform-arms2/conform-mut-cond-unconditional.py
.ufo/waves/round-40/scratch/mutconform-arms2/conform-pristine.py
.ufo/waves/round-40/scratch/mutconform-arms2/selftest-mutant.txt
.ufo/waves/round-40/scratch/mutconform-arms2/selftest-pristine.txt
```

### scratch

71 paths — round-40-era scratch fixtures under .scratch/, same sweep; only .scratch/round22/ was named at the time (LOG.md round-41 entry).

```
.scratch/CritConjunctSemantics/conform-v3-commentonly.py
.scratch/CritConjunctSemantics/conform-v3-renamed.py
.scratch/CritConjunctSemantics/conform-v3-unwired.py
.scratch/CritConjunctSemantics/renamed-audit.err
.scratch/CritConjunctSemantics/renamed-audit.out
.scratch/CritConjunctSemantics/renamed-selftest.out
.scratch/CritConjunctSemantics/unwired-audit.err
.scratch/CritConjunctSemantics/unwired-audit.out
.scratch/CritConjunctSemantics/unwired-selftest.err
.scratch/CritConjunctSemantics/unwired-selftest.out
.scratch/CritDrainedTuple/counter-drained-tuple.py
.scratch/CritDrainedTuple/counter-tuple-rebind.py
.scratch/CritDrainedTuple/fat-tool.py
.scratch/CritFreezeTiming/c11-before-lane-repro.txt
.scratch/CritFreezeTiming/c11-red-repro.txt
.scratch/CritFreezeTiming/survivors-build.log
.scratch/CritFreezeTiming/survivors/survivor-barecomm.py
.scratch/CritFreezeTiming/survivors/survivor-cond.py
.scratch/CritFreezeTiming/survivors/survivor-decoy.py
.scratch/CritFreezeTiming/survivors/survivor-divzero.py
.scratch/CritFreezeTiming/survivors/survivor-inf.py
.scratch/CritFreezeTiming/survivors/survivor-second-popen.py
.scratch/CritFreezeTiming/survivors/survivor-shadow-neg.py
.scratch/CritFreezeTiming/survivors/survivor-shadow-none.py
.scratch/CritFreezeTiming/survivors/survivor-tuple.py
.scratch/CritFreezeTiming/survivors/survivor-underscore.py
.scratch/CritNewSurvivor/survivor-deadloop-rebind.py
.scratch/CritNewSurvivor/survivor-tupleunpack-none.py
.scratch/CritNewSurvivor/survivor-walrus-none.py
.scratch/ExeDagN-c11-after-fixture-n.txt
.scratch/MutGateFirstParent/dag-mutant.txt
.scratch/MutGateFirstParent/dag-p-pristine.txt
.scratch/MutGateFirstParent/dag-p-restored.txt
.scratch/MutGateFirstParent/gate-v3-mutant-preserved.py
.scratch/MutGateFirstParent/gate-v3-mutant.py
.scratch/MutGateFirstParent/gate-v3-pristine.py
.scratch/MutGateFirstParent/mutation.diff
.scratch/MutGateFirstParent/selftest-mutant-preserved.txt
.scratch/MutGateFirstParent/selftest-mutant.txt
.scratch/MutGateFirstParent/selftest-pristine.txt
.scratch/MutGateFirstParent/selftest-restored.txt
.scratch/MutGateReadd/dag-mutant.txt
.scratch/MutGateReadd/gate-v3-readd-mutant.py
.scratch/SrcGitCommit-git-rev-parse.html
.scratch/c11-after-fixture-r-ExeDagR.txt
.scratch/critnewdag/build-dags.py
.scratch/critnewdag/runlog.txt
.scratch/mutgate-eligible/baseline-dags.txt
.scratch/mutgate-eligible/baseline-selftest.txt
.scratch/mutgate-eligible/gate-mutant.py
.scratch/mutgate-eligible/mutant-dags.txt
.scratch/mutgate-eligible/mutant-e37.txt
.scratch/mutgate-eligible/mutant-lane.txt
.scratch/mutgate-eligible/mutant-selftest.txt
.scratch/mutgate-eligible/mutation.diff
.scratch/mutgate-eligible/restored-dags.txt
.scratch/mutgate-eligible/restored-lane.txt
.scratch/mutgate-eligible/restored-selftest.txt
.scratch/rev-scorecard-claims/dags-v2.txt
.scratch/rev-scorecard-claims/dags-v3.txt
.scratch/rev-scorecard-claims/multicounter.replay.txt
.scratch/rev-scorecard-claims/survivor-barecomm.replay.txt
.scratch/rev-scorecard-claims/survivor-cond.replay.txt
.scratch/rev-scorecard-claims/survivor-decoy.replay.txt
.scratch/rev-scorecard-claims/survivor-divzero.replay.txt
.scratch/rev-scorecard-claims/survivor-inf.replay.txt
.scratch/rev-scorecard-claims/survivor-second-popen.replay.txt
.scratch/rev-scorecard-claims/survivor-shadow-neg.replay.txt
.scratch/rev-scorecard-claims/survivor-shadow-none.replay.txt
.scratch/rev-scorecard-claims/survivor-tuple.replay.txt
.scratch/rev-scorecard-claims/survivor-underscore.replay.txt
```

### freeze

20 paths — the named round-41 freeze set (15 under `.ufo/waves/round-41/`,
`tools/mori-round41-calibration.py`, `tools/mori-sources-appendonly.py`,
`corpus/README.md`, `corpus/SOURCES.md`,
`corpus/knowledge/conform-bindings-r41.md`), enumerated in
`.ufo/waves/round-42/evidence/freeze-r42.txt`; listed here only to bound the
145 — this section's fence is empty by construction.

```
```
