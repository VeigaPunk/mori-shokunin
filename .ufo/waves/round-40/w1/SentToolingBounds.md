# SentToolingBounds — round-40 wave prompt review

## Verdict

**Not fully bounded at the per-seat task level.** The shared `context` contains the required prohibitions, so they apply when the dispatcher supplies it with every item. The prompt generator stores that context separately from `items[].prompt`, however, and several task instructions leave output destinations or lane paths relative/unspecified. No seat action or unauthorized write was performed during this review.

## Findings

### Medium — temporary and draft outputs are not consistently confined

**Exploit path:** a seat follows a task literally from the documented fleet-root working directory. `LabDagDeterminism` asks it to build five DAGs in isolated `.scratch` directories, and `ExeDagDeterminism` asks for an isolated `.scratch` directory, without giving an absolute lane path. Since the shared context explicitly says a relative path resolves under the fleet repo, a literal `.scratch` can create files in the read-only fleet root. `ExeDagN` supplies an unresolved `<out>` argument; `ExeDagP` and `ExeDagR` say only `run-c11-dags.py dag-p/dag-r`. Their “Re-derive” targets are under `evidence/`, outside the executor write allowance, so an agent might overwrite frozen receipts instead of emitting to scratch and comparing.

Other write-intent ambiguity: `ScrScorecardRow` says “Draft the SCORECARD.md ... rows,” `ScrLessonDraft` says “Draft corpus/lessons/round-40.md ...,” and `ScrLandedChanges` asks for a draft without an output path. The shared bounds classify read-only seats and executors but do not state what a `scribe` may write. Construct/copy tasks for `CritNewSurvivor`, `CritNewDag`, `CritConjunctSemantics`, `CritDrainedTuple`, `MutGateReadd`, `MutGateEligible`, `MutGateFirstParent`, and `MutConformArms` likewise do not name a temporary output directory or authorize their non-executor roles to write there.

**Impact:** accidental fleet-root writes, frozen-evidence replacement, or unauthorized edits to lane production files are plausible; none was observed. The task could also produce incomplete evidence if an agent avoids the ambiguous operation.

**Smallest remediation:** explicitly allow all temporary fixture/copy outputs only under the absolute lane path `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/`; require re-derivations to write there and compare against `evidence/` read-only. State that scribe/critic/mutation-tester outputs are report-only under `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/w1/` unless a separate write is expressly authorized; do not direct them to edit production files.

### Low — shared guardrails are a separate field, not in each stored prompt

**Evidence:** `gen-wave-spec.py:41-44` constructs each `items[].prompt` from `GODSPEED + task + Report trailer`; `gen-wave-spec.py:158-159` stores `CONTEXT` separately as the spec-level `context`. The spec has 66 items. The shared context itself correctly says the fleet is read-only, prohibits sibling-lane writes and lane Git/jj mutations, requires absolute lane paths, limits executor writes to one item artifact under `w1/` or `.scratch/`, and says `never run pacman` (`gen-wave-spec.py:21-26`).

**Exploit path:** a dispatcher or downstream consumer that forwards only `items[].prompt` drops those protections. The current assignment included the shared context, so this omission was not observed in this invocation; it is a packaging dependency, not evidence of a live dispatcher failure.

**Impact:** if context is omitted, item prompts do not independently enforce the no-pacman/no-fleet-write rules or a write scope.

**Smallest remediation:** make the dispatcher prepend/attach `spec.context` to every item prompt and assert this during wave generation/dispatch; optionally include a short explicit write prohibition in each prompt as defense in depth.

### Low — relative path instructions conflict with the stated absolute-path rule

The context says the tools start at the fleet root and that relative paths resolve in the fleet repo (`gen-wave-spec.py:24`), but multiple tasks name lane inputs/outputs relatively. Examples include `ScoutPriorWaves` (`.ufo/waves/...`), `ScoutCorpusFrontier` (`corpus/README.md`), `ScoutQualityBar` (`corpus/QUALITY.md`), `ScoutDriftProbe` and `SimpGateV3` (`tools/...`), `RevFindingsCoverage`, `RevLessonGate`, `RevErratum`, and `RevKnowledgeProvenance` (`corpus/...`), and `ScrReportWork` (relative `w1/` output). `ExeExtractPins` and `ExeFreezePins` use `git show <rev>:<path>` without specifying the lane repository; `ScoutDriftProbe` and `RevGateDiff` similarly give `git log/diff` commands without `git -C <lane>`. `ExeParity` names `count-c7`/`count-c8` but not their paths. `ExeDagDeterminism` and `LabDagDeterminism` use relative `.scratch`.

**Impact:** read-only commands can inspect the fleet repo instead of mori and yield false/no findings; relative output paths can target the fleet. No such commands were run here.

**Smallest remediation:** use absolute lane paths for filesystem inputs/outputs and `git -C /home/vgpnk/Projects/shokunin/mori-shokunin ...` for Git commands. Keep the report-trailer-relative path as the documented exception, resolved beneath `reportDir`.

## Check of required prohibitions

- **Pacman:** explicitly forbidden in the shared context; no task asks to use it.
- **Fleet/sibling writes:** explicitly forbidden in the shared context; `ConnSiblingOverlap` also says not to edit sibling repos. No task expressly asks to write to the fleet or a sibling, but the relative `.scratch` case above can conflict with this prohibition.
- **Write locations:** executor-only allowance is present in shared context, but scribe and fixture-building critic/mutation tasks have the ambiguities described above.
- **Absolute paths:** the shared rule is explicit and all generated report trailers include the absolute lane root. Numerous task-specific paths/commands do not satisfy the rule; see the examples above.

## Evidence and commands

No shell commands were run; this was a static, read-only prompt review. No tools were installed and no checks/builds/tests were run.

Inspected with `read`:

- `.../.ufo/waves/round-40/w1-spec.json` — `reportDir` is `.ufo/waves/round-40/w1`; the top-level spec has `context` and `items`.
- `.../.ufo/waves/round-40/gen-wave-spec.py:19-35` — shared roots, absolute-path rule, write bounds, and pacman prohibition.
- `.../.ufo/waves/round-40/gen-wave-spec.py:41-44` and `:154-159` — item prompt assembly and separate `context` field.
- `.../.ufo/waves/round-40/gen-wave-spec.py:55-85`, `:87-123`, and `:125-152` — executor, scribe, scout, reviewer, critic, mutation, sentinel, and lab task instructions cited above.
