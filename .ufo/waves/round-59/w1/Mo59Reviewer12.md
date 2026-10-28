# Mo59Reviewer12 — settlement artifact survey verification (read-only)

**Verdict: ADVERSARIAL FINDING (2 committed artifacts falsify the universal reading
of the "note null / output nonempty / member key-set" claims); 8/10 files clean.**

Scope executed: all **10** committed `*-results.json` files under rounds 50–58 at
freeze revision `60b3a76ad0524c8978cc51922940be1c8c388915` (≥ the required 6).
Blobs verified byte-identical across entering `2b9f0397`, freeze `60b3a76a`, and
HEAD `8ff344ff` via `git rev-parse <rev>:<path>` — all `SAME`, so the survey is
revision-stable.

## Claim predicates tested (per file, per member)

Derived from the seat brief + `tools/mori-settlement-scan.py` (sha256
`4c04bf21…5ac9a9` == counter PIN `count-c2.py:53`; docstring lines 9–13):
- **A top-level keys:** object; `lane`/`wave` nonempty str, `round` int≥1,
  `seats` int == `len(results)`, `results` list; exact key set reported.
- **B member key set:** every member a dict with exactly `{name,agent,output,note}`.
- **C note null:** every `member.note is null`.
- **D output nonempty:** every `member.output` is a nonempty str.
- Aux: `name` nonempty/unique, `agent` in the 10-role enum, seats==members.

## Results (all 10 committed *-results.json, r50–r58)

| file | seats=members | top keys | member keys | note null | output nonempty | verdict |
|---|---|---|---|---|---|---|
| r50 a2w1 | 64/64 | exact 5 | exact | **FAIL 64/64 non-null** | **FAIL 64/64 null** | **COUNTEREXAMPLE** |
| r51 w1 | 68/68 | exact 5 | exact | 0 non-null | 0 empty/null | OK |
| r52 w1 | 68/68 | exact 5 | exact | 0 non-null | 0 empty/null | OK |
| r53 a2r1 | 8/8 | exact 5 | exact | 0 non-null | 0 empty/null | OK |
| r53 w1 | 67/67 | **+4 extras** | **67/67 extra `report_file`** | 0 non-null | 0 empty/null | **COUNTEREXAMPLE (known)** |
| r54 w1 | 74/74 | exact 5 | exact | 0 non-null | 0 empty/null | OK |
| r55 w1 | 64/64 | exact 5 | exact | 0 non-null | 0 empty/null | OK |
| r56 w1 | 64/64 | exact 5 | exact | 0 non-null | 0 empty/null | OK |
| r57 w1 | 64/64 | exact 5 | exact | 0 non-null | 0 empty/null | OK |
| r58 w1 | 64/64 | exact 5 | exact | 0 non-null | 0 empty/null | OK |

Exact top-level key set on all OK files: `{lane, results, round, seats, wave}`.
No duplicate names, no bad agents, no seats mismatch, no non-str outputs
anywhere.

## Finding 1 (new, adversarial) — r50 `a2w1-results.json` falsifies universal C/D

Every one of the 64 members has `"output": null` and a non-null `"note"` —
e.g. member[0]:
`{"name":"Mo50bExecC1Rerun","agent":"executor","output":null,"note":"orchestrator
kernel restarted mid-wave; seat output was delivered to the orchestrator session
but not retained — read the seat report file in the wave dir"}`.

Consequences:
- "**note** null" and "**output** nonempty" hold on the r54–r58 corpus the C2
  claim pins (`count-c2.py` ARTIFACTS/REAL_SCAN = r54–r58 only, contract line
  69–75) but are **false over rounds 50–58 as a class**. Any entry claim worded
  as "every committed *-results.json" or "note null everywhere" must exclude
  r50 a2w1 (and r53 w1 for key-set claims); the tool's own hedge "`note` free
  (null observed everywhere)" (docstring line 13) is scoped to observed
  artifacts and is not a universal invariant.
- The r50 file still scans `SETTLEMENT_SCAN_OK` under the frozen tool (note is
  free, null output only counted in `empty_output`) — the scan verdict does not
  capture claims C/D. Corroborated: frozen tool over all 10 files reports FAIL
  only for r53 w1 (`member[N]:extra_keys=report_file`), exit 1; r50 a2w1 passes.
## Finding 2 (known/expected) — r53 `w1-results.json` falsifies A-exactness and B

67/67 members carry the extra key `report_file`; top level adds
`{note, outputs_recovered, settled_by→"orchestrator session exit (no seat live)",
spawned}`. This matches the contract's designated drift negative control
(`count-c2.py:76` DRIFT_SCAN; contract lines 78–79: "MUST scan FAIL (`report_file`
extra keys — schema drift, reported not fixed)"). Not a new defect, but it bounds
any "member key set" claim: it is false on 1/5 r50–r53 files.

## Finding 3 (scope note) — r58 `evidence/w1-settlement.json` is a different schema

The sixth C2 artifact is `mori-wave-settlement-v1` census data
(`{ignored_json, lane_root, schema, totals, unreadable_json, waves}`), **not** a
`*-results.json` member file. Member-level predicates (B/C/D) are vacuous on it;
entry claims over this file must quote its actual top-level shape (it would score
`results_not_list`, `seats_mismatch`, `lane/wave/round_bad` if fed to the
scanner — consistent with `count-c2.py` listing it in ARTIFACTS for pinning but
not in REAL_SCAN). Checked anyway; included for completeness only.

## Bounded method (receipts)

- Enumerate: `git ls-tree -r --name-only 60b3a76a | grep -E 'round-5[0-8]/.*results.*\.json$'` → 10 paths (shown above).
- Revision stability: `git rev-parse <enter|freeze|HEAD>:<path>` → all triples `SAME` (blob shas r50 `239fc416`, r51 `5596238f`, r52 `7b994433`, r53a2r1 `ddf30d66`, r53w1 `eb3aa50e`, r54 `52461ffd`, r55 `39562ece`, r56 `12053ae4`, r57 `9507020f`, r58 `9064e531`).
- Extract: `git show 60b3a76a:<path>` → scratch `artifacts/` (10 files, 1.94 MB total).
- Own checker (independent of the tool, mirrors its predicate surface exactly):
  per-file JSON report quoted in the table; counters for extra/missing member
  keys, note_nonnull, output null/empty/non-str, duplicate names, bad agents.
- Corroboration: extracted `tools/mori-settlement-scan.py` at freeze (sha256
  `4c04bf21…5ac9a9` == PIN), ran it over all extracted files: FAIL only on
  r53 w1 (`member[0..66]:extra_keys=report_file`), exit 1; all others OK —
  matching contract lines 77–79 exactly.

## Assessment for the claim

- Claims bounded to the **six pinned artifacts** (r54–r58 w1 + r58 settlement
  for pins only): entry-plausible claims A–D hold; no counterexample.
- Claims stated **universally** over r50–r58 `*-results.json`: falsified by
  `.ufo/waves/round-50/a2w1-results.json` (claims C, D) and
  `.ufo/waves/round-53/w1-results.json` (claims A-exactness, B).
- Residual gap: `note`/`output` are members' fields; r50 shows the orchestrator
  can emit null-output+annotated members on partial settlement. The frozen
  counter's scan arm is insensitive to that class — acceptable (it is the
  designated counting surface) but the entry must not convert it into a
  universality claim.

No production edits, no VCS mutation, no fleet/sibling writes; all evidence from
`git show`/`git rev-parse`/`git ls-tree` at named revisions plus scratch-only
extraction under `/fast/scratch/hyaku/mori-r59/Mo59Reviewer12/` (cleaned after
this report).
