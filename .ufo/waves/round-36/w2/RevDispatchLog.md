# RevDispatchLog — mori r36 wave 2 — dispatch-log truthfulness audit

Seat: `mori-r36-w2-RevDispatchLog-23` (leaf; no subagents; no lane edits except this report).
Measured: 2026-10-23T18:59Z (audit ran ~18:50–19:05Z against the lane at `/home/vgpnk/Projects/shokunin/mori-shokunin`).

Attacks: the truthfulness of
`.ufo/waves/round-36/dispatch-log.txt` — every claim reconciled against artifacts:
c0 25 seats (25 `Ctl*.md` reports), w1 33 tasks (dispatch payload + registry + report files; dead/refused seats
named with the log's error texts), the three attempt-1 commits (`da12b37`, `c1a026c`, `5842dc0`), the data
commit `bf0df77fee4b6ef54a90aea09335c7617f125151`, the two counter receipts, and the gate/index checks (re-run live).
FAIL any claim the artifacts do not support.

Tooling installs (authorization record): **none** — only the lane's own read-only tools were run.

---

## 1. Artifacts consulted

- `dispatch-log.txt` at data tip `bf0df77` (26 lines, committed) and at integration `9ca8f2e` (42 lines).
- `.ufo/waves/round-36/{c0-dispatch.json,w1-dispatch.json,w1-spec.json,w1/swarm-registry.json,w2/swarm-registry.json}`.
- `c0/` (25 `Ctl*.md` + `controls/` 25 `.py`), `w1/` (28 `.md` + registry), `w2/`.
- `evidence/{c1-before,c2-before,c1-after,c2-after,c0-rescore-v2,census-start,freeze,freeze-v2}.txt`, `evidence/refs/`.
- Commits `da12b378`, `c1a026cb`, `5842dc04`, `bf0df77`, `9ca8f2e` (git, read-only).
- Live re-runs: `tools/mori-sources-appendonly.py` gate, `tools/mori-index-clean.sh`, `tools/mori-source-drift.py --selftest`.

## 2. Claim-by-claim reconciliation

| # | dispatch-log claim | artifact | status |
|---|---|---|---|
| 1 | census start 10:4xZ, `mori ok`, `EXIT=0` (`evidence/census-start.txt`) | receipt mtime 07:48:53L = 10:48:53Z; last line `mori ok`, `EXIT=0` (13 W04 dup-url warnings precede) | TRUE |
| 2 | counters before-receipts `c1/c2 tool_absent unmet` (11:47Z) | `c1-before.txt` = `tool_absent / C1=unmet / EXIT=1`; `c2-before.txt` = `tool_absent / C2=unmet / EXIT=1` (mtime 08:47:08L = 11:47:08Z) | TRUE |
| 3 | freeze commit next (11:47Z) → attempt-1 freeze commit `da12b37` | `da12b3786f88626a26c951fab6b716bef6b8498e`, committer 08:47:20L = 11:47:20Z, subject "freeze C1/C2 contract and counters ... before receipts"; `freeze.txt` mtime 08:47:16L | TRUE |
| 4 | c0: 25 seats `CtlK1-K11,K13; CtlJ1-J13`, payload `c0-dispatch.json`, settle 12:33Z | `c0-dispatch.json` tasks=25, names exactly the 25 above; `c0/` has exactly 25 `Ctl*.md`; `c0/controls/` has 25 `.py` | TRUE |
| 5 | c0 v1 results: K9 met, J11 met (harness-keyed), K13 met (rule-level skip / oldest copy) | `CtlK9.md` head `control K9 shape harness-keyed`, `counter_sha256 ed3f0e5e…` (= v1 counter pin, contract v2 section line "v1 counters sha256 ed3f0e5e…4145, 302f9aa0…affb, frozen at da12b378"); `CtlJ11.md` `shape harness-keyed`, v1 pin; `CtlK13.md` `shape rule-level skip (oldest copy)`, v1 pin | TRUE |
| 6 | c0 v2 re-score 12:03Z: 25/25 unmet, refs met (`evidence/c0-rescore-v2.txt`) | 27 `==` headers = 25 controls + REF1 + REF2; `C1=unmet`×12 + `C2=unmet`×13 = 25; `C1=met`×1 (REF1), `C2=met`×1 (REF2); REF shas match `evidence/refs/ref-c1.py` `0d9c808b…` / `ref-c2.py` `08874f8f…`; header timestamp 12:03:04Z; freeze-v2 mtime 09:03:04L = 12:03:04Z | TRUE |
| 7 | freeze v2 commit `c1a026cb` (12:03Z) | `c1a026cb156c5fe84d76dc79190f1885ad11abf4`, committer 09:03:05L = 12:03:05Z, subject "C0 control receipts (K9/J11/K13 met v1), counters re-designed ... 25/25 controls unmet under v2" | TRUE |
| 8 | w1: 33 tasks; `w1-dispatch.json`; granted after 642 s; settle 12:50Z; dispatched 12:03Z as one task call | `w1-dispatch.json` `counts {spawn:33,resume:0,total:33}`; `taskCall.tasks` = 33 names; registry `w1/swarm-registry.json` = 33 members, same names/roles; `createdAt 11:47:57.340Z` + 642 s = 11:58:39Z ≈ grant 11:59Z; `updatedAt 12:03:19Z` ≈ dispatch 12:03Z | TRUE |
| 9 | w1 dead: MutC1Novel, MutC2Novel (rate limit, 6 s, quoted text) and hold: CritC1Counter / CritC2Counter (cyber_policy, 14 s / 29 s) | names+roles present in payload/registry (mutation-tester / critic); none of the four has a report file in `w1/`; the exact quoted error strings appear **nowhere else** in the lane (grep for `resource_exhausted`/`cyber_policy` outside the log hits only older-round lessons/evidence and this round's w2 spec) — log-only, self-reported | TRUE* (*unwitnessed, see §4/§6) |
| 10 | MutC1Novel/MutC2Novel cause = Main routing change (m_swe → m_sol) | log-only narrative; no independent artifact; consistent with the rate-limit text ("Reached free model rate limit", reset 17:01Z ≈ 12:04Z+4h56m) | TRUE* (unwitnessed) |
| 11 | C0 settled 25/25, `CtlJ12 last` (12:04Z) | `CtlJ12.md` mtime 09:04:00L = 12:04:00Z = latest of the 25 (first at 11:49Z) | TRUE |
| 12 | C1 declared exploratory before data; contract last section; counters/predicates unchanged; commit `5842dc0` | `5842dc04bb3d3b7aa2bdaaf462dcff536358444` committer 09:09:14L = 12:09:14Z, subject "C1 declared exploratory before data ..."; contract@bf0df77's **last section** is "C1 declared exploratory before data (12:10Z, after wave-1 CritAxisFit)"; `w1/CritAxisFit.md:10` `VERDICT: C1 fails`; `w1/MineCopyFidelity.md` shows S156–S160 excerpts and S176/S177 footer-only drift; P-C1/P-C2 sentences byte-identical between c1a026cb and bf0df77 (diff) and match the receipt headers verbatim | TRUE |
| 13 | C2 receipt at bf0df77: `C2=met`, blind 24/24, real pass, oracle ids 18, seed 15440749816798970567 | `evidence/c2-after.txt` verbatim: `blind arm: 24/24 …`, `real arm: pass`, `appendonly_violations=18 ids=[18 ids] …`, `C2=met`, `seed=15440749816798970567`; mtime 15:20:27L = 18:20:27Z | TRUE |
| 14 | C1 receipt at bf0df77: `C1=met` byte-evidence, blind 40/40 mismatches=0, real 220 rows / oracle_fetched=58 / fresh=49 / drifted=9 / excluded=0 / tool mismatches=0, seed 7388485190103051243 | `evidence/c1-after.txt` verbatim: `blind_rows=40 … mismatches=0`; `real_rows=220 oracle_fetched=58 oracle_fresh=49 oracle_drifted=9 oracle_excluded=0 … mismatches=0`; `C1=met`; `seed=7388485190103051243`; mtime 15:21:50L = 18:21:50Z | TRUE |
| 15 | round append-only gate: `round_changed=[]` exit 0 | live re-run: `python3 tools/mori-sources-appendonly.py bf0df77fee4b6ef54a90aea09335c7617f125151 --round-base 6bd57097` → `… superseded=[18 ids] round_changed=[]`, `EXIT=0` (violations 18 all discharged by supersede rows S073/S201/S202/S206–S220) | TRUE |
| 16 | index clean staged=0 intent_to_add=0 | live re-run: `bash tools/mori-index-clean.sh .` → `MORI_INDEX_CLEAN staged=0 intent_to_add=0`, `EXIT=0`; `git diff --cached --name-only` = empty (0 files) | TRUE |
| 17 | attempt-2 kept: SOURCES S205–S220, QUALITY 103–105, SKILL Round36 rows, corpus/evidence/sources-r36/, knowledge/source-drift-r36.md | at bf0df77: 16 table rows S205–S220 present; QUALITY 98/103/104/105 present (lines 715/822/829/837); SKILL.md Round36 section (856–874) with the three tool rows; `corpus/evidence/sources-r36/` has the S205+ `.src` copies; `knowledge/source-drift-r36.md` present | TRUE |
| 18 | selftest PASS 4 cases (drift tool) | live re-run: `python3 tools/mori-source-drift.py --selftest` → `selftest exit_code PASS / row_states PASS / summary PASS / missing_sources_exit2 PASS`, `MORI_SOURCE_DRIFT_SELFTEST: PASS (4 cases)`, `EXIT=0` | TRUE |
| 19 | data commit landed `bf0df77` (15:4xZ, helper push verified) | `bf0df77fee4b6ef54a90aea09335c7617f125151` = HEAD; **committer 15:20:10L = 18:20:10Z**, author 12:09:14Z — the "15:4xZ" label matches no artifact timestamp (see F3). "helper push verified" not independently checkable (fetch prohibited) | PARTIAL (hash TRUE; timestamp FALSE; push unverifiable) |
| 20 | w1 reports "30/33" in attempt-2 kept line | **FALSE** — see F1 (actual 28 on disk; also committed at bf0df77 as 28) | **FALSE** |
| 21 | "tools/mori-source-drift.py was never built by attempt 1 — L1 built it" | **FALSE literal**, see F2 — scratch build exists (12:26:50Z, parse-OK, different sha); true only as "never delivered/landed" | **FALSE literal** |

## 3. Findings (by severity)

### F1 [moderate] — false report count "30/33" in the committed log — `dispatch-log.txt@bf0df77:21`
Command: `git show bf0df77:.ufo/waves/round-36/dispatch-log.txt` (26 lines) → line 21:
`kept: … + w1 reports (30/33; MutC1Novel,` …
Observed artifacts:
- `w1-dispatch.json` `counts`: `spawn 33`; payload = 33 named tasks.
- `w1/` contains exactly **28** `.md` reports (glob; committed set at bf0df77 = the same 28 per `ls-tree`).
- Set difference dispatch − reports = 5 names: MutC1Novel, MutC2Novel, CritC1Counter, CritC2Counter, **BuildDriftTool**.
- 33 − 2 dead − 2 held = 29 maximum possible reporters; 28 exist. "30" is arithmetically impossible on any reading, and 30 + the 4 named exclusions = 34 > 33 (double-count). The true reconciliation is `33 = 28 + 2 dead + 2 refused-hold + 1 (BuildDriftTool: no report, no return)`.
- Lane-wide grep for `30/33`: only occurrence is `dispatch-log.txt:21`. No claim/contract/counter cites it (C1/C2 and repairs unaffected). It is a false count in the permanent round record at the data tip.

### F2 [moderate] — "never built by attempt 1" contradicted by the seat's scratch artifact — `dispatch-log.txt@bf0df77:25`
Line 25: `discarded: none; rebuilt: tools/mori-source-drift.py was never built by attempt 1 — L1 built it to the …`.
Observed artifact: `/fast/scratch/hyaku/mori-r36/BuildDriftTool/tools/mori-source-drift.py`
- `stat` → `2026-10-23 09:26:50.552379884 -0300` (12:26:50Z, inside the w1 window: dispatched ~12:03Z, settle 12:50Z), size 17911.
- `python3 -c "import ast; ast.parse(...)"` → parse OK (complete tool, not a fragment).
- `sha256sum`: scratch `460c34a970b8acbc…` vs lane tool `578667ca3ad0a3a8…` (different build; `diff` 655 lines).
The literal claim is false: a build was produced by attempt 1 (in the seat-named scratch dir, in-window). What is true is "never delivered/landed by attempt 1" (no `w1/BuildDriftTool.md`, and the lane tool is L1's build). Attribution of the scratch build to the BuildDriftTool seat is [INFERENCE] from the seat-named directory and timestamp (writer not witnessed).

### F3 [minor] — timestamp labels inconsistent with artifact timestamps — `dispatch-log.txt@bf0df77:30-31`
- Line 30 `15:4xZ data commit landed bf0df77…`; line 31 `15:5xZ counters scored …`.
- Artifacts: bf0df77 committer **18:20:10Z** (author 12:09:14Z); `c2-after.txt` mtime **18:20:27Z**; `c1-after.txt` **18:21:50Z**; `drift-live-r36.txt` 18:47:06Z; integration commit `9ca8f2e` committer 18:58:57Z while its new log line says `17:1xZ integration batch`.
- All morning entries (10:4x/10:48/11:47/11:48/11:59/12:03/12:04/12:10Z) match UTC artifact timestamps to the minute; the afternoon entries match no artifact timestamp under any consistent timezone reading (UTC reading off 2.5–3 h; local-as-Z reading off ≥20 min; `17:1xZ` is in the future relative to the commit). The labels are mis-stamped/mislabeled. This remains in the integration-repaired version (lines 30–38 there).

### F4 [observation] — evidence limits on the four reported exclusions
- The w1 registry records `agentId: null, item: null` for all 33 members (no return status anywhere); harness transcripts for past-session subagents are not persisted. The only witnesses for the four exclusions are the log's own text (error strings, durations) and the absence of their report files. `history://` lists no w1 seat agents.
- Duration claims (6 s/14 s/29 s) and `live=73/74/67`, "C2 49m, C1 57m" are log-only, unfalsifiable from artifacts. "Granted after 642 s" is corroborated indirectly (registry createdAt + 642 s = grant 11:59Z).

## 4. Post-audit state (record under audit changed mid-wave)

During this audit the working-tree `dispatch-log.txt` was amended (from "30/33"/"never built" to "28/33 on disk; BuildDriftTool never returned — its scratch build survived but was never delivered … (w2/RevWave1Audit F2)") and committed in integration `9ca8f2e` (annitter 18:58:57Z) together with c1/c2-after receipts, drift-live receipt, freeze-v3. The false lines F1/F2 are therefore **already repaired in the current HEAD**; the defects stand in the immutable data-tip record `bf0df77`. Remaining working changes: `contract.md` (post-integration history-correction edit) and two new w2 reports (untracked). No index entries (staged=0, intent_to_add=0 still).

## 5. Residual risk and verification gaps

- F4: dead/refused error strings are unwitnessed (log-only); return status of the five non-reporting seats is not machine-attested (registry null agentId).
- "helper push verified" not independently checkable (git fetch prohibited for this seat).
- `live=N` seat counts and run durations not verifiable from lane artifacts.
- The scratch build's authorship (F2) is inference.
Measurements above are reproduced verbatim; claims 1–19 reconcile TRUE against artifacts. Fail triggers fire:

## 6. Verdict

Attacked item: dispatch-log truthfulness. Fail triggers fire:
- F1: `dispatch-log.txt@bf0df77:21` — false "30/33" (actual 28; arithmetic impossible; BuildDriftTool unaccounted).
- F2: `dispatch-log.txt@bf0df77:25` — literal false "never built by attempt 1" (scratch build exists).
- F3: `dispatch-log.txt@bf0df77:30-31` — timestamp labels match no artifact timestamps.

VERDICT: **FAIL** — defects in the committed data-tip record (F1/F2 already amended by integration `9ca8f2e` during the wave; F3 still present in the amended version). No remediation performed (mori province: detection and report only).
