# Mo58Critic28 — wave-context audit

**Counterexample:** None found in the assigned prompt checks.

**Evidence / bounded method:** Read the frozen `contract.md`, `count-c1.py`, and `count-c2.py`; inspected this seat's prompt in `.ufo/waves/round-58/w1-spec.json` and `.ufo/waves/round-58/w1-dispatch.json`; cross-checked `.ufo/waves/round-58/w1/swarm-registry.json` and report directory.

- The seat prompt begins `/skill:godspeed`; the spec and dispatch each contain exactly one `Mo58Critic28` seat, role `critic`.
- The `Report:` trailer resolves to `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-58/w1/Mo58Critic28.md`; spec, dispatch, and registry all specify `.ufo/waves/round-58/w1` as `reportDir`.
- The wave instructions require an explicit per-seat scratch directory and `TMPDIR`, copying any receipt before cleanup, and cleanup before yielding. I created `/fast/scratch/hyaku/mori-r58/Mo58Critic28` and will remove only that directory.
- The prompt prohibits pacman and unverified remote scripts; it separately prohibits production/corpus-registry/SCORECARD/LOG/lane-VCS edits and fleet/sibling writes, while allowing only this scoped report.
- Registry has 64 unique members; the attack roles total 42/64 (reviewer 22, critic 10, mutation-tester 8, sentinel 2), meeting the contract's ≥25% threshold.
- Freeze revision `fe8801120a67c1a6b8899d7d0423839caa09e7d0` is present and is an ancestor of the entering revision's successor HEAD. The contract and both counter blobs match byte-for-byte between freeze and HEAD. The post-freeze diff adds only dispatch/spec/registry artifacts, not frozen counters or contract.

**Impacted axes:** Prompt/guard fidelity; report-path and seat identity; frozen-artifact integrity. No adverse axis impact identified.

**Smallest safe correction:** None indicated by this bounded audit. No lane/fleet/VCS changes made; unrelated pre-existing worktree changes were left untouched.
