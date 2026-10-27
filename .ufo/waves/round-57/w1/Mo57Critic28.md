# Mo57Critic28 — C2 `unclosed` interpretation review

## Counterexample and evidence

The committed round-56 driver-live report is `.ufo/waves/round-56/w1/Mo56ExecDriverFixtures.md`. Its §2 gives concrete controls: `in-flight` has one launch, zero completes, `in_flight=true`, `unclosed=1` (lines 43, 67-75); the `attempt-rollover` fixture has two launches, one completion, one dead event, but `unclosed=0` (lines 41, 68). In §8 the live snapshot records 124 total unclosed pairings across 23 lanes (lines 358-369), while the same report records a later completion changing kake from `unclosed=13, in_flight=true` to `unclosed=12, in_flight=false` (lines 371-380). These support interpreting the count as unmatched launch records in that log snapshot, not a count of processes currently running.

A strong counterexample to equating the fields is already in the fixture evidence: in `variants`, kama has one launch, one completion, one dead event, `in_flight=true`, and `unclosed=1` (lines 76-78); thus an unmatched launch can coexist with a terminal event and the summary boolean, and cannot be read as a direct current-running census. F1 gives another limitation: 35 `lane-round-failed` prose records are not recognized as closers; 9 unique open-launch keys (29 by multiplicity) coincide with such failure records (lines 405-415). F4 documents asymmetrical attempt pairing and potential latent mixed-writer cases (lines 430-436). Therefore `unclosed` is an algorithmic pairing diagnostic bounded by this parser's recognized grammar and pairing rules, not proof of live work, provider death, or even necessarily absence of a terminal event.

The report's §8 is a point-in-time log snapshot, not a durable present-tense status: it explicitly notes append-only drift and a newly arrived completion changing counts (lines 371-380). Its own §10 leaves judgment about limits to another reviewer (lines 394-401).

## Verdict / axes

C2 asks for source-grounded interpretation and limits, specifically that `unclosed` is a pairing count rather than a present-running count (`.ufo/waves/round-57/contract.md:7`). The committed report provides strong counterexamples and exact pairing mechanics (`tools/mori-driver-liveness.py:109-143`, `:144-150`), but by itself is evidence about algorithm and observed log samples, not proof that any corresponding work is running now. The report's `in_flight` boolean is also a derived summary (`tools/mori-driver-liveness.py:109-112`), not independent host/process observation. No inference about provider death or current execution is warranted from absent reports or this count.

Impacted axis: C2 depth, specifically interpretation limits and source-groundedness. The exact predicate is not disproven; these are necessary qualifications, not a reason to broaden it.

## Smallest safe correction

State: “`unclosed` counts launch entries still unmatched under the probe's recognized event grammar and attempt-pairing rules in the captured log; it is not a present-running count. Unrecognized terminal/failure prose, mixed attempt tags, and snapshot timing can leave the diagnostic unmatched after work has ended or change it later.” Cite the parser and the report's F1/F4 plus append-only example. Do not infer running work or provider death from the count alone.
