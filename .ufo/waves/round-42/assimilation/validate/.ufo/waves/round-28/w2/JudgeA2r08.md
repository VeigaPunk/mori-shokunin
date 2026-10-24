verdict: holds — rule A2-08's three frozen cases pin only values that follow from the rule text; all passed at the freeze and still pass at f2de0ee; tool unchanged after freeze.

# JudgeA2r08 — A2-08: a `null` earlyoom journal reads `KILLERS_UNKNOWN` for any earlyoom state

## Rule text (two reads, consistent)
- `.ufo/waves/round-27/contract.md:56`: "a `null` earlyoom journal reads `KILLERS_UNKNOWN` for any earlyoom state" (frozen rule list, A2-08 row).
- `.ufo/waves/round-26/contract.md:181-182` (wave-2 fixes bullet): "a `null` journal reads `KILLERS_UNKNOWN` for any earlyoom state".
- Independent backing: `.ufo/waves/round-26/contract.md:99-101` verdict rule 2 — `KILLERS_UNKNOWN`, exit 2 when "a needed read is `null`"; `:73` — "`null` means the read failed".

## Cases (3) at f2de0ee, `tools/fixtures/mori-oom-killers/cases-a2.json` (blob `7ba553d`)

| case | earlyoom_show → state | pinned verdict/exit | follows? |
|---|---|---|---|
| `a2-08-null-journal-inactive-earlyoom` | `ActiveState=inactive` → `inactive` | `KILLERS_UNKNOWN`, exit 2 | yes |
| `a2-08-null-journal-absent-earlyoom` | `LoadState=not-found` → `absent` | `KILLERS_UNKNOWN`, exit 2 | yes |
| `a2-08-null-journal-active-earlyoom-readable-oomd` | `ActiveState=active` → `active` | `KILLERS_UNKNOWN`, exit 2 | yes |

Each pinned value follows from the rule text:
- `verdict: KILLERS_UNKNOWN`, `exit: 2` — verbatim A2-08 ("for any earlyoom state" covers inactive, absent, active); also verdict rule 2 at round-26 contract `:99-101`.
- `earlyoom.actions: null` — journal is null so actions cannot be computed; schema explicitly allows null (round-26 contract `:93-94`), and inactive/absent killers report `actions: null` (`:102-103`). For the active case, null is the only honest value — no journal, no counts.
- `earlyoom.state` — `inactive`/`active` from `ActiveState` per round-26 contract `:162` (A2b lists active/inactive as the mapped states); `absent` is in the state enum (`:90`) and `LoadState=not-found` is the only input shape that can produce it.
- `oomd.state`, `oomd.notices_this_boot` — direct reads of the inputs (`ActiveState`, `oomd_notices: 0`).
- No positive evidence in any case: journal null (no send/escalation lines), `oomd_notices` 0 → round-26 contract `:97` (KILLER_ACTED rule) not met, so nothing overrides UNKNOWN.

## Freeze selftest
- `.ufo/waves/round-28/evidence/c2-freeze-selftest.txt:1-4`: at freeze commit `d21b8bd`, `python3 -I -B tools/mori-oom-killers.py --selftest --cases tools/fixtures/mori-oom-killers/cases-a2.json` → `MORI_OOM_KILLERS_SELFTEST: PASS 30/30`, `exit=0`. No A2-08 case failed → no `tool error` / `case error` / `unclear text` ruling needed.

## Tool change after freeze?
- `git rev-parse d21b8bd:tools/mori-oom-killers.py f2de0ee:tools/mori-oom-killers.py` → identical blob `3fb78bbc2612c38e463e04083bdb213954647568`; cases file identical blob `7ba553d45e3b00d507e57132cc3c28fb140f83fd`. `git log d21b8bd..f2de0ee -- tools/mori-oom-killers.py tools/fixtures/mori-oom-killers/` → empty. Tool unchanged since freeze; the no-KILLER_ACTED-regression clause is satisfied by identity.

## Direct re-run at f2de0ee (temp extract `/fast/scratch/hyaku/mori-r28-w2/JudgeA2r08/`, never the lane)
`python3 -I -B tool.py --inputs <case>` on each of the three inputs:
- inactive: `verdict KILLERS_UNKNOWN`, exit 2, `earlyoom.state inactive`, `actions null`, `oomd.state inactive`, `notices_this_boot 0` — all pins matched.
- absent: `verdict KILLERS_UNKNOWN`, exit 2, `earlyoom.state absent`, `actions null`, `oomd.state active`, `notices_this_boot 0` — all pins matched.
- active: `verdict KILLERS_UNKNOWN`, exit 2, `earlyoom.state active`, `actions null`, `oomd.state active`, `notices_this_boot 0` — all pins matched.

## Residual risk / coverage notes (not findings)
- "Any earlyoom state" has no `unavailable`-state case. Harmless: an `unavailable` state already forces `KILLERS_UNKNOWN` via A2-02 (round-26 contract `:162`), so a missing case cannot flip a verdict.
- The `LoadState=not-found` → `absent` mapping is implicit (enum at round-26 contract `:90`, no explicit derivation line); consistent with tool output and A2-09's "removed (`not-found`)" phrasing at `:182`.

## Tooling
- No installs or upgrades performed; used stock `python3`, `git` read-only (`show`, `rev-parse`, `log`) only. No writes to the lane outside this report.
