# Mo57Critic23 — FR5 coverage cross-check

## Counterexample and evidence

The round-56 claim that the driver-liveness probe's “new surface” is strict per-event pairing is not cleanly outside prior core: `corpus/lessons/round-56.md:73-75` explicitly says the census silence surface already read launch epochs since round 2 and only the probe's *strict per-event pairing* was new. This is a narrower distinction than “new driver-liveness observability surface.” The code does implement pairing (`tools/mori-driver-liveness.py:54-62`, parser at `:77+`; selftests for pairing and rollover at `:275-296`), but these demonstrate implementation/behavior, not that the measured concept is outside all existing core.

A stronger counterexample to broad novelty: `SKILL.md:15` already defines fleet liveness using watchdog pid, log freshness, and `.ufo/state/*.round` values; `SKILL.md:21` already describes lane silence from watchdog launch epoch plus post-launch authorship. The verifier records this overlap and the softened novelty claim (`corpus/lessons/round-56-verifier-spotcheck.md:21-29,77`). Thus strict pairing may be a genuinely new *granularity/algorithm*, while launch-epoch observability and per-lane liveness are established surfaces. The probe's own docstring says “frontier FR5” (`tools/mori-driver-liveness.py:2`), but that label is not evidence of distinct observability coverage.

## Verdict / axes

No frozen round-57 predicate is contradicted: contract C1 is capability-table completeness for driver-liveness and vote-binding, while C2 concerns interpretation of `unclosed` (`.ufo/waves/round-57/contract.md:5-7`). This is a coverage/novelty qualification, not grounds to broaden C1 or reject its exact row criterion. It bears on coverage claims and calibration of what counts as genuinely new, not on round-57 acceptance counters.

## Smallest safe correction

Describe the novelty precisely as strict per-event launch/terminal pairing and its `unclosed` diagnostic, explicitly distinguishing it from the already-existing launch-epoch/lane-silence core. Do not claim a wholly new liveness dimension absent evidence. Evidence cited above is local source text; no live host health or provider state inferred.
