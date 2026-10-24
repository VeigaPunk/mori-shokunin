# ScribeLessonDraft — round-18 lesson sections and QUALITY rows 51–54 (draft)

Seat: MoriR18Recovery.ScribeLessonDraft (scribe, leaf). Lane: /home/vgpnk/Projects/shokunin/mori-shokunin.
Entering tip d005cdd (`d005cdde0e009dea6c0cc29b37163de536528658`); freeze commit 29b0dc7.
Target file `corpus/lessons/round-18.md` was NOT written. This report is the draft.
Status: draft complete; nothing executed beyond read-only commands listed in §5.

## 0. Scope and privacy boundary

- Read: `.ufo/waves/round-18/contract.md`; `frozen/*` at 29b0dc7 (policy, population summary, register, ledger format); committed lane text at d005cdd (`corpus/QUALITY.md`, `corpus/lessons/round-17*.md`, `SCORECARD.md`, `LOG.md`, `.ufo/waves/round-17/*-dispatch-attempts.json` key sets); fleet report grep for two labels only.
- Did NOT open: any must-redact build report body (only `sha256sum` and `wc -l` of their blobs), any session store, shell history, privileged or operator configuration, or private documents. No hit text is copied into this report; hits are cited by path, class id, count and SHA-256 only.
- Class tokens are avoided in this file so that the C1 gate does not count this report as a hit (rule: no literal class token in a lane-committed draft).

## 1. Observed facts used by the draft

F1 — C1 population (`frozen/c1-population.json` summary, observed): hits 119; files 28; non_author 3 (`corpus/lessons/round-17-verifier-spotcheck.md`, 3 hits); must_redact 40; metric_before 116 = 119 − 3. Per class: R1 22, R2 30, R3 9, R4 3, R5 4, R6 6, R7 13, R8 11, R9 21 (sum 119).

F2 — routed sub-count per must-redact file (observed counts): `.ufo/waves/round-17/build/PacmanActorTrace.md` 18; `.ufo/waves/round-17/build/OmpRetryConfig.md` 17; `.ufo/waves/round-17/build/SessionExitCorrelation.md` 5 (total 40). Blob SHA-256 at d005cdd: PacmanActorTrace `109e92f4d846c80d08a7ccb18c51dd42d1c0aabb9e921709515421c5f79097ef` (157 lines); OmpRetryConfig `d6340be91155b713e327f310f6b1f82eefe8746d46c6455b61fa8fb7392b2ec7` (223 lines); SessionExitCorrelation `437b902fbc1c74174e06549a107e2dfbab315d8bca0dcfc55dde36175a57a7bf` (137 lines).

F3 — non-routed hits the contract's "after = 0" also requires clearing (observed counts): `.ufo/waves/round-17/wave1-spec.json` 11; `.ufo/waves/round-17/wave1-dispatch.json` 11; `.ufo/waves/round-17/falsify/ConformanceAudit.md` 8; `.ufo/waves/round-17/build/DeadSeatCrossCheck.md` 6; `.ufo/waves/round-17/evidence/seat-live.json` 4; `corpus/lessons/round-17.md` 1 (author file, counts toward the metric); 20+ further files with 1–5 hits each. M1 scope is therefore every unallowlisted hit, not only the 40 routed hits.

