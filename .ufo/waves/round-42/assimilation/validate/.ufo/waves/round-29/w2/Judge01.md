# Judge01 — `r29-a2-07-dryrun-inside-scope` (rule A2-07)

Seat: `MoriR29.Judge01`, non-author judge for round-29 C2 mismatch judging.
Read only: `.ufo/waves/round-27/contract.md:40-80`, `.ufo/waves/round-26/contract.md`
(whole, incl. amendment A2 at :152-190), the case object in
`tools/fixtures/mori-oom-killers/cases-a2-r29.json` (id `r29-a2-07-dryrun-inside-scope`),
and the two outputs `…/L1/judge/r29-a2-07-dryrun-inside-scope.{base,fix}.json`.
Tool source, fix diff, other reports and lessons were not read.

## Input shape (case `inputs`)

- `earlyoom_show`: `ActiveState=active`, `ActiveEnterTimestampMonotonic=3000` → the
  scope is journal lines with `__MONOTONIC_TIMESTAMP` ≥ 3000 (round-26
  `contract.md:78-79`: "earlyoom lines whose `__MONOTONIC_TIMESTAMP` ≥
  `ActiveEnterTimestampMonotonic` of the current earlyoom invocation, in the
  current boot").
- Journal records (ts → MESSAGE):
  - 1000 `earlyoom 1.9.0`, 1100 `sending SIGTERM to process …` — invocation 1,
    send line outside the current invocation.
  - 3500 `earlyoom 1.9.0`, 3600 `dryrun mode enabled, will not kill anything` —
    invocation 2, a dry-run invocation.
  - 4000 `earlyoom 1.9.0` — a new version line splits invocation 3 here
    (round-26 `contract.md:82`: "`earlyoom <version>` → version (the first line
    of an invocation)").
  - 4100 `sending SIGKILL to process …` — a real send inside invocation 3,
    in scope.
- `oomd_show` `ActiveState=inactive`; `oomd_notices: 0`.

## Deciding rule text

- A2-07, round-27 `contract.md:55`: "dry-run applies per invocation (split at
  each version line): one dry-run invocation does not zero another invocation's
  real sends". Same rule as adopted, round-26 `contract.md:180-181`.
- Round-26 `contract.md:166-167` (A6): dry-run suppression holds only "when the
  invocation logged `dryrun mode enabled`" — invocation 3 (from ts 4000) did not.
- Round-26 `contract.md:85`: "`sending SIGTERM to process ` / `sending SIGKILL to
  process ` → one action each" → the 4100 line is `sigkill` 1.
- Round-26 `contract.md:97-98`: "`KILLER_ACTED`, exit 1: any earlyoom `sending
  SIG…to process` or escalation line in scope".
- Round-26 `contract.md:175-176`: `earlier_invocation_send_lines` counts send and
  escalation lines of this boot outside the current invocation → the 1100 SIGTERM
  is 1. For an active earlyoom it is "reported but does not change the verdict"
  (:178-179), so the verdict here rests on the in-scope SIGKILL alone.
- Round-26 `contract.md:93`: `scope_complete` true — the current invocation's
  version line (4000) is inside the scope.

## Ruling table (expect vs base vs fix)

| field | expected | base | fix | ruling | contract line |
|---|---|---|---|---|---|
| verdict | KILLER_ACTED | KILLERS_QUIET | KILLER_ACTED | tool error | r26:97-98; r27:55 |
| exit | 1 | 0 | 1 | tool error | r26:97 |
| earlyoom.state | active | active | active | (base agrees) | r26:90-92, 162-163 |
| earlyoom.version | 1.9.0 | 1.9.0 | 1.9.0 | (base agrees) | r26:82 |
| earlyoom.grammar | verified-1.9.0 | verified-1.9.0 | verified-1.9.0 | (base agrees) | r26:92 |
| earlyoom.scope_complete | true | true | true | (base agrees) | r26:93 |
| earlyoom.actions.sigterm | 0 | 0 | 0 | (base agrees) | r26:85, 175-176 |
| earlyoom.actions.sigkill | 1 | 0 | 1 | tool error | r26:85; r27:55; r26:180-181 |
| earlyoom.actions.escalations | 0 | 0 | 0 | (base agrees) | r26:86 |
| earlyoom.actions.kill_failed | 0 | 0 | 0 | (base agrees) | r26:87 |
| earlyoom.actions.low_memory_warnings | 0 | 0 | 0 | (base agrees) | r26:88 |
| earlyoom.dryrun_send_lines | 0 | 1 | 0 | tool error | r26:166-167; r27:55 |
| earlyoom.process_group_lines | 0 | 0 | 0 | (base agrees) | r27:51 |
| earlyoom.earlier_invocation_send_lines | 1 | 1 | 1 | (base agrees) | r26:175-176 |
| oomd.state | inactive | inactive | inactive | (base agrees) | r26:90-92 |
| oomd.notices_this_boot | 0 | 0 | 0 | (base agrees) | r26:95, 97 |

Every pinned expectation is consistent with the rule text — no `case error` and
no `unclear text` on the compared fields.

## Fix assessment

Fix matches the case on every pinned field. Fields the fix changed vs base:
`earlyoom.actions.sigkill` 0→1, `earlyoom.dryrun_send_lines` 1→0,
`verdict` KILLERS_QUIET→KILLER_ACTED, `exit` 0→1 — exactly the four fields where
the base disagreed, all moved to the values the rule text decides. No field the
fix changed is wrong under the rule text.

Residual observation (not a ruling): `earlyoom.dryrun` prints `true` in both
outputs and is not pinned by the case. Round-26 `contract.md:94` lists the field
without pinning its semantics; under a strictly per-invocation reading of A6 the
current invocation never logged `dryrun mode enabled`, but the text does not
decide whether the flag reports "current invocation" or "any invocation this
boot" — [INFERENCE] the latter reading makes `true` defensible.

## Tools

No installs or upgrades needed; used system `python3` (stdlib `json`) and the
`read` tool only.

case_ruling=tool error
