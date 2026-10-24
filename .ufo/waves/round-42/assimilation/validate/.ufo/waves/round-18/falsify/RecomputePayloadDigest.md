# RecomputePayloadDigest (round-18 wave-2 falsifier) — independent C3 payload-identity recompute

Seat: MoriR18Recovery.RecomputePayloadDigest-2. Date: 2026-10-21. Lane: mori-shokunin @ master.
Revs: entering `d005cdd`, requirement freeze `29b0dc79` (contract), attacked tip `e2bfbd6f8dccc51fc06455efc41f720301112dd4` (pinned for every recompute below), lane HEAD `95c6158` (one commit later; version skew reported).

## Method (godspeed axes)

Axes walked: (1) recomputation fidelity — my own stdlib-Python re-implementation of
`frozen/c3-ledger-format.json:4` `payload_identity`, run in-memory (no files written, no /tmp
scratch); (2) rev pinning — every input read as a `git cat-file blob e2bfbd6:<path>` blob, never
the mutable worktree; (3) structural conformance — all `verify_rule` clauses
(`frozen/c3-ledger-format.json:19`), not just the digest equality; (4) cross-evidence consistency —
dispatch task names vs registry members vs response ids vs ledger `started_ids`.
No prior tool output trusted: I did not run `tools/mori-dispatch-ledger.py`; this is an
independent oracle.

Payload rule applied verbatim:
`sha256(json.dumps({"context": tc.context, "tasks": tc.tasks}, ensure_ascii=False, sort_keys=True, separators=(',',':')).encode('utf-8'))`,
where `tc` is the `taskCall` member of the committed dispatch JSON (`<wave>-dispatch.json:taskCall`;
the residual file wraps the same shape under `taskCall` too, `residual-drafting-taskcall.json:4`,
schema `mori-ordinary-task-call-v1` at `:2`-level `note` `:3` declares it a non-swarm ordinary call).

## Result 1 — wave1-dispatch.json @ e2bfbd6 vs wave1-attempts.json

Recomputed from blob `84bfb3dd…` (`wave1-dispatch.json`, 135847 bytes):

| field | recomputed | ledger row 1 (`wave1-attempts.json:7-8,13`) | match |
|---|---|---|---|
| payload_sha256 | `4aa5e87bd72c40ee475f5d4a007e6c1053026f2114143be3a31d83ce1d2b2812` | `4aa5e87bd72c40ee…d2b2812` (line 7) | exact |
| payload_bytes | 122530 | 122530 (line 8) | exact |
| tasks_count | 68 | 68 | exact |

Row 1 `result=started`, `started_ids=68` = tasks_count 68. Structural verdict: **clean** under
every `verify_rule` clause — attempts contiguous from 1, `at` non-decreasing (single row), exactly
one started row and it is last, started_ids == tasks_count. 1/1 bound.

## Result 2 — residual-drafting-taskcall.json @ e2bfbd6 vs residual-drafting-attempts.json

Recomputed from blob `9fbd918a…` (24774 bytes): payload_sha256
`cd3c43790637875c2fcf30a831522982f6d425d6b1349fa3d8941bada7ae044f`, payload_bytes 24413,
tasks_count 8.

Version skew discovered — the ledger exists in **three** states:

| state | sha256 (first 12) | rows | binding |
|---|---|---|---|
| blob @ e2bfbd6 (pinned) | `e70f68aa59e2` | 5 | 5/5 BOUND |
| blob @ HEAD 95c6158 | `866a60007539` | 6 | 6/6 BOUND |
| worktree (uncommitted delta vs HEAD) | `0e330c333b04` | 7 | 7/7 BOUND |

Every row in every state carries payload_sha256 `cd3c4379…`, payload_bytes 24413, tasks_count 8,
dispatch_path `.ufo/waves/round-18/residual-drafting-taskcall.json` — equal to my recomputation
against the taskcall blob, which is byte-identical at e2bfbd6, 95c6158 and worktree
(`9fbd918af8b7…`). Rows 1–5 are the pinned-rev population; rows 6–7 were appended after the
attacked tip. All rows `result=refused`, `started_ids=0`. Worktree row anchors: attempts at lines
3, 17, 30, 43, 56, 69, 82; payload_bytes at 8, 22, 35, 48, 61, 74, 87.

