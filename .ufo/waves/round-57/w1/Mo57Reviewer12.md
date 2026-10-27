# Mo57Reviewer12 — no-harm and kumitate boundary

## Verdict

**No boundary violation is evidenced in the frozen contract or the round-56 source/tool.** The round-56 driver-liveness vocabulary is explicitly log-derived, read-only, and disclaims health verdicts; kumitate's lifecycle defines settlement separately through operator-supplied `ufo-swarm-results-v1` results and collection. **The eight proposed round-57 claims were not available to inspect at this review point**: `corpus/knowledge/watchdog-unclosed-r57.md` was absent, and the frozen contract says the entry was absent before the wave (`contract.md:7`). Therefore this is not a semantic approval of the eventual claims.

## Evidence and boundary

- Mori's live tool defines `unclosed` as launches without same-`(lane, round, attempt)` completes, “a pairing count, not a failure claim”; it says `in_flight`/`unclosed` are log-shape facts, not health verdicts, and “Read-only” (`tools/mori-driver-liveness.py:24-45, 224-253`). The implementation pairs events per lane and emits the count (`:129-180`). The round-56 knowledge entry further says unclosed launches are not “stuck,” the log is driver-authored rather than authenticated, and the probe never remediates (`corpus/knowledge/driver-liveness-r56.md:20-26, 60-77`).
- Kumitate's lifecycle source says wave settlement is operator-supplied `ufo-swarm-results-v1` input to `collect`, and defines outcomes and dispatch/results identity joins separately (`/home/vgpnk/Projects/shokunin/kumitate-shokunin/corpus/knowledge/swarm-wave-lifecycle.md:37-45, 98-129`). The prior round-56 boundary audit independently found disjoint subjects (lane-round-attempt vs wave member), close semantics, and authority (`.ufo/waves/round-56/w1/Mo56ConnKumitate.md:137-172`).
- The frozen round-57 C2 contract asks for eight quoted/source-grounded claims and the pairing-count distinction (`.ufo/waves/round-57/contract.md:7`). Its counter is not a semantic boundary check: `count-c2.py` checks for eight `| K` lines, quote delimiters, `S548`/registry text, and the literal “pairing count” (`.ufo/waves/round-57/count-c2.py:8-19`). A claim like “`unclosed=3` proves three wave members were not accepted” could satisfy those superficial tests while improperly converting a driver-log count into kumitate settlement semantics. This is a counterexample to the counter's ability to certify the boundary, not evidence that the absent entry actually makes that claim.

## Finding / residual risk

**No demonstrated violation; semantic review remains open for the actual eight rows.** At inspection, the target entry did not exist; no claim-by-claim finding can be grounded. The frozen C2 counter alone cannot close this gap. On eventual review, reject any statement that treats `unclosed` as present-running work, failure, accepted/unaccepted result, or settled/unsettled wave state; retain it as a count of unmatched driver-log launch/close pairs and distinguish it from kumitate's result-based collection. Do not infer provider death from missing reports or take remediation action.

Verification performed: read-only inspection of the frozen contract/counters, driver tool and round-56 knowledge/boundary evidence, and kumitate province/lifecycle sources. No production edits, fixtures, tests, or commits.

Report: .ufo/waves/round-57/w1/Mo57Reviewer12.md