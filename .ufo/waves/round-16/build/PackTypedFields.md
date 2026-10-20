# PackTypedFields — round16 TypedFields fixture pack

## Files changed
- `.ufo/waves/round-16/fixtures/TypedFields.json` (new, 4 cases)

## Cases
All cases share the schema from the wave1 fixture contract: `anchor`
(`mori-journal-anchor-v1`, matching `scope`, `boot_id` = 32×"a",
`cursor` = "anchor"), literal JSONL `stdout` whose first record echoes the
anchor cursor+boot and is dropped, empty `stderr`, `returncode` 0.

1. `typedfields_msgid_array_sigkill` (user): record carries
   `MESSAGE_ID:["98e322203f7a4ed290d09fe03c09fe15"]` (array), `EXIT_CODE:"killed"`,
   `EXIT_STATUS:"9"`. Expect rc0 `MORI_JOURNAL_WINDOW_OK`,
   `records_after_anchor=1`, all four `positive_*` = 0 — a non-scalar
   `MESSAGE_ID` cannot satisfy any r15 predicate but does not break record
   shape (object, same boot, unique scalar `__CURSOR`).
2. `typedfields_msgid_array_unit_oom` (system): `MESSAGE_ID` array containing
   the unit-failure id `d9b373ed55a64feb8242e02dbe79a49c`, `UNIT_RESULT:"oom-kill"`.
   Expect rc0, `records_after_anchor=1`, `positive_unit_oom=0`, all others 0.
3. `typedfields_exit_status_bool_true` (user): correct scalar
   `MESSAGE_ID:"98e322203f7a4ed290d09fe03c09fe15"`, `EXIT_CODE:"killed"`,
   `EXIT_STATUS:true` (boolean). Expect rc0, `records_after_anchor=1`,
   `positive_process_sigkill=0` — r15 predicate accepts only string `"9"` or
   number `9`; bool/array/null/other rejected (mori-census.sh:981-984, 1054).
4. `typedfields_bool_status_mixed_valid` (user): `EXIT_STATUS:false` sigkill
   record followed by a fully valid positive sigkill record
   (`EXIT_STATUS:"9"`). Expect rc0, `records_after_anchor=2`,
   `positive_process_sigkill=1`, others 0 — non-scalar sibling does not poison
   a valid positive and is never itself positive.

## Evidence retained
- Catalog ids verified byte-exact against `tools/mori-census.sh`:
  `JOURNAL_ID_UNIT_SIGKILL=98e322203f7a4ed290d09fe03c09fe15` (:1035),
  `JOURNAL_ID_UNIT_FAILURE=d9b373ed55a64feb8242e02dbe79a49c` (:1036),
  class/predicate semantics :909-920, :976-984, :1052-1055.
- Pack parses as JSON; every `stdout` line parses as a JSON object
  (verified with python3 json.loads, syntax check only — no tool run).
- Every case asserts `want_rc=0`, `want_id=MORI_JOURNAL_WINDOW_OK`, plus
  `scope`, `records_after_anchor`, and all four `positive_*` want fields —
  four topic-specific successes, no refusals.

## L1-compliance disclosure (post-clarification)
- No live journalctl/systemd queries, no measurement/probe loops, no
  background jobs, no tests/gates/builds/smoke/formatters, no outside-lane
  writes, no /tmp output, no commits.
- Sole command execution: `python3 -c json.loads` over each `stdout` line of
  the fixture file just written — a syntax well-formedness check of this
  lane's own artifact only. Not verification of any production tool and not
  claimed as such; disclosed to MoriR16 and MoriR16.Lesson.

## Interpretation note (coordinated by exact id WindowHarness if disputed)
Typed-field records are kept inside the window (rc0, counted in
`records_after_anchor`) rather than invalidating the capture: the interface's
record-validity rule is "object + same boot + unique valid scalar cursor";
type-strict field predicates govern only the positive counts, matching the
r15 census model where a record with non-scalar `MESSAGE_ID`/`EXIT_STATUS`
fails the per-record positive test without fabricating a malformed-capture
unavailability. If WindowHarness defines `want` as a subset match, the listed
fields are the intended assertions; `reason` is absent on rc0 by contract.

## Risks / blockers
- If the tool author instead treats a non-scalar `MESSAGE_ID` as
  malformed-capture (rc2), cases 1–3 flip to `MORI_JOURNAL_WINDOW_UNAVAILABLE`;
  flagged here so the WindowTool lane and harness can settle the contract.
- No execution performed (per contract); pack digest not yet pinned —
  harness `--pin-fixtures` step is the owner's post-integration gate.
- No installs performed; no tools needed beyond python3 stdlib for syntax check.
