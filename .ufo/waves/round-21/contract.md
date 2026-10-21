# Round21 repair contract

Entering branch tip e9f340ce986f82a60baad1b8e5ead655ab818a1c. L1 MoriR21 holds planner/integration. Round20 was rejected-harmed: freshness and calibration harmed, coverage improved. Current MANIFEST has the mori closure at entry405 (operator steer said404); its ruling, not the index, governs. No new pin is permitted this round. r10 and r20 baseline bytes and historical registers remain unchanged.

## Claims (two causally separable claims)

C1 freshness (lowest score tie5): repair disappearance evidence loss by retaining the identities aggregator-r10 and aggregator-r10-resume as explicit unresolved historical observations, with baseline/deletion/cleanup provenance, and operationally blocking baseline acceptance while disposition is unknown. Before:2 historical required wave observations absent from a retained loss register; after:0 omitted,2 unresolved remain visible. This is evidence assurance repair, not proof of settlement. Count from committed snapshots with the same new evaluator on before and after. All historical evidence remains append-only. New capability missing at entering revision is separately labelled, never historical production bugs.

C2 calibration (lowest tie5): supersede QUALITY67's universal cause-only permission with an operational evidence-loss-first classification rule. Before: cause-only live-state rule permits lost required evidence; after: missing required evidence implies census-regression/pin blocked unless independently evidenced per-wave disposition exists. Known safe state changes remain live-state. Same evaluator must actually read the old/new rule objects; it may not presume failure from phase. Count mismatched decisions against an independent frozen expectation table. Retain the old criterion unchanged, append explicit supersession and correct active instructions/index/scorecard/province prose by appended errata. No health, completeness, independent closure or promotion assertion.

## Shared data interface

New stdlib CLI tools/mori-evidence-loss.py:
`audit --required FILE --accounting FILE`: required schema mori-required-observations-v1 with observations [{id,baseline,evidence}]. accounting schema mori-loss-accounting-v1 with observations [{id,state,baseline,deletion,cleanup,independent_disposition}]. Each provenance field is an object {path,revision,sha256} pointing to a committed own-lane evidence copy (relative paths, SHA256 bytes); baseline/deletion/cleanup must be present for retained rows. state unresolved permits independent_disposition:null and blocks pin. state disposed requires independent_disposition object with path/revision/sha256 and independent:true, distinct actor from cleanup, explicit wave id and disposition settlement|cleanup-accounted. Unknown/missing/malformed/stale evidence never resolves a row. Tool validates hashes of files beneath --root (required argument), rejects absolute/.. or symlink path components. No report text emitted. Output stable JSON schema mori-evidence-loss-audit-v1 with omitted,retained,unresolved,disposed,invalid,pin_allowed and issues. rc0 only complete valid accounting and zero unresolved; rc1 expected blocker or omission; rc2 setup/input failure. A complete unresolved accounting is an observability improvement despite deliberate rc1.
`classify --rule FILE --cases FILE`: rule schema mori-evidence-loss-rule-v1 {evidence_loss_blocks:boolean}; cases schema mori-evidence-loss-cases-v1 cases [{id,required_evidence_lost:boolean,independent_disposition:boolean,ordinary_state_change:boolean,expected_class,expected_pin_allowed}]. Rule true: lost and not independently disposed -> census-regression,false; otherwise live-state,true. Rule false reproduces Q67 cause-only permission, always live-state,true. Emit per-case observed decisions, mismatched count, matched; rc0 all match,1 mismatch,2 setup. Historical Q67 is interpreted narrowly via explicit before-rule object citing Q67, not claimed to have had code.
--selftest builds isolated fixtures and asserts rc plus stable finding_id, tests absent/tampered/duplicate/unsafe evidence, unknown disposition, and both rules. No live writes, no network.

## Frozen rule cases

loss-unknown:true,false,true => census-regression,false
loss-cleanup-only:true,false,false => census-regression,false
loss-independent-cleanup:true,true,false => live-state,true
loss-independent-settlement:true,true,true => live-state,true
ordinary-aging:false,false,true => live-state,true
ordinary-state:false,false,false => live-state,true

The source lesson must cite reopened S066 (ApprovalTests README approval decision, not authority for mori's policy); open S072 reject again for outside sample if needed. Frontier FR3 remains authoritative lifecycle unknown: only retained historical accounting grows, no settled disposition fabricated. QUALITY64/65/66/68 routed defects are disclosed; fix only defects necessary for these two claims, else explicitly retain debt. Wave1 64 substantive tasks, wave2 only if64 distinct remaining attack items. No padded wave.
