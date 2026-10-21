# Round-18 out-of-metric privacy triage (L1 MoriR18Recovery)

The frozen C1 classes are a recall floor (`frozen/c1-policy.json` `known_limit`). Wave-1 reading
sweeps (`build/Sweep*.md`, `build/Adj*.md` "additional" sections) flagged context the classes
miss. This register records the L1 gate decision per finding family. It is outside the C1
count; it is the repair-first "whole-round sweep" disposition. No private text is reproduced.

## Decision rule (L1)

Privacy finding = an item in the "never" column of `corpus/knowledge/evidence-minimization-r18.md`:
other-session tool output or transcript content, session identities, operator OMP configuration
or routing values, session-record values beyond field names, personal documents, shell history,
privileged configuration, personal identities/emails, host home-config paths with values.
Not a privacy finding by itself: a sibling seat's result reported inside the same round's wave
(lane work), lane-internal jj/git operation ids and revisions, world-readable host log line
numbers and package names, lane seat names, public-source quotes, fleet lane names.

## Dispositions

| Family (sweep tag → files) | Decision | Where |
|---|---|---|
| Routed files PacmanActorTrace, OmpRetryConfig, SessionExitCorrelation | **admit → minimized** (whole-body replacement, provenance blob + SHA-256 retained) | commit b8f5c6c |
| Frozen-class identity tokens in 22 non-routed files (session ids, store paths, tool-log numbers, document paths, config line refs) | **admit → token-redacted** | commit b8f5c6c |
| ConformanceAudit V4/V8/V9/V11 value fragments (session name fragment, reason/kind values, config location, login account, tool-log number) | **admit → redacted** | commit b8f5c6c |
| Session-record values and per-seat retry values: RetryRecoveryShape (V13), SeatNaming, SentinelTranscripts, ReviewSeatBreachDetect, TranscriptShapes, DeadSeatCrossCheck | **admit → minimization pending**; drafting call refused by the process job cap (see `residual-drafting-attempts.json`); carried as named debt if still refused at round end | this file, report |
| Operator/host config values: SentinelJjSandbox (user jj config), JjEnvFacts (home config paths, env values), ReviewJjAuditRouting:67,69, HelperFailureWindows:29,202, OverlapJjSiblings:12 (personal identity/email) | **admit → minimization pending** (same refused call covers the first two; the rest are L1 line edits if time allows) | this file, report |
| SW1 "other-seat tool/report results" inside round-17 build reports (FrontierLinkage, HelperFailureWindows, KnowledgeJjBranch, JjGate, …) | **reject** — lane work of the same round, not private context | rule above |
| SW4/SW5 lane-own timeline: MisrootR16Facts, MisrootSweep, LiveLaneHeadVsBranch, JjGate prior pass | **reject** — the `MoriR16.Lesson` witness is mori's own misrooted disclosure (closure judged it "probe/disclosure facts, not a credential or a transcript dump", spot-check :190-194); dispatch timelines are lane receipts | spot-check :190-194 |
| Package transaction history (PacmanTxnToday, OverlapTsukuroi:25-39, SrcPacmanLog, ReopenPacmanLog) | **reject except joined private context** — world-readable host log facts are tsukuroi handoff evidence; their joined document/session identities were redacted | b8f5c6c |
| Earlier rounds r15/r16 (SweepR15Md2, SweepR16Md2: lane identifiers, privileged-group membership at r16 SiblingScope.md:20) | **carry** — outside the routed round; r16 SiblingScope:20 queued for minimization next round | report |
| Wave-1 sweeps that died (SweepR17Build1, SweepR17Falsify1/3, SweepR16Md1, SweepR15Md1, SweepR1314Md) | **coverage gap** — those chunks had no wave-1 reading; wave 2 re-sweeps the tip | wave 2 |
