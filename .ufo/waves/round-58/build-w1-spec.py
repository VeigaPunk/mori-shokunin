#!/usr/bin/env python3
"""Build the one 64-seat round-58 v2 wave spec; no dispatch here."""
import json
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/mori-shokunin')
FLEET = Path('/home/vgpnk/Projects/shokunin')
W = LANE / '.ufo/waves/round-58'
GOD = Path('/home/vgpnk/.agents/skills/godspeed/directive.md').read_text().rstrip('\n')
FREEZE = 'fe8801120a67c1a6b8899d7d0423839caa09e7d0'

assignments = [
    ('reviewer', 22), ('critic', 10), ('mutation-tester', 8),
    ('executor', 8), ('scribe', 6), ('scout', 4), ('connector', 2),
    ('sentinel', 2), ('revenger', 1), ('simplifier', 1),
]
checks = [
    'C1 active-register identity: independently trace how the frozen counter identifies the round-35 current register; attempt a fixture with the superseded first stub plus the active register and report any counterexample.',
    'C1 pointer resolution: attack the frozen git cat-file -e evidence-path checks with malformed, missing, absolute, and wrong-tree paths; report exact fixture and observed verdict.',
    'C1 MANIFEST binding: compare the two round-56 capability rows to MANIFEST rounds[832].capabilities_added[0..1]; test whether altered names or keys can still pass.',
    'C1 do-nothing: run the frozen counter at the entering revision and identify the cheapest no-work state that could meet its target; exact command, output, exit.',
    'C2 quote binding: attack count-c2.py with fabricated backticks, a valid locator on the wrong line, short substrings, duplicate K numbers, and stale copy bytes; use only a scratch fixture.',
    'C2 registry binding: attack the S550 row parser with duplicate IDs, wrong status, dangling used-by, malformed column counts, and a lookalike ID; exact scratch receipt.',
    'C2 claim scope: compare the proposed driver event-class entry with round-57 watchdog-unclosed-r57.md; identify duplicated claims or overreach with line evidence.',
    'C2 source grounding: reopen tools/mori-driver-liveness.py at the frozen revision and assess whether each proposed event-class statement is actually supported by its cited line.',
    'Frontier: rederive the mori absent-defect-register slice (S244/S262/S268); hand-check source reachability and located quote where possible, distinguishing absent from unreachable.',
    'Census: independently derive the round-start registry count and manual tier/status histograms from committed corpus/SOURCES.md; report commands and outputs.',
    'considerthese: check 2026-10-26 suggestion 1 status against tools/mori-pin-check.py and identify one still-unimplemented suggestion suitable for this round; do not edit operator input.',
    'Cross-claim no-harm: inspect contract, counters, and round-56/57 records for falsifier, axis overlap, frozen-rule drift, or detection/report boundary bleed.',
    'Cross-sibling overlap: inspect kumitate and tsukuroi province boundaries for the proposed driver parser semantics; report overlap only, never absorb sibling ownership.',
    'Wave-context audit: check the prompt for GODSPEED prefix, correct absolute report path, scratch cleanup, pacman guard, and no lane/fleet mutation permission.',
]
items = []
idx = 0
for role, count in assignments:
    for _ in range(count):
        idx += 1
        name = f'Mo58{role.title().replace("-", "")}{idx:02d}'
        check = checks[(idx - 1) % len(checks)]
        if role == 'executor':
            check += ' This is an executor item: run only the frozen counter/selftest or a bounded scratch fixture; do not edit production files, commit, or mutate lane VCS.'
        if role == 'scribe':
            check += ' Return a draft or review note only; do not edit corpus or registry files.'
        if role in ('reviewer', 'critic', 'mutation-tester', 'sentinel', 'revenger', 'simplifier'):
            check += ' Return an adversarial finding or explicit no-counterexample result with bounded method; no production edits.'
        if role == 'scout':
            check += ' Read-only reconnaissance; cite the opened URL/path and located quote if accessible.'
        if role == 'connector':
            check += ' Connector duty: compare sibling lane surfaces and report overlap/refusal boundaries.'
        prompt = ('/skill:godspeed\n' + GOD + '\n\n' +
                  f'{name}: {check} Read {W}/contract.md and the frozen counter files first. '
                  f'Use the freeze revision {FREEZE}. Return concise findings with exact evidence; '
                  f'no commits, no VCS mutation, no fleet/sibling writes.')
        items.append({'name': name, 'role': role, 'prompt': prompt})

context = f'''# mori round 58 — one v2 build/falsify wave (64 seats)
Lane repo: {LANE}. Fleet root: {FLEET}. L1: MoriR58. Frozen contract: {W}/contract.md. Frozen counters: {W}/count-c1.py and {W}/count-c2.py. Freeze revision: {FREEZE}; entering revision: b783d0b892637ce8d20f188cad20e4d8913ca635. Claims: C1 calibration (active capability-register counter identity and pointer resolution); C2 depth (quote-bound source entry on driver-liveness event classes). One wave, policy v2, 64 seats. L1 holds the canonical planner seat; connector items carry bounded sibling-overlap/planning walks because `planner` is not a validator role. Attack share is reviewer+critic+mutation-tester+sentinel.

Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Write only your own report under {W}/w1/. Do not edit production files, corpus registry, SCORECARD, LOG, or lane VCS; return findings/drafts only. Do not write to fleet or sibling repos. Use absolute paths.

Scratch root for this round is `$HYAKU_SCRATCH/mori-r58/<seat-name>/` (default `/fast/scratch/hyaku`): create it explicitly, set TMPDIR there, clean it before yielding, and copy any small receipt into your report directory first. `/tmp` only for files under 50 MB, never as evidence. One lightweight clone/worktree per seat only if needed; prefer `git show`/read-only reads. Check `{FLEET}/scripts/hyaku/disk-guard.sh status` before heavy work; on ENOSPC report free space and do not rerun until status is green.

Before installing/updating a tool, read `/home/vgpnk/.omp/agent/RULES.md`; use official channels and record tool/version/channel/reason. Pacman transactions are paused host-wide: do not run pacman. No pacman, no unverified remote scripts. Never expose secrets, session material or private URLs. Detection/report only; no remediation or provider-death inference. No seat spawns or additional swarms. Frozen claims, counters, predicates and kill rules are immutable after scoring. Any fixture repo must be initialized at an explicit scratch path and every git command must use `git -C <that path>`; never commit outside that throwaway repo. Every report is lane-local under the absolute path above.'''

spec = {'wave': 'mori-r58-w1', 'reportDir': '.ufo/waves/round-58/w1', 'context': context, 'items': items}
(W / 'w1-spec.json').write_text(json.dumps(spec, indent=2) + '\n')
print(f'wrote {len(items)} distinct items; roles=' + ','.join(f'{r}:{n}' for r,n in assignments))
