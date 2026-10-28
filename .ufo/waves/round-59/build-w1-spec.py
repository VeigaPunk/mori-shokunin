#!/usr/bin/env python3
"""Build the one 64-seat round-59 v2 wave spec; no dispatch here."""
import json
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/mori-shokunin')
FLEET = Path('/home/vgpnk/Projects/shokunin')
W = LANE / '.ufo/waves/round-59'
GOD = Path('/home/vgpnk/.agents/skills/godspeed/directive.md').read_text().rstrip('\n')
FREEZE = '60b3a76ad0524c8978cc51922940be1c8c388915'
ENTERING = '2b9f03975bfb6e508f35074ac8181ec8bf54e805'

assignments = [
    ('reviewer', 20), ('critic', 10), ('mutation-tester', 8),
    ('executor', 8), ('scribe', 4), ('scout', 4), ('connector', 2),
    ('sentinel', 2), ('revenger', 4), ('simplifier', 2),
]

reviewer_items = [
    'C1 fixture battery re-verification: materialize each of the 13 committed fixtures-c1 trees at the freeze revision, run the pinned tool over each, and confirm the observed reason prefixes cover its expect.txt; report any fixture that scores met or fails for a different reason.',
    'C1 register-identity attack: construct scorecard fixtures (a third declarer, a declarer embedded inside a non-Capabilities section, a register table split by a `## ` heading, a table whose key cell has padded backticks) and report whether the counter/tool still binds correctly.',
    'C1 pointer attack: try backticked evidence tokens that are syntactically valid but semantically wrong — a `…` ellipsis path, a path with trailing whitespace inside backticks, a pointer to a directory, a duplicate pointer — and report what the counter accepts.',
    'C1 manifest attack: build manifest fixtures where rounds[832].capabilities_added[0] is a non-string, capabilities_added is a dict, lane_round is a string "56", or the two strings swap indexes; report exact reason tokens.',
    'C1 real-arm replay: independently re-derive the real arm — extract SCORECARD.md at freeze, MANIFEST.json at 2807c6ab, run the tool, compare verdict/bound to the committed receipt; report any divergence.',
    'C1 do-nothing re-derivation: run the frozen counter at the entering revision and enumerate the cheapest work-skipping states that could reach met; report whether any exist.',
    'C2 claim-grammar attack: feed eval_entry-shaped entries with claims that dodge the regex (leading whitespace, `**K01**` vs `K1`, two claims on one line, a claim with an empty quote, a pin that is uppercase hex) and report what parses.',
    'C2 quote-span attack: construct an entry whose quotes are byte-exact but against the WRONG file (same text in two artifacts), a quote spanning a \\n boundary via offset, and a quote containing a backtick; report verdicts.',
    'C2 rows-binding attack: SOURCES rows with 3-space indent, a used-by cell listing the entry plus another path, a mined row whose used-by is the entry but whose anchor cell is empty; report verdicts.',
    'C2 scan-arm attack: results.json fixtures — seats non-int, results tuple-in-list, name non-str, output empty string vs null, note non-null, duplicate name across files; run the pinned tool and report verdicts.',
    'C2 real-scan replay: independently run the pinned tool over the five committed r54-r58 results files and the r53 drift file; confirm OK/exit 0 and FAIL/exit 1 with exact output.',
    'Settlement artifact survey verification: pick 6 committed *-results.json files across rounds 50-58 and verify the entry-plausible claims (top-level keys, member key set, note null, output nonempty) hold; report any counterexample.',
    'C1+C2 counter cross-check: verify the frozen target output tokens in contract.md are exactly the tokens count-c1.py and count-c2.py emit (run both at freeze; diff token sets); report any token not emitted.',
    'Frozen-byte integrity: sha256 the frozen contract, both counters, both tools at the freeze revision and at the working tree; report equality or divergence.',
    'Scratch/TMPDIR audit: verify no committed counter or tool writes outside TMPDIR/--scratch (grep for /tmp, mkdtemp, tempfile) and that --scratch is accepted; report violations.',
    'Fixture-coverage gap analysis: enumerate constructions NOT covered by the 13 C1 fixtures and 12 C2 trees that could still false-green; report the three most dangerous gaps.',
    'C2 ARTIFACTS binding: verify each pinned copy name maps to a real committed .ufo artifact and sha256-equality holds at the freeze revision for files that exist (the .ufo side) — report mismatches.',
    'Kill-rule audit: list every byte the freeze pins (counter, contract, tool shas, fixtures, expect files) and check nothing outside is required for met; report under- or over-pinning.',
    'No-harm review: inspect contract, counters, tools, and fixtures for axis harm — anything that weakens an existing gate, deletes evidence, or absorbs sibling scope; report findings.',
    'Frontier coverage check: does the C2 entry topic (wave settlement artifacts) sit inside mori PROVINCE (fleet liveness, wave settlement)? Cite the PROVINCE lines; flag any adjacent-domain bleed.',
]

