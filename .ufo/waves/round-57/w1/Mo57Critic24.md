# Mo57Critic24 — interpretation boundary review

## Counterexample and evidence

The safe interpretation is narrower than settlement or execution status. The frozen C2 asks for eight source-located claims about the watchdog `unclosed` field and explicitly requires saying it is a pairing count, not a present-running count (`.ufo/waves/round-57/contract.md:7`). Existing source-backed round-56 note says `unclosed` means launches with no same-round close and describes every field as a log-shape fact, making no health verdict (`corpus/knowledge/driver-liveness-r56.md:19-26,62-68`). The underlying writer extract contains only emitted `launch`, `complete`, `lane-dead-no-report`, `launch-fail`, and `wrap` records (`corpus/evidence/sources-r56/watchdog-log-grammar-v2.txt:1-11`); it does not establish whether a process remains alive or a wave is authoritatively settled.

Strong counterexample to any expanded interpretation: a launch followed by no same-round close can arise because the driver never emitted/recorded a close, the log was rewritten/truncated, or the lane's execution stopped without a terminal event. Thus identical `unclosed` counts are compatible with a currently running process and with no currently running process. The note itself warns events are unauthenticated and rewritten logs rewrite the reading (`driver-liveness-r56.md:66-68`). Likewise `corpus/knowledge/wave-settlement-r20.md:15-18,36-44` distinguishes report-presence observation from accepted result semantics and says the latter belongs to kumitate. Do not reinterpret this driver's pairing field as that authority's settlement token.

## Verdict / axes

No counterexample to the exact frozen C2 predicate: the required distinction is precisely the appropriate bounded claim. A statement that `unclosed` proves a live/running lane, a failed wave, or a settled/unsettled mission would be unsupported and crosses the mori/kumitate boundary. This is a depth/calibration boundary, not a reason to broaden the predicate or claim a score delta.

## Smallest safe correction

Keep each claim at the source's observable level: an unmatched same-round launch in the parsed driver log under the stated grammar. Explicitly say it neither counts current processes nor authenticates execution nor settles a wave; defer mission/result settlement semantics to kumitate. Cite the source-copy quote for each asserted interpretation, and avoid converting absence of a close into provider death or any remediation.
