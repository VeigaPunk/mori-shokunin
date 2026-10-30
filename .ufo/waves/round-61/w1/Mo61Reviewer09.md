# Mo61Reviewer09 — wave-shape conformance

## Findings (severity order)

No actionable wave-shape defect found in the assigned dispatch artifact.

Axes: seat-band conformance; role diversity/attack share; connector scarcity; identity uniqueness; metadata/registry consistency.

Evidence file: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/w1-dispatch.json` (SHA-256 `c21329857418461e073dd71c7195cbc434d7d30ed57d5626f19220ba143c4121`). All line references below refer to this absolute path unless otherwise stated.

| Measure | Observed |
|---|---:|
| Task seats | 64 |
| Registry members | 64 |
| Declared spawn / resume / total | 64 / 0 / 64 |
| scribe | 13 |
| executor | 12 |
| scout | 5 |
| connector | 2 |
| revenger | 3 |
| simplifier | 2 |
| reviewer | 9 |
| critic | 7 |
| mutation-tester | 8 |
| sentinel | 3 |
| labrat | 0 |
| Attack roles | 30 / 64 = **46.875%** |
| Duplicate task names | 0 |
| Duplicate JSON keys (including registry names) | 0 |
| Unknown roles | 0 |
| Task/registry name differences or role mismatches | 0 |

Attack count uses exactly reviewer + critic + mutation-tester + sentinel + labrat + revenger: 9 + 7 + 8 + 3 + 0 + 3 = 30, exceeding the frozen 25% floor. The two seats named `Mo61LabPressure` and `Mo61LabDeterminism` are explicitly **executor**, not labrat, and were not counted as attackers (:734–740).

Policy v2 **64–128 band applies**: metadata :8–9 sets `waveMinLanes=64`, `waveMaxLanes=128`; 64 is inside that inclusive band. The frozen contract `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/contract.md:127–132` explicitly identifies policy v2 and the same band. Global `minLanes=16`, `maxLanes=256` (:6–7) do not replace the wave-specific band. Counts :16–20 agree with parsed task and registry counts. Connector identities are `Mo61ConnSibling` and `Mo61ConnConsider` (:548–556): 2/64 = 3.125%; the contract says “few” without a numeric cap.

Role-definition line pointers (all task-side `agent` fields):
- scribe: 425,430,435,440,445,450,455,460,465,470,585,590,595
- executor: 475,480,485,490,495,500,505,510,515,520,735,740
- scout: 525,530,535,540,545
- connector: 550,555
- revenger: 560,565,570
- simplifier: 575,580
- reviewer: 600,605,610,615,620,625,630,635,640
- critic: 645,650,655,660,665,670,675
- mutation-tester: 680,685,690,695,700,705,710,715
- sentinel: 720,725,730

## Commands and measured output

Read-only Python JSON analysis was executed through the eval tool, using `json.loads(text, object_pairs_hook=hook)`; `hook` counted duplicate keys before constructing each dictionary. Tasks were counted from `taskCall.tasks`, roles from each task's `agent`, registry roles from `registry.members[*].role`, and task-name duplicates with `collections.Counter`. Unknown roles were checked against `{scribe,executor,scout,connector,revenger,simplifier,reviewer,critic,mutation-tester,sentinel,labrat}`. Name sets and every task/registry role pair were compared.

Core expressions (with `d` the parsed file):
```python
tasks = d['taskCall']['tasks']
members = d['registry']['members']
roles = collections.Counter(t['agent'] for t in tasks)
attack = {'reviewer','critic','mutation-tester','sentinel','labrat','revenger'}
len(tasks), len(members), sum(roles[r] for r in attack)
```
Measured output:
```text
tasks=64 registry_members=64 attack_count=30 attack_share=0.46875
connectors=2 duplicate_task_names=[] duplicate_json_keys=[] unknown_roles=[]
registry_only=[] task_only=[] role_mismatches=[] resume_sends=0
```
Registry and task role-count dictionaries were identical. No counter execution, fixture, git mutation, production edit, or tool installation was needed. Seat scratch was created, TMPDIR set to `/fast/scratch/hyaku/mori-r61/Mo61Reviewer09`, then the empty seat directory removed successfully.

## Residual risk and verification gaps

- This is static dispatch-shape evidence, not proof of 64 actual launches, concurrent liveness, settlement, saturation, or same-identity rerouting. No such runtime claim is made. There are zero resume seats and zero `resumeSends` (:745), so no resume-continuity preflight is exercised by this artifact.
- `xd://lsp` was attempted and returned `No such tool`; semantic status/references/definition/diagnostics were unavailable. JSON structural analysis, not grep, supplies the count evidence.
- Dispatch metadata does not carry an explicit numeric policy-version field; the v2 designation is grounded in the frozen contract, and its band is independently present in the dispatch metadata.
- “Few connector seats” has no frozen numeric threshold; the exact count and share are reported rather than inventing one.

Self-evaluation: accuracy 4/5 (static evidence cannot establish launches); completeness 5/5 (all assigned measures reported); clarity 4/5 (line inventory is lengthy but supports audit); actionability 5/5 (exact values and source pointers); conciseness 4/5 (reproducibility adds length). Overall 4.4/5. Improvement priority: preserve distinction between declared shape and runtime evidence; do not promote this report to a saturation claim. Would the user agree? Expected yes for this scoped static review.