critic_items = [
    'Falsify C1: construct the cheapest full-met path that skips real verification (a fabricated bound map, a fixture-dir with a passing scorecard only, a tool renamed); report whether the counter catches it.',
    'Falsify C2: construct the cheapest entry that scores met without real claims (quotes repeated trivially across 3 files, claims that are tautologies of the JSON shape); report.',
    'Attack the claim grammar itself: is `line:` vs `offset:` ambiguous for a one-line file? Can a K claim cite a line that is whitespace-only? Report.',
    'Attack MANIFEST_REV pinning: find what a post-pin MANIFEST change would do to the counter (stale pin vs live file) and report the risk class.',
    'Attack the drift arm: does exit-1-on-r53 prove discrimination or just extra-key intolerance? Propose a stricter drift fixture and report.',
    'Attack the do-nothing adequacy: is there a committed state between entering and freeze that scores met with less work than claimed? Report.',
    'Counter-honesty: audit count-c1.py and count-c2.py for self-graded arms (REF-function equivalence where the counter and tool share an author); report which arms lack independent proof.',
    'Report-contract pre-check: verify the round-59 report can cite every receipt this wave must produce; list any evidence the frozen claims need that no arm writes.',
    'Probe counter robustness under hostile file content: a scorecard with CRLF, a manifest with NaN, an entry with BOM; report behavior.',
    'Question the C2 scope: are r54-r58 results files the right artifact set? Check earlier rounds for differently shaped results files that should be in DRIFT/REAL sets; report.',
]

mutation_items = [
    'Mutate count-c1.py: remove the pointer arm, relax binding to first-## Capabilities, drop MANIFEST_REV pin — then run against a constructed state; report which mutations escape detection by the fixture battery.',
    'Mutate count-c2.py: remove the grammar arm, accept len(cells)>=11, drop the pin check; construct entries that now false-green; report.',
    'Mutate mori-register-check.py selftest fixtures: a fixture whose expect prefix is `binding` but the failure is `keys` — does the counter notice prefix-vs-reason mismatch? Report.',
    'Mutation-test the entry grammar regex: report constructs it accepts that should not parse (e.g., `—` vs `-`, quote containing `; pin `).',
    'Mutation-test the settlement scanner: fields that silently pass (output as non-str truthy, seats bool True, round float 59.0); report each verdict.',
    'Mutate a fixture expect file semantics: if an expect lists two prefixes and only one reason fires, does the counter still pass it? Demonstrate.',
    'Boundary mutation: a claim line that parses but whose file is a symlink or empty; a SOURCES row where used-by is `corpus/knowledge/wave-settlement-artifacts-r59.md,` with trailing comma; report.',
    'Counter selftest honesty: do the counter selftests exercise the same code path as the measure path? Mutate a pure-function and report whether selftest or measure catches it.',
]

executor_items = [
    'Run both frozen counters at the entering revision 2b9f0397 and at freeze 60b3a76a with --scratch under your seat dir; paste full outputs and exit codes.',
    'Run both tool selftests (REGCHECK_SELFTEST, SETSCAN_SELFTEST) with --scratch under your seat dir; paste outputs and rc.',
    'Enumerate the fixture battery: for each fixtures-c1 dir, run the tool and print verdict+reasons; paste a table.',
    'Enumerate trees-c2: extract each tree at freeze to scratch, run eval_entry-equivalent (count-c2.py internal — import it), print verdict+reasons per tree.',
    'Scan every committed .ufo/waves/*/w*-results.json file in the lane with the pinned tool; list which pass, which fail, and the failure classes.',
    'Compute sha256 of every committed *-results.json and *-settlement*.json under .ufo/waves/ rounds 50-58; paste the list for entry pin candidates.',
    'Survey results.json anomalies: for every committed results file, report members vs seats, empty outputs, non-null notes, and member key-sets; paste a compact table.',
    'Re-derive the SOURCES census manually (row count, tier and status histograms, malformed count) from committed corpus/SOURCES.md and compare to the census validator output; paste both.',
]

