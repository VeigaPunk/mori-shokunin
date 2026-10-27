# Mo58Reviewer01 — C1 active-register identity

**Result: no counterexample in the assigned stub-first fixture.** The frozen counter selected the active register when the superseded `## Capabilities` stub preceded it.

## Evidence

- Freeze revision `fe8801120a67c1a6b8899d7d0423839caa09e7d0` exists. Counter bytes at that revision and the lane working-tree counter have identical SHA-256 `6ecdb627bb55522c258dc484ed5c530cfd6f7c57c6a89b4c38179df4c0f84e4b`.
- In `count-c1.py`, `_find_register` visits exact stripped `## Capabilities` headings in file order, extracts each section through the next `## ` heading, and accepts the first whose first 12 body lines contain `BIND_SENT = "the lane's current capabilities register"`, whose body lacks `STUB_MARK = "-- none yet --"`, and whose body contains `| key | capability |`. `measure` then requires at least 10 `rounds[...]` key rows.
- Production `SCORECARD.md` has the superseded exact heading at line 596 and active round-35 exact heading at line 1951. The identity sentence is at line 1953. The active section contains 20 keyed rows. The first stub uses the em-dash text `— none yet —` (line 600), not the counter's ASCII `-- none yet --` marker.
- Bounded throwaway-git fixture, using an unchanged copy of the frozen counter and fixture manifest/pointer files: production-shaped em-dash stub first + active section yielded `C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none` (exit 0). ASCII-marker stub first + active yielded the same. Stub-only control yielded `C1=unmet rows=0 ... binding=bad` (exit 1).
- Frozen counter selftest: `C1_SELFTEST pass=4 fail=0`. Read-only measurement at lane tip `4272736cfc5147586e1543413772f80daf44b04b`: `C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none` (exit 0).

## Residual risk / scope

The marker check is ASCII-specific and therefore does not match the actual em-dash stub; the tested stub is nevertheless rejected because its section lacks the identity sentence and register header. Selection is first-match among sections satisfying those text predicates, not a structural round-35 identifier: a preceding forged section with the identity sentence/header and sufficient rows could win. This fixture did not test forged competing registers; no false binding to the superseded stub was observed.
