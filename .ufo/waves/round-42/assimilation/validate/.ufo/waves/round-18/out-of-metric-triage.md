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
| Session-record values and per-seat retry values: RetryRecoveryShape (V13) | **admit → redacted by the L1** (value histogram and epoch range withheld; key shape kept) | this round |
| SeatNaming, SentinelTranscripts, ReviewSeatBreachDetect, TranscriptShapes, DeadSeatCrossCheck (sweep-flagged "session corpus/record" lines) | **reject after L1 reading** — filename census counts, record-type names, key names, and provider/model and errorMessage class tokens are the round-17 contract's allowlisted fields and aggregates (the closure accepted the same projection in `seat-live-final.json`, spot-check :333-336); identity tokens in them were already redacted | L1 reading, this round |
| Operator user git/jj configuration settings: SentinelJjSandbox:31-32 (V12) | **admit → redacted by the L1** | this round |
| Host env paths (JjEnvFacts HOME/XDG paths), lane jj repo-config settings (ReviewJjAuditRouting:67,69), lane identity (HelperFailureWindows:29,202) | **reject** — the home path is already in every lane path; lane jj settings and lane identity are lane state, not operator-private | rule above |
| Operator personal name/email: OverlapJjSiblings:12, CensusConsumers:186, knowledge silence-grading-r2.md:146 | **admit → redacted by the L1** | commit e2bfbd6 |
| Residual minimization drafting call (8 scribes) | **superseded** — refused 7 times by the process job cap; the L1 performed the admitted redactions itself; the refused-only ledger stays as C3 evidence | `residual-drafting-attempts.json` |
| SW1 "other-seat tool/report results" inside round-17 build reports (FrontierLinkage, HelperFailureWindows, KnowledgeJjBranch, JjGate, …) | **reject** — lane work of the same round, not private context | rule above |
| SW4/SW5 lane-own timeline: MisrootR16Facts, MisrootSweep, LiveLaneHeadVsBranch, JjGate prior pass | **reject** — the `MoriR16.Lesson` witness is mori's own misrooted disclosure (closure judged it "probe/disclosure facts, not a credential or a transcript dump", spot-check :190-194); dispatch timelines are lane receipts | spot-check :190-194 |
| Package transaction history (PacmanTxnToday, OverlapTsukuroi:25-39, SrcPacmanLog, ReopenPacmanLog) | **reject except joined private context** — world-readable host log facts are tsukuroi handoff evidence; their joined document/session identities were redacted | b8f5c6c |
| Earlier rounds r15/r16 (SweepR15Md2, SweepR16Md2: lane identifiers, privileged-group membership at r16 SiblingScope.md:20) | **carry** — outside the routed round; r16 SiblingScope:20 queued for minimization next round | report |
| Wave-1 sweeps that died (SweepR17Build1, SweepR17Falsify1/3, SweepR16Md1, SweepR15Md1, SweepR1314Md) | **coverage gap** — those chunks had no wave-1 reading; wave 2 re-sweeps the tip | wave 2 |

## Wave-2 falsification dispositions (appended)

| Finding (falsify report) | Decision | Where |
|---|---|---|
| OmpRetryConfig: integration truncated at an inner code fence; config-state and transcript aggregates remained (AttackMinOmpRetryConfig, ConformanceAuditR18) | **admit → second-pass minimization**: §1 config summary and §5 store aggregates removed, §3–§8 restored | this round |
| PacmanActorTrace: shell-record search result and privileged logging state (AttackMinPacmanActorTrace, ConformanceAuditR18) | **admit → removed** | this round |
| SessionExitCorrelation: exact snapshot times (AttackMinSessionExit) | **admit → withheld** | this round |
| Round-18 Redact* reports carried full replacement drafts | **admit → draft bodies removed**, pointer kept | this round |
| PacmanTxnToday:119-120 joined account and home-directory split (AttackTokPackageRefs, CriticTriageRule) | **admit → withheld** | this round |
| DeadSeatCrossCheck: session-dir time fragment; broken shell example (AttackTokDeadSeatCrossCheck) | **admit → withheld and repaired** | this round |
| ConformanceAudit:38 lane-resident session copy snapshot name; OmpRetryDocs:240 example session identity | **admit → withheld** | this round |
| seat-live.json: round-18 token edit broke the outer JSON (AttackTokSeatLive) | **admit → regenerated** from the d005cdd blob by JSON-aware redaction; inner stdout re-serialized compactly | this round |
| SentinelJjSandbox:31-32 user git/jj configuration (V12); SeatNaming store-minted cache stem; silence-grading-r2 personal name variants (AttackTokIdentityEdits) | **admit → withheld** | this round |
| r16 SiblingScope:20 group membership | **admit → withheld** | this round |
| Role→alias route handles in round-2 admission and LOG/SCORECARD (AttackTokRound2Json, ResweepCorpusRoot) | **reject** — role→alias routing is published in the committed fleet round prompts; provider/model chains from the operator config are the private part and are not present | `.ufo/prompts/mori-round-18.md` (fleet) |
| r17 wave1 spec/dispatch prompt asking a seat to read config keys (AttackTokR17Wave1Spec) | **reject** — an instruction naming a surface, no values (rule a); the conduct it caused is V9 | spot-check :313 |
| Off-lane home paths (ResweepR13–R16: `~/.local/bin`, `~/.cache/...`), group membership in r13 journal-permission reasoning, operator's public GitHub handle/wiki link | **reject** — tool locations and journal-access permissions are domain facts; the account name is in every lane path; the GitHub handle is the public remote | rule above |
| Session-derived aggregates (provider/model counts, errorMessage class tokens, record-type names, per-lane classification counts) (AttackTokTranscriptShapes, AttackTokSeatBreachDetect, AttackTokRetryRecoveryShape) | **reject** — round-17 contract allowlisted fields and aggregates; the closure accepted the same projection | spot-check :333-336 |
| Line-digest guessability (SentinelHashRisk, medium) | **carry** — stated as a limit in the knowledge note and QUALITY 51; salting or file-level digests is next-round design work | knowledge note |
