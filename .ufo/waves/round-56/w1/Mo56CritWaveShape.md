# Mo56CritWaveShape — wave-shape conformance check for mori round 56 w1

Seat role: critic (wave-shape). Scope: verify w1-spec.json conforms to the round
contract and the wave-shape rules from the seat spec. No fleet or lane state was
modified; all reads are read-only. No subagents dispatched (leaf seat).

Checked file: /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-56/w1-spec.json
(python3 json.load -> OK, 81670 bytes; committed at acc62f54 "round-56: validate
w1 dispatch (64 seats, policy v2)" on top of 7eab9188 "round-56: w1 spec 64
seats (add wave-shape critic)"; `git status --porcelain` on the spec shows
nothing — tracked and clean).

## Evidence (commands + output)

Command: python3 structural summary of the spec
- top keys: wave='mori-r56-w1', reportDir='.ufo/waves/round-56/w1', context (str), items (list)
- items: 64; every item schema is exactly {name, role, prompt} — no model/agent key on any item
- output excerpt: `n_items= 64`, `item keys sample: {"name","role","prompt"}`

Command: role census over items
- output: roles: {'scout': 4, 'executor': 20, 'scribe': 7, 'reviewer': 9,
  'critic': 10, 'mutation-tester': 6, 'connector': 2, 'sentinel': 4,
  'revenger': 1, 'simplifier': 1}
- attack seats = reviewer 9 + critic 10 + mutation-tester 6 + labrat 0 +
  security-reviewer 0 = 25 of 64 = 39.1% (>= 25% and >= 16 absolute)
- planner seats: none (contract: "The planner seat is held by the L1 (the
  validator does not permit a planner role)")
- connector seats present: Mo56ConnKumitate, Mo56ConnSources (2)
- all 64 names unique, all prefixed Mo56; no unknown role values

Command: context sentence checks (substring match against spec context)
- 'install or upgrade tools that help the task' -> True (tooling authorization,
  operator 2026-10-19, with RULES.md reference and record-keeping clause)
- 'ALL pacman transactions are PAUSED host-wide' -> True and
  'never run pacman' -> True (pacman guard, orchestrator ruling 2026-10-20)
- 'Report:` trailer path is relative to' -> True and
  'write it at /home/vgpnk/Projects/shokunin/mori-shokunin/<that path>' -> True
  (Report-trailer resolution sentence present verbatim)
- 'NO vote items' -> True (vote-line protocol for this wave)

Command: model-alias scan over the whole spec blob (kimi, claude, gpt, sonnet,
opus, haiku, llama, qwen, deepseek, gemini, mistral, o3, o4, grok, phi)
- no model alias anywhere in any prompt or field; the only 'phi' hits are
  inside the word "philosophical" in the shared godspeed directive text
- every prompt leads with /skill:godspeed (checked: True)

Command: absolute-path census over all 64 prompts (regex on /home, /fast, /tmp,
/var, /proc, /sys anchors; 116 distinct absolute paths)
- every Report trailer: exactly one `Report:` line per item, each naming
  `.ufo/waves/round-56/w1/<item name>.md` (checker printed no BAD lines for
  all 64 items)
- every write target (scratch) is /fast/scratch/hyaku/mori-r56/<seat>/ —
  exactly the operator scratch directive path
- non-lane-repo paths cited are read-only and explicitly authorized:
  - /fast/scratch/hyaku/mori-r56/<seat>/ — mandated scratch (context rule)
  - /home/vgpnk/Projects/shokuknow — context: "read-only: read bytes, run
    nothing there" (Mo56ExecQuarantine, Mo56ExecAssimSlice, Mo56CritAssim)
  - /home/vgpnk/Projects/shokunin/.ufo/watchdog.log — the contract's own C1
    surface ("the hyaku driver's .ufo/watchdog log ... as a second
    fleet-liveness source"); lane rule allows reading the fleet log
    (Mo56ScoutLogGrammar, Mo56LabProbe)
  - /home/vgpnk/Projects/shokunin/.ufo/state/, shokunin.conf,
    scripts/hyaku/inline.sh, scripts/shokunin-watchdog.sh,
    scripts/sources-census.sh, AXES.md, CORPUS.md,
    kumitate-shokunin/PROVINCE.md — host/fleet observability reads
    (detection and report only; context forbids mutation of the fleet repo
    and sibling lanes, not reads; connector role exists precisely for
    cross-lane reads)
  - '/home/vgpnk' and '/tmp' appear in Mo56ExecPortability / Mo56SentPorts
    only as grep audit patterns over the round-56 diff (portability sweep for
    hardcoded paths), not as write targets
- no item instructs writing outside the lane repo, the scratch root, or /tmp
  under the 50 MB rule

Route table: the spec hardcodes no model alias and carries no model field, so
routing is entirely host-side. The host route table itself is operator-side
(harness session routing), consistent with the standing rule "Never hardcode
model aliases in the lane repo; the route table, not this prompt, decides
which model serves which role" (.ufo/prompts/*). I did not need its contents
to confirm the spec violates nothing; UNVERIFIED for the table's contents
itself (operator-side, out of lane scope).

## Conformance verdicts (one per seat-spec check)

| Check | Result |
|---|---|
| Seat count in policy v2 band 64-128 | PASS (64) |
| Attack-role share >= 25% | PASS (25/64 = 39.1%; also >= 16 absolute, matching contract "attack seats >= 16 (25%)") |
| Every role routed per host route table, no model alias hardcoded | PASS (roles only; zero alias strings; table is host-side) |
| Connector seat present | PASS (Mo56ConnKumitate, Mo56ConnSources) |
| No planner role | PASS (none; L1 holds the planner seat per contract) |
| Every item names absolute paths under the lane repo (for its write/report targets) | PASS (all 64 Report trailers resolve to .ufo/waves/round-56/w1/<name>.md; all writes go to scratch; non-lane paths are authorized read-only fleet observability surfaces or audit patterns) |
| Context carries tooling authorization + pacman guard sentences | PASS (both verbatim) |
| Report-trailer resolution sentence present | PASS (verbatim in context; per-item trailers conform) |

No violations found. The wave spec matches the contract's wave shape ("One v2
wave w1 (64 seats) carries build and falsification; attack seats >= 16 (25%)")
and the committed validator receipt acc62f54 ("validate w1 dispatch (64 seats,
policy v2)") agrees with the on-disk bytes I checked.

## Findings

- LOW — w1-spec.json items cite fleet-root read paths outside the lane repo
  (/home/vgpnk/Projects/shokunin/.ufo/watchdog.log, .ufo/state/, scripts/*,
  shokunin.conf, AXES.md, CORPUS.md, kumitate-shokunin/PROVINCE.md). Not a
  violation: these are read-only detection surfaces the lane exists to observe,
  and the context explicitly authorizes reading the fleet log and forbids only
  mutation. Listed so the binder knows the citations were reviewed.
- LOW — /home/vgpnk and /tmp strings in Mo56ExecPortability and Mo56SentPorts
  prompts (grep audit patterns for the portability sweep). Not write targets;
  no action needed.
- INFO — the host route table's contents are operator-side and were not
  inspected (UNVERIFIED by design); the spec side of the routing rule is clean.

No HIGH or MED findings. Wave shape conforms; expect none was the correct
expectation.
