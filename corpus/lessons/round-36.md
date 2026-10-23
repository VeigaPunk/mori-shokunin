# Round 36 — 2026-10-23 (L1 MoriR36, attempt 2; attempt 1 died with the phase-4 orchestrator, addendum §5 inheritance)

## Gate

Candidates this round:

| candidate | decision | evidence |
|---|---|---|
| C2 — SOURCES append-only gate capability (`tools/mori-sources-appendonly.py`, promoted from the round-35 wave script with new deleted-row detection) | **admitted** (measured) | frozen counter `count-c2.py` at clean tip `bf0df77`: blind arm 24/24 sandbox histories match the run-time-hidden truth; real arm == independent oracle at rev 6bd57097 (base f10a320d), 18 ids; `C2=met`, seed 15440749816798970567 (`.ufo/waves/round-36/evidence/c2-after.txt`); re-scored clean across 7 fresh draws (w2/ExecReC2A.md) and fixed seeds 42/7; independently re-derived without the counter's code by w2/RevC2Oracle.md (byte-identical oracle) |
| C1 — source-drift byte probe (`tools/mori-source-drift.py`) | **admitted as technique; claim lands `unprovable`** | declared exploratory before data (attempt-1 ruling, commit 5842dc0): the frozen byte predicate cannot carry a freshness verdict (w1/CritAxisFit.md — unchanged source classifies `drifted` when the committed copy is an annotated excerpt). Byte behavior verified: blind 40/40 mismatches=0, real arm fetched=58 fresh=49 drifted=9 mismatches=0, seed 7388485190103051243 (evidence/c1-after.txt). No named non-author reviewer exists inside the round — the hyaku closure session is the reviewer of record; without its judgment the claim is `unprovable`, reported as such. |
| SOURCES rows S205–S220 (16 rows; S211 a rejection) | **admitted** | each row opened this round; located quotes verified contiguous ≤25 words by w1 SupS* and w2 RevSupS* seats (all PASS; S210 copy drift = post-copy asset rebuild, taught prose intact; S211 is byte-unstable by construction — rejected row, never `fresh`) |
| README coverage-map rows (source-drift probe; append-only gate) | **admitted** | `corpus/README.md` Round-36 section |

Rejected: none new this round (S211's rejection is recorded as a row, per the rejection-is-evidence rule).

Spot-check result: **left for the outside closure** (every seat above is lane-dispatched; PROTOCOL.md:63-64).

Registry changes logged (rule 2 old→new): S205 `used-by` `tools/mori-source-drift.py` →
`corpus/knowledge/source-drift-r36.md` (mined used-by must cite the entry that cites the row;
w2/RevKnowledgeDrift F2). Status/recheck unchanged.

## Mistakes

| # | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M1 | axis-fit (a counter that cannot carry its axis) | w1/CritAxisFit.md: S156's pinned source is byte-identical to its round-30 recorded digest yet classifies `drifted` because the committed copy is an annotated excerpt; 5 of the then-7 oracle-drifted rows are such excerpts | none — caught pre-data by the wave-1 critic; became the pre-data exploratory declaration (contract.md, commit 5842dc0) and QUALITY 105 | C1 declared exploratory before any tool landed; P-C1 kept and reported as byte-behavior evidence only; QUALITY 105 requires comparing the live full-document sha256 with the recorded open-time sha before counting a drifted row as a source change |
| M2 | number-drift (a count carried past its population) | the "seven drifted rows" observation (c0-rescore, 12:03Z, 204-row corpus) was copied into post-data guidance (knowledge note, QUALITY 105 witness, SKILL Round36 bullet) while the landed 220-row corpus measures **nine** (adds S210 asset rebuild, S211 fetch-varying page); caught independently by five w2 seats (ExecDriftLive, ExecReC1A, ExecManualOracleSample, RevC1Interface, RevKnowledgeDrift) | none — the w2 attack wave | all four sites now carry the dated nine-row enumeration with commands and open-time shas (`corpus/knowledge/source-drift-r36.md`, QUALITY 105-addendum, SKILL.md Round36, README Round-36); the note records the S210/S211 reader-action classes |
| M3 | landing (attempt died mid-round) | attempt 1 of round 36 died with the phase-4 orchestrator (~09:30 -03): contract, counters, c0 receipts and 28 wave-1 reports were committed, but the C1 tool, the two data receipts and the wave-1 dispatch payload were not; the claim had no runnable artifact at the pushed tip | addendum §5 (earlier-attempt inheritance) | this attempt re-verified every inherited artifact (counters re-pinned, receipts re-scored at a clean tip, wave-1 reports audited by RevWave1Audit/RevDispatchLog) and landed the missing bytes; the failure mode (orchestrator death between waves) is recorded here for the operator |
| M4 | scope (remediation wording in a detection lane) | w2/RevNoHarm: the drift note's exit-2 row said "Restore DIR/corpus/SOURCES.md and run again" | w2/RevNoHarm (no prior criterion names doc-level remediation phrasing) | reworded to detection+report language; the restore decision is named operator-owned. Related disclosed residual (frozen bytes, cannot edit post-data): count-c2.py:70-82 SIGKILLs only its own timed-out sandbox child on a tool timeout — registered as r37 debt |

## Round shape (for the report)

c0 25 + w1 33 (attempt 1, settled; dead: MutC1Novel, MutC2Novel — provider rate limit; refused-hold:
CritC1Counter, CritC2Counter — provider cyber_policy) + w2 66 (attempt 2, dispatched by the orchestrator per
the mid-flight directive; 36+ reports landed at integration time, the rest recorded in the dispatch log).
Round total 124 ≤ 128. Registry note (w2/RevWave1Audit F3): the w2 swarm-registry records null agentId/item
for all seats — a side effect of the orchestrator-inline dispatch (the L1 never sees the task-call return ids);
disk reports under `.ufo/waves/round-36/w2/` are the only return evidence.
