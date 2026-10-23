# ScribeScorecard — round-36 scorecard draft

**Item attacked:** accuracy of the proposed round-36 move-log entries, C2 capability row, and round-37 Planned row. Axes: C2 operability; C1 exploratory freshness technique (not freshness admission); evidence traceability; planning scope.

## Provenance and boundaries

Source basis: the frozen claim contract `.ufo/waves/round-36/contract.md`, receipts `evidence/c2-after.txt` and `evidence/c1-after.txt`, and L1's round-36 measurement record in `dispatch-log.txt:30-35`. The requested measurement tip is `bf0df77fee4b6ef54a90aea09335c7617f125151`; entering tip is `6bd57097`.

The commands and outputs below are transcribed from those records, not rerun by this scribe. No tools were installed. No lane product file, judge, or SCORECARD was edited; the only file written is this report. The draft is for L1 to land or revise.

## Proposed SCORECARD move-log rows

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 36 | operability | `python3 .ufo/waves/round-36/count-c2.py 6bd57097` → `tool_absent C2=unmet`, exit 1 (`evidence/c2-before.txt`) | `python3 .ufo/waves/round-36/count-c2.py bf0df77fee4b6ef54a90aea09335c7617f125151` → blind 24/24, real arm pass, `C2=met`, seed `15440749816798970567` (`evidence/c2-after.txt`). Gate check: `python3 tools/mori-sources-appendonly.py bf0df77fee4b6ef54a90aea09335c7617f125151 --round-base 6bd57097` → `round_changed=[]`, exit 0. | `evidence/c2-before.txt`, `evidence/c2-after.txt`; gate command above |
| 36 | freshness technique — C1 exploratory; no freshness verdict admitted | `python3 .ufo/waves/round-36/count-c1.py 6bd57097` → tool absent, `C1=unmet`, exit 1 (`evidence/c1-before.txt`) | `python3 .ufo/waves/round-36/count-c1.py bf0df77fee4b6ef54a90aea09335c7617f125151` → blind 40/40, mismatches=0; real rows=220, oracle-fetched=58, fresh=49, drifted=9, excluded=0, mismatches=0; `C1=met` as byte-behavior evidence, seed `7388485190103051243` (`evidence/c1-after.txt`). **Claim disposition: unprovable** absent a named non-author reviewer; this result is not freshness admission. | `evidence/c1-before.txt`, `evidence/c1-after.txt`; exploratory rule `.ufo/waves/round-36/contract.md:119-131` |

**Receipt/output distinction:** `c2-after.txt` records the historical gate tool's output with 18 existing immutable-cell violations and `tool exit=1`, while the frozen counter reports `C2=met` because tool and oracle agree. `c1-after.txt` records the probe's `tool_exit=1` for nine `drifted` rows while the frozen counter reports `C1=met` because the probe matches its byte-classification oracle. Neither counter token licenses interpreting C1 as a freshness verdict.

## Proposed capabilities-register row

| key | name | what it can now do | evidence | first working |
|---|---|---|---|---|
| round-36 C2 | sources append-only gate with deleted-row detection | Flags in-place immutable-cell edits, deleted rows, superseders, and per-round changed ids of `corpus/SOURCES.md`. | `evidence/c2-after.txt` (the `count-c2.py` receipt above); `python3 tools/mori-sources-appendonly.py bf0df77fee4b6ef54a90aea09335c7617f125151 --round-base 6bd57097` → `round_changed=[]`, exit 0. | 36 |

No C1 capability row is proposed: the task's exploratory disposition is `unprovable` without the required named non-author reviewer. Keep the byte evidence in C1's move-log row only.

## Proposed Planned row

**Planned round 37:** (1) address disclosed counter residuals by redesigning the timeout path to avoid SIGKILL of the sandbox child (requires a counter re-freeze and a new claim), and re-score C2 with a fixture exercising `oracle_excluded>0`; (2) pursue the C1 follow-on by comparing like representations and binding the witness to the taught claim; (3) make one claim on a remaining lowest axis (depth or calibration) with a counter that fails content-free controls.

This is a proposed plan, not a measurement or a claim that round 37 has started.

## Findings and limits

- The proposed rows preserve the distinction between C2's measured operability result and C1's byte-behavior receipt versus claim verdict.
- No score increase is proposed: the evidence supports capability acquisition/technique progress, not a numeric axis-score change.
- Out of scope: independently rerunning counters, auditing the entire scorecard, determining closure admission, or changing lane files.
- Artifact written: `.ufo/waves/round-36/w2/ScribeScorecard.md` only.

**VERDICT: PASS** — no defect found in this scoped draft; C1 is explicitly unprovable absent a named non-author reviewer, and its byte result is not presented as freshness admission.
