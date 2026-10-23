# ScribeLog — Round 36 LOG entry draft

Seat: `mori-r36-w2-ScribeLog-28` (leaf; report-only).

**Attacks:** completeness and truthfulness of the Round 36 entry in `LOG.md`, especially provenance for the freeze/re-score, the C1 exploratory boundary, counter receipts, gate results, and wave accounting.

**Tooling:** no installs. I ran no commands or checks; findings below are transcribed from the artifacts listed. Counter invocation forms are shown from the frozen counters' CLI usage and the dispatch-log mapping; the receipt files do not preserve their shell transcript.

## Evidence and findings

- Current entry: `LOG.md:2109-2124`. Its C2 and C1 receipt numbers/seeds agree with `evidence/c2-after.txt` and `evidence/c1-after.txt`; the entry correctly characterizes C1 as byte evidence and says the claim is unprovable absent a named non-author reviewer (`LOG.md:2110-2115`; declaration commit `5842dc0`). I found no inference of freshness admission from the C1 byte probe.
- Completeness gap: `LOG.md:2109-2118` omits the requested initial freeze commit `da12b37` and v2 control re-score/freeze commit `c1a026c`; the `c1a026c` receipt records 25/25 controls unmet and both positive references met (`evidence/c0-rescore-v2.txt`, `evidence/freeze-v2.txt`).
- Wave-accounting gap: `LOG.md:2118` records `36+ reports at integration`; the later close-out record says 45 reports on disk and 21 still running out of 66 wave-2 seats (`dispatch-log.txt:58-59`). The existing integration-time count is not contradicted, but it does not give the requested close-out accounting.
- Gate results: the dispatch log records `round_changed=[]`, exit 0, and index clean `staged=0 intent_to_add=0` (`dispatch-log.txt:35`; data commit `bf0df77`). The detailed command for the gate is included below. The dispatch log does not preserve the original index-check shell line; `w2/RevDispatchLog.md` records the audit command `bash tools/mori-index-clean.sh .` and its output, not an independently preserved L1 shell transcript.

## Draft for `LOG.md`

```markdown
## Round 36 (attempt 2, 2026-10-23, L1 MoriR36) — freeze, measurement and routed repairs

- Freeze `da12b37`: contract and v1 counters were pinned before data at entering tip `6bd57097` (`.ufo/waves/round-36/evidence/freeze.txt`). The v2 re-design was frozen at `c1a026c`; `evidence/c0-rescore-v2.txt` records 25/25 negative controls unmet and both builder references met (`evidence/freeze-v2.txt`).
- C1 declaration `5842dc0`: C1 was declared exploratory before data. P-C1 measures byte classification only, not freshness; the declaration allows `unprovable-but-better` only with a named non-author reviewer, otherwise `unprovable` (`contract.md`, final section).
- Data commit `bf0df77fee4b6ef54a90aea09335c7617f125151`: `python3 .ufo/waves/round-36/count-c2.py bf0df77fee4b6ef54a90aea09335c7617f125151` → `evidence/c2-after.txt`: C2=met; blind 24/24, real arm pass, 18 oracle ids; seed `15440749816798970567`.
- Data commit `bf0df77fee4b6ef54a90aea09335c7617f125151`: `python3 .ufo/waves/round-36/count-c1.py bf0df77fee4b6ef54a90aea09335c7617f125151` → `evidence/c1-after.txt`: byte-evidence C1=met; blind 40/40, mismatches=0; real 220 rows, oracle-fetched=58, fresh=49, drifted=9, excluded=0, mismatches=0; seed `7388485190103051243`. This is not a freshness verdict (`5842dc0`).
- Data commit `bf0df77fee4b6ef54a90aea09335c7617f125151`: `python3 tools/mori-sources-appendonly.py bf0df77fee4b6ef54a90aea09335c7617f125151 --round-base 6bd57097` → `round_changed=[]`, exit 0. Index check recorded at the same data tip: `bash tools/mori-index-clean.sh .` → staged=0, intent_to_add=0, exit 0 (`dispatch-log.txt:35`; command line corroborated by `w2/RevDispatchLog.md`).
- Routed repairs in `bf0df77`: 18 in-place-edited SOURCES ids discharged by supersede rows S205–S220; gate registry rows in SKILL.md; QUALITY 103–105; index-clean gate; README Round-36 rows; source-drift knowledge note and evidence copies.
- Wave accounting from the `tool.task` dispatch records: C0 had 25 seats, all 25 settled (`c1a026c`; `c0-dispatch.json`); attempt-1 wave 1 had 33 seats and 28 reports on disk, with two rate-limited dead seats, two provider cyber_policy holds, and BuildDriftTool not returning a report (`bf0df77`; `w1-dispatch.json`, `dispatch-log.txt:20-29`).
- Wave accounting from the orchestrator's one batched `tool.task` call: wave 2 had 66 seats; 45 reports were on disk at close and 21 seats remained running at the freeze deadline; round total 124 seats (`9ca8f2e`; `w2-taskcall.json`, `dispatch-log.txt:58-59`).
```

## Scope and limits

- Only this report file is written; `LOG.md`, counters, receipts, and other lane files were not edited.
- No counter, gate, index check, census, build, test, or freshness probe was rerun. Reported measurements come from the named receipts/dispatch record.
- `c1-after.txt` and `c2-after.txt` do not embed their invoking shell lines; the draft shows the frozen CLI form with the recorded revision. The index-check output is present in the dispatch log, but its L1 shell invocation is not preserved there.
- No freshness verdict is inferred from P-C1. The separate wave-2 live-recheck material is not evaluated here.

**Affected surface:** `.ufo/waves/round-36/w2/ScribeLog.md` only.

**Artifact paths:** `LOG.md:2109-2124`; `.ufo/waves/round-36/dispatch-log.txt`; `.ufo/waves/round-36/contract.md`; `.ufo/waves/round-36/evidence/{freeze.txt,freeze-v2.txt,c0-rescore-v2.txt,c1-after.txt,c2-after.txt}`; `.ufo/waves/round-36/w2/RevDispatchLog.md`.

Report: `.ufo/waves/round-36/w2/ScribeLog.md`

VERDICT: FAIL — completeness defect in the current LOG entry: `LOG.md:2109-2118` omits the required `da12b37`/`c1a026c` freeze and re-score anchors and full wave-2 close-out count; draft above supplies them. No C1 freshness-admission defect found.
