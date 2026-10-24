measured 2026-10-23T09:13:40Z

# Wave-2 falsification — register row for mori round 14, key `rounds[339].capabilities_added[0]`

Seat MoriR35.JudgeRowsR14 (non-author reviewer; leaf, no subagents, no background jobs). Landed tip judged: lane commit cedb0ec4f3a4f672804deac388b7191258f01fcd (SCORECARD read via `git show` at that rev, not the working tree). Closure record: fleet MANIFEST.json rounds[339] at 37b51a24; fleet report .ufo/reports/round-14/mori.md at 37b51a24; spot-check corpus/lessons/round-14-verifier-spotcheck.md at lane 0fa5e0de194bcc270a927a166664113e6821442b. No tools installed or updated; no writes outside this report.

## Row under test

Exactly one row in the final `## Capabilities` section of SCORECARD.md@cedb0ec4 carries a rounds[339] key (section spans :1941-1978; the rounds[339] row is :1962; no duplicate key exists). Cells, abbreviated without table pipes:

- key: `rounds[339].capabilities_added[0]`
- capability: `typed journal alarm and subject triage`
- what it can now do: Classifies structured failed-unit subjects as fleet, tsukuroi-routed or unresolved and raises one critical OOM journal alarm; the six named fixture failures went 6 to 0; no live-positive or exhaustive coverage proof.
- evidence: `tools/mori-round14-regressions.py`
- first-working round: 14

MANIFEST.json rounds[339] at 37b51a24: lane_round 14, admitted true, capabilities_added has exactly one entry, `typed journal alarm and subject triage`, verification.spotcheck points at the spot-check above, commit mori-shokunin@0fa5e0de194bcc270a927a166664113e6821442b.

## (a) Closure faithfulness, sentence by sentence

Capability cell: equals the MANIFEST rounds[339].capabilities_added[0] string verbatim. Non-empty. First-working round 14 matches rounds[339].round/lane_round 14. [MET]

What-cell sentence 1 — Classifies structured failed-unit subjects as fleet, tsukuroi-routed or unresolved and raises one critical OOM journal alarm.
- The closure's bounded claim is to 'restore structured OOM critical/DRIFT, fleet/non-fleet subject partition and tsukuroi triage' (spot-check :8). The classifier 'separates fleet/non-fleet/unattributed findings' and 'emits one global critical OOM line' (spot-check :54, citing tools/mori-census.sh:1267-1290 and :1293-1331 at the closure bytes).
- Fleet report :9 (37b51a24): partition uses exactly one valid UNIT or USER_UNIT; non-fleet output names owner=tsukuroi; 'ambiguous/missing/malformed subjects are separately unattributed with `owner=unresolved`'. Fleet/tsukuroi-routed/unresolved is exactly the record's three-way outcome. [MET]
- Alarm: report :8, 'Restored exactly one global `OOM_KILL_JOURNAL severity=crit`'; gate docstring tools/mori-round14-regressions.py:24-26,66 at 0fa5e0de. 'Structured' is the record's own adjective (typed UNIT/USER_UNIT plane, report :5). [MET]

What-cell sentence 2 — the six named fixture failures went 6 to 0.
- MANIFEST rounds[339].verification.rechecks: 'Independently recounted six named strict acceptance failures [6,0]'; report :43-44 shows the same counting command and output, report :77 six named acceptance failures 6 to 0; spot-check :34 [6, 0]. The six ids are named in both the report's jq filter and the gate registry (R14_OOM_ALARM_USER, R14_OOM_ALARM_SYSTEM, R14_UNIT_OOM_KILL, R14_UNIT_FAILED_FLEET, R14_UNIT_FAILED_NONFLEET, R14_UNIT_SIGNAL_WARN; gate :24-42).
- I re-parsed the committed receipts at 0fa5e0de myself: red-before-accepted/evidence.json has status counts fail=43 with all six named ids failing; green-after-accepted/evidence.json has pass=44 fail=0 with zero of the six failing. 6 to 0 is what the record and the artifact both show. [MET]
- The fixture bound is kept: 'nonzero synthetic fixture observations, not live load' (spot-check :50); report :53 labels the vectors fixture. The cell says fixture failures, not live or production-defect counts. [MET]

What-cell sentence 3 — no live-positive or exhaustive coverage proof.
- Spot-check :8: 'does not admit exhaustive old-MESSAGE equivalence, authenticated membership, unique-victim counts, positive-load live behavior or comprehensive OOM coverage'. Spot-check :52: the live bracket was 12/12 all zero and 'cannot prove positive-load alarms, unique victims or fleet causation'. Report :56 and :86 state the same limits. The cell's disclaimer is bounded exactly as the record bounds it. [MET]

No fact in the what-cell is absent from the record, and none exceeds the record's bounds. (a) met.

## (b) Evidence-cell form

SCORECARD.md:1962 evidence cell contains exactly one backticked path, `tools/mori-round14-regressions.py`, and no other content. The path exists at the closure commit (2476 lines via `git show 0fa5e0de...:tools/mori-round14-regressions.py`) and at the judged tip (2800 lines). Only backticked paths. [MET]

## (c) Pointer relevance (outside the rule)

Opened tools/mori-round14-regressions.py at 0fa5e0de. Its docstring and registry cover precisely this capability, not a sibling one: the six named acceptance arms (:24 R14_OOM_ALARM_USER, :25 R14_OOM_ALARM_SYSTEM, :26 R14_UNIT_OOM_KILL, :31 R14_UNIT_FAILED_FLEET, :32 R14_UNIT_FAILED_NONFLEET, :42 R14_UNIT_SIGNAL_WARN), the three-way subject outcomes (:31 fleet owner=mori, :32 nonfleet owner=tsukuroi, :33 and :37 unattributed for emitter-only and ambiguous subjects), the single-global-alarm rule (:66 OOM: exactly ONE global FINDING OOM_KILL_JOURNAL severity=crit per census), and never-summed scoped counters (:45-46). This is the gate whose committed red/green receipts the report cites as the C1 measurement (report :39-44) and whose r14 selftest the spot-check verified as committed evidence (spot-check receipt table). It implements and demonstrates the typed journal alarm and subject triage capability. [DEMONSTRATES THIS CAPABILITY]

## Verdicts

VERDICT: rounds[339].capabilities_added[0] supported
VERDICT: rounds[339].capabilities_added[0] pointer-relevance holds

## Residual risk and verification gaps

- Behavioral re-execution: I re-parsed committed receipt JSON but did not re-run the census or the gate; the 6-to-0 figure is verified against the record and the committed receipts, not fresh behavior. This matches the spot-check's own stance (committed-evidence verification).
- The what-cell's first sentence states the capability in general form; its fixture-only and non-exhaustive bounds ride on sentences 2-3. The record states the restore at bounded scope (spot-check :8), so I read this as faithful compression, not overclaim.
- Evidence path resolves at both closure commit and tip, but the register binds evidence to the artifact the round landed; I checked existence and subject matter at 0fa5e0de, not byte identity across later revisions.
- Other register rows (keys rounds[313], [345], [353], [386], [398], [427], [443], [455], [462], [476], [495]) are out of scope for this seat.
