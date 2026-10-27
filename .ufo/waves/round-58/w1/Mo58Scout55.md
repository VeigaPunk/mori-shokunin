# Mo58Scout55 — cross-sibling overlap

## Observed

- At Mori freeze `fe8801120a67c1a6b8899d7d0423839caa09e7d0`, `tools/mori-driver-liveness.py` describes a read-only probe that reads `.ufo/watchdog.log` and reports log-shape facts; its frozen grammar includes `launch`, `complete`, `lane-dead-no-report`, `launch-fail`, and `wrap` (path: `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-driver-liveness.py`, docstring and `LINE_RE` / `parse_log`). The event writers are the fleet scripts: `/home/vgpnk/Projects/shokunin/scripts/hyaku/inline.sh:149,176,182` logs launch/complete/dead; `/home/vgpnk/Projects/shokunin/scripts/shokunin-watchdog.sh:241-249,266,398,405` logs launch-fail/launch/wrap/complete.
- Kumitate's current `/home/vgpnk/Projects/shokunin/kumitate-shokunin/PROVINCE.md` says its domain “orchestration & tooling — scopes OMP task/hub, ufo-fsd scripts & runtime,” and its frontier includes “OMP harness contract (task batch, agent hub, agent discovery).” Mori's current `/home/vgpnk/Projects/shokunin/mori-shokunin/PROVINCE.md` says it refuses the “dispatch and orchestration mechanism (→ kumitate).” Kumitate's `corpus/knowledge/worker-heartbeat-liveness.md:28-31` also discusses the dispatcher's pull-based liveness signal and repend, though it is not the same log parser.
- Tsukuroi's current `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md` defines its “driver/firmware plane” as “kernel modules, nvidia driver + GSP firmware presence, `nvidia-smi` shape”; ADJ-05 routes task/hub dispatch and orchestration semantics to kumitate. Searches found historical watchdog-log event examples in tsukuroi evidence, but no `mori-driver-liveness` or parser/event-class ownership declaration there.

## Overlap assessment

- **Kumitate — semantic overlap to report, not transfer:** interpretation of these records as OMP/hyaku launch, completion, retry/dead, launch-failure, or wrap/orchestration lifecycle events touches kumitate's orchestration and ufo-fsd/OMP boundary. Mori's bounded, read-only extraction of log facts remains distinct from owning dispatch correctness or lifecycle decisions. Preserve this split in any depth entry: parser-observed syntax/facts versus orchestration meaning/adjudication.
- **Tsukuroi — no semantic overlap observed:** “driver” is a lexical collision here. Tsukuroi's cited boundary is OS device-driver/firmware state, while this parser concerns the fleet orchestration driver log. Historical log examples in tsukuroi materials are evidence citations, not a claim of parser ownership.

## Gaps / confidence

High confidence on the declared province split from the opened current declarations and frozen Mori parser. No direct ownership statement was found assigning the two fleet writer scripts themselves to kumitate; that narrower attribution remains unresolved. Sibling declarations were read from their live worktrees, not freeze-pinned snapshots.