scribe_items = [
    'Draft the C2 depth entry skeleton: corpus/knowledge/wave-settlement-artifacts-r59.md in the frozen claim grammar — propose 10-14 candidate claims with file/span/pin triples computed from the committed artifacts (sha256 + byte offsets); return the draft as your report (do NOT write it into corpus).',
    'Draft the round-59 lesson skeleton: Gate block for the six artifact S-rows (S553-S558) with <=25-word located quotes per row, plus a reject candidate you verify; return the draft.',
    'Draft the SCORECARD round-59 section skeleton: claim table rows for C1/C2 with the frozen counting commands and receipt names; return the draft.',
    'Draft the LOG.md round-59 entry skeleton: what was claimed, frozen, controlled, waved; return the draft.',
]

scout_items = [
    'Recon the mori absent-defect-register slice: re-derive it per contract.md (the awk command) and hand-check each row (S244/S262/S268 and any new) — source reachable? located quote? verdict per row.',
    'Survey sibling lanes for wave-settlement knowledge overlap: do kumitate (swarm-wave lifecycle), tsukuroi, or kaidoku already hold claims about *-results.json shape or seat settlement? Report overlap only.',
    'Open considerthese/2026-10-26.md (and any newer file); list which suggestions remain unimplemented and nominate at most one for this round; verify suggestion status against lane tools.',
    'Survey all committed *-results.json and *settlement*.json under .ufo/waves/: enumerate distinct top-level key sets and member key sets across rounds; report a shape census table.',
]

connector_items = [
    'Sibling-overlap walk (bounded planning data-walk): map what kumitate owns about wave settlement (ufo-swarm-results-v1 input, collect step) vs what this round claims for mori (artifact shape facts); report the boundary and any contested scope.',
    'Connector pattern scan: compare how other lanes (kama, kotoba, chousa — check one each) structure their depth-entry claim grammar and frozen counters; report patterns mori should or should not adopt.',
]

sentinel_items = [
    'Boundary audit: verify every counter/tool/seat action stays read-only on lane git, never writes outside scratch/wave dirs, never reads session/secret material; flag any violation.',
    'Security review of the new tools: path handling in --root, eval of entry text, subprocess invocation surfaces; report anything reachable by hostile committed content.',
]

revenger_items = [
    'Reverse-engineer the .ready handoff: read committed w1.ready / w1.ready.dispatched / w1-dispatch.json across rounds 56-58 and derive the lifecycle (who writes each, when results.json appears); report the documented-vs-observed differences.',
    'Derive the results.json writer contract from evidence: compare dispatch taskCall tasks[] names to results[] names across 5 rounds; report the settlement semantics actually observable.',
    'Investigate report_file extra keys: which rounds carry them, when the field appeared/disappeared, and what that says about writer versions; report with evidence.',
    'Investigate dead-seat evidence: find a committed results.json member whose report file is missing (e.g., r55 Mo55Rc14) and document how the artifact records partial settlement.',
]

simplifier_items = [
    'Review tools/mori-register-check.py and tools/mori-settlement-scan.py for dead code, redundant checks, and unclear failure text; report simplifications (no edits).',
    'Review fixtures-c1/trees-c2 for duplicated coverage and missing obvious cases (e.g., an empty evidence cell vs absent evidence column); report.',
]

buckets = {
    'reviewer': reviewer_items, 'critic': critic_items,
    'mutation-tester': mutation_items, 'executor': executor_items,
    'scribe': scribe_items, 'scout': scout_items, 'connector': connector_items,
    'sentinel': sentinel_items, 'revenger': revenger_items,
    'simplifier': simplifier_items,
}