F4 — round-18 committed handoff material already carries class-token hits (observed with `git -C <lane> grep -c` at commit 11db4df, a child of the freeze commit): `.ufo/waves/round-18/wave1-dispatch.json` 10; `.ufo/waves/round-18/wave1-plan.json` 10; `.ufo/waves/round-18/wave1-spec.json` 10; `.ufo/waves/round-18/frozen/c1-policy.json` 6 (the policy's own class regexes; a rule-(b) candidate only). The same M1 pattern recurs in round 18 before the retention gate exists. `.ufo/waves/round-18/wave1-attempts.json` showed 0 hits.

F5 — freeze ordering (observed): d005cdd is an ancestor of 29b0dc7; exactly one commit lies between them (29b0dc7 itself, touching only `.ufo/waves/round-18/` contract and frozen paths). 11db4df follows the freeze and touches only `.ufo/waves/round-18/`. `git diff-tree d005cdd HEAD -- tools` is empty, so no impl path has changed at HEAD. Freeze-order verdict for r18-C1..C3 at HEAD would be `no-implementation` [INFERENCE from verdict_rule, not run].

F6 — r17-C3 "pre-build" labels (five declared locations, the frozen register's list; each confirmed by grep for the label word): fleet `.ufo/reports/round-17/mori.md:25` and `:94` (fleet root, outside lane); lane `SCORECARD.md:1114`; lane `LOG.md:1197` (the same line also labels the C2 universe, which the register classes as constancy, not pre-build); lane `corpus/lessons/round-17.md:245` (M18). Non-author ruling: `corpus/lessons/round-17-verifier-spotcheck.md:207-213,398-402` — C3 pins and tool co-committed at `2be8294`; "not a demonstrated pre-build freeze" at `:128-130`.

F7 — `corpus/evidence/freeze-register.json` does not exist at d005cdd (`git cat-file -e` rc 128). The contract's "appended correction row" therefore creates the file; the freeze-order tool's `--corrections` path must treat it as the first correction, append-only.

F8 — legacy attempt receipts (observed key sets, no values read): wave1 `wave1-dispatch-attempts.json` has 5 rows with keys `{at, refused}` (4 rows) or `{at, refused, result}` (1 row, result `refused`); wave2 `wave2-dispatch-attempts.json` has 4 rows with keys `{at, refused}`. No row has `payload_sha256`, `payload_bytes`, `dispatch_path`, `tasks_count`, `slot_grant` or `started_ids`. Legacy unbound row count observed by key inspection: 9 [INFERENCE until `tools/mori-dispatch-ledger.py verify` runs]. Spotcheck self-disclosure: `corpus/lessons/round-17-verifier-spotcheck.md:291-297`.

F9 — V-table (observed text, dispositions only): V1–V3, V5–V14 carried (V5–V7 at `:309-311`); V4 external handoff to operator/tsukuroi (`:308`); V15 not a violation on its cited context (`:319`); table at `:305-319`; routed defect 3 at `:403-407` (contract item 3 names V1–V3/V5–V14 plus L1 authorization). Round-17 M10 (`corpus/lessons/round-17.md:75`) is the L1 authorization conflict.

F10 — existing QUALITY tail (observed): criteria 43–50 added round 17; last row 50 at `corpus/QUALITY.md:146-150`. Captured-by check for M1: Q44 (CONTEXT_OK receipt bound to spec SHA, instruction text), Q45 (probe disclosure enumeration), Q50 (derived metadata honors retention contract; a display-cap rule) — none minimizes committed handoff material. Hence captured-by none is confirmed.

## 2. Draft `## Mistakes` rows (for `corpus/lessons/round-18.md`)

Columns follow round-17 format: ID | Class | Evidence pointer | Captured-by | Fix / falsifier. Class `adjacency`, `provenance` are new labels; `reference-drift` and `scope` are existing.

| ID | Class | Evidence pointer | Captured-by | Fix / falsifier |
|---|---|---|---|---|
| M1 | adjacency | Population at d005cdd: 119 hits, 28 files, 3 non-author, 40 routed, metric 116 (`.ufo/waves/round-18/frozen/c1-population.json` summary). Routed: `.ufo/waves/round-17/build/PacmanActorTrace.md` 18, `…/OmpRetryConfig.md` 17, `…/SessionExitCorrelation.md` 5 (blob SHA-256 in F2). Non-routed: `…/wave1-spec.json` 11, `…/wave1-dispatch.json` 11, `…/falsify/ConformanceAudit.md` 8, `…/evidence/seat-live.json` 4, `corpus/lessons/round-17.md` 1. Policy and disclosure: `corpus/lessons/round-17-verifier-spotcheck.md:339-346`, routed defect 1 at `:388-397`. | none. Q44 binds dispatch instruction text to spec SHA; Q45 enumerates probe disclosures; Q50 is a display-cap rule. None minimizes committed handoff material (retention, not disclosure). | Store scoped summaries, counts and SHA-256 of private sources — never excerpts, session or store identities, or configuration values. Redact (no allowlist row) the three routed files and every other unallowlisted hit found by the whole-tree sweep, not only the 40. Failure-capable check: `tools/mori-retention-gate.py scan --repo <lane> --rev d005cdd --policy frozen/c1-policy.json --expect-population frozen/c1-population.json` must exit 1 and reproduce 119 / 116 / 40; each planted fixture must exit 1. After-state: exit 0 with 0 routed hits, zero `allowlist_forbidden` findings, and 0 unallowlisted hits at the measured round-18 commit (the F4 round-18 hits included). Already-pushed history is not rewritten; exposure assessment stays with the operator/kagi owner. → Q51 |
| M2 | reference-drift | r17-C3 declared `pre-build` at five locations: `.ufo/reports/round-17/mori.md:25,94` (fleet root), `SCORECARD.md:1114`, `LOG.md:1197`, `corpus/lessons/round-17.md:245`. Register row in `frozen/c2-register.json`. Non-author ruling co-evolved: `corpus/lessons/round-17-verifier-spotcheck.md:207-213,398-402`; C3 pins and tool co-committed at `2be8294`. | none at d005cdd: no freeze-order check existed; the ruling was recorded only in the spotcheck; no QUALITY criterion covered freeze labels. | A `pre-build` label is a verdict, not prose. Failure-capable check: `tools/mori-freeze-order.py check --repo <lane> --register frozen/c2-register.json` must print r17-C3 `verdict: co-evolved`, `co_committed: true`, overclaim 1 and exit 1 at d005cdd; a planted co-committed fixture must grade `co-evolved` and fail when labelled pre-build. Correction: append-only row in `corpus/evidence/freeze-register.json` (file absent at d005cdd, F7); after-state overclaims 0, oracle agreement 3/3 with the non-author rulings. Round-18 claims are `pre-build` only if 29b0dc7 precedes the first impl commit (currently none: verdict `no-implementation`). Do not use the word "precommitted" as a freeze label. → Q52 |
| M3 | provenance | `.ufo/waves/round-17/wave1-dispatch-attempts.json` (5 rows) and `.ufo/waves/round-17/wave2-dispatch-attempts.json` (4 rows); observed key sets `{at,refused}` / `{at,refused,result}` only — no payload digest, byte length, dispatch path, slot grant or started-id field (F8). Self-disclosure `corpus/lessons/round-17-verifier-spotcheck.md:291-297`. | partial. The limitation is recorded in the spotcheck only. Q44 binds the spec, not each attempt's payload bytes. | Append one ledger row per task-call attempt before the call, completed with the observed result, per `frozen/c3-ledger-format.json`. Failure-capable check: `tools/mori-dispatch-ledger.py verify --repo <lane> --rev d005cdd --ledger <round-17 wave1 attempts>` reports 5 unbound rows and exits 1; the wave2 ledger reports 4 and exits 1; planted arms (tampered payload, mismatched digest, non-final started row, duplicate started row) each exit 1 with unbound or failed findings; bad input or tampered snapshot exits 2. Round-18 `wave*-attempts.json` must verify clean (0 unbound). Known limit: the binding proves the committed payload equals the hashed payload, not the exact bytes the task tool received. → Q53 |
| M4 | scope | Carried V-table `corpus/lessons/round-17-verifier-spotcheck.md:300-320` (V5–V7 at `:309-311`); routed defect 3 at `:403-407`; round-17 M8–M14 and M10 (`corpus/lessons/round-17.md:70-76`, `:234-244`). Carried set: V1–V3, V5–V14 plus the L1 authorization conflict (M10); V4 is an external handoff; V15 is not a violation on its cited context. | partial. QUALITY 37 (messaging restriction), 38 (/tmp writes), 39 (selftest is not permission), 44 (instruction receipt) cover some classes. VCS-scope (V1, V2, V5–V7, V12, V14) and field-projection (V3, V8–V11, V13) classes have no criterion, and the next round did not restate them. | Each round-18 wave context restates the pre-action bounds: lane reads only via `git -C <lane> show|log|ls-tree|cat-file|rev-list|diff-tree|grep`; jj only with `--ignore-working-copy`; scratch only under the seat's own `.scratch`; field projection limited to allowlisted fields. Failure-capable checks: `tools/mori-round17-context-check.py` on the round-18 wave context must exit 1 when any bound clause is removed (missing-clause finding). `tools/mori-retention-gate.py` exit 1 catches only the committed field-projection leakage its classes can see (F4). The VCS items have no committed-artifact check: they are instruction text, not runtime prevention. A clean final state does not close V-items; they stay open named debt. → Q54 |

## 3. Draft QUALITY criteria rows (append to `corpus/QUALITY.md` after row 50)

Heading to add before the rows (matching existing style): `## Criteria added round 18`

51. Committed handoff material (reports, dispatch specs, evidence JSON) carries scoped summaries, counts and SHA-256 of private sources, never excerpts, session or store identities, or configuration values. A whole-tree retention sweep at the measured revision must exit 0 with zero unallowlisted hits; a must-redact file carries no allowlist row. Disclosing a copy does not satisfy this criterion. ← lessons/round-18.md#M1; lessons/round-17-verifier-spotcheck.md:339-346,388-397.
52. A `pre-build` freeze label is a verdict from the freeze-order check, not prose: a claim's frozen inputs must precede its first implementation commit strictly. Inputs co-committed with an implementation grade `co-evolved`, and a co-evolved claim keeps its correction row, never a rewritten label. ← lessons/round-18.md#M2; lessons/round-17-verifier-spotcheck.md:207-213,398-402.
53. Every dispatch attempt is recorded per attempt, before the call, with the SHA-256 and byte length of its committed payload and the observed result. A row without a payload digest, a tampered or mismatched payload, or a non-final or duplicate started row is unbound and fails the ledger verify. Spec-level binding (criterion 44) does not satisfy this. ← lessons/round-18.md#M3; lessons/round-17-verifier-spotcheck.md:291-297.
54. Carried procedural defects remain open, named debt in the next round: every wave context restates the pre-action VCS, scratch and field-projection bounds, and each carried V-id keeps its disposition. Instruction-text bounds are never cited as runtime prevention, and a clean final state does not close a carried item. ← lessons/round-18.md#M4; lessons/round-17-verifier-spotcheck.md:300-320,403-407.

## 4. Findings for the integration owner (not lesson text)

1. C1 "after = 0" must cover F3 and F4, not only the three routed files; the contract's "116 (routed 40)" frames the metric correctly, but the routed-file description understates the scope (28 files).
2. Round-18 committed wave1 dispatch, plan and spec files (F4) carry class-token hits at 11db4df before the gate exists. Adjudicate each under the policy's rule (a)/(b)/(c) or redact; do not allowlist a must-redact path.
3. The register's `corpus/evidence/freeze-register.json` does not exist at d005cdd (F7); creating it is the correction mechanism the contract names.
4. Verdicts for r17-C1 and r17-C2 are [INFERENCE] from the spotcheck rulings; the tool must produce them, and oracle agreement is 3/3 only if it does.
5. `corpus/lessons/round-17.md:245` and the `LOG.md:1197` sentence are both cited by the register; the LOG line mixes a C2 constancy statement with the C3 label. Keep the appended correction precise about which claim each sentence labels.

## 5. Commands run (all read-only; no installs or updates)

- `read` of `.ufo/waves/round-18/contract.md` (ok).
- `git -C <lane> show d005cdd:corpus/QUALITY.md | tail/head/grep` — rc 0.
- `git -C <lane> ls-tree --name-only d005cdd corpus/lessons/` and `-r ... .ufo/waves/round-17` — rc 0.
- `git -C <lane> show 29b0dc7:.ufo/waves/round-18/frozen/{c2-register.json,c1-policy.json,c1-population.json,c3-ledger-format.json}` piped to `head`/`jq` — rc 0.
- `git -C <lane> show d005cdd:corpus/lessons/round-17.md` and `round-17-verifier-spotcheck.md` with `sed -n` ranges and `grep -n` — rc 0.
- `git -C <lane> grep -n -i precommit d005cdd -- …` — rc 0 (3 lane hits).
- `grep -n -i "precommit|pre-build"` on `/home/vgpnk/Projects/shokunin/.ufo/reports/round-17/mori.md` — rc 0 (2 fleet hits; read-only, fleet file not written).
- `jq` key/count summaries of frozen population and round-17 attempt ledgers — rc 0 (no hit text printed).
- `sha256sum` and `wc -l` of three must-redact blobs at d005cdd — rc 0 (no content displayed).
- `git merge-base --is-ancestor d005cdd 29b0dc7` — rc 0; `git rev-list --reverse --topo-order d005cdd..29b0dc7` — 1 commit; `git diff-tree` of 29b0dc7 and 11db4df — frozen/round-18 paths only; `git diff-tree d005cdd HEAD -- tools` — empty.
- `git cat-file -e d005cdd:corpus/evidence/freeze-register.json` — rc 128 (absent).
- `git -C <lane> grep -c -E <class-token alternation> 11db4df -- .ufo/waves/round-18/` — rc 0 (counts only; the alternation is not printed here).
- Own-process scratch: one `git show d005cdd:corpus/lessons/round-17-verifier-spotcheck.md > /tmp/x` redirect was made in error (a /tmp write, forbidden for seats). The file held committed non-author lesson text, no private value; it was removed with `rm -f /tmp/x` (rc 0). Disclosed as a scope deviation (cf. QUALITY 38).

Tools installed or updated: none. Record: no tool, version, channel or reason — nothing installed.

Not executed: `tools/mori-retention-gate.py`, `tools/mori-freeze-order.py`, `tools/mori-dispatch-ledger.py`, `tools/mori-round17-context-check.py` (none is named in my item as runnable; the draft names their checks for the integration owner to run once). No selftest was run. No live probe, journal query, background job, pacman transaction or network fetch.

## 6. Checks for the main agent to run once (named, not executed here)

- `tools/mori-retention-gate.py scan … --expect-population frozen/c1-population.json` at d005cdd: expect exit 1, 119 / 116 / 40.
- `tools/mori-freeze-order.py check … --register frozen/c2-register.json` at d005cdd: expect r17-C3 `co-evolved`, overclaim 1, exit 1.
- `tools/mori-dispatch-ledger.py verify … --ledger` on round-17 wave1 and wave2 attempts: expect 5 and 4 unbound, exit 1.
- `tools/mori-round17-context-check.py` on the round-18 wave1 context: expect exit 0, then exit 1 when a bound clause is removed in a planted copy.
