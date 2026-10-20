# PackProducerFailure — round 16 advisory report

## Files changed
- `.ufo/waves/round-16/fixtures/ProducerFailure.json` (created; sole owned file, 4 cases, all refusal cases specific to producer-exit-code topic)

## Behavior (fixture intent, not executed — no runs per contract)
Every case: producer exits nonzero while its stdout is a structurally valid
JSONL window stream. Expected tool result is always `want_rc=2`,
`want_id=MORI_JOURNAL_WINDOW_UNAVAILABLE` — a nonzero producer rc invalidates the
whole capture regardless of how valid-looking the emitted records are, and no
positive counts may surface. `want` is left `{}` because the shared schema names
only `want_rc`/`want_id` as stable for unavailable results; a reason-string
vocabulary is not yet published by the harness (asked WindowHarness whether a
stable reason assertion exists — will amend if one is defined).

- Compliance disclosure (L1 r16 clarification): zero live journalctl queries,
  measurement/probe loops, background jobs, tests, gates, builds, or smoke runs.
  The only self-check was an in-process `json.loads` parse of the fixture bytes
  this seat authored (pure static syntax/structure validation of my own file —
  no subprocess spawn, no tool execution, no /tmp output, no outside-lane write).

| id | scope | returncode | stream shape |
|---|---|---|---|
| producer-rc5-positive-stream | user | 5 | anchor record + kernel-oom `fe6faa94…` + unit-failure `d9b373ed…`/`UNIT_RESULT=oom-kill` |
| producer-rc124-positive-stream | system | 124 | anchor + kernel-oom + sigkill `98e32220…`/`EXIT_CODE=killed`/`EXIT_STATUS="9"` + unit-failure `signal` (covers 3 of 4 positive predicates) |
| producer-rc137-positive-stream | user | 137 | anchor + sigkill record with `EXIT_STATUS` as JSON number `9` (r15 predicate accepts numeric 9) |
| producer-rc5-anchor-only | system | 5 | anchor record only — the refusal boundary: even a window that would succeed (records_after_anchor=0) must refuse on nonzero rc |

Distinctness: three different nonzero codes (5, 124, 137 — real journald error
class, timeout-kill-shaped, SIGKILL-shaped), both scopes, string-vs-numeric
`EXIT_STATUS`, all four positive predicate classes represented across the pack,
and one anchor-only boundary refusal.

## Evidence basis
- Catalog ids byte-verified against `tools/mori-census.sh` constants (lines 1032–1036):
  kernel-oom `fe6faa94e7774663a0da52717891d8ef`, oomd `d989611b15e44c9dbf31e3c81256e4ed`,
  coredump `fc2e22bc6ee647b6b90729ab34a250b1`, unit-sigkill `98e322203f7a4ed290d09fe03c09fe15`,
  unit-failure `d9b373ed55a64feb8242e02dbe79a49c`.
- Positive predicates from r15 jq filters (lines 1052–1055): exact string
  `MESSAGE_ID`, `UNIT_RESULT` exact `"oom-kill"`/`"signal"`, `EXIT_CODE=="killed"`
  with `EXIT_STATUS` string `"9"` or number `9`.
- Cursor strings use real journald cursor shape (`s=…;i=…;b=…;m=…;t=…;x=…`) but
  are synthetic and distinct per case; anchor cursor appears as `__CURSOR` of the
  first stream record, all later cursors unique scalars, same-boot `_BOOT_ID` per case.
- JSONL streams are literal escaped strings per the pack schema; `stderr` is
  empty in every case so the nonzero rc is the sole refusal trigger (stderr
  contamination is PackStderr's topic).

## Schema finding for the wave
- The wave1 spec's hint ID for unit-failure (`d9b373ed55a64e6c8e2e7d70a0fce472`)
  appears nowhere in census source; the real catalog id is
  `d9b373ed55a64feb8242e02dbe79a49c`. Notified PackUnitOom by message; used the
  census-verified value here per "hints not authority".

## Risks / open items
- If WindowHarness defines a stable `reason` vocabulary or requires `scope` in
  rc2 output, `want:{}` should gain those fields; pending their answer.
- No execution: fixture never run through a harness or tool (per contract);
  self-check was a pure JSON parse asserting cursor uniqueness, anchor-first
  ordering, and boot-id consistency.
- No installs or updates performed.
