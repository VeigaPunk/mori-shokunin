# Judge05 — non-author judge: case `r29-a2-10-unbounded-missing-stamp-alone`

Role: non-author judge (amendment A2 of the round-28 contract carried into round-29 C2 'Mismatch judging').
Read only: round-27 contract `:40-80`, round-26 contract (whole spec incl. amendment A2 and output spec),
the case object in `cases-a2-r29.json`, and `r29-a2-10-unbounded-missing-stamp-alone.base.json` /
`.fix.json`. Did NOT read the tool source, the fix diff, other reports, or the lessons.

## Case summary

- Inputs (`tools/fixtures/mori-oom-killers/cases-a2-r29.json:700-713`): `earlyoom_show` has
  `ActiveState=active` but NO `ActiveEnterTimestampMonotonic`; journal has two records: version line
  `earlyoom 1.9.0` with `__MONOTONIC_TIMESTAMP=73100000`, and send line
  `sending SIGTERM to process 4101 "fictional-orchid"` with NO `__MONOTONIC_TIMESTAMP`; `oomd_notices=0`.
- `why` (`cases-a2-r29.json:699`): A2-10 leaves the unstamped send uncounted and the scope incomplete;
  A2-05 leaves the invocation unbounded (missing stamp) so scope incomplete; no counted positive evidence →
  `KILLERS_UNKNOWN`/exit 2.

## Field-by-field comparison (expect vs base vs fix)

| field | expected | base | fix | ruling | contract line |
|---|---|---|---|---|---|
| verdict | KILLERS_UNKNOWN | KILLER_ACTED | KILLERS_UNKNOWN | tool error | round-26:186-188; round-26:98-101; round-27:58 |
| exit | 2 | 1 | 2 | tool error | round-26:96-99 |
| earlyoom.state | active | active | active | match | — |
| earlyoom.version | 1.9.0 | 1.9.0 | 1.9.0 | match | — |
| earlyoom.grammar | verified-1.9.0 | verified-1.9.0 | verified-1.9.0 | match | — |
| earlyoom.scope_complete | false | false | false | match | — |
| earlyoom.actions.sigterm | 0 | 1 | 0 | tool error | round-26:186-188; round-27:58 |
| earlyoom.actions.sigkill | 0 | 0 | 0 | match | — |
| earlyoom.actions.escalations | 0 | 0 | 0 | match | — |
| earlyoom.actions.kill_failed | 0 | 0 | 0 | match | — |
| earlyoom.actions.low_memory_warnings | 0 | 0 | 0 | match | — |
| earlyoom.process_group_lines | 0 | 0 | 0 | match | — |
| earlyoom.earlier_invocation_send_lines | 0 | 0 | 0 | match | — |
| earlyoom.dryrun | false | false | false | match | — |
| earlyoom.dryrun_send_lines | 0 | 0 | 0 | match | — |
| oomd.state | inactive | inactive | inactive | match | — |
| oomd.notices_this_boot | 0 | 0 | 0 | match | — |

## Rulings (the three expect/base mismatch fields)

1. `earlyoom.actions.sigterm` (expected 0, base 1) — **TOOL ERROR**. Contract line:
   `.ufo/waves/round-26/contract.md:186-188`: "a journal record without a numeric `__MONOTONIC_TIMESTAMP`
   is now left uncounted and makes the scope incomplete, instead of a setup error". The only send record has no
   numeric stamp, so it is uncounted; `sigterm` is pinned 0 (also `cases-a2-r29.json` rule A2-10 at
   `.ufo/waves/round-27/contract.md:58`). Base counting it as `sigterm=1` contradicts the rule.
2. `verdict` (expected KILLERS_UNKNOWN, base KILLER_ACTED) — **TOOL ERROR**. Contract line:
   `.ufo/waves/round-26/contract.md:98-101`: "KILLERS_UNKNOWN, exit 2: no positive evidence, and any of: …
   earlyoom active but `scope_complete` false …". With the send uncounted there is no positive evidence
   (`oomd_notices=0`), and `scope_complete=false` holds both via A2-10 (unstamped record) and via A2-05
   (missing `ActiveEnterTimestampMonotonic`, `.ufo/waves/round-27/contract.md:53`,
   `.ufo/waves/round-26/contract.md:173-174`). Base's KILLER_ACTED contradicts.
3. `exit` (expected 2, base 1) — **TOOL ERROR**. Contract line: `.ufo/waves/round-26/contract.md:96-102`
   verdict↔exit mapping: `KILLERS_UNKNOWN` exits 2, `KILLER_ACTED` exits 1. Base exit 1 pairs with the wrong
   (ruled-above) verdict.

## Fix check

- FIX matches every case field (all rows in the table: verdict, exit, and each `expect.fields` path).
- FIX changed exactly the three mismatched fields: `sigterm` 1→0, `verdict` KILLER_ACTED→KILLERS_UNKNOWN,
  `exit` 1→2. Each change is now correct under the rule text (quotes in Rulings above); no field the fix
  changed is wrong under the rule text.

case_ruling=tool error