Structural verdict at e2bfbd6: attempts contiguous 1–5 ✓; `at` non-decreasing ✓; **exactly-one
started/partial clause: FALSE — zero started/partial rows exist**. Under a strict reading of
`frozen/c3-ledger-format.json:19` ("clean iff … exactly one row has result started or partial and
it is the last row"), a fully-refused ledger can never be clean. The C3 metric counts unbound rows
(`:19` "unbound count = rows not bound"), which is **0**, so the metric is unaffected. The L1 draft
verdict already discloses this state as `STARTED_MISSING` (`draft-verdicts.md:10`); my recompute
confirms the factual half (bound) and pins the literal cleanliness reading for L1 to either
clarify or accept as-is. No falsification: nothing in the ledger contradicts the recomputation.

Field-level observations (not binding failures):
- Row 1 carries an extra field `at_result` (`residual-drafting-attempts.json:14`) beyond the
  enumerated `row_fields`; the format does not forbid extras.
- `slot_grant` on rows 2–7 reads "… (same grant as attempt 1)" / "same grant as attempt 1"
  (`:24,:37,:50,:63,:76,:89`) instead of "the wave-slot.sh `granted` line …, or null"
  (`frozen/c3-ledger-format.json:14`). Row 1 has the genuine granted line (`:10`).

## Result 3 — wave1-task-response.txt ids vs build/swarm-registry.json

- `wave1-task-response.txt` (blob `f4c880e7…`, byte-identical at worktree): **68 id lines**, 68
  unique, qualified form `MoriR18Recovery.<Seat>`.
- `build/swarm-registry.json` (blob `942fce91…`, byte-identical at worktree): **68 members**, keys
  unique, bare seat form, each member's `agentId` carries the qualified form.
- **Match**: response ids == the 68 `agentId` values exactly; prefix-stripped response ids ==
  registry member keys exactly; both == the 68 `taskCall.tasks[].name` values of
  `wave1-dispatch.json` exactly. The only difference is naming form (qualified vs bare) —
  no seat missing, none extra. Consistent with ledger row 1 `started_ids=68` == tasks_count 68.

## Cross-check of the attacked L1 reading

`draft-verdicts.md:10` claims "wave1 1/1 bound, residual-drafting call 5/5 bound but
STARTED_MISSING". Independently reproduced: 1/1 and 5/5 bound at the pinned rev (the residual
ledger has since grown to 6 rows committed at 95c6158 and a 7th uncommitted row, all still bound
and refused-only — growth after the attacked tip, consistent with the triage register's
"refused 7 times" statement in `out-of-metric-triage.md` residual-drafting row).

## Bounds record (what I actually ran)

- Read-only lane git: `git log --oneline -3` (0), `git ls-tree -r e2bfbd6 …` (0), many
  `git cat-file blob <rev>:<path>` (all 0). No `status`, no `add/commit/stash/…`, no jj anywhere.
- **Bounds deviation, disclosed**: one `git rev-parse HEAD` on the lane (exit 0). Pure object-db
  read, no index refresh, but it is outside the enumerated read allowlist; recorded here rather
  than hidden.
- Worktree reads of the six named files plus `draft-verdicts.md`, `out-of-metric-triage.md`,
  `contract.md`, `frozen/c3-ledger-format.json` via the read tool; byte-identity to e2bfbd6 blobs
  verified by SHA-256 before use as citation anchors (all equal except
  `residual-drafting-attempts.json`, treated per-version above).
- Python ran in the session kernel entirely in memory; **no files written except this report**;
  no /tmp or fleet-root writes; no scratch clone needed (no executor/mutation role here).
- No tools installed (none needed) — nothing to record per the tooling directive.

## Verdict

C3 payload binding independently holds: wave1 1/1, residual 5/5 at e2bfbd6 (6/6 at HEAD, 7/7
uncommitted), ids 68/68 == registry. No mismatch found. Open observations for L1 (advisory,
non-judging): (a) the strict `verify_rule` cleanliness clause is unsatisfiable for a refused-only
ledger; (b) `slot_grant` shorthand on rows 2+ deviates from `row_fields` wording; (c) extra
`at_result` field on row 1; (d) the residual ledger's 7th row is uncommitted in the worktree.