items = []
idx = 0
for role, count in assignments:
    pool = buckets[role]
    for j in range(count):
        idx += 1
        name = 'Mo59%s%02d' % (role.title().replace('-', ''), idx)
        check = pool[j % len(pool)]
        if role == 'executor':
            check += ' Executor item: run frozen counters/tools/scratch fixtures only; do not edit production files, commit, or mutate lane VCS.'
        if role == 'scribe':
            check += ' Return drafts in your report file only; do not edit corpus, registry, SCORECARD or LOG.'
        if role in ('reviewer', 'critic', 'mutation-tester', 'sentinel', 'revenger', 'simplifier'):
            check += ' Return an adversarial finding or an explicit no-counterexample result with bounded method; no production edits.'
        if role == 'scout':
            check += ' Read-only reconnaissance; cite opened paths and located quotes.'
        if role == 'connector':
            check += ' Connector duty: report overlap/refusal boundaries and patterns; no edits.'
        prompt = ('/skill:godspeed\n' + GOD + '\n\n' +
                  f'{name}: {check} Read {W}/contract.md and the frozen counters '
                  f'{W}/count-c1.py and {W}/count-c2.py first (freeze revision {FREEZE}, '
                  f'entering {ENTERING}). Work read-only; return concise findings with exact '
                  'evidence (commands, outputs, line pointers). No commits, no VCS mutation, '
                  'no fleet/sibling writes.')
        items.append({'name': name, 'role': role, 'prompt': prompt})

context = f'''# mori round 59 — one v2 build/falsify wave (64 seats)
Lane repo: {LANE}. Fleet root: {FLEET}. L1: MoriR59a2. Frozen contract: {W}/contract.md. Frozen counters: {W}/count-c1.py and {W}/count-c2.py. Freeze revision: {FREEZE} (amended freeze: initial freeze ccfd554e plus pre-data counter fix); entering revision: {ENTERING}. Claims: C1 calibration (tools/mori-register-check.py — active-register binding, 13 hostile fixtures, MANIFEST_REV-pinned binding); C2 depth (tools/mori-settlement-scan.py + corpus/knowledge/wave-settlement-artifacts-r59.md — >=10 byte-exact pin-bound claims over >=3 committed settlement artifacts, mined S-rows, 12 hostile trees). One wave, policy v2, 64 seats. L1 holds the canonical planner seat; connector items carry bounded sibling-overlap/planning walks because `planner` is not a validator role. Attack share is reviewer+critic+mutation-tester+sentinel = 40/64.

Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Write only your own report under {W}/w1/. Do not edit production files, corpus registry, SCORECARD, LOG, or lane VCS; return findings/drafts only. Do not write to fleet or sibling repos. Use absolute paths for every file access.

Scratch root for this round is `$HYAKU_SCRATCH/mori-r59/<seat-name>/` (default `/fast/scratch/hyaku`): create it explicitly with mkdir -p, set TMPDIR there, pass --scratch to the counters, clean it before yielding, and copy any small receipt into your report first. `/tmp` only for files under 50 MB, never as evidence. One lightweight clone/worktree per seat only if needed; prefer `git show`/read-only reads (a lane gate or selftest that runs git writes must run on a sandbox clone under your scratch dir, never in the lane). Check `{FLEET}/scripts/hyaku/disk-guard.sh status` before heavy work; on ENOSPC report free space and do not rerun until status is green.

Before installing/updating a tool, read `/home/vgpnk/.omp/agent/RULES.md`; use official channels and record tool/version/channel/reason. Pacman transactions are paused host-wide: do not run pacman. Never pipe unverified remote scripts into a shell. Never expose secrets, session material or private URLs. Detection/report only; no remediation or provider-death inference. No seat spawns or additional swarms. Frozen claims, counters, predicates and kill rules are immutable after scoring. Any fixture repo must be initialized at an explicit scratch path (`D=$(mktemp -d -p $HYAKU_SCRATCH/mori-r59/<seat-name>) && git -C "$D" init -q`) and every git command must use `git -C <that path>`; never commit outside that throwaway repo. Never `agent://all`; you report only through your report file.'''

spec = {'wave': 'mori-r59-w1', 'reportDir': '.ufo/waves/round-59/w1',
        'context': context, 'items': items}
(W / 'w1-spec.json').write_text(json.dumps(spec, indent=2) + '\n')
print('wrote %d distinct items; roles=%s'
      % (len(items), ','.join('%s:%d' % (r, n) for r, n in assignments)))
