#!/usr/bin/env python3
"""Build the 64-seat round-57 verification wave spec."""
import json
from pathlib import Path
GOD=Path('/home/vgpnk/.agents/skills/godspeed/directive.md').read_text().rstrip('\n')
W=Path('/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-57')
L=Path('/home/vgpnk/Projects/shokunin/mori-shokunin')
F=Path('/home/vgpnk/Projects/shokunin')
assignments=[('reviewer',22),('critic',10),('mutation-tester',8),('executor',6),('scribe',8),('scout',4),('connector',2),('sentinel',2),('revenger',1),('simplifier',1)]
checks=[
'C1 calibration: independently inspect the two round-56 demonstrations and verify the SCORECARD capability row names and evidence pointers; report any false claim.',
'C1 counter attack: find a do-nothing or junk-row fixture that reaches its target; name exact bytes and expected output.',
'C1 mutation: mutate each capability row field (name, evidence path, first-working round) and check whether the frozen counter rejects it.',
'C2 depth: reopen the committed round-56 driver-live report and verify the pairing list and whether unclosed counts mean running work.',
'C2 source-grounding: independently locate one exact quote in the committed source report and test the knowledge claim it supports.',
'C2 counter attack: devise a fixture that makes the entry counter falsely report eight located claims or a mined S548 source.',
'Cross-claim no-harm: inspect the frozen claims, predicates, controls, and round-56 artifacts for scope bleed or axis harm.',
'Frontier: inspect the current SOURCES registry and identify a real in-scope source opened this round that supports one claim; do not write the registry.',
'Round-56 routed defect: inspect exact capability-table defect and recommend a falsifiable correction with evidence.',
'Round-56 routed defect: inspect receipt path/wording defects and provide an independent recheck plan; no edits.',
'Coverage cross-check: inspect FR5 and the driver-liveness probe for one new observability surface genuinely outside current core; report only.',
'No-harm and boundary: check proposed interpretations remain detection/report only and do not claim authoritative settlement semantics owned by kumitate.'
]
items=[]; idx=0
for role,count in assignments:
 for _ in range(count):
  idx+=1; name=f'Mo57{role.title().replace("-", "")}{idx:02d}'; check=checks[(idx-1)%len(checks)]
  if role=='executor': check+=' Execute the frozen C1 or C2 counter on the entering revision and inspect the corresponding counter implementation for the assigned arm; capture exact output and exit code.'
  prompt='/skill:godspeed\n'+GOD+'\n\n'+f'{name}: {check} Read the frozen contract `{W}/contract.md` first. Return concise findings with exact file:line/command evidence, counterexamples and verdict; no production edits or commits.'
  items.append({'name':name,'role':role,'prompt':prompt})
context=f'''# mori round 57 — one v2 verification wave
Lane repo: {L}. Fleet root: {F}. L1: MoriR57. Claims and frozen predicates: {W}/contract.md. Entering branch revision 53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2; freeze landed 618562c72a03dc4d17386b715357f863fd327274. C1 is calibration: round-56 driver-liveness and vote-binding demonstrations appear in SCORECARD capabilities with resolving evidence and first-working round 56. C2 is depth: eight source-grounded statements on interpretation and limits of watchdog `unclosed` pairing counts. Controls at entering tip: {W}/controls.txt. Attack exact predicates; do not broaden them.

Every Report trailer is relative to {L}; write it at {L}/<that path>. Write only your own report under {W}/w1/. No fleet/sibling/lane code changes or commit/jj mutations. Use absolute paths. Detection/report only: never remediate host state or infer provider death from missing reports. No secrets/private URLs.

Scratch: use `$HYAKU_SCRATCH/mori-r57/<seat-name>/`, default `/fast/scratch/hyaku`; mkdir explicitly, set TMPDIR there and clean before yielding; `/tmp` only for files under 50 MB and never cite it. One lightweight archive/worktree per seat; check `{F}/scripts/hyaku/disk-guard.sh status` before heavy work and stop on ENOSPC. Before installing/updating a tool read `/home/vgpnk/.omp/agent/RULES.md`, use official channels and record tool/version/channel/reason. Pacman is paused: do not run pacman.

Frozen contract/counters are immutable after scoring. Do not change predicates, counters, kill rules, claims or targets. Auditors return findings; fixtures must live only under scratch and use explicit `git -C` paths. No seat spawns/additional swarms.'''
(W/'w1-spec.json').write_text(json.dumps({'wave':'mori-r57-w1','reportDir':'.ufo/waves/round-57/w1','context':context,'items':items},indent=2)+'\n')
print(f'wrote {len(items)} distinct items')
