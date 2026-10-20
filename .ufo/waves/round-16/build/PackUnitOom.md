# PackUnitOom — .ufo/waves/round-16/fixtures/UnitOom.json

## Files changed
- `.ufo/waves/round-16/fixtures/UnitOom.json` (new, 5315 bytes, 4 cases)
- `.ufo/waves/round-16/build/PackUnitOom.md` (this report)

## Authority check: topic-id hint was WRONG
- Lane hint claimed unit-failure id `d9b373ed55a64e6c8e2e7d70a0fce472` ("hints not authority").
- Verified source bytes in `tools/mori-census.sh`: line 1036
  `JOURNAL_ID_UNIT_FAILURE=d9b373ed55a64feb8242e02dbe79a49c` and stub routing
  `MESSAGE_ID=d9b373ed*` -> `unit_failure` (line 2811). The hint id appears
  nowhere in the file. **Pack uses `d9b373ed55a64feb8242e02dbe79a49c` throughout.**
- r15 positive predicate verified at line 1055 (`JOURNAL_JQ_POS_UNIT`) and the `oom` def
  at line 1095: `positive_unit_oom` requires `UNIT_RESULT` to be exactly the STRING
  `"oom-kill"` — case-sensitive `==`, non-string never counts.

## Cases (all shared schema, rc0 / MORI_JOURNAL_WINDOW_OK)
| id | scope | records after anchor | positive_unit_oom |
|---|---|---|---|
| `unitoom_exact_result_counts_user` | user | 1 | 1 |
| `unitoom_wrong_case_variants_zero_system` | system | 3 (`OOM-KILL`, `Oom-Kill`, `oom-KILL`) | 0 |
| `unitoom_mixed_exact_and_wrongcase_user` | user | 2 (`OOM-kill` + `oom-kill`) | 1 |
| `unitoom_wrongcase_absent_other_result_zero_system` | system | 3 (`Oom-kill`, absent UNIT_RESULT, `resources`) | 0 |

Every `want` pins all four positive tokens (non-target = 0), `records_after_anchor`,
`scope`, and `evidence_basis=validated-record-subsets`.

## Deliberate trap worth noting for WindowTool/WindowHarness
- The anchor record in every case carries `UNIT_RESULT:"oom-kill"` itself. If the tool
  fails to drop the first parsed record (or fails to match it by exact `__CURSOR` +
  `_BOOT_ID`), positives are inflated by 1 and every case fails — the pack doubles as an
  anchor-drop check.
- Cursors are unique printable scalars (`s=r16u;i=9f;n=NNN;x=HHHH`); all `_BOOT_ID`
  values are 32 lowercase hex and equal the anchor `boot_id`.
- Records carry only the contracted output fields (`__CURSOR,_BOOT_ID,MESSAGE_ID,
  UNIT_RESULT` + client-supplied `UNIT`/`USER_UNIT`); no `MESSAGE`, no `EXIT_CODE`/
  `EXIT_STATUS` (unit-failure records; sigkill predicate untouched).
- Case 4 overlaps TypedFields/RecordShape adjacent ground only mildly (absent field,
  `resources`) — included to pin that a non-string/absent UNIT_RESULT yields a real 0,
  not omission.

## Schema assumptions (coordinate exact-id questions to WindowHarness)
- `want` treated as the selected-fields subset the harness asserts; `want_rc`/`want_id`
  drive rc + finding-id assertions. `timeout`/`overflow` optional keys omitted here
  (all cases are finite successes per pack topic).
- `anchor.scope` equals case `scope`; `anchor.cursor` == first stdout record's
  `__CURSOR` byte-for-byte.

## Evidence retained
- `grep` of tools/mori-census.sh:1032-1036, 1055, 1095-1096, 2811 (ids, predicates).
- Round-15 sibling packs (UnitUser.json, NegativeResults.json) read for id/field shapes;
  r16 case schema taken from the wave contract (no prior r16 fixture existed to reuse).
- Pack self-validated post-write: JSON round-trip, unique case ids, unique cursors,
  first-record cursor+boot match, all `_BOOT_ID` equal anchor, all UNIT_RESULT strings.

## Risks / blockers
- If the r16 tool classifies positives by a different key than `MESSAGE_ID`+exact
  `UNIT_RESULT=="oom-kill"`, wants 0/1 may need re-alignment — predicates were copied
  from r15 production jq verbatim per the contract ("using r15 predicates").
- No runs performed (leaf rule); WindowTool/WindowHarness own execution. No installs.